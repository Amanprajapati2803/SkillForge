from flask import Blueprint, session, render_template, request, url_for, redirect, flash, send_file
from models.skill import Skill
from models.learning_session import LearningSession
from models.resources import Resource
from models.learning_game import LearningGame, LearningGameProgress
from utils.auth import login_required
from database.database import db
from utils.progression import award_skill_xp, award_user_xp
from models.user import User
from services.achievement_service import unlock_achievement
from services.challenge_service import update_challenge_progress
from utils.achievements import check_achievements
from utils.cultivation import get_current_rank
from datetime import datetime, timezone
from services.skill_progress import get_skill_progress
from utils.resource_files import resource_file_path

skills_bp = Blueprint("skills", __name__)


@skills_bp.route("/skills", methods=["GET", "POST"])
@login_required
def skills():
    user = User.query.get(session["user_id"])

    if request.method == "POST":
        skill_name = request.form.get("skill_name", "").strip()
        if not skill_name:
            flash("Skill name cannot be empty.", "error")
            return redirect(url_for("skills.skills"))

        new_skill = Skill(name=skill_name, user_id=session["user_id"])
        db.session.add(new_skill)
        db.session.commit()

        check_achievements(user)
        update_challenge_progress(session["user_id"], "Skill Builder")
        unlock_achievement(session["user_id"], "First Step")

        flash(f"Added {skill_name} to your skills.", "success")
        return redirect(url_for("skills.skills"))

    skills = Skill.query.filter_by(user_id=session["user_id"]).all()

    total_xp = user.xp
    current_rank = get_current_rank(total_xp)
    skill_count = len(skills)

    skill_progress = get_skill_progress(user.id)
    game_progress = {skill_id: evidence["percent"] for skill_id, evidence in skill_progress.items()}


    return render_template(
        "dashboard/skills.html",
        skills=skills,
        user=user,
        total_xp=total_xp,
        current_rank=current_rank,
        skill_count=skill_count,
        game_progress=game_progress,
        skill_progress=skill_progress,
        resource_count=Resource.query.join(Skill).filter(Skill.user_id == user.id).count(),
        demonstrated_count=sum(1 for item in skill_progress.values() if item["demonstrated"]),
    )


@skills_bp.route("/skills/delete/<int:skill_id>", methods=["POST"])
@login_required
def delete_skill(skill_id):
    skill = Skill.query.filter_by(id=skill_id, user_id=session["user_id"]).first()
    if skill:
        db.session.delete(skill)
        db.session.commit()
        flash(f"Technique '{skill.name}' has been forgotten.", "info")
    else:
        flash("Technique not found.", "error")
    return redirect(url_for("skills.skills"))


@skills_bp.route("/skills/edit/<int:skill_id>", methods=["POST"])
@login_required
def edit_skill(skill_id):
    skill = Skill.query.filter_by(
        id=skill_id, user_id=session["user_id"]
    ).first_or_404()

    new_name = request.form.get("skill_name", "").strip()
    if new_name:
        skill.name = new_name
        db.session.commit()
        flash("Technique renamed successfully.", "success")
    else:
        flash("Name cannot be empty.", "error")

    return redirect(url_for("skills.skills"))


@skills_bp.route("/skills/<int:skill_id>/add-xp", methods=["POST"])
@login_required
def add_skill_xp(skill_id):
    skill = Skill.query.filter_by(
        id=skill_id, user_id=session["user_id"]
    ).first_or_404()

    # ========== COOLDOWN & DAILY CAP SYSTEM ==========
    COOLDOWN_MINUTES = 15
    DAILY_XP_CAP = 100
    xp_amount = 10

    # Initialize cooldown tracking in session
    if "xp_cooldowns" not in session:
        session["xp_cooldowns"] = {}

    skill_key = f"skill_{skill_id}"
    now = datetime.now(timezone.utc)
    today_str = now.strftime("%Y-%m-%d")

    # Get or create tracking data for this skill
    tracking = session["xp_cooldowns"].get(skill_key, {
        "last_click": None,
        "daily_xp": 0,
        "date": today_str
    })

    # Reset daily XP if it's a new day
    if tracking.get("date") != today_str:
        tracking["daily_xp"] = 0
        tracking["date"] = today_str

    # Check daily cap
    if tracking["daily_xp"] >= DAILY_XP_CAP:
        flash(f"⚠️ Daily cultivation limit reached for {skill.name}! (Max {DAILY_XP_CAP} XP/day)", "error")
        return redirect(url_for("skills.skills"))

    # Check cooldown
    if tracking["last_click"]:
        last_click = datetime.fromisoformat(tracking["last_click"])
        minutes_since = (now - last_click).total_seconds() / 60
        if minutes_since < COOLDOWN_MINUTES:
            mins_left = int(COOLDOWN_MINUTES - minutes_since)
            flash(f"⏳ Your qi needs {mins_left} more minute{'s' if mins_left != 1 else ''} to recover before cultivating {skill.name} again!", "error")
            return redirect(url_for("skills.skills"))

    # ========== AWARD XP ==========
    award_skill_xp(skill, xp_amount)

    session_record = LearningSession(
        skill_id=skill.id,
        title=f"Practiced {skill.name}",
        duration=15,
        notes="Quick practice session from skill page",
        xp_earned=xp_amount,
        created_at=now
    )
    db.session.add(session_record)

    activity = award_user_xp(skill.user, xp_amount, f"Practiced {skill.name}")
    if activity:
        db.session.add(activity)

    db.session.commit()
    check_achievements(skill.user)
    update_challenge_progress(session["user_id"], "Practice Sessions")

    # Update tracking
    tracking["last_click"] = now.isoformat()
    tracking["daily_xp"] = tracking.get("daily_xp", 0) + xp_amount
    session["xp_cooldowns"][skill_key] = tracking
    session.modified = True

    remaining = DAILY_XP_CAP - tracking["daily_xp"]
    flash(f"✨ +{xp_amount} XP gained in {skill.name}! ({remaining} XP remaining today)", "success")
    return redirect(url_for("skills.skills"))


