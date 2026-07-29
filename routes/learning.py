from flask import Blueprint, request, redirect, url_for,session
from database.database import db
from models.skill import Skill
from models.learning_session import LearningSession
from utils.progression import calculate_session_xp
from utils.progression import (
    calculate_session_xp,award_skill_xp,award_user_xp,remove_skill_xp,remove_user_xp
)
from utils.auth import login_required
from services.challenge_service import update_challenge_progress
from models.user import User
from utils.achievements import check_achievements

learning_bp = Blueprint("learning_session", __name__)


@learning_bp.route("/skill/<int:skill_id>/session/add", methods=["POST"])
@login_required
def add_session(skill_id):

    skill = Skill.query.filter_by(
        id=skill_id,
        user_id=session["user_id"]
    ).first_or_404()

    duration = int(request.form["duration"])
    xp = calculate_session_xp(duration)

    learning_session = LearningSession(
        skill_id=skill.id,
        title=request.form["title"],
        duration=duration,
        notes=request.form.get("notes"),
        xp_earned=xp,
    )
    
    award_skill_xp(skill, xp)

    activity = award_user_xp(
        skill.user,
        xp,
        f"Completed learning session: {learning_session.title}"
    )

    db.session.add(learning_session)
    
    if activity:
        db.session.add(activity)
        
    
    db.session.commit()
    
    check_achievements(skill.user)
    
    update_challenge_progress(
        session["user_id"],
        "Practice Sessions"
    )

    return redirect(
        url_for("skills.skill_realm", skill_id=skill.id)
    )


@learning_bp.route(
    "/session/<int:session_id>/delete",
    methods=["POST"]
)
@login_required
def delete_session(session_id):

    learning_session = LearningSession.query.get_or_404(session_id)

    skill = Skill.query.filter_by(
        id=learning_session.skill_id,
        user_id=session["user_id"]
    ).first_or_404()

    # Reverse the XP that this session awarded
    remove_skill_xp(skill, learning_session.xp_earned)
    remove_user_xp(skill.user, learning_session.xp_earned)

    # Delete the session
    db.session.delete(learning_session)

    db.session.commit()

    return redirect(
        url_for("skills.skill_realm", skill_id=skill.id)
    )
    

@learning_bp.route(
    "/session/<int:session_id>/edit",
    methods=["POST"]
)
@login_required
def edit_session(session_id):

    learning_session = LearningSession.query.get_or_404(session_id)

    skill = Skill.query.filter_by(
        id=learning_session.skill_id,
        user_id=session["user_id"]
    ).first_or_404()
    
    remove_skill_xp(skill, learning_session.xp_earned)
    remove_user_xp(skill.user, learning_session.xp_earned)

    learning_session.title = request.form["title"]

    learning_session.duration = int(
        request.form["duration"]
    )

    learning_session.notes = request.form.get("notes")
    
    new_xp = calculate_session_xp(
        learning_session.duration
    )
    
    learning_session.xp_earned = new_xp
    
    award_skill_xp(skill, new_xp)

    activity = award_user_xp(
        skill.user,
        new_xp,
        f"Updated learning session: {learning_session.title}"
    )
    
    if activity:
        db.session.add(activity)

    db.session.commit()

    check_achievements(skill.user)
    
    return redirect(
        url_for("skills.skill_realm", skill_id=skill.id)
    )
