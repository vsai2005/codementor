"""
Section 10: Heaps & Priority Queues (Days 111 to 120)
"""

SEC10_DAYS = {   111: {   'hint': 'p = (i - 1) // 2 if i > 0 else None. l = 2*i + 1 if 2*i + 1 < n else None. r = 2*i + 2 if 2*i + '
                     '2 < n else None.',
             'mechanics': 'For 0-indexed array: `parent(i) = (i - 1) // 2`, `left(i) = 2 * i + 1`, `right(i) = 2 * i + '
                          '2`. Min-Heap property: `arr[parent] <= arr[child]`. Max-Heap property: `arr[parent] >= '
                          'arr[child]`. Being a complete tree ensures array compact density without empty holes.',
             'patterns': ["Relatives of idx 1 (20): {'val': 20, 'parent': 10, 'left': 40, 'right': 50}"],
             'practice_task': 'Compute the parent, left child, and right child values for a given index in a flat heap '
                              'array.',
             'q1': 'In a 0-indexed flat array representing a binary heap, what is the parent index formula for node '
                   '`i`?',
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! For node 1 (left child of 0): (1 - 1) // 2 = 0. For node 2 (right child of '
                                '0): (2 - 1) // 2 = 0. For node 3 (left child of 1): (3 - 1) // 2 = 1. Integer '
                                'division handles both left and right uniformly.',
                           'B': 'Incorrect: That is for 1-indexed heaps.',
                           'C': 'Incorrect: 2*i computes a child index in 1-indexed trees.',
                           'D': 'Incorrect: Indexing requires division by 2.'},
             'q1_opts': [   {'id': 'A', 'label': '`(i - 1) // 2`'},
                            {'id': 'B', 'label': '`i // 2`'},
                            {'id': 'C', 'label': '`2 * i`'},
                            {'id': 'D', 'label': '`i - 2`'}],
             'q2': "Why does a binary heap require the tree to be a 'Complete Binary Tree'?",
             'q2_ans': 'A',
             'q2_exp': {   'A': 'Correct! A complete binary tree is completely filled on all levels except possibly '
                                'the lowest, which is filled from left to right. This guarantees all N nodes occupy '
                                'indices `0` to `N-1` contiguously.',
                           'B': 'Incorrect: Sorting does not require complete trees.',
                           'C': 'Incorrect: Node values are independent of tree topology.',
                           'D': 'Incorrect: Python lists could store None, but gaps waste memory.'},
             'q2_opts': [   {   'id': 'A',
                                'label': 'To guarantee that the flat array has no gaps or empty elements between index '
                                         '0 and index N - 1'},
                            {'id': 'B', 'label': 'Because incomplete trees cannot be sorted'},
                            {'id': 'C', 'label': 'To prevent node values from being negative'},
                            {'id': 'D', 'label': 'Python arrays reject sparse indices'}],
             'recap': [   {   'concept': 'Pointerless Topology',
                              'naiveIntuition': 'Trees must use left and right pointer objects',
                              'pythonReality': 'Complete binary trees map directly onto contiguous arrays where '
                                               'pointer links are replaced by instant arithmetic'},
                          {   'concept': 'Cache Locality',
                              'naiveIntuition': 'Heap performance is identical to pointer trees',
                              'pythonReality': 'Flat arrays maximize CPU L1/L2 cache hit rates compared to '
                                               'pointer-chasing across fragmented heap memory'}],
             'sample_code': '# 1D Array indexing for Binary Heap\n'
                            '# parent(i) = (i - 1) // 2\n'
                            '# left(i)   = 2 * i + 1\n'
                            '# right(i)  = 2 * i + 2\n'
                            'heap = [10, 20, 30, 40, 50, 60, 70]\n'
                            '# Element 20 is at idx 1: left child is idx 3 (40), right child is idx 4 (50)',
             'solution': 'def get_heap_relatives(arr: list[int], i: int) -> dict[str, int]:\n'
                         '    n = len(arr)\n'
                         '    p_idx = (i - 1) // 2 if i > 0 else None\n'
                         '    l_idx = 2 * i + 1 if 2 * i + 1 < n else None\n'
                         '    r_idx = 2 * i + 2 if 2 * i + 2 < n else None\n'
                         '    return {\n'
                         "        'val': arr[i],\n"
                         "        'parent': arr[p_idx] if p_idx is not None else None,\n"
                         "        'left': arr[l_idx] if l_idx is not None else None,\n"
                         "        'right': arr[r_idx] if r_idx is not None else None,\n"
                         '    }\n'
                         '\n'
                         'heap = [10, 20, 30, 40, 50, 60, 70]\n'
                         "print('Relatives of idx 1 (20):', get_heap_relatives(heap, 1))\n",
             'starter': 'def get_heap_relatives(arr: list[int], i: int) -> dict[str, int]:\n'
                        '    # TODO: Return parent, left child, and right child values (or None if out of bounds)\n'
                        '    return {}\n'
                        '\n'
                        'heap = [10, 20, 30, 40, 50, 60, 70]\n'
                        "print('Relatives of idx 1 (20):', get_heap_relatives(heap, 1))\n",
             'summary': 'Binary Heaps map a complete binary tree into a 1D flat array with zero pointer overhead, '
                        'guaranteeing parent-child relationship indexing via simple arithmetic.',
             'takeaway': 'Flat arrays store complete binary trees with zero pointer overhead using arithmetic index '
                         'formulas.'},
    112: {   'hint': 'Helper sift_down(i): find smallest among i, 2*i+1, 2*i+2. If smallest != i: swap and recurse '
                     'sift_down(smallest). Run sift_down from n//2 - 1 down to 0.',
             'mechanics': 'Sift-Up: swap with parent while `val < parent`, used on `push()`. Sift-Down: swap with '
                          'smallest child while `val > child`, used on `pop()`. Heapify runs Sift-Down from index '
                          '`N//2 - 1` down to 0. Math proof: $\\sum_{h=0}^{\\log N} \\frac{N}{2^{h+1}} O(h) = O(N)$.',
             'patterns': ['Min element at root: 1'],
             'practice_task': 'Implement in-place bottom-up min-heapify on an unsorted array.',
             'q1': 'Why is bottom-up `heapify` O(N) time, whereas inserting N elements one-by-one into an initially '
                   'empty heap is O(N log N)?',
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! Height 0 has N/2 nodes (0 swaps). Height 1 has N/4 nodes (1 swap max). '
                                'Height h has N / 2^(h+1) nodes. Summing $(N / 2^{h+1}) \\times h$ forms a converging '
                                'geometric series equal to $O(N)$. Sequential insertion sifts up N/2 leaves all the '
                                'way to root (N/2 * log N = O(N log N)).',
                           'B': 'Incorrect: Heapify is structural sifting, not binary search.',
                           'C': 'Incorrect: The asymptotic difference is mathematical, not implementation-specific.',
                           'D': 'Incorrect: The mathematical summation of heights proves O(N).'},
             'q1_opts': [   {   'id': 'A',
                                'label': 'In bottom-up heapify, the majority of nodes (N/2 leaves) require 0 swaps, '
                                         'and nodes with larger heights are exponentially fewer, summing to O(N)'},
                            {'id': 'B', 'label': 'Because heapify uses binary search'},
                            {'id': 'C', 'label': 'Because Python optimizes heapify in C'},
                            {'id': 'D', 'label': 'Because N/2 is equal to O(N)'}],
             'q2': 'Why does heapify start iterating backwards from index `N // 2 - 1` rather than index `N - 1`?',
             'q2_ans': 'A',
             'q2_exp': {   'A': 'Correct! Any index >= N // 2 has left child index 2*i + 1 >= N, which is out of '
                                'bounds. Leaves have no children to sift down into, making them valid sub-heaps '
                                'already.',
                           'B': 'Incorrect: Lists can be accessed at any valid index.',
                           'C': 'Incorrect: Indices are contiguous.',
                           'D': 'Incorrect: Leaves are not sorted.'},
             'q2_opts': [   {   'id': 'A',
                                'label': 'Indices from `N // 2` to `N - 1` are leaf nodes with no children, so they '
                                         'already satisfy the heap property trivially'},
                            {'id': 'B', 'label': 'Because Python lists cannot be sliced past halfway'},
                            {'id': 'C', 'label': 'To skip odd numbers'},
                            {'id': 'D', 'label': 'Because the second half is automatically sorted'}],
             'recap': [   {   'concept': 'Convergent Height Summation',
                              'naiveIntuition': 'Heapify takes O(N log N) because heap operations take O(log N)',
                              'pythonReality': 'Only the single root node can travel height log N; 50% of nodes travel '
                                               '0 steps, making the total sum strictly O(N)'},
                          {   'concept': 'In-Place Construction',
                              'naiveIntuition': 'Allocate a new heap array to insert elements',
                              'pythonReality': 'Sifting down in reverse index order reorganizes raw arrays in-place '
                                               'with O(1) auxiliary space'}],
             'sample_code': '# Sift-down operation\n'
                            'def sift_down(arr, n, i):\n'
                            '    smallest = i\n'
                            '    l = 2 * i + 1\n'
                            '    r = 2 * i + 2\n'
                            '    if l < n and arr[l] < arr[smallest]: smallest = l\n'
                            '    if r < n and arr[r] < arr[smallest]: smallest = r\n'
                            '    if smallest != i:\n'
                            '        arr[i], arr[smallest] = arr[smallest], arr[i]\n'
                            '        sift_down(arr, n, smallest)',
             'solution': 'def heapify_min(arr: list[int]) -> None:\n'
                         '    n = len(arr)\n'
                         '    def sift_down(i):\n'
                         '        smallest = i\n'
                         '        l = 2 * i + 1\n'
                         '        r = 2 * i + 2\n'
                         '        if l < n and arr[l] < arr[smallest]:\n'
                         '            smallest = l\n'
                         '        if r < n and arr[r] < arr[smallest]:\n'
                         '            smallest = r\n'
                         '        if smallest != i:\n'
                         '            arr[i], arr[smallest] = arr[smallest], arr[i]\n'
                         '            sift_down(smallest)\n'
                         '    for i in range(n // 2 - 1, -1, -1):\n'
                         '        sift_down(i)\n'
                         '\n'
                         'nums = [9, 4, 7, 1, 6, 2, 5, 3]\n'
                         'heapify_min(nums)\n'
                         "print('Min element at root:', nums[0])\n",
             'starter': 'def heapify_min(arr: list[int]) -> None:\n'
                        '    # TODO: Implement in-place bottom-up heapify in O(N) time\n'
                        '    pass\n'
                        '\n'
                        'nums = [9, 4, 7, 1, 6, 2, 5, 3]\n'
                        'heapify_min(nums)\n'
                        "print('Min element at root:', nums[0])\n",
             'summary': 'Sift-Up and Sift-Down maintain the heap invariant, while Bottom-Up Heapify transforms an '
                        'arbitrary N-element array into a valid heap in linear O(N) time.',
             'takeaway': 'Bottom-up heapify runs in linear O(N) time because most nodes reside near the bottom with '
                         'minimal sift-down distance.'},
    113: {   'hint': 'In add_task: heapq.heappush(self.heap, (priority, self.counter, task)); self.counter += 1. In '
                     'get_next_task: return heapq.heappop(self.heap)[2].',
             'mechanics': '`heapq.heapify(lst)` transforms list in O(N). `heapq.heappush(lst, item)` and '
                          '`heapq.heappop(lst)` run in O(log N). For Max-Heap: push `-x` and pop `-heappop()`. For '
                          'multi-attribute tuples `(priority, tie_breaker, task)`: Python compares items element by '
                          'element from index 0.',
             'patterns': ['Next: critical_patch', 'Next: email_sync'],
             'practice_task': 'Use heapq with a 3-element tuple (priority, count, task) to implement a Priority '
                              'Scheduler.',
             'q1': 'When pushing tuples `(priority, data)` into a `heapq`, what happens if two items have identical '
                   '`priority` and `data` is an unorderable object (like a custom ListNode)?',
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! Python tuple comparison evaluates indices sequentially: `t1[0] < t2[0]`. If '
                                'equal, it evaluates `t1[1] < t2[1]`. If `data` lacks `__lt__`, comparison crashes '
                                'with TypeError.',
                           'B': 'Incorrect: Python comparison is strictly deterministic.',
                           'C': 'Incorrect: In Python 3, arbitrary object comparison via memory address was removed '
                                '(PEP 207).',
                           'D': 'Incorrect: Duplicate priorities trigger tie-breaking.'},
             'q1_opts': [   {   'id': 'A',
                                'label': "Python raises `TypeError: '<' not supported between instances` because it "
                                         'attempts to break the priority tie by comparing the second tuple element'},
                            {'id': 'B', 'label': 'Python picks one at random'},
                            {'id': 'C', 'label': 'Python uses object memory addresses'},
                            {'id': 'D', 'label': 'Python ignores duplicate priorities'}],
             'q2': 'How do you safely prevent tuple comparison crashes when storing unorderable objects in a heap?',
             'q2_ans': 'A',
             'q2_exp': {   'A': 'Correct! Because `count` increments on every insertion, no two tuples ever share the '
                                'same `count`. The tie is broken at index 1 before Python ever reaches the unorderable '
                                '`item` at index 2.',
                           'B': 'Incorrect: String representation can be slow and fail on identical strings.',
                           'C': "Incorrect: Doesn't solve runtime comparison in heapq.",
                           'D': "Incorrect: Negation doesn't prevent ties."},
             'q2_opts': [   {   'id': 'A',
                                'label': 'Insert a unique incrementing integer counter as the second element: '
                                         '`(priority, count, item)`'},
                            {'id': 'B', 'label': 'Convert the custom object to a string'},
                            {'id': 'C', 'label': 'Sort the objects beforehand'},
                            {'id': 'D', 'label': 'Use negative priorities'}],
             'recap': [   {   'concept': 'Tuple Tie-Breaker Idiom',
                              'naiveIntuition': 'Store (priority, task) tuples',
                              'pythonReality': 'Using (priority, count, task) guarantees FIFO stability among equal '
                                               'priorities and prevents comparison TypeErrors'},
                          {   'concept': 'Max-Heap Dual Inversion',
                              'naiveIntuition': 'Python lacks max-heap support',
                              'pythonReality': 'Negating numbers transforms a min-heap into a max-heap in zero extra '
                                               'lines'}],
             'sample_code': 'import heapq\n'
                            '# Min-heap\n'
                            'h = [5, 1, 3]\n'
                            'heapq.heapify(h)\n'
                            "print('Min:', heapq.heappop(h)) # 1\n"
                            '\n'
                            '# Max-heap via negation\n'
                            'max_h = [-5, -1, -3]\n'
                            'heapq.heapify(max_h)\n'
                            "print('Max:', -heapq.heappop(max_h)) # 5",
             'solution': 'import heapq\n'
                         '\n'
                         'class PriorityScheduler:\n'
                         '    def __init__(self):\n'
                         '        self.heap = []\n'
                         '        self.counter = 0\n'
                         '\n'
                         '    def add_task(self, task: str, priority: int) -> None:\n'
                         '        heapq.heappush(self.heap, (priority, self.counter, task))\n'
                         '        self.counter += 1\n'
                         '\n'
                         '    def get_next_task(self) -> str:\n'
                         '        if not self.heap:\n'
                         "            return ''\n"
                         '        p, c, task = heapq.heappop(self.heap)\n'
                         '        return task\n'
                         '\n'
                         'sched = PriorityScheduler()\n'
                         "sched.add_task('backup', 3)\n"
                         "sched.add_task('critical_patch', 1)\n"
                         "sched.add_task('email_sync', 2)\n"
                         "print('Next:', sched.get_next_task())\n"
                         "print('Next:', sched.get_next_task())\n",
             'starter': 'import heapq\n'
                        '\n'
                        'class PriorityScheduler:\n'
                        '    def __init__(self):\n'
                        '        self.heap = []\n'
                        '        self.counter = 0\n'
                        '\n'
                        '    # TODO: Implement add_task(task, priority) and get_next_task() -> str\n'
                        '\n'
                        'sched = PriorityScheduler()\n'
                        "sched.add_task('backup', 3)\n"
                        "sched.add_task('critical_patch', 1)\n"
                        "sched.add_task('email_sync', 2)\n"
                        "print('Next:', sched.get_next_task())\n"
                        "print('Next:', sched.get_next_task())\n",
             'summary': "Python's `heapq` module implements a Min-Heap on standard lists, requiring value negation for "
                        'Max-Heaps and custom `__lt__` wrapper classes for complex tie-breaking.',
             'takeaway': "Python's heapq defaults to min-heaps; negate numbers for max-heaps and use unique "
                         'tie-breaker tokens in tuples.'},
    114: {   'hint': 'Count with Counter. Create buckets array of size len(nums)+1. Place num into buckets[freq]. '
                     'Sweep backwards from end of buckets, appending to res until len(res) == k.',
             'mechanics': 'Step 1: count frequencies with `collections.Counter`. Method A (Heap): maintain size-K '
                          'min-heap of `(freq, num)`. Method B (Bucket Sort): create an array `buckets` where '
                          '`buckets[freq]` holds numbers with that frequency. Iterate backwards from index N to '
                          'collect top K in O(N) time.',
             'patterns': ['Top 2: [1, 2]'],
             'practice_task': 'Find the top K most frequent elements in an array using Bucket Sort.',
             'q1': 'Why is Bucket Sort able to achieve O(N) linear time for Top K Frequent Elements?',
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! No number can appear more than N times. Creating N + 1 buckets allows '
                                'grouping elements by frequency in O(N) time, bypassing the $\\Omega(N \\log N)$ '
                                'comparison sort barrier.',
                           'B': 'Incorrect: Works for any numbers or strings.',
                           'C': 'Incorrect: Dicts preserve insertion order, not frequency order.',
                           'D': 'Incorrect: K can be any integer up to unique element count.'},
             'q1_opts': [   {   'id': 'A',
                                'label': 'Because the maximum possible frequency of any element is strictly bounded by '
                                         'array length N, allowing bucket indices to represent frequencies directly '
                                         'without comparison sorting'},
                            {'id': 'B', 'label': 'Because all elements in the input array are positive'},
                            {'id': 'C', 'label': 'Because Python dictionaries sort keys automatically'},
                            {'id': 'D', 'label': 'Because K is always equal to 1'}],
             'q2': 'When is the Heap approach preferred over the Bucket Sort approach for top frequent items?',
             'q2_ans': 'A',
             'q2_exp': {   'A': 'Correct! In streaming systems where total N is unknown or unbounded, creating an '
                                'array of size N is impossible. A min-heap of size K stores only the active leaders in '
                                'bounded O(K) space.',
                           'B': 'Incorrect: For tiny N, both are trivial.',
                           'C': 'Incorrect: Both handle identical elements easily.',
                           'D': 'Incorrect: Streaming constraints favor heaps.'},
             'q2_opts': [   {   'id': 'A',
                                'label': 'When data arrives as an infinite stream or memory cannot accommodate N '
                                         'buckets'},
                            {'id': 'B', 'label': 'When N is less than 5'},
                            {'id': 'C', 'label': 'When all numbers are identical'},
                            {'id': 'D', 'label': 'Never, bucket sort is always superior'}],
             'recap': [   {   'concept': 'Bounded Domain Exploitation',
                              'naiveIntuition': 'Sort frequency pairs using comparison sort O(U log U)',
                              'pythonReality': 'When the domain of sorting keys (frequencies) is bounded by N, bucket '
                                               'sorting achieves linear O(N) time'},
                          {   'concept': 'Multi-Paradigm Mastery',
                              'naiveIntuition': 'There is only one optimal algorithm per problem',
                              'pythonReality': 'Heap approach optimizes streaming space O(K); Bucket sort optimizes '
                                               'batch execution time O(N)'}],
             'sample_code': '# Top K Frequent via Bucket Sort\n'
                            'from collections import Counter\n'
                            'def top_k_frequent(nums, k):\n'
                            '    counts = Counter(nums)\n'
                            '    buckets = [[] for _ in range(len(nums) + 1)]\n'
                            '    for num, freq in counts.items(): buckets[freq].append(num)\n'
                            '    res = []\n'
                            '    for freq in range(len(buckets) - 1, 0, -1):\n'
                            '        for num in buckets[freq]:\n'
                            '            res.append(num)\n'
                            '            if len(res) == k: return res',
             'solution': 'from collections import Counter\n'
                         '\n'
                         'def top_k_frequent(nums: list[int], k: int) -> list[int]:\n'
                         '    counts = Counter(nums)\n'
                         '    buckets = [[] for _ in range(len(nums) + 1)]\n'
                         '    for num, freq in counts.items():\n'
                         '        buckets[freq].append(num)\n'
                         '    res = []\n'
                         '    for freq in range(len(buckets) - 1, 0, -1):\n'
                         '        for num in buckets[freq]:\n'
                         '            res.append(num)\n'
                         '            if len(res) == k:\n'
                         '                return res\n'
                         '    return res\n'
                         '\n'
                         "print('Top 2:', sorted(top_k_frequent([1, 1, 1, 2, 2, 3], 2)))\n",
             'starter': 'from collections import Counter\n'
                        '\n'
                        'def top_k_frequent(nums: list[int], k: int) -> list[int]:\n'
                        '    # TODO: Implement bucket sort by frequency to return top k frequent elements in O(N)\n'
                        '    return []\n'
                        '\n'
                        "print('Top 2:', sorted(top_k_frequent([1, 1, 1, 2, 2, 3], 2)))\n",
             'summary': 'Top K Frequent Elements combines frequency counting with a min-heap of size K (O(N log K) '
                        'time) or Bucket Sort by frequency (O(N) time).',
             'takeaway': 'Frequencies are bounded by N, enabling O(N) bucket sort as an alternative to heaps.'},
    115: {   'hint': 'Push initial elements: (arr[0], i, 0). While heap: pop val, a_idx, e_idx; append val to res; if '
                     'e_idx + 1 < len(arrays[a_idx]): push next element.',
             'mechanics': 'Initialize a min-heap with the head node of each of the K lists: `(node.val, i, node)`. Pop '
                          'the smallest node, attach it to `curr.next`, and if `node.next` exists, push '
                          '`(node.next.val, i, node.next)` into the heap. Repeat until heap is empty.',
             'patterns': ['Merged: [1, 2, 3, 4, 5, 6, 7, 8, 9]'],
             'practice_task': 'Merge K sorted lists of integers represented as lists into a single sorted list using a '
                              'min-heap.',
             'q1': 'Why is the time complexity of merging K sorted lists with total N nodes O(N log K) rather than O(N '
                   'log N)?',
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! The heap stores at most one node per list (size K). Extracting min and '
                                'inserting successor takes O(log K). Across all N nodes in total, time is $N \\times '
                                'O(\\log K) = O(N \\log K)$.',
                           'B': 'Incorrect: Lists are separate and unmerged.',
                           'C': 'Incorrect: K can be arbitrarily large.',
                           'D': 'Incorrect: Heap maintains dynamic minimum.'},
             'q1_opts': [   {   'id': 'A',
                                'label': 'The heap never contains more than K active elements simultaneously, so each '
                                         'of the N nodes experiences an O(log K) heap operation'},
                            {'id': 'B', 'label': 'Because the linked lists are already merged'},
                            {'id': 'C', 'label': 'Because K is always equal to 2'},
                            {'id': 'D', 'label': 'Because binary search is used to find K'}],
             'q2': 'Why must the tuple pushed to the heap include the list index `i` as `(node.val, i, node)`?',
             'q2_ans': 'A',
             'q2_exp': {   'A': 'Correct! If two nodes have `node1.val == node2.val`, Python falls back to comparing '
                                'the second element. Integer `i` is distinct for each list, breaking the tie cleanly '
                                'before reaching `node`.',
                           'B': 'Incorrect: It serves purely as a tie-breaker.',
                           'C': 'Incorrect: Heapq accepts any comparable objects.',
                           'D': 'Incorrect: List length is not stored.'},
             'q2_opts': [   {   'id': 'A',
                                'label': 'To act as a unique tie-breaker, preventing Python from attempting to compare '
                                         'unorderable `ListNode` objects when two nodes have equal values'},
                            {'id': 'B', 'label': 'To count total nodes'},
                            {'id': 'C', 'label': 'Because heapq requires 3-tuples'},
                            {'id': 'D', 'label': 'To determine which list is longest'}],
             'recap': [   {   'concept': 'K-Way Tournament',
                              'naiveIntuition': 'Compare all K list heads with a linear loop O(K * N)',
                              'pythonReality': 'A min-heap reduces the K-way comparison tournament to logarithmic '
                                               'O(log K) per extracted element'},
                          {   'concept': 'Pointer Frontier',
                              'naiveIntuition': 'Load all N nodes into the heap at once O(N log N)',
                              'pythonReality': 'Only the active frontier (1 node per list) needs to be in the heap at '
                                               'any instant, capping size to K'}],
             'sample_code': '# Merge K Sorted Lists pattern\n'
                            '# heap holds (node.val, list_idx, node)\n'
                            '# pop minimum, advance list_idx pointer, push next node',
             'solution': 'import heapq\n'
                         '\n'
                         'def merge_k_arrays(arrays: list[list[int]]) -> list[int]:\n'
                         '    heap = []\n'
                         '    for i, arr in enumerate(arrays):\n'
                         '        if arr:\n'
                         '            heapq.heappush(heap, (arr[0], i, 0))\n'
                         '    res = []\n'
                         '    while heap:\n'
                         '        val, a_idx, e_idx = heapq.heappop(heap)\n'
                         '        res.append(val)\n'
                         '        if e_idx + 1 < len(arrays[a_idx]):\n'
                         '            next_val = arrays[a_idx][e_idx + 1]\n'
                         '            heapq.heappush(heap, (next_val, a_idx, e_idx + 1))\n'
                         '    return res\n'
                         '\n'
                         'arrs = [[1, 4, 7], [2, 5, 8], [3, 6, 9]]\n'
                         "print('Merged:', merge_k_arrays(arrs))\n",
             'starter': 'import heapq\n'
                        '\n'
                        'def merge_k_arrays(arrays: list[list[int]]) -> list[int]:\n'
                        '    # TODO: Maintain a min-heap of (val, array_idx, elem_idx) to merge in O(N log K)\n'
                        '    return []\n'
                        '\n'
                        'arrs = [[1, 4, 7], [2, 5, 8], [3, 6, 9]]\n'
                        "print('Merged:', merge_k_arrays(arrs))\n",
             'summary': 'Merge K Sorted Lists combines K sorted linked lists into a single sorted list in O(N log K) '
                        'time using a Min-Heap of size K.',
             'takeaway': 'Maintaining K active pointers in a min-heap resolves K-way merging in O(N log K) time.'},
    116: {   'hint': 'Push -num to small. If small root > large root: move to large. Balance lengths so len(small) is '
                     'either len(large) or len(large) + 1. If len(small) > len(large): return -small[0] else '
                     '(-small[0] + large[0]) / 2.',
             'mechanics': 'Divide stream into two halves: `small` (max-heap storing smaller half) and `large` '
                          '(min-heap storing larger half). Invariant 1: all elements in `small` <= all in `large`. '
                          'Invariant 2: sizes balanced so `len(small) == len(large)` (even) or `len(small) == '
                          'len(large) + 1` (odd). Median is `small[0]` or `(small[0] + large[0]) / 2`.',
             'patterns': ['Median (1, 2): 1.5', 'Median (1, 2, 3): 2.0'],
             'practice_task': 'Implement MedianFinder supporting add_num and find_median.',
             'q1': 'Why does the smaller half of numbers require a MAX-heap rather than a min-heap?',
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! The median sits at the boundary between the two halves. The highest value in '
                                'the lower half (`small.root`) and the lowest value in the upper half (`large.root`) '
                                'directly sandwich the median.',
                           'B': 'Incorrect: Python heapq defaults to min-heaps.',
                           'C': 'Incorrect: Heaps do not completely sort their elements.',
                           'D': 'Incorrect: Numbers can be arbitrary.'},
             'q1_opts': [   {   'id': 'A',
                                'label': 'Because the median boundary is the LARGEST element of the smaller half, '
                                         'which resides at the root of a max-heap in O(1)'},
                            {'id': 'B', 'label': 'Because Python heapq only supports max-heaps'},
                            {'id': 'C', 'label': 'To sort the smaller numbers in reverse'},
                            {'id': 'D', 'label': 'Because small numbers are always negative'}],
             'q2': 'What are the time complexities for `addNum()` and `findMedian()` in the two-heap median finder?',
             'q2_ans': 'A',
             'q2_exp': {   'A': 'Correct! Adding a number performs a constant number of heap push and pop operations, '
                                'each taking O(log N). Inspecting the roots to compute the median takes O(1) time.',
                           'B': 'Incorrect: Heaps avoid linear scans.',
                           'C': 'Incorrect: Inserting into a heap requires O(log N) sifting.',
                           'D': 'Incorrect: Two-heap structure eliminates O(N) median scans.'},
             'q2_opts': [   {'id': 'A', 'label': '`addNum` is O(log N), `findMedian` is O(1)'},
                            {'id': 'B', 'label': 'Both are O(N)'},
                            {'id': 'C', 'label': 'Both are O(1)'},
                            {'id': 'D', 'label': '`addNum` is O(1), `findMedian` is O(N)'}],
             'recap': [   {   'concept': 'Opposing Heap Equilibrium',
                              'naiveIntuition': 'Sort the array on every insertion O(N log N)',
                              'pythonReality': 'Maintaining a max-heap and min-heap back-to-back locks the middle '
                                               'elements in place with O(log N) updates'},
                          {   'concept': 'Instant Median Access',
                              'naiveIntuition': 'Finding median requires scanning elements',
                              'pythonReality': 'The roots of the balanced two-heap structure give instant O(1) access '
                                               'to median candidates'}],
             'sample_code': '# Two-Heap Median Finder\n'
                            '# small: max-heap (negated) stores values <= median\n'
                            '# large: min-heap stores values >= median\n'
                            '# Balance: 0 <= len(small) - len(large) <= 1',
             'solution': 'import heapq\n'
                         '\n'
                         'class MedianFinder:\n'
                         '    def __init__(self):\n'
                         '        self.small = [] # max-heap\n'
                         '        self.large = [] # min-heap\n'
                         '\n'
                         '    def add_num(self, num: int) -> None:\n'
                         '        # Push to small first\n'
                         '        heapq.heappush(self.small, -num)\n'
                         '        # Balance order: largest in small must be <= smallest in large\n'
                         '        if self.small and self.large and (-self.small[0] > self.large[0]):\n'
                         '            val = -heapq.heappop(self.small)\n'
                         '            heapq.heappush(self.large, val)\n'
                         '        # Balance sizes: small can have at most 1 more element than large\n'
                         '        if len(self.small) > len(self.large) + 1:\n'
                         '            val = -heapq.heappop(self.small)\n'
                         '            heapq.heappush(self.large, val)\n'
                         '        elif len(self.large) > len(self.small):\n'
                         '            val = heapq.heappop(self.large)\n'
                         '            heapq.heappush(self.small, -val)\n'
                         '\n'
                         '    def find_median(self) -> float:\n'
                         '        if len(self.small) > len(self.large):\n'
                         '            return float(-self.small[0])\n'
                         '        return (-self.small[0] + self.large[0]) / 2.0\n'
                         '\n'
                         'mf = MedianFinder()\n'
                         'mf.add_num(1)\n'
                         'mf.add_num(2)\n'
                         "print('Median (1, 2):', mf.find_median())\n"
                         'mf.add_num(3)\n'
                         "print('Median (1, 2, 3):', mf.find_median())\n",
             'starter': 'import heapq\n'
                        '\n'
                        'class MedianFinder:\n'
                        '    def __init__(self):\n'
                        '        self.small = [] # max-heap (stores -val)\n'
                        '        self.large = [] # min-heap\n'
                        '\n'
                        '    # TODO: Implement add_num(num) and find_median() -> float\n'
                        '\n'
                        'mf = MedianFinder()\n'
                        'mf.add_num(1)\n'
                        'mf.add_num(2)\n'
                        "print('Median (1, 2):', mf.find_median()) # 1.5\n"
                        'mf.add_num(3)\n'
                        "print('Median (1, 2, 3):', mf.find_median()) # 2.0\n",
             'summary': 'Finding Median from Data Stream uses a Two-Heap Architecture: a Max-Heap for the smaller half '
                        'and a Min-Heap for the larger half, delivering O(log N) insertion and O(1) median retrieval.',
             'takeaway': 'Opposing min and max heaps maintain the median split of dynamic data streams in O(1) query '
                         'time.'},
    117: {   'hint': 'Count frequencies and push -cnt to max_heap. q = deque(). time = 0. While max_heap or q: time += '
                     '1. If max_heap: cnt = 1 + heappop; if cnt != 0: q.append((cnt, time + n)). If q and q[0][1] == '
                     'time: heappush(max_heap, q.popleft()[0]). Return time.',
             'mechanics': 'Count task frequencies. Max-heap stores frequencies (greedy: execute most frequent task '
                          'first). A FIFO queue stores `(remaining_freq, ready_time)`. In each unit of time: pop most '
                          'frequent task, decrement frequency. If tasks remain, enqueue with `ready_time = '
                          'current_time + n`. If queue front is ready at `current_time`, re-push to heap.',
             'patterns': ['Total time (n=2): 8'],
             'practice_task': 'Calculate the least number of CPU units required to finish all tasks with cooling '
                              'period n.',
             'q1': 'Why is it mathematically optimal to always execute the task with the highest remaining frequency '
                   'first?',
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! The most frequent task acts as the bottleneck dictating the minimum schedule '
                                'length. Interleaving lower-frequency tasks inside its cooling slots prevents having '
                                'idle time at the end.',
                           'B': 'Incorrect: All tasks take exactly 1 unit of time.',
                           'C': 'Incorrect: Max-heap selection is our deliberate strategy.',
                           'D': 'Incorrect: Memory footprint is tiny.'},
             'q1_opts': [   {   'id': 'A',
                                'label': 'Tasks with higher frequencies require the most future cooling intervals, so '
                                         'scheduling them earliest gives the maximum room to interleave other tasks '
                                         'and avoid CPU idle cycles'},
                            {'id': 'B', 'label': 'Because higher frequency tasks run faster on the CPU'},
                            {'id': 'C', 'label': 'Because Python sorts heap elements automatically'},
                            {'id': 'D', 'label': 'To clear memory fastest'}],
             'q2': 'What happens in a time step if the max-heap is empty but the cooldown queue is not empty?',
             'q2_ans': 'A',
             'q2_exp': {   'A': 'Correct! If no tasks are ready to run and pending tasks are still cooling, the CPU '
                                'has no valid work and must increment clock time while idling.',
                           'B': 'Incorrect: Tasks remain to be executed.',
                           'C': 'Incorrect: Cooldown constraints must be respected.',
                           'D': 'Incorrect: That violates cooling rules.'},
             'q2_opts': [   {   'id': 'A',
                                'label': 'The CPU must execute an IDLE cycle because all remaining tasks are currently '
                                         'cooling down'},
                            {'id': 'B', 'label': 'The scheduler terminates immediately'},
                            {'id': 'C', 'label': 'The cooling constraint is ignored'},
                            {'id': 'D', 'label': 'A task is executed twice'}],
             'recap': [   {   'concept': 'Dual Container Scheduling',
                              'naiveIntuition': 'Simulate cooldowns with an array of timestamps',
                              'pythonReality': 'Pairing a Priority Queue (active ready pool) with a FIFO Queue '
                                               '(cooldown waitlist) models state transitions in O(log K)'},
                          {   'concept': 'Bottleneck Domination',
                              'naiveIntuition': 'All tasks contribute equally to idle time',
                              'pythonReality': 'The maximum frequency task forms the scheduling skeleton; all other '
                                               'tasks fill intermediate slots'}],
             'sample_code': '# Task Scheduler with Cooldown Queue\n'
                            '# heap: max frequencies available to execute\n'
                            '# queue: (freq, available_time) cooling down',
             'solution': 'from collections import Counter, deque\n'
                         'import heapq\n'
                         '\n'
                         'def least_interval(tasks: list[str], n: int) -> int:\n'
                         '    counts = Counter(tasks)\n'
                         '    max_heap = [-cnt for cnt in counts.values()]\n'
                         '    heapq.heapify(max_heap)\n'
                         '    \n'
                         '    q = deque() # (cnt, ready_time)\n'
                         '    time = 0\n'
                         '    while max_heap or q:\n'
                         '        time += 1\n'
                         '        if max_heap:\n'
                         '            cnt = 1 + heapq.heappop(max_heap) # cnt is negative, add 1 towards 0\n'
                         '            if cnt != 0:\n'
                         '                q.append((cnt, time + n))\n'
                         '        if q and q[0][1] == time:\n'
                         '            heapq.heappush(max_heap, q.popleft()[0])\n'
                         '    return time\n'
                         '\n'
                         "print('Total time (n=2):', least_interval(['A', 'A', 'A', 'B', 'B', 'B'], 2))\n",
             'starter': 'from collections import Counter, deque\n'
                        'import heapq\n'
                        '\n'
                        'def least_interval(tasks: list[str], n: int) -> int:\n'
                        '    # TODO: Implement max-heap + cooldown queue scheduler\n'
                        '    return 0\n'
                        '\n'
                        "print('Total time (n=2):', least_interval(['A', 'A', 'A', 'B', 'B', 'B'], 2)) # 8\n",
             'summary': 'Task Scheduler coordinates CPU execution of tasks with cooling periods using a Greedy '
                        'Max-Heap paired with a Cooldown FIFO Queue to minimize idle intervals.',
             'takeaway': 'Greedy execution of the most frequent remaining tasks minimizes mandatory idle cooling '
                         'slots.'},
    118: {   'hint': 'Track self.pos[item] = idx during swaps. In decrease_key(item, new_p): set heap[idx][0] = new_p '
                     'and call _sift_up(idx).',
             'mechanics': 'Standard heaps require O(N) linear scans to find an item before updating its priority. An '
                          'Indexed Priority Queue maintains `pos = {item: index}` tracking where each item sits in the '
                          'flat `heap` array. Whenever items swap during sift-up or sift-down, their positions in '
                          '`pos` are updated simultaneously in O(1). This unlocks O(log N) `change_priority()` '
                          'essential for Dijkstra and A* search.',
             'patterns': ["Next task: (5, 'task_B')", "Next task: (10, 'task_A')"],
             'practice_task': 'Implement an Indexed Priority Queue with O(log N) decrease_key support.',
             'q1': "Why does Python's standard `heapq` module NOT provide a built-in `decrease_key` operation?",
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! Without a reverse lookup dictionary `pos[item] = index`, locating the item '
                                'inside the heap list takes O(N) linear time, destroying logarithmic efficiency. '
                                'Python developers use lazy deletion or indexed priority queues instead.',
                           'B': "Incorrect: decrease_key is the foundational primitive of Dijkstra's algorithm.",
                           'C': 'Incorrect: Python list element swapping is O(1).',
                           'D': 'Incorrect: Python lists are mutable.'},
             'q1_opts': [   {   'id': 'A',
                                'label': 'Standard heapq operates on plain Python lists without maintaining a '
                                         'secondary hash table of item-to-index positions; finding an element requires '
                                         'an O(N) scan'},
                            {'id': 'B', 'label': 'Because priorities cannot decrease in computer science'},
                            {'id': 'C', 'label': 'Because Python lists cannot swap elements'},
                            {'id': 'D', 'label': 'Because heaps are strictly immutable in Python'}],
             'q2': 'What is the time complexity of `decrease_key` in an Indexed Priority Queue with N elements?',
             'q2_ans': 'A',
             'q2_exp': {   'A': 'Correct! The hash map gives the heap index in O(1) time. Updating the value and '
                                'bubbling up towards the root takes O(log N) swaps.',
                           'B': 'Incorrect: O(N) is the cost in unindexed heaps.',
                           'C': 'Incorrect: Re-heapifying the entire array takes O(N), but sift-up is O(log N).',
                           'D': 'Incorrect: Fibonacci heaps achieve amortized O(1) decrease-key, but standard binary '
                                'IPQs are O(log N).'},
             'q2_opts': [   {   'id': 'A',
                                'label': 'O(log N) time, because pos[item] locates the index in O(1) and sift-up '
                                         'travels at most the tree height H = log2 N'},
                            {'id': 'B', 'label': 'O(N) time'},
                            {'id': 'C', 'label': 'O(N log N) time'},
                            {'id': 'D', 'label': 'O(1) time'}],
             'recap': [   {   'concept': 'Inverted Heap Indexing',
                              'naiveIntuition': 'Heaps only support accessing the root element',
                              'pythonReality': 'Maintaining a parallel dictionary of item-to-index pointers unlocks '
                                               'O(log N) updates to arbitrary elements in the heap'},
                          {   'concept': 'Heap Mutation Parity',
                              'naiveIntuition': 'Re-sorting the array on priority updates is fine',
                              'pythonReality': 'Full re-heapify takes O(N); single-element sift-up takes O(log N), '
                                               'making shortest path graph algorithms viable at production scale'}],
             'sample_code': '# Indexed Priority Queue Skeleton\n'
                            'class IndexedPQ:\n'
                            '    def __init__(self):\n'
                            '        self.heap = []       # [(priority, item)]\n'
                            '        self.pos = {}        # {item: heap_index}\n'
                            '    def swap(self, i, j):\n'
                            '        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]\n'
                            '        self.pos[self.heap[i][1]] = i\n'
                            '        self.pos[self.heap[j][1]] = j\n'
                            '    def decrease_key(self, item, new_p):\n'
                            '        idx = self.pos[item]\n'
                            '        self.heap[idx] = (new_p, item)\n'
                            '        # sift-up from idx in O(log N)\n'
                            '        while idx > 0:\n'
                            '            p = (idx - 1) // 2\n'
                            '            if self.heap[idx][0] < self.heap[p][0]:\n'
                            '                self.swap(idx, p); idx = p\n'
                            '            else: break',
             'solution': 'class IndexedMinPQ:\n'
                         '    def __init__(self):\n'
                         '        self.heap = []\n'
                         '        self.pos = {}\n'
                         '\n'
                         '    def _swap(self, i: int, j: int) -> None:\n'
                         '        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]\n'
                         '        self.pos[self.heap[i][1]] = i\n'
                         '        self.pos[self.heap[j][1]] = j\n'
                         '\n'
                         '    def push(self, item: str, priority: int) -> None:\n'
                         '        idx = len(self.heap)\n'
                         '        self.heap.append([priority, item])\n'
                         '        self.pos[item] = idx\n'
                         '        self._sift_up(idx)\n'
                         '\n'
                         '    def _sift_up(self, idx: int) -> None:\n'
                         '        while idx > 0:\n'
                         '            parent = (idx - 1) // 2\n'
                         '            if self.heap[idx][0] < self.heap[parent][0]:\n'
                         '                self._swap(idx, parent)\n'
                         '                idx = parent\n'
                         '            else:\n'
                         '                break\n'
                         '\n'
                         '    def decrease_key(self, item: str, new_priority: int) -> None:\n'
                         '        if item in self.pos:\n'
                         '            idx = self.pos[item]\n'
                         '            if new_priority < self.heap[idx][0]:\n'
                         '                self.heap[idx][0] = new_priority\n'
                         '                self._sift_up(idx)\n'
                         '\n'
                         '    def pop_min(self) -> tuple[int, str]:\n'
                         '        min_entry = self.heap[0]\n'
                         '        last_entry = self.heap.pop()\n'
                         '        del self.pos[min_entry[1]]\n'
                         '        if self.heap:\n'
                         '            self.heap[0] = last_entry\n'
                         '            self.pos[last_entry[1]] = 0\n'
                         '            self._sift_down(0)\n'
                         '        return tuple(min_entry)\n'
                         '\n'
                         '    def _sift_down(self, idx: int) -> None:\n'
                         '        n = len(self.heap)\n'
                         '        while 2 * idx + 1 < n:\n'
                         '            smallest = idx\n'
                         '            left = 2 * idx + 1\n'
                         '            right = 2 * idx + 2\n'
                         '            if left < n and self.heap[left][0] < self.heap[smallest][0]:\n'
                         '                smallest = left\n'
                         '            if right < n and self.heap[right][0] < self.heap[smallest][0]:\n'
                         '                smallest = right\n'
                         '            if smallest != idx:\n'
                         '                self._swap(idx, smallest)\n'
                         '                idx = smallest\n'
                         '            else:\n'
                         '                break\n'
                         '\n'
                         'pq = IndexedMinPQ()\n'
                         "pq.push('task_A', 10)\n"
                         "pq.push('task_B', 20)\n"
                         "pq.decrease_key('task_B', 5) # task_B promoted to priority 5!\n"
                         "print('Next task:', pq.pop_min()) # (5, 'task_B')\n"
                         "print('Next task:', pq.pop_min()) # (10, 'task_A')\n",
             'starter': 'class IndexedMinPQ:\n'
                        '    def __init__(self):\n'
                        '        self.heap = []  # list of [priority, item]\n'
                        '        self.pos = {}   # item -> index in heap\n'
                        '\n'
                        '    # TODO: Implement push, pop_min, and decrease_key(item, new_priority)\n'
                        '\n'
                        'pq = IndexedMinPQ()\n'
                        '# Test usage\n',
             'summary': 'Indexed Priority Queues associate an inverted index map (key to heap-array position) with a '
                        'binary heap, enabling O(log N) decrease_key priority updates and arbitrary key removals.',
             'takeaway': 'Maintaining a reverse index map pos[item] = heap_idx enables O(log N) decrease_key priority '
                         'updates.'},
    119: {   'hint': 'Initialize heap with [(matrix[r][0], r, 0) for r in range(min(k, len(matrix)))]. Loop k times: '
                     'pop val, r, c; if c + 1 < n: push (matrix[r][c+1], r, c+1). Return val.',
             'mechanics': 'Initialize min-heap with the first element of each of the first min(K, N) rows: '
                          '`(matrix[r][0], r, 0)`. Pop the minimum element K times. When popping `(val, r, c)`, push '
                          'the immediate right neighbor `(matrix[r][c + 1], r, c + 1)` if within bounds. The K-th '
                          'popped element is the answer.',
             'patterns': ['8th smallest: 13'],
             'practice_task': 'Find the Kth smallest element in a row- and column-sorted matrix using a min-heap.',
             'q1': 'Why is it sufficient to initialize the min-heap with only the first element of each row '
                   '`(matrix[r][0], r, 0)`?',
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! Since every row is sorted from left to right, no element `matrix[r][c]` '
                                '(with c > 0) can be smaller than `matrix[r][0]`. The row heads form the complete '
                                'initial candidate frontier.',
                           'B': 'Incorrect: Matrix can have arbitrary dimensions N x N.',
                           'C': 'Incorrect: Diagonals are not necessarily contiguous.',
                           'D': 'Incorrect: Elements can be strictly distinct.'},
             'q1_opts': [   {   'id': 'A',
                                'label': 'Because each row is sorted, `matrix[r][0]` is the smallest element in its '
                                         'row, guaranteeing that the global minimum must be among row heads'},
                            {'id': 'B', 'label': 'Because matrix rows cannot exceed length 3'},
                            {'id': 'C', 'label': 'Because the matrix diagonal is sorted'},
                            {'id': 'D', 'label': 'Because all row elements are identical'}],
             'q2': 'What is the maximum number of elements present in the heap at any given moment during the '
                   'algorithm?',
             'q2_ans': 'A',
             'q2_exp': {   'A': 'Correct! Each row contributes at most one active candidate pointer at a time. The '
                                'heap size never exceeds the row count (or K if K < N), keeping space complexity to '
                                'O(min(K, N)).',
                           'B': 'Incorrect: Full matrix is never dumped into the heap.',
                           'C': 'Incorrect: Heap maintains a multi-row frontier.',
                           'D': 'Incorrect: Matrix expansion is polynomial.'},
             'q2_opts': [   {'id': 'A', 'label': '`min(K, N)` elements'},
                            {'id': 'B', 'label': '`N * N` elements'},
                            {'id': 'C', 'label': '1 element'},
                            {'id': 'D', 'label': '2^N elements'}],
             'recap': [   {   'concept': '2D Matrix as K Sorted Sequences',
                              'naiveIntuition': 'Flatten and sort the entire N^2 matrix in O(N^2 log N)',
                              'pythonReality': 'Viewing matrix rows as sorted lists reduces the search to a K-way '
                                               'merge in O(K log N) time and O(N) space'},
                          {   'concept': 'Frontier Advancing',
                              'naiveIntuition': 'Explore both down and right neighbors causing duplicate entries',
                              'pythonReality': 'Seeding all row heads and advancing strictly rightward guarantees '
                                               'every matrix cell is visited at most once with zero duplicates'}],
             'sample_code': '# Kth Smallest in Sorted Matrix\n'
                            'import heapq\n'
                            'def kth_smallest_matrix(matrix, k):\n'
                            '    n = len(matrix)\n'
                            '    h = [(matrix[r][0], r, 0) for r in range(min(k, n))]\n'
                            '    heapq.heapify(h)\n'
                            '    for _ in range(k):\n'
                            '        val, r, c = heapq.heappop(h)\n'
                            '        if c + 1 < n: heapq.heappush(h, (matrix[r][c + 1], r, c + 1))\n'
                            '    return val',
             'solution': 'import heapq\n'
                         '\n'
                         'def kth_smallest_matrix(matrix: list[list[int]], k: int) -> int:\n'
                         '    n = len(matrix)\n'
                         '    heap = [(matrix[r][0], r, 0) for r in range(min(k, n))]\n'
                         '    heapq.heapify(heap)\n'
                         '    val = -1\n'
                         '    for _ in range(k):\n'
                         '        val, r, c = heapq.heappop(heap)\n'
                         '        if c + 1 < n:\n'
                         '            heapq.heappush(heap, (matrix[r][c + 1], r, c + 1))\n'
                         '    return val\n'
                         '\n'
                         'mat = [\n'
                         '  [1,  5,  9],\n'
                         '  [10, 11, 13],\n'
                         '  [12, 13, 15]\n'
                         ']\n'
                         "print('8th smallest:', kth_smallest_matrix(mat, 8))\n",
             'starter': 'import heapq\n'
                        '\n'
                        'def kth_smallest_matrix(matrix: list[list[int]], k: int) -> int:\n'
                        '    # TODO: Maintain min-heap of row heads and advance horizontally\n'
                        '    return -1\n'
                        '\n'
                        'mat = [\n'
                        '  [1,  5,  9],\n'
                        '  [10, 11, 13],\n'
                        '  [12, 13, 15]\n'
                        ']\n'
                        "print('8th smallest:', kth_smallest_matrix(mat, 8)) # 13\n",
             'summary': 'Kth Smallest Element in a Sorted Matrix explores a 2D matrix where rows and columns are '
                        'sorted, expanding frontier elements with a Min-Heap in O(K log(min(K, N))) time.',
             'takeaway': 'Row/column sorted matrices behave as K sorted linked lists, explored via min-heap '
                         'frontiers.'},
    120: {   'hint': 'Push (-dist_sq, x, y) into heap. If len(heap) > k: heapq.heappop(heap). Return [[x, y] for _, x, '
                     'y in heap].',
             'mechanics': 'Heap Problem Taxonomy: (1) Dynamic extremum lookup / priority queue? Min-Heap / Max-Heap. '
                          '(2) Top-K elements in stream? Min-heap of size K. (3) Continuous median tracking? Balanced '
                          'two-heap (max-heap small, min-heap large). (4) K-way merging? Frontier heap of size K.',
             'patterns': ['2 Closest: [[-2, 2], [0, 1]]'],
             'practice_task': 'Build a K-Nearest Points to Origin selector using a Max-Heap of size K.',
             'q1': 'Which data structure combination is optimal for calculating the running 95th percentile latency of '
                   'a live web service processing millions of requests per second?',
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! Just like running median (50th percentile) uses 50/50 two-heap balance, any '
                                'arbitrary P-th percentile is maintained by rebalancing two heaps to an exact P / (100 '
                                '- P) size ratio in O(log N) time.',
                           'B': 'Incorrect: Sorting millions of elements on every request crashes latency.',
                           'C': 'Incorrect: Linked list has O(N) insertion.',
                           'D': 'Incorrect: Stacks cannot maintain percentile ordering.'},
             'q1_opts': [   {   'id': 'A',
                                'label': 'Two Heaps (a Max-Heap holding the bottom 95% and a Min-Heap holding the top '
                                         '5%), balanced dynamically'},
                            {'id': 'B', 'label': 'Sorting the array on every incoming HTTP request in O(N log N)'},
                            {'id': 'C', 'label': 'A single singly linked list'},
                            {'id': 'D', 'label': 'A LIFO stack'}],
             'q2': 'What is the time complexity of building a heap from N elements via `heapq.heapify` versus pushing '
                   'elements one by one?',
             'q2_ans': 'A',
             'q2_exp': {   'A': 'Correct! Heapify exploits bottom-up sift-down where the vast majority of nodes reside '
                                'near leaf levels, mathematically bounding the summation of heights to O(N).',
                           'B': 'Incorrect: Heapify is strictly faster than repeated pushes.',
                           'C': 'Incorrect: Repeated push is bounded by N log N.',
                           'D': 'Incorrect: Heapify is never quadratic.'},
             'q2_opts': [   {'id': 'A', 'label': '`heapify` is O(N) linear time, while repeated pushing is O(N log N)'},
                            {'id': 'B', 'label': 'Both are O(N log N)'},
                            {'id': 'C', 'label': 'Both are O(N)'},
                            {'id': 'D', 'label': '`heapify` is O(N^2)'}],
             'recap': [   {   'concept': 'Distance Inversion',
                              'naiveIntuition': 'Sort all points by distance O(N log N)',
                              'pythonReality': 'A max-heap of size K evicts the furthest points, maintaining the K '
                                               'closest in O(N log K) time and O(K) space'},
                          {   'concept': 'Section 10 Synthesis',
                              'naiveIntuition': 'Priority queues are only used for basic sorting',
                              'pythonReality': "Heaps form the algorithmic engine behind Dijkstra's shortest path, "
                                               "Prim's MST, A* pathfinding, Huffman coding, and OS process "
                                               'schedulers'}],
             'sample_code': '# Heap Architecture Selection:\n'
                            '# Top-K Largest -> Min-Heap size K (O(N log K))\n'
                            '# Top-K Smallest -> Max-Heap size K (O(N log K))\n'
                            '# Continuous Median -> Dual Heap Balance (O(log N) insert, O(1) query)\n'
                            '# Merge K Sorted -> Frontier Min-Heap size K (O(N log K))',
             'solution': 'import heapq\n'
                         '\n'
                         'def k_closest(points: list[list[int]], k: int) -> list[list[int]]:\n'
                         '    heap = [] # max-heap stores (-dist_sq, x, y)\n'
                         '    for x, y in points:\n'
                         '        dist_sq = x * x + y * y\n'
                         '        heapq.heappush(heap, (-dist_sq, x, y))\n'
                         '        if len(heap) > k:\n'
                         '            heapq.heappop(heap)\n'
                         '    return [[x, y] for _, x, y in heap]\n'
                         '\n'
                         'pts = [[1, 3], [-2, 2], [5, 8], [0, 1]]\n'
                         "print('2 Closest:', sorted(k_closest(pts, 2)))\n",
             'starter': 'import heapq\n'
                        '\n'
                        'def k_closest(points: list[list[int]], k: int) -> list[list[int]]:\n'
                        '    # TODO: Maintain max-heap of size K based on Euclidean distance squared (x^2 + y^2)\n'
                        '    return []\n'
                        '\n'
                        'pts = [[1, 3], [-2, 2], [5, 8], [0, 1]]\n'
                        "print('2 Closest:', k_closest(pts, 2))\n",
             'summary': 'Section 10 Review synthesizes flat array binary heaps, linear heapify, heapq comparator '
                        'patterns, top-K selection, and multi-heap architectures.',
             'takeaway': 'Heaps provide logarithmic priority ordering, transforming sorting bottlenecks into streaming '
                         'real-time pipelines.'}}
