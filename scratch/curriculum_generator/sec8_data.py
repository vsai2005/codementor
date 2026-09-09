"""
Section 8: Stacks & Queues (Days 86 to 95)
"""

SEC8_DAYS = {   86: {   'hint': 'Use append() for push, _data.pop() for pop, _data[-1] for peek, and len(_data) == 0 for is_empty.',
            'mechanics': 'A stack restricts access strictly to the topmost element. In Python, dynamic lists act as '
                         'stacks via `append()` and `pop()`, running in amortized O(1) time at the contiguous tail. '
                         'Alternatively, a singly linked list can back a stack by inserting and removing at head in '
                         'strict O(1) worst-case time.',
            'patterns': ['Peek: 20', 'Popped: 20', 'Is empty: False'],
            'practice_task': 'Implement a Stack class with push, pop, peek, and is_empty methods.',
            'q1': 'Why is `list.pop()` in Python O(1) amortized, but `list.pop(0)` is O(N)?',
            'q1_ans': 'A',
            'q1_exp': {   'A': 'Correct! Python lists are contiguous pointer arrays. Removing from index 0 leaves an '
                               'empty slot at the beginning, forcing CPython to memmove all remaining N - 1 pointers '
                               'left by 1 position (O(N)). Removing from the end just decrements the size counter '
                               '(O(1)).',
                          'B': 'Incorrect: Python lists are contiguous arrays, not linked lists.',
                          'C': 'Incorrect: All list indices are mutable.',
                          'D': 'Incorrect: Pop operates by index offset, not search.'},
            'q1_opts': [   {   'id': 'A',
                               'label': '`list.pop()` removes the final element without moving others, whereas '
                                        '`list.pop(0)` requires shifting all N - 1 remaining elements to the left in '
                                        'memory'},
                           {'id': 'B', 'label': 'Because Python lists are doubly linked lists under the hood'},
                           {'id': 'C', 'label': 'Because index 0 is immutable in Python'},
                           {'id': 'D', 'label': 'Because pop() uses binary search'}],
            'q2': 'What exception is raised when calling `pop()` on an empty Python list?',
            'q2_ans': 'A',
            'q2_exp': {   'A': 'Correct! In Python, calling pop() on an empty sequence raises an `IndexError`. Always '
                               'verify `if stack:` before popping.',
                          'B': 'Incorrect: KeyError applies to mappings.',
                          'C': 'Incorrect: ValueError indicates an invalid value argument.',
                          'D': 'Incorrect: Python throws an exception rather than returning None.'},
            'q2_opts': [   {'id': 'A', 'label': 'IndexError: pop from empty list'},
                           {'id': 'B', 'label': 'KeyError'},
                           {'id': 'C', 'label': 'ValueError'},
                           {'id': 'D', 'label': 'None is returned'}],
            'recap': [   {   'concept': 'LIFO Boundary Protection',
                             'naiveIntuition': 'Allow arbitrary index access on stacks',
                             'pythonReality': 'Restricting access strictly to the top element prevents subtle state '
                                              'bugs and preserves algorithmic invariants'},
                         {   'concept': 'Contiguous Tail Amortization',
                             'naiveIntuition': 'Dynamic arrays reallocate on every push',
                             'pythonReality': "CPython's geometric over-allocation ensures append() and pop() cost "
                                              'O(1) amortized time'}],
            'sample_code': '# Stack using Python list\n'
                           'stack = []\n'
                           'stack.append(10) # Push\n'
                           'stack.append(20)\n'
                           'top = stack[-1]  # Peek (20)\n'
                           'popped = stack.pop() # Pop (20)\n'
                           "print('Stack:', stack, 'Popped:', popped)",
            'solution': 'class ArrayStack:\n'
                        '    def __init__(self):\n'
                        '        self._data = []\n'
                        '\n'
                        '    def push(self, val: int) -> None:\n'
                        '        self._data.append(val)\n'
                        '\n'
                        '    def pop(self) -> int:\n'
                        '        if not self._data:\n'
                        "            raise IndexError('pop from empty stack')\n"
                        '        return self._data.pop()\n'
                        '\n'
                        '    def peek(self) -> int:\n'
                        '        if not self._data:\n'
                        "            raise IndexError('peek from empty stack')\n"
                        '        return self._data[-1]\n'
                        '\n'
                        '    def is_empty(self) -> bool:\n'
                        '        return len(self._data) == 0\n'
                        '\n'
                        's = ArrayStack()\n'
                        's.push(10)\n'
                        's.push(20)\n'
                        "print('Peek:', s.peek())\n"
                        "print('Popped:', s.pop())\n"
                        "print('Is empty:', s.is_empty())\n",
            'starter': 'class ArrayStack:\n'
                       '    def __init__(self):\n'
                       '        self._data = []\n'
                       '\n'
                       '    # TODO: Implement push(val), pop() -> int, peek() -> int, and is_empty() -> bool\n'
                       '\n'
                       's = ArrayStack()\n'
                       's.push(10)\n'
                       's.push(20)\n'
                       "print('Peek:', s.peek())\n"
                       "print('Popped:', s.pop())\n"
                       "print('Is empty:', s.is_empty())\n",
            'summary': 'Stacks enforce Last-In, First-Out (LIFO) discipline, supporting O(1) push, pop, and peek '
                       'operations.',
            'takeaway': 'LIFO discipline restricts mutations to a single boundary, guaranteeing O(1) operations.'},
    87: {   'hint': 'Check if len(s) % 2 != 0. Loop chars: if closing bracket check stack and top match then pop, else '
                    'append opening bracket. Return len(stack) == 0.',
            'mechanics': 'Iterate through characters. If opening bracket, push onto stack. If closing bracket, verify '
                         'that stack is non-empty and `stack[-1]` matches corresponding opening token (`mapping[ch]`), '
                         'then pop. Return True if stack is empty at termination.',
            'patterns': ['Test 1: True', 'Test 2: False', 'Test 3: False', 'Test 4: True'],
            'practice_task': 'Write a function that validates balanced parentheses across () [] and {}.',
            'q1': 'If string s has an odd length, why can it be rejected immediately in O(1) time?',
            'q1_ans': 'A',
            'q1_exp': {   'A': 'Correct! Every bracket must pair with its complement. If `len(s) % 2 != 0`, at least '
                               'one bracket is guaranteed to remain unmatched, allowing an immediate O(1) early exit.',
                          'B': 'Incorrect: Stacks accept any number of elements.',
                          'C': 'Incorrect: Hashing has nothing to do with parity.',
                          'D': 'Incorrect: Even length is a mandatory mathematical invariant.'},
            'q1_opts': [   {   'id': 'A',
                               'label': 'Because every opening bracket requires an exact matching closing partner, so '
                                        'balanced bracket strings must have an even length'},
                           {'id': 'B', 'label': 'Because Python stacks only accept even counts'},
                           {'id': 'C', 'label': 'Because odd numbers cannot be hashed'},
                           {'id': 'D', 'label': 'It cannot be rejected immediately'}],
            'q2': "What error condition is detected if `stack` is empty when encountering a closing bracket `')'`?",
            'q2_ans': 'A',
            'q2_exp': {   'A': 'Correct! A closing delimiter needs an existing opening delimiter at the top of the '
                               'stack. If the stack is empty, there is no opening partner, so the expression is '
                               'immediately invalid.',
                          'B': 'Incorrect: Unmatched opening delimiters are detected when the stack is non-empty at '
                               'the end of the string.',
                          'C': 'Incorrect: No memory overflow occurs.',
                          'D': 'Incorrect: Syntactic mismatch is not corruption.'},
            'q2_opts': [   {   'id': 'A',
                               'label': 'An unmatched closing delimiter (no corresponding opening bracket preceded '
                                        'it)'},
                           {'id': 'B', 'label': 'An unmatched opening delimiter'},
                           {'id': 'C', 'label': 'A memory overflow'},
                           {'id': 'D', 'label': 'String corruption'}],
            'recap': [   {   'concept': 'LIFO Nesting Mirror',
                             'naiveIntuition': "Count counts of '(' and ')' with counters",
                             'pythonReality': "Counters fail to detect interleaved nesting errors like '([)]'; stacks "
                                              'enforce strict hierarchical pairing'},
                         {   'concept': 'Early Rejection Invariant',
                             'naiveIntuition': 'Always scan the full string',
                             'pythonReality': 'Checking len(s) % 2 != 0 and verifying stack state on closing brackets '
                                              'enables immediate early exit'}],
            'sample_code': 'def is_valid(s):\n'
                           "    mapping = {')': '(', '}': '{', ']': '['}\n"
                           '    stack = []\n'
                           '    for ch in s:\n'
                           '        if ch in mapping:\n'
                           "            top = stack.pop() if stack else '#'\n"
                           '            if mapping[ch] != top: return False\n'
                           '        else:\n'
                           '            stack.append(ch)\n'
                           '    return len(stack) == 0',
            'solution': 'def is_valid_parentheses(s: str) -> bool:\n'
                        '    if len(s) % 2 != 0:\n'
                        '        return False\n'
                        "    mapping = {')': '(', '}': '{', ']': '['}\n"
                        '    stack = []\n'
                        '    for ch in s:\n'
                        '        if ch in mapping:\n'
                        '            if not stack or stack[-1] != mapping[ch]:\n'
                        '                return False\n'
                        '            stack.pop()\n'
                        '        else:\n'
                        '            stack.append(ch)\n'
                        '    return len(stack) == 0\n'
                        '\n'
                        "print('Test 1:', is_valid_parentheses('()[]{}'))\n"
                        "print('Test 2:', is_valid_parentheses('(]'))\n"
                        "print('Test 3:', is_valid_parentheses('([)]'))\n"
                        "print('Test 4:', is_valid_parentheses('{[]}'))\n",
            'starter': 'def is_valid_parentheses(s: str) -> bool:\n'
                       '    # TODO: Use a stack to validate balanced syntax\n'
                       '    return False\n'
                       '\n'
                       "print('Test 1:', is_valid_parentheses('()[]{}'))\n"
                       "print('Test 2:', is_valid_parentheses('(]'))\n"
                       "print('Test 3:', is_valid_parentheses('([)]'))\n"
                       "print('Test 4:', is_valid_parentheses('{[]}'))\n",
            'summary': 'Parentheses Matching evaluates nested syntactic structures by matching closing delimiters '
                       'against the most recent unmatched opening delimiter stored on a stack.',
            'takeaway': 'Stacks naturally mirror nested syntactic hierarchy in linear O(N) time.'},
    88: {   'hint': 'In push: m = val if not self.ms else min(val, self.ms[-1]); ms.append(m). In pop: pop both s and '
                    'ms. In get_min: return ms[-1].',
            'mechanics': 'On `push(x)`: the auxiliary `min_stack` pushes `min(x, min_stack[-1])`. On `pop()`: both the '
                         'primary stack and `min_stack` pop simultaneously. Thus `min_stack[-1]` always reflects the '
                         'global minimum of the active stack in strict O(1) time.',
            'patterns': ['Min: -3', 'Top: 0', 'Min: -2'],
            'practice_task': 'Implement a MinStack that retrieves the minimum element in O(1) time.',
            'q1': "Why can't we simply track a single variable `current_min` instead of an auxiliary stack?",
            'q1_ans': 'A',
            'q1_exp': {   'A': 'Correct! If the minimum element is popped off, the stack needs to restore the minimum '
                               'that existed before that element was pushed. A secondary stack records this exact '
                               'historical timeline.',
                          'B': 'Incorrect: Python numbers can be negative.',
                          'C': 'Incorrect: Instance attributes are accessible.',
                          'D': 'Incorrect: When minimum is popped, finding next minimum takes O(N) without a history '
                               'structure.'},
            'q1_opts': [   {   'id': 'A',
                               'label': 'When the element equal to `current_min` is popped, a single variable cannot '
                                        'recover the previous minimum without an O(N) scan of the entire stack'},
                           {'id': 'B', 'label': 'Because single variables cannot store negative numbers'},
                           {'id': 'C', 'label': 'Because Python functions cannot read global variables'},
                           {'id': 'D', 'label': 'A single variable does work with O(1) pop'}],
            'q2': 'What is the auxiliary space complexity of the Min Stack design?',
            'q2_ans': 'A',
            'q2_exp': {   'A': 'Correct! Each pushed element stores its corresponding minimum in `min_stack`, doubling '
                               'the memory usage to 2N elements (asymptotically O(N)).',
                          'B': 'Incorrect: Historical tracking requires proportional storage.',
                          'C': 'Incorrect: Space is linear, not quadratic.',
                          'D': 'Incorrect: Logarithmic storage does not store full element histories.'},
            'q2_opts': [   {'id': 'A', 'label': 'O(N) space, where N is the number of active elements'},
                           {'id': 'B', 'label': 'O(1) space'},
                           {'id': 'C', 'label': 'O(N^2) space'},
                           {'id': 'D', 'label': 'O(log N) space'}],
            'recap': [   {   'concept': 'State History Preservation',
                             'naiveIntuition': 'Calculate min dynamically on demand',
                             'pythonReality': 'Caching the running minimum at every stack frame enables instant O(1) '
                                              'retrieval'},
                         {   'concept': 'Time-Space Trade-off',
                             'naiveIntuition': 'O(1) time requires complex algorithms',
                             'pythonReality': 'Investing an extra O(N) auxiliary stack collapses getMin() from O(N) '
                                              'linear scan to O(1) lookup'}],
            'sample_code': '# Min Stack dual-stack design\n'
                           'class MinStack:\n'
                           '    def __init__(self):\n'
                           '        self.stack = []\n'
                           '        self.min_stack = []\n'
                           '    def push(self, val):\n'
                           '        self.stack.append(val)\n'
                           '        new_min = min(val, self.min_stack[-1]) if self.min_stack else val\n'
                           '        self.min_stack.append(new_min)\n'
                           '    def pop(self):\n'
                           '        self.stack.pop()\n'
                           '        self.min_stack.pop()\n'
                           '    def getMin(self):\n'
                           '        return self.min_stack[-1]',
            'solution': 'class MinStack:\n'
                        '    def __init__(self):\n'
                        '        self.s = []\n'
                        '        self.ms = []\n'
                        '\n'
                        '    def push(self, val: int) -> None:\n'
                        '        self.s.append(val)\n'
                        '        m = val if not self.ms else min(val, self.ms[-1])\n'
                        '        self.ms.append(m)\n'
                        '\n'
                        '    def pop(self) -> None:\n'
                        '        if self.s:\n'
                        '            self.s.pop()\n'
                        '            self.ms.pop()\n'
                        '\n'
                        '    def top(self) -> int:\n'
                        '        return self.s[-1] if self.s else -1\n'
                        '\n'
                        '    def get_min(self) -> int:\n'
                        '        return self.ms[-1] if self.ms else -1\n'
                        '\n'
                        'ms = MinStack()\n'
                        'ms.push(-2)\n'
                        'ms.push(0)\n'
                        'ms.push(-3)\n'
                        "print('Min:', ms.get_min())\n"
                        'ms.pop()\n'
                        "print('Top:', ms.top())\n"
                        "print('Min:', ms.get_min())\n",
            'starter': 'class MinStack:\n'
                       '    def __init__(self):\n'
                       '        self.s = []\n'
                       '        self.ms = []\n'
                       '\n'
                       '    # TODO: Implement push(val), pop(), top() -> int, and get_min() -> int\n'
                       '\n'
                       'ms = MinStack()\n'
                       'ms.push(-2)\n'
                       'ms.push(0)\n'
                       'ms.push(-3)\n'
                       "print('Min:', ms.get_min()) # -3\n"
                       'ms.pop()\n'
                       "print('Top:', ms.top())     # 0\n"
                       "print('Min:', ms.get_min()) # -2\n",
            'summary': 'Min Stack achieves O(1) getMin() alongside O(1) push and pop by maintaining a secondary '
                       'auxiliary stack of minimums or storing (val, current_min) tuples.',
            'takeaway': 'Parallel auxiliary stacks preserve invariant histories across reversible push/pop timelines.'},
    89: {   'hint': 'Check is_full() in en_queue, assign data[tail]=val, tail=(tail+1)%cap, size+=1. In de_queue check '
                    'size==0, head=(head+1)%cap, size-=1.',
            'mechanics': 'The buffer maintains `head`, `tail`, `size`, and `capacity`. Enqueue: `data[tail] = val; '
                         'tail = (tail + 1) % capacity; size += 1`. Dequeue: `val = data[head]; head = (head + 1) % '
                         'capacity; size -= 1`. All operations run in strict O(1) time without re-allocations.',
            'patterns': [   'Enq 1: True',
                            'Enq 2: True',
                            'Enq 3: True',
                            'Enq 4 (overflow): False',
                            'Front: 1',
                            'Deq: True',
                            'Enq 4 (now ok): True'],
            'practice_task': 'Build a Circular Queue with enqueue, dequeue, front, and is_full methods.',
            'q1': 'Why is modular arithmetic `(idx + 1) % capacity` essential in a circular queue?',
            'q1_ans': 'A',
            'q1_exp': {   'A': 'Correct! When `idx == capacity - 1`, `(capacity - 1 + 1) % capacity == 0`. The pointer '
                               'smoothly wraps back to index 0 without moving elements.',
                          'B': 'Incorrect: Modular indexing is pointer arithmetic, not encryption.',
                          'C': 'Incorrect: Array size remains fixed.',
                          'D': 'Incorrect: Elements can be duplicated.'},
            'q1_opts': [   {   'id': 'A',
                               'label': 'It causes pointers reaching the end of the array to wrap around to index 0, '
                                        'reusing freed slots at the front'},
                           {'id': 'B', 'label': 'It encrypts queue contents'},
                           {'id': 'C', 'label': 'It automatically expands array size'},
                           {'id': 'D', 'label': 'It prevents duplicate elements'}],
            'q2': 'In a circular queue with capacity K, how do you distinguish between a full queue and an empty '
                  'queue?',
            'q2_ans': 'A',
            'q2_exp': {   'A': 'Correct! When `head == tail`, the queue could be either completely empty or completely '
                               'full. Maintaining an explicit `size` counter trivially disambiguates the two states.',
                          'B': 'Incorrect: `head == tail` occurs when both empty and full unless an extra dummy slot '
                               'is reserved.',
                          'C': 'Incorrect: Queues are ordered chronologically, not sorted.',
                          'D': 'Incorrect: Fixed-capacity buffers can become full.'},
            'q2_opts': [   {   'id': 'A',
                               'label': 'By maintaining an explicit `size` counter (empty if `size == 0`, full if '
                                        '`size == capacity`)'},
                           {'id': 'B', 'label': 'By checking if `head == tail`'},
                           {'id': 'C', 'label': 'By sorting the array'},
                           {'id': 'D', 'label': 'Circular queues cannot be full'}],
            'recap': [   {   'concept': 'Ring Buffer Wraparound',
                             'naiveIntuition': 'Shift all array elements forward on dequeue',
                             'pythonReality': 'Advancing head with modular arithmetic reclaims capacity in O(1) time '
                                              'without touching array data'},
                         {   'concept': 'Zero Dynamic Allocation',
                             'naiveIntuition': 'Queues must dynamically grow and shrink',
                             'pythonReality': 'Fixed circular buffers eliminate garbage collection spikes in '
                                              'latency-critical packet routers and audio buffers'}],
            'sample_code': '# Circular queue modular pointer wrapping\n'
                           '# tail = (tail + 1) % capacity\n'
                           '# head = (head + 1) % capacity',
            'solution': 'class MyCircularQueue:\n'
                        '    def __init__(self, k: int):\n'
                        '        self.cap = k\n'
                        '        self.data = [0] * k\n'
                        '        self.head = 0\n'
                        '        self.tail = 0\n'
                        '        self.size = 0\n'
                        '\n'
                        '    def en_queue(self, val: int) -> bool:\n'
                        '        if self.is_full():\n'
                        '            return False\n'
                        '        self.data[self.tail] = val\n'
                        '        self.tail = (self.tail + 1) % self.cap\n'
                        '        self.size += 1\n'
                        '        return True\n'
                        '\n'
                        '    def de_queue(self) -> bool:\n'
                        '        if self.size == 0:\n'
                        '            return False\n'
                        '        self.head = (self.head + 1) % self.cap\n'
                        '        self.size -= 1\n'
                        '        return True\n'
                        '\n'
                        '    def front(self) -> int:\n'
                        '        if self.size == 0:\n'
                        '            return -1\n'
                        '        return self.data[self.head]\n'
                        '\n'
                        '    def is_full(self) -> bool:\n'
                        '        return self.size == self.cap\n'
                        '\n'
                        'q = MyCircularQueue(3)\n'
                        "print('Enq 1:', q.en_queue(1))\n"
                        "print('Enq 2:', q.en_queue(2))\n"
                        "print('Enq 3:', q.en_queue(3))\n"
                        "print('Enq 4 (overflow):', q.en_queue(4))\n"
                        "print('Front:', q.front())\n"
                        "print('Deq:', q.de_queue())\n"
                        "print('Enq 4 (now ok):', q.en_queue(4))\n",
            'starter': 'class MyCircularQueue:\n'
                       '    def __init__(self, k: int):\n'
                       '        self.cap = k\n'
                       '        self.data = [0] * k\n'
                       '        self.head = 0\n'
                       '        self.tail = 0\n'
                       '        self.size = 0\n'
                       '\n'
                       '    # TODO: Implement en_queue(val) -> bool, de_queue() -> bool, front() -> int, is_full() -> '
                       'bool\n'
                       '\n'
                       'q = MyCircularQueue(3)\n'
                       "print('Enq 1:', q.en_queue(1))\n"
                       "print('Enq 2:', q.en_queue(2))\n"
                       "print('Enq 3:', q.en_queue(3))\n"
                       "print('Enq 4 (overflow):', q.en_queue(4))\n"
                       "print('Front:', q.front())\n"
                       "print('Deq:', q.de_queue())\n"
                       "print('Enq 4 (now ok):', q.en_queue(4))\n",
            'summary': 'Circular Queues wrap head and tail indices around a fixed-size array using modular arithmetic '
                       '(`(idx + 1) % capacity`), eliminating memory shifts in hardware buffers.',
            'takeaway': 'Circular ring buffers enable high-performance zero-allocation FIFO streaming in embedded and '
                        'OS systems.'},
    90: {   'hint': 'In push: in_stack.append(x). In peek: if not out_stack: while in_stack: '
                    'out_stack.append(in_stack.pop()); return out_stack[-1]. In pop: peek() and out_stack.pop().',
            'mechanics': 'Maintain two stacks: `in_stack` (for push) and `out_stack` (for pop/peek). Push appends to '
                         '`in_stack` in O(1). When popping or peeking: if `out_stack` is empty, pop all elements from '
                         '`in_stack` and push them into `out_stack`, reversing their order to restore FIFO! Amortized '
                         'analysis: each element is pushed and popped at most twice, averaging O(1) across all '
                         'operations.',
            'patterns': ['Peek: 1', 'Pop: 1', 'Empty: False'],
            'practice_task': 'Implement a First-In, First-Out (FIFO) queue using two LIFO stacks.',
            'q1': 'Why is the amortized time complexity of `pop()` and `peek()` in a two-stack queue O(1), even though '
                  'transferring elements takes O(N) when out_stack is empty?',
            'q1_ans': 'A',
            'q1_exp': {   'A': 'Correct! By the accounting method of amortized analysis, each item has 2 pushes and 2 '
                               'pops across its entire journey. 4 operations per item = amortized O(1) constant time.',
                          'B': 'Incorrect: Algorithmic complexity is mathematical, not compiler dependent.',
                          'C': 'Incorrect: out_stack starts empty.',
                          'D': 'Incorrect: Python lists are contiguous arrays.'},
            'q1_opts': [   {   'id': 'A',
                               'label': 'Each element is moved from in_stack to out_stack exactly once across its '
                                        'entire lifetime in the queue; the O(N) transfer cost is distributed over N '
                                        'individual O(1) operations'},
                           {'id': 'B', 'label': 'Because transferring uses a C compiler optimization'},
                           {'id': 'C', 'label': 'Because out_stack is never empty'},
                           {'id': 'D', 'label': 'Because Python stacks are doubly linked lists'}],
            'q2': 'When should elements be moved from `in_stack` to `out_stack`?',
            'q2_ans': 'A',
            'q2_exp': {   'A': 'Correct! If out_stack still holds older elements, pouring newer elements on top of '
                               'them would violate FIFO order. Only refill out_stack when it is fully drained.',
                          'B': 'Incorrect: Transferring after every push would degrade push to O(N).',
                          'C': 'Incorrect: Transfers must be strictly demand-driven.',
                          'D': 'Incorrect: Data structures require deterministic ordering invariants.'},
            'q2_opts': [   {   'id': 'A',
                               'label': 'ONLY when out_stack is completely empty; premature transfers would scramble '
                                        'the relative FIFO arrival order of newer elements'},
                           {'id': 'B', 'label': 'After every single push'},
                           {'id': 'C', 'label': 'Whenever in_stack has more than 5 elements'},
                           {'id': 'D', 'label': 'At random intervals'}],
            'recap': [   {   'concept': 'Double Inversion Identity',
                             'naiveIntuition': 'Stacks can never act as queues',
                             'pythonReality': 'Inverting a stack twice restores the original FIFO order, proving '
                                              'structural duality between queues and stacks'},
                         {   'concept': 'Amortized Efficiency',
                             'naiveIntuition': 'Occasional O(N) operations mean the algorithm is slow',
                             'pythonReality': 'Infrequent batch transfers averaged over thousands of items maintain '
                                              'sub-microsecond latency'}],
            'sample_code': '# Queue using Two Stacks\n'
                           'class MyQueue:\n'
                           '    def __init__(self):\n'
                           '        self.in_stk = []; self.out_stk = []\n'
                           '    def push(self, x):\n'
                           '        self.in_stk.append(x)\n'
                           '    def pop(self):\n'
                           '        self.peek()\n'
                           '        return self.out_stk.pop()\n'
                           '    def peek(self):\n'
                           '        if not self.out_stk:\n'
                           '            while self.in_stk: self.out_stk.append(self.in_stk.pop())\n'
                           '        return self.out_stk[-1]\n'
                           '    def empty(self):\n'
                           '        return not self.in_stk and not self.out_stk',
            'solution': 'class MyQueue:\n'
                        '    def __init__(self):\n'
                        '        self.in_stack = []\n'
                        '        self.out_stack = []\n'
                        '\n'
                        '    def push(self, x: int) -> None:\n'
                        '        self.in_stack.append(x)\n'
                        '\n'
                        '    def pop(self) -> int:\n'
                        '        self.peek()\n'
                        '        return self.out_stack.pop()\n'
                        '\n'
                        '    def peek(self) -> int:\n'
                        '        if not self.out_stack:\n'
                        '            while self.in_stack:\n'
                        '                self.out_stack.append(self.in_stack.pop())\n'
                        '        return self.out_stack[-1]\n'
                        '\n'
                        '    def empty(self) -> bool:\n'
                        '        return not self.in_stack and not self.out_stack\n'
                        '\n'
                        'q = MyQueue()\n'
                        'q.push(1)\n'
                        'q.push(2)\n'
                        "print('Peek:', q.peek())\n"
                        "print('Pop:', q.pop())\n"
                        "print('Empty:', q.empty())\n",
            'starter': 'class MyQueue:\n'
                       '    def __init__(self):\n'
                       '        self.in_stack = []\n'
                       '        self.out_stack = []\n'
                       '\n'
                       '    # TODO: Implement push(x), pop() -> int, peek() -> int, and empty() -> bool\n'
                       '\n'
                       'q = MyQueue()\n'
                       'q.push(1)\n'
                       'q.push(2)\n'
                       "print('Peek:', q.peek()) # 1\n"
                       "print('Pop:', q.pop())   # 1\n"
                       "print('Empty:', q.empty()) # False\n",
            'summary': 'Implementing a FIFO Queue using Two LIFO Stacks transfers elements from an input stack to an '
                       'output stack lazily, achieving amortized O(1) push and pop.',
            'takeaway': 'Reversing LIFO twice yields FIFO; lazy batch transfers ensure amortized O(1) queue '
                        'operations.'},
    91: {   'hint': 'Initialize res = [-1] * len(nums), stack = []. Loop i, x: while stack and nums[stack[-1]] < x: '
                    'res[stack.pop()] = x; stack.append(i). Return res.',
            'mechanics': 'Maintain a stack of indices with decreasing values. When visiting `arr[i]`: while stack is '
                         'non-empty and `arr[i] > arr[stack[-1]]`, pop index `idx` from stack; `arr[i]` is the Next '
                         'Greater Element for `idx`. Then push `i`. Elements left on the stack have no greater '
                         'element.',
            'patterns': ['NGE: [4, 2, 4, -1, -1]'],
            'practice_task': 'Find the Next Greater Element for each array entry (return -1 if none exists).',
            'q1': 'Why is the time complexity of the monotonic stack algorithm O(N) even though there is a nested '
                  'while loop inside the for loop?',
            'q1_ans': 'A',
            'q1_exp': {   'A': 'Correct! Across the entire execution of the outer loop (N iterations), at most N '
                               'elements are pushed, so at most N elements can ever be popped. The amortized cost per '
                               'element is O(1).',
                          'B': 'Incorrect: Monotonic stack works on completely arbitrary unsorted arrays.',
                          'C': 'Incorrect: The while loop can pop multiple elements in a single iteration.',
                          'D': 'Incorrect: Complexity is an algorithmic property, not an interpreter optimization.'},
            'q1_opts': [   {   'id': 'A',
                               'label': 'Each element is pushed onto the stack exactly once and popped at most once, '
                                        'bounding total operations by 2N = O(N)'},
                           {'id': 'B', 'label': 'Because the array is sorted'},
                           {'id': 'C', 'label': 'Because the while loop only runs once per execution'},
                           {'id': 'D', 'label': 'Because Python lists optimize inner loops'}],
            'q2': 'Why does the monotonic stack store indices rather than raw values?',
            'q2_ans': 'A',
            'q2_exp': {   'A': 'Correct! Storing indices gives dual power: `nums[idx]` yields the value, while `idx` '
                               'allows updating `res[idx] = x` and measuring horizontal span (`i - idx`).',
                          'B': 'Incorrect: Python stacks can store any object.',
                          'C': 'Incorrect: Both are integers in CPython.',
                          'D': 'Incorrect: No string conversion occurs.'},
            'q2_opts': [   {   'id': 'A',
                               'label': 'Indices allow updating the result array at the exact original position and '
                                        'computing horizontal distances'},
                           {'id': 'B', 'label': 'Python lists cannot store numbers directly in stacks'},
                           {'id': 'C', 'label': 'Indices require less memory than integers'},
                           {'id': 'D', 'label': 'Because values are converted to strings'}],
            'recap': [   {   'concept': 'Amortized Linear Bound',
                             'naiveIntuition': 'Nested loops imply O(N^2) quadratic time',
                             'pythonReality': 'Monotonic stacks guarantee that each element enters and exits the stack '
                                              'at most once, yielding strictly O(N) aggregate time'},
                         {   'concept': 'Monotonic Invariant',
                             'naiveIntuition': 'Check all rightward elements sequentially',
                             'pythonReality': 'Stack elements represent active queries waiting for their first larger '
                                              'successor; popping on arrival resolves them instantly'}],
            'sample_code': '# Next Greater Element\n'
                           'def next_greater(nums):\n'
                           '    res = [-1] * len(nums)\n'
                           '    stack = [] # indices\n'
                           '    for i, x in enumerate(nums):\n'
                           '        while stack and nums[stack[-1]] < x:\n'
                           '            prev_idx = stack.pop()\n'
                           '            res[prev_idx] = x\n'
                           '        stack.append(i)\n'
                           '    return res',
            'solution': 'def next_greater_elements(nums: list[int]) -> list[int]:\n'
                        '    res = [-1] * len(nums)\n'
                        '    stack = []\n'
                        '    for i, x in enumerate(nums):\n'
                        '        while stack and nums[stack[-1]] < x:\n'
                        '            idx = stack.pop()\n'
                        '            res[idx] = x\n'
                        '        stack.append(i)\n'
                        '    return res\n'
                        '\n'
                        "print('NGE:', next_greater_elements([2, 1, 2, 4, 3]))\n",
            'starter': 'def next_greater_elements(nums: list[int]) -> list[int]:\n'
                       '    # TODO: Use a monotonic decreasing stack of indices\n'
                       '    # Return array of next greater elements\n'
                       '    return []\n'
                       '\n'
                       "print('NGE:', next_greater_elements([2, 1, 2, 4, 3]))\n",
            'summary': 'Monotonic Stacks maintain elements in strictly monotonic (increasing or decreasing) order, '
                       'finding the Next Greater Element for all array items in amortized O(N) time.',
            'takeaway': 'Each index is pushed and popped at most once, achieving amortized O(N) resolution of nearest '
                        'greater/smaller queries.'},
    92: {   'hint': 'Append 0 to heights copy. stack = [-1], max_area = 0. While stack[-1] != -1 and h_copy[stack[-1]] '
                    '>= h: height = h_copy[stack.pop()], width = i - stack[-1] - 1, max_area = max(max_area, height * '
                    'width). stack.append(i).',
            'mechanics': 'For each bar of height H, the rectangle width extends left to the first smaller bar and '
                         'right to the first smaller bar. When a shorter bar arrives, it pops taller bars from the '
                         "stack. The popped bar's area is: `height * (current_index - stack[-1] - 1)`. Padding with "
                         'boundary zero-height sentinels simplifies draining.',
            'patterns': ['Max Area 1: 10', 'Max Area 2: 4'],
            'practice_task': 'Calculate the largest rectangular area in an input histogram.',
            'q1': 'Why do we pad the heights list with a sentinel value of 0 at the end?',
            'q1_ans': 'A',
            'q1_exp': {   'A': 'Correct! Because heights are non-negative, appending 0 guarantees that every bar '
                               'remaining on the monotonic increasing stack is strictly greater than 0, cleanly '
                               'draining the stack without duplicate cleanup loops.',
                          'B': 'Incorrect: Parity is irrelevant.',
                          'C': 'Incorrect: Bars can have height 0.',
                          'D': 'Incorrect: Algorithmic sentinel has no relation to cache lines.'},
            'q1_opts': [   {   'id': 'A',
                               'label': 'To force all remaining bars on the stack to be popped and their areas '
                                        'calculated before algorithm termination'},
                           {'id': 'B', 'label': 'To make the array length an even number'},
                           {'id': 'C', 'label': 'Because histogram bars cannot have height 0'},
                           {'id': 'D', 'label': 'To reset CPU cache lines'}],
            'q2': 'When bar `H` is popped from the stack between `stack[-1]` and `current_i`, what is its effective '
                  'rectangle width?',
            'q2_ans': 'A',
            'q2_exp': {   'A': 'Correct! The limiting bar spans strictly between the smaller left boundary `stack[-1]` '
                               'and smaller right boundary `current_i`. The number of bars strictly between them is '
                               '`current_i - stack[-1] - 1`.',
                          'B': 'Incorrect: That includes one of the smaller boundary indices.',
                          'C': 'Incorrect: Does not account for left bound.',
                          'D': 'Incorrect: That is total array length.'},
            'q2_opts': [   {'id': 'A', 'label': '`current_i - stack[-1] - 1`'},
                           {'id': 'B', 'label': '`current_i - stack[-1]`'},
                           {'id': 'C', 'label': '`current_i + 1`'},
                           {'id': 'D', 'label': '`len(heights)`'}],
            'recap': [   {   'concept': 'Boundary Sentinels',
                             'naiveIntuition': 'Write a separate loop to pop remaining bars after the main loop',
                             'pythonReality': 'Padding input with sentinel 0 flushes the monotonic stack naturally, '
                                              'eliminating code duplication'},
                         {   'concept': 'Width Derivation Invariant',
                             'naiveIntuition': 'Width is simply index distance from start',
                             'pythonReality': 'The stack index immediately below the popped element marks the exact '
                                              'left bound of smaller height'}],
            'sample_code': '# Largest Rectangle in Histogram\n'
                           'def largest_rectangle_area(heights):\n'
                           '    stack = [-1] # Sentinel index\n'
                           '    max_area = 0\n'
                           '    heights.append(0) # Sentinel flush\n'
                           '    for i, h in enumerate(heights):\n'
                           '        while stack[-1] != -1 and heights[stack[-1]] >= h:\n'
                           '            height = heights[stack.pop()]\n'
                           '            width = i - stack[-1] - 1\n'
                           '            max_area = max(max_area, height * width)\n'
                           '        stack.append(i)\n'
                           '    heights.pop()\n'
                           '    return max_area',
            'solution': 'def largest_rectangle(heights: list[int]) -> int:\n'
                        '    h_copy = heights + [0]\n'
                        '    stack = [-1]\n'
                        '    max_area = 0\n'
                        '    for i, h in enumerate(h_copy):\n'
                        '        while stack[-1] != -1 and h_copy[stack[-1]] >= h:\n'
                        '            height = h_copy[stack.pop()]\n'
                        '            width = i - stack[-1] - 1\n'
                        '            max_area = max(max_area, height * width)\n'
                        '        stack.append(i)\n'
                        '    return max_area\n'
                        '\n'
                        "print('Max Area 1:', largest_rectangle([2, 1, 5, 6, 2, 3]))\n"
                        "print('Max Area 2:', largest_rectangle([2, 4]))\n",
            'starter': 'def largest_rectangle(heights: list[int]) -> int:\n'
                       '    # TODO: Implement largest rectangle using a monotonic increasing stack\n'
                       '    return 0\n'
                       '\n'
                       "print('Max Area 1:', largest_rectangle([2, 1, 5, 6, 2, 3])) # 10\n"
                       "print('Max Area 2:', largest_rectangle([2, 4]))             # 4\n",
            'summary': 'Largest Rectangle in Histogram utilizes a Monotonic Increasing Stack to determine the left and '
                       'right boundaries where each bar is the limiting height, running in O(N) time.',
            'takeaway': 'Monotonic increasing stacks identify left/right smaller boundaries to compute maximal areas '
                        'in O(N) time.'},
    93: {   'hint': 'Loop i, x: if q and q[0] <= i - k: q.popleft(); while q and nums[q[-1]] <= x: q.pop(); '
                    'q.append(i); if i >= k - 1: res.append(nums[q[0]]). Return res.',
            'mechanics': 'A double-ended queue (`deque`) stores indices. For each new index `i`: (1) Evict expired '
                         'indices from the front: `while q and q[0] <= i - k: q.popleft()`. (2) Evict smaller elements '
                         'from the back: `while q and nums[q[-1]] <= nums[i]: q.pop()`. (3) Append `i`. The window '
                         'maximum is always at `nums[q[0]]`.',
            'patterns': ['Sliding max (k=3): [3, 3, 5, 5, 6, 7]'],
            'practice_task': 'Find the maximum value in every sliding window of size K.',
            'q1': 'Why can elements smaller than `nums[i]` be safely popped from the back of the deque when `nums[i]` '
                  'enters the window?',
            'q1_ans': 'A',
            'q1_exp': {   'A': 'Correct! Any element that is older (smaller index) AND smaller in value can never be '
                               'the maximum of any current or future window that contains `nums[i]`. It is permanently '
                               'dominated.',
                          'B': 'Incorrect: Deque grows dynamically.',
                          'C': 'Incorrect: Algorithmic dominance is independent of hardware.',
                          'D': 'Incorrect: Deque itself enforces no sorting.'},
            'q1_opts': [   {   'id': 'A',
                               'label': 'Because `nums[i]` is both larger and will stay in the sliding window longer '
                                        'than those preceding smaller elements, rendering them useless as potential '
                                        'maximums'},
                           {'id': 'B', 'label': 'Because the deque has a fixed capacity of 5'},
                           {'id': 'C', 'label': 'To save battery on mobile devices'},
                           {'id': 'D', 'label': 'Because Python deque requires sorted values'}],
            'q2': 'What is the total time complexity of Sliding Window Maximum across an array of length N using a '
                  'monotonic deque?',
            'q2_ans': 'A',
            'q2_exp': {   'A': 'Correct! Every element index enters the deque once and leaves the deque at most once '
                               '(either from the back when dominated or from the front when expired). Total operations '
                               '$\\le 2N = O(N)$.',
                          'B': 'Incorrect: O(N * K) is the naive brute force sliding window.',
                          'C': 'Incorrect: O(N log K) is the heap or balanced BST approach.',
                          'D': 'Incorrect: Monotonic deque completely avoids quadratic scans.'},
            'q2_opts': [   {'id': 'A', 'label': 'O(N) amortized time'},
                           {'id': 'B', 'label': 'O(N * K)'},
                           {'id': 'C', 'label': 'O(N log K)'},
                           {'id': 'D', 'label': 'O(N^2)'}],
            'recap': [   {   'concept': 'Domination Invariant',
                             'naiveIntuition': 'Keep all window elements in container',
                             'pythonReality': 'Pruning elements that are both smaller and older eliminates clutter, '
                                              'ensuring the front always holds the maximum in O(1)'},
                         {   'concept': 'Bidirectional Pruning',
                             'naiveIntuition': 'Queues only pop from one side',
                             'pythonReality': 'A deque permits popping expired elements from the front and dominated '
                                              'elements from the back'}],
            'sample_code': 'from collections import deque\n'
                           'def max_sliding_window(nums, k):\n'
                           '    q = deque() # indices\n'
                           '    res = []\n'
                           '    for i, x in enumerate(nums):\n'
                           '        if q and q[0] <= i - k: q.popleft()\n'
                           '        while q and nums[q[-1]] <= x: q.pop()\n'
                           '        q.append(i)\n'
                           '        if i >= k - 1: res.append(nums[q[0]])\n'
                           '    return res',
            'solution': 'from collections import deque\n'
                        '\n'
                        'def sliding_max(nums: list[int], k: int) -> list[int]:\n'
                        '    q = deque()\n'
                        '    res = []\n'
                        '    for i, x in enumerate(nums):\n'
                        '        if q and q[0] <= i - k:\n'
                        '            q.popleft()\n'
                        '        while q and nums[q[-1]] <= x:\n'
                        '            q.pop()\n'
                        '        q.append(i)\n'
                        '        if i >= k - 1:\n'
                        '            res.append(nums[q[0]])\n'
                        '    return res\n'
                        '\n'
                        'nums = [1, 3, -1, -3, 5, 3, 6, 7]\n'
                        "print('Sliding max (k=3):', sliding_max(nums, 3))\n",
            'starter': 'from collections import deque\n'
                       '\n'
                       'def sliding_max(nums: list[int], k: int) -> list[int]:\n'
                       '    # TODO: Implement sliding window maximum using collections.deque\n'
                       '    return []\n'
                       '\n'
                       'nums = [1, 3, -1, -3, 5, 3, 6, 7]\n'
                       "print('Sliding max (k=3):', sliding_max(nums, 3))\n",
            'summary': 'Monotonic Deques maintain elements in monotonically decreasing order to solve the Sliding '
                       'Window Maximum problem in amortized O(N) time.',
            'takeaway': 'Monotonic deques maintain candidates for window extremums, pruning suboptimal elements in '
                        'O(1) amortized time.'},
    94: {   'hint': "Track vals and ops stacks. If digit parse full integer. If '(' push to ops. If ')' pop and apply "
                    "until '('. If operator, while top op has >= precedence apply, then push operator.",
            'mechanics': "Read tokens left to right: (1) If number, push to values. (2) If '(', push to ops. (3) If "
                         "')', pop and apply operators until '(' is matched. (4) If operator (+, -, *, /): while top "
                         'of ops has >= precedence, pop and apply. Push current operator. At end, apply remaining '
                         'operators in ops. Evaluates expressions in strictly O(N) time.',
            'patterns': ['3 + 2 * 2 = 7', '(1 + (4 + 5 + 2) - 3) = 9'],
            'practice_task': 'Evaluate a mathematical expression containing +, -, *, and parentheses.',
            'q1': 'Why does the Shunting-Yard algorithm pop and evaluate existing operators when encountering a new '
                  'operator of LOWER or EQUAL precedence?',
            'q1_ans': 'A',
            'q1_exp': {   'A': 'Correct! E.g. in `2 * 3 + 4`, when encountering `+` (precedence 1), the waiting `*` '
                               '(precedence 2) has higher precedence and must be evaluated (`2 * 3 = 6`) before `+` '
                               'can be stored.',
                          'B': 'Incorrect: Operator stacks can grow to arbitrary depth.',
                          'C': 'Incorrect: Precedence enforcement is syntactic.',
                          'D': 'Incorrect: Parentheses create isolated precedence scopes.'},
            'q1_opts': [   {   'id': 'A',
                               'label': 'Higher or equal precedence operators already waiting on the stack must be '
                                        'evaluated immediately because their binding to preceding numbers is now '
                                        'complete'},
                           {'id': 'B', 'label': 'Because stacks can only hold 2 operators'},
                           {'id': 'C', 'label': 'To prevent numbers from overflowing'},
                           {'id': 'D', 'label': 'Because parenthesis matching requires empty operator stacks'}],
            'q2': 'What is the time complexity of evaluating an arithmetic expression string of length N using the '
                  'Shunting-Yard algorithm?',
            'q2_ans': 'A',
            'q2_exp': {   'A': 'Correct! Every token is pushed onto the operand or operator stack once and popped at '
                               'most once. Total operations are proportional to N.',
                          'B': 'Incorrect: Stack passes do not re-scan the string.',
                          'C': 'Incorrect: Shunting-Yard is strictly polynomial linear.',
                          'D': 'Incorrect: No sorting or divide-and-conquer is involved.'},
            'q2_opts': [   {   'id': 'A',
                               'label': 'O(N) linear time, because each character, number, and operator is pushed and '
                                        'popped at most once'},
                           {'id': 'B', 'label': 'O(N^2) quadratic time'},
                           {'id': 'C', 'label': 'O(2^N) exponential time'},
                           {'id': 'D', 'label': 'O(N log N) time'}],
            'recap': [   {   'concept': 'Operator Precedence Invariant',
                             'naiveIntuition': 'Evaluate expressions strictly left-to-right',
                             'pythonReality': 'Stack-based precedence deferral guarantees that multiplication and '
                                              'division resolve before addition and subtraction'},
                         {   'concept': 'Syntactic Stack Scoping',
                             'naiveIntuition': 'Parentheses require recursive parsing',
                             'pythonReality': "Pushing '(' onto the operator stack scopes precedence evaluation "
                                              'without needing recursion'}],
            'sample_code': '# Basic Calculator Expression Evaluator\n'
                           'def calculate(s):\n'
                           '    vals, ops = [], []\n'
                           "    prec = {'+': 1, '-': 1, '*': 2, '/': 2}\n"
                           '    def apply():\n'
                           '        op = ops.pop(); b = vals.pop(); a = vals.pop()\n'
                           "        if op == '+': vals.append(a + b)\n"
                           "        elif op == '-': vals.append(a - b)\n"
                           "        elif op == '*': vals.append(a * b)\n"
                           "        elif op == '/': vals.append(int(a / b))\n"
                           '    i = 0\n'
                           '    while i < len(s):\n'
                           '        if s[i].isdigit():\n'
                           '            n = 0\n'
                           '            while i < len(s) and s[i].isdigit(): n = n * 10 + int(s[i]); i += 1\n'
                           '            vals.append(n); continue\n'
                           '        elif s[i] in prec:\n'
                           '            while ops and ops[-1] in prec and prec[ops[-1]] >= prec[s[i]]: apply()\n'
                           '            ops.append(s[i])\n'
                           "        elif s[i] == '(': ops.append('(')\n"
                           "        elif s[i] == ')':\n"
                           "            while ops[-1] != '(': apply()\n"
                           '            ops.pop()\n'
                           '        i += 1\n'
                           '    while ops: apply()\n'
                           '    return vals[0]',
            'solution': 'def eval_expression(s: str) -> int:\n'
                        '    vals, ops = [], []\n'
                        "    prec = {'+': 1, '-': 1, '*': 2, '/': 2}\n"
                        '    def apply():\n'
                        '        op = ops.pop()\n'
                        '        b = vals.pop()\n'
                        '        a = vals.pop()\n'
                        "        if op == '+':\n"
                        '            vals.append(a + b)\n'
                        "        elif op == '-':\n"
                        '            vals.append(a - b)\n'
                        "        elif op == '*':\n"
                        '            vals.append(a * b)\n'
                        "        elif op == '/':\n"
                        '            vals.append(int(a / b))\n'
                        '    i = 0\n'
                        '    while i < len(s):\n'
                        "        if s[i] == ' ':\n"
                        '            i += 1\n'
                        '            continue\n'
                        '        if s[i].isdigit():\n'
                        '            n = 0\n'
                        '            while i < len(s) and s[i].isdigit():\n'
                        '                n = n * 10 + int(s[i])\n'
                        '                i += 1\n'
                        '            vals.append(n)\n'
                        '            continue\n'
                        "        elif s[i] == '(':\n"
                        "            ops.append('(')\n"
                        "        elif s[i] == ')':\n"
                        "            while ops and ops[-1] != '(':\n"
                        '                apply()\n'
                        "            if ops and ops[-1] == '(':\n"
                        '                ops.pop()\n'
                        '        elif s[i] in prec:\n'
                        '            while ops and ops[-1] in prec and prec[ops[-1]] >= prec[s[i]]:\n'
                        '                apply()\n'
                        '            ops.append(s[i])\n'
                        '        i += 1\n'
                        '    while ops:\n'
                        '        apply()\n'
                        '    return vals[0] if vals else 0\n'
                        '\n'
                        "print('3 + 2 * 2 =', eval_expression('3 + 2 * 2'))\n"
                        "print('(1 + (4 + 5 + 2) - 3) =', eval_expression('(1 + (4 + 5 + 2) - 3)'))\n",
            'starter': 'def eval_expression(s: str) -> int:\n'
                       '    # TODO: Implement Shunting-Yard / 2-stack expression evaluator\n'
                       '    return 0\n'
                       '\n'
                       "print('3 + 2 * 2 =', eval_expression('3 + 2 * 2'))       # 7\n"
                       "print('(1 + (4 + 5 + 2) - 3) =', eval_expression('(1 + (4 + 5 + 2) - 3)')) # 9\n",
            'summary': 'The Shunting-Yard Algorithm parses infix mathematical expressions into Postfix (Reverse Polish '
                       'Notation) or directly evaluates them using an Operator Stack and Operand Stack.',
            'takeaway': 'Operator precedence stacks ensure high-precedence operations (*, /) execute before '
                        'lower-precedence ones (+, -).'},
    95: {   'hint': 'Initialize res = [0] * len(temps), stack = []. Loop i, t: while stack and temps[stack[-1]] < t: '
                    'prev = stack.pop(); res[prev] = i - prev. stack.append(i). Return res.',
            'mechanics': 'Framework: (1) Does order require matching nested pairs or undo history? Use Stack. (2) Does '
                         'order require temporal arrival or breadth-first exploration? Use Queue. (3) Does the problem '
                         'ask for next greater/smaller element? Use Monotonic Stack. (4) Does the problem ask for '
                         'sliding window extremum? Use Monotonic Deque.',
            'patterns': ['Daily temps: [1, 1, 4, 2, 1, 1, 0, 0]'],
            'practice_task': 'Solve Daily Temperatures: return an array where answer[i] is days until warmer '
                             'temperature.',
            'q1': 'Which data structure is optimal for finding the daily temperature span (number of days until a '
                  'warmer day)?',
            'q1_ans': 'A',
            'q1_exp': {   'A': 'Correct! Daily temperatures is an exact Next Greater Element archetype. Maintaining a '
                               "monotonic decreasing stack of indices resolves each day's span in amortized O(N) time.",
                          'B': 'Incorrect: Circular queue does not maintain sorted temperature ordering.',
                          'C': 'Incorrect: BST has higher overhead and tree balancing complexity.',
                          'D': 'Incorrect: Quadratic loop times out on large inputs.'},
            'q1_opts': [   {'id': 'A', 'label': 'Monotonic Decreasing Stack storing day indices in O(N) time'},
                           {'id': 'B', 'label': 'Circular Queue in O(N^2) time'},
                           {'id': 'C', 'label': 'Binary Search Tree in O(N log N) time'},
                           {'id': 'D', 'label': 'Nested for loops in O(N^2) time'}],
            'q2': 'When building an operating system process scheduler where tasks must be serviced strictly in '
                  'arrival order, which discipline is required?',
            'q2_ans': 'A',
            'q2_exp': {   'A': 'Correct! First-In, First-Out guarantees starvation-free fairness by executing tasks in '
                               'the exact order they were enqueued.',
                          'B': 'Incorrect: LIFO starves older processes indefinitely.',
                          'C': 'Incorrect: Monotonic stacks do not maintain FIFO arrival ordering.',
                          'D': 'Incorrect: Raw arrays require O(N) removal from front.'},
            'q2_opts': [   {'id': 'A', 'label': 'FIFO Queue discipline'},
                           {'id': 'B', 'label': 'LIFO Stack discipline'},
                           {'id': 'C', 'label': 'Monotonic Stack discipline'},
                           {'id': 'D', 'label': 'Random Access Array'}],
            'recap': [   {   'concept': 'Index Difference Span',
                             'naiveIntuition': 'Store temperatures directly in the stack',
                             'pythonReality': 'Storing day indices allows computing both the value comparison and the '
                                              'time distance i - prev in O(1)'},
                         {   'concept': 'Section 8 Synthesis',
                             'naiveIntuition': 'Linear data structures only store raw data',
                             'pythonReality': 'Stack and queue disciplines impose invariant orders that enable '
                                              'amortized O(N) algorithms for complex span and area problems'}],
            'sample_code': '# Linear Discipline Selection Matrix:\n'
                           '# LIFO -> Stack (Backtracking, Syntax, Call Stack)\n'
                           '# FIFO -> Queue (BFS, Buffers, Scheduling)\n'
                           '# Extremum -> Monotonic Stack / Monotonic Deque',
            'solution': 'def daily_temperatures(temps: list[int]) -> list[int]:\n'
                        '    res = [0] * len(temps)\n'
                        '    stack = []\n'
                        '    for i, t in enumerate(temps):\n'
                        '        while stack and temps[stack[-1]] < t:\n'
                        '            prev_idx = stack.pop()\n'
                        '            res[prev_idx] = i - prev_idx\n'
                        '        stack.append(i)\n'
                        '    return res\n'
                        '\n'
                        "print('Daily temps:', daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]))\n",
            'starter': 'def daily_temperatures(temps: list[int]) -> list[int]:\n'
                       '    # TODO: Use a monotonic stack of indices\n'
                       '    # Compute days until warmer temperature for each day\n'
                       '    return []\n'
                       '\n'
                       "print('Daily temps:', daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]))\n",
            'summary': 'Section 8 Review synthesizes LIFO stacks, FIFO queues, circular ring buffers, min stacks, '
                       'monotonic stacks, and sliding window deques into an algorithmic decision framework.',
            'takeaway': 'Selecting the correct linear discipline reduces complex quadratic search spaces into '
                        'amortized O(N) linear scans.'}}
