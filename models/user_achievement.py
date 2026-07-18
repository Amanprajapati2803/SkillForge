from database.database import db
from datetime import datetime, timezone


class UserAchievement(db.Model):

    __tablename__ = "user_achievements"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    achievement_id = db.Column(
        db.Integer,
        db.ForeignKey("achievements.id"),
        nullable=False
    )

    earned_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc)
    )