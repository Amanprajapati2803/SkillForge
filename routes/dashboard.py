from flask import Blueprint, render_template, redirect, flash, url_for
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
from services.challenge_service import ensure_daily_challenges, claim_challenge_reward
from models.daily_challenge import DailyChallenge
from datetime import datetime, timezone

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
    recent_activities = get_recent_activities(user.id)

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
    flash(message, "success" if success else "error")
    return redirect(url_for("dashboard.home"))


@dashboard_bp.route("/sessions")
@login_required
def sessions():
    user = User.query.get(session["user_id"])

    # Fetch all learning sessions for this user
    user_skills = Skill.query.filter_by(user_id=user.id).all()
    skill_ids = [s.id for s in user_skills]

    all_sessions = []
    if skill_ids:
        all_sessions = (
            LearningSession.query
            .filter(LearningSession.skill_id.in_(skill_ids))
            .order_by(LearningSession.created_at.desc())
            .all()
        )

    # Categorize sessions (handle naive vs aware datetime mismatch)
    from datetime import datetime, timedelta, timezone
    now = datetime.now(timezone.utc)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

    live_sessions = []
    recorded_sessions = []

    for s in all_sessions:
        if not s.created_at:
            continue
        # Make both datetimes aware for comparison
        session_time = s.created_at
        if session_time.tzinfo is None:
            session_time = session_time.replace(tzinfo=timezone.utc)

        if session_time >= today_start:
            live_sessions.append(s)
        else:
            recorded_sessions.append(s)

    # Total stats
    total_minutes = sum(s.duration or 0 for s in all_sessions)
    total_xp = sum(s.xp_earned or 0 for s in all_sessions)

    return render_template(
        "dashboard/sessions.html",
        user=user,
        all_sessions=all_sessions,
        live_sessions=live_sessions,
        recorded_sessions=recorded_sessions,
        total_minutes=total_minutes,
        total_xp=total_xp,
        session_count=len(all_sessions)
    )


@dashboard_bp.route("/rewards")
@login_required
def rewards():
    user = User.query.get(session["user_id"])
    return render_template("dashboard/rewards.html", user=user)


@dashboard_bp.route("/certify")
@login_required
def certify():
    user = User.query.get(session["user_id"])
    return render_template("dashboard/certificate.html", user=user)


# @dashboard_bp.route("/community")
# def community():
#     return render_template("dashboard/community.html")

@dashboard_bp.route("/leaderboard")
@login_required
def leaderboard():
    users = User.query.order_by(User.xp.desc()).all()

 # assign rank 
    for index, u in enumerate(users, start=1):
        u.rank = index
        u.sect_title = get_sect_title(u.level)
        
    top_users = users[:3]

    current_user_obj = next(
        (u for u in users if u.id == session["user_id"]),
        None
    )

    total_users = len(users)

    if current_user_obj:
        percentile = round(
            ((total_users - current_user_obj.rank + 1) / total_users) * 100
        )
    else:
        percentile = 0

    next_rank = None
    xp_needed = 0

    if current_user_obj and current_user_obj.rank > 1:
        next_rank = users[current_user_obj.rank - 2]
        xp_needed = max(0, next_rank.xp - current_user_obj.xp + 1)



    return render_template(
        "dashboard/leaderboard.html",
        user=current_user_obj,
        users=users,
        top_users=top_users,
        current_user=current_user_obj,
        total_users=total_users,
        percentile=percentile,
        next_rank=next_rank,
        xp_needed=xp_needed
    )