"""
Section 4: Arrays & Strings (Days 36 to 50)
Full authoring definitions for all 15 days with true practice archetypes,
distinguishable starter vs solution code, authentic 4-option MCQs with unique diagnostic explanations.
"""

SEC4_DAYS = {
    36: {
        "summary": "Static contiguous arrays store uniform data at contiguous memory addresses, enabling immediate O(1) random access via arithmetic offset.",
        "mechanics": "CPU cache lines (typically 64 bytes) fetch contiguous memory blocks into L1/L2 cache. Sequential array reads exhibit high spatial locality and near-zero cache misses.",
        "takeaway": "Contiguous memory layouts optimize CPU cache line utilization and provide O(1) arithmetic indexing.",
        "sample_code": "# Row-major iteration has high spatial locality (cache-friendly)\nmatrix = [[1, 2, 3], [4, 5, 6]]\nfor row in matrix:\n    for val in row:\n        pass",
        "q1": "Why is accessing array elements in contiguous memory significantly faster than following pointer chains?",
        "q1_opts": [
            {"id": "A", "label": "Hardware prefetchers load contiguous cache lines into L1/L2 cache before instructions request them"},
            {"id": "B", "label": "Contiguous arrays bypass RAM completely and live in CPU registers"},
            {"id": "C", "label": "Pointer chains require garbage collection passes on every dereference"},
            {"id": "D", "label": "Python compiles contiguous arrays into machine code at runtime"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! When a memory address is accessed, the CPU fetches the entire 64-byte cache line, ensuring subsequent adjacent items hit fast L1/L2 cache.",
            "B": "Incorrect: Arrays reside in RAM; only active variables reside in registers.",
            "C": "Incorrect: Garbage collection does not execute on simple pointer dereferences.",
            "D": "Incorrect: CPython interprets bytecode; it does not JIT-compile arrays to machine code."
        },
        "q2": "What is the primary trade-off of static contiguous arrays compared to linked lists?",
        "q2_opts": [
            {"id": "A", "label": "Arrays allow O(1) insertions at arbitrary positions"},
            {"id": "B", "label": "Arrays provide O(1) index lookups but require O(N) shifts for arbitrary insertions and deletions"},
            {"id": "C", "label": "Arrays use significantly more memory per element than linked nodes"},
            {"id": "D", "label": "Arrays cannot store negative numbers"}
        ],
        "q2_ans": "B",
        "q2_exp": {
            "A": "Incorrect: Arbitrary insertions require shifting elements right, which is O(N).",
            "B": "Correct! Contiguous memory allows direct arithmetic indexing base + i*stride, but inserting or removing items necessitates shifting all subsequent elements.",
            "C": "Incorrect: Linked lists use more memory because each node stores pointer references.",
            "D": "Incorrect: Arrays can store any supported data type."
        },
        "practice_task": "Trace memory access strides and measure cache efficiency simulation.",
        "starter": "# Day 36: Cache Locality Simulation (Tracing)\n# Predict the difference between row-major and column-major iteration.\nrows, cols = 3, 3\ngrid = [[r * cols + c for c in range(cols)] for r in range(rows)]\n\n# TODO 1: Extract elements in row-major order (row by row)\nrow_major = []\n\n# TODO 2: Extract elements in column-major order (col by col)\ncol_major = []\n\nprint('Row major:', row_major)\nprint('Col major:', col_major)\n",
        "solution": "rows, cols = 3, 3\ngrid = [[r * cols + c for c in range(cols)] for r in range(rows)]\nrow_major = [grid[r][c] for r in range(rows) for c in range(cols)]\ncol_major = [grid[r][c] for c in range(cols) for r in range(rows)]\nprint('Row major:', row_major)\nprint('Col major:', col_major)\n",
        "patterns": ["Row major: [0, 1, 2, 3, 4, 5, 6, 7, 8]", "Col major: [0, 3, 6, 1, 4, 7, 2, 5, 8]"],
        "hint": "Iterate r outer and c inner for row-major; iterate c outer and r inner for col-major.",
        "recap": [
            {"concept": "Spatial Locality", "naiveIntuition": "Loop order does not affect performance", "pythonReality": "Row-major traversal hits contiguous cache lines, drastically outperforming strided column jumps"},
            {"concept": "Array Indexing", "naiveIntuition": "Python traverses pointer chains to find lst[i]", "pythonReality": "CPython calculates base + i * 8 bytes immediately in O(1) time"}
        ]
    },
    37: {
        "summary": "1D Prefix Sums precompute cumulative array sums in O(N) time, enabling any contiguous subarray range sum query sum(arr[L..R]) to be evaluated in strict O(1) time.",
        "mechanics": "Define prefix[0] = 0 and prefix[i] = prefix[i-1] + arr[i-1] for 1-indexed tables. Then sum(arr[L..R]) = prefix[R+1] - prefix[L].",
        "takeaway": "Trading O(N) precomputation space reduces repeated range sum queries from O(N) to O(1).",
        "sample_code": "nums = [1, 2, 3, 4, 5]\npref = [0] * (len(nums) + 1)\nfor i in range(len(nums)):\n    pref[i + 1] = pref[i] + nums[i]\n# sum of nums[1..3] ([2, 3, 4]):\nrange_sum = pref[4] - pref[1] # 10 - 1 = 9",
        "q1": "Why is 1-indexed prefix padding (prefix[0] = 0) considered a best practice?",
        "q1_opts": [
            {"id": "A", "label": "It eliminates boundary edge-case conditionals when querying ranges starting at index 0"},
            {"id": "B", "label": "Python arrays cannot begin at index 0"},
            {"id": "C", "label": "It reduces prefix array space complexity from O(N) to O(1)"},
            {"id": "D", "label": "It allows negative numbers to be stored in the prefix array"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! When L = 0, pref[R+1] - pref[0] gracefully returns pref[R+1] - 0 without needing an 'if L == 0' branch.",
            "B": "Incorrect: Python uses 0-based indexing natively.",
            "C": "Incorrect: The prefix array still requires O(N) auxiliary space.",
            "D": "Incorrect: Prefix sums handle negative numbers regardless of 0 or 1-indexing."
        },
        "q2": "Given nums = [3, -1, 4, 2], what is the 1-indexed prefix array?",
        "q2_opts": [
            {"id": "A", "label": "[0, 3, 2, 6, 8]"},
            {"id": "B", "label": "[3, 2, 6, 8]"},
            {"id": "C", "label": "[0, 3, 4, 8, 10]"},
            {"id": "D", "label": "[8, 6, 2, 3, 0]"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! pref[0]=0, pref[1]=3, pref[2]=3+(-1)=2, pref[3]=2+4=6, pref[4]=6+2=8.",
            "B": "Incorrect: This is 0-indexed without the leading zero sentinel.",
            "C": "Incorrect: -1 must be subtracted, not added as positive 1.",
            "D": "Incorrect: This is reversed."
        },
        "practice_task": "Implement an immutable PrefixSum class supporting O(1) range queries.",
        "starter": "class NumArray:\n    def __init__(self, nums: list[int]):\n        # TODO 1: Construct 1-indexed prefix array 'self.pref'\n        self.pref = []\n\n    def sum_range(self, left: int, right: int) -> int:\n        # TODO 2: Return sum of nums[left..right] in O(1) time\n        return 0\n\nobj = NumArray([-2, 0, 3, -5, 2, -1])\nprint('Query 0..2:', obj.sum_range(0, 2))\nprint('Query 2..5:', obj.sum_range(2, 5))\n",
        "solution": "class NumArray:\n    def __init__(self, nums: list[int]):\n        self.pref = [0] * (len(nums) + 1)\n        for i, x in enumerate(nums):\n            self.pref[i + 1] = self.pref[i] + x\n\n    def sum_range(self, left: int, right: int) -> int:\n        return self.pref[right + 1] - self.pref[left]\n\nobj = NumArray([-2, 0, 3, -5, 2, -1])\nprint('Query 0..2:', obj.sum_range(0, 2))\nprint('Query 2..5:', obj.sum_range(2, 5))\n",
        "patterns": ["Query 0..2: 1", "Query 2..5: -1"],
        "hint": "Initialize self.pref with size len(nums) + 1, then return self.pref[right + 1] - self.pref[left].",
        "recap": [
            {"concept": "Range Query Cost", "naiveIntuition": "Calling sum(nums[L:R+1]) inside a loop is fine", "pythonReality": "sum(slice) is O(K) time and O(K) space; Prefix sums answer in O(1) time and O(1) space"},
            {"concept": "Zero Sentinel", "naiveIntuition": "Padding with 0 wastes memory", "pythonReality": "The leading 0 allows range [0..R] to use the exact same formula pref[R+1] - pref[0]"}
        ]
    },
    38: {
        "summary": "Difference Arrays allow multiple range updates (incrementing all elements in arr[L..R] by val) to be performed in O(1) time each, followed by a single O(N) prefix sum pass.",
        "mechanics": "Let diff[i] = arr[i] - arr[i-1]. Adding val to [L..R] simply executes diff[L] += val and diff[R+1] -= val. Cumulative prefix sums of diff reproduce the final modified array.",
        "takeaway": "Batch multiple range updates in O(1) time using difference boundary markings, then reconstruct in a single O(N) sweep.",
        "sample_code": "# Range update [1, 3] += 5 on array of size 5\ndiff = [0] * 6\nL, R, val = 1, 3, 5\ndiff[L] += val\ndiff[R + 1] -= val\n# Reconstruct:\nres = [0] * 5\ncurr = 0\nfor i in range(5):\n    curr += diff[i]\n    res[i] = curr",
        "q1": "Why must diff[R + 1] be decremented by val when adding val to range [L..R]?",
        "q1_opts": [
            {"id": "A", "label": "To cancel out the addition of val for all indices beyond R during the prefix reconstruction pass"},
            {"id": "B", "label": "To prevent array index out of bounds errors"},
            {"id": "C", "label": "Because difference arrays must always sum to zero"},
            {"id": "D", "label": "To handle negative numbers in the range"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! The addition at diff[L] ripples through all subsequent prefix sums. Subtracting val at R+1 terminates the ripple effect at index R.",
            "B": "Incorrect: Bounds checking is separate from mathematical delta cancellation.",
            "C": "Incorrect: The difference array sums to the final element's value, not necessarily zero.",
            "D": "Incorrect: The mechanism functions identically for positive and negative values."
        },
        "q2": "What is the overall time complexity of performing Q range updates on an array of size N using a difference array?",
        "q2_opts": [
            {"id": "A", "label": "O(Q + N)"},
            {"id": "B", "label": "O(Q * N)"},
            {"id": "C", "label": "O(N log Q)"},
            {"id": "D", "label": "O(Q log N)"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! Each of the Q updates takes O(1) time, and the final prefix sum sweep takes O(N) time. Total: O(Q + N).",
            "B": "Incorrect: Naive loop updates take O(Q * N), but difference arrays avoid this.",
            "C": "Incorrect: No tree structures or binary searches are involved.",
            "D": "Incorrect: Difference updates do not use logarithmic operations."
        },
        "practice_task": "Apply difference array range updates to track airline flight bookings.",
        "starter": "def corp_flight_bookings(bookings: list[list[int]], n: int) -> list[int]:\n    diff = [0] * (n + 2)\n    # TODO: For each [first, last, seats] in bookings, update diff[first] and diff[last + 1]\n    \n    res = [0] * n\n    # TODO: Reconstruct res using a single prefix sum sweep\n    return res\n\nbookings = [[1, 2, 10], [2, 3, 20], [2, 5, 25]]\nprint('Final seats:', corp_flight_bookings(bookings, 5))\n",
        "solution": "def corp_flight_bookings(bookings: list[list[int]], n: int) -> list[int]:\n    diff = [0] * (n + 2)\n    for first, last, seats in bookings:\n        diff[first] += seats\n        diff[last + 1] -= seats\n    res = [0] * n\n    curr = 0\n    for i in range(1, n + 1):\n        curr += diff[i]\n        res[i - 1] = curr\n    return res\n\nbookings = [[1, 2, 10], [2, 3, 20], [2, 5, 25]]\nprint('Final seats:', corp_flight_bookings(bookings, 5))\n",
        "patterns": ["Final seats: [10, 55, 45, 25, 25]"],
        "hint": "diff[first] += seats, diff[last + 1] -= seats, then accumulate with a running sum for i from 1 to n.",
        "recap": [
            {"concept": "Range Update Cost", "naiveIntuition": "Update each index in range [L..R] with a for-loop", "pythonReality": "A naive loop is O(N) per update; difference boundary markers diff[L]+=v and diff[R+1]-=v take O(1)"},
            {"concept": "Reconstruction", "naiveIntuition": "Rebuilding array takes extra allocations", "pythonReality": "A single O(N) cumulative sum converts boundary deltas back into original values"}
        ]
    },
    39: {
        "summary": "Opposing Two Pointers start at opposite boundaries (left = 0, right = N - 1) and converge inward based on monotonic evaluation, pruning suboptimal candidate pairs in O(N) time.",
        "mechanics": "In Container With Most Water, width decreases on every step. Therefore, to find a potentially larger area, we must advance the pointer pointing to the shorter vertical line.",
        "takeaway": "Opposing pointers reduce pair searches from O(N^2) to O(N) whenever the search space can be pruned monotonically.",
        "sample_code": "# Container With Most Water\ndef max_area(height):\n    L, R = 0, len(height) - 1\n    best = 0\n    while L < R:\n        area = min(height[L], height[R]) * (R - L)\n        best = max(best, area)\n        if height[L] < height[R]: L += 1\n        else: R -= 1\n    return best",
        "q1": "In Container With Most Water, why do we advance the pointer with the shorter height?",
        "q1_opts": [
            {"id": "A", "label": "Because moving the taller line can only decrease width without any chance of increasing the limiting height"},
            {"id": "B", "label": "Because moving the shorter line guarantees that the next area will be larger"},
            {"id": "C", "label": "To ensure left and right pointers meet at the exact array center"},
            {"id": "D", "label": "Because Python optimizes increments of the left pointer"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! Area is constrained by min(h[L], h[R]). If we move the taller line, width decreases while the height bottleneck remains bounded by the shorter line, guaranteeing a smaller area.",
            "B": "Incorrect: Moving the shorter line might find a taller line, but does not guarantee a larger area.",
            "C": "Incorrect: The pointers meet wherever convergence occurs, not necessarily at the center.",
            "D": "Incorrect: Python has no such pointer increment optimization."
        },
        "q2": "What prerequisite condition must be satisfied before applying opposing two pointers to the Two-Sum problem?",
        "q2_opts": [
            {"id": "A", "label": "The input array must be sorted in ascending order"},
            {"id": "B", "label": "All array elements must be positive integers"},
            {"id": "C", "label": "The array length must be an even number"},
            {"id": "D", "label": "The array cannot contain duplicate values"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! Inward pointer movement requires monotonicity: if sum < target, increment left to increase sum; if sum > target, decrement right to decrease sum.",
            "B": "Incorrect: Two pointers on sorted arrays work with negative integers.",
            "C": "Incorrect: Any array length >= 2 is valid.",
            "D": "Incorrect: Duplicates are permitted."
        },
        "practice_task": "Solve Container With Most Water in O(N) time and O(1) space.",
        "starter": "def max_area(height: list[int]) -> int:\n    left = 0\n    right = len(height) - 1\n    max_water = 0\n    # TODO: While left < right, calculate area, update max_water, and advance shorter line\n    \n    return max_water\n\nheights = [1, 8, 6, 2, 5, 4, 8, 3, 7]\nprint('Max water container:', max_area(heights))\n",
        "solution": "def max_area(height: list[int]) -> int:\n    left = 0\n    right = len(height) - 1\n    max_water = 0\n    while left < right:\n        current_water = min(height[left], height[right]) * (right - left)\n        if current_water > max_water:\n            max_water = current_water\n        if height[left] < height[right]:\n            left += 1\n        else:\n            right -= 1\n    return max_water\n\nheights = [1, 8, 6, 2, 5, 4, 8, 3, 7]\nprint('Max water container:', max_area(heights))\n",
        "patterns": ["Max water container: 49"],
        "hint": "Calculate width = right - left, h = min(height[left], height[right]), then increment left if height[left] < height[right] else decrement right.",
        "recap": [
            {"concept": "Search Space Pruning", "naiveIntuition": "All pairs (i, j) must be tested in O(N^2)", "pythonReality": "By moving the shorter pointer, we prove that all other pairs with the shorter line are strictly inferior, eliminating N-1 candidates per step"},
            {"concept": "Space Complexity", "naiveIntuition": "Need auxiliary arrays to track areas", "pythonReality": "Only two integer pointers and a max tracker are required, achieving strict O(1) auxiliary space"}
        ]
    },
    40: {
        "summary": "Fast and Slow Pointers use a read pointer (fast) scanning forward and a write pointer (slow) retaining valid elements to mutate arrays in-place in O(N) time and O(1) space.",
        "mechanics": "To remove duplicates or zeroes in-place: fast pointer advances unconditionally every iteration. If arr[fast] satisfies the retention predicate, arr[slow] = arr[fast] and slow increments.",
        "takeaway": "Fast/slow pointers perform in-place array filtering and compaction in O(N) time without allocating extra lists.",
        "sample_code": "# In-place Move Zeroes\nnums = [0, 1, 0, 3, 12]\nslow = 0\nfor fast in range(len(nums)):\n    if nums[fast] != 0:\n        nums[slow], nums[fast] = nums[fast], nums[slow]\n        slow += 1",
        "q1": "In the Remove Duplicates from Sorted Array algorithm, what condition causes the slow pointer to advance?",
        "q1_opts": [
            {"id": "A", "label": "When nums[fast] != nums[slow], indicating a brand new unique value has been discovered"},
            {"id": "B", "label": "When nums[fast] == nums[slow]"},
            {"id": "C", "label": "On every single iteration unconditionally"},
            {"id": "D", "label": "Only when fast reaches the end of the array"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! When nums[fast] differs from the last written unique item at nums[slow], slow increments and writes the new unique value.",
            "B": "Incorrect: If they are equal, it is a duplicate that must be skipped.",
            "C": "Incorrect: Fast advances unconditionally, but slow only advances on new unique elements.",
            "D": "Incorrect: Slow advances incrementally throughout the traversal."
        },
        "q2": "What is the auxiliary space complexity of removing zeroes in-place using fast and slow pointers?",
        "q2_opts": [
            {"id": "A", "label": "O(1) auxiliary space because mutations overwrite existing memory in-place"},
            {"id": "B", "label": "O(N) auxiliary space because a new list is created"},
            {"id": "C", "label": "O(log N) auxiliary space for pointer offsets"},
            {"id": "D", "label": "O(K) where K is the number of zeroes"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! Only two integer variables (fast and slow) are stored; elements are swapped directly within the existing list buffer.",
            "B": "Incorrect: No new list is allocated.",
            "C": "Incorrect: Integer variables use fixed 64-bit space, which is O(1).",
            "D": "Incorrect: Zeroes are swapped in-place without extra storage."
        },
        "practice_task": "Complete in-place zero compaction by filling the critical swap invariant.",
        "starter": "def move_zeroes(nums: list[int]) -> list[int]:\n    slow = 0\n    for fast in range(len(nums)):\n        ### CRITICAL INVARIANT: YOUR CODE HERE ###\n        # If nums[fast] is non-zero, swap nums[slow] and nums[fast], then increment slow\n        pass\n    return nums\n\nnums = [0, 1, 0, 3, 12]\nprint('Compacted:', move_zeroes(nums))\n",
        "solution": "def move_zeroes(nums: list[int]) -> list[int]:\n    slow = 0\n    for fast in range(len(nums)):\n        if nums[fast] != 0:\n            nums[slow], nums[fast] = nums[fast], nums[slow]\n            slow += 1\n    return nums\n\nnums = [0, 1, 0, 3, 12]\nprint('Compacted:', move_zeroes(nums))\n",
        "patterns": ["Compacted: [1, 3, 12, 0, 0]"],
        "hint": "Check `if nums[fast] != 0:`, then execute `nums[slow], nums[fast] = nums[fast], nums[slow]` and `slow += 1`.",
        "recap": [
            {"concept": "Compaction Invariant", "naiveIntuition": "Filter into a new list and reassign", "pythonReality": "Slow pointer partitions the array: indices < slow are processed non-zeroes; indices >= slow are pending/zeroes"},
            {"concept": "List Slicing vs In-Place", "naiveIntuition": "nums = [x for x in nums if x != 0] is in-place", "pythonReality": "Comprehensions allocate a new list; fast/slow pointers mutate the caller's array directly in O(1) space"}
        ]
    },
    41: {
        "summary": "Fixed Sliding Windows maintain state across a constant span K in O(1) time per slide by adding the right incoming element and subtracting the left outgoing element.",
        "mechanics": "Initialize window sum over nums[:K]. For index i from K to N-1, window_sum += nums[i] - nums[i - K]. Max sum updates at each step in strict O(1) time.",
        "takeaway": "Slide fixed windows in O(1) time per step by adjusting the rolling aggregate by the difference between incoming and outgoing elements.",
        "sample_code": "# Fixed window rolling sum of size k\ndef max_sub_k(arr, k):\n    w = sum(arr[:k])\n    ans = w\n    for i in range(k, len(arr)):\n        w += arr[i] - arr[i - k]\n        ans = max(ans, w)\n    return ans",
        "q1": "Why is the fixed sliding window approach O(N) rather than O(N * K)?",
        "q1_opts": [
            {"id": "A", "label": "Each step reuses K - 1 elements from the previous window and performs only two arithmetic operations"},
            {"id": "B", "label": "Python's sum() function caches previous results automatically"},
            {"id": "C", "label": "Because the window size K is always treated as a mathematical constant 1"},
            {"id": "D", "label": "It sorts the array in O(N) time first"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! Two consecutive windows overlap across K - 1 elements. Adding arr[i] and subtracting arr[i - k] updates the state in O(1) time.",
            "B": "Incorrect: sum() recomputes elements from scratch every call.",
            "C": "Incorrect: K can be arbitrarily large up to N.",
            "D": "Incorrect: Sorting changes contiguous ordering and destroys subarrays."
        },
        "q2": "What is the optimal way to initialize a fixed sliding window algorithm?",
        "q2_opts": [
            {"id": "A", "label": "Compute the initial sum of the first K elements upfront before starting the loop at index K"},
            {"id": "B", "label": "Start the loop at index 0 and use an 'if i >= k' check on every iteration"},
            {"id": "C", "label": "Initialize window sum to float('-inf')"},
            {"id": "D", "label": "Pad the array with K zeroes at the beginning"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! Precomputing sum(nums[:k]) cleanly establishes the loop invariant before sliding from index K to N.",
            "B": "Incorrect: Branching on every iteration adds branch predictor overhead.",
            "C": "Incorrect: Window sum must match actual element values.",
            "D": "Incorrect: Padding alters array indexing and allocations."
        },
        "practice_task": "Find the maximum average subarray of fixed size k.",
        "starter": "def find_max_average(nums: list[int], k: int) -> float:\n    # TODO 1: Initialize window_sum with the sum of the first k elements\n    window_sum = 0\n    max_sum = 0\n    \n    # TODO 2: Slide window from index k to len(nums) and update max_sum\n    \n    return max_sum / k\n\nnums = [1, 12, -5, -6, 50, 3]\nk = 4\nprint('Max average:', find_max_average(nums, k))\n",
        "solution": "def find_max_average(nums: list[int], k: int) -> float:\n    window_sum = sum(nums[:k])\n    max_sum = window_sum\n    for i in range(k, len(nums)):\n        window_sum += nums[i] - nums[i - k]\n        if window_sum > max_sum:\n            max_sum = window_sum\n    return max_sum / k\n\nnums = [1, 12, -5, -6, 50, 3]\nk = 4\nprint('Max average:', find_max_average(nums, k))\n",
        "patterns": ["Max average: 12.75"],
        "hint": "window_sum = sum(nums[:k]), max_sum = window_sum, loop for i in range(k, len(nums)) updating window_sum += nums[i] - nums[i - k].",
        "recap": [
            {"concept": "Overlapping Windows", "naiveIntuition": "Recalculate each window sum from scratch in O(K)", "pythonReality": "Adjusting running sum by incoming minus outgoing is strictly O(1)"},
            {"concept": "Division Timing", "naiveIntuition": "Divide by K on every iteration", "pythonReality": "Track maximum sum and perform a single division by K at the very end"}
        ]
    },
    42: {
        "summary": "Dynamic Sliding Windows expand the right pointer to acquire elements and contract the left pointer when validity invariants are violated, processing strings/arrays in O(N) time.",
        "mechanics": "In Longest Substring Without Repeating Characters: right pointer inserts s[R] into a character-index map. If s[R] was seen at index >= L, jump left pointer to seen[s[R]] + 1.",
        "takeaway": "Dynamic windows maintain monotonicity: both left and right pointers only move forward, guaranteeing O(N) total steps.",
        "sample_code": "# Longest Substring Without Repeating Characters\ndef length_of_longest_substring(s):\n    seen = {}\n    L = 0\n    best = 0\n    for R, ch in enumerate(s):\n        if ch in seen and seen[ch] >= L:\n            L = seen[ch] + 1\n        seen[ch] = R\n        best = max(best, R - L + 1)\n    return best",
        "q1": "Why does Longest Substring Without Repeating Characters run in O(N) time even with an inner pointer shift?",
        "q1_opts": [
            {"id": "A", "label": "Both left and right pointers only advance forward; each character is visited at most twice"},
            {"id": "B", "label": "The hash table lookup takes O(N) time"},
            {"id": "C", "label": "The string length is bounded by the 26-letter alphabet"},
            {"id": "D", "label": "Python optimizes while loops on strings into single-cycle operations"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! Right pointer moves 0 to N-1; Left pointer moves monotonically forward. The total pointer movements are bounded by 2N = O(N).",
            "B": "Incorrect: Hash map lookup is O(1) average time.",
            "C": "Incorrect: Input strings can contain arbitrary Unicode characters and lengths.",
            "D": "Incorrect: No such compiler optimization exists."
        },
        "q2": "Why must we verify `seen[ch] >= L` before jumping the left pointer to `seen[ch] + 1`?",
        "q2_opts": [
            {"id": "A", "label": "To ignore occurrences of ch that appeared before the current window boundary L"},
            {"id": "B", "label": "To ensure seen[ch] does not throw a KeyError"},
            {"id": "C", "label": "Because left pointer cannot exceed the array length"},
            {"id": "D", "label": "To avoid negative indices"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! If a character was seen at index 2, but our window has already moved to L = 5, the duplicate is outside our active window and must not pull L backward!",
            "B": "Incorrect: KeyError is avoided by checking 'ch in seen'.",
            "C": "Incorrect: L is bounded by R.",
            "D": "Incorrect: Indices are non-negative."
        },
        "practice_task": "Find the length of the longest substring without repeating characters.",
        "starter": "def length_of_longest_substring(s: str) -> int:\n    last_seen = {}\n    left = 0\n    max_len = 0\n    # TODO: Traverse with right pointer, update left on duplicates within window, and update max_len\n    \n    return max_len\n\ns = 'abcabcbb'\nprint('Longest unique substring length:', length_of_longest_substring(s))\n",
        "solution": "def length_of_longest_substring(s: str) -> int:\n    last_seen = {}\n    left = 0\n    max_len = 0\n    for right, ch in enumerate(s):\n        if ch in last_seen and last_seen[ch] >= left:\n            left = last_seen[ch] + 1\n        last_seen[ch] = right\n        current_len = right - left + 1\n        if current_len > max_len:\n            max_len = current_len\n    return max_len\n\ns = 'abcabcbb'\nprint('Longest unique substring length:', length_of_longest_substring(s))\n",
        "patterns": ["Longest unique substring length: 3"],
        "hint": "Check `if ch in last_seen and last_seen[ch] >= left: left = last_seen[ch] + 1`, update `last_seen[ch] = right`, and record `max(max_len, right - left + 1)`.",
        "recap": [
            {"concept": "Pointer Monotonicity", "naiveIntuition": "Restarting the window requires scanning backward", "pythonReality": "Left pointer jumps directly past the previous duplicate using stored indices, never moving backward"},
            {"concept": "Window Length", "naiveIntuition": "Length is right - left", "pythonReality": "0-indexed inclusive window length is right - left + 1"}
        ]
    },
    43: {
        "summary": "Kadane's Algorithm finds the maximum contiguous subarray sum in O(N) time and O(1) space by deciding at each element whether to extend the existing subarray or start fresh.",
        "mechanics": "Let curr_sum = max(x, curr_sum + x). If curr_sum drops below x (or below 0), starting fresh from x is mathematically superior to carrying a negative accumulator.",
        "takeaway": "Kadane's algorithm evaluates local choices (extend vs restart) to achieve global maximum subarray sums in a single linear pass.",
        "sample_code": "# Kadane's Algorithm\ndef max_sub_array(nums):\n    curr = nums[0]\n    best = nums[0]\n    for x in nums[1:]:\n        curr = max(x, curr + x)\n        best = max(best, curr)\n    return best",
        "q1": "Under what condition does Kadane's algorithm restart the current subarray sum?",
        "q1_opts": [
            {"id": "A", "label": "When the incoming element x is greater than curr_sum + x (i.e. curr_sum < 0)"},
            {"id": "B", "label": "When the incoming element is equal to zero"},
            {"id": "C", "label": "Whenever a negative number is encountered"},
            {"id": "D", "label": "Only when the array has all negative elements"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! If curr_sum is negative, adding it to x produces a value smaller than x itself. It is always better to discard the negative prefix and start fresh at x.",
            "B": "Incorrect: Zero does not decrease the sum.",
            "C": "Incorrect: Negative numbers are accepted if the overall accumulator remains positive.",
            "D": "Incorrect: Restart decisions happen dynamically whenever prefixes become negative deficits."
        },
        "q2": "Why should best_sum be initialized to nums[0] rather than 0?",
        "q2_opts": [
            {"id": "A", "label": "To handle arrays where all numbers are negative, ensuring the least negative number is returned"},
            {"id": "B", "label": "Because Python does not allow initializing variables to 0"},
            {"id": "C", "label": "To avoid a DivisionByZero error"},
            {"id": "D", "label": "Because nums[0] is always the maximum element"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! If nums = [-5, -2, -8], initializing to 0 would incorrectly return 0 (an empty subarray). Initializing to nums[0] correctly returns -2.",
            "B": "Incorrect: Zero is a valid integer in Python.",
            "C": "Incorrect: No division occurs in Kadane's algorithm.",
            "D": "Incorrect: nums[0] can be any value."
        },
        "practice_task": "Implement Kadane's algorithm tracking maximum sum and subarray start/end indices.",
        "starter": "def max_sub_array_with_indices(nums: list[int]) -> tuple[int, int, int]:\n    # TODO: Implement Kadane's algorithm returning (max_sum, start_idx, end_idx)\n    max_sum = nums[0]\n    start = end = 0\n    return max_sum, start, end\n\nnums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]\nprint('Result:', max_sub_array_with_indices(nums))\n",
        "solution": "def max_sub_array_with_indices(nums: list[int]) -> tuple[int, int, int]:\n    max_sum = nums[0]\n    curr_sum = nums[0]\n    start = end = temp_start = 0\n    for i in range(1, len(nums)):\n        if nums[i] > curr_sum + nums[i]:\n            curr_sum = nums[i]\n            temp_start = i\n        else:\n            curr_sum += nums[i]\n        if curr_sum > max_sum:\n            max_sum = curr_sum\n            start = temp_start\n            end = i\n    return max_sum, start, end\n\nnums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]\nprint('Result:', max_sub_array_with_indices(nums))\n",
        "patterns": ["Result: (6, 3, 6)"],
        "hint": "Track temp_start whenever nums[i] > curr_sum + nums[i]. When curr_sum > max_sum, update start = temp_start and end = i.",
        "recap": [
            {"concept": "Local vs Global Optimum", "naiveIntuition": "Track all subarray combinations O(N^2)", "pythonReality": "Maintaining local maximum curr = max(x, curr + x) guarantees reaching the global maximum in O(N)"},
            {"concept": "Negative-Only Arrays", "naiveIntuition": "Maximum sum is 0", "pythonReality": "Subarray must be non-empty; the maximum sum is the single least-negative element"}
        ]
    },
    44: {
        "summary": "In-Place Array Rotation by K steps can be performed in O(N) time and O(1) auxiliary space using the Triple-Reversal algorithm.",
        "mechanics": "To rotate right by K: normalize k = k % N. 1. Reverse entire array. 2. Reverse first k elements. 3. Reverse remaining N - k elements.",
        "takeaway": "Three consecutive in-place reversals reorder array segments in O(N) time without allocating auxiliary memory.",
        "sample_code": "# In-place rotation by k\ndef rotate(nums, k):\n    n = len(nums)\n    k %= n\n    def rev(l, r):\n        while l < r:\n            nums[l], nums[r] = nums[r], nums[l]\n            l += 1; r -= 1\n    rev(0, n - 1)\n    rev(0, k - 1)\n    rev(k, n - 1)",
        "q1": "Why is the step `k = k % len(nums)` essential before rotating?",
        "q1_opts": [
            {"id": "A", "label": "Rotating an array of length N by N full cycles produces the identical original array; modulo eliminates redundant full rotations"},
            {"id": "B", "label": "To convert negative values of k into positive values"},
            {"id": "C", "label": "Because Python slice indices must be smaller than 10"},
            {"id": "D", "label": "To round k down to the nearest even number"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! If N = 5 and K = 12, rotating 12 times is identical to rotating 12 % 5 = 2 times. Modulo prevents out-of-bounds indexing.",
            "B": "Incorrect: In Python k % n handles negative numbers, but the primary reason is eliminating redundant full cycles.",
            "C": "Incorrect: Slices have no such limitation.",
            "D": "Incorrect: K can be odd or even."
        },
        "q2": "What is the memory complexity of the Triple-Reversal rotation algorithm?",
        "q2_opts": [
            {"id": "A", "label": "O(1) auxiliary space because pointer swaps mutate the original array in-place"},
            {"id": "B", "label": "O(N) auxiliary space because elements are copied into temporary lists"},
            {"id": "C", "label": "O(K) auxiliary space"},
            {"id": "D", "label": "O(log N) auxiliary space"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! Elements are swapped directly within the existing buffer using two integer pointer indices; zero new lists are created.",
            "B": "Incorrect: Slicing creates new lists, but triple reversal does not.",
            "C": "Incorrect: K does not dictate memory allocation.",
            "D": "Incorrect: The reversal helper is iterative, using O(1) stack frames."
        },
        "practice_task": "Debug off-by-one errors in in-place array triple reversal.",
        "starter": "# Day 44 Debugging Challenge: Array Rotation\n# BUG REPORT: This rotation function crashes with IndexError because boundary indices are off by one!\ndef rotate_buggy(nums: list[int], k: int) -> list[int]:\n    n = len(nums)\n    k %= n\n    def reverse(l, r):\n        while l < r:\n            nums[l], nums[r] = nums[r], nums[l]\n            l += 1\n            r -= 1\n    # BUG: Passing n instead of n - 1 causes IndexError!\n    reverse(0, n)\n    reverse(0, k)\n    reverse(k, n)\n    return nums\n\n# INSTRUCTION: Fix the boundary calls to pass valid inclusive indices.\nnums = [1, 2, 3, 4, 5, 6, 7]\nprint('Rotated:', rotate_buggy(nums, 3))\n",
        "solution": "def rotate_buggy(nums: list[int], k: int) -> list[int]:\n    n = len(nums)\n    k %= n\n    def reverse(l, r):\n        while l < r:\n            nums[l], nums[r] = nums[r], nums[l]\n            l += 1\n            r -= 1\n    reverse(0, n - 1)\n    reverse(0, k - 1)\n    reverse(k, n - 1)\n    return nums\n\nnums = [1, 2, 3, 4, 5, 6, 7]\nprint('Rotated:', rotate_buggy(nums, 3))\n",
        "patterns": ["Rotated: [5, 6, 7, 1, 2, 3, 4]"],
        "hint": "Change `reverse(0, n)` to `reverse(0, n - 1)`, `reverse(0, k)` to `reverse(0, k - 1)`, and `reverse(k, n)` to `reverse(k, n - 1)`.",
        "recap": [
            {"concept": "Triple Reversal Order", "naiveIntuition": "Shift elements one by one K times in O(N * K)", "pythonReality": "Reversing [0..N-1], [0..K-1], and [K..N-1] achieves the rotation in O(N) time and O(1) space"},
            {"concept": "Inclusive Indices", "naiveIntuition": "Pass len(nums) as right pointer", "pythonReality": "In-place pointer reversal uses inclusive indices: right boundary is len(nums) - 1"}
        ]
    },
    45: {
        "summary": "String Parsing and Deterministic Finite Automata (DFA) model transitions between formal parser states (Whitespace, Sign, Digits) to parse tokens robustly.",
        "mechanics": "In string-to-integer (atoi): define states: 0=START, 1=SIGN, 2=IN_NUM. Handle whitespace, optional '+' or '-', parse consecutive digits with 32-bit clamping [-2^31, 2^31 - 1].",
        "takeaway": "DFA state machines structure complex string parsing logic, eliminating fragile nested conditional branching.",
        "sample_code": "# DFA State Machine for string-to-integer\ndef my_atoi(s):\n    s = s.strip()\n    if not s: return 0\n    sign = -1 if s[0] == '-' else 1\n    if s[0] in '+-': s = s[1:]\n    res = 0\n    for ch in s:\n        if not ch.isdigit(): break\n        res = res * 10 + int(ch)\n    res *= sign\n    return max(-2**31, min(2**31 - 1, res))",
        "q1": "Why is a Deterministic Finite Automaton (DFA) preferred over chained regular expressions for complex token parsing in high-throughput systems?",
        "q1_opts": [
            {"id": "A", "label": "DFAs parse character by character in guaranteed O(N) time without catastrophic backtracking regex stalls"},
            {"id": "B", "label": "DFAs use less RAM because they do not support strings"},
            {"id": "C", "label": "Regular expressions cannot match numeric characters"},
            {"id": "D", "label": "DFAs automatically handle 64-bit integer overflows"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! A DFA processes each character exactly once in O(1) state transition time, preventing exponential regex backtracking vulnerabilities (ReDoS).",
            "B": "Incorrect: DFAs operate on string streams.",
            "C": "Incorrect: Regex matches digits via \\d.",
            "D": "Incorrect: Clamping must be implemented explicitly in the accumulator logic."
        },
        "q2": "What are the 32-bit signed integer minimum and maximum clamping limits in standard coding challenges?",
        "q2_opts": [
            {"id": "A", "label": "-2^31 (-2,147,483,648) and 2^31 - 1 (2,147,483,647)"},
            {"id": "B", "label": "-2^32 and 2^32"},
            {"id": "C", "label": "0 and 2^31"},
            {"id": "D", "label": "-1,000,000 and 1,000,000"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! Standard two's complement 32-bit signed integers span -2,147,483,648 to 2,147,483,647.",
            "B": "Incorrect: 2^32 is unsigned 32-bit width.",
            "C": "Incorrect: Signed integers include negative ranges.",
            "D": "Incorrect: Arbitrary decimal constants do not match hardware boundaries."
        },
        "practice_task": "Build a robust string-to-integer (atoi) parser with sign handling and clamping.",
        "starter": "def my_atoi(s: str) -> int:\n    # TODO: Implement string-to-integer conversion\n    # 1. Discard leading whitespace\n    # 2. Check for optional '+' or '-'\n    # 3. Read consecutive digits and convert\n    # 4. Clamp within [-2**31, 2**31 - 1]\n    return 0\n\nprint('Test 1:', my_atoi('   -42'))\nprint('Test 2:', my_atoi('4193 with words'))\nprint('Test 3:', my_atoi('-91283472332'))\n",
        "solution": "def my_atoi(s: str) -> int:\n    s = s.strip()\n    if not s:\n        return 0\n    sign = 1\n    idx = 0\n    if s[0] == '-':\n        sign = -1\n        idx = 1\n    elif s[0] == '+':\n        idx = 1\n    res = 0\n    while idx < len(s) and s[idx].isdigit():\n        res = res * 10 + (ord(s[idx]) - ord('0'))\n        idx += 1\n    res *= sign\n    INT_MIN, INT_MAX = -2**31, 2**31 - 1\n    if res < INT_MIN:\n        return INT_MIN\n    if res > INT_MAX:\n        return INT_MAX\n    return res\n\nprint('Test 1:', my_atoi('   -42'))\nprint('Test 2:', my_atoi('4193 with words'))\nprint('Test 3:', my_atoi('-91283472332'))\n",
        "patterns": ["Test 1: -42", "Test 2: 4193", "Test 3: -2147483648"],
        "hint": "Strip whitespace, check sign, accumulate digits with res = res * 10 + int(ch), then clamp between -2**31 and 2**31 - 1.",
        "recap": [
            {"concept": "Digit Parsing", "naiveIntuition": "int(s) parses all valid strings", "pythonReality": "int('4193 with words') raises ValueError; manual state machine stops cleanly at non-digits"},
            {"concept": "Clamping", "naiveIntuition": "Python handles huge integers automatically", "pythonReality": "Python integers have arbitrary precision, but interview specifications mandate explicit 32-bit hardware clamping"}
        ]
    },
    46: {
        "summary": "Palindrome Verification uses opposing two pointers, while finding the Longest Palindromic Substring expands outward around 2N - 1 possible centers in O(N^2) time and O(1) space.",
        "mechanics": "A string of length N has N single-character centers (odd palindromes 'aba') and N - 1 two-character center gaps (even palindromes 'abba'). Expanding outward verifies mirror equality.",
        "takeaway": "Expanding around 2N - 1 centers identifies all palindromic substrings in O(N^2) time and O(1) auxiliary memory.",
        "sample_code": "# Expand around center\ndef expand(s, l, r):\n    while l >= 0 and r < len(s) and s[l] == s[r]:\n        l -= 1; r += 1\n    return s[l + 1:r]",
        "q1": "Why are there 2N - 1 potential centers in a string of length N?",
        "q1_opts": [
            {"id": "A", "label": "There are N character centers for odd-length palindromes and N - 1 inter-character gaps for even-length palindromes"},
            {"id": "B", "label": "Because strings are indexed from -N to N - 1 in Python"},
            {"id": "C", "label": "Every palindrome must contain at least 2 centers"},
            {"id": "D", "label": "It accounts for uppercase and lowercase ASCII characters"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! An odd-length palindrome like 'aba' centers on 'b' (N positions). An even-length palindrome like 'abba' centers between 'b' and 'b' (N - 1 positions). Total = 2N - 1.",
            "B": "Incorrect: Negative indexing is a syntax feature, not a structural count of symmetry axes.",
            "C": "Incorrect: Odd palindromes have a single middle character.",
            "D": "Incorrect: Case sensitivity is unrelated to center count."
        },
        "q2": "What is the time complexity of the Expand Around Center algorithm for finding the longest palindromic substring?",
        "q2_opts": [
            {"id": "A", "label": "O(N^2) time and O(1) auxiliary space"},
            {"id": "B", "label": "O(N^3) time and O(N) space"},
            {"id": "C", "label": "O(N log N) time"},
            {"id": "D", "label": "O(N) time and O(N) space"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! There are 2N - 1 centers, and each expansion extends at most O(N) steps. Total time: O(N^2). Auxiliary space is O(1) because only boundary pointers are stored.",
            "B": "Incorrect: Brute-force substring checking is O(N^3), but expanding around centers avoids the third loop.",
            "C": "Incorrect: No divide-and-conquer sorting is performed.",
            "D": "Incorrect: Linear O(N) requires Manacher's algorithm."
        },
        "practice_task": "Find the longest palindromic substring via center expansion.",
        "starter": "def longest_palindrome(s: str) -> str:\n    if not s:\n        return ''\n    # TODO: Helper function to expand around (l, r) and return longest palindrome\n    # Loop i through range(len(s)), expanding around (i, i) and (i, i + 1)\n    return ''\n\ns = 'babad'\nprint('Longest palindrome:', longest_palindrome(s))\n",
        "solution": "def longest_palindrome(s: str) -> str:\n    if not s:\n        return ''\n    def expand(l: int, r: int) -> str:\n        while l >= 0 and r < len(s) and s[l] == s[r]:\n            l -= 1\n            r += 1\n        return s[l + 1:r]\n    longest = ''\n    for i in range(len(s)):\n        p1 = expand(i, i)\n        p2 = expand(i, i + 1)\n        if len(p1) > len(longest):\n            longest = p1\n        if len(p2) > len(longest):\n            longest = p2\n    return longest\n\ns = 'babad'\nprint('Longest palindrome:', longest_palindrome(s))\n",
        "patterns": ["Longest palindrome: bab"],
        "hint": "Write helper `expand(l, r)` that loops `while l >= 0 and r < len(s) and s[l] == s[r]: l -= 1; r += 1; return s[l+1:r]`.",
        "recap": [
            {"concept": "Center Duality", "naiveIntuition": "Only expand around single characters", "pythonReality": "Must expand around both single characters (i, i) and adjacent pairs (i, i + 1)"},
            {"concept": "Slice Boundary", "naiveIntuition": "Return s[l:r]", "pythonReality": "When loop terminates, s[l] != s[r]; valid palindrome boundaries are l + 1 up to r"}
        ]
    },
    47: {
        "summary": "2D Matrix Spiral Order Traversal navigates outer boundaries inward, shifting top, bottom, left, and right boundary variables to visit all M x N elements without memory allocation.",
        "mechanics": "1. Traverse top row (left to right), increment top. 2. Traverse right col (top to bottom), decrement right. 3. If top <= bottom, traverse bottom row (right to left), decrement bottom. 4. If left <= right, traverse left col (bottom to top), increment left.",
        "takeaway": "Maintain four boundary limits and verify boundary crossing invariants on every direction transition.",
        "sample_code": "# Spiral Matrix Traversal\ndef spiral_order(matrix):\n    if not matrix: return []\n    res = []\n    T, B, L, R = 0, len(matrix) - 1, 0, len(matrix[0]) - 1\n    while T <= B and L <= R:\n        for c in range(L, R + 1): res.append(matrix[T][c])\n        T += 1\n        for r in range(T, B + 1): res.append(matrix[r][R])\n        R -= 1\n        if T <= B:\n            for c in range(R, L - 1, -1): res.append(matrix[B][c])\n            B -= 1\n        if L <= R:\n            for r in range(B, T - 1, -1): res.append(matrix[r][L])\n            L += 1\n    return res",
        "q1": "Why must we verify `if T <= B` before traversing the bottom row from right to left in spiral traversal?",
        "q1_opts": [
            {"id": "A", "label": "Because incrementing T in the first step might cause T to exceed B on single-row matrices, causing duplicate row visits"},
            {"id": "B", "label": "To check if the matrix elements are sorted"},
            {"id": "C", "label": "Because range() crashes if stop is smaller than start"},
            {"id": "D", "label": "To handle negative coordinate indices"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! If a matrix has 1 row (T=0, B=0), after traversing right, T becomes 1. Without `if T <= B`, the bottom traversal would re-visit row 0 in reverse!",
            "B": "Incorrect: Spiral order applies to any matrix regardless of sorting.",
            "C": "Incorrect: range with step -1 handles start > stop gracefully.",
            "D": "Incorrect: Indices are non-negative."
        },
        "q2": "What is the time and auxiliary space complexity of spiral matrix traversal?",
        "q2_opts": [
            {"id": "A", "label": "O(M * N) time and O(1) auxiliary space (excluding output buffer)"},
            {"id": "B", "label": "O(M + N) time and O(M * N) space"},
            {"id": "C", "label": "O(N^2) time and O(N) space"},
            {"id": "D", "label": "O(M * N log(M * N)) time"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! Every cell is visited exactly once, requiring O(M * N) time. Auxiliary space is O(1) as only 4 boundary integers are stored.",
            "B": "Incorrect: Must visit all M * N cells, which is O(M * N).",
            "C": "Incorrect: M and N may differ.",
            "D": "Incorrect: No sorting or divide-and-conquer is involved."
        },
        "practice_task": "Traverse an M x N matrix in clockwise spiral order.",
        "starter": "def spiral_order(matrix: list[list[int]]) -> list[int]:\n    if not matrix or not matrix[0]:\n        return []\n    res = []\n    top, bottom = 0, len(matrix) - 1\n    left, right = 0, len(matrix[0]) - 1\n    # TODO: While top <= bottom and left <= right, execute the 4 boundary passes\n    \n    return res\n\nmatrix = [\n    [1, 2, 3],\n    [4, 5, 6],\n    [7, 8, 9]\n]\nprint('Spiral order:', spiral_order(matrix))\n",
        "solution": "def spiral_order(matrix: list[list[int]]) -> list[int]:\n    if not matrix or not matrix[0]:\n        return []\n    res = []\n    top, bottom = 0, len(matrix) - 1\n    left, right = 0, len(matrix[0]) - 1\n    while top <= bottom and left <= right:\n        for c in range(left, right + 1):\n            res.append(matrix[top][c])\n        top += 1\n        for r in range(top, bottom + 1):\n            res.append(matrix[r][right])\n        right -= 1\n        if top <= bottom:\n            for c in range(right, left - 1, -1):\n                res.append(matrix[bottom][c])\n            bottom -= 1\n        if left <= right:\n            for r in range(bottom, top - 1, -1):\n                res.append(matrix[r][left])\n            left += 1\n    return res\n\nmatrix = [\n    [1, 2, 3],\n    [4, 5, 6],\n    [7, 8, 9]\n]\nprint('Spiral order:', spiral_order(matrix))\n",
        "patterns": ["Spiral order: [1, 2, 3, 6, 9, 8, 7, 4, 5]"],
        "hint": "Follow the four passes: left to right on top, top to bottom on right, right to left on bottom (guarded by top <= bottom), and bottom to top on left (guarded by left <= right).",
        "recap": [
            {"concept": "Boundary Contraction", "naiveIntuition": "Track visited coordinates in a hash set", "pythonReality": "Four integer boundary boundaries (top, bottom, left, right) simulate the shrinking spiral in O(1) space"},
            {"concept": "Single-Row Guard", "naiveIntuition": "The while loop condition is sufficient", "pythonReality": "top and right mutate midway through an iteration; inner guards are mandatory to prevent single-row duplicate passes"}
        ]
    },
    48: {
        "summary": "Rotating an N x N matrix 90 degrees clockwise in-place is achieved by a 2-step geometric transformation: transpose the matrix across its main diagonal, then reverse every row horizontally.",
        "mechanics": "Step 1 (Transpose): Swap matrix[i][j] with matrix[j][i] for all j > i. This flips rows into columns. Step 2 (Reverse Rows): Reverse each row in-place via two pointers or row.reverse(). Both steps run strictly in O(N^2) time with O(1) auxiliary space.",
        "takeaway": "Clockwise 90-degree rotation = Transpose + Horizontal Row Reversal in O(1) space.",
        "sample_code": "# In-place 90 degree clockwise matrix rotation\ndef rotate_matrix(mat):\n    n = len(mat)\n    # 1. Transpose: flip across main diagonal\n    for i in range(n):\n        for j in range(i + 1, n):\n            mat[i][j], mat[j][i] = mat[j][i], mat[i][j]\n    # 2. Reverse each row\n    for row in mat:\n        row.reverse()\n    return mat",
        "q1": "Why does transposing a matrix followed by reversing each row achieve a 90-degree clockwise rotation?",
        "q1_opts": [
            {"id": "A", "label": "Transposing converts cell (r, c) to (c, r), and reversing the row maps column index c to (N - 1 - c), resulting in (r, c) -> (c, N - 1 - r)"},
            {"id": "B", "label": "Because reversing rows multiplies the matrix by -1"},
            {"id": "C", "label": "Because transposing shifts all cells diagonally left"},
            {"id": "D", "label": "It only works for identity matrices"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! In a 90-degree clockwise turn, cell (r, c) must land at (c, N - 1 - r). Transpose places (r, c) at (c, r), and reversing row c moves column r to N - 1 - r. The composition yields exact clockwise rotation in-place.",
            "B": "Incorrect: Row reversal rearranges columns; it does not negate numeric values.",
            "C": "Incorrect: Transposing reflects across the main diagonal.",
            "D": "Incorrect: Transpose + reverse works on any square N x N matrix."
        },
        "q2": "What is the auxiliary space complexity of rotating an N x N matrix in-place using Transpose + Reverse?",
        "q2_opts": [
            {"id": "A", "label": "O(1) auxiliary space, modifying the existing matrix buffers directly"},
            {"id": "B", "label": "O(N^2) auxiliary space"},
            {"id": "C", "label": "O(N) auxiliary space"},
            {"id": "D", "label": "O(log N) stack space"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! Swapping elements in-place requires only a single temporary variable during assignment, achieving strict O(1) extra space.",
            "B": "Incorrect: Creating a new rotated matrix takes O(N^2), but the in-place method uses O(1).",
            "C": "Incorrect: Zero extra row arrays are allocated.",
            "D": "Incorrect: The algorithm is purely iterative with zero recursion."
        },
        "practice_task": "Rotate an N x N matrix 90 degrees clockwise in-place.",
        "starter": "def rotate(matrix: list[list[int]]) -> None:\n    n = len(matrix)\n    # TODO 1: Transpose matrix in-place (swap matrix[i][j] and matrix[j][i] for j > i)\n    \n    # TODO 2: Reverse each row in-place\n    pass\n\nmat = [\n    [1, 2, 3],\n    [4, 5, 6],\n    [7, 8, 9]\n]\nrotate(mat)\nprint('Rotated matrix:', mat)\n",
        "solution": "def rotate(matrix: list[list[int]]) -> None:\n    n = len(matrix)\n    for i in range(n):\n        for j in range(i + 1, n):\n            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]\n    for row in matrix:\n        row.reverse()\n\nmat = [\n    [1, 2, 3],\n    [4, 5, 6],\n    [7, 8, 9]\n]\nrotate(mat)\nprint('Rotated matrix:', mat)\n",
        "patterns": ["Rotated matrix: [[7, 4, 1], [8, 5, 2], [9, 6, 3]]"],
        "hint": "Loop i from 0 to n-1 and j from i+1 to n-1: swap matrix[i][j], matrix[j][i]. Then for row in matrix: row.reverse().",
        "recap": [
            {"concept": "Transpose + Reverse Invariant", "naiveIntuition": "Allocate a new N x N matrix and copy cells (O(N^2) space)", "pythonReality": "Transposing across diagonal followed by reversing rows achieves 90-degree clockwise rotation strictly in-place with O(1) extra memory"},
            {"concept": "Diagonal Invariant", "naiveIntuition": "Loop through all i and all j during transpose", "pythonReality": "Looping j from i+1 to n-1 ensures each pair is swapped exactly once; looping all j would un-swap elements back to original"}
        ]
    },
    49: {
        "summary": "Interval Problems require sorting intervals by start times (or end times) so overlapping relationships can be evaluated monotonically in O(N log N) time.",
        "mechanics": "Sort intervals by start time. Maintain merged = [intervals[0]]. For each curr: if curr.start <= merged[-1].end: merged[-1].end = max(merged[-1].end, curr.end) (overlap). Else: merged.append(curr).",
        "takeaway": "Sorting intervals unlocks linear merge passes; overlap is tested via curr.start <= prev.end.",
        "sample_code": "# Merge Overlapping Intervals\ndef merge_intervals(intervals):\n    intervals.sort(key=lambda x: x[0])\n    merged = [intervals[0]]\n    for curr in intervals[1:]:\n        if curr[0] <= merged[-1][1]:\n            merged[-1][1] = max(merged[-1][1], curr[1])\n        else:\n            merged.append(curr)\n    return merged",
        "q1": "Why is sorting by start time necessary before merging overlapping intervals?",
        "q1_opts": [
            {"id": "A", "label": "It guarantees that any interval that can overlap with the current merged interval appears immediately next in the sequence"},
            {"id": "B", "label": "Because Python's sort() function runs in O(N) time"},
            {"id": "C", "label": "To ensure intervals are sorted in descending order of length"},
            {"id": "D", "label": "It is not necessary; intervals can be merged in random order"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! Sorting establishes temporal monotonicity: once an interval starts after the current merged end time, no subsequent interval can ever overlap with the current merged interval.",
            "B": "Incorrect: Comparison sort takes O(N log N).",
            "C": "Incorrect: Length is not used as the primary sort key.",
            "D": "Incorrect: Without sorting, finding all overlapping components requires O(N^2) pairwise checks."
        },
        "q2": "When two intervals [start1, end1] and [start2, end2] overlap (start2 <= end1), what is the new merged end time?",
        "q2_opts": [
            {"id": "A", "label": "max(end1, end2)"},
            {"id": "B", "label": "end2"},
            {"id": "C", "label": "end1 + end2"},
            {"id": "D", "label": "min(end1, end2)"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! The second interval might be completely contained within the first (e.g. [1, 5] and [2, 3]), so the merged end must be the maximum of both ends.",
            "B": "Incorrect: If end2 < end1, using end2 would incorrectly shrink the interval.",
            "C": "Incorrect: Summing ends falsely extends the interval duration.",
            "D": "Incorrect: Minimum calculates intersection, not union merge."
        },
        "practice_task": "Merge all overlapping intervals in an input collection.",
        "starter": "def merge(intervals: list[list[int]]) -> list[list[int]]:\n    if not intervals:\n        return []\n    # TODO 1: Sort intervals by start time\n    # TODO 2: Initialize merged list with first interval\n    # TODO 3: Iterate and merge when curr[0] <= merged[-1][1]\n    return []\n\nintervals = [[1, 3], [2, 6], [8, 10], [15, 18]]\nprint('Merged:', merge(intervals))\n",
        "solution": "def merge(intervals: list[list[int]]) -> list[list[int]]:\n    if not intervals:\n        return []\n    intervals.sort(key=lambda x: x[0])\n    merged = [intervals[0]]\n    for curr in intervals[1:]:\n        if curr[0] <= merged[-1][1]:\n            merged[-1][1] = max(merged[-1][1], curr[1])\n        else:\n            merged.append(curr)\n    return merged\n\nintervals = [[1, 3], [2, 6], [8, 10], [15, 18]]\nprint('Merged:', merge(intervals))\n",
        "patterns": ["Merged: [[1, 6], [8, 10], [15, 18]]"],
        "hint": "Sort by lambda x: x[0], initialize merged = [intervals[0]], loop checking if curr[0] <= merged[-1][1] and update merged[-1][1] = max(merged[-1][1], curr[1]).",
        "recap": [
            {"concept": "Interval Sorting", "naiveIntuition": "Compare all pairs to find overlaps O(N^2)", "pythonReality": "Sorting by start time in O(N log N) allows a single linear O(N) sweep to merge all overlapping segments"},
            {"concept": "Contained Interval", "naiveIntuition": "Always set end to curr[1]", "pythonReality": "If curr is completely inside merged[-1], max(merged[-1][1], curr[1]) prevents shrinking the end boundary"}
        ]
    },
    50: {
        "summary": "Section 4 Capstone integrates prefix sums, two pointers, sliding windows, and interval merges into a calendar booking management engine.",
        "mechanics": "The calendar engine accepts booking intervals [start, end), detects conflicts in O(log N) time, computes peak concurrent meetings using boundary event scan-lines, and answers range queries.",
        "takeaway": "Combining contiguous array techniques enables high-performance scheduling and analytical systems.",
        "sample_code": "# Boundary Event Scan-line for Max Concurrent Meetings\ndef max_concurrent(meetings):\n    events = []\n    for s, e in meetings:\n        events.append((s, 1))  # Start: +1 meeting\n        events.append((e, -1)) # End: -1 meeting\n    events.sort(key=lambda x: (x[0], x[1])) # If times match, end (-1) before start (+1)\n    curr = best = 0\n    for time, delta in events:\n        curr += delta\n        best = max(best, curr)\n    return best",
        "q1": "In the boundary event scan-line algorithm, if a meeting ends at 10 and another starts at 10, how should events be sorted?",
        "q1_opts": [
            {"id": "A", "label": "End event (-1) should be processed before start event (+1) if meetings touching at endpoints do not conflict"},
            {"id": "B", "label": "Start event (+1) must always precede end event"},
            {"id": "C", "label": "Order does not matter"},
            {"id": "D", "label": "Sort strictly by meeting duration"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! If interval [9, 10) and [10, 11) share endpoint 10, processing end (-1) first drops the room count before the new meeting (+1) claims it.",
            "B": "Incorrect: Processing +1 first creates a false peak of 2 concurrent meetings at time 10.",
            "C": "Incorrect: Tie-breaking order directly changes the computed peak.",
            "D": "Incorrect: Time alignment requires sorting on timestamp."
        },
        "q2": "What is the time complexity of the boundary event scan-line algorithm for N meetings?",
        "q2_opts": [
            {"id": "A", "label": "O(N log N) to sort 2N boundary events, followed by an O(N) sweep"},
            {"id": "B", "label": "O(N^2) pairwise comparisons"},
            {"id": "C", "label": "O(N) with no sorting required"},
            {"id": "D", "label": "O(1) auxiliary space"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! Generating 2N event tuples and sorting them takes O(N log N) time; the single linear pass takes O(N). Total: O(N log N).",
            "B": "Incorrect: The event scan-line avoids quadratic comparisons.",
            "C": "Incorrect: Events must be ordered chronologically.",
            "D": "Incorrect: The event list requires O(N) auxiliary space."
        },
        "practice_task": "Architect a Meeting Room Scheduler computing maximum concurrent active meetings.",
        "starter": "def min_meeting_rooms(intervals: list[list[int]]) -> int:\n    # TODO 1: Create events array with (start, 1) and (end, -1)\n    # TODO 2: Sort events by time; tie-break: end (-1) before start (1)\n    # TODO 3: Track running sum and find maximum concurrent rooms\n    return 0\n\nmeetings = [[0, 30], [5, 10], [15, 20]]\nprint('Min meeting rooms needed:', min_meeting_rooms(meetings))\n",
        "solution": "def min_meeting_rooms(intervals: list[list[int]]) -> int:\n    events = []\n    for start, end in intervals:\n        events.append((start, 1))\n        events.append((end, -1))\n    events.sort(key=lambda x: (x[0], x[1]))\n    curr_rooms = 0\n    max_rooms = 0\n    for time, delta in events:\n        curr_rooms += delta\n        if curr_rooms > max_rooms:\n            max_rooms = curr_rooms\n    return max_rooms\n\nmeetings = [[0, 30], [5, 10], [15, 20]]\nprint('Min meeting rooms needed:', min_meeting_rooms(meetings))\n",
        "patterns": ["Min meeting rooms needed: 2"],
        "hint": "Append (s, 1) and (e, -1). Sort by lambda x: (x[0], x[1]). Accumulate delta and record maximum.",
        "recap": [
            {"concept": "Boundary Scan-Line", "naiveIntuition": "Simulate every minute on a timeline", "pythonReality": "Discrete event scan-line only visits start and end timestamps in O(N log N), handling infinite time bounds"},
            {"concept": "Section 4 Synthesis", "naiveIntuition": "Array algorithms are independent tricks", "pythonReality": "Prefix sums, two pointers, sliding windows, and event sorting form an interconnected toolbox for contiguous data"}
        ]
    }
}
