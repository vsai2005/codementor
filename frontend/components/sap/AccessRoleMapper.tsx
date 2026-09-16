"use client";

import React, { useState } from "react";

export interface RoleAssignment {
  role_id: string;
  role_name: string;
  catalogs: string[];
  assigned_spaces: string[];
  has_sod_conflict: boolean;
  sod_warning?: string;
}

const DEFAULT_ASSIGNMENTS: RoleAssignment[] = [
  {
    role_id: "SAP_BR_PURCHASER",
    role_name: "Strategic Purchaser",
    catalogs: ["SAP_PRC_BC_PURCHASER_STRAT", "SAP_PRC_BC_PO_MANAGE"],
    assigned_spaces: ["Purchasing Operations", "Supplier Collaboration"],
    has_sod_conflict: false,
  },
  {
    role_id: "SAP_BR_AP_ACCOUNTANT",
    role_name: "Accounts Payable Accountant",
    catalogs: ["SAP_FIN_BC_AP_INVOICES", "SAP_FIN_BC_AP_PAYMENTS"],
    assigned_spaces: ["Payables Management", "Payment Processing"],
    has_sod_conflict: true,
    sod_warning: "Segregation of Duties (SoD) Risk: User currently holds both PO issuance and direct vendor payment release authorities.",
  },
  {
    role_id: "SAP_BR_INTERNAL_AUDITOR",
    role_name: "Internal Auditor",
    catalogs: ["SAP_AUD_BC_TRACE", "SAP_AUD_BC_RECONCILIATION"],
    assigned_spaces: ["Compliance & Audit"],
    has_sod_conflict: false,
  },
];

interface AccessRoleMapperProps {
  title?: string;
  instruction?: string;
}

