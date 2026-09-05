"""Create reminders table

Revision ID: bbc54b2ce216
Revises: 32296570c158
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "bbc54b2ce216"
down_revision: Union[str, Sequence[str], None] = "32296570c158"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "reminders",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("ujumbe", sa.String(), nullable=False),
        sa.Column("tarehe", sa.Date(), nullable=False),
        sa.Column(
            "hali",
            sa.String(),
            nullable=False,
            server_default="haijakamilika"
        ),
        sa.Column("crop_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["crop_id"],
            ["crops.id"]
        ),
        sa.PrimaryKeyConstraint("id")
    )

    op.create_index(
        op.f("ix_reminders_id"),
        "reminders",
        ["id"],
        unique=False
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_reminders_id"),
        table_name="reminders"
    )

    op.drop_table("reminders")