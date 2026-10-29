"""connect shared community resources to skill libraries"""
from alembic import op
import sqlalchemy as sa

revision = "a1b2c3d4e5f6"
down_revision = "d8c67f4d9a10"
branch_labels = None
depends_on = None


def _columns(table):
    return {item["name"] for item in sa.inspect(op.get_bind()).get_columns(table)}


def upgrade():
    if "skill_name" not in _columns("community_posts"):
        op.add_column("community_posts", sa.Column("skill_name", sa.String(length=100), nullable=True))
        op.create_index("ix_community_posts_skill_name", "community_posts", ["skill_name"])
    if "attachment_name" not in _columns("community_posts"):
        op.add_column("community_posts", sa.Column("attachment_name", sa.String(length=255), nullable=True))
    if "external_url" not in _columns("community_posts"):
        op.add_column("community_posts", sa.Column("external_url", sa.String(length=1000), nullable=True))
    if "source_post_id" not in _columns("resources"):
        with op.batch_alter_table("resources") as batch_op:
            batch_op.add_column(sa.Column("source_post_id", sa.Integer(), nullable=True))
            batch_op.create_foreign_key("fk_resources_source_post_id_community_posts", "community_posts", ["source_post_id"], ["id"], ondelete="SET NULL")
        op.create_index("ix_resources_source_post_id", "resources", ["source_post_id"])
    if "storage_key" not in _columns("resources"):
        op.add_column("resources", sa.Column("storage_key", sa.String(length=255), nullable=True))
    if "original_filename" not in _columns("resources"):
        op.add_column("resources", sa.Column("original_filename", sa.String(length=255), nullable=True))
    constraints = {item.get("name") for item in sa.inspect(op.get_bind()).get_unique_constraints("resources")}
    if "uq_resource_skill_source_post" not in constraints:
        with op.batch_alter_table("resources") as batch_op:
            batch_op.create_unique_constraint("uq_resource_skill_source_post", ["skill_id", "source_post_id"])


def downgrade():
    with op.batch_alter_table("resources") as batch_op:
        batch_op.drop_constraint("uq_resource_skill_source_post", type_="unique")
    indexes = {item["name"] for item in sa.inspect(op.get_bind()).get_indexes("resources")}
    if "ix_resources_source_post_id" in indexes:
        op.drop_index("ix_resources_source_post_id", table_name="resources")
    fks = {item.get("name") for item in sa.inspect(op.get_bind()).get_foreign_keys("resources")}
    if "fk_resources_source_post_id_community_posts" in fks:
        with op.batch_alter_table("resources") as batch_op:
            batch_op.drop_constraint("fk_resources_source_post_id_community_posts", type_="foreignkey")
    for column in ("original_filename", "storage_key", "source_post_id"):
        if column in _columns("resources"):
            op.drop_column("resources", column)
    if "external_url" in _columns("community_posts"):
        op.drop_column("community_posts", "external_url")
    if "attachment_name" in _columns("community_posts"):
        op.drop_column("community_posts", "attachment_name")
    if "skill_name" in _columns("community_posts"):
        indexes = {item["name"] for item in sa.inspect(op.get_bind()).get_indexes("community_posts")}
        if "ix_community_posts_skill_name" in indexes:
            op.drop_index("ix_community_posts_skill_name", table_name="community_posts")
        op.drop_column("community_posts", "skill_name")
