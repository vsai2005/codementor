"use client";

import React, { useState } from "react";

export interface ProcessStage {
  stage?: string;
  name?: string;
  module?: string;
  department?: string;
  tcode?: string;
  doc_type?: string;
  document?: string;
  impact?: string;
  status?: string;
  step_number?: number;
}

interface ProcessFlowProps {
  flowData: ProcessStage[];
  title?: string;
  description?: string;
}

export function ProcessFlow({
  flowData,
  title = "End-to-End Cross-Functional Process Flow",
  description = "Click each stage in the pipeline to inspect how documents and postings move across SAP modules in real time.",
}: ProcessFlowProps) {
  const [selectedIdx, setSelectedIdx] = useState<number>(0);
  const activeStage = flowData[selectedIdx] || flowData[0];

  const getStageTitle = (item?: ProcessStage) => item?.stage || item?.name || "Stage";
  const getStageModule = (item?: ProcessStage) => item?.module || item?.department || "Cross-Module";
  const getStageDoc = (item?: ProcessStage) => item?.doc_type || item?.document || "Document";
  const getStageTcode = (item?: ProcessStage) => item?.tcode || item?.department || "SAP S/4HANA App";
  const getStageStatus = (item?: ProcessStage) => item?.status || "In Sequence";

  const handleKeyDown = (e: React.KeyboardEvent, currentIdx: number) => {
    if (e.key === "ArrowRight") {
      e.preventDefault();
      setSelectedIdx(Math.min(flowData.length - 1, currentIdx + 1));
    } else if (e.key === "ArrowLeft") {
      e.preventDefault();
      setSelectedIdx(Math.max(0, currentIdx - 1));
    }
  };

  return (
    <div className="border-3 border-ink bg-surface p-5 shadow-hard">
      <div className="mb-4">
        <h3 className="text-base font-black text-ink">{title}</h3>
        <p className="text-xs text-muted mt-0.5">{description}</p>
      </div>

      {/* Horizontal Stage Stepper with Arrow Key Navigation */}
      <div
        role="tablist"
        aria-label="Process stages"
        className="flex items-center gap-2 overflow-x-auto pb-3 pt-1 border-b-2 border-ink scrollbar-thin"
      >
        {flowData.map((item, idx) => {
          const isSelected = idx === selectedIdx;
          const stageTitle = getStageTitle(item);
          const stageMod = getStageModule(item);
          const stageDoc = getStageDoc(item);

          return (
            <React.Fragment key={idx}>
              <button
                role="tab"
                aria-selected={isSelected}
                aria-controls={`stage-panel-${idx}`}
                id={`stage-tab-${idx}`}
                tabIndex={isSelected ? 0 : -1}
                type="button"
                onKeyDown={(e) => handleKeyDown(e, idx)}
                onClick={() => setSelectedIdx(idx)}
                className={`flex-1 min-w-[140px] p-2.5 text-left border-2 border-ink transition-all focus-visible:ring-2 focus-visible:ring-ink focus-visible:outline-none ${
                  isSelected
                    ? "bg-ink text-surface shadow-hard-sm"
                    : "bg-surface hover:bg-surface-raised text-ink"
                }`}
              >
                <div className="flex items-center justify-between text-[10px] font-mono font-bold uppercase mb-1">
                  <span>Step {idx + 1}</span>
                  <span
                    className={`px-1 rounded border border-ink/20 ${
                      isSelected
                        ? "bg-emerald-400 text-ink"
                        : "bg-purple-100 text-purple-900"
                    }`}
                  >
                    {stageMod.split(" ")[0]}
                  </span>
                </div>
                <div className="text-xs font-black truncate">{stageTitle}</div>
                <div
                  className={`text-[10px] truncate ${
                    isSelected ? "text-surface/80" : "text-muted"
                  }`}
                >
                  {stageDoc}
                </div>
              </button>

              {idx < flowData.length - 1 && (
                <span aria-hidden="true" className="text-ink font-black text-sm px-0.5 shrink-0">
                  →
                </span>
              )}
            </React.Fragment>
          );
        })}
      </div>

      {/* Stage Detail Drilldown */}
      {activeStage && (
        <div
          role="tabpanel"
          id={`stage-panel-${selectedIdx}`}
          aria-labelledby={`stage-tab-${selectedIdx}`}
          className="mt-4 bg-surface-raised border-2 border-ink p-4"
        >
          <div className="flex flex-wrap items-center justify-between gap-2 mb-3">
            <div>
              <span className="text-[10px] font-mono uppercase bg-blue-100 border border-ink text-ink font-bold px-2 py-0.5 mr-2">
                Module / Team: {getStageModule(activeStage)}
              </span>
              <span className="text-sm font-black text-ink">
                {getStageTitle(activeStage)} (Step {selectedIdx + 1} of {flowData.length})
              </span>
            </div>
            <div className="text-xs font-mono font-bold bg-amber-100 border border-ink px-2 py-0.5 text-ink">
              Status: {getStageStatus(activeStage)}
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
            <div className="border border-ink/40 bg-surface p-3">
              <div className="text-[10px] font-mono font-bold uppercase text-muted mb-1">
                Transaction / Application Scope
              </div>
              <div className="font-mono font-bold text-ink text-xs">
                {getStageTcode(activeStage)}
              </div>
            </div>

            <div className="border border-ink/40 bg-surface p-3">
              <div className="text-[10px] font-mono font-bold uppercase text-muted mb-1">
                Generated Enterprise Document
              </div>
              <div className="font-mono font-bold text-ink text-xs">
                {getStageDoc(activeStage)}
              </div>
            </div>
          </div>

          <div className="mt-3 border border-ink/40 bg-surface p-3">
            <div className="text-[10px] font-mono font-bold uppercase text-muted mb-1">
              Cross-Module Financial & Operational Impact
            </div>
            <p className="text-xs text-ink font-medium leading-relaxed">
              {activeStage.impact}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
