"use client";

import React from "react";

export function AiTeacherTypingIndicator() {
  return (
    <div className="flex items-start gap-2.5 my-2">
      <div className="w-7 h-7 rounded border border-ink/40 bg-accent/20 flex items-center justify-center font-mono text-xs shrink-0 select-none shadow-hard-sm">
        🧠
      </div>
      <div className="card bg-surface border-2 border-ink px-3 py-2 shadow-hard-sm max-w-[80%] flex items-center gap-2">
        <span className="font-mono text-xs text-muted">AI Mentor is thinking</span>
        <div className="flex items-center gap-1">
          <span className="w-1.5 h-1.5 bg-accent rounded-full animate-bounce [animation-delay:-0.3s]" />
          <span className="w-1.5 h-1.5 bg-accent rounded-full animate-bounce [animation-delay:-0.15s]" />
          <span className="w-1.5 h-1.5 bg-accent rounded-full animate-bounce" />
        </div>
      </div>
    </div>
  );
}
