"""create otp verifications table

Revision ID: b79fb4b2ea32
Revises: bbc54b2ce216
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b79fb4b2ea32"
down_revision: Union[str, Sequence[str], None] = "bbc54b2ce216"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "otp_verifications",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("simu", sa.String(), nullable=False),
        sa.Column("code", sa.String(), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.Column("farmer_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["farmer_id"],
            ["farmers.id"]
        ),
        sa.PrimaryKeyConstraint("id")
    )

    op.create_index(
        op.f("ix_otp_verifications_id"),
        "otp_verifications",
        ["id"],
        unique=False
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_otp_verifications_id"),
        table_name="otp_verifications"
    )

    op.drop_table("otp_verifications")