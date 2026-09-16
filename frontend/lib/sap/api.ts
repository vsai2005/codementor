import type {
  SapCurriculumOverview,
  SapDayDetail,
  SapLessonDetail,
  SapProgressResponse,
  SapPlacementProfile,
} from "./types";

const BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";
const TOKEN_KEY = "codementor.token";

function authHeaders(): Record<string, string> {
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (typeof window !== "undefined") {
    const token = window.localStorage.getItem(TOKEN_KEY);
    if (token) headers["Authorization"] = `Bearer ${token}`;
  }
  return headers;
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    ...options,
    headers: { ...authHeaders(), ...(options.headers as Record<string, string>) },
  });

  if (!res.ok) {
    const body = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(body.detail || `Request failed with status ${res.status}`);
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

  completeLesson: (dayNumber: number): Promise<any> =>
    request<any>("/api/sap/learning/complete-lesson", {
      method: "POST",
      body: JSON.stringify({ day_number: dayNumber }),
    }),

  submitPlacement: (payload: {
    domain_scores: Record<string, number>;
    experience_years?: number;
    persona_self_select?: string;
  }): Promise<SapPlacementProfile> =>
    request<SapPlacementProfile>("/api/sap/placement/submit", {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  getPlacementProfile: (): Promise<SapPlacementProfile> =>
    request<SapPlacementProfile>("/api/sap/placement/profile"),

  submitAssessment: (payload: {
    day_number: number;
    assessment_id: string;
    assessment_type: string;
    rubric_spec?: Record<string, any>;
    submission_payload?: Record<string, any>;
  }): Promise<any> =>
    request<any>("/api/sap/assessments/submit", {
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

