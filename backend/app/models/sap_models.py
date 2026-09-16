"""SQLAlchemy 2.x declarative models for the SAP Learning Engine."""

from __future__ import annotations

import enum
import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.models import Base, _uuid_pk


class SAPMasteryState(str, enum.Enum):
    UNSEEN = "unseen"
    INTRODUCED = "introduced"
    LEARNING = "learning"
    PRACTICING = "practicing"
    MASTERED = "mastered"
    NEEDS_REMEDIATION = "needs_remediation"


class SAPPrerequisiteType(str, enum.Enum):
    REQUIRED = "REQUIRED"
    RECOMMENDED = "RECOMMENDED"
    EXPANDS_UPON = "EXPANDS_UPON"


class SAPDayConceptRole(str, enum.Enum):
    CORE = "CORE"
    SECONDARY = "SECONDARY"
    REINFORCEMENT = "REINFORCEMENT"


class SAPPlacementStatus(str, enum.Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    SKIPPED = "SKIPPED"


class SAPAssessmentAttemptType(str, enum.Enum):
    DAILY_CHECK = "DAILY_CHECK"
    PRACTICE = "PRACTICE"
    REMEDIATION_RECOVERY = "REMEDIATION_RECOVERY"
    PLACEMENT_TEST = "PLACEMENT_TEST"


class SAPDayStatus(str, enum.Enum):
    LOCKED = "locked"
    AVAILABLE = "available"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    WAIVED_BY_PLACEMENT = "waived_by_placement"


class SAPLearningMode(str, enum.Enum):
    GUIDED = "GUIDED"
    MISSION = "MISSION"


class SAPAssistanceLevel(str, enum.Enum):
    TRAINING = "TRAINING"
    GUIDED = "GUIDED"
    JOB = "JOB"


class SAPMissionType(str, enum.Enum):
    BUSINESS_REQUEST = "business_request"
    PROCESS_TASK = "process_task"
    INCIDENT = "incident"
    TROUBLESHOOTING = "troubleshooting"
    CONFIGURATION = "configuration"
    ARCHITECTURE_DECISION = "architecture_decision"
    DATA_TASK = "data_task"
    DEVELOPMENT_TASK = "development_task"
    INTEGRATION_TASK = "integration_task"
    PROJECT = "project"
    CAPSTONE = "capstone"


class SAPMissionAttemptStatus(str, enum.Enum):
    STARTED = "started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class SAPSkillEvidenceSourceType(str, enum.Enum):
    GUIDED_ASSESSMENT = "guided_assessment"
    MISSION = "mission"
    REMEDIATION = "remediation"
    SIMULATION = "simulation"
    STATIC_VALIDATION = "static_validation"
    PLACEMENT = "placement"
    CAPSTONE = "capstone"


# =============================================================================
# 1. Curriculum & Roadmap
# =============================================================================


class SAPCourse(Base):
    __tablename__ = "sap_courses"

    id: Mapped[uuid.UUID] = _uuid_pk()
    slug: Mapped[str] = mapped_column(String(80), unique=True, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    total_days: Mapped[int] = mapped_column(Integer, nullable=False, default=100)
    version: Mapped[str] = mapped_column(String(20), nullable=False, default="1.0")
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    phases: Mapped[list[SAPPhase]] = relationship(
        back_populates="course", cascade="all, delete-orphan"
    )
    days: Mapped[list[SAPDay]] = relationship(
        back_populates="course", cascade="all, delete-orphan"
    )


class SAPPhase(Base):
    __tablename__ = "sap_phases"

    id: Mapped[uuid.UUID] = _uuid_pk()
    course_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("sap_courses.id", ondelete="CASCADE"), nullable=False, index=True
    )
    phase_number: Mapped[int] = mapped_column(Integer, nullable=False)
    slug: Mapped[str] = mapped_column(String(80), unique=True, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    subtitle: Mapped[str | None] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text)
    day_start: Mapped[int] = mapped_column(Integer, nullable=False)
    day_end: Mapped[int] = mapped_column(Integer, nullable=False)
    color_theme: Mapped[str] = mapped_column(String(50), nullable=False, default="blue")
    icon: Mapped[str | None] = mapped_column(String(80))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    course: Mapped[SAPCourse] = relationship(back_populates="phases")
    days: Mapped[list[SAPDay]] = relationship(
        back_populates="phase", cascade="all, delete-orphan"
    )

    __table_args__ = (
        UniqueConstraint("course_id", "phase_number", name="uq_sap_course_phase_number"),
        CheckConstraint("day_end >= day_start", name="ck_sap_phase_day_range"),
    )


class SAPDay(Base):
    __tablename__ = "sap_days"

    id: Mapped[uuid.UUID] = _uuid_pk()
    course_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("sap_courses.id", ondelete="CASCADE"), nullable=False, index=True
    )
    phase_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("sap_phases.id", ondelete="CASCADE"), nullable=False, index=True
    )
    day_number: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    slug: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    subtitle: Mapped[str | None] = mapped_column(String(255))
    description_md: Mapped[str | None] = mapped_column(Text)
    estimated_minutes: Mapped[int] = mapped_column(Integer, nullable=False, default=60)
    tier: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    env_tier: Mapped[str] = mapped_column(String(50), nullable=False, default="browser_only")
    env_prerequisites: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    objectives: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    theory_content_md: Mapped[str | None] = mapped_column(Text)
    practice_meta: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    course: Mapped[SAPCourse] = relationship(back_populates="days")
    phase: Mapped[SAPPhase] = relationship(back_populates="days")
    day_concepts: Mapped[list[SAPDayConcept]] = relationship(
        back_populates="day", cascade="all, delete-orphan"
    )
    assessments: Mapped[list[SAPAssessment]] = relationship(
        back_populates="day", cascade="all, delete-orphan"
    )
    user_day_states: Mapped[list[SAPUserDayState]] = relationship(back_populates="day")

    __table_args__ = (
        UniqueConstraint("course_id", "day_number", name="uq_sap_course_day_number"),
        CheckConstraint("tier BETWEEN 1 AND 5", name="ck_sap_day_tier_range"),
        Index("ix_sap_days_phase_day", "phase_id", "day_number"),
    )


