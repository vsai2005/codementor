/** Mirrors the backend Pydantic models in app/schemas/api.py. */

export type Severity = "minor" | "major" | "critical";
export type Mastery = "weak" | "learning" | "strong";

export interface User {
  id: string;
  username: string;
  email: string | null;
  name: string;
  avatar_url: string | null;
}

export interface Topic {
  id: string;
  slug: string;
  name: string;
}

export interface ProblemSummary {
  id: string;
  slug: string;
  title: string;
  difficulty_tier: number;
  topic: Topic;
  generated?: boolean;
}

export interface ConceptLesson {
  pattern: string;
  summary: string;
  when_to_use: string;
  worked_example: string;
}

export interface GenerationMeta {
  topic: string;
  tier: number;
  validated_cases: number;
}

export interface ProblemDetail extends ProblemSummary {
  statement_md: string;
  constraints_md: string;
  optimal_time: string;
  optimal_space: string;
  entry_point: string;
  starter_code: Record<string, string>;
  concept?: ConceptLesson | null;
  generation?: GenerationMeta;
}

export interface ProblemPage {
  items: ProblemSummary[];
  page: number;
  page_size: number;
  total: number;
}

export interface TestCaseResult {
  index: number;
  passed: boolean;
  status: string;
  runtime_ms: number;
  stdout: string;
  stderr: string;
}

export interface TestsResponse {
  passed: number;
  total: number;
  all_passed: boolean;
  results: TestCaseResult[];
}

export interface Scores {
  correctness: number;
  time_complexity: number;
  space_complexity: number;
  readability: number;
  edge_cases: number;
}

export interface Complexity {
  time: string;
  space: string;
}

export interface Issue {
  severity: Severity;
  title: string;
  detail: string;
  line: number | null;
}

export interface Review {
  overall_score: number;
  scores: Scores;
  detected_complexity: Complexity;
  optimal_complexity: Complexity;
  summary: string;
  issues: Issue[];
  improvement_hint: string;
  weak_topics: string[];
  review_degraded: boolean;
}

export interface DifficultyChange {
  from: number;
  to: number;
  rolling_score: number;
  banner: string;
}

export interface ReviewSchedule {
  interval_days: number;
  due_at: string;
  reps: number;
  ease: number;
}

export interface MisconceptionHit {
  tag: string;
  label: string;
  tip: string;
  count: number;
}

export interface Badge {
  id: string;
  emoji: string;
  label: string;
  desc: string;
  earned?: boolean;
  earned_at?: string | null;
}

export interface MomentumDelta {
  xp_earned: number;
  total_xp: number;
  level: number;
  level_progress: number;
  level_span: number;
  streak: number;
  solved_today: number;
  daily_goal: number;
  new_badges: Badge[];
}

export interface SubmissionResponse {
  submission_id: string;
  tests: TestsResponse;
  review: Review;
  difficulty: DifficultyChange;
  review_schedule?: ReviewSchedule;
  misconception?: MisconceptionHit | null;
  momentum?: MomentumDelta;
}

export interface TopicProgress {
  topic: Topic;
  current_tier: number;
  attempts: number;
  avg_score: number;
  mastery: Mastery;
  last_practiced_at: string | null;
}

export interface ProgressResponse {
  topics: TopicProgress[];
}

export interface TrendPoint {
  submission_id: string;
  overall_score: number;
  created_at: string;
}

export interface TrendResponse {
  points: TrendPoint[];
}

export interface MemoryNote {
  id: string;
  content: string;
  similarity: number;
}

export interface TutorResponse {
  reply: string;
  retrieved_notes: MemoryNote[];
}

export interface CoachResponse {
  message: string;
}

export interface ReviewQueueItem extends ProblemSummary {
  due_at: string | null;
  last_score: number | null;
  reps: number;
  due_in_days: number;
}

export interface ReviewQueueResponse {
  due: ReviewQueueItem[];
  upcoming: ReviewQueueItem[];
  due_count: number;
  tracked_count: number;
}

export interface Misconception {
  tag: string;
  label: string;
  tip: string;
  count: number;
  last_at: string | null;
  problems: string[];
}

export interface MisconceptionsResponse {
  items: Misconception[];
  total: number;
}

export interface MomentumSummary {
  xp: number;
  level: number;
  level_progress: number;
  level_span: number;
  streak: number;
  longest_streak: number;
  daily_goal: number;
  solved_today: number;
  solved_count: number;
  badges: Badge[];
  earned_count: number;
}

export interface CustomRunResponse {
  status: string;
  returned: unknown;
  stdout: string;
  stderr: string;
  runtime_ms: number;
}

export interface ReferenceSolution {
  available: boolean;
  language: string;
  code: string;
  commentary: string;
}

export const TIER_LABELS: Record<number, string> = {
  1: "Easy",
  2: "Easy-Medium",
  3: "Medium",
  4: "Medium-Hard",
  5: "Hard",
};
