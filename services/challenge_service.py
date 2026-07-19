import random
from models.daily_challenge import DailyChallenge
from database.database import db
from datetime import datetime , timezone
from models.user import User
from models.daily_challenge import DailyChallenge
from services.activity_service import log_activity
from utils.progression import calculate_level

CHALLENGE_POOL = [
    {
        "title": "Practice Sessions",
        "description": "Complete 2 practice sessions.",
        "target": 2,
        "xp_reward": 100,
    },
    {
        "title": "Resource Collector",
        "description": "Add 1 learning resource.",
        "target": 1,
        "xp_reward": 50,
    },
    {
        "title": "Skill Builder",
        "description": "Create 1 new skill.",
        "target": 1,
        "xp_reward": 75,
    },
]


def generate_daily_challenges():
    return random.sample(CHALLENGE_POOL, 3)

def create_daily_challenges(user_id):
    challenges = generate_daily_challenges()

    for challenge in challenges:

        db.session.add(
            DailyChallenge(
                user_id=user_id,
                title=challenge["title"],
                description=challenge["description"],
                target=challenge["target"],
                xp_reward=challenge["xp_reward"],
            )
        )

    db.session.commit()
    
def ensure_daily_challenges(user_id):

    today = datetime.now(timezone.utc).date()

    existing = DailyChallenge.query.filter(
        DailyChallenge.user_id == user_id
    ).all()

    today_challenges = [
        c for c in existing
        if c.created_at.date() == today
    ]

    if len(today_challenges) == 0:
        create_daily_challenges(user_id)
   
    
    # update daily challenges     
def update_challenge_progress(user_id, title, amount=1):

    today = datetime.now(timezone.utc).date()

    challenges = DailyChallenge.query.filter_by(
        user_id=user_id
    ).all()

    for challenge in challenges:

        if challenge.created_at.date() != today:
            continue

        if challenge.title != title:
            continue

        if challenge.completed:
            continue

        challenge.progress += amount

        if challenge.progress >= challenge.target:
            challenge.progress = challenge.target
            challenge.completed = True

        db.session.commit()

        break
    



def claim_challenge_reward(challenge_id, user_id):

    challenge = DailyChallenge.query.filter_by(
        id=challenge_id,
        user_id=user_id
    ).first()

    if not challenge:
        return False, "Challenge not found."

    if not challenge.completed:
        return False, "Challenge is not completed yet."

    if challenge.claimed:
        return False, "Reward already claimed."

    user = User.query.get(user_id)

    # Award XP
    user.xp += challenge.xp_reward

    # Update level
    user.level = calculate_level(user.xp)

    # Mark reward as claimed
    challenge.claimed = True

    # Log activity
    log_activity(
        user.id,
        f"Claimed Daily Challenge: {challenge.title}",
        challenge.xp_reward
    )

    db.session.commit()

    return True, "Reward claimed successfully!"