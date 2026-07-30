"""Seed topics and problems.

Idempotent: re-running upserts by slug rather than duplicating.

Inventory note: the PRD's Phase 1 asks for 40-60 problems while BUILD_PROMPTS
asks for 12. This seeds 18 (3 per topic, tiers 1-5). That is enough to
demonstrate adaptive difficulty, but /api/problems/next widens its tier search
when a tier is empty precisely because 18 problems cannot fill 6 topics x 5
tiers. Add problems before claiming the adaptive engine is fully exercised.

Run:  python -m app.seed
"""

from __future__ import annotations

import uuid

from sqlalchemy import select

from app.database import SessionLocal
from app.models.models import Problem, Topic

TOPICS = [
    ("arrays", "Arrays & Hashing"),
    ("two-pointers", "Two Pointers"),
    ("strings", "Strings"),
    ("stacks", "Stacks & Queues"),
    ("binary-search", "Binary Search"),
    ("graphs", "Graphs & Trees"),
]


def P(slug, title, topic, tier, entry, statement, constraints,
      opt_t, opt_s, starter, cases):
    return {
        "slug": slug, "title": title, "topic": topic, "difficulty_tier": tier,
        "entry_point": entry, "statement_md": statement, "constraints_md": constraints,
        "optimal_time": opt_t, "optimal_space": opt_s,
        "starter_code": {"python": starter}, "test_cases": cases,
    }


