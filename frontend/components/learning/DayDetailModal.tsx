"use client";

import { useEffect } from "react";
import Link from "next/link";
import { CurriculumDay, DayStatus } from "@/lib/curriculum/types";
import { getPracticeForDay } from "@/lib/curriculum/practiceCoverageMap";

interface DayDetailModalProps {
  day: CurriculumDay | null;
  status: DayStatus;
  onClose: () => void;
  onToggleComplete: (dayNumber: number) => void;
}

export function DayDetailModal({
  day,
  status,
  onClose,
  onToggleComplete,
}: DayDetailModalProps) {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [onClose]);

  if (!day) return null;

  const isLocked = status === "locked";
  const isCompleted = status === "completed";
  const isCurrent = status === "current";
  const isPracticeRequired = status === "practice_required";
  const practiceMapping = getPracticeForDay(day.day_number);

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm"
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-day-title"
      onClick={(e) => {
        if (e.target === e.currentTarget) onClose();
      }}
    >
      <div
        className="card w-full max-w-lg max-h-[90vh] overflow-y-auto bg-surface p-6 relative shadow-hard"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-start justify-between gap-3 border-b-2 border-ink/10 pb-3">
          <div>
            <div className="flex items-center gap-2">
              <span className="font-mono text-xs font-bold uppercase text-accent">
                Day {String(day.day_number).padStart(3, "0")}
              </span>
              <span className="text-muted text-xs">•</span>
              <span className="font-mono text-xs text-muted">
                {day.estimated_minutes} min duration
              </span>
              {isPracticeRequired && (
                <span className="rounded border border-amber-600 dark:border-amber-500 bg-amber-500/15 px-1.5 py-0.5 text-[10px] font-mono font-bold uppercase text-amber-700 dark:text-amber-300">
                  Practice Required
                </span>
              )}
              {isCurrent && (
                <span className="rounded border border-accent bg-accent/15 px-1.5 py-0.5 text-[10px] font-mono font-bold uppercase text-accent">
                  Active
                </span>
              )}
              {isCompleted && (
                <span className="rounded border border-accent-2 bg-accent-2/15 px-1.5 py-0.5 text-[10px] font-mono font-bold uppercase text-accent-2">
                  Completed
                </span>
              )}
            </div>
            <h3
              id="modal-day-title"
              className="mt-1 font-display text-xl font-bold text-ink"
            >
              {day.title}
            </h3>
          </div>

          <button
            type="button"
            onClick={onClose}
            className="flex h-8 w-8 min-h-[32px] min-w-[32px] items-center justify-center border-2 border-ink bg-surface text-ink hover:bg-ink hover:text-bg transition-colors"
            aria-label="Close dialog"
          >
            ✕
          </button>
        </div>

        {/* Content */}
        <div className="mt-4 space-y-4">
          <div>
            <span className="label">Topic Description</span>
            <p className="mt-1 font-body text-sm text-ink/80 leading-relaxed">
              {day.description}
            </p>
          </div>

          <div>
            <span className="label">Key Concepts & Focus</span>
            <div className="mt-1.5 flex flex-wrap gap-1.5">
              {day.concepts.map((concept) => (
                <span
                  key={concept}
                  className="rounded border border-ink/30 bg-bg px-2 py-0.5 font-mono text-xs text-ink font-medium"
                >
                  {concept}
                </span>
              ))}
            </div>
          </div>

          {/* Daily Practice Information */}
          {practiceMapping && (
            <div className="border-2 border-black dark:border-border bg-bg/50 p-3.5 text-xs space-y-1.5">
              <div className="flex items-center justify-between font-bold font-mono text-ink">
                <span>🎯 Daily Practice Problem</span>
                <span className="text-[10px] uppercase px-1.5 py-0.5 border border-black dark:border-border bg-surface">
                  Tier {practiceMapping.difficulty_tier}
                </span>
              </div>
              <p className="text-ink font-semibold font-mono text-sm">
                {practiceMapping.primary_problem_slug}
              </p>
              <p className="text-muted leading-relaxed font-body">
                Topic: {practiceMapping.topic_name}. Pass all test cases to complete Day {day.day_number} and unlock Day {day.day_number < 160 ? day.day_number + 1 : 160}.
              </p>
            </div>
          )}
        </div>

        {/* Footer Actions */}
        <div className="mt-6 flex flex-wrap items-center justify-between gap-3 border-t-2 border-ink/10 pt-4">
          <button
            type="button"
            onClick={onClose}
            className="btn text-xs"
          >
            Close
          </button>

          <div className="flex items-center gap-2">
            {!isLocked && (
              <>
                {isPracticeRequired && practiceMapping ? (
                  <>
                    <Link
                      href={`/practice/${practiceMapping.primary_problem_slug}?day=${day.day_number}`}
                      className="btn btn-primary text-xs font-bold flex items-center gap-1 shadow-hard-sm"
                    >
                      <span>Solve Practice Problem →</span>
                    </Link>
                    <Link
                      href={`/learning/day/${day.day_number}`}
                      className="btn text-xs hover:border-ink"
                    >
                      Review Lesson
                    </Link>
                  </>
                ) : (
                  <Link
                    href={`/learning/day/${day.day_number}`}
                    className="btn btn-primary text-xs font-bold flex items-center gap-1 shadow-hard-sm"
                  >
                    <span>{isCompleted ? "Review Lesson →" : "Start Interactive Lesson →"}</span>
                  </Link>
                )}
              </>
            )}
            {isLocked && (
              <span className="font-mono text-xs text-muted">
                Complete Day {day.day_number - 1} to unlock
              </span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
