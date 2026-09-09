import { DailyLessonPackage } from "../types";

export const BATCH_4_LESSONS: Record<number, DailyLessonPackage> = {
  61: {
  "dayNumber": 61,
  "title": "Python's Timsort Architecture",
  "topicName": "Timsort Architecture",
  "sectionId": "searching-and-sorting",
  "estimatedMinutes": 35,
  "difficulty": "DEVELOPING",
  "prerequisites": [
    56,
    60
  ],
  "concepts": [
    "Natural Runs & Galloping Mode",
    "Minrun Computation & Stack Balance"
  ],
  "practiceSkills": [
    "Timsort Architecture Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Trace natural ascending and descending run identification in Python's list.sort()",
    "Explain binary insertion sort integration on sub-arrays under minrun thresholds"
  ],
  "practiceArchetype": "tracing",
  "flowTier": "tier2"
,
  "steps": [
    {
        "id": "day61-step1",
        "stepNumber": 1,
        "title": "Python's Timsort Architecture: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Timsort Architecture",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Timsort Architecture.",
        "markdownContent": [
            "Timsort is Python's standard sorting algorithm, combining adaptive mergesort with binary insertion sort on small natural runs (minrun 32 to 64).",
            "### Foundational Mental Model\nWhen approaching problems requiring **Timsort Architecture**, remember the central principle: Timsort achieves linear O(N) best-case time on real-world partially sorted data and guarantees O(N log N) worst-case time with stability."
        ],
        "snippets": [
            {
                "title": "Timsort Architecture Implementation Template",
                "code": "# Timsort in Python standard library\narr = [5, 1, 4, 2, 8]\narr.sort() # Invokes CPython Timsort\nprint(arr) # [1, 2, 4, 5, 8]",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Timsort achieves linear O(N) best-case time on real-world partially sorted data and guarantees O(N log N) worst-case time with stability."
    },
    {
        "id": "day61-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Timsort Architecture",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Timsort scans for natural ascending (a <= b) or strictly descending (a > b) runs. Descending runs are reversed in O(N). Small runs are extended with binary insertion sort to reach minrun. Balanced runs are merged using a stack.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Timsort achieves linear O(N) best-case time on real-world partially sorted data and guarantees O(N log N) worst-case time with stability.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Timsort Architecture Core Invariant",
                "content": "Timsort achieves linear O(N) best-case time on real-world partially sorted data and guarantees O(N log N) worst-case time with stability."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Timsort achieves linear O(N) best-case time on real-world partially sorted data and guarantees O(N log N) worst-case time with stability."
    },
    {
        "id": "day61-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Timsort Architecture",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d61-q1",
                "question": "What is the best-case time complexity of Python's Timsort on already sorted data?",
                "options": [
                    {
                        "id": "A",
                        "label": "O(N)"
                    },
                    {
                        "id": "B",
                        "label": "O(N log N)"
                    },
                    {
                        "id": "C",
                        "label": "O(log N)"
                    },
                    {
                        "id": "D",
                        "label": "O(N^2)"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Timsort identifies the entire array as a single natural ascending run in a single linear pass of N-1 comparisons.",
                    "B": "Incorrect: That is Timsort's worst-case guarantee.",
                    "C": "Incorrect: Must inspect all N elements.",
                    "D": "Incorrect: Timsort strictly prevents quadratic behavior."
                }
            },
            {
                "id": "chk-d61-q2",
                "question": "What is the purpose of 'minrun' in Timsort?",
                "options": [
                    {
                        "id": "A",
                        "label": "To balance the merge stack by ensuring small runs are extended using binary insertion sort, keeping the total number of runs close to a power of 2"
                    },
                    {
                        "id": "B",
                        "label": "To set the maximum recursion limit"
                    },
                    {
                        "id": "C",
                        "label": "To limit the maximum array size Python can sort"
                    },
                    {
                        "id": "D",
                        "label": "To prevent sorting strings"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! A minrun between 32 and 64 ensures that small sub-arrays are sorted quickly with low overhead, and the number of runs remaining to merge is balanced.",
                    "B": "Incorrect: Timsort is iterative and uses an explicit stack.",
                    "C": "Incorrect: Timsort sorts arrays of arbitrary lengths.",
                    "D": "Incorrect: Timsort sorts any comparable objects."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day61-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Timsort Architecture",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Trace natural run identification in Timsort.",
        "subheading": "Implement and verify Timsort Architecture in the interactive workspace.",
        "task": {
            "title": "Trace natural run identification in Timsort.",
            "instructions": [
                "Trace natural run identification in Timsort.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "# Day 61 Tracing: Timsort Natural Run Detection\ndef identify_runs(arr: list[int]) -> list[list[int]]:\n    # TODO: Scan array, group consecutive ascending or strictly descending elements into runs\n    # Reverse any descending runs so all runs are ascending\n    runs = []\n    return runs\n\nnums = [1, 2, 3, 10, 8, 4, 7, 9]\nprint('Identified runs:', identify_runs(nums))\n",
            "solutionCode": "def identify_runs(arr: list[int]) -> list[list[int]]:\n    if not arr:\n        return []\n    runs = []\n    n = len(arr)\n    i = 0\n    while i < n:\n        start = i\n        if i == n - 1:\n            runs.append([arr[start]])\n            break\n        if arr[i + 1] >= arr[i]:\n            while i + 1 < n and arr[i + 1] >= arr[i]:\n                i += 1\n            runs.append(arr[start:i + 1])\n        else:\n            while i + 1 < n and arr[i + 1] < arr[i]:\n                i += 1\n            run = arr[start:i + 1]\n            run.reverse()\n            runs.append(run)\n        i += 1\n    return runs\n\nnums = [1, 2, 3, 10, 8, 4, 7, 9]\nprint('Identified runs:', identify_runs(nums))\n",
            "expectedOutputPatterns": [
                "Identified runs: [[1, 2, 3], [4, 8, 10], [7, 9]]"
            ],
            "hint": "Check if next element is >= current (ascending) or < (descending). Slice run, reverse descending runs, and append."
        },
        "keyTakeaway": "Successfully implemented and verified Timsort Architecture!"
    },
    {
        "id": "day61-step5",
        "stepNumber": 5,
        "title": "Day 61 Complete: Python's Timsort Architecture",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 61,
        "heading": "Mastery Achieved: Python's Timsort Architecture",
        "subheading": "You have solidified key mental models and techniques for Timsort Architecture.",
        "recapRows": [
            {
                "concept": "Real-World Data Exploitation",
                "naiveIntuition": "Data is randomly shuffled",
                "pythonReality": "Real datasets contain long streaks of sorted items; Timsort exploits natural runs to achieve near-linear time"
            },
            {
                "concept": "Galloping Mode",
                "naiveIntuition": "Merge always steps one by one",
                "pythonReality": "When one run wins repeatedly, Timsort switches to galloping mode (binary search) to skip blocks of elements"
            }
        ],
        "solidifiedConcepts": [
            "Natural Runs & Galloping Mode",
            "Minrun Computation & Stack Balance"
        ],
        "nextDayPreview": {
            "dayNumber": 62,
            "title": "Custom Comparators & Multi-Key Sorting",
            "description": "Master Python's key parameter in sorted(), multi-level tuple keys, and functools.cmp_to_key."
        }
    }
]
},
  62: {
  "dayNumber": 62,
  "title": "Custom Comparators & Multi-Key Sorting",
  "topicName": "Custom Sorting",
  "sectionId": "searching-and-sorting",
  "estimatedMinutes": 30,
  "difficulty": "DEVELOPING",
  "prerequisites": [
    22,
    25,
    61
  ],
  "concepts": [
    "key Function Lambdas",
    "Multi-Attribute Tuple Keys"
  ],
  "practiceSkills": [
    "Custom Sorting Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Construct complex multi-key sorting pipelines using tuple keys and reverse flags",
    "Bridge legacy three-way comparators using functools.cmp_to_key"
  ],
  "practiceArchetype": "completion",
  "flowTier": "tier1"
,
  "steps": [
    {
        "id": "day62-step1",
        "stepNumber": 1,
        "title": "Custom Comparators & Multi-Key Sorting: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Custom Sorting",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Custom Sorting.",
        "markdownContent": [
            "Custom Comparators and Multi-Key Sorting use key functions, lambdas, and tuple comparisons to sort complex heterogeneous records by primary, secondary, and reverse attributes.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Custom Sorting**, remember the central principle: Tuples provide elegant multi-attribute sorting keys; negating numeric terms reverses direction for specific columns."
        ],
        "snippets": [
            {
                "title": "Custom Sorting Implementation Template",
                "code": "# Multi-key sorting: sort by grade asc, score desc\nstudents = [('Alice', 'B', 85), ('Bob', 'A', 92), ('Charlie', 'B', 95)]\nstudents.sort(key=lambda s: (s[1], -s[2]))\n# Bob (A, 92), Charlie (B, 95), Alice (B, 85)",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Tuples provide elegant multi-attribute sorting keys; negating numeric terms reverses direction for specific columns."
    },
    {
        "id": "day62-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Custom Sorting",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Python compares tuples element by element: (a1, b1) < (a2, b2) checks a1 < a2; if equal, checks b1 < b2. To sort primary ascending and secondary descending: key = lambda x: (x.age, -x.score).",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Tuples provide elegant multi-attribute sorting keys; negating numeric terms reverses direction for specific columns.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Custom Sorting Core Invariant",
                "content": "Tuples provide elegant multi-attribute sorting keys; negating numeric terms reverses direction for specific columns."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Tuples provide elegant multi-attribute sorting keys; negating numeric terms reverses direction for specific columns."
    },
    {
        "id": "day62-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Custom Sorting",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d62-q1",
                "question": "How do you sort students by grade ascending, and for students with the same grade, by score descending?",
                "options": [
                    {
                        "id": "A",
                        "label": "key=lambda s: (s.grade, -s.score)"
                    },
                    {
                        "id": "B",
                        "label": "key=lambda s: (s.grade, s.score), reverse=True"
                    },
                    {
                        "id": "C",
                        "label": "key=lambda s: s.grade - s.score"
                    },
                    {
                        "id": "D",
                        "label": "key=lambda s: (-s.grade, s.score)"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! The first tuple element s.grade sorts ascending. Negating -s.score causes higher scores to become smaller numbers, sorting descending.",
                    "B": "Incorrect: reverse=True would flip both grade and score to descending.",
                    "C": "Incorrect: You cannot subtract integers from string grades.",
                    "D": "Incorrect: Strings cannot be negated with unary minus."
                }
            },
            {
                "id": "chk-d62-q2",
                "question": "What does functools.cmp_to_key do in Python 3?",
                "options": [
                    {
                        "id": "A",
                        "label": "Converts a legacy three-way comparison function (returning -1, 0, 1) into a key function suitable for sorted()"
                    },
                    {
                        "id": "B",
                        "label": "Converts keys to dictionary hash values"
                    },
                    {
                        "id": "C",
                        "label": "Encrypts sorting keys for security"
                    },
                    {
                        "id": "D",
                        "label": "Sorts keys in O(1) time"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Python 3 eliminated the `cmp` argument in favor of `key`. `cmp_to_key` wraps legacy comparator functions into a class implementing dunder comparison methods.",
                    "B": "Incorrect: It wraps comparators into key classes.",
                    "C": "Incorrect: No encryption is performed.",
                    "D": "Incorrect: Sorting complexity remains O(N log N)."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day62-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Custom Sorting",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Sort items using multi-key tuple lambdas.",
        "subheading": "Implement and verify Custom Sorting in the interactive workspace.",
        "task": {
            "title": "Sort items using multi-key tuple lambdas.",
            "instructions": [
                "Sort items using multi-key tuple lambdas.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "# Day 62 Practice: Multi-Key Log Sorting\nlogs = [\n    ('user1', 200, 15),\n    ('user2', 500, 8),\n    ('user3', 200, 42),\n    ('user4', 500, 20)\n]\n# TODO: Sort logs by status_code ascending, and tie-break by duration descending\nsorted_logs = []\nprint('Sorted logs:', sorted_logs)\n",
            "solutionCode": "logs = [\n    ('user1', 200, 15),\n    ('user2', 500, 8),\n    ('user3', 200, 42),\n    ('user4', 500, 20)\n]\nsorted_logs = sorted(logs, key=lambda x: (x[1], -x[2]))\nprint('Sorted logs:', sorted_logs)\n",
            "expectedOutputPatterns": [
                "Sorted logs: [('user3', 200, 42), ('user1', 200, 15), ('user4', 500, 20), ('user2', 500, 8)]"
            ],
            "hint": "Use `sorted(logs, key=lambda x: (x[1], -x[2]))`."
        },
        "keyTakeaway": "Successfully implemented and verified Custom Sorting!"
    },
    {
        "id": "day62-step5",
        "stepNumber": 5,
        "title": "Day 62 Complete: Custom Comparators & Multi-Key Sorting",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 62,
        "heading": "Mastery Achieved: Custom Comparators & Multi-Key Sorting",
        "subheading": "You have solidified key mental models and techniques for Custom Sorting.",
        "recapRows": [
            {
                "concept": "Tuple Comparison",
                "naiveIntuition": "Must perform two independent sorting passes",
                "pythonReality": "Tuple keys (primary, secondary) evaluate tie-breakers automatically in a single sort pass"
            },
            {
                "concept": "Stability Advantage",
                "naiveIntuition": "Sort passes overwrite previous order",
                "pythonReality": "Because Python's sort is stable, you can also sort secondary first, then primary second"
            }
        ],
        "solidifiedConcepts": [
            "key Function Lambdas",
            "Multi-Attribute Tuple Keys"
        ],
        "nextDayPreview": {
            "dayNumber": 63,
            "title": "Inversion Counting with Merge Sort",
            "description": "Count the number of inverted pairs in an array in O(N log N) time by augmenting the merge sort procedure."
        }
    }
]
},
  63: {
  "dayNumber": 63,
  "title": "Inversion Counting with Merge Sort",
  "topicName": "Inversion Counting",
  "sectionId": "searching-and-sorting",
  "estimatedMinutes": 35,
  "difficulty": "DEVELOPING",
  "prerequisites": [
    56
  ],
  "concepts": [
    "Inversion Pair Invariant",
    "Merge Step Accumulation"
  ],
  "practiceSkills": [
    "Inversion Counting Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Count array inversions in O(N log N) time by instrumenting the Merge Sort merge phase",
    "Deduce remaining inversions when an element from the right array is selected first"
  ],
  "practiceArchetype": "problem",
  "flowTier": "tier2"
,
  "steps": [
    {
        "id": "day63-step1",
        "stepNumber": 1,
        "title": "Inversion Counting with Merge Sort: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Inversion Counting",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Inversion Counting.",
        "markdownContent": [
            "Inversion Counting measures how far an array is from sorted order, solvable in O(N log N) time by augmenting the merge step of Merge Sort.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Inversion Counting**, remember the central principle: Instrumenting the Merge Sort merge phase counts array inversions in O(N log N) time."
        ],
        "snippets": [
            {
                "title": "Inversion Counting Implementation Template",
                "code": "# Counting inversions during merge\n# if R[j] < L[i]: inversions += len(L) - i",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Instrumenting the Merge Sort merge phase counts array inversions in O(N log N) time."
    },
    {
        "id": "day63-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Inversion Counting",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "An inversion is a pair (i, j) where i < j but arr[i] > arr[j]. During merge: if right element R[j] is smaller than L[i], then R[j] is smaller than ALL remaining elements in L! Add len(L) - i to inversions.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Instrumenting the Merge Sort merge phase counts array inversions in O(N log N) time.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Inversion Counting Core Invariant",
                "content": "Instrumenting the Merge Sort merge phase counts array inversions in O(N log N) time."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Instrumenting the Merge Sort merge phase counts array inversions in O(N log N) time."
    },
    {
        "id": "day63-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Inversion Counting",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d63-q1",
                "question": "During the merge of two sorted lists L and R, if R[j] < L[i], how many inversions are contributed by R[j]?",
                "options": [
                    {
                        "id": "A",
                        "label": "len(L) - i, because all elements from L[i] to the end of L are greater than R[j]"
                    },
                    {
                        "id": "B",
                        "label": "Exactly 1 inversion"
                    },
                    {
                        "id": "C",
                        "label": "i + 1 inversions"
                    },
                    {
                        "id": "D",
                        "label": "len(R) - j inversions"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Because L is already sorted, if L[i] > R[j], every subsequent element L[i+1], L[i+2], ... is also > R[j]. Thus, R[j] forms inversions with all remaining len(L) - i elements!",
                    "B": "Incorrect: R[j] forms an inversion with every remaining element in L, not just L[i].",
                    "C": "Incorrect: Elements before i are already smaller than R[j].",
                    "D": "Incorrect: Inversions are formed against elements in the left sub-array."
                }
            },
            {
                "id": "chk-d63-q2",
                "question": "What does an inversion count of 0 indicate about an array?",
                "options": [
                    {
                        "id": "A",
                        "label": "The array is already perfectly sorted in non-decreasing order"
                    },
                    {
                        "id": "B",
                        "label": "The array contains no duplicate elements"
                    },
                    {
                        "id": "C",
                        "label": "The array is sorted in descending order"
                    },
                    {
                        "id": "D",
                        "label": "The array has an odd number of elements"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! If there are no pairs where i < j and arr[i] > arr[j], every element is <= its successors, which is the exact definition of sorted order.",
                    "B": "Incorrect: Duplicates can have 0 inversions if sorted.",
                    "C": "Incorrect: Descending order has the maximum number of inversions: N*(N-1)/2.",
                    "D": "Incorrect: Inversion count is independent of parity."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day63-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Inversion Counting",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Count total inversions in an array using Merge Sort.",
        "subheading": "Implement and verify Inversion Counting in the interactive workspace.",
        "task": {
            "title": "Count total inversions in an array using Merge Sort.",
            "instructions": [
                "Count total inversions in an array using Merge Sort.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "def count_inversions(arr: list[int]) -> int:\n    def sort_and_count(nums: list[int]) -> tuple[list[int], int]:\n        if len(nums) <= 1:\n            return nums, 0\n        mid = len(nums) // 2\n        left, count_l = sort_and_count(nums[:mid])\n        right, count_r = sort_and_count(nums[mid:])\n        merged = []\n        inv = count_l + count_r\n        i = j = 0\n        # TODO: Merge left and right, adding (len(left) - i) to inv when right[j] < left[i]\n        return merged, inv\n    _, total = sort_and_count(arr)\n    return total\n\nnums = [8, 4, 2, 1]\nprint('Total inversions:', count_inversions(nums))\n",
            "solutionCode": "def count_inversions(arr: list[int]) -> int:\n    def sort_and_count(nums: list[int]) -> tuple[list[int], int]:\n        if len(nums) <= 1:\n            return nums, 0\n        mid = len(nums) // 2\n        left, count_l = sort_and_count(nums[:mid])\n        right, count_r = sort_and_count(nums[mid:])\n        merged = []\n        inv = count_l + count_r\n        i = j = 0\n        while i < len(left) and j < len(right):\n            if left[i] <= right[j]:\n                merged.append(left[i])\n                i += 1\n            else:\n                merged.append(right[j])\n                inv += len(left) - i\n                j += 1\n        merged.extend(left[i:])\n        merged.extend(right[j:])\n        return merged, inv\n    _, total = sort_and_count(arr)\n    return total\n\nnums = [8, 4, 2, 1]\nprint('Total inversions:', count_inversions(nums))\n",
            "expectedOutputPatterns": [
                "Total inversions: 6"
            ],
            "hint": "When `right[j] < left[i]`, append `right[j]`, increment `j += 1`, and add `len(left) - i` to `inv`."
        },
        "keyTakeaway": "Successfully implemented and verified Inversion Counting!"
    },
    {
        "id": "day63-step5",
        "stepNumber": 5,
        "title": "Day 63 Complete: Inversion Counting with Merge Sort",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 63,
        "heading": "Mastery Achieved: Inversion Counting with Merge Sort",
        "subheading": "You have solidified key mental models and techniques for Inversion Counting.",
        "recapRows": [
            {
                "concept": "Simultaneous Counting",
                "naiveIntuition": "Compare all pairs in O(N^2)",
                "pythonReality": "Instrumenting the merge step counts all cross-boundary inversions in bulk in O(N log N)"
            },
            {
                "concept": "Maximum Inversions",
                "naiveIntuition": "Maximum inversions is N",
                "pythonReality": "A reversed array of size N has N * (N - 1) // 2 inversions"
            }
        ],
        "solidifiedConcepts": [
            "Inversion Pair Invariant",
            "Merge Step Accumulation"
        ],
        "nextDayPreview": {
            "dayNumber": 64,
            "title": "Ternary Search on Unimodal Functions",
            "description": "Apply ternary search to find extrema of unimodal functions by dividing intervals into three equal segments."
        }
    }
]
},
  64: {
  "dayNumber": 64,
  "title": "Ternary Search on Unimodal Functions",
  "topicName": "Ternary Search",
  "sectionId": "searching-and-sorting",
  "estimatedMinutes": 30,
  "difficulty": "DEVELOPING",
  "prerequisites": [
    51
  ],
  "concepts": [
    "Unimodal Function Extremum",
    "Trisection Convergence"
  ],
  "practiceSkills": [
    "Ternary Search Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Locate the extremum of a unimodal continuous function via search-space trisection",
    "Prove the 2/3 range reduction factor per iteration"
  ],
  "practiceArchetype": "algorithm",
  "flowTier": "tier1"
,
  "steps": [
    {
        "id": "day64-step1",
        "stepNumber": 1,
        "title": "Ternary Search on Unimodal Functions: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Ternary Search",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Ternary Search.",
        "markdownContent": [
            "Ternary Search finds the peak or trough of a unimodal continuous function by dividing the search interval into three equal parts using two midpoints m1 and m2.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Ternary Search**, remember the central principle: Ternary search optimizes unimodal functions in O(log3/2(Range)) steps."
        ],
        "snippets": [
            {
                "title": "Ternary Search Implementation Template",
                "code": "# Ternary search for maximum of unimodal function\ndef ternary_search_max(f, L, R, eps=1e-7):\n    while R - L > eps:\n        m1 = L + (R - L) / 3\n        m2 = R - (R - L) / 3\n        if f(m1) < f(m2): L = m1\n        else: R = m2\n    return (L + R) / 2",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Ternary search optimizes unimodal functions in O(log3/2(Range)) steps."
    },
    {
        "id": "day64-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Ternary Search",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Calculate m1 = L + (R - L) / 3 and m2 = R - (R - L) / 3. If f(m1) < f(m2), the maximum cannot reside in [L..m1], so update L = m1. Else R = m2. Range shrinks by 2/3 each step.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Ternary search optimizes unimodal functions in O(log3/2(Range)) steps.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Ternary Search Core Invariant",
                "content": "Ternary search optimizes unimodal functions in O(log3/2(Range)) steps."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Ternary search optimizes unimodal functions in O(log3/2(Range)) steps."
    },
    {
        "id": "day64-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Ternary Search",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d64-q1",
                "question": "What prerequisite must a function satisfy for ternary search to find its extremum?",
                "options": [
                    {
                        "id": "A",
                        "label": "The function must be unimodal: strictly increasing up to a unique peak, then strictly decreasing (or vice versa)"
                    },
                    {
                        "id": "B",
                        "label": "The function must be linear"
                    },
                    {
                        "id": "C",
                        "label": "The function must return integer values only"
                    },
                    {
                        "id": "D",
                        "label": "The derivative of the function must be constant"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Unimodality ensures that evaluating two midpoints m1 and m2 reliably discards one-third of the interval containing strictly inferior values.",
                    "B": "Incorrect: Linear functions have no internal peaks.",
                    "C": "Incorrect: Ternary search works on continuous real-valued functions.",
                    "D": "Incorrect: Constant derivative implies a straight line."
                }
            },
            {
                "id": "chk-d64-q2",
                "question": "By what factor does the search range shrink in each iteration of ternary search?",
                "options": [
                    {
                        "id": "A",
                        "label": "The interval shrinks to 2/3 of its previous width"
                    },
                    {
                        "id": "B",
                        "label": "The interval shrinks to 1/2 of its previous width"
                    },
                    {
                        "id": "C",
                        "label": "The interval shrinks to 1/3 of its previous width"
                    },
                    {
                        "id": "D",
                        "label": "The interval shrinks by a constant 1 unit"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Dividing into three equal parts and eliminating one third leaves two thirds: the new width is (2/3) * previous_width.",
                    "B": "Incorrect: 1/2 is the reduction factor of binary search.",
                    "C": "Incorrect: We eliminate 1/3, keeping 2/3.",
                    "D": "Incorrect: Convergence is geometric, not arithmetic."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day64-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Ternary Search",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Find the maximum of a quadratic parabola using ternary search.",
        "subheading": "Implement and verify Ternary Search in the interactive workspace.",
        "task": {
            "title": "Find the maximum of a quadratic parabola using ternary search.",
            "instructions": [
                "Find the maximum of a quadratic parabola using ternary search.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "def find_parabola_peak(L: float, R: float) -> float:\n    # Function f(x) = -(x - 3)**2 + 10 (peak at x = 3)\n    def f(x: float) -> float:\n        return -(x - 3) ** 2 + 10\n    # TODO: Perform ternary search with while R - L > 1e-6\n    return (L + R) / 2\n\nprint('Peak x location:', round(find_parabola_peak(0.0, 10.0), 2))\n",
            "solutionCode": "def find_parabola_peak(L: float, R: float) -> float:\n    def f(x: float) -> float:\n        return -(x - 3) ** 2 + 10\n    while R - L > 1e-6:\n        m1 = L + (R - L) / 3\n        m2 = R - (R - L) / 3\n        if f(m1) < f(m2):\n            L = m1\n        else:\n            R = m2\n    return (L + R) / 2\n\nprint('Peak x location:', round(find_parabola_peak(0.0, 10.0), 2))\n",
            "expectedOutputPatterns": [
                "Peak x location: 3.0"
            ],
            "hint": "While R - L > 1e-6: m1 = L + (R - L) / 3, m2 = R - (R - L) / 3. If f(m1) < f(m2): L = m1 else R = m2. Return (L + R) / 2."
        },
        "keyTakeaway": "Successfully implemented and verified Ternary Search!"
    },
    {
        "id": "day64-step5",
        "stepNumber": 5,
        "title": "Day 64 Complete: Ternary Search on Unimodal Functions",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 64,
        "heading": "Mastery Achieved: Ternary Search on Unimodal Functions",
        "subheading": "You have solidified key mental models and techniques for Ternary Search.",
        "recapRows": [
            {
                "concept": "Trisection vs Bisection",
                "naiveIntuition": "Binary search is always faster",
                "pythonReality": "Binary search requires monotonic functions (derivatives); ternary search finds peaks directly without computing derivatives"
            },
            {
                "concept": "Convergence Precision",
                "naiveIntuition": "Iterate until L == R",
                "pythonReality": "Floating point operations never reach exact equality; stop when R - L < epsilon (e.g. 1e-7)"
            }
        ],
        "solidifiedConcepts": [
            "Unimodal Function Extremum",
            "Trisection Convergence"
        ],
        "nextDayPreview": {
            "dayNumber": 65,
            "title": "Section 5 Review & Search/Sort Mastery",
            "description": "Synthesize binary search paradigms, comparison and non-comparison sorting algorithms, and custom comparators."
        }
    }
]
},
  65: {
  "dayNumber": 65,
  "title": "Section 5 Review & Search/Sort Mastery",
  "topicName": "Search & Sort Milestone",
  "sectionId": "searching-and-sorting",
  "estimatedMinutes": 45,
  "difficulty": "DEVELOPING",
  "prerequisites": [
    52,
    53,
    56,
    57,
    61,
    62
  ],
  "concepts": [
    "Search/Sort Hybridization",
    "Asymptotic Trade-off Selection",
    "Adaptive Pipelines"
  ],
  "practiceSkills": [
    "Search & Sort Milestone Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Design a high-performance hybrid sorting algorithm dynamically switching strategies at threshold K",
    "Solve composite placement interview problems under strict time and space budgets"
  ],
  "practiceArchetype": "milestone",
  "flowTier": "tier3"
,
  "steps": [
    {
        "id": "day65-step1",
        "stepNumber": 1,
        "title": "Section 5 Review & Search/Sort Mastery: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Search & Sort Milestone",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Search & Sort Milestone.",
        "markdownContent": [
            "Section 5 Review synthesizes binary search boundaries, divide-and-conquer sorting, non-comparison limits, and custom comparators into a high-performance hybrid sorting engine.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Search & Sort Milestone**, remember the central principle: Real-world sorting algorithms combine algorithmic strategies to maximize practical performance across different input sizes."
        ],
        "snippets": [
            {
                "title": "Search & Sort Milestone Implementation Template",
                "code": "# Hybrid Sort switching threshold\n# if len(arr) <= 16: insertion_sort(arr)\n# else: merge_sort(arr)",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Real-world sorting algorithms combine algorithmic strategies to maximize practical performance across different input sizes."
    },
    {
        "id": "day65-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Search & Sort Milestone",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "The hybrid sorting engine partitions large arrays with Quick Sort / Merge Sort and switches to Insertion Sort on small subarrays (size <= 16), minimizing overhead and cache misses.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Real-world sorting algorithms combine algorithmic strategies to maximize practical performance across different input sizes.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Search & Sort Milestone Core Invariant",
                "content": "Real-world sorting algorithms combine algorithmic strategies to maximize practical performance across different input sizes."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Real-world sorting algorithms combine algorithmic strategies to maximize practical performance across different input sizes."
    },
    {
        "id": "day65-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Search & Sort Milestone",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d65-q1",
                "question": "Why do production sorting algorithms (like Timsort and Introsort) switch to Insertion Sort on sub-arrays of size <= 16 or 32?",
                "options": [
                    {
                        "id": "A",
                        "label": "On small sub-arrays, Insertion Sort has near-zero overhead and higher cache locality, outperforming O(N log N) divide-and-conquer algorithms"
                    },
                    {
                        "id": "B",
                        "label": "Because Quick Sort cannot sort arrays smaller than 32 elements"
                    },
                    {
                        "id": "C",
                        "label": "To satisfy Python bytecode limits"
                    },
                    {
                        "id": "D",
                        "label": "To avoid allocating CPU registers"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Asymptotic Big-O hides constant factors. For N <= 16, N^2 <= 256 while N log N with recursion overhead has a higher total operation count. Insertion sort runs faster on tiny inputs.",
                    "B": "Incorrect: Quick Sort functions on any length >= 2.",
                    "C": "Incorrect: No bytecode limits are involved.",
                    "D": "Incorrect: Register allocation is handled by the hardware/compiler."
                }
            },
            {
                "id": "chk-d65-q2",
                "question": "Which sorting algorithm is optimal for sorting 10,000,000 integers known to fall strictly within the range [0, 100]?",
                "options": [
                    {
                        "id": "A",
                        "label": "Counting Sort in O(N) time and O(1) extra space"
                    },
                    {
                        "id": "B",
                        "label": "Quick Sort in O(N log N)"
                    },
                    {
                        "id": "C",
                        "label": "Merge Sort in O(N log N)"
                    },
                    {
                        "id": "D",
                        "label": "Insertion Sort in O(N^2)"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! With range K = 100 and N = 10,000,000, Counting Sort allocates an array of only 101 integers and completes in O(N) linear time, vastly outperforming comparison sorts.",
                    "B": "Incorrect: Quick Sort would perform ~240 million comparisons.",
                    "C": "Incorrect: Merge Sort would require 80MB of auxiliary buffer memory.",
                    "D": "Incorrect: Quadratic sort on 10 million elements would stall for hours."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day65-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Search & Sort Milestone",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Build a hybrid sorting function that switches to insertion sort when sub-array size <= 4.",
        "subheading": "Implement and verify Search & Sort Milestone in the interactive workspace.",
        "task": {
            "title": "Build a hybrid sorting function that switches to insertion sort when sub-array size <= 4.",
            "instructions": [
                "Build a hybrid sorting function that switches to insertion sort when sub-array size <= 4.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "def hybrid_sort(arr: list[int], threshold: int = 4) -> list[int]:\n    # TODO: If len(arr) <= threshold, sort using insertion sort\n    # Otherwise, split at mid, recurse, and merge\n    return arr\n\nnums = [9, 3, 1, 7, 5, 8, 2, 6, 4]\nprint('Hybrid sorted:', hybrid_sort(nums, 4))\n",
            "solutionCode": "def hybrid_sort(arr: list[int], threshold: int = 4) -> list[int]:\n    if len(arr) <= threshold:\n        for i in range(1, len(arr)):\n            key = arr[i]\n            j = i - 1\n            while j >= 0 and arr[j] > key:\n                arr[j + 1] = arr[j]\n                j -= 1\n            arr[j + 1] = key\n        return arr\n    mid = len(arr) // 2\n    left = hybrid_sort(arr[:mid], threshold)\n    right = hybrid_sort(arr[mid:], threshold)\n    res = []\n    i = j = 0\n    while i < len(left) and j < len(right):\n        if left[i] <= right[j]:\n            res.append(left[i])\n            i += 1\n        else:\n            res.append(right[j])\n            j += 1\n    res.extend(left[i:])\n    res.extend(right[j:])\n    return res\n\nnums = [9, 3, 1, 7, 5, 8, 2, 6, 4]\nprint('Hybrid sorted:', hybrid_sort(nums, 4))\n",
            "expectedOutputPatterns": [
                "Hybrid sorted: [1, 2, 3, 4, 5, 6, 7, 8, 9]"
            ],
            "hint": "Check `if len(arr) <= threshold: do insertion sort and return arr`. Else recurse on left and right, then merge with two pointers."
        },
        "keyTakeaway": "Successfully implemented and verified Search & Sort Milestone!"
    },
    {
        "id": "day65-step5",
        "stepNumber": 5,
        "title": "Day 65 Complete: Section 5 Review & Search/Sort Mastery",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 65,
        "heading": "Mastery Achieved: Section 5 Review & Search/Sort Mastery",
        "subheading": "You have solidified key mental models and techniques for Search & Sort Milestone.",
        "recapRows": [
            {
                "concept": "Hybrid Architecture",
                "naiveIntuition": "One sorting algorithm is always the best",
                "pythonReality": "Real-world engineering combines algorithms: divide-and-conquer on macroscopic scale, insertion sort on microscopic scale"
            },
            {
                "concept": "Section 5 Synthesis",
                "naiveIntuition": "Searching and sorting are separate topics",
                "pythonReality": "Sorting is the preprocessing step that transforms unsorted O(N) searches into logarithmic O(log N) binary searches"
            }
        ],
        "solidifiedConcepts": [
            "Search/Sort Hybridization",
            "Asymptotic Trade-off Selection",
            "Adaptive Pipelines"
        ],
        "nextDayPreview": {
            "dayNumber": 66,
            "title": "Hash Functions, Prime Moduli & Distribution",
            "description": "Understand hash function properties: uniformity, determinism, avalanche effect, and prime-number modulo bucketing."
        }
    }
]
},
  66: {
  "dayNumber": 66,
  "title": "Hash Functions, Prime Moduli & Distribution",
  "topicName": "Hash Functions",
  "sectionId": "hashing-and-hash-tables",
  "estimatedMinutes": 30,
  "difficulty": "DEVELOPING",
  "prerequisites": [
    15,
    27
  ],
  "concepts": [
    "Uniform Distribution & Avalanche Effect",
    "Prime Modulo Bucketing"
  ],
  "practiceSkills": [
    "Hash Functions Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Evaluate hash functions on key avalanche and uniformity metrics",
    "Apply prime modulus division to minimize bucket collisions"
  ],
  "practiceArchetype": "tracing",
  "flowTier": "tier1"
,
  "steps": [
    {
        "id": "day66-step1",
        "stepNumber": 1,
        "title": "Hash Functions, Prime Moduli & Distribution: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Hash Functions",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Hash Functions.",
        "markdownContent": [
            "Hash Functions map arbitrary keys into fixed-size integer bucket indices, requiring determinism, uniform distribution, and avalanche effect.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Hash Functions**, remember the central principle: Good hash functions scatter keys uniformly across prime-sized bucket arrays, preventing clustering."
        ],
        "snippets": [
            {
                "title": "Hash Functions Implementation Template",
                "code": "# Polynomial Rolling Hash function for strings\ndef string_hash(s, P=31, M=1_000_000_007):\n    h = 0\n    for ch in s:\n        h = (h * P + ord(ch)) % M\n    return h",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Good hash functions scatter keys uniformly across prime-sized bucket arrays, preventing clustering."
    },
    {
        "id": "day66-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Hash Functions",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Using a prime modulus (bucket_idx = hash(key) % P) minimizes collisions when keys exhibit stride patterns. The avalanche effect ensures a single bit flip in the input completely alters the output hash bits.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Good hash functions scatter keys uniformly across prime-sized bucket arrays, preventing clustering.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Hash Functions Core Invariant",
                "content": "Good hash functions scatter keys uniformly across prime-sized bucket arrays, preventing clustering."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Good hash functions scatter keys uniformly across prime-sized bucket arrays, preventing clustering."
    },
    {
        "id": "day66-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Hash Functions",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d66-q1",
                "question": "Why are prime numbers typically used as moduli when mapping hash values to bucket arrays?",
                "options": [
                    {
                        "id": "A",
                        "label": "Prime moduli prevent common factors with key patterns from causing systematic bucket clustering"
                    },
                    {
                        "id": "B",
                        "label": "Because computers can only divide by prime numbers"
                    },
                    {
                        "id": "C",
                        "label": "Prime moduli eliminate all hash collisions completely"
                    },
                    {
                        "id": "D",
                        "label": "Python enforces that array lengths must be prime"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! If bucket count M shares factors with key strides (e.g. even numbers modulo 100), keys only map to a fraction of the buckets. A prime modulus shares no factors, distributing keys uniformly.",
                    "B": "Incorrect: Hardware ALUs divide by any non-zero integer.",
                    "C": "Incorrect: Pigeonhole Principle guarantees collisions whenever key count > bucket count.",
                    "D": "Incorrect: Python uses powers of 2 for dict sizes."
                }
            },
            {
                "id": "chk-d66-q2",
                "question": "What is the 'avalanche effect' in hash function design?",
                "options": [
                    {
                        "id": "A",
                        "label": "A single bit change in the input key causes approximately 50% of the output hash bits to flip randomly"
                    },
                    {
                        "id": "B",
                        "label": "The hash table expands exponentially when full"
                    },
                    {
                        "id": "C",
                        "label": "Memory usage doubles every second"
                    },
                    {
                        "id": "D",
                        "label": "All keys collapse into bucket zero"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Cryptographic and high-quality hash functions ensure that small input variations result in completely uncorrelated output hashes.",
                    "B": "Incorrect: That describes dynamic resizing load factor policies.",
                    "C": "Incorrect: Hash functions do not allocate memory dynamically.",
                    "D": "Incorrect: That is worst-case hash collapse."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day66-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Hash Functions",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Trace hash bit distribution across bucket arrays.",
        "subheading": "Implement and verify Hash Functions in the interactive workspace.",
        "task": {
            "title": "Trace hash bit distribution across bucket arrays.",
            "instructions": [
                "Trace hash bit distribution across bucket arrays.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "# Day 66 Tracing: Hash Bucket Distribution\ndef bucket_distribution(keys: list[str], num_buckets: int) -> dict[int, list[str]]:\n    buckets = {i: [] for i in range(num_buckets)}\n    # TODO: For each key, compute polynomial hash (P=31, M=10007), map to bucket, append key\n    return buckets\n\nwords = ['cat', 'dog', 'act', 'god', 'tac']\nprint('Buckets:', bucket_distribution(words, 5))\n",
            "solutionCode": "def bucket_distribution(keys: list[str], num_buckets: int) -> dict[int, list[str]]:\n    buckets = {i: [] for i in range(num_buckets)}\n    for k in keys:\n        h = 0\n        for ch in k:\n            h = (h * 31 + ord(ch)) % 10007\n        b_idx = h % num_buckets\n        buckets[b_idx].append(k)\n    return buckets\n\nwords = ['cat', 'dog', 'act', 'god', 'tac']\nprint('Buckets:', bucket_distribution(words, 5))\n",
            "expectedOutputPatterns": [
                "Buckets: {0: ['act'], 1: ['cat', 'tac'], 2: ['dog'], 3: ['god'], 4: []}"
            ],
            "hint": "Loop over key: h = (h * 31 + ord(ch)) % 10007. Bucket index is h % num_buckets."
        },
        "keyTakeaway": "Successfully implemented and verified Hash Functions!"
    },
    {
        "id": "day66-step5",
        "stepNumber": 5,
        "title": "Day 66 Complete: Hash Functions, Prime Moduli & Distribution",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 66,
        "heading": "Mastery Achieved: Hash Functions, Prime Moduli & Distribution",
        "subheading": "You have solidified key mental models and techniques for Hash Functions.",
        "recapRows": [
            {
                "concept": "Pigeonhole Inevitability",
                "naiveIntuition": "A perfect hash function has zero collisions",
                "pythonReality": "When mapping infinite inputs to finite buckets, collisions are mathematically inevitable; resolution strategies are required"
            },
            {
                "concept": "Deterministic Invariant",
                "naiveIntuition": "hash() can return different numbers for identical keys",
                "pythonReality": "A hash function must return the identical hash integer for equal keys within a single program execution"
            }
        ],
        "solidifiedConcepts": [
            "Uniform Distribution & Avalanche Effect",
            "Prime Modulo Bucketing"
        ],
        "nextDayPreview": {
            "dayNumber": 67,
            "title": "Collision Resolution: Chaining vs Probing",
            "description": "Implement collision resolution via separate chaining and open addressing (linear, quadratic, and double hashing)."
        }
    }
]
},
  67: {
  "dayNumber": 67,
  "title": "Collision Resolution: Chaining vs Probing",
  "topicName": "Collision Resolution",
  "sectionId": "hashing-and-hash-tables",
  "estimatedMinutes": 35,
  "difficulty": "DEVELOPING",
  "prerequisites": [
    66
  ],
  "concepts": [
    "Separate Chaining with Buckets",
    "Linear & Quadratic Probing"
  ],
  "practiceSkills": [
    "Collision Resolution Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Implement a hash map resolving collisions via separate chaining buckets",
    "Trace open addressing probing sequences and tombstone deletion markers"
  ],
  "practiceArchetype": "algorithm",
  "flowTier": "tier2"
,
  "steps": [
    {
        "id": "day67-step1",
        "stepNumber": 1,
        "title": "Collision Resolution: Chaining vs Probing: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Collision Resolution",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Collision Resolution.",
        "markdownContent": [
            "Collision Resolution manages hash collisions via Separate Chaining (linked buckets) or Open Addressing (probing empty slots within a contiguous array).",
            "### Foundational Mental Model\nWhen approaching problems requiring **Collision Resolution**, remember the central principle: Maintaining load factors below 2/3 guarantees average O(1) lookup and insertion times."
        ],
        "snippets": [
            {
                "title": "Collision Resolution Implementation Template",
                "code": "# Separate Chaining Hash Map\nclass SimpleHashMap:\n    def __init__(self, size=10):\n        self.buckets = [[] for _ in range(size)]\n    def put(self, k, v):\n        b = self.buckets[hash(k) % len(self.buckets)]\n        for i, (k2, _) in enumerate(b):\n            if k2 == k: b[i] = (k, v); return\n        b.append((k, v))\n    def get(self, k):\n        b = self.buckets[hash(k) % len(self.buckets)]\n        for k2, v in b:\n            if k2 == k: return v\n        return None",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Maintaining load factors below 2/3 guarantees average O(1) lookup and insertion times."
    },
    {
        "id": "day67-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Collision Resolution",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Separate Chaining stores collisions in linked lists or balanced trees per bucket. Linear Probing tests idx + 1, idx + 2. When load factor (N / capacity) exceeds 0.66, the table doubles and rehashes all keys.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Maintaining load factors below 2/3 guarantees average O(1) lookup and insertion times.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Collision Resolution Core Invariant",
                "content": "Maintaining load factors below 2/3 guarantees average O(1) lookup and insertion times."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Maintaining load factors below 2/3 guarantees average O(1) lookup and insertion times."
    },
    {
        "id": "day67-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Collision Resolution",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d67-q1",
                "question": "Why must an open-addressing hash table use 'tombstones' (dummy markers) when deleting keys?",
                "options": [
                    {
                        "id": "A",
                        "label": "To prevent probe chains from terminating prematurely on empty slots, preserving lookup paths for keys inserted later in the probe sequence"
                    },
                    {
                        "id": "B",
                        "label": "To prevent memory leaks in Python"
                    },
                    {
                        "id": "C",
                        "label": "Because open addressing cannot delete keys"
                    },
                    {
                        "id": "D",
                        "label": "To rehash the entire table immediately"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! If a slot is simply marked empty (None), linear probing stops searching immediately. A tombstone signals: 'keep probing because a deleted key used to be here'.",
                    "B": "Incorrect: Tombstones maintain lookup correctness, not garbage collection.",
                    "C": "Incorrect: Keys can be deleted using tombstones.",
                    "D": "Incorrect: Rehashing occurs on resize, not on deletion."
                }
            },
            {
                "id": "chk-d67-q2",
                "question": "What happens to the worst-case time complexity of a hash map if all N keys hash to the exact same bucket?",
                "options": [
                    {
                        "id": "A",
                        "label": "It degrades from O(1) to O(N) linear scan time"
                    },
                    {
                        "id": "B",
                        "label": "It remains strictly O(1)"
                    },
                    {
                        "id": "C",
                        "label": "It crashes with a MemoryError"
                    },
                    {
                        "id": "D",
                        "label": "It becomes O(log N)"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! If all keys land in a single bucket, looking up an item requires scanning all N elements in that chain, degrading to O(N).",
                    "B": "Incorrect: O(1) is average-case with uniform distribution.",
                    "C": "Incorrect: Memory is bounded by N.",
                    "D": "Incorrect: Degradation is O(N) unless buckets are balanced trees (like Java HashMap)."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day67-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Collision Resolution",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Implement a basic hash map using separate chaining buckets.",
        "subheading": "Implement and verify Collision Resolution in the interactive workspace.",
        "task": {
            "title": "Implement a basic hash map using separate chaining buckets.",
            "instructions": [
                "Implement a basic hash map using separate chaining buckets.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "class MyHashMap:\n    def __init__(self):\n        self.size = 1000\n        self.table = [[] for _ in range(self.size)]\n\n    def put(self, key: int, value: int) -> None:\n        # TODO: Hash key, check if key exists in bucket (update), else append (key, value)\n        pass\n\n    def get(self, key: int) -> int:\n        # TODO: Hash key, search bucket, return value or -1\n        return -1\n\nhm = MyHashMap()\nhm.put(1, 100)\nhm.put(2, 200)\nhm.put(1, 150)\nprint('Get key 1:', hm.get(1))\nprint('Get key 2:', hm.get(2))\nprint('Get key 3:', hm.get(3))\n",
            "solutionCode": "class MyHashMap:\n    def __init__(self):\n        self.size = 1000\n        self.table = [[] for _ in range(self.size)]\n\n    def put(self, key: int, value: int) -> None:\n        b_idx = key % self.size\n        bucket = self.table[b_idx]\n        for i, (k, v) in enumerate(bucket):\n            if k == key:\n                bucket[i] = (key, value)\n                return\n        bucket.append((key, value))\n\n    def get(self, key: int) -> int:\n        b_idx = key % self.size\n        bucket = self.table[b_idx]\n        for k, v in bucket:\n            if k == key:\n                return v\n        return -1\n\nhm = MyHashMap()\nhm.put(1, 100)\nhm.put(2, 200)\nhm.put(1, 150)\nprint('Get key 1:', hm.get(1))\nprint('Get key 2:', hm.get(2))\nprint('Get key 3:', hm.get(3))\n",
            "expectedOutputPatterns": [
                "Get key 1: 150",
                "Get key 2: 200",
                "Get key 3: -1"
            ],
            "hint": "Bucket is self.table[key % self.size]. Search for matching k to update; if not found, append (key, value)."
        },
        "keyTakeaway": "Successfully implemented and verified Collision Resolution!"
    },
    {
        "id": "day67-step5",
        "stepNumber": 5,
        "title": "Day 67 Complete: Collision Resolution: Chaining vs Probing",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 67,
        "heading": "Mastery Achieved: Collision Resolution: Chaining vs Probing",
        "subheading": "You have solidified key mental models and techniques for Collision Resolution.",
        "recapRows": [
            {
                "concept": "Load Factor Balance",
                "naiveIntuition": "Fill buckets until 100% full",
                "pythonReality": "When load factor exceeds 2/3, performance degrades rapidly; resizing at 66% preserves O(1) performance"
            },
            {
                "concept": "CPython Compact Dict",
                "naiveIntuition": "Python uses separate chaining",
                "pythonReality": "CPython 3.6+ uses open addressing with a sparse index array and a dense entries table to save memory and preserve insertion order"
            }
        ],
        "solidifiedConcepts": [
            "Separate Chaining with Buckets",
            "Linear & Quadratic Probing"
        ],
        "nextDayPreview": {
            "dayNumber": 68,
            "title": "Frequency Counting & Anagram Detection",
            "description": "Use frequency tables and hash maps to solve anagram detection and character count equality in O(N) time."
        }
    }
]
},
  68: {
  "dayNumber": 68,
  "title": "Frequency Counting & Anagram Detection",
  "topicName": "Frequency Hashing",
  "sectionId": "hashing-and-hash-tables",
  "estimatedMinutes": 30,
  "difficulty": "DEVELOPING",
  "prerequisites": [
    3,
    17,
    67
  ],
  "concepts": [
    "Fixed Alphabet Frequency Arrays",
    "Valid Anagram Verification"
  ],
  "practiceSkills": [
    "Frequency Hashing Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Count character frequencies in O(N) time and O(1) auxiliary space using ord() offsets",
    "Determine anagram equivalence without sorting inputs"
  ],
  "practiceArchetype": "problem",
  "flowTier": "tier1"
,
  "steps": [
    {
        "id": "day68-step1",
        "stepNumber": 1,
        "title": "Frequency Counting & Anagram Detection: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Frequency Hashing",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Frequency Hashing.",
        "markdownContent": [
            "Frequency Counting uses fixed-size arrays or hash maps to record element occurrences, solving Anagram Detection and First Unique Character in O(N) time.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Frequency Hashing**, remember the central principle: Counting frequencies directly with 26-slot arrays avoids sorting overhead and runs in O(N) time and O(1) space."
        ],
        "snippets": [
            {
                "title": "Frequency Hashing Implementation Template",
                "code": "# Valid Anagram using frequency array\ndef is_anagram(s, t):\n    if len(s) != len(t): return False\n    counts = [0] * 26\n    for ch1, ch2 in zip(s, t):\n        counts[ord(ch1) - ord('a')] += 1\n        counts[ord(ch2) - ord('a')] -= 1\n    return all(c == 0 for c in counts)",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Counting frequencies directly with 26-slot arrays avoids sorting overhead and runs in O(N) time and O(1) space."
    },
    {
        "id": "day68-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Frequency Hashing",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "For lowercase English letters: allocate count = [0] * 26. Increment count[ord(ch) - ord('a')] for s, decrement for t. If all 26 entries equal 0, s and t are valid anagrams.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Counting frequencies directly with 26-slot arrays avoids sorting overhead and runs in O(N) time and O(1) space.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Frequency Hashing Core Invariant",
                "content": "Counting frequencies directly with 26-slot arrays avoids sorting overhead and runs in O(N) time and O(1) space."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Counting frequencies directly with 26-slot arrays avoids sorting overhead and runs in O(N) time and O(1) space."
    },
    {
        "id": "day68-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Frequency Hashing",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d68-q1",
                "question": "Why is a fixed 26-element integer array preferred over a general dictionary for lowercase English string anagrams?",
                "options": [
                    {
                        "id": "A",
                        "label": "It uses fixed O(1) space, zero heap hash allocations, and immediate direct index offsets ord(c) - ord('a')"
                    },
                    {
                        "id": "B",
                        "label": "Because dictionaries cannot store negative numbers"
                    },
                    {
                        "id": "C",
                        "label": "Because string sorting takes O(1) time"
                    },
                    {
                        "id": "D",
                        "label": "Dictionaries cannot compare letter counts"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! A 26-element array allocates fixed contiguous memory once, avoiding hash calculations, open addressing probes, and dictionary resizing overhead.",
                    "B": "Incorrect: Dictionaries can store any integers.",
                    "C": "Incorrect: String sorting takes O(N log N).",
                    "D": "Incorrect: Dictionaries can count letters, but arrays have lower constant factors."
                }
            },
            {
                "id": "chk-d68-q2",
                "question": "What is the time complexity of comparing two strings of length N using sorted(s) == sorted(t)?",
                "options": [
                    {
                        "id": "A",
                        "label": "O(N log N)"
                    },
                    {
                        "id": "B",
                        "label": "O(N)"
                    },
                    {
                        "id": "C",
                        "label": "O(1)"
                    },
                    {
                        "id": "D",
                        "label": "O(N^2)"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Sorting both strings takes O(N log N) time; frequency arrays reduce this to strictly linear O(N) time.",
                    "B": "Incorrect: Comparison sort cannot beat Omega(N log N).",
                    "C": "Incorrect: All characters must be processed.",
                    "D": "Incorrect: Timsort is O(N log N), not quadratic."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day68-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Frequency Hashing",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Determine if two strings are valid anagrams in O(N) time and O(1) space.",
        "subheading": "Implement and verify Frequency Hashing in the interactive workspace.",
        "task": {
            "title": "Determine if two strings are valid anagrams in O(N) time and O(1) space.",
            "instructions": [
                "Determine if two strings are valid anagrams in O(N) time and O(1) space.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "def is_anagram(s: str, t: str) -> bool:\n    if len(s) != len(t):\n        return False\n    # TODO: Count character frequencies using ord(c) - ord('a') and verify all counts are 0\n    return False\n\nprint('Anagram test 1:', is_anagram('anagram', 'nagaram'))\nprint('Anagram test 2:', is_anagram('rat', 'car'))\n",
            "solutionCode": "def is_anagram(s: str, t: str) -> bool:\n    if len(s) != len(t):\n        return False\n    counts = [0] * 26\n    for ch1, ch2 in zip(s, t):\n        counts[ord(ch1) - ord('a')] += 1\n        counts[ord(ch2) - ord('a')] -= 1\n    return all(c == 0 for c in counts)\n\nprint('Anagram test 1:', is_anagram('anagram', 'nagaram'))\nprint('Anagram test 2:', is_anagram('rat', 'car'))\n",
            "expectedOutputPatterns": [
                "Anagram test 1: True",
                "Anagram test 2: False"
            ],
            "hint": "counts = [0] * 26. In zip(s, t), increment ord(ch1) - 97 and decrement ord(ch2) - 97. Return all(c == 0 for c in counts)."
        },
        "keyTakeaway": "Successfully implemented and verified Frequency Hashing!"
    },
    {
        "id": "day68-step5",
        "stepNumber": 5,
        "title": "Day 68 Complete: Frequency Counting & Anagram Detection",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 68,
        "heading": "Mastery Achieved: Frequency Counting & Anagram Detection",
        "subheading": "You have solidified key mental models and techniques for Frequency Hashing.",
        "recapRows": [
            {
                "concept": "Array vs Hash Map",
                "naiveIntuition": "Always use dict for frequencies",
                "pythonReality": "When alphabet size is bounded (e.g. 26 letters), a fixed array is lighter and faster than a hash map"
            },
            {
                "concept": "Early Length Guard",
                "naiveIntuition": "Count all characters first",
                "pythonReality": "If len(s) != len(t), return False immediately in O(1) time"
            }
        ],
        "solidifiedConcepts": [
            "Fixed Alphabet Frequency Arrays",
            "Valid Anagram Verification"
        ],
        "nextDayPreview": {
            "dayNumber": 69,
            "title": "Subarray Sums = K with Prefix Hash Maps",
            "description": "Combine prefix sums with hash maps to count contiguous subarrays summing to K in O(N) time."
        }
    }
]
},
  69: {
  "dayNumber": 69,
  "title": "Subarray Sums = K with Prefix Hash Maps",
  "topicName": "Prefix Hash Maps",
  "sectionId": "hashing-and-hash-tables",
  "estimatedMinutes": 40,
  "difficulty": "DEVELOPING",
  "prerequisites": [
    37,
    68
  ],
  "concepts": [
    "Prefix Sum Frequency Invariant",
    "Two-Sum Reduction (pref - k)"
  ],
  "practiceSkills": [
    "Prefix Hash Maps Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Store cumulative prefix sum frequencies in a hash table to find target subarrays",
    "Solve Subarray Sum Equals K in O(N) time and O(N) space"
  ],
  "practiceArchetype": "problem",
  "flowTier": "tier2"
,
  "steps": [
    {
        "id": "day69-step1",
        "stepNumber": 1,
        "title": "Subarray Sums = K with Prefix Hash Maps: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Prefix Hash Maps",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Prefix Hash Maps.",
        "markdownContent": [
            "Subarray Sum Equals K pairs prefix sums with hash maps to count contiguous subarrays summing to K in O(N) time and O(N) space.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Prefix Hash Maps**, remember the central principle: Prefix sums paired with hash maps reduce contiguous subarray sum queries from O(N^2) to O(N)."
        ],
        "snippets": [
            {
                "title": "Prefix Hash Maps Implementation Template",
                "code": "# Subarray Sum Equals K\ndef subarray_sum(nums, k):\n    counts = {0: 1} # Base prefix before index 0\n    curr = ans = 0\n    for x in nums:\n        curr += x\n        ans += counts.get(curr - k, 0)\n        counts[curr] = counts.get(curr, 0) + 1\n    return ans",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Prefix sums paired with hash maps reduce contiguous subarray sum queries from O(N^2) to O(N)."
    },
    {
        "id": "day69-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Prefix Hash Maps",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "If pref[j] - pref[i] == k, then pref[i] == pref[j] - k. By tracking the frequencies of past prefix sums in a hash map, we count all matching indices i in O(1) time per element.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Prefix sums paired with hash maps reduce contiguous subarray sum queries from O(N^2) to O(N).\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Prefix Hash Maps Core Invariant",
                "content": "Prefix sums paired with hash maps reduce contiguous subarray sum queries from O(N^2) to O(N)."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Prefix sums paired with hash maps reduce contiguous subarray sum queries from O(N^2) to O(N)."
    },
    {
        "id": "day69-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Prefix Hash Maps",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d69-q1",
                "question": "Why must the prefix sum frequency map be initialized with `{0: 1}` before scanning elements?",
                "options": [
                    {
                        "id": "A",
                        "label": "To handle subarrays starting from index 0 whose cumulative sum directly equals K without needing a previous subtraction"
                    },
                    {
                        "id": "B",
                        "label": "To prevent division by zero errors"
                    },
                    {
                        "id": "C",
                        "label": "Because 0 is the default key in all Python dictionaries"
                    },
                    {
                        "id": "D",
                        "label": "It is not required and can be omitted"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! If curr == k, curr - k = 0. Having {0: 1} ensures that subarrays spanning from index 0 to the current element are counted.",
                    "B": "Incorrect: No division is performed.",
                    "C": "Incorrect: Dictionaries have no default keys unless defaultdict is used.",
                    "D": "Incorrect: Without {0: 1}, all subarrays starting at index 0 are omitted."
                }
            },
            {
                "id": "chk-d69-q2",
                "question": "Why can't we use a simple sliding window for Subarray Sum Equals K if the array contains negative numbers?",
                "options": [
                    {
                        "id": "A",
                        "label": "Negative numbers destroy window monotonicity: expanding the window can decrease the sum, and shrinking can increase the sum"
                    },
                    {
                        "id": "B",
                        "label": "Sliding window cannot be implemented in Python"
                    },
                    {
                        "id": "C",
                        "label": "Negative numbers cannot be stored in variables"
                    },
                    {
                        "id": "D",
                        "label": "Sliding window requires all numbers to be equal"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Sliding window requires monotonic sums (adding numbers always increases sum). Negative numbers break this, making the prefix hash map the only linear O(N) solution.",
                    "B": "Incorrect: Sliding window is widely used in Python.",
                    "C": "Incorrect: Negative numbers are valid integers.",
                    "D": "Incorrect: Window elements can vary."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day69-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Prefix Hash Maps",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Count total contiguous subarrays summing to target K.",
        "subheading": "Implement and verify Prefix Hash Maps in the interactive workspace.",
        "task": {
            "title": "Count total contiguous subarrays summing to target K.",
            "instructions": [
                "Count total contiguous subarrays summing to target K.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "def subarray_sum(nums: list[int], k: int) -> int:\n    counts = {0: 1}\n    curr_sum = 0\n    total_subarrays = 0\n    # TODO: Iterate nums, update curr_sum, add counts.get(curr_sum - k, 0) to total, and update counts map\n    \n    return total_subarrays\n\nnums = [1, 2, 3, -2, 2]\nprint('Total subarrays summing to 3:', subarray_sum(nums, 3))\n",
            "solutionCode": "def subarray_sum(nums: list[int], k: int) -> int:\n    counts = {0: 1}\n    curr_sum = 0\n    total_subarrays = 0\n    for x in nums:\n        curr_sum += x\n        total_subarrays += counts.get(curr_sum - k, 0)\n        counts[curr_sum] = counts.get(curr_sum, 0) + 1\n    return total_subarrays\n\nnums = [1, 2, 3, -2, 2]\nprint('Total subarrays summing to 3:', subarray_sum(nums, 3))\n",
            "expectedOutputPatterns": [
                "Total subarrays summing to 3: 3"
            ],
            "hint": "Loop x in nums: curr_sum += x, total += counts.get(curr_sum - k, 0), counts[curr_sum] = counts.get(curr_sum, 0) + 1."
        },
        "keyTakeaway": "Successfully implemented and verified Prefix Hash Maps!"
    },
    {
        "id": "day69-step5",
        "stepNumber": 5,
        "title": "Day 69 Complete: Subarray Sums = K with Prefix Hash Maps",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 69,
        "heading": "Mastery Achieved: Subarray Sums = K with Prefix Hash Maps",
        "subheading": "You have solidified key mental models and techniques for Prefix Hash Maps.",
        "recapRows": [
            {
                "concept": "Two-Sum on Prefixes",
                "naiveIntuition": "Check all subarray sums in O(N^2)",
                "pythonReality": "Looking up (curr - k) in past prefix frequencies reduces subarray counting to O(N)"
            },
            {
                "concept": "Update Order",
                "naiveIntuition": "Add current prefix to map before checking count",
                "pythonReality": "Check (curr - k) first, then increment counts[curr] to avoid counting empty subarrays"
            }
        ],
        "solidifiedConcepts": [
            "Prefix Sum Frequency Invariant",
            "Two-Sum Reduction (pref - k)"
        ],
        "nextDayPreview": {
            "dayNumber": 70,
            "title": "Grouping & Canonical Equivalence Keys",
            "description": "Design canonical hash keys to group anagrams, coordinate patterns, and equivalence classes in O(N * K) time."
        }
    }
]
},
  70: {
  "dayNumber": 70,
  "title": "Grouping & Canonical Equivalence Keys",
  "topicName": "Equivalence Hashing",
  "sectionId": "hashing-and-hash-tables",
  "estimatedMinutes": 30,
  "difficulty": "DEVELOPING",
  "prerequisites": [
    14,
    68
  ],
  "concepts": [
    "Canonical Representation Tuple",
    "Multi-Element Grouping"
  ],
  "practiceSkills": [
    "Equivalence Hashing Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Construct immutable tuple signature keys to partition elements into equivalence classes",
    "Group anagrams in O(N * K) time without expensive string sorts"
  ],
  "practiceArchetype": "problem",
  "flowTier": "tier1"
,
  "steps": [
    {
        "id": "day70-step1",
        "stepNumber": 1,
        "title": "Grouping & Canonical Equivalence Keys: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Equivalence Hashing",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Equivalence Hashing.",
        "markdownContent": [
            "Grouping into Equivalence Classes constructs canonical hash keys (sorted strings or character count tuples) to partition items in O(N * K) time.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Equivalence Hashing**, remember the central principle: Canonical representation keys group permutations and equivalence classes in O(N * K) time without sorting."
        ],
        "snippets": [
            {
                "title": "Equivalence Hashing Implementation Template",
                "code": "# Group Anagrams by character count tuple\nfrom collections import defaultdict\ndef group_anagrams(words):\n    groups = defaultdict(list)\n    for w in words:\n        count = [0] * 26\n        for ch in w: count[ord(ch) - ord('a')] += 1\n        groups[tuple(count)].append(w)\n    return list(groups.values())",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Canonical representation keys group permutations and equivalence classes in O(N * K) time without sorting."
    },
    {
        "id": "day70-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Equivalence Hashing",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "For Group Anagrams: map each word to a 26-tuple of character counts: tuple([0]*26). Because tuples are hashable, use the tuple as a dictionary key: groups[key].append(word).",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Canonical representation keys group permutations and equivalence classes in O(N * K) time without sorting.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Equivalence Hashing Core Invariant",
                "content": "Canonical representation keys group permutations and equivalence classes in O(N * K) time without sorting."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Canonical representation keys group permutations and equivalence classes in O(N * K) time without sorting."
    },
    {
        "id": "day70-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Equivalence Hashing",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d70-q1",
                "question": "Why is a 26-element tuple used as the dictionary key rather than a 26-element list in Group Anagrams?",
                "options": [
                    {
                        "id": "A",
                        "label": "Lists are mutable and unhashable; tuples are immutable and hashable, allowing them to serve as dictionary keys"
                    },
                    {
                        "id": "B",
                        "label": "Tuples sort faster than lists"
                    },
                    {
                        "id": "C",
                        "label": "Python does not allow lists with 26 elements"
                    },
                    {
                        "id": "D",
                        "label": "Lists cannot store integer zeroes"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! In Python, dictionary keys must implement __hash__. Mutable lists set __hash__ = None, raising TypeError: unhashable type: 'list'. Tuples are immutable and hashable.",
                    "B": "Incorrect: Tuples are not sorted here.",
                    "C": "Incorrect: Lists can have arbitrary lengths.",
                    "D": "Incorrect: Lists can store any integer."
                }
            },
            {
                "id": "chk-d70-q2",
                "question": "What is the time complexity of grouping N words of maximum length K using count-tuple keys compared to string-sorting keys?",
                "options": [
                    {
                        "id": "A",
                        "label": "O(N * K) for count tuples vs O(N * K log K) for string sorting"
                    },
                    {
                        "id": "B",
                        "label": "O(N^2) for count tuples"
                    },
                    {
                        "id": "C",
                        "label": "O(N * K) for both"
                    },
                    {
                        "id": "D",
                        "label": "O(1) for count tuples"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Building a 26-count array takes O(K) linear time per word. Sorting each word takes O(K log K). Across N words: O(N * K) vs O(N * K log K).",
                    "B": "Incorrect: Count tuples take linear time in total word length.",
                    "C": "Incorrect: Sorting adds the log K factor.",
                    "D": "Incorrect: Must inspect all K characters."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day70-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Equivalence Hashing",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Group anagrams together using character frequency tuple keys.",
        "subheading": "Implement and verify Equivalence Hashing in the interactive workspace.",
        "task": {
            "title": "Group anagrams together using character frequency tuple keys.",
            "instructions": [
                "Group anagrams together using character frequency tuple keys.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "from collections import defaultdict\n\ndef group_anagrams(strs: list[str]) -> list[list[str]]:\n    ans = defaultdict(list)\n    # TODO: For each word, compute 26-tuple of character counts, use as dict key, append word\n    return sorted([sorted(g) for g in ans.values()])\n\nwords = ['eat', 'tea', 'tan', 'ate', 'nat', 'bat']\nprint('Grouped:', group_anagrams(words))\n",
            "solutionCode": "from collections import defaultdict\n\ndef group_anagrams(strs: list[str]) -> list[list[str]]:\n    ans = defaultdict(list)\n    for s in strs:\n        count = [0] * 26\n        for ch in s:\n            count[ord(ch) - ord('a')] += 1\n        ans[tuple(count)].append(s)\n    return sorted([sorted(g) for g in ans.values()])\n\nwords = ['eat', 'tea', 'tan', 'ate', 'nat', 'bat']\nprint('Grouped:', group_anagrams(words))\n",
            "expectedOutputPatterns": [
                "Grouped: [['ate', 'eat', 'tea'], ['bat'], ['nat', 'tan']]"
            ],
            "hint": "Initialize count = [0] * 26. Loop ch in s: count[ord(ch) - 97] += 1. Use ans[tuple(count)].append(s)."
        },
        "keyTakeaway": "Successfully implemented and verified Equivalence Hashing!"
    },
    {
        "id": "day70-step5",
        "stepNumber": 5,
        "title": "Day 70 Complete: Grouping & Canonical Equivalence Keys",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 70,
        "heading": "Mastery Achieved: Grouping & Canonical Equivalence Keys",
        "subheading": "You have solidified key mental models and techniques for Equivalence Hashing.",
        "recapRows": [
            {
                "concept": "Canonical Signatures",
                "naiveIntuition": "Compare every word with every other word O(N^2)",
                "pythonReality": "Transforming each word into its canonical signature groups matching words in a single O(N) hash pass"
            },
            {
                "concept": "Tuple Hashability",
                "naiveIntuition": "Convert count array to string key",
                "pythonReality": "tuple(count) is directly hashable in C, avoiding string formatting allocations"
            }
        ],
        "solidifiedConcepts": [
            "Canonical Representation Tuple",
            "Multi-Element Grouping"
        ],
        "nextDayPreview": {
            "dayNumber": 71,
            "title": "Hash Sets for O(1) Consecutive Sequences",
            "description": "Find the longest consecutive integer sequence in unsorted arrays in O(N) time using O(1) hash set lookups."
        }
    }
]
},
  71: {
  "dayNumber": 71,
  "title": "Hash Sets for O(1) Consecutive Sequences",
  "topicName": "Sequence Hashing",
  "sectionId": "hashing-and-hash-tables",
  "estimatedMinutes": 35,
  "difficulty": "DEVELOPING",
  "prerequisites": [
    17,
    70
  ],
  "concepts": [
    "Sequence Start Verification (num - 1)",
    "O(1) Set Membership Streak"
  ],
  "practiceSkills": [
    "Sequence Hashing Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Identify sequence heads by checking absence of (num - 1) in a hash set",
    "Find the Longest Consecutive Sequence in an unsorted array in strict O(N) time"
  ],
  "practiceArchetype": "problem",
  "flowTier": "tier2"
,
  "steps": [
    {
        "id": "day71-step1",
        "stepNumber": 1,
        "title": "Hash Sets for O(1) Consecutive Sequences: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Sequence Hashing",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Sequence Hashing.",
        "markdownContent": [
            "Hash Sets enable O(1) membership lookups to find the Longest Consecutive Sequence in an unsorted array in linear O(N) time.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Sequence Hashing**, remember the central principle: Checking that num - 1 is absent ensures each element is visited at most twice, guaranteeing O(N) time."
        ],
        "snippets": [
            {
                "title": "Sequence Hashing Implementation Template",
                "code": "# Longest Consecutive Sequence in O(N)\ndef longest_consecutive(nums):\n    s = set(nums)\n    best = 0\n    for x in s:\n        if (x - 1) not in s: # Sequence start!\n            curr = x\n            streak = 1\n            while (curr + 1) in s:\n                curr += 1; streak += 1\n            best = max(best, streak)\n    return best",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Checking that num - 1 is absent ensures each element is visited at most twice, guaranteeing O(N) time."
    },
    {
        "id": "day71-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Sequence Hashing",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Insert all numbers into a set. Only attempt to build sequences from sequence starts: if (num - 1) is NOT in the set, num is a sequence head! Loop while (num + streak) in set.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Checking that num - 1 is absent ensures each element is visited at most twice, guaranteeing O(N) time.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Sequence Hashing Core Invariant",
                "content": "Checking that num - 1 is absent ensures each element is visited at most twice, guaranteeing O(N) time."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Checking that num - 1 is absent ensures each element is visited at most twice, guaranteeing O(N) time."
    },
    {
        "id": "day71-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Sequence Hashing",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d71-q1",
                "question": "Why is the condition `if (x - 1) not in num_set` critical for achieving O(N) time?",
                "options": [
                    {
                        "id": "A",
                        "label": "It guarantees that the inner while loop only executes for numbers that start a sequence, ensuring each number is visited at most twice overall"
                    },
                    {
                        "id": "B",
                        "label": "It prevents searching for negative numbers"
                    },
                    {
                        "id": "C",
                        "label": "To sort the set in ascending order"
                    },
                    {
                        "id": "D",
                        "label": "To avoid infinite loops"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! If we looped from every number, an array [1, 2, 3, 4, 5] would do 5 + 4 + 3 + 2 + 1 = O(N^2) work. By only starting from sequence heads (where x-1 is missing), each number is traversed exactly once.",
                    "B": "Incorrect: Negative numbers are valid sequence members.",
                    "C": "Incorrect: Sets are unordered.",
                    "D": "Incorrect: Finite numbers cannot create infinite streaks."
                }
            },
            {
                "id": "chk-d71-q2",
                "question": "What is the time complexity of inserting all N array elements into a Python set?",
                "options": [
                    {
                        "id": "A",
                        "label": "O(N) average time"
                    },
                    {
                        "id": "B",
                        "label": "O(N log N)"
                    },
                    {
                        "id": "C",
                        "label": "O(1)"
                    },
                    {
                        "id": "D",
                        "label": "O(N^2)"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Each of the N set insertions takes O(1) average time. Building the initial set takes O(N) time.",
                    "B": "Incorrect: Trees take O(N log N); hash sets take O(N).",
                    "C": "Incorrect: O(1) is the cost per element, not for all N.",
                    "D": "Incorrect: Quadratic only under catastrophic pathological collisions."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day71-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Sequence Hashing",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Find the length of the longest consecutive elements sequence in an unsorted array.",
        "subheading": "Implement and verify Sequence Hashing in the interactive workspace.",
        "task": {
            "title": "Find the length of the longest consecutive elements sequence in an unsorted array.",
            "instructions": [
                "Find the length of the longest consecutive elements sequence in an unsorted array.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "def longest_consecutive(nums: list[int]) -> int:\n    if not nums:\n        return 0\n    num_set = set(nums)\n    max_streak = 0\n    # TODO: Iterate num_set, check if num - 1 is not in set (start of streak), count length\n    \n    return max_streak\n\nnums = [100, 4, 200, 1, 3, 2]\nprint('Longest consecutive streak:', longest_consecutive(nums))\n",
            "solutionCode": "def longest_consecutive(nums: list[int]) -> int:\n    if not nums:\n        return 0\n    num_set = set(nums)\n    max_streak = 0\n    for x in num_set:\n        if (x - 1) not in num_set:\n            curr = x\n            streak = 1\n            while (curr + 1) in num_set:\n                curr += 1\n                streak += 1\n            if streak > max_streak:\n                max_streak = streak\n    return max_streak\n\nnums = [100, 4, 200, 1, 3, 2]\nprint('Longest consecutive streak:', longest_consecutive(nums))\n",
            "expectedOutputPatterns": [
                "Longest consecutive streak: 4"
            ],
            "hint": "Convert nums to set. Loop x in num_set: if (x - 1) not in num_set: count streak with while (curr + 1) in num_set. Update max_streak."
        },
        "keyTakeaway": "Successfully implemented and verified Sequence Hashing!"
    },
    {
        "id": "day71-step5",
        "stepNumber": 5,
        "title": "Day 71 Complete: Hash Sets for O(1) Consecutive Sequences",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 71,
        "heading": "Mastery Achieved: Hash Sets for O(1) Consecutive Sequences",
        "subheading": "You have solidified key mental models and techniques for Sequence Hashing.",
        "recapRows": [
            {
                "concept": "Sequence Head Invariant",
                "naiveIntuition": "Sort array in O(N log N)",
                "pythonReality": "Filtering on sequence heads (x - 1 not in set) achieves strictly linear O(N) runtime"
            },
            {
                "concept": "Set Deduping",
                "naiveIntuition": "Duplicates extend sequence length",
                "pythonReality": "set(nums) naturally deduplicates elements so [1, 2, 2, 3] cleanly produces streak of 3"
            }
        ],
        "solidifiedConcepts": [
            "Sequence Start Verification (num - 1)",
            "O(1) Set Membership Streak"
        ],
        "nextDayPreview": {
            "dayNumber": 72,
            "title": "Rolling Hash & Rabin-Karp Substring Search",
            "description": "Implement polynomial rolling hashes and the Rabin-Karp algorithm for average O(N + M) substring matching."
        }
    }
]
},
  72: {
  "dayNumber": 72,
  "title": "Rolling Hash & Rabin-Karp Substring Search",
  "topicName": "Rolling Hash",
  "sectionId": "hashing-and-hash-tables",
  "estimatedMinutes": 45,
  "difficulty": "DEVELOPING",
  "prerequisites": [
    45,
    66
  ],
  "concepts": [
    "Polynomial Rolling Hash Formula",
    "Spurious Hit Spurious Verification"
  ],
  "practiceSkills": [
    "Rolling Hash Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Implement the polynomial rolling hash window slide formula in O(1) update time",
    "Execute the Rabin-Karp substring search algorithm with prime modulo hashing"
  ],
  "practiceArchetype": "algorithm",
  "flowTier": "tier3"
,
  "steps": [
    {
        "id": "day72-step1",
        "stepNumber": 1,
        "title": "Rolling Hash & Rabin-Karp Substring Search: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Rolling Hash",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Rolling Hash.",
        "markdownContent": [
            "Rabin-Karp Substring Search uses polynomial rolling hashes to find patterns in average O(N + M) time, updating window hashes in O(1) time without re-hashing.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Rolling Hash**, remember the central principle: Rolling hashes slide across strings in O(1) arithmetic updates per step, matching patterns in linear average time."
        ],
        "snippets": [
            {
                "title": "Rolling Hash Implementation Template",
                "code": "# Rabin-Karp Rolling Hash update\n# new_hash = ((old_hash - old_char * high_base) * base + new_char) % MOD",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Rolling hashes slide across strings in O(1) arithmetic updates per step, matching patterns in linear average time."
    },
    {
        "id": "day72-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Rolling Hash",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Hash formula: H = (H_prev - s[i - M] * base^(M-1)) * base + s[i]. If window hash matches pattern hash, verify character equality to eliminate spurious hash collisions.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Rolling hashes slide across strings in O(1) arithmetic updates per step, matching patterns in linear average time.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Rolling Hash Core Invariant",
                "content": "Rolling hashes slide across strings in O(1) arithmetic updates per step, matching patterns in linear average time."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Rolling hashes slide across strings in O(1) arithmetic updates per step, matching patterns in linear average time."
    },
    {
        "id": "day72-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Rolling Hash",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d72-q1",
                "question": "Why must the Rabin-Karp algorithm perform a character-by-character string comparison when window hash equals pattern hash?",
                "options": [
                    {
                        "id": "A",
                        "label": "To verify that the match is genuine and not a spurious collision where different strings produced identical hash values modulo M"
                    },
                    {
                        "id": "B",
                        "label": "Because Python hash values are always 0"
                    },
                    {
                        "id": "C",
                        "label": "To update the pattern hash"
                    },
                    {
                        "id": "D",
                        "label": "To reset the sliding window"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Because modulo operations map an infinite space of strings to finite integers, hash collisions (spurious hits) can occur. Direct verification guarantees correctness.",
                    "B": "Incorrect: Hashes are non-zero integers.",
                    "C": "Incorrect: The pattern hash is immutable.",
                    "D": "Incorrect: The window continues sliding normally."
                }
            },
            {
                "id": "chk-d72-q2",
                "question": "What is the worst-case time complexity of the Rabin-Karp algorithm under adversarial hash collisions?",
                "options": [
                    {
                        "id": "A",
                        "label": "O(N * M) when every window hash collides with the pattern hash"
                    },
                    {
                        "id": "B",
                        "label": "O(N + M)"
                    },
                    {
                        "id": "C",
                        "label": "O(log(N * M))"
                    },
                    {
                        "id": "D",
                        "label": "O(1)"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! If an adversary constructs strings where every window produces a spurious hash match, the algorithm performs N full M-character string comparisons: O(N * M).",
                    "B": "Incorrect: O(N + M) is the average case.",
                    "C": "Incorrect: String matching requires visiting text characters.",
                    "D": "Incorrect: Substring search requires examining the text."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day72-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Rolling Hash",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Implement Rabin-Karp substring search with rolling hash slide.",
        "subheading": "Implement and verify Rolling Hash in the interactive workspace.",
        "task": {
            "title": "Implement Rabin-Karp substring search with rolling hash slide.",
            "instructions": [
                "Implement Rabin-Karp substring search with rolling hash slide.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "def rabin_karp(text: str, pattern: str) -> int:\n    if not pattern:\n        return 0\n    if len(pattern) > len(text):\n        return -1\n    # TODO: Compute pattern hash and first text window hash\n    # Slide window in O(1) time and check equality on hash match\n    return -1\n\ntext = 'hello world'\nprint('Found pattern at index:', rabin_karp(text, 'world'))\n",
            "solutionCode": "def rabin_karp(text: str, pattern: str) -> int:\n    if not pattern:\n        return 0\n    if len(pattern) > len(text):\n        return -1\n    M, N = len(pattern), len(text)\n    BASE, MOD = 256, 10**9 + 7\n    h_pattern = 0\n    h_window = 0\n    power = 1\n    for i in range(M - 1):\n        power = (power * BASE) % MOD\n    for i in range(M):\n        h_pattern = (h_pattern * BASE + ord(pattern[i])) % MOD\n        h_window = (h_window * BASE + ord(text[i])) % MOD\n    for i in range(N - M + 1):\n        if h_pattern == h_window:\n            if text[i:i + M] == pattern:\n                return i\n        if i < N - M:\n            h_window = ((h_window - ord(text[i]) * power) * BASE + ord(text[i + M])) % MOD\n            if h_window < 0:\n                h_window += MOD\n    return -1\n\ntext = 'hello world'\nprint('Found pattern at index:', rabin_karp(text, 'world'))\n",
            "expectedOutputPatterns": [
                "Found pattern at index: 6"
            ],
            "hint": "Compute initial hashes using Horner's rule. On each slide, subtract `ord(text[i]) * power`, multiply by BASE, add `ord(text[i + M])`, and take `% MOD`."
        },
        "keyTakeaway": "Successfully implemented and verified Rolling Hash!"
    },
    {
        "id": "day72-step5",
        "stepNumber": 5,
        "title": "Day 72 Complete: Rolling Hash & Rabin-Karp Substring Search",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 72,
        "heading": "Mastery Achieved: Rolling Hash & Rabin-Karp Substring Search",
        "subheading": "You have solidified key mental models and techniques for Rolling Hash.",
        "recapRows": [
            {
                "concept": "O(1) Rolling Update",
                "naiveIntuition": "Recompute hash from scratch in O(M)",
                "pythonReality": "Subtracting old leading character and adding new trailing character updates hash in O(1) arithmetic"
            },
            {
                "concept": "Spurious Verification",
                "naiveIntuition": "Hash match guarantees string match",
                "pythonReality": "Modulo collisions mean two different strings can share a hash; verify text[i:i+M] == pattern"
            }
        ],
        "solidifiedConcepts": [
            "Polynomial Rolling Hash Formula",
            "Spurious Hit Spurious Verification"
        ],
        "nextDayPreview": {
            "dayNumber": 73,
            "title": "LRU Cache Architecture via OrderedDict",
            "description": "Build an O(1) Least Recently Used (LRU) Cache utilizing collections.OrderedDict as an introductory bridge."
        }
    }
]
},
  73: {
  "dayNumber": 73,
  "title": "LRU Cache Architecture via OrderedDict",
  "topicName": "OrderedDict LRU",
  "sectionId": "hashing-and-hash-tables",
  "estimatedMinutes": 35,
  "difficulty": "DEVELOPING",
  "prerequisites": [
    18,
    67
  ],
  "concepts": [
    "Doubly Linked Hash Table Concept",
    "O(1) Move-to-End Eviction"
  ],
  "practiceSkills": [
    "OrderedDict LRU Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Implement an LRU Cache in O(1) time using Python's collections.OrderedDict",
    "Manage key eviction policies under fixed capacity limits"
  ],
  "practiceArchetype": "algorithm",
  "flowTier": "tier2"
,
  "steps": [
    {
        "id": "day73-step1",
        "stepNumber": 1,
        "title": "LRU Cache Architecture via OrderedDict: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: OrderedDict LRU",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for OrderedDict LRU.",
        "markdownContent": [
            "LRU (Least Recently Used) Cache evicts the item that has not been accessed for the longest period when capacity is exceeded, implementable in O(1) via collections.OrderedDict.",
            "### Foundational Mental Model\nWhen approaching problems requiring **OrderedDict LRU**, remember the central principle: OrderedDict combines hash map lookup with doubly linked list ordering to achieve strict O(1) LRU caching."
        ],
        "snippets": [
            {
                "title": "OrderedDict LRU Implementation Template",
                "code": "# LRU Cache using collections.OrderedDict\nfrom collections import OrderedDict\nclass LRUCache:\n    def __init__(self, capacity):\n        self.cap = capacity\n        self.cache = OrderedDict()\n    def get(self, key):\n        if key not in self.cache: return -1\n        self.cache.move_to_end(key)\n        return self.cache[key]\n    def put(self, key, value):\n        if key in self.cache: self.cache.move_to_end(key)\n        self.cache[key] = value\n        if len(self.cache) > self.cap: self.cache.popitem(last=False)",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "OrderedDict combines hash map lookup with doubly linked list ordering to achieve strict O(1) LRU caching."
    },
    {
        "id": "day73-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: OrderedDict LRU",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "get(key): if key in cache, move to end (mark recent) and return value. put(key, value): if exists, update and move to end. If new and len == capacity, popitem(last=False) evicts oldest.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: OrderedDict combines hash map lookup with doubly linked list ordering to achieve strict O(1) LRU caching.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "OrderedDict LRU Core Invariant",
                "content": "OrderedDict combines hash map lookup with doubly linked list ordering to achieve strict O(1) LRU caching."
            }
        ],
        "keyTakeaway": "Operational invariant locked: OrderedDict combines hash map lookup with doubly linked list ordering to achieve strict O(1) LRU caching."
    },
    {
        "id": "day73-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: OrderedDict LRU",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d73-q1",
                "question": "What does `popitem(last=False)` do in Python's `collections.OrderedDict`?",
                "options": [
                    {
                        "id": "A",
                        "label": "Removes and returns the first (oldest / least recently used) key-value pair in O(1) time"
                    },
                    {
                        "id": "B",
                        "label": "Removes the newest item added to the dictionary"
                    },
                    {
                        "id": "C",
                        "label": "Wipes the entire dictionary"
                    },
                    {
                        "id": "D",
                        "label": "Sorts the dictionary in reverse order"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! `last=False` specifies FIFO eviction (head of the doubly linked list), removing the least recently used element.",
                    "B": "Incorrect: `last=True` (default) removes the newest LIFO item.",
                    "C": "Incorrect: popitem removes a single item.",
                    "D": "Incorrect: No sorting is performed."
                }
            },
            {
                "id": "chk-d73-q2",
                "question": "What are the time complexities of `get()` and `put()` in a correctly implemented LRU Cache?",
                "options": [
                    {
                        "id": "A",
                        "label": "Both get() and put() run in strict O(1) time"
                    },
                    {
                        "id": "B",
                        "label": "get() is O(1), but put() is O(N)"
                    },
                    {
                        "id": "C",
                        "label": "Both run in O(log N) time"
                    },
                    {
                        "id": "D",
                        "label": "Both run in O(N) time"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Hash map provides O(1) key node lookup, and the doubly linked list provides O(1) pointer detachment and head/tail insertion.",
                    "B": "Incorrect: put() operates in O(1) time.",
                    "C": "Incorrect: No tree structures are used.",
                    "D": "Incorrect: O(N) is unacceptable for production caches."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day73-step4",
        "stepNumber": 4,
        "title": "Guided Practice: OrderedDict LRU",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Implement an LRU Cache using collections.OrderedDict.",
        "subheading": "Implement and verify OrderedDict LRU in the interactive workspace.",
        "task": {
            "title": "Implement an LRU Cache using collections.OrderedDict.",
            "instructions": [
                "Implement an LRU Cache using collections.OrderedDict.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "from collections import OrderedDict\n\nclass LRUCache:\n    def __init__(self, capacity: int):\n        # TODO: Initialize capacity and OrderedDict storage\n        pass\n\n    def get(self, key: int) -> int:\n        # TODO: If key exists, move_to_end and return value; else return -1\n        return -1\n\n    def put(self, key: int, value: int) -> None:\n        # TODO: Update or insert key; if over capacity, popitem(last=False)\n        pass\n\nlru = LRUCache(2)\nlru.put(1, 1)\nlru.put(2, 2)\nprint('Get key 1:', lru.get(1))  # 1 (moves key 1 to recent)\nlru.put(3, 3)                     # Evicts key 2!\nprint('Get key 2:', lru.get(2))  # -1 (evicted)\n",
            "solutionCode": "from collections import OrderedDict\n\nclass LRUCache:\n    def __init__(self, capacity: int):\n        self.capacity = capacity\n        self.cache = OrderedDict()\n\n    def get(self, key: int) -> int:\n        if key not in self.cache:\n            return -1\n        self.cache.move_to_end(key)\n        return self.cache[key]\n\n    def put(self, key: int, value: int) -> None:\n        if key in self.cache:\n            self.cache.move_to_end(key)\n        self.cache[key] = value\n        if len(self.cache) > self.capacity:\n            self.cache.popitem(last=False)\n\nlru = LRUCache(2)\nlru.put(1, 1)\nlru.put(2, 2)\nprint('Get key 1:', lru.get(1))\nlru.put(3, 3)\nprint('Get key 2:', lru.get(2))\n",
            "expectedOutputPatterns": [
                "Get key 1: 1",
                "Get key 2: -1"
            ],
            "hint": "In get: if key in self.cache: self.cache.move_to_end(key); return self.cache[key]. In put: check key, assign, and if len > capacity: self.cache.popitem(last=False)."
        },
        "keyTakeaway": "Successfully implemented and verified OrderedDict LRU!"
    },
    {
        "id": "day73-step5",
        "stepNumber": 5,
        "title": "Day 73 Complete: LRU Cache Architecture via OrderedDict",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 73,
        "heading": "Mastery Achieved: LRU Cache Architecture via OrderedDict",
        "subheading": "You have solidified key mental models and techniques for OrderedDict LRU.",
        "recapRows": [
            {
                "concept": "Dual Data Structure",
                "naiveIntuition": "A hash map alone is sufficient for LRU",
                "pythonReality": "Hash maps have no inherent access recency ordering; pairing with a doubly linked list provides O(1) order manipulation"
            },
            {
                "concept": "Access as Mutation",
                "naiveIntuition": "get() is a read-only operation",
                "pythonReality": "In an LRU cache, get() mutates the access order, promoting the accessed key to the most recent position"
            }
        ],
        "solidifiedConcepts": [
            "Doubly Linked Hash Table Concept",
            "O(1) Move-to-End Eviction"
        ],
        "nextDayPreview": {
            "dayNumber": 74,
            "title": "LFU Cache Design Principles",
            "description": "Architect an O(1) Least Frequently Used (LFU) cache using nested frequency buckets and reciprocal pointers."
        }
    }
]
},
  74: {
  "dayNumber": 74,
  "title": "LFU Cache Design Principles",
  "topicName": "LFU Cache",
  "sectionId": "hashing-and-hash-tables",
  "estimatedMinutes": 45,
  "difficulty": "DEVELOPING",
  "prerequisites": [
    73
  ],
  "concepts": [
    "Frequency Bucket Doubly Linked Lists",
    "Min-Frequency Pointer Invariant"
  ],
  "practiceSkills": [
    "LFU Cache Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Design an LFU cache tracking access frequencies and secondary recency orders",
    "Maintain min_freq tracking in O(1) time across get and put operations"
  ],
  "practiceArchetype": "milestone",
  "flowTier": "tier3"
,
  "steps": [
    {
        "id": "day74-step1",
        "stepNumber": 1,
        "title": "LFU Cache Design Principles: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: LFU Cache",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for LFU Cache.",
        "markdownContent": [
            "LFU (Least Frequently Used) Cache evicts the element with the lowest access count, tie-breaking by least recently used, operating in strict O(1) time.",
            "### Foundational Mental Model\nWhen approaching problems requiring **LFU Cache**, remember the central principle: LFU requires two synchronized hash maps: key-to-node and frequency-to-doubly-linked-list."
        ],
        "snippets": [
            {
                "title": "LFU Cache Implementation Template",
                "code": "# LFU Cache architecture\n# key_to_node: key -> Node(key, val, freq)\n# freq_to_dll: freq -> DoublyLinkedList()\n# min_freq tracks lowest active frequency",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "LFU requires two synchronized hash maps: key-to-node and frequency-to-doubly-linked-list."
    },
    {
        "id": "day74-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: LFU Cache",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Maintain a key-to-node map and a frequency-to-DLL map. Track min_freq. When get/put increments a key's count, detach from freq_map[f] and insert into freq_map[f+1]. Update min_freq in O(1).",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: LFU requires two synchronized hash maps: key-to-node and frequency-to-doubly-linked-list.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "LFU Cache Core Invariant",
                "content": "LFU requires two synchronized hash maps: key-to-node and frequency-to-doubly-linked-list."
            }
        ],
        "keyTakeaway": "Operational invariant locked: LFU requires two synchronized hash maps: key-to-node and frequency-to-doubly-linked-list."
    },
    {
        "id": "day74-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: LFU Cache",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d74-q1",
                "question": "Why does an LFU Cache require tracking `min_freq` as a separate state variable?",
                "options": [
                    {
                        "id": "A",
                        "label": "To evict the least frequently used key in strict O(1) time without scanning all frequency buckets"
                    },
                    {
                        "id": "B",
                        "label": "To prevent keys from having frequency 0"
                    },
                    {
                        "id": "C",
                        "label": "Because Python dictionaries cannot store frequencies"
                    },
                    {
                        "id": "D",
                        "label": "To limit the maximum cache size"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! When capacity is exceeded, eviction occurs from `freq_to_dll[min_freq]`. Tracking `min_freq` allows immediate O(1) access to the lowest-frequency bucket.",
                    "B": "Incorrect: Initial frequency is 1.",
                    "C": "Incorrect: Dictionaries can store any integers.",
                    "D": "Incorrect: Capacity limits cache size."
                }
            },
            {
                "id": "chk-d74-q2",
                "question": "When an existing key's frequency increments from F to F+1, under what condition does `min_freq` increment by 1?",
                "options": [
                    {
                        "id": "A",
                        "label": "When min_freq == F and the frequency bucket F becomes completely empty after the key is moved"
                    },
                    {
                        "id": "B",
                        "label": "On every single get() operation unconditionally"
                    },
                    {
                        "id": "C",
                        "label": "Only when a new key is inserted"
                    },
                    {
                        "id": "D",
                        "label": "Whenever F is an even number"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! If the moved key was the ONLY key in bucket `min_freq`, that frequency bucket is now empty, so the new minimum active frequency must be F + 1.",
                    "B": "Incorrect: Other keys might remain at frequency F.",
                    "C": "Incorrect: New keys reset `min_freq` to 1.",
                    "D": "Incorrect: Parity has no effect on frequency logic."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day74-step4",
        "stepNumber": 4,
        "title": "Guided Practice: LFU Cache",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Design the frequency promotion step of an LFU Cache.",
        "subheading": "Implement and verify LFU Cache in the interactive workspace.",
        "task": {
            "title": "Design the frequency promotion step of an LFU Cache.",
            "instructions": [
                "Design the frequency promotion step of an LFU Cache.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "# Day 74 Milestone: LFU Frequency Promotion Engine\nclass LFUSimulator:\n    def __init__(self):\n        self.key_freq = {}\n        self.freq_keys = {} # freq -> list of keys\n        self.min_freq = 0\n\n    def access(self, key: str) -> None:\n        # TODO: Increment key frequency, update freq_keys buckets and min_freq\n        pass\n\nlfu = LFUSimulator()\nlfu.access('A')\nlfu.access('B')\nlfu.access('A') # 'A' has freq 2, 'B' has freq 1\nprint('Min freq:', lfu.min_freq)\nprint('Keys at min freq:', lfu.freq_keys[lfu.min_freq])\n",
            "solutionCode": "class LFUSimulator:\n    def __init__(self):\n        self.key_freq = {}\n        self.freq_keys = {}\n        self.min_freq = 0\n\n    def access(self, key: str) -> None:\n        if key not in self.key_freq:\n            self.key_freq[key] = 1\n            self.freq_keys.setdefault(1, []).append(key)\n            self.min_freq = 1\n        else:\n            old_f = self.key_freq[key]\n            new_f = old_f + 1\n            self.key_freq[key] = new_f\n            self.freq_keys[old_f].remove(key)\n            self.freq_keys.setdefault(new_f, []).append(key)\n            if self.min_freq == old_f and not self.freq_keys[old_f]:\n                self.min_freq = new_f\n\nlfu = LFUSimulator()\nlfu.access('A')\nlfu.access('B')\nlfu.access('A')\nprint('Min freq:', lfu.min_freq)\nprint('Keys at min freq:', lfu.freq_keys[lfu.min_freq])\n",
            "expectedOutputPatterns": [
                "Min freq: 1",
                "Keys at min freq: ['B']"
            ],
            "hint": "If key exists: old_f = key_freq[key], key_freq[key] = old_f + 1, move from freq_keys[old_f] to freq_keys[old_f + 1]. If old_f was min_freq and is now empty: min_freq += 1."
        },
        "keyTakeaway": "Successfully implemented and verified LFU Cache!"
    },
    {
        "id": "day74-step5",
        "stepNumber": 5,
        "title": "Day 74 Complete: LFU Cache Design Principles",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 74,
        "heading": "Mastery Achieved: LFU Cache Design Principles",
        "subheading": "You have solidified key mental models and techniques for LFU Cache.",
        "recapRows": [
            {
                "concept": "Frequency Bucketing",
                "naiveIntuition": "Sort cache by frequency on eviction O(N log N)",
                "pythonReality": "Grouping keys into doubly linked lists by frequency enables O(1) promotions and evictions"
            },
            {
                "concept": "LRU Tie-Breaker",
                "naiveIntuition": "Any key with min_freq can be dropped",
                "pythonReality": "When multiple keys share the minimum frequency, the least recently used key among them is evicted"
            }
        ],
        "solidifiedConcepts": [
            "Frequency Bucket Doubly Linked Lists",
            "Min-Frequency Pointer Invariant"
        ],
        "nextDayPreview": {
            "dayNumber": 75,
            "title": "Section 6 Review & Hashing Mastery",
            "description": "Synthesize hash maps, hash sets, rolling hashes, and cache architectures into a complete caching engine."
        }
    }
]
},
  75: {
  "dayNumber": 75,
  "title": "Section 6 Review & Hashing Mastery",
  "topicName": "Hashing Milestone",
  "sectionId": "hashing-and-hash-tables",
  "estimatedMinutes": 40,
  "difficulty": "DEVELOPING",
  "prerequisites": [
    67,
    69,
    70,
    71,
    72,
    73
  ],
  "concepts": [
    "Hash Table Architectural Trade-offs",
    "Collision Resistance",
    "Cache Policy Integration"
  ],
  "practiceSkills": [
    "Hashing Milestone Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Evaluate hash table designs under adversarial collision attack scenarios",
    "Synthesize hash tables and sliding windows into an optimal streaming lookup pipeline"
  ],
  "practiceArchetype": "milestone",
  "flowTier": "tier2"
,
  "steps": [
    {
        "id": "day75-step1",
        "stepNumber": 1,
        "title": "Section 6 Review & Hashing Mastery: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Hashing Milestone",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Hashing Milestone.",
        "markdownContent": [
            "Section 6 Review synthesizes hash functions, collision resolution, frequency mapping, rolling hashes, and cache eviction architectures into a collision-resistant caching system.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Hashing Milestone**, remember the central principle: Hash tables trade memory overhead for O(1) average access, powering caching and indexing across all software tiers."
        ],
        "snippets": [
            {
                "title": "Hashing Milestone Implementation Template",
                "code": "# Cache Eviction and Hash Table Synthesis\n# Load factor alpha = N / M. Keep alpha <= 0.66",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Hash tables trade memory overhead for O(1) average access, powering caching and indexing across all software tiers."
    },
    {
        "id": "day75-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Hashing Milestone",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Evaluate hash table trade-offs: open addressing maximizes cache locality for small records; separate chaining avoids clustering and deletion tombstone overhead. Rolling hashes accelerate string search.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Hash tables trade memory overhead for O(1) average access, powering caching and indexing across all software tiers.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Hashing Milestone Core Invariant",
                "content": "Hash tables trade memory overhead for O(1) average access, powering caching and indexing across all software tiers."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Hash tables trade memory overhead for O(1) average access, powering caching and indexing across all software tiers."
    },
    {
        "id": "day75-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Hashing Milestone",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d75-q1",
                "question": "What is the primary advantage of Open Addressing over Separate Chaining in hardware performance?",
                "options": [
                    {
                        "id": "A",
                        "label": "Open addressing stores all elements in a single contiguous array, exhibiting superior CPU cache line locality without pointer chasing"
                    },
                    {
                        "id": "B",
                        "label": "Open addressing can never become full"
                    },
                    {
                        "id": "C",
                        "label": "Open addressing avoids the need for hash functions"
                    },
                    {
                        "id": "D",
                        "label": "Open addressing runs in O(0) time"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Because all keys and values reside directly in contiguous slots, linear probing sweeps contiguous cache lines, drastically reducing memory bus latency compared to linked list pointers.",
                    "B": "Incorrect: Open addressing tables CAN become 100% full.",
                    "C": "Incorrect: Both techniques require hash functions.",
                    "D": "Incorrect: Sub-O(1) complexity does not exist."
                }
            },
            {
                "id": "chk-d75-q2",
                "question": "In interview problems, when should you choose a Hash Set over a Boolean Array?",
                "options": [
                    {
                        "id": "A",
                        "label": "When the domain of keys is sparse or unbounded (e.g. arbitrary strings, coordinates, or integers up to 10^9)"
                    },
                    {
                        "id": "B",
                        "label": "When all keys are integers from 0 to 25"
                    },
                    {
                        "id": "C",
                        "label": "When memory is severely limited to a few bytes"
                    },
                    {
                        "id": "D",
                        "label": "When keys must be kept sorted"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! If keys span huge or non-integer ranges, allocating a boolean array of 10^9 elements is impossible. A hash set dynamically stores only the active N keys.",
                    "B": "Incorrect: Bounded ranges [0..25] are faster with a fixed boolean array.",
                    "C": "Incorrect: Hash sets have pointer and table overhead.",
                    "D": "Incorrect: Sets are unordered; use trees for sorted keys."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day75-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Hashing Milestone",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Build a collision-resistant Deduplication Filter with load factor monitoring.",
        "subheading": "Implement and verify Hashing Milestone in the interactive workspace.",
        "task": {
            "title": "Build a collision-resistant Deduplication Filter with load factor monitoring.",
            "instructions": [
                "Build a collision-resistant Deduplication Filter with load factor monitoring.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "class DeduplicationFilter:\n    def __init__(self, capacity: int = 5):\n        self.capacity = capacity\n        self.buckets = [[] for _ in range(capacity)]\n        self.count = 0\n\n    def add(self, item: str) -> bool:\n        # TODO: Return False if item already exists\n        # Otherwise add item, increment count, and return True\n        return False\n\n    def load_factor(self) -> float:\n        return self.count / self.capacity\n\ndedup = DeduplicationFilter(5)\nprint('Add alpha:', dedup.add('alpha'))\nprint('Add beta:', dedup.add('beta'))\nprint('Add alpha again:', dedup.add('alpha'))\nprint('Load factor:', dedup.load_factor())\n",
            "solutionCode": "class DeduplicationFilter:\n    def __init__(self, capacity: int = 5):\n        self.capacity = capacity\n        self.buckets = [[] for _ in range(capacity)]\n        self.count = 0\n\n    def add(self, item: str) -> bool:\n        b_idx = hash(item) % self.capacity\n        bucket = self.buckets[b_idx]\n        if item in bucket:\n            return False\n        bucket.append(item)\n        self.count += 1\n        return True\n\n    def load_factor(self) -> float:\n        return self.count / self.capacity\n\ndedup = DeduplicationFilter(5)\nprint('Add alpha:', dedup.add('alpha'))\nprint('Add beta:', dedup.add('beta'))\nprint('Add alpha again:', dedup.add('alpha'))\nprint('Load factor:', dedup.load_factor())\n",
            "expectedOutputPatterns": [
                "Add alpha: True",
                "Add beta: True",
                "Add alpha again: False",
                "Load factor: 0.4"
            ],
            "hint": "Compute b_idx = hash(item) % self.capacity. Check if item in self.buckets[b_idx]: if so return False. Else append, self.count += 1, and return True."
        },
        "keyTakeaway": "Successfully implemented and verified Hashing Milestone!"
    },
    {
        "id": "day75-step5",
        "stepNumber": 5,
        "title": "Day 75 Complete: Section 6 Review & Hashing Mastery",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 75,
        "heading": "Mastery Achieved: Section 6 Review & Hashing Mastery",
        "subheading": "You have solidified key mental models and techniques for Hashing Milestone.",
        "recapRows": [
            {
                "concept": "Load Factor Monitoring",
                "naiveIntuition": "Tables manage memory automatically",
                "pythonReality": "In custom data structures, tracking load_factor = N / capacity triggers doubling resizes before performance drops"
            },
            {
                "concept": "Section 6 Synthesis",
                "naiveIntuition": "Hash tables only store simple key-values",
                "pythonReality": "Hash maps power LRU/LFU caches, rolling hash algorithms, graph adjacency lists, and dynamic programming memo tables"
            }
        ],
        "solidifiedConcepts": [
            "Hash Table Architectural Trade-offs",
            "Collision Resistance",
            "Cache Policy Integration"
        ],
        "nextDayPreview": {
            "dayNumber": 76,
            "title": "Singly Linked List: Structure & Traversal",
            "description": "Define ListNode nodes, manage head references, traverse lists, and analyze non-contiguous heap allocations."
        }
    }
]
},
  76: {
  "dayNumber": 76,
  "title": "Singly Linked List: Structure & Traversal",
  "topicName": "Linked List Basics",
  "sectionId": "linked-lists",
  "estimatedMinutes": 30,
  "difficulty": "INTERMEDIATE",
  "prerequisites": [
    22,
    36
  ],
  "concepts": [
    "ListNode Pointer Reference",
    "Sequential Pointer Traversal"
  ],
  "practiceSkills": [
    "Linked List Basics Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Construct a custom ListNode class and traverse nodes until curr is None",
    "Contrast linked list dynamic pointer chains with contiguous array memory"
  ],
  "practiceArchetype": "guided",
  "flowTier": "tier1"
,
  "steps": [
    {
        "id": "day76-step1",
        "stepNumber": 1,
        "title": "Singly Linked List: Structure & Traversal: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Linked List Basics",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Linked List Basics.",
        "markdownContent": [
            "Singly Linked Lists chain individual ListNode objects via pointer references, trading array contiguous indexing for dynamic O(1) node insertion.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Linked List Basics**, remember the central principle: Linked lists eliminate contiguous array resizing overhead but forfeit O(1) random index access."
        ],
        "snippets": [
            {
                "title": "Linked List Basics Implementation Template",
                "code": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\nhead = ListNode(1, ListNode(2, ListNode(3)))\ncurr = head\nwhile curr:\n    print(curr.val, end=' -> ')\n    curr = curr.next\nprint('None')",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Linked lists eliminate contiguous array resizing overhead but forfeit O(1) random index access."
    },
    {
        "id": "day76-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Linked List Basics",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Each node stores val and a next pointer reference. Traversal proceeds sequentially via curr = curr.next until reaching None. Unlike contiguous Python lists, linked list nodes are scattered across arbitrary heap memory addresses.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Linked lists eliminate contiguous array resizing overhead but forfeit O(1) random index access.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Linked List Basics Core Invariant",
                "content": "Linked lists eliminate contiguous array resizing overhead but forfeit O(1) random index access."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Linked lists eliminate contiguous array resizing overhead but forfeit O(1) random index access."
    },
    {
        "id": "day76-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Linked List Basics",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d76-q1",
                "question": "What is the primary memory difference between a Python list and a singly linked list?",
                "options": [
                    {
                        "id": "A",
                        "label": "Python lists store contiguous arrays of memory pointers allowing O(1) indexing, whereas linked lists scatter nodes across heap memory connected via node.next references"
                    },
                    {
                        "id": "B",
                        "label": "Linked lists can only store strings while Python lists store numbers"
                    },
                    {
                        "id": "C",
                        "label": "Python lists consume zero memory when empty"
                    },
                    {
                        "id": "D",
                        "label": "Linked lists cannot be modified after creation"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Contiguous memory allows hardware ALUs to compute base + index * pointer_size in O(1) time. Linked lists require sequential pointer hopping (curr = curr.next) taking O(N) to reach index N.",
                    "B": "Incorrect: Both data structures can store any Python object.",
                    "C": "Incorrect: Python list objects have fixed struct overhead.",
                    "D": "Incorrect: Linked lists are mutable dynamic structures."
                }
            },
            {
                "id": "chk-d76-q2",
                "question": "What happens if a traversal loop executes curr = curr.next when curr is None?",
                "options": [
                    {
                        "id": "A",
                        "label": "Python raises AttributeError: 'NoneType' object has no attribute 'next'"
                    },
                    {
                        "id": "B",
                        "label": "The loop terminates cleanly"
                    },
                    {
                        "id": "C",
                        "label": "Python automatically resets curr back to head"
                    },
                    {
                        "id": "D",
                        "label": "A circular reference is formed"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Attempting to access an attribute on None immediately triggers an AttributeError. Guard loops with while curr:.",
                    "B": "Incorrect: Dereferencing None raises an exception.",
                    "C": "Incorrect: Python runtime does not infer head recovery.",
                    "D": "Incorrect: No pointers are redirected."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day76-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Linked List Basics",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Construct a linked list from an array of integers and return the values collected during traversal.",
        "subheading": "Implement and verify Linked List Basics in the interactive workspace.",
        "task": {
            "title": "Construct a linked list from an array of integers and return the values collected during traversal.",
            "instructions": [
                "Construct a linked list from an array of integers and return the values collected during traversal.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef build_and_traverse(values: list[int]) -> list[int]:\n    # TODO: Build singly linked list from values\n    # Traverse the list and collect all node.val into a result list\n    return []\n\nprint('Collected:', build_and_traverse([10, 20, 30, 40]))\n",
            "solutionCode": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef build_and_traverse(values: list[int]) -> list[int]:\n    if not values:\n        return []\n    head = ListNode(values[0])\n    curr = head\n    for v in values[1:]:\n        curr.next = ListNode(v)\n        curr = curr.next\n    \n    result = []\n    curr = head\n    while curr:\n        result.append(curr.val)\n        curr = curr.next\n    return result\n\nprint('Collected:', build_and_traverse([10, 20, 30, 40]))\n",
            "expectedOutputPatterns": [
                "Collected: [10, 20, 30, 40]"
            ],
            "hint": "Create head = ListNode(values[0]). Loop through remaining items, attach curr.next = ListNode(v), and advance curr = curr.next."
        },
        "keyTakeaway": "Successfully implemented and verified Linked List Basics!"
    },
    {
        "id": "day76-step5",
        "stepNumber": 5,
        "title": "Day 76 Complete: Singly Linked List: Structure & Traversal",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 76,
        "heading": "Mastery Achieved: Singly Linked List: Structure & Traversal",
        "subheading": "You have solidified key mental models and techniques for Linked List Basics.",
        "recapRows": [
            {
                "concept": "Pointer Sequentiality",
                "naiveIntuition": "Access node k with list[k]",
                "pythonReality": "Linked lists require sequential traversal through k next pointers in O(K) time"
            },
            {
                "concept": "Dynamic Allocation",
                "naiveIntuition": "Linked lists require continuous memory blocks",
                "pythonReality": "Nodes exist independently in heap memory, connected solely by reference pointers"
            }
        ],
        "solidifiedConcepts": [
            "ListNode Pointer Reference",
            "Sequential Pointer Traversal"
        ],
        "nextDayPreview": {
            "dayNumber": 77,
            "title": "Insertion, Deletion & Dummy Sentinels",
            "description": "Use dummy sentinel nodes to eliminate special cases when inserting or deleting nodes at list boundaries."
        }
    }
]
},
  77: {
  "dayNumber": 77,
  "title": "Insertion, Deletion & Dummy Sentinels",
  "topicName": "Sentinel Nodes",
  "sectionId": "linked-lists",
  "estimatedMinutes": 35,
  "difficulty": "INTERMEDIATE",
  "prerequisites": [
    76
  ],
  "concepts": [
    "Dummy Sentinel Head Node",
    "Predecessor Pointer Rewiring"
  ],
  "practiceSkills": [
    "Sentinel Nodes Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Eliminate head edge-case conditionals using a dummy sentinel node",
    "Insert and delete interior list nodes in O(1) pointer operations given predecessor"
  ],
  "practiceArchetype": "completion",
  "flowTier": "tier1"
,
  "steps": [
    {
        "id": "day77-step1",
        "stepNumber": 1,
        "title": "Insertion, Deletion & Dummy Sentinels: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Sentinel Nodes",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Sentinel Nodes.",
        "markdownContent": [
            "Insertion and Deletion in singly linked lists mutate .next pointers, with Dummy Sentinels (dummy = ListNode(0, head)) elegantly eliminating head edge cases.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Sentinel Nodes**, remember the central principle: Using a dummy head sentinel unifies edge-case operations at head, middle, and tail."
        ],
        "snippets": [
            {
                "title": "Sentinel Nodes Implementation Template",
                "code": "# Deleting target value with dummy sentinel\ndef remove_elements(head, target):\n    dummy = ListNode(0, head)\n    curr = dummy\n    while curr.next:\n        if curr.next.val == target:\n            curr.next = curr.next.next\n        else:\n            curr = curr.next\n    return dummy.next",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Using a dummy head sentinel unifies edge-case operations at head, middle, and tail."
    },
    {
        "id": "day77-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Sentinel Nodes",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Inserting after node curr requires: new_node.next = curr.next; curr.next = new_node. Deleting target after curr: curr.next = curr.next.next. Dummy sentinels prevent special-case branching when operating on index 0.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Using a dummy head sentinel unifies edge-case operations at head, middle, and tail.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Sentinel Nodes Core Invariant",
                "content": "Using a dummy head sentinel unifies edge-case operations at head, middle, and tail."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Using a dummy head sentinel unifies edge-case operations at head, middle, and tail."
    },
    {
        "id": "day77-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Sentinel Nodes",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d77-q1",
                "question": "Why does using a dummy node (dummy = ListNode(0, head)) simplify node deletion algorithms?",
                "options": [
                    {
                        "id": "A",
                        "label": "It guarantees that every node to be evaluated (including the original head) has a non-null predecessor node curr"
                    },
                    {
                        "id": "B",
                        "label": "It reduces the algorithmic time complexity from O(N) to O(1)"
                    },
                    {
                        "id": "C",
                        "label": "It prevents memory garbage collection"
                    },
                    {
                        "id": "D",
                        "label": "It automatically sorts the linked list"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Without a dummy node, deleting the head node requires distinct head = head.next branching. A dummy sentinel ensures every node has a preceding node curr such that curr.next = curr.next.next works uniformly.",
                    "B": "Incorrect: Traversal still requires O(N) time.",
                    "C": "Incorrect: Unreferenced deleted nodes are cleanly garbage-collected.",
                    "D": "Incorrect: Sentinels have no effect on element order."
                }
            },
            {
                "id": "chk-d77-q2",
                "question": "What is the critical order of operations when inserting new_node after curr?",
                "options": [
                    {
                        "id": "A",
                        "label": "Set new_node.next = curr.next FIRST, then set curr.next = new_node"
                    },
                    {
                        "id": "B",
                        "label": "Set curr.next = new_node FIRST, then set new_node.next = curr.next"
                    },
                    {
                        "id": "C",
                        "label": "Order does not matter in Python"
                    },
                    {
                        "id": "D",
                        "label": "Delete curr first"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! If you set curr.next = new_node first, you overwrite the reference to the subsequent nodes, permanently orphaning the rest of the list.",
                    "B": "Incorrect: This results in new_node.next = new_node, creating an infinite self-cycle and dropping remaining nodes.",
                    "C": "Incorrect: Reference assignment order is strictly sequential in imperative execution.",
                    "D": "Incorrect: Deleting curr destroys the insertion anchor."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day77-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Sentinel Nodes",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Use a dummy sentinel to delete all nodes matching a target value.",
        "subheading": "Implement and verify Sentinel Nodes in the interactive workspace.",
        "task": {
            "title": "Use a dummy sentinel to delete all nodes matching a target value.",
            "instructions": [
                "Use a dummy sentinel to delete all nodes matching a target value.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef remove_all_val(head: ListNode, target: int) -> list[int]:\n    # TODO: Initialize dummy = ListNode(0, head)\n    # Delete all nodes where node.val == target\n    # Return values of remaining list as a Python list\n    return []\n\n# 1 -> 2 -> 6 -> 3 -> 6 -> None (remove 6)\nh = ListNode(1, ListNode(2, ListNode(6, ListNode(3, ListNode(6)))))\nprint('Remaining:', remove_all_val(h, 6))\n",
            "solutionCode": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef remove_all_val(head: ListNode, target: int) -> list[int]:\n    dummy = ListNode(0, head)\n    curr = dummy\n    while curr.next:\n        if curr.next.val == target:\n            curr.next = curr.next.next\n        else:\n            curr = curr.next\n    \n    res = []\n    node = dummy.next\n    while node:\n        res.append(node.val)\n        node = node.next\n    return res\n\nh = ListNode(1, ListNode(2, ListNode(6, ListNode(3, ListNode(6)))))\nprint('Remaining:', remove_all_val(h, 6))\n",
            "expectedOutputPatterns": [
                "Remaining: [1, 2, 3]"
            ],
            "hint": "dummy = ListNode(0, head); curr = dummy. While curr.next: if curr.next.val == target: curr.next = curr.next.next else: curr = curr.next. Return traversed dummy.next."
        },
        "keyTakeaway": "Successfully implemented and verified Sentinel Nodes!"
    },
    {
        "id": "day77-step5",
        "stepNumber": 5,
        "title": "Day 77 Complete: Insertion, Deletion & Dummy Sentinels",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 77,
        "heading": "Mastery Achieved: Insertion, Deletion & Dummy Sentinels",
        "subheading": "You have solidified key mental models and techniques for Sentinel Nodes.",
        "recapRows": [
            {
                "concept": "Sentinel Utility",
                "naiveIntuition": "Handle head deletion with if head.val == target: head = head.next",
                "pythonReality": "Dummy nodes eliminate repetitive edge-case branches by guaranteeing every active node has a valid predecessor"
            },
            {
                "concept": "Unlinking Garbage Collection",
                "naiveIntuition": "Deleted nodes remain in memory forever",
                "pythonReality": "In CPython, reference count drops to 0 when unlinked, automatically freeing memory"
            }
        ],
        "solidifiedConcepts": [
            "Dummy Sentinel Head Node",
            "Predecessor Pointer Rewiring"
        ],
        "nextDayPreview": {
            "dayNumber": 78,
            "title": "In-Place Linked List Pointer Reversal",
            "description": "Reverse singly linked lists iteratively in O(N) time and O(1) space using three pointers (prev, curr, next_node)."
        }
    }
]
},
  78: {
  "dayNumber": 78,
  "title": "In-Place Linked List Pointer Reversal",
  "topicName": "List Reversal",
  "sectionId": "linked-lists",
  "estimatedMinutes": 35,
  "difficulty": "INTERMEDIATE",
  "prerequisites": [
    77
  ],
  "concepts": [
    "Three-Pointer Iterative Reversal",
    "next_node Forward Caching"
  ],
  "practiceSkills": [
    "List Reversal Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Cache forward references in next_node before mutating curr.next to prev",
    "Reverse a singly linked list in-place in O(N) time and O(1) space"
  ],
  "practiceArchetype": "debugging",
  "flowTier": "tier2"
,
  "steps": [
    {
        "id": "day78-step1",
        "stepNumber": 1,
        "title": "In-Place Linked List Pointer Reversal: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: List Reversal",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for List Reversal.",
        "markdownContent": [
            "In-Place Linked List Reversal reverses all .next pointers in O(N) time and O(1) space using three iterative pointers: prev, curr, and next_node.",
            "### Foundational Mental Model\nWhen approaching problems requiring **List Reversal**, remember the central principle: Three-pointer reversal modifies links in-place with O(1) auxiliary space."
        ],
        "snippets": [
            {
                "title": "List Reversal Implementation Template",
                "code": "# Iterative in-place reversal\ndef reverse_list(head):\n    prev = None\n    curr = head\n    while curr:\n        nxt = curr.next\n        curr.next = prev\n        prev = curr\n        curr = nxt\n    return prev",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Three-pointer reversal modifies links in-place with O(1) auxiliary space."
    },
    {
        "id": "day78-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: List Reversal",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "At each step, cache next_node = curr.next, redirect curr.next = prev, then shift window: prev = curr and curr = next_node. At loop termination (curr is None), prev points to the new head.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Three-pointer reversal modifies links in-place with O(1) auxiliary space.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "List Reversal Core Invariant",
                "content": "Three-pointer reversal modifies links in-place with O(1) auxiliary space."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Three-pointer reversal modifies links in-place with O(1) auxiliary space."
    },
    {
        "id": "day78-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: List Reversal",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d78-q1",
                "question": "What is the role of nxt = curr.next in the three-pointer reversal loop?",
                "options": [
                    {
                        "id": "A",
                        "label": "It temporarily saves the pointer to the rest of the unreversed list before curr.next is overwritten"
                    },
                    {
                        "id": "B",
                        "label": "It reverses the tail pointer"
                    },
                    {
                        "id": "C",
                        "label": "It allocates a new node on the heap"
                    },
                    {
                        "id": "D",
                        "label": "It checks if the list contains duplicates"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! As soon as curr.next = prev is executed, the forward reference to the next node is severed. Without caching nxt = curr.next beforehand, the remainder of the list becomes unreachable.",
                    "B": "Incorrect: It does not operate on the tail.",
                    "C": "Incorrect: No memory is allocated.",
                    "D": "Incorrect: It does not evaluate values."
                }
            },
            {
                "id": "chk-d78-q2",
                "question": "What node reference should be returned as the new head after the reversal loop terminates?",
                "options": [
                    {
                        "id": "A",
                        "label": "prev, because curr has become None and prev holds the former tail"
                    },
                    {
                        "id": "B",
                        "label": "curr, because it marks the end of the loop"
                    },
                    {
                        "id": "C",
                        "label": "head, because it retains the original starting pointer"
                    },
                    {
                        "id": "D",
                        "label": "dummy.next"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! When curr reaches None, prev points to the last processed node (the former tail), which is now the new head.",
                    "B": "Incorrect: curr is None upon loop exit.",
                    "C": "Incorrect: head is now the terminal tail node pointing to None.",
                    "D": "Incorrect: No dummy node was used in standard three-pointer reversal."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day78-step4",
        "stepNumber": 4,
        "title": "Guided Practice: List Reversal",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Reverse a singly linked list in-place and return the reversed node values.",
        "subheading": "Implement and verify List Reversal in the interactive workspace.",
        "task": {
            "title": "Reverse a singly linked list in-place and return the reversed node values.",
            "instructions": [
                "Reverse a singly linked list in-place and return the reversed node values.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef reverse_and_collect(head: ListNode) -> list[int]:\n    # TODO: Implement three-pointer in-place reversal\n    # Return values of the reversed list\n    return []\n\n# 1 -> 2 -> 3 -> 4 -> 5 -> None\nh = ListNode(1, ListNode(2, ListNode(3, ListNode(4, ListNode(5)))))\nprint('Reversed:', reverse_and_collect(h))\n",
            "solutionCode": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef reverse_and_collect(head: ListNode) -> list[int]:\n    prev = None\n    curr = head\n    while curr:\n        nxt = curr.next\n        curr.next = prev\n        prev = curr\n        curr = nxt\n    \n    res = []\n    node = prev\n    while node:\n        res.append(node.val)\n        node = node.next\n    return res\n\nh = ListNode(1, ListNode(2, ListNode(3, ListNode(4, ListNode(5)))))\nprint('Reversed:', reverse_and_collect(h))\n",
            "expectedOutputPatterns": [
                "Reversed: [5, 4, 3, 2, 1]"
            ],
            "hint": "prev = None, curr = head. While curr: nxt = curr.next; curr.next = prev; prev = curr; curr = nxt. Return values starting from prev."
        },
        "keyTakeaway": "Successfully implemented and verified List Reversal!"
    },
    {
        "id": "day78-step5",
        "stepNumber": 5,
        "title": "Day 78 Complete: In-Place Linked List Pointer Reversal",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 78,
        "heading": "Mastery Achieved: In-Place Linked List Pointer Reversal",
        "subheading": "You have solidified key mental models and techniques for List Reversal.",
        "recapRows": [
            {
                "concept": "Pointer Inversion Invariant",
                "naiveIntuition": "Copy nodes into a new reversed list",
                "pythonReality": "In-place three-pointer reversal mutates pointers directly in O(1) auxiliary space with zero heap re-allocation"
            },
            {
                "concept": "Loop Termination Bound",
                "naiveIntuition": "Stop when curr.next is None",
                "pythonReality": "Stopping at while curr: ensures the final node is also processed and reversed into prev"
            }
        ],
        "solidifiedConcepts": [
            "Three-Pointer Iterative Reversal",
            "next_node Forward Caching"
        ],
        "nextDayPreview": {
            "dayNumber": 79,
            "title": "Fast & Slow Pointers (Tortoise & Hare)",
            "description": "Use the fast and slow pointer technique to find list midpoints and Kth-from-end nodes in a single traversal."
        }
    }
]
},
  79: {
  "dayNumber": 79,
  "title": "Fast & Slow Pointers (Tortoise & Hare)",
  "topicName": "Runner Technique",
  "sectionId": "linked-lists",
  "estimatedMinutes": 35,
  "difficulty": "INTERMEDIATE",
  "prerequisites": [
    78
  ],
  "concepts": [
    "2x Speed Differential",
    "Midpoint & Kth-from-End Extraction"
  ],
  "practiceSkills": [
    "Runner Technique Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Locate the exact midpoint of a linked list in a single pass using runner pointers",
    "Extract the Kth node from the end using a fixed-gap pointer pair"
  ],
  "practiceArchetype": "completion",
  "flowTier": "tier2"
,
  "steps": [
    {
        "id": "day79-step1",
        "stepNumber": 1,
        "title": "Fast & Slow Pointers (Tortoise & Hare): Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Runner Technique",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Runner Technique.",
        "markdownContent": [
            "Fast and Slow Pointers (Tortoise and Hare) traverse lists at 1x and 2x speeds, locating list midpoints in a single pass and detecting cycles.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Runner Technique**, remember the central principle: Advancing fast twice as fast as slow finds the exact midpoint in a single O(N) pass."
        ],
        "snippets": [
            {
                "title": "Runner Technique Implementation Template",
                "code": "# Find middle node\ndef find_middle(head):\n    slow = fast = head\n    while fast and fast.next:\n        slow = slow.next\n        fast = fast.next.next\n    return slow",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Advancing fast twice as fast as slow finds the exact midpoint in a single O(N) pass."
    },
    {
        "id": "day79-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Runner Technique",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "While fast and fast.next: slow = slow.next and fast = fast.next.next. When fast reaches the end, slow is exactly at the middle node (index N // 2).",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Advancing fast twice as fast as slow finds the exact midpoint in a single O(N) pass.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Runner Technique Core Invariant",
                "content": "Advancing fast twice as fast as slow finds the exact midpoint in a single O(N) pass."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Advancing fast twice as fast as slow finds the exact midpoint in a single O(N) pass."
    },
    {
        "id": "day79-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Runner Technique",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d79-q1",
                "question": "For an even-length list (e.g. 1 -> 2 -> 3 -> 4 -> None), which node will slow point to when using while fast and fast.next?",
                "options": [
                    {
                        "id": "A",
                        "label": "The second middle node (node with value 3, index 2)"
                    },
                    {
                        "id": "B",
                        "label": "The first middle node (node with value 2, index 1)"
                    },
                    {
                        "id": "C",
                        "label": "The head node (value 1)"
                    },
                    {
                        "id": "D",
                        "label": "The tail node (value 4)"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Initially slow=1, fast=1. Step 1: slow=2, fast=3. Step 2: slow=3, fast=None. Loop terminates because fast is None. Slow rests on the second middle node (3).",
                    "B": "Incorrect: To stop at the first middle node, the loop condition must be while fast.next and fast.next.next:.",
                    "C": "Incorrect: Slow advances on every iteration.",
                    "D": "Incorrect: Slow only travels half distance."
                }
            },
            {
                "id": "chk-d79-q2",
                "question": "Why must the loop guard check both fast AND fast.next?",
                "options": [
                    {
                        "id": "A",
                        "label": "To prevent an AttributeError when computing fast.next.next if fast or fast.next is None"
                    },
                    {
                        "id": "B",
                        "label": "Because slow pointer might be None"
                    },
                    {
                        "id": "C",
                        "label": "To handle negative values in nodes"
                    },
                    {
                        "id": "D",
                        "label": "To prevent stack overflow"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! If fast is None, fast.next raises an exception. If fast.next is None, fast.next.next raises an exception. Checking both ensures safe 2-step jumping.",
                    "B": "Incorrect: Slow lags behind fast and is never None before fast.",
                    "C": "Incorrect: Values do not influence traversal.",
                    "D": "Incorrect: Iterative loops do not consume stack frames."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day79-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Runner Technique",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Locate the middle element of a linked list using fast and slow pointers.",
        "subheading": "Implement and verify Runner Technique in the interactive workspace.",
        "task": {
            "title": "Locate the middle element of a linked list using fast and slow pointers.",
            "instructions": [
                "Locate the middle element of a linked list using fast and slow pointers.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef get_middle_val(head: ListNode) -> int:\n    # TODO: Advance slow 1 step and fast 2 steps\n    # Return the val of the middle node\n    return -1\n\n# 10 -> 20 -> 30 -> 40 -> 50 -> None\nh = ListNode(10, ListNode(20, ListNode(30, ListNode(40, ListNode(50)))))\nprint('Middle value:', get_middle_val(h))\n",
            "solutionCode": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef get_middle_val(head: ListNode) -> int:\n    slow = fast = head\n    while fast and fast.next:\n        slow = slow.next\n        fast = fast.next.next\n    return slow.val if slow else -1\n\nh = ListNode(10, ListNode(20, ListNode(30, ListNode(40, ListNode(50)))))\nprint('Middle value:', get_middle_val(h))\n",
            "expectedOutputPatterns": [
                "Middle value: 30"
            ],
            "hint": "slow = fast = head. While fast and fast.next: slow = slow.next; fast = fast.next.next. Return slow.val."
        },
        "keyTakeaway": "Successfully implemented and verified Runner Technique!"
    },
    {
        "id": "day79-step5",
        "stepNumber": 5,
        "title": "Day 79 Complete: Fast & Slow Pointers (Tortoise & Hare)",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 79,
        "heading": "Mastery Achieved: Fast & Slow Pointers (Tortoise & Hare)",
        "subheading": "You have solidified key mental models and techniques for Runner Technique.",
        "recapRows": [
            {
                "concept": "Single-Pass Midpoint",
                "naiveIntuition": "Count length N first, then traverse N//2 steps",
                "pythonReality": "Fast/slow pointers find the exact midpoint in a single O(N) pass without two full traversals"
            },
            {
                "concept": "Speed Ratio Invariant",
                "naiveIntuition": "Fast pointer might skip over slow without meeting",
                "pythonReality": "In discrete cycles, relative speed of 1 step/iteration guarantees fast catches slow without jumping past"
            }
        ],
        "solidifiedConcepts": [
            "2x Speed Differential",
            "Midpoint & Kth-from-End Extraction"
        ],
        "nextDayPreview": {
            "dayNumber": 80,
            "title": "Floyd's Cycle Detection & Entry Proof",
            "description": "Implement Floyd's Cycle Detection algorithm, prove 2k - k = k cycle convergence, and locate cycle start nodes."
        }
    }
]
},
  80: {
  "dayNumber": 80,
  "title": "Floyd's Cycle Detection & Entry Proof",
  "topicName": "Cycle Detection",
  "sectionId": "linked-lists",
  "estimatedMinutes": 40,
  "difficulty": "INTERMEDIATE",
  "prerequisites": [
    79
  ],
  "concepts": [
    "Floyd's Tortoise & Hare Cycle",
    "Mathematical Entry Point Derivation"
  ],
  "practiceSkills": [
    "Cycle Detection Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Detect whether a linked list contains a cycle without auxiliary hash sets",
    "Prove mathematically that moving one pointer from head matches the cycle entry node"
  ],
  "practiceArchetype": "algorithm",
  "flowTier": "tier3"
,
  "steps": [
    {
        "id": "day80-step1",
        "stepNumber": 1,
        "title": "Floyd's Cycle Detection & Entry Proof: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Cycle Detection",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Cycle Detection.",
        "markdownContent": [
            "Floyd's Cycle Detection Algorithm detects cycles and locates cycle entry points using relative speed convergence and modular arithmetic proof.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Cycle Detection**, remember the central principle: Floyd's algorithm proves cycle existence and pinpoints cycle entry in O(N) time and O(1) space."
        ],
        "snippets": [
            {
                "title": "Cycle Detection Implementation Template",
                "code": "# Floyd's Cycle Entry Detection\ndef detect_cycle_entry(head):\n    slow = fast = head\n    while fast and fast.next:\n        slow = slow.next\n        fast = fast.next.next\n        if slow == fast:\n            slow = head\n            while slow != fast:\n                slow = slow.next\n                fast = fast.next\n            return slow\n    return None",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Floyd's algorithm proves cycle existence and pinpoints cycle entry in O(N) time and O(1) space."
    },
    {
        "id": "day80-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Cycle Detection",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "If a cycle of length C exists and head is distance F from cycle entry: when slow and fast meet at distance 'a' into the cycle, fast has traveled 2*dist(slow). Math proof: 2(F + a) = F + a + k*C => F = k*C - a. Resetting slow to head and advancing both at 1x speed makes them collide exactly at the cycle entry node!",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Floyd's algorithm proves cycle existence and pinpoints cycle entry in O(N) time and O(1) space.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Cycle Detection Core Invariant",
                "content": "Floyd's algorithm proves cycle existence and pinpoints cycle entry in O(N) time and O(1) space."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Floyd's algorithm proves cycle existence and pinpoints cycle entry in O(N) time and O(1) space."
    },
    {
        "id": "day80-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Cycle Detection",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d80-q1",
                "question": "Why does resetting slow to head and advancing both pointers at 1 step/iteration guarantee they meet at the cycle entry?",
                "options": [
                    {
                        "id": "A",
                        "label": "Because the distance from head to entry (F) is mathematically equal to the distance from meeting point to entry traversing forward (k*C - a)"
                    },
                    {
                        "id": "B",
                        "label": "Because fast pointer moves backwards"
                    },
                    {
                        "id": "C",
                        "label": "Because the cycle length is always prime"
                    },
                    {
                        "id": "D",
                        "label": "Because slow pointer runs twice as fast in Phase 2"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Derived from 2(F + a) = F + a + kC => F = kC - a. Pointers starting at head and meeting point will meet after exactly F steps, which is the entrance node.",
                    "B": "Incorrect: Linked list pointers only advance forward.",
                    "C": "Incorrect: Cycle length can be any positive integer.",
                    "D": "Incorrect: Both pointers move at exactly 1 step/iteration in Phase 2."
                }
            },
            {
                "id": "chk-d80-q2",
                "question": "What is the auxiliary space complexity of Floyd's Cycle Algorithm compared to a HashSet visited approach?",
                "options": [
                    {
                        "id": "A",
                        "label": "Floyd's uses O(1) space, whereas a HashSet approach consumes O(N) memory to record visited node IDs"
                    },
                    {
                        "id": "B",
                        "label": "Both consume O(N) auxiliary space"
                    },
                    {
                        "id": "C",
                        "label": "Floyd's consumes O(N^2) space"
                    },
                    {
                        "id": "D",
                        "label": "HashSet uses O(1) space"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Floyd's algorithm tracks only two pointers (slow and fast), requiring strictly O(1) space without allocating hash set structures.",
                    "B": "Incorrect: Floyd's allocates no additional collections.",
                    "C": "Incorrect: Pointer manipulation is strictly O(1).",
                    "D": "Incorrect: Storing N node addresses in a set requires O(N) space."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day80-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Cycle Detection",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Detect if a cycle exists in a linked list and return True or False.",
        "subheading": "Implement and verify Cycle Detection in the interactive workspace.",
        "task": {
            "title": "Detect if a cycle exists in a linked list and return True or False.",
            "instructions": [
                "Detect if a cycle exists in a linked list and return True or False.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef has_cycle(head: ListNode) -> bool:\n    # TODO: Implement Phase 1 of Floyd's cycle detection\n    return False\n\n# Create list with cycle: 1 -> 2 -> 3 -> 4 -> points back to 2\nn1 = ListNode(1); n2 = ListNode(2); n3 = ListNode(3); n4 = ListNode(4)\nn1.next = n2; n2.next = n3; n3.next = n4; n4.next = n2\nprint('Has cycle:', has_cycle(n1))\n",
            "solutionCode": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef has_cycle(head: ListNode) -> bool:\n    slow = fast = head\n    while fast and fast.next:\n        slow = slow.next\n        fast = fast.next.next\n        if slow == fast:\n            return True\n    return False\n\nn1 = ListNode(1); n2 = ListNode(2); n3 = ListNode(3); n4 = ListNode(4)\nn1.next = n2; n2.next = n3; n3.next = n4; n4.next = n2\nprint('Has cycle:', has_cycle(n1))\n",
            "expectedOutputPatterns": [
                "Has cycle: True"
            ],
            "hint": "slow = fast = head. While fast and fast.next: slow = slow.next; fast = fast.next.next; if slow == fast: return True. If loop finishes, return False."
        },
        "keyTakeaway": "Successfully implemented and verified Cycle Detection!"
    },
    {
        "id": "day80-step5",
        "stepNumber": 5,
        "title": "Day 80 Complete: Floyd's Cycle Detection & Entry Proof",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 80,
        "heading": "Mastery Achieved: Floyd's Cycle Detection & Entry Proof",
        "subheading": "You have solidified key mental models and techniques for Cycle Detection.",
        "recapRows": [
            {
                "concept": "Relative Speed Reduction",
                "naiveIntuition": "Fast might jump over slow",
                "pythonReality": "Fast gains exactly 1 step on slow per iteration, making collision mathematically inevitable in any cycle"
            },
            {
                "concept": "Floyd Entry Invariant",
                "naiveIntuition": "Meeting point is always the cycle entry",
                "pythonReality": "Meeting point is inside the cycle; resetting slow to head and walking at 1x speed locates the entry node"
            }
        ],
        "solidifiedConcepts": [
            "Floyd's Tortoise & Hare Cycle",
            "Mathematical Entry Point Derivation"
        ],
        "nextDayPreview": {
            "dayNumber": 81,
            "title": "Merge Two Sorted Lists & K-Way Splicing",
            "description": "Merge two sorted linked lists in-place in O(N1 + N2) time and introduce K-way list splicing."
        }
    }
]
},
};
