export interface SapCourse {
  slug: string;
  title: string;
  description: string;
  total_days: number;
  version: string;
}

export interface SapPhase {
  phase_number: number;
  slug: string;
  title: string;
  subtitle?: string | null;
  day_start: number;
  day_end: number;
  color_theme: string;
  icon?: string | null;
}

export interface SapDaySummary {
  day_number: number;
  phase_number: number;
  slug: string;
  title: string;
  description: string;
  tier: number;
  env_tier: string;
  estimated_minutes: number;
  atomic_concepts: string[];
  practice_types: string[];
  assessment_types: string[];
}

export interface SapDayDetail extends SapDaySummary {
  objectives: string[];
  env_prerequisites: Record<string, any>;
  prerequisites: string[];
}

export interface SapCurriculumOverview {
  course: SapCourse;
  phases: SapPhase[];
  total_days: number;
  days: SapDaySummary[];
}

export type SapDayStatus =
  | "completed"
  | "current"
  | "available"
  | "locked"
  | "in_progress"
  | "waived_by_placement";

export interface SapDayStateDetail {
  day_number: number;
  lesson_completed: boolean;
  lesson_completed_at?: string | null;
  practice_completed: boolean;
  practice_completed_at?: string | null;
  assessment_passed: boolean;
  assessment_passed_at?: string | null;
  completed: boolean;
  completed_at?: string | null;
  waived?: boolean;
  unlocked: boolean;
  status: SapDayStatus;
}

export interface SapProgressResponse {
  course_slug: string;
  current_day: number;
  completed_days: number[];
  waived_days?: number[];
  total_days: number;
  day_states: Record<string, SapDayStateDetail>;
}

export interface SapPracticeStepResult {
  step_id: string;
  correct: boolean;
  feedback?: string | null;
}

export interface SapCompletePracticeResponse {
  day_number: number;
  passed: boolean;
  practice_completed: boolean;
  results: SapPracticeStepResult[];
  day_completed?: boolean;
  unlocked_next_day?: boolean;
  current_day?: number | null;
  day_state?: SapDayStateDetail | null;
}

export interface SapCompleteLessonResponse {
  day_number: number;
  lesson_completed: boolean;
  day_completed: boolean;
  unlocked_next_day: boolean;
  current_day: number;
  day_state: SapDayStateDetail;
}

export interface PlacementQuestionOption {
  id: string;
  text: string;
}

export interface PlacementQuestion {
  id: string;
  topic: string;
  topic_label: string;
  concept_slug: string;
  question: string;
  options: PlacementQuestionOption[];
  difficulty: number;
}

export interface SapPlacementProfile {
  persona: string;
  diagnostic_score: number;
  recommended_start_day: number;
  unlocked_days: number[];
  waived_days?: number[];
  rationale: string;
  domain_scores: Record<string, number>;
  topic_breakdown?: Array<{
    topic: string;
    label: string;
    score: number;
  }>;
  demonstrated_concepts?: string[];
  gap_concepts?: string[];
}

export type SapExecutionCategory =
  | "STATIC_VALIDATION"
  | "LOCAL_SIMULATION"
  | "REAL_SAP_EXECUTION";

export interface SapExecutionValidateResponse {
  success: boolean;
  status: string;
  output: string;
  findings: Array<{
    severity: "error" | "warning" | "info";
    line?: number | null;
    column?: number | null;
    rule_code: string;
    message: string;
  }>;
  runtime_ms: number;
  provider_category: SapExecutionCategory;
  is_sandboxed_simulation: boolean;
  is_live_sap_system: boolean;
}

export type SapLearningMode = "GUIDED" | "MISSION";
export type SapAssistanceLevel = "TRAINING" | "GUIDED" | "JOB";

export interface SapModeStateResponse {
  preferred_mode: SapLearningMode;
  last_active_mode: SapLearningMode;
  current_guided_day: number;
  current_mission_id?: string | null;
  assistance_level: SapAssistanceLevel;
}

export interface SapEnterpriseViewResponse {
  slug: string;
  name: string;
  code: string;
  industry: string;
  description_md?: string | null;
  company_state: Record<string, any>;
  landscape_metadata: Record<string, any>;
  state_version: number;
  status: string;
}

export interface SapEnterpriseResetResponse {
  status: string;
  state_version: number;
  message: string;
}

export interface SapMissionSummary {
  id: string;
  slug: string;
  title: string;
  description: string;
  mission_type: string;
  difficulty: number;
  estimated_minutes: number;
  related_days: number[];
  concept_slugs: string[];
  is_unlocked: boolean;
  missing_prerequisites: string[];
  attempt_status: string;
  score?: number | null;
  passed: boolean;
}

