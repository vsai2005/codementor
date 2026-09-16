"use client";

import React, { useState } from "react";

export interface PricingCondition {
  step: number;
  condition_type: string;
  name: string;
  calculation_type: string;
  amount: number;
  currency: string;
  account_key: string;
  gl_account: string;
  gl_name: string;
  posting_type: "Debit" | "Credit" | "Statistical";
}

const DEFAULT_CONDITIONS: PricingCondition[] = [
  {
    step: 10,
    condition_type: "PR00",
    name: "Base Selling Price (Gross)",
    calculation_type: "Fixed Rate (€1,500 / EA x 30 EA)",
    amount: 45000,
    currency: "EUR",
    account_key: "ERL",
    gl_account: "410000",
    gl_name: "Domestic Sales Revenue",
    posting_type: "Credit",
  },
  {
    step: 20,
    condition_type: "K004",
    name: "Customer Volume Rebate / Discount",
    calculation_type: "Percentage (-6.67%)",
    amount: -3000,
    currency: "EUR",
    account_key: "ERS",
    gl_account: "420000",
    gl_name: "Sales Deductions / Discounts",
    posting_type: "Debit",
  },
  {
    step: 30,
    condition_type: "MWST",
    name: "Value Added Tax (Output VAT 19%)",
    calculation_type: "Percentage (19% on Net €42,000)",
    amount: 7980,
    currency: "EUR",
    account_key: "MWS",
    gl_account: "217000",
    gl_name: "Sales Tax Payable (Output VAT)",
    posting_type: "Credit",
  },
];

interface BillingAccountingFlowProps {
  title?: string;
  instruction?: string;
}

