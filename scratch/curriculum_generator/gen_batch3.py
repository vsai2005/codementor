import os
from .common import (
    CURRICULUM_MAP,
    get_difficulty,
    get_next_preview,
    make_explanation_step,
    make_checkpoint_step,
    make_practice_step,
    make_completion_step,
)
from .batch_author_engine import build_batch_ts_file

def create_day_41():
    # Sliding Window: Fixed Size
    return {
        "dayNumber": 41,
        "title": "Sliding Window: Fixed Size",
        "topicName": "Fixed Window",
        "sectionId": "arrays-and-strings",
        "estimatedMinutes": 35,
        "difficulty": "DEVELOPING",
        "prerequisites": [40],
        "concepts": ["Fixed Window Invariant", "Element Slide (In/Out)", "Rolling Aggregate", "O(N) Amortized Pass"],
        "practiceSkills": ["Fixed Window Maintenance", "Rolling Sum Optimization", "Boundary Initialization"],
        "steps": [
            make_explanation_step(
                "day41-step1", 1, "The Fixed Sliding Window Pattern", "Fixed Window Concept",
                "Maintaining State Across Constant-Size Windows in O(1) Per Step",
                "How to transition from O(N * K) brute force to linear O(N) by adding the new element and subtracting the old.",
                [
                    "When computing statistics (sum, average, max, distinct count) across all contiguous subarrays of fixed length $K$, naive evaluation computes each window from scratch in $O(K)$ time, costing $O(N \\times K)$ overall.",
                    "The **Fixed Sliding Window** observes that two consecutive windows of size $K$ share $K - 1$ common elements! Only two elements change:",
                    "1. The element entering the window at the right boundary: `+ arr[i]`",
                    "2. The element leaving the window at the left boundary: `- arr[i - k]`",
                    "Updating the window sum takes **$O(1)$ constant time** per slide, dropping the total complexity across the entire array to strictly **$O(N)$**!"
                ],
                snippets=[{
                    "title": "Fixed Window Rolling Sum",
                    "code": "def max_sum_subarray(nums, k):\n    window_sum = sum(nums[:k]) # Initialize first window of size k\n    max_sum = window_sum\n    for i in range(k, len(nums)):\n        window_sum += nums[i] - nums[i - k] # Slide: add new, remove old\n        max_sum = max(max_sum, window_sum)\n    return max_sum",
                    "language": "python",
                    "caption": "O(N) fixed sliding window sum."
                }],
                callouts=[{
                    "type": "tip",
                    "title": "Initialize First Window Explicitly",
                    "content": "Sum the first $K$ elements upfront (`sum(nums[:k])`), then start your loop from index `k` up to `len(nums)`. This keeps loop invariants clean."
                }],
                takeaway="Slide fixed windows in O(1) time by adding the incoming element and subtracting the outgoing element."
            ),
            make_explanation_step(
                "day41-step2", 2, "Rolling Frequency Tracking", "Rolling Frequency",
                "Fixed Window with Character Counts and Anagram Matching",
                "Maintain a fixed-size frequency hash map for pattern matching.",
                [
                    "Fixed sliding windows extend naturally to frequency maps (e.g. *Find All Anagrams in a String*).",
                    "Given string $S$ and pattern $P$, the window size is fixed at $K = \\text{len}(P)$.",
                    "Maintain the character counts of the current window. On each slide:",
                    "- Increment count for incoming character `window_counts[s[i]] += 1`.",
                    "- Decrement count for outgoing character `window_counts[s[i - k]] -= 1` (and delete key if count reaches 0).",
                    "- Compare window frequencies to pattern frequencies in $O(1)$ time (at most 26 alphabet characters)."
                ],
                snippets=[{
                    "title": "Sliding Frequency Window",
                    "code": "from collections import Counter\n\ndef find_anagrams(s, p):\n    k = len(p)\n    p_count = Counter(p)\n    w_count = Counter(s[:k])\n    res = []\n    if w_count == p_count:\n        res.append(0)\n    for i in range(k, len(s)):\n        w_count[s[i]] += 1\n        w_count[s[i - k]] -= 1\n        if w_count[s[i - k]] == 0:\n            del w_count[s[i - k]]\n        if w_count == p_count:\n            res.append(i - k + 1)\n    return res",
                    "language": "python",
                    "caption": "Tracking anagram windows via sliding Counter."
                }],
                callouts=[{
                    "type": "warning",
                    "title": "Delete Zero Keys",
                    "content": "In Python, `Counter({'a': 0}) != Counter({})`! When decrementing a frequency to zero, explicitly `del w_count[key]` so equality checks remain accurate."
                }],
                takeaway="Cleanly prune zero-count keys from frequency maps to maintain direct equality comparison."
            ),
            make_checkpoint_step(
                "day41-step3", 3, "Fixed Window Checkpoint", "Checkpoint",
                "Test Your Mastery of Fixed Sliding Windows",
                "Evaluate window bounds and sliding update operations.",
                [
                    {
                        "id": "chk-d41-q1",
                        "question": "What is the time complexity to find the maximum sum subarray of size K in an array of size N using a fixed sliding window?",
                        "options": [
                            {"id": "A", "label": "O(N * K)"},
                            {"id": "B", "label": "O(N)"},
                            {"id": "C", "label": "O(N log K)"},
                            {"id": "D", "label": "O(K)"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: That is the brute-force approach.",
                            "B": "Correct! Initializing the window takes O(K), and each of the remaining N - K slides takes O(1) arithmetic time. Total time: O(K + (N - K)) = O(N).",
                            "C": "Incorrect: No heap or sorting is required for basic sum.",
                            "D": "Incorrect: The algorithm must visit all N elements."
                        }
                    },
                    {
                        "id": "chk-d41-q2",
                        "question": "When sliding a window of size K forward at step index `i`, which element leaves the window?",
                        "options": [
                            {"id": "A", "label": "nums[i - 1]"},
                            {"id": "B", "label": "nums[i - k]"},
                            {"id": "C", "label": "nums[i - k - 1]"},
                            {"id": "D", "label": "nums[k]"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: nums[i - 1] is still inside the window.",
                            "B": "Correct! The window at index i covers indices from i - k + 1 to i. The element that just fell outside the window was at index i - k.",
                            "C": "Incorrect: Off-by-one.",
                            "D": "Incorrect: The leaving index changes as i advances."
                        }
                    }
                ],
                takeaway="Fixed sliding window achieves O(N) total time; the leaving element is always nums[i - k]."
            ),
            make_practice_step(
                "day41-step4", 4, "Maximum Average Subarray", "Practice",
                "Find Maximum Average Subarray of Size K",
                "Implement maximum average subarray finder using fixed sliding window.",
                "Max Average Subarray Solver",
                [
                    "Given `nums = [1, 12, -5, -6, 50, 3]` and `k = 4`.",
                    "Initialize `window_sum = sum(nums[:k])`.",
                    "Track `max_sum = window_sum`.",
                    "Slide from `i = k` to `len(nums) - 1`, updating `window_sum += nums[i] - nums[i - k]`.",
                    "Return `max_sum / k` rounded to 2 decimal places.",
                    "Print `'Max average:', max_avg`."
                ],
                """# Day 41 Practice: Max Average Subarray Solver
nums = [1, 12, -5, -6, 50, 3]
k = 4

window_sum = sum(nums[:k])
max_sum = window_sum

for i in range(k, len(nums)):
    window_sum += nums[i] - nums[i - k]
    max_sum = max(max_sum, window_sum)

max_avg = round(max_sum / k, 2)
print("Max average:", max_avg)
""",
                """nums = [1, 12, -5, -6, 50, 3]
k = 4

window_sum = sum(nums[:k])
max_sum = window_sum

for i in range(k, len(nums)):
    window_sum += nums[i] - nums[i - k]
    max_sum = max(max_sum, window_sum)

max_avg = round(max_sum / k, 2)
print("Max average:", max_avg)
""",
                ["Max average: 12.75"],
                "Optimal window is [12, -5, -6, 50] with sum 51 -> 51 / 4 = 12.75.",
                takeaway="Fixed sliding windows track running aggregates in O(1) time per step."
            ),
            make_completion_step(
                "day41-step5", 5, "Fixed Sliding Window Mastery", "Recap",
                41, "Day 41 Complete: Sliding Window: Fixed Size",
                "You have mastered fixed-size window sliding, rolling sum algebra, and frequency map maintenance.",
                [
                    {
                        "concept": "Window Recomputation",
                        "naiveIntuition": "Sum all K elements on every step",
                        "pythonReality": "Add incoming element and subtract outgoing element in O(1) time"
                    },
                    {
                        "concept": "Frequency Map Pruning",
                        "naiveIntuition": "Setting count to 0 removes the key from Counter",
                        "pythonReality": "Zero keys must be explicitly deleted via del map[key] for accurate equality comparisons"
                    }
                ],
                ["Fixed Window Invariant", "Incoming vs Outgoing Element Update", "O(N) Amortized Execution", "Rolling Frequency Counters"],
                get_next_preview(41)
            )
        ]
    }

print("Batch 3 generator module initialized.")
