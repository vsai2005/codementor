"""
Practice Problems for Section 11 (Advanced Graph Algorithms)
Total problems: 7
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

SEC11_GRAPHS_PROBLEMS = [
    P(
        "course-schedule-ii", "Course Schedule II (Topological Sort)", "graphs", 4, "find_order",
        "There are a total of `num_courses` courses labeled from `0` to `num_courses - 1`. You are given an array `prerequisites` where `prerequisites[i] = [a_i, b_i]` indicates that you must take course `b_i` before `a_i`.\n\nReturn the ordering of courses you should take to finish all courses. If it is impossible to finish all courses, return an empty array `[]`.",
        "- `1 <= num_courses <= 2000`\n- `0 <= len(prerequisites) <= 5000`",
        "O(V + E)", "O(V + E)",
        "def find_order(num_courses: int, prerequisites: list[list[int]]) -> list[int]:\n    pass\n",
        [
            {"args": [2, [[1, 0]]], "expected": [0, 1]},
            {"args": [4, [[1, 0], [2, 0], [3, 1], [3, 2]]], "expected": [0, 1, 2, 3]},
            {"args": [1, []], "expected": [0]},
            {"args": [2, [[1, 0], [0, 1]]], "expected": []}
        ],
        "from collections import deque, defaultdict\n\ndef find_order(num_courses: int, prerequisites: list[list[int]]) -> list[int]:\n    adj = defaultdict(list)\n    in_degree = [0] * num_courses\n    for dest, src in prerequisites:\n        adj[src].append(dest)\n        in_degree[dest] += 1\n    q = deque([i for i in range(num_courses) if in_degree[i] == 0])\n    order = []\n    while q:\n        curr = q.popleft()\n        order.append(curr)\n        for nxt in adj[curr]:\n            in_degree[nxt] -= 1\n            if in_degree[nxt] == 0:\n                q.append(nxt)\n    return order if len(order) == num_courses else []\n"
    ),

    P(
        "is-graph-bipartite", "Is Graph Bipartite? (2-Coloring)", "graphs", 3, "is_bipartite",
        "There is an undirected graph with `n` nodes, where each node is numbered between `0` and `n - 1`. You are given a 2D array `graph`, where `graph[u]` is an array of nodes that node `u` is adjacent to.\n\nReturn `True` if and only if it is bipartite (2-colorable).",
        "- `graph.length == n`\n- `1 <= n <= 100`\n- `0 <= graph[u].length < n`",
        "O(V + E)", "O(V)",
        "def is_bipartite(graph: list[list[int]]) -> bool:\n    pass\n",
        [
            {"args": [[[1, 2, 3], [0, 2], [0, 1, 3], [0, 2]]], "expected": False},
            {"args": [[[1, 3], [0, 2], [1, 3], [0, 2]]], "expected": True},
            {"args": [[[]]], "expected": True},
            {"args": [[[1], [0]]], "expected": True}
        ],
        "def is_bipartite(graph: list[list[int]]) -> bool:\n    color = {}\n    for node in range(len(graph)):\n        if node not in color:\n            color[node] = 0\n            q = [node]\n            while q:\n                curr = q.pop(0)\n                for neighbor in graph[curr]:\n                    if neighbor not in color:\n                        color[neighbor] = 1 - color[curr]\n                        q.append(neighbor)\n                    elif color[neighbor] == color[curr]:\n                        return False\n    return True\n"
    ),

    P(
        "network-delay-time", "Network Delay Time (Dijkstra's Algorithm)", "graphs", 3, "network_delay_time",
        "You are given a network of `n` nodes labeled `1` to `n`. `times[i] = [u, v, w]` represents the travel time from node `u` to node `v`. We send a signal from node `k`. Return the minimum time needed for all `n` nodes to receive the signal. If it is impossible, return `-1`.\n\nUse Dijkstra's algorithm with a min-heap.",
        "- `1 <= k <= n <= 100`\n- `1 <= len(times) <= 6000`\n- `0 <= w <= 100`",
        "O((V + E) log V)", "O(V + E)",
        "def network_delay_time(times: list[list[int]], n: int, k: int) -> int:\n    pass\n",
        [
            {"args": [[[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2], "expected": 2},
            {"args": [[[1, 2, 1]], 2, 1], "expected": 1},
            {"args": [[[1, 2, 1]], 2, 2], "expected": -1},
            {"args": [[[1, 2, 1], [2, 3, 2], [1, 3, 4]], 3, 1], "expected": 3}
        ],
        "import heapq\nfrom collections import defaultdict\n\ndef network_delay_time(times: list[list[int]], n: int, k: int) -> int:\n    adj = defaultdict(list)\n    for u, v, w in times:\n        adj[u].append((v, w))\n    heap = [(0, k)]\n    dist = {}\n    while heap:\n        d, u = heapq.heappop(heap)\n        if u in dist:\n            continue\n        dist[u] = d\n        for v, w in adj[u]:\n            if v not in dist:\n                heapq.heappush(heap, (d + w, v))\n    return max(dist.values()) if len(dist) == n else -1\n"
    ),

    P(
        "cheapest-flights-within-k-stops", "Cheapest Flights Within K Stops (Bellman-Ford)", "graphs", 4, "find_cheapest_price",
        "There are `n` cities connected by some number of flights. You are given an array `flights` where `flights[i] = [from_i, to_i, price_i]`.\n\nYou are also given three integers `src`, `dst`, and `k`, return the cheapest price from `src` to `dst` with at most `k` stops. If there is no such route, return `-1`.",
        "- `1 <= n <= 100`\n- `0 <= len(flights) <= (n * (n - 1) / 2)`\n- `0 <= k < n`",
        "O(k * E)", "O(V)",
        "def find_cheapest_price(n: int, flights: list[list[int]], src: int, dst: int, k: int) -> int:\n    pass\n",
        [
            {"args": [4, [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]], 0, 3, 1], "expected": 700},
            {"args": [3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 1], "expected": 200},
            {"args": [3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 0], "expected": 500}
        ],
        "def find_cheapest_price(n: int, flights: list[list[int]], src: int, dst: int, k: int) -> int:\n    prices = [float('inf')] * n\n    prices[src] = 0\n    for _ in range(k + 1):\n        temp = list(prices)\n        for u, v, p in flights:\n            if prices[u] != float('inf') and prices[u] + p < temp[v]:\n                temp[v] = prices[u] + p\n        prices = temp\n    return prices[dst] if prices[dst] != float('inf') else -1\n"
    ),

    P(
        "redundant-connection", "Redundant Connection (DSU Union-Find)", "graphs", 3, "find_redundant_connection",
        "In this problem, a tree is an undirected graph that is connected and has no cycles. You are given a graph that started as a tree with `n` nodes labeled `1` to `n`, with one additional edge added. Return an edge that can be removed so that the resulting graph is a tree of `n` nodes.\n\nSolve using Disjoint Set Union (DSU) with path compression.",
        "- `n == len(edges)`\n- `3 <= n <= 1000`",
        "O(n * alpha(n))", "O(n)",
        "def find_redundant_connection(edges: list[list[int]]) -> list[int]:\n    pass\n",
        [
            {"args": [[[1, 2], [1, 3], [2, 3]]], "expected": [2, 3]},
            {"args": [[[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]], "expected": [1, 4]},
            {"args": [[[1, 3], [3, 4], [1, 4], [1, 5]]], "expected": [1, 4]}
        ],
        "def find_redundant_connection(edges: list[list[int]]) -> list[int]:\n    parent = list(range(len(edges) + 1))\n    def find(i):\n        if parent[i] != i:\n            parent[i] = find(parent[i])\n        return parent[i]\n    for u, v in edges:\n        root_u = find(u)\n        root_v = find(v)\n        if root_u == root_v:\n            return [u, v]\n        parent[root_u] = root_v\n    return []\n"
    ),

    P(
        "min-cost-to-connect-all-points", "Min Cost to Connect All Points (Kruskal's MST)", "graphs", 4, "min_cost_connect_points",
        "You are given an array `points` representing integer coordinates of some points on a 2D plane. The cost of connecting two points `[x_i, y_i]` and `[x_j, y_j]` is the Manhattan distance: `|x_i - x_j| + |y_i - y_j|`.\n\nReturn the minimum cost to make all points connected (Minimum Spanning Tree).",
        "- `1 <= len(points) <= 1000`\n- `-10^6 <= x_i, y_i <= 10^6`",
        "O(E log E)", "O(V + E)",
        "def min_cost_connect_points(points: list[list[int]]) -> int:\n    pass\n",
        [
            {"args": [[[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]]], "expected": 20},
            {"args": [[[3, 12], [-2, 5], [-4, 1]]], "expected": 18},
            {"args": [[[0, 0]]], "expected": 0}
        ],
        "def min_cost_connect_points(points: list[list[int]]) -> int:\n    n = len(points)\n    edges = []\n    for i in range(n):\n        for j in range(i + 1, n):\n            dist = abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1])\n            edges.append((dist, i, j))\n    edges.sort()\n    parent = list(range(n))\n    def find(i):\n        if parent[i] != i:\n            parent[i] = find(parent[i])\n        return parent[i]\n    total_cost = 0\n    edges_count = 0\n    for dist, u, v in edges:\n        ru = find(u)\n        rv = find(v)\n        if ru != rv:\n            parent[ru] = rv\n            total_cost += dist\n            edges_count += 1\n            if edges_count == n - 1:\n                break\n    return total_cost\n"
    ),

    P(
        "critical-connections-in-a-network", "Critical Connections (Tarjan's Bridges)", "graphs", 5, "critical_connections",
        "There are `n` servers numbered `0` to `n - 1` connected by undirected server-to-server `connections`. Return all critical connections in the network in any order. An edge is a critical connection (bridge) if removing it will make some servers unable to reach each other.\n\nSort each connection `[u, v]` with `u < v`, and sort the outer list.",
        "- `2 <= n <= 10^5`\n- `n - 1 <= len(connections) <= 10^5`",
        "O(V + E)", "O(V + E)",
        "def critical_connections(n: int, connections: list[list[int]]) -> list[list[int]]:\n    pass\n",
        [
            {"args": [4, [[0, 1], [1, 2], [2, 0], [1, 3]]], "expected": [[1, 3]]},
            {"args": [2, [[0, 1]]], "expected": [[0, 1]]},
            {"args": [5, [[1, 0], [2, 0], [3, 2], [4, 2], [4, 3], [3, 0], [4, 0]]], "expected": [[0, 1]]}
        ],
        "from collections import defaultdict\n\ndef critical_connections(n: int, connections: list[list[int]]) -> list[list[int]]:\n    adj = defaultdict(list)\n    for u, v in connections:\n        adj[u].append(v)\n        adj[v].append(u)\n    disc = [-1] * n\n    low = [-1] * n\n    bridges = []\n    time = 0\n    def dfs(u, p):\n        nonlocal time\n        disc[u] = low[u] = time\n        time += 1\n        for v in adj[u]:\n            if v == p:\n                continue\n            if disc[v] != -1:\n                low[u] = min(low[u], disc[v])\n            else:\n                dfs(v, u)\n                low[u] = min(low[u], low[v])\n                if low[v] > disc[u]:\n                    bridges.append(sorted([u, v]))\n    for i in range(n):\n        if disc[i] == -1:\n            dfs(i, -1)\n    bridges.sort()\n    return bridges\n"
    )
]
