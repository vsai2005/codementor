"""
Section 11: Graph Algorithms (Days 121 to 135)
"""

SEC11_DAYS = {   121: {   'hint': 'Build adj = {i: [] for i in range(n)}. Loop u, v: adj[u].append(v); adj[v].append(u). Return {i: '
                     'len(adj[i]) for i in range(n)}.',
             'mechanics': 'Adjacency List (`dict[int, list[int]]`): O(V + E) memory, O(deg(u)) neighbor iteration. '
                          'Adjacency Matrix (`list[list[int]]`): O(V^2) memory, O(1) edge lookup `matrix[u][v]`. In '
                          'real-world graphs where E << V^2, adjacency lists dominate.',
             'patterns': ['Degrees: {0: 2, 1: 2, 2: 3, 3: 1}'],
             'practice_task': 'Build an undirected Adjacency List from an edge list and calculate vertex degrees.',
             'q1': 'Why is an Adjacency List preferred over an Adjacency Matrix for a sparse graph with 1,000,000 '
                   'vertices and 2,000,000 edges?',
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! V^2 for 1M vertices is 10^12 elements (terabytes of memory). An adjacency '
                                'list stores only actual edges (2M entries), fitting comfortably in standard RAM.',
                           'B': 'Incorrect: Lists do not sort elements automatically.',
                           'C': 'Incorrect: Asymmetric matrices easily represent directed graphs.',
                           'D': 'Incorrect: Python lists of lists easily form 2D matrices.'},
             'q1_opts': [   {   'id': 'A',
                                'label': 'An adjacency matrix would allocate 1,000,000 x 1,000,000 cells (~1 Terabyte '
                                         'of RAM), whereas an adjacency list consumes only O(V + E) (~24 Megabytes)'},
                            {'id': 'B', 'label': 'Because adjacency lists sort vertex values automatically'},
                            {'id': 'C', 'label': 'Because matrices cannot represent directed graphs'},
                            {'id': 'D', 'label': 'Because Python does not support 2D arrays'}],
             'q2': 'What is the time complexity to check if an edge exists between vertex u and vertex v in an '
                   'Adjacency Matrix versus an Adjacency List?',
             'q2_ans': 'A',
             'q2_exp': {   'A': 'Correct! In a matrix, `matrix[u][v]` is an instant O(1) index lookup. In an adjacency '
                                'list, one must scan the neighbors of u (`v in adj[u]`), taking O(deg(u)).',
                           'B': 'Incorrect: List search requires scanning neighbor array.',
                           'C': 'Incorrect: Matrix is direct index access.',
                           'D': 'Incorrect: Inverted.'},
             'q2_opts': [   {   'id': 'A',
                                'label': 'Matrix is O(1) direct lookup, while Adjacency List is O(degree(u)) search'},
                            {'id': 'B', 'label': 'Both are O(1)'},
                            {'id': 'C', 'label': 'Both are O(V)'},
                            {'id': 'D', 'label': 'List is O(1), Matrix is O(V)'}],
             'recap': [   {   'concept': 'Sparsity Advantage',
                              'naiveIntuition': 'Always use 2D matrices for graphs',
                              'pythonReality': 'Most real-world networks (web links, social graphs) are extremely '
                                               'sparse; adjacency lists prevent catastrophic O(V^2) memory explosions'},
                          {   'concept': 'Neighbor Iteration Bound',
                              'naiveIntuition': 'Finding neighbors in a matrix is O(deg(u))',
                              'pythonReality': 'Finding neighbors in a matrix requires scanning all V columns (O(V)); '
                                               'adjacency lists iterate strictly over the degree of u'}],
             'sample_code': '# Adjacency List from edge list\n'
                            'def build_adj_list(n, edges, directed=False):\n'
                            '    adj = {i: [] for i in range(n)}\n'
                            '    for u, v in edges:\n'
                            '        adj[u].append(v)\n'
                            '        if not directed: adj[v].append(u)\n'
                            '    return adj',
             'solution': 'def get_vertex_degrees(n: int, edges: list[list[int]]) -> dict[int, int]:\n'
                         '    adj = {i: [] for i in range(n)}\n'
                         '    for u, v in edges:\n'
                         '        adj[u].append(v)\n'
                         '        adj[v].append(u)\n'
                         '    return {i: len(adj[i]) for i in range(n)}\n'
                         '\n'
                         'edges = [[0, 1], [0, 2], [1, 2], [2, 3]]\n'
                         "print('Degrees:', get_vertex_degrees(4, edges))\n",
             'starter': 'def get_vertex_degrees(n: int, edges: list[list[int]]) -> dict[int, int]:\n'
                        '    # TODO: Construct adjacency list and return degree of each vertex\n'
                        '    return {}\n'
                        '\n'
                        'edges = [[0, 1], [0, 2], [1, 2], [2, 3]]\n'
                        "print('Degrees:', get_vertex_degrees(4, edges))\n",
             'summary': 'Graph Representations model pairwise relationships via Adjacency Lists (optimal for sparse '
                        'graphs) or Adjacency Matrices (optimal for dense graphs).',
             'takeaway': 'Adjacency lists provide optimal O(V + E) space for sparse graphs and rapid neighbor '
                         'iteration.'},
    122: {   'hint': 'Build adj list. q = deque([(start, 0)]), visited = {start}. While q: curr, d = popleft. If curr '
                     '== target: return d. For nxt in adj[curr]: if nxt not in visited: visited.add(nxt), '
                     'q.append((nxt, d + 1)). Return -1.',
             'mechanics': 'Initialize `queue = deque([start])`, `visited = {start}`, `dist = {start: 0}`. While queue '
                          'is non-empty: pop `curr = q.popleft()`. For each `neighbor` of `curr`: if `neighbor not in '
                          'visited`, mark visited, record `dist[neighbor] = dist[curr] + 1`, and enqueue. Terminates '
                          'in O(V + E) time.',
             'patterns': ['Shortest path 0 -> 4: 3'],
             'practice_task': 'Find the shortest path distance between start and end vertices in an unweighted graph '
                              'using BFS.',
             'q1': 'Why is the first path discovered by BFS to any node guaranteed to be the shortest path in an '
                   'unweighted graph?',
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! FIFO queue properties ensure that nodes are visited in monotonically '
                                'increasing order of edge distance: distance 0, then all distance 1, then all distance '
                                '2. Thus, the first arrival is minimal.',
                           'B': 'Incorrect: Unweighted graphs have uniform edge costs of 1.',
                           'C': 'Incorrect: Graphs can have cycles; visited sets prevent re-visiting.',
                           'D': 'Incorrect: Queues pop in FIFO order, not binary search.'},
             'q1_opts': [   {   'id': 'A',
                                'label': 'BFS explores all nodes at distance K before exploring any node at distance K '
                                         '+ 1, making earlier arrival strictly shorter'},
                            {'id': 'B', 'label': 'Because BFS sorts the edge weights in ascending order'},
                            {'id': 'C', 'label': 'Because graphs have no cycles'},
                            {'id': 'D', 'label': 'Because the queue uses binary search'}],
             'q2': 'What catastrophic bug occurs if you mark a vertex as `visited` upon POPPING from the queue rather '
                   'than upon PUSHING?',
             'q2_ans': 'A',
             'q2_exp': {   'A': 'Correct! Marking visited upon enqueueing immediately blocks other incoming paths from '
                                're-adding that same vertex. Delaying visited marking until dequeueing allows dense '
                                'graphs to enqueue the same vertex $O(V)$ times, exploding queue size.',
                           'B': 'Incorrect: No KeyError is raised.',
                           'C': 'Incorrect: Traversal directions are unaffected.',
                           'D': 'Incorrect: Unweighted distances are always non-negative integers.'},
             'q2_opts': [   {   'id': 'A',
                                'label': 'Multiple paths to the same unvisited node will push redundant duplicate '
                                         'copies into the queue, causing exponential memory bloat and TLE'},
                            {'id': 'B', 'label': 'Python raises an unhandled KeyError'},
                            {'id': 'C', 'label': 'The graph reverses direction'},
                            {'id': 'D', 'label': 'The shortest path becomes negative'}],
             'recap': [   {   'concept': 'Immediate Visited Registration',
                              'naiveIntuition': 'Mark node visited when popping from queue',
                              'pythonReality': 'Marking visited immediately at enqueue time prevents duplicate node '
                                               'insertions and preserves linear O(V + E) bounds'},
                          {   'concept': 'Concentric Frontier Expansion',
                              'naiveIntuition': 'DFS can also find shortest paths',
                              'pythonReality': 'DFS wanders down arbitrary deep paths first, requiring exhaustive '
                                               'O(V!) search; BFS finds shortest paths directly in O(V + E)'}],
             'sample_code': 'from collections import deque\n'
                            'def bfs_shortest_path(adj, start, target):\n'
                            '    q = deque([(start, 0)])\n'
                            '    visited = {start}\n'
                            '    while q:\n'
                            '        curr, d = q.popleft()\n'
                            '        if curr == target: return d\n'
                            '        for nxt in adj[curr]:\n'
                            '            if nxt not in visited:\n'
                            '                visited.add(nxt)\n'
                            '                q.append((nxt, d + 1))\n'
                            '    return -1',
             'solution': 'from collections import deque\n'
                         '\n'
                         'def shortest_path(n: int, edges: list[list[int]], start: int, target: int) -> int:\n'
                         '    adj = {i: [] for i in range(n)}\n'
                         '    for u, v in edges:\n'
                         '        adj[u].append(v)\n'
                         '        adj[v].append(u)\n'
                         '    \n'
                         '    q = deque([(start, 0)])\n'
                         '    visited = {start}\n'
                         '    while q:\n'
                         '        curr, d = q.popleft()\n'
                         '        if curr == target:\n'
                         '            return d\n'
                         '        for nxt in adj[curr]:\n'
                         '            if nxt not in visited:\n'
                         '                visited.add(nxt)\n'
                         '                q.append((nxt, d + 1))\n'
                         '    return -1\n'
                         '\n'
                         'edges = [[0, 1], [0, 2], [1, 3], [2, 3], [3, 4]]\n'
                         "print('Shortest path 0 -> 4:', shortest_path(5, edges, 0, 4))\n",
             'starter': 'from collections import deque\n'
                        '\n'
                        'def shortest_path(n: int, edges: list[list[int]], start: int, target: int) -> int:\n'
                        '    # TODO: Build adjacency list and find shortest distance using BFS\n'
                        '    return -1\n'
                        '\n'
                        'edges = [[0, 1], [0, 2], [1, 3], [2, 3], [3, 4]]\n'
                        "print('Shortest path 0 -> 4:', shortest_path(5, edges, 0, 4))\n",
             'summary': 'Breadth-First Search (BFS) finds the Shortest Path in Unweighted Graphs by exploring vertices '
                        'in concentric expanding rings of distance using a FIFO Queue.',
             'takeaway': 'In unweighted graphs, the first time BFS reaches a vertex is guaranteed to be its shortest '
                         'path.'},
    123: {   'hint': 'Build adj. state = [0] * n. Helper dfs(u): state[u] = 1; loop v in adj[u]: if state[v] == 1 '
                     'return True; if state[v] == 0 and dfs(v) return True; state[u] = 2; return False. Check all '
                     'unvisited nodes in range(n).',
             'mechanics': 'Three-color state machine: 0 = Unvisited (White), 1 = Visiting (Gray, active on recursion '
                          'stack), 2 = Visited (Black, fully explored). In directed graphs, encountering a neighbor '
                          'with state 1 indicates a Back-Edge, proving the presence of a cycle in O(V + E) time.',
             'patterns': ['G1 Has Cycle: True', 'G2 Has Cycle: False'],
             'practice_task': 'Detect if a directed graph contains a cycle using 3-color DFS.',
             'q1': 'Why is a simple boolean `visited` set insufficient to detect cycles in a DIRECTED graph?',
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! In DAGs like diamond paths (0 -> 1 -> 3 and 0 -> 2 -> 3), node 3 is visited '
                                'twice via cross paths, but no cycle exists. A cycle exists only when an edge points '
                                "back to an active ancestor currently in state 'visiting'.",
                           'B': 'Incorrect: Node IDs are non-negative indices.',
                           'C': 'Incorrect: Directed graphs frequently contain cycles.',
                           'D': 'Incorrect: Sets have O(1) average lookup.'},
             'q1_opts': [   {   'id': 'A',
                                'label': 'A node might be visited from two separate converging paths (Cross-Edge) '
                                         'without forming a cycle; only reaching an active ancestor on the CURRENT '
                                         'recursion path constitutes a cycle'},
                            {'id': 'B', 'label': 'Because boolean sets cannot store negative numbers'},
                            {'id': 'C', 'label': 'Because directed graphs cannot have cycles'},
                            {'id': 'D', 'label': 'Because sets do not support lookup in O(1)'}],
             'q2': 'In an UNDIRECTED graph, how is a cycle distinguished from the trivial backtracking edge to the '
                   'parent node?',
             'q2_ans': 'A',
             'q2_exp': {   'A': 'Correct! In an undirected graph, edge (u, v) allows walking u -> v and immediately v '
                                '-> u. Passing `parent` prevents mistaking this reciprocal edge for a cycle; reaching '
                                'any other already-visited node proves a true cycle.',
                           'B': 'Incorrect: Never mutate graph topology during traversal.',
                           'C': 'Incorrect: Undirected graphs can have cycles.',
                           'D': 'Incorrect: Traversal order does not eliminate the parent check.'},
             'q2_opts': [   {   'id': 'A',
                                'label': 'By passing `parent` into the DFS call and ignoring the edge `if neighbor == '
                                         'parent`'},
                            {'id': 'B', 'label': 'By deleting the parent node'},
                            {'id': 'C', 'label': 'Undirected graphs cannot have cycles'},
                            {'id': 'D', 'label': 'By sorting edges by weight'}],
             'recap': [   {   'concept': 'Three-State Disambiguation',
                              'naiveIntuition': 'Visited nodes cannot be visited again',
                              'pythonReality': "Distinguishing 'visiting' (active ancestor on current path) from "
                                               "'visited' (fully closed branch) separates genuine cycles from "
                                               'cross-edges'},
                          {   'concept': 'Disconnected Forest Sweeping',
                              'naiveIntuition': 'Running DFS once from node 0 explores the whole graph',
                              'pythonReality': 'A graph may have multiple disconnected components; an outer loop over '
                                               'all nodes ensures 100% coverage'}],
             'sample_code': '# Directed Cycle Detection via 3-State DFS\n'
                            'def has_cycle(n, adj):\n'
                            '    state = [0] * n # 0: unvisited, 1: visiting, 2: visited\n'
                            '    def dfs(u):\n'
                            '        state[u] = 1 # Mark visiting\n'
                            '        for v in adj[u]:\n'
                            '            if state[v] == 1: return True # Back-edge found!\n'
                            '            if state[v] == 0 and dfs(v): return True\n'
                            '        state[u] = 2 # Mark visited\n'
                            '        return False\n'
                            '    return any(state[i] == 0 and dfs(i) for i in range(n))',
             'solution': 'def has_cycle_directed(n: int, edges: list[list[int]]) -> bool:\n'
                         '    adj = {i: [] for i in range(n)}\n'
                         '    for u, v in edges:\n'
                         '        adj[u].append(v)\n'
                         '    \n'
                         '    state = [0] * n\n'
                         '    def dfs(u):\n'
                         '        state[u] = 1\n'
                         '        for v in adj[u]:\n'
                         '            if state[v] == 1:\n'
                         '                return True\n'
                         '            if state[v] == 0 and dfs(v):\n'
                         '                return True\n'
                         '        state[u] = 2\n'
                         '        return False\n'
                         '\n'
                         '    for i in range(n):\n'
                         '        if state[i] == 0:\n'
                         '            if dfs(i):\n'
                         '                return True\n'
                         '    return False\n'
                         '\n'
                         'e1 = [[0, 1], [1, 2], [2, 0]]\n'
                         'e2 = [[0, 1], [1, 2]]\n'
                         "print('G1 Has Cycle:', has_cycle_directed(3, e1))\n"
                         "print('G2 Has Cycle:', has_cycle_directed(3, e2))\n",
             'starter': 'def has_cycle_directed(n: int, edges: list[list[int]]) -> bool:\n'
                        '    # TODO: Implement 3-state DFS cycle detection\n'
                        '    return False\n'
                        '\n'
                        '# Graph 1: 0 -> 1 -> 2 -> 0 (Cycle!)\n'
                        'e1 = [[0, 1], [1, 2], [2, 0]]\n'
                        '# Graph 2: 0 -> 1 -> 2 (No cycle)\n'
                        'e2 = [[0, 1], [1, 2]]\n'
                        "print('G1 Has Cycle:', has_cycle_directed(3, e1))\n"
                        "print('G2 Has Cycle:', has_cycle_directed(3, e2))\n",
             'summary': 'Depth-First Search (DFS) explores branches deeply before backtracking, identifying Connected '
                        'Components and detecting Cycles via three-color node state tracking.',
             'takeaway': 'Encountering an active ancestor (visiting state) on the recursion stack proves a directed '
                         'cycle.'},
    124: {   'hint': 'In dfs(u): mark visited[u] = 1. For v in adj[u]: if visited[v] == 1 return False; if visited[v] '
                     '== 0 and not dfs(v) return False. visited[u] = 2. Return True. Check all courses i in range(n).',
             'mechanics': 'Every vertex has one of three states: 0=WHITE (unvisited), 1=GRAY (currently being explored '
                          'on call stack), 2=BLACK (completely processed and backtrack completed). During DFS from '
                          'vertex u, if we encounter an adjacent vertex v that is GRAY (visited[v] == 1), an active '
                          'back-edge exists, confirming a directed cycle.',
             'patterns': ['Can finish [0->1, 1->0]: False', 'Can finish [0->1, 1->2]: True'],
             'practice_task': 'Detect whether a directed course prerequisite graph contains a cycle (Deadlock '
                              'Detection).',
             'q1': 'Why is a simple 2-state boolean visited array (True/False) INSUFFICIENT for cycle detection in '
                   'DIRECTED graphs?',
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! In directed graphs, reaching an already-visited vertex via a cross-edge '
                                '(e.g. 1 -> 2 and 1 -> 3 -> 2) is completely acyclic. Cycles occur ONLY when an edge '
                                'points back to an active ancestor currently in state GRAY.',
                           'B': 'Incorrect: DFS is the canonical algorithm for directed graphs.',
                           'C': 'Incorrect: Memory representation is irrelevant to cycle geometry.',
                           'D': 'Incorrect: Directed Acyclic Graphs (DAGs) have zero cycles.'},
             'q1_opts': [   {   'id': 'A',
                                'label': 'A True entry could be a cross-edge or forward-edge to a previously finished '
                                         'node that does not form a cycle; only edges to active ancestors on the '
                                         'current call stack form cycles'},
                            {'id': 'B', 'label': 'Because directed graphs cannot be traversed with DFS'},
                            {'id': 'C', 'label': 'Because booleans take more memory than integers'},
                            {'id': 'D', 'label': 'Because directed graphs always have cycles'}],
             'q2': 'What does state BLACK (visited[u] == 2) signify in the 3-coloring algorithm?',
             'q2_ans': 'A',
             'q2_exp': {   'A': 'Correct! Once all neighbors of u are verified acyclic, u transitions from Gray to '
                                'Black. Any subsequent edge encountering a Black vertex can safely prune that branch '
                                'immediately.',
                           'B': 'Incorrect: Gray-to-Gray transitions detect cycles.',
                           'C': 'Incorrect: Nodes with out-degree > 0 transition to Black after exploration.',
                           'D': 'Incorrect: Any node transitions to Black when its subtree completes.'},
             'q2_opts': [   {   'id': 'A',
                                'label': 'All descendants reachable from vertex u have been fully explored with zero '
                                         'cycles found, so u can be safely pruned from future inspection'},
                            {'id': 'B', 'label': 'A cycle has been found at vertex u'},
                            {'id': 'C', 'label': 'Vertex u has no outgoing edges'},
                            {'id': 'D', 'label': 'Vertex u is the root of the graph'}],
             'recap': [   {   'concept': 'Recursion Stack Invariant',
                              'naiveIntuition': 'Any visited node means a cycle',
                              'pythonReality': 'Only nodes currently in the recursion stack (Gray) indicate cycles; '
                                               'already completed nodes (Black) are safe cross-edges'},
                          {   'concept': 'Topological Equivalency',
                              'naiveIntuition': 'Cycle detection is unrelated to topo sort',
                              'pythonReality': 'A directed graph has a cycle if and only if a valid topological '
                                               'ordering does NOT exist'}],
             'sample_code': '# 3-Color Cycle Detection in Directed Graph\n'
                            'def has_cycle(n, adj):\n'
                            '    visited = [0] * n  # 0=White, 1=Gray, 2=Black\n'
                            '    def dfs(u):\n'
                            '        visited[u] = 1 # Mark Gray\n'
                            '        for v in adj[u]:\n'
                            '            if visited[v] == 1: return True  # Cycle detected!\n'
                            '            if visited[v] == 0 and dfs(v): return True\n'
                            '        visited[u] = 2 # Mark Black\n'
                            '        return False\n'
                            '    return any(visited[i] == 0 and dfs(i) for i in range(n))',
             'solution': 'def can_finish_courses(num_courses: int, prerequisites: list[list[int]]) -> bool:\n'
                         '    adj = {i: [] for i in range(num_courses)}\n'
                         '    for crs, pre in prerequisites:\n'
                         '        adj[pre].append(crs)\n'
                         '    visited = [0] * num_courses\n'
                         '    def dfs(u):\n'
                         '        visited[u] = 1\n'
                         '        for v in adj[u]:\n'
                         '            if visited[v] == 1:\n'
                         '                return False\n'
                         '            if visited[v] == 0 and not dfs(v):\n'
                         '                return False\n'
                         '        visited[u] = 2\n'
                         '        return True\n'
                         '    for i in range(num_courses):\n'
                         '        if visited[i] == 0:\n'
                         '            if not dfs(i):\n'
                         '                return False\n'
                         '    return True\n'
                         '\n'
                         "print('Can finish [0->1, 1->0]:', can_finish_courses(2, [[1, 0], [0, 1]]))\n"
                         "print('Can finish [0->1, 1->2]:', can_finish_courses(3, [[1, 0], [2, 1]]))\n",
             'starter': 'def can_finish_courses(num_courses: int, prerequisites: list[list[int]]) -> bool:\n'
                        '    adj = {i: [] for i in range(num_courses)}\n'
                        '    for crs, pre in prerequisites:\n'
                        '        adj[pre].append(crs)\n'
                        '    visited = [0] * num_courses  # 0=White, 1=Gray, 2=Black\n'
                        '    # TODO: Implement 3-color DFS to return True if no cycles, False if cycle exists\n'
                        '    return True\n'
                        '\n'
                        "print('Can finish [0->1, 1->0]:', can_finish_courses(2, [[1, 0], [0, 1]])) # False\n"
                        "print('Can finish [0->1, 1->2]:', can_finish_courses(3, [[1, 0], [2, 1]])) # True\n",
             'summary': 'Cycle Detection in Directed Graphs uses DFS 3-Coloring (White, Gray, Black) to detect '
                        'back-edges to active ancestors currently on the recursion call stack in O(V + E) time.',
             'takeaway': 'A directed cycle exists if and only if DFS encounters a back-edge to a GRAY ancestor '
                         'currently on the call stack.'},
    125: {   'hint': 'Build adj and in_deg arrays: for crs, pre: adj[pre].append(crs); in_deg[crs] += 1. q = '
                     'deque(nodes with in_deg == 0). While q: pop, append to res, decrement neighbors, enqueue if '
                     'in_deg == 0. Return res if len(res) == num_courses else [].',
             'mechanics': 'Calculate `in_degree` for all vertices. Enqueue all vertices with `in_degree == 0`. While '
                          'queue is non-empty: pop `u`, append to result list. For each neighbor `v` of `u`: decrement '
                          '`in_degree[v]`. If `in_degree[v] == 0`: enqueue `v`. If result length < V, the graph '
                          'contains a cycle.',
             'patterns': ['Course order: [0, 1, 2, 3]'],
             'practice_task': 'Perform topological sort on course prerequisites to determine a valid course completion '
                              'order.',
             'q1': "Why does a final `len(order) < n` prove that the directed graph contains a cycle in Kahn's "
                   'algorithm?',
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! Every node in a cycle has at least one predecessor inside the cycle. Since '
                                'no cycle member can have its in-degree reduced to 0, all cycle nodes are permanently '
                                'locked out of the queue.',
                           'B': 'Incorrect: Deque handles memory dynamically.',
                           'C': 'Incorrect: Works for any number of vertices.',
                           'D': 'Incorrect: In-degrees are decremented to 0, never negative.'},
             'q1_opts': [   {   'id': 'A',
                                'label': 'Vertices inside a directed cycle always retain an in-degree >= 1 from each '
                                         'other, so none of them can ever reach in-degree 0 and enter the queue'},
                            {'id': 'B', 'label': 'Because the queue ran out of memory'},
                            {   'id': 'C',
                                'label': 'Because topological sort only works for graphs with even number of vertices'},
                            {'id': 'D', 'label': 'Because in-degree became negative'}],
             'q2': 'What does an in-degree of 0 mean for a task in a dependency graph?',
             'q2_ans': 'A',
             'q2_exp': {   'A': 'Correct! In a build system or prerequisite chain, incoming edges represent '
                                'dependencies. In-degree 0 means no remaining dependencies, making the task '
                                'immediately runnable.',
                           'B': 'Incorrect: It is ready to run.',
                           'C': 'Incorrect: It is ready to begin, not already done.',
                           'D': 'Incorrect: In-degree measures incoming edges, not outgoing.'},
             'q2_opts': [   {   'id': 'A',
                                'label': 'The task has zero unmet prerequisites and is ready to be executed '
                                         'immediately'},
                            {'id': 'B', 'label': 'The task cannot be executed'},
                            {'id': 'C', 'label': 'The task has already completed'},
                            {'id': 'D', 'label': 'The task has no outgoing edges'}],
             'recap': [   {   'concept': 'Prerequisite Resolution Flow',
                              'naiveIntuition': 'Sort courses by course number',
                              'pythonReality': 'Topological order reflects dependency satisfaction; in-degree tracking '
                                               'guarantees no task runs before its prerequisites complete'},
                          {   'concept': "Dual Utility of Kahn's",
                              'naiveIntuition': 'Cycle detection and topological ordering require separate passes',
                              'pythonReality': "Kahn's algorithm accomplishes both simultaneously: valid DAGs yield "
                                               'the full topological sequence, while cycles result in truncated '
                                               'outputs'}],
             'sample_code': "# Kahn's Topological Sort\n"
                            'from collections import deque\n'
                            'def topological_sort_kahn(n, adj):\n'
                            '    in_degree = [0] * n\n'
                            '    for u in range(n):\n'
                            '        for v in adj[u]: in_degree[v] += 1\n'
                            '    q = deque([i for i in range(n) if in_degree[i] == 0])\n'
                            '    order = []\n'
                            '    while q:\n'
                            '        u = q.popleft()\n'
                            '        order.append(u)\n'
                            '        for v in adj[u]:\n'
                            '            in_degree[v] -= 1\n'
                            '            if in_degree[v] == 0: q.append(v)\n'
                            '    return order if len(order) == n else [] # Empty if cycle',
             'solution': 'from collections import deque\n'
                         '\n'
                         'def course_order(num_courses: int, prerequisites: list[list[int]]) -> list[int]:\n'
                         '    adj = {i: [] for i in range(num_courses)}\n'
                         '    in_deg = [0] * num_courses\n'
                         '    for crs, pre in prerequisites:\n'
                         '        adj[pre].append(crs)\n'
                         '        in_deg[crs] += 1\n'
                         '    \n'
                         '    q = deque([i for i in range(num_courses) if in_deg[i] == 0])\n'
                         '    res = []\n'
                         '    while q:\n'
                         '        u = q.popleft()\n'
                         '        res.append(u)\n'
                         '        for v in adj[u]:\n'
                         '            in_deg[v] -= 1\n'
                         '            if in_deg[v] == 0:\n'
                         '                q.append(v)\n'
                         '    return res if len(res) == num_courses else []\n'
                         '\n'
                         'prereqs = [[1, 0], [2, 0], [3, 1], [3, 2]]\n'
                         "print('Course order:', course_order(4, prereqs))\n",
             'starter': 'from collections import deque\n'
                        '\n'
                        'def course_order(num_courses: int, prerequisites: list[list[int]]) -> list[int]:\n'
                        "    # TODO: Implement Kahn's algorithm for Course Schedule II\n"
                        '    # prerequisites[i] = [course, prereq] (prereq -> course)\n'
                        '    return []\n'
                        '\n'
                        '# 4 courses: 0, 1, 2, 3. Prereqs: 1->0, 2->0, 3->1, 3->2\n'
                        'prereqs = [[1, 0], [2, 0], [3, 1], [3, 2]]\n'
                        "print('Course order:', course_order(4, prereqs))\n",
             'summary': 'Topological Sort linearly orders vertices in a Directed Acyclic Graph (DAG) such that for '
                        "every directed edge u -> v, u appears before v. Kahn's Algorithm resolves dependencies via "
                        'in-degree tracking and a FIFO queue.',
             'takeaway': "Kahn's algorithm orders DAG dependencies in O(V + E) time while naturally detecting cycles "
                         'if output length < V.'},
    126: {   'hint': 'State 0: unvisited, 1: visiting, 2: visited. In dfs(u): state[u] = 1; loop neighbors: if state '
                     '== 1 return False; if state == 0 and not dfs(v) return False. state[u] = 2; '
                     'post_order.append(u); return True. Loop all nodes, return post_order[::-1].',
             'mechanics': 'For each unvisited node: run DFS. In post-order (after all descendants have finished '
                          "exploring), append `node` to stack. If a node encounters a neighbor in state 'visiting', a "
                          'cycle exists. Reversing the post-order stack yields the exact topological order in O(V + E) '
                          'time.',
             'patterns': ['DFS Topo Sort: [0, 2, 1, 3]'],
             'practice_task': 'Implement DFS post-order topological sort.',
             'q1': 'Why must the post-order result list be reversed to obtain a valid topological sort?',
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! If u -> v, v must complete before u can finish. Thus, v is appended to '
                                'post-order before u. Reversing the list puts u before v, restoring the correct '
                                'dependency order.',
                           'B': 'Incorrect: Lists can insert at index 0 (though O(N)).',
                           'C': 'Incorrect: Starting order does not change finishing relations.',
                           'D': 'Incorrect: Reversal is a mathematical requirement of post-order finishing.'},
             'q1_opts': [   {   'id': 'A',
                                'label': 'A node only finishes its post-order DFS after all its downstream '
                                         'dependencies have completely finished, meaning terminal nodes finish first '
                                         'and must be placed at the end'},
                            {'id': 'B', 'label': 'Because Python lists can only be appended to the right'},
                            {'id': 'C', 'label': 'Because DFS starts from the largest node index'},
                            {'id': 'D', 'label': 'To fix a sorting bug'}],
             'q2': 'What is the time and space complexity of DFS Topological Sort on a graph with V vertices and E '
                   'edges?',
             'q2_ans': 'A',
             'q2_exp': {   'A': 'Correct! Every vertex and edge is traversed once in O(V + E) time. Auxiliary storage '
                                'includes the state array, call stack, and result list, totaling O(V).',
                           'B': 'Incorrect: DFS avoids quadratic scanning.',
                           'C': 'Incorrect: Adjacency list is O(V + E).',
                           'D': 'Incorrect: All nodes must be visited.'},
             'q2_opts': [   {'id': 'A', 'label': 'O(V + E) time and O(V) auxiliary space'},
                            {'id': 'B', 'label': 'O(V * E) time and O(1) space'},
                            {'id': 'C', 'label': 'O(V^2) time and O(E) space'},
                            {'id': 'D', 'label': 'O(log V) time and O(V) space'}],
             'recap': [   {   'concept': 'Finishing Time Duality',
                              'naiveIntuition': 'Discovery time determines dependency order',
                              'pythonReality': 'Discovery time depends on arbitrary branch selection; finishing time '
                                               'strictly mirrors leaf-to-root completion'},
                          {   'concept': 'DFS vs BFS Equivalence',
                              'naiveIntuition': "Kahn's and DFS produce different dependencies",
                              'pythonReality': 'Both generate valid topological orderings (though ties may resolve '
                                               'differently), operating in O(V + E) time'}],
             'sample_code': '# DFS Topological Sort\n'
                            'def topo_dfs(n, adj):\n'
                            '    state = [0] * n # 0: unvisited, 1: visiting, 2: visited\n'
                            '    res = []\n'
                            '    def dfs(u):\n'
                            '        state[u] = 1\n'
                            '        for v in adj[u]:\n'
                            '            if state[v] == 1: return False\n'
                            '            if state[v] == 0 and not dfs(v): return False\n'
                            '        state[u] = 2\n'
                            '        res.append(u) # Post-order finish\n'
                            '        return True\n'
                            '    for i in range(n):\n'
                            '        if state[i] == 0 and not dfs(i): return []\n'
                            '    return res[::-1] # Reverse post-order',
             'solution': 'def topo_sort_dfs(n: int, edges: list[list[int]]) -> list[int]:\n'
                         '    adj = {i: [] for i in range(n)}\n'
                         '    for u, v in edges:\n'
                         '        adj[u].append(v)\n'
                         '    \n'
                         '    state = [0] * n\n'
                         '    post_order = []\n'
                         '    def dfs(u):\n'
                         '        state[u] = 1\n'
                         '        for v in adj[u]:\n'
                         '            if state[v] == 1:\n'
                         '                return False\n'
                         '            if state[v] == 0 and not dfs(v):\n'
                         '                return False\n'
                         '        state[u] = 2\n'
                         '        post_order.append(u)\n'
                         '        return True\n'
                         '\n'
                         '    for i in range(n):\n'
                         '        if state[i] == 0:\n'
                         '            if not dfs(i):\n'
                         '                return []\n'
                         '    return post_order[::-1]\n'
                         '\n'
                         'edges = [[0, 1], [0, 2], [1, 3], [2, 3]]\n'
                         "print('DFS Topo Sort:', topo_sort_dfs(4, edges))\n",
             'starter': 'def topo_sort_dfs(n: int, edges: list[list[int]]) -> list[int]:\n'
                        '    # TODO: Implement DFS topological sort with cycle detection\n'
                        '    return []\n'
                        '\n'
                        '# 0 -> 1, 0 -> 2, 1 -> 3, 2 -> 3\n'
                        'edges = [[0, 1], [0, 2], [1, 3], [2, 3]]\n'
                        "print('DFS Topo Sort:', topo_sort_dfs(4, edges))\n",
             'summary': 'Topological Sort via DFS Post-Order Reversal sorts DAGs by recording vertices upon post-order '
                        'completion and reversing the resulting list.',
             'takeaway': 'Reversing DFS post-order finishing times produces a valid topological sequence for any DAG.'},
    127: {   'hint': 'color = [-1] * n. Loop i in range(n): if color[i] == -1: color[i] = 0, q = deque([i]). While q: '
                     'u = q.popleft(). For v in adj[u]: if color[v] == -1: color[v] = 1 - color[u], q.append(v). Elif '
                     'color[v] == color[u]: return False. Return True.',
             'mechanics': 'Graph is bipartite if and only if it contains NO odd-length cycles. Traversal: assign '
                          '`color[start] = 1`. For each neighbor `v`: if uncolored, assign `color[v] = 1 - color[u]` '
                          'and recurse/enqueue. If `v` is already colored and `color[v] == color[u]`, a color conflict '
                          'is detected: return False.',
             'patterns': ['Triangle Bipartite: False', 'Square Bipartite: True'],
             'practice_task': 'Determine whether an undirected graph is bipartite.',
             'q1': 'What fundamental topological property makes a graph non-bipartite?',
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! In an odd cycle (e.g. triangle of 3 nodes), alternating colors 0-1-0 forces '
                                'the 3rd node to connect back to node 1 with the same color 0, causing an inevitable '
                                'conflict.',
                           'B': 'Incorrect: Even cycles (like 4-node squares) alternate colors 0-1-0-1 perfectly.',
                           'C': 'Incorrect: Total vertices can be odd as long as cycles are even.',
                           'D': 'Incorrect: Bipartition is an unweighted structural property.'},
             'q1_opts': [   {   'id': 'A',
                                'label': 'The presence of at least one cycle with an ODD number of vertices/edges'},
                            {'id': 'B', 'label': 'The presence of an even cycle'},
                            {'id': 'C', 'label': 'Having an odd number of total vertices in the graph'},
                            {'id': 'D', 'label': 'Having negative edge weights'}],
             'q2': 'Why must the outer loop iterate through all vertices from 0 to N - 1?',
             'q2_ans': 'A',
             'q2_exp': {   'A': 'Correct! If a graph consists of two separate components, checking only component 1 '
                                'leaves component 2 uninspected. Component 2 might harbor an odd cycle.',
                           'B': 'Incorrect: No sorting is performed.',
                           'C': 'Incorrect: Coloring values are binary states.',
                           'D': 'Incorrect: Algorithmic component traversal.'},
             'q2_opts': [   {   'id': 'A',
                                'label': 'The graph might contain multiple disconnected components, each requiring '
                                         'independent 2-coloring validation'},
                            {'id': 'B', 'label': 'To sort the vertices'},
                            {'id': 'C', 'label': 'Because colors are 0-indexed'},
                            {'id': 'D', 'label': 'To reset CPU registers'}],
             'recap': [   {   'concept': 'Odd Cycle Equivalence Theorem',
                              'naiveIntuition': 'Bipartition requires knowing both sets in advance',
                              'pythonReality': 'Greedy alternating 2-coloring succeeds if and only if the graph is '
                                               'free of odd cycles'},
                          {   'concept': 'Matching & Network Flows',
                              'naiveIntuition': 'Bipartition is purely academic',
                              'pythonReality': 'Bipartite graphs model job assignment, stable matching, and bipartite '
                                               'maximum matching via Ford-Fulkerson'}],
             'sample_code': '# 2-Coloring Bipartite check\n'
                            'def is_bipartite(n, adj):\n'
                            '    color = [-1] * n\n'
                            '    for i in range(n):\n'
                            '        if color[i] != -1: continue\n'
                            '        color[i] = 0\n'
                            '        q = deque([i])\n'
                            '        while q:\n'
                            '            u = q.popleft()\n'
                            '            for v in adj[u]:\n'
                            '                if color[v] == -1:\n'
                            '                    color[v] = 1 - color[u]\n'
                            '                    q.append(v)\n'
                            '                elif color[v] == color[u]:\n'
                            '                    return False # Conflict!\n'
                            '    return True',
             'solution': 'from collections import deque\n'
                         '\n'
                         'def is_graph_bipartite(n: int, edges: list[list[int]]) -> bool:\n'
                         '    adj = {i: [] for i in range(n)}\n'
                         '    for u, v in edges:\n'
                         '        adj[u].append(v)\n'
                         '        adj[v].append(u)\n'
                         '    \n'
                         '    color = [-1] * n\n'
                         '    for i in range(n):\n'
                         '        if color[i] != -1:\n'
                         '            continue\n'
                         '        color[i] = 0\n'
                         '        q = deque([i])\n'
                         '        while q:\n'
                         '            u = q.popleft()\n'
                         '            for v in adj[u]:\n'
                         '                if color[v] == -1:\n'
                         '                    color[v] = 1 - color[u]\n'
                         '                    q.append(v)\n'
                         '                elif color[v] == color[u]:\n'
                         '                    return False\n'
                         '    return True\n'
                         '\n'
                         'e_triangle = [[0, 1], [1, 2], [2, 0]]\n'
                         'e_square = [[0, 1], [1, 2], [2, 3], [3, 0]]\n'
                         "print('Triangle Bipartite:', is_graph_bipartite(3, e_triangle))\n"
                         "print('Square Bipartite:', is_graph_bipartite(4, e_square))\n",
             'starter': 'from collections import deque\n'
                        '\n'
                        'def is_graph_bipartite(n: int, edges: list[list[int]]) -> bool:\n'
                        '    # TODO: Implement 2-coloring BFS to verify bipartiteness\n'
                        '    return True\n'
                        '\n'
                        '# Triangle graph (odd cycle): 0-1, 1-2, 2-0 -> False\n'
                        'e_triangle = [[0, 1], [1, 2], [2, 0]]\n'
                        '# Square graph (even cycle): 0-1, 1-2, 2-3, 3-0 -> True\n'
                        'e_square = [[0, 1], [1, 2], [2, 3], [3, 0]]\n'
                        "print('Triangle Bipartite:', is_graph_bipartite(3, e_triangle))\n"
                        "print('Square Bipartite:', is_graph_bipartite(4, e_square))\n",
             'summary': 'Bipartite Graph Verification determines if graph vertices can be partitioned into two '
                        'independent sets such that no two adjacent vertices share the same color (2-Coloring via '
                        'BFS/DFS).',
             'takeaway': 'A graph is bipartite if and only if it is 2-colorable (contains zero odd-length cycles).'},
    128: {   'hint': 'Initialize dist = [inf] * n, dist[start] = 0, pq = [(0, start)]. Loop while pq: pop d, u. If d > '
                     'dist[u]: continue. For v, w in adj[u]: if dist[u] + w < dist[v]: dist[v] = dist[u] + w, push '
                     '(dist[v], v). Return dist.',
             'mechanics': 'Maintain `dist` table initialized to infinity, `dist[start] = 0`. Min-heap stores '
                          '`(current_dist, u)`. Pop minimum: if `current_dist > dist[u]`, discard (stale entry). For '
                          'each neighbor `v` with weight `w`: if `dist[u] + w < dist[v]`, relax edge: `dist[v] = '
                          'dist[u] + w`, and push `(dist[v], v)` into heap.',
             'patterns': ['Distances from 0: [0, 3, 1, 4]'],
             'practice_task': "Implement Dijkstra's algorithm to compute shortest path distances from node 0 to all "
                              'other nodes.',
             'q1': "Why does Dijkstra's algorithm fail on graphs with NEGATIVE edge weights?",
             'q1_ans': 'A',
             'q1_exp': {   'A': "Correct! Dijkstra's greedy correctness relies on the invariant that adding "
                                'non-negative edges can only INCREASE or maintain path lengths. Negative edges break '
                                'this monotonicity, potentially offering shorter paths after a node has been marked '
                                'finalized.',
                           'B': 'Incorrect: Python min-heaps handle negative numbers seamlessly.',
                           'C': 'Incorrect: Edge direction is independent of weight.',
                           'D': 'Incorrect: Python floats support negative values.'},
             'q1_opts': [   {   'id': 'A',
                                'label': 'Dijkstra assumes that once a node is popped from the heap, its shortest '
                                         'distance is finalized; a negative edge discovered later could retroactively '
                                         'produce an even shorter path, violating the greedy invariant'},
                            {'id': 'B', 'label': 'Because min-heaps crash when given negative numbers'},
                            {   'id': 'C',
                                'label': 'Because negative weights turn directed graphs into undirected graphs'},
                            {'id': 'D', 'label': 'Because Python floats cannot represent negative infinity'}],
             'q2': "What is the purpose of the stale entry check `if d > dist[u]: continue` in Dijkstra's algorithm?",
             'q2_ans': 'A',
             'q2_exp': {   'A': 'Correct! Instead of an expensive O(V) search to update existing heap keys, we simply '
                                'push the new smaller distance `(dist[v], v)`. When the older obsolete entries are '
                                'popped later, `d > dist[u]` discards them in O(1).',
                           'B': "Incorrect: Disconnected nodes remain float('inf').",
                           'C': 'Incorrect: Heap maintains minimum distance.',
                           'D': 'Incorrect: Dijkstra is iterative.'},
             'q2_opts': [   {   'id': 'A',
                                'label': "Python's `heapq` does not support `decrease_key`, so relaxed vertices push "
                                         'new tuples into the heap; older, higher-distance entries must be skipped '
                                         'when popped'},
                            {'id': 'B', 'label': 'To check for disconnected components'},
                            {'id': 'C', 'label': 'To sort the vertices in descending order'},
                            {'id': 'D', 'label': 'To prevent stack overflow'}],
             'recap': [   {   'concept': 'Lazy Deletion Technique',
                              'naiveIntuition': 'Update existing heap entries with decrease_key',
                              'pythonReality': 'Pushing duplicates and filtering stale entries with if d > dist[u]: '
                                               'continue achieves optimal O((V + E) log V) with standard heapq'},
                          {   'concept': 'Non-Negative Monotonicity',
                              'naiveIntuition': 'Dijkstra works on any graph with weights',
                              'pythonReality': 'Dijkstra requires strictly non-negative weights; for negative weights, '
                                               'use Bellman-Ford'}],
             'sample_code': 'import heapq\n'
                            'def dijkstra(n, adj, start):\n'
                            "    dist = [float('inf')] * n\n"
                            '    dist[start] = 0\n'
                            '    pq = [(0, start)]\n'
                            '    while pq:\n'
                            '        d, u = heapq.heappop(pq)\n'
                            '        if d > dist[u]: continue # Stale entry check!\n'
                            '        for v, w in adj[u]:\n'
                            '            if dist[u] + w < dist[v]:\n'
                            '                dist[v] = dist[u] + w\n'
                            '                heapq.heappush(pq, (dist[v], v))\n'
                            '    return dist',
             'solution': 'import heapq\n'
                         '\n'
                         'def dijkstra_shortest_paths(n: int, edges: list[list[int]], start: int) -> list[int]:\n'
                         '    adj = {i: [] for i in range(n)}\n'
                         '    for u, v, w in edges:\n'
                         '        adj[u].append((v, w))\n'
                         '    \n'
                         "    dist = [float('inf')] * n\n"
                         '    dist[start] = 0\n'
                         '    pq = [(0, start)]\n'
                         '    while pq:\n'
                         '        d, u = heapq.heappop(pq)\n'
                         '        if d > dist[u]:\n'
                         '            continue\n'
                         '        for v, w in adj[u]:\n'
                         '            if dist[u] + w < dist[v]:\n'
                         '                dist[v] = dist[u] + w\n'
                         '                heapq.heappush(pq, (dist[v], v))\n'
                         '    return dist\n'
                         '\n'
                         'edges = [[0, 1, 4], [0, 2, 1], [2, 1, 2], [1, 3, 1]]\n'
                         "print('Distances from 0:', dijkstra_shortest_paths(4, edges, 0))\n",
             'starter': 'import heapq\n'
                        '\n'
                        'def dijkstra_shortest_paths(n: int, edges: list[list[int]], start: int) -> list[int]:\n'
                        '    # TODO: edges: [u, v, weight] (directed)\n'
                        '    # Compute shortest distance from start to all vertices\n'
                        '    return []\n'
                        '\n'
                        '# 0 -> 1 (w=4), 0 -> 2 (w=1), 2 -> 1 (w=2), 1 -> 3 (w=1)\n'
                        'edges = [[0, 1, 4], [0, 2, 1], [2, 1, 2], [1, 3, 1]]\n'
                        "print('Distances from 0:', dijkstra_shortest_paths(4, edges, 0))\n",
             'summary': "Dijkstra's Algorithm finds the Shortest Paths from a single source in graphs with "
                        'non-negative edge weights using a Min-Heap (Priority Queue) to perform greedy distance '
                        'relaxations in O((V + E) log V) time.',
             'takeaway': 'Dijkstra greedily locks in the shortest distance to the closest unvisited node, requiring '
                         'non-negative edge weights.'},
    129: {   'hint': 'dist = [inf] * n, dist[start] = 0. Loop n - 1 times: for u, v, w in edges: if dist[u] != inf and '
                     'dist[u] + w < dist[v]: dist[v] = dist[u] + w. Loop once more for negative cycles.',
             'mechanics': 'Initialize `dist = [inf] * V`, `dist[start] = 0`. Repeat V - 1 times: for each edge `(u, v, '
                          'w)`, relax: `if dist[u] + w < dist[v]: dist[v] = dist[u] + w`. Run a V-th pass: if ANY edge '
                          'can still be relaxed, a negative weight cycle exists.',
             'patterns': ['Distances: [0, 4, 2]'],
             'practice_task': 'Implement Bellman-Ford to compute shortest paths and detect negative cycles.',
             'q1': 'Why is relaxing all edges V - 1 times sufficient to find all shortest paths in a graph with V '
                   'vertices (assuming no negative cycles)?',
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! Any path with >= V edges must visit at least one vertex twice, forming a '
                                'cycle. In the absence of negative cycles, the optimal shortest path is always simple '
                                'and contains at most V - 1 edges.',
                           'B': 'Incorrect: Edge order can be completely arbitrary in Bellman-Ford.',
                           'C': 'Incorrect: Complete graph diameter is 1.',
                           'D': 'Incorrect: Loop bound is derived from graph theory.'},
             'q1_opts': [   {   'id': 'A',
                                'label': 'A simple path without cycles can visit at most V vertices, which requires '
                                         'traversing at most V - 1 edges; each relaxation pass guarantees at least one '
                                         'more edge of the shortest path is resolved'},
                            {'id': 'B', 'label': 'Because edges are sorted by weight'},
                            {'id': 'C', 'label': 'Because V - 1 is the diameter of complete graphs'},
                            {'id': 'D', 'label': 'Because Python limits loops to V - 1 iterations'}],
             'q2': 'What occurs if an edge can STILL be relaxed during the V-th pass of Bellman-Ford?',
             'q2_ans': 'A',
             'q2_exp': {   'A': 'Correct! If a path can be shortened beyond V - 1 edges, it must be traversing a cycle '
                                'whose total weight is strictly negative, allowing arbitrary reduction of distances.',
                           'B': 'Incorrect: Disconnected nodes simply remain infinity.',
                           'C': 'Incorrect: No finite number of passes can resolve negative cycles.',
                           'D': 'Incorrect: Positive weights finalize within V - 1 passes.'},
             'q2_opts': [   {   'id': 'A',
                                'label': 'A negative weight cycle exists reachable from the source, meaning path '
                                         'lengths can be reduced infinitely'},
                            {'id': 'B', 'label': 'The graph is disconnected'},
                            {'id': 'C', 'label': 'The algorithm needs one more pass'},
                            {'id': 'D', 'label': 'The edge weights are all positive'}],
             'recap': [   {   'concept': 'Dynamic Programming over Edge Counts',
                              'naiveIntuition': 'Bellman-Ford is a queue traversal',
                              'pythonReality': 'Bellman-Ford is DP over edge lengths: pass k computes shortest paths '
                                               'using at most k edges'},
                          {   'concept': 'Negative Cycle Diagnostic',
                              'naiveIntuition': 'Negative edges are impossible to handle',
                              'pythonReality': 'Bellman-Ford cleanly handles negative edge weights and flags infinite '
                                               'reduction arbitrage cycles'}],
             'sample_code': '# Bellman-Ford with Negative Cycle Detection\n'
                            'def bellman_ford(n, edges, start):\n'
                            "    dist = [float('inf')] * n\n"
                            '    dist[start] = 0\n'
                            '    for _ in range(n - 1):\n'
                            '        for u, v, w in edges:\n'
                            "            if dist[u] != float('inf') and dist[u] + w < dist[v]:\n"
                            '                dist[v] = dist[u] + w\n'
                            '    # V-th pass detects negative cycle\n'
                            '    for u, v, w in edges:\n'
                            "        if dist[u] != float('inf') and dist[u] + w < dist[v]:\n"
                            '            return None # Negative cycle detected!\n'
                            '    return dist',
             'solution': 'def bellman_ford_shortest(n: int, edges: list[list[int]], start: int) -> list[int]:\n'
                         "    dist = [float('inf')] * n\n"
                         '    dist[start] = 0\n'
                         '    for _ in range(n - 1):\n'
                         '        for u, v, w in edges:\n'
                         "            if dist[u] != float('inf') and dist[u] + w < dist[v]:\n"
                         '                dist[v] = dist[u] + w\n'
                         '    for u, v, w in edges:\n'
                         "        if dist[u] != float('inf') and dist[u] + w < dist[v]:\n"
                         '            return []\n'
                         '    return dist\n'
                         '\n'
                         'e = [[0, 1, 4], [1, 2, -2], [0, 2, 5]]\n'
                         "print('Distances:', bellman_ford_shortest(3, e, 0))\n",
             'starter': 'def bellman_ford_shortest(n: int, edges: list[list[int]], start: int) -> list[int]:\n'
                        '    # TODO: Relax all edges n - 1 times; check n-th pass for negative cycles\n'
                        '    # Return dist array or [] if negative cycle exists\n'
                        '    return []\n'
                        '\n'
                        '# 0 -> 1 (w=4), 1 -> 2 (w=-2), 0 -> 2 (w=5)\n'
                        'e = [[0, 1, 4], [1, 2, -2], [0, 2, 5]]\n'
                        "print('Distances:', bellman_ford_shortest(3, e, 0))\n",
             'summary': 'Bellman-Ford Algorithm computes shortest paths on graphs with arbitrary (including negative) '
                        'weights and detects Negative Weight Cycles by relaxing all edges V - 1 times in O(V * E) '
                        'time.',
             'takeaway': 'Any shortest path in a graph with V vertices has at most V - 1 edges; further relaxation '
                         'implies a negative cycle.'},
    130: {   'hint': 'Start with components = n. For each u, v in edges: if dsu.union(u, v): components -= 1. Return '
                     'components.',
             'mechanics': 'Each element points to a parent: `parent[i] = i`. Find with Path Compression: recursively '
                          'update `parent[x] = find(parent[x])`, flattening the tree into depth 1. Union by Rank: '
                          "attach the shorter tree under the taller tree's root. Combined, operations take Inverse "
                          'Ackermann $\\alpha(N) \\le 4$ time.',
             'patterns': ['Components count: 2'],
             'practice_task': 'Count the number of connected components in an undirected graph using DSU.',
             'q1': 'How does Path Compression in `find(x)` optimize future queries?',
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! As recursion unwinds, `self.parent[x] = root` redirects every ancestor node '
                                'to point directly to the group leader. Subsequent calls for any node along that chain '
                                'take strict O(1).',
                           'B': 'Incorrect: Sets partition disjoint elements; no nodes are deleted.',
                           'C': 'Incorrect: Parent references point to roots, not sorted values.',
                           'D': 'Incorrect: Mutation occurs in-place on the parent array.'},
             'q1_opts': [   {   'id': 'A',
                                'label': 'It directly re-points every node along the traversal path directly to the '
                                         'representative root, flattening tree depth to ~1 for all subsequent lookups'},
                            {'id': 'B', 'label': 'It deletes duplicate elements from the set'},
                            {'id': 'C', 'label': 'It sorts the parents in numerical order'},
                            {'id': 'D', 'label': 'It creates a copy of the tree in memory'}],
             'q2': 'What is the amortized time complexity of a sequence of M DSU operations on N elements when '
                   'combining Path Compression and Union by Rank?',
             'q2_ans': 'A',
             'q2_exp': {   'A': 'Correct! Tarjan proved that path compression combined with union by rank/size '
                                'achieves $O(M \\cdot \\alpha(N))$ time. Because $\\alpha(10^{80}) < 5$, each '
                                'operation runs in virtually O(1) time.',
                           'B': 'Incorrect: O(log N) is the bound when using Union by Rank alone without Path '
                                'Compression.',
                           'C': 'Incorrect: Without optimizations, degenerate chains take O(N).',
                           'D': 'Incorrect: Quadratic bounds apply only to naive array scanning.'},
             'q2_opts': [   {   'id': 'A',
                                'label': 'O(M * alpha(N)), where alpha is the Inverse Ackermann function (effectively '
                                         '<= 4 for all practical universe sizes)'},
                            {'id': 'B', 'label': 'O(M * log N)'},
                            {'id': 'C', 'label': 'O(M * N)'},
                            {'id': 'D', 'label': 'O(M^2)'}],
             'recap': [   {   'concept': 'Dynamic Equivalence Partitioning',
                              'naiveIntuition': 'Re-run BFS on every edge addition',
                              'pythonReality': 'DSU maintains transitive connectivity dynamically in O(alpha(N)) '
                                               'without rebuilding adjacency lists'},
                          {   'concept': 'Forest Representation',
                              'naiveIntuition': 'Store sets as Python set() objects',
                              'pythonReality': 'Representing disjoint sets as inverted parent-pointer trees in a flat '
                                               'array eliminates set union allocation costs'}],
             'sample_code': '# DSU Class with Path Compression & Union by Rank\n'
                            'class DSU:\n'
                            '    def __init__(self, n):\n'
                            '        self.parent = list(range(n))\n'
                            '        self.rank = [0] * n\n'
                            '    def find(self, x):\n'
                            '        if self.parent[x] != x:\n'
                            '            self.parent[x] = self.find(self.parent[x]) # Path compression\n'
                            '        return self.parent[x]\n'
                            '    def union(self, x, y):\n'
                            '        rx, ry = self.find(x), self.find(y)\n'
                            '        if rx == ry: return False\n'
                            '        if self.rank[rx] < self.rank[ry]: rx, ry = ry, rx\n'
                            '        self.parent[ry] = rx\n'
                            '        if self.rank[rx] == self.rank[ry]: self.rank[rx] += 1\n'
                            '        return True',
             'solution': 'class DSU:\n'
                         '    def __init__(self, n):\n'
                         '        self.p = list(range(n))\n'
                         '    def find(self, x):\n'
                         '        if self.p[x] != x:\n'
                         '            self.p[x] = self.find(self.p[x])\n'
                         '        return self.p[x]\n'
                         '    def union(self, x, y):\n'
                         '        rx, ry = self.find(x), self.find(y)\n'
                         '        if rx != ry:\n'
                         '            self.p[rx] = ry\n'
                         '            return True\n'
                         '        return False\n'
                         '\n'
                         'def count_components(n: int, edges: list[list[int]]) -> int:\n'
                         '    dsu = DSU(n)\n'
                         '    components = n\n'
                         '    for u, v in edges:\n'
                         '        if dsu.union(u, v):\n'
                         '            components -= 1\n'
                         '    return components\n'
                         '\n'
                         'edges = [[0, 1], [1, 2], [3, 4]]\n'
                         "print('Components count:', count_components(5, edges))\n",
             'starter': 'class DSU:\n'
                        '    def __init__(self, n):\n'
                        '        self.p = list(range(n))\n'
                        '    def find(self, x):\n'
                        '        if self.p[x] != x:\n'
                        '            self.p[x] = self.find(self.p[x])\n'
                        '        return self.p[x]\n'
                        '    def union(self, x, y):\n'
                        '        rx, ry = self.find(x), self.find(y)\n'
                        '        if rx != ry:\n'
                        '            self.p[rx] = ry\n'
                        '            return True\n'
                        '        return False\n'
                        '\n'
                        'def count_components(n: int, edges: list[list[int]]) -> int:\n'
                        '    # TODO: Union edges and count unique component roots\n'
                        '    return 0\n'
                        '\n'
                        'edges = [[0, 1], [1, 2], [3, 4]]\n'
                        "print('Components count:', count_components(5, edges)) # 2 ({0, 1, 2} and {3, 4})\n",
             'summary': 'Disjoint Set Union (DSU / Union-Find) maintains partitioned equivalence classes of elements, '
                        'executing Find and Union in near-constant amortized O(alpha(N)) time using Path Compression '
                        'and Union by Rank.',
             'takeaway': 'Path compression + union by rank flattens forest depths, delivering near-instant O(alpha(N)) '
                         'connectivity queries.'},
    131: {   'hint': 'Sort edges by w: edges.sort(key=lambda x: x[2]). Loop u, v, w: if dsu.union(u, v): total += w; '
                     'count += 1; if count == n - 1: break. Return total.',
             'mechanics': 'Sort all edges by weight ascending. Initialize DSU with V vertices, `mst_weight = 0`, '
                          '`edges_count = 0`. For each `(u, v, w)`: check `if dsu.find(u) != dsu.find(v)`: union u and '
                          'v, add w to `mst_weight`, increment `edges_count`. Stop when `edges_count == V - 1`.',
             'patterns': ['MST Weight: 19'],
             'practice_task': "Calculate the total weight of a Minimum Spanning Tree using Kruskal's algorithm.",
             'q1': "Why is the sorting step `O(E log E)` the asymptotic bottleneck of Kruskal's algorithm?",
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! DSU operations are so fast ($O(E \\cdot \\alpha(V)) \\approx O(E)$) that the '
                                'initial comparison sort on edge weights ($O(E \\log E) = O(E \\log V)$) completely '
                                'dictates total execution time.',
                           'B': 'Incorrect: DSU is near O(1) per operation.',
                           'C': 'Incorrect: Edges are sorted once.',
                           'D': 'Incorrect: Kruskal scans sorted edges linearly.'},
             'q1_opts': [   {   'id': 'A',
                                'label': 'Sorting E edges takes O(E log E), while the subsequent DSU operations take '
                                         'near-linear O(E * alpha(V)), making sorting dominant'},
                            {'id': 'B', 'label': 'Because DSU takes O(E^2) time'},
                            {'id': 'C', 'label': 'Because edges must be sorted twice'},
                            {'id': 'D', 'label': 'Because Kruskal uses binary search on vertices'}],
             'q2': 'What mathematical property of spanning trees ensures that Kruskal terminates when `edges_used == V '
                   '- 1`?',
             'q2_ans': 'A',
             'q2_exp': {   'A': 'Correct! A tree on V vertices has exactly V - 1 edges by definition. Once V - 1 '
                                'cycle-free edges have been merged into the DSU, all V vertices belong to a single '
                                'connected component.',
                           'B': 'Incorrect: Graphs can have up to V*(V-1)/2 edges.',
                           'C': 'Incorrect: DSU supports any number of elements.',
                           'D': 'Incorrect: Kruskal is an iterative loop.'},
             'q2_opts': [   {   'id': 'A',
                                'label': 'Any tree spanning V vertices consists of exactly V - 1 edges with zero '
                                         'cycles'},
                            {'id': 'B', 'label': 'A graph cannot have more than V - 1 edges'},
                            {'id': 'C', 'label': 'Because DSU only supports V - 1 elements'},
                            {'id': 'D', 'label': 'To prevent stack overflow'}],
             'recap': [   {   'concept': 'Global Greedy Edge Selection',
                              'naiveIntuition': 'Grow tree from an initial starting root',
                              'pythonReality': 'Kruskal operates globally across all edges, growing disconnected '
                                               'forest islands until they merge into a single tree'},
                          {   'concept': 'Cut Property Foundation',
                              'naiveIntuition': 'Greedy choices might fail globally',
                              'pythonReality': 'The Cut Property of graphs guarantees that the lightest edge crossing '
                                               'any partition cut must belong to some MST'}],
             'sample_code': "# Kruskal's MST\n"
                            'def kruskal(n, edges):\n'
                            '    edges.sort(key=lambda x: x[2]) # Sort by weight\n'
                            '    dsu = DSU(n)\n'
                            '    total_weight = 0\n'
                            '    edges_used = 0\n'
                            '    for u, v, w in edges:\n'
                            '        if dsu.union(u, v):\n'
                            '            total_weight += w\n'
                            '            edges_used += 1\n'
                            '            if edges_used == n - 1: break\n'
                            '    return total_weight if edges_used == n - 1 else -1',
             'solution': 'class DSU:\n'
                         '    def __init__(self, n):\n'
                         '        self.p = list(range(n))\n'
                         '    def find(self, x):\n'
                         '        if self.p[x] != x:\n'
                         '            self.p[x] = self.find(self.p[x])\n'
                         '        return self.p[x]\n'
                         '    def union(self, x, y):\n'
                         '        rx, ry = self.find(x), self.find(y)\n'
                         '        if rx != ry:\n'
                         '            self.p[rx] = ry\n'
                         '            return True\n'
                         '        return False\n'
                         '\n'
                         'def min_spanning_tree_weight(n: int, edges: list[list[int]]) -> int:\n'
                         '    edges.sort(key=lambda x: x[2])\n'
                         '    dsu = DSU(n)\n'
                         '    total = 0\n'
                         '    count = 0\n'
                         '    for u, v, w in edges:\n'
                         '        if dsu.union(u, v):\n'
                         '            total += w\n'
                         '            count += 1\n'
                         '            if count == n - 1:\n'
                         '                break\n'
                         '    return total if count == n - 1 else -1\n'
                         '\n'
                         'edges = [[0, 1, 10], [0, 2, 6], [0, 3, 5], [1, 3, 15], [2, 3, 4]]\n'
                         "print('MST Weight:', min_spanning_tree_weight(4, edges))\n",
             'starter': 'class DSU:\n'
                        '    def __init__(self, n):\n'
                        '        self.p = list(range(n))\n'
                        '    def find(self, x):\n'
                        '        if self.p[x] != x:\n'
                        '            self.p[x] = self.find(self.p[x])\n'
                        '        return self.p[x]\n'
                        '    def union(self, x, y):\n'
                        '        rx, ry = self.find(x), self.find(y)\n'
                        '        if rx != ry:\n'
                        '            self.p[rx] = ry\n'
                        '            return True\n'
                        '        return False\n'
                        '\n'
                        'def min_spanning_tree_weight(n: int, edges: list[list[int]]) -> int:\n'
                        "    # TODO: edges: [u, v, weight]. Implement Kruskal's algorithm\n"
                        '    return 0\n'
                        '\n'
                        'edges = [[0, 1, 10], [0, 2, 6], [0, 3, 5], [1, 3, 15], [2, 3, 4]]\n'
                        "print('MST Weight:', min_spanning_tree_weight(4, edges)) # 19 (edges: 2-3 (4), 0-3 (5), 0-1 "
                        '(10))\n',
             'summary': "Kruskal's Algorithm constructs a Minimum Spanning Tree (MST) by greedily sorting all edges by "
                        'weight and adding edges that do not form cycles using DSU in O(E log E) time.',
             'takeaway': 'Kruskal greedily adds the cheapest available edge that connects two previously disjoint '
                         'components.'},
    132: {   'hint': 'adj: u -> (v, w). visited = set(), pq = [(0, 0)], total = 0. While pq and len(visited) < n: pop '
                     'w, u. If u in visited continue. visited.add(u); total += w. Loop neighbors: push (weight, v) if '
                     'v not in visited.',
             'mechanics': 'Start with arbitrary root in `visited = {start}`. Min-heap stores candidate crossing edges '
                          '`(weight, neighbor)`. While heap non-empty and `len(visited) < V`: pop cheapest edge `(w, '
                          'u)`. If `u in visited`: discard. Else mark `visited.add(u)`, add `w` to MST weight, and '
                          'push all edges from `u` to unvisited neighbors.',
             'patterns': ['Prim MST Weight: 6'],
             'practice_task': "Compute the Minimum Spanning Tree weight using Prim's algorithm.",
             'q1': "How does Prim's algorithm differ conceptually from Kruskal's algorithm in how the tree grows?",
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! Prim maintains one connected tree at all times, adding the cheapest edge '
                                'crossing the cut between the tree and the remaining nodes. Kruskal considers all '
                                'edges globally, merging separate trees.',
                           'B': 'Incorrect: Prim uses a min-heap, Kruskal uses DSU.',
                           'C': 'Incorrect: Both algorithms operate on undirected weighted graphs.',
                           'D': 'Incorrect: Both compute an identical optimal MST total weight.'},
             'q1_opts': [   {   'id': 'A',
                                'label': 'Prim grows a single contiguous tree outwards from an initial vertex, while '
                                         'Kruskal merges an independent forest of disconnected components across the '
                                         'whole graph'},
                            {'id': 'B', 'label': 'Prim uses a stack, Kruskal uses a queue'},
                            {'id': 'C', 'label': 'Prim only works on directed graphs'},
                            {'id': 'D', 'label': 'Kruskal produces a tree with lower weight than Prim'}],
             'q2': "When is Prim's algorithm preferred over Kruskal's algorithm?",
             'q2_ans': 'A',
             'q2_exp': {   'A': "Correct! In dense graphs with E ~ V^2, Kruskal's sorting costs $O(V^2 \\log V)$. "
                                "Prim's algorithm (using an adjacency matrix and distance array) runs in $O(V^2)$ "
                                'without sorting edges.',
                           'B': 'Incorrect: Negative weights do not affect MST algorithms because spanning trees have '
                                'fixed V-1 edges without cycles.',
                           'C': 'Incorrect: Disconnected graphs cannot form a single spanning tree.',
                           'D': 'Incorrect: Neither fits in 1 byte.'},
             'q2_opts': [   {   'id': 'A',
                                'label': 'On dense graphs where E approaches V^2 (especially with an adjacency matrix '
                                         'implementation O(V^2))'},
                            {'id': 'B', 'label': 'When all edge weights are negative'},
                            {'id': 'C', 'label': 'When the graph is disconnected'},
                            {'id': 'D', 'label': 'When memory is limited to 1 byte'}],
             'recap': [   {   'concept': 'Cut Edge Relaxation',
                              'naiveIntuition': 'Sort all graph edges first',
                              'pythonReality': 'Prim only inspects edges incident to the current tree boundary, '
                                               'dynamically maintaining cut candidates via min-heap'},
                          {   'concept': 'Structural Invariant Equivalence',
                              'naiveIntuition': 'Different MST algorithms produce different weights',
                              'pythonReality': 'Both Kruskal and Prim produce the identical minimum spanning tree '
                                               'weight for any connected weighted graph'}],
             'sample_code': "# Prim's MST\n"
                            'import heapq\n'
                            'def prim(n, adj):\n'
                            '    visited = set()\n'
                            '    pq = [(0, 0)] # (weight, vertex)\n'
                            '    total_weight = 0\n'
                            '    while pq and len(visited) < n:\n'
                            '        w, u = heapq.heappop(pq)\n'
                            '        if u in visited: continue\n'
                            '        visited.add(u)\n'
                            '        total_weight += w\n'
                            '        for v, weight in adj[u]:\n'
                            '            if v not in visited:\n'
                            '                heapq.heappush(pq, (weight, v))\n'
                            '    return total_weight if len(visited) == n else -1',
             'solution': 'import heapq\n'
                         '\n'
                         'def prim_mst(n: int, edges: list[list[int]]) -> int:\n'
                         '    adj = {i: [] for i in range(n)}\n'
                         '    for u, v, w in edges:\n'
                         '        adj[u].append((v, w))\n'
                         '        adj[v].append((u, w))\n'
                         '    \n'
                         '    visited = set()\n'
                         '    pq = [(0, 0)]\n'
                         '    total = 0\n'
                         '    while pq and len(visited) < n:\n'
                         '        w, u = heapq.heappop(pq)\n'
                         '        if u in visited:\n'
                         '            continue\n'
                         '        visited.add(u)\n'
                         '        total += w\n'
                         '        for v, weight in adj[u]:\n'
                         '            if v not in visited:\n'
                         '                heapq.heappush(pq, (weight, v))\n'
                         '    return total if len(visited) == n else -1\n'
                         '\n'
                         'edges = [[0, 1, 1], [1, 2, 2], [0, 2, 4], [2, 3, 3]]\n'
                         "print('Prim MST Weight:', prim_mst(4, edges))\n",
             'starter': 'import heapq\n'
                        '\n'
                        'def prim_mst(n: int, edges: list[list[int]]) -> int:\n'
                        "    # TODO: Build adj list and implement Prim's algorithm with heapq\n"
                        '    return 0\n'
                        '\n'
                        'edges = [[0, 1, 1], [1, 2, 2], [0, 2, 4], [2, 3, 3]]\n'
                        "print('Prim MST Weight:', prim_mst(4, edges)) # 6 (edges: 0-1 (1), 1-2 (2), 2-3 (3))\n",
             'summary': "Prim's Algorithm constructs an MST by growing a single connected tree from an arbitrary "
                        'starting vertex, greedily adding the cheapest cut edge using a Min-Heap in O((V + E) log V) '
                        'time.',
             'takeaway': 'Prim grows a single tree vertex by vertex; Kruskal merges a forest edge by edge.'},
    133: {   'hint': 'tin = [-1] * n, low = [-1] * n, timer = 0. In dfs(u, p): tin[u] = low[u] = timer; timer += 1. '
                     'For v in adj[u]: if v == p continue. If tin[v] != -1: low[u] = min(low[u], tin[v]). Else: dfs(v, '
                     'u); low[u] = min(low[u], low[v]); if low[v] > tin[u]: bridges.append([u, v]).',
             'mechanics': 'Track discovery time `tin[u]` and lowest reachable discovery time `low[u]`. For edge `(u, '
                          'v)`: if `v == parent`: continue. If `v` already visited: `low[u] = min(low[u], tin[v])` '
                          '(back-edge). Else recurse on `v`, then `low[u] = min(low[u], low[v])`. Bridge condition: if '
                          '`low[v] > tin[u]`, edge `(u, v)` is a critical bridge!',
             'patterns': ['Bridges: [[1, 3]]'],
             'practice_task': "Find all critical connection bridges in a network using Tarjan's algorithm.",
             'q1': "What does the condition `low[v] > tin[u]` prove about edge `(u, v)` in Tarjan's algorithm?",
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! `tin[u]` is when u was discovered. If `low[v] > tin[u]`, it means the '
                                "highest ancestor reachable from v's subtree was discovered strictly after u. "
                                'Therefore, no alternate path back to the rest of the graph exists.',
                           'B': "Incorrect: If (u, v) were part of a triangle, low[v] <= tin[u], so it wouldn't be a "
                                'bridge.',
                           'C': 'Incorrect: Degree is irrelevant.',
                           'D': 'Incorrect: Bridges are unweighted structural edges.'},
             'q1_opts': [   {   'id': 'A',
                                'label': 'Node v and its entire subtree have zero back-edges reaching ancestor u or '
                                         "earlier, so removing (u, v) completely isolates v's component"},
                            {'id': 'B', 'label': 'Edge (u, v) is part of a triangle'},
                            {'id': 'C', 'label': 'Vertex v has a smaller degree than u'},
                            {'id': 'D', 'label': 'The graph contains a negative cycle'}],
             'q2': 'Why must the check `if v == p: continue` be enforced in undirected bridge discovery?',
             'q2_ans': 'A',
             'q2_exp': {   'A': 'Correct! In undirected graphs, (u, v) implies (v, u). If we allowed `low[u] = '
                                'min(low[u], tin[parent])`, EVERY edge would trivially claim low <= tin, falsely '
                                'hiding all bridges.',
                           'B': 'Incorrect: Graph is general undirected graph.',
                           'C': 'Incorrect: Parents are active in the recursion stack.',
                           'D': 'Incorrect: Has nothing to do with sorting.'},
             'q2_opts': [   {   'id': 'A',
                                'label': 'To prevent treating the trivial reciprocal edge back to the direct parent as '
                                         'a cycle-forming back-edge'},
                            {'id': 'B', 'label': 'To prevent infinite loops in binary trees'},
                            {'id': 'C', 'label': 'Because parent nodes are already deleted'},
                            {'id': 'D', 'label': 'To sort edges'}],
             'recap': [   {   'concept': 'Low-Link Reachability Metric',
                              'naiveIntuition': 'Test each edge by deleting it and re-running BFS O(E * (V + E))',
                              'pythonReality': "Tarjan's low-link discovery time identifies all critical bridges in a "
                                               'single O(V + E) linear pass'},
                          {   'concept': 'Infrastructure Resilience',
                              'naiveIntuition': 'All redundant networks are robust',
                              'pythonReality': 'Bridge edges represent single points of failure in power grids, '
                                               'internet backbones, and distributed consensus clusters'}],
             'sample_code': "# Tarjan's Bridges Detection\n"
                            'def find_bridges(n, adj):\n'
                            '    tin = [-1] * n\n'
                            '    low = [-1] * n\n'
                            '    timer = 0\n'
                            '    bridges = []\n'
                            '    def dfs(u, p=-1):\n'
                            '        nonlocal timer\n'
                            '        tin[u] = low[u] = timer\n'
                            '        timer += 1\n'
                            '        for v in adj[u]:\n'
                            '            if v == p: continue\n'
                            '            if tin[v] != -1:\n'
                            '                low[u] = min(low[u], tin[v])\n'
                            '            else:\n'
                            '                dfs(v, u)\n'
                            '                low[u] = min(low[u], low[v])\n'
                            '                if low[v] > tin[u]:\n'
                            '                    bridges.append((u, v))\n'
                            '    for i in range(n):\n'
                            '        if tin[i] == -1: dfs(i)\n'
                            '    return bridges',
             'solution': 'def critical_connections(n: int, connections: list[list[int]]) -> list[list[int]]:\n'
                         '    adj = {i: [] for i in range(n)}\n'
                         '    for u, v in connections:\n'
                         '        adj[u].append(v)\n'
                         '        adj[v].append(u)\n'
                         '    \n'
                         '    tin = [-1] * n\n'
                         '    low = [-1] * n\n'
                         '    timer = 0\n'
                         '    bridges = []\n'
                         '    \n'
                         '    def dfs(u, p=-1):\n'
                         '        nonlocal timer\n'
                         '        tin[u] = low[u] = timer\n'
                         '        timer += 1\n'
                         '        for v in adj[u]:\n'
                         '            if v == p:\n'
                         '                continue\n'
                         '            if tin[v] != -1:\n'
                         '                low[u] = min(low[u], tin[v])\n'
                         '            else:\n'
                         '                dfs(v, u)\n'
                         '                low[u] = min(low[u], low[v])\n'
                         '                if low[v] > tin[u]:\n'
                         '                    bridges.append([u, v])\n'
                         '                    \n'
                         '    for i in range(n):\n'
                         '        if tin[i] == -1:\n'
                         '            dfs(i)\n'
                         '    return bridges\n'
                         '\n'
                         'conns = [[0, 1], [1, 2], [2, 0], [1, 3]]\n'
                         "print('Bridges:', critical_connections(4, conns))\n",
             'starter': 'def critical_connections(n: int, connections: list[list[int]]) -> list[list[int]]:\n'
                        "    # TODO: Implement Tarjan's bridge algorithm\n"
                        '    return []\n'
                        '\n'
                        '# 0-1, 1-2, 2-0 (cycle), 1-3 (bridge to 3)\n'
                        'conns = [[0, 1], [1, 2], [2, 0], [1, 3]]\n'
                        "print('Bridges:', critical_connections(4, conns)) # [[1, 3]]\n",
             'summary': 'Bridges and Articulation Points identify critical failure edges and vertices whose removal '
                        "increases graph connected components, discovered via Tarjan's Low-Link DFS in O(V + E) time.",
             'takeaway': "If a subtree's lowest reachable node is discovered strictly AFTER u (low[v] > tin[u]), edge "
                         '(u, v) is a bridge.'},
    134: {   'hint': 'Pass 1: dfs on adj, push to stack on finish. Invert edges into adj_rev. Pass 2: pop from stack, '
                     'if not visited in G^T, dfs on adj_rev to gather SCC component.',
             'mechanics': 'Pass 1: Run DFS on original graph, recording vertices in a stack upon finishing. Pass 2: '
                          'Invert all directed edges (transpose graph $G^T$). Pop vertices from stack; if unvisited in '
                          '$G^T$, launch DFS to collect the entire SCC.',
             'patterns': ['SCCs: [[0, 1, 2], [3]]'],
             'practice_task': "Find all Strongly Connected Components in a directed graph using Kosaraju's algorithm.",
             'q1': 'Why does reversing the graph edges ($G^T$) prevent DFS in Pass 2 from leaking into other SCCs?',
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! In the condensation DAG of SCCs, edges point from source SCC to sink SCC. In '
                                '$G^T$, edges point from sink to source. Popping the highest finish time starts at the '
                                'source of $G^T$ (the sink of G), trapping the search strictly within that SCC.',
                           'B': 'Incorrect: Cycles inside an SCC remain cycles in $G^T$.',
                           'C': 'Incorrect: Transpose graph remains directed.',
                           'D': 'Incorrect: Edge count is identical.'},
             'q1_opts': [   {   'id': 'A',
                                'label': 'Edges between SCCs point from earlier-finishing components to later ones in '
                                         '$G^T$; popping from the stack processes components in topological sink '
                                         'order, preventing outward escape'},
                            {'id': 'B', 'label': 'Because reversing edges destroys all cycles'},
                            {'id': 'C', 'label': 'Because $G^T$ converts the directed graph into an undirected graph'},
                            {'id': 'D', 'label': 'Because transpose graphs have half as many edges'}],
             'q2': 'What is the result of condensing every SCC in a directed graph into a single super-vertex?',
             'q2_ans': 'A',
             'q2_exp': {   'A': 'Correct! By definition, all mutual reachability cycles are collapsed inside their '
                                'respective SCCs. Any remaining inter-component edges must be strictly acyclic, '
                                'forming the Condensation DAG.',
                           'B': 'Incorrect: Only edges between components exist.',
                           'C': 'Incorrect: Edges remain strictly directed.',
                           'D': 'Incorrect: If an inter-component cycle existed, those components would have merged '
                                'into a single SCC.'},
             'q2_opts': [   {'id': 'A', 'label': 'A Directed Acyclic Graph (DAG) with zero cycles'},
                            {'id': 'B', 'label': 'A complete graph'},
                            {'id': 'C', 'label': 'An undirected tree'},
                            {'id': 'D', 'label': 'A single giant cycle'}],
             'recap': [   {   'concept': 'Transpose Graph Trapping',
                              'naiveIntuition': 'SCC requires checking all pairs reachability in O(V^3)',
                              'pythonReality': 'Two linear DFS passes on G and G^T decompose the graph into SCCs in '
                                               'optimal O(V + E) time'},
                          {   'concept': 'Condensation DAG',
                              'naiveIntuition': 'Cyclic graphs cannot be topologically sorted',
                              'pythonReality': 'Collapsing SCCs produces a condensation DAG that CAN be topologically '
                                               'sorted, enabling dynamic programming on general directed graphs'}],
             'sample_code': "# Kosaraju's SCC Algorithm\n"
                            'def kosaraju_scc(n, adj):\n'
                            '    stack = []\n'
                            '    visited = [False] * n\n'
                            '    def dfs1(u):\n'
                            '        visited[u] = True\n'
                            '        for v in adj[u]:\n'
                            '            if not visited[v]: dfs1(v)\n'
                            '        stack.append(u) # Finish stack\n'
                            '    for i in range(n):\n'
                            '        if not visited[i]: dfs1(i)\n'
                            '    # Transpose graph\n'
                            '    adj_rev = {i: [] for i in range(n)}\n'
                            '    for u in range(n):\n'
                            '        for v in adj[u]: adj_rev[v].append(u)\n'
                            '    # Pass 2\n'
                            '    visited = [False] * n\n'
                            '    sccs = []\n'
                            '    while stack:\n'
                            '        u = stack.pop()\n'
                            '        if not visited[u]:\n'
                            '            comp = []\n'
                            '            def dfs2(curr):\n'
                            '                visited[curr] = True\n'
                            '                comp.append(curr)\n'
                            '                for nxt in adj_rev[curr]:\n'
                            '                    if not visited[nxt]: dfs2(nxt)\n'
                            '            dfs2(u)\n'
                            '            sccs.append(comp)\n'
                            '    return sccs',
             'solution': 'def find_sccs(n: int, edges: list[list[int]]) -> list[list[int]]:\n'
                         '    adj = {i: [] for i in range(n)}\n'
                         '    adj_rev = {i: [] for i in range(n)}\n'
                         '    for u, v in edges:\n'
                         '        adj[u].append(v)\n'
                         '        adj_rev[v].append(u)\n'
                         '    \n'
                         '    stack = []\n'
                         '    visited = [False] * n\n'
                         '    def dfs1(u):\n'
                         '        visited[u] = True\n'
                         '        for v in adj[u]:\n'
                         '            if not visited[v]:\n'
                         '                dfs1(v)\n'
                         '        stack.append(u)\n'
                         '        \n'
                         '    for i in range(n):\n'
                         '        if not visited[i]:\n'
                         '            dfs1(i)\n'
                         '            \n'
                         '    visited = [False] * n\n'
                         '    sccs = []\n'
                         '    while stack:\n'
                         '        root = stack.pop()\n'
                         '        if not visited[root]:\n'
                         '            comp = []\n'
                         '            def dfs2(u):\n'
                         '                visited[u] = True\n'
                         '                comp.append(u)\n'
                         '                for v in adj_rev[u]:\n'
                         '                    if not visited[v]:\n'
                         '                        dfs2(v)\n'
                         '            dfs2(root)\n'
                         '            sccs.append(sorted(comp))\n'
                         '    return sorted(sccs)\n'
                         '\n'
                         'edges = [[0, 1], [1, 2], [2, 0], [2, 3]]\n'
                         "print('SCCs:', find_sccs(4, edges))\n",
             'starter': 'def find_sccs(n: int, edges: list[list[int]]) -> list[list[int]]:\n'
                        "    # TODO: Implement Kosaraju's 2-pass algorithm\n"
                        '    return []\n'
                        '\n'
                        '# SCC 1: 0 -> 1 -> 2 -> 0; Edge: 2 -> 3; SCC 2: 3\n'
                        'edges = [[0, 1], [1, 2], [2, 0], [2, 3]]\n'
                        "print('SCCs:', find_sccs(4, edges))\n",
             'summary': 'Strongly Connected Components (SCCs) are maximal subgraphs in directed graphs where every '
                        "vertex is reachable from every other vertex, decomposed via Kosaraju's Two-Pass Algorithm in "
                        'O(V + E) time.',
             'takeaway': 'Reversing edges in G^T traps DFS inside the source SCC, isolating strongly connected '
                         'components.'},
    135: {   'hint': 'Build undirected adj. dist = [inf]*n, dist[src] = 0, pq = [(0, src)]. While pq: pop d, u. If d > '
                     'dist[u] continue. If u == dst return d. For v, w in adj[u]: if dist[u] + w < dist[v]: dist[v] = '
                     'dist[u] + w, push (dist[v], v). Return -1.',
             'mechanics': 'Graph Algorithm Selector: (1) Unweighted shortest path? BFS. (2) Topological dependency? '
                          "Kahn's or DFS Topo. (3) Non-negative weighted shortest path? Dijkstra. (4) Negative "
                          'weights/cycles? Bellman-Ford. (5) Disjoint connectivity / dynamic merges? DSU. (6) Minimum '
                          'Spanning Tree? Kruskal (sparse) or Prim (dense). (7) 2-coloring? Bipartite BFS. (8) '
                          "Critical edges? Tarjan's low-link bridges. (9) Mutual reachability? Kosaraju/Tarjan SCCs.",
             'patterns': ['Min latency 0 -> 3: 9'],
             'practice_task': 'Build an all-in-one Network Path Analyzer that finds the minimum latency route between '
                              'servers using Dijkstra.',
             'q1': 'You need to find the shortest delivery route in a city network with 50,000 intersections and '
                   '120,000 one-way streets with non-negative street lengths. Which algorithm is optimal?',
             'q1_ans': 'A',
             'q1_exp': {   'A': 'Correct! Non-negative weights on a sparse graph (120K edges on 50K vertices) are '
                                'perfectly optimized by Dijkstra with a min-heap, resolving the route in milliseconds. '
                                'Bellman-Ford would require ~6 billion operations.',
                           'B': "Incorrect: Bellman-Ford's O(V*E) would take minutes/hours.",
                           'C': 'Incorrect: BFS ignores street lengths, giving incorrect route distances.',
                           'D': 'Incorrect: Kosaraju finds strongly connected components, not shortest paths.'},
             'q1_opts': [   {   'id': 'A',
                                'label': "Dijkstra's Algorithm with a Min-Heap, running in O((V + E) log V) time"},
                            {'id': 'B', 'label': 'Bellman-Ford Algorithm in O(V * E) time'},
                            {'id': 'C', 'label': 'Standard unweighted BFS'},
                            {'id': 'D', 'label': "Kosaraju's Algorithm"}],
             'q2': 'Which algorithm determines whether an electrical power grid will split into disconnected islands '
                   'if any single transmission line fails?',
             'q2_ans': 'A',
             'q2_exp': {   'A': 'Correct! A transmission line whose removal splits the network into disconnected '
                                'components is by definition a bridge edge, discovered in linear O(V + E) time by '
                                "Tarjan's low-link algorithm.",
                           'B': 'Incorrect: Dijkstra computes shortest path distances.',
                           'C': "Incorrect: Kahn's applies to directed acyclic dependencies.",
                           'D': 'Incorrect: Floyd-Warshall computes all-pairs shortest paths in O(V^3).'},
             'q2_opts': [   {'id': 'A', 'label': "Tarjan's Bridge-Finding Algorithm in O(V + E) time"},
                            {'id': 'B', 'label': "Dijkstra's Algorithm"},
                            {'id': 'C', 'label': "Kahn's Topological Sort"},
                            {'id': 'D', 'label': 'Floyd-Warshall Algorithm'}],
             'recap': [   {   'concept': 'Algorithm Invariant Alignment',
                              'naiveIntuition': 'One graph algorithm fits all scenarios',
                              'pythonReality': 'Selecting graph algorithms is an exact science dictated by edge '
                                               'weights, graph directionality, and output requirements'},
                          {   'concept': 'Section 11 Synthesis',
                              'naiveIntuition': 'Graphs are disparate collection of independent tricks',
                              'pythonReality': 'All graph algorithms are state-space search variations over vertices '
                                               'and edges with specific pruning invariants'}],
             'sample_code': '# Graph Master Selection Matrix:\n'
                            '# BFS: Unweighted Shortest Path O(V + E)\n'
                            '# Dijkstra: Non-negative Weighted Shortest Path O((V + E) log V)\n'
                            '# Bellman-Ford: Arbitrary Weights + Negative Cycles O(V * E)\n'
                            '# DSU: Dynamic Connectivity O(alpha(V))\n'
                            '# Kruskal/Prim: MST O(E log V)',
             'solution': 'import heapq\n'
                         '\n'
                         'def analyze_network(n: int, connections: list[list[int]], src: int, dst: int) -> int:\n'
                         '    adj = {i: [] for i in range(n)}\n'
                         '    for u, v, w in connections:\n'
                         '        adj[u].append((v, w))\n'
                         '        adj[v].append((u, w))\n'
                         '    \n'
                         "    dist = [float('inf')] * n\n"
                         '    dist[src] = 0\n'
                         '    pq = [(0, src)]\n'
                         '    while pq:\n'
                         '        d, u = heapq.heappop(pq)\n'
                         '        if d > dist[u]:\n'
                         '            continue\n'
                         '        if u == dst:\n'
                         '            return d\n'
                         '        for v, w in adj[u]:\n'
                         '            if dist[u] + w < dist[v]:\n'
                         '                dist[v] = dist[u] + w\n'
                         '                heapq.heappush(pq, (dist[v], v))\n'
                         "    return -1 if dist[dst] == float('inf') else dist[dst]\n"
                         '\n'
                         'conns = [[0, 1, 10], [0, 2, 3], [2, 1, 1], [1, 3, 5], [2, 3, 8]]\n'
                         "print('Min latency 0 -> 3:', analyze_network(4, conns, 0, 3))\n",
             'starter': 'import heapq\n'
                        '\n'
                        'def analyze_network(n: int, connections: list[list[int]], src: int, dst: int) -> int:\n'
                        '    # TODO: connections: [u, v, latency_ms]\n'
                        '    # Find minimum latency from src to dst using Dijkstra\n'
                        '    return -1\n'
                        '\n'
                        'conns = [[0, 1, 10], [0, 2, 3], [2, 1, 1], [1, 3, 5], [2, 3, 8]]\n'
                        "print('Min latency 0 -> 3:', analyze_network(4, conns, 0, 3))\n",
             'summary': 'Section 11 Review synthesizes graph representations, BFS shortest path, 3-color DFS cycle '
                        'detection, Topological Sort, Dijkstra, Bellman-Ford, DSU, Kruskal, Prim, Bipartite, Bridges, '
                        'and SCCs into an algorithmic master blueprint.',
             'takeaway': 'Every graph algorithm matches specific edge constraints (weighted vs unweighted, directed vs '
                         'undirected, positive vs negative).'}}
