"use client";

import { useEffect, useState } from "react";

export type Theme = "light" | "dark";

const STORAGE_KEY = "codementor.theme";

function currentTheme(): Theme {
  if (typeof document === "undefined") return "light";
  return document.documentElement.dataset.theme === "dark" ? "dark" : "light";
}

/** Apply a theme everywhere: stamp <html>, persist it, and notify subscribers. */
export function applyTheme(theme: Theme): void {
  document.documentElement.dataset.theme = theme;
  try {
    localStorage.setItem(STORAGE_KEY, theme);
  } catch {
    /* private mode / storage disabled — theme still applies for this session */
  }
  window.dispatchEvent(new CustomEvent("themechange", { detail: theme }));
}

/**
 * Reads the active theme (set pre-paint by the inline script in layout.tsx) and
 * re-renders when it changes. `toggle` flips light/dark; components like the
 * Monaco editor read `theme` to pick their own dark variant.
 */
export function useTheme() {
  // Start "light" to match the server render, then sync on mount to avoid a
  // hydration mismatch.
  const [theme, setTheme] = useState<Theme>("light");

  useEffect(() => {
    setTheme(currentTheme());
    const onChange = () => setTheme(currentTheme());
    window.addEventListener("themechange", onChange);
    return () => window.removeEventListener("themechange", onChange);
  }, []);

  const toggle = () => applyTheme(theme === "dark" ? "light" : "dark");

  return { theme, toggle, setTheme: applyTheme };
}
