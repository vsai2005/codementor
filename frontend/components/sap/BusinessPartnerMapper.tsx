"use client";

import React, { useState } from "react";

export interface BpRole {
  role_code: string;
  name: string;
  category: "General" | "Vendor" | "Customer";
  description: string;
  required_for: string;
}

const AVAILABLE_ROLES: BpRole[] = [
  {
    role_code: "000000",
    name: "Business Partner (General)",
    category: "General",
    description: "Central name, address, tax identification, and legal form.",
    required_for: "Baseline identity across all operations.",
  },
  {
    role_code: "FLVN00",
    name: "Supplier (Financial Accounting)",
    category: "Vendor",
    description: "Company Code data (reconciliation account, payment terms, withholding tax).",
    required_for: "Posting invoices in Financials (FI-AP).",
  },
  {
    role_code: "FLVN01",
    name: "Supplier (Purchasing)",
    category: "Vendor",
    description: "Purchasing Org data (order currency, Incoterms, partner schemas).",
    required_for: "Issuing Purchase Orders in Procurement (MM-PUR).",
  },
  {
    role_code: "FLCU00",
    name: "Customer (Financial Accounting)",
    category: "Customer",
    description: "Company Code data (reconciliation account, dunning, credit payment).",
    required_for: "Posting customer invoices & receivables in FI-AR.",
  },
  {
    role_code: "FLCU01",
    name: "Customer (Sales & Distribution)",
    category: "Customer",
    description: "Sales Org data (sales area, shipping conditions, pricing group).",
    required_for: "Creating Sales Orders and Deliveries in SD.",
  },
];

interface BusinessPartnerMapperProps {
  title?: string;
  instruction?: string;
}

export function BusinessPartnerMapper({
  title = "Business Partner (BP) & CVI Synchronization Cockpit",
  instruction = "In S/4HANA, the Business Partner is the mandatory single point of entry for all partner master data. Configure the required roles for Rheinland Precision Optics (VEND-101) to enable both purchasing and financial invoicing.",
}: BusinessPartnerMapperProps) {
  const [assignedRoles, setAssignedRoles] = useState<string[]>(["000000"]);
  const [cviSyncActive, setCviSyncActive] = useState<boolean>(false);
  const [syncResult, setSyncResult] = useState<string | null>(null);

  const toggleRole = (code: string) => {
    if (code === "000000") return; // 000000 is always assigned
    if (cviSyncActive) return; // Locked once synchronized
    setAssignedRoles((prev) =>
      prev.includes(code) ? prev.filter((r) => r !== code) : [...prev, code]
    );
  };

  const handleSyncCVI = () => {
    const hasFlvn00 = assignedRoles.includes("FLVN00");
    const hasFlvn01 = assignedRoles.includes("FLVN01");

    if (hasFlvn00 && hasFlvn01) {
      setCviSyncActive(true);
      setSyncResult("SUCCESS");
    } else {
      setCviSyncActive(true);
      setSyncResult("INCOMPLETE");
    }
  };

  const handleReset = () => {
    setAssignedRoles(["000000"]);
    setCviSyncActive(false);
    setSyncResult(null);
  };

  return (
    <div className="border-3 border-ink bg-surface p-5 shadow-hard">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-2 mb-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="border border-ink bg-amber-200 text-amber-950 px-2 py-0.5 text-xs font-mono font-bold">
              [SIMULATION MODEL] BP & CVI
            </span>
            <h3 className="text-base font-black text-ink">{title}</h3>
          </div>
          <p className="text-xs text-muted mt-1 leading-relaxed">{instruction}</p>
        </div>

        <div className="flex items-center gap-2 font-mono text-xs">
          <span className="border border-ink bg-surface-raised px-2.5 py-1 text-ink font-bold">
            Partner: BP-101 (Rheinland Optics)
          </span>
        </div>
      </div>

      {/* Role Selection Matrix */}
      <div className="border-2 border-ink bg-surface-raised p-4 mb-5">
        <div className="flex items-center justify-between text-xs font-mono font-bold text-muted mb-3">
          <span>Available S/4HANA Partner Roles</span>
          <span>Click to Assign / Unassign</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          {AVAILABLE_ROLES.map((role) => {
            const isAssigned = assignedRoles.includes(role.role_code);
            const isGeneral = role.role_code === "000000";

            return (
              <button
                key={role.role_code}
                type="button"
                aria-pressed={isAssigned}
                onClick={() => toggleRole(role.role_code)}
                disabled={cviSyncActive || isGeneral}
                className={`p-3 text-left border-2 border-ink transition-all focus-visible:ring-2 focus-visible:ring-ink ${
                  isAssigned
                    ? "bg-amber-100 shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] border-amber-900"
                    : "bg-surface hover:bg-surface-raised opacity-75"
                }`}
              >
                <div className="flex items-center justify-between text-xs font-mono font-bold mb-1">
                  <span className="text-ink">Role {role.role_code}</span>
                  <span
                    className={`px-1.5 py-0.5 text-[10px] font-bold border ${
                      isAssigned
                        ? "bg-emerald-100 text-emerald-950 border-emerald-500"
                        : "bg-muted/20 text-muted border-ink/20"
                    }`}
                  >
                    {isAssigned ? "✓ ASSIGNED" : "UNASSIGNED"}
                  </span>
                </div>
                <div className="text-xs font-black text-ink">{role.name}</div>
                <p className="text-[11px] text-muted mt-1 leading-snug font-medium">
                  {role.description}
                </p>
                <div className="text-[10px] text-amber-900 font-mono font-bold mt-2">
                  Scope: {role.required_for}
                </div>
              </button>
            );
          })}
        </div>

        {/* Action Controls */}
        <div className="mt-4 flex flex-wrap items-center justify-between gap-3 pt-3 border-t border-ink/20">
          <div className="text-xs font-mono font-bold text-ink">
            Active Roles: {assignedRoles.join(", ")}
          </div>

          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={handleSyncCVI}
              disabled={cviSyncActive}
              className="border-2 border-ink bg-amber-400 px-4 py-1.5 text-xs font-black uppercase text-ink shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:bg-amber-300 disabled:opacity-50 focus-visible:ring-2 focus-visible:ring-ink"
            >
              Simulate CVI Synchronization (MDS_LOAD_COCKPIT)
            </button>
            {cviSyncActive && (
              <button
                type="button"
                onClick={handleReset}
                className="border border-ink bg-surface px-3 py-1.5 text-xs font-mono font-bold text-ink hover:bg-surface-raised"
              >
                Reconfigure Roles ↻
              </button>
            )}
          </div>
        </div>
      </div>

      {/* CVI Synchronization Results */}
      {syncResult && (
        <div
          role="alert"
          className={`border-3 border-ink p-4 mb-5 ${
            syncResult === "SUCCESS"
              ? "bg-emerald-100 text-emerald-950"
              : "bg-rose-100 text-rose-950"
          }`}
        >
          <div className="text-xs font-mono font-bold uppercase mb-1">
            {syncResult === "SUCCESS"
              ? "✓ CVI Synchronization Complete — Tables Synchronized"
              : "⚠️ CVI Synchronization Failed — Incomplete Role Definition"}
          </div>
          <p className="text-xs leading-relaxed font-medium">
            {syncResult === "SUCCESS" ? (
              <>
                Customer-Vendor Integration successfully generated the underlying <strong>LFA1</strong> (General Supplier) and <strong>LFB1</strong> (Company Code NM01) views from the central <strong>BUT000</strong> Business Partner record. Nova Manufacturing can now issue POs and post vendor invoices without dual-entry errors.
              </>
            ) : (
              <>
                Procurement requires both <strong>FLVN00</strong> (Financial Accounting for invoice posting) and <strong>FLVN01</strong> (Purchasing Org for PO issuance). Missing either role causes Purchasing or Accounting transactions to terminate with <em>&quot;Supplier not maintained for company code/org&quot;</em> errors.
              </>
            )}
          </p>
        </div>
      )}

      {/* Conceptual Architectural Invariant */}
      <div className="border border-ink bg-surface p-3 text-xs font-mono">
        <span className="font-bold text-ink block mb-1">Why CVI was made mandatory:</span>
        <p className="text-muted leading-relaxed text-[11px]">
          In ECC, vendors and customers were maintained in separate transactions (XK01 vs XD01) with duplicate address, bank, and tax records. In S/4HANA, BUT000 stores master data once; CVI seamlessly populates legacy compatibility tables so existing programs run without modification.
        </p>
      </div>
    </div>
  );
}
