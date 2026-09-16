"use client";

import React, { useState } from "react";

interface AnnotationDefinition {
  id: string;
  name: string;
  category: "@Semantics" | "@Analytics" | "@EndUserText" | "@Consumption" | "@AccessControl";
  sample_syntax: string;
  consumer_framework: "Fiori Elements UI" | "Analytical Engine (SADL)" | "Compiler / DCL" | "Value Help";
  architectural_impact: string;
  risk_if_omitted: string;
}

const ANNOTATIONS: AnnotationDefinition[] = [
  {
    id: "ann-sem-amt",
    name: "@Semantics.amount.currencyCode",
    category: "@Semantics",
    sample_syntax: `@Semantics.amount.currencyCode: 'TransactionCurrency'
NetAmount : abap.curr(15,2);`,
    consumer_framework: "Fiori Elements UI",
    architectural_impact: "Binds monetary values to a designated currency code field in the same projection list. Enforces decimal formatting.",
    risk_if_omitted: "Fiori displays raw unformatted decimals; multi-currency totals will erroneously aggregate without exchange rate conversion!",
  },
  {
    id: "ann-sem-qty",
    name: "@Semantics.quantity.unitOfMeasure",
    category: "@Semantics",
    sample_syntax: `@Semantics.quantity.unitOfMeasure: 'OrderQuantityUnit'
OrderQuantity : abap.quan(13,3);`,
    consumer_framework: "Analytical Engine (SADL)",
    architectural_impact: "Binds physical quantities to their unit of measure (e.g. EA, KG, LITER), enabling unit-safe rollups.",
    risk_if_omitted: "Quantities in differing units (e.g. 10 Pallets + 50 Each) get summed together incorrectly as 60.",
  },
  {
    id: "ann-ana-cube",
    name: "@Analytics.dataCategory: #CUBE",
    category: "@Analytics",
    sample_syntax: `@Analytics.dataCategory: #CUBE
define view entity I_RoboticsProductionCube ...`,
    consumer_framework: "Analytical Engine (SADL)",
    architectural_impact: "Registers the CDS entity as a multidimensional fact cube with measures and dimension associations.",
    risk_if_omitted: "Cannot be consumed as an analytical source in SAP Analytics Cloud or S/4HANA analytical queries.",
  },
  {
    id: "ann-ui-label",
    name: "@EndUserText.label",
    category: "@EndUserText",
    sample_syntax: `@EndUserText.label: 'Manufacturing Actual Cost Analysis'
define view entity ...`,
    consumer_framework: "Fiori Elements UI",
    architectural_impact: "Provides human-readable, translatable text strings linked to ABAP text repositories (SE63).",
    risk_if_omitted: "UI headers fall back to raw technical field names (e.g. 'NETWR', 'MATNR') degrading user experience.",
  },
  {
    id: "ann-acc-check",
    name: "@AccessControl.authorizationCheck: #CHECK",
    category: "@AccessControl",
    sample_syntax: `@AccessControl.authorizationCheck: #CHECK
define view entity I_PlantInventory ...`,
    consumer_framework: "Compiler / DCL",
    architectural_impact: "Directs the ABAP runtime to enforce corresponding DCL access control roles on database select operations.",
    risk_if_omitted: "Security vulnerability! If set to #NOT_ALLOWED or omitted carelessly, unauthorized users see restricted rows across plants.",
  },
];

interface AnnotationInspectorProps {
  title?: string;
  instruction?: string;
}

