from .common import (
    CURRICULUM_MAP,
    get_difficulty,
    get_next_preview,
    make_explanation_step,
    make_checkpoint_step,
    make_practice_step,
    make_completion_step,
)

def get_sec2_part2_days():
    days = {}

    # DAY 15: Dictionaries: Hash Map Internals
    days[15] = {
        "dayNumber": 15,
        "title": "Dictionaries: Hash Map Internals",
        "topicName": "Hash Tables & Dicts",
        "sectionId": "python-core",
        "estimatedMinutes": 30,
        "difficulty": "FOUNDATIONAL",
        "prerequisites": [14],
        "concepts": ["Compact Dict Layout", "Hash Function __hash__", "Collision Probing", "O(1) Average Lookup"],
        "practiceSkills": ["Dictionary Key Hashing", "Collision Resolution Understanding", "Key Mutability Safety"],
        "steps": [
            make_explanation_step(
                "day15-step1", 1, "CPython's Compact Dict Architecture", "Dict Memory Layout",
                "How Python Achieves O(1) Average Lookup with Insertion-Ordered Compact Tables",
                "Explore the internal sparse index table and compact entries array introduced in Python 3.6.",
                [
                    "In Python 3.6+, dictionaries are **insertion-ordered** and memory-compact. Internally, a dictionary consists of two arrays:",
                    "1. A **sparse hash table (indices array)** storing small integer indices or `-1` (empty).",
                    "2. A **dense entries array** storing `[hash, key_pointer, value_pointer]` in the exact order keys were inserted.",
                    "When looking up `d[key]`, Python computes `h = hash(key)`. It computes index `idx = h & (size - 1)` into the sparse table to find the entry slot.",
                    "If two distinct keys hash to the same slot (a **collision**), Python resolves it using **open addressing with perturb-based probing** until an empty slot or the matching key is found."
                ],
                snippets=[{
                    "title": "Hashing and Object Identity",
                    "code": "key1 = 'name'\nkey2 = 'name'\nprint(hash(key1) == hash(key2)) # True\n\n# Dict preserves insertion order\nd = {'z': 1, 'a': 2, 'm': 3}\nprint(list(d.keys())) # ['z', 'a', 'm']",
                    "language": "python",
                    "caption": "Consistent hashing and guaranteed insertion order."
                }],
                callouts=[{
                    "type": "tip",
                    "title": "What Makes a Key Valid?",
                    "content": "A dictionary key must be **hashable**: it must implement `__hash__()` and `__eq__()`, and its hash value must never change during its lifetime. Mutable types (lists, dicts, sets) are unhashable."
                }],
                takeaway="CPython compact dicts combine sparse index arrays with dense entry tables for O(1) lookup and order preservation."
            ),
            make_explanation_step(
                "day15-step2", 2, "Hash Collisions & Amortized O(1)", "Collisions & Probing",
                "Collision Probing and Worst-Case O(N) Degradation",
                "Why hash lookups are O(1) average but can degrade under adversarial collisions.",
                [
                    "Because the universe of possible strings and numbers is infinite while the hash table size is finite, hash collisions are mathematically inevitable (by the Pigeonhole Principle).",
                    "When a collision occurs, Python computes a new probe offset: `idx = (5 * idx + 1 + perturb) & mask`. This pseudo-random walk visits every table slot without clustering.",
                    "When the table becomes ~66% full (load factor threshold 2/3), Python doubles table capacity to minimize collision chains.",
                    "While average lookup is $O(1)$, adversarial input causing all keys to collide degrades lookup to $O(N)$."
                ],
                snippets=[{
                    "title": "Safe Lookup with .get() and in",
                    "code": "counts = {'a': 10, 'b': 20}\n# O(1) membership check\nif 'c' in counts:\n    print(counts['c'])\n\n# O(1) safe retrieval with default\nprint(counts.get('c', 0)) # 0 (does not raise KeyError)",
                    "language": "python",
                    "caption": "Testing keys and defaulting safely."
                }],
                callouts=[{
                    "type": "warning",
                    "title": "Never Mutate a Key After Insertion",
                    "content": "If you use a custom object whose attributes change after being placed in a dict, its hash or equality might change, making the key permanently lost inside the table!"
                }],
                takeaway="Hash collisions are resolved via open addressing; tables resize at 2/3 load factor to maintain O(1) lookups."
            ),
            make_checkpoint_step(
                "day15-step3", 3, "Dict Internals Checkpoint", "Checkpoint",
                "Test Your Mastery of Hash Tables and Key Constraints",
                "Verify key requirements and complexity realities.",
                [
                    {
                        "id": "chk-d15-q1",
                        "question": "Which object CANNOT be used as a dictionary key?",
                        "options": [
                            {"id": "A", "label": "frozenset([1, 2, 3])"},
                            {"id": "B", "label": "(1, 2, 'hello')"},
                            {"id": "C", "label": "[1, 2, 3]"},
                            {"id": "D", "label": "42"}
                        ],
                        "correctOptionId": "C",
                        "explanations": {
                            "A": "Incorrect: frozenset is immutable and hashable.",
                            "B": "Incorrect: A tuple containing only immutable items is hashable.",
                            "C": "Correct! Lists are mutable containers and implement neither __hash__ nor fixed value invariants, raising TypeError: unhashable type: 'list'.",
                            "D": "Incorrect: Integers are immutable and hashable."
                        }
                    },
                    {
                        "id": "chk-d15-q2",
                        "question": "What is the average time complexity of key lookup in a Python dictionary?",
                        "options": [
                            {"id": "A", "label": "O(log N)"},
                            {"id": "B", "label": "O(1)"},
                            {"id": "C", "label": "O(N)"},
                            {"id": "D", "label": "O(N log N)"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: Binary search trees are O(log N), but hash tables are O(1).",
                            "B": "Correct! Hash tables map keys to indices in O(1) average time.",
                            "C": "Incorrect: O(N) is the theoretical worst case under pathological collisions.",
                            "D": "Incorrect: Lookups do not sort keys."
                        }
                    }
                ],
                takeaway="Only hashable immutable types can be dictionary keys; average lookup is O(1)."
            ),
            make_practice_step(
                "day15-step4", 4, "Build a Frequency Counter", "Practice",
                "Tally Character Frequencies Manually",
                "Implement a character tally using dictionary lookups and .get().",
                "Frequency Map Builder",
                [
                    "Given string `text = 'abracadabra'`.",
                    "Iterate over each character `ch` in `text`.",
                    "Use `freq[ch] = freq.get(ch, 0) + 1` to record the count.",
                    "Print the count for `'a'` and `'r'`."
                ],
                """# Day 15 Practice: Frequency Map Builder
text = "abracadabra"

freq = {}

# TODO: Count frequency of each character using .get(ch, 0)
for ch in text:
    pass

print("Count of a:", freq.get("a", 0))
print("Count of r:", freq.get("r", 0))
""",
                """text = "abracadabra"

freq = {}
for ch in text:
    freq[ch] = freq.get(ch, 0) + 1

print("Count of a:", freq.get("a", 0))
print("Count of r:", freq.get("r", 0))
""",
                ["Count of a: 5", "Count of r: 2"],
                "Use `freq[ch] = freq.get(ch, 0) + 1` inside the loop.",
                takeaway="The .get(key, default) method provides clean, KeyError-free dictionary accumulation."
            ),
            make_completion_step(
                "day15-step5", 5, "Dictionary Internals Mastery", "Recap",
                15, "Day 15 Complete: Dictionaries: Hash Map Internals",
                "You have mastered compact dictionary memory layout, open addressing, and key hashability rules.",
                [
                    {
                        "concept": "Dictionary Ordering",
                        "naiveIntuition": "Dictionaries are completely unordered collections",
                        "pythonReality": "Since Python 3.6+, dictionaries strictly preserve insertion order"
                    },
                    {
                        "concept": "Dict Keys",
                        "naiveIntuition": "Any Python object can be a dict key",
                        "pythonReality": "Only objects with immutable hash values and valid __eq__ can be keys"
                    }
                ],
                ["Compact Dict Architecture", "Hash Collisions & Probing", "Hashability Contract", ".get(key, default) Pattern"],
                get_next_preview(15)
            )
        ]
    }

    # DAY 16: Dictionary Methods & Patterns
    days[16] = {
        "dayNumber": 16,
        "title": "Dictionary Methods & Patterns",
        "topicName": "Dictionary Patterns",
        "sectionId": "python-core",
        "estimatedMinutes": 30,
        "difficulty": "FOUNDATIONAL",
        "prerequisites": [15],
        "concepts": ["setdefault & get", "Dict Comprehensions", "Dictionary Views", "Dict Merging ( | )"],
        "practiceSkills": ["setdefault Accumulation", "Dict Comprehensions", "Dynamic Key Merging"],
        "steps": [
            make_explanation_step(
                "day16-step1", 1, "setdefault & Dictionary Views", "setdefault & Views",
                "Accumulating Groups with setdefault and Dynamic Dict Views",
                "Group items cleanly and inspect dynamic dictionary views.",
                [
                    "`dict.setdefault(key, default)` returns the value if `key` is in the dict; if not, it inserts `key` with `default` and returns `default`.",
                    "This is ideal for grouping items into lists: `groups.setdefault(category, []).append(item)`.",
                    "Methods `.keys()`, `.values()`, and `.items()` return **dictionary views**. Views do not allocate new lists; they provide dynamic, live windows into the dictionary's internal entries that reflect additions or deletions immediately.",
                    "Dictionary keys views support set-like operations (`&`, `|`, `-`): `d1.keys() & d2.keys()` computes common keys in $O(\\min(N, M))$ time."
                ],
                snippets=[{
                    "title": "Grouping with setdefault and View Intersections",
                    "code": "groups = {}\nfor word in ['cat', 'car', 'apple', 'dog']:\n    groups.setdefault(word[0], []).append(word)\nprint(groups) # {'c': ['cat', 'car'], 'a': ['apple'], 'd': ['dog']}\n\n# Set operations on dict views\nd1 = {'a': 1, 'b': 2}\nd2 = {'b': 20, 'c': 30}\nprint(d1.keys() & d2.keys()) # {'b'}",
                    "language": "python",
                    "caption": "Live views and grouping patterns."
                }],
                callouts=[{
                    "type": "tip",
                    "title": "Dict Merge Operator (|)",
                    "content": "In Python 3.9+, you can merge dictionaries cleanly with `merged = d1 | d2`. Values in `d2` overwrite keys in `d1`."
                }],
                takeaway="setdefault groups values into containers in one line; dict views support set operations."
            ),
            make_explanation_step(
                "day16-step2", 2, "Dict Comprehensions & Inversion", "Dict Comprehensions",
                "Constructing and Inverting Dictionaries Elegantly",
                "Master `{k_expr: v_expr for item in iterable}` transformations.",
                [
                    "Dict comprehensions create dictionaries concisely: `{k: v for k, v in iterable}`.",
                    "A classic pattern is **dictionary inversion** (swapping keys and values): `{v: k for k, v in original.items()}`, assuming values are unique and hashable.",
                    "Comprehensions also support conditional filtering: `{k: v for k, v in scores.items() if v >= 60}`."
                ],
                snippets=[{
                    "title": "Inverting a Dictionary",
                    "code": "code_to_char = {65: 'A', 66: 'B', 67: 'C'}\nchar_to_code = {char: code for code, char in code_to_char.items()}\nprint(char_to_code) # {'A': 65, 'B': 66, 'C': 67}",
                    "language": "python",
                    "caption": "Inverting lookups with dict comprehensions."
                }],
                callouts=[{
                    "type": "warning",
                    "title": "Duplicate Values Overwrite",
                    "content": "When inverting `{ 'a': 1, 'b': 1 }`, the second item overwrites the first (`{ 1: 'b' }`). Use lists for multi-value inversions."
                }],
                takeaway="Dict comprehensions allow elegant filtering, mapping, and key-value inversion."
            ),
            make_checkpoint_step(
                "day16-step3", 3, "Dict Patterns Checkpoint", "Checkpoint",
                "Test Your Mastery of setdefault and Comprehensions",
                "Diagnose dictionary operations and merging.",
                [
                    {
                        "id": "chk-d16-q1",
                        "question": "What does `d.setdefault('items', []).append(10)` do if 'items' already exists with value `[1, 2]`?",
                        "options": [
                            {"id": "A", "label": "Overwrites 'items' with [10]"},
                            {"id": "B", "label": "Raises KeyError"},
                            {"id": "C", "label": "Appends 10 to the existing list, making it [1, 2, 10]"},
                            {"id": "D", "label": "Creates a new copy of the list"}
                        ],
                        "correctOptionId": "C",
                        "explanations": {
                            "A": "Incorrect: setdefault does not overwrite existing keys.",
                            "B": "Incorrect: setdefault never raises KeyError.",
                            "C": "Correct! Because 'items' is already present, setdefault returns the existing list `[1, 2]`, and `.append(10)` mutates it to `[1, 2, 10]`.",
                            "D": "Incorrect: It returns the existing reference in-place."
                        }
                    },
                    {
                        "id": "chk-d16-q2",
                        "question": "In Python 3.9+, what is the result of `{'a': 1, 'b': 2} | {'b': 99, 'c': 3}`?",
                        "options": [
                            {"id": "A", "label": "{'a': 1, 'b': 2, 'c': 3}"},
                            {"id": "B", "label": "{'a': 1, 'b': 99, 'c': 3}"},
                            {"id": "C", "label": "TypeError: unsupported operand type"},
                            {"id": "D", "label": "{'b': 99}"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: Right operand takes precedence on duplicate keys.",
                            "B": "Correct! The dictionary union operator `|` merges keys, with the right operand's value overwriting matching keys from the left operand.",
                            "C": "Incorrect: `|` is fully supported on dicts in Python 3.9+.",
                            "D": "Incorrect: Non-overlapping keys from both dictionaries are preserved."
                        }
                    }
                ],
                takeaway="setdefault returns existing references without overwriting; `|` merges with right-side precedence."
            ),
            make_practice_step(
                "day16-step4", 4, "Group Anagrams Preview", "Practice",
                "Group Words by Length Using setdefault",
                "Implement word length bucketing using setdefault.",
                "Word Length Bucket Aggregator",
                [
                    "Given `words = ['code', 'py', 'algo', 'mentor', 'ds', 'tree']`.",
                    "Group words by their length (`len(word)`) into `buckets` using `setdefault`.",
                    "Print the bucket for length 4 and length 2."
                ],
                """# Day 16 Practice: Word Length Bucket Aggregator
words = ["code", "py", "algo", "mentor", "ds", "tree"]

buckets = {}

# TODO: Group each word into buckets[len(word)] using setdefault
for w in words:
    pass

print("Length 4 words:", buckets.get(4))
print("Length 2 words:", buckets.get(2))
""",
                """words = ["code", "py", "algo", "mentor", "ds", "tree"]

buckets = {}
for w in words:
    buckets.setdefault(len(w), []).append(w)

print("Length 4 words:", buckets.get(4))
print("Length 2 words:", buckets.get(2))
""",
                ["Length 4 words: ['code', 'algo', 'tree']", "Length 2 words: ['py', 'ds']"],
                "Use `buckets.setdefault(len(w), []).append(w)`.",
                takeaway="setdefault streamlines grouping patterns across algorithms without nested if-checks."
            ),
            make_completion_step(
                "day16-step5", 5, "Dict Methods & Patterns Mastery", "Recap",
                16, "Day 16 Complete: Dictionary Methods & Patterns",
                "You have mastered setdefault grouping, dictionary views, and union operators.",
                [
                    {
                        "concept": "Dictionary Views",
                        "naiveIntuition": "dict.keys() creates a brand new copy list of keys",
                        "pythonReality": "It returns a lightweight live view reflecting dictionary changes in real time"
                    },
                    {
                        "concept": "setdefault Utility",
                        "naiveIntuition": "Always check `if k not in d:` before appending to list values",
                        "pythonReality": "setdefault(k, []).append(v) accomplishes check, initialization, and append in one line"
                    }
                ],
                ["setdefault Accumulation Pattern", "Dictionary Views & Set Operations", "Dict Comprehensions", "Merge Operator (|)"],
                get_next_preview(16)
            )
        ]
    }

    # DAY 17: Sets & Set Operations
    days[17] = {
        "dayNumber": 17,
        "title": "Sets: Set Theory & Operations",
        "topicName": "Set Theory & Invariants",
        "sectionId": "python-core",
        "estimatedMinutes": 30,
        "difficulty": "FOUNDATIONAL",
        "prerequisites": [16],
        "concepts": ["Set Theory Operations", "frozenset", "O(1) Membership", "Deduplication"],
        "practiceSkills": ["Set Operations (&, |, -, ^)", "O(1) Membership Testing", "Deduplication Invariants"],
        "steps": [
            make_explanation_step(
                "day17-step1", 1, "Set Architecture & O(1) Membership", "Set Architecture",
                "Sets as Value-Free Hash Maps with O(1) Membership Testing",
                "How Python sets achieve instantaneous lookups and automatic uniqueness.",
                [
                    "A `set` in Python is an unordered collection of unique, hashable elements. Under the hood, a set is implemented as a hash table with entry keys but no values.",
                    "Because sets use hashing, testing membership (`x in my_set`) takes **$O(1)$ average time**, compared to **$O(N)$** for lists!",
                    "In algorithmic problems, checking `if x in list` inside a loop degrades performance to $O(N^2)$. Converting the collection to a `set` drops total time to $O(N)$."
                ],
                snippets=[{
                    "title": "O(1) Membership vs O(N) List Lookup",
                    "code": "# Slow O(N) list search\nseen_list = [1, 2, 3, 4]\nprint(3 in seen_list) # O(N) scan\n\n# Fast O(1) set lookup\nseen_set = {1, 2, 3, 4}\nprint(3 in seen_set)  # O(1) hash lookup",
                    "language": "python",
                    "caption": "Replacing lists with sets for instant membership checks."
                }],
                callouts=[{
                    "type": "tip",
                    "title": "Creating an Empty Set",
                    "content": "To create an empty set, you MUST write `s = set()`. Writing `s = {}` creates an empty **dictionary**!"
                }],
                takeaway="Sets provide O(1) average membership checks; empty sets must be initialized with set()."
            ),
            make_explanation_step(
                "day17-step2", 2, "Mathematical Set Operations & frozenset", "Set Operations",
                "Union, Intersection, Difference, Symmetric Difference, and frozenset",
                "Expressive mathematical logic using set operators.",
                [
                    "Python sets support high-speed C-level mathematical operations:",
                    "- **Union (`a | b`)**: Elements in either `a` or `b`.",
                    "- **Intersection (`a & b`)**: Elements in both `a` and `b`.",
                    "- **Difference (`a - b`)**: Elements in `a` but not in `b`.",
                    "- **Symmetric Difference (`a ^ b`)**: Elements in either `a` or `b`, but not both.",
                    "A standard `set` is mutable and therefore unhashable. A `frozenset` is an immutable set that can be used as a dictionary key or placed inside another set."
                ],
                snippets=[{
                    "title": "Mathematical Set Operations",
                    "code": "frontend = {'HTML', 'CSS', 'JavaScript', 'React'}\nbackend = {'Python', 'SQL', 'JavaScript', 'Docker'}\n\n# Common skills (Intersection)\nprint('Common:', frontend & backend) # {'JavaScript'}\n\n# Frontend only (Difference)\nprint('Frontend only:', frontend - backend) # {'HTML', 'CSS', 'React'}",
                    "language": "python",
                    "caption": "Set theory operators in action."
                }],
                callouts=[{
                    "type": "warning",
                    "title": "Sets Do Not Preserve Order",
                    "content": "Do not rely on element order in sets! Iterating over a set produces elements in arbitrary hash table order."
                }],
                takeaway="Set operators (&, |, -, ^) execute in O(min(len(a), len(b))) time; frozenset is immutable and hashable."
            ),
            make_checkpoint_step(
                "day17-step3", 3, "Sets Checkpoint", "Checkpoint",
                "Test Your Mastery of Set Invariants",
                "Evaluate membership complexity, syntax, and operations.",
                [
                    {
                        "id": "chk-d17-q1",
                        "question": "What is the type of `obj = {}`?",
                        "options": [
                            {"id": "A", "label": "<class 'set'>"},
                            {"id": "B", "label": "<class 'dict'>"},
                            {"id": "C", "label": "SyntaxError"},
                            {"id": "D", "label": "<class 'frozenset'>"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: Empty curly braces {} always create a dictionary.",
                            "B": "Correct! Because dictionaries preceded sets in Python's history, {} denotes an empty dict. Empty sets must be created with set().",
                            "C": "Incorrect: {} is valid syntax.",
                            "D": "Incorrect: frozenset must be called explicitly."
                        }
                    },
                    {
                        "id": "chk-d17-q2",
                        "question": "What is the time complexity of `val in my_set` on a set with N items (assuming good hash distribution)?",
                        "options": [
                            {"id": "A", "label": "O(N)"},
                            {"id": "B", "label": "O(log N)"},
                            {"id": "C", "label": "O(1)"},
                            {"id": "D", "label": "O(N^2)"}
                        ],
                        "correctOptionId": "C",
                        "explanations": {
                            "A": "Incorrect: O(N) is the cost for lists or tuples.",
                            "B": "Incorrect: Sets are not trees.",
                            "C": "Correct! Set lookup hashes the key and checks the slot in O(1) average time.",
                            "D": "Incorrect: Hash lookup is constant time."
                        }
                    }
                ],
                takeaway="{} creates a dict, set() creates an empty set; membership testing is O(1)."
            ),
            make_practice_step(
                "day17-step4", 4, "Unique Visitor Analyzer", "Practice",
                "Find Unique and Common Log Visitors",
                "Analyze visitor overlap between two servers using set operations.",
                "Server Overlap Analyzer",
                [
                    "Given `srv1_logs = ['alice', 'bob', 'charlie', 'alice', 'dave']` and `srv2_logs = ['bob', 'dave', 'eve', 'frank']`.",
                    "Convert both logs to sets to eliminate duplicates.",
                    "Find `common_users` present on both servers using intersection (`&`).",
                    "Find `unique_all` present across either server using union (`|`).",
                    "Print `'Common users count:', len(common_users)` and `'Total unique visitors:', len(unique_all)`."
                ],
                """# Day 17 Practice: Server Overlap Analyzer
srv1_logs = ["alice", "bob", "charlie", "alice", "dave"]
srv2_logs = ["bob", "dave", "eve", "frank"]

# TODO 1: Convert to sets
s1 = set()
s2 = set()

# TODO 2: Compute common_users (intersection) and unique_all (union)
common_users = set()
unique_all = set()

print("Common users count:", len(common_users))
print("Total unique visitors:", len(unique_all))
""",
                """srv1_logs = ["alice", "bob", "charlie", "alice", "dave"]
srv2_logs = ["bob", "dave", "eve", "frank"]

s1 = set(srv1_logs)
s2 = set(srv2_logs)

common_users = s1 & s2
unique_all = s1 | s2

print("Common users count:", len(common_users))
print("Total unique visitors:", len(unique_all))
""",
                ["Common users count: 2", "Total unique visitors: 6"],
                "Convert logs with set(srv1_logs), then use s1 & s2 and s1 | s2.",
                takeaway="Set conversions automatically deduplicate sequences, and bitwise operators execute fast set algebra."
            ),
            make_completion_step(
                "day17-step5", 5, "Sets & Mathematical Operations Mastery", "Recap",
                17, "Day 17 Complete: Sets: Set Theory & Operations",
                "You have mastered set hashing, O(1) membership, mathematical operations, and frozenset.",
                [
                    {
                        "concept": "Empty Set Initialization",
                        "naiveIntuition": "s = {} creates an empty set",
                        "pythonReality": "s = {} creates an empty dictionary; use s = set()"
                    },
                    {
                        "concept": "Membership Complexity",
                        "naiveIntuition": "item in list is just as fast as item in set",
                        "pythonReality": "List search is O(N) linear scan; set search is O(1) hash lookup"
                    }
                ],
                ["O(1) Hash Membership Testing", "Set Theory Operators (&, |, -, ^)", "frozenset Hashable Collections", "Deduplication Invariants"],
                get_next_preview(17)
            )
        ]
    }

    # DAY 18: The Collections Module
    days[18] = {
        "dayNumber": 18,
        "title": "The Collections Module",
        "topicName": "collections Module",
        "sectionId": "python-core",
        "estimatedMinutes": 30,
        "difficulty": "FOUNDATIONAL",
        "prerequisites": [17],
        "concepts": ["collections.Counter", "defaultdict", "deque O(1) Pops", "OrderedDict"],
        "practiceSkills": ["Counter Tallying & most_common", "defaultdict Nesting", "deque O(1) Push/Pop"],
        "steps": [
            make_explanation_step(
                "day18-step1", 1, "Counter & defaultdict", "Counter & defaultdict",
                "Specialized Containers: collections.Counter and defaultdict",
                "Eliminate boilerplate counting and grouping code.",
                [
                    "`collections.Counter` is a dictionary subclass designed specifically for counting hashable objects. It initializes frequency tallies instantly: `c = Counter(iterable)`.",
                    "Accessing missing keys in a Counter returns `0` instead of raising `KeyError`.",
                    "`Counter.most_common(k)` returns the `k` most frequent elements in $O(N \\log k)$ time using an internal heap.",
                    "`collections.defaultdict(factory)` automatically calls `factory()` to generate default values whenever a non-existent key is accessed: `defaultdict(list)`, `defaultdict(int)`, `defaultdict(set)`."
                ],
                snippets=[{
                    "title": "Counter and defaultdict Usage",
                    "code": "from collections import Counter, defaultdict\n\n# Instant frequency tally\ncounts = Counter('banana')\nprint(counts) # Counter({'a': 3, 'n': 2, 'b': 1})\nprint(counts.most_common(1)) # [('a', 3)]\n\n# Auto-grouping without setdefault boilerplate\ngroups = defaultdict(list)\ngroups['fruits'].append('apple')",
                    "language": "python",
                    "caption": "Zero-boilerplate counting and auto-initializing groups."
                }],
                callouts=[{
                    "type": "tip",
                    "title": "most_common(K) Performance",
                    "content": "`Counter.most_common(k)` uses `heapq.nlargest` under the hood, running in $O(N \\log k)$ time without sorting the entire dictionary."
                }],
                takeaway="Counter tallies frequencies instantly; defaultdict creates missing keys automatically using a factory callable."
            ),
            make_explanation_step(
                "day18-step2", 2, "deque: Double-Ended Queue", "deque & O(1) Pops",
                "Why collections.deque is Essential for Breadth-First Search (BFS) and Queues",
                "Achieve true O(1) appends and pops from both ends.",
                [
                    "Python's `list` is a contiguous dynamic array, making `list.pop(0)` an $O(N)$ operation that shifts all elements.",
                    "`collections.deque` (double-ended queue) is implemented as a **doubly linked list of fixed-size blocks (chunks of 64 elements)**.",
                    "This architecture guarantees **$O(1)$ worst-case time complexity** for: `append()`, `appendleft()`, `pop()`, and `popleft()`!",
                    "Every queue, BFS algorithm, and sliding window buffer in Python MUST use `deque` rather than a standard `list`."
                ],
                snippets=[{
                    "title": "deque Operations",
                    "code": "from collections import deque\n\nq = deque([1, 2, 3])\nq.append(4)       # O(1) - push to right\nq.appendleft(0)   # O(1) - push to left\nfirst = q.popleft() # O(1) - pop from left (vital for BFS!)\nlast = q.pop()       # O(1) - pop from right\nprint('Queue remaining:', q) # deque([1, 2, 3])",
                    "language": "python",
                    "caption": "O(1) double-ended queue operations."
                }],
                callouts=[{
                    "type": "warning",
                    "title": "deque Random Access is O(N)",
                    "content": "While `deque` is $O(1)$ at both ends, indexing in the middle (`q[N//2]`) is $O(N)$! Use a list if you need fast random indexing."
                }],
                takeaway="deque provides true O(1) appends and pops at both ends, making it mandatory for queues and BFS."
            ),
            make_checkpoint_step(
                "day18-step3", 3, "Collections Checkpoint", "Checkpoint",
                "Test Your Mastery of Specialized Collections",
                "Evaluate queue performance and defaultdict behavior.",
                [
                    {
                        "id": "chk-d18-q1",
                        "question": "Why should you NEVER use `lst.pop(0)` for a queue of N items in algorithmic problems?",
                        "options": [
                            {"id": "A", "label": "It mutates the list"},
                            {"id": "B", "label": "It shifts all N-1 elements left in memory, making N pops cost O(N^2) total"},
                            {"id": "C", "label": "It raises IndexError on lists with even length"},
                            {"id": "D", "label": "It converts integers to floats"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: Queues are supposed to mutate state.",
                            "B": "Correct! Because lists are contiguous arrays, pop(0) takes O(N) time. Executing N pops results in quadratic O(N^2) time. Use collections.deque for O(1) popleft().",
                            "C": "Incorrect: pop(0) works on any non-empty list.",
                            "D": "Incorrect: pop(0) does not change types."
                        }
                    },
                    {
                        "id": "chk-d18-q2",
                        "question": "What happens when you access `c['missing']` on a `c = collections.Counter()`?",
                        "options": [
                            {"id": "A", "label": "Raises KeyError"},
                            {"id": "B", "label": "Returns None"},
                            {"id": "C", "label": "Returns 0 without raising an error"},
                            {"id": "D", "label": "Inserts 'missing': None"}
                        ],
                        "correctOptionId": "C",
                        "explanations": {
                            "A": "Incorrect: Counter overrides __missing__ to return 0.",
                            "B": "Incorrect: It returns numeric 0.",
                            "C": "Correct! Counter returns 0 for any missing key, making frequency comparisons seamless.",
                            "D": "Incorrect: It does not insert None."
                        }
                    }
                ],
                takeaway="pop(0) on a list is O(N) while deque.popleft() is O(1); Counter returns 0 for missing keys."
            ),
            make_practice_step(
                "day18-step4", 4, "Top-K Frequent Elements Preview", "Practice",
                "Find Most Frequent Words Using Counter",
                "Extract the top 2 most common words from a corpus.",
                "Top-K Word Frequency Extractor",
                [
                    "Given `text = 'apple banana apple orange banana apple grape banana'`.",
                    "Split the text into a list of words.",
                    "Use `collections.Counter` to tally word frequencies.",
                    "Extract the 2 most common words using `.most_common(2)`.",
                    "Print `'Top 2 words:', top_words`."
                ],
                """# Day 18 Practice: Top-K Word Frequency Extractor
from collections import Counter

text = "apple banana apple orange banana apple grape banana"

# TODO 1: Split text into words
words = text.split()

# TODO 2: Tally with Counter and extract most_common(2)
counts = Counter()
top_words = []

print("Top 2 words:", top_words)
""",
                """from collections import Counter

text = "apple banana apple orange banana apple grape banana"
words = text.split()

counts = Counter(words)
top_words = counts.most_common(2)

print("Top 2 words:", top_words)
""",
                ["Top 2 words: [('apple', 3), ('banana', 3)]"],
                "Initialize `counts = Counter(words)` then call `counts.most_common(2)`.",
                takeaway="Counter.most_common(k) solves frequency ranking problems efficiently."
            ),
            make_completion_step(
                "day18-step5", 5, "Collections Module Mastery", "Recap",
                18, "Day 18 Complete: The Collections Module",
                "You have mastered Counter, defaultdict, and O(1) double-ended queue mechanics.",
                [
                    {
                        "concept": "Queue Implementation",
                        "naiveIntuition": "Use list with append() and pop(0)",
                        "pythonReality": "list.pop(0) is O(N) and causes TLE; always use collections.deque with popleft()"
                    },
                    {
                        "concept": "Missing Key in Counter",
                        "naiveIntuition": "Counter['x'] raises KeyError if 'x' hasn't been added",
                        "pythonReality": "Counter returns 0 for missing keys without error"
                    }
                ],
                ["collections.Counter & most_common()", "defaultdict(factory) Pattern", "deque O(1) popleft() Invariant", "Avoid list.pop(0) Anti-Pattern"],
                get_next_preview(18)
            )
        ]
    }

    # DAY 19: Iterators & Iteration Protocol
    days[19] = {
        "dayNumber": 19,
        "title": "Iterators & Iteration Protocol",
        "topicName": "Iteration Protocol",
        "sectionId": "python-core",
        "estimatedMinutes": 30,
        "difficulty": "FOUNDATIONAL",
        "prerequisites": [18],
        "concepts": ["__iter__ and __next__", "StopIteration", "Iterable vs Iterator", "Sentinel iter()"],
        "practiceSkills": ["Custom Iterator Implementation", "Iteration State Tracking", "StopIteration Termination"],
        "steps": [
            make_explanation_step(
                "day19-step1", 1, "The Iteration Protocol Invariants", "Iteration Protocol",
                "How Python Loops Work: The __iter__() and __next__() Protocol",
                "Discover the universal contract driving Python's for loops, comprehensions, and unpacking.",
                [
                    "An **Iterable** is any object capable of returning an iterator. It implements `__iter__()`, which returns an iterator object.",
                    "An **Iterator** is an object representing a stream of data. It implements:",
                    "1. `__iter__()`: Returns `self`.",
                    "2. `__next__()`: Returns the next item from the stream. When no elements remain, it MUST raise `StopIteration`.",
                    "When you write `for item in collection:`, Python calls `it = iter(collection)`, then repeatedly calls `next(it)` inside a hidden loop until catching `StopIteration`."
                ],
                snippets=[{
                    "title": "Manual Simulation of for Loop",
                    "code": "items = [10, 20, 30]\n# What Python does behind the scenes:\nit = iter(items) # Calls items.__iter__()\nwhile True:\n    try:\n        val = next(it) # Calls it.__next__()\n        print(val)\n    except StopIteration:\n        break # End of stream reached!",
                    "language": "python",
                    "caption": "Explicit simulation of Python's iteration protocol."
                }],
                callouts=[{
                    "type": "tip",
                    "title": "Iterators are Consumable",
                    "content": "An iterator is a one-way stateful stream! Once exhausted, calling `next()` continues to raise `StopIteration`. You cannot reset an iterator; you must create a new one."
                }],
                takeaway="Iterables implement __iter__; iterators implement __iter__ and stateful __next__, terminating with StopIteration."
            ),
            make_explanation_step(
                "day19-step2", 2, "Building a Custom Iterator Class", "Custom Iterator",
                "Implementing State-Preserving Iterators with Bounds",
                "Write your own iterator class from scratch.",
                [
                    "To build a custom iterator class:",
                    "- Initialize state in `__init__` (e.g. current index or pointer).",
                    "- Return `self` in `__iter__()`.",
                    "- In `__next__()`, check boundaries. If within range, advance internal state and return the value; if out of range, raise `StopIteration`.",
                    "The two-argument form `iter(callable, sentinel)` repeatedly calls `callable()` until it returns `sentinel`, creating an instant iterator from functions."
                ],
                snippets=[{
                    "title": "Custom Countdown Iterator",
                    "code": "class Countdown:\n    def __init__(self, start):\n        self.current = start\n    def __iter__(self):\n        return self\n    def __next__(self):\n        if self.current <= 0:\n            raise StopIteration\n        val = self.current\n        self.current -= 1\n        return val\n\nfor num in Countdown(3):\n    print(num) # 3, 2, 1",
                    "language": "python",
                    "caption": "Stateful custom iterator class."
                }],
                callouts=[{
                    "type": "deep-dive",
                    "title": "Sentinel iter() Pattern",
                    "content": "`for block in iter(lambda: f.read(1024), b''):` reads chunks of a file until an empty bytes sentinel is returned."
                }],
                takeaway="Custom iterators preserve state between calls to __next__() and signal completion with StopIteration."
            ),
            make_checkpoint_step(
                "day19-step3", 3, "Iteration Protocol Checkpoint", "Checkpoint",
                "Test Your Mastery of the Iteration Protocol",
                "Evaluate iterator exhaustion and protocol methods.",
                [
                    {
                        "id": "chk-d19-q1",
                        "question": "What happens if you run a second `for` loop over an iterator that has already completed?",
                        "options": [
                            {"id": "A", "label": "It restarts from the beginning automatically"},
                            {"id": "B", "label": "The second loop does nothing because the iterator is exhausted"},
                            {"id": "C", "label": "Raises RuntimeError: Iterator reused"},
                            {"id": "D", "label": "Iterates in reverse"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: Iterators do not restart; they are stateful and one-way.",
                            "B": "Correct! Once an iterator raises StopIteration, all subsequent calls to next() immediately raise StopIteration, so the second loop exits with 0 iterations.",
                            "C": "Incorrect: Exhausted iterators do not raise RuntimeError.",
                            "D": "Incorrect: Iterators cannot traverse backwards."
                        }
                    },
                    {
                        "id": "chk-d19-q2",
                        "question": "What method must an object implement to be considered an ITERABLE (can be passed to `iter()`)?",
                        "options": [
                            {"id": "A", "label": "__next__()"},
                            {"id": "B", "label": "__iter__()"},
                            {"id": "C", "label": "__hash__()"},
                            {"id": "D", "label": "__len__()"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: __next__() is required by an iterator, not just an iterable.",
                            "B": "Correct! An iterable implements __iter__() returning an iterator.",
                            "C": "Incorrect: Hashability is for dictionary keys.",
                            "D": "Incorrect: Generators and streams do not need to know their length."
                        }
                    }
                ],
                takeaway="Iterators are one-way streams that exhaust once; iterables implement __iter__."
            ),
            make_practice_step(
                "day19-step4", 4, "Build an Even Number Stepper", "Practice",
                "Implement an EvenNumberIterator Class",
                "Write an iterator that yields even numbers up to a maximum limit.",
                "Even Number Iterator",
                [
                    "Create class `EvenStepper` that takes `max_limit` in `__init__` and initializes `self.current = 0`.",
                    "Implement `__iter__(self)` returning `self`.",
                    "Implement `__next__(self)`: while `self.current <= self.max_limit`, record the even number, increment `self.current += 2`, and return the number.",
                    "When `self.current > self.max_limit`, raise `StopIteration`.",
                    "Iterate over `EvenStepper(6)` and collect items into a list."
                ],
                """# Day 19 Practice: Even Number Iterator

class EvenStepper:
    def __init__(self, max_limit):
        self.max_limit = max_limit
        self.current = 0

    def __iter__(self):
        return self

    def __next__(self):
        # TODO: If self.current > self.max_limit, raise StopIteration
        # Otherwise save val = self.current, increment self.current by 2, and return val
        pass

evens = list(EvenStepper(6))
print("Evens:", evens)
""",
                """class EvenStepper:
    def __init__(self, max_limit):
        self.max_limit = max_limit
        self.current = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current > self.max_limit:
            raise StopIteration
        val = self.current
        self.current += 2
        return val

evens = list(EvenStepper(6))
print("Evens:", evens)
""",
                ["Evens: [0, 2, 4, 6]"],
                "Raise StopIteration when `self.current > self.max_limit`, otherwise advance and return.",
                takeaway="Custom iterator classes maintain pointer states and terminate cleanly with StopIteration."
            ),
            make_completion_step(
                "day19-step5", 5, "Iteration Protocol Mastery", "Recap",
                19, "Day 19 Complete: Iterators & Iteration Protocol",
                "You have mastered __iter__, __next__, StopIteration mechanics, and custom stream classes.",
                [
                    {
                        "concept": "Iterator Reuse",
                        "naiveIntuition": "Loops over an iterator can be run multiple times",
                        "pythonReality": "Iterators exhaust after one pass; you must obtain a new iterator from the iterable"
                    },
                    {
                        "concept": "Protocol Methods",
                        "naiveIntuition": "Iterables and iterators are the same thing",
                        "pythonReality": "Iterables create iterators via __iter__; iterators produce items via __next__"
                    }
                ],
                ["__iter__() & __next__() Contract", "StopIteration Signaling", "Stateful Stream Consumption", "Sentinel iter() Syntax"],
                get_next_preview(19)
            )
        ]
    }

    # DAY 20: Generators & Yield Semantics
    days[20] = {
        "dayNumber": 20,
        "title": "Generators & Yield Semantics",
        "topicName": "Generators & yield",
        "sectionId": "python-core",
        "estimatedMinutes": 30,
        "difficulty": "FOUNDATIONAL",
        "prerequisites": [19],
        "concepts": ["yield & yield from", "Generator Expressions", "Lazy Evaluation", "Memory Optimization"],
        "practiceSkills": ["Generator Function Authoring", "Lazy Pipeline Processing", "yield from Delegation"],
        "steps": [
            make_explanation_step(
                "day20-step1", 1, "The yield Keyword & Frame Suspension", "yield & Suspension",
                "How Generators Work: Suspending and Resuming Call Frames",
                "Generate infinite or massive data streams with fixed O(1) memory.",
                [
                    "A function containing the `yield` keyword is a **generator function**. Calling a generator function does NOT execute its body immediately; it returns a **generator object**.",
                    "When `next()` is called on the generator, Python executes bytecode until encountering `yield <value>`. It produces `<value>` and **suspends the execution frame**, freezing all local variables and instruction pointers in place.",
                    "On the next `next()` call, execution resumes immediately after the `yield` statement with all local state intact!",
                    "When the generator returns (or finishes), it automatically raises `StopIteration`."
                ],
                snippets=[{
                    "title": "Generator Execution Lifecycle",
                    "code": "def fibonacci():\n    a, b = 0, 1\n    while True:\n        yield a\n        a, b = b, a + b\n\n# Consuming infinite stream lazily with O(1) memory\nfib = fibonacci()\nfor _ in range(5):\n    print(next(fib)) # 0, 1, 1, 2, 3",
                    "language": "python",
                    "caption": "Infinite stream generator with O(1) memory footprint."
                }],
                callouts=[{
                    "type": "tip",
                    "title": "Memory Optimization",
                    "content": "Reading a 10 GB log file with a list crashes with `MemoryError`. Yielding line by line with a generator uses only a few kilobytes of RAM."
                }],
                takeaway="yield suspends the function frame, returning values lazily with O(1) auxiliary memory."
            ),
            make_explanation_step(
                "day20-step2", 2, "Generator Expressions & yield from", "yield from & GenExps",
                "Sub-generator Delegation and Lightweight Generator Expressions",
                "Chain generators cleanly and write inline lazy streams.",
                [
                    "A **generator expression** uses parentheses: `gen = (x * x for x in range(10))`. Unlike list comprehensions, it computes values on demand without allocating an array.",
                    "`yield from sub_gen` delegates iteration directly to a sub-generator, flattening nested streams efficiently without manual loops.",
                    "Passing a generator expression directly into functions like `sum()`, `min()`, or `max()` avoids double parentheses: `sum(x * x for x in nums)`."
                ],
                snippets=[{
                    "title": "yield from and GenExps in Action",
                    "code": "def flatten(nested):\n    for sublist in nested:\n        yield from sublist # Flattens sub-iterables cleanly\n\nprint(list(flatten([[1, 2], [3, 4]]))) # [1, 2, 3, 4]\n\n# Generator expression in sum()\ntotal = sum(x for x in range(100) if x % 2 == 0)",
                    "language": "python",
                    "caption": "Delegating iteration with yield from."
                }],
                callouts=[{
                    "type": "warning",
                    "title": "GenExp Exhaustion",
                    "content": "Just like iterators, generator expressions can only be consumed once! If you iterate over `g` twice, the second pass yields nothing."
                }],
                takeaway="yield from delegates to sub-generators; generator expressions provide lazy inline streams."
            ),
            make_checkpoint_step(
                "day20-step3", 3, "Generators Checkpoint", "Checkpoint",
                "Test Your Mastery of Generators and yield",
                "Evaluate frame suspension and generator memory consumption.",
                [
                    {
                        "id": "chk-d20-q1",
                        "question": "What happens when you call a function that contains a `yield` statement, e.g. `g = my_gen()`?",
                        "options": [
                            {"id": "A", "label": "The function executes completely up to the return statement"},
                            {"id": "B", "label": "It returns a generator iterator object without executing the function body yet"},
                            {"id": "C", "label": "It yields the first value immediately"},
                            {"id": "D", "label": "SyntaxError unless decorated with @generator"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: No code in the function runs upon calling my_gen().",
                            "B": "Correct! Calling a generator function instantiates and returns a generator object. Code execution only begins when next(g) is invoked.",
                            "C": "Incorrect: The first yield is reached only after next(g) is called.",
                            "D": "Incorrect: yield is a native Python keyword requiring no decorator."
                        }
                    },
                    {
                        "id": "chk-d20-q2",
                        "question": "What is the primary memory advantage of `(x for x in range(10**8))` over `[x for x in range(10**8)]`?",
                        "options": [
                            {"id": "A", "label": "The generator expression compiles to C code"},
                            {"id": "B", "label": "The generator consumes O(1) memory because elements are produced on-the-fly, while the list allocates gigabytes for all 100M pointers upfront"},
                            {"id": "C", "label": "The generator runs multithreaded"},
                            {"id": "D", "label": "There is no difference"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: Both run in CPython bytecode.",
                            "B": "Correct! List comprehensions build the complete pointer array in RAM, whereas generator expressions evaluate lazily with O(1) memory overhead.",
                            "C": "Incorrect: Generators run synchronously in the single-threaded interpreter.",
                            "D": "Incorrect: The memory difference is massive (gigabytes vs bytes)."
                        }
                    }
                ],
                takeaway="Calling a generator function returns a lazy generator object; generator expressions consume O(1) memory."
            ),
            make_practice_step(
                "day20-step4", 4, "Build a Windowed Batch Generator", "Practice",
                "Stream Elements in Fixed-Size Batches",
                "Write a generator function that yields items in chunks of size K.",
                "Batch Stream Chunking Generator",
                [
                    "Write a generator function `batch_stream(items, batch_size)`.",
                    "Loop through `items` using index steps: `for i in range(0, len(items), batch_size):`.",
                    "Yield the slice `items[i : i + batch_size]`.",
                    "Test it on `data = [1, 2, 3, 4, 5, 6, 7]` with `batch_size = 3`.",
                    "Collect the batches into a list and print `'Batches:', batches`."
                ],
                """# Day 20 Practice: Batch Stream Chunking Generator

def batch_stream(items, batch_size):
    # TODO: Loop i from 0 to len(items) with step batch_size
    # and yield slice items[i : i + batch_size]
    pass

data = [1, 2, 3, 4, 5, 6, 7]
batches = list(batch_stream(data, 3))
print("Batches:", batches)
""",
                """def batch_stream(items, batch_size):
    for i in range(0, len(items), batch_size):
        yield items[i : i + batch_size]

data = [1, 2, 3, 4, 5, 6, 7]
batches = list(batch_stream(data, 3))
print("Batches:", batches)
""",
                ["Batches: [[1, 2, 3], [4, 5, 6], [7]]"],
                "Use `yield items[i : i + batch_size]` inside `for i in range(0, len(items), batch_size):`.",
                takeaway="Generators decompose bulk collections into lazy chunks without allocating duplicate outer structures."
            ),
            make_completion_step(
                "day20-step5", 5, "Generators & Yield Mastery", "Recap",
                20, "Day 20 Complete: Generators & Yield Semantics",
                "You have mastered frame suspension, lazy stream evaluation, and yield from delegation.",
                [
                    {
                        "concept": "Function Invocation",
                        "naiveIntuition": "Calling gen_func() runs the code immediately",
                        "pythonReality": "It returns a suspended generator object; code runs only when next() is called"
                    },
                    {
                        "concept": "Memory Consumption",
                        "naiveIntuition": "Generating millions of items requires millions of memory slots",
                        "pythonReality": "Generators compute items on demand with fixed O(1) memory"
                    }
                ],
                ["yield Frame Suspension Mechanics", "O(1) Memory Streams", "yield from Sub-generator Delegation", "Generator Expressions vs Comprehensions"],
                get_next_preview(20)
            )
        ]
    }

    return days
