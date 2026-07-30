"use client";

import { useEffect, useRef, useState } from "react";

const PREFIX = "codementor.draft.";
const INTERVAL_MS = 2000;

/** Autosave to localStorage every 2s and restore on mount (PRD 4.4).
 *
 *  Writes on an interval rather than on every keystroke so a fast typist does
 *  not thrash localStorage, and only when the text has actually changed since
 *  the last write. */
export function useAutosave(
  problemId: string,
  code: string,
): { restored: string | null; clearDraft: () => void; savedAt: number | null } {
  const [restored, setRestored] = useState<string | null>(null);
  const [savedAt, setSavedAt] = useState<number | null>(null);
  const latest = useRef(code);
  const lastWritten = useRef<string | null>(null);

  latest.current = code;

  useEffect(() => {
    try {
      const stored = window.localStorage.getItem(PREFIX + problemId);
      setRestored(stored);
      lastWritten.current = stored;
    } catch {
      setRestored(null);
    }
  }, [problemId]);

  useEffect(() => {
    const write = () => {
      const value = latest.current;
      if (value === lastWritten.current) return;
      try {
        window.localStorage.setItem(PREFIX + problemId, value);
        lastWritten.current = value;
        setSavedAt(Date.now());
      } catch {
        /* quota exceeded or storage disabled — losing the draft is bad but
           crashing the editor is worse */
      }
    };

    const timer = window.setInterval(write, INTERVAL_MS);
    // Also flush on tab close, where the interval will not fire in time.
    window.addEventListener("beforeunload", write);
    return () => {
      window.clearInterval(timer);
      window.removeEventListener("beforeunload", write);
      write();
    };
  }, [problemId]);

  const clearDraft = () => {
    try {
      window.localStorage.removeItem(PREFIX + problemId);
      lastWritten.current = null;
    } catch {
      /* ignore */
    }
  };

  return { restored, clearDraft, savedAt };
}
