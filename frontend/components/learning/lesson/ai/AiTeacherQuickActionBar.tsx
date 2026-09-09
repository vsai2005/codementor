"use client";

import React from "react";
import { QUICK_ACTIONS, QuickActionType } from "./types";

interface AiTeacherQuickActionBarProps {
  onSelectAction: (action: QuickActionType) => void;
  disabled?: boolean;
  activeAction?: string | null;
}

export function AiTeacherQuickActionBar({
  onSelectAction,
  disabled = false,
  activeAction,
}: AiTeacherQuickActionBarProps) {
  return (
    <div className="border-b border-ink/20 bg-bg/80 px-3 py-2 shrink-0">
      <div className="flex items-center gap-1.5 overflow-x-auto no-scrollbar py-0.5">
        {QUICK_ACTIONS.map((action) => {
          const isActive = activeAction === action.id;
          return (
            <button
              key={action.id}
              type="button"
              disabled={disabled}
              onClick={() => onSelectAction(action.id)}
              title={action.description}
              className={`shrink-0 font-mono text-[11px] font-bold px-2 py-1 rounded-sm border transition-all flex items-center gap-1 active:translate-y-0.5 ${
                isActive
                  ? "bg-accent text-bg border-ink shadow-hard-sm"
                  : "bg-surface hover:bg-bg border-ink/30 text-ink shadow-sm hover:border-ink"
              } disabled:opacity-40 disabled:cursor-not-allowed`}
            >
              <span>{action.icon}</span>
              <span>{action.label}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
}
