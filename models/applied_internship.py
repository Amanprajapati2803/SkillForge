from database.database import db
from datetime import datetime, timezone


class AppliedInternship(db.Model):

    __tablename__ = "applied_internships"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    internship_id = db.Column(
        db.Integer,
        db.ForeignKey("internships.id"),
        nullable=False
    )

    status = db.Column(
        db.String(50),
        default="Applied"
    )

    applied_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc)
    )