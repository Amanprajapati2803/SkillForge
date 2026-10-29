import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

from flask import Blueprint, abort, flash, redirect, render_template, request, session, url_for

from database.database import db
from models.learning_game import LearningGame, LearningGameMatch, LearningGameProgress
from models.resources import Resource
from models.community_post import CommunityPost
from models.skill import Skill
from models.user import User
from services.game_builder import build_game, extract_text
from services.story_mode import get_story_scene
from utils.auth import login_required
from utils.progression import award_skill_xp, award_user_xp
from utils.resource_files import resource_file_path, store_resource_file

learning_game_bp = Blueprint("learning_game", __name__)
MAX_RESOURCE_BYTES = 10 * 1024 * 1024
PASS_SCORE = 70
ROUND_SECONDS = 12
ROPE_EDGE = 3
BOT_RULES = {
    "easy": {"accuracy": 0.42, "delay": (5.0, 11.5)},
    "medium": {"accuracy": 0.68, "delay": (3.0, 9.0)},
    "hard": {"accuracy": 0.86, "delay": (1.5, 7.5)},
}


def _owned_game(game_id):
    return LearningGame.query.join(Skill).filter(
        LearningGame.id == game_id,
        Skill.user_id == session["user_id"],
    ).first_or_404()


def _progress_for(game):
    progress = LearningGameProgress.query.filter_by(
        user_id=session["user_id"], game_id=game.id
    ).first()
    if progress is None:
        progress = LearningGameProgress(user_id=session["user_id"], game_id=game.id)
        db.session.add(progress)
        db.session.flush()
    return progress


def _refresh_question_bank(game):
    # Older saved games may contain only one question per stage. Rebuild from
    # the stored study text so they also get multiple tug-of-war rounds.
    if len(game.questions or []) < 3:
        source = "\n\n".join(section.get("body", "") for section in game.sections)
        try:
            _, questions = build_game(source)
        except ValueError:
            return
        if len(questions) > len(game.questions or []):
            game.questions = questions
            db.session.commit()


def _owned_match(game_id, match_id):
    return LearningGameMatch.query.filter_by(
        id=match_id, game_id=game_id, user_id=session["user_id"]
    ).first_or_404()


def _utc(value):
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def _schedule_round(match, started_at=None):
    started_at = started_at or datetime.now(timezone.utc)
    rules = BOT_RULES.get(match.difficulty, BOT_RULES["medium"])
    match.round_deadline_at = started_at + timedelta(seconds=ROUND_SECONDS)
    match.bot_has_answer = random.random() < rules["accuracy"]
    match.bot_answer_at = None
    if match.bot_has_answer:
        delay = random.uniform(*rules["delay"])
        if delay < ROUND_SECONDS:
            match.bot_answer_at = started_at + timedelta(seconds=delay)
        else:
            match.bot_has_answer = False


def _finish_match(game, match):
    match.status = "completed"
    match.finished_at = datetime.now(timezone.utc)
    rounds_played = len(match.rounds or [])
    score = round((match.player_correct / rounds_played) * 100) if rounds_played else 0
    progress = LearningGameProgress.query.filter_by(
        user_id=match.user_id, game_id=game.id
    ).first()
    if progress is None:
        progress = LearningGameProgress(user_id=match.user_id, game_id=game.id)
        db.session.add(progress)
        db.session.flush()
    first_pass = score >= PASS_SCORE and not progress.quiz_passed
    progress.attempts += 1
    progress.best_score = max(progress.best_score, score)
    progress.quiz_passed = progress.quiz_passed or score >= PASS_SCORE
    progress.updated_at = datetime.now(timezone.utc)

    if first_pass:
        user = User.query.get(match.user_id)
        award_skill_xp(game.skill, 20)
        activity = award_user_xp(user, 20, f"Passed the learning game: {game.source_title}")
        if activity:
            db.session.add(activity)
    return score, first_pass


