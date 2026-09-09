"""
Section 5: Searching & Sorting Algorithms (Days 51 to 65)
Full authoring definitions for all 15 days with true practice archetypes,
distinguishable starter vs solution code, authentic 4-option MCQs with unique diagnostic explanations.
"""

SEC5_DAYS = {
    51: {
        "summary": "Linear search scans sequentially in O(N) time, whereas Binary Search halves the remaining search space on every comparison, achieving logarithmic O(log N) time.",
        "mechanics": "By testing the midpoint of a sorted array, we determine with certainty which half contains the target. The search space reduces as N, N/2, N/4, ... terminating in log2(N) steps.",
        "takeaway": "Logarithmic search halving requires sorted ordering and scales to billions of elements in under 35 comparisons.",
        "sample_code": "# Search space halving\n# For N = 1,000,000, log2(N) ~= 20 iterations max\nimport math\nprint('Max comparisons for 1M:', math.ceil(math.log2(1_000_000))) # 20",
        "q1": "How many comparisons does binary search require in the worst case to search through 1,000,000 sorted elements?",
        "q1_opts": [
            {"id": "A", "label": "Approximately 20 comparisons"},
            {"id": "B", "label": "Approximately 500,000 comparisons"},
            {"id": "C", "label": "Approximately 1,000 comparisons"},
            {"id": "D", "label": "Exactly 1,000,000 comparisons"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! Since 2^20 = 1,048,576 > 1,000,000, halving the range 20 times reduces the search interval to a single element.",
            "B": "Incorrect: That is average linear search, not binary search.",
            "C": "Incorrect: 2^10 is 1024, not 1 million.",
            "D": "Incorrect: That is worst-case linear search."
        },
        "q2": "Why does binary search fail if applied to an unsorted array?",
        "q2_opts": [
            {"id": "A", "label": "Without monotonic ordering, comparing with mid does not guarantee that the target cannot reside in the discarded half"},
            {"id": "B", "label": "Because mid index computation requires sorted numbers"},
            {"id": "C", "label": "Python raises a TypeError on unsorted arrays"},
            {"id": "D", "label": "Because unsorted arrays cannot be 0-indexed"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! Binary search relies entirely on the invariant that if target < arr[mid], the target CANNOT be in the right half. Without sorted order, this invariant is broken.",
            "B": "Incorrect: Mid index arithmetic (L + R) // 2 works on any integer range.",
            "C": "Incorrect: Python has no runtime sortedness check.",
            "D": "Incorrect: All lists are 0-indexed."
        },
        "practice_task": "Trace search space halving step-by-step and count total comparisons.",
        "starter": "# Day 51 Tracing Practice: Search Space Halving\ndef trace_binary_search(arr: list[int], target: int) -> tuple[int, list[int]]:\n    left, right = 0, len(arr) - 1\n    visited_mids = []\n    found_idx = -1\n    # TODO: While left <= right, record mid element in visited_mids and halve range\n    \n    return found_idx, visited_mids\n\nnums = [2, 5, 8, 12, 16, 23, 38, 45, 56, 72, 91]\nidx, mids = trace_binary_search(nums, 72)\nprint('Found index:', idx)\nprint('Visited mid elements:', mids)\n",
        "solution": "def trace_binary_search(arr: list[int], target: int) -> tuple[int, list[int]]:\n    left, right = 0, len(arr) - 1\n    visited_mids = []\n    found_idx = -1\n    while left <= right:\n        mid = left + (right - left) // 2\n        visited_mids.append(arr[mid])\n        if arr[mid] == target:\n            found_idx = mid\n            break\n        elif arr[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return found_idx, visited_mids\n\nnums = [2, 5, 8, 12, 16, 23, 38, 45, 56, 72, 91]\nidx, mids = trace_binary_search(nums, 72)\nprint('Found index:', idx)\nprint('Visited mid elements:', mids)\n",
        "patterns": ["Found index: 9", "Visited mid elements: [23, 56, 72]"],
        "hint": "mid = left + (right - left) // 2. Record arr[mid] into visited_mids, then update left = mid + 1 or right = mid - 1.",
        "recap": [
            {"concept": "Halving Power", "naiveIntuition": "Searching large arrays takes seconds", "pythonReality": "Binary search finds any item in a billion sorted elements in ~30 operations"},
            {"concept": "Sorted Requirement", "naiveIntuition": "Binary search works on any collection", "pythonReality": "Requires strictly monotonic data; sorting first takes O(N log N)"}
        ]
    },
    52: {
        "summary": "Boundary Binary Search locates insertion positions and duplicate boundaries (bisect_left vs bisect_right) by maintaining loop invariants across left <= right intervals.",
        "mechanics": "To find the first position >= target (bisect_left): if arr[mid] >= target, record candidate index and search left (right = mid - 1). Else search right (left = mid + 1).",
        "takeaway": "Lower bound (bisect_left) finds the first index >= target; upper bound (bisect_right) finds the first index > target.",
        "sample_code": "# Lower bound binary search\ndef lower_bound(arr, target):\n    L, R = 0, len(arr) - 1\n    ans = len(arr)\n    while L <= R:\n        mid = L + (R - L) // 2\n        if arr[mid] >= target:\n            ans = mid\n            R = mid - 1 # Keep searching left for earlier occurrence\n        else:\n            L = mid + 1\n    return ans",
        "q1": "In lower_bound binary search, why do we update `right = mid - 1` even when `arr[mid] == target`?",
        "q1_opts": [
            {"id": "A", "label": "To continue searching the left sub-interval for potentially earlier duplicate occurrences of the target"},
            {"id": "B", "label": "Because mid cannot be the correct answer"},
            {"id": "C", "label": "To trigger the loop termination condition immediately"},
            {"id": "D", "label": "To prevent duplicate return values"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! When searching for the FIRST occurrence (lower bound), finding a match means mid is a candidate, but an earlier identical element might exist further left.",
            "B": "Incorrect: mid is saved as the current best candidate before searching left.",
            "C": "Incorrect: Loop termination occurs when L > R.",
            "D": "Incorrect: Duplicate values are valid."
        },
        "q2": "Given arr = [1, 2, 4, 4, 4, 7, 9], what are the indices returned by bisect_left(arr, 4) and bisect_right(arr, 4)?",
        "q2_opts": [
            {"id": "A", "label": "bisect_left returns 2, bisect_right returns 5"},
            {"id": "B", "label": "bisect_left returns 4, bisect_right returns 4"},
            {"id": "C", "label": "bisect_left returns 0, bisect_right returns 6"},
            {"id": "D", "label": "bisect_left returns 2, bisect_right returns 4"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! The first 4 is at index 2 (bisect_left). The first element strictly greater than 4 is 7 at index 5 (bisect_right).",
            "B": "Incorrect: 4 is the target value, not the index.",
            "C": "Incorrect: Indices are 2 and 5.",
            "D": "Incorrect: Index 4 holds the last 4; bisect_right returns the insertion position after it (index 5)."
        },
        "practice_task": "Complete lower bound binary search by writing the critical invariant condition.",
        "starter": "def search_first_occurrence(nums: list[int], target: int) -> int:\n    left, right = 0, len(nums) - 1\n    first_idx = -1\n    while left <= right:\n        mid = left + (right - left) // 2\n        ### CRITICAL INVARIANT: YOUR CODE HERE ###\n        # If nums[mid] >= target, save mid if it equals target, and search left; else search right\n        pass\n    return first_idx\n\nnums = [1, 2, 3, 3, 3, 5, 6]\nprint('First occurrence of 3:', search_first_occurrence(nums, 3))\n",
        "solution": "def search_first_occurrence(nums: list[int], target: int) -> int:\n    left, right = 0, len(nums) - 1\n    first_idx = -1\n    while left <= right:\n        mid = left + (right - left) // 2\n        if nums[mid] == target:\n            first_idx = mid\n            right = mid - 1\n        elif nums[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return first_idx\n\nnums = [1, 2, 3, 3, 3, 5, 6]\nprint('First occurrence of 3:', search_first_occurrence(nums, 3))\n",
        "patterns": ["First occurrence of 3: 2"],
        "hint": "If nums[mid] == target: save first_idx = mid and right = mid - 1. If nums[mid] < target: left = mid + 1. Else: right = mid - 1.",
        "recap": [
            {"concept": "Midpoint Overflow", "naiveIntuition": "(L + R) // 2 is always safe", "pythonReality": "Python handles big ints, but L + (R - L) // 2 is standard across all languages to prevent 32-bit overflow"},
            {"concept": "Range Invariant", "naiveIntuition": "while left < right vs while left <= right", "pythonReality": "left <= right searches single-element intervals [i, i]; left < right requires careful boundary maintenance"}
        ]
    },
    53: {
        "summary": "Binary Search on Answer Space solves optimization problems by binary searching over candidate answers, using a monotonic boolean check function to find minimum or maximum feasible values.",
        "mechanics": "If a capacity of C is feasible, all capacities > C are also feasible (monotonicity). Search range [min_val, max_val]; if check(mid) is True, record mid and search smaller: R = mid - 1.",
        "takeaway": "Map optimization problems ('minimum speed/capacity') to monotonic boolean check predicates and binary search the answer range.",
        "sample_code": "# Binary search on answer space: Koko eating bananas\n# Range: low = 1, high = max(piles)\n# if can_eat_in_time(speed): high = mid - 1",
        "q1": "What mathematical property must an optimization problem satisfy to be solvable via Binary Search on Answer Space?",
        "q1_opts": [
            {"id": "A", "label": "Monotonicity: if answer X is feasible, all answers in one direction must also be feasible"},
            {"id": "B", "label": "The input array must be sorted in ascending order"},
            {"id": "C", "label": "The number of items must be a power of two"},
            {"id": "D", "label": "The check function must run in O(1) time"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! Monotonicity (e.g. FFFTTT or TTTFFF) ensures that a single midpoint evaluation eliminates half of the candidate answer space with certainty.",
            "B": "Incorrect: The input data does not need to be sorted; only the answer range [low..high] is sorted.",
            "C": "Incorrect: Binary search operates over any integer interval.",
            "D": "Incorrect: Check functions typically run in O(N) time."
        },
        "q2": "What is the total time complexity of Binary Search on Answer Space with range [1..M] and an O(N) feasibility check?",
        "q2_opts": [
            {"id": "A", "label": "O(N log M)"},
            {"id": "B", "label": "O(N * M)"},
            {"id": "C", "label": "O(M log N)"},
            {"id": "D", "label": "O(log(N * M))"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! There are log2(M) iterations of binary search, and each iteration invokes the O(N) check function. Total: O(N log M).",
            "B": "Incorrect: Linear search over answers is O(N * M), but binary search optimizes it to O(N log M).",
            "C": "Incorrect: Logarithm applies to answer space M.",
            "D": "Incorrect: Time is multiplicative, not logarithmic in both."
        },
        "practice_task": "Solve Capacity to Ship Packages Within D Days using monotonic answer search.",
        "starter": "def ship_within_days(weights: list[int], days: int) -> int:\n    def feasible(capacity: int) -> bool:\n        # TODO 1: Return True if weights can be shipped within 'days' at given capacity\n        return True\n    \n    left = max(weights)\n    right = sum(weights)\n    ans = right\n    # TODO 2: Binary search capacity range [left, right] to find minimum feasible capacity\n    return ans\n\nweights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]\nprint('Minimum capacity:', ship_within_days(weights, 5))\n",
        "solution": "def ship_within_days(weights: list[int], days: int) -> int:\n    def feasible(capacity: int) -> bool:\n        d = 1\n        curr = 0\n        for w in weights:\n            if curr + w > capacity:\n                d += 1\n                curr = w\n            else:\n                curr += w\n        return d <= days\n    left = max(weights)\n    right = sum(weights)\n    ans = right\n    while left <= right:\n        mid = left + (right - left) // 2\n        if feasible(mid):\n            ans = mid\n            right = mid - 1\n        else:\n            left = mid + 1\n    return ans\n\nweights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]\nprint('Minimum capacity:', ship_within_days(weights, 5))\n",
        "patterns": ["Minimum capacity: 15"],
        "hint": "Check function accumulates weights into days: when curr + w > capacity, day_count += 1 and curr = w. If day_count <= days: ans = mid and right = mid - 1.",
        "recap": [
            {"concept": "Input vs Answer", "naiveIntuition": "Binary search searches arrays of numbers", "pythonReality": "Binary search can search abstract ranges of potential answers (capacities, speeds, thresholds)"},
            {"concept": "Search Bounds", "naiveIntuition": "low = 0, high = infinity", "pythonReality": "Tight bounds matter: minimum capacity is max(weights); maximum capacity is sum(weights)"}
        ]
    },
    54: {
        "summary": "Rotated Sorted Arrays contain an inflection point (pivot) dividing the array into two sorted segments, searchable in O(log N) time by identifying which half is sorted.",
        "mechanics": "Compare arr[L] with arr[mid]. If arr[L] <= arr[mid], the left half is normally sorted: test if target lies within [arr[L], arr[mid]]; if so R = mid - 1, else L = mid + 1. Otherwise the right half is sorted.",
        "takeaway": "At least one half of a rotated sorted array is always normally sorted; determine which half is sorted and test if target falls within its bounds.",
        "sample_code": "# Search in Rotated Sorted Array\ndef search_rotated(nums, target):\n    L, R = 0, len(nums) - 1\n    while L <= R:\n        mid = L + (R - L) // 2\n        if nums[mid] == target: return mid\n        if nums[L] <= nums[mid]: # Left sorted\n            if nums[L] <= target < nums[mid]: R = mid - 1\n            else: L = mid + 1\n        else: # Right sorted\n            if nums[mid] < target <= nums[R]: L = mid + 1\n            else: R = mid - 1\n    return -1",
        "q1": "In a rotated sorted array without duplicates, what property is guaranteed for any midpoint index?",
        "q1_opts": [
            {"id": "A", "label": "At least one half (either [L..mid] or [mid..R]) is guaranteed to be strictly sorted in ascending order"},
            {"id": "B", "label": "The midpoint is always the pivot element"},
            {"id": "C", "label": "Both halves are always rotated"},
            {"id": "D", "label": "The array cannot be searched in O(log N) time"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! Because a single rotation creates at most one inflection point, that point can reside in at most one half. The other half is guaranteed to be normally sorted.",
            "B": "Incorrect: The pivot can be anywhere.",
            "C": "Incorrect: Only one half contains the rotation boundary.",
            "D": "Incorrect: O(log N) search is fully achievable."
        },
        "q2": "If `nums[L] <= nums[mid]`, how do we test if `target` resides in the left half?",
        "q2_opts": [
            {"id": "A", "label": "nums[L] <= target < nums[mid]"},
            {"id": "B", "label": "target > nums[mid]"},
            {"id": "C", "label": "target <= nums[L]"},
            {"id": "D", "label": "nums[L] < nums[mid]"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! Since the left half is sorted, target is in [L..mid) if and only if it is >= nums[L] and < nums[mid].",
            "B": "Incorrect: target > nums[mid] lies outside the left half.",
            "C": "Incorrect: target could be smaller than all elements in that half.",
            "D": "Incorrect: This checks array elements, not the target."
        },
        "practice_task": "Debug search logic in rotated sorted arrays.",
        "starter": "# Day 54 Debugging Challenge: Rotated Array Search\n# BUG REPORT: This code fails to find target in rotated arrays because the right-half condition is inverted!\ndef search_rotated_buggy(nums: list[int], target: int) -> int:\n    left, right = 0, len(nums) - 1\n    while left <= right:\n        mid = left + (right - left) // 2\n        if nums[mid] == target:\n            return mid\n        if nums[left] <= nums[mid]:\n            if nums[left] <= target < nums[mid]:\n                right = mid - 1\n            else:\n                left = mid + 1\n        else:\n            # BUG: Inverted condition here\n            if nums[mid] <= target < nums[right]:\n                left = mid + 1\n            else:\n                right = mid - 1\n    return -1\n\n# INSTRUCTION: Fix the boundary check for the right-sorted half.\nnums = [4, 5, 6, 7, 0, 1, 2]\nprint('Index of 0:', search_rotated_buggy(nums, 0))\n",
        "solution": "def search_rotated_buggy(nums: list[int], target: int) -> int:\n    left, right = 0, len(nums) - 1\n    while left <= right:\n        mid = left + (right - left) // 2\n        if nums[mid] == target:\n            return mid\n        if nums[left] <= nums[mid]:\n            if nums[left] <= target < nums[mid]:\n                right = mid - 1\n            else:\n                left = mid + 1\n        else:\n            if nums[mid] < target <= nums[right]:\n                left = mid + 1\n            else:\n                right = mid - 1\n    return -1\n\nnums = [4, 5, 6, 7, 0, 1, 2]\nprint('Index of 0:', search_rotated_buggy(nums, 0))\n",
        "patterns": ["Index of 0: 4"],
        "hint": "Change `if nums[mid] <= target < nums[right]:` to `if nums[mid] < target <= nums[right]:`.",
        "recap": [
            {"concept": "Sorted Half Determination", "naiveIntuition": "Find the rotation pivot first", "pythonReality": "Comparing nums[L] <= nums[mid] directly identifies the sorted half without finding the pivot"},
            {"concept": "Inclusive Right Bound", "naiveIntuition": "target < nums[right]", "pythonReality": "target <= nums[right] is required to include the element at index right"}
        ]
    },
    55: {
        "summary": "Quadratic Sorts (Bubble, Selection, Insertion) have O(N^2) worst-case time, but Insertion Sort achieves linear O(N) best-case time on nearly-sorted data and maintains stability.",
        "mechanics": "Insertion sort shifts elements greater than key one position right, placing key in its sorted spot. Stability means equal elements maintain their relative initial order.",
        "takeaway": "Insertion Sort is the premier O(N) sort for small or nearly-sorted arrays and forms the base engine of Timsort.",
        "sample_code": "# Insertion Sort\ndef insertion_sort(arr):\n    for i in range(1, len(arr)):\n        key = arr[i]\n        j = i - 1\n        while j >= 0 and arr[j] > key:\n            arr[j + 1] = arr[j]\n            j -= 1\n        arr[j + 1] = key\n    return arr",
        "q1": "Why is Insertion Sort adaptive, achieving O(N) time on already sorted arrays?",
        "q1_opts": [
            {"id": "A", "label": "The inner while loop terminates on the very first comparison (arr[j] > key is False), executing only 1 comparison per element"},
            {"id": "B", "label": "It uses binary search to insert items"},
            {"id": "C", "label": "It divides the array in half recursively"},
            {"id": "D", "label": "It builds a heap of elements"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! If the array is sorted, each element key is already >= arr[i-1], so the inner loop never shifts any elements, running N-1 comparisons total.",
            "B": "Incorrect: Standard insertion sort shifts linearly; binary insertion sort still requires O(N) shifts.",
            "C": "Incorrect: Insertion sort is an iterative incremental algorithm.",
            "D": "Incorrect: Heaps are used in HeapSort."
        },
        "q2": "What makes a sorting algorithm 'stable'?",
        "q2_opts": [
            {"id": "A", "label": "Equal keys preserve their relative input order in the sorted output"},
            {"id": "B", "label": "The algorithm never crashes with stack overflow"},
            {"id": "C", "label": "The runtime is guaranteed to be O(N log N)"},
            {"id": "D", "label": "The memory usage does not exceed O(1)"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! Stability ensures that if item A appears before item B with identical keys, A is guaranteed to appear before B in the sorted result.",
            "B": "Incorrect: Stability relates to element ordering, not call stack safety.",
            "C": "Incorrect: Quadratic sorts can be stable; unstable sorts like QuickSort can be O(N log N).",
            "D": "Incorrect: Space efficiency is orthogonal to stability."
        },
        "practice_task": "Debug an insertion sort implementation that violates stability.",
        "starter": "# Day 55 Debugging Challenge: Sorting Stability\n# BUG REPORT: This insertion sort violates stability because `>=` causes equal elements to swap places!\ndef unstable_insertion_sort(items: list[tuple[int, str]]) -> list[tuple[int, str]]:\n    arr = list(items)\n    for i in range(1, len(arr)):\n        key = arr[i]\n        j = i - 1\n        # BUG: Using `>=` shifts equal elements, destroying stable input order!\n        while j >= 0 and arr[j][0] >= key[0]:\n            arr[j + 1] = arr[j]\n            j -= 1\n        arr[j + 1] = key\n    return arr\n\n# INSTRUCTION: Fix the comparison to strictly `>` to restore stability.\ndata = [(2, 'first'), (1, 'only'), (2, 'second')]\nprint('Stable sorted:', unstable_insertion_sort(data))\n",
        "solution": "def unstable_insertion_sort(items: list[tuple[int, str]]) -> list[tuple[int, str]]:\n    arr = list(items)\n    for i in range(1, len(arr)):\n        key = arr[i]\n        j = i - 1\n        while j >= 0 and arr[j][0] > key[0]:\n            arr[j + 1] = arr[j]\n            j -= 1\n        arr[j + 1] = key\n    return arr\n\ndata = [(2, 'first'), (1, 'only'), (2, 'second')]\nprint('Stable sorted:', unstable_insertion_sort(data))\n",
        "patterns": ["Stable sorted: [(1, 'only'), (2, 'first'), (2, 'second')]"],
        "hint": "Change `arr[j][0] >= key[0]` to `arr[j][0] > key[0]` so equal elements stop shifting.",
        "recap": [
            {"concept": "Strict Greater-Than", "naiveIntuition": ">= and > produce identical sorted lists", "pythonReality": ">= shifts equal elements, reversing their original order and breaking sorting stability"},
            {"concept": "Adaptive Complexity", "naiveIntuition": "All O(N^2) sorts perform equally on sorted data", "pythonReality": "Selection Sort always takes O(N^2); Insertion Sort adapts to O(N) on sorted inputs"}
        ]
    },
    56: {
        "summary": "Merge Sort is a Divide-and-Conquer algorithm guaranteeing O(N log N) time and stability by recursively halving arrays and merging sorted subarrays.",
        "mechanics": "Base case: len <= 1. Divide: mid = len // 2. Recursively sort left and right halves. Combine: two-pointer merge into an auxiliary list in O(N) time.",
        "takeaway": "Merge Sort guarantees predictable O(N log N) worst-case time and stability, trading O(N) auxiliary space.",
        "sample_code": "# Merge Sort\ndef merge_sort(arr):\n    if len(arr) <= 1: return arr\n    mid = len(arr) // 2\n    L = merge_sort(arr[:mid])\n    R = merge_sort(arr[mid:])\n    res = []\n    i = j = 0\n    while i < len(L) and j < len(R):\n        if L[i] <= R[j]: res.append(L[i]); i += 1\n        else: res.append(R[j]); j += 1\n    res.extend(L[i:]); res.extend(R[j:])\n    return res",
        "q1": "Why does Merge Sort require O(N) auxiliary space in standard implementations?",
        "q1_opts": [
            {"id": "A", "label": "Merging two sorted subarrays requires an auxiliary buffer to store combined elements without overwriting unvisited items"},
            {"id": "B", "label": "Because the recursion stack depth is O(N)"},
            {"id": "C", "label": "Python creates a new process for each recursive call"},
            {"id": "D", "label": "Because mid index computation allocates memory"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! During the merge phase, elements must be written into a separate buffer to avoid overwriting elements that have not yet been compared.",
            "B": "Incorrect: The recursion stack depth is logarithmic O(log N).",
            "C": "Incorrect: Python uses standard thread stack frames.",
            "D": "Incorrect: Integer arithmetic requires no heap allocations."
        },
        "q2": "What line in the Merge Sort merge phase guarantees that the sort remains STABLE?",
        "q2_opts": [
            {"id": "A", "label": "if L[i] <= R[j]: selecting left element on equality"},
            {"id": "B", "label": "mid = len(arr) // 2"},
            {"id": "C", "label": "if len(arr) <= 1: return arr"},
            {"id": "D", "label": "res.extend(R[j:])"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! By choosing L[i] when L[i] == R[j], elements from the left subarray (which originally appeared earlier in the input) are placed first, preserving relative order.",
            "B": "Incorrect: Midpoint division does not handle value comparison.",
            "C": "Incorrect: This is the base case.",
            "D": "Incorrect: This appends remaining right elements."
        },
        "practice_task": "Implement full recursive Merge Sort with linear two-pointer merge.",
        "starter": "def merge_sort(arr: list[int]) -> list[int]:\n    # TODO 1: Base case (len <= 1)\n    # TODO 2: Split into left and right, recurse\n    # TODO 3: Merge sorted halves using two pointers\n    return arr\n\nnums = [38, 27, 43, 3, 9, 82, 10]\nprint('Sorted:', merge_sort(nums))\n",
        "solution": "def merge_sort(arr: list[int]) -> list[int]:\n    if len(arr) <= 1:\n        return arr\n    mid = len(arr) // 2\n    left = merge_sort(arr[:mid])\n    right = merge_sort(arr[mid:])\n    res = []\n    i = j = 0\n    while i < len(left) and j < len(right):\n        if left[i] <= right[j]:\n            res.append(left[i])\n            i += 1\n        else:\n            res.append(right[j])\n            j += 1\n    res.extend(left[i:])\n    res.extend(right[j:])\n    return res\n\nnums = [38, 27, 43, 3, 9, 82, 10]\nprint('Sorted:', merge_sort(nums))\n",
        "patterns": ["Sorted: [3, 9, 10, 27, 38, 43, 82]"],
        "hint": "Base case len(arr) <= 1. Recursively sort left = arr[:mid] and right = arr[mid:]. Merge with two pointers while i < len(left) and j < len(right).",
        "recap": [
            {"concept": "Guaranteed Bound", "naiveIntuition": "QuickSort is always faster than MergeSort", "pythonReality": "MergeSort guarantees O(N log N) worst-case without degenerate pivot pitfalls"},
            {"concept": "Space Penalty", "naiveIntuition": "MergeSort operates in O(1) space", "pythonReality": "Merging requires O(N) auxiliary space; in-place array merge sort is inefficient in practice"}
        ]
    },
    57: {
        "summary": "Quick Sort is an in-place divide-and-conquer algorithm that selects a pivot, partitions the array around it, and recurses on sub-arrays, achieving O(N log N) expected time and O(log N) stack space.",
        "mechanics": "Hoare partitioning uses two pointers converging from both ends, swapping elements on wrong sides of the pivot. Median-of-three pivot selection prevents O(N^2) sorted-input degradation.",
        "takeaway": "Quick Sort achieves superior cache performance due to in-place swaps, with expected O(N log N) runtime.",
        "sample_code": "# In-place Quick Sort with Hoare Partition\ndef quick_sort(arr, low, high):\n    if low < high:\n        p = partition(arr, low, high)\n        quick_sort(arr, low, p)\n        quick_sort(arr, p + 1, high)",
        "q1": "What causes Quick Sort to degrade to worst-case O(N^2) time complexity?",
        "q1_opts": [
            {"id": "A", "label": "Consistently choosing the minimum or maximum element as pivot, creating unbalanced partitions of sizes 1 and N-1"},
            {"id": "B", "label": "Using an in-place partition scheme"},
            {"id": "C", "label": "Sorting arrays containing negative numbers"},
            {"id": "D", "label": "Using Hoare partitioning instead of Lomuto"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! When partitions split into 0 and N-1 items on every step, the recurrence becomes T(N) = T(N-1) + O(N) = O(N^2).",
            "B": "Incorrect: In-place partitioning is standard and efficient.",
            "C": "Incorrect: Numbers' signs do not affect partitioning.",
            "D": "Incorrect: Both schemes suffer O(N^2) under poor pivots; Hoare does fewer swaps."
        },
        "q2": "Why does Python's standard library use Timsort instead of pure Quick Sort?",
        "q2_opts": [
            {"id": "A", "label": "Timsort guarantees O(N log N) worst case and is strictly STABLE, whereas Quick Sort is unstable and can degrade to O(N^2)"},
            {"id": "B", "label": "Quick Sort cannot sort strings in Python"},
            {"id": "C", "label": "Quick Sort requires O(N) auxiliary memory"},
            {"id": "D", "label": "Timsort runs in O(1) space"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! Real-world software demands stability (preserving input order for multi-key sorting) and worst-case performance guarantees that Quick Sort cannot provide.",
            "B": "Incorrect: Quick Sort sorts any comparable type.",
            "C": "Incorrect: Quick Sort uses O(log N) stack space.",
            "D": "Incorrect: Timsort uses O(N) auxiliary space for run merging."
        },
        "practice_task": "Implement in-place Quick Sort using Lomuto partitioning.",
        "starter": "def quick_sort(arr: list[int], low: int, high: int) -> None:\n    def partition(l: int, h: int) -> int:\n        pivot = arr[h]\n        i = l\n        # TODO 1: Partition elements < pivot to the left using pointer i\n        # TODO 2: Place pivot at index i and return i\n        return i\n\n    # TODO 3: If low < high, partition and recurse on left and right sub-arrays\n    pass\n\nnums = [10, 7, 8, 9, 1, 5]\nquick_sort(nums, 0, len(nums) - 1)\nprint('Quick sorted:', nums)\n",
        "solution": "def quick_sort(arr: list[int], low: int, high: int) -> None:\n    def partition(l: int, h: int) -> int:\n        pivot = arr[h]\n        i = l\n        for j in range(l, h):\n            if arr[j] < pivot:\n                arr[i], arr[j] = arr[j], arr[i]\n                i += 1\n        arr[i], arr[h] = arr[h], arr[i]\n        return i\n    if low < high:\n        pi = partition(low, high)\n        quick_sort(arr, low, pi - 1)\n        quick_sort(arr, pi + 1, high)\n\nnums = [10, 7, 8, 9, 1, 5]\nquick_sort(nums, 0, len(nums) - 1)\nprint('Quick sorted:', nums)\n",
        "patterns": ["Quick sorted: [1, 5, 7, 8, 9, 10]"],
        "hint": "Loop j from l to h-1: if arr[j] < pivot: swap arr[i], arr[j] and i += 1. Swap arr[i], arr[h] and recurse on (low, pi-1) and (pi+1, high).",
        "recap": [
            {"concept": "In-Place Swaps", "naiveIntuition": "List comprehension quicksort [x for x in arr if x < p] is standard", "pythonReality": "Comprehension quicksort allocates new lists on every level O(N log N space); true quicksort operates in-place"},
            {"concept": "Pivot Choice", "naiveIntuition": "Always pick arr[0]", "pythonReality": "Picking arr[0] on sorted arrays triggers O(N^2) quadratic disaster; use randomized or median-of-three pivots"}
        ]
    },
    58: {
        "summary": "Quickselect finds the Kth smallest (or largest) element in an unsorted array in expected O(N) time by recursing only into the partition containing K, discarding the other half.",
        "mechanics": "After partitioning around pivot index P: if P == k, return arr[P]. If k < P, recurse left (low..P-1). If k > P, recurse right (P+1..high). Recurrence: T(N) = T(N/2) + O(N) = O(N).",
        "takeaway": "Quickselect achieves linear O(N) expected time for order statistics by pruning half the problem space at each step.",
        "sample_code": "# Quickselect expected O(N)\ndef quickselect(nums, k):\n    p = partition(nums)\n    if p == k: return nums[p]\n    elif k < p: return quickselect(left, k)\n    else: return quickselect(right, k)",
        "q1": "Why is Quickselect's expected time complexity O(N) while Quick Sort is O(N log N)?",
        "q1_opts": [
            {"id": "A", "label": "Quickselect recurses into only ONE partition, creating a geometric series N + N/2 + N/4 + ... = 2N = O(N)"},
            {"id": "B", "label": "Quickselect does not use partitioning"},
            {"id": "C", "label": "Quickselect sorts the array using counting sort first"},
            {"id": "D", "label": "Because K is always smaller than log N"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! Quick Sort recurses into BOTH sub-arrays (work per level = N, log N levels = N log N). Quickselect discards one half at each step (N + N/2 + N/4 + ... = 2N = O(N)).",
            "B": "Incorrect: Quickselect uses the exact same partition function as Quick Sort.",
            "C": "Incorrect: No preliminary sorting is performed.",
            "D": "Incorrect: K can be any index from 0 to N-1."
        },
        "q2": "To find the Kth LARGEST element in an array of length N, what 0-indexed order statistic index do we target in Quickselect?",
        "q2_opts": [
            {"id": "A", "label": "N - K"},
            {"id": "B", "label": "K - 1"},
            {"id": "C", "label": "K"},
            {"id": "D", "label": "N // K"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! In an ascending sorted array of size N, the 1st largest is at index N-1, the 2nd largest at N-2, and the Kth largest at N - K.",
            "B": "Incorrect: K - 1 is the Kth smallest element.",
            "C": "Incorrect: Off-by-one error.",
            "D": "Incorrect: Division is unrelated to rank ordering."
        },
        "practice_task": "Complete Quickselect by filling in the single-sided branch selection invariant.",
        "starter": "def find_kth_largest(nums: list[int], k: int) -> int:\n    target_idx = len(nums) - k\n    def select(l: int, r: int) -> int:\n        pivot = nums[r]\n        i = l\n        for j in range(l, r):\n            if nums[j] <= pivot:\n                nums[i], nums[j] = nums[j], nums[i]\n                i += 1\n        nums[i], nums[r] = nums[r], nums[i]\n        ### CRITICAL INVARIANT: YOUR CODE HERE ###\n        # If i == target_idx, return nums[i]\n        # Else recurse left if target_idx < i, or right if target_idx > i\n        return -1\n    return select(0, len(nums) - 1)\n\nnums = [3, 2, 1, 5, 6, 4]\nprint('2nd largest element:', find_kth_largest(nums, 2))\n",
        "solution": "def find_kth_largest(nums: list[int], k: int) -> int:\n    target_idx = len(nums) - k\n    def select(l: int, r: int) -> int:\n        pivot = nums[r]\n        i = l\n        for j in range(l, r):\n            if nums[j] <= pivot:\n                nums[i], nums[j] = nums[j], nums[i]\n                i += 1\n        nums[i], nums[r] = nums[r], nums[i]\n        if i == target_idx:\n            return nums[i]\n        elif target_idx < i:\n            return select(l, i - 1)\n        else:\n            return select(i + 1, r)\n    return select(0, len(nums) - 1)\n\nnums = [3, 2, 1, 5, 6, 4]\nprint('2nd largest element:', find_kth_largest(nums, 2))\n",
        "patterns": ["2nd largest element: 5"],
        "hint": "Check `if i == target_idx: return nums[i]`. If `target_idx < i`: `return select(l, i - 1)`. Else: `return select(i + 1, r)`.",
        "recap": [
            {"concept": "Pruning Half the Work", "naiveIntuition": "Finding Kth element requires full O(N log N) sort", "pythonReality": "Discarding the non-promising partition achieves linear O(N) expected time"},
            {"concept": "In-Place Reordering", "naiveIntuition": "Quickselect preserves original array order", "pythonReality": "Quickselect mutates array elements around pivots in-place"}
        ]
    },
    59: {
        "summary": "Counting Sort is a non-comparison integer sorting algorithm running in linear O(N + K) time by tallying element frequencies and computing cumulative placement offsets.",
        "mechanics": "Count occurrences of each integer in range [0..K]. Compute prefix sums of counts: count[i] indicates the number of elements <= i. Place elements in reverse to ensure stability.",
        "takeaway": "Counting Sort breaks the Omega(N log N) comparison barrier, running in O(N + K) time when key range K is bounded.",
        "sample_code": "# Stable Counting Sort over range [0..K]\ndef counting_sort(arr, K):\n    count = [0] * (K + 1)\n    for x in arr: count[x] += 1\n    for i in range(1, K + 1): count[i] += count[i - 1]\n    res = [0] * len(arr)\n    for x in reversed(arr):\n        res[count[x] - 1] = x\n        count[x] -= 1\n    return res",
        "q1": "Why is the comparison sorting lower bound Omega(N log N) not applicable to Counting Sort?",
        "q1_opts": [
            {"id": "A", "label": "Counting Sort does not compare elements against each other; it uses integer values directly as array memory indices"},
            {"id": "B", "label": "Because Counting Sort runs in O(1) space"},
            {"id": "C", "label": "Because Python optimizes count arrays using C code"},
            {"id": "D", "label": "Counting Sort only works on arrays of length <= 100"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! The Omega(N log N) lower bound is proven via decision trees for comparison-based sorts. Non-comparison sorts bypass decision trees by using direct memory addressing.",
            "B": "Incorrect: Counting Sort requires O(N + K) auxiliary space.",
            "C": "Incorrect: Algorithmic complexity is independent of language implementation.",
            "D": "Incorrect: It scales to arbitrary N as long as range K is reasonable."
        },
        "q2": "When does Counting Sort become an INEFFICIENT choice?",
        "q2_opts": [
            {"id": "A", "label": "When the range of values K is significantly larger than the number of elements N (e.g. K = 10^9 and N = 10)"},
            {"id": "B", "label": "When all numbers are positive"},
            {"id": "C", "label": "When the array contains duplicate elements"},
            {"id": "D", "label": "When N > 1,000"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! Space and time are O(N + K). If K = 10^9, allocating a count array of 1 billion slots for 10 elements wastes massive time and gigabytes of RAM.",
            "B": "Incorrect: Positive numbers are ideal for 0-indexed counting.",
            "C": "Incorrect: Counting Sort excels at duplicate keys.",
            "D": "Incorrect: Counting Sort handles millions of elements effortlessly if K is bounded."
        },
        "practice_task": "Implement stable Counting Sort for bounded non-negative integers.",
        "starter": "def counting_sort(arr: list[int]) -> list[int]:\n    if not arr:\n        return []\n    # TODO 1: Find max value K and build count frequency array\n    # TODO 2: Accumulate prefix sums in count array\n    # TODO 3: Iterate arr in reverse and place elements into output array\n    return []\n\nnums = [4, 2, 2, 8, 3, 3, 1]\nprint('Counting sorted:', counting_sort(nums))\n",
        "solution": "def counting_sort(arr: list[int]) -> list[int]:\n    if not arr:\n        return []\n    max_val = max(arr)\n    count = [0] * (max_val + 1)\n    for x in arr:\n        count[x] += 1\n    for i in range(1, len(count)):\n        count[i] += count[i - 1]\n    res = [0] * len(arr)\n    for x in reversed(arr):\n        res[count[x] - 1] = x\n        count[x] -= 1\n    return res\n\nnums = [4, 2, 2, 8, 3, 3, 1]\nprint('Counting sorted:', counting_sort(nums))\n",
        "patterns": ["Counting sorted: [1, 2, 2, 3, 3, 4, 8]"],
        "hint": "count = [0] * (max(arr) + 1). Accumulate count[i] += count[i-1]. Traverse reversed(arr) placing res[count[x] - 1] = x and decrementing count[x].",
        "recap": [
            {"concept": "Non-Comparison Indexing", "naiveIntuition": "Sorting requires pairwise comparisons", "pythonReality": "Using integer values directly as array indices bypasses the comparison bound entirely"},
            {"concept": "Reverse Placement Stability", "naiveIntuition": "Forward placement is fine", "pythonReality": "Traversing input in reverse places identical keys from the back forward, preserving original relative order"}
        ]
    },
    60: {
        "summary": "Radix Sort processes integer keys digit-by-digit using stable Counting Sort subroutines, while Bucket Sort distributes uniformly distributed keys into buckets for O(N) sorting.",
        "mechanics": "LSD Radix Sort sorts by least significant digit first (1s place, 10s place, 100s place). Because sub-sorts are stable, higher-order passes preserve the sorted order of lower digits.",
        "takeaway": "Radix Sort sorts N fixed-width integers in O(D * (N + B)) time where D is digit count and B is base.",
        "sample_code": "# LSD Radix Sort digit pass\ndef radix_sort(arr):\n    max_val = max(arr)\n    exp = 1\n    while max_val // exp > 0:\n        counting_sort_by_digit(arr, exp)\n        exp *= 10",
        "q1": "Why MUST the digit sub-sorting algorithm in Radix Sort be STABLE?",
        "q1_opts": [
            {"id": "A", "label": "To preserve the sorted order established by earlier (less significant) digit passes when sorting higher digits"},
            {"id": "B", "label": "To prevent integers from exceeding 32-bit width"},
            {"id": "C", "label": "Because unstable algorithms cannot sort base-10 numbers"},
            {"id": "D", "label": "To reduce space complexity to O(1)"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! If two numbers have the same tens digit (e.g. 23 and 27), stability ensures that 23 remains before 27 because the units pass previously sorted them as 3 < 7.",
            "B": "Incorrect: Bit width is unaffected.",
            "C": "Incorrect: Stability is an ordering property, not a radix base constraint.",
            "D": "Incorrect: Radix sort requires auxiliary memory for buckets."
        },
        "q2": "What is the time complexity of sorting N numbers with maximum D digits in base 10 using Radix Sort?",
        "q2_opts": [
            {"id": "A", "label": "O(D * (N + 10))"},
            {"id": "B", "label": "O(N log N)"},
            {"id": "C", "label": "O(N^D)"},
            {"id": "D", "label": "O(10^D)"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! There are D passes, and each counting sort pass over base-10 digits takes O(N + 10) time. Total: O(D * (N + 10)).",
            "B": "Incorrect: Radix Sort is non-comparison and does not depend on log N.",
            "C": "Incorrect: The relationship is multiplicative, not exponential in N.",
            "D": "Incorrect: Does not scale with 10^D."
        },
        "practice_task": "Implement LSD Radix Sort for non-negative integers.",
        "starter": "def radix_sort(arr: list[int]) -> list[int]:\n    if not arr:\n        return []\n    # TODO: Perform LSD Radix sort using digit extraction (exp = 1, 10, 100, ...)\n    return arr\n\nnums = [170, 45, 75, 90, 802, 24, 2, 66]\nprint('Radix sorted:', radix_sort(nums))\n",
        "solution": "def radix_sort(arr: list[int]) -> list[int]:\n    if not arr:\n        return []\n    max_val = max(arr)\n    exp = 1\n    while max_val // exp > 0:\n        output = [0] * len(arr)\n        count = [0] * 10\n        for x in arr:\n            digit = (x // exp) % 10\n            count[digit] += 1\n        for i in range(1, 10):\n            count[i] += count[i - 1]\n        for x in reversed(arr):\n            digit = (x // exp) % 10\n            output[count[digit] - 1] = x\n            count[digit] -= 1\n        arr = output\n        exp *= 10\n    return arr\n\nnums = [170, 45, 75, 90, 802, 24, 2, 66]\nprint('Radix sorted:', radix_sort(nums))\n",
        "patterns": ["Radix sorted: [2, 24, 45, 66, 75, 90, 170, 802]"],
        "hint": "Extract digit = (x // exp) % 10. Perform stable counting sort into output, replace arr = output, and multiply exp *= 10 while max_val // exp > 0.",
        "recap": [
            {"concept": "LSD vs MSD", "naiveIntuition": "Sort by highest digit first", "pythonReality": "LSD (Least Significant Digit) allows simple iterative passes; MSD requires recursive bucket partitioning"},
            {"concept": "Base Selection", "naiveIntuition": "Must always use base 10", "pythonReality": "In systems programming, Radix sort uses base 256 (byte-by-byte) or base 65536 to sort binary keys in fast bit shifts"}
        ]
    },
    61: {
        "summary": "Timsort is Python's standard sorting algorithm, combining adaptive mergesort with binary insertion sort on small natural runs (minrun 32 to 64).",
        "mechanics": "Timsort scans for natural ascending (a <= b) or strictly descending (a > b) runs. Descending runs are reversed in O(N). Small runs are extended with binary insertion sort to reach minrun. Balanced runs are merged using a stack.",
        "takeaway": "Timsort achieves linear O(N) best-case time on real-world partially sorted data and guarantees O(N log N) worst-case time with stability.",
        "sample_code": "# Timsort in Python standard library\narr = [5, 1, 4, 2, 8]\narr.sort() # Invokes CPython Timsort\nprint(arr) # [1, 2, 4, 5, 8]",
        "q1": "What is the best-case time complexity of Python's Timsort on already sorted data?",
        "q1_opts": [
            {"id": "A", "label": "O(N)"},
            {"id": "B", "label": "O(N log N)"},
            {"id": "C", "label": "O(log N)"},
            {"id": "D", "label": "O(N^2)"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! Timsort identifies the entire array as a single natural ascending run in a single linear pass of N-1 comparisons.",
            "B": "Incorrect: That is Timsort's worst-case guarantee.",
            "C": "Incorrect: Must inspect all N elements.",
            "D": "Incorrect: Timsort strictly prevents quadratic behavior."
        },
        "q2": "What is the purpose of 'minrun' in Timsort?",
        "q2_opts": [
            {"id": "A", "label": "To balance the merge stack by ensuring small runs are extended using binary insertion sort, keeping the total number of runs close to a power of 2"},
            {"id": "B", "label": "To set the maximum recursion limit"},
            {"id": "C", "label": "To limit the maximum array size Python can sort"},
            {"id": "D", "label": "To prevent sorting strings"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! A minrun between 32 and 64 ensures that small sub-arrays are sorted quickly with low overhead, and the number of runs remaining to merge is balanced.",
            "B": "Incorrect: Timsort is iterative and uses an explicit stack.",
            "C": "Incorrect: Timsort sorts arrays of arbitrary lengths.",
            "D": "Incorrect: Timsort sorts any comparable objects."
        },
        "practice_task": "Trace natural run identification in Timsort.",
        "starter": "# Day 61 Tracing: Timsort Natural Run Detection\ndef identify_runs(arr: list[int]) -> list[list[int]]:\n    # TODO: Scan array, group consecutive ascending or strictly descending elements into runs\n    # Reverse any descending runs so all runs are ascending\n    runs = []\n    return runs\n\nnums = [1, 2, 3, 10, 8, 4, 7, 9]\nprint('Identified runs:', identify_runs(nums))\n",
        "solution": "def identify_runs(arr: list[int]) -> list[list[int]]:\n    if not arr:\n        return []\n    runs = []\n    n = len(arr)\n    i = 0\n    while i < n:\n        start = i\n        if i == n - 1:\n            runs.append([arr[start]])\n            break\n        if arr[i + 1] >= arr[i]:\n            while i + 1 < n and arr[i + 1] >= arr[i]:\n                i += 1\n            runs.append(arr[start:i + 1])\n        else:\n            while i + 1 < n and arr[i + 1] < arr[i]:\n                i += 1\n            run = arr[start:i + 1]\n            run.reverse()\n            runs.append(run)\n        i += 1\n    return runs\n\nnums = [1, 2, 3, 10, 8, 4, 7, 9]\nprint('Identified runs:', identify_runs(nums))\n",
        "patterns": ["Identified runs: [[1, 2, 3], [4, 8, 10], [7, 9]]"],
        "hint": "Check if next element is >= current (ascending) or < (descending). Slice run, reverse descending runs, and append.",
        "recap": [
            {"concept": "Real-World Data Exploitation", "naiveIntuition": "Data is randomly shuffled", "pythonReality": "Real datasets contain long streaks of sorted items; Timsort exploits natural runs to achieve near-linear time"},
            {"concept": "Galloping Mode", "naiveIntuition": "Merge always steps one by one", "pythonReality": "When one run wins repeatedly, Timsort switches to galloping mode (binary search) to skip blocks of elements"}
        ]
    },
    62: {
        "summary": "Custom Comparators and Multi-Key Sorting use key functions, lambdas, and tuple comparisons to sort complex heterogeneous records by primary, secondary, and reverse attributes.",
        "mechanics": "Python compares tuples element by element: (a1, b1) < (a2, b2) checks a1 < a2; if equal, checks b1 < b2. To sort primary ascending and secondary descending: key = lambda x: (x.age, -x.score).",
        "takeaway": "Tuples provide elegant multi-attribute sorting keys; negating numeric terms reverses direction for specific columns.",
        "sample_code": "# Multi-key sorting: sort by grade asc, score desc\nstudents = [('Alice', 'B', 85), ('Bob', 'A', 92), ('Charlie', 'B', 95)]\nstudents.sort(key=lambda s: (s[1], -s[2]))\n# Bob (A, 92), Charlie (B, 95), Alice (B, 85)",
        "q1": "How do you sort students by grade ascending, and for students with the same grade, by score descending?",
        "q1_opts": [
            {"id": "A", "label": "key=lambda s: (s.grade, -s.score)"},
            {"id": "B", "label": "key=lambda s: (s.grade, s.score), reverse=True"},
            {"id": "C", "label": "key=lambda s: s.grade - s.score"},
            {"id": "D", "label": "key=lambda s: (-s.grade, s.score)"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! The first tuple element s.grade sorts ascending. Negating -s.score causes higher scores to become smaller numbers, sorting descending.",
            "B": "Incorrect: reverse=True would flip both grade and score to descending.",
            "C": "Incorrect: You cannot subtract integers from string grades.",
            "D": "Incorrect: Strings cannot be negated with unary minus."
        },
        "q2": "What does functools.cmp_to_key do in Python 3?",
        "q2_opts": [
            {"id": "A", "label": "Converts a legacy three-way comparison function (returning -1, 0, 1) into a key function suitable for sorted()"},
            {"id": "B", "label": "Converts keys to dictionary hash values"},
            {"id": "C", "label": "Encrypts sorting keys for security"},
            {"id": "D", "label": "Sorts keys in O(1) time"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! Python 3 eliminated the `cmp` argument in favor of `key`. `cmp_to_key` wraps legacy comparator functions into a class implementing dunder comparison methods.",
            "B": "Incorrect: It wraps comparators into key classes.",
            "C": "Incorrect: No encryption is performed.",
            "D": "Incorrect: Sorting complexity remains O(N log N)."
        },
        "practice_task": "Sort items using multi-key tuple lambdas.",
        "starter": "# Day 62 Practice: Multi-Key Log Sorting\nlogs = [\n    ('user1', 200, 15),\n    ('user2', 500, 8),\n    ('user3', 200, 42),\n    ('user4', 500, 20)\n]\n# TODO: Sort logs by status_code ascending, and tie-break by duration descending\nsorted_logs = []\nprint('Sorted logs:', sorted_logs)\n",
        "solution": "logs = [\n    ('user1', 200, 15),\n    ('user2', 500, 8),\n    ('user3', 200, 42),\n    ('user4', 500, 20)\n]\nsorted_logs = sorted(logs, key=lambda x: (x[1], -x[2]))\nprint('Sorted logs:', sorted_logs)\n",
        "patterns": ["Sorted logs: [('user3', 200, 42), ('user1', 200, 15), ('user4', 500, 20), ('user2', 500, 8)]"],
        "hint": "Use `sorted(logs, key=lambda x: (x[1], -x[2]))`.",
        "recap": [
            {"concept": "Tuple Comparison", "naiveIntuition": "Must perform two independent sorting passes", "pythonReality": "Tuple keys (primary, secondary) evaluate tie-breakers automatically in a single sort pass"},
            {"concept": "Stability Advantage", "naiveIntuition": "Sort passes overwrite previous order", "pythonReality": "Because Python's sort is stable, you can also sort secondary first, then primary second"}
        ]
    },
    63: {
        "summary": "Inversion Counting measures how far an array is from sorted order, solvable in O(N log N) time by augmenting the merge step of Merge Sort.",
        "mechanics": "An inversion is a pair (i, j) where i < j but arr[i] > arr[j]. During merge: if right element R[j] is smaller than L[i], then R[j] is smaller than ALL remaining elements in L! Add len(L) - i to inversions.",
        "takeaway": "Instrumenting the Merge Sort merge phase counts array inversions in O(N log N) time.",
        "sample_code": "# Counting inversions during merge\n# if R[j] < L[i]: inversions += len(L) - i",
        "q1": "During the merge of two sorted lists L and R, if R[j] < L[i], how many inversions are contributed by R[j]?",
        "q1_opts": [
            {"id": "A", "label": "len(L) - i, because all elements from L[i] to the end of L are greater than R[j]"},
            {"id": "B", "label": "Exactly 1 inversion"},
            {"id": "C", "label": "i + 1 inversions"},
            {"id": "D", "label": "len(R) - j inversions"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! Because L is already sorted, if L[i] > R[j], every subsequent element L[i+1], L[i+2], ... is also > R[j]. Thus, R[j] forms inversions with all remaining len(L) - i elements!",
            "B": "Incorrect: R[j] forms an inversion with every remaining element in L, not just L[i].",
            "C": "Incorrect: Elements before i are already smaller than R[j].",
            "D": "Incorrect: Inversions are formed against elements in the left sub-array."
        },
        "q2": "What does an inversion count of 0 indicate about an array?",
        "q2_opts": [
            {"id": "A", "label": "The array is already perfectly sorted in non-decreasing order"},
            {"id": "B", "label": "The array contains no duplicate elements"},
            {"id": "C", "label": "The array is sorted in descending order"},
            {"id": "D", "label": "The array has an odd number of elements"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! If there are no pairs where i < j and arr[i] > arr[j], every element is <= its successors, which is the exact definition of sorted order.",
            "B": "Incorrect: Duplicates can have 0 inversions if sorted.",
            "C": "Incorrect: Descending order has the maximum number of inversions: N*(N-1)/2.",
            "D": "Incorrect: Inversion count is independent of parity."
        },
        "practice_task": "Count total inversions in an array using Merge Sort.",
        "starter": "def count_inversions(arr: list[int]) -> int:\n    def sort_and_count(nums: list[int]) -> tuple[list[int], int]:\n        if len(nums) <= 1:\n            return nums, 0\n        mid = len(nums) // 2\n        left, count_l = sort_and_count(nums[:mid])\n        right, count_r = sort_and_count(nums[mid:])\n        merged = []\n        inv = count_l + count_r\n        i = j = 0\n        # TODO: Merge left and right, adding (len(left) - i) to inv when right[j] < left[i]\n        return merged, inv\n    _, total = sort_and_count(arr)\n    return total\n\nnums = [8, 4, 2, 1]\nprint('Total inversions:', count_inversions(nums))\n",
        "solution": "def count_inversions(arr: list[int]) -> int:\n    def sort_and_count(nums: list[int]) -> tuple[list[int], int]:\n        if len(nums) <= 1:\n            return nums, 0\n        mid = len(nums) // 2\n        left, count_l = sort_and_count(nums[:mid])\n        right, count_r = sort_and_count(nums[mid:])\n        merged = []\n        inv = count_l + count_r\n        i = j = 0\n        while i < len(left) and j < len(right):\n            if left[i] <= right[j]:\n                merged.append(left[i])\n                i += 1\n            else:\n                merged.append(right[j])\n                inv += len(left) - i\n                j += 1\n        merged.extend(left[i:])\n        merged.extend(right[j:])\n        return merged, inv\n    _, total = sort_and_count(arr)\n    return total\n\nnums = [8, 4, 2, 1]\nprint('Total inversions:', count_inversions(nums))\n",
        "patterns": ["Total inversions: 6"],
        "hint": "When `right[j] < left[i]`, append `right[j]`, increment `j += 1`, and add `len(left) - i` to `inv`.",
        "recap": [
            {"concept": "Simultaneous Counting", "naiveIntuition": "Compare all pairs in O(N^2)", "pythonReality": "Instrumenting the merge step counts all cross-boundary inversions in bulk in O(N log N)"},
            {"concept": "Maximum Inversions", "naiveIntuition": "Maximum inversions is N", "pythonReality": "A reversed array of size N has N * (N - 1) // 2 inversions"}
        ]
    },
    64: {
        "summary": "Ternary Search finds the peak or trough of a unimodal continuous function by dividing the search interval into three equal parts using two midpoints m1 and m2.",
        "mechanics": "Calculate m1 = L + (R - L) / 3 and m2 = R - (R - L) / 3. If f(m1) < f(m2), the maximum cannot reside in [L..m1], so update L = m1. Else R = m2. Range shrinks by 2/3 each step.",
        "takeaway": "Ternary search optimizes unimodal functions in O(log3/2(Range)) steps.",
        "sample_code": "# Ternary search for maximum of unimodal function\ndef ternary_search_max(f, L, R, eps=1e-7):\n    while R - L > eps:\n        m1 = L + (R - L) / 3\n        m2 = R - (R - L) / 3\n        if f(m1) < f(m2): L = m1\n        else: R = m2\n    return (L + R) / 2",
        "q1": "What prerequisite must a function satisfy for ternary search to find its extremum?",
        "q1_opts": [
            {"id": "A", "label": "The function must be unimodal: strictly increasing up to a unique peak, then strictly decreasing (or vice versa)"},
            {"id": "B", "label": "The function must be linear"},
            {"id": "C", "label": "The function must return integer values only"},
            {"id": "D", "label": "The derivative of the function must be constant"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! Unimodality ensures that evaluating two midpoints m1 and m2 reliably discards one-third of the interval containing strictly inferior values.",
            "B": "Incorrect: Linear functions have no internal peaks.",
            "C": "Incorrect: Ternary search works on continuous real-valued functions.",
            "D": "Incorrect: Constant derivative implies a straight line."
        },
        "q2": "By what factor does the search range shrink in each iteration of ternary search?",
        "q2_opts": [
            {"id": "A", "label": "The interval shrinks to 2/3 of its previous width"},
            {"id": "B", "label": "The interval shrinks to 1/2 of its previous width"},
            {"id": "C", "label": "The interval shrinks to 1/3 of its previous width"},
            {"id": "D", "label": "The interval shrinks by a constant 1 unit"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! Dividing into three equal parts and eliminating one third leaves two thirds: the new width is (2/3) * previous_width.",
            "B": "Incorrect: 1/2 is the reduction factor of binary search.",
            "C": "Incorrect: We eliminate 1/3, keeping 2/3.",
            "D": "Incorrect: Convergence is geometric, not arithmetic."
        },
        "practice_task": "Find the maximum of a quadratic parabola using ternary search.",
        "starter": "def find_parabola_peak(L: float, R: float) -> float:\n    # Function f(x) = -(x - 3)**2 + 10 (peak at x = 3)\n    def f(x: float) -> float:\n        return -(x - 3) ** 2 + 10\n    # TODO: Perform ternary search with while R - L > 1e-6\n    return (L + R) / 2\n\nprint('Peak x location:', round(find_parabola_peak(0.0, 10.0), 2))\n",
        "solution": "def find_parabola_peak(L: float, R: float) -> float:\n    def f(x: float) -> float:\n        return -(x - 3) ** 2 + 10\n    while R - L > 1e-6:\n        m1 = L + (R - L) / 3\n        m2 = R - (R - L) / 3\n        if f(m1) < f(m2):\n            L = m1\n        else:\n            R = m2\n    return (L + R) / 2\n\nprint('Peak x location:', round(find_parabola_peak(0.0, 10.0), 2))\n",
        "patterns": ["Peak x location: 3.0"],
        "hint": "While R - L > 1e-6: m1 = L + (R - L) / 3, m2 = R - (R - L) / 3. If f(m1) < f(m2): L = m1 else R = m2. Return (L + R) / 2.",
        "recap": [
            {"concept": "Trisection vs Bisection", "naiveIntuition": "Binary search is always faster", "pythonReality": "Binary search requires monotonic functions (derivatives); ternary search finds peaks directly without computing derivatives"},
            {"concept": "Convergence Precision", "naiveIntuition": "Iterate until L == R", "pythonReality": "Floating point operations never reach exact equality; stop when R - L < epsilon (e.g. 1e-7)"}
        ]
    },
    65: {
        "summary": "Section 5 Review synthesizes binary search boundaries, divide-and-conquer sorting, non-comparison limits, and custom comparators into a high-performance hybrid sorting engine.",
        "mechanics": "The hybrid sorting engine partitions large arrays with Quick Sort / Merge Sort and switches to Insertion Sort on small subarrays (size <= 16), minimizing overhead and cache misses.",
        "takeaway": "Real-world sorting algorithms combine algorithmic strategies to maximize practical performance across different input sizes.",
        "sample_code": "# Hybrid Sort switching threshold\n# if len(arr) <= 16: insertion_sort(arr)\n# else: merge_sort(arr)",
        "q1": "Why do production sorting algorithms (like Timsort and Introsort) switch to Insertion Sort on sub-arrays of size <= 16 or 32?",
        "q1_opts": [
            {"id": "A", "label": "On small sub-arrays, Insertion Sort has near-zero overhead and higher cache locality, outperforming O(N log N) divide-and-conquer algorithms"},
            {"id": "B", "label": "Because Quick Sort cannot sort arrays smaller than 32 elements"},
            {"id": "C", "label": "To satisfy Python bytecode limits"},
            {"id": "D", "label": "To avoid allocating CPU registers"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! Asymptotic Big-O hides constant factors. For N <= 16, N^2 <= 256 while N log N with recursion overhead has a higher total operation count. Insertion sort runs faster on tiny inputs.",
            "B": "Incorrect: Quick Sort functions on any length >= 2.",
            "C": "Incorrect: No bytecode limits are involved.",
            "D": "Incorrect: Register allocation is handled by the hardware/compiler."
        },
        "q2": "Which sorting algorithm is optimal for sorting 10,000,000 integers known to fall strictly within the range [0, 100]?",
        "q2_opts": [
            {"id": "A", "label": "Counting Sort in O(N) time and O(1) extra space"},
            {"id": "B", "label": "Quick Sort in O(N log N)"},
            {"id": "C", "label": "Merge Sort in O(N log N)"},
            {"id": "D", "label": "Insertion Sort in O(N^2)"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! With range K = 100 and N = 10,000,000, Counting Sort allocates an array of only 101 integers and completes in O(N) linear time, vastly outperforming comparison sorts.",
            "B": "Incorrect: Quick Sort would perform ~240 million comparisons.",
            "C": "Incorrect: Merge Sort would require 80MB of auxiliary buffer memory.",
            "D": "Incorrect: Quadratic sort on 10 million elements would stall for hours."
        },
        "practice_task": "Build a hybrid sorting function that switches to insertion sort when sub-array size <= 4.",
        "starter": "def hybrid_sort(arr: list[int], threshold: int = 4) -> list[int]:\n    # TODO: If len(arr) <= threshold, sort using insertion sort\n    # Otherwise, split at mid, recurse, and merge\n    return arr\n\nnums = [9, 3, 1, 7, 5, 8, 2, 6, 4]\nprint('Hybrid sorted:', hybrid_sort(nums, 4))\n",
        "solution": "def hybrid_sort(arr: list[int], threshold: int = 4) -> list[int]:\n    if len(arr) <= threshold:\n        for i in range(1, len(arr)):\n            key = arr[i]\n            j = i - 1\n            while j >= 0 and arr[j] > key:\n                arr[j + 1] = arr[j]\n                j -= 1\n            arr[j + 1] = key\n        return arr\n    mid = len(arr) // 2\n    left = hybrid_sort(arr[:mid], threshold)\n    right = hybrid_sort(arr[mid:], threshold)\n    res = []\n    i = j = 0\n    while i < len(left) and j < len(right):\n        if left[i] <= right[j]:\n            res.append(left[i])\n            i += 1\n        else:\n            res.append(right[j])\n            j += 1\n    res.extend(left[i:])\n    res.extend(right[j:])\n    return res\n\nnums = [9, 3, 1, 7, 5, 8, 2, 6, 4]\nprint('Hybrid sorted:', hybrid_sort(nums, 4))\n",
        "patterns": ["Hybrid sorted: [1, 2, 3, 4, 5, 6, 7, 8, 9]"],
        "hint": "Check `if len(arr) <= threshold: do insertion sort and return arr`. Else recurse on left and right, then merge with two pointers.",
        "recap": [
            {"concept": "Hybrid Architecture", "naiveIntuition": "One sorting algorithm is always the best", "pythonReality": "Real-world engineering combines algorithms: divide-and-conquer on macroscopic scale, insertion sort on microscopic scale"},
            {"concept": "Section 5 Synthesis", "naiveIntuition": "Searching and sorting are separate topics", "pythonReality": "Sorting is the preprocessing step that transforms unsorted O(N) searches into logarithmic O(log N) binary searches"}
        ]
    }
}
