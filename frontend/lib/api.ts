import type {
  CoachResponse,
  CustomRunResponse,
  MisconceptionsResponse,
  MomentumSummary,
  ProblemDetail,
  ProblemPage,
  ProgressResponse,
  ReferenceSolution,
  Review,
  ReviewQueueResponse,
  SubmissionResponse,
  TestsResponse,
  TrendResponse,
  TutorResponse,
  User,
} from "./types";

const BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";
const TOKEN_KEY = "codementor.token";

export class ApiError extends Error {
  readonly status: number;
  readonly retryAfterS: number | null;

  constructor(status: number, message: string, retryAfterS: number | null = null) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.retryAfterS = retryAfterS;
  }
}

export function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return window.localStorage.getItem(TOKEN_KEY);
}

export function setToken(token: string): void {
  window.localStorage.setItem(TOKEN_KEY, token);
}

export function clearToken(): void {
  window.localStorage.removeItem(TOKEN_KEY);
}

interface RequestOptions {
  method?: "GET" | "POST";
  body?: unknown;
  signal?: AbortSignal;
}

async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const token = getToken();
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const response = await fetch(`${BASE}${path}`, {
    method: options.method ?? "GET",
    headers,
    body: options.body === undefined ? undefined : JSON.stringify(options.body),
    signal: options.signal,
  });

  // A 401 on a request that carried a token means the session is genuinely
  // expired/invalid — clear it and say so. A 401 WITHOUT a token (e.g. a login
  // with a wrong password) is not a session problem: fall through so the
  // server's real message ("Incorrect username/email or password.") is shown.
  if (response.status === 401 && token) {
    clearToken();
    throw new ApiError(401, "Your session expired. Please sign in again.");
  }

  if (!response.ok) {
    let detail = `Request failed (${response.status})`;
    let retryAfter: number | null = null;
    try {
      const payload = (await response.json()) as { detail?: string; retry_after_s?: number };
      if (payload.detail) detail = payload.detail;
      if (typeof payload.retry_after_s === "number") retryAfter = payload.retry_after_s;
    } catch {
      /* non-JSON error body; keep the generic message */
    }
    const header = response.headers.get("Retry-After");
    if (retryAfter === null && header) retryAfter = Number.parseInt(header, 10);
    throw new ApiError(response.status, detail, retryAfter);
  }

  return (await response.json()) as T;
}

export const api = {
  register: (body: { username: string; password: string; email?: string; name?: string }) =>
    request<{ access_token: string; user: User }>("/api/auth/register", {
      method: "POST",
      body,
    }),

  login: (body: { identifier: string; password: string }) =>
    request<{ access_token: string; user: User }>("/api/auth/login", {
      method: "POST",
      body,
    }),

  me: () => request<User>("/api/auth/me"),

  listProblems: (params: { topic?: string; tier?: number; page?: number } = {}) => {
    const query = new URLSearchParams();
    if (params.topic) query.set("topic", params.topic);
    if (params.tier !== undefined) query.set("tier", String(params.tier));
    query.set("page", String(params.page ?? 1));
    return request<ProblemPage>(`/api/problems?${query.toString()}`);
  },

  getProblem: (id: string) => request<ProblemDetail>(`/api/problems/${id}`),

  nextProblem: () => request<ProblemDetail>("/api/problems/next"),

  generateProblem: (body: { topic?: string; tier?: number } = {}) =>
    request<ProblemDetail>("/api/problems/generate", { method: "POST", body }),

  referenceSolution: (id: string) =>
    request<ReferenceSolution>(`/api/problems/${id}/reference`),

  runTests: (body: { problem_id: string; language: string; code: string }, signal?: AbortSignal) =>
    request<TestsResponse>("/api/submissions/run", { method: "POST", body, signal }),

  runCustom: (body: { problem_id: string; code: string; args: unknown[] }) =>
    request<CustomRunResponse>("/api/submissions/run-custom", { method: "POST", body }),

  submit: (
    body: { problem_id: string; language: string; code: string; plan?: string },
    signal?: AbortSignal,
  ) => request<SubmissionResponse>("/api/submissions", { method: "POST", body, signal }),

  progress: () => request<ProgressResponse>("/api/progress/topics"),

  trend: (n = 20) => request<TrendResponse>(`/api/progress/trend?n=${n}`),

  reviewQueue: () => request<ReviewQueueResponse>("/api/review/due"),

  misconceptions: () => request<MisconceptionsResponse>("/api/insights/misconceptions"),

  momentum: () => request<MomentumSummary>("/api/momentum"),

  tutor: (body: { message: string; problem_id?: string; code?: string }) =>
    request<TutorResponse>("/api/tutor/chat", { method: "POST", body }),

  coach: (body: {
    problem_id: string;
    code: string;
    review: Review;
    tests: TestsResponse;
    plan?: string;
  }) => request<CoachResponse>("/api/coach/debrief", { method: "POST", body }),
};
