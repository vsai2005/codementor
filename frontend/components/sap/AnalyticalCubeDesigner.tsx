"use client";

import React, { useState } from "react";

interface FactRow {
  plant: "PL01" | "PL02";
  product: "DXTR-1000" | "RAW-01";
  customer: "CUST-501" | "CUST-502";
  gross_amount: number;
  net_amount: number;
  cogs_amount: number;
  quantity: number;
}

const FACT_RECORDS: FactRow[] = [
  { plant: "PL01", product: "DXTR-1000", customer: "CUST-501", gross_amount: 45000, net_amount: 42000, cogs_amount: 28000, quantity: 28 },
  { plant: "PL01", product: "RAW-01", customer: "CUST-502", gross_amount: 15000, net_amount: 14000, cogs_amount: 9000, quantity: 140 },
  { plant: "PL02", product: "DXTR-1000", customer: "CUST-501", gross_amount: 32000, net_amount: 30000, cogs_amount: 19500, quantity: 20 },
  { plant: "PL02", product: "RAW-01", customer: "CUST-502", gross_amount: 8500, net_amount: 8000, cogs_amount: 5200, quantity: 80 },
];

interface AnalyticalCubeDesignerProps {
  title?: string;
  instruction?: string;
}

export const AnalyticalCubeDesigner: React.FC<AnalyticalCubeDesignerProps> = ({
  title = "CDS Analytical Cube & Multidimensional Query Designer",
  instruction = "Configure analytical measures, aggregation rules (@Aggregation.default: #SUM), and slice multidimensional dimensions.",
}) => {
  const [selectedGroupBy, setSelectedGroupBy] = useState<"PLANT" | "PRODUCT" | "CUSTOMER">("PLANT");
  const [selectedMeasure, setSelectedMeasure] = useState<"net_amount" | "cogs_amount" | "margin">("margin");

  // Aggregate by chosen dimension
  const aggregatedData = React.useMemo(() => {
    const map = new Map<
      string,
      { dimension: string; gross: number; net: number; cogs: number; qty: number }
    >();

    FACT_RECORDS.forEach((row) => {
      const key =
        selectedGroupBy === "PLANT"
          ? row.plant
          : selectedGroupBy === "PRODUCT"
          ? row.product
          : row.customer;

      const existing = map.get(key) || { dimension: key, gross: 0, net: 0, cogs: 0, qty: 0 };
      existing.gross += row.gross_amount;
      existing.net += row.net_amount;
      existing.cogs += row.cogs_amount;
      existing.qty += row.quantity;
      map.set(key, existing);
    });

    return Array.from(map.values()).map((item) => ({
      ...item,
      margin: item.net - item.cogs,
      margin_pct: item.net > 0 ? ((item.net - item.cogs) / item.net) * 100 : 0,
    }));
  }, [selectedGroupBy]);

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

        {/* Dimension Slice Selector */}
        <div className="flex border-2 border-ink">
          {(["PLANT", "PRODUCT", "CUSTOMER"] as const).map((dim) => (
            <button
              key={dim}
              type="button"
              onClick={() => setSelectedGroupBy(dim)}
              className={`px-3 py-1.5 text-xs font-mono font-bold transition-colors border-r border-ink last:border-r-0 ${
                selectedGroupBy === dim ? "bg-ink text-surface font-black" : "bg-surface hover:bg-surface-raised"
              }`}
            >
              Slice by {dim}
            </button>
          ))}
        </div>
      </div>

      {/* DDL Definition & Measures */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Analytical Cube CDS Code */}
        <div className="border-2 border-ink bg-surface-raised p-4 space-y-2">
          <div className="flex justify-between items-center border-b border-ink/40 pb-1">
            <h4 className="text-xs font-mono font-black uppercase tracking-wider">
              CDS Cube Definition (#CUBE)
            </h4>
            <span className="text-[10px] font-mono bg-accent text-surface px-2 py-0.5 font-bold">
              FACT REPOSITORY
            </span>
          </div>
          <pre className="p-3 bg-surface border border-ink text-xs font-mono overflow-x-auto text-ink/90 leading-relaxed max-h-48 overflow-y-auto">
            <code>{`@EndUserText.label: 'Nova Executive Sales Cube'
@Analytics.dataCategory: #CUBE
@VDM.viewType: #COMPOSITE
define view entity I_NovaSalesMarginCube
  as select from I_SalesOrderItem
{
  key SalesOrder,
  key SalesOrderItem,
      Plant,
      Product,
      SoldToParty as Customer,

      @Aggregation.default: #SUM
      @Semantics.amount.currencyCode: 'Currency'
      NetAmount,

      @Aggregation.default: #SUM
      @Semantics.amount.currencyCode: 'Currency'
      CostOfGoodsSold,

      Currency
}`}</code>
          </pre>
        </div>

        {/* Measure Selector & Slicing Controls */}
        <div className="border-2 border-ink bg-surface p-4 space-y-3">
          <div className="flex justify-between items-center border-b border-ink/40 pb-1">
            <h4 className="text-xs font-mono font-black uppercase tracking-wider">
              Analytical Query Projection (#QUERY)
            </h4>
            <span className="text-[10px] font-mono bg-ink text-surface px-2 py-0.5 font-bold">
              TRANSIENT SLICE
            </span>
          </div>

          <p className="text-xs font-mono text-muted">
            The Analytical Engine executes in-memory vector aggregation along the selected dimension:
          </p>

          <div className="grid grid-cols-3 gap-2 pt-2">
            <button
              type="button"
              onClick={() => setSelectedMeasure("net_amount")}
              className={`p-2 text-xs font-mono border-2 border-ink font-bold transition-colors ${
                selectedMeasure === "net_amount" ? "bg-ink text-surface font-black" : "hover:bg-surface-raised"
              }`}
            >
              Net Revenue
            </button>
            <button
              type="button"
              onClick={() => setSelectedMeasure("cogs_amount")}
              className={`p-2 text-xs font-mono border-2 border-ink font-bold transition-colors ${
                selectedMeasure === "cogs_amount" ? "bg-ink text-surface font-black" : "hover:bg-surface-raised"
              }`}
            >
              Cost of Goods (COGS)
            </button>
            <button
              type="button"
              onClick={() => setSelectedMeasure("margin")}
              className={`p-2 text-xs font-mono border-2 border-ink font-bold transition-colors ${
                selectedMeasure === "margin" ? "bg-accent text-surface font-black" : "hover:bg-surface-raised"
              }`}
            >
              Gross Profit Margin
            </button>
          </div>
        </div>
      </div>

      {/* Multidimensional Pivot Table */}
      <div className="space-y-2">
        <h4 className="text-xs font-mono font-black uppercase text-muted tracking-wider">
          Multidimensional Query Slicing Result ({aggregatedData.length} Dimensional Nodes)
        </h4>
        <div className="overflow-x-auto border-2 border-ink">
          <table className="w-full text-left text-xs font-mono">
            <thead className="bg-surface-raised border-b-2 border-ink">
              <tr>
                <th className="p-2.5 uppercase font-black">Dimension: {selectedGroupBy}</th>
                <th className="p-2.5 text-right font-black">Total Quantity</th>
                <th className="p-2.5 text-right font-black">Gross Billed</th>
                <th className="p-2.5 text-right font-black">Net Billed (SUM)</th>
                <th className="p-2.5 text-right font-black">COGS (SUM)</th>
                <th className="p-2.5 text-right font-black text-accent">Gross Margin (€)</th>
                <th className="p-2.5 text-right font-black text-accent">Margin (%)</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-ink/20">
              {aggregatedData.map((row) => (
                <tr key={row.dimension} className="hover:bg-surface-raised">
                  <td className="p-2.5 font-bold">{row.dimension}</td>
                  <td className="p-2.5 text-right">{row.qty.toLocaleString()} EA</td>
                  <td className="p-2.5 text-right">€{row.gross.toLocaleString()}</td>
                  <td className="p-2.5 text-right">€{row.net.toLocaleString()}</td>
                  <td className="p-2.5 text-right">€{row.cogs.toLocaleString()}</td>
                  <td className="p-2.5 text-right font-black text-accent">€{row.margin.toLocaleString()}</td>
                  <td className="p-2.5 text-right font-bold text-accent">{row.margin_pct.toFixed(1)}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Truthfulness Notice */}
      <div className="p-3 bg-surface border-2 border-ink text-[11px] font-mono text-muted flex items-center justify-between">
        <span>* Educational simulation of S/4HANA embedded analytics #CUBE multidimensional aggregation.</span>
        <span className="font-bold text-ink">[LOCAL SIMULATION ONLY]</span>
      </div>
    </div>
  );
};
