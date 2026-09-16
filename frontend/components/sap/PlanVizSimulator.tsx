"use client";

import React, { useState } from "react";

interface PlanOperator {
  id: string;
  name: string;
  engine: "COLUMN" | "ROW" | "CALC" | "SQL";
  inclusive_time_ms: number;
  exclusive_time_ms: number;
  output_rows: number;
  memory_peak_kb: number;
  description: string;
  is_pushdown: boolean;
}

const PUSHDOWN_PLAN: PlanOperator[] = [
  {
    id: "op-1",
    name: "COLUMN SEARCH (Aggregation Pushdown)",
    engine: "COLUMN",
    inclusive_time_ms: 8.2,
    exclusive_time_ms: 5.1,
    output_rows: 4,
    memory_peak_kb: 420,
    description: "Evaluated directly in the HANA columnar engine with dictionary vectors. Filtered by Plant NM01/PL01 and grouped by Product Hierarchy in-memory.",
    is_pushdown: true,
  },
  {
    id: "op-2",
    name: "INVERTED INDEX RANGE SCAN (ACDOCA~PostingDate)",
    engine: "COLUMN",
    inclusive_time_ms: 2.1,
    exclusive_time_ms: 2.1,
    output_rows: 2400,
    memory_peak_kb: 180,
    description: "Utilizes HANA secondary inverted index on Posting Date to prune non-matching column partitions without full table scan.",
    is_pushdown: true,
  },
  {
    id: "op-3",
    name: "PROJECT (Calculated Margins)",
    engine: "SQL",
    inclusive_time_ms: 1.0,
    exclusive_time_ms: 1.0,
    output_rows: 4,
    memory_peak_kb: 64,
    description: "Final projection of calculated profit margins returning only 4 aggregated summary rows to the client.",
    is_pushdown: true,
  },
];

const NON_PUSHDOWN_PLAN: PlanOperator[] = [
  {
    id: "op-np-1",
    name: "TABLE SCAN (ACDOCA - Full Partition Read)",
    engine: "ROW",
    inclusive_time_ms: 380.0,
    exclusive_time_ms: 290.0,
    output_rows: 150000,
    memory_peak_kb: 86400,
    description: "Full table scan in row engine without filter pushdown. All 150,000 journal records materialized into temporary memory buffers.",
    is_pushdown: false,
  },
  {
    id: "op-np-2",
    name: "CALCULATION ENGINE (Row-by-Row Loop)",
    engine: "CALC",
    inclusive_time_ms: 190.0,
    exclusive_time_ms: 170.0,
    output_rows: 150000,
    memory_peak_kb: 45000,
    description: "Engine-hop to Calculation Engine executing row-by-row currency conversion loops in application memory.",
    is_pushdown: false,
  },
  {
    id: "op-np-3",
    name: "NETWORK TRANSPORT TO AS ABAP",
    engine: "SQL",
    inclusive_time_ms: 110.0,
    exclusive_time_ms: 110.0,
    output_rows: 150000,
    memory_peak_kb: 32000,
    description: "Massive payload transfer of 150,000 rows over network connection for aggregation inside ABAP internal tables.",
    is_pushdown: false,
  },
];

interface PlanVizSimulatorProps {
  title?: string;
  instruction?: string;
}

