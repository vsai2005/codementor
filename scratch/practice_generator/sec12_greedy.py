"""
Practice Problems for Section 12 (Greedy Algorithms)
Total problems: 8
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

SEC12_GREEDY_PROBLEMS = [
    P(
        "non-overlapping-intervals", "Non-overlapping Intervals (Interval Scheduling)", "greedy", 3, "erase_overlap_intervals",
        "Given an array of intervals `intervals` where `intervals[i] = [start_i, end_i]`, return the minimum number of intervals you need to remove to make the rest of the intervals non-overlapping.\n\nUse earliest finish time greedy choice.",
        "- `1 <= len(intervals) <= 10^5`\n- `intervals[i].length == 2`",
        "O(n log n)", "O(1)",
        "def erase_overlap_intervals(intervals: list[list[int]]) -> int:\n    pass\n",
        [
            {"args": [[[1, 2], [2, 3], [3, 4], [1, 3]]], "expected": 1},
            {"args": [[[1, 2], [1, 2], [1, 2]]], "expected": 2},
            {"args": [[[1, 2], [2, 3]]], "expected": 0},
            {"args": [[[1, 100], [11, 22], [1, 11], [2, 12]]], "expected": 2}
        ],
        "def erase_overlap_intervals(intervals: list[list[int]]) -> int:\n    if not intervals:\n        return 0\n    intervals.sort(key=lambda x: x[1])\n    end = intervals[0][1]\n    count = 0\n    for i in range(1, len(intervals)):\n        if intervals[i][0] < end:\n            count += 1\n        else:\n            end = intervals[i][1]\n    return count\n"
    ),

    P(
        "maximum-units-on-a-truck", "Maximum Units on a Truck (Fractional Greedy)", "greedy", 1, "maximum_units",
        "You are assigned to put some amount of boxes onto one truck. You are given a 2D array `box_types`, where `box_types[i] = [number_of_boxes_i, number_of_units_per_box_i]`. You are also given an integer `truck_size`, which is the maximum number of boxes that can be put on the truck.\n\nReturn the maximum total number of units that can be put on the truck.",
        "- `1 <= len(box_types) <= 1000`\n- `1 <= truck_size <= 10^6`",
        "O(n log n)", "O(1)",
        "def maximum_units(box_types: list[list[int]], truck_size: int) -> int:\n    pass\n",
        [
            {"args": [[[1, 3], [2, 2], [3, 1]], 4], "expected": 8},
            {"args": [[[5, 10], [2, 5], [4, 7], [3, 9]], 10], "expected": 91},
            {"args": [[[1, 1]], 0], "expected": 0}
        ],
        "def maximum_units(box_types: list[list[int]], truck_size: int) -> int:\n    box_types.sort(key=lambda x: x[1], reverse=True)\n    total_units = 0\n    for count, units in box_types:\n        take = min(truck_size, count)\n        total_units += take * units\n        truck_size -= take\n        if truck_size == 0:\n            break\n    return total_units\n"
    ),

    P(
        "jump-game", "Jump Game (Reachability Frontier)", "greedy", 2, "can_jump",
        "You are given an integer array `nums`. You are initially positioned at the array's first index, and each element in the array represents your maximum jump length at that position.\n\nReturn `True` if you can reach the last index, or `False` otherwise.",
        "- `1 <= len(nums) <= 10^4`\n- `0 <= nums[i] <= 10^5`",
        "O(n)", "O(1)",
        "def can_jump(nums: list[int]) -> bool:\n    pass\n",
        [
            {"args": [[2, 3, 1, 1, 4]], "expected": True},
            {"args": [[3, 2, 1, 0, 4]], "expected": False},
            {"args": [[0]], "expected": True},
            {"args": [[2, 0, 0]], "expected": True}
        ],
        "def can_jump(nums: list[int]) -> bool:\n    max_reach = 0\n    for i, jump in enumerate(nums):\n        if i > max_reach:\n            return False\n        max_reach = max(max_reach, i + jump)\n    return True\n"
    ),

    P(
        "jump-game-ii", "Jump Game II (Minimum Jumps)", "greedy", 3, "jump_min",
        "You are given a 0-indexed array of integers `nums` of length `n`. You are initially positioned at `nums[0]`. Each element `nums[i]` represents the maximum length of a forward jump from index `i`.\n\nReturn the minimum number of jumps to reach `nums[n - 1]`. You are guaranteed that you can reach the end.",
        "- `1 <= len(nums) <= 10^4`\n- `0 <= nums[i] <= 1000`",
        "O(n)", "O(1)",
        "def jump_min(nums: list[int]) -> int:\n    pass\n",
        [
            {"args": [[2, 3, 1, 1, 4]], "expected": 2},
            {"args": [[2, 3, 0, 1, 4]], "expected": 2},
            {"args": [[1]], "expected": 0},
            {"args": [[1, 2, 3]], "expected": 2}
        ],
        "def jump_min(nums: list[int]) -> int:\n    jumps = 0\n    curr_end = 0\n    curr_farthest = 0\n    for i in range(len(nums) - 1):\n        curr_farthest = max(curr_farthest, i + nums[i])\n        if i == curr_end:\n            jumps += 1\n            curr_end = curr_farthest\n    return jumps\n"
    ),

    P(
        "partition-labels", "Partition Labels (Last Occurrence Sweep)", "greedy", 2, "partition_labels",
        "You are given a string `s`. We want to partition the string into as many parts as possible so that each letter appears in at most one part.\n\nReturn a list of integers representing the size of these parts.",
        "- `1 <= len(s) <= 500`\n- `s` consists of lowercase English letters",
        "O(n)", "O(1)",
        "def partition_labels(s: str) -> list[int]:\n    pass\n",
        [
            {"args": ["ababcbacadefegdehijhklij"], "expected": [9, 7, 8]},
            {"args": ["eccbbbbdec"], "expected": [10]},
            {"args": ["a"], "expected": [1]},
            {"args": ["abcdef"], "expected": [1, 1, 1, 1, 1, 1]}
        ],
        "def partition_labels(s: str) -> list[int]:\n    last = {c: i for i, c in enumerate(s)}\n    res = []\n    anchor = j = 0\n    for i, c in enumerate(s):\n        j = max(j, last[c])\n        if i == j:\n            res.append(i - anchor + 1)\n            anchor = i + 1\n    return res\n"
    ),

    P(
        "gas-station", "Gas Station (Circular Circuit)", "greedy", 3, "can_complete_circuit",
        "There are `n` gas stations along a circular route, where the amount of gas at the `i`th station is `gas[i]`.\n\nYou have a car with an unlimited gas tank and it costs `cost[i]` of gas to travel from the `i`th station to its next `(i + 1)`th station. Return the starting gas station's index if you can travel around the circuit once in the clockwise direction, otherwise return `-1`.",
        "- `n == len(gas) == len(cost)`\n- `1 <= n <= 10^5`",
        "O(n)", "O(1)",
        "def can_complete_circuit(gas: list[int], cost: list[int]) -> int:\n    pass\n",
        [
            {"args": [[1, 2, 3, 4, 5], [3, 4, 5, 1, 2]], "expected": 3},
            {"args": [[2, 3, 4], [3, 4, 3]], "expected": -1},
            {"args": [[5, 1, 2, 3, 4], [4, 4, 1, 5, 1]], "expected": 4}
        ],
        "def can_complete_circuit(gas: list[int], cost: list[int]) -> int:\n    if sum(gas) < sum(cost):\n        return -1\n    total_tank = 0\n    start = 0\n    for i in range(len(gas)):\n        total_tank += gas[i] - cost[i]\n        if total_tank < 0:\n            start = i + 1\n            total_tank = 0\n    return start\n"
    ),

    P(
        "candy", "Candy Distribution (Two-Pass Greedy)", "greedy", 4, "candy",
        "There are `n` children standing in a line. Each child is assigned a rating value given in the integer array `ratings`.\n\nYou are giving candies to these children subjected to: each child must have at least one candy; children with a higher rating get more candies than their neighbors. Return the minimum number of candies you need to distribute.",
        "- `n == len(ratings)`\n- `1 <= n <= 2 * 10^4`",
        "O(n)", "O(n)",
        "def candy(ratings: list[int]) -> int:\n    pass\n",
        [
            {"args": [[1, 0, 2]], "expected": 5},  # [2, 1, 2]
            {"args": [[1, 2, 2]], "expected": 4},  # [1, 2, 1]
            {"args": [[1]], "expected": 1},
            {"args": [[1, 3, 2, 2, 1]], "expected": 7}
        ],
        "def candy(ratings: list[int]) -> int:\n    n = len(ratings)\n    candies = [1] * n\n    for i in range(1, n):\n        if ratings[i] > ratings[i - 1]:\n            candies[i] = candies[i - 1] + 1\n    for i in range(n - 2, -1, -1):\n        if ratings[i] > ratings[i + 1]:\n            candies[i] = max(candies[i], candies[i + 1] + 1)\n    return sum(candies)\n"
    ),

    P(
        "minimum-deletions-to-make-character-frequencies-unique", "Minimum Deletions for Unique Frequencies", "greedy", 2, "min_deletions",
        "A string `s` is called good if there are no two different characters in `s` that have the same frequency. Given a string `s`, return the minimum number of characters you need to delete to make `s` good.",
        "- `1 <= len(s) <= 10^5`\n- `s` contains only lowercase English letters",
        "O(n)", "O(1)",
        "def min_deletions(s: str) -> int:\n    pass\n",
        [
            {"args": ["aab"], "expected": 0},
            {"args": ["aaabbbcc"], "expected": 2},
            {"args": ["ceabaacb"], "expected": 2}
        ],
        "from collections import Counter\n\ndef min_deletions(s: str) -> int:\n    cnt = Counter(s)\n    deletions = 0\n    used = set()\n    for freq in cnt.values():\n        while freq > 0 and freq in used:\n            freq -= 1\n            deletions += 1\n        used.add(freq)\n    return deletions\n"
    )
]
