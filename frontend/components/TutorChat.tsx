"use client";

import { useRef, useState } from "react";

import { ApiError, api } from "@/lib/api";
import type { MemoryNote } from "@/lib/types";
import { MemoryNoteCard } from "./MemoryNoteCard";

interface Turn {
  role: "user" | "tutor";
  text: string;
  notes?: MemoryNote[];
}

export function TutorChat({ problemId }: { problemId?: string }) {
  const [turns, setTurns] = useState<Turn[]>([]);
  const [draft, setDraft] = useState("");
  const [sending, setSending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const inFlight = useRef(false);

  const send = async () => {
    const message = draft.trim();
    if (message === "" || inFlight.current) return;

    inFlight.current = true;
    setSending(true);
    setError(null);
    setTurns((prev) => [...prev, { role: "user", text: message }]);
    setDraft("");

    try {
      const result = await api.tutor(
        problemId ? { message, problem_id: problemId } : { message },
      );
      setTurns((prev) => [
        ...prev,
        { role: "tutor", text: result.reply, notes: result.retrieved_notes },
      ]);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "The tutor is unreachable right now.");
    } finally {
      inFlight.current = false;
      setSending(false);
    }
  };

  return (
    <div className="flex h-full flex-col gap-3">
      <div className="flex-1 space-y-3 overflow-y-auto" aria-live="polite">
        {turns.length === 0 && (
          <p className="font-body text-sm text-muted">
            Ask about a problem, a concept, or what you keep getting wrong.
          </p>
        )}

        {turns.map((turn, i) => (
          <div key={i} className="space-y-2">
            <div
              className={`card-flat p-3 ${turn.role === "user" ? "bg-bg" : "bg-surface"}`}
            >
              <p className="label mb-1">{turn.role === "user" ? "You" : "Tutor"}</p>
              <p className="whitespace-pre-wrap font-body text-sm leading-relaxed">
                {turn.text}
              </p>
            </div>

            {turn.notes && turn.notes.length > 0 && (
              <div className="space-y-2 pl-3">
                {turn.notes.map((note) => (
                  <MemoryNoteCard key={note.id} note={note} />
                ))}
              </div>
            )}
          </div>
        ))}

        {sending && <p className="font-body text-sm text-muted">Thinking…</p>}
        {error && (
          <p className="card-flat border-l-4 border-l-accent p-3 font-body text-sm" role="alert">
            {error}
          </p>
        )}
      </div>

      <div className="flex gap-2">
        <textarea
          value={draft}
          onChange={(event) => setDraft(event.target.value)}
          onKeyDown={(event) => {
            if (event.key === "Enter" && !event.shiftKey) {
              event.preventDefault();
              void send();
            }
          }}
          rows={2}
          placeholder="Ask your tutor…"
          className="min-w-0 flex-1 resize-none border-2 border-ink bg-surface p-2 font-body text-sm outline-none focus:shadow-hard-sm"
        />
        <button type="button" className="btn btn-primary" onClick={send} disabled={sending}>
          Send
        </button>
      </div>
    </div>
  );
}
