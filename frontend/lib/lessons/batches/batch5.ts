import { DailyLessonPackage } from "../types";

export const BATCH_5_LESSONS: Record<number, DailyLessonPackage> = {
  81: {
  "dayNumber": 81,
  "title": "Merge Two Sorted Lists & K-Way Splicing",
  "topicName": "List Merging",
  "sectionId": "linked-lists",
  "estimatedMinutes": 35,
  "difficulty": "INTERMEDIATE",
  "prerequisites": [
    77,
    78
  ],
  "concepts": [
    "Sentinel Splice Invariant",
    "Iterative In-Place Splice"
  ],
  "practiceSkills": [
    "List Merging Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Merge two sorted singly linked lists in-place in O(N + M) time without new allocations",
    "Splice node pointers monotonically preserving sorted sequence"
  ],
  "practiceArchetype": "problem",
  "flowTier": "tier2"
,
  "steps": [
    {
        "id": "day81-step1",
        "stepNumber": 1,
        "title": "Merge Two Sorted Lists & K-Way Splicing: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: List Merging",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for List Merging.",
        "markdownContent": [
            "Merging Sorted Lists splices existing nodes into non-decreasing order using a dummy head sentinel and two pointers, running in O(N + M) time and O(1) extra space.",
            "### Foundational Mental Model\nWhen approaching problems requiring **List Merging**, remember the central principle: Splicing existing node references merges sorted lists without creating new node objects."
        ],
        "snippets": [
            {
                "title": "List Merging Implementation Template",
                "code": "# Merge two sorted lists\ndef merge_two_lists(l1, l2):\n    dummy = ListNode(0)\n    curr = dummy\n    while l1 and l2:\n        if l1.val <= l2.val:\n            curr.next = l1; l1 = l1.next\n        else:\n            curr.next = l2; l2 = l2.next\n        curr = curr.next\n    curr.next = l1 or l2\n    return dummy.next",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Splicing existing node references merges sorted lists without creating new node objects."
    },
    {
        "id": "day81-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: List Merging",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Initialize dummy = ListNode(0), curr = dummy. Compare l1.val and l2.val, attach smaller node to curr.next, and advance corresponding pointer. When one list empties, splice the remaining sublist directly via curr.next = l1 or l2.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Splicing existing node references merges sorted lists without creating new node objects.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "List Merging Core Invariant",
                "content": "Splicing existing node references merges sorted lists without creating new node objects."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Splicing existing node references merges sorted lists without creating new node objects."
    },
    {
        "id": "day81-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: List Merging",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d81-q1",
                "question": "Why is curr.next = l1 or l2 sufficient when the loop while l1 and l2: terminates?",
                "options": [
                    {
                        "id": "A",
                        "label": "Because the remaining non-empty list is already sorted and can be attached as an entire contiguous chain in O(1) time"
                    },
                    {
                        "id": "B",
                        "label": "Because both lists are guaranteed to be empty"
                    },
                    {
                        "id": "C",
                        "label": "To trigger list reversal"
                    },
                    {
                        "id": "D",
                        "label": "Because Python automatically merges remaining nodes"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Unlike arrays where remaining elements must be copied one by one, a linked list's remaining nodes are already chained together; splicing the pointer takes O(1) time.",
                    "B": "Incorrect: One list still contains remaining elements.",
                    "C": "Incorrect: No reversal occurs.",
                    "D": "Incorrect: Splicing is an explicit assignment of references."
                }
            },
            {
                "id": "chk-d81-q2",
                "question": "What is the total time complexity of merging two sorted linked lists of lengths N and M?",
                "options": [
                    {
                        "id": "A",
                        "label": "O(N + M)"
                    },
                    {
                        "id": "B",
                        "label": "O(N * M)"
                    },
                    {
                        "id": "C",
                        "label": "O(log(N + M))"
                    },
                    {
                        "id": "D",
                        "label": "O(1)"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Each comparison advances either pointer l1 or l2 by one node. At most N + M comparisons occur.",
                    "B": "Incorrect: Nested comparison is not needed because both inputs are sorted.",
                    "C": "Incorrect: Cannot inspect all elements in logarithmic time.",
                    "D": "Incorrect: Every node must be visited."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day81-step4",
        "stepNumber": 4,
        "title": "Guided Practice: List Merging",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Merge two sorted linked lists into a single sorted list and collect values.",
        "subheading": "Implement and verify List Merging in the interactive workspace.",
        "task": {
            "title": "Merge two sorted linked lists into a single sorted list and collect values.",
            "instructions": [
                "Merge two sorted linked lists into a single sorted list and collect values.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef merge_and_collect(l1: ListNode, l2: ListNode) -> list[int]:\n    # TODO: Merge l1 and l2 using a dummy sentinel\n    # Return values in sorted order\n    return []\n\n# l1: 1 -> 3 -> 5; l2: 2 -> 4 -> 6\nl1 = ListNode(1, ListNode(3, ListNode(5)))\nl2 = ListNode(2, ListNode(4, ListNode(6)))\nprint('Merged:', merge_and_collect(l1, l2))\n",
            "solutionCode": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef merge_and_collect(l1: ListNode, l2: ListNode) -> list[int]:\n    dummy = ListNode(0)\n    curr = dummy\n    while l1 and l2:\n        if l1.val <= l2.val:\n            curr.next = l1\n            l1 = l1.next\n        else:\n            curr.next = l2\n            l2 = l2.next\n        curr = curr.next\n    curr.next = l1 or l2\n    \n    res = []\n    node = dummy.next\n    while node:\n        res.append(node.val)\n        node = node.next\n    return res\n\nl1 = ListNode(1, ListNode(3, ListNode(5)))\nl2 = ListNode(2, ListNode(4, ListNode(6)))\nprint('Merged:', merge_and_collect(l1, l2))\n",
            "expectedOutputPatterns": [
                "Merged: [1, 2, 3, 4, 5, 6]"
            ],
            "hint": "dummy = ListNode(0); curr = dummy. While l1 and l2: attach smaller node, advance that list and curr. Splicing remaining: curr.next = l1 or l2. Return traversed dummy.next."
        },
        "keyTakeaway": "Successfully implemented and verified List Merging!"
    },
    {
        "id": "day81-step5",
        "stepNumber": 5,
        "title": "Day 81 Complete: Merge Two Sorted Lists & K-Way Splicing",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 81,
        "heading": "Mastery Achieved: Merge Two Sorted Lists & K-Way Splicing",
        "subheading": "You have solidified key mental models and techniques for List Merging.",
        "recapRows": [
            {
                "concept": "Pointer Splicing",
                "naiveIntuition": "Create brand new nodes for merged list",
                "pythonReality": "Re-wiring existing node pointers merges lists in O(1) auxiliary space without memory allocations"
            },
            {
                "concept": "Residual Chain Attachment",
                "naiveIntuition": "Loop through all remaining nodes one by one",
                "pythonReality": "Attaching the head of the non-empty list links all remaining nodes in a single O(1) assignment"
            }
        ],
        "solidifiedConcepts": [
            "Sentinel Splice Invariant",
            "Iterative In-Place Splice"
        ],
        "nextDayPreview": {
            "dayNumber": 82,
            "title": "Doubly Linked Lists & Bi-Directional Nodes",
            "description": "Implement Doubly Linked Lists, manage prev/next pointers, and achieve O(1) arbitrary node detachment."
        }
    }
]
},
  82: {
  "dayNumber": 82,
  "title": "Doubly Linked Lists & Bi-Directional Nodes",
  "topicName": "Doubly Linked Lists",
  "sectionId": "linked-lists",
  "estimatedMinutes": 30,
  "difficulty": "INTERMEDIATE",
  "prerequisites": [
    77
  ],
  "concepts": [
    "prev & next Bi-Directional Pointers",
    "O(1) Self-Detachment"
  ],
  "practiceSkills": [
    "Doubly Linked Lists Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Implement a Doubly Linked List node with prev and next references",
    "Detach arbitrary interior nodes in strict O(1) time without finding predecessor"
  ],
  "practiceArchetype": "algorithm",
  "flowTier": "tier1"
,
  "steps": [
    {
        "id": "day82-step1",
        "stepNumber": 1,
        "title": "Doubly Linked Lists & Bi-Directional Nodes: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Doubly Linked Lists",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Doubly Linked Lists.",
        "markdownContent": [
            "Doubly Linked Lists (DLL) equip nodes with both prev and next pointers, enabling true O(1) deletion and insertion at arbitrary positions given a direct node reference.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Doubly Linked Lists**, remember the central principle: DLLs provide O(1) deletion of any node given its reference, forming the foundation of LRU caches."
        ],
        "snippets": [
            {
                "title": "Doubly Linked Lists Implementation Template",
                "code": "class DLLNode:\n    def __init__(self, key=0, val=0):\n        self.key = key; self.val = val\n        self.prev = None; self.next = None\n\nhead = DLLNode(); tail = DLLNode()\nhead.next = tail; tail.prev = head",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "DLLs provide O(1) deletion of any node given its reference, forming the foundation of LRU caches."
    },
    {
        "id": "day82-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Doubly Linked Lists",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Node deletion: node.prev.next = node.next; node.next.prev = node.prev. By placing permanent dummy head and tail sentinels, head and tail boundary checks vanish completely.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: DLLs provide O(1) deletion of any node given its reference, forming the foundation of LRU caches.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Doubly Linked Lists Core Invariant",
                "content": "DLLs provide O(1) deletion of any node given its reference, forming the foundation of LRU caches."
            }
        ],
        "keyTakeaway": "Operational invariant locked: DLLs provide O(1) deletion of any node given its reference, forming the foundation of LRU caches."
    },
    {
        "id": "day82-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Doubly Linked Lists",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d82-q1",
                "question": "Why is node deletion O(1) in a Doubly Linked List when given the node reference, but O(N) in a Singly Linked List?",
                "options": [
                    {
                        "id": "A",
                        "label": "In a DLL, node.prev immediately yields the predecessor, whereas a singly linked list must traverse from head to find the preceding node"
                    },
                    {
                        "id": "B",
                        "label": "Because DLL nodes are stored in Python dictionaries"
                    },
                    {
                        "id": "C",
                        "label": "Because DLLs are stored in contiguous memory"
                    },
                    {
                        "id": "D",
                        "label": "Because singly linked lists cannot delete nodes"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Deletion requires mutating the predecessor's next pointer. In a singly linked list, finding that predecessor takes O(N) search from head. In a DLL, node.prev gives direct O(1) access.",
                    "B": "Incorrect: DLL is a linked pointer structure, not a dict.",
                    "C": "Incorrect: DLL nodes are heap-allocated non-contiguously.",
                    "D": "Incorrect: Singly linked lists can delete nodes, but finding predecessor is O(N)."
                }
            },
            {
                "id": "chk-d82-q2",
                "question": "What happens if you delete a node by setting node.prev.next = node.next without updating node.next.prev = node.prev?",
                "options": [
                    {
                        "id": "A",
                        "label": "Forward traversal skips the deleted node, but backward traversal still encounters it, corrupting the bi-directional invariant"
                    },
                    {
                        "id": "B",
                        "label": "Python automatically updates node.next.prev"
                    },
                    {
                        "id": "C",
                        "label": "The program crashes with MemoryError"
                    },
                    {
                        "id": "D",
                        "label": "The node is cloned"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Bi-directional consistency requires both forward (next) and backward (prev) links to be synchronized; missing one causes asymmetric corruption.",
                    "B": "Incorrect: Python does not infer dual pointer mutations.",
                    "C": "Incorrect: No memory overflow occurs.",
                    "D": "Incorrect: Nodes are not duplicated."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day82-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Doubly Linked Lists",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Implement an O(1) node removal method for a Doubly Linked List with sentinels.",
        "subheading": "Implement and verify Doubly Linked Lists in the interactive workspace.",
        "task": {
            "title": "Implement an O(1) node removal method for a Doubly Linked List with sentinels.",
            "instructions": [
                "Implement an O(1) node removal method for a Doubly Linked List with sentinels.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "class DLLNode:\n    def __init__(self, val=0):\n        self.val = val\n        self.prev = None\n        self.next = None\n\nclass DoublyLinkedList:\n    def __init__(self):\n        self.head = DLLNode(0)\n        self.tail = DLLNode(0)\n        self.head.next = self.tail\n        self.tail.prev = self.head\n\n    def add_to_head(self, node: DLLNode):\n        node.next = self.head.next\n        node.prev = self.head\n        self.head.next.prev = node\n        self.head.next = node\n\n    def remove_node(self, node: DLLNode) -> None:\n        # TODO: Mutate node.prev and node.next to unlink node in O(1)\n        pass\n\n    def to_list(self) -> list[int]:\n        res = []\n        curr = self.head.next\n        while curr != self.tail:\n            res.append(curr.val)\n            curr = curr.next\n        return res\n\ndll = DoublyLinkedList()\nn1 = DLLNode(1); n2 = DLLNode(2); n3 = DLLNode(3)\ndll.add_to_head(n3); dll.add_to_head(n2); dll.add_to_head(n1)\ndll.remove_node(n2)\nprint('DLL after removal:', dll.to_list())\n",
            "solutionCode": "class DLLNode:\n    def __init__(self, val=0):\n        self.val = val\n        self.prev = None\n        self.next = None\n\nclass DoublyLinkedList:\n    def __init__(self):\n        self.head = DLLNode(0)\n        self.tail = DLLNode(0)\n        self.head.next = self.tail\n        self.tail.prev = self.head\n\n    def add_to_head(self, node: DLLNode):\n        node.next = self.head.next\n        node.prev = self.head\n        self.head.next.prev = node\n        self.head.next = node\n\n    def remove_node(self, node: DLLNode) -> None:\n        p = node.prev\n        n = node.next\n        p.next = n\n        n.prev = p\n\n    def to_list(self) -> list[int]:\n        res = []\n        curr = self.head.next\n        while curr != self.tail:\n            res.append(curr.val)\n            curr = curr.next\n        return res\n\ndll = DoublyLinkedList()\nn1 = DLLNode(1); n2 = DLLNode(2); n3 = DLLNode(3)\ndll.add_to_head(n3); dll.add_to_head(n2); dll.add_to_head(n1)\ndll.remove_node(n2)\nprint('DLL after removal:', dll.to_list())\n",
            "expectedOutputPatterns": [
                "DLL after removal: [1, 3]"
            ],
            "hint": "Set node.prev.next = node.next and node.next.prev = node.prev."
        },
        "keyTakeaway": "Successfully implemented and verified Doubly Linked Lists!"
    },
    {
        "id": "day82-step5",
        "stepNumber": 5,
        "title": "Day 82 Complete: Doubly Linked Lists & Bi-Directional Nodes",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 82,
        "heading": "Mastery Achieved: Doubly Linked Lists & Bi-Directional Nodes",
        "subheading": "You have solidified key mental models and techniques for Doubly Linked Lists.",
        "recapRows": [
            {
                "concept": "Direct Predecessor Access",
                "naiveIntuition": "All linked lists need O(N) traversal to delete",
                "pythonReality": "DLL stores backward pointers, making deletion strictly O(1) when given the node reference"
            },
            {
                "concept": "Dual Boundary Sentinels",
                "naiveIntuition": "Manage None checks at head and tail",
                "pythonReality": "Permanent dummy head and tail nodes eliminate all None checks during insertions and deletions"
            }
        ],
        "solidifiedConcepts": [
            "prev & next Bi-Directional Pointers",
            "O(1) Self-Detachment"
        ],
        "nextDayPreview": {
            "dayNumber": 83,
            "title": "Scratch-Built LRU Cache (DLL + Hash Map)",
            "description": "Build a production-grade O(1) LRU Cache from scratch combining a Hash Map with a Doubly Linked List with sentinels."
        }
    }
]
},
  83: {
  "dayNumber": 83,
  "title": "Scratch-Built LRU Cache (DLL + Hash Map)",
  "topicName": "Scratch LRU Cache",
  "sectionId": "linked-lists",
  "estimatedMinutes": 45,
  "difficulty": "INTERMEDIATE",
  "prerequisites": [
    73,
    82
  ],
  "concepts": [
    "Hash Map to DLL Node Pointers",
    "O(1) get() and put() Operations"
  ],
  "practiceSkills": [
    "Scratch LRU Cache Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Architect a complete LRU Cache from scratch pairing a hash map with a doubly linked list",
    "Maintain head/tail dummy sentinels to guarantee O(1) eviction and promotion"
  ],
  "practiceArchetype": "milestone",
  "flowTier": "tier3"
,
  "steps": [
    {
        "id": "day83-step1",
        "stepNumber": 1,
        "title": "Scratch-Built LRU Cache (DLL + Hash Map): Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Scratch LRU Cache",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Scratch LRU Cache.",
        "markdownContent": [
            "LRU Cache architecture combines a Hash Map (for O(1) key-to-node lookup) and a Doubly Linked List (for O(1) eviction of Least Recently Used items).",
            "### Foundational Mental Model\nWhen approaching problems requiring **Scratch LRU Cache**, remember the central principle: Pairing a hash map with a doubly linked list achieves O(1) get and O(1) put with LRU ordering."
        ],
        "snippets": [
            {
                "title": "Scratch LRU Cache Implementation Template",
                "code": "# LRU Cache structural combination\n# map: key -> DLLNode\n# DLL: head (MRU) <-> ... <-> tail (LRU)",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Pairing a hash map with a doubly linked list achieves O(1) get and O(1) put with LRU ordering."
    },
    {
        "id": "day83-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Scratch LRU Cache",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "The Hash Map stores key -> DLLNode(key, val). When a key is accessed or updated (get or put), the node is unlinked and moved to the head (Most Recently Used). When capacity is exceeded, tail.prev (Least Recently Used) is evicted from both the DLL and the map.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Pairing a hash map with a doubly linked list achieves O(1) get and O(1) put with LRU ordering.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Scratch LRU Cache Core Invariant",
                "content": "Pairing a hash map with a doubly linked list achieves O(1) get and O(1) put with LRU ordering."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Pairing a hash map with a doubly linked list achieves O(1) get and O(1) put with LRU ordering."
    },
    {
        "id": "day83-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Scratch LRU Cache",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d83-q1",
                "question": "Why does an LRU Cache require BOTH a Hash Map and a Doubly Linked List?",
                "options": [
                    {
                        "id": "A",
                        "label": "The hash map provides O(1) key lookup, while the DLL maintains recency order and enables O(1) removal of the accessed node"
                    },
                    {
                        "id": "B",
                        "label": "Because Python dictionaries cannot store integers"
                    },
                    {
                        "id": "C",
                        "label": "To sort keys alphabetically"
                    },
                    {
                        "id": "D",
                        "label": "To reduce space complexity to O(0)"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! A DLL alone takes O(N) to find a key. A hash map alone cannot rearrange recency ordering in O(1). Together, they deliver O(1) lookup, O(1) update, and O(1) eviction.",
                    "B": "Incorrect: Python dicts store arbitrary hashable keys.",
                    "C": "Incorrect: Order is temporal recency, not alphabetical.",
                    "D": "Incorrect: Space is O(capacity)."
                }
            },
            {
                "id": "chk-d83-q2",
                "question": "Why must the DLLNode in an LRU Cache store BOTH key and val, rather than just val?",
                "options": [
                    {
                        "id": "A",
                        "label": "When evicting the least recently used node (tail.prev), its key is required to delete the corresponding entry from the hash map"
                    },
                    {
                        "id": "B",
                        "label": "To satisfy Python class constraints"
                    },
                    {
                        "id": "C",
                        "label": "To prevent hash collisions"
                    },
                    {
                        "id": "D",
                        "label": "Because values are immutable"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Eviction starts from the DLL tail (tail.prev). Without storing key on the node, there is no way to know which key to del cache[node.key] in the hash map.",
                    "B": "Incorrect: Custom classes can have any attributes.",
                    "C": "Incorrect: Collisions are handled internally by the map.",
                    "D": "Incorrect: Values can be mutable."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day83-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Scratch LRU Cache",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Implement an LRU Cache supporting get and put operations in O(1) time.",
        "subheading": "Implement and verify Scratch LRU Cache in the interactive workspace.",
        "task": {
            "title": "Implement an LRU Cache supporting get and put operations in O(1) time.",
            "instructions": [
                "Implement an LRU Cache supporting get and put operations in O(1) time.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "class DNode:\n    def __init__(self, key=0, val=0):\n        self.key = key\n        self.val = val\n        self.prev = None\n        self.next = None\n\nclass LRUCache:\n    def __init__(self, capacity: int):\n        self.capacity = capacity\n        self.map = {}\n        self.head = DNode()\n        self.tail = DNode()\n        self.head.next = self.tail\n        self.tail.prev = self.head\n\n    # TODO: Implement _remove(node) and _add(node) helper methods\n    # TODO: Implement get(key) -> int and put(key, val) -> None\n\nlru = LRUCache(2)\nlru.put(1, 1)\nlru.put(2, 2)\nprint('Get 1:', lru.get(1))\nlru.put(3, 3)\nprint('Get 2:', lru.get(2))\n",
            "solutionCode": "class DNode:\n    def __init__(self, key=0, val=0):\n        self.key = key\n        self.val = val\n        self.prev = None\n        self.next = None\n\nclass LRUCache:\n    def __init__(self, capacity: int):\n        self.capacity = capacity\n        self.map = {}\n        self.head = DNode()\n        self.tail = DNode()\n        self.head.next = self.tail\n        self.tail.prev = self.head\n\n    def _remove(self, node: DNode):\n        p = node.prev\n        n = node.next\n        p.next = n\n        n.prev = p\n\n    def _add(self, node: DNode):\n        node.next = self.head.next\n        node.prev = self.head\n        self.head.next.prev = node\n        self.head.next = node\n\n    def get(self, key: int) -> int:\n        if key in self.map:\n            node = self.map[key]\n            self._remove(node)\n            self._add(node)\n            return node.val\n        return -1\n\n    def put(self, key: int, val: int) -> None:\n        if key in self.map:\n            self._remove(self.map[key])\n        node = DNode(key, val)\n        self._add(node)\n        self.map[key] = node\n        if len(self.map) > self.capacity:\n            lru = self.tail.prev\n            self._remove(lru)\n            del self.map[lru.key]\n\nlru = LRUCache(2)\nlru.put(1, 1)\nlru.put(2, 2)\nprint('Get 1:', lru.get(1))\nlru.put(3, 3)\nprint('Get 2:', lru.get(2))\n",
            "expectedOutputPatterns": [
                "Get 1: 1",
                "Get 2: -1"
            ],
            "hint": "_remove(node) unlinks pointers; _add(node) inserts right after head. In get(): move node to head and return val. In put(): if key exists remove old node, add new node, and if over capacity remove tail.prev and del map[tail.prev.key]."
        },
        "keyTakeaway": "Successfully implemented and verified Scratch LRU Cache!"
    },
    {
        "id": "day83-step5",
        "stepNumber": 5,
        "title": "Day 83 Complete: Scratch-Built LRU Cache (DLL + Hash Map)",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 83,
        "heading": "Mastery Achieved: Scratch-Built LRU Cache (DLL + Hash Map)",
        "subheading": "You have solidified key mental models and techniques for Scratch LRU Cache.",
        "recapRows": [
            {
                "concept": "Hybrid Data Structures",
                "naiveIntuition": "Use a single collection for everything",
                "pythonReality": "Combining hash maps with doubly linked lists marries O(1) random key lookup with O(1) sequence reordering"
            },
            {
                "concept": "Eviction Reverse Lookup",
                "naiveIntuition": "Nodes only need values",
                "pythonReality": "Nodes must store keys so that eviction from the DLL tail can delete the key from the hash map in O(1)"
            }
        ],
        "solidifiedConcepts": [
            "Hash Map to DLL Node Pointers",
            "O(1) get() and put() Operations"
        ],
        "nextDayPreview": {
            "dayNumber": 84,
            "title": "Reverse Nodes in K-Group",
            "description": "Reverse linked lists in groups of K nodes, handling subsegment reversals and boundary reconnects in O(N) time."
        }
    }
]
},
  84: {
  "dayNumber": 84,
  "title": "Reverse Nodes in K-Group",
  "topicName": "K-Group Reversal",
  "sectionId": "linked-lists",
  "estimatedMinutes": 45,
  "difficulty": "INTERMEDIATE",
  "prerequisites": [
    78,
    81
  ],
  "concepts": [
    "K-Node Segment Isolation",
    "Boundary Pointer Re-Wiring"
  ],
  "practiceSkills": [
    "K-Group Reversal Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Count and reverse contiguous subsegments of k nodes in-place",
    "Reconnect reversed segment endpoints cleanly to preceding and following sublists"
  ],
  "practiceArchetype": "problem",
  "flowTier": "tier3"
,
  "steps": [
    {
        "id": "day84-step1",
        "stepNumber": 1,
        "title": "Reverse Nodes in K-Group: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: K-Group Reversal",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for K-Group Reversal.",
        "markdownContent": [
            "Reverse Nodes in K-Group partitions a linked list into contiguous blocks of size K, inverting pointers within each full block while leaving leftover segments intact.",
            "### Foundational Mental Model\nWhen approaching problems requiring **K-Group Reversal**, remember the central principle: K-group reversal decomposes list processing into discrete sub-reversals with rigorous boundary re-linking."
        ],
        "snippets": [
            {
                "title": "K-Group Reversal Implementation Template",
                "code": "# K-Group reversal outline\n# 1. Count K nodes to verify full group\n# 2. Reverse K nodes\n# 3. Recursively or iteratively wire group boundaries",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "K-group reversal decomposes list processing into discrete sub-reversals with rigorous boundary re-linking."
    },
    {
        "id": "day84-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: K-Group Reversal",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "For each segment, count K nodes forward. If fewer than K nodes remain, leave untouched. Otherwise, reverse the K nodes using standard 3-pointer reversal, link the predecessor segment to the new sub-head, and connect the old sub-head to the next segment.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: K-group reversal decomposes list processing into discrete sub-reversals with rigorous boundary re-linking.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "K-Group Reversal Core Invariant",
                "content": "K-group reversal decomposes list processing into discrete sub-reversals with rigorous boundary re-linking."
            }
        ],
        "keyTakeaway": "Operational invariant locked: K-group reversal decomposes list processing into discrete sub-reversals with rigorous boundary re-linking."
    },
    {
        "id": "day84-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: K-Group Reversal",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d84-q1",
                "question": "If a linked list has 7 nodes and K = 3, what is the fate of the 7th node in Reverse Nodes in K-Group?",
                "options": [
                    {
                        "id": "A",
                        "label": "It remains in its original position unreversed because the final block has size 1 < K"
                    },
                    {
                        "id": "B",
                        "label": "It is deleted from the list"
                    },
                    {
                        "id": "C",
                        "label": "It is padded with dummy nodes to reach size 3"
                    },
                    {
                        "id": "D",
                        "label": "It is moved to the head of the list"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Problem invariant states: remaining nodes not forming a full group of size K must retain their original order.",
                    "B": "Incorrect: All nodes are preserved.",
                    "C": "Incorrect: No padding nodes are inserted.",
                    "D": "Incorrect: It remains at the end."
                }
            },
            {
                "id": "chk-d84-q2",
                "question": "What pointer technique guarantees that the boundary preceding each K-group can be updated cleanly?",
                "options": [
                    {
                        "id": "A",
                        "label": "Maintaining a group_prev pointer that anchors the node immediately before the K-block being inverted"
                    },
                    {
                        "id": "B",
                        "label": "Using global variables"
                    },
                    {
                        "id": "C",
                        "label": "Converting the list to a string"
                    },
                    {
                        "id": "D",
                        "label": "Sorting the entire list first"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! group_prev.next is re-pointed to the new reversed sub-head, ensuring seamless continuity between adjacent reversed groups.",
                    "B": "Incorrect: Imperative pointer tracking avoids globals.",
                    "C": "Incorrect: String conversion defeats pointer manipulation.",
                    "D": "Incorrect: Values must not be arbitrarily sorted."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day84-step4",
        "stepNumber": 4,
        "title": "Guided Practice: K-Group Reversal",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Reverse pairs of nodes (K = 2) in a linked list and return the resulting values.",
        "subheading": "Implement and verify K-Group Reversal in the interactive workspace.",
        "task": {
            "title": "Reverse pairs of nodes (K = 2) in a linked list and return the resulting values.",
            "instructions": [
                "Reverse pairs of nodes (K = 2) in a linked list and return the resulting values.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef swap_pairs(head: ListNode) -> list[int]:\n    # TODO: Reverse nodes in pairs (K=2) using a dummy sentinel\n    # Return values of the modified list\n    return []\n\n# 1 -> 2 -> 3 -> 4 -> None\nh = ListNode(1, ListNode(2, ListNode(3, ListNode(4))))\nprint('Swapped pairs:', swap_pairs(h))\n",
            "solutionCode": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef swap_pairs(head: ListNode) -> list[int]:\n    dummy = ListNode(0, head)\n    prev = dummy\n    while prev.next and prev.next.next:\n        first = prev.next\n        second = prev.next.next\n        first.next = second.next\n        second.next = first\n        prev.next = second\n        prev = first\n    \n    res = []\n    curr = dummy.next\n    while curr:\n        res.append(curr.val)\n        curr = curr.next\n    return res\n\nh = ListNode(1, ListNode(2, ListNode(3, ListNode(4))))\nprint('Swapped pairs:', swap_pairs(h))\n",
            "expectedOutputPatterns": [
                "Swapped pairs: [2, 1, 4, 3]"
            ],
            "hint": "dummy = ListNode(0, head); prev = dummy. While prev.next and prev.next.next: first = prev.next; second = prev.next.next. Rewire: first.next = second.next; second.next = first; prev.next = second; prev = first."
        },
        "keyTakeaway": "Successfully implemented and verified K-Group Reversal!"
    },
    {
        "id": "day84-step5",
        "stepNumber": 5,
        "title": "Day 84 Complete: Reverse Nodes in K-Group",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 84,
        "heading": "Mastery Achieved: Reverse Nodes in K-Group",
        "subheading": "You have solidified key mental models and techniques for K-Group Reversal.",
        "recapRows": [
            {
                "concept": "Subsegment Pointer Rewiring",
                "naiveIntuition": "Swap node values directly",
                "pythonReality": "Swapping node values is considered an anti-pattern in interviews and fails when nodes hold large payloads; rewiring pointers preserves node identity"
            },
            {
                "concept": "Group Boundary Continuity",
                "naiveIntuition": "Reverse segments independently and stitch later",
                "pythonReality": "Maintaining group_prev enables continuous in-place stitching during the single traversal pass"
            }
        ],
        "solidifiedConcepts": [
            "K-Node Segment Isolation",
            "Boundary Pointer Re-Wiring"
        ],
        "nextDayPreview": {
            "dayNumber": 85,
            "title": "Section 7 Review & Pointer Discipline",
            "description": "Synthesize pointer manipulation disciplines, sentinel architectures, and recursive linked-list sorting."
        }
    }
]
},
  85: {
  "dayNumber": 85,
  "title": "Section 7 Review & Pointer Discipline",
  "topicName": "Linked List Milestone",
  "sectionId": "linked-lists",
  "estimatedMinutes": 40,
  "difficulty": "INTERMEDIATE",
  "prerequisites": [
    78,
    80,
    81,
    83,
    84
  ],
  "concepts": [
    "Pointer Leak Prevention",
    "In-Place List Merge Sort",
    "Sentinel Standardization"
  ],
  "practiceSkills": [
    "Linked List Milestone Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Sort linked lists in O(N log N) time and O(log N) stack space using linked list merge sort",
    "Audit pointer manipulation logic against cyclic reference leaks and lost heads"
  ],
  "practiceArchetype": "milestone",
  "flowTier": "tier2"
,
  "steps": [
    {
        "id": "day85-step1",
        "stepNumber": 1,
        "title": "Section 7 Review & Pointer Discipline: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Linked List Milestone",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Linked List Milestone.",
        "markdownContent": [
            "Section 7 Review synthesizes pointer discipline, dummy sentinels, two-pointer race mechanics, doubly linked structures, and LRU cache architecture.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Linked List Milestone**, remember the central principle: Pointer discipline and dummy sentinels guarantee robust, zero-edge-case linked list algorithms."
        ],
        "snippets": [
            {
                "title": "Linked List Milestone Implementation Template",
                "code": "# Master Linked List Discipline Checklist:\n# 1. dummy = ListNode(0, head)\n# 2. nxt = curr.next before curr.next = ...\n# 3. while fast and fast.next for two-pointer races",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Pointer discipline and dummy sentinels guarantee robust, zero-edge-case linked list algorithms."
    },
    {
        "id": "day85-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Linked List Milestone",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Mastering linked lists requires 3 core disciplines: (1) Always sketch pointer mutations before writing code, (2) Cache forward references before overwriting .next, and (3) Use dummy sentinels to unify boundary operations.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Pointer discipline and dummy sentinels guarantee robust, zero-edge-case linked list algorithms.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Linked List Milestone Core Invariant",
                "content": "Pointer discipline and dummy sentinels guarantee robust, zero-edge-case linked list algorithms."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Pointer discipline and dummy sentinels guarantee robust, zero-edge-case linked list algorithms."
    },
    {
        "id": "day85-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Linked List Milestone",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d85-q1",
                "question": "Which of the following operations takes O(1) time in a singly linked list with only a head reference?",
                "options": [
                    {
                        "id": "A",
                        "label": "Inserting a new node at the head (new_node.next = head; head = new_node)"
                    },
                    {
                        "id": "B",
                        "label": "Finding the middle node"
                    },
                    {
                        "id": "C",
                        "label": "Deleting the tail node"
                    },
                    {
                        "id": "D",
                        "label": "Accessing element at index K"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Prepending at the head involves only two reference assignments and requires no traversal, running in strict O(1) time.",
                    "B": "Incorrect: Finding the middle takes O(N) traversal.",
                    "C": "Incorrect: Deleting the tail takes O(N) to find the penultimate node.",
                    "D": "Incorrect: Indexing takes O(K) sequential traversal."
                }
            },
            {
                "id": "chk-d85-q2",
                "question": "What is the primary trade-off of a Doubly Linked List over a Singly Linked List?",
                "options": [
                    {
                        "id": "A",
                        "label": "DLL enables O(1) bidirectional traversal and deletion at the cost of an additional prev pointer per node (higher memory overhead)"
                    },
                    {
                        "id": "B",
                        "label": "DLL cannot store strings"
                    },
                    {
                        "id": "C",
                        "label": "DLL has slower search time than O(N)"
                    },
                    {
                        "id": "D",
                        "label": "DLL is only supported in C++, not Python"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Every node in a DLL stores two references (prev and next), roughly doubling the pointer memory footprint per node while enabling O(1) removal and backward iteration.",
                    "B": "Incorrect: Any Python object can be stored.",
                    "C": "Incorrect: Search time is still O(N).",
                    "D": "Incorrect: Python classes easily implement DLLs."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day85-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Linked List Milestone",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Build a Linked List Palindrome Verifier in O(N) time and O(1) space.",
        "subheading": "Implement and verify Linked List Milestone in the interactive workspace.",
        "task": {
            "title": "Build a Linked List Palindrome Verifier in O(N) time and O(1) space.",
            "instructions": [
                "Build a Linked List Palindrome Verifier in O(N) time and O(1) space.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef is_palindrome(head: ListNode) -> bool:\n    # TODO 1: Find middle using fast/slow pointers\n    # TODO 2: Reverse second half in-place\n    # TODO 3: Compare first and second halves node by node\n    return False\n\n# 1 -> 2 -> 2 -> 1 -> None\npal = ListNode(1, ListNode(2, ListNode(2, ListNode(1))))\nprint('Is palindrome:', is_palindrome(pal))\n",
            "solutionCode": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef is_palindrome(head: ListNode) -> bool:\n    if not head or not head.next:\n        return True\n    slow = fast = head\n    while fast and fast.next:\n        slow = slow.next\n        fast = fast.next.next\n    prev = None\n    curr = slow\n    while curr:\n        nxt = curr.next\n        curr.next = prev\n        prev = curr\n        curr = nxt\n    p1 = head\n    p2 = prev\n    while p2:\n        if p1.val != p2.val:\n            return False\n        p1 = p1.next\n        p2 = p2.next\n    return True\n\npal = ListNode(1, ListNode(2, ListNode(2, ListNode(1))))\nprint('Is palindrome:', is_palindrome(pal))\n",
            "expectedOutputPatterns": [
                "Is palindrome: True"
            ],
            "hint": "Find middle with slow/fast. Reverse starting from slow with three pointers (prev, curr, nxt). Compare head with prev until second half is exhausted."
        },
        "keyTakeaway": "Successfully implemented and verified Linked List Milestone!"
    },
    {
        "id": "day85-step5",
        "stepNumber": 5,
        "title": "Day 85 Complete: Section 7 Review & Pointer Discipline",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 85,
        "heading": "Mastery Achieved: Section 7 Review & Pointer Discipline",
        "subheading": "You have solidified key mental models and techniques for Linked List Milestone.",
        "recapRows": [
            {
                "concept": "Three-Stage Algorithmic Composition",
                "naiveIntuition": "Copy to an array and check pal == pal[::-1] in O(N) space",
                "pythonReality": "Composing Fast/Slow pointers + In-place Reversal + Two-Pointer check achieves O(N) time in strict O(1) auxiliary space"
            },
            {
                "concept": "Section 7 Synthesis",
                "naiveIntuition": "Linked lists are legacy data structures",
                "pythonReality": "Linked nodes form the backbone of memory allocators, OS kernel task schedulers, and high-performance caches like LRU/LFU"
            }
        ],
        "solidifiedConcepts": [
            "Pointer Leak Prevention",
            "In-Place List Merge Sort",
            "Sentinel Standardization"
        ],
        "nextDayPreview": {
            "dayNumber": 86,
            "title": "Stack LIFO Mechanics & Array Backing",
            "description": "Understand Last-In-First-Out (LIFO) stack mechanics, amortized O(1) list backing, and underflow guards."
        }
    }
]
},
  86: {
  "dayNumber": 86,
  "title": "Stack LIFO Mechanics & Array Backing",
  "topicName": "Stack Foundations",
  "sectionId": "stacks-and-queues",
  "estimatedMinutes": 30,
  "difficulty": "INTERMEDIATE",
  "prerequisites": [
    11,
    28
  ],
  "concepts": [
    "LIFO Ordering & Operations",
    "Stack Overflow & Underflow Guards"
  ],
  "practiceSkills": [
    "Stack Foundations Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Implement an array-backed stack with O(1) push, pop, and peek operations",
    "Enforce defensive bounds checking against stack underflow"
  ],
  "practiceArchetype": "guided",
  "flowTier": "tier1"
,
  "steps": [
    {
        "id": "day86-step1",
        "stepNumber": 1,
        "title": "Stack LIFO Mechanics & Array Backing: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Stack Foundations",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Stack Foundations.",
        "markdownContent": [
            "Stacks enforce Last-In, First-Out (LIFO) discipline, supporting O(1) push, pop, and peek operations.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Stack Foundations**, remember the central principle: LIFO discipline restricts mutations to a single boundary, guaranteeing O(1) operations."
        ],
        "snippets": [
            {
                "title": "Stack Foundations Implementation Template",
                "code": "# Stack using Python list\nstack = []\nstack.append(10) # Push\nstack.append(20)\ntop = stack[-1]  # Peek (20)\npopped = stack.pop() # Pop (20)\nprint('Stack:', stack, 'Popped:', popped)",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "LIFO discipline restricts mutations to a single boundary, guaranteeing O(1) operations."
    },
    {
        "id": "day86-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Stack Foundations",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "A stack restricts access strictly to the topmost element. In Python, dynamic lists act as stacks via `append()` and `pop()`, running in amortized O(1) time at the contiguous tail. Alternatively, a singly linked list can back a stack by inserting and removing at head in strict O(1) worst-case time.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: LIFO discipline restricts mutations to a single boundary, guaranteeing O(1) operations.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Stack Foundations Core Invariant",
                "content": "LIFO discipline restricts mutations to a single boundary, guaranteeing O(1) operations."
            }
        ],
        "keyTakeaway": "Operational invariant locked: LIFO discipline restricts mutations to a single boundary, guaranteeing O(1) operations."
    },
    {
        "id": "day86-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Stack Foundations",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d86-q1",
                "question": "Why is `list.pop()` in Python O(1) amortized, but `list.pop(0)` is O(N)?",
                "options": [
                    {
                        "id": "A",
                        "label": "`list.pop()` removes the final element without moving others, whereas `list.pop(0)` requires shifting all N - 1 remaining elements to the left in memory"
                    },
                    {
                        "id": "B",
                        "label": "Because Python lists are doubly linked lists under the hood"
                    },
                    {
                        "id": "C",
                        "label": "Because index 0 is immutable in Python"
                    },
                    {
                        "id": "D",
                        "label": "Because pop() uses binary search"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Python lists are contiguous pointer arrays. Removing from index 0 leaves an empty slot at the beginning, forcing CPython to memmove all remaining N - 1 pointers left by 1 position (O(N)). Removing from the end just decrements the size counter (O(1)).",
                    "B": "Incorrect: Python lists are contiguous arrays, not linked lists.",
                    "C": "Incorrect: All list indices are mutable.",
                    "D": "Incorrect: Pop operates by index offset, not search."
                }
            },
            {
                "id": "chk-d86-q2",
                "question": "What exception is raised when calling `pop()` on an empty Python list?",
                "options": [
                    {
                        "id": "A",
                        "label": "IndexError: pop from empty list"
                    },
                    {
                        "id": "B",
                        "label": "KeyError"
                    },
                    {
                        "id": "C",
                        "label": "ValueError"
                    },
                    {
                        "id": "D",
                        "label": "None is returned"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! In Python, calling pop() on an empty sequence raises an `IndexError`. Always verify `if stack:` before popping.",
                    "B": "Incorrect: KeyError applies to mappings.",
                    "C": "Incorrect: ValueError indicates an invalid value argument.",
                    "D": "Incorrect: Python throws an exception rather than returning None."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day86-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Stack Foundations",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Implement a Stack class with push, pop, peek, and is_empty methods.",
        "subheading": "Implement and verify Stack Foundations in the interactive workspace.",
        "task": {
            "title": "Implement a Stack class with push, pop, peek, and is_empty methods.",
            "instructions": [
                "Implement a Stack class with push, pop, peek, and is_empty methods.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "class ArrayStack:\n    def __init__(self):\n        self._data = []\n\n    # TODO: Implement push(val), pop() -> int, peek() -> int, and is_empty() -> bool\n\ns = ArrayStack()\ns.push(10)\ns.push(20)\nprint('Peek:', s.peek())\nprint('Popped:', s.pop())\nprint('Is empty:', s.is_empty())\n",
            "solutionCode": "class ArrayStack:\n    def __init__(self):\n        self._data = []\n\n    def push(self, val: int) -> None:\n        self._data.append(val)\n\n    def pop(self) -> int:\n        if not self._data:\n            raise IndexError('pop from empty stack')\n        return self._data.pop()\n\n    def peek(self) -> int:\n        if not self._data:\n            raise IndexError('peek from empty stack')\n        return self._data[-1]\n\n    def is_empty(self) -> bool:\n        return len(self._data) == 0\n\ns = ArrayStack()\ns.push(10)\ns.push(20)\nprint('Peek:', s.peek())\nprint('Popped:', s.pop())\nprint('Is empty:', s.is_empty())\n",
            "expectedOutputPatterns": [
                "Peek: 20",
                "Popped: 20",
                "Is empty: False"
            ],
            "hint": "Use append() for push, _data.pop() for pop, _data[-1] for peek, and len(_data) == 0 for is_empty."
        },
        "keyTakeaway": "Successfully implemented and verified Stack Foundations!"
    },
    {
        "id": "day86-step5",
        "stepNumber": 5,
        "title": "Day 86 Complete: Stack LIFO Mechanics & Array Backing",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 86,
        "heading": "Mastery Achieved: Stack LIFO Mechanics & Array Backing",
        "subheading": "You have solidified key mental models and techniques for Stack Foundations.",
        "recapRows": [
            {
                "concept": "LIFO Boundary Protection",
                "naiveIntuition": "Allow arbitrary index access on stacks",
                "pythonReality": "Restricting access strictly to the top element prevents subtle state bugs and preserves algorithmic invariants"
            },
            {
                "concept": "Contiguous Tail Amortization",
                "naiveIntuition": "Dynamic arrays reallocate on every push",
                "pythonReality": "CPython's geometric over-allocation ensures append() and pop() cost O(1) amortized time"
            }
        ],
        "solidifiedConcepts": [
            "LIFO Ordering & Operations",
            "Stack Overflow & Underflow Guards"
        ],
        "nextDayPreview": {
            "dayNumber": 87,
            "title": "Parentheses Matching & Balanced Syntax",
            "description": "Solve balanced parentheses matching with multiple bracket types in O(N) time using a LIFO stack."
        }
    }
]
},
  87: {
  "dayNumber": 87,
  "title": "Parentheses Matching & Balanced Syntax",
  "topicName": "Balanced Syntax",
  "sectionId": "stacks-and-queues",
  "estimatedMinutes": 30,
  "difficulty": "INTERMEDIATE",
  "prerequisites": [
    86
  ],
  "concepts": [
    "Closing-to-Opening Hash Map",
    "Stack Emptiness Termination Invariant"
  ],
  "practiceSkills": [
    "Balanced Syntax Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Validate nested bracket syntax by matching closing brackets against the stack top",
    "Determine syntax correctness in O(N) time and O(N) space"
  ],
  "practiceArchetype": "problem",
  "flowTier": "tier1"
,
  "steps": [
    {
        "id": "day87-step1",
        "stepNumber": 1,
        "title": "Parentheses Matching & Balanced Syntax: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Balanced Syntax",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Balanced Syntax.",
        "markdownContent": [
            "Parentheses Matching evaluates nested syntactic structures by matching closing delimiters against the most recent unmatched opening delimiter stored on a stack.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Balanced Syntax**, remember the central principle: Stacks naturally mirror nested syntactic hierarchy in linear O(N) time."
        ],
        "snippets": [
            {
                "title": "Balanced Syntax Implementation Template",
                "code": "def is_valid(s):\n    mapping = {')': '(', '}': '{', ']': '['}\n    stack = []\n    for ch in s:\n        if ch in mapping:\n            top = stack.pop() if stack else '#'\n            if mapping[ch] != top: return False\n        else:\n            stack.append(ch)\n    return len(stack) == 0",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Stacks naturally mirror nested syntactic hierarchy in linear O(N) time."
    },
    {
        "id": "day87-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Balanced Syntax",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Iterate through characters. If opening bracket, push onto stack. If closing bracket, verify that stack is non-empty and `stack[-1]` matches corresponding opening token (`mapping[ch]`), then pop. Return True if stack is empty at termination.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Stacks naturally mirror nested syntactic hierarchy in linear O(N) time.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Balanced Syntax Core Invariant",
                "content": "Stacks naturally mirror nested syntactic hierarchy in linear O(N) time."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Stacks naturally mirror nested syntactic hierarchy in linear O(N) time."
    },
    {
        "id": "day87-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Balanced Syntax",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d87-q1",
                "question": "If string s has an odd length, why can it be rejected immediately in O(1) time?",
                "options": [
                    {
                        "id": "A",
                        "label": "Because every opening bracket requires an exact matching closing partner, so balanced bracket strings must have an even length"
                    },
                    {
                        "id": "B",
                        "label": "Because Python stacks only accept even counts"
                    },
                    {
                        "id": "C",
                        "label": "Because odd numbers cannot be hashed"
                    },
                    {
                        "id": "D",
                        "label": "It cannot be rejected immediately"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Every bracket must pair with its complement. If `len(s) % 2 != 0`, at least one bracket is guaranteed to remain unmatched, allowing an immediate O(1) early exit.",
                    "B": "Incorrect: Stacks accept any number of elements.",
                    "C": "Incorrect: Hashing has nothing to do with parity.",
                    "D": "Incorrect: Even length is a mandatory mathematical invariant."
                }
            },
            {
                "id": "chk-d87-q2",
                "question": "What error condition is detected if `stack` is empty when encountering a closing bracket `')'`?",
                "options": [
                    {
                        "id": "A",
                        "label": "An unmatched closing delimiter (no corresponding opening bracket preceded it)"
                    },
                    {
                        "id": "B",
                        "label": "An unmatched opening delimiter"
                    },
                    {
                        "id": "C",
                        "label": "A memory overflow"
                    },
                    {
                        "id": "D",
                        "label": "String corruption"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! A closing delimiter needs an existing opening delimiter at the top of the stack. If the stack is empty, there is no opening partner, so the expression is immediately invalid.",
                    "B": "Incorrect: Unmatched opening delimiters are detected when the stack is non-empty at the end of the string.",
                    "C": "Incorrect: No memory overflow occurs.",
                    "D": "Incorrect: Syntactic mismatch is not corruption."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day87-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Balanced Syntax",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Write a function that validates balanced parentheses across () [] and {}.",
        "subheading": "Implement and verify Balanced Syntax in the interactive workspace.",
        "task": {
            "title": "Write a function that validates balanced parentheses across () [] and {}.",
            "instructions": [
                "Write a function that validates balanced parentheses across () [] and {}.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "def is_valid_parentheses(s: str) -> bool:\n    # TODO: Use a stack to validate balanced syntax\n    return False\n\nprint('Test 1:', is_valid_parentheses('()[]{}'))\nprint('Test 2:', is_valid_parentheses('(]'))\nprint('Test 3:', is_valid_parentheses('([)]'))\nprint('Test 4:', is_valid_parentheses('{[]}'))\n",
            "solutionCode": "def is_valid_parentheses(s: str) -> bool:\n    if len(s) % 2 != 0:\n        return False\n    mapping = {')': '(', '}': '{', ']': '['}\n    stack = []\n    for ch in s:\n        if ch in mapping:\n            if not stack or stack[-1] != mapping[ch]:\n                return False\n            stack.pop()\n        else:\n            stack.append(ch)\n    return len(stack) == 0\n\nprint('Test 1:', is_valid_parentheses('()[]{}'))\nprint('Test 2:', is_valid_parentheses('(]'))\nprint('Test 3:', is_valid_parentheses('([)]'))\nprint('Test 4:', is_valid_parentheses('{[]}'))\n",
            "expectedOutputPatterns": [
                "Test 1: True",
                "Test 2: False",
                "Test 3: False",
                "Test 4: True"
            ],
            "hint": "Check if len(s) % 2 != 0. Loop chars: if closing bracket check stack and top match then pop, else append opening bracket. Return len(stack) == 0."
        },
        "keyTakeaway": "Successfully implemented and verified Balanced Syntax!"
    },
    {
        "id": "day87-step5",
        "stepNumber": 5,
        "title": "Day 87 Complete: Parentheses Matching & Balanced Syntax",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 87,
        "heading": "Mastery Achieved: Parentheses Matching & Balanced Syntax",
        "subheading": "You have solidified key mental models and techniques for Balanced Syntax.",
        "recapRows": [
            {
                "concept": "LIFO Nesting Mirror",
                "naiveIntuition": "Count counts of '(' and ')' with counters",
                "pythonReality": "Counters fail to detect interleaved nesting errors like '([)]'; stacks enforce strict hierarchical pairing"
            },
            {
                "concept": "Early Rejection Invariant",
                "naiveIntuition": "Always scan the full string",
                "pythonReality": "Checking len(s) % 2 != 0 and verifying stack state on closing brackets enables immediate early exit"
            }
        ],
        "solidifiedConcepts": [
            "Closing-to-Opening Hash Map",
            "Stack Emptiness Termination Invariant"
        ],
        "nextDayPreview": {
            "dayNumber": 88,
            "title": "Min-Stack Design with O(1) Retrieval",
            "description": "Design a stack supporting push, pop, top, and retrieving the minimum element in O(1) auxiliary time."
        }
    }
]
},
  88: {
  "dayNumber": 88,
  "title": "Min-Stack Design with O(1) Retrieval",
  "topicName": "Min-Stack",
  "sectionId": "stacks-and-queues",
  "estimatedMinutes": 35,
  "difficulty": "INTERMEDIATE",
  "prerequisites": [
    86
  ],
  "concepts": [
    "Auxiliary Min-Tracker Stack",
    "Value-Min State Tuples"
  ],
  "practiceSkills": [
    "Min-Stack Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Architect a stack supporting getMin() in strict O(1) time alongside push() and pop()",
    "Maintain running minimum invariants across push and pop mutations"
  ],
  "practiceArchetype": "algorithm",
  "flowTier": "tier1"
,
  "steps": [
    {
        "id": "day88-step1",
        "stepNumber": 1,
        "title": "Min-Stack Design with O(1) Retrieval: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Min-Stack",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Min-Stack.",
        "markdownContent": [
            "Min Stack achieves O(1) getMin() alongside O(1) push and pop by maintaining a secondary auxiliary stack of minimums or storing (val, current_min) tuples.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Min-Stack**, remember the central principle: Parallel auxiliary stacks preserve invariant histories across reversible push/pop timelines."
        ],
        "snippets": [
            {
                "title": "Min-Stack Implementation Template",
                "code": "# Min Stack dual-stack design\nclass MinStack:\n    def __init__(self):\n        self.stack = []\n        self.min_stack = []\n    def push(self, val):\n        self.stack.append(val)\n        new_min = min(val, self.min_stack[-1]) if self.min_stack else val\n        self.min_stack.append(new_min)\n    def pop(self):\n        self.stack.pop()\n        self.min_stack.pop()\n    def getMin(self):\n        return self.min_stack[-1]",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Parallel auxiliary stacks preserve invariant histories across reversible push/pop timelines."
    },
    {
        "id": "day88-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Min-Stack",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "On `push(x)`: the auxiliary `min_stack` pushes `min(x, min_stack[-1])`. On `pop()`: both the primary stack and `min_stack` pop simultaneously. Thus `min_stack[-1]` always reflects the global minimum of the active stack in strict O(1) time.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Parallel auxiliary stacks preserve invariant histories across reversible push/pop timelines.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Min-Stack Core Invariant",
                "content": "Parallel auxiliary stacks preserve invariant histories across reversible push/pop timelines."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Parallel auxiliary stacks preserve invariant histories across reversible push/pop timelines."
    },
    {
        "id": "day88-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Min-Stack",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d88-q1",
                "question": "Why can't we simply track a single variable `current_min` instead of an auxiliary stack?",
                "options": [
                    {
                        "id": "A",
                        "label": "When the element equal to `current_min` is popped, a single variable cannot recover the previous minimum without an O(N) scan of the entire stack"
                    },
                    {
                        "id": "B",
                        "label": "Because single variables cannot store negative numbers"
                    },
                    {
                        "id": "C",
                        "label": "Because Python functions cannot read global variables"
                    },
                    {
                        "id": "D",
                        "label": "A single variable does work with O(1) pop"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! If the minimum element is popped off, the stack needs to restore the minimum that existed before that element was pushed. A secondary stack records this exact historical timeline.",
                    "B": "Incorrect: Python numbers can be negative.",
                    "C": "Incorrect: Instance attributes are accessible.",
                    "D": "Incorrect: When minimum is popped, finding next minimum takes O(N) without a history structure."
                }
            },
            {
                "id": "chk-d88-q2",
                "question": "What is the auxiliary space complexity of the Min Stack design?",
                "options": [
                    {
                        "id": "A",
                        "label": "O(N) space, where N is the number of active elements"
                    },
                    {
                        "id": "B",
                        "label": "O(1) space"
                    },
                    {
                        "id": "C",
                        "label": "O(N^2) space"
                    },
                    {
                        "id": "D",
                        "label": "O(log N) space"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Each pushed element stores its corresponding minimum in `min_stack`, doubling the memory usage to 2N elements (asymptotically O(N)).",
                    "B": "Incorrect: Historical tracking requires proportional storage.",
                    "C": "Incorrect: Space is linear, not quadratic.",
                    "D": "Incorrect: Logarithmic storage does not store full element histories."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day88-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Min-Stack",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Implement a MinStack that retrieves the minimum element in O(1) time.",
        "subheading": "Implement and verify Min-Stack in the interactive workspace.",
        "task": {
            "title": "Implement a MinStack that retrieves the minimum element in O(1) time.",
            "instructions": [
                "Implement a MinStack that retrieves the minimum element in O(1) time.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "class MinStack:\n    def __init__(self):\n        self.s = []\n        self.ms = []\n\n    # TODO: Implement push(val), pop(), top() -> int, and get_min() -> int\n\nms = MinStack()\nms.push(-2)\nms.push(0)\nms.push(-3)\nprint('Min:', ms.get_min()) # -3\nms.pop()\nprint('Top:', ms.top())     # 0\nprint('Min:', ms.get_min()) # -2\n",
            "solutionCode": "class MinStack:\n    def __init__(self):\n        self.s = []\n        self.ms = []\n\n    def push(self, val: int) -> None:\n        self.s.append(val)\n        m = val if not self.ms else min(val, self.ms[-1])\n        self.ms.append(m)\n\n    def pop(self) -> None:\n        if self.s:\n            self.s.pop()\n            self.ms.pop()\n\n    def top(self) -> int:\n        return self.s[-1] if self.s else -1\n\n    def get_min(self) -> int:\n        return self.ms[-1] if self.ms else -1\n\nms = MinStack()\nms.push(-2)\nms.push(0)\nms.push(-3)\nprint('Min:', ms.get_min())\nms.pop()\nprint('Top:', ms.top())\nprint('Min:', ms.get_min())\n",
            "expectedOutputPatterns": [
                "Min: -3",
                "Top: 0",
                "Min: -2"
            ],
            "hint": "In push: m = val if not self.ms else min(val, self.ms[-1]); ms.append(m). In pop: pop both s and ms. In get_min: return ms[-1]."
        },
        "keyTakeaway": "Successfully implemented and verified Min-Stack!"
    },
    {
        "id": "day88-step5",
        "stepNumber": 5,
        "title": "Day 88 Complete: Min-Stack Design with O(1) Retrieval",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 88,
        "heading": "Mastery Achieved: Min-Stack Design with O(1) Retrieval",
        "subheading": "You have solidified key mental models and techniques for Min-Stack.",
        "recapRows": [
            {
                "concept": "State History Preservation",
                "naiveIntuition": "Calculate min dynamically on demand",
                "pythonReality": "Caching the running minimum at every stack frame enables instant O(1) retrieval"
            },
            {
                "concept": "Time-Space Trade-off",
                "naiveIntuition": "O(1) time requires complex algorithms",
                "pythonReality": "Investing an extra O(N) auxiliary stack collapses getMin() from O(N) linear scan to O(1) lookup"
            }
        ],
        "solidifiedConcepts": [
            "Auxiliary Min-Tracker Stack",
            "Value-Min State Tuples"
        ],
        "nextDayPreview": {
            "dayNumber": 89,
            "title": "Queue FIFO Mechanics & Circular Ring Buffers",
            "description": "Implement First-In-First-Out (FIFO) queue semantics, circular array buffers, and avoid list pop(0) penalties."
        }
    }
]
},
  89: {
  "dayNumber": 89,
  "title": "Queue FIFO Mechanics & Circular Ring Buffers",
  "topicName": "Queue Foundations",
  "sectionId": "stacks-and-queues",
  "estimatedMinutes": 35,
  "difficulty": "INTERMEDIATE",
  "prerequisites": [
    11,
    86
  ],
  "concepts": [
    "FIFO Ordering & Head/Tail Indices",
    "Circular Ring Buffer Modulo Math"
  ],
  "practiceSkills": [
    "Queue Foundations Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Implement a fixed-capacity circular queue using head, tail, and modulo index arithmetic",
    "Explain why list.pop(0) causes O(N) degradation and how ring buffers achieve O(1)"
  ],
  "practiceArchetype": "algorithm",
  "flowTier": "tier1"
,
  "steps": [
    {
        "id": "day89-step1",
        "stepNumber": 1,
        "title": "Queue FIFO Mechanics & Circular Ring Buffers: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Queue Foundations",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Queue Foundations.",
        "markdownContent": [
            "Circular Queues wrap head and tail indices around a fixed-size array using modular arithmetic (`(idx + 1) % capacity`), eliminating memory shifts in hardware buffers.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Queue Foundations**, remember the central principle: Circular ring buffers enable high-performance zero-allocation FIFO streaming in embedded and OS systems."
        ],
        "snippets": [
            {
                "title": "Queue Foundations Implementation Template",
                "code": "# Circular queue modular pointer wrapping\n# tail = (tail + 1) % capacity\n# head = (head + 1) % capacity",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Circular ring buffers enable high-performance zero-allocation FIFO streaming in embedded and OS systems."
    },
    {
        "id": "day89-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Queue Foundations",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "The buffer maintains `head`, `tail`, `size`, and `capacity`. Enqueue: `data[tail] = val; tail = (tail + 1) % capacity; size += 1`. Dequeue: `val = data[head]; head = (head + 1) % capacity; size -= 1`. All operations run in strict O(1) time without re-allocations.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Circular ring buffers enable high-performance zero-allocation FIFO streaming in embedded and OS systems.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Queue Foundations Core Invariant",
                "content": "Circular ring buffers enable high-performance zero-allocation FIFO streaming in embedded and OS systems."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Circular ring buffers enable high-performance zero-allocation FIFO streaming in embedded and OS systems."
    },
    {
        "id": "day89-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Queue Foundations",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d89-q1",
                "question": "Why is modular arithmetic `(idx + 1) % capacity` essential in a circular queue?",
                "options": [
                    {
                        "id": "A",
                        "label": "It causes pointers reaching the end of the array to wrap around to index 0, reusing freed slots at the front"
                    },
                    {
                        "id": "B",
                        "label": "It encrypts queue contents"
                    },
                    {
                        "id": "C",
                        "label": "It automatically expands array size"
                    },
                    {
                        "id": "D",
                        "label": "It prevents duplicate elements"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! When `idx == capacity - 1`, `(capacity - 1 + 1) % capacity == 0`. The pointer smoothly wraps back to index 0 without moving elements.",
                    "B": "Incorrect: Modular indexing is pointer arithmetic, not encryption.",
                    "C": "Incorrect: Array size remains fixed.",
                    "D": "Incorrect: Elements can be duplicated."
                }
            },
            {
                "id": "chk-d89-q2",
                "question": "In a circular queue with capacity K, how do you distinguish between a full queue and an empty queue?",
                "options": [
                    {
                        "id": "A",
                        "label": "By maintaining an explicit `size` counter (empty if `size == 0`, full if `size == capacity`)"
                    },
                    {
                        "id": "B",
                        "label": "By checking if `head == tail`"
                    },
                    {
                        "id": "C",
                        "label": "By sorting the array"
                    },
                    {
                        "id": "D",
                        "label": "Circular queues cannot be full"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! When `head == tail`, the queue could be either completely empty or completely full. Maintaining an explicit `size` counter trivially disambiguates the two states.",
                    "B": "Incorrect: `head == tail` occurs when both empty and full unless an extra dummy slot is reserved.",
                    "C": "Incorrect: Queues are ordered chronologically, not sorted.",
                    "D": "Incorrect: Fixed-capacity buffers can become full."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day89-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Queue Foundations",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Build a Circular Queue with enqueue, dequeue, front, and is_full methods.",
        "subheading": "Implement and verify Queue Foundations in the interactive workspace.",
        "task": {
            "title": "Build a Circular Queue with enqueue, dequeue, front, and is_full methods.",
            "instructions": [
                "Build a Circular Queue with enqueue, dequeue, front, and is_full methods.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "class MyCircularQueue:\n    def __init__(self, k: int):\n        self.cap = k\n        self.data = [0] * k\n        self.head = 0\n        self.tail = 0\n        self.size = 0\n\n    # TODO: Implement en_queue(val) -> bool, de_queue() -> bool, front() -> int, is_full() -> bool\n\nq = MyCircularQueue(3)\nprint('Enq 1:', q.en_queue(1))\nprint('Enq 2:', q.en_queue(2))\nprint('Enq 3:', q.en_queue(3))\nprint('Enq 4 (overflow):', q.en_queue(4))\nprint('Front:', q.front())\nprint('Deq:', q.de_queue())\nprint('Enq 4 (now ok):', q.en_queue(4))\n",
            "solutionCode": "class MyCircularQueue:\n    def __init__(self, k: int):\n        self.cap = k\n        self.data = [0] * k\n        self.head = 0\n        self.tail = 0\n        self.size = 0\n\n    def en_queue(self, val: int) -> bool:\n        if self.is_full():\n            return False\n        self.data[self.tail] = val\n        self.tail = (self.tail + 1) % self.cap\n        self.size += 1\n        return True\n\n    def de_queue(self) -> bool:\n        if self.size == 0:\n            return False\n        self.head = (self.head + 1) % self.cap\n        self.size -= 1\n        return True\n\n    def front(self) -> int:\n        if self.size == 0:\n            return -1\n        return self.data[self.head]\n\n    def is_full(self) -> bool:\n        return self.size == self.cap\n\nq = MyCircularQueue(3)\nprint('Enq 1:', q.en_queue(1))\nprint('Enq 2:', q.en_queue(2))\nprint('Enq 3:', q.en_queue(3))\nprint('Enq 4 (overflow):', q.en_queue(4))\nprint('Front:', q.front())\nprint('Deq:', q.de_queue())\nprint('Enq 4 (now ok):', q.en_queue(4))\n",
            "expectedOutputPatterns": [
                "Enq 1: True",
                "Enq 2: True",
                "Enq 3: True",
                "Enq 4 (overflow): False",
                "Front: 1",
                "Deq: True",
                "Enq 4 (now ok): True"
            ],
            "hint": "Check is_full() in en_queue, assign data[tail]=val, tail=(tail+1)%cap, size+=1. In de_queue check size==0, head=(head+1)%cap, size-=1."
        },
        "keyTakeaway": "Successfully implemented and verified Queue Foundations!"
    },
    {
        "id": "day89-step5",
        "stepNumber": 5,
        "title": "Day 89 Complete: Queue FIFO Mechanics & Circular Ring Buffers",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 89,
        "heading": "Mastery Achieved: Queue FIFO Mechanics & Circular Ring Buffers",
        "subheading": "You have solidified key mental models and techniques for Queue Foundations.",
        "recapRows": [
            {
                "concept": "Ring Buffer Wraparound",
                "naiveIntuition": "Shift all array elements forward on dequeue",
                "pythonReality": "Advancing head with modular arithmetic reclaims capacity in O(1) time without touching array data"
            },
            {
                "concept": "Zero Dynamic Allocation",
                "naiveIntuition": "Queues must dynamically grow and shrink",
                "pythonReality": "Fixed circular buffers eliminate garbage collection spikes in latency-critical packet routers and audio buffers"
            }
        ],
        "solidifiedConcepts": [
            "FIFO Ordering & Head/Tail Indices",
            "Circular Ring Buffer Modulo Math"
        ],
        "nextDayPreview": {
            "dayNumber": 90,
            "title": "Implement Queue Using Two Stacks",
            "description": "Implement a FIFO queue using two LIFO stacks, proving amortized O(1) time per operation via lazy transfers."
        }
    }
]
},
  90: {
  "dayNumber": 90,
  "title": "Implement Queue Using Two Stacks",
  "topicName": "Two-Stack Queue",
  "sectionId": "stacks-and-queues",
  "estimatedMinutes": 30,
  "difficulty": "INTERMEDIATE",
  "prerequisites": [
    86,
    89
  ],
  "concepts": [
    "Input Stack & Output Stack",
    "Amortized O(1) Transfer Invariant"
  ],
  "practiceSkills": [
    "Two-Stack Queue Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Simulate FIFO queue behavior using two LIFO stacks",
    "Prove amortized O(1) time per element using potential function accounting"
  ],
  "practiceArchetype": "algorithm",
  "flowTier": "tier1"
,
  "steps": [
    {
        "id": "day90-step1",
        "stepNumber": 1,
        "title": "Implement Queue Using Two Stacks: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Two-Stack Queue",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Two-Stack Queue.",
        "markdownContent": [
            "Implementing a FIFO Queue using Two LIFO Stacks transfers elements from an input stack to an output stack lazily, achieving amortized O(1) push and pop.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Two-Stack Queue**, remember the central principle: Reversing LIFO twice yields FIFO; lazy batch transfers ensure amortized O(1) queue operations."
        ],
        "snippets": [
            {
                "title": "Two-Stack Queue Implementation Template",
                "code": "# Queue using Two Stacks\nclass MyQueue:\n    def __init__(self):\n        self.in_stk = []; self.out_stk = []\n    def push(self, x):\n        self.in_stk.append(x)\n    def pop(self):\n        self.peek()\n        return self.out_stk.pop()\n    def peek(self):\n        if not self.out_stk:\n            while self.in_stk: self.out_stk.append(self.in_stk.pop())\n        return self.out_stk[-1]\n    def empty(self):\n        return not self.in_stk and not self.out_stk",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Reversing LIFO twice yields FIFO; lazy batch transfers ensure amortized O(1) queue operations."
    },
    {
        "id": "day90-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Two-Stack Queue",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Maintain two stacks: `in_stack` (for push) and `out_stack` (for pop/peek). Push appends to `in_stack` in O(1). When popping or peeking: if `out_stack` is empty, pop all elements from `in_stack` and push them into `out_stack`, reversing their order to restore FIFO! Amortized analysis: each element is pushed and popped at most twice, averaging O(1) across all operations.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Reversing LIFO twice yields FIFO; lazy batch transfers ensure amortized O(1) queue operations.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Two-Stack Queue Core Invariant",
                "content": "Reversing LIFO twice yields FIFO; lazy batch transfers ensure amortized O(1) queue operations."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Reversing LIFO twice yields FIFO; lazy batch transfers ensure amortized O(1) queue operations."
    },
    {
        "id": "day90-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Two-Stack Queue",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d90-q1",
                "question": "Why is the amortized time complexity of `pop()` and `peek()` in a two-stack queue O(1), even though transferring elements takes O(N) when out_stack is empty?",
                "options": [
                    {
                        "id": "A",
                        "label": "Each element is moved from in_stack to out_stack exactly once across its entire lifetime in the queue; the O(N) transfer cost is distributed over N individual O(1) operations"
                    },
                    {
                        "id": "B",
                        "label": "Because transferring uses a C compiler optimization"
                    },
                    {
                        "id": "C",
                        "label": "Because out_stack is never empty"
                    },
                    {
                        "id": "D",
                        "label": "Because Python stacks are doubly linked lists"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! By the accounting method of amortized analysis, each item has 2 pushes and 2 pops across its entire journey. 4 operations per item = amortized O(1) constant time.",
                    "B": "Incorrect: Algorithmic complexity is mathematical, not compiler dependent.",
                    "C": "Incorrect: out_stack starts empty.",
                    "D": "Incorrect: Python lists are contiguous arrays."
                }
            },
            {
                "id": "chk-d90-q2",
                "question": "When should elements be moved from `in_stack` to `out_stack`?",
                "options": [
                    {
                        "id": "A",
                        "label": "ONLY when out_stack is completely empty; premature transfers would scramble the relative FIFO arrival order of newer elements"
                    },
                    {
                        "id": "B",
                        "label": "After every single push"
                    },
                    {
                        "id": "C",
                        "label": "Whenever in_stack has more than 5 elements"
                    },
                    {
                        "id": "D",
                        "label": "At random intervals"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! If out_stack still holds older elements, pouring newer elements on top of them would violate FIFO order. Only refill out_stack when it is fully drained.",
                    "B": "Incorrect: Transferring after every push would degrade push to O(N).",
                    "C": "Incorrect: Transfers must be strictly demand-driven.",
                    "D": "Incorrect: Data structures require deterministic ordering invariants."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day90-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Two-Stack Queue",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Implement a First-In, First-Out (FIFO) queue using two LIFO stacks.",
        "subheading": "Implement and verify Two-Stack Queue in the interactive workspace.",
        "task": {
            "title": "Implement a First-In, First-Out (FIFO) queue using two LIFO stacks.",
            "instructions": [
                "Implement a First-In, First-Out (FIFO) queue using two LIFO stacks.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "class MyQueue:\n    def __init__(self):\n        self.in_stack = []\n        self.out_stack = []\n\n    # TODO: Implement push(x), pop() -> int, peek() -> int, and empty() -> bool\n\nq = MyQueue()\nq.push(1)\nq.push(2)\nprint('Peek:', q.peek()) # 1\nprint('Pop:', q.pop())   # 1\nprint('Empty:', q.empty()) # False\n",
            "solutionCode": "class MyQueue:\n    def __init__(self):\n        self.in_stack = []\n        self.out_stack = []\n\n    def push(self, x: int) -> None:\n        self.in_stack.append(x)\n\n    def pop(self) -> int:\n        self.peek()\n        return self.out_stack.pop()\n\n    def peek(self) -> int:\n        if not self.out_stack:\n            while self.in_stack:\n                self.out_stack.append(self.in_stack.pop())\n        return self.out_stack[-1]\n\n    def empty(self) -> bool:\n        return not self.in_stack and not self.out_stack\n\nq = MyQueue()\nq.push(1)\nq.push(2)\nprint('Peek:', q.peek())\nprint('Pop:', q.pop())\nprint('Empty:', q.empty())\n",
            "expectedOutputPatterns": [
                "Peek: 1",
                "Pop: 1",
                "Empty: False"
            ],
            "hint": "In push: in_stack.append(x). In peek: if not out_stack: while in_stack: out_stack.append(in_stack.pop()); return out_stack[-1]. In pop: peek() and out_stack.pop()."
        },
        "keyTakeaway": "Successfully implemented and verified Two-Stack Queue!"
    },
    {
        "id": "day90-step5",
        "stepNumber": 5,
        "title": "Day 90 Complete: Implement Queue Using Two Stacks",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 90,
        "heading": "Mastery Achieved: Implement Queue Using Two Stacks",
        "subheading": "You have solidified key mental models and techniques for Two-Stack Queue.",
        "recapRows": [
            {
                "concept": "Double Inversion Identity",
                "naiveIntuition": "Stacks can never act as queues",
                "pythonReality": "Inverting a stack twice restores the original FIFO order, proving structural duality between queues and stacks"
            },
            {
                "concept": "Amortized Efficiency",
                "naiveIntuition": "Occasional O(N) operations mean the algorithm is slow",
                "pythonReality": "Infrequent batch transfers averaged over thousands of items maintain sub-microsecond latency"
            }
        ],
        "solidifiedConcepts": [
            "Input Stack & Output Stack",
            "Amortized O(1) Transfer Invariant"
        ],
        "nextDayPreview": {
            "dayNumber": 91,
            "title": "Monotonic Stack: Next Greater Element",
            "description": "Master the monotonic stack pattern to solve Next Greater Element and stock span problems in linear O(N) time."
        }
    }
]
},
  91: {
  "dayNumber": 91,
  "title": "Monotonic Stack: Next Greater Element",
  "topicName": "Monotonic Stack",
  "sectionId": "stacks-and-queues",
  "estimatedMinutes": 40,
  "difficulty": "INTERMEDIATE",
  "prerequisites": [
    86
  ],
  "concepts": [
    "Monotonically Decreasing Stack",
    "Immediate Pop Resolution"
  ],
  "practiceSkills": [
    "Monotonic Stack Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Maintain a monotonically decreasing stack of array indices to find next greater elements",
    "Process array elements in O(N) total time by amortizing pushes and pops"
  ],
  "practiceArchetype": "problem",
  "flowTier": "tier2"
,
  "steps": [
    {
        "id": "day91-step1",
        "stepNumber": 1,
        "title": "Monotonic Stack: Next Greater Element: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Monotonic Stack",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Monotonic Stack.",
        "markdownContent": [
            "Monotonic Stacks maintain elements in strictly monotonic (increasing or decreasing) order, finding the Next Greater Element for all array items in amortized O(N) time.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Monotonic Stack**, remember the central principle: Each index is pushed and popped at most once, achieving amortized O(N) resolution of nearest greater/smaller queries."
        ],
        "snippets": [
            {
                "title": "Monotonic Stack Implementation Template",
                "code": "# Next Greater Element\ndef next_greater(nums):\n    res = [-1] * len(nums)\n    stack = [] # indices\n    for i, x in enumerate(nums):\n        while stack and nums[stack[-1]] < x:\n            prev_idx = stack.pop()\n            res[prev_idx] = x\n        stack.append(i)\n    return res",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Each index is pushed and popped at most once, achieving amortized O(N) resolution of nearest greater/smaller queries."
    },
    {
        "id": "day91-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Monotonic Stack",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Maintain a stack of indices with decreasing values. When visiting `arr[i]`: while stack is non-empty and `arr[i] > arr[stack[-1]]`, pop index `idx` from stack; `arr[i]` is the Next Greater Element for `idx`. Then push `i`. Elements left on the stack have no greater element.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Each index is pushed and popped at most once, achieving amortized O(N) resolution of nearest greater/smaller queries.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Monotonic Stack Core Invariant",
                "content": "Each index is pushed and popped at most once, achieving amortized O(N) resolution of nearest greater/smaller queries."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Each index is pushed and popped at most once, achieving amortized O(N) resolution of nearest greater/smaller queries."
    },
    {
        "id": "day91-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Monotonic Stack",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d91-q1",
                "question": "Why is the time complexity of the monotonic stack algorithm O(N) even though there is a nested while loop inside the for loop?",
                "options": [
                    {
                        "id": "A",
                        "label": "Each element is pushed onto the stack exactly once and popped at most once, bounding total operations by 2N = O(N)"
                    },
                    {
                        "id": "B",
                        "label": "Because the array is sorted"
                    },
                    {
                        "id": "C",
                        "label": "Because the while loop only runs once per execution"
                    },
                    {
                        "id": "D",
                        "label": "Because Python lists optimize inner loops"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Across the entire execution of the outer loop (N iterations), at most N elements are pushed, so at most N elements can ever be popped. The amortized cost per element is O(1).",
                    "B": "Incorrect: Monotonic stack works on completely arbitrary unsorted arrays.",
                    "C": "Incorrect: The while loop can pop multiple elements in a single iteration.",
                    "D": "Incorrect: Complexity is an algorithmic property, not an interpreter optimization."
                }
            },
            {
                "id": "chk-d91-q2",
                "question": "Why does the monotonic stack store indices rather than raw values?",
                "options": [
                    {
                        "id": "A",
                        "label": "Indices allow updating the result array at the exact original position and computing horizontal distances"
                    },
                    {
                        "id": "B",
                        "label": "Python lists cannot store numbers directly in stacks"
                    },
                    {
                        "id": "C",
                        "label": "Indices require less memory than integers"
                    },
                    {
                        "id": "D",
                        "label": "Because values are converted to strings"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Storing indices gives dual power: `nums[idx]` yields the value, while `idx` allows updating `res[idx] = x` and measuring horizontal span (`i - idx`).",
                    "B": "Incorrect: Python stacks can store any object.",
                    "C": "Incorrect: Both are integers in CPython.",
                    "D": "Incorrect: No string conversion occurs."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day91-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Monotonic Stack",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Find the Next Greater Element for each array entry (return -1 if none exists).",
        "subheading": "Implement and verify Monotonic Stack in the interactive workspace.",
        "task": {
            "title": "Find the Next Greater Element for each array entry (return -1 if none exists).",
            "instructions": [
                "Find the Next Greater Element for each array entry (return -1 if none exists).",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "def next_greater_elements(nums: list[int]) -> list[int]:\n    # TODO: Use a monotonic decreasing stack of indices\n    # Return array of next greater elements\n    return []\n\nprint('NGE:', next_greater_elements([2, 1, 2, 4, 3]))\n",
            "solutionCode": "def next_greater_elements(nums: list[int]) -> list[int]:\n    res = [-1] * len(nums)\n    stack = []\n    for i, x in enumerate(nums):\n        while stack and nums[stack[-1]] < x:\n            idx = stack.pop()\n            res[idx] = x\n        stack.append(i)\n    return res\n\nprint('NGE:', next_greater_elements([2, 1, 2, 4, 3]))\n",
            "expectedOutputPatterns": [
                "NGE: [4, 2, 4, -1, -1]"
            ],
            "hint": "Initialize res = [-1] * len(nums), stack = []. Loop i, x: while stack and nums[stack[-1]] < x: res[stack.pop()] = x; stack.append(i). Return res."
        },
        "keyTakeaway": "Successfully implemented and verified Monotonic Stack!"
    },
    {
        "id": "day91-step5",
        "stepNumber": 5,
        "title": "Day 91 Complete: Monotonic Stack: Next Greater Element",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 91,
        "heading": "Mastery Achieved: Monotonic Stack: Next Greater Element",
        "subheading": "You have solidified key mental models and techniques for Monotonic Stack.",
        "recapRows": [
            {
                "concept": "Amortized Linear Bound",
                "naiveIntuition": "Nested loops imply O(N^2) quadratic time",
                "pythonReality": "Monotonic stacks guarantee that each element enters and exits the stack at most once, yielding strictly O(N) aggregate time"
            },
            {
                "concept": "Monotonic Invariant",
                "naiveIntuition": "Check all rightward elements sequentially",
                "pythonReality": "Stack elements represent active queries waiting for their first larger successor; popping on arrival resolves them instantly"
            }
        ],
        "solidifiedConcepts": [
            "Monotonically Decreasing Stack",
            "Immediate Pop Resolution"
        ],
        "nextDayPreview": {
            "dayNumber": 92,
            "title": "Monotonic Stack: Largest Histogram Rectangle",
            "description": "Apply monotonic stacks to compute the largest rectangular area in histograms and maximal binary rectangles in O(N) time."
        }
    }
]
},
  92: {
  "dayNumber": 92,
  "title": "Monotonic Stack: Largest Histogram Rectangle",
  "topicName": "Histogram Monotonic Stack",
  "sectionId": "stacks-and-queues",
  "estimatedMinutes": 45,
  "difficulty": "INTERMEDIATE",
  "prerequisites": [
    91
  ],
  "concepts": [
    "Left & Right Smaller Bounds",
    "Width Calculation from Popped Index"
  ],
  "practiceSkills": [
    "Histogram Monotonic Stack Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Calculate maximum rectangular area under a histogram in O(N) time using a monotonic stack",
    "Extend histogram algorithms to solve Maximal Rectangle in 2D binary matrices"
  ],
  "practiceArchetype": "problem",
  "flowTier": "tier3"
,
  "steps": [
    {
        "id": "day92-step1",
        "stepNumber": 1,
        "title": "Monotonic Stack: Largest Histogram Rectangle: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Histogram Monotonic Stack",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Histogram Monotonic Stack.",
        "markdownContent": [
            "Largest Rectangle in Histogram utilizes a Monotonic Increasing Stack to determine the left and right boundaries where each bar is the limiting height, running in O(N) time.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Histogram Monotonic Stack**, remember the central principle: Monotonic increasing stacks identify left/right smaller boundaries to compute maximal areas in O(N) time."
        ],
        "snippets": [
            {
                "title": "Histogram Monotonic Stack Implementation Template",
                "code": "# Largest Rectangle in Histogram\ndef largest_rectangle_area(heights):\n    stack = [-1] # Sentinel index\n    max_area = 0\n    heights.append(0) # Sentinel flush\n    for i, h in enumerate(heights):\n        while stack[-1] != -1 and heights[stack[-1]] >= h:\n            height = heights[stack.pop()]\n            width = i - stack[-1] - 1\n            max_area = max(max_area, height * width)\n        stack.append(i)\n    heights.pop()\n    return max_area",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Monotonic increasing stacks identify left/right smaller boundaries to compute maximal areas in O(N) time."
    },
    {
        "id": "day92-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Histogram Monotonic Stack",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "For each bar of height H, the rectangle width extends left to the first smaller bar and right to the first smaller bar. When a shorter bar arrives, it pops taller bars from the stack. The popped bar's area is: `height * (current_index - stack[-1] - 1)`. Padding with boundary zero-height sentinels simplifies draining.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Monotonic increasing stacks identify left/right smaller boundaries to compute maximal areas in O(N) time.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Histogram Monotonic Stack Core Invariant",
                "content": "Monotonic increasing stacks identify left/right smaller boundaries to compute maximal areas in O(N) time."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Monotonic increasing stacks identify left/right smaller boundaries to compute maximal areas in O(N) time."
    },
    {
        "id": "day92-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Histogram Monotonic Stack",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d92-q1",
                "question": "Why do we pad the heights list with a sentinel value of 0 at the end?",
                "options": [
                    {
                        "id": "A",
                        "label": "To force all remaining bars on the stack to be popped and their areas calculated before algorithm termination"
                    },
                    {
                        "id": "B",
                        "label": "To make the array length an even number"
                    },
                    {
                        "id": "C",
                        "label": "Because histogram bars cannot have height 0"
                    },
                    {
                        "id": "D",
                        "label": "To reset CPU cache lines"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Because heights are non-negative, appending 0 guarantees that every bar remaining on the monotonic increasing stack is strictly greater than 0, cleanly draining the stack without duplicate cleanup loops.",
                    "B": "Incorrect: Parity is irrelevant.",
                    "C": "Incorrect: Bars can have height 0.",
                    "D": "Incorrect: Algorithmic sentinel has no relation to cache lines."
                }
            },
            {
                "id": "chk-d92-q2",
                "question": "When bar `H` is popped from the stack between `stack[-1]` and `current_i`, what is its effective rectangle width?",
                "options": [
                    {
                        "id": "A",
                        "label": "`current_i - stack[-1] - 1`"
                    },
                    {
                        "id": "B",
                        "label": "`current_i - stack[-1]`"
                    },
                    {
                        "id": "C",
                        "label": "`current_i + 1`"
                    },
                    {
                        "id": "D",
                        "label": "`len(heights)`"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! The limiting bar spans strictly between the smaller left boundary `stack[-1]` and smaller right boundary `current_i`. The number of bars strictly between them is `current_i - stack[-1] - 1`.",
                    "B": "Incorrect: That includes one of the smaller boundary indices.",
                    "C": "Incorrect: Does not account for left bound.",
                    "D": "Incorrect: That is total array length."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day92-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Histogram Monotonic Stack",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Calculate the largest rectangular area in an input histogram.",
        "subheading": "Implement and verify Histogram Monotonic Stack in the interactive workspace.",
        "task": {
            "title": "Calculate the largest rectangular area in an input histogram.",
            "instructions": [
                "Calculate the largest rectangular area in an input histogram.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "def largest_rectangle(heights: list[int]) -> int:\n    # TODO: Implement largest rectangle using a monotonic increasing stack\n    return 0\n\nprint('Max Area 1:', largest_rectangle([2, 1, 5, 6, 2, 3])) # 10\nprint('Max Area 2:', largest_rectangle([2, 4]))             # 4\n",
            "solutionCode": "def largest_rectangle(heights: list[int]) -> int:\n    h_copy = heights + [0]\n    stack = [-1]\n    max_area = 0\n    for i, h in enumerate(h_copy):\n        while stack[-1] != -1 and h_copy[stack[-1]] >= h:\n            height = h_copy[stack.pop()]\n            width = i - stack[-1] - 1\n            max_area = max(max_area, height * width)\n        stack.append(i)\n    return max_area\n\nprint('Max Area 1:', largest_rectangle([2, 1, 5, 6, 2, 3]))\nprint('Max Area 2:', largest_rectangle([2, 4]))\n",
            "expectedOutputPatterns": [
                "Max Area 1: 10",
                "Max Area 2: 4"
            ],
            "hint": "Append 0 to heights copy. stack = [-1], max_area = 0. While stack[-1] != -1 and h_copy[stack[-1]] >= h: height = h_copy[stack.pop()], width = i - stack[-1] - 1, max_area = max(max_area, height * width). stack.append(i)."
        },
        "keyTakeaway": "Successfully implemented and verified Histogram Monotonic Stack!"
    },
    {
        "id": "day92-step5",
        "stepNumber": 5,
        "title": "Day 92 Complete: Monotonic Stack: Largest Histogram Rectangle",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 92,
        "heading": "Mastery Achieved: Monotonic Stack: Largest Histogram Rectangle",
        "subheading": "You have solidified key mental models and techniques for Histogram Monotonic Stack.",
        "recapRows": [
            {
                "concept": "Boundary Sentinels",
                "naiveIntuition": "Write a separate loop to pop remaining bars after the main loop",
                "pythonReality": "Padding input with sentinel 0 flushes the monotonic stack naturally, eliminating code duplication"
            },
            {
                "concept": "Width Derivation Invariant",
                "naiveIntuition": "Width is simply index distance from start",
                "pythonReality": "The stack index immediately below the popped element marks the exact left bound of smaller height"
            }
        ],
        "solidifiedConcepts": [
            "Left & Right Smaller Bounds",
            "Width Calculation from Popped Index"
        ],
        "nextDayPreview": {
            "dayNumber": 93,
            "title": "Monotonic Queue & Sliding Window Maximum",
            "description": "Implement monotonic double-ended queues (deques) to solve the Sliding Window Maximum problem in O(N) time."
        }
    }
]
},
  93: {
  "dayNumber": 93,
  "title": "Monotonic Queue & Sliding Window Maximum",
  "topicName": "Monotonic Queue",
  "sectionId": "stacks-and-queues",
  "estimatedMinutes": 40,
  "difficulty": "INTERMEDIATE",
  "prerequisites": [
    18,
    91
  ],
  "concepts": [
    "Monotonically Decreasing Deque",
    "Out-of-Window Index Eviction"
  ],
  "practiceSkills": [
    "Monotonic Queue Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Maintain a double-ended queue storing candidate maximums in strictly descending order",
    "Solve the Sliding Window Maximum problem in strict O(N) time and O(K) space"
  ],
  "practiceArchetype": "problem",
  "flowTier": "tier2"
,
  "steps": [
    {
        "id": "day93-step1",
        "stepNumber": 1,
        "title": "Monotonic Queue & Sliding Window Maximum: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Monotonic Queue",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Monotonic Queue.",
        "markdownContent": [
            "Monotonic Deques maintain elements in monotonically decreasing order to solve the Sliding Window Maximum problem in amortized O(N) time.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Monotonic Queue**, remember the central principle: Monotonic deques maintain candidates for window extremums, pruning suboptimal elements in O(1) amortized time."
        ],
        "snippets": [
            {
                "title": "Monotonic Queue Implementation Template",
                "code": "from collections import deque\ndef max_sliding_window(nums, k):\n    q = deque() # indices\n    res = []\n    for i, x in enumerate(nums):\n        if q and q[0] <= i - k: q.popleft()\n        while q and nums[q[-1]] <= x: q.pop()\n        q.append(i)\n        if i >= k - 1: res.append(nums[q[0]])\n    return res",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Monotonic deques maintain candidates for window extremums, pruning suboptimal elements in O(1) amortized time."
    },
    {
        "id": "day93-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Monotonic Queue",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "A double-ended queue (`deque`) stores indices. For each new index `i`: (1) Evict expired indices from the front: `while q and q[0] <= i - k: q.popleft()`. (2) Evict smaller elements from the back: `while q and nums[q[-1]] <= nums[i]: q.pop()`. (3) Append `i`. The window maximum is always at `nums[q[0]]`.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Monotonic deques maintain candidates for window extremums, pruning suboptimal elements in O(1) amortized time.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Monotonic Queue Core Invariant",
                "content": "Monotonic deques maintain candidates for window extremums, pruning suboptimal elements in O(1) amortized time."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Monotonic deques maintain candidates for window extremums, pruning suboptimal elements in O(1) amortized time."
    },
    {
        "id": "day93-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Monotonic Queue",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d93-q1",
                "question": "Why can elements smaller than `nums[i]` be safely popped from the back of the deque when `nums[i]` enters the window?",
                "options": [
                    {
                        "id": "A",
                        "label": "Because `nums[i]` is both larger and will stay in the sliding window longer than those preceding smaller elements, rendering them useless as potential maximums"
                    },
                    {
                        "id": "B",
                        "label": "Because the deque has a fixed capacity of 5"
                    },
                    {
                        "id": "C",
                        "label": "To save battery on mobile devices"
                    },
                    {
                        "id": "D",
                        "label": "Because Python deque requires sorted values"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Any element that is older (smaller index) AND smaller in value can never be the maximum of any current or future window that contains `nums[i]`. It is permanently dominated.",
                    "B": "Incorrect: Deque grows dynamically.",
                    "C": "Incorrect: Algorithmic dominance is independent of hardware.",
                    "D": "Incorrect: Deque itself enforces no sorting."
                }
            },
            {
                "id": "chk-d93-q2",
                "question": "What is the total time complexity of Sliding Window Maximum across an array of length N using a monotonic deque?",
                "options": [
                    {
                        "id": "A",
                        "label": "O(N) amortized time"
                    },
                    {
                        "id": "B",
                        "label": "O(N * K)"
                    },
                    {
                        "id": "C",
                        "label": "O(N log K)"
                    },
                    {
                        "id": "D",
                        "label": "O(N^2)"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Every element index enters the deque once and leaves the deque at most once (either from the back when dominated or from the front when expired). Total operations $\\le 2N = O(N)$.",
                    "B": "Incorrect: O(N * K) is the naive brute force sliding window.",
                    "C": "Incorrect: O(N log K) is the heap or balanced BST approach.",
                    "D": "Incorrect: Monotonic deque completely avoids quadratic scans."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day93-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Monotonic Queue",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Find the maximum value in every sliding window of size K.",
        "subheading": "Implement and verify Monotonic Queue in the interactive workspace.",
        "task": {
            "title": "Find the maximum value in every sliding window of size K.",
            "instructions": [
                "Find the maximum value in every sliding window of size K.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "from collections import deque\n\ndef sliding_max(nums: list[int], k: int) -> list[int]:\n    # TODO: Implement sliding window maximum using collections.deque\n    return []\n\nnums = [1, 3, -1, -3, 5, 3, 6, 7]\nprint('Sliding max (k=3):', sliding_max(nums, 3))\n",
            "solutionCode": "from collections import deque\n\ndef sliding_max(nums: list[int], k: int) -> list[int]:\n    q = deque()\n    res = []\n    for i, x in enumerate(nums):\n        if q and q[0] <= i - k:\n            q.popleft()\n        while q and nums[q[-1]] <= x:\n            q.pop()\n        q.append(i)\n        if i >= k - 1:\n            res.append(nums[q[0]])\n    return res\n\nnums = [1, 3, -1, -3, 5, 3, 6, 7]\nprint('Sliding max (k=3):', sliding_max(nums, 3))\n",
            "expectedOutputPatterns": [
                "Sliding max (k=3): [3, 3, 5, 5, 6, 7]"
            ],
            "hint": "Loop i, x: if q and q[0] <= i - k: q.popleft(); while q and nums[q[-1]] <= x: q.pop(); q.append(i); if i >= k - 1: res.append(nums[q[0]]). Return res."
        },
        "keyTakeaway": "Successfully implemented and verified Monotonic Queue!"
    },
    {
        "id": "day93-step5",
        "stepNumber": 5,
        "title": "Day 93 Complete: Monotonic Queue & Sliding Window Maximum",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 93,
        "heading": "Mastery Achieved: Monotonic Queue & Sliding Window Maximum",
        "subheading": "You have solidified key mental models and techniques for Monotonic Queue.",
        "recapRows": [
            {
                "concept": "Domination Invariant",
                "naiveIntuition": "Keep all window elements in container",
                "pythonReality": "Pruning elements that are both smaller and older eliminates clutter, ensuring the front always holds the maximum in O(1)"
            },
            {
                "concept": "Bidirectional Pruning",
                "naiveIntuition": "Queues only pop from one side",
                "pythonReality": "A deque permits popping expired elements from the front and dominated elements from the back"
            }
        ],
        "solidifiedConcepts": [
            "Monotonically Decreasing Deque",
            "Out-of-Window Index Eviction"
        ],
        "nextDayPreview": {
            "dayNumber": 94,
            "title": "Expression Parsing & Shunting-Yard Algorithm",
            "description": "Implement Dijkstra's Shunting-Yard algorithm to parse infix expressions into postfix RPN and evaluate them."
        }
    }
]
},
  94: {
  "dayNumber": 94,
  "title": "Expression Parsing & Shunting-Yard Algorithm",
  "topicName": "Expression Parsing",
  "sectionId": "stacks-and-queues",
  "estimatedMinutes": 45,
  "difficulty": "INTERMEDIATE",
  "prerequisites": [
    86,
    87
  ],
  "concepts": [
    "Operator Precedence & Associativity",
    "Dijkstra's Shunting-Yard (Infix to Postfix)"
  ],
  "practiceSkills": [
    "Expression Parsing Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Convert infix mathematical expressions into postfix Reverse Polish Notation (RPN)",
    "Evaluate composite arithmetic expressions containing parentheses, +, -, *, / in O(N) time"
  ],
  "practiceArchetype": "algorithm",
  "flowTier": "tier3"
,
  "steps": [
    {
        "id": "day94-step1",
        "stepNumber": 1,
        "title": "Expression Parsing & Shunting-Yard Algorithm: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Expression Parsing",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Expression Parsing.",
        "markdownContent": [
            "The Shunting-Yard Algorithm parses infix mathematical expressions into Postfix (Reverse Polish Notation) or directly evaluates them using an Operator Stack and Operand Stack.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Expression Parsing**, remember the central principle: Operator precedence stacks ensure high-precedence operations (*, /) execute before lower-precedence ones (+, -)."
        ],
        "snippets": [
            {
                "title": "Expression Parsing Implementation Template",
                "code": "# Basic Calculator Expression Evaluator\ndef calculate(s):\n    vals, ops = [], []\n    prec = {'+': 1, '-': 1, '*': 2, '/': 2}\n    def apply():\n        op = ops.pop(); b = vals.pop(); a = vals.pop()\n        if op == '+': vals.append(a + b)\n        elif op == '-': vals.append(a - b)\n        elif op == '*': vals.append(a * b)\n        elif op == '/': vals.append(int(a / b))\n    i = 0\n    while i < len(s):\n        if s[i].isdigit():\n            n = 0\n            while i < len(s) and s[i].isdigit(): n = n * 10 + int(s[i]); i += 1\n            vals.append(n); continue\n        elif s[i] in prec:\n            while ops and ops[-1] in prec and prec[ops[-1]] >= prec[s[i]]: apply()\n            ops.append(s[i])\n        elif s[i] == '(': ops.append('(')\n        elif s[i] == ')':\n            while ops[-1] != '(': apply()\n            ops.pop()\n        i += 1\n    while ops: apply()\n    return vals[0]",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Operator precedence stacks ensure high-precedence operations (*, /) execute before lower-precedence ones (+, -)."
    },
    {
        "id": "day94-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Expression Parsing",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Read tokens left to right: (1) If number, push to values. (2) If '(', push to ops. (3) If ')', pop and apply operators until '(' is matched. (4) If operator (+, -, *, /): while top of ops has >= precedence, pop and apply. Push current operator. At end, apply remaining operators in ops. Evaluates expressions in strictly O(N) time.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Operator precedence stacks ensure high-precedence operations (*, /) execute before lower-precedence ones (+, -).\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Expression Parsing Core Invariant",
                "content": "Operator precedence stacks ensure high-precedence operations (*, /) execute before lower-precedence ones (+, -)."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Operator precedence stacks ensure high-precedence operations (*, /) execute before lower-precedence ones (+, -)."
    },
    {
        "id": "day94-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Expression Parsing",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d94-q1",
                "question": "Why does the Shunting-Yard algorithm pop and evaluate existing operators when encountering a new operator of LOWER or EQUAL precedence?",
                "options": [
                    {
                        "id": "A",
                        "label": "Higher or equal precedence operators already waiting on the stack must be evaluated immediately because their binding to preceding numbers is now complete"
                    },
                    {
                        "id": "B",
                        "label": "Because stacks can only hold 2 operators"
                    },
                    {
                        "id": "C",
                        "label": "To prevent numbers from overflowing"
                    },
                    {
                        "id": "D",
                        "label": "Because parenthesis matching requires empty operator stacks"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! E.g. in `2 * 3 + 4`, when encountering `+` (precedence 1), the waiting `*` (precedence 2) has higher precedence and must be evaluated (`2 * 3 = 6`) before `+` can be stored.",
                    "B": "Incorrect: Operator stacks can grow to arbitrary depth.",
                    "C": "Incorrect: Precedence enforcement is syntactic.",
                    "D": "Incorrect: Parentheses create isolated precedence scopes."
                }
            },
            {
                "id": "chk-d94-q2",
                "question": "What is the time complexity of evaluating an arithmetic expression string of length N using the Shunting-Yard algorithm?",
                "options": [
                    {
                        "id": "A",
                        "label": "O(N) linear time, because each character, number, and operator is pushed and popped at most once"
                    },
                    {
                        "id": "B",
                        "label": "O(N^2) quadratic time"
                    },
                    {
                        "id": "C",
                        "label": "O(2^N) exponential time"
                    },
                    {
                        "id": "D",
                        "label": "O(N log N) time"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Every token is pushed onto the operand or operator stack once and popped at most once. Total operations are proportional to N.",
                    "B": "Incorrect: Stack passes do not re-scan the string.",
                    "C": "Incorrect: Shunting-Yard is strictly polynomial linear.",
                    "D": "Incorrect: No sorting or divide-and-conquer is involved."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day94-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Expression Parsing",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Evaluate a mathematical expression containing +, -, *, and parentheses.",
        "subheading": "Implement and verify Expression Parsing in the interactive workspace.",
        "task": {
            "title": "Evaluate a mathematical expression containing +, -, *, and parentheses.",
            "instructions": [
                "Evaluate a mathematical expression containing +, -, *, and parentheses.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "def eval_expression(s: str) -> int:\n    # TODO: Implement Shunting-Yard / 2-stack expression evaluator\n    return 0\n\nprint('3 + 2 * 2 =', eval_expression('3 + 2 * 2'))       # 7\nprint('(1 + (4 + 5 + 2) - 3) =', eval_expression('(1 + (4 + 5 + 2) - 3)')) # 9\n",
            "solutionCode": "def eval_expression(s: str) -> int:\n    vals, ops = [], []\n    prec = {'+': 1, '-': 1, '*': 2, '/': 2}\n    def apply():\n        op = ops.pop()\n        b = vals.pop()\n        a = vals.pop()\n        if op == '+':\n            vals.append(a + b)\n        elif op == '-':\n            vals.append(a - b)\n        elif op == '*':\n            vals.append(a * b)\n        elif op == '/':\n            vals.append(int(a / b))\n    i = 0\n    while i < len(s):\n        if s[i] == ' ':\n            i += 1\n            continue\n        if s[i].isdigit():\n            n = 0\n            while i < len(s) and s[i].isdigit():\n                n = n * 10 + int(s[i])\n                i += 1\n            vals.append(n)\n            continue\n        elif s[i] == '(':\n            ops.append('(')\n        elif s[i] == ')':\n            while ops and ops[-1] != '(':\n                apply()\n            if ops and ops[-1] == '(':\n                ops.pop()\n        elif s[i] in prec:\n            while ops and ops[-1] in prec and prec[ops[-1]] >= prec[s[i]]:\n                apply()\n            ops.append(s[i])\n        i += 1\n    while ops:\n        apply()\n    return vals[0] if vals else 0\n\nprint('3 + 2 * 2 =', eval_expression('3 + 2 * 2'))\nprint('(1 + (4 + 5 + 2) - 3) =', eval_expression('(1 + (4 + 5 + 2) - 3)'))\n",
            "expectedOutputPatterns": [
                "3 + 2 * 2 = 7",
                "(1 + (4 + 5 + 2) - 3) = 9"
            ],
            "hint": "Track vals and ops stacks. If digit parse full integer. If '(' push to ops. If ')' pop and apply until '('. If operator, while top op has >= precedence apply, then push operator."
        },
        "keyTakeaway": "Successfully implemented and verified Expression Parsing!"
    },
    {
        "id": "day94-step5",
        "stepNumber": 5,
        "title": "Day 94 Complete: Expression Parsing & Shunting-Yard Algorithm",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 94,
        "heading": "Mastery Achieved: Expression Parsing & Shunting-Yard Algorithm",
        "subheading": "You have solidified key mental models and techniques for Expression Parsing.",
        "recapRows": [
            {
                "concept": "Operator Precedence Invariant",
                "naiveIntuition": "Evaluate expressions strictly left-to-right",
                "pythonReality": "Stack-based precedence deferral guarantees that multiplication and division resolve before addition and subtraction"
            },
            {
                "concept": "Syntactic Stack Scoping",
                "naiveIntuition": "Parentheses require recursive parsing",
                "pythonReality": "Pushing '(' onto the operator stack scopes precedence evaluation without needing recursion"
            }
        ],
        "solidifiedConcepts": [
            "Operator Precedence & Associativity",
            "Dijkstra's Shunting-Yard (Infix to Postfix)"
        ],
        "nextDayPreview": {
            "dayNumber": 95,
            "title": "Section 8 Review & Linear State Machines",
            "description": "Synthesize stacks, queues, deques, and monotonic patterns into a complete expression and state evaluation engine."
        }
    }
]
},
  95: {
  "dayNumber": 95,
  "title": "Section 8 Review & Linear State Machines",
  "topicName": "Stacks & Queues Milestone",
  "sectionId": "stacks-and-queues",
  "estimatedMinutes": 40,
  "difficulty": "INTERMEDIATE",
  "prerequisites": [
    87,
    88,
    91,
    92,
    93,
    94
  ],
  "concepts": [
    "Linear Data Structure Selection",
    "State Machine Buffer Coordination",
    "Amortized Bounds"
  ],
  "practiceSkills": [
    "Stacks & Queues Milestone Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Architect a calculator engine evaluating nested expressions with unary operators",
    "Select optimal stack and queue structures matching problem invariants"
  ],
  "practiceArchetype": "milestone",
  "flowTier": "tier2"
,
  "steps": [
    {
        "id": "day95-step1",
        "stepNumber": 1,
        "title": "Section 8 Review & Linear State Machines: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Stacks & Queues Milestone",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Stacks & Queues Milestone.",
        "markdownContent": [
            "Section 8 Review synthesizes LIFO stacks, FIFO queues, circular ring buffers, min stacks, monotonic stacks, and sliding window deques into an algorithmic decision framework.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Stacks & Queues Milestone**, remember the central principle: Selecting the correct linear discipline reduces complex quadratic search spaces into amortized O(N) linear scans."
        ],
        "snippets": [
            {
                "title": "Stacks & Queues Milestone Implementation Template",
                "code": "# Linear Discipline Selection Matrix:\n# LIFO -> Stack (Backtracking, Syntax, Call Stack)\n# FIFO -> Queue (BFS, Buffers, Scheduling)\n# Extremum -> Monotonic Stack / Monotonic Deque",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Selecting the correct linear discipline reduces complex quadratic search spaces into amortized O(N) linear scans."
    },
    {
        "id": "day95-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Stacks & Queues Milestone",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Framework: (1) Does order require matching nested pairs or undo history? Use Stack. (2) Does order require temporal arrival or breadth-first exploration? Use Queue. (3) Does the problem ask for next greater/smaller element? Use Monotonic Stack. (4) Does the problem ask for sliding window extremum? Use Monotonic Deque.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Selecting the correct linear discipline reduces complex quadratic search spaces into amortized O(N) linear scans.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Stacks & Queues Milestone Core Invariant",
                "content": "Selecting the correct linear discipline reduces complex quadratic search spaces into amortized O(N) linear scans."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Selecting the correct linear discipline reduces complex quadratic search spaces into amortized O(N) linear scans."
    },
    {
        "id": "day95-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Stacks & Queues Milestone",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d95-q1",
                "question": "Which data structure is optimal for finding the daily temperature span (number of days until a warmer day)?",
                "options": [
                    {
                        "id": "A",
                        "label": "Monotonic Decreasing Stack storing day indices in O(N) time"
                    },
                    {
                        "id": "B",
                        "label": "Circular Queue in O(N^2) time"
                    },
                    {
                        "id": "C",
                        "label": "Binary Search Tree in O(N log N) time"
                    },
                    {
                        "id": "D",
                        "label": "Nested for loops in O(N^2) time"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Daily temperatures is an exact Next Greater Element archetype. Maintaining a monotonic decreasing stack of indices resolves each day's span in amortized O(N) time.",
                    "B": "Incorrect: Circular queue does not maintain sorted temperature ordering.",
                    "C": "Incorrect: BST has higher overhead and tree balancing complexity.",
                    "D": "Incorrect: Quadratic loop times out on large inputs."
                }
            },
            {
                "id": "chk-d95-q2",
                "question": "When building an operating system process scheduler where tasks must be serviced strictly in arrival order, which discipline is required?",
                "options": [
                    {
                        "id": "A",
                        "label": "FIFO Queue discipline"
                    },
                    {
                        "id": "B",
                        "label": "LIFO Stack discipline"
                    },
                    {
                        "id": "C",
                        "label": "Monotonic Stack discipline"
                    },
                    {
                        "id": "D",
                        "label": "Random Access Array"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! First-In, First-Out guarantees starvation-free fairness by executing tasks in the exact order they were enqueued.",
                    "B": "Incorrect: LIFO starves older processes indefinitely.",
                    "C": "Incorrect: Monotonic stacks do not maintain FIFO arrival ordering.",
                    "D": "Incorrect: Raw arrays require O(N) removal from front."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day95-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Stacks & Queues Milestone",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Solve Daily Temperatures: return an array where answer[i] is days until warmer temperature.",
        "subheading": "Implement and verify Stacks & Queues Milestone in the interactive workspace.",
        "task": {
            "title": "Solve Daily Temperatures: return an array where answer[i] is days until warmer temperature.",
            "instructions": [
                "Solve Daily Temperatures: return an array where answer[i] is days until warmer temperature.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "def daily_temperatures(temps: list[int]) -> list[int]:\n    # TODO: Use a monotonic stack of indices\n    # Compute days until warmer temperature for each day\n    return []\n\nprint('Daily temps:', daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]))\n",
            "solutionCode": "def daily_temperatures(temps: list[int]) -> list[int]:\n    res = [0] * len(temps)\n    stack = []\n    for i, t in enumerate(temps):\n        while stack and temps[stack[-1]] < t:\n            prev_idx = stack.pop()\n            res[prev_idx] = i - prev_idx\n        stack.append(i)\n    return res\n\nprint('Daily temps:', daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]))\n",
            "expectedOutputPatterns": [
                "Daily temps: [1, 1, 4, 2, 1, 1, 0, 0]"
            ],
            "hint": "Initialize res = [0] * len(temps), stack = []. Loop i, t: while stack and temps[stack[-1]] < t: prev = stack.pop(); res[prev] = i - prev. stack.append(i). Return res."
        },
        "keyTakeaway": "Successfully implemented and verified Stacks & Queues Milestone!"
    },
    {
        "id": "day95-step5",
        "stepNumber": 5,
        "title": "Day 95 Complete: Section 8 Review & Linear State Machines",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 95,
        "heading": "Mastery Achieved: Section 8 Review & Linear State Machines",
        "subheading": "You have solidified key mental models and techniques for Stacks & Queues Milestone.",
        "recapRows": [
            {
                "concept": "Index Difference Span",
                "naiveIntuition": "Store temperatures directly in the stack",
                "pythonReality": "Storing day indices allows computing both the value comparison and the time distance i - prev in O(1)"
            },
            {
                "concept": "Section 8 Synthesis",
                "naiveIntuition": "Linear data structures only store raw data",
                "pythonReality": "Stack and queue disciplines impose invariant orders that enable amortized O(N) algorithms for complex span and area problems"
            }
        ],
        "solidifiedConcepts": [
            "Linear Data Structure Selection",
            "State Machine Buffer Coordination",
            "Amortized Bounds"
        ],
        "nextDayPreview": {
            "dayNumber": 96,
            "title": "Tree Terminology & Hierarchical Anatomy",
            "description": "Understand tree terminology: root, leaves, depth, height, ancestor/descendant relationships, and TreeNode classes."
        }
    }
]
},
  96: {
  "dayNumber": 96,
  "title": "Tree Terminology & Hierarchical Anatomy",
  "topicName": "Tree Foundations",
  "sectionId": "trees-and-bst",
  "estimatedMinutes": 30,
  "difficulty": "INTERMEDIATE",
  "prerequisites": [
    76
  ],
  "concepts": [
    "Hierarchical Node Anatomy",
    "Height, Depth & Edge Counts"
  ],
  "practiceSkills": [
    "Tree Foundations Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Define a binary tree TreeNode class and recursive child pointer structures",
    "Calculate tree height, node depths, and verify leaf node conditions"
  ],
  "practiceArchetype": "guided",
  "flowTier": "tier1"
,
  "steps": [
    {
        "id": "day96-step1",
        "stepNumber": 1,
        "title": "Tree Terminology & Hierarchical Anatomy: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Tree Foundations",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Tree Foundations.",
        "markdownContent": [
            "Binary Trees organize hierarchical data where each TreeNode contains a value and references to at most two children (left and right).",
            "### Foundational Mental Model\nWhen approaching problems requiring **Tree Foundations**, remember the central principle: Tree algorithms mirror the recursive anatomy of tree nodes."
        ],
        "snippets": [
            {
                "title": "Tree Foundations Implementation Template",
                "code": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\nroot = TreeNode(1, TreeNode(2), TreeNode(3))\nprint('Root:', root.val, 'Left:', root.left.val, 'Right:', root.right.val)",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Tree algorithms mirror the recursive anatomy of tree nodes."
    },
    {
        "id": "day96-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Tree Foundations",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Recursive definition: a tree is either empty (None) or a root node pointing to two disjoint binary trees (left and right subtrees). Node height is max edges to a leaf; node depth is edges from root. Maximum nodes at level L is 2^L.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Tree algorithms mirror the recursive anatomy of tree nodes.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Tree Foundations Core Invariant",
                "content": "Tree algorithms mirror the recursive anatomy of tree nodes."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Tree algorithms mirror the recursive anatomy of tree nodes."
    },
    {
        "id": "day96-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Tree Foundations",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d96-q1",
                "question": "What is the maximum number of nodes in a binary tree of height H (where a single root node has height 0)?",
                "options": [
                    {
                        "id": "A",
                        "label": "2^(H + 1) - 1"
                    },
                    {
                        "id": "B",
                        "label": "2^H"
                    },
                    {
                        "id": "C",
                        "label": "H^2"
                    },
                    {
                        "id": "D",
                        "label": "2 * H"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Summing nodes at each level: 2^0 + 2^1 + ... + 2^H = 2^(H+1) - 1. For H=0, total is 2^1 - 1 = 1; for H=2, total is 2^3 - 1 = 7.",
                    "B": "Incorrect: 2^H is the maximum nodes on level H alone, not the total tree nodes.",
                    "C": "Incorrect: Tree growth is exponential, not polynomial.",
                    "D": "Incorrect: Tree growth is exponential, not linear."
                }
            },
            {
                "id": "chk-d96-q2",
                "question": "What distinguishes a leaf node from an internal node in a binary tree?",
                "options": [
                    {
                        "id": "A",
                        "label": "A leaf node has both left and right pointers equal to None"
                    },
                    {
                        "id": "B",
                        "label": "A leaf node has value 0"
                    },
                    {
                        "id": "C",
                        "label": "A leaf node is the root of the tree"
                    },
                    {
                        "id": "D",
                        "label": "A leaf node has only a left child"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! By definition, terminal leaf nodes have no children: `node.left is None and node.right is None`.",
                    "B": "Incorrect: Leaf nodes can store any value.",
                    "C": "Incorrect: The root has no parent, but can have children.",
                    "D": "Incorrect: A node with a child is an internal node."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day96-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Tree Foundations",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Count the total number of leaf nodes in a binary tree.",
        "subheading": "Implement and verify Tree Foundations in the interactive workspace.",
        "task": {
            "title": "Count the total number of leaf nodes in a binary tree.",
            "instructions": [
                "Count the total number of leaf nodes in a binary tree.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef count_leaves(root: TreeNode) -> int:\n    # TODO: Recursively count leaf nodes\n    return 0\n\n# Tree: 1 -> left: 2, right: 3 -> left: 4, right: 5\nt = TreeNode(1, TreeNode(2), TreeNode(3, TreeNode(4), TreeNode(5)))\nprint('Leaf count:', count_leaves(t))\n",
            "solutionCode": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef count_leaves(root: TreeNode) -> int:\n    if not root:\n        return 0\n    if not root.left and not root.right:\n        return 1\n    return count_leaves(root.left) + count_leaves(root.right)\n\nt = TreeNode(1, TreeNode(2), TreeNode(3, TreeNode(4), TreeNode(5)))\nprint('Leaf count:', count_leaves(t))\n",
            "expectedOutputPatterns": [
                "Leaf count: 3"
            ],
            "hint": "Base cases: if not root return 0; if not root.left and not root.right return 1. Recurse: count_leaves(root.left) + count_leaves(root.right)."
        },
        "keyTakeaway": "Successfully implemented and verified Tree Foundations!"
    },
    {
        "id": "day96-step5",
        "stepNumber": 5,
        "title": "Day 96 Complete: Tree Terminology & Hierarchical Anatomy",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 96,
        "heading": "Mastery Achieved: Tree Terminology & Hierarchical Anatomy",
        "subheading": "You have solidified key mental models and techniques for Tree Foundations.",
        "recapRows": [
            {
                "concept": "Recursive Self-Similarity",
                "naiveIntuition": "Iterate through tree with index loops",
                "pythonReality": "Each child node is itself the root of an independent subtree, making recursive decomposition the natural paradigm"
            },
            {
                "concept": "Branching Complexity",
                "naiveIntuition": "Binary trees are always fast",
                "pythonReality": "Degenerate trees (skewed chains) degrade to O(N) linear lists; balanced trees guarantee O(log N) depth"
            }
        ],
        "solidifiedConcepts": [
            "Hierarchical Node Anatomy",
            "Height, Depth & Edge Counts"
        ],
        "nextDayPreview": {
            "dayNumber": 97,
            "title": "Recursive Traversals: Pre, In, Post-Order",
            "description": "Implement recursive pre-order (NLR), in-order (LNR), and post-order (LRN) binary tree traversals in O(N) time."
        }
    }
]
},
  97: {
  "dayNumber": 97,
  "title": "Recursive Traversals: Pre, In, Post-Order",
  "topicName": "Recursive Traversals",
  "sectionId": "trees-and-bst",
  "estimatedMinutes": 35,
  "difficulty": "INTERMEDIATE",
  "prerequisites": [
    30,
    96
  ],
  "concepts": [
    "NLR, LNR, LRN Visiting Orders",
    "Call Stack Tree Traversal"
  ],
  "practiceSkills": [
    "Recursive Traversals Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Trace Pre-order, In-order, and Post-order recursive visits across binary trees",
    "Predict visiting sequence output for tree construction and destruction"
  ],
  "practiceArchetype": "tracing",
  "flowTier": "tier2"
,
  "steps": [
    {
        "id": "day97-step1",
        "stepNumber": 1,
        "title": "Recursive Traversals: Pre, In, Post-Order: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Recursive Traversals",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Recursive Traversals.",
        "markdownContent": [
            "Tree Traversals (Pre-order, In-order, Post-order) systematically visit all N nodes using Depth-First Search (DFS), each defined by when the root is processed relative to its subtrees.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Recursive Traversals**, remember the central principle: In-order traversal visits BST keys in strictly sorted order; post-order processes subtrees before parents."
        ],
        "snippets": [
            {
                "title": "Recursive Traversals Implementation Template",
                "code": "# Tree Traversals\ndef in_order(node, res):\n    if not node: return\n    in_order(node.left, res)\n    res.append(node.val)\n    in_order(node.right, res)",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "In-order traversal visits BST keys in strictly sorted order; post-order processes subtrees before parents."
    },
    {
        "id": "day97-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Recursive Traversals",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Pre-order (Root, Left, Right): used for tree cloning and serialization. In-order (Left, Root, Right): yields monotonically sorted values in Binary Search Trees. Post-order (Left, Right, Root): used for bottom-up cleanup, deletions, and subtree metric calculations.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: In-order traversal visits BST keys in strictly sorted order; post-order processes subtrees before parents.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Recursive Traversals Core Invariant",
                "content": "In-order traversal visits BST keys in strictly sorted order; post-order processes subtrees before parents."
            }
        ],
        "keyTakeaway": "Operational invariant locked: In-order traversal visits BST keys in strictly sorted order; post-order processes subtrees before parents."
    },
    {
        "id": "day97-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Recursive Traversals",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d97-q1",
                "question": "Which traversal order processes a node's left and right subtrees BEFORE processing the node itself?",
                "options": [
                    {
                        "id": "A",
                        "label": "Post-order traversal (Left, Right, Root)"
                    },
                    {
                        "id": "B",
                        "label": "Pre-order traversal (Root, Left, Right)"
                    },
                    {
                        "id": "C",
                        "label": "In-order traversal (Left, Root, Right)"
                    },
                    {
                        "id": "D",
                        "label": "Level-order traversal"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Post-order evaluates both children before aggregating results at the parent, making it ideal for calculating subtree heights, directory disk usage, and bottom-up DP.",
                    "B": "Incorrect: Pre-order visits root first.",
                    "C": "Incorrect: In-order visits root between left and right.",
                    "D": "Incorrect: Level-order visits nodes by depth."
                }
            },
            {
                "id": "chk-d97-q2",
                "question": "What sequence is produced by an in-order traversal of a valid Binary Search Tree (BST)?",
                "options": [
                    {
                        "id": "A",
                        "label": "Strictly ascending sorted order"
                    },
                    {
                        "id": "B",
                        "label": "Strictly descending sorted order"
                    },
                    {
                        "id": "C",
                        "label": "Random order"
                    },
                    {
                        "id": "D",
                        "label": "Reverse level order"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Because BST invariant enforces `left < root < right`, in-order traversal (Left, Root, Right) guarantees elements are visited in strictly ascending sorted order.",
                    "B": "Incorrect: Ascending, not descending.",
                    "C": "Incorrect: The order is strictly deterministic.",
                    "D": "Incorrect: Depth is not flattened into reverse level order."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day97-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Recursive Traversals",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Implement In-order traversal and collect values in an array.",
        "subheading": "Implement and verify Recursive Traversals in the interactive workspace.",
        "task": {
            "title": "Implement In-order traversal and collect values in an array.",
            "instructions": [
                "Implement In-order traversal and collect values in an array.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef inorder_traversal(root: TreeNode) -> list[int]:\n    # TODO: Collect node values in Left -> Root -> Right order\n    return []\n\n# BST: 2 -> left: 1, right: 3\nbst = TreeNode(2, TreeNode(1), TreeNode(3))\nprint('In-order:', inorder_traversal(bst))\n",
            "solutionCode": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef inorder_traversal(root: TreeNode) -> list[int]:\n    res = []\n    def dfs(node):\n        if not node:\n            return\n        dfs(node.left)\n        res.append(node.val)\n        dfs(node.right)\n    dfs(root)\n    return res\n\nbst = TreeNode(2, TreeNode(1), TreeNode(3))\nprint('In-order:', inorder_traversal(bst))\n",
            "expectedOutputPatterns": [
                "In-order: [1, 2, 3]"
            ],
            "hint": "Helper dfs(node): if not node return; dfs(node.left); res.append(node.val); dfs(node.right). Call dfs(root) and return res."
        },
        "keyTakeaway": "Successfully implemented and verified Recursive Traversals!"
    },
    {
        "id": "day97-step5",
        "stepNumber": 5,
        "title": "Day 97 Complete: Recursive Traversals: Pre, In, Post-Order",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 97,
        "heading": "Mastery Achieved: Recursive Traversals: Pre, In, Post-Order",
        "subheading": "You have solidified key mental models and techniques for Recursive Traversals.",
        "recapRows": [
            {
                "concept": "Traversal Positioning",
                "naiveIntuition": "Traversals visit nodes in different orders on the tree",
                "pythonReality": "The call stack traverses identical paths; only the moment of processing node.val changes relative to recursive calls"
            },
            {
                "concept": "BST Monotonicity",
                "naiveIntuition": "Sort BST nodes after extraction",
                "pythonReality": "In-order traversal extracts sorted data in O(N) time with zero comparison sorting required"
            }
        ],
        "solidifiedConcepts": [
            "NLR, LNR, LRN Visiting Orders",
            "Call Stack Tree Traversal"
        ],
        "nextDayPreview": {
            "dayNumber": 98,
            "title": "Iterative Tree Traversals via Explicit Stack",
            "description": "Implement pre-order, in-order, and post-order tree traversals iteratively using an explicit stack in O(N) time."
        }
    }
]
},
  98: {
  "dayNumber": 98,
  "title": "Iterative Tree Traversals via Explicit Stack",
  "topicName": "Iterative Traversals",
  "sectionId": "trees-and-bst",
  "estimatedMinutes": 40,
  "difficulty": "INTERMEDIATE",
  "prerequisites": [
    86,
    97
  ],
  "concepts": [
    "Explicit Stack Simulation",
    "Left-Spine Descent Invariant"
  ],
  "practiceSkills": [
    "Iterative Traversals Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Implement iterative in-order and pre-order tree traversals using an explicit stack",
    "Eliminate recursion overhead and prevent stack overflow on deep unbalanced trees"
  ],
  "practiceArchetype": "algorithm",
  "flowTier": "tier2"
,
  "steps": [
    {
        "id": "day98-step1",
        "stepNumber": 1,
        "title": "Iterative Tree Traversals via Explicit Stack: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Iterative Traversals",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Iterative Traversals.",
        "markdownContent": [
            "Iterative Tree Traversals simulate the system recursion call stack using an explicit Python list to prevent RecursionError on skewed trees of depth up to N.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Iterative Traversals**, remember the central principle: Simulating the call stack with a while loop and explicit list eliminates Python's recursion limit while matching DFS performance."
        ],
        "snippets": [
            {
                "title": "Iterative Traversals Implementation Template",
                "code": "# Iterative In-Order Traversal via Explicit Stack\ndef inorder_iterative(root):\n    res, stack = [], []\n    curr = root\n    while curr or stack:\n        while curr:\n            stack.append(curr)\n            curr = curr.left\n        curr = stack.pop()\n        res.append(curr.val)\n        curr = curr.right\n    return res",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Simulating the call stack with a while loop and explicit list eliminates Python's recursion limit while matching DFS performance."
    },
    {
        "id": "day98-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Iterative Traversals",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Iterative In-Order: push nodes onto stack while descending down the left spine (`curr = curr.left`). When curr is None, pop from stack, process node value, and move to right child (`curr = node.right`). The stack holds at most H nodes at any moment, guaranteeing O(N) time and O(H) space.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Simulating the call stack with a while loop and explicit list eliminates Python's recursion limit while matching DFS performance.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Iterative Traversals Core Invariant",
                "content": "Simulating the call stack with a while loop and explicit list eliminates Python's recursion limit while matching DFS performance."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Simulating the call stack with a while loop and explicit list eliminates Python's recursion limit while matching DFS performance."
    },
    {
        "id": "day98-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Iterative Traversals",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d98-q1",
                "question": "Why is an explicit stack loop preferred over recursion when processing unbalanced, deep trees in production Python environments?",
                "options": [
                    {
                        "id": "A",
                        "label": "Python enforces a default call stack limit (1000 frames); recursion on a skewed tree of depth 10,000 raises RecursionError, whereas an explicit heap-allocated list can hold millions of elements"
                    },
                    {
                        "id": "B",
                        "label": "Because iterative loops run in O(1) time"
                    },
                    {
                        "id": "C",
                        "label": "Because explicit stacks sort the tree nodes"
                    },
                    {
                        "id": "D",
                        "label": "Because recursion does not work on binary trees"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Python's interpreter terminates with RecursionError when stack depth exceeds sys.getrecursionlimit() (typically 1000). Allocating an explicit stack on the heap handles arbitrarily deep degenerate trees safely.",
                    "B": "Incorrect: Visiting N nodes strictly requires O(N) operations.",
                    "C": "Incorrect: In-order traversal yields sorted order on BSTs specifically, not arbitrary binary trees.",
                    "D": "Incorrect: Recursion is the natural representation of tree anatomy."
                }
            },
            {
                "id": "chk-d98-q2",
                "question": "In the iterative in-order template, when `curr` becomes `None`, what is the invariant governing the next step?",
                "options": [
                    {
                        "id": "A",
                        "label": "The node at the top of the stack is the leftmost unvisited ancestor whose left subtree is completely exhausted; popping it visits that node before moving to its right child"
                    },
                    {
                        "id": "B",
                        "label": "The tree traversal is finished and the loop must break"
                    },
                    {
                        "id": "C",
                        "label": "curr must be reset to root"
                    },
                    {
                        "id": "D",
                        "label": "stack must be cleared"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! When `curr` is None, we have reached the bottom of the current left branch. The top of the stack is the immediate parent, ready to be processed before exploring its right branch.",
                    "B": "Incorrect: Traversal completes only when BOTH curr is None AND stack is empty.",
                    "C": "Incorrect: Resetting to root causes infinite loops.",
                    "D": "Incorrect: Clearing the stack loses remaining parent nodes."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day98-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Iterative Traversals",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Implement iterative in-order tree traversal using an explicit stack.",
        "subheading": "Implement and verify Iterative Traversals in the interactive workspace.",
        "task": {
            "title": "Implement iterative in-order tree traversal using an explicit stack.",
            "instructions": [
                "Implement iterative in-order tree traversal using an explicit stack.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef inorder_traversal(root: TreeNode) -> list[int]:\n    # TODO: Implement iterative in-order using explicit stack\n    return []\n\n# Tree: 1 -> right: 2 (left: 3) -> In-order: [1, 3, 2]\nt = TreeNode(1, None, TreeNode(2, TreeNode(3), None))\nprint('In-order:', inorder_traversal(t))\n",
            "solutionCode": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef inorder_traversal(root: TreeNode) -> list[int]:\n    res, stack = [], []\n    curr = root\n    while curr or stack:\n        while curr:\n            stack.append(curr)\n            curr = curr.left\n        curr = stack.pop()\n        res.append(curr.val)\n        curr = curr.right\n    return res\n\nt = TreeNode(1, None, TreeNode(2, TreeNode(3), None))\nprint('In-order:', inorder_traversal(t))\n",
            "expectedOutputPatterns": [
                "In-order: [1, 3, 2]"
            ],
            "hint": "Loop while curr or stack: while curr: stack.append(curr); curr = curr.left. curr = stack.pop(); res.append(curr.val); curr = curr.right."
        },
        "keyTakeaway": "Successfully implemented and verified Iterative Traversals!"
    },
    {
        "id": "day98-step5",
        "stepNumber": 5,
        "title": "Day 98 Complete: Iterative Tree Traversals via Explicit Stack",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 98,
        "heading": "Mastery Achieved: Iterative Tree Traversals via Explicit Stack",
        "subheading": "You have solidified key mental models and techniques for Iterative Traversals.",
        "recapRows": [
            {
                "concept": "Left-Spine Descent",
                "naiveIntuition": "Pop and push simultaneously",
                "pythonReality": "Pushing all left children before processing matches recursive call-stack activation records"
            },
            {
                "concept": "Heap-Allocated Safety",
                "naiveIntuition": "Recursion is always better in Python",
                "pythonReality": "Deep recursion risks call stack exhaustion; explicit loops on heap memory provide enterprise resilience"
            }
        ],
        "solidifiedConcepts": [
            "Explicit Stack Simulation",
            "Left-Spine Descent Invariant"
        ],
        "nextDayPreview": {
            "dayNumber": 99,
            "title": "BFS & Level-Order Queue Traversal",
            "description": "Implement breadth-first search (BFS) level-order traversal on trees using queues, handling level batching."
        }
    }
]
},
  99: {
  "dayNumber": 99,
  "title": "BFS & Level-Order Queue Traversal",
  "topicName": "Level-Order BFS",
  "sectionId": "trees-and-bst",
  "estimatedMinutes": 35,
  "difficulty": "INTERMEDIATE",
  "prerequisites": [
    89,
    97
  ],
  "concepts": [
    "FIFO Queue Level Batching",
    "Zigzag & Level Width Tracking"
  ],
  "practiceSkills": [
    "Level-Order BFS Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Traverse binary trees level-by-level using a FIFO queue recording row arrays",
    "Compute level averages, tree widths, and zigzag level-order paths in O(N) time"
  ],
  "practiceArchetype": "algorithm",
  "flowTier": "tier2"
,
  "steps": [
    {
        "id": "day99-step1",
        "stepNumber": 1,
        "title": "BFS & Level-Order Queue Traversal: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Level-Order BFS",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Level-Order BFS.",
        "markdownContent": [
            "Breadth-First Search (Level-Order Traversal) explores trees level by level horizontally using a FIFO queue (`collections.deque`), batching nodes by depth.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Level-Order BFS**, remember the central principle: Freezing level_size at each outer iteration cleanly separates tree levels in O(N) time."
        ],
        "snippets": [
            {
                "title": "Level-Order BFS Implementation Template",
                "code": "from collections import deque\ndef level_order(root):\n    if not root: return []\n    q = deque([root])\n    levels = []\n    while q:\n        level = []\n        for _ in range(len(q)):\n            node = q.popleft()\n            level.append(node.val)\n            if node.left: q.append(node.left)\n            if node.right: q.append(node.right)\n        levels.append(level)\n    return levels",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Freezing level_size at each outer iteration cleanly separates tree levels in O(N) time."
    },
    {
        "id": "day99-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Level-Order BFS",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Initialize `queue = deque([root])`. While queue is non-empty: capture `level_size = len(queue)`. Pop exactly `level_size` nodes for current level, append their values to current level array, and enqueue their non-null children. Advance to next level.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Freezing level_size at each outer iteration cleanly separates tree levels in O(N) time.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Level-Order BFS Core Invariant",
                "content": "Freezing level_size at each outer iteration cleanly separates tree levels in O(N) time."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Freezing level_size at each outer iteration cleanly separates tree levels in O(N) time."
    },
    {
        "id": "day99-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Level-Order BFS",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d99-q1",
                "question": "Why is `for _ in range(len(q)):` used inside the `while q:` loop in level-order traversal?",
                "options": [
                    {
                        "id": "A",
                        "label": "It snapshots the exact count of nodes belonging to the current depth level before any children of the next level are enqueued"
                    },
                    {
                        "id": "B",
                        "label": "To prevent an infinite loop"
                    },
                    {
                        "id": "C",
                        "label": "Because range() is required by Python deques"
                    },
                    {
                        "id": "D",
                        "label": "To sort the nodes in each level"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Evaluating `len(q)` at the start of the loop captures exactly the nodes on the current level. Enqueuing children during the loop grows `q`, but the loop runs only for the pre-calculated count.",
                    "B": "Incorrect: The while loop condition prevents infinite looping.",
                    "C": "Incorrect: Range is standard Python iteration.",
                    "D": "Incorrect: Level nodes maintain left-to-right discovery order, not sorted."
                }
            },
            {
                "id": "chk-d99-q2",
                "question": "What is the maximum space complexity of level-order traversal in a complete binary tree of N nodes?",
                "options": [
                    {
                        "id": "A",
                        "label": "O(N) space, because the bottom leaf level contains approximately N / 2 nodes"
                    },
                    {
                        "id": "B",
                        "label": "O(1) space"
                    },
                    {
                        "id": "C",
                        "label": "O(log N) space"
                    },
                    {
                        "id": "D",
                        "label": "O(N^2) space"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! In a full binary tree, the last level contains ceil(N / 2) nodes. The queue holds all leaf nodes simultaneously, consuming O(N) auxiliary space.",
                    "B": "Incorrect: The queue stores entire levels in memory.",
                    "C": "Incorrect: O(log N) is the space complexity for DFS call stack, not BFS queue.",
                    "D": "Incorrect: Total nodes across all levels is N."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day99-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Level-Order BFS",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Return the level-order traversal of a binary tree as a list of lists of integers.",
        "subheading": "Implement and verify Level-Order BFS in the interactive workspace.",
        "task": {
            "title": "Return the level-order traversal of a binary tree as a list of lists of integers.",
            "instructions": [
                "Return the level-order traversal of a binary tree as a list of lists of integers.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "from collections import deque\n\nclass TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef get_levels(root: TreeNode) -> list[list[int]]:\n    # TODO: Implement BFS level-order traversal\n    return []\n\n# Tree: 3 -> left: 9, right: 20 (left: 15, right: 7)\nt = TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))\nprint('Levels:', get_levels(t))\n",
            "solutionCode": "from collections import deque\n\nclass TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef get_levels(root: TreeNode) -> list[list[int]]:\n    if not root:\n        return []\n    q = deque([root])\n    res = []\n    while q:\n        level = []\n        for _ in range(len(q)):\n            node = q.popleft()\n            level.append(node.val)\n            if node.left:\n                q.append(node.left)\n            if node.right:\n                q.append(node.right)\n        res.append(level)\n    return res\n\nt = TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))\nprint('Levels:', get_levels(t))\n",
            "expectedOutputPatterns": [
                "Levels: [[3], [9, 20], [15, 7]]"
            ],
            "hint": "Check if not root return []. q = deque([root]). While q: level = [], loop range(len(q)): popleft, append val, push left/right children if non-null. Append level to res."
        },
        "keyTakeaway": "Successfully implemented and verified Level-Order BFS!"
    },
    {
        "id": "day99-step5",
        "stepNumber": 5,
        "title": "Day 99 Complete: BFS & Level-Order Queue Traversal",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 99,
        "heading": "Mastery Achieved: BFS & Level-Order Queue Traversal",
        "subheading": "You have solidified key mental models and techniques for Level-Order BFS.",
        "recapRows": [
            {
                "concept": "BFS Snapshot Pattern",
                "naiveIntuition": "Track depth with node tuples (node, depth)",
                "pythonReality": "Processing len(q) nodes in a nested loop groups levels naturally without storing depth metadata"
            },
            {
                "concept": "DFS vs BFS Space Asymmetry",
                "naiveIntuition": "BFS and DFS use the same memory",
                "pythonReality": "DFS memory scales with height O(H) (call stack); BFS memory scales with width O(W) (queue), which can be O(N) in wide trees"
            }
        ],
        "solidifiedConcepts": [
            "FIFO Queue Level Batching",
            "Zigzag & Level Width Tracking"
        ],
        "nextDayPreview": {
            "dayNumber": 100,
            "title": "Tree Properties: Height, Diameter & Symmetry",
            "description": "Compute tree height, diameter, balance factors, and test tree symmetry using bottom-up post-order DFS in O(N) time."
        }
    }
]
},
  100: {
  "dayNumber": 100,
  "title": "Tree Properties: Height, Diameter & Symmetry",
  "topicName": "Tree Properties",
  "sectionId": "trees-and-bst",
  "estimatedMinutes": 35,
  "difficulty": "INTERMEDIATE",
  "prerequisites": [
    97
  ],
  "concepts": [
    "Post-Order State Aggregation",
    "Global Diameter Calculation (Left + Right)"
  ],
  "practiceSkills": [
    "Tree Properties Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Calculate maximum tree diameter by computing left and right branch heights bottom-up",
    "Verify binary tree mirror symmetry using recursive dual-node checks"
  ],
  "practiceArchetype": "problem",
  "flowTier": "tier2"
,
  "steps": [
    {
        "id": "day100-step1",
        "stepNumber": 1,
        "title": "Tree Properties: Height, Diameter & Symmetry: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Tree Properties",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Tree Properties.",
        "markdownContent": [
            "Diameter of a Binary Tree is the length of the longest path between any two nodes, computed in O(N) time by returning subtree height while updating a global diameter.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Tree Properties**, remember the central principle: Return one value to the caller while updating a global optimal metric to avoid O(N^2) recalculations."
        ],
        "snippets": [
            {
                "title": "Tree Properties Implementation Template",
                "code": "# Diameter in O(N)\nclass Solution:\n    def diameter_of_binary_tree(self, root):\n        self.diameter = 0\n        def height(node):\n            if not node: return 0\n            lh = height(node.left)\n            rh = height(node.right)\n            self.diameter = max(self.diameter, lh + rh)\n            return 1 + max(lh, rh)\n        height(root)\n        return self.diameter",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Return one value to the caller while updating a global optimal metric to avoid O(N^2) recalculations."
    },
    {
        "id": "day100-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Tree Properties",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "The longest path passing through node `curr` is `height(curr.left) + height(curr.right)`. A naive algorithm calling `height()` for each node takes O(N^2). A post-order DFS updates `self.max_diameter = max(self.max_diameter, left_h + right_h)` and returns `1 + max(left_h, right_h)` in a single O(N) pass.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Return one value to the caller while updating a global optimal metric to avoid O(N^2) recalculations.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Tree Properties Core Invariant",
                "content": "Return one value to the caller while updating a global optimal metric to avoid O(N^2) recalculations."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Return one value to the caller while updating a global optimal metric to avoid O(N^2) recalculations."
    },
    {
        "id": "day100-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Tree Properties",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d100-q1",
                "question": "Does the longest path (diameter) of a binary tree always pass through the root node?",
                "options": [
                    {
                        "id": "A",
                        "label": "No, the longest path might reside entirely within a deep left or right subtree without passing through the root"
                    },
                    {
                        "id": "B",
                        "label": "Yes, diameter must always pass through the root"
                    },
                    {
                        "id": "C",
                        "label": "Only in balanced trees"
                    },
                    {
                        "id": "D",
                        "label": "Only if root has two children"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! If the left subtree is very deep and bushy while the right subtree is a single leaf, the two deepest leaves within the left subtree can form a diameter longer than any path through the root.",
                    "B": "Incorrect: Diameter is defined between ANY two nodes.",
                    "C": "Incorrect: Even in balanced trees it can bypass root if heights align.",
                    "D": "Incorrect: Root presence is not required."
                }
            },
            {
                "id": "chk-d100-q2",
                "question": "Why does combining height calculation with global diameter tracking run in O(N) time?",
                "options": [
                    {
                        "id": "A",
                        "label": "Every node is visited exactly once in post-order, computing both local height and diameter contribution in O(1) operations"
                    },
                    {
                        "id": "B",
                        "label": "Because the tree is converted into an array"
                    },
                    {
                        "id": "C",
                        "label": "Because it uses memoization on node values"
                    },
                    {
                        "id": "D",
                        "label": "Because diameter is always constant"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Post-order DFS visits each of the N nodes once, doing O(1) additions and comparisons per node. Total time is strictly O(N).",
                    "B": "Incorrect: No array conversion is performed.",
                    "C": "Incorrect: Pure recursion without memo table.",
                    "D": "Incorrect: Diameter depends dynamically on tree topology."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day100-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Tree Properties",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Calculate the diameter (number of edges on longest path) of a binary tree.",
        "subheading": "Implement and verify Tree Properties in the interactive workspace.",
        "task": {
            "title": "Calculate the diameter (number of edges on longest path) of a binary tree.",
            "instructions": [
                "Calculate the diameter (number of edges on longest path) of a binary tree.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef tree_diameter(root: TreeNode) -> int:\n    # TODO: Implement single-pass O(N) diameter calculation\n    return 0\n\n# 1 -> left: 2 (left: 4, right: 5), right: 3. Longest path: 4-2-1-3 or 5-2-1-3 (3 edges)\nt = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3))\nprint('Diameter:', tree_diameter(t))\n",
            "solutionCode": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef tree_diameter(root: TreeNode) -> int:\n    max_d = 0\n    def height(node):\n        nonlocal max_d\n        if not node:\n            return 0\n        lh = height(node.left)\n        rh = height(node.right)\n        max_d = max(max_d, lh + rh)\n        return 1 + max(lh, rh)\n    height(root)\n    return max_d\n\nt = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3))\nprint('Diameter:', tree_diameter(t))\n",
            "expectedOutputPatterns": [
                "Diameter: 3"
            ],
            "hint": "Define nonlocal max_d = 0. In helper height(node): if not node return 0. lh = height(node.left), rh = height(node.right). max_d = max(max_d, lh + rh). Return 1 + max(lh, rh). Return max_d after height(root)."
        },
        "keyTakeaway": "Successfully implemented and verified Tree Properties!"
    },
    {
        "id": "day100-step5",
        "stepNumber": 5,
        "title": "Day 100 Complete: Tree Properties: Height, Diameter & Symmetry",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 100,
        "heading": "Mastery Achieved: Tree Properties: Height, Diameter & Symmetry",
        "subheading": "You have solidified key mental models and techniques for Tree Properties.",
        "recapRows": [
            {
                "concept": "Dual Role Recursion",
                "naiveIntuition": "Separate height function from diameter search (O(N^2))",
                "pythonReality": "Returning local height up the call stack while updating global diameter achieves linear O(N) performance"
            },
            {
                "concept": "Edge Count Invariant",
                "naiveIntuition": "Diameter is node count",
                "pythonReality": "Diameter is traditionally measured in edges between nodes (nodes on path - 1); lh + rh yields edges directly"
            }
        ],
        "solidifiedConcepts": [
            "Post-Order State Aggregation",
            "Global Diameter Calculation (Left + Right)"
        ],
        "nextDayPreview": {
            "dayNumber": 101,
            "title": "Binary Search Tree (BST) Invariant & Search",
            "description": "Understand the BST property (Left < Root < Right), validate BST invariants, and perform O(H) key lookups."
        }
    }
]
},
};
