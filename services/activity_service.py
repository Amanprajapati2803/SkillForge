from models.activity_log import ActivityLog


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