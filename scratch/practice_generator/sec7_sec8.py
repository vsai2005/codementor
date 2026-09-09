"""
Practice Problems for Section 7 (Linked Lists) and Section 8 (Stacks & Queues)
Total problems: 14
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

SEC7_SEC8_PROBLEMS = [
    # --- Section 7: Linked Lists (Days 76-85) ---
    P(
        "delete-node-linked-list", "Delete Node in a Linked List", "linked-lists", 1, "delete_node_in_list",
        "Given an array `values` representing a singly linked list and an integer `val` to delete (guaranteed not to be the tail), simulate deleting the node by overwriting its value and splicing out its next pointer. Return the resulting linked list as an array.",
        "- `2 <= len(values) <= 1000`\n- `val` is present in `values` and is not the last element",
        "O(n)", "O(1)",
        "def delete_node_in_list(values: list[int], val: int) -> list[int]:\n    pass\n",
        [
            {"args": [[4, 5, 1, 9], 5], "expected": [4, 1, 9]},
            {"args": [[4, 5, 1, 9], 1], "expected": [4, 5, 9]},
            {"args": [[1, 2], 1], "expected": [2]},
            {"args": [[0, 1, 2], 1], "expected": [0, 2]}
        ],
        "def delete_node_in_list(values: list[int], val: int) -> list[int]:\n    # Simulate node deletion in-place\n    idx = values.index(val)\n    values[idx] = values[idx + 1]\n    del values[idx + 1]\n    return values\n"
    ),

    P(
        "remove-linked-list-elements", "Remove Linked List Elements (Dummy Sentinel)", "linked-lists", 2, "remove_elements",
        "Given an array `values` representing a linked list and an integer `val`, remove all nodes of the linked list that have `node.val == val`, and return the new list.\n\nUse a dummy sentinel node to handle head removals cleanly.",
        "- `0 <= len(values) <= 10^4`\n- `0 <= val <= 50`",
        "O(n)", "O(1)",
        "def remove_elements(values: list[int], val: int) -> list[int]:\n    pass\n",
        [
            {"args": [[1, 2, 6, 3, 4, 5, 6], 6], "expected": [1, 2, 3, 4, 5]},
            {"args": [[], 1], "expected": []},
            {"args": [[7, 7, 7, 7], 7], "expected": []},
            {"args": [[1, 2, 2, 1], 2], "expected": [1, 1]},
            {"args": [[1], 2], "expected": [1]}
        ],
        "def remove_elements(values: list[int], val: int) -> list[int]:\n    return [x for x in values if x != val]\n"
    ),

    P(
        "reverse-linked-list", "Reverse Linked List (Iterative 3-Pointer)", "linked-lists", 2, "reverse_list_nodes",
        "Given an array `values` representing a singly linked list, reverse the nodes using an iterative 3-pointer pattern (`prev`, `curr`, `next_temp`) in $O(N)$ time and $O(1)$ space. Return the reversed list.",
        "- `0 <= len(values) <= 5000`\n- `-5000 <= values[i] <= 5000`",
        "O(n)", "O(1)",
        "def reverse_list_nodes(values: list[int]) -> list[int]:\n    pass\n",
        [
            {"args": [[1, 2, 3, 4, 5]], "expected": [5, 4, 3, 2, 1]},
            {"args": [[1, 2]], "expected": [2, 1]},
            {"args": [[]], "expected": []},
            {"args": [[10]], "expected": [10]},
            {"args": [[-1, -2, -3]], "expected": [-3, -2, -1]}
        ],
        "def reverse_list_nodes(values: list[int]) -> list[int]:\n    # In-place 3-pointer node traversal simulation\n    left, right = 0, len(values) - 1\n    while left < right:\n        values[left], values[right] = values[right], values[left]\n        left += 1\n        right -= 1\n    return values\n"
    ),

    P(
        "middle-of-the-linked-list", "Middle of the Linked List (Fast & Slow)", "linked-lists", 1, "find_middle_node",
        "Given the array `values` of a singly linked list, return the values from the middle node to the end of the list.\n\nIf there are two middle nodes, return the second middle node (fast & slow runner pointer technique).",
        "- `1 <= len(values) <= 100`\n- `1 <= values[i] <= 100`",
        "O(n)", "O(1)",
        "def find_middle_node(values: list[int]) -> list[int]:\n    pass\n",
        [
            {"args": [[1, 2, 3, 4, 5]], "expected": [3, 4, 5]},
            {"args": [[1, 2, 3, 4, 5, 6]], "expected": [4, 5, 6]},
            {"args": [[1]], "expected": [1]},
            {"args": [[1, 2]], "expected": [2]},
            {"args": [[10, 20, 30, 40]], "expected": [30, 40]}
        ],
        "def find_middle_node(values: list[int]) -> list[int]:\n    slow = 0\n    fast = 0\n    while fast < len(values) and fast + 1 < len(values):\n        slow += 1\n        fast += 2\n    return values[slow:]\n"
    ),

    P(
        "linked-list-cycle", "Linked List Cycle Detection (Floyd's)", "linked-lists", 2, "has_cycle",
        "Given an array `values` and an integer `pos` representing the index that the tail connects back to (forming a cycle, or `-1` if no cycle), return `True` if there is a cycle in the linked list. Otherwise, return `False`.",
        "- `0 <= len(values) <= 10^4`\n- `-1 <= pos < len(values)`",
        "O(n)", "O(1)",
        "def has_cycle(values: list[int], pos: int) -> bool:\n    pass\n",
        [
            {"args": [[3, 2, 0, -4], 1], "expected": True},
            {"args": [[1, 2], 0], "expected": True},
            {"args": [[1], -1], "expected": False},
            {"args": [[], -1], "expected": False},
            {"args": [[1, 2, 3, 4], -1], "expected": False}
        ],
        "def has_cycle(values: list[int], pos: int) -> bool:\n    return pos != -1 and len(values) > 0\n"
    ),

    P(
        "linked-list-cycle-ii", "Linked List Cycle Entry Point", "linked-lists", 3, "detect_cycle_entry",
        "Given an array `values` and an index `pos` where the tail links back to, return the index of the node where the cycle begins. If there is no cycle, return `-1`.\n\nDerive the mathematical proof using Floyd's Tortoise and Hare algorithm.",
        "- `0 <= len(values) <= 10^4`\n- `-1 <= pos < len(values)`",
        "O(n)", "O(1)",
        "def detect_cycle_entry(values: list[int], pos: int) -> int:\n    pass\n",
        [
            {"args": [[3, 2, 0, -4], 1], "expected": 1},
            {"args": [[1, 2], 0], "expected": 0},
            {"args": [[1], -1], "expected": -1},
            {"args": [[1, 2, 3, 4, 5], 2], "expected": 2},
            {"args": [[], -1], "expected": -1}
        ],
        "def detect_cycle_entry(values: list[int], pos: int) -> int:\n    if not values or pos == -1:\n        return -1\n    return pos\n"
    ),

    P(
        "merge-two-sorted-linked-lists", "Merge Two Sorted Lists (Pointer Splicing)", "linked-lists", 2, "merge_two_lists",
        "You are given the heads of two sorted linked lists `list1` and `list2`. Merge the two lists into one sorted list by splicing together node pointers. Return the merged list.",
        "- `0 <= len(list1), len(list2) <= 50`\n- `-100 <= list1[i], list2[i] <= 100`",
        "O(n + m)", "O(1)",
        "def merge_two_lists(list1: list[int], list2: list[int]) -> list[int]:\n    pass\n",
        [
            {"args": [[1, 2, 4], [1, 3, 4]], "expected": [1, 1, 2, 3, 4, 4]},
            {"args": [[], []], "expected": []},
            {"args": [[], [0]], "expected": [0]},
            {"args": [[5], [1, 2, 3]], "expected": [1, 2, 3, 5]},
            {"args": [[2, 4, 6], [1, 3, 5]], "expected": [1, 2, 3, 4, 5, 6]}
        ],
        "def merge_two_lists(list1: list[int], list2: list[int]) -> list[int]:\n    i = j = 0\n    res = []\n    while i < len(list1) and j < len(list2):\n        if list1[i] <= list2[j]:\n            res.append(list1[i])\n            i += 1\n        else:\n            res.append(list2[j])\n            j += 1\n    res.extend(list1[i:])\n    res.extend(list2[j:])\n    return res\n"
    ),

    P(
        "remove-nth-node-from-end", "Remove Nth Node From End of List", "linked-lists", 2, "remove_nth_from_end",
        "Given an array `values` representing a linked list, remove the `n`th node from the end of the list and return the resulting list.\n\nUse dual pointers separated by `n` steps in a single pass.",
        "- `1 <= len(values) <= 1000`\n- `1 <= n <= len(values)`",
        "O(n)", "O(1)",
        "def remove_nth_from_end(values: list[int], n: int) -> list[int]:\n    pass\n",
        [
            {"args": [[1, 2, 3, 4, 5], 2], "expected": [1, 2, 3, 5]},
            {"args": [[1], 1], "expected": []},
            {"args": [[1, 2], 1], "expected": [1]},
            {"args": [[1, 2], 2], "expected": [2]},
            {"args": [[10, 20, 30, 40], 4], "expected": [20, 30, 40]}
        ],
        "def remove_nth_from_end(values: list[int], n: int) -> list[int]:\n    idx = len(values) - n\n    return values[:idx] + values[idx + 1:]\n"
    ),

    P(
        "reverse-nodes-in-k-group", "Reverse Nodes in k-Group", "linked-lists", 5, "reverse_k_group",
        "Given the array `values` of a linked list, reverse the nodes of the list `k` at a time, and return the modified list.\n\n`k` is a positive integer. If the number of nodes is not a multiple of `k` then left-out nodes at the end remain as-is.",
        "- `1 <= k <= len(values) <= 5000`\n- `0 <= values[i] <= 1000`",
        "O(n)", "O(1)",
        "def reverse_k_group(values: list[int], k: int) -> list[int]:\n    pass\n",
        [
            {"args": [[1, 2, 3, 4, 5], 2], "expected": [2, 1, 4, 3, 5]},
            {"args": [[1, 2, 3, 4, 5], 3], "expected": [3, 2, 1, 4, 5]},
            {"args": [[1, 2, 3, 4, 5], 1], "expected": [1, 2, 3, 4, 5]},
            {"args": [[1], 1], "expected": [1]},
            {"args": [[1, 2, 3, 4, 5, 6], 3], "expected": [3, 2, 1, 6, 5, 4]}
        ],
        "def reverse_k_group(values: list[int], k: int) -> list[int]:\n    res = []\n    for i in range(0, len(values), k):\n        chunk = values[i:i + k]\n        if len(chunk) == k:\n            res.extend(chunk[::-1])\n        else:\n            res.extend(chunk)\n    return res\n"
    ),

    P(
        "sort-list", "Sort Linked List (O(N log N) Merge Sort)", "linked-lists", 4, "sort_linked_list",
        "Given the array `values` of a linked list, return the list after sorting it in ascending order in $O(n \\log n)$ time and $O(1)$ space using linked list merge sort.",
        "- `0 <= len(values) <= 5 * 10^4`\n- `-10^5 <= values[i] <= 10^5`",
        "O(n log n)", "O(log n)",
        "def sort_linked_list(values: list[int]) -> list[int]:\n    pass\n",
        [
            {"args": [[4, 2, 1, 3]], "expected": [1, 2, 3, 4]},
            {"args": [[-1, 5, 3, 4, 0]], "expected": [-1, 0, 3, 4, 5]},
            {"args": [[]], "expected": []},
            {"args": [[1]], "expected": [1]},
            {"args": [[10, 1, 9, 2, 8, 3]], "expected": [1, 2, 3, 8, 9, 10]}
        ],
        "def sort_linked_list(values: list[int]) -> list[int]:\n    return sorted(values)\n"
    ),

    # --- Section 8: Stacks & Queues (Days 86-95) ---
    P(
        "design-circular-queue", "Design Circular Queue (Ring Buffer)", "stacks", 2, "simulate_circular_queue",
        "Simulate a circular FIFO queue of fixed `capacity`. Operations: `[['enq', val], ['deq'], ['front'], ['rear'], ['isEmpty'], ['isFull']]`. Return the list of return values.\n\nUse head/tail pointer modulo arithmetic.",
        "- `1 <= capacity <= 1000`\n- `0 <= val <= 1000`\n- At most `3000` calls",
        "O(1) per op", "O(capacity)",
        "def simulate_circular_queue(capacity: int, operations: list) -> list:\n    pass\n",
        [
            {"args": [3, [["enq", 1], ["enq", 2], ["enq", 3], ["enq", 4], ["rear"], ["isFull"], ["deq"], ["enq", 4], ["rear"]]],
             "expected": [True, True, True, False, 3, True, True, True, 4]},
            {"args": [2, [["enq", 1], ["deq"], ["isEmpty"], ["front"]]],
             "expected": [True, True, True, -1]}
        ],
        "def simulate_circular_queue(capacity: int, operations: list) -> list:\n    q = [0] * capacity\n    head = 0\n    count = 0\n    out = []\n    for op in operations:\n        cmd = op[0]\n        if cmd == 'enq':\n            val = op[1]\n            if count == capacity:\n                out.append(False)\n            else:\n                tail = (head + count) % capacity\n                q[tail] = val\n                count += 1\n                out.append(True)\n        elif cmd == 'deq':\n            if count == 0:\n                out.append(False)\n            else:\n                head = (head + 1) % capacity\n                count -= 1\n                out.append(True)\n        elif cmd == 'front':\n            out.append(-1 if count == 0 else q[head])\n        elif cmd == 'rear':\n            tail = (head + count - 1) % capacity\n            out.append(-1 if count == 0 else q[tail])\n        elif cmd == 'isEmpty':\n            out.append(count == 0)\n        elif cmd == 'isFull':\n            out.append(count == capacity)\n    return out\n"
    ),

    P(
        "implement-queue-using-stacks", "Implement Queue Using Two Stacks", "stacks", 2, "simulate_queue_via_stacks",
        "Implement a FIFO queue using only two LIFO stacks. Support `push(x)`, `pop()`, `peek()`, and `empty()`. Given an operations list `[['push', x], ['pop'], ['peek'], ['empty']]`, return the outputs list.",
        "- `1 <= x <= 9`\n- At most `100` calls to operations",
        "O(1) amortized", "O(n)",
        "def simulate_queue_via_stacks(operations: list) -> list:\n    pass\n",
        [
            {"args": [[["push", 1], ["push", 2], ["peek"], ["pop"], ["empty"]]],
             "expected": [None, None, 1, 1, False]},
            {"args": [[["push", 1], ["pop"], ["empty"]]],
             "expected": [None, 1, True]}
        ],
        "def simulate_queue_via_stacks(operations: list) -> list:\n    in_stack = []\n    out_stack = []\n    res = []\n    for op in operations:\n        cmd = op[0]\n        if cmd == 'push':\n            in_stack.append(op[1])\n            res.append(None)\n        elif cmd == 'pop':\n            if not out_stack:\n                while in_stack:\n                    out_stack.append(in_stack.pop())\n            res.append(out_stack.pop())\n        elif cmd == 'peek':\n            if not out_stack:\n                while in_stack:\n                    out_stack.append(in_stack.pop())\n            res.append(out_stack[-1])\n        elif cmd == 'empty':\n            res.append(len(in_stack) == 0 and len(out_stack) == 0)\n    return res\n"
    ),

    P(
        "sliding-window-maximum", "Sliding Window Maximum (Monotonic Deque)", "stacks", 4, "max_sliding_window",
        "You are given an array of integers `nums`, there is a sliding window of size `k` which is moving from the very left of the array to the very right. Return the max sliding window.\n\nYou must solve this in $O(N)$ linear time using a monotonic double-ended queue (`deque`).",
        "- `1 <= len(nums) <= 10^5`\n- `-10^4 <= nums[i] <= 10^4`\n- `1 <= k <= len(nums)`",
        "O(n)", "O(k)",
        "def max_sliding_window(nums: list[int], k: int) -> list[int]:\n    pass\n",
        [
            {"args": [[1, 3, -1, -3, 5, 3, 6, 7], 3], "expected": [3, 3, 5, 5, 6, 7]},
            {"args": [[1], 1], "expected": [1]},
            {"args": [[1, -1], 1], "expected": [1, -1]},
            {"args": [[9, 11], 2], "expected": [11]},
            {"args": [[4, -2], 2], "expected": [4]}
        ],
        "from collections import deque\n\ndef max_sliding_window(nums: list[int], k: int) -> list[int]:\n    d = deque()\n    res = []\n    for i in range(len(nums)):\n        while d and d[0] < i - k + 1:\n            d.popleft()\n        while d and nums[d[-1]] < nums[i]:\n            d.pop()\n        d.append(i)\n        if i >= k - 1:\n            res.append(nums[d[0]])\n    return res\n"
    ),

    P(
        "basic-calculator-ii", "Basic Calculator II (Operator Precedence)", "stacks", 3, "calculate",
        "Given a string `s` which represents an expression, evaluate this expression and return its value.\n\nThe integer divisions should truncate toward zero. `s` consists of integers and operators (`'+'`, `'-'`, `'*'`, `'/'`) separated by spaces.",
        "- `1 <= len(s) <= 3 * 10^5`\n- `s` consists of digits and `'+'`, `'-'`, `'*'`, `'/'` and whitespace",
        "O(n)", "O(n)",
        "def calculate(s: str) -> int:\n    pass\n",
        [
            {"args": ["3+2*2"], "expected": 7},
            {"args": [" 3/2 "], "expected": 1},
            {"args": [" 3+5 / 2 "], "expected": 5},
            {"args": ["14-3/2"], "expected": 13},
            {"args": ["100"], "expected": 100}
        ],
        "def calculate(s: str) -> int:\n    stack = []\n    curr = 0\n    op = '+'\n    s += '+'\n    for ch in s:\n        if ch.isdigit():\n            curr = curr * 10 + int(ch)\n        elif ch in '+-*/':\n            if op == '+':\n                stack.append(curr)\n            elif op == '-':\n                stack.append(-curr)\n            elif op == '*':\n                stack.append(stack.pop() * curr)\n            elif op == '/':\n                prev = stack.pop()\n                stack.append(int(prev / curr))\n            op = ch\n            curr = 0\n    return sum(stack)\n"
    )
]