def _resolve_round(game, match, selected_index=None, timed_out=False):
    if match.status != "active":
        return "This tug-of-war is already finished."

    now = datetime.now(timezone.utc)
    deadline = _utc(match.round_deadline_at)
    if now >= deadline:
        timed_out = True
        selected_index = None

    question_index = match.question_order[match.current_round]
    question = game.questions[question_index]
    is_correct = selected_index == question["answer_index"]
    bot_at = _utc(match.bot_answer_at) if match.bot_answer_at else None
    bot_was_first = bool(match.bot_has_answer and bot_at and bot_at <= now and bot_at <= deadline)

    if is_correct:
        match.player_correct += 1
    if bot_was_first:
        match.bot_correct += 1

    if timed_out:
        outcome = "bot"
        reason = "Time ran out. The computer pulled the rope."
    elif is_correct and not bot_was_first:
        outcome = "player"
        reason = "Correct and first! You pulled the rope."
    elif bot_was_first:
        outcome = "bot"
        reason = "The computer answered correctly first and pulled the rope."
    else:
        outcome = "bot"
        reason = "That answer was incorrect. The computer pulled the rope."

    match.rope_position = max(-ROPE_EDGE, min(ROPE_EDGE, match.rope_position + (1 if outcome == "player" else -1)))
    match.rounds = (match.rounds or []) + [{
        "question_index": question_index,
        "selected_index": selected_index,
        "correct": bool(is_correct),
        "outcome": outcome,
        "reason": reason,
        "rope_after": match.rope_position,
    }]

    match.current_round += 1
    questions_exhausted = match.current_round >= len(match.question_order)
    rope_reached_end = abs(match.rope_position) >= ROPE_EDGE
    if questions_exhausted or rope_reached_end:
        score, first_pass = _finish_match(game, match)
        if first_pass:
            reason += f" You passed with {score}% and earned 20 XP."
        elif score >= PASS_SCORE:
            reason += f" Your best score is saved ({score}%)."
        else:
            reason += f" Match accuracy: {score}%; {PASS_SCORE}% is needed to demonstrate the skill."
    else:
        _schedule_round(match, now)

    db.session.commit()
    return reason


@learning_game_bp.route("/skills/<int:skill_id>/games/upload", methods=["POST"])
@login_required
def upload_resource(skill_id):
    skill = Skill.query.filter_by(id=skill_id, user_id=session["user_id"]).first_or_404()
    upload = request.files.get("material")
    if not upload or not upload.filename:
        flash("Choose a resource file first.", "error")
        return redirect(url_for("skills.skill_realm", skill_id=skill.id))

    payload = upload.read(MAX_RESOURCE_BYTES + 1)
    if not payload:
        flash("That file is empty.", "error")
        return redirect(url_for("skills.skill_realm", skill_id=skill.id))
    if len(payload) > MAX_RESOURCE_BYTES:
        flash("The maximum resource size is 10 MB.", "error")
        return redirect(url_for("skills.skill_realm", skill_id=skill.id))

    try:
        source_text = extract_text(upload.filename, payload)
        sections, questions = build_game(source_text)
    except ValueError as exc:
        flash(str(exc), "error")
        return redirect(url_for("skills.skill_realm", skill_id=skill.id))

    title = (request.form.get("title") or Path(upload.filename).stem).strip()[:180]
    storage_key, original_filename = store_resource_file(payload, upload.filename)
    resource = Resource(
        skill_id=skill.id, title=(title or "Learning resource")[:150],
        resource_type="pdf" if Path(original_filename).suffix.lower() == ".pdf" else "notes",
        url="#", description="Uploaded learning material used to build this game.",
        difficulty="Beginner", storage_key=storage_key, original_filename=original_filename,
    )
    db.session.add(resource)
    db.session.flush()
    resource.url = url_for("skills.download_resource", resource_id=resource.id)
    game = LearningGame(
        skill_id=skill.id,
        source_title=title or "Learning resource",
        sections=sections,
        questions=questions,
    )
    db.session.add(game)
    db.session.flush()
    db.session.add(LearningGameProgress(user_id=session["user_id"], game_id=game.id))
    db.session.commit()

    flash(f"Saved your resource and built {len(sections)} study stages with {len(questions)} one-question rounds.", "success")
    return redirect(url_for("learning_game.play", game_id=game.id))


