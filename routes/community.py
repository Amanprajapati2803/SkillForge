from pathlib import Path

from flask import Blueprint, render_template, request, redirect, url_for, session, abort, jsonify, flash, send_file
from models.user import User
from models.skill import Skill
from models.resources import Resource
from models.community_post import CommunityPost
from database.database import db
from utils.resource_files import resource_file_path, store_resource_file
from utils.auth import login_required
from services.community_service import (
    get_all_posts,
    toggle_like,
    add_comment,
    delete_comment,
    get_post_details,
)

community_bp = Blueprint("communities", __name__)


@community_bp.route("/community")
@login_required
def community():
    user = User.query.get(session["user_id"])
    posts = get_all_posts()

    return render_template(
        "dashboard/community.html",
        posts=posts,
        user=user
    )
    
@community_bp.route("/community/create", methods=["POST"])
@login_required
def create_community_post():
    title = request.form.get("title", "").strip()[:200]
    content = request.form.get("content", "").strip()
    category = request.form.get("category", "GENERAL").strip().upper()[:50]
    skill_name = request.form.get("skill_name", "").strip()[:100] or None
    external_url = request.form.get("external_url", "").strip()[:1000] or None
    attachment = request.files.get("attachment")
    attachment_key = attachment_name = None

    if not title or not content:
        flash("Add a title and a short description before posting.", "error")
        return redirect(url_for("communities.community"))

    payload = None
    if attachment and attachment.filename:
        attachment_name = Path(attachment.filename).name[:255]
        extension = Path(attachment_name).suffix.lower()
        allowed = {".pdf", ".txt", ".md", ".markdown", ".doc", ".docx", ".ppt", ".pptx", ".csv", ".xlsx", ".zip"}
        if extension not in allowed:
            flash("Upload a PDF, text/Markdown, Office document, CSV, or ZIP file.", "error")
            return redirect(url_for("communities.community"))
        payload = attachment.read(10 * 1024 * 1024 + 1)
        if not payload or len(payload) > 10 * 1024 * 1024:
            flash("Attachments must be non-empty and no larger than 10 MB.", "error")
            return redirect(url_for("communities.community"))

    if category == "RESOURCE" and not (payload or external_url):
        flash("A resource post needs an attachment or a resource link.", "error")
        return redirect(url_for("communities.community"))
    if external_url and not external_url.startswith(("https://", "http://")):
        flash("Resource links must begin with http:// or https://.", "error")
        return redirect(url_for("communities.community"))

    if payload is not None:
        attachment_key, _ = store_resource_file(payload, attachment_name)
    post = CommunityPost(
        user_id=session["user_id"], title=title, content=content,
        category=category, skill_name=skill_name,
        attachment_url=attachment_key, attachment_name=attachment_name,
        external_url=external_url,
    )
    try:
        db.session.add(post)
        db.session.commit()
    except Exception:
        db.session.rollback()
        if attachment_key:
            path = resource_file_path(attachment_key)
            if path:
                path.unlink(missing_ok=True)
        raise

    flash("Learning resource shared with the community." if category == "RESOURCE" else "Your post is live in the community.", "success")
    return redirect(url_for("communities.view_post", post_id=post.id))


@community_bp.route("/community/post/<int:post_id>")
@login_required
def view_post(post_id):

    data = get_post_details(
        post_id=post_id,
        user_id=session["user_id"]
    )

    if not data:
        abort(404)

    user_skills = Skill.query.filter_by(user_id=session["user_id"]).order_by(Skill.name.asc()).all()
    matching_skills = [skill for skill in user_skills if data["post"].skill_name and skill.name.strip().casefold() == data["post"].skill_name.strip().casefold()]
    return render_template(
        "dashboard/post_detail.html",
        **data, matching_skills=matching_skills, user_skills=user_skills,
    )


@community_bp.route("/community/post/<int:post_id>/download")
@login_required
def download_attachment(post_id):
    post = CommunityPost.query.get_or_404(post_id)
    path = resource_file_path(post.attachment_url)
    if not path:
        abort(404)
    return send_file(path, as_attachment=True, download_name=post.attachment_name or "learning-resource")


@community_bp.route("/community/post/<int:post_id>/save-to-skill", methods=["POST"])
@login_required
def save_post_to_skill(post_id):
    post = CommunityPost.query.get_or_404(post_id)
    skill = Skill.query.filter_by(id=request.form.get("skill_id", type=int), user_id=session["user_id"]).first_or_404()
    if post.skill_name and skill.name.strip().casefold() != post.skill_name.strip().casefold():
        flash(f"This resource is tagged for {post.skill_name}. Choose a matching skill to save it.", "error")
        return redirect(url_for("communities.view_post", post_id=post.id))
    if not (post.attachment_url or post.external_url):
        flash("This post does not have a downloadable resource.", "error")
        return redirect(url_for("communities.view_post", post_id=post.id))
    existing = Resource.query.filter_by(skill_id=skill.id, source_post_id=post.id).first()
    if existing:
        flash("This resource is already in your skill library.", "info")
        return redirect(url_for("skills.skill_realm", skill_id=skill.id))

    suffix = Path(post.attachment_name or "").suffix.lower()
    resource_type = "pdf" if suffix == ".pdf" else "notes" if suffix in {".txt", ".md", ".markdown"} else "other"
    resource = Resource(
        skill_id=skill.id, title=post.title[:150], resource_type=resource_type,
        url=post.external_url or "#", description=f"Shared by {post.user.name}. {post.content}"[:2000],
        difficulty="Beginner", source_post_id=post.id,
        original_filename=post.attachment_name,
    )
    db.session.add(resource)
    db.session.flush()
    if post.attachment_url:
        resource.url = url_for("skills.download_resource", resource_id=resource.id)
    db.session.commit()
    flash(f"Saved to your {skill.name} resources. You can now build a learning game from it.", "success")
    if post.attachment_url:
        path = resource_file_path(post.attachment_url)
        if path:
            return send_file(path, as_attachment=True, download_name=post.attachment_name or post.title)
    if post.external_url:
        return redirect(post.external_url)
    return redirect(url_for("skills.skill_realm", skill_id=skill.id))
    
@community_bp.route("/community/post/<int:post_id>/like", methods=["POST"])
@login_required
def like_post(post_id):

    result = toggle_like(
        post_id=post_id,
        user_id=session["user_id"]
    )

    return jsonify(result)

@community_bp.route("/community/post/<int:post_id>/comment", methods=["POST"])
@login_required
def create_comment(post_id):

    content = request.form.get("content", "").strip()

    if not content:
        return redirect(url_for("communities.view_post", post_id=post_id))

    add_comment(
        post_id=post_id,
        user_id=session["user_id"],
        content=content,
    )

    return redirect(url_for("communities.view_post", post_id=post_id))

@community_bp.route("/community/comment/<int:comment_id>/delete", methods=["POST"])
@login_required
def remove_comment(comment_id):

    delete_comment(
        comment_id=comment_id,
        user_id=session["user_id"],
    )

    return redirect(request.referrer or url_for("communities.community"))