"""Add user_learning_day_state table with safe ownership tracking.

Revision ID: 0003
Revises: 0002
Create Date: 2026-09-15
"""

import logging
import sqlalchemy as sa
from alembic import context, op
from sqlalchemy.dialects import postgresql

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None

logger = logging.getLogger("alembic.runtime.migration_0003")

TABLE_NAME = "user_learning_day_state"
MARKER_TABLE = "_alembic_0003_user_learning_day_state_created"


def _table_exists(table_name: str) -> bool:
    if context.is_offline_mode():
        return False
    bind = op.get_bind()
    if bind is None:
        return False
    inspector = sa.inspect(bind)
    return inspector.has_table(table_name)


def _get_existing_indexes(table_name: str) -> set[str]:
    if context.is_offline_mode():
        return set()
    bind = op.get_bind()
    if bind is None:
        return set()
    inspector = sa.inspect(bind)
    return {idx["name"] for idx in inspector.get_indexes(table_name)}


def upgrade() -> None:
    if not _table_exists(TABLE_NAME):
        # 1. Create table
        op.create_table(
            TABLE_NAME,
            sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
            sa.Column(
                "user_id",
                postgresql.UUID(as_uuid=True),
                sa.ForeignKey("users.id", ondelete="CASCADE"),
                nullable=False,
            ),
            sa.Column("day_number", sa.Integer(), nullable=False),
            sa.Column("lesson_completed", sa.Boolean(), nullable=False, server_default=sa.false()),
            sa.Column("lesson_completed_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("practice_passed", sa.Boolean(), nullable=False, server_default=sa.false()),
            sa.Column("practice_passed_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("completed", sa.Boolean(), nullable=False, server_default=sa.false()),
            sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column(
                "created_at",
                sa.DateTime(timezone=True),
                server_default=sa.func.now(),
                nullable=False,
            ),
            sa.Column(
                "updated_at",
                sa.DateTime(timezone=True),
                server_default=sa.func.now(),
                nullable=False,
            ),
            sa.UniqueConstraint("user_id", "day_number", name="uq_user_learning_day"),
        )
        op.create_index("ix_user_learning_day_state_user_id", TABLE_NAME, ["user_id"])
        op.create_index("ix_user_learning_day_state_day_number", TABLE_NAME, ["day_number"])
        op.create_index("ix_user_learning_user_day", TABLE_NAME, ["user_id", "day_number"])

        # 2. Record ownership marker table
        op.create_table(
            MARKER_TABLE,
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), primary_key=True),
        )
    else:
        # Table already existed before this migration; only ensure composite and search indexes exist
        existing_indexes = _get_existing_indexes(TABLE_NAME)
        if "ix_user_learning_day_state_user_id" not in existing_indexes:
            op.create_index("ix_user_learning_day_state_user_id", TABLE_NAME, ["user_id"])
        if "ix_user_learning_day_state_day_number" not in existing_indexes:
            op.create_index("ix_user_learning_day_state_day_number", TABLE_NAME, ["day_number"])
        if "ix_user_learning_user_day" not in existing_indexes:
            op.create_index("ix_user_learning_user_day", TABLE_NAME, ["user_id", "day_number"])


def downgrade() -> None:
    if context.is_offline_mode():
        op.drop_table(TABLE_NAME)
        op.drop_table(MARKER_TABLE)
        return

    table_exists = _table_exists(TABLE_NAME)
    was_created_by_migration = _table_exists(MARKER_TABLE)

    if table_exists and was_created_by_migration:
        existing_indexes = _get_existing_indexes(TABLE_NAME)
        if "ix_user_learning_user_day" in existing_indexes:
            op.drop_index("ix_user_learning_user_day", table_name=TABLE_NAME)
        if "ix_user_learning_day_state_day_number" in existing_indexes:
            op.drop_index("ix_user_learning_day_state_day_number", table_name=TABLE_NAME)
        if "ix_user_learning_day_state_user_id" in existing_indexes:
            op.drop_index("ix_user_learning_day_state_user_id", table_name=TABLE_NAME)
        op.drop_table(TABLE_NAME)
        op.drop_table(MARKER_TABLE)
    elif table_exists:
        logger.warning(
            "Table '%s' pre-existed before migration 0003 was applied. "
            "Preserving table and user data during downgrade.",
            TABLE_NAME,
        )
