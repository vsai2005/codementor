"use client";

import React, { useState } from "react";

export interface ModuleInteraction {
  trigger_event: string;
  lead_module: string;
  interacting_modules: string[];
  documents_created: string[];
  posting_logic: string;
}

interface ModuleInteractionVisualizerProps {
  flowData?: ModuleInteraction[];
  title?: string;
  instruction?: string;
}

export function ModuleInteractionVisualizer({
  flowData = [],
  title = "Synchronous Cross-Module Integration Visualizer",
  instruction = "Select operational trigger events to inspect how MM and SD logistics actions generate simultaneous FI/CO accounting documents.",
}: ModuleInteractionVisualizerProps) {
  const [selectedIdx, setSelectedIdx] = useState<number>(0);
  const activeInteraction = flowData[selectedIdx] || flowData[0];

  return (
    <div className="border-3 border-ink bg-surface p-5 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
      <div className="mb-4">
        <h3 className="text-base font-black text-ink">{title}</h3>
        <p className="text-xs text-muted mt-0.5">{instruction}</p>
      </div>

      {/* Trigger Event Tabs */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-2 mb-4">
        {flowData.map((item, idx) => {
          const isSelected = idx === selectedIdx;
          return (
            <button
              key={idx}
              type="button"
              onClick={() => setSelectedIdx(idx)}
              className={`p-3 text-left border-2 border-ink transition-all ${
                isSelected
                  ? "bg-ink text-surface shadow-[3px_3px_0px_0px_rgba(16,185,129,1)] translate-x-0.5"
                  : "bg-surface hover:bg-surface-raised text-ink"
              }`}
            >
              <div className="flex items-center justify-between text-[10px] font-mono font-bold mb-1">
                <span>EVENT #{idx + 1}</span>
                <span
                  className={`px-1.5 py-0.5 rounded ${
                    isSelected ? "bg-emerald-400 text-ink" : "bg-emerald-100 text-emerald-900"
                  }`}
                >
                  {item.lead_module}
                </span>
              </div>
              <div className="text-xs font-black line-clamp-2">
                {item.trigger_event}
              </div>
            </button>
          );
        })}
      </div>

      {/* Cross-Module Posting Flow Visualization */}
      {activeInteraction && (
        <div className="border-2 border-ink bg-surface-raised p-4 space-y-4">
          {/* Header Bar */}
          <div className="flex flex-wrap items-center justify-between gap-2 border-b border-ink/20 pb-2">
            <div className="text-sm font-black text-ink">
              {activeInteraction.trigger_event}
            </div>
            <div className="flex items-center gap-1.5 text-xs font-mono">
              <span className="text-muted font-bold">Interacting:</span>
              {activeInteraction.interacting_modules.map((mod, i) => (
                <span
                  key={i}
                  className="bg-purple-100 text-purple-900 border border-purple-300 font-bold px-1.5 py-0.5 rounded text-[10px]"
                >
                  {mod}
                </span>
              ))}
            </div>
          </div>

          {/* Generated Documents Flow */}
          <div>
            <div className="text-[10px] font-mono font-bold uppercase text-muted mb-2">
              Synchronous Dual-Document Generation (Zero Latency)
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {activeInteraction.documents_created.map((doc, idx) => {
                const isMaterialDoc = doc.toLowerCase().includes("material");
                return (
                  <div
                    key={idx}
                    className={`border-2 border-ink p-3 ${
                      isMaterialDoc ? "bg-blue-50" : "bg-emerald-50"
                    }`}
                  >
                    <div className="text-[10px] font-mono font-bold uppercase text-muted mb-0.5">
                      {isMaterialDoc ? "📦 Logistics Ledger" : "💳 General Ledger (FI)"}
                    </div>
                    <div className="text-xs font-black font-mono text-ink">
                      {doc}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Posting Logic / T-Account Representation */}
          <div className="border-2 border-ink bg-surface p-4">
            <div className="text-[10px] font-mono font-bold uppercase text-muted mb-2">
              Automated Account Determination & G/L Impact
            </div>
            <div className="bg-amber-50 border border-amber-300 p-3 font-mono text-xs font-bold text-amber-950">
              {activeInteraction.posting_logic}
            </div>
            <p className="text-[11px] text-muted mt-2">
              Postings execute atomically inside a single SAP Logical Unit of Work (LUW).
              If the financial posting fails, the goods movement is rolled back automatically.
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
