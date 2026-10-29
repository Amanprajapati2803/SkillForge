from flask import Blueprint, render_template, session, redirect, url_for, flash
from utils.auth import login_required
from models.achievement import Achievement
from models.user_achievement import UserAchievement
from models.user import User
from models.skill import Skill
from models.learning_session import LearningSession
from database.database import db
from datetime import datetime, timezone
from sqlalchemy import func

achievement_bp = Blueprint("achievement", __name__)


def get_certificate_progress(user):
    """Calculate progress for all possible certificates."""

    # Get user stats
    skills = Skill.query.filter_by(user_id=user.id).all()
    skill_count = len(skills)
    total_xp = user.xp or 0
    streak = user.streak or 0

    # Total hours
    total_minutes = db.session.query(func.sum(LearningSession.duration)).join(Skill).filter(Skill.user_id == user.id).scalar() or 0
    total_hours = total_minutes / 60

    # Total sessions
    total_sessions = LearningSession.query.join(Skill).filter(Skill.user_id == user.id).count()

    # Check which achievements already unlocked
    unlocked = UserAchievement.query.filter_by(user_id=user.id).all()
    unlocked_keys = {ua.achievement.key for ua in unlocked if ua.achievement}

    # Define all certificates
    certificates = []

    # 1. FIRST STEP - Create first skill
    cert = {
        "key": "first_skill",
        "title": "First Step",
        "subtitle": "The Journey Begins",
        "description": "Created your first technique and began the path of cultivation.",
        "level": "MASTERY LEVEL I",
        "date": None,
        "icon": "⚔️",
        "rarity": "Common",
        "progress": min(100, skill_count * 100),
        "progress_text": f"{skill_count}/1 Skills",
        "unlocked": skill_count >= 1,
        "color": "gold"
    }
    if "first_skill" in unlocked_keys:
        cert["unlocked"] = True
    certificates.append(cert)

    # 2. FIRST SESSION - Complete first practice
    cert = {
        "key": "first_session",
        "title": "Initiate Practitioner",
        "subtitle": "First Cultivation",
        "description": "Completed your first learning session and earned your initial XP.",
        "level": "MASTERY LEVEL I",
        "date": None,
        "icon": "📖",
        "rarity": "Common",
        "progress": min(100, total_sessions * 100),
        "progress_text": f"{total_sessions}/1 Sessions",
        "unlocked": total_sessions >= 1,
        "color": "green"
    }
    if "first_session" in unlocked_keys:
        cert["unlocked"] = True
    certificates.append(cert)

    # 3. SKILL MASTERY - Level 10 in any skill
    max_skill_level = max([s.level or 1 for s in skills], default=1)
    max_skill_xp = max([s.xp or 0 for s in skills], default=0)
    cert = {
        "key": "skill_mastery",
        "title": "Technique Grandmaster",
        "subtitle": "Mastery Achieved",
        "description": "Reached Level 10 in a single technique, proving deep dedication.",
        "level": "MASTERY LEVEL X",
        "date": None,
        "icon": "🏆",
        "rarity": "Rare",
        "progress": min(100, (max_skill_xp / 1000) * 100),
        "progress_text": f"{max_skill_xp}/1000 XP (Lv. {max_skill_level})",
        "unlocked": max_skill_level >= 10,
        "color": "purple"
    }
    if "skill_mastery" in unlocked_keys:
        cert["unlocked"] = True
    certificates.append(cert)

    # 4. INNER GATE - Reach 1500 total XP
    cert = {
        "key": "inner_gate",
        "title": "Inner Gate Disciple",
        "subtitle": "Rank Ascension",
        "description": "Transcended the outer gates and entered the inner sanctum of the sect.",
        "level": "RANK UP",
        "date": None,
        "icon": "🚪",
        "rarity": "Uncommon",
        "progress": min(100, (total_xp / 1500) * 100),
        "progress_text": f"{total_xp}/1500 XP",
        "unlocked": total_xp >= 1500,
        "color": "blue"
    }
    if "inner_gate" in unlocked_keys:
        cert["unlocked"] = True
    certificates.append(cert)

    # 5. CORE DISCIPLE - Reach 5000 total XP
    cert = {
        "key": "core_disciple",
        "title": "Core Disciple",
        "subtitle": "Rank Ascension",
        "description": "Recognized as a core member of the sect with profound cultivation.",
        "level": "RANK UP",
        "date": None,
        "icon": "💎",
        "rarity": "Rare",
        "progress": min(100, (total_xp / 5000) * 100),
        "progress_text": f"{total_xp}/5000 XP",
        "unlocked": total_xp >= 5000,
        "color": "cyan"
    }
    if "core_disciple" in unlocked_keys:
        cert["unlocked"] = True
    certificates.append(cert)

    # 6. STREAK KEEPER - 7 day streak
    cert = {
        "key": "streak_keeper",
        "title": "Flame Keeper",
        "subtitle": "Unbroken Dedication",
        "description": "Maintained a 7-day cultivation streak without breaking the chain.",
        "level": "DEDICATION",
        "date": None,
        "icon": "🔥",
        "rarity": "Uncommon",
        "progress": min(100, (streak / 7) * 100),
        "progress_text": f"{streak}/7 Days",
        "unlocked": streak >= 7,
        "color": "orange"
    }
    if "streak_keeper" in unlocked_keys:
        cert["unlocked"] = True
    certificates.append(cert)

    # 7. MASTER OF MANY - 5+ skills
    cert = {
        "key": "master_of_many",
        "title": "Polymath Cultivator",
        "subtitle": "Breadth of Knowledge",
        "description": "Mastered 5 different techniques across multiple disciplines.",
        "level": "VERSATILITY",
        "date": None,
        "icon": "📚",
        "rarity": "Rare",
        "progress": min(100, (skill_count / 5) * 100),
        "progress_text": f"{skill_count}/5 Skills",
        "unlocked": skill_count >= 5,
        "color": "teal"
    }
    if "master_of_many" in unlocked_keys:
        cert["unlocked"] = True
    certificates.append(cert)

    # 8. CENTURION - 100 hours
    cert = {
        "key": "centurion",
        "title": "Centurion of Code",
        "subtitle": "100 Hours Logged",
        "description": "Dedicated over 100 hours to active cultivation and practice.",
        "level": "ENDURANCE",
        "date": None,
        "icon": "⏱️",
        "rarity": "Epic",
        "progress": min(100, (total_hours / 100) * 100),
        "progress_text": f"{total_hours:.1f}/100 Hours",
        "unlocked": total_hours >= 100,
        "color": "red"
    }
    if "centurion" in unlocked_keys:
        cert["unlocked"] = True
    certificates.append(cert)

    # 9. DEDICATED DISCIPLE - 50 sessions
    cert = {
        "key": "dedicated_disciple",
        "title": "Dedicated Disciple",
        "subtitle": "50 Sessions Complete",
        "description": "Completed 50 learning sessions, proving unwavering commitment.",
        "level": "COMMITMENT",
        "date": None,
        "icon": "🎯",
        "rarity": "Rare",
        "progress": min(100, (total_sessions / 50) * 100),
        "progress_text": f"{total_sessions}/50 Sessions",
        "unlocked": total_sessions >= 50,
        "color": "indigo"
    }
    if "dedicated_disciple" in unlocked_keys:
        cert["unlocked"] = True
    certificates.append(cert)

    # 10. ELDER - Reach 12000 total XP
    cert = {
        "key": "elder",
        "title": "Elder of the Sect",
        "subtitle": "Rank Ascension",
        "description": "Attained the revered rank of Elder through decades of cultivation.",
        "level": "RANK UP",
        "date": None,
        "icon": "👑",
        "rarity": "Epic",
        "progress": min(100, (total_xp / 12000) * 100),
        "progress_text": f"{total_xp}/12000 XP",
        "unlocked": total_xp >= 12000,
        "color": "yellow"
    }
    if "elder" in unlocked_keys:
        cert["unlocked"] = True
    certificates.append(cert)

    # Auto-unlock any newly earned achievements
    for cert in certificates:
        if cert["unlocked"] and cert["key"] not in unlocked_keys:
            # Check if achievement exists in DB
            ach = Achievement.query.filter_by(key=cert["key"]).first()
            if not ach:
                ach = Achievement(
                    title=cert["title"],
                    description=cert["description"],
                    icon=cert["icon"],
                    xp_reward=50,
                    category="Certificate",
                    rarity=cert["rarity"],
                    key=cert["key"]
                )
                db.session.add(ach)
                db.session.commit()

            # Create user achievement
            ua = UserAchievement(user_id=user.id, achievement_id=ach.id)
            db.session.add(ua)
            db.session.commit()
            unlocked_keys.add(cert["key"])

    # Split into unlocked and locked
    unlocked_certs = [c for c in certificates if c["unlocked"]]
    locked_certs = [c for c in certificates if not c["unlocked"]]

    # Sort locked by progress (closest first)
    locked_certs.sort(key=lambda x: x["progress"], reverse=True)

    return unlocked_certs, locked_certs, total_hours, total_sessions


@achievement_bp.route("/achievements")
@login_required
def achievements():
    return redirect(url_for("dashboard.home"))