export interface SapMissionStep {
  step_id: string;
  title: string;
  step_type: string;
  instruction: string;
  options?: Array<{ id: string; label: string; is_correct?: boolean }>;
  correct_order?: string[];
}

export interface SapMissionDetail {
  id: string;
  slug: string;
  title: string;
  description: string;
  mission_type: string;
  difficulty: number;
  estimated_minutes: number;
  company_context: Record<string, any>;
  enterprise_code: string;
  company_state: Record<string, any>;
  assistance_level: SapAssistanceLevel;
  assistance_rules: {
    allow_hints?: boolean;
    hints?: string[];
    show_prerequisite_primer?: boolean;
  };
  steps: SapMissionStep[];
  related_days: number[];
  concept_slugs: string[];
  current_attempt?: {
    status: string;
    score: number;
    passed: boolean;
    current_step_index: number;
  } | null;
}

export interface SapMissionStepAttemptResponse {
  step_id: string;
  step_success: boolean;
  step_feedback: string;
  mission_completed: boolean;
  mission_passed: boolean;
  current_score: number;
  steps_completed_count: number;
  total_steps: number;
}

export interface SapSkillEvidenceItem {
  id: string;
  concept_slug: string;
  concept_name?: string | null;
  source_type: string;
  source_id: string;
  mode: string;
  assistance_level: string;
  difficulty: number;
  score: number;
  result: string;
  evidence_summary: string;
  details?: Record<string, any>;
  recorded_at?: string | null;
}

export interface SapSkillEvidenceSummaryResponse {
  user_id: string;
  total_evidence_count: number;
  evidences: SapSkillEvidenceItem[];
}

export type SapAssessmentType =
  | "abap_challenge"
  | "analytics_eval"
  | "capstone_multi_concept"
  | "capstone_quiz"
  | "cds_challenge"
  | "concept_quiz"
  | "data_modeling"
  | "decision_matrix"
  | "mcq"
  | "process_ordering"
  | "rap_challenge"
  | "rubric_based"
  | "scenario_decision"
  | "simulation"
  | "technical_audit"
  | "troubleshooting";

export interface SapAssessmentSubmitRequest {
  day_number: number;
  assessment_id: string;
  assessment_type: SapAssessmentType;
  rubric_spec?: Record<string, any>;
  submission_payload?: Record<string, any>;
}

export interface SapAssessmentSubmitResponse {
  submission_id: string;
  passed: boolean;
  score: number;
  feedback: string;
  evaluation_breakdown: Record<string, any>;
  mastery_updated: boolean;
  concept_evaluations: Array<{
    concept_slug: string;
    score: number;
    passed: boolean;
    remediation_capsule?: any;
  }>;
  remediation_required: boolean;
  remediation_capsule?: any;
  all_remediations: any[];
  day_completed?: boolean;
  unlocked_next_day?: boolean;
  current_day?: number;
  next_day_number?: number;
}

// --- Guided Learning 8-Step Lesson Schemas ---

export interface SapLessonStep {
  step_id: string;
  step_type:
    | "learn"
    | "understand"
    | "visual_example"
    | "example"
    | "interactive_practice"
    | "practice"
    | "challenge"
    | "assessment"
    | "mastery_evidence"
    | "evidence"
    | "completion"
    | string;
  title: string;
  content_md?: string | null;
  subtitle?: string | null;
  key_terms?: Array<{ term: string; definition: string }> | null;
  takeaway?: string | null;
  company_context?: Record<string, any> | null;
  component_type?: string | null;
  instruction?: string | null;
  flow_data?: any[] | null;
  scenarios?: any[] | null;
  items?: any[] | null;
  units?: any[] | null;
  entries?: any[] | null;
  records?: any[] | null;
  flow_nodes?: any[] | null;
  scenario_md?: string | null;
  options?: any[] | null;
  concept_slug?: string | null;
  questions?: any[] | null;
  evidence_rule?: string | null;
  summary_md?: string | null;
  recommended_mission?: {
    slug: string;
    title: string;
    description?: string;
    desc?: string;
  } | null;
  is_capstone?: boolean | null;
  assessment_type?: SapAssessmentType | string | null;
  assessment_id?: string | null;
  /** Server-graded Practice step: answer key withheld; submit via completePractice. */
  practice_evidence?: boolean | null;
  multi_concept_eval?: boolean | null;
  concepts_evaluated?: string[] | null;
}

export interface SapLessonDetail {
  day_number: number;
  slug: string;
  title: string;
  subtitle?: string | null;
  estimated_minutes: number;
  atomic_concepts: string[];
  recommended_mission_slug?: string | null;
  steps: SapLessonStep[];
}
