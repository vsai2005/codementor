"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { sapApi } from "@/lib/sap/api";
import type { SapCurriculumOverview, SapPlacementProfile } from "@/lib/sap/types";

export default function SapHubPage() {
  const [curriculum, setCurriculum] = useState<SapCurriculumOverview | null>(null);
  const [placement, setPlacement] = useState<SapPlacementProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedPhase, setSelectedPhase] = useState<number>(1);

  const loadData = () => {
    setLoading(true);
    setError(null);

    Promise.allSettled([
      sapApi.getCurriculum(),
      sapApi.getPlacementProfile(),
    ]).then(([curResult, placeResult]) => {
      if (curResult.status === "fulfilled") {
        setCurriculum(curResult.value);
      } else {
        const reason = curResult.reason;
        const msg =
          reason instanceof Error
            ? reason.message
            : "Could not retrieve the SAP curriculum. Verify that backend is running.";
        setError(msg);
      }

      if (placeResult.status === "fulfilled") {
        setPlacement(placeResult.value);
      }
      setLoading(false);
    });
  };

  useEffect(() => {
    loadData();
  }, []);

  const activePhaseObj = curriculum?.phases.find((p) => p.phase_number === selectedPhase);
  const phaseDays = curriculum?.days.filter((d) => d.phase_number === selectedPhase) || [];

  return (
    <AppShell>
      <div className="mx-auto max-w-[1400px] px-4 py-8">
        {/* Learning Mode Switcher Bar */}
        <div className="mb-6 border-3 border-ink bg-surface p-4 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] flex flex-wrap items-center justify-between gap-4">
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-xs font-mono font-bold uppercase text-muted">SAP LEARNING TRACK:</span>
            <div className="flex rounded border border-ink overflow-hidden">
              <Link
                href="/sap/learning"
                className="bg-emerald-400 text-ink px-3 py-1 text-xs font-bold hover:bg-emerald-500 transition-all"
              >
                ✓ Guided Learning (100 Days)
              </Link>
              <Link
                href="/sap/missions"
                className="bg-amber-300 text-ink px-3 py-1 text-xs font-bold hover:bg-amber-400 transition-all border-l border-ink"
              >
                Enterprise Missions (Nova Mfg) →
              </Link>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-xs font-mono font-bold uppercase text-muted">PERSISTENT DIGITAL TWIN:</span>
            <span className="border border-ink bg-sky-100 text-ink px-2.5 py-0.5 text-xs font-bold font-mono">
              Nova Manufacturing (NM01)
            </span>
          </div>
        </div>

        {/* Hero Section */}
        <div className="border-4 border-ink bg-surface p-6 sm:p-8 shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] mb-8">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div>
              <div className="inline-block border-2 border-ink bg-amber-300 px-3 py-1 text-xs font-bold uppercase tracking-wider text-ink mb-3">
                Enterprise S/4HANA & ABAP Cloud Engine
              </div>
              <h1 className="text-3xl font-black tracking-tight sm:text-4xl text-ink">
                100-Day S/4HANA Enterprise Track
              </h1>
              <p className="mt-2 max-w-2xl text-sm sm:text-base text-muted">
                A data-driven, adaptive knowledge graph curriculum spanning ERP Architecture, In-Memory Data Semantics, End-to-End Business Processes, Fiori Elements, Clean Core, RAP, and BTP Integration.
              </p>
            </div>
            <div className="flex flex-wrap gap-3">
              <Link
                href="/sap/learning"
                className="border-2 border-ink bg-emerald-400 px-4 py-2.5 text-sm font-bold text-ink shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[1px] hover:translate-y-[1px] hover:shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] transition-all"
              >
                100-Day Roadmap →
              </Link>
              <Link
                href="/sap/missions"
                className="border-2 border-ink bg-amber-300 px-4 py-2.5 text-sm font-bold text-ink shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[1px] hover:translate-y-[1px] hover:shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] transition-all"
              >
                Enterprise Missions →
              </Link>
              <Link
                href="/sap/placement"
                className="border-2 border-ink bg-cyan-300 px-4 py-2.5 text-sm font-bold text-ink shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[1px] hover:translate-y-[1px] hover:shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] transition-all"
              >
                {placement ? `Placement: ${placement.persona}` : "Diagnostic Placement"}
              </Link>
            </div>
          </div>

          {/* Quick Metrics Bar */}
          <div className="mt-6 grid grid-cols-2 gap-3 border-t-2 border-ink pt-6 sm:grid-cols-4">
            <div className="border-2 border-ink bg-surface-raised p-3">
              <div className="text-xs uppercase text-muted font-bold">Total Milestones</div>
              <div className="text-2xl font-black text-ink">{curriculum?.total_days || 100} Days</div>
            </div>
            <div className="border-2 border-ink bg-surface-raised p-3">
              <div className="text-xs uppercase text-muted font-bold">Curricular Phases</div>
              <div className="text-2xl font-black text-ink">{curriculum?.phases.length || 9} Phases</div>
            </div>
            <div className="border-2 border-ink bg-surface-raised p-3">
              <div className="text-xs uppercase text-muted font-bold">Knowledge Model</div>
              <div className="text-2xl font-black text-ink">Adaptive DAG</div>
            </div>
            <div className="border-2 border-ink bg-surface-raised p-3">
              <div className="text-xs uppercase text-muted font-bold">Architecture Guard</div>
              <div className="text-2xl font-black text-emerald-600">Clean Core</div>
            </div>
          </div>
        </div>

        {/* Error State Banner */}
        {error && (
          <div className="border-3 border-ink bg-red-50 p-6 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] mb-8">
            <div className="flex items-center gap-3 mb-2">
              <span className="text-xl">⚠️</span>
              <h3 className="text-base font-black text-red-900 uppercase">Unable to Load SAP Curriculum</h3>
            </div>
            <p className="text-sm text-red-800 mb-4 font-mono">{error}</p>
            <button
              onClick={() => loadData()}
              className="border-2 border-ink bg-emerald-400 px-4 py-2 text-xs font-bold text-ink shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:bg-emerald-300 transition-all"
            >
              Retry Loading Curriculum
            </button>
          </div>
        )}

        {/* Loading Skeleton */}
        {loading && !error && (
          <div className="border-3 border-dashed border-ink bg-surface p-12 text-center shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] mb-8">
            <div className="inline-block animate-spin text-2xl mb-2">⚙️</div>
            <div className="text-base font-black text-ink">Loading Authoritative SAP Curriculum Manifest…</div>
            <p className="text-xs text-muted mt-1 font-mono">Fetching 9 phases, 100 days, and adaptive DAG nodes from active backend</p>
          </div>
        )}

        {/* Phase Breakdown (All 9 Phases) */}
        {!loading && curriculum && (
          <>
            <div className="mb-6 flex items-center justify-between">
              <h2 className="text-xl font-black text-ink uppercase tracking-wide">
                9 Curriculum Phases (Days 1–100)
              </h2>
              <Link href="/sap/learning" className="text-xs font-bold text-muted hover:text-ink underline">
                Open full learning journey →
              </Link>
            </div>

            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 mb-10">
              {curriculum.phases.map((phase) => {
                const isSelected = phase.phase_number === selectedPhase;
                return (
                  <div
                    key={phase.slug}
                    onClick={() => setSelectedPhase(phase.phase_number)}
                    className={`cursor-pointer flex flex-col justify-between border-3 border-ink p-5 transition-all ${
                      isSelected
                        ? "bg-amber-50 shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] translate-x-[-1px] translate-y-[-1px]"
                        : "bg-surface shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[-1px] hover:translate-y-[-1px]"
                    }`}
                  >
                    <div>
                      <div className="flex items-center justify-between text-xs font-bold uppercase text-muted mb-2">
                        <span>Phase {phase.phase_number}</span>
                        <span className="border border-ink bg-surface-raised px-2 py-0.5 font-mono">
                          Days {phase.day_start}–{phase.day_end}
                        </span>
                      </div>
                      <h3 className="text-lg font-black text-ink mb-1">{phase.title}</h3>
                      <p className="text-xs text-muted mb-4">{phase.subtitle}</p>
                    </div>
                    <div className="border-t border-ink pt-3 flex items-center justify-between">
                      <span className="text-xs font-mono font-bold text-muted">
                        {phase.day_end - phase.day_start + 1} Milestones
                      </span>
                      <span className="text-xs font-bold text-ink underline">
                        {isSelected ? "Viewing Below ↓" : "View Milestones →"}
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Selected Phase 100-Day Milestones Preview */}
            {activePhaseObj && (
              <div className="border-4 border-ink bg-surface p-6 sm:p-8 shadow-[6px_6px_0px_0px_rgba(0,0,0,1)]">
                <div className="flex flex-wrap items-center justify-between gap-4 mb-6 border-b-2 border-ink pb-4">
                  <div>
                    <div className="text-xs font-mono font-bold uppercase text-muted mb-1">
                      PHASE {activePhaseObj.phase_number} OF 9 • DAYS {activePhaseObj.day_start}–{activePhaseObj.day_end}
                    </div>
                    <h3 className="text-2xl font-black text-ink">{activePhaseObj.title}</h3>
                    <p className="text-sm text-muted mt-1">{activePhaseObj.subtitle}</p>
                  </div>
                  <Link
                    href={`/sap/learning`}
                    className="border-2 border-ink bg-emerald-400 px-4 py-2 text-xs font-bold text-ink shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:bg-emerald-300 transition-all"
                  >
                    Start Phase in Guided Learning →
                  </Link>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                  {phaseDays.map((d) => (
                    <Link
                      key={d.day_number}
                      href={`/sap/learning/day/${d.day_number}`}
                      className="group border-2 border-ink bg-surface-raised p-4 shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[-1px] hover:translate-y-[-1px] transition-all flex flex-col justify-between"
                    >
                      <div>
                        <div className="flex items-center justify-between text-xs font-mono font-bold text-muted mb-2">
                          <span>DAY {d.day_number}</span>
                          <span className="border border-ink bg-purple-100 px-1.5 py-0.5 text-[10px] text-ink">
                            {d.env_tier}
                          </span>
                        </div>
                        <h4 className="text-sm font-black text-ink mb-1 group-hover:underline">{d.title}</h4>
                        <p className="text-xs text-muted line-clamp-2 mb-3">{d.description}</p>
                      </div>
                      <div className="border-t border-ink/40 pt-2 flex items-center justify-between text-[11px] font-mono font-bold text-muted">
                        <span>{d.estimated_minutes} min</span>
                        <span className="text-ink font-bold group-hover:underline">Launch →</span>
                      </div>
                    </Link>
                  ))}
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </AppShell>
  );
}

