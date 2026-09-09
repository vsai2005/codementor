"""
Section 12: Greedy Algorithms (Days 136 to 145)
"""

SEC12_DAYS = {   136: {   'hint': 'Sort coins descending. For each c: count += rem // c; rem %= c. Return count.',
             'mechanics': 'Unlike Dynamic Programming which considers multiple choices and memoizes subproblems, a '
                          'greedy algorithm commits irreversibly to a single best immediate choice. Correctness must '
                          "be mathematically proven using either the Exchange Argument or the 'Greedy Stays Ahead' "
                          'induction technique.',
             'patterns': ['Coins for 41 cents: 4', 'Coins for 30 cents: 2'],
             'practice_task': 'Calculate minimum coins needed for an amount using standard canonical coins [25, 10, 5, '
                              '1].',
             'q1': 'Why does the greedy coin change algorithm succeed on standard currency [25, 10, 5, 1] but FAIL on '
                   'arbitrary denominations like [4, 3, 1] for amount = 6?',
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! Canonical currencies have the property that larger denominations are '
                                'multiples or combinations that never block better solutions. For [4, 3, 1], the '
                                'greedy choice 4 irreversibly misses the global optimum 3 + 3.',
                           'B': 'Incorrect: Parity does not determine greedy optimality.',
                           'C': 'Incorrect: Number of denominations does not determine greedy properties.',
                           'D': 'Incorrect: Truncation is standard integer arithmetic.'},
             'q1_opts': [   {   'id': 'A',
                                'label': 'Greedy picks 4 first, leaving 2, which requires two 1s (total 3 coins: '
                                         '4+1+1), whereas the optimal global solution is two coins (3+3)'},
                            {'id': 'B', 'label': 'Because 6 is an even number'},
                            {'id': 'C', 'label': 'Because [4, 3, 1] has only 3 coin types'},
                            {'id': 'D', 'label': 'Because Python division truncates towards zero'}],
             'q2': "What is the core idea of the 'Exchange Argument' in proving greedy algorithms?",
             'q2_ans': 'A',
             'q2_exp': {   'A': 'Correct! The exchange argument starts with a hypothetical non-greedy optimal solution '
                                "OPT. Step by step, it swaps choices in OPT with the greedy algorithm's choices, "
                                'showing total cost does not worsen. Thus, greedy is as good as any optimal solution.',
                           'B': 'Incorrect: Virtual memory swap is unrelated.',
                           'C': 'Incorrect: Heap types are implementation details.',
                           'D': 'Incorrect: Proof of correctness is distinct from time complexity.'},
             'q2_opts': [   {   'id': 'A',
                                'label': 'Assume an arbitrary optimal solution exists, and prove that swapping its '
                                         'first difference with the greedy choice results in an equally good or better '
                                         'solution without losing feasibility'},
                            {'id': 'B', 'label': 'Swapping RAM memory with hard disk storage'},
                            {'id': 'C', 'label': 'Exchanging min-heaps for max-heaps'},
                            {'id': 'D', 'label': 'Proving that the algorithm runs in O(N log N)'}],
             'recap': [   {   'concept': 'Greedy Choice Property',
                              'naiveIntuition': 'Greedy algorithms always work because they pick the biggest value',
                              'pythonReality': 'Greedy only produces globally optimal outcomes for problems possessing '
                                               'matroids or the exchange property; general optimization requires DP'},
                          {   'concept': 'Canonical Currency Specificity',
                              'naiveIntuition': 'All coin change problems are greedy',
                              'pythonReality': 'Arbitrary coin systems require 1D Dynamic Programming because greedy '
                                               'choices can lock out superior combinations'}],
             'sample_code': '# Greedy Coin Change (for Canonical Currency Systems like US cents [25, 10, 5, 1])\n'
                            'def min_coins_canonical(coins, amount):\n'
                            '    coins.sort(reverse=True)\n'
                            '    count = 0\n'
                            '    for c in coins:\n'
                            '        count += amount // c\n'
                            '        amount %= c\n'
                            '    return count',
             'solution': 'def min_canonical_coins(coins: list[int], amount: int) -> int:\n'
                         '    coins_sorted = sorted(coins, reverse=True)\n'
                         '    count = 0\n'
                         '    rem = amount\n'
                         '    for c in coins_sorted:\n'
                         '        count += rem // c\n'
                         '        rem %= c\n'
                         '    return count\n'
                         '\n'
                         'coins = [25, 10, 5, 1]\n'
                         "print('Coins for 41 cents:', min_canonical_coins(coins, 41))\n"
                         "print('Coins for 30 cents:', min_canonical_coins(coins, 30))\n",
             'starter': 'def min_canonical_coins(coins: list[int], amount: int) -> int:\n'
                        '    # TODO: Implement greedy coin change for canonical currency\n'
                        '    return 0\n'
                        '\n'
                        'coins = [25, 10, 5, 1]\n'
                        "print('Coins for 41 cents:', min_canonical_coins(coins, 41)) # 4 (25 + 10 + 5 + 1)\n"
                        "print('Coins for 30 cents:', min_canonical_coins(coins, 30)) # 2 (25 + 5)\n",
             'summary': 'Greedy Algorithms make the locally optimal choice at each decision step, arriving at the '
                        'global optimum without backtracking when problems exhibit Optimal Substructure and the Greedy '
                        'Choice Property.',
             'takeaway': 'Greedy algorithms make irreversible local optimal choices; correctness requires formal proof '
                         'via exchange arguments.'},
    137: {   'hint': 'Sort by lambda x: x[1]. Loop s, e: if s >= last_end: count += 1; last_end = e. Return count.',
             'mechanics': 'Sort intervals `(start, end)` by `end` ascending. Select first interval, set `last_end = '
                          'end`. Iterate through remaining intervals: if `start >= last_end`: select interval, update '
                          '`last_end = end`. Proof: finishing earliest leaves the maximum remaining timeline for '
                          'future tasks.',
             'patterns': ['Max activities: 4'],
             'practice_task': 'Find the maximum number of mutually compatible activities that can be scheduled.',
             'q1': 'Why must intervals be sorted by EARLIEST FINISH TIME rather than earliest start time or shortest '
                   'duration?',
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! Counterexample for start time: an activity starting at 0 and running to 100 '
                                'blocks all others. Counterexample for shortest duration: a short activity in the '
                                'middle blocks two activities on either side. Earliest finish time is proven optimal.',
                           'B': 'Incorrect: Python compares any tuple elements.',
                           'C': 'Incorrect: While true, A is the direct causal proof of finish time optimality.',
                           'D': 'Incorrect: Start times are also numbers.'},
             'q1_opts': [   {   'id': 'A',
                                'label': 'Finishing earliest frees the resource as soon as possible, leaving the '
                                         'maximum possible time window available to schedule future activities'},
                            {'id': 'B', 'label': 'Because start times cannot be compared in Python'},
                            {   'id': 'C',
                                'label': 'Because shortest duration activities can conflict with two long activities'},
                            {'id': 'D', 'label': 'Because finish times are always integers'}],
             'q2': "What is the equivalent formulation for 'Minimum Number of Intervals to Remove to make remainder "
                   "Non-overlapping'?",
             'q2_ans': 'A',
             'q2_exp': {   'A': 'Correct! Maximizing the preserved non-overlapping intervals is the exact mathematical '
                                'complement of minimizing the number of removed intervals. Total removals = N - '
                                'max_preserved.',
                           'B': 'Incorrect: Halving is arbitrary.',
                           'C': 'Incorrect: Assumes all intervals overlap.',
                           'D': 'Incorrect: Summing timestamps is meaningless.'},
             'q2_opts': [   {'id': 'A', 'label': '`total_intervals - max_non_overlapping_activities()`'},
                            {'id': 'B', 'label': '`max_non_overlapping_activities() // 2`'},
                            {'id': 'C', 'label': '`len(intervals) - 1`'},
                            {'id': 'D', 'label': 'Sum of all end times'}],
             'recap': [   {   'concept': 'Earliest Deadline Principle',
                              'naiveIntuition': 'Sort intervals by start time',
                              'pythonReality': 'Sorting by start time fails on long tasks that start early; sorting by '
                                               'finish time greedily maximizes future resource availability'},
                          {   'concept': 'Duality of Interval Problems',
                              'naiveIntuition': 'Deletion and selection need different algorithms',
                              'pythonReality': 'Max Non-Overlapping Intervals and Min Interval Removals are exact dual '
                                               'formulations of the same greedy sweep'}],
             'sample_code': '# Interval Scheduling (Max Non-overlapping Activities)\n'
                            'def max_activities(intervals):\n'
                            '    intervals.sort(key=lambda x: x[1]) # Sort by end time\n'
                            '    count = 0\n'
                            "    last_end = float('-inf')\n"
                            '    for s, e in intervals:\n'
                            '        if s >= last_end:\n'
                            '            count += 1\n'
                            '            last_end = e\n'
                            '    return count',
             'solution': 'def max_compatible_intervals(intervals: list[list[int]]) -> int:\n'
                         '    intervals_sorted = sorted(intervals, key=lambda x: x[1])\n'
                         '    count = 0\n'
                         "    last_end = float('-inf')\n"
                         '    for s, e in intervals_sorted:\n'
                         '        if s >= last_end:\n'
                         '            count += 1\n'
                         '            last_end = e\n'
                         '    return count\n'
                         '\n'
                         'acts = [[1, 4], [3, 5], [0, 6], [5, 7], [3, 9], [5, 9], [6, 10], [8, 11], [8, 12], [2, 14], '
                         '[12, 16]]\n'
                         "print('Max activities:', max_compatible_intervals(acts))\n",
             'starter': 'def max_compatible_intervals(intervals: list[list[int]]) -> int:\n'
                        '    # TODO: Sort by finish time and select maximum non-overlapping intervals\n'
                        '    return 0\n'
                        '\n'
                        '# Intervals: [1, 4], [3, 5], [0, 6], [5, 7], [3, 9], [5, 9], [6, 10], [8, 11], [8, 12], [2, '
                        '14], [12, 16]\n'
                        'acts = [[1, 4], [3, 5], [0, 6], [5, 7], [3, 9], [5, 9], [6, 10], [8, 11], [8, 12], [2, 14], '
                        '[12, 16]]\n'
                        "print('Max activities:', max_compatible_intervals(acts)) # 4 ([1, 4], [5, 7], [8, 11], [12, "
                        '16])\n',
             'summary': 'Activity Selection (Interval Scheduling) maximizes the number of non-overlapping intervals by '
                        'greedily sorting intervals by EARLIEST FINISH TIME in O(N log N) time.',
             'takeaway': 'Sorting intervals by earliest finish time leaves the maximal remaining time for future '
                         'intervals.'},
    138: {   'hint': 'items = sorted(zip(values, weights), key=lambda x: x[0]/x[1], reverse=True). If rem >= w: total '
                     '+= v, rem -= w. Else: total += v * (rem / w), break. Return total.',
             'mechanics': 'Compute `ratio = val / weight` for each item. Sort items descending by ratio. For each '
                          'item: if `capacity >= weight`: take all (`val`, subtract `weight`). Else: take fraction '
                          '`capacity / weight * val`, fill knapsack to 0, break. Total time: O(N log N).',
             'patterns': ['Max value: 240.0'],
             'practice_task': 'Calculate the maximum total value obtainable in a Fractional Knapsack.',
             'q1': 'Why does the greedy Value-to-Weight ratio strategy work for Fractional Knapsack but FAIL for 0/1 '
                   'Knapsack?',
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! Consider capacity 50. Item 1: v=60, w=10 (ratio 6). Item 2: v=100, w=20 '
                                '(ratio 5). Item 3: v=120, w=30 (ratio 4). In 0/1, taking item 1 and 2 leaves 20 '
                                'capacity, unable to fit item 3 (total 160). But taking item 2 and 3 yields total 220!',
                           'B': 'Incorrect: Knapsack weights are positive.',
                           'C': 'Incorrect: Python sorts floats accurately.',
                           'D': 'Incorrect: Fractional knapsack is a simple sort.'},
             'q1_opts': [   {   'id': 'A',
                                'label': 'In 0/1 Knapsack, items cannot be broken into fractions; taking the highest '
                                         'ratio item can leave unused capacity that cannot be filled by remaining '
                                         'large items, resulting in suboptimal total value'},
                            {'id': 'B', 'label': 'Because 0/1 Knapsack weights are always negative'},
                            {'id': 'C', 'label': 'Because Python cannot sort floats'},
                            {'id': 'D', 'label': 'Because fractional knapsack uses binary search'}],
             'q2': 'What is the time complexity of the Fractional Knapsack algorithm on N items?',
             'q2_ans': 'A',
             'q2_exp': {   'A': 'Correct! Computing ratios and sorting N items takes O(N log N). The greedy pass '
                                'visits items sequentially until capacity is exhausted (O(N)). Overall: O(N log N).',
                           'B': 'Incorrect: O(N * W) is the pseudo-polynomial DP bound for 0/1 Knapsack.',
                           'C': 'Incorrect: O(2^N) is brute force enumeration.',
                           'D': 'Incorrect: All items must be evaluated.'},
             'q2_opts': [   {'id': 'A', 'label': 'O(N log N) to sort by ratio, followed by O(N) single pass'},
                            {'id': 'B', 'label': 'O(N * W) where W is capacity'},
                            {'id': 'C', 'label': 'O(2^N)'},
                            {'id': 'D', 'label': 'O(1)'}],
             'recap': [   {   'concept': 'Divisibility as Greedy Enabler',
                              'naiveIntuition': '0/1 Knapsack can be solved with heuristics',
                              'pythonReality': 'Fractional flexibility enables continuous greedy optimization; '
                                               'discrete integer constraints introduce NP-hard combinatorial packing'},
                          {   'concept': 'Density Sorting Metric',
                              'naiveIntuition': 'Sort by highest absolute value',
                              'pythonReality': 'Value density (value per unit weight) measures true economic '
                                               'efficiency per unit of constrained capacity'}],
             'sample_code': '# Fractional Knapsack\n'
                            'def fractional_knapsack(items, capacity):\n'
                            '    # items: (value, weight)\n'
                            '    items.sort(key=lambda x: x[0] / x[1], reverse=True)\n'
                            '    total_val = 0.0\n'
                            '    rem = capacity\n'
                            '    for v, w in items:\n'
                            '        if rem >= w:\n'
                            '            total_val += v; rem -= w\n'
                            '        else:\n'
                            '            total_val += v * (rem / w); break\n'
                            '    return total_val',
             'solution': 'def max_fractional_value(values: list[int], weights: list[int], capacity: int) -> float:\n'
                         '    items = sorted(zip(values, weights), key=lambda x: x[0] / x[1], reverse=True)\n'
                         '    total = 0.0\n'
                         '    rem = capacity\n'
                         '    for v, w in items:\n'
                         '        if rem >= w:\n'
                         '            total += v\n'
                         '            rem -= w\n'
                         '        else:\n'
                         '            total += v * (rem / w)\n'
                         '            break\n'
                         '    return total\n'
                         '\n'
                         'vals = [60, 100, 120]\n'
                         'wts = [10, 20, 30]\n'
                         'cap = 50\n'
                         "print('Max value:', max_fractional_value(vals, wts, cap))\n",
             'starter': 'def max_fractional_value(values: list[int], weights: list[int], capacity: int) -> float:\n'
                        '    # TODO: Sort by value/weight ratio and greedily take items\n'
                        '    return 0.0\n'
                        '\n'
                        'vals = [60, 100, 120]\n'
                        'wts = [10, 20, 30]\n'
                        'cap = 50\n'
                        "print('Max value:', max_fractional_value(vals, wts, cap)) # 240.0 (all of 1 & 2, 2/3 of 3)\n",
             'summary': 'Fractional Knapsack greedily takes items with the highest Value-to-Weight ratio (v/w) because '
                        'items can be subdivided, whereas 0/1 Knapsack requires Dynamic Programming because '
                        'indivisible items cause capacity wastage.',
             'takeaway': 'Fractional knapsack solves optimally via value/weight greedy sorting; 0/1 knapsack fails '
                         'greedy and requires DP.'},
    139: {   'hint': 'Count frequencies. Merge lowest two groups in min-heap, incrementing code length by 1 for '
                     'characters in both groups. Return sum(counts[ch] * code_lens[ch]).',
             'mechanics': 'Count character frequencies. Push each character as a leaf node `(freq, char)` into a '
                          'min-heap. Repeatedly pop the two lowest frequency nodes, merge them into an internal parent '
                          'node with `freq = f1 + f2`, and push back into heap. Repeat until one root tree remains. '
                          "Path left is '0', path right is '1'.",
             'patterns': ['Total bits: 23'],
             'practice_task': 'Calculate total encoded bit length of a message using Huffman coding frequencies.',
             'q1': "What does it mean for Huffman Codes to be 'Prefix-Free'?",
             'q1_ans': 'A',
             'q1_exp': {   'A': "Correct! In a prefix-free code, if 'a' is '0' and 'b' is '10', encountering '0' "
                                "immediately and uniquely identifies 'a'. Because every symbol corresponds to a leaf "
                                'in the binary tree, no code can be a prefix of another.',
                           'B': "Incorrect: Codes branch with both '0' and '1'.",
                           'C': 'Incorrect: Fixed-length codes are standard ASCII/Unicode, not variable-length Huffman '
                                'codes.',
                           'D': 'Incorrect: Codes represent any byte symbol.'},
             'q1_opts': [   {   'id': 'A',
                                'label': "No character's binary code is a prefix of any other character's code, "
                                         'allowing continuous stream decoding without delimiter markers'},
                            {'id': 'B', 'label': "All codes start with '0'"},
                            {'id': 'C', 'label': 'All codes have the exact same length (e.g. 8 bits)'},
                            {'id': 'D', 'label': 'The code contains no vowels'}],
             'q2': 'What is the time complexity to build a Huffman Tree for an alphabet of K unique characters using a '
                   'min-heap?',
             'q2_ans': 'A',
             'q2_exp': {   'A': 'Correct! Initially building the heap takes O(K). There are K - 1 merge steps, each '
                                'performing two heappops and one heappush on a heap of size <= K, costing O(log K). '
                                'Total: O(K log K).',
                           'B': 'Incorrect: Min-heap avoids quadratic scans.',
                           'C': 'Incorrect: Tree construction is strictly polynomial.',
                           'D': 'Incorrect: Every character must be merged.'},
             'q2_opts': [   {'id': 'A', 'label': 'O(K log K)'},
                            {'id': 'B', 'label': 'O(K^2)'},
                            {'id': 'C', 'label': 'O(2^K)'},
                            {'id': 'D', 'label': 'O(1)'}],
             'recap': [   {   'concept': 'Frequency Inversion Coding',
                              'naiveIntuition': 'Assign fixed 8-bit bytes to all characters',
                              'pythonReality': "Frequent characters ('e', 'a') receive 1-3 bit codes; rare characters "
                                               "('z', 'q') receive 8+ bit codes, drastically reducing average file "
                                               'size'},
                          {   'concept': 'Leaf Node Uniqueness',
                              'naiveIntuition': 'Prefix codes need end-of-character markers',
                              'pythonReality': 'Placing all characters exclusively at leaf nodes mathematically '
                                               'guarantees prefix-free decodability without delimiters'}],
             'sample_code': '# Huffman Coding Tree Construction\n'
                            'import heapq\n'
                            'def huffman_tree(char_freqs):\n'
                            "    pq = [[freq, [char, '']] for char, freq in char_freqs.items()]\n"
                            '    heapq.heapify(pq)\n'
                            '    while len(pq) > 1:\n'
                            '        lo = heapq.heappop(pq)\n'
                            '        hi = heapq.heappop(pq)\n'
                            "        for pair in lo[1:]: pair[1] = '0' + pair[1]\n"
                            "        for pair in hi[1:]: pair[1] = '1' + pair[1]\n"
                            '        heapq.heappush(pq, [lo[0] + hi[0]] + lo[1:] + hi[1:])\n'
                            '    return sorted(heapq.heappop(pq)[1:], key=lambda p: (len(p[1]), p))\n',
             'solution': 'import heapq\n'
                         'from collections import Counter\n'
                         '\n'
                         'def huffman_encoded_length(text: str) -> int:\n'
                         '    if not text:\n'
                         '        return 0\n'
                         '    counts = Counter(text)\n'
                         '    if len(counts) == 1:\n'
                         '        return len(text)\n'
                         '    # (freq, unique_id, [char_list])\n'
                         '    heap = [[freq, [ch]] for ch, freq in counts.items()]\n'
                         '    heapq.heapify(heap)\n'
                         '    code_lens = {ch: 0 for ch in counts}\n'
                         '    while len(heap) > 1:\n'
                         '        f1, chs1 = heapq.heappop(heap)\n'
                         '        f2, chs2 = heapq.heappop(heap)\n'
                         '        for ch in chs1:\n'
                         '            code_lens[ch] += 1\n'
                         '        for ch in chs2:\n'
                         '            code_lens[ch] += 1\n'
                         '        heapq.heappush(heap, [f1 + f2, chs1 + chs2])\n'
                         '    return sum(counts[ch] * code_lens[ch] for ch in counts)\n'
                         '\n'
                         "msg = 'abracadabra'\n"
                         "print('Total bits:', huffman_encoded_length(msg))\n",
             'starter': 'import heapq\n'
                        'from collections import Counter\n'
                        '\n'
                        'def huffman_encoded_length(text: str) -> int:\n'
                        '    # TODO: Build Huffman tree and return total bits: sum(freq * code_length)\n'
                        '    return 0\n'
                        '\n'
                        "msg = 'abracadabra'\n"
                        "print('Total bits:', huffman_encoded_length(msg))\n",
             'summary': 'Huffman Coding generates optimal prefix-free variable-length binary codes for lossless data '
                        'compression using a Min-Heap to build a binary tree bottom-up.',
             'takeaway': 'More frequent characters receive shorter bit codes, minimizing expected file size without '
                         'prefix ambiguity.'},
    140: {   'hint': 'Track jumps = 0, curr_end = 0, farthest = 0. Loop i in range(len(nums) - 1): farthest = '
                     'max(farthest, i + nums[i]); if i == curr_end: jumps += 1, curr_end = farthest. Return jumps.',
             'mechanics': 'Jump Game I: maintain `max_reach = max(max_reach, i + nums[i])`. If `i > max_reach`: cannot '
                          'advance (return False). Return True if `max_reach >= n - 1`. Jump Game II: maintain '
                          '`curr_end` (boundary of current jump) and `farthest`. When `i == curr_end`: `jumps += 1; '
                          'curr_end = farthest`.',
             'patterns': ['Min jumps [2,3,1,1,4]: 2', 'Min jumps [2,3,0,1,4]: 2'],
             'practice_task': 'Determine minimum jumps required to reach the last index in an array.',
             'q1': 'In Jump Game I, why does `if i > max_reach:` prove that the last index can never be reached?',
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! If the loop index `i` exceeds `max_reach`, no sequence of jumps from index 0 '
                                'to i-1 can ever reach index `i` or beyond. It is impossible to advance further.',
                           'B': 'Incorrect: Jumps are non-negative integers.',
                           'C': 'Incorrect: End of array is n - 1.',
                           'D': 'Incorrect: max_reach is monotonically non-decreasing.'},
             'q1_opts': [   {   'id': 'A',
                                'label': 'Index `i` is beyond the furthest position reachable from any preceding '
                                         'index, meaning the learner has encountered an impassable gap'},
                            {'id': 'B', 'label': 'Because nums[i] is negative'},
                            {'id': 'C', 'label': 'Because i reached the end of the array'},
                            {'id': 'D', 'label': 'Because max_reach was reset to 0'}],
             'q2': 'Why does the loop in Jump Game II iterate up to `len(nums) - 1` rather than `len(nums)`?',
             'q2_ans': 'A',
             'q2_exp': {   'A': 'Correct! If `curr_end` happens to be at `n - 1`, landing on `n - 1` means you have '
                                'already arrived. Checking `i == curr_end` on the final element would incorrectly '
                                'charge for another jump.',
                           'B': 'Incorrect: Indexing is valid up to n - 1.',
                           'C': 'Incorrect: Final element value is arbitrary.',
                           'D': 'Incorrect: Standard range limit logic.'},
             'q2_opts': [   {   'id': 'A',
                                'label': 'Once you reach the final index `n - 1`, no additional jump is required to '
                                         'reach the destination; processing `n - 1` would erroneously trigger `jumps '
                                         '+= 1`'},
                            {'id': 'B', 'label': 'To prevent an IndexError'},
                            {'id': 'C', 'label': 'Because the last index is always 0'},
                            {'id': 'D', 'label': 'Python loops require n - 1'}],
             'recap': [   {   'concept': 'Implicit BFS Levels',
                              'naiveIntuition': 'Use BFS or DP (O(N^2)) to check all landing spots',
                              'pythonReality': 'curr_end marks the boundary of the current BFS level; greedy frontier '
                                               'tracking collapses BFS to O(N) time and O(1) space'},
                          {   'concept': 'Horizon Expansion',
                              'naiveIntuition': 'Pick the jump that has the biggest number',
                              'pythonReality': 'Greedily optimize the reach horizon i + nums[i], not the local jump '
                                               'size nums[i]'}],
             'sample_code': '# Jump Game II (Min Jumps)\n'
                            'def min_jumps(nums):\n'
                            '    jumps = 0\n'
                            '    curr_end = 0\n'
                            '    farthest = 0\n'
                            '    for i in range(len(nums) - 1):\n'
                            '        farthest = max(farthest, i + nums[i])\n'
                            '        if i == curr_end:\n'
                            '            jumps += 1\n'
                            '            curr_end = farthest\n'
                            '    return jumps',
             'solution': 'def jump(nums: list[int]) -> int:\n'
                         '    jumps = 0\n'
                         '    curr_end = 0\n'
                         '    farthest = 0\n'
                         '    for i in range(len(nums) - 1):\n'
                         '        farthest = max(farthest, i + nums[i])\n'
                         '        if i == curr_end:\n'
                         '            jumps += 1\n'
                         '            curr_end = farthest\n'
                         '    return jumps\n'
                         '\n'
                         "print('Min jumps [2,3,1,1,4]:', jump([2, 3, 1, 1, 4]))\n"
                         "print('Min jumps [2,3,0,1,4]:', jump([2, 3, 0, 1, 4]))\n",
             'starter': 'def jump(nums: list[int]) -> int:\n'
                        '    # TODO: Implement Jump Game II in O(N) time and O(1) space\n'
                        '    return 0\n'
                        '\n'
                        "print('Min jumps [2,3,1,1,4]:', jump([2, 3, 1, 1, 4])) # 2 (0 -> 1 -> 4)\n"
                        "print('Min jumps [2,3,0,1,4]:', jump([2, 3, 0, 1, 4])) # 2\n",
             'summary': 'Jump Game I (Reachability) and Jump Game II (Minimum Jumps) greedily track the furthest '
                        'reachable index in linear O(N) time.',
             'takeaway': 'Greedy jump algorithms track the furthest reachable frontier, updating jump counts only when '
                         'crossing previous boundaries.'},
    141: {   'hint': 'last = {ch: i for i, ch in enumerate(s)}. start = end = 0. Loop i, ch: end = max(end, last[ch]); '
                     'if i == end: res.append(end - start + 1); start = i + 1. Return res.',
             'mechanics': 'Pass 1: Record `last_idx = {ch: i for i, ch in enumerate(s)}`. Pass 2: Maintain `start = 0` '
                          'and `end = 0`. For each index `i`: expand partition `end = max(end, last_idx[s[i]])`. When '
                          '`i == end`: the partition is complete! Record `end - start + 1`, reset `start = i + 1`. '
                          'Runs in O(N) time.',
             'patterns': ['Partitions: [9, 7, 8]'],
             'practice_task': 'Partition a string into maximum disjoint segments where letters appear in at most one '
                              'segment.',
             'q1': 'Why is `end = max(end, last[ch])` necessary when scanning characters in Partition Labels?',
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! The problem requires that every character appears in AT MOST ONE partition. '
                                "If character 'b' has its last occurrence at index 15, the partition containing the "
                                "first 'b' must extend at least to index 15.",
                           'B': 'Incorrect: All characters are treated identically.',
                           'C': 'Incorrect: String preserves original sequence order.',
                           'D': 'Incorrect: Indices are within len(s).'},
             'q1_opts': [   {   'id': 'A',
                                'label': 'If a newly encountered character appears later in the string than `end`, the '
                                         "current partition boundary must expand rightward to include that character's "
                                         'final occurrence'},
                            {'id': 'B', 'label': 'To count the number of vowels in the string'},
                            {'id': 'C', 'label': 'To sort the characters alphabetically'},
                            {'id': 'D', 'label': 'To prevent an index out of bounds error'}],
             'q2': 'What is the time complexity of Partition Labels on a string of length N with lowercase English '
                   'alphabet?',
             'q2_ans': 'A',
             'q2_exp': {   'A': 'Correct! Two linear passes over N characters take O(N). The `last` dictionary stores '
                                "at most 26 entries (for 'a' through 'z'), consuming strictly O(1) space.",
                           'B': 'Incorrect: Last occurrence lookup is O(1).',
                           'C': 'Incorrect: No sorting is needed.',
                           'D': 'Incorrect: Pure linear scan.'},
             'q2_opts': [   {   'id': 'A',
                                'label': 'O(N) time and O(1) auxiliary space (since alphabet size is fixed at <= 26)'},
                            {'id': 'B', 'label': 'O(N^2)'},
                            {'id': 'C', 'label': 'O(N log N)'},
                            {'id': 'D', 'label': 'O(2^N)'}],
             'recap': [   {   'concept': 'Dynamic Interval Merging',
                              'naiveIntuition': 'Generate intervals [first, last] for all 26 letters and merge them',
                              'pythonReality': 'Expanding end = max(end, last[ch]) implicitly merges intervals on the '
                                               'fly in a single pass without allocating interval objects'},
                          {   'concept': 'Alphabet Bounded Space',
                              'naiveIntuition': 'Hash map consumes O(N) space',
                              'pythonReality': 'Fixed alphabets (ASCII 26/128/256) bound hash map size to O(1) '
                                               'constant auxiliary space'}],
             'sample_code': '# Partition Labels\n'
                            'def partition_labels(s):\n'
                            '    last = {ch: i for i, ch in enumerate(s)}\n'
                            '    res = []\n'
                            '    start = end = 0\n'
                            '    for i, ch in enumerate(s):\n'
                            '        end = max(end, last[ch])\n'
                            '        if i == end:\n'
                            '            res.append(end - start + 1)\n'
                            '            start = i + 1\n'
                            '    return res',
             'solution': 'def partition_string(s: str) -> list[int]:\n'
                         '    last = {ch: i for i, ch in enumerate(s)}\n'
                         '    res = []\n'
                         '    start = end = 0\n'
                         '    for i, ch in enumerate(s):\n'
                         '        end = max(end, last[ch])\n'
                         '        if i == end:\n'
                         '            res.append(end - start + 1)\n'
                         '            start = i + 1\n'
                         '    return res\n'
                         '\n'
                         "s = 'ababcbacadefegdehijhklij'\n"
                         "print('Partitions:', partition_string(s))\n",
             'starter': 'def partition_string(s: str) -> list[int]:\n'
                        '    # TODO: Return list of segment lengths\n'
                        '    return []\n'
                        '\n'
                        "s = 'ababcbacadefegdehijhklij'\n"
                        "print('Partitions:', partition_string(s)) # [9, 7, 8]\n",
             'summary': 'Partition Labels partitions a string into as many parts as possible such that each letter '
                        'appears in at most one part, greedily expanding partition boundaries to the last occurrence '
                        'of each seen character.',
             'takeaway': 'A partition can only close when the scanning index reaches the maximum last-occurrence of '
                         'all characters seen so far.'},
    142: {   'hint': 'Check if sum(gas) < sum(cost) return -1. Loop i: curr_tank += gas[i] - cost[i]; if curr_tank < '
                     '0: start = i + 1, curr_tank = 0. Return start.',
             'mechanics': 'Rule 1: If `sum(gas) < sum(cost)`, completing a circuit is impossible (return -1). Rule 2: '
                          'If running `curr_tank += gas[i] - cost[i]` drops below 0 when traveling from candidate '
                          '`start` to `i`, NO station between `start` and `i` can be a valid starting point! Reset '
                          '`start = i + 1` and `curr_tank = 0`.',
             'patterns': ['Start index: 3'],
             'practice_task': 'Find the starting gas station index to complete the circular journey.',
             'q1': 'Why is it guaranteed that no station between `start` and `i` could have been a valid starting '
                   'station if `curr_tank` became negative at index `i`?',
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! Starting at `k` (where start < k <= i) deprives the car of whatever positive '
                                'surplus accumulated between `start` and `k`. If you ran dry with bonus gas, you will '
                                'certainly run dry starting from 0.',
                           'B': 'Incorrect: Gas arrays are unsorted.',
                           'C': 'Incorrect: Circular routes wrap around naturally.',
                           'D': 'Incorrect: Costs are strictly positive.'},
             'q1_opts': [   {   'id': 'A',
                                'label': 'Since the journey from `start` entered each intermediate station with '
                                         'non-negative gas surplus, starting from any intermediate station with 0 '
                                         'surplus would run out of gas even earlier at index `i`'},
                            {'id': 'B', 'label': 'Because gas stations are sorted by capacity'},
                            {'id': 'C', 'label': 'Because circular arrays cannot reset'},
                            {'id': 'D', 'label': 'Because cost becomes negative'}],
             'q2': 'Why does `sum(gas) >= sum(cost)` guarantee that the found candidate `start` will successfully '
                   'complete the full circular route without needing a second verification pass?',
             'q2_ans': 'A',
             'q2_exp': {   'A': 'Correct! Net gas = (Surplus from start to N-1) + (Deficit from 0 to start). Since Net '
                                'gas >= 0, Surplus >= |Deficit|. The surplus accumulated on the second leg is '
                                'guaranteed to swallow the deficit of the first leg.',
                           'B': 'Incorrect: Pure mathematical theorem.',
                           'C': 'Incorrect: The loop runs exactly once.',
                           'D': 'Incorrect: Individual stations can have gas < cost.'},
             'q2_opts': [   {   'id': 'A',
                                'label': 'The candidate has already proven it can reach the end of the array (N - 1) '
                                         'with non-negative gas; since total net gas across the entire circle is >= 0, '
                                         'that remaining surplus is mathematically guaranteed to cover the '
                                         'wrapped-around prefix from 0 to start'},
                            {'id': 'B', 'label': 'Because Python verifies it in the background'},
                            {'id': 'C', 'label': 'Because the loop runs twice'},
                            {'id': 'D', 'label': 'Because all elements in gas are greater than cost'}],
             'recap': [   {   'concept': 'Deficit Accumulation Pruning',
                              'naiveIntuition': 'Simulate circular drive from every station O(N^2)',
                              'pythonReality': 'Failing at station i eliminates the entire sub-range [start..i] '
                                               'simultaneously, collapsing search to O(N)'},
                          {   'concept': 'Conservation of Net Flow',
                              'naiveIntuition': 'Check wrap-around with modulo loop',
                              'pythonReality': 'When sum(gas) >= sum(cost), wrap-around feasibility is mathematically '
                                               'guaranteed by global conservation'}],
             'sample_code': '# Gas Station in O(N)\n'
                            'def can_complete_circuit(gas, cost):\n'
                            '    if sum(gas) < sum(cost): return -1\n'
                            '    total_tank = curr_tank = start = 0\n'
                            '    for i in range(len(gas)):\n'
                            '        curr_tank += gas[i] - cost[i]\n'
                            '        if curr_tank < 0:\n'
                            '            start = i + 1\n'
                            '            curr_tank = 0\n'
                            '    return start',
             'solution': 'def can_complete_circuit(gas: list[int], cost: list[int]) -> int:\n'
                         '    if sum(gas) < sum(cost):\n'
                         '        return -1\n'
                         '    start = 0\n'
                         '    curr_tank = 0\n'
                         '    for i in range(len(gas)):\n'
                         '        curr_tank += gas[i] - cost[i]\n'
                         '        if curr_tank < 0:\n'
                         '            start = i + 1\n'
                         '            curr_tank = 0\n'
                         '    return start\n'
                         '\n'
                         'gas = [1, 2, 3, 4, 5]\n'
                         'cost = [3, 4, 5, 1, 2]\n'
                         "print('Start index:', can_complete_circuit(gas, cost))\n",
             'starter': 'def can_complete_circuit(gas: list[int], cost: list[int]) -> int:\n'
                        '    # TODO: Implement single-pass O(N) gas station circuit\n'
                        '    return -1\n'
                        '\n'
                        'gas = [1, 2, 3, 4, 5]\n'
                        'cost = [3, 4, 5, 1, 2]\n'
                        "print('Start index:', can_complete_circuit(gas, cost)) # 3\n",
             'summary': 'Gas Station Circuit determines the unique starting station to complete a circular route by '
                        'tracking running net deficits and resetting starting candidates in a single O(N) pass.',
             'takeaway': 'If sum(gas) >= sum(cost), a solution is guaranteed; the first station after the worst '
                         'running deficit is the answer.'},
    143: {   'hint': 'candies = [1] * n. Forward pass: if ratings[i] > ratings[i-1]: candies[i] = candies[i-1] + 1. '
                     'Backward pass: if ratings[i] > ratings[i+1]: candies[i] = max(candies[i], candies[i+1] + 1). '
                     'Return sum(candies).',
             'mechanics': 'Initialize `candies = [1] * n`. Pass 1 (Left-to-Right): if `ratings[i] > ratings[i - 1]`: '
                          '`candies[i] = candies[i - 1] + 1`. Pass 2 (Right-to-Left): if `ratings[i] > ratings[i + '
                          '1]`: `candies[i] = max(candies[i], candies[i + 1] + 1)`. Total candies is `sum(candies)`.',
             'patterns': ['Candies [1, 0, 2]: 5', 'Candies [1, 2, 2]: 4'],
             'practice_task': 'Calculate the minimum total candies needed to distribute according to ratings.',
             'q1': 'Why is `candies[i] = max(candies[i], candies[i + 1] + 1)` used in the right-to-left pass instead '
                   'of direct assignment?',
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! If a child already received 5 candies in Pass 1 to satisfy their left '
                                'neighbor, assigning `candies[i + 1] + 1` (say, 2) directly would violate the left '
                                'neighbor condition. Taking `max()` guarantees both constraints hold simultaneously.',
                           'B': 'Incorrect: All values are >= 1.',
                           'C': 'Incorrect: Distribution reflects local ratings peaks and valleys.',
                           'D': 'Incorrect: No division is used.'},
             'q1_opts': [   {   'id': 'A',
                                'label': 'To satisfy the right-neighbor condition without destroying the left-neighbor '
                                         'condition already satisfied during Pass 1'},
                            {'id': 'B', 'label': 'Because candies cannot be negative'},
                            {'id': 'C', 'label': 'To sort the candies in ascending order'},
                            {'id': 'D', 'label': 'To prevent dividing by zero'}],
             'q2': 'What is the time and space complexity of the two-pass candy algorithm for N children?',
             'q2_ans': 'A',
             'q2_exp': {   'A': 'Correct! Two sequential linear passes (one forward, one backward) take $2N = O(N)$ '
                                'time. The candies array allocates N integers (O(N) space).',
                           'B': 'Incorrect: No sorting is performed.',
                           'C': 'Incorrect: No nested loops exist.',
                           'D': 'Incorrect: Must inspect all N children.'},
             'q2_opts': [   {'id': 'A', 'label': 'O(N) time and O(N) auxiliary space'},
                            {'id': 'B', 'label': 'O(N log N) time and O(1) space'},
                            {'id': 'C', 'label': 'O(N^2) time and O(N) space'},
                            {'id': 'D', 'label': 'O(1) time and O(1) space'}],
             'recap': [   {   'concept': 'Constraint Decoupling',
                              'naiveIntuition': 'Simultaneously balance left and right neighbors',
                              'pythonReality': 'Simultaneous multi-directional constraints often deadlock; splitting '
                                               'into two unidirectional passes cleanly decouples the logic'},
                          {   'concept': 'Peak Value Resolution',
                              'naiveIntuition': 'Peak elements require complex graphs',
                              'pythonReality': 'Taking max(left_pass, right_pass) at each peak naturally resolves '
                                               'local maxima with minimal candies'}],
             'sample_code': '# Candy Two-Pass Greedy\n'
                            'def candy(ratings):\n'
                            '    n = len(ratings)\n'
                            '    candies = [1] * n\n'
                            '    for i in range(1, n):\n'
                            '        if ratings[i] > ratings[i - 1]: candies[i] = candies[i - 1] + 1\n'
                            '    for i in range(n - 2, -1, -1):\n'
                            '        if ratings[i] > ratings[i + 1]: candies[i] = max(candies[i], candies[i + 1] + 1)\n'
                            '    return sum(candies)',
             'solution': 'def distribute_candy(ratings: list[int]) -> int:\n'
                         '    n = len(ratings)\n'
                         '    candies = [1] * n\n'
                         '    for i in range(1, n):\n'
                         '        if ratings[i] > ratings[i - 1]:\n'
                         '            candies[i] = candies[i - 1] + 1\n'
                         '    for i in range(n - 2, -1, -1):\n'
                         '        if ratings[i] > ratings[i + 1]:\n'
                         '            candies[i] = max(candies[i], candies[i + 1] + 1)\n'
                         '    return sum(candies)\n'
                         '\n'
                         "print('Candies [1, 0, 2]:', distribute_candy([1, 0, 2]))\n"
                         "print('Candies [1, 2, 2]:', distribute_candy([1, 2, 2]))\n",
             'starter': 'def distribute_candy(ratings: list[int]) -> int:\n'
                        '    # TODO: Implement two-pass greedy candy distribution\n'
                        '    return 0\n'
                        '\n'
                        "print('Candies [1, 0, 2]:', distribute_candy([1, 0, 2])) # 5 (2 + 1 + 2)\n"
                        "print('Candies [1, 2, 2]:', distribute_candy([1, 2, 2])) # 4 (1 + 2 + 1)\n",
             'summary': 'Candy Distribution gives each child at least 1 candy while ensuring children with higher '
                        'ratings than their immediate neighbors receive more candies, solved using a Two-Pass Greedy '
                        'Invariant in O(N) time.',
             'takeaway': 'Bidirectional greedy passes decouple left and right neighbor constraints into independent '
                         'linear sweeps.'},
    144: {   'hint': 'Sort jobs by profit descending. max_d = max(j[1]). slots = [-1] * (max_d + 1). Loop j_id, d, p: '
                     'loop t from d down to 1: if slots[t] == -1: slots[t] = j_id, total += p, break. Return total.',
             'mechanics': 'Sort jobs by profit descending. Find maximum deadline D. Initialize timeline slots `slots = '
                          '[False] * (D + 1)`. For each job `(id, deadline, profit)`: scan backwards from `min(D, '
                          'deadline)` down to 1. If an empty slot `t` is found: assign job to slot `t`, mark `slots[t] '
                          '= True`, add profit. Stop when all jobs or slots are exhausted.',
             'patterns': ['Max profit: 60'],
             'practice_task': 'Maximize total profit by scheduling jobs before their deadlines.',
             'q1': 'Why should a job with deadline D be placed in the LATEST possible available slot `t <= D` rather '
                   'than the earliest available slot (like slot 1)?',
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! A job with deadline 5 can run in slot 1, 2, 3, 4, or 5. A job with deadline '
                                '1 can ONLY run in slot 1. Greedily delaying the flexible job preserves slot 1 for the '
                                'rigid job, maximizing total completed jobs.',
                           'B': 'Incorrect: Slot placement cost is constant.',
                           'C': 'Incorrect: Profits are fixed attributes of the jobs.',
                           'D': 'Incorrect: Python lists are 0-indexed.'},
             'q1_opts': [   {   'id': 'A',
                                'label': 'Placing it as late as possible preserves earlier time slots for other jobs '
                                         'that might have tighter, earlier deadlines'},
                            {'id': 'B', 'label': 'Because slot 1 takes longer to compute'},
                            {'id': 'C', 'label': 'Because later slots yield higher profits'},
                            {'id': 'D', 'label': 'Because Python arrays are 1-indexed'}],
             'q2': 'How can slot lookups be accelerated from O(D) backwards scan to near O(1) in large-scale job '
                   'scheduling?',
             'q2_ans': 'A',
             'q2_exp': {   'A': 'Correct! When slot `t` is occupied, `dsu.union(t, t - 1)` connects it to the '
                                'preceding slot. Calling `dsu.find(deadline)` instantly jumps directly to the latest '
                                'open slot in $O(\\alpha(D))$ time without linear scanning.',
                           'B': 'Incorrect: Linked list still takes O(D) to find earlier slots.',
                           'C': 'Incorrect: Profit ordering is mandatory.',
                           'D': 'Incorrect: Algorithmic optimization is independent of hardware speed.'},
             'q2_opts': [   {   'id': 'A',
                                'label': 'By using a Disjoint Set Union (DSU) structure where each slot points to the '
                                         'next available earlier slot via path compression'},
                            {'id': 'B', 'label': 'By using a singly linked list'},
                            {'id': 'C', 'label': 'By sorting jobs alphabetically'},
                            {'id': 'D', 'label': 'By doubling CPU clock frequency'}],
             'recap': [   {   'concept': 'Opportunity Preservation',
                              'naiveIntuition': 'Schedule highest profit jobs at the earliest available time',
                              'pythonReality': 'Delaying execution to the latest feasible deadline preserves earlier '
                                               'slots for tighter upcoming deadlines'},
                          {   'concept': 'DSU Slot Acceleration',
                              'naiveIntuition': 'Finding open time slots requires linear scans',
                              'pythonReality': 'Union-Find path compression transforms linear slot searches into '
                                               'near-instant O(alpha(D)) lookups'}],
             'sample_code': '# Job Sequencing with Deadlines\n'
                            'def job_scheduling(jobs):\n'
                            '    # jobs: (id, deadline, profit)\n'
                            '    jobs.sort(key=lambda x: x[2], reverse=True) # Sort by profit\n'
                            '    max_d = max(job[1] for job in jobs)\n'
                            '    slots = [-1] * (max_d + 1)\n'
                            '    total_profit = 0\n'
                            '    for j_id, d, p in jobs:\n'
                            '        for t in range(d, 0, -1):\n'
                            '            if slots[t] == -1:\n'
                            '                slots[t] = j_id\n'
                            '                total_profit += p\n'
                            '                break\n'
                            '    return total_profit',
             'solution': 'def max_job_profit(jobs: list[list[int]]) -> int:\n'
                         '    if not jobs:\n'
                         '        return 0\n'
                         '    jobs_sorted = sorted(jobs, key=lambda x: x[2], reverse=True)\n'
                         '    max_d = max(j[1] for j in jobs_sorted)\n'
                         '    slots = [-1] * (max_d + 1)\n'
                         '    total = 0\n'
                         '    for j_id, d, p in jobs_sorted:\n'
                         '        for t in range(d, 0, -1):\n'
                         '            if slots[t] == -1:\n'
                         '                slots[t] = j_id\n'
                         '                total += p\n'
                         '                break\n'
                         '    return total\n'
                         '\n'
                         'job_list = [[1, 4, 20], [2, 1, 10], [3, 1, 40], [4, 1, 30]]\n'
                         "print('Max profit:', max_job_profit(job_list))\n",
             'starter': 'def max_job_profit(jobs: list[list[int]]) -> int:\n'
                        '    # TODO: jobs: [id, deadline, profit]. Return maximum total profit\n'
                        '    return 0\n'
                        '\n'
                        '# Jobs: [1, 4, 20], [2, 1, 10], [3, 1, 40], [4, 1, 30]\n'
                        '# Best: Job 3 in slot 1 (40), Job 1 in slot 4 (20) -> total 60\n'
                        'job_list = [[1, 4, 20], [2, 1, 10], [3, 1, 40], [4, 1, 30]]\n'
                        "print('Max profit:', max_job_profit(job_list))\n",
             'summary': 'Task Scheduling with Deadlines and Penalties maximizes profit by sorting jobs by decreasing '
                        'profit and greedily scheduling each job in the latest available time slot before its '
                        'deadline.',
             'takeaway': 'Scheduling high-profit jobs as late as possible before their deadline leaves earlier slots '
                         'open for other constrained jobs.'},
    145: {   'hint': 'Create events with (s, 1) and (e, -1). Sort by (x[0], x[1]). Sweep and track max running sum.',
             'mechanics': 'Greedy Checklist: (1) Does the problem exhibit the Greedy Choice Property (locally optimal '
                          'choices stay optimal globally)? (2) Can an Exchange Argument prove that any optimal '
                          'solution can be transformed into the greedy solution without loss? If NO (e.g. 0/1 '
                          'Knapsack, Coin Change with arbitrary coins, Longest Path), greedy FAILS and Dynamic '
                          'Programming or Backtracking is required.',
             'patterns': ['Min rooms: 2'],
             'practice_task': 'Build a Greedy Meeting Room Optimizer that calculates minimum conference rooms required '
                              'for an event schedule.',
             'q1': 'Which of the following problems can be solved OPTIMALLY using a Greedy Algorithm?',
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! Minimum Spanning Trees satisfy the Matroid property, where greedy edge '
                                'selection (Kruskal/Prim) is mathematically guaranteed to find the true global '
                                'minimum.',
                           'B': 'Incorrect: 0/1 Knapsack requires Dynamic Programming.',
                           'C': 'Incorrect: Longest Simple Path is NP-hard.',
                           'D': 'Incorrect: TSP nearest-neighbor greedy heuristic can be arbitrarily worse than '
                                'optimal.'},
             'q1_opts': [   {'id': 'A', 'label': 'Minimum Spanning Tree in an undirected graph (Kruskal or Prim)'},
                            {'id': 'B', 'label': '0/1 Knapsack Problem with integer weights'},
                            {'id': 'C', 'label': 'Longest Simple Path in a general graph'},
                            {'id': 'D', 'label': 'Travelling Salesperson Problem (TSP)'}],
             'q2': 'Why does the Nearest Neighbor greedy heuristic fail to find the optimal route in the Travelling '
                   'Salesperson Problem (TSP)?',
             'q2_ans': 'A',
             'q2_exp': {   'A': 'Correct! Greedy algorithms cannot anticipate the future consequences of closing off '
                                'options. Picking the closest neighbor early on can force a catastrophic '
                                'cross-continent return flight at the final step.',
                           'B': 'Incorrect: TSP requires visiting all cities and returning to start.',
                           'C': 'Incorrect: Fails even in Euclidean space.',
                           'D': 'Incorrect: TSP graphs are typically complete graphs.'},
             'q2_opts': [   {   'id': 'A',
                                'label': 'Visiting the closest unvisited city at each step can trap the salesman into '
                                         'having no choices left at the end except an exorbitantly expensive final '
                                         'return edge'},
                            {'id': 'B', 'label': 'Because cities cannot be visited in loops'},
                            {'id': 'C', 'label': 'Because distances are non-Euclidean'},
                            {'id': 'D', 'label': 'Because TSP graphs are always bipartite'}],
             'recap': [   {   'concept': 'Greedy Boundary Verification',
                              'naiveIntuition': 'If greedy seems fast, write it immediately',
                              'pythonReality': 'Always test greedy ideas against small counterexamples; if a '
                                               'counterexample exists, immediately pivot to Dynamic Programming'},
                          {   'concept': 'Section 12 Synthesis',
                              'naiveIntuition': 'Greedy is just common sense',
                              'pythonReality': 'Greedy algorithms are rigorous structural optimizations proven by '
                                               'exchange arguments, forming the fastest tier of polynomial '
                                               'algorithms'}],
             'sample_code': '# Greedy vs DP Decision Framework:\n'
                            '# 1. Continuous / Fractional choices -> Greedy (Fractional Knapsack)\n'
                            '# 2. Earliest Deadline / Frontier expansion -> Greedy (Intervals, Jumps)\n'
                            '# 3. Discrete / Overlapping subproblems with trade-offs -> DP (0/1 Knapsack, Coin Change)',
             'solution': 'def min_rooms(intervals: list[list[int]]) -> int:\n'
                         '    events = []\n'
                         '    for s, e in intervals:\n'
                         '        events.append((s, 1))\n'
                         '        events.append((e, -1))\n'
                         '    # If times match, process end (-1) before start (1)\n'
                         '    events.sort(key=lambda x: (x[0], x[1]))\n'
                         '    curr = 0\n'
                         '    peak = 0\n'
                         '    for t, delta in events:\n'
                         '        curr += delta\n'
                         '        if curr > peak:\n'
                         '            peak = curr\n'
                         '    return peak\n'
                         '\n'
                         'meetings = [[0, 30], [5, 10], [15, 20]]\n'
                         "print('Min rooms:', min_rooms(meetings))\n",
             'starter': 'def min_rooms(intervals: list[list[int]]) -> int:\n'
                        '    # TODO: Calculate minimum meeting rooms needed using greedy boundary events\n'
                        '    return 0\n'
                        '\n'
                        'meetings = [[0, 30], [5, 10], [15, 20]]\n'
                        "print('Min rooms:', min_rooms(meetings)) # 2\n",
             'summary': 'Section 12 Review synthesizes Greedy Strategy, Activity Selection, Fractional Knapsack, '
                        'Huffman Coding, Jump Games, Gas Station, Candy, and Deadline Scheduling into an overarching '
                        'framework distinguishing when Greedy succeeds vs when it fails.',
             'takeaway': 'Greedy succeeds when local choices never restrict optimal future paths; otherwise, Dynamic '
                         'Programming is mandatory.'}}
