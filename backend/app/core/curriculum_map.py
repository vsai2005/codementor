"""Curriculum to Practice mapping for the 160-day Python roadmap.

CURRICULUM_DAY_PRACTICE (day -> practice problem slug) is the single authoritative
source. The reverse lookup is derived from it at import time and is never written by
hand, so it cannot drift. A slug may be the practice problem of several days (e.g. a
problem revisited in a later review day); the reverse lookup therefore maps each slug to
ALL of its days, and callers must never assume a slug belongs to exactly one day.
"""

from __future__ import annotations

from types import MappingProxyType
from typing import Mapping

CURRICULUM_DAY_PRACTICE = {1: 'celsius-to-fahrenheit', 2: 'time-converter-seconds', 3: 'slice-url-domain', 4: 'leap-year-checker', 5: 'sum-multiples-loop', 6: 'count-loop-operations', 7: 'common-keys-intersection', 8: 'recursive-sum-digits', 9: 'flatten-2d-matrix', 10: 'vector2d-operations', 11: 'remove-element', 12: 'merge-sorted-array', 13: 'group-by-parity', 14: 'find-the-difference', 15: 'string-to-integer-atoi', 16: 'sliding-window-deque', 17: 'power-of-three', 18: 'powx-n', 19: 'subsets-recursive', 20: 'generate-parentheses', 21: 'palindrome-number', 22: 'sort-colors', 23: 'contains-duplicate', 24: 'two-sum', 25: 'valid-anagram', 26: 'running-sum', 27: 'range-sum-query-immutable', 28: 'range-sum-query-2d-immutable', 29: 'max-consecutive-ones', 30: 'product-except-self', 31: 'merge-intervals', 32: 'move-zeroes', 33: 'max-subarray', 34: 'longest-common-prefix', 35: 'reverse-words', 36: 'valid-palindrome', 37: 'two-sum-sorted', 38: 'three-sum', 39: 'container-most-water', 40: 'trapping-rain-water', 41: 'sorted-squares', 42: 'longest-substring', 43: 'maximum-average-subarray-i', 44: 'minimum-size-subarray-sum', 45: 'repeated-dna-sequences', 46: 'majority-element', 47: 'rotate-array', 48: 'find-disappeared', 49: 'sort-by-parity', 50: 'trapping-rain-water', 51: 'binary-search', 52: 'search-insert-position', 53: 'search-range', 54: 'search-rotated', 55: 'insertion-sort-list-array', 56: 'sort-an-array', 57: 'sort-colors', 58: 'kth-largest-element-in-an-array', 59: 'relative-sort-array', 60: 'sort-an-array', 61: 'find-min-rotated', 62: 'find-peak', 63: 'count-negatives', 64: 'koko-bananas', 65: 'median-two-arrays', 66: 'design-hashmap', 67: 'group-anagrams', 68: 'first-unique-char', 69: 'subarray-sum-k', 70: 'longest-consecutive-sequence', 71: 'insert-delete-getrandom-o1', 72: 'lru-cache', 73: 'longest-palindrome', 74: 'count-vowels', 75: 'longest-consecutive-sequence', 76: 'reverse-list', 77: 'reverse-linked-list', 78: 'middle-of-the-linked-list', 79: 'merge-two-sorted-linked-lists', 80: 'merge-sorted-lists', 81: 'linked-list-cycle', 82: 'linked-list-cycle-ii', 83: 'remove-nth-node-from-end', 84: 'remove-linked-list-elements', 85: 'reverse-nodes-in-k-group', 86: 'valid-parentheses', 87: 'valid-parentheses', 88: 'min-stack-ops', 89: 'design-circular-queue', 90: 'implement-queue-using-stacks', 91: 'daily-temperatures', 92: 'asteroid-collision', 93: 'sliding-window-maximum', 94: 'eval-rpn', 95: 'simplify-path', 96: 'binary-tree-inorder-traversal', 97: 'maximum-depth-of-binary-tree', 98: 'invert-binary-tree', 99: 'binary-tree-level-order-traversal', 100: 'symmetric-tree', 101: 'validate-binary-search-tree', 102: 'kth-smallest-element-in-a-bst', 103: 'lowest-common-ancestor-of-a-binary-tree', 104: 'serialize-and-deserialize-binary-tree', 105: 'same-tree', 106: 'balanced-binary-tree', 107: 'lowest-common-ancestor-of-a-bst', 108: 'implement-trie-prefix-tree', 109: 'design-add-and-search-words', 110: 'validate-binary-search-tree', 111: 'last-stone-weight', 112: 'kth-largest-element-in-a-stream', 113: 'k-closest-points-to-origin', 114: 'top-k-frequent-elements', 115: 'merge-k-sorted-lists', 116: 'find-median-from-data-stream', 117: 'task-scheduler', 118: 'find-k-pairs-with-smallest-sums', 119: 'find-median-from-data-stream', 120: 'merge-k-sorted-lists', 121: 'find-judge', 122: 'valid-path', 123: 'flood-fill', 124: 'course-schedule', 125: 'course-schedule-ii', 126: 'keys-and-rooms', 127: 'is-graph-bipartite', 128: 'network-delay-time', 129: 'cheapest-flights-within-k-stops', 130: 'redundant-connection', 131: 'min-cost-to-connect-all-points', 132: 'min-cost-to-connect-all-points', 133: 'critical-connections-in-a-network', 134: 'critical-connections-in-a-network', 135: 'number-of-islands', 136: 'maximum-units-on-a-truck', 137: 'non-overlapping-intervals', 138: 'maximum-units-on-a-truck', 139: 'minimum-deletions-to-make-character-frequencies-unique', 140: 'jump-game', 141: 'partition-labels', 142: 'gas-station', 143: 'candy', 144: 'jump-game-ii', 145: 'candy', 146: 'climbing-stairs', 147: 'house-robber', 148: 'unique-paths', 149: 'partition-equal-subset-sum', 150: 'coin-change', 151: 'longest-increasing-subsequence', 152: 'longest-common-subsequence', 153: 'edit-distance', 154: 'coin-change-ii', 155: 'minimum-path-sum', 156: 'number-of-1-bits', 157: 'n-queens', 158: 'range-sum-query-mutable', 159: 'word-search-ii', 160: 'lfu-cache'}


def _derive_slug_to_days(forward: Mapping[int, str]) -> Mapping[str, tuple[int, ...]]:
    reverse: dict[str, list[int]] = {}
    for day in sorted(forward):
        reverse.setdefault(forward[day], []).append(day)
    return MappingProxyType({slug: tuple(days) for slug, days in reverse.items()})


# Derived, read-only: slug -> every curriculum day (ascending) whose practice problem it is.
PRACTICE_SLUG_TO_DAYS: Mapping[str, tuple[int, ...]] = _derive_slug_to_days(CURRICULUM_DAY_PRACTICE)


def practice_days_for_slug(slug: str) -> tuple[int, ...]:
    """All curriculum days whose practice problem is `slug` (empty if none)."""
    return PRACTICE_SLUG_TO_DAYS.get(slug, ())


def is_practice_for_day(slug: str, day_number: int) -> bool:
    """True only if `slug` is the authoritative practice problem of `day_number`."""
    return CURRICULUM_DAY_PRACTICE.get(day_number) == slug
