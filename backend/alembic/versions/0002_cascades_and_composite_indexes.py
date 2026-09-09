"""Cascades, auth columns, and composite indexes (Phase 3).

Revision ID: 0002
Revises: 0001
Create Date: 2026-09-08
"""

import sqlalchemy as sa
from alembic import op

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Add auth credentials and username columns to users
    op.add_column("users", sa.Column("username", sa.String(80), nullable=True))
    op.add_column("users", sa.Column("pwd_hash", sa.String(128), nullable=True))
    op.add_column("users", sa.Column("salt", sa.String(64), nullable=True))
    op.create_index("ix_users_username", "users", ["username"], unique=True)

    # 2. Add composite index on submissions(user_id, created_at DESC)
    op.create_index(
        "ix_submissions_user_created_desc",
        "submissions",
        ["user_id", sa.text("created_at DESC")],
    )

    # 3. Add composite index on user_topic_state(user_id, topic_id)
    op.create_index(
        "ix_user_topic_state_user_topic",
        "user_topic_state",
        ["user_id", "topic_id"],
    )

    # 4. Enforce CASCADE on memory_notes foreign keys
    op.drop_constraint("memory_notes_submission_id_fkey", "memory_notes", type_="foreignkey")
    op.drop_constraint("memory_notes_topic_id_fkey", "memory_notes", type_="foreignkey")
    op.create_foreign_key(
        "memory_notes_submission_id_fkey",
        "memory_notes",
        "submissions",
        ["submission_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "memory_notes_topic_id_fkey",
        "memory_notes",
        "topics",
        ["topic_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint("memory_notes_topic_id_fkey", "memory_notes", type_="foreignkey")
    op.drop_constraint("memory_notes_submission_id_fkey", "memory_notes", type_="foreignkey")
    op.create_foreign_key(
        "memory_notes_topic_id_fkey",
        "memory_notes",
        "topics",
        ["topic_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_foreign_key(
        "memory_notes_submission_id_fkey",
        "memory_notes",
        "submissions",
        ["submission_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.drop_index("ix_user_topic_state_user_topic", table_name="user_topic_state")
    op.drop_index("ix_submissions_user_created_desc", table_name="submissions")
    op.drop_index("ix_users_username", table_name="users")
    op.drop_column("users", "salt")
    op.drop_column("users", "pwd_hash")
    op.drop_column("users", "username")
