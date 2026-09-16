"use client";

import React, { useState } from "react";

interface VDMViewNode {
  id: string;
  name: string;
  tier: "BASIC" | "COMPOSITE" | "CONSUMPTION";
  prefix: "I_" | "R_" | "C_";
  release_status: "RELEASED_C1" | "RELEASED_C2" | "NOT_RELEASED";
  source_tables_or_views: string[];
  description: string;
  sample_ddl: string;
  clean_core_role: string;
}

const VDM_CATALOG: VDMViewNode[] = [
  {
    id: "vdm-basic-plant",
    name: "I_Plant",
    tier: "BASIC",
    prefix: "I_",
    release_status: "RELEASED_C1",
    source_tables_or_views: ["T001W (Plants/Branches)"],
    description: "Basic Interface View mapping organizational plant master data directly from transparent table T001W without business logic.",
    sample_ddl: `@EndUserText.label: 'Plant Basic View'
@VDM.viewType: #BASIC
@AccessControl.authorizationCheck: #NOT_REQUIRED
define view entity I_Plant
  as select from t001w
{
  key werks as Plant,
      name1 as PlantName,
      vkorg as SalesOrganization,
      bwkey as ValuationArea
}`,
    clean_core_role: "Stable foundational entity; protected by contract C1 for system upgrade stability.",
  },
  {
    id: "vdm-basic-product",
    name: "I_Product",
    tier: "BASIC",
    prefix: "I_",
    release_status: "RELEASED_C1",
    source_tables_or_views: ["MARA (General Material Data)"],
    description: "Basic Interface View representing central material/product master data attributes.",
    sample_ddl: `@EndUserText.label: 'Product Basic View'
@VDM.viewType: #BASIC
@AccessControl.authorizationCheck: #NOT_REQUIRED
define view entity I_Product
  as select from mara
{
  key matnr as Product,
      mtart as ProductType,
      matkl as ProductCategory,
      meins as BaseUnit
}`,
    clean_core_role: "Universal dimension entity referenced by logistics, manufacturing, and billing.",
  },
  {
    id: "vdm-comp-sales",
    name: "I_SalesOrderWithItems",
    tier: "COMPOSITE",
    prefix: "I_",
    release_status: "RELEASED_C1",
    source_tables_or_views: ["I_SalesOrderHeader", "I_SalesOrderItem", "I_Product", "I_Plant"],
    description: "Composite View combining sales order line items with product master data, plant attributes, and delivery status.",
    sample_ddl: `@EndUserText.label: 'Sales Order Composite Cube'
@VDM.viewType: #COMPOSITE
@Analytics.dataCategory: #CUBE
define view entity I_SalesOrderWithItems
  as select from I_SalesOrderItem as Item
  association [1..1] to I_Plant as _Plant on $projection.Plant = _Plant.Plant
  association [1..1] to I_Product as _Product on $projection.Product = _Product.Product
{
  key Item.SalesOrder,
  key Item.SalesOrderItem,
      Item.Plant,
      Item.Product,
      @Aggregation.default: #SUM
      @Semantics.amount.currencyCode: 'Currency'
      Item.NetAmount,
      Item.Currency,
      _Plant,
      _Product
}`,
    clean_core_role: "Core business logic tier. Never exposes UI-specific annotations; aggregates enterprise state.",
  },
  {
    id: "vdm-cons-query",
    name: "C_RoboticsSalesMarginQuery",
    tier: "CONSUMPTION",
    prefix: "C_",
    release_status: "RELEASED_C2",
    source_tables_or_views: ["I_SalesOrderWithItems"],
    description: "Consumption View designed specifically for the Executive Robotics Margin Fiori App and analytical KPI cards.",
    sample_ddl: `@EndUserText.label: 'Robotics Margin Analytical Query'
@VDM.viewType: #CONSUMPTION
@Analytics.query: true
@AccessControl.authorizationCheck: #CHECK
define view entity C_RoboticsSalesMarginQuery
  as select from I_SalesOrderWithItems
{
  @AnalyticsDetails.query.axis: #ROWS
  Plant,
  @AnalyticsDetails.query.axis: #ROWS
  Product,
  @AnalyticsDetails.query.axis: #COLUMNS
  NetAmount
}`,
    clean_core_role: "Application-specific projection. Other CDS views are strictly prohibited from referencing Consumption views.",
  },
];

interface VDMBuilderProps {
  title?: string;
  instruction?: string;
}

