"use client";

import { useEffect, useState, useMemo, useCallback, useRef } from "react";
import { CURRICULUM_SECTIONS, TOTAL_CURRICULUM_DAYS } from "./curriculumData";
import { DayStatus, LearningJourneyProgress, DayProgressRecord, CurriculumDay, CurriculumSection } from "./types";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth";

const STORAGE_KEY = "codementor.learning.progress";

// 160-Day Full Curriculum: All 160 days are accessible
export const STAGE_MAX_ACCESSIBLE_DAY = 160;

const DEFAULT_PROGRESS: LearningJourneyProgress = {
  current_day: 1,
  completed_days: [],
  day_records: {},
  last_activity_timestamp: Date.now(),
};

/**
 * Validates and sanitizes cached local progress.
 * For a day to be considered completed in guest/offline mode:
 * BOTH lesson_completed and practice_passed must be strictly true.
 * Days unlock strictly in sequential order (Day 1 -> Day 2 -> ...).
 */
function sanitizeLocalProgress(parsed: Partial<LearningJourneyProgress>): LearningJourneyProgress {
  const day_records: Record<number, DayProgressRecord> = parsed.day_records || {};

  // Find consecutive completed days starting from Day 1
  const validCompleted: number[] = [];
  for (let d = 1; d <= TOTAL_CURRICULUM_DAYS; d++) {
    const rec = day_records[d];
    if (rec && rec.lesson_completed && rec.practice_passed) {
      validCompleted.push(d);
    } else {
      // Progression chain breaks at the first incomplete day
      break;
    }
  }

  const current_day = Math.min(
    STAGE_MAX_ACCESSIBLE_DAY,
    validCompleted.length + 1
  );

  return {
    current_day,
    completed_days: validCompleted,
    day_records,
    last_activity_timestamp: Number(parsed.last_activity_timestamp) || Date.now(),
  };
}

