"use client";

import React, { useState } from "react";

interface SampleRecord {
  order_id: string;
  customer: string;
  amount_eur: number;
  currency: string;
  days_open: number;
  discount_rate: number | null;
}

const SAMPLE_ORDERS: SampleRecord[] = [
  { order_id: "100045", customer: "CUST-501", amount_eur: 45000, currency: "EUR", days_open: 18, discount_rate: 0.05 },
  { order_id: "100046", customer: "CUST-502", amount_eur: 12500, currency: "EUR", days_open: 42, discount_rate: null },
  { order_id: "100047", customer: "CUST-503", amount_eur: 88000, currency: "EUR", days_open: 5, discount_rate: 0.10 },
  { order_id: "100048", customer: "CUST-504", amount_eur: 3200, currency: "EUR", days_open: 65, discount_rate: null },
];

interface CDSExpressionLabProps {
  title?: string;
  instruction?: string;
}

export const CDSExpressionLab: React.FC<CDSExpressionLabProps> = ({
  title = "CDS Expressions & Parameter Workbench",
  instruction = "Test in-database CASE statements, currency conversions, coalesce null-handling, and parameter evaluation.",
}) => {
  const [targetCurrency, setTargetCurrency] = useState<"USD" | "GBP" | "EUR">("USD");
  const [urgencyThreshold, setUrgencyThreshold] = useState<number>(30);
  const [activeTab, setActiveTab] = useState<"case" | "currency" | "parameters">("case");

  const rates: Record<string, number> = {
    USD: 1.08,
    GBP: 0.85,
    EUR: 1.0,
  };

  const getUrgencyBadge = (days: number) => {
    if (days > urgencyThreshold) {
      return { label: "CRITICAL_OVERDUE", color: "bg-danger text-surface" };
    }
    if (days > 14) {
      return { label: "IN_REVIEW", color: "bg-ink text-surface" };
    }
    return { label: "ON_TRACK", color: "bg-accent text-surface" };
  };

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

        {/* Lab Navigation Tabs */}
        <div className="flex border-2 border-ink">
          <button
            type="button"
            onClick={() => setActiveTab("case")}
            className={`px-3 py-1.5 text-xs font-mono font-bold transition-colors ${
              activeTab === "case" ? "bg-ink text-surface font-black" : "bg-surface text-ink hover:bg-surface-raised"
            }`}
          >
            1. CASE Expressions
          </button>
          <button
            type="button"
            onClick={() => setActiveTab("currency")}
            className={`px-3 py-1.5 text-xs font-mono font-bold border-l border-ink transition-colors ${
              activeTab === "currency" ? "bg-ink text-surface font-black" : "bg-surface text-ink hover:bg-surface-raised"
            }`}
          >
            2. Currency Conversion
          </button>
          <button
            type="button"
            onClick={() => setActiveTab("parameters")}
            className={`px-3 py-1.5 text-xs font-mono font-bold border-l border-ink transition-colors ${
              activeTab === "parameters" ? "bg-ink text-surface font-black" : "bg-surface text-ink hover:bg-surface-raised"
            }`}
          >
            3. Session Variables ($session)
          </button>
        </div>
      </div>

      {/* Controls & DDL Preview */}
      <div className="grid grid-cols-1 md:grid-cols-12 gap-6">
        {/* Dynamic Parameter Controls */}
        <div className="md:col-span-4 border-2 border-ink bg-surface-raised p-4 space-y-4">
          <h4 className="text-xs font-mono font-black uppercase text-ink tracking-wider border-b border-ink/40 pb-1">
            Execution Parameters
          </h4>

          {activeTab === "case" && (
            <div className="space-y-3">
              <label className="block text-xs font-mono font-bold text-ink">
                Urgency Threshold (Days Open):
                <span className="block text-lg font-black text-accent mt-0.5">{urgencyThreshold} days</span>
              </label>
              <input
                type="range"
                min={15}
                max={60}
                step={5}
                value={urgencyThreshold}
                onChange={(e) => setUrgencyThreshold(Number(e.target.value))}
                className="w-full accent-ink cursor-pointer"
              />
              <p className="text-[10px] font-mono text-muted">
                Adjusting threshold triggers real-time in-engine CASE re-evaluation across all sales documents.
              </p>
            </div>
          )}

          {activeTab === "currency" && (
            <div className="space-y-3">
              <label className="block text-xs font-mono font-bold text-ink">Target Currency (:p_target_curr)</label>
              <div className="grid grid-cols-3 gap-2">
                {(["USD", "GBP", "EUR"] as const).map((curr) => (
                  <button
                    key={curr}
                    type="button"
                    onClick={() => setTargetCurrency(curr)}
                    className={`p-2 text-xs font-mono font-bold border-2 border-ink transition-colors ${
                      targetCurrency === curr ? "bg-ink text-surface font-black" : "bg-surface hover:bg-surface-raised"
                    }`}
                  >
                    {curr}
                  </button>
                ))}
              </div>
              <p className="text-[10px] font-mono text-muted">
                HANA calls `currency_conversion(...)` pushdown table function referencing TCURR exchange rates.
              </p>
            </div>
          )}

          {activeTab === "parameters" && (
            <div className="space-y-2 text-xs font-mono">
              <div className="bg-surface p-2 border border-ink">
                <span className="text-[10px] text-muted block">$session.user</span>
                <span className="font-bold font-mono">NOVA_LEAD_ARCHITECT</span>
              </div>
              <div className="bg-surface p-2 border border-ink">
                <span className="text-[10px] text-muted block">$session.client</span>
                <span className="font-bold font-mono">100 (Development Golden)</span>
              </div>
              <div className="bg-surface p-2 border border-ink">
                <span className="text-[10px] text-muted block">$session.system_date</span>
                <span className="font-bold font-mono">2026-09-25</span>
              </div>
            </div>
          )}
        </div>

        {/* Code Snippet */}
        <div className="md:col-span-8 space-y-2">
          <div className="flex justify-between items-center bg-ink text-surface px-3 py-1 text-[10px] font-mono font-bold">
            <span>ABAP CDS View Entity Expression</span>
            <span>PUSHED DOWN TO HANA</span>
          </div>
          <pre className="p-3 bg-surface border-2 border-ink text-xs font-mono overflow-x-auto text-ink/90 leading-relaxed max-h-40 overflow-y-auto">
            <code>
              {activeTab === "case" &&
                `case
  when DaysOpen > ${urgencyThreshold} then 'CRITICAL_OVERDUE'
  when DaysOpen > 14 then 'IN_REVIEW'
  else 'ON_TRACK'
end as FulfillmentUrgency,
coalesce(DiscountRate, 0.00) as EffectiveDiscount`}
              {activeTab === "currency" &&
                `currency_conversion(
  amount             => NetAmount,
  source_currency    => Currency,
  target_currency    => $parameters.p_target_curr,
  exchange_rate_date => $session.system_date
) as ConvertedAmount`}
              {activeTab === "parameters" &&
                `with parameters
  p_target_curr : waers,
  p_cutoff_date : abap.dats
as select from I_SalesOrder
{
  key SalesOrder,
      $session.user        as CreatedBySessionUser,
      $session.system_date as EvaluationDate
}`}
            </code>
          </pre>
        </div>
      </div>

      {/* Evaluated Live Result Table */}
      <div className="space-y-2">
        <h4 className="text-xs font-mono font-black uppercase text-muted tracking-wider">
          Simulated Query Results (Evaluated in In-Memory Column Engine)
        </h4>
        <div className="overflow-x-auto border-2 border-ink">
          <table className="w-full text-left text-xs font-mono">
            <thead className="bg-surface-raised border-b-2 border-ink">
              <tr>
                <th className="p-2">Order #</th>
                <th className="p-2">Customer</th>
                <th className="p-2 text-right">Raw EUR Amount</th>
                <th className="p-2 text-right">Effective Discount (Coalesced)</th>
                <th className="p-2 text-center">Days Open</th>
                <th className="p-2 text-center">Fulfillment Urgency (CASE)</th>
                <th className="p-2 text-right">Converted ({targetCurrency})</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-ink/20">
              {SAMPLE_ORDERS.map((o) => {
                const urgency = getUrgencyBadge(o.days_open);
                const convAmount = o.amount_eur * (rates[targetCurrency] || 1.0);
                const effDiscount = (o.discount_rate ?? 0.0) * 100;

                return (
                  <tr key={o.order_id} className="hover:bg-surface-raised">
                    <td className="p-2 font-bold">{o.order_id}</td>
                    <td className="p-2">{o.customer}</td>
                    <td className="p-2 text-right">€{o.amount_eur.toLocaleString()}</td>
                    <td className="p-2 text-right">{effDiscount.toFixed(1)}%</td>
                    <td className="p-2 text-center">{o.days_open} d</td>
                    <td className="p-2 text-center">
                      <span className={`px-2 py-0.5 text-[10px] font-bold border border-ink ${urgency.color}`}>
                        {urgency.label}
                      </span>
                    </td>
                    <td className="p-2 text-right font-black">
                      {targetCurrency === "USD" ? "$" : targetCurrency === "GBP" ? "£" : "€"}
                      {convAmount.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* Truthfulness Notice */}
      <div className="p-3 bg-surface border-2 border-ink text-[11px] font-mono text-muted flex items-center justify-between">
        <span>* Live educational simulation demonstrating CDS expression pushdown and parameter propagation.</span>
        <span className="font-bold text-ink">[LOCAL SIMULATION ONLY]</span>
      </div>
    </div>
  );
};
