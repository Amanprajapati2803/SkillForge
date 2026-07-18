from database.database import db
from models.achievement import Achievement
from models.user_achievement import UserAchievement
from models.user import User
from utils.progression import award_user_xp


def unlock_achievement(user_id, title):

    achievement = Achievement.query.filter_by(title=title).first()

    if not achievement:
        return

    already_unlocked = UserAchievement.query.filter_by(
        user_id=user_id, achievement_id=achievement.id
    ).first()

    if already_unlocked:
        return

    unlocked = UserAchievement(user_id=user_id, achievement_id=achievement.id)

    db.session.add(unlocked)
    
    user = User.query.get(user_id)

    if user:
        activity = award_user_xp(
            user,
            achievement.xp_reward,
            f"🏆 Achievement Unlocked: {achievement.title}"
        )

    db.session.add(activity)
    db.session.commit()
