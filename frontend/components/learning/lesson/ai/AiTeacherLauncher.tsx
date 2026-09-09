"use client";

import React from "react";

interface AiTeacherLauncherProps {
  isOpen: boolean;
  onToggle: () => void;
  hasUnread?: boolean;
}

export function AiTeacherLauncher({
  isOpen,
  onToggle,
  hasUnread = false,
}: AiTeacherLauncherProps) {
  return (
    <button
      type="button"
      onClick={onToggle}
      aria-label={isOpen ? "Close AI Mentor panel" : "Open AI Mentor panel"}
      aria-expanded={isOpen}
      className={`fixed bottom-20 right-3 sm:bottom-20 sm:right-6 z-40 btn font-mono text-xs sm:text-sm font-bold flex items-center gap-2 px-3.5 py-2.5 rounded border-2 border-ink transition-all shadow-hard active:translate-y-0.5 ${
        isOpen
          ? "bg-ink text-bg shadow-none"
          : "bg-surface hover:bg-bg text-ink hover:shadow-hard-lg"
      }`}
    >
      <span className="text-base select-none">\ud83e\udde0</span>
      <span className="font-display tracking-wide">
        {isOpen ? "Close Mentor" : "AI Mentor"}
      </span>
      <kbd className="hidden sm:inline-block px-1.5 py-0.5 rounded bg-ink/10 text-ink/80 text-[10px] font-mono border border-ink/20">
        \u2318K
      </kbd>

      {hasUnread && !isOpen && (
        <span className="absolute -top-1 -right-1 flex h-3 w-3">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-accent opacity-75" />
          <span className="relative inline-flex rounded-full h-3 w-3 bg-accent border border-ink" />
        </span>
      )}
    </button>
  );
}
