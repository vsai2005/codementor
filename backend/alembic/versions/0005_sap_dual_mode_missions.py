"""SAP Dual Learning Experiences: Guided Learning & Enterprise Mission Mode.

Revision ID: 0005
Revises: 0004
Create Date: 2026-09-16
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0005"
down_revision = "0004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. sap_enterprises
    op.create_table(
        "sap_enterprises",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("slug", sa.String(80), nullable=False, unique=True),
        sa.Column("name", sa.String(150), nullable=False),
        sa.Column("code", sa.String(10), nullable=False),
        sa.Column("industry", sa.String(100), nullable=False),
        sa.Column("description_md", sa.Text(), nullable=True),
        sa.Column("template_state", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("landscape_metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_sap_enterprises_slug", "sap_enterprises", ["slug"])

    # 2. sap_enterprise_instances
    op.create_table(
        "sap_enterprise_instances",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "enterprise_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("sap_enterprises.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("state_version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("status", sa.String(30), nullable=False, server_default="active"),
        sa.Column("company_state", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("audit_log", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="[]"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("user_id", "enterprise_id", name="uq_sap_enterprise_instance_user_enterprise"),
    )
    op.create_index("ix_sap_enterprise_instance_user", "sap_enterprise_instances", ["user_id"])
    op.create_index("ix_sap_enterprise_instance_enterprise", "sap_enterprise_instances", ["enterprise_id"])

    # 3. sap_missions
    op.create_table(
        "sap_missions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("slug", sa.String(100), nullable=False, unique=True),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("mission_type", sa.String(50), nullable=False),
        sa.Column("difficulty", sa.Integer(), nullable=False, server_default="1"),
        sa.Column(
            "enterprise_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("sap_enterprises.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("company_context", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("initial_state_patch", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("target_state_criteria", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("related_days", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="[]"),
        sa.Column("concept_slugs", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="[]"),
        sa.Column("prerequisite_concepts", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="[]"),
        sa.Column("environment_requirement", sa.String(50), nullable=False, server_default="browser"),
        sa.Column("assistance_rules", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("steps", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="[]"),
        sa.Column("success_criteria", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("failure_conditions", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("estimated_minutes", sa.Integer(), nullable=False, server_default="20"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_sap_missions_slug", "sap_missions", ["slug"])
    op.create_index("ix_sap_missions_enterprise_id", "sap_missions", ["enterprise_id"])

    # 4. sap_mission_concepts
    op.create_table(
        "sap_mission_concepts",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "mission_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("sap_missions.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "concept_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("sap_concepts.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("relevance", sa.String(30), nullable=False, server_default="PRIMARY"),
        sa.UniqueConstraint("mission_id", "concept_id", name="uq_sap_mission_concept"),
    )
    op.create_index("ix_sap_mission_concepts_mission", "sap_mission_concepts", ["mission_id"])
    op.create_index("ix_sap_mission_concepts_concept", "sap_mission_concepts", ["concept_id"])

    # 5. sap_mission_attempts
    op.create_table(
        "sap_mission_attempts",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "mission_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("sap_missions.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("status", sa.String(30), nullable=False, server_default="started"),
        sa.Column("assistance_level", sa.String(20), nullable=False, server_default="TRAINING"),
        sa.Column("current_step_index", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("steps_completed", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="[]"),
        sa.Column("learner_responses", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("state_mutations", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="[]"),
        sa.Column("score", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("passed", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("feedback", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("started_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("duration_seconds", sa.Integer(), nullable=True),
    )
    op.create_index("ix_sap_mission_attempt_user_mission", "sap_mission_attempts", ["user_id", "mission_id"])
    op.create_index("ix_sap_mission_attempt_created", "sap_mission_attempts", ["user_id", "started_at"])

    # 6. sap_skill_evidence
    op.create_table(
        "sap_skill_evidence",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "concept_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("sap_concepts.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("source_type", sa.String(50), nullable=False, server_default="guided_assessment"),
        sa.Column("source_id", sa.String(100), nullable=False),
        sa.Column("mode", sa.String(20), nullable=False, server_default="GUIDED"),
        sa.Column("assistance_level", sa.String(20), nullable=False, server_default="TRAINING"),
        sa.Column("difficulty", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("score", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("result", sa.String(30), nullable=False, server_default="passed"),
        sa.Column("evidence_summary", sa.String(255), nullable=False),
        sa.Column("details", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("recorded_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_sap_skill_evidence_user_concept", "sap_skill_evidence", ["user_id", "concept_id"])
    op.create_index("ix_sap_skill_evidence_user_recorded", "sap_skill_evidence", ["user_id", "recorded_at"])
    op.create_index("ix_sap_skill_evidence_user_source", "sap_skill_evidence", ["user_id", "source_type"])

    # 7. Add dual-mode tracking columns to sap_user_state
    op.add_column("sap_user_state", sa.Column("preferred_mode", sa.String(20), nullable=False, server_default="GUIDED"))
    op.add_column("sap_user_state", sa.Column("last_active_mode", sa.String(20), nullable=False, server_default="GUIDED"))
    op.add_column("sap_user_state", sa.Column("current_guided_day", sa.Integer(), nullable=False, server_default="1"))
    op.add_column(
        "sap_user_state",
        sa.Column(
            "current_mission_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("sap_missions.id", ondelete="SET NULL"),
            nullable=True,
        ),
    )
    op.add_column("sap_user_state", sa.Column("assistance_level", sa.String(20), nullable=False, server_default="TRAINING"))
    op.create_index("ix_sap_user_state_current_mission", "sap_user_state", ["current_mission_id"])


def downgrade() -> None:
    # 1. Remove columns from sap_user_state
    op.drop_index("ix_sap_user_state_current_mission", table_name="sap_user_state")
    op.drop_column("sap_user_state", "assistance_level")
    op.drop_column("sap_user_state", "current_mission_id")
    op.drop_column("sap_user_state", "current_guided_day")
    op.drop_column("sap_user_state", "last_active_mode")
    op.drop_column("sap_user_state", "preferred_mode")

    # 2. Drop tables in reverse dependency order
    op.drop_table("sap_skill_evidence")
    op.drop_table("sap_mission_attempts")
    op.drop_table("sap_mission_concepts")
    op.drop_table("sap_missions")
    op.drop_table("sap_enterprise_instances")
    op.drop_table("sap_enterprises")
