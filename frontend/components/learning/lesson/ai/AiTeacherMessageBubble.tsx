"use client";

import React from "react";
import { ChatMessage, QuickActionType } from "./types";
import { LessonMarkdown } from "../LessonMarkdown";

interface AiTeacherMessageBubbleProps {
  message: ChatMessage;
  onSelectAction?: (action: QuickActionType) => void;
}

export function AiTeacherMessageBubble({
  message,
  onSelectAction,
}: AiTeacherMessageBubbleProps) {
  const isUser = message.role === "user";

  const timeString = message.timestamp
    ? new Date(message.timestamp).toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      })
    : "";

  return (
    <div className={`flex items-start gap-2.5 my-3 ${isUser ? "flex-row-reverse" : "flex-row"}`}>
      {/* Avatar Badge */}
      <div
        className={`w-7 h-7 rounded border border-ink/40 flex items-center justify-center font-mono text-xs shrink-0 select-none shadow-hard-sm ${
          isUser
            ? "bg-accent/30 text-accent font-bold"
            : "bg-surface text-ink font-bold"
        }`}
      >
        {isUser ? "YOU" : "\ud83e\udde0"}
      </div>

      {/* Bubble Container */}
      <div
        className={`max-w-[88%] sm:max-w-[82%] card p-3.5 border-2 border-ink shadow-hard-sm transition-all ${
          isUser
            ? "bg-accent/15 text-ink rounded-tr-none"
            : "bg-surface text-ink rounded-tl-none"
        }`}
      >
        {/* Header (Role & Time) */}
        <div className="flex items-center justify-between gap-3 mb-1.5 pb-1 border-b border-ink/10 text-[11px] font-mono text-muted">
          <span className="font-bold uppercase tracking-wider text-ink/80">
            {isUser ? "You" : "AI Mentor"}
          </span>
          <span>{timeString}</span>
        </div>

        {/* Markdown Rendered Content */}
        <div className="text-sm leading-relaxed overflow-x-auto break-words">
          <LessonMarkdown content={message.content} />
        </div>

        {/* Related Concepts (if provided by curriculum knowledge engine) */}
        {message.relatedConcepts && message.relatedConcepts.length > 0 && (
          <div className="mt-3 pt-2 border-t border-ink/15 flex flex-wrap items-center gap-1.5">
            <span className="font-mono text-[10px] uppercase font-bold text-muted">Related:</span>
            {message.relatedConcepts.map((c: any, i: number) => {
              const label = typeof c === "string" ? c : `Day ${c.day}: ${c.title}`;
              return (
                <span
                  key={i}
                  className="font-mono text-[10px] px-1.5 py-0.5 rounded border border-ink/20 bg-bg/80 text-ink"
                >
                  {label}
                </span>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