export const AnnotationInspector: React.FC<AnnotationInspectorProps> = ({
  title = "CDS Annotations Catalog & Consumer Framework Inspector",
  instruction = "Inspect how annotations drive analytical engines, Fiori Elements, and security runtimes.",
}) => {
  const [selectedAnn, setSelectedAnn] = useState<AnnotationDefinition>(ANNOTATIONS[0]!);
  const [activeCategory, setActiveCategory] = useState<string>("ALL");

  const categories = ["ALL", "@Semantics", "@Analytics", "@EndUserText", "@AccessControl"];
  const filtered =
    activeCategory === "ALL" ? ANNOTATIONS : ANNOTATIONS.filter((a) => a.category === activeCategory);

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

        {/* Category Tabs */}
        <div className="flex flex-wrap border-2 border-ink">
          {categories.map((cat) => (
            <button
              key={cat}
              type="button"
              onClick={() => setActiveCategory(cat)}
              className={`px-3 py-1.5 text-xs font-mono font-bold transition-colors border-r border-ink last:border-r-0 ${
                activeCategory === cat ? "bg-ink text-surface font-black" : "bg-surface text-ink hover:bg-surface-raised"
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      {/* Grid Inspector */}
      <div className="grid grid-cols-1 md:grid-cols-12 gap-6">
        {/* Annotation Badges List */}
        <div className="md:col-span-5 space-y-2">
          <h4 className="text-xs font-mono font-black uppercase text-muted tracking-wider">
            Annotations ({filtered.length})
          </h4>
          <div className="space-y-2">
            {filtered.map((ann) => (
              <button
                key={ann.id}
                type="button"
                onClick={() => setSelectedAnn(ann)}
                className={`w-full text-left p-3 border-2 border-ink transition-all ${
                  selectedAnn.id === ann.id
                    ? "bg-ink text-surface shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] translate-x-1"
                    : "bg-surface hover:bg-surface-raised"
                }`}
              >
                <div className="flex items-center justify-between text-xs font-mono">
                  <span className="font-black truncate">{ann.name}</span>
                  <span
                    className={`px-1.5 py-0.5 text-[10px] font-bold border ${
                      selectedAnn.id === ann.id
                        ? "border-surface text-surface"
                        : "border-ink bg-surface-raised text-ink"
                    }`}
                  >
                    {ann.category}
                  </span>
                </div>
                <div className="text-[10px] font-mono mt-1 opacity-80">
                  Consumer: {ann.consumer_framework}
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Deep Dive Panel */}
        <div className="md:col-span-7 border-2 border-ink bg-surface-raised p-4 space-y-4">
          <div className="flex justify-between items-center border-b-2 border-ink pb-2">
            <div>
              <h4 className="text-sm font-mono font-black text-ink">{selectedAnn.name}</h4>
              <span className="text-[10px] font-mono text-muted">
                Category: <strong>{selectedAnn.category}</strong> • Consumer:{" "}
                <strong className="text-accent">{selectedAnn.consumer_framework}</strong>
              </span>
            </div>
          </div>

          <div>
            <span className="text-[10px] font-mono uppercase font-bold text-muted block mb-1">
              Sample Syntax in CDS View Entity:
            </span>
            <pre className="p-3 bg-surface border-2 border-ink text-xs font-mono overflow-x-auto text-ink/90 leading-relaxed">
              <code>{selectedAnn.sample_syntax}</code>
            </pre>
          </div>

          <div className="bg-surface p-3 border border-ink space-y-2 text-xs font-mono">
            <div>
              <span className="font-black text-ink block text-[10px] uppercase">Architectural Purpose:</span>
              <p className="text-muted leading-relaxed mt-0.5">{selectedAnn.architectural_impact}</p>
            </div>
            <div className="pt-2 border-t border-ink/20">
              <span className="font-black text-danger block text-[10px] uppercase">Production Risk If Omitted:</span>
              <p className="text-danger leading-relaxed mt-0.5">{selectedAnn.risk_if_omitted}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Truthfulness Notice */}
      <div className="p-3 bg-surface border-2 border-ink text-[11px] font-mono text-muted flex items-center justify-between">
        <span>* Educational CDS annotation catalog modeling SAP S/4HANA metadata governance.</span>
        <span className="font-bold text-ink">[LOCAL SIMULATION ONLY]</span>
      </div>
    </div>
  );
};