export function AccessRoleMapper({
  title = "Fiori Role Architecture & Segregation of Duties (SoD)",
  instruction = "Audit access permissions for a logistics specialist at Nova Manufacturing. Reconcile Business Roles, Fiori Catalogs, Spaces, and resolve critical Segregation of Duties conflicts.",
}: AccessRoleMapperProps) {
  const [roles, setRoles] = useState<RoleAssignment[]>(DEFAULT_ASSIGNMENTS);
  const [selectedRole, setSelectedRole] = useState<string>("SAP_BR_AP_ACCOUNTANT");
  const [sodResolved, setSodResolved] = useState<boolean>(false);

  const activeRole = roles.find((r) => r.role_id === selectedRole) || roles[0];

  const handleRevokePayment = () => {
    setRoles((prev) =>
      prev.map((r) =>
        r.role_id === "SAP_BR_AP_ACCOUNTANT"
          ? {
              ...r,
              catalogs: ["SAP_FIN_BC_AP_INVOICES"],
              has_sod_conflict: false,
              sod_warning: undefined,
            }
          : r
      )
    );
    setSodResolved(true);
  };

  const handleReset = () => {
    setRoles(DEFAULT_ASSIGNMENTS);
    setSodResolved(false);
  };

  return (
    <div className="border-3 border-ink bg-surface p-5 shadow-hard">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-2 mb-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="border border-ink bg-rose-200 text-rose-950 px-2 py-0.5 text-xs font-mono font-bold">
              [SIMULATION MODEL] IAM & GOVERNANCE
            </span>
            <h3 className="text-base font-black text-ink">{title}</h3>
          </div>
          <p className="text-xs text-muted mt-1 leading-relaxed">{instruction}</p>
        </div>

        <div className="text-xs font-mono font-bold bg-surface-raised border border-ink p-1.5">
          User: <span className="text-purple-700">ANNA.MULLER (Plant PL01)</span>
        </div>
      </div>

      {/* Role Selector Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 mb-5">
        {roles.map((r) => {
          const isSelected = r.role_id === selectedRole;
          return (
            <button
              key={r.role_id}
              type="button"
              aria-pressed={isSelected}
              onClick={() => setSelectedRole(r.role_id)}
              className={`p-3 text-left border-2 border-ink transition-all focus-visible:ring-2 focus-visible:ring-ink ${
                isSelected
                  ? "bg-amber-100 shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] border-amber-900"
                  : "bg-surface hover:bg-surface-raised"
              }`}
            >
              <div className="flex items-center justify-between font-mono text-xs font-bold mb-1">
                <span className="truncate max-w-[130px]">{r.role_id}</span>
                {r.has_sod_conflict && (
                  <span className="bg-rose-100 text-rose-900 border border-rose-400 px-1 py-0.2 text-[10px]">
                    SoD ALERT
                  </span>
                )}
              </div>
              <div className="text-xs font-black text-ink">{r.role_name}</div>
              <div className="text-[10px] text-muted mt-1 font-mono">
                {r.catalogs.length} Catalogs • {r.assigned_spaces.length} Spaces
              </div>
            </button>
          );
        })}
      </div>

      {/* Role Detail Inspector */}
      <div className="border-2 border-ink bg-surface-raised p-4 mb-5 space-y-3">
        <div className="flex items-center justify-between border-b border-ink pb-2">
          <div>
            <h4 className="text-sm font-black text-ink">{activeRole?.role_name} ({activeRole?.role_id})</h4>
            <span className="text-xs text-muted">Role-Based Access Control Specification</span>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs font-mono">
          <div className="p-3 border border-ink bg-surface">
            <span className="text-[10px] uppercase text-muted block mb-1">Assigned Business Spaces & Pages</span>
            <ul className="list-disc pl-4 space-y-1">
              {activeRole?.assigned_spaces.map((space) => (
                <li key={space} className="font-bold text-ink">{space}</li>
              ))}
            </ul>
          </div>

          <div className="p-3 border border-ink bg-surface">
            <span className="text-[10px] uppercase text-muted block mb-1">Assigned Business Catalogs (PFCG Authorization)</span>
            <ul className="list-disc pl-4 space-y-1">
              {activeRole?.catalogs.map((cat) => (
                <li key={cat} className="font-bold text-ink">{cat}</li>
              ))}
            </ul>
          </div>
        </div>

        {/* SoD Alert & Action */}
        {activeRole?.has_sod_conflict && (
          <div role="alert" className="border-2 border-rose-500 bg-rose-50 p-3 text-xs text-rose-950 space-y-2">
            <div className="font-mono font-bold uppercase text-rose-900">
              🚨 Segregation of Duties (SoD) Conflict Detected
            </div>
            <p className="font-medium leading-relaxed">
              {activeRole?.sod_warning}
            </p>
            <button
              type="button"
              onClick={handleRevokePayment}
              className="border-2 border-ink bg-rose-500 hover:bg-rose-600 text-white font-black uppercase text-xs px-3 py-1.5 shadow-[2px_2px_0px_0px_rgba(0,0,0,1)]"
            >
              Simulate Remediation: Reassign to Restricted Role (SAP_BR_AP_CLERK_INVOICES)
            </button>
          </div>
        )}

        {sodResolved && !activeRole?.has_sod_conflict && selectedRole === "SAP_BR_AP_ACCOUNTANT" && (
          <div role="alert" className="border-2 border-emerald-500 bg-emerald-50 p-3 text-xs text-emerald-950 font-bold flex flex-wrap items-center justify-between gap-2">
            <span>✓ SoD Conflict Cleared! Anna retains invoice verification authority without dual control over disbursement release.</span>
            <button
              type="button"
              onClick={handleReset}
              className="border border-ink bg-surface px-2.5 py-1 text-[11px] font-mono font-bold text-ink hover:bg-surface-raised"
            >
              Reset Audit ↻
            </button>
          </div>
        )}
      </div>

      {/* Architectural Rule Callout */}
      <div className="border border-ink bg-surface p-3 text-xs font-mono">
        <span className="font-bold text-ink block mb-1">Fiori Launchpad Architecture Hierarchy:</span>
        <div className="text-[11px] text-muted flex flex-wrap items-center gap-1.5">
          <span className="bg-surface-raised px-1.5 py-0.5 border">Business Role (PFCG)</span>
          <span>→</span>
          <span className="bg-surface-raised px-1.5 py-0.5 border">Business Space (Domain Navigation)</span>
          <span>→</span>
          <span className="bg-surface-raised px-1.5 py-0.5 border">Business Page (Topic Section)</span>
          <span>→</span>
          <span className="bg-surface-raised px-1.5 py-0.5 border">Business Catalog (Tile + Authorization Object)</span>
        </div>
      </div>
    </div>
  );
}