# =============================================================================
# 2. Concept Knowledge Graph (DAG)
# =============================================================================


class SAPConcept(Base):
    __tablename__ = "sap_concepts"

    id: Mapped[uuid.UUID] = _uuid_pk()
    slug: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    category: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    subcategory: Mapped[str | None] = mapped_column(String(100))
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    description: Mapped[str | None] = mapped_column(Text)
    weight: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    prerequisites: Mapped[list[SAPConceptPrerequisite]] = relationship(
        "SAPConceptPrerequisite",
        foreign_keys="SAPConceptPrerequisite.target_id",
        back_populates="target",
        cascade="all, delete-orphan",
    )
    dependents: Mapped[list[SAPConceptPrerequisite]] = relationship(
        "SAPConceptPrerequisite",
        foreign_keys="SAPConceptPrerequisite.prerequisite_id",
        back_populates="prerequisite",
        cascade="all, delete-orphan",
    )
    day_mappings: Mapped[list[SAPDayConcept]] = relationship(
        back_populates="concept", cascade="all, delete-orphan"
    )
    remediation_capsules: Mapped[list[SAPRemediationCapsule]] = relationship(
        back_populates="concept", cascade="all, delete-orphan"
    )
    user_masteries: Mapped[list[SAPUserConceptMastery]] = relationship(
        back_populates="concept", cascade="all, delete-orphan"
    )

    __table_args__ = (
        CheckConstraint("difficulty BETWEEN 1 AND 5", name="ck_sap_concept_diff_range"),
        Index("ix_sap_concepts_category_diff", "category", "difficulty"),
    )


