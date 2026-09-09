"""
Practice Problems for Section 14 (Advanced DSA, Bit Manipulation & Capstones)
Total problems: 7
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

SEC14_ADV_PROBLEMS = [
    P(
        "counting-bits", "Counting Bits (Bitwise DP)", "bit-manipulation", 1, "count_bits",
        "Given an integer `n`, return an array `ans` of length `n + 1` such that for each `i` (`0 <= i <= n`), `ans[i]` is the number of `1`'s in the binary representation of `i`.\n\nSolve it in $O(n)$ time using DP recurrence: `ans[i] = ans[i >> 1] + (i & 1)`.",
        "- `0 <= n <= 10^5`",
        "O(n)", "O(1)",
        "def count_bits(n: int) -> list[int]:\n    pass\n",
        [
            {"args": [2], "expected": [0, 1, 1]},
            {"args": [5], "expected": [0, 1, 1, 2, 1, 2]},
            {"args": [0], "expected": [0]},
            {"args": [8], "expected": [0, 1, 1, 2, 1, 2, 2, 3, 1]}
        ],
        "def count_bits(n: int) -> list[int]:\n    dp = [0] * (n + 1)\n    for i in range(1, n + 1):\n        dp[i] = dp[i >> 1] + (i & 1)\n    return dp\n"
    ),

    P(
        "number-of-1-bits", "Number of 1 Bits (Brian Kernighan's)", "bit-manipulation", 1, "hamming_weight",
        "Given a positive integer `n`, write a function that returns the number of set bits (1s) it has in its binary representation (also known as Hamming weight).\n\nUse Brian Kernighan's algorithm `n = n & (n - 1)` which jumps in $O(k)$ steps where $k$ is the number of set bits.",
        "- `1 <= n <= 2^31 - 1`",
        "O(k)", "O(1)",
        "def hamming_weight(n: int) -> int:\n    pass\n",
        [
            {"args": [11], "expected": 3},  # 1011 -> 3
            {"args": [128], "expected": 1},  # 10000000 -> 1
            {"args": [2147483645], "expected": 30},
            {"args": [1], "expected": 1},
            {"args": [7], "expected": 3}
        ],
        "def hamming_weight(n: int) -> int:\n    count = 0\n    while n:\n        n &= n - 1\n        count += 1\n    return count\n"
    ),

    P(
        "subsets", "Subsets via Bitmask Enumeration", "bit-manipulation", 2, "subsets_bitmask",
        "Given an integer array `nums` of unique elements, return all possible subsets using bitmask enumeration (`1 << n`).\n\nSort the returned subsets by length, then lexicographically.",
        "- `1 <= len(nums) <= 10`\n- All elements of `nums` are unique",
        "O(n * 2^n)", "O(n * 2^n)",
        "def subsets_bitmask(nums: list[int]) -> list[list[int]]:\n    pass\n",
        [
            {"args": [[1, 2, 3]], "expected": [[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]]},
            {"args": [[0]], "expected": [[], [0]]},
            {"args": [[1, 2]], "expected": [[], [1], [2], [1, 2]]}
        ],
        "def subsets_bitmask(nums: list[int]) -> list[list[int]]:\n    nums.sort()\n    n = len(nums)\n    res = []\n    for mask in range(1 << n):\n        subset = [nums[i] for i in range(n) if (mask >> i) & 1]\n        res.append(subset)\n    res.sort(key=lambda s: (len(s), s))\n    return res\n"
    ),

    P(
        "n-queens", "N-Queens (Bitmask Backtracking)", "advanced-dsa", 4, "total_n_queens",
        "The n-queens puzzle is the problem of placing `n` queens on an `n x n` chessboard such that no two queens attack each other.\n\nGiven an integer `n`, return the number of distinct solutions to the n-queens puzzle. Use bitmasks for column, main diagonal, and anti-diagonal pruning.",
        "- `1 <= n <= 9`",
        "O(n!)", "O(n)",
        "def total_n_queens(n: int) -> int:\n    pass\n",
        [
            {"args": [4], "expected": 2},
            {"args": [1], "expected": 1},
            {"args": [8], "expected": 92},
            {"args": [5], "expected": 10},
            {"args": [6], "expected": 4}
        ],
        "def total_n_queens(n: int) -> int:\n    count = 0\n    def backtrack(row, cols, diag1, diag2):\n        nonlocal count\n        if row == n:\n            count += 1\n            return\n        avail = ((1 << n) - 1) & ~(cols | diag1 | diag2)\n        while avail:\n            p = avail & -avail\n            avail &= avail - 1\n            backtrack(row + 1, cols | p, (diag1 | p) << 1, (diag2 | p) >> 1)\n    backtrack(0, 0, 0, 0)\n    return count\n"
    ),

    P(
        "range-sum-query-mutable", "Range Sum Query - Mutable (Segment Tree)", "advanced-dsa", 4, "simulate_segment_tree",
        "Implement a Segment Tree for dynamic range sum queries with point updates. Given initial array `nums` and a list of operations `[['update', index, val], ['sumRange', left, right]]`, return the list of query outputs (returns `None` for `update`, and the computed sum for `sumRange`).",
        "- `1 <= len(nums) <= 3 * 10^4`\n- `-100 <= nums[i] <= 100`\n- At most `3 * 10^4` calls to `update` and `sumRange`",
        "O(log n) per op", "O(n)",
        "def simulate_segment_tree(nums: list[int], operations: list) -> list:\n    pass\n",
        [
            {"args": [[1, 3, 5], [["sumRange", 0, 2], ["update", 1, 2], ["sumRange", 0, 2]]],
             "expected": [9, None, 8]},
            {"args": [[7, 2, 7, 2, 0], [["update", 4, 6], ["update", 0, 2], ["sumRange", 0, 4]]],
             "expected": [None, None, 19]},
            {"args": [[1], [["sumRange", 0, 0]]],
             "expected": [1]}
        ],
        "def simulate_segment_tree(nums: list[int], operations: list) -> list:\n    n = len(nums)\n    tree = [0] * (2 * n)\n    for i in range(n):\n        tree[n + i] = nums[i]\n    for i in range(n - 1, 0, -1):\n        tree[i] = tree[2 * i] + tree[2 * i + 1]\n    out = []\n    for op in operations:\n        cmd = op[0]\n        if cmd == 'update':\n            idx, val = op[1], op[2]\n            pos = n + idx\n            tree[pos] = val\n            while pos > 1:\n                pos //= 2\n                tree[pos] = tree[2 * pos] + tree[2 * pos + 1]\n            out.append(None)\n        elif cmd == 'sumRange':\n            l, r = op[1], op[2]\n            l += n\n            r += n + 1\n            total = 0\n            while l < r:\n                if l % 2 == 1:\n                    total += tree[l]\n                    l += 1\n                if r % 2 == 1:\n                    r -= 1\n                    total += tree[r]\n                l //= 2\n                r //= 2\n            out.append(total)\n    return out\n"
    ),

    P(
        "lfu-cache", "LFU Cache Simulation (Least Frequently Used)", "advanced-dsa", 5, "simulate_lfu_cache",
        "Simulate an LFU (Least Frequently Used) Cache of given `capacity`. Operations: `[['put', key, value], ['get', key]]`. Return the results list (`None` on `put`, value or `-1` on `get`). When capacity is reached, evict the least frequently used key, tie-breaking by least recently used.",
        "- `0 <= capacity <= 10^4`\n- `0 <= key <= 10^5`\n- At most `2 * 10^4` calls",
        "O(1) per op", "O(capacity)",
        "def simulate_lfu_cache(capacity: int, operations: list) -> list:\n    pass\n",
        [
            {"args": [2, [["put", 1, 1], ["put", 2, 2], ["get", 1], ["put", 3, 3], ["get", 2], ["get", 3], ["put", 4, 4], ["get", 1], ["get", 3], ["get", 4]]],
             "expected": [None, None, 1, None, -1, 3, None, -1, 3, 4]},
            {"args": [0, [["put", 0, 0], ["get", 0]]],
             "expected": [None, -1]}
        ],
        "from collections import defaultdict, OrderedDict\n\ndef simulate_lfu_cache(capacity: int, operations: list) -> list:\n    if capacity <= 0:\n        return [None if op[0] == 'put' else -1 for op in operations]\n    key_val = {}\n    key_freq = {}\n    freq_keys = defaultdict(OrderedDict)\n    min_freq = 0\n    out = []\n    for op in operations:\n        cmd = op[0]\n        if cmd == 'get':\n            key = op[1]\n            if key not in key_val:\n                out.append(-1)\n            else:\n                freq = key_freq[key]\n                val = key_val[key]\n                del freq_keys[freq][key]\n                if not freq_keys[freq] and min_freq == freq:\n                    min_freq += 1\n                key_freq[key] = freq + 1\n                freq_keys[freq + 1][key] = True\n                out.append(val)\n        elif cmd == 'put':\n            key, val = op[1], op[2]\n            if key in key_val:\n                key_val[key] = val\n                freq = key_freq[key]\n                del freq_keys[freq][key]\n                if not freq_keys[freq] and min_freq == freq:\n                    min_freq += 1\n                key_freq[key] = freq + 1\n                freq_keys[freq + 1][key] = True\n            else:\n                if len(key_val) >= capacity:\n                    evict_key, _ = freq_keys[min_freq].popitem(last=False)\n                    del key_val[evict_key]\n                    del key_freq[evict_key]\n                key_val[key] = val\n                key_freq[key] = 1\n                freq_keys[1][key] = True\n                min_freq = 1\n            out.append(None)\n    return out\n"
    ),

    P(
        "word-search-ii", "Word Search II (Prefix Trie + 2D Backtracking)", "advanced-dsa", 5, "find_words",
        "Given an `m x n` board of characters and a list of strings `words`, return all words on the board.\n\nEach word must be constructed from letters of sequentially adjacent cells (horizontally or vertically neighboring). Return the found words sorted lexicographically.",
        "- `1 <= m, n <= 12`\n- `1 <= len(words) <= 3 * 10^4`\n- `1 <= len(words[i]) <= 10`",
        "O(m * n * 4^L)", "O(total trie chars)",
        "def find_words(board: list[list[str]], words: list[str]) -> list[str]:\n    pass\n",
        [
            {"args": [
                [["o", "a", "a", "n"],
                 ["e", "t", "a", "e"],
                 ["i", "h", "k", "r"],
                 ["i", "f", "l", "v"]],
                ["oath", "pea", "eat", "rain"]
            ], "expected": ["eat", "oath"]},
            {"args": [
                [["a", "b"],
                 ["c", "d"]],
                ["abcb"]
            ], "expected": []},
            {"args": [
                [["a"]],
                ["a"]
            ], "expected": ["a"]}
        ],
        "def find_words(board: list[list[str]], words: list[str]) -> list[str]:\n    trie = {}\n    for word in words:\n        node = trie\n        for ch in word:\n            node = node.setdefault(ch, {})\n        node['$'] = word\n    m, n = len(board), len(board[0])\n    found = set()\n    def dfs(r, c, parent):\n        ch = board[r][c]\n        curr_node = parent.get(ch)\n        if not curr_node:\n            return\n        if '$' in curr_node:\n            found.add(curr_node['$'])\n        board[r][c] = '#'\n        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:\n            nr, nc = r + dr, c + dc\n            if 0 <= nr < m and 0 <= nc < n and board[nr][nc] != '#':\n                dfs(nr, nc, curr_node)\n        board[r][c] = ch\n    for r in range(m):\n        for c in range(n):\n            dfs(r, c, trie)\n    return sorted(list(found))\n"
    )
]
