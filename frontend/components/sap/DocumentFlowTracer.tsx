"use client";

import React, { useState } from "react";

export interface DocumentNode {
  doc_id: string;
  doc_type: string;
  doc_name: string;
  module: "SD" | "LE" | "MM" | "FI";
  status: "COMPLETED" | "CLEARED" | "OPEN" | "BEING_PROCESSED";
  date: string;
  created_by: string;
  amount?: string;
  underlying_table: string;
  preceding_doc?: string;
  subsequent_doc?: string;
  details: string;
}

const DEFAULT_FLOW: DocumentNode[] = [
  {
    doc_id: "10042",
    doc_type: "OR (Standard Order)",
    doc_name: "Sales Order",
    module: "SD",
    status: "COMPLETED",
    date: "2026-09-10",
    created_by: "SALES_OP01",
    amount: "€42,000.00",
    underlying_table: "VBAK / VBAP",
    subsequent_doc: "80019",
    details: "Customer CUST-501 (Nordics Industrial AB) ordered 30x DXTR-1000 robotics controllers. ATP check confirmed availability at Plant PL01.",
  },
  {
    doc_id: "80019",
    doc_type: "LF (Outbound Delivery)",
    doc_name: "Outbound Delivery",
    module: "LE",
    status: "COMPLETED",
    date: "2026-09-11",
    created_by: "WH_CLERK02",
    underlying_table: "LIKP / LIPS",
    preceding_doc: "10042",
    subsequent_doc: "490001",
    details: "Heidelberg shipping point picked and packed 30 units from Storage Location FG01 into handling units.",
  },
  {
    doc_id: "490001",
    doc_type: "WA (Goods Issue)",
    doc_name: "Post Goods Issue (PGI)",
    module: "MM",
    status: "COMPLETED",
    date: "2026-09-11",
    created_by: "WH_CLERK02",
    amount: "€25,500.00 (COGS)",
    underlying_table: "MATDOC",
    preceding_doc: "80019",
    subsequent_doc: "900055",
    details: "Inventory balance reduced by 30 units. Cost of Goods Sold (COGS) posted to ACDOCA in parallel with MATDOC single insert.",
  },
  {
    doc_id: "900055",
    doc_type: "F2 (Invoice)",
    doc_name: "Billing Document",
    module: "SD",
    status: "COMPLETED",
    date: "2026-09-12",
    created_by: "BILL_BATCH",
    amount: "€42,000.00",
    underlying_table: "VBRK / VBRP",
    preceding_doc: "80019",
    subsequent_doc: "100008",
    details: "Commercial invoice generated for CUST-501 with net 30 payment terms and 19% German VAT calculation.",
  },
  {
    doc_id: "100008",
    doc_type: "RV (Billing Doc Transfer)",
    doc_name: "Journal Entry",
    module: "FI",
    status: "COMPLETED",
    date: "2026-09-12",
    created_by: "BILL_BATCH",
    amount: "€49,980.00 (Gross)",
    underlying_table: "ACDOCA",
    preceding_doc: "900055",
    subsequent_doc: "100021",
    details: "Universal Journal entry generated synchronously: Dr Accounts Receivable (Customer CUST-501), Cr Revenue, Cr Output Tax.",
  },
  {
    doc_id: "100021",
    doc_type: "DZ (Customer Payment)",
    doc_name: "Incoming Payment & Clearing",
    module: "FI",
    status: "CLEARED",
    date: "2026-09-15",
    created_by: "BANK_FEED",
    amount: "€49,980.00",
    underlying_table: "ACDOCA",
    preceding_doc: "100008",
    details: "Bank electronic transfer cleared open items in ACDOCA. Zero residual open balance remains on customer subledger.",
  },
];

interface DocumentFlowTracerProps {
  flowNodes?: DocumentNode[];
  title?: string;
  instruction?: string;
}