class SAPConceptPrerequisite(Base):
    __tablename__ = "sap_concept_prerequisites"

    id: Mapped[uuid.UUID] = _uuid_pk()
    prerequisite_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("sap_concepts.id", ondelete="CASCADE"), nullable=False, index=True
    )
    target_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("sap_concepts.id", ondelete="CASCADE"), nullable=False, index=True
    )
    relation_type: Mapped[str] = mapped_column(
        String(50), nullable=False, default=SAPPrerequisiteType.REQUIRED.value
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    prerequisite: Mapped[SAPConcept] = relationship(
        "SAPConcept", foreign_keys=[prerequisite_id], back_populates="dependents"
    )
    target: Mapped[SAPConcept] = relationship(
        "SAPConcept", foreign_keys=[target_id], back_populates="prerequisites"
    )

    __table_args__ = (
        UniqueConstraint("prerequisite_id", "target_id", name="uq_sap_concept_prereq_target"),
        CheckConstraint("prerequisite_id != target_id", name="ck_sap_prereq_no_self_loop"),
    )


class SAPDayConcept(Base):
    __tablename__ = "sap_day_concepts"

    id: Mapped[uuid.UUID] = _uuid_pk()
    day_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("sap_days.id", ondelete="CASCADE"), nullable=False, index=True
    )
    concept_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("sap_concepts.id", ondelete="CASCADE"), nullable=False, index=True
    )
    role: Mapped[str] = mapped_column(
        String(50), nullable=False, default=SAPDayConceptRole.CORE.value
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    day: Mapped[SAPDay] = relationship(back_populates="day_concepts")
    concept: Mapped[SAPConcept] = relationship(back_populates="day_mappings")

    __table_args__ = (
        UniqueConstraint("day_id", "concept_id", name="uq_sap_day_concept"),
    )


# =============================================================================
# 3. Assessment & Remediation Engine
# =============================================================================


class SAPAssessment(Base):
    __tablename__ = "sap_assessments"

    id: Mapped[uuid.UUID] = _uuid_pk()
    day_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("sap_days.id", ondelete="CASCADE"), nullable=True, index=True
    )
    day_number: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    primary_concept_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("sap_concepts.id", ondelete="SET NULL"), nullable=True, index=True
    )
    slug: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    assessment_type: Mapped[str] = mapped_column(String(50), nullable=False)
    prompt_md: Mapped[str] = mapped_column(Text, nullable=False)
    question_data: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    rubric_or_solution: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    scoring_criteria: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    mastery_impact: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    max_score: Mapped[int] = mapped_column(Integer, nullable=False, default=100)
    pass_score: Mapped[int] = mapped_column(Integer, nullable=False, default=70)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    day: Mapped[SAPDay | None] = relationship(back_populates="assessments")
    primary_concept: Mapped[SAPConcept | None] = relationship()
    attempts: Mapped[list[SAPAssessmentAttempt]] = relationship(
        back_populates="assessment", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("ix_sap_assessments_day_type", "day_number", "assessment_type"),
    )


class SAPRemediationCapsule(Base):
    __tablename__ = "sap_remediation_capsules"

    id: Mapped[uuid.UUID] = _uuid_pk()
    concept_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("sap_concepts.id", ondelete="CASCADE"), nullable=False, index=True
    )
    slug: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    deficiency_triggers: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    remediation_content_md: Mapped[str] = mapped_column(Text, nullable=False)
    micro_example_code: Mapped[str | None] = mapped_column(Text)
    micro_example_lang: Mapped[str] = mapped_column(String(30), nullable=False, default="abap")
    recovery_assessment_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("sap_assessments.id", ondelete="SET NULL"), nullable=True, index=True
    )
    recovery_challenge_spec: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    concept: Mapped[SAPConcept] = relationship(back_populates="remediation_capsules")
    recovery_assessment: Mapped[SAPAssessment | None] = relationship()


# =============================================================================
# 4. User Placement, Progress & Continuous Mastery
# =============================================================================


class SAPPlacementProfile(Base):
    __tablename__ = "sap_placement_profiles"

    id: Mapped[uuid.UUID] = _uuid_pk()
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True
    )
    persona: Mapped[str] = mapped_column(String(80), nullable=False)
    experience_years: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    prior_sap_experience: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    diagnostic_results: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    concept_benchmarks: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    recommended_start_day: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    recommended_phase_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("sap_phases.id", ondelete="SET NULL"), nullable=True, index=True
    )
    rationale: Mapped[str | None] = mapped_column(Text)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    recommended_phase: Mapped[SAPPhase | None] = relationship()


class SAPUserState(Base):
    __tablename__ = "sap_user_state"

    id: Mapped[uuid.UUID] = _uuid_pk()
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True
    )
    target_course_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("sap_courses.id", ondelete="SET NULL"), nullable=True, index=True
    )
    current_recommended_day: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    onboarding_persona: Mapped[str | None] = mapped_column(String(80))
    placement_status: Mapped[str] = mapped_column(
        String(50), nullable=False, default=SAPPlacementStatus.PENDING.value
    )
    placement_score: Mapped[float | None] = mapped_column(Float)
    completed_days_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    preferred_mode: Mapped[str] = mapped_column(
        String(20), nullable=False, default=SAPLearningMode.GUIDED.value
    )
    last_active_mode: Mapped[str] = mapped_column(
        String(20), nullable=False, default=SAPLearningMode.GUIDED.value
    )
    current_guided_day: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    current_mission_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("sap_missions.id", ondelete="SET NULL"), nullable=True, index=True
    )
    assistance_level: Mapped[str] = mapped_column(
        String(20), nullable=False, default=SAPAssistanceLevel.TRAINING.value
    )
    streak_days: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    last_active_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    remediation_state: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    target_course: Mapped[SAPCourse | None] = relationship()