export function BillingAccountingFlow({
  title = "Customer Billing & Financial Account Determination (VKOA)",
  instruction = "Explore how SAP S/4HANA converts commercial SD pricing condition records into General Ledger accounting line items in ACDOCA via Account Keys (ERL, ERS, MWS).",
}: BillingAccountingFlowProps) {
  const [activeTab, setActiveTab] = useState<"pricing" | "vkoa" | "acdoca">("pricing");
  const [selectedConditionType, setSelectedConditionType] = useState<string>("PR00");
  const [quizAnswer, setQuizAnswer] = useState<string>("");
  const [quizSubmitted, setQuizSubmitted] = useState<boolean>(false);

  const netValue = 45000 - 3000;
  const taxValue = 7980;
  const grossInvoiceTotal = netValue + taxValue;

  const handleResetQuiz = () => {
    setQuizSubmitted(false);
    setQuizAnswer("");
  };

  return (
    <div className="border-3 border-ink bg-surface p-5 shadow-hard">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-2 mb-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="border border-ink bg-emerald-200 text-emerald-950 px-2 py-0.5 text-xs font-mono font-bold">
              [SIMULATION MODEL] SD-FI INTEGRATION
            </span>
            <span className="border border-ink bg-surface-raised px-2 py-0.5 text-xs font-mono font-bold text-ink">
              Billing Doc: #900055 • Type: F2
            </span>
            <h3 className="text-base font-black text-ink">{title}</h3>
          </div>
          <p className="text-xs text-muted mt-1 leading-relaxed">{instruction}</p>
        </div>

        <div className="text-xs font-mono bg-surface-raised border border-ink p-1.5">
          Payer: <strong className="text-indigo-700">CUST-501</strong> | Total: <strong className="text-emerald-800">€{grossInvoiceTotal.toLocaleString()}</strong>
        </div>
      </div>

      {/* Mode Navigation Tabs */}
      <div className="flex border-b-2 border-ink mb-4 gap-1">
        {[
          { id: "pricing", label: "1. SD Pricing Conditions" },
          { id: "vkoa", label: "2. Account Determination (VKOA)" },
          { id: "acdoca", label: "3. Resulting ACDOCA Journal" },
        ].map((tab) => (
          <button
            key={tab.id}
            type="button"
            onClick={() => setActiveTab(tab.id as "pricing" | "vkoa" | "acdoca")}
            className={`px-3 py-1.5 text-xs font-mono font-bold border-t-2 border-x-2 border-ink -mb-[2px] transition-all focus-visible:ring-2 focus-visible:ring-ink ${
              activeTab === tab.id
                ? "bg-surface text-ink border-b-2 border-b-surface font-black"
                : "bg-surface-raised text-muted hover:bg-surface"
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab 1: SD Pricing Conditions */}
      {activeTab === "pricing" && (
        <div className="space-y-4 mb-4">
          <div className="overflow-x-auto border-2 border-ink bg-surface">
            <table className="w-full text-xs font-mono text-left">
              <thead className="bg-surface-raised border-b-2 border-ink text-ink font-bold">
                <tr>
                  <th className="p-2">Step</th>
                  <th className="p-2">Condition</th>
                  <th className="p-2">Description</th>
                  <th className="p-2">Calculation</th>
                  <th className="p-2 text-right">Amount (EUR)</th>
                  <th className="p-2">Account Key</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-ink/20">
                {DEFAULT_CONDITIONS.map((cond) => (
                  <tr
                    key={cond.condition_type}
                    onClick={() => setSelectedConditionType(cond.condition_type)}
                    className={`cursor-pointer transition-colors ${
                      selectedConditionType === cond.condition_type
                        ? "bg-amber-100 font-bold"
                        : "hover:bg-surface-raised"
                    }`}
                  >
                    <td className="p-2">{cond.step}</td>
                    <td className="p-2 font-bold text-indigo-700">{cond.condition_type}</td>
                    <td className="p-2">{cond.name}</td>
                    <td className="p-2 text-muted">{cond.calculation_type}</td>
                    <td className={`p-2 text-right font-bold ${cond.amount < 0 ? "text-rose-700" : "text-ink"}`}>
                      €{cond.amount.toLocaleString()}
                    </td>
                    <td className="p-2">
                      <span className="px-1.5 py-0.5 border border-ink bg-surface text-ink font-bold">
                        {cond.account_key}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="p-3 border border-ink bg-surface-raised text-xs font-mono flex flex-wrap items-center justify-between gap-2">
            <div>Net Value: <strong>€{netValue.toLocaleString()}</strong> + Tax: <strong>€{taxValue.toLocaleString()}</strong></div>
            <div className="text-sm font-black text-ink">Total Commercial Receivable: €{grossInvoiceTotal.toLocaleString()}</div>
          </div>
        </div>
      )}

      {/* Tab 2: VKOA Account Determination Rules */}
      {activeTab === "vkoa" && (
        <div className="space-y-4 mb-4">
          <div className="border-2 border-ink bg-surface p-4 text-xs font-mono space-y-3">
            <h4 className="font-bold text-ink uppercase">VKOA Mapping Matrix (Chart of Accounts: NMCA)</h4>
            <p className="text-muted leading-relaxed font-sans text-xs">
              SAP pricing conditions do <strong>not</strong> hardcode General Ledger numbers. Instead, during billing creation (VF01), the engine evaluates Application <code>V</code>, Chart of Accounts <code>NMCA</code>, Sales Org <code>SO01</code>, and the <strong>Account Key</strong> defined in the Pricing Procedure.
            </p>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              <div className="p-3 border border-ink bg-surface-raised">
                <span className="text-[10px] uppercase font-bold text-muted block">Account Key: ERL</span>
                <span className="text-base font-black text-indigo-800">G/L 410000</span>
                <p className="text-[11px] font-sans text-ink mt-1">Domestic Sales Revenue (Credit)</p>
              </div>
              <div className="p-3 border border-ink bg-surface-raised">
                <span className="text-[10px] uppercase font-bold text-muted block">Account Key: ERS</span>
                <span className="text-base font-black text-rose-800">G/L 420000</span>
                <p className="text-[11px] font-sans text-ink mt-1">Customer Discounts / Deductions (Debit)</p>
              </div>
              <div className="p-3 border border-ink bg-surface-raised">
                <span className="text-[10px] uppercase font-bold text-muted block">Account Key: MWS</span>
                <span className="text-base font-black text-amber-800">G/L 217000</span>
                <p className="text-[11px] font-sans text-ink mt-1">Sales Output VAT (Credit)</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tab 3: Resulting ACDOCA Journal */}
      {activeTab === "acdoca" && (
        <div className="space-y-4 mb-4">
          <div className="border-2 border-ink bg-surface p-4 text-xs font-mono space-y-3">
            <div className="flex items-center justify-between border-b border-ink/20 pb-2">
              <span className="font-bold text-ink uppercase">ACDOCA FI Journal Document #900055</span>
              <span className="text-muted">Ledger: 0L (Leading) • Currency: EUR</span>
            </div>

            <div className="divide-y divide-ink/20">
              <div className="py-2 flex items-center justify-between">
                <div>
                  <span className="font-bold text-indigo-700">Line 001 | PK 01 (Debit Customer AR)</span>
                  <div className="text-muted text-[11px]">Subledger Account: CUST-501 (Reconciliation G/L: 121000 Trade Debtors)</div>
                </div>
                <div className="text-right font-black text-ink">Debit €49,980.00</div>
              </div>

              <div className="py-2 flex items-center justify-between">
                <div>
                  <span className="font-bold text-emerald-700">Line 002 | PK 50 (Credit Sales Revenue)</span>
                  <div className="text-muted text-[11px]">G/L Account: 410000 (VKOA Key: ERL via PR00 - K004)</div>
                </div>
                <div className="text-right font-black text-ink">Credit €42,000.00</div>
              </div>

              <div className="py-2 flex items-center justify-between">
                <div>
                  <span className="font-bold text-amber-700">Line 003 | PK 50 (Credit Output VAT)</span>
                  <div className="text-muted text-[11px]">G/L Account: 217000 (VKOA Key: MWS via MWST 19%)</div>
                </div>
                <div className="text-right font-black text-ink">Credit €7,980.00</div>
              </div>
            </div>

            <div className="border-t-2 border-ink pt-2 flex items-center justify-between font-bold">
              <span>Total Balance Verification:</span>
              <span className="text-emerald-700">Sum Debit €49,980.00 = Sum Credit €49,980.00 (Balanced ✓)</span>
            </div>
          </div>
        </div>
      )}

      {/* Practice Challenge */}
      <div className="border-2 border-ink bg-surface p-4">
        <fieldset>
          <legend className="text-xs font-mono font-bold uppercase text-ink mb-2">
            Integration Challenge: Pricing & General Ledger Determination
          </legend>
          <p className="text-xs text-ink mb-3 font-medium">
            Where does SAP get the General Ledger account number to credit sales revenue when a billing document is saved in transaction VF01?
          </p>

          <div className="space-y-2 mb-3">
            {[
              {
                id: "ans_vkoa",
                text: "From table VKOA (Revenue Account Determination), which maps the pricing condition's Account Key (e.g., ERL) together with Sales Org and Chart of Accounts to G/L 410000.",
                correct: true,
              },
              {
                id: "ans_manual",
                text: "The billing clerk types the 6-digit G/L account number manually into every line item in VF01.",
                correct: false,
              },
              {
                id: "ans_material",
                text: "The G/L account is hardcoded inside the customer's home address master record.",
                correct: false,
              },
            ].map((opt) => (
              <label
                key={opt.id}
                className={`flex items-start gap-2.5 p-2.5 border border-ink cursor-pointer text-xs font-medium transition-all focus-within:ring-2 focus-within:ring-ink ${
                  quizAnswer === opt.id
                    ? "bg-ink text-surface font-bold"
                    : "bg-surface-raised hover:bg-surface text-ink"
                }`}
              >
                <input
                  type="radio"
                  name="billing_flow_quiz"
                  value={opt.id}
                  checked={quizAnswer === opt.id}
                  disabled={quizSubmitted}
                  onChange={() => setQuizAnswer(opt.id)}
                  className="mt-0.5 accent-emerald-600"
                />
                <span>{opt.text}</span>
              </label>
            ))}
          </div>

          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <button
                type="button"
                onClick={() => setQuizSubmitted(true)}
                disabled={!quizAnswer || quizSubmitted}
                className="border-2 border-ink bg-emerald-400 px-4 py-1.5 text-xs font-black uppercase text-ink shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:bg-emerald-300 disabled:opacity-50"
              >
                Check Answer
              </button>
              {quizSubmitted && (
                <button
                  type="button"
                  onClick={handleResetQuiz}
                  className="border border-ink bg-surface px-3 py-1.5 text-xs font-mono font-bold text-ink hover:bg-surface-raised"
                >
                  Reset ↻
                </button>
              )}
            </div>

            {quizSubmitted && (
              <div
                role="alert"
                className={`text-xs font-bold px-3 py-1 border ${
                  quizAnswer === "ans_vkoa"
                    ? "bg-emerald-100 text-emerald-900 border-emerald-400"
                    : "bg-rose-100 text-rose-900 border-rose-400"
                }`}
              >
                {quizAnswer === "ans_vkoa"
                  ? "✓ Correct! VKOA provides the automated integration link between SD pricing and FI G/L accounts."
                  : "✗ Incorrect. Account determination in SAP SD is fully automated via table VKOA and account keys."}
              </div>
            )}
          </div>
        </fieldset>
      </div>
    </div>
  );
}
