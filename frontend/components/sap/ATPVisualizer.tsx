"use client";

import React, { useState } from "react";

export interface PlantStock {
  plant_code: string;
  plant_name: string;
  unrestricted_stock: number;
  open_sales_reservations: number;
  replenishment_lead_time_days: number;
  available_atp: number;
}

const INITIAL_PLANTS: PlantStock[] = [
  {
    plant_code: "PL01",
    plant_name: "Heidelberg Assembly",
    unrestricted_stock: 45,
    open_sales_reservations: 30,
    replenishment_lead_time_days: 2,
    available_atp: 15,
  },
  {
    plant_code: "PL02",
    plant_name: "Austin Tech Center",
    unrestricted_stock: 80,
    open_sales_reservations: 10,
    replenishment_lead_time_days: 5,
    available_atp: 70,
  },
];

interface ATPVisualizerProps {
  title?: string;
  instruction?: string;
}

export function ATPVisualizer({
  title = "Advanced ATP (aATP) & Multi-Plant Sourcing",
  instruction = "Simulate how SAP S/4HANA performs an Available-to-Promise (ATP) check when Customer CUST-501 places a rush order for 40x DXTR-1000 controllers. Use Alternative-Based Confirmation (ABC) to resolve plant shortages.",
}: ATPVisualizerProps) {
  const [requestedQty, setRequestedQty] = useState<number>(40);
  const [enableABC, setEnableABC] = useState<boolean>(false);

  const plantPL01 = INITIAL_PLANTS[0]!;
  const plantPL02 = INITIAL_PLANTS[1]!;

  const pl01Shortage = requestedQty > plantPL01.available_atp;
  const pl01Deficit = requestedQty - plantPL01.available_atp;

  return (
    <div className="border-3 border-ink bg-surface p-5 shadow-hard">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-2 mb-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="border border-ink bg-sky-200 text-sky-950 px-2 py-0.5 text-xs font-mono font-bold">
              [SIMULATION MODEL] ADVANCED ATP
            </span>
            <span className="border border-ink bg-surface-raised px-2 py-0.5 text-xs font-mono font-bold text-ink">
              Material: DXTR-1000 (Robotics Controller)
            </span>
            <h3 className="text-base font-black text-ink">{title}</h3>
          </div>
          <p className="text-xs text-muted mt-1 leading-relaxed">{instruction}</p>
        </div>

        <div className="text-xs font-mono font-bold bg-surface-raised border border-ink p-1.5">
          Customer: <span className="text-purple-700">CUST-501 (Req: {requestedQty} EA)</span>
        </div>
      </div>

      {/* Interactive Controls Bar */}
      <div className="border-2 border-ink bg-surface-raised p-3 mb-5 flex flex-wrap items-center justify-between gap-3 text-xs font-mono">
        <div className="flex items-center gap-2">
          <label htmlFor="req_qty" className="font-bold text-ink">
            Order Quantity:
          </label>
          <input
            id="req_qty"
            type="number"
            min="10"
            max="100"
            step="5"
            value={requestedQty}
            onChange={(e) => setRequestedQty(Number(e.target.value))}
            className="w-20 p-1 border border-ink bg-surface font-black text-ink focus-visible:ring-2 focus-visible:ring-ink"
          />
          <span className="text-muted">EA</span>
        </div>

        <div className="flex items-center gap-2">
          <label className="flex items-center gap-2 cursor-pointer font-bold text-ink">
            <input
              type="checkbox"
              checked={enableABC}
              onChange={(e) => setEnableABC(e.target.checked)}
              className="accent-sky-600"
            />
            <span>Enable Alternative-Based Confirmation (ABC Substitution)</span>
          </label>
        </div>
      </div>

      {/* Multi-Plant Inventory Status Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-5 font-mono text-xs">
        {/* Plant PL01 Card */}
        <div className="border-2 border-ink p-4 transition-all bg-sky-50 shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] border-sky-950">
          <div className="flex items-center justify-between border-b border-ink/40 pb-2 mb-3">
            <div>
              <span className="text-[10px] text-muted uppercase font-bold block">Primary Delivering Plant</span>
              <h4 className="text-sm font-black text-ink">{plantPL01.plant_code} — {plantPL01.plant_name}</h4>
            </div>
            <span className="bg-sky-200 text-sky-950 border border-sky-600 px-1.5 py-0.5 text-[10px] font-bold">
              Default Sourcing
            </span>
          </div>

          <div className="space-y-1.5">
            <div className="flex justify-between">
              <span className="text-muted">Unrestricted Stock:</span>
              <span className="font-bold text-ink">{plantPL01.unrestricted_stock} EA</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted">Open Reservations:</span>
              <span className="font-bold text-rose-700">-{plantPL01.open_sales_reservations} EA</span>
            </div>
            <div className="flex justify-between border-t border-ink/20 pt-1">
              <span className="font-bold text-ink">Available to Promise (ATP):</span>
              <span className="font-black text-emerald-950 text-sm">{plantPL01.available_atp} EA</span>
            </div>
            <div className="text-[10px] text-muted mt-2 pt-1 border-t border-ink/10">
              Replenishment Lead Time: {plantPL01.replenishment_lead_time_days} days
            </div>
          </div>
        </div>

        {/* Plant PL02 Card */}
        <div
          className={`border-2 border-ink p-4 transition-all ${
            enableABC
              ? "bg-emerald-50 shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] border-emerald-950"
              : "bg-surface opacity-60"
          }`}
        >
          <div className="flex items-center justify-between border-b border-ink/40 pb-2 mb-3">
            <div>
              <span className="text-[10px] text-muted uppercase font-bold block">Alternative Plant (ABC Candidate)</span>
              <h4 className="text-sm font-black text-ink">{plantPL02.plant_code} — {plantPL02.plant_name}</h4>
            </div>
            <span
              className={`px-1.5 py-0.5 text-[10px] font-bold border ${
                enableABC
                  ? "bg-emerald-200 text-emerald-950 border-emerald-600"
                  : "bg-muted/20 text-muted border-ink/20"
              }`}
            >
              {enableABC ? "ABC Active" : "ABC Standby"}
            </span>
          </div>

          <div className="space-y-1.5">
            <div className="flex justify-between">
              <span className="text-muted">Unrestricted Stock:</span>
              <span className="font-bold text-ink">{plantPL02.unrestricted_stock} EA</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted">Open Reservations:</span>
              <span className="font-bold text-rose-700">-{plantPL02.open_sales_reservations} EA</span>
            </div>
            <div className="flex justify-between border-t border-ink/20 pt-1">
              <span className="font-bold text-ink">Available to Promise (ATP):</span>
              <span className="font-black text-emerald-950 text-sm">{plantPL02.available_atp} EA</span>
            </div>
            <div className="text-[10px] text-muted mt-2 pt-1 border-t border-ink/10">
              Replenishment Lead Time: {plantPL02.replenishment_lead_time_days} days (Transatlantic Freight)
            </div>
          </div>
        </div>
      </div>

      {/* Confirmation Outcome Banner */}
      <div className="border-2 border-ink bg-surface-raised p-4 mb-4">
        <div className="space-y-2">
          <span className="text-[10px] text-muted uppercase font-bold font-mono block">
            Automated ATP Confirmation Strategy
          </span>

          {!enableABC && pl01Shortage ? (
            <div role="alert" className="p-3 border border-amber-500 bg-amber-50 text-amber-950 text-xs font-mono">
              <div className="font-black text-amber-900 mb-1">
                ⚠️ Partial Confirmation at Primary Plant PL01
              </div>
              <div>
                Order for {requestedQty} EA cannot be fully satisfied from PL01 immediately.
                <ul className="list-disc pl-4 mt-1 space-y-0.5">
                  <li><strong>Immediate Delivery</strong>: Confirmed {plantPL01.available_atp} EA for shipping tomorrow.</li>
                  <li><strong>Backorder Line</strong>: Deficit of {pl01Deficit} EA delayed by {plantPL01.replenishment_lead_time_days} days pending production.</li>
                </ul>
                <div className="mt-2 text-indigo-900 font-bold">
                  💡 Tip: Enable Alternative-Based Confirmation (ABC) to auto-fulfill the shortage from Austin (PL02).
                </div>
              </div>
            </div>
          ) : enableABC && pl01Shortage ? (
            <div role="alert" className="p-3 border border-emerald-500 bg-emerald-50 text-emerald-950 text-xs font-mono">
              <div className="font-black text-emerald-900 mb-1">
                ✓ Alternative-Based Confirmation (ABC) Succeeded!
              </div>
              <div>
                Multi-plant schedule line split executed automatically:
                <ul className="list-disc pl-4 mt-1 space-y-0.5">
                  <li>Schedule Line 1: <strong>{plantPL01.available_atp} EA</strong> delivered from Plant PL01 (Heidelberg).</li>
                  <li>Schedule Line 2: <strong>{pl01Deficit} EA</strong> substituted from Plant PL02 (Austin) with zero delayed backorder!</li>
                </ul>
              </div>
            </div>
          ) : (
            <div role="alert" className="p-3 border border-emerald-500 bg-emerald-50 text-emerald-950 text-xs font-mono">
              <div className="font-black text-emerald-900 mb-1">
                ✓ Full Confirmation at Primary Plant PL01
              </div>
              All {requestedQty} EA confirmed for immediate shipment from Heidelberg. Zero shortage detected.
            </div>
          )}
        </div>
      </div>

      {/* Architectural Invariant */}
      <div className="border border-ink bg-surface p-3 text-xs font-mono">
        <span className="font-bold text-ink block mb-1">Advanced ATP (aATP) S/4HANA Invariant:</span>
        <p className="text-muted leading-relaxed text-[11px]">
          In S/4HANA, <strong>aATP</strong> runs in-memory directly on the HANA database layer using native SQLScript algorithms. When stock shortages occur, <strong>Alternative-Based Confirmation (ABC)</strong> dynamically analyzes alternative plants, storage locations, or substitute materials, and <strong>Backorder Processing (BOP)</strong> re-prioritizes orders based on customer profitability tiers.
        </p>
      </div>
    </div>
  );
}
