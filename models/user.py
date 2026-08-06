from database.database import db


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

    college = db.Column(db.String(100))

    xp = db.Column(db.Integer, default=0)

    bio = db.Column(db.Text)

    level = db.Column(db.Integer, default=1)

    streak = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, server_default=db.func.now())

    skills = db.relationship(
        "Skill", backref="user", lazy=True, cascade="all, delete-orphan"
    )

    activity_logs = db.relationship(
        "ActivityLog", backref="user", lazy=True, cascade="all, delete-orphan"
    )

    applications = db.relationship(
        "AppliedInternship", backref="user", lazy=True, cascade="all, delete-orphan"
    )

    two_factor_enabled = db.Column(db.Boolean, default=False, nullable=False)

    notify_feed = db.Column(db.Boolean, default=True, nullable=False)

    notify_sessions = db.Column(db.Boolean, default=True, nullable=False)

    notify_digest = db.Column(db.Boolean, default=True, nullable=False)

    notify_badges = db.Column(db.Boolean, default=False, nullable=False)

    google_linked = db.Column(db.Boolean, default=False, nullable=False)

    github_linked = db.Column(db.Boolean, default=False, nullable=False)

    linkedin_linked = db.Column(db.Boolean, default=False, nullable=False)

    avatar = db.Column(db.String(255), default="default-avatar.png")

    community_posts = db.relationship(
        "CommunityPost",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan",
    )

    community_comments = db.relationship(
        "CommunityComment",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan",
    )

    community_likes = db.relationship(
        "CommunityLike",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan",
    )

    community_bookmarks = db.relationship(
        "CommunityBookmark",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan",
    )
