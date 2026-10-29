from database.database import db


class CommunityPost(db.Model):

    __tablename__ = "community_posts"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    title = db.Column(db.String(200), nullable=False)

    content = db.Column(db.Text, nullable=False)

    category = db.Column(db.String(50), nullable=False)

    skill_name = db.Column(db.String(100), nullable=True, index=True)

    image_url = db.Column(db.String(255))

    attachment_url = db.Column(db.String(255))  # private stored filename

    attachment_name = db.Column(db.String(255))  # original filename shown to learners

    external_url = db.Column(db.String(1000))

    is_pinned = db.Column(db.Boolean, default=False)

    views = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, server_default=db.func.now())

    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), onupdate=db.func.now()
    )

    comments = db.relationship(
        "CommunityComment", backref="post", lazy=True, cascade="all, delete-orphan"
    )

    likes = db.relationship(
        "CommunityLike", backref="post", lazy=True, cascade="all, delete-orphan"
    )

    bookmarks = db.relationship(
        "CommunityBookmark", backref="post", lazy=True, cascade="all, delete-orphan"
    )
