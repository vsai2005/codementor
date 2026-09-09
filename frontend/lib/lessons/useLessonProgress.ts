"use client";

import { useState, useEffect, useCallback, useMemo } from "react";
import { LessonProgress, LessonStep } from "./types";

interface UseLessonProgressOptions {
  dayNumber: number;
  steps: LessonStep[];
  onCompleteDay?: () => void;
}

export function useLessonProgress({
  dayNumber,
  steps,
  onCompleteDay,
}: UseLessonProgressOptions) {
  const storageKey = `codementor.lesson.${dayNumber}.progress`;
  const totalSteps = steps.length;

  const defaultProgress = useMemo<LessonProgress>(
    () => ({
      dayNumber,
      currentStepIndex: 0,
      maxUnlockedStepIndex: 0,
      checkpointAnswers: {},
      codeDraft: "",
      practiceCompleted: false,
      isCompleted: false,
    }),
    [dayNumber]
  );

  const [progress, setProgress] = useState<LessonProgress>(defaultProgress);
  const [isLoaded, setIsLoaded] = useState(false);

  // Hydrate from localStorage after mount
  useEffect(() => {
    try {
      const raw = localStorage.getItem(storageKey);
      if (raw) {
        const parsed = JSON.parse(raw) as Partial<LessonProgress>;
        if (parsed && typeof parsed === "object") {
          const rawCurrent = Number(parsed.currentStepIndex);
          const rawMax = Number(parsed.maxUnlockedStepIndex);

          const currentStepIndex = Number.isInteger(rawCurrent)
            ? Math.max(0, Math.min(totalSteps - 1, rawCurrent))
            : 0;

          const maxUnlockedStepIndex = Number.isInteger(rawMax)
            ? Math.max(currentStepIndex, Math.min(totalSteps - 1, rawMax))
            : currentStepIndex;

          const checkpointAnswers =
            parsed.checkpointAnswers &&
            typeof parsed.checkpointAnswers === "object" &&
            !Array.isArray(parsed.checkpointAnswers)
              ? parsed.checkpointAnswers
              : {};

          setProgress({
            dayNumber,
            currentStepIndex,
            maxUnlockedStepIndex,
            checkpointAnswers,
            codeDraft: typeof parsed.codeDraft === "string" ? parsed.codeDraft : "",
            practiceCompleted: Boolean(parsed.practiceCompleted),
            isCompleted: Boolean(parsed.isCompleted),
            completedAt: parsed.completedAt,
          });
        }
      }
    } catch {
      // Keep defaultProgress on parse error
    } finally {
      setIsLoaded(true);
    }
  }, [dayNumber, storageKey, totalSteps]);

  // Persist updater helper
  const saveProgress = useCallback(
    (updater: (prev: LessonProgress) => LessonProgress) => {
      setProgress((prev) => {
        const next = updater(prev);
        try {
          localStorage.setItem(storageKey, JSON.stringify(next));
        } catch {
          // Gracefully ignore storage quota errors
        }
        return next;
      });
    },
    [storageKey]
  );

  const currentStep: LessonStep = useMemo(
    () => (steps[progress.currentStepIndex] || steps[0])!,
    [steps, progress.currentStepIndex]
  );

  const isCurrentStepGated = useMemo(() => {
    if (!currentStep) return false;

    if (currentStep.type === "checkpoint") {
      // All checkpoint items in this step must be answered correctly
      return currentStep.checkpoints.some((chk) => {
        const answer = progress.checkpointAnswers[chk.id];
        return !answer || !answer.isCorrect;
      });
    }

    if (currentStep.type === "practice") {
      // Must have successfully executed practice task
      return !progress.practiceCompleted;
    }

    return false;
  }, [currentStep, progress.checkpointAnswers, progress.practiceCompleted]);

  const canAdvance = useMemo(() => {
    if (progress.currentStepIndex >= totalSteps - 1) return false;
    return !isCurrentStepGated;
  }, [progress.currentStepIndex, totalSteps, isCurrentStepGated]);

  const canGoBack = useMemo(() => progress.currentStepIndex > 0, [progress.currentStepIndex]);

  const goToStep = useCallback(
    (index: number) => {
      if (index < 0 || index >= totalSteps) return;
      // Allow jumping only to unlocked steps
      if (index <= progress.maxUnlockedStepIndex) {
        saveProgress((prev) => ({
          ...prev,
          currentStepIndex: index,
        }));
      }
    },
    [totalSteps, progress.maxUnlockedStepIndex, saveProgress]
  );

  const nextStep = useCallback(() => {
    if (!canAdvance) return;
    saveProgress((prev) => {
      const nextIndex = Math.min(totalSteps - 1, prev.currentStepIndex + 1);
      const nextMax = Math.max(prev.maxUnlockedStepIndex, nextIndex);
      return {
        ...prev,
        currentStepIndex: nextIndex,
        maxUnlockedStepIndex: nextMax,
      };
    });
  }, [canAdvance, totalSteps, saveProgress]);

  const prevStep = useCallback(() => {
    if (!canGoBack) return;
    saveProgress((prev) => ({
      ...prev,
      currentStepIndex: Math.max(0, prev.currentStepIndex - 1),
    }));
  }, [canGoBack, saveProgress]);

  const recordCheckpointAnswer = useCallback(
    (checkpointId: string, selectedOptionId: string, isCorrect: boolean) => {
      saveProgress((prev) => {
        const nextAnswers = {
          ...prev.checkpointAnswers,
          [checkpointId]: { selectedOptionId, isCorrect },
        };

        // Check if all checkpoints in current step are now correct
        let canUnlockNext = false;
        if (currentStep && currentStep.type === "checkpoint") {
          canUnlockNext = currentStep.checkpoints.every((chk) => {
            if (chk.id === checkpointId) return isCorrect;
            const existing = nextAnswers[chk.id];
            return existing && existing.isCorrect;
          });
        }

        const nextMax = canUnlockNext
          ? Math.max(prev.maxUnlockedStepIndex, prev.currentStepIndex + 1)
          : prev.maxUnlockedStepIndex;

        return {
          ...prev,
          checkpointAnswers: nextAnswers,
          maxUnlockedStepIndex: Math.min(totalSteps - 1, nextMax),
        };
      });
    },
    [currentStep, totalSteps, saveProgress]
  );

  const setCodeDraft = useCallback(
    (code: string) => {
      saveProgress((prev) => ({
        ...prev,
        codeDraft: code,
      }));
    },
    [saveProgress]
  );

  const setPracticeCompleted = useCallback(
    (completed: boolean) => {
      saveProgress((prev) => {
        const nextMax = completed
          ? Math.max(prev.maxUnlockedStepIndex, prev.currentStepIndex + 1)
          : prev.maxUnlockedStepIndex;

        return {
          ...prev,
          practiceCompleted: completed,
          maxUnlockedStepIndex: Math.min(totalSteps - 1, nextMax),
        };
      });
    },
    [totalSteps, saveProgress]
  );

  const completeDay = useCallback(() => {
    saveProgress((prev) => ({
      ...prev,
      isCompleted: true,
      completedAt: Date.now(),
    }));
    if (onCompleteDay) {
      onCompleteDay();
    }
  }, [saveProgress, onCompleteDay]);

  const resetLesson = useCallback(() => {
    saveProgress(() => ({
      dayNumber,
      currentStepIndex: 0,
      maxUnlockedStepIndex: 0,
      checkpointAnswers: {},
      codeDraft: "",
      practiceCompleted: false,
      isCompleted: false,
    }));
  }, [dayNumber, saveProgress]);

  return {
    isLoaded,
    progress,
    currentStep,
    currentStepIndex: progress.currentStepIndex,
    maxUnlockedStepIndex: progress.maxUnlockedStepIndex,
    isCurrentStepGated,
    canAdvance,
    canGoBack,
    goToStep,
    nextStep,
    prevStep,
    recordCheckpointAnswer,
    setCodeDraft,
    setPracticeCompleted,
    completeDay,
    resetLesson,
  };
}
