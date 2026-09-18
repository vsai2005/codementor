"""SAP Pydantic Request/Response Models."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Literal
from pydantic import BaseModel, ConfigDict, Field

from app.models.sap_models import SAPMasteryState, SAPPlacementStatus


# --- Curriculum Schemas ---

class SAPPhaseSummary(BaseModel):
    phase_number: int
    slug: str
    title: str
    subtitle: str | None = None
    day_start: int
    day_end: int
    color_theme: str
    icon: str | None = None


class SAPDaySummary(BaseModel):
    day_number: int
    phase_number: int
    slug: str
    title: str
    description: str
    tier: int
    env_tier: str
    estimated_minutes: int
    atomic_concepts: list[str] = Field(default_factory=list)
    practice_types: list[str] = Field(default_factory=list)
    assessment_types: list[str] = Field(default_factory=list)


class SAPDayDetail(SAPDaySummary):
    objectives: list[str] = Field(default_factory=list)
    env_prerequisites: dict[str, Any] = Field(default_factory=dict)
    prerequisites: list[str] = Field(default_factory=list)


class SAPConceptDetail(BaseModel):
    slug: str
    name: str
    category: str
    difficulty: int
    curriculum_days: list[int] = Field(default_factory=list)
    direct_prerequisites: list[str] = Field(default_factory=list)
    all_ancestor_prerequisites: list[str] = Field(default_factory=list)
    root_prerequisites: list[str] = Field(default_factory=list)
    dependents: list[str] = Field(default_factory=list)
    mastery_threshold: float = 80.0
    remediation_available: bool = False
    remediation_capsule_slug: str | None = None


class SAPRemediationCapsuleDetail(BaseModel):
    slug: str
    target_concept_slug: str
    title: str
    deficiency_triggers: list[str]
    prerequisite_deficiencies: list[str]
    remediation_content_md: str
    recovery_assessment_slug: str


# --- Progression Schemas ---

class SAPDayStateDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    day_number: int
    lesson_completed: bool
    lesson_completed_at: datetime | None = None
    practice_completed: bool = False
    practice_completed_at: datetime | None = None
    assessment_passed: bool
    assessment_passed_at: datetime | None = None
    completed: bool
    completed_at: datetime | None = None
    waived: bool = False
    unlocked: bool
    status: Literal["completed", "current", "available", "locked", "in_progress", "waived_by_placement"]


class SAPProgressResponse(BaseModel):
    course_slug: str = "sap-s4hana-mastery"
    current_day: int
    completed_days: list[int]
    waived_days: list[int] = Field(default_factory=list)
    total_days: int = 100
    day_states: dict[str, SAPDayStateDetail]


class SAPCompleteLessonRequest(BaseModel):
    day_number: int = Field(..., ge=1, le=100, description="SAP day number to mark complete")


class SAPCompleteLessonResponse(BaseModel):
    day_number: int
    lesson_completed: bool
    day_completed: bool
    unlocked_next_day: bool
    current_day: int
    day_state: SAPDayStateDetail


class SAPCompletePracticeRequest(BaseModel):
    day_number: int = Field(..., ge=1, le=100, description="SAP day number for practice completion")


class SAPCompletePracticeResponse(BaseModel):
    day_number: int
    practice_completed: bool
    day_completed: bool = False
    unlocked_next_day: bool = False
    current_day: int | None = None
    day_state: SAPDayStateDetail | None = None


# --- Concept Mastery Schemas ---

class SAPConceptMasteryItem(BaseModel):
    concept_slug: str
    mastery_state: SAPMasteryState
    mastery_score: float
    confidence: float
    attempts: int
    successful_attempts: int
    last_assessed_at: datetime | None = None
    last_mastered_at: datetime | None = None


class SAPMasterySummaryResponse(BaseModel):
    total_tracked: int
    breakdown: dict[str, int]
    concepts: list[SAPConceptMasteryItem]


class SAPRecordConceptMasteryRequest(BaseModel):
    concept_slug: str
    score: float = Field(..., ge=0.0, le=100.0)


# --- Placement Schemas ---

class PlacementQuestionOption(BaseModel):
    id: str
    text: str


class PlacementQuestionOut(BaseModel):
    id: str
    topic: str
    topic_label: str
    concept_slug: str
    question: str
    options: list[PlacementQuestionOption]
    difficulty: int = 1


class SAPPlacementDiagnosticRequest(BaseModel):
    experience_level: str | None = Field(
        default=None,
        description="Experience level: 'fresher', 'experienced', or 'not_sure'."
    )
    persona_self_select: str | None = None
    experience_years: float = Field(default=0.0, ge=0.0)
    answers: dict[str, str] = Field(
        default_factory=dict,
        description="Map of question ID -> chosen option ID ('a', 'b', 'c', 'd')."
    )
    domain_scores: dict[str, float] | None = Field(
        default=None,
        description="Optional benchmark scores per domain (0.0 to 100.0) for backward compatibility."
    )


class SAPPlacementChooseStartRequest(BaseModel):
    start_day: int = Field(..., ge=1, le=100, description="Desired starting day number (e.g. 1 or recommended day)")


class SAPPlacementProfileResponse(BaseModel):
    persona: str
    diagnostic_score: float
    recommended_start_day: int
    unlocked_days: list[int]
    waived_days: list[int] = Field(default_factory=list)
    rationale: str
    domain_scores: dict[str, float] = Field(default_factory=dict)
    topic_breakdown: list[dict[str, Any]] = Field(default_factory=list)
    demonstrated_concepts: list[str] = Field(default_factory=list)
    gap_concepts: list[str] = Field(default_factory=list)



# --- Assessment Schemas ---

SAPAssessmentType = Literal[
    "abap_challenge",
    "analytics_eval",
    "capstone_multi_concept",
    "capstone_quiz",
    "cds_challenge",
    "concept_quiz",
    "data_modeling",
    "decision_matrix",
    "mcq",
    "process_ordering",
    "rap_challenge",
    "rubric_based",
    "scenario_decision",
    "simulation",
    "technical_audit",
    "troubleshooting",
]


class SAPAssessmentSubmitRequest(BaseModel):
    day_number: int = Field(..., ge=1, le=100)
    assessment_id: str
    assessment_type: SAPAssessmentType = Field(
        ...,
        description="Explicit validated curriculum assessment type: e.g. 'capstone_multi_concept', 'mcq', 'process_ordering', 'scenario_decision', 'rubric_based', 'simulation', 'troubleshooting', 'abap_challenge', 'cds_challenge', 'rap_challenge', etc."
    )
    rubric_spec: dict[str, Any] = Field(default_factory=dict)
    submission_payload: dict[str, Any] = Field(default_factory=dict)


class SAPAssessmentSubmitResponse(BaseModel):
    submission_id: str
    passed: bool
    score: float
    feedback: str
    evaluation_breakdown: dict[str, Any]
    mastery_updated: bool = False
    concept_evaluations: list[dict[str, Any]] = Field(default_factory=list)
    remediation_required: bool = False
    remediation_capsule: SAPRemediationCapsuleDetail | None = None
    all_remediations: list[dict[str, Any]] = Field(default_factory=list)
    day_completed: bool = False
    unlocked_next_day: bool = False
    current_day: int | None = None
    next_day_number: int | None = None


# --- Execution Provider Schemas ---

class SAPExecutionValidateRequest(BaseModel):
    provider_type: Literal["simulation", "cds_validation", "abap_cloud"]
    code_or_payload: str
    context_parameters: dict[str, Any] = Field(default_factory=dict)


class DiagnosticFindingOut(BaseModel):
    severity: Literal["error", "warning", "info"]
    line: int | None = None
    column: int | None = None
    rule_code: str
    message: str


class SAPExecutionValidateResponse(BaseModel):
    success: bool
    status: str
    output: str
    findings: list[DiagnosticFindingOut] = Field(default_factory=list)
    runtime_ms: int = 0
    # Truthfulness metadata
    provider_category: str = Field(
        default="STATIC_VALIDATION",
        description="Execution classification: STATIC_VALIDATION | LOCAL_SIMULATION | REAL_SAP_EXECUTION",
    )
    is_sandboxed_simulation: bool = Field(
        default=False,
        description="Whether verification occurred in an in-memory mock/sandboxed simulation",
    )
    is_live_sap_system: bool = Field(
        default=False,
        description="Truthfulness indicator: False affirms no connection to live SAP NetWeaver/BTP/kernel",
    )


# --- Mode & Assistance Schemas ---

class SAPModeSwitchRequest(BaseModel):
    mode: Literal["GUIDED", "MISSION"]
    assistance_level: Literal["TRAINING", "GUIDED", "JOB"] | None = None


class SAPModeStateResponse(BaseModel):
    preferred_mode: str
    last_active_mode: str
    current_guided_day: int
    current_mission_id: str | None = None
    assistance_level: str


# --- Enterprise Digital Twin Schemas ---

class SAPEnterpriseViewResponse(BaseModel):
    slug: str
    name: str
    code: str
    industry: str
    description_md: str | None = None
    company_state: dict[str, Any] = Field(default_factory=dict)
    landscape_metadata: dict[str, Any] = Field(default_factory=dict)
    state_version: int = 1
    status: str = "active"


class SAPEnterpriseResetResponse(BaseModel):
    status: str
    state_version: int
    message: str


# --- Mission Schemas ---

class SAPMissionSummary(BaseModel):
    id: str
    slug: str
    title: str
    description: str
    mission_type: str
    difficulty: int
    estimated_minutes: int
    related_days: list[int] = Field(default_factory=list)
    concept_slugs: list[str] = Field(default_factory=list)
    is_unlocked: bool = True
    missing_prerequisites: list[str] = Field(default_factory=list)
    attempt_status: str = "not_started"
    score: float | None = None
    passed: bool = False


class SAPMissionDetail(BaseModel):
    id: str
    slug: str
    title: str
    description: str
    mission_type: str
    difficulty: int
    estimated_minutes: int
    company_context: dict[str, Any] = Field(default_factory=dict)
    enterprise_code: str = "NM01"
    company_state: dict[str, Any] = Field(default_factory=dict)
    assistance_level: str = "TRAINING"
    assistance_rules: dict[str, Any] = Field(default_factory=dict)
    steps: list[dict[str, Any]] = Field(default_factory=list)
    related_days: list[int] = Field(default_factory=list)
    concept_slugs: list[str] = Field(default_factory=list)
    current_attempt: dict[str, Any] | None = None


class SAPMissionStartResponse(BaseModel):
    mission_slug: str
    attempt_id: str
    status: str
    assistance_level: str
    current_step_index: int = 0


class SAPMissionStepAttemptRequest(BaseModel):
    step_id: str
    payload: dict[str, Any] = Field(default_factory=dict)
    assistance_level: Literal["TRAINING", "GUIDED", "JOB"] = "TRAINING"


class SAPMissionStepAttemptResponse(BaseModel):
    step_id: str
    step_success: bool
    step_feedback: str
    mission_completed: bool
    mission_passed: bool
    current_score: float
    steps_completed_count: int
    total_steps: int


# --- Skill Evidence Schemas ---

class SAPSkillEvidenceItem(BaseModel):
    id: str
    concept_slug: str
    concept_name: str | None = None
    source_type: str
    source_id: str
    mode: str
    assistance_level: str
    difficulty: int
    score: float
    result: str
    evidence_summary: str
    details: dict[str, Any] = Field(default_factory=dict)
    recorded_at: str | None = None


class SAPSkillEvidenceSummaryResponse(BaseModel):
    user_id: str
    total_evidence_count: int
    evidences: list[SAPSkillEvidenceItem] = Field(default_factory=list)


# --- Lesson Detail Schemas ---

class SAPLessonStep(BaseModel):
    step_id: str
    step_type: str
    title: str
    content_md: str | None = None
    subtitle: str | None = None
    key_terms: list[dict[str, str]] | None = None
    takeaway: str | None = None
    company_context: dict[str, Any] | None = None
    component_type: str | None = None
    instruction: str | None = None
    flow_data: list[dict[str, Any]] | None = None
    scenarios: list[dict[str, Any]] | None = None
    items: list[dict[str, Any]] | None = None
    units: list[dict[str, Any]] | None = None
    scenario_md: str | None = None
    options: list[dict[str, Any]] | None = None
    concept_slug: str | None = None
    questions: list[dict[str, Any]] | None = None
    evidence_rule: str | None = None
    summary_md: str | None = None
    recommended_mission: dict[str, str] | None = None
    is_capstone: bool | None = None
    multi_concept_eval: bool | None = None
    concepts_evaluated: list[str] | None = None


class SAPLessonDetail(BaseModel):
    day_number: int
    slug: str
    title: str
    subtitle: str | None = None
    estimated_minutes: int = 60
    atomic_concepts: list[str] = Field(default_factory=list)
    recommended_mission_slug: str | None = None
    steps: list[SAPLessonStep] = Field(default_factory=list)


