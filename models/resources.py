from database.database import db
from datetime import datetime, timezone


class Resource(db.Model):
    __tablename__ = "resources"

    id = db.Column(db.Integer, primary_key=True)

    skill_id = db.Column(db.Integer, db.ForeignKey("skill.id"), nullable=False)

    title = db.Column(db.String(150), nullable=False)

    resource_type = db.Column(db.String(30), nullable=False)

    url = db.Column(db.String(500), nullable=False)

    description = db.Column(db.Text)

    skill = db.relationship("Skill", backref="resources")
    
    difficulty = db.Column(db.String(50), nullable=True)  
