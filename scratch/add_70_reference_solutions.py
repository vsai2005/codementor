import json
import re

with open('scratch/existing_70_problems.json', encoding='utf-8') as f:
    data = json.load(f)

problems = data["problems"]
slugs = [p["slug"] for p in problems]
print(f"Loaded {len(slugs)} original slugs.")

# Canonical reference solutions for the 70 original problems
SOLUTIONS = {
    # arrays
    "contains-duplicate": "def contains_duplicate(nums):\n    return len(nums) != len(set(nums))\n",
    "two-sum": "def two_sum(nums, target):\n    seen = {}\n    for i, x in enumerate(nums):\n        if target - x in seen:\n            return [seen[target - x], i]\n        seen[x] = i\n    return []\n",
    "product-except-self": "def product_except_self(nums):\n    n = len(nums)\n    out = [1] * n\n    pref = 1\n    for i in range(n):\n        out[i] = pref\n        pref *= nums[i]\n    suff = 1\n    for i in range(n - 1, -1, -1):\n        out[i] *= suff\n        suff *= nums[i]\n    return out\n",
    "running-sum": "def running_sum(nums):\n    res = []\n    curr = 0\n    for x in nums:\n        curr += x\n        res.append(curr)\n    return res\n",
    "max-consecutive-ones": "def find_max_consecutive_ones(nums):\n    max_ones = curr = 0\n    for x in nums:\n        if x == 1:\n            curr += 1\n            max_ones = max(max_ones, curr)\n        else:\n            curr = 0\n    return max_ones\n",
    "single-number": "def single_number(nums):\n    res = 0\n    for x in nums:\n        res ^= x\n    return res\n",
    "move-zeroes": "def move_zeroes(nums):\n    p = 0\n    for i in range(len(nums)):\n        if nums[i] != 0:\n            nums[p], nums[i] = nums[i], nums[p]\n            p += 1\n    return nums\n",
    "majority-element": "def majority_element(nums):\n    cand = None\n    count = 0\n    for x in nums:\n        if count == 0:\n            cand = x\n        count += (1 if x == cand else -1)\n    return cand\n",
    "max-subarray": "def max_sub_array(nums):\n    max_sum = curr = nums[0]\n    for x in nums[1:]:\n        curr = max(x, curr + x)\n        max_sum = max(max_sum, curr)\n    return max_sum\n",
    "find-disappeared": "def find_disappeared_numbers(nums):\n    n = len(nums)\n    s = set(nums)\n    return [i for i in range(1, n + 1) if i not in s]\n",
    "rotate-array": "def rotate(nums, k):\n    k = k % len(nums)\n    nums[:] = nums[-k:] + nums[:-k]\n    return nums\n",
    "subarray-sum-k": "def subarray_sum(nums, k):\n    count = 0\n    curr = 0\n    seen = {0: 1}\n    for x in nums:\n        curr += x\n        if curr - k in seen:\n            count += seen[curr - k]\n        seen[curr] = seen.get(curr, 0) + 1\n    return count\n",

    # two-pointers
    "reverse-list": "def reverse_list(items):\n    items.reverse()\n    return items\n",
    "valid-palindrome": "def is_palindrome(s):\n    filtered = [ch.lower() for ch in s if ch.isalnum()]\n    return filtered == filtered[::-1]\n",
    "container-most-water": "def max_area(height):\n    l, r = 0, len(height) - 1\n    max_w = 0\n    while l < r:\n        w = (r - l) * min(height[l], height[r])\n        max_w = max(max_w, w)\n        if height[l] < height[r]:\n            l += 1\n        else:\n            r -= 1\n    return max_w\n",
    "is-subsequence": "def is_subsequence(s, t):\n    i = j = 0\n    while i < len(s) and j < len(t):\n        if s[i] == t[j]:\n            i += 1\n        j += 1\n    return i == len(s)\n",
    "sorted-squares": "def sorted_squares(nums):\n    res = [x * x for x in nums]\n    res.sort()\n    return res\n",
    "two-sum-sorted": "def two_sum_sorted(numbers, target):\n    l, r = 0, len(numbers) - 1\n    while l < r:\n        s = numbers[l] + numbers[r]\n        if s == target:\n            return [l + 1, r + 1]\n        elif s < target:\n            l += 1\n        else:\n            r -= 1\n    return []\n",
    "sort-by-parity": "def sort_array_by_parity(nums):\n    evens = [x for x in nums if x % 2 == 0]\n    odds = [x for x in nums if x % 2 != 0]\n    return evens + odds\n",
    "dedupe-sorted": "def dedupe_sorted(nums):\n    res = []\n    for x in nums:\n        if not res or res[-1] != x: res.append(x)\n    return res\n",
    "merge-sorted-lists": "def merge_sorted(list1, list2):\n    i = j = 0\n    res = []\n    while i < len(list1) and j < len(list2):\n        if list1[i] <= list2[j]:\n            res.append(list1[i])\n            i += 1\n        else:\n            res.append(list2[j])\n            j += 1\n    res.extend(list1[i:])\n    res.extend(list2[j:])\n    return res\n",
    "three-sum": "def three_sum(nums):\n    nums.sort()\n    res = []\n    for i in range(len(nums) - 2):\n        if i > 0 and nums[i] == nums[i - 1]:\n            continue\n        l, r = i + 1, len(nums) - 1\n        while l < r:\n            s = nums[i] + nums[l] + nums[r]\n            if s == 0:\n                res.append([nums[i], nums[l], nums[r]])\n                while l < r and nums[l] == nums[l + 1]:\n                    l += 1\n                while l < r and nums[r] == nums[r - 1]:\n                    r -= 1\n                l += 1\n                r -= 1\n            elif s < 0:\n                l += 1\n            else:\n                r -= 1\n    return res\n",
    "trapping-rain-water": "def trap(height):\n    if not height:\n        return 0\n    l, r = 0, len(height) - 1\n    max_l, max_r = height[l], height[r]\n    water = 0\n    while l < r:\n        if max_l <= max_r:\n            l += 1\n            max_l = max(max_l, height[l])\n            water += max_l - height[l]\n        else:\n            r -= 1\n            max_r = max(max_r, height[r])\n            water += max_r - height[r]\n    return water\n",

    # strings
    "count-vowels": "def count_vowels(s):\n    vowels = set('aeiouAEIOU')\n    return sum(1 for ch in s if ch in vowels)\n",
    "valid-anagram": "def is_anagram(s, t):\n    return sorted(s) == sorted(t)\n",
    "longest-substring": "def length_of_longest_substring(s):\n    seen = {}\n    max_len = start = 0\n    for i, ch in enumerate(s):\n        if ch in seen and seen[ch] >= start:\n            start = seen[ch] + 1\n        seen[ch] = i\n        max_len = max(max_len, i - start + 1)\n    return max_len\n",
    "reverse-string": "def reverse_string(s):\n    return s[::-1]\n",
    "fizzbuzz": "def fizz_buzz(n):\n    res = []\n    for i in range(1, n + 1):\n        if i % 15 == 0:\n            res.append('FizzBuzz')\n        elif i % 3 == 0:\n            res.append('Fizz')\n        elif i % 5 == 0:\n            res.append('Buzz')\n        else:\n            res.append(str(i))\n    return res\n",
    "first-unique-char": "from collections import Counter\ndef first_uniq_char(s):\n    c = Counter(s)\n    for i, ch in enumerate(s):\n        if c[ch] == 1:\n            return i\n    return -1\n",
    "longest-common-prefix": "def longest_common_prefix(strs):\n    if not strs:\n        return ''\n    prefix = strs[0]\n    for s in strs[1:]:\n        while not s.startswith(prefix):\n            prefix = prefix[:-1]\n            if not prefix:\n                return ''\n    return prefix\n",
    "reverse-words": "def reverse_words(s):\n    return ' '.join(s.strip().split()[::-1])\n",
    "longest-palindrome": "from collections import Counter\ndef longest_palindrome(s):\n    counts = Counter(s)\n    length = 0\n    odd_found = False\n    for count in counts.values():\n        if count % 2 == 0:\n            length += count\n        else:\n            length += count - 1\n            odd_found = True\n    return length + (1 if odd_found else 0)\n",
    "roman-to-int": "def roman_to_int(s):\n    vals = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}\n    total = 0\n    for i in range(len(s)):\n        if i + 1 < len(s) and vals[s[i]] < vals[s[i + 1]]:\n            total -= vals[s[i]]\n        else:\n            total += vals[s[i]]\n    return total\n",
    "valid-palindrome-ii": "def valid_palindrome_ii(s):\n    def is_pal(i, j):\n        while i < j:\n            if s[i] != s[j]: return False\n            i += 1; j -= 1\n        return True\n    l, r = 0, len(s) - 1\n    while l < r:\n        if s[l] != s[r]:\n            return is_pal(l + 1, r) or is_pal(l, r - 1)\n        l += 1; r -= 1\n    return True\n",
    "add-binary": "def add_binary(a, b):\n    return bin(int(a, 2) + int(b, 2))[2:]\n",

    # stacks
    "valid-parentheses": "def is_valid(s):\n    stack = []\n    pairs = {')': '(', '}': '{', ']': '['}\n    for ch in s:\n        if ch in '({[':\n            stack.append(ch)\n        elif ch in pairs:\n            if not stack or stack.pop() != pairs[ch]:\n                return False\n    return len(stack) == 0\n",
    "min-stack-ops": "def min_after_ops(operations):\n    stack = []\n    for op in operations:\n        if op == '+':\n            stack.append(stack[-1] + stack[-2])\n        elif op == 'D':\n            stack.append(stack[-1] * 2)\n        elif op == 'C':\n            stack.pop()\n        else:\n            stack.append(int(op))\n    return sum(stack)\n",
    "daily-temperatures": "def daily_temperatures(temperatures):\n    n = len(temperatures)\n    res = [0] * n\n    stack = []\n    for i, t in enumerate(temperatures):\n        while stack and temperatures[stack[-1]] < t:\n            prev = stack.pop()\n            res[prev] = i - prev\n        stack.append(i)\n    return res\n",
    "backspace-compare": "def backspace_compare(s, t):\n    def build(st):\n        stack = []\n        for c in st:\n            if c == '#':\n                if stack: stack.pop()\n            else:\n                stack.append(c)\n        return stack\n    return build(s) == build(t)\n",
    "remove-adjacent-dupes": "def remove_adjacent_duplicates(s):\n    stack = []\n    for c in s:\n        if stack and stack[-1] == c:\n            stack.pop()\n        else:\n            stack.append(c)\n    return ''.join(stack)\n",
    "make-good": "def make_good(s):\n    stack = []\n    for c in s:\n        if stack and abs(ord(stack[-1]) - ord(c)) == 32:\n            stack.pop()\n        else:\n            stack.append(c)\n    return ''.join(stack)\n",
    "eval-rpn": "def eval_rpn(tokens):\n    stack = []\n    for t in tokens:\n        if t in '+-*/':\n            b = stack.pop()\n            a = stack.pop()\n            if t == '+': stack.append(a + b)\n            elif t == '-': stack.append(a - b)\n            elif t == '*': stack.append(a * b)\n            elif t == '/': stack.append(int(a / b))\n        else:\n            stack.append(int(t))\n    return stack[0]\n",
    "simplify-path": "def simplify_path(path):\n    parts = path.split('/')\n    stack = []\n    for p in parts:\n        if p == '..':\n            if stack: stack.pop()\n        elif p and p != '.':\n            stack.append(p)\n    return '/' + '/'.join(stack)\n",
    "decode-string": "def decode_string(s):\n    stack = []\n    curr_str = ''\n    curr_num = 0\n    for c in s:\n        if c.isdigit():\n            curr_num = curr_num * 10 + int(c)\n        elif c == '[':\n            stack.append((curr_str, curr_num))\n            curr_str = ''\n            curr_num = 0\n        elif c == ']':\n            prev_str, num = stack.pop()\n            curr_str = prev_str + curr_str * num\n        else:\n            curr_str += c\n    return curr_str\n",
    "asteroid-collision": "def asteroid_collision(asteroids):\n    stack = []\n    for ast in asteroids:\n        while stack and ast < 0 < stack[-1]:\n            if stack[-1] < -ast:\n                stack.pop()\n                continue\n            elif stack[-1] == -ast:\n                stack.pop()\n            break\n        else:\n            stack.append(ast)\n    return stack\n",
    "largest-rectangle": "def largest_rectangle_area(heights):\n    stack = [-1]\n    max_area = 0\n    heights.append(0)\n    for i, h in enumerate(heights):\n        while stack[-1] != -1 and heights[stack[-1]] > h:\n            height = heights[stack.pop()]\n            width = i - stack[-1] - 1\n            max_area = max(max_area, height * width)\n        stack.append(i)\n    heights.pop()\n    return max_area\n",

    # binary-search
    "binary-search": "def search(nums, target):\n    l, r = 0, len(nums) - 1\n    while l <= r:\n        mid = (l + r) // 2\n        if nums[mid] == target: return mid\n        elif nums[mid] < target: l = mid + 1\n        else: r = mid - 1\n    return -1\n",
    "search-rotated": "def search_rotated(nums, target):\n    l, r = 0, len(nums) - 1\n    while l <= r:\n        mid = (l + r) // 2\n        if nums[mid] == target: return mid\n        if nums[l] <= nums[mid]:\n            if nums[l] <= target < nums[mid]: r = mid - 1\n            else: l = mid + 1\n        else:\n            if nums[mid] < target <= nums[r]: l = mid + 1\n            else: r = mid - 1\n    return -1\n",
    "median-two-arrays": "def find_median(nums1, nums2):\n    merged = sorted(nums1 + nums2)\n    n = len(merged)\n    if n % 2 == 1: return float(merged[n // 2])\n    return (merged[n // 2 - 1] + merged[n // 2]) / 2.0\n",
    "search-insert": "def search_insert(nums, target):\n    l, r = 0, len(nums) - 1\n    while l <= r:\n        mid = (l + r) // 2\n        if nums[mid] == target: return mid\n        elif nums[mid] < target: l = mid + 1\n        else: r = mid - 1\n    return l\n",
    "my-sqrt": "def my_sqrt(x):\n    if x < 2: return x\n    l, r = 1, x // 2\n    while l <= r:\n        mid = (l + r) // 2\n        if mid * mid <= x: l = mid + 1\n        else: r = mid - 1\n    return r\n",
    "arrange-coins": "def arrange_coins(n):\n    l, r = 0, n\n    while l <= r:\n        mid = (l + r) // 2\n        if mid * (mid + 1) // 2 <= n: l = mid + 1\n        else: r = mid - 1\n    return r\n",
    "count-negatives": "def count_negatives(grid):\n    count = 0\n    for row in grid:\n        for x in row:\n            if x < 0: count += 1\n    return count\n",
    "find-min-rotated": "def find_min(nums):\n    l, r = 0, len(nums) - 1\n    while l < r:\n        mid = (l + r) // 2\n        if nums[mid] > nums[r]: l = mid + 1\n        else: r = mid\n    return nums[l]\n",
    "find-peak": "def find_peak_element(nums):\n    l, r = 0, len(nums) - 1\n    while l < r:\n        mid = (l + r) // 2\n        if nums[mid] > nums[mid + 1]: r = mid\n        else: l = mid + 1\n    return l\n",
    "search-range": "def search_range(nums, target):\n    import bisect\n    l = bisect.bisect_left(nums, target)\n    if l == len(nums) or nums[l] != target: return [-1, -1]\n    r = bisect.bisect_right(nums, target) - 1\n    return [l, r]\n",
    "single-non-duplicate": "def single_non_duplicate(nums):\n    l, r = 0, len(nums) - 1\n    while l < r:\n        mid = (l + r) // 2\n        if mid % 2 == 1: mid -= 1\n        if nums[mid] == nums[mid + 1]: l = mid + 2\n        else: r = mid\n    return nums[l]\n",
    "koko-bananas": "def min_eating_speed(piles, h):\n    import math\n    l, r = 1, max(piles)\n    while l < r:\n        mid = (l + r) // 2\n        hours = sum(math.ceil(p / mid) for p in piles)\n        if hours <= h: r = mid\n        else: l = mid + 1\n    return l\n",

    # graphs
    "max-depth": "def max_depth(items):\n    if not isinstance(items, list): return 0\n    if not items: return 1\n    return 1 + max((max_depth(x) for x in items), default=0)\n",
    "number-of-islands": "def num_islands(grid):\n    if not grid: return 0\n    m, n = len(grid), len(grid[0])\n    visited = set()\n    count = 0\n    def dfs(r, c):\n        visited.add((r, c))\n        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:\n            nr, nc = r + dr, c + dc\n            if 0 <= nr < m and 0 <= nc < n and (nr, nc) not in visited and str(grid[nr][nc]) == '1':\n                dfs(nr, nc)\n    for r in range(m):\n        for c in range(n):\n            if str(grid[r][c]) == '1' and (r, c) not in visited:\n                count += 1\n                dfs(r, c)\n    return count\n",
    "course-schedule": "from collections import deque, defaultdict\ndef can_finish(num_courses, prerequisites):\n    adj = defaultdict(list)\n    in_deg = [0] * num_courses\n    for dest, src in prerequisites:\n        adj[src].append(dest)\n        in_deg[dest] += 1\n    q = deque([i for i in range(num_courses) if in_deg[i] == 0])\n    visited = 0\n    while q:\n        curr = q.popleft()\n        visited += 1\n        for nxt in adj[curr]:\n            in_deg[nxt] -= 1\n            if in_deg[nxt] == 0:\n                q.append(nxt)\n    return visited == num_courses\n",
    "find-center": "def find_center(edges):\n    return edges[0][0] if edges[0][0] in edges[1] else edges[0][1]\n",
    "find-judge": "def find_judge(n, trust):\n    scores = [0] * (n + 1)\n    for a, b in trust:\n        scores[a] -= 1\n        scores[b] += 1\n    for i in range(1, n + 1):\n        if scores[i] == n - 1: return i\n    return -1\n",
    "island-perimeter": "def island_perimeter(grid):\n    m, n = len(grid), len(grid[0])\n    peri = 0\n    for r in range(m):\n        for c in range(n):\n            if grid[r][c] == 1:\n                peri += 4\n                if r > 0 and grid[r - 1][c] == 1: peri -= 2\n                if c > 0 and grid[r][c - 1] == 1: peri -= 2\n    return peri\n",
    "flood-fill": "def flood_fill(image, sr, sc, color):\n    orig = image[sr][sc]\n    if orig == color: return image\n    m, n = len(image), len(image[0])\n    def dfs(r, c):\n        if 0 <= r < m and 0 <= c < n and image[r][c] == orig:\n            image[r][c] = color\n            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:\n                dfs(r + dr, c + dc)\n    dfs(sr, sc)\n    return image\n",
    "keys-and-rooms": "def can_visit_all_rooms(rooms):\n    visited = {0}\n    stack = [0]\n    while stack:\n        curr = stack.pop()\n        for key in rooms[curr]:\n            if key not in visited:\n                visited.add(key)\n                stack.append(key)\n    return len(visited) == len(rooms)\n",
    "valid-path": "from collections import defaultdict\ndef valid_path(n, edges, source, destination):\n    adj = defaultdict(list)\n    for u, v in edges:\n        adj[u].append(v)\n        adj[v].append(u)\n    visited = {source}\n    stack = [source]\n    while stack:\n        curr = stack.pop()\n        if curr == destination: return True\n        for nxt in adj[curr]:\n            if nxt not in visited:\n                visited.add(nxt)\n                stack.append(nxt)\n    return False\n",
    "count-components": "def count_components(n, edges):\n    parent = list(range(n))\n    def find(i):\n        if parent[i] != i: parent[i] = find(parent[i])\n        return parent[i]\n    components = n\n    for u, v in edges:\n        ru, rv = find(u), find(v)\n        if ru != rv:\n            parent[ru] = rv\n            components -= 1\n    return components\n",
    "max-area-island": "def max_area_of_island(grid):\n    m, n = len(grid), len(grid[0])\n    visited = set()\n    def dfs(r, c):\n        visited.add((r, c))\n        area = 1\n        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:\n            nr, nc = r + dr, c + dc\n            if 0 <= nr < m and 0 <= nc < n and (nr, nc) not in visited and grid[nr][nc] == 1:\n                area += dfs(nr, nc)\n        return area\n    max_a = 0\n    for r in range(m):\n        for c in range(n):\n            if grid[r][c] == 1 and (r, c) not in visited:\n                max_a = max(max_a, dfs(r, c))\n    return max_a\n",
    "rotting-oranges": "from collections import deque\ndef oranges_rotting(grid):\n    m, n = len(grid), len(grid[0])\n    q = deque()\n    fresh = 0\n    for r in range(m):\n        for c in range(n):\n            if grid[r][c] == 2: q.append((r, c, 0))\n            elif grid[r][c] == 1: fresh += 1\n    minutes = 0\n    while q:\n        r, c, d = q.popleft()\n        minutes = d\n        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:\n            nr, nc = r + dr, c + dc\n            if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1:\n                grid[nr][nc] = 2\n                fresh -= 1\n                q.append((nr, nc, d + 1))\n    return minutes if fresh == 0 else -1\n"
}

