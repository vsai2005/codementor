"use client";

import React, { useState } from "react";

interface CDSConceptMapperProps {
  title?: string;
  instruction?: string;
}

export function CDSConceptMapper({
  title = "Core Data Services (CDS) View Entity & Code Pushdown",
  instruction = "Explore ABAP Core Data Services (CDS), the cornerstone of modern S/4HANA semantic data modeling. Compare the code-to-data pushdown philosophy against legacy application loops.",
}: CDSConceptMapperProps) {
  const [activeLayer, setActiveLayer] = useState<"BASIC" | "COMPOSITE" | "CONSUMPTION">("COMPOSITE");
  const [activeParadigm, setActiveParadigm] = useState<"PUSHDOWN" | "LEGACY">("PUSHDOWN");
  const [quizAnswer, setQuizAnswer] = useState<string>("");
  const [quizEvaluated, setQuizEvaluated] = useState<boolean>(false);

  const getCodeSnippet = () => {
    switch (activeLayer) {
      case "BASIC":
        return `@AbapCatalog.viewEnhancementCategory: [#NONE]
@AccessControl.authorizationCheck: #CHECK
@EndUserText.label: 'Basic Interface View for Materials'
define view entity I_MaterialBasic
  as select from mara
{
  key matnr as Material,
      matkl as MaterialGroup,
      meins as BaseUnitOfMeasure,
      brgew as GrossWeight
}`;
      case "COMPOSITE":
        return `@AbapCatalog.viewEnhancementCategory: [#NONE]
@AccessControl.authorizationCheck: #CHECK
@EndUserText.label: 'Composite View: Production Stock Cube'
@Analytics.dataCategory: #CUBE
define view entity I_ProductionStockCube
  as select from matdoc
  association [1..1] to I_MaterialBasic as _Material
    on $projection.Material = _Material.Material
{
  key matnr as Material,
  key werks as Plant,
  key lgort as StorageLocation,
      @Semantics.quantity.unitOfMeasure: 'BaseUnit'
      sum(menge) as TotalStockQuantity,
      meins      as BaseUnit,
      _Material
}`;
      case "CONSUMPTION":
        return `@AbapCatalog.viewEnhancementCategory: [#NONE]
@AccessControl.authorizationCheck: #CHECK
@EndUserText.label: 'Consumption View: Nova Stock KPI'
@Analytics.query: true
// Consumed via InA Protocol / Multidimensional Reporting or exposed via RAP Service Definition
define view entity C_NovaStockKPI
  as select from I_ProductionStockCube
{
  key Material,
  key Plant,
      TotalStockQuantity,
      BaseUnit,
      _Material.MaterialGroup as Group
}`;
    }
  };

  return (
    <div className="border-3 border-ink bg-surface p-5 shadow-hard">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-2 mb-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="border border-ink bg-indigo-200 text-indigo-950 px-2 py-0.5 text-xs font-mono font-bold">
              [SIMULATION MODEL] ABAP CDS
            </span>
            <h3 className="text-base font-black text-ink">{title}</h3>
          </div>
          <p className="text-xs text-muted mt-1 leading-relaxed">{instruction}</p>
        </div>

        {/* Layer Tabs */}
        <div className="flex items-center border-2 border-ink bg-surface-raised p-1 gap-1">
          {(["BASIC", "COMPOSITE", "CONSUMPTION"] as const).map((layer) => (
            <button
              key={layer}
              type="button"
              onClick={() => setActiveLayer(layer)}
              className={`px-2.5 py-1 text-xs font-mono font-bold border border-ink transition-all focus-visible:ring-2 focus-visible:ring-ink focus-visible:outline-none ${
                activeLayer === layer
                  ? "bg-ink text-surface shadow-[1px_1px_0px_0px_rgba(0,0,0,1)]"
                  : "bg-surface hover:bg-surface-raised text-ink"
              }`}
            >
              {layer === "BASIC" ? "1. Basic (I_)" : layer === "COMPOSITE" ? "2. Composite (I_)" : "3. Consumption (C_)"}
            </button>
          ))}
        </div>
      </div>

      {/* Code Pushdown vs Legacy Comparison */}
      <div className="mb-4 flex items-center justify-between border-2 border-ink bg-surface-raised p-2">
        <span className="text-xs font-mono font-bold text-muted uppercase">Execution Strategy:</span>
        <div className="flex gap-1">
          <button
            type="button"
            onClick={() => setActiveParadigm("PUSHDOWN")}
            className={`px-3 py-1 text-xs font-bold border border-ink ${
              activeParadigm === "PUSHDOWN"
                ? "bg-emerald-300 text-emerald-950 font-black shadow-[1px_1px_0px_0px_rgba(0,0,0,1)]"
                : "bg-surface text-ink hover:bg-surface-raised"
            }`}
          >
            ✓ Modern S/4HANA: Code Pushdown (HANA DB)
          </button>
          <button
            type="button"
            onClick={() => setActiveParadigm("LEGACY")}
            className={`px-3 py-1 text-xs font-bold border border-ink ${
              activeParadigm === "LEGACY"
                ? "bg-rose-300 text-rose-950 font-black shadow-[1px_1px_0px_0px_rgba(0,0,0,1)]"
                : "bg-surface text-ink hover:bg-surface-raised"
            }`}
          >
            Legacy ECC: Data-to-Code (App Server Loop)
          </button>
        </div>
      </div>

      {/* Main Grid: Code Inspector + VDM Explanation */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-4 mb-5">
        {/* Code Editor Preview */}
        <div className="lg:col-span-7 border-2 border-ink bg-neutral-900 text-neutral-100 p-4 font-mono text-xs shadow-inner">
          <div className="flex items-center justify-between border-b border-neutral-700 pb-2 mb-3 text-[11px] text-neutral-400">
            <span>ADT Eclipse Editor • View Entity Syntax</span>
            <span className="text-amber-400">Status: Active</span>
          </div>

          <pre className="overflow-x-auto text-[11px] leading-relaxed text-emerald-400">
            <code>{getCodeSnippet()}</code>
          </pre>
        </div>

        {/* Semantic Layer Card */}
        <div className="lg:col-span-5 border-2 border-ink bg-surface p-4">
          <div className="border-b border-ink pb-2 mb-3">
            <span className="text-xs font-mono font-bold uppercase text-muted">
              VDM Architecture Role
            </span>
            <h4 className="text-sm font-black text-ink">
              {activeLayer === "BASIC" && "Basic Interface View (P_ / I_)"}
              {activeLayer === "COMPOSITE" && "Composite View (I_ Cube)"}
              {activeLayer === "CONSUMPTION" && "Consumption View (C_ Query / OData)"}
            </h4>
          </div>

          <div className="space-y-3 text-xs">
            <p className="text-ink leading-relaxed font-medium">
              {activeLayer === "BASIC" &&
                "Directly models raw database tables (e.g. MARA, BUT000, ACDOCA) without heavy joins or business logic. Provides stable, reusable atomic building blocks for the entire enterprise."}
              {activeLayer === "COMPOSITE" &&
                "Combines multiple basic views via associations. Performs joins, aggregations (SUM, AVG), and encapsulates core business logic. Annotated with @Analytics.dataCategory: #CUBE for reporting engines."}
              {activeLayer === "CONSUMPTION" &&
                "The top-most user-facing layer. Designed specifically for UI consumption (Fiori Elements, SAP Analytics Cloud). Published directly as an OData V4 service without writing manual ABAP gateway classes."}
            </p>

            <div className="p-2.5 border border-ink bg-surface-raised font-mono text-[11px]">
              <span className="text-muted block text-[10px] uppercase font-bold">Paradigm Impact</span>
              {activeParadigm === "PUSHDOWN" ? (
                <span className="text-emerald-900 font-bold">
                  ⚡ Calculations pushed down to HANA in-memory engine. Only the resulting aggregated KPI rows cross the network to the application server.
                </span>
              ) : (
                <span className="text-rose-900 font-bold">
                  ⚠️ 2,000,000 raw table rows transferred across the network to AS ABAP; application server loops over rows in memory to compute sum.
                </span>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Practice Challenge */}
      <div className="border-2 border-ink bg-surface-raised p-4">
        <fieldset>
          <legend className="text-xs font-mono font-bold uppercase text-ink mb-2">
            Verification Challenge: CDS Architecture Invariant
          </legend>
          <p className="text-xs text-ink mb-3 font-medium">
            What is the key difference between a modern <strong>CDS View Entity</strong> (introduced in S/4HANA 2020+) and a legacy Classical CDS DDIC-based view?
          </p>

          <div className="space-y-2 mb-3">
            {[
              {
                id: "ans_a",
                text: "A View Entity creates no redundant SQL DDIC view in the ABAP dictionary, eliminates activation overhead, and executes pure HANA native pushdown.",
                correct: true,
              },
              {
                id: "ans_b",
                text: "A View Entity replaces the underlying database table completely and permanently stores cached query results in the application server buffer.",
                correct: false,
              },
              {
                id: "ans_c",
                text: "A View Entity requires explicit SQL DDL CREATE TABLE statements to be manually run by database administrators in the HANA studio.",
                correct: false,
              },
            ].map((opt) => (
              <label
                key={opt.id}
                className={`flex items-start gap-2.5 p-2.5 border border-ink cursor-pointer text-xs font-medium transition-all focus-within:ring-2 focus-within:ring-ink ${
                  quizAnswer === opt.id
                    ? "bg-ink text-surface font-bold"
                    : "bg-surface hover:bg-surface-raised text-ink"
                }`}
              >
                <input
                  type="radio"
                  name="cds_practice_quiz"
                  value={opt.id}
                  checked={quizAnswer === opt.id}
                  disabled={quizEvaluated}
                  onChange={() => setQuizAnswer(opt.id)}
                  className="mt-0.5 accent-indigo-600"
                />
                <span>{opt.text}</span>
              </label>
            ))}
          </div>

          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <button
                type="button"
                onClick={() => setQuizEvaluated(true)}
                disabled={!quizAnswer || quizEvaluated}
                className="border-2 border-ink bg-indigo-400 px-4 py-1.5 text-xs font-black uppercase text-ink shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:bg-indigo-300 disabled:opacity-50"
              >
                Check Answer
              </button>
              {quizEvaluated && (
                <button
                  type="button"
                  onClick={() => {
                    setQuizEvaluated(false);
                    setQuizAnswer("");
                  }}
                  className="border border-ink bg-surface px-3 py-1.5 text-xs font-mono font-bold text-ink hover:bg-surface-raised"
                >
                  Reset ↻
                </button>
              )}
            </div>

            {quizEvaluated && (
              <div
                role="alert"
                className={`text-xs font-bold px-3 py-1 border ${
                  quizAnswer === "ans_a"
                    ? "bg-emerald-100 text-emerald-900 border-emerald-400"
                    : "bg-rose-100 text-rose-900 border-rose-400"
                }`}
              >
                {quizAnswer === "ans_a"
                  ? "✓ Correct! View Entities cleanly separate ABAP semantics from unnecessary DDIC artifacts."
                  : "✗ Incorrect. Review the evolution from DDIC views to CDS View Entities."}
              </div>
            )}
          </div>
        </fieldset>
      </div>
    </div>
  );
}
