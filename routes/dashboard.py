from flask import Blueprint, render_template
from models.skill import Skill
from services.user_service import get_user
from flask import session
from utils.auth import login_required
from utils.cultivation import get_current_rank, get_next_rank
from services.activity_service import get_recent_activities
from sqlalchemy import func
from models.learning_session import LearningSession
from database.database import db

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/home")
@login_required
def home():

    user = get_user(session["user_id"])
    
    
    
    progress_percent = user.xp % 100

    circumference = 515.2

    dash_offset = circumference * (100 - progress_percent) / 100
    
    current_rank = get_current_rank(user.xp)

    next_rank, xp_remaining = get_next_rank(user.xp)
    
    recent_activities=get_recent_activities(user.id)
    
    total_skills = Skill.query.filter_by(user_id=user.id).count()

    completed_sessions = (
        LearningSession.query
        .join(Skill)
        .filter(Skill.user_id == user.id)
        .count()
    )

    total_minutes = (
        db.session.query(func.sum(LearningSession.duration))
        .join(Skill)
        .filter(Skill.user_id == user.id)
        .scalar() or 0
    )
    
    hours = total_minutes // 60
    minutes = total_minutes % 60
    
    recent_sessions = (
        LearningSession.query
        .join(Skill)
        .filter(Skill.user_id == user.id)
        .order_by(LearningSession.created_at.desc())
        .limit(3)
        .all()
    )
    
    top_skills = (
        Skill.query
        .filter_by(user_id=user.id)
        .order_by(Skill.xp.desc())
        .limit(3)
        .all()
    )

    return render_template(
        "dashboard/home.html",
        user=user,
        progress_percent=progress_percent,
        dash_offset=dash_offset,
        current_rank=current_rank,
        next_rank=next_rank,
        xp_remaining=xp_remaining,
        recent_activities=recent_activities,
        total_skills=total_skills,
        completed_sessions=completed_sessions,
        total_minutes=total_minutes,
        minutes=minutes,
        hours=hours,
        recent_sessions=recent_sessions,
        top_skills=top_skills
    )


@dashboard_bp.route("/sessions")
def sessions():
    return render_template("dashboard/sessions.html")


@dashboard_bp.route("/rewards")
def rewards():
    return render_template("dashboard/rewards.html")

@dashboard_bp.route("/certify")
def certify():
    return render_template("dashboard/certificate.html")


@dashboard_bp.route("/community")
def community():
    return render_template("dashboard/community.html")


@dashboard_bp.route("/leaderboard")
def lead():
    return render_template("dashboard/leaderboard.html")