@learning_game_bp.route("/resources/<int:resource_id>/build-game", methods=["POST"])
@login_required
def build_game_from_resource(resource_id):
    resource = Resource.query.join(Skill).filter(
        Resource.id == resource_id, Skill.user_id == session["user_id"]
    ).first_or_404()
    filename = resource.original_filename
    path = resource_file_path(resource.storage_key) if resource.storage_key else None
    if resource.source_post_id:
        post = CommunityPost.query.get(resource.source_post_id)
        if post:
            filename = filename or post.attachment_name
            path = resource_file_path(post.attachment_url) if post.attachment_url else None
    if not path or not filename:
        flash("This saved item has no supported file to turn into a game. Download or open the original link instead.", "error")
        return redirect(url_for("skills.skill_realm", skill_id=resource.skill_id))
    try:
        source_text = extract_text(filename, path.read_bytes())
        sections, questions = build_game(source_text)
    except ValueError as exc:
        flash(str(exc), "error")
        return redirect(url_for("skills.skill_realm", skill_id=resource.skill_id))
    game = LearningGame(
        skill_id=resource.skill_id, source_title=resource.title[:180],
        sections=sections, questions=questions,
    )
    db.session.add(game)
    db.session.flush()
    db.session.add(LearningGameProgress(user_id=session["user_id"], game_id=game.id))
    db.session.commit()
    flash(f"Built a learning game from {resource.title}.", "success")
    return redirect(url_for("learning_game.play", game_id=game.id))


@learning_game_bp.route("/games/<int:game_id>")
@login_required
def play(game_id):
    game = _owned_game(game_id)
    progress = _progress_for(game)
    section_count = len(game.sections)
    mode = request.args.get("mode", "study")
    pending_checkpoint = session.get("story_checkpoint") or {}
    if (mode != "checkpoint" and pending_checkpoint.get("game_id") == game.id
            and pending_checkpoint.get("milestone") == progress.completed_sections):
        return redirect(url_for("learning_game.play", game_id=game.id, mode="checkpoint"))
    if mode == "checkpoint":
        checkpoint = session.get("story_checkpoint") or {}
        if checkpoint.get("game_id") != game.id or checkpoint.get("milestone") != progress.completed_sections:
            return redirect(url_for("learning_game.play", game_id=game.id, section=progress.completed_sections))
        question_index = checkpoint.get("question_index", -1)
        if not isinstance(question_index, int) or question_index < 0 or question_index >= len(game.questions):
            session.pop("story_checkpoint", None)
            return redirect(url_for("learning_game.play", game_id=game.id, section=progress.completed_sections))
        return render_template(
            "game/checkpoint.html", game=game, question=game.questions[question_index],
            milestone=progress.completed_sections, section_count=section_count,
        )
    if mode in {"quiz", "match"}:
        if progress.completed_sections < section_count:
            flash("Finish each learning stage before starting a tug-of-war.", "info")
            return redirect(url_for("learning_game.play", game_id=game.id, section=progress.completed_sections))
        _refresh_question_bank(game)
        latest_match = LearningGameMatch.query.filter_by(
            user_id=session["user_id"], game_id=game.id
        ).order_by(LearningGameMatch.created_at.desc()).first()
        return render_template(
            "game/match_lobby.html", game=game, progress=progress,
            latest_match=latest_match, pass_score=PASS_SCORE,
        )

    if progress.completed_sections >= section_count:
        return redirect(url_for("learning_game.play", game_id=game.id, mode="match"))
    try:
        section_index = int(request.args.get("section", progress.completed_sections))
    except (TypeError, ValueError):
        section_index = progress.completed_sections
    section_index = max(0, min(section_index, section_count - 1))
    section = game.sections[section_index]
    return render_template(
        "game/play.html", game=game, progress=progress, mode="study",
        section=section, section_index=section_index, section_count=section_count,
        story=get_story_scene(section_index, game.source_title, section.get("body", "")),
    )


