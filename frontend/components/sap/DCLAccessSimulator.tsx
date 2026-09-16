"use client";

import React, { useState } from "react";

interface Persona {
  id: string;
  name: string;
  role: string;
  pfcg_object: string;
  authorized_plants: string[];
  injected_where_clause: string;
}

interface InventoryRow {
  material: string;
  description: string;
  plant: string;
  storage_loc: string;
  unrestricted_stock: number;
  unit: string;
  value_eur: number;
}

const PERSONAS: Persona[] = [
  {
    id: "user-hd",
    name: "Klaus Schmidt",
    role: "Heidelberg Plant Manager (PL01)",
    pfcg_object: "M_MATE_WRK (Plant Authorization)",
    authorized_plants: ["PL01"],
    injected_where_clause: "WHERE (Plant = 'PL01')",
  },
  {
    id: "user-at",
    name: "Sarah Miller",
    role: "Austin Plant Manager (PL02)",
    pfcg_object: "M_MATE_WRK (Plant Authorization)",
    authorized_plants: ["PL02"],
    injected_where_clause: "WHERE (Plant = 'PL02')",
  },
  {
    id: "user-vp",
    name: "Elena Rostova",
    role: "Global Supply Chain VP (NM01)",
    pfcg_object: "M_MATE_WRK (Full Company Scope)",
    authorized_plants: ["PL01", "PL02"],
    injected_where_clause: "WHERE (Plant IN ('PL01', 'PL02'))",
  },
  {
    id: "user-guest",
    name: "External Temp Auditor",
    role: "Restricted Guest (No Plant Authorizations)",
    pfcg_object: "M_MATE_WRK (Empty Role)",
    authorized_plants: [],
    injected_where_clause: "WHERE (1 = 0) -- Blocked by DCL",
  },
];

const FULL_INVENTORY_TABLE: InventoryRow[] = [
  { material: "DXTR-1000", description: "Industrial Robotics Controller", plant: "PL01", storage_loc: "FG01", unrestricted_stock: 45, unit: "EA", value_eur: 67500 },
  { material: "RAW-01", description: "Precision Optical Sensor Array", plant: "PL01", storage_loc: "RAW1", unrestricted_stock: 250, unit: "EA", value_eur: 25000 },
  { material: "DXTR-1000", description: "Industrial Robotics Controller", plant: "PL02", storage_loc: "FG01", unrestricted_stock: 28, unit: "EA", value_eur: 42000 },
  { material: "RAW-01", description: "Precision Optical Sensor Array", plant: "PL02", storage_loc: "RAW1", unrestricted_stock: 110, unit: "EA", value_eur: 11000 },
];

interface DCLAccessSimulatorProps {
  title?: string;
  instruction?: string;
}

