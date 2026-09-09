"use client";

import Link from "next/link";
import { useJourney } from "@/lib/curriculum/useJourney";

export function LearningRoadmapCard() {
  const { currentDay, completedDays, currentDayData, currentSection } = useJourney();

  const totalDays = 160;
  const completedCount = completedDays.length;
  const progressPercent = Math.round((completedCount / totalDays) * 100);

  return (
    <div className="card p-5 bg-surface">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <span className="label text-accent font-bold">160-Day Curriculum</span>
            <span className="text-muted text-xs">•</span>
            <span className="font-mono text-xs text-muted">
              Section {currentSection?.section_number ?? 1}: {currentSection?.title ?? "Foundations"}
            </span>
          </div>

          <h2 className="font-display text-xl font-bold text-ink">
            Day {currentDay}: {currentDayData?.title ?? "Foundations"}
          </h2>

          <p className="max-w-xl font-body text-xs text-muted leading-relaxed">
            {currentDayData?.description ?? "Follow the structured step-by-step engineering roadmap."}
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <Link
            href="/learning"
            className="btn btn-primary flex items-center gap-1.5 text-xs"
          >
            <span>Continue Learning</span>
            <span className="font-bold">→</span>
          </Link>
        </div>
      </div>

      {/* Progress Bar & Sub-metrics */}
      <div className="mt-4 pt-3 border-t border-ink/10 flex flex-wrap items-center justify-between gap-3 text-xs font-mono">
        <div className="flex items-center gap-2">
          <span className="text-ink font-bold">{completedCount} of {totalDays} days finished</span>
          <span className="text-muted">({progressPercent}%)</span>
        </div>

        <div className="h-2 w-32 sm:w-48 rounded-full border border-ink/20 bg-bg overflow-hidden">
          <div
            className="h-full bg-accent-2 transition-all duration-300"
            style={{ width: `${progressPercent}%` }}
          />
        </div>
      </div>
    </div>
  );
}
