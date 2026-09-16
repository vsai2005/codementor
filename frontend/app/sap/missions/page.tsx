"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { sapApi } from "@/lib/sap/api";
import type {
  SapEnterpriseViewResponse,
  SapMissionSummary,
  SapAssistanceLevel,
  SapSkillEvidenceItem,
} from "@/lib/sap/types";

export default function SapMissionsPage() {
  const [enterprise, setEnterprise] = useState<SapEnterpriseViewResponse | null>(null);
  const [missions, setMissions] = useState<SapMissionSummary[]>([]);
  const [assistanceLevel, setAssistanceLevel] = useState<SapAssistanceLevel>("TRAINING");
  const [evidence, setEvidence] = useState<SapSkillEvidenceItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [resetting, setResetting] = useState(false);
  const [resetMessage, setResetMessage] = useState<string | null>(null);

  const loadData = async () => {
    try {
      const [companyData, missionsData, modesData, evidenceData] = await Promise.all([
        sapApi.getCompany().catch(() => null),
        sapApi.getMissions().catch(() => []),
        sapApi.getModes().catch(() => null),
        sapApi.getSkillEvidence(10).catch(() => ({ evidences: [] })),
      ]);

      if (companyData) setEnterprise(companyData);
      if (missionsData) setMissions(missionsData);
      if (modesData?.assistance_level) setAssistanceLevel(modesData.assistance_level);
      if (evidenceData?.evidences) setEvidence(evidenceData.evidences);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleAssistanceChange = async (level: SapAssistanceLevel) => {
    setAssistanceLevel(level);
    try {
      await sapApi.switchMode({ mode: "MISSION", assistance_level: level });
    } catch (err) {
      console.error("Failed to update assistance level:", err);
    }
  };

  const [confirmReset, setConfirmReset] = useState(false);

  const handleResetEnterprise = async () => {
    setResetting(true);
    setResetMessage(null);
    setConfirmReset(false);
    try {
      const res = await sapApi.resetCompany();
      setResetMessage(res.message || "Enterprise digital twin reset successfully.");
      await loadData();
    } catch (err: any) {
      setResetMessage(err.message || "Failed to reset enterprise state.");
    } finally {
      setResetting(false);
    }
  };

  const getMissionTypeColor = (type: string) => {
    switch (type.toUpperCase()) {
      case "INCIDENT":
        return "bg-rose-200 text-rose-900 border-rose-400";
      case "CONFIGURATION":
        return "bg-amber-200 text-amber-900 border-amber-400";
      case "PROCESS_TASK":
        return "bg-sky-200 text-sky-900 border-sky-400";
      case "CAPSTONE":
        return "bg-purple-200 text-purple-900 border-purple-400";
      default:
        return "bg-gray-200 text-gray-900 border-gray-400";
    }
  };

  if (loading) {
    return (
      <AppShell>
        <div className="mx-auto max-w-[1400px] px-4 py-16 text-center">
          <div className="text-xl font-bold font-mono">Loading Enterprise Mission Control...</div>
        </div>
      </AppShell>
    );
  }

  return (
    <AppShell>
      <div className="mx-auto max-w-[1400px] px-4 py-8">
        {/* Navigation & Mode Switcher Bar */}
        <div className="mb-6 border-3 border-ink bg-surface p-4 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] flex flex-wrap items-center justify-between gap-4">
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-xs font-mono font-bold uppercase text-muted">SAP LEARNING TRACK:</span>
            <div className="flex rounded border border-ink overflow-hidden">
              <Link
                href="/sap/learning"
                className="bg-surface text-ink px-3 py-1 text-xs font-bold hover:bg-surface-raised transition-all"
              >
                Guided Learning (100 Days)
              </Link>
              <span className="bg-amber-300 text-ink px-3 py-1 text-xs font-bold border-l border-ink">
                ✓ Enterprise Mission Mode (Nova Mfg)
              </span>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <Link
              href="/sap"
              className="text-xs font-bold underline hover:text-amber-700"
            >
              ← Back to SAP Hub
            </Link>
          </div>
        </div>

        {/* Header Briefing */}
        <div className="border-4 border-ink bg-surface p-6 sm:p-8 shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] mb-8">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div>
              <div className="inline-block border-2 border-ink bg-amber-300 px-3 py-1 text-xs font-bold uppercase tracking-wider text-ink mb-3">
                Mission Mode Experience
              </div>
              <h1 className="text-3xl font-black tracking-tight sm:text-4xl text-ink">
                Enterprise Mission Control
              </h1>
              <p className="mt-2 max-w-3xl text-sm sm:text-base text-muted">
                Step directly into the shoes of an SAP Solutions Engineer at Nova Manufacturing. Tackle authentic business changes, process breakdowns, and configuration tasks. Every mission feeds your continuous skill evidence graph.
              </p>
            </div>

            {/* Assistance Level Toggle */}
            <div className="border-2 border-ink bg-surface-raised p-4 shadow-[3px_3px_0px_0px_rgba(0,0,0,1)]">
              <div id="assistance-group-label" className="text-xs font-mono font-bold uppercase text-muted mb-2">Assistance Level</div>
              <div role="radiogroup" aria-labelledby="assistance-group-label" className="flex gap-1">
                {(["TRAINING", "GUIDED", "JOB"] as SapAssistanceLevel[]).map((level) => (
                  <button
                    key={level}
                    role="radio"
                    aria-checked={assistanceLevel === level}
                    onClick={() => handleAssistanceChange(level)}
                    className={`px-3 py-1 text-xs font-bold border border-ink transition-all focus-visible:ring-2 focus-visible:ring-ink focus-visible:outline-none ${
                      assistanceLevel === level
                        ? "bg-ink text-surface shadow-[1px_1px_0px_0px_rgba(0,0,0,1)]"
                        : "bg-surface hover:bg-surface-raised text-ink"
                    }`}
                  >
                    {level === "TRAINING" ? "Training" : level === "GUIDED" ? "Guided" : "Job Role"}
                  </button>
                ))}
              </div>
              <p className="mt-2 text-[11px] text-muted max-w-[220px]">
                {assistanceLevel === "TRAINING" && "Full hints, primer links, maximum guidance."}
                {assistanceLevel === "GUIDED" && "Standard enterprise guidance and hints."}
                {assistanceLevel === "JOB" && "Zero hints. Autonomous workplace evaluation."}
              </p>
            </div>
          </div>
        </div>

        {/* Digital Twin Company Context Card */}
        <div className="border-3 border-ink bg-surface p-6 shadow-[5px_5px_0px_0px_rgba(0,0,0,1)] mb-8">
          <div className="flex flex-wrap items-center justify-between border-b-2 border-ink pb-4 mb-4 gap-3">
            <div>
              <div className="flex items-center gap-2">
                <span className="border border-ink bg-sky-200 text-sky-900 px-2 py-0.5 text-xs font-mono font-bold">
                  {enterprise?.code || "NM01"}
                </span>
                <h2 className="text-xl font-black text-ink">{enterprise?.name || "Nova Manufacturing Inc."}</h2>
              </div>
              <p className="text-xs text-muted mt-1">
                {enterprise?.industry || "Industrial Machinery & High-Precision Equipment"} • State Revision v{enterprise?.state_version || 1}
              </p>
            </div>

            <div className="flex items-center gap-2">
              {confirmReset ? (
                <div className="flex items-center gap-2">
                  <span className="text-xs font-bold text-rose-900">Reset to baseline?</span>
                  <button
                    onClick={handleResetEnterprise}
                    disabled={resetting}
                    className="border-2 border-ink bg-rose-600 hover:bg-rose-700 px-3 py-1.5 text-xs font-bold text-white shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] disabled:opacity-50"
                  >
                    {resetting ? "Resetting…" : "Yes, Confirm"}
                  </button>
                  <button
                    onClick={() => setConfirmReset(false)}
                    disabled={resetting}
                    className="border-2 border-ink bg-surface hover:bg-surface-raised px-2.5 py-1.5 text-xs font-bold text-ink"
                  >
                    Cancel
                  </button>
                </div>
              ) : (
                <button
                  onClick={() => setConfirmReset(true)}
                  disabled={resetting}
                  className="border-2 border-ink bg-rose-100 hover:bg-rose-200 px-3 py-1.5 text-xs font-bold text-rose-900 shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] disabled:opacity-50 focus-visible:ring-2 focus-visible:ring-ink"
                >
                  ↺ Reset Enterprise State
                </button>
              )}
            </div>
          </div>

          {resetMessage && (
            <div className="mb-4 p-2 bg-emerald-100 border border-emerald-400 text-emerald-900 text-xs font-semibold">
              {resetMessage}
            </div>
          )}

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs font-mono">
            <div className="border border-ink bg-surface-raised p-2.5">
              <span className="text-muted block text-[10px] uppercase">Org Structure</span>
              <span className="font-bold text-ink">NM01 / PL01 / PL02</span>
            </div>
            <div className="border border-ink bg-surface-raised p-2.5">
              <span className="text-muted block text-[10px] uppercase">Procurement & Sales</span>
              <span className="font-bold text-ink">PO01 / SO01</span>
            </div>
            <div className="border border-ink bg-surface-raised p-2.5">
              <span className="text-muted block text-[10px] uppercase">Architecture</span>
              <span className="font-bold text-ink">S/4HANA Private Cloud</span>
            </div>
            <div className="border border-ink bg-surface-raised p-2.5">
              <span className="text-muted block text-[10px] uppercase">Extensibility Tier</span>
              <span className="font-bold text-ink">Clean Core Tier-1</span>
            </div>
          </div>
        </div>

        {/* Missions Grid */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-black text-ink">Enterprise Mission Briefings</h2>
            <span className="text-xs font-mono text-muted">{missions.length} Missions Available</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {missions.map((m) => (
              <div
                key={m.id}
                className="border-3 border-ink bg-surface p-5 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-center justify-between gap-2 mb-2">
                    <span
                      className={`text-[10px] font-mono font-bold uppercase border px-2 py-0.5 ${getMissionTypeColor(
                        m.mission_type
                      )}`}
                    >
                      {m.mission_type}
                    </span>
                    <span className="text-xs font-mono text-muted">
                      Difficulty: {"★".repeat(m.difficulty)}{"☆".repeat(Math.max(0, 3 - m.difficulty))}
                    </span>
                  </div>

                  <h3 className="text-lg font-black text-ink mb-1">{m.title}</h3>
                  <p className="text-xs text-muted mb-4 line-clamp-2">{m.description}</p>

                  {/* Related Days & Concepts */}
                  <div className="mb-4">
                    <div className="text-[10px] font-mono uppercase text-muted mb-1">Aligned Guided Days:</div>
                    <div className="flex flex-wrap gap-1">
                      {m.related_days.map((day) => (
                        <span key={day} className="border border-ink bg-emerald-100 text-ink px-1.5 py-0.5 text-[10px] font-mono font-bold">
                          Day {day}
                        </span>
                      ))}
                    </div>
                  </div>

                  <div className="mb-4">
                    <div className="text-[10px] font-mono uppercase text-muted mb-1">Tested Concepts:</div>
                    <div className="flex flex-wrap gap-1">
                      {m.concept_slugs.map((c) => (
                        <span key={c} className="border border-ink/40 bg-surface-raised text-ink px-1.5 py-0.5 text-[10px] font-mono">
                          {c}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>

                <div className="border-t-2 border-ink pt-3 flex items-center justify-between">
                  <div className="text-xs font-mono">
                    {m.passed ? (
                      <span className="text-emerald-700 font-bold">✓ Completed ({m.score}%)</span>
                    ) : m.attempt_status === "IN_PROGRESS" ? (
                      <span className="text-amber-700 font-bold">● In Progress</span>
                    ) : (
                      <span className="text-muted">Not Started</span>
                    )}
                  </div>

                  <Link
                    href={`/sap/missions/${m.slug}`}
                    className="border-2 border-ink bg-amber-300 hover:bg-amber-400 px-3 py-1.5 text-xs font-bold text-ink shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] transition-all"
                  >
                    {m.passed ? "Review Mission →" : m.attempt_status === "IN_PROGRESS" ? "Resume →" : "Launch Mission →"}
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Skill Evidence Stream */}
        {evidence.length > 0 && (
          <div className="border-3 border-ink bg-surface p-6 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
            <h2 className="text-lg font-black text-ink mb-3">Unified Skill Evidence Feed</h2>
            <p className="text-xs text-muted mb-4">
              Continuous knowledge trace updating the same DAG concept mastery whether earned through Guided assessments or Mission tasks.
            </p>
            <div className="space-y-2">
              {evidence.slice(0, 5).map((ev) => (
                <div key={ev.id} className="border border-ink bg-surface-raised p-3 flex flex-wrap items-center justify-between gap-2 text-xs">
                  <div className="flex items-center gap-2">
                    <span className="border border-ink bg-amber-200 px-1.5 py-0.5 text-[10px] font-mono font-bold">
                      {ev.mode}
                    </span>
                    <span className="font-mono font-bold text-ink">{ev.concept_slug}</span>
                    <span className="text-muted">— {ev.evidence_summary}</span>
                  </div>
                  <div className="flex items-center gap-3 font-mono">
                    <span className="text-xs font-bold text-emerald-700">{ev.score}%</span>
                    <span className="text-[10px] text-muted">{ev.result}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </AppShell>
  );
}
