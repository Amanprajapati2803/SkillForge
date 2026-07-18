from database.database import db


class Achievement(db.Model):

    __tablename__ = "achievements"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100), nullable=False)

    description = db.Column(db.String(255), nullable=False)

    icon = db.Column(db.String(20), nullable=False)

    xp_reward = db.Column(db.Integer, default=0)