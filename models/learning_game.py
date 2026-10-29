from datetime import datetime, timezone

from database.database import db


class LearningGame(db.Model):
    __tablename__ = "learning_games"

    id = db.Column(db.Integer, primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey("skill.id", ondelete="CASCADE"), nullable=False, index=True)
    source_title = db.Column(db.String(180), nullable=False)
    sections = db.Column(db.JSON, nullable=False)
    questions = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    skill = db.relationship("Skill", backref=db.backref("learning_games", cascade="all, delete-orphan", lazy=True))
    progress_records = db.relationship("LearningGameProgress", back_populates="game", cascade="all, delete-orphan", lazy=True)
    matches = db.relationship("LearningGameMatch", back_populates="game", cascade="all, delete-orphan", lazy=True)


class LearningGameProgress(db.Model):
    __tablename__ = "learning_game_progress"
    __table_args__ = (db.UniqueConstraint("user_id", "game_id", name="uq_learning_game_progress_user_game"),)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    game_id = db.Column(db.Integer, db.ForeignKey("learning_games.id", ondelete="CASCADE"), nullable=False, index=True)
    completed_sections = db.Column(db.Integer, nullable=False, default=0)
    attempts = db.Column(db.Integer, nullable=False, default=0)
    best_score = db.Column(db.Integer, nullable=False, default=0)
    quiz_passed = db.Column(db.Boolean, nullable=False, default=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    user = db.relationship("User", backref=db.backref("learning_game_progress", cascade="all, delete-orphan", lazy=True))
    game = db.relationship("LearningGame", back_populates="progress_records")


class LearningGameMatch(db.Model):
    __tablename__ = "learning_game_matches"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    game_id = db.Column(db.Integer, db.ForeignKey("learning_games.id", ondelete="CASCADE"), nullable=False, index=True)
    status = db.Column(db.String(20), nullable=False, default="active")
    difficulty = db.Column(db.String(20), nullable=False, default="medium")
    question_order = db.Column(db.JSON, nullable=False)
    rounds = db.Column(db.JSON, nullable=False, default=list)
    current_round = db.Column(db.Integer, nullable=False, default=0)
    rope_position = db.Column(db.Integer, nullable=False, default=0)
    player_correct = db.Column(db.Integer, nullable=False, default=0)
    bot_correct = db.Column(db.Integer, nullable=False, default=0)
    bot_has_answer = db.Column(db.Boolean, nullable=False, default=False)
    bot_answer_at = db.Column(db.DateTime, nullable=True)
    round_deadline_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    finished_at = db.Column(db.DateTime, nullable=True)

    user = db.relationship("User", backref=db.backref("learning_game_matches", cascade="all, delete-orphan", lazy=True))
    game = db.relationship("LearningGame", back_populates="matches")
