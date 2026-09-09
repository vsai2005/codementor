"""
Fix and re-align all section data files in scratch/curriculum_generator/
to guarantee 100% synchronization with curriculum_160.json.
"""

import pprint

# ---------------------------------------------------------------------------
# Section 11 (Graphs: Days 121-135)
# ---------------------------------------------------------------------------
def fix_sec11():
    from scratch.curriculum_generator.sec11_data import SEC11_DAYS

    bipartite = SEC11_DAYS[132]
    dijkstra = SEC11_DAYS[127]
    bellman = SEC11_DAYS[128]
    dsu = SEC11_DAYS[129]
    kruskal = SEC11_DAYS[130]
    prim = SEC11_DAYS[131]

    # Day 124: 3-Color Directed Cycle Detection
    cycle_124 = {
        "summary": "Cycle Detection in Directed Graphs uses DFS 3-Coloring (White, Gray, Black) to detect back-edges to active ancestors currently on the recursion call stack in O(V + E) time.",
        "mechanics": "Every vertex has one of three states: 0=WHITE (unvisited), 1=GRAY (currently being explored on call stack), 2=BLACK (completely processed and backtrack completed). During DFS from vertex u, if we encounter an adjacent vertex v that is GRAY (visited[v] == 1), an active back-edge exists, confirming a directed cycle.",
        "takeaway": "A directed cycle exists if and only if DFS encounters a back-edge to a GRAY ancestor currently on the call stack.",
        "sample_code": "# 3-Color Cycle Detection in Directed Graph\ndef has_cycle(n, adj):\n    visited = [0] * n  # 0=White, 1=Gray, 2=Black\n    def dfs(u):\n        visited[u] = 1 # Mark Gray\n        for v in adj[u]:\n            if visited[v] == 1: return True  # Cycle detected!\n            if visited[v] == 0 and dfs(v): return True\n        visited[u] = 2 # Mark Black\n        return False\n    return any(visited[i] == 0 and dfs(i) for i in range(n))",
        "q1": "Why is a simple 2-state boolean visited array (True/False) INSUFFICIENT for cycle detection in DIRECTED graphs?",
        "q1_opts": [
            {"id": "A", "label": "A True entry could be a cross-edge or forward-edge to a previously finished node that does not form a cycle; only edges to active ancestors on the current call stack form cycles"},
            {"id": "B", "label": "Because directed graphs cannot be traversed with DFS"},
            {"id": "C", "label": "Because booleans take more memory than integers"},
            {"id": "D", "label": "Because directed graphs always have cycles"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! In directed graphs, reaching an already-visited vertex via a cross-edge (e.g. 1 -> 2 and 1 -> 3 -> 2) is completely acyclic. Cycles occur ONLY when an edge points back to an active ancestor currently in state GRAY.",
            "B": "Incorrect: DFS is the canonical algorithm for directed graphs.",
            "C": "Incorrect: Memory representation is irrelevant to cycle geometry.",
            "D": "Incorrect: Directed Acyclic Graphs (DAGs) have zero cycles."
        },
        "q2": "What does state BLACK (visited[u] == 2) signify in the 3-coloring algorithm?",
        "q2_opts": [
            {"id": "A", "label": "All descendants reachable from vertex u have been fully explored with zero cycles found, so u can be safely pruned from future inspection"},
            {"id": "B", "label": "A cycle has been found at vertex u"},
            {"id": "C", "label": "Vertex u has no outgoing edges"},
            {"id": "D", "label": "Vertex u is the root of the graph"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! Once all neighbors of u are verified acyclic, u transitions from Gray to Black. Any subsequent edge encountering a Black vertex can safely prune that branch immediately.",
            "B": "Incorrect: Gray-to-Gray transitions detect cycles.",
            "C": "Incorrect: Nodes with out-degree > 0 transition to Black after exploration.",
            "D": "Incorrect: Any node transitions to Black when its subtree completes."
        },
        "practice_task": "Detect whether a directed course prerequisite graph contains a cycle (Deadlock Detection).",
        "starter": "def can_finish_courses(num_courses: int, prerequisites: list[list[int]]) -> bool:\n    adj = {i: [] for i in range(num_courses)}\n    for crs, pre in prerequisites:\n        adj[pre].append(crs)\n    visited = [0] * num_courses  # 0=White, 1=Gray, 2=Black\n    # TODO: Implement 3-color DFS to return True if no cycles, False if cycle exists\n    return True\n\nprint('Can finish [0->1, 1->0]:', can_finish_courses(2, [[1, 0], [0, 1]])) # False\nprint('Can finish [0->1, 1->2]:', can_finish_courses(3, [[1, 0], [2, 1]])) # True\n",
        "solution": "def can_finish_courses(num_courses: int, prerequisites: list[list[int]]) -> bool:\n    adj = {i: [] for i in range(num_courses)}\n    for crs, pre in prerequisites:\n        adj[pre].append(crs)\n    visited = [0] * num_courses\n    def dfs(u):\n        visited[u] = 1\n        for v in adj[u]:\n            if visited[v] == 1:\n                return False\n            if visited[v] == 0 and not dfs(v):\n                return False\n        visited[u] = 2\n        return True\n    for i in range(num_courses):\n        if visited[i] == 0:\n            if not dfs(i):\n                return False\n    return True\n\nprint('Can finish [0->1, 1->0]:', can_finish_courses(2, [[1, 0], [0, 1]]))\nprint('Can finish [0->1, 1->2]:', can_finish_courses(3, [[1, 0], [2, 1]]))\n",
        "patterns": ["Can finish [0->1, 1->0]: False", "Can finish [0->1, 1->2]: True"],
        "hint": "In dfs(u): mark visited[u] = 1. For v in adj[u]: if visited[v] == 1 return False; if visited[v] == 0 and not dfs(v) return False. visited[u] = 2. Return True. Check all courses i in range(n).",
        "recap": [
            {"concept": "Recursion Stack Invariant", "naiveIntuition": "Any visited node means a cycle", "pythonReality": "Only nodes currently in the recursion stack (Gray) indicate cycles; already completed nodes (Black) are safe cross-edges"},
            {"concept": "Topological Equivalency", "naiveIntuition": "Cycle detection is unrelated to topo sort", "pythonReality": "A directed graph has a cycle if and only if a valid topological ordering does NOT exist"}
        ]
    }

    new_dict = dict(SEC11_DAYS)
    new_dict[124] = cycle_124
    new_dict[127] = bipartite
    new_dict[128] = dijkstra
    new_dict[129] = bellman
    new_dict[130] = dsu
    new_dict[131] = kruskal
    new_dict[132] = prim

    code = '"""\nSection 11: Graph Algorithms (Days 121 to 135)\n"""\n\nSEC11_DAYS = ' + pprint.pformat(new_dict, indent=4, width=120) + "\n"
    with open("scratch/curriculum_generator/sec11_data.py", "w", encoding="utf-8") as f:
        f.write(code)
    print("sec11_data.py re-aligned successfully!")


# ---------------------------------------------------------------------------
# Section 13 (Dynamic Programming: Days 146-155)
# ---------------------------------------------------------------------------
def fix_sec13():
    from scratch.curriculum_generator.sec13_data import SEC13_DAYS

    # In sec13:
    # 148 was Coin Change
    # 149 was LIS
    # 150 was 2D Grid DP
    # 151 was 0/1 Knapsack
    # Target:
    # 148 = 2D Grid DP
    # 149 = 0/1 Knapsack
    # 150 = Coin Change
    # 151 = LIS
    grid_dp = SEC13_DAYS[150]
    knapsack = SEC13_DAYS[151]
    coin_change = SEC13_DAYS[148]
    lis = SEC13_DAYS[149]

    new_dict = dict(SEC13_DAYS)
    new_dict[148] = grid_dp
    new_dict[149] = knapsack
    new_dict[150] = coin_change
    new_dict[151] = lis

    code = '"""\nSection 13: Dynamic Programming (Days 146 to 155)\n"""\n\nSEC13_DAYS = ' + pprint.pformat(new_dict, indent=4, width=120) + "\n"
    with open("scratch/curriculum_generator/sec13_data.py", "w", encoding="utf-8") as f:
        f.write(code)
    print("sec13_data.py re-aligned successfully!")


# ---------------------------------------------------------------------------
# Section 14 (Advanced DSA & Capstones: Days 156-160)
# ---------------------------------------------------------------------------
def fix_sec14():
    from scratch.curriculum_generator.sec14_data import SEC14_DAYS

    # 156: Bit Manipulation (was 158)
    bit_manip = SEC14_DAYS[158]
    # 158: Segment Trees (was 157)
    seg_tree = SEC14_DAYS[157]

    # Day 157: Backtracking & N-Queens
    nqueens_157 = {
        "summary": "Backtracking explores state-space trees depth-first, pruning invalid search branches via constraint invariants to solve combinatorial search problems like N-Queens.",
        "mechanics": "Place queens row by row from r = 0 to N - 1. A queen at (r, c) attacks column c, major diagonal (r - c), and minor diagonal (r + c). Maintain three hash sets or bitmasks (cols, diag1, diag2). If column or diagonals are occupied, skip (pruning). If r == N, record board configuration.",
        "takeaway": "Pruning candidate states early reduces exponential O(N!) exploration trees to manageable search paths.",
        "sample_code": "# N-Queens Backtracking with State Pruning\ndef solve_n_queens(n):\n    res = []\n    cols = set(); diag1 = set(); diag2 = set()\n    board = [['.'] * n for _ in range(n)]\n    def backtrack(r):\n        if r == n:\n            res.append([''.join(row) for row in board]); return\n        for c in range(n):\n            if c in cols or (r - c) in diag1 or (r + c) in diag2: continue\n            cols.add(c); diag1.add(r - c); diag2.add(r + c)\n            board[r][c] = 'Q'\n            backtrack(r + 1)\n            board[r][c] = '.'\n            cols.remove(c); diag1.remove(r - c); diag2.remove(r + c)\n    backtrack(0)\n    return res",
        "q1": "Why do the expressions (r - c) and (r + c) uniquely identify the diagonals on an N x N chessboard?",
        "q1_opts": [
            {"id": "A", "label": "All cells on any top-left to bottom-right diagonal share a constant (r - c), and all cells on any top-right to bottom-left diagonal share a constant (r + c)"},
            {"id": "B", "label": "Because chess boards are symmetric"},
            {"id": "C", "label": "Because r + c is always an even number"},
            {"id": "D", "label": "Because queens move in circles"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! Along main diagonals, moving down and right increments both r and c by 1, so (r+1) - (c+1) = r - c (constant). Along anti-diagonals, moving down and left increments r and decrements c, so (r+1) + (c-1) = r + c (constant).",
            "B": "Incorrect: Geometric invariants hold mathematically.",
            "C": "Incorrect: r + c can be odd or even.",
            "D": "Incorrect: Queens move along linear axes."
        },
        "q2": "What is the primary benefit of tracking `cols`, `diag1`, and `diag2` sets during N-Queens backtracking?",
        "q2_opts": [
            {"id": "A", "label": "O(1) conflict checks per cell placement, avoiding an O(N) scan across previous rows for each candidate column"},
            {"id": "B", "label": "It eliminates the need for recursion"},
            {"id": "C", "label": "It sorts the output boards"},
            {"id": "D", "label": "It guarantees polynomial O(N^2) total runtime"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! Checking set membership takes O(1) time. Without sets, verifying if a queen attacks existing queens requires checking 8 directional rays in O(N).",
            "B": "Incorrect: Backtracking is fundamentally recursive.",
            "C": "Incorrect: Sets are unordered.",
            "D": "Incorrect: N-Queens search space remains exponential in the worst case."
        },
        "practice_task": "Calculate the total number of distinct solutions to the N-Queens puzzle.",
        "starter": "def total_n_queens(n: int) -> int:\n    # TODO: Count valid N-Queens configurations using state pruning\n    # Track cols, diag1 (r - c), and diag2 (r + c)\n    return 0\n\nprint('Total solutions for N=4:', total_n_queens(4)) # 2\nprint('Total solutions for N=8:', total_n_queens(8)) # 92\n",
        "solution": "def total_n_queens(n: int) -> int:\n    cols = set()\n    diag1 = set()\n    diag2 = set()\n    count = 0\n    def backtrack(r):\n        nonlocal count\n        if r == n:\n            count += 1\n            return\n        for c in range(n):\n            if c in cols or (r - c) in diag1 or (r + c) in diag2:\n                continue\n            cols.add(c)\n            diag1.add(r - c)\n            diag2.add(r + c)\n            backtrack(r + 1)\n            cols.remove(c)\n            diag1.remove(r - c)\n            diag2.remove(r + c)\n    backtrack(0)\n    return count\n\nprint('Total solutions for N=4:', total_n_queens(4))\nprint('Total solutions for N=8:', total_n_queens(8))\n",
        "patterns": ["Total solutions for N=4: 2", "Total solutions for N=8: 92"],
        "hint": "Define cols, diag1, diag2 sets. In backtrack(r): if r == n increment count. For c in range(n): if safe, add to sets, recurse backtrack(r+1), remove from sets.",
        "recap": [
            {"concept": "Constraint Pruning", "naiveIntuition": "Generate all N^N queen placements and validate at the end", "pythonReality": "Pruning conflicting paths at row r prevents exploring millions of invalid branch combinations"},
            {"concept": "State Symmetry", "naiveIntuition": "Backtracking must explore every branch blindly", "pythonReality": "Exploiting horizontal reflection symmetry can cut N-Queens search time by 50%"}
        ]
    }

    # Day 159: Complex Problem Decomposition & Word Search II
    word_search_159 = {
        "summary": "Complex Problem Decomposition combines foundational data structures into cohesive pipelines, exemplified by Word Search II combining Trie prefix indexing with 2D Grid Backtracking.",
        "mechanics": "To search for a dictionary of words on an M x N board: (1) Insert all words into a Trie. (2) From each board cell, launch a DFS backtracking search guided by the Trie. (3) If current grid character is not in current TrieNode.children, prune immediately. (4) When a word is matched, add to results and prune leaf Trie nodes to optimize remaining search passes.",
        "takeaway": "Trie prefix pruning prevents exploring dead-end paths on grids, collapsing exponential searches to linear word lengths.",
        "sample_code": "# Word Search II: Trie + 2D Backtracking\nclass TrieNode:\n    def __init__(self):\n        self.children = {}; self.word = None\n\ndef find_words(board, words):\n    root = TrieNode()\n    for w in words:\n        node = root\n        for ch in w: node = node.children.setdefault(ch, TrieNode())\n        node.word = w\n    res = []\n    def dfs(r, c, node):\n        ch = board[r][c]\n        if ch not in node.children: return\n        nxt = node.children[ch]\n        if nxt.word: res.append(nxt.word); nxt.word = None\n        board[r][c] = '#'\n        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:\n            nr, nc = r + dr, c + dc\n            if 0 <= nr < len(board) and 0 <= nc < len(board[0]) and board[nr][nc] != '#':\n                dfs(nr, nc, nxt)\n        board[r][c] = ch\n    for r in range(len(board)):\n        for c in range(len(board[0])): dfs(r, c, root)\n    return res",
        "q1": "Why is matching all dictionary words simultaneously using a Trie dramatically faster than searching for each word individually using standard Word Search I?",
        "q1_opts": [
            {"id": "A", "label": "Trie prefix sharing explores common prefixes once for all words; if a 3-letter prefix does not exist on the board, thousands of words sharing that prefix are pruned in a single step"},
            {"id": "B", "label": "Because Tries sort the 2D board"},
            {"id": "C", "label": "Because Word Search I cannot find words with duplicates"},
            {"id": "D", "label": "Because individual searches consume more network bandwidth"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! If 500 words begin with 'micro', Trie-guided search explores 'micro' on the grid once. If 'mic' is not adjacent, all 500 words are discarded at depth 3, avoiding 500 separate 2D traversals.",
            "B": "Incorrect: The board is not sorted.",
            "C": "Incorrect: Word Search I handles duplicate letters.",
            "D": "Incorrect: Algorithmic time complexity within memory."
        },
        "q2": "Why do we temporarily replace `board[r][c] = '#'` during 2D grid DFS?",
        "q2_opts": [
            {"id": "A", "label": "To mark the current cell as visited within the current path without allocating an O(M * N) separate visited set, restoring it during backtrack"},
            {"id": "B", "label": "To delete the letter permanently"},
            {"id": "C", "label": "Because '#' is an ASCII wildcard"},
            {"id": "D", "label": "To prevent Python stack overflow"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! In-place grid cell mutation acts as an O(1) visited marker. Restoring `board[r][c] = ch` upon backtracking ensures the cell remains available for alternative paths.",
            "B": "Incorrect: The letter is restored during backtracking.",
            "C": "Incorrect: '#' is purely a sentinel value.",
            "D": "Incorrect: Call stack depth depends on word length, not marker values."
        },
        "practice_task": "Find all words from a dictionary present in a 2D letter board using Trie prefix backtracking.",
        "starter": "def find_words_in_board(board: list[list[str]], words: list[str]) -> list[str]:\n    # TODO: Build Trie and execute 2D DFS with prefix pruning\n    return []\n\nb = [\n    ['o', 'a', 'a', 'n'],\n    ['e', 't', 'a', 'e'],\n    ['i', 'h', 'k', 'r'],\n    ['i', 'f', 'l', 'v']\n]\nw = ['oath', 'pea', 'eat', 'rain']\nprint('Words found:', sorted(find_words_in_board(b, w))) # ['eat', 'oath']\n",
        "solution": "class TNode:\n    def __init__(self):\n        self.children = {}\n        self.word = None\n\ndef find_words_in_board(board: list[list[str]], words: list[str]) -> list[str]:\n    root = TNode()\n    for w in words:\n        node = root\n        for ch in w:\n            if ch not in node.children:\n                node.children[ch] = TNode()\n            node = node.children[ch]\n        node.word = w\n    res = []\n    R, C = len(board), len(board[0])\n    def dfs(r, c, node):\n        ch = board[r][c]\n        if ch not in node.children:\n            return\n        nxt = node.children[ch]\n        if nxt.word:\n            res.append(nxt.word)\n            nxt.word = None\n        board[r][c] = '#'\n        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:\n            nr, nc = r + dr, c + dc\n            if 0 <= nr < R and 0 <= nc < C and board[nr][nc] != '#':\n                dfs(nr, nc, nxt)\n        board[r][c] = ch\n    for r in range(R):\n        for c in range(C):\n            dfs(r, c, root)\n    return res\n\nb = [\n    ['o', 'a', 'a', 'n'],\n    ['e', 't', 'a', 'e'],\n    ['i', 'h', 'k', 'r'],\n    ['i', 'f', 'l', 'v']\n]\nw = ['oath', 'pea', 'eat', 'rain']\nprint('Words found:', sorted(find_words_in_board(b, w)))\n",
        "patterns": ["Words found: ['eat', 'oath']"],
        "hint": "Build Trie. In dfs(r, c, node): ch = board[r][c]. If ch not in node.children return. nxt = node.children[ch]. If nxt.word: append and set nxt.word = None. Mark board[r][c] = '#', recurse 4 directions, restore board[r][c] = ch.",
        "recap": [
            {"concept": "Hybrid Data Structure Design", "naiveIntuition": "Choose either a Trie or a Graph algorithm", "pythonReality": "Combining Trie prefix indexing with 2D Grid DFS eliminates redundancy and solves problems that would otherwise be computationally intractable"},
            {"concept": "In-Place Backtracking Sentinels", "naiveIntuition": "Allocate a 2D boolean array for visited cells", "pythonReality": "Overwriting board[r][c] with '#' and restoring it on return saves O(M * N) memory and allocation overhead"}
        ]
    }

    # Day 160: Production LFU Cache Capstone
    lfu_160 = {
        "summary": "The Complete Engineer Capstone: Implement a Production-Grade LFU (Least Frequently Used) Cache supporting get and put in strict O(1) time using dual Hash Maps and Doubly Linked Lists.",
        "mechanics": "An LFU Cache evicts the least frequently requested key (with ties broken by least recently used). Architecture: (1) `key_to_val` stores {key: val}. (2) `key_to_freq` stores {key: frequency}. (3) `freq_to_keys` stores {freq: OrderedDict} (or DLL) keeping keys in LRU insertion order. (4) `min_freq` scalar tracks global minimum frequency. In O(1) get/put, promote key from freq to freq + 1; on capacity overflow, evict the oldest key from `freq_to_keys[min_freq]`.",
        "takeaway": "LFU Cache with dual hash maps and OrderedDict achieves true O(1) get and put, mastering production-level memory management.",
        "sample_code": "# LFU Cache O(1) with OrderedDict\nfrom collections import defaultdict, OrderedDict\nclass LFUCache:\n    def __init__(self, capacity):\n        self.cap = capacity; self.vals = {}; self.freqs = {}\n        self.freq_keys = defaultdict(OrderedDict); self.min_freq = 0\n    def get(self, key):\n        if key not in self.vals: return -1\n        f = self.freqs[key]; self.freqs[key] = f + 1\n        del self.freq_keys[f][key]\n        if not self.freq_keys[f] and self.min_freq == f: self.min_freq += 1\n        self.freq_keys[f + 1][key] = True\n        return self.vals[key]",
        "q1": "Why is a Min-Heap INSUFFICIENT to achieve O(1) time complexity for LFU Cache operations?",
        "q1_opts": [
            {"id": "A", "label": "A min-heap requires O(log N) time to update a key's frequency and reorganize the heap, violating strict O(1) operational bounds"},
            {"id": "B", "label": "Because min-heaps cannot break ties"},
            {"id": "C", "label": "Because Python heaps only store integers"},
            {"id": "D", "label": "Because heaps cannot store keys"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! Updating frequency in a heap takes O(log N). Dual hash maps with doubly linked lists (or OrderedDict buckets) achieve strict O(1) updates, removals, and min-frequency promotions.",
            "B": "Incorrect: Heaps can break ties with timestamps, but remain O(log N).",
            "C": "Incorrect: Python heaps store any comparable tuples.",
            "D": "Incorrect: Heaps can store key-frequency pairs."
        },
        "q2": "In an LFU Cache, why is `min_freq` guaranteed to be at most incremented by 1 during a `get(key)` operation?",
        "q2_opts": [
            {"id": "A", "label": "The accessed key's frequency increases from f to f + 1; if f was min_freq and that bucket is now empty, the new minimum frequency must be f + 1"},
            {"id": "B", "label": "Because get always returns 1"},
            {"id": "C", "label": "Because all keys are promoted simultaneously"},
            {"id": "D", "label": "Because capacity is always 1"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! A single get operation increments only ONE key by exactly 1. If that bucket was the sole occupant of min_freq, the global min_freq advances to f + 1 in O(1) time without scanning.",
            "B": "Incorrect: Return value is the stored item value.",
            "C": "Incorrect: Only the queried key is promoted.",
            "D": "Incorrect: Capacity can be any positive integer."
        },
        "practice_task": "Implement a fully functional, production-ready LFU Cache supporting O(1) get and put operations.",
        "starter": "from collections import defaultdict, OrderedDict\n\nclass LFUCache:\n    def __init__(self, capacity: int):\n        self.cap = capacity\n        self.vals = {}       # key -> val\n        self.freqs = {}      # key -> freq\n        self.freq_keys = defaultdict(OrderedDict) # freq -> OrderedDict of keys\n        self.min_freq = 0\n\n    def get(self, key: int) -> int:\n        # TODO: Return val and promote frequency in O(1)\n        return -1\n\n    def put(self, key: int, value: int) -> None:\n        # TODO: Insert or update key, evicting LFU key if at capacity\n        pass\n\ncache = LFUCache(2)\ncache.put(1, 1)\ncache.put(2, 2)\nprint('Get 1 (freq 2):', cache.get(1))   # 1\ncache.put(3, 3)                         # Evicts key 2 (freq 1)\nprint('Get 2 (evicted):', cache.get(2)) # -1\nprint('Get 3 (freq 2):', cache.get(3))   # 3\nprint('160-Day Capstone Mastered:', True)\n",
        "solution": "from collections import defaultdict, OrderedDict\n\nclass LFUCache:\n    def __init__(self, capacity: int):\n        self.cap = capacity\n        self.vals = {}\n        self.freqs = {}\n        self.freq_keys = defaultdict(OrderedDict)\n        self.min_freq = 0\n\n    def _promote(self, key: int) -> None:\n        f = self.freqs[key]\n        self.freqs[key] = f + 1\n        del self.freq_keys[f][key]\n        if not self.freq_keys[f] and self.min_freq == f:\n            self.min_freq += 1\n        self.freq_keys[f + 1][key] = True\n\n    def get(self, key: int) -> int:\n        if key not in self.vals:\n            return -1\n        self._promote(key)\n        return self.vals[key]\n\n    def put(self, key: int, value: int) -> None:\n        if self.cap <= 0:\n            return\n        if key in self.vals:\n            self.vals[key] = value\n            self._promote(key)\n            return\n        if len(self.vals) >= self.cap:\n            evict_key, _ = self.freq_keys[self.min_freq].popitem(last=False)\n            del self.vals[evict_key]\n            del self.freqs[evict_key]\n        self.vals[key] = value\n        self.freqs[key] = 1\n        self.freq_keys[1][key] = True\n        self.min_freq = 1\n\ncache = LFUCache(2)\ncache.put(1, 1)\ncache.put(2, 2)\nprint('Get 1 (freq 2):', cache.get(1))\ncache.put(3, 3)\nprint('Get 2 (evicted):', cache.get(2))\nprint('Get 3 (freq 2):', cache.get(3))\nprint('160-Day Capstone Mastered:', True)\n",
        "patterns": [
            "Get 1 (freq 2): 1",
            "Get 2 (evicted): -1",
            "Get 3 (freq 2): 3",
            "160-Day Capstone Mastered: True"
        ],
        "hint": "In _promote(key): increment freqs[key], remove from freq_keys[f], advance min_freq if empty, insert into freq_keys[f+1]. In put: if at cap, popitem(last=False) from freq_keys[min_freq].",
        "recap": [
            {"concept": "Dual Hash Map Architecture", "naiveIntuition": "Cache eviction always needs heap priority queues", "pythonReality": "Dual hash maps paired with doubly linked lists achieve true O(1) lookups and O(1) evictions without O(log N) overhead"},
            {"concept": "160-Day Capstone Synthesis", "naiveIntuition": "Curriculum complete means memorizing interview problems", "pythonReality": "You have mastered the complete engineering continuum from Python memory mechanics to production systems architecture"}
        ]
    }

    new_dict = {
        156: bit_manip,
        157: nqueens_157,
        158: seg_tree,
        159: word_search_159,
        160: lfu_160
    }

    code = '"""\nSection 14: Advanced DSA & Interview Mastery (Days 156 to 160)\n"""\n\nSEC14_DAYS = ' + pprint.pformat(new_dict, indent=4, width=120) + "\n"
    with open("scratch/curriculum_generator/sec14_data.py", "w", encoding="utf-8") as f:
        f.write(code)
    print("sec14_data.py re-aligned successfully!")

if __name__ == "__main__":
    fix_sec11()
    fix_sec13()
    fix_sec14()
