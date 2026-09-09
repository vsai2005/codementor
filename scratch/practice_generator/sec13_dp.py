"""
Practice Problems for Section 13 (Dynamic Programming)
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

SEC13_DP_PROBLEMS = [
    P(
        "climbing-stairs", "Climbing Stairs (1D DP State Compression)", "dynamic-programming", 1, "climb_stairs",
        "You are climbing a staircase. It takes `n` steps to reach the top. Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?\n\nSolve with $O(1)$ auxiliary space.",
        "- `1 <= n <= 45`",
        "O(n)", "O(1)",
        "def climb_stairs(n: int) -> int:\n    pass\n",
        [
            {"args": [2], "expected": 2},
            {"args": [3], "expected": 3},
            {"args": [1], "expected": 1},
            {"args": [5], "expected": 8},
            {"args": [10], "expected": 89}
        ],
        "def climb_stairs(n: int) -> int:\n    if n <= 2:\n        return n\n    a, b = 1, 2\n    for _ in range(3, n + 1):\n        a, b = b, a + b\n    return b\n"
    ),

    P(
        "house-robber", "House Robber (Non-Adjacent Recurrence)", "dynamic-programming", 2, "rob",
        "You are planning to rob houses along a street. Each house has a certain amount of money stashed, but adjacent houses have connected security systems that will contact police if two adjacent houses are broken into on the same night.\n\nReturn the maximum amount of money you can rob tonight without alerting the police.",
        "- `1 <= len(nums) <= 100`\n- `0 <= nums[i] <= 400`",
        "O(n)", "O(1)",
        "def rob(nums: list[int]) -> int:\n    pass\n",
        [
            {"args": [[1, 2, 3, 1]], "expected": 4},
            {"args": [[2, 7, 9, 3, 1]], "expected": 12},
            {"args": [[0]], "expected": 0},
            {"args": [[2, 1, 1, 2]], "expected": 4}
        ],
        "def rob(nums: list[int]) -> int:\n    prev2 = prev1 = 0\n    for num in nums:\n        prev2, prev1 = prev1, max(prev1, prev2 + num)\n    return prev1\n"
    ),

    P(
        "house-robber-ii", "House Robber II (Circular Street)", "dynamic-programming", 3, "rob_circular",
        "All houses at this place are arranged in a circle. That means the first house is the neighbor of the last one. Adjacent houses cannot be broken into on the same night.\n\nReturn the maximum amount of money you can rob without alerting the police.",
        "- `1 <= len(nums) <= 100`\n- `0 <= nums[i] <= 1000`",
        "O(n)", "O(1)",
        "def rob_circular(nums: list[int]) -> int:\n    pass\n",
        [
            {"args": [[2, 3, 2]], "expected": 3},
            {"args": [[1, 2, 3, 1]], "expected": 4},
            {"args": [[1, 2, 3]], "expected": 3},
            {"args": [[5]], "expected": 5}
        ],
        "def rob_circular(nums: list[int]) -> int:\n    if len(nums) == 1:\n        return nums[0]\n    def linear_rob(sub):\n        prev2 = prev1 = 0\n        for num in sub:\n            prev2, prev1 = prev1, max(prev1, prev2 + num)\n        return prev1\n    return max(linear_rob(nums[:-1]), linear_rob(nums[1:]))\n"
    ),

    P(
        "unique-paths", "Unique Paths (2D Grid Combinatorics)", "dynamic-programming", 2, "unique_paths",
        "There is a robot on an `m x n` grid. The robot is initially located at top-left corner `(0, 0)`. The robot tries to move to bottom-right corner `(m - 1, n - 1)`. The robot can only move either down or right at any point.\n\nReturn the number of possible unique paths.",
        "- `1 <= m, n <= 100`\n- The answer will be less than or equal to $2 \\times 10^9$",
        "O(m * n)", "O(n)",
        "def unique_paths(m: int, n: int) -> int:\n    pass\n",
        [
            {"args": [3, 7], "expected": 28},
            {"args": [3, 2], "expected": 3},
            {"args": [1, 1], "expected": 1},
            {"args": [3, 3], "expected": 6}
        ],
        "def unique_paths(m: int, n: int) -> int:\n    row = [1] * n\n    for _ in range(m - 1):\n        for j in range(1, n):\n            row[j] += row[j - 1]\n    return row[-1]\n"
    ),

    P(
        "minimum-path-sum", "Minimum Path Sum (2D Grid DP)", "dynamic-programming", 3, "min_path_sum",
        "Given a `m x n` `grid` filled with non-negative numbers, find a path from top left to bottom right, which minimizes the sum of all numbers along its path. You can only move either down or right at any point.",
        "- `m == len(grid)`\n- `n == len(grid[0])`\n- `1 <= m, n <= 200`\n- `0 <= grid[i][j] <= 200`",
        "O(m * n)", "O(n)",
        "def min_path_sum(grid: list[list[int]]) -> int:\n    pass\n",
        [
            {"args": [[[1, 3, 1], [1, 5, 1], [4, 2, 1]]], "expected": 7},
            {"args": [[[1, 2, 3], [4, 5, 6]]], "expected": 12},
            {"args": [[[5]]], "expected": 5}
        ],
        "def min_path_sum(grid: list[list[int]]) -> int:\n    m, n = len(grid), len(grid[0])\n    dp = [float('inf')] * (n + 1)\n    dp[1] = 0\n    for r in range(m):\n        new_dp = [float('inf')] * (n + 1)\n        for c in range(n):\n            new_dp[c + 1] = grid[r][c] + min(dp[c + 1], new_dp[c])\n        dp = new_dp\n    return dp[n]\n"
    ),

    P(
        "partition-equal-subset-sum", "Partition Equal Subset Sum (0/1 Knapsack)", "dynamic-programming", 3, "can_partition",
        "Given an integer array `nums`, return `True` if you can partition the array into two subsets such that the sum of the elements in both subsets is equal or `False` otherwise.\n\nUse 0/1 knapsack 1D reverse capacity loop.",
        "- `1 <= len(nums) <= 200`\n- `1 <= nums[i] <= 100`",
        "O(n * target)", "O(target)",
        "def can_partition(nums: list[int]) -> bool:\n    pass\n",
        [
            {"args": [[1, 5, 11, 5]], "expected": True},
            {"args": [[1, 2, 3, 5]], "expected": False},
            {"args": [[2, 2]], "expected": True},
            {"args": [[1]], "expected": False}
        ],
        "def can_partition(nums: list[int]) -> bool:\n    total = sum(nums)\n    if total % 2 != 0:\n        return False\n    target = total // 2\n    dp = [True] + [False] * target\n    for num in nums:\n        for j in range(target, num - 1, -1):\n            dp[j] = dp[j] or dp[j - num]\n    return dp[target]\n"
    ),

    P(
        "coin-change", "Coin Change (Fewest Coins)", "dynamic-programming", 3, "coin_change",
        "You are given an integer array `coins` representing coins of different denominations and an integer `amount` representing a total amount of money.\n\nReturn the fewest number of coins that you need to make up that amount. If that amount cannot be made up, return `-1`.\n\nYou may assume an infinite number of each kind of coin.",
        "- `1 <= len(coins) <= 12`\n- `1 <= coins[i] <= 2^31 - 1`\n- `0 <= amount <= 10^4`",
        "O(len(coins) * amount)", "O(amount)",
        "def coin_change(coins: list[int], amount: int) -> int:\n    pass\n",
        [
            {"args": [[1, 2, 5], 11], "expected": 3},
            {"args": [[2], 3], "expected": -1},
            {"args": [[1], 0], "expected": 0},
            {"args": [[1], 1], "expected": 1},
            {"args": [[2, 5, 10, 1], 27], "expected": 4}
        ],
        "def coin_change(coins: list[int], amount: int) -> int:\n    dp = [0] + [float('inf')] * amount\n    for c in coins:\n        for x in range(c, amount + 1):\n            dp[x] = min(dp[x], dp[x - c] + 1)\n    return dp[amount] if dp[amount] != float('inf') else -1\n"
    ),

    P(
        "coin-change-ii", "Coin Change II (Total Combinations)", "dynamic-programming", 3, "coin_change_combinations",
        "You are given an integer array `coins` representing coins of different denominations and an integer `amount` representing a total amount of money.\n\nReturn the number of combinations that make up that amount. If that amount of money cannot be made up by any combination of the coins, return 0.",
        "- `1 <= len(coins) <= 300`\n- `1 <= coins[i] <= 5000`\n- `0 <= amount <= 5000`",
        "O(len(coins) * amount)", "O(amount)",
        "def coin_change_combinations(amount: int, coins: list[int]) -> int:\n    pass\n",
        [
            {"args": [5, [1, 2, 5]], "expected": 4},
            {"args": [3, [2]], "expected": 0},
            {"args": [10, [10]], "expected": 1},
            {"args": [0, [7]], "expected": 1}
        ],
        "def coin_change_combinations(amount: int, coins: list[int]) -> int:\n    dp = [1] + [0] * amount\n    for c in coins:\n        for x in range(c, amount + 1):\n            dp[x] += dp[x - c]\n    return dp[amount]\n"
    ),

    P(
        "longest-increasing-subsequence", "Longest Increasing Subsequence (Patience Sorting)", "dynamic-programming", 3, "length_of_lis",
        "Given an integer array `nums`, return the length of the longest strictly increasing subsequence.\n\nYou must solve this in $O(n \\log n)$ time using patience sorting and binary search (`bisect_left`).",
        "- `1 <= len(nums) <= 2500`\n- `-10^4 <= nums[i] <= 10^4`",
        "O(n log n)", "O(n)",
        "def length_of_lis(nums: list[int]) -> int:\n    pass\n",
        [
            {"args": [[10, 9, 2, 5, 3, 7, 101, 18]], "expected": 4},
            {"args": [[0, 1, 0, 3, 2, 3]], "expected": 4},
            {"args": [[7, 7, 7, 7, 7, 7, 7]], "expected": 1},
            {"args": [[1, 3, 6, 7, 9, 4, 10, 5, 6]], "expected": 6}
        ],
        "import bisect\n\ndef length_of_lis(nums: list[int]) -> int:\n    tails = []\n    for x in nums:\n        idx = bisect.bisect_left(tails, x)\n        if idx == len(tails):\n            tails.append(x)\n        else:\n            tails[idx] = x\n    return len(tails)\n"
    ),

    P(
        "longest-common-subsequence", "Longest Common Subsequence", "dynamic-programming", 3, "longest_common_subsequence",
        "Given two strings `text1` and `text2`, return the length of their longest common subsequence. If there is no common subsequence, return `0`.",
        "- `1 <= len(text1), len(text2) <= 1000`\n- `text1` and `text2` consist of only lowercase English characters",
        "O(m * n)", "O(min(m, n))",
        "def longest_common_subsequence(text1: str, text2: str) -> int:\n    pass\n",
        [
            {"args": ["abcde", "ace"], "expected": 3},
            {"args": ["abc", "abc"], "expected": 3},
            {"args": ["abc", "def"], "expected": 0},
            {"args": ["bl", "yby"], "expected": 1}
        ],
        "def longest_common_subsequence(text1: str, text2: str) -> int:\n    if len(text1) < len(text2):\n        text1, text2 = text2, text1\n    dp = [0] * (len(text2) + 1)\n    for c1 in text1:\n        prev = 0\n        for j, c2 in enumerate(text2):\n            temp = dp[j + 1]\n            if c1 == c2:\n                dp[j + 1] = prev + 1\n            else:\n                dp[j + 1] = max(dp[j + 1], dp[j])\n            prev = temp\n    return dp[-1]\n"
    ),

    P(
        "edit-distance", "Edit Distance (Levenshtein Distance)", "dynamic-programming", 4, "min_distance",
        "Given two strings `word1` and `word2`, return the minimum number of operations required to convert `word1` to `word2`.\n\nYou have the following three operations permitted on a word: insert a character, delete a character, or replace a character.",
        "- `0 <= len(word1), len(word2) <= 500`\n- `word1` and `word2` consist of lowercase English letters",
        "O(m * n)", "O(n)",
        "def min_distance(word1: str, word2: str) -> int:\n    pass\n",
        [
            {"args": ["horse", "ros"], "expected": 3},
            {"args": ["intention", "execution"], "expected": 5},
            {"args": ["", ""], "expected": 0},
            {"args": ["a", "b"], "expected": 1},
            {"args": ["", "abc"], "expected": 3}
        ],
        "def min_distance(word1: str, word2: str) -> int:\n    m, n = len(word1), len(word2)\n    dp = list(range(n + 1))\n    for i in range(1, m + 1):\n        new_dp = [i] + [0] * n\n        for j in range(1, n + 1):\n            if word1[i - 1] == word2[j - 1]:\n                new_dp[j] = dp[j - 1]\n            else:\n                new_dp[j] = 1 + min(dp[j], new_dp[j - 1], dp[j - 1])\n        dp = new_dp\n    return dp[n]\n"
    )
]