export const DCLAccessSimulator: React.FC<DCLAccessSimulatorProps> = ({
  title = "DCL Access Control & Row-Level Security Simulator",
  instruction = "Switch user personas to inspect how declarative DCL rules inject database-tier authorization filters into HANA queries.",
}) => {
  const [selectedPersona, setSelectedPersona] = useState<Persona>(PERSONAS[0]!);

  const visibleRows = FULL_INVENTORY_TABLE.filter((row) =>
    selectedPersona.authorized_plants.includes(row.plant)
  );

  const blockedRowCount = FULL_INVENTORY_TABLE.length - visibleRows.length;

  return (
    <div className="border-4 border-ink bg-surface p-6 shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] space-y-6">
      {/* Header */}
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

        {/* Persona Selectors */}
        <div className="flex flex-wrap border-2 border-ink">
          {PERSONAS.map((p) => (
            <button
              key={p.id}
              type="button"
              onClick={() => setSelectedPersona(p)}
              className={`px-3 py-1.5 text-xs font-mono font-bold transition-colors border-r border-ink last:border-r-0 ${
                selectedPersona.id === p.id
                  ? "bg-ink text-surface font-black"
                  : "bg-surface hover:bg-surface-raised"
              }`}
            >
              {p.name.split(" ")[0]} ({p.authorized_plants.join(",") || "None"})
            </button>
          ))}
        </div>
      </div>

      {/* Security Context Banner */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="border-2 border-ink bg-surface-raised p-3">
          <span className="text-[10px] font-mono text-muted uppercase font-bold">Active User Persona</span>
          <p className="text-lg font-mono font-black text-ink">{selectedPersona.name}</p>
          <span className="text-[10px] font-mono text-muted">{selectedPersona.role}</span>
        </div>
        <div className="border-2 border-ink bg-surface-raised p-3">
          <span className="text-[10px] font-mono text-muted uppercase font-bold">PFCG Authorization Aspect</span>
          <p className="text-sm font-mono font-black text-ink">{selectedPersona.pfcg_object}</p>
          <span className="text-[10px] font-mono text-muted">
            Authorized: {selectedPersona.authorized_plants.join(", ") || "No Plants"}
          </span>
        </div>
        <div className="border-2 border-ink bg-surface-raised p-3">
          <span className="text-[10px] font-mono text-muted uppercase font-bold">Row-Level Filter Result</span>
          <p
            className={`text-lg font-mono font-black ${
              selectedPersona.authorized_plants.length === 0 ? "text-danger" : "text-accent"
            }`}
          >
            {visibleRows.length} Rows Visible / {blockedRowCount} Blocked
          </p>
          <span className="text-[10px] font-mono text-muted">Database-tier enforcement</span>
        </div>
      </div>

      {/* DCL Code & Injected SQL */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* DCL Role Source */}
        <div className="border-2 border-ink bg-surface-raised p-4 space-y-2">
          <div className="flex justify-between items-center border-b border-ink/40 pb-1">
            <h4 className="text-xs font-mono font-black uppercase tracking-wider">
              Data Control Language (DCL) DEFINE ROLE
            </h4>
            <span className="text-[10px] font-mono bg-accent text-surface px-2 py-0.5 font-bold">
              DECLARATIVE RULE
            </span>
          </div>

          <pre className="p-3 bg-surface border border-ink text-xs font-mono overflow-x-auto text-ink/90 leading-relaxed max-h-48 overflow-y-auto">
            <code>{`@EndUserText.label: 'Nova Plant Authorization Role'
@MappingRole: true
define role Z_Nova_Plant_Access {
  grant select on I_NovaPlantInventory
  where (Plant) = aspect pfcg_auth(
    M_MATE_WRK,
    WERKS,
    ACTVT = '03'
  );
}`}</code>
          </pre>
          <p className="text-[11px] font-mono text-muted">
            The authorization check is bound to PFCG authorization object `M_MATE_WRK` field `WERKS` for display activity (`03`).
          </p>
        </div>

        {/* Runtime Injected SQL */}
        <div className="border-2 border-ink bg-surface p-4 space-y-2">
          <div className="flex justify-between items-center border-b border-ink/40 pb-1">
            <h4 className="text-xs font-mono font-black uppercase tracking-wider">
              HANA SQL with Injected Filter
            </h4>
            <span className="text-[10px] font-mono bg-ink text-surface px-2 py-0.5 font-bold">
              AUTOMATIC INJECTION
            </span>
          </div>

          <pre className="p-3 bg-ink text-surface border-2 border-ink text-xs font-mono overflow-x-auto leading-relaxed max-h-48 overflow-y-auto">
            <code>{`SELECT
    Material,
    Description,
    Plant,
    StorageLocation,
    UnrestrictedStock,
    ValueEUR
FROM I_NovaPlantInventory
${selectedPersona.injected_where_clause};`}</code>
          </pre>
          <p className="text-[11px] font-mono text-muted">
            The developer wrote a plain `SELECT` statement. The HANA SQL optimizer transparently injected the DCL authorization filter.
          </p>
        </div>
      </div>

      {/* Resulting View Rows */}
      <div className="space-y-2">
        <h4 className="text-xs font-mono font-black uppercase text-muted tracking-wider">
          Query Output for {selectedPersona.name} ({visibleRows.length} Rows Returned)
        </h4>
        <div className="overflow-x-auto border-2 border-ink">
          <table className="w-full text-left text-xs font-mono">
            <thead className="bg-surface-raised border-b-2 border-ink">
              <tr>
                <th className="p-2">Material</th>
                <th className="p-2">Description</th>
                <th className="p-2">Plant</th>
                <th className="p-2">Storage Loc</th>
                <th className="p-2 text-right">Unrestricted Stock</th>
                <th className="p-2 text-right">Total Value (€)</th>
                <th className="p-2 text-center">Security Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-ink/20">
              {visibleRows.length === 0 ? (
                <tr>
                  <td colSpan={7} className="p-4 text-center text-danger font-bold italic bg-danger/5">
                    ACCESS DENIED: Zero rows returned. User lacks authorization object M_MATE_WRK for any plant.
                  </td>
                </tr>
              ) : (
                visibleRows.map((row, idx) => (
                  <tr key={idx} className="hover:bg-surface-raised">
                    <td className="p-2 font-bold">{row.material}</td>
                    <td className="p-2">{row.description}</td>
                    <td className="p-2 font-bold text-accent">{row.plant}</td>
                    <td className="p-2">{row.storage_loc}</td>
                    <td className="p-2 text-right">{row.unrestricted_stock} {row.unit}</td>
                    <td className="p-2 text-right">€{row.value_eur.toLocaleString()}</td>
                    <td className="p-2 text-center">
                      <span className="px-2 py-0.5 text-[10px] font-bold border border-ink bg-accent text-surface">
                        AUTHORIZED
                      </span>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Truthfulness Notice */}
      <div className="p-3 bg-surface border-2 border-ink text-[11px] font-mono text-muted flex items-center justify-between">
        <span>* Educational DCL security simulation modeling declarative row-level filtering in SAP S/4HANA.</span>
        <span className="font-bold text-ink">[LOCAL SIMULATION ONLY]</span>
      </div>
    </div>
  );
};
