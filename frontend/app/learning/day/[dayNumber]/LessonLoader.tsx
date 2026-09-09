"use client";

import React, { useEffect, useState } from "react";
import { useJourney, STAGE_MAX_ACCESSIBLE_DAY } from "@/lib/curriculum/useJourney";
import { getLessonPackage } from "@/lib/lessons/loader";
import { DailyLessonPackage } from "@/lib/lessons/types";
import { LessonShell, LockedDayGate } from "@/components/learning/lesson";

interface LessonLoaderProps {
  dayNumber: number;
}

export function LessonLoader({ dayNumber }: LessonLoaderProps) {
  // Safety Gate: If day is beyond STAGE_MAX_ACCESSIBLE_DAY or less than 1, render the locked route guard immediately
  if (dayNumber > STAGE_MAX_ACCESSIBLE_DAY || dayNumber < 1) {
    return <LockedDayGate dayNumber={dayNumber} />;
  }

  const { isLoaded, getDayStatus, markDayComplete } = useJourney();
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
      onMarkDayComplete={markDayComplete}
    />
  );
}
