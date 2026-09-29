"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";

import { useJourney } from "@/lib/curriculum/useJourney";
import {
  pythonCourseCard,
  sapCourseCard,
  type CourseCard,
  type CourseStatus,
} from "@/lib/learning/hub";
import { sapApi } from "@/lib/sap/api";
import type { SapPlacementProfile, SapProgressResponse } from "@/lib/sap/types";

const STATUS_LABEL: Record<CourseStatus, string> = {
  not_started: "Not started",
  in_progress: "In progress",
  completed: "Completed",
};

function CourseCardView({
  card,
  eyebrow,
  currentLine,
  ready,
}: {
  card: CourseCard;
  eyebrow: string;
  currentLine: string | null;
  ready: boolean;
}) {
  const testId = `course-card-${card.id}`;
  return (
    <article className="card flex flex-col p-5" data-testid={testId} aria-labelledby={`${testId}-title`}>
      <div className="flex items-center justify-between gap-2">
        <span className="label text-accent">{eyebrow}</span>
        {ready ? (
          <span
            className="border border-ink px-1.5 py-0.5 font-mono text-[10px] font-bold uppercase"
            data-testid={`${testId}-status`}
          >
            {STATUS_LABEL[card.status]}
          </span>
        ) : null}
      </div>

      <h2 id={`${testId}-title`} className="mt-2 font-display text-2xl font-bold text-ink">
        {card.title}
      </h2>
      <p className="mt-1 font-body text-sm leading-relaxed text-muted">{card.tagline}</p>

      <div className="mt-4 min-h-[3.5rem]">
        {ready ? (
          <>
            <div className="flex flex-wrap items-baseline justify-between gap-2 font-mono text-xs">
              <span className="font-bold text-ink" data-testid={`${testId}-progress`}>
                {card.completedDays} of {card.totalDays} days completed
              </span>
              <span className="text-muted">{card.percent}%</span>
            </div>
            <div
              className="mt-2 h-3 w-full overflow-hidden rounded-full border-2 border-ink bg-surface"
              role="progressbar"
              aria-label={`${card.title} progress`}
              aria-valuemin={0}
              aria-valuemax={100}
              aria-valuenow={card.percent}
            >
              <div
                className="h-full bg-accent-2 transition-all duration-300"
                style={{ width: `${card.percent}%` }}
              />
            </div>
            {currentLine ? (
              <p className="mt-2 font-body text-xs text-muted" data-testid={`${testId}-current`}>
                {currentLine}
              </p>
            ) : null}
          </>
        ) : (
          <p className="font-body text-xs text-muted">Loading your progress…</p>
        )}
      </div>

      <div className="mt-5 flex flex-wrap items-center gap-2">
        {ready ? (
          <Link
            href={card.primaryHref}
            className="btn btn-primary flex items-center gap-1.5 text-xs"
            data-testid={`${testId}-primary`}
          >
            <span>{card.primaryLabel}</span>
            <span className="font-bold">→</span>
          </Link>
        ) : (
          <span className="btn btn-primary cursor-not-allowed text-xs opacity-50" aria-disabled="true">
            Loading…
          </span>
        )}
        <Link href={card.secondaryHref} className="btn text-xs" data-testid={`${testId}-secondary`}>
          {card.secondaryLabel}
        </Link>
      </div>
    </article>
  );
}

export function LearningHub() {
  const {
    progress,
    currentDay,
    completedDays,
    currentDayData,
    isLoaded,
    serverSynced,
  } = useJourney();
  // Wait for the server sync too, so a signed-in learner never sees "Start" flip to "Continue".
  const pythonLoaded = isLoaded && serverSynced;

  const [sapProgress, setSapProgress] = useState<SapProgressResponse | null>(null);
  const [sapPlacement, setSapPlacement] = useState<SapPlacementProfile | null>(null);
  const [sapLoaded, setSapLoaded] = useState(false);

  useEffect(() => {
    let cancelled = false;
    // Signed-out visitors and failed requests both leave these null, which the card shows
    // as a not-started course with a Start action.
    Promise.allSettled([sapApi.getProgress(), sapApi.getPlacementProfile()]).then(
      ([progressResult, placementResult]) => {
        if (cancelled) return;
        if (progressResult.status === "fulfilled") setSapProgress(progressResult.value);
        if (placementResult.status === "fulfilled") setSapPlacement(placementResult.value);
        setSapLoaded(true);
      }
    );
    return () => {
      cancelled = true;
    };
  }, []);

  const pythonCard = useMemo(
    () =>
      pythonCourseCard({
        currentDay,
        completedDays,
        dayRecords: progress.day_records,
      }),
    [currentDay, completedDays, progress.day_records]
  );
  const sapCard = useMemo(() => sapCourseCard(sapProgress, sapPlacement), [sapProgress, sapPlacement]);

  const pythonCurrentLine =
    pythonCard.status === "in_progress" && currentDayData
      ? `Current: Day ${pythonCard.currentDay} — ${currentDayData.title}`
      : pythonCard.status === "in_progress"
        ? `Current: Day ${pythonCard.currentDay}`
        : null;
  const sapCurrentLine =
    sapCard.status === "in_progress" ? `Current: Day ${sapCard.currentDay} of ${sapCard.totalDays}` : null;

  return (
    <div className="mx-auto max-w-[1100px] space-y-6 px-3 py-8 sm:px-4">
      <header>
        <p className="label">Learning Hub</p>
        <h1 className="mt-1 font-display text-3xl font-bold text-ink">Choose your course</h1>
        <p className="mt-2 max-w-2xl font-body text-sm leading-relaxed text-muted">
          Two structured, day-by-day courses. Pick up where you left off, or start a new one.
        </p>
      </header>

      <div className="grid gap-5 md:grid-cols-2">
        <CourseCardView
          card={pythonCard}
          eyebrow="160-day course"
          currentLine={pythonCurrentLine}
          ready={pythonLoaded}
        />
        <CourseCardView card={sapCard} eyebrow="100-day course" currentLine={sapCurrentLine} ready={sapLoaded} />
      </div>
    </div>
  );
}