export const PlanVizSimulator: React.FC<PlanVizSimulatorProps> = ({
  title = "HANA Plan Visualizer (PlanViz) Execution Simulator",
  instruction = "Compare in-memory Column Engine Pushdown vs un-pushed Application Looping execution plans.",
}) => {
  const [activeMode, setActiveMode] = useState<"pushdown" | "non_pushdown">("pushdown");
  const [selectedOp, setSelectedOp] = useState<PlanOperator>(PUSHDOWN_PLAN[0]!);

  const currentPlan = activeMode === "pushdown" ? PUSHDOWN_PLAN : NON_PUSHDOWN_PLAN;
  const totalTime = currentPlan.reduce((acc, op) => acc + op.exclusive_time_ms, 0);
  const totalMemory = currentPlan.reduce((acc, op) => Math.max(acc, op.memory_peak_kb), 0);

  const handleModeChange = (mode: "pushdown" | "non_pushdown") => {
    setActiveMode(mode);
    setSelectedOp(mode === "pushdown" ? PUSHDOWN_PLAN[0]! : NON_PUSHDOWN_PLAN[0]!);
  };

  return (
    <div className="border-4 border-ink bg-surface p-6 shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] space-y-6">
      {/* Header Badge */}
      <div className="flex flex-wrap items-center justify-between gap-3 border-b-2 border-ink pb-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="border-2 border-ink bg-accent text-surface px-2 py-0.5 text-xs font-mono font-black uppercase tracking-wider">
              [SIMULATION MODEL]
            </span>
            <span className="border-2 border-ink bg-surface-raised px-2 py-0.5 text-xs font-mono font-bold text-muted">
              STATIC_VALIDATION / LOCAL_SIMULATION
            </span>
          </div>
          <h3 className="text-xl font-black font-mono tracking-tight mt-2">{title}</h3>
          <p className="text-xs font-mono text-muted mt-1">{instruction}</p>
        </div>

        {/* Mode Toggle */}
        <div className="flex border-2 border-ink">
          <button
            type="button"
            onClick={() => handleModeChange("pushdown")}
            className={`px-3 py-1.5 text-xs font-mono font-bold transition-colors ${
              activeMode === "pushdown"
                ? "bg-accent text-surface font-black"
                : "bg-surface text-ink hover:bg-surface-raised"
            }`}
          >
            Optimized Pushdown (CDS)
          </button>
          <button
            type="button"
            onClick={() => handleModeChange("non_pushdown")}
            className={`px-3 py-1.5 text-xs font-mono font-bold border-l-2 border-ink transition-colors ${
              activeMode === "non_pushdown"
                ? "bg-danger text-surface font-black"
                : "bg-surface text-ink hover:bg-surface-raised"
            }`}
          >
            Un-Pushed ABAP Loop
          </button>
        </div>
      </div>

      {/* Metrics Summary Card */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="border-2 border-ink bg-surface-raised p-3">
          <span className="text-[10px] font-mono text-muted uppercase font-bold">Total Execution Time</span>
          <p className={`text-2xl font-mono font-black ${activeMode === "pushdown" ? "text-accent" : "text-danger"}`}>
            {totalTime.toFixed(1)} ms
          </p>
          <span className="text-[10px] font-mono text-muted">
            {activeMode === "pushdown" ? "46x faster in-memory" : "Severe CPU overhead"}
          </span>
        </div>
        <div className="border-2 border-ink bg-surface-raised p-3">
          <span className="text-[10px] font-mono text-muted uppercase font-bold">Peak Memory Consumption</span>
          <p className={`text-2xl font-mono font-black ${activeMode === "pushdown" ? "text-accent" : "text-danger"}`}>
            {(totalMemory / 1024).toFixed(2)} MB
          </p>
          <span className="text-[10px] font-mono text-muted">
            {activeMode === "pushdown" ? "Pruned columnar vectors" : "Heavy row materialization"}
          </span>
        </div>
        <div className="border-2 border-ink bg-surface-raised p-3">
          <span className="text-[10px] font-mono text-muted uppercase font-bold">Transferred Rows to App Tier</span>
          <p className={`text-2xl font-mono font-black ${activeMode === "pushdown" ? "text-accent" : "text-danger"}`}>
            {activeMode === "pushdown" ? "4 rows" : "150,000 rows"}
          </p>
          <span className="text-[10px] font-mono text-muted">
            {activeMode === "pushdown" ? "Aggregated before transfer" : "Unfiltered data dump"}
          </span>
        </div>
      </div>

      {/* Plan Operator Hierarchy Visualizer */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="space-y-3">
          <h4 className="text-xs font-mono font-black uppercase text-muted tracking-wider">
            Execution Operator Tree (PlanViz Nodes)
          </h4>
          <div className="space-y-2">
            {currentPlan.map((op, idx) => (
              <button
                key={op.id}
                type="button"
                onClick={() => setSelectedOp(op)}
                className={`w-full text-left p-3 border-2 border-ink transition-all ${
                  selectedOp.id === op.id
                    ? "bg-ink text-surface shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] translate-x-1"
                    : "bg-surface hover:bg-surface-raised"
                }`}
              >
                <div className="flex items-center justify-between text-xs font-mono">
                  <span className="font-black">
                    #{idx + 1} {op.name}
                  </span>
                  <span
                    className={`px-1.5 py-0.5 text-[10px] font-bold border ${
                      selectedOp.id === op.id
                        ? "border-surface text-surface"
                        : "border-ink bg-surface-raised text-ink"
                    }`}
                  >
                    {op.engine}
                  </span>
                </div>
                <div className="flex justify-between items-center text-[10px] font-mono mt-1 opacity-80">
                  <span>{op.output_rows.toLocaleString()} rows</span>
                  <span>{op.inclusive_time_ms.toFixed(1)} ms</span>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Operator Inspection Panel */}
        <div className="border-2 border-ink bg-surface-raised p-4 space-y-4">
          <div className="flex justify-between items-center border-b-2 border-ink pb-2">
            <h4 className="text-xs font-mono font-black uppercase tracking-wider">
              Operator Details: {selectedOp.name}
            </h4>
            <span
              className={`text-[10px] font-mono px-2 py-0.5 font-bold ${
                selectedOp.is_pushdown ? "bg-accent text-surface" : "bg-danger text-surface"
              }`}
            >
              {selectedOp.is_pushdown ? "PUSHED DOWN" : "NON-PUSHDOWN"}
            </span>
          </div>

          <div className="space-y-2 text-xs font-mono">
            <div className="flex justify-between py-1 border-b border-ink/20">
              <span className="text-muted">Target Engine:</span>
              <span className="font-bold">{selectedOp.engine} Engine</span>
            </div>
            <div className="flex justify-between py-1 border-b border-ink/20">
              <span className="text-muted">Inclusive Time:</span>
              <span className="font-bold">{selectedOp.inclusive_time_ms} ms</span>
            </div>
            <div className="flex justify-between py-1 border-b border-ink/20">
              <span className="text-muted">Exclusive Time:</span>
              <span className="font-bold">{selectedOp.exclusive_time_ms} ms</span>
            </div>
            <div className="flex justify-between py-1 border-b border-ink/20">
              <span className="text-muted">Output Cardinality:</span>
              <span className="font-bold">{selectedOp.output_rows.toLocaleString()} rows</span>
            </div>
            <div className="flex justify-between py-1 border-b border-ink/20">
              <span className="text-muted">Peak Memory:</span>
              <span className="font-bold">{selectedOp.memory_peak_kb} KB</span>
            </div>
          </div>

          <div className="bg-surface p-3 border border-ink text-xs font-mono leading-relaxed">
            <span className="font-black block text-[10px] text-muted uppercase mb-1">Architectural Analysis:</span>
            {selectedOp.description}
          </div>
        </div>
      </div>

      {/* Truthfulness Footer Notice */}
      <div className="p-3 bg-surface border-2 border-ink text-[11px] font-mono text-muted flex items-center justify-between">
        <span>* This is an educational PlanViz model illustrating HANA in-memory engine principles.</span>
        <span className="font-bold text-ink">[LOCAL SIMULATION ONLY]</span>
      </div>
    </div>
  );
};
