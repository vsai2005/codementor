"use client";

import React, { useState, useEffect, useRef, useCallback } from "react";
import { ChatMessage, QuickActionType } from "./types";
import { AiTeacherQuickActionBar } from "./AiTeacherQuickActionBar";
import { AiTeacherMessageBubble } from "./AiTeacherMessageBubble";
import { AiTeacherTypingIndicator } from "./AiTeacherTypingIndicator";
import { api, ApiError } from "@/lib/api";

interface AiTeacherDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  dayNumber: number;
  stepNumber: number;
  stepHeading: string;
  stepType: string;
  stepTakeaway?: string;
  currentCode?: string;
}

export function AiTeacherDrawer({
  isOpen,
  onClose,
  dayNumber,
  stepNumber,
  stepHeading,
  stepType,
  stepTakeaway,
  currentCode,
}: AiTeacherDrawerProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputMessage, setInputMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [hintLevel, setHintLevel] = useState(1);
  const [isPinned, setIsPinned] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  // Auto-scroll to bottom on new messages
  useEffect(() => {
    if (isOpen) {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages, isLoading, isOpen]);

  // Initial welcome greeting when drawer opens for the first time
  useEffect(() => {
    if (isOpen && messages.length === 0) {
      setMessages([
        {
          id: "welcome-msg",
          role: "assistant",
          content: `Hello! I'm your **AI Mentor** for Day ${dayNumber}: **${stepHeading}**.\n\nAsk me any question about this concept, request a progressive hint, or use the quick action buttons above to explore!`,
          timestamp: new Date(),
        },
      ]);
    }
  }, [isOpen, dayNumber, stepHeading, messages.length]);

  // Focus input when opened
  useEffect(() => {
    if (isOpen) {
      setTimeout(() => inputRef.current?.focus(), 150);
    }
  }, [isOpen]);

  // Keyboard shortcut listener (Cmd/Ctrl + K to toggle, Escape to close)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        if (isOpen) onClose();
      } else if (e.key === "Escape" && isOpen && !isPinned) {
        onClose();
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [isOpen, isPinned, onClose]);

  // Send a regular user question
  const handleSendMessage = useCallback(
    async (textToSend?: string, actionType?: QuickActionType) => {
      const query = (textToSend !== undefined ? textToSend : inputMessage).trim();
      if (!query && !actionType) return;

      setErrorMessage(null);
      const userMsgId = `user-${Date.now()}`;
      const newUserMsg: ChatMessage = {
        id: userMsgId,
        role: "user",
        content: query || `Action: ${actionType}`,
        timestamp: new Date(),
        quickAction: actionType,
      };

      setMessages((prev) => [...prev, newUserMsg]);
      if (!textToSend) setInputMessage("");
      setIsLoading(true);

      try {
        let resp;
        const historyPayload = messages.slice(-10).map((m) => ({
          role: m.role,
          content: m.content,
        }));

        if (actionType) {
          resp = await api.learningTutorQuickAction({
            day_number: dayNumber,
            step_number: stepNumber,
            action: actionType,
            user_code: currentCode,
            step_context: {
              step_type: stepType,
              heading: stepHeading,
              takeaway: stepTakeaway,
            },
            history: historyPayload,
            hint_level: actionType === "give_hint" ? hintLevel : 1,
          });

          if (actionType === "give_hint") {
            setHintLevel((prev) => (prev >= 3 ? 1 : prev + 1));
          }
        } else {
          resp = await api.learningTutorChat({
            day_number: dayNumber,
            step_number: stepNumber,
            message: query,
            history: historyPayload,
            user_code: currentCode,
            step_context: {
              step_type: stepType,
              heading: stepHeading,
              takeaway: stepTakeaway,
            },
            hint_level: hintLevel,
          });
        }

        const assistantMsg: ChatMessage = {
          id: `asst-${Date.now()}`,
          role: "assistant",
          content: resp.reply,
          timestamp: new Date(),
          quickAction: resp.quick_action || undefined,
          relatedConcepts: resp.related_concepts,
          visual: resp.visual,
        };
        setMessages((prev) => [...prev, assistantMsg]);
      } catch (err: any) {
        let errText = "I encountered an error connecting to my brain. Please try again.";
        if (err instanceof ApiError) {
          if (err.status === 429) {
            errText = `You've asked quite a few questions! Please wait ${err.retryAfterS || 30} seconds before asking again.`;
          } else if (err.status === 401) {
            errText = "Please sign in or refresh your session to continue chatting with the AI Mentor.";
          } else if (err.message) {
            errText = err.message;
          }
        }
        setErrorMessage(errText);
      } finally {
        setIsLoading(false);
      }
    },
    [
      inputMessage,
      messages,
      dayNumber,
      stepNumber,
      stepType,
      stepHeading,
      stepTakeaway,
      currentCode,
      hintLevel,
    ]
  );

  const handleQuickAction = (action: QuickActionType) => {
    handleSendMessage(undefined, action);
  };

  const handleInputKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  if (!isOpen) return null;

  return (
    <>
      {/* Backdrop overlay for mobile */}
      <div
        className={`fixed inset-0 bg-ink/30 z-40 transition-opacity md:hidden ${
          isPinned ? "hidden" : "block"
        }`}
        onClick={onClose}
      />

      {/* Main Drawer Container */}
      <aside
        aria-label="AI Mentor Learning Assistant"
        className={`fixed top-0 right-0 z-50 h-full w-full md:w-[480px] lg:w-[520px] bg-bg border-l-2 border-ink shadow-hard-lg flex flex-col transition-transform duration-200 ease-out`}
      >
        {/* Header */}
        <div className="flex items-center justify-between px-4 py-3 border-b-2 border-ink bg-surface shrink-0">
          <div className="flex items-center gap-2">
            <span className="text-xl">\ud83e\udde0</span>
            <div>
              <h2 className="font-display text-sm font-bold text-ink leading-tight flex items-center gap-2">
                <span>AI Mentor</span>
                <span className="font-mono text-[10px] px-1.5 py-0.5 rounded border border-accent/40 bg-accent/10 text-accent uppercase font-bold">
                  Socratic
                </span>
              </h2>
              <p className="font-mono text-[11px] text-muted truncate max-w-[240px]">
                Day {dayNumber} \u2022 Step {stepNumber}: {stepHeading}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-1.5">
            {/* Desktop Pin/Split View Toggle */}
            <button
              type="button"
              onClick={() => setIsPinned((prev) => !prev)}
              className={`hidden md:inline-flex font-mono text-xs px-2 py-1 border border-ink/30 rounded transition-colors ${
                isPinned ? "bg-ink text-bg font-bold" : "hover:border-ink bg-surface text-ink"
              }`}
              title={isPinned ? "Unpin drawer" : "Pin drawer side-by-side"}
            >
              {isPinned ? "\ud83d\udccc Pinned" : "\ud83d\udccc Pin"}
            </button>

            {/* Close Button */}
            <button
              type="button"
              onClick={onClose}
              className="font-mono text-sm font-bold w-8 h-8 rounded border border-ink/30 hover:border-ink hover:bg-ink hover:text-bg flex items-center justify-center transition-colors"
              aria-label="Close AI Mentor"
            >
              \u2715
            </button>
          </div>
        </div>

        {/* Quick Action Chips Bar */}
        <AiTeacherQuickActionBar
          onSelectAction={handleQuickAction}
          disabled={isLoading}
        />

        {/* Messages Scroll Area */}
        <div className="flex-1 overflow-y-auto px-4 py-3 space-y-2">
          {messages.map((msg) => (
            <AiTeacherMessageBubble
              key={msg.id}
              message={msg}
              onSelectAction={handleQuickAction}
            />
          ))}

          {isLoading && <AiTeacherTypingIndicator />}

          {errorMessage && (
            <div className="card p-3 my-2 border-2 border-red-500 bg-red-500/10 text-red-700 dark:text-red-400 font-mono text-xs">
              {errorMessage}
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input Bar Footer */}
        <div className="p-3 border-t-2 border-ink bg-surface shrink-0">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSendMessage();
            }}
            className="flex items-end gap-2"
          >
            <div className="flex-1 relative">
              <textarea
                ref={inputRef}
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyDown={handleInputKeyDown}
                placeholder="Ask your AI Mentor anything about this lesson..."
                rows={2}
                disabled={isLoading}
                className="w-full resize-none rounded border-2 border-ink bg-bg p-2 font-mono text-xs text-ink placeholder:text-muted focus:outline-none focus:border-accent disabled:opacity-50"
              />
              <span className="hidden sm:inline-block absolute right-2 bottom-2 font-mono text-[10px] text-muted select-none">
                \u23ce Enter
              </span>
            </div>

            <button
              type="submit"
              disabled={isLoading || !inputMessage.trim()}
              className="btn btn-primary min-h-[42px] px-4 font-mono text-xs font-bold border-2 border-ink shadow-hard-sm hover:shadow-hard disabled:opacity-40 disabled:cursor-not-allowed transition-all"
            >
              Send
            </button>
          </form>
        </div>
      </aside>
    </>
  );
}
