"use client";

import React, { memo } from "react";
import Link from "next/link";
import { CurriculumDay, DayStatus } from "@/lib/curriculum/types";

interface DayNodeProps {
  day: CurriculumDay;
  status: DayStatus;
  onSelectDay?: (day: CurriculumDay) => void;
  onToggleComplete?: (dayNumber: number) => void;
}

export const DayNode = memo(function DayNode({
  day,
  status,
  onSelectDay,
  onToggleComplete,
}: DayNodeProps) {
  const isLocked = status === "locked";
  const isCurrent = status === "current";
  const isCompleted = status === "completed";

  const getStatusBadge = () => {
    switch (status) {
      case "completed":
        return (
          <span className="inline-flex items-center gap-1 rounded border border-accent-2 bg-accent-2/10 px-1.5 py-0.5 font-mono text-[10px] font-bold uppercase tracking-wider text-accent-2">
            <svg
              className="h-3 w-3"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={2.5}
            >
              <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
            </svg>
            Done
          </span>
        );
      case "current":
        return (
          <span className="inline-flex items-center gap-1 rounded border border-accent bg-accent/15 px-1.5 py-0.5 font-mono text-[10px] font-bold uppercase tracking-wider text-accent">
            <span className="relative flex h-2 w-2">
              <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-accent opacity-75"></span>
              <span className="relative inline-flex h-2 w-2 rounded-full bg-accent"></span>
            </span>
            Active
          </span>
        );
      case "practice_required":
        return (
          <span className="inline-flex items-center gap-1 rounded border border-amber-600 dark:border-amber-500 bg-amber-500/15 px-1.5 py-0.5 font-mono text-[10px] font-bold uppercase tracking-wider text-amber-700 dark:text-amber-300">
            <span className="relative flex h-2 w-2">
              <span className="relative inline-flex h-2 w-2 rounded-full bg-amber-500"></span>
            </span>
            Practice Req.
          </span>
        );
      case "available":
        return (
          <span className="inline-flex items-center gap-1 rounded border border-ink/30 bg-surface px-1.5 py-0.5 font-mono text-[10px] font-bold uppercase tracking-wider text-ink/70">
            Ready
          </span>
        );
      case "locked":
        return (
          <span className="inline-flex items-center gap-1 rounded border border-ink/20 bg-muted/10 px-1.5 py-0.5 font-mono text-[10px] font-bold uppercase tracking-wider text-muted">
            <svg
              className="h-2.5 w-2.5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={2}
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
              />
            </svg>
            Locked
          </span>
        );
    }
  };

  const containerClasses = () => {
    if (status === "practice_required") {
      return "border-2 border-amber-500 bg-surface shadow-hard-sm ring-2 ring-amber-500/20 hover:-translate-y-0.5 transition-all cursor-pointer";
    }
    if (isCurrent) {
      return "border-2 border-accent bg-surface shadow-hard-accent ring-2 ring-accent/20 hover:-translate-y-0.5 transition-all cursor-pointer";
    }
    if (isCompleted) {
      return "border-2 border-accent-2/70 bg-surface shadow-hard-sm hover:border-accent-2 hover:-translate-y-0.5 transition-all cursor-pointer";
    }
    if (isLocked) {
      return "border-2 border-dashed border-ink/25 bg-surface/40 opacity-70 hover:opacity-90 hover:border-ink/40 transition-all cursor-pointer";
    }
    // Available
    return "border-2 border-ink bg-surface shadow-hard-sm hover:-translate-y-0.5 hover:shadow-hard transition-all cursor-pointer";
  };


  return (
    <div
      id={`day-${day.day_number}`}
      tabIndex={0}
      onClick={() => onSelectDay?.(day)}
      onKeyDown={(e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          onSelectDay?.(day);
        }
      }}
      className={`group relative flex flex-col justify-between p-4 transition-all duration-150 focus:outline-none focus:ring-2 focus:ring-accent ${containerClasses()}`}
      role="button"
      aria-label={`Day ${day.day_number}: ${day.title} - Status: ${status}`}
    >
      {/* Node Header */}
      <div>
        <div className="flex items-center justify-between gap-2">
          <div className="flex items-center gap-1.5">
            <span className="font-mono text-xs font-bold text-ink">
              DAY {String(day.day_number).padStart(3, "0")}
            </span>
            <span className="text-[10px] text-muted">•</span>
            <span className="font-mono text-[10px] text-muted">
              {day.estimated_minutes}m
            </span>
          </div>
          {getStatusBadge()}
        </div>

        {/* Title & Topic */}
        <h4
          className={`mt-2 font-body font-bold text-sm sm:text-base leading-snug transition-colors ${
            isLocked ? "text-muted" : "text-ink group-hover:text-accent"
          }`}
        >
          {day.title}
        </h4>

        <p className="mt-1 line-clamp-2 font-body text-xs text-muted">
          {day.description}
        </p>
      </div>

      {/* Concepts Pills & Actions */}
      <div className="mt-4 pt-3 border-t border-ink/10">
        <div className="flex flex-wrap gap-1">
          {day.concepts.slice(0, 3).map((concept) => (
            <span
              key={concept}
              className={`inline-block rounded border px-1.5 py-0.5 font-mono text-[10px] ${
                isLocked
                  ? "border-ink/10 text-muted/60"
                  : "border-ink/20 bg-bg/50 text-ink/80"
              }`}
            >
              {concept}
            </span>
          ))}
          {day.concepts.length > 3 && (
            <span className="font-mono text-[10px] text-muted">
              +{day.concepts.length - 3}
            </span>
          )}
        </div>

        {/* Action button if actionable */}
        <div className="mt-3 flex items-center justify-between gap-2">
          <span
            className={`text-xs font-semibold font-body inline-flex items-center gap-1 ${
              isLocked
                ? "text-muted hover:text-ink"
                : isCurrent
                ? "text-accent font-bold group-hover:underline"
                : "text-ink group-hover:text-accent"
            }`}
          >
            {isLocked ? (
              <span>Inspect →</span>
            ) : isCurrent ? (
              <Link
                href={`/learning/day/${day.day_number}`}
                onClick={(e) => e.stopPropagation()}
                className="hover:underline flex items-center gap-1"
              >
                <span>Start Day →</span>
              </Link>
            ) : isCompleted ? (
              <Link
                href={`/learning/day/${day.day_number}`}
                onClick={(e) => e.stopPropagation()}
                className="hover:underline flex items-center gap-1"
              >
                <span>Review →</span>
              </Link>
            ) : status === "available" ? (
              <Link
                href={`/learning/day/${day.day_number}`}
                onClick={(e) => e.stopPropagation()}
                className="hover:underline flex items-center gap-1"
              >
                <span>Open Day →</span>
              </Link>
            ) : (
              <span>Inspect →</span>
            )}
          </span>

          {/* Quick toggle completion button */}
          {!isLocked && onToggleComplete && (
            <button
              type="button"
              onClick={(e) => {
                e.stopPropagation();
                onToggleComplete(day.day_number);
              }}
              title={isCompleted ? "Mark as Incomplete" : "Mark as Completed"}
              aria-label={isCompleted ? `Mark Day ${day.day_number} incomplete` : `Mark Day ${day.day_number} complete`}
              className={`rounded border px-2 py-1 font-mono text-[11px] transition-colors ${
                isCompleted
                  ? "border-accent-2/60 text-accent-2 hover:border-accent-2 hover:bg-accent-2/10"
                  : "border-ink/30 text-muted hover:border-ink hover:text-ink"
              }`}
            >
              {isCompleted ? "Unmark" : "Mark done"}
            </button>
          )}
        </div>
      </div>
    </div>
  );
});
