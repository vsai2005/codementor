"""Adaptive difficulty engine (PRD 3.2).

Deliberately a pure function: no DB session, no FastAPI, no I/O. That makes
every rule in 3.2 table-testable, and it is the honest answer to the interview
question "how do you know the tier logic is right?"
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Sequence

MIN_TIER = 1
MAX_TIER = 5
PROMOTE_AT = 80.0
DEMOTE_BELOW = 50.0
WINDOW = 3
WEIGHTS = (0.5, 0.3, 0.2)  # most recent first

Direction = Literal["promote", "hold", "demote"]


@dataclass(frozen=True)
class TierDecision:
    tier_from: int
    tier_to: int
    rolling_score: float
    direction: Direction
    reason: str

    @property
    def changed(self) -> bool:
        return self.tier_from != self.tier_to


def compute_rolling(recent_scores: Sequence[float]) -> float:
    """Weighted average of the last <=3 scores, most recent first.

    With fewer than 3 scores the PRD says "use the average of available
    scores" -- a plain mean, not the weighted formula with missing terms,
    which would silently deflate the result toward zero.
    """
    window = list(recent_scores[:WINDOW])
    if not window:
        return 0.0
    if len(window) < WINDOW:
        return sum(window) / len(window)
    return round(sum(w * s for w, s in zip(WEIGHTS, window)), 4)


def compute_next_tier(
    current_tier: int,
    recent_scores: Sequence[float],
    last_event_was_demotion: bool = False,
) -> TierDecision:
    """Decide the next tier for one topic.

    recent_scores: most recent first. Only the first 3 are considered.
    last_event_was_demotion: cooldown flag -- blocks back-to-back demotions.
    """
    tier = _clamp(current_tier)
    rolling = compute_rolling(recent_scores)
    attempts = len(recent_scores)

    if attempts == 0:
        return TierDecision(tier, tier, 0.0, "hold", "no submissions yet")

    # --- promotion ---
    if rolling >= PROMOTE_AT:
        if attempts < WINDOW:
            return TierDecision(
                tier, tier, rolling, "hold",
                f"score {rolling:.1f} qualifies, but only {attempts} of "
                f"{WINDOW} submissions -- promotion needs a fuller sample",
            )
        if tier >= MAX_TIER:
            return TierDecision(tier, tier, rolling, "hold",
                                f"score {rolling:.1f} but already at max tier {MAX_TIER}")
        return TierDecision(tier, tier + 1, rolling, "promote",
                            f"rolling {rolling:.1f} >= {PROMOTE_AT:.0f}, promoted one step")

    # --- demotion ---
    if rolling < DEMOTE_BELOW:
        if last_event_was_demotion:
            return TierDecision(tier, tier, rolling, "hold",
                                f"rolling {rolling:.1f} below {DEMOTE_BELOW:.0f} but "
                                "cooldown blocks consecutive demotion")
        if tier <= MIN_TIER:
            return TierDecision(tier, tier, rolling, "hold",
                                f"rolling {rolling:.1f} but already at min tier {MIN_TIER}")
        return TierDecision(tier, tier - 1, rolling, "demote",
                            f"rolling {rolling:.1f} < {DEMOTE_BELOW:.0f}, demoted one step")

    # --- hold ---
    return TierDecision(tier, tier, rolling, "hold",
                        f"rolling {rolling:.1f} in hold band "
                        f"[{DEMOTE_BELOW:.0f}, {PROMOTE_AT:.0f})")


def _clamp(tier: int) -> int:
    return max(MIN_TIER, min(MAX_TIER, tier))


TIER_LABELS = {1: "Easy", 2: "Easy-Medium", 3: "Medium", 4: "Medium-Hard", 5: "Hard"}


def banner_text(decision: TierDecision) -> str:
    """The UI string required by PRD 4.4 -- the product's differentiator."""
    to_label = TIER_LABELS[decision.tier_to]
    score = int(round(decision.rolling_score))
    if decision.direction == "promote":
        return f"Score {score} → next problem moves up to {to_label}"
    if decision.direction == "demote":
        return f"Score {score} → next problem eases to {to_label}"
    return f"Score {score} → next problem stays at {to_label}"


# --- topic prioritisation (PRD 3.3) -------------------------------------

def topic_priority(avg_score: float, days_since_practiced: float | None,
                   half_life_days: float = 14.0) -> float:
    """priority = (1 - avg/100)*0.6 + recency_decay*0.4

    recency_decay grows the longer a topic goes untouched, saturating at 1.
    A never-practiced topic gets maximum recency pressure.
    """
    weakness = max(0.0, 1.0 - (avg_score / 100.0))
    if days_since_practiced is None:
        recency = 1.0
    else:
        recency = min(1.0, days_since_practiced / (half_life_days * 2))
    return round(weakness * 0.6 + recency * 0.4, 6)