export function useJourney() {
  const { user } = useAuth();
  const [progress, setProgress] = useState<LearningJourneyProgress>(DEFAULT_PROGRESS);
  const [isLoaded, setIsLoaded] = useState(false);
  const progressRef = useRef(progress);
  const inFlightPracticeSyncRef = useRef<Set<number>>(new Set());

  useEffect(() => {
    progressRef.current = progress;
  }, [progress]);

  const saveProgress = useCallback((updater: (prev: LearningJourneyProgress) => LearningJourneyProgress) => {
    setProgress((prev) => {
      const nextProgress = updater(prev);
      progressRef.current = nextProgress;
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(nextProgress));
      } catch {
        // Gracefully handle storage quota or privacy mode errors
      }
      return nextProgress;
    });
  }, []);

  // Server synchronization: authoritative server state REPLACES local state (no union, no Math.max)
  const syncWithServer = useCallback(async () => {
    try {
      const res = await api.learningProgress();
      if (res && Array.isArray(res.completed_days)) {
        saveProgress(() => {
          const serverCompleted = [...res.completed_days].sort((a: number, b: number) => a - b);
          const serverCurrent = res.current_day || 1;
          const dayRecords: Record<number, DayProgressRecord> = {};
          if (res.day_states) {
            for (const [dStr, st] of Object.entries(res.day_states)) {
              const d = Number(dStr);
              dayRecords[d] = {
                day_number: st.day_number,
                lesson_completed: st.lesson_completed,
                lesson_completed_at: st.lesson_completed_at,
                practice_passed: st.practice_passed,
                practice_passed_at: st.practice_passed_at,
                completed: st.completed,
                completed_at: st.completed_at,
                unlocked: st.unlocked,
                status: st.status as DayStatus,
                practice_problem_slug: st.practice_problem_slug,
              };
            }
          }
          return {
            current_day: serverCurrent,
            completed_days: serverCompleted,
            day_records: dayRecords,
            last_activity_timestamp: Date.now(),
          };
        });
      }
    } catch {
      // Unauthenticated or offline: preserve sanitized local state
    }
  }, [saveProgress]);

  // Initialize and sanitize from localStorage on mount, then sync with server
  useEffect(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) {
        const parsed = JSON.parse(stored) as Partial<LearningJourneyProgress>;
        if (parsed && typeof parsed === "object") {
          const sanitized = sanitizeLocalProgress(parsed);
          setProgress(sanitized);
        }
      }
    } catch {
      // Fallback to default progress on read error
    } finally {
      setIsLoaded(true);
    }

    syncWithServer();
  }, [syncWithServer]);

  // Re-sync authoritative server state whenever user login changes
  useEffect(() => {
    if (user) {
      syncWithServer();
    }
  }, [user, syncWithServer]);

  const completedSet = useMemo(() => new Set(progress.completed_days), [progress.completed_days]);

  const getDayStatus = useCallback(
    (dayNumber: number): DayStatus => {
      if (completedSet.has(dayNumber)) {
        return "completed";
      }
      // Safety gate: Days beyond the stage ceiling or invalid days are strictly locked
      if (dayNumber > STAGE_MAX_ACCESSIBLE_DAY || dayNumber < 1) {
        return "locked";
      }
      const record = progress.day_records?.[dayNumber];
      if (record?.lesson_completed && !record?.practice_passed) {
        return "practice_required";
      }
      if (dayNumber === progress.current_day) {
        return "current";
      }
      if (dayNumber < progress.current_day) {
        return "available";
      }
      return "locked";
    },
    [completedSet, progress.current_day, progress.day_records]
  );

  /**
   * Marks a lesson complete.
   * Completing a lesson strictly sets lesson_completed = true.
   * It NEVER sets practice_passed = true or completed = true on its own.
   * The day only becomes completed if practice_passed is already true.
   */
  const markLessonComplete = useCallback(
    async (dayNumber: number) => {
      saveProgress((prev) => {
        const records = { ...(prev.day_records || {}) };
        const existing = records[dayNumber] || {
          day_number: dayNumber,
          lesson_completed: false,
          practice_passed: false,
          completed: false,
        };
        const lesson_completed = true;
        const practice_passed = Boolean(existing.practice_passed);
        const completed = lesson_completed && practice_passed;

        records[dayNumber] = {
          ...existing,
          lesson_completed: true,
          lesson_completed_at: existing.lesson_completed_at || new Date().toISOString(),
          practice_passed,
          completed,
          completed_at: completed ? (existing.completed_at || new Date().toISOString()) : null,
        };

        const nextCompletedSet = new Set(prev.completed_days);
        if (completed) {
          nextCompletedSet.add(dayNumber);
        } else {
          nextCompletedSet.delete(dayNumber);
        }

        // Recalculate current day sequentially
        let nextCurrent = 1;
        while (nextCompletedSet.has(nextCurrent) && nextCurrent < TOTAL_CURRICULUM_DAYS) {
          nextCurrent++;
        }

        return {
          ...prev,
          current_day: nextCurrent,
          completed_days: Array.from(nextCompletedSet).sort((a, b) => a - b),
          day_records: records,
          last_activity_timestamp: Date.now(),
        };
      });

      try {
        await api.completeLesson(dayNumber);
        await syncWithServer();
      } catch {
        // Offline or unauthenticated guest fallback
      }
    },
    [saveProgress, syncWithServer]
  );

  /**
   * Records that practice was passed.
   * Practice submission is the single canonical pathway that sets practice_passed = true.
   * The day only becomes completed if lesson_completed is already true.
   */
  const recordPracticePassed = useCallback(
    async (dayNumber: number) => {
      // Synchronous idempotency check: if practice is already passed or sync is in-flight, exit immediately
      if (
        inFlightPracticeSyncRef.current.has(dayNumber) ||
        progressRef.current.day_records?.[dayNumber]?.practice_passed
      ) {
        return;
      }

      inFlightPracticeSyncRef.current.add(dayNumber);

      try {
        saveProgress((prev) => {
          const records = { ...(prev.day_records || {}) };
          const existing = records[dayNumber] || {
            day_number: dayNumber,
            lesson_completed: false,
            practice_passed: false,
            completed: false,
          };

          if (existing.practice_passed) {
            return prev;
          }

          const lesson_completed = Boolean(existing.lesson_completed);
          const practice_passed = true;
          const completed = lesson_completed && practice_passed;

          records[dayNumber] = {
            ...existing,
            lesson_completed,
            practice_passed: true,
            practice_passed_at: existing.practice_passed_at || new Date().toISOString(),
            completed,
            completed_at: completed ? (existing.completed_at || new Date().toISOString()) : null,
          };

          const nextCompletedSet = new Set(prev.completed_days);
          if (completed) {
            nextCompletedSet.add(dayNumber);
          } else {
            nextCompletedSet.delete(dayNumber);
          }

          let nextCurrent = 1;
          while (nextCompletedSet.has(nextCurrent) && nextCurrent < TOTAL_CURRICULUM_DAYS) {
            nextCurrent++;
          }

          return {
            ...prev,
            current_day: nextCurrent,
            completed_days: Array.from(nextCompletedSet).sort((a, b) => a - b),
            day_records: records,
            last_activity_timestamp: Date.now(),
          };
        });

        await syncWithServer();
      } catch {
        // Offline or unauthenticated guest fallback
      } finally {
        inFlightPracticeSyncRef.current.delete(dayNumber);
      }
    },
    [saveProgress, syncWithServer]
  );

  // Cross-component and cross-tab listener for practice submission pass events
  useEffect(() => {
    const handlePracticeEvent = (e: Event) => {
      const customEvent = e as CustomEvent<{ day_number: number }>;
      if (customEvent.detail?.day_number) {
        recordPracticePassed(customEvent.detail.day_number);
      }
    };
    window.addEventListener("codementor:practice-passed", handlePracticeEvent);
    return () => {
      window.removeEventListener("codementor:practice-passed", handlePracticeEvent);
    };
  }, [recordPracticePassed]);

  const setCurrentDay = useCallback(
    (dayNumber: number) => {
      if (dayNumber >= 1 && dayNumber <= TOTAL_CURRICULUM_DAYS) {
        saveProgress((prev) => ({
          ...prev,
          current_day: dayNumber,
          last_activity_timestamp: Date.now(),
        }));
      }
    },
    [saveProgress]
  );

  const resetProgress = useCallback(() => {
    saveProgress(() => ({
      current_day: 1,
      completed_days: [],
      day_records: {},
      last_activity_timestamp: Date.now(),
    }));
  }, [saveProgress]);

  // Find current day metadata and section
  const currentDayData = useMemo<CurriculumDay | undefined>(() => {
    for (const section of CURRICULUM_SECTIONS) {
      const found = section.days.find((d) => d.day_number === progress.current_day);
      if (found) return found;
    }
    return CURRICULUM_SECTIONS[0]?.days[0];
  }, [progress.current_day]);

  const currentSection = useMemo<CurriculumSection | undefined>(() => {
    return (
      CURRICULUM_SECTIONS.find(
        (sec) => progress.current_day >= sec.day_start && progress.current_day <= sec.day_end
      ) ?? CURRICULUM_SECTIONS[0]
    );
  }, [progress.current_day]);

  const stats = useMemo(() => {
    const completedCount = progress.completed_days.length;
    const percentage = Math.round((completedCount / TOTAL_CURRICULUM_DAYS) * 100);
    return {
      completedCount,
      totalDays: TOTAL_CURRICULUM_DAYS,
      percentage,
    };
  }, [progress.completed_days]);

  return {
    progress,
    currentDay: progress.current_day,
    completedDays: progress.completed_days,
    isLoaded,
    getDayStatus,
    markLessonComplete,
    recordPracticePassed,
    setCurrentDay,
    resetProgress,
    currentDayData,
    currentSection,
    stats,
  };
}
