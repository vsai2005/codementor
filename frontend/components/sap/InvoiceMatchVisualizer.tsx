"use client";

import React, { useState } from "react";

export interface ThreeWayMatchCase {
  case_id: string;
  po_number: string;
  po_quantity: number;
  po_unit_price: number;
  gr_number: string;
  gr_quantity: number;
  inv_number: string;
  inv_quantity: number;
  inv_unit_price: number;
  vendor_code: string;
  vendor_name: string;
  expected_block: boolean;
  block_reason?: string;
  tolerance_key: "PP" | "DQ" | "OK";
}

const SAMPLE_CASES: ThreeWayMatchCase[] = [
  {
    case_id: "match_clean",
    po_number: "4500019820",
    po_quantity: 500,
    po_unit_price: 50.0,
    gr_number: "5000018890",
    gr_quantity: 500,
    inv_number: "5105600112",
    inv_quantity: 500,
    inv_unit_price: 50.0,
    vendor_code: "VEND-101",
    vendor_name: "Rheinland Precision Optics",
    expected_block: false,
    tolerance_key: "OK",
  },
  {
    case_id: "price_variance",
    po_number: "4500019821",
    po_quantity: 200,
    po_unit_price: 50.0,
    gr_number: "5000018891",
    gr_quantity: 200,
    inv_number: "5105600113",
    inv_quantity: 200,
    inv_unit_price: 58.5, // 17% price variance (exceeds PP tolerance of 5%)
    vendor_code: "VEND-101",
    vendor_name: "Rheinland Precision Optics",
    expected_block: true,
    block_reason: "Price Variance Tolerance Key PP Exceeded (+17.0% vs PO). Invoice blocked with status 'R'.",
    tolerance_key: "PP",
  },
  {
    case_id: "quantity_mismatch",
    po_number: "4500019822",
    po_quantity: 400,
    po_unit_price: 50.0,
    gr_number: "5000018892",
    gr_quantity: 250, // Partial delivery
    inv_number: "5105600114",
    inv_quantity: 400, // Vendor billed for full 400!
    inv_unit_price: 50.0,
    vendor_code: "VEND-101",
    vendor_name: "Rheinland Precision Optics",
    expected_block: true,
    block_reason: "Quantity Variance Tolerance Key DQ Exceeded (Invoiced 400 EA vs Delivered 250 EA). Invoice blocked.",
    tolerance_key: "DQ",
  },
];

interface InvoiceMatchVisualizerProps {
  title?: string;
  instruction?: string;
}

