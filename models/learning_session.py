from database.database import db
from datetime import datetime,timezone


class LearningSession(db.Model):
    __tablename__ = "learning_sessions"

    id = db.Column(db.Integer, primary_key=True)

    skill_id = db.Column(
        db.Integer,
        db.ForeignKey("skill.id"),
        nullable=False
    )

    title = db.Column(db.String(150), nullable=False)

    duration = db.Column(db.Integer, nullable=False)  # Minutes

    notes = db.Column(db.Text)

    xp_earned = db.Column(db.Integer, default=0)

    created_at = db.Column(
        db.DateTime,
        default=datetime.now(timezone.utc)
    )

    skill = db.relationship(
        "Skill",
        back_populates="sessions"
    )