class SAPUserDayState(Base):
    __tablename__ = "sap_user_day_state"

    id: Mapped[uuid.UUID] = _uuid_pk()
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    day_number: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    day_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("sap_days.id", ondelete="SET NULL"), nullable=True, index=True
    )
    status: Mapped[str] = mapped_column(
        String(40), nullable=False, default=SAPDayStatus.LOCKED.value
    )
    waived: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    lesson_started: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    lesson_started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    lesson_completed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    lesson_completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    practice_completed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    practice_completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    assessment_passed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    assessment_passed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    completed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    time_spent_seconds: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    day: Mapped[SAPDay | None] = relationship(back_populates="user_day_states")

    __table_args__ = (
        UniqueConstraint("user_id", "day_number", name="uq_sap_user_day_state_user_day"),
        Index("ix_sap_user_day_state_lookup", "user_id", "day_number"),
    )


class SAPUserConceptMastery(Base):
    __tablename__ = "sap_user_concept_mastery"

    id: Mapped[uuid.UUID] = _uuid_pk()
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    concept_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("sap_concepts.id", ondelete="CASCADE"), nullable=False, index=True
    )
    mastery_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.5)
    attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    successful_attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    mastery_state: Mapped[str] = mapped_column(
        String(40), nullable=False, default=SAPMasteryState.UNSEEN.value
    )
    last_assessed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_mastered_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    history: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    concept: Mapped[SAPConcept] = relationship(back_populates="user_masteries")

    __table_args__ = (
        UniqueConstraint("user_id", "concept_id", name="uq_sap_user_concept_mastery"),
        CheckConstraint("mastery_score BETWEEN 0.0 AND 100.0", name="ck_sap_mastery_score_range"),
        CheckConstraint("confidence BETWEEN 0.0 AND 1.0", name="ck_sap_mastery_confidence_range"),
        CheckConstraint(
            "mastery_state IN ('unseen', 'introduced', 'learning', 'practicing', 'mastered', 'needs_remediation')",
            name="ck_sap_mastery_state_valid",
        ),
        Index("ix_sap_user_concept_state", "user_id", "mastery_state"),
    )


class SAPAssessmentAttempt(Base):
    __tablename__ = "sap_assessment_attempts"

    id: Mapped[uuid.UUID] = _uuid_pk()
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    assessment_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("sap_assessments.id", ondelete="CASCADE"), nullable=False, index=True
    )
    attempt_type: Mapped[str] = mapped_column(
        String(50), nullable=False, default=SAPAssessmentAttemptType.DAILY_CHECK.value
    )
    response: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    evaluation: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    passed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    duration_seconds: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )

    assessment: Mapped[SAPAssessment] = relationship(back_populates="attempts")

    __table_args__ = (
        Index("ix_sap_attempt_user_assessment", "user_id", "assessment_id"),
        Index("ix_sap_attempt_user_created", "user_id", "created_at"),
    )


# =============================================================================
# 5. Enterprise Digital Twin, Missions & Skill Evidence
# =============================================================================


class SAPEnterprise(Base):
    __tablename__ = "sap_enterprises"

    id: Mapped[uuid.UUID] = _uuid_pk()
    slug: Mapped[str] = mapped_column(String(80), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    code: Mapped[str] = mapped_column(String(10), nullable=False)  # e.g. "NM01"
    industry: Mapped[str] = mapped_column(String(100), nullable=False)
    description_md: Mapped[str | None] = mapped_column(Text)
    template_state: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    landscape_metadata: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    instances: Mapped[list[SAPEnterpriseInstance]] = relationship(
        back_populates="enterprise", cascade="all, delete-orphan"
    )
    missions: Mapped[list[SAPMission]] = relationship(back_populates="enterprise")


class SAPEnterpriseInstance(Base):
    __tablename__ = "sap_enterprise_instances"

    id: Mapped[uuid.UUID] = _uuid_pk()
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    enterprise_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("sap_enterprises.id", ondelete="CASCADE"), nullable=False, index=True
    )
    state_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="active")
    company_state: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    audit_log: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    enterprise: Mapped[SAPEnterprise] = relationship(back_populates="instances")

    __table_args__ = (
        UniqueConstraint("user_id", "enterprise_id", name="uq_sap_enterprise_instance_user_enterprise"),
        Index("ix_sap_enterprise_instance_user", "user_id"),
    )


