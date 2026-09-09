"use client";

import { useEffect, useState, useMemo, useCallback } from "react";
import { CURRICULUM_SECTIONS, TOTAL_CURRICULUM_DAYS } from "./curriculumData";
import { DayStatus, LearningJourneyProgress, DayProgressRecord, CurriculumDay, CurriculumSection } from "./types";
import { api, getToken } from "@/lib/api";

const STORAGE_KEY = "codementor.learning.progress";

// 160-Day Full Curriculum: All 160 days are accessible
export const STAGE_MAX_ACCESSIBLE_DAY = 160;

const DEFAULT_PROGRESS: LearningJourneyProgress = {
  current_day: 1,
  completed_days: [],
  day_records: {},
  last_activity_timestamp: Date.now(),
};

export function useJourney() {
  const [progress, setProgress] = useState<LearningJourneyProgress>(DEFAULT_PROGRESS);
  const [isLoaded, setIsLoaded] = useState(false);

  const saveProgress = useCallback((updater: (prev: LearningJourneyProgress) => LearningJourneyProgress) => {
    setProgress((prev) => {
      const nextProgress = updater(prev);
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(nextProgress));
      } catch {
        // Gracefully handle storage quota or privacy mode errors
      }
      return nextProgress;
    });
  }, []);

  // Initialize and sanitize from localStorage after client hydration, then sync with server
  useEffect(() => {
    let currentLocal = DEFAULT_PROGRESS;
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) {
        const parsed = JSON.parse(stored) as Partial<LearningJourneyProgress>;
        if (parsed && typeof parsed === "object") {
          const rawDay = Number(parsed.current_day);
          const current_day = Number.isInteger(rawDay)
            ? Math.max(1, Math.min(STAGE_MAX_ACCESSIBLE_DAY, rawDay))
            : 1;

          const completed_days = Array.isArray(parsed.completed_days)
            ? Array.from(
                new Set(
                  parsed.completed_days
                    .map(Number)
                    .filter((n) => Number.isInteger(n) && n >= 1 && n <= TOTAL_CURRICULUM_DAYS)
                )
              ).sort((a, b) => a - b)
            : [];

          currentLocal = {
            current_day,
            completed_days,
            day_records: parsed.day_records || {},
            last_activity_timestamp: Number(parsed.last_activity_timestamp) || Date.now(),
          };
          setProgress(currentLocal);
        }
      }
    } catch {
      // Fallback to default progress on read error
    } finally {
      setIsLoaded(true);
    }

    // Authoritative server synchronization when authenticated
    const token = getToken();
    if (token) {
      api.learningProgress()
        .then((res) => {
          if (res && Array.isArray(res.completed_days)) {
            saveProgress((prev) => {
              const mergedCompleted = Array.from(
                new Set([...prev.completed_days, ...res.completed_days])
              ).sort((a, b) => a - b);
              const serverCurrent = res.current_day || 1;
              const nextCurrent = Math.max(prev.current_day, serverCurrent);
              const dayRecords: Record<number, DayProgressRecord> = { ...(prev.day_records || {}) };
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
                current_day: nextCurrent,
                completed_days: mergedCompleted,
                day_records: dayRecords,
                last_activity_timestamp: Date.now(),
              };
            });
          }
        })
        .catch(() => {
          // If offline or network issue, rely gracefully on localStorage cache
        });
    }
  }, [saveProgress]);

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
        records[dayNumber] = {
          ...existing,
          lesson_completed: true,
          lesson_completed_at: existing.lesson_completed_at || new Date().toISOString(),
        };
        return {
          ...prev,
          day_records: records,
          last_activity_timestamp: Date.now(),
        };
      });

      try {
        const token = getToken();
        if (token) {
          await api.completeLesson(dayNumber);
        }
      } catch {
        // Continue gracefully
      }
    },
    [saveProgress]
  );

  const markDayComplete = useCallback(
    (dayNumber: number) => {
      saveProgress((prev) => {
        const nextSet = new Set(prev.completed_days);
        nextSet.add(dayNumber);
        const candidateNext = Math.max(prev.current_day, dayNumber + 1);
        const nextDay = Math.min(STAGE_MAX_ACCESSIBLE_DAY, candidateNext);
        const records = { ...(prev.day_records || {}) };
        const existing = records[dayNumber] || {
          day_number: dayNumber,
          lesson_completed: true,
          practice_passed: false,
          completed: false,
        };
        records[dayNumber] = {
          ...existing,
          lesson_completed: true,
          practice_passed: true,
          completed: true,
          completed_at: existing.completed_at || new Date().toISOString(),
        };
        return {
          current_day: nextDay,
          completed_days: Array.from(nextSet).sort((a, b) => a - b),
          day_records: records,
          last_activity_timestamp: Date.now(),
        };
      });
    },
    [saveProgress]
  );

  // Cross-component and cross-tab listener for practice submission pass events
  useEffect(() => {
    const handleDayEvent = (e: Event) => {
      const customEvent = e as CustomEvent<{ day_number: number }>;
      if (customEvent.detail?.day_number) {
        markDayComplete(customEvent.detail.day_number);
      }
    };
    window.addEventListener("codementor:day-completed", handleDayEvent);
    return () => {
      window.removeEventListener("codementor:day-completed", handleDayEvent);
    };
  }, [markDayComplete]);

  const unmarkDayComplete = useCallback(
    (dayNumber: number) => {
      saveProgress((prev) => {
        const nextCompleted = prev.completed_days.filter((d) => d !== dayNumber);
        const nextDay = Math.min(prev.current_day, dayNumber);
        const records = { ...(prev.day_records || {}) };
        if (records[dayNumber]) {
          records[dayNumber] = {
            ...records[dayNumber],
            practice_passed: false,
            completed: false,
            completed_at: null,
          };
        }
        return {
          current_day: nextDay,
          completed_days: nextCompleted,
          day_records: records,
          last_activity_timestamp: Date.now(),
        };
      });
    },
    [saveProgress]
  );

  const toggleDayComplete = useCallback(
    (dayNumber: number) => {
      if (completedSet.has(dayNumber)) {
        unmarkDayComplete(dayNumber);
      } else {
        markDayComplete(dayNumber);
      }
    },
    [completedSet, markDayComplete, unmarkDayComplete]
  );

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
    markDayComplete,
    unmarkDayComplete,
    toggleDayComplete,
    setCurrentDay,
    resetProgress,
    currentDayData,
    currentSection,
    stats,
  };
}
