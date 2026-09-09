"use client";

import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import type { TrendPoint } from "@/lib/types";
import { useTheme } from "@/lib/useTheme";

// Recharts can't read Tailwind classes, so it gets the palette explicitly per
// theme. Kept in sync with the CSS variables in globals.css.
const PALETTE = {
  light: { ink: "#14213D", surface: "#FFFFFF", accent: "#E4572E" },
  dark: { ink: "#F2EDE3", surface: "#26231F", accent: "#F0764E" },
};

export function ScoreTrendChart({ points }: { points: TrendPoint[] }) {
  const { theme } = useTheme();
  const c = PALETTE[theme];

  if (points.length === 0) {
    return (
      <div className="card-flat p-4">
        <p className="font-body text-sm text-muted">No submissions yet.</p>
      </div>
    );
  }

  const data = points.map((point, index) => ({
    n: index + 1,
    score: point.overall_score,
  }));

  return (
    <div className="card p-3">
      <p className="label mb-2">Score trend</p>
      <div className="h-56 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data} margin={{ top: 4, right: 8, bottom: 4, left: -18 }}>
            <CartesianGrid stroke={c.ink} strokeOpacity={0.12} vertical={false} />
            <XAxis dataKey="n" stroke={c.ink} tick={{ fontSize: 11, fill: c.ink }} />
            <YAxis domain={[0, 100]} stroke={c.ink} tick={{ fontSize: 11, fill: c.ink }} />
            <Tooltip
              contentStyle={{
                border: `2px solid ${c.ink}`,
                borderRadius: 0,
                background: c.surface,
                color: c.ink,
                fontSize: 12,
              }}
            />
            <Line
              type="monotone"
              dataKey="score"
              stroke={c.accent}
              strokeWidth={2}
              dot={{ r: 3, fill: c.ink }}
              isAnimationActive={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
