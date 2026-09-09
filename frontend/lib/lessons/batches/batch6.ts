import { DailyLessonPackage } from "../types";

export const BATCH_6_LESSONS: Record<number, DailyLessonPackage> = {
  101: {
  "dayNumber": 101,
  "title": "Binary Search Tree (BST) Invariant & Search",
  "topicName": "BST Invariant",
  "sectionId": "trees-and-bst",
  "estimatedMinutes": 35,
  "difficulty": "INTERMEDIATE",
  "prerequisites": [
    52,
    97
  ],
  "concepts": [
    "Left < Root < Right Invariant",
    "Recursive Boundary Validation (low, high)"
  ],
  "practiceSkills": [
    "BST Invariant Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Verify binary search tree validity by passing recursive open interval bounds (low, high)",
    "Search for target keys in O(H) time where H is tree height"
  ],
  "practiceArchetype": "completion",
  "flowTier": "tier2"
,
  "steps": [
    {
        "id": "day101-step1",
        "stepNumber": 1,
        "title": "Binary Search Tree (BST) Invariant & Search: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: BST Invariant",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for BST Invariant.",
        "markdownContent": [
            "Binary Search Tree (BST) Invariant requires that for every node, ALL nodes in its left subtree are strictly smaller (`val < root.val`) and ALL nodes in its right subtree are strictly greater (`val > root.val`).",
            "### Foundational Mental Model\nWhen approaching problems requiring **BST Invariant**, remember the central principle: BST validation requires bounding entire subtrees with inherited (min_val, max_val) ranges."
        ],
        "snippets": [
            {
                "title": "BST Invariant Implementation Template",
                "code": "# Valid BST using Range Propagation\ndef is_valid_bst(root):\n    def validate(node, low, high):\n        if not node: return True\n        if not (low < node.val < high): return False\n        return validate(node.left, low, node.val) and validate(node.right, node.val, high)\n    return validate(root, float('-inf'), float('inf'))",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "BST validation requires bounding entire subtrees with inherited (min_val, max_val) ranges."
    },
    {
        "id": "day101-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: BST Invariant",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "A naive check `root.left.val < root.val < root.right.val` is INVALID because it only checks local children, missing violations deep in subtrees. Validating a BST requires propagating a valid range `(min_val, max_val)`: left child range is `(min_val, root.val)` and right child range is `(root.val, max_val)`.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: BST validation requires bounding entire subtrees with inherited (min_val, max_val) ranges.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "BST Invariant Core Invariant",
                "content": "BST validation requires bounding entire subtrees with inherited (min_val, max_val) ranges."
            }
        ],
        "keyTakeaway": "Operational invariant locked: BST validation requires bounding entire subtrees with inherited (min_val, max_val) ranges."
    },
    {
        "id": "day101-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: BST Invariant",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d101-q1",
                "question": "Why is checking only `node.left.val < node.val < node.right.val` insufficient to validate a BST?",
                "options": [
                    {
                        "id": "A",
                        "label": "A node deep in the left subtree might have a value greater than an ancestor root, violating the global BST property while satisfying local child checks"
                    },
                    {
                        "id": "B",
                        "label": "Because binary search trees cannot have duplicate values"
                    },
                    {
                        "id": "C",
                        "label": "Because left child can be None"
                    },
                    {
                        "id": "D",
                        "label": "Because negative numbers break comparison"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Consider root=10, root.left=5, root.left.right=15. Locally, 15 > 5 is valid, but 15 > 10 violates the invariant that ALL nodes in the left subtree of 10 must be < 10.",
                    "B": "Incorrect: While duplicates are excluded, the flaw is global scope violation.",
                    "C": "Incorrect: None checks are trivially handled.",
                    "D": "Incorrect: Python comparisons handle negative numbers uniformly."
                }
            },
            {
                "id": "chk-d101-q2",
                "question": "What is the alternative method to validate a BST using in-order traversal?",
                "options": [
                    {
                        "id": "A",
                        "label": "Perform an in-order traversal and verify that every visited node is strictly greater than the previously visited node"
                    },
                    {
                        "id": "B",
                        "label": "Check if tree depth is log N"
                    },
                    {
                        "id": "C",
                        "label": "Sum all nodes and check if even"
                    },
                    {
                        "id": "D",
                        "label": "Level-order traversal must be sorted"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Because in-order traversal of a valid BST visits keys in strictly increasing order, tracking `prev_val` and asserting `node.val > prev_val` validates the BST in O(N) time.",
                    "B": "Incorrect: BSTs are not necessarily balanced.",
                    "C": "Incorrect: Sum parity is unrelated to ordering.",
                    "D": "Incorrect: Level-order is not sorted."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day101-step4",
        "stepNumber": 4,
        "title": "Guided Practice: BST Invariant",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Validate whether a binary tree satisfies the Binary Search Tree invariant.",
        "subheading": "Implement and verify BST Invariant in the interactive workspace.",
        "task": {
            "title": "Validate whether a binary tree satisfies the Binary Search Tree invariant.",
            "instructions": [
                "Validate whether a binary tree satisfies the Binary Search Tree invariant.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef is_valid_bst(root: TreeNode) -> bool:\n    # TODO: Validate BST using range propagation\n    return False\n\n# Valid: 2 (1, 3)\nt1 = TreeNode(2, TreeNode(1), TreeNode(3))\n# Invalid: 5 (1, 4 with left: 3, right: 6) -> 3 is in right subtree of 5 but < 5\nt2 = TreeNode(5, TreeNode(1), TreeNode(4, TreeNode(3), TreeNode(6)))\nprint('T1 Valid:', is_valid_bst(t1))\nprint('T2 Valid:', is_valid_bst(t2))\n",
            "solutionCode": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef is_valid_bst(root: TreeNode) -> bool:\n    def validate(node, low, high):\n        if not node:\n            return True\n        if not (low < node.val < high):\n            return False\n        return validate(node.left, low, node.val) and validate(node.right, node.val, high)\n    return validate(root, float('-inf'), float('inf'))\n\nt1 = TreeNode(2, TreeNode(1), TreeNode(3))\nt2 = TreeNode(5, TreeNode(1), TreeNode(4, TreeNode(3), TreeNode(6)))\nprint('T1 Valid:', is_valid_bst(t1))\nprint('T2 Valid:', is_valid_bst(t2))\n",
            "expectedOutputPatterns": [
                "T1 Valid: True",
                "T2 Valid: False"
            ],
            "hint": "Helper validate(node, low, high): if not node: return True. If not (low < node.val < high): return False. Return validate(node.left, low, node.val) and validate(node.right, node.val, high)."
        },
        "keyTakeaway": "Successfully implemented and verified BST Invariant!"
    },
    {
        "id": "day101-step5",
        "stepNumber": 5,
        "title": "Day 101 Complete: Binary Search Tree (BST) Invariant & Search",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 101,
        "heading": "Mastery Achieved: Binary Search Tree (BST) Invariant & Search",
        "subheading": "You have solidified key mental models and techniques for BST Invariant.",
        "recapRows": [
            {
                "concept": "Global Invariant Range",
                "naiveIntuition": "Compare node with immediate children",
                "pythonReality": "Every node inherits bounding constraints (min, max) from all ancestors along its path from root"
            },
            {
                "concept": "Strict Monotonicity",
                "naiveIntuition": "BST permits equal values on left or right",
                "pythonReality": "Standard BST definition enforces strictly less (<) and strictly greater (>); duplicates require frequency counters"
            }
        ],
        "solidifiedConcepts": [
            "Left < Root < Right Invariant",
            "Recursive Boundary Validation (low, high)"
        ],
        "nextDayPreview": {
            "dayNumber": 102,
            "title": "BST Insertion, Deletion & Successor Rewiring",
            "description": "Implement BST insertion and deletion, handling 0, 1, and 2-child cases and in-order successor replacements."
        }
    }
]
},
  102: {
  "dayNumber": 102,
  "title": "BST Insertion, Deletion & Successor Rewiring",
  "topicName": "BST Mutations",
  "sectionId": "trees-and-bst",
  "estimatedMinutes": 45,
  "difficulty": "INTERMEDIATE",
  "prerequisites": [
    101
  ],
  "concepts": [
    "In-Order Successor Substitution",
    "Two-Child Deletion Rewiring"
  ],
  "practiceSkills": [
    "BST Mutations Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Insert new values into BST leaf positions preserving the BST invariant",
    "Delete interior nodes with two children by substituting the in-order successor"
  ],
  "practiceArchetype": "debugging",
  "flowTier": "tier3"
,
  "steps": [
    {
        "id": "day102-step1",
        "stepNumber": 1,
        "title": "BST Insertion, Deletion & Successor Rewiring: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: BST Mutations",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for BST Mutations.",
        "markdownContent": [
            "BST Search, Insertion, and Deletion operate in O(H) time by steering left or right, with deletion managing 3 structural cases: leaf node, single child, and two children.",
            "### Foundational Mental Model\nWhen approaching problems requiring **BST Mutations**, remember the central principle: Two-child deletion preserves the BST invariant by splicing the in-order successor."
        ],
        "snippets": [
            {
                "title": "BST Mutations Implementation Template",
                "code": "# BST Insertion\ndef insert_into_bst(root, val):\n    if not root: return TreeNode(val)\n    if val < root.val: root.left = insert_into_bst(root.left, val)\n    else: root.right = insert_into_bst(root.right, val)\n    return root",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Two-child deletion preserves the BST invariant by splicing the in-order successor."
    },
    {
        "id": "day102-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: BST Mutations",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Search: if `target < val` steer left, elif `target > val` steer right, else found. Insert: traverse to empty spot and attach new node. Delete node with 2 children: replace node's value with its In-order Successor (smallest value in right subtree), then delete the successor from the right subtree.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Two-child deletion preserves the BST invariant by splicing the in-order successor.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "BST Mutations Core Invariant",
                "content": "Two-child deletion preserves the BST invariant by splicing the in-order successor."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Two-child deletion preserves the BST invariant by splicing the in-order successor."
    },
    {
        "id": "day102-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: BST Mutations",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d102-q1",
                "question": "Why is the In-order Successor (minimum node in the right subtree) used to replace a deleted node with two children?",
                "options": [
                    {
                        "id": "A",
                        "label": "It is guaranteed to be greater than all nodes in the left subtree and smaller than all remaining nodes in the right subtree, preserving the BST invariant"
                    },
                    {
                        "id": "B",
                        "label": "Because it has no children at all"
                    },
                    {
                        "id": "C",
                        "label": "Because it is stored at index 0 in memory"
                    },
                    {
                        "id": "D",
                        "label": "Because Python automatically selects it"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! The in-order successor is the immediately next key in sorted order. Placing it at the deleted position maintains the property that left subtree < new_val < right subtree.",
                    "B": "Incorrect: The successor can have a right child (though it cannot have a left child).",
                    "C": "Incorrect: Tree nodes are non-contiguous heap objects.",
                    "D": "Incorrect: Successor selection is an explicit algorithmic step."
                }
            },
            {
                "id": "chk-d102-q2",
                "question": "Can the In-order Successor of a node ever have a left child?",
                "options": [
                    {
                        "id": "A",
                        "label": "No, because any left child would have a smaller value, contradicting the fact that the successor is the minimum node in that subtree"
                    },
                    {
                        "id": "B",
                        "label": "Yes, it can have up to 2 left children"
                    },
                    {
                        "id": "C",
                        "label": "Yes, if the tree is unbalanced"
                    },
                    {
                        "id": "D",
                        "label": "Only in AVL trees"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Finding the minimum in a subtree follows left pointers until `curr.left is None`. Hence, the in-order successor is guaranteed to have at most ONE child (a right child).",
                    "B": "Incorrect: Binary tree nodes have at most 1 left child.",
                    "C": "Incorrect: Minimum property guarantees curr.left is None.",
                    "D": "Incorrect: True for all BSTs."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day102-step4",
        "stepNumber": 4,
        "title": "Guided Practice: BST Mutations",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Insert a value into a Binary Search Tree and return the root.",
        "subheading": "Implement and verify BST Mutations in the interactive workspace.",
        "task": {
            "title": "Insert a value into a Binary Search Tree and return the root.",
            "instructions": [
                "Insert a value into a Binary Search Tree and return the root.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef insert_bst(root: TreeNode, val: int) -> TreeNode:\n    # TODO: Recursively insert val into BST\n    return root\n\ndef inorder(node):\n    return inorder(node.left) + [node.val] + inorder(node.right) if node else []\n\nroot = TreeNode(4, TreeNode(2), TreeNode(7))\ninsert_bst(root, 5)\nprint('Inorder after insert 5:', inorder(root))\n",
            "solutionCode": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef insert_bst(root: TreeNode, val: int) -> TreeNode:\n    if not root:\n        return TreeNode(val)\n    if val < root.val:\n        root.left = insert_bst(root.left, val)\n    else:\n        root.right = insert_bst(root.right, val)\n    return root\n\ndef inorder(node):\n    return inorder(node.left) + [node.val] + inorder(node.right) if node else []\n\nroot = TreeNode(4, TreeNode(2), TreeNode(7))\ninsert_bst(root, 5)\nprint('Inorder after insert 5:', inorder(root))\n",
            "expectedOutputPatterns": [
                "Inorder after insert 5: [2, 4, 5, 7]"
            ],
            "hint": "if not root return TreeNode(val). If val < root.val: root.left = insert_bst(root.left, val) else: root.right = insert_bst(root.right, val). Return root."
        },
        "keyTakeaway": "Successfully implemented and verified BST Mutations!"
    },
    {
        "id": "day102-step5",
        "stepNumber": 5,
        "title": "Day 102 Complete: BST Insertion, Deletion & Successor Rewiring",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 102,
        "heading": "Mastery Achieved: BST Insertion, Deletion & Successor Rewiring",
        "subheading": "You have solidified key mental models and techniques for BST Mutations.",
        "recapRows": [
            {
                "concept": "Search Steering Property",
                "naiveIntuition": "Search both subtrees like normal binary tree",
                "pythonReality": "Comparing target with root.val halves the search path at every step, taking O(H) time without inspecting both sides"
            },
            {
                "concept": "Successor Simplicity",
                "naiveIntuition": "Deleting a 2-child node requires restructuring the entire tree",
                "pythonReality": "Copying the successor's value and deleting the successor reduces 2-child deletion to trivial 0-or-1 child deletion"
            }
        ],
        "solidifiedConcepts": [
            "In-Order Successor Substitution",
            "Two-Child Deletion Rewiring"
        ],
        "nextDayPreview": {
            "dayNumber": 103,
            "title": "Lowest Common Ancestor (LCA) in BST and Tree",
            "description": "Find the Lowest Common Ancestor (LCA) in BSTs in O(H) time and general binary trees in O(N) time via DFS."
        }
    }
]
},
  103: {
  "dayNumber": 103,
  "title": "Lowest Common Ancestor (LCA) in BST and Tree",
  "topicName": "Lowest Common Ancestor",
  "sectionId": "trees-and-bst",
  "estimatedMinutes": 35,
  "difficulty": "INTERMEDIATE",
  "prerequisites": [
    101
  ],
  "concepts": [
    "BST Value-Guided Bifurcation",
    "General Tree Dual-Branch DFS"
  ],
  "practiceSkills": [
    "Lowest Common Ancestor Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Find the LCA of two nodes in a BST in O(H) time using numerical value bifurcation",
    "Locate LCA in general binary trees using post-order node presence bubbling"
  ],
  "practiceArchetype": "problem",
  "flowTier": "tier2"
,
  "steps": [
    {
        "id": "day103-step1",
        "stepNumber": 1,
        "title": "Lowest Common Ancestor (LCA) in BST and Tree: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Lowest Common Ancestor",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Lowest Common Ancestor.",
        "markdownContent": [
            "Lowest Common Ancestor (LCA) in a Binary Tree identifies the deepest node that has both nodes p and q as descendants using bottom-up subtree search in O(N) time.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Lowest Common Ancestor**, remember the central principle: When left and right subtrees each return one of the target nodes, the current root is their Lowest Common Ancestor."
        ],
        "snippets": [
            {
                "title": "Lowest Common Ancestor Implementation Template",
                "code": "# Lowest Common Ancestor (Binary Tree)\ndef lowest_common_ancestor(root, p, q):\n    if not root or root == p or root == q:\n        return root\n    left = lowest_common_ancestor(root.left, p, q)\n    right = lowest_common_ancestor(root.right, p, q)\n    if left and right: return root # Both sides found\n    return left or right          # Pass up whichever was found",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "When left and right subtrees each return one of the target nodes, the current root is their Lowest Common Ancestor."
    },
    {
        "id": "day103-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Lowest Common Ancestor",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "If `root in (None, p, q)`: return root. Search left and right subtrees: `left = LCA(root.left, p, q)` and `right = LCA(root.right, p, q)`. If both `left` and `right` return non-null, `root` is the LCA! If only one is non-null, propagate that non-null node up.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: When left and right subtrees each return one of the target nodes, the current root is their Lowest Common Ancestor.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Lowest Common Ancestor Core Invariant",
                "content": "When left and right subtrees each return one of the target nodes, the current root is their Lowest Common Ancestor."
            }
        ],
        "keyTakeaway": "Operational invariant locked: When left and right subtrees each return one of the target nodes, the current root is their Lowest Common Ancestor."
    },
    {
        "id": "day103-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Lowest Common Ancestor",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d103-q1",
                "question": "If `left` returns node `p` and `right` returns node `q`, why is `root` guaranteed to be their Lowest Common Ancestor?",
                "options": [
                    {
                        "id": "A",
                        "label": "Because `p` and `q` are located in different subtrees branching directly off `root`, making `root` their lowest mutual convergence point"
                    },
                    {
                        "id": "B",
                        "label": "Because `root` is always the LCA for any pair"
                    },
                    {
                        "id": "C",
                        "label": "Because left is smaller than right in all binary trees"
                    },
                    {
                        "id": "D",
                        "label": "Because p and q have identical heights"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Since one target resides in the left subtree and the other resides in the right subtree, no deeper descendant node can be an ancestor to both. The current node is the lowest common point.",
                    "B": "Incorrect: Ancestor can be a deeper node than tree root.",
                    "C": "Incorrect: Only BSTs have value ordering.",
                    "D": "Incorrect: Targets can reside at different heights."
                }
            },
            {
                "id": "chk-d103-q2",
                "question": "What happens in the LCA algorithm if node `q` is a direct descendant of node `p`?",
                "options": [
                    {
                        "id": "A",
                        "label": "The algorithm returns `p` immediately when visiting `p`, because `p` is its own ancestor and the search does not need to delve deeper"
                    },
                    {
                        "id": "B",
                        "label": "The algorithm returns None"
                    },
                    {
                        "id": "C",
                        "label": "An infinite recursion occurs"
                    },
                    {
                        "id": "D",
                        "label": "The algorithm returns root"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! The base case `if root == p:` returns `p`. Since `q` is inside `p`'s subtree, `p` will bubble up as the sole non-null return value to the top, correctly identifying `p` as the LCA.",
                    "B": "Incorrect: A non-null ancestor is found.",
                    "C": "Incorrect: Trees are acyclic.",
                    "D": "Incorrect: Returns the lowest ancestor p."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day103-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Lowest Common Ancestor",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Find the Lowest Common Ancestor of two given nodes in a binary tree.",
        "subheading": "Implement and verify Lowest Common Ancestor in the interactive workspace.",
        "task": {
            "title": "Find the Lowest Common Ancestor of two given nodes in a binary tree.",
            "instructions": [
                "Find the Lowest Common Ancestor of two given nodes in a binary tree.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef find_lca(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:\n    # TODO: Implement bottom-up LCA search\n    return None\n\n# 3 -> left: 5 (left: 6, right: 2), right: 1 (left: 0, right: 8)\nn6 = TreeNode(6); n2 = TreeNode(2); n5 = TreeNode(5, n6, n2)\nn0 = TreeNode(0); n8 = TreeNode(8); n1 = TreeNode(1, n0, n8)\nroot = TreeNode(3, n5, n1)\n\n# LCA of 5 and 1 is 3\nprint('LCA(5, 1):', find_lca(root, n5, n1).val)\n# LCA of 5 and 2 is 5\nprint('LCA(5, 2):', find_lca(root, n5, n2).val)\n",
            "solutionCode": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef find_lca(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:\n    if not root or root == p or root == q:\n        return root\n    left = find_lca(root.left, p, q)\n    right = find_lca(root.right, p, q)\n    if left and right:\n        return root\n    return left or right\n\nn6 = TreeNode(6); n2 = TreeNode(2); n5 = TreeNode(5, n6, n2)\nn0 = TreeNode(0); n8 = TreeNode(8); n1 = TreeNode(1, n0, n8)\nroot = TreeNode(3, n5, n1)\n\nprint('LCA(5, 1):', find_lca(root, n5, n1).val)\nprint('LCA(5, 2):', find_lca(root, n5, n2).val)\n",
            "expectedOutputPatterns": [
                "LCA(5, 1): 3",
                "LCA(5, 2): 5"
            ],
            "hint": "if not root or root == p or root == q: return root. left = find_lca(root.left, p, q); right = find_lca(root.right, p, q). If left and right: return root. Return left or right."
        },
        "keyTakeaway": "Successfully implemented and verified Lowest Common Ancestor!"
    },
    {
        "id": "day103-step5",
        "stepNumber": 5,
        "title": "Day 103 Complete: Lowest Common Ancestor (LCA) in BST and Tree",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 103,
        "heading": "Mastery Achieved: Lowest Common Ancestor (LCA) in BST and Tree",
        "subheading": "You have solidified key mental models and techniques for Lowest Common Ancestor.",
        "recapRows": [
            {
                "concept": "Convergence Bubbling",
                "naiveIntuition": "Store root-to-node paths in lists and compare prefixes",
                "pythonReality": "Bottom-up DFS bubbles found references up the stack, identifying convergence directly in O(1) auxiliary stack frames"
            },
            {
                "concept": "Ancestor Self-Inclusion",
                "naiveIntuition": "A node cannot be its own ancestor",
                "pythonReality": "In tree hierarchy, a node is considered a descendant of itself, allowing ancestor queries where p is an ancestor of q"
            }
        ],
        "solidifiedConcepts": [
            "BST Value-Guided Bifurcation",
            "General Tree Dual-Branch DFS"
        ],
        "nextDayPreview": {
            "dayNumber": 104,
            "title": "Tree Serialization & Deserialization",
            "description": "Serialize binary trees into flat string representations and reconstruct them using pre-order and BFS iterators."
        }
    }
]
},
  104: {
  "dayNumber": 104,
  "title": "Tree Serialization & Deserialization",
  "topicName": "Tree Serialization",
  "sectionId": "trees-and-bst",
  "estimatedMinutes": 40,
  "difficulty": "INTERMEDIATE",
  "prerequisites": [
    97,
    99
  ],
  "concepts": [
    "Pre-order String Representation",
    "None Marker Stream Reconstruction"
  ],
  "practiceSkills": [
    "Tree Serialization Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Encode a binary tree into a delimited string representation using pre-order traversal with null markers",
    "Reconstruct the identical tree structure from string tokens in O(N) time"
  ],
  "practiceArchetype": "algorithm",
  "flowTier": "tier3"
,
  "steps": [
    {
        "id": "day104-step1",
        "stepNumber": 1,
        "title": "Tree Serialization & Deserialization: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Tree Serialization",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Tree Serialization.",
        "markdownContent": [
            "Tree Serialization converts a tree structure into a flat string representation using delimiter tokens and null sentinels ('#'), and deserialization reconstructs the tree in O(N) time.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Tree Serialization**, remember the central principle: Explicit null sentinels eliminate ambiguity, allowing single-pass preorder serialization and deserialization."
        ],
        "snippets": [
            {
                "title": "Tree Serialization Implementation Template",
                "code": "# Serialization & Deserialization\ndef serialize(root):\n    res = []\n    def dfs(node):\n        if not node: res.append('#'); return\n        res.append(str(node.val))\n        dfs(node.left)\n        dfs(node.right)\n    dfs(root)\n    return ','.join(res)\n\ndef deserialize(data):\n    tokens = iter(data.split(','))\n    def dfs():\n        val = next(tokens)\n        if val == '#': return None\n        node = TreeNode(int(val))\n        node.left = dfs()\n        node.right = dfs()\n        return node\n    return dfs()",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Explicit null sentinels eliminate ambiguity, allowing single-pass preorder serialization and deserialization."
    },
    {
        "id": "day104-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Tree Serialization",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Serialize: pre-order traversal writing `node.val` and `'#'` for `None`, joined by commas. Deserialize: split string into token queue/iterator. For each token: if `'#'` return None; else create `node = TreeNode(int(token))`, then recursively construct `node.left` and `node.right`.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Explicit null sentinels eliminate ambiguity, allowing single-pass preorder serialization and deserialization.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Tree Serialization Core Invariant",
                "content": "Explicit null sentinels eliminate ambiguity, allowing single-pass preorder serialization and deserialization."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Explicit null sentinels eliminate ambiguity, allowing single-pass preorder serialization and deserialization."
    },
    {
        "id": "day104-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Tree Serialization",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d104-q1",
                "question": "Why does preorder traversal with null markers ('#') allow unique reconstruction, whereas preorder without null markers cannot?",
                "options": [
                    {
                        "id": "A",
                        "label": "Null markers explicitly record when child branches terminate, removing all ambiguity about node leaf/internal status"
                    },
                    {
                        "id": "B",
                        "label": "Because strings cannot store numbers"
                    },
                    {
                        "id": "C",
                        "label": "Because commas sort the values"
                    },
                    {
                        "id": "D",
                        "label": "It makes the string shorter"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Without null markers, [1, 2] could mean 1 has left child 2, or 1 has right child 2. Recording '1,2,#,#,#' unambiguously pins down the exact empty slots.",
                    "B": "Incorrect: Python strings readily store digits.",
                    "C": "Incorrect: Commas act as delimiters, not sorters.",
                    "D": "Incorrect: Null markers increase length but guarantee uniqueness."
                }
            },
            {
                "id": "chk-d104-q2",
                "question": "What is the time complexity of deserializing a tree string of N nodes using an iterator?",
                "options": [
                    {
                        "id": "A",
                        "label": "O(N), because each token is consumed once by `next(tokens)` in O(1)"
                    },
                    {
                        "id": "B",
                        "label": "O(N^2)"
                    },
                    {
                        "id": "C",
                        "label": "O(N log N)"
                    },
                    {
                        "id": "D",
                        "label": "O(2^N)"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Splitting takes O(N) time. The iterator advances forward monotonically with each node creation, consuming 2N + 1 tokens total (N nodes + N + 1 null sentinels). Overall: O(N).",
                    "B": "Incorrect: No nested token scanning occurs.",
                    "C": "Incorrect: No sorting is involved.",
                    "D": "Incorrect: Linear traversal through tokens."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day104-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Tree Serialization",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Serialize a binary tree to string and deserialize it back, verifying structure preservation.",
        "subheading": "Implement and verify Tree Serialization in the interactive workspace.",
        "task": {
            "title": "Serialize a binary tree to string and deserialize it back, verifying structure preservation.",
            "instructions": [
                "Serialize a binary tree to string and deserialize it back, verifying structure preservation.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef serialize(root: TreeNode) -> str:\n    # TODO: Serialize tree to comma-separated string with '#' for None\n    return ''\n\ndef deserialize(data: str) -> TreeNode:\n    # TODO: Reconstruct tree from serialized string\n    return None\n\nt = TreeNode(1, TreeNode(2), TreeNode(3, TreeNode(4), TreeNode(5)))\ns = serialize(t)\nprint('Serialized:', s)\nrebuilt = deserialize(s)\nprint('Rebuilt root:', rebuilt.val, 'Rebuilt right left:', rebuilt.right.left.val)\n",
            "solutionCode": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef serialize(root: TreeNode) -> str:\n    res = []\n    def dfs(node):\n        if not node:\n            res.append('#')\n            return\n        res.append(str(node.val))\n        dfs(node.left)\n        dfs(node.right)\n    dfs(root)\n    return ','.join(res)\n\ndef deserialize(data: str) -> TreeNode:\n    tokens = iter(data.split(','))\n    def dfs():\n        val = next(tokens)\n        if val == '#':\n            return None\n        node = TreeNode(int(val))\n        node.left = dfs()\n        node.right = dfs()\n        return node\n    return dfs()\n\nt = TreeNode(1, TreeNode(2), TreeNode(3, TreeNode(4), TreeNode(5)))\ns = serialize(t)\nprint('Serialized:', s)\nrebuilt = deserialize(s)\nprint('Rebuilt root:', rebuilt.val, 'Rebuilt right left:', rebuilt.right.left.val)\n",
            "expectedOutputPatterns": [
                "Serialized: 1,2,#,#,3,4,#,#,5,#,#",
                "Rebuilt root: 1 Rebuilt right left: 4"
            ],
            "hint": "In serialize: if not node res.append('#'); else append str(node.val), dfs(left), dfs(right). Return ','.join(res). In deserialize: tokens = iter(data.split(',')). Helper dfs(): val = next(tokens); if val == '#' return None. node = TreeNode(int(val)), left = dfs(), right = dfs(). Return node."
        },
        "keyTakeaway": "Successfully implemented and verified Tree Serialization!"
    },
    {
        "id": "day104-step5",
        "stepNumber": 5,
        "title": "Day 104 Complete: Tree Serialization & Deserialization",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 104,
        "heading": "Mastery Achieved: Tree Serialization & Deserialization",
        "subheading": "You have solidified key mental models and techniques for Tree Serialization.",
        "recapRows": [
            {
                "concept": "State Marshalling",
                "naiveIntuition": "Save pointers to disk directly",
                "pythonReality": "Memory addresses are ephemeral; flattening data structures into canonical text/binary formats is required for persistence and network transmission"
            },
            {
                "concept": "Sentinel Disambiguation",
                "naiveIntuition": "Omit empty children to save space",
                "pythonReality": "Explicit null sentinels eliminate ambiguity, allowing single-pass linear reconstruction"
            }
        ],
        "solidifiedConcepts": [
            "Pre-order String Representation",
            "None Marker Stream Reconstruction"
        ],
        "nextDayPreview": {
            "dayNumber": 105,
            "title": "Morris In-Order Traversal & Threaded Pointers",
            "description": "Traverse binary trees in-order in O(1) auxiliary space using Morris Traversal and threaded binary tree pointers."
        }
    }
]
},
  105: {
  "dayNumber": 105,
  "title": "Morris In-Order Traversal & Threaded Pointers",
  "topicName": "Morris Traversal",
  "sectionId": "trees-and-bst",
  "estimatedMinutes": 45,
  "difficulty": "INTERMEDIATE",
  "prerequisites": [
    102
  ],
  "concepts": [
    "In-Order Predecessor Rightmost Pointer",
    "O(1) Auxiliary Space Invariant"
  ],
  "practiceSkills": [
    "Morris Traversal Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Establish temporary threads from in-order predecessors to current nodes",
    "Traverse binary search trees in strictly O(1) auxiliary space without stack or recursion"
  ],
  "practiceArchetype": "algorithm",
  "flowTier": "tier3"
,
  "steps": [
    {
        "id": "day105-step1",
        "stepNumber": 1,
        "title": "Morris In-Order Traversal & Threaded Pointers: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Morris Traversal",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Morris Traversal.",
        "markdownContent": [
            "Morris In-Order Traversal achieves O(N) time and strictly O(1) auxiliary space by temporarily threading unused null pointers of in-order predecessors back to current nodes.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Morris Traversal**, remember the central principle: Morris traversal eliminates recursion stacks by threading leaf null pointers back to ancestors."
        ],
        "snippets": [
            {
                "title": "Morris Traversal Implementation Template",
                "code": "# Morris In-Order Traversal in O(1) space\ndef morris_inorder(root):\n    res = []\n    curr = root\n    while curr:\n        if not curr.left:\n            res.append(curr.val)\n            curr = curr.right\n        else:\n            pred = curr.left\n            while pred.right and pred.right != curr:\n                pred = pred.right\n            if not pred.right:\n                pred.right = curr # Thread!\n                curr = curr.left\n            else:\n                pred.right = None # Remove thread!\n                res.append(curr.val)\n                curr = curr.right\n    return res",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Morris traversal eliminates recursion stacks by threading leaf null pointers back to ancestors."
    },
    {
        "id": "day105-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Morris Traversal",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "For node `curr`: if `curr.left is None`: visit `curr.val`, `curr = curr.right`. Else find in-order predecessor `pred` (rightmost node of left subtree). If `pred.right is None`: create thread `pred.right = curr` and move `curr = curr.left`. If `pred.right == curr`: dismantle thread `pred.right = None`, visit `curr.val`, move `curr = curr.right`.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Morris traversal eliminates recursion stacks by threading leaf null pointers back to ancestors.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Morris Traversal Core Invariant",
                "content": "Morris traversal eliminates recursion stacks by threading leaf null pointers back to ancestors."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Morris traversal eliminates recursion stacks by threading leaf null pointers back to ancestors."
    },
    {
        "id": "day105-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Morris Traversal",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d105-q1",
                "question": "How does Morris Traversal achieve O(1) space without a stack or recursion?",
                "options": [
                    {
                        "id": "A",
                        "label": "It temporarily utilizes the unused null right pointers of leaf nodes to store return paths back up to ancestors"
                    },
                    {
                        "id": "B",
                        "label": "It compresses node values into a 64-bit integer"
                    },
                    {
                        "id": "C",
                        "label": "It uses Python generator closures"
                    },
                    {
                        "id": "D",
                        "label": "It converts the tree into an array"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Every in-order predecessor has a null right pointer. Morris temporarily points this null reference to `curr`, providing an O(1) return bridge back up to the ancestor without a call stack.",
                    "B": "Incorrect: Pointer threading is used, not value compression.",
                    "C": "Incorrect: Python generators still require stack frames.",
                    "D": "Incorrect: An array consumes O(N) auxiliary space."
                }
            },
            {
                "id": "chk-d105-q2",
                "question": "Why must the temporary thread `pred.right = None` be removed during the second visit?",
                "options": [
                    {
                        "id": "A",
                        "label": "To restore the tree to its exact original structure and prevent infinite cycles during subsequent operations"
                    },
                    {
                        "id": "B",
                        "label": "To free heap memory"
                    },
                    {
                        "id": "C",
                        "label": "Because Python forbids circular references"
                    },
                    {
                        "id": "D",
                        "label": "To trigger garbage collection"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Tree traversals must not permanently mutate the caller's data structure. Restoring `pred.right = None` leaves the tree in its original, unmodified state.",
                    "B": "Incorrect: No new memory was allocated.",
                    "C": "Incorrect: Python allows circular structures, but tree invariants forbid cycles.",
                    "D": "Incorrect: Garbage collection is not triggered by restoring pointers."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day105-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Morris Traversal",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Implement Morris Traversal to retrieve in-order values with O(1) auxiliary space.",
        "subheading": "Implement and verify Morris Traversal in the interactive workspace.",
        "task": {
            "title": "Implement Morris Traversal to retrieve in-order values with O(1) auxiliary space.",
            "instructions": [
                "Implement Morris Traversal to retrieve in-order values with O(1) auxiliary space.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef morris_traversal(root: TreeNode) -> list[int]:\n    # TODO: Implement Morris in-order traversal using temporary pointer threading\n    return []\n\n# 2 -> left: 1, right: 3\nt = TreeNode(2, TreeNode(1), TreeNode(3))\nprint('Morris Inorder:', morris_traversal(t))\n",
            "solutionCode": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef morris_traversal(root: TreeNode) -> list[int]:\n    res = []\n    curr = root\n    while curr:\n        if not curr.left:\n            res.append(curr.val)\n            curr = curr.right\n        else:\n            pred = curr.left\n            while pred.right and pred.right != curr:\n                pred = pred.right\n            if not pred.right:\n                pred.right = curr\n                curr = curr.left\n            else:\n                pred.right = None\n                res.append(curr.val)\n                curr = curr.right\n    return res\n\nt = TreeNode(2, TreeNode(1), TreeNode(3))\nprint('Morris Inorder:', morris_traversal(t))\n",
            "expectedOutputPatterns": [
                "Morris Inorder: [1, 2, 3]"
            ],
            "hint": "Loop while curr: if not curr.left: res.append(curr.val); curr = curr.right. Else pred = curr.left; find rightmost node not equal to curr. If pred.right is None: thread pred.right = curr; curr = curr.left. Else: unthread pred.right = None; res.append(curr.val); curr = curr.right."
        },
        "keyTakeaway": "Successfully implemented and verified Morris Traversal!"
    },
    {
        "id": "day105-step5",
        "stepNumber": 5,
        "title": "Day 105 Complete: Morris In-Order Traversal & Threaded Pointers",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 105,
        "heading": "Mastery Achieved: Morris In-Order Traversal & Threaded Pointers",
        "subheading": "You have solidified key mental models and techniques for Morris Traversal.",
        "recapRows": [
            {
                "concept": "Threaded Return Paths",
                "naiveIntuition": "O(1) space traversal is impossible because trees have no parent pointers",
                "pythonReality": "Repurposing dead null pointers as temporary escape ropes allows climbing back up without call stack memory"
            },
            {
                "concept": "Two-Pass Edge Invariant",
                "naiveIntuition": "Finding predecessors makes Morris O(N^2)",
                "pythonReality": "Each edge is traversed at most 3 times (create thread, explore, dismantle thread), bounding total time to strictly O(N)"
            }
        ],
        "solidifiedConcepts": [
            "In-Order Predecessor Rightmost Pointer",
            "O(1) Auxiliary Space Invariant"
        ],
        "nextDayPreview": {
            "dayNumber": 106,
            "title": "Balanced BSTs: AVL Tree Rotations (LL, RR)",
            "description": "Understand AVL balance factors, height-balance invariants, and implement left and right tree rotations."
        }
    }
]
},
  106: {
  "dayNumber": 106,
  "title": "Balanced BSTs: AVL Tree Rotations (LL, RR)",
  "topicName": "AVL Rotations",
  "sectionId": "trees-and-bst",
  "estimatedMinutes": 45,
  "difficulty": "INTERMEDIATE",
  "prerequisites": [
    102
  ],
  "concepts": [
    "Height Balance Factor (-1, 0, +1)",
    "Single & Double Rotations (LL, RR, LR, RL)"
  ],
  "practiceSkills": [
    "AVL Rotations Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Calculate AVL node balance factors from left and right subtree heights",
    "Trace single and double tree rotations that restore O(log N) height balance"
  ],
  "practiceArchetype": "tracing",
  "flowTier": "tier3"
,
  "steps": [
    {
        "id": "day106-step1",
        "stepNumber": 1,
        "title": "Balanced BSTs: AVL Tree Rotations (LL, RR): Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: AVL Rotations",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for AVL Rotations.",
        "markdownContent": [
            "AVL Trees maintain self-balancing guarantees where balance factor (height(left) - height(right)) remains in {-1, 0, 1} via four rotation primitives.",
            "### Foundational Mental Model\nWhen approaching problems requiring **AVL Rotations**, remember the central principle: AVL rotations rebalance subtrees in O(1) time while preserving BST in-order invariants."
        ],
        "snippets": [
            {
                "title": "AVL Rotations Implementation Template",
                "code": "# Right Rotation on Node y (Left-Left rebalance)\n#     y               x\n#    / \\             / \\\n#   x   T3   -->    T1  y\n#  / \\                 / \\\n# T1  T2              T2 T3\ndef rotate_right(y):\n    x = y.left\n    T2 = x.right\n    x.right = y\n    y.left = T2\n    return x # New root of subtree",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "AVL rotations rebalance subtrees in O(1) time while preserving BST in-order invariants."
    },
    {
        "id": "day106-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: AVL Rotations",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Rotations update child references in O(1) time without altering in-order BST ordering. 4 Cases: (1) Left-Left: single Right Rotation on root. (2) Right-Right: single Left Rotation on root. (3) Left-Right: Left Rotation on left child, then Right Rotation on root. (4) Right-Left: Right Rotation on right child, then Left Rotation on root.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: AVL rotations rebalance subtrees in O(1) time while preserving BST in-order invariants.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "AVL Rotations Core Invariant",
                "content": "AVL rotations rebalance subtrees in O(1) time while preserving BST in-order invariants."
            }
        ],
        "keyTakeaway": "Operational invariant locked: AVL rotations rebalance subtrees in O(1) time while preserving BST in-order invariants."
    },
    {
        "id": "day106-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: AVL Rotations",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d106-q1",
                "question": "In an AVL tree Right Rotation on node `y`, what happens to `x.right` (sub-tree T2)?",
                "options": [
                    {
                        "id": "A",
                        "label": "It becomes the left child of node `y` (`y.left = T2`), correctly preserving the invariant `x < T2 < y`"
                    },
                    {
                        "id": "B",
                        "label": "It is deleted from the tree"
                    },
                    {
                        "id": "C",
                        "label": "It becomes the right child of `x`"
                    },
                    {
                        "id": "D",
                        "label": "It becomes the root of the entire tree"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Because T2 was originally in the right subtree of x, `T2 > x`. Because T2 was in the left subtree of y, `T2 < y`. When y becomes x's right child, attaching T2 as y's left child strictly preserves `x < T2 < y`.",
                    "B": "Incorrect: All nodes are preserved.",
                    "C": "Incorrect: x's right child becomes y.",
                    "D": "Incorrect: x becomes the new root of this subtree."
                }
            },
            {
                "id": "chk-d106-q2",
                "question": "When an insertion creates a Left-Right imbalance (node inserted into right subtree of left child), what sequence of rotations is required?",
                "options": [
                    {
                        "id": "A",
                        "label": "Left Rotation on the left child, followed by Right Rotation on the parent"
                    },
                    {
                        "id": "B",
                        "label": "Right Rotation on the parent only"
                    },
                    {
                        "id": "C",
                        "label": "Two Right Rotations on the parent"
                    },
                    {
                        "id": "D",
                        "label": "Left Rotation on the parent only"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! The Left-Right zigzag shape cannot be solved by a single rotation. First, rotating left on the left child straightens the zigzag into a Left-Left line. Second, rotating right on the parent balances the tree.",
                    "B": "Incorrect: Single right rotation leaves the subtree unbalanced.",
                    "C": "Incorrect: Two right rotations corrupt structure.",
                    "D": "Incorrect: Left rotation is for Right-Right cases."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day106-step4",
        "stepNumber": 4,
        "title": "Guided Practice: AVL Rotations",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Implement Right Rotation on a binary tree node and verify pointer reassignment.",
        "subheading": "Implement and verify AVL Rotations in the interactive workspace.",
        "task": {
            "title": "Implement Right Rotation on a binary tree node and verify pointer reassignment.",
            "instructions": [
                "Implement Right Rotation on a binary tree node and verify pointer reassignment.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef right_rotate(y: TreeNode) -> TreeNode:\n    # TODO: Implement right rotation: return new root x\n    return y\n\n# Left-skewed: 3 -> left: 2 (left: 1)\ny = TreeNode(3, TreeNode(2, TreeNode(1))) \nnew_root = right_rotate(y)\nprint('New root:', new_root.val, 'Left:', new_root.left.val, 'Right:', new_root.right.val)\n",
            "solutionCode": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef right_rotate(y: TreeNode) -> TreeNode:\n    x = y.left\n    T2 = x.right\n    x.right = y\n    y.left = T2\n    return x\n\ny = TreeNode(3, TreeNode(2, TreeNode(1)))\nnew_root = right_rotate(y)\nprint('New root:', new_root.val, 'Left:', new_root.left.val, 'Right:', new_root.right.val)\n",
            "expectedOutputPatterns": [
                "New root: 2 Left: 1 Right: 3"
            ],
            "hint": "x = y.left; T2 = x.right; x.right = y; y.left = T2; return x."
        },
        "keyTakeaway": "Successfully implemented and verified AVL Rotations!"
    },
    {
        "id": "day106-step5",
        "stepNumber": 5,
        "title": "Day 106 Complete: Balanced BSTs: AVL Tree Rotations (LL, RR)",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 106,
        "heading": "Mastery Achieved: Balanced BSTs: AVL Tree Rotations (LL, RR)",
        "subheading": "You have solidified key mental models and techniques for AVL Rotations.",
        "recapRows": [
            {
                "concept": "Rotational Invariant Preservation",
                "naiveIntuition": "Rotations re-order tree values",
                "pythonReality": "Rotations alter depth and topology while keeping the in-order sorted traversal sequence 100% identical"
            },
            {
                "concept": "Logarithmic Height Guarantee",
                "naiveIntuition": "Standard BSTs are always O(log N)",
                "pythonReality": "Without AVL or Red-Black balancing, worst-case insertions degenerate BSTs into O(N) linked lists"
            }
        ],
        "solidifiedConcepts": [
            "Height Balance Factor (-1, 0, +1)",
            "Single & Double Rotations (LL, RR, LR, RL)"
        ],
        "nextDayPreview": {
            "dayNumber": 107,
            "title": "Red-Black Tree Principles & Invariants",
            "description": "Analyze Red-Black tree color invariants, black-height guarantees, and compare performance trade-offs against AVL trees."
        }
    }
]
},
  107: {
  "dayNumber": 107,
  "title": "Red-Black Tree Principles & Invariants",
  "topicName": "Red-Black Trees",
  "sectionId": "trees-and-bst",
  "estimatedMinutes": 35,
  "difficulty": "INTERMEDIATE",
  "prerequisites": [
    106
  ],
  "concepts": [
    "Red/Black Color Invariants",
    "Black-Height Invariant & Recolor Rules"
  ],
  "practiceSkills": [
    "Red-Black Trees Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Trace the 5 Red-Black tree properties guaranteeing maximum height <= 2 log(N+1)",
    "Differentiate recoloring steps from rotation steps during node insertion"
  ],
  "practiceArchetype": "tracing",
  "flowTier": "tier2"
,
  "steps": [
    {
        "id": "day107-step1",
        "stepNumber": 1,
        "title": "Red-Black Tree Principles & Invariants: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Red-Black Trees",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Red-Black Trees.",
        "markdownContent": [
            "Red-Black Trees maintain approximate balance through local node coloring invariants, guaranteeing worst-case O(log N) operations with fewer tree rotations on updates than AVL trees.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Red-Black Trees**, remember the central principle: Equal black-height across all paths bounds the maximum path length to at most twice the minimum path length."
        ],
        "snippets": [
            {
                "title": "Red-Black Trees Implementation Template",
                "code": "# Red-Black Tree Invariants Verification\ndef verify_black_height(node):\n    if not node: return 0\n    left_bh = verify_black_height(node.left)\n    right_bh = verify_black_height(node.right)\n    if left_bh != right_bh: raise ValueError('Black height mismatch!')\n    return left_bh + (1 if node.color == 'BLACK' else 0)",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Equal black-height across all paths bounds the maximum path length to at most twice the minimum path length."
    },
    {
        "id": "day107-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Red-Black Trees",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "The 5 Red-Black Invariants: (1) Every node is RED or BLACK. (2) The root is always BLACK. (3) Every leaf (None) is BLACK. (4) If a node is RED, both its children are BLACK (no two consecutive red nodes). (5) For each node, all paths from that node to descendant leaves contain the SAME number of black nodes (Black-Height). Tree height is strictly bounded: H <= 2 * log2(N + 1).",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Equal black-height across all paths bounds the maximum path length to at most twice the minimum path length.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Red-Black Trees Core Invariant",
                "content": "Equal black-height across all paths bounds the maximum path length to at most twice the minimum path length."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Equal black-height across all paths bounds the maximum path length to at most twice the minimum path length."
    },
    {
        "id": "day107-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Red-Black Trees",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d107-q1",
                "question": "Why does the invariant 'no two consecutive red nodes' combined with 'equal black-height' guarantee balanced O(log N) search time?",
                "options": [
                    {
                        "id": "A",
                        "label": "The shortest possible path consists entirely of black nodes (length BH), while the longest possible path alternates red and black (length 2 * BH), bounding maximum depth to at most 2 * log2(N + 1)"
                    },
                    {
                        "id": "B",
                        "label": "Because red nodes are deleted after insertion"
                    },
                    {
                        "id": "C",
                        "label": "Because black nodes do not count towards tree height"
                    },
                    {
                        "id": "D",
                        "label": "Because red-black trees are perfectly symmetric complete trees"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Since red nodes cannot have red children, you can never have two red nodes in a row. The longest path can at most double the shortest path length (2 * BH). Hence height is strictly bounded within 2 * log2(N + 1) = O(log N).",
                    "B": "Incorrect: Nodes remain in the tree with their assigned colors.",
                    "C": "Incorrect: All nodes contribute to operational depth.",
                    "D": "Incorrect: Red-black trees are approximately balanced, not complete trees."
                }
            },
            {
                "id": "chk-d107-q2",
                "question": "Why do production systems (like Java's TreeMap and C++'s std::map) prefer Red-Black Trees over AVL Trees for general-purpose associative containers?",
                "options": [
                    {
                        "id": "A",
                        "label": "Red-Black trees require at most 2 rotations per insertion and at most 3 rotations per deletion, resulting in faster write/update throughput than more rigidly balanced AVL trees"
                    },
                    {
                        "id": "B",
                        "label": "Because AVL trees cannot store integers"
                    },
                    {
                        "id": "C",
                        "label": "Because Red-Black trees use 0 memory"
                    },
                    {
                        "id": "D",
                        "label": "Because Red-Black trees are faster at lookups than AVL trees"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! AVL trees are more rigidly balanced, which makes lookups slightly faster, but frequent updates trigger cascade rotations up to O(log N). Red-Black trees bound rotations to O(1) constant rotations per mutation.",
                    "B": "Incorrect: AVL trees store all comparable keys.",
                    "C": "Incorrect: Node color requires at least 1 bit.",
                    "D": "Incorrect: AVL trees have strictly shallower height, making pure lookups marginally faster."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day107-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Red-Black Trees",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Implement Black-Height Verification to validate whether a colored binary tree satisfies the Red-Black Black-Height invariant.",
        "subheading": "Implement and verify Red-Black Trees in the interactive workspace.",
        "task": {
            "title": "Implement Black-Height Verification to validate whether a colored binary tree satisfies the Red-Black Black-Height invariant.",
            "instructions": [
                "Implement Black-Height Verification to validate whether a colored binary tree satisfies the Red-Black Black-Height invariant.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "class RBNode:\n    def __init__(self, val, color='BLACK', left=None, right=None):\n        self.val = val\n        self.color = color  # 'RED' or 'BLACK'\n        self.left = left\n        self.right = right\n\ndef is_valid_black_height(root: RBNode) -> bool:\n    # TODO: Return True if all root-to-leaf paths have identical count of BLACK nodes\n    return False\n\n# Root(B) -> left: 1(B), right: 3(R -> left: 2(B))\n# Path 1: B -> B = 2 black nodes. Path 2: B -> R -> B = 2 black nodes. Valid!\nvalid_tree = RBNode(2, 'BLACK', RBNode(1, 'BLACK'), RBNode(3, 'RED', RBNode(2.5, 'BLACK')))\nprint('Is valid black height:', is_valid_black_height(valid_tree)) # True\n",
            "solutionCode": "class RBNode:\n    def __init__(self, val, color='BLACK', left=None, right=None):\n        self.val = val\n        self.color = color\n        self.left = left\n        self.right = right\n\ndef is_valid_black_height(root: RBNode) -> bool:\n    def check(node):\n        if not node:\n            return 1 # Null leaves are black\n        lb = check(node.left)\n        rb = check(node.right)\n        if lb == -1 or rb == -1 or lb != rb:\n            return -1\n        return lb + (1 if node.color == 'BLACK' else 0)\n    return check(root) != -1\n\nvalid_tree = RBNode(2, 'BLACK', RBNode(1, 'BLACK'), RBNode(3, 'RED', RBNode(2.5, 'BLACK')))\nprint('Is valid black height:', is_valid_black_height(valid_tree))\n",
            "expectedOutputPatterns": [
                "Is valid black height: True"
            ],
            "hint": "Helper check(node) returns black-height or -1 if mismatch. If not node return 1. If check(left) != check(right) return -1. Add 1 if node.color == 'BLACK'."
        },
        "keyTakeaway": "Successfully implemented and verified Red-Black Trees!"
    },
    {
        "id": "day107-step5",
        "stepNumber": 5,
        "title": "Day 107 Complete: Red-Black Tree Principles & Invariants",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 107,
        "heading": "Mastery Achieved: Red-Black Tree Principles & Invariants",
        "subheading": "You have solidified key mental models and techniques for Red-Black Trees.",
        "recapRows": [
            {
                "concept": "Black-Height Balance Invariant",
                "naiveIntuition": "Trees must be strictly balanced at every single node",
                "pythonReality": "Equalizing black-height bounds depth to within a 2x factor, delivering logarithmic guarantees with minimal rotation overhead"
            },
            {
                "concept": "Mutation Rotation Bound",
                "naiveIntuition": "Balancing always requires rotating the entire tree",
                "pythonReality": "Red-Black re-coloring absorbs most updates; at most 2 or 3 rotations are ever needed per insert/delete"
            }
        ],
        "solidifiedConcepts": [
            "Red/Black Color Invariants",
            "Black-Height Invariant & Recolor Rules"
        ],
        "nextDayPreview": {
            "dayNumber": 108,
            "title": "Tries (Prefix Trees): Structure & Lookup",
            "description": "Build a Trie (Prefix Tree) data structure supporting O(L) word insertion, full-word search, and prefix matching."
        }
    }
]
},
  108: {
  "dayNumber": 108,
  "title": "Tries (Prefix Trees): Structure & Lookup",
  "topicName": "Trie Architecture",
  "sectionId": "trees-and-bst",
  "estimatedMinutes": 35,
  "difficulty": "INTERMEDIATE",
  "prerequisites": [
    15,
    96
  ],
  "concepts": [
    "26-Child Alphabet TrieNode",
    "is_end Word Termination Flag"
  ],
  "practiceSkills": [
    "Trie Architecture Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Implement a prefix Trie with insert, search, and startsWith methods in O(L) time",
    "Contrast Trie string prefix search with hash map string lookups"
  ],
  "practiceArchetype": "algorithm",
  "flowTier": "tier2"
,
  "steps": [
    {
        "id": "day108-step1",
        "stepNumber": 1,
        "title": "Tries (Prefix Trees): Structure & Lookup: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Trie Architecture",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Trie Architecture.",
        "markdownContent": [
            "Tries (Prefix Trees) organize strings character-by-character where common prefixes share common ancestor nodes, enabling O(L) search, prefix matching, and insertion independent of dictionary size N.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Trie Architecture**, remember the central principle: Tries achieve O(L) prefix search proportional solely to word length L, bypassing expensive scans across N dictionary entries."
        ],
        "snippets": [
            {
                "title": "Trie Architecture Implementation Template",
                "code": "# Trie Prefix Tree\nclass TrieNode:\n    def __init__(self):\n        self.children = {}\n        self.is_end = False\n\nclass Trie:\n    def __init__(self):\n        self.root = TrieNode()\n    def insert(self, word):\n        curr = self.root\n        for ch in word:\n            curr = curr.children.setdefault(ch, TrieNode())\n        curr.is_end = True\n    def search(self, word):\n        curr = self.root\n        for ch in word:\n            if ch not in curr.children: return False\n            curr = curr.children[ch]\n        return curr.is_end",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Tries achieve O(L) prefix search proportional solely to word length L, bypassing expensive scans across N dictionary entries."
    },
    {
        "id": "day108-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Trie Architecture",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Each TrieNode contains `children = {}` (mapping char to child node) and boolean `is_end = False`. Insertion walks down the character path, creating nodes as needed. Lookup verifies the path exists. Prefix queries check path existence without requiring `is_end`.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Tries achieve O(L) prefix search proportional solely to word length L, bypassing expensive scans across N dictionary entries.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Trie Architecture Core Invariant",
                "content": "Tries achieve O(L) prefix search proportional solely to word length L, bypassing expensive scans across N dictionary entries."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Tries achieve O(L) prefix search proportional solely to word length L, bypassing expensive scans across N dictionary entries."
    },
    {
        "id": "day108-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Trie Architecture",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d108-q1",
                "question": "Why is Trie search time complexity O(L) where L is query length, rather than depending on the number of stored words N?",
                "options": [
                    {
                        "id": "A",
                        "label": "Each character lookup follows a direct dictionary pointer in O(1) time down a tree branch of depth L, never inspecting unrelated branches"
                    },
                    {
                        "id": "B",
                        "label": "Because the Trie sorts all words in memory"
                    },
                    {
                        "id": "C",
                        "label": "Because N is always smaller than L"
                    },
                    {
                        "id": "D",
                        "label": "Because Tries use binary search on strings"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Whether the Trie stores 10 words or 10,000,000 words, searching for a 4-letter prefix like 'code' performs exactly 4 child lookups down the matching branch, taking strictly O(L) time.",
                    "B": "Incorrect: Tries do not require array sorting.",
                    "C": "Incorrect: Word count N is typically much larger than word length L.",
                    "D": "Incorrect: Tries use hash/array indexing at each node, not binary search."
                }
            },
            {
                "id": "chk-d108-q2",
                "question": "What distinguishes `search(word)` from `starts_with(prefix)` in a Trie?",
                "options": [
                    {
                        "id": "A",
                        "label": "search(word) requires `curr.is_end == True` at the final node, while starts_with(prefix) only requires the character path to exist"
                    },
                    {
                        "id": "B",
                        "label": "starts_with is O(N) while search is O(1)"
                    },
                    {
                        "id": "C",
                        "label": "search checks suffixes instead of prefixes"
                    },
                    {
                        "id": "D",
                        "label": "There is no difference"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! If 'apple' is inserted, 'app' is a valid prefix (`starts_with('app') == True`), but not a complete word (`search('app') == False`) until explicitly marked `is_end = True`.",
                    "B": "Incorrect: Both operations run in O(L) time.",
                    "C": "Incorrect: Both traverse from prefix root downward.",
                    "D": "Incorrect: The `is_end` check differentiates words from intermediate prefixes."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day108-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Trie Architecture",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Implement a complete Trie supporting insert, search, and starts_with.",
        "subheading": "Implement and verify Trie Architecture in the interactive workspace.",
        "task": {
            "title": "Implement a complete Trie supporting insert, search, and starts_with.",
            "instructions": [
                "Implement a complete Trie supporting insert, search, and starts_with.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "class TrieNode:\n    def __init__(self):\n        self.children = {}\n        self.is_end = False\n\nclass Trie:\n    def __init__(self):\n        self.root = TrieNode()\n\n    # TODO: Implement insert, search, and starts_with\n\nt = Trie()\nt.insert('code')\nprint('Search code:', t.search('code'))       # True\nprint('Search cod:', t.search('cod'))         # False\nprint('Starts with cod:', t.starts_with('cod')) # True\n",
            "solutionCode": "class TrieNode:\n    def __init__(self):\n        self.children = {}\n        self.is_end = False\n\nclass Trie:\n    def __init__(self):\n        self.root = TrieNode()\n\n    def insert(self, word: str) -> None:\n        curr = self.root\n        for ch in word:\n            if ch not in curr.children:\n                curr.children[ch] = TrieNode()\n            curr = curr.children[ch]\n        curr.is_end = True\n\n    def search(self, word: str) -> bool:\n        curr = self.root\n        for ch in word:\n            if ch not in curr.children:\n                return False\n            curr = curr.children[ch]\n        return curr.is_end\n\n    def starts_with(self, prefix: str) -> bool:\n        curr = self.root\n        for ch in prefix:\n            if ch not in curr.children:\n                return False\n            curr = curr.children[ch]\n        return True\n\nt = Trie()\nt.insert('code')\nprint('Search code:', t.search('code'))\nprint('Search cod:', t.search('cod'))\nprint('Starts with cod:', t.starts_with('cod'))\n",
            "expectedOutputPatterns": [
                "Search code: True",
                "Search cod: False",
                "Starts with cod: True"
            ],
            "hint": "In insert: loop ch, setdefault TrieNode(), set is_end = True. In search: verify path exists and return curr.is_end. In starts_with: verify path exists and return True."
        },
        "keyTakeaway": "Successfully implemented and verified Trie Architecture!"
    },
    {
        "id": "day108-step5",
        "stepNumber": 5,
        "title": "Day 108 Complete: Tries (Prefix Trees): Structure & Lookup",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 108,
        "heading": "Mastery Achieved: Tries (Prefix Trees): Structure & Lookup",
        "subheading": "You have solidified key mental models and techniques for Trie Architecture.",
        "recapRows": [
            {
                "concept": "Prefix Consolidation",
                "naiveIntuition": "Store words in an array and use string.startswith()",
                "pythonReality": "Tries consolidate overlapping prefixes into shared tree nodes, collapsing redundant scans into O(L) lookups"
            },
            {
                "concept": "Word Boundary Disambiguation",
                "naiveIntuition": "Reaching a node means the word exists",
                "pythonReality": "Only nodes with is_end == True denote complete stored words; intermediate nodes represent valid prefixes"
            }
        ],
        "solidifiedConcepts": [
            "26-Child Alphabet TrieNode",
            "is_end Word Termination Flag"
        ],
        "nextDayPreview": {
            "dayNumber": 109,
            "title": "Trie Applications: Autocomplete & Wildcards",
            "description": "Apply Tries to autocomplete dictionary queries and wildcard pattern searches using recursive backtracking."
        }
    }
]
},
  109: {
  "dayNumber": 109,
  "title": "Trie Applications: Autocomplete & Wildcards",
  "topicName": "Trie Applications",
  "sectionId": "trees-and-bst",
  "estimatedMinutes": 40,
  "difficulty": "INTERMEDIATE",
  "prerequisites": [
    108
  ],
  "concepts": [
    "DFS Prefix Subtree Collection",
    "Wildcard '.' Branching Traversal"
  ],
  "practiceSkills": [
    "Trie Applications Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Implement an autocomplete search engine returning all words sharing a common prefix",
    "Traverse all child branches upon encountering wildcard '.' characters"
  ],
  "practiceArchetype": "problem",
  "flowTier": "tier3"
,
  "steps": [
    {
        "id": "day109-step1",
        "stepNumber": 1,
        "title": "Trie Applications: Autocomplete & Wildcards: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Trie Applications",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Trie Applications.",
        "markdownContent": [
            "Trie Applications extend basic prefix matching to support Autocomplete suggestions and Wildcard Pattern Search (matching '.' to any character) via DFS branching.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Trie Applications**, remember the central principle: Wildcard character '.' transforms linear Trie descent into multi-branch DFS, exploring all valid phonetic avenues."
        ],
        "snippets": [
            {
                "title": "Trie Applications Implementation Template",
                "code": "# WordDictionary with '.' Wildcards\ndef search_wildcard(node, word, idx):\n    if idx == len(word): return node.is_end\n    ch = word[idx]\n    if ch == '.':\n        return any(search_wildcard(child, word, idx + 1) for child in node.children.values())\n    if ch in node.children:\n        return search_wildcard(node.children[ch], word, idx + 1)\n    return False",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Wildcard character '.' transforms linear Trie descent into multi-branch DFS, exploring all valid phonetic avenues."
    },
    {
        "id": "day109-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Trie Applications",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Wildcard Search: for literal characters, follow `curr.children[ch]`. For wildcard `'.'`: recurse across ALL available child branches in `curr.children.values()`. If any branch matches the remaining pattern, return True. Autocomplete: descend to the prefix node, then launch a DFS to collect all descendant words.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Wildcard character '.' transforms linear Trie descent into multi-branch DFS, exploring all valid phonetic avenues.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Trie Applications Core Invariant",
                "content": "Wildcard character '.' transforms linear Trie descent into multi-branch DFS, exploring all valid phonetic avenues."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Wildcard character '.' transforms linear Trie descent into multi-branch DFS, exploring all valid phonetic avenues."
    },
    {
        "id": "day109-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Trie Applications",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d109-q1",
                "question": "What is the worst-case time complexity of searching a pattern consisting entirely of wildcards '...' in a Trie with branching factor 26?",
                "options": [
                    {
                        "id": "A",
                        "label": "O(26^L) where L is pattern length, exploring every branch in the tree"
                    },
                    {
                        "id": "B",
                        "label": "O(L) linear time"
                    },
                    {
                        "id": "C",
                        "label": "O(N * L) space"
                    },
                    {
                        "id": "D",
                        "label": "O(1) constant time"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! With all wildcards, the search cannot prune any character branches, forcing DFS to explore all available child branches down to depth L. For 26 letters, worst case is O(26^L).",
                    "B": "Incorrect: That applies to literal queries without wildcards.",
                    "C": "Incorrect: Time complexity is exponential.",
                    "D": "Incorrect: Must traverse tree branches."
                }
            },
            {
                "id": "chk-d109-q2",
                "question": "In an Autocomplete system, what is the first step before collecting word suggestions?",
                "options": [
                    {
                        "id": "A",
                        "label": "Descend down the Trie along the prefix characters; if the prefix path exists, the target node is the root of the suggestion subtree"
                    },
                    {
                        "id": "B",
                        "label": "Sort all words in the dictionary alphabetically"
                    },
                    {
                        "id": "C",
                        "label": "Delete words with different lengths"
                    },
                    {
                        "id": "D",
                        "label": "Convert all words to lowercase integers"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Finding the prefix node in O(L) isolates the exact subtree containing all words beginning with that prefix. Subtree DFS then collects candidate completions.",
                    "B": "Incorrect: The Trie structure already enforces prefix clustering.",
                    "C": "Incorrect: Autocomplete words have variable lengths.",
                    "D": "Incorrect: Trie processes string characters directly."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day109-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Trie Applications",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Build a WordDictionary supporting '.' wildcards matching any single letter.",
        "subheading": "Implement and verify Trie Applications in the interactive workspace.",
        "task": {
            "title": "Build a WordDictionary supporting '.' wildcards matching any single letter.",
            "instructions": [
                "Build a WordDictionary supporting '.' wildcards matching any single letter.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "class TrieNode:\n    def __init__(self):\n        self.children = {}\n        self.is_end = False\n\nclass WordDictionary:\n    def __init__(self):\n        self.root = TrieNode()\n\n    def add_word(self, word: str) -> None:\n        # TODO: Insert word into Trie\n        pass\n\n    def search(self, word: str) -> bool:\n        # TODO: Search word where '.' matches any character\n        return False\n\nwd = WordDictionary()\nwd.add_word('bad')\nwd.add_word('dad')\nwd.add_word('mad')\nprint('Search pad:', wd.search('pad')) # False\nprint('Search bad:', wd.search('bad')) # True\nprint('Search .ad:', wd.search('.ad')) # True\nprint('Search b..:', wd.search('b..')) # True\n",
            "solutionCode": "class TrieNode:\n    def __init__(self):\n        self.children = {}\n        self.is_end = False\n\nclass WordDictionary:\n    def __init__(self):\n        self.root = TrieNode()\n\n    def add_word(self, word: str) -> None:\n        curr = self.root\n        for ch in word:\n            if ch not in curr.children:\n                curr.children[ch] = TrieNode()\n            curr = curr.children[ch]\n        curr.is_end = True\n\n    def search(self, word: str) -> bool:\n        def dfs(idx, node):\n            if idx == len(word):\n                return node.is_end\n            ch = word[idx]\n            if ch == '.':\n                for child in node.children.values():\n                    if dfs(idx + 1, child):\n                        return True\n                return False\n            if ch not in node.children:\n                return False\n            return dfs(idx + 1, node.children[ch])\n        return dfs(0, self.root)\n\nwd = WordDictionary()\nwd.add_word('bad')\nwd.add_word('dad')\nwd.add_word('mad')\nprint('Search pad:', wd.search('pad'))\nprint('Search bad:', wd.search('bad'))\nprint('Search .ad:', wd.search('.ad'))\nprint('Search b..:', wd.search('b..'))\n",
            "expectedOutputPatterns": [
                "Search pad: False",
                "Search bad: True",
                "Search .ad: True",
                "Search b..: True"
            ],
            "hint": "In search: helper dfs(idx, node). If idx == len(word) return node.is_end. If ch == '.': for child in node.children.values(): if dfs(idx+1, child) return True; return False. Else if ch in node.children return dfs(idx+1, node.children[ch])."
        },
        "keyTakeaway": "Successfully implemented and verified Trie Applications!"
    },
    {
        "id": "day109-step5",
        "stepNumber": 5,
        "title": "Day 109 Complete: Trie Applications: Autocomplete & Wildcards",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 109,
        "heading": "Mastery Achieved: Trie Applications: Autocomplete & Wildcards",
        "subheading": "You have solidified key mental models and techniques for Trie Applications.",
        "recapRows": [
            {
                "concept": "Multi-Branch Pruning",
                "naiveIntuition": "Wildcards require regex searches across all words",
                "pythonReality": "Trie-guided DFS branches only on existing letters at each step, pruning dead branches immediately"
            },
            {
                "concept": "Subtree Scoping",
                "naiveIntuition": "Autocomplete checks every word in dictionary",
                "pythonReality": "Walking the prefix path scopes the search to exactly the descendant subtree, ignoring 99% of unrelated words"
            }
        ],
        "solidifiedConcepts": [
            "DFS Prefix Subtree Collection",
            "Wildcard '.' Branching Traversal"
        ],
        "nextDayPreview": {
            "dayNumber": 110,
            "title": "Section 9 Review & Tree Recursion Mastery",
            "description": "Synthesize binary tree recursions, BST search invariants, self-balancing rotations, and prefix Trie indexing."
        }
    }
]
},
  110: {
  "dayNumber": 110,
  "title": "Section 9 Review & Tree Recursion Mastery",
  "topicName": "Trees Milestone",
  "sectionId": "trees-and-bst",
  "estimatedMinutes": 45,
  "difficulty": "INTERMEDIATE",
  "prerequisites": [
    100,
    102,
    103,
    104,
    105,
    108
  ],
  "concepts": [
    "Recursive Tree Decomposition",
    "BST Balancing Trade-offs",
    "Trie Indexing Integration"
  ],
  "practiceSkills": [
    "Trees Milestone Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Architect an in-memory search catalog combining a Trie with a balanced BST",
    "Evaluate asymptotic worst-case bounds on degenerate vs balanced trees"
  ],
  "practiceArchetype": "milestone",
  "flowTier": "tier3"
,
  "steps": [
    {
        "id": "day110-step1",
        "stepNumber": 1,
        "title": "Section 9 Review & Tree Recursion Mastery: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Trees Milestone",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Trees Milestone.",
        "markdownContent": [
            "Section 9 Review synthesizes binary tree traversals, level-order BFS, bottom-up DFS recursion, BST invariants, Morris traversal, and self-balancing rotations.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Trees Milestone**, remember the central principle: Tree algorithms are mastered by matching tree topology invariants to recursion and queue patterns."
        ],
        "snippets": [
            {
                "title": "Trees Milestone Implementation Template",
                "code": "# Tree Problem Solving Taxonomy:\n# 1. Top-Down: pass arguments downward (Path Sum, Validate BST Range)\n# 2. Bottom-Up: combine child returns upward (Height, Diameter, LCA)\n# 3. Breadth-First: level-by-level queue (Level-Order, Zigzag)\n# 4. In-Order: BST monotonicity (Sorted recovery, K-th smallest)",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Tree algorithms are mastered by matching tree topology invariants to recursion and queue patterns."
    },
    {
        "id": "day110-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Trees Milestone",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Master tree problem classification: (1) Level by level / shortest path? Use BFS with deque. (2) Subtree aggregation / height / diameter? Use post-order bottom-up DFS. (3) Range bounds / sorted values? Use BST in-order properties. (4) Zero memory constraints? Use Morris traversal.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Tree algorithms are mastered by matching tree topology invariants to recursion and queue patterns.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Trees Milestone Core Invariant",
                "content": "Tree algorithms are mastered by matching tree topology invariants to recursion and queue patterns."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Tree algorithms are mastered by matching tree topology invariants to recursion and queue patterns."
    },
    {
        "id": "day110-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Trees Milestone",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d110-q1",
                "question": "Which traversal strategy should be selected when asked to find the minimum depth to a leaf node in a huge binary tree with millions of nodes?",
                "options": [
                    {
                        "id": "A",
                        "label": "BFS level-order traversal, because it terminates the moment the very first leaf node is encountered at the shallowest depth"
                    },
                    {
                        "id": "B",
                        "label": "DFS post-order traversal"
                    },
                    {
                        "id": "C",
                        "label": "In-order traversal"
                    },
                    {
                        "id": "D",
                        "label": "Morris traversal"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! BFS searches level by level. The moment it pops a node with `not node.left and not node.right`, that depth is guaranteed to be minimal. It terminates without exploring deeper massive subtrees.",
                    "B": "Incorrect: DFS might plunge down a million-node deep subtree before checking shallow leaves on other branches.",
                    "C": "Incorrect: In-order does not correlate with leaf depth.",
                    "D": "Incorrect: Morris visits all nodes."
                }
            },
            {
                "id": "chk-d110-q2",
                "question": "What is the primary operational trade-off of maintaining an AVL balanced tree compared to a naive BST?",
                "options": [
                    {
                        "id": "A",
                        "label": "AVL guarantees O(log N) worst-case search and insert times at the cost of rebalancing rotation overhead on insertions and deletions"
                    },
                    {
                        "id": "B",
                        "label": "AVL trees cannot store negative numbers"
                    },
                    {
                        "id": "C",
                        "label": "Naive BST is faster on worst-case data"
                    },
                    {
                        "id": "D",
                        "label": "AVL trees consume O(N^2) memory"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! AVL trees eliminate the O(N) degraded list scenario by rebalancing in O(1) rotations, ensuring strict O(log N) worst-case operation times.",
                    "B": "Incorrect: All numbers are supported.",
                    "C": "Incorrect: Naive BST degrades to O(N) on sorted inputs.",
                    "D": "Incorrect: Space is strictly O(N)."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day110-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Trees Milestone",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Find the K-th smallest element in a Binary Search Tree.",
        "subheading": "Implement and verify Trees Milestone in the interactive workspace.",
        "task": {
            "title": "Find the K-th smallest element in a Binary Search Tree.",
            "instructions": [
                "Find the K-th smallest element in a Binary Search Tree.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef kth_smallest(root: TreeNode, k: int) -> int:\n    # TODO: Exploit BST in-order sorted traversal to find k-th smallest (1-indexed)\n    return -1\n\n# BST: 3 -> left: 1 (right: 2), right: 4. k=1 is 1; k=3 is 3\nt = TreeNode(3, TreeNode(1, None, TreeNode(2)), TreeNode(4))\nprint('1st smallest:', kth_smallest(t, 1))\nprint('3rd smallest:', kth_smallest(t, 3))\n",
            "solutionCode": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef kth_smallest(root: TreeNode, k: int) -> int:\n    stack = []\n    curr = root\n    while curr or stack:\n        while curr:\n            stack.append(curr)\n            curr = curr.left\n        curr = stack.pop()\n        k -= 1\n        if k == 0:\n            return curr.val\n        curr = curr.right\n    return -1\n\nt = TreeNode(3, TreeNode(1, None, TreeNode(2)), TreeNode(4))\nprint('1st smallest:', kth_smallest(t, 1))\nprint('3rd smallest:', kth_smallest(t, 3))\n",
            "expectedOutputPatterns": [
                "1st smallest: 1",
                "3rd smallest: 3"
            ],
            "hint": "Iterative in-order using stack: while curr or stack: while curr: stack.append(curr); curr = curr.left. curr = stack.pop(); k -= 1; if k == 0 return curr.val; curr = curr.right."
        },
        "keyTakeaway": "Successfully implemented and verified Trees Milestone!"
    },
    {
        "id": "day110-step5",
        "stepNumber": 5,
        "title": "Day 110 Complete: Section 9 Review & Tree Recursion Mastery",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 110,
        "heading": "Mastery Achieved: Section 9 Review & Tree Recursion Mastery",
        "subheading": "You have solidified key mental models and techniques for Trees Milestone.",
        "recapRows": [
            {
                "concept": "In-Order Early Stopping",
                "naiveIntuition": "Extract all N nodes into an array, then return array[k-1]",
                "pythonReality": "Stopping the in-order traversal at step k finds the answer in O(H + K) time without traversing the remainder of the tree"
            },
            {
                "concept": "Section 9 Synthesis",
                "naiveIntuition": "Tree algorithms are unrelated formulas",
                "pythonReality": "All tree algorithms flow from three foundational paradigms: Level-Order Queue (BFS), Depth-First Recurrence (DFS), and In-Order Monotonicity (BST)"
            }
        ],
        "solidifiedConcepts": [
            "Recursive Tree Decomposition",
            "BST Balancing Trade-offs",
            "Trie Indexing Integration"
        ],
        "nextDayPreview": {
            "dayNumber": 111,
            "title": "Binary Heap Layout in Flat Arrays",
            "description": "Examine binary heap flat-array indexing (parent = (i-1)//2, left = 2i+1, right = 2i+2) and complete tree layouts."
        }
    }
]
},
  111: {
  "dayNumber": 111,
  "title": "Binary Heap Layout in Flat Arrays",
  "topicName": "Heap Array Layout",
  "sectionId": "heaps-and-priority-queues",
  "estimatedMinutes": 30,
  "difficulty": "INTERMEDIATE",
  "prerequisites": [
    36,
    96
  ],
  "concepts": [
    "Complete Binary Tree Property",
    "0-Indexed Parent/Child Formulas"
  ],
  "practiceSkills": [
    "Heap Array Layout Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Map a complete binary tree into a 1D flat array using parent=(i-1)//2 and children=2i+1, 2i+2",
    "Verify the binary min-heap property: parent <= children"
  ],
  "practiceArchetype": "tracing",
  "flowTier": "tier1"
,
  "steps": [
    {
        "id": "day111-step1",
        "stepNumber": 1,
        "title": "Binary Heap Layout in Flat Arrays: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Heap Array Layout",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Heap Array Layout.",
        "markdownContent": [
            "Binary Heaps map a complete binary tree into a 1D flat array with zero pointer overhead, guaranteeing parent-child relationship indexing via simple arithmetic.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Heap Array Layout**, remember the central principle: Flat arrays store complete binary trees with zero pointer overhead using arithmetic index formulas."
        ],
        "snippets": [
            {
                "title": "Heap Array Layout Implementation Template",
                "code": "# 1D Array indexing for Binary Heap\n# parent(i) = (i - 1) // 2\n# left(i)   = 2 * i + 1\n# right(i)  = 2 * i + 2\nheap = [10, 20, 30, 40, 50, 60, 70]\n# Element 20 is at idx 1: left child is idx 3 (40), right child is idx 4 (50)",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Flat arrays store complete binary trees with zero pointer overhead using arithmetic index formulas."
    },
    {
        "id": "day111-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Heap Array Layout",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "For 0-indexed array: `parent(i) = (i - 1) // 2`, `left(i) = 2 * i + 1`, `right(i) = 2 * i + 2`. Min-Heap property: `arr[parent] <= arr[child]`. Max-Heap property: `arr[parent] >= arr[child]`. Being a complete tree ensures array compact density without empty holes.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Flat arrays store complete binary trees with zero pointer overhead using arithmetic index formulas.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Heap Array Layout Core Invariant",
                "content": "Flat arrays store complete binary trees with zero pointer overhead using arithmetic index formulas."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Flat arrays store complete binary trees with zero pointer overhead using arithmetic index formulas."
    },
    {
        "id": "day111-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Heap Array Layout",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d111-q1",
                "question": "In a 0-indexed flat array representing a binary heap, what is the parent index formula for node `i`?",
                "options": [
                    {
                        "id": "A",
                        "label": "`(i - 1) // 2`"
                    },
                    {
                        "id": "B",
                        "label": "`i // 2`"
                    },
                    {
                        "id": "C",
                        "label": "`2 * i`"
                    },
                    {
                        "id": "D",
                        "label": "`i - 2`"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! For node 1 (left child of 0): (1 - 1) // 2 = 0. For node 2 (right child of 0): (2 - 1) // 2 = 0. For node 3 (left child of 1): (3 - 1) // 2 = 1. Integer division handles both left and right uniformly.",
                    "B": "Incorrect: That is for 1-indexed heaps.",
                    "C": "Incorrect: 2*i computes a child index in 1-indexed trees.",
                    "D": "Incorrect: Indexing requires division by 2."
                }
            },
            {
                "id": "chk-d111-q2",
                "question": "Why does a binary heap require the tree to be a 'Complete Binary Tree'?",
                "options": [
                    {
                        "id": "A",
                        "label": "To guarantee that the flat array has no gaps or empty elements between index 0 and index N - 1"
                    },
                    {
                        "id": "B",
                        "label": "Because incomplete trees cannot be sorted"
                    },
                    {
                        "id": "C",
                        "label": "To prevent node values from being negative"
                    },
                    {
                        "id": "D",
                        "label": "Python arrays reject sparse indices"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! A complete binary tree is completely filled on all levels except possibly the lowest, which is filled from left to right. This guarantees all N nodes occupy indices `0` to `N-1` contiguously.",
                    "B": "Incorrect: Sorting does not require complete trees.",
                    "C": "Incorrect: Node values are independent of tree topology.",
                    "D": "Incorrect: Python lists could store None, but gaps waste memory."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day111-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Heap Array Layout",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Compute the parent, left child, and right child values for a given index in a flat heap array.",
        "subheading": "Implement and verify Heap Array Layout in the interactive workspace.",
        "task": {
            "title": "Compute the parent, left child, and right child values for a given index in a flat heap array.",
            "instructions": [
                "Compute the parent, left child, and right child values for a given index in a flat heap array.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "def get_heap_relatives(arr: list[int], i: int) -> dict[str, int]:\n    # TODO: Return parent, left child, and right child values (or None if out of bounds)\n    return {}\n\nheap = [10, 20, 30, 40, 50, 60, 70]\nprint('Relatives of idx 1 (20):', get_heap_relatives(heap, 1))\n",
            "solutionCode": "def get_heap_relatives(arr: list[int], i: int) -> dict[str, int]:\n    n = len(arr)\n    p_idx = (i - 1) // 2 if i > 0 else None\n    l_idx = 2 * i + 1 if 2 * i + 1 < n else None\n    r_idx = 2 * i + 2 if 2 * i + 2 < n else None\n    return {\n        'val': arr[i],\n        'parent': arr[p_idx] if p_idx is not None else None,\n        'left': arr[l_idx] if l_idx is not None else None,\n        'right': arr[r_idx] if r_idx is not None else None,\n    }\n\nheap = [10, 20, 30, 40, 50, 60, 70]\nprint('Relatives of idx 1 (20):', get_heap_relatives(heap, 1))\n",
            "expectedOutputPatterns": [
                "Relatives of idx 1 (20): {'val': 20, 'parent': 10, 'left': 40, 'right': 50}"
            ],
            "hint": "p = (i - 1) // 2 if i > 0 else None. l = 2*i + 1 if 2*i + 1 < n else None. r = 2*i + 2 if 2*i + 2 < n else None."
        },
        "keyTakeaway": "Successfully implemented and verified Heap Array Layout!"
    },
    {
        "id": "day111-step5",
        "stepNumber": 5,
        "title": "Day 111 Complete: Binary Heap Layout in Flat Arrays",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 111,
        "heading": "Mastery Achieved: Binary Heap Layout in Flat Arrays",
        "subheading": "You have solidified key mental models and techniques for Heap Array Layout.",
        "recapRows": [
            {
                "concept": "Pointerless Topology",
                "naiveIntuition": "Trees must use left and right pointer objects",
                "pythonReality": "Complete binary trees map directly onto contiguous arrays where pointer links are replaced by instant arithmetic"
            },
            {
                "concept": "Cache Locality",
                "naiveIntuition": "Heap performance is identical to pointer trees",
                "pythonReality": "Flat arrays maximize CPU L1/L2 cache hit rates compared to pointer-chasing across fragmented heap memory"
            }
        ],
        "solidifiedConcepts": [
            "Complete Binary Tree Property",
            "0-Indexed Parent/Child Formulas"
        ],
        "nextDayPreview": {
            "dayNumber": 112,
            "title": "Heapify, Sift-Up & Sift-Down Mechanics",
            "description": "Implement sift-up and sift-down operations, and prove that bottom-up heapify runs in linear O(N) time."
        }
    }
]
},
  112: {
  "dayNumber": 112,
  "title": "Heapify, Sift-Up & Sift-Down Mechanics",
  "topicName": "Heap Mechanics",
  "sectionId": "heaps-and-priority-queues",
  "estimatedMinutes": 45,
  "difficulty": "INTERMEDIATE",
  "prerequisites": [
    111
  ],
  "concepts": [
    "Sift-Up (Bubble-Up) & Sift-Down",
    "Linear O(N) Bottom-Up Heapify"
  ],
  "practiceSkills": [
    "Heap Mechanics Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Implement sift-up and sift-down mechanics to restore heap invariants in O(log N) time",
    "Prove mathematically that bottom-up heapify builds a heap in linear O(N) time"
  ],
  "practiceArchetype": "algorithm",
  "flowTier": "tier3"
,
  "steps": [
    {
        "id": "day112-step1",
        "stepNumber": 1,
        "title": "Heapify, Sift-Up & Sift-Down Mechanics: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Heap Mechanics",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Heap Mechanics.",
        "markdownContent": [
            "Sift-Up and Sift-Down maintain the heap invariant, while Bottom-Up Heapify transforms an arbitrary N-element array into a valid heap in linear O(N) time.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Heap Mechanics**, remember the central principle: Bottom-up heapify runs in linear O(N) time because most nodes reside near the bottom with minimal sift-down distance."
        ],
        "snippets": [
            {
                "title": "Heap Mechanics Implementation Template",
                "code": "# Sift-down operation\ndef sift_down(arr, n, i):\n    smallest = i\n    l = 2 * i + 1\n    r = 2 * i + 2\n    if l < n and arr[l] < arr[smallest]: smallest = l\n    if r < n and arr[r] < arr[smallest]: smallest = r\n    if smallest != i:\n        arr[i], arr[smallest] = arr[smallest], arr[i]\n        sift_down(arr, n, smallest)",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Bottom-up heapify runs in linear O(N) time because most nodes reside near the bottom with minimal sift-down distance."
    },
    {
        "id": "day112-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Heap Mechanics",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Sift-Up: swap with parent while `val < parent`, used on `push()`. Sift-Down: swap with smallest child while `val > child`, used on `pop()`. Heapify runs Sift-Down from index `N//2 - 1` down to 0. Math proof: $\\sum_{h=0}^{\\log N} \\frac{N}{2^{h+1}} O(h) = O(N)$.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Bottom-up heapify runs in linear O(N) time because most nodes reside near the bottom with minimal sift-down distance.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Heap Mechanics Core Invariant",
                "content": "Bottom-up heapify runs in linear O(N) time because most nodes reside near the bottom with minimal sift-down distance."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Bottom-up heapify runs in linear O(N) time because most nodes reside near the bottom with minimal sift-down distance."
    },
    {
        "id": "day112-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Heap Mechanics",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d112-q1",
                "question": "Why is bottom-up `heapify` O(N) time, whereas inserting N elements one-by-one into an initially empty heap is O(N log N)?",
                "options": [
                    {
                        "id": "A",
                        "label": "In bottom-up heapify, the majority of nodes (N/2 leaves) require 0 swaps, and nodes with larger heights are exponentially fewer, summing to O(N)"
                    },
                    {
                        "id": "B",
                        "label": "Because heapify uses binary search"
                    },
                    {
                        "id": "C",
                        "label": "Because Python optimizes heapify in C"
                    },
                    {
                        "id": "D",
                        "label": "Because N/2 is equal to O(N)"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Height 0 has N/2 nodes (0 swaps). Height 1 has N/4 nodes (1 swap max). Height h has N / 2^(h+1) nodes. Summing $(N / 2^{h+1}) \\times h$ forms a converging geometric series equal to $O(N)$. Sequential insertion sifts up N/2 leaves all the way to root (N/2 * log N = O(N log N)).",
                    "B": "Incorrect: Heapify is structural sifting, not binary search.",
                    "C": "Incorrect: The asymptotic difference is mathematical, not implementation-specific.",
                    "D": "Incorrect: The mathematical summation of heights proves O(N)."
                }
            },
            {
                "id": "chk-d112-q2",
                "question": "Why does heapify start iterating backwards from index `N // 2 - 1` rather than index `N - 1`?",
                "options": [
                    {
                        "id": "A",
                        "label": "Indices from `N // 2` to `N - 1` are leaf nodes with no children, so they already satisfy the heap property trivially"
                    },
                    {
                        "id": "B",
                        "label": "Because Python lists cannot be sliced past halfway"
                    },
                    {
                        "id": "C",
                        "label": "To skip odd numbers"
                    },
                    {
                        "id": "D",
                        "label": "Because the second half is automatically sorted"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Any index >= N // 2 has left child index 2*i + 1 >= N, which is out of bounds. Leaves have no children to sift down into, making them valid sub-heaps already.",
                    "B": "Incorrect: Lists can be accessed at any valid index.",
                    "C": "Incorrect: Indices are contiguous.",
                    "D": "Incorrect: Leaves are not sorted."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day112-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Heap Mechanics",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Implement in-place bottom-up min-heapify on an unsorted array.",
        "subheading": "Implement and verify Heap Mechanics in the interactive workspace.",
        "task": {
            "title": "Implement in-place bottom-up min-heapify on an unsorted array.",
            "instructions": [
                "Implement in-place bottom-up min-heapify on an unsorted array.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "def heapify_min(arr: list[int]) -> None:\n    # TODO: Implement in-place bottom-up heapify in O(N) time\n    pass\n\nnums = [9, 4, 7, 1, 6, 2, 5, 3]\nheapify_min(nums)\nprint('Min element at root:', nums[0])\n",
            "solutionCode": "def heapify_min(arr: list[int]) -> None:\n    n = len(arr)\n    def sift_down(i):\n        smallest = i\n        l = 2 * i + 1\n        r = 2 * i + 2\n        if l < n and arr[l] < arr[smallest]:\n            smallest = l\n        if r < n and arr[r] < arr[smallest]:\n            smallest = r\n        if smallest != i:\n            arr[i], arr[smallest] = arr[smallest], arr[i]\n            sift_down(smallest)\n    for i in range(n // 2 - 1, -1, -1):\n        sift_down(i)\n\nnums = [9, 4, 7, 1, 6, 2, 5, 3]\nheapify_min(nums)\nprint('Min element at root:', nums[0])\n",
            "expectedOutputPatterns": [
                "Min element at root: 1"
            ],
            "hint": "Helper sift_down(i): find smallest among i, 2*i+1, 2*i+2. If smallest != i: swap and recurse sift_down(smallest). Run sift_down from n//2 - 1 down to 0."
        },
        "keyTakeaway": "Successfully implemented and verified Heap Mechanics!"
    },
    {
        "id": "day112-step5",
        "stepNumber": 5,
        "title": "Day 112 Complete: Heapify, Sift-Up & Sift-Down Mechanics",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 112,
        "heading": "Mastery Achieved: Heapify, Sift-Up & Sift-Down Mechanics",
        "subheading": "You have solidified key mental models and techniques for Heap Mechanics.",
        "recapRows": [
            {
                "concept": "Convergent Height Summation",
                "naiveIntuition": "Heapify takes O(N log N) because heap operations take O(log N)",
                "pythonReality": "Only the single root node can travel height log N; 50% of nodes travel 0 steps, making the total sum strictly O(N)"
            },
            {
                "concept": "In-Place Construction",
                "naiveIntuition": "Allocate a new heap array to insert elements",
                "pythonReality": "Sifting down in reverse index order reorganizes raw arrays in-place with O(1) auxiliary space"
            }
        ],
        "solidifiedConcepts": [
            "Sift-Up (Bubble-Up) & Sift-Down",
            "Linear O(N) Bottom-Up Heapify"
        ],
        "nextDayPreview": {
            "dayNumber": 113,
            "title": "Python's heapq Module & Tie-Breaker Patterns",
            "description": "Master Python's heapq module, simulate max-heaps via negation, and use counter tie-breakers to prevent comparison crashes."
        }
    }
]
},
  113: {
  "dayNumber": 113,
  "title": "Python's heapq Module & Tie-Breaker Patterns",
  "topicName": "heapq Mechanics",
  "sectionId": "heaps-and-priority-queues",
  "estimatedMinutes": 30,
  "difficulty": "INTERMEDIATE",
  "prerequisites": [
    22,
    112
  ],
  "concepts": [
    "heapq Min-Heap Primitives",
    "Tuple Tie-Breaker Crash Prevention"
  ],
  "practiceSkills": [
    "heapq Mechanics Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Use heapq.heappush, heappop, and heapify to manage priority queues",
    "Prevent tuple comparison crashes on identical priorities using unique counter sequence ids"
  ],
  "practiceArchetype": "completion",
  "flowTier": "tier1"
,
  "steps": [
    {
        "id": "day113-step1",
        "stepNumber": 1,
        "title": "Python's heapq Module & Tie-Breaker Patterns: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: heapq Mechanics",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for heapq Mechanics.",
        "markdownContent": [
            "Python's `heapq` module implements a Min-Heap on standard lists, requiring value negation for Max-Heaps and custom `__lt__` wrapper classes for complex tie-breaking.",
            "### Foundational Mental Model\nWhen approaching problems requiring **heapq Mechanics**, remember the central principle: Python's heapq defaults to min-heaps; negate numbers for max-heaps and use unique tie-breaker tokens in tuples."
        ],
        "snippets": [
            {
                "title": "heapq Mechanics Implementation Template",
                "code": "import heapq\n# Min-heap\nh = [5, 1, 3]\nheapq.heapify(h)\nprint('Min:', heapq.heappop(h)) # 1\n\n# Max-heap via negation\nmax_h = [-5, -1, -3]\nheapq.heapify(max_h)\nprint('Max:', -heapq.heappop(max_h)) # 5",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Python's heapq defaults to min-heaps; negate numbers for max-heaps and use unique tie-breaker tokens in tuples."
    },
    {
        "id": "day113-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: heapq Mechanics",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "`heapq.heapify(lst)` transforms list in O(N). `heapq.heappush(lst, item)` and `heapq.heappop(lst)` run in O(log N). For Max-Heap: push `-x` and pop `-heappop()`. For multi-attribute tuples `(priority, tie_breaker, task)`: Python compares items element by element from index 0.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Python's heapq defaults to min-heaps; negate numbers for max-heaps and use unique tie-breaker tokens in tuples.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "heapq Mechanics Core Invariant",
                "content": "Python's heapq defaults to min-heaps; negate numbers for max-heaps and use unique tie-breaker tokens in tuples."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Python's heapq defaults to min-heaps; negate numbers for max-heaps and use unique tie-breaker tokens in tuples."
    },
    {
        "id": "day113-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: heapq Mechanics",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d113-q1",
                "question": "When pushing tuples `(priority, data)` into a `heapq`, what happens if two items have identical `priority` and `data` is an unorderable object (like a custom ListNode)?",
                "options": [
                    {
                        "id": "A",
                        "label": "Python raises `TypeError: '<' not supported between instances` because it attempts to break the priority tie by comparing the second tuple element"
                    },
                    {
                        "id": "B",
                        "label": "Python picks one at random"
                    },
                    {
                        "id": "C",
                        "label": "Python uses object memory addresses"
                    },
                    {
                        "id": "D",
                        "label": "Python ignores duplicate priorities"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Python tuple comparison evaluates indices sequentially: `t1[0] < t2[0]`. If equal, it evaluates `t1[1] < t2[1]`. If `data` lacks `__lt__`, comparison crashes with TypeError.",
                    "B": "Incorrect: Python comparison is strictly deterministic.",
                    "C": "Incorrect: In Python 3, arbitrary object comparison via memory address was removed (PEP 207).",
                    "D": "Incorrect: Duplicate priorities trigger tie-breaking."
                }
            },
            {
                "id": "chk-d113-q2",
                "question": "How do you safely prevent tuple comparison crashes when storing unorderable objects in a heap?",
                "options": [
                    {
                        "id": "A",
                        "label": "Insert a unique incrementing integer counter as the second element: `(priority, count, item)`"
                    },
                    {
                        "id": "B",
                        "label": "Convert the custom object to a string"
                    },
                    {
                        "id": "C",
                        "label": "Sort the objects beforehand"
                    },
                    {
                        "id": "D",
                        "label": "Use negative priorities"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Because `count` increments on every insertion, no two tuples ever share the same `count`. The tie is broken at index 1 before Python ever reaches the unorderable `item` at index 2.",
                    "B": "Incorrect: String representation can be slow and fail on identical strings.",
                    "C": "Incorrect: Doesn't solve runtime comparison in heapq.",
                    "D": "Incorrect: Negation doesn't prevent ties."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day113-step4",
        "stepNumber": 4,
        "title": "Guided Practice: heapq Mechanics",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Use heapq with a 3-element tuple (priority, count, task) to implement a Priority Scheduler.",
        "subheading": "Implement and verify heapq Mechanics in the interactive workspace.",
        "task": {
            "title": "Use heapq with a 3-element tuple (priority, count, task) to implement a Priority Scheduler.",
            "instructions": [
                "Use heapq with a 3-element tuple (priority, count, task) to implement a Priority Scheduler.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "import heapq\n\nclass PriorityScheduler:\n    def __init__(self):\n        self.heap = []\n        self.counter = 0\n\n    # TODO: Implement add_task(task, priority) and get_next_task() -> str\n\nsched = PriorityScheduler()\nsched.add_task('backup', 3)\nsched.add_task('critical_patch', 1)\nsched.add_task('email_sync', 2)\nprint('Next:', sched.get_next_task())\nprint('Next:', sched.get_next_task())\n",
            "solutionCode": "import heapq\n\nclass PriorityScheduler:\n    def __init__(self):\n        self.heap = []\n        self.counter = 0\n\n    def add_task(self, task: str, priority: int) -> None:\n        heapq.heappush(self.heap, (priority, self.counter, task))\n        self.counter += 1\n\n    def get_next_task(self) -> str:\n        if not self.heap:\n            return ''\n        p, c, task = heapq.heappop(self.heap)\n        return task\n\nsched = PriorityScheduler()\nsched.add_task('backup', 3)\nsched.add_task('critical_patch', 1)\nsched.add_task('email_sync', 2)\nprint('Next:', sched.get_next_task())\nprint('Next:', sched.get_next_task())\n",
            "expectedOutputPatterns": [
                "Next: critical_patch",
                "Next: email_sync"
            ],
            "hint": "In add_task: heapq.heappush(self.heap, (priority, self.counter, task)); self.counter += 1. In get_next_task: return heapq.heappop(self.heap)[2]."
        },
        "keyTakeaway": "Successfully implemented and verified heapq Mechanics!"
    },
    {
        "id": "day113-step5",
        "stepNumber": 5,
        "title": "Day 113 Complete: Python's heapq Module & Tie-Breaker Patterns",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 113,
        "heading": "Mastery Achieved: Python's heapq Module & Tie-Breaker Patterns",
        "subheading": "You have solidified key mental models and techniques for heapq Mechanics.",
        "recapRows": [
            {
                "concept": "Tuple Tie-Breaker Idiom",
                "naiveIntuition": "Store (priority, task) tuples",
                "pythonReality": "Using (priority, count, task) guarantees FIFO stability among equal priorities and prevents comparison TypeErrors"
            },
            {
                "concept": "Max-Heap Dual Inversion",
                "naiveIntuition": "Python lacks max-heap support",
                "pythonReality": "Negating numbers transforms a min-heap into a max-heap in zero extra lines"
            }
        ],
        "solidifiedConcepts": [
            "heapq Min-Heap Primitives",
            "Tuple Tie-Breaker Crash Prevention"
        ],
        "nextDayPreview": {
            "dayNumber": 114,
            "title": "Top K Frequent Elements in Data Streams",
            "description": "Find the K most frequent items in continuous streams in O(N log K) time using bounded min-heaps."
        }
    }
]
},
  114: {
  "dayNumber": 114,
  "title": "Top K Frequent Elements in Data Streams",
  "topicName": "Top-K Streaming",
  "sectionId": "heaps-and-priority-queues",
  "estimatedMinutes": 35,
  "difficulty": "INTERMEDIATE",
  "prerequisites": [
    68,
    113
  ],
  "concepts": [
    "Bounded Min-Heap of Size K",
    "O(N log K) Extraction"
  ],
  "practiceSkills": [
    "Top-K Streaming Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Maintain a min-heap of size K to identify top K frequent elements in O(N log K) time",
    "Contrast bounded min-heap filtering against full O(N log N) array sorting"
  ],
  "practiceArchetype": "problem",
  "flowTier": "tier2"
,
  "steps": [
    {
        "id": "day114-step1",
        "stepNumber": 1,
        "title": "Top K Frequent Elements in Data Streams: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Top-K Streaming",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Top-K Streaming.",
        "markdownContent": [
            "Top K Frequent Elements combines frequency counting with a min-heap of size K (O(N log K) time) or Bucket Sort by frequency (O(N) time).",
            "### Foundational Mental Model\nWhen approaching problems requiring **Top-K Streaming**, remember the central principle: Frequencies are bounded by N, enabling O(N) bucket sort as an alternative to heaps."
        ],
        "snippets": [
            {
                "title": "Top-K Streaming Implementation Template",
                "code": "# Top K Frequent via Bucket Sort\nfrom collections import Counter\ndef top_k_frequent(nums, k):\n    counts = Counter(nums)\n    buckets = [[] for _ in range(len(nums) + 1)]\n    for num, freq in counts.items(): buckets[freq].append(num)\n    res = []\n    for freq in range(len(buckets) - 1, 0, -1):\n        for num in buckets[freq]:\n            res.append(num)\n            if len(res) == k: return res",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Frequencies are bounded by N, enabling O(N) bucket sort as an alternative to heaps."
    },
    {
        "id": "day114-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Top-K Streaming",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Step 1: count frequencies with `collections.Counter`. Method A (Heap): maintain size-K min-heap of `(freq, num)`. Method B (Bucket Sort): create an array `buckets` where `buckets[freq]` holds numbers with that frequency. Iterate backwards from index N to collect top K in O(N) time.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Frequencies are bounded by N, enabling O(N) bucket sort as an alternative to heaps.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Top-K Streaming Core Invariant",
                "content": "Frequencies are bounded by N, enabling O(N) bucket sort as an alternative to heaps."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Frequencies are bounded by N, enabling O(N) bucket sort as an alternative to heaps."
    },
    {
        "id": "day114-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Top-K Streaming",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d114-q1",
                "question": "Why is Bucket Sort able to achieve O(N) linear time for Top K Frequent Elements?",
                "options": [
                    {
                        "id": "A",
                        "label": "Because the maximum possible frequency of any element is strictly bounded by array length N, allowing bucket indices to represent frequencies directly without comparison sorting"
                    },
                    {
                        "id": "B",
                        "label": "Because all elements in the input array are positive"
                    },
                    {
                        "id": "C",
                        "label": "Because Python dictionaries sort keys automatically"
                    },
                    {
                        "id": "D",
                        "label": "Because K is always equal to 1"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! No number can appear more than N times. Creating N + 1 buckets allows grouping elements by frequency in O(N) time, bypassing the $\\Omega(N \\log N)$ comparison sort barrier.",
                    "B": "Incorrect: Works for any numbers or strings.",
                    "C": "Incorrect: Dicts preserve insertion order, not frequency order.",
                    "D": "Incorrect: K can be any integer up to unique element count."
                }
            },
            {
                "id": "chk-d114-q2",
                "question": "When is the Heap approach preferred over the Bucket Sort approach for top frequent items?",
                "options": [
                    {
                        "id": "A",
                        "label": "When data arrives as an infinite stream or memory cannot accommodate N buckets"
                    },
                    {
                        "id": "B",
                        "label": "When N is less than 5"
                    },
                    {
                        "id": "C",
                        "label": "When all numbers are identical"
                    },
                    {
                        "id": "D",
                        "label": "Never, bucket sort is always superior"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! In streaming systems where total N is unknown or unbounded, creating an array of size N is impossible. A min-heap of size K stores only the active leaders in bounded O(K) space.",
                    "B": "Incorrect: For tiny N, both are trivial.",
                    "C": "Incorrect: Both handle identical elements easily.",
                    "D": "Incorrect: Streaming constraints favor heaps."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day114-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Top-K Streaming",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Find the top K most frequent elements in an array using Bucket Sort.",
        "subheading": "Implement and verify Top-K Streaming in the interactive workspace.",
        "task": {
            "title": "Find the top K most frequent elements in an array using Bucket Sort.",
            "instructions": [
                "Find the top K most frequent elements in an array using Bucket Sort.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "from collections import Counter\n\ndef top_k_frequent(nums: list[int], k: int) -> list[int]:\n    # TODO: Implement bucket sort by frequency to return top k frequent elements in O(N)\n    return []\n\nprint('Top 2:', sorted(top_k_frequent([1, 1, 1, 2, 2, 3], 2)))\n",
            "solutionCode": "from collections import Counter\n\ndef top_k_frequent(nums: list[int], k: int) -> list[int]:\n    counts = Counter(nums)\n    buckets = [[] for _ in range(len(nums) + 1)]\n    for num, freq in counts.items():\n        buckets[freq].append(num)\n    res = []\n    for freq in range(len(buckets) - 1, 0, -1):\n        for num in buckets[freq]:\n            res.append(num)\n            if len(res) == k:\n                return res\n    return res\n\nprint('Top 2:', sorted(top_k_frequent([1, 1, 1, 2, 2, 3], 2)))\n",
            "expectedOutputPatterns": [
                "Top 2: [1, 2]"
            ],
            "hint": "Count with Counter. Create buckets array of size len(nums)+1. Place num into buckets[freq]. Sweep backwards from end of buckets, appending to res until len(res) == k."
        },
        "keyTakeaway": "Successfully implemented and verified Top-K Streaming!"
    },
    {
        "id": "day114-step5",
        "stepNumber": 5,
        "title": "Day 114 Complete: Top K Frequent Elements in Data Streams",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 114,
        "heading": "Mastery Achieved: Top K Frequent Elements in Data Streams",
        "subheading": "You have solidified key mental models and techniques for Top-K Streaming.",
        "recapRows": [
            {
                "concept": "Bounded Domain Exploitation",
                "naiveIntuition": "Sort frequency pairs using comparison sort O(U log U)",
                "pythonReality": "When the domain of sorting keys (frequencies) is bounded by N, bucket sorting achieves linear O(N) time"
            },
            {
                "concept": "Multi-Paradigm Mastery",
                "naiveIntuition": "There is only one optimal algorithm per problem",
                "pythonReality": "Heap approach optimizes streaming space O(K); Bucket sort optimizes batch execution time O(N)"
            }
        ],
        "solidifiedConcepts": [
            "Bounded Min-Heap of Size K",
            "O(N log K) Extraction"
        ],
        "nextDayPreview": {
            "dayNumber": 115,
            "title": "Merge K Sorted Lists via Min-Heap",
            "description": "Merge K sorted lists or streams into a single sorted list in O(N log K) time using priority queue frontiers."
        }
    }
]
},
  115: {
  "dayNumber": 115,
  "title": "Merge K Sorted Lists via Min-Heap",
  "topicName": "K-Way Merging",
  "sectionId": "heaps-and-priority-queues",
  "estimatedMinutes": 40,
  "difficulty": "INTERMEDIATE",
  "prerequisites": [
    81,
    113
  ],
  "concepts": [
    "Frontier Pointer Min-Heap",
    "O(N log K) Multi-Stream Merging"
  ],
  "practiceSkills": [
    "K-Way Merging Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Merge K sorted linked lists or streams using a min-heap tracking current heads",
    "Achieve optimal O(N log K) total runtime and O(K) auxiliary space"
  ],
  "practiceArchetype": "problem",
  "flowTier": "tier2"
,
  "steps": [
    {
        "id": "day115-step1",
        "stepNumber": 1,
        "title": "Merge K Sorted Lists via Min-Heap: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: K-Way Merging",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for K-Way Merging.",
        "markdownContent": [
            "Merge K Sorted Lists combines K sorted linked lists into a single sorted list in O(N log K) time using a Min-Heap of size K.",
            "### Foundational Mental Model\nWhen approaching problems requiring **K-Way Merging**, remember the central principle: Maintaining K active pointers in a min-heap resolves K-way merging in O(N log K) time."
        ],
        "snippets": [
            {
                "title": "K-Way Merging Implementation Template",
                "code": "# Merge K Sorted Lists pattern\n# heap holds (node.val, list_idx, node)\n# pop minimum, advance list_idx pointer, push next node",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Maintaining K active pointers in a min-heap resolves K-way merging in O(N log K) time."
    },
    {
        "id": "day115-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: K-Way Merging",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Initialize a min-heap with the head node of each of the K lists: `(node.val, i, node)`. Pop the smallest node, attach it to `curr.next`, and if `node.next` exists, push `(node.next.val, i, node.next)` into the heap. Repeat until heap is empty.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Maintaining K active pointers in a min-heap resolves K-way merging in O(N log K) time.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "K-Way Merging Core Invariant",
                "content": "Maintaining K active pointers in a min-heap resolves K-way merging in O(N log K) time."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Maintaining K active pointers in a min-heap resolves K-way merging in O(N log K) time."
    },
    {
        "id": "day115-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: K-Way Merging",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d115-q1",
                "question": "Why is the time complexity of merging K sorted lists with total N nodes O(N log K) rather than O(N log N)?",
                "options": [
                    {
                        "id": "A",
                        "label": "The heap never contains more than K active elements simultaneously, so each of the N nodes experiences an O(log K) heap operation"
                    },
                    {
                        "id": "B",
                        "label": "Because the linked lists are already merged"
                    },
                    {
                        "id": "C",
                        "label": "Because K is always equal to 2"
                    },
                    {
                        "id": "D",
                        "label": "Because binary search is used to find K"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! The heap stores at most one node per list (size K). Extracting min and inserting successor takes O(log K). Across all N nodes in total, time is $N \\times O(\\log K) = O(N \\log K)$.",
                    "B": "Incorrect: Lists are separate and unmerged.",
                    "C": "Incorrect: K can be arbitrarily large.",
                    "D": "Incorrect: Heap maintains dynamic minimum."
                }
            },
            {
                "id": "chk-d115-q2",
                "question": "Why must the tuple pushed to the heap include the list index `i` as `(node.val, i, node)`?",
                "options": [
                    {
                        "id": "A",
                        "label": "To act as a unique tie-breaker, preventing Python from attempting to compare unorderable `ListNode` objects when two nodes have equal values"
                    },
                    {
                        "id": "B",
                        "label": "To count total nodes"
                    },
                    {
                        "id": "C",
                        "label": "Because heapq requires 3-tuples"
                    },
                    {
                        "id": "D",
                        "label": "To determine which list is longest"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! If two nodes have `node1.val == node2.val`, Python falls back to comparing the second element. Integer `i` is distinct for each list, breaking the tie cleanly before reaching `node`.",
                    "B": "Incorrect: It serves purely as a tie-breaker.",
                    "C": "Incorrect: Heapq accepts any comparable objects.",
                    "D": "Incorrect: List length is not stored."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day115-step4",
        "stepNumber": 4,
        "title": "Guided Practice: K-Way Merging",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Merge K sorted lists of integers represented as lists into a single sorted list using a min-heap.",
        "subheading": "Implement and verify K-Way Merging in the interactive workspace.",
        "task": {
            "title": "Merge K sorted lists of integers represented as lists into a single sorted list using a min-heap.",
            "instructions": [
                "Merge K sorted lists of integers represented as lists into a single sorted list using a min-heap.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "import heapq\n\ndef merge_k_arrays(arrays: list[list[int]]) -> list[int]:\n    # TODO: Maintain a min-heap of (val, array_idx, elem_idx) to merge in O(N log K)\n    return []\n\narrs = [[1, 4, 7], [2, 5, 8], [3, 6, 9]]\nprint('Merged:', merge_k_arrays(arrs))\n",
            "solutionCode": "import heapq\n\ndef merge_k_arrays(arrays: list[list[int]]) -> list[int]:\n    heap = []\n    for i, arr in enumerate(arrays):\n        if arr:\n            heapq.heappush(heap, (arr[0], i, 0))\n    res = []\n    while heap:\n        val, a_idx, e_idx = heapq.heappop(heap)\n        res.append(val)\n        if e_idx + 1 < len(arrays[a_idx]):\n            next_val = arrays[a_idx][e_idx + 1]\n            heapq.heappush(heap, (next_val, a_idx, e_idx + 1))\n    return res\n\narrs = [[1, 4, 7], [2, 5, 8], [3, 6, 9]]\nprint('Merged:', merge_k_arrays(arrs))\n",
            "expectedOutputPatterns": [
                "Merged: [1, 2, 3, 4, 5, 6, 7, 8, 9]"
            ],
            "hint": "Push initial elements: (arr[0], i, 0). While heap: pop val, a_idx, e_idx; append val to res; if e_idx + 1 < len(arrays[a_idx]): push next element."
        },
        "keyTakeaway": "Successfully implemented and verified K-Way Merging!"
    },
    {
        "id": "day115-step5",
        "stepNumber": 5,
        "title": "Day 115 Complete: Merge K Sorted Lists via Min-Heap",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 115,
        "heading": "Mastery Achieved: Merge K Sorted Lists via Min-Heap",
        "subheading": "You have solidified key mental models and techniques for K-Way Merging.",
        "recapRows": [
            {
                "concept": "K-Way Tournament",
                "naiveIntuition": "Compare all K list heads with a linear loop O(K * N)",
                "pythonReality": "A min-heap reduces the K-way comparison tournament to logarithmic O(log K) per extracted element"
            },
            {
                "concept": "Pointer Frontier",
                "naiveIntuition": "Load all N nodes into the heap at once O(N log N)",
                "pythonReality": "Only the active frontier (1 node per list) needs to be in the heap at any instant, capping size to K"
            }
        ],
        "solidifiedConcepts": [
            "Frontier Pointer Min-Heap",
            "O(N log K) Multi-Stream Merging"
        ],
        "nextDayPreview": {
            "dayNumber": 116,
            "title": "Two-Heap Pattern: Median of a Stream",
            "description": "Implement the two-heap pattern (max-heap for lower half, min-heap for upper half) to find stream medians in O(1) time."
        }
    }
]
},
  116: {
  "dayNumber": 116,
  "title": "Two-Heap Pattern: Median of a Stream",
  "topicName": "Two Heaps",
  "sectionId": "heaps-and-priority-queues",
  "estimatedMinutes": 45,
  "difficulty": "INTERMEDIATE",
  "prerequisites": [
    113
  ],
  "concepts": [
    "Max-Heap (Lower) & Min-Heap (Upper)",
    "O(1) Median & O(log N) Insertion"
  ],
  "practiceSkills": [
    "Two Heaps Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Balance a max-heap of smaller elements and min-heap of larger elements",
    "Retrieve running medians in O(1) time and insert stream values in O(log N) time"
  ],
  "practiceArchetype": "algorithm",
  "flowTier": "tier3"
,
  "steps": [
    {
        "id": "day116-step1",
        "stepNumber": 1,
        "title": "Two-Heap Pattern: Median of a Stream: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Two Heaps",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Two Heaps.",
        "markdownContent": [
            "Finding Median from Data Stream uses a Two-Heap Architecture: a Max-Heap for the smaller half and a Min-Heap for the larger half, delivering O(log N) insertion and O(1) median retrieval.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Two Heaps**, remember the central principle: Opposing min and max heaps maintain the median split of dynamic data streams in O(1) query time."
        ],
        "snippets": [
            {
                "title": "Two Heaps Implementation Template",
                "code": "# Two-Heap Median Finder\n# small: max-heap (negated) stores values <= median\n# large: min-heap stores values >= median\n# Balance: 0 <= len(small) - len(large) <= 1",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Opposing min and max heaps maintain the median split of dynamic data streams in O(1) query time."
    },
    {
        "id": "day116-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Two Heaps",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Divide stream into two halves: `small` (max-heap storing smaller half) and `large` (min-heap storing larger half). Invariant 1: all elements in `small` <= all in `large`. Invariant 2: sizes balanced so `len(small) == len(large)` (even) or `len(small) == len(large) + 1` (odd). Median is `small[0]` or `(small[0] + large[0]) / 2`.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Opposing min and max heaps maintain the median split of dynamic data streams in O(1) query time.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Two Heaps Core Invariant",
                "content": "Opposing min and max heaps maintain the median split of dynamic data streams in O(1) query time."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Opposing min and max heaps maintain the median split of dynamic data streams in O(1) query time."
    },
    {
        "id": "day116-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Two Heaps",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d116-q1",
                "question": "Why does the smaller half of numbers require a MAX-heap rather than a min-heap?",
                "options": [
                    {
                        "id": "A",
                        "label": "Because the median boundary is the LARGEST element of the smaller half, which resides at the root of a max-heap in O(1)"
                    },
                    {
                        "id": "B",
                        "label": "Because Python heapq only supports max-heaps"
                    },
                    {
                        "id": "C",
                        "label": "To sort the smaller numbers in reverse"
                    },
                    {
                        "id": "D",
                        "label": "Because small numbers are always negative"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! The median sits at the boundary between the two halves. The highest value in the lower half (`small.root`) and the lowest value in the upper half (`large.root`) directly sandwich the median.",
                    "B": "Incorrect: Python heapq defaults to min-heaps.",
                    "C": "Incorrect: Heaps do not completely sort their elements.",
                    "D": "Incorrect: Numbers can be arbitrary."
                }
            },
            {
                "id": "chk-d116-q2",
                "question": "What are the time complexities for `addNum()` and `findMedian()` in the two-heap median finder?",
                "options": [
                    {
                        "id": "A",
                        "label": "`addNum` is O(log N), `findMedian` is O(1)"
                    },
                    {
                        "id": "B",
                        "label": "Both are O(N)"
                    },
                    {
                        "id": "C",
                        "label": "Both are O(1)"
                    },
                    {
                        "id": "D",
                        "label": "`addNum` is O(1), `findMedian` is O(N)"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Adding a number performs a constant number of heap push and pop operations, each taking O(log N). Inspecting the roots to compute the median takes O(1) time.",
                    "B": "Incorrect: Heaps avoid linear scans.",
                    "C": "Incorrect: Inserting into a heap requires O(log N) sifting.",
                    "D": "Incorrect: Two-heap structure eliminates O(N) median scans."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day116-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Two Heaps",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Implement MedianFinder supporting add_num and find_median.",
        "subheading": "Implement and verify Two Heaps in the interactive workspace.",
        "task": {
            "title": "Implement MedianFinder supporting add_num and find_median.",
            "instructions": [
                "Implement MedianFinder supporting add_num and find_median.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "import heapq\n\nclass MedianFinder:\n    def __init__(self):\n        self.small = [] # max-heap (stores -val)\n        self.large = [] # min-heap\n\n    # TODO: Implement add_num(num) and find_median() -> float\n\nmf = MedianFinder()\nmf.add_num(1)\nmf.add_num(2)\nprint('Median (1, 2):', mf.find_median()) # 1.5\nmf.add_num(3)\nprint('Median (1, 2, 3):', mf.find_median()) # 2.0\n",
            "solutionCode": "import heapq\n\nclass MedianFinder:\n    def __init__(self):\n        self.small = [] # max-heap\n        self.large = [] # min-heap\n\n    def add_num(self, num: int) -> None:\n        # Push to small first\n        heapq.heappush(self.small, -num)\n        # Balance order: largest in small must be <= smallest in large\n        if self.small and self.large and (-self.small[0] > self.large[0]):\n            val = -heapq.heappop(self.small)\n            heapq.heappush(self.large, val)\n        # Balance sizes: small can have at most 1 more element than large\n        if len(self.small) > len(self.large) + 1:\n            val = -heapq.heappop(self.small)\n            heapq.heappush(self.large, val)\n        elif len(self.large) > len(self.small):\n            val = heapq.heappop(self.large)\n            heapq.heappush(self.small, -val)\n\n    def find_median(self) -> float:\n        if len(self.small) > len(self.large):\n            return float(-self.small[0])\n        return (-self.small[0] + self.large[0]) / 2.0\n\nmf = MedianFinder()\nmf.add_num(1)\nmf.add_num(2)\nprint('Median (1, 2):', mf.find_median())\nmf.add_num(3)\nprint('Median (1, 2, 3):', mf.find_median())\n",
            "expectedOutputPatterns": [
                "Median (1, 2): 1.5",
                "Median (1, 2, 3): 2.0"
            ],
            "hint": "Push -num to small. If small root > large root: move to large. Balance lengths so len(small) is either len(large) or len(large) + 1. If len(small) > len(large): return -small[0] else (-small[0] + large[0]) / 2."
        },
        "keyTakeaway": "Successfully implemented and verified Two Heaps!"
    },
    {
        "id": "day116-step5",
        "stepNumber": 5,
        "title": "Day 116 Complete: Two-Heap Pattern: Median of a Stream",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 116,
        "heading": "Mastery Achieved: Two-Heap Pattern: Median of a Stream",
        "subheading": "You have solidified key mental models and techniques for Two Heaps.",
        "recapRows": [
            {
                "concept": "Opposing Heap Equilibrium",
                "naiveIntuition": "Sort the array on every insertion O(N log N)",
                "pythonReality": "Maintaining a max-heap and min-heap back-to-back locks the middle elements in place with O(log N) updates"
            },
            {
                "concept": "Instant Median Access",
                "naiveIntuition": "Finding median requires scanning elements",
                "pythonReality": "The roots of the balanced two-heap structure give instant O(1) access to median candidates"
            }
        ],
        "solidifiedConcepts": [
            "Max-Heap (Lower) & Min-Heap (Upper)",
            "O(1) Median & O(log N) Insertion"
        ],
        "nextDayPreview": {
            "dayNumber": 117,
            "title": "Task Scheduler & Priority Reorganization",
            "description": "Schedule CPU tasks with cooling intervals using greedy max-heaps and cooldown queue staging in O(N) time."
        }
    }
]
},
  117: {
  "dayNumber": 117,
  "title": "Task Scheduler & Priority Reorganization",
  "topicName": "Task Scheduling",
  "sectionId": "heaps-and-priority-queues",
  "estimatedMinutes": 40,
  "difficulty": "INTERMEDIATE",
  "prerequisites": [
    113,
    114
  ],
  "concepts": [
    "Greedy Max-Frequency Extraction",
    "Cooldown Queue Waiting Line"
  ],
  "practiceSkills": [
    "Task Scheduling Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Schedule CPU tasks with cooldown interval n using a max-heap and wait queue",
    "Compute minimum CPU idle intervals to complete all tasks"
  ],
  "practiceArchetype": "problem",
  "flowTier": "tier2"
,
  "steps": [
    {
        "id": "day117-step1",
        "stepNumber": 1,
        "title": "Task Scheduler & Priority Reorganization: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Task Scheduling",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Task Scheduling.",
        "markdownContent": [
            "Task Scheduler coordinates CPU execution of tasks with cooling periods using a Greedy Max-Heap paired with a Cooldown FIFO Queue to minimize idle intervals.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Task Scheduling**, remember the central principle: Greedy execution of the most frequent remaining tasks minimizes mandatory idle cooling slots."
        ],
        "snippets": [
            {
                "title": "Task Scheduling Implementation Template",
                "code": "# Task Scheduler with Cooldown Queue\n# heap: max frequencies available to execute\n# queue: (freq, available_time) cooling down",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Greedy execution of the most frequent remaining tasks minimizes mandatory idle cooling slots."
    },
    {
        "id": "day117-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Task Scheduling",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Count task frequencies. Max-heap stores frequencies (greedy: execute most frequent task first). A FIFO queue stores `(remaining_freq, ready_time)`. In each unit of time: pop most frequent task, decrement frequency. If tasks remain, enqueue with `ready_time = current_time + n`. If queue front is ready at `current_time`, re-push to heap.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Greedy execution of the most frequent remaining tasks minimizes mandatory idle cooling slots.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Task Scheduling Core Invariant",
                "content": "Greedy execution of the most frequent remaining tasks minimizes mandatory idle cooling slots."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Greedy execution of the most frequent remaining tasks minimizes mandatory idle cooling slots."
    },
    {
        "id": "day117-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Task Scheduling",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d117-q1",
                "question": "Why is it mathematically optimal to always execute the task with the highest remaining frequency first?",
                "options": [
                    {
                        "id": "A",
                        "label": "Tasks with higher frequencies require the most future cooling intervals, so scheduling them earliest gives the maximum room to interleave other tasks and avoid CPU idle cycles"
                    },
                    {
                        "id": "B",
                        "label": "Because higher frequency tasks run faster on the CPU"
                    },
                    {
                        "id": "C",
                        "label": "Because Python sorts heap elements automatically"
                    },
                    {
                        "id": "D",
                        "label": "To clear memory fastest"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! The most frequent task acts as the bottleneck dictating the minimum schedule length. Interleaving lower-frequency tasks inside its cooling slots prevents having idle time at the end.",
                    "B": "Incorrect: All tasks take exactly 1 unit of time.",
                    "C": "Incorrect: Max-heap selection is our deliberate strategy.",
                    "D": "Incorrect: Memory footprint is tiny."
                }
            },
            {
                "id": "chk-d117-q2",
                "question": "What happens in a time step if the max-heap is empty but the cooldown queue is not empty?",
                "options": [
                    {
                        "id": "A",
                        "label": "The CPU must execute an IDLE cycle because all remaining tasks are currently cooling down"
                    },
                    {
                        "id": "B",
                        "label": "The scheduler terminates immediately"
                    },
                    {
                        "id": "C",
                        "label": "The cooling constraint is ignored"
                    },
                    {
                        "id": "D",
                        "label": "A task is executed twice"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! If no tasks are ready to run and pending tasks are still cooling, the CPU has no valid work and must increment clock time while idling.",
                    "B": "Incorrect: Tasks remain to be executed.",
                    "C": "Incorrect: Cooldown constraints must be respected.",
                    "D": "Incorrect: That violates cooling rules."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day117-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Task Scheduling",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Calculate the least number of CPU units required to finish all tasks with cooling period n.",
        "subheading": "Implement and verify Task Scheduling in the interactive workspace.",
        "task": {
            "title": "Calculate the least number of CPU units required to finish all tasks with cooling period n.",
            "instructions": [
                "Calculate the least number of CPU units required to finish all tasks with cooling period n.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "from collections import Counter, deque\nimport heapq\n\ndef least_interval(tasks: list[str], n: int) -> int:\n    # TODO: Implement max-heap + cooldown queue scheduler\n    return 0\n\nprint('Total time (n=2):', least_interval(['A', 'A', 'A', 'B', 'B', 'B'], 2)) # 8\n",
            "solutionCode": "from collections import Counter, deque\nimport heapq\n\ndef least_interval(tasks: list[str], n: int) -> int:\n    counts = Counter(tasks)\n    max_heap = [-cnt for cnt in counts.values()]\n    heapq.heapify(max_heap)\n    \n    q = deque() # (cnt, ready_time)\n    time = 0\n    while max_heap or q:\n        time += 1\n        if max_heap:\n            cnt = 1 + heapq.heappop(max_heap) # cnt is negative, add 1 towards 0\n            if cnt != 0:\n                q.append((cnt, time + n))\n        if q and q[0][1] == time:\n            heapq.heappush(max_heap, q.popleft()[0])\n    return time\n\nprint('Total time (n=2):', least_interval(['A', 'A', 'A', 'B', 'B', 'B'], 2))\n",
            "expectedOutputPatterns": [
                "Total time (n=2): 8"
            ],
            "hint": "Count frequencies and push -cnt to max_heap. q = deque(). time = 0. While max_heap or q: time += 1. If max_heap: cnt = 1 + heappop; if cnt != 0: q.append((cnt, time + n)). If q and q[0][1] == time: heappush(max_heap, q.popleft()[0]). Return time."
        },
        "keyTakeaway": "Successfully implemented and verified Task Scheduling!"
    },
    {
        "id": "day117-step5",
        "stepNumber": 5,
        "title": "Day 117 Complete: Task Scheduler & Priority Reorganization",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 117,
        "heading": "Mastery Achieved: Task Scheduler & Priority Reorganization",
        "subheading": "You have solidified key mental models and techniques for Task Scheduling.",
        "recapRows": [
            {
                "concept": "Dual Container Scheduling",
                "naiveIntuition": "Simulate cooldowns with an array of timestamps",
                "pythonReality": "Pairing a Priority Queue (active ready pool) with a FIFO Queue (cooldown waitlist) models state transitions in O(log K)"
            },
            {
                "concept": "Bottleneck Domination",
                "naiveIntuition": "All tasks contribute equally to idle time",
                "pythonReality": "The maximum frequency task forms the scheduling skeleton; all other tasks fill intermediate slots"
            }
        ],
        "solidifiedConcepts": [
            "Greedy Max-Frequency Extraction",
            "Cooldown Queue Waiting Line"
        ],
        "nextDayPreview": {
            "dayNumber": 118,
            "title": "Indexed Priority Queue Principles",
            "description": "Design an Indexed Priority Queue supporting O(log N) arbitrary priority updates (decrease-key) and deletions."
        }
    }
]
},
  118: {
  "dayNumber": 118,
  "title": "Indexed Priority Queue Principles",
  "topicName": "Indexed Priority Queue",
  "sectionId": "heaps-and-priority-queues",
  "estimatedMinutes": 45,
  "difficulty": "INTERMEDIATE",
  "prerequisites": [
    112
  ],
  "concepts": [
    "Position Lookup Mapping (Key -> Index)",
    "O(log N) decrease_key Operation"
  ],
  "practiceSkills": [
    "Indexed Priority Queue Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Augment a binary heap with a hash map tracking element array indices",
    "Update priorities in-place (decrease_key) in strict O(log N) time without scanning"
  ],
  "practiceArchetype": "algorithm",
  "flowTier": "tier3"
,
  "steps": [
    {
        "id": "day118-step1",
        "stepNumber": 1,
        "title": "Indexed Priority Queue Principles: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Indexed Priority Queue",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Indexed Priority Queue.",
        "markdownContent": [
            "Indexed Priority Queues associate an inverted index map (key to heap-array position) with a binary heap, enabling O(log N) decrease_key priority updates and arbitrary key removals.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Indexed Priority Queue**, remember the central principle: Maintaining a reverse index map pos[item] = heap_idx enables O(log N) decrease_key priority updates."
        ],
        "snippets": [
            {
                "title": "Indexed Priority Queue Implementation Template",
                "code": "# Indexed Priority Queue Skeleton\nclass IndexedPQ:\n    def __init__(self):\n        self.heap = []       # [(priority, item)]\n        self.pos = {}        # {item: heap_index}\n    def swap(self, i, j):\n        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]\n        self.pos[self.heap[i][1]] = i\n        self.pos[self.heap[j][1]] = j\n    def decrease_key(self, item, new_p):\n        idx = self.pos[item]\n        self.heap[idx] = (new_p, item)\n        # sift-up from idx in O(log N)\n        while idx > 0:\n            p = (idx - 1) // 2\n            if self.heap[idx][0] < self.heap[p][0]:\n                self.swap(idx, p); idx = p\n            else: break",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Maintaining a reverse index map pos[item] = heap_idx enables O(log N) decrease_key priority updates."
    },
    {
        "id": "day118-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Indexed Priority Queue",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Standard heaps require O(N) linear scans to find an item before updating its priority. An Indexed Priority Queue maintains `pos = {item: index}` tracking where each item sits in the flat `heap` array. Whenever items swap during sift-up or sift-down, their positions in `pos` are updated simultaneously in O(1). This unlocks O(log N) `change_priority()` essential for Dijkstra and A* search.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Maintaining a reverse index map pos[item] = heap_idx enables O(log N) decrease_key priority updates.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Indexed Priority Queue Core Invariant",
                "content": "Maintaining a reverse index map pos[item] = heap_idx enables O(log N) decrease_key priority updates."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Maintaining a reverse index map pos[item] = heap_idx enables O(log N) decrease_key priority updates."
    },
    {
        "id": "day118-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Indexed Priority Queue",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d118-q1",
                "question": "Why does Python's standard `heapq` module NOT provide a built-in `decrease_key` operation?",
                "options": [
                    {
                        "id": "A",
                        "label": "Standard heapq operates on plain Python lists without maintaining a secondary hash table of item-to-index positions; finding an element requires an O(N) scan"
                    },
                    {
                        "id": "B",
                        "label": "Because priorities cannot decrease in computer science"
                    },
                    {
                        "id": "C",
                        "label": "Because Python lists cannot swap elements"
                    },
                    {
                        "id": "D",
                        "label": "Because heaps are strictly immutable in Python"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Without a reverse lookup dictionary `pos[item] = index`, locating the item inside the heap list takes O(N) linear time, destroying logarithmic efficiency. Python developers use lazy deletion or indexed priority queues instead.",
                    "B": "Incorrect: decrease_key is the foundational primitive of Dijkstra's algorithm.",
                    "C": "Incorrect: Python list element swapping is O(1).",
                    "D": "Incorrect: Python lists are mutable."
                }
            },
            {
                "id": "chk-d118-q2",
                "question": "What is the time complexity of `decrease_key` in an Indexed Priority Queue with N elements?",
                "options": [
                    {
                        "id": "A",
                        "label": "O(log N) time, because pos[item] locates the index in O(1) and sift-up travels at most the tree height H = log2 N"
                    },
                    {
                        "id": "B",
                        "label": "O(N) time"
                    },
                    {
                        "id": "C",
                        "label": "O(N log N) time"
                    },
                    {
                        "id": "D",
                        "label": "O(1) time"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! The hash map gives the heap index in O(1) time. Updating the value and bubbling up towards the root takes O(log N) swaps.",
                    "B": "Incorrect: O(N) is the cost in unindexed heaps.",
                    "C": "Incorrect: Re-heapifying the entire array takes O(N), but sift-up is O(log N).",
                    "D": "Incorrect: Fibonacci heaps achieve amortized O(1) decrease-key, but standard binary IPQs are O(log N)."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day118-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Indexed Priority Queue",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Implement an Indexed Priority Queue with O(log N) decrease_key support.",
        "subheading": "Implement and verify Indexed Priority Queue in the interactive workspace.",
        "task": {
            "title": "Implement an Indexed Priority Queue with O(log N) decrease_key support.",
            "instructions": [
                "Implement an Indexed Priority Queue with O(log N) decrease_key support.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "class IndexedMinPQ:\n    def __init__(self):\n        self.heap = []  # list of [priority, item]\n        self.pos = {}   # item -> index in heap\n\n    # TODO: Implement push, pop_min, and decrease_key(item, new_priority)\n\npq = IndexedMinPQ()\n# Test usage\n",
            "solutionCode": "class IndexedMinPQ:\n    def __init__(self):\n        self.heap = []\n        self.pos = {}\n\n    def _swap(self, i: int, j: int) -> None:\n        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]\n        self.pos[self.heap[i][1]] = i\n        self.pos[self.heap[j][1]] = j\n\n    def push(self, item: str, priority: int) -> None:\n        idx = len(self.heap)\n        self.heap.append([priority, item])\n        self.pos[item] = idx\n        self._sift_up(idx)\n\n    def _sift_up(self, idx: int) -> None:\n        while idx > 0:\n            parent = (idx - 1) // 2\n            if self.heap[idx][0] < self.heap[parent][0]:\n                self._swap(idx, parent)\n                idx = parent\n            else:\n                break\n\n    def decrease_key(self, item: str, new_priority: int) -> None:\n        if item in self.pos:\n            idx = self.pos[item]\n            if new_priority < self.heap[idx][0]:\n                self.heap[idx][0] = new_priority\n                self._sift_up(idx)\n\n    def pop_min(self) -> tuple[int, str]:\n        min_entry = self.heap[0]\n        last_entry = self.heap.pop()\n        del self.pos[min_entry[1]]\n        if self.heap:\n            self.heap[0] = last_entry\n            self.pos[last_entry[1]] = 0\n            self._sift_down(0)\n        return tuple(min_entry)\n\n    def _sift_down(self, idx: int) -> None:\n        n = len(self.heap)\n        while 2 * idx + 1 < n:\n            smallest = idx\n            left = 2 * idx + 1\n            right = 2 * idx + 2\n            if left < n and self.heap[left][0] < self.heap[smallest][0]:\n                smallest = left\n            if right < n and self.heap[right][0] < self.heap[smallest][0]:\n                smallest = right\n            if smallest != idx:\n                self._swap(idx, smallest)\n                idx = smallest\n            else:\n                break\n\npq = IndexedMinPQ()\npq.push('task_A', 10)\npq.push('task_B', 20)\npq.decrease_key('task_B', 5) # task_B promoted to priority 5!\nprint('Next task:', pq.pop_min()) # (5, 'task_B')\nprint('Next task:', pq.pop_min()) # (10, 'task_A')\n",
            "expectedOutputPatterns": [
                "Next task: (5, 'task_B')",
                "Next task: (10, 'task_A')"
            ],
            "hint": "Track self.pos[item] = idx during swaps. In decrease_key(item, new_p): set heap[idx][0] = new_p and call _sift_up(idx)."
        },
        "keyTakeaway": "Successfully implemented and verified Indexed Priority Queue!"
    },
    {
        "id": "day118-step5",
        "stepNumber": 5,
        "title": "Day 118 Complete: Indexed Priority Queue Principles",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 118,
        "heading": "Mastery Achieved: Indexed Priority Queue Principles",
        "subheading": "You have solidified key mental models and techniques for Indexed Priority Queue.",
        "recapRows": [
            {
                "concept": "Inverted Heap Indexing",
                "naiveIntuition": "Heaps only support accessing the root element",
                "pythonReality": "Maintaining a parallel dictionary of item-to-index pointers unlocks O(log N) updates to arbitrary elements in the heap"
            },
            {
                "concept": "Heap Mutation Parity",
                "naiveIntuition": "Re-sorting the array on priority updates is fine",
                "pythonReality": "Full re-heapify takes O(N); single-element sift-up takes O(log N), making shortest path graph algorithms viable at production scale"
            }
        ],
        "solidifiedConcepts": [
            "Position Lookup Mapping (Key -> Index)",
            "O(log N) decrease_key Operation"
        ],
        "nextDayPreview": {
            "dayNumber": 119,
            "title": "Kth Smallest Element in Sorted Matrix",
            "description": "Locate the Kth smallest element in row/column sorted matrices using heap frontier exploration in O(K log N) time."
        }
    }
]
},
  119: {
  "dayNumber": 119,
  "title": "Kth Smallest Element in Sorted Matrix",
  "topicName": "Matrix Kth Smallest",
  "sectionId": "heaps-and-priority-queues",
  "estimatedMinutes": 35,
  "difficulty": "INTERMEDIATE",
  "prerequisites": [
    47,
    113
  ],
  "concepts": [
    "Row/Column Frontier Min-Heap",
    "O(K log(min(K, N))) Search"
  ],
  "practiceSkills": [
    "Matrix Kth Smallest Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Extract K smallest elements from row-and-column sorted matrices via frontier heaps",
    "Contrast priority queue frontier search against monotonic binary search"
  ],
  "practiceArchetype": "problem",
  "flowTier": "tier2"
,
  "steps": [
    {
        "id": "day119-step1",
        "stepNumber": 1,
        "title": "Kth Smallest Element in Sorted Matrix: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Matrix Kth Smallest",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Matrix Kth Smallest.",
        "markdownContent": [
            "Kth Smallest Element in a Sorted Matrix explores a 2D matrix where rows and columns are sorted, expanding frontier elements with a Min-Heap in O(K log(min(K, N))) time.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Matrix Kth Smallest**, remember the central principle: Row/column sorted matrices behave as K sorted linked lists, explored via min-heap frontiers."
        ],
        "snippets": [
            {
                "title": "Matrix Kth Smallest Implementation Template",
                "code": "# Kth Smallest in Sorted Matrix\nimport heapq\ndef kth_smallest_matrix(matrix, k):\n    n = len(matrix)\n    h = [(matrix[r][0], r, 0) for r in range(min(k, n))]\n    heapq.heapify(h)\n    for _ in range(k):\n        val, r, c = heapq.heappop(h)\n        if c + 1 < n: heapq.heappush(h, (matrix[r][c + 1], r, c + 1))\n    return val",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Row/column sorted matrices behave as K sorted linked lists, explored via min-heap frontiers."
    },
    {
        "id": "day119-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Matrix Kth Smallest",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Initialize min-heap with the first element of each of the first min(K, N) rows: `(matrix[r][0], r, 0)`. Pop the minimum element K times. When popping `(val, r, c)`, push the immediate right neighbor `(matrix[r][c + 1], r, c + 1)` if within bounds. The K-th popped element is the answer.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Row/column sorted matrices behave as K sorted linked lists, explored via min-heap frontiers.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Matrix Kth Smallest Core Invariant",
                "content": "Row/column sorted matrices behave as K sorted linked lists, explored via min-heap frontiers."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Row/column sorted matrices behave as K sorted linked lists, explored via min-heap frontiers."
    },
    {
        "id": "day119-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Matrix Kth Smallest",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d119-q1",
                "question": "Why is it sufficient to initialize the min-heap with only the first element of each row `(matrix[r][0], r, 0)`?",
                "options": [
                    {
                        "id": "A",
                        "label": "Because each row is sorted, `matrix[r][0]` is the smallest element in its row, guaranteeing that the global minimum must be among row heads"
                    },
                    {
                        "id": "B",
                        "label": "Because matrix rows cannot exceed length 3"
                    },
                    {
                        "id": "C",
                        "label": "Because the matrix diagonal is sorted"
                    },
                    {
                        "id": "D",
                        "label": "Because all row elements are identical"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Since every row is sorted from left to right, no element `matrix[r][c]` (with c > 0) can be smaller than `matrix[r][0]`. The row heads form the complete initial candidate frontier.",
                    "B": "Incorrect: Matrix can have arbitrary dimensions N x N.",
                    "C": "Incorrect: Diagonals are not necessarily contiguous.",
                    "D": "Incorrect: Elements can be strictly distinct."
                }
            },
            {
                "id": "chk-d119-q2",
                "question": "What is the maximum number of elements present in the heap at any given moment during the algorithm?",
                "options": [
                    {
                        "id": "A",
                        "label": "`min(K, N)` elements"
                    },
                    {
                        "id": "B",
                        "label": "`N * N` elements"
                    },
                    {
                        "id": "C",
                        "label": "1 element"
                    },
                    {
                        "id": "D",
                        "label": "2^N elements"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Each row contributes at most one active candidate pointer at a time. The heap size never exceeds the row count (or K if K < N), keeping space complexity to O(min(K, N)).",
                    "B": "Incorrect: Full matrix is never dumped into the heap.",
                    "C": "Incorrect: Heap maintains a multi-row frontier.",
                    "D": "Incorrect: Matrix expansion is polynomial."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day119-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Matrix Kth Smallest",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Find the Kth smallest element in a row- and column-sorted matrix using a min-heap.",
        "subheading": "Implement and verify Matrix Kth Smallest in the interactive workspace.",
        "task": {
            "title": "Find the Kth smallest element in a row- and column-sorted matrix using a min-heap.",
            "instructions": [
                "Find the Kth smallest element in a row- and column-sorted matrix using a min-heap.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "import heapq\n\ndef kth_smallest_matrix(matrix: list[list[int]], k: int) -> int:\n    # TODO: Maintain min-heap of row heads and advance horizontally\n    return -1\n\nmat = [\n  [1,  5,  9],\n  [10, 11, 13],\n  [12, 13, 15]\n]\nprint('8th smallest:', kth_smallest_matrix(mat, 8)) # 13\n",
            "solutionCode": "import heapq\n\ndef kth_smallest_matrix(matrix: list[list[int]], k: int) -> int:\n    n = len(matrix)\n    heap = [(matrix[r][0], r, 0) for r in range(min(k, n))]\n    heapq.heapify(heap)\n    val = -1\n    for _ in range(k):\n        val, r, c = heapq.heappop(heap)\n        if c + 1 < n:\n            heapq.heappush(heap, (matrix[r][c + 1], r, c + 1))\n    return val\n\nmat = [\n  [1,  5,  9],\n  [10, 11, 13],\n  [12, 13, 15]\n]\nprint('8th smallest:', kth_smallest_matrix(mat, 8))\n",
            "expectedOutputPatterns": [
                "8th smallest: 13"
            ],
            "hint": "Initialize heap with [(matrix[r][0], r, 0) for r in range(min(k, len(matrix)))]. Loop k times: pop val, r, c; if c + 1 < n: push (matrix[r][c+1], r, c+1). Return val."
        },
        "keyTakeaway": "Successfully implemented and verified Matrix Kth Smallest!"
    },
    {
        "id": "day119-step5",
        "stepNumber": 5,
        "title": "Day 119 Complete: Kth Smallest Element in Sorted Matrix",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 119,
        "heading": "Mastery Achieved: Kth Smallest Element in Sorted Matrix",
        "subheading": "You have solidified key mental models and techniques for Matrix Kth Smallest.",
        "recapRows": [
            {
                "concept": "2D Matrix as K Sorted Sequences",
                "naiveIntuition": "Flatten and sort the entire N^2 matrix in O(N^2 log N)",
                "pythonReality": "Viewing matrix rows as sorted lists reduces the search to a K-way merge in O(K log N) time and O(N) space"
            },
            {
                "concept": "Frontier Advancing",
                "naiveIntuition": "Explore both down and right neighbors causing duplicate entries",
                "pythonReality": "Seeding all row heads and advancing strictly rightward guarantees every matrix cell is visited at most once with zero duplicates"
            }
        ],
        "solidifiedConcepts": [
            "Row/Column Frontier Min-Heap",
            "O(K log(min(K, N))) Search"
        ],
        "nextDayPreview": {
            "dayNumber": 120,
            "title": "Section 10 Review & Priority Queue Design",
            "description": "Synthesize binary heap algorithms, running median dual-heaps, and indexed priority queues into a streaming scheduler."
        }
    }
]
},
  120: {
  "dayNumber": 120,
  "title": "Section 10 Review & Priority Queue Design",
  "topicName": "Heaps Milestone",
  "sectionId": "heaps-and-priority-queues",
  "estimatedMinutes": 45,
  "difficulty": "INTERMEDIATE",
  "prerequisites": [
    112,
    113,
    115,
    116,
    118
  ],
  "concepts": [
    "Priority Queue Engineering",
    "Dynamic Rebalancing",
    "Stream Processing Under SLA"
  ],
  "practiceSkills": [
    "Heaps Milestone Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Architect a priority dispatch engine handling dynamic priority shifts and task starvation",
    "Evaluate space-time trade-offs between two-heaps, sorted arrays, and balanced BSTs"
  ],
  "practiceArchetype": "milestone",
  "flowTier": "tier3"
,
  "steps": [
    {
        "id": "day120-step1",
        "stepNumber": 1,
        "title": "Section 10 Review & Priority Queue Design: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Heaps Milestone",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Heaps Milestone.",
        "markdownContent": [
            "Section 10 Review synthesizes flat array binary heaps, linear heapify, heapq comparator patterns, top-K selection, and multi-heap architectures.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Heaps Milestone**, remember the central principle: Heaps provide logarithmic priority ordering, transforming sorting bottlenecks into streaming real-time pipelines."
        ],
        "snippets": [
            {
                "title": "Heaps Milestone Implementation Template",
                "code": "# Heap Architecture Selection:\n# Top-K Largest -> Min-Heap size K (O(N log K))\n# Top-K Smallest -> Max-Heap size K (O(N log K))\n# Continuous Median -> Dual Heap Balance (O(log N) insert, O(1) query)\n# Merge K Sorted -> Frontier Min-Heap size K (O(N log K))",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Heaps provide logarithmic priority ordering, transforming sorting bottlenecks into streaming real-time pipelines."
    },
    {
        "id": "day120-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Heaps Milestone",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Heap Problem Taxonomy: (1) Dynamic extremum lookup / priority queue? Min-Heap / Max-Heap. (2) Top-K elements in stream? Min-heap of size K. (3) Continuous median tracking? Balanced two-heap (max-heap small, min-heap large). (4) K-way merging? Frontier heap of size K.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Heaps provide logarithmic priority ordering, transforming sorting bottlenecks into streaming real-time pipelines.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Heaps Milestone Core Invariant",
                "content": "Heaps provide logarithmic priority ordering, transforming sorting bottlenecks into streaming real-time pipelines."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Heaps provide logarithmic priority ordering, transforming sorting bottlenecks into streaming real-time pipelines."
    },
    {
        "id": "day120-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Heaps Milestone",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d120-q1",
                "question": "Which data structure combination is optimal for calculating the running 95th percentile latency of a live web service processing millions of requests per second?",
                "options": [
                    {
                        "id": "A",
                        "label": "Two Heaps (a Max-Heap holding the bottom 95% and a Min-Heap holding the top 5%), balanced dynamically"
                    },
                    {
                        "id": "B",
                        "label": "Sorting the array on every incoming HTTP request in O(N log N)"
                    },
                    {
                        "id": "C",
                        "label": "A single singly linked list"
                    },
                    {
                        "id": "D",
                        "label": "A LIFO stack"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Just like running median (50th percentile) uses 50/50 two-heap balance, any arbitrary P-th percentile is maintained by rebalancing two heaps to an exact P / (100 - P) size ratio in O(log N) time.",
                    "B": "Incorrect: Sorting millions of elements on every request crashes latency.",
                    "C": "Incorrect: Linked list has O(N) insertion.",
                    "D": "Incorrect: Stacks cannot maintain percentile ordering."
                }
            },
            {
                "id": "chk-d120-q2",
                "question": "What is the time complexity of building a heap from N elements via `heapq.heapify` versus pushing elements one by one?",
                "options": [
                    {
                        "id": "A",
                        "label": "`heapify` is O(N) linear time, while repeated pushing is O(N log N)"
                    },
                    {
                        "id": "B",
                        "label": "Both are O(N log N)"
                    },
                    {
                        "id": "C",
                        "label": "Both are O(N)"
                    },
                    {
                        "id": "D",
                        "label": "`heapify` is O(N^2)"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Heapify exploits bottom-up sift-down where the vast majority of nodes reside near leaf levels, mathematically bounding the summation of heights to O(N).",
                    "B": "Incorrect: Heapify is strictly faster than repeated pushes.",
                    "C": "Incorrect: Repeated push is bounded by N log N.",
                    "D": "Incorrect: Heapify is never quadratic."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day120-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Heaps Milestone",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Build a K-Nearest Points to Origin selector using a Max-Heap of size K.",
        "subheading": "Implement and verify Heaps Milestone in the interactive workspace.",
        "task": {
            "title": "Build a K-Nearest Points to Origin selector using a Max-Heap of size K.",
            "instructions": [
                "Build a K-Nearest Points to Origin selector using a Max-Heap of size K.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "import heapq\n\ndef k_closest(points: list[list[int]], k: int) -> list[list[int]]:\n    # TODO: Maintain max-heap of size K based on Euclidean distance squared (x^2 + y^2)\n    return []\n\npts = [[1, 3], [-2, 2], [5, 8], [0, 1]]\nprint('2 Closest:', k_closest(pts, 2))\n",
            "solutionCode": "import heapq\n\ndef k_closest(points: list[list[int]], k: int) -> list[list[int]]:\n    heap = [] # max-heap stores (-dist_sq, x, y)\n    for x, y in points:\n        dist_sq = x * x + y * y\n        heapq.heappush(heap, (-dist_sq, x, y))\n        if len(heap) > k:\n            heapq.heappop(heap)\n    return [[x, y] for _, x, y in heap]\n\npts = [[1, 3], [-2, 2], [5, 8], [0, 1]]\nprint('2 Closest:', sorted(k_closest(pts, 2)))\n",
            "expectedOutputPatterns": [
                "2 Closest: [[-2, 2], [0, 1]]"
            ],
            "hint": "Push (-dist_sq, x, y) into heap. If len(heap) > k: heapq.heappop(heap). Return [[x, y] for _, x, y in heap]."
        },
        "keyTakeaway": "Successfully implemented and verified Heaps Milestone!"
    },
    {
        "id": "day120-step5",
        "stepNumber": 5,
        "title": "Day 120 Complete: Section 10 Review & Priority Queue Design",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 120,
        "heading": "Mastery Achieved: Section 10 Review & Priority Queue Design",
        "subheading": "You have solidified key mental models and techniques for Heaps Milestone.",
        "recapRows": [
            {
                "concept": "Distance Inversion",
                "naiveIntuition": "Sort all points by distance O(N log N)",
                "pythonReality": "A max-heap of size K evicts the furthest points, maintaining the K closest in O(N log K) time and O(K) space"
            },
            {
                "concept": "Section 10 Synthesis",
                "naiveIntuition": "Priority queues are only used for basic sorting",
                "pythonReality": "Heaps form the algorithmic engine behind Dijkstra's shortest path, Prim's MST, A* pathfinding, Huffman coding, and OS process schedulers"
            }
        ],
        "solidifiedConcepts": [
            "Priority Queue Engineering",
            "Dynamic Rebalancing",
            "Stream Processing Under SLA"
        ],
        "nextDayPreview": {
            "dayNumber": 121,
            "title": "Graph Representations & Adjacency Lists",
            "description": "Represent graphs using adjacency lists, adjacency matrices, and edge lists; evaluate density trade-offs."
        }
    }
]
},
};
