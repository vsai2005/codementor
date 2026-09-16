"use client";

import React, { useState } from "react";

export interface TransportStep {
  system_id: string;
  system_name: string;
  client: string;
  role: string;
  status: "LOCKED" | "CURRENT" | "COMPLETED" | "BLOCKED";
  actions: string[];
}

interface LandscapeFlowProps {
  title?: string;
  instruction?: string;
}

const DEFAULT_STEPS: TransportStep[] = [
  {
    system_id: "DEV",
    system_name: "Development System",
    client: "100 (Customizing) / 110 (Workbench)",
    role: "Where developers and functional consultants build and unit test changes.",
    status: "COMPLETED",
    actions: ["TR Created (DEVK900142)", "Tasks Released", "Transport Request Released"],
  },
  {
    system_id: "QAS",
    system_name: "Quality Assurance System",
    client: "200 (Integration Testing)",
    role: "Where end-to-end integration and user acceptance testing (UAT) occurs.",
    status: "CURRENT",
    actions: ["Import TR into QAS (STMS)", "Execute Cross-Module Test in Plant PL01", "Sign off Business Approval"],
  },
  {
    system_id: "PRD",
    system_name: "Production System",
    client: "300 (Live Operations)",
    role: "The live operating system. Zero direct configuration or code changes permitted.",
    status: "LOCKED",
    actions: ["Pre-Cutover Validation", "Emergency Maintenance Window Import", "Post-Import Verification"],
  },
];

