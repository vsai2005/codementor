"use client";

import React, { useState } from "react";

export interface ArchitectureLayer {
  layer: string;
  components: string;
  role: string;
  diagnostic: string;
}

interface ArchitectureLayerMapperProps {
  flowData?: ArchitectureLayer[];
  title?: string;
  instruction?: string;
}

export function ArchitectureLayerMapper({
  flowData = [],
  title = "SAP 3-Tier Enterprise Architecture Diagnostic",
  instruction = "Click each architectural layer to inspect its system components, runtime responsibilities, and operational diagnostic indicators.",
}: ArchitectureLayerMapperProps) {
  const [activeIdx, setActiveIdx] = useState<number>(1); // Default to Application Layer
  const currentLayer = flowData[activeIdx] || flowData[0];

  return (
    <div className="border-3 border-ink bg-surface p-5 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
      <div className="mb-4">
        <h3 className="text-base font-black text-ink">{title}</h3>
        <p className="text-xs text-muted mt-0.5">{instruction}</p>
      </div>

      {/* 3-Tier Diagram Stack */}
      <div className="space-y-3 mb-6">
        {flowData.map((layer, idx) => {
          const isSelected = idx === activeIdx;
          const tierColors = [
            "border-sky-500 bg-sky-50",
            "border-purple-500 bg-purple-50",
            "border-emerald-500 bg-emerald-50",
          ];

          return (
            <button
              key={idx}
              type="button"
              onClick={() => setActiveIdx(idx)}
              className={`w-full text-left border-3 border-ink p-4 transition-all flex flex-col md:flex-row md:items-center justify-between gap-3 ${
                isSelected
                  ? "bg-ink text-surface shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] translate-x-1"
                  : `${tierColors[idx % 3]} hover:bg-surface-raised text-ink`
              }`}
            >
              <div className="flex items-center gap-3">
                <span
                  className={`font-mono text-xs font-black px-2.5 py-1 border-2 border-ink ${
                    isSelected ? "bg-amber-300 text-ink" : "bg-white text-ink"
                  }`}
                >
                  LAYER {idx + 1}
                </span>
                <div>
                  <div className="text-sm font-black tracking-wide">
                    {layer.layer}
                  </div>
                  <div
                    className={`text-xs font-mono truncate max-w-md ${
                      isSelected ? "text-surface/80" : "text-muted"
                    }`}
                  >
                    {layer.components}
                  </div>
                </div>
              </div>

              <span
                className={`text-xs font-mono font-bold px-3 py-1 border ${
                  isSelected
                    ? "border-surface text-surface"
                    : "border-ink bg-surface text-ink"
                }`}
              >
                Inspect Layer →
              </span>
            </button>
          );
        })}
      </div>

      {/* Selected Layer Diagnostic Pane */}
      {currentLayer && (
        <div className="border-2 border-ink bg-surface-raised p-4">
          <div className="flex items-center justify-between border-b border-ink/20 pb-2 mb-3">
            <div className="text-sm font-black text-ink">
              Diagnostic Dossier: {currentLayer.layer}
            </div>
            <span className="text-[10px] font-mono font-bold uppercase bg-blue-100 border border-ink px-2 py-0.5 text-ink">
              System Invariant
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-3 text-xs">
            <div className="border border-ink/30 bg-surface p-3">
              <div className="text-[10px] font-mono font-bold uppercase text-muted mb-1">
                Subsystems & Components
              </div>
              <div className="font-mono text-ink font-semibold">
                {currentLayer.components}
              </div>
            </div>

            <div className="border border-ink/30 bg-surface p-3">
              <div className="text-[10px] font-mono font-bold uppercase text-muted mb-1">
                Runtime Execution Responsibility
              </div>
              <p className="text-ink leading-relaxed font-medium">
                {currentLayer.role}
              </p>
            </div>
          </div>

          <div className="border border-amber-400 bg-amber-50 p-3 text-xs">
            <div className="text-[10px] font-mono font-black uppercase text-amber-900 mb-1">
              ⚠️ Operational Incident Diagnostic
            </div>
            <p className="text-amber-950 font-medium leading-relaxed">
              {currentLayer.diagnostic}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
