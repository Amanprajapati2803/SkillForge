"""create resource learning games and learner progress"""
from alembic import op
import sqlalchemy as sa

revision = "d8c67f4d9a10"
down_revision = "f2e1b18db4b0"
branch_labels = None
depends_on = None


def _table_exists(name):
    return sa.inspect(op.get_bind()).has_table(name)


def _ensure_index(table, name, columns):
    indexes = {item["name"] for item in sa.inspect(op.get_bind()).get_indexes(table)}
    if name not in indexes:
        op.create_index(name, table, columns)


def upgrade():
    # app.py calls db.create_all() during startup. Avoid failing if that already
    # created either table before Flask-Migrate runs this revision.
    if not _table_exists("learning_games"):
        op.create_table(
            "learning_games",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("skill_id", sa.Integer(), nullable=False),
            sa.Column("source_title", sa.String(length=180), nullable=False),
            sa.Column("sections", sa.JSON(), nullable=False),
            sa.Column("questions", sa.JSON(), nullable=False),
            sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
            sa.ForeignKeyConstraint(["skill_id"], ["skill.id"], ondelete="CASCADE"),
            sa.PrimaryKeyConstraint("id"),
        )
    _ensure_index("learning_games", "ix_learning_games_skill_id", ["skill_id"])

    if not _table_exists("learning_game_progress"):
        op.create_table(
            "learning_game_progress",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("user_id", sa.Integer(), nullable=False),
            sa.Column("game_id", sa.Integer(), nullable=False),
            sa.Column("completed_sections", sa.Integer(), nullable=False, server_default="0"),
            sa.Column("attempts", sa.Integer(), nullable=False, server_default="0"),
            sa.Column("best_score", sa.Integer(), nullable=False, server_default="0"),
            sa.Column("quiz_passed", sa.Boolean(), nullable=False, server_default=sa.false()),
            sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
            sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
            sa.ForeignKeyConstraint(["game_id"], ["learning_games.id"], ondelete="CASCADE"),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("user_id", "game_id", name="uq_learning_game_progress_user_game"),
        )
    _ensure_index("learning_game_progress", "ix_learning_game_progress_user_id", ["user_id"])
    _ensure_index("learning_game_progress", "ix_learning_game_progress_game_id", ["game_id"])

    if not _table_exists("learning_game_matches"):
        op.create_table(
            "learning_game_matches",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("user_id", sa.Integer(), nullable=False),
            sa.Column("game_id", sa.Integer(), nullable=False),
            sa.Column("status", sa.String(length=20), nullable=False),
            sa.Column("difficulty", sa.String(length=20), nullable=False),
            sa.Column("question_order", sa.JSON(), nullable=False),
            sa.Column("rounds", sa.JSON(), nullable=False),
            sa.Column("current_round", sa.Integer(), nullable=False),
            sa.Column("rope_position", sa.Integer(), nullable=False),
            sa.Column("player_correct", sa.Integer(), nullable=False),
            sa.Column("bot_correct", sa.Integer(), nullable=False),
            sa.Column("bot_has_answer", sa.Boolean(), nullable=False),
            sa.Column("bot_answer_at", sa.DateTime(), nullable=True),
            sa.Column("round_deadline_at", sa.DateTime(), nullable=False),
            sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
            sa.Column("finished_at", sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
            sa.ForeignKeyConstraint(["game_id"], ["learning_games.id"], ondelete="CASCADE"),
            sa.PrimaryKeyConstraint("id"),
        )
    _ensure_index("learning_game_matches", "ix_learning_game_matches_user_id", ["user_id"])
    _ensure_index("learning_game_matches", "ix_learning_game_matches_game_id", ["game_id"])


def downgrade():
    if _table_exists("learning_game_matches"):
        indexes = {item["name"] for item in sa.inspect(op.get_bind()).get_indexes("learning_game_matches")}
        for name in ("ix_learning_game_matches_game_id", "ix_learning_game_matches_user_id"):
            if name in indexes:
                op.drop_index(name, table_name="learning_game_matches")
        op.drop_table("learning_game_matches")
    if _table_exists("learning_game_progress"):
        indexes = {item["name"] for item in sa.inspect(op.get_bind()).get_indexes("learning_game_progress")}
        for name in ("ix_learning_game_progress_game_id", "ix_learning_game_progress_user_id"):
            if name in indexes:
                op.drop_index(name, table_name="learning_game_progress")
        op.drop_table("learning_game_progress")
    if _table_exists("learning_games"):
        indexes = {item["name"] for item in sa.inspect(op.get_bind()).get_indexes("learning_games")}
        if "ix_learning_games_skill_id" in indexes:
            op.drop_index("ix_learning_games_skill_id", table_name="learning_games")
        op.drop_table("learning_games")
