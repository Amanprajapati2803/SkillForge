from database.database import db
from datetime import datetime, timezone


class Resource(db.Model):
    __tablename__ = "resources"
    __table_args__ = (db.UniqueConstraint("skill_id", "source_post_id", name="uq_resource_skill_source_post"),)

    id = db.Column(db.Integer, primary_key=True)

    skill_id = db.Column(db.Integer, db.ForeignKey("skill.id"), nullable=False)

    title = db.Column(db.String(150), nullable=False)

    resource_type = db.Column(db.String(30), nullable=False)

    url = db.Column(db.String(500), nullable=False)

    description = db.Column(db.Text)

    skill = db.relationship("Skill", backref="resources")
    
    difficulty = db.Column(db.String(50), nullable=True)

    # A saved community attachment appears in the learner's own skill library.
    source_post_id = db.Column(db.Integer, db.ForeignKey(
        "community_posts.id", name="fk_resources_source_post_id_community_posts", ondelete="SET NULL"
    ), nullable=True, index=True)
    storage_key = db.Column(db.String(255), nullable=True)
    original_filename = db.Column(db.String(255), nullable=True)
