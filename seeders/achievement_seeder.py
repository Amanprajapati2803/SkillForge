# from database.database import db
# from models.achievement import Achievement


# def seed_achievements():

#     achievements = [

#         {
#             "title": "First Step",
#             "description": "Create your first skill.",
#             "icon": "🌱",
#             "xp_reward": 50,
#         },

#         {
#             "title": "Learner",
#             "description": "Complete your first learning session.",
#             "icon": "📚",
#             "xp_reward": 100,
#         },

#         {
#             "title": "XP Hunter",
#             "description": "Earn 1000 XP.",
#             "icon": "⚡",
#             "xp_reward": 200,
#         },

#         {
#             "title": "Level Up",
#             "description": "Reach Level 5.",
#             "icon": "⭐",
#             "xp_reward": 250,
#         },

#         {
#             "title": "Skill Master",
#             "description": "Reach Level 10 in a skill.",
#             "icon": "💎",
#             "xp_reward": 500,
#         },

#         {
#             "title": "Consistent",
#             "description": "Complete 30 learning sessions.",
#             "icon": "🎯",
#             "xp_reward": 400,
#         },

#         {
#             "title": "On Fire",
#             "description": "Maintain a 7-day streak.",
#             "icon": "🔥",
#             "xp_reward": 300,
#         },
#     ]

#     for achievement in achievements:

#         exists = Achievement.query.filter_by(
#             title=achievement["title"]
#         ).first()

#         if not exists:
#             db.session.add(Achievement(**achievement))

#     db.session.commit()

#     print("✅ Achievements seeded successfully!")