export const VDMBuilder: React.FC<VDMBuilderProps> = ({
  title = "S/4HANA Virtual Data Model (VDM) Architecture Studio",
  instruction = "Explore the three architectural tiers of the VDM and inspect stability contracts and naming rules.",
}) => {
  const [selectedTier, setSelectedTier] = useState<"ALL" | "BASIC" | "COMPOSITE" | "CONSUMPTION">("ALL");
  const [activeView, setActiveView] = useState<VDMViewNode>(VDM_CATALOG[2]!);

  const filteredViews =
    selectedTier === "ALL" ? VDM_CATALOG : VDM_CATALOG.filter((v) => v.tier === selectedTier);

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

        {/* Tier Filter Tabs */}
        <div className="flex flex-wrap border-2 border-ink">
          {(["ALL", "BASIC", "COMPOSITE", "CONSUMPTION"] as const).map((tier) => (
            <button
              key={tier}
              type="button"
              onClick={() => setSelectedTier(tier)}
              className={`px-3 py-1.5 text-xs font-mono font-bold transition-colors border-r border-ink last:border-r-0 ${
                selectedTier === tier
                  ? "bg-ink text-surface font-black"
                  : "bg-surface text-ink hover:bg-surface-raised"
              }`}
            >
              {tier === "ALL" ? "All Tiers" : `${tier} (${tier === "BASIC" ? "I_" : tier === "COMPOSITE" ? "R_/I_" : "C_"})`}
            </button>
          ))}
        </div>
      </div>

      {/* 3-Tier Layering Flow Visualization */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Tier 1 Card */}
        <div className="border-2 border-ink bg-surface-raised p-3">
          <div className="flex items-center justify-between mb-1">
            <span className="text-xs font-mono font-black text-accent uppercase">BASIC (@VDM.viewType: #BASIC)</span>
            <span className="text-[10px] font-mono border border-ink px-1 bg-surface font-bold">RAW TABLES</span>
          </div>
          <p className="text-[11px] font-mono text-muted leading-tight">
            1-to-1 projection on database tables without joins. Typically uses I_ prefix. Exposes cleansed master and transactional attributes.
          </p>
        </div>

        {/* Tier 2 Card */}
        <div className="border-2 border-ink bg-surface-raised p-3">
          <div className="flex items-center justify-between mb-1">
            <span className="text-xs font-mono font-black text-ink uppercase">COMPOSITE (@VDM.viewType: #COMPOSITE)</span>
            <span className="text-[10px] font-mono border border-ink px-1 bg-surface font-bold">CORE ENTITIES</span>
          </div>
          <p className="text-[11px] font-mono text-muted leading-tight">
            Business associations, calculations, and cubes combining basic views (uses R_ or I_ prefix). Agnostic to UI layer.
          </p>
        </div>

        {/* Tier 3 Card */}
        <div className="border-2 border-ink bg-surface-raised p-3">
          <div className="flex items-center justify-between mb-1">
            <span className="text-xs font-mono font-black text-danger uppercase">CONSUMPTION (@VDM.viewType: #CONSUMPTION)</span>
            <span className="text-[10px] font-mono border border-ink px-1 bg-surface font-bold">APP SPECIFIC</span>
          </div>
          <p className="text-[11px] font-mono text-muted leading-tight">
            Tailored specifically for Fiori apps or analytical queries (typically uses C_ prefix). Never reused by other views.
          </p>
        </div>
      </div>

      {/* Catalog & Inspector Split View */}
      <div className="grid grid-cols-1 md:grid-cols-12 gap-6">
        {/* Entity List */}
        <div className="md:col-span-5 space-y-2">
          <h4 className="text-xs font-mono font-black uppercase text-muted tracking-wider">
            VDM Entity Catalog ({filteredViews.length})
          </h4>
          <div className="space-y-2">
            {filteredViews.map((view) => (
              <button
                key={view.id}
                type="button"
                onClick={() => setActiveView(view)}
                className={`w-full text-left p-3 border-2 border-ink transition-all ${
                  activeView.id === view.id
                    ? "bg-ink text-surface shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] translate-x-1"
                    : "bg-surface hover:bg-surface-raised"
                }`}
              >
                <div className="flex items-center justify-between text-xs font-mono">
                  <span className="font-black">{view.name}</span>
                  <span
                    className={`px-1.5 py-0.5 text-[10px] font-bold border ${
                      activeView.id === view.id
                        ? "border-surface text-surface"
                        : "border-ink bg-surface-raised text-ink"
                    }`}
                  >
                    {view.tier}
                  </span>
                </div>
                <div className="text-[10px] font-mono mt-1 opacity-80 truncate">
                  Sources: {view.source_tables_or_views.join(", ")}
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Inspector & DDL Preview */}
        <div className="md:col-span-7 border-2 border-ink bg-surface-raised p-4 space-y-4">
          <div className="flex flex-wrap items-center justify-between gap-2 border-b-2 border-ink pb-2">
            <div>
              <h4 className="text-sm font-mono font-black text-ink">{activeView.name}</h4>
              <span className="text-[10px] font-mono text-muted">
                Prefix: <strong className="text-ink">{activeView.prefix}</strong> • Tier:{" "}
                <strong className="text-ink">{activeView.tier}</strong>
              </span>
            </div>
            <span className="text-[10px] font-mono px-2 py-0.5 font-black border border-ink bg-accent text-surface">
              {activeView.release_status}
            </span>
          </div>

          <div className="bg-surface p-3 border border-ink text-xs font-mono leading-relaxed space-y-2">
            <p>{activeView.description}</p>
            <div className="p-2 bg-surface-raised border border-ink/40 text-[11px]">
              <strong className="block text-ink uppercase text-[10px] mb-0.5">Clean Core Governance Rule:</strong>
              {activeView.clean_core_role}
            </div>
          </div>

          {/* DDL Code Block */}
          <div>
            <div className="flex justify-between items-center bg-ink text-surface px-3 py-1 text-[10px] font-mono font-bold">
              <span>ABAP Core Data Services Definition</span>
              <span>READ-ONLY VIEW ENTITY</span>
            </div>
            <pre className="p-3 bg-surface border-2 border-ink text-xs font-mono overflow-x-auto text-ink/90 leading-relaxed max-h-60 overflow-y-auto">
              <code>{activeView.sample_ddl}</code>
            </pre>
          </div>
        </div>
      </div>

      {/* Truthfulness Notice */}
      <div className="p-3 bg-surface border-2 border-ink text-[11px] font-mono text-muted flex flex-col md:flex-row md:items-center md:justify-between gap-1">
        <span>* VDM tiers are BASIC, COMPOSITE, CONSUMPTION. Release contracts (C1 = Use System-Internally, C2 = Use as Remote API) are orthogonal API release contracts, not VDM tiers. View types derive from @VDM.viewType, not prefixes alone.</span>
        <span className="font-bold text-ink whitespace-nowrap">[LOCAL SIMULATION ONLY]</span>
      </div>
    </div>
  );
};
