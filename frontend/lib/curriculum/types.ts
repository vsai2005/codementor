export type DayStatus = "completed" | "current" | "practice_required" | "available" | "locked";

export interface CurriculumDay {
  day_number: number;
  title: string;
  topic_name: string;
  section_id: string;
  estimated_minutes: number;
  description: string;
  concepts: string[];
}

export interface CurriculumSection {
  id: string;
  section_number: number;
  title: string;
  tagline: string;
  day_start: number;
  day_end: number;
  icon: string;
  days: CurriculumDay[];
}

export interface DayProgressRecord {
  day_number: number;
  lesson_completed: boolean;
  lesson_completed_at?: string | null;
  practice_passed: boolean;
  practice_passed_at?: string | null;
  completed: boolean;
  completed_at?: string | null;
  unlocked?: boolean;
  status?: DayStatus;
  practice_problem_slug?: string;
}

export interface LearningJourneyProgress {
  current_day: number;
  completed_days: number[];
  day_records?: Record<number, DayProgressRecord>;
  last_activity_timestamp: number;
}

