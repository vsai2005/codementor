"use client";

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { sapApi } from "@/lib/sap/api";
import type {
  SapCurriculumOverview,
  SapPlacementProfile,
  SapProgressResponse,
} from "@/lib/sap/types";

export default function SapLearningPage() {
  // Authoritative curriculum (9 phases, 100 days)
  const [curriculum, setCurriculum] = useState<SapCurriculumOverview | null>(null);
  const [curriculumLoading, setCurriculumLoading] = useState(true);
  const [curriculumError, setCurriculumError] = useState<string | null>(null);

  // User progression & placement profile (decoupled from public curriculum)
  const [progress, setProgress] = useState<SapProgressResponse | null>(null);
  const [progressLoading, setProgressLoading] = useState(true);
  const [progressError, setProgressError] = useState<string | null>(null);

  const [placement, setPlacement] = useState<SapPlacementProfile | null>(null);
  const [activePhase, setActivePhase] = useState<number>(1);

  // 1. Authoritative curriculum loader — isolated from user session
  const loadCurriculum = useCallback(() => {
    setCurriculumLoading(true);
    setCurriculumError(null);

    sapApi
      .getCurriculum()
      .then((curData) => {
        setCurriculum(curData);
      })
      .catch((err) => {
        const msg =
          err instanceof Error
            ? err.message
            : "Could not retrieve the SAP curriculum. Verify that backend is running.";
        setCurriculumError(msg);
      })
      .finally(() => {
        setCurriculumLoading(false);
      });
  }, []);

  // 2. Authoritative learner progression & placement loader
  const loadUserData = useCallback(() => {
    setProgressLoading(true);
    setProgressError(null);

    Promise.allSettled([
      sapApi.getProgress(),
      sapApi.getPlacementProfile(),
    ]).then(([progResult, placeResult]) => {
      if (progResult.status === "fulfilled") {
        setProgress(progResult.value);
        setProgressError(null);
      } else {
        const reason = progResult.reason;
        // 401 is expected for unauthenticated / guest learners
        if (reason?.status !== 401 && reason?.message !== "Unauthorized") {
          setProgressError(
            reason instanceof Error
              ? reason.message
              : "Could not sync saved progress with server."
          );
        }
      }

      if (placeResult.status === "fulfilled") {
        setPlacement(placeResult.value);
      }

      setProgressLoading(false);
    });
  }, []);

  useEffect(() => {
    loadCurriculum();
    loadUserData();
  }, [loadCurriculum, loadUserData]);

  // Sync active phase with learner's current milestone once loaded
  useEffect(() => {
    if (progress?.current_day && curriculum?.phases) {
      const curDay = progress.current_day;
      const matchingPhase = curriculum.phases.find(
        (p) => curDay >= p.day_start && curDay <= p.day_end
      );
      if (matchingPhase) {
        setActivePhase(matchingPhase.phase_number);
      }
    }
  }, [progress?.current_day, curriculum]);

  // Learner Classification for Permanent Primary CTA
  const hasPlacement = Boolean(placement && placement.recommended_start_day);
  const hasProgress = Boolean(
    progress &&
      (progress.completed_days.length > 0 ||
        progress.current_day > 1 ||
        Object.values(progress.day_states || {}).some(
          (s) => s.lesson_completed || s.practice_completed || s.completed
        ))
  );

  const isNewLearner = !hasPlacement && !hasProgress;
  const currentDay = progress?.current_day || placement?.recommended_start_day || 1;
  const primaryCtaHref = isNewLearner
    ? "/sap/placement"
    : `/sap/learning/day/${currentDay}`;
  const primaryCtaLabel = isNewLearner
    ? "START SAP LEARNING"
    : `CONTINUE LEARNING — DAY ${currentDay}`;

  // Waived days set (must NOT count towards completed days)
  const waivedSet = new Set<number>([
    ...(progress?.waived_days || []),
    ...(placement?.waived_days || []),
  ]);
  const completedDaysCount = (progress?.completed_days || []).filter(
    (d) => !waivedSet.has(d)
  ).length;
  const waivedDaysCount = waivedSet.size;

  // Exact 4-State Meaningful Per-Day CTA Engine
  const getDayDetails = (dayNumber: number) => {
    const dayState = progress?.day_states?.[String(dayNumber)];
    const isWaived = Boolean(
      dayState?.status === "waived_by_placement" ||
        dayState?.waived ||
        waivedSet.has(dayNumber)
    );

    // 1. Waived by placement: visually distinct, reviewed on demand, does NOT count as completed
    if (isWaived) {
      return {
        ctaState: "REVIEW DAY" as const,
        isWaived: true,
        isClickable: true,
        badge: (
          <span className="border border-ink bg-sky-200 text-ink px-2 py-0.5 text-xs font-bold uppercase font-mono">
            WAIVED BY PLACEMENT
          </span>
        ),
        buttonClass:
          "border-2 border-ink bg-sky-200 hover:bg-sky-300 text-ink font-bold shadow-[2px_2px_0px_0px_rgba(0,0,0,1)]",
        cardClass:
          "border-2 border-dashed border-sky-600 bg-sky-50/70 shadow-[3px_3px_0px_0px_rgba(2,132,199,0.35)] hover:translate-x-[1px] hover:translate-y-[1px]",
      };
    }

    // 2. Authoritative Completed: lesson & assessment verified by backend
    if (dayState?.completed) {
      return {
        ctaState: "REVIEW DAY" as const,
        isWaived: false,
        isClickable: true,
        badge: (
          <span className="border border-ink bg-emerald-400 text-ink px-2 py-0.5 text-xs font-bold uppercase">
            ✓ COMPLETED
          </span>
        ),
        buttonClass:
          "border-2 border-ink bg-emerald-300 hover:bg-emerald-400 text-ink font-bold shadow-[2px_2px_0px_0px_rgba(0,0,0,1)]",
        cardClass:
          "border-2 border-ink bg-emerald-50/40 shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[1px] hover:translate-y-[1px]",
      };
    }

    // 3. Active / In Progress: lesson or practice in progress
    const hasStarted = Boolean(
      dayState?.status === "in_progress" ||
        dayState?.lesson_completed ||
        dayState?.practice_completed ||
        (dayNumber === currentDay &&
          (dayState?.lesson_completed || dayState?.practice_completed))
    );

    if (hasStarted) {
      return {
        ctaState: "CONTINUE DAY" as const,
        isWaived: false,
        isClickable: true,
        badge: (
          <span className="border border-ink bg-amber-300 text-ink px-2 py-0.5 text-xs font-bold uppercase animate-pulse">
            IN PROGRESS
          </span>
        ),
        buttonClass:
          "border-2 border-ink bg-amber-300 hover:bg-amber-400 text-ink font-bold shadow-[2px_2px_0px_0px_rgba(0,0,0,1)]",
        cardClass:
          "border-2 border-ink bg-surface shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[1px] hover:translate-y-[1px]",
      };
    }

    // 4. Available first visit: unlocked milestone ready to begin
    const isAvailable = Boolean(
      dayState?.unlocked ||
        dayState?.status === "available" ||
        (dayState?.status === "current" && !hasStarted) ||
        (!progress && dayNumber === 1) ||
        (dayNumber === currentDay && !hasStarted) ||
        (dayNumber === 1 && !dayState?.completed)
    );

    if (isAvailable) {
      return {
        ctaState: "START DAY" as const,
        isWaived: false,
        isClickable: true,
        badge: (
          <span className="border border-ink bg-cyan-200 text-ink px-2 py-0.5 text-xs font-bold uppercase">
            AVAILABLE
          </span>
        ),
        buttonClass:
          "border-2 border-ink bg-cyan-300 hover:bg-cyan-400 text-ink font-bold shadow-[2px_2px_0px_0px_rgba(0,0,0,1)]",
        cardClass:
          "border-2 border-ink bg-surface shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[1px] hover:translate-y-[1px]",
      };
    }

    // 5. Inaccessible: locked milestone
    return {
      ctaState: "LOCKED" as const,
      isWaived: false,
      isClickable: false,
      badge: (
        <span className="border border-ink bg-surface-raised text-muted px-2 py-0.5 text-xs font-mono">
          LOCKED
        </span>
      ),
      buttonClass:
        "border-2 border-ink/40 bg-gray-200 text-gray-400 font-mono font-bold cursor-not-allowed",
      cardClass: "border-2 border-ink/30 bg-surface-raised opacity-60",
    };
  };

  const currentPhaseObj = curriculum?.phases.find((p) => p.phase_number === activePhase);
  const phaseDays =
    curriculum?.days.filter((d) => d.phase_number === activePhase) || [];

  return (
    <AppShell>
      <div className="mx-auto max-w-[1400px] px-4 py-8">
        {/* Navigation Breadcrumbs & Metrics Header */}
        <div className="mb-6 flex flex-wrap items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 text-xs font-mono font-bold text-muted mb-1">
              <Link href="/sap" className="hover:text-ink underline">
                SAP HUB
              </Link>
              <span>/</span>
              <span>100-DAY ROADMAP</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-black text-ink">
              S/4HANA Enterprise Curriculum
            </h1>
          </div>
          <div className="flex flex-wrap items-center gap-3">
            <span className="border-2 border-ink bg-surface px-3 py-1.5 text-xs font-mono font-bold text-ink shadow-[2px_2px_0px_0px_rgba(0,0,0,1)]">
              Progress: {completedDaysCount} / 100 Days
              {waivedDaysCount > 0 && (
                <span className="ml-2 text-sky-700 bg-sky-100 border border-sky-300 px-1.5 py-0.5 text-[10px]">
                  +{waivedDaysCount} waived
                </span>
              )}
            </span>
            <Link
              href="/sap/placement"
              className="border-2 border-ink bg-surface-raised px-3 py-1.5 text-xs font-bold text-ink hover:bg-amber-200 shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] transition-all"
            >
              {placement ? `Placement: ${placement.persona}` : "Diagnostic Placement"}
            </Link>
          </div>
        </div>

        {/* Permanent Primary CTA Banner */}
        <div className="mb-8 border-3 border-ink bg-surface p-5 sm:p-6 shadow-[5px_5px_0px_0px_rgba(0,0,0,1)] flex flex-wrap items-center justify-between gap-4">
          <div>
            <div className="inline-block border border-ink bg-amber-300 px-2.5 py-0.5 text-[11px] font-mono font-bold uppercase tracking-wider text-ink mb-1.5">
              {isNewLearner ? "PRIMARY ACTION • ONBOARDING" : `ACTIVE TRACK • DAY ${currentDay} OF 100`}
            </div>
            <h2 className="text-xl sm:text-2xl font-black text-ink">
              {isNewLearner
                ? "Begin S/4HANA Enterprise Curriculum"
                : `Resume Enterprise Learning — Day ${currentDay}`}
            </h2>
            <p className="text-xs sm:text-sm text-muted mt-1 max-w-2xl">
              {isNewLearner
                ? "Take our diagnostic placement to tailor your starting milestone or start with Day 1."
                : "Continue your verified hands-on journey across enterprise business processes and architecture."}
            </p>
          </div>
          <div>
            <Link
              href={primaryCtaHref}
              className="inline-flex items-center gap-2 border-3 border-ink bg-emerald-400 hover:bg-emerald-300 px-6 py-3 text-sm sm:text-base font-black text-ink shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[2px] hover:translate-y-[2px] hover:shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] transition-all"
            >
              {primaryCtaLabel} →
            </Link>
          </div>
        </div>

        {/* Curriculum Fatal Error Banner (only shown if curriculum itself cannot be loaded) */}
        {curriculumError && !curriculum && (
          <div className="border-3 border-ink bg-red-50 p-6 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] mb-8">
            <div className="flex items-center gap-3 mb-2">
              <span className="text-xl">⚠️</span>
              <h3 className="text-base font-black text-red-900 uppercase">
                Unable to Load SAP Curriculum
              </h3>
            </div>
            <p className="text-sm text-red-800 mb-4 font-mono">{curriculumError}</p>
            <button
              onClick={loadCurriculum}
              className="border-2 border-ink bg-emerald-400 px-4 py-2 text-xs font-bold text-ink shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:bg-emerald-300 transition-all"
            >
              Retry Loading Curriculum
            </button>
          </div>
        )}

        {/* User Progress Non-Blocking Warning Banner with Retry State */}
        {progressError && (
          <div className="mb-6 border-2 border-amber-600 bg-amber-50 p-4 shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] flex flex-wrap items-center justify-between gap-3">
            <div className="flex items-center gap-2 text-sm text-amber-900">
              <span className="text-lg">⚠️</span>
              <span>
                <strong>Progress sync unavailable:</strong> {progressError}. Showing
                authoritative public curriculum.
              </span>
            </div>
            <button
              onClick={loadUserData}
              disabled={progressLoading}
              className="border-2 border-ink bg-amber-300 hover:bg-amber-400 disabled:opacity-60 px-3 py-1.5 text-xs font-bold text-ink shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] transition-all"
            >
              {progressLoading ? "Retrying…" : "Retry Progress Sync"}
            </button>
          </div>
        )}

        {/* Curriculum Loading Skeleton */}
        {curriculumLoading && !curriculum && (
          <div className="border-3 border-dashed border-ink bg-surface p-12 text-center shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] mb-8">
            <div className="inline-block animate-spin text-2xl mb-2">⚙️</div>
            <div className="text-base font-black text-ink">
              Loading 100-Day S/4HANA Curriculum…
            </div>
            <p className="text-xs text-muted mt-1 font-mono">
              Loading all 9 phases and 100 enterprise milestones
            </p>
          </div>
        )}

        {/* Phase Navigator Tabs (All 9 Phases) */}
        {curriculum && (
          <>
            <div className="mb-8 flex gap-2 overflow-x-auto border-b-2 border-ink pb-3 scrollbar-thin">
              {curriculum.phases.map((phase) => {
                const isActive = phase.phase_number === activePhase;
                return (
                  <button
                    key={phase.phase_number}
                    onClick={() => setActivePhase(phase.phase_number)}
                    className={`shrink-0 border-2 border-ink px-4 py-2 text-xs font-bold transition-all ${
                      isActive
                        ? "bg-ink text-surface shadow-[2px_2px_0px_0px_rgba(0,0,0,1)]"
                        : "bg-surface text-ink hover:bg-surface-raised"
                    }`}
                  >
                    P{phase.phase_number}: Days {phase.day_start}–{phase.day_end}
                  </button>
                );
              })}
            </div>

            {/* Active Phase Banner */}
            {currentPhaseObj && (
              <div className="mb-6 border-3 border-ink bg-surface p-5 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
                <div className="flex items-center justify-between text-xs font-bold uppercase text-muted mb-1">
                  <span>Phase {currentPhaseObj.phase_number} of 9</span>
                  <span className="font-mono">
                    Days {currentPhaseObj.day_start} to {currentPhaseObj.day_end}
                  </span>
                </div>
                <h2 className="text-xl font-black text-ink">{currentPhaseObj.title}</h2>
                <p className="text-xs sm:text-sm text-muted mt-1">
                  {currentPhaseObj.subtitle}
                </p>
              </div>
            )}

            {/* Days Grid */}
            <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
              {phaseDays.map((day) => {
                const {
                  ctaState,
                  isClickable,
                  badge,
                  buttonClass,
                  cardClass,
                } = getDayDetails(day.day_number);

                return (
                  <div
                    key={day.day_number}
                    className={`p-5 flex flex-col justify-between transition-all ${cardClass}`}
                  >
                    <div>
                      <div className="flex items-center justify-between gap-2 mb-2">
                        <span className="text-xs font-mono font-bold text-muted">
                          DAY {day.day_number}
                        </span>
                        {badge}
                      </div>
                      <h3 className="text-base font-black text-ink mb-1.5">{day.title}</h3>
                      <p className="text-xs text-muted mb-3 line-clamp-2">
                        {day.description}
                      </p>

                      {/* Environment & Concept Tags */}
                      <div className="flex flex-wrap gap-1.5 mb-4">
                        <span className="border border-ink bg-purple-100 px-2 py-0.5 text-[10px] font-mono font-bold text-ink">
                          env: {day.env_tier}
                        </span>
                        <span className="border border-ink bg-blue-100 px-2 py-0.5 text-[10px] font-mono font-bold text-ink">
                          {day.estimated_minutes}m
                        </span>
                        {day.atomic_concepts.slice(0, 3).map((c) => (
                          <span
                            key={c}
                            className="border border-ink bg-surface-raised px-2 py-0.5 text-[10px] font-mono text-muted"
                          >
                            {c}
                          </span>
                        ))}
                      </div>
                    </div>

                    <div className="border-t border-ink pt-3 flex items-center justify-between">
                      <span className="text-[11px] font-mono font-bold text-muted">
                        {day.practice_types.join(", ") || "Standard"}
                      </span>
                      {isClickable ? (
                        <Link
                          href={`/sap/learning/day/${day.day_number}`}
                          className={`px-3 py-1.5 text-xs transition-all ${buttonClass}`}
                        >
                          {ctaState} →
                        </Link>
                      ) : (
                        <button
                          disabled
                          className={`px-3 py-1.5 text-xs transition-all ${buttonClass}`}
                        >
                          🔒 {ctaState}
                        </button>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </>
        )}
      </div>
    </AppShell>
  );
}
