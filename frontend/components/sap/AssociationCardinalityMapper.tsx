"use client";

import React, { useState } from "react";

interface AssociationScenario {
  id: string;
  name: string;
  cardinality: "[1..1]" | "[0..1]" | "[1..*]" | "[0..*]";
  target_entity: string;
  relationship_nature: string;
  on_clause: string;
  path_expression: string;
  is_path_accessed: boolean;
  generated_sql_with_path: string;
  generated_sql_without_path: string;
  risk_warning: string;
}

const SCENARIOS: AssociationScenario[] = [
  {
    id: "sc-cust",
    name: "_Customer (Header to Sold-To Partner)",
    cardinality: "[1..1]",
    target_entity: "I_Customer",
    relationship_nature: "Every sales order header has exactly one Sold-To customer partner.",
    on_clause: "$projection.SoldToParty = _Customer.Customer",
    path_expression: "_Customer.Country",
    is_path_accessed: true,
    generated_sql_with_path: `SELECT
    t0.SalesOrder,
    t0.NetAmount,
    t1.Country AS CustomerCountry
FROM VBAK t0
LEFT OUTER MANY TO ONE JOIN KNA1 t1
    ON t0.SoldToParty = t1.Customer`,
    generated_sql_without_path: `SELECT
    t0.SalesOrder,
    t0.NetAmount
FROM VBAK t0
-- NO JOIN INSTANTIATED: Declaring an association does not join target tables until fields are consumed via path expressions`,
    risk_warning: "Safe cardinality. 1..1 allows optimizer to prune join if no fields from _Customer are requested.",
  },
  {
    id: "sc-items",
    name: "_Items (Header to Line Items)",
    cardinality: "[1..*]",
    target_entity: "I_SalesOrderItem",
    relationship_nature: "One sales order contains one or more line items.",
    on_clause: "$projection.SalesOrder = _Items.SalesOrder",
    path_expression: "_Items.Material",
    is_path_accessed: false,
    generated_sql_with_path: `SELECT
    t0.SalesOrder,
    t0.NetAmount,
    t1.Material
FROM VBAK t0
LEFT OUTER ONE TO MANY JOIN VBAP t1
    ON t0.SalesOrder = t1.SalesOrder`,
    generated_sql_without_path: `SELECT
    t0.SalesOrder,
    t0.NetAmount
FROM VBAK t0
-- NO JOIN INSTANTIATED: Only root header fields projected; associated item join is not instantiated`,
    risk_warning: "Caution: Declaring [1..1] when data is [1..*] can cause the SQL optimizer to skip distinct filtering, duplicating aggregated financial totals!",
  },
  {
    id: "sc-deliv",
    name: "_Delivery (Line Item to Outbound Delivery)",
    cardinality: "[0..1]",
    target_entity: "I_DeliveryDocumentItem",
    relationship_nature: "An unfulfilled sales order line item may not yet have an outbound delivery.",
    on_clause: "$projection.SalesOrder = _Delivery.SalesOrder AND $projection.Item = _Delivery.Item",
    path_expression: "_Delivery.PickingStatus",
    is_path_accessed: true,
    generated_sql_with_path: `SELECT
    t0.SalesOrder,
    t0.SalesOrderItem,
    t1.PickingStatus
FROM VBAP t0
LEFT OUTER JOIN LIPS t1
    ON t0.SalesOrder = t1.SalesOrder AND t0.Item = t1.Item`,
    generated_sql_without_path: `SELECT
    t0.SalesOrder,
    t0.SalesOrderItem
FROM VBAP t0`,
    risk_warning: "Using 0..1 correctly specifies that delivery might not exist yet (outer join preserved).",
  },
];

interface AssociationCardinalityMapperProps {
  title?: string;
  instruction?: string;
}

