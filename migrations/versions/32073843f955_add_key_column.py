from alembic import op
import sqlalchemy as sa

revision = "32073843f955"
down_revision = "a987a9b76a9c"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("achievements") as batch_op:
        batch_op.add_column(
            sa.Column("key", sa.String(50), nullable=True)
        )


def downgrade():
    with op.batch_alter_table("achievements") as batch_op:
        batch_op.drop_column("key")