from flask import Blueprint, render_template, session
from utils.auth import login_required
from models.achievement import Achievement
from models.user_achievement import UserAchievement

achievement_bp = Blueprint("achievement", __name__)


@achievement_bp.route("/achievements")
@login_required
def achievements():

    achievements = Achievement.query.all()

    unlocked = UserAchievement.query.filter_by(
        user_id=session["user_id"]
    ).all()

    unlocked_ids = {
        achievement.achievement_id
        for achievement in unlocked
    }

    return render_template(
        "dashboard/achievement.html",
        achievements=achievements,
        unlocked_ids=unlocked_ids,
        unlocked_count=len(unlocked_ids),
        total_count=len(achievements),
    )