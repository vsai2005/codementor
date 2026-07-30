"""Table-driven tests for the adaptive difficulty engine (PRD 3.2)."""

import pytest

from app.services.difficulty import (
    TierDecision,
    banner_text,
    compute_next_tier,
    compute_rolling,
    topic_priority,
)


# (name, tier, scores_recent_first, cooldown, expected_tier, expected_direction)
CASES = [
    # PRD's own worked example
    ("prd example: 65 holds",        3, [65, 65, 65], False, 3, "hold"),
    ("three 90s promote once only",  2, [90, 90, 90], False, 3, "promote"),
    ("max tier stays capped",        5, [95, 95, 95], False, 5, "hold"),
    ("min tier stays floored",       1, [20, 20, 20], False, 1, "hold"),
    ("clear demotion",               3, [30, 40, 45], False, 2, "demote"),
    ("cooldown blocks demotion",     3, [30, 40, 45], True,  3, "hold"),
    ("two submissions never promote",3, [95, 95],     False, 3, "hold"),
    ("one submission never promotes",3, [100],        False, 3, "hold"),
    ("two low submissions demote",   3, [10, 20],     False, 2, "demote"),
    ("boundary 80 promotes",         2, [80, 80, 80], False, 3, "promote"),
    ("boundary 79.9 holds",          2, [80, 80, 79], False, 2, "hold"),
    ("boundary 50 holds",            3, [50, 50, 50], False, 3, "hold"),
    ("boundary 49 demotes",          3, [49, 49, 49], False, 2, "demote"),
    ("no history holds",             3, [],           False, 3, "hold"),
]


@pytest.mark.parametrize("name,tier,scores,cooldown,want_tier,want_dir", CASES)
def test_tier_table(name, tier, scores, cooldown, want_tier, want_dir):
    d = compute_next_tier(tier, scores, cooldown)
    assert d.tier_to == want_tier, f"{name}: {d.reason}"
    assert d.direction == want_dir, f"{name}: {d.reason}"
    assert 1 <= d.tier_to <= 5


def test_rolling_weights_match_hand_calculation():
    # 0.5*90 + 0.3*60 + 0.2*30 = 45 + 18 + 6 = 69
    assert compute_rolling([90, 60, 30]) == pytest.approx(69.0)
    # most recent dominates: same scores reversed gives a very different answer
    assert compute_rolling([30, 60, 90]) == pytest.approx(51.0)


def test_fewer_than_three_uses_plain_average_not_deflated_weights():
    # Weighted formula on 2 items would give 0.5*80+0.3*80 = 64 -- wrong.
    assert compute_rolling([80, 80]) == pytest.approx(80.0)
    assert compute_rolling([100]) == pytest.approx(100.0)


def test_only_last_three_scores_are_considered():
    assert compute_rolling([90, 90, 90, 0, 0, 0]) == pytest.approx(90.0)


def test_promotion_is_one_step_even_with_perfect_scores():
    d = compute_next_tier(1, [100, 100, 100])
    assert d.tier_to == 2, "must not jump multiple tiers"


def test_consecutive_demotions_demote_once_then_cooldown_blocks():
    first = compute_next_tier(4, [40, 40, 40], last_event_was_demotion=False)
    assert first.direction == "demote" and first.tier_to == 3

    second = compute_next_tier(
        first.tier_to, [35, 40, 40], last_event_was_demotion=(first.direction == "demote")
    )
    assert second.direction == "hold", "cooldown must block back-to-back demotion"
    assert second.tier_to == 3

    third = compute_next_tier(
        second.tier_to, [35, 35, 40], last_event_was_demotion=(second.direction == "demote")
    )
    assert third.direction == "demote", "cooldown lifts after one held submission"
    assert third.tier_to == 2


def test_tiers_are_independent_across_topics():
    arrays = compute_next_tier(4, [90, 90, 90])
    graphs = compute_next_tier(2, [30, 30, 30])
    assert arrays.tier_to == 5
    assert graphs.tier_to == 1
    assert arrays.tier_to != graphs.tier_to


def test_every_decision_carries_a_reason_for_the_events_table():
    # A difficulty_events row is written for EVERY submission, including
    # no-change ones -- so a hold must still explain itself.
    d = compute_next_tier(3, [65, 65, 65])
    assert not d.changed
    assert d.reason and len(d.reason) > 10
    assert d.rolling_score == pytest.approx(65.0)


def test_banner_text_matches_the_prd_string():
    d = compute_next_tier(3, [65, 65, 65])
    assert banner_text(d) == "Score 65 → next problem stays at Medium"
    assert "moves up" in banner_text(compute_next_tier(2, [90, 90, 90]))
    assert "eases" in banner_text(compute_next_tier(3, [30, 30, 30]))


def test_topic_priority_favours_weak_and_stale_topics():
    weak_stale = topic_priority(avg_score=30, days_since_practiced=40)
    strong_fresh = topic_priority(avg_score=95, days_since_practiced=0)
    never_touched = topic_priority(avg_score=50, days_since_practiced=None)

    assert weak_stale > strong_fresh
    assert never_touched > topic_priority(50, days_since_practiced=0)
    assert 0.0 <= strong_fresh <= 1.0


def test_convergence_simulation_reaches_true_level_within_five_problems():
    """PRD success criterion: converges to the user's real level in <=5 problems.

    Simulated user is genuinely a tier-4 solver: they score high below their
    level, middling at it, and poorly above it.
    """
    def score_for(tier: int) -> float:
        return {1: 98, 2: 95, 3: 88, 4: 66, 5: 35}[tier]

    tier, scores, cooldown = 1, [], False
    trajectory = [tier]
    for _ in range(10):
        scores.insert(0, score_for(tier))
        d = compute_next_tier(tier, scores, cooldown)
        cooldown = d.direction == "demote"
        tier = d.tier_to
        trajectory.append(tier)

    assert trajectory[-1] == 4, trajectory
    assert trajectory[7] == 4, f"did not settle by submission 7: {trajectory}"
    assert max(trajectory) <= 5 and min(trajectory) >= 1
