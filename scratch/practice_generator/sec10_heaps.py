"""
Practice Problems for Section 10 (Heaps & Priority Queues)
Total problems: 8
"""

def P(slug, title, topic, tier, entry, statement, constraints,
      opt_t, opt_s, starter, cases, reference_solution=""):
    return {
        "slug": slug, "title": title, "topic": topic, "difficulty_tier": tier,
        "entry_point": entry, "statement_md": statement, "constraints_md": constraints,
        "optimal_time": opt_t, "optimal_space": opt_s,
        "starter_code": {"python": starter}, "test_cases": cases,
        "reference_solution": reference_solution,
    }

SEC10_HEAPS_PROBLEMS = [
    P(
        "last-stone-weight", "Last Stone Weight (Max-Heap)", "heaps", 1, "last_stone_weight",
        "You are given an array of integers `stones` where `stones[i]` is the weight of the `i`th stone.\n\nWe play a game with the stones: on each turn, we choose the heaviest two stones and smash them together. If `x == y`, both are destroyed. If `x != y`, the stone of weight `x` is destroyed, and the stone of weight `y` has new weight `y - x`. Return the weight of the last remaining stone, or `0` if none remain.",
        "- `1 <= len(stones) <= 30`\n- `1 <= stones[i] <= 1000`",
        "O(n log n)", "O(n)",
        "def last_stone_weight(stones: list[int]) -> int:\n    pass\n",
        [
            {"args": [[2, 7, 4, 1, 8, 1]], "expected": 1},
            {"args": [[1]], "expected": 1},
            {"args": [[2, 2]], "expected": 0},
            {"args": [[10, 4, 2, 10]], "expected": 2},
            {"args": [[3, 7, 2]], "expected": 2}
        ],
        "import heapq\n\ndef last_stone_weight(stones: list[int]) -> int:\n    heap = [-s for s in stones]\n    heapq.heapify(heap)\n    while len(heap) > 1:\n        s1 = -heapq.heappop(heap)\n        s2 = -heapq.heappop(heap)\n        if s1 != s2:\n            heapq.heappush(heap, -(s1 - s2))\n    return -heap[0] if heap else 0\n"
    ),

    P(
        "kth-largest-element-in-a-stream", "Kth Largest Element in a Stream (Min-Heap)", "heaps", 2, "simulate_kth_largest_stream",
        "Design a class to find the `k`th largest element in a stream. Given integer `k`, initial integer list `nums`, and a sequence of additions `adds`, return the list of `k`th largest elements after each add.\n\nMaintain a min-heap of size $K$.",
        "- `1 <= k <= 10^4`\n- `0 <= len(nums) <= 10^4`\n- `-10^4 <= val <= 10^4`",
        "O(log k) per add", "O(k)",
        "def simulate_kth_largest_stream(k: int, nums: list[int], adds: list[int]) -> list[int]:\n    pass\n",
        [
            {"args": [3, [4, 5, 8, 2], [3, 5, 10, 9, 4]], "expected": [4, 5, 5, 8, 8]},
            {"args": [1, [], [-3, -2, -4, 0, 4]], "expected": [-3, -2, -2, 0, 4]},
            {"args": [2, [0], [-1, 1, -2, 2]], "expected": [-1, 0, 0, 1]}
        ],
        "import heapq\n\ndef simulate_kth_largest_stream(k: int, nums: list[int], adds: list[int]) -> list[int]:\n    heap = list(nums)\n    heapq.heapify(heap)\n    while len(heap) > k:\n        heapq.heappop(heap)\n    res = []\n    for val in adds:\n        heapq.heappush(heap, val)\n        if len(heap) > k:\n            heapq.heappop(heap)\n        res.append(heap[0])\n    return res\n"
    ),

    P(
        "top-k-frequent-elements", "Top K Frequent Elements (Heap / Bucket)", "heaps", 2, "top_k_frequent",
        "Given an integer array `nums` and an integer `k`, return the `k` most frequent elements. Return the result sorted in ascending order.\n\nYou may assume the answer is unique.",
        "- `1 <= len(nums) <= 10^5`\n- `k` is in range `[1, number of unique elements]`",
        "O(n log k)", "O(n)",
        "def top_k_frequent(nums: list[int], k: int) -> list[int]:\n    pass\n",
        [
            {"args": [[1, 1, 1, 2, 2, 3], 2], "expected": [1, 2]},
            {"args": [[1], 1], "expected": [1]},
            {"args": [[4, 1, -1, 2, -1, 2, 3], 2], "expected": [-1, 2]},
            {"args": [[1, 2, 3], 3], "expected": [1, 2, 3]}
        ],
        "from collections import Counter\n\ndef top_k_frequent(nums: list[int], k: int) -> list[int]:\n    counts = Counter(nums)\n    most = [item for item, _ in counts.most_common(k)]\n    return sorted(most)\n"
    ),

    P(
        "merge-k-sorted-lists", "Merge k Sorted Lists (Min-Heap Priority Queue)", "heaps", 4, "merge_k_lists",
        "You are given an array of `k` linked-lists `lists`, each linked-list is sorted in ascending order. Merge all the linked-lists into one sorted list and return it.\n\nSolve this in $O(N \\log k)$ time using a min-heap.",
        "- `k == len(lists)`\n- `0 <= k <= 10^4`\n- `0 <= len(lists[i]) <= 500`\n- `-10^4 <= lists[i][j] <= 10^4`",
        "O(N log k)", "O(k)",
        "def merge_k_lists(lists: list[list[int]]) -> list[int]:\n    pass\n",
        [
            {"args": [[[1, 4, 5], [1, 3, 4], [2, 6]]], "expected": [1, 1, 2, 3, 4, 4, 5, 6]},
            {"args": [[]], "expected": []},
            {"args": [[[]]], "expected": []},
            {"args": [[[1], [0]]], "expected": [0, 1]},
            {"args": [[[2, 3], [], [1]]], "expected": [1, 2, 3]}
        ],
        "import heapq\n\ndef merge_k_lists(lists: list[list[int]]) -> list[int]:\n    heap = []\n    for i, lst in enumerate(lists):\n        if lst:\n            heapq.heappush(heap, (lst[0], i, 0))\n    res = []\n    while heap:\n        val, list_idx, elem_idx = heapq.heappop(heap)\n        res.append(val)\n        if elem_idx + 1 < len(lists[list_idx]):\n            next_val = lists[list_idx][elem_idx + 1]\n            heapq.heappush(heap, (next_val, list_idx, elem_idx + 1))\n    return res\n"
    ),

    P(
        "find-median-from-data-stream", "Find Median from Data Stream (Dual-Heap)", "heaps", 5, "running_median",
        "The median is the middle value in an ordered integer list. Implement running median over a sequence of numbers `nums`.\n\nReturn the list of medians after each insertion, with each median rounded to 1 decimal place. Use two heaps: a max-heap for the lower half and a min-heap for the upper half.",
        "- `1 <= len(nums) <= 10^4`\n- `-10^5 <= nums[i] <= 10^5`",
        "O(n log n)", "O(n)",
        "def running_median(nums: list[int]) -> list[float]:\n    pass\n",
        [
            {"args": [[2, 1, 5, 7, 2, 0, 5]], "expected": [2.0, 1.5, 2.0, 3.5, 2.0, 2.0, 2.0]},
            {"args": [[1]], "expected": [1.0]},
            {"args": [[1, 2]], "expected": [1.0, 1.5]},
            {"args": [[1, 2, 3]], "expected": [1.0, 1.5, 2.0]},
            {"args": [[6, 10, 2, 6, 5, 0, 6, 3, 1, 0, 0]], "expected": [6.0, 8.0, 6.0, 6.0, 6.0, 5.5, 6.0, 5.5, 5.0, 4.0, 3.0]}
        ],
        "import heapq\n\ndef running_median(nums: list[int]) -> list[float]:\n    small = []  # max-heap (negated)\n    large = []  # min-heap\n    res = []\n    for num in nums:\n        heapq.heappush(small, -num)\n        if small and large and (-small[0] > large[0]):\n            val = -heapq.heappop(small)\n            heapq.heappush(large, val)\n        if len(small) > len(large) + 1:\n            val = -heapq.heappop(small)\n            heapq.heappush(large, val)\n        elif len(large) > len(small):\n            val = heapq.heappop(large)\n            heapq.heappush(small, -val)\n        if len(small) > len(large):\n            res.append(round(float(-small[0]), 1))\n        else:\n            res.append(round((-small[0] + large[0]) / 2.0, 1))\n    return res\n"
    ),

    P(
        "task-scheduler", "Task Scheduler (Max-Heap Cooldown)", "heaps", 3, "least_interval",
        "Given a characters array `tasks`, representing the tasks a CPU needs to do, and an integer `n` as cooling intervals between identical tasks, return the least number of intervals that the CPU will take to finish all tasks.",
        "- `1 <= len(tasks) <= 10^4`\n- `tasks[i]` is uppercase English letter\n- `0 <= n <= 100`",
        "O(n)", "O(1)",
        "def least_interval(tasks: list[str], n: int) -> int:\n    pass\n",
        [
            {"args": [["A", "A", "A", "B", "B", "B"], 2], "expected": 8},
            {"args": [["A", "A", "A", "B", "B", "B"], 0], "expected": 6},
            {"args": [["A", "A", "A", "A", "A", "A", "B", "C", "D", "E", "F", "G"], 2], "expected": 16},
            {"args": [["A"], 2], "expected": 1}
        ],
        "from collections import Counter\n\ndef least_interval(tasks: list[str], n: int) -> int:\n    counts = Counter(tasks)\n    max_freq = max(counts.values())\n    max_count = sum(1 for count in counts.values() if count == max_freq)\n    return max(len(tasks), (max_freq - 1) * (n + 1) + max_count)\n"
    ),

    P(
        "k-closest-points-to-origin", "K Closest Points to Origin (Heap)", "heaps", 2, "k_closest",
        "Given an array of `points` where `points[i] = [x_i, y_i]` represents a point on the X-Y plane and an integer `k`, return the `k` closest points to the origin `(0, 0)`.\n\nThe distance between two points is Euclidean distance. Return the result sorted by distance.",
        "- `1 <= k <= len(points) <= 10^4`\n- `-10^4 <= x_i, y_i <= 10^4`",
        "O(n log k)", "O(k)",
        "def k_closest(points: list[list[int]], k: int) -> list[list[int]]:\n    pass\n",
        [
            {"args": [[[1, 3], [-2, 2]], 1], "expected": [[-2, 2]]},
            {"args": [[[3, 3], [5, -1], [-2, 4]], 2], "expected": [[3, 3], [-2, 4]]},
            {"args": [[[0, 1], [1, 0]], 2], "expected": [[0, 1], [1, 0]]}
        ],
        "def k_closest(points: list[list[int]], k: int) -> list[list[int]]:\n    points.sort(key=lambda p: p[0]**2 + p[1]**2)\n    return points[:k]\n"
    ),

    P(
        "find-k-pairs-with-smallest-sums", "Find K Pairs with Smallest Sums", "heaps", 4, "k_smallest_pairs",
        "You are given two integer arrays `nums1` and `nums2` sorted in ascending order and an integer `k`.\n\nDefine a pair `(u, v)` which consists of one element from `nums1` and one element from `nums2`. Return the `k` pairs `[u, v]` with the smallest sums.",
        "- `1 <= len(nums1), len(nums2) <= 10^4`\n- `-10^9 <= nums1[i], nums2[i] <= 10^9`\n- `1 <= k <= 1000`",
        "O(k log k)", "O(k)",
        "def k_smallest_pairs(nums1: list[int], nums2: list[int], k: int) -> list[list[int]]:\n    pass\n",
        [
            {"args": [[1, 7, 11], [2, 4, 6], 3], "expected": [[1, 2], [1, 4], [1, 6]]},
            {"args": [[1, 1, 2], [1, 2, 3], 2], "expected": [[1, 1], [1, 1]]},
            {"args": [[1, 2], [3], 3], "expected": [[1, 3], [2, 3]]}
        ],
        "import heapq\n\ndef k_smallest_pairs(nums1: list[int], nums2: list[int], k: int) -> list[list[int]]:\n    if not nums1 or not nums2 or k <= 0:\n        return []\n    heap = []\n    for i in range(min(k, len(nums1))):\n        heapq.heappush(heap, (nums1[i] + nums2[0], i, 0))\n    res = []\n    while heap and len(res) < k:\n        total, i, j = heapq.heappop(heap)\n        res.append([nums1[i], nums2[j]])\n        if j + 1 < len(nums2):\n            heapq.heappush(heap, (nums1[i] + nums2[j + 1], i, j + 1))\n    return res\n"
    )
]
