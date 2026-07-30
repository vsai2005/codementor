"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-07-28
"""

import sqlalchemy as sa
from alembic import op
from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects import postgresql

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None

EMBED_DIM = 1536


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String(320), nullable=False, unique=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("avatar_url", sa.Text()),
        sa.Column("google_sub", sa.String(255), unique=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_users_email", "users", ["email"])
    op.create_index("ix_users_google_sub", "users", ["google_sub"])

    op.create_table(
        "topics",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("slug", sa.String(80), nullable=False, unique=True),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("parent_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("topics.id", ondelete="SET NULL")),
    )
    op.create_index("ix_topics_slug", "topics", ["slug"])

    op.create_table(
        "problems",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("slug", sa.String(120), nullable=False, unique=True),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("statement_md", sa.Text(), nullable=False),
        sa.Column("constraints_md", sa.Text(), nullable=False, server_default=""),
        sa.Column("difficulty_tier", sa.Integer(), nullable=False),
        sa.Column("topic_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("topics.id", ondelete="CASCADE"), nullable=False),
        sa.Column("optimal_time", sa.String(40), nullable=False, server_default="O(n)"),
        sa.Column("optimal_space", sa.String(40), nullable=False, server_default="O(1)"),
        sa.Column("entry_point", sa.String(80), nullable=False, server_default="solve"),
        sa.Column("test_cases", postgresql.JSONB(), nullable=False),
        sa.Column("starter_code", postgresql.JSONB(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.CheckConstraint("difficulty_tier BETWEEN 1 AND 5", name="ck_problems_tier_range"),
    )
    op.create_index("ix_problems_slug", "problems", ["slug"])
    op.create_index("ix_problems_topic_tier", "problems", ["topic_id", "difficulty_tier"])

    op.create_table(
        "submissions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("problem_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("problems.id", ondelete="CASCADE"), nullable=False),
        sa.Column("language", sa.String(20), nullable=False, server_default="python"),
        sa.Column("code", sa.Text(), nullable=False),
        sa.Column("tests_passed", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("tests_total", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("overall_score", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("scores", postgresql.JSONB(), nullable=False),
        sa.Column("review", postgresql.JSONB(), nullable=False),
        sa.Column("review_degraded", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_submissions_user_created", "submissions", ["user_id", "created_at"])
    op.create_index("ix_submissions_user_problem", "submissions", ["user_id", "problem_id"])

    mastery = postgresql.ENUM("weak", "learning", "strong", name="mastery_enum")
    mastery.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "user_topic_state",
        sa.Column("user_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("topic_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("topics.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("current_tier", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("attempts", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("avg_score", sa.Float(), nullable=False, server_default="0"),
        sa.Column("mastery", mastery, nullable=False, server_default="weak"),
        sa.Column("last_practiced_at", sa.DateTime(timezone=True)),
        sa.CheckConstraint("current_tier BETWEEN 1 AND 5", name="ck_uts_tier_range"),
    )

    op.create_table(
        "difficulty_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("topic_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("topics.id", ondelete="CASCADE"), nullable=False),
        sa.Column("submission_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("submissions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("rolling_score", sa.Float(), nullable=False),
        sa.Column("tier_from", sa.Integer(), nullable=False),
        sa.Column("tier_to", sa.Integer(), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_difficulty_events_user_topic", "difficulty_events",
                    ["user_id", "topic_id", "created_at"])

    op.create_table(
        "memory_notes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("submission_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("submissions.id", ondelete="SET NULL")),
        sa.Column("topic_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("topics.id", ondelete="SET NULL")),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("embedding", Vector(EMBED_DIM), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_memory_notes_user_created", "memory_notes", ["user_id", "created_at"])
    op.execute(
        "CREATE INDEX ix_memory_notes_embedding ON memory_notes "
        "USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100)"
    )


def downgrade() -> None:
    op.drop_table("memory_notes")
    op.drop_table("difficulty_events")
    op.drop_table("user_topic_state")
    op.execute("DROP TYPE IF EXISTS mastery_enum")
    op.drop_table("submissions")
    op.drop_table("problems")
    op.drop_table("topics")
    op.drop_table("users")
    # The vector extension is intentionally left in place: dropping it would
    # break any other schema in the same database.
