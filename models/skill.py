from database.database import db
from datetime import datetime , timezone

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    name = db.Column(db.String(100), nullable=False)

    xp = db.Column(db.Integer, default=0)

    level = db.Column(db.Integer, default=1)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    sessions = db.relationship(
    "LearningSession",
    back_populates="skill",
    cascade="all, delete-orphan",
    lazy=True
)