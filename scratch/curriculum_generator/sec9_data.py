"""
Section 9: Trees & Binary Search Trees (Days 96 to 110)
"""

SEC9_DAYS = {   96: {   'hint': 'Base cases: if not root return 0; if not root.left and not root.right return 1. Recurse: '
                    'count_leaves(root.left) + count_leaves(root.right).',
            'mechanics': 'Recursive definition: a tree is either empty (None) or a root node pointing to two disjoint '
                         'binary trees (left and right subtrees). Node height is max edges to a leaf; node depth is '
                         'edges from root. Maximum nodes at level L is 2^L.',
            'patterns': ['Leaf count: 3'],
            'practice_task': 'Count the total number of leaf nodes in a binary tree.',
            'q1': 'What is the maximum number of nodes in a binary tree of height H (where a single root node has '
                  'height 0)?',
            'q1_ans': 'A',
            'q1_exp': {   'A': 'Correct! Summing nodes at each level: 2^0 + 2^1 + ... + 2^H = 2^(H+1) - 1. For H=0, '
                               'total is 2^1 - 1 = 1; for H=2, total is 2^3 - 1 = 7.',
                          'B': 'Incorrect: 2^H is the maximum nodes on level H alone, not the total tree nodes.',
                          'C': 'Incorrect: Tree growth is exponential, not polynomial.',
                          'D': 'Incorrect: Tree growth is exponential, not linear.'},
            'q1_opts': [   {'id': 'A', 'label': '2^(H + 1) - 1'},
                           {'id': 'B', 'label': '2^H'},
                           {'id': 'C', 'label': 'H^2'},
                           {'id': 'D', 'label': '2 * H'}],
            'q2': 'What distinguishes a leaf node from an internal node in a binary tree?',
            'q2_ans': 'A',
            'q2_exp': {   'A': 'Correct! By definition, terminal leaf nodes have no children: `node.left is None and '
                               'node.right is None`.',
                          'B': 'Incorrect: Leaf nodes can store any value.',
                          'C': 'Incorrect: The root has no parent, but can have children.',
                          'D': 'Incorrect: A node with a child is an internal node.'},
            'q2_opts': [   {'id': 'A', 'label': 'A leaf node has both left and right pointers equal to None'},
                           {'id': 'B', 'label': 'A leaf node has value 0'},
                           {'id': 'C', 'label': 'A leaf node is the root of the tree'},
                           {'id': 'D', 'label': 'A leaf node has only a left child'}],
            'recap': [   {   'concept': 'Recursive Self-Similarity',
                             'naiveIntuition': 'Iterate through tree with index loops',
                             'pythonReality': 'Each child node is itself the root of an independent subtree, making '
                                              'recursive decomposition the natural paradigm'},
                         {   'concept': 'Branching Complexity',
                             'naiveIntuition': 'Binary trees are always fast',
                             'pythonReality': 'Degenerate trees (skewed chains) degrade to O(N) linear lists; balanced '
                                              'trees guarantee O(log N) depth'}],
            'sample_code': 'class TreeNode:\n'
                           '    def __init__(self, val=0, left=None, right=None):\n'
                           '        self.val = val\n'
                           '        self.left = left\n'
                           '        self.right = right\n'
                           '\n'
                           'root = TreeNode(1, TreeNode(2), TreeNode(3))\n'
                           "print('Root:', root.val, 'Left:', root.left.val, 'Right:', root.right.val)",
            'solution': 'class TreeNode:\n'
                        '    def __init__(self, val=0, left=None, right=None):\n'
                        '        self.val = val\n'
                        '        self.left = left\n'
                        '        self.right = right\n'
                        '\n'
                        'def count_leaves(root: TreeNode) -> int:\n'
                        '    if not root:\n'
                        '        return 0\n'
                        '    if not root.left and not root.right:\n'
                        '        return 1\n'
                        '    return count_leaves(root.left) + count_leaves(root.right)\n'
                        '\n'
                        't = TreeNode(1, TreeNode(2), TreeNode(3, TreeNode(4), TreeNode(5)))\n'
                        "print('Leaf count:', count_leaves(t))\n",
            'starter': 'class TreeNode:\n'
                       '    def __init__(self, val=0, left=None, right=None):\n'
                       '        self.val = val\n'
                       '        self.left = left\n'
                       '        self.right = right\n'
                       '\n'
                       'def count_leaves(root: TreeNode) -> int:\n'
                       '    # TODO: Recursively count leaf nodes\n'
                       '    return 0\n'
                       '\n'
                       '# Tree: 1 -> left: 2, right: 3 -> left: 4, right: 5\n'
                       't = TreeNode(1, TreeNode(2), TreeNode(3, TreeNode(4), TreeNode(5)))\n'
                       "print('Leaf count:', count_leaves(t))\n",
            'summary': 'Binary Trees organize hierarchical data where each TreeNode contains a value and references to '
                       'at most two children (left and right).',
            'takeaway': 'Tree algorithms mirror the recursive anatomy of tree nodes.'},
    97: {   'hint': 'Helper dfs(node): if not node return; dfs(node.left); res.append(node.val); dfs(node.right). Call '
                    'dfs(root) and return res.',
            'mechanics': 'Pre-order (Root, Left, Right): used for tree cloning and serialization. In-order (Left, '
                         'Root, Right): yields monotonically sorted values in Binary Search Trees. Post-order (Left, '
                         'Right, Root): used for bottom-up cleanup, deletions, and subtree metric calculations.',
            'patterns': ['In-order: [1, 2, 3]'],
            'practice_task': 'Implement In-order traversal and collect values in an array.',
            'q1': "Which traversal order processes a node's left and right subtrees BEFORE processing the node itself?",
            'q1_ans': 'A',
            'q1_exp': {   'A': 'Correct! Post-order evaluates both children before aggregating results at the parent, '
                               'making it ideal for calculating subtree heights, directory disk usage, and bottom-up '
                               'DP.',
                          'B': 'Incorrect: Pre-order visits root first.',
                          'C': 'Incorrect: In-order visits root between left and right.',
                          'D': 'Incorrect: Level-order visits nodes by depth.'},
            'q1_opts': [   {'id': 'A', 'label': 'Post-order traversal (Left, Right, Root)'},
                           {'id': 'B', 'label': 'Pre-order traversal (Root, Left, Right)'},
                           {'id': 'C', 'label': 'In-order traversal (Left, Root, Right)'},
                           {'id': 'D', 'label': 'Level-order traversal'}],
            'q2': 'What sequence is produced by an in-order traversal of a valid Binary Search Tree (BST)?',
            'q2_ans': 'A',
            'q2_exp': {   'A': 'Correct! Because BST invariant enforces `left < root < right`, in-order traversal '
                               '(Left, Root, Right) guarantees elements are visited in strictly ascending sorted '
                               'order.',
                          'B': 'Incorrect: Ascending, not descending.',
                          'C': 'Incorrect: The order is strictly deterministic.',
                          'D': 'Incorrect: Depth is not flattened into reverse level order.'},
            'q2_opts': [   {'id': 'A', 'label': 'Strictly ascending sorted order'},
                           {'id': 'B', 'label': 'Strictly descending sorted order'},
                           {'id': 'C', 'label': 'Random order'},
                           {'id': 'D', 'label': 'Reverse level order'}],
            'recap': [   {   'concept': 'Traversal Positioning',
                             'naiveIntuition': 'Traversals visit nodes in different orders on the tree',
                             'pythonReality': 'The call stack traverses identical paths; only the moment of processing '
                                              'node.val changes relative to recursive calls'},
                         {   'concept': 'BST Monotonicity',
                             'naiveIntuition': 'Sort BST nodes after extraction',
                             'pythonReality': 'In-order traversal extracts sorted data in O(N) time with zero '
                                              'comparison sorting required'}],
            'sample_code': '# Tree Traversals\n'
                           'def in_order(node, res):\n'
                           '    if not node: return\n'
                           '    in_order(node.left, res)\n'
                           '    res.append(node.val)\n'
                           '    in_order(node.right, res)',
            'solution': 'class TreeNode:\n'
                        '    def __init__(self, val=0, left=None, right=None):\n'
                        '        self.val = val\n'
                        '        self.left = left\n'
                        '        self.right = right\n'
                        '\n'
                        'def inorder_traversal(root: TreeNode) -> list[int]:\n'
                        '    res = []\n'
                        '    def dfs(node):\n'
                        '        if not node:\n'
                        '            return\n'
                        '        dfs(node.left)\n'
                        '        res.append(node.val)\n'
                        '        dfs(node.right)\n'
                        '    dfs(root)\n'
                        '    return res\n'
                        '\n'
                        'bst = TreeNode(2, TreeNode(1), TreeNode(3))\n'
                        "print('In-order:', inorder_traversal(bst))\n",
            'starter': 'class TreeNode:\n'
                       '    def __init__(self, val=0, left=None, right=None):\n'
                       '        self.val = val\n'
                       '        self.left = left\n'
                       '        self.right = right\n'
                       '\n'
                       'def inorder_traversal(root: TreeNode) -> list[int]:\n'
                       '    # TODO: Collect node values in Left -> Root -> Right order\n'
                       '    return []\n'
                       '\n'
                       '# BST: 2 -> left: 1, right: 3\n'
                       'bst = TreeNode(2, TreeNode(1), TreeNode(3))\n'
                       "print('In-order:', inorder_traversal(bst))\n",
            'summary': 'Tree Traversals (Pre-order, In-order, Post-order) systematically visit all N nodes using '
                       'Depth-First Search (DFS), each defined by when the root is processed relative to its subtrees.',
            'takeaway': 'In-order traversal visits BST keys in strictly sorted order; post-order processes subtrees '
                        'before parents.'},
    98: {   'hint': 'Loop while curr or stack: while curr: stack.append(curr); curr = curr.left. curr = stack.pop(); '
                    'res.append(curr.val); curr = curr.right.',
            'mechanics': 'Iterative In-Order: push nodes onto stack while descending down the left spine (`curr = '
                         'curr.left`). When curr is None, pop from stack, process node value, and move to right child '
                         '(`curr = node.right`). The stack holds at most H nodes at any moment, guaranteeing O(N) time '
                         'and O(H) space.',
            'patterns': ['In-order: [1, 3, 2]'],
            'practice_task': 'Implement iterative in-order tree traversal using an explicit stack.',
            'q1': 'Why is an explicit stack loop preferred over recursion when processing unbalanced, deep trees in '
                  'production Python environments?',
            'q1_ans': 'A',
            'q1_exp': {   'A': "Correct! Python's interpreter terminates with RecursionError when stack depth exceeds "
                               'sys.getrecursionlimit() (typically 1000). Allocating an explicit stack on the heap '
                               'handles arbitrarily deep degenerate trees safely.',
                          'B': 'Incorrect: Visiting N nodes strictly requires O(N) operations.',
                          'C': 'Incorrect: In-order traversal yields sorted order on BSTs specifically, not arbitrary '
                               'binary trees.',
                          'D': 'Incorrect: Recursion is the natural representation of tree anatomy.'},
            'q1_opts': [   {   'id': 'A',
                               'label': 'Python enforces a default call stack limit (1000 frames); recursion on a '
                                        'skewed tree of depth 10,000 raises RecursionError, whereas an explicit '
                                        'heap-allocated list can hold millions of elements'},
                           {'id': 'B', 'label': 'Because iterative loops run in O(1) time'},
                           {'id': 'C', 'label': 'Because explicit stacks sort the tree nodes'},
                           {'id': 'D', 'label': 'Because recursion does not work on binary trees'}],
            'q2': 'In the iterative in-order template, when `curr` becomes `None`, what is the invariant governing the '
                  'next step?',
            'q2_ans': 'A',
            'q2_exp': {   'A': 'Correct! When `curr` is None, we have reached the bottom of the current left branch. '
                               'The top of the stack is the immediate parent, ready to be processed before exploring '
                               'its right branch.',
                          'B': 'Incorrect: Traversal completes only when BOTH curr is None AND stack is empty.',
                          'C': 'Incorrect: Resetting to root causes infinite loops.',
                          'D': 'Incorrect: Clearing the stack loses remaining parent nodes.'},
            'q2_opts': [   {   'id': 'A',
                               'label': 'The node at the top of the stack is the leftmost unvisited ancestor whose '
                                        'left subtree is completely exhausted; popping it visits that node before '
                                        'moving to its right child'},
                           {'id': 'B', 'label': 'The tree traversal is finished and the loop must break'},
                           {'id': 'C', 'label': 'curr must be reset to root'},
                           {'id': 'D', 'label': 'stack must be cleared'}],
            'recap': [   {   'concept': 'Left-Spine Descent',
                             'naiveIntuition': 'Pop and push simultaneously',
                             'pythonReality': 'Pushing all left children before processing matches recursive '
                                              'call-stack activation records'},
                         {   'concept': 'Heap-Allocated Safety',
                             'naiveIntuition': 'Recursion is always better in Python',
                             'pythonReality': 'Deep recursion risks call stack exhaustion; explicit loops on heap '
                                              'memory provide enterprise resilience'}],
            'sample_code': '# Iterative In-Order Traversal via Explicit Stack\n'
                           'def inorder_iterative(root):\n'
                           '    res, stack = [], []\n'
                           '    curr = root\n'
                           '    while curr or stack:\n'
                           '        while curr:\n'
                           '            stack.append(curr)\n'
                           '            curr = curr.left\n'
                           '        curr = stack.pop()\n'
                           '        res.append(curr.val)\n'
                           '        curr = curr.right\n'
                           '    return res',
            'solution': 'class TreeNode:\n'
                        '    def __init__(self, val=0, left=None, right=None):\n'
                        '        self.val = val\n'
                        '        self.left = left\n'
                        '        self.right = right\n'
                        '\n'
                        'def inorder_traversal(root: TreeNode) -> list[int]:\n'
                        '    res, stack = [], []\n'
                        '    curr = root\n'
                        '    while curr or stack:\n'
                        '        while curr:\n'
                        '            stack.append(curr)\n'
                        '            curr = curr.left\n'
                        '        curr = stack.pop()\n'
                        '        res.append(curr.val)\n'
                        '        curr = curr.right\n'
                        '    return res\n'
                        '\n'
                        't = TreeNode(1, None, TreeNode(2, TreeNode(3), None))\n'
                        "print('In-order:', inorder_traversal(t))\n",
            'starter': 'class TreeNode:\n'
                       '    def __init__(self, val=0, left=None, right=None):\n'
                       '        self.val = val\n'
                       '        self.left = left\n'
                       '        self.right = right\n'
                       '\n'
                       'def inorder_traversal(root: TreeNode) -> list[int]:\n'
                       '    # TODO: Implement iterative in-order using explicit stack\n'
                       '    return []\n'
                       '\n'
                       '# Tree: 1 -> right: 2 (left: 3) -> In-order: [1, 3, 2]\n'
                       't = TreeNode(1, None, TreeNode(2, TreeNode(3), None))\n'
                       "print('In-order:', inorder_traversal(t))\n",
            'summary': 'Iterative Tree Traversals simulate the system recursion call stack using an explicit Python '
                       'list to prevent RecursionError on skewed trees of depth up to N.',
            'takeaway': "Simulating the call stack with a while loop and explicit list eliminates Python's recursion "
                        'limit while matching DFS performance.'},
    99: {   'hint': 'Check if not root return []. q = deque([root]). While q: level = [], loop range(len(q)): popleft, '
                    'append val, push left/right children if non-null. Append level to res.',
            'mechanics': 'Initialize `queue = deque([root])`. While queue is non-empty: capture `level_size = '
                         'len(queue)`. Pop exactly `level_size` nodes for current level, append their values to '
                         'current level array, and enqueue their non-null children. Advance to next level.',
            'patterns': ['Levels: [[3], [9, 20], [15, 7]]'],
            'practice_task': 'Return the level-order traversal of a binary tree as a list of lists of integers.',
            'q1': 'Why is `for _ in range(len(q)):` used inside the `while q:` loop in level-order traversal?',
            'q1_ans': 'A',
            'q1_exp': {   'A': 'Correct! Evaluating `len(q)` at the start of the loop captures exactly the nodes on '
                               'the current level. Enqueuing children during the loop grows `q`, but the loop runs '
                               'only for the pre-calculated count.',
                          'B': 'Incorrect: The while loop condition prevents infinite looping.',
                          'C': 'Incorrect: Range is standard Python iteration.',
                          'D': 'Incorrect: Level nodes maintain left-to-right discovery order, not sorted.'},
            'q1_opts': [   {   'id': 'A',
                               'label': 'It snapshots the exact count of nodes belonging to the current depth level '
                                        'before any children of the next level are enqueued'},
                           {'id': 'B', 'label': 'To prevent an infinite loop'},
                           {'id': 'C', 'label': 'Because range() is required by Python deques'},
                           {'id': 'D', 'label': 'To sort the nodes in each level'}],
            'q2': 'What is the maximum space complexity of level-order traversal in a complete binary tree of N nodes?',
            'q2_ans': 'A',
            'q2_exp': {   'A': 'Correct! In a full binary tree, the last level contains ceil(N / 2) nodes. The queue '
                               'holds all leaf nodes simultaneously, consuming O(N) auxiliary space.',
                          'B': 'Incorrect: The queue stores entire levels in memory.',
                          'C': 'Incorrect: O(log N) is the space complexity for DFS call stack, not BFS queue.',
                          'D': 'Incorrect: Total nodes across all levels is N.'},
            'q2_opts': [   {   'id': 'A',
                               'label': 'O(N) space, because the bottom leaf level contains approximately N / 2 nodes'},
                           {'id': 'B', 'label': 'O(1) space'},
                           {'id': 'C', 'label': 'O(log N) space'},
                           {'id': 'D', 'label': 'O(N^2) space'}],
            'recap': [   {   'concept': 'BFS Snapshot Pattern',
                             'naiveIntuition': 'Track depth with node tuples (node, depth)',
                             'pythonReality': 'Processing len(q) nodes in a nested loop groups levels naturally '
                                              'without storing depth metadata'},
                         {   'concept': 'DFS vs BFS Space Asymmetry',
                             'naiveIntuition': 'BFS and DFS use the same memory',
                             'pythonReality': 'DFS memory scales with height O(H) (call stack); BFS memory scales with '
                                              'width O(W) (queue), which can be O(N) in wide trees'}],
            'sample_code': 'from collections import deque\n'
                           'def level_order(root):\n'
                           '    if not root: return []\n'
                           '    q = deque([root])\n'
                           '    levels = []\n'
                           '    while q:\n'
                           '        level = []\n'
                           '        for _ in range(len(q)):\n'
                           '            node = q.popleft()\n'
                           '            level.append(node.val)\n'
                           '            if node.left: q.append(node.left)\n'
                           '            if node.right: q.append(node.right)\n'
                           '        levels.append(level)\n'
                           '    return levels',
            'solution': 'from collections import deque\n'
                        '\n'
                        'class TreeNode:\n'
                        '    def __init__(self, val=0, left=None, right=None):\n'
                        '        self.val = val\n'
                        '        self.left = left\n'
                        '        self.right = right\n'
                        '\n'
                        'def get_levels(root: TreeNode) -> list[list[int]]:\n'
                        '    if not root:\n'
                        '        return []\n'
                        '    q = deque([root])\n'
                        '    res = []\n'
                        '    while q:\n'
                        '        level = []\n'
                        '        for _ in range(len(q)):\n'
                        '            node = q.popleft()\n'
                        '            level.append(node.val)\n'
                        '            if node.left:\n'
                        '                q.append(node.left)\n'
                        '            if node.right:\n'
                        '                q.append(node.right)\n'
                        '        res.append(level)\n'
                        '    return res\n'
                        '\n'
                        't = TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))\n'
                        "print('Levels:', get_levels(t))\n",
            'starter': 'from collections import deque\n'
                       '\n'
                       'class TreeNode:\n'
                       '    def __init__(self, val=0, left=None, right=None):\n'
                       '        self.val = val\n'
                       '        self.left = left\n'
                       '        self.right = right\n'
                       '\n'
                       'def get_levels(root: TreeNode) -> list[list[int]]:\n'
                       '    # TODO: Implement BFS level-order traversal\n'
                       '    return []\n'
                       '\n'
                       '# Tree: 3 -> left: 9, right: 20 (left: 15, right: 7)\n'
                       't = TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))\n'
                       "print('Levels:', get_levels(t))\n",
            'summary': 'Breadth-First Search (Level-Order Traversal) explores trees level by level horizontally using '
                       'a FIFO queue (`collections.deque`), batching nodes by depth.',
            'takeaway': 'Freezing level_size at each outer iteration cleanly separates tree levels in O(N) time.'},
    100: {   'hint': 'Define nonlocal max_d = 0. In helper height(node): if not node return 0. lh = height(node.left), '
                     'rh = height(node.right). max_d = max(max_d, lh + rh). Return 1 + max(lh, rh). Return max_d after '
                     'height(root).',
             'mechanics': 'The longest path passing through node `curr` is `height(curr.left) + height(curr.right)`. A '
                          'naive algorithm calling `height()` for each node takes O(N^2). A post-order DFS updates '
                          '`self.max_diameter = max(self.max_diameter, left_h + right_h)` and returns `1 + max(left_h, '
                          'right_h)` in a single O(N) pass.',
             'patterns': ['Diameter: 3'],
             'practice_task': 'Calculate the diameter (number of edges on longest path) of a binary tree.',
             'q1': 'Does the longest path (diameter) of a binary tree always pass through the root node?',
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! If the left subtree is very deep and bushy while the right subtree is a '
                                'single leaf, the two deepest leaves within the left subtree can form a diameter '
                                'longer than any path through the root.',
                           'B': 'Incorrect: Diameter is defined between ANY two nodes.',
                           'C': 'Incorrect: Even in balanced trees it can bypass root if heights align.',
                           'D': 'Incorrect: Root presence is not required.'},
             'q1_opts': [   {   'id': 'A',
                                'label': 'No, the longest path might reside entirely within a deep left or right '
                                         'subtree without passing through the root'},
                            {'id': 'B', 'label': 'Yes, diameter must always pass through the root'},
                            {'id': 'C', 'label': 'Only in balanced trees'},
                            {'id': 'D', 'label': 'Only if root has two children'}],
             'q2': 'Why does combining height calculation with global diameter tracking run in O(N) time?',
             'q2_ans': 'A',
             'q2_exp': {   'A': 'Correct! Post-order DFS visits each of the N nodes once, doing O(1) additions and '
                                'comparisons per node. Total time is strictly O(N).',
                           'B': 'Incorrect: No array conversion is performed.',
                           'C': 'Incorrect: Pure recursion without memo table.',
                           'D': 'Incorrect: Diameter depends dynamically on tree topology.'},
             'q2_opts': [   {   'id': 'A',
                                'label': 'Every node is visited exactly once in post-order, computing both local '
                                         'height and diameter contribution in O(1) operations'},
                            {'id': 'B', 'label': 'Because the tree is converted into an array'},
                            {'id': 'C', 'label': 'Because it uses memoization on node values'},
                            {'id': 'D', 'label': 'Because diameter is always constant'}],
             'recap': [   {   'concept': 'Dual Role Recursion',
                              'naiveIntuition': 'Separate height function from diameter search (O(N^2))',
                              'pythonReality': 'Returning local height up the call stack while updating global '
                                               'diameter achieves linear O(N) performance'},
                          {   'concept': 'Edge Count Invariant',
                              'naiveIntuition': 'Diameter is node count',
                              'pythonReality': 'Diameter is traditionally measured in edges between nodes (nodes on '
                                               'path - 1); lh + rh yields edges directly'}],
             'sample_code': '# Diameter in O(N)\n'
                            'class Solution:\n'
                            '    def diameter_of_binary_tree(self, root):\n'
                            '        self.diameter = 0\n'
                            '        def height(node):\n'
                            '            if not node: return 0\n'
                            '            lh = height(node.left)\n'
                            '            rh = height(node.right)\n'
                            '            self.diameter = max(self.diameter, lh + rh)\n'
                            '            return 1 + max(lh, rh)\n'
                            '        height(root)\n'
                            '        return self.diameter',
             'solution': 'class TreeNode:\n'
                         '    def __init__(self, val=0, left=None, right=None):\n'
                         '        self.val = val\n'
                         '        self.left = left\n'
                         '        self.right = right\n'
                         '\n'
                         'def tree_diameter(root: TreeNode) -> int:\n'
                         '    max_d = 0\n'
                         '    def height(node):\n'
                         '        nonlocal max_d\n'
                         '        if not node:\n'
                         '            return 0\n'
                         '        lh = height(node.left)\n'
                         '        rh = height(node.right)\n'
                         '        max_d = max(max_d, lh + rh)\n'
                         '        return 1 + max(lh, rh)\n'
                         '    height(root)\n'
                         '    return max_d\n'
                         '\n'
                         't = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3))\n'
                         "print('Diameter:', tree_diameter(t))\n",
             'starter': 'class TreeNode:\n'
                        '    def __init__(self, val=0, left=None, right=None):\n'
                        '        self.val = val\n'
                        '        self.left = left\n'
                        '        self.right = right\n'
                        '\n'
                        'def tree_diameter(root: TreeNode) -> int:\n'
                        '    # TODO: Implement single-pass O(N) diameter calculation\n'
                        '    return 0\n'
                        '\n'
                        '# 1 -> left: 2 (left: 4, right: 5), right: 3. Longest path: 4-2-1-3 or 5-2-1-3 (3 edges)\n'
                        't = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3))\n'
                        "print('Diameter:', tree_diameter(t))\n",
             'summary': 'Diameter of a Binary Tree is the length of the longest path between any two nodes, computed '
                        'in O(N) time by returning subtree height while updating a global diameter.',
             'takeaway': 'Return one value to the caller while updating a global optimal metric to avoid O(N^2) '
                         'recalculations.'},
    101: {   'hint': 'Helper validate(node, low, high): if not node: return True. If not (low < node.val < high): '
                     'return False. Return validate(node.left, low, node.val) and validate(node.right, node.val, '
                     'high).',
             'mechanics': 'A naive check `root.left.val < root.val < root.right.val` is INVALID because it only checks '
                          'local children, missing violations deep in subtrees. Validating a BST requires propagating '
                          'a valid range `(min_val, max_val)`: left child range is `(min_val, root.val)` and right '
                          'child range is `(root.val, max_val)`.',
             'patterns': ['T1 Valid: True', 'T2 Valid: False'],
             'practice_task': 'Validate whether a binary tree satisfies the Binary Search Tree invariant.',
             'q1': 'Why is checking only `node.left.val < node.val < node.right.val` insufficient to validate a BST?',
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! Consider root=10, root.left=5, root.left.right=15. Locally, 15 > 5 is valid, '
                                'but 15 > 10 violates the invariant that ALL nodes in the left subtree of 10 must be < '
                                '10.',
                           'B': 'Incorrect: While duplicates are excluded, the flaw is global scope violation.',
                           'C': 'Incorrect: None checks are trivially handled.',
                           'D': 'Incorrect: Python comparisons handle negative numbers uniformly.'},
             'q1_opts': [   {   'id': 'A',
                                'label': 'A node deep in the left subtree might have a value greater than an ancestor '
                                         'root, violating the global BST property while satisfying local child checks'},
                            {'id': 'B', 'label': 'Because binary search trees cannot have duplicate values'},
                            {'id': 'C', 'label': 'Because left child can be None'},
                            {'id': 'D', 'label': 'Because negative numbers break comparison'}],
             'q2': 'What is the alternative method to validate a BST using in-order traversal?',
             'q2_ans': 'A',
             'q2_exp': {   'A': 'Correct! Because in-order traversal of a valid BST visits keys in strictly increasing '
                                'order, tracking `prev_val` and asserting `node.val > prev_val` validates the BST in '
                                'O(N) time.',
                           'B': 'Incorrect: BSTs are not necessarily balanced.',
                           'C': 'Incorrect: Sum parity is unrelated to ordering.',
                           'D': 'Incorrect: Level-order is not sorted.'},
             'q2_opts': [   {   'id': 'A',
                                'label': 'Perform an in-order traversal and verify that every visited node is strictly '
                                         'greater than the previously visited node'},
                            {'id': 'B', 'label': 'Check if tree depth is log N'},
                            {'id': 'C', 'label': 'Sum all nodes and check if even'},
                            {'id': 'D', 'label': 'Level-order traversal must be sorted'}],
             'recap': [   {   'concept': 'Global Invariant Range',
                              'naiveIntuition': 'Compare node with immediate children',
                              'pythonReality': 'Every node inherits bounding constraints (min, max) from all ancestors '
                                               'along its path from root'},
                          {   'concept': 'Strict Monotonicity',
                              'naiveIntuition': 'BST permits equal values on left or right',
                              'pythonReality': 'Standard BST definition enforces strictly less (<) and strictly '
                                               'greater (>); duplicates require frequency counters'}],
             'sample_code': '# Valid BST using Range Propagation\n'
                            'def is_valid_bst(root):\n'
                            '    def validate(node, low, high):\n'
                            '        if not node: return True\n'
                            '        if not (low < node.val < high): return False\n'
                            '        return validate(node.left, low, node.val) and validate(node.right, node.val, '
                            'high)\n'
                            "    return validate(root, float('-inf'), float('inf'))",
             'solution': 'class TreeNode:\n'
                         '    def __init__(self, val=0, left=None, right=None):\n'
                         '        self.val = val\n'
                         '        self.left = left\n'
                         '        self.right = right\n'
                         '\n'
                         'def is_valid_bst(root: TreeNode) -> bool:\n'
                         '    def validate(node, low, high):\n'
                         '        if not node:\n'
                         '            return True\n'
                         '        if not (low < node.val < high):\n'
                         '            return False\n'
                         '        return validate(node.left, low, node.val) and validate(node.right, node.val, high)\n'
                         "    return validate(root, float('-inf'), float('inf'))\n"
                         '\n'
                         't1 = TreeNode(2, TreeNode(1), TreeNode(3))\n'
                         't2 = TreeNode(5, TreeNode(1), TreeNode(4, TreeNode(3), TreeNode(6)))\n'
                         "print('T1 Valid:', is_valid_bst(t1))\n"
                         "print('T2 Valid:', is_valid_bst(t2))\n",
             'starter': 'class TreeNode:\n'
                        '    def __init__(self, val=0, left=None, right=None):\n'
                        '        self.val = val\n'
                        '        self.left = left\n'
                        '        self.right = right\n'
                        '\n'
                        'def is_valid_bst(root: TreeNode) -> bool:\n'
                        '    # TODO: Validate BST using range propagation\n'
                        '    return False\n'
                        '\n'
                        '# Valid: 2 (1, 3)\n'
                        't1 = TreeNode(2, TreeNode(1), TreeNode(3))\n'
                        '# Invalid: 5 (1, 4 with left: 3, right: 6) -> 3 is in right subtree of 5 but < 5\n'
                        't2 = TreeNode(5, TreeNode(1), TreeNode(4, TreeNode(3), TreeNode(6)))\n'
                        "print('T1 Valid:', is_valid_bst(t1))\n"
                        "print('T2 Valid:', is_valid_bst(t2))\n",
             'summary': 'Binary Search Tree (BST) Invariant requires that for every node, ALL nodes in its left '
                        'subtree are strictly smaller (`val < root.val`) and ALL nodes in its right subtree are '
                        'strictly greater (`val > root.val`).',
             'takeaway': 'BST validation requires bounding entire subtrees with inherited (min_val, max_val) ranges.'},
    102: {   'hint': 'if not root return TreeNode(val). If val < root.val: root.left = insert_bst(root.left, val) '
                     'else: root.right = insert_bst(root.right, val). Return root.',
             'mechanics': 'Search: if `target < val` steer left, elif `target > val` steer right, else found. Insert: '
                          "traverse to empty spot and attach new node. Delete node with 2 children: replace node's "
                          'value with its In-order Successor (smallest value in right subtree), then delete the '
                          'successor from the right subtree.',
             'patterns': ['Inorder after insert 5: [2, 4, 5, 7]'],
             'practice_task': 'Insert a value into a Binary Search Tree and return the root.',
             'q1': 'Why is the In-order Successor (minimum node in the right subtree) used to replace a deleted node '
                   'with two children?',
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! The in-order successor is the immediately next key in sorted order. Placing '
                                'it at the deleted position maintains the property that left subtree < new_val < right '
                                'subtree.',
                           'B': 'Incorrect: The successor can have a right child (though it cannot have a left child).',
                           'C': 'Incorrect: Tree nodes are non-contiguous heap objects.',
                           'D': 'Incorrect: Successor selection is an explicit algorithmic step.'},
             'q1_opts': [   {   'id': 'A',
                                'label': 'It is guaranteed to be greater than all nodes in the left subtree and '
                                         'smaller than all remaining nodes in the right subtree, preserving the BST '
                                         'invariant'},
                            {'id': 'B', 'label': 'Because it has no children at all'},
                            {'id': 'C', 'label': 'Because it is stored at index 0 in memory'},
                            {'id': 'D', 'label': 'Because Python automatically selects it'}],
             'q2': 'Can the In-order Successor of a node ever have a left child?',
             'q2_ans': 'A',
             'q2_exp': {   'A': 'Correct! Finding the minimum in a subtree follows left pointers until `curr.left is '
                                'None`. Hence, the in-order successor is guaranteed to have at most ONE child (a right '
                                'child).',
                           'B': 'Incorrect: Binary tree nodes have at most 1 left child.',
                           'C': 'Incorrect: Minimum property guarantees curr.left is None.',
                           'D': 'Incorrect: True for all BSTs.'},
             'q2_opts': [   {   'id': 'A',
                                'label': 'No, because any left child would have a smaller value, contradicting the '
                                         'fact that the successor is the minimum node in that subtree'},
                            {'id': 'B', 'label': 'Yes, it can have up to 2 left children'},
                            {'id': 'C', 'label': 'Yes, if the tree is unbalanced'},
                            {'id': 'D', 'label': 'Only in AVL trees'}],
             'recap': [   {   'concept': 'Search Steering Property',
                              'naiveIntuition': 'Search both subtrees like normal binary tree',
                              'pythonReality': 'Comparing target with root.val halves the search path at every step, '
                                               'taking O(H) time without inspecting both sides'},
                          {   'concept': 'Successor Simplicity',
                              'naiveIntuition': 'Deleting a 2-child node requires restructuring the entire tree',
                              'pythonReality': "Copying the successor's value and deleting the successor reduces "
                                               '2-child deletion to trivial 0-or-1 child deletion'}],
             'sample_code': '# BST Insertion\n'
                            'def insert_into_bst(root, val):\n'
                            '    if not root: return TreeNode(val)\n'
                            '    if val < root.val: root.left = insert_into_bst(root.left, val)\n'
                            '    else: root.right = insert_into_bst(root.right, val)\n'
                            '    return root',
             'solution': 'class TreeNode:\n'
                         '    def __init__(self, val=0, left=None, right=None):\n'
                         '        self.val = val\n'
                         '        self.left = left\n'
                         '        self.right = right\n'
                         '\n'
                         'def insert_bst(root: TreeNode, val: int) -> TreeNode:\n'
                         '    if not root:\n'
                         '        return TreeNode(val)\n'
                         '    if val < root.val:\n'
                         '        root.left = insert_bst(root.left, val)\n'
                         '    else:\n'
                         '        root.right = insert_bst(root.right, val)\n'
                         '    return root\n'
                         '\n'
                         'def inorder(node):\n'
                         '    return inorder(node.left) + [node.val] + inorder(node.right) if node else []\n'
                         '\n'
                         'root = TreeNode(4, TreeNode(2), TreeNode(7))\n'
                         'insert_bst(root, 5)\n'
                         "print('Inorder after insert 5:', inorder(root))\n",
             'starter': 'class TreeNode:\n'
                        '    def __init__(self, val=0, left=None, right=None):\n'
                        '        self.val = val\n'
                        '        self.left = left\n'
                        '        self.right = right\n'
                        '\n'
                        'def insert_bst(root: TreeNode, val: int) -> TreeNode:\n'
                        '    # TODO: Recursively insert val into BST\n'
                        '    return root\n'
                        '\n'
                        'def inorder(node):\n'
                        '    return inorder(node.left) + [node.val] + inorder(node.right) if node else []\n'
                        '\n'
                        'root = TreeNode(4, TreeNode(2), TreeNode(7))\n'
                        'insert_bst(root, 5)\n'
                        "print('Inorder after insert 5:', inorder(root))\n",
             'summary': 'BST Search, Insertion, and Deletion operate in O(H) time by steering left or right, with '
                        'deletion managing 3 structural cases: leaf node, single child, and two children.',
             'takeaway': 'Two-child deletion preserves the BST invariant by splicing the in-order successor.'},
    103: {   'hint': 'if not root or root == p or root == q: return root. left = find_lca(root.left, p, q); right = '
                     'find_lca(root.right, p, q). If left and right: return root. Return left or right.',
             'mechanics': 'If `root in (None, p, q)`: return root. Search left and right subtrees: `left = '
                          'LCA(root.left, p, q)` and `right = LCA(root.right, p, q)`. If both `left` and `right` '
                          'return non-null, `root` is the LCA! If only one is non-null, propagate that non-null node '
                          'up.',
             'patterns': ['LCA(5, 1): 3', 'LCA(5, 2): 5'],
             'practice_task': 'Find the Lowest Common Ancestor of two given nodes in a binary tree.',
             'q1': 'If `left` returns node `p` and `right` returns node `q`, why is `root` guaranteed to be their '
                   'Lowest Common Ancestor?',
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! Since one target resides in the left subtree and the other resides in the '
                                'right subtree, no deeper descendant node can be an ancestor to both. The current node '
                                'is the lowest common point.',
                           'B': 'Incorrect: Ancestor can be a deeper node than tree root.',
                           'C': 'Incorrect: Only BSTs have value ordering.',
                           'D': 'Incorrect: Targets can reside at different heights.'},
             'q1_opts': [   {   'id': 'A',
                                'label': 'Because `p` and `q` are located in different subtrees branching directly off '
                                         '`root`, making `root` their lowest mutual convergence point'},
                            {'id': 'B', 'label': 'Because `root` is always the LCA for any pair'},
                            {'id': 'C', 'label': 'Because left is smaller than right in all binary trees'},
                            {'id': 'D', 'label': 'Because p and q have identical heights'}],
             'q2': 'What happens in the LCA algorithm if node `q` is a direct descendant of node `p`?',
             'q2_ans': 'A',
             'q2_exp': {   'A': "Correct! The base case `if root == p:` returns `p`. Since `q` is inside `p`'s "
                                'subtree, `p` will bubble up as the sole non-null return value to the top, correctly '
                                'identifying `p` as the LCA.',
                           'B': 'Incorrect: A non-null ancestor is found.',
                           'C': 'Incorrect: Trees are acyclic.',
                           'D': 'Incorrect: Returns the lowest ancestor p.'},
             'q2_opts': [   {   'id': 'A',
                                'label': 'The algorithm returns `p` immediately when visiting `p`, because `p` is its '
                                         'own ancestor and the search does not need to delve deeper'},
                            {'id': 'B', 'label': 'The algorithm returns None'},
                            {'id': 'C', 'label': 'An infinite recursion occurs'},
                            {'id': 'D', 'label': 'The algorithm returns root'}],
             'recap': [   {   'concept': 'Convergence Bubbling',
                              'naiveIntuition': 'Store root-to-node paths in lists and compare prefixes',
                              'pythonReality': 'Bottom-up DFS bubbles found references up the stack, identifying '
                                               'convergence directly in O(1) auxiliary stack frames'},
                          {   'concept': 'Ancestor Self-Inclusion',
                              'naiveIntuition': 'A node cannot be its own ancestor',
                              'pythonReality': 'In tree hierarchy, a node is considered a descendant of itself, '
                                               'allowing ancestor queries where p is an ancestor of q'}],
             'sample_code': '# Lowest Common Ancestor (Binary Tree)\n'
                            'def lowest_common_ancestor(root, p, q):\n'
                            '    if not root or root == p or root == q:\n'
                            '        return root\n'
                            '    left = lowest_common_ancestor(root.left, p, q)\n'
                            '    right = lowest_common_ancestor(root.right, p, q)\n'
                            '    if left and right: return root # Both sides found\n'
                            '    return left or right          # Pass up whichever was found',
             'solution': 'class TreeNode:\n'
                         '    def __init__(self, val=0, left=None, right=None):\n'
                         '        self.val = val\n'
                         '        self.left = left\n'
                         '        self.right = right\n'
                         '\n'
                         'def find_lca(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:\n'
                         '    if not root or root == p or root == q:\n'
                         '        return root\n'
                         '    left = find_lca(root.left, p, q)\n'
                         '    right = find_lca(root.right, p, q)\n'
                         '    if left and right:\n'
                         '        return root\n'
                         '    return left or right\n'
                         '\n'
                         'n6 = TreeNode(6); n2 = TreeNode(2); n5 = TreeNode(5, n6, n2)\n'
                         'n0 = TreeNode(0); n8 = TreeNode(8); n1 = TreeNode(1, n0, n8)\n'
                         'root = TreeNode(3, n5, n1)\n'
                         '\n'
                         "print('LCA(5, 1):', find_lca(root, n5, n1).val)\n"
                         "print('LCA(5, 2):', find_lca(root, n5, n2).val)\n",
             'starter': 'class TreeNode:\n'
                        '    def __init__(self, val=0, left=None, right=None):\n'
                        '        self.val = val\n'
                        '        self.left = left\n'
                        '        self.right = right\n'
                        '\n'
                        'def find_lca(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:\n'
                        '    # TODO: Implement bottom-up LCA search\n'
                        '    return None\n'
                        '\n'
                        '# 3 -> left: 5 (left: 6, right: 2), right: 1 (left: 0, right: 8)\n'
                        'n6 = TreeNode(6); n2 = TreeNode(2); n5 = TreeNode(5, n6, n2)\n'
                        'n0 = TreeNode(0); n8 = TreeNode(8); n1 = TreeNode(1, n0, n8)\n'
                        'root = TreeNode(3, n5, n1)\n'
                        '\n'
                        '# LCA of 5 and 1 is 3\n'
                        "print('LCA(5, 1):', find_lca(root, n5, n1).val)\n"
                        '# LCA of 5 and 2 is 5\n'
                        "print('LCA(5, 2):', find_lca(root, n5, n2).val)\n",
             'summary': 'Lowest Common Ancestor (LCA) in a Binary Tree identifies the deepest node that has both nodes '
                        'p and q as descendants using bottom-up subtree search in O(N) time.',
             'takeaway': 'When left and right subtrees each return one of the target nodes, the current root is their '
                         'Lowest Common Ancestor.'},
    104: {   'hint': "In serialize: if not node res.append('#'); else append str(node.val), dfs(left), dfs(right). "
                     "Return ','.join(res). In deserialize: tokens = iter(data.split(',')). Helper dfs(): val = "
                     "next(tokens); if val == '#' return None. node = TreeNode(int(val)), left = dfs(), right = dfs(). "
                     'Return node.',
             'mechanics': "Serialize: pre-order traversal writing `node.val` and `'#'` for `None`, joined by commas. "
                          "Deserialize: split string into token queue/iterator. For each token: if `'#'` return None; "
                          'else create `node = TreeNode(int(token))`, then recursively construct `node.left` and '
                          '`node.right`.',
             'patterns': ['Serialized: 1,2,#,#,3,4,#,#,5,#,#', 'Rebuilt root: 1 Rebuilt right left: 4'],
             'practice_task': 'Serialize a binary tree to string and deserialize it back, verifying structure '
                              'preservation.',
             'q1': "Why does preorder traversal with null markers ('#') allow unique reconstruction, whereas preorder "
                   'without null markers cannot?',
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! Without null markers, [1, 2] could mean 1 has left child 2, or 1 has right '
                                "child 2. Recording '1,2,#,#,#' unambiguously pins down the exact empty slots.",
                           'B': 'Incorrect: Python strings readily store digits.',
                           'C': 'Incorrect: Commas act as delimiters, not sorters.',
                           'D': 'Incorrect: Null markers increase length but guarantee uniqueness.'},
             'q1_opts': [   {   'id': 'A',
                                'label': 'Null markers explicitly record when child branches terminate, removing all '
                                         'ambiguity about node leaf/internal status'},
                            {'id': 'B', 'label': 'Because strings cannot store numbers'},
                            {'id': 'C', 'label': 'Because commas sort the values'},
                            {'id': 'D', 'label': 'It makes the string shorter'}],
             'q2': 'What is the time complexity of deserializing a tree string of N nodes using an iterator?',
             'q2_ans': 'A',
             'q2_exp': {   'A': 'Correct! Splitting takes O(N) time. The iterator advances forward monotonically with '
                                'each node creation, consuming 2N + 1 tokens total (N nodes + N + 1 null sentinels). '
                                'Overall: O(N).',
                           'B': 'Incorrect: No nested token scanning occurs.',
                           'C': 'Incorrect: No sorting is involved.',
                           'D': 'Incorrect: Linear traversal through tokens.'},
             'q2_opts': [   {'id': 'A', 'label': 'O(N), because each token is consumed once by `next(tokens)` in O(1)'},
                            {'id': 'B', 'label': 'O(N^2)'},
                            {'id': 'C', 'label': 'O(N log N)'},
                            {'id': 'D', 'label': 'O(2^N)'}],
             'recap': [   {   'concept': 'State Marshalling',
                              'naiveIntuition': 'Save pointers to disk directly',
                              'pythonReality': 'Memory addresses are ephemeral; flattening data structures into '
                                               'canonical text/binary formats is required for persistence and network '
                                               'transmission'},
                          {   'concept': 'Sentinel Disambiguation',
                              'naiveIntuition': 'Omit empty children to save space',
                              'pythonReality': 'Explicit null sentinels eliminate ambiguity, allowing single-pass '
                                               'linear reconstruction'}],
             'sample_code': '# Serialization & Deserialization\n'
                            'def serialize(root):\n'
                            '    res = []\n'
                            '    def dfs(node):\n'
                            "        if not node: res.append('#'); return\n"
                            '        res.append(str(node.val))\n'
                            '        dfs(node.left)\n'
                            '        dfs(node.right)\n'
                            '    dfs(root)\n'
                            "    return ','.join(res)\n"
                            '\n'
                            'def deserialize(data):\n'
                            "    tokens = iter(data.split(','))\n"
                            '    def dfs():\n'
                            '        val = next(tokens)\n'
                            "        if val == '#': return None\n"
                            '        node = TreeNode(int(val))\n'
                            '        node.left = dfs()\n'
                            '        node.right = dfs()\n'
                            '        return node\n'
                            '    return dfs()',
             'solution': 'class TreeNode:\n'
                         '    def __init__(self, val=0, left=None, right=None):\n'
                         '        self.val = val\n'
                         '        self.left = left\n'
                         '        self.right = right\n'
                         '\n'
                         'def serialize(root: TreeNode) -> str:\n'
                         '    res = []\n'
                         '    def dfs(node):\n'
                         '        if not node:\n'
                         "            res.append('#')\n"
                         '            return\n'
                         '        res.append(str(node.val))\n'
                         '        dfs(node.left)\n'
                         '        dfs(node.right)\n'
                         '    dfs(root)\n'
                         "    return ','.join(res)\n"
                         '\n'
                         'def deserialize(data: str) -> TreeNode:\n'
                         "    tokens = iter(data.split(','))\n"
                         '    def dfs():\n'
                         '        val = next(tokens)\n'
                         "        if val == '#':\n"
                         '            return None\n'
                         '        node = TreeNode(int(val))\n'
                         '        node.left = dfs()\n'
                         '        node.right = dfs()\n'
                         '        return node\n'
                         '    return dfs()\n'
                         '\n'
                         't = TreeNode(1, TreeNode(2), TreeNode(3, TreeNode(4), TreeNode(5)))\n'
                         's = serialize(t)\n'
                         "print('Serialized:', s)\n"
                         'rebuilt = deserialize(s)\n'
                         "print('Rebuilt root:', rebuilt.val, 'Rebuilt right left:', rebuilt.right.left.val)\n",
             'starter': 'class TreeNode:\n'
                        '    def __init__(self, val=0, left=None, right=None):\n'
                        '        self.val = val\n'
                        '        self.left = left\n'
                        '        self.right = right\n'
                        '\n'
                        'def serialize(root: TreeNode) -> str:\n'
                        "    # TODO: Serialize tree to comma-separated string with '#' for None\n"
                        "    return ''\n"
                        '\n'
                        'def deserialize(data: str) -> TreeNode:\n'
                        '    # TODO: Reconstruct tree from serialized string\n'
                        '    return None\n'
                        '\n'
                        't = TreeNode(1, TreeNode(2), TreeNode(3, TreeNode(4), TreeNode(5)))\n'
                        's = serialize(t)\n'
                        "print('Serialized:', s)\n"
                        'rebuilt = deserialize(s)\n'
                        "print('Rebuilt root:', rebuilt.val, 'Rebuilt right left:', rebuilt.right.left.val)\n",
             'summary': 'Tree Serialization converts a tree structure into a flat string representation using '
                        "delimiter tokens and null sentinels ('#'), and deserialization reconstructs the tree in O(N) "
                        'time.',
             'takeaway': 'Explicit null sentinels eliminate ambiguity, allowing single-pass preorder serialization and '
                         'deserialization.'},
    105: {   'hint': 'Loop while curr: if not curr.left: res.append(curr.val); curr = curr.right. Else pred = '
                     'curr.left; find rightmost node not equal to curr. If pred.right is None: thread pred.right = '
                     'curr; curr = curr.left. Else: unthread pred.right = None; res.append(curr.val); curr = '
                     'curr.right.',
             'mechanics': 'For node `curr`: if `curr.left is None`: visit `curr.val`, `curr = curr.right`. Else find '
                          'in-order predecessor `pred` (rightmost node of left subtree). If `pred.right is None`: '
                          'create thread `pred.right = curr` and move `curr = curr.left`. If `pred.right == curr`: '
                          'dismantle thread `pred.right = None`, visit `curr.val`, move `curr = curr.right`.',
             'patterns': ['Morris Inorder: [1, 2, 3]'],
             'practice_task': 'Implement Morris Traversal to retrieve in-order values with O(1) auxiliary space.',
             'q1': 'How does Morris Traversal achieve O(1) space without a stack or recursion?',
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! Every in-order predecessor has a null right pointer. Morris temporarily '
                                'points this null reference to `curr`, providing an O(1) return bridge back up to the '
                                'ancestor without a call stack.',
                           'B': 'Incorrect: Pointer threading is used, not value compression.',
                           'C': 'Incorrect: Python generators still require stack frames.',
                           'D': 'Incorrect: An array consumes O(N) auxiliary space.'},
             'q1_opts': [   {   'id': 'A',
                                'label': 'It temporarily utilizes the unused null right pointers of leaf nodes to '
                                         'store return paths back up to ancestors'},
                            {'id': 'B', 'label': 'It compresses node values into a 64-bit integer'},
                            {'id': 'C', 'label': 'It uses Python generator closures'},
                            {'id': 'D', 'label': 'It converts the tree into an array'}],
             'q2': 'Why must the temporary thread `pred.right = None` be removed during the second visit?',
             'q2_ans': 'A',
             'q2_exp': {   'A': "Correct! Tree traversals must not permanently mutate the caller's data structure. "
                                'Restoring `pred.right = None` leaves the tree in its original, unmodified state.',
                           'B': 'Incorrect: No new memory was allocated.',
                           'C': 'Incorrect: Python allows circular structures, but tree invariants forbid cycles.',
                           'D': 'Incorrect: Garbage collection is not triggered by restoring pointers.'},
             'q2_opts': [   {   'id': 'A',
                                'label': 'To restore the tree to its exact original structure and prevent infinite '
                                         'cycles during subsequent operations'},
                            {'id': 'B', 'label': 'To free heap memory'},
                            {'id': 'C', 'label': 'Because Python forbids circular references'},
                            {'id': 'D', 'label': 'To trigger garbage collection'}],
             'recap': [   {   'concept': 'Threaded Return Paths',
                              'naiveIntuition': 'O(1) space traversal is impossible because trees have no parent '
                                                'pointers',
                              'pythonReality': 'Repurposing dead null pointers as temporary escape ropes allows '
                                               'climbing back up without call stack memory'},
                          {   'concept': 'Two-Pass Edge Invariant',
                              'naiveIntuition': 'Finding predecessors makes Morris O(N^2)',
                              'pythonReality': 'Each edge is traversed at most 3 times (create thread, explore, '
                                               'dismantle thread), bounding total time to strictly O(N)'}],
             'sample_code': '# Morris In-Order Traversal in O(1) space\n'
                            'def morris_inorder(root):\n'
                            '    res = []\n'
                            '    curr = root\n'
                            '    while curr:\n'
                            '        if not curr.left:\n'
                            '            res.append(curr.val)\n'
                            '            curr = curr.right\n'
                            '        else:\n'
                            '            pred = curr.left\n'
                            '            while pred.right and pred.right != curr:\n'
                            '                pred = pred.right\n'
                            '            if not pred.right:\n'
                            '                pred.right = curr # Thread!\n'
                            '                curr = curr.left\n'
                            '            else:\n'
                            '                pred.right = None # Remove thread!\n'
                            '                res.append(curr.val)\n'
                            '                curr = curr.right\n'
                            '    return res',
             'solution': 'class TreeNode:\n'
                         '    def __init__(self, val=0, left=None, right=None):\n'
                         '        self.val = val\n'
                         '        self.left = left\n'
                         '        self.right = right\n'
                         '\n'
                         'def morris_traversal(root: TreeNode) -> list[int]:\n'
                         '    res = []\n'
                         '    curr = root\n'
                         '    while curr:\n'
                         '        if not curr.left:\n'
                         '            res.append(curr.val)\n'
                         '            curr = curr.right\n'
                         '        else:\n'
                         '            pred = curr.left\n'
                         '            while pred.right and pred.right != curr:\n'
                         '                pred = pred.right\n'
                         '            if not pred.right:\n'
                         '                pred.right = curr\n'
                         '                curr = curr.left\n'
                         '            else:\n'
                         '                pred.right = None\n'
                         '                res.append(curr.val)\n'
                         '                curr = curr.right\n'
                         '    return res\n'
                         '\n'
                         't = TreeNode(2, TreeNode(1), TreeNode(3))\n'
                         "print('Morris Inorder:', morris_traversal(t))\n",
             'starter': 'class TreeNode:\n'
                        '    def __init__(self, val=0, left=None, right=None):\n'
                        '        self.val = val\n'
                        '        self.left = left\n'
                        '        self.right = right\n'
                        '\n'
                        'def morris_traversal(root: TreeNode) -> list[int]:\n'
                        '    # TODO: Implement Morris in-order traversal using temporary pointer threading\n'
                        '    return []\n'
                        '\n'
                        '# 2 -> left: 1, right: 3\n'
                        't = TreeNode(2, TreeNode(1), TreeNode(3))\n'
                        "print('Morris Inorder:', morris_traversal(t))\n",
             'summary': 'Morris In-Order Traversal achieves O(N) time and strictly O(1) auxiliary space by temporarily '
                        'threading unused null pointers of in-order predecessors back to current nodes.',
             'takeaway': 'Morris traversal eliminates recursion stacks by threading leaf null pointers back to '
                         'ancestors.'},
    106: {   'hint': 'x = y.left; T2 = x.right; x.right = y; y.left = T2; return x.',
             'mechanics': 'Rotations update child references in O(1) time without altering in-order BST ordering. 4 '
                          'Cases: (1) Left-Left: single Right Rotation on root. (2) Right-Right: single Left Rotation '
                          'on root. (3) Left-Right: Left Rotation on left child, then Right Rotation on root. (4) '
                          'Right-Left: Right Rotation on right child, then Left Rotation on root.',
             'patterns': ['New root: 2 Left: 1 Right: 3'],
             'practice_task': 'Implement Right Rotation on a binary tree node and verify pointer reassignment.',
             'q1': 'In an AVL tree Right Rotation on node `y`, what happens to `x.right` (sub-tree T2)?',
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! Because T2 was originally in the right subtree of x, `T2 > x`. Because T2 '
                                "was in the left subtree of y, `T2 < y`. When y becomes x's right child, attaching T2 "
                                "as y's left child strictly preserves `x < T2 < y`.",
                           'B': 'Incorrect: All nodes are preserved.',
                           'C': "Incorrect: x's right child becomes y.",
                           'D': 'Incorrect: x becomes the new root of this subtree.'},
             'q1_opts': [   {   'id': 'A',
                                'label': 'It becomes the left child of node `y` (`y.left = T2`), correctly preserving '
                                         'the invariant `x < T2 < y`'},
                            {'id': 'B', 'label': 'It is deleted from the tree'},
                            {'id': 'C', 'label': 'It becomes the right child of `x`'},
                            {'id': 'D', 'label': 'It becomes the root of the entire tree'}],
             'q2': 'When an insertion creates a Left-Right imbalance (node inserted into right subtree of left child), '
                   'what sequence of rotations is required?',
             'q2_ans': 'A',
             'q2_exp': {   'A': 'Correct! The Left-Right zigzag shape cannot be solved by a single rotation. First, '
                                'rotating left on the left child straightens the zigzag into a Left-Left line. Second, '
                                'rotating right on the parent balances the tree.',
                           'B': 'Incorrect: Single right rotation leaves the subtree unbalanced.',
                           'C': 'Incorrect: Two right rotations corrupt structure.',
                           'D': 'Incorrect: Left rotation is for Right-Right cases.'},
             'q2_opts': [   {   'id': 'A',
                                'label': 'Left Rotation on the left child, followed by Right Rotation on the parent'},
                            {'id': 'B', 'label': 'Right Rotation on the parent only'},
                            {'id': 'C', 'label': 'Two Right Rotations on the parent'},
                            {'id': 'D', 'label': 'Left Rotation on the parent only'}],
             'recap': [   {   'concept': 'Rotational Invariant Preservation',
                              'naiveIntuition': 'Rotations re-order tree values',
                              'pythonReality': 'Rotations alter depth and topology while keeping the in-order sorted '
                                               'traversal sequence 100% identical'},
                          {   'concept': 'Logarithmic Height Guarantee',
                              'naiveIntuition': 'Standard BSTs are always O(log N)',
                              'pythonReality': 'Without AVL or Red-Black balancing, worst-case insertions degenerate '
                                               'BSTs into O(N) linked lists'}],
             'sample_code': '# Right Rotation on Node y (Left-Left rebalance)\n'
                            '#     y               x\n'
                            '#    / \\             / \\\n'
                            '#   x   T3   -->    T1  y\n'
                            '#  / \\                 / \\\n'
                            '# T1  T2              T2 T3\n'
                            'def rotate_right(y):\n'
                            '    x = y.left\n'
                            '    T2 = x.right\n'
                            '    x.right = y\n'
                            '    y.left = T2\n'
                            '    return x # New root of subtree',
             'solution': 'class TreeNode:\n'
                         '    def __init__(self, val=0, left=None, right=None):\n'
                         '        self.val = val\n'
                         '        self.left = left\n'
                         '        self.right = right\n'
                         '\n'
                         'def right_rotate(y: TreeNode) -> TreeNode:\n'
                         '    x = y.left\n'
                         '    T2 = x.right\n'
                         '    x.right = y\n'
                         '    y.left = T2\n'
                         '    return x\n'
                         '\n'
                         'y = TreeNode(3, TreeNode(2, TreeNode(1)))\n'
                         'new_root = right_rotate(y)\n'
                         "print('New root:', new_root.val, 'Left:', new_root.left.val, 'Right:', new_root.right.val)\n",
             'starter': 'class TreeNode:\n'
                        '    def __init__(self, val=0, left=None, right=None):\n'
                        '        self.val = val\n'
                        '        self.left = left\n'
                        '        self.right = right\n'
                        '\n'
                        'def right_rotate(y: TreeNode) -> TreeNode:\n'
                        '    # TODO: Implement right rotation: return new root x\n'
                        '    return y\n'
                        '\n'
                        '# Left-skewed: 3 -> left: 2 (left: 1)\n'
                        'y = TreeNode(3, TreeNode(2, TreeNode(1))) \n'
                        'new_root = right_rotate(y)\n'
                        "print('New root:', new_root.val, 'Left:', new_root.left.val, 'Right:', new_root.right.val)\n",
             'summary': 'AVL Trees maintain self-balancing guarantees where balance factor (height(left) - '
                        'height(right)) remains in {-1, 0, 1} via four rotation primitives.',
             'takeaway': 'AVL rotations rebalance subtrees in O(1) time while preserving BST in-order invariants.'},
    107: {   'hint': 'Helper check(node) returns black-height or -1 if mismatch. If not node return 1. If check(left) '
                     "!= check(right) return -1. Add 1 if node.color == 'BLACK'.",
             'mechanics': 'The 5 Red-Black Invariants: (1) Every node is RED or BLACK. (2) The root is always BLACK. '
                          '(3) Every leaf (None) is BLACK. (4) If a node is RED, both its children are BLACK (no two '
                          'consecutive red nodes). (5) For each node, all paths from that node to descendant leaves '
                          'contain the SAME number of black nodes (Black-Height). Tree height is strictly bounded: H '
                          '<= 2 * log2(N + 1).',
             'patterns': ['Is valid black height: True'],
             'practice_task': 'Implement Black-Height Verification to validate whether a colored binary tree satisfies '
                              'the Red-Black Black-Height invariant.',
             'q1': "Why does the invariant 'no two consecutive red nodes' combined with 'equal black-height' guarantee "
                   'balanced O(log N) search time?',
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! Since red nodes cannot have red children, you can never have two red nodes '
                                'in a row. The longest path can at most double the shortest path length (2 * BH). '
                                'Hence height is strictly bounded within 2 * log2(N + 1) = O(log N).',
                           'B': 'Incorrect: Nodes remain in the tree with their assigned colors.',
                           'C': 'Incorrect: All nodes contribute to operational depth.',
                           'D': 'Incorrect: Red-black trees are approximately balanced, not complete trees.'},
             'q1_opts': [   {   'id': 'A',
                                'label': 'The shortest possible path consists entirely of black nodes (length BH), '
                                         'while the longest possible path alternates red and black (length 2 * BH), '
                                         'bounding maximum depth to at most 2 * log2(N + 1)'},
                            {'id': 'B', 'label': 'Because red nodes are deleted after insertion'},
                            {'id': 'C', 'label': 'Because black nodes do not count towards tree height'},
                            {'id': 'D', 'label': 'Because red-black trees are perfectly symmetric complete trees'}],
             'q2': "Why do production systems (like Java's TreeMap and C++'s std::map) prefer Red-Black Trees over AVL "
                   'Trees for general-purpose associative containers?',
             'q2_ans': 'A',
             'q2_exp': {   'A': 'Correct! AVL trees are more rigidly balanced, which makes lookups slightly faster, '
                                'but frequent updates trigger cascade rotations up to O(log N). Red-Black trees bound '
                                'rotations to O(1) constant rotations per mutation.',
                           'B': 'Incorrect: AVL trees store all comparable keys.',
                           'C': 'Incorrect: Node color requires at least 1 bit.',
                           'D': 'Incorrect: AVL trees have strictly shallower height, making pure lookups marginally '
                                'faster.'},
             'q2_opts': [   {   'id': 'A',
                                'label': 'Red-Black trees require at most 2 rotations per insertion and at most 3 '
                                         'rotations per deletion, resulting in faster write/update throughput than '
                                         'more rigidly balanced AVL trees'},
                            {'id': 'B', 'label': 'Because AVL trees cannot store integers'},
                            {'id': 'C', 'label': 'Because Red-Black trees use 0 memory'},
                            {'id': 'D', 'label': 'Because Red-Black trees are faster at lookups than AVL trees'}],
             'recap': [   {   'concept': 'Black-Height Balance Invariant',
                              'naiveIntuition': 'Trees must be strictly balanced at every single node',
                              'pythonReality': 'Equalizing black-height bounds depth to within a 2x factor, delivering '
                                               'logarithmic guarantees with minimal rotation overhead'},
                          {   'concept': 'Mutation Rotation Bound',
                              'naiveIntuition': 'Balancing always requires rotating the entire tree',
                              'pythonReality': 'Red-Black re-coloring absorbs most updates; at most 2 or 3 rotations '
                                               'are ever needed per insert/delete'}],
             'sample_code': '# Red-Black Tree Invariants Verification\n'
                            'def verify_black_height(node):\n'
                            '    if not node: return 0\n'
                            '    left_bh = verify_black_height(node.left)\n'
                            '    right_bh = verify_black_height(node.right)\n'
                            "    if left_bh != right_bh: raise ValueError('Black height mismatch!')\n"
                            "    return left_bh + (1 if node.color == 'BLACK' else 0)",
             'solution': 'class RBNode:\n'
                         "    def __init__(self, val, color='BLACK', left=None, right=None):\n"
                         '        self.val = val\n'
                         '        self.color = color\n'
                         '        self.left = left\n'
                         '        self.right = right\n'
                         '\n'
                         'def is_valid_black_height(root: RBNode) -> bool:\n'
                         '    def check(node):\n'
                         '        if not node:\n'
                         '            return 1 # Null leaves are black\n'
                         '        lb = check(node.left)\n'
                         '        rb = check(node.right)\n'
                         '        if lb == -1 or rb == -1 or lb != rb:\n'
                         '            return -1\n'
                         "        return lb + (1 if node.color == 'BLACK' else 0)\n"
                         '    return check(root) != -1\n'
                         '\n'
                         "valid_tree = RBNode(2, 'BLACK', RBNode(1, 'BLACK'), RBNode(3, 'RED', RBNode(2.5, 'BLACK')))\n"
                         "print('Is valid black height:', is_valid_black_height(valid_tree))\n",
             'starter': 'class RBNode:\n'
                        "    def __init__(self, val, color='BLACK', left=None, right=None):\n"
                        '        self.val = val\n'
                        "        self.color = color  # 'RED' or 'BLACK'\n"
                        '        self.left = left\n'
                        '        self.right = right\n'
                        '\n'
                        'def is_valid_black_height(root: RBNode) -> bool:\n'
                        '    # TODO: Return True if all root-to-leaf paths have identical count of BLACK nodes\n'
                        '    return False\n'
                        '\n'
                        '# Root(B) -> left: 1(B), right: 3(R -> left: 2(B))\n'
                        '# Path 1: B -> B = 2 black nodes. Path 2: B -> R -> B = 2 black nodes. Valid!\n'
                        "valid_tree = RBNode(2, 'BLACK', RBNode(1, 'BLACK'), RBNode(3, 'RED', RBNode(2.5, 'BLACK')))\n"
                        "print('Is valid black height:', is_valid_black_height(valid_tree)) # True\n",
             'summary': 'Red-Black Trees maintain approximate balance through local node coloring invariants, '
                        'guaranteeing worst-case O(log N) operations with fewer tree rotations on updates than AVL '
                        'trees.',
             'takeaway': 'Equal black-height across all paths bounds the maximum path length to at most twice the '
                         'minimum path length.'},
    108: {   'hint': 'In insert: loop ch, setdefault TrieNode(), set is_end = True. In search: verify path exists and '
                     'return curr.is_end. In starts_with: verify path exists and return True.',
             'mechanics': 'Each TrieNode contains `children = {}` (mapping char to child node) and boolean `is_end = '
                          'False`. Insertion walks down the character path, creating nodes as needed. Lookup verifies '
                          'the path exists. Prefix queries check path existence without requiring `is_end`.',
             'patterns': ['Search code: True', 'Search cod: False', 'Starts with cod: True'],
             'practice_task': 'Implement a complete Trie supporting insert, search, and starts_with.',
             'q1': 'Why is Trie search time complexity O(L) where L is query length, rather than depending on the '
                   'number of stored words N?',
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! Whether the Trie stores 10 words or 10,000,000 words, searching for a '
                                "4-letter prefix like 'code' performs exactly 4 child lookups down the matching "
                                'branch, taking strictly O(L) time.',
                           'B': 'Incorrect: Tries do not require array sorting.',
                           'C': 'Incorrect: Word count N is typically much larger than word length L.',
                           'D': 'Incorrect: Tries use hash/array indexing at each node, not binary search.'},
             'q1_opts': [   {   'id': 'A',
                                'label': 'Each character lookup follows a direct dictionary pointer in O(1) time down '
                                         'a tree branch of depth L, never inspecting unrelated branches'},
                            {'id': 'B', 'label': 'Because the Trie sorts all words in memory'},
                            {'id': 'C', 'label': 'Because N is always smaller than L'},
                            {'id': 'D', 'label': 'Because Tries use binary search on strings'}],
             'q2': 'What distinguishes `search(word)` from `starts_with(prefix)` in a Trie?',
             'q2_ans': 'A',
             'q2_exp': {   'A': "Correct! If 'apple' is inserted, 'app' is a valid prefix (`starts_with('app') == "
                                "True`), but not a complete word (`search('app') == False`) until explicitly marked "
                                '`is_end = True`.',
                           'B': 'Incorrect: Both operations run in O(L) time.',
                           'C': 'Incorrect: Both traverse from prefix root downward.',
                           'D': 'Incorrect: The `is_end` check differentiates words from intermediate prefixes.'},
             'q2_opts': [   {   'id': 'A',
                                'label': 'search(word) requires `curr.is_end == True` at the final node, while '
                                         'starts_with(prefix) only requires the character path to exist'},
                            {'id': 'B', 'label': 'starts_with is O(N) while search is O(1)'},
                            {'id': 'C', 'label': 'search checks suffixes instead of prefixes'},
                            {'id': 'D', 'label': 'There is no difference'}],
             'recap': [   {   'concept': 'Prefix Consolidation',
                              'naiveIntuition': 'Store words in an array and use string.startswith()',
                              'pythonReality': 'Tries consolidate overlapping prefixes into shared tree nodes, '
                                               'collapsing redundant scans into O(L) lookups'},
                          {   'concept': 'Word Boundary Disambiguation',
                              'naiveIntuition': 'Reaching a node means the word exists',
                              'pythonReality': 'Only nodes with is_end == True denote complete stored words; '
                                               'intermediate nodes represent valid prefixes'}],
             'sample_code': '# Trie Prefix Tree\n'
                            'class TrieNode:\n'
                            '    def __init__(self):\n'
                            '        self.children = {}\n'
                            '        self.is_end = False\n'
                            '\n'
                            'class Trie:\n'
                            '    def __init__(self):\n'
                            '        self.root = TrieNode()\n'
                            '    def insert(self, word):\n'
                            '        curr = self.root\n'
                            '        for ch in word:\n'
                            '            curr = curr.children.setdefault(ch, TrieNode())\n'
                            '        curr.is_end = True\n'
                            '    def search(self, word):\n'
                            '        curr = self.root\n'
                            '        for ch in word:\n'
                            '            if ch not in curr.children: return False\n'
                            '            curr = curr.children[ch]\n'
                            '        return curr.is_end',
             'solution': 'class TrieNode:\n'
                         '    def __init__(self):\n'
                         '        self.children = {}\n'
                         '        self.is_end = False\n'
                         '\n'
                         'class Trie:\n'
                         '    def __init__(self):\n'
                         '        self.root = TrieNode()\n'
                         '\n'
                         '    def insert(self, word: str) -> None:\n'
                         '        curr = self.root\n'
                         '        for ch in word:\n'
                         '            if ch not in curr.children:\n'
                         '                curr.children[ch] = TrieNode()\n'
                         '            curr = curr.children[ch]\n'
                         '        curr.is_end = True\n'
                         '\n'
                         '    def search(self, word: str) -> bool:\n'
                         '        curr = self.root\n'
                         '        for ch in word:\n'
                         '            if ch not in curr.children:\n'
                         '                return False\n'
                         '            curr = curr.children[ch]\n'
                         '        return curr.is_end\n'
                         '\n'
                         '    def starts_with(self, prefix: str) -> bool:\n'
                         '        curr = self.root\n'
                         '        for ch in prefix:\n'
                         '            if ch not in curr.children:\n'
                         '                return False\n'
                         '            curr = curr.children[ch]\n'
                         '        return True\n'
                         '\n'
                         't = Trie()\n'
                         "t.insert('code')\n"
                         "print('Search code:', t.search('code'))\n"
                         "print('Search cod:', t.search('cod'))\n"
                         "print('Starts with cod:', t.starts_with('cod'))\n",
             'starter': 'class TrieNode:\n'
                        '    def __init__(self):\n'
                        '        self.children = {}\n'
                        '        self.is_end = False\n'
                        '\n'
                        'class Trie:\n'
                        '    def __init__(self):\n'
                        '        self.root = TrieNode()\n'
                        '\n'
                        '    # TODO: Implement insert, search, and starts_with\n'
                        '\n'
                        't = Trie()\n'
                        "t.insert('code')\n"
                        "print('Search code:', t.search('code'))       # True\n"
                        "print('Search cod:', t.search('cod'))         # False\n"
                        "print('Starts with cod:', t.starts_with('cod')) # True\n",
             'summary': 'Tries (Prefix Trees) organize strings character-by-character where common prefixes share '
                        'common ancestor nodes, enabling O(L) search, prefix matching, and insertion independent of '
                        'dictionary size N.',
             'takeaway': 'Tries achieve O(L) prefix search proportional solely to word length L, bypassing expensive '
                         'scans across N dictionary entries.'},
    109: {   'hint': "In search: helper dfs(idx, node). If idx == len(word) return node.is_end. If ch == '.': for "
                     'child in node.children.values(): if dfs(idx+1, child) return True; return False. Else if ch in '
                     'node.children return dfs(idx+1, node.children[ch]).',
             'mechanics': "Wildcard Search: for literal characters, follow `curr.children[ch]`. For wildcard `'.'`: "
                          'recurse across ALL available child branches in `curr.children.values()`. If any branch '
                          'matches the remaining pattern, return True. Autocomplete: descend to the prefix node, then '
                          'launch a DFS to collect all descendant words.',
             'patterns': ['Search pad: False', 'Search bad: True', 'Search .ad: True', 'Search b..: True'],
             'practice_task': "Build a WordDictionary supporting '.' wildcards matching any single letter.",
             'q1': 'What is the worst-case time complexity of searching a pattern consisting entirely of wildcards '
                   "'...' in a Trie with branching factor 26?",
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! With all wildcards, the search cannot prune any character branches, forcing '
                                'DFS to explore all available child branches down to depth L. For 26 letters, worst '
                                'case is O(26^L).',
                           'B': 'Incorrect: That applies to literal queries without wildcards.',
                           'C': 'Incorrect: Time complexity is exponential.',
                           'D': 'Incorrect: Must traverse tree branches.'},
             'q1_opts': [   {   'id': 'A',
                                'label': 'O(26^L) where L is pattern length, exploring every branch in the tree'},
                            {'id': 'B', 'label': 'O(L) linear time'},
                            {'id': 'C', 'label': 'O(N * L) space'},
                            {'id': 'D', 'label': 'O(1) constant time'}],
             'q2': 'In an Autocomplete system, what is the first step before collecting word suggestions?',
             'q2_ans': 'A',
             'q2_exp': {   'A': 'Correct! Finding the prefix node in O(L) isolates the exact subtree containing all '
                                'words beginning with that prefix. Subtree DFS then collects candidate completions.',
                           'B': 'Incorrect: The Trie structure already enforces prefix clustering.',
                           'C': 'Incorrect: Autocomplete words have variable lengths.',
                           'D': 'Incorrect: Trie processes string characters directly.'},
             'q2_opts': [   {   'id': 'A',
                                'label': 'Descend down the Trie along the prefix characters; if the prefix path '
                                         'exists, the target node is the root of the suggestion subtree'},
                            {'id': 'B', 'label': 'Sort all words in the dictionary alphabetically'},
                            {'id': 'C', 'label': 'Delete words with different lengths'},
                            {'id': 'D', 'label': 'Convert all words to lowercase integers'}],
             'recap': [   {   'concept': 'Multi-Branch Pruning',
                              'naiveIntuition': 'Wildcards require regex searches across all words',
                              'pythonReality': 'Trie-guided DFS branches only on existing letters at each step, '
                                               'pruning dead branches immediately'},
                          {   'concept': 'Subtree Scoping',
                              'naiveIntuition': 'Autocomplete checks every word in dictionary',
                              'pythonReality': 'Walking the prefix path scopes the search to exactly the descendant '
                                               'subtree, ignoring 99% of unrelated words'}],
             'sample_code': "# WordDictionary with '.' Wildcards\n"
                            'def search_wildcard(node, word, idx):\n'
                            '    if idx == len(word): return node.is_end\n'
                            '    ch = word[idx]\n'
                            "    if ch == '.':\n"
                            '        return any(search_wildcard(child, word, idx + 1) for child in '
                            'node.children.values())\n'
                            '    if ch in node.children:\n'
                            '        return search_wildcard(node.children[ch], word, idx + 1)\n'
                            '    return False',
             'solution': 'class TrieNode:\n'
                         '    def __init__(self):\n'
                         '        self.children = {}\n'
                         '        self.is_end = False\n'
                         '\n'
                         'class WordDictionary:\n'
                         '    def __init__(self):\n'
                         '        self.root = TrieNode()\n'
                         '\n'
                         '    def add_word(self, word: str) -> None:\n'
                         '        curr = self.root\n'
                         '        for ch in word:\n'
                         '            if ch not in curr.children:\n'
                         '                curr.children[ch] = TrieNode()\n'
                         '            curr = curr.children[ch]\n'
                         '        curr.is_end = True\n'
                         '\n'
                         '    def search(self, word: str) -> bool:\n'
                         '        def dfs(idx, node):\n'
                         '            if idx == len(word):\n'
                         '                return node.is_end\n'
                         '            ch = word[idx]\n'
                         "            if ch == '.':\n"
                         '                for child in node.children.values():\n'
                         '                    if dfs(idx + 1, child):\n'
                         '                        return True\n'
                         '                return False\n'
                         '            if ch not in node.children:\n'
                         '                return False\n'
                         '            return dfs(idx + 1, node.children[ch])\n'
                         '        return dfs(0, self.root)\n'
                         '\n'
                         'wd = WordDictionary()\n'
                         "wd.add_word('bad')\n"
                         "wd.add_word('dad')\n"
                         "wd.add_word('mad')\n"
                         "print('Search pad:', wd.search('pad'))\n"
                         "print('Search bad:', wd.search('bad'))\n"
                         "print('Search .ad:', wd.search('.ad'))\n"
                         "print('Search b..:', wd.search('b..'))\n",
             'starter': 'class TrieNode:\n'
                        '    def __init__(self):\n'
                        '        self.children = {}\n'
                        '        self.is_end = False\n'
                        '\n'
                        'class WordDictionary:\n'
                        '    def __init__(self):\n'
                        '        self.root = TrieNode()\n'
                        '\n'
                        '    def add_word(self, word: str) -> None:\n'
                        '        # TODO: Insert word into Trie\n'
                        '        pass\n'
                        '\n'
                        '    def search(self, word: str) -> bool:\n'
                        "        # TODO: Search word where '.' matches any character\n"
                        '        return False\n'
                        '\n'
                        'wd = WordDictionary()\n'
                        "wd.add_word('bad')\n"
                        "wd.add_word('dad')\n"
                        "wd.add_word('mad')\n"
                        "print('Search pad:', wd.search('pad')) # False\n"
                        "print('Search bad:', wd.search('bad')) # True\n"
                        "print('Search .ad:', wd.search('.ad')) # True\n"
                        "print('Search b..:', wd.search('b..')) # True\n",
             'summary': 'Trie Applications extend basic prefix matching to support Autocomplete suggestions and '
                        "Wildcard Pattern Search (matching '.' to any character) via DFS branching.",
             'takeaway': "Wildcard character '.' transforms linear Trie descent into multi-branch DFS, exploring all "
                         'valid phonetic avenues.'},
    110: {   'hint': 'Iterative in-order using stack: while curr or stack: while curr: stack.append(curr); curr = '
                     'curr.left. curr = stack.pop(); k -= 1; if k == 0 return curr.val; curr = curr.right.',
             'mechanics': 'Master tree problem classification: (1) Level by level / shortest path? Use BFS with deque. '
                          '(2) Subtree aggregation / height / diameter? Use post-order bottom-up DFS. (3) Range bounds '
                          '/ sorted values? Use BST in-order properties. (4) Zero memory constraints? Use Morris '
                          'traversal.',
             'patterns': ['1st smallest: 1', '3rd smallest: 3'],
             'practice_task': 'Find the K-th smallest element in a Binary Search Tree.',
             'q1': 'Which traversal strategy should be selected when asked to find the minimum depth to a leaf node in '
                   'a huge binary tree with millions of nodes?',
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! BFS searches level by level. The moment it pops a node with `not node.left '
                                'and not node.right`, that depth is guaranteed to be minimal. It terminates without '
                                'exploring deeper massive subtrees.',
                           'B': 'Incorrect: DFS might plunge down a million-node deep subtree before checking shallow '
                                'leaves on other branches.',
                           'C': 'Incorrect: In-order does not correlate with leaf depth.',
                           'D': 'Incorrect: Morris visits all nodes.'},
             'q1_opts': [   {   'id': 'A',
                                'label': 'BFS level-order traversal, because it terminates the moment the very first '
                                         'leaf node is encountered at the shallowest depth'},
                            {'id': 'B', 'label': 'DFS post-order traversal'},
                            {'id': 'C', 'label': 'In-order traversal'},
                            {'id': 'D', 'label': 'Morris traversal'}],
             'q2': 'What is the primary operational trade-off of maintaining an AVL balanced tree compared to a naive '
                   'BST?',
             'q2_ans': 'A',
             'q2_exp': {   'A': 'Correct! AVL trees eliminate the O(N) degraded list scenario by rebalancing in O(1) '
                                'rotations, ensuring strict O(log N) worst-case operation times.',
                           'B': 'Incorrect: All numbers are supported.',
                           'C': 'Incorrect: Naive BST degrades to O(N) on sorted inputs.',
                           'D': 'Incorrect: Space is strictly O(N).'},
             'q2_opts': [   {   'id': 'A',
                                'label': 'AVL guarantees O(log N) worst-case search and insert times at the cost of '
                                         'rebalancing rotation overhead on insertions and deletions'},
                            {'id': 'B', 'label': 'AVL trees cannot store negative numbers'},
                            {'id': 'C', 'label': 'Naive BST is faster on worst-case data'},
                            {'id': 'D', 'label': 'AVL trees consume O(N^2) memory'}],
             'recap': [   {   'concept': 'In-Order Early Stopping',
                              'naiveIntuition': 'Extract all N nodes into an array, then return array[k-1]',
                              'pythonReality': 'Stopping the in-order traversal at step k finds the answer in O(H + K) '
                                               'time without traversing the remainder of the tree'},
                          {   'concept': 'Section 9 Synthesis',
                              'naiveIntuition': 'Tree algorithms are unrelated formulas',
                              'pythonReality': 'All tree algorithms flow from three foundational paradigms: '
                                               'Level-Order Queue (BFS), Depth-First Recurrence (DFS), and In-Order '
                                               'Monotonicity (BST)'}],
             'sample_code': '# Tree Problem Solving Taxonomy:\n'
                            '# 1. Top-Down: pass arguments downward (Path Sum, Validate BST Range)\n'
                            '# 2. Bottom-Up: combine child returns upward (Height, Diameter, LCA)\n'
                            '# 3. Breadth-First: level-by-level queue (Level-Order, Zigzag)\n'
                            '# 4. In-Order: BST monotonicity (Sorted recovery, K-th smallest)',
             'solution': 'class TreeNode:\n'
                         '    def __init__(self, val=0, left=None, right=None):\n'
                         '        self.val = val\n'
                         '        self.left = left\n'
                         '        self.right = right\n'
                         '\n'
                         'def kth_smallest(root: TreeNode, k: int) -> int:\n'
                         '    stack = []\n'
                         '    curr = root\n'
                         '    while curr or stack:\n'
                         '        while curr:\n'
                         '            stack.append(curr)\n'
                         '            curr = curr.left\n'
                         '        curr = stack.pop()\n'
                         '        k -= 1\n'
                         '        if k == 0:\n'
                         '            return curr.val\n'
                         '        curr = curr.right\n'
                         '    return -1\n'
                         '\n'
                         't = TreeNode(3, TreeNode(1, None, TreeNode(2)), TreeNode(4))\n'
                         "print('1st smallest:', kth_smallest(t, 1))\n"
                         "print('3rd smallest:', kth_smallest(t, 3))\n",
             'starter': 'class TreeNode:\n'
                        '    def __init__(self, val=0, left=None, right=None):\n'
                        '        self.val = val\n'
                        '        self.left = left\n'
                        '        self.right = right\n'
                        '\n'
                        'def kth_smallest(root: TreeNode, k: int) -> int:\n'
                        '    # TODO: Exploit BST in-order sorted traversal to find k-th smallest (1-indexed)\n'
                        '    return -1\n'
                        '\n'
                        '# BST: 3 -> left: 1 (right: 2), right: 4. k=1 is 1; k=3 is 3\n'
                        't = TreeNode(3, TreeNode(1, None, TreeNode(2)), TreeNode(4))\n'
                        "print('1st smallest:', kth_smallest(t, 1))\n"
                        "print('3rd smallest:', kth_smallest(t, 3))\n",
             'summary': 'Section 9 Review synthesizes binary tree traversals, level-order BFS, bottom-up DFS '
                        'recursion, BST invariants, Morris traversal, and self-balancing rotations.',
             'takeaway': 'Tree algorithms are mastered by matching tree topology invariants to recursion and queue '
                         'patterns.'}}
