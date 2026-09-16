"""SAP Learning Engine core schema.

Revision ID: 0004
Revises: 0003
Create Date: 2026-09-15
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. sap_courses
    op.create_table(
        "sap_courses",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("slug", sa.String(80), nullable=False, unique=True),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("total_days", sa.Integer(), nullable=False, server_default="100"),
        sa.Column("version", sa.String(20), nullable=False, server_default="1.0"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_sap_courses_slug", "sap_courses", ["slug"])

    # 2. sap_phases
    op.create_table(
        "sap_phases",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "course_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("sap_courses.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("phase_number", sa.Integer(), nullable=False),
        sa.Column("slug", sa.String(80), nullable=False, unique=True),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("subtitle", sa.String(255), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("day_start", sa.Integer(), nullable=False),
        sa.Column("day_end", sa.Integer(), nullable=False),
        sa.Column("color_theme", sa.String(50), nullable=False, server_default="blue"),
        sa.Column("icon", sa.String(80), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("course_id", "phase_number", name="uq_sap_course_phase_number"),
        sa.CheckConstraint("day_end >= day_start", name="ck_sap_phase_day_range"),
    )
    op.create_index("ix_sap_phases_course_id", "sap_phases", ["course_id"])
    op.create_index("ix_sap_phases_slug", "sap_phases", ["slug"])

    # 3. sap_days
    op.create_table(
        "sap_days",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "course_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("sap_courses.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "phase_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("sap_phases.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("day_number", sa.Integer(), nullable=False),
        sa.Column("slug", sa.String(120), nullable=False, unique=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("subtitle", sa.String(255), nullable=True),
        sa.Column("description_md", sa.Text(), nullable=True),
        sa.Column("estimated_minutes", sa.Integer(), nullable=False, server_default="60"),
        sa.Column("tier", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("env_tier", sa.String(50), nullable=False, server_default="browser_only"),
        sa.Column("env_prerequisites", postgresql.JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("objectives", postgresql.JSONB(), nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("theory_content_md", sa.Text(), nullable=True),
        sa.Column("practice_meta", postgresql.JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("course_id", "day_number", name="uq_sap_course_day_number"),
        sa.CheckConstraint("tier BETWEEN 1 AND 5", name="ck_sap_day_tier_range"),
    )
    op.create_index("ix_sap_days_course_id", "sap_days", ["course_id"])
    op.create_index("ix_sap_days_phase_id", "sap_days", ["phase_id"])
    op.create_index("ix_sap_days_day_number", "sap_days", ["day_number"])
    op.create_index("ix_sap_days_slug", "sap_days", ["slug"])
    op.create_index("ix_sap_days_phase_day", "sap_days", ["phase_id", "day_number"])

    # 4. sap_concepts
    op.create_table(
        "sap_concepts",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("slug", sa.String(120), nullable=False, unique=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("category", sa.String(80), nullable=False),
        sa.Column("subcategory", sa.String(100), nullable=True),
        sa.Column("difficulty", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("weight", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint("difficulty BETWEEN 1 AND 5", name="ck_sap_concept_diff_range"),
    )
    op.create_index("ix_sap_concepts_slug", "sap_concepts", ["slug"])
    op.create_index("ix_sap_concepts_category", "sap_concepts", ["category"])
    op.create_index("ix_sap_concepts_category_diff", "sap_concepts", ["category", "difficulty"])

    # 5. sap_concept_prerequisites
    op.create_table(
        "sap_concept_prerequisites",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "prerequisite_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("sap_concepts.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "target_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("sap_concepts.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("relation_type", sa.String(50), nullable=False, server_default="REQUIRED"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("prerequisite_id", "target_id", name="uq_sap_concept_prereq_target"),
        sa.CheckConstraint("prerequisite_id != target_id", name="ck_sap_prereq_no_self_loop"),
    )
    op.create_index("ix_sap_concept_prerequisites_prereq", "sap_concept_prerequisites", ["prerequisite_id"])
    op.create_index("ix_sap_concept_prerequisites_target", "sap_concept_prerequisites", ["target_id"])

    # 6. sap_day_concepts
    op.create_table(
        "sap_day_concepts",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "day_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("sap_days.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "concept_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("sap_concepts.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("role", sa.String(50), nullable=False, server_default="CORE"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("day_id", "concept_id", name="uq_sap_day_concept"),
    )
    op.create_index("ix_sap_day_concepts_day_id", "sap_day_concepts", ["day_id"])
    op.create_index("ix_sap_day_concepts_concept_id", "sap_day_concepts", ["concept_id"])

    # 7. sap_assessments
    op.create_table(
        "sap_assessments",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "day_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("sap_days.id", ondelete="CASCADE"),
            nullable=True,
        ),
        sa.Column("day_number", sa.Integer(), nullable=True),
        sa.Column(
            "primary_concept_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("sap_concepts.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("slug", sa.String(120), nullable=False, unique=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("assessment_type", sa.String(50), nullable=False),
        sa.Column("prompt_md", sa.Text(), nullable=False),
        sa.Column("question_data", postgresql.JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("rubric_or_solution", postgresql.JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("scoring_criteria", postgresql.JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("mastery_impact", postgresql.JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("max_score", sa.Integer(), nullable=False, server_default="100"),
        sa.Column("pass_score", sa.Integer(), nullable=False, server_default="70"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_sap_assessments_day_id", "sap_assessments", ["day_id"])
    op.create_index("ix_sap_assessments_day_number", "sap_assessments", ["day_number"])
    op.create_index("ix_sap_assessments_primary_concept", "sap_assessments", ["primary_concept_id"])
    op.create_index("ix_sap_assessments_slug", "sap_assessments", ["slug"])
    op.create_index("ix_sap_assessments_day_type", "sap_assessments", ["day_number", "assessment_type"])

    # 8. sap_remediation_capsules
    op.create_table(
        "sap_remediation_capsules",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "concept_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("sap_concepts.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("slug", sa.String(120), nullable=False, unique=True),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("deficiency_triggers", postgresql.JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("remediation_content_md", sa.Text(), nullable=False),
        sa.Column("micro_example_code", sa.Text(), nullable=True),
        sa.Column("micro_example_lang", sa.String(30), nullable=False, server_default="abap"),
        sa.Column(
            "recovery_assessment_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("sap_assessments.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("recovery_challenge_spec", postgresql.JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_sap_remediation_capsules_concept_id", "sap_remediation_capsules", ["concept_id"])
    op.create_index("ix_sap_remediation_capsules_slug", "sap_remediation_capsules", ["slug"])
    op.create_index("ix_sap_remediation_capsules_recovery_assessment_id", "sap_remediation_capsules", ["recovery_assessment_id"])

    # 9. sap_placement_profiles
    op.create_table(
        "sap_placement_profiles",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        ),
        sa.Column("persona", sa.String(80), nullable=False),
        sa.Column("experience_years", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("prior_sap_experience", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("diagnostic_results", postgresql.JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("concept_benchmarks", postgresql.JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("recommended_start_day", sa.Integer(), nullable=False, server_default="1"),
        sa.Column(
            "recommended_phase_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("sap_phases.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("rationale", sa.Text(), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_sap_placement_profiles_user_id", "sap_placement_profiles", ["user_id"])
    op.create_index("ix_sap_placement_profiles_phase_id", "sap_placement_profiles", ["recommended_phase_id"])

    # 10. sap_user_state
    op.create_table(
        "sap_user_state",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        ),
        sa.Column(
            "target_course_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("sap_courses.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("current_recommended_day", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("onboarding_persona", sa.String(80), nullable=True),
        sa.Column("placement_status", sa.String(50), nullable=False, server_default="PENDING"),
        sa.Column("placement_score", sa.Float(), nullable=True),
        sa.Column("completed_days_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("streak_days", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("last_active_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("remediation_state", postgresql.JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_sap_user_state_user_id", "sap_user_state", ["user_id"])
    op.create_index("ix_sap_user_state_course_id", "sap_user_state", ["target_course_id"])

    # 11. sap_user_day_state
    op.create_table(
        "sap_user_day_state",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("day_number", sa.Integer(), nullable=False),
        sa.Column(
            "day_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("sap_days.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("status", sa.String(40), nullable=False, server_default="locked"),
        sa.Column("waived", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("lesson_started", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("lesson_started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("lesson_completed", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("lesson_completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("practice_completed", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("practice_completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("assessment_passed", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("assessment_passed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("time_spent_seconds", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("user_id", "day_number", name="uq_sap_user_day_state_user_day"),
    )
    op.create_index("ix_sap_user_day_state_user_id", "sap_user_day_state", ["user_id"])
    op.create_index("ix_sap_user_day_state_day_number", "sap_user_day_state", ["day_number"])
    op.create_index("ix_sap_user_day_state_day_id", "sap_user_day_state", ["day_id"])
    op.create_index("ix_sap_user_day_state_lookup", "sap_user_day_state", ["user_id", "day_number"])

    # 12. sap_user_concept_mastery
    op.create_table(
        "sap_user_concept_mastery",
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
        sa.Column("mastery_score", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("confidence", sa.Float(), nullable=False, server_default="0.5"),
        sa.Column("attempts", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("successful_attempts", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("mastery_state", sa.String(40), nullable=False, server_default="unseen"),
        sa.Column("last_assessed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_mastered_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("history", postgresql.JSONB(), nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("user_id", "concept_id", name="uq_sap_user_concept_mastery"),
        sa.CheckConstraint("mastery_score BETWEEN 0.0 AND 100.0", name="ck_sap_mastery_score_range"),
        sa.CheckConstraint("confidence BETWEEN 0.0 AND 1.0", name="ck_sap_mastery_confidence_range"),
        sa.CheckConstraint(
            "mastery_state IN ('unseen', 'introduced', 'learning', 'practicing', 'mastered', 'needs_remediation')",
            name="ck_sap_mastery_state_valid",
        ),
    )
    op.create_index("ix_sap_user_concept_mastery_user_id", "sap_user_concept_mastery", ["user_id"])
    op.create_index("ix_sap_user_concept_mastery_concept_id", "sap_user_concept_mastery", ["concept_id"])
    op.create_index("ix_sap_user_concept_state", "sap_user_concept_mastery", ["user_id", "mastery_state"])

    # 13. sap_assessment_attempts
    op.create_table(
        "sap_assessment_attempts",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "assessment_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("sap_assessments.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("attempt_type", sa.String(50), nullable=False, server_default="DAILY_CHECK"),
        sa.Column("response", postgresql.JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("evaluation", postgresql.JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("score", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("passed", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("duration_seconds", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_sap_assessment_attempts_user_id", "sap_assessment_attempts", ["user_id"])
    op.create_index("ix_sap_assessment_attempts_assessment_id", "sap_assessment_attempts", ["assessment_id"])
    op.create_index("ix_sap_attempt_user_assessment", "sap_assessment_attempts", ["user_id", "assessment_id"])
    op.create_index("ix_sap_attempt_user_created", "sap_assessment_attempts", ["user_id", "created_at"])


def downgrade() -> None:
    op.drop_table("sap_assessment_attempts")
    op.drop_table("sap_user_concept_mastery")
    op.drop_table("sap_user_day_state")
    op.drop_table("sap_user_state")
    op.drop_table("sap_placement_profiles")
    op.drop_table("sap_remediation_capsules")
    op.drop_table("sap_assessments")
    op.drop_table("sap_day_concepts")
    op.drop_table("sap_concept_prerequisites")
    op.drop_table("sap_concepts")
    op.drop_table("sap_days")
    op.drop_table("sap_phases")
    op.drop_table("sap_courses")
