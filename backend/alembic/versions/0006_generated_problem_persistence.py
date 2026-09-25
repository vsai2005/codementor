"""Durable AI-Generated Problem Persistence & Reference Solution Storage.

Revision ID: 0006
Revises: 0005
Create Date: 2026-09-25
"""

import sqlalchemy as sa
from alembic import op

revision = "0006"
down_revision = "0005"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "problems",
        sa.Column("is_generated", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.add_column(
        "problems",
        sa.Column("generation_source", sa.String(40), nullable=False, server_default="curated"),
    )
    op.add_column(
        "problems",
        sa.Column("reference_solution", sa.Text(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("problems", "reference_solution")
    op.drop_column("problems", "generation_source")
    op.drop_column("problems", "is_generated")
