from database.database import db
from models.user_achievement import UserAchievement
from models.achievement import Achievement
from models.skill import Skill


def unlock_achievement(user_id, achievement_key):
    """
    Unlock an achievement for a user if it hasn't
    already been unlocked.
    """

    achievement = Achievement.query.filter_by(
        key=achievement_key
    ).first()

    if not achievement:
        return False

    already_unlocked = UserAchievement.query.filter_by(
        user_id=user_id,
        achievement_id=achievement.id
    ).first()

    if already_unlocked:
        return False

    unlocked = UserAchievement(
        user_id=user_id,
        achievement_id=achievement.id
    )

    db.session.add(unlocked)
    db.session.commit()

    return True


def check_achievements(user):

    # 🌱 First Step
    if len(user.skills) >= 1:
        unlock_achievement(user.id, "first_step")

    # ⚡ XP Hunter
    if user.xp >= 1000:
        unlock_achievement(user.id, "xp_1000")

    # ⭐ Level Up
    if user.level >= 5:
        unlock_achievement(user.id, "level_5")

    # 🔥 On Fire
    if user.streak >= 7:
        unlock_achievement(user.id, "streak_7")
        
    
    # 📚 Count all learning sessions
    total_sessions = 0

    for skill in user.skills:
        total_sessions += len(skill.sessions)

    # 🎓 First learning session
    if total_sessions >= 1:
        unlock_achievement(user.id, "first_session")

    # 🎯 30 learning sessions
    if total_sessions >= 30:
        unlock_achievement(user.id, "sessions_30")
        
    
    # 💎 Any skill reaches Level 10
    for skill in user.skills:
        if skill.level >= 10:
            unlock_achievement(user.id, "skill_level_10")
            break