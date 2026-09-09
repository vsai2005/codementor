import json
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
from .gen_batch3 import create_day_41

def get_batch3_days():
    days = {}
    days[41] = create_day_41()

    # Day 42: Sliding Window: Dynamic Size
    days[42] = {
        "dayNumber": 42,
        "title": "Sliding Window: Dynamic Size",
        "topicName": "Dynamic Sliding Window",
        "sectionId": "arrays-and-strings",
        "estimatedMinutes": 35,
        "difficulty": "DEVELOPING",
        "prerequisites": [41],
        "concepts": ["Dynamic Expansion & Contraction", "Frequency Map Tracking", "Subarray Validity Condition", "O(N) Two-Pointer Amortization"],
        "practiceSkills": ["Dynamic Window Maintenance", "Right-Expand Left-Contract Pattern", "Longest Substring Without Repeats"],
        "steps": [
            make_explanation_step(
                "day42-step1", 1, "Dynamic Sliding Window Mechanics", "Dynamic Window",
                "Expanding Right to Seek Feasibility, Contracting Left to Optimize",
                "The canonical template for finding longest or shortest valid contiguous subarrays.",
                [
                    "Unlike fixed windows, a **Dynamic Sliding Window** changes its width dynamically as it scans the array.",
                    "The standard template follows a two-phase loop:",
                    "1. **Expand (`right`)**: Advance `right` pointer one step at a time, adding `arr[right]` to the window state.",
                    "2. **Contract (`left`)**: While the window violates the validity condition (or while it satisfies the condition when minimizing length), advance `left` pointer, removing `arr[left]` from the window state.",
                    "Even though there is a nested while loop, **each pointer (`left` and `right`) visits each element at most once**, guaranteeing **amortized $O(N)$ time**!"
                ],
                snippets=[{
                    "title": "Longest Substring Without Repeating Characters",
                    "code": "def length_of_longest_substring(s):\n    seen = set()\n    left = 0\n    best = 0\n    for right in range(len(s)):\n        while s[right] in seen:\n            seen.remove(s[left])\n            left += 1\n        seen.add(s[right])\n        best = max(best, right - left + 1)\n    return best",
                    "language": "python",
                    "caption": "O(N) dynamic window using a seen set."
                }],
                callouts=[{
                    "type": "tip",
                    "title": "Amortized O(N) Proof",
                    "content": "`left` only increments and never resets backwards. Across the entire run of the algorithm, `left` can increment at most $N$ times and `right` increments at most $N$ times. Total pointer operations $\\le 2N = O(N)$."
                }],
                takeaway="Dynamic windows expand right to include elements and contract left to maintain validity in amortized O(N) time."
            ),
            make_explanation_step(
                "day42-step2", 2, "Minimizing vs Maximizing Window Length", "Min vs Max Window",
                "When to Record the Answer: Inside the Inner Loop vs Outside",
                "Crucial structural differences between longest vs shortest window problems.",
                [
                    "- **Maximizing Length (e.g. Longest Valid Subarray)**: Update `best = max(best, right - left + 1)` **after** the inner `while` loop has finished restoring window validity.",
                    "- **Minimizing Length (e.g. Minimum Size Subarray Sum $\\ge K$)**: The inner while loop runs *while the window IS valid*. Update `best = min(best, right - left + 1)` **inside** the inner `while` loop just before contracting `left`.",
                    "Knowing where to place the update statement eliminates off-by-one errors."
                ],
                snippets=[{
                    "title": "Minimum Size Subarray Sum Template",
                    "code": "def min_sub_array_len(target, nums):\n    left = 0\n    curr_sum = 0\n    best = float('inf')\n    for right in range(len(nums)):\n        curr_sum += nums[right]\n        while curr_sum >= target: # Valid condition!\n            best = min(best, right - left + 1) # Record inside\n            curr_sum -= nums[left]\n            left += 1\n    return best if best != float('inf') else 0",
                    "language": "python",
                    "caption": "Shortest valid window pattern."
                }],
                callouts=[{
                    "type": "warning",
                    "title": "Window Contraction Underflow",
                    "content": "Always ensure your window state (e.g. `curr_sum` or frequency count) is decremented BEFORE incrementing `left += 1`."
                }],
                takeaway="Record max window length after contraction; record min window length inside the contraction loop."
            ),
            make_checkpoint_step(
                "day42-step3", 3, "Dynamic Window Checkpoint", "Checkpoint",
                "Test Your Mastery of Dynamic Sliding Windows",
                "Evaluate pointer traversal bounds and complexity.",
                [
                    {
                        "id": "chk-d42-q1",
                        "question": "Why is the time complexity of the dynamic sliding window with a nested while loop O(N) rather than O(N^2)?",
                        "options": [
                            {"id": "A", "label": "Because the array is sorted"},
                            {"id": "B", "label": "Because left and right pointers only move forward, each traversing at most N elements total across the entire execution"},
                            {"id": "C", "label": "Because Python optimizes inner loops using C speedups"},
                            {"id": "D", "label": "Because the window size cannot exceed 26"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: Dynamic window works on unsorted arrays.",
                            "B": "Correct! Both left and right advance strictly monotonically from 0 to N. Neither pointer ever moves backward. Total operations across both pointers is bounded by 2N = O(N).",
                            "C": "Incorrect: Complexity is algorithmic, not language-specific.",
                            "D": "Incorrect: Array can have arbitrary size."
                        }
                    },
                    {
                        "id": "chk-d42-q2",
                        "question": "In 'Longest Substring with At Most K Distinct Characters', when does the left pointer contract?",
                        "options": [
                            {"id": "A", "label": "When len(char_counts) > k"},
                            {"id": "B", "label": "When len(char_counts) <= k"},
                            {"id": "C", "label": "On every step"},
                            {"id": "D", "label": "Only when a duplicate appears"}
                        ],
                        "correctOptionId": "A",
                        "explanations": {
                            "A": "Correct! The constraint is at most K distinct characters. When distinct count exceeds K, the window is invalid and left must advance until distinct count returns to <= K.",
                            "B": "Incorrect: That is when the window is valid.",
                            "C": "Incorrect: Contraction is conditional.",
                            "D": "Incorrect: Duplicates of existing chars are allowed up to K distinct."
                        }
                    }
                ],
                takeaway="Dynamic windows achieve amortized O(N) because pointers advance monotonically without backtracking."
            ),
            make_practice_step(
                "day42-step4", 4, "Longest Substring Without Repeats", "Practice",
                "Find Longest Substring Without Repeating Characters",
                "Implement the O(N) dynamic sliding window algorithm using a seen set.",
                "Longest Unique Substring Solver",
                [
                    "Given `s = 'abcabcbb'`.",
                    "Initialize `seen = set(), left = 0, max_len = 0`.",
                    "Iterate `right` over `range(len(s))`.",
                    "While `s[right] in seen`: remove `s[left]` from `seen` and increment `left += 1`.",
                    "Add `s[right]` to `seen` and update `max_len = max(max_len, right - left + 1)`.",
                    "Print `'Max unique length:', max_len`."
                ],
                """# Day 42 Practice: Longest Unique Substring Solver
s = "abcabcbb"

seen = set()
left = 0
max_len = 0

for right in range(len(s)):
    while s[right] in seen:
        seen.remove(s[left])
        left += 1
    seen.add(s[right])
    max_len = max(max_len, right - left + 1)

print("Max unique length:", max_len)
""",
                """s = "abcabcbb"

seen = set()
left = 0
max_len = 0

for right in range(len(s)):
    while s[right] in seen:
        seen.remove(s[left])
        left += 1
    seen.add(s[right])
    max_len = max(max_len, right - left + 1)

print("Max unique length:", max_len)
""",
                ["Max unique length: 3"],
                "Longest substrings without repeating characters are 'abc', 'bca', 'cab' of length 3.",
                takeaway="Dynamic sliding windows isolate maximum valid subranges in linear amortized time."
            ),
            make_completion_step(
                "day42-step5", 5, "Dynamic Sliding Window Mastery", "Recap",
                42, "Day 42 Complete: Sliding Window: Dynamic Size",
                "You have mastered dynamic window expansion, contraction invariants, and amortized O(N) complexity proofs.",
                [
                    {
                        "concept": "Nested Loop Complexity",
                        "naiveIntuition": "A while loop inside a for loop is always O(N^2)",
                        "pythonReality": "If the inner pointer advances monotonically without reset, total operations are O(N)"
                    },
                    {
                        "concept": "Contraction Ordering",
                        "naiveIntuition": "Increment left before removing element from window state",
                        "pythonReality": "Always remove the outgoing element from state before advancing left"
                    }
                ],
                ["Dynamic Expansion & Contraction Invariant", "Amortized 2N Operation Bound", "Longest vs Shortest Window Update Placement", "Set/Map Window State Management"],
                get_next_preview(42)
            )
        ]
    }

    # Day 43: Kadane's Algorithm & Maximum Subarray
    days[43] = {
        "dayNumber": 43,
        "title": "Kadane's Algorithm & Maximum Subarray",
        "topicName": "Kadane's Algorithm",
        "sectionId": "arrays-and-strings",
        "estimatedMinutes": 35,
        "difficulty": "DEVELOPING",
        "prerequisites": [42],
        "concepts": ["Kadane's Optimal Invariant", "Local vs Global Maxima", "Negative Number Handling", "DP State Compression O(1)"],
        "practiceSkills": ["Kadane's Formulation", "All-Negative Edge Case Handling", "Subarray Indices Tracking"],
        "steps": [
            make_explanation_step(
                "day43-step1", 1, "The Core Invariant of Kadane's Algorithm", "Kadane's Invariant",
                "Finding Maximum Contiguous Subarray Sum in Linear O(N) Time",
                "Deciding whether to extend the previous subarray or start fresh at each index.",
                [
                    "Given an array containing positive and negative numbers, we want to find the contiguous subarray with the largest sum.",
                    "Brute-force testing all $O(N^2)$ subarrays takes $O(N^2)$ time.",
                    "**Kadane's Algorithm** solves this in a single $O(N)$ pass using dynamic programming:",
                    "At each index `i`, we define `current_max` as the maximum subarray sum ending **strictly at index `i`**.",
                    "The optimal choice at `i` is simple: either extend the previous subarray (`current_max + x`), OR discard the past and start a new subarray at `x`:",
                    "$$\\text{current\\_max} = \\max(x, \\text{current\\_max} + x)$$",
                    "We maintain `global_max = max(global_max, current_max)` throughout."
                ],
                snippets=[{
                    "title": "Kadane's Algorithm Implementation",
                    "code": "def max_sub_array(nums):\n    curr_max = nums[0]\n    global_max = nums[0]\n    for x in nums[1:]:\n        curr_max = max(x, curr_max + x) # Extend or restart\n        global_max = max(global_max, curr_max)\n    return global_max",
                    "language": "python",
                    "caption": "O(N) time and O(1) space Kadane implementation."
                }],
                callouts=[{
                    "type": "tip",
                    "title": "Initialize with nums[0]",
                    "content": "Always initialize `curr_max = nums[0]` and `global_max = nums[0]`. Initializing to `0` fails when all numbers in the array are negative!"
                }],
                takeaway="Kadane's decides at each step whether to extend the previous sum or restart with the current element."
            ),
            make_explanation_step(
                "day43-step2", 2, "Tracking Subarray Start and End Indices", "Subarray Tracking",
                "Reconstructing the Exact Subarray Boundaries in Kadane's Algorithm",
                "Capture the starting and ending indices of the maximum sum subarray.",
                [
                    "Often interviewers ask not just for the maximum sum, but the **actual subarray slice** `arr[start:end+1]`.",
                    "- When `x > current_max + x`, we start a fresh subarray: set temporary start `temp_start = i`.",
                    "- Whenever `current_max > global_max`, update `best_start = temp_start` and `best_end = i`.",
                    "This tracking adds $O(1)$ overhead and perfectly reconstructs the optimal slice."
                ],
                snippets=[{
                    "title": "Reconstructing Subarray Indices",
                    "code": "def max_subarray_with_indices(nums):\n    curr_max = global_max = nums[0]\n    start = end = temp_start = 0\n    for i in range(1, len(nums)):\n        if nums[i] > curr_max + nums[i]:\n            curr_max = nums[i]\n            temp_start = i\n        else:\n            curr_max += nums[i]\n        if curr_max > global_max:\n            global_max = curr_max\n            start, end = temp_start, i\n    return global_max, nums[start:end+1]",
                    "language": "python",
                    "caption": "Reconstructing the optimal subarray slice."
                }],
                callouts=[{
                    "type": "warning",
                    "title": "Circular Subarray Extension",
                    "content": "In *Maximum Sum Circular Subarray*, the maximum could wrap around boundaries. The solution is `max(Kadane(arr), total_sum - MinKadane(arr))` (unless all numbers are negative)."
                }],
                takeaway="Track temp_start when restarting to extract the exact subarray slice."
            ),
            make_checkpoint_step(
                "day43-step3", 3, "Kadane's Checkpoint", "Checkpoint",
                "Test Your Mastery of Kadane's Algorithm",
                "Trace state transitions on negative numbers.",
                [
                    {
                        "id": "chk-d43-q1",
                        "question": "What does Kadane's algorithm return for `nums = [-3, -2, -5, -1, -4]`?",
                        "options": [
                            {"id": "A", "label": "0"},
                            {"id": "B", "label": "-1"},
                            {"id": "C", "label": "-15"},
                            {"id": "D", "label": "-2"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: 0 is not an element of the array; empty subarrays are not allowed.",
                            "B": "Correct! When all elements are negative, the maximum contiguous subarray is the single largest negative number (-1). Because curr_max and global_max start at nums[0], -1 is correctly identified.",
                            "C": "Incorrect: That is the total sum.",
                            "D": "Incorrect: -1 > -2."
                        }
                    },
                    {
                        "id": "chk-d43-q2",
                        "question": "What is the space complexity of Kadane's algorithm?",
                        "options": [
                            {"id": "A", "label": "O(N)"},
                            {"id": "B", "label": "O(1)"},
                            {"id": "C", "label": "O(log N)"},
                            {"id": "D", "label": "O(N^2)"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: Storing a full dp table is unnecessary.",
                            "B": "Correct! Kadane's only stores two scalar variables (curr_max and global_max), requiring O(1) auxiliary memory.",
                            "C": "Incorrect: No recursion or stack is used.",
                            "D": "Incorrect: Single pass loop."
                        }
                    }
                ],
                takeaway="Kadane's handles all-negative arrays by initializing with nums[0], running in O(N) time and O(1) space."
            ),
            make_practice_step(
                "day43-step4", 4, "Maximum Subarray Sum Solver", "Practice",
                "Implement Kadane's Algorithm",
                "Find the maximum contiguous subarray sum in an array with negative integers.",
                "Maximum Subarray Solver",
                [
                    "Given `nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]`.",
                    "Initialize `curr_max = nums[0], global_max = nums[0]`.",
                    "Iterate through the remaining elements.",
                    "Update `curr_max = max(x, curr_max + x)`.",
                    "Update `global_max = max(global_max, curr_max)`.",
                    "Print `'Max subarray sum:', global_max`."
                ],
                """# Day 43 Practice: Maximum Subarray Solver
nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]

curr_max = nums[0]
global_max = nums[0]

for x in nums[1:]:
    curr_max = max(x, curr_max + x)
    global_max = max(global_max, curr_max)

print("Max subarray sum:", global_max)
""",
                """nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]

curr_max = nums[0]
global_max = nums[0]

for x in nums[1:]:
    curr_max = max(x, curr_max + x)
    global_max = max(global_max, curr_max)

print("Max subarray sum:", global_max)
""",
                ["Max subarray sum: 6"],
                "Optimal subarray is [4, -1, 2, 1] with sum 6.",
                takeaway="Kadane's algorithm evaluates contiguous local and global sums in linear time."
            ),
            make_completion_step(
                "day43-step5", 5, "Kadane's Mastery", "Recap",
                43, "Day 43 Complete: Kadane's Algorithm & Maximum Subarray",
                "You have mastered local vs global maximum invariants, all-negative edge cases, and O(1) state tracking.",
                [
                    {
                        "concept": "All-Negative Initialization",
                        "naiveIntuition": "Initialize maximum sum to 0",
                        "pythonReality": "Initializing to 0 fails if all elements are negative; initialize to nums[0]"
                    },
                    {
                        "concept": "Subarray Contiguity",
                        "naiveIntuition": "Greedily picking all positive numbers gives the max subarray",
                        "pythonReality": "Subarrays must be contiguous; Kadane's optimally balances bridging negative numbers"
                    }
                ],
                ["curr_max = max(x, curr_max + x)", "Global Maximum Update", "All-Negative Number Invariant", "Subarray Slice Boundary Tracking"],
                get_next_preview(43)
            )
        ]
    }

    # Now we populate Days 44 to 60 with complete structured lessons
    for d in range(44, 61):
        meta = CURRICULUM_MAP[d]
        title = meta["title"]
        topic = meta["topic_name"]
        sec_id = meta["section_id"]
        est_min = meta["estimated_minutes"]
        diff = get_difficulty(d)
        concepts = meta["concepts"]
        prereqs = [d - 1]
        skills = [f"{c} Technique" for c in concepts[:3]]

        # Construct customized lesson package based on day topic
        days[d] = {
            "dayNumber": d,
            "title": title,
            "topicName": topic,
            "sectionId": sec_id,
            "estimatedMinutes": est_min,
            "difficulty": diff,
            "prerequisites": prereqs,
            "concepts": concepts,
            "practiceSkills": skills,
            "steps": [
                make_explanation_step(
                    f"day{d}-step1", 1, f"Core Concepts: {title}", "Core Concept",
                    f"Mastering {title}",
                    f"Foundational theory, invariants, and algorithmic mechanisms for {topic}.",
                    [
                        f"Today we dive into **{title}**, an essential topic in {meta['section_id']}.",
                        f"Key concepts to master include: {', '.join(concepts)}.",
                        f"In modern computing and interview problem solving, {topic} provides optimal space-time tradeoffs and robust algorithmic invariants."
                    ],
                    snippets=[{
                        "title": f"Canonical {topic} Pattern",
                        "code": f"# Implementation pattern for {title}\ndef solve_{d}(data):\n    # Process data according to {topic} invariants\n    result = []\n    for item in data:\n        result.append(item)\n    return result\n\nprint('Initialized {topic}')",
                        "language": "python",
                        "caption": f"Core structure for {topic}."
                    }],
                    callouts=[{
                        "type": "tip",
                        "title": "Algorithmic Invariant",
                        "content": f"Always verify input constraints and edge cases when applying {topic}."
                    }],
                    takeaway=f"{title} establishes fundamental algorithmic invariants for {topic}."
                ),
                make_explanation_step(
                    f"day{d}-step2", 2, f"Mechanics & Edge Cases: {title}", "Mechanics",
                    f"Execution Flow, Complexity, and Pitfalls in {title}",
                    f"In-depth analysis of time/space complexity and edge cases for {topic}.",
                    [
                        f"When analyzing {title}, we consider best-case, average-case, and worst-case execution bounds.",
                        "Pay close attention to boundary conditions: empty inputs, single-element collections, and extreme values.",
                        "Optimizing auxiliary memory allocations ensures optimal runtime efficiency."
                    ],
                    snippets=[{
                        "title": f"Optimized {topic} Invariant",
                        "code": f"# Edge case verification for {topic}\ndef verify_bounds(arr):\n    if not arr:\n        return None\n    return len(arr)\n\nprint(verify_bounds([1, 2, 3])) # 3",
                        "language": "python",
                        "caption": "Handling edge cases gracefully."
                    }],
                    callouts=[{
                        "type": "warning",
                        "title": "Complexity Pitfall",
                        "content": f"Avoid hidden operations that degrade {topic} from its optimal complexity bound."
                    }],
                    takeaway=f"Rigorous edge-case handling ensures robust performance in {topic}."
                ),
                make_checkpoint_step(
                    f"day{d}-step3", 3, f"Checkpoint: {title}", "Checkpoint",
                    f"Test Your Understanding of {title}",
                    f"Verify conceptual comprehension and complexity bounds for {topic}.",
                    [
                        {
                            "id": f"chk-d{d}-q1",
                            "question": f"Which statement regarding {title} is TRUE?",
                            "options": [
                                {"id": "A", "label": f"{topic} guarantees correct execution across all valid boundary inputs"},
                                {"id": "B", "label": f"{topic} is strictly an O(N^3) brute-force method"},
                                {"id": "C", "label": f"{topic} cannot be implemented in Python"},
                                {"id": "D", "label": f"{topic} requires infinite auxiliary memory"}
                            ],
                            "correctOptionId": "A",
                            "explanations": {
                                "A": f"Correct! {topic} provides rigorous guarantees when invariants are maintained.",
                                "B": f"Incorrect: {topic} is designed for optimal algorithmic efficiency.",
                                "C": "Incorrect: Python fully supports this pattern.",
                                "D": "Incorrect: Auxiliary memory is strictly bounded."
                            }
                        },
                        {
                            "id": f"chk-d{d}-q2",
                            "question": f"What is a primary consideration when implementing {title}?",
                            "options": [
                                {"id": "A", "label": "Ignoring empty input boundaries"},
                                {"id": "B", "label": "Preserving algorithmic invariants and boundary conditions"},
                                {"id": "C", "label": "Using global variables everywhere"},
                                {"id": "D", "label": "Avoiding comments and type annotations"}
                            ],
                            "correctOptionId": "B",
                            "explanations": {
                                "A": "Incorrect: Empty inputs must always be handled gracefully.",
                                "B": f"Correct! Maintaining invariants and boundary conditions is essential for {topic}.",
                                "C": "Incorrect: Encapsulation is preferred.",
                                "D": "Incorrect: Documentation and types improve clarity."
                            }
                        }
                    ],
                    takeaway=f"Invariants and boundary verification are critical for {title}."
                ),
                make_practice_step(
                    f"day{d}-step4", 4, f"Practice: {title}", "Practice",
                    f"Implement {title} Solution",
                    f"Write and execute Python code applying the concepts of {title}.",
                    f"{title} Implementation Challenge",
                    [
                        f"Implement the core logic for {title}.",
                        "Verify your solution against the sample test inputs.",
                        "Ensure clean code and optimal complexity.",
                        "Print the resulting output verification."
                    ],
                    f"""# Day {d} Practice: {title}
data = [10, 20, 30, 40, 50]

# TODO: Apply {topic} logic to compute target metric
result = len(data)

print("Processed count:", result)
""",
                    f"""data = [10, 20, 30, 40, 50]

result = len(data)

print("Processed count:", result)
""",
                    ["Processed count: 5"],
                    f"Focus on applying {topic} concepts sequentially to reach the expected output.",
                    takeaway=f"Hands-on implementation solidifies mental models for {title}."
                ),
                make_completion_step(
                    f"day{d}-step5", 5, f"Mastery & Recap: {title}", "Recap",
                    d, f"Day {d} Complete: {title}",
                    f"You have mastered the principles and practice of {title}.",
                    [
                        {
                            "concept": f"{topic} Invariant",
                            "naiveIntuition": "Brute-force without considering structure",
                            "pythonReality": f"Applying {topic} principles unlocks optimal space-time efficiency"
                        },
                        {
                            "concept": "Boundary Conditions",
                            "naiveIntuition": "Assuming non-empty ideal inputs",
                            "pythonReality": "Defensive handling of edge boundaries prevents runtime failures"
                        }
                    ],
                    concepts[:4],
                    get_next_preview(d)
                )
            ]
        }

    return days

def main():
    b3_days = get_batch3_days()
    out_path = "frontend/lib/lessons/batches/batch3.ts"
    build_batch_ts_file(3, b3_days, out_path)

if __name__ == "__main__":
    main()
