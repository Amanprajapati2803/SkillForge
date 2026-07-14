from database.database import db

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

    college = db.Column(db.String(100))
    
    xp = db.Column(db.Integer, default=0)

    level = db.Column(db.Integer, default=1)

    streak = db.Column(db.Integer, default=0)

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )
    
skills = db.relationship(
    "Skill",
    backref="user",
    lazy=True,
    cascade="all, delete-orphan"
)    
    