@skills_bp.route("/skills/<int:skill_id>")
@login_required
def skill_realm(skill_id):
    user = User.query.get(session["user_id"])
    skill = Skill.query.filter_by(
        id=skill_id,
        user_id=session["user_id"]
    ).first_or_404()

    # FIXED: removed .order_by(Resource.created_at.desc()) since Resource has no created_at
    resources = Resource.query.filter_by(skill_id=skill.id).all()

    games = LearningGame.query.filter_by(skill_id=skill.id).order_by(LearningGame.created_at.desc()).all()
    progress_by_game = {item.game_id: item for item in LearningGameProgress.query.filter_by(user_id=user.id).all()}
    game_progress = {game.id: progress_by_game.get(game.id) for game in games}

    sessions = sorted(
        skill.sessions,
        key=lambda s: s.created_at if s.created_at else datetime.min.replace(tzinfo=timezone.utc),
        reverse=True
    )

    return render_template(
        "dashboard/skill_realm.html",
        user=user,
        skill=skill,
        resources=resources,
        sessions=sessions,
        games=games,
        game_progress=game_progress,
        skill_learning_progress=get_skill_progress(user.id).get(skill.id, {"percent": 0, "studied": 0, "total": 0, "best_accuracy": 0, "attempts": 0, "demonstrated": False, "resources": 0}),
    )


# ==================== RESOURCE CRUD ====================

@skills_bp.route("/skills/<int:skill_id>/resources/add", methods=["POST"])
@login_required
def add_resource(skill_id):
    skill = Skill.query.filter_by(
        id=skill_id, user_id=session["user_id"]
    ).first_or_404()

    title = request.form.get("title", "").strip()
    resource_type = request.form.get("resource_type", "other")
    url = request.form.get("url", "").strip()
    description = request.form.get("description", "").strip()
    difficulty = request.form.get("difficulty", "Beginner")

    if not title or not url:
        flash("Title and URL are required.", "error")
        return redirect(url_for("skills.skill_realm", skill_id=skill.id))

    new_resource = Resource(
        skill_id=skill.id,
        title=title,
        resource_type=resource_type,
        url=url,
        description=description,
        difficulty=difficulty
    )
    db.session.add(new_resource)
    db.session.commit()

    update_challenge_progress(session["user_id"], "Resource Collector")
    flash(f"Resource '{title}' added to {skill.name} archive!", "success")
    return redirect(url_for("skills.skill_realm", skill_id=skill.id))


@skills_bp.route("/resources/<int:resource_id>/download")
@login_required
def download_resource(resource_id):
    resource = Resource.query.get_or_404(resource_id)
    Skill.query.filter_by(id=resource.skill_id, user_id=session["user_id"]).first_or_404()
    if resource.storage_key:
        path = resource_file_path(resource.storage_key)
        if not path:
            flash("The saved file is missing from storage.", "error")
            return redirect(url_for("skills.skill_realm", skill_id=resource.skill_id))
        return send_file(path, as_attachment=True, download_name=resource.original_filename or resource.title)
    if resource.source_post_id:
        from models.community_post import CommunityPost
        post = CommunityPost.query.get(resource.source_post_id)
        if post and post.attachment_url:
            return redirect(url_for("communities.download_attachment", post_id=post.id))
        if post and post.external_url:
            return redirect(post.external_url)
    if resource.url and resource.url != "#":
        return redirect(resource.url)
    flash("This resource has no file or link to open.", "error")
    return redirect(url_for("skills.skill_realm", skill_id=resource.skill_id))


@skills_bp.route("/resources/<int:resource_id>/delete", methods=["POST"])
@login_required
def delete_resource(resource_id):
    resource = Resource.query.get_or_404(resource_id)
    skill = Skill.query.filter_by(
        id=resource.skill_id, user_id=session["user_id"]
    ).first_or_404()

    storage_key = resource.storage_key
    db.session.delete(resource)
    db.session.commit()
    if storage_key:
        path = resource_file_path(storage_key)
        if path:
            path.unlink(missing_ok=True)
    flash("Resource removed from archive.", "info")
    return redirect(url_for("skills.skill_realm", skill_id=skill.id))


@skills_bp.route("/resources/<int:resource_id>/edit", methods=["POST"])
@login_required
def edit_resource(resource_id):
    resource = Resource.query.get_or_404(resource_id)
    skill = Skill.query.filter_by(
        id=resource.skill_id, user_id=session["user_id"]
    ).first_or_404()

    resource.title = request.form.get("title", resource.title)
    resource.resource_type = request.form.get("resource_type", resource.resource_type)
    resource.url = request.form.get("url", resource.url)
    resource.description = request.form.get("description", resource.description)
    resource.difficulty = request.form.get("difficulty", resource.difficulty)

    db.session.commit()
    flash("Resource updated successfully.", "success")
    return redirect(url_for("skills.skill_realm", skill_id=skill.id))