export function InvoiceMatchVisualizer({
  title = "3-Way Match & Invoice Variance Simulator (MIRO)",
  instruction = "Compare Purchase Order (PO), Goods Receipt (GR), and Vendor Invoice line items. Observe how automated tolerance keys (PP, DQ) trigger Payment Block 'R' when variances exceed configured thresholds.",
}: InvoiceMatchVisualizerProps) {
  const [activeCaseId, setActiveCaseId] = useState<string>("match_clean");
  const [released, setReleased] = useState<boolean>(false);

  const activeCase = (SAMPLE_CASES.find((c) => c.case_id === activeCaseId) || SAMPLE_CASES[0])!;

  const poTotal = activeCase.po_quantity * activeCase.po_unit_price;
  const grTotal = activeCase.gr_quantity * activeCase.po_unit_price;
  const invTotal = activeCase.inv_quantity * activeCase.inv_unit_price;
  const priceDiff = activeCase.inv_unit_price - activeCase.po_unit_price;
  const qtyDiff = activeCase.inv_quantity - activeCase.gr_quantity;

  const handleSelectCase = (id: string) => {
    setActiveCaseId(id);
    setReleased(false);
  };

  const handleReleaseBlock = () => {
    setReleased(true);
  };

  return (
    <div className="border-3 border-ink bg-surface p-5 shadow-hard">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-2 mb-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="border border-ink bg-amber-200 text-amber-950 px-2 py-0.5 text-xs font-mono font-bold">
              [SIMULATION MODEL] 3-WAY MATCH
            </span>
            <span className="border border-ink bg-surface-raised px-2 py-0.5 text-xs font-mono font-bold text-ink">
              T-Code: MIRO • Company: NM01
            </span>
            <h3 className="text-base font-black text-ink">{title}</h3>
          </div>
          <p className="text-xs text-muted mt-1 leading-relaxed">{instruction}</p>
        </div>

        {/* Case Selector Tabs */}
        <div className="flex items-center border-2 border-ink bg-surface-raised p-1 gap-1">
          {SAMPLE_CASES.map((c) => (
            <button
              key={c.case_id}
              type="button"
              onClick={() => handleSelectCase(c.case_id)}
              className={`px-2.5 py-1 text-xs font-mono font-bold border border-ink transition-all focus-visible:ring-2 focus-visible:ring-ink ${
                activeCaseId === c.case_id
                  ? "bg-ink text-surface shadow-[1px_1px_0px_0px_rgba(0,0,0,1)]"
                  : "bg-surface hover:bg-surface-raised text-ink"
              }`}
            >
              {c.case_id === "match_clean"
                ? "1. Clean Match"
                : c.case_id === "price_variance"
                ? "2. Price Variance (PP)"
                : "3. Quantity Variance (DQ)"}
            </button>
          ))}
        </div>
      </div>

      {/* 3-Way Match Columns Comparison */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mb-5 font-mono text-xs">
        {/* PO Column */}
        <div className="border-2 border-ink bg-surface p-3 space-y-2">
          <div className="flex items-center justify-between border-b border-ink/40 pb-1">
            <span className="font-bold text-ink uppercase">1. Purchase Order</span>
            <span className="text-[10px] text-muted">EKKO/EKPO</span>
          </div>
          <div className="space-y-1">
            <div className="flex justify-between">
              <span className="text-muted">PO Number:</span>
              <span className="font-bold text-ink">{activeCase.po_number}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted">Quantity:</span>
              <span className="font-bold text-ink">{activeCase.po_quantity} EA</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted">Agreed Price:</span>
              <span className="font-bold text-ink">€{activeCase.po_unit_price.toFixed(2)}/EA</span>
            </div>
            <div className="flex justify-between border-t border-ink/20 pt-1">
              <span className="font-bold text-ink">PO Commitment:</span>
              <span className="font-black text-ink">€{poTotal.toLocaleString(undefined, { minimumFractionDigits: 2 })}</span>
            </div>
          </div>
        </div>

        {/* GR Column */}
        <div className="border-2 border-ink bg-surface p-3 space-y-2">
          <div className="flex items-center justify-between border-b border-ink/40 pb-1">
            <span className="font-bold text-ink uppercase">2. Goods Receipt</span>
            <span className="text-[10px] text-muted">MATDOC 101</span>
          </div>
          <div className="space-y-1">
            <div className="flex justify-between">
              <span className="text-muted">Material Doc:</span>
              <span className="font-bold text-ink">{activeCase.gr_number}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted">Quantity Recvd:</span>
              <span className={`font-bold ${qtyDiff > 0 ? "text-amber-700 underline" : "text-ink"}`}>
                {activeCase.gr_quantity} EA
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted">Valuation Price:</span>
              <span className="font-bold text-ink">€{activeCase.po_unit_price.toFixed(2)}/EA</span>
            </div>
            <div className="flex justify-between border-t border-ink/20 pt-1">
              <span className="font-bold text-ink">GR/IR Balance:</span>
              <span className="font-black text-ink">€{grTotal.toLocaleString(undefined, { minimumFractionDigits: 2 })}</span>
            </div>
          </div>
        </div>

        {/* Invoice Column */}
        <div className="border-2 border-ink bg-surface p-3 space-y-2">
          <div className="flex items-center justify-between border-b border-ink/40 pb-1">
            <span className="font-bold text-ink uppercase">3. Supplier Invoice</span>
            <span className="text-[10px] text-muted">RBKP/RSEG</span>
          </div>
          <div className="space-y-1">
            <div className="flex justify-between">
              <span className="text-muted">Invoice No:</span>
              <span className="font-bold text-ink">{activeCase.inv_number}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted">Billed Quantity:</span>
              <span className={`font-bold ${qtyDiff > 0 ? "text-rose-700 underline" : "text-ink"}`}>
                {activeCase.inv_quantity} EA
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted">Billed Price:</span>
              <span className={`font-bold ${priceDiff > 0 ? "text-rose-700 underline" : "text-ink"}`}>
                €{activeCase.inv_unit_price.toFixed(2)}/EA
              </span>
            </div>
            <div className="flex justify-between border-t border-ink/20 pt-1">
              <span className="font-bold text-ink">Vendor Claim:</span>
              <span className="font-black text-ink">€{invTotal.toLocaleString(undefined, { minimumFractionDigits: 2 })}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Verification Status Banner */}
      <div className="border-2 border-ink bg-surface-raised p-4 mb-4">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <span className="text-[10px] text-muted uppercase font-bold font-mono block">
              3-Way Match Verification Outcome
            </span>
            <div className="flex items-center gap-2 mt-1">
              {activeCase.expected_block && !released ? (
                <span className="bg-rose-500 text-white font-mono text-xs px-2 py-0.5 font-black uppercase">
                  ⛔ PAYMENT BLOCKED (STATUS R)
                </span>
              ) : (
                <span className="bg-emerald-500 text-white font-mono text-xs px-2 py-0.5 font-black uppercase">
                  ✓ VERIFIED & APPROVED FOR PAYMENT
                </span>
              )}
              <span className="text-xs text-ink font-bold">
                {activeCase.expected_block && !released
                  ? activeCase.block_reason
                  : released
                  ? "Payment Block 'R' manually released via MRBR after purchasing variance sign-off."
                  : "Zero variance detected. Document cleared automatically into Accounts Payable ledger."}
              </span>
            </div>
          </div>

          {activeCase.expected_block && !released && (
            <button
              type="button"
              onClick={handleReleaseBlock}
              className="border-2 border-ink bg-amber-400 px-3 py-1.5 text-xs font-black uppercase text-ink shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:bg-amber-300"
            >
              Simulate Release via MRBR
            </button>
          )}
        </div>
      </div>

      {/* Integration Invariant Note */}
      <div className="border border-ink bg-surface p-3 text-xs font-mono">
        <span className="font-bold text-ink block mb-1">Logistics Invoice Verification (LIV) Invariant:</span>
        <p className="text-muted leading-relaxed text-[11px]">
          If an invoice is blocked with status <strong>R</strong>, it posts to <code>ACDOCA</code> with an open item on the vendor subledger, but the payment program (<code>F110</code>) strictly ignores it until an authorized procurement specialist executes transaction <strong>MRBR</strong> (Release Blocked Invoices).
        </p>
      </div>
    </div>
  );
}
