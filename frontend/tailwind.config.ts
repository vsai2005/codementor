import type { Config } from "tailwindcss";

/** Tokens are PRD 4.2 verbatim: flat surfaces, 2px ink borders, offset hard
 *  shadows (4px 4px 0). No gradients, no glassmorphism. */
const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        // Colors resolve from CSS variables (RGB channel triplets) so the whole
        // palette — solids AND /alpha utilities — flips with [data-theme].
        bg: "rgb(var(--bg) / <alpha-value>)",
        surface: "rgb(var(--surface) / <alpha-value>)",
        ink: "rgb(var(--ink) / <alpha-value>)",
        accent: "rgb(var(--accent) / <alpha-value>)",
        "accent-2": "rgb(var(--accent-2) / <alpha-value>)",
        muted: "rgb(var(--muted) / <alpha-value>)",
      },
      fontFamily: {
        display: ["var(--font-display)", "Georgia", "serif"],
        body: ["var(--font-body)", "system-ui", "sans-serif"],
        mono: ["ui-monospace", "Menlo", "monospace"],
      },
      boxShadow: {
        // The hard shadow follows --ink, so it becomes a light offset on dark bg.
        hard: "4px 4px 0 rgb(var(--ink))",
        "hard-sm": "2px 2px 0 rgb(var(--ink))",
        "hard-accent": "4px 4px 0 rgb(var(--accent))",
      },
    },
  },
  plugins: [],
};
export default config;
