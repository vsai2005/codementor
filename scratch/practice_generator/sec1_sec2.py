"""
Practice Problems for Section 1 (Python Foundations) and Section 2 (Python Core & Containers)
Total problems: 16
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

SEC1_SEC2_PROBLEMS = [
    # --- Section 1: Python Foundations (Days 1-10) ---
    P(
        "celsius-to-fahrenheit", "Celsius to Fahrenheit Converter", "python-basics", 1, "convert_celsius",
        "Given a floating-point temperature in Celsius `c`, return the temperature converted to Fahrenheit rounded to 2 decimal places.\n\nThe conversion formula is `F = (C * 9/5) + 32`.",
        "- `-273.15 <= c <= 1000.0`\n- Round result to 2 decimal places using `round(val, 2)`",
        "O(1)", "O(1)",
        "def convert_celsius(c: float) -> float:\n    pass\n",
        [
            {"args": [0.0], "expected": 32.0},
            {"args": [100.0], "expected": 212.0},
            {"args": [-40.0], "expected": -40.0},
            {"args": [37.0], "expected": 98.6},
            {"args": [-273.15], "expected": -459.67},
            {"args": [25.5], "expected": 77.9}
        ],
        "def convert_celsius(c: float) -> float:\n    return round((c * 9.0 / 5.0) + 32.0, 2)\n"
    ),

    P(
        "time-converter-seconds", "Seconds to Digital Time", "python-basics", 1, "format_seconds",
        "Given an integer `total_seconds`, return a formatted digital clock string in `\"HH:MM:SS\"` format with leading zeros.\n\nUse integer division `//` and modulo `%` arithmetic.",
        "- `0 <= total_seconds <= 863999` (up to 99 hours, 59 mins, 59 secs)",
        "O(1)", "O(1)",
        "def format_seconds(total_seconds: int) -> str:\n    pass\n",
        [
            {"args": [0], "expected": "00:00:00"},
            {"args": [59], "expected": "00:00:59"},
            {"args": [60], "expected": "00:01:00"},
            {"args": [3661], "expected": "01:01:01"},
            {"args": [86399], "expected": "23:59:59"},
            {"args": [3599], "expected": "00:59:59"}
        ],
        "def format_seconds(total_seconds: int) -> str:\n    h = total_seconds // 3600\n    rem = total_seconds % 3600\n    m = rem // 60\n    s = rem % 60\n    return f\"{h:02d}:{m:02d}:{s:02d}\"\n"
    ),

    P(
        "slice-url-domain", "Extract Domain from URL", "python-basics", 1, "extract_domain",
        "Given a website URL string `url`, extract and return the core domain name (excluding protocol `http://` or `https://` and path after `/`).\n\nFor example, `\"https://codementor.io/learn\"` becomes `\"codementor.io\"`.",
        "- `1 <= len(url) <= 500`\n- URL begins with `http://` or `https://`",
        "O(n)", "O(n)",
        "def extract_domain(url: str) -> str:\n    pass\n",
        [
            {"args": ["https://codementor.io/learn"], "expected": "codementor.io"},
            {"args": ["http://python.org"], "expected": "python.org"},
            {"args": ["https://sub.domain.com/path/to/page?q=1"], "expected": "sub.domain.com"},
            {"args": ["http://localhost:8000/api"], "expected": "localhost:8000"},
            {"args": ["https://google.com/"], "expected": "google.com"}
        ],
        "def extract_domain(url: str) -> str:\n    if url.startswith(\"https://\"):\n        url = url[8:]\n    elif url.startswith(\"http://\"):\n        url = url[7:]\n    return url.split(\"/\")[0]\n"
    ),

    P(
        "leap-year-checker", "Leap Year Boolean Invariant", "python-basics", 1, "is_leap_year",
        "Given a calendar `year`, return `True` if it is a leap year, and `False` otherwise.\n\nA leap year is divisible by 4, except end-of-century years which must also be divisible by 400 (e.g. 1900 was not a leap year, but 2000 was).",
        "- `1 <= year <= 9999`",
        "O(1)", "O(1)",
        "def is_leap_year(year: int) -> bool:\n    pass\n",
        [
            {"args": [2024], "expected": True},
            {"args": [2023], "expected": False},
            {"args": [1900], "expected": False},
            {"args": [2000], "expected": True},
            {"args": [2400], "expected": True},
            {"args": [1800], "expected": False}
        ],
        "def is_leap_year(year: int) -> bool:\n    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)\n"
    ),

    P(
        "sum-multiples-loop", "Sum of Multiples in Range", "python-basics", 1, "sum_multiples",
        "Given positive integers `n`, `a`, and `b`, return the sum of all positive integers less than or equal to `n` that are divisible by `a` or `b` (or both).",
        "- `1 <= n <= 10^4`\n- `1 <= a, b <= 100`",
        "O(n)", "O(1)",
        "def sum_multiples(n: int, a: int, b: int) -> int:\n    pass\n",
        [
            {"args": [10, 3, 5], "expected": 33},  # 3, 5, 6, 9, 10 -> 33
            {"args": [7, 2, 4], "expected": 12},   # 2, 4, 6 -> 12
            {"args": [1, 2, 3], "expected": 0},
            {"args": [15, 3, 5], "expected": 60},
            {"args": [20, 7, 11], "expected": 32}  # 7, 14, 11 -> 32
        ],
        "def sum_multiples(n: int, a: int, b: int) -> int:\n    total = 0\n    for i in range(1, n + 1):\n        if i % a == 0 or i % b == 0:\n            total += i\n    return total\n"
    ),

    P(
        "palindrome-number", "Palindrome Number (Arithmetic)", "python-basics", 1, "is_palindrome_number",
        "Given an integer `x`, return `True` if `x` is a palindrome integer, and `False` otherwise.\n\nNegative numbers are never palindromes (e.g. `-121` reversed is `121-`). Can you solve it without converting the integer to a string?",
        "- `-2^31 <= x <= 2^31 - 1`",
        "O(log10(x))", "O(1)",
        "def is_palindrome_number(x: int) -> bool:\n    pass\n",
        [
            {"args": [121], "expected": True},
            {"args": [-121], "expected": False},
            {"args": [10], "expected": False},
            {"args": [0], "expected": True},
            {"args": [12321], "expected": True},
            {"args": [1000021], "expected": False}
        ],
        "def is_palindrome_number(x: int) -> bool:\n    if x < 0 or (x % 10 == 0 and x != 0):\n        return False\n    rev = 0\n    orig = x\n    while x > 0:\n        rev = rev * 10 + (x % 10)\n        x //= 10\n    return rev == orig\n"
    ),

    P(
        "string-to-integer-atoi", "String to Integer (atoi)", "python-basics", 3, "my_atoi",
        "Implement the `my_atoi(s)` function which converts a string to a 32-bit signed integer:\n1. Whitespace: Ignore leading whitespace.\n2. Signedness: Determine sign with `'+'` or `'-'`.\n3. Conversion: Read contiguous digits until non-digit or end.\n4. Clamping: If integer is outside `[-2^31, 2^31 - 1]`, clamp to bound.",
        "- `0 <= len(s) <= 200`\n- Clamped range: `[-2147483648, 2147483647]`",
        "O(n)", "O(1)",
        "def my_atoi(s: str) -> int:\n    pass\n",
        [
            {"args": ["42"], "expected": 42},
            {"args": ["   -042"], "expected": -42},
            {"args": ["1337c0d3"], "expected": 1337},
            {"args": ["0-1"], "expected": 0},
            {"args": ["words and 987"], "expected": 0},
            {"args": ["-91283472332"], "expected": -2147483648}
        ],
        "def my_atoi(s: str) -> int:\n    s = s.lstrip()\n    if not s:\n        return 0\n    sign = 1\n    idx = 0\n    if s[0] == '-':\n        sign = -1\n        idx = 1\n    elif s[0] == '+':\n        idx = 1\n    val = 0\n    while idx < len(s) and s[idx].isdigit():\n        val = val * 10 + int(s[idx])\n        idx += 1\n    val *= sign\n    MIN_INT = -2147483648\n    MAX_INT = 2147483647\n    if val < MIN_INT:\n        return MIN_INT\n    if val > MAX_INT:\n        return MAX_INT\n    return val\n"
    ),

    # --- Section 2: Python Core & Containers (Days 11-25) ---
    P(
        "remove-element", "Remove Element (In-Place)", "python-basics", 1, "remove_element",
        "Given an integer array `nums` and an integer `val`, remove all occurrences of `val` in `nums` in-place. Return the number of elements in `nums` which are not equal to `val`.\n\nModify `nums` in-place and return the list containing only the valid remaining elements.",
        "- `0 <= len(nums) <= 100`\n- `0 <= nums[i] <= 50`\n- `0 <= val <= 100`",
        "O(n)", "O(1)",
        "def remove_element(nums: list[int], val: int) -> list[int]:\n    pass\n",
        [
            {"args": [[3, 2, 2, 3], 3], "expected": [2, 2]},
            {"args": [[0, 1, 2, 2, 3, 0, 4, 2], 2], "expected": [0, 1, 3, 0, 4]},
            {"args": [[], 1], "expected": []},
            {"args": [[1], 1], "expected": []},
            {"args": [[1, 2, 3], 4], "expected": [1, 2, 3]}
        ],
        "def remove_element(nums: list[int], val: int) -> list[int]:\n    k = 0\n    for i in range(len(nums)):\n        if nums[i] != val:\n            nums[k] = nums[i]\n            k += 1\n    return nums[:k]\n"
    ),

    P(
        "flatten-2d-matrix", "Flatten 2D Matrix Comprehension", "python-basics", 1, "flatten_matrix",
        "Given an `m x n` 2D grid of integers `matrix`, return a single flat 1D list containing all elements in row-major order.\n\nSolve this using a nested list comprehension expression.",
        "- `0 <= len(matrix) <= 100`\n- `0 <= len(matrix[i]) <= 100`",
        "O(m * n)", "O(m * n)",
        "def flatten_matrix(matrix: list[list[int]]) -> list[int]:\n    pass\n",
        [
            {"args": [[[1, 2, 3], [4, 5, 6], [7, 8, 9]]], "expected": [1, 2, 3, 4, 5, 6, 7, 8, 9]},
            {"args": [[[1, 2], [3, 4]]], "expected": [1, 2, 3, 4]},
            {"args": [[]], "expected": []},
            {"args": [[[1], [2], [3]]], "expected": [1, 2, 3]},
            {"args": [[[10, 20, 30]]], "expected": [10, 20, 30]}
        ],
        "def flatten_matrix(matrix: list[list[int]]) -> list[int]:\n    return [val for row in matrix for val in row]\n"
    ),

    P(
        "group-by-parity", "Group by Parity Buckets", "python-basics", 2, "group_parity",
        "Given a list of integers `nums`, return a dictionary with two keys: `'even'` containing all even numbers in original order, and `'odd'` containing all odd numbers in original order.",
        "- `0 <= len(nums) <= 1000`\n- `-10^6 <= nums[i] <= 10^6`",
        "O(n)", "O(n)",
        "def group_parity(nums: list[int]) -> dict[str, list[int]]:\n    pass\n",
        [
            {"args": [[1, 2, 3, 4, 5, 6]], "expected": {"even": [2, 4, 6], "odd": [1, 3, 5]}},
            {"args": [[2, 4, 6]], "expected": {"even": [2, 4, 6], "odd": []}},
            {"args": [[1, 3, 5]], "expected": {"even": [], "odd": [1, 3, 5]}},
            {"args": [[]], "expected": {"even": [], "odd": []}},
            {"args": [[0, -1, -2, -3]], "expected": {"even": [0, -2], "odd": [-1, -3]}}
        ],
        "def group_parity(nums: list[int]) -> dict[str, list[int]]:\n    res = {'even': [], 'odd': []}\n    for x in nums:\n        if x % 2 == 0:\n            res['even'].append(x)\n        else:\n            res['odd'].append(x)\n    return res\n"
    ),

    P(
        "common-keys-intersection", "Common Dictionary Key Matching", "python-basics", 1, "match_common_keys",
        "Given two dictionaries `d1` and `d2`, return a sorted list of all keys that appear in both dictionaries where their associated values are strictly equal (`d1[k] == d2[k]`).",
        "- `0 <= len(d1), len(d2) <= 1000`",
        "O(n log n)", "O(n)",
        "def match_common_keys(d1: dict, d2: dict) -> list:\n    pass\n",
        [
            {"args": [{"a": 1, "b": 2, "c": 3}, {"b": 2, "c": 4, "d": 5}], "expected": ["b"]},
            {"args": [{"x": 10, "y": 20}, {"x": 10, "y": 20}], "expected": ["x", "y"]},
            {"args": [{"a": 1}, {"a": 2}], "expected": []},
            {"args": [{}, {"a": 1}], "expected": []},
            {"args": [{"apple": 5, "banana": 3, "cherry": 7}, {"banana": 3, "cherry": 7, "date": 9}], "expected": ["banana", "cherry"]}
        ],
        "def match_common_keys(d1: dict, d2: dict) -> list:\n    common = [k for k in d1 if k in d2 and d1[k] == d2[k]]\n    common.sort()\n    return common\n"
    ),

    P(
        "vector2d-operations", "2D Vector Protocol Engine", "python-basics", 2, "evaluate_vector_stream",
        "Implement a 2D Vector engine supporting addition, scalar multiplication, dot product, and magnitude. Process an operations list where each command is `['ADD', [x1, y1], [x2, y2]]`, `['SCALE', [x, y], factor]`, `['DOT', [x1, y1], [x2, y2]]`, or `['MAG', [x, y]]`. Return the list of results (magnitudes rounded to 2 decimal places).",
        "- `1 <= len(operations) <= 500`\n- `-1000 <= coordinates <= 1000`",
        "O(n)", "O(n)",
        "def evaluate_vector_stream(operations: list) -> list:\n    # Define Vector2D with __add__, __mul__, etc.\n    pass\n",
        [
            {"args": [[["ADD", [1, 2], [3, 4]], ["DOT", [1, 2], [3, 4]], ["SCALE", [2, 3], 3], ["MAG", [3, 4]]]], "expected": [[4, 6], 11, [6, 9], 5.0]},
            {"args": [[["MAG", [0, 0]], ["DOT", [1, 0], [0, 1]]]], "expected": [0.0, 0]},
            {"args": [[["ADD", [-5, 10], [5, -10]]]], "expected": [[0, 0]]},
            {"args": [[["SCALE", [1, -1], -2]]], "expected": [[-2, 2]]},
            {"args": [[["MAG", [1, 1]]]], "expected": [1.41]}
        ],
        "import math\n\ndef evaluate_vector_stream(operations: list) -> list:\n    res = []\n    for op in operations:\n        cmd = op[0]\n        if cmd == 'ADD':\n            res.append([op[1][0] + op[2][0], op[1][1] + op[2][1]])\n        elif cmd == 'SCALE':\n            res.append([op[1][0] * op[2], op[1][1] * op[2]])\n        elif cmd == 'DOT':\n            res.append(op[1][0] * op[2][0] + op[1][1] * op[2][1])\n        elif cmd == 'MAG':\n            res.append(round(math.hypot(op[1][0], op[1][1]), 2))\n    return res\n"
    ),

    P(
        "sliding-window-deque", "Moving Average Stream", "python-basics", 2, "moving_average_stream",
        "Given a stream of integers `nums` and a window size `k`, return a list containing the moving average of the last at most `k` numbers as each number is processed, rounded to 2 decimal places.\n\nUse `collections.deque` for O(1) sliding window window maintenance.",
        "- `1 <= k <= 10^4`\n- `1 <= len(nums) <= 10^5`",
        "O(n)", "O(k)",
        "def moving_average_stream(nums: list[int], k: int) -> list[float]:\n    pass\n",
        [
            {"args": [[1, 10, 3, 5], 3], "expected": [1.0, 5.5, 4.67, 6.0]},
            {"args": [[5], 1], "expected": [5.0]},
            {"args": [[1, 2, 3, 4, 5], 1], "expected": [1.0, 2.0, 3.0, 4.0, 5.0]},
            {"args": [[10, 20], 5], "expected": [10.0, 15.0]},
            {"args": [[4, 8, 12, 16], 2], "expected": [4.0, 6.0, 10.0, 14.0]}
        ],
        "from collections import deque\n\ndef moving_average_stream(nums: list[int], k: int) -> list[float]:\n    window = deque()\n    running_sum = 0\n    res = []\n    for x in nums:\n        window.append(x)\n        running_sum += x\n        if len(window) > k:\n            running_sum -= window.popleft()\n        res.append(round(running_sum / len(window), 2))\n    return res\n"
    ),

    P(
        "merge-sorted-array", "Merge Sorted Array (In-Place)", "python-basics", 2, "merge_sorted_array",
        "You are given two integer arrays `nums1` and `nums2`, sorted in non-decreasing order, and two integers `m` and `n`, representing the number of elements in `nums1` and `nums2` respectively.\n\n`nums1` has length `m + n`, where the last `n` elements are set to `0`. Merge `nums2` into `nums1` as one sorted array in-place and return `nums1`.",
        "- `len(nums1) == m + n`\n- `len(nums2) == n`\n- `0 <= m, n <= 200`",
        "O(m + n)", "O(1)",
        "def merge_sorted_array(nums1: list[int], m: int, nums2: list[int], n: int) -> list[int]:\n    pass\n",
        [
            {"args": [[1, 2, 3, 0, 0, 0], 3, [2, 5, 6], 3], "expected": [1, 2, 2, 3, 5, 6]},
            {"args": [[1], 1, [], 0], "expected": [1]},
            {"args": [[0], 0, [1], 1], "expected": [1]},
            {"args": [[4, 5, 6, 0, 0, 0], 3, [1, 2, 3], 3], "expected": [1, 2, 3, 4, 5, 6]},
            {"args": [[2, 0], 1, [1], 1], "expected": [1, 2]}
        ],
        "def merge_sorted_array(nums1: list[int], m: int, nums2: list[int], n: int) -> list[int]:\n    p1 = m - 1\n    p2 = n - 1\n    p = m + n - 1\n    while p2 >= 0:\n        if p1 >= 0 and nums1[p1] > nums2[p2]:\n            nums1[p] = nums1[p1]\n            p1 -= 1\n        else:\n            nums1[p] = nums2[p2]\n            p2 -= 1\n        p -= 1\n    return nums1\n"
    ),

    P(
        "find-the-difference", "Find the Difference", "python-basics", 1, "find_the_difference",
        "You are given two strings `s` and `t`. String `t` is generated by random shuffling string `s` and then adding one more letter at a random position.\n\nReturn the letter that was added to `t`.",
        "- `0 <= len(s) <= 1000`\n- `len(t) == len(s) + 1`\n- `s` and `t` consist of lowercase English letters",
        "O(n)", "O(1)",
        "def find_the_difference(s: str, t: str) -> str:\n    pass\n",
        [
            {"args": ["abcd", "abcde"], "expected": "e"},
            {"args": ["", "y"], "expected": "y"},
            {"args": ["a", "aa"], "expected": "a"},
            {"args": ["ae", "aea"], "expected": "a"},
            {"args": ["hello", "olhelo"], "expected": "o"}
        ],
        "def find_the_difference(s: str, t: str) -> str:\n    res = 0\n    for ch in s:\n        res ^= ord(ch)\n    for ch in t:\n        res ^= ord(ch)\n    return chr(res)\n"
    ),

    P(
        "sort-colors", "Sort Colors (Dutch National Flag)", "python-basics", 3, "sort_colors",
        "Given an array `nums` with `n` objects colored red (0), white (1), or blue (2), sort them in-place so that objects of the same color are adjacent, with colors in order red, white, blue (0, 1, 2).\n\nYou must solve this in-place in $O(N)$ one-pass using constant extra space $O(1)$. Return `nums`.",
        "- `1 <= len(nums) <= 300`\n- `nums[i]` is either `0`, `1`, or `2`",
        "O(n)", "O(1)",
        "def sort_colors(nums: list[int]) -> list[int]:\n    pass\n",
        [
            {"args": [[2, 0, 2, 1, 1, 0]], "expected": [0, 0, 1, 1, 2, 2]},
            {"args": [[2, 0, 1]], "expected": [0, 1, 2]},
            {"args": [[0]], "expected": [0]},
            {"args": [[1]], "expected": [1]},
            {"args": [[2, 2, 1, 1, 0, 0]], "expected": [0, 0, 1, 1, 2, 2]}
        ],
        "def sort_colors(nums: list[int]) -> list[int]:\n    low = 0\n    mid = 0\n    high = len(nums) - 1\n    while mid <= high:\n        if nums[mid] == 0:\n            nums[low], nums[mid] = nums[mid], nums[low]\n            low += 1\n            mid += 1\n        elif nums[mid] == 1:\n            mid += 1\n        else:\n            nums[mid], nums[high] = nums[high], nums[mid]\n            high -= 1\n    return nums\n"
    )
]
