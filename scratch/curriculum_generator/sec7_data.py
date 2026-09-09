"""
Section 7: Linked Lists (Days 76 to 85)
Full authoring definitions for all 10 days with true practice archetypes,
distinguishable starter vs solution code, authentic 4-option MCQs with unique diagnostic explanations.
"""

SEC7_DAYS = {
    76: {
        "summary": "Singly Linked Lists chain individual ListNode objects via pointer references, trading array contiguous indexing for dynamic O(1) node insertion.",
        "mechanics": "Each node stores val and a next pointer reference. Traversal proceeds sequentially via curr = curr.next until reaching None. Unlike contiguous Python lists, linked list nodes are scattered across arbitrary heap memory addresses.",
        "takeaway": "Linked lists eliminate contiguous array resizing overhead but forfeit O(1) random index access.",
        "sample_code": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\nhead = ListNode(1, ListNode(2, ListNode(3)))\ncurr = head\nwhile curr:\n    print(curr.val, end=' -> ')\n    curr = curr.next\nprint('None')",
        "q1": "What is the primary memory difference between a Python list and a singly linked list?",
        "q1_opts": [
            {"id": "A", "label": "Python lists store contiguous arrays of memory pointers allowing O(1) indexing, whereas linked lists scatter nodes across heap memory connected via node.next references"},
            {"id": "B", "label": "Linked lists can only store strings while Python lists store numbers"},
            {"id": "C", "label": "Python lists consume zero memory when empty"},
            {"id": "D", "label": "Linked lists cannot be modified after creation"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! Contiguous memory allows hardware ALUs to compute base + index * pointer_size in O(1) time. Linked lists require sequential pointer hopping (curr = curr.next) taking O(N) to reach index N.",
            "B": "Incorrect: Both data structures can store any Python object.",
            "C": "Incorrect: Python list objects have fixed struct overhead.",
            "D": "Incorrect: Linked lists are mutable dynamic structures."
        },
        "q2": "What happens if a traversal loop executes curr = curr.next when curr is None?",
        "q2_opts": [
            {"id": "A", "label": "Python raises AttributeError: 'NoneType' object has no attribute 'next'"},
            {"id": "B", "label": "The loop terminates cleanly"},
            {"id": "C", "label": "Python automatically resets curr back to head"},
            {"id": "D", "label": "A circular reference is formed"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! Attempting to access an attribute on None immediately triggers an AttributeError. Guard loops with while curr:.",
            "B": "Incorrect: Dereferencing None raises an exception.",
            "C": "Incorrect: Python runtime does not infer head recovery.",
            "D": "Incorrect: No pointers are redirected."
        },
        "practice_task": "Construct a linked list from an array of integers and return the values collected during traversal.",
        "starter": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef build_and_traverse(values: list[int]) -> list[int]:\n    # TODO: Build singly linked list from values\n    # Traverse the list and collect all node.val into a result list\n    return []\n\nprint('Collected:', build_and_traverse([10, 20, 30, 40]))\n",
        "solution": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef build_and_traverse(values: list[int]) -> list[int]:\n    if not values:\n        return []\n    head = ListNode(values[0])\n    curr = head\n    for v in values[1:]:\n        curr.next = ListNode(v)\n        curr = curr.next\n    \n    result = []\n    curr = head\n    while curr:\n        result.append(curr.val)\n        curr = curr.next\n    return result\n\nprint('Collected:', build_and_traverse([10, 20, 30, 40]))\n",
        "patterns": ["Collected: [10, 20, 30, 40]"],
        "hint": "Create head = ListNode(values[0]). Loop through remaining items, attach curr.next = ListNode(v), and advance curr = curr.next.",
        "recap": [
            {"concept": "Pointer Sequentiality", "naiveIntuition": "Access node k with list[k]", "pythonReality": "Linked lists require sequential traversal through k next pointers in O(K) time"},
            {"concept": "Dynamic Allocation", "naiveIntuition": "Linked lists require continuous memory blocks", "pythonReality": "Nodes exist independently in heap memory, connected solely by reference pointers"}
        ]
    },
    77: {
        "summary": "Insertion and Deletion in singly linked lists mutate .next pointers, with Dummy Sentinels (dummy = ListNode(0, head)) elegantly eliminating head edge cases.",
        "mechanics": "Inserting after node curr requires: new_node.next = curr.next; curr.next = new_node. Deleting target after curr: curr.next = curr.next.next. Dummy sentinels prevent special-case branching when operating on index 0.",
        "takeaway": "Using a dummy head sentinel unifies edge-case operations at head, middle, and tail.",
        "sample_code": "# Deleting target value with dummy sentinel\ndef remove_elements(head, target):\n    dummy = ListNode(0, head)\n    curr = dummy\n    while curr.next:\n        if curr.next.val == target:\n            curr.next = curr.next.next\n        else:\n            curr = curr.next\n    return dummy.next",
        "q1": "Why does using a dummy node (dummy = ListNode(0, head)) simplify node deletion algorithms?",
        "q1_opts": [
            {"id": "A", "label": "It guarantees that every node to be evaluated (including the original head) has a non-null predecessor node curr"},
            {"id": "B", "label": "It reduces the algorithmic time complexity from O(N) to O(1)"},
            {"id": "C", "label": "It prevents memory garbage collection"},
            {"id": "D", "label": "It automatically sorts the linked list"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! Without a dummy node, deleting the head node requires distinct head = head.next branching. A dummy sentinel ensures every node has a preceding node curr such that curr.next = curr.next.next works uniformly.",
            "B": "Incorrect: Traversal still requires O(N) time.",
            "C": "Incorrect: Unreferenced deleted nodes are cleanly garbage-collected.",
            "D": "Incorrect: Sentinels have no effect on element order."
        },
        "q2": "What is the critical order of operations when inserting new_node after curr?",
        "q2_opts": [
            {"id": "A", "label": "Set new_node.next = curr.next FIRST, then set curr.next = new_node"},
            {"id": "B", "label": "Set curr.next = new_node FIRST, then set new_node.next = curr.next"},
            {"id": "C", "label": "Order does not matter in Python"},
            {"id": "D", "label": "Delete curr first"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! If you set curr.next = new_node first, you overwrite the reference to the subsequent nodes, permanently orphaning the rest of the list.",
            "B": "Incorrect: This results in new_node.next = new_node, creating an infinite self-cycle and dropping remaining nodes.",
            "C": "Incorrect: Reference assignment order is strictly sequential in imperative execution.",
            "D": "Incorrect: Deleting curr destroys the insertion anchor."
        },
        "practice_task": "Use a dummy sentinel to delete all nodes matching a target value.",
        "starter": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef remove_all_val(head: ListNode, target: int) -> list[int]:\n    # TODO: Initialize dummy = ListNode(0, head)\n    # Delete all nodes where node.val == target\n    # Return values of remaining list as a Python list\n    return []\n\n# 1 -> 2 -> 6 -> 3 -> 6 -> None (remove 6)\nh = ListNode(1, ListNode(2, ListNode(6, ListNode(3, ListNode(6)))))\nprint('Remaining:', remove_all_val(h, 6))\n",
        "solution": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef remove_all_val(head: ListNode, target: int) -> list[int]:\n    dummy = ListNode(0, head)\n    curr = dummy\n    while curr.next:\n        if curr.next.val == target:\n            curr.next = curr.next.next\n        else:\n            curr = curr.next\n    \n    res = []\n    node = dummy.next\n    while node:\n        res.append(node.val)\n        node = node.next\n    return res\n\nh = ListNode(1, ListNode(2, ListNode(6, ListNode(3, ListNode(6)))))\nprint('Remaining:', remove_all_val(h, 6))\n",
        "patterns": ["Remaining: [1, 2, 3]"],
        "hint": "dummy = ListNode(0, head); curr = dummy. While curr.next: if curr.next.val == target: curr.next = curr.next.next else: curr = curr.next. Return traversed dummy.next.",
        "recap": [
            {"concept": "Sentinel Utility", "naiveIntuition": "Handle head deletion with if head.val == target: head = head.next", "pythonReality": "Dummy nodes eliminate repetitive edge-case branches by guaranteeing every active node has a valid predecessor"},
            {"concept": "Unlinking Garbage Collection", "naiveIntuition": "Deleted nodes remain in memory forever", "pythonReality": "In CPython, reference count drops to 0 when unlinked, automatically freeing memory"}
        ]
    },
    78: {
        "summary": "In-Place Linked List Reversal reverses all .next pointers in O(N) time and O(1) space using three iterative pointers: prev, curr, and next_node.",
        "mechanics": "At each step, cache next_node = curr.next, redirect curr.next = prev, then shift window: prev = curr and curr = next_node. At loop termination (curr is None), prev points to the new head.",
        "takeaway": "Three-pointer reversal modifies links in-place with O(1) auxiliary space.",
        "sample_code": "# Iterative in-place reversal\ndef reverse_list(head):\n    prev = None\n    curr = head\n    while curr:\n        nxt = curr.next\n        curr.next = prev\n        prev = curr\n        curr = nxt\n    return prev",
        "q1": "What is the role of nxt = curr.next in the three-pointer reversal loop?",
        "q1_opts": [
            {"id": "A", "label": "It temporarily saves the pointer to the rest of the unreversed list before curr.next is overwritten"},
            {"id": "B", "label": "It reverses the tail pointer"},
            {"id": "C", "label": "It allocates a new node on the heap"},
            {"id": "D", "label": "It checks if the list contains duplicates"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! As soon as curr.next = prev is executed, the forward reference to the next node is severed. Without caching nxt = curr.next beforehand, the remainder of the list becomes unreachable.",
            "B": "Incorrect: It does not operate on the tail.",
            "C": "Incorrect: No memory is allocated.",
            "D": "Incorrect: It does not evaluate values."
        },
        "q2": "What node reference should be returned as the new head after the reversal loop terminates?",
        "q2_opts": [
            {"id": "A", "label": "prev, because curr has become None and prev holds the former tail"},
            {"id": "B", "label": "curr, because it marks the end of the loop"},
            {"id": "C", "label": "head, because it retains the original starting pointer"},
            {"id": "D", "label": "dummy.next"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! When curr reaches None, prev points to the last processed node (the former tail), which is now the new head.",
            "B": "Incorrect: curr is None upon loop exit.",
            "C": "Incorrect: head is now the terminal tail node pointing to None.",
            "D": "Incorrect: No dummy node was used in standard three-pointer reversal."
        },
        "practice_task": "Reverse a singly linked list in-place and return the reversed node values.",
        "starter": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef reverse_and_collect(head: ListNode) -> list[int]:\n    # TODO: Implement three-pointer in-place reversal\n    # Return values of the reversed list\n    return []\n\n# 1 -> 2 -> 3 -> 4 -> 5 -> None\nh = ListNode(1, ListNode(2, ListNode(3, ListNode(4, ListNode(5)))))\nprint('Reversed:', reverse_and_collect(h))\n",
        "solution": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef reverse_and_collect(head: ListNode) -> list[int]:\n    prev = None\n    curr = head\n    while curr:\n        nxt = curr.next\n        curr.next = prev\n        prev = curr\n        curr = nxt\n    \n    res = []\n    node = prev\n    while node:\n        res.append(node.val)\n        node = node.next\n    return res\n\nh = ListNode(1, ListNode(2, ListNode(3, ListNode(4, ListNode(5)))))\nprint('Reversed:', reverse_and_collect(h))\n",
        "patterns": ["Reversed: [5, 4, 3, 2, 1]"],
        "hint": "prev = None, curr = head. While curr: nxt = curr.next; curr.next = prev; prev = curr; curr = nxt. Return values starting from prev.",
        "recap": [
            {"concept": "Pointer Inversion Invariant", "naiveIntuition": "Copy nodes into a new reversed list", "pythonReality": "In-place three-pointer reversal mutates pointers directly in O(1) auxiliary space with zero heap re-allocation"},
            {"concept": "Loop Termination Bound", "naiveIntuition": "Stop when curr.next is None", "pythonReality": "Stopping at while curr: ensures the final node is also processed and reversed into prev"}
        ]
    },
    79: {
        "summary": "Fast and Slow Pointers (Tortoise and Hare) traverse lists at 1x and 2x speeds, locating list midpoints in a single pass and detecting cycles.",
        "mechanics": "While fast and fast.next: slow = slow.next and fast = fast.next.next. When fast reaches the end, slow is exactly at the middle node (index N // 2).",
        "takeaway": "Advancing fast twice as fast as slow finds the exact midpoint in a single O(N) pass.",
        "sample_code": "# Find middle node\ndef find_middle(head):\n    slow = fast = head\n    while fast and fast.next:\n        slow = slow.next\n        fast = fast.next.next\n    return slow",
        "q1": "For an even-length list (e.g. 1 -> 2 -> 3 -> 4 -> None), which node will slow point to when using while fast and fast.next?",
        "q1_opts": [
            {"id": "A", "label": "The second middle node (node with value 3, index 2)"},
            {"id": "B", "label": "The first middle node (node with value 2, index 1)"},
            {"id": "C", "label": "The head node (value 1)"},
            {"id": "D", "label": "The tail node (value 4)"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! Initially slow=1, fast=1. Step 1: slow=2, fast=3. Step 2: slow=3, fast=None. Loop terminates because fast is None. Slow rests on the second middle node (3).",
            "B": "Incorrect: To stop at the first middle node, the loop condition must be while fast.next and fast.next.next:.",
            "C": "Incorrect: Slow advances on every iteration.",
            "D": "Incorrect: Slow only travels half distance."
        },
        "q2": "Why must the loop guard check both fast AND fast.next?",
        "q2_opts": [
            {"id": "A", "label": "To prevent an AttributeError when computing fast.next.next if fast or fast.next is None"},
            {"id": "B", "label": "Because slow pointer might be None"},
            {"id": "C", "label": "To handle negative values in nodes"},
            {"id": "D", "label": "To prevent stack overflow"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! If fast is None, fast.next raises an exception. If fast.next is None, fast.next.next raises an exception. Checking both ensures safe 2-step jumping.",
            "B": "Incorrect: Slow lags behind fast and is never None before fast.",
            "C": "Incorrect: Values do not influence traversal.",
            "D": "Incorrect: Iterative loops do not consume stack frames."
        },
        "practice_task": "Locate the middle element of a linked list using fast and slow pointers.",
        "starter": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef get_middle_val(head: ListNode) -> int:\n    # TODO: Advance slow 1 step and fast 2 steps\n    # Return the val of the middle node\n    return -1\n\n# 10 -> 20 -> 30 -> 40 -> 50 -> None\nh = ListNode(10, ListNode(20, ListNode(30, ListNode(40, ListNode(50)))))\nprint('Middle value:', get_middle_val(h))\n",
        "solution": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef get_middle_val(head: ListNode) -> int:\n    slow = fast = head\n    while fast and fast.next:\n        slow = slow.next\n        fast = fast.next.next\n    return slow.val if slow else -1\n\nh = ListNode(10, ListNode(20, ListNode(30, ListNode(40, ListNode(50)))))\nprint('Middle value:', get_middle_val(h))\n",
        "patterns": ["Middle value: 30"],
        "hint": "slow = fast = head. While fast and fast.next: slow = slow.next; fast = fast.next.next. Return slow.val.",
        "recap": [
            {"concept": "Single-Pass Midpoint", "naiveIntuition": "Count length N first, then traverse N//2 steps", "pythonReality": "Fast/slow pointers find the exact midpoint in a single O(N) pass without two full traversals"},
            {"concept": "Speed Ratio Invariant", "naiveIntuition": "Fast pointer might skip over slow without meeting", "pythonReality": "In discrete cycles, relative speed of 1 step/iteration guarantees fast catches slow without jumping past"}
        ]
    },
    80: {
        "summary": "Floyd's Cycle Detection Algorithm detects cycles and locates cycle entry points using relative speed convergence and modular arithmetic proof.",
        "mechanics": "If a cycle of length C exists and head is distance F from cycle entry: when slow and fast meet at distance 'a' into the cycle, fast has traveled 2*dist(slow). Math proof: 2(F + a) = F + a + k*C => F = k*C - a. Resetting slow to head and advancing both at 1x speed makes them collide exactly at the cycle entry node!",
        "takeaway": "Floyd's algorithm proves cycle existence and pinpoints cycle entry in O(N) time and O(1) space.",
        "sample_code": "# Floyd's Cycle Entry Detection\ndef detect_cycle_entry(head):\n    slow = fast = head\n    while fast and fast.next:\n        slow = slow.next\n        fast = fast.next.next\n        if slow == fast:\n            slow = head\n            while slow != fast:\n                slow = slow.next\n                fast = fast.next\n            return slow\n    return None",
        "q1": "Why does resetting slow to head and advancing both pointers at 1 step/iteration guarantee they meet at the cycle entry?",
        "q1_opts": [
            {"id": "A", "label": "Because the distance from head to entry (F) is mathematically equal to the distance from meeting point to entry traversing forward (k*C - a)"},
            {"id": "B", "label": "Because fast pointer moves backwards"},
            {"id": "C", "label": "Because the cycle length is always prime"},
            {"id": "D", "label": "Because slow pointer runs twice as fast in Phase 2"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! Derived from 2(F + a) = F + a + kC => F = kC - a. Pointers starting at head and meeting point will meet after exactly F steps, which is the entrance node.",
            "B": "Incorrect: Linked list pointers only advance forward.",
            "C": "Incorrect: Cycle length can be any positive integer.",
            "D": "Incorrect: Both pointers move at exactly 1 step/iteration in Phase 2."
        },
        "q2": "What is the auxiliary space complexity of Floyd's Cycle Algorithm compared to a HashSet visited approach?",
        "q2_opts": [
            {"id": "A", "label": "Floyd's uses O(1) space, whereas a HashSet approach consumes O(N) memory to record visited node IDs"},
            {"id": "B", "label": "Both consume O(N) auxiliary space"},
            {"id": "C", "label": "Floyd's consumes O(N^2) space"},
            {"id": "D", "label": "HashSet uses O(1) space"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! Floyd's algorithm tracks only two pointers (slow and fast), requiring strictly O(1) space without allocating hash set structures.",
            "B": "Incorrect: Floyd's allocates no additional collections.",
            "C": "Incorrect: Pointer manipulation is strictly O(1).",
            "D": "Incorrect: Storing N node addresses in a set requires O(N) space."
        },
        "practice_task": "Detect if a cycle exists in a linked list and return True or False.",
        "starter": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef has_cycle(head: ListNode) -> bool:\n    # TODO: Implement Phase 1 of Floyd's cycle detection\n    return False\n\n# Create list with cycle: 1 -> 2 -> 3 -> 4 -> points back to 2\nn1 = ListNode(1); n2 = ListNode(2); n3 = ListNode(3); n4 = ListNode(4)\nn1.next = n2; n2.next = n3; n3.next = n4; n4.next = n2\nprint('Has cycle:', has_cycle(n1))\n",
        "solution": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef has_cycle(head: ListNode) -> bool:\n    slow = fast = head\n    while fast and fast.next:\n        slow = slow.next\n        fast = fast.next.next\n        if slow == fast:\n            return True\n    return False\n\nn1 = ListNode(1); n2 = ListNode(2); n3 = ListNode(3); n4 = ListNode(4)\nn1.next = n2; n2.next = n3; n3.next = n4; n4.next = n2\nprint('Has cycle:', has_cycle(n1))\n",
        "patterns": ["Has cycle: True"],
        "hint": "slow = fast = head. While fast and fast.next: slow = slow.next; fast = fast.next.next; if slow == fast: return True. If loop finishes, return False.",
        "recap": [
            {"concept": "Relative Speed Reduction", "naiveIntuition": "Fast might jump over slow", "pythonReality": "Fast gains exactly 1 step on slow per iteration, making collision mathematically inevitable in any cycle"},
            {"concept": "Floyd Entry Invariant", "naiveIntuition": "Meeting point is always the cycle entry", "pythonReality": "Meeting point is inside the cycle; resetting slow to head and walking at 1x speed locates the entry node"}
        ]
    },
    81: {
        "summary": "Merging Sorted Lists splices existing nodes into non-decreasing order using a dummy head sentinel and two pointers, running in O(N + M) time and O(1) extra space.",
        "mechanics": "Initialize dummy = ListNode(0), curr = dummy. Compare l1.val and l2.val, attach smaller node to curr.next, and advance corresponding pointer. When one list empties, splice the remaining sublist directly via curr.next = l1 or l2.",
        "takeaway": "Splicing existing node references merges sorted lists without creating new node objects.",
        "sample_code": "# Merge two sorted lists\ndef merge_two_lists(l1, l2):\n    dummy = ListNode(0)\n    curr = dummy\n    while l1 and l2:\n        if l1.val <= l2.val:\n            curr.next = l1; l1 = l1.next\n        else:\n            curr.next = l2; l2 = l2.next\n        curr = curr.next\n    curr.next = l1 or l2\n    return dummy.next",
        "q1": "Why is curr.next = l1 or l2 sufficient when the loop while l1 and l2: terminates?",
        "q1_opts": [
            {"id": "A", "label": "Because the remaining non-empty list is already sorted and can be attached as an entire contiguous chain in O(1) time"},
            {"id": "B", "label": "Because both lists are guaranteed to be empty"},
            {"id": "C", "label": "To trigger list reversal"},
            {"id": "D", "label": "Because Python automatically merges remaining nodes"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! Unlike arrays where remaining elements must be copied one by one, a linked list's remaining nodes are already chained together; splicing the pointer takes O(1) time.",
            "B": "Incorrect: One list still contains remaining elements.",
            "C": "Incorrect: No reversal occurs.",
            "D": "Incorrect: Splicing is an explicit assignment of references."
        },
        "q2": "What is the total time complexity of merging two sorted linked lists of lengths N and M?",
        "q2_opts": [
            {"id": "A", "label": "O(N + M)"},
            {"id": "B", "label": "O(N * M)"},
            {"id": "C", "label": "O(log(N + M))"},
            {"id": "D", "label": "O(1)"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! Each comparison advances either pointer l1 or l2 by one node. At most N + M comparisons occur.",
            "B": "Incorrect: Nested comparison is not needed because both inputs are sorted.",
            "C": "Incorrect: Cannot inspect all elements in logarithmic time.",
            "D": "Incorrect: Every node must be visited."
        },
        "practice_task": "Merge two sorted linked lists into a single sorted list and collect values.",
        "starter": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef merge_and_collect(l1: ListNode, l2: ListNode) -> list[int]:\n    # TODO: Merge l1 and l2 using a dummy sentinel\n    # Return values in sorted order\n    return []\n\n# l1: 1 -> 3 -> 5; l2: 2 -> 4 -> 6\nl1 = ListNode(1, ListNode(3, ListNode(5)))\nl2 = ListNode(2, ListNode(4, ListNode(6)))\nprint('Merged:', merge_and_collect(l1, l2))\n",
        "solution": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef merge_and_collect(l1: ListNode, l2: ListNode) -> list[int]:\n    dummy = ListNode(0)\n    curr = dummy\n    while l1 and l2:\n        if l1.val <= l2.val:\n            curr.next = l1\n            l1 = l1.next\n        else:\n            curr.next = l2\n            l2 = l2.next\n        curr = curr.next\n    curr.next = l1 or l2\n    \n    res = []\n    node = dummy.next\n    while node:\n        res.append(node.val)\n        node = node.next\n    return res\n\nl1 = ListNode(1, ListNode(3, ListNode(5)))\nl2 = ListNode(2, ListNode(4, ListNode(6)))\nprint('Merged:', merge_and_collect(l1, l2))\n",
        "patterns": ["Merged: [1, 2, 3, 4, 5, 6]"],
        "hint": "dummy = ListNode(0); curr = dummy. While l1 and l2: attach smaller node, advance that list and curr. Splicing remaining: curr.next = l1 or l2. Return traversed dummy.next.",
        "recap": [
            {"concept": "Pointer Splicing", "naiveIntuition": "Create brand new nodes for merged list", "pythonReality": "Re-wiring existing node pointers merges lists in O(1) auxiliary space without memory allocations"},
            {"concept": "Residual Chain Attachment", "naiveIntuition": "Loop through all remaining nodes one by one", "pythonReality": "Attaching the head of the non-empty list links all remaining nodes in a single O(1) assignment"}
        ]
    },
    82: {
        "summary": "Doubly Linked Lists (DLL) equip nodes with both prev and next pointers, enabling true O(1) deletion and insertion at arbitrary positions given a direct node reference.",
        "mechanics": "Node deletion: node.prev.next = node.next; node.next.prev = node.prev. By placing permanent dummy head and tail sentinels, head and tail boundary checks vanish completely.",
        "takeaway": "DLLs provide O(1) deletion of any node given its reference, forming the foundation of LRU caches.",
        "sample_code": "class DLLNode:\n    def __init__(self, key=0, val=0):\n        self.key = key; self.val = val\n        self.prev = None; self.next = None\n\nhead = DLLNode(); tail = DLLNode()\nhead.next = tail; tail.prev = head",
        "q1": "Why is node deletion O(1) in a Doubly Linked List when given the node reference, but O(N) in a Singly Linked List?",
        "q1_opts": [
            {"id": "A", "label": "In a DLL, node.prev immediately yields the predecessor, whereas a singly linked list must traverse from head to find the preceding node"},
            {"id": "B", "label": "Because DLL nodes are stored in Python dictionaries"},
            {"id": "C", "label": "Because DLLs are stored in contiguous memory"},
            {"id": "D", "label": "Because singly linked lists cannot delete nodes"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! Deletion requires mutating the predecessor's next pointer. In a singly linked list, finding that predecessor takes O(N) search from head. In a DLL, node.prev gives direct O(1) access.",
            "B": "Incorrect: DLL is a linked pointer structure, not a dict.",
            "C": "Incorrect: DLL nodes are heap-allocated non-contiguously.",
            "D": "Incorrect: Singly linked lists can delete nodes, but finding predecessor is O(N)."
        },
        "q2": "What happens if you delete a node by setting node.prev.next = node.next without updating node.next.prev = node.prev?",
        "q2_opts": [
            {"id": "A", "label": "Forward traversal skips the deleted node, but backward traversal still encounters it, corrupting the bi-directional invariant"},
            {"id": "B", "label": "Python automatically updates node.next.prev"},
            {"id": "C", "label": "The program crashes with MemoryError"},
            {"id": "D", "label": "The node is cloned"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! Bi-directional consistency requires both forward (next) and backward (prev) links to be synchronized; missing one causes asymmetric corruption.",
            "B": "Incorrect: Python does not infer dual pointer mutations.",
            "C": "Incorrect: No memory overflow occurs.",
            "D": "Incorrect: Nodes are not duplicated."
        },
        "practice_task": "Implement an O(1) node removal method for a Doubly Linked List with sentinels.",
        "starter": "class DLLNode:\n    def __init__(self, val=0):\n        self.val = val\n        self.prev = None\n        self.next = None\n\nclass DoublyLinkedList:\n    def __init__(self):\n        self.head = DLLNode(0)\n        self.tail = DLLNode(0)\n        self.head.next = self.tail\n        self.tail.prev = self.head\n\n    def add_to_head(self, node: DLLNode):\n        node.next = self.head.next\n        node.prev = self.head\n        self.head.next.prev = node\n        self.head.next = node\n\n    def remove_node(self, node: DLLNode) -> None:\n        # TODO: Mutate node.prev and node.next to unlink node in O(1)\n        pass\n\n    def to_list(self) -> list[int]:\n        res = []\n        curr = self.head.next\n        while curr != self.tail:\n            res.append(curr.val)\n            curr = curr.next\n        return res\n\ndll = DoublyLinkedList()\nn1 = DLLNode(1); n2 = DLLNode(2); n3 = DLLNode(3)\ndll.add_to_head(n3); dll.add_to_head(n2); dll.add_to_head(n1)\ndll.remove_node(n2)\nprint('DLL after removal:', dll.to_list())\n",
        "solution": "class DLLNode:\n    def __init__(self, val=0):\n        self.val = val\n        self.prev = None\n        self.next = None\n\nclass DoublyLinkedList:\n    def __init__(self):\n        self.head = DLLNode(0)\n        self.tail = DLLNode(0)\n        self.head.next = self.tail\n        self.tail.prev = self.head\n\n    def add_to_head(self, node: DLLNode):\n        node.next = self.head.next\n        node.prev = self.head\n        self.head.next.prev = node\n        self.head.next = node\n\n    def remove_node(self, node: DLLNode) -> None:\n        p = node.prev\n        n = node.next\n        p.next = n\n        n.prev = p\n\n    def to_list(self) -> list[int]:\n        res = []\n        curr = self.head.next\n        while curr != self.tail:\n            res.append(curr.val)\n            curr = curr.next\n        return res\n\ndll = DoublyLinkedList()\nn1 = DLLNode(1); n2 = DLLNode(2); n3 = DLLNode(3)\ndll.add_to_head(n3); dll.add_to_head(n2); dll.add_to_head(n1)\ndll.remove_node(n2)\nprint('DLL after removal:', dll.to_list())\n",
        "patterns": ["DLL after removal: [1, 3]"],
        "hint": "Set node.prev.next = node.next and node.next.prev = node.prev.",
        "recap": [
            {"concept": "Direct Predecessor Access", "naiveIntuition": "All linked lists need O(N) traversal to delete", "pythonReality": "DLL stores backward pointers, making deletion strictly O(1) when given the node reference"},
            {"concept": "Dual Boundary Sentinels", "naiveIntuition": "Manage None checks at head and tail", "pythonReality": "Permanent dummy head and tail nodes eliminate all None checks during insertions and deletions"}
        ]
    },
    83: {
        "summary": "LRU Cache architecture combines a Hash Map (for O(1) key-to-node lookup) and a Doubly Linked List (for O(1) eviction of Least Recently Used items).",
        "mechanics": "The Hash Map stores key -> DLLNode(key, val). When a key is accessed or updated (get or put), the node is unlinked and moved to the head (Most Recently Used). When capacity is exceeded, tail.prev (Least Recently Used) is evicted from both the DLL and the map.",
        "takeaway": "Pairing a hash map with a doubly linked list achieves O(1) get and O(1) put with LRU ordering.",
        "sample_code": "# LRU Cache structural combination\n# map: key -> DLLNode\n# DLL: head (MRU) <-> ... <-> tail (LRU)",
        "q1": "Why does an LRU Cache require BOTH a Hash Map and a Doubly Linked List?",
        "q1_opts": [
            {"id": "A", "label": "The hash map provides O(1) key lookup, while the DLL maintains recency order and enables O(1) removal of the accessed node"},
            {"id": "B", "label": "Because Python dictionaries cannot store integers"},
            {"id": "C", "label": "To sort keys alphabetically"},
            {"id": "D", "label": "To reduce space complexity to O(0)"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! A DLL alone takes O(N) to find a key. A hash map alone cannot rearrange recency ordering in O(1). Together, they deliver O(1) lookup, O(1) update, and O(1) eviction.",
            "B": "Incorrect: Python dicts store arbitrary hashable keys.",
            "C": "Incorrect: Order is temporal recency, not alphabetical.",
            "D": "Incorrect: Space is O(capacity)."
        },
        "q2": "Why must the DLLNode in an LRU Cache store BOTH key and val, rather than just val?",
        "q2_opts": [
            {"id": "A", "label": "When evicting the least recently used node (tail.prev), its key is required to delete the corresponding entry from the hash map"},
            {"id": "B", "label": "To satisfy Python class constraints"},
            {"id": "C", "label": "To prevent hash collisions"},
            {"id": "D", "label": "Because values are immutable"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! Eviction starts from the DLL tail (tail.prev). Without storing key on the node, there is no way to know which key to del cache[node.key] in the hash map.",
            "B": "Incorrect: Custom classes can have any attributes.",
            "C": "Incorrect: Collisions are handled internally by the map.",
            "D": "Incorrect: Values can be mutable."
        },
        "practice_task": "Implement an LRU Cache supporting get and put operations in O(1) time.",
        "starter": "class DNode:\n    def __init__(self, key=0, val=0):\n        self.key = key\n        self.val = val\n        self.prev = None\n        self.next = None\n\nclass LRUCache:\n    def __init__(self, capacity: int):\n        self.capacity = capacity\n        self.map = {}\n        self.head = DNode()\n        self.tail = DNode()\n        self.head.next = self.tail\n        self.tail.prev = self.head\n\n    # TODO: Implement _remove(node) and _add(node) helper methods\n    # TODO: Implement get(key) -> int and put(key, val) -> None\n\nlru = LRUCache(2)\nlru.put(1, 1)\nlru.put(2, 2)\nprint('Get 1:', lru.get(1))\nlru.put(3, 3)\nprint('Get 2:', lru.get(2))\n",
        "solution": "class DNode:\n    def __init__(self, key=0, val=0):\n        self.key = key\n        self.val = val\n        self.prev = None\n        self.next = None\n\nclass LRUCache:\n    def __init__(self, capacity: int):\n        self.capacity = capacity\n        self.map = {}\n        self.head = DNode()\n        self.tail = DNode()\n        self.head.next = self.tail\n        self.tail.prev = self.head\n\n    def _remove(self, node: DNode):\n        p = node.prev\n        n = node.next\n        p.next = n\n        n.prev = p\n\n    def _add(self, node: DNode):\n        node.next = self.head.next\n        node.prev = self.head\n        self.head.next.prev = node\n        self.head.next = node\n\n    def get(self, key: int) -> int:\n        if key in self.map:\n            node = self.map[key]\n            self._remove(node)\n            self._add(node)\n            return node.val\n        return -1\n\n    def put(self, key: int, val: int) -> None:\n        if key in self.map:\n            self._remove(self.map[key])\n        node = DNode(key, val)\n        self._add(node)\n        self.map[key] = node\n        if len(self.map) > self.capacity:\n            lru = self.tail.prev\n            self._remove(lru)\n            del self.map[lru.key]\n\nlru = LRUCache(2)\nlru.put(1, 1)\nlru.put(2, 2)\nprint('Get 1:', lru.get(1))\nlru.put(3, 3)\nprint('Get 2:', lru.get(2))\n",
        "patterns": ["Get 1: 1", "Get 2: -1"],
        "hint": "_remove(node) unlinks pointers; _add(node) inserts right after head. In get(): move node to head and return val. In put(): if key exists remove old node, add new node, and if over capacity remove tail.prev and del map[tail.prev.key].",
        "recap": [
            {"concept": "Hybrid Data Structures", "naiveIntuition": "Use a single collection for everything", "pythonReality": "Combining hash maps with doubly linked lists marries O(1) random key lookup with O(1) sequence reordering"},
            {"concept": "Eviction Reverse Lookup", "naiveIntuition": "Nodes only need values", "pythonReality": "Nodes must store keys so that eviction from the DLL tail can delete the key from the hash map in O(1)"}
        ]
    },
    84: {
        "summary": "Reverse Nodes in K-Group partitions a linked list into contiguous blocks of size K, inverting pointers within each full block while leaving leftover segments intact.",
        "mechanics": "For each segment, count K nodes forward. If fewer than K nodes remain, leave untouched. Otherwise, reverse the K nodes using standard 3-pointer reversal, link the predecessor segment to the new sub-head, and connect the old sub-head to the next segment.",
        "takeaway": "K-group reversal decomposes list processing into discrete sub-reversals with rigorous boundary re-linking.",
        "sample_code": "# K-Group reversal outline\n# 1. Count K nodes to verify full group\n# 2. Reverse K nodes\n# 3. Recursively or iteratively wire group boundaries",
        "q1": "If a linked list has 7 nodes and K = 3, what is the fate of the 7th node in Reverse Nodes in K-Group?",
        "q1_opts": [
            {"id": "A", "label": "It remains in its original position unreversed because the final block has size 1 < K"},
            {"id": "B", "label": "It is deleted from the list"},
            {"id": "C", "label": "It is padded with dummy nodes to reach size 3"},
            {"id": "D", "label": "It is moved to the head of the list"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! Problem invariant states: remaining nodes not forming a full group of size K must retain their original order.",
            "B": "Incorrect: All nodes are preserved.",
            "C": "Incorrect: No padding nodes are inserted.",
            "D": "Incorrect: It remains at the end."
        },
        "q2": "What pointer technique guarantees that the boundary preceding each K-group can be updated cleanly?",
        "q2_opts": [
            {"id": "A", "label": "Maintaining a group_prev pointer that anchors the node immediately before the K-block being inverted"},
            {"id": "B", "label": "Using global variables"},
            {"id": "C", "label": "Converting the list to a string"},
            {"id": "D", "label": "Sorting the entire list first"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! group_prev.next is re-pointed to the new reversed sub-head, ensuring seamless continuity between adjacent reversed groups.",
            "B": "Incorrect: Imperative pointer tracking avoids globals.",
            "C": "Incorrect: String conversion defeats pointer manipulation.",
            "D": "Incorrect: Values must not be arbitrarily sorted."
        },
        "practice_task": "Reverse pairs of nodes (K = 2) in a linked list and return the resulting values.",
        "starter": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef swap_pairs(head: ListNode) -> list[int]:\n    # TODO: Reverse nodes in pairs (K=2) using a dummy sentinel\n    # Return values of the modified list\n    return []\n\n# 1 -> 2 -> 3 -> 4 -> None\nh = ListNode(1, ListNode(2, ListNode(3, ListNode(4))))\nprint('Swapped pairs:', swap_pairs(h))\n",
        "solution": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef swap_pairs(head: ListNode) -> list[int]:\n    dummy = ListNode(0, head)\n    prev = dummy\n    while prev.next and prev.next.next:\n        first = prev.next\n        second = prev.next.next\n        first.next = second.next\n        second.next = first\n        prev.next = second\n        prev = first\n    \n    res = []\n    curr = dummy.next\n    while curr:\n        res.append(curr.val)\n        curr = curr.next\n    return res\n\nh = ListNode(1, ListNode(2, ListNode(3, ListNode(4))))\nprint('Swapped pairs:', swap_pairs(h))\n",
        "patterns": ["Swapped pairs: [2, 1, 4, 3]"],
        "hint": "dummy = ListNode(0, head); prev = dummy. While prev.next and prev.next.next: first = prev.next; second = prev.next.next. Rewire: first.next = second.next; second.next = first; prev.next = second; prev = first.",
        "recap": [
            {"concept": "Subsegment Pointer Rewiring", "naiveIntuition": "Swap node values directly", "pythonReality": "Swapping node values is considered an anti-pattern in interviews and fails when nodes hold large payloads; rewiring pointers preserves node identity"},
            {"concept": "Group Boundary Continuity", "naiveIntuition": "Reverse segments independently and stitch later", "pythonReality": "Maintaining group_prev enables continuous in-place stitching during the single traversal pass"}
        ]
    },
    85: {
        "summary": "Section 7 Review synthesizes pointer discipline, dummy sentinels, two-pointer race mechanics, doubly linked structures, and LRU cache architecture.",
        "mechanics": "Mastering linked lists requires 3 core disciplines: (1) Always sketch pointer mutations before writing code, (2) Cache forward references before overwriting .next, and (3) Use dummy sentinels to unify boundary operations.",
        "takeaway": "Pointer discipline and dummy sentinels guarantee robust, zero-edge-case linked list algorithms.",
        "sample_code": "# Master Linked List Discipline Checklist:\n# 1. dummy = ListNode(0, head)\n# 2. nxt = curr.next before curr.next = ...\n# 3. while fast and fast.next for two-pointer races",
        "q1": "Which of the following operations takes O(1) time in a singly linked list with only a head reference?",
        "q1_opts": [
            {"id": "A", "label": "Inserting a new node at the head (new_node.next = head; head = new_node)"},
            {"id": "B", "label": "Finding the middle node"},
            {"id": "C", "label": "Deleting the tail node"},
            {"id": "D", "label": "Accessing element at index K"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! Prepending at the head involves only two reference assignments and requires no traversal, running in strict O(1) time.",
            "B": "Incorrect: Finding the middle takes O(N) traversal.",
            "C": "Incorrect: Deleting the tail takes O(N) to find the penultimate node.",
            "D": "Incorrect: Indexing takes O(K) sequential traversal."
        },
        "q2": "What is the primary trade-off of a Doubly Linked List over a Singly Linked List?",
        "q2_opts": [
            {"id": "A", "label": "DLL enables O(1) bidirectional traversal and deletion at the cost of an additional prev pointer per node (higher memory overhead)"},
            {"id": "B", "label": "DLL cannot store strings"},
            {"id": "C", "label": "DLL has slower search time than O(N)"},
            {"id": "D", "label": "DLL is only supported in C++, not Python"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! Every node in a DLL stores two references (prev and next), roughly doubling the pointer memory footprint per node while enabling O(1) removal and backward iteration.",
            "B": "Incorrect: Any Python object can be stored.",
            "C": "Incorrect: Search time is still O(N).",
            "D": "Incorrect: Python classes easily implement DLLs."
        },
        "practice_task": "Build a Linked List Palindrome Verifier in O(N) time and O(1) space.",
        "starter": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef is_palindrome(head: ListNode) -> bool:\n    # TODO 1: Find middle using fast/slow pointers\n    # TODO 2: Reverse second half in-place\n    # TODO 3: Compare first and second halves node by node\n    return False\n\n# 1 -> 2 -> 2 -> 1 -> None\npal = ListNode(1, ListNode(2, ListNode(2, ListNode(1))))\nprint('Is palindrome:', is_palindrome(pal))\n",
        "solution": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef is_palindrome(head: ListNode) -> bool:\n    if not head or not head.next:\n        return True\n    slow = fast = head\n    while fast and fast.next:\n        slow = slow.next\n        fast = fast.next.next\n    prev = None\n    curr = slow\n    while curr:\n        nxt = curr.next\n        curr.next = prev\n        prev = curr\n        curr = nxt\n    p1 = head\n    p2 = prev\n    while p2:\n        if p1.val != p2.val:\n            return False\n        p1 = p1.next\n        p2 = p2.next\n    return True\n\npal = ListNode(1, ListNode(2, ListNode(2, ListNode(1))))\nprint('Is palindrome:', is_palindrome(pal))\n",
        "patterns": ["Is palindrome: True"],
        "hint": "Find middle with slow/fast. Reverse starting from slow with three pointers (prev, curr, nxt). Compare head with prev until second half is exhausted.",
        "recap": [
            {"concept": "Three-Stage Algorithmic Composition", "naiveIntuition": "Copy to an array and check pal == pal[::-1] in O(N) space", "pythonReality": "Composing Fast/Slow pointers + In-place Reversal + Two-Pointer check achieves O(N) time in strict O(1) auxiliary space"},
            {"concept": "Section 7 Synthesis", "naiveIntuition": "Linked lists are legacy data structures", "pythonReality": "Linked nodes form the backbone of memory allocators, OS kernel task schedulers, and high-performance caches like LRU/LFU"}
        ]
    }
}
