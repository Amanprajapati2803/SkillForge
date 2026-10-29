from models.learning_game import LearningGame, LearningGameProgress
from models.skill import Skill


def get_skill_progress(user_id):
    """Return transparent, resource-based study and quiz evidence per skill."""
    skills = Skill.query.filter_by(user_id=user_id).order_by(Skill.name.asc()).all()
    games = LearningGame.query.join(Skill).filter(Skill.user_id == user_id).all()
    game_ids = [game.id for game in games]
    progress_by_game = {
        progress.game_id: progress
        for progress in LearningGameProgress.query.filter(
            LearningGameProgress.user_id == user_id,
            LearningGameProgress.game_id.in_(game_ids or [-1]),
        ).all()
    }
    by_skill = {skill.id: {"studied": 0, "total": 0, "best_accuracy": 0, "attempts": 0, "demonstrated": False, "resources": 0}
                for skill in skills}
    for game in games:
        data = by_skill.get(game.skill_id)
        if data is None:
            continue
        progress = progress_by_game.get(game.id)
        section_count = len(game.sections or [])
        data["total"] += section_count
        data["studied"] += min(progress.completed_sections, section_count) if progress else 0
        data["resources"] += 1
        if progress:
            data["best_accuracy"] = max(data["best_accuracy"], progress.best_score or 0)
            data["attempts"] += progress.attempts or 0
            data["demonstrated"] = data["demonstrated"] or bool(progress.quiz_passed)
    result = {}
    for skill in skills:
        data = by_skill[skill.id]
        data["percent"] = round(data["studied"] * 100 / data["total"]) if data["total"] else 0
        data["skill"] = skill
        result[skill.id] = data
    return result
