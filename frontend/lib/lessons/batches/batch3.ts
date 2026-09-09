import { DailyLessonPackage } from "../types";

export const BATCH_3_LESSONS: Record<number, DailyLessonPackage> = {
  41: {
  "dayNumber": 41,
  "title": "Sliding Window: Fixed Size",
  "topicName": "Fixed Window",
  "sectionId": "arrays-and-strings",
  "estimatedMinutes": 35,
  "difficulty": "DEVELOPING",
  "prerequisites": [
    37,
    40
  ],
  "concepts": [
    "Rolling Window State",
    "O(1) Element Slide Transition"
  ],
  "practiceSkills": [
    "Fixed Window Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Maintain rolling window state across fixed length k by adding incoming and subtracting outgoing elements",
    "Compute maximum subarray sums and rolling averages in O(N) time"
  ],
  "practiceArchetype": "problem",
  "flowTier": "tier2"
,
  "steps": [
    {
        "id": "day41-step1",
        "stepNumber": 1,
        "title": "Sliding Window: Fixed Size: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Fixed Window",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Fixed Window.",
        "markdownContent": [
            "Fixed Sliding Windows maintain state across a constant span K in O(1) time per slide by adding the right incoming element and subtracting the left outgoing element.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Fixed Window**, remember the central principle: Slide fixed windows in O(1) time per step by adjusting the rolling aggregate by the difference between incoming and outgoing elements."
        ],
        "snippets": [
            {
                "title": "Fixed Window Implementation Template",
                "code": "# Fixed window rolling sum of size k\ndef max_sub_k(arr, k):\n    w = sum(arr[:k])\n    ans = w\n    for i in range(k, len(arr)):\n        w += arr[i] - arr[i - k]\n        ans = max(ans, w)\n    return ans",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Slide fixed windows in O(1) time per step by adjusting the rolling aggregate by the difference between incoming and outgoing elements."
    },
    {
        "id": "day41-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Fixed Window",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Initialize window sum over nums[:K]. For index i from K to N-1, window_sum += nums[i] - nums[i - K]. Max sum updates at each step in strict O(1) time.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Slide fixed windows in O(1) time per step by adjusting the rolling aggregate by the difference between incoming and outgoing elements.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Fixed Window Core Invariant",
                "content": "Slide fixed windows in O(1) time per step by adjusting the rolling aggregate by the difference between incoming and outgoing elements."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Slide fixed windows in O(1) time per step by adjusting the rolling aggregate by the difference between incoming and outgoing elements."
    },
    {
        "id": "day41-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Fixed Window",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d41-q1",
                "question": "Why is the fixed sliding window approach O(N) rather than O(N * K)?",
                "options": [
                    {
                        "id": "A",
                        "label": "Each step reuses K - 1 elements from the previous window and performs only two arithmetic operations"
                    },
                    {
                        "id": "B",
                        "label": "Python's sum() function caches previous results automatically"
                    },
                    {
                        "id": "C",
                        "label": "Because the window size K is always treated as a mathematical constant 1"
                    },
                    {
                        "id": "D",
                        "label": "It sorts the array in O(N) time first"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Two consecutive windows overlap across K - 1 elements. Adding arr[i] and subtracting arr[i - k] updates the state in O(1) time.",
                    "B": "Incorrect: sum() recomputes elements from scratch every call.",
                    "C": "Incorrect: K can be arbitrarily large up to N.",
                    "D": "Incorrect: Sorting changes contiguous ordering and destroys subarrays."
                }
            },
            {
                "id": "chk-d41-q2",
                "question": "What is the optimal way to initialize a fixed sliding window algorithm?",
                "options": [
                    {
                        "id": "A",
                        "label": "Compute the initial sum of the first K elements upfront before starting the loop at index K"
                    },
                    {
                        "id": "B",
                        "label": "Start the loop at index 0 and use an 'if i >= k' check on every iteration"
                    },
                    {
                        "id": "C",
                        "label": "Initialize window sum to float('-inf')"
                    },
                    {
                        "id": "D",
                        "label": "Pad the array with K zeroes at the beginning"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Precomputing sum(nums[:k]) cleanly establishes the loop invariant before sliding from index K to N.",
                    "B": "Incorrect: Branching on every iteration adds branch predictor overhead.",
                    "C": "Incorrect: Window sum must match actual element values.",
                    "D": "Incorrect: Padding alters array indexing and allocations."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day41-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Fixed Window",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Find the maximum average subarray of fixed size k.",
        "subheading": "Implement and verify Fixed Window in the interactive workspace.",
        "task": {
            "title": "Find the maximum average subarray of fixed size k.",
            "instructions": [
                "Find the maximum average subarray of fixed size k.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "def find_max_average(nums: list[int], k: int) -> float:\n    # TODO 1: Initialize window_sum with the sum of the first k elements\n    window_sum = 0\n    max_sum = 0\n    \n    # TODO 2: Slide window from index k to len(nums) and update max_sum\n    \n    return max_sum / k\n\nnums = [1, 12, -5, -6, 50, 3]\nk = 4\nprint('Max average:', find_max_average(nums, k))\n",
            "solutionCode": "def find_max_average(nums: list[int], k: int) -> float:\n    window_sum = sum(nums[:k])\n    max_sum = window_sum\n    for i in range(k, len(nums)):\n        window_sum += nums[i] - nums[i - k]\n        if window_sum > max_sum:\n            max_sum = window_sum\n    return max_sum / k\n\nnums = [1, 12, -5, -6, 50, 3]\nk = 4\nprint('Max average:', find_max_average(nums, k))\n",
            "expectedOutputPatterns": [
                "Max average: 12.75"
            ],
            "hint": "window_sum = sum(nums[:k]), max_sum = window_sum, loop for i in range(k, len(nums)) updating window_sum += nums[i] - nums[i - k]."
        },
        "keyTakeaway": "Successfully implemented and verified Fixed Window!"
    },
    {
        "id": "day41-step5",
        "stepNumber": 5,
        "title": "Day 41 Complete: Sliding Window: Fixed Size",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 41,
        "heading": "Mastery Achieved: Sliding Window: Fixed Size",
        "subheading": "You have solidified key mental models and techniques for Fixed Window.",
        "recapRows": [
            {
                "concept": "Overlapping Windows",
                "naiveIntuition": "Recalculate each window sum from scratch in O(K)",
                "pythonReality": "Adjusting running sum by incoming minus outgoing is strictly O(1)"
            },
            {
                "concept": "Division Timing",
                "naiveIntuition": "Divide by K on every iteration",
                "pythonReality": "Track maximum sum and perform a single division by K at the very end"
            }
        ],
        "solidifiedConcepts": [
            "Rolling Window State",
            "O(1) Element Slide Transition"
        ],
        "nextDayPreview": {
            "dayNumber": 42,
            "title": "Sliding Window: Dynamic Size",
            "description": "Master dynamic sliding windows that expand and contract based on validity predicates, solving substring problems."
        }
    }
]
},
  42: {
  "dayNumber": 42,
  "title": "Sliding Window: Dynamic Size",
  "topicName": "Dynamic Window",
  "sectionId": "arrays-and-strings",
  "estimatedMinutes": 40,
  "difficulty": "DEVELOPING",
  "prerequisites": [
    41
  ],
  "concepts": [
    "Expand-Right & Contract-Left",
    "Monotonic Condition Predicates"
  ],
  "practiceSkills": [
    "Dynamic Window Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Expand right pointers to find valid subsegments and contract left pointers to restore invariants",
    "Solve the Longest Substring Without Repeating Characters in O(N) time"
  ],
  "practiceArchetype": "problem",
  "flowTier": "tier2"
,
  "steps": [
    {
        "id": "day42-step1",
        "stepNumber": 1,
        "title": "Sliding Window: Dynamic Size: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Dynamic Window",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Dynamic Window.",
        "markdownContent": [
            "Dynamic Sliding Windows expand the right pointer to acquire elements and contract the left pointer when validity invariants are violated, processing strings/arrays in O(N) time.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Dynamic Window**, remember the central principle: Dynamic windows maintain monotonicity: both left and right pointers only move forward, guaranteeing O(N) total steps."
        ],
        "snippets": [
            {
                "title": "Dynamic Window Implementation Template",
                "code": "# Longest Substring Without Repeating Characters\ndef length_of_longest_substring(s):\n    seen = {}\n    L = 0\n    best = 0\n    for R, ch in enumerate(s):\n        if ch in seen and seen[ch] >= L:\n            L = seen[ch] + 1\n        seen[ch] = R\n        best = max(best, R - L + 1)\n    return best",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Dynamic windows maintain monotonicity: both left and right pointers only move forward, guaranteeing O(N) total steps."
    },
    {
        "id": "day42-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Dynamic Window",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "In Longest Substring Without Repeating Characters: right pointer inserts s[R] into a character-index map. If s[R] was seen at index >= L, jump left pointer to seen[s[R]] + 1.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Dynamic windows maintain monotonicity: both left and right pointers only move forward, guaranteeing O(N) total steps.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Dynamic Window Core Invariant",
                "content": "Dynamic windows maintain monotonicity: both left and right pointers only move forward, guaranteeing O(N) total steps."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Dynamic windows maintain monotonicity: both left and right pointers only move forward, guaranteeing O(N) total steps."
    },
    {
        "id": "day42-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Dynamic Window",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d42-q1",
                "question": "Why does Longest Substring Without Repeating Characters run in O(N) time even with an inner pointer shift?",
                "options": [
                    {
                        "id": "A",
                        "label": "Both left and right pointers only advance forward; each character is visited at most twice"
                    },
                    {
                        "id": "B",
                        "label": "The hash table lookup takes O(N) time"
                    },
                    {
                        "id": "C",
                        "label": "The string length is bounded by the 26-letter alphabet"
                    },
                    {
                        "id": "D",
                        "label": "Python optimizes while loops on strings into single-cycle operations"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Right pointer moves 0 to N-1; Left pointer moves monotonically forward. The total pointer movements are bounded by 2N = O(N).",
                    "B": "Incorrect: Hash map lookup is O(1) average time.",
                    "C": "Incorrect: Input strings can contain arbitrary Unicode characters and lengths.",
                    "D": "Incorrect: No such compiler optimization exists."
                }
            },
            {
                "id": "chk-d42-q2",
                "question": "Why must we verify `seen[ch] >= L` before jumping the left pointer to `seen[ch] + 1`?",
                "options": [
                    {
                        "id": "A",
                        "label": "To ignore occurrences of ch that appeared before the current window boundary L"
                    },
                    {
                        "id": "B",
                        "label": "To ensure seen[ch] does not throw a KeyError"
                    },
                    {
                        "id": "C",
                        "label": "Because left pointer cannot exceed the array length"
                    },
                    {
                        "id": "D",
                        "label": "To avoid negative indices"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! If a character was seen at index 2, but our window has already moved to L = 5, the duplicate is outside our active window and must not pull L backward!",
                    "B": "Incorrect: KeyError is avoided by checking 'ch in seen'.",
                    "C": "Incorrect: L is bounded by R.",
                    "D": "Incorrect: Indices are non-negative."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day42-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Dynamic Window",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Find the length of the longest substring without repeating characters.",
        "subheading": "Implement and verify Dynamic Window in the interactive workspace.",
        "task": {
            "title": "Find the length of the longest substring without repeating characters.",
            "instructions": [
                "Find the length of the longest substring without repeating characters.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "def length_of_longest_substring(s: str) -> int:\n    last_seen = {}\n    left = 0\n    max_len = 0\n    # TODO: Traverse with right pointer, update left on duplicates within window, and update max_len\n    \n    return max_len\n\ns = 'abcabcbb'\nprint('Longest unique substring length:', length_of_longest_substring(s))\n",
            "solutionCode": "def length_of_longest_substring(s: str) -> int:\n    last_seen = {}\n    left = 0\n    max_len = 0\n    for right, ch in enumerate(s):\n        if ch in last_seen and last_seen[ch] >= left:\n            left = last_seen[ch] + 1\n        last_seen[ch] = right\n        current_len = right - left + 1\n        if current_len > max_len:\n            max_len = current_len\n    return max_len\n\ns = 'abcabcbb'\nprint('Longest unique substring length:', length_of_longest_substring(s))\n",
            "expectedOutputPatterns": [
                "Longest unique substring length: 3"
            ],
            "hint": "Check `if ch in last_seen and last_seen[ch] >= left: left = last_seen[ch] + 1`, update `last_seen[ch] = right`, and record `max(max_len, right - left + 1)`."
        },
        "keyTakeaway": "Successfully implemented and verified Dynamic Window!"
    },
    {
        "id": "day42-step5",
        "stepNumber": 5,
        "title": "Day 42 Complete: Sliding Window: Dynamic Size",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 42,
        "heading": "Mastery Achieved: Sliding Window: Dynamic Size",
        "subheading": "You have solidified key mental models and techniques for Dynamic Window.",
        "recapRows": [
            {
                "concept": "Pointer Monotonicity",
                "naiveIntuition": "Restarting the window requires scanning backward",
                "pythonReality": "Left pointer jumps directly past the previous duplicate using stored indices, never moving backward"
            },
            {
                "concept": "Window Length",
                "naiveIntuition": "Length is right - left",
                "pythonReality": "0-indexed inclusive window length is right - left + 1"
            }
        ],
        "solidifiedConcepts": [
            "Expand-Right & Contract-Left",
            "Monotonic Condition Predicates"
        ],
        "nextDayPreview": {
            "dayNumber": 43,
            "title": "Kadane's Algorithm & Maximum Subarray",
            "description": "Implement Kadane's algorithm to find maximum contiguous subarray sums in O(N) time and O(1) space, with boundary tracking."
        }
    }
]
},
  43: {
  "dayNumber": 43,
  "title": "Kadane's Algorithm & Maximum Subarray",
  "topicName": "Subarray Optimization",
  "sectionId": "arrays-and-strings",
  "estimatedMinutes": 35,
  "difficulty": "DEVELOPING",
  "prerequisites": [
    37
  ],
  "concepts": [
    "Kadane's Local vs Global Maxima",
    "Subarray Reset Condition"
  ],
  "practiceSkills": [
    "Subarray Optimization Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Formulate the local choice invariant: extend existing subarray or start fresh from current element",
    "Implement Kadane's algorithm tracking maximum sum and subarray boundary indices in O(N) time and O(1) space"
  ],
  "practiceArchetype": "algorithm",
  "flowTier": "tier2"
,
  "steps": [
    {
        "id": "day43-step1",
        "stepNumber": 1,
        "title": "Kadane's Algorithm & Maximum Subarray: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Subarray Optimization",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Subarray Optimization.",
        "markdownContent": [
            "Kadane's Algorithm finds the maximum contiguous subarray sum in O(N) time and O(1) space by deciding at each element whether to extend the existing subarray or start fresh.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Subarray Optimization**, remember the central principle: Kadane's algorithm evaluates local choices (extend vs restart) to achieve global maximum subarray sums in a single linear pass."
        ],
        "snippets": [
            {
                "title": "Subarray Optimization Implementation Template",
                "code": "# Kadane's Algorithm\ndef max_sub_array(nums):\n    curr = nums[0]\n    best = nums[0]\n    for x in nums[1:]:\n        curr = max(x, curr + x)\n        best = max(best, curr)\n    return best",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Kadane's algorithm evaluates local choices (extend vs restart) to achieve global maximum subarray sums in a single linear pass."
    },
    {
        "id": "day43-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Subarray Optimization",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Let curr_sum = max(x, curr_sum + x). If curr_sum drops below x (or below 0), starting fresh from x is mathematically superior to carrying a negative accumulator.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Kadane's algorithm evaluates local choices (extend vs restart) to achieve global maximum subarray sums in a single linear pass.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Subarray Optimization Core Invariant",
                "content": "Kadane's algorithm evaluates local choices (extend vs restart) to achieve global maximum subarray sums in a single linear pass."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Kadane's algorithm evaluates local choices (extend vs restart) to achieve global maximum subarray sums in a single linear pass."
    },
    {
        "id": "day43-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Subarray Optimization",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d43-q1",
                "question": "Under what condition does Kadane's algorithm restart the current subarray sum?",
                "options": [
                    {
                        "id": "A",
                        "label": "When the incoming element x is greater than curr_sum + x (i.e. curr_sum < 0)"
                    },
                    {
                        "id": "B",
                        "label": "When the incoming element is equal to zero"
                    },
                    {
                        "id": "C",
                        "label": "Whenever a negative number is encountered"
                    },
                    {
                        "id": "D",
                        "label": "Only when the array has all negative elements"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! If curr_sum is negative, adding it to x produces a value smaller than x itself. It is always better to discard the negative prefix and start fresh at x.",
                    "B": "Incorrect: Zero does not decrease the sum.",
                    "C": "Incorrect: Negative numbers are accepted if the overall accumulator remains positive.",
                    "D": "Incorrect: Restart decisions happen dynamically whenever prefixes become negative deficits."
                }
            },
            {
                "id": "chk-d43-q2",
                "question": "Why should best_sum be initialized to nums[0] rather than 0?",
                "options": [
                    {
                        "id": "A",
                        "label": "To handle arrays where all numbers are negative, ensuring the least negative number is returned"
                    },
                    {
                        "id": "B",
                        "label": "Because Python does not allow initializing variables to 0"
                    },
                    {
                        "id": "C",
                        "label": "To avoid a DivisionByZero error"
                    },
                    {
                        "id": "D",
                        "label": "Because nums[0] is always the maximum element"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! If nums = [-5, -2, -8], initializing to 0 would incorrectly return 0 (an empty subarray). Initializing to nums[0] correctly returns -2.",
                    "B": "Incorrect: Zero is a valid integer in Python.",
                    "C": "Incorrect: No division occurs in Kadane's algorithm.",
                    "D": "Incorrect: nums[0] can be any value."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day43-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Subarray Optimization",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Implement Kadane's algorithm tracking maximum sum and subarray start/end indices.",
        "subheading": "Implement and verify Subarray Optimization in the interactive workspace.",
        "task": {
            "title": "Implement Kadane's algorithm tracking maximum sum and subarray start/end indices.",
            "instructions": [
                "Implement Kadane's algorithm tracking maximum sum and subarray start/end indices.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "def max_sub_array_with_indices(nums: list[int]) -> tuple[int, int, int]:\n    # TODO: Implement Kadane's algorithm returning (max_sum, start_idx, end_idx)\n    max_sum = nums[0]\n    start = end = 0\n    return max_sum, start, end\n\nnums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]\nprint('Result:', max_sub_array_with_indices(nums))\n",
            "solutionCode": "def max_sub_array_with_indices(nums: list[int]) -> tuple[int, int, int]:\n    max_sum = nums[0]\n    curr_sum = nums[0]\n    start = end = temp_start = 0\n    for i in range(1, len(nums)):\n        if nums[i] > curr_sum + nums[i]:\n            curr_sum = nums[i]\n            temp_start = i\n        else:\n            curr_sum += nums[i]\n        if curr_sum > max_sum:\n            max_sum = curr_sum\n            start = temp_start\n            end = i\n    return max_sum, start, end\n\nnums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]\nprint('Result:', max_sub_array_with_indices(nums))\n",
            "expectedOutputPatterns": [
                "Result: (6, 3, 6)"
            ],
            "hint": "Track temp_start whenever nums[i] > curr_sum + nums[i]. When curr_sum > max_sum, update start = temp_start and end = i."
        },
        "keyTakeaway": "Successfully implemented and verified Subarray Optimization!"
    },
    {
        "id": "day43-step5",
        "stepNumber": 5,
        "title": "Day 43 Complete: Kadane's Algorithm & Maximum Subarray",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 43,
        "heading": "Mastery Achieved: Kadane's Algorithm & Maximum Subarray",
        "subheading": "You have solidified key mental models and techniques for Subarray Optimization.",
        "recapRows": [
            {
                "concept": "Local vs Global Optimum",
                "naiveIntuition": "Track all subarray combinations O(N^2)",
                "pythonReality": "Maintaining local maximum curr = max(x, curr + x) guarantees reaching the global maximum in O(N)"
            },
            {
                "concept": "Negative-Only Arrays",
                "naiveIntuition": "Maximum sum is 0",
                "pythonReality": "Subarray must be non-empty; the maximum sum is the single least-negative element"
            }
        ],
        "solidifiedConcepts": [
            "Kadane's Local vs Global Maxima",
            "Subarray Reset Condition"
        ],
        "nextDayPreview": {
            "dayNumber": 44,
            "title": "In-Place Array Rotation & Reversal",
            "description": "Rotate arrays in O(1) auxiliary space using the three-reversal trick, cyclic replacements, and block swapping."
        }
    }
]
},
  44: {
  "dayNumber": 44,
  "title": "In-Place Array Rotation & Reversal",
  "topicName": "Array Manipulations",
  "sectionId": "arrays-and-strings",
  "estimatedMinutes": 30,
  "difficulty": "DEVELOPING",
  "prerequisites": [
    40
  ],
  "concepts": [
    "Triple-Reversal Algorithm",
    "Block Swap Invariants"
  ],
  "practiceSkills": [
    "Array Manipulations Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Rotate arrays by k positions in O(N) time and O(1) auxiliary space using triple reversals",
    "Debug off-by-one pointer swaps on odd and even length segments"
  ],
  "practiceArchetype": "debugging",
  "flowTier": "tier2"
,
  "steps": [
    {
        "id": "day44-step1",
        "stepNumber": 1,
        "title": "In-Place Array Rotation & Reversal: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Array Manipulations",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Array Manipulations.",
        "markdownContent": [
            "In-Place Array Rotation by K steps can be performed in O(N) time and O(1) auxiliary space using the Triple-Reversal algorithm.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Array Manipulations**, remember the central principle: Three consecutive in-place reversals reorder array segments in O(N) time without allocating auxiliary memory."
        ],
        "snippets": [
            {
                "title": "Array Manipulations Implementation Template",
                "code": "# In-place rotation by k\ndef rotate(nums, k):\n    n = len(nums)\n    k %= n\n    def rev(l, r):\n        while l < r:\n            nums[l], nums[r] = nums[r], nums[l]\n            l += 1; r -= 1\n    rev(0, n - 1)\n    rev(0, k - 1)\n    rev(k, n - 1)",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Three consecutive in-place reversals reorder array segments in O(N) time without allocating auxiliary memory."
    },
    {
        "id": "day44-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Array Manipulations",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "To rotate right by K: normalize k = k % N. 1. Reverse entire array. 2. Reverse first k elements. 3. Reverse remaining N - k elements.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Three consecutive in-place reversals reorder array segments in O(N) time without allocating auxiliary memory.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Array Manipulations Core Invariant",
                "content": "Three consecutive in-place reversals reorder array segments in O(N) time without allocating auxiliary memory."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Three consecutive in-place reversals reorder array segments in O(N) time without allocating auxiliary memory."
    },
    {
        "id": "day44-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Array Manipulations",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d44-q1",
                "question": "Why is the step `k = k % len(nums)` essential before rotating?",
                "options": [
                    {
                        "id": "A",
                        "label": "Rotating an array of length N by N full cycles produces the identical original array; modulo eliminates redundant full rotations"
                    },
                    {
                        "id": "B",
                        "label": "To convert negative values of k into positive values"
                    },
                    {
                        "id": "C",
                        "label": "Because Python slice indices must be smaller than 10"
                    },
                    {
                        "id": "D",
                        "label": "To round k down to the nearest even number"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! If N = 5 and K = 12, rotating 12 times is identical to rotating 12 % 5 = 2 times. Modulo prevents out-of-bounds indexing.",
                    "B": "Incorrect: In Python k % n handles negative numbers, but the primary reason is eliminating redundant full cycles.",
                    "C": "Incorrect: Slices have no such limitation.",
                    "D": "Incorrect: K can be odd or even."
                }
            },
            {
                "id": "chk-d44-q2",
                "question": "What is the memory complexity of the Triple-Reversal rotation algorithm?",
                "options": [
                    {
                        "id": "A",
                        "label": "O(1) auxiliary space because pointer swaps mutate the original array in-place"
                    },
                    {
                        "id": "B",
                        "label": "O(N) auxiliary space because elements are copied into temporary lists"
                    },
                    {
                        "id": "C",
                        "label": "O(K) auxiliary space"
                    },
                    {
                        "id": "D",
                        "label": "O(log N) auxiliary space"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Elements are swapped directly within the existing buffer using two integer pointer indices; zero new lists are created.",
                    "B": "Incorrect: Slicing creates new lists, but triple reversal does not.",
                    "C": "Incorrect: K does not dictate memory allocation.",
                    "D": "Incorrect: The reversal helper is iterative, using O(1) stack frames."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day44-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Array Manipulations",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Debug off-by-one errors in in-place array triple reversal.",
        "subheading": "Implement and verify Array Manipulations in the interactive workspace.",
        "task": {
            "title": "Debug off-by-one errors in in-place array triple reversal.",
            "instructions": [
                "Debug off-by-one errors in in-place array triple reversal.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "# Day 44 Debugging Challenge: Array Rotation\n# BUG REPORT: This rotation function crashes with IndexError because boundary indices are off by one!\ndef rotate_buggy(nums: list[int], k: int) -> list[int]:\n    n = len(nums)\n    k %= n\n    def reverse(l, r):\n        while l < r:\n            nums[l], nums[r] = nums[r], nums[l]\n            l += 1\n            r -= 1\n    # BUG: Passing n instead of n - 1 causes IndexError!\n    reverse(0, n)\n    reverse(0, k)\n    reverse(k, n)\n    return nums\n\n# INSTRUCTION: Fix the boundary calls to pass valid inclusive indices.\nnums = [1, 2, 3, 4, 5, 6, 7]\nprint('Rotated:', rotate_buggy(nums, 3))\n",
            "solutionCode": "def rotate_buggy(nums: list[int], k: int) -> list[int]:\n    n = len(nums)\n    k %= n\n    def reverse(l, r):\n        while l < r:\n            nums[l], nums[r] = nums[r], nums[l]\n            l += 1\n            r -= 1\n    reverse(0, n - 1)\n    reverse(0, k - 1)\n    reverse(k, n - 1)\n    return nums\n\nnums = [1, 2, 3, 4, 5, 6, 7]\nprint('Rotated:', rotate_buggy(nums, 3))\n",
            "expectedOutputPatterns": [
                "Rotated: [5, 6, 7, 1, 2, 3, 4]"
            ],
            "hint": "Change `reverse(0, n)` to `reverse(0, n - 1)`, `reverse(0, k)` to `reverse(0, k - 1)`, and `reverse(k, n)` to `reverse(k, n - 1)`."
        },
        "keyTakeaway": "Successfully implemented and verified Array Manipulations!"
    },
    {
        "id": "day44-step5",
        "stepNumber": 5,
        "title": "Day 44 Complete: In-Place Array Rotation & Reversal",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 44,
        "heading": "Mastery Achieved: In-Place Array Rotation & Reversal",
        "subheading": "You have solidified key mental models and techniques for Array Manipulations.",
        "recapRows": [
            {
                "concept": "Triple Reversal Order",
                "naiveIntuition": "Shift elements one by one K times in O(N * K)",
                "pythonReality": "Reversing [0..N-1], [0..K-1], and [K..N-1] achieves the rotation in O(N) time and O(1) space"
            },
            {
                "concept": "Inclusive Indices",
                "naiveIntuition": "Pass len(nums) as right pointer",
                "pythonReality": "In-place pointer reversal uses inclusive indices: right boundary is len(nums) - 1"
            }
        ],
        "solidifiedConcepts": [
            "Triple-Reversal Algorithm",
            "Block Swap Invariants"
        ],
        "nextDayPreview": {
            "dayNumber": 45,
            "title": "String Parsing & State Machine Tokenization",
            "description": "Build state machines to parse complex strings, validate numeric formats, and implement string-to-integer (atoi)."
        }
    }
]
},
  45: {
  "dayNumber": 45,
  "title": "String Parsing & State Machine Tokenization",
  "topicName": "String State Machines",
  "sectionId": "arrays-and-strings",
  "estimatedMinutes": 40,
  "difficulty": "DEVELOPING",
  "prerequisites": [
    3,
    44
  ],
  "concepts": [
    "Deterministic Finite Automata (DFA)",
    "Edge Case Parsing Guardrails"
  ],
  "practiceSkills": [
    "String State Machines Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Design a deterministic finite automaton state machine to parse strings into typed tokens",
    "Implement robust string-to-integer conversion (atoi) handling leading whitespace, signs, and clamping"
  ],
  "practiceArchetype": "algorithm",
  "flowTier": "tier3"
,
  "steps": [
    {
        "id": "day45-step1",
        "stepNumber": 1,
        "title": "String Parsing & State Machine Tokenization: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: String State Machines",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for String State Machines.",
        "markdownContent": [
            "String Parsing and Deterministic Finite Automata (DFA) model transitions between formal parser states (Whitespace, Sign, Digits) to parse tokens robustly.",
            "### Foundational Mental Model\nWhen approaching problems requiring **String State Machines**, remember the central principle: DFA state machines structure complex string parsing logic, eliminating fragile nested conditional branching."
        ],
        "snippets": [
            {
                "title": "String State Machines Implementation Template",
                "code": "# DFA State Machine for string-to-integer\ndef my_atoi(s):\n    s = s.strip()\n    if not s: return 0\n    sign = -1 if s[0] == '-' else 1\n    if s[0] in '+-': s = s[1:]\n    res = 0\n    for ch in s:\n        if not ch.isdigit(): break\n        res = res * 10 + int(ch)\n    res *= sign\n    return max(-2**31, min(2**31 - 1, res))",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "DFA state machines structure complex string parsing logic, eliminating fragile nested conditional branching."
    },
    {
        "id": "day45-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: String State Machines",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "In string-to-integer (atoi): define states: 0=START, 1=SIGN, 2=IN_NUM. Handle whitespace, optional '+' or '-', parse consecutive digits with 32-bit clamping [-2^31, 2^31 - 1].",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: DFA state machines structure complex string parsing logic, eliminating fragile nested conditional branching.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "String State Machines Core Invariant",
                "content": "DFA state machines structure complex string parsing logic, eliminating fragile nested conditional branching."
            }
        ],
        "keyTakeaway": "Operational invariant locked: DFA state machines structure complex string parsing logic, eliminating fragile nested conditional branching."
    },
    {
        "id": "day45-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: String State Machines",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d45-q1",
                "question": "Why is a Deterministic Finite Automaton (DFA) preferred over chained regular expressions for complex token parsing in high-throughput systems?",
                "options": [
                    {
                        "id": "A",
                        "label": "DFAs parse character by character in guaranteed O(N) time without catastrophic backtracking regex stalls"
                    },
                    {
                        "id": "B",
                        "label": "DFAs use less RAM because they do not support strings"
                    },
                    {
                        "id": "C",
                        "label": "Regular expressions cannot match numeric characters"
                    },
                    {
                        "id": "D",
                        "label": "DFAs automatically handle 64-bit integer overflows"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! A DFA processes each character exactly once in O(1) state transition time, preventing exponential regex backtracking vulnerabilities (ReDoS).",
                    "B": "Incorrect: DFAs operate on string streams.",
                    "C": "Incorrect: Regex matches digits via \\d.",
                    "D": "Incorrect: Clamping must be implemented explicitly in the accumulator logic."
                }
            },
            {
                "id": "chk-d45-q2",
                "question": "What are the 32-bit signed integer minimum and maximum clamping limits in standard coding challenges?",
                "options": [
                    {
                        "id": "A",
                        "label": "-2^31 (-2,147,483,648) and 2^31 - 1 (2,147,483,647)"
                    },
                    {
                        "id": "B",
                        "label": "-2^32 and 2^32"
                    },
                    {
                        "id": "C",
                        "label": "0 and 2^31"
                    },
                    {
                        "id": "D",
                        "label": "-1,000,000 and 1,000,000"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Standard two's complement 32-bit signed integers span -2,147,483,648 to 2,147,483,647.",
                    "B": "Incorrect: 2^32 is unsigned 32-bit width.",
                    "C": "Incorrect: Signed integers include negative ranges.",
                    "D": "Incorrect: Arbitrary decimal constants do not match hardware boundaries."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day45-step4",
        "stepNumber": 4,
        "title": "Guided Practice: String State Machines",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Build a robust string-to-integer (atoi) parser with sign handling and clamping.",
        "subheading": "Implement and verify String State Machines in the interactive workspace.",
        "task": {
            "title": "Build a robust string-to-integer (atoi) parser with sign handling and clamping.",
            "instructions": [
                "Build a robust string-to-integer (atoi) parser with sign handling and clamping.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "def my_atoi(s: str) -> int:\n    # TODO: Implement string-to-integer conversion\n    # 1. Discard leading whitespace\n    # 2. Check for optional '+' or '-'\n    # 3. Read consecutive digits and convert\n    # 4. Clamp within [-2**31, 2**31 - 1]\n    return 0\n\nprint('Test 1:', my_atoi('   -42'))\nprint('Test 2:', my_atoi('4193 with words'))\nprint('Test 3:', my_atoi('-91283472332'))\n",
            "solutionCode": "def my_atoi(s: str) -> int:\n    s = s.strip()\n    if not s:\n        return 0\n    sign = 1\n    idx = 0\n    if s[0] == '-':\n        sign = -1\n        idx = 1\n    elif s[0] == '+':\n        idx = 1\n    res = 0\n    while idx < len(s) and s[idx].isdigit():\n        res = res * 10 + (ord(s[idx]) - ord('0'))\n        idx += 1\n    res *= sign\n    INT_MIN, INT_MAX = -2**31, 2**31 - 1\n    if res < INT_MIN:\n        return INT_MIN\n    if res > INT_MAX:\n        return INT_MAX\n    return res\n\nprint('Test 1:', my_atoi('   -42'))\nprint('Test 2:', my_atoi('4193 with words'))\nprint('Test 3:', my_atoi('-91283472332'))\n",
            "expectedOutputPatterns": [
                "Test 1: -42",
                "Test 2: 4193",
                "Test 3: -2147483648"
            ],
            "hint": "Strip whitespace, check sign, accumulate digits with res = res * 10 + int(ch), then clamp between -2**31 and 2**31 - 1."
        },
        "keyTakeaway": "Successfully implemented and verified String State Machines!"
    },
    {
        "id": "day45-step5",
        "stepNumber": 5,
        "title": "Day 45 Complete: String Parsing & State Machine Tokenization",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 45,
        "heading": "Mastery Achieved: String Parsing & State Machine Tokenization",
        "subheading": "You have solidified key mental models and techniques for String State Machines.",
        "recapRows": [
            {
                "concept": "Digit Parsing",
                "naiveIntuition": "int(s) parses all valid strings",
                "pythonReality": "int('4193 with words') raises ValueError; manual state machine stops cleanly at non-digits"
            },
            {
                "concept": "Clamping",
                "naiveIntuition": "Python handles huge integers automatically",
                "pythonReality": "Python integers have arbitrary precision, but interview specifications mandate explicit 32-bit hardware clamping"
            }
        ],
        "solidifiedConcepts": [
            "Deterministic Finite Automata (DFA)",
            "Edge Case Parsing Guardrails"
        ],
        "nextDayPreview": {
            "dayNumber": 46,
            "title": "Palindrome Verification & Center Expansion",
            "description": "Verify palindromes using two pointers and find longest palindromic substrings by expanding around 2N-1 centers."
        }
    }
]
},
  46: {
  "dayNumber": 46,
  "title": "Palindrome Verification & Center Expansion",
  "topicName": "Palindromes",
  "sectionId": "arrays-and-strings",
  "estimatedMinutes": 35,
  "difficulty": "DEVELOPING",
  "prerequisites": [
    39,
    45
  ],
  "concepts": [
    "Center Expansion Paradigm",
    "Odd vs Even Length Palindromes"
  ],
  "practiceSkills": [
    "Palindromes Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Expand around 2N - 1 potential centers to identify palindromic substrings in O(N^2) time and O(1) space",
    "Verify alphanumeric palindrome sentences using two pointers skipping non-alphanumeric characters"
  ],
  "practiceArchetype": "problem",
  "flowTier": "tier2"
,
  "steps": [
    {
        "id": "day46-step1",
        "stepNumber": 1,
        "title": "Palindrome Verification & Center Expansion: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Palindromes",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Palindromes.",
        "markdownContent": [
            "Palindrome Verification uses opposing two pointers, while finding the Longest Palindromic Substring expands outward around 2N - 1 possible centers in O(N^2) time and O(1) space.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Palindromes**, remember the central principle: Expanding around 2N - 1 centers identifies all palindromic substrings in O(N^2) time and O(1) auxiliary memory."
        ],
        "snippets": [
            {
                "title": "Palindromes Implementation Template",
                "code": "# Expand around center\ndef expand(s, l, r):\n    while l >= 0 and r < len(s) and s[l] == s[r]:\n        l -= 1; r += 1\n    return s[l + 1:r]",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Expanding around 2N - 1 centers identifies all palindromic substrings in O(N^2) time and O(1) auxiliary memory."
    },
    {
        "id": "day46-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Palindromes",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "A string of length N has N single-character centers (odd palindromes 'aba') and N - 1 two-character center gaps (even palindromes 'abba'). Expanding outward verifies mirror equality.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Expanding around 2N - 1 centers identifies all palindromic substrings in O(N^2) time and O(1) auxiliary memory.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Palindromes Core Invariant",
                "content": "Expanding around 2N - 1 centers identifies all palindromic substrings in O(N^2) time and O(1) auxiliary memory."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Expanding around 2N - 1 centers identifies all palindromic substrings in O(N^2) time and O(1) auxiliary memory."
    },
    {
        "id": "day46-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Palindromes",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d46-q1",
                "question": "Why are there 2N - 1 potential centers in a string of length N?",
                "options": [
                    {
                        "id": "A",
                        "label": "There are N character centers for odd-length palindromes and N - 1 inter-character gaps for even-length palindromes"
                    },
                    {
                        "id": "B",
                        "label": "Because strings are indexed from -N to N - 1 in Python"
                    },
                    {
                        "id": "C",
                        "label": "Every palindrome must contain at least 2 centers"
                    },
                    {
                        "id": "D",
                        "label": "It accounts for uppercase and lowercase ASCII characters"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! An odd-length palindrome like 'aba' centers on 'b' (N positions). An even-length palindrome like 'abba' centers between 'b' and 'b' (N - 1 positions). Total = 2N - 1.",
                    "B": "Incorrect: Negative indexing is a syntax feature, not a structural count of symmetry axes.",
                    "C": "Incorrect: Odd palindromes have a single middle character.",
                    "D": "Incorrect: Case sensitivity is unrelated to center count."
                }
            },
            {
                "id": "chk-d46-q2",
                "question": "What is the time complexity of the Expand Around Center algorithm for finding the longest palindromic substring?",
                "options": [
                    {
                        "id": "A",
                        "label": "O(N^2) time and O(1) auxiliary space"
                    },
                    {
                        "id": "B",
                        "label": "O(N^3) time and O(N) space"
                    },
                    {
                        "id": "C",
                        "label": "O(N log N) time"
                    },
                    {
                        "id": "D",
                        "label": "O(N) time and O(N) space"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! There are 2N - 1 centers, and each expansion extends at most O(N) steps. Total time: O(N^2). Auxiliary space is O(1) because only boundary pointers are stored.",
                    "B": "Incorrect: Brute-force substring checking is O(N^3), but expanding around centers avoids the third loop.",
                    "C": "Incorrect: No divide-and-conquer sorting is performed.",
                    "D": "Incorrect: Linear O(N) requires Manacher's algorithm."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day46-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Palindromes",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Find the longest palindromic substring via center expansion.",
        "subheading": "Implement and verify Palindromes in the interactive workspace.",
        "task": {
            "title": "Find the longest palindromic substring via center expansion.",
            "instructions": [
                "Find the longest palindromic substring via center expansion.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "def longest_palindrome(s: str) -> str:\n    if not s:\n        return ''\n    # TODO: Helper function to expand around (l, r) and return longest palindrome\n    # Loop i through range(len(s)), expanding around (i, i) and (i, i + 1)\n    return ''\n\ns = 'babad'\nprint('Longest palindrome:', longest_palindrome(s))\n",
            "solutionCode": "def longest_palindrome(s: str) -> str:\n    if not s:\n        return ''\n    def expand(l: int, r: int) -> str:\n        while l >= 0 and r < len(s) and s[l] == s[r]:\n            l -= 1\n            r += 1\n        return s[l + 1:r]\n    longest = ''\n    for i in range(len(s)):\n        p1 = expand(i, i)\n        p2 = expand(i, i + 1)\n        if len(p1) > len(longest):\n            longest = p1\n        if len(p2) > len(longest):\n            longest = p2\n    return longest\n\ns = 'babad'\nprint('Longest palindrome:', longest_palindrome(s))\n",
            "expectedOutputPatterns": [
                "Longest palindrome: bab"
            ],
            "hint": "Write helper `expand(l, r)` that loops `while l >= 0 and r < len(s) and s[l] == s[r]: l -= 1; r += 1; return s[l+1:r]`."
        },
        "keyTakeaway": "Successfully implemented and verified Palindromes!"
    },
    {
        "id": "day46-step5",
        "stepNumber": 5,
        "title": "Day 46 Complete: Palindrome Verification & Center Expansion",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 46,
        "heading": "Mastery Achieved: Palindrome Verification & Center Expansion",
        "subheading": "You have solidified key mental models and techniques for Palindromes.",
        "recapRows": [
            {
                "concept": "Center Duality",
                "naiveIntuition": "Only expand around single characters",
                "pythonReality": "Must expand around both single characters (i, i) and adjacent pairs (i, i + 1)"
            },
            {
                "concept": "Slice Boundary",
                "naiveIntuition": "Return s[l:r]",
                "pythonReality": "When loop terminates, s[l] != s[r]; valid palindrome boundaries are l + 1 up to r"
            }
        ],
        "solidifiedConcepts": [
            "Center Expansion Paradigm",
            "Odd vs Even Length Palindromes"
        ],
        "nextDayPreview": {
            "dayNumber": 47,
            "title": "2D Matrix Traversals & Spiral Order",
            "description": "Navigate 2D grids, extract diagonals, rotate matrices in-place, and traverse boundary spirals without allocations."
        }
    }
]
},
  47: {
  "dayNumber": 47,
  "title": "2D Matrix Traversals & Spiral Order",
  "topicName": "Matrix Algorithms",
  "sectionId": "arrays-and-strings",
  "estimatedMinutes": 35,
  "difficulty": "DEVELOPING",
  "prerequisites": [
    36
  ],
  "concepts": [
    "Matrix Boundary Invariants",
    "Directional Offset Stepping"
  ],
  "practiceSkills": [
    "Matrix Algorithms Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Traverse an M x N matrix in spiral order while updating top, bottom, left, and right boundary limits",
    "Rotate matrices 90 degrees in-place by transposing and reversing rows"
  ],
  "practiceArchetype": "problem",
  "flowTier": "tier2"
,
  "steps": [
    {
        "id": "day47-step1",
        "stepNumber": 1,
        "title": "2D Matrix Traversals & Spiral Order: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Matrix Algorithms",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Matrix Algorithms.",
        "markdownContent": [
            "2D Matrix Spiral Order Traversal navigates outer boundaries inward, shifting top, bottom, left, and right boundary variables to visit all M x N elements without memory allocation.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Matrix Algorithms**, remember the central principle: Maintain four boundary limits and verify boundary crossing invariants on every direction transition."
        ],
        "snippets": [
            {
                "title": "Matrix Algorithms Implementation Template",
                "code": "# Spiral Matrix Traversal\ndef spiral_order(matrix):\n    if not matrix: return []\n    res = []\n    T, B, L, R = 0, len(matrix) - 1, 0, len(matrix[0]) - 1\n    while T <= B and L <= R:\n        for c in range(L, R + 1): res.append(matrix[T][c])\n        T += 1\n        for r in range(T, B + 1): res.append(matrix[r][R])\n        R -= 1\n        if T <= B:\n            for c in range(R, L - 1, -1): res.append(matrix[B][c])\n            B -= 1\n        if L <= R:\n            for r in range(B, T - 1, -1): res.append(matrix[r][L])\n            L += 1\n    return res",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Maintain four boundary limits and verify boundary crossing invariants on every direction transition."
    },
    {
        "id": "day47-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Matrix Algorithms",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "1. Traverse top row (left to right), increment top. 2. Traverse right col (top to bottom), decrement right. 3. If top <= bottom, traverse bottom row (right to left), decrement bottom. 4. If left <= right, traverse left col (bottom to top), increment left.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Maintain four boundary limits and verify boundary crossing invariants on every direction transition.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Matrix Algorithms Core Invariant",
                "content": "Maintain four boundary limits and verify boundary crossing invariants on every direction transition."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Maintain four boundary limits and verify boundary crossing invariants on every direction transition."
    },
    {
        "id": "day47-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Matrix Algorithms",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d47-q1",
                "question": "Why must we verify `if T <= B` before traversing the bottom row from right to left in spiral traversal?",
                "options": [
                    {
                        "id": "A",
                        "label": "Because incrementing T in the first step might cause T to exceed B on single-row matrices, causing duplicate row visits"
                    },
                    {
                        "id": "B",
                        "label": "To check if the matrix elements are sorted"
                    },
                    {
                        "id": "C",
                        "label": "Because range() crashes if stop is smaller than start"
                    },
                    {
                        "id": "D",
                        "label": "To handle negative coordinate indices"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! If a matrix has 1 row (T=0, B=0), after traversing right, T becomes 1. Without `if T <= B`, the bottom traversal would re-visit row 0 in reverse!",
                    "B": "Incorrect: Spiral order applies to any matrix regardless of sorting.",
                    "C": "Incorrect: range with step -1 handles start > stop gracefully.",
                    "D": "Incorrect: Indices are non-negative."
                }
            },
            {
                "id": "chk-d47-q2",
                "question": "What is the time and auxiliary space complexity of spiral matrix traversal?",
                "options": [
                    {
                        "id": "A",
                        "label": "O(M * N) time and O(1) auxiliary space (excluding output buffer)"
                    },
                    {
                        "id": "B",
                        "label": "O(M + N) time and O(M * N) space"
                    },
                    {
                        "id": "C",
                        "label": "O(N^2) time and O(N) space"
                    },
                    {
                        "id": "D",
                        "label": "O(M * N log(M * N)) time"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Every cell is visited exactly once, requiring O(M * N) time. Auxiliary space is O(1) as only 4 boundary integers are stored.",
                    "B": "Incorrect: Must visit all M * N cells, which is O(M * N).",
                    "C": "Incorrect: M and N may differ.",
                    "D": "Incorrect: No sorting or divide-and-conquer is involved."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day47-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Matrix Algorithms",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Traverse an M x N matrix in clockwise spiral order.",
        "subheading": "Implement and verify Matrix Algorithms in the interactive workspace.",
        "task": {
            "title": "Traverse an M x N matrix in clockwise spiral order.",
            "instructions": [
                "Traverse an M x N matrix in clockwise spiral order.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "def spiral_order(matrix: list[list[int]]) -> list[int]:\n    if not matrix or not matrix[0]:\n        return []\n    res = []\n    top, bottom = 0, len(matrix) - 1\n    left, right = 0, len(matrix[0]) - 1\n    # TODO: While top <= bottom and left <= right, execute the 4 boundary passes\n    \n    return res\n\nmatrix = [\n    [1, 2, 3],\n    [4, 5, 6],\n    [7, 8, 9]\n]\nprint('Spiral order:', spiral_order(matrix))\n",
            "solutionCode": "def spiral_order(matrix: list[list[int]]) -> list[int]:\n    if not matrix or not matrix[0]:\n        return []\n    res = []\n    top, bottom = 0, len(matrix) - 1\n    left, right = 0, len(matrix[0]) - 1\n    while top <= bottom and left <= right:\n        for c in range(left, right + 1):\n            res.append(matrix[top][c])\n        top += 1\n        for r in range(top, bottom + 1):\n            res.append(matrix[r][right])\n        right -= 1\n        if top <= bottom:\n            for c in range(right, left - 1, -1):\n                res.append(matrix[bottom][c])\n            bottom -= 1\n        if left <= right:\n            for r in range(bottom, top - 1, -1):\n                res.append(matrix[r][left])\n            left += 1\n    return res\n\nmatrix = [\n    [1, 2, 3],\n    [4, 5, 6],\n    [7, 8, 9]\n]\nprint('Spiral order:', spiral_order(matrix))\n",
            "expectedOutputPatterns": [
                "Spiral order: [1, 2, 3, 6, 9, 8, 7, 4, 5]"
            ],
            "hint": "Follow the four passes: left to right on top, top to bottom on right, right to left on bottom (guarded by top <= bottom), and bottom to top on left (guarded by left <= right)."
        },
        "keyTakeaway": "Successfully implemented and verified Matrix Algorithms!"
    },
    {
        "id": "day47-step5",
        "stepNumber": 5,
        "title": "Day 47 Complete: 2D Matrix Traversals & Spiral Order",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 47,
        "heading": "Mastery Achieved: 2D Matrix Traversals & Spiral Order",
        "subheading": "You have solidified key mental models and techniques for Matrix Algorithms.",
        "recapRows": [
            {
                "concept": "Boundary Contraction",
                "naiveIntuition": "Track visited coordinates in a hash set",
                "pythonReality": "Four integer boundary boundaries (top, bottom, left, right) simulate the shrinking spiral in O(1) space"
            },
            {
                "concept": "Single-Row Guard",
                "naiveIntuition": "The while loop condition is sufficient",
                "pythonReality": "top and right mutate midway through an iteration; inner guards are mandatory to prevent single-row duplicate passes"
            }
        ],
        "solidifiedConcepts": [
            "Matrix Boundary Invariants",
            "Directional Offset Stepping"
        ],
        "nextDayPreview": {
            "dayNumber": 48,
            "title": "2D Prefix Sums & Matrix Accumulation",
            "description": "Construct 2D prefix sum tables using the inclusion-exclusion principle to query rectangular submatrix sums in O(1) time."
        }
    }
]
},
  48: {
  "dayNumber": 48,
  "title": "2D Prefix Sums & Matrix Accumulation",
  "topicName": "2D Prefix Sums",
  "sectionId": "arrays-and-strings",
  "estimatedMinutes": 40,
  "difficulty": "DEVELOPING",
  "prerequisites": [
    37,
    47
  ],
  "concepts": [
    "Inclusion-Exclusion Principle",
    "O(1) Submatrix Sum Queries"
  ],
  "practiceSkills": [
    "2D Prefix Sums Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Construct a 2D prefix sum table using the 2D inclusion-exclusion principle",
    "Evaluate arbitrary submatrix sum queries in strict O(1) time"
  ],
  "practiceArchetype": "algorithm",
  "flowTier": "tier3"
,
  "steps": [
    {
        "id": "day48-step1",
        "stepNumber": 1,
        "title": "2D Prefix Sums & Matrix Accumulation: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: 2D Prefix Sums",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for 2D Prefix Sums.",
        "markdownContent": [
            "Rotating an N x N matrix 90 degrees clockwise in-place is achieved by a 2-step geometric transformation: transpose the matrix across its main diagonal, then reverse every row horizontally.",
            "### Foundational Mental Model\nWhen approaching problems requiring **2D Prefix Sums**, remember the central principle: Clockwise 90-degree rotation = Transpose + Horizontal Row Reversal in O(1) space."
        ],
        "snippets": [
            {
                "title": "2D Prefix Sums Implementation Template",
                "code": "# In-place 90 degree clockwise matrix rotation\ndef rotate_matrix(mat):\n    n = len(mat)\n    # 1. Transpose: flip across main diagonal\n    for i in range(n):\n        for j in range(i + 1, n):\n            mat[i][j], mat[j][i] = mat[j][i], mat[i][j]\n    # 2. Reverse each row\n    for row in mat:\n        row.reverse()\n    return mat",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Clockwise 90-degree rotation = Transpose + Horizontal Row Reversal in O(1) space."
    },
    {
        "id": "day48-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: 2D Prefix Sums",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Step 1 (Transpose): Swap matrix[i][j] with matrix[j][i] for all j > i. This flips rows into columns. Step 2 (Reverse Rows): Reverse each row in-place via two pointers or row.reverse(). Both steps run strictly in O(N^2) time with O(1) auxiliary space.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Clockwise 90-degree rotation = Transpose + Horizontal Row Reversal in O(1) space.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "2D Prefix Sums Core Invariant",
                "content": "Clockwise 90-degree rotation = Transpose + Horizontal Row Reversal in O(1) space."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Clockwise 90-degree rotation = Transpose + Horizontal Row Reversal in O(1) space."
    },
    {
        "id": "day48-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: 2D Prefix Sums",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d48-q1",
                "question": "Why does transposing a matrix followed by reversing each row achieve a 90-degree clockwise rotation?",
                "options": [
                    {
                        "id": "A",
                        "label": "Transposing converts cell (r, c) to (c, r), and reversing the row maps column index c to (N - 1 - c), resulting in (r, c) -> (c, N - 1 - r)"
                    },
                    {
                        "id": "B",
                        "label": "Because reversing rows multiplies the matrix by -1"
                    },
                    {
                        "id": "C",
                        "label": "Because transposing shifts all cells diagonally left"
                    },
                    {
                        "id": "D",
                        "label": "It only works for identity matrices"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! In a 90-degree clockwise turn, cell (r, c) must land at (c, N - 1 - r). Transpose places (r, c) at (c, r), and reversing row c moves column r to N - 1 - r. The composition yields exact clockwise rotation in-place.",
                    "B": "Incorrect: Row reversal rearranges columns; it does not negate numeric values.",
                    "C": "Incorrect: Transposing reflects across the main diagonal.",
                    "D": "Incorrect: Transpose + reverse works on any square N x N matrix."
                }
            },
            {
                "id": "chk-d48-q2",
                "question": "What is the auxiliary space complexity of rotating an N x N matrix in-place using Transpose + Reverse?",
                "options": [
                    {
                        "id": "A",
                        "label": "O(1) auxiliary space, modifying the existing matrix buffers directly"
                    },
                    {
                        "id": "B",
                        "label": "O(N^2) auxiliary space"
                    },
                    {
                        "id": "C",
                        "label": "O(N) auxiliary space"
                    },
                    {
                        "id": "D",
                        "label": "O(log N) stack space"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Swapping elements in-place requires only a single temporary variable during assignment, achieving strict O(1) extra space.",
                    "B": "Incorrect: Creating a new rotated matrix takes O(N^2), but the in-place method uses O(1).",
                    "C": "Incorrect: Zero extra row arrays are allocated.",
                    "D": "Incorrect: The algorithm is purely iterative with zero recursion."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day48-step4",
        "stepNumber": 4,
        "title": "Guided Practice: 2D Prefix Sums",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Rotate an N x N matrix 90 degrees clockwise in-place.",
        "subheading": "Implement and verify 2D Prefix Sums in the interactive workspace.",
        "task": {
            "title": "Rotate an N x N matrix 90 degrees clockwise in-place.",
            "instructions": [
                "Rotate an N x N matrix 90 degrees clockwise in-place.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "def rotate(matrix: list[list[int]]) -> None:\n    n = len(matrix)\n    # TODO 1: Transpose matrix in-place (swap matrix[i][j] and matrix[j][i] for j > i)\n    \n    # TODO 2: Reverse each row in-place\n    pass\n\nmat = [\n    [1, 2, 3],\n    [4, 5, 6],\n    [7, 8, 9]\n]\nrotate(mat)\nprint('Rotated matrix:', mat)\n",
            "solutionCode": "def rotate(matrix: list[list[int]]) -> None:\n    n = len(matrix)\n    for i in range(n):\n        for j in range(i + 1, n):\n            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]\n    for row in matrix:\n        row.reverse()\n\nmat = [\n    [1, 2, 3],\n    [4, 5, 6],\n    [7, 8, 9]\n]\nrotate(mat)\nprint('Rotated matrix:', mat)\n",
            "expectedOutputPatterns": [
                "Rotated matrix: [[7, 4, 1], [8, 5, 2], [9, 6, 3]]"
            ],
            "hint": "Loop i from 0 to n-1 and j from i+1 to n-1: swap matrix[i][j], matrix[j][i]. Then for row in matrix: row.reverse()."
        },
        "keyTakeaway": "Successfully implemented and verified 2D Prefix Sums!"
    },
    {
        "id": "day48-step5",
        "stepNumber": 5,
        "title": "Day 48 Complete: 2D Prefix Sums & Matrix Accumulation",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 48,
        "heading": "Mastery Achieved: 2D Prefix Sums & Matrix Accumulation",
        "subheading": "You have solidified key mental models and techniques for 2D Prefix Sums.",
        "recapRows": [
            {
                "concept": "Transpose + Reverse Invariant",
                "naiveIntuition": "Allocate a new N x N matrix and copy cells (O(N^2) space)",
                "pythonReality": "Transposing across diagonal followed by reversing rows achieves 90-degree clockwise rotation strictly in-place with O(1) extra memory"
            },
            {
                "concept": "Diagonal Invariant",
                "naiveIntuition": "Loop through all i and all j during transpose",
                "pythonReality": "Looping j from i+1 to n-1 ensures each pair is swapped exactly once; looping all j would un-swap elements back to original"
            }
        ],
        "solidifiedConcepts": [
            "Inclusion-Exclusion Principle",
            "O(1) Submatrix Sum Queries"
        ],
        "nextDayPreview": {
            "dayNumber": 49,
            "title": "Intervals: Sorting & Merging Overlaps",
            "description": "Sort intervals, merge overlapping ranges, insert new intervals, and determine interval intersections in O(N log N) time."
        }
    }
]
},
  49: {
  "dayNumber": 49,
  "title": "Intervals: Sorting & Merging Overlaps",
  "topicName": "Interval Scheduling",
  "sectionId": "arrays-and-strings",
  "estimatedMinutes": 35,
  "difficulty": "DEVELOPING",
  "prerequisites": [
    25,
    40
  ],
  "concepts": [
    "Interval Overlap Invariant",
    "Greedy Interval Merging"
  ],
  "practiceSkills": [
    "Interval Scheduling Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Sort intervals by start times and merge overlapping segments in O(N log N) time",
    "Determine non-overlapping intervals and schedule rooms using boundary scan lines"
  ],
  "practiceArchetype": "problem",
  "flowTier": "tier2"
,
  "steps": [
    {
        "id": "day49-step1",
        "stepNumber": 1,
        "title": "Intervals: Sorting & Merging Overlaps: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Interval Scheduling",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Interval Scheduling.",
        "markdownContent": [
            "Interval Problems require sorting intervals by start times (or end times) so overlapping relationships can be evaluated monotonically in O(N log N) time.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Interval Scheduling**, remember the central principle: Sorting intervals unlocks linear merge passes; overlap is tested via curr.start <= prev.end."
        ],
        "snippets": [
            {
                "title": "Interval Scheduling Implementation Template",
                "code": "# Merge Overlapping Intervals\ndef merge_intervals(intervals):\n    intervals.sort(key=lambda x: x[0])\n    merged = [intervals[0]]\n    for curr in intervals[1:]:\n        if curr[0] <= merged[-1][1]:\n            merged[-1][1] = max(merged[-1][1], curr[1])\n        else:\n            merged.append(curr)\n    return merged",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Sorting intervals unlocks linear merge passes; overlap is tested via curr.start <= prev.end."
    },
    {
        "id": "day49-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Interval Scheduling",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Sort intervals by start time. Maintain merged = [intervals[0]]. For each curr: if curr.start <= merged[-1].end: merged[-1].end = max(merged[-1].end, curr.end) (overlap). Else: merged.append(curr).",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Sorting intervals unlocks linear merge passes; overlap is tested via curr.start <= prev.end.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Interval Scheduling Core Invariant",
                "content": "Sorting intervals unlocks linear merge passes; overlap is tested via curr.start <= prev.end."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Sorting intervals unlocks linear merge passes; overlap is tested via curr.start <= prev.end."
    },
    {
        "id": "day49-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Interval Scheduling",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d49-q1",
                "question": "Why is sorting by start time necessary before merging overlapping intervals?",
                "options": [
                    {
                        "id": "A",
                        "label": "It guarantees that any interval that can overlap with the current merged interval appears immediately next in the sequence"
                    },
                    {
                        "id": "B",
                        "label": "Because Python's sort() function runs in O(N) time"
                    },
                    {
                        "id": "C",
                        "label": "To ensure intervals are sorted in descending order of length"
                    },
                    {
                        "id": "D",
                        "label": "It is not necessary; intervals can be merged in random order"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Sorting establishes temporal monotonicity: once an interval starts after the current merged end time, no subsequent interval can ever overlap with the current merged interval.",
                    "B": "Incorrect: Comparison sort takes O(N log N).",
                    "C": "Incorrect: Length is not used as the primary sort key.",
                    "D": "Incorrect: Without sorting, finding all overlapping components requires O(N^2) pairwise checks."
                }
            },
            {
                "id": "chk-d49-q2",
                "question": "When two intervals [start1, end1] and [start2, end2] overlap (start2 <= end1), what is the new merged end time?",
                "options": [
                    {
                        "id": "A",
                        "label": "max(end1, end2)"
                    },
                    {
                        "id": "B",
                        "label": "end2"
                    },
                    {
                        "id": "C",
                        "label": "end1 + end2"
                    },
                    {
                        "id": "D",
                        "label": "min(end1, end2)"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! The second interval might be completely contained within the first (e.g. [1, 5] and [2, 3]), so the merged end must be the maximum of both ends.",
                    "B": "Incorrect: If end2 < end1, using end2 would incorrectly shrink the interval.",
                    "C": "Incorrect: Summing ends falsely extends the interval duration.",
                    "D": "Incorrect: Minimum calculates intersection, not union merge."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day49-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Interval Scheduling",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Merge all overlapping intervals in an input collection.",
        "subheading": "Implement and verify Interval Scheduling in the interactive workspace.",
        "task": {
            "title": "Merge all overlapping intervals in an input collection.",
            "instructions": [
                "Merge all overlapping intervals in an input collection.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "def merge(intervals: list[list[int]]) -> list[list[int]]:\n    if not intervals:\n        return []\n    # TODO 1: Sort intervals by start time\n    # TODO 2: Initialize merged list with first interval\n    # TODO 3: Iterate and merge when curr[0] <= merged[-1][1]\n    return []\n\nintervals = [[1, 3], [2, 6], [8, 10], [15, 18]]\nprint('Merged:', merge(intervals))\n",
            "solutionCode": "def merge(intervals: list[list[int]]) -> list[list[int]]:\n    if not intervals:\n        return []\n    intervals.sort(key=lambda x: x[0])\n    merged = [intervals[0]]\n    for curr in intervals[1:]:\n        if curr[0] <= merged[-1][1]:\n            merged[-1][1] = max(merged[-1][1], curr[1])\n        else:\n            merged.append(curr)\n    return merged\n\nintervals = [[1, 3], [2, 6], [8, 10], [15, 18]]\nprint('Merged:', merge(intervals))\n",
            "expectedOutputPatterns": [
                "Merged: [[1, 6], [8, 10], [15, 18]]"
            ],
            "hint": "Sort by lambda x: x[0], initialize merged = [intervals[0]], loop checking if curr[0] <= merged[-1][1] and update merged[-1][1] = max(merged[-1][1], curr[1])."
        },
        "keyTakeaway": "Successfully implemented and verified Interval Scheduling!"
    },
    {
        "id": "day49-step5",
        "stepNumber": 5,
        "title": "Day 49 Complete: Intervals: Sorting & Merging Overlaps",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 49,
        "heading": "Mastery Achieved: Intervals: Sorting & Merging Overlaps",
        "subheading": "You have solidified key mental models and techniques for Interval Scheduling.",
        "recapRows": [
            {
                "concept": "Interval Sorting",
                "naiveIntuition": "Compare all pairs to find overlaps O(N^2)",
                "pythonReality": "Sorting by start time in O(N log N) allows a single linear O(N) sweep to merge all overlapping segments"
            },
            {
                "concept": "Contained Interval",
                "naiveIntuition": "Always set end to curr[1]",
                "pythonReality": "If curr is completely inside merged[-1], max(merged[-1][1], curr[1]) prevents shrinking the end boundary"
            }
        ],
        "solidifiedConcepts": [
            "Interval Overlap Invariant",
            "Greedy Interval Merging"
        ],
        "nextDayPreview": {
            "dayNumber": 50,
            "title": "Section 4 Capstone: Linear Array Patterns",
            "description": "Synthesize two-pointers, sliding windows, prefix sums, and interval merging into a composite challenge."
        }
    }
]
},
  50: {
  "dayNumber": 50,
  "title": "Section 4 Capstone: Linear Array Patterns",
  "topicName": "Array Capstone",
  "sectionId": "arrays-and-strings",
  "estimatedMinutes": 45,
  "difficulty": "DEVELOPING",
  "prerequisites": [
    37,
    39,
    41,
    43,
    49
  ],
  "concepts": [
    "Pattern Hybridization",
    "Composite Data Pipelines",
    "Production Bounds"
  ],
  "practiceSkills": [
    "Array Capstone Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Synthesize prefix sums, two pointers, and interval merges to architect a calendar engine",
    "Optimize compound array queries meeting strict O(N) time constraints"
  ],
  "practiceArchetype": "milestone",
  "flowTier": "tier3"
,
  "steps": [
    {
        "id": "day50-step1",
        "stepNumber": 1,
        "title": "Section 4 Capstone: Linear Array Patterns: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Array Capstone",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Array Capstone.",
        "markdownContent": [
            "Section 4 Capstone integrates prefix sums, two pointers, sliding windows, and interval merges into a calendar booking management engine.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Array Capstone**, remember the central principle: Combining contiguous array techniques enables high-performance scheduling and analytical systems."
        ],
        "snippets": [
            {
                "title": "Array Capstone Implementation Template",
                "code": "# Boundary Event Scan-line for Max Concurrent Meetings\ndef max_concurrent(meetings):\n    events = []\n    for s, e in meetings:\n        events.append((s, 1))  # Start: +1 meeting\n        events.append((e, -1)) # End: -1 meeting\n    events.sort(key=lambda x: (x[0], x[1])) # If times match, end (-1) before start (+1)\n    curr = best = 0\n    for time, delta in events:\n        curr += delta\n        best = max(best, curr)\n    return best",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Combining contiguous array techniques enables high-performance scheduling and analytical systems."
    },
    {
        "id": "day50-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Array Capstone",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "The calendar engine accepts booking intervals [start, end), detects conflicts in O(log N) time, computes peak concurrent meetings using boundary event scan-lines, and answers range queries.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Combining contiguous array techniques enables high-performance scheduling and analytical systems.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Array Capstone Core Invariant",
                "content": "Combining contiguous array techniques enables high-performance scheduling and analytical systems."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Combining contiguous array techniques enables high-performance scheduling and analytical systems."
    },
    {
        "id": "day50-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Array Capstone",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d50-q1",
                "question": "In the boundary event scan-line algorithm, if a meeting ends at 10 and another starts at 10, how should events be sorted?",
                "options": [
                    {
                        "id": "A",
                        "label": "End event (-1) should be processed before start event (+1) if meetings touching at endpoints do not conflict"
                    },
                    {
                        "id": "B",
                        "label": "Start event (+1) must always precede end event"
                    },
                    {
                        "id": "C",
                        "label": "Order does not matter"
                    },
                    {
                        "id": "D",
                        "label": "Sort strictly by meeting duration"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! If interval [9, 10) and [10, 11) share endpoint 10, processing end (-1) first drops the room count before the new meeting (+1) claims it.",
                    "B": "Incorrect: Processing +1 first creates a false peak of 2 concurrent meetings at time 10.",
                    "C": "Incorrect: Tie-breaking order directly changes the computed peak.",
                    "D": "Incorrect: Time alignment requires sorting on timestamp."
                }
            },
            {
                "id": "chk-d50-q2",
                "question": "What is the time complexity of the boundary event scan-line algorithm for N meetings?",
                "options": [
                    {
                        "id": "A",
                        "label": "O(N log N) to sort 2N boundary events, followed by an O(N) sweep"
                    },
                    {
                        "id": "B",
                        "label": "O(N^2) pairwise comparisons"
                    },
                    {
                        "id": "C",
                        "label": "O(N) with no sorting required"
                    },
                    {
                        "id": "D",
                        "label": "O(1) auxiliary space"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Generating 2N event tuples and sorting them takes O(N log N) time; the single linear pass takes O(N). Total: O(N log N).",
                    "B": "Incorrect: The event scan-line avoids quadratic comparisons.",
                    "C": "Incorrect: Events must be ordered chronologically.",
                    "D": "Incorrect: The event list requires O(N) auxiliary space."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day50-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Array Capstone",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Architect a Meeting Room Scheduler computing maximum concurrent active meetings.",
        "subheading": "Implement and verify Array Capstone in the interactive workspace.",
        "task": {
            "title": "Architect a Meeting Room Scheduler computing maximum concurrent active meetings.",
            "instructions": [
                "Architect a Meeting Room Scheduler computing maximum concurrent active meetings.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "def min_meeting_rooms(intervals: list[list[int]]) -> int:\n    # TODO 1: Create events array with (start, 1) and (end, -1)\n    # TODO 2: Sort events by time; tie-break: end (-1) before start (1)\n    # TODO 3: Track running sum and find maximum concurrent rooms\n    return 0\n\nmeetings = [[0, 30], [5, 10], [15, 20]]\nprint('Min meeting rooms needed:', min_meeting_rooms(meetings))\n",
            "solutionCode": "def min_meeting_rooms(intervals: list[list[int]]) -> int:\n    events = []\n    for start, end in intervals:\n        events.append((start, 1))\n        events.append((end, -1))\n    events.sort(key=lambda x: (x[0], x[1]))\n    curr_rooms = 0\n    max_rooms = 0\n    for time, delta in events:\n        curr_rooms += delta\n        if curr_rooms > max_rooms:\n            max_rooms = curr_rooms\n    return max_rooms\n\nmeetings = [[0, 30], [5, 10], [15, 20]]\nprint('Min meeting rooms needed:', min_meeting_rooms(meetings))\n",
            "expectedOutputPatterns": [
                "Min meeting rooms needed: 2"
            ],
            "hint": "Append (s, 1) and (e, -1). Sort by lambda x: (x[0], x[1]). Accumulate delta and record maximum."
        },
        "keyTakeaway": "Successfully implemented and verified Array Capstone!"
    },
    {
        "id": "day50-step5",
        "stepNumber": 5,
        "title": "Day 50 Complete: Section 4 Capstone: Linear Array Patterns",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 50,
        "heading": "Mastery Achieved: Section 4 Capstone: Linear Array Patterns",
        "subheading": "You have solidified key mental models and techniques for Array Capstone.",
        "recapRows": [
            {
                "concept": "Boundary Scan-Line",
                "naiveIntuition": "Simulate every minute on a timeline",
                "pythonReality": "Discrete event scan-line only visits start and end timestamps in O(N log N), handling infinite time bounds"
            },
            {
                "concept": "Section 4 Synthesis",
                "naiveIntuition": "Array algorithms are independent tricks",
                "pythonReality": "Prefix sums, two pointers, sliding windows, and event sorting form an interconnected toolbox for contiguous data"
            }
        ],
        "solidifiedConcepts": [
            "Pattern Hybridization",
            "Composite Data Pipelines",
            "Production Bounds"
        ],
        "nextDayPreview": {
            "dayNumber": 51,
            "title": "Linear Search vs Binary Search Halving",
            "description": "Contrast linear search with binary search, proving O(log N) runtime through search-space halving."
        }
    }
]
},
  51: {
  "dayNumber": 51,
  "title": "Linear Search vs Binary Search Halving",
  "topicName": "Search Foundations",
  "sectionId": "searching-and-sorting",
  "estimatedMinutes": 30,
  "difficulty": "DEVELOPING",
  "prerequisites": [
    27,
    36
  ],
  "concepts": [
    "Linear Scan vs Logarithmic Halving",
    "Search Space Invariant"
  ],
  "practiceSkills": [
    "Search Foundations Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Trace binary search interval halving and logarithmic depth bounds",
    "Prove necessity of sorted order before applying binary search"
  ],
  "practiceArchetype": "tracing",
  "flowTier": "tier1"
,
  "steps": [
    {
        "id": "day51-step1",
        "stepNumber": 1,
        "title": "Linear Search vs Binary Search Halving: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Search Foundations",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Search Foundations.",
        "markdownContent": [
            "Linear search scans sequentially in O(N) time, whereas Binary Search halves the remaining search space on every comparison, achieving logarithmic O(log N) time.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Search Foundations**, remember the central principle: Logarithmic search halving requires sorted ordering and scales to billions of elements in under 35 comparisons."
        ],
        "snippets": [
            {
                "title": "Search Foundations Implementation Template",
                "code": "# Search space halving\n# For N = 1,000,000, log2(N) ~= 20 iterations max\nimport math\nprint('Max comparisons for 1M:', math.ceil(math.log2(1_000_000))) # 20",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Logarithmic search halving requires sorted ordering and scales to billions of elements in under 35 comparisons."
    },
    {
        "id": "day51-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Search Foundations",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "By testing the midpoint of a sorted array, we determine with certainty which half contains the target. The search space reduces as N, N/2, N/4, ... terminating in log2(N) steps.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Logarithmic search halving requires sorted ordering and scales to billions of elements in under 35 comparisons.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Search Foundations Core Invariant",
                "content": "Logarithmic search halving requires sorted ordering and scales to billions of elements in under 35 comparisons."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Logarithmic search halving requires sorted ordering and scales to billions of elements in under 35 comparisons."
    },
    {
        "id": "day51-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Search Foundations",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d51-q1",
                "question": "How many comparisons does binary search require in the worst case to search through 1,000,000 sorted elements?",
                "options": [
                    {
                        "id": "A",
                        "label": "Approximately 20 comparisons"
                    },
                    {
                        "id": "B",
                        "label": "Approximately 500,000 comparisons"
                    },
                    {
                        "id": "C",
                        "label": "Approximately 1,000 comparisons"
                    },
                    {
                        "id": "D",
                        "label": "Exactly 1,000,000 comparisons"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Since 2^20 = 1,048,576 > 1,000,000, halving the range 20 times reduces the search interval to a single element.",
                    "B": "Incorrect: That is average linear search, not binary search.",
                    "C": "Incorrect: 2^10 is 1024, not 1 million.",
                    "D": "Incorrect: That is worst-case linear search."
                }
            },
            {
                "id": "chk-d51-q2",
                "question": "Why does binary search fail if applied to an unsorted array?",
                "options": [
                    {
                        "id": "A",
                        "label": "Without monotonic ordering, comparing with mid does not guarantee that the target cannot reside in the discarded half"
                    },
                    {
                        "id": "B",
                        "label": "Because mid index computation requires sorted numbers"
                    },
                    {
                        "id": "C",
                        "label": "Python raises a TypeError on unsorted arrays"
                    },
                    {
                        "id": "D",
                        "label": "Because unsorted arrays cannot be 0-indexed"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Binary search relies entirely on the invariant that if target < arr[mid], the target CANNOT be in the right half. Without sorted order, this invariant is broken.",
                    "B": "Incorrect: Mid index arithmetic (L + R) // 2 works on any integer range.",
                    "C": "Incorrect: Python has no runtime sortedness check.",
                    "D": "Incorrect: All lists are 0-indexed."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day51-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Search Foundations",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Trace search space halving step-by-step and count total comparisons.",
        "subheading": "Implement and verify Search Foundations in the interactive workspace.",
        "task": {
            "title": "Trace search space halving step-by-step and count total comparisons.",
            "instructions": [
                "Trace search space halving step-by-step and count total comparisons.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "# Day 51 Tracing Practice: Search Space Halving\ndef trace_binary_search(arr: list[int], target: int) -> tuple[int, list[int]]:\n    left, right = 0, len(arr) - 1\n    visited_mids = []\n    found_idx = -1\n    # TODO: While left <= right, record mid element in visited_mids and halve range\n    \n    return found_idx, visited_mids\n\nnums = [2, 5, 8, 12, 16, 23, 38, 45, 56, 72, 91]\nidx, mids = trace_binary_search(nums, 72)\nprint('Found index:', idx)\nprint('Visited mid elements:', mids)\n",
            "solutionCode": "def trace_binary_search(arr: list[int], target: int) -> tuple[int, list[int]]:\n    left, right = 0, len(arr) - 1\n    visited_mids = []\n    found_idx = -1\n    while left <= right:\n        mid = left + (right - left) // 2\n        visited_mids.append(arr[mid])\n        if arr[mid] == target:\n            found_idx = mid\n            break\n        elif arr[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return found_idx, visited_mids\n\nnums = [2, 5, 8, 12, 16, 23, 38, 45, 56, 72, 91]\nidx, mids = trace_binary_search(nums, 72)\nprint('Found index:', idx)\nprint('Visited mid elements:', mids)\n",
            "expectedOutputPatterns": [
                "Found index: 9",
                "Visited mid elements: [23, 56, 72]"
            ],
            "hint": "mid = left + (right - left) // 2. Record arr[mid] into visited_mids, then update left = mid + 1 or right = mid - 1."
        },
        "keyTakeaway": "Successfully implemented and verified Search Foundations!"
    },
    {
        "id": "day51-step5",
        "stepNumber": 5,
        "title": "Day 51 Complete: Linear Search vs Binary Search Halving",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 51,
        "heading": "Mastery Achieved: Linear Search vs Binary Search Halving",
        "subheading": "You have solidified key mental models and techniques for Search Foundations.",
        "recapRows": [
            {
                "concept": "Halving Power",
                "naiveIntuition": "Searching large arrays takes seconds",
                "pythonReality": "Binary search finds any item in a billion sorted elements in ~30 operations"
            },
            {
                "concept": "Sorted Requirement",
                "naiveIntuition": "Binary search works on any collection",
                "pythonReality": "Requires strictly monotonic data; sorting first takes O(N log N)"
            }
        ],
        "solidifiedConcepts": [
            "Linear Scan vs Logarithmic Halving",
            "Search Space Invariant"
        ],
        "nextDayPreview": {
            "dayNumber": 52,
            "title": "Classical Binary Search & Boundary Indices",
            "description": "Master boundary conditions, lower and upper bounds, bisect semantics, and avoiding infinite loops in binary search."
        }
    }
]
},
  52: {
  "dayNumber": 52,
  "title": "Classical Binary Search & Boundary Indices",
  "topicName": "Binary Search Boundaries",
  "sectionId": "searching-and-sorting",
  "estimatedMinutes": 35,
  "difficulty": "DEVELOPING",
  "prerequisites": [
    51
  ],
  "concepts": [
    "Midpoint Calculation (L + (R-L)//2)",
    "Bisect Left & Right Boundaries"
  ],
  "practiceSkills": [
    "Binary Search Boundaries Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Prevent integer overflow bugs in midpoint computation",
    "Implement exact lower-bound and upper-bound binary searches (bisect_left / bisect_right)"
  ],
  "practiceArchetype": "completion",
  "flowTier": "tier2"
,
  "steps": [
    {
        "id": "day52-step1",
        "stepNumber": 1,
        "title": "Classical Binary Search & Boundary Indices: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Binary Search Boundaries",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Binary Search Boundaries.",
        "markdownContent": [
            "Boundary Binary Search locates insertion positions and duplicate boundaries (bisect_left vs bisect_right) by maintaining loop invariants across left <= right intervals.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Binary Search Boundaries**, remember the central principle: Lower bound (bisect_left) finds the first index >= target; upper bound (bisect_right) finds the first index > target."
        ],
        "snippets": [
            {
                "title": "Binary Search Boundaries Implementation Template",
                "code": "# Lower bound binary search\ndef lower_bound(arr, target):\n    L, R = 0, len(arr) - 1\n    ans = len(arr)\n    while L <= R:\n        mid = L + (R - L) // 2\n        if arr[mid] >= target:\n            ans = mid\n            R = mid - 1 # Keep searching left for earlier occurrence\n        else:\n            L = mid + 1\n    return ans",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Lower bound (bisect_left) finds the first index >= target; upper bound (bisect_right) finds the first index > target."
    },
    {
        "id": "day52-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Binary Search Boundaries",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "To find the first position >= target (bisect_left): if arr[mid] >= target, record candidate index and search left (right = mid - 1). Else search right (left = mid + 1).",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Lower bound (bisect_left) finds the first index >= target; upper bound (bisect_right) finds the first index > target.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Binary Search Boundaries Core Invariant",
                "content": "Lower bound (bisect_left) finds the first index >= target; upper bound (bisect_right) finds the first index > target."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Lower bound (bisect_left) finds the first index >= target; upper bound (bisect_right) finds the first index > target."
    },
    {
        "id": "day52-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Binary Search Boundaries",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d52-q1",
                "question": "In lower_bound binary search, why do we update `right = mid - 1` even when `arr[mid] == target`?",
                "options": [
                    {
                        "id": "A",
                        "label": "To continue searching the left sub-interval for potentially earlier duplicate occurrences of the target"
                    },
                    {
                        "id": "B",
                        "label": "Because mid cannot be the correct answer"
                    },
                    {
                        "id": "C",
                        "label": "To trigger the loop termination condition immediately"
                    },
                    {
                        "id": "D",
                        "label": "To prevent duplicate return values"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! When searching for the FIRST occurrence (lower bound), finding a match means mid is a candidate, but an earlier identical element might exist further left.",
                    "B": "Incorrect: mid is saved as the current best candidate before searching left.",
                    "C": "Incorrect: Loop termination occurs when L > R.",
                    "D": "Incorrect: Duplicate values are valid."
                }
            },
            {
                "id": "chk-d52-q2",
                "question": "Given arr = [1, 2, 4, 4, 4, 7, 9], what are the indices returned by bisect_left(arr, 4) and bisect_right(arr, 4)?",
                "options": [
                    {
                        "id": "A",
                        "label": "bisect_left returns 2, bisect_right returns 5"
                    },
                    {
                        "id": "B",
                        "label": "bisect_left returns 4, bisect_right returns 4"
                    },
                    {
                        "id": "C",
                        "label": "bisect_left returns 0, bisect_right returns 6"
                    },
                    {
                        "id": "D",
                        "label": "bisect_left returns 2, bisect_right returns 4"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! The first 4 is at index 2 (bisect_left). The first element strictly greater than 4 is 7 at index 5 (bisect_right).",
                    "B": "Incorrect: 4 is the target value, not the index.",
                    "C": "Incorrect: Indices are 2 and 5.",
                    "D": "Incorrect: Index 4 holds the last 4; bisect_right returns the insertion position after it (index 5)."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day52-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Binary Search Boundaries",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Complete lower bound binary search by writing the critical invariant condition.",
        "subheading": "Implement and verify Binary Search Boundaries in the interactive workspace.",
        "task": {
            "title": "Complete lower bound binary search by writing the critical invariant condition.",
            "instructions": [
                "Complete lower bound binary search by writing the critical invariant condition.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "def search_first_occurrence(nums: list[int], target: int) -> int:\n    left, right = 0, len(nums) - 1\n    first_idx = -1\n    while left <= right:\n        mid = left + (right - left) // 2\n        ### CRITICAL INVARIANT: YOUR CODE HERE ###\n        # If nums[mid] >= target, save mid if it equals target, and search left; else search right\n        pass\n    return first_idx\n\nnums = [1, 2, 3, 3, 3, 5, 6]\nprint('First occurrence of 3:', search_first_occurrence(nums, 3))\n",
            "solutionCode": "def search_first_occurrence(nums: list[int], target: int) -> int:\n    left, right = 0, len(nums) - 1\n    first_idx = -1\n    while left <= right:\n        mid = left + (right - left) // 2\n        if nums[mid] == target:\n            first_idx = mid\n            right = mid - 1\n        elif nums[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return first_idx\n\nnums = [1, 2, 3, 3, 3, 5, 6]\nprint('First occurrence of 3:', search_first_occurrence(nums, 3))\n",
            "expectedOutputPatterns": [
                "First occurrence of 3: 2"
            ],
            "hint": "If nums[mid] == target: save first_idx = mid and right = mid - 1. If nums[mid] < target: left = mid + 1. Else: right = mid - 1."
        },
        "keyTakeaway": "Successfully implemented and verified Binary Search Boundaries!"
    },
    {
        "id": "day52-step5",
        "stepNumber": 5,
        "title": "Day 52 Complete: Classical Binary Search & Boundary Indices",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 52,
        "heading": "Mastery Achieved: Classical Binary Search & Boundary Indices",
        "subheading": "You have solidified key mental models and techniques for Binary Search Boundaries.",
        "recapRows": [
            {
                "concept": "Midpoint Overflow",
                "naiveIntuition": "(L + R) // 2 is always safe",
                "pythonReality": "Python handles big ints, but L + (R - L) // 2 is standard across all languages to prevent 32-bit overflow"
            },
            {
                "concept": "Range Invariant",
                "naiveIntuition": "while left < right vs while left <= right",
                "pythonReality": "left <= right searches single-element intervals [i, i]; left < right requires careful boundary maintenance"
            }
        ],
        "solidifiedConcepts": [
            "Midpoint Calculation (L + (R-L)//2)",
            "Bisect Left & Right Boundaries"
        ],
        "nextDayPreview": {
            "dayNumber": 53,
            "title": "Binary Search on Monotonic Answer Space",
            "description": "Apply binary search to monotonic answer spaces to find optimal parameters meeting problem constraints."
        }
    }
]
},
  53: {
  "dayNumber": 53,
  "title": "Binary Search on Monotonic Answer Space",
  "topicName": "Answer Space Search",
  "sectionId": "searching-and-sorting",
  "estimatedMinutes": 40,
  "difficulty": "DEVELOPING",
  "prerequisites": [
    52
  ],
  "concepts": [
    "Monotonic Feasibility Predicate",
    "Answer Space Search Invariant"
  ],
  "practiceSkills": [
    "Answer Space Search Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Map optimization problems to monotonic boolean check functions",
    "Solve Capacity to Ship Packages and Koko Eating Bananas in O(N log(Range)) time"
  ],
  "practiceArchetype": "problem",
  "flowTier": "tier2"
,
  "steps": [
    {
        "id": "day53-step1",
        "stepNumber": 1,
        "title": "Binary Search on Monotonic Answer Space: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Answer Space Search",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Answer Space Search.",
        "markdownContent": [
            "Binary Search on Answer Space solves optimization problems by binary searching over candidate answers, using a monotonic boolean check function to find minimum or maximum feasible values.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Answer Space Search**, remember the central principle: Map optimization problems ('minimum speed/capacity') to monotonic boolean check predicates and binary search the answer range."
        ],
        "snippets": [
            {
                "title": "Answer Space Search Implementation Template",
                "code": "# Binary search on answer space: Koko eating bananas\n# Range: low = 1, high = max(piles)\n# if can_eat_in_time(speed): high = mid - 1",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Map optimization problems ('minimum speed/capacity') to monotonic boolean check predicates and binary search the answer range."
    },
    {
        "id": "day53-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Answer Space Search",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "If a capacity of C is feasible, all capacities > C are also feasible (monotonicity). Search range [min_val, max_val]; if check(mid) is True, record mid and search smaller: R = mid - 1.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Map optimization problems ('minimum speed/capacity') to monotonic boolean check predicates and binary search the answer range.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Answer Space Search Core Invariant",
                "content": "Map optimization problems ('minimum speed/capacity') to monotonic boolean check predicates and binary search the answer range."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Map optimization problems ('minimum speed/capacity') to monotonic boolean check predicates and binary search the answer range."
    },
    {
        "id": "day53-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Answer Space Search",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d53-q1",
                "question": "What mathematical property must an optimization problem satisfy to be solvable via Binary Search on Answer Space?",
                "options": [
                    {
                        "id": "A",
                        "label": "Monotonicity: if answer X is feasible, all answers in one direction must also be feasible"
                    },
                    {
                        "id": "B",
                        "label": "The input array must be sorted in ascending order"
                    },
                    {
                        "id": "C",
                        "label": "The number of items must be a power of two"
                    },
                    {
                        "id": "D",
                        "label": "The check function must run in O(1) time"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Monotonicity (e.g. FFFTTT or TTTFFF) ensures that a single midpoint evaluation eliminates half of the candidate answer space with certainty.",
                    "B": "Incorrect: The input data does not need to be sorted; only the answer range [low..high] is sorted.",
                    "C": "Incorrect: Binary search operates over any integer interval.",
                    "D": "Incorrect: Check functions typically run in O(N) time."
                }
            },
            {
                "id": "chk-d53-q2",
                "question": "What is the total time complexity of Binary Search on Answer Space with range [1..M] and an O(N) feasibility check?",
                "options": [
                    {
                        "id": "A",
                        "label": "O(N log M)"
                    },
                    {
                        "id": "B",
                        "label": "O(N * M)"
                    },
                    {
                        "id": "C",
                        "label": "O(M log N)"
                    },
                    {
                        "id": "D",
                        "label": "O(log(N * M))"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! There are log2(M) iterations of binary search, and each iteration invokes the O(N) check function. Total: O(N log M).",
                    "B": "Incorrect: Linear search over answers is O(N * M), but binary search optimizes it to O(N log M).",
                    "C": "Incorrect: Logarithm applies to answer space M.",
                    "D": "Incorrect: Time is multiplicative, not logarithmic in both."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day53-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Answer Space Search",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Solve Capacity to Ship Packages Within D Days using monotonic answer search.",
        "subheading": "Implement and verify Answer Space Search in the interactive workspace.",
        "task": {
            "title": "Solve Capacity to Ship Packages Within D Days using monotonic answer search.",
            "instructions": [
                "Solve Capacity to Ship Packages Within D Days using monotonic answer search.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "def ship_within_days(weights: list[int], days: int) -> int:\n    def feasible(capacity: int) -> bool:\n        # TODO 1: Return True if weights can be shipped within 'days' at given capacity\n        return True\n    \n    left = max(weights)\n    right = sum(weights)\n    ans = right\n    # TODO 2: Binary search capacity range [left, right] to find minimum feasible capacity\n    return ans\n\nweights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]\nprint('Minimum capacity:', ship_within_days(weights, 5))\n",
            "solutionCode": "def ship_within_days(weights: list[int], days: int) -> int:\n    def feasible(capacity: int) -> bool:\n        d = 1\n        curr = 0\n        for w in weights:\n            if curr + w > capacity:\n                d += 1\n                curr = w\n            else:\n                curr += w\n        return d <= days\n    left = max(weights)\n    right = sum(weights)\n    ans = right\n    while left <= right:\n        mid = left + (right - left) // 2\n        if feasible(mid):\n            ans = mid\n            right = mid - 1\n        else:\n            left = mid + 1\n    return ans\n\nweights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]\nprint('Minimum capacity:', ship_within_days(weights, 5))\n",
            "expectedOutputPatterns": [
                "Minimum capacity: 15"
            ],
            "hint": "Check function accumulates weights into days: when curr + w > capacity, day_count += 1 and curr = w. If day_count <= days: ans = mid and right = mid - 1."
        },
        "keyTakeaway": "Successfully implemented and verified Answer Space Search!"
    },
    {
        "id": "day53-step5",
        "stepNumber": 5,
        "title": "Day 53 Complete: Binary Search on Monotonic Answer Space",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 53,
        "heading": "Mastery Achieved: Binary Search on Monotonic Answer Space",
        "subheading": "You have solidified key mental models and techniques for Answer Space Search.",
        "recapRows": [
            {
                "concept": "Input vs Answer",
                "naiveIntuition": "Binary search searches arrays of numbers",
                "pythonReality": "Binary search can search abstract ranges of potential answers (capacities, speeds, thresholds)"
            },
            {
                "concept": "Search Bounds",
                "naiveIntuition": "low = 0, high = infinity",
                "pythonReality": "Tight bounds matter: minimum capacity is max(weights); maximum capacity is sum(weights)"
            }
        ],
        "solidifiedConcepts": [
            "Monotonic Feasibility Predicate",
            "Answer Space Search Invariant"
        ],
        "nextDayPreview": {
            "dayNumber": 54,
            "title": "Rotated Sorted Arrays & Peak Finding",
            "description": "Find elements in rotated sorted arrays and locate local peaks using modified binary search predicates."
        }
    }
]
},
  54: {
  "dayNumber": 54,
  "title": "Rotated Sorted Arrays & Peak Finding",
  "topicName": "Rotated Search",
  "sectionId": "searching-and-sorting",
  "estimatedMinutes": 35,
  "difficulty": "DEVELOPING",
  "prerequisites": [
    52
  ],
  "concepts": [
    "Sorted Half Identification",
    "Inflection Point Invariants"
  ],
  "practiceSkills": [
    "Rotated Search Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Determine which half of a rotated sorted array is monotonically ordered",
    "Locate target elements and inflection minimums in O(log N) time"
  ],
  "practiceArchetype": "debugging",
  "flowTier": "tier2"
,
  "steps": [
    {
        "id": "day54-step1",
        "stepNumber": 1,
        "title": "Rotated Sorted Arrays & Peak Finding: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Rotated Search",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Rotated Search.",
        "markdownContent": [
            "Rotated Sorted Arrays contain an inflection point (pivot) dividing the array into two sorted segments, searchable in O(log N) time by identifying which half is sorted.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Rotated Search**, remember the central principle: At least one half of a rotated sorted array is always normally sorted; determine which half is sorted and test if target falls within its bounds."
        ],
        "snippets": [
            {
                "title": "Rotated Search Implementation Template",
                "code": "# Search in Rotated Sorted Array\ndef search_rotated(nums, target):\n    L, R = 0, len(nums) - 1\n    while L <= R:\n        mid = L + (R - L) // 2\n        if nums[mid] == target: return mid\n        if nums[L] <= nums[mid]: # Left sorted\n            if nums[L] <= target < nums[mid]: R = mid - 1\n            else: L = mid + 1\n        else: # Right sorted\n            if nums[mid] < target <= nums[R]: L = mid + 1\n            else: R = mid - 1\n    return -1",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "At least one half of a rotated sorted array is always normally sorted; determine which half is sorted and test if target falls within its bounds."
    },
    {
        "id": "day54-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Rotated Search",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Compare arr[L] with arr[mid]. If arr[L] <= arr[mid], the left half is normally sorted: test if target lies within [arr[L], arr[mid]]; if so R = mid - 1, else L = mid + 1. Otherwise the right half is sorted.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: At least one half of a rotated sorted array is always normally sorted; determine which half is sorted and test if target falls within its bounds.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Rotated Search Core Invariant",
                "content": "At least one half of a rotated sorted array is always normally sorted; determine which half is sorted and test if target falls within its bounds."
            }
        ],
        "keyTakeaway": "Operational invariant locked: At least one half of a rotated sorted array is always normally sorted; determine which half is sorted and test if target falls within its bounds."
    },
    {
        "id": "day54-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Rotated Search",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d54-q1",
                "question": "In a rotated sorted array without duplicates, what property is guaranteed for any midpoint index?",
                "options": [
                    {
                        "id": "A",
                        "label": "At least one half (either [L..mid] or [mid..R]) is guaranteed to be strictly sorted in ascending order"
                    },
                    {
                        "id": "B",
                        "label": "The midpoint is always the pivot element"
                    },
                    {
                        "id": "C",
                        "label": "Both halves are always rotated"
                    },
                    {
                        "id": "D",
                        "label": "The array cannot be searched in O(log N) time"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Because a single rotation creates at most one inflection point, that point can reside in at most one half. The other half is guaranteed to be normally sorted.",
                    "B": "Incorrect: The pivot can be anywhere.",
                    "C": "Incorrect: Only one half contains the rotation boundary.",
                    "D": "Incorrect: O(log N) search is fully achievable."
                }
            },
            {
                "id": "chk-d54-q2",
                "question": "If `nums[L] <= nums[mid]`, how do we test if `target` resides in the left half?",
                "options": [
                    {
                        "id": "A",
                        "label": "nums[L] <= target < nums[mid]"
                    },
                    {
                        "id": "B",
                        "label": "target > nums[mid]"
                    },
                    {
                        "id": "C",
                        "label": "target <= nums[L]"
                    },
                    {
                        "id": "D",
                        "label": "nums[L] < nums[mid]"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Since the left half is sorted, target is in [L..mid) if and only if it is >= nums[L] and < nums[mid].",
                    "B": "Incorrect: target > nums[mid] lies outside the left half.",
                    "C": "Incorrect: target could be smaller than all elements in that half.",
                    "D": "Incorrect: This checks array elements, not the target."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day54-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Rotated Search",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Debug search logic in rotated sorted arrays.",
        "subheading": "Implement and verify Rotated Search in the interactive workspace.",
        "task": {
            "title": "Debug search logic in rotated sorted arrays.",
            "instructions": [
                "Debug search logic in rotated sorted arrays.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "# Day 54 Debugging Challenge: Rotated Array Search\n# BUG REPORT: This code fails to find target in rotated arrays because the right-half condition is inverted!\ndef search_rotated_buggy(nums: list[int], target: int) -> int:\n    left, right = 0, len(nums) - 1\n    while left <= right:\n        mid = left + (right - left) // 2\n        if nums[mid] == target:\n            return mid\n        if nums[left] <= nums[mid]:\n            if nums[left] <= target < nums[mid]:\n                right = mid - 1\n            else:\n                left = mid + 1\n        else:\n            # BUG: Inverted condition here\n            if nums[mid] <= target < nums[right]:\n                left = mid + 1\n            else:\n                right = mid - 1\n    return -1\n\n# INSTRUCTION: Fix the boundary check for the right-sorted half.\nnums = [4, 5, 6, 7, 0, 1, 2]\nprint('Index of 0:', search_rotated_buggy(nums, 0))\n",
            "solutionCode": "def search_rotated_buggy(nums: list[int], target: int) -> int:\n    left, right = 0, len(nums) - 1\n    while left <= right:\n        mid = left + (right - left) // 2\n        if nums[mid] == target:\n            return mid\n        if nums[left] <= nums[mid]:\n            if nums[left] <= target < nums[mid]:\n                right = mid - 1\n            else:\n                left = mid + 1\n        else:\n            if nums[mid] < target <= nums[right]:\n                left = mid + 1\n            else:\n                right = mid - 1\n    return -1\n\nnums = [4, 5, 6, 7, 0, 1, 2]\nprint('Index of 0:', search_rotated_buggy(nums, 0))\n",
            "expectedOutputPatterns": [
                "Index of 0: 4"
            ],
            "hint": "Change `if nums[mid] <= target < nums[right]:` to `if nums[mid] < target <= nums[right]:`."
        },
        "keyTakeaway": "Successfully implemented and verified Rotated Search!"
    },
    {
        "id": "day54-step5",
        "stepNumber": 5,
        "title": "Day 54 Complete: Rotated Sorted Arrays & Peak Finding",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 54,
        "heading": "Mastery Achieved: Rotated Sorted Arrays & Peak Finding",
        "subheading": "You have solidified key mental models and techniques for Rotated Search.",
        "recapRows": [
            {
                "concept": "Sorted Half Determination",
                "naiveIntuition": "Find the rotation pivot first",
                "pythonReality": "Comparing nums[L] <= nums[mid] directly identifies the sorted half without finding the pivot"
            },
            {
                "concept": "Inclusive Right Bound",
                "naiveIntuition": "target < nums[right]",
                "pythonReality": "target <= nums[right] is required to include the element at index right"
            }
        ],
        "solidifiedConcepts": [
            "Sorted Half Identification",
            "Inflection Point Invariants"
        ],
        "nextDayPreview": {
            "dayNumber": 55,
            "title": "Quadratic Sorts: Bubble, Selection, Insertion",
            "description": "Analyze Bubble, Selection, and Insertion Sort, proving O(N^2) bounds and stability trade-offs."
        }
    }
]
},
  55: {
  "dayNumber": 55,
  "title": "Quadratic Sorts: Bubble, Selection, Insertion",
  "topicName": "Quadratic Sorts",
  "sectionId": "searching-and-sorting",
  "estimatedMinutes": 30,
  "difficulty": "DEVELOPING",
  "prerequisites": [
    34,
    36
  ],
  "concepts": [
    "Insertion Sort Invariant",
    "Stability in Sorting Algorithms"
  ],
  "practiceSkills": [
    "Quadratic Sorts Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Explain why insertion sort achieves linear O(N) performance on nearly-sorted data",
    "Debug sorting stability violations where equal keys are unintentionally swapped"
  ],
  "practiceArchetype": "debugging",
  "flowTier": "tier1"
,
  "steps": [
    {
        "id": "day55-step1",
        "stepNumber": 1,
        "title": "Quadratic Sorts: Bubble, Selection, Insertion: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Quadratic Sorts",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Quadratic Sorts.",
        "markdownContent": [
            "Quadratic Sorts (Bubble, Selection, Insertion) have O(N^2) worst-case time, but Insertion Sort achieves linear O(N) best-case time on nearly-sorted data and maintains stability.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Quadratic Sorts**, remember the central principle: Insertion Sort is the premier O(N) sort for small or nearly-sorted arrays and forms the base engine of Timsort."
        ],
        "snippets": [
            {
                "title": "Quadratic Sorts Implementation Template",
                "code": "# Insertion Sort\ndef insertion_sort(arr):\n    for i in range(1, len(arr)):\n        key = arr[i]\n        j = i - 1\n        while j >= 0 and arr[j] > key:\n            arr[j + 1] = arr[j]\n            j -= 1\n        arr[j + 1] = key\n    return arr",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Insertion Sort is the premier O(N) sort for small or nearly-sorted arrays and forms the base engine of Timsort."
    },
    {
        "id": "day55-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Quadratic Sorts",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Insertion sort shifts elements greater than key one position right, placing key in its sorted spot. Stability means equal elements maintain their relative initial order.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Insertion Sort is the premier O(N) sort for small or nearly-sorted arrays and forms the base engine of Timsort.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Quadratic Sorts Core Invariant",
                "content": "Insertion Sort is the premier O(N) sort for small or nearly-sorted arrays and forms the base engine of Timsort."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Insertion Sort is the premier O(N) sort for small or nearly-sorted arrays and forms the base engine of Timsort."
    },
    {
        "id": "day55-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Quadratic Sorts",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d55-q1",
                "question": "Why is Insertion Sort adaptive, achieving O(N) time on already sorted arrays?",
                "options": [
                    {
                        "id": "A",
                        "label": "The inner while loop terminates on the very first comparison (arr[j] > key is False), executing only 1 comparison per element"
                    },
                    {
                        "id": "B",
                        "label": "It uses binary search to insert items"
                    },
                    {
                        "id": "C",
                        "label": "It divides the array in half recursively"
                    },
                    {
                        "id": "D",
                        "label": "It builds a heap of elements"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! If the array is sorted, each element key is already >= arr[i-1], so the inner loop never shifts any elements, running N-1 comparisons total.",
                    "B": "Incorrect: Standard insertion sort shifts linearly; binary insertion sort still requires O(N) shifts.",
                    "C": "Incorrect: Insertion sort is an iterative incremental algorithm.",
                    "D": "Incorrect: Heaps are used in HeapSort."
                }
            },
            {
                "id": "chk-d55-q2",
                "question": "What makes a sorting algorithm 'stable'?",
                "options": [
                    {
                        "id": "A",
                        "label": "Equal keys preserve their relative input order in the sorted output"
                    },
                    {
                        "id": "B",
                        "label": "The algorithm never crashes with stack overflow"
                    },
                    {
                        "id": "C",
                        "label": "The runtime is guaranteed to be O(N log N)"
                    },
                    {
                        "id": "D",
                        "label": "The memory usage does not exceed O(1)"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Stability ensures that if item A appears before item B with identical keys, A is guaranteed to appear before B in the sorted result.",
                    "B": "Incorrect: Stability relates to element ordering, not call stack safety.",
                    "C": "Incorrect: Quadratic sorts can be stable; unstable sorts like QuickSort can be O(N log N).",
                    "D": "Incorrect: Space efficiency is orthogonal to stability."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day55-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Quadratic Sorts",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Debug an insertion sort implementation that violates stability.",
        "subheading": "Implement and verify Quadratic Sorts in the interactive workspace.",
        "task": {
            "title": "Debug an insertion sort implementation that violates stability.",
            "instructions": [
                "Debug an insertion sort implementation that violates stability.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "# Day 55 Debugging Challenge: Sorting Stability\n# BUG REPORT: This insertion sort violates stability because `>=` causes equal elements to swap places!\ndef unstable_insertion_sort(items: list[tuple[int, str]]) -> list[tuple[int, str]]:\n    arr = list(items)\n    for i in range(1, len(arr)):\n        key = arr[i]\n        j = i - 1\n        # BUG: Using `>=` shifts equal elements, destroying stable input order!\n        while j >= 0 and arr[j][0] >= key[0]:\n            arr[j + 1] = arr[j]\n            j -= 1\n        arr[j + 1] = key\n    return arr\n\n# INSTRUCTION: Fix the comparison to strictly `>` to restore stability.\ndata = [(2, 'first'), (1, 'only'), (2, 'second')]\nprint('Stable sorted:', unstable_insertion_sort(data))\n",
            "solutionCode": "def unstable_insertion_sort(items: list[tuple[int, str]]) -> list[tuple[int, str]]:\n    arr = list(items)\n    for i in range(1, len(arr)):\n        key = arr[i]\n        j = i - 1\n        while j >= 0 and arr[j][0] > key[0]:\n            arr[j + 1] = arr[j]\n            j -= 1\n        arr[j + 1] = key\n    return arr\n\ndata = [(2, 'first'), (1, 'only'), (2, 'second')]\nprint('Stable sorted:', unstable_insertion_sort(data))\n",
            "expectedOutputPatterns": [
                "Stable sorted: [(1, 'only'), (2, 'first'), (2, 'second')]"
            ],
            "hint": "Change `arr[j][0] >= key[0]` to `arr[j][0] > key[0]` so equal elements stop shifting."
        },
        "keyTakeaway": "Successfully implemented and verified Quadratic Sorts!"
    },
    {
        "id": "day55-step5",
        "stepNumber": 5,
        "title": "Day 55 Complete: Quadratic Sorts: Bubble, Selection, Insertion",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 55,
        "heading": "Mastery Achieved: Quadratic Sorts: Bubble, Selection, Insertion",
        "subheading": "You have solidified key mental models and techniques for Quadratic Sorts.",
        "recapRows": [
            {
                "concept": "Strict Greater-Than",
                "naiveIntuition": ">= and > produce identical sorted lists",
                "pythonReality": ">= shifts equal elements, reversing their original order and breaking sorting stability"
            },
            {
                "concept": "Adaptive Complexity",
                "naiveIntuition": "All O(N^2) sorts perform equally on sorted data",
                "pythonReality": "Selection Sort always takes O(N^2); Insertion Sort adapts to O(N) on sorted inputs"
            }
        ],
        "solidifiedConcepts": [
            "Insertion Sort Invariant",
            "Stability in Sorting Algorithms"
        ],
        "nextDayPreview": {
            "dayNumber": 56,
            "title": "Merge Sort: Divide, Conquer, Combine",
            "description": "Implement Merge Sort recursively, trace recursion trees, and prove the O(N log N) stable sorting guarantee."
        }
    }
]
},
  56: {
  "dayNumber": 56,
  "title": "Merge Sort: Divide, Conquer, Combine",
  "topicName": "Merge Sort",
  "sectionId": "searching-and-sorting",
  "estimatedMinutes": 45,
  "difficulty": "DEVELOPING",
  "prerequisites": [
    31,
    33,
    55
  ],
  "concepts": [
    "Divide & Conquer Merge Step",
    "Stable O(N log N) Guarantee"
  ],
  "practiceSkills": [
    "Merge Sort Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Implement recursive Merge Sort with linear merge combination passes",
    "Analyze O(N log N) time and O(N) auxiliary space requirements"
  ],
  "practiceArchetype": "algorithm",
  "flowTier": "tier3"
,
  "steps": [
    {
        "id": "day56-step1",
        "stepNumber": 1,
        "title": "Merge Sort: Divide, Conquer, Combine: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Merge Sort",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Merge Sort.",
        "markdownContent": [
            "Merge Sort is a Divide-and-Conquer algorithm guaranteeing O(N log N) time and stability by recursively halving arrays and merging sorted subarrays.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Merge Sort**, remember the central principle: Merge Sort guarantees predictable O(N log N) worst-case time and stability, trading O(N) auxiliary space."
        ],
        "snippets": [
            {
                "title": "Merge Sort Implementation Template",
                "code": "# Merge Sort\ndef merge_sort(arr):\n    if len(arr) <= 1: return arr\n    mid = len(arr) // 2\n    L = merge_sort(arr[:mid])\n    R = merge_sort(arr[mid:])\n    res = []\n    i = j = 0\n    while i < len(L) and j < len(R):\n        if L[i] <= R[j]: res.append(L[i]); i += 1\n        else: res.append(R[j]); j += 1\n    res.extend(L[i:]); res.extend(R[j:])\n    return res",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Merge Sort guarantees predictable O(N log N) worst-case time and stability, trading O(N) auxiliary space."
    },
    {
        "id": "day56-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Merge Sort",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Base case: len <= 1. Divide: mid = len // 2. Recursively sort left and right halves. Combine: two-pointer merge into an auxiliary list in O(N) time.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Merge Sort guarantees predictable O(N log N) worst-case time and stability, trading O(N) auxiliary space.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Merge Sort Core Invariant",
                "content": "Merge Sort guarantees predictable O(N log N) worst-case time and stability, trading O(N) auxiliary space."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Merge Sort guarantees predictable O(N log N) worst-case time and stability, trading O(N) auxiliary space."
    },
    {
        "id": "day56-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Merge Sort",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d56-q1",
                "question": "Why does Merge Sort require O(N) auxiliary space in standard implementations?",
                "options": [
                    {
                        "id": "A",
                        "label": "Merging two sorted subarrays requires an auxiliary buffer to store combined elements without overwriting unvisited items"
                    },
                    {
                        "id": "B",
                        "label": "Because the recursion stack depth is O(N)"
                    },
                    {
                        "id": "C",
                        "label": "Python creates a new process for each recursive call"
                    },
                    {
                        "id": "D",
                        "label": "Because mid index computation allocates memory"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! During the merge phase, elements must be written into a separate buffer to avoid overwriting elements that have not yet been compared.",
                    "B": "Incorrect: The recursion stack depth is logarithmic O(log N).",
                    "C": "Incorrect: Python uses standard thread stack frames.",
                    "D": "Incorrect: Integer arithmetic requires no heap allocations."
                }
            },
            {
                "id": "chk-d56-q2",
                "question": "What line in the Merge Sort merge phase guarantees that the sort remains STABLE?",
                "options": [
                    {
                        "id": "A",
                        "label": "if L[i] <= R[j]: selecting left element on equality"
                    },
                    {
                        "id": "B",
                        "label": "mid = len(arr) // 2"
                    },
                    {
                        "id": "C",
                        "label": "if len(arr) <= 1: return arr"
                    },
                    {
                        "id": "D",
                        "label": "res.extend(R[j:])"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! By choosing L[i] when L[i] == R[j], elements from the left subarray (which originally appeared earlier in the input) are placed first, preserving relative order.",
                    "B": "Incorrect: Midpoint division does not handle value comparison.",
                    "C": "Incorrect: This is the base case.",
                    "D": "Incorrect: This appends remaining right elements."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day56-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Merge Sort",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Implement full recursive Merge Sort with linear two-pointer merge.",
        "subheading": "Implement and verify Merge Sort in the interactive workspace.",
        "task": {
            "title": "Implement full recursive Merge Sort with linear two-pointer merge.",
            "instructions": [
                "Implement full recursive Merge Sort with linear two-pointer merge.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "def merge_sort(arr: list[int]) -> list[int]:\n    # TODO 1: Base case (len <= 1)\n    # TODO 2: Split into left and right, recurse\n    # TODO 3: Merge sorted halves using two pointers\n    return arr\n\nnums = [38, 27, 43, 3, 9, 82, 10]\nprint('Sorted:', merge_sort(nums))\n",
            "solutionCode": "def merge_sort(arr: list[int]) -> list[int]:\n    if len(arr) <= 1:\n        return arr\n    mid = len(arr) // 2\n    left = merge_sort(arr[:mid])\n    right = merge_sort(arr[mid:])\n    res = []\n    i = j = 0\n    while i < len(left) and j < len(right):\n        if left[i] <= right[j]:\n            res.append(left[i])\n            i += 1\n        else:\n            res.append(right[j])\n            j += 1\n    res.extend(left[i:])\n    res.extend(right[j:])\n    return res\n\nnums = [38, 27, 43, 3, 9, 82, 10]\nprint('Sorted:', merge_sort(nums))\n",
            "expectedOutputPatterns": [
                "Sorted: [3, 9, 10, 27, 38, 43, 82]"
            ],
            "hint": "Base case len(arr) <= 1. Recursively sort left = arr[:mid] and right = arr[mid:]. Merge with two pointers while i < len(left) and j < len(right)."
        },
        "keyTakeaway": "Successfully implemented and verified Merge Sort!"
    },
    {
        "id": "day56-step5",
        "stepNumber": 5,
        "title": "Day 56 Complete: Merge Sort: Divide, Conquer, Combine",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 56,
        "heading": "Mastery Achieved: Merge Sort: Divide, Conquer, Combine",
        "subheading": "You have solidified key mental models and techniques for Merge Sort.",
        "recapRows": [
            {
                "concept": "Guaranteed Bound",
                "naiveIntuition": "QuickSort is always faster than MergeSort",
                "pythonReality": "MergeSort guarantees O(N log N) worst-case without degenerate pivot pitfalls"
            },
            {
                "concept": "Space Penalty",
                "naiveIntuition": "MergeSort operates in O(1) space",
                "pythonReality": "Merging requires O(N) auxiliary space; in-place array merge sort is inefficient in practice"
            }
        ],
        "solidifiedConcepts": [
            "Divide & Conquer Merge Step",
            "Stable O(N log N) Guarantee"
        ],
        "nextDayPreview": {
            "dayNumber": 57,
            "title": "Quick Sort & Hoare Partitioning",
            "description": "Implement Quick Sort, master Lomuto and Hoare partitioning, analyze expected O(N log N) time, and avoid worst-case pivots."
        }
    }
]
},
  57: {
  "dayNumber": 57,
  "title": "Quick Sort & Hoare Partitioning",
  "topicName": "Quick Sort",
  "sectionId": "searching-and-sorting",
  "estimatedMinutes": 45,
  "difficulty": "DEVELOPING",
  "prerequisites": [
    31,
    56
  ],
  "concepts": [
    "Hoare vs Lomuto Partitioning",
    "Pivot Selection & O(N^2) Degeneracy"
  ],
  "practiceSkills": [
    "Quick Sort Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Implement in-place Hoare partition scheme with median-of-three pivot selection",
    "Explain worst-case O(N^2) degradation on sorted inputs and randomization fixes"
  ],
  "practiceArchetype": "algorithm",
  "flowTier": "tier3"
,
  "steps": [
    {
        "id": "day57-step1",
        "stepNumber": 1,
        "title": "Quick Sort & Hoare Partitioning: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Quick Sort",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Quick Sort.",
        "markdownContent": [
            "Quick Sort is an in-place divide-and-conquer algorithm that selects a pivot, partitions the array around it, and recurses on sub-arrays, achieving O(N log N) expected time and O(log N) stack space.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Quick Sort**, remember the central principle: Quick Sort achieves superior cache performance due to in-place swaps, with expected O(N log N) runtime."
        ],
        "snippets": [
            {
                "title": "Quick Sort Implementation Template",
                "code": "# In-place Quick Sort with Hoare Partition\ndef quick_sort(arr, low, high):\n    if low < high:\n        p = partition(arr, low, high)\n        quick_sort(arr, low, p)\n        quick_sort(arr, p + 1, high)",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Quick Sort achieves superior cache performance due to in-place swaps, with expected O(N log N) runtime."
    },
    {
        "id": "day57-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Quick Sort",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Hoare partitioning uses two pointers converging from both ends, swapping elements on wrong sides of the pivot. Median-of-three pivot selection prevents O(N^2) sorted-input degradation.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Quick Sort achieves superior cache performance due to in-place swaps, with expected O(N log N) runtime.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Quick Sort Core Invariant",
                "content": "Quick Sort achieves superior cache performance due to in-place swaps, with expected O(N log N) runtime."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Quick Sort achieves superior cache performance due to in-place swaps, with expected O(N log N) runtime."
    },
    {
        "id": "day57-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Quick Sort",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d57-q1",
                "question": "What causes Quick Sort to degrade to worst-case O(N^2) time complexity?",
                "options": [
                    {
                        "id": "A",
                        "label": "Consistently choosing the minimum or maximum element as pivot, creating unbalanced partitions of sizes 1 and N-1"
                    },
                    {
                        "id": "B",
                        "label": "Using an in-place partition scheme"
                    },
                    {
                        "id": "C",
                        "label": "Sorting arrays containing negative numbers"
                    },
                    {
                        "id": "D",
                        "label": "Using Hoare partitioning instead of Lomuto"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! When partitions split into 0 and N-1 items on every step, the recurrence becomes T(N) = T(N-1) + O(N) = O(N^2).",
                    "B": "Incorrect: In-place partitioning is standard and efficient.",
                    "C": "Incorrect: Numbers' signs do not affect partitioning.",
                    "D": "Incorrect: Both schemes suffer O(N^2) under poor pivots; Hoare does fewer swaps."
                }
            },
            {
                "id": "chk-d57-q2",
                "question": "Why does Python's standard library use Timsort instead of pure Quick Sort?",
                "options": [
                    {
                        "id": "A",
                        "label": "Timsort guarantees O(N log N) worst case and is strictly STABLE, whereas Quick Sort is unstable and can degrade to O(N^2)"
                    },
                    {
                        "id": "B",
                        "label": "Quick Sort cannot sort strings in Python"
                    },
                    {
                        "id": "C",
                        "label": "Quick Sort requires O(N) auxiliary memory"
                    },
                    {
                        "id": "D",
                        "label": "Timsort runs in O(1) space"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Real-world software demands stability (preserving input order for multi-key sorting) and worst-case performance guarantees that Quick Sort cannot provide.",
                    "B": "Incorrect: Quick Sort sorts any comparable type.",
                    "C": "Incorrect: Quick Sort uses O(log N) stack space.",
                    "D": "Incorrect: Timsort uses O(N) auxiliary space for run merging."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day57-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Quick Sort",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Implement in-place Quick Sort using Lomuto partitioning.",
        "subheading": "Implement and verify Quick Sort in the interactive workspace.",
        "task": {
            "title": "Implement in-place Quick Sort using Lomuto partitioning.",
            "instructions": [
                "Implement in-place Quick Sort using Lomuto partitioning.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "def quick_sort(arr: list[int], low: int, high: int) -> None:\n    def partition(l: int, h: int) -> int:\n        pivot = arr[h]\n        i = l\n        # TODO 1: Partition elements < pivot to the left using pointer i\n        # TODO 2: Place pivot at index i and return i\n        return i\n\n    # TODO 3: If low < high, partition and recurse on left and right sub-arrays\n    pass\n\nnums = [10, 7, 8, 9, 1, 5]\nquick_sort(nums, 0, len(nums) - 1)\nprint('Quick sorted:', nums)\n",
            "solutionCode": "def quick_sort(arr: list[int], low: int, high: int) -> None:\n    def partition(l: int, h: int) -> int:\n        pivot = arr[h]\n        i = l\n        for j in range(l, h):\n            if arr[j] < pivot:\n                arr[i], arr[j] = arr[j], arr[i]\n                i += 1\n        arr[i], arr[h] = arr[h], arr[i]\n        return i\n    if low < high:\n        pi = partition(low, high)\n        quick_sort(arr, low, pi - 1)\n        quick_sort(arr, pi + 1, high)\n\nnums = [10, 7, 8, 9, 1, 5]\nquick_sort(nums, 0, len(nums) - 1)\nprint('Quick sorted:', nums)\n",
            "expectedOutputPatterns": [
                "Quick sorted: [1, 5, 7, 8, 9, 10]"
            ],
            "hint": "Loop j from l to h-1: if arr[j] < pivot: swap arr[i], arr[j] and i += 1. Swap arr[i], arr[h] and recurse on (low, pi-1) and (pi+1, high)."
        },
        "keyTakeaway": "Successfully implemented and verified Quick Sort!"
    },
    {
        "id": "day57-step5",
        "stepNumber": 5,
        "title": "Day 57 Complete: Quick Sort & Hoare Partitioning",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 57,
        "heading": "Mastery Achieved: Quick Sort & Hoare Partitioning",
        "subheading": "You have solidified key mental models and techniques for Quick Sort.",
        "recapRows": [
            {
                "concept": "In-Place Swaps",
                "naiveIntuition": "List comprehension quicksort [x for x in arr if x < p] is standard",
                "pythonReality": "Comprehension quicksort allocates new lists on every level O(N log N space); true quicksort operates in-place"
            },
            {
                "concept": "Pivot Choice",
                "naiveIntuition": "Always pick arr[0]",
                "pythonReality": "Picking arr[0] on sorted arrays triggers O(N^2) quadratic disaster; use randomized or median-of-three pivots"
            }
        ],
        "solidifiedConcepts": [
            "Hoare vs Lomuto Partitioning",
            "Pivot Selection & O(N^2) Degeneracy"
        ],
        "nextDayPreview": {
            "dayNumber": 58,
            "title": "Quickselect: Expected O(N) Kth Order",
            "description": "Use Quickselect to find the Kth smallest or largest element in expected O(N) time without full sorting."
        }
    }
]
},
  58: {
  "dayNumber": 58,
  "title": "Quickselect: Expected O(N) Kth Order",
  "topicName": "Order Statistics",
  "sectionId": "searching-and-sorting",
  "estimatedMinutes": 35,
  "difficulty": "DEVELOPING",
  "prerequisites": [
    57
  ],
  "concepts": [
    "Single-Sided Partition Discarding",
    "Expected O(N) Recurrence"
  ],
  "practiceSkills": [
    "Order Statistics Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Discard non-promising partitions to locate the Kth largest element in expected O(N) time",
    "Prove the geometric series convergence T(N) = N + N/2 + N/4 = 2N"
  ],
  "practiceArchetype": "completion",
  "flowTier": "tier2"
,
  "steps": [
    {
        "id": "day58-step1",
        "stepNumber": 1,
        "title": "Quickselect: Expected O(N) Kth Order: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Order Statistics",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Order Statistics.",
        "markdownContent": [
            "Quickselect finds the Kth smallest (or largest) element in an unsorted array in expected O(N) time by recursing only into the partition containing K, discarding the other half.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Order Statistics**, remember the central principle: Quickselect achieves linear O(N) expected time for order statistics by pruning half the problem space at each step."
        ],
        "snippets": [
            {
                "title": "Order Statistics Implementation Template",
                "code": "# Quickselect expected O(N)\ndef quickselect(nums, k):\n    p = partition(nums)\n    if p == k: return nums[p]\n    elif k < p: return quickselect(left, k)\n    else: return quickselect(right, k)",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Quickselect achieves linear O(N) expected time for order statistics by pruning half the problem space at each step."
    },
    {
        "id": "day58-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Order Statistics",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "After partitioning around pivot index P: if P == k, return arr[P]. If k < P, recurse left (low..P-1). If k > P, recurse right (P+1..high). Recurrence: T(N) = T(N/2) + O(N) = O(N).",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Quickselect achieves linear O(N) expected time for order statistics by pruning half the problem space at each step.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Order Statistics Core Invariant",
                "content": "Quickselect achieves linear O(N) expected time for order statistics by pruning half the problem space at each step."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Quickselect achieves linear O(N) expected time for order statistics by pruning half the problem space at each step."
    },
    {
        "id": "day58-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Order Statistics",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d58-q1",
                "question": "Why is Quickselect's expected time complexity O(N) while Quick Sort is O(N log N)?",
                "options": [
                    {
                        "id": "A",
                        "label": "Quickselect recurses into only ONE partition, creating a geometric series N + N/2 + N/4 + ... = 2N = O(N)"
                    },
                    {
                        "id": "B",
                        "label": "Quickselect does not use partitioning"
                    },
                    {
                        "id": "C",
                        "label": "Quickselect sorts the array using counting sort first"
                    },
                    {
                        "id": "D",
                        "label": "Because K is always smaller than log N"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Quick Sort recurses into BOTH sub-arrays (work per level = N, log N levels = N log N). Quickselect discards one half at each step (N + N/2 + N/4 + ... = 2N = O(N)).",
                    "B": "Incorrect: Quickselect uses the exact same partition function as Quick Sort.",
                    "C": "Incorrect: No preliminary sorting is performed.",
                    "D": "Incorrect: K can be any index from 0 to N-1."
                }
            },
            {
                "id": "chk-d58-q2",
                "question": "To find the Kth LARGEST element in an array of length N, what 0-indexed order statistic index do we target in Quickselect?",
                "options": [
                    {
                        "id": "A",
                        "label": "N - K"
                    },
                    {
                        "id": "B",
                        "label": "K - 1"
                    },
                    {
                        "id": "C",
                        "label": "K"
                    },
                    {
                        "id": "D",
                        "label": "N // K"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! In an ascending sorted array of size N, the 1st largest is at index N-1, the 2nd largest at N-2, and the Kth largest at N - K.",
                    "B": "Incorrect: K - 1 is the Kth smallest element.",
                    "C": "Incorrect: Off-by-one error.",
                    "D": "Incorrect: Division is unrelated to rank ordering."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day58-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Order Statistics",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Complete Quickselect by filling in the single-sided branch selection invariant.",
        "subheading": "Implement and verify Order Statistics in the interactive workspace.",
        "task": {
            "title": "Complete Quickselect by filling in the single-sided branch selection invariant.",
            "instructions": [
                "Complete Quickselect by filling in the single-sided branch selection invariant.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "def find_kth_largest(nums: list[int], k: int) -> int:\n    target_idx = len(nums) - k\n    def select(l: int, r: int) -> int:\n        pivot = nums[r]\n        i = l\n        for j in range(l, r):\n            if nums[j] <= pivot:\n                nums[i], nums[j] = nums[j], nums[i]\n                i += 1\n        nums[i], nums[r] = nums[r], nums[i]\n        ### CRITICAL INVARIANT: YOUR CODE HERE ###\n        # If i == target_idx, return nums[i]\n        # Else recurse left if target_idx < i, or right if target_idx > i\n        return -1\n    return select(0, len(nums) - 1)\n\nnums = [3, 2, 1, 5, 6, 4]\nprint('2nd largest element:', find_kth_largest(nums, 2))\n",
            "solutionCode": "def find_kth_largest(nums: list[int], k: int) -> int:\n    target_idx = len(nums) - k\n    def select(l: int, r: int) -> int:\n        pivot = nums[r]\n        i = l\n        for j in range(l, r):\n            if nums[j] <= pivot:\n                nums[i], nums[j] = nums[j], nums[i]\n                i += 1\n        nums[i], nums[r] = nums[r], nums[i]\n        if i == target_idx:\n            return nums[i]\n        elif target_idx < i:\n            return select(l, i - 1)\n        else:\n            return select(i + 1, r)\n    return select(0, len(nums) - 1)\n\nnums = [3, 2, 1, 5, 6, 4]\nprint('2nd largest element:', find_kth_largest(nums, 2))\n",
            "expectedOutputPatterns": [
                "2nd largest element: 5"
            ],
            "hint": "Check `if i == target_idx: return nums[i]`. If `target_idx < i`: `return select(l, i - 1)`. Else: `return select(i + 1, r)`."
        },
        "keyTakeaway": "Successfully implemented and verified Order Statistics!"
    },
    {
        "id": "day58-step5",
        "stepNumber": 5,
        "title": "Day 58 Complete: Quickselect: Expected O(N) Kth Order",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 58,
        "heading": "Mastery Achieved: Quickselect: Expected O(N) Kth Order",
        "subheading": "You have solidified key mental models and techniques for Order Statistics.",
        "recapRows": [
            {
                "concept": "Pruning Half the Work",
                "naiveIntuition": "Finding Kth element requires full O(N log N) sort",
                "pythonReality": "Discarding the non-promising partition achieves linear O(N) expected time"
            },
            {
                "concept": "In-Place Reordering",
                "naiveIntuition": "Quickselect preserves original array order",
                "pythonReality": "Quickselect mutates array elements around pivots in-place"
            }
        ],
        "solidifiedConcepts": [
            "Single-Sided Partition Discarding",
            "Expected O(N) Recurrence"
        ],
        "nextDayPreview": {
            "dayNumber": 59,
            "title": "Counting Sort & Non-Comparison Bounds",
            "description": "Break the Omega(N log N) comparison barrier with stable Counting Sort over bounded integer ranges."
        }
    }
]
},
  59: {
  "dayNumber": 59,
  "title": "Counting Sort & Non-Comparison Bounds",
  "topicName": "Counting Sort",
  "sectionId": "searching-and-sorting",
  "estimatedMinutes": 35,
  "difficulty": "DEVELOPING",
  "prerequisites": [
    36,
    56
  ],
  "concepts": [
    "Non-Comparison Sorting Invariant",
    "Cumulative Frequency Offsets"
  ],
  "practiceSkills": [
    "Counting Sort Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Bypass the Omega(N log N) comparison sort lower bound using frequency arrays",
    "Implement stable Counting Sort in O(N + K) time and O(K) space"
  ],
  "practiceArchetype": "algorithm",
  "flowTier": "tier2"
,
  "steps": [
    {
        "id": "day59-step1",
        "stepNumber": 1,
        "title": "Counting Sort & Non-Comparison Bounds: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Counting Sort",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Counting Sort.",
        "markdownContent": [
            "Counting Sort is a non-comparison integer sorting algorithm running in linear O(N + K) time by tallying element frequencies and computing cumulative placement offsets.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Counting Sort**, remember the central principle: Counting Sort breaks the Omega(N log N) comparison barrier, running in O(N + K) time when key range K is bounded."
        ],
        "snippets": [
            {
                "title": "Counting Sort Implementation Template",
                "code": "# Stable Counting Sort over range [0..K]\ndef counting_sort(arr, K):\n    count = [0] * (K + 1)\n    for x in arr: count[x] += 1\n    for i in range(1, K + 1): count[i] += count[i - 1]\n    res = [0] * len(arr)\n    for x in reversed(arr):\n        res[count[x] - 1] = x\n        count[x] -= 1\n    return res",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Counting Sort breaks the Omega(N log N) comparison barrier, running in O(N + K) time when key range K is bounded."
    },
    {
        "id": "day59-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Counting Sort",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Count occurrences of each integer in range [0..K]. Compute prefix sums of counts: count[i] indicates the number of elements <= i. Place elements in reverse to ensure stability.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Counting Sort breaks the Omega(N log N) comparison barrier, running in O(N + K) time when key range K is bounded.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Counting Sort Core Invariant",
                "content": "Counting Sort breaks the Omega(N log N) comparison barrier, running in O(N + K) time when key range K is bounded."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Counting Sort breaks the Omega(N log N) comparison barrier, running in O(N + K) time when key range K is bounded."
    },
    {
        "id": "day59-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Counting Sort",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d59-q1",
                "question": "Why is the comparison sorting lower bound Omega(N log N) not applicable to Counting Sort?",
                "options": [
                    {
                        "id": "A",
                        "label": "Counting Sort does not compare elements against each other; it uses integer values directly as array memory indices"
                    },
                    {
                        "id": "B",
                        "label": "Because Counting Sort runs in O(1) space"
                    },
                    {
                        "id": "C",
                        "label": "Because Python optimizes count arrays using C code"
                    },
                    {
                        "id": "D",
                        "label": "Counting Sort only works on arrays of length <= 100"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! The Omega(N log N) lower bound is proven via decision trees for comparison-based sorts. Non-comparison sorts bypass decision trees by using direct memory addressing.",
                    "B": "Incorrect: Counting Sort requires O(N + K) auxiliary space.",
                    "C": "Incorrect: Algorithmic complexity is independent of language implementation.",
                    "D": "Incorrect: It scales to arbitrary N as long as range K is reasonable."
                }
            },
            {
                "id": "chk-d59-q2",
                "question": "When does Counting Sort become an INEFFICIENT choice?",
                "options": [
                    {
                        "id": "A",
                        "label": "When the range of values K is significantly larger than the number of elements N (e.g. K = 10^9 and N = 10)"
                    },
                    {
                        "id": "B",
                        "label": "When all numbers are positive"
                    },
                    {
                        "id": "C",
                        "label": "When the array contains duplicate elements"
                    },
                    {
                        "id": "D",
                        "label": "When N > 1,000"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Space and time are O(N + K). If K = 10^9, allocating a count array of 1 billion slots for 10 elements wastes massive time and gigabytes of RAM.",
                    "B": "Incorrect: Positive numbers are ideal for 0-indexed counting.",
                    "C": "Incorrect: Counting Sort excels at duplicate keys.",
                    "D": "Incorrect: Counting Sort handles millions of elements effortlessly if K is bounded."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day59-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Counting Sort",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Implement stable Counting Sort for bounded non-negative integers.",
        "subheading": "Implement and verify Counting Sort in the interactive workspace.",
        "task": {
            "title": "Implement stable Counting Sort for bounded non-negative integers.",
            "instructions": [
                "Implement stable Counting Sort for bounded non-negative integers.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "def counting_sort(arr: list[int]) -> list[int]:\n    if not arr:\n        return []\n    # TODO 1: Find max value K and build count frequency array\n    # TODO 2: Accumulate prefix sums in count array\n    # TODO 3: Iterate arr in reverse and place elements into output array\n    return []\n\nnums = [4, 2, 2, 8, 3, 3, 1]\nprint('Counting sorted:', counting_sort(nums))\n",
            "solutionCode": "def counting_sort(arr: list[int]) -> list[int]:\n    if not arr:\n        return []\n    max_val = max(arr)\n    count = [0] * (max_val + 1)\n    for x in arr:\n        count[x] += 1\n    for i in range(1, len(count)):\n        count[i] += count[i - 1]\n    res = [0] * len(arr)\n    for x in reversed(arr):\n        res[count[x] - 1] = x\n        count[x] -= 1\n    return res\n\nnums = [4, 2, 2, 8, 3, 3, 1]\nprint('Counting sorted:', counting_sort(nums))\n",
            "expectedOutputPatterns": [
                "Counting sorted: [1, 2, 2, 3, 3, 4, 8]"
            ],
            "hint": "count = [0] * (max(arr) + 1). Accumulate count[i] += count[i-1]. Traverse reversed(arr) placing res[count[x] - 1] = x and decrementing count[x]."
        },
        "keyTakeaway": "Successfully implemented and verified Counting Sort!"
    },
    {
        "id": "day59-step5",
        "stepNumber": 5,
        "title": "Day 59 Complete: Counting Sort & Non-Comparison Bounds",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 59,
        "heading": "Mastery Achieved: Counting Sort & Non-Comparison Bounds",
        "subheading": "You have solidified key mental models and techniques for Counting Sort.",
        "recapRows": [
            {
                "concept": "Non-Comparison Indexing",
                "naiveIntuition": "Sorting requires pairwise comparisons",
                "pythonReality": "Using integer values directly as array indices bypasses the comparison bound entirely"
            },
            {
                "concept": "Reverse Placement Stability",
                "naiveIntuition": "Forward placement is fine",
                "pythonReality": "Traversing input in reverse places identical keys from the back forward, preserving original relative order"
            }
        ],
        "solidifiedConcepts": [
            "Non-Comparison Sorting Invariant",
            "Cumulative Frequency Offsets"
        ],
        "nextDayPreview": {
            "dayNumber": 60,
            "title": "Radix Sort & Bucket Sort",
            "description": "Implement Radix Sort and Bucket Sort for linear-time sorting of fixed-width integers and uniform numbers."
        }
    }
]
},
  60: {
  "dayNumber": 60,
  "title": "Radix Sort & Bucket Sort",
  "topicName": "Distribution Sorts",
  "sectionId": "searching-and-sorting",
  "estimatedMinutes": 40,
  "difficulty": "DEVELOPING",
  "prerequisites": [
    59
  ],
  "concepts": [
    "LSD vs MSD Radix Passes",
    "Bucket Sort Distribution"
  ],
  "practiceSkills": [
    "Distribution Sorts Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Implement Least Significant Digit (LSD) Radix Sort across fixed integer representations",
    "Distribute uniform floating-point keys into buckets in O(N) average time"
  ],
  "practiceArchetype": "algorithm",
  "flowTier": "tier3"
,
  "steps": [
    {
        "id": "day60-step1",
        "stepNumber": 1,
        "title": "Radix Sort & Bucket Sort: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Distribution Sorts",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Distribution Sorts.",
        "markdownContent": [
            "Radix Sort processes integer keys digit-by-digit using stable Counting Sort subroutines, while Bucket Sort distributes uniformly distributed keys into buckets for O(N) sorting.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Distribution Sorts**, remember the central principle: Radix Sort sorts N fixed-width integers in O(D * (N + B)) time where D is digit count and B is base."
        ],
        "snippets": [
            {
                "title": "Distribution Sorts Implementation Template",
                "code": "# LSD Radix Sort digit pass\ndef radix_sort(arr):\n    max_val = max(arr)\n    exp = 1\n    while max_val // exp > 0:\n        counting_sort_by_digit(arr, exp)\n        exp *= 10",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Radix Sort sorts N fixed-width integers in O(D * (N + B)) time where D is digit count and B is base."
    },
    {
        "id": "day60-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Distribution Sorts",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "LSD Radix Sort sorts by least significant digit first (1s place, 10s place, 100s place). Because sub-sorts are stable, higher-order passes preserve the sorted order of lower digits.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Radix Sort sorts N fixed-width integers in O(D * (N + B)) time where D is digit count and B is base.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Distribution Sorts Core Invariant",
                "content": "Radix Sort sorts N fixed-width integers in O(D * (N + B)) time where D is digit count and B is base."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Radix Sort sorts N fixed-width integers in O(D * (N + B)) time where D is digit count and B is base."
    },
    {
        "id": "day60-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Distribution Sorts",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d60-q1",
                "question": "Why MUST the digit sub-sorting algorithm in Radix Sort be STABLE?",
                "options": [
                    {
                        "id": "A",
                        "label": "To preserve the sorted order established by earlier (less significant) digit passes when sorting higher digits"
                    },
                    {
                        "id": "B",
                        "label": "To prevent integers from exceeding 32-bit width"
                    },
                    {
                        "id": "C",
                        "label": "Because unstable algorithms cannot sort base-10 numbers"
                    },
                    {
                        "id": "D",
                        "label": "To reduce space complexity to O(1)"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! If two numbers have the same tens digit (e.g. 23 and 27), stability ensures that 23 remains before 27 because the units pass previously sorted them as 3 < 7.",
                    "B": "Incorrect: Bit width is unaffected.",
                    "C": "Incorrect: Stability is an ordering property, not a radix base constraint.",
                    "D": "Incorrect: Radix sort requires auxiliary memory for buckets."
                }
            },
            {
                "id": "chk-d60-q2",
                "question": "What is the time complexity of sorting N numbers with maximum D digits in base 10 using Radix Sort?",
                "options": [
                    {
                        "id": "A",
                        "label": "O(D * (N + 10))"
                    },
                    {
                        "id": "B",
                        "label": "O(N log N)"
                    },
                    {
                        "id": "C",
                        "label": "O(N^D)"
                    },
                    {
                        "id": "D",
                        "label": "O(10^D)"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! There are D passes, and each counting sort pass over base-10 digits takes O(N + 10) time. Total: O(D * (N + 10)).",
                    "B": "Incorrect: Radix Sort is non-comparison and does not depend on log N.",
                    "C": "Incorrect: The relationship is multiplicative, not exponential in N.",
                    "D": "Incorrect: Does not scale with 10^D."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day60-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Distribution Sorts",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Implement LSD Radix Sort for non-negative integers.",
        "subheading": "Implement and verify Distribution Sorts in the interactive workspace.",
        "task": {
            "title": "Implement LSD Radix Sort for non-negative integers.",
            "instructions": [
                "Implement LSD Radix Sort for non-negative integers.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "def radix_sort(arr: list[int]) -> list[int]:\n    if not arr:\n        return []\n    # TODO: Perform LSD Radix sort using digit extraction (exp = 1, 10, 100, ...)\n    return arr\n\nnums = [170, 45, 75, 90, 802, 24, 2, 66]\nprint('Radix sorted:', radix_sort(nums))\n",
            "solutionCode": "def radix_sort(arr: list[int]) -> list[int]:\n    if not arr:\n        return []\n    max_val = max(arr)\n    exp = 1\n    while max_val // exp > 0:\n        output = [0] * len(arr)\n        count = [0] * 10\n        for x in arr:\n            digit = (x // exp) % 10\n            count[digit] += 1\n        for i in range(1, 10):\n            count[i] += count[i - 1]\n        for x in reversed(arr):\n            digit = (x // exp) % 10\n            output[count[digit] - 1] = x\n            count[digit] -= 1\n        arr = output\n        exp *= 10\n    return arr\n\nnums = [170, 45, 75, 90, 802, 24, 2, 66]\nprint('Radix sorted:', radix_sort(nums))\n",
            "expectedOutputPatterns": [
                "Radix sorted: [2, 24, 45, 66, 75, 90, 170, 802]"
            ],
            "hint": "Extract digit = (x // exp) % 10. Perform stable counting sort into output, replace arr = output, and multiply exp *= 10 while max_val // exp > 0."
        },
        "keyTakeaway": "Successfully implemented and verified Distribution Sorts!"
    },
    {
        "id": "day60-step5",
        "stepNumber": 5,
        "title": "Day 60 Complete: Radix Sort & Bucket Sort",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 60,
        "heading": "Mastery Achieved: Radix Sort & Bucket Sort",
        "subheading": "You have solidified key mental models and techniques for Distribution Sorts.",
        "recapRows": [
            {
                "concept": "LSD vs MSD",
                "naiveIntuition": "Sort by highest digit first",
                "pythonReality": "LSD (Least Significant Digit) allows simple iterative passes; MSD requires recursive bucket partitioning"
            },
            {
                "concept": "Base Selection",
                "naiveIntuition": "Must always use base 10",
                "pythonReality": "In systems programming, Radix sort uses base 256 (byte-by-byte) or base 65536 to sort binary keys in fast bit shifts"
            }
        ],
        "solidifiedConcepts": [
            "LSD vs MSD Radix Passes",
            "Bucket Sort Distribution"
        ],
        "nextDayPreview": {
            "dayNumber": 61,
            "title": "Python's Timsort Architecture",
            "description": "Examine Python's built-in Timsort algorithm, minruns, run merging invariants, and galloping mode."
        }
    }
]
},
};