@learning_game_bp.route("/games/<int:game_id>/checkpoint/answer", methods=["POST"])
@login_required
def answer_story_checkpoint(game_id):
    game = _owned_game(game_id)
    checkpoint = session.get("story_checkpoint") or {}
    progress = _progress_for(game)
    if checkpoint.get("game_id") != game.id or checkpoint.get("milestone") != progress.completed_sections:
        flash("That story checkpoint has expired. Continue your adventure from the current stage.", "info")
        return redirect(url_for("learning_game.play", game_id=game.id, section=progress.completed_sections))

    question_index = checkpoint.get("question_index", -1)
    try:
        selected_index = int(request.form.get("answer", "-1"))
    except (TypeError, ValueError):
        selected_index = -1
    if not isinstance(question_index, int) or question_index < 0 or question_index >= len(game.questions):
        session.pop("story_checkpoint", None)
        return redirect(url_for("learning_game.play", game_id=game.id, section=progress.completed_sections))
    question = game.questions[question_index]
    if selected_index < 0 or selected_index >= len(question.get("options", [])):
        flash("Choose an answer to continue the story.", "error")
        return redirect(url_for("learning_game.play", game_id=game.id, mode="checkpoint"))

    correct = selected_index == question.get("answer_index")
    session.pop("story_checkpoint", None)
    if correct:
        flash("Mira lights another lantern. You recalled the idea correctly!", "success")
    else:
        answer = question["options"][question["answer_index"]]
        flash(f"Mira shares the clue: {answer}. You can review the lesson as you continue.", "info")
    if progress.completed_sections >= len(game.sections):
        return redirect(url_for("learning_game.play", game_id=game.id, mode="match"))
    return redirect(url_for("learning_game.play", game_id=game.id, section=progress.completed_sections))


@learning_game_bp.route("/games/<int:game_id>/sections/<int:section_index>/complete", methods=["POST"])
@login_required
def complete_section(game_id, section_index):
    game = _owned_game(game_id)
    progress = _progress_for(game)
    if section_index < 0 or section_index >= len(game.sections):
        abort(404)
    if section_index > progress.completed_sections:
        flash("Complete the earlier stages first.", "info")
        return redirect(url_for("learning_game.play", game_id=game.id, section=progress.completed_sections))
    newly_completed = section_index == progress.completed_sections
    if newly_completed:
        progress.completed_sections += 1
        progress.updated_at = datetime.now(timezone.utc)
        db.session.commit()

    if newly_completed and progress.completed_sections % 3 == 0:
        eligible = [index for index, question in enumerate(game.questions)
                    if question.get("section_index", -1) < progress.completed_sections]
        if eligible:
            session["story_checkpoint"] = {
                "game_id": game.id,
                "milestone": progress.completed_sections,
                "question_index": random.choice(eligible),
            }
            return redirect(url_for("learning_game.play", game_id=game.id, mode="checkpoint"))
    if progress.completed_sections >= len(game.sections):
        return redirect(url_for("learning_game.play", game_id=game.id, mode="match"))
    return redirect(url_for("learning_game.play", game_id=game.id, section=progress.completed_sections))


@learning_game_bp.route("/games/<int:game_id>/matches/start", methods=["POST"])
@login_required
def start_match(game_id):
    game = _owned_game(game_id)
    progress = _progress_for(game)
    if progress.completed_sections < len(game.sections):
        flash("Finish the study stages before starting the tug-of-war.", "error")
        return redirect(url_for("learning_game.play", game_id=game.id, section=progress.completed_sections))
    _refresh_question_bank(game)
    if not game.questions:
        flash("This resource has no playable questions yet.", "error")
        return redirect(url_for("skills.skill_realm", skill_id=game.skill_id))

    difficulty = request.form.get("difficulty", "medium").lower()
    if difficulty not in BOT_RULES:
        difficulty = "medium"
    question_order = list(range(len(game.questions)))
    random.SystemRandom().shuffle(question_order)
    now = datetime.now(timezone.utc)
    match = LearningGameMatch(
        user_id=session["user_id"], game_id=game.id, difficulty=difficulty,
        question_order=question_order, rounds=[], current_round=0,
        rope_position=0, player_correct=0, bot_correct=0,
    )
    _schedule_round(match, now)
    db.session.add(match)
    db.session.commit()
    return redirect(url_for("learning_game.match_view", game_id=game.id, match_id=match.id))


