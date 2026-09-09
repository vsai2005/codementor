"use client";

import { useCallback, useEffect, useRef, useState } from "react";

const PREFIX = "codementor.draft.";
const DEBOUNCE_MS = 1200;

/**
 * Race-condition-free autosave with trailing debounce and request cancellation (Phase 5).
 *
 * Uses `useRef` to maintain:
 *  - latestCodeRef: latest buffer state
 *  - abortControllerRef: aborts in-flight save operations
 *  - debounceTimerRef: 1,200ms trailing debounce
 */
export function useAutosave(
  problemId: string,
  code: string,
): { restored: string | null; clearDraft: () => void; savedAt: number | null } {
  const [restored, setRestored] = useState<string | null>(null);
  const [savedAt, setSavedAt] = useState<number | null>(null);

  const latestCodeRef = useRef(code);
  const lastWrittenRef = useRef<string | null>(null);
  const debounceTimerRef = useRef<NodeJS.Timeout | null>(null);
  const abortControllerRef = useRef<AbortController | null>(null);

  latestCodeRef.current = code;

  // Restore on mount
  useEffect(() => {
    try {
      const stored = window.localStorage.getItem(PREFIX + problemId);
      setRestored(stored);
      lastWrittenRef.current = stored;
    } catch {
      setRestored(null);
    }
  }, [problemId]);

  // 1,200ms trailing debounce with cancellation
  useEffect(() => {
    if (debounceTimerRef.current) {
      clearTimeout(debounceTimerRef.current);
    }

    debounceTimerRef.current = setTimeout(() => {
      const currentCode = latestCodeRef.current;
      if (currentCode === lastWrittenRef.current) return;

      // Cancel any prior in-flight save controller
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
      abortControllerRef.current = new AbortController();

      try {
        window.localStorage.setItem(PREFIX + problemId, currentCode);
        lastWrittenRef.current = currentCode;
        setSavedAt(Date.now());
      } catch {
        /* quota exceeded or storage disabled */
      }
    }, DEBOUNCE_MS);

    return () => {
      if (debounceTimerRef.current) {
        clearTimeout(debounceTimerRef.current);
      }
    };
  }, [code, problemId]);

  // Flush on unload
  useEffect(() => {
    const handleBeforeUnload = () => {
      const currentCode = latestCodeRef.current;
      if (currentCode !== lastWrittenRef.current) {
        try {
          window.localStorage.setItem(PREFIX + problemId, currentCode);
          lastWrittenRef.current = currentCode;
        } catch {
          /* ignore */
        }
      }
    };

    window.addEventListener("beforeunload", handleBeforeUnload);
    return () => {
      window.removeEventListener("beforeunload", handleBeforeUnload);
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
    };
  }, [problemId]);

  const clearDraft = useCallback(() => {
    try {
      window.localStorage.removeItem(PREFIX + problemId);
      lastWrittenRef.current = null;
    } catch {
      /* ignore */
    }
  }, [problemId]);

  return { restored, clearDraft, savedAt };
}
