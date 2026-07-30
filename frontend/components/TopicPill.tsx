import { TIER_LABELS } from "@/lib/types";

export function TopicPill({ label, tier }: { label: string; tier?: number }) {
  return (
    <span className="inline-flex items-center gap-1 border-2 border-ink bg-surface px-2 py-0.5 font-body text-xs font-semibold">
      {label}
      {tier !== undefined && (
        <span className="text-muted">· {TIER_LABELS[tier] ?? `T${tier}`}</span>
      )}
    </span>
  );
}
