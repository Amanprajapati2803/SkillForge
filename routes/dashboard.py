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
    skills = Skill.query.filter_by(user_id=user.id).order_by(Skill.name.asc()).all()
    from services.skill_progress import get_skill_progress
    from models.learning_game import LearningGame, LearningGameProgress
    from models.resources import Resource
    from models.applied_internship import AppliedInternship

    skill_progress = get_skill_progress(user.id)
    recent_games = (LearningGame.query.join(Skill)
                    .filter(Skill.user_id == user.id)
                    .order_by(LearningGame.created_at.desc()).limit(5).all())
    progress_by_game = {
        item.game_id: item
        for item in LearningGameProgress.query.filter_by(user_id=user.id).all()
    }
    next_game = next((game for game in recent_games
                      if len(game.sections or []) > (progress_by_game.get(game.id).completed_sections if progress_by_game.get(game.id) else 0)), None)
    if next_game:
        next_game_progress = progress_by_game.get(next_game.id)
        next_action_url = url_for("learning_game.play", game_id=next_game.id)
        next_action_label = "Continue learning"
        completed = next_game_progress.completed_sections if next_game_progress else 0
        next_action_detail = f"{next_game.source_title} · Stage {completed + 1} of {len(next_game.sections)}"
    elif recent_games:
        next_game = recent_games[0]
        next_action_url = url_for("learning_game.play", game_id=next_game.id, mode="match")
        next_action_label = "Play the skill challenge"
        next_action_detail = f"Your study stages are ready for a quiz · {next_game.skill.name}"
    elif skills:
        next_action_url = url_for("skills.skill_realm", skill_id=skills[0].id)
        next_action_label = "Add a learning resource"
        next_action_detail = f"Start with {skills[0].name}"
    else:
        next_action_url = url_for("skills.skills")
        next_action_label = "Add your first skill"
        next_action_detail = "Choose a skill you want to learn"

    recent_applications = (AppliedInternship.query.filter_by(user_id=user.id)
                           .order_by(AppliedInternship.applied_at.desc()).limit(3).all())
    resources_count = Resource.query.join(Skill).filter(Skill.user_id == user.id).count()
    demonstrated_count = sum(1 for item in skill_progress.values() if item["demonstrated"])

    return render_template(
        "dashboard/home.html", user=user, skills=skills,
        skill_progress=skill_progress, recent_games=recent_games,
        game_progress_by_id=progress_by_game,
        recent_applications=recent_applications, resources_count=resources_count,
        demonstrated_count=demonstrated_count, next_action_url=next_action_url,
        next_action_label=next_action_label, next_action_detail=next_action_detail,
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
    return redirect(url_for("dashboard.home"))

@dashboard_bp.route("/rewards")
@login_required
def rewards():
    return redirect(url_for("dashboard.home"))

@dashboard_bp.route("/certify")
@login_required
def certify():
    return redirect(url_for("dashboard.home"))

@dashboard_bp.route("/leaderboard")
@login_required
def leaderboard():
    return redirect(url_for("dashboard.home"))