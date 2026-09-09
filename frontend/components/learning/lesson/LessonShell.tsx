"use client";

import React, { useCallback } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { LessonStep } from "@/lib/lessons/types";
import { useLessonProgress } from "@/lib/lessons/useLessonProgress";
import { StepProgressBar } from "./StepProgressBar";
import { ExplanationCard } from "./ExplanationCard";
import { KnowledgeCheck } from "./KnowledgeCheck";
import { MemoryVisualizer } from "./MemoryVisualizer";
import { DivisionModuloVisualizer } from "./DivisionModuloVisualizer";
import { InteractiveCodeRunner } from "./InteractiveCodeRunner";
import { LessonCompletion } from "./LessonCompletion";

interface LessonShellProps {
  dayNumber: number;
  title: string;
  steps: LessonStep[];
  onMarkDayComplete: (dayNumber: number) => void;
}

export function LessonShell({
  dayNumber,
  title,
  steps,
  onMarkDayComplete,
}: LessonShellProps) {
  const {
    isLoaded,
    progress,
    currentStep,
    currentStepIndex,
    maxUnlockedStepIndex,
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
  } = useLessonProgress({
    dayNumber,
    steps,
    onCompleteDay: () => onMarkDayComplete(dayNumber),
  });

  const router = useRouter();

  const handleFinishDay = useCallback(() => {
    completeDay();
    router.push("/learning");
  }, [completeDay, router]);

  const handleStepChange = useCallback(
    (index: number) => {
      goToStep(index);
      window.scrollTo({ top: 0, behavior: "smooth" });
    },
    [goToStep]
  );

  const handleNextStep = useCallback(() => {
    nextStep();
    window.scrollTo({ top: 0, behavior: "smooth" });
  }, [nextStep]);

  const handlePrevStep = useCallback(() => {
    prevStep();
    window.scrollTo({ top: 0, behavior: "smooth" });
  }, [prevStep]);

  const handleRestart = useCallback(() => {
    if (window.confirm(`Restart this lesson from Step 1? Your completed progress on Day ${dayNumber} will reset to Step 1.`)) {
      resetLesson();
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  }, [dayNumber, resetLesson]);

  if (!isLoaded || !currentStep) {
    return (
      <div className="min-h-screen bg-bg flex items-center justify-center p-4">
        <div className="card p-6 bg-surface text-center">
          <p className="font-mono text-sm text-muted">Loading interactive lesson…</p>
        </div>
      </div>
    );
  }

  const activeStep = currentStep;

  return (
    <div className="min-h-screen bg-bg text-ink flex flex-col pb-24">
      {/* Sticky Top Navigation & Progress Header */}
      <header className="sticky top-0 z-30 border-b-2 border-ink bg-surface shadow-hard-sm">
        <div className="mx-auto max-w-5xl px-3 sm:px-6 py-3 space-y-3">
          {/* Top Row: Meta & Links */}
          <div className="flex items-center justify-between gap-3">
            <div className="flex items-center gap-2 sm:gap-3">
              <Link
                href="/learning"
                className="font-mono text-xs font-bold px-2 py-1 border border-ink/30 bg-bg hover:border-ink hover:bg-ink hover:text-bg transition-colors"
              >
                ← Roadmap
              </Link>
              <span className="font-mono text-xs font-bold text-accent px-2 py-0.5 border border-accent/40 bg-accent/10 rounded">
                Day {String(dayNumber).padStart(3, "0")}
              </span>
              <h1 className="font-display text-sm sm:text-base font-bold text-ink truncate max-w-[200px] sm:max-w-md">
                {title}
              </h1>
            </div>

            <div className="flex items-center gap-2">
              <button
                type="button"
                onClick={handleRestart}
                className="font-mono text-[11px] text-muted hover:text-ink px-2 py-0.5 border border-ink/20 hover:border-ink transition-colors"
                title="Reset lesson progress"
              >
                Restart
              </button>
            </div>
          </div>

          {/* Bottom Row: Step Progress Bar */}
          <StepProgressBar
            steps={steps}
            currentStepIndex={currentStepIndex}
            maxUnlockedStepIndex={maxUnlockedStepIndex}
            onSelectStep={handleStepChange}
          />
        </div>
      </header>

      {/* Main Lesson Viewport */}
      <main className="mx-auto max-w-4xl w-full px-3 sm:px-6 py-8 flex-1">
        {activeStep.type === "explanation" && (
          <ExplanationCard step={activeStep} />
        )}

        {activeStep.type === "checkpoint" && (
          <KnowledgeCheck
            step={activeStep}
            answers={progress.checkpointAnswers}
            onAnswer={recordCheckpointAnswer}
          />
        )}

        {activeStep.type === "visualizer" && (
          activeStep.visualizerKind === "division-modulo" || dayNumber === 2 ? (
            <DivisionModuloVisualizer step={activeStep} />
          ) : (
            <MemoryVisualizer step={activeStep} />
          )
        )}

        {activeStep.type === "practice" && (
          <InteractiveCodeRunner
            step={activeStep}
            dayNumber={dayNumber}
            savedCode={progress.codeDraft}
            isCompleted={progress.practiceCompleted}
            onCodeChange={setCodeDraft}
            onCompletePractice={() => setPracticeCompleted(true)}
          />
        )}

        {activeStep.type === "completion" && (
          <LessonCompletion
            step={activeStep}
            isCompleted={progress.isCompleted}
            onFinishDay={completeDay}
          />
        )}
      </main>

      {/* Sticky Bottom Action Dock */}
      <nav aria-label="Lesson Step Navigation" className="fixed bottom-0 left-0 right-0 z-30 border-t-2 border-ink bg-surface shadow-hard">
        <div className="mx-auto max-w-4xl px-4 py-3 flex items-center justify-between gap-3">
          <button
            type="button"
            disabled={!canGoBack}
            onClick={handlePrevStep}
            className="btn min-h-[44px] text-xs sm:text-sm font-semibold border-2 border-ink shadow-hard-sm disabled:opacity-30 disabled:cursor-not-allowed transition-all focus-visible:ring-2 focus-visible:ring-accent"
          >
            ← Previous
          </button>

          {/* Gating Status Indicator */}
          <div className="text-center px-2 flex-1 min-w-0">
            {isCurrentStepGated ? (
              <span className="font-mono text-xs text-amber-700 dark:text-amber-400 font-bold block truncate">
                {currentStep?.type === "practice" ? (
                  <>
                    <span className="sm:hidden">⚠️ Practice Code Required</span>
                    <span className="hidden sm:inline">⚠️ Run and verify practice code to unlock Next Step</span>
                  </>
                ) : (
                  <>
                    <span className="sm:hidden">⚠️ Checkpoint Required</span>
                    <span className="hidden sm:inline">⚠️ Answer checkpoint correctly to unlock Next Step</span>
                  </>
                )}
              </span>
            ) : currentStepIndex === steps.length - 1 ? (
              <span className="font-mono text-xs text-accent-2 font-bold block truncate">
                🎉 Day {dayNumber} Complete!
              </span>
            ) : (
              <span className="font-mono text-xs text-muted block truncate">
                Step {currentStepIndex + 1} of {steps.length} • {currentStep?.shortLabel}
              </span>
            )}
          </div>

          {currentStepIndex < steps.length - 1 ? (
            <button
              type="button"
              disabled={!canAdvance}
              onClick={handleNextStep}
              className={`btn min-h-[44px] text-xs sm:text-sm font-bold shadow-hard-sm transition-all focus-visible:ring-2 focus-visible:ring-accent ${
                canAdvance
                  ? "btn-primary hover:shadow-hard hover:-translate-y-0.5"
                  : "bg-muted/30 text-muted border-ink/30 cursor-not-allowed opacity-50"
              }`}
            >
              Next Step →
            </button>
          ) : (
            <button
              type="button"
              onClick={handleFinishDay}
              className="btn btn-primary min-h-[44px] text-xs sm:text-sm font-bold shadow-hard-sm hover:shadow-hard focus-visible:ring-2 focus-visible:ring-accent"
            >
              Finish Day {dayNumber} →
            </button>
          )}
        </div>
      </nav>
    </div>
  );
}