export function LandscapeFlow({
  title = "3-System Landscape & Transport Management (DEV → QAS → PRD)",
  instruction = "Follow a Change Request for Nova Manufacturing across the enterprise landscape. Ensure governance rules, transport sequence integrity, and strict production protection.",
}: LandscapeFlowProps) {
  const [activeSystemId, setActiveSystemId] = useState<string>("DEV");
  const [transportsReleased, setTransportsReleased] = useState<boolean>(true);
  const [qasImported, setQasImported] = useState<boolean>(false);
  const [prdImported, setPrdImported] = useState<boolean>(false);
  const [errorNotice, setErrorNotice] = useState<string | null>(null);

  const handleImportQas = () => {
    if (!transportsReleased) {
      setErrorNotice("Cannot import to QAS: Transport Request has not been released in DEV.");
      return;
    }
    setErrorNotice(null);
    setQasImported(true);
    setActiveSystemId("QAS");
  };

  const handleImportPrd = () => {
    if (!qasImported) {
      setErrorNotice("Governance Violation: Transport cannot be imported into PRD before successful verification in QAS.");
      return;
    }
    setErrorNotice(null);
    setPrdImported(true);
    setActiveSystemId("PRD");
  };

  const handleReset = () => {
    setTransportsReleased(true);
    setQasImported(false);
    setPrdImported(false);
    setErrorNotice(null);
    setActiveSystemId("DEV");
  };

  const currentStep = DEFAULT_STEPS.find((s) => s.system_id === activeSystemId) || DEFAULT_STEPS[0]!;

  return (
    <div className="border-3 border-ink bg-surface p-5 shadow-hard">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-2 mb-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="border border-ink bg-amber-200 text-amber-950 px-2 py-0.5 text-xs font-mono font-bold">
              [SIMULATION MODEL] LANDSCAPE GOVERNANCE
            </span>
            <h3 className="text-base font-black text-ink">{title}</h3>
          </div>
          <p className="text-xs text-muted mt-1 leading-relaxed">{instruction}</p>
        </div>

        <div className="text-xs font-mono font-bold bg-surface-raised border border-ink p-1.5">
          TR: <span className="text-purple-700">DEVK900142</span> (Nova Plant PL02 SLoc Config)
        </div>
      </div>

      {/* Visual Pipeline Bar */}
      <div className="grid grid-cols-3 gap-2 mb-5">
        {DEFAULT_STEPS.map((step) => {
          const isSelected = step.system_id === activeSystemId;
          const isDone =
            (step.system_id === "DEV" && transportsReleased) ||
            (step.system_id === "QAS" && qasImported) ||
            (step.system_id === "PRD" && prdImported);

          return (
            <button
              key={step.system_id}
              type="button"
              aria-current={isSelected ? "step" : undefined}
              onClick={() => setActiveSystemId(step.system_id)}
              className={`p-3 text-left border-2 border-ink transition-all focus-visible:ring-2 focus-visible:ring-ink ${
                isSelected
                  ? "bg-amber-100 shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] border-amber-900"
                  : isDone
                  ? "bg-emerald-50 text-emerald-950"
                  : "bg-surface hover:bg-surface-raised"
              }`}
            >
              <div className="flex items-center justify-between font-mono text-xs font-bold mb-1">
                <span>{step.system_id}</span>
                <span
                  className={`text-[10px] px-1 py-0.5 border ${
                    isDone
                      ? "bg-emerald-200 text-emerald-900 border-emerald-500"
                      : "bg-muted/20 text-muted border-ink/20"
                  }`}
                >
                  {isDone ? "VERIFIED" : "PENDING"}
                </span>
              </div>
              <div className="text-xs font-black text-ink">{step.system_name}</div>
              <div className="text-[10px] text-muted font-mono mt-1">Client: {step.client}</div>
            </button>
          );
        })}
      </div>

      {/* System Details & Pipeline Action */}
      <div className="border-2 border-ink bg-surface-raised p-4 mb-5">
        <div className="flex flex-wrap items-center justify-between border-b border-ink/30 pb-3 mb-3 gap-2">
          <div>
            <span className="text-xs font-mono font-bold uppercase text-ink">
              Selected System: {currentStep.system_id} ({currentStep.system_name})
            </span>
            <p className="text-xs text-muted mt-0.5">{currentStep.role}</p>
          </div>

          {/* Action Trigger Buttons */}
          <div className="flex items-center gap-2">
            {activeSystemId === "QAS" && !qasImported && (
              <button
                type="button"
                onClick={handleImportQas}
                className="border-2 border-ink bg-sky-400 px-3 py-1.5 text-xs font-black uppercase text-ink shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:bg-sky-300"
              >
                Simulate QAS Import (STMS) →
              </button>
            )}

            {activeSystemId === "PRD" && !prdImported && (
              <button
                type="button"
                onClick={handleImportPrd}
                className="border-2 border-ink bg-emerald-400 px-3 py-1.5 text-xs font-black uppercase text-ink shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:bg-emerald-300"
              >
                Simulate PRD Deployment (STMS) 🛡️
              </button>
            )}

            {(qasImported || prdImported) && (
              <button
                type="button"
                onClick={handleReset}
                className="border border-ink bg-surface px-2.5 py-1 text-xs font-mono font-bold text-ink hover:bg-surface-raised"
              >
                Reset Pipeline ↻
              </button>
            )}
          </div>
        </div>

        {errorNotice && (
          <div role="alert" className="border border-rose-500 bg-rose-100 p-2.5 text-xs text-rose-900 font-bold mb-3">
            ⚠️ {errorNotice}
          </div>
        )}

        {prdImported && (
          <div role="alert" className="border border-emerald-500 bg-emerald-100 p-2.5 text-xs text-emerald-950 font-bold mb-3">
            ✓ Transport DEVK900142 successfully committed to Production PRD (Client 300). Clean Core compliance validated with zero manual deviations.
          </div>
        )}

        <div className="space-y-2 text-xs font-mono">
          <div className="text-[11px] font-bold text-muted uppercase">Mandatory System Invariants:</div>
          <ul className="list-disc pl-4 space-y-1 text-muted">
            <li>
              <strong>No Overtaking</strong>: If Transport A creates CDS entity <code>ZI_SalesOrderItem</code>, and Transport B references that entity in an analytical cube <code>ZC_SalesOrderCube</code>, Transport B cannot overtake Transport A into QAS or PRD.
            </li>
            <li>
              <strong>Client 300 Protection</strong>: Production client SCC4 settings strictly set to <em>&quot;No changes allowed&quot;</em>.
            </li>
            <li>
              <strong>Cloud 3-System Landscape (3SL)</strong>: In S/4HANA Cloud Public Edition, CBC manages initial business scope, while Private Cloud and On-Premise use standard SPRO customizing with CTS/STMS transport pipelines.
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}
