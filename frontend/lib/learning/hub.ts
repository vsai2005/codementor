// Pure course-card logic for the unified Learning Hub (/learning).
//
// Deliberately free of React, fetches and "@/" aliases so it can be unit-tested with
// `node --test`. Only erasable TypeScript syntax and type-only imports are used.
//
// The Start/Continue rules mirror the existing course entry points and must stay in step
// with them:
//   * Python + DSA: /learning/python (roadmap), /learning/day/{n} (lesson)
//   * SAP S/4HANA:  /sap/placement for a brand-new learner (placement comes first),
//                   /sap/learning/day/{n} once placed or started (see app/sap/learning/page.tsx)

import type { SapPlacementProfile, SapProgressResponse } from "../sap/types";

export const PYTHON_TOTAL_DAYS = 160;
export const SAP_TOTAL_DAYS = 100;

export type CourseId = "python-dsa" | "sap-s4hana";
export type CourseStatus = "not_started" | "in_progress" | "completed";

export interface CourseCard {
  id: CourseId;
  title: string;
  tagline: string;
  totalDays: number;
  completedDays: number;
  currentDay: number;
  percent: number;
  status: CourseStatus;
  primaryLabel: string;
  primaryHref: string;
  secondaryLabel: string;
  secondaryHref: string;
}

export interface PythonDayRecordLike {
  lesson_completed?: boolean;
  practice_passed?: boolean;
}

export interface PythonProgressInput {
  currentDay: number;
  completedDays: number[];
  dayRecords?: Record<number, PythonDayRecordLike | undefined>;
}

function clamp(value: number, min: number, max: number): number {
  if (!Number.isFinite(value)) return min;
  return Math.min(max, Math.max(min, Math.trunc(value)));
}

export function percentComplete(completed: number, total: number): number {
  if (total <= 0) return 0;
  return clamp(Math.round((completed / total) * 100), 0, 100);
}

/** Distinct in-range day numbers, so stale or duplicated data cannot inflate progress. */
function countDays(days: number[] | undefined, total: number, exclude?: Set<number>): number {
  const seen = new Set<number>();
  for (const d of days ?? []) {
    if (Number.isInteger(d) && d >= 1 && d <= total && !exclude?.has(d)) seen.add(d);
  }
  return seen.size;
}

export function pythonCourseCard(input: PythonProgressInput): CourseCard {
  const total = PYTHON_TOTAL_DAYS;
  const completed = countDays(input.completedDays, total);
  const anyActivity = Object.values(input.dayRecords ?? {}).some(
    (r) => Boolean(r?.lesson_completed || r?.practice_passed)
  );
  const status: CourseStatus =
    completed >= total ? "completed" : completed > 0 || anyActivity ? "in_progress" : "not_started";
  const currentDay = status === "completed" ? total : clamp(input.currentDay, 1, total);

  const base = {
    id: "python-dsa" as const,
    title: "Python + DSA",
    tagline: "160-day roadmap from Python fundamentals to advanced data structures and algorithms.",
    totalDays: total,
    completedDays: completed,
    currentDay,
    percent: percentComplete(completed, total),
    status,
    secondaryLabel: "View roadmap",
    secondaryHref: "/learning/python",
  };

  if (status === "completed") {
    return { ...base, primaryLabel: "Review course", primaryHref: "/learning/python" };
  }
  if (status === "in_progress") {
    return {
      ...base,
      primaryLabel: `Continue — Day ${currentDay}`,
      primaryHref: `/learning/day/${currentDay}`,
    };
  }
  return { ...base, primaryLabel: "Start course", primaryHref: "/learning/day/1" };
}

export function sapCourseCard(
  progress: SapProgressResponse | null,
  placement: SapPlacementProfile | null
): CourseCard {
  const total = progress?.total_days && progress.total_days > 0 ? progress.total_days : SAP_TOTAL_DAYS;

  const hasPlacement = Boolean(placement && placement.recommended_start_day);
  const hasProgress = Boolean(
    progress &&
      (progress.completed_days.length > 0 ||
        progress.current_day > 1 ||
        Object.values(progress.day_states ?? {}).some(
          (s) => s.lesson_completed || s.practice_completed || s.completed
        ))
  );
  const isNewLearner = !hasPlacement && !hasProgress;

  // Server progress is authoritative for waivers; the placement profile is only a fallback
  // while progress is unavailable. Waived days never count as completed.
  const waived = new Set<number>(progress ? progress.waived_days ?? [] : placement?.waived_days ?? []);
  const completed = countDays(progress?.completed_days, total, waived);

  const rawCurrent = progress?.current_day || placement?.recommended_start_day || 1;
  const status: CourseStatus =
    completed >= total ? "completed" : isNewLearner ? "not_started" : "in_progress";
  const currentDay = clamp(rawCurrent, 1, total);

  const base = {
    id: "sap-s4hana" as const,
    title: "SAP S/4HANA",
    tagline: "100-day guided path through S/4HANA architecture, CDS, ABAP and business processes.",
    totalDays: total,
    completedDays: completed,
    currentDay,
    percent: percentComplete(completed, total),
    status,
    secondaryLabel: "Course overview",
    secondaryHref: "/sap",
  };

  if (status === "completed") {
    return { ...base, primaryLabel: "Review course", primaryHref: "/sap" };
  }
  if (isNewLearner) {
    return { ...base, primaryLabel: "Start course", primaryHref: "/sap/placement" };
  }
  return {
    ...base,
    primaryLabel: `Continue — Day ${currentDay}`,
    primaryHref: `/sap/learning/day/${currentDay}`,
  };
}
