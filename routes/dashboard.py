from flask import Blueprint, render_template,redirect,flash,url_for
from models.skill import Skill
from services.user_service import get_user
from flask import session
from utils.auth import login_required
from utils.cultivation import get_current_rank, get_next_rank
from services.activity_service import get_recent_activities
from sqlalchemy import func
from models.learning_session import LearningSession
from database.database import db
from models.user import User
from utils.titles import get_sect_title
from services.challenge_service import ensure_daily_challenges,claim_challenge_reward
from models.daily_challenge import DailyChallenge
from datetime import datetime,timezone

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/home")
@login_required
def home():

    user = get_user(session["user_id"])
    
    ensure_daily_challenges(user.id)
    
    
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
    
    today = datetime.now(timezone.utc).date()

    daily_challenges = (
        DailyChallenge.query
        .filter_by(user_id=user.id)
        .all()
    )

    daily_challenges = [
        challenge
        for challenge in daily_challenges
        if challenge.created_at.date() == today
    ]

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
        top_skills=top_skills,
        daily_challenges=daily_challenges
    )
    
@dashboard_bp.route("/challenge/<int:challenge_id>/claim", methods=["POST"])
@login_required
def claim_challenge(challenge_id):

    success, message = claim_challenge_reward(
        challenge_id,
        session["user_id"]
    )

    flash(message)

    return redirect(url_for("dashboard.home"))


@dashboard_bp.route("/sessions")
def sessions():
    return render_template("dashboard/sessions.html", user=session["user_id"])


@dashboard_bp.route("/rewards")
def rewards():
    return render_template("dashboard/rewards.html",user=session["user_id"])

@dashboard_bp.route("/certify")
def certify():
    return render_template("dashboard/certificate.html",user=session["user_id"])


@dashboard_bp.route("/community")
def community():
    return render_template("dashboard/community.html")

@dashboard_bp.route("/leaderboard")
@login_required
def leaderboard():
    users = User.query.order_by(User.xp.desc()).all()

    # Assign ranks
    for index, user in enumerate(users, start=1):
        user.rank = index

    top_users = users[:3]

    current_user = next(
        (user for user in users if user.id == session["user_id"]),
        None
    )

    total_users = len(users)

    if current_user:
        percentile = round(
            ((total_users - current_user.rank + 1) / total_users) * 100
        )
    else:
        percentile = 0
        
    next_rank = None
    xp_needed = 0

    if current_user and current_user.rank > 1:
        next_rank = users[current_user.rank - 2]
        xp_needed = max(0, next_rank.xp - current_user.xp + 1)    

    for index, user in enumerate(users, start=1):
        user.rank = index
        user.sect_title = get_sect_title(user.level)
        
    return render_template(
        "dashboard/leaderboard.html",
        users=users,
        top_users=top_users,
        current_user=current_user,
        total_users=total_users,
        percentile=percentile,
        next_rank=next_rank,
        xp_needed=xp_needed
    )