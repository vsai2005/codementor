"use client";

import React from "react";
import Link from "next/link";

interface LockedDayGateProps {
  dayNumber: number;
}

export function LockedDayGate({ dayNumber }: LockedDayGateProps) {
  const prerequisiteDay = Math.max(1, dayNumber - 1);

  return (
    <div className="mx-auto max-w-2xl px-4 py-16 text-center">
      <div className="card p-8 sm:p-12 bg-surface border-2 border-dashed border-ink/40 shadow-hard space-y-6">
        <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full border-2 border-ink bg-bg/80 text-2xl shadow-hard-sm">
          🔒
        </div>

        <div>
          <span className="label text-muted font-mono uppercase tracking-widest text-xs">
            Curriculum Gated
          </span>
          <h1 className="mt-2 font-display text-2xl sm:text-3xl font-bold text-ink">
            Day {dayNumber} is Locked
          </h1>
          <p className="mt-3 font-body text-sm sm:text-base text-ink/80 leading-relaxed max-w-md mx-auto">
            To unlock Day {dayNumber}, you must first complete the lesson and pass the daily coding practice for Day {prerequisiteDay}.
          </p>
        </div>

        <div className="border-2 border-ink/20 bg-bg/40 p-4 text-xs font-mono text-muted max-w-md mx-auto">
          💡 Each day in the 160-day curriculum requires both mastering lesson concepts and passing the daily coding challenge in the Practice Portal.
        </div>

        <div className="flex flex-wrap items-center justify-center gap-3 pt-2">
          <Link
            href={`/learning/day/${prerequisiteDay}`}
            className="btn btn-primary font-bold shadow-hard-sm hover:shadow-hard"
          >
            Go to Day {prerequisiteDay} →
          </Link>
          <Link
            href="/learning"
            className="btn font-semibold text-xs border-2 border-ink shadow-hard-sm hover:shadow-hard"
          >
            ← Back to Roadmap
          </Link>
        </div>
      </div>
    </div>
  );
}