class SAPMission(Base):
    __tablename__ = "sap_missions"

    id: Mapped[uuid.UUID] = _uuid_pk()
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    mission_type: Mapped[str] = mapped_column(String(50), nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    enterprise_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("sap_enterprises.id", ondelete="SET NULL"), nullable=True, index=True
    )
    company_context: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    initial_state_patch: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    target_state_criteria: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    related_days: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    concept_slugs: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    prerequisite_concepts: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    environment_requirement: Mapped[str] = mapped_column(String(50), nullable=False, default="browser")
    assistance_rules: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    steps: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    success_criteria: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    failure_conditions: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    estimated_minutes: Mapped[int] = mapped_column(Integer, nullable=False, default=20)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    enterprise: Mapped[SAPEnterprise | None] = relationship(back_populates="missions")
    mission_concepts: Mapped[list[SAPMissionConcept]] = relationship(
        back_populates="mission", cascade="all, delete-orphan"
    )
    attempts: Mapped[list[SAPMissionAttempt]] = relationship(
        back_populates="mission", cascade="all, delete-orphan"
    )


class SAPMissionConcept(Base):
    __tablename__ = "sap_mission_concepts"

    id: Mapped[uuid.UUID] = _uuid_pk()
    mission_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("sap_missions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    concept_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("sap_concepts.id", ondelete="CASCADE"), nullable=False, index=True
    )
    relevance: Mapped[str] = mapped_column(String(30), nullable=False, default="PRIMARY")

    mission: Mapped[SAPMission] = relationship(back_populates="mission_concepts")
    concept: Mapped[SAPConcept] = relationship()

    __table_args__ = (
        UniqueConstraint("mission_id", "concept_id", name="uq_sap_mission_concept"),
    )


class SAPMissionAttempt(Base):
    __tablename__ = "sap_mission_attempts"

    id: Mapped[uuid.UUID] = _uuid_pk()
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    mission_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("sap_missions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    status: Mapped[str] = mapped_column(
        String(30), nullable=False, default=SAPMissionAttemptStatus.STARTED.value
    )
    assistance_level: Mapped[str] = mapped_column(
        String(20), nullable=False, default=SAPAssistanceLevel.TRAINING.value
    )
    current_step_index: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    steps_completed: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    learner_responses: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    state_mutations: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    passed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    feedback: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    duration_seconds: Mapped[int | None] = mapped_column(Integer)

    mission: Mapped[SAPMission] = relationship(back_populates="attempts")

    __table_args__ = (
        Index("ix_sap_mission_attempt_user_mission", "user_id", "mission_id"),
        Index("ix_sap_mission_attempt_created", "user_id", "started_at"),
    )


class SAPSkillEvidence(Base):
    __tablename__ = "sap_skill_evidence"

    id: Mapped[uuid.UUID] = _uuid_pk()
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    concept_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("sap_concepts.id", ondelete="CASCADE"), nullable=False, index=True
    )
    source_type: Mapped[str] = mapped_column(
        String(50), nullable=False, default=SAPSkillEvidenceSourceType.GUIDED_ASSESSMENT.value
    )
    source_id: Mapped[str] = mapped_column(String(100), nullable=False)
    mode: Mapped[str] = mapped_column(
        String(20), nullable=False, default=SAPLearningMode.GUIDED.value
    )
    assistance_level: Mapped[str] = mapped_column(
        String(20), nullable=False, default=SAPAssistanceLevel.TRAINING.value
    )
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    result: Mapped[str] = mapped_column(String(30), nullable=False, default="passed")
    evidence_summary: Mapped[str] = mapped_column(String(255), nullable=False)
    details: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )

    concept: Mapped[SAPConcept] = relationship()

    __table_args__ = (
        Index("ix_sap_skill_evidence_user_concept", "user_id", "concept_id"),
        Index("ix_sap_skill_evidence_user_recorded", "user_id", "recorded_at"),
        Index("ix_sap_skill_evidence_user_source", "user_id", "source_type"),
    )
