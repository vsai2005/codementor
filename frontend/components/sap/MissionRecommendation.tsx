"use client";

import React from "react";
import Link from "next/link";

interface MissionRecommendationProps {
  mission: {
    slug: string;
    title: string;
    description?: string;
    desc?: string;
  };
}

export function MissionRecommendation({ mission }: MissionRecommendationProps) {
  const description = mission.description || mission.desc || "";

  return (
    <div className="border-3 border-ink bg-gradient-to-br from-purple-50 to-indigo-50 p-6 shadow-[5px_5px_0px_0px_rgba(79,70,229,1)]">
      <div className="flex flex-wrap items-center justify-between gap-2 mb-3">
        <div className="flex items-center gap-2">
          <span className="text-[10px] font-mono font-bold uppercase bg-indigo-600 text-white px-2.5 py-0.5 border border-ink">
            Recommended Enterprise Mission
          </span>
          <span className="text-xs font-mono font-bold text-indigo-900">
            Nova Manufacturing Twin
          </span>
        </div>
        <span className="text-xs font-mono text-muted">
          Hands-On Practical Lab
        </span>
      </div>

      <h3 className="text-lg font-black text-ink mb-2">
        {mission.title}
      </h3>

      <p className="text-xs sm:text-sm text-ink/80 leading-relaxed mb-5 font-medium">
        {description}
      </p>

      <div className="flex flex-wrap items-center gap-3">
        <Link
          href={`/sap/missions/${mission.slug}`}
          className="border-3 border-ink bg-indigo-600 text-white px-5 py-2.5 text-xs font-black uppercase tracking-wider shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] hover:bg-indigo-500 hover:translate-x-0.5 hover:translate-y-0.5 transition-all inline-flex items-center gap-2"
        >
          <span>Launch Mission in Enterprise Twin</span>
          <span>→</span>
        </Link>

        <Link
          href="/sap/missions"
          className="border-2 border-ink bg-surface px-4 py-2 text-xs font-bold text-ink hover:bg-surface-raised transition-all"
        >
          Browse All Missions
        </Link>
      </div>
    </div>
  );
}
