from database.database import db
from datetime import datetime


class Session(db.Model):
    __tablename__ = "sessions"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(30), nullable=False)

    host = db.Column(db.String(100), nullable=False)

    start_datetime = db.Column(db.DateTime, nullable=False)
    end_datetime = db.Column(db.DateTime, nullable=False)

    meeting_link = db.Column(db.String(255))
    recording_link = db.Column(db.String(255))

    thumbnail = db.Column(db.String(255))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)