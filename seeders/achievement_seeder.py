from database.database import db
from models.achievement import Achievement


def seed_achievements():

    achievements = [

        {
            "title": "First Step",
            "key": "first_step",
            "description": "Create your first skill.",
            "icon": "🌱",
            "xp_reward": 50,
        },
        {
            "title": "Learner",
            "key": "first_session",
            "description": "Complete your first learning session.",
            "icon": "📚",
            "xp_reward": 100,
        },
        {
            "title": "XP Hunter",
            "key": "xp_1000",
            "description": "Earn 1000 XP.",
            "icon": "⚡",
            "xp_reward": 200,
        },
        {
            "title": "Level Up",
            "key": "level_5",
            "description": "Reach Level 5.",
            "icon": "⭐",
            "xp_reward": 250,
        },
        {
            "title": "Skill Master",
            "key": "skill_level_10",
            "description": "Reach Level 10 in a skill.",
            "icon": "💎",
            "xp_reward": 500,
        },
        {
            "title": "Consistent",
            "key": "sessions_30",
            "description": "Complete 30 learning sessions.",
            "icon": "🎯",
            "xp_reward": 400,
        },
        {
            "title": "On Fire",
            "key": "streak_7",
            "description": "Maintain a 7-day streak.",
            "icon": "🔥",
            "xp_reward": 300,
        },
    ]

    for achievement in achievements:

        exists = Achievement.query.filter_by(
            title=achievement["title"]
        ).first()

        if exists:
            exists.key = achievement["key"]
        else:
            db.session.add(Achievement(**achievement))

    db.session.commit()

    print("✅ Achievements seeded successfully!")