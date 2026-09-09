"use client";

import React from "react";
import { LessonStep } from "@/lib/lessons/types";

interface StepProgressBarProps {
  steps: LessonStep[];
  currentStepIndex: number;
  maxUnlockedStepIndex: number;
  onSelectStep: (index: number) => void;
}

export function StepProgressBar({
  steps,
  currentStepIndex,
  maxUnlockedStepIndex,
  onSelectStep,
}: StepProgressBarProps) {
  return (
    <div
      role="progressbar"
      aria-label="Lesson Progress"
      aria-valuenow={currentStepIndex + 1}
      aria-valuemin={1}
      aria-valuemax={steps.length}
      className="w-full"
    >
      {/* Desktop & Tablet: Segmented Bar */}
      <div
        className="hidden sm:grid gap-1.5 w-full"
        style={{ gridTemplateColumns: `repeat(${steps.length}, minmax(0, 1fr))` }}
      >
        {steps.map((step, idx) => {
          const isCurrent = idx === currentStepIndex;
          const isPast = idx < currentStepIndex;
          const isUnlocked = idx <= maxUnlockedStepIndex;

          let btnClass = "border-2 text-xs font-mono font-bold py-2 px-1 transition-all text-center truncate flex items-center justify-center gap-1 min-h-[40px] focus-visible:ring-2 focus-visible:ring-accent focus-visible:ring-offset-2 ";
          if (isCurrent) {
            btnClass += "border-accent bg-accent text-white dark:text-bg shadow-hard-sm ring-2 ring-accent/30";
          } else if (isPast) {
            btnClass += "border-ink bg-accent-2/15 text-accent-2 hover:bg-accent-2/25 cursor-pointer";
          } else if (isUnlocked) {
            btnClass += "border-ink bg-surface text-ink hover:bg-bg cursor-pointer";
          } else {
            btnClass += "border-ink/20 bg-muted/10 text-muted cursor-not-allowed opacity-60";
          }

          return (
            <button
              key={step.id}
              type="button"
              disabled={!isUnlocked}
              onClick={() => onSelectStep(idx)}
              title={`Step ${idx + 1}: ${step.title}`}
              className={btnClass}
            >
              {isPast && (
                <svg className="h-3.5 w-3.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={3}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                </svg>
              )}
              {isCurrent && (
                <span className="relative flex h-2 w-2 shrink-0">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-white opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-white"></span>
                </span>
              )}
              {/* On tablet (<1024px), display compact step number to prevent text truncation */}
              <span className="hidden lg:inline truncate">{step.shortLabel}</span>
              <span className="lg:hidden font-mono">{String(idx + 1).padStart(2, "0")}</span>
            </button>
          );
        })}
      </div>

      {/* Mobile: 44px Accessible Touch Targets with Step Dots */}
      <div className="sm:hidden flex items-center justify-between gap-2">
        <div className="flex items-center gap-1.5 flex-1">
          {steps.map((step, idx) => {
            const isCurrent = idx === currentStepIndex;
            const isPast = idx < currentStepIndex;
            const isUnlocked = idx <= maxUnlockedStepIndex;

            let dotClass = "h-3.5 w-full rounded-none border transition-all ";
            if (isCurrent) {
              dotClass += "border-accent bg-accent shadow-hard-sm scale-105";
            } else if (isPast) {
              dotClass += "border-ink bg-accent-2";
            } else if (isUnlocked) {
              dotClass += "border-ink bg-surface";
            } else {
              dotClass += "border-ink/20 bg-muted/20 opacity-50";
            }

            return (
              <button
                key={step.id}
                type="button"
                disabled={!isUnlocked}
                onClick={() => onSelectStep(idx)}
                aria-label={`Step ${idx + 1}: ${step.title}${isCurrent ? " (Current)" : isPast ? " (Completed)" : ""}`}
                className="flex-1 py-3.5 -my-2 flex items-center justify-center focus-visible:ring-2 focus-visible:ring-accent"
              >
                <span className={dotClass} />
              </button>
            );
          })}
        </div>

        <span className="font-mono text-xs font-bold text-ink shrink-0 px-2 py-1 border border-ink/30 bg-surface">
          {currentStepIndex + 1}/{steps.length}
        </span>
      </div>
    </div>
  );
}
