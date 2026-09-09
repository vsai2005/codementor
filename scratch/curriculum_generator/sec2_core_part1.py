from .common import (
    CURRICULUM_MAP,
    get_difficulty,
    get_next_preview,
    make_explanation_step,
    make_checkpoint_step,
    make_practice_step,
    make_completion_step,
)

def get_sec2_days():
    days = {}

    # DAY 11: Lists: Memory Layout & Operations
    days[11] = {
        "dayNumber": 11,
        "title": "Lists: Memory Layout & Operations",
        "topicName": "Dynamic Arrays",
        "sectionId": "python-core",
        "estimatedMinutes": 30,
        "difficulty": "FOUNDATIONAL",
        "prerequisites": [10],
        "concepts": ["Dynamic Array Internals", "Amortized O(1)", "append vs insert", "Over-allocation"],
        "practiceSkills": ["List Construction", "Amortized Cost Analysis", "In-Place Modifications"],
        "steps": [
            make_explanation_step(
                "day11-step1", 1, "CPython List Memory Layout", "Memory Layout",
                "How Python Lists Work Under the Hood: Contiguous Pointer Arrays",
                "Discover why Python lists are dynamic arrays of pointers, not linked lists.",
                [
                    "In CPython, a `list` is implemented as a variable-length contiguous array of pointers to objects (`PyObject**`). The list itself does not store the objects directly; it stores 64-bit memory addresses pointing to the objects on the heap.",
                    "Because pointers are laid out contiguously in memory, indexing (`lst[i]`) is an immediate $O(1)$ arithmetic pointer offset: `base_address + i * 8 bytes`.",
                    "When appending items, CPython uses an over-allocation strategy: when capacity is exceeded, it allocates extra headroom (approx. growth factor ~1.125x + 3 to 6 slots). This guarantees that `append()` has an **amortized $O(1)$** time complexity."
                ],
                snippets=[{
                    "title": "List Pointer Array Mechanics",
                    "code": "import sys\nitems = []\nprint('Initial size:', sys.getsizeof(items))\nfor i in range(10):\n    items.append(i)\n    print(f'Len: {len(items)}, Size in bytes: {sys.getsizeof(items)}')",
                    "language": "python",
                    "caption": "Watching CPython resize and over-allocate capacity in bursts."
                }],
                callouts=[{
                    "type": "tip",
                    "title": "Amortized O(1) append",
                    "content": "Most `append()` calls take O(1) time. Occasionally a resize takes O(N) to copy pointers, but amortized across all appends, each append costs O(1)."
                }],
                takeaway="Lists are contiguous pointer arrays providing O(1) indexing and amortized O(1) appending."
            ),
            make_explanation_step(
                "day11-step2", 2, "append vs insert & pop Complexity", "Cost Trade-offs",
                "Why insert(0, x) is O(N) While append(x) is O(1)",
                "Understanding the computational cost of shifting array elements.",
                [
                    "Adding to the end with `lst.append(x)` is amortized $O(1)$ because no other elements shift.",
                    "Inserting at the beginning with `lst.insert(0, x)` or popping from the beginning with `lst.pop(0)` is $O(N)$! Every existing pointer in the array must be shifted by one memory slot.",
                    "Popping from the end `lst.pop()` is $O(1)$ because no element shifting is required.",
                    "If you frequently add or remove items from the front of a sequence, use `collections.deque` ($O(1)$ at both ends) instead of a list."
                ],
                snippets=[{
                    "title": "Operation Complexities",
                    "code": "lst = [10, 20, 30]\nlst.append(40) # O(1) amortized - appends at end\nlst.pop()       # O(1) - removes from end\nlst.insert(0, 5) # O(N) - shifts all elements right!\nlst.pop(0)      # O(N) - shifts all elements left!",
                    "language": "python",
                    "caption": "Operations at the front shift all elements, costing O(N)."
                }],
                callouts=[{
                    "type": "warning",
                    "title": "Queue Anti-Pattern",
                    "content": "Never use `list.pop(0)` as a queue in algorithmic problems! N pops from a list will degrade your algorithm to $O(N^2)$."
                }],
                takeaway="append and pop at the end are O(1); insert and pop at index 0 require O(N) shifts."
            ),
            make_checkpoint_step(
                "day11-step3", 3, "List Operations Checkpoint", "Checkpoint",
                "Verify Your Understanding of List Complexities",
                "Test your knowledge of pointer arrays and shifting costs.",
                [
                    {
                        "id": "chk-d11-q1",
                        "question": "What is the time complexity of `lst.insert(0, val)` on a list of length N?",
                        "options": [
                            {"id": "A", "label": "O(1)"},
                            {"id": "B", "label": "O(log N)"},
                            {"id": "C", "label": "O(N)"},
                            {"id": "D", "label": "O(N^2)"}
                        ],
                        "correctOptionId": "C",
                        "explanations": {
                            "A": "Incorrect: Inserting at the beginning requires moving all existing elements.",
                            "B": "Incorrect: Lists do not use tree-based structures.",
                            "C": "Correct! Because lists are contiguous arrays, inserting at index 0 requires shifting all N existing pointers one position to the right.",
                            "D": "Incorrect: A single insert is O(N), not quadratic."
                        }
                    },
                    {
                        "id": "chk-d11-q2",
                        "question": "What does a Python list actually store in its contiguous memory buffer?",
                        "options": [
                            {"id": "A", "label": "The raw bytes of each number and string packed directly"},
                            {"id": "B", "label": "64-bit pointers (memory addresses) pointing to objects on the heap"},
                            {"id": "C", "label": "A doubly linked list of node structs"},
                            {"id": "D", "label": "A hash table of indices to values"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: That is what array.array or NumPy does; Python lists store pointers.",
                            "B": "Correct! Python lists are arrays of PyObject* pointers, which allows them to store heterogeneous object types dynamically.",
                            "C": "Incorrect: Python lists are dynamic arrays, not linked lists.",
                            "D": "Incorrect: Indices are array offsets, not hash table keys."
                        }
                    }
                ],
                takeaway="Lists store contiguous object pointers; inserting at index 0 requires O(N) shifts."
            ),
            make_practice_step(
                "day11-step4", 4, "Efficient In-Place Operations", "Practice",
                "Filter and Reverse Array In-Place",
                "Manipulate list pointers efficiently using in-place methods.",
                "In-Place List Processing",
                [
                    "Given `nums = [12, 5, 8, 19, 24, 7, 10]`.",
                    "Filter `nums` in-place so it retains only numbers greater than 10 (or build a filtered list).",
                    "Reverse the resulting list in-place using `.reverse()`.",
                    "Print `'Processed list:', nums`."
                ],
                """# Day 11 Practice: In-Place List Processing
nums = [12, 5, 8, 19, 24, 7, 10]

# TODO 1: Filter nums to retain only numbers greater than 10
# (Build a list of numbers > 10 or filter in a loop)
nums = []

# TODO 2: Reverse nums in-place by calling nums.reverse()

print("Processed list:", nums)
""",
                """nums = [12, 5, 8, 19, 24, 7, 10]
nums = [x for x in nums if x > 10]
nums.reverse()

print("Processed list:", nums)
""",
                ["Processed list: [24, 19, 12]"],
                "Filter elements with `[x for x in nums if x > 10]` then call `nums.reverse()`.",
                takeaway="List methods like .reverse() mutate the list in-place in O(N) time with O(1) extra space."
            ),
            make_completion_step(
                "day11-step5", 5, "Lists & Memory Layout Mastery", "Recap",
                11, "Day 11 Complete: Lists: Memory Layout & Operations",
                "You have mastered contiguous pointer arrays, amortized resizing, and operation costs.",
                [
                    {
                        "concept": "List Storage",
                        "naiveIntuition": "Lists store items directly inside contiguous slots",
                        "pythonReality": "Lists store contiguous 64-bit pointers referencing independent heap objects"
                    },
                    {
                        "concept": "pop(0) Performance",
                        "naiveIntuition": "Popping from the front is as fast as popping from the end",
                        "pythonReality": "pop(0) is O(N) because every remaining pointer must shift left"
                    }
                ],
                ["Contiguous Pointer Array Layout", "Amortized O(1) Over-Allocation", "insert(0) vs append() Costs", "In-Place List Mutation"],
                get_next_preview(11)
            )
        ]
    }

    # DAY 12: List Slicing & Mutability Traps
    days[12] = {
        "dayNumber": 12,
        "title": "List Slicing & Mutability Traps",
        "topicName": "List Slicing & Copies",
        "sectionId": "python-core",
        "estimatedMinutes": 30,
        "difficulty": "FOUNDATIONAL",
        "prerequisites": [11],
        "concepts": ["Shallow vs Deep Copy", "copy module", "Slice Assignment", "is vs =="],
        "practiceSkills": ["Shallow vs Deep Copying", "Slice Mutation", "Reference Isolation"],
        "steps": [
            make_explanation_step(
                "day12-step1", 1, "Shallow vs Deep Copies", "Shallow vs Deep Copy",
                "The Shallow Copy Hazard with Nested Mutable Objects",
                "Learn why slice copies only copy outer pointers, leaving inner objects shared.",
                [
                    "When you slice a list with `new_list = old_list[:]` or call `old_list.copy()`, Python performs a **shallow copy**.",
                    "A shallow copy creates a new outer list container, but it copies the exact same object pointers from the original list.",
                    "If the list contains mutable child objects (like nested lists `[[1, 2], [3, 4]]`), mutating an inner list through `new_list[0].append(99)` also mutates `old_list[0]`!",
                    "To create a completely independent duplicate including all nested sub-objects, use `copy.deepcopy()`."
                ],
                snippets=[{
                    "title": "Shallow Copy Hazard",
                    "code": "import copy\norig = [[1, 2], [3, 4]]\nshallow = orig[:]        # Shallow copy\ndeep = copy.deepcopy(orig) # Deep copy\n\nshallow[0].append(99) # Mutates orig[0] as well!\ndeep[1].append(88)    # Does NOT mutate orig[1]\nprint('Original:', orig)",
                    "language": "python",
                    "caption": "Shallow copies share pointers to nested mutable children."
                }],
                callouts=[{
                    "type": "warning",
                    "title": "The [[0] * N] * M Trap",
                    "content": "`grid = [[0] * 3] * 3` creates 3 references to the EXACT SAME row list! Mutating `grid[0][0] = 1` turns the entire column into 1s. Always write `[[0] * 3 for _ in range(3)]`."
                }],
                takeaway="Shallow copies duplicate the outer pointer buffer; deepcopy clones all nested objects."
            ),
            make_explanation_step(
                "day12-step2", 2, "Slice Assignment Mechanics", "Slice Assignment",
                "Replacing, Inserting, and Deleting Slices In-Place",
                "Powerful in-place mutations using target slices.",
                [
                    "Slice assignment `lst[start:stop] = iterable` replaces the targeted slice range with elements from the iterable in-place.",
                    "Unlike item assignment (`lst[0] = x`), slice assignment can expand or contract the list length: `lst[1:3] = [10, 20, 30, 40]` expands the list.",
                    "Assigning an empty list `lst[1:3] = []` deletes that slice in-place.",
                    "`lst[:] = new_items` replaces all elements in-place while **preserving the original list identity (`id(lst)`)**."
                ],
                snippets=[{
                    "title": "Slice Assignment in Action",
                    "code": "nums = [1, 2, 3, 4, 5]\nnums[1:4] = [20, 30] # Replaces [2, 3, 4] with [20, 30]\nprint(nums)          # [1, 20, 30, 5]\n\nnums[:] = [99]       # In-place wipe and replace\nprint(nums)          # [99]",
                    "language": "python",
                    "caption": "Slice assignment modifies length and contents in-place."
                }],
                callouts=[{
                    "type": "tip",
                    "title": "Pass by Reference In-Place Mutation",
                    "content": "In LeetCode problems requiring in-place modification (like 'Remove Duplicates'), `nums[:] = clean_nums` modifies the caller's array directly."
                }],
                takeaway="Slice assignment modifies list contents and lengths in-place while keeping the object ID intact."
            ),
            make_checkpoint_step(
                "day12-step3", 3, "Copies & Slices Checkpoint", "Checkpoint",
                "Test Your Mastery of Copies and Slice Assignment",
                "Diagnose shared references and slice replacements.",
                [
                    {
                        "id": "chk-d12-q1",
                        "question": "What is the content of `matrix` after running this code?\n\n```python\nmatrix = [[0] * 2] * 2\nmatrix[0][0] = 7\n```",
                        "options": [
                            {"id": "A", "label": "[[7, 0], [0, 0]]"},
                            {"id": "B", "label": "[[7, 0], [7, 0]]"},
                            {"id": "C", "label": "[[7, 7], [0, 0]]"},
                            {"id": "D", "label": "TypeError: cannot mutate nested lists"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: The two rows are not independent lists.",
                            "B": "Correct! `[row] * 2` duplicates the pointer to the same row object twice. Modifying row 0 modifies row 1 simultaneously.",
                            "C": "Incorrect: Only index 0 of the shared row was updated.",
                            "D": "Incorrect: Lists are mutable; no TypeError occurs."
                        }
                    },
                    {
                        "id": "chk-d12-q2",
                        "question": "What is the difference between `a = b[:]` and `a = copy.deepcopy(b)` when `b = [[1, 2]]`?",
                        "options": [
                            {"id": "A", "label": "There is no difference"},
                            {"id": "B", "label": "b[:] creates a shallow copy where a[0] is b[0]; deepcopy creates an independent inner list"},
                            {"id": "C", "label": "deepcopy is faster and uses less memory"},
                            {"id": "D", "label": "b[:] mutates b"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: Shallow vs deep copy handle inner references differently.",
                            "B": "Correct! Slicing copies outer pointers, so a[0] is b[0] is True. deepcopy recursively duplicates all child objects.",
                            "C": "Incorrect: deepcopy is slower due to recursive traversal and memoization.",
                            "D": "Incorrect: Slicing does not mutate the source list."
                        }
                    }
                ],
                takeaway="Multiplication of lists duplicates pointers; deepcopy recursively duplicates nested objects."
            ),
            make_practice_step(
                "day12-step4", 4, "Build 2D Grid Safely", "Practice",
                "Construct an Independent 2D Matrix",
                "Create a 3x3 matrix where each row is an independent list object.",
                "Safe 2D Matrix Creator",
                [
                    "Build a 3-row by 3-column matrix initialized with zeroes using a list comprehension: `[[0] * 3 for _ in range(3)]`.",
                    "Set the center cell `matrix[1][1] = 5`.",
                    "Set top-left cell `matrix[0][0] = 1` and bottom-right cell `matrix[2][2] = 9`.",
                    "Print row 0, row 1, and row 2 on separate lines."
                ],
                """# Day 12 Practice: Safe 2D Matrix Creator

# TODO 1: Construct a 3x3 grid with independent rows using list comprehension
matrix = []

# TODO 2: Update specific coordinates
# matrix[0][0] = 1
# matrix[1][1] = 5
# matrix[2][2] = 9

for row in matrix:
    print(row)
""",
                """matrix = [[0] * 3 for _ in range(3)]
matrix[0][0] = 1
matrix[1][1] = 5
matrix[2][2] = 9

for row in matrix:
    print(row)
""",
                ["[1, 0, 0]", "[0, 5, 0]", "[0, 0, 9]"],
                "Use `matrix = [[0] * 3 for _ in range(3)]` then assign individual cell coordinates.",
                takeaway="List comprehensions evaluate the row constructor on each iteration, creating separate objects."
            ),
            make_completion_step(
                "day12-step5", 5, "List Copies & Slices Mastery", "Recap",
                12, "Day 12 Complete: List Slicing & Mutability Traps",
                "You have mastered shallow vs deep copies, grid construction, and in-place slice replacement.",
                [
                    {
                        "concept": "Grid Initialization",
                        "naiveIntuition": "[[0]*C]*R creates an R x C matrix with independent rows",
                        "pythonReality": "It duplicates the reference to the same row R times; always use comprehension"
                    },
                    {
                        "concept": "Slice Assignment",
                        "naiveIntuition": "lst[1:3] = [99] causes an error because lengths don't match",
                        "pythonReality": "Slice assignment dynamically adjusts length and replaces the slice in-place"
                    }
                ],
                ["Shallow Copying Mechanics", "copy.deepcopy() Usage", "Slice Assignment In-Place", "The [[0]*C]*R Reference Trap"],
                get_next_preview(12)
            )
        ]
    }

    # DAY 13: List Comprehensions & Expressions
    days[13] = {
        "dayNumber": 13,
        "title": "List Comprehensions & Expressions",
        "topicName": "List Comprehensions",
        "sectionId": "python-core",
        "estimatedMinutes": 25,
        "difficulty": "FOUNDATIONAL",
        "prerequisites": [12],
        "concepts": ["List Comprehensions", "Filtering Syntax", "Nested Comprehensions", "Bytecode Speed"],
        "practiceSkills": ["Comprehension Construction", "Multi-Condition Filtering", "Matrix Flattening"],
        "steps": [
            make_explanation_step(
                "day13-step1", 1, "Comprehension Syntax & Performance", "Comprehension Syntax",
                "Expressive Transformation: [expr for item in iterable if condition]",
                "Why list comprehensions are faster and more idiomatic than explicit append loops.",
                [
                    "A list comprehension constructs a new list by applying an expression to each item in an iterable, with optional filtering: `[expr for item in iterable if condition]`.",
                    "List comprehensions are not just syntactic sugar: at the CPython bytecode level, they execute via a dedicated `LIST_APPEND` instruction inside an optimized loop frame, running ~20-30% faster than manual `for` loops with `.append()`.",
                    "Multiple `if` conditions act as logical `and` filters: `[x for x in nums if x > 0 if x % 2 == 0]`."
                ],
                snippets=[{
                    "title": "Comprehensions vs for loops",
                    "code": "# Manual loop:\nevens = []\nfor x in range(10):\n    if x % 2 == 0:\n        evens.append(x * x)\n\n# Pythonic Comprehension (faster & cleaner):\nevens_comp = [x * x for x in range(10) if x % 2 == 0]",
                    "language": "python",
                    "caption": "Concise and fast transformation with list comprehensions."
                }],
                callouts=[{
                    "type": "tip",
                    "title": "Bytecode Efficiency",
                    "content": "List comprehensions bypass Python-level attribute lookups (`.append`) by calling CPython's internal list-resizing macro directly."
                }],
                takeaway="List comprehensions run faster than append loops and provide declarative data transformations."
            ),
            make_explanation_step(
                "day13-step2", 2, "Nested Comprehensions & Flattening", "Nested Comprehensions",
                "Matrix Flattening and Multi-Loop Comprehensions",
                "Master the reading order of nested comprehensions: outer loops come first.",
                [
                    "When writing nested comprehensions, the `for` clauses appear in the exact same order as nested loops:",
                    "```python\n# Flattening a 2D matrix:\nflattened = [val for row in matrix for val in row]\n```",
                    "Notice the order: first `for row in matrix`, then `for val in row`.",
                    "For conditional transformations, place `if-else` before the `for`: `[x if x > 0 else 0 for x in nums]` (ternary expression)."
                ],
                snippets=[{
                    "title": "Nested Comprehensions and Ternary Placements",
                    "code": "matrix = [[1, 2], [3, 4], [5, 6]]\nflat = [x for row in matrix for x in row] # [1, 2, 3, 4, 5, 6]\n\n# Ternary transformation:\nclamped = [x if x >= 0 else 0 for x in [-2, 5, -1, 8]] # [0, 5, 0, 8]",
                    "language": "python",
                    "caption": "Loop order matches nested indentation order."
                }],
                callouts=[{
                    "type": "warning",
                    "title": "Readability Rule",
                    "content": "Do not nest more than two loops inside a single comprehension. Deeply nested comprehensions hurt readability; use normal loops instead."
                }],
                takeaway="In nested comprehensions, outer loops come first; ternary if-else goes before the for clause."
            ),
            make_checkpoint_step(
                "day13-step3", 3, "Comprehensions Checkpoint", "Checkpoint",
                "Test Your Mastery of Comprehensions",
                "Verify comprehension syntax, ordering, and filtering.",
                [
                    {
                        "id": "chk-d13-q1",
                        "question": "What is the result of `[x * 2 for x in [1, 2, 3] if x > 1]`?",
                        "options": [
                            {"id": "A", "label": "[2, 4, 6]"},
                            {"id": "B", "label": "[4, 6]"},
                            {"id": "C", "label": "[2, 3]"},
                            {"id": "D", "label": "[4]"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: x = 1 is filtered out by `if x > 1`.",
                            "B": "Correct! Elements > 1 are 2 and 3; multiplying by 2 yields [4, 6].",
                            "C": "Incorrect: The expression x * 2 was not applied.",
                            "D": "Incorrect: Both 2 and 3 satisfy the filter."
                        }
                    },
                    {
                        "id": "chk-d13-q2",
                        "question": "Where does a conditional ternary (`val_true if cond else val_false`) belong in a comprehension?",
                        "options": [
                            {"id": "A", "label": "At the very end: `[x for x in nums if cond else val]`"},
                            {"id": "B", "label": "At the beginning as the output expression: `[x if cond else val for x in nums]`"},
                            {"id": "C", "label": "Ternary expressions are illegal in comprehensions"},
                            {"id": "D", "label": "Inside parentheses after `in`"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: The trailing `if` is strictly for filtering items in or out.",
                            "B": "Correct! When transforming elements conditionally with if/else, the ternary expression acts as the output expression before the `for`.",
                            "C": "Incorrect: Ternary expressions are widely used in comprehensions.",
                            "D": "Incorrect: Syntax error."
                        }
                    }
                ],
                takeaway="Filtering conditions go at the end; transformation ternaries go at the beginning."
            ),
            make_practice_step(
                "day13-step4", 4, "Matrix Transformation Challenge", "Practice",
                "Extract and Square Positive Numbers from Matrix",
                "Write a nested comprehension to process a 2D matrix.",
                "Matrix Positive Squarer",
                [
                    "Given `matrix = [[-2, 3, -1], [4, -5, 6], [0, 7, -8]]`.",
                    "Write a single list comprehension that flattens the matrix, filters only positive numbers (`> 0`), and squares them.",
                    "Assign the result to `positive_squares`.",
                    "Print `'Positive squares:', positive_squares`."
                ],
                """# Day 13 Practice: Matrix Positive Squarer
matrix = [[-2, 3, -1], [4, -5, 6], [0, 7, -8]]

# TODO: Single list comprehension to extract, filter (> 0), and square positive numbers
positive_squares = []

print("Positive squares:", positive_squares)
""",
                """matrix = [[-2, 3, -1], [4, -5, 6], [0, 7, -8]]

positive_squares = [x * x for row in matrix for x in row if x > 0]

print("Positive squares:", positive_squares)
""",
                ["Positive squares: [9, 16, 36, 49]"],
                "Use `[x * x for row in matrix for x in row if x > 0]`.",
                takeaway="Nested comprehensions combine flattening, filtering, and transformation into a single clean pass."
            ),
            make_completion_step(
                "day13-step5", 5, "List Comprehensions Mastery", "Recap",
                13, "Day 13 Complete: List Comprehensions & Expressions",
                "You have mastered declarative list creation, bytecode optimization, and nested loops.",
                [
                    {
                        "concept": "Filter vs Ternary Placement",
                        "naiveIntuition": "Put if/else at the end of the comprehension",
                        "pythonReality": "Trailing `if` filters elements; leading `if/else` is a ternary expression transforming elements"
                    },
                    {
                        "concept": "Loop Ordering",
                        "naiveIntuition": "Inner loops come first in nested comprehensions",
                        "pythonReality": "Loops appear in the same order as written in nested for loops (outer first)"
                    }
                ],
                ["[expr for x in seq if cond]", "CPython LIST_APPEND Optimization", "Nested Comprehension Order", "Ternary Output Transformations"],
                get_next_preview(13)
            )
        ]
    }

    # DAY 14: Tuples & Immutability Guarantees
    days[14] = {
        "dayNumber": 14,
        "title": "Tuples & Immutability Guarantees",
        "topicName": "Tuples & Immutability",
        "sectionId": "python-core",
        "estimatedMinutes": 25,
        "difficulty": "FOUNDATIONAL",
        "prerequisites": [13],
        "concepts": ["Tuple Packing/Unpacking", "Hashability", "namedtuple", "Memory Footprint"],
        "practiceSkills": ["Tuple Unpacking", "Hashable Key Creation", "Memory Efficiency Evaluation"],
        "steps": [
            make_explanation_step(
                "day14-step1", 1, "Tuples vs Lists: Immutability & Memory", "Tuples vs Lists",
                "Why Tuples Exist: Immutability, Hashability, and Overhead",
                "Understand why tuples are lighter, faster, and hashable.",
                [
                    "A `tuple` is an ordered, immutable sequence. Unlike lists, once a tuple is created, its length and pointer slots cannot be changed.",
                    "Because tuples have fixed lengths, CPython allocates exact memory with zero over-allocation headroom, making tuples ~20-30% smaller in bytes than lists of the same length.",
                    "Crucially, because tuples are immutable, a tuple containing only immutable elements is **hashable**! This means tuples can be used as **keys in dictionaries** and **elements in sets**, whereas lists can never be dictionary keys."
                ],
                snippets=[{
                    "title": "Tuples as Dictionary Keys",
                    "code": "# 2D Grid coordinates as dictionary keys\ngrid_cache = {}\ngrid_cache[(0, 1)] = 'Right'\ngrid_cache[(1, 0)] = 'Down'\n\n# grid_cache[[0, 1]] = 'Error' # TypeError: unhashable type: 'list'",
                    "language": "python",
                    "caption": "Tuples serve as hashable composite keys for graphs and grids."
                }],
                callouts=[{
                    "type": "tip",
                    "title": "Single-Element Tuple Syntax",
                    "content": "A single-element tuple requires a trailing comma: `(42,)`. Writing `(42)` is just a parenthesized integer!"
                }],
                takeaway="Tuples are immutable, memory-efficient, and hashable if their elements are hashable."
            ),
            make_explanation_step(
                "day14-step2", 2, "Tuple Packing, Unpacking & namedtuple", "Unpacking & namedtuple",
                "Extended Unpacking with Asterisk and Lightweight Structs",
                "Unpack sequences cleanly and define structured records.",
                [
                    "Tuple unpacking binds sequence elements directly to variables: `a, b = (10, 20)`.",
                    "Extended iterable unpacking uses `*rest` to capture arbitrary middle or tail elements: `first, *middle, last = [1, 2, 3, 4, 5]`.",
                    "`collections.namedtuple` creates tuple subclasses with named fields, combining the lightweight memory of tuples with attribute access (`point.x`, `point.y`)."
                ],
                snippets=[{
                    "title": "Extended Unpacking and namedtuple",
                    "code": "from collections import namedtuple\n\n# Extended unpacking\nhead, *tail = [10, 20, 30, 40]\nprint(head) # 10\nprint(tail) # [20, 30, 40]\n\n# namedtuple\nPoint = namedtuple('Point', ['x', 'y'])\np = Point(3, 4)\nprint(p.x, p.y) # 3 4",
                    "language": "python",
                    "caption": "Clean unpacking and namedtuple records."
                }],
                callouts=[{
                    "type": "warning",
                    "title": "Tuple Containing Mutable Child",
                    "content": "If a tuple contains a mutable object like `t = ([1, 2], 3)`, `t` is NOT hashable! Immutability of the container does not make mutable children hashable."
                }],
                takeaway="Tuples support extended unpacking (*rest) and namedtuple provides readable lightweight structs."
            ),
            make_checkpoint_step(
                "day14-step3", 3, "Tuples & Hashability Checkpoint", "Checkpoint",
                "Test Your Understanding of Tuples and Hashability",
                "Verify tuple creation, hashability rules, and unpacking.",
                [
                    {
                        "id": "chk-d14-q1",
                        "question": "Which of the following tuples CAN be used as a dictionary key?",
                        "options": [
                            {"id": "A", "label": "(1, 'alpha', [2, 3])"},
                            {"id": "B", "label": "(1, 'alpha', (2, 3))"},
                            {"id": "C", "label": "(1, 'alpha', {'key': 4})"},
                            {"id": "D", "label": "None of them, because tuples cannot be dict keys"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: It contains a list child, which is mutable and unhashable.",
                            "B": "Correct! All elements (int, str, and inner tuple of ints) are immutable and hashable.",
                            "C": "Incorrect: It contains a dict, which is mutable and unhashable.",
                            "D": "Incorrect: Tuples with hashable elements are fully valid dict keys."
                        }
                    },
                    {
                        "id": "chk-d14-q2",
                        "question": "What is the type of `x = (5)` vs `y = (5,)`?",
                        "options": [
                            {"id": "A", "label": "Both are tuples"},
                            {"id": "B", "label": "x is int, y is tuple"},
                            {"id": "C", "label": "x is tuple, y is syntax error"},
                            {"id": "D", "label": "Both are ints"}
                        ],
                        "correctOptionId": "B",
                        "explanations": {
                            "A": "Incorrect: Parentheses alone without commas group expressions.",
                            "B": "Correct! (5) is an integer enclosed in arithmetic parentheses; (5,) with a comma is a 1-element tuple.",
                            "C": "Incorrect: y is valid tuple syntax.",
                            "D": "Incorrect: y is a tuple."
                        }
                    }
                ],
                takeaway="A tuple is hashable only if all its elements are hashable; 1-tuples require a trailing comma."
            ),
            make_practice_step(
                "day14-step4", 4, "Grid Coordinate Distance Calculator", "Practice",
                "Coordinate Lookup and Distance Cache",
                "Use tuples as hashable keys in a geometric memoization cache.",
                "Coordinate Distance Cache",
                [
                    "Given coordinate pairs `points = [((0, 0), (3, 4)), ((1, 1), (4, 5))]`.",
                    "For each pair `(p1, p2)`, compute Manhattan distance: `abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])`.",
                    "Store the distance in `dist_cache` using `(p1, p2)` as the dictionary key.",
                    "Print `'Cache entries:', len(dist_cache)` and `'Origin to target distance:', dist_cache[((0, 0), (3, 4))]`."
                ],
                """# Day 14 Practice: Coordinate Distance Cache
points = [((0, 0), (3, 4)), ((1, 1), (4, 5))]

dist_cache = {}

# TODO: Compute Manhattan distance for each pair and cache in dist_cache
for p1, p2 in points:
    # Compute dist = abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    # Store in dist_cache[(p1, p2)] = dist
    pass

print("Cache entries:", len(dist_cache))
print("Origin to target distance:", dist_cache[((0, 0), (3, 4))])
""",
                """points = [((0, 0), (3, 4)), ((1, 1), (4, 5))]

dist_cache = {}
for p1, p2 in points:
    dist = abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    dist_cache[(p1, p2)] = dist

print("Cache entries:", len(dist_cache))
print("Origin to target distance:", dist_cache[((0, 0), (3, 4))])
""",
                ["Cache entries: 2", "Origin to target distance: 7"],
                "Calculate `dist = abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])` and assign to `dist_cache[(p1, p2)]`.",
                takeaway="Nested immutable tuples form hashable composite keys ideal for geometric and graph caches."
            ),
            make_completion_step(
                "day14-step5", 5, "Tuples & Immutability Mastery", "Recap",
                14, "Day 14 Complete: Tuples & Immutability Guarantees",
                "You have mastered tuple memory compactness, hashability prerequisites, and unpacking.",
                [
                    {
                        "concept": "Single-Element Tuples",
                        "naiveIntuition": "t = (10) creates a 1-item tuple",
                        "pythonReality": "Parentheses group expressions; you must include a comma: (10,)"
                    },
                    {
                        "concept": "Tuple Hashability",
                        "naiveIntuition": "All tuples can be used as dictionary keys",
                        "pythonReality": "A tuple is hashable only if every element inside it is also hashable"
                    }
                ],
                ["Tuple Memory Compactness", "Hashable Dictionary Keys", "Extended Unpacking (*rest)", "namedtuple Lightweight Structs"],
                get_next_preview(14)
            )
        ]
    }

    # We will complete Days 15 to 25 with full fidelity
    return days