export const AssociationCardinalityMapper: React.FC<AssociationCardinalityMapperProps> = ({
  title = "CDS Associations vs Eager SQL Joins Workbench",
  instruction = "Declaring an association provides reusable navigation semantics without joining; consuming fields through path expressions instantiates joins on-demand.",
}) => {
  const [selectedScenario, setSelectedScenario] = useState<AssociationScenario>(SCENARIOS[0]!);
  const [isPathAccessed, setIsPathAccessed] = useState<boolean>(true);

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

        {/* Path Access Toggle */}
        <div className="flex items-center gap-2 border-2 border-ink p-1 bg-surface-raised">
          <span className="text-xs font-mono font-bold px-2">Path Expression Traversal:</span>
          <button
            type="button"
            onClick={() => setIsPathAccessed(true)}
            className={`px-3 py-1 text-xs font-mono font-bold transition-colors ${
              isPathAccessed ? "bg-accent text-surface font-black" : "bg-surface hover:bg-surface-raised"
            }`}
          >
            Requested (_Customer.Country)
          </button>
          <button
            type="button"
            onClick={() => setIsPathAccessed(false)}
            className={`px-3 py-1 text-xs font-mono font-bold transition-colors ${
              !isPathAccessed ? "bg-ink text-surface font-black" : "bg-surface hover:bg-surface-raised"
            }`}
          >
            Omitted (Only Header Fields)
          </button>
        </div>
      </div>

      {/* Scenario Selector */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        {SCENARIOS.map((sc) => (
          <button
            key={sc.id}
            type="button"
            onClick={() => setSelectedScenario(sc)}
            className={`p-3 text-left border-2 border-ink transition-all ${
              selectedScenario.id === sc.id
                ? "bg-ink text-surface shadow-[3px_3px_0px_0px_rgba(0,0,0,1)]"
                : "bg-surface hover:bg-surface-raised"
            }`}
          >
            <div className="flex items-center justify-between text-xs font-mono">
              <span className="font-black">{sc.name}</span>
              <span className="font-mono px-1.5 py-0.5 border text-[10px] font-bold">
                {sc.cardinality}
              </span>
            </div>
            <span className="text-[10px] font-mono block mt-1 opacity-80 truncate">
              Target: {sc.target_entity}
            </span>
          </button>
        ))}
      </div>

      {/* Association Details & Comparison */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* CDS DDL Definition */}
        <div className="border-2 border-ink bg-surface-raised p-4 space-y-3">
          <div className="flex justify-between items-center border-b border-ink/40 pb-2">
            <h4 className="text-xs font-mono font-black uppercase tracking-wider">
              ABAP CDS Association Definition
            </h4>
            <span className="text-[10px] font-mono bg-accent/20 px-2 py-0.5 border border-ink font-bold">
              LAZY EVALUATION
            </span>
          </div>

          <pre className="p-3 bg-surface border border-ink text-xs font-mono overflow-x-auto text-ink/90 leading-relaxed">
            <code>{`association ${selectedScenario.cardinality} to ${selectedScenario.target_entity} as ${selectedScenario.name.split(" ")[0]}
  on ${selectedScenario.on_clause}`}</code>
          </pre>

          <div className="space-y-1 text-xs font-mono">
            <span className="text-muted block text-[10px] uppercase font-bold">Business Relationship:</span>
            <p className="leading-relaxed">{selectedScenario.relationship_nature}</p>
          </div>

          <div className="p-2.5 bg-surface border border-ink text-xs font-mono space-y-1">
            <span className="text-danger font-black block text-[10px] uppercase">Architectural Invariant:</span>
            <p className="text-[11px] leading-relaxed text-muted">{selectedScenario.risk_warning}</p>
          </div>
        </div>

        {/* Runtime Generated SQL */}
        <div className="border-2 border-ink bg-surface p-4 space-y-3">
          <div className="flex justify-between items-center border-b border-ink/40 pb-2">
            <h4 className="text-xs font-mono font-black uppercase tracking-wider">
              Generated HANA SQL Statement
            </h4>
            <span
              className={`text-[10px] font-mono px-2 py-0.5 font-bold border border-ink ${
                isPathAccessed ? "bg-accent text-surface" : "bg-surface-raised text-muted"
              }`}
            >
              {isPathAccessed ? "JOIN TRIGGERED" : "JOIN PRUNED (NO JOIN)"}
            </span>
          </div>

          <pre className="p-3 bg-ink text-surface border-2 border-ink text-xs font-mono overflow-x-auto leading-relaxed min-h-[160px]">
            <code>
              {isPathAccessed
                ? selectedScenario.generated_sql_with_path
                : selectedScenario.generated_sql_without_path}
            </code>
          </pre>

          <p className="text-[11px] font-mono text-muted leading-tight">
            {isPathAccessed
              ? "Because the consumer accessed path expression " + selectedScenario.path_expression + ", the SQL Optimizer instantiated the join on-demand."
              : "No join instantiated! The query projected only root entity fields, allowing the SQL optimizer to prune the target table completely."}
          </p>
        </div>
      </div>

      {/* Truthfulness Notice */}
      <div className="p-3 bg-surface border-2 border-ink text-[11px] font-mono text-muted flex flex-col md:flex-row md:items-center md:justify-between gap-1">
        <span>* Associations provide reusable navigation semantics; declaring an association does not itself join tables. Consuming target fields via path expressions instantiates joins. Associations are not automatically faster than joins.</span>
        <span className="font-bold text-ink whitespace-nowrap">[LOCAL SIMULATION ONLY]</span>
      </div>
    </div>
  );
};