print(f"Total reference solutions mapped: {len(SOLUTIONS)}/70")
assert len(SOLUTIONS) == 70, f"Missing solutions for {set(slugs) - set(SOLUTIONS.keys())}"

# Test all 70 reference solutions against test_cases
import copy
errors = []
for p in problems:
    slug = p["slug"]
    entry = p["entry_point"]
    cases = p["test_cases"]
    sol = SOLUTIONS[slug]
    ns = {}
    try:
        exec(sol, ns)
    except Exception as e:
        errors.append(f"{slug} failed to compile: {e}")
        continue
    fn = ns.get(entry)
    if not fn:
        errors.append(f"{slug} entry point {entry} not found")
        continue
    for i, c in enumerate(cases):
        args_copy = copy.deepcopy(c["args"])
        expected = c["expected"]
        try:
            actual = fn(*args_copy)
            if isinstance(expected, float) and isinstance(actual, (int, float)):
                match = abs(actual - expected) < 1e-4
            else:
                match = (actual == expected)
            if not match:
                errors.append(f"{slug} case #{i+1} FAIL: expected {expected} got {actual}")
        except Exception as e:
            errors.append(f"{slug} case #{i+1} ERROR: {e}")

if errors:
    print(f"Errors in existing 70 solutions: {len(errors)}")
    for err in errors[:10]:
        print(" ", err)
else:
    print(">>> ALL 70 EXISTING REFERENCE SOLUTIONS PASSED 100% OF TEST CASES! <<<")

# Now update backend/app/seed.py so the first 70 problems include reference_solution
with open('backend/app/seed.py', encoding='utf-8') as f:
    seed_text = f.read()

# Update each P call with its reference solution if not already present
for slug, sol in SOLUTIONS.items():
    # Look for P("slug", ... ) and append sol as last parameter
    pattern = rf'(P\(\s*[\'"]{slug}[\'"].*?test_cases\s*:\s*cases\s*,\s*)\)'
    # Or matches P(slug, ..., cases)
    # Let's inspect how P is called in seed.py

print("Done.")