export function DocumentFlowTracer({
  flowNodes = DEFAULT_FLOW,
  title = "S/4HANA End-to-End Document Flow Tracer",
  instruction = "Trace the chronological document lineage of an order at Nova Manufacturing. Inspect table VBFA references and see how logistics documents integrate seamlessly with the ACDOCA Universal Journal.",
}: DocumentFlowTracerProps) {
  const nodes = flowNodes.length > 0 ? flowNodes : DEFAULT_FLOW;
  const [selectedDocId, setSelectedDocId] = useState<string>(nodes[0]?.doc_id || "");

  const activeNode = nodes.find((n) => n.doc_id === selectedDocId) || nodes[0];

  const getModuleColor = (mod: string) => {
    switch (mod) {
      case "SD":
        return "bg-amber-100 text-amber-900 border-amber-400";
      case "LE":
        return "bg-sky-100 text-sky-900 border-sky-400";
      case "MM":
        return "bg-purple-100 text-purple-900 border-purple-400";
      case "FI":
        return "bg-emerald-100 text-emerald-900 border-emerald-400";
      default:
        return "bg-gray-100 text-gray-900 border-gray-400";
    }
  };

  return (
    <div className="border-3 border-ink bg-surface p-5 shadow-hard">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-2 mb-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="border border-ink bg-emerald-200 text-emerald-950 px-2 py-0.5 text-xs font-mono font-bold">
              [SIMULATION MODEL] VBFA → ACDOCA
            </span>
            <h3 className="text-base font-black text-ink">{title}</h3>
          </div>
          <p className="text-xs text-muted mt-1 leading-relaxed">{instruction}</p>
        </div>

        <div className="text-xs font-mono font-bold bg-surface-raised border border-ink p-1.5">
          Order: <span className="text-indigo-700">#10042 (CUST-501)</span>
        </div>
      </div>

      {/* Horizontal Flow Pipeline */}
      <div
        role="tablist"
        aria-label="Document Flow Chain"
        className="flex items-center gap-2 overflow-x-auto pb-2 mb-5 scrollbar-thin"
      >
        {nodes.map((node, i) => {
          const isSelected = node.doc_id === activeNode?.doc_id;
          return (
            <React.Fragment key={node.doc_id}>
              <button
                type="button"
                role="tab"
                aria-selected={isSelected}
                onClick={() => setSelectedDocId(node.doc_id)}
                className={`min-w-[140px] p-3 text-left border-2 border-ink transition-all focus-visible:ring-2 focus-visible:ring-ink shrink-0 ${
                  isSelected
                    ? "bg-amber-100 shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] border-amber-900 scale-[1.02]"
                    : "bg-surface hover:bg-surface-raised"
                }`}
              >
                <div className="flex items-center justify-between text-[10px] font-mono font-bold mb-1">
                  <span>Step {i + 1}</span>
                  <span className={`px-1 py-0.2 border ${getModuleColor(node.module)}`}>
                    {node.module}
                  </span>
                </div>
                <div className="text-xs font-black text-ink">{node.doc_name}</div>
                <div className="text-[10px] text-muted font-mono mt-1 truncate">
                  Doc #{node.doc_id}
                </div>
              </button>
              {i < nodes.length - 1 && (
                <span aria-hidden="true" className="font-mono text-ink font-bold text-sm shrink-0">
                  →
                </span>
              )}
            </React.Fragment>
          );
        })}
      </div>

      {/* Selected Document Detailed Inspection */}
      <div className="border-2 border-ink bg-surface-raised p-4 mb-4">
        <div className="flex flex-wrap items-center justify-between border-b border-ink/30 pb-3 mb-3 gap-2">
          <div>
            <div className="flex items-center gap-2">
              <span className={`px-2 py-0.5 text-xs font-mono font-bold border ${getModuleColor(activeNode?.module || "SD")}`}>
                {activeNode?.module || "SD"} Module
              </span>
              <h4 className="text-base font-black text-ink">
                {activeNode?.doc_name} (#{activeNode?.doc_id})
              </h4>
            </div>
            <div className="text-xs text-muted font-mono mt-1">
              Type: {activeNode?.doc_type} • Primary Table: <strong>{activeNode?.underlying_table}</strong>
            </div>
          </div>

          <div className="text-right font-mono text-xs">
            <span className="bg-emerald-100 text-emerald-950 border border-emerald-500 px-2 py-0.5 font-bold">
              {activeNode?.status}
            </span>
            {activeNode?.amount && (
              <div className="font-black text-ink mt-1">{activeNode?.amount}</div>
            )}
          </div>
        </div>

        <p className="text-xs text-ink leading-relaxed font-medium mb-3">
          {activeNode?.details}
        </p>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs font-mono">
          <div className="p-2 border border-ink/40 bg-surface">
            <span className="text-[10px] text-muted uppercase block">Created Date</span>
            <span className="font-bold text-ink">{activeNode?.date}</span>
          </div>
          <div className="p-2 border border-ink/40 bg-surface">
            <span className="text-[10px] text-muted uppercase block">Created By</span>
            <span className="font-bold text-ink">{activeNode?.created_by}</span>
          </div>
          <div className="p-2 border border-ink/40 bg-surface">
            <span className="text-[10px] text-muted uppercase block">Preceding Document</span>
            <span className="font-bold text-ink">{activeNode?.preceding_doc ? `#${activeNode.preceding_doc}` : "Initial Trigger"}</span>
          </div>
          <div className="p-2 border border-ink/40 bg-surface">
            <span className="text-[10px] text-muted uppercase block">Subsequent Document</span>
            <span className="font-bold text-ink">{activeNode?.subsequent_doc ? `#${activeNode.subsequent_doc}` : "End of Flow"}</span>
          </div>
        </div>
      </div>

      {/* Cross-Module Integration Key Takeaway */}
      <div className="border border-ink bg-surface p-3 text-xs font-mono">
        <span className="font-bold text-ink block mb-1">S/4HANA Integration Invariant:</span>
        <p className="text-muted leading-relaxed text-[11px]">
          Table <strong>VBFA</strong> stores predecessor/successor links across Sales and Logistics. When Goods Issue (Step 3) and Billing (Step 5) post, financial journal records are written directly into <strong>ACDOCA</strong> with the originating reference keys (<code>AWTYP = &#39;MKPF&#39; / &#39;VBRK&#39;</code>, <code>AWKEY</code>) and SD references (<code>VGBEL</code> / <code>VGPOS</code>), ensuring complete end-to-end traceability.
        </p>
      </div>
    </div>
  );
}
