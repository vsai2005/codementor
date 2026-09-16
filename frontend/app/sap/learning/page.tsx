"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { sapApi } from "@/lib/sap/api";
import type { SapCurriculumOverview, SapProgressResponse } from "@/lib/sap/types";

export default function SapLearningPage() {
  const [curriculum, setCurriculum] = useState<SapCurriculumOverview | null>(null);
  const [progress, setProgress] = useState<SapProgressResponse | null>(null);
  const [activePhase, setActivePhase] = useState<number>(1);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      sapApi.getCurriculum().catch(() => null),
      sapApi.getProgress().catch(() => null),
    ]).then(([curData, progData]) => {
      if (curData) setCurriculum(curData);
      if (progData) {
        setProgress(progData);
        // Find active phase from current day
        const curDay = progData.current_day;
        const matchingPhase = curData?.phases.find(
          (p) => curDay >= p.day_start && curDay <= p.day_end
        );
        if (matchingPhase) setActivePhase(matchingPhase.phase_number);
      }
      setLoading(false);
    });
  }, []);

  const getDayStatusBadge = (dayNumber: number) => {
    const dayState = progress?.day_states[String(dayNumber)];
    if (!dayState) {
      return dayNumber === 1 ? (
        <span className="border border-ink bg-emerald-300 px-2 py-0.5 text-xs font-bold text-ink">
          START HERE
        </span>
      ) : (
        <span className="border border-ink bg-surface-raised px-2 py-0.5 text-xs font-mono text-muted">
          LOCKED
        </span>
      );
    }

    if (dayState.status === "completed") {
      return (
        <span className="border border-ink bg-emerald-400 px-2 py-0.5 text-xs font-bold text-ink">
          ✓ COMPLETED
        </span>
      );
    } else if (dayState.status === "waived_by_placement" || dayState.waived) {
      return (
        <span className="border border-ink bg-sky-200 text-ink px-2 py-0.5 text-xs font-bold uppercase">
          WAIVED BY PLACEMENT
        </span>
      );
    } else if (dayState.status === "current" || dayState.status === "in_progress") {
      return (
        <span className="border border-ink bg-amber-300 px-2 py-0.5 text-xs font-bold text-ink animate-pulse">
          IN PROGRESS
        </span>
      );
    } else if (dayState.status === "available") {
      return (
        <span className="border border-ink bg-cyan-200 px-2 py-0.5 text-xs font-bold text-ink">
          AVAILABLE
        </span>
      );
    }
    return (
      <span className="border border-ink bg-surface-raised px-2 py-0.5 text-xs font-mono text-muted">
        LOCKED
      </span>
    );
  };

  const currentPhaseObj = curriculum?.phases.find((p) => p.phase_number === activePhase);
  const phaseDays = curriculum?.days.filter((d) => d.phase_number === activePhase) || [];

  return (
    <AppShell>
      <div className="mx-auto max-w-[1400px] px-4 py-8">
        {/* Navigation Breadcrumbs & Header */}
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
          <div className="flex items-center gap-3">
            <span className="border-2 border-ink bg-surface px-3 py-1 text-xs font-mono font-bold text-ink">
              Progress: {progress?.completed_days.length || 0} / 100 Days
            </span>
            <Link
              href="/sap/placement"
              className="border-2 border-ink bg-surface-raised px-3 py-1 text-xs font-bold text-ink hover:bg-amber-200"
            >
              Diagnostic Placement
            </Link>
          </div>
        </div>

        {/* Phase Navigator Tabs */}
        <div className="mb-8 flex gap-2 overflow-x-auto border-b-2 border-ink pb-3 scrollbar-thin">
          {(curriculum?.phases || []).map((phase) => {
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
              <span className="font-mono">Days {currentPhaseObj.day_start} to {currentPhaseObj.day_end}</span>
            </div>
            <h2 className="text-xl font-black text-ink">{currentPhaseObj.title}</h2>
            <p className="text-xs sm:text-sm text-muted mt-1">{currentPhaseObj.subtitle}</p>
          </div>
        )}

        {/* Days Grid */}
        {loading ? (
          <div className="p-8 text-center text-sm font-bold text-muted border-2 border-dashed border-ink">
            Loading Phase Milestones…
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
            {phaseDays.map((day) => {
              const dayState = progress?.day_states[String(day.day_number)];
              const isWaived = dayState?.status === "waived_by_placement" || Boolean(dayState?.waived);
              const isLocked = !isWaived && dayState?.status === "locked" && day.day_number !== 1;

              return (
                <div
                  key={day.day_number}
                  className={`border-2 border-ink p-5 flex flex-col justify-between transition-all ${
                    isLocked
                      ? "bg-surface-raised opacity-70"
                      : isWaived
                      ? "bg-sky-50/60 shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[1px] hover:translate-y-[1px]"
                      : "bg-surface shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[1px] hover:translate-y-[1px]"
                  }`}
                >
                  <div>
                    <div className="flex items-center justify-between gap-2 mb-2">
                      <span className="text-xs font-mono font-bold text-muted">
                        DAY {day.day_number}
                      </span>
                      {getDayStatusBadge(day.day_number)}
                    </div>
                    <h3 className="text-base font-black text-ink mb-1.5">{day.title}</h3>
                    <p className="text-xs text-muted mb-3 line-clamp-2">{day.description}</p>

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
                    <Link
                      href={`/sap/learning/day/${day.day_number}`}
                      className={`border border-ink px-3 py-1 text-xs font-bold text-ink transition-all ${
                        isLocked
                          ? "pointer-events-none bg-gray-200 text-gray-500"
                          : isWaived
                          ? "bg-sky-200 hover:bg-sky-300"
                          : "bg-amber-300 hover:bg-amber-400"
                      }`}
                    >
                      {isWaived ? "Review Day →" : "Enter Day →"}
                    </Link>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </AppShell>
  );
}
