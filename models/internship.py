from database.database import db
from datetime import datetime, timezone


class Internship(db.Model):

    __tablename__ = "internships"

    id = db.Column(db.Integer, primary_key=True)

    company = db.Column(db.String(100), nullable=False)

    title = db.Column(db.String(150), nullable=False)

    description = db.Column(db.Text, nullable=False)

    location = db.Column(db.String(100), nullable=False)

    internship_type = db.Column(db.String(50), nullable=False)

    apply_link = db.Column(db.String(300), nullable=False)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    
    
    applications = db.relationship(
        "AppliedInternship",
        backref="internship",
        lazy=True,
        cascade="all, delete-orphan"
    )

    internship_skills = db.relationship(
        "InternshipSkill",
        backref="internship",
        lazy=True,
        cascade="all, delete-orphan"
    )