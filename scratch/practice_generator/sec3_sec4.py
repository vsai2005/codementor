"""
Practice Problems for Section 3 (Computational Thinking & Recursion) and Section 4 (Arrays & Strings)
Total problems: 11
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

SEC3_SEC4_PROBLEMS = [
    # --- Section 3: Computational Thinking & Recursion (Days 26-35) ---
    P(
        "count-loop-operations", "Count Nested Loop Operations", "python-basics", 1, "count_operations",
        "Given integer `n`, compute how many times the innermost statement executes in the following algorithm:\n```python\nfor i in range(1, n + 1):\n    j = 1\n    while j <= i:\n        count += 1\n        j *= 2\n```\nReturn the total count without timing out on large $N$.",
        "- `1 <= n <= 10^5`",
        "O(n)", "O(1)",
        "def count_operations(n: int) -> int:\n    pass\n",
        [
            {"args": [1], "expected": 1},
            {"args": [2], "expected": 3},  # i=1: 1, i=2: 2 -> 3
            {"args": [4], "expected": 8},  # i=1:1, i=2:2, i=3:2, i=4:3 -> 8
            {"args": [10], "expected": 29},
            {"args": [100], "expected": 580}
        ],
        "def count_operations(n: int) -> int:\n    total = 0\n    for i in range(1, n + 1):\n        total += i.bit_length()\n    return total\n"
    ),

    P(
        "power-of-three", "Power of Three (Recursion)", "python-basics", 1, "is_power_of_three",
        "Given an integer `n`, return `True` if it is a power of three. Otherwise, return `False`.\n\nAn integer `n` is a power of three if there exists an integer `x` such that `n == 3^x`.",
        "- `-2^31 <= n <= 2^31 - 1`",
        "O(log3(n))", "O(log3(n))",
        "def is_power_of_three(n: int) -> bool:\n    pass\n",
        [
            {"args": [27], "expected": True},
            {"args": [0], "expected": False},
            {"args": [-1], "expected": False},
            {"args": [1], "expected": True},
            {"args": [9], "expected": True},
            {"args": [45], "expected": False}
        ],
        "def is_power_of_three(n: int) -> bool:\n    if n <= 0:\n        return False\n    if n == 1:\n        return True\n    if n % 3 != 0:\n        return False\n    return is_power_of_three(n // 3)\n"
    ),

    P(
        "subsets-recursive", "Subsets (Power Set Tree)", "python-basics", 2, "generate_subsets",
        "Given an integer array `nums` of unique elements, return all possible subsets (the power set).\n\nThe solution set must not contain duplicate subsets. Subsets should be sorted by length, then lexicographically.",
        "- `1 <= len(nums) <= 10`\n- `-10 <= nums[i] <= 10`\n- All elements of `nums` are unique",
        "O(n * 2^n)", "O(n * 2^n)",
        "def generate_subsets(nums: list[int]) -> list[list[int]]:\n    pass\n",
        [
            {"args": [[1, 2, 3]], "expected": [[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]]},
            {"args": [[0]], "expected": [[], [0]]},
            {"args": [[1, 2]], "expected": [[], [1], [2], [1, 2]]},
            {"args": [[5]], "expected": [[], [5]]},
            {"args": [[-1, 1]], "expected": [[], [-1], [1], [-1, 1]]}
        ],
        "def generate_subsets(nums: list[int]) -> list[list[int]]:\n    nums.sort()\n    res = []\n    def backtrack(idx, current):\n        if idx == len(nums):\n            res.append(list(current))\n            return\n        backtrack(idx + 1, current)\n        current.append(nums[idx])\n        backtrack(idx + 1, current)\n        current.pop()\n    backtrack(0, [])\n    res.sort(key=lambda x: (len(x), x))\n    return res\n"
    ),

    P(
        "powx-n", "Pow(x, n) Logarithmic Divide & Conquer", "python-basics", 3, "my_pow",
        "Implement `pow(x, n)`, which calculates `x` raised to the power `n` ($x^n$) in $O(\\log |n|)$ time.\n\nRound the result to 4 decimal places.",
        "- `-100.0 < x < 100.0`\n- `-2^31 <= n <= 2^31 - 1`",
        "O(log n)", "O(log n)",
        "def my_pow(x: float, n: int) -> float:\n    pass\n",
        [
            {"args": [2.0, 10], "expected": 1024.0},
            {"args": [2.1, 3], "expected": 9.261},
            {"args": [2.0, -2], "expected": 0.25},
            {"args": [1.0, 2147483647], "expected": 1.0},
            {"args": [-2.0, 2], "expected": 4.0},
            {"args": [-2.0, 3], "expected": -8.0}
        ],
        "def my_pow(x: float, n: int) -> float:\n    def fast_pow(base, exp):\n        if exp == 0:\n            return 1.0\n        half = fast_pow(base, exp // 2)\n        if exp % 2 == 0:\n            return half * half\n        else:\n            return half * half * base\n    if n < 0:\n        x = 1.0 / x\n        n = -n\n    return round(fast_pow(x, n), 4)\n"
    ),

    P(
        "generate-parentheses", "Generate Balanced Parentheses", "python-basics", 3, "generate_parentheses",
        "Given `n` pairs of parentheses, write a function to generate all combinations of well-formed parentheses.\n\nReturn the list in lexicographical order.",
        "- `1 <= n <= 8`",
        "O(4^n / sqrt(n))", "O(n)",
        "def generate_parentheses(n: int) -> list[str]:\n    pass\n",
        [
            {"args": [1], "expected": ["()"]},
            {"args": [2], "expected": ["(())", "()()"]},
            {"args": [3], "expected": ["((()))", "(()())", "(())()", "()(())", "()()()"]},
            {"args": [4], "expected": ["(((())))", "((()()))", "((())())", "((()))()", "(()(()))", "(()()())", "(()())()", "(())(())", "(())()()", "()((()))", "()(()())", "()(())()", "()()(())", "()()()()"]}
        ],
        "def generate_parentheses(n: int) -> list[str]:\n    res = []\n    def dfs(open_c, close_c, path):\n        if len(path) == 2 * n:\n            res.append(path)\n            return\n        if open_c < n:\n            dfs(open_c + 1, close_c, path + '(')\n        if close_c < open_c:\n            dfs(open_c, close_c + 1, path + ')')\n    dfs(0, 0, '')\n    res.sort()\n    return res\n"
    ),

    P(
        "recursive-sum-digits", "Recursive Digit Sum", "python-basics", 1, "sum_digits",
        "Given a non-negative integer `n`, return the sum of its digits calculated recursively until a single-digit root is produced.",
        "- `0 <= n <= 10^9`",
        "O(log n)", "O(log n)",
        "def sum_digits(n: int) -> int:\n    pass\n",
        [
            {"args": [38], "expected": 2},  # 3+8=11 -> 1+1=2
            {"args": [0], "expected": 0},
            {"args": [9], "expected": 9},
            {"args": [9999], "expected": 9},
            {"args": [12345], "expected": 6}
        ],
        "def sum_digits(n: int) -> int:\n    if n < 10:\n        return n\n    s = sum(int(d) for d in str(n))\n    return sum_digits(s)\n"
    ),

    # --- Section 4: Arrays & Strings (Days 36-50) ---
    P(
        "range-sum-query-immutable", "Range Sum Query (1D Prefix Sums)", "arrays", 2, "compute_range_sums",
        "Given an integer array `nums` and a list of query ranges `queries = [[l_1, r_1], [l_2, r_2], ...]`, return a list of the sum of elements from index `l` to `r` inclusive for each query.\n\nPrecompute a 1D prefix sum array to answer each query in $O(1)$ time.",
        "- `1 <= len(nums) <= 10^4`\n- `1 <= len(queries) <= 10^4`\n- `0 <= l <= r < len(nums)`",
        "O(n + q)", "O(n)",
        "def compute_range_sums(nums: list[int], queries: list[list[int]]) -> list[int]:\n    pass\n",
        [
            {"args": [[-2, 0, 3, -5, 2, -1], [[0, 2], [2, 5], [0, 5]]], "expected": [1, -1, -3]},
            {"args": [[1, 2, 3, 4, 5], [[0, 4], [1, 3], [2, 2]]], "expected": [15, 9, 3]},
            {"args": [[10], [[0, 0]]], "expected": [10]},
            {"args": [[0, 0, 0], [[0, 1], [1, 2]]], "expected": [0, 0]}
        ],
        "def compute_range_sums(nums: list[int], queries: list[list[int]]) -> list[int]:\n    prefix = [0] * (len(nums) + 1)\n    for i in range(len(nums)):\n        prefix[i + 1] = prefix[i] + nums[i]\n    return [prefix[r + 1] - prefix[l] for l, r in queries]\n"
    ),

    P(
        "maximum-average-subarray-i", "Maximum Average Subarray (Fixed Window)", "arrays", 2, "find_max_average",
        "You are given an integer array `nums` consisting of `n` elements, and an integer `k`.\n\nFind a contiguous subarray whose length is equal to `k` that has the maximum average value and return this value rounded to 2 decimal places.",
        "- `1 <= k <= len(nums) <= 10^5`\n- `-10^4 <= nums[i] <= 10^4`",
        "O(n)", "O(1)",
        "def find_max_average(nums: list[int], k: int) -> float:\n    pass\n",
        [
            {"args": [[1, 12, -5, -6, 50, 3], 4], "expected": 12.75},
            {"args": [[5], 1], "expected": 5.0},
            {"args": [[0, 4, 0, 3, 2], 1], "expected": 4.0},
            {"args": [[-1, -2, -3, -4], 2], "expected": -1.5},
            {"args": [[4, 2, 1, 3, 3], 2], "expected": 3.0}
        ],
        "def find_max_average(nums: list[int], k: int) -> float:\n    curr_sum = sum(nums[:k])\n    max_sum = curr_sum\n    for i in range(k, len(nums)):\n        curr_sum += nums[i] - nums[i - k]\n        if curr_sum > max_sum:\n            max_sum = curr_sum\n    return round(max_sum / k, 2)\n"
    ),

    P(
        "range-sum-query-2d-immutable", "2D Matrix Range Sum (Inclusion-Exclusion)", "arrays", 3, "matrix_range_sum",
        "Given a 2D integer matrix `matrix` and a list of rectangular query regions `queries = [[r1, c1, r2, c2], ...]`, calculate the sum of the elements inside the rectangle defined by top-left `(r1, c1)` and bottom-right `(r2, c2)` inclusive.\n\nPrecompute a 2D prefix sum array.",
        "- `1 <= m, n <= 200`\n- `1 <= len(queries) <= 10^4`\n- `0 <= r1 <= r2 < m`, `0 <= c1 <= c2 < n`",
        "O(m * n + q)", "O(m * n)",
        "def matrix_range_sum(matrix: list[list[int]], queries: list[list[int]]) -> list[int]:\n    pass\n",
        [
            {"args": [
                [[3, 0, 1, 4, 2],
                 [5, 6, 3, 2, 1],
                 [1, 2, 0, 1, 5],
                 [4, 1, 0, 1, 7],
                 [1, 0, 3, 0, 5]],
                [[2, 1, 4, 3], [1, 1, 2, 2], [1, 2, 2, 4]]
            ], "expected": [8, 11, 12]},
            {"args": [[[1, 2], [3, 4]], [[0, 0, 1, 1], [0, 1, 1, 1]]], "expected": [10, 6]},
            {"args": [[[5]], [[0, 0, 0, 0]]], "expected": [5]}
        ],
        "def matrix_range_sum(matrix: list[list[int]], queries: list[list[int]]) -> list[int]:\n    if not matrix or not matrix[0]:\n        return []\n    m, n = len(matrix), len(matrix[0])\n    dp = [[0] * (n + 1) for _ in range(m + 1)]\n    for r in range(m):\n        for c in range(n):\n            dp[r + 1][c + 1] = matrix[r][c] + dp[r][c + 1] + dp[r + 1][c] - dp[r][c]\n    res = []\n    for r1, c1, r2, c2 in queries:\n        total = dp[r2 + 1][c2 + 1] - dp[r1][c2 + 1] - dp[r2 + 1][c1] + dp[r1][c1]\n        res.append(total)\n    return res\n"
    ),

    P(
        "merge-intervals", "Merge Overlapping Intervals", "arrays", 3, "merge_intervals",
        "Given an array of `intervals` where `intervals[i] = [start_i, end_i]`, merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all the intervals in the input.\n\nReturn the intervals sorted by start time.",
        "- `1 <= len(intervals) <= 10^4`\n- `intervals[i].length == 2`\n- `0 <= start_i <= end_i <= 10^4`",
        "O(n log n)", "O(n)",
        "def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:\n    pass\n",
        [
            {"args": [[[1, 3], [2, 6], [8, 10], [15, 18]]], "expected": [[1, 6], [8, 10], [15, 18]]},
            {"args": [[[1, 4], [4, 5]]], "expected": [[1, 5]]},
            {"args": [[[1, 4], [0, 4]]], "expected": [[0, 4]]},
            {"args": [[[1, 4], [2, 3]]], "expected": [[1, 4]]},
            {"args": [[[6, 8]]], "expected": [[6, 8]]}
        ],
        "def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:\n    if not intervals:\n        return []\n    intervals.sort(key=lambda x: x[0])\n    merged = [intervals[0]]\n    for current in intervals[1:]:\n        prev = merged[-1]\n        if current[0] <= prev[1]:\n            prev[1] = max(prev[1], current[1])\n        else:\n            merged.append(current)\n    return merged\n"
    ),

    P(
        "minimum-size-subarray-sum", "Minimum Size Subarray Sum (Dynamic Window)", "arrays", 3, "min_sub_array_len",
        "Given an array of positive integers `nums` and a positive integer `target`, return the minimal length of a contiguous subarray `[nums[l], ..., nums[r]]` of which the sum is greater than or equal to `target`. If there is no such subarray, return `0` instead.",
        "- `1 <= target <= 10^9`\n- `1 <= len(nums) <= 10^5`\n- `1 <= nums[i] <= 10^4`",
        "O(n)", "O(1)",
        "def min_sub_array_len(target: int, nums: list[int]) -> int:\n    pass\n",
        [
            {"args": [7, [2, 3, 1, 2, 4, 3]], "expected": 2},  # [4, 3] sum=7 len=2
            {"args": [4, [1, 4, 4]], "expected": 1},
            {"args": [11, [1, 1, 1, 1, 1, 1, 1, 1]], "expected": 0},
            {"args": [15, [1, 2, 3, 4, 5]], "expected": 5},
            {"args": [6, [10, 2, 3]], "expected": 1}
        ],
        "def min_sub_array_len(target: int, nums: list[int]) -> int:\n    left = 0\n    current_sum = 0\n    min_len = float('inf')\n    for right in range(len(nums)):\n        current_sum += nums[right]\n        while current_sum >= target:\n            min_len = min(min_len, right - left + 1)\n            current_sum -= nums[left]\n            left += 1\n    return 0 if min_len == float('inf') else min_len\n"
    )
]
