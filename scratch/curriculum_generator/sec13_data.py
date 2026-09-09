"""
Section 13: Dynamic Programming (Days 146 to 155)
"""

SEC13_DAYS = {   146: {   'hint': 'Base cases: if n <= 1 return n. a, b = 0, 1. Loop _ in range(2, n + 1): a, b = b, a + b. Return '
                     'b.',
             'mechanics': 'Top-Down: write recursive brute-force, wrap with `@functools.lru_cache(None)` to cache '
                          'intermediate returns in a hash table. Bottom-Up Tabulation: create table `dp = [0] * (n + '
                          '1)`, fill base cases, and evaluate states iteratively in topological order. Tabulation '
                          'eliminates recursion stack overhead.',
             'patterns': ['Fib(10): 55', 'Fib(30): 832040'],
             'practice_task': 'Implement bottom-up tabulation to compute the N-th Fibonacci number in O(N) time and '
                              'O(1) auxiliary space.',
             'q1': 'Why does Top-Down memoization reduce the time complexity of computing Fibonacci from O(2^N) to '
                   'O(N)?',
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! Without memoization, the recursive tree branches into 2^N duplicate calls. '
                                'Caching ensures only N unique subproblems `[0..N]` are computed, each taking O(1) '
                                'additions. Total: O(N).',
                           'B': 'Incorrect: Python interpreter executes standard bytecode.',
                           'C': 'Incorrect: Top-down recursion still consumes call stack frames.',
                           'D': 'Incorrect: Complexity represents operation counts, which are positive.'},
             'q1_opts': [   {   'id': 'A',
                                'label': 'Each distinct subproblem state fib(k) is computed exactly once and cached; '
                                         'subsequent encounters retrieve the answer in O(1) time'},
                            {'id': 'B', 'label': 'Because memoization compiles Python code to C'},
                            {'id': 'C', 'label': 'Because the call stack is bypassed entirely'},
                            {'id': 'D', 'label': 'Because 2^N becomes negative for large N'}],
             'q2': 'What is the primary operational advantage of Bottom-Up Tabulation over Top-Down Memoization?',
             'q2_ans': 'A',
             'q2_exp': {   'A': "Correct! Python's default recursion limit is 1000. For large N (e.g. 100,000), "
                                'top-down crashes with stack overflow. Bottom-up loops never overflow and can discard '
                                'older states to achieve O(1) space.',
                           'B': 'Incorrect: DP state ordering requires a DAG (no cycles).',
                           'C': 'Incorrect: Base cases are mandatory in all DP.',
                           'D': 'Incorrect: Time depends on total state transitions.'},
             'q2_opts': [   {   'id': 'A',
                                'label': "Tabulation avoids Python's `RecursionError` call stack limits and allows "
                                         'rolling-variable space optimization (e.g. from O(N) to O(1))'},
                            {'id': 'B', 'label': 'Tabulation works on graphs with negative cycles'},
                            {'id': 'C', 'label': 'Tabulation does not require base cases'},
                            {'id': 'D', 'label': 'Tabulation is always O(1) time'}],
             'recap': [   {   'concept': 'Overlapping Subproblems',
                              'naiveIntuition': 'Recursion calculates each branch independently',
                              'pythonReality': 'Identifying identical redundant subproblem states allows caching to '
                                               'collapse exponential trees into polynomial linear paths'},
                          {   'concept': 'State Reduction',
                              'naiveIntuition': 'Always allocate a full dp array of size N + 1',
                              'pythonReality': 'When transition relations only reference the last K previous states, '
                                               'rolling variables reduce memory from O(N) to O(1)'}],
             'sample_code': '# Top-Down with Memoization vs Bottom-Up Tabulation\n'
                            '# Fibonacci example\n'
                            'def fib_memo(n, memo={}):\n'
                            '    if n <= 1: return n\n'
                            '    if n not in memo: memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)\n'
                            '    return memo[n]\n'
                            '\n'
                            'def fib_tab(n):\n'
                            '    if n <= 1: return n\n'
                            '    a, b = 0, 1\n'
                            '    for _ in range(2, n + 1): a, b = b, a + b\n'
                            '    return b',
             'solution': 'def fibonacci(n: int) -> int:\n'
                         '    if n <= 1:\n'
                         '        return n\n'
                         '    a, b = 0, 1\n'
                         '    for _ in range(2, n + 1):\n'
                         '        a, b = b, a + b\n'
                         '    return b\n'
                         '\n'
                         "print('Fib(10):', fibonacci(10))\n"
                         "print('Fib(30):', fibonacci(30))\n",
             'starter': 'def fibonacci(n: int) -> int:\n'
                        '    # TODO: Implement O(N) time and O(1) space Fibonacci\n'
                        '    return 0\n'
                        '\n'
                        "print('Fib(10):', fibonacci(10)) # 55\n"
                        "print('Fib(30):', fibonacci(30)) # 832040\n",
             'summary': 'Dynamic Programming solves complex problems by breaking them down into Overlapping '
                        'Subproblems and Optimal Substructures, evaluated via Top-Down Memoization or Bottom-Up '
                        'Tabulation.',
             'takeaway': 'Memoization caches top-down recursion; Tabulation builds bottom-up tables iteratively '
                         'without stack frames.'},
    147: {   'hint': 'prev1 = prev2 = 0. Loop x in nums: curr = max(prev1, x + prev2); prev2 = prev1; prev1 = curr. '
                     'Return prev1.',
             'mechanics': 'House Robber recurrence: at house `i`, decide to rob (`nums[i] + dp[i-2]`) or skip '
                          '(`dp[i-1]`). State transition: `dp[i] = max(dp[i - 1], nums[i] + dp[i - 2])`. Because '
                          '`dp[i]` depends only on the immediate two previous states, maintain `prev2` and `prev1` '
                          'variables in O(1) space.',
             'patterns': ['Max loot [1, 2, 3, 1]: 4', 'Max loot [2, 7, 9, 3, 1]: 12'],
             'practice_task': 'Calculate the maximum loot obtainable without robbing adjacent houses.',
             'q1': 'In House Robber, why does `max(prev1, x + prev2)` guarantee that no two adjacent houses are ever '
                   'robbed?',
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! The two choices are: (1) Skip house `i`, retaining `prev1` (which might have '
                                'robbed house `i-1`). (2) Rob house `i` (`x`), which forbids robbing house `i-1`, '
                                'adding `x` to `prev2`.',
                           'B': 'Incorrect: All houses are considered.',
                           'C': 'Incorrect: Algorithmic constraint, not physics.',
                           'D': 'Incorrect: Street order is fixed.'},
             'q1_opts': [   {   'id': 'A',
                                'label': 'If we choose to rob house `x`, its loot is added exclusively to `prev2` (the '
                                         'optimal loot up to two houses prior), strictly skipping the adjacent house '
                                         '`prev1`'},
                            {'id': 'B', 'label': 'Because houses with odd indices are deleted'},
                            {'id': 'C', 'label': 'Because the police alarm resets every two minutes'},
                            {'id': 'D', 'label': 'Because nums is sorted in ascending order'}],
             'q2': 'How is House Robber II (where houses are arranged in a circle) solved using the standard linear '
                   'House Robber algorithm?',
             'q2_ans': 'A',
             'q2_exp': {   'A': 'Correct! In a circle, house 0 and house N - 1 are adjacent and cannot both be robbed. '
                                'Thus, any valid solution either excludes house 0 or excludes house N - 1. Two linear '
                                'runs cover all cases in O(N).',
                           'B': 'Incorrect: Division alters profits.',
                           'C': 'Incorrect: Sorting destroys neighborhood adjacency.',
                           'D': 'Incorrect: Runs in strict O(N) linear time.'},
             'q2_opts': [   {   'id': 'A',
                                'label': 'Run standard House Robber twice: once on `nums[1:]` (excluding first house) '
                                         'and once on `nums[:-1]` (excluding last house), returning the maximum'},
                            {'id': 'B', 'label': 'Divide all house values by 2'},
                            {'id': 'C', 'label': 'Sort the houses by loot'},
                            {'id': 'D', 'label': 'Circular house robber cannot be solved in polynomial time'}],
             'recap': [   {   'concept': 'State Space Compression',
                              'naiveIntuition': 'Maintain a full dp array of size N',
                              'pythonReality': 'When the transition recurrence only looks back 2 steps, 2 scalar '
                                               'variables achieve identical results with zero memory allocations'},
                          {   'concept': 'Boundary Decoupling in Cycles',
                              'naiveIntuition': 'Cycles require specialized circular algorithms',
                              'pythonReality': 'Circular dependencies can be split into two linear sub-problems by '
                                               'fixing the state of one boundary node'}],
             'sample_code': '# House Robber in O(1) space\n'
                            'def rob(nums):\n'
                            '    prev1 = prev2 = 0\n'
                            '    for x in nums:\n'
                            '        curr = max(prev1, x + prev2)\n'
                            '        prev2 = prev1\n'
                            '        prev1 = curr\n'
                            '    return prev1',
             'solution': 'def rob_houses(nums: list[int]) -> int:\n'
                         '    prev1 = prev2 = 0\n'
                         '    for x in nums:\n'
                         '        curr = max(prev1, x + prev2)\n'
                         '        prev2 = prev1\n'
                         '        prev1 = curr\n'
                         '    return prev1\n'
                         '\n'
                         "print('Max loot [1, 2, 3, 1]:', rob_houses([1, 2, 3, 1]))\n"
                         "print('Max loot [2, 7, 9, 3, 1]:', rob_houses([2, 7, 9, 3, 1]))\n",
             'starter': 'def rob_houses(nums: list[int]) -> int:\n'
                        '    # TODO: Implement House Robber in O(N) time and O(1) space\n'
                        '    return 0\n'
                        '\n'
                        "print('Max loot [1, 2, 3, 1]:', rob_houses([1, 2, 3, 1])) # 4 (1 + 3)\n"
                        "print('Max loot [2, 7, 9, 3, 1]:', rob_houses([2, 7, 9, 3, 1])) # 12 (2 + 9 + 1)\n",
             'summary': '1D Dynamic Programming optimizes linear sequence decisions where the current choice depends '
                        'on previous optimal choices, exemplified by House Robber with O(1) rolling space.',
             'takeaway': 'Binary choice at step i (include vs exclude) yields dp[i] = max(skip, take + dp[i-2]), '
                         'optimized to O(1) space.'},
    148: {   'hint': 'dp = [inf] * C; dp[0] = 0. Loop r: dp[0] += grid[r][0]; loop c from 1 to C-1: dp[c] = grid[r][c] '
                     '+ min(dp[c], dp[c-1]). Return dp[-1].',
             'mechanics': 'Unique Paths recurrence: `dp[r][c] = dp[r-1][c] + dp[r][c-1]`. Minimum Path Sum recurrence: '
                          '`dp[r][c] = grid[r][c] + min(dp[r-1][c], dp[r][c-1])`. Top row and left column serve as '
                          'base cases. Rolling array: `dp[c] = dp[c] + dp[c-1]` optimizes space from O(R * C) to O(C).',
             'patterns': ['Min path sum: 7'],
             'practice_task': 'Calculate the minimum path sum from top-left to bottom-right in a grid with '
                              'non-negative numbers.',
             'q1': 'Why can 2D Grid DP be optimized from an R x C table down to a single 1D array of size C?',
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! In the update `dp[c] += dp[c-1]`, `dp[c]` on the right side holds the value '
                                'from row `r-1`, while `dp[c-1]` holds the newly updated value from row `r`. '
                                'Historical rows older than `r-1` are never referenced again.',
                           'B': 'Incorrect: Works for any rectangular dimensions.',
                           'C': 'Incorrect: Rows below r are not yet computed.',
                           'D': 'Incorrect: Time complexity remains O(R * C).'},
             'q1_opts': [   {   'id': 'A',
                                'label': "Computing cell (r, c) only requires the value from the current row's left "
                                         "neighbor `dp[c - 1]` and the previous row's cell `dp[c]` at the exact same "
                                         'column'},
                            {'id': 'B', 'label': 'Because the grid is a square'},
                            {'id': 'C', 'label': 'Because rows below r are already calculated'},
                            {'id': 'D', 'label': 'To make the algorithm run in O(1) time'}],
             'q2': 'In Minimum Path Sum with obstacles, what value should be assigned to an obstacle cell during DP '
                   'transitions?',
             'q2_ans': 'A',
             'q2_exp': {   'A': 'Correct! Setting obstacle cost to infinity guarantees `min()` will never choose to '
                                'route through that cell. For counting paths, setting paths to 0 ensures it '
                                'contributes nothing to downstream cells.',
                           'B': 'Incorrect: Negative numbers would attract minimum path searches.',
                           'C': 'Incorrect: Arbitrary sum.',
                           'D': 'Incorrect: Grid topology must be preserved.'},
             'q2_opts': [   {   'id': 'A',
                                'label': 'Infinity (or 0 for path counts), effectively blocking paths from traveling '
                                         'through that cell'},
                            {'id': 'B', 'label': '-1'},
                            {'id': 'C', 'label': 'The sum of all grid cells'},
                            {'id': 'D', 'label': 'Delete the obstacle column'}],
             'recap': [   {   'concept': 'Topological Grid DAG',
                              'naiveIntuition': 'Grids can have cycles',
                              'pythonReality': 'Restricting moves to right and down guarantees that grid coordinates '
                                               'form a Directed Acyclic Graph with natural row-major topological '
                                               'order'},
                          {   'concept': 'Row-Level Memory Reclamation',
                              'naiveIntuition': 'Always allocate R x C matrices',
                              'pythonReality': 'Maintaining only the active row buffer reduces space complexity from '
                                               'O(R * C) to O(C)'}],
             'sample_code': '# Unique Paths in O(C) Space\n'
                            'def unique_paths(m, n):\n'
                            '    dp = [1] * n\n'
                            '    for r in range(1, m):\n'
                            '        for c in range(1, n):\n'
                            '            dp[c] += dp[c - 1]\n'
                            '    return dp[-1]',
             'solution': 'def min_path_sum(grid: list[list[int]]) -> int:\n'
                         '    R, C = len(grid), len(grid[0])\n'
                         "    dp = [float('inf')] * C\n"
                         '    dp[0] = 0\n'
                         '    for r in range(R):\n'
                         '        dp[0] += grid[r][0]\n'
                         '        for c in range(1, C):\n'
                         '            dp[c] = grid[r][c] + min(dp[c], dp[c - 1])\n'
                         '    return dp[-1]\n'
                         '\n'
                         'g = [\n'
                         '  [1, 3, 1],\n'
                         '  [1, 5, 1],\n'
                         '  [4, 2, 1]\n'
                         ']\n'
                         "print('Min path sum:', min_path_sum(g))\n",
             'starter': 'def min_path_sum(grid: list[list[int]]) -> int:\n'
                        '    # TODO: Implement 2D Grid DP for Minimum Path Sum\n'
                        '    return 0\n'
                        '\n'
                        'g = [\n'
                        '  [1, 3, 1],\n'
                        '  [1, 5, 1],\n'
                        '  [4, 2, 1]\n'
                        ']\n'
                        "print('Min path sum:', min_path_sum(g)) # 7 (1 -> 3 -> 1 -> 1 -> 1)\n",
             'summary': '2D Grid Dynamic Programming evaluates optimal paths across matrices where moves are '
                        'restricted (e.g. right and down), solved in O(R * C) time with O(C) rolling array space.',
             'takeaway': 'Grid cells depend strictly on top and left neighbors, allowing row-by-row 1D space '
                         'compression.'},
    149: {   'hint': 'total = sum(nums). If total % 2 != 0 return False. target = total // 2. dp = [False] * (target + '
                     '1); dp[0] = True. Loop x in nums: loop w from target down to x: if dp[w - x]: dp[w] = True. '
                     'Return dp[target].',
             'mechanics': '2D recurrence: `dp[i][w] = max(dp[i-1][w], val[i] + dp[i-1][w - wt[i]])`. 1D space '
                          'optimization: `dp = [0] * (W + 1)`. When evaluating item `(val, wt)`: loop capacity `w` '
                          'BACKWARDS from `W` down to `wt`: `dp[w] = max(dp[w], val + dp[w - wt])`. Backwards '
                          'iteration prevents reusing the same item multiple times.',
             'patterns': ['Can partition [1, 5, 11, 5]: True', 'Can partition [1, 2, 3, 5]: False'],
             'practice_task': 'Determine if an array can be partitioned into two subsets with equal sum using 0/1 '
                              'Knapsack.',
             'q1': 'Why MUST the capacity loop iterate in REVERSE order (from W down to weight) when using a 1D DP '
                   'array for 0/1 Knapsack?',
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! In a 1D array, `dp[cap - w]` needs to represent the state from the PREVIOUS '
                                'item. Scanning left-to-right overwrites `dp[cap - w]` with the current item first, '
                                'causing duplicate inclusions. Scanning right-to-left reads the pristine previous row '
                                'values.',
                           'B': 'Incorrect: Python range() works in either direction.',
                           'C': 'Incorrect: Array order represents capacities, not item weights.',
                           'D': 'Incorrect: The loop stops safely at w.'},
             'q1_opts': [   {   'id': 'A',
                                'label': 'Forward iteration would use the newly updated values from the CURRENT item, '
                                         'accidentally allowing the same item to be included multiple times (Unbounded '
                                         'Knapsack)'},
                            {'id': 'B', 'label': 'Because Python range() only works backwards with steps'},
                            {'id': 'C', 'label': 'To sort the weights in descending order'},
                            {'id': 'D', 'label': 'To avoid reaching index 0'}],
             'q2': 'What classic problem is directly equivalent to 0/1 Knapsack?',
             'q2_ans': 'A',
             'q2_exp': {   'A': 'Correct! If `sum(nums)` is even, the question is: can we find a subset of items whose '
                                'total weight equals exactly `target = sum(nums) // 2`? This is identical to a 0/1 '
                                "knapsack where each number's weight equals its value.",
                           'B': 'Incorrect: LCS is a 2-sequence string alignment problem.',
                           'C': 'Incorrect: Dijkstra is graph shortest paths.',
                           'D': 'Incorrect: Topo sort is DAG vertex ordering.'},
             'q2_opts': [   {   'id': 'A',
                                'label': 'Partition Equal Subset Sum (determining if an array can be partitioned into '
                                         'two subsets with equal sum = sum(nums) // 2)'},
                            {'id': 'B', 'label': 'Longest Common Subsequence'},
                            {'id': 'C', 'label': "Dijkstra's Shortest Path"},
                            {'id': 'D', 'label': 'Topological Sort'}],
             'recap': [   {   'concept': 'Reverse Sweep State Shielding',
                              'naiveIntuition': 'Forward iteration works for all DP',
                              'pythonReality': "Reverse sweeps in 1D arrays shield the previous layer's state from "
                                               'being overwritten, enforcing strict 0/1 item exclusivity'},
                          {   'concept': 'Pseudo-Polynomial Complexity',
                              'naiveIntuition': 'O(N * W) is polynomial in input size',
                              'pythonReality': 'Because W is encoded in log(W) bits, O(N * W) is pseudo-polynomial; '
                                               'knapsack is weakly NP-complete'}],
             'sample_code': '# 0/1 Knapsack in O(W) space\n'
                            'def knapsack_01(values, weights, W):\n'
                            '    dp = [0] * (W + 1)\n'
                            '    for v, w in zip(values, weights):\n'
                            '        for cap in range(W, w - 1, -1): # Reverse sweep!\n'
                            '            dp[cap] = max(dp[cap], v + dp[cap - w])\n'
                            '    return dp[W]',
             'solution': 'def can_partition(nums: list[int]) -> bool:\n'
                         '    total = sum(nums)\n'
                         '    if total % 2 != 0:\n'
                         '        return False\n'
                         '    target = total // 2\n'
                         '    dp = [False] * (target + 1)\n'
                         '    dp[0] = True\n'
                         '    for x in nums:\n'
                         '        for w in range(target, x - 1, -1):\n'
                         '            if dp[w - x]:\n'
                         '                dp[w] = True\n'
                         '    return dp[target]\n'
                         '\n'
                         "print('Can partition [1, 5, 11, 5]:', can_partition([1, 5, 11, 5]))\n"
                         "print('Can partition [1, 2, 3, 5]:', can_partition([1, 2, 3, 5]))\n",
             'starter': 'def can_partition(nums: list[int]) -> bool:\n'
                        '    # TODO: Implement 0/1 knapsack backwards sweep for Partition Equal Subset Sum\n'
                        '    return False\n'
                        '\n'
                        "print('Can partition [1, 5, 11, 5]:', can_partition([1, 5, 11, 5])) # True (1 + 5 + 5 = 11)\n"
                        "print('Can partition [1, 2, 3, 5]:', can_partition([1, 2, 3, 5]))   # False\n",
             'summary': '0/1 Knapsack solves discrete subset selection under capacity constraints by deciding whether '
                        'to include or exclude each item, requiring backwards 1D array traversal in O(N * W) time.',
             'takeaway': 'Iterating capacity backwards in 1D array guarantees each item is used at most once (0/1 '
                         'constraint).'},
    150: {   'hint': "dp = [float('inf')] * (amount + 1); dp[0] = 0. Loop a from 1 to amount: loop c in coins: if a - "
                     'c >= 0: dp[a] = min(dp[a], 1 + dp[a - c]). Return dp[amount] if != inf else -1.',
             'mechanics': "Initialize `dp = [float('inf')] * (amount + 1)`, `dp[0] = 0`. For each `amt` from 1 to "
                          '`amount`: for each `c` in `coins`: if `amt - c >= 0`: `dp[amt] = min(dp[amt], 1 + dp[amt - '
                          'c])`. Returns `dp[amount]` if not infinity else -1. Total time: O(amount * len(coins)).',
             'patterns': ['Coins for 11 [1, 2, 5]: 3', 'Coins for 3 [2]: -1'],
             'practice_task': 'Calculate the fewest number of coins needed to make up an amount.',
             'q1': 'Why is `dp[0]` initialized to 0 in Coin Change?',
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! When making amount `c` with a single coin of value `c`, `1 + dp[c - c] = 1 + '
                                'dp[0] = 1 + 0 = 1`. A base of 0 grounds all subsequent additions.',
                           'B': "Incorrect: We explicitly initialize with float('inf').",
                           'C': 'Incorrect: Array has size amount + 1.',
                           'D': 'Incorrect: Base case reflects economic reality of zero target.'},
             'q1_opts': [   {   'id': 'A',
                                'label': 'It takes exactly 0 coins to make a total amount of 0, serving as the base '
                                         'case for all valid subproblems'},
                            {'id': 'B', 'label': 'Because 0 is the default value in Python arrays'},
                            {'id': 'C', 'label': 'To prevent an IndexError at index 0'},
                            {'id': 'D', 'label': 'Because coins cannot have value 0'}],
             'q2': 'What is the difference in loop ordering between finding MINIMUM COINS (Coin Change I) versus '
                   'finding NUMBER OF COMBINATIONS (Coin Change II)?',
             'q2_ans': 'A',
             'q2_exp': {   'A': 'Correct! In combinations, placing coins in the outer loop ensures we consider each '
                                'coin type once in sequence, counting [1, 2] but NOT [2, 1]. For minimum coins, order '
                                'does not change the minimum count.',
                           'B': 'Incorrect: Reversing amount loop is for 0/1 knapsack, not combinations.',
                           'C': 'Incorrect: Inner vs outer loop completely changes combination vs permutation counts.',
                           'D': 'Incorrect: Sorting coins is only an optional speedup.'},
             'q2_opts': [   {   'id': 'A',
                                'label': 'Min Coins can iterate coins inside or outside, but Combinations MUST iterate '
                                         'coins in the outer loop to prevent counting permutations as distinct '
                                         'solutions'},
                            {'id': 'B', 'label': 'Combinations requires reversing the amount loop'},
                            {'id': 'C', 'label': 'There is no difference'},
                            {'id': 'D', 'label': 'Min Coins requires sorting the coins'}],
             'recap': [   {   'concept': 'Unbounded Optimal Transition',
                              'naiveIntuition': 'Try all possible coin counts recursively',
                              'pythonReality': 'Evaluating states by target amount builds solutions from smallest '
                                               'amounts upward in O(amount * num_coins) time'},
                          {   'concept': 'Loop Order Invariance in Extremums',
                              'naiveIntuition': 'Loop order always matters',
                              'pythonReality': 'When finding a min or max extremum, order of addition does not affect '
                                               'the optimal scalar value'}],
             'sample_code': '# Coin Change (Min Coins)\n'
                            'def coin_change(coins, amount):\n'
                            "    dp = [float('inf')] * (amount + 1)\n"
                            '    dp[0] = 0\n'
                            '    for a in range(1, amount + 1):\n'
                            '        for c in coins:\n'
                            '            if a - c >= 0:\n'
                            '                dp[a] = min(dp[a], 1 + dp[a - c])\n'
                            "    return dp[amount] if dp[amount] != float('inf') else -1",
             'solution': 'def min_coins(coins: list[int], amount: int) -> int:\n'
                         "    dp = [float('inf')] * (amount + 1)\n"
                         '    dp[0] = 0\n'
                         '    for a in range(1, amount + 1):\n'
                         '        for c in coins:\n'
                         '            if a - c >= 0:\n'
                         '                dp[a] = min(dp[a], 1 + dp[a - c])\n'
                         "    return dp[amount] if dp[amount] != float('inf') else -1\n"
                         '\n'
                         "print('Coins for 11 [1, 2, 5]:', min_coins([1, 2, 5], 11))\n"
                         "print('Coins for 3 [2]:', min_coins([2], 3))\n",
             'starter': 'def min_coins(coins: list[int], amount: int) -> int:\n'
                        '    # TODO: Implement 1D DP for Coin Change\n'
                        '    return -1\n'
                        '\n'
                        "print('Coins for 11 [1, 2, 5]:', min_coins([1, 2, 5], 11)) # 3 (5 + 5 + 1)\n"
                        "print('Coins for 3 [2]:', min_coins([2], 3))             # -1\n",
             'summary': 'Coin Change (Fewest Coins to Make Amount) models Unbounded Knapsack where each denomination '
                        'can be used unlimited times, solved by iterating over amounts from 1 to A.',
             'takeaway': 'Unbounded choices allow reusing the same coin, filling dp[amt] = min(dp[amt], 1 + dp[amt - '
                         'c]).'},
    151: {   'hint': 'tails = []. Loop x in nums: idx = bisect_left(tails, x); if idx == len(tails): tails.append(x) '
                     'else: tails[idx] = x. Return len(tails).',
             'mechanics': 'O(N^2) DP: `dp[i] = 1 + max([dp[j] for j in range(i) if nums[j] < nums[i]] or [0])`. O(N '
                          'log N) Patience Sorting: maintain `tails` array where `tails[i]` stores the smallest tail '
                          'of all increasing subsequences of length `i + 1`. For each `x`, binary search '
                          '(`bisect_left`) for `x` in `tails` and update or append.',
             'patterns': ['LIS length: 4'],
             'practice_task': 'Find the length of the Longest Increasing Subsequence in O(N log N) time.',
             'q1': 'What does `tails[k]` represent in the O(N log N) patience sorting algorithm for LIS?',
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! Keeping the tail element as small as possible maximizes future opportunities '
                                'for subsequent numbers to extend that subsequence. `tails` is strictly monotonic, '
                                'enabling binary search via `bisect_left`.',
                           'B': 'Incorrect: `tails` stores element values, not counts.',
                           'C': 'Incorrect: Crucial distinction: `tails` does NOT represent the actual subsequence, '
                                'only its length and boundary candidates.',
                           'D': 'Incorrect: Sum is unrelated.'},
             'q1_opts': [   {   'id': 'A',
                                'label': 'The SMALLEST tail element among all valid increasing subsequences of length '
                                         '`k + 1` found so far'},
                            {'id': 'B', 'label': 'The total number of subsequences of length k'},
                            {'id': 'C', 'label': 'The actual elements of the longest increasing subsequence in order'},
                            {'id': 'D', 'label': 'The sum of elements in the longest subsequence'}],
             'q2': 'Why does `bisect_left(tails, x)` take O(log N) time?',
             'q2_ans': 'A',
             'q2_exp': {   'A': 'Correct! By invariant, an increasing subsequence of length k+1 must have a strictly '
                                'larger tail than a subsequence of length k. Thus, `tails` is always sorted, enabling '
                                'logarithmic binary search.',
                           'B': 'Incorrect: `nums` is an unsorted arbitrary array.',
                           'C': 'Incorrect: Bisect is binary search on a list.',
                           'D': 'Incorrect: Tails can grow up to length N.'},
             'q2_opts': [   {   'id': 'A',
                                'label': 'The `tails` array is mathematically guaranteed to remain strictly sorted in '
                                         'ascending order at all times'},
                            {'id': 'B', 'label': 'Because `nums` was sorted before execution'},
                            {'id': 'C', 'label': 'Because bisect uses a hash table'},
                            {'id': 'D', 'label': 'Because tails cannot exceed length 20'}],
             'recap': [   {   'concept': 'Greedy-DP Hybridization',
                              'naiveIntuition': 'DP must always inspect all j < i in O(N^2)',
                              'pythonReality': 'Combining DP state definitions with greedy patience sorting reduces '
                                               'the transition lookup to O(log N)'},
                          {   'concept': 'Tail Candidate Dominance',
                              'naiveIntuition': 'Store all valid subsequences in memory',
                              'pythonReality': 'Only the minimal tail value for each length matters for future growth; '
                                               'all higher tails for the same length are dominated'}],
             'sample_code': '# LIS in O(N log N) using Patience Sorting\n'
                            'from bisect import bisect_left\n'
                            'def length_of_lis(nums):\n'
                            '    tails = []\n'
                            '    for x in nums:\n'
                            '        idx = bisect_left(tails, x)\n'
                            '        if idx == len(tails): tails.append(x)\n'
                            '        else: tails[idx] = x\n'
                            '    return len(tails)',
             'solution': 'from bisect import bisect_left\n'
                         '\n'
                         'def longest_increasing_subsequence(nums: list[int]) -> int:\n'
                         '    tails = []\n'
                         '    for x in nums:\n'
                         '        idx = bisect_left(tails, x)\n'
                         '        if idx == len(tails):\n'
                         '            tails.append(x)\n'
                         '        else:\n'
                         '            tails[idx] = x\n'
                         '    return len(tails)\n'
                         '\n'
                         'nums = [10, 9, 2, 5, 3, 7, 101, 18]\n'
                         "print('LIS length:', longest_increasing_subsequence(nums))\n",
             'starter': 'from bisect import bisect_left\n'
                        '\n'
                        'def longest_increasing_subsequence(nums: list[int]) -> int:\n'
                        '    # TODO: Implement O(N log N) LIS using bisect_left\n'
                        '    return 0\n'
                        '\n'
                        'nums = [10, 9, 2, 5, 3, 7, 101, 18]\n'
                        "print('LIS length:', longest_increasing_subsequence(nums)) # 4 ([2, 3, 7, 101] or [2, 5, 7, "
                        '18])\n',
             'summary': 'Longest Increasing Subsequence (LIS) finds the longest strictly ascending subsequence, '
                        'solvable in O(N^2) using 1D DP and in O(N log N) using Patience Sorting with binary search.',
             'takeaway': 'Patience sorting replaces quadratic subproblem scans with binary search on monotonic tail '
                         'candidates.'},
    152: {   'hint': 'dp = [[0] * (m + 1) for _ in range(n + 1)]. Loop i 1..n: loop j 1..m: if text1[i-1] == '
                     'text2[j-1]: dp[i][j] = 1 + dp[i-1][j-1] else: dp[i][j] = max(dp[i-1][j], dp[i][j-1]). Return '
                     'dp[n][m].',
             'mechanics': 'Table `dp[i][j]` represents LCS of `s1[:i]` and `s2[:j]`. If `s1[i - 1] == s2[j - 1]`: '
                          'match! `dp[i][j] = 1 + dp[i - 1][j - 1]`. Else mismatch: take best without s1 character or '
                          'without s2 character: `dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])`. Backtracking from '
                          '`dp[N][M]` recovers the sequence string.',
             'patterns': ['LCS(abcde, ace): 3', 'LCS(abc, def): 0'],
             'practice_task': 'Calculate the length of the Longest Common Subsequence between two strings.',
             'q1': 'Why do we add 1 to `dp[i - 1][j - 1]` (diagonal) when characters match, rather than taking `1 + '
                   'max(dp[i - 1][j], dp[i][j - 1])`?',
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! When `s1[i-1] == s2[j-1]`, that character extends the LCS of `s1[:i-1]` and '
                                '`s2[:j-1]`. It is mathematically proven that matching them greedily is never '
                                'suboptimal to skipping one.',
                           'B': 'Incorrect: Parity and primality are unrelated.',
                           'C': 'Incorrect: Subsequences can contain duplicates.',
                           'D': 'Incorrect: Python strings are 0-indexed.'},
             'q1_opts': [   {   'id': 'A',
                                'label': 'Matching characters pair exclusively with each other; both prefixes can '
                                         'discard their matched terminal characters simultaneously'},
                            {'id': 'B', 'label': 'Because diagonal numbers are always prime'},
                            {'id': 'C', 'label': 'To prevent duplicate characters'},
                            {'id': 'D', 'label': 'Because strings are 1-indexed'}],
             'q2': 'What real-world tool relies directly on the Longest Common Subsequence algorithm?',
             'q2_ans': 'A',
             'q2_exp': {   'A': 'Correct! `git diff` computes line-by-line differences between file revisions by '
                                'computing the LCS of file lines. Lines in the LCS are unchanged; other lines are '
                                'additions or deletions.',
                           'B': 'Incorrect: Defrag operates on block sectors.',
                           'C': 'Incorrect: DNS is tree/cache routing.',
                           'D': 'Incorrect: Shaders compute vector graphics.'},
             'q2_opts': [   {'id': 'A', 'label': 'The Unix `diff` utility and Git version control diff engines'},
                            {'id': 'B', 'label': 'Disk defragmenters'},
                            {'id': 'C', 'label': 'DNS lookup resolvers'},
                            {'id': 'D', 'label': 'GPU shader pipelines'}],
             'recap': [   {   'concept': 'Diagonal vs Coordinate Decisions',
                              'naiveIntuition': 'Always take the max of adjacent cells',
                              'pythonReality': 'Matching characters allow a diagonal leap (both strings advance); '
                                               'non-matching characters test unilateral advancement'},
                          {   'concept': 'Diff Engine Foundation',
                              'naiveIntuition': 'Comparing files requires AI',
                              'pythonReality': 'LCS provides the exact mathematical foundation for code diffing, DNA '
                                               'genome alignment, and spell checkers'}],
             'sample_code': '# Longest Common Subsequence\n'
                            'def lcs(s1, s2):\n'
                            '    n, m = len(s1), len(s2)\n'
                            '    dp = [[0] * (m + 1) for _ in range(n + 1)]\n'
                            '    for i in range(1, n + 1):\n'
                            '        for j in range(1, m + 1):\n'
                            '            if s1[i - 1] == s2[j - 1]:\n'
                            '                dp[i][j] = 1 + dp[i - 1][j - 1]\n'
                            '            else:\n'
                            '                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])\n'
                            '    return dp[n][m]',
             'solution': 'def longest_common_subsequence(text1: str, text2: str) -> int:\n'
                         '    n, m = len(text1), len(text2)\n'
                         '    dp = [[0] * (m + 1) for _ in range(n + 1)]\n'
                         '    for i in range(1, n + 1):\n'
                         '        for j in range(1, m + 1):\n'
                         '            if text1[i - 1] == text2[j - 1]:\n'
                         '                dp[i][j] = 1 + dp[i - 1][j - 1]\n'
                         '            else:\n'
                         '                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])\n'
                         '    return dp[n][m]\n'
                         '\n'
                         "print('LCS(abcde, ace):', longest_common_subsequence('abcde', 'ace'))\n"
                         "print('LCS(abc, def):', longest_common_subsequence('abc', 'def'))\n",
             'starter': 'def longest_common_subsequence(text1: str, text2: str) -> int:\n'
                        '    # TODO: Implement 2D LCS table\n'
                        '    return 0\n'
                        '\n'
                        "print('LCS(abcde, ace):', longest_common_subsequence('abcde', 'ace')) # 3 ('ace')\n"
                        "print('LCS(abc, def):', longest_common_subsequence('abc', 'def'))     # 0\n",
             'summary': 'Longest Common Subsequence (LCS) finds the longest sequence appearing in relative order '
                        'within two strings using 2D DP table matching in O(N * M) time.',
             'takeaway': 'Character matches advance both pointers diagonally (+1); mismatches take the max of '
                         'horizontal and vertical branches.'},
    153: {   'hint': 'dp = [[0]*(m+1) for _ in range(n+1)]. Init dp[i][0]=i, dp[0][j]=j. Loop i 1..n, j 1..m: if '
                     'word1[i-1]==word2[j-1]: dp[i][j]=dp[i-1][j-1] else: dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], '
                     'dp[i-1][j-1]). Return dp[n][m].',
             'mechanics': 'If `w1[i - 1] == w2[j - 1]`: cost 0 (`dp[i][j] = dp[i - 1][j - 1]`). Else: `1 + min(insert, '
                          'delete, replace)` where Insert is `dp[i][j - 1]`, Delete is `dp[i - 1][j]`, and Replace is '
                          '`dp[i - 1][j - 1]`. Base cases: `dp[i][0] = i` (delete all) and `dp[0][j] = j` (insert '
                          'all).',
             'patterns': ['horse -> ros: 3', 'intention -> execution: 5'],
             'practice_task': 'Calculate the minimum number of edit operations to convert word1 into word2.',
             'q1': 'What operation corresponds to the state transition `dp[i][j - 1]` in Edit Distance?',
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! If we insert `w2[j-1]` into `w1`, that character is now matched. We advance '
                                'index `j`, but index `i` remains waiting to be converted, represented by transition '
                                '`dp[i][j-1]`.',
                           'B': 'Incorrect: Deletion removes `w1[i-1]`, which advances `i` without advancing `j` '
                                '(`dp[i-1][j]`).',
                           'C': 'Incorrect: Replacement consumes both characters (`dp[i-1][j-1]`).',
                           'D': 'Incorrect: Transposition is Damerau-Levenshtein distance.'},
             'q1_opts': [   {   'id': 'A',
                                'label': 'INSERTION: inserting character `w2[j - 1]` into `w1`, satisfying the target '
                                         'character and advancing `j` while leaving `i` unchanged'},
                            {'id': 'B', 'label': 'DELETION: deleting character from `w1`'},
                            {'id': 'C', 'label': 'REPLACEMENT: replacing character'},
                            {'id': 'D', 'label': 'SWAP: transposing adjacent characters'}],
             'q2': 'Why is `dp[i][0]` initialized to `i` in the Edit Distance base case?',
             'q2_ans': 'A',
             'q2_exp': {   'A': 'Correct! If the target string is empty, the only way to convert an i-character string '
                                'into `""` is to delete all `i` characters one by one, requiring `i` operations.',
                           'B': 'Incorrect: Base case reflects operation costs.',
                           'C': 'Incorrect: Empty strings are valid base inputs.',
                           'D': 'Incorrect: The matrix is generally rectangular (n != m).'},
             'q2_opts': [   {   'id': 'A',
                                'label': 'Converting a string of length `i` into an empty string `""` requires exactly '
                                         '`i` deletions'},
                            {'id': 'B', 'label': 'Because 0 is the starting index'},
                            {'id': 'C', 'label': 'Because strings cannot be empty'},
                            {'id': 'D', 'label': 'To satisfy matrix symmetry'}],
             'recap': [   {   'concept': 'Tri-Directional Decision Space',
                              'naiveIntuition': 'Only consider insertions and deletions',
                              'pythonReality': 'Modeling all 3 atomic string edits (insert, delete, replace) covers '
                                               'every possible typographical mutation'},
                          {   'concept': 'Diagonal Cost Neutrality',
                              'naiveIntuition': 'Matching characters cost 1',
                              'pythonReality': 'When characters match, the edit distance cost is 0, cleanly bypassing '
                                               'all three mutation penalties'}],
             'sample_code': '# Edit Distance\n'
                            'def min_distance(w1, w2):\n'
                            '    n, m = len(w1), len(w2)\n'
                            '    dp = [[0] * (m + 1) for _ in range(n + 1)]\n'
                            '    for i in range(n + 1): dp[i][0] = i\n'
                            '    for j in range(m + 1): dp[0][j] = j\n'
                            '    for i in range(1, n + 1):\n'
                            '        for j in range(1, m + 1):\n'
                            '            if w1[i - 1] == w2[j - 1]: dp[i][j] = dp[i - 1][j - 1]\n'
                            '            else: dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])\n'
                            '    return dp[n][m]',
             'solution': 'def edit_distance(word1: str, word2: str) -> int:\n'
                         '    n, m = len(word1), len(word2)\n'
                         '    dp = [[0] * (m + 1) for _ in range(n + 1)]\n'
                         '    for i in range(n + 1):\n'
                         '        dp[i][0] = i\n'
                         '    for j in range(m + 1):\n'
                         '        dp[0][j] = j\n'
                         '    for i in range(1, n + 1):\n'
                         '        for j in range(1, m + 1):\n'
                         '            if word1[i - 1] == word2[j - 1]:\n'
                         '                dp[i][j] = dp[i - 1][j - 1]\n'
                         '            else:\n'
                         '                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])\n'
                         '    return dp[n][m]\n'
                         '\n'
                         "print('horse -> ros:', edit_distance('horse', 'ros'))\n"
                         "print('intention -> execution:', edit_distance('intention', 'execution'))\n",
             'starter': 'def edit_distance(word1: str, word2: str) -> int:\n'
                        '    # TODO: Implement Levenshtein Distance DP table\n'
                        '    return 0\n'
                        '\n'
                        "print('horse -> ros:', edit_distance('horse', 'ros')) # 3 (replace h->r, remove r, remove e)\n"
                        "print('intention -> execution:', edit_distance('intention', 'execution')) # 5\n",
             'summary': 'Edit Distance (Levenshtein Distance) computes the minimum operations (Insert, Delete, '
                        'Replace) required to convert word1 into word2 using a 2D DP matrix in O(N * M) time.',
             'takeaway': 'Edit distance chooses min(insert, delete, replace) at mismatches, with cost 0 on matches.'},
    154: {   'hint': 'n = len(dims) - 1. dp = [[0]*n for _ in range(n)]. Loop L from 2 to n: loop i from 0 to n - L: j '
                     '= i + L - 1; dp[i][j] = inf; loop k from i to j-1: cost = dp[i][k] + dp[k+1][j] + '
                     'dims[i]*dims[k+1]*dims[j+1]; dp[i][j] = min(dp[i][j], cost). Return dp[0][n-1].',
             'mechanics': 'For interval `[i, j]`, iterate over all possible split pivots `k` between `i` and `j`. '
                          'Recurrence: `dp[i][j] = min/max over k of (dp[i][k] + dp[k+1][j] + cost(i, k, j))`. Crucial '
                          'invariant: length `L` must be the outer loop (from 1 to N) so smaller sub-intervals are '
                          'computed before larger intervals reference them.',
             'patterns': ['Min multiplications: 18000'],
             'practice_task': 'Calculate the minimum scalar multiplications needed to multiply a chain of matrices.',
             'q1': 'Why MUST the outermost loop of an Interval DP algorithm iterate over the INTERVAL LENGTH `L` '
                   'rather than the starting index `i`?',
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! In `dp[i][j] = dp[i][k] + dp[k+1][j] + cost`, both `[i, k]` and `[k+1, j]` '
                                'are strictly shorter intervals than `[i, j]`. Iterating by length `L = 2, 3, ... N` '
                                'guarantees all required sub-intervals are already solved.',
                           'B': 'Incorrect: Index loops are standard.',
                           'C': 'Incorrect: All integer lengths are evaluated.',
                           'D': 'Incorrect: Time remains cubic O(N^3).'},
             'q1_opts': [   {   'id': 'A',
                                'label': 'Computing an interval of length `L` requires the optimal results of strictly '
                                         'smaller sub-intervals (`length < L`); iterating by length guarantees '
                                         'topological readiness'},
                            {'id': 'B', 'label': 'Because starting index `i` cannot be looped in Python'},
                            {'id': 'C', 'label': 'Because intervals must be prime lengths'},
                            {'id': 'D', 'label': 'To reduce time complexity from O(N^3) to O(N)'}],
             'q2': 'In the Burst Balloons problem, why do we frame the decision around which balloon is popped LAST in '
                   'interval `[i, j]` rather than first?',
             'q2_ans': 'A',
             'q2_exp': {   'A': 'Correct! Popping first causes remaining balloons to become adjacent across the split, '
                                'creating tangled dependencies. Popping last leaves boundaries fixed, completely '
                                'decoupling the left and right subproblems.',
                           'B': 'Incorrect: Last balloon yields large points.',
                           'C': 'Incorrect: Popping first is just impossible to decompose cleanly.',
                           'D': 'Incorrect: Array order must remain intact.'},
             'q2_opts': [   {   'id': 'A',
                                'label': 'Popping balloon `k` last means balloons `i - 1` and `j + 1` act as fixed '
                                         'boundary anchors, making subproblems `[i, k - 1]` and `[k + 1, j]` '
                                         'completely independent of each other'},
                            {'id': 'B', 'label': 'Because the last balloon yields 0 points'},
                            {'id': 'C', 'label': 'Because popping first crashes recursion'},
                            {'id': 'D', 'label': 'To sort the balloons by size'}],
             'recap': [   {   'concept': 'Length-First Topological Ordering',
                              'naiveIntuition': 'Loop i from 0 to N and j from 0 to N',
                              'pythonReality': 'Standard coordinate loops reference uncalculated states; organizing '
                                               'transitions by interval span L enforces strict dependency ordering'},
                          {   'concept': 'Boundary Decoupling Inversion',
                              'naiveIntuition': 'Pick the first operation to execute',
                              'pythonReality': 'In interval problems with adjacency effects (Burst Balloons, Matrix '
                                               'Chain), picking the LAST operation leaves boundary anchors intact'}],
             'sample_code': '# Matrix Chain Multiplication / Interval DP Template\n'
                            'def matrix_chain_order(dims):\n'
                            '    n = len(dims) - 1 # Number of matrices\n'
                            '    dp = [[0] * n for _ in range(n)]\n'
                            '    for L in range(2, n + 1): # Interval length\n'
                            '        for i in range(n - L + 1):\n'
                            '            j = i + L - 1\n'
                            "            dp[i][j] = float('inf')\n"
                            '            for k in range(i, j):\n'
                            '                cost = dp[i][k] + dp[k + 1][j] + dims[i] * dims[k + 1] * dims[j + 1]\n'
                            '                dp[i][j] = min(dp[i][j], cost)\n'
                            '    return dp[0][n - 1]',
             'solution': 'def min_matrix_mult(dims: list[int]) -> int:\n'
                         '    n = len(dims) - 1\n'
                         '    dp = [[0] * n for _ in range(n)]\n'
                         '    for L in range(2, n + 1):\n'
                         '        for i in range(n - L + 1):\n'
                         '            j = i + L - 1\n'
                         "            dp[i][j] = float('inf')\n"
                         '            for k in range(i, j):\n'
                         '                cost = dp[i][k] + dp[k + 1][j] + dims[i] * dims[k + 1] * dims[j + 1]\n'
                         '                dp[i][j] = min(dp[i][j], cost)\n'
                         '    return dp[0][n - 1]\n'
                         '\n'
                         "print('Min multiplications:', min_matrix_mult([10, 20, 30, 40]))\n",
             'starter': 'def min_matrix_mult(dims: list[int]) -> int:\n'
                        '    # TODO: Implement Matrix Chain Multiplication using Interval DP\n'
                        '    return 0\n'
                        '\n'
                        '# Matrices: 10x20, 20x30, 30x40 -> dims = [10, 20, 30, 40]\n'
                        '# (A1 * A2) * A3 = (10*20*30) + (10*30*40) = 6000 + 12000 = 18000\n'
                        "print('Min multiplications:', min_matrix_mult([10, 20, 30, 40]))\n",
             'summary': 'Interval Dynamic Programming solves optimization problems over continuous sub-ranges [i, j] '
                        'by iterating over interval lengths L from 1 to N and partitioning at pivot k in O(N^3) time.',
             'takeaway': 'Interval DP evaluates sub-ranges by increasing length L so smaller intervals are ready when '
                         'computing [i, j].'},
    155: {   'hint': 'dp = [False] * (len(s) + 1); dp[0] = True. words = set(word_dict). Loop i 1..len(s): loop j '
                     '0..i-1: if dp[j] and s[j:i] in words: dp[i] = True; break. Return dp[len(s)].',
             'mechanics': 'The 4-Step DP Blueprint: (1) State Representation: Define what parameters `(i, j, w)` '
                          'uniquely capture the subproblem state. (2) Recurrence Relation: Formulate decisions (take '
                          'vs skip, match vs mismatch, split at k). (3) Base Cases: Establish ground truth for empty '
                          'inputs. (4) Direction & Optimization: Determine evaluation order and compress dimensions.',
             'patterns': ['leetcode breakable: True', 'catsandog breakable: False'],
             'practice_task': 'Build a Word Break validator using 1D Partition DP.',
             'q1': 'You are given a problem where an array can be split into contiguous subarrays, and you need to '
                   'optimize a metric across all possible partitions. Which DP paradigm applies?',
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! Partitioning a sequence into valid segments (like Word Break, Palindrome '
                                'Partitioning, or Matrix Chain) is the canonical domain of 1D Partition DP and '
                                'Interval DP.',
                           'B': 'Incorrect: Dijkstra computes graph paths.',
                           'C': 'Incorrect: Greedy fails when sub-choices have trade-offs.',
                           'D': 'Incorrect: Partitioning is combinatorial.'},
             'q1_opts': [   {   'id': 'A',
                                'label': '1D Partition DP (`dp[i] = min over j < i of dp[j] + cost(j, i)`) or Interval '
                                         'DP (`dp[i][j] = min over k of dp[i][k] + dp[k+1][j]`)'},
                            {'id': 'B', 'label': "Dijkstra's Algorithm"},
                            {'id': 'C', 'label': 'Greedy Interval Scheduling'},
                            {'id': 'D', 'label': 'Binary Search on Array'}],
             'q2': 'What is the key indicator that a problem CANNOT be solved with Dynamic Programming?',
             'q2_ans': 'A',
             'q2_exp': {   'A': 'Correct! DP requires the state transition graph to be a Directed Acyclic Graph (DAG). '
                                'If cycles exist, no topological evaluation order exists without simultaneous '
                                'equations or shortest-path algorithms.',
                           'B': 'Incorrect: Optimal substructure is required for DP.',
                           'C': 'Incorrect: Overlapping subproblems are the hallmark of DP.',
                           'D': 'Incorrect: DP readily handles negative numbers.'},
             'q2_opts': [   {   'id': 'A',
                                'label': 'Subproblems contain cyclical dependencies (e.g. state A depends on state B, '
                                         'and state B depends on state A)'},
                            {'id': 'B', 'label': 'The problem has optimal substructure'},
                            {'id': 'C', 'label': 'The problem has overlapping subproblems'},
                            {'id': 'D', 'label': 'The numbers in the problem are negative'}],
             'recap': [   {   'concept': 'Partition State Transition',
                              'naiveIntuition': 'Match greedy prefixes',
                              'pythonReality': 'Greedy prefix matching gets stuck on ambiguous word splits; checking '
                                               'all j < i with dp[j] guarantees complete coverage'},
                          {   'concept': 'Section 13 Synthesis',
                              'naiveIntuition': 'DP requires memorizing dozens of unique formulas',
                              'pythonReality': 'All DP problems are topological sweeps over DAGs; once states and '
                                               'choices are identified, the recurrence writes itself'}],
             'sample_code': '# 4-Step DP Blueprint Checklist:\n'
                            '# 1. State: dp[i] or dp[i][j]\n'
                            '# 2. Transition: min/max over available decisions\n'
                            '# 3. Base cases: dp[0] = base\n'
                            '# 4. Space compression: rolling variables or reverse sweeps',
             'solution': 'def word_break(s: str, word_dict: list[str]) -> bool:\n'
                         '    words = set(word_dict)\n'
                         '    dp = [False] * (len(s) + 1)\n'
                         '    dp[0] = True\n'
                         '    for i in range(1, len(s) + 1):\n'
                         '        for j in range(i):\n'
                         '            if dp[j] and s[j:i] in words:\n'
                         '                dp[i] = True\n'
                         '                break\n'
                         '    return dp[len(s)]\n'
                         '\n'
                         "words = ['leet', 'code']\n"
                         "print('leetcode breakable:', word_break('leetcode', words))\n"
                         "print('catsandog breakable:', word_break('catsandog', ['cats', 'dog', 'sand', 'and', "
                         "'cat']))\n",
             'starter': 'def word_break(s: str, word_dict: list[str]) -> bool:\n'
                        '    # TODO: dp[i] is True if s[:i] can be segmented into dictionary words\n'
                        '    return False\n'
                        '\n'
                        "words = ['leet', 'code']\n"
                        "print('leetcode breakable:', word_break('leetcode', words)) # True\n"
                        "print('catsandog breakable:', word_break('catsandog', ['cats', 'dog', 'sand', 'and', 'cat'])) "
                        '# False\n',
             'summary': 'Section 13 Review synthesizes Memoization vs Tabulation, 1D DP, Knapsack variations, LIS '
                        'patience sorting, 2D Grid DP, LCS, Edit Distance, and Interval DP into a 4-Step Dynamic '
                        'Programming State Design Blueprint.',
             'takeaway': 'Dynamic Programming is state-space traversal on DAGs; mastering DP requires identifying '
                         'states and invariant transitions.'}}
