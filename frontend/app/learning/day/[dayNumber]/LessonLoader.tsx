"use client";

import React, { useEffect, useState } from "react";
import { useJourney, STAGE_MAX_ACCESSIBLE_DAY } from "@/lib/curriculum/useJourney";
import { getLessonPackage } from "@/lib/lessons/loader";
import { DailyLessonPackage } from "@/lib/lessons/types";
import { LessonShell, LockedDayGate } from "@/components/learning/lesson";

import Link from "next/link";

interface LessonLoaderProps {
  dayNumber: number;
}

export function LessonLoader({ dayNumber }: LessonLoaderProps) {
  // Guard: If day is outside the valid curriculum range (1 to STAGE_MAX_ACCESSIBLE_DAY), render 404
  if (dayNumber < 1 || dayNumber > STAGE_MAX_ACCESSIBLE_DAY) {
    return (
      <div className="mx-auto max-w-2xl px-4 py-16 text-center">
        <div className="card p-8 sm:p-12 bg-surface border-2 border-ink shadow-hard space-y-4">
          <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full border-2 border-ink bg-bg text-2xl shadow-hard-sm">
            ❓
          </div>
          <h1 className="font-display text-2xl font-bold text-ink">
            Day {dayNumber} Does Not Exist
          </h1>
          <p className="font-body text-sm text-ink/80 max-w-md mx-auto">
            The Python &amp; DSA curriculum spans Days 1 through {STAGE_MAX_ACCESSIBLE_DAY}.
          </p>
          <div className="pt-2">
            <Link href="/learning" className="btn btn-primary font-bold shadow-hard-sm hover:shadow-hard">
              ← Back to 160-Day Roadmap
            </Link>
          </div>
        </div>
      </div>
    );
  }

  const { isLoaded, getDayStatus, markLessonComplete } = useJourney();
  const [pkg, setPkg] = useState<DailyLessonPackage | null>(null);
  const [loadingPkg, setLoadingPkg] = useState(true);

  useEffect(() => {
    let active = true;
    setLoadingPkg(true);
    getLessonPackage(dayNumber)
      .then((loaded) => {
        if (active) {
          setPkg(loaded);
          setLoadingPkg(false);
        }
      })
      .catch((err) => {
        console.error("Failed to load lesson package", err);
        if (active) {
          setPkg(null);
          setLoadingPkg(false);
        }
      });
    return () => {
      active = false;
    };
  }, [dayNumber]);

  if (!isLoaded || loadingPkg) {
    return (
      <div className="min-h-screen bg-bg flex items-center justify-center p-4">
        <div className="card p-6 bg-surface text-center shadow-hard">
          <div className="animate-pulse space-y-3">
            <div className="h-4 bg-ink/10 rounded w-48 mx-auto" />
            <p className="font-mono text-xs text-muted">Loading Day {dayNumber} interactive lesson…</p>
          </div>
        </div>
      </div>
    );
  }

  const status = getDayStatus(dayNumber);

  // Safety Gate: If day is locked or beyond STAGE_MAX_ACCESSIBLE_DAY, render the locked route guard
  if (status === "locked" || dayNumber > STAGE_MAX_ACCESSIBLE_DAY || !pkg) {
    return <LockedDayGate dayNumber={dayNumber} />;
  }

  return (
    <LessonShell
      dayNumber={pkg.dayNumber}
      title={pkg.title}
      steps={pkg.steps}
      onLessonComplete={markLessonComplete}
    />
  );
}
