"""
Practice Problems for Section 9 (Trees & Binary Search Trees)
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

SEC9_TREES_PROBLEMS = [
    P(
        "binary-tree-inorder-traversal", "Binary Tree Inorder Traversal", "trees", 1, "inorder_traversal",
        "Given the root of a binary tree represented as a level-order array `root` (where `None` denotes empty nodes), return the inorder traversal of its nodes' values.",
        "- `0 <= len(root) <= 100`\n- `-100 <= node.val <= 100`",
        "O(n)", "O(n)",
        "def inorder_traversal(root: list) -> list[int]:\n    pass\n",
        [
            {"args": [[1, None, 2, None, None, 3]], "expected": [1, 3, 2]},
            {"args": [[]], "expected": []},
            {"args": [[1]], "expected": [1]},
            {"args": [[1, 2, 3, 4, 5]], "expected": [4, 2, 5, 1, 3]},
            {"args": [[1, None, 2]], "expected": [1, 2]}
        ],
        "def inorder_traversal(root: list) -> list[int]:\n    if not root:\n        return []\n    res = []\n    def dfs(idx):\n        if idx >= len(root) or root[idx] is None:\n            return\n        dfs(2 * idx + 1)\n        res.append(root[idx])\n        dfs(2 * idx + 2)\n    dfs(0)\n    return res\n"
    ),

    P(
        "invert-binary-tree", "Invert Binary Tree", "trees", 1, "invert_tree",
        "Given the root of a binary tree represented as a flat array `root`, invert the tree (swap left and right subtrees recursively) and return its level-order array.",
        "- `0 <= len(root) <= 100`",
        "O(n)", "O(n)",
        "def invert_tree(root: list) -> list:\n    pass\n",
        [
            {"args": [[4, 2, 7, 1, 3, 6, 9]], "expected": [4, 7, 2, 9, 6, 3, 1]},
            {"args": [[2, 1, 3]], "expected": [2, 3, 1]},
            {"args": [[]], "expected": []},
            {"args": [[1]], "expected": [1]}
        ],
        "def invert_tree(root: list) -> list:\n    if not root:\n        return []\n    # Tree array inversion level-by-level\n    res = list(root)\n    level = 0\n    start = 0\n    while start < len(res):\n        count = 1 << level\n        end = min(start + count, len(res))\n        res[start:end] = reversed(res[start:end])\n        start += count\n        level += 1\n    return res\n"
    ),

    P(
        "maximum-depth-of-binary-tree", "Maximum Depth of Binary Tree", "trees", 1, "max_depth",
        "Given the root of a binary tree represented as a level-order array `root`, return its maximum depth.\n\nA binary tree's maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.",
        "- `0 <= len(root) <= 10^4`",
        "O(n)", "O(h)",
        "def max_depth(root: list) -> int:\n    pass\n",
        [
            {"args": [[3, 9, 20, None, None, 15, 7]], "expected": 3},
            {"args": [[1, None, 2]], "expected": 2},
            {"args": [[]], "expected": 0},
            {"args": [[0]], "expected": 1},
            {"args": [[1, 2, 3, 4, 5]], "expected": 3}
        ],
        "def max_depth(root: list) -> int:\n    if not root:\n        return 0\n    def get_d(idx):\n        if idx >= len(root) or root[idx] is None:\n            return 0\n        return 1 + max(get_d(2 * idx + 1), get_d(2 * idx + 2))\n    return get_d(0)\n"
    ),

    P(
        "same-tree", "Same Tree (Structural Equivalence)", "trees", 1, "is_same_tree",
        "Given the roots of two binary trees `p` and `q`, write a function to check if they are the same or not.\n\nTwo binary trees are considered the same if they are structurally identical, and the nodes have the same value.",
        "- `0 <= len(p), len(q) <= 100`",
        "O(n)", "O(h)",
        "def is_same_tree(p: list, q: list) -> bool:\n    pass\n",
        [
            {"args": [[1, 2, 3], [1, 2, 3]], "expected": True},
            {"args": [[1, 2], [1, None, 2]], "expected": False},
            {"args": [[1, 2, 1], [1, 1, 2]], "expected": False},
            {"args": [[], []], "expected": True},
            {"args": [[1], [1]], "expected": True}
        ],
        "def is_same_tree(p: list, q: list) -> bool:\n    return p == q\n"
    ),

    P(
        "symmetric-tree", "Symmetric Tree (Mirror Reflection)", "trees", 2, "is_symmetric",
        "Given the root of a binary tree `root`, check whether it is a mirror of itself (i.e., symmetric around its center).",
        "- `0 <= len(root) <= 1000`",
        "O(n)", "O(h)",
        "def is_symmetric(root: list) -> bool:\n    pass\n",
        [
            {"args": [[1, 2, 2, 3, 4, 4, 3]], "expected": True},
            {"args": [[1, 2, 2, None, 3, None, 3]], "expected": False},
            {"args": [[]], "expected": True},
            {"args": [[1]], "expected": True},
            {"args": [[1, 2, 2, 2, None, 2]], "expected": False}
        ],
        "def is_symmetric(root: list) -> bool:\n    if not root:\n        return True\n    def is_mirror(i, j):\n        n = len(root)\n        if i >= n and j >= n:\n            return True\n        v1 = root[i] if i < n else None\n        v2 = root[j] if j < n else None\n        if v1 is None and v2 is None:\n            return True\n        if v1 != v2:\n            return False\n        return is_mirror(2 * i + 1, 2 * j + 2) and is_mirror(2 * i + 2, 2 * j + 1)\n    return is_mirror(1, 2)\n"
    ),

    P(
        "binary-tree-level-order-traversal", "Binary Tree Level Order Traversal (BFS)", "trees", 2, "level_order",
        "Given the root of a binary tree `root`, return the level order traversal of its nodes' values (i.e., from left to right, level by level).",
        "- `0 <= len(root) <= 2000`",
        "O(n)", "O(n)",
        "def level_order(root: list) -> list[list[int]]:\n    pass\n",
        [
            {"args": [[3, 9, 20, None, None, 15, 7]], "expected": [[3], [9, 20], [15, 7]]},
            {"args": [[1]], "expected": [[1]]},
            {"args": [[]], "expected": []},
            {"args": [[1, 2, 3, 4, 5, 6, 7]], "expected": [[1], [2, 3], [4, 5, 6, 7]]}
        ],
        "def level_order(root: list) -> list[list[int]]:\n    if not root or root[0] is None:\n        return []\n    res = []\n    level = 0\n    start = 0\n    while start < len(root):\n        count = 1 << level\n        end = min(start + count, len(root))\n        vals = [root[i] for i in range(start, end) if root[i] is not None]\n        if vals:\n            res.append(vals)\n        start += count\n        level += 1\n    return res\n"
    ),

    P(
        "validate-binary-search-tree", "Validate Binary Search Tree", "trees", 3, "is_valid_bst",
        "Given the root of a binary tree `root`, determine if it is a valid binary search tree (BST).\n\nA valid BST requires all keys in the left subtree to be strictly less than the node's key, and all keys in the right subtree to be strictly greater.",
        "- `0 <= len(root) <= 10^4`\n- `-2^31 <= node.val <= 2^31 - 1`",
        "O(n)", "O(h)",
        "def is_valid_bst(root: list) -> bool:\n    pass\n",
        [
            {"args": [[2, 1, 3]], "expected": True},
            {"args": [[5, 1, 4, None, None, 3, 6]], "expected": False},
            {"args": [[1]], "expected": True},
            {"args": [[]], "expected": True},
            {"args": [[10, 5, 15, None, None, 6, 20]], "expected": False}
        ],
        "def is_valid_bst(root: list) -> bool:\n    if not root:\n        return True\n    def check(idx, low, high):\n        if idx >= len(root) or root[idx] is None:\n            return True\n        val = root[idx]\n        if val <= low or val >= high:\n            return False\n        return check(2 * idx + 1, low, val) and check(2 * idx + 2, val, high)\n    return check(0, float('-inf'), float('inf'))\n"
    ),

    P(
        "lowest-common-ancestor-of-a-bst", "Lowest Common Ancestor of a BST", "trees", 2, "lowest_common_ancestor_bst",
        "Given a binary search tree `root` and two node values `p` and `q`, find the value of the lowest common ancestor (LCA) node of `p` and `q`.\n\nIn a BST, if both `p` and `q` are smaller than root, LCA is in left; if both are larger, LCA is in right; otherwise root is LCA.",
        "- `2 <= len(root) <= 10^4`\n- All node values are unique\n- `p` and `q` exist in the BST",
        "O(h)", "O(1)",
        "def lowest_common_ancestor_bst(root: list, p: int, q: int) -> int:\n    pass\n",
        [
            {"args": [[6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], 2, 8], "expected": 6},
            {"args": [[6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], 2, 4], "expected": 2},
            {"args": [[2, 1], 2, 1], "expected": 2}
        ],
        "def lowest_common_ancestor_bst(root: list, p: int, q: int) -> int:\n    curr = 0\n    while curr < len(root) and root[curr] is not None:\n        val = root[curr]\n        if p < val and q < val:\n            curr = 2 * curr + 1\n        elif p > val and q > val:\n            curr = 2 * curr + 2\n        else:\n            return val\n    return -1\n"
    ),

    P(
        "lowest-common-ancestor-of-a-binary-tree", "Lowest Common Ancestor of a Binary Tree", "trees", 3, "lowest_common_ancestor_tree",
        "Given a general binary tree `root` and two values `p` and `q`, find the value of the Lowest Common Ancestor (LCA) node.",
        "- `2 <= len(root) <= 10^4`\n- All node values are unique",
        "O(n)", "O(h)",
        "def lowest_common_ancestor_tree(root: list, p: int, q: int) -> int:\n    pass\n",
        [
            {"args": [[3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], 5, 1], "expected": 3},
            {"args": [[3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], 5, 4], "expected": 5},
            {"args": [[1, 2], 1, 2], "expected": 1}
        ],
        "def lowest_common_ancestor_tree(root: list, p: int, q: int) -> int:\n    def find(idx):\n        if idx >= len(root) or root[idx] is None:\n            return None\n        val = root[idx]\n        if val == p or val == q:\n            return val\n        left = find(2 * idx + 1)\n        right = find(2 * idx + 2)\n        if left is not None and right is not None:\n            return val\n        return left if left is not None else right\n    return find(0)\n"
    ),

    P(
        "kth-smallest-element-in-a-bst", "Kth Smallest Element in a BST", "trees", 3, "kth_smallest_bst",
        "Given the root of a binary search tree `root` and an integer `k`, return the `k`th smallest value (1-indexed) of all the values of the nodes in the tree.",
        "- `1 <= k <= len(root) <= 10^4`",
        "O(h + k)", "O(h)",
        "def kth_smallest_bst(root: list, k: int) -> int:\n    pass\n",
        [
            {"args": [[3, 1, 4, None, 2], 1], "expected": 1},
            {"args": [[5, 3, 6, 2, 4, None, None, 1], 3], "expected": 3},
            {"args": [[1], 1], "expected": 1},
            {"args": [[2, 1, 3], 2], "expected": 2}
        ],
        "def kth_smallest_bst(root: list, k: int) -> int:\n    res = []\n    def inorder(idx):\n        if idx >= len(root) or root[idx] is None or len(res) >= k:\n            return\n        inorder(2 * idx + 1)\n        res.append(root[idx])\n        inorder(2 * idx + 2)\n    inorder(0)\n    return res[k - 1]\n"
    ),

    P(
        "balanced-binary-tree", "Balanced Binary Tree (AVL Check)", "trees", 2, "is_balanced",
        "Given a binary tree `root`, determine if it is height-balanced.\n\nA height-balanced binary tree is a binary tree in which the depth of the two subtrees of every node never differs by more than one.",
        "- `0 <= len(root) <= 5000`",
        "O(n)", "O(h)",
        "def is_balanced(root: list) -> bool:\n    pass\n",
        [
            {"args": [[3, 9, 20, None, None, 15, 7]], "expected": True},
            {"args": [[1, 2, 2, 3, 3, None, None, 4, 4]], "expected": False},
            {"args": [[]], "expected": True},
            {"args": [[1]], "expected": True},
            {"args": [[1, 2, 3]], "expected": True}
        ],
        "def is_balanced(root: list) -> bool:\n    def check(idx):\n        if idx >= len(root) or root[idx] is None:\n            return 0\n        left = check(2 * idx + 1)\n        if left == -1:\n            return -1\n        right = check(2 * idx + 2)\n        if right == -1:\n            return -1\n        if abs(left - right) > 1:\n            return -1\n        return 1 + max(left, right)\n    return check(0) != -1\n"
    ),

    P(
        "implement-trie-prefix-tree", "Implement Trie (Prefix Tree)", "trees", 3, "simulate_trie",
        "Implement a Trie with `insert`, `search`, and `startsWith` methods. Given an operations sequence `[['insert', word], ['search', word], ['startsWith', prefix]]`, return the output list.",
        "- `1 <= len(word), len(prefix) <= 2000`\n- All inputs consist of lowercase English letters",
        "O(L) per op", "O(total characters)",
        "def simulate_trie(operations: list) -> list:\n    pass\n",
        [
            {"args": [[["insert", "apple"], ["search", "apple"], ["search", "app"], ["startsWith", "app"], ["insert", "app"], ["search", "app"]]],
             "expected": [None, True, False, True, None, True]},
            {"args": [[["insert", "hello"], ["startsWith", "he"], ["search", "hell"]]],
             "expected": [None, True, False]}
        ],
        "def simulate_trie(operations: list) -> list:\n    root = {}\n    out = []\n    for op in operations:\n        cmd, word = op[0], op[1]\n        if cmd == 'insert':\n            node = root\n            for ch in word:\n                node = node.setdefault(ch, {})\n            node['#'] = True\n            out.append(None)\n        elif cmd == 'search':\n            node = root\n            found = True\n            for ch in word:\n                if ch not in node:\n                    found = False\n                    break\n                node = node[ch]\n            out.append(found and '#' in node)\n        elif cmd == 'startsWith':\n            node = root\n            found = True\n            for ch in word:\n                if ch not in node:\n                    found = False\n                    break\n                node = node[ch]\n            out.append(found)\n    return out\n"
    ),

    P(
        "design-add-and-search-words", "Design Add and Search Words (Wildcard Trie)", "trees", 3, "simulate_word_dictionary",
        "Design a data structure that supports adding new words and finding if a string matches any previously added string, where `'.'` matches any letter. Operations: `[['addWord', word], ['search', word]]`. Return outcomes list.",
        "- `1 <= len(word) <= 25`\n- At most `1000` calls",
        "O(M) add, O(26^k * M) search", "O(total chars)",
        "def simulate_word_dictionary(operations: list) -> list:\n    pass\n",
        [
            {"args": [[["addWord", "bad"], ["addWord", "dad"], ["addWord", "mad"], ["search", "pad"], ["search", "bad"], ["search", ".ad"], ["search", "b.."]]],
             "expected": [None, None, None, False, True, True, True]},
            {"args": [[["addWord", "a"], ["addWord", "a"], ["search", "."], ["search", "a"], ["search", "aa"]]],
             "expected": [None, None, True, True, False]}
        ],
        "def simulate_word_dictionary(operations: list) -> list:\n    root = {}\n    out = []\n    for op in operations:\n        cmd, word = op[0], op[1]\n        if cmd == 'addWord':\n            node = root\n            for ch in word:\n                node = node.setdefault(ch, {})\n            node['#'] = True\n            out.append(None)\n        elif cmd == 'search':\n            def search_node(w_idx, node):\n                if w_idx == len(word):\n                    return '#' in node\n                ch = word[w_idx]\n                if ch == '.':\n                    for key in node:\n                        if key != '#' and search_node(w_idx + 1, node[key]):\n                            return True\n                    return False\n                if ch not in node:\n                    return False\n                return search_node(w_idx + 1, node[ch])\n            out.append(search_node(0, root))\n    return out\n"
    ),

    P(
        "serialize-and-deserialize-binary-tree", "Serialize and Deserialize Binary Tree", "trees", 5, "roundtrip_tree",
        "Design an algorithm to serialize and deserialize a binary tree into a string and back. Function `roundtrip_tree(root)` should serialize the tree to a string, deserialize it, and return the level-order array representation.",
        "- `0 <= len(root) <= 1000`",
        "O(n)", "O(n)",
        "def roundtrip_tree(root: list) -> list:\n    pass\n",
        [
            {"args": [[1, 2, 3, None, None, 4, 5]], "expected": [1, 2, 3, None, None, 4, 5]},
            {"args": [[]], "expected": []},
            {"args": [[1]], "expected": [1]},
            {"args": [[1, 2]], "expected": [1, 2]}
        ],
        "def roundtrip_tree(root: list) -> list:\n    # Deterministic roundtrip\n    s = ','.join('null' if x is None else str(x) for x in root)\n    if not s or s == 'null':\n        return []\n    parts = s.split(',')\n    return [None if p == 'null' else int(p) for p in parts]\n"
    )
]
