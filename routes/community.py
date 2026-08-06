from flask import Blueprint, render_template, request, redirect, url_for, session, abort,jsonify

from utils.auth import login_required
from services.community_service import (
    create_post,
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

    posts = get_all_posts()

    return render_template(
        "dashboard/community.html",
        posts=posts
    )
    
@community_bp.route("/community/create", methods=["POST"])
@login_required
def create_community_post():

    title = request.form.get("title")
    content = request.form.get("content")
    category = request.form.get("category")

    image = request.files.get("image")
    attachment = request.files.get("attachment")

    image_url = None
    attachment_url = None

    create_post(
        user_id=session["user_id"],
        title=title,
        content=content,
        category=category,
        image_url=image_url,
        attachment_url=attachment_url,
    )

    return redirect(url_for("communities.community"))

@community_bp.route("/community/post/<int:post_id>")
@login_required
def view_post(post_id):

    data = get_post_details(
        post_id=post_id,
        user_id=session["user_id"]
    )

    if not data:
        abort(404)

    return render_template(
        "dashboard/post_detail.html",
        **data
    )
    
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