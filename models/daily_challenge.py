from database.database import db
from datetime import datetime, timezone


class DailyChallenge(db.Model):

    __tablename__ = "daily_challenges"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    title = db.Column(db.String(150), nullable=False)

    description = db.Column(db.String(255))

    target = db.Column(db.Integer, nullable=False)

    progress = db.Column(db.Integer, default=0)

    xp_reward = db.Column(db.Integer, default=50)

    completed = db.Column(db.Boolean, default=False)

    claimed = db.Column(db.Boolean, default=False)

    
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    user = db.relationship("User", backref="daily_challenges")