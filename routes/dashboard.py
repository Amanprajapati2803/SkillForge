from flask import Blueprint, render_template
from services.user_service import get_user
from flask import session
from utils.auth import login_required
from utils.cultivation import get_current_rank, get_next_rank
from services.activity_service import get_recent_activities

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

    return render_template(
        "dashboard/home.html",
        user=user,
        progress_percent=progress_percent,
        dash_offset=dash_offset,
        current_rank=current_rank,
        next_rank=next_rank,
        xp_remaining=xp_remaining,
        recent_activities=recent_activities
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