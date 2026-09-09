"use client";

import Link from "next/link";
import { CurriculumDay, CurriculumSection } from "@/lib/curriculum/types";

interface JourneyHeroProps {
  currentDay: number;
  completedDays: number[];
  currentDayData?: CurriculumDay;
  currentSection?: CurriculumSection;
  onContinue: () => void;
  onReset: () => void;
}

export function JourneyHero({
  currentDay,
  completedDays,
  currentDayData,
  currentSection,
  onContinue,
  onReset,
}: JourneyHeroProps) {
  const totalDays = 160;
  const completedCount = completedDays.length;
  const progressPercent = Math.round((completedCount / totalDays) * 100);

  const handleResetWithConfirm = () => {
    if (
      typeof window !== "undefined" &&
      window.confirm("Are you sure you want to reset your learning roadmap progress back to Day 1?")
    ) {
      onReset();
    }
  };

  return (
    <div className="card p-5 sm:p-7 relative overflow-hidden bg-surface">
      {/* Top Tagline & Meta */}
      <div className="flex flex-wrap items-center justify-between gap-3 border-b-2 border-ink/10 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="label text-accent font-bold">Curriculum Roadmap</span>
            <span className="text-muted text-xs">•</span>
            <span className="font-mono text-xs font-semibold text-muted">
              160-Day Deep Dive
            </span>
          </div>
          <h1 className="mt-1 font-display text-2xl sm:text-3xl font-bold text-ink">
            Python & DSA Learning Path
          </h1>
        </div>

        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={handleResetWithConfirm}
            className="border-2 border-ink/30 bg-surface px-2.5 py-1 font-mono text-xs text-muted hover:border-ink hover:text-ink transition-colors"
            title="Reset roadmap progress"
          >
            Reset Progress
          </button>
        </div>
      </div>

      {/* Main Stats Grid */}
      <div className="mt-5 grid gap-5 lg:grid-cols-[1.4fr_1fr]">
        {/* Current Active Day Spotlight */}
        <div className="border-2 border-ink bg-bg/40 p-4 sm:p-5 shadow-hard-sm">
          <div className="flex items-center justify-between">
            <span className="font-mono text-xs font-bold uppercase tracking-wider text-accent">
              Active Focus • Day {currentDay} of {totalDays}
            </span>
            <span className="rounded border border-accent bg-accent/15 px-2 py-0.5 font-mono text-[11px] font-bold text-accent">
              CURRENT
            </span>
          </div>

          <h2 className="mt-2 font-display text-xl font-bold text-ink">
            {currentDayData ? currentDayData.title : `Day ${currentDay}`}
          </h2>

          <p className="mt-1 font-body text-xs text-muted leading-relaxed">
            {currentDayData?.description ??
              "Continue your sequential mastery of algorithmic thinking and data structures."}
          </p>

          <div className="mt-3 flex flex-wrap items-center gap-2">
            <span className="font-mono text-xs font-semibold text-ink">
              Section: {currentSection?.title ?? "Foundations"}
            </span>
            <span className="text-muted text-xs">•</span>
            <span className="font-mono text-xs text-muted">
              Est. {currentDayData?.estimated_minutes ?? 30} mins
            </span>
          </div>

          <div className="mt-5 flex flex-wrap items-center gap-3">
            {currentDay === 1 ? (
              <Link
                href="/learning/day/1"
                className="btn btn-primary flex items-center gap-2"
              >
                <span>Continue Day 1</span>
                <span className="font-bold">→</span>
              </Link>
            ) : (
              <button
                type="button"
                onClick={onContinue}
                className="btn btn-primary flex items-center gap-2"
              >
                <span>Continue Day {currentDay}</span>
                <span className="font-bold">→</span>
              </button>
            )}
            <button
              type="button"
              onClick={onContinue}
              className="btn text-xs"
            >
              Locate in Roadmap
            </button>
          </div>
        </div>

        {/* Global Progress Metrics */}
        <div className="flex flex-col justify-between border-2 border-ink bg-bg/20 p-4 sm:p-5">
          <div>
            <span className="label">Overall Completion</span>
            <div className="mt-2 flex items-baseline gap-2">
              <span className="font-display text-4xl font-bold text-ink">
                {progressPercent}%
              </span>
              <span className="font-mono text-xs text-muted">
                ({completedCount} of {totalDays} days finished)
              </span>
            </div>

            {/* Micro Progress Bar */}
            <div className="mt-3 h-3 w-full rounded-full border-2 border-ink bg-surface overflow-hidden">
              <div
                className="h-full bg-accent-2 transition-all duration-300"
                style={{ width: `${progressPercent}%` }}
              />
            </div>
          </div>

          <div className="mt-4 pt-3 border-t border-ink/10 grid grid-cols-2 gap-2 text-xs font-mono">
            <div>
              <span className="text-muted block text-[10px] uppercase">Sections</span>
              <span className="font-bold text-ink">14 Total Modules</span>
            </div>
            <div>
              <span className="text-muted block text-[10px] uppercase">Pace</span>
              <span className="font-bold text-ink">1 Day / Session</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
