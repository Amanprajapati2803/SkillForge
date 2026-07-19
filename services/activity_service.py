from models.activity_log import ActivityLog
from database.database import db


def get_recent_activities(user_id, limit=5):
    """
    Return the most recent activity logs for a user.
    """

    return (
        ActivityLog.query
        .filter_by(user_id=user_id)
        .order_by(ActivityLog.created_at.desc())
        .limit(limit)
        .all()
    )
    
def log_activity(user_id, description,xp_earned):

    activity = ActivityLog(
        user_id=user_id,
        description=description,
        xp_earned=xp_earned
    )

    db.session.add(activity)