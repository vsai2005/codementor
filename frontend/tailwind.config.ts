import type { Config } from "tailwindcss";

/** Tokens are PRD 4.2 verbatim: flat surfaces, 2px ink borders, offset hard
 *  shadows (4px 4px 0). No gradients, no glassmorphism. */
const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        bg: "#F6F1E7",
        surface: "#FFFFFF",
        ink: "#14213D",
        accent: "#E4572E",
        "accent-2": "#17594A",
        muted: "#5A5A52",
      },
      fontFamily: {
        display: ["var(--font-display)", "Georgia", "serif"],
        body: ["var(--font-body)", "system-ui", "sans-serif"],
        mono: ["ui-monospace", "Menlo", "monospace"],
      },
      boxShadow: {
        hard: "4px 4px 0 #14213D",
        "hard-sm": "2px 2px 0 #14213D",
        "hard-accent": "4px 4px 0 #E4572E",
      },
    },
  },
  plugins: [],
};
export default config;