PROBLEMS = [
    # --- arrays -----------------------------------------------------------
    P("contains-duplicate", "Contains Duplicate", "arrays", 1, "contains_duplicate",
      "Given an integer array `nums`, return `true` if any value appears at least twice.",
      "- `0 <= len(nums) <= 10^5`\n- `-10^9 <= nums[i] <= 10^9`", "O(n)", "O(n)",
      "def contains_duplicate(nums):\n    pass\n",
      [{"args": [[1, 2, 3, 1]], "expected": True},
       {"args": [[1, 2, 3, 4]], "expected": False},
       {"args": [[]], "expected": False},
       {"args": [[7]], "expected": False},
       {"args": [[0, 0]], "expected": True},
       {"args": [[-1, -1, 5]], "expected": True}]),

    P("two-sum", "Two Sum", "arrays", 2, "two_sum",
      "Given `nums` and `target`, return indices of the two numbers summing to "
      "`target`. Return `[]` if none exist.",
      "- Exactly one valid answer when one exists\n- `0 <= len(nums) <= 10^4`",
      "O(n)", "O(n)",
      "def two_sum(nums, target):\n    pass\n",
      [{"args": [[2, 7, 11, 15], 9], "expected": [0, 1]},
       {"args": [[3, 2, 4], 6], "expected": [1, 2]},
       {"args": [[3, 3], 6], "expected": [0, 1]},
       {"args": [[], 0], "expected": []},
       {"args": [[1], 1], "expected": []},
       {"args": [[-3, 4, 3, 90], 0], "expected": [0, 2]}]),

    P("product-except-self", "Product of Array Except Self", "arrays", 4,
      "product_except_self",
      "Return an array where `out[i]` is the product of all elements except "
      "`nums[i]`. Do it without division.",
      "- `1 <= len(nums) <= 10^5`\n- Products fit in 32 bits", "O(n)", "O(1)",
      "def product_except_self(nums):\n    pass\n",
      [{"args": [[1, 2, 3, 4]], "expected": [24, 12, 8, 6]},
       {"args": [[-1, 1, 0, -3, 3]], "expected": [0, 0, 9, 0, 0]},
       {"args": [[1, 1]], "expected": [1, 1]},
       {"args": [[5]], "expected": [1]},
       {"args": [[0, 0]], "expected": [0, 0]},
       {"args": [[2, 3, 4, 5]], "expected": [60, 40, 30, 24]}]),

    # --- two pointers -----------------------------------------------------
    P("reverse-list", "Reverse a List", "two-pointers", 1, "reverse_list",
      "Reverse a list in place and return it.",
      "- `0 <= len(items) <= 10^5`", "O(n)", "O(1)",
      "def reverse_list(items):\n    pass\n",
      [{"args": [[1, 2, 3]], "expected": [3, 2, 1]},
       {"args": [[]], "expected": []},
       {"args": [[1]], "expected": [1]},
       {"args": [[1, 2]], "expected": [2, 1]},
       {"args": [[5, 5, 5]], "expected": [5, 5, 5]}]),

    P("valid-palindrome", "Valid Palindrome", "two-pointers", 2, "is_palindrome",
      "Return `true` if `s` is a palindrome, considering only alphanumeric "
      "characters and ignoring case.",
      "- `0 <= len(s) <= 2 * 10^5`", "O(n)", "O(1)",
      "def is_palindrome(s):\n    pass\n",
      [{"args": ["A man, a plan, a canal: Panama"], "expected": True},
       {"args": ["race a car"], "expected": False},
       {"args": [""], "expected": True},
       {"args": [" "], "expected": True},
       {"args": ["ab_a"], "expected": True},
       {"args": ["0P"], "expected": False}]),

    P("container-most-water", "Container With Most Water", "two-pointers", 4,
      "max_area",
      "Given heights, find two lines forming a container holding the most water.",
      "- `2 <= len(height) <= 10^5`", "O(n)", "O(1)",
      "def max_area(height):\n    pass\n",
      [{"args": [[1, 8, 6, 2, 5, 4, 8, 3, 7]], "expected": 49},
       {"args": [[1, 1]], "expected": 1},
       {"args": [[4, 3, 2, 1, 4]], "expected": 16},
       {"args": [[1, 2, 1]], "expected": 2},
       {"args": [[0, 0]], "expected": 0},
       {"args": [[2, 3, 4, 5, 18, 17, 6]], "expected": 17}]),

    # --- strings ----------------------------------------------------------
    P("count-vowels", "Count Vowels", "strings", 1, "count_vowels",
      "Return the number of vowels (a, e, i, o, u, case-insensitive) in `s`.",
      "- `0 <= len(s) <= 10^5`", "O(n)", "O(1)",
      "def count_vowels(s):\n    pass\n",
      [{"args": ["hello"], "expected": 2},
       {"args": [""], "expected": 0},
       {"args": ["xyz"], "expected": 0},
       {"args": ["AEIOU"], "expected": 5},
       {"args": ["aAeE"], "expected": 4}]),

    P("valid-anagram", "Valid Anagram", "strings", 2, "is_anagram",
      "Return `true` if `t` is an anagram of `s`.",
      "- `0 <= len(s), len(t) <= 5 * 10^4`\n- Lowercase English letters",
      "O(n)", "O(1)",
      "def is_anagram(s, t):\n    pass\n",
      [{"args": ["anagram", "nagaram"], "expected": True},
       {"args": ["rat", "car"], "expected": False},
       {"args": ["", ""], "expected": True},
       {"args": ["a", "ab"], "expected": False},
       {"args": ["aacc", "ccac"], "expected": False},
       {"args": ["ab", "ba"], "expected": True}]),

    P("longest-substring", "Longest Substring Without Repeating Characters",
      "strings", 4, "length_of_longest_substring",
      "Return the length of the longest substring without repeating characters.",
      "- `0 <= len(s) <= 5 * 10^4`", "O(n)", "O(min(n, m))",
      "def length_of_longest_substring(s):\n    pass\n",
      [{"args": ["abcabcbb"], "expected": 3},
       {"args": ["bbbbb"], "expected": 1},
       {"args": ["pwwkew"], "expected": 3},
       {"args": [""], "expected": 0},
       {"args": [" "], "expected": 1},
       {"args": ["dvdf"], "expected": 3}]),

    # --- stacks -----------------------------------------------------------
    P("valid-parentheses", "Valid Parentheses", "stacks", 2, "is_valid",
      "Given a string of brackets, determine if the input is valid.",
      "- `0 <= len(s) <= 10^4`", "O(n)", "O(n)",
      "def is_valid(s):\n    pass\n",
      [{"args": ["()"], "expected": True},
       {"args": ["()[]{}"], "expected": True},
       {"args": ["(]"], "expected": False},
       {"args": [""], "expected": True},
       {"args": ["("], "expected": False},
       {"args": ["]"], "expected": False}]),

    P("min-stack-ops", "Minimum After Operations", "stacks", 3, "min_after_ops",
      "Process a list of ops: an integer pushes, `'C'` cancels the last, "
      "`'D'` pushes double the last, `'+'` pushes the sum of the last two. "
      "Return the final total.",
      "- `1 <= len(ops) <= 1000`", "O(n)", "O(n)",
      "def min_after_ops(ops):\n    pass\n",
      [{"args": [[5, 2, "C", "D", "+"]], "expected": 30},
       {"args": [[5, -2, 4, "C", "D", 9, "+", "+"]], "expected": 27},
       {"args": [[1]], "expected": 1},
       {"args": [[1, "C"]], "expected": 0},
       {"args": [[3, "D"]], "expected": 9}]),

    P("daily-temperatures", "Daily Temperatures", "stacks", 4, "daily_temperatures",
      "For each day, how many days until a warmer temperature? 0 if none.",
      "- `1 <= len(temps) <= 10^5`", "O(n)", "O(n)",
      "def daily_temperatures(temps):\n    pass\n",
      [{"args": [[73, 74, 75, 71, 69, 72, 76, 73]],
        "expected": [1, 1, 4, 2, 1, 1, 0, 0]},
       {"args": [[30, 40, 50, 60]], "expected": [1, 1, 1, 0]},
       {"args": [[30, 60, 90]], "expected": [1, 1, 0]},
       {"args": [[50]], "expected": [0]},
       {"args": [[50, 50, 50]], "expected": [0, 0, 0]}]),

    # --- binary search ----------------------------------------------------
    P("binary-search", "Binary Search", "binary-search", 1, "search",
      "Return the index of `target` in a sorted array, or -1.",
      "- `0 <= len(nums) <= 10^4`\n- `nums` is sorted ascending", "O(log n)", "O(1)",
      "def search(nums, target):\n    pass\n",
      [{"args": [[-1, 0, 3, 5, 9, 12], 9], "expected": 4},
       {"args": [[-1, 0, 3, 5, 9, 12], 2], "expected": -1},
       {"args": [[], 1], "expected": -1},
       {"args": [[5], 5], "expected": 0},
       {"args": [[5], 1], "expected": -1},
       {"args": [[1, 2], 2], "expected": 1}]),

    P("search-rotated", "Search in Rotated Sorted Array", "binary-search", 4,
      "search_rotated",
      "Search `target` in a rotated sorted array in O(log n). Return index or -1.",
      "- `1 <= len(nums) <= 5000`\n- All values distinct", "O(log n)", "O(1)",
      "def search_rotated(nums, target):\n    pass\n",
      [{"args": [[4, 5, 6, 7, 0, 1, 2], 0], "expected": 4},
       {"args": [[4, 5, 6, 7, 0, 1, 2], 3], "expected": -1},
       {"args": [[1], 0], "expected": -1},
       {"args": [[1], 1], "expected": 0},
       {"args": [[3, 1], 1], "expected": 1},
       {"args": [[5, 1, 3], 3], "expected": 2}]),

    P("median-two-arrays", "Median of Two Sorted Arrays", "binary-search", 5,
      "find_median",
      "Return the median of two sorted arrays in O(log(m+n)).",
      "- `0 <= m + n <= 2000`\n- Not concatenate-and-sort", "O(log(m+n))", "O(1)",
      "def find_median(a, b):\n    pass\n",
      [{"args": [[1, 3], [2]], "expected": 2.0},
       {"args": [[1, 2], [3, 4]], "expected": 2.5},
       {"args": [[], [1]], "expected": 1.0},
       {"args": [[2], []], "expected": 2.0},
       {"args": [[0, 0], [0, 0]], "expected": 0.0},
       {"args": [[1, 1, 3], [2]], "expected": 1.5}]),

    # --- graphs / trees ---------------------------------------------------
    P("max-depth", "Maximum Depth of Nested List", "graphs", 2, "max_depth",
      "Given a nested list, return its maximum nesting depth. `[]` has depth 1.",
      "- Nesting depth `<= 100`", "O(n)", "O(d)",
      "def max_depth(items):\n    pass\n",
      [{"args": [[1, 2, 3]], "expected": 1},
       {"args": [[1, [2, [3]]]], "expected": 3},
       {"args": [[]], "expected": 1},
       {"args": [[[], []]], "expected": 2},
       {"args": [[[[[1]]]]], "expected": 4}]),

    P("number-of-islands", "Number of Islands", "graphs", 4, "num_islands",
      "Count islands in a grid of `'1'` (land) and `'0'` (water). "
      "Islands connect 4-directionally.",
      "- `0 <= rows, cols <= 300`", "O(m*n)", "O(m*n)",
      "def num_islands(grid):\n    pass\n",
      [{"args": [[["1", "1", "0"], ["1", "0", "0"], ["0", "0", "1"]]], "expected": 2},
       {"args": [[["1", "1"], ["1", "1"]]], "expected": 1},
       {"args": [[]], "expected": 0},
       {"args": [[["0"]]], "expected": 0},
       {"args": [[["1"]]], "expected": 1},
       {"args": [[["1", "0", "1"], ["0", "0", "0"], ["1", "0", "1"]]], "expected": 4}]),

    P("course-schedule", "Course Schedule", "graphs", 5, "can_finish",
      "Given `n` courses and prerequisite pairs `[a, b]` (take `b` before `a`), "
      "return whether all courses can be finished.",
      "- `1 <= n <= 2000`\n- Detect cycles", "O(V+E)", "O(V+E)",
      "def can_finish(n, prerequisites):\n    pass\n",
      [{"args": [2, [[1, 0]]], "expected": True},
       {"args": [2, [[1, 0], [0, 1]]], "expected": False},
       {"args": [1, []], "expected": True},
       {"args": [3, [[1, 0], [2, 1]]], "expected": True},
       {"args": [3, [[0, 1], [1, 2], [2, 0]]], "expected": False},
       {"args": [4, [[1, 0], [2, 0], [3, 1], [3, 2]]], "expected": True}]),
]


def seed() -> None:
    db = SessionLocal()
    try:
        topic_ids: dict[str, uuid.UUID] = {}
        for slug, name in TOPICS:
            topic = db.execute(select(Topic).where(Topic.slug == slug)).scalars().first()
            if topic is None:
                topic = Topic(id=uuid.uuid4(), slug=slug, name=name)
                db.add(topic)
                db.flush()
            topic_ids[slug] = topic.id

        created = updated = 0
        for spec in PROBLEMS:
            data = dict(spec)
            topic_slug = data.pop("topic")
            existing = db.execute(
                select(Problem).where(Problem.slug == data["slug"])
            ).scalars().first()

            if existing is None:
                db.add(Problem(id=uuid.uuid4(), topic_id=topic_ids[topic_slug], **data))
                created += 1
            else:
                for key, value in data.items():
                    setattr(existing, key, value)
                existing.topic_id = topic_ids[topic_slug]
                updated += 1

        db.commit()
        tiers = sorted({p["difficulty_tier"] for p in PROBLEMS})
        print(f"seeded {len(TOPICS)} topics, {created} new / {updated} updated problems")
        print(f"tiers present: {tiers}")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