@learning_game_bp.route("/games/<int:game_id>/matches/<int:match_id>")
@login_required
def match_view(game_id, match_id):
    game = _owned_game(game_id)
    match = _owned_match(game.id, match_id)
    progress = LearningGameProgress.query.filter_by(user_id=session["user_id"], game_id=game.id).first()
    question = None
    remaining_seconds = 0
    if match.status == "active":
        if match.current_round >= len(match.question_order):
            match.status = "completed"
            match.finished_at = datetime.now(timezone.utc)
            db.session.commit()
        else:
            question = game.questions[match.question_order[match.current_round]]
            remaining_seconds = max(0, (_utc(match.round_deadline_at) - datetime.now(timezone.utc)).total_seconds())
    rounds_played = len(match.rounds or [])
    accuracy = round((match.player_correct / rounds_played) * 100) if rounds_played else 0
    return render_template(
        "game/match.html", game=game, match=match, question=question,
        progress=progress, round_number=min(match.current_round + (1 if match.status == "active" else 0), len(match.question_order)),
        rounds_total=len(match.question_order), remaining_seconds=remaining_seconds,
        rope_edge=ROPE_EDGE, accuracy=accuracy, pass_score=PASS_SCORE,
    )


@learning_game_bp.route("/games/<int:game_id>/matches/<int:match_id>/answer", methods=["POST"])
@login_required
def submit_match_answer(game_id, match_id):
    game = _owned_game(game_id)
    match = _owned_match(game.id, match_id)
    try:
        selected_index = int(request.form.get("answer", "-1"))
    except (TypeError, ValueError):
        selected_index = -1
    if match.status != "active":
        flash("That tug-of-war has finished.", "info")
    elif match.current_round >= len(match.question_order):
        abort(404)
    else:
        question = game.questions[match.question_order[match.current_round]]
        if selected_index < 0 or selected_index >= len(question["options"]):
            flash("Choose an answer to play the round.", "error")
        else:
            message = _resolve_round(game, match, selected_index=selected_index)
            flash(message, "success" if match.status == "completed" and match.rope_position > 0 else "info")
    return redirect(url_for("learning_game.match_view", game_id=game.id, match_id=match.id))


@learning_game_bp.route("/games/<int:game_id>/matches/<int:match_id>/timeout", methods=["POST"])
@login_required
def timeout_match_round(game_id, match_id):
    game = _owned_game(game_id)
    match = _owned_match(game.id, match_id)
    if match.status == "active":
        if datetime.now(timezone.utc) < _utc(match.round_deadline_at):
            flash("The round timer is still running.", "info")
        else:
            message = _resolve_round(game, match, timed_out=True)
            flash(message, "info")
    return redirect(url_for("learning_game.match_view", game_id=game.id, match_id=match.id))


@learning_game_bp.route("/games/<int:game_id>/quiz", methods=["POST"])
@login_required
def legacy_quiz_submit(game_id):
    # Older open quiz pages should land on the current one-question game flow.
    return redirect(url_for("learning_game.play", game_id=game_id, mode="match"))


@learning_game_bp.route("/games/<int:game_id>/delete", methods=["POST"])
@login_required
def delete_game(game_id):
    game = _owned_game(game_id)
    skill_id = game.skill_id
    db.session.delete(game)
    db.session.commit()
    flash("Learning game removed.", "info")
    return redirect(url_for("skills.skill_realm", skill_id=skill_id))
