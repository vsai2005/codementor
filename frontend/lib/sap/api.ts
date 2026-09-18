import type {
  SapCurriculumOverview,
  SapDayDetail,
  SapLessonDetail,
  SapProgressResponse,
  SapPlacementProfile,
  PlacementQuestion,
  SapAssessmentSubmitRequest,
  SapAssessmentSubmitResponse,
  SapCompleteLessonResponse,
  SapCompletePracticeResponse,
} from "./types";

const BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "";

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    ...options,
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      ...(options.headers as Record<string, string>),
    },
  });

  if (!res.ok) {
    let detail = `Request failed with status ${res.status}`;
    try {
      const body = await res.json();
      if (body.detail) detail = body.detail;
    } catch {
      detail = res.statusText || detail;
    }
    const err = new Error(detail);
    (err as any).status = res.status;
    throw err;
  }

  return res.json();
}

export const sapApi = {
  getCurriculum: (): Promise<SapCurriculumOverview> => request<SapCurriculumOverview>("/api/sap/curriculum"),

  getDayDetail: (dayNumber: number): Promise<SapDayDetail> =>
    request<SapDayDetail>(`/api/sap/curriculum/days/${dayNumber}`),

  getLesson: (dayNumber: number): Promise<SapLessonDetail> =>
    request<SapLessonDetail>(`/api/sap/learning/lessons/${dayNumber}`),

  getConceptDetail: (slug: string): Promise<any> =>
    request<any>(`/api/sap/curriculum/concepts/${slug}`),

  getProgress: (): Promise<SapProgressResponse> =>
    request<SapProgressResponse>("/api/sap/learning/progress"),

  completeLesson: (dayNumber: number): Promise<SapCompleteLessonResponse> =>
    request<SapCompleteLessonResponse>("/api/sap/learning/complete-lesson", {
      method: "POST",
      body: JSON.stringify({ day_number: dayNumber }),
    }),

  completePractice: (dayNumber: number): Promise<SapCompletePracticeResponse> =>
    request<SapCompletePracticeResponse>("/api/sap/learning/complete-practice", {
      method: "POST",
      body: JSON.stringify({ day_number: dayNumber }),
    }),

  getPlacementQuestions: (track: "experienced" | "not_sure" = "experienced"): Promise<PlacementQuestion[]> =>
    request<PlacementQuestion[]>(`/api/sap/placement/questions?track=${track}`),

  submitPlacement: (payload: {
    experience_level?: string;
    answers?: Record<string, string>;
    domain_scores?: Record<string, number>;
    experience_years?: number;
    persona_self_select?: string;
  }): Promise<SapPlacementProfile> =>
    request<SapPlacementProfile>("/api/sap/placement/submit", {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  chooseStartDay: (startDay: number): Promise<SapPlacementProfile> =>
    request<SapPlacementProfile>("/api/sap/placement/choose-start", {
      method: "POST",
      body: JSON.stringify({ start_day: startDay }),
    }),

  getPlacementProfile: (): Promise<SapPlacementProfile> =>
    request<SapPlacementProfile>("/api/sap/placement/profile"),

  submitAssessment: (payload: SapAssessmentSubmitRequest): Promise<SapAssessmentSubmitResponse> =>
    request<SapAssessmentSubmitResponse>("/api/sap/assessments/submit", {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  validateExecution: (payload: {
    provider_type: "simulation" | "cds_validation" | "abap_cloud";
    code_or_payload: string;
    context_parameters?: Record<string, any>;
  }): Promise<any> =>
    request<any>("/api/sap/execution/validate", {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  // --- Learning Modes & Assistance ---
  getModes: (): Promise<any> => request<any>("/api/sap/modes"),

  switchMode: (payload: {
    mode: "GUIDED" | "MISSION";
    assistance_level?: "TRAINING" | "GUIDED" | "JOB";
  }): Promise<any> =>
    request<any>("/api/sap/modes", {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  // --- Enterprise Digital Twin ---
  getCompany: (): Promise<any> => request<any>("/api/sap/company"),

  resetCompany: (): Promise<any> =>
    request<any>("/api/sap/company/reset", {
      method: "POST",
    }),

  // --- Enterprise Missions ---
  getMissions: (): Promise<any[]> => request<any[]>("/api/sap/missions"),

  getMissionDetail: (slug: string, assistanceLevel?: string): Promise<any> => {
    const query = assistanceLevel ? `?assistance_level=${encodeURIComponent(assistanceLevel)}` : "";
    return request<any>(`/api/sap/missions/${slug}${query}`);
  },

  startMission: (slug: string, assistanceLevel: string = "TRAINING"): Promise<any> =>
    request<any>(`/api/sap/missions/${slug}/start?assistance_level=${encodeURIComponent(assistanceLevel)}`, {
      method: "POST",
    }),

  attemptMissionStep: (
    slug: string,
    payload: { step_id: string; payload: Record<string, any>; assistance_level?: string }
  ): Promise<any> =>
    request<any>(`/api/sap/missions/${slug}/attempt`, {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  // --- Skill Evidence Graph ---
  getSkillEvidence: (limit: number = 50): Promise<any> =>
    request<any>(`/api/sap/evidence?limit=${limit}`),

  getConceptEvidence: (slug: string): Promise<any[]> =>
    request<any[]>(`/api/sap/evidence/concepts/${slug}`),
};

