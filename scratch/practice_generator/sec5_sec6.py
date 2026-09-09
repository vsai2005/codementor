"""
Practice Problems for Section 5 (Searching & Sorting) and Section 6 (Hashing & Hash Tables)
Total problems: 12
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

SEC5_SEC6_PROBLEMS = [
    # --- Section 5: Searching & Sorting (Days 51-65) ---
    P(
        "search-insert-position", "Search Insert Position (Bisect Left)", "binary-search", 1, "search_insert",
        "Given a sorted array of distinct integers `nums` and a target value `target`, return the index if the target is found. If not, return the index where it would be if it were inserted in order.\n\nYou must write an algorithm with $O(\\log n)$ runtime complexity.",
        "- `1 <= len(nums) <= 10^4`\n- `-10^4 <= nums[i], target <= 10^4`\n- `nums` contains distinct values sorted in ascending order",
        "O(log n)", "O(1)",
        "def search_insert(nums: list[int], target: int) -> int:\n    pass\n",
        [
            {"args": [[1, 3, 5, 6], 5], "expected": 2},
            {"args": [[1, 3, 5, 6], 2], "expected": 1},
            {"args": [[1, 3, 5, 6], 7], "expected": 4},
            {"args": [[1, 3, 5, 6], 0], "expected": 0},
            {"args": [[1], 1], "expected": 0}
        ],
        "def search_insert(nums: list[int], target: int) -> int:\n    left, right = 0, len(nums) - 1\n    while left <= right:\n        mid = (left + right) // 2\n        if nums[mid] == target:\n            return mid\n        elif nums[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return left\n"
    ),

    P(
        "sort-an-array", "Sort an Array (Merge Sort Canonical)", "searching-sorting", 3, "sort_array",
        "Given an array of integers `nums`, sort the array in ascending order and return it.\n\nYou must solve the problem without using any built-in `sort()` or `sorted()` functions and with $O(n \\log n)$ time complexity.",
        "- `1 <= len(nums) <= 5 * 10^4`\n- `-5 * 10^4 <= nums[i] <= 5 * 10^4`",
        "O(n log n)", "O(n)",
        "def sort_array(nums: list[int]) -> list[int]:\n    pass\n",
        [
            {"args": [[5, 2, 3, 1]], "expected": [1, 2, 3, 5]},
            {"args": [[5, 1, 1, 2, 0, 0]], "expected": [0, 0, 1, 1, 2, 5]},
            {"args": [[1]], "expected": [1]},
            {"args": [[-4, 0, 7, 4, 9, -5, -1, 0, -7, -1]], "expected": [-7, -5, -4, -1, -1, 0, 0, 4, 7, 9]},
            {"args": [[10, -10]], "expected": [-10, 10]}
        ],
        "def sort_array(nums: list[int]) -> list[int]:\n    if len(nums) <= 1:\n        return nums\n    mid = len(nums) // 2\n    left = sort_array(nums[:mid])\n    right = sort_array(nums[mid:])\n    res = []\n    i = j = 0\n    while i < len(left) and j < len(right):\n        if left[i] <= right[j]:\n            res.append(left[i])\n            i += 1\n        else:\n            res.append(right[j])\n            j += 1\n    res.extend(left[i:])\n    res.extend(right[j:])\n    return res\n"
    ),

    P(
        "kth-largest-element-in-an-array", "Kth Largest Element in an Array (Quickselect)", "searching-sorting", 3, "find_kth_largest",
        "Given an integer array `nums` and an integer `k`, return the `k`th largest element in the array.\n\nNote that it is the `k`th largest element in the sorted order, not the `k`th distinct element. Can you solve it in $O(N)$ average time using Quickselect?",
        "- `1 <= k <= len(nums) <= 10^5`\n- `-10^4 <= nums[i] <= 10^4`",
        "O(n)", "O(1)",
        "def find_kth_largest(nums: list[int], k: int) -> int:\n    pass\n",
        [
            {"args": [[3, 2, 1, 5, 6, 4], 2], "expected": 5},
            {"args": [[3, 2, 3, 1, 2, 4, 5, 5, 6], 4], "expected": 4},
            {"args": [[1], 1], "expected": 1},
            {"args": [[7, 10, 4, 3, 20, 15], 3], "expected": 10},
            {"args": [[-1, -1], 2], "expected": -1}
        ],
        "import random\n\ndef find_kth_largest(nums: list[int], k: int) -> int:\n    target_idx = len(nums) - k\n    def select(left, right):\n        pivot_idx = random.randint(left, right)\n        pivot = nums[pivot_idx]\n        nums[pivot_idx], nums[right] = nums[right], nums[pivot_idx]\n        p = left\n        for i in range(left, right):\n            if nums[i] <= pivot:\n                nums[p], nums[i] = nums[i], nums[p]\n                p += 1\n        nums[p], nums[right] = nums[right], nums[p]\n        if p == target_idx:\n            return nums[p]\n        elif p < target_idx:\n            return select(p + 1, right)\n        else:\n            return select(left, p - 1)\n    return select(0, len(nums) - 1)\n"
    ),

    P(
        "relative-sort-array", "Relative Sort Array (Counting Sort)", "searching-sorting", 2, "relative_sort_array",
        "Given two arrays `arr1` and `arr2`, the elements of `arr2` are distinct, and all elements in `arr2` are also in `arr1`.\n\nSort the elements of `arr1` such that the relative ordering of items in `arr1` are the same as in `arr2`. Elements that do not appear in `arr2` should be placed at the end of `arr1` in ascending order.",
        "- `1 <= len(arr1), len(arr2) <= 1000`\n- `0 <= arr1[i], arr2[i] <= 1000`\n- All elements of `arr2` are distinct",
        "O(n + k log k)", "O(n)",
        "def relative_sort_array(arr1: list[int], arr2: list[int]) -> list[int]:\n    pass\n",
        [
            {"args": [[2, 3, 1, 3, 2, 4, 6, 7, 9, 2, 19], [2, 1, 4, 3, 9, 6]], "expected": [2, 2, 2, 1, 4, 3, 3, 9, 6, 7, 19]},
            {"args": [[28, 6, 22, 8, 44, 17], [22, 28, 8, 6]], "expected": [22, 28, 8, 6, 17, 44]},
            {"args": [[1, 2, 3], [3, 2, 1]], "expected": [3, 2, 1]},
            {"args": [[5, 4, 3, 2, 1], [1, 5]], "expected": [1, 5, 2, 3, 4]}
        ],
        "from collections import Counter\n\ndef relative_sort_array(arr1: list[int], arr2: list[int]) -> list[int]:\n    counts = Counter(arr1)\n    res = []\n    for x in arr2:\n        if x in counts:\n            res.extend([x] * counts[x])\n            del counts[x]\n    remaining = sorted(counts.elements())\n    res.extend(remaining)\n    return res\n"
    ),

    P(
        "capacity-to-ship-packages", "Capacity to Ship Packages Within D Days", "searching-sorting", 4, "ship_within_days",
        "A conveyor belt has packages that must be shipped within `days` days. The `i`th package has weight `weights[i]`.\n\nReturn the least weight capacity of the ship that will result in all the packages on the conveyor belt being shipped within `days` days in order.",
        "- `1 <= days <= len(weights) <= 5 * 10^4`\n- `1 <= weights[i] <= 500`",
        "O(n * log(sum(weights)))", "O(1)",
        "def ship_within_days(weights: list[int], days: int) -> int:\n    pass\n",
        [
            {"args": [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5], "expected": 15},
            {"args": [[3, 2, 2, 4, 1, 4], 3], "expected": 6},
            {"args": [[1, 2, 3, 1, 1], 4], "expected": 3},
            {"args": [[10], 1], "expected": 10},
            {"args": [[1, 1, 1, 1], 2], "expected": 2}
        ],
        "def ship_within_days(weights: list[int], days: int) -> int:\n    def feasible(capacity):\n        d = 1\n        current_load = 0\n        for w in weights:\n            if current_load + w > capacity:\n                d += 1\n                current_load = w\n                if d > days:\n                    return False\n            else:\n                current_load += w\n        return True\n    left = max(weights)\n    right = sum(weights)\n    ans = right\n    while left <= right:\n        mid = (left + right) // 2\n        if feasible(mid):\n            ans = mid\n            right = mid - 1\n        else:\n            left = mid + 1\n    return ans\n"
    ),

    P(
        "insertion-sort-list-array", "Insertion Sort Simulation", "searching-sorting", 2, "insertion_sort",
        "Given an integer array `nums`, sort the array using the Insertion Sort algorithm and return the sorted array. Return `nums` after in-place sorting.",
        "- `0 <= len(nums) <= 500`\n- `-1000 <= nums[i] <= 1000`",
        "O(n^2)", "O(1)",
        "def insertion_sort(nums: list[int]) -> list[int]:\n    pass\n",
        [
            {"args": [[12, 11, 13, 5, 6]], "expected": [5, 6, 11, 12, 13]},
            {"args": [[1]], "expected": [1]},
            {"args": [[]], "expected": []},
            {"args": [[3, 1, 2]], "expected": [1, 2, 3]},
            {"args": [[5, 4, 3, 2, 1]], "expected": [1, 2, 3, 4, 5]}
        ],
        "def insertion_sort(nums: list[int]) -> list[int]:\n    for i in range(1, len(nums)):\n        key = nums[i]\n        j = i - 1\n        while j >= 0 and nums[j] > key:\n            nums[j + 1] = nums[j]\n            j -= 1\n        nums[j + 1] = key\n    return nums\n"
    ),

    # --- Section 6: Hashing & Hash Tables (Days 66-75) ---
    P(
        "group-anagrams", "Group Anagrams", "hashing", 3, "group_anagrams",
        "Given an array of strings `strs`, group the anagrams together. Return the grouped anagrams where each inner group is sorted lexicographically, and the outer list is sorted by the first word of each group.",
        "- `0 <= len(strs) <= 10^4`\n- `0 <= len(strs[i]) <= 100`\n- `strs[i]` consists of lowercase English letters",
        "O(n * k log k)", "O(n * k)",
        "def group_anagrams(strs: list[str]) -> list[list[str]]:\n    pass\n",
        [
            {"args": [["eat", "tea", "tan", "ate", "nat", "bat"]], "expected": [["ate", "eat", "tea"], ["bat"], ["nat", "tan"]]},
            {"args": [[""]], "expected": [[""]]},
            {"args": [["a"]], "expected": [["a"]]},
            {"args": [[]], "expected": []},
            {"args": [["abc", "bca", "cab", "xyz", "zyx"]], "expected": [["abc", "bca", "cab"], ["xyz", "zyx"]]}
        ],
        "from collections import defaultdict\n\ndef group_anagrams(strs: list[str]) -> list[list[str]]:\n    groups = defaultdict(list)\n    for s in strs:\n        key = tuple(sorted(s))\n        groups[key].append(s)\n    res = [sorted(group) for group in groups.values()]\n    res.sort(key=lambda g: g[0] if g else '')\n    return res\n"
    ),

    P(
        "longest-consecutive-sequence", "Longest Consecutive Sequence (Hash Set)", "hashing", 3, "longest_consecutive",
        "Given an unsorted array of integers `nums`, return the length of the longest consecutive elements sequence.\n\nYou must write an algorithm that runs in $O(n)$ time using a hash set.",
        "- `0 <= len(nums) <= 10^5`\n- `-10^9 <= nums[i] <= 10^9`",
        "O(n)", "O(n)",
        "def longest_consecutive(nums: list[int]) -> int:\n    pass\n",
        [
            {"args": [[100, 4, 200, 1, 3, 2]], "expected": 4},  # [1, 2, 3, 4] -> 4
            {"args": [[0, 3, 7, 2, 5, 8, 4, 6, 0, 1]], "expected": 9},
            {"args": [[]], "expected": 0},
            {"args": [[1]], "expected": 1},
            {"args": [[10, 20, 30]], "expected": 1}
        ],
        "def longest_consecutive(nums: list[int]) -> int:\n    num_set = set(nums)\n    longest = 0\n    for num in num_set:\n        if num - 1 not in num_set:\n            curr = num\n            streak = 1\n            while curr + 1 in num_set:\n                curr += 1\n                streak += 1\n            longest = max(longest, streak)\n    return longest\n"
    ),

    P(
        "repeated-dna-sequences", "Repeated DNA Sequences (Rolling Hash)", "hashing", 3, "find_repeated_dna_sequences",
        "The DNA sequence is composed of a series of nucleotides abbreviated as `'A'`, `'C'`, `'G'`, and `'T'`.\n\nGiven a string `s` that represents a DNA sequence, return all the 10-letter-long sequences (substrings) that occur more than once in a DNA molecule. Return the list sorted lexicographically.",
        "- `1 <= len(s) <= 10^5`\n- `s[i]` is either `'A'`, `'C'`, `'G'`, or `'T'`",
        "O(n)", "O(n)",
        "def find_repeated_dna_sequences(s: str) -> list[str]:\n    pass\n",
        [
            {"args": ["AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT"], "expected": ["AAAAACCCCC", "CCCCCAAAAA"]},
            {"args": ["AAAAAAAAAAAAA"], "expected": ["AAAAAAAAAA"]},
            {"args": ["ACGTACGTAC"], "expected": []},
            {"args": ["A"], "expected": []}
        ],
        "def find_repeated_dna_sequences(s: str) -> list[str]:\n    seen = set()\n    repeated = set()\n    for i in range(len(s) - 9):\n        sub = s[i:i + 10]\n        if sub in seen:\n            repeated.add(sub)\n        else:\n            seen.add(sub)\n    return sorted(list(repeated))\n"
    ),

    P(
        "lru-cache", "LRU Cache Simulation (DLL + Hash Map)", "hashing", 4, "simulate_lru_cache",
        "Simulate an LRU (Least Recently Used) Cache of given `capacity`. Given a sequence of operations `[['put', key, val], ['get', key], ...]`, return the list of output values (returns `-1` on missing `get`, and `None` on `put`).",
        "- `1 <= capacity <= 3000`\n- `0 <= key <= 10^4`\n- `0 <= value <= 10^5`\n- At most `2 * 10^4` calls to `get` and `put`",
        "O(1) per op", "O(capacity)",
        "def simulate_lru_cache(capacity: int, operations: list) -> list:\n    pass\n",
        [
            {"args": [2, [["put", 1, 1], ["put", 2, 2], ["get", 1], ["put", 3, 3], ["get", 2], ["put", 4, 4], ["get", 1], ["get", 3], ["get", 4]]],
             "expected": [None, None, 1, None, -1, None, -1, 3, 4]},
            {"args": [1, [["put", 2, 1], ["get", 2], ["put", 3, 2], ["get", 2], ["get", 3]]],
             "expected": [None, 1, None, -1, 2]},
            {"args": [2, [["get", 2]]],
             "expected": [-1]}
        ],
        "from collections import OrderedDict\n\ndef simulate_lru_cache(capacity: int, operations: list) -> list:\n    cache = OrderedDict()\n    out = []\n    for op in operations:\n        cmd = op[0]\n        if cmd == 'put':\n            key, val = op[1], op[2]\n            if key in cache:\n                cache.move_to_end(key)\n            cache[key] = val\n            if len(cache) > capacity:\n                cache.popitem(last=False)\n            out.append(None)\n        elif cmd == 'get':\n            key = op[1]\n            if key in cache:\n                cache.move_to_end(key)\n                out.append(cache[key])\n            else:\n                out.append(-1)\n    return out\n"
    ),

    P(
        "insert-delete-getrandom-o1", "Insert Delete GetRandom O(1)", "hashing", 3, "simulate_randomized_set",
        "Simulate a set supporting `insert(val)` (returns True if inserted, False if already present) and `remove(val)` (returns True if removed, False if not present). Return the list of boolean outcomes.",
        "- `-2^31 <= val <= 2^31 - 1`\n- At most `2 * 10^4` calls",
        "O(1) average", "O(n)",
        "def simulate_randomized_set(operations: list) -> list[bool]:\n    pass\n",
        [
            {"args": [[["insert", 1], ["remove", 2], ["insert", 2], ["insert", 1], ["remove", 1], ["insert", 2]]],
             "expected": [True, False, True, False, True, False]},
            {"args": [[["remove", 0], ["remove", 0], ["insert", 0], ["remove", 0], ["insert", 0]]],
             "expected": [False, False, True, True, True]}
        ],
        "def simulate_randomized_set(operations: list) -> list[bool]:\n    indices = {}\n    nums = []\n    out = []\n    for cmd, val in operations:\n        if cmd == 'insert':\n            if val in indices:\n                out.append(False)\n            else:\n                indices[val] = len(nums)\n                nums.append(val)\n                out.append(True)\n        elif cmd == 'remove':\n            if val not in indices:\n                out.append(False)\n            else:\n                idx = indices[val]\n                last_val = nums[-1]\n                nums[idx] = last_val\n                indices[last_val] = idx\n                nums.pop()\n                del indices[val]\n                out.append(True)\n    return out\n"
    ),

    P(
        "design-hashmap", "Design HashMap Chaining", "hashing", 2, "simulate_hashmap",
        "Simulate a HashMap without using built-in hash tables. Process operations: `[['put', key, value], ['get', key], ['remove', key]]`. Return the results list (returns `None` for `put`/`remove`, and value or `-1` for `get`).",
        "- `0 <= key, value <= 10^6`\n- At most `10^4` calls to operations",
        "O(1) amortized", "O(n)",
        "def simulate_hashmap(operations: list) -> list:\n    pass\n",
        [
            {"args": [[["put", 1, 1], ["put", 2, 2], ["get", 1], ["get", 3], ["put", 2, 1], ["get", 2], ["remove", 2], ["get", 2]]],
             "expected": [None, None, 1, -1, None, 1, None, -1]},
            {"args": [[["get", 10], ["remove", 10]]],
             "expected": [-1, None]}
        ],
        "def simulate_hashmap(operations: list) -> list:\n    SIZE = 1000\n    buckets = [[] for _ in range(SIZE)]\n    out = []\n    for op in operations:\n        cmd = op[0]\n        key = op[1]\n        h = key % SIZE\n        bucket = buckets[h]\n        if cmd == 'put':\n            val = op[2]\n            found = False\n            for i, (k, v) in enumerate(bucket):\n                if k == key:\n                    bucket[i] = (key, val)\n                    found = True\n                    break\n            if not found:\n                bucket.append((key, val))\n            out.append(None)\n        elif cmd == 'get':\n            found_val = -1\n            for k, v in bucket:\n                if k == key:\n                    found_val = v\n                    break\n            out.append(found_val)\n        elif cmd == 'remove':\n            for i, (k, v) in enumerate(bucket):\n                if k == key:\n                    del bucket[i]\n                    break\n            out.append(None)\n    return out\n"
    )
]
