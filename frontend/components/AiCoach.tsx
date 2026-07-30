"use client";

import { useEffect, useRef, useState } from "react";

import { ApiError, api } from "@/lib/api";
import type { ProblemDetail, Review, TestsResponse } from "@/lib/types";

interface Turn {
  role: "you" | "coach";
  text: string;
  tone?: "debrief";
}

/** A finished submission the coach should debrief. `key` changes per submit. */
export interface CoachSubmission {
  key: string;
  review: Review;
  tests: TestsResponse;
  plan?: string;
}

const QUICK_ASKS = [
  { label: "💡 Give me a hint", message: "Give me a small hint to move forward — don't solve it for me." },
  { label: "🔍 What's wrong?", message: "Look at my current code and tell me what's wrong or what edge case I'm missing." },
  { label: "⚡ How do I optimize?", message: "How can I make my current approach faster or use less memory?" },
];

export function AiCoach({
  problem,
  code,
  submission,
}: {
  problem: ProblemDetail;
  code: string;
  submission: CoachSubmission | null;
}) {
  const [turns, setTurns] = useState<Turn[]>([]);
  const [draft, setDraft] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const inFlight = useRef(false);
  const lastDebriefed = useRef<string | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);

  // Always send the freshest code, even mid-request, without re-creating send().
  const codeRef = useRef(code);
  codeRef.current = code;

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight });
  }, [turns, busy]);

  // Auto-debrief once per new submission: praise + where to improve.
  useEffect(() => {
    if (!submission || submission.key === lastDebriefed.current) return;
    lastDebriefed.current = submission.key;
    let cancelled = false;

    setBusy(true);
    setError(null);
    api
      .coach({
        problem_id: problem.id,
        code: codeRef.current,
        review: submission.review,
        tests: submission.tests,
        plan: submission.plan,
      })
      .then((res) => {
        if (!cancelled) {
          setTurns((prev) => [...prev, { role: "coach", text: res.message, tone: "debrief" }]);
        }
      })
      .catch(() => {
        if (!cancelled) {
          setTurns((prev) => [
            ...prev,
            {
              role: "coach",
              text: "Great effort getting a submission in! I couldn't reach my full brain for the debrief — check the Review tab for your scores, then ask me anything here.",
              tone: "debrief",
            },
          ]);
        }
      })
      .finally(() => !cancelled && setBusy(false));

    return () => {
      cancelled = true;
    };
  }, [submission, problem.id]);

  const ask = async (message: string) => {
    const text = message.trim();
    if (text === "" || inFlight.current) return;

    inFlight.current = true;
    setBusy(true);
    setError(null);
    setTurns((prev) => [...prev, { role: "you", text }]);
    setDraft("");

    try {
      const res = await api.tutor({ message: text, problem_id: problem.id, code: codeRef.current });
      setTurns((prev) => [...prev, { role: "coach", text: res.reply }]);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Your coach is unreachable right now.");
    } finally {
      inFlight.current = false;
      setBusy(false);
    }
  };

  return (
    <div className="flex h-full flex-col gap-3">
      <div className="flex items-center gap-2">
        <span className="text-lg" aria-hidden>
          🤖
        </span>
        <p className="font-display text-base font-bold">AI Coach</p>
      </div>

      <div ref={scrollRef} className="flex-1 space-y-3 overflow-y-auto pr-1" aria-live="polite">
        {turns.length === 0 && !busy && (
          <p className="font-body text-sm text-muted">
            I can see your code. Stuck? Ask for a hint, or tap a button below. After you submit,
            I&apos;ll tell you what you nailed and where to level up. 🚀
          </p>
        )}

        {turns.map((turn, i) => (
          <div
            key={i}
            className={
              turn.tone === "debrief"
                ? "card-flat border-l-4 border-l-accent-2 bg-surface p-3"
                : `card-flat p-3 ${turn.role === "you" ? "bg-bg" : "bg-surface"}`
            }
          >
            <p className="label mb-1">
              {turn.role === "you" ? "You" : turn.tone === "debrief" ? "Coach · debrief" : "Coach"}
            </p>
            <p className="whitespace-pre-wrap font-body text-sm leading-relaxed">{turn.text}</p>
          </div>
        ))}

        {busy && <p className="font-body text-sm text-muted">Thinking…</p>}
        {error && (
          <p className="card-flat border-l-4 border-l-accent p-3 font-body text-sm" role="alert">
            {error}
          </p>
        )}
      </div>

      <div className="flex flex-wrap gap-2">
        {QUICK_ASKS.map((q) => (
          <button
            key={q.label}
            type="button"
            className="btn px-2 py-1 text-xs"
            onClick={() => ask(q.message)}
            disabled={busy}
          >
            {q.label}
          </button>
        ))}
      </div>

      <div className="flex gap-2">
        <textarea
          value={draft}
          onChange={(e) => setDraft(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              void ask(draft);
            }
          }}
          rows={2}
          placeholder="Ask your coach anything…"
          className="min-w-0 flex-1 resize-none border-2 border-ink bg-surface p-2 font-body text-sm outline-none focus:shadow-hard-sm"
        />
        <button
          type="button"
          className="btn btn-primary"
          onClick={() => ask(draft)}
          disabled={busy}
        >
          Send
        </button>
      </div>
    </div>
  );
}
