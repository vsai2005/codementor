"use client";

import React, { useState } from "react";

export interface OrgUnit {
  id?: string;
  unit?: string;
  type?: string;
  code: string;
  role?: string;
  description?: string;
  parent?: string | null;
  level?: number;
}

interface OrgStructureMapperProps {
  units?: OrgUnit[];
  title?: string;
  instruction?: string;
}

export function OrgStructureMapper({
  units = [],
  title = "Enterprise Organizational Hierarchy Explorer",
  instruction = "Click organizational units to explore hierarchical bindings and structural constraints.",
}: OrgStructureMapperProps) {
  const [selectedCode, setSelectedCode] = useState<string>(
    units[0]?.code || "100"
  );

  const selectedUnit = units.find((u) => u.code === selectedCode) || units[0];

  const getUnitType = (u?: OrgUnit) => u?.unit || u?.type || "Unit";
  const getUnitRole = (u?: OrgUnit) => u?.role || u?.description || "Enterprise organizational entity.";

  return (
    <div className="border-3 border-ink bg-surface p-5 shadow-hard">
      <div className="flex flex-wrap items-center justify-between gap-2 mb-4">
        <div>
          <h3 className="text-base font-black text-ink">{title}</h3>
          <p className="text-xs text-muted mt-0.5">{instruction}</p>
        </div>
        {units.length > 0 && units[0] && (
          <button
            type="button"
            onClick={() => setSelectedCode(units[0]?.code || "")}
            className="border border-ink bg-surface px-2.5 py-1 text-[11px] font-mono font-bold text-ink hover:bg-surface-raised focus-visible:ring-2 focus-visible:ring-ink"
          >
            Reset to Top Node ({units[0].code}) ↻
          </button>
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {/* Left 2 Cols: Interactive Tree Structure */}
        <div className="lg:col-span-2 border-2 border-ink bg-surface-raised p-4">
          <div className="text-[11px] font-mono font-bold uppercase text-muted mb-3">
            Organizational Tree (Nova Manufacturing NM01)
          </div>

          <div role="tree" aria-label="Organizational Hierarchy" className="space-y-2">
            {units.map((unit) => {
              const isSelected = unit.code === selectedCode;
              const parentStr = unit.parent || "";
              const indentClass = !unit.parent
                ? "ml-0"
                : parentStr.toLowerCase().includes("client")
                ? "ml-2 sm:ml-4 border-l-2 border-ink/30 pl-2 sm:pl-3"
                : parentStr.toLowerCase().includes("company") || parentStr.toLowerCase().includes("u2")
                ? "ml-4 sm:ml-8 border-l-2 border-ink/30 pl-2 sm:pl-3"
                : "ml-6 sm:ml-12 border-l-2 border-ink/30 pl-2 sm:pl-3";

              return (
                <div key={unit.code} className={`${indentClass} transition-all`}>
                  <button
                    role="treeitem"
                    aria-selected={isSelected}
                    type="button"
                    onClick={() => setSelectedCode(unit.code)}
                    className={`w-full text-left border-2 border-ink p-2.5 transition-all flex flex-wrap sm:flex-nowrap items-center justify-between gap-1 focus-visible:ring-2 focus-visible:ring-purple-600 focus-visible:outline-none ${
                      isSelected
                        ? "bg-ink text-surface shadow-hard-sm translate-x-1"
                        : "bg-surface hover:bg-surface-raised text-ink"
                    }`}
                  >
                    <div className="flex items-center gap-2">
                      <span
                        className={`text-[10px] font-mono font-bold px-1.5 py-0.5 rounded border uppercase ${
                          isSelected
                            ? "bg-purple-400 text-ink border-ink"
                            : "bg-purple-100 text-purple-900 border-purple-300"
                        }`}
                      >
                        {getUnitType(unit)}
                      </span>
                      <span className="text-xs font-black font-mono">
                        {unit.code}
                      </span>
                    </div>

                    {unit.parent && (
                      <span
                        className={`text-[10px] font-mono ${
                          isSelected ? "text-surface/80" : "text-muted"
                        }`}
                      >
                        Parent: {unit.parent}
                      </span>
                    )}
                  </button>
                </div>
              );
            })}
          </div>
        </div>

        {/* Right Col: Selected Unit Card & Invariants */}
        {selectedUnit && (
          <div className="border-2 border-ink bg-surface p-4 flex flex-col justify-between">
            <div>
              <div className="flex items-center gap-2 mb-2">
                <span className="text-[10px] font-mono font-bold uppercase bg-ink text-surface px-2 py-0.5">
                  {getUnitType(selectedUnit)}
                </span>
                <span className="text-sm font-black font-mono text-ink">
                  Code: {selectedUnit.code}
                </span>
              </div>

              <div className="text-xs font-mono text-muted mb-3">
                Assigned Under: {selectedUnit.parent || "None (Enterprise Root)"}
              </div>

              <div className="border border-ink/40 bg-surface-raised p-3 mb-4">
                <div className="text-[10px] font-mono font-bold uppercase text-muted mb-1">
                  Architectural Role & Scope
                </div>
                <p className="text-xs text-ink leading-relaxed font-medium">
                  {getUnitRole(selectedUnit)}
                </p>
              </div>

              <div className="border border-amber-400 bg-amber-50 p-3 text-xs text-amber-950">
                <span className="font-bold">Enterprise Invariant: </span>
                {getUnitType(selectedUnit).toLowerCase().includes("plant") && (
                  <span>
                    A Plant must belong to exactly ONE Company Code. Valuated stock
                    and production accounting flow strictly through this single link.
                  </span>
                )}
                {getUnitType(selectedUnit).toLowerCase().includes("company") && (
                  <span>
                    Must generate statutory financial statements. Valuation area
                    (inventory price) is strictly assigned at or below this level.
                  </span>
                )}
                {getUnitType(selectedUnit).toLowerCase().includes("purchasing") && (
                  <span>
                    Can be assigned to Company Code (centralized) or left cross-company
                    to negotiate volume discounts across multiple legal entities.
                  </span>
                )}
                {getUnitType(selectedUnit).toLowerCase().includes("sales") && (
                  <span>
                    Directly tied to exactly one Company Code. Responsible for
                    distributing goods and legally billing customers.
                  </span>
                )}
                {getUnitType(selectedUnit).toLowerCase().includes("client") && (
                  <span>
                    Master data (BP numbers, material IDs) can be shared across
                    the client, but views are activated per Company Code and Plant.
                  </span>
                )}
              </div>
            </div>

            <div className="mt-4 pt-3 border-t border-ink/20 text-[10px] font-mono text-muted">
              Digital Twin: Nova Manufacturing Corp (Client 100)
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
