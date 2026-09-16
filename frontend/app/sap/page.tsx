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

  useEffect(() => {
    Promise.all([
      sapApi.getCurriculum().catch(() => null),
      sapApi.getPlacementProfile().catch(() => null),
    ]).then(([curData, placeData]) => {
      if (curData) setCurriculum(curData);
      if (placeData) setPlacement(placeData);
      setLoading(false);
    });
  }, []);

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
              <div className="text-2xl font-black text-ink">100 Days</div>
            </div>
            <div className="border-2 border-ink bg-surface-raised p-3">
              <div className="text-xs uppercase text-muted font-bold">Curricular Phases</div>
              <div className="text-2xl font-black text-ink">9 Phases</div>
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

        {/* Phase Breakdown */}
        <div className="mb-6 flex items-center justify-between">
          <h2 className="text-xl font-black text-ink uppercase tracking-wide">
            Curriculum Phases (Days 1–100)
          </h2>
          <Link href="/sap/learning" className="text-xs font-bold text-muted hover:text-ink underline">
            View full syllabus & DAG
          </Link>
        </div>

        {loading ? (
          <div className="p-8 text-center text-sm font-bold text-muted border-2 border-dashed border-ink">
            Loading authoritative SAP curriculum manifest…
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {(curriculum?.phases || []).map((phase) => (
              <div
                key={phase.slug}
                className="flex flex-col justify-between border-3 border-ink bg-surface p-5 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]"
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
                  <Link
                    href={`/sap/learning#phase-${phase.phase_number}`}
                    className="text-xs font-bold text-ink underline hover:text-indigo-600"
                  >
                    Explore Days →
                  </Link>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </AppShell>
  );
}
