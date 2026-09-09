import { DailyLessonPackage } from "../types";

export const BATCH_7_LESSONS: Record<number, DailyLessonPackage> = {
  121: {
  "dayNumber": 121,
  "title": "Graph Representations & Adjacency Lists",
  "topicName": "Graph Representations",
  "sectionId": "graphs",
  "estimatedMinutes": 30,
  "difficulty": "ADVANCED",
  "prerequisites": [
    15,
    18,
    36
  ],
  "concepts": [
    "Adjacency List vs Adjacency Matrix",
    "Directed, Undirected & Weighted Graphs"
  ],
  "practiceSkills": [
    "Graph Representations Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Construct adjacency list dictionary representations from edge lists in O(V + E) time",
    "Evaluate space and edge query trade-offs between sparse lists and dense matrices"
  ],
  "practiceArchetype": "guided",
  "flowTier": "tier1"
,
  "steps": [
    {
        "id": "day121-step1",
        "stepNumber": 1,
        "title": "Graph Representations & Adjacency Lists: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Graph Representations",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Graph Representations.",
        "markdownContent": [
            "Graph Representations model pairwise relationships via Adjacency Lists (optimal for sparse graphs) or Adjacency Matrices (optimal for dense graphs).",
            "### Foundational Mental Model\nWhen approaching problems requiring **Graph Representations**, remember the central principle: Adjacency lists provide optimal O(V + E) space for sparse graphs and rapid neighbor iteration."
        ],
        "snippets": [
            {
                "title": "Graph Representations Implementation Template",
                "code": "# Adjacency List from edge list\ndef build_adj_list(n, edges, directed=False):\n    adj = {i: [] for i in range(n)}\n    for u, v in edges:\n        adj[u].append(v)\n        if not directed: adj[v].append(u)\n    return adj",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Adjacency lists provide optimal O(V + E) space for sparse graphs and rapid neighbor iteration."
    },
    {
        "id": "day121-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Graph Representations",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Adjacency List (`dict[int, list[int]]`): O(V + E) memory, O(deg(u)) neighbor iteration. Adjacency Matrix (`list[list[int]]`): O(V^2) memory, O(1) edge lookup `matrix[u][v]`. In real-world graphs where E << V^2, adjacency lists dominate.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Adjacency lists provide optimal O(V + E) space for sparse graphs and rapid neighbor iteration.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Graph Representations Core Invariant",
                "content": "Adjacency lists provide optimal O(V + E) space for sparse graphs and rapid neighbor iteration."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Adjacency lists provide optimal O(V + E) space for sparse graphs and rapid neighbor iteration."
    },
    {
        "id": "day121-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Graph Representations",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d121-q1",
                "question": "Why is an Adjacency List preferred over an Adjacency Matrix for a sparse graph with 1,000,000 vertices and 2,000,000 edges?",
                "options": [
                    {
                        "id": "A",
                        "label": "An adjacency matrix would allocate 1,000,000 x 1,000,000 cells (~1 Terabyte of RAM), whereas an adjacency list consumes only O(V + E) (~24 Megabytes)"
                    },
                    {
                        "id": "B",
                        "label": "Because adjacency lists sort vertex values automatically"
                    },
                    {
                        "id": "C",
                        "label": "Because matrices cannot represent directed graphs"
                    },
                    {
                        "id": "D",
                        "label": "Because Python does not support 2D arrays"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! V^2 for 1M vertices is 10^12 elements (terabytes of memory). An adjacency list stores only actual edges (2M entries), fitting comfortably in standard RAM.",
                    "B": "Incorrect: Lists do not sort elements automatically.",
                    "C": "Incorrect: Asymmetric matrices easily represent directed graphs.",
                    "D": "Incorrect: Python lists of lists easily form 2D matrices."
                }
            },
            {
                "id": "chk-d121-q2",
                "question": "What is the time complexity to check if an edge exists between vertex u and vertex v in an Adjacency Matrix versus an Adjacency List?",
                "options": [
                    {
                        "id": "A",
                        "label": "Matrix is O(1) direct lookup, while Adjacency List is O(degree(u)) search"
                    },
                    {
                        "id": "B",
                        "label": "Both are O(1)"
                    },
                    {
                        "id": "C",
                        "label": "Both are O(V)"
                    },
                    {
                        "id": "D",
                        "label": "List is O(1), Matrix is O(V)"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! In a matrix, `matrix[u][v]` is an instant O(1) index lookup. In an adjacency list, one must scan the neighbors of u (`v in adj[u]`), taking O(deg(u)).",
                    "B": "Incorrect: List search requires scanning neighbor array.",
                    "C": "Incorrect: Matrix is direct index access.",
                    "D": "Incorrect: Inverted."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day121-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Graph Representations",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Build an undirected Adjacency List from an edge list and calculate vertex degrees.",
        "subheading": "Implement and verify Graph Representations in the interactive workspace.",
        "task": {
            "title": "Build an undirected Adjacency List from an edge list and calculate vertex degrees.",
            "instructions": [
                "Build an undirected Adjacency List from an edge list and calculate vertex degrees.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "def get_vertex_degrees(n: int, edges: list[list[int]]) -> dict[int, int]:\n    # TODO: Construct adjacency list and return degree of each vertex\n    return {}\n\nedges = [[0, 1], [0, 2], [1, 2], [2, 3]]\nprint('Degrees:', get_vertex_degrees(4, edges))\n",
            "solutionCode": "def get_vertex_degrees(n: int, edges: list[list[int]]) -> dict[int, int]:\n    adj = {i: [] for i in range(n)}\n    for u, v in edges:\n        adj[u].append(v)\n        adj[v].append(u)\n    return {i: len(adj[i]) for i in range(n)}\n\nedges = [[0, 1], [0, 2], [1, 2], [2, 3]]\nprint('Degrees:', get_vertex_degrees(4, edges))\n",
            "expectedOutputPatterns": [
                "Degrees: {0: 2, 1: 2, 2: 3, 3: 1}"
            ],
            "hint": "Build adj = {i: [] for i in range(n)}. Loop u, v: adj[u].append(v); adj[v].append(u). Return {i: len(adj[i]) for i in range(n)}."
        },
        "keyTakeaway": "Successfully implemented and verified Graph Representations!"
    },
    {
        "id": "day121-step5",
        "stepNumber": 5,
        "title": "Day 121 Complete: Graph Representations & Adjacency Lists",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 121,
        "heading": "Mastery Achieved: Graph Representations & Adjacency Lists",
        "subheading": "You have solidified key mental models and techniques for Graph Representations.",
        "recapRows": [
            {
                "concept": "Sparsity Advantage",
                "naiveIntuition": "Always use 2D matrices for graphs",
                "pythonReality": "Most real-world networks (web links, social graphs) are extremely sparse; adjacency lists prevent catastrophic O(V^2) memory explosions"
            },
            {
                "concept": "Neighbor Iteration Bound",
                "naiveIntuition": "Finding neighbors in a matrix is O(deg(u))",
                "pythonReality": "Finding neighbors in a matrix requires scanning all V columns (O(V)); adjacency lists iterate strictly over the degree of u"
            }
        ],
        "solidifiedConcepts": [
            "Adjacency List vs Adjacency Matrix",
            "Directed, Undirected & Weighted Graphs"
        ],
        "nextDayPreview": {
            "dayNumber": 122,
            "title": "BFS & Unweighted Shortest Path",
            "description": "Implement BFS using collections.deque to find shortest paths on unweighted graphs and reconstruct shortest paths."
        }
    }
]
},
  122: {
  "dayNumber": 122,
  "title": "BFS & Unweighted Shortest Path",
  "topicName": "Breadth-First Search",
  "sectionId": "graphs",
  "estimatedMinutes": 35,
  "difficulty": "ADVANCED",
  "prerequisites": [
    89,
    121
  ],
  "concepts": [
    "FIFO Queue Level Expansion",
    "Predecessor Array & Distance Tracking"
  ],
  "practiceSkills": [
    "Breadth-First Search Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Implement Breadth-First Search (BFS) to find shortest path distances on unweighted graphs",
    "Reconstruct shortest path vertices using a predecessor parent map in O(V + E) time"
  ],
  "practiceArchetype": "algorithm",
  "flowTier": "tier2"
,
  "steps": [
    {
        "id": "day122-step1",
        "stepNumber": 1,
        "title": "BFS & Unweighted Shortest Path: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Breadth-First Search",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Breadth-First Search.",
        "markdownContent": [
            "Breadth-First Search (BFS) finds the Shortest Path in Unweighted Graphs by exploring vertices in concentric expanding rings of distance using a FIFO Queue.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Breadth-First Search**, remember the central principle: In unweighted graphs, the first time BFS reaches a vertex is guaranteed to be its shortest path."
        ],
        "snippets": [
            {
                "title": "Breadth-First Search Implementation Template",
                "code": "from collections import deque\ndef bfs_shortest_path(adj, start, target):\n    q = deque([(start, 0)])\n    visited = {start}\n    while q:\n        curr, d = q.popleft()\n        if curr == target: return d\n        for nxt in adj[curr]:\n            if nxt not in visited:\n                visited.add(nxt)\n                q.append((nxt, d + 1))\n    return -1",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "In unweighted graphs, the first time BFS reaches a vertex is guaranteed to be its shortest path."
    },
    {
        "id": "day122-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Breadth-First Search",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Initialize `queue = deque([start])`, `visited = {start}`, `dist = {start: 0}`. While queue is non-empty: pop `curr = q.popleft()`. For each `neighbor` of `curr`: if `neighbor not in visited`, mark visited, record `dist[neighbor] = dist[curr] + 1`, and enqueue. Terminates in O(V + E) time.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: In unweighted graphs, the first time BFS reaches a vertex is guaranteed to be its shortest path.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Breadth-First Search Core Invariant",
                "content": "In unweighted graphs, the first time BFS reaches a vertex is guaranteed to be its shortest path."
            }
        ],
        "keyTakeaway": "Operational invariant locked: In unweighted graphs, the first time BFS reaches a vertex is guaranteed to be its shortest path."
    },
    {
        "id": "day122-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Breadth-First Search",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d122-q1",
                "question": "Why is the first path discovered by BFS to any node guaranteed to be the shortest path in an unweighted graph?",
                "options": [
                    {
                        "id": "A",
                        "label": "BFS explores all nodes at distance K before exploring any node at distance K + 1, making earlier arrival strictly shorter"
                    },
                    {
                        "id": "B",
                        "label": "Because BFS sorts the edge weights in ascending order"
                    },
                    {
                        "id": "C",
                        "label": "Because graphs have no cycles"
                    },
                    {
                        "id": "D",
                        "label": "Because the queue uses binary search"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! FIFO queue properties ensure that nodes are visited in monotonically increasing order of edge distance: distance 0, then all distance 1, then all distance 2. Thus, the first arrival is minimal.",
                    "B": "Incorrect: Unweighted graphs have uniform edge costs of 1.",
                    "C": "Incorrect: Graphs can have cycles; visited sets prevent re-visiting.",
                    "D": "Incorrect: Queues pop in FIFO order, not binary search."
                }
            },
            {
                "id": "chk-d122-q2",
                "question": "What catastrophic bug occurs if you mark a vertex as `visited` upon POPPING from the queue rather than upon PUSHING?",
                "options": [
                    {
                        "id": "A",
                        "label": "Multiple paths to the same unvisited node will push redundant duplicate copies into the queue, causing exponential memory bloat and TLE"
                    },
                    {
                        "id": "B",
                        "label": "Python raises an unhandled KeyError"
                    },
                    {
                        "id": "C",
                        "label": "The graph reverses direction"
                    },
                    {
                        "id": "D",
                        "label": "The shortest path becomes negative"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Marking visited upon enqueueing immediately blocks other incoming paths from re-adding that same vertex. Delaying visited marking until dequeueing allows dense graphs to enqueue the same vertex $O(V)$ times, exploding queue size.",
                    "B": "Incorrect: No KeyError is raised.",
                    "C": "Incorrect: Traversal directions are unaffected.",
                    "D": "Incorrect: Unweighted distances are always non-negative integers."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day122-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Breadth-First Search",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Find the shortest path distance between start and end vertices in an unweighted graph using BFS.",
        "subheading": "Implement and verify Breadth-First Search in the interactive workspace.",
        "task": {
            "title": "Find the shortest path distance between start and end vertices in an unweighted graph using BFS.",
            "instructions": [
                "Find the shortest path distance between start and end vertices in an unweighted graph using BFS.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "from collections import deque\n\ndef shortest_path(n: int, edges: list[list[int]], start: int, target: int) -> int:\n    # TODO: Build adjacency list and find shortest distance using BFS\n    return -1\n\nedges = [[0, 1], [0, 2], [1, 3], [2, 3], [3, 4]]\nprint('Shortest path 0 -> 4:', shortest_path(5, edges, 0, 4))\n",
            "solutionCode": "from collections import deque\n\ndef shortest_path(n: int, edges: list[list[int]], start: int, target: int) -> int:\n    adj = {i: [] for i in range(n)}\n    for u, v in edges:\n        adj[u].append(v)\n        adj[v].append(u)\n    \n    q = deque([(start, 0)])\n    visited = {start}\n    while q:\n        curr, d = q.popleft()\n        if curr == target:\n            return d\n        for nxt in adj[curr]:\n            if nxt not in visited:\n                visited.add(nxt)\n                q.append((nxt, d + 1))\n    return -1\n\nedges = [[0, 1], [0, 2], [1, 3], [2, 3], [3, 4]]\nprint('Shortest path 0 -> 4:', shortest_path(5, edges, 0, 4))\n",
            "expectedOutputPatterns": [
                "Shortest path 0 -> 4: 3"
            ],
            "hint": "Build adj list. q = deque([(start, 0)]), visited = {start}. While q: curr, d = popleft. If curr == target: return d. For nxt in adj[curr]: if nxt not in visited: visited.add(nxt), q.append((nxt, d + 1)). Return -1."
        },
        "keyTakeaway": "Successfully implemented and verified Breadth-First Search!"
    },
    {
        "id": "day122-step5",
        "stepNumber": 5,
        "title": "Day 122 Complete: BFS & Unweighted Shortest Path",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 122,
        "heading": "Mastery Achieved: BFS & Unweighted Shortest Path",
        "subheading": "You have solidified key mental models and techniques for Breadth-First Search.",
        "recapRows": [
            {
                "concept": "Immediate Visited Registration",
                "naiveIntuition": "Mark node visited when popping from queue",
                "pythonReality": "Marking visited immediately at enqueue time prevents duplicate node insertions and preserves linear O(V + E) bounds"
            },
            {
                "concept": "Concentric Frontier Expansion",
                "naiveIntuition": "DFS can also find shortest paths",
                "pythonReality": "DFS wanders down arbitrary deep paths first, requiring exhaustive O(V!) search; BFS finds shortest paths directly in O(V + E)"
            }
        ],
        "solidifiedConcepts": [
            "FIFO Queue Level Expansion",
            "Predecessor Array & Distance Tracking"
        ],
        "nextDayPreview": {
            "dayNumber": 123,
            "title": "DFS, Connected Components & Flood Fill",
            "description": "Implement recursive and iterative DFS, count connected components, and solve 2D grid flood fill problems."
        }
    }
]
},
  123: {
  "dayNumber": 123,
  "title": "DFS, Connected Components & Flood Fill",
  "topicName": "Depth-First Search",
  "sectionId": "graphs",
  "estimatedMinutes": 35,
  "difficulty": "ADVANCED",
  "prerequisites": [
    30,
    121
  ],
  "concepts": [
    "Recursive DFS Traversal",
    "Visited Set & Grid Flood Fill"
  ],
  "practiceSkills": [
    "Depth-First Search Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Traverse all reachable graph vertices using Depth-First Search with a visited set",
    "Count connected components and solve 2D grid flood fill problems in O(V + E) time"
  ],
  "practiceArchetype": "algorithm",
  "flowTier": "tier2"
,
  "steps": [
    {
        "id": "day123-step1",
        "stepNumber": 1,
        "title": "DFS, Connected Components & Flood Fill: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Depth-First Search",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Depth-First Search.",
        "markdownContent": [
            "Depth-First Search (DFS) explores branches deeply before backtracking, identifying Connected Components and detecting Cycles via three-color node state tracking.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Depth-First Search**, remember the central principle: Encountering an active ancestor (visiting state) on the recursion stack proves a directed cycle."
        ],
        "snippets": [
            {
                "title": "Depth-First Search Implementation Template",
                "code": "# Directed Cycle Detection via 3-State DFS\ndef has_cycle(n, adj):\n    state = [0] * n # 0: unvisited, 1: visiting, 2: visited\n    def dfs(u):\n        state[u] = 1 # Mark visiting\n        for v in adj[u]:\n            if state[v] == 1: return True # Back-edge found!\n            if state[v] == 0 and dfs(v): return True\n        state[u] = 2 # Mark visited\n        return False\n    return any(state[i] == 0 and dfs(i) for i in range(n))",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Encountering an active ancestor (visiting state) on the recursion stack proves a directed cycle."
    },
    {
        "id": "day123-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Depth-First Search",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Three-color state machine: 0 = Unvisited (White), 1 = Visiting (Gray, active on recursion stack), 2 = Visited (Black, fully explored). In directed graphs, encountering a neighbor with state 1 indicates a Back-Edge, proving the presence of a cycle in O(V + E) time.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Encountering an active ancestor (visiting state) on the recursion stack proves a directed cycle.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Depth-First Search Core Invariant",
                "content": "Encountering an active ancestor (visiting state) on the recursion stack proves a directed cycle."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Encountering an active ancestor (visiting state) on the recursion stack proves a directed cycle."
    },
    {
        "id": "day123-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Depth-First Search",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d123-q1",
                "question": "Why is a simple boolean `visited` set insufficient to detect cycles in a DIRECTED graph?",
                "options": [
                    {
                        "id": "A",
                        "label": "A node might be visited from two separate converging paths (Cross-Edge) without forming a cycle; only reaching an active ancestor on the CURRENT recursion path constitutes a cycle"
                    },
                    {
                        "id": "B",
                        "label": "Because boolean sets cannot store negative numbers"
                    },
                    {
                        "id": "C",
                        "label": "Because directed graphs cannot have cycles"
                    },
                    {
                        "id": "D",
                        "label": "Because sets do not support lookup in O(1)"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! In DAGs like diamond paths (0 -> 1 -> 3 and 0 -> 2 -> 3), node 3 is visited twice via cross paths, but no cycle exists. A cycle exists only when an edge points back to an active ancestor currently in state 'visiting'.",
                    "B": "Incorrect: Node IDs are non-negative indices.",
                    "C": "Incorrect: Directed graphs frequently contain cycles.",
                    "D": "Incorrect: Sets have O(1) average lookup."
                }
            },
            {
                "id": "chk-d123-q2",
                "question": "In an UNDIRECTED graph, how is a cycle distinguished from the trivial backtracking edge to the parent node?",
                "options": [
                    {
                        "id": "A",
                        "label": "By passing `parent` into the DFS call and ignoring the edge `if neighbor == parent`"
                    },
                    {
                        "id": "B",
                        "label": "By deleting the parent node"
                    },
                    {
                        "id": "C",
                        "label": "Undirected graphs cannot have cycles"
                    },
                    {
                        "id": "D",
                        "label": "By sorting edges by weight"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! In an undirected graph, edge (u, v) allows walking u -> v and immediately v -> u. Passing `parent` prevents mistaking this reciprocal edge for a cycle; reaching any other already-visited node proves a true cycle.",
                    "B": "Incorrect: Never mutate graph topology during traversal.",
                    "C": "Incorrect: Undirected graphs can have cycles.",
                    "D": "Incorrect: Traversal order does not eliminate the parent check."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day123-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Depth-First Search",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Detect if a directed graph contains a cycle using 3-color DFS.",
        "subheading": "Implement and verify Depth-First Search in the interactive workspace.",
        "task": {
            "title": "Detect if a directed graph contains a cycle using 3-color DFS.",
            "instructions": [
                "Detect if a directed graph contains a cycle using 3-color DFS.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "def has_cycle_directed(n: int, edges: list[list[int]]) -> bool:\n    # TODO: Implement 3-state DFS cycle detection\n    return False\n\n# Graph 1: 0 -> 1 -> 2 -> 0 (Cycle!)\ne1 = [[0, 1], [1, 2], [2, 0]]\n# Graph 2: 0 -> 1 -> 2 (No cycle)\ne2 = [[0, 1], [1, 2]]\nprint('G1 Has Cycle:', has_cycle_directed(3, e1))\nprint('G2 Has Cycle:', has_cycle_directed(3, e2))\n",
            "solutionCode": "def has_cycle_directed(n: int, edges: list[list[int]]) -> bool:\n    adj = {i: [] for i in range(n)}\n    for u, v in edges:\n        adj[u].append(v)\n    \n    state = [0] * n\n    def dfs(u):\n        state[u] = 1\n        for v in adj[u]:\n            if state[v] == 1:\n                return True\n            if state[v] == 0 and dfs(v):\n                return True\n        state[u] = 2\n        return False\n\n    for i in range(n):\n        if state[i] == 0:\n            if dfs(i):\n                return True\n    return False\n\ne1 = [[0, 1], [1, 2], [2, 0]]\ne2 = [[0, 1], [1, 2]]\nprint('G1 Has Cycle:', has_cycle_directed(3, e1))\nprint('G2 Has Cycle:', has_cycle_directed(3, e2))\n",
            "expectedOutputPatterns": [
                "G1 Has Cycle: True",
                "G2 Has Cycle: False"
            ],
            "hint": "Build adj. state = [0] * n. Helper dfs(u): state[u] = 1; loop v in adj[u]: if state[v] == 1 return True; if state[v] == 0 and dfs(v) return True; state[u] = 2; return False. Check all unvisited nodes in range(n)."
        },
        "keyTakeaway": "Successfully implemented and verified Depth-First Search!"
    },
    {
        "id": "day123-step5",
        "stepNumber": 5,
        "title": "Day 123 Complete: DFS, Connected Components & Flood Fill",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 123,
        "heading": "Mastery Achieved: DFS, Connected Components & Flood Fill",
        "subheading": "You have solidified key mental models and techniques for Depth-First Search.",
        "recapRows": [
            {
                "concept": "Three-State Disambiguation",
                "naiveIntuition": "Visited nodes cannot be visited again",
                "pythonReality": "Distinguishing 'visiting' (active ancestor on current path) from 'visited' (fully closed branch) separates genuine cycles from cross-edges"
            },
            {
                "concept": "Disconnected Forest Sweeping",
                "naiveIntuition": "Running DFS once from node 0 explores the whole graph",
                "pythonReality": "A graph may have multiple disconnected components; an outer loop over all nodes ensures 100% coverage"
            }
        ],
        "solidifiedConcepts": [
            "Recursive DFS Traversal",
            "Visited Set & Grid Flood Fill"
        ],
        "nextDayPreview": {
            "dayNumber": 124,
            "title": "Cycle Detection in Directed Graphs (3-Color)",
            "description": "Detect cycles in directed graphs using three-color DFS marking (Unvisited, Visiting, Visited) and back-edge identification."
        }
    }
]
},
  124: {
  "dayNumber": 124,
  "title": "Cycle Detection in Directed Graphs (3-Color)",
  "topicName": "Cycle Detection",
  "sectionId": "graphs",
  "estimatedMinutes": 35,
  "difficulty": "ADVANCED",
  "prerequisites": [
    123
  ],
  "concepts": [
    "Three-Color State Marking (White, Gray, Black)",
    "Back-Edge Detection"
  ],
  "practiceSkills": [
    "Cycle Detection Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Detect cycles in directed graphs by identifying back-edges to gray nodes on the current recursion stack",
    "Differentiate directed cycle detection from undirected visited-set checks"
  ],
  "practiceArchetype": "debugging",
  "flowTier": "tier2"
,
  "steps": [
    {
        "id": "day124-step1",
        "stepNumber": 1,
        "title": "Cycle Detection in Directed Graphs (3-Color): Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Cycle Detection",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Cycle Detection.",
        "markdownContent": [
            "Cycle Detection in Directed Graphs uses DFS 3-Coloring (White, Gray, Black) to detect back-edges to active ancestors currently on the recursion call stack in O(V + E) time.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Cycle Detection**, remember the central principle: A directed cycle exists if and only if DFS encounters a back-edge to a GRAY ancestor currently on the call stack."
        ],
        "snippets": [
            {
                "title": "Cycle Detection Implementation Template",
                "code": "# 3-Color Cycle Detection in Directed Graph\ndef has_cycle(n, adj):\n    visited = [0] * n  # 0=White, 1=Gray, 2=Black\n    def dfs(u):\n        visited[u] = 1 # Mark Gray\n        for v in adj[u]:\n            if visited[v] == 1: return True  # Cycle detected!\n            if visited[v] == 0 and dfs(v): return True\n        visited[u] = 2 # Mark Black\n        return False\n    return any(visited[i] == 0 and dfs(i) for i in range(n))",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "A directed cycle exists if and only if DFS encounters a back-edge to a GRAY ancestor currently on the call stack."
    },
    {
        "id": "day124-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Cycle Detection",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Every vertex has one of three states: 0=WHITE (unvisited), 1=GRAY (currently being explored on call stack), 2=BLACK (completely processed and backtrack completed). During DFS from vertex u, if we encounter an adjacent vertex v that is GRAY (visited[v] == 1), an active back-edge exists, confirming a directed cycle.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: A directed cycle exists if and only if DFS encounters a back-edge to a GRAY ancestor currently on the call stack.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Cycle Detection Core Invariant",
                "content": "A directed cycle exists if and only if DFS encounters a back-edge to a GRAY ancestor currently on the call stack."
            }
        ],
        "keyTakeaway": "Operational invariant locked: A directed cycle exists if and only if DFS encounters a back-edge to a GRAY ancestor currently on the call stack."
    },
    {
        "id": "day124-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Cycle Detection",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d124-q1",
                "question": "Why is a simple 2-state boolean visited array (True/False) INSUFFICIENT for cycle detection in DIRECTED graphs?",
                "options": [
                    {
                        "id": "A",
                        "label": "A True entry could be a cross-edge or forward-edge to a previously finished node that does not form a cycle; only edges to active ancestors on the current call stack form cycles"
                    },
                    {
                        "id": "B",
                        "label": "Because directed graphs cannot be traversed with DFS"
                    },
                    {
                        "id": "C",
                        "label": "Because booleans take more memory than integers"
                    },
                    {
                        "id": "D",
                        "label": "Because directed graphs always have cycles"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! In directed graphs, reaching an already-visited vertex via a cross-edge (e.g. 1 -> 2 and 1 -> 3 -> 2) is completely acyclic. Cycles occur ONLY when an edge points back to an active ancestor currently in state GRAY.",
                    "B": "Incorrect: DFS is the canonical algorithm for directed graphs.",
                    "C": "Incorrect: Memory representation is irrelevant to cycle geometry.",
                    "D": "Incorrect: Directed Acyclic Graphs (DAGs) have zero cycles."
                }
            },
            {
                "id": "chk-d124-q2",
                "question": "What does state BLACK (visited[u] == 2) signify in the 3-coloring algorithm?",
                "options": [
                    {
                        "id": "A",
                        "label": "All descendants reachable from vertex u have been fully explored with zero cycles found, so u can be safely pruned from future inspection"
                    },
                    {
                        "id": "B",
                        "label": "A cycle has been found at vertex u"
                    },
                    {
                        "id": "C",
                        "label": "Vertex u has no outgoing edges"
                    },
                    {
                        "id": "D",
                        "label": "Vertex u is the root of the graph"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Once all neighbors of u are verified acyclic, u transitions from Gray to Black. Any subsequent edge encountering a Black vertex can safely prune that branch immediately.",
                    "B": "Incorrect: Gray-to-Gray transitions detect cycles.",
                    "C": "Incorrect: Nodes with out-degree > 0 transition to Black after exploration.",
                    "D": "Incorrect: Any node transitions to Black when its subtree completes."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day124-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Cycle Detection",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Detect whether a directed course prerequisite graph contains a cycle (Deadlock Detection).",
        "subheading": "Implement and verify Cycle Detection in the interactive workspace.",
        "task": {
            "title": "Detect whether a directed course prerequisite graph contains a cycle (Deadlock Detection).",
            "instructions": [
                "Detect whether a directed course prerequisite graph contains a cycle (Deadlock Detection).",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "def can_finish_courses(num_courses: int, prerequisites: list[list[int]]) -> bool:\n    adj = {i: [] for i in range(num_courses)}\n    for crs, pre in prerequisites:\n        adj[pre].append(crs)\n    visited = [0] * num_courses  # 0=White, 1=Gray, 2=Black\n    # TODO: Implement 3-color DFS to return True if no cycles, False if cycle exists\n    return True\n\nprint('Can finish [0->1, 1->0]:', can_finish_courses(2, [[1, 0], [0, 1]])) # False\nprint('Can finish [0->1, 1->2]:', can_finish_courses(3, [[1, 0], [2, 1]])) # True\n",
            "solutionCode": "def can_finish_courses(num_courses: int, prerequisites: list[list[int]]) -> bool:\n    adj = {i: [] for i in range(num_courses)}\n    for crs, pre in prerequisites:\n        adj[pre].append(crs)\n    visited = [0] * num_courses\n    def dfs(u):\n        visited[u] = 1\n        for v in adj[u]:\n            if visited[v] == 1:\n                return False\n            if visited[v] == 0 and not dfs(v):\n                return False\n        visited[u] = 2\n        return True\n    for i in range(num_courses):\n        if visited[i] == 0:\n            if not dfs(i):\n                return False\n    return True\n\nprint('Can finish [0->1, 1->0]:', can_finish_courses(2, [[1, 0], [0, 1]]))\nprint('Can finish [0->1, 1->2]:', can_finish_courses(3, [[1, 0], [2, 1]]))\n",
            "expectedOutputPatterns": [
                "Can finish [0->1, 1->0]: False",
                "Can finish [0->1, 1->2]: True"
            ],
            "hint": "In dfs(u): mark visited[u] = 1. For v in adj[u]: if visited[v] == 1 return False; if visited[v] == 0 and not dfs(v) return False. visited[u] = 2. Return True. Check all courses i in range(n)."
        },
        "keyTakeaway": "Successfully implemented and verified Cycle Detection!"
    },
    {
        "id": "day124-step5",
        "stepNumber": 5,
        "title": "Day 124 Complete: Cycle Detection in Directed Graphs (3-Color)",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 124,
        "heading": "Mastery Achieved: Cycle Detection in Directed Graphs (3-Color)",
        "subheading": "You have solidified key mental models and techniques for Cycle Detection.",
        "recapRows": [
            {
                "concept": "Recursion Stack Invariant",
                "naiveIntuition": "Any visited node means a cycle",
                "pythonReality": "Only nodes currently in the recursion stack (Gray) indicate cycles; already completed nodes (Black) are safe cross-edges"
            },
            {
                "concept": "Topological Equivalency",
                "naiveIntuition": "Cycle detection is unrelated to topo sort",
                "pythonReality": "A directed graph has a cycle if and only if a valid topological ordering does NOT exist"
            }
        ],
        "solidifiedConcepts": [
            "Three-Color State Marking (White, Gray, Black)",
            "Back-Edge Detection"
        ],
        "nextDayPreview": {
            "dayNumber": 125,
            "title": "Topological Sort: Kahn's In-Degree BFS",
            "description": "Implement Kahn's algorithm for topological sorting of DAGs using in-degree arrays and zero-degree queues."
        }
    }
]
},
  125: {
  "dayNumber": 125,
  "title": "Topological Sort: Kahn's In-Degree BFS",
  "topicName": "Topological Sort BFS",
  "sectionId": "graphs",
  "estimatedMinutes": 40,
  "difficulty": "ADVANCED",
  "prerequisites": [
    122,
    124
  ],
  "concepts": [
    "In-Degree Array Construction",
    "Zero-In-Degree FIFO Queue"
  ],
  "practiceSkills": [
    "Topological Sort BFS Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Compute vertex in-degrees and process zero-in-degree nodes sequentially",
    "Produce a valid topological order of a DAG or detect cyclic dependency errors in O(V + E) time"
  ],
  "practiceArchetype": "algorithm",
  "flowTier": "tier2"
,
  "steps": [
    {
        "id": "day125-step1",
        "stepNumber": 1,
        "title": "Topological Sort: Kahn's In-Degree BFS: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Topological Sort BFS",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Topological Sort BFS.",
        "markdownContent": [
            "Topological Sort linearly orders vertices in a Directed Acyclic Graph (DAG) such that for every directed edge u -> v, u appears before v. Kahn's Algorithm resolves dependencies via in-degree tracking and a FIFO queue.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Topological Sort BFS**, remember the central principle: Kahn's algorithm orders DAG dependencies in O(V + E) time while naturally detecting cycles if output length < V."
        ],
        "snippets": [
            {
                "title": "Topological Sort BFS Implementation Template",
                "code": "# Kahn's Topological Sort\nfrom collections import deque\ndef topological_sort_kahn(n, adj):\n    in_degree = [0] * n\n    for u in range(n):\n        for v in adj[u]: in_degree[v] += 1\n    q = deque([i for i in range(n) if in_degree[i] == 0])\n    order = []\n    while q:\n        u = q.popleft()\n        order.append(u)\n        for v in adj[u]:\n            in_degree[v] -= 1\n            if in_degree[v] == 0: q.append(v)\n    return order if len(order) == n else [] # Empty if cycle",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Kahn's algorithm orders DAG dependencies in O(V + E) time while naturally detecting cycles if output length < V."
    },
    {
        "id": "day125-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Topological Sort BFS",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Calculate `in_degree` for all vertices. Enqueue all vertices with `in_degree == 0`. While queue is non-empty: pop `u`, append to result list. For each neighbor `v` of `u`: decrement `in_degree[v]`. If `in_degree[v] == 0`: enqueue `v`. If result length < V, the graph contains a cycle.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Kahn's algorithm orders DAG dependencies in O(V + E) time while naturally detecting cycles if output length < V.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Topological Sort BFS Core Invariant",
                "content": "Kahn's algorithm orders DAG dependencies in O(V + E) time while naturally detecting cycles if output length < V."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Kahn's algorithm orders DAG dependencies in O(V + E) time while naturally detecting cycles if output length < V."
    },
    {
        "id": "day125-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Topological Sort BFS",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d125-q1",
                "question": "Why does a final `len(order) < n` prove that the directed graph contains a cycle in Kahn's algorithm?",
                "options": [
                    {
                        "id": "A",
                        "label": "Vertices inside a directed cycle always retain an in-degree >= 1 from each other, so none of them can ever reach in-degree 0 and enter the queue"
                    },
                    {
                        "id": "B",
                        "label": "Because the queue ran out of memory"
                    },
                    {
                        "id": "C",
                        "label": "Because topological sort only works for graphs with even number of vertices"
                    },
                    {
                        "id": "D",
                        "label": "Because in-degree became negative"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Every node in a cycle has at least one predecessor inside the cycle. Since no cycle member can have its in-degree reduced to 0, all cycle nodes are permanently locked out of the queue.",
                    "B": "Incorrect: Deque handles memory dynamically.",
                    "C": "Incorrect: Works for any number of vertices.",
                    "D": "Incorrect: In-degrees are decremented to 0, never negative."
                }
            },
            {
                "id": "chk-d125-q2",
                "question": "What does an in-degree of 0 mean for a task in a dependency graph?",
                "options": [
                    {
                        "id": "A",
                        "label": "The task has zero unmet prerequisites and is ready to be executed immediately"
                    },
                    {
                        "id": "B",
                        "label": "The task cannot be executed"
                    },
                    {
                        "id": "C",
                        "label": "The task has already completed"
                    },
                    {
                        "id": "D",
                        "label": "The task has no outgoing edges"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! In a build system or prerequisite chain, incoming edges represent dependencies. In-degree 0 means no remaining dependencies, making the task immediately runnable.",
                    "B": "Incorrect: It is ready to run.",
                    "C": "Incorrect: It is ready to begin, not already done.",
                    "D": "Incorrect: In-degree measures incoming edges, not outgoing."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day125-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Topological Sort BFS",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Perform topological sort on course prerequisites to determine a valid course completion order.",
        "subheading": "Implement and verify Topological Sort BFS in the interactive workspace.",
        "task": {
            "title": "Perform topological sort on course prerequisites to determine a valid course completion order.",
            "instructions": [
                "Perform topological sort on course prerequisites to determine a valid course completion order.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "from collections import deque\n\ndef course_order(num_courses: int, prerequisites: list[list[int]]) -> list[int]:\n    # TODO: Implement Kahn's algorithm for Course Schedule II\n    # prerequisites[i] = [course, prereq] (prereq -> course)\n    return []\n\n# 4 courses: 0, 1, 2, 3. Prereqs: 1->0, 2->0, 3->1, 3->2\nprereqs = [[1, 0], [2, 0], [3, 1], [3, 2]]\nprint('Course order:', course_order(4, prereqs))\n",
            "solutionCode": "from collections import deque\n\ndef course_order(num_courses: int, prerequisites: list[list[int]]) -> list[int]:\n    adj = {i: [] for i in range(num_courses)}\n    in_deg = [0] * num_courses\n    for crs, pre in prerequisites:\n        adj[pre].append(crs)\n        in_deg[crs] += 1\n    \n    q = deque([i for i in range(num_courses) if in_deg[i] == 0])\n    res = []\n    while q:\n        u = q.popleft()\n        res.append(u)\n        for v in adj[u]:\n            in_deg[v] -= 1\n            if in_deg[v] == 0:\n                q.append(v)\n    return res if len(res) == num_courses else []\n\nprereqs = [[1, 0], [2, 0], [3, 1], [3, 2]]\nprint('Course order:', course_order(4, prereqs))\n",
            "expectedOutputPatterns": [
                "Course order: [0, 1, 2, 3]"
            ],
            "hint": "Build adj and in_deg arrays: for crs, pre: adj[pre].append(crs); in_deg[crs] += 1. q = deque(nodes with in_deg == 0). While q: pop, append to res, decrement neighbors, enqueue if in_deg == 0. Return res if len(res) == num_courses else []."
        },
        "keyTakeaway": "Successfully implemented and verified Topological Sort BFS!"
    },
    {
        "id": "day125-step5",
        "stepNumber": 5,
        "title": "Day 125 Complete: Topological Sort: Kahn's In-Degree BFS",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 125,
        "heading": "Mastery Achieved: Topological Sort: Kahn's In-Degree BFS",
        "subheading": "You have solidified key mental models and techniques for Topological Sort BFS.",
        "recapRows": [
            {
                "concept": "Prerequisite Resolution Flow",
                "naiveIntuition": "Sort courses by course number",
                "pythonReality": "Topological order reflects dependency satisfaction; in-degree tracking guarantees no task runs before its prerequisites complete"
            },
            {
                "concept": "Dual Utility of Kahn's",
                "naiveIntuition": "Cycle detection and topological ordering require separate passes",
                "pythonReality": "Kahn's algorithm accomplishes both simultaneously: valid DAGs yield the full topological sequence, while cycles result in truncated outputs"
            }
        ],
        "solidifiedConcepts": [
            "In-Degree Array Construction",
            "Zero-In-Degree FIFO Queue"
        ],
        "nextDayPreview": {
            "dayNumber": 126,
            "title": "Topological Sort: DFS Post-Order Reversal",
            "description": "Implement topological sort using DFS post-order traversal reversal and detect invalid cyclic dependencies."
        }
    }
]
},
  126: {
  "dayNumber": 126,
  "title": "Topological Sort: DFS Post-Order Reversal",
  "topicName": "Topological Sort DFS",
  "sectionId": "graphs",
  "estimatedMinutes": 35,
  "difficulty": "ADVANCED",
  "prerequisites": [
    123,
    125
  ],
  "concepts": [
    "DFS Finishing Time Post-Order",
    "Reversed Post-Order Sequence"
  ],
  "practiceSkills": [
    "Topological Sort DFS Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Record DFS finish order and reverse the post-order sequence to produce a topological sort",
    "Solve Course Schedule II under prerequisite constraints"
  ],
  "practiceArchetype": "problem",
  "flowTier": "tier2"
,
  "steps": [
    {
        "id": "day126-step1",
        "stepNumber": 1,
        "title": "Topological Sort: DFS Post-Order Reversal: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Topological Sort DFS",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Topological Sort DFS.",
        "markdownContent": [
            "Topological Sort via DFS Post-Order Reversal sorts DAGs by recording vertices upon post-order completion and reversing the resulting list.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Topological Sort DFS**, remember the central principle: Reversing DFS post-order finishing times produces a valid topological sequence for any DAG."
        ],
        "snippets": [
            {
                "title": "Topological Sort DFS Implementation Template",
                "code": "# DFS Topological Sort\ndef topo_dfs(n, adj):\n    state = [0] * n # 0: unvisited, 1: visiting, 2: visited\n    res = []\n    def dfs(u):\n        state[u] = 1\n        for v in adj[u]:\n            if state[v] == 1: return False\n            if state[v] == 0 and not dfs(v): return False\n        state[u] = 2\n        res.append(u) # Post-order finish\n        return True\n    for i in range(n):\n        if state[i] == 0 and not dfs(i): return []\n    return res[::-1] # Reverse post-order",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Reversing DFS post-order finishing times produces a valid topological sequence for any DAG."
    },
    {
        "id": "day126-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Topological Sort DFS",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "For each unvisited node: run DFS. In post-order (after all descendants have finished exploring), append `node` to stack. If a node encounters a neighbor in state 'visiting', a cycle exists. Reversing the post-order stack yields the exact topological order in O(V + E) time.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Reversing DFS post-order finishing times produces a valid topological sequence for any DAG.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Topological Sort DFS Core Invariant",
                "content": "Reversing DFS post-order finishing times produces a valid topological sequence for any DAG."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Reversing DFS post-order finishing times produces a valid topological sequence for any DAG."
    },
    {
        "id": "day126-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Topological Sort DFS",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d126-q1",
                "question": "Why must the post-order result list be reversed to obtain a valid topological sort?",
                "options": [
                    {
                        "id": "A",
                        "label": "A node only finishes its post-order DFS after all its downstream dependencies have completely finished, meaning terminal nodes finish first and must be placed at the end"
                    },
                    {
                        "id": "B",
                        "label": "Because Python lists can only be appended to the right"
                    },
                    {
                        "id": "C",
                        "label": "Because DFS starts from the largest node index"
                    },
                    {
                        "id": "D",
                        "label": "To fix a sorting bug"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! If u -> v, v must complete before u can finish. Thus, v is appended to post-order before u. Reversing the list puts u before v, restoring the correct dependency order.",
                    "B": "Incorrect: Lists can insert at index 0 (though O(N)).",
                    "C": "Incorrect: Starting order does not change finishing relations.",
                    "D": "Incorrect: Reversal is a mathematical requirement of post-order finishing."
                }
            },
            {
                "id": "chk-d126-q2",
                "question": "What is the time and space complexity of DFS Topological Sort on a graph with V vertices and E edges?",
                "options": [
                    {
                        "id": "A",
                        "label": "O(V + E) time and O(V) auxiliary space"
                    },
                    {
                        "id": "B",
                        "label": "O(V * E) time and O(1) space"
                    },
                    {
                        "id": "C",
                        "label": "O(V^2) time and O(E) space"
                    },
                    {
                        "id": "D",
                        "label": "O(log V) time and O(V) space"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Every vertex and edge is traversed once in O(V + E) time. Auxiliary storage includes the state array, call stack, and result list, totaling O(V).",
                    "B": "Incorrect: DFS avoids quadratic scanning.",
                    "C": "Incorrect: Adjacency list is O(V + E).",
                    "D": "Incorrect: All nodes must be visited."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day126-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Topological Sort DFS",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Implement DFS post-order topological sort.",
        "subheading": "Implement and verify Topological Sort DFS in the interactive workspace.",
        "task": {
            "title": "Implement DFS post-order topological sort.",
            "instructions": [
                "Implement DFS post-order topological sort.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "def topo_sort_dfs(n: int, edges: list[list[int]]) -> list[int]:\n    # TODO: Implement DFS topological sort with cycle detection\n    return []\n\n# 0 -> 1, 0 -> 2, 1 -> 3, 2 -> 3\nedges = [[0, 1], [0, 2], [1, 3], [2, 3]]\nprint('DFS Topo Sort:', topo_sort_dfs(4, edges))\n",
            "solutionCode": "def topo_sort_dfs(n: int, edges: list[list[int]]) -> list[int]:\n    adj = {i: [] for i in range(n)}\n    for u, v in edges:\n        adj[u].append(v)\n    \n    state = [0] * n\n    post_order = []\n    def dfs(u):\n        state[u] = 1\n        for v in adj[u]:\n            if state[v] == 1:\n                return False\n            if state[v] == 0 and not dfs(v):\n                return False\n        state[u] = 2\n        post_order.append(u)\n        return True\n\n    for i in range(n):\n        if state[i] == 0:\n            if not dfs(i):\n                return []\n    return post_order[::-1]\n\nedges = [[0, 1], [0, 2], [1, 3], [2, 3]]\nprint('DFS Topo Sort:', topo_sort_dfs(4, edges))\n",
            "expectedOutputPatterns": [
                "DFS Topo Sort: [0, 2, 1, 3]"
            ],
            "hint": "State 0: unvisited, 1: visiting, 2: visited. In dfs(u): state[u] = 1; loop neighbors: if state == 1 return False; if state == 0 and not dfs(v) return False. state[u] = 2; post_order.append(u); return True. Loop all nodes, return post_order[::-1]."
        },
        "keyTakeaway": "Successfully implemented and verified Topological Sort DFS!"
    },
    {
        "id": "day126-step5",
        "stepNumber": 5,
        "title": "Day 126 Complete: Topological Sort: DFS Post-Order Reversal",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 126,
        "heading": "Mastery Achieved: Topological Sort: DFS Post-Order Reversal",
        "subheading": "You have solidified key mental models and techniques for Topological Sort DFS.",
        "recapRows": [
            {
                "concept": "Finishing Time Duality",
                "naiveIntuition": "Discovery time determines dependency order",
                "pythonReality": "Discovery time depends on arbitrary branch selection; finishing time strictly mirrors leaf-to-root completion"
            },
            {
                "concept": "DFS vs BFS Equivalence",
                "naiveIntuition": "Kahn's and DFS produce different dependencies",
                "pythonReality": "Both generate valid topological orderings (though ties may resolve differently), operating in O(V + E) time"
            }
        ],
        "solidifiedConcepts": [
            "DFS Finishing Time Post-Order",
            "Reversed Post-Order Sequence"
        ],
        "nextDayPreview": {
            "dayNumber": 127,
            "title": "Bipartite Graph Verification (2-Coloring)",
            "description": "Determine whether a graph is bipartite (2-colorable) using alternating BFS/DFS vertex coloring in O(V + E) time."
        }
    }
]
},
  127: {
  "dayNumber": 127,
  "title": "Bipartite Graph Verification (2-Coloring)",
  "topicName": "Bipartite Verification",
  "sectionId": "graphs",
  "estimatedMinutes": 30,
  "difficulty": "ADVANCED",
  "prerequisites": [
    122
  ],
  "concepts": [
    "Vertex 2-Coloring Invariant",
    "Odd-Length Cycle Non-Bipartite Rule"
  ],
  "practiceSkills": [
    "Bipartite Verification Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Color graph vertices with two alternating labels using BFS/DFS",
    "Prove a graph is non-bipartite if adjacent vertices share identical color labels"
  ],
  "practiceArchetype": "problem",
  "flowTier": "tier1"
,
  "steps": [
    {
        "id": "day127-step1",
        "stepNumber": 1,
        "title": "Bipartite Graph Verification (2-Coloring): Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Bipartite Verification",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Bipartite Verification.",
        "markdownContent": [
            "Bipartite Graph Verification determines if graph vertices can be partitioned into two independent sets such that no two adjacent vertices share the same color (2-Coloring via BFS/DFS).",
            "### Foundational Mental Model\nWhen approaching problems requiring **Bipartite Verification**, remember the central principle: A graph is bipartite if and only if it is 2-colorable (contains zero odd-length cycles)."
        ],
        "snippets": [
            {
                "title": "Bipartite Verification Implementation Template",
                "code": "# 2-Coloring Bipartite check\ndef is_bipartite(n, adj):\n    color = [-1] * n\n    for i in range(n):\n        if color[i] != -1: continue\n        color[i] = 0\n        q = deque([i])\n        while q:\n            u = q.popleft()\n            for v in adj[u]:\n                if color[v] == -1:\n                    color[v] = 1 - color[u]\n                    q.append(v)\n                elif color[v] == color[u]:\n                    return False # Conflict!\n    return True",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "A graph is bipartite if and only if it is 2-colorable (contains zero odd-length cycles)."
    },
    {
        "id": "day127-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Bipartite Verification",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Graph is bipartite if and only if it contains NO odd-length cycles. Traversal: assign `color[start] = 1`. For each neighbor `v`: if uncolored, assign `color[v] = 1 - color[u]` and recurse/enqueue. If `v` is already colored and `color[v] == color[u]`, a color conflict is detected: return False.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: A graph is bipartite if and only if it is 2-colorable (contains zero odd-length cycles).\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Bipartite Verification Core Invariant",
                "content": "A graph is bipartite if and only if it is 2-colorable (contains zero odd-length cycles)."
            }
        ],
        "keyTakeaway": "Operational invariant locked: A graph is bipartite if and only if it is 2-colorable (contains zero odd-length cycles)."
    },
    {
        "id": "day127-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Bipartite Verification",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d127-q1",
                "question": "What fundamental topological property makes a graph non-bipartite?",
                "options": [
                    {
                        "id": "A",
                        "label": "The presence of at least one cycle with an ODD number of vertices/edges"
                    },
                    {
                        "id": "B",
                        "label": "The presence of an even cycle"
                    },
                    {
                        "id": "C",
                        "label": "Having an odd number of total vertices in the graph"
                    },
                    {
                        "id": "D",
                        "label": "Having negative edge weights"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! In an odd cycle (e.g. triangle of 3 nodes), alternating colors 0-1-0 forces the 3rd node to connect back to node 1 with the same color 0, causing an inevitable conflict.",
                    "B": "Incorrect: Even cycles (like 4-node squares) alternate colors 0-1-0-1 perfectly.",
                    "C": "Incorrect: Total vertices can be odd as long as cycles are even.",
                    "D": "Incorrect: Bipartition is an unweighted structural property."
                }
            },
            {
                "id": "chk-d127-q2",
                "question": "Why must the outer loop iterate through all vertices from 0 to N - 1?",
                "options": [
                    {
                        "id": "A",
                        "label": "The graph might contain multiple disconnected components, each requiring independent 2-coloring validation"
                    },
                    {
                        "id": "B",
                        "label": "To sort the vertices"
                    },
                    {
                        "id": "C",
                        "label": "Because colors are 0-indexed"
                    },
                    {
                        "id": "D",
                        "label": "To reset CPU registers"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! If a graph consists of two separate components, checking only component 1 leaves component 2 uninspected. Component 2 might harbor an odd cycle.",
                    "B": "Incorrect: No sorting is performed.",
                    "C": "Incorrect: Coloring values are binary states.",
                    "D": "Incorrect: Algorithmic component traversal."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day127-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Bipartite Verification",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Determine whether an undirected graph is bipartite.",
        "subheading": "Implement and verify Bipartite Verification in the interactive workspace.",
        "task": {
            "title": "Determine whether an undirected graph is bipartite.",
            "instructions": [
                "Determine whether an undirected graph is bipartite.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "from collections import deque\n\ndef is_graph_bipartite(n: int, edges: list[list[int]]) -> bool:\n    # TODO: Implement 2-coloring BFS to verify bipartiteness\n    return True\n\n# Triangle graph (odd cycle): 0-1, 1-2, 2-0 -> False\ne_triangle = [[0, 1], [1, 2], [2, 0]]\n# Square graph (even cycle): 0-1, 1-2, 2-3, 3-0 -> True\ne_square = [[0, 1], [1, 2], [2, 3], [3, 0]]\nprint('Triangle Bipartite:', is_graph_bipartite(3, e_triangle))\nprint('Square Bipartite:', is_graph_bipartite(4, e_square))\n",
            "solutionCode": "from collections import deque\n\ndef is_graph_bipartite(n: int, edges: list[list[int]]) -> bool:\n    adj = {i: [] for i in range(n)}\n    for u, v in edges:\n        adj[u].append(v)\n        adj[v].append(u)\n    \n    color = [-1] * n\n    for i in range(n):\n        if color[i] != -1:\n            continue\n        color[i] = 0\n        q = deque([i])\n        while q:\n            u = q.popleft()\n            for v in adj[u]:\n                if color[v] == -1:\n                    color[v] = 1 - color[u]\n                    q.append(v)\n                elif color[v] == color[u]:\n                    return False\n    return True\n\ne_triangle = [[0, 1], [1, 2], [2, 0]]\ne_square = [[0, 1], [1, 2], [2, 3], [3, 0]]\nprint('Triangle Bipartite:', is_graph_bipartite(3, e_triangle))\nprint('Square Bipartite:', is_graph_bipartite(4, e_square))\n",
            "expectedOutputPatterns": [
                "Triangle Bipartite: False",
                "Square Bipartite: True"
            ],
            "hint": "color = [-1] * n. Loop i in range(n): if color[i] == -1: color[i] = 0, q = deque([i]). While q: u = q.popleft(). For v in adj[u]: if color[v] == -1: color[v] = 1 - color[u], q.append(v). Elif color[v] == color[u]: return False. Return True."
        },
        "keyTakeaway": "Successfully implemented and verified Bipartite Verification!"
    },
    {
        "id": "day127-step5",
        "stepNumber": 5,
        "title": "Day 127 Complete: Bipartite Graph Verification (2-Coloring)",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 127,
        "heading": "Mastery Achieved: Bipartite Graph Verification (2-Coloring)",
        "subheading": "You have solidified key mental models and techniques for Bipartite Verification.",
        "recapRows": [
            {
                "concept": "Odd Cycle Equivalence Theorem",
                "naiveIntuition": "Bipartition requires knowing both sets in advance",
                "pythonReality": "Greedy alternating 2-coloring succeeds if and only if the graph is free of odd cycles"
            },
            {
                "concept": "Matching & Network Flows",
                "naiveIntuition": "Bipartition is purely academic",
                "pythonReality": "Bipartite graphs model job assignment, stable matching, and bipartite maximum matching via Ford-Fulkerson"
            }
        ],
        "solidifiedConcepts": [
            "Vertex 2-Coloring Invariant",
            "Odd-Length Cycle Non-Bipartite Rule"
        ],
        "nextDayPreview": {
            "dayNumber": 128,
            "title": "Dijkstra's Algorithm: Shortest Paths",
            "description": "Implement Dijkstra's algorithm using priority queues to compute single-source shortest paths with non-negative edge weights."
        }
    }
]
},
  128: {
  "dayNumber": 128,
  "title": "Dijkstra's Algorithm: Shortest Paths",
  "topicName": "Dijkstra's Algorithm",
  "sectionId": "graphs",
  "estimatedMinutes": 45,
  "difficulty": "ADVANCED",
  "prerequisites": [
    113,
    121
  ],
  "concepts": [
    "Greedy Distance Relaxation (d[v] = d[u] + w)",
    "Min-Heap Optimization O((V+E) log V)"
  ],
  "practiceSkills": [
    "Dijkstra's Algorithm Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Implement Dijkstra's algorithm to compute single-source shortest paths on non-negative weighted graphs",
    "Maintain a min-heap of tentative distances and skip stale extracted entries in O((V + E) log V) time"
  ],
  "practiceArchetype": "algorithm",
  "flowTier": "tier3"
,
  "steps": [
    {
        "id": "day128-step1",
        "stepNumber": 1,
        "title": "Dijkstra's Algorithm: Shortest Paths: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Dijkstra's Algorithm",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Dijkstra's Algorithm.",
        "markdownContent": [
            "Dijkstra's Algorithm finds the Shortest Paths from a single source in graphs with non-negative edge weights using a Min-Heap (Priority Queue) to perform greedy distance relaxations in O((V + E) log V) time.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Dijkstra's Algorithm**, remember the central principle: Dijkstra greedily locks in the shortest distance to the closest unvisited node, requiring non-negative edge weights."
        ],
        "snippets": [
            {
                "title": "Dijkstra's Algorithm Implementation Template",
                "code": "import heapq\ndef dijkstra(n, adj, start):\n    dist = [float('inf')] * n\n    dist[start] = 0\n    pq = [(0, start)]\n    while pq:\n        d, u = heapq.heappop(pq)\n        if d > dist[u]: continue # Stale entry check!\n        for v, w in adj[u]:\n            if dist[u] + w < dist[v]:\n                dist[v] = dist[u] + w\n                heapq.heappush(pq, (dist[v], v))\n    return dist",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Dijkstra greedily locks in the shortest distance to the closest unvisited node, requiring non-negative edge weights."
    },
    {
        "id": "day128-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Dijkstra's Algorithm",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Maintain `dist` table initialized to infinity, `dist[start] = 0`. Min-heap stores `(current_dist, u)`. Pop minimum: if `current_dist > dist[u]`, discard (stale entry). For each neighbor `v` with weight `w`: if `dist[u] + w < dist[v]`, relax edge: `dist[v] = dist[u] + w`, and push `(dist[v], v)` into heap.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Dijkstra greedily locks in the shortest distance to the closest unvisited node, requiring non-negative edge weights.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Dijkstra's Algorithm Core Invariant",
                "content": "Dijkstra greedily locks in the shortest distance to the closest unvisited node, requiring non-negative edge weights."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Dijkstra greedily locks in the shortest distance to the closest unvisited node, requiring non-negative edge weights."
    },
    {
        "id": "day128-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Dijkstra's Algorithm",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d128-q1",
                "question": "Why does Dijkstra's algorithm fail on graphs with NEGATIVE edge weights?",
                "options": [
                    {
                        "id": "A",
                        "label": "Dijkstra assumes that once a node is popped from the heap, its shortest distance is finalized; a negative edge discovered later could retroactively produce an even shorter path, violating the greedy invariant"
                    },
                    {
                        "id": "B",
                        "label": "Because min-heaps crash when given negative numbers"
                    },
                    {
                        "id": "C",
                        "label": "Because negative weights turn directed graphs into undirected graphs"
                    },
                    {
                        "id": "D",
                        "label": "Because Python floats cannot represent negative infinity"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Dijkstra's greedy correctness relies on the invariant that adding non-negative edges can only INCREASE or maintain path lengths. Negative edges break this monotonicity, potentially offering shorter paths after a node has been marked finalized.",
                    "B": "Incorrect: Python min-heaps handle negative numbers seamlessly.",
                    "C": "Incorrect: Edge direction is independent of weight.",
                    "D": "Incorrect: Python floats support negative values."
                }
            },
            {
                "id": "chk-d128-q2",
                "question": "What is the purpose of the stale entry check `if d > dist[u]: continue` in Dijkstra's algorithm?",
                "options": [
                    {
                        "id": "A",
                        "label": "Python's `heapq` does not support `decrease_key`, so relaxed vertices push new tuples into the heap; older, higher-distance entries must be skipped when popped"
                    },
                    {
                        "id": "B",
                        "label": "To check for disconnected components"
                    },
                    {
                        "id": "C",
                        "label": "To sort the vertices in descending order"
                    },
                    {
                        "id": "D",
                        "label": "To prevent stack overflow"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Instead of an expensive O(V) search to update existing heap keys, we simply push the new smaller distance `(dist[v], v)`. When the older obsolete entries are popped later, `d > dist[u]` discards them in O(1).",
                    "B": "Incorrect: Disconnected nodes remain float('inf').",
                    "C": "Incorrect: Heap maintains minimum distance.",
                    "D": "Incorrect: Dijkstra is iterative."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day128-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Dijkstra's Algorithm",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Implement Dijkstra's algorithm to compute shortest path distances from node 0 to all other nodes.",
        "subheading": "Implement and verify Dijkstra's Algorithm in the interactive workspace.",
        "task": {
            "title": "Implement Dijkstra's algorithm to compute shortest path distances from node 0 to all other nodes.",
            "instructions": [
                "Implement Dijkstra's algorithm to compute shortest path distances from node 0 to all other nodes.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "import heapq\n\ndef dijkstra_shortest_paths(n: int, edges: list[list[int]], start: int) -> list[int]:\n    # TODO: edges: [u, v, weight] (directed)\n    # Compute shortest distance from start to all vertices\n    return []\n\n# 0 -> 1 (w=4), 0 -> 2 (w=1), 2 -> 1 (w=2), 1 -> 3 (w=1)\nedges = [[0, 1, 4], [0, 2, 1], [2, 1, 2], [1, 3, 1]]\nprint('Distances from 0:', dijkstra_shortest_paths(4, edges, 0))\n",
            "solutionCode": "import heapq\n\ndef dijkstra_shortest_paths(n: int, edges: list[list[int]], start: int) -> list[int]:\n    adj = {i: [] for i in range(n)}\n    for u, v, w in edges:\n        adj[u].append((v, w))\n    \n    dist = [float('inf')] * n\n    dist[start] = 0\n    pq = [(0, start)]\n    while pq:\n        d, u = heapq.heappop(pq)\n        if d > dist[u]:\n            continue\n        for v, w in adj[u]:\n            if dist[u] + w < dist[v]:\n                dist[v] = dist[u] + w\n                heapq.heappush(pq, (dist[v], v))\n    return dist\n\nedges = [[0, 1, 4], [0, 2, 1], [2, 1, 2], [1, 3, 1]]\nprint('Distances from 0:', dijkstra_shortest_paths(4, edges, 0))\n",
            "expectedOutputPatterns": [
                "Distances from 0: [0, 3, 1, 4]"
            ],
            "hint": "Initialize dist = [inf] * n, dist[start] = 0, pq = [(0, start)]. Loop while pq: pop d, u. If d > dist[u]: continue. For v, w in adj[u]: if dist[u] + w < dist[v]: dist[v] = dist[u] + w, push (dist[v], v). Return dist."
        },
        "keyTakeaway": "Successfully implemented and verified Dijkstra's Algorithm!"
    },
    {
        "id": "day128-step5",
        "stepNumber": 5,
        "title": "Day 128 Complete: Dijkstra's Algorithm: Shortest Paths",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 128,
        "heading": "Mastery Achieved: Dijkstra's Algorithm: Shortest Paths",
        "subheading": "You have solidified key mental models and techniques for Dijkstra's Algorithm.",
        "recapRows": [
            {
                "concept": "Lazy Deletion Technique",
                "naiveIntuition": "Update existing heap entries with decrease_key",
                "pythonReality": "Pushing duplicates and filtering stale entries with if d > dist[u]: continue achieves optimal O((V + E) log V) with standard heapq"
            },
            {
                "concept": "Non-Negative Monotonicity",
                "naiveIntuition": "Dijkstra works on any graph with weights",
                "pythonReality": "Dijkstra requires strictly non-negative weights; for negative weights, use Bellman-Ford"
            }
        ],
        "solidifiedConcepts": [
            "Greedy Distance Relaxation (d[v] = d[u] + w)",
            "Min-Heap Optimization O((V+E) log V)"
        ],
        "nextDayPreview": {
            "dayNumber": 129,
            "title": "Bellman-Ford & Negative Cycle Detection",
            "description": "Implement the Bellman-Ford algorithm in O(V * E) time, handle negative weights, and detect reachable negative cycles."
        }
    }
]
},
  129: {
  "dayNumber": 129,
  "title": "Bellman-Ford & Negative Cycle Detection",
  "topicName": "Bellman-Ford",
  "sectionId": "graphs",
  "estimatedMinutes": 45,
  "difficulty": "ADVANCED",
  "prerequisites": [
    128
  ],
  "concepts": [
    "V-1 Edge Relaxation Passes",
    "Negative Weight Cycle Detection on Pass V"
  ],
  "practiceSkills": [
    "Bellman-Ford Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Relax all graph edges V - 1 times to find shortest paths with negative edge weights",
    "Identify negative-weight cycles by checking if distances continue decreasing on pass V"
  ],
  "practiceArchetype": "algorithm",
  "flowTier": "tier3"
,
  "steps": [
    {
        "id": "day129-step1",
        "stepNumber": 1,
        "title": "Bellman-Ford & Negative Cycle Detection: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Bellman-Ford",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Bellman-Ford.",
        "markdownContent": [
            "Bellman-Ford Algorithm computes shortest paths on graphs with arbitrary (including negative) weights and detects Negative Weight Cycles by relaxing all edges V - 1 times in O(V * E) time.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Bellman-Ford**, remember the central principle: Any shortest path in a graph with V vertices has at most V - 1 edges; further relaxation implies a negative cycle."
        ],
        "snippets": [
            {
                "title": "Bellman-Ford Implementation Template",
                "code": "# Bellman-Ford with Negative Cycle Detection\ndef bellman_ford(n, edges, start):\n    dist = [float('inf')] * n\n    dist[start] = 0\n    for _ in range(n - 1):\n        for u, v, w in edges:\n            if dist[u] != float('inf') and dist[u] + w < dist[v]:\n                dist[v] = dist[u] + w\n    # V-th pass detects negative cycle\n    for u, v, w in edges:\n        if dist[u] != float('inf') and dist[u] + w < dist[v]:\n            return None # Negative cycle detected!\n    return dist",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Any shortest path in a graph with V vertices has at most V - 1 edges; further relaxation implies a negative cycle."
    },
    {
        "id": "day129-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Bellman-Ford",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Initialize `dist = [inf] * V`, `dist[start] = 0`. Repeat V - 1 times: for each edge `(u, v, w)`, relax: `if dist[u] + w < dist[v]: dist[v] = dist[u] + w`. Run a V-th pass: if ANY edge can still be relaxed, a negative weight cycle exists.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Any shortest path in a graph with V vertices has at most V - 1 edges; further relaxation implies a negative cycle.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Bellman-Ford Core Invariant",
                "content": "Any shortest path in a graph with V vertices has at most V - 1 edges; further relaxation implies a negative cycle."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Any shortest path in a graph with V vertices has at most V - 1 edges; further relaxation implies a negative cycle."
    },
    {
        "id": "day129-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Bellman-Ford",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d129-q1",
                "question": "Why is relaxing all edges V - 1 times sufficient to find all shortest paths in a graph with V vertices (assuming no negative cycles)?",
                "options": [
                    {
                        "id": "A",
                        "label": "A simple path without cycles can visit at most V vertices, which requires traversing at most V - 1 edges; each relaxation pass guarantees at least one more edge of the shortest path is resolved"
                    },
                    {
                        "id": "B",
                        "label": "Because edges are sorted by weight"
                    },
                    {
                        "id": "C",
                        "label": "Because V - 1 is the diameter of complete graphs"
                    },
                    {
                        "id": "D",
                        "label": "Because Python limits loops to V - 1 iterations"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Any path with >= V edges must visit at least one vertex twice, forming a cycle. In the absence of negative cycles, the optimal shortest path is always simple and contains at most V - 1 edges.",
                    "B": "Incorrect: Edge order can be completely arbitrary in Bellman-Ford.",
                    "C": "Incorrect: Complete graph diameter is 1.",
                    "D": "Incorrect: Loop bound is derived from graph theory."
                }
            },
            {
                "id": "chk-d129-q2",
                "question": "What occurs if an edge can STILL be relaxed during the V-th pass of Bellman-Ford?",
                "options": [
                    {
                        "id": "A",
                        "label": "A negative weight cycle exists reachable from the source, meaning path lengths can be reduced infinitely"
                    },
                    {
                        "id": "B",
                        "label": "The graph is disconnected"
                    },
                    {
                        "id": "C",
                        "label": "The algorithm needs one more pass"
                    },
                    {
                        "id": "D",
                        "label": "The edge weights are all positive"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! If a path can be shortened beyond V - 1 edges, it must be traversing a cycle whose total weight is strictly negative, allowing arbitrary reduction of distances.",
                    "B": "Incorrect: Disconnected nodes simply remain infinity.",
                    "C": "Incorrect: No finite number of passes can resolve negative cycles.",
                    "D": "Incorrect: Positive weights finalize within V - 1 passes."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day129-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Bellman-Ford",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Implement Bellman-Ford to compute shortest paths and detect negative cycles.",
        "subheading": "Implement and verify Bellman-Ford in the interactive workspace.",
        "task": {
            "title": "Implement Bellman-Ford to compute shortest paths and detect negative cycles.",
            "instructions": [
                "Implement Bellman-Ford to compute shortest paths and detect negative cycles.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "def bellman_ford_shortest(n: int, edges: list[list[int]], start: int) -> list[int]:\n    # TODO: Relax all edges n - 1 times; check n-th pass for negative cycles\n    # Return dist array or [] if negative cycle exists\n    return []\n\n# 0 -> 1 (w=4), 1 -> 2 (w=-2), 0 -> 2 (w=5)\ne = [[0, 1, 4], [1, 2, -2], [0, 2, 5]]\nprint('Distances:', bellman_ford_shortest(3, e, 0))\n",
            "solutionCode": "def bellman_ford_shortest(n: int, edges: list[list[int]], start: int) -> list[int]:\n    dist = [float('inf')] * n\n    dist[start] = 0\n    for _ in range(n - 1):\n        for u, v, w in edges:\n            if dist[u] != float('inf') and dist[u] + w < dist[v]:\n                dist[v] = dist[u] + w\n    for u, v, w in edges:\n        if dist[u] != float('inf') and dist[u] + w < dist[v]:\n            return []\n    return dist\n\ne = [[0, 1, 4], [1, 2, -2], [0, 2, 5]]\nprint('Distances:', bellman_ford_shortest(3, e, 0))\n",
            "expectedOutputPatterns": [
                "Distances: [0, 4, 2]"
            ],
            "hint": "dist = [inf] * n, dist[start] = 0. Loop n - 1 times: for u, v, w in edges: if dist[u] != inf and dist[u] + w < dist[v]: dist[v] = dist[u] + w. Loop once more for negative cycles."
        },
        "keyTakeaway": "Successfully implemented and verified Bellman-Ford!"
    },
    {
        "id": "day129-step5",
        "stepNumber": 5,
        "title": "Day 129 Complete: Bellman-Ford & Negative Cycle Detection",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 129,
        "heading": "Mastery Achieved: Bellman-Ford & Negative Cycle Detection",
        "subheading": "You have solidified key mental models and techniques for Bellman-Ford.",
        "recapRows": [
            {
                "concept": "Dynamic Programming over Edge Counts",
                "naiveIntuition": "Bellman-Ford is a queue traversal",
                "pythonReality": "Bellman-Ford is DP over edge lengths: pass k computes shortest paths using at most k edges"
            },
            {
                "concept": "Negative Cycle Diagnostic",
                "naiveIntuition": "Negative edges are impossible to handle",
                "pythonReality": "Bellman-Ford cleanly handles negative edge weights and flags infinite reduction arbitrage cycles"
            }
        ],
        "solidifiedConcepts": [
            "V-1 Edge Relaxation Passes",
            "Negative Weight Cycle Detection on Pass V"
        ],
        "nextDayPreview": {
            "dayNumber": 130,
            "title": "Disjoint Set Union (DSU / Union-Find)",
            "description": "Implement Disjoint Set Union (DSU) with Path Compression and Union by Rank, achieving near-O(1) amortized time."
        }
    }
]
},
  130: {
  "dayNumber": 130,
  "title": "Disjoint Set Union (DSU / Union-Find)",
  "topicName": "Disjoint Set Union",
  "sectionId": "graphs",
  "estimatedMinutes": 45,
  "difficulty": "ADVANCED",
  "prerequisites": [
    121
  ],
  "concepts": [
    "Path Compression Invariant",
    "Union by Rank/Size & Inverse Ackermann O(alpha(N))"
  ],
  "practiceSkills": [
    "Disjoint Set Union Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Implement Disjoint Set Union (Union-Find) with root representative find operations",
    "Achieve nearly O(1) amortized operations using Path Compression and Union by Rank"
  ],
  "practiceArchetype": "algorithm",
  "flowTier": "tier3"
,
  "steps": [
    {
        "id": "day130-step1",
        "stepNumber": 1,
        "title": "Disjoint Set Union (DSU / Union-Find): Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Disjoint Set Union",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Disjoint Set Union.",
        "markdownContent": [
            "Disjoint Set Union (DSU / Union-Find) maintains partitioned equivalence classes of elements, executing Find and Union in near-constant amortized O(alpha(N)) time using Path Compression and Union by Rank.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Disjoint Set Union**, remember the central principle: Path compression + union by rank flattens forest depths, delivering near-instant O(alpha(N)) connectivity queries."
        ],
        "snippets": [
            {
                "title": "Disjoint Set Union Implementation Template",
                "code": "# DSU Class with Path Compression & Union by Rank\nclass DSU:\n    def __init__(self, n):\n        self.parent = list(range(n))\n        self.rank = [0] * n\n    def find(self, x):\n        if self.parent[x] != x:\n            self.parent[x] = self.find(self.parent[x]) # Path compression\n        return self.parent[x]\n    def union(self, x, y):\n        rx, ry = self.find(x), self.find(y)\n        if rx == ry: return False\n        if self.rank[rx] < self.rank[ry]: rx, ry = ry, rx\n        self.parent[ry] = rx\n        if self.rank[rx] == self.rank[ry]: self.rank[rx] += 1\n        return True",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Path compression + union by rank flattens forest depths, delivering near-instant O(alpha(N)) connectivity queries."
    },
    {
        "id": "day130-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Disjoint Set Union",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Each element points to a parent: `parent[i] = i`. Find with Path Compression: recursively update `parent[x] = find(parent[x])`, flattening the tree into depth 1. Union by Rank: attach the shorter tree under the taller tree's root. Combined, operations take Inverse Ackermann $\\alpha(N) \\le 4$ time.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Path compression + union by rank flattens forest depths, delivering near-instant O(alpha(N)) connectivity queries.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Disjoint Set Union Core Invariant",
                "content": "Path compression + union by rank flattens forest depths, delivering near-instant O(alpha(N)) connectivity queries."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Path compression + union by rank flattens forest depths, delivering near-instant O(alpha(N)) connectivity queries."
    },
    {
        "id": "day130-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Disjoint Set Union",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d130-q1",
                "question": "How does Path Compression in `find(x)` optimize future queries?",
                "options": [
                    {
                        "id": "A",
                        "label": "It directly re-points every node along the traversal path directly to the representative root, flattening tree depth to ~1 for all subsequent lookups"
                    },
                    {
                        "id": "B",
                        "label": "It deletes duplicate elements from the set"
                    },
                    {
                        "id": "C",
                        "label": "It sorts the parents in numerical order"
                    },
                    {
                        "id": "D",
                        "label": "It creates a copy of the tree in memory"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! As recursion unwinds, `self.parent[x] = root` redirects every ancestor node to point directly to the group leader. Subsequent calls for any node along that chain take strict O(1).",
                    "B": "Incorrect: Sets partition disjoint elements; no nodes are deleted.",
                    "C": "Incorrect: Parent references point to roots, not sorted values.",
                    "D": "Incorrect: Mutation occurs in-place on the parent array."
                }
            },
            {
                "id": "chk-d130-q2",
                "question": "What is the amortized time complexity of a sequence of M DSU operations on N elements when combining Path Compression and Union by Rank?",
                "options": [
                    {
                        "id": "A",
                        "label": "O(M * alpha(N)), where alpha is the Inverse Ackermann function (effectively <= 4 for all practical universe sizes)"
                    },
                    {
                        "id": "B",
                        "label": "O(M * log N)"
                    },
                    {
                        "id": "C",
                        "label": "O(M * N)"
                    },
                    {
                        "id": "D",
                        "label": "O(M^2)"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Tarjan proved that path compression combined with union by rank/size achieves $O(M \\cdot \\alpha(N))$ time. Because $\\alpha(10^{80}) < 5$, each operation runs in virtually O(1) time.",
                    "B": "Incorrect: O(log N) is the bound when using Union by Rank alone without Path Compression.",
                    "C": "Incorrect: Without optimizations, degenerate chains take O(N).",
                    "D": "Incorrect: Quadratic bounds apply only to naive array scanning."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day130-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Disjoint Set Union",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Count the number of connected components in an undirected graph using DSU.",
        "subheading": "Implement and verify Disjoint Set Union in the interactive workspace.",
        "task": {
            "title": "Count the number of connected components in an undirected graph using DSU.",
            "instructions": [
                "Count the number of connected components in an undirected graph using DSU.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "class DSU:\n    def __init__(self, n):\n        self.p = list(range(n))\n    def find(self, x):\n        if self.p[x] != x:\n            self.p[x] = self.find(self.p[x])\n        return self.p[x]\n    def union(self, x, y):\n        rx, ry = self.find(x), self.find(y)\n        if rx != ry:\n            self.p[rx] = ry\n            return True\n        return False\n\ndef count_components(n: int, edges: list[list[int]]) -> int:\n    # TODO: Union edges and count unique component roots\n    return 0\n\nedges = [[0, 1], [1, 2], [3, 4]]\nprint('Components count:', count_components(5, edges)) # 2 ({0, 1, 2} and {3, 4})\n",
            "solutionCode": "class DSU:\n    def __init__(self, n):\n        self.p = list(range(n))\n    def find(self, x):\n        if self.p[x] != x:\n            self.p[x] = self.find(self.p[x])\n        return self.p[x]\n    def union(self, x, y):\n        rx, ry = self.find(x), self.find(y)\n        if rx != ry:\n            self.p[rx] = ry\n            return True\n        return False\n\ndef count_components(n: int, edges: list[list[int]]) -> int:\n    dsu = DSU(n)\n    components = n\n    for u, v in edges:\n        if dsu.union(u, v):\n            components -= 1\n    return components\n\nedges = [[0, 1], [1, 2], [3, 4]]\nprint('Components count:', count_components(5, edges))\n",
            "expectedOutputPatterns": [
                "Components count: 2"
            ],
            "hint": "Start with components = n. For each u, v in edges: if dsu.union(u, v): components -= 1. Return components."
        },
        "keyTakeaway": "Successfully implemented and verified Disjoint Set Union!"
    },
    {
        "id": "day130-step5",
        "stepNumber": 5,
        "title": "Day 130 Complete: Disjoint Set Union (DSU / Union-Find)",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 130,
        "heading": "Mastery Achieved: Disjoint Set Union (DSU / Union-Find)",
        "subheading": "You have solidified key mental models and techniques for Disjoint Set Union.",
        "recapRows": [
            {
                "concept": "Dynamic Equivalence Partitioning",
                "naiveIntuition": "Re-run BFS on every edge addition",
                "pythonReality": "DSU maintains transitive connectivity dynamically in O(alpha(N)) without rebuilding adjacency lists"
            },
            {
                "concept": "Forest Representation",
                "naiveIntuition": "Store sets as Python set() objects",
                "pythonReality": "Representing disjoint sets as inverted parent-pointer trees in a flat array eliminates set union allocation costs"
            }
        ],
        "solidifiedConcepts": [
            "Path Compression Invariant",
            "Union by Rank/Size & Inverse Ackermann O(alpha(N))"
        ],
        "nextDayPreview": {
            "dayNumber": 131,
            "title": "Minimum Spanning Tree: Kruskal's with DSU",
            "description": "Implement Kruskal's algorithm to find Minimum Spanning Trees (MST) by sorting edges and avoiding cycles with DSU."
        }
    }
]
},
  131: {
  "dayNumber": 131,
  "title": "Minimum Spanning Tree: Kruskal's with DSU",
  "topicName": "Kruskal's MST",
  "sectionId": "graphs",
  "estimatedMinutes": 45,
  "difficulty": "ADVANCED",
  "prerequisites": [
    130
  ],
  "concepts": [
    "Greedy Edge Weight Sorting",
    "Cycle Avoidance via DSU"
  ],
  "practiceSkills": [
    "Kruskal's MST Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Sort all graph edges by weight and greedily select non-cyclic edges using DSU",
    "Construct a Minimum Spanning Tree in O(E log E) time"
  ],
  "practiceArchetype": "algorithm",
  "flowTier": "tier3"
,
  "steps": [
    {
        "id": "day131-step1",
        "stepNumber": 1,
        "title": "Minimum Spanning Tree: Kruskal's with DSU: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Kruskal's MST",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Kruskal's MST.",
        "markdownContent": [
            "Kruskal's Algorithm constructs a Minimum Spanning Tree (MST) by greedily sorting all edges by weight and adding edges that do not form cycles using DSU in O(E log E) time.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Kruskal's MST**, remember the central principle: Kruskal greedily adds the cheapest available edge that connects two previously disjoint components."
        ],
        "snippets": [
            {
                "title": "Kruskal's MST Implementation Template",
                "code": "# Kruskal's MST\ndef kruskal(n, edges):\n    edges.sort(key=lambda x: x[2]) # Sort by weight\n    dsu = DSU(n)\n    total_weight = 0\n    edges_used = 0\n    for u, v, w in edges:\n        if dsu.union(u, v):\n            total_weight += w\n            edges_used += 1\n            if edges_used == n - 1: break\n    return total_weight if edges_used == n - 1 else -1",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Kruskal greedily adds the cheapest available edge that connects two previously disjoint components."
    },
    {
        "id": "day131-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Kruskal's MST",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Sort all edges by weight ascending. Initialize DSU with V vertices, `mst_weight = 0`, `edges_count = 0`. For each `(u, v, w)`: check `if dsu.find(u) != dsu.find(v)`: union u and v, add w to `mst_weight`, increment `edges_count`. Stop when `edges_count == V - 1`.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Kruskal greedily adds the cheapest available edge that connects two previously disjoint components.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Kruskal's MST Core Invariant",
                "content": "Kruskal greedily adds the cheapest available edge that connects two previously disjoint components."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Kruskal greedily adds the cheapest available edge that connects two previously disjoint components."
    },
    {
        "id": "day131-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Kruskal's MST",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d131-q1",
                "question": "Why is the sorting step `O(E log E)` the asymptotic bottleneck of Kruskal's algorithm?",
                "options": [
                    {
                        "id": "A",
                        "label": "Sorting E edges takes O(E log E), while the subsequent DSU operations take near-linear O(E * alpha(V)), making sorting dominant"
                    },
                    {
                        "id": "B",
                        "label": "Because DSU takes O(E^2) time"
                    },
                    {
                        "id": "C",
                        "label": "Because edges must be sorted twice"
                    },
                    {
                        "id": "D",
                        "label": "Because Kruskal uses binary search on vertices"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! DSU operations are so fast ($O(E \\cdot \\alpha(V)) \\approx O(E)$) that the initial comparison sort on edge weights ($O(E \\log E) = O(E \\log V)$) completely dictates total execution time.",
                    "B": "Incorrect: DSU is near O(1) per operation.",
                    "C": "Incorrect: Edges are sorted once.",
                    "D": "Incorrect: Kruskal scans sorted edges linearly."
                }
            },
            {
                "id": "chk-d131-q2",
                "question": "What mathematical property of spanning trees ensures that Kruskal terminates when `edges_used == V - 1`?",
                "options": [
                    {
                        "id": "A",
                        "label": "Any tree spanning V vertices consists of exactly V - 1 edges with zero cycles"
                    },
                    {
                        "id": "B",
                        "label": "A graph cannot have more than V - 1 edges"
                    },
                    {
                        "id": "C",
                        "label": "Because DSU only supports V - 1 elements"
                    },
                    {
                        "id": "D",
                        "label": "To prevent stack overflow"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! A tree on V vertices has exactly V - 1 edges by definition. Once V - 1 cycle-free edges have been merged into the DSU, all V vertices belong to a single connected component.",
                    "B": "Incorrect: Graphs can have up to V*(V-1)/2 edges.",
                    "C": "Incorrect: DSU supports any number of elements.",
                    "D": "Incorrect: Kruskal is an iterative loop."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day131-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Kruskal's MST",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Calculate the total weight of a Minimum Spanning Tree using Kruskal's algorithm.",
        "subheading": "Implement and verify Kruskal's MST in the interactive workspace.",
        "task": {
            "title": "Calculate the total weight of a Minimum Spanning Tree using Kruskal's algorithm.",
            "instructions": [
                "Calculate the total weight of a Minimum Spanning Tree using Kruskal's algorithm.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "class DSU:\n    def __init__(self, n):\n        self.p = list(range(n))\n    def find(self, x):\n        if self.p[x] != x:\n            self.p[x] = self.find(self.p[x])\n        return self.p[x]\n    def union(self, x, y):\n        rx, ry = self.find(x), self.find(y)\n        if rx != ry:\n            self.p[rx] = ry\n            return True\n        return False\n\ndef min_spanning_tree_weight(n: int, edges: list[list[int]]) -> int:\n    # TODO: edges: [u, v, weight]. Implement Kruskal's algorithm\n    return 0\n\nedges = [[0, 1, 10], [0, 2, 6], [0, 3, 5], [1, 3, 15], [2, 3, 4]]\nprint('MST Weight:', min_spanning_tree_weight(4, edges)) # 19 (edges: 2-3 (4), 0-3 (5), 0-1 (10))\n",
            "solutionCode": "class DSU:\n    def __init__(self, n):\n        self.p = list(range(n))\n    def find(self, x):\n        if self.p[x] != x:\n            self.p[x] = self.find(self.p[x])\n        return self.p[x]\n    def union(self, x, y):\n        rx, ry = self.find(x), self.find(y)\n        if rx != ry:\n            self.p[rx] = ry\n            return True\n        return False\n\ndef min_spanning_tree_weight(n: int, edges: list[list[int]]) -> int:\n    edges.sort(key=lambda x: x[2])\n    dsu = DSU(n)\n    total = 0\n    count = 0\n    for u, v, w in edges:\n        if dsu.union(u, v):\n            total += w\n            count += 1\n            if count == n - 1:\n                break\n    return total if count == n - 1 else -1\n\nedges = [[0, 1, 10], [0, 2, 6], [0, 3, 5], [1, 3, 15], [2, 3, 4]]\nprint('MST Weight:', min_spanning_tree_weight(4, edges))\n",
            "expectedOutputPatterns": [
                "MST Weight: 19"
            ],
            "hint": "Sort edges by w: edges.sort(key=lambda x: x[2]). Loop u, v, w: if dsu.union(u, v): total += w; count += 1; if count == n - 1: break. Return total."
        },
        "keyTakeaway": "Successfully implemented and verified Kruskal's MST!"
    },
    {
        "id": "day131-step5",
        "stepNumber": 5,
        "title": "Day 131 Complete: Minimum Spanning Tree: Kruskal's with DSU",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 131,
        "heading": "Mastery Achieved: Minimum Spanning Tree: Kruskal's with DSU",
        "subheading": "You have solidified key mental models and techniques for Kruskal's MST.",
        "recapRows": [
            {
                "concept": "Global Greedy Edge Selection",
                "naiveIntuition": "Grow tree from an initial starting root",
                "pythonReality": "Kruskal operates globally across all edges, growing disconnected forest islands until they merge into a single tree"
            },
            {
                "concept": "Cut Property Foundation",
                "naiveIntuition": "Greedy choices might fail globally",
                "pythonReality": "The Cut Property of graphs guarantees that the lightest edge crossing any partition cut must belong to some MST"
            }
        ],
        "solidifiedConcepts": [
            "Greedy Edge Weight Sorting",
            "Cycle Avoidance via DSU"
        ],
        "nextDayPreview": {
            "dayNumber": 132,
            "title": "Minimum Spanning Tree: Prim's Algorithm",
            "description": "Implement Prim's algorithm for Minimum Spanning Trees using priority queues to select minimum crossing edges."
        }
    }
]
},
  132: {
  "dayNumber": 132,
  "title": "Minimum Spanning Tree: Prim's Algorithm",
  "topicName": "Prim's MST",
  "sectionId": "graphs",
  "estimatedMinutes": 40,
  "difficulty": "ADVANCED",
  "prerequisites": [
    113,
    131
  ],
  "concepts": [
    "Growing Subtree Frontier Cut",
    "Min-Heap Crossing Edge Selection"
  ],
  "practiceSkills": [
    "Prim's MST Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Grow an MST from a start vertex by repeatedly selecting the minimum crossing edge via a min-heap",
    "Achieve O((V + E) log V) runtime on dense graphs"
  ],
  "practiceArchetype": "algorithm",
  "flowTier": "tier2"
,
  "steps": [
    {
        "id": "day132-step1",
        "stepNumber": 1,
        "title": "Minimum Spanning Tree: Prim's Algorithm: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Prim's MST",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Prim's MST.",
        "markdownContent": [
            "Prim's Algorithm constructs an MST by growing a single connected tree from an arbitrary starting vertex, greedily adding the cheapest cut edge using a Min-Heap in O((V + E) log V) time.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Prim's MST**, remember the central principle: Prim grows a single tree vertex by vertex; Kruskal merges a forest edge by edge."
        ],
        "snippets": [
            {
                "title": "Prim's MST Implementation Template",
                "code": "# Prim's MST\nimport heapq\ndef prim(n, adj):\n    visited = set()\n    pq = [(0, 0)] # (weight, vertex)\n    total_weight = 0\n    while pq and len(visited) < n:\n        w, u = heapq.heappop(pq)\n        if u in visited: continue\n        visited.add(u)\n        total_weight += w\n        for v, weight in adj[u]:\n            if v not in visited:\n                heapq.heappush(pq, (weight, v))\n    return total_weight if len(visited) == n else -1",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Prim grows a single tree vertex by vertex; Kruskal merges a forest edge by edge."
    },
    {
        "id": "day132-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Prim's MST",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Start with arbitrary root in `visited = {start}`. Min-heap stores candidate crossing edges `(weight, neighbor)`. While heap non-empty and `len(visited) < V`: pop cheapest edge `(w, u)`. If `u in visited`: discard. Else mark `visited.add(u)`, add `w` to MST weight, and push all edges from `u` to unvisited neighbors.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Prim grows a single tree vertex by vertex; Kruskal merges a forest edge by edge.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Prim's MST Core Invariant",
                "content": "Prim grows a single tree vertex by vertex; Kruskal merges a forest edge by edge."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Prim grows a single tree vertex by vertex; Kruskal merges a forest edge by edge."
    },
    {
        "id": "day132-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Prim's MST",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d132-q1",
                "question": "How does Prim's algorithm differ conceptually from Kruskal's algorithm in how the tree grows?",
                "options": [
                    {
                        "id": "A",
                        "label": "Prim grows a single contiguous tree outwards from an initial vertex, while Kruskal merges an independent forest of disconnected components across the whole graph"
                    },
                    {
                        "id": "B",
                        "label": "Prim uses a stack, Kruskal uses a queue"
                    },
                    {
                        "id": "C",
                        "label": "Prim only works on directed graphs"
                    },
                    {
                        "id": "D",
                        "label": "Kruskal produces a tree with lower weight than Prim"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Prim maintains one connected tree at all times, adding the cheapest edge crossing the cut between the tree and the remaining nodes. Kruskal considers all edges globally, merging separate trees.",
                    "B": "Incorrect: Prim uses a min-heap, Kruskal uses DSU.",
                    "C": "Incorrect: Both algorithms operate on undirected weighted graphs.",
                    "D": "Incorrect: Both compute an identical optimal MST total weight."
                }
            },
            {
                "id": "chk-d132-q2",
                "question": "When is Prim's algorithm preferred over Kruskal's algorithm?",
                "options": [
                    {
                        "id": "A",
                        "label": "On dense graphs where E approaches V^2 (especially with an adjacency matrix implementation O(V^2))"
                    },
                    {
                        "id": "B",
                        "label": "When all edge weights are negative"
                    },
                    {
                        "id": "C",
                        "label": "When the graph is disconnected"
                    },
                    {
                        "id": "D",
                        "label": "When memory is limited to 1 byte"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! In dense graphs with E ~ V^2, Kruskal's sorting costs $O(V^2 \\log V)$. Prim's algorithm (using an adjacency matrix and distance array) runs in $O(V^2)$ without sorting edges.",
                    "B": "Incorrect: Negative weights do not affect MST algorithms because spanning trees have fixed V-1 edges without cycles.",
                    "C": "Incorrect: Disconnected graphs cannot form a single spanning tree.",
                    "D": "Incorrect: Neither fits in 1 byte."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day132-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Prim's MST",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Compute the Minimum Spanning Tree weight using Prim's algorithm.",
        "subheading": "Implement and verify Prim's MST in the interactive workspace.",
        "task": {
            "title": "Compute the Minimum Spanning Tree weight using Prim's algorithm.",
            "instructions": [
                "Compute the Minimum Spanning Tree weight using Prim's algorithm.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "import heapq\n\ndef prim_mst(n: int, edges: list[list[int]]) -> int:\n    # TODO: Build adj list and implement Prim's algorithm with heapq\n    return 0\n\nedges = [[0, 1, 1], [1, 2, 2], [0, 2, 4], [2, 3, 3]]\nprint('Prim MST Weight:', prim_mst(4, edges)) # 6 (edges: 0-1 (1), 1-2 (2), 2-3 (3))\n",
            "solutionCode": "import heapq\n\ndef prim_mst(n: int, edges: list[list[int]]) -> int:\n    adj = {i: [] for i in range(n)}\n    for u, v, w in edges:\n        adj[u].append((v, w))\n        adj[v].append((u, w))\n    \n    visited = set()\n    pq = [(0, 0)]\n    total = 0\n    while pq and len(visited) < n:\n        w, u = heapq.heappop(pq)\n        if u in visited:\n            continue\n        visited.add(u)\n        total += w\n        for v, weight in adj[u]:\n            if v not in visited:\n                heapq.heappush(pq, (weight, v))\n    return total if len(visited) == n else -1\n\nedges = [[0, 1, 1], [1, 2, 2], [0, 2, 4], [2, 3, 3]]\nprint('Prim MST Weight:', prim_mst(4, edges))\n",
            "expectedOutputPatterns": [
                "Prim MST Weight: 6"
            ],
            "hint": "adj: u -> (v, w). visited = set(), pq = [(0, 0)], total = 0. While pq and len(visited) < n: pop w, u. If u in visited continue. visited.add(u); total += w. Loop neighbors: push (weight, v) if v not in visited."
        },
        "keyTakeaway": "Successfully implemented and verified Prim's MST!"
    },
    {
        "id": "day132-step5",
        "stepNumber": 5,
        "title": "Day 132 Complete: Minimum Spanning Tree: Prim's Algorithm",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 132,
        "heading": "Mastery Achieved: Minimum Spanning Tree: Prim's Algorithm",
        "subheading": "You have solidified key mental models and techniques for Prim's MST.",
        "recapRows": [
            {
                "concept": "Cut Edge Relaxation",
                "naiveIntuition": "Sort all graph edges first",
                "pythonReality": "Prim only inspects edges incident to the current tree boundary, dynamically maintaining cut candidates via min-heap"
            },
            {
                "concept": "Structural Invariant Equivalence",
                "naiveIntuition": "Different MST algorithms produce different weights",
                "pythonReality": "Both Kruskal and Prim produce the identical minimum spanning tree weight for any connected weighted graph"
            }
        ],
        "solidifiedConcepts": [
            "Growing Subtree Frontier Cut",
            "Min-Heap Crossing Edge Selection"
        ],
        "nextDayPreview": {
            "dayNumber": 133,
            "title": "Undirected Bridges & Articulation Points",
            "description": "Find all bridges and articulation points in undirected graphs using Tarjan's discovery time (tin) and low-link (low) DFS."
        }
    }
]
},
  133: {
  "dayNumber": 133,
  "title": "Undirected Bridges & Articulation Points",
  "topicName": "Bridges & Articulation",
  "sectionId": "graphs",
  "estimatedMinutes": 45,
  "difficulty": "ADVANCED",
  "prerequisites": [
    123
  ],
  "concepts": [
    "DFS Discovery Times (tin)",
    "Low-Link Values (low) & Bridge Condition (low[v] > tin[u])"
  ],
  "practiceSkills": [
    "Bridges & Articulation Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Calculate discovery times and lowest reachable ancestor depths during a single DFS traversal",
    "Locate all critical bridges and articulation cut-vertices in O(V + E) time"
  ],
  "practiceArchetype": "algorithm",
  "flowTier": "tier3"
,
  "steps": [
    {
        "id": "day133-step1",
        "stepNumber": 1,
        "title": "Undirected Bridges & Articulation Points: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Bridges & Articulation",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Bridges & Articulation.",
        "markdownContent": [
            "Bridges and Articulation Points identify critical failure edges and vertices whose removal increases graph connected components, discovered via Tarjan's Low-Link DFS in O(V + E) time.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Bridges & Articulation**, remember the central principle: If a subtree's lowest reachable node is discovered strictly AFTER u (low[v] > tin[u]), edge (u, v) is a bridge."
        ],
        "snippets": [
            {
                "title": "Bridges & Articulation Implementation Template",
                "code": "# Tarjan's Bridges Detection\ndef find_bridges(n, adj):\n    tin = [-1] * n\n    low = [-1] * n\n    timer = 0\n    bridges = []\n    def dfs(u, p=-1):\n        nonlocal timer\n        tin[u] = low[u] = timer\n        timer += 1\n        for v in adj[u]:\n            if v == p: continue\n            if tin[v] != -1:\n                low[u] = min(low[u], tin[v])\n            else:\n                dfs(v, u)\n                low[u] = min(low[u], low[v])\n                if low[v] > tin[u]:\n                    bridges.append((u, v))\n    for i in range(n):\n        if tin[i] == -1: dfs(i)\n    return bridges",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "If a subtree's lowest reachable node is discovered strictly AFTER u (low[v] > tin[u]), edge (u, v) is a bridge."
    },
    {
        "id": "day133-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Bridges & Articulation",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Track discovery time `tin[u]` and lowest reachable discovery time `low[u]`. For edge `(u, v)`: if `v == parent`: continue. If `v` already visited: `low[u] = min(low[u], tin[v])` (back-edge). Else recurse on `v`, then `low[u] = min(low[u], low[v])`. Bridge condition: if `low[v] > tin[u]`, edge `(u, v)` is a critical bridge!",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: If a subtree's lowest reachable node is discovered strictly AFTER u (low[v] > tin[u]), edge (u, v) is a bridge.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Bridges & Articulation Core Invariant",
                "content": "If a subtree's lowest reachable node is discovered strictly AFTER u (low[v] > tin[u]), edge (u, v) is a bridge."
            }
        ],
        "keyTakeaway": "Operational invariant locked: If a subtree's lowest reachable node is discovered strictly AFTER u (low[v] > tin[u]), edge (u, v) is a bridge."
    },
    {
        "id": "day133-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Bridges & Articulation",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d133-q1",
                "question": "What does the condition `low[v] > tin[u]` prove about edge `(u, v)` in Tarjan's algorithm?",
                "options": [
                    {
                        "id": "A",
                        "label": "Node v and its entire subtree have zero back-edges reaching ancestor u or earlier, so removing (u, v) completely isolates v's component"
                    },
                    {
                        "id": "B",
                        "label": "Edge (u, v) is part of a triangle"
                    },
                    {
                        "id": "C",
                        "label": "Vertex v has a smaller degree than u"
                    },
                    {
                        "id": "D",
                        "label": "The graph contains a negative cycle"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! `tin[u]` is when u was discovered. If `low[v] > tin[u]`, it means the highest ancestor reachable from v's subtree was discovered strictly after u. Therefore, no alternate path back to the rest of the graph exists.",
                    "B": "Incorrect: If (u, v) were part of a triangle, low[v] <= tin[u], so it wouldn't be a bridge.",
                    "C": "Incorrect: Degree is irrelevant.",
                    "D": "Incorrect: Bridges are unweighted structural edges."
                }
            },
            {
                "id": "chk-d133-q2",
                "question": "Why must the check `if v == p: continue` be enforced in undirected bridge discovery?",
                "options": [
                    {
                        "id": "A",
                        "label": "To prevent treating the trivial reciprocal edge back to the direct parent as a cycle-forming back-edge"
                    },
                    {
                        "id": "B",
                        "label": "To prevent infinite loops in binary trees"
                    },
                    {
                        "id": "C",
                        "label": "Because parent nodes are already deleted"
                    },
                    {
                        "id": "D",
                        "label": "To sort edges"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! In undirected graphs, (u, v) implies (v, u). If we allowed `low[u] = min(low[u], tin[parent])`, EVERY edge would trivially claim low <= tin, falsely hiding all bridges.",
                    "B": "Incorrect: Graph is general undirected graph.",
                    "C": "Incorrect: Parents are active in the recursion stack.",
                    "D": "Incorrect: Has nothing to do with sorting."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day133-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Bridges & Articulation",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Find all critical connection bridges in a network using Tarjan's algorithm.",
        "subheading": "Implement and verify Bridges & Articulation in the interactive workspace.",
        "task": {
            "title": "Find all critical connection bridges in a network using Tarjan's algorithm.",
            "instructions": [
                "Find all critical connection bridges in a network using Tarjan's algorithm.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "def critical_connections(n: int, connections: list[list[int]]) -> list[list[int]]:\n    # TODO: Implement Tarjan's bridge algorithm\n    return []\n\n# 0-1, 1-2, 2-0 (cycle), 1-3 (bridge to 3)\nconns = [[0, 1], [1, 2], [2, 0], [1, 3]]\nprint('Bridges:', critical_connections(4, conns)) # [[1, 3]]\n",
            "solutionCode": "def critical_connections(n: int, connections: list[list[int]]) -> list[list[int]]:\n    adj = {i: [] for i in range(n)}\n    for u, v in connections:\n        adj[u].append(v)\n        adj[v].append(u)\n    \n    tin = [-1] * n\n    low = [-1] * n\n    timer = 0\n    bridges = []\n    \n    def dfs(u, p=-1):\n        nonlocal timer\n        tin[u] = low[u] = timer\n        timer += 1\n        for v in adj[u]:\n            if v == p:\n                continue\n            if tin[v] != -1:\n                low[u] = min(low[u], tin[v])\n            else:\n                dfs(v, u)\n                low[u] = min(low[u], low[v])\n                if low[v] > tin[u]:\n                    bridges.append([u, v])\n                    \n    for i in range(n):\n        if tin[i] == -1:\n            dfs(i)\n    return bridges\n\nconns = [[0, 1], [1, 2], [2, 0], [1, 3]]\nprint('Bridges:', critical_connections(4, conns))\n",
            "expectedOutputPatterns": [
                "Bridges: [[1, 3]]"
            ],
            "hint": "tin = [-1] * n, low = [-1] * n, timer = 0. In dfs(u, p): tin[u] = low[u] = timer; timer += 1. For v in adj[u]: if v == p continue. If tin[v] != -1: low[u] = min(low[u], tin[v]). Else: dfs(v, u); low[u] = min(low[u], low[v]); if low[v] > tin[u]: bridges.append([u, v])."
        },
        "keyTakeaway": "Successfully implemented and verified Bridges & Articulation!"
    },
    {
        "id": "day133-step5",
        "stepNumber": 5,
        "title": "Day 133 Complete: Undirected Bridges & Articulation Points",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 133,
        "heading": "Mastery Achieved: Undirected Bridges & Articulation Points",
        "subheading": "You have solidified key mental models and techniques for Bridges & Articulation.",
        "recapRows": [
            {
                "concept": "Low-Link Reachability Metric",
                "naiveIntuition": "Test each edge by deleting it and re-running BFS O(E * (V + E))",
                "pythonReality": "Tarjan's low-link discovery time identifies all critical bridges in a single O(V + E) linear pass"
            },
            {
                "concept": "Infrastructure Resilience",
                "naiveIntuition": "All redundant networks are robust",
                "pythonReality": "Bridge edges represent single points of failure in power grids, internet backbones, and distributed consensus clusters"
            }
        ],
        "solidifiedConcepts": [
            "DFS Discovery Times (tin)",
            "Low-Link Values (low) & Bridge Condition (low[v] > tin[u])"
        ],
        "nextDayPreview": {
            "dayNumber": 134,
            "title": "Strongly Connected Components (Kosaraju)",
            "description": "Implement Kosaraju's two-pass DFS algorithm on graphs and their transposes to find Strongly Connected Components in DAGs."
        }
    }
]
},
  134: {
  "dayNumber": 134,
  "title": "Strongly Connected Components (Kosaraju)",
  "topicName": "Strongly Connected Components",
  "sectionId": "graphs",
  "estimatedMinutes": 45,
  "difficulty": "ADVANCED",
  "prerequisites": [
    123,
    133
  ],
  "concepts": [
    "Transpose Graph Reversal",
    "Kosaraju's Two-Pass DFS Algorithm"
  ],
  "practiceSkills": [
    "Strongly Connected Components Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Reconstruct transposed reversed graphs where directed edge orientations are inverted",
    "Extract all Strongly Connected Components (SCCs) in directed graphs using Kosaraju's algorithm in O(V + E) time"
  ],
  "practiceArchetype": "algorithm",
  "flowTier": "tier3"
,
  "steps": [
    {
        "id": "day134-step1",
        "stepNumber": 1,
        "title": "Strongly Connected Components (Kosaraju): Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Strongly Connected Components",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Strongly Connected Components.",
        "markdownContent": [
            "Strongly Connected Components (SCCs) are maximal subgraphs in directed graphs where every vertex is reachable from every other vertex, decomposed via Kosaraju's Two-Pass Algorithm in O(V + E) time.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Strongly Connected Components**, remember the central principle: Reversing edges in G^T traps DFS inside the source SCC, isolating strongly connected components."
        ],
        "snippets": [
            {
                "title": "Strongly Connected Components Implementation Template",
                "code": "# Kosaraju's SCC Algorithm\ndef kosaraju_scc(n, adj):\n    stack = []\n    visited = [False] * n\n    def dfs1(u):\n        visited[u] = True\n        for v in adj[u]:\n            if not visited[v]: dfs1(v)\n        stack.append(u) # Finish stack\n    for i in range(n):\n        if not visited[i]: dfs1(i)\n    # Transpose graph\n    adj_rev = {i: [] for i in range(n)}\n    for u in range(n):\n        for v in adj[u]: adj_rev[v].append(u)\n    # Pass 2\n    visited = [False] * n\n    sccs = []\n    while stack:\n        u = stack.pop()\n        if not visited[u]:\n            comp = []\n            def dfs2(curr):\n                visited[curr] = True\n                comp.append(curr)\n                for nxt in adj_rev[curr]:\n                    if not visited[nxt]: dfs2(nxt)\n            dfs2(u)\n            sccs.append(comp)\n    return sccs",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Reversing edges in G^T traps DFS inside the source SCC, isolating strongly connected components."
    },
    {
        "id": "day134-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Strongly Connected Components",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Pass 1: Run DFS on original graph, recording vertices in a stack upon finishing. Pass 2: Invert all directed edges (transpose graph $G^T$). Pop vertices from stack; if unvisited in $G^T$, launch DFS to collect the entire SCC.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Reversing edges in G^T traps DFS inside the source SCC, isolating strongly connected components.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Strongly Connected Components Core Invariant",
                "content": "Reversing edges in G^T traps DFS inside the source SCC, isolating strongly connected components."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Reversing edges in G^T traps DFS inside the source SCC, isolating strongly connected components."
    },
    {
        "id": "day134-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Strongly Connected Components",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d134-q1",
                "question": "Why does reversing the graph edges ($G^T$) prevent DFS in Pass 2 from leaking into other SCCs?",
                "options": [
                    {
                        "id": "A",
                        "label": "Edges between SCCs point from earlier-finishing components to later ones in $G^T$; popping from the stack processes components in topological sink order, preventing outward escape"
                    },
                    {
                        "id": "B",
                        "label": "Because reversing edges destroys all cycles"
                    },
                    {
                        "id": "C",
                        "label": "Because $G^T$ converts the directed graph into an undirected graph"
                    },
                    {
                        "id": "D",
                        "label": "Because transpose graphs have half as many edges"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! In the condensation DAG of SCCs, edges point from source SCC to sink SCC. In $G^T$, edges point from sink to source. Popping the highest finish time starts at the source of $G^T$ (the sink of G), trapping the search strictly within that SCC.",
                    "B": "Incorrect: Cycles inside an SCC remain cycles in $G^T$.",
                    "C": "Incorrect: Transpose graph remains directed.",
                    "D": "Incorrect: Edge count is identical."
                }
            },
            {
                "id": "chk-d134-q2",
                "question": "What is the result of condensing every SCC in a directed graph into a single super-vertex?",
                "options": [
                    {
                        "id": "A",
                        "label": "A Directed Acyclic Graph (DAG) with zero cycles"
                    },
                    {
                        "id": "B",
                        "label": "A complete graph"
                    },
                    {
                        "id": "C",
                        "label": "An undirected tree"
                    },
                    {
                        "id": "D",
                        "label": "A single giant cycle"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! By definition, all mutual reachability cycles are collapsed inside their respective SCCs. Any remaining inter-component edges must be strictly acyclic, forming the Condensation DAG.",
                    "B": "Incorrect: Only edges between components exist.",
                    "C": "Incorrect: Edges remain strictly directed.",
                    "D": "Incorrect: If an inter-component cycle existed, those components would have merged into a single SCC."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day134-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Strongly Connected Components",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Find all Strongly Connected Components in a directed graph using Kosaraju's algorithm.",
        "subheading": "Implement and verify Strongly Connected Components in the interactive workspace.",
        "task": {
            "title": "Find all Strongly Connected Components in a directed graph using Kosaraju's algorithm.",
            "instructions": [
                "Find all Strongly Connected Components in a directed graph using Kosaraju's algorithm.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "def find_sccs(n: int, edges: list[list[int]]) -> list[list[int]]:\n    # TODO: Implement Kosaraju's 2-pass algorithm\n    return []\n\n# SCC 1: 0 -> 1 -> 2 -> 0; Edge: 2 -> 3; SCC 2: 3\nedges = [[0, 1], [1, 2], [2, 0], [2, 3]]\nprint('SCCs:', find_sccs(4, edges))\n",
            "solutionCode": "def find_sccs(n: int, edges: list[list[int]]) -> list[list[int]]:\n    adj = {i: [] for i in range(n)}\n    adj_rev = {i: [] for i in range(n)}\n    for u, v in edges:\n        adj[u].append(v)\n        adj_rev[v].append(u)\n    \n    stack = []\n    visited = [False] * n\n    def dfs1(u):\n        visited[u] = True\n        for v in adj[u]:\n            if not visited[v]:\n                dfs1(v)\n        stack.append(u)\n        \n    for i in range(n):\n        if not visited[i]:\n            dfs1(i)\n            \n    visited = [False] * n\n    sccs = []\n    while stack:\n        root = stack.pop()\n        if not visited[root]:\n            comp = []\n            def dfs2(u):\n                visited[u] = True\n                comp.append(u)\n                for v in adj_rev[u]:\n                    if not visited[v]:\n                        dfs2(v)\n            dfs2(root)\n            sccs.append(sorted(comp))\n    return sorted(sccs)\n\nedges = [[0, 1], [1, 2], [2, 0], [2, 3]]\nprint('SCCs:', find_sccs(4, edges))\n",
            "expectedOutputPatterns": [
                "SCCs: [[0, 1, 2], [3]]"
            ],
            "hint": "Pass 1: dfs on adj, push to stack on finish. Invert edges into adj_rev. Pass 2: pop from stack, if not visited in G^T, dfs on adj_rev to gather SCC component."
        },
        "keyTakeaway": "Successfully implemented and verified Strongly Connected Components!"
    },
    {
        "id": "day134-step5",
        "stepNumber": 5,
        "title": "Day 134 Complete: Strongly Connected Components (Kosaraju)",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 134,
        "heading": "Mastery Achieved: Strongly Connected Components (Kosaraju)",
        "subheading": "You have solidified key mental models and techniques for Strongly Connected Components.",
        "recapRows": [
            {
                "concept": "Transpose Graph Trapping",
                "naiveIntuition": "SCC requires checking all pairs reachability in O(V^3)",
                "pythonReality": "Two linear DFS passes on G and G^T decompose the graph into SCCs in optimal O(V + E) time"
            },
            {
                "concept": "Condensation DAG",
                "naiveIntuition": "Cyclic graphs cannot be topologically sorted",
                "pythonReality": "Collapsing SCCs produces a condensation DAG that CAN be topologically sorted, enabling dynamic programming on general directed graphs"
            }
        ],
        "solidifiedConcepts": [
            "Transpose Graph Reversal",
            "Kosaraju's Two-Pass DFS Algorithm"
        ],
        "nextDayPreview": {
            "dayNumber": 135,
            "title": "Section 11 Review & Graph Synthesis",
            "description": "Synthesize BFS, DFS, topological sorting, Dijkstra, DSU, MSTs, and SCC algorithms into a comprehensive network router."
        }
    }
]
},
  135: {
  "dayNumber": 135,
  "title": "Section 11 Review & Graph Synthesis",
  "topicName": "Graph Milestone",
  "sectionId": "graphs",
  "estimatedMinutes": 45,
  "difficulty": "ADVANCED",
  "prerequisites": [
    122,
    125,
    128,
    130,
    131,
    134
  ],
  "concepts": [
    "Shortest Path vs MST Selection",
    "Topological Pipeline Architecture",
    "Component Condensation"
  ],
  "practiceSkills": [
    "Graph Milestone Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Design a multi-modal routing engine integrating Dijkstra, BFS, and DSU under real-world constraints",
    "Condense directed cyclic graphs into topological DAG components"
  ],
  "practiceArchetype": "milestone",
  "flowTier": "tier3"
,
  "steps": [
    {
        "id": "day135-step1",
        "stepNumber": 1,
        "title": "Section 11 Review & Graph Synthesis: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Graph Milestone",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Graph Milestone.",
        "markdownContent": [
            "Section 11 Review synthesizes graph representations, BFS shortest path, 3-color DFS cycle detection, Topological Sort, Dijkstra, Bellman-Ford, DSU, Kruskal, Prim, Bipartite, Bridges, and SCCs into an algorithmic master blueprint.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Graph Milestone**, remember the central principle: Every graph algorithm matches specific edge constraints (weighted vs unweighted, directed vs undirected, positive vs negative)."
        ],
        "snippets": [
            {
                "title": "Graph Milestone Implementation Template",
                "code": "# Graph Master Selection Matrix:\n# BFS: Unweighted Shortest Path O(V + E)\n# Dijkstra: Non-negative Weighted Shortest Path O((V + E) log V)\n# Bellman-Ford: Arbitrary Weights + Negative Cycles O(V * E)\n# DSU: Dynamic Connectivity O(alpha(V))\n# Kruskal/Prim: MST O(E log V)",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Every graph algorithm matches specific edge constraints (weighted vs unweighted, directed vs undirected, positive vs negative)."
    },
    {
        "id": "day135-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Graph Milestone",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Graph Algorithm Selector: (1) Unweighted shortest path? BFS. (2) Topological dependency? Kahn's or DFS Topo. (3) Non-negative weighted shortest path? Dijkstra. (4) Negative weights/cycles? Bellman-Ford. (5) Disjoint connectivity / dynamic merges? DSU. (6) Minimum Spanning Tree? Kruskal (sparse) or Prim (dense). (7) 2-coloring? Bipartite BFS. (8) Critical edges? Tarjan's low-link bridges. (9) Mutual reachability? Kosaraju/Tarjan SCCs.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Every graph algorithm matches specific edge constraints (weighted vs unweighted, directed vs undirected, positive vs negative).\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Graph Milestone Core Invariant",
                "content": "Every graph algorithm matches specific edge constraints (weighted vs unweighted, directed vs undirected, positive vs negative)."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Every graph algorithm matches specific edge constraints (weighted vs unweighted, directed vs undirected, positive vs negative)."
    },
    {
        "id": "day135-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Graph Milestone",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d135-q1",
                "question": "You need to find the shortest delivery route in a city network with 50,000 intersections and 120,000 one-way streets with non-negative street lengths. Which algorithm is optimal?",
                "options": [
                    {
                        "id": "A",
                        "label": "Dijkstra's Algorithm with a Min-Heap, running in O((V + E) log V) time"
                    },
                    {
                        "id": "B",
                        "label": "Bellman-Ford Algorithm in O(V * E) time"
                    },
                    {
                        "id": "C",
                        "label": "Standard unweighted BFS"
                    },
                    {
                        "id": "D",
                        "label": "Kosaraju's Algorithm"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Non-negative weights on a sparse graph (120K edges on 50K vertices) are perfectly optimized by Dijkstra with a min-heap, resolving the route in milliseconds. Bellman-Ford would require ~6 billion operations.",
                    "B": "Incorrect: Bellman-Ford's O(V*E) would take minutes/hours.",
                    "C": "Incorrect: BFS ignores street lengths, giving incorrect route distances.",
                    "D": "Incorrect: Kosaraju finds strongly connected components, not shortest paths."
                }
            },
            {
                "id": "chk-d135-q2",
                "question": "Which algorithm determines whether an electrical power grid will split into disconnected islands if any single transmission line fails?",
                "options": [
                    {
                        "id": "A",
                        "label": "Tarjan's Bridge-Finding Algorithm in O(V + E) time"
                    },
                    {
                        "id": "B",
                        "label": "Dijkstra's Algorithm"
                    },
                    {
                        "id": "C",
                        "label": "Kahn's Topological Sort"
                    },
                    {
                        "id": "D",
                        "label": "Floyd-Warshall Algorithm"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! A transmission line whose removal splits the network into disconnected components is by definition a bridge edge, discovered in linear O(V + E) time by Tarjan's low-link algorithm.",
                    "B": "Incorrect: Dijkstra computes shortest path distances.",
                    "C": "Incorrect: Kahn's applies to directed acyclic dependencies.",
                    "D": "Incorrect: Floyd-Warshall computes all-pairs shortest paths in O(V^3)."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day135-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Graph Milestone",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Build an all-in-one Network Path Analyzer that finds the minimum latency route between servers using Dijkstra.",
        "subheading": "Implement and verify Graph Milestone in the interactive workspace.",
        "task": {
            "title": "Build an all-in-one Network Path Analyzer that finds the minimum latency route between servers using Dijkstra.",
            "instructions": [
                "Build an all-in-one Network Path Analyzer that finds the minimum latency route between servers using Dijkstra.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "import heapq\n\ndef analyze_network(n: int, connections: list[list[int]], src: int, dst: int) -> int:\n    # TODO: connections: [u, v, latency_ms]\n    # Find minimum latency from src to dst using Dijkstra\n    return -1\n\nconns = [[0, 1, 10], [0, 2, 3], [2, 1, 1], [1, 3, 5], [2, 3, 8]]\nprint('Min latency 0 -> 3:', analyze_network(4, conns, 0, 3))\n",
            "solutionCode": "import heapq\n\ndef analyze_network(n: int, connections: list[list[int]], src: int, dst: int) -> int:\n    adj = {i: [] for i in range(n)}\n    for u, v, w in connections:\n        adj[u].append((v, w))\n        adj[v].append((u, w))\n    \n    dist = [float('inf')] * n\n    dist[src] = 0\n    pq = [(0, src)]\n    while pq:\n        d, u = heapq.heappop(pq)\n        if d > dist[u]:\n            continue\n        if u == dst:\n            return d\n        for v, w in adj[u]:\n            if dist[u] + w < dist[v]:\n                dist[v] = dist[u] + w\n                heapq.heappush(pq, (dist[v], v))\n    return -1 if dist[dst] == float('inf') else dist[dst]\n\nconns = [[0, 1, 10], [0, 2, 3], [2, 1, 1], [1, 3, 5], [2, 3, 8]]\nprint('Min latency 0 -> 3:', analyze_network(4, conns, 0, 3))\n",
            "expectedOutputPatterns": [
                "Min latency 0 -> 3: 9"
            ],
            "hint": "Build undirected adj. dist = [inf]*n, dist[src] = 0, pq = [(0, src)]. While pq: pop d, u. If d > dist[u] continue. If u == dst return d. For v, w in adj[u]: if dist[u] + w < dist[v]: dist[v] = dist[u] + w, push (dist[v], v). Return -1."
        },
        "keyTakeaway": "Successfully implemented and verified Graph Milestone!"
    },
    {
        "id": "day135-step5",
        "stepNumber": 5,
        "title": "Day 135 Complete: Section 11 Review & Graph Synthesis",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 135,
        "heading": "Mastery Achieved: Section 11 Review & Graph Synthesis",
        "subheading": "You have solidified key mental models and techniques for Graph Milestone.",
        "recapRows": [
            {
                "concept": "Algorithm Invariant Alignment",
                "naiveIntuition": "One graph algorithm fits all scenarios",
                "pythonReality": "Selecting graph algorithms is an exact science dictated by edge weights, graph directionality, and output requirements"
            },
            {
                "concept": "Section 11 Synthesis",
                "naiveIntuition": "Graphs are disparate collection of independent tricks",
                "pythonReality": "All graph algorithms are state-space search variations over vertices and edges with specific pruning invariants"
            }
        ],
        "solidifiedConcepts": [
            "Shortest Path vs MST Selection",
            "Topological Pipeline Architecture",
            "Component Condensation"
        ],
        "nextDayPreview": {
            "dayNumber": 136,
            "title": "Greedy Choice Property & Exchange Arguments",
            "description": "Understand the Greedy Choice Property, Optimal Substructure, and prove optimality using exchange arguments."
        }
    }
]
},
  136: {
  "dayNumber": 136,
  "title": "Greedy Choice Property & Exchange Arguments",
  "topicName": "Greedy Foundations",
  "sectionId": "greedy-algorithms",
  "estimatedMinutes": 30,
  "difficulty": "ADVANCED",
  "prerequisites": [
    26,
    49
  ],
  "concepts": [
    "Greedy-Choice Property",
    "Exchange Argument Proof Technique"
  ],
  "practiceSkills": [
    "Greedy Foundations Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Evaluate whether locally optimal choices lead to globally optimal solutions",
    "Formulate exchange argument proofs showing no optimal solution beats greedy"
  ],
  "practiceArchetype": "tracing",
  "flowTier": "tier1"
,
  "steps": [
    {
        "id": "day136-step1",
        "stepNumber": 1,
        "title": "Greedy Choice Property & Exchange Arguments: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Greedy Foundations",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Greedy Foundations.",
        "markdownContent": [
            "Greedy Algorithms make the locally optimal choice at each decision step, arriving at the global optimum without backtracking when problems exhibit Optimal Substructure and the Greedy Choice Property.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Greedy Foundations**, remember the central principle: Greedy algorithms make irreversible local optimal choices; correctness requires formal proof via exchange arguments."
        ],
        "snippets": [
            {
                "title": "Greedy Foundations Implementation Template",
                "code": "# Greedy Coin Change (for Canonical Currency Systems like US cents [25, 10, 5, 1])\ndef min_coins_canonical(coins, amount):\n    coins.sort(reverse=True)\n    count = 0\n    for c in coins:\n        count += amount // c\n        amount %= c\n    return count",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Greedy algorithms make irreversible local optimal choices; correctness requires formal proof via exchange arguments."
    },
    {
        "id": "day136-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Greedy Foundations",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Unlike Dynamic Programming which considers multiple choices and memoizes subproblems, a greedy algorithm commits irreversibly to a single best immediate choice. Correctness must be mathematically proven using either the Exchange Argument or the 'Greedy Stays Ahead' induction technique.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Greedy algorithms make irreversible local optimal choices; correctness requires formal proof via exchange arguments.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Greedy Foundations Core Invariant",
                "content": "Greedy algorithms make irreversible local optimal choices; correctness requires formal proof via exchange arguments."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Greedy algorithms make irreversible local optimal choices; correctness requires formal proof via exchange arguments."
    },
    {
        "id": "day136-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Greedy Foundations",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d136-q1",
                "question": "Why does the greedy coin change algorithm succeed on standard currency [25, 10, 5, 1] but FAIL on arbitrary denominations like [4, 3, 1] for amount = 6?",
                "options": [
                    {
                        "id": "A",
                        "label": "Greedy picks 4 first, leaving 2, which requires two 1s (total 3 coins: 4+1+1), whereas the optimal global solution is two coins (3+3)"
                    },
                    {
                        "id": "B",
                        "label": "Because 6 is an even number"
                    },
                    {
                        "id": "C",
                        "label": "Because [4, 3, 1] has only 3 coin types"
                    },
                    {
                        "id": "D",
                        "label": "Because Python division truncates towards zero"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Canonical currencies have the property that larger denominations are multiples or combinations that never block better solutions. For [4, 3, 1], the greedy choice 4 irreversibly misses the global optimum 3 + 3.",
                    "B": "Incorrect: Parity does not determine greedy optimality.",
                    "C": "Incorrect: Number of denominations does not determine greedy properties.",
                    "D": "Incorrect: Truncation is standard integer arithmetic."
                }
            },
            {
                "id": "chk-d136-q2",
                "question": "What is the core idea of the 'Exchange Argument' in proving greedy algorithms?",
                "options": [
                    {
                        "id": "A",
                        "label": "Assume an arbitrary optimal solution exists, and prove that swapping its first difference with the greedy choice results in an equally good or better solution without losing feasibility"
                    },
                    {
                        "id": "B",
                        "label": "Swapping RAM memory with hard disk storage"
                    },
                    {
                        "id": "C",
                        "label": "Exchanging min-heaps for max-heaps"
                    },
                    {
                        "id": "D",
                        "label": "Proving that the algorithm runs in O(N log N)"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! The exchange argument starts with a hypothetical non-greedy optimal solution OPT. Step by step, it swaps choices in OPT with the greedy algorithm's choices, showing total cost does not worsen. Thus, greedy is as good as any optimal solution.",
                    "B": "Incorrect: Virtual memory swap is unrelated.",
                    "C": "Incorrect: Heap types are implementation details.",
                    "D": "Incorrect: Proof of correctness is distinct from time complexity."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day136-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Greedy Foundations",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Calculate minimum coins needed for an amount using standard canonical coins [25, 10, 5, 1].",
        "subheading": "Implement and verify Greedy Foundations in the interactive workspace.",
        "task": {
            "title": "Calculate minimum coins needed for an amount using standard canonical coins [25, 10, 5, 1].",
            "instructions": [
                "Calculate minimum coins needed for an amount using standard canonical coins [25, 10, 5, 1].",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "def min_canonical_coins(coins: list[int], amount: int) -> int:\n    # TODO: Implement greedy coin change for canonical currency\n    return 0\n\ncoins = [25, 10, 5, 1]\nprint('Coins for 41 cents:', min_canonical_coins(coins, 41)) # 4 (25 + 10 + 5 + 1)\nprint('Coins for 30 cents:', min_canonical_coins(coins, 30)) # 2 (25 + 5)\n",
            "solutionCode": "def min_canonical_coins(coins: list[int], amount: int) -> int:\n    coins_sorted = sorted(coins, reverse=True)\n    count = 0\n    rem = amount\n    for c in coins_sorted:\n        count += rem // c\n        rem %= c\n    return count\n\ncoins = [25, 10, 5, 1]\nprint('Coins for 41 cents:', min_canonical_coins(coins, 41))\nprint('Coins for 30 cents:', min_canonical_coins(coins, 30))\n",
            "expectedOutputPatterns": [
                "Coins for 41 cents: 4",
                "Coins for 30 cents: 2"
            ],
            "hint": "Sort coins descending. For each c: count += rem // c; rem %= c. Return count."
        },
        "keyTakeaway": "Successfully implemented and verified Greedy Foundations!"
    },
    {
        "id": "day136-step5",
        "stepNumber": 5,
        "title": "Day 136 Complete: Greedy Choice Property & Exchange Arguments",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 136,
        "heading": "Mastery Achieved: Greedy Choice Property & Exchange Arguments",
        "subheading": "You have solidified key mental models and techniques for Greedy Foundations.",
        "recapRows": [
            {
                "concept": "Greedy Choice Property",
                "naiveIntuition": "Greedy algorithms always work because they pick the biggest value",
                "pythonReality": "Greedy only produces globally optimal outcomes for problems possessing matroids or the exchange property; general optimization requires DP"
            },
            {
                "concept": "Canonical Currency Specificity",
                "naiveIntuition": "All coin change problems are greedy",
                "pythonReality": "Arbitrary coin systems require 1D Dynamic Programming because greedy choices can lock out superior combinations"
            }
        ],
        "solidifiedConcepts": [
            "Greedy-Choice Property",
            "Exchange Argument Proof Technique"
        ],
        "nextDayPreview": {
            "dayNumber": 137,
            "title": "Activity Selection & Interval Scheduling",
            "description": "Solve the Activity Selection problem by sorting on earliest finish time, proving optimality via exchange arguments."
        }
    }
]
},
  137: {
  "dayNumber": 137,
  "title": "Activity Selection & Interval Scheduling",
  "topicName": "Activity Selection",
  "sectionId": "greedy-algorithms",
  "estimatedMinutes": 35,
  "difficulty": "ADVANCED",
  "prerequisites": [
    49,
    136
  ],
  "concepts": [
    "Earliest Finishing Time Greedy Sort",
    "Non-Overlapping Choice Invariant"
  ],
  "practiceSkills": [
    "Activity Selection Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Sort intervals by earliest finish time to maximize non-overlapping scheduled tasks",
    "Prove greedy interval scheduling optimality in O(N log N) time"
  ],
  "practiceArchetype": "algorithm",
  "flowTier": "tier1"
,
  "steps": [
    {
        "id": "day137-step1",
        "stepNumber": 1,
        "title": "Activity Selection & Interval Scheduling: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Activity Selection",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Activity Selection.",
        "markdownContent": [
            "Activity Selection (Interval Scheduling) maximizes the number of non-overlapping intervals by greedily sorting intervals by EARLIEST FINISH TIME in O(N log N) time.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Activity Selection**, remember the central principle: Sorting intervals by earliest finish time leaves the maximal remaining time for future intervals."
        ],
        "snippets": [
            {
                "title": "Activity Selection Implementation Template",
                "code": "# Interval Scheduling (Max Non-overlapping Activities)\ndef max_activities(intervals):\n    intervals.sort(key=lambda x: x[1]) # Sort by end time\n    count = 0\n    last_end = float('-inf')\n    for s, e in intervals:\n        if s >= last_end:\n            count += 1\n            last_end = e\n    return count",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Sorting intervals by earliest finish time leaves the maximal remaining time for future intervals."
    },
    {
        "id": "day137-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Activity Selection",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Sort intervals `(start, end)` by `end` ascending. Select first interval, set `last_end = end`. Iterate through remaining intervals: if `start >= last_end`: select interval, update `last_end = end`. Proof: finishing earliest leaves the maximum remaining timeline for future tasks.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Sorting intervals by earliest finish time leaves the maximal remaining time for future intervals.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Activity Selection Core Invariant",
                "content": "Sorting intervals by earliest finish time leaves the maximal remaining time for future intervals."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Sorting intervals by earliest finish time leaves the maximal remaining time for future intervals."
    },
    {
        "id": "day137-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Activity Selection",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d137-q1",
                "question": "Why must intervals be sorted by EARLIEST FINISH TIME rather than earliest start time or shortest duration?",
                "options": [
                    {
                        "id": "A",
                        "label": "Finishing earliest frees the resource as soon as possible, leaving the maximum possible time window available to schedule future activities"
                    },
                    {
                        "id": "B",
                        "label": "Because start times cannot be compared in Python"
                    },
                    {
                        "id": "C",
                        "label": "Because shortest duration activities can conflict with two long activities"
                    },
                    {
                        "id": "D",
                        "label": "Because finish times are always integers"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Counterexample for start time: an activity starting at 0 and running to 100 blocks all others. Counterexample for shortest duration: a short activity in the middle blocks two activities on either side. Earliest finish time is proven optimal.",
                    "B": "Incorrect: Python compares any tuple elements.",
                    "C": "Incorrect: While true, A is the direct causal proof of finish time optimality.",
                    "D": "Incorrect: Start times are also numbers."
                }
            },
            {
                "id": "chk-d137-q2",
                "question": "What is the equivalent formulation for 'Minimum Number of Intervals to Remove to make remainder Non-overlapping'?",
                "options": [
                    {
                        "id": "A",
                        "label": "`total_intervals - max_non_overlapping_activities()`"
                    },
                    {
                        "id": "B",
                        "label": "`max_non_overlapping_activities() // 2`"
                    },
                    {
                        "id": "C",
                        "label": "`len(intervals) - 1`"
                    },
                    {
                        "id": "D",
                        "label": "Sum of all end times"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Maximizing the preserved non-overlapping intervals is the exact mathematical complement of minimizing the number of removed intervals. Total removals = N - max_preserved.",
                    "B": "Incorrect: Halving is arbitrary.",
                    "C": "Incorrect: Assumes all intervals overlap.",
                    "D": "Incorrect: Summing timestamps is meaningless."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day137-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Activity Selection",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Find the maximum number of mutually compatible activities that can be scheduled.",
        "subheading": "Implement and verify Activity Selection in the interactive workspace.",
        "task": {
            "title": "Find the maximum number of mutually compatible activities that can be scheduled.",
            "instructions": [
                "Find the maximum number of mutually compatible activities that can be scheduled.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "def max_compatible_intervals(intervals: list[list[int]]) -> int:\n    # TODO: Sort by finish time and select maximum non-overlapping intervals\n    return 0\n\n# Intervals: [1, 4], [3, 5], [0, 6], [5, 7], [3, 9], [5, 9], [6, 10], [8, 11], [8, 12], [2, 14], [12, 16]\nacts = [[1, 4], [3, 5], [0, 6], [5, 7], [3, 9], [5, 9], [6, 10], [8, 11], [8, 12], [2, 14], [12, 16]]\nprint('Max activities:', max_compatible_intervals(acts)) # 4 ([1, 4], [5, 7], [8, 11], [12, 16])\n",
            "solutionCode": "def max_compatible_intervals(intervals: list[list[int]]) -> int:\n    intervals_sorted = sorted(intervals, key=lambda x: x[1])\n    count = 0\n    last_end = float('-inf')\n    for s, e in intervals_sorted:\n        if s >= last_end:\n            count += 1\n            last_end = e\n    return count\n\nacts = [[1, 4], [3, 5], [0, 6], [5, 7], [3, 9], [5, 9], [6, 10], [8, 11], [8, 12], [2, 14], [12, 16]]\nprint('Max activities:', max_compatible_intervals(acts))\n",
            "expectedOutputPatterns": [
                "Max activities: 4"
            ],
            "hint": "Sort by lambda x: x[1]. Loop s, e: if s >= last_end: count += 1; last_end = e. Return count."
        },
        "keyTakeaway": "Successfully implemented and verified Activity Selection!"
    },
    {
        "id": "day137-step5",
        "stepNumber": 5,
        "title": "Day 137 Complete: Activity Selection & Interval Scheduling",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 137,
        "heading": "Mastery Achieved: Activity Selection & Interval Scheduling",
        "subheading": "You have solidified key mental models and techniques for Activity Selection.",
        "recapRows": [
            {
                "concept": "Earliest Deadline Principle",
                "naiveIntuition": "Sort intervals by start time",
                "pythonReality": "Sorting by start time fails on long tasks that start early; sorting by finish time greedily maximizes future resource availability"
            },
            {
                "concept": "Duality of Interval Problems",
                "naiveIntuition": "Deletion and selection need different algorithms",
                "pythonReality": "Max Non-Overlapping Intervals and Min Interval Removals are exact dual formulations of the same greedy sweep"
            }
        ],
        "solidifiedConcepts": [
            "Earliest Finishing Time Greedy Sort",
            "Non-Overlapping Choice Invariant"
        ],
        "nextDayPreview": {
            "dayNumber": 138,
            "title": "Fractional Knapsack & Value Density Sorting",
            "description": "Implement the Fractional Knapsack problem in O(N log N) time by greedily sorting items by value-to-weight density."
        }
    }
]
},
  138: {
  "dayNumber": 138,
  "title": "Fractional Knapsack & Value Density Sorting",
  "topicName": "Fractional Knapsack",
  "sectionId": "greedy-algorithms",
  "estimatedMinutes": 35,
  "difficulty": "ADVANCED",
  "prerequisites": [
    136
  ],
  "concepts": [
    "Value-to-Weight Ratio Density",
    "Continuous Item Partitioning"
  ],
  "practiceSkills": [
    "Fractional Knapsack Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Sort items by value-per-weight density to maximize total value in fractional knapsacks",
    "Contrast fractional greedy solvability with 0/1 integer knapsack NP-hardness"
  ],
  "practiceArchetype": "algorithm",
  "flowTier": "tier1"
,
  "steps": [
    {
        "id": "day138-step1",
        "stepNumber": 1,
        "title": "Fractional Knapsack & Value Density Sorting: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Fractional Knapsack",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Fractional Knapsack.",
        "markdownContent": [
            "Fractional Knapsack greedily takes items with the highest Value-to-Weight ratio (v/w) because items can be subdivided, whereas 0/1 Knapsack requires Dynamic Programming because indivisible items cause capacity wastage.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Fractional Knapsack**, remember the central principle: Fractional knapsack solves optimally via value/weight greedy sorting; 0/1 knapsack fails greedy and requires DP."
        ],
        "snippets": [
            {
                "title": "Fractional Knapsack Implementation Template",
                "code": "# Fractional Knapsack\ndef fractional_knapsack(items, capacity):\n    # items: (value, weight)\n    items.sort(key=lambda x: x[0] / x[1], reverse=True)\n    total_val = 0.0\n    rem = capacity\n    for v, w in items:\n        if rem >= w:\n            total_val += v; rem -= w\n        else:\n            total_val += v * (rem / w); break\n    return total_val",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Fractional knapsack solves optimally via value/weight greedy sorting; 0/1 knapsack fails greedy and requires DP."
    },
    {
        "id": "day138-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Fractional Knapsack",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Compute `ratio = val / weight` for each item. Sort items descending by ratio. For each item: if `capacity >= weight`: take all (`val`, subtract `weight`). Else: take fraction `capacity / weight * val`, fill knapsack to 0, break. Total time: O(N log N).",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Fractional knapsack solves optimally via value/weight greedy sorting; 0/1 knapsack fails greedy and requires DP.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Fractional Knapsack Core Invariant",
                "content": "Fractional knapsack solves optimally via value/weight greedy sorting; 0/1 knapsack fails greedy and requires DP."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Fractional knapsack solves optimally via value/weight greedy sorting; 0/1 knapsack fails greedy and requires DP."
    },
    {
        "id": "day138-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Fractional Knapsack",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d138-q1",
                "question": "Why does the greedy Value-to-Weight ratio strategy work for Fractional Knapsack but FAIL for 0/1 Knapsack?",
                "options": [
                    {
                        "id": "A",
                        "label": "In 0/1 Knapsack, items cannot be broken into fractions; taking the highest ratio item can leave unused capacity that cannot be filled by remaining large items, resulting in suboptimal total value"
                    },
                    {
                        "id": "B",
                        "label": "Because 0/1 Knapsack weights are always negative"
                    },
                    {
                        "id": "C",
                        "label": "Because Python cannot sort floats"
                    },
                    {
                        "id": "D",
                        "label": "Because fractional knapsack uses binary search"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Consider capacity 50. Item 1: v=60, w=10 (ratio 6). Item 2: v=100, w=20 (ratio 5). Item 3: v=120, w=30 (ratio 4). In 0/1, taking item 1 and 2 leaves 20 capacity, unable to fit item 3 (total 160). But taking item 2 and 3 yields total 220!",
                    "B": "Incorrect: Knapsack weights are positive.",
                    "C": "Incorrect: Python sorts floats accurately.",
                    "D": "Incorrect: Fractional knapsack is a simple sort."
                }
            },
            {
                "id": "chk-d138-q2",
                "question": "What is the time complexity of the Fractional Knapsack algorithm on N items?",
                "options": [
                    {
                        "id": "A",
                        "label": "O(N log N) to sort by ratio, followed by O(N) single pass"
                    },
                    {
                        "id": "B",
                        "label": "O(N * W) where W is capacity"
                    },
                    {
                        "id": "C",
                        "label": "O(2^N)"
                    },
                    {
                        "id": "D",
                        "label": "O(1)"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Computing ratios and sorting N items takes O(N log N). The greedy pass visits items sequentially until capacity is exhausted (O(N)). Overall: O(N log N).",
                    "B": "Incorrect: O(N * W) is the pseudo-polynomial DP bound for 0/1 Knapsack.",
                    "C": "Incorrect: O(2^N) is brute force enumeration.",
                    "D": "Incorrect: All items must be evaluated."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day138-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Fractional Knapsack",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Calculate the maximum total value obtainable in a Fractional Knapsack.",
        "subheading": "Implement and verify Fractional Knapsack in the interactive workspace.",
        "task": {
            "title": "Calculate the maximum total value obtainable in a Fractional Knapsack.",
            "instructions": [
                "Calculate the maximum total value obtainable in a Fractional Knapsack.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "def max_fractional_value(values: list[int], weights: list[int], capacity: int) -> float:\n    # TODO: Sort by value/weight ratio and greedily take items\n    return 0.0\n\nvals = [60, 100, 120]\nwts = [10, 20, 30]\ncap = 50\nprint('Max value:', max_fractional_value(vals, wts, cap)) # 240.0 (all of 1 & 2, 2/3 of 3)\n",
            "solutionCode": "def max_fractional_value(values: list[int], weights: list[int], capacity: int) -> float:\n    items = sorted(zip(values, weights), key=lambda x: x[0] / x[1], reverse=True)\n    total = 0.0\n    rem = capacity\n    for v, w in items:\n        if rem >= w:\n            total += v\n            rem -= w\n        else:\n            total += v * (rem / w)\n            break\n    return total\n\nvals = [60, 100, 120]\nwts = [10, 20, 30]\ncap = 50\nprint('Max value:', max_fractional_value(vals, wts, cap))\n",
            "expectedOutputPatterns": [
                "Max value: 240.0"
            ],
            "hint": "items = sorted(zip(values, weights), key=lambda x: x[0]/x[1], reverse=True). If rem >= w: total += v, rem -= w. Else: total += v * (rem / w), break. Return total."
        },
        "keyTakeaway": "Successfully implemented and verified Fractional Knapsack!"
    },
    {
        "id": "day138-step5",
        "stepNumber": 5,
        "title": "Day 138 Complete: Fractional Knapsack & Value Density Sorting",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 138,
        "heading": "Mastery Achieved: Fractional Knapsack & Value Density Sorting",
        "subheading": "You have solidified key mental models and techniques for Fractional Knapsack.",
        "recapRows": [
            {
                "concept": "Divisibility as Greedy Enabler",
                "naiveIntuition": "0/1 Knapsack can be solved with heuristics",
                "pythonReality": "Fractional flexibility enables continuous greedy optimization; discrete integer constraints introduce NP-hard combinatorial packing"
            },
            {
                "concept": "Density Sorting Metric",
                "naiveIntuition": "Sort by highest absolute value",
                "pythonReality": "Value density (value per unit weight) measures true economic efficiency per unit of constrained capacity"
            }
        ],
        "solidifiedConcepts": [
            "Value-to-Weight Ratio Density",
            "Continuous Item Partitioning"
        ],
        "nextDayPreview": {
            "dayNumber": 139,
            "title": "Huffman Coding & Optimal Prefix Trees",
            "description": "Construct optimal variable-length prefix codes using Huffman's algorithm with priority queues in O(N log N) time."
        }
    }
]
},
  139: {
  "dayNumber": 139,
  "title": "Huffman Coding & Optimal Prefix Trees",
  "topicName": "Huffman Coding",
  "sectionId": "greedy-algorithms",
  "estimatedMinutes": 45,
  "difficulty": "ADVANCED",
  "prerequisites": [
    113,
    136
  ],
  "concepts": [
    "Optimal Prefix Code Invariant",
    "Min-Heap Bottom-Up Tree Merging"
  ],
  "practiceSkills": [
    "Huffman Coding Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Construct an optimal prefix code tree by repeatedly merging the two least frequent nodes",
    "Generate variable-length binary encoding tables without prefix ambiguity"
  ],
  "practiceArchetype": "algorithm",
  "flowTier": "tier3"
,
  "steps": [
    {
        "id": "day139-step1",
        "stepNumber": 1,
        "title": "Huffman Coding & Optimal Prefix Trees: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Huffman Coding",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Huffman Coding.",
        "markdownContent": [
            "Huffman Coding generates optimal prefix-free variable-length binary codes for lossless data compression using a Min-Heap to build a binary tree bottom-up.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Huffman Coding**, remember the central principle: More frequent characters receive shorter bit codes, minimizing expected file size without prefix ambiguity."
        ],
        "snippets": [
            {
                "title": "Huffman Coding Implementation Template",
                "code": "# Huffman Coding Tree Construction\nimport heapq\ndef huffman_tree(char_freqs):\n    pq = [[freq, [char, '']] for char, freq in char_freqs.items()]\n    heapq.heapify(pq)\n    while len(pq) > 1:\n        lo = heapq.heappop(pq)\n        hi = heapq.heappop(pq)\n        for pair in lo[1:]: pair[1] = '0' + pair[1]\n        for pair in hi[1:]: pair[1] = '1' + pair[1]\n        heapq.heappush(pq, [lo[0] + hi[0]] + lo[1:] + hi[1:])\n    return sorted(heapq.heappop(pq)[1:], key=lambda p: (len(p[1]), p))\n",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "More frequent characters receive shorter bit codes, minimizing expected file size without prefix ambiguity."
    },
    {
        "id": "day139-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Huffman Coding",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Count character frequencies. Push each character as a leaf node `(freq, char)` into a min-heap. Repeatedly pop the two lowest frequency nodes, merge them into an internal parent node with `freq = f1 + f2`, and push back into heap. Repeat until one root tree remains. Path left is '0', path right is '1'.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: More frequent characters receive shorter bit codes, minimizing expected file size without prefix ambiguity.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Huffman Coding Core Invariant",
                "content": "More frequent characters receive shorter bit codes, minimizing expected file size without prefix ambiguity."
            }
        ],
        "keyTakeaway": "Operational invariant locked: More frequent characters receive shorter bit codes, minimizing expected file size without prefix ambiguity."
    },
    {
        "id": "day139-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Huffman Coding",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d139-q1",
                "question": "What does it mean for Huffman Codes to be 'Prefix-Free'?",
                "options": [
                    {
                        "id": "A",
                        "label": "No character's binary code is a prefix of any other character's code, allowing continuous stream decoding without delimiter markers"
                    },
                    {
                        "id": "B",
                        "label": "All codes start with '0'"
                    },
                    {
                        "id": "C",
                        "label": "All codes have the exact same length (e.g. 8 bits)"
                    },
                    {
                        "id": "D",
                        "label": "The code contains no vowels"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! In a prefix-free code, if 'a' is '0' and 'b' is '10', encountering '0' immediately and uniquely identifies 'a'. Because every symbol corresponds to a leaf in the binary tree, no code can be a prefix of another.",
                    "B": "Incorrect: Codes branch with both '0' and '1'.",
                    "C": "Incorrect: Fixed-length codes are standard ASCII/Unicode, not variable-length Huffman codes.",
                    "D": "Incorrect: Codes represent any byte symbol."
                }
            },
            {
                "id": "chk-d139-q2",
                "question": "What is the time complexity to build a Huffman Tree for an alphabet of K unique characters using a min-heap?",
                "options": [
                    {
                        "id": "A",
                        "label": "O(K log K)"
                    },
                    {
                        "id": "B",
                        "label": "O(K^2)"
                    },
                    {
                        "id": "C",
                        "label": "O(2^K)"
                    },
                    {
                        "id": "D",
                        "label": "O(1)"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Initially building the heap takes O(K). There are K - 1 merge steps, each performing two heappops and one heappush on a heap of size <= K, costing O(log K). Total: O(K log K).",
                    "B": "Incorrect: Min-heap avoids quadratic scans.",
                    "C": "Incorrect: Tree construction is strictly polynomial.",
                    "D": "Incorrect: Every character must be merged."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day139-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Huffman Coding",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Calculate total encoded bit length of a message using Huffman coding frequencies.",
        "subheading": "Implement and verify Huffman Coding in the interactive workspace.",
        "task": {
            "title": "Calculate total encoded bit length of a message using Huffman coding frequencies.",
            "instructions": [
                "Calculate total encoded bit length of a message using Huffman coding frequencies.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "import heapq\nfrom collections import Counter\n\ndef huffman_encoded_length(text: str) -> int:\n    # TODO: Build Huffman tree and return total bits: sum(freq * code_length)\n    return 0\n\nmsg = 'abracadabra'\nprint('Total bits:', huffman_encoded_length(msg))\n",
            "solutionCode": "import heapq\nfrom collections import Counter\n\ndef huffman_encoded_length(text: str) -> int:\n    if not text:\n        return 0\n    counts = Counter(text)\n    if len(counts) == 1:\n        return len(text)\n    # (freq, unique_id, [char_list])\n    heap = [[freq, [ch]] for ch, freq in counts.items()]\n    heapq.heapify(heap)\n    code_lens = {ch: 0 for ch in counts}\n    while len(heap) > 1:\n        f1, chs1 = heapq.heappop(heap)\n        f2, chs2 = heapq.heappop(heap)\n        for ch in chs1:\n            code_lens[ch] += 1\n        for ch in chs2:\n            code_lens[ch] += 1\n        heapq.heappush(heap, [f1 + f2, chs1 + chs2])\n    return sum(counts[ch] * code_lens[ch] for ch in counts)\n\nmsg = 'abracadabra'\nprint('Total bits:', huffman_encoded_length(msg))\n",
            "expectedOutputPatterns": [
                "Total bits: 23"
            ],
            "hint": "Count frequencies. Merge lowest two groups in min-heap, incrementing code length by 1 for characters in both groups. Return sum(counts[ch] * code_lens[ch])."
        },
        "keyTakeaway": "Successfully implemented and verified Huffman Coding!"
    },
    {
        "id": "day139-step5",
        "stepNumber": 5,
        "title": "Day 139 Complete: Huffman Coding & Optimal Prefix Trees",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 139,
        "heading": "Mastery Achieved: Huffman Coding & Optimal Prefix Trees",
        "subheading": "You have solidified key mental models and techniques for Huffman Coding.",
        "recapRows": [
            {
                "concept": "Frequency Inversion Coding",
                "naiveIntuition": "Assign fixed 8-bit bytes to all characters",
                "pythonReality": "Frequent characters ('e', 'a') receive 1-3 bit codes; rare characters ('z', 'q') receive 8+ bit codes, drastically reducing average file size"
            },
            {
                "concept": "Leaf Node Uniqueness",
                "naiveIntuition": "Prefix codes need end-of-character markers",
                "pythonReality": "Placing all characters exclusively at leaf nodes mathematically guarantees prefix-free decodability without delimiters"
            }
        ],
        "solidifiedConcepts": [
            "Optimal Prefix Code Invariant",
            "Min-Heap Bottom-Up Tree Merging"
        ],
        "nextDayPreview": {
            "dayNumber": 140,
            "title": "Jump Game & Reachability Frontiers",
            "description": "Solve Jump Game I (reachability) and Jump Game II (minimum jumps) using greedy frontier advancement in O(N) time."
        }
    }
]
},
  140: {
  "dayNumber": 140,
  "title": "Jump Game & Reachability Frontiers",
  "topicName": "Reachability Greedy",
  "sectionId": "greedy-algorithms",
  "estimatedMinutes": 35,
  "difficulty": "ADVANCED",
  "prerequisites": [
    43,
    136
  ],
  "concepts": [
    "Max Reachability Frontier Invariant",
    "Boundary Jump Step Increments"
  ],
  "practiceSkills": [
    "Reachability Greedy Implementation",
    "Invariant Verification",
    "Complexity Analysis"
  ],
  "learningObjectives": [
    "Track maximum reachable index frontiers to determine if array ends are reachable in O(N) time",
    "Compute minimum jumps to reach the end using greedy interval boundary shifts"
  ],
  "practiceArchetype": "problem",
  "flowTier": "tier2"
,
  "steps": [
    {
        "id": "day140-step1",
        "stepNumber": 1,
        "title": "Jump Game & Reachability Frontiers: Foundations",
        "shortLabel": "Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Intuition & Core Principles: Reachability Greedy",
        "subheading": "Understand the core intuition, mental model, and foundational motivation for Reachability Greedy.",
        "markdownContent": [
            "Jump Game I (Reachability) and Jump Game II (Minimum Jumps) greedily track the furthest reachable index in linear O(N) time.",
            "### Foundational Mental Model\nWhen approaching problems requiring **Reachability Greedy**, remember the central principle: Greedy jump algorithms track the furthest reachable frontier, updating jump counts only when crossing previous boundaries."
        ],
        "snippets": [
            {
                "title": "Reachability Greedy Implementation Template",
                "code": "# Jump Game II (Min Jumps)\ndef min_jumps(nums):\n    jumps = 0\n    curr_end = 0\n    farthest = 0\n    for i in range(len(nums) - 1):\n        farthest = max(farthest, i + nums[i])\n        if i == curr_end:\n            jumps += 1\n            curr_end = farthest\n    return jumps",
                "language": "python"
            }
        ],
        "callouts": [],
        "keyTakeaway": "Greedy jump algorithms track the furthest reachable frontier, updating jump counts only when crossing previous boundaries."
    },
    {
        "id": "day140-step2",
        "stepNumber": 2,
        "title": "Mechanics & Invariants",
        "shortLabel": "Mechanics",
        "type": "explanation",
        "isGated": false,
        "heading": "Operational Invariants & Complexity: Reachability Greedy",
        "subheading": "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
        "markdownContent": [
            "Jump Game I: maintain `max_reach = max(max_reach, i + nums[i])`. If `i > max_reach`: cannot advance (return False). Return True if `max_reach >= n - 1`. Jump Game II: maintain `curr_end` (boundary of current jump) and `farthest`. When `i == curr_end`: `jumps += 1; curr_end = farthest`.",
            "### Complexity & Correctness Invariants\n- **Core Invariant**: Greedy jump algorithms track the furthest reachable frontier, updating jump counts only when crossing previous boundaries.\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
        ],
        "snippets": [],
        "callouts": [
            {
                "type": "tip",
                "title": "Reachability Greedy Core Invariant",
                "content": "Greedy jump algorithms track the furthest reachable frontier, updating jump counts only when crossing previous boundaries."
            }
        ],
        "keyTakeaway": "Operational invariant locked: Greedy jump algorithms track the furthest reachable frontier, updating jump counts only when crossing previous boundaries."
    },
    {
        "id": "day140-step3",
        "stepNumber": 3,
        "title": "Knowledge Check: Reachability Greedy",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Evaluate Conceptual Mastery & Edge Cases",
        "subheading": "Verify your understanding of algorithmic bounds and mechanics before coding.",
        "checkpoints": [
            {
                "id": "chk-d140-q1",
                "question": "In Jump Game I, why does `if i > max_reach:` prove that the last index can never be reached?",
                "options": [
                    {
                        "id": "A",
                        "label": "Index `i` is beyond the furthest position reachable from any preceding index, meaning the learner has encountered an impassable gap"
                    },
                    {
                        "id": "B",
                        "label": "Because nums[i] is negative"
                    },
                    {
                        "id": "C",
                        "label": "Because i reached the end of the array"
                    },
                    {
                        "id": "D",
                        "label": "Because max_reach was reset to 0"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! If the loop index `i` exceeds `max_reach`, no sequence of jumps from index 0 to i-1 can ever reach index `i` or beyond. It is impossible to advance further.",
                    "B": "Incorrect: Jumps are non-negative integers.",
                    "C": "Incorrect: End of array is n - 1.",
                    "D": "Incorrect: max_reach is monotonically non-decreasing."
                }
            },
            {
                "id": "chk-d140-q2",
                "question": "Why does the loop in Jump Game II iterate up to `len(nums) - 1` rather than `len(nums)`?",
                "options": [
                    {
                        "id": "A",
                        "label": "Once you reach the final index `n - 1`, no additional jump is required to reach the destination; processing `n - 1` would erroneously trigger `jumps += 1`"
                    },
                    {
                        "id": "B",
                        "label": "To prevent an IndexError"
                    },
                    {
                        "id": "C",
                        "label": "Because the last index is always 0"
                    },
                    {
                        "id": "D",
                        "label": "Python loops require n - 1"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! If `curr_end` happens to be at `n - 1`, landing on `n - 1` means you have already arrived. Checking `i == curr_end` on the final element would incorrectly charge for another jump.",
                    "B": "Incorrect: Indexing is valid up to n - 1.",
                    "C": "Incorrect: Final element value is arbitrary.",
                    "D": "Incorrect: Standard range limit logic."
                }
            }
        ],
        "keyTakeaway": "Checkpoint verified! You are ready for the coding challenge."
    },
    {
        "id": "day140-step4",
        "stepNumber": 4,
        "title": "Guided Practice: Reachability Greedy",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Determine minimum jumps required to reach the last index in an array.",
        "subheading": "Implement and verify Reachability Greedy in the interactive workspace.",
        "task": {
            "title": "Determine minimum jumps required to reach the last index in an array.",
            "instructions": [
                "Determine minimum jumps required to reach the last index in an array.",
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            "starterCode": "def jump(nums: list[int]) -> int:\n    # TODO: Implement Jump Game II in O(N) time and O(1) space\n    return 0\n\nprint('Min jumps [2,3,1,1,4]:', jump([2, 3, 1, 1, 4])) # 2 (0 -> 1 -> 4)\nprint('Min jumps [2,3,0,1,4]:', jump([2, 3, 0, 1, 4])) # 2\n",
            "solutionCode": "def jump(nums: list[int]) -> int:\n    jumps = 0\n    curr_end = 0\n    farthest = 0\n    for i in range(len(nums) - 1):\n        farthest = max(farthest, i + nums[i])\n        if i == curr_end:\n            jumps += 1\n            curr_end = farthest\n    return jumps\n\nprint('Min jumps [2,3,1,1,4]:', jump([2, 3, 1, 1, 4]))\nprint('Min jumps [2,3,0,1,4]:', jump([2, 3, 0, 1, 4]))\n",
            "expectedOutputPatterns": [
                "Min jumps [2,3,1,1,4]: 2",
                "Min jumps [2,3,0,1,4]: 2"
            ],
            "hint": "Track jumps = 0, curr_end = 0, farthest = 0. Loop i in range(len(nums) - 1): farthest = max(farthest, i + nums[i]); if i == curr_end: jumps += 1, curr_end = farthest. Return jumps."
        },
        "keyTakeaway": "Successfully implemented and verified Reachability Greedy!"
    },
    {
        "id": "day140-step5",
        "stepNumber": 5,
        "title": "Day 140 Complete: Jump Game & Reachability Frontiers",
        "shortLabel": "Mastery",
        "type": "completion",
        "isGated": false,
        "dayNumber": 140,
        "heading": "Mastery Achieved: Jump Game & Reachability Frontiers",
        "subheading": "You have solidified key mental models and techniques for Reachability Greedy.",
        "recapRows": [
            {
                "concept": "Implicit BFS Levels",
                "naiveIntuition": "Use BFS or DP (O(N^2)) to check all landing spots",
                "pythonReality": "curr_end marks the boundary of the current BFS level; greedy frontier tracking collapses BFS to O(N) time and O(1) space"
            },
            {
                "concept": "Horizon Expansion",
                "naiveIntuition": "Pick the jump that has the biggest number",
                "pythonReality": "Greedily optimize the reach horizon i + nums[i], not the local jump size nums[i]"
            }
        ],
        "solidifiedConcepts": [
            "Max Reachability Frontier Invariant",
            "Boundary Jump Step Increments"
        ],
        "nextDayPreview": {
            "dayNumber": 141,
            "title": "Partition Labels & Last Seen Indices",
            "description": "Partition strings into maximal parts such that each character appears in at most one part in O(N) time."
        }
    }
]
},
};
