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

export function ScoreTrendChart({ points }: { points: TrendPoint[] }) {
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
            <CartesianGrid stroke="#14213D" strokeOpacity={0.12} vertical={false} />
            <XAxis dataKey="n" stroke="#14213D" tick={{ fontSize: 11 }} />
            <YAxis domain={[0, 100]} stroke="#14213D" tick={{ fontSize: 11 }} />
            <Tooltip
              contentStyle={{
                border: "2px solid #14213D",
                borderRadius: 0,
                background: "#FFFFFF",
                fontSize: 12,
              }}
            />
            <Line
              type="monotone"
              dataKey="score"
              stroke="#E4572E"
              strokeWidth={2}
              dot={{ r: 3, fill: "#14213D" }}
              isAnimationActive={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
