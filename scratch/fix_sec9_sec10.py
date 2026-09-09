"""
Fix and re-align all section data files in scratch/curriculum_generator/
to guarantee 100% synchronization with curriculum_160.json.
"""

import pprint
import sys
sys.path.insert(0, ".")

# ---------------------------------------------------------------------------
# Section 9 (Trees & BSTs: Days 96-110)
# ---------------------------------------------------------------------------
def fix_sec9():
    from scratch.curriculum_generator.sec9_data import SEC9_DAYS

    # Day 98: Iterative Tree Traversals via Explicit Stack
    d98 = {
        "summary": "Iterative Tree Traversals simulate the system recursion call stack using an explicit Python list to prevent RecursionError on skewed trees of depth up to N.",
        "mechanics": "Iterative In-Order: push nodes onto stack while descending down the left spine (`curr = curr.left`). When curr is None, pop from stack, process node value, and move to right child (`curr = node.right`). The stack holds at most H nodes at any moment, guaranteeing O(N) time and O(H) space.",
        "takeaway": "Simulating the call stack with a while loop and explicit list eliminates Python's recursion limit while matching DFS performance.",
        "sample_code": "# Iterative In-Order Traversal via Explicit Stack\ndef inorder_iterative(root):\n    res, stack = [], []\n    curr = root\n    while curr or stack:\n        while curr:\n            stack.append(curr)\n            curr = curr.left\n        curr = stack.pop()\n        res.append(curr.val)\n        curr = curr.right\n    return res",
        "q1": "Why is an explicit stack loop preferred over recursion when processing unbalanced, deep trees in production Python environments?",
        "q1_opts": [
            {"id": "A", "label": "Python enforces a default call stack limit (1000 frames); recursion on a skewed tree of depth 10,000 raises RecursionError, whereas an explicit heap-allocated list can hold millions of elements"},
            {"id": "B", "label": "Because iterative loops run in O(1) time"},
            {"id": "C", "label": "Because explicit stacks sort the tree nodes"},
            {"id": "D", "label": "Because recursion does not work on binary trees"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! Python's interpreter terminates with RecursionError when stack depth exceeds sys.getrecursionlimit() (typically 1000). Allocating an explicit stack on the heap handles arbitrarily deep degenerate trees safely.",
            "B": "Incorrect: Visiting N nodes strictly requires O(N) operations.",
            "C": "Incorrect: In-order traversal yields sorted order on BSTs specifically, not arbitrary binary trees.",
            "D": "Incorrect: Recursion is the natural representation of tree anatomy."
        },
        "q2": "In the iterative in-order template, when `curr` becomes `None`, what is the invariant governing the next step?",
        "q2_opts": [
            {"id": "A", "label": "The node at the top of the stack is the leftmost unvisited ancestor whose left subtree is completely exhausted; popping it visits that node before moving to its right child"},
            {"id": "B", "label": "The tree traversal is finished and the loop must break"},
            {"id": "C", "label": "curr must be reset to root"},
            {"id": "D", "label": "stack must be cleared"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! When `curr` is None, we have reached the bottom of the current left branch. The top of the stack is the immediate parent, ready to be processed before exploring its right branch.",
            "B": "Incorrect: Traversal completes only when BOTH curr is None AND stack is empty.",
            "C": "Incorrect: Resetting to root causes infinite loops.",
            "D": "Incorrect: Clearing the stack loses remaining parent nodes."
        },
        "practice_task": "Implement iterative in-order tree traversal using an explicit stack.",
        "starter": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef inorder_traversal(root: TreeNode) -> list[int]:\n    # TODO: Implement iterative in-order using explicit stack\n    return []\n\n# Tree: 1 -> right: 2 (left: 3) -> In-order: [1, 3, 2]\nt = TreeNode(1, None, TreeNode(2, TreeNode(3), None))\nprint('In-order:', inorder_traversal(t))\n",
        "solution": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef inorder_traversal(root: TreeNode) -> list[int]:\n    res, stack = [], []\n    curr = root\n    while curr or stack:\n        while curr:\n            stack.append(curr)\n            curr = curr.left\n        curr = stack.pop()\n        res.append(curr.val)\n        curr = curr.right\n    return res\n\nt = TreeNode(1, None, TreeNode(2, TreeNode(3), None))\nprint('In-order:', inorder_traversal(t))\n",
        "patterns": ["In-order: [1, 3, 2]"],
        "hint": "Loop while curr or stack: while curr: stack.append(curr); curr = curr.left. curr = stack.pop(); res.append(curr.val); curr = curr.right.",
        "recap": [
            {"concept": "Left-Spine Descent", "naiveIntuition": "Pop and push simultaneously", "pythonReality": "Pushing all left children before processing matches recursive call-stack activation records"},
            {"concept": "Heap-Allocated Safety", "naiveIntuition": "Recursion is always better in Python", "pythonReality": "Deep recursion risks call stack exhaustion; explicit loops on heap memory provide enterprise resilience"}
        ]
    }

    # Day 99: BFS & Level-Order Queue Traversal
    d99 = SEC9_DAYS[98] # was level order at 98

    # Day 100: Tree Properties: Height, Diameter & Symmetry
    d100 = SEC9_DAYS[100] # was diameter at 100

    # Day 101: BST Invariant & Search
    d101 = SEC9_DAYS[103] # was BST invariant at 103

    # Day 102: BST Insertion, Deletion & Successor Rewiring
    d102 = SEC9_DAYS[104] # was BST search/insert/delete at 104

    # Day 103: Lowest Common Ancestor (LCA) in BST and Tree
    d103 = SEC9_DAYS[102] # was LCA in binary tree at 102

    # Day 104: Tree Serialization & Deserialization
    d104 = SEC9_DAYS[108] # was serialization at 108

    # Day 105: Morris In-Order Traversal & Threaded Pointers
    d105 = SEC9_DAYS[105] # was Morris at 105

    # Day 106: Balanced BSTs: AVL Tree Rotations (LL, RR)
    d106 = SEC9_DAYS[109] # was AVL at 109

    # Day 107: Red-Black Tree Principles & Invariants
    d107 = {
        "summary": "Red-Black Trees maintain approximate balance through local node coloring invariants, guaranteeing worst-case O(log N) operations with fewer tree rotations on updates than AVL trees.",
        "mechanics": "The 5 Red-Black Invariants: (1) Every node is RED or BLACK. (2) The root is always BLACK. (3) Every leaf (None) is BLACK. (4) If a node is RED, both its children are BLACK (no two consecutive red nodes). (5) For each node, all paths from that node to descendant leaves contain the SAME number of black nodes (Black-Height). Tree height is strictly bounded: H <= 2 * log2(N + 1).",
        "takeaway": "Equal black-height across all paths bounds the maximum path length to at most twice the minimum path length.",
        "sample_code": "# Red-Black Tree Invariants Verification\ndef verify_black_height(node):\n    if not node: return 0\n    left_bh = verify_black_height(node.left)\n    right_bh = verify_black_height(node.right)\n    if left_bh != right_bh: raise ValueError('Black height mismatch!')\n    return left_bh + (1 if node.color == 'BLACK' else 0)",
        "q1": "Why does the invariant 'no two consecutive red nodes' combined with 'equal black-height' guarantee balanced O(log N) search time?",
        "q1_opts": [
            {"id": "A", "label": "The shortest possible path consists entirely of black nodes (length BH), while the longest possible path alternates red and black (length 2 * BH), bounding maximum depth to at most 2 * log2(N + 1)"},
            {"id": "B", "label": "Because red nodes are deleted after insertion"},
            {"id": "C", "label": "Because black nodes do not count towards tree height"},
            {"id": "D", "label": "Because red-black trees are perfectly symmetric complete trees"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! Since red nodes cannot have red children, you can never have two red nodes in a row. The longest path can at most double the shortest path length (2 * BH). Hence height is strictly bounded within 2 * log2(N + 1) = O(log N).",
            "B": "Incorrect: Nodes remain in the tree with their assigned colors.",
            "C": "Incorrect: All nodes contribute to operational depth.",
            "D": "Incorrect: Red-black trees are approximately balanced, not complete trees."
        },
        "q2": "Why do production systems (like Java's TreeMap and C++'s std::map) prefer Red-Black Trees over AVL Trees for general-purpose associative containers?",
        "q2_opts": [
            {"id": "A", "label": "Red-Black trees require at most 2 rotations per insertion and at most 3 rotations per deletion, resulting in faster write/update throughput than more rigidly balanced AVL trees"},
            {"id": "B", "label": "Because AVL trees cannot store integers"},
            {"id": "C", "label": "Because Red-Black trees use 0 memory"},
            {"id": "D", "label": "Because Red-Black trees are faster at lookups than AVL trees"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! AVL trees are more rigidly balanced, which makes lookups slightly faster, but frequent updates trigger cascade rotations up to O(log N). Red-Black trees bound rotations to O(1) constant rotations per mutation.",
            "B": "Incorrect: AVL trees store all comparable keys.",
            "C": "Incorrect: Node color requires at least 1 bit.",
            "D": "Incorrect: AVL trees have strictly shallower height, making pure lookups marginally faster."
        },
        "practice_task": "Implement Black-Height Verification to validate whether a colored binary tree satisfies the Red-Black Black-Height invariant.",
        "starter": "class RBNode:\n    def __init__(self, val, color='BLACK', left=None, right=None):\n        self.val = val\n        self.color = color  # 'RED' or 'BLACK'\n        self.left = left\n        self.right = right\n\ndef is_valid_black_height(root: RBNode) -> bool:\n    # TODO: Return True if all root-to-leaf paths have identical count of BLACK nodes\n    return False\n\n# Root(B) -> left: 1(B), right: 3(R -> left: 2(B))\n# Path 1: B -> B = 2 black nodes. Path 2: B -> R -> B = 2 black nodes. Valid!\nvalid_tree = RBNode(2, 'BLACK', RBNode(1, 'BLACK'), RBNode(3, 'RED', RBNode(2.5, 'BLACK')))\nprint('Is valid black height:', is_valid_black_height(valid_tree)) # True\n",
        "solution": "class RBNode:\n    def __init__(self, val, color='BLACK', left=None, right=None):\n        self.val = val\n        self.color = color\n        self.left = left\n        self.right = right\n\ndef is_valid_black_height(root: RBNode) -> bool:\n    def check(node):\n        if not node:\n            return 1 # Null leaves are black\n        lb = check(node.left)\n        rb = check(node.right)\n        if lb == -1 or rb == -1 or lb != rb:\n            return -1\n        return lb + (1 if node.color == 'BLACK' else 0)\n    return check(root) != -1\n\nvalid_tree = RBNode(2, 'BLACK', RBNode(1, 'BLACK'), RBNode(3, 'RED', RBNode(2.5, 'BLACK')))\nprint('Is valid black height:', is_valid_black_height(valid_tree))\n",
        "patterns": ["Is valid black height: True"],
        "hint": "Helper check(node) returns black-height or -1 if mismatch. If not node return 1. If check(left) != check(right) return -1. Add 1 if node.color == 'BLACK'.",
        "recap": [
            {"concept": "Black-Height Balance Invariant", "naiveIntuition": "Trees must be strictly balanced at every single node", "pythonReality": "Equalizing black-height bounds depth to within a 2x factor, delivering logarithmic guarantees with minimal rotation overhead"},
            {"concept": "Mutation Rotation Bound", "naiveIntuition": "Balancing always requires rotating the entire tree", "pythonReality": "Red-Black re-coloring absorbs most updates; at most 2 or 3 rotations are ever needed per insert/delete"}
        ]
    }

    # Day 108: Tries (Prefix Trees): Structure & Lookup
    d108 = {
        "summary": "Tries (Prefix Trees) organize strings character-by-character where common prefixes share common ancestor nodes, enabling O(L) search, prefix matching, and insertion independent of dictionary size N.",
        "mechanics": "Each TrieNode contains `children = {}` (mapping char to child node) and boolean `is_end = False`. Insertion walks down the character path, creating nodes as needed. Lookup verifies the path exists. Prefix queries check path existence without requiring `is_end`.",
        "takeaway": "Tries achieve O(L) prefix search proportional solely to word length L, bypassing expensive scans across N dictionary entries.",
        "sample_code": "# Trie Prefix Tree\nclass TrieNode:\n    def __init__(self):\n        self.children = {}\n        self.is_end = False\n\nclass Trie:\n    def __init__(self):\n        self.root = TrieNode()\n    def insert(self, word):\n        curr = self.root\n        for ch in word:\n            curr = curr.children.setdefault(ch, TrieNode())\n        curr.is_end = True\n    def search(self, word):\n        curr = self.root\n        for ch in word:\n            if ch not in curr.children: return False\n            curr = curr.children[ch]\n        return curr.is_end",
        "q1": "Why is Trie search time complexity O(L) where L is query length, rather than depending on the number of stored words N?",
        "q1_opts": [
            {"id": "A", "label": "Each character lookup follows a direct dictionary pointer in O(1) time down a tree branch of depth L, never inspecting unrelated branches"},
            {"id": "B", "label": "Because the Trie sorts all words in memory"},
            {"id": "C", "label": "Because N is always smaller than L"},
            {"id": "D", "label": "Because Tries use binary search on strings"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! Whether the Trie stores 10 words or 10,000,000 words, searching for a 4-letter prefix like 'code' performs exactly 4 child lookups down the matching branch, taking strictly O(L) time.",
            "B": "Incorrect: Tries do not require array sorting.",
            "C": "Incorrect: Word count N is typically much larger than word length L.",
            "D": "Incorrect: Tries use hash/array indexing at each node, not binary search."
        },
        "q2": "What distinguishes `search(word)` from `starts_with(prefix)` in a Trie?",
        "q2_opts": [
            {"id": "A", "label": "search(word) requires `curr.is_end == True` at the final node, while starts_with(prefix) only requires the character path to exist"},
            {"id": "B", "label": "starts_with is O(N) while search is O(1)"},
            {"id": "C", "label": "search checks suffixes instead of prefixes"},
            {"id": "D", "label": "There is no difference"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! If 'apple' is inserted, 'app' is a valid prefix (`starts_with('app') == True`), but not a complete word (`search('app') == False`) until explicitly marked `is_end = True`.",
            "B": "Incorrect: Both operations run in O(L) time.",
            "C": "Incorrect: Both traverse from prefix root downward.",
            "D": "Incorrect: The `is_end` check differentiates words from intermediate prefixes."
        },
        "practice_task": "Implement a complete Trie supporting insert, search, and starts_with.",
        "starter": "class TrieNode:\n    def __init__(self):\n        self.children = {}\n        self.is_end = False\n\nclass Trie:\n    def __init__(self):\n        self.root = TrieNode()\n\n    # TODO: Implement insert, search, and starts_with\n\nt = Trie()\nt.insert('code')\nprint('Search code:', t.search('code'))       # True\nprint('Search cod:', t.search('cod'))         # False\nprint('Starts with cod:', t.starts_with('cod')) # True\n",
        "solution": "class TrieNode:\n    def __init__(self):\n        self.children = {}\n        self.is_end = False\n\nclass Trie:\n    def __init__(self):\n        self.root = TrieNode()\n\n    def insert(self, word: str) -> None:\n        curr = self.root\n        for ch in word:\n            if ch not in curr.children:\n                curr.children[ch] = TrieNode()\n            curr = curr.children[ch]\n        curr.is_end = True\n\n    def search(self, word: str) -> bool:\n        curr = self.root\n        for ch in word:\n            if ch not in curr.children:\n                return False\n            curr = curr.children[ch]\n        return curr.is_end\n\n    def starts_with(self, prefix: str) -> bool:\n        curr = self.root\n        for ch in prefix:\n            if ch not in curr.children:\n                return False\n            curr = curr.children[ch]\n        return True\n\nt = Trie()\nt.insert('code')\nprint('Search code:', t.search('code'))\nprint('Search cod:', t.search('cod'))\nprint('Starts with cod:', t.starts_with('cod'))\n",
        "patterns": ["Search code: True", "Search cod: False", "Starts with cod: True"],
        "hint": "In insert: loop ch, setdefault TrieNode(), set is_end = True. In search: verify path exists and return curr.is_end. In starts_with: verify path exists and return True.",
        "recap": [
            {"concept": "Prefix Consolidation", "naiveIntuition": "Store words in an array and use string.startswith()", "pythonReality": "Tries consolidate overlapping prefixes into shared tree nodes, collapsing redundant scans into O(L) lookups"},
            {"concept": "Word Boundary Disambiguation", "naiveIntuition": "Reaching a node means the word exists", "pythonReality": "Only nodes with is_end == True denote complete stored words; intermediate nodes represent valid prefixes"}
        ]
    }

    # Day 109: Trie Applications: Autocomplete & Wildcards
    d109 = {
        "summary": "Trie Applications extend basic prefix matching to support Autocomplete suggestions and Wildcard Pattern Search (matching '.' to any character) via DFS branching.",
        "mechanics": "Wildcard Search: for literal characters, follow `curr.children[ch]`. For wildcard `'.'`: recurse across ALL available child branches in `curr.children.values()`. If any branch matches the remaining pattern, return True. Autocomplete: descend to the prefix node, then launch a DFS to collect all descendant words.",
        "takeaway": "Wildcard character '.' transforms linear Trie descent into multi-branch DFS, exploring all valid phonetic avenues.",
        "sample_code": "# WordDictionary with '.' Wildcards\ndef search_wildcard(node, word, idx):\n    if idx == len(word): return node.is_end\n    ch = word[idx]\n    if ch == '.':\n        return any(search_wildcard(child, word, idx + 1) for child in node.children.values())\n    if ch in node.children:\n        return search_wildcard(node.children[ch], word, idx + 1)\n    return False",
        "q1": "What is the worst-case time complexity of searching a pattern consisting entirely of wildcards '...' in a Trie with branching factor 26?",
        "q1_opts": [
            {"id": "A", "label": "O(26^L) where L is pattern length, exploring every branch in the tree"},
            {"id": "B", "label": "O(L) linear time"},
            {"id": "C", "label": "O(N * L) space"},
            {"id": "D", "label": "O(1) constant time"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! With all wildcards, the search cannot prune any character branches, forcing DFS to explore all available child branches down to depth L. For 26 letters, worst case is O(26^L).",
            "B": "Incorrect: That applies to literal queries without wildcards.",
            "C": "Incorrect: Time complexity is exponential.",
            "D": "Incorrect: Must traverse tree branches."
        },
        "q2": "In an Autocomplete system, what is the first step before collecting word suggestions?",
        "q2_opts": [
            {"id": "A", "label": "Descend down the Trie along the prefix characters; if the prefix path exists, the target node is the root of the suggestion subtree"},
            {"id": "B", "label": "Sort all words in the dictionary alphabetically"},
            {"id": "C", "label": "Delete words with different lengths"},
            {"id": "D", "label": "Convert all words to lowercase integers"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! Finding the prefix node in O(L) isolates the exact subtree containing all words beginning with that prefix. Subtree DFS then collects candidate completions.",
            "B": "Incorrect: The Trie structure already enforces prefix clustering.",
            "C": "Incorrect: Autocomplete words have variable lengths.",
            "D": "Incorrect: Trie processes string characters directly."
        },
        "practice_task": "Build a WordDictionary supporting '.' wildcards matching any single letter.",
        "starter": "class TrieNode:\n    def __init__(self):\n        self.children = {}\n        self.is_end = False\n\nclass WordDictionary:\n    def __init__(self):\n        self.root = TrieNode()\n\n    def add_word(self, word: str) -> None:\n        # TODO: Insert word into Trie\n        pass\n\n    def search(self, word: str) -> bool:\n        # TODO: Search word where '.' matches any character\n        return False\n\nwd = WordDictionary()\nwd.add_word('bad')\nwd.add_word('dad')\nwd.add_word('mad')\nprint('Search pad:', wd.search('pad')) # False\nprint('Search bad:', wd.search('bad')) # True\nprint('Search .ad:', wd.search('.ad')) # True\nprint('Search b..:', wd.search('b..')) # True\n",
        "solution": "class TrieNode:\n    def __init__(self):\n        self.children = {}\n        self.is_end = False\n\nclass WordDictionary:\n    def __init__(self):\n        self.root = TrieNode()\n\n    def add_word(self, word: str) -> None:\n        curr = self.root\n        for ch in word:\n            if ch not in curr.children:\n                curr.children[ch] = TrieNode()\n            curr = curr.children[ch]\n        curr.is_end = True\n\n    def search(self, word: str) -> bool:\n        def dfs(idx, node):\n            if idx == len(word):\n                return node.is_end\n            ch = word[idx]\n            if ch == '.':\n                for child in node.children.values():\n                    if dfs(idx + 1, child):\n                        return True\n                return False\n            if ch not in node.children:\n                return False\n            return dfs(idx + 1, node.children[ch])\n        return dfs(0, self.root)\n\nwd = WordDictionary()\nwd.add_word('bad')\nwd.add_word('dad')\nwd.add_word('mad')\nprint('Search pad:', wd.search('pad'))\nprint('Search bad:', wd.search('bad'))\nprint('Search .ad:', wd.search('.ad'))\nprint('Search b..:', wd.search('b..'))\n",
        "patterns": ["Search pad: False", "Search bad: True", "Search .ad: True", "Search b..: True"],
        "hint": "In search: helper dfs(idx, node). If idx == len(word) return node.is_end. If ch == '.': for child in node.children.values(): if dfs(idx+1, child) return True; return False. Else if ch in node.children return dfs(idx+1, node.children[ch]).",
        "recap": [
            {"concept": "Multi-Branch Pruning", "naiveIntuition": "Wildcards require regex searches across all words", "pythonReality": "Trie-guided DFS branches only on existing letters at each step, pruning dead branches immediately"},
            {"concept": "Subtree Scoping", "naiveIntuition": "Autocomplete checks every word in dictionary", "pythonReality": "Walking the prefix path scopes the search to exactly the descendant subtree, ignoring 99% of unrelated words"}
        ]
    }

    # Day 110: Review
    d110 = SEC9_DAYS[110]

    new_dict = {
        96: SEC9_DAYS[96],
        97: SEC9_DAYS[97],
        98: d98,
        99: d99,
        100: d100,
        101: d101,
        102: d102,
        103: d103,
        104: d104,
        105: d105,
        106: d106,
        107: d107,
        108: d108,
        109: d109,
        110: d110
    }

    code = '"""\nSection 9: Trees & Binary Search Trees (Days 96 to 110)\n"""\n\nSEC9_DAYS = ' + pprint.pformat(new_dict, indent=4, width=120) + "\n"
    with open("scratch/curriculum_generator/sec9_data.py", "w", encoding="utf-8") as f:
        f.write(code)
    print("sec9_data.py re-aligned successfully!")


# ---------------------------------------------------------------------------
# Section 10 (Heaps & Priority Queues: Days 111-120)
# ---------------------------------------------------------------------------
def fix_sec10():
    from scratch.curriculum_generator.sec10_data import SEC10_DAYS

    # Day 114: Top K Frequent Elements in Data Streams
    d114 = SEC10_DAYS[115] # Top-K Frequent was at 115
    # Day 115: Merge K Sorted Lists via Min-Heap
    d115 = SEC10_DAYS[116] # Merge K was at 116
    # Day 116: Two-Heap Pattern: Median of a Stream
    d116 = SEC10_DAYS[117] # Median was at 117
    # Day 117: Task Scheduler & Priority Reorganization
    d117 = SEC10_DAYS[118] # Task scheduler was at 118

    # Day 118: Indexed Priority Queue Principles (decrease_key)
    d118 = {
        "summary": "Indexed Priority Queues associate an inverted index map (key to heap-array position) with a binary heap, enabling O(log N) decrease_key priority updates and arbitrary key removals.",
        "mechanics": "Standard heaps require O(N) linear scans to find an item before updating its priority. An Indexed Priority Queue maintains `pos = {item: index}` tracking where each item sits in the flat `heap` array. Whenever items swap during sift-up or sift-down, their positions in `pos` are updated simultaneously in O(1). This unlocks O(log N) `change_priority()` essential for Dijkstra and A* search.",
        "takeaway": "Maintaining a reverse index map pos[item] = heap_idx enables O(log N) decrease_key priority updates.",
        "sample_code": "# Indexed Priority Queue Skeleton\nclass IndexedPQ:\n    def __init__(self):\n        self.heap = []       # [(priority, item)]\n        self.pos = {}        # {item: heap_index}\n    def swap(self, i, j):\n        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]\n        self.pos[self.heap[i][1]] = i\n        self.pos[self.heap[j][1]] = j\n    def decrease_key(self, item, new_p):\n        idx = self.pos[item]\n        self.heap[idx] = (new_p, item)\n        # sift-up from idx in O(log N)\n        while idx > 0:\n            p = (idx - 1) // 2\n            if self.heap[idx][0] < self.heap[p][0]:\n                self.swap(idx, p); idx = p\n            else: break",
        "q1": "Why does Python's standard `heapq` module NOT provide a built-in `decrease_key` operation?",
        "q1_opts": [
            {"id": "A", "label": "Standard heapq operates on plain Python lists without maintaining a secondary hash table of item-to-index positions; finding an element requires an O(N) scan"},
            {"id": "B", "label": "Because priorities cannot decrease in computer science"},
            {"id": "C", "label": "Because Python lists cannot swap elements"},
            {"id": "D", "label": "Because heaps are strictly immutable in Python"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! Without a reverse lookup dictionary `pos[item] = index`, locating the item inside the heap list takes O(N) linear time, destroying logarithmic efficiency. Python developers use lazy deletion or indexed priority queues instead.",
            "B": "Incorrect: decrease_key is the foundational primitive of Dijkstra's algorithm.",
            "C": "Incorrect: Python list element swapping is O(1).",
            "D": "Incorrect: Python lists are mutable."
        },
        "q2": "What is the time complexity of `decrease_key` in an Indexed Priority Queue with N elements?",
        "q2_opts": [
            {"id": "A", "label": "O(log N) time, because pos[item] locates the index in O(1) and sift-up travels at most the tree height H = log2 N"},
            {"id": "B", "label": "O(N) time"},
            {"id": "C", "label": "O(N log N) time"},
            {"id": "D", "label": "O(1) time"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! The hash map gives the heap index in O(1) time. Updating the value and bubbling up towards the root takes O(log N) swaps.",
            "B": "Incorrect: O(N) is the cost in unindexed heaps.",
            "C": "Incorrect: Re-heapifying the entire array takes O(N), but sift-up is O(log N).",
            "D": "Incorrect: Fibonacci heaps achieve amortized O(1) decrease-key, but standard binary IPQs are O(log N)."
        },
        "practice_task": "Implement an Indexed Priority Queue with O(log N) decrease_key support.",
        "starter": "class IndexedMinPQ:\n    def __init__(self):\n        self.heap = []  # list of [priority, item]\n        self.pos = {}   # item -> index in heap\n\n    # TODO: Implement push, pop_min, and decrease_key(item, new_priority)\n\npq = IndexedMinPQ()\n# Test usage\n",
        "solution": "class IndexedMinPQ:\n    def __init__(self):\n        self.heap = []\n        self.pos = {}\n\n    def _swap(self, i: int, j: int) -> None:\n        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]\n        self.pos[self.heap[i][1]] = i\n        self.pos[self.heap[j][1]] = j\n\n    def push(self, item: str, priority: int) -> None:\n        idx = len(self.heap)\n        self.heap.append([priority, item])\n        self.pos[item] = idx\n        self._sift_up(idx)\n\n    def _sift_up(self, idx: int) -> None:\n        while idx > 0:\n            parent = (idx - 1) // 2\n            if self.heap[idx][0] < self.heap[parent][0]:\n                self._swap(idx, parent)\n                idx = parent\n            else:\n                break\n\n    def decrease_key(self, item: str, new_priority: int) -> None:\n        if item in self.pos:\n            idx = self.pos[item]\n            if new_priority < self.heap[idx][0]:\n                self.heap[idx][0] = new_priority\n                self._sift_up(idx)\n\n    def pop_min(self) -> tuple[int, str]:\n        min_entry = self.heap[0]\n        last_entry = self.heap.pop()\n        del self.pos[min_entry[1]]\n        if self.heap:\n            self.heap[0] = last_entry\n            self.pos[last_entry[1]] = 0\n            self._sift_down(0)\n        return tuple(min_entry)\n\n    def _sift_down(self, idx: int) -> None:\n        n = len(self.heap)\n        while 2 * idx + 1 < n:\n            smallest = idx\n            left = 2 * idx + 1\n            right = 2 * idx + 2\n            if left < n and self.heap[left][0] < self.heap[smallest][0]:\n                smallest = left\n            if right < n and self.heap[right][0] < self.heap[smallest][0]:\n                smallest = right\n            if smallest != idx:\n                self._swap(idx, smallest)\n                idx = smallest\n            else:\n                break\n\npq = IndexedMinPQ()\npq.push('task_A', 10)\npq.push('task_B', 20)\npq.decrease_key('task_B', 5) # task_B promoted to priority 5!\nprint('Next task:', pq.pop_min()) # (5, 'task_B')\nprint('Next task:', pq.pop_min()) # (10, 'task_A')\n",
        "patterns": ["Next task: (5, 'task_B')", "Next task: (10, 'task_A')"],
        "hint": "Track self.pos[item] = idx during swaps. In decrease_key(item, new_p): set heap[idx][0] = new_p and call _sift_up(idx).",
        "recap": [
            {"concept": "Inverted Heap Indexing", "naiveIntuition": "Heaps only support accessing the root element", "pythonReality": "Maintaining a parallel dictionary of item-to-index pointers unlocks O(log N) updates to arbitrary elements in the heap"},
            {"concept": "Heap Mutation Parity", "naiveIntuition": "Re-sorting the array on priority updates is fine", "pythonReality": "Full re-heapify takes O(N); single-element sift-up takes O(log N), making shortest path graph algorithms viable at production scale"}
        ]
    }

    new_dict = {
        111: SEC10_DAYS[111],
        112: SEC10_DAYS[112],
        113: SEC10_DAYS[113],
        114: d114,
        115: d115,
        116: d116,
        117: d117,
        118: d118,
        119: SEC10_DAYS[119],
        120: SEC10_DAYS[120]
    }

    code = '"""\nSection 10: Heaps & Priority Queues (Days 111 to 120)\n"""\n\nSEC10_DAYS = ' + pprint.pformat(new_dict, indent=4, width=120) + "\n"
    with open("scratch/curriculum_generator/sec10_data.py", "w", encoding="utf-8") as f:
        f.write(code)
    print("sec10_data.py re-aligned successfully!")

if __name__ == "__main__":
    fix_sec9()
    fix_sec10()
