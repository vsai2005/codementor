interface ScoreBarProps {
  label: string;
  value: number;
  weight?: number;
}

/** Flat bar, 2px ink border, no gradient fill. */
export function ScoreBar({ label, value, weight }: ScoreBarProps) {
  const clamped = Math.max(0, Math.min(100, value));
  const fill = clamped >= 80 ? "bg-accent-2" : clamped >= 50 ? "bg-accent" : "bg-ink";

  return (
    <div>
      <div className="mb-1 flex items-baseline justify-between gap-2">
        <span className="font-body text-sm font-medium">
          {label}
          {weight !== undefined && (
            <span className="ml-1 text-xs text-muted">{Math.round(weight * 100)}%</span>
          )}
        </span>
        <span className="font-mono text-sm tabular-nums">{clamped}</span>
      </div>
      <div
        className="h-3 w-full border-2 border-ink bg-surface"
        role="meter"
        aria-valuenow={clamped}
        aria-valuemin={0}
        aria-valuemax={100}
        aria-label={label}
      >
        <div className={`h-full ${fill}`} style={{ width: `${clamped}%` }} />
      </div>
    </div>
  );
}
