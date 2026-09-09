"""
Section 6: Hashing & Hash Tables (Days 66 to 75)
Full authoring definitions for all 10 days with true practice archetypes,
distinguishable starter vs solution code, authentic 4-option MCQs with unique diagnostic explanations.
"""

SEC6_DAYS = {
    66: {
        "summary": "Hash Functions map arbitrary keys into fixed-size integer bucket indices, requiring determinism, uniform distribution, and avalanche effect.",
        "mechanics": "Using a prime modulus (bucket_idx = hash(key) % P) minimizes collisions when keys exhibit stride patterns. The avalanche effect ensures a single bit flip in the input completely alters the output hash bits.",
        "takeaway": "Good hash functions scatter keys uniformly across prime-sized bucket arrays, preventing clustering.",
        "sample_code": "# Polynomial Rolling Hash function for strings\ndef string_hash(s, P=31, M=1_000_000_007):\n    h = 0\n    for ch in s:\n        h = (h * P + ord(ch)) % M\n    return h",
        "q1": "Why are prime numbers typically used as moduli when mapping hash values to bucket arrays?",
        "q1_opts": [
            {"id": "A", "label": "Prime moduli prevent common factors with key patterns from causing systematic bucket clustering"},
            {"id": "B", "label": "Because computers can only divide by prime numbers"},
            {"id": "C", "label": "Prime moduli eliminate all hash collisions completely"},
            {"id": "D", "label": "Python enforces that array lengths must be prime"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! If bucket count M shares factors with key strides (e.g. even numbers modulo 100), keys only map to a fraction of the buckets. A prime modulus shares no factors, distributing keys uniformly.",
            "B": "Incorrect: Hardware ALUs divide by any non-zero integer.",
            "C": "Incorrect: Pigeonhole Principle guarantees collisions whenever key count > bucket count.",
            "D": "Incorrect: Python uses powers of 2 for dict sizes."
        },
        "q2": "What is the 'avalanche effect' in hash function design?",
        "q2_opts": [
            {"id": "A", "label": "A single bit change in the input key causes approximately 50% of the output hash bits to flip randomly"},
            {"id": "B", "label": "The hash table expands exponentially when full"},
            {"id": "C", "label": "Memory usage doubles every second"},
            {"id": "D", "label": "All keys collapse into bucket zero"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! Cryptographic and high-quality hash functions ensure that small input variations result in completely uncorrelated output hashes.",
            "B": "Incorrect: That describes dynamic resizing load factor policies.",
            "C": "Incorrect: Hash functions do not allocate memory dynamically.",
            "D": "Incorrect: That is worst-case hash collapse."
        },
        "practice_task": "Trace hash bit distribution across bucket arrays.",
        "starter": "# Day 66 Tracing: Hash Bucket Distribution\ndef bucket_distribution(keys: list[str], num_buckets: int) -> dict[int, list[str]]:\n    buckets = {i: [] for i in range(num_buckets)}\n    # TODO: For each key, compute polynomial hash (P=31, M=10007), map to bucket, append key\n    return buckets\n\nwords = ['cat', 'dog', 'act', 'god', 'tac']\nprint('Buckets:', bucket_distribution(words, 5))\n",
        "solution": "def bucket_distribution(keys: list[str], num_buckets: int) -> dict[int, list[str]]:\n    buckets = {i: [] for i in range(num_buckets)}\n    for k in keys:\n        h = 0\n        for ch in k:\n            h = (h * 31 + ord(ch)) % 10007\n        b_idx = h % num_buckets\n        buckets[b_idx].append(k)\n    return buckets\n\nwords = ['cat', 'dog', 'act', 'god', 'tac']\nprint('Buckets:', bucket_distribution(words, 5))\n",
        "patterns": ["Buckets: {0: ['act'], 1: ['cat', 'tac'], 2: ['dog'], 3: ['god'], 4: []}"],
        "hint": "Loop over key: h = (h * 31 + ord(ch)) % 10007. Bucket index is h % num_buckets.",
        "recap": [
            {"concept": "Pigeonhole Inevitability", "naiveIntuition": "A perfect hash function has zero collisions", "pythonReality": "When mapping infinite inputs to finite buckets, collisions are mathematically inevitable; resolution strategies are required"},
            {"concept": "Deterministic Invariant", "naiveIntuition": "hash() can return different numbers for identical keys", "pythonReality": "A hash function must return the identical hash integer for equal keys within a single program execution"}
        ]
    },
    67: {
        "summary": "Collision Resolution manages hash collisions via Separate Chaining (linked buckets) or Open Addressing (probing empty slots within a contiguous array).",
        "mechanics": "Separate Chaining stores collisions in linked lists or balanced trees per bucket. Linear Probing tests idx + 1, idx + 2. When load factor (N / capacity) exceeds 0.66, the table doubles and rehashes all keys.",
        "takeaway": "Maintaining load factors below 2/3 guarantees average O(1) lookup and insertion times.",
        "sample_code": "# Separate Chaining Hash Map\nclass SimpleHashMap:\n    def __init__(self, size=10):\n        self.buckets = [[] for _ in range(size)]\n    def put(self, k, v):\n        b = self.buckets[hash(k) % len(self.buckets)]\n        for i, (k2, _) in enumerate(b):\n            if k2 == k: b[i] = (k, v); return\n        b.append((k, v))\n    def get(self, k):\n        b = self.buckets[hash(k) % len(self.buckets)]\n        for k2, v in b:\n            if k2 == k: return v\n        return None",
        "q1": "Why must an open-addressing hash table use 'tombstones' (dummy markers) when deleting keys?",
        "q1_opts": [
            {"id": "A", "label": "To prevent probe chains from terminating prematurely on empty slots, preserving lookup paths for keys inserted later in the probe sequence"},
            {"id": "B", "label": "To prevent memory leaks in Python"},
            {"id": "C", "label": "Because open addressing cannot delete keys"},
            {"id": "D", "label": "To rehash the entire table immediately"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! If a slot is simply marked empty (None), linear probing stops searching immediately. A tombstone signals: 'keep probing because a deleted key used to be here'.",
            "B": "Incorrect: Tombstones maintain lookup correctness, not garbage collection.",
            "C": "Incorrect: Keys can be deleted using tombstones.",
            "D": "Incorrect: Rehashing occurs on resize, not on deletion."
        },
        "q2": "What happens to the worst-case time complexity of a hash map if all N keys hash to the exact same bucket?",
        "q2_opts": [
            {"id": "A", "label": "It degrades from O(1) to O(N) linear scan time"},
            {"id": "B", "label": "It remains strictly O(1)"},
            {"id": "C", "label": "It crashes with a MemoryError"},
            {"id": "D", "label": "It becomes O(log N)"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! If all keys land in a single bucket, looking up an item requires scanning all N elements in that chain, degrading to O(N).",
            "B": "Incorrect: O(1) is average-case with uniform distribution.",
            "C": "Incorrect: Memory is bounded by N.",
            "D": "Incorrect: Degradation is O(N) unless buckets are balanced trees (like Java HashMap)."
        },
        "practice_task": "Implement a basic hash map using separate chaining buckets.",
        "starter": "class MyHashMap:\n    def __init__(self):\n        self.size = 1000\n        self.table = [[] for _ in range(self.size)]\n\n    def put(self, key: int, value: int) -> None:\n        # TODO: Hash key, check if key exists in bucket (update), else append (key, value)\n        pass\n\n    def get(self, key: int) -> int:\n        # TODO: Hash key, search bucket, return value or -1\n        return -1\n\nhm = MyHashMap()\nhm.put(1, 100)\nhm.put(2, 200)\nhm.put(1, 150)\nprint('Get key 1:', hm.get(1))\nprint('Get key 2:', hm.get(2))\nprint('Get key 3:', hm.get(3))\n",
        "solution": "class MyHashMap:\n    def __init__(self):\n        self.size = 1000\n        self.table = [[] for _ in range(self.size)]\n\n    def put(self, key: int, value: int) -> None:\n        b_idx = key % self.size\n        bucket = self.table[b_idx]\n        for i, (k, v) in enumerate(bucket):\n            if k == key:\n                bucket[i] = (key, value)\n                return\n        bucket.append((key, value))\n\n    def get(self, key: int) -> int:\n        b_idx = key % self.size\n        bucket = self.table[b_idx]\n        for k, v in bucket:\n            if k == key:\n                return v\n        return -1\n\nhm = MyHashMap()\nhm.put(1, 100)\nhm.put(2, 200)\nhm.put(1, 150)\nprint('Get key 1:', hm.get(1))\nprint('Get key 2:', hm.get(2))\nprint('Get key 3:', hm.get(3))\n",
        "patterns": ["Get key 1: 150", "Get key 2: 200", "Get key 3: -1"],
        "hint": "Bucket is self.table[key % self.size]. Search for matching k to update; if not found, append (key, value).",
        "recap": [
            {"concept": "Load Factor Balance", "naiveIntuition": "Fill buckets until 100% full", "pythonReality": "When load factor exceeds 2/3, performance degrades rapidly; resizing at 66% preserves O(1) performance"},
            {"concept": "CPython Compact Dict", "naiveIntuition": "Python uses separate chaining", "pythonReality": "CPython 3.6+ uses open addressing with a sparse index array and a dense entries table to save memory and preserve insertion order"}
        ]
    },
    68: {
        "summary": "Frequency Counting uses fixed-size arrays or hash maps to record element occurrences, solving Anagram Detection and First Unique Character in O(N) time.",
        "mechanics": "For lowercase English letters: allocate count = [0] * 26. Increment count[ord(ch) - ord('a')] for s, decrement for t. If all 26 entries equal 0, s and t are valid anagrams.",
        "takeaway": "Counting frequencies directly with 26-slot arrays avoids sorting overhead and runs in O(N) time and O(1) space.",
        "sample_code": "# Valid Anagram using frequency array\ndef is_anagram(s, t):\n    if len(s) != len(t): return False\n    counts = [0] * 26\n    for ch1, ch2 in zip(s, t):\n        counts[ord(ch1) - ord('a')] += 1\n        counts[ord(ch2) - ord('a')] -= 1\n    return all(c == 0 for c in counts)",
        "q1": "Why is a fixed 26-element integer array preferred over a general dictionary for lowercase English string anagrams?",
        "q1_opts": [
            {"id": "A", "label": "It uses fixed O(1) space, zero heap hash allocations, and immediate direct index offsets ord(c) - ord('a')"},
            {"id": "B", "label": "Because dictionaries cannot store negative numbers"},
            {"id": "C", "label": "Because string sorting takes O(1) time"},
            {"id": "D", "label": "Dictionaries cannot compare letter counts"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! A 26-element array allocates fixed contiguous memory once, avoiding hash calculations, open addressing probes, and dictionary resizing overhead.",
            "B": "Incorrect: Dictionaries can store any integers.",
            "C": "Incorrect: String sorting takes O(N log N).",
            "D": "Incorrect: Dictionaries can count letters, but arrays have lower constant factors."
        },
        "q2": "What is the time complexity of comparing two strings of length N using sorted(s) == sorted(t)?",
        "q2_opts": [
            {"id": "A", "label": "O(N log N)"},
            {"id": "B", "label": "O(N)"},
            {"id": "C", "label": "O(1)"},
            {"id": "D", "label": "O(N^2)"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! Sorting both strings takes O(N log N) time; frequency arrays reduce this to strictly linear O(N) time.",
            "B": "Incorrect: Comparison sort cannot beat Omega(N log N).",
            "C": "Incorrect: All characters must be processed.",
            "D": "Incorrect: Timsort is O(N log N), not quadratic."
        },
        "practice_task": "Determine if two strings are valid anagrams in O(N) time and O(1) space.",
        "starter": "def is_anagram(s: str, t: str) -> bool:\n    if len(s) != len(t):\n        return False\n    # TODO: Count character frequencies using ord(c) - ord('a') and verify all counts are 0\n    return False\n\nprint('Anagram test 1:', is_anagram('anagram', 'nagaram'))\nprint('Anagram test 2:', is_anagram('rat', 'car'))\n",
        "solution": "def is_anagram(s: str, t: str) -> bool:\n    if len(s) != len(t):\n        return False\n    counts = [0] * 26\n    for ch1, ch2 in zip(s, t):\n        counts[ord(ch1) - ord('a')] += 1\n        counts[ord(ch2) - ord('a')] -= 1\n    return all(c == 0 for c in counts)\n\nprint('Anagram test 1:', is_anagram('anagram', 'nagaram'))\nprint('Anagram test 2:', is_anagram('rat', 'car'))\n",
        "patterns": ["Anagram test 1: True", "Anagram test 2: False"],
        "hint": "counts = [0] * 26. In zip(s, t), increment ord(ch1) - 97 and decrement ord(ch2) - 97. Return all(c == 0 for c in counts).",
        "recap": [
            {"concept": "Array vs Hash Map", "naiveIntuition": "Always use dict for frequencies", "pythonReality": "When alphabet size is bounded (e.g. 26 letters), a fixed array is lighter and faster than a hash map"},
            {"concept": "Early Length Guard", "naiveIntuition": "Count all characters first", "pythonReality": "If len(s) != len(t), return False immediately in O(1) time"}
        ]
    },
    69: {
        "summary": "Subarray Sum Equals K pairs prefix sums with hash maps to count contiguous subarrays summing to K in O(N) time and O(N) space.",
        "mechanics": "If pref[j] - pref[i] == k, then pref[i] == pref[j] - k. By tracking the frequencies of past prefix sums in a hash map, we count all matching indices i in O(1) time per element.",
        "takeaway": "Prefix sums paired with hash maps reduce contiguous subarray sum queries from O(N^2) to O(N).",
        "sample_code": "# Subarray Sum Equals K\ndef subarray_sum(nums, k):\n    counts = {0: 1} # Base prefix before index 0\n    curr = ans = 0\n    for x in nums:\n        curr += x\n        ans += counts.get(curr - k, 0)\n        counts[curr] = counts.get(curr, 0) + 1\n    return ans",
        "q1": "Why must the prefix sum frequency map be initialized with `{0: 1}` before scanning elements?",
        "q1_opts": [
            {"id": "A", "label": "To handle subarrays starting from index 0 whose cumulative sum directly equals K without needing a previous subtraction"},
            {"id": "B", "label": "To prevent division by zero errors"},
            {"id": "C", "label": "Because 0 is the default key in all Python dictionaries"},
            {"id": "D", "label": "It is not required and can be omitted"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! If curr == k, curr - k = 0. Having {0: 1} ensures that subarrays spanning from index 0 to the current element are counted.",
            "B": "Incorrect: No division is performed.",
            "C": "Incorrect: Dictionaries have no default keys unless defaultdict is used.",
            "D": "Incorrect: Without {0: 1}, all subarrays starting at index 0 are omitted."
        },
        "q2": "Why can't we use a simple sliding window for Subarray Sum Equals K if the array contains negative numbers?",
        "q2_opts": [
            {"id": "A", "label": "Negative numbers destroy window monotonicity: expanding the window can decrease the sum, and shrinking can increase the sum"},
            {"id": "B", "label": "Sliding window cannot be implemented in Python"},
            {"id": "C", "label": "Negative numbers cannot be stored in variables"},
            {"id": "D", "label": "Sliding window requires all numbers to be equal"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! Sliding window requires monotonic sums (adding numbers always increases sum). Negative numbers break this, making the prefix hash map the only linear O(N) solution.",
            "B": "Incorrect: Sliding window is widely used in Python.",
            "C": "Incorrect: Negative numbers are valid integers.",
            "D": "Incorrect: Window elements can vary."
        },
        "practice_task": "Count total contiguous subarrays summing to target K.",
        "starter": "def subarray_sum(nums: list[int], k: int) -> int:\n    counts = {0: 1}\n    curr_sum = 0\n    total_subarrays = 0\n    # TODO: Iterate nums, update curr_sum, add counts.get(curr_sum - k, 0) to total, and update counts map\n    \n    return total_subarrays\n\nnums = [1, 2, 3, -2, 2]\nprint('Total subarrays summing to 3:', subarray_sum(nums, 3))\n",
        "solution": "def subarray_sum(nums: list[int], k: int) -> int:\n    counts = {0: 1}\n    curr_sum = 0\n    total_subarrays = 0\n    for x in nums:\n        curr_sum += x\n        total_subarrays += counts.get(curr_sum - k, 0)\n        counts[curr_sum] = counts.get(curr_sum, 0) + 1\n    return total_subarrays\n\nnums = [1, 2, 3, -2, 2]\nprint('Total subarrays summing to 3:', subarray_sum(nums, 3))\n",
        "patterns": ["Total subarrays summing to 3: 3"],
        "hint": "Loop x in nums: curr_sum += x, total += counts.get(curr_sum - k, 0), counts[curr_sum] = counts.get(curr_sum, 0) + 1.",
        "recap": [
            {"concept": "Two-Sum on Prefixes", "naiveIntuition": "Check all subarray sums in O(N^2)", "pythonReality": "Looking up (curr - k) in past prefix frequencies reduces subarray counting to O(N)"},
            {"concept": "Update Order", "naiveIntuition": "Add current prefix to map before checking count", "pythonReality": "Check (curr - k) first, then increment counts[curr] to avoid counting empty subarrays"}
        ]
    },
    70: {
        "summary": "Grouping into Equivalence Classes constructs canonical hash keys (sorted strings or character count tuples) to partition items in O(N * K) time.",
        "mechanics": "For Group Anagrams: map each word to a 26-tuple of character counts: tuple([0]*26). Because tuples are hashable, use the tuple as a dictionary key: groups[key].append(word).",
        "takeaway": "Canonical representation keys group permutations and equivalence classes in O(N * K) time without sorting.",
        "sample_code": "# Group Anagrams by character count tuple\nfrom collections import defaultdict\ndef group_anagrams(words):\n    groups = defaultdict(list)\n    for w in words:\n        count = [0] * 26\n        for ch in w: count[ord(ch) - ord('a')] += 1\n        groups[tuple(count)].append(w)\n    return list(groups.values())",
        "q1": "Why is a 26-element tuple used as the dictionary key rather than a 26-element list in Group Anagrams?",
        "q1_opts": [
            {"id": "A", "label": "Lists are mutable and unhashable; tuples are immutable and hashable, allowing them to serve as dictionary keys"},
            {"id": "B", "label": "Tuples sort faster than lists"},
            {"id": "C", "label": "Python does not allow lists with 26 elements"},
            {"id": "D", "label": "Lists cannot store integer zeroes"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! In Python, dictionary keys must implement __hash__. Mutable lists set __hash__ = None, raising TypeError: unhashable type: 'list'. Tuples are immutable and hashable.",
            "B": "Incorrect: Tuples are not sorted here.",
            "C": "Incorrect: Lists can have arbitrary lengths.",
            "D": "Incorrect: Lists can store any integer."
        },
        "q2": "What is the time complexity of grouping N words of maximum length K using count-tuple keys compared to string-sorting keys?",
        "q2_opts": [
            {"id": "A", "label": "O(N * K) for count tuples vs O(N * K log K) for string sorting"},
            {"id": "B", "label": "O(N^2) for count tuples"},
            {"id": "C", "label": "O(N * K) for both"},
            {"id": "D", "label": "O(1) for count tuples"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! Building a 26-count array takes O(K) linear time per word. Sorting each word takes O(K log K). Across N words: O(N * K) vs O(N * K log K).",
            "B": "Incorrect: Count tuples take linear time in total word length.",
            "C": "Incorrect: Sorting adds the log K factor.",
            "D": "Incorrect: Must inspect all K characters."
        },
        "practice_task": "Group anagrams together using character frequency tuple keys.",
        "starter": "from collections import defaultdict\n\ndef group_anagrams(strs: list[str]) -> list[list[str]]:\n    ans = defaultdict(list)\n    # TODO: For each word, compute 26-tuple of character counts, use as dict key, append word\n    return sorted([sorted(g) for g in ans.values()])\n\nwords = ['eat', 'tea', 'tan', 'ate', 'nat', 'bat']\nprint('Grouped:', group_anagrams(words))\n",
        "solution": "from collections import defaultdict\n\ndef group_anagrams(strs: list[str]) -> list[list[str]]:\n    ans = defaultdict(list)\n    for s in strs:\n        count = [0] * 26\n        for ch in s:\n            count[ord(ch) - ord('a')] += 1\n        ans[tuple(count)].append(s)\n    return sorted([sorted(g) for g in ans.values()])\n\nwords = ['eat', 'tea', 'tan', 'ate', 'nat', 'bat']\nprint('Grouped:', group_anagrams(words))\n",
        "patterns": ["Grouped: [['ate', 'eat', 'tea'], ['bat'], ['nat', 'tan']]"],
        "hint": "Initialize count = [0] * 26. Loop ch in s: count[ord(ch) - 97] += 1. Use ans[tuple(count)].append(s).",
        "recap": [
            {"concept": "Canonical Signatures", "naiveIntuition": "Compare every word with every other word O(N^2)", "pythonReality": "Transforming each word into its canonical signature groups matching words in a single O(N) hash pass"},
            {"concept": "Tuple Hashability", "naiveIntuition": "Convert count array to string key", "pythonReality": "tuple(count) is directly hashable in C, avoiding string formatting allocations"}
        ]
    },
    71: {
        "summary": "Hash Sets enable O(1) membership lookups to find the Longest Consecutive Sequence in an unsorted array in linear O(N) time.",
        "mechanics": "Insert all numbers into a set. Only attempt to build sequences from sequence starts: if (num - 1) is NOT in the set, num is a sequence head! Loop while (num + streak) in set.",
        "takeaway": "Checking that num - 1 is absent ensures each element is visited at most twice, guaranteeing O(N) time.",
        "sample_code": "# Longest Consecutive Sequence in O(N)\ndef longest_consecutive(nums):\n    s = set(nums)\n    best = 0\n    for x in s:\n        if (x - 1) not in s: # Sequence start!\n            curr = x\n            streak = 1\n            while (curr + 1) in s:\n                curr += 1; streak += 1\n            best = max(best, streak)\n    return best",
        "q1": "Why is the condition `if (x - 1) not in num_set` critical for achieving O(N) time?",
        "q1_opts": [
            {"id": "A", "label": "It guarantees that the inner while loop only executes for numbers that start a sequence, ensuring each number is visited at most twice overall"},
            {"id": "B", "label": "It prevents searching for negative numbers"},
            {"id": "C", "label": "To sort the set in ascending order"},
            {"id": "D", "label": "To avoid infinite loops"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! If we looped from every number, an array [1, 2, 3, 4, 5] would do 5 + 4 + 3 + 2 + 1 = O(N^2) work. By only starting from sequence heads (where x-1 is missing), each number is traversed exactly once.",
            "B": "Incorrect: Negative numbers are valid sequence members.",
            "C": "Incorrect: Sets are unordered.",
            "D": "Incorrect: Finite numbers cannot create infinite streaks."
        },
        "q2": "What is the time complexity of inserting all N array elements into a Python set?",
        "q2_opts": [
            {"id": "A", "label": "O(N) average time"},
            {"id": "B", "label": "O(N log N)"},
            {"id": "C", "label": "O(1)"},
            {"id": "D", "label": "O(N^2)"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! Each of the N set insertions takes O(1) average time. Building the initial set takes O(N) time.",
            "B": "Incorrect: Trees take O(N log N); hash sets take O(N).",
            "C": "Incorrect: O(1) is the cost per element, not for all N.",
            "D": "Incorrect: Quadratic only under catastrophic pathological collisions."
        },
        "practice_task": "Find the length of the longest consecutive elements sequence in an unsorted array.",
        "starter": "def longest_consecutive(nums: list[int]) -> int:\n    if not nums:\n        return 0\n    num_set = set(nums)\n    max_streak = 0\n    # TODO: Iterate num_set, check if num - 1 is not in set (start of streak), count length\n    \n    return max_streak\n\nnums = [100, 4, 200, 1, 3, 2]\nprint('Longest consecutive streak:', longest_consecutive(nums))\n",
        "solution": "def longest_consecutive(nums: list[int]) -> int:\n    if not nums:\n        return 0\n    num_set = set(nums)\n    max_streak = 0\n    for x in num_set:\n        if (x - 1) not in num_set:\n            curr = x\n            streak = 1\n            while (curr + 1) in num_set:\n                curr += 1\n                streak += 1\n            if streak > max_streak:\n                max_streak = streak\n    return max_streak\n\nnums = [100, 4, 200, 1, 3, 2]\nprint('Longest consecutive streak:', longest_consecutive(nums))\n",
        "patterns": ["Longest consecutive streak: 4"],
        "hint": "Convert nums to set. Loop x in num_set: if (x - 1) not in num_set: count streak with while (curr + 1) in num_set. Update max_streak.",
        "recap": [
            {"concept": "Sequence Head Invariant", "naiveIntuition": "Sort array in O(N log N)", "pythonReality": "Filtering on sequence heads (x - 1 not in set) achieves strictly linear O(N) runtime"},
            {"concept": "Set Deduping", "naiveIntuition": "Duplicates extend sequence length", "pythonReality": "set(nums) naturally deduplicates elements so [1, 2, 2, 3] cleanly produces streak of 3"}
        ]
    },
    72: {
        "summary": "Rabin-Karp Substring Search uses polynomial rolling hashes to find patterns in average O(N + M) time, updating window hashes in O(1) time without re-hashing.",
        "mechanics": "Hash formula: H = (H_prev - s[i - M] * base^(M-1)) * base + s[i]. If window hash matches pattern hash, verify character equality to eliminate spurious hash collisions.",
        "takeaway": "Rolling hashes slide across strings in O(1) arithmetic updates per step, matching patterns in linear average time.",
        "sample_code": "# Rabin-Karp Rolling Hash update\n# new_hash = ((old_hash - old_char * high_base) * base + new_char) % MOD",
        "q1": "Why must the Rabin-Karp algorithm perform a character-by-character string comparison when window hash equals pattern hash?",
        "q1_opts": [
            {"id": "A", "label": "To verify that the match is genuine and not a spurious collision where different strings produced identical hash values modulo M"},
            {"id": "B", "label": "Because Python hash values are always 0"},
            {"id": "C", "label": "To update the pattern hash"},
            {"id": "D", "label": "To reset the sliding window"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! Because modulo operations map an infinite space of strings to finite integers, hash collisions (spurious hits) can occur. Direct verification guarantees correctness.",
            "B": "Incorrect: Hashes are non-zero integers.",
            "C": "Incorrect: The pattern hash is immutable.",
            "D": "Incorrect: The window continues sliding normally."
        },
        "q2": "What is the worst-case time complexity of the Rabin-Karp algorithm under adversarial hash collisions?",
        "q2_opts": [
            {"id": "A", "label": "O(N * M) when every window hash collides with the pattern hash"},
            {"id": "B", "label": "O(N + M)"},
            {"id": "C", "label": "O(log(N * M))"},
            {"id": "D", "label": "O(1)"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! If an adversary constructs strings where every window produces a spurious hash match, the algorithm performs N full M-character string comparisons: O(N * M).",
            "B": "Incorrect: O(N + M) is the average case.",
            "C": "Incorrect: String matching requires visiting text characters.",
            "D": "Incorrect: Substring search requires examining the text."
        },
        "practice_task": "Implement Rabin-Karp substring search with rolling hash slide.",
        "starter": "def rabin_karp(text: str, pattern: str) -> int:\n    if not pattern:\n        return 0\n    if len(pattern) > len(text):\n        return -1\n    # TODO: Compute pattern hash and first text window hash\n    # Slide window in O(1) time and check equality on hash match\n    return -1\n\ntext = 'hello world'\nprint('Found pattern at index:', rabin_karp(text, 'world'))\n",
        "solution": "def rabin_karp(text: str, pattern: str) -> int:\n    if not pattern:\n        return 0\n    if len(pattern) > len(text):\n        return -1\n    M, N = len(pattern), len(text)\n    BASE, MOD = 256, 10**9 + 7\n    h_pattern = 0\n    h_window = 0\n    power = 1\n    for i in range(M - 1):\n        power = (power * BASE) % MOD\n    for i in range(M):\n        h_pattern = (h_pattern * BASE + ord(pattern[i])) % MOD\n        h_window = (h_window * BASE + ord(text[i])) % MOD\n    for i in range(N - M + 1):\n        if h_pattern == h_window:\n            if text[i:i + M] == pattern:\n                return i\n        if i < N - M:\n            h_window = ((h_window - ord(text[i]) * power) * BASE + ord(text[i + M])) % MOD\n            if h_window < 0:\n                h_window += MOD\n    return -1\n\ntext = 'hello world'\nprint('Found pattern at index:', rabin_karp(text, 'world'))\n",
        "patterns": ["Found pattern at index: 6"],
        "hint": "Compute initial hashes using Horner's rule. On each slide, subtract `ord(text[i]) * power`, multiply by BASE, add `ord(text[i + M])`, and take `% MOD`.",
        "recap": [
            {"concept": "O(1) Rolling Update", "naiveIntuition": "Recompute hash from scratch in O(M)", "pythonReality": "Subtracting old leading character and adding new trailing character updates hash in O(1) arithmetic"},
            {"concept": "Spurious Verification", "naiveIntuition": "Hash match guarantees string match", "pythonReality": "Modulo collisions mean two different strings can share a hash; verify text[i:i+M] == pattern"}
        ]
    },
    73: {
        "summary": "LRU (Least Recently Used) Cache evicts the item that has not been accessed for the longest period when capacity is exceeded, implementable in O(1) via collections.OrderedDict.",
        "mechanics": "get(key): if key in cache, move to end (mark recent) and return value. put(key, value): if exists, update and move to end. If new and len == capacity, popitem(last=False) evicts oldest.",
        "takeaway": "OrderedDict combines hash map lookup with doubly linked list ordering to achieve strict O(1) LRU caching.",
        "sample_code": "# LRU Cache using collections.OrderedDict\nfrom collections import OrderedDict\nclass LRUCache:\n    def __init__(self, capacity):\n        self.cap = capacity\n        self.cache = OrderedDict()\n    def get(self, key):\n        if key not in self.cache: return -1\n        self.cache.move_to_end(key)\n        return self.cache[key]\n    def put(self, key, value):\n        if key in self.cache: self.cache.move_to_end(key)\n        self.cache[key] = value\n        if len(self.cache) > self.cap: self.cache.popitem(last=False)",
        "q1": "What does `popitem(last=False)` do in Python's `collections.OrderedDict`?",
        "q1_opts": [
            {"id": "A", "label": "Removes and returns the first (oldest / least recently used) key-value pair in O(1) time"},
            {"id": "B", "label": "Removes the newest item added to the dictionary"},
            {"id": "C", "label": "Wipes the entire dictionary"},
            {"id": "D", "label": "Sorts the dictionary in reverse order"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! `last=False` specifies FIFO eviction (head of the doubly linked list), removing the least recently used element.",
            "B": "Incorrect: `last=True` (default) removes the newest LIFO item.",
            "C": "Incorrect: popitem removes a single item.",
            "D": "Incorrect: No sorting is performed."
        },
        "q2": "What are the time complexities of `get()` and `put()` in a correctly implemented LRU Cache?",
        "q2_opts": [
            {"id": "A", "label": "Both get() and put() run in strict O(1) time"},
            {"id": "B", "label": "get() is O(1), but put() is O(N)"},
            {"id": "C", "label": "Both run in O(log N) time"},
            {"id": "D", "label": "Both run in O(N) time"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! Hash map provides O(1) key node lookup, and the doubly linked list provides O(1) pointer detachment and head/tail insertion.",
            "B": "Incorrect: put() operates in O(1) time.",
            "C": "Incorrect: No tree structures are used.",
            "D": "Incorrect: O(N) is unacceptable for production caches."
        },
        "practice_task": "Implement an LRU Cache using collections.OrderedDict.",
        "starter": "from collections import OrderedDict\n\nclass LRUCache:\n    def __init__(self, capacity: int):\n        # TODO: Initialize capacity and OrderedDict storage\n        pass\n\n    def get(self, key: int) -> int:\n        # TODO: If key exists, move_to_end and return value; else return -1\n        return -1\n\n    def put(self, key: int, value: int) -> None:\n        # TODO: Update or insert key; if over capacity, popitem(last=False)\n        pass\n\nlru = LRUCache(2)\nlru.put(1, 1)\nlru.put(2, 2)\nprint('Get key 1:', lru.get(1))  # 1 (moves key 1 to recent)\nlru.put(3, 3)                     # Evicts key 2!\nprint('Get key 2:', lru.get(2))  # -1 (evicted)\n",
        "solution": "from collections import OrderedDict\n\nclass LRUCache:\n    def __init__(self, capacity: int):\n        self.capacity = capacity\n        self.cache = OrderedDict()\n\n    def get(self, key: int) -> int:\n        if key not in self.cache:\n            return -1\n        self.cache.move_to_end(key)\n        return self.cache[key]\n\n    def put(self, key: int, value: int) -> None:\n        if key in self.cache:\n            self.cache.move_to_end(key)\n        self.cache[key] = value\n        if len(self.cache) > self.capacity:\n            self.cache.popitem(last=False)\n\nlru = LRUCache(2)\nlru.put(1, 1)\nlru.put(2, 2)\nprint('Get key 1:', lru.get(1))\nlru.put(3, 3)\nprint('Get key 2:', lru.get(2))\n",
        "patterns": ["Get key 1: 1", "Get key 2: -1"],
        "hint": "In get: if key in self.cache: self.cache.move_to_end(key); return self.cache[key]. In put: check key, assign, and if len > capacity: self.cache.popitem(last=False).",
        "recap": [
            {"concept": "Dual Data Structure", "naiveIntuition": "A hash map alone is sufficient for LRU", "pythonReality": "Hash maps have no inherent access recency ordering; pairing with a doubly linked list provides O(1) order manipulation"},
            {"concept": "Access as Mutation", "naiveIntuition": "get() is a read-only operation", "pythonReality": "In an LRU cache, get() mutates the access order, promoting the accessed key to the most recent position"}
        ]
    },
    74: {
        "summary": "LFU (Least Frequently Used) Cache evicts the element with the lowest access count, tie-breaking by least recently used, operating in strict O(1) time.",
        "mechanics": "Maintain a key-to-node map and a frequency-to-DLL map. Track min_freq. When get/put increments a key's count, detach from freq_map[f] and insert into freq_map[f+1]. Update min_freq in O(1).",
        "takeaway": "LFU requires two synchronized hash maps: key-to-node and frequency-to-doubly-linked-list.",
        "sample_code": "# LFU Cache architecture\n# key_to_node: key -> Node(key, val, freq)\n# freq_to_dll: freq -> DoublyLinkedList()\n# min_freq tracks lowest active frequency",
        "q1": "Why does an LFU Cache require tracking `min_freq` as a separate state variable?",
        "q1_opts": [
            {"id": "A", "label": "To evict the least frequently used key in strict O(1) time without scanning all frequency buckets"},
            {"id": "B", "label": "To prevent keys from having frequency 0"},
            {"id": "C", "label": "Because Python dictionaries cannot store frequencies"},
            {"id": "D", "label": "To limit the maximum cache size"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! When capacity is exceeded, eviction occurs from `freq_to_dll[min_freq]`. Tracking `min_freq` allows immediate O(1) access to the lowest-frequency bucket.",
            "B": "Incorrect: Initial frequency is 1.",
            "C": "Incorrect: Dictionaries can store any integers.",
            "D": "Incorrect: Capacity limits cache size."
        },
        "q2": "When an existing key's frequency increments from F to F+1, under what condition does `min_freq` increment by 1?",
        "q2_opts": [
            {"id": "A", "label": "When min_freq == F and the frequency bucket F becomes completely empty after the key is moved"},
            {"id": "B", "label": "On every single get() operation unconditionally"},
            {"id": "C", "label": "Only when a new key is inserted"},
            {"id": "D", "label": "Whenever F is an even number"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! If the moved key was the ONLY key in bucket `min_freq`, that frequency bucket is now empty, so the new minimum active frequency must be F + 1.",
            "B": "Incorrect: Other keys might remain at frequency F.",
            "C": "Incorrect: New keys reset `min_freq` to 1.",
            "D": "Incorrect: Parity has no effect on frequency logic."
        },
        "practice_task": "Design the frequency promotion step of an LFU Cache.",
        "starter": "# Day 74 Milestone: LFU Frequency Promotion Engine\nclass LFUSimulator:\n    def __init__(self):\n        self.key_freq = {}\n        self.freq_keys = {} # freq -> list of keys\n        self.min_freq = 0\n\n    def access(self, key: str) -> None:\n        # TODO: Increment key frequency, update freq_keys buckets and min_freq\n        pass\n\nlfu = LFUSimulator()\nlfu.access('A')\nlfu.access('B')\nlfu.access('A') # 'A' has freq 2, 'B' has freq 1\nprint('Min freq:', lfu.min_freq)\nprint('Keys at min freq:', lfu.freq_keys[lfu.min_freq])\n",
        "solution": "class LFUSimulator:\n    def __init__(self):\n        self.key_freq = {}\n        self.freq_keys = {}\n        self.min_freq = 0\n\n    def access(self, key: str) -> None:\n        if key not in self.key_freq:\n            self.key_freq[key] = 1\n            self.freq_keys.setdefault(1, []).append(key)\n            self.min_freq = 1\n        else:\n            old_f = self.key_freq[key]\n            new_f = old_f + 1\n            self.key_freq[key] = new_f\n            self.freq_keys[old_f].remove(key)\n            self.freq_keys.setdefault(new_f, []).append(key)\n            if self.min_freq == old_f and not self.freq_keys[old_f]:\n                self.min_freq = new_f\n\nlfu = LFUSimulator()\nlfu.access('A')\nlfu.access('B')\nlfu.access('A')\nprint('Min freq:', lfu.min_freq)\nprint('Keys at min freq:', lfu.freq_keys[lfu.min_freq])\n",
        "patterns": ["Min freq: 1", "Keys at min freq: ['B']"],
        "hint": "If key exists: old_f = key_freq[key], key_freq[key] = old_f + 1, move from freq_keys[old_f] to freq_keys[old_f + 1]. If old_f was min_freq and is now empty: min_freq += 1.",
        "recap": [
            {"concept": "Frequency Bucketing", "naiveIntuition": "Sort cache by frequency on eviction O(N log N)", "pythonReality": "Grouping keys into doubly linked lists by frequency enables O(1) promotions and evictions"},
            {"concept": "LRU Tie-Breaker", "naiveIntuition": "Any key with min_freq can be dropped", "pythonReality": "When multiple keys share the minimum frequency, the least recently used key among them is evicted"}
        ]
    },
    75: {
        "summary": "Section 6 Review synthesizes hash functions, collision resolution, frequency mapping, rolling hashes, and cache eviction architectures into a collision-resistant caching system.",
        "mechanics": "Evaluate hash table trade-offs: open addressing maximizes cache locality for small records; separate chaining avoids clustering and deletion tombstone overhead. Rolling hashes accelerate string search.",
        "takeaway": "Hash tables trade memory overhead for O(1) average access, powering caching and indexing across all software tiers.",
        "sample_code": "# Cache Eviction and Hash Table Synthesis\n# Load factor alpha = N / M. Keep alpha <= 0.66",
        "q1": "What is the primary advantage of Open Addressing over Separate Chaining in hardware performance?",
        "q1_opts": [
            {"id": "A", "label": "Open addressing stores all elements in a single contiguous array, exhibiting superior CPU cache line locality without pointer chasing"},
            {"id": "B", "label": "Open addressing can never become full"},
            {"id": "C", "label": "Open addressing avoids the need for hash functions"},
            {"id": "D", "label": "Open addressing runs in O(0) time"}
        ],
        "q1_ans": "A",
        "q1_exp": {
            "A": "Correct! Because all keys and values reside directly in contiguous slots, linear probing sweeps contiguous cache lines, drastically reducing memory bus latency compared to linked list pointers.",
            "B": "Incorrect: Open addressing tables CAN become 100% full.",
            "C": "Incorrect: Both techniques require hash functions.",
            "D": "Incorrect: Sub-O(1) complexity does not exist."
        },
        "q2": "In interview problems, when should you choose a Hash Set over a Boolean Array?",
        "q2_opts": [
            {"id": "A", "label": "When the domain of keys is sparse or unbounded (e.g. arbitrary strings, coordinates, or integers up to 10^9)"},
            {"id": "B", "label": "When all keys are integers from 0 to 25"},
            {"id": "C", "label": "When memory is severely limited to a few bytes"},
            {"id": "D", "label": "When keys must be kept sorted"}
        ],
        "q2_ans": "A",
        "q2_exp": {
            "A": "Correct! If keys span huge or non-integer ranges, allocating a boolean array of 10^9 elements is impossible. A hash set dynamically stores only the active N keys.",
            "B": "Incorrect: Bounded ranges [0..25] are faster with a fixed boolean array.",
            "C": "Incorrect: Hash sets have pointer and table overhead.",
            "D": "Incorrect: Sets are unordered; use trees for sorted keys."
        },
        "practice_task": "Build a collision-resistant Deduplication Filter with load factor monitoring.",
        "starter": "class DeduplicationFilter:\n    def __init__(self, capacity: int = 5):\n        self.capacity = capacity\n        self.buckets = [[] for _ in range(capacity)]\n        self.count = 0\n\n    def add(self, item: str) -> bool:\n        # TODO: Return False if item already exists\n        # Otherwise add item, increment count, and return True\n        return False\n\n    def load_factor(self) -> float:\n        return self.count / self.capacity\n\ndedup = DeduplicationFilter(5)\nprint('Add alpha:', dedup.add('alpha'))\nprint('Add beta:', dedup.add('beta'))\nprint('Add alpha again:', dedup.add('alpha'))\nprint('Load factor:', dedup.load_factor())\n",
        "solution": "class DeduplicationFilter:\n    def __init__(self, capacity: int = 5):\n        self.capacity = capacity\n        self.buckets = [[] for _ in range(capacity)]\n        self.count = 0\n\n    def add(self, item: str) -> bool:\n        b_idx = hash(item) % self.capacity\n        bucket = self.buckets[b_idx]\n        if item in bucket:\n            return False\n        bucket.append(item)\n        self.count += 1\n        return True\n\n    def load_factor(self) -> float:\n        return self.count / self.capacity\n\ndedup = DeduplicationFilter(5)\nprint('Add alpha:', dedup.add('alpha'))\nprint('Add beta:', dedup.add('beta'))\nprint('Add alpha again:', dedup.add('alpha'))\nprint('Load factor:', dedup.load_factor())\n",
        "patterns": ["Add alpha: True", "Add beta: True", "Add alpha again: False", "Load factor: 0.4"],
        "hint": "Compute b_idx = hash(item) % self.capacity. Check if item in self.buckets[b_idx]: if so return False. Else append, self.count += 1, and return True.",
        "recap": [
            {"concept": "Load Factor Monitoring", "naiveIntuition": "Tables manage memory automatically", "pythonReality": "In custom data structures, tracking load_factor = N / capacity triggers doubling resizes before performance drops"},
            {"concept": "Section 6 Synthesis", "naiveIntuition": "Hash tables only store simple key-values", "pythonReality": "Hash maps power LRU/LFU caches, rolling hash algorithms, graph adjacency lists, and dynamic programming memo tables"}
        ]
    }
}
