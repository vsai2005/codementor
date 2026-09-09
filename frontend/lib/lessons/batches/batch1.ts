import { DailyLessonPackage } from "../types";
import { DAY_1_STEPS } from "../day1Data";
import { DAY_2_STEPS } from "../day2Data";

export const BATCH_1_LESSONS: Record<number, DailyLessonPackage> = {
  1: {
  "dayNumber": 1,
  "title": "Variables, Expressions & Memory Model",
  "topicName": "Python Syntax",
  "sectionId": "python-foundations",
  "estimatedMinutes": 30,
  "difficulty": "BEGINNER",
  "prerequisites": [],
  "concepts": [
    "Dynamic Typing",
    "Object References",
    "Memory Model",
    "id() & type()"
  ],
  "practiceSkills": [
    "Variable Declaration",
    "Expression Evaluation",
    "Memory Model Tracing"
  ]
,
  "steps": DAY_1_STEPS
},
  2: {
  "dayNumber": 2,
  "title": "Numerical Types, Arithmetic & Bitwise",
  "topicName": "Numeric System",
  "sectionId": "python-foundations",
  "estimatedMinutes": 25,
  "difficulty": "BEGINNER",
  "prerequisites": [
    1
  ],
  "concepts": [
    "Integers & Floats",
    "Floor Division & Modulo",
    "Bitwise Operators"
  ],
  "practiceSkills": [
    "Arithmetic Computations",
    "Modulo Calculations",
    "Type Casting"
  ]
,
  "steps": DAY_2_STEPS
},
  3: {
  "dayNumber": 3,
  "title": "Strings & String Formatting",
  "topicName": "String Processing",
  "sectionId": "python-foundations",
  "estimatedMinutes": 30,
  "difficulty": "BEGINNER",
  "prerequisites": [
    2
  ],
  "concepts": [
    "String Immutability",
    "Slice Notation",
    "f-strings",
    "Encoding (ASCII/UTF-8)"
  ],
  "practiceSkills": [
    "String Slicing",
    "f-string Formatting",
    "String Immutability Reasoning"
  ]
,
  "steps": [
    {
        "id": "day3-step1",
        "stepNumber": 1,
        "title": "String Immutability & Indexing",
        "shortLabel": "Immutability",
        "type": "explanation",
        "isGated": false,
        "heading": "Strings as Immutable Unicode Sequences",
        "subheading": "Understanding memory allocation, 0-based indexing, and why strings cannot be modified in place.",
        "markdownContent": [
            "In Python, a string (`str`) is an ordered, immutable sequence of Unicode code points. Once created in heap memory, its characters cannot be altered in place.",
            "Python uses 0-based indexing for positive offsets (`0` to `len - 1`) and negative indexing from the end (`-1` to `-len`). Attempting to mutate an index like `text[0] = 'h'` raises a `TypeError: 'str' object does not support item assignment`.",
            "To modify a string, Python requires allocating a new string object containing the desired transformation."
        ],
        "snippets": [
            {
                "title": "String Indexing and Immutability",
                "code": "msg = \"Python\"\nprint(msg[0])   # 'P'\nprint(msg[-1])  # 'n'\n# msg[0] = 'p'  # Raises TypeError!",
                "language": "python",
                "caption": "Accessing characters via positive and negative indexing."
            }
        ],
        "callouts": [
            {
                "type": "warning",
                "title": "Strings Cannot Mutate In-Place",
                "content": "Any string method like `.upper()` or `.replace()` does not alter the original string. It returns a brand new string object."
            }
        ],
        "keyTakeaway": "Strings in Python are immutable sequences; all transformations create new string objects."
    },
    {
        "id": "day3-step2",
        "stepNumber": 2,
        "title": "Slice Notation & f-strings",
        "shortLabel": "Slicing & Formatting",
        "type": "explanation",
        "isGated": false,
        "heading": "Mastering [start:stop:step] and Formatted String Literals",
        "subheading": "Extract substrings cleanly and format values with Python 3.6+ f-strings.",
        "markdownContent": [
            "The slicing syntax `sequence[start:stop:step]` extracts elements from `start` up to but not including `stop`. Slicing never raises `IndexError` even with out-of-range bounds.",
            "Omitting `start` defaults to `0`, omitting `stop` defaults to sequence length, and a negative step reverses traversal (e.g. `s[::-1]`).",
            "Formatted string literals (f-strings) prefix strings with `f\"...\"` and evaluate bracketed expressions `{expr}` at runtime with high performance."
        ],
        "snippets": [
            {
                "title": "Slicing and f-string Patterns",
                "code": "text = \"CodeMentor\"\nprefix = text[:4]       # 'Code'\nreversed_text = text[::-1] # 'rotnMeMdoC'\n\nname, score = \"Alice\", 98.5\nprint(f\"{name} scored {score:.1f}%\")",
                "language": "python",
                "caption": "Slice bounds and f-string formatting specifiers."
            }
        ],
        "callouts": [
            {
                "type": "tip",
                "title": "O(K) Slicing Cost",
                "content": "Slicing a string of length K allocates a new string of length K, costing O(K) time and space."
            }
        ],
        "keyTakeaway": "Slice notation [start:stop:step] returns a new string, and f-strings evaluate expressions at runtime."
    },
    {
        "id": "day3-step3",
        "stepNumber": 3,
        "title": "String Slicing & Mutability Checkpoint",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Verify Your Understanding of Strings",
        "subheading": "Test your mental model of indexing, immutability, and slice bounds.",
        "checkpoints": [
            {
                "id": "chk-d3-q1",
                "question": "What is the output of the following snippet?\n\n```python\ns = 'Algorithm'\nres = s[2:7:2]\nprint(res)\n```",
                "options": [
                    {
                        "id": "A",
                        "label": "'grt'"
                    },
                    {
                        "id": "B",
                        "label": "'loi'"
                    },
                    {
                        "id": "C",
                        "label": "'gor'"
                    },
                    {
                        "id": "D",
                        "label": "'lg'"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! In 'Algorithm' (indices 0:A, 1:l, 2:g, 3:o, 4:r, 5:i, 6:t), slice 2:7:2 samples indices 2, 4, and 6, producing 'grt'.",
                    "B": "Incorrect: 1-based indexing was accidentally used.",
                    "C": "Incorrect: Step size was skipped or miscalculated.",
                    "D": "Incorrect: The slice includes index 6 ('t') because 6 < 7."
                }
            },
            {
                "id": "chk-d3-q2",
                "question": "What happens when executing `word = 'cat'; word[0] = 'b'`?",
                "options": [
                    {
                        "id": "A",
                        "label": "word becomes 'bat'"
                    },
                    {
                        "id": "B",
                        "label": "TypeError is raised because strings are immutable"
                    },
                    {
                        "id": "C",
                        "label": "SyntaxError is raised during parsing"
                    },
                    {
                        "id": "D",
                        "label": "word becomes ('b', 'a', 't')"
                    }
                ],
                "correctOptionId": "B",
                "explanations": {
                    "A": "Incorrect: Python strings cannot be modified in-place; they do not support item assignment.",
                    "B": "Correct! Python raises TypeError: 'str' object does not support item assignment.",
                    "C": "Incorrect: The syntax is valid Python; the error is a runtime TypeError.",
                    "D": "Incorrect: String indexing assignment does not convert strings to tuples."
                }
            }
        ],
        "keyTakeaway": "Strings cannot be modified in place, and slices take indices [start, start+step, ... < stop]."
    },
    {
        "id": "day3-step4",
        "stepNumber": 4,
        "title": "Format and Transform Strings",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Build a Formatted User Tag Generator",
        "subheading": "Write a Python script that formats usernames and extracts domain handles.",
        "task": {
            "title": "User Tag & Clean Username Generator",
            "instructions": [
                "Given `raw_user = '  alice_dev  '` and `domain = 'codementor.io'`, strip whitespace from `raw_user`.",
                "Extract the first 5 characters of the stripped username.",
                "Construct `user_handle` formatted as `@<clean_user>#<first5>` using f-strings.",
                "Print the resulting `user_handle`."
            ],
            "starterCode": "# Day 3 Practice: User Tag Generator\nraw_user = \"  alice_dev  \"\ndomain = \"codementor.io\"\n\n# TODO 1: Strip leading and trailing whitespace from raw_user\nclean_user = \"\"\n\n# TODO 2: Slice the first 5 characters from clean_user\nuser_prefix = \"\"\n\n# TODO 3: Construct the user handle using an f-string: \"@{clean_user}#{user_prefix}\"\nuser_handle = \"\"\n\nprint(\"User handle:\", user_handle)\n",
            "solutionCode": "raw_user = \"  alice_dev  \"\ndomain = \"codementor.io\"\n\nclean_user = raw_user.strip()\nuser_prefix = clean_user[:5]\nuser_handle = f\"@{clean_user}#{user_prefix}\"\n\nprint(\"User handle:\", user_handle)\n",
            "expectedOutputPatterns": [
                "User handle: @alice_dev#alice"
            ],
            "hint": "Use raw_user.strip() to remove padding spaces, clean_user[:5] for the first 5 letters, and f'@{clean_user}#{user_prefix}'."
        },
        "keyTakeaway": "String methods like .strip() return clean copies, and f-strings provide elegant interpolation."
    },
    {
        "id": "day3-step5",
        "stepNumber": 5,
        "title": "Strings Mastery & Recap",
        "shortLabel": "Recap",
        "type": "completion",
        "isGated": false,
        "dayNumber": 3,
        "heading": "Day 3 Complete: Strings & String Formatting",
        "subheading": "You understand string immutability, slice indexing, and modern formatting.",
        "recapRows": [
            {
                "concept": "String Modification",
                "naiveIntuition": "Change characters directly like text[0] = 'A'",
                "pythonReality": "Strings are immutable; create a new string via slicing or methods"
            },
            {
                "concept": "Slice Out-of-Bounds",
                "naiveIntuition": "text[0:100] on a 5-char string crashes with IndexError",
                "pythonReality": "Slicing gracefully clamps to the valid boundaries without raising an error"
            }
        ],
        "solidifiedConcepts": [
            "String Immutability",
            "Slice Notation [start:stop:step]",
            "f-string Interpolation",
            "String Stripping"
        ],
        "nextDayPreview": {
            "dayNumber": 4,
            "title": "Booleans & Logical Control Flow",
            "description": "Understand truthiness, boolean coercion, short-circuit logical evaluation, and conditional branch structures."
        }
    }
]
},
  4: {
  "dayNumber": 4,
  "title": "Booleans & Logical Control Flow",
  "topicName": "Boolean Logic",
  "sectionId": "python-foundations",
  "estimatedMinutes": 25,
  "difficulty": "BEGINNER",
  "prerequisites": [
    3
  ],
  "concepts": [
    "Truthiness",
    "Short-circuit Evaluation",
    "if/elif/else",
    "Ternary Expressions"
  ],
  "practiceSkills": [
    "Conditional Branching",
    "Short-Circuit Logic",
    "Ternary Evaluation"
  ]
,
  "steps": [
    {
        "id": "day4-step1",
        "stepNumber": 1,
        "title": "Boolean Logic & Truthiness",
        "shortLabel": "Truthiness",
        "type": "explanation",
        "isGated": false,
        "heading": "Boolean Logic, Truth Values, and Truthiness",
        "subheading": "Learn how Python evaluates every object as truthy or falsy in boolean contexts.",
        "markdownContent": [
            "Python has a built-in `bool` type with two singleton values: `True` and `False`. In conditional contexts, every Python object has an implicit truth value.",
            "The following objects evaluate to `False` in boolean contexts: `None`, `False`, numeric zeros (`0`, `0.0`, `0j`), empty collections (`''`, `()`, `[]`, `{}`, `set()`), and objects whose `__bool__()` or `__len__()` returns `0` or `False`.",
            "All other objects evaluate to `True`. This allows concise idiomatic guards like `if items:` instead of `if len(items) > 0:`."
        ],
        "snippets": [
            {
                "title": "Truthiness in Action",
                "code": "empty_list = []\nif not empty_list:\n    print(\"List is empty!\")\n\nval = 42\nprint(bool(val))  # True\nprint(bool(0))    # False",
                "language": "python",
                "caption": "Implicit truth testing of objects in conditional statements."
            }
        ],
        "callouts": [
            {
                "type": "tip",
                "title": "Prefer Pythonic Truth Checks",
                "content": "Write `if text:` rather than `if text != \"\":`. Python tests truthiness directly."
            }
        ],
        "keyTakeaway": "Every Python object has a boolean value; empty sequences and zeros evaluate to False."
    },
    {
        "id": "day4-step2",
        "stepNumber": 2,
        "title": "Short-Circuiting & Ternary",
        "shortLabel": "Short-Circuit",
        "type": "explanation",
        "isGated": false,
        "heading": "Short-Circuit Evaluation and Conditional Expressions",
        "subheading": "How 'and' and 'or' return operands, and how to write clean ternary expressions.",
        "markdownContent": [
            "Logical operators `and` and `or` use short-circuit evaluation. Python evaluates expressions from left to right and stops as soon as the outcome is certain.",
            "`a and b` evaluates `a`; if `a` is falsy, it returns `a` immediately without evaluating `b`. If `a` is truthy, it returns `b`.",
            "`a or b` evaluates `a`; if `a` is truthy, it returns `a` immediately. If `a` is falsy, it returns `b`.",
            "Ternary conditional expressions use the form: `val_if_true if condition else val_if_false`."
        ],
        "snippets": [
            {
                "title": "Short-Circuiting and Ternary Syntax",
                "code": "# Short-circuiting avoids division by zero\ncount, total = 0, 100\navg = (count > 0) and (total / count) # Returns False safely!\n\n# Ternary expression\nage = 20\nstatus = \"Adult\" if age >= 18 else \"Minor\"",
                "language": "python",
                "caption": "Using short-circuiting as safety guards."
            }
        ],
        "callouts": [
            {
                "type": "deep-dive",
                "title": "Logical Operators Return Operands",
                "content": "In Python, `x or y` does NOT return True/False; it returns the actual object `x` or `y`!"
            }
        ],
        "keyTakeaway": "'and' and 'or' return the decisive operand, stopping evaluation as soon as the result is known."
    },
    {
        "id": "day4-step3",
        "stepNumber": 3,
        "title": "Logic & Short-Circuit Checkpoint",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Test Your Mastery of Truthiness and Short-Circuiting",
        "subheading": "Evaluate operands and determine exact return values.",
        "checkpoints": [
            {
                "id": "chk-d4-q1",
                "question": "What is the exact value of the expression `\"default\" or 42`?",
                "options": [
                    {
                        "id": "A",
                        "label": "True"
                    },
                    {
                        "id": "B",
                        "label": "\"default\""
                    },
                    {
                        "id": "C",
                        "label": "42"
                    },
                    {
                        "id": "D",
                        "label": "False"
                    }
                ],
                "correctOptionId": "B",
                "explanations": {
                    "A": "Incorrect: 'or' does not convert the result to a boolean; it returns the decisive operand.",
                    "B": "Correct! Non-empty string 'default' is truthy, so 'or' short-circuits immediately and returns 'default'.",
                    "C": "Incorrect: The right operand is never evaluated because the left operand was already truthy.",
                    "D": "Incorrect: 'default' is truthy."
                }
            },
            {
                "id": "chk-d4-q2",
                "question": "Which value is considered FALSY in Python?",
                "options": [
                    {
                        "id": "A",
                        "label": "\"False\""
                    },
                    {
                        "id": "B",
                        "label": "[0]"
                    },
                    {
                        "id": "C",
                        "label": "0.0"
                    },
                    {
                        "id": "D",
                        "label": "{-1}"
                    }
                ],
                "correctOptionId": "C",
                "explanations": {
                    "A": "Incorrect: A non-empty string is always truthy, even if it contains the word 'False'.",
                    "B": "Incorrect: A non-empty list containing element 0 has length 1 and is truthy.",
                    "C": "Correct! Numeric floating-point zero (0.0) is falsy.",
                    "D": "Incorrect: A set containing elements has length > 0 and is truthy."
                }
            }
        ],
        "keyTakeaway": "Short-circuit logic returns the operand that determined the truth outcome."
    },
    {
        "id": "day4-step4",
        "stepNumber": 4,
        "title": "Short-Circuit Guard & Ternary Practice",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Implement a Safe Division Rate Limiter",
        "subheading": "Build safe mathematical metrics using short-circuiting and ternary expressions.",
        "task": {
            "title": "Safe Metric Evaluator",
            "instructions": [
                "Given `total_requests = 150` and `elapsed_seconds = 0`, compute `requests_per_second`.",
                "Use short-circuiting to ensure division by zero never occurs: if `elapsed_seconds > 0`, compute `total_requests / elapsed_seconds`; otherwise `0.0`.",
                "Assign `load_status` to `'HIGH'` if `requests_per_second > 50` else `'NORMAL'` using a ternary expression.",
                "Print both `requests_per_second` and `load_status`."
            ],
            "starterCode": "# Day 4 Practice: Safe Metric Evaluator\ntotal_requests = 150\nelapsed_seconds = 0\n\n# TODO 1: Safely compute rps using ternary or short-circuit logic (default to 0.0 if elapsed_seconds == 0)\nrequests_per_second = 0.0\n\n# TODO 2: Assign load_status ('HIGH' if requests_per_second > 50 else 'NORMAL')\nload_status = \"\"\n\nprint(\"RPS:\", requests_per_second)\nprint(\"Status:\", load_status)\n",
            "solutionCode": "total_requests = 150\nelapsed_seconds = 0\n\nrequests_per_second = (total_requests / elapsed_seconds) if elapsed_seconds > 0 else 0.0\nload_status = \"HIGH\" if requests_per_second > 50 else \"NORMAL\"\n\nprint(\"RPS:\", requests_per_second)\nprint(\"Status:\", load_status)\n",
            "expectedOutputPatterns": [
                "RPS: 0.0",
                "Status: NORMAL"
            ],
            "hint": "Use a ternary check `(total / elapsed) if elapsed > 0 else 0.0` to guard against ZeroDivisionError."
        },
        "keyTakeaway": "Guarding expressions with conditions prevents runtime crashes and maintains clean data flow."
    },
    {
        "id": "day4-step5",
        "stepNumber": 5,
        "title": "Logic & Control Flow Mastery",
        "shortLabel": "Recap",
        "type": "completion",
        "isGated": false,
        "dayNumber": 4,
        "heading": "Day 4 Complete: Booleans & Logical Control Flow",
        "subheading": "You have mastered Python truthiness, short-circuit evaluation, and ternary branching.",
        "recapRows": [
            {
                "concept": "Return Value of and/or",
                "naiveIntuition": "and / or always return True or False",
                "pythonReality": "They return the actual operand object that finalized the decision"
            },
            {
                "concept": "Empty Containers",
                "naiveIntuition": "Compare len(lst) == 0",
                "pythonReality": "Empty collections are natively falsy; write `if not lst:`"
            }
        ],
        "solidifiedConcepts": [
            "Truthiness & Falsy Values",
            "Short-Circuit Evaluation",
            "Ternary Expressions",
            "Safe Guard Conditions"
        ],
        "nextDayPreview": {
            "dayNumber": 5,
            "title": "Loops & Iteration Semantics",
            "description": "Implement while and for-in loops, loop control statements (break, continue), and the for-else construct."
        }
    }
]
},
  5: {
  "dayNumber": 5,
  "title": "Loops & Iteration Semantics",
  "topicName": "Loops & Iteration",
  "sectionId": "python-foundations",
  "estimatedMinutes": 30,
  "difficulty": "BEGINNER",
  "prerequisites": [
    4
  ],
  "concepts": [
    "for / while Loops",
    "break & continue",
    "for-else Construct",
    "range() Mechanics"
  ],
  "practiceSkills": [
    "Loop Execution Control",
    "Early Termination with break",
    "Loop-else Logic"
  ]
,
  "steps": [
    {
        "id": "day5-step1",
        "stepNumber": 1,
        "title": "Loop Mechanisms & range()",
        "shortLabel": "Loops & range",
        "type": "explanation",
        "isGated": false,
        "heading": "Iteration with for, while, and the Lazy range() Sequence",
        "subheading": "Understand how Python iterates over collections and generates integer ranges on demand.",
        "markdownContent": [
            "Python's `for` loop is fundamentally a foreach iterator: it pulls elements sequentially from any iterable using the iteration protocol.",
            "`range(start, stop, step)` represents an immutable sequence of numbers. Crucially, `range` does not allocate all numbers in memory at once; it generates them lazily with $O(1)$ memory overhead.",
            "`while` loops continue executing as long as their condition remains truthy, making them ideal when the total iteration count is unknown beforehand."
        ],
        "snippets": [
            {
                "title": "for and while loops with range",
                "code": "for i in range(1, 6): # 1, 2, 3, 4, 5\n    if i % 2 == 0:\n        continue # skip even numbers\n    print(i)",
                "language": "python",
                "caption": "Skipping loop iterations with continue."
            }
        ],
        "callouts": [
            {
                "type": "tip",
                "title": "range() is O(1) Memory",
                "content": "`range(10**9)` consumes the same tiny amount of memory as `range(10)` because it only stores start, stop, and step."
            }
        ],
        "keyTakeaway": "range() produces integers lazily with O(1) memory, and for loops iterate over any sequence."
    },
    {
        "id": "day5-step2",
        "stepNumber": 2,
        "title": "Loop Control & The else Clause",
        "shortLabel": "break & else",
        "type": "explanation",
        "isGated": false,
        "heading": "Mastering break, continue, and the Unique for-else Construct",
        "subheading": "Use loop-else for search patterns without boolean flag variables.",
        "markdownContent": [
            "`break` terminates the innermost enclosing loop immediately.",
            "`continue` skips the rest of the current iteration and jumps to the next cycle.",
            "Python loops have an optional `else:` clause. The `else` block executes IF AND ONLY IF the loop finished normally without encountering a `break` statement.",
            "This pattern elegantly solves search problems: if target is found, break; if loop completes without finding, execute the else fallback."
        ],
        "snippets": [
            {
                "title": "The Search Pattern with for-else",
                "code": "nums = [2, 4, 6, 8]\ntarget = 5\n\nfor n in nums:\n    if n == target:\n        print(\"Found!\")\n        break\nelse:\n    print(\"Target not found in list\")",
                "language": "python",
                "caption": "The else block executes only if no break occurred."
            }
        ],
        "callouts": [
            {
                "type": "deep-dive",
                "title": "Think 'no-break' rather than 'else'",
                "content": "A helpful mental trick is to read `for ... else:` as `for ... if no break:`."
            }
        ],
        "keyTakeaway": "The else clause of a loop runs only if the loop ran to completion without hitting a break."
    },
    {
        "id": "day5-step3",
        "stepNumber": 3,
        "title": "Loop Control Checkpoint",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Test Your Mastery of Loop Control Flow",
        "subheading": "Predict the output of break, continue, and loop-else constructs.",
        "checkpoints": [
            {
                "id": "chk-d5-q1",
                "question": "What will this code print?\n\n```python\nfor x in [1, 2, 3]:\n    if x == 2:\n        break\nelse:\n    print('Done')\n```",
                "options": [
                    {
                        "id": "A",
                        "label": "'Done'"
                    },
                    {
                        "id": "B",
                        "label": "Nothing is printed"
                    },
                    {
                        "id": "C",
                        "label": "SyntaxError on else after for"
                    },
                    {
                        "id": "D",
                        "label": "2"
                    }
                ],
                "correctOptionId": "B",
                "explanations": {
                    "A": "Incorrect: The loop executed a break statement when x == 2, so the else block is bypassed.",
                    "B": "Correct! Because x == 2 triggers break, the loop terminates immediately and the else block never executes.",
                    "C": "Incorrect: for-else is valid Python syntax.",
                    "D": "Incorrect: There is no print statement inside the loop."
                }
            },
            {
                "id": "chk-d5-q2",
                "question": "How much memory does `range(1_000_000_000)` consume in Python 3?",
                "options": [
                    {
                        "id": "A",
                        "label": "Around 8 Gigabytes of RAM"
                    },
                    {
                        "id": "B",
                        "label": "A fixed small O(1) memory footprint (~48 bytes)"
                    },
                    {
                        "id": "C",
                        "label": "It depends on whether it is assigned to a variable"
                    },
                    {
                        "id": "D",
                        "label": "MemoryError is raised immediately"
                    }
                ],
                "correctOptionId": "B",
                "explanations": {
                    "A": "Incorrect: In Python 2, `range` created a full list, but Python 3 `range` is a lazy sequence.",
                    "B": "Correct! Python 3's range object stores only start, stop, and step in fixed O(1) space.",
                    "C": "Incorrect: range is always a lightweight object regardless of assignment.",
                    "D": "Incorrect: No memory error occurs because elements are computed on the fly."
                }
            }
        ],
        "keyTakeaway": "break skips the loop-else block, and range() generates integers lazily in O(1) space."
    },
    {
        "id": "day5-step4",
        "stepNumber": 4,
        "title": "Search with Loop-Else",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Find First Prime Divisor Using Loop-Else",
        "subheading": "Implement a prime factor search utilizing loop control and loop-else.",
        "task": {
            "title": "Prime Searcher",
            "instructions": [
                "Given integer `candidate = 29`, test if any number from 2 up to 28 divides `candidate` evenly.",
                "If a divisor `d` is found, print `f'Divisible by {d}'` and `break`.",
                "In the loop's `else` clause, print `'Number is prime'`.",
                "Run the code to verify that 29 is correctly identified as prime."
            ],
            "starterCode": "# Day 5 Practice: Prime Searcher\ncandidate = 29\n\n# TODO: Loop through numbers from 2 up to candidate (exclusive)\n# If candidate % d == 0, print f\"Divisible by {d}\" and break\n# In the loop's else block, print \"Number is prime\"\n\nfor d in range(2, candidate):\n    if candidate % d == 0:\n        print(f\"Divisible by {d}\")\n        break\nelse:\n    # TODO: Print prime confirmation\n    pass\n",
            "solutionCode": "candidate = 29\n\nfor d in range(2, candidate):\n    if candidate % d == 0:\n        print(f\"Divisible by {d}\")\n        break\nelse:\n    print(\"Number is prime\")\n",
            "expectedOutputPatterns": [
                "Number is prime"
            ],
            "hint": "Place `print('Number is prime')` in the `else:` block aligned with `for`."
        },
        "keyTakeaway": "Using for-else avoids clumsy boolean flags when searching for matches."
    },
    {
        "id": "day5-step5",
        "stepNumber": 5,
        "title": "Loops Mastery & Recap",
        "shortLabel": "Recap",
        "type": "completion",
        "isGated": false,
        "dayNumber": 5,
        "heading": "Day 5 Complete: Loops & Iteration Semantics",
        "subheading": "You have mastered lazy range sequences, loop control, and the for-else search pattern.",
        "recapRows": [
            {
                "concept": "Loop Else Clause",
                "naiveIntuition": "Runs on every loop completion or behaves like if-else",
                "pythonReality": "Runs ONLY if the loop exits naturally without encountering a break"
            },
            {
                "concept": "range Memory",
                "naiveIntuition": "range(1000000) stores a million integers in memory",
                "pythonReality": "range is a lazy generator-like sequence consuming O(1) memory"
            }
        ],
        "solidifiedConcepts": [
            "for & while Loops",
            "break vs continue",
            "for-else Construct",
            "Lazy range() Invariant"
        ],
        "nextDayPreview": {
            "dayNumber": 6,
            "title": "Functions, Stack Frames & LEGB Scope",
            "description": "Define reusable procedures, return contracts, local vs global scope, and the LEGB namespace lookup rule."
        }
    }
]
},
  6: {
  "dayNumber": 6,
  "title": "Functions & Variable Scope",
  "topicName": "Functions & Scope",
  "sectionId": "python-foundations",
  "estimatedMinutes": 30,
  "difficulty": "BEGINNER",
  "prerequisites": [
    5
  ],
  "concepts": [
    "def & return",
    "LEGB Rule",
    "global & nonlocal",
    "Call Stack Basics"
  ],
  "practiceSkills": [
    "Function Definition",
    "Scope Resolution (LEGB)",
    "Encapsulation"
  ]
,
  "steps": [
    {
        "id": "day6-step1",
        "stepNumber": 1,
        "title": "Functions & The Call Stack",
        "shortLabel": "Functions & Call Stack",
        "type": "explanation",
        "isGated": false,
        "heading": "Functions, Frame Objects, and the Call Stack",
        "subheading": "Understand what happens in memory when a function is invoked and returned.",
        "markdownContent": [
            "Functions in Python are defined with the `def` keyword. A function definition creates a function object and binds it to a name in the current scope.",
            "When a function is called, Python pushes a new stack frame onto the call stack. This frame holds the function's local variables, arguments, and return pointer.",
            "If a function reaches the end of its body without an explicit `return` statement, it implicitly returns `None`."
        ],
        "snippets": [
            {
                "title": "Function Call and Frame Lifecycle",
                "code": "def square(n):\n    res = n * n\n    return res\n\nval = square(5) # Pushes frame, computes 25, pops frame\nprint(val)      # 25",
                "language": "python",
                "caption": "Frame creation and value return."
            }
        ],
        "callouts": [
            {
                "type": "tip",
                "title": "Implicit None Return",
                "content": "A function with no return statement returns None by default. `print(my_func())` will display `None`."
            }
        ],
        "keyTakeaway": "Every function call pushes a frame onto the call stack; omitting return returns None."
    },
    {
        "id": "day6-step2",
        "stepNumber": 2,
        "title": "The LEGB Scope Resolution Rule",
        "shortLabel": "LEGB Scope",
        "type": "explanation",
        "isGated": false,
        "heading": "Variable Scoping: Local, Enclosing, Global, Built-in",
        "subheading": "How Python searches namespaces to resolve variable names.",
        "markdownContent": [
            "When Python resolves a variable name, it follows the LEGB hierarchy strictly in order:",
            "1. **Local (L)**: Names assigned inside the current function frame.",
            "2. **Enclosing (E)**: Names in outer enclosing functions (closures).",
            "3. **Global (G)**: Names assigned at top-level module scope.",
            "4. **Built-in (B)**: Python's built-in names (`len`, `range`, `print`, `int`).",
            "Assigning to a variable inside a function makes it local by default, unless declared `global` or `nonlocal`."
        ],
        "snippets": [
            {
                "title": "LEGB Scope in Action",
                "code": "x = 'Global'\n\ndef outer():\n    x = 'Enclosing'\n    def inner():\n        x = 'Local'\n        print(x) # Prints 'Local'\n    inner()\nouter()",
                "language": "python",
                "caption": "Python stops searching at the first matching scope in LEGB."
            }
        ],
        "callouts": [
            {
                "type": "warning",
                "title": "UnboundLocalError Trap",
                "content": "Assigning to a variable anywhere in a function marks it as local throughout the ENTIRE function. Reading it before assignment raises `UnboundLocalError`."
            }
        ],
        "keyTakeaway": "Python resolves names from Local -> Enclosing -> Global -> Built-in (LEGB)."
    },
    {
        "id": "day6-step3",
        "stepNumber": 3,
        "title": "Scope & Functions Checkpoint",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Verify Your Mental Model of Python Scope",
        "subheading": "Trace name resolution and spot scope pitfalls.",
        "checkpoints": [
            {
                "id": "chk-d6-q1",
                "question": "What happens when executing this code?\n\n```python\ncounter = 10\ndef inc():\n    counter += 1\ninc()\n```",
                "options": [
                    {
                        "id": "A",
                        "label": "counter becomes 11"
                    },
                    {
                        "id": "B",
                        "label": "UnboundLocalError is raised"
                    },
                    {
                        "id": "C",
                        "label": "counter remains 10"
                    },
                    {
                        "id": "D",
                        "label": "NameError: counter is not defined"
                    }
                ],
                "correctOptionId": "B",
                "explanations": {
                    "A": "Incorrect: counter is not modified because an error occurs first.",
                    "B": "Correct! Because `counter += 1` involves assignment, Python flags `counter` as a local variable. But it attempts to read it before assignment, raising `UnboundLocalError`.",
                    "C": "Incorrect: The function does not complete execution.",
                    "D": "Incorrect: The specific exception is UnboundLocalError, a subclass of NameError."
                }
            },
            {
                "id": "chk-d6-q2",
                "question": "What does a Python function return if there is no explicit `return` statement?",
                "options": [
                    {
                        "id": "A",
                        "label": "0"
                    },
                    {
                        "id": "B",
                        "label": "False"
                    },
                    {
                        "id": "C",
                        "label": "None"
                    },
                    {
                        "id": "D",
                        "label": "Undefined"
                    }
                ],
                "correctOptionId": "C",
                "explanations": {
                    "A": "Incorrect: 0 is a number, not the default return.",
                    "B": "Incorrect: False is a boolean.",
                    "C": "Correct! Python functions implicitly return the singleton object `None` when execution completes without return.",
                    "D": "Incorrect: JavaScript has 'undefined', but Python uses `None`."
                }
            }
        ],
        "keyTakeaway": "Rebinding variables inside a function makes them local; functions return None by default."
    },
    {
        "id": "day6-step4",
        "stepNumber": 4,
        "title": "Write Pure Functions with Scope",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Implement a Pure Metric Formatter",
        "subheading": "Build a function that transforms scores without polluting outer variables.",
        "task": {
            "title": "Pure Score Normalizer",
            "instructions": [
                "Write a function `normalize_score(raw, max_val)` that computes `(raw / max_val) * 100`.",
                "If `raw < 0` or `max_val <= 0`, return `0.0`.",
                "Format the result to 1 decimal place as a float: `round(score, 1)`.",
                "Call `normalize_score(45, 60)` and print `'Normalized:', result`."
            ],
            "starterCode": "# Day 6 Practice: Pure Score Normalizer\n\ndef normalize_score(raw, max_val):\n    # TODO 1: Guard against invalid inputs (raw < 0 or max_val <= 0)\n    if raw < 0 or max_val <= 0:\n        return 0.0\n    \n    # TODO 2: Compute percentage and round to 1 decimal place\n    score = 0.0\n    return score\n\nresult = normalize_score(45, 60)\nprint(\"Normalized:\", result)\n",
            "solutionCode": "def normalize_score(raw, max_val):\n    if raw < 0 or max_val <= 0:\n        return 0.0\n    return round((raw / max_val) * 100, 1)\n\nresult = normalize_score(45, 60)\nprint(\"Normalized:\", result)\n",
            "expectedOutputPatterns": [
                "Normalized: 75.0"
            ],
            "hint": "Compute (raw / max_val) * 100 and pass it to round(..., 1)."
        },
        "keyTakeaway": "Pure functions encapsulate calculation without mutating outer scope state."
    },
    {
        "id": "day6-step5",
        "stepNumber": 5,
        "title": "Functions & Scope Mastery",
        "shortLabel": "Recap",
        "type": "completion",
        "isGated": false,
        "dayNumber": 6,
        "heading": "Day 6 Complete: Functions & Variable Scope",
        "subheading": "You have mastered call stack frame lifecycles, LEGB name resolution, and pure function design.",
        "recapRows": [
            {
                "concept": "Assignment in Functions",
                "naiveIntuition": "Assigning to x reads or writes the global x automatically",
                "pythonReality": "Any assignment inside a function marks that name as local for the entire function scope"
            },
            {
                "concept": "Missing Return",
                "naiveIntuition": "Functions without return produce an error or return void",
                "pythonReality": "They return the singleton object None"
            }
        ],
        "solidifiedConcepts": [
            "def & return Semantics",
            "Call Stack Frames",
            "LEGB Rule",
            "UnboundLocalError Pitfall"
        ],
        "nextDayPreview": {
            "dayNumber": 7,
            "title": "Function Signatures & Default Argument Trap",
            "description": "Inspect positional and keyword arguments, variadic *args/**kwargs, and the classic mutable default argument trap."
        }
    }
]
},
  7: {
  "dayNumber": 7,
  "title": "Function Arguments & Signatures",
  "topicName": "Function Signatures",
  "sectionId": "python-foundations",
  "estimatedMinutes": 30,
  "difficulty": "BEGINNER",
  "prerequisites": [
    6
  ],
  "concepts": [
    "*args and **kwargs",
    "Keyword-Only Args",
    "Mutable Default Trap",
    "Type Annotations"
  ],
  "practiceSkills": [
    "Variadic Arguments",
    "Default Parameter Safety",
    "Keyword-Only Parameters"
  ]
,
  "steps": [
    {
        "id": "day7-step1",
        "stepNumber": 1,
        "title": "The Mutable Default Argument Trap",
        "shortLabel": "Default Arg Trap",
        "type": "explanation",
        "isGated": false,
        "heading": "Why You Must Never Use Mutable Objects as Default Arguments",
        "subheading": "Understand when default arguments are evaluated in Python.",
        "markdownContent": [
            "A critical pitfall in Python is that **default argument values are evaluated once when the function definition is executed, NOT each time the function is called**.",
            "If you use a mutable object (like a `list` or `dict`) as a default argument, all function invocations that omit that argument share the **exact same object** in heap memory!",
            "The idiomatic Pythonic solution is to set the default argument to `None` and initialize a new container inside the function body if the argument is `None`."
        ],
        "snippets": [
            {
                "title": "The Mutable Default Trap and Fix",
                "code": "# DANGEROUS:\ndef bad_append(item, target=[]):\n    target.append(item)\n    return target\n\n# IDIOMATIC & SAFE:\ndef safe_append(item, target=None):\n    if target is None:\n        target = []\n    target.append(item)\n    return target",
                "language": "python",
                "caption": "Always use None as the default sentinel for mutable arguments."
            }
        ],
        "callouts": [
            {
                "type": "warning",
                "title": "Shared Mutable State",
                "content": "`bad_append(1)` followed by `bad_append(2)` returns `[1, 2]` because both calls mutate the single shared list attached to the function object!"
            }
        ],
        "keyTakeaway": "Default arguments evaluate once at function definition time; use None for mutable defaults."
    },
    {
        "id": "day7-step2",
        "stepNumber": 2,
        "title": "*args, **kwargs & Keyword-Only Arguments",
        "shortLabel": "Variadic & Keyword-Only",
        "type": "explanation",
        "isGated": false,
        "heading": "Flexibility with Variadic Arguments and Enforced Keyword Arguments",
        "subheading": "Capture arbitrary positional and keyword arguments cleanly.",
        "markdownContent": [
            "`*args` packs extra positional arguments into a `tuple`.",
            "`**kwargs` packs extra keyword arguments into a `dict`.",
            "Placing a bare `*` in the parameter list forces all subsequent parameters to be passed strictly as keyword arguments (keyword-only parameters), preventing ambiguous boolean flags."
        ],
        "snippets": [
            {
                "title": "Keyword-Only and Variadic Parameters",
                "code": "def configure(mode, *, timeout=30, verbose=False):\n    print(mode, timeout, verbose)\n\n# configure('prod', 10) # TypeError! timeout must be named\nconfigure('prod', timeout=10) # Valid!",
                "language": "python",
                "caption": "Enforcing keyword arguments with bare asterisk."
            }
        ],
        "callouts": [
            {
                "type": "tip",
                "title": "Self-Documenting Code",
                "content": "Keyword-only arguments prevent confusing calls like `load_data(True, False, 10)`."
            }
        ],
        "keyTakeaway": "*args gathers positional tuples, **kwargs gathers keyword dicts, and bare * enforces keyword-only args."
    },
    {
        "id": "day7-step3",
        "stepNumber": 3,
        "title": "Argument Signatures Checkpoint",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Test Your Understanding of Python Parameter Binding",
        "subheading": "Diagnose default argument mutations and variadic packing.",
        "checkpoints": [
            {
                "id": "chk-d7-q1",
                "question": "What is the output of running this code?\n\n```python\ndef add_item(val, items=[]):\n    items.append(val)\n    return items\n\nprint(add_item('A'))\nprint(add_item('B'))\n```",
                "options": [
                    {
                        "id": "A",
                        "label": "['A'] then ['B']"
                    },
                    {
                        "id": "B",
                        "label": "['A'] then ['A', 'B']"
                    },
                    {
                        "id": "C",
                        "label": "['A', 'B'] then ['A', 'B']"
                    },
                    {
                        "id": "D",
                        "label": "TypeError: default list not allowed"
                    }
                ],
                "correctOptionId": "B",
                "explanations": {
                    "A": "Incorrect: The default list is not recreated on the second call.",
                    "B": "Correct! Because default arguments are evaluated once at definition time, both calls mutate the exact same list object.",
                    "C": "Incorrect: The first call produces ['A'] before 'B' is added.",
                    "D": "Incorrect: Python allows mutable defaults, but it creates shared state bugs."
                }
            },
            {
                "id": "chk-d7-q2",
                "question": "In `def query(table, *, limit=100):`, how must `limit` be passed?",
                "options": [
                    {
                        "id": "A",
                        "label": "Only as a positional argument: query('users', 50)"
                    },
                    {
                        "id": "B",
                        "label": "Only as a keyword argument: query('users', limit=50)"
                    },
                    {
                        "id": "C",
                        "label": "Either positional or keyword"
                    },
                    {
                        "id": "D",
                        "label": "It cannot be overridden"
                    }
                ],
                "correctOptionId": "B",
                "explanations": {
                    "A": "Incorrect: The bare * prevents positional passing.",
                    "B": "Correct! Parameters defined after a bare * are strictly keyword-only.",
                    "C": "Incorrect: That would be the case without the bare *.",
                    "D": "Incorrect: Keyword-only arguments can be freely overridden by passing limit=value."
                }
            }
        ],
        "keyTakeaway": "Mutable defaults share state across calls; bare * enforces keyword-only parameters."
    },
    {
        "id": "day7-step4",
        "stepNumber": 4,
        "title": "Build Robust Function Signature",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Safe Tag Accumulator with Keyword-Only Options",
        "subheading": "Create a function that collects tags without mutable default side effects.",
        "task": {
            "title": "Safe Tag Register",
            "instructions": [
                "Define a function `register_tags(entity, *tags, prefix='#', existing=None)`.",
                "If `existing is None`, initialize `existing = []` inside the function.",
                "Iterate over `tags` and append `f'{prefix}{t}'` to `existing`.",
                "Return `existing`.",
                "Call `register_tags('Post1', 'python', 'dsa')` and print the returned list."
            ],
            "starterCode": "# Day 7 Practice: Safe Tag Register\n\ndef register_tags(entity, *tags, prefix=\"#\", existing=None):\n    # TODO 1: Guard against mutable default side-effects\n    if existing is None:\n        existing = []\n    \n    # TODO 2: Format each tag with prefix and append to existing\n    for t in tags:\n        pass\n        \n    return existing\n\nresult = register_tags(\"Post1\", \"python\", \"dsa\")\nprint(\"Tags:\", result)\n",
            "solutionCode": "def register_tags(entity, *tags, prefix=\"#\", existing=None):\n    if existing is None:\n        existing = []\n    for t in tags:\n        existing.append(f\"{prefix}{t}\")\n    return existing\n\nresult = register_tags(\"Post1\", \"python\", \"dsa\")\nprint(\"Tags:\", result)\n",
            "expectedOutputPatterns": [
                "Tags: ['#python', '#dsa']"
            ],
            "hint": "Use `if existing is None: existing = []` and append `f'{prefix}{t}'` for each tag in `tags`."
        },
        "keyTakeaway": "Variadic arguments gather elements into a tuple, while sentinel defaults ensure safety."
    },
    {
        "id": "day7-step5",
        "stepNumber": 5,
        "title": "Signatures & Arguments Mastery",
        "shortLabel": "Recap",
        "type": "completion",
        "isGated": false,
        "dayNumber": 7,
        "heading": "Day 7 Complete: Function Arguments & Signatures",
        "subheading": "You have mastered variadic arguments, keyword-only enforcement, and the mutable default trap.",
        "recapRows": [
            {
                "concept": "Default Argument Timing",
                "naiveIntuition": "Defaults evaluate each time the function is called",
                "pythonReality": "Defaults evaluate once at definition time; mutable defaults share state across calls"
            },
            {
                "concept": "Keyword-Only Asterisk",
                "naiveIntuition": "The * symbol can only be used with an argument name like *args",
                "pythonReality": "A bare * in the parameter list forces all following parameters to be keyword-only"
            }
        ],
        "solidifiedConcepts": [
            "Mutable Default Trap",
            "None Sentinel Pattern",
            "*args & **kwargs Packing",
            "Keyword-Only Parameters"
        ],
        "nextDayPreview": {
            "dayNumber": 8,
            "title": "Basic I/O & Robust Type Casting",
            "description": "Process standard input safely, parse structured tokens, handle EOF errors, and cast input data."
        }
    }
]
},
  8: {
  "dayNumber": 8,
  "title": "Basic I/O & Robust Type Casting",
  "topicName": "I/O & Type Casting",
  "sectionId": "python-foundations",
  "estimatedMinutes": 25,
  "difficulty": "BEGINNER",
  "prerequisites": [
    7
  ],
  "concepts": [
    "sys.stdin vs input()",
    "Type Casting",
    "EOF Handling",
    "Format Specifiers"
  ],
  "practiceSkills": [
    "Safe Type Conversion",
    "Input Parsing",
    "Exception-Resilient Casting"
  ]
,
  "steps": [
    {
        "id": "day8-step1",
        "stepNumber": 1,
        "title": "Input Streams & Fast I/O",
        "shortLabel": "Input & Streams",
        "type": "explanation",
        "isGated": false,
        "heading": "Standard Input, sys.stdin, and Type Casting",
        "subheading": "How Python reads input from terminal and competitive programming streams.",
        "markdownContent": [
            "`input()` reads a single line from standard input and always returns a `str` (stripping the trailing newline).",
            "For competitive programming and large datasets ($10^5+$ lines), `input()` is slow due to prompt handling. `sys.stdin.readline` is significantly faster because it reads directly from the OS buffer without overhead.",
            "Because input is always textual, numerical computations require explicit type casting: `int()` or `float()`."
        ],
        "snippets": [
            {
                "title": "Reading and Casting Multiple Values",
                "code": "# Parsing a line of space-separated integers\nline = \"10 20 30 40\"\nnums = [int(x) for x in line.split()]\nprint(nums)  # [10, 20, 30, 40]",
                "language": "python",
                "caption": "Splitting and casting strings into integers."
            }
        ],
        "callouts": [
            {
                "type": "tip",
                "title": "Fast I/O Pattern",
                "content": "In performance-critical input scenarios, use `import sys; input = sys.stdin.readline`."
            }
        ],
        "keyTakeaway": "Input is always string data; fast I/O uses sys.stdin.readline and explicit casting."
    },
    {
        "id": "day8-step2",
        "stepNumber": 2,
        "title": "Robust Casting & Formatting",
        "shortLabel": "Casting & Specifiers",
        "type": "explanation",
        "isGated": false,
        "heading": "Handling Conversion Errors and Advanced Format Specifiers",
        "subheading": "Safely parse numbers without crashing and format outputs with precision.",
        "markdownContent": [
            "Attempting to cast invalid strings like `int('abc')` or `int('3.14')` raises `ValueError`.",
            "To convert float strings to integers, cast through float first: `int(float('3.14'))` yields `3`.",
            "Format specifiers in f-strings control width, alignment, and decimal precision: `{val:.2f}` rounds to 2 decimal places, `{val:>10}` right-aligns in a 10-character field."
        ],
        "snippets": [
            {
                "title": "Format Specifiers in Action",
                "code": "pi = 3.14159265\nprint(f\"{pi:.3f}\")     # '3.142'\n\nval = 42\nprint(f\"{val:06d}\")    # '000042' (padded with zeros)",
                "language": "python",
                "caption": "Zero padding and precision formatting."
            }
        ],
        "callouts": [
            {
                "type": "warning",
                "title": "int('3.14') Raises ValueError",
                "content": "`int()` does not automatically parse decimal points. It expects integer string digits or an explicit base."
            }
        ],
        "keyTakeaway": "Use try/except for robust type casting and f-string format specifiers for structured output."
    },
    {
        "id": "day8-step3",
        "stepNumber": 3,
        "title": "I/O & Casting Checkpoint",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Test Your Mastery of Python Type Casting and Streams",
        "subheading": "Diagnose type conversion behavior and format outputs.",
        "checkpoints": [
            {
                "id": "chk-d8-q1",
                "question": "What happens when executing `int('45.8')` in Python?",
                "options": [
                    {
                        "id": "A",
                        "label": "Returns 45 (flooring the value)"
                    },
                    {
                        "id": "B",
                        "label": "Returns 46 (rounding up)"
                    },
                    {
                        "id": "C",
                        "label": "Raises ValueError"
                    },
                    {
                        "id": "D",
                        "label": "Returns 45.8 as a float"
                    }
                ],
                "correctOptionId": "C",
                "explanations": {
                    "A": "Incorrect: int() on a string cannot contain decimal dots.",
                    "B": "Incorrect: Python never rounds strings implicitly.",
                    "C": "Correct! int() on a string literal containing a decimal point raises ValueError: invalid literal for int() with base 10: '45.8'.",
                    "D": "Incorrect: int() never returns a float."
                }
            },
            {
                "id": "chk-d8-q2",
                "question": "What does `f'{7:04d}'` produce?",
                "options": [
                    {
                        "id": "A",
                        "label": "'7000'"
                    },
                    {
                        "id": "B",
                        "label": "'0007'"
                    },
                    {
                        "id": "C",
                        "label": "'   7'"
                    },
                    {
                        "id": "D",
                        "label": "'7.0000'"
                    }
                ],
                "correctOptionId": "B",
                "explanations": {
                    "A": "Incorrect: Zero padding pads on the left.",
                    "B": "Correct! :04d formats an integer with width 4, padding leading spaces with zeros, giving '0007'.",
                    "C": "Incorrect: :4d without 0 would pad with spaces.",
                    "D": "Incorrect: The format specifies integer 'd', not float 'f'."
                }
            }
        ],
        "keyTakeaway": "int() on a string with decimal raises ValueError; :04d zero-pads integers to width 4."
    },
    {
        "id": "day8-step4",
        "stepNumber": 4,
        "title": "Robust Input Parser",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Parse and Aggregate Mixed Sensor Readings",
        "subheading": "Write a parser that extracts valid numbers from dirty sensor string records.",
        "task": {
            "title": "Sensor Data Stream Parser",
            "instructions": [
                "Given `raw_records = [' 42 ', '15.5', 'ERROR', '99', 'N/A', '3.14']`.",
                "Iterate over `raw_records`, strip whitespace, and attempt to convert each item to a `float`.",
                "If conversion fails, ignore the item.",
                "Calculate the sum of all valid numbers, rounded to 2 decimal places.",
                "Print `'Valid count:', len(valid_nums)` and `'Total sum:', total_sum`."
            ],
            "starterCode": "# Day 8 Practice: Sensor Data Stream Parser\nraw_records = [\" 42 \", \"15.5\", \"ERROR\", \"99\", \"N/A\", \"3.14\"]\n\nvalid_nums = []\n\n# TODO: Parse raw_records safely\nfor rec in raw_records:\n    # Try converting rec.strip() to float; if ValueError occurs, continue\n    pass\n\ntotal_sum = round(sum(valid_nums), 2)\nprint(\"Valid count:\", len(valid_nums))\nprint(\"Total sum:\", total_sum)\n",
            "solutionCode": "raw_records = [\" 42 \", \"15.5\", \"ERROR\", \"99\", \"N/A\", \"3.14\"]\n\nvalid_nums = []\nfor rec in raw_records:\n    try:\n        val = float(rec.strip())\n        valid_nums.append(val)\n    except ValueError:\n        continue\n\ntotal_sum = round(sum(valid_nums), 2)\nprint(\"Valid count:\", len(valid_nums))\nprint(\"Total sum:\", total_sum)\n",
            "expectedOutputPatterns": [
                "Valid count: 4",
                "Total sum: 159.64"
            ],
            "hint": "Use a try / except ValueError block around float(rec.strip()) to safely filter out corrupted records."
        },
        "keyTakeaway": "Defensive type casting with try/except ensures robust processing of external streams."
    },
    {
        "id": "day8-step5",
        "stepNumber": 5,
        "title": "I/O & Type Casting Mastery",
        "shortLabel": "Recap",
        "type": "completion",
        "isGated": false,
        "dayNumber": 8,
        "heading": "Day 8 Complete: Basic I/O & Robust Type Casting",
        "subheading": "You have mastered stream processing, conversion exception safety, and format specifiers.",
        "recapRows": [
            {
                "concept": "int() on Float String",
                "naiveIntuition": "int('12.34') will truncate to 12",
                "pythonReality": "It raises ValueError; you must parse as float first: int(float('12.34'))"
            },
            {
                "concept": "input() Speed",
                "naiveIntuition": "input() is identical in speed to sys.stdin.readline()",
                "pythonReality": "input() has significant interactive overhead; sys.stdin.readline is 3-5x faster"
            }
        ],
        "solidifiedConcepts": [
            "sys.stdin vs input()",
            "Type Casting Invariants",
            "Format Specifiers (:04d, :.2f)",
            "Defensive ValueError Handling"
        ],
        "nextDayPreview": {
            "dayNumber": 9,
            "title": "Python Standard Library Essentials",
            "description": "Leverage standard modules including math, sys, random, and string for algorithmic utility."
        }
    }
]
},
  9: {
  "dayNumber": 9,
  "title": "Python Standard Library Essentials",
  "topicName": "Standard Library",
  "sectionId": "python-foundations",
  "estimatedMinutes": 30,
  "difficulty": "BEGINNER",
  "prerequisites": [
    8
  ],
  "concepts": [
    "math Module",
    "sys Module",
    "random Module",
    "Builtin Functions"
  ],
  "practiceSkills": [
    "Math Utility Usage",
    "System Introspection",
    "Builtin Combinations"
  ]
,
  "steps": [
    {
        "id": "day9-step1",
        "stepNumber": 1,
        "title": "The math & sys Modules",
        "shortLabel": "math & sys Modules",
        "type": "explanation",
        "isGated": false,
        "heading": "Standard Library Powerhouse: math and sys",
        "subheading": "Leverage C-accelerated math routines and system properties.",
        "markdownContent": [
            "Python's `math` module provides high-speed C-level mathematical functions: `math.gcd(a, b)`, `math.isqrt(n)` (integer square root), `math.comb(n, k)`, `math.ceil()`, and `math.floor()`.",
            "`math.isqrt(n)` computes $\\lfloor\\sqrt{n}\\rfloor$ using exact integer arithmetic without floating-point precision inaccuracies\u2014vital for number theory and prime testing.",
            "The `sys` module provides system-level information: `sys.maxsize` (maximum addressable integer pointer size), `sys.setrecursionlimit()`, and `sys.getsizeof()`."
        ],
        "snippets": [
            {
                "title": "math and sys Essentials",
                "code": "import math, sys\n\nprint(math.gcd(48, 180)) # 12\nprint(math.isqrt(27))    # 5 (exact integer floor)\nprint(sys.maxsize > 2**31) # True (on 64-bit platforms)",
                "language": "python",
                "caption": "C-accelerated math primitives."
            }
        ],
        "callouts": [
            {
                "type": "tip",
                "title": "Use math.isqrt instead of int(n**0.5)",
                "content": "For large numbers ($n > 10^{15}$), `float(n**0.5)` loses precision bits. `math.isqrt(n)` is mathematically exact."
            }
        ],
        "keyTakeaway": "math.gcd and math.isqrt provide exact, C-optimized numerical operations."
    },
    {
        "id": "day9-step2",
        "stepNumber": 2,
        "title": "Essential Built-ins: zip, enumerate, any, all",
        "shortLabel": "Core Built-ins",
        "type": "explanation",
        "isGated": false,
        "heading": "Idiomatic Iteration with enumerate, zip, any, and all",
        "subheading": "Replace manual indexing loops with clean built-in iterators.",
        "markdownContent": [
            "`enumerate(iterable, start=0)` yields `(index, item)` tuples, eliminating manual index counters.",
            "`zip(*iterables)` aggregates elements from each iterable in parallel, stopping when the shortest iterable is exhausted.",
            "`any(iterable)` returns `True` if at least one element is truthy (short-circuiting early).",
            "`all(iterable)` returns `True` only if every element is truthy."
        ],
        "snippets": [
            {
                "title": "Built-ins in Action",
                "code": "names = ['Alice', 'Bob', 'Charlie']\nfor idx, name in enumerate(names, start=1):\n    print(f'{idx}. {name}')\n\nscores = [85, 92, 78]\nfor name, score in zip(names, scores):\n    print(f'{name}: {score}')",
                "language": "python",
                "caption": "Clean pairing and index tracking."
            }
        ],
        "callouts": [
            {
                "type": "deep-dive",
                "title": "any and all Short-Circuit",
                "content": "`any([False, True, crash()])` will NEVER call `crash()` because it short-circuits on `True`."
            }
        ],
        "keyTakeaway": "enumerate tracks indices cleanly, zip pairs sequences, and any/all provide short-circuiting tests."
    },
    {
        "id": "day9-step3",
        "stepNumber": 3,
        "title": "Standard Library Checkpoint",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Verify Your Command of Standard Utilities",
        "subheading": "Evaluate zip, enumerate, and math routines.",
        "checkpoints": [
            {
                "id": "chk-d9-q1",
                "question": "What is the result of `list(zip([1, 2, 3], ['a', 'b']))`?",
                "options": [
                    {
                        "id": "A",
                        "label": "[(1, 'a'), (2, 'b'), (3, None)]"
                    },
                    {
                        "id": "B",
                        "label": "[(1, 'a'), (2, 'b')]"
                    },
                    {
                        "id": "C",
                        "label": "ValueError: unequal sequence lengths"
                    },
                    {
                        "id": "D",
                        "label": "[(1, 'a'), (2, 'b'), (3, '')]"
                    }
                ],
                "correctOptionId": "B",
                "explanations": {
                    "A": "Incorrect: zip() does not pad with None (that is itertools.zip_longest).",
                    "B": "Correct! Standard zip() stops as soon as the shortest input sequence is exhausted.",
                    "C": "Incorrect: zip() does not raise ValueError on mismatched lengths.",
                    "D": "Incorrect: No padding occurs."
                }
            },
            {
                "id": "chk-d9-q2",
                "question": "Why is `math.isqrt(n)` preferred over `int(math.sqrt(n))` for large integers?",
                "options": [
                    {
                        "id": "A",
                        "label": "math.sqrt() is deprecated in Python 3"
                    },
                    {
                        "id": "B",
                        "label": "math.sqrt() converts to a 64-bit float, causing precision loss for n > 2^53"
                    },
                    {
                        "id": "C",
                        "label": "math.isqrt() returns a floating point number"
                    },
                    {
                        "id": "D",
                        "label": "math.isqrt() only works for prime numbers"
                    }
                ],
                "correctOptionId": "B",
                "explanations": {
                    "A": "Incorrect: math.sqrt() is not deprecated.",
                    "B": "Correct! Floats have 53 bits of precision (~15-17 decimal digits). For large integers, math.sqrt loses precision, while math.isqrt uses exact integer arithmetic.",
                    "C": "Incorrect: math.isqrt() returns an integer.",
                    "D": "Incorrect: math.isqrt works on all non-negative integers."
                }
            }
        ],
        "keyTakeaway": "zip() terminates at the shortest input; math.isqrt() preserves exact integer precision."
    },
    {
        "id": "day9-step4",
        "stepNumber": 4,
        "title": "Leaderboard Pairer with zip and enumerate",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Construct Formatted Ranked Leaderboard",
        "subheading": "Combine zip and enumerate to rank player scores.",
        "task": {
            "title": "Leaderboard Formatter",
            "instructions": [
                "Given `players = ['Diana', 'Bruce', 'Clark']` and `scores = [950, 890, 920]`.",
                "Pair each player with their score, and sort the pairs in descending order of score.",
                "Enumerate through the sorted leaderboard starting from rank 1.",
                "Print each entry formatted as `f'{rank}. {player} - {score} pts'`."
            ],
            "starterCode": "# Day 9 Practice: Leaderboard Formatter\nplayers = [\"Diana\", \"Bruce\", \"Clark\"]\nscores = [950, 890, 920]\n\n# TODO 1: Pair players with scores using zip\npairs = list(zip(players, scores))\n\n# TODO 2: Sort pairs descending by score (score is at index 1 of the tuple)\nsorted_pairs = sorted(pairs, key=lambda x: x[1], reverse=True)\n\n# TODO 3: Enumerate starting at rank 1 and print each line\nfor rank, (player, score) in enumerate(sorted_pairs, start=1):\n    print(f\"{rank}. {player} - {score} pts\")\n",
            "solutionCode": "players = [\"Diana\", \"Bruce\", \"Clark\"]\nscores = [950, 890, 920]\n\npairs = list(zip(players, scores))\nsorted_pairs = sorted(pairs, key=lambda x: x[1], reverse=True)\n\nfor rank, (player, score) in enumerate(sorted_pairs, start=1):\n    print(f\"{rank}. {player} - {score} pts\")\n",
            "expectedOutputPatterns": [
                "1. Diana - 950 pts",
                "2. Clark - 920 pts",
                "3. Bruce - 890 pts"
            ],
            "hint": "Combine zip(players, scores) and enumerate(sorted_pairs, start=1) to generate ranked outputs."
        },
        "keyTakeaway": "Combining built-in iterators like zip and enumerate produces expressive, idiomatic code."
    },
    {
        "id": "day9-step5",
        "stepNumber": 5,
        "title": "Standard Library Essentials Mastery",
        "shortLabel": "Recap",
        "type": "completion",
        "isGated": false,
        "dayNumber": 9,
        "heading": "Day 9 Complete: Python Standard Library Essentials",
        "subheading": "You have mastered math modules, system properties, and core built-in iterators.",
        "recapRows": [
            {
                "concept": "zip Length Handling",
                "naiveIntuition": "zip pads missing values from shorter lists",
                "pythonReality": "Standard zip stops at the shortest list; use itertools.zip_longest for padding"
            },
            {
                "concept": "Integer Square Root",
                "naiveIntuition": "int(n**0.5) is safe for all integers",
                "pythonReality": "Floating point casting loses precision for large numbers; use math.isqrt(n)"
            }
        ],
        "solidifiedConcepts": [
            "math.gcd & math.isqrt",
            "enumerate(seq, start=1)",
            "zip(*iterables) Semantics",
            "any() & all() Short-Circuiting"
        ],
        "nextDayPreview": {
            "dayNumber": 10,
            "title": "Foundations Check & Synthetic Practice",
            "description": "Synthesize variables, conditionals, loops, and functional decomposition to build self-contained algorithmic scripts."
        }
    }
]
},
  10: {
  "dayNumber": 10,
  "title": "Foundations Check & Synthetic Practice",
  "topicName": "Section 1 Synthesis",
  "sectionId": "python-foundations",
  "estimatedMinutes": 35,
  "difficulty": "BEGINNER",
  "prerequisites": [
    9
  ],
  "concepts": [
    "Control Flow Synthesis",
    "Decomposition",
    "Edge Case Handling",
    "Code Cleanliness"
  ],
  "practiceSkills": [
    "Multi-Concept Integration",
    "Algorithm Decomposition",
    "Edge Case Hardening"
  ]
,
  "steps": [
    {
        "id": "day10-step1",
        "stepNumber": 1,
        "title": "Section 1 Architectural Synthesis",
        "shortLabel": "Synthesis Model",
        "type": "explanation",
        "isGated": false,
        "heading": "Synthesizing Python Foundations: Memory, Flow & Semantics",
        "subheading": "Consolidate the core mental models established in Days 1 through 9.",
        "markdownContent": [
            "Over the first 9 days, you built the foundation of Python computation:",
            "1. **Names & Memory**: Variables are name tags bound to heap objects; numbers and strings are immutable; assignment never copies values into boxes.",
            "2. **Arithmetic & Logic**: Floor division rounds toward negative infinity (`//`), logical operators return decisive operands, and every object has a boolean truth value.",
            "3. **Control Flow & Scope**: Loops support lazy evaluation with `range()` and search fallbacks with `else:`; functions encapsulate frames following the LEGB scope rule.",
            "4. **Argument Protocols & Built-ins**: Default arguments evaluate once; built-ins like `enumerate`, `zip`, and `math` provide C-accelerated primitives."
        ],
        "snippets": [
            {
                "title": "Integrated Pythonic Pattern",
                "code": "def process_batch(items, *, max_limit=10, transform=None):\n    \"\"\"Demonstrates keyword-only enforcement and None sentinel defaults.\"\"\"\n    if transform is None:\n        transform = lambda x: x\n    return [transform(x) for x in items[:max_limit]]",
                "language": "python",
                "caption": "Combining function signatures, guards, and comprehensions."
            }
        ],
        "callouts": [
            {
                "type": "tip",
                "title": "Milestone Achievement",
                "content": "You are now ready to tackle composite data structures (lists, dicts, sets, tuples) in Section 2 with zero misconceptions about memory!"
            }
        ],
        "keyTakeaway": "A solid understanding of memory references, scope, and control flow enables confident Python architecture."
    },
    {
        "id": "day10-step2",
        "stepNumber": 2,
        "title": "Decomposition & Edge Case Checklist",
        "shortLabel": "Decomposition",
        "type": "explanation",
        "isGated": false,
        "heading": "Algorithmic Thinking: Breaking Down Multi-Step Problems",
        "subheading": "A systematic framework for decomposing engineering challenges.",
        "markdownContent": [
            "When solving multi-step programming tasks:",
            "1. **Input Validation**: Check for empty inputs, zeroes, negative bounds, and unexpected types.",
            "2. **Invariant Definition**: Identify what condition must hold true before and after each loop iteration.",
            "3. **State Isolation**: Ensure functions compute results purely without leaking state to outer scopes.",
            "4. **Complexity Budget**: Verify that your approach scales cleanly within memory and time constraints."
        ],
        "snippets": [
            {
                "title": "Defensive Decomposition Pattern",
                "code": "def find_first_peak(nums):\n    if not nums: # Guard empty\n        return None\n    for i in range(len(nums)):\n        left = nums[i-1] if i > 0 else float('-inf')\n        right = nums[i+1] if i < len(nums) - 1 else float('-inf')\n        if nums[i] >= left and nums[i] >= right:\n            return (i, nums[i])\n    return None",
                "language": "python",
                "caption": "Guarding boundaries and managing edge states."
            }
        ],
        "callouts": [
            {
                "type": "deep-dive",
                "title": "Avoid Clumsy Flags",
                "content": "Notice how the guard `if not nums:` handles empty inputs upfront, simplifying subsequent logic."
            }
        ],
        "keyTakeaway": "Guard edge cases early and isolate invariants across loop cycles."
    },
    {
        "id": "day10-step3",
        "stepNumber": 3,
        "title": "Foundations Milestone Checkpoint",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Verify Section 1 Mastery Across Core Tenets",
        "subheading": "Test your synthesized mental model of Python fundamentals.",
        "checkpoints": [
            {
                "id": "chk-d10-q1",
                "question": "Which of the following statements about Python memory and assignment is TRUE?",
                "options": [
                    {
                        "id": "A",
                        "label": "a = [1, 2]; b = a creates an independent clone of the list in memory"
                    },
                    {
                        "id": "B",
                        "label": "Integers and strings can have their internal characters/values modified in-place"
                    },
                    {
                        "id": "C",
                        "label": "Assignment binds a name tag in the local namespace to an object in heap memory"
                    },
                    {
                        "id": "D",
                        "label": "Variables store values directly inside named memory slots like C structs"
                    }
                ],
                "correctOptionId": "C",
                "explanations": {
                    "A": "Incorrect: b = a binds 'b' to the exact same list object in memory.",
                    "B": "Incorrect: Integers and strings are strictly immutable.",
                    "C": "Correct! In Python, variables are names pointing to heap objects; assignment attaches or rebinds these name tags.",
                    "D": "Incorrect: Python uses object references, not fixed value boxes."
                }
            },
            {
                "id": "chk-d10-q2",
                "question": "What will `bool([]) or 'OK' and 0 or [42]` evaluate to?",
                "options": [
                    {
                        "id": "A",
                        "label": "True"
                    },
                    {
                        "id": "B",
                        "label": "'OK'"
                    },
                    {
                        "id": "C",
                        "label": "[42]"
                    },
                    {
                        "id": "D",
                        "label": "0"
                    }
                ],
                "correctOptionId": "C",
                "explanations": {
                    "A": "Incorrect: Short-circuiting returns the decisive operand object, not a boolean.",
                    "B": "Incorrect: 'and' binds tighter than 'or'. 'OK' and 0 evaluates to 0.",
                    "C": "Correct! Precedence: ('OK' and 0) evaluates to 0. The expression becomes: bool([]) or 0 or [42]. bool([]) is False. False or 0 is 0 (falsy). 0 or [42] returns [42]!",
                    "D": "Incorrect: 0 is falsy, so evaluation continues to [42]."
                }
            }
        ],
        "keyTakeaway": "Operator precedence: 'and' binds tighter than 'or', and short-circuiting returns the decisive operand."
    },
    {
        "id": "day10-step4",
        "stepNumber": 4,
        "title": "Synthesize: Transaction Validator",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Build an End-to-End Account Ledger Validator",
        "subheading": "Combine functions, loops, safe casting, guards, and formatted outputs.",
        "task": {
            "title": "Financial Ledger Validator",
            "instructions": [
                "Given raw ledger entries: `entries = ['100.50', '-25.00', 'INVALID', '50.25', '  -10.75  ', 'N/A']`.",
                "Parse valid numerical transactions (floats) defensively, ignoring invalid tokens.",
                "Separate transactions into `credits` (positive amounts) and `debits` (negative amounts).",
                "Compute `net_balance = sum(credits) + sum(debits)`, rounded to 2 decimal places.",
                "Print `'Credits count:', len(credits)`",
                "Print `'Debits count:', len(debits)`",
                "Print `'Net balance:', f'{net_balance:.2f}'`."
            ],
            "starterCode": "# Day 10 Practice: Financial Ledger Validator\nentries = [\"100.50\", \"-25.00\", \"INVALID\", \"50.25\", \"  -10.75  \", \"N/A\"]\n\ncredits = []\ndebits = []\n\n# TODO: Parse valid transactions and separate into credits and debits\nfor item in entries:\n    pass\n\nnet_balance = round(sum(credits) + sum(debits), 2)\n\nprint(\"Credits count:\", len(credits))\nprint(\"Debits count:\", len(debits))\nprint(\"Net balance:\", f\"{net_balance:.2f}\")\n",
            "solutionCode": "entries = [\"100.50\", \"-25.00\", \"INVALID\", \"50.25\", \"  -10.75  \", \"N/A\"]\n\ncredits = []\ndebits = []\n\nfor item in entries:\n    try:\n        val = float(item.strip())\n        if val >= 0:\n            credits.append(val)\n        else:\n            debits.append(val)\n    except ValueError:\n        continue\n\nnet_balance = round(sum(credits) + sum(debits), 2)\n\nprint(\"Credits count:\", len(credits))\nprint(\"Debits count:\", len(debits))\nprint(\"Net balance:\", f\"{net_balance:.2f}\")\n",
            "expectedOutputPatterns": [
                "Credits count: 2",
                "Debits count: 2",
                "Net balance: 115.00"
            ],
            "hint": "Use try/except ValueError on float(item.strip()), append positive values to credits and negative values to debits."
        },
        "keyTakeaway": "Synthesizing parsing, validation, and control flow builds resilient software foundations."
    },
    {
        "id": "day10-step5",
        "stepNumber": 5,
        "title": "Section 1 Foundations Mastery",
        "shortLabel": "Recap",
        "type": "completion",
        "isGated": false,
        "dayNumber": 10,
        "heading": "Day 10 Complete: Foundations Check & Synthetic Practice",
        "subheading": "Congratulations! You have completed Section 1: Python Foundations with deep conceptual and practical mastery.",
        "recapRows": [
            {
                "concept": "Variables & Memory",
                "naiveIntuition": "Variables are boxes holding copied values",
                "pythonReality": "Variables are pointers/labels bound to heap objects"
            },
            {
                "concept": "Operator Precedence",
                "naiveIntuition": "Expressions evaluate strictly left to right",
                "pythonReality": "Arithmetic and logical operators adhere to strict precedence ('and' before 'or')"
            }
        ],
        "solidifiedConcepts": [
            "Python Memory Model",
            "Short-Circuit Logic",
            "Loop-else Constructs",
            "LEGB Function Scoping",
            "Defensive I/O"
        ],
        "nextDayPreview": {
            "dayNumber": 11,
            "title": "Lists: Memory Layout & Dynamic Resizing",
            "description": "Analyze dynamic array memory layouts, pointer arrays in CPython, amortized O(1) append, and the O(N) insert/pop(0) penalty."
        }
    }
]
},
  11: {
  "dayNumber": 11,
  "title": "Lists: Memory Layout & Operations",
  "topicName": "Dynamic Arrays",
  "sectionId": "python-core",
  "estimatedMinutes": 30,
  "difficulty": "FOUNDATIONAL",
  "prerequisites": [
    10
  ],
  "concepts": [
    "Dynamic Array Internals",
    "Amortized O(1)",
    "append vs insert",
    "Over-allocation"
  ],
  "practiceSkills": [
    "List Construction",
    "Amortized Cost Analysis",
    "In-Place Modifications"
  ]
,
  "steps": [
    {
        "id": "day11-step1",
        "stepNumber": 1,
        "title": "CPython List Memory Layout",
        "shortLabel": "Memory Layout",
        "type": "explanation",
        "isGated": false,
        "heading": "How Python Lists Work Under the Hood: Contiguous Pointer Arrays",
        "subheading": "Discover why Python lists are dynamic arrays of pointers, not linked lists.",
        "markdownContent": [
            "In CPython, a `list` is implemented as a variable-length contiguous array of pointers to objects (`PyObject**`). The list itself does not store the objects directly; it stores 64-bit memory addresses pointing to the objects on the heap.",
            "Because pointers are laid out contiguously in memory, indexing (`lst[i]`) is an immediate $O(1)$ arithmetic pointer offset: `base_address + i * 8 bytes`.",
            "When appending items, CPython uses an over-allocation strategy: when capacity is exceeded, it allocates extra headroom (approx. growth factor ~1.125x + 3 to 6 slots). This guarantees that `append()` has an **amortized $O(1)$** time complexity."
        ],
        "snippets": [
            {
                "title": "List Pointer Array Mechanics",
                "code": "import sys\nitems = []\nprint('Initial size:', sys.getsizeof(items))\nfor i in range(10):\n    items.append(i)\n    print(f'Len: {len(items)}, Size in bytes: {sys.getsizeof(items)}')",
                "language": "python",
                "caption": "Watching CPython resize and over-allocate capacity in bursts."
            }
        ],
        "callouts": [
            {
                "type": "tip",
                "title": "Amortized O(1) append",
                "content": "Most `append()` calls take O(1) time. Occasionally a resize takes O(N) to copy pointers, but amortized across all appends, each append costs O(1)."
            }
        ],
        "keyTakeaway": "Lists are contiguous pointer arrays providing O(1) indexing and amortized O(1) appending."
    },
    {
        "id": "day11-step2",
        "stepNumber": 2,
        "title": "append vs insert & pop Complexity",
        "shortLabel": "Cost Trade-offs",
        "type": "explanation",
        "isGated": false,
        "heading": "Why insert(0, x) is O(N) While append(x) is O(1)",
        "subheading": "Understanding the computational cost of shifting array elements.",
        "markdownContent": [
            "Adding to the end with `lst.append(x)` is amortized $O(1)$ because no other elements shift.",
            "Inserting at the beginning with `lst.insert(0, x)` or popping from the beginning with `lst.pop(0)` is $O(N)$! Every existing pointer in the array must be shifted by one memory slot.",
            "Popping from the end `lst.pop()` is $O(1)$ because no element shifting is required.",
            "If you frequently add or remove items from the front of a sequence, use `collections.deque` ($O(1)$ at both ends) instead of a list."
        ],
        "snippets": [
            {
                "title": "Operation Complexities",
                "code": "lst = [10, 20, 30]\nlst.append(40) # O(1) amortized - appends at end\nlst.pop()       # O(1) - removes from end\nlst.insert(0, 5) # O(N) - shifts all elements right!\nlst.pop(0)      # O(N) - shifts all elements left!",
                "language": "python",
                "caption": "Operations at the front shift all elements, costing O(N)."
            }
        ],
        "callouts": [
            {
                "type": "warning",
                "title": "Queue Anti-Pattern",
                "content": "Never use `list.pop(0)` as a queue in algorithmic problems! N pops from a list will degrade your algorithm to $O(N^2)$."
            }
        ],
        "keyTakeaway": "append and pop at the end are O(1); insert and pop at index 0 require O(N) shifts."
    },
    {
        "id": "day11-step3",
        "stepNumber": 3,
        "title": "List Operations Checkpoint",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Verify Your Understanding of List Complexities",
        "subheading": "Test your knowledge of pointer arrays and shifting costs.",
        "checkpoints": [
            {
                "id": "chk-d11-q1",
                "question": "What is the time complexity of `lst.insert(0, val)` on a list of length N?",
                "options": [
                    {
                        "id": "A",
                        "label": "O(1)"
                    },
                    {
                        "id": "B",
                        "label": "O(log N)"
                    },
                    {
                        "id": "C",
                        "label": "O(N)"
                    },
                    {
                        "id": "D",
                        "label": "O(N^2)"
                    }
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
                    {
                        "id": "A",
                        "label": "The raw bytes of each number and string packed directly"
                    },
                    {
                        "id": "B",
                        "label": "64-bit pointers (memory addresses) pointing to objects on the heap"
                    },
                    {
                        "id": "C",
                        "label": "A doubly linked list of node structs"
                    },
                    {
                        "id": "D",
                        "label": "A hash table of indices to values"
                    }
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
        "keyTakeaway": "Lists store contiguous object pointers; inserting at index 0 requires O(N) shifts."
    },
    {
        "id": "day11-step4",
        "stepNumber": 4,
        "title": "Efficient In-Place Operations",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Filter and Reverse Array In-Place",
        "subheading": "Manipulate list pointers efficiently using in-place methods.",
        "task": {
            "title": "In-Place List Processing",
            "instructions": [
                "Given `nums = [12, 5, 8, 19, 24, 7, 10]`.",
                "Filter `nums` in-place so it retains only numbers greater than 10 (or build a filtered list).",
                "Reverse the resulting list in-place using `.reverse()`.",
                "Print `'Processed list:', nums`."
            ],
            "starterCode": "# Day 11 Practice: In-Place List Processing\nnums = [12, 5, 8, 19, 24, 7, 10]\n\n# TODO 1: Filter nums to retain only numbers greater than 10\n# (Build a list of numbers > 10 or filter in a loop)\nnums = []\n\n# TODO 2: Reverse nums in-place by calling nums.reverse()\n\nprint(\"Processed list:\", nums)\n",
            "solutionCode": "nums = [12, 5, 8, 19, 24, 7, 10]\nnums = [x for x in nums if x > 10]\nnums.reverse()\n\nprint(\"Processed list:\", nums)\n",
            "expectedOutputPatterns": [
                "Processed list: [24, 19, 12]"
            ],
            "hint": "Filter elements with `[x for x in nums if x > 10]` then call `nums.reverse()`."
        },
        "keyTakeaway": "List methods like .reverse() mutate the list in-place in O(N) time with O(1) extra space."
    },
    {
        "id": "day11-step5",
        "stepNumber": 5,
        "title": "Lists & Memory Layout Mastery",
        "shortLabel": "Recap",
        "type": "completion",
        "isGated": false,
        "dayNumber": 11,
        "heading": "Day 11 Complete: Lists: Memory Layout & Operations",
        "subheading": "You have mastered contiguous pointer arrays, amortized resizing, and operation costs.",
        "recapRows": [
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
        "solidifiedConcepts": [
            "Contiguous Pointer Array Layout",
            "Amortized O(1) Over-Allocation",
            "insert(0) vs append() Costs",
            "In-Place List Mutation"
        ],
        "nextDayPreview": {
            "dayNumber": 12,
            "title": "List Slicing O(K) Cost & Mutability Traps",
            "description": "Analyze the O(K) time and space complexity of list slicing, shallow vs deep copies, and in-place list mutations."
        }
    }
]
},
  12: {
  "dayNumber": 12,
  "title": "List Slicing & Mutability Traps",
  "topicName": "List Slicing & Copies",
  "sectionId": "python-core",
  "estimatedMinutes": 30,
  "difficulty": "FOUNDATIONAL",
  "prerequisites": [
    11
  ],
  "concepts": [
    "Shallow vs Deep Copy",
    "copy module",
    "Slice Assignment",
    "is vs =="
  ],
  "practiceSkills": [
    "Shallow vs Deep Copying",
    "Slice Mutation",
    "Reference Isolation"
  ]
,
  "steps": [
    {
        "id": "day12-step1",
        "stepNumber": 1,
        "title": "Shallow vs Deep Copies",
        "shortLabel": "Shallow vs Deep Copy",
        "type": "explanation",
        "isGated": false,
        "heading": "The Shallow Copy Hazard with Nested Mutable Objects",
        "subheading": "Learn why slice copies only copy outer pointers, leaving inner objects shared.",
        "markdownContent": [
            "When you slice a list with `new_list = old_list[:]` or call `old_list.copy()`, Python performs a **shallow copy**.",
            "A shallow copy creates a new outer list container, but it copies the exact same object pointers from the original list.",
            "If the list contains mutable child objects (like nested lists `[[1, 2], [3, 4]]`), mutating an inner list through `new_list[0].append(99)` also mutates `old_list[0]`!",
            "To create a completely independent duplicate including all nested sub-objects, use `copy.deepcopy()`."
        ],
        "snippets": [
            {
                "title": "Shallow Copy Hazard",
                "code": "import copy\norig = [[1, 2], [3, 4]]\nshallow = orig[:]        # Shallow copy\ndeep = copy.deepcopy(orig) # Deep copy\n\nshallow[0].append(99) # Mutates orig[0] as well!\ndeep[1].append(88)    # Does NOT mutate orig[1]\nprint('Original:', orig)",
                "language": "python",
                "caption": "Shallow copies share pointers to nested mutable children."
            }
        ],
        "callouts": [
            {
                "type": "warning",
                "title": "The [[0] * N] * M Trap",
                "content": "`grid = [[0] * 3] * 3` creates 3 references to the EXACT SAME row list! Mutating `grid[0][0] = 1` turns the entire column into 1s. Always write `[[0] * 3 for _ in range(3)]`."
            }
        ],
        "keyTakeaway": "Shallow copies duplicate the outer pointer buffer; deepcopy clones all nested objects."
    },
    {
        "id": "day12-step2",
        "stepNumber": 2,
        "title": "Slice Assignment Mechanics",
        "shortLabel": "Slice Assignment",
        "type": "explanation",
        "isGated": false,
        "heading": "Replacing, Inserting, and Deleting Slices In-Place",
        "subheading": "Powerful in-place mutations using target slices.",
        "markdownContent": [
            "Slice assignment `lst[start:stop] = iterable` replaces the targeted slice range with elements from the iterable in-place.",
            "Unlike item assignment (`lst[0] = x`), slice assignment can expand or contract the list length: `lst[1:3] = [10, 20, 30, 40]` expands the list.",
            "Assigning an empty list `lst[1:3] = []` deletes that slice in-place.",
            "`lst[:] = new_items` replaces all elements in-place while **preserving the original list identity (`id(lst)`)**."
        ],
        "snippets": [
            {
                "title": "Slice Assignment in Action",
                "code": "nums = [1, 2, 3, 4, 5]\nnums[1:4] = [20, 30] # Replaces [2, 3, 4] with [20, 30]\nprint(nums)          # [1, 20, 30, 5]\n\nnums[:] = [99]       # In-place wipe and replace\nprint(nums)          # [99]",
                "language": "python",
                "caption": "Slice assignment modifies length and contents in-place."
            }
        ],
        "callouts": [
            {
                "type": "tip",
                "title": "Pass by Reference In-Place Mutation",
                "content": "In LeetCode problems requiring in-place modification (like 'Remove Duplicates'), `nums[:] = clean_nums` modifies the caller's array directly."
            }
        ],
        "keyTakeaway": "Slice assignment modifies list contents and lengths in-place while keeping the object ID intact."
    },
    {
        "id": "day12-step3",
        "stepNumber": 3,
        "title": "Copies & Slices Checkpoint",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Test Your Mastery of Copies and Slice Assignment",
        "subheading": "Diagnose shared references and slice replacements.",
        "checkpoints": [
            {
                "id": "chk-d12-q1",
                "question": "What is the content of `matrix` after running this code?\n\n```python\nmatrix = [[0] * 2] * 2\nmatrix[0][0] = 7\n```",
                "options": [
                    {
                        "id": "A",
                        "label": "[[7, 0], [0, 0]]"
                    },
                    {
                        "id": "B",
                        "label": "[[7, 0], [7, 0]]"
                    },
                    {
                        "id": "C",
                        "label": "[[7, 7], [0, 0]]"
                    },
                    {
                        "id": "D",
                        "label": "TypeError: cannot mutate nested lists"
                    }
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
                    {
                        "id": "A",
                        "label": "There is no difference"
                    },
                    {
                        "id": "B",
                        "label": "b[:] creates a shallow copy where a[0] is b[0]; deepcopy creates an independent inner list"
                    },
                    {
                        "id": "C",
                        "label": "deepcopy is faster and uses less memory"
                    },
                    {
                        "id": "D",
                        "label": "b[:] mutates b"
                    }
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
        "keyTakeaway": "Multiplication of lists duplicates pointers; deepcopy recursively duplicates nested objects."
    },
    {
        "id": "day12-step4",
        "stepNumber": 4,
        "title": "Build 2D Grid Safely",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Construct an Independent 2D Matrix",
        "subheading": "Create a 3x3 matrix where each row is an independent list object.",
        "task": {
            "title": "Safe 2D Matrix Creator",
            "instructions": [
                "Build a 3-row by 3-column matrix initialized with zeroes using a list comprehension: `[[0] * 3 for _ in range(3)]`.",
                "Set the center cell `matrix[1][1] = 5`.",
                "Set top-left cell `matrix[0][0] = 1` and bottom-right cell `matrix[2][2] = 9`.",
                "Print row 0, row 1, and row 2 on separate lines."
            ],
            "starterCode": "# Day 12 Practice: Safe 2D Matrix Creator\n\n# TODO 1: Construct a 3x3 grid with independent rows using list comprehension\nmatrix = []\n\n# TODO 2: Update specific coordinates\n# matrix[0][0] = 1\n# matrix[1][1] = 5\n# matrix[2][2] = 9\n\nfor row in matrix:\n    print(row)\n",
            "solutionCode": "matrix = [[0] * 3 for _ in range(3)]\nmatrix[0][0] = 1\nmatrix[1][1] = 5\nmatrix[2][2] = 9\n\nfor row in matrix:\n    print(row)\n",
            "expectedOutputPatterns": [
                "[1, 0, 0]",
                "[0, 5, 0]",
                "[0, 0, 9]"
            ],
            "hint": "Use `matrix = [[0] * 3 for _ in range(3)]` then assign individual cell coordinates."
        },
        "keyTakeaway": "List comprehensions evaluate the row constructor on each iteration, creating separate objects."
    },
    {
        "id": "day12-step5",
        "stepNumber": 5,
        "title": "List Copies & Slices Mastery",
        "shortLabel": "Recap",
        "type": "completion",
        "isGated": false,
        "dayNumber": 12,
        "heading": "Day 12 Complete: List Slicing & Mutability Traps",
        "subheading": "You have mastered shallow vs deep copies, grid construction, and in-place slice replacement.",
        "recapRows": [
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
        "solidifiedConcepts": [
            "Shallow Copying Mechanics",
            "copy.deepcopy() Usage",
            "Slice Assignment In-Place",
            "The [[0]*C]*R Reference Trap"
        ],
        "nextDayPreview": {
            "dayNumber": 13,
            "title": "List Comprehensions & Expressions",
            "description": "Transform data expressively and efficiently using list comprehensions and conditional filters."
        }
    }
]
},
  13: {
  "dayNumber": 13,
  "title": "List Comprehensions & Expressions",
  "topicName": "List Comprehensions",
  "sectionId": "python-core",
  "estimatedMinutes": 25,
  "difficulty": "FOUNDATIONAL",
  "prerequisites": [
    12
  ],
  "concepts": [
    "List Comprehensions",
    "Filtering Syntax",
    "Nested Comprehensions",
    "Bytecode Speed"
  ],
  "practiceSkills": [
    "Comprehension Construction",
    "Multi-Condition Filtering",
    "Matrix Flattening"
  ]
,
  "steps": [
    {
        "id": "day13-step1",
        "stepNumber": 1,
        "title": "Comprehension Syntax & Performance",
        "shortLabel": "Comprehension Syntax",
        "type": "explanation",
        "isGated": false,
        "heading": "Expressive Transformation: [expr for item in iterable if condition]",
        "subheading": "Why list comprehensions are faster and more idiomatic than explicit append loops.",
        "markdownContent": [
            "A list comprehension constructs a new list by applying an expression to each item in an iterable, with optional filtering: `[expr for item in iterable if condition]`.",
            "List comprehensions are not just syntactic sugar: at the CPython bytecode level, they execute via a dedicated `LIST_APPEND` instruction inside an optimized loop frame, running ~20-30% faster than manual `for` loops with `.append()`.",
            "Multiple `if` conditions act as logical `and` filters: `[x for x in nums if x > 0 if x % 2 == 0]`."
        ],
        "snippets": [
            {
                "title": "Comprehensions vs for loops",
                "code": "# Manual loop:\nevens = []\nfor x in range(10):\n    if x % 2 == 0:\n        evens.append(x * x)\n\n# Pythonic Comprehension (faster & cleaner):\nevens_comp = [x * x for x in range(10) if x % 2 == 0]",
                "language": "python",
                "caption": "Concise and fast transformation with list comprehensions."
            }
        ],
        "callouts": [
            {
                "type": "tip",
                "title": "Bytecode Efficiency",
                "content": "List comprehensions bypass Python-level attribute lookups (`.append`) by calling CPython's internal list-resizing macro directly."
            }
        ],
        "keyTakeaway": "List comprehensions run faster than append loops and provide declarative data transformations."
    },
    {
        "id": "day13-step2",
        "stepNumber": 2,
        "title": "Nested Comprehensions & Flattening",
        "shortLabel": "Nested Comprehensions",
        "type": "explanation",
        "isGated": false,
        "heading": "Matrix Flattening and Multi-Loop Comprehensions",
        "subheading": "Master the reading order of nested comprehensions: outer loops come first.",
        "markdownContent": [
            "When writing nested comprehensions, the `for` clauses appear in the exact same order as nested loops:",
            "```python\n# Flattening a 2D matrix:\nflattened = [val for row in matrix for val in row]\n```",
            "Notice the order: first `for row in matrix`, then `for val in row`.",
            "For conditional transformations, place `if-else` before the `for`: `[x if x > 0 else 0 for x in nums]` (ternary expression)."
        ],
        "snippets": [
            {
                "title": "Nested Comprehensions and Ternary Placements",
                "code": "matrix = [[1, 2], [3, 4], [5, 6]]\nflat = [x for row in matrix for x in row] # [1, 2, 3, 4, 5, 6]\n\n# Ternary transformation:\nclamped = [x if x >= 0 else 0 for x in [-2, 5, -1, 8]] # [0, 5, 0, 8]",
                "language": "python",
                "caption": "Loop order matches nested indentation order."
            }
        ],
        "callouts": [
            {
                "type": "warning",
                "title": "Readability Rule",
                "content": "Do not nest more than two loops inside a single comprehension. Deeply nested comprehensions hurt readability; use normal loops instead."
            }
        ],
        "keyTakeaway": "In nested comprehensions, outer loops come first; ternary if-else goes before the for clause."
    },
    {
        "id": "day13-step3",
        "stepNumber": 3,
        "title": "Comprehensions Checkpoint",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Test Your Mastery of Comprehensions",
        "subheading": "Verify comprehension syntax, ordering, and filtering.",
        "checkpoints": [
            {
                "id": "chk-d13-q1",
                "question": "What is the result of `[x * 2 for x in [1, 2, 3] if x > 1]`?",
                "options": [
                    {
                        "id": "A",
                        "label": "[2, 4, 6]"
                    },
                    {
                        "id": "B",
                        "label": "[4, 6]"
                    },
                    {
                        "id": "C",
                        "label": "[2, 3]"
                    },
                    {
                        "id": "D",
                        "label": "[4]"
                    }
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
                    {
                        "id": "A",
                        "label": "At the very end: `[x for x in nums if cond else val]`"
                    },
                    {
                        "id": "B",
                        "label": "At the beginning as the output expression: `[x if cond else val for x in nums]`"
                    },
                    {
                        "id": "C",
                        "label": "Ternary expressions are illegal in comprehensions"
                    },
                    {
                        "id": "D",
                        "label": "Inside parentheses after `in`"
                    }
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
        "keyTakeaway": "Filtering conditions go at the end; transformation ternaries go at the beginning."
    },
    {
        "id": "day13-step4",
        "stepNumber": 4,
        "title": "Matrix Transformation Challenge",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Extract and Square Positive Numbers from Matrix",
        "subheading": "Write a nested comprehension to process a 2D matrix.",
        "task": {
            "title": "Matrix Positive Squarer",
            "instructions": [
                "Given `matrix = [[-2, 3, -1], [4, -5, 6], [0, 7, -8]]`.",
                "Write a single list comprehension that flattens the matrix, filters only positive numbers (`> 0`), and squares them.",
                "Assign the result to `positive_squares`.",
                "Print `'Positive squares:', positive_squares`."
            ],
            "starterCode": "# Day 13 Practice: Matrix Positive Squarer\nmatrix = [[-2, 3, -1], [4, -5, 6], [0, 7, -8]]\n\n# TODO: Single list comprehension to extract, filter (> 0), and square positive numbers\npositive_squares = []\n\nprint(\"Positive squares:\", positive_squares)\n",
            "solutionCode": "matrix = [[-2, 3, -1], [4, -5, 6], [0, 7, -8]]\n\npositive_squares = [x * x for row in matrix for x in row if x > 0]\n\nprint(\"Positive squares:\", positive_squares)\n",
            "expectedOutputPatterns": [
                "Positive squares: [9, 16, 36, 49]"
            ],
            "hint": "Use `[x * x for row in matrix for x in row if x > 0]`."
        },
        "keyTakeaway": "Nested comprehensions combine flattening, filtering, and transformation into a single clean pass."
    },
    {
        "id": "day13-step5",
        "stepNumber": 5,
        "title": "List Comprehensions Mastery",
        "shortLabel": "Recap",
        "type": "completion",
        "isGated": false,
        "dayNumber": 13,
        "heading": "Day 13 Complete: List Comprehensions & Expressions",
        "subheading": "You have mastered declarative list creation, bytecode optimization, and nested loops.",
        "recapRows": [
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
        "solidifiedConcepts": [
            "[expr for x in seq if cond]",
            "CPython LIST_APPEND Optimization",
            "Nested Comprehension Order",
            "Ternary Output Transformations"
        ],
        "nextDayPreview": {
            "dayNumber": 14,
            "title": "Tuples, Immutability & The Tuple Swap Idiom",
            "description": "Understand tuple immutability, memory savings over lists, unpacking idioms, and using tuples as hashable coordinate keys."
        }
    }
]
},
  14: {
  "dayNumber": 14,
  "title": "Tuples & Immutability Guarantees",
  "topicName": "Tuples & Immutability",
  "sectionId": "python-core",
  "estimatedMinutes": 25,
  "difficulty": "FOUNDATIONAL",
  "prerequisites": [
    13
  ],
  "concepts": [
    "Tuple Packing/Unpacking",
    "Hashability",
    "namedtuple",
    "Memory Footprint"
  ],
  "practiceSkills": [
    "Tuple Unpacking",
    "Hashable Key Creation",
    "Memory Efficiency Evaluation"
  ]
,
  "steps": [
    {
        "id": "day14-step1",
        "stepNumber": 1,
        "title": "Tuples vs Lists: Immutability & Memory",
        "shortLabel": "Tuples vs Lists",
        "type": "explanation",
        "isGated": false,
        "heading": "Why Tuples Exist: Immutability, Hashability, and Overhead",
        "subheading": "Understand why tuples are lighter, faster, and hashable.",
        "markdownContent": [
            "A `tuple` is an ordered, immutable sequence. Unlike lists, once a tuple is created, its length and pointer slots cannot be changed.",
            "Because tuples have fixed lengths, CPython allocates exact memory with zero over-allocation headroom, making tuples ~20-30% smaller in bytes than lists of the same length.",
            "Crucially, because tuples are immutable, a tuple containing only immutable elements is **hashable**! This means tuples can be used as **keys in dictionaries** and **elements in sets**, whereas lists can never be dictionary keys."
        ],
        "snippets": [
            {
                "title": "Tuples as Dictionary Keys",
                "code": "# 2D Grid coordinates as dictionary keys\ngrid_cache = {}\ngrid_cache[(0, 1)] = 'Right'\ngrid_cache[(1, 0)] = 'Down'\n\n# grid_cache[[0, 1]] = 'Error' # TypeError: unhashable type: 'list'",
                "language": "python",
                "caption": "Tuples serve as hashable composite keys for graphs and grids."
            }
        ],
        "callouts": [
            {
                "type": "tip",
                "title": "Single-Element Tuple Syntax",
                "content": "A single-element tuple requires a trailing comma: `(42,)`. Writing `(42)` is just a parenthesized integer!"
            }
        ],
        "keyTakeaway": "Tuples are immutable, memory-efficient, and hashable if their elements are hashable."
    },
    {
        "id": "day14-step2",
        "stepNumber": 2,
        "title": "Tuple Packing, Unpacking & namedtuple",
        "shortLabel": "Unpacking & namedtuple",
        "type": "explanation",
        "isGated": false,
        "heading": "Extended Unpacking with Asterisk and Lightweight Structs",
        "subheading": "Unpack sequences cleanly and define structured records.",
        "markdownContent": [
            "Tuple unpacking binds sequence elements directly to variables: `a, b = (10, 20)`.",
            "Extended iterable unpacking uses `*rest` to capture arbitrary middle or tail elements: `first, *middle, last = [1, 2, 3, 4, 5]`.",
            "`collections.namedtuple` creates tuple subclasses with named fields, combining the lightweight memory of tuples with attribute access (`point.x`, `point.y`)."
        ],
        "snippets": [
            {
                "title": "Extended Unpacking and namedtuple",
                "code": "from collections import namedtuple\n\n# Extended unpacking\nhead, *tail = [10, 20, 30, 40]\nprint(head) # 10\nprint(tail) # [20, 30, 40]\n\n# namedtuple\nPoint = namedtuple('Point', ['x', 'y'])\np = Point(3, 4)\nprint(p.x, p.y) # 3 4",
                "language": "python",
                "caption": "Clean unpacking and namedtuple records."
            }
        ],
        "callouts": [
            {
                "type": "warning",
                "title": "Tuple Containing Mutable Child",
                "content": "If a tuple contains a mutable object like `t = ([1, 2], 3)`, `t` is NOT hashable! Immutability of the container does not make mutable children hashable."
            }
        ],
        "keyTakeaway": "Tuples support extended unpacking (*rest) and namedtuple provides readable lightweight structs."
    },
    {
        "id": "day14-step3",
        "stepNumber": 3,
        "title": "Tuples & Hashability Checkpoint",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Test Your Understanding of Tuples and Hashability",
        "subheading": "Verify tuple creation, hashability rules, and unpacking.",
        "checkpoints": [
            {
                "id": "chk-d14-q1",
                "question": "Which of the following tuples CAN be used as a dictionary key?",
                "options": [
                    {
                        "id": "A",
                        "label": "(1, 'alpha', [2, 3])"
                    },
                    {
                        "id": "B",
                        "label": "(1, 'alpha', (2, 3))"
                    },
                    {
                        "id": "C",
                        "label": "(1, 'alpha', {'key': 4})"
                    },
                    {
                        "id": "D",
                        "label": "None of them, because tuples cannot be dict keys"
                    }
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
                    {
                        "id": "A",
                        "label": "Both are tuples"
                    },
                    {
                        "id": "B",
                        "label": "x is int, y is tuple"
                    },
                    {
                        "id": "C",
                        "label": "x is tuple, y is syntax error"
                    },
                    {
                        "id": "D",
                        "label": "Both are ints"
                    }
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
        "keyTakeaway": "A tuple is hashable only if all its elements are hashable; 1-tuples require a trailing comma."
    },
    {
        "id": "day14-step4",
        "stepNumber": 4,
        "title": "Grid Coordinate Distance Calculator",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Coordinate Lookup and Distance Cache",
        "subheading": "Use tuples as hashable keys in a geometric memoization cache.",
        "task": {
            "title": "Coordinate Distance Cache",
            "instructions": [
                "Given coordinate pairs `points = [((0, 0), (3, 4)), ((1, 1), (4, 5))]`.",
                "For each pair `(p1, p2)`, compute Manhattan distance: `abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])`.",
                "Store the distance in `dist_cache` using `(p1, p2)` as the dictionary key.",
                "Print `'Cache entries:', len(dist_cache)` and `'Origin to target distance:', dist_cache[((0, 0), (3, 4))]`."
            ],
            "starterCode": "# Day 14 Practice: Coordinate Distance Cache\npoints = [((0, 0), (3, 4)), ((1, 1), (4, 5))]\n\ndist_cache = {}\n\n# TODO: Compute Manhattan distance for each pair and cache in dist_cache\nfor p1, p2 in points:\n    # Compute dist = abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])\n    # Store in dist_cache[(p1, p2)] = dist\n    pass\n\nprint(\"Cache entries:\", len(dist_cache))\nprint(\"Origin to target distance:\", dist_cache[((0, 0), (3, 4))])\n",
            "solutionCode": "points = [((0, 0), (3, 4)), ((1, 1), (4, 5))]\n\ndist_cache = {}\nfor p1, p2 in points:\n    dist = abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])\n    dist_cache[(p1, p2)] = dist\n\nprint(\"Cache entries:\", len(dist_cache))\nprint(\"Origin to target distance:\", dist_cache[((0, 0), (3, 4))])\n",
            "expectedOutputPatterns": [
                "Cache entries: 2",
                "Origin to target distance: 7"
            ],
            "hint": "Calculate `dist = abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])` and assign to `dist_cache[(p1, p2)]`."
        },
        "keyTakeaway": "Nested immutable tuples form hashable composite keys ideal for geometric and graph caches."
    },
    {
        "id": "day14-step5",
        "stepNumber": 5,
        "title": "Tuples & Immutability Mastery",
        "shortLabel": "Recap",
        "type": "completion",
        "isGated": false,
        "dayNumber": 14,
        "heading": "Day 14 Complete: Tuples & Immutability Guarantees",
        "subheading": "You have mastered tuple memory compactness, hashability prerequisites, and unpacking.",
        "recapRows": [
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
        "solidifiedConcepts": [
            "Tuple Memory Compactness",
            "Hashable Dictionary Keys",
            "Extended Unpacking (*rest)",
            "namedtuple Lightweight Structs"
        ],
        "nextDayPreview": {
            "dayNumber": 15,
            "title": "Dictionaries: Compact Hash Table Internals",
            "description": "Explore CPython's compact dictionary architecture, hash functions, open-addressing collision resolution, and average O(1) lookups."
        }
    }
]
},
  15: {
  "dayNumber": 15,
  "title": "Dictionaries: Hash Map Internals",
  "topicName": "Hash Tables & Dicts",
  "sectionId": "python-core",
  "estimatedMinutes": 30,
  "difficulty": "FOUNDATIONAL",
  "prerequisites": [
    14
  ],
  "concepts": [
    "Compact Dict Layout",
    "Hash Function __hash__",
    "Collision Probing",
    "O(1) Average Lookup"
  ],
  "practiceSkills": [
    "Dictionary Key Hashing",
    "Collision Resolution Understanding",
    "Key Mutability Safety"
  ]
,
  "steps": [
    {
        "id": "day15-step1",
        "stepNumber": 1,
        "title": "CPython's Compact Dict Architecture",
        "shortLabel": "Dict Memory Layout",
        "type": "explanation",
        "isGated": false,
        "heading": "How Python Achieves O(1) Average Lookup with Insertion-Ordered Compact Tables",
        "subheading": "Explore the internal sparse index table and compact entries array introduced in Python 3.6.",
        "markdownContent": [
            "In Python 3.6+, dictionaries are **insertion-ordered** and memory-compact. Internally, a dictionary consists of two arrays:",
            "1. A **sparse hash table (indices array)** storing small integer indices or `-1` (empty).",
            "2. A **dense entries array** storing `[hash, key_pointer, value_pointer]` in the exact order keys were inserted.",
            "When looking up `d[key]`, Python computes `h = hash(key)`. It computes index `idx = h & (size - 1)` into the sparse table to find the entry slot.",
            "If two distinct keys hash to the same slot (a **collision**), Python resolves it using **open addressing with perturb-based probing** until an empty slot or the matching key is found."
        ],
        "snippets": [
            {
                "title": "Hashing and Object Identity",
                "code": "key1 = 'name'\nkey2 = 'name'\nprint(hash(key1) == hash(key2)) # True\n\n# Dict preserves insertion order\nd = {'z': 1, 'a': 2, 'm': 3}\nprint(list(d.keys())) # ['z', 'a', 'm']",
                "language": "python",
                "caption": "Consistent hashing and guaranteed insertion order."
            }
        ],
        "callouts": [
            {
                "type": "tip",
                "title": "What Makes a Key Valid?",
                "content": "A dictionary key must be **hashable**: it must implement `__hash__()` and `__eq__()`, and its hash value must never change during its lifetime. Mutable types (lists, dicts, sets) are unhashable."
            }
        ],
        "keyTakeaway": "CPython compact dicts combine sparse index arrays with dense entry tables for O(1) lookup and order preservation."
    },
    {
        "id": "day15-step2",
        "stepNumber": 2,
        "title": "Hash Collisions & Amortized O(1)",
        "shortLabel": "Collisions & Probing",
        "type": "explanation",
        "isGated": false,
        "heading": "Collision Probing and Worst-Case O(N) Degradation",
        "subheading": "Why hash lookups are O(1) average but can degrade under adversarial collisions.",
        "markdownContent": [
            "Because the universe of possible strings and numbers is infinite while the hash table size is finite, hash collisions are mathematically inevitable (by the Pigeonhole Principle).",
            "When a collision occurs, Python computes a new probe offset: `idx = (5 * idx + 1 + perturb) & mask`. This pseudo-random walk visits every table slot without clustering.",
            "When the table becomes ~66% full (load factor threshold 2/3), Python doubles table capacity to minimize collision chains.",
            "While average lookup is $O(1)$, adversarial input causing all keys to collide degrades lookup to $O(N)$."
        ],
        "snippets": [
            {
                "title": "Safe Lookup with .get() and in",
                "code": "counts = {'a': 10, 'b': 20}\n# O(1) membership check\nif 'c' in counts:\n    print(counts['c'])\n\n# O(1) safe retrieval with default\nprint(counts.get('c', 0)) # 0 (does not raise KeyError)",
                "language": "python",
                "caption": "Testing keys and defaulting safely."
            }
        ],
        "callouts": [
            {
                "type": "warning",
                "title": "Never Mutate a Key After Insertion",
                "content": "If you use a custom object whose attributes change after being placed in a dict, its hash or equality might change, making the key permanently lost inside the table!"
            }
        ],
        "keyTakeaway": "Hash collisions are resolved via open addressing; tables resize at 2/3 load factor to maintain O(1) lookups."
    },
    {
        "id": "day15-step3",
        "stepNumber": 3,
        "title": "Dict Internals Checkpoint",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Test Your Mastery of Hash Tables and Key Constraints",
        "subheading": "Verify key requirements and complexity realities.",
        "checkpoints": [
            {
                "id": "chk-d15-q1",
                "question": "Which object CANNOT be used as a dictionary key?",
                "options": [
                    {
                        "id": "A",
                        "label": "frozenset([1, 2, 3])"
                    },
                    {
                        "id": "B",
                        "label": "(1, 2, 'hello')"
                    },
                    {
                        "id": "C",
                        "label": "[1, 2, 3]"
                    },
                    {
                        "id": "D",
                        "label": "42"
                    }
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
                    {
                        "id": "A",
                        "label": "O(log N)"
                    },
                    {
                        "id": "B",
                        "label": "O(1)"
                    },
                    {
                        "id": "C",
                        "label": "O(N)"
                    },
                    {
                        "id": "D",
                        "label": "O(N log N)"
                    }
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
        "keyTakeaway": "Only hashable immutable types can be dictionary keys; average lookup is O(1)."
    },
    {
        "id": "day15-step4",
        "stepNumber": 4,
        "title": "Build a Frequency Counter",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Tally Character Frequencies Manually",
        "subheading": "Implement a character tally using dictionary lookups and .get().",
        "task": {
            "title": "Frequency Map Builder",
            "instructions": [
                "Given string `text = 'abracadabra'`.",
                "Iterate over each character `ch` in `text`.",
                "Use `freq[ch] = freq.get(ch, 0) + 1` to record the count.",
                "Print the count for `'a'` and `'r'`."
            ],
            "starterCode": "# Day 15 Practice: Frequency Map Builder\ntext = \"abracadabra\"\n\nfreq = {}\n\n# TODO: Count frequency of each character using .get(ch, 0)\nfor ch in text:\n    pass\n\nprint(\"Count of a:\", freq.get(\"a\", 0))\nprint(\"Count of r:\", freq.get(\"r\", 0))\n",
            "solutionCode": "text = \"abracadabra\"\n\nfreq = {}\nfor ch in text:\n    freq[ch] = freq.get(ch, 0) + 1\n\nprint(\"Count of a:\", freq.get(\"a\", 0))\nprint(\"Count of r:\", freq.get(\"r\", 0))\n",
            "expectedOutputPatterns": [
                "Count of a: 5",
                "Count of r: 2"
            ],
            "hint": "Use `freq[ch] = freq.get(ch, 0) + 1` inside the loop."
        },
        "keyTakeaway": "The .get(key, default) method provides clean, KeyError-free dictionary accumulation."
    },
    {
        "id": "day15-step5",
        "stepNumber": 5,
        "title": "Dictionary Internals Mastery",
        "shortLabel": "Recap",
        "type": "completion",
        "isGated": false,
        "dayNumber": 15,
        "heading": "Day 15 Complete: Dictionaries: Hash Map Internals",
        "subheading": "You have mastered compact dictionary memory layout, open addressing, and key hashability rules.",
        "recapRows": [
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
        "solidifiedConcepts": [
            "Compact Dict Architecture",
            "Hash Collisions & Probing",
            "Hashability Contract",
            ".get(key, default) Pattern"
        ],
        "nextDayPreview": {
            "dayNumber": 16,
            "title": "Dictionary Methods, Views & Aggregation",
            "description": "Apply get(), setdefault(), dictionary views (.keys(), .values(), .items()), and modern dictionary merging."
        }
    }
]
},
  16: {
  "dayNumber": 16,
  "title": "Dictionary Methods & Patterns",
  "topicName": "Dictionary Patterns",
  "sectionId": "python-core",
  "estimatedMinutes": 30,
  "difficulty": "FOUNDATIONAL",
  "prerequisites": [
    15
  ],
  "concepts": [
    "setdefault & get",
    "Dict Comprehensions",
    "Dictionary Views",
    "Dict Merging ( | )"
  ],
  "practiceSkills": [
    "setdefault Accumulation",
    "Dict Comprehensions",
    "Dynamic Key Merging"
  ]
,
  "steps": [
    {
        "id": "day16-step1",
        "stepNumber": 1,
        "title": "setdefault & Dictionary Views",
        "shortLabel": "setdefault & Views",
        "type": "explanation",
        "isGated": false,
        "heading": "Accumulating Groups with setdefault and Dynamic Dict Views",
        "subheading": "Group items cleanly and inspect dynamic dictionary views.",
        "markdownContent": [
            "`dict.setdefault(key, default)` returns the value if `key` is in the dict; if not, it inserts `key` with `default` and returns `default`.",
            "This is ideal for grouping items into lists: `groups.setdefault(category, []).append(item)`.",
            "Methods `.keys()`, `.values()`, and `.items()` return **dictionary views**. Views do not allocate new lists; they provide dynamic, live windows into the dictionary's internal entries that reflect additions or deletions immediately.",
            "Dictionary keys views support set-like operations (`&`, `|`, `-`): `d1.keys() & d2.keys()` computes common keys in $O(\\min(N, M))$ time."
        ],
        "snippets": [
            {
                "title": "Grouping with setdefault and View Intersections",
                "code": "groups = {}\nfor word in ['cat', 'car', 'apple', 'dog']:\n    groups.setdefault(word[0], []).append(word)\nprint(groups) # {'c': ['cat', 'car'], 'a': ['apple'], 'd': ['dog']}\n\n# Set operations on dict views\nd1 = {'a': 1, 'b': 2}\nd2 = {'b': 20, 'c': 30}\nprint(d1.keys() & d2.keys()) # {'b'}",
                "language": "python",
                "caption": "Live views and grouping patterns."
            }
        ],
        "callouts": [
            {
                "type": "tip",
                "title": "Dict Merge Operator (|)",
                "content": "In Python 3.9+, you can merge dictionaries cleanly with `merged = d1 | d2`. Values in `d2` overwrite keys in `d1`."
            }
        ],
        "keyTakeaway": "setdefault groups values into containers in one line; dict views support set operations."
    },
    {
        "id": "day16-step2",
        "stepNumber": 2,
        "title": "Dict Comprehensions & Inversion",
        "shortLabel": "Dict Comprehensions",
        "type": "explanation",
        "isGated": false,
        "heading": "Constructing and Inverting Dictionaries Elegantly",
        "subheading": "Master `{k_expr: v_expr for item in iterable}` transformations.",
        "markdownContent": [
            "Dict comprehensions create dictionaries concisely: `{k: v for k, v in iterable}`.",
            "A classic pattern is **dictionary inversion** (swapping keys and values): `{v: k for k, v in original.items()}`, assuming values are unique and hashable.",
            "Comprehensions also support conditional filtering: `{k: v for k, v in scores.items() if v >= 60}`."
        ],
        "snippets": [
            {
                "title": "Inverting a Dictionary",
                "code": "code_to_char = {65: 'A', 66: 'B', 67: 'C'}\nchar_to_code = {char: code for code, char in code_to_char.items()}\nprint(char_to_code) # {'A': 65, 'B': 66, 'C': 67}",
                "language": "python",
                "caption": "Inverting lookups with dict comprehensions."
            }
        ],
        "callouts": [
            {
                "type": "warning",
                "title": "Duplicate Values Overwrite",
                "content": "When inverting `{ 'a': 1, 'b': 1 }`, the second item overwrites the first (`{ 1: 'b' }`). Use lists for multi-value inversions."
            }
        ],
        "keyTakeaway": "Dict comprehensions allow elegant filtering, mapping, and key-value inversion."
    },
    {
        "id": "day16-step3",
        "stepNumber": 3,
        "title": "Dict Patterns Checkpoint",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Test Your Mastery of setdefault and Comprehensions",
        "subheading": "Diagnose dictionary operations and merging.",
        "checkpoints": [
            {
                "id": "chk-d16-q1",
                "question": "What does `d.setdefault('items', []).append(10)` do if 'items' already exists with value `[1, 2]`?",
                "options": [
                    {
                        "id": "A",
                        "label": "Overwrites 'items' with [10]"
                    },
                    {
                        "id": "B",
                        "label": "Raises KeyError"
                    },
                    {
                        "id": "C",
                        "label": "Appends 10 to the existing list, making it [1, 2, 10]"
                    },
                    {
                        "id": "D",
                        "label": "Creates a new copy of the list"
                    }
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
                    {
                        "id": "A",
                        "label": "{'a': 1, 'b': 2, 'c': 3}"
                    },
                    {
                        "id": "B",
                        "label": "{'a': 1, 'b': 99, 'c': 3}"
                    },
                    {
                        "id": "C",
                        "label": "TypeError: unsupported operand type"
                    },
                    {
                        "id": "D",
                        "label": "{'b': 99}"
                    }
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
        "keyTakeaway": "setdefault returns existing references without overwriting; `|` merges with right-side precedence."
    },
    {
        "id": "day16-step4",
        "stepNumber": 4,
        "title": "Group Anagrams Preview",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Group Words by Length Using setdefault",
        "subheading": "Implement word length bucketing using setdefault.",
        "task": {
            "title": "Word Length Bucket Aggregator",
            "instructions": [
                "Given `words = ['code', 'py', 'algo', 'mentor', 'ds', 'tree']`.",
                "Group words by their length (`len(word)`) into `buckets` using `setdefault`.",
                "Print the bucket for length 4 and length 2."
            ],
            "starterCode": "# Day 16 Practice: Word Length Bucket Aggregator\nwords = [\"code\", \"py\", \"algo\", \"mentor\", \"ds\", \"tree\"]\n\nbuckets = {}\n\n# TODO: Group each word into buckets[len(word)] using setdefault\nfor w in words:\n    pass\n\nprint(\"Length 4 words:\", buckets.get(4))\nprint(\"Length 2 words:\", buckets.get(2))\n",
            "solutionCode": "words = [\"code\", \"py\", \"algo\", \"mentor\", \"ds\", \"tree\"]\n\nbuckets = {}\nfor w in words:\n    buckets.setdefault(len(w), []).append(w)\n\nprint(\"Length 4 words:\", buckets.get(4))\nprint(\"Length 2 words:\", buckets.get(2))\n",
            "expectedOutputPatterns": [
                "Length 4 words: ['code', 'algo', 'tree']",
                "Length 2 words: ['py', 'ds']"
            ],
            "hint": "Use `buckets.setdefault(len(w), []).append(w)`."
        },
        "keyTakeaway": "setdefault streamlines grouping patterns across algorithms without nested if-checks."
    },
    {
        "id": "day16-step5",
        "stepNumber": 5,
        "title": "Dict Methods & Patterns Mastery",
        "shortLabel": "Recap",
        "type": "completion",
        "isGated": false,
        "dayNumber": 16,
        "heading": "Day 16 Complete: Dictionary Methods & Patterns",
        "subheading": "You have mastered setdefault grouping, dictionary views, and union operators.",
        "recapRows": [
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
        "solidifiedConcepts": [
            "setdefault Accumulation Pattern",
            "Dictionary Views & Set Operations",
            "Dict Comprehensions",
            "Merge Operator (|)"
        ],
        "nextDayPreview": {
            "dayNumber": 17,
            "title": "Sets: Value-Free Hash Tables & O(1) Lookups",
            "description": "Use sets for O(1) membership testing, deduplication, set algebra, and understand the immutable frozenset."
        }
    }
]
},
  17: {
  "dayNumber": 17,
  "title": "Sets: Set Theory & Operations",
  "topicName": "Set Theory & Invariants",
  "sectionId": "python-core",
  "estimatedMinutes": 30,
  "difficulty": "FOUNDATIONAL",
  "prerequisites": [
    16
  ],
  "concepts": [
    "Set Theory Operations",
    "frozenset",
    "O(1) Membership",
    "Deduplication"
  ],
  "practiceSkills": [
    "Set Operations (&, |, -, ^)",
    "O(1) Membership Testing",
    "Deduplication Invariants"
  ]
,
  "steps": [
    {
        "id": "day17-step1",
        "stepNumber": 1,
        "title": "Set Architecture & O(1) Membership",
        "shortLabel": "Set Architecture",
        "type": "explanation",
        "isGated": false,
        "heading": "Sets as Value-Free Hash Maps with O(1) Membership Testing",
        "subheading": "How Python sets achieve instantaneous lookups and automatic uniqueness.",
        "markdownContent": [
            "A `set` in Python is an unordered collection of unique, hashable elements. Under the hood, a set is implemented as a hash table with entry keys but no values.",
            "Because sets use hashing, testing membership (`x in my_set`) takes **$O(1)$ average time**, compared to **$O(N)$** for lists!",
            "In algorithmic problems, checking `if x in list` inside a loop degrades performance to $O(N^2)$. Converting the collection to a `set` drops total time to $O(N)$."
        ],
        "snippets": [
            {
                "title": "O(1) Membership vs O(N) List Lookup",
                "code": "# Slow O(N) list search\nseen_list = [1, 2, 3, 4]\nprint(3 in seen_list) # O(N) scan\n\n# Fast O(1) set lookup\nseen_set = {1, 2, 3, 4}\nprint(3 in seen_set)  # O(1) hash lookup",
                "language": "python",
                "caption": "Replacing lists with sets for instant membership checks."
            }
        ],
        "callouts": [
            {
                "type": "tip",
                "title": "Creating an Empty Set",
                "content": "To create an empty set, you MUST write `s = set()`. Writing `s = {}` creates an empty **dictionary**!"
            }
        ],
        "keyTakeaway": "Sets provide O(1) average membership checks; empty sets must be initialized with set()."
    },
    {
        "id": "day17-step2",
        "stepNumber": 2,
        "title": "Mathematical Set Operations & frozenset",
        "shortLabel": "Set Operations",
        "type": "explanation",
        "isGated": false,
        "heading": "Union, Intersection, Difference, Symmetric Difference, and frozenset",
        "subheading": "Expressive mathematical logic using set operators.",
        "markdownContent": [
            "Python sets support high-speed C-level mathematical operations:",
            "- **Union (`a | b`)**: Elements in either `a` or `b`.",
            "- **Intersection (`a & b`)**: Elements in both `a` and `b`.",
            "- **Difference (`a - b`)**: Elements in `a` but not in `b`.",
            "- **Symmetric Difference (`a ^ b`)**: Elements in either `a` or `b`, but not both.",
            "A standard `set` is mutable and therefore unhashable. A `frozenset` is an immutable set that can be used as a dictionary key or placed inside another set."
        ],
        "snippets": [
            {
                "title": "Mathematical Set Operations",
                "code": "frontend = {'HTML', 'CSS', 'JavaScript', 'React'}\nbackend = {'Python', 'SQL', 'JavaScript', 'Docker'}\n\n# Common skills (Intersection)\nprint('Common:', frontend & backend) # {'JavaScript'}\n\n# Frontend only (Difference)\nprint('Frontend only:', frontend - backend) # {'HTML', 'CSS', 'React'}",
                "language": "python",
                "caption": "Set theory operators in action."
            }
        ],
        "callouts": [
            {
                "type": "warning",
                "title": "Sets Do Not Preserve Order",
                "content": "Do not rely on element order in sets! Iterating over a set produces elements in arbitrary hash table order."
            }
        ],
        "keyTakeaway": "Set operators (&, |, -, ^) execute in O(min(len(a), len(b))) time; frozenset is immutable and hashable."
    },
    {
        "id": "day17-step3",
        "stepNumber": 3,
        "title": "Sets Checkpoint",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Test Your Mastery of Set Invariants",
        "subheading": "Evaluate membership complexity, syntax, and operations.",
        "checkpoints": [
            {
                "id": "chk-d17-q1",
                "question": "What is the type of `obj = {}`?",
                "options": [
                    {
                        "id": "A",
                        "label": "<class 'set'>"
                    },
                    {
                        "id": "B",
                        "label": "<class 'dict'>"
                    },
                    {
                        "id": "C",
                        "label": "SyntaxError"
                    },
                    {
                        "id": "D",
                        "label": "<class 'frozenset'>"
                    }
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
                    {
                        "id": "A",
                        "label": "O(N)"
                    },
                    {
                        "id": "B",
                        "label": "O(log N)"
                    },
                    {
                        "id": "C",
                        "label": "O(1)"
                    },
                    {
                        "id": "D",
                        "label": "O(N^2)"
                    }
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
        "keyTakeaway": "{} creates a dict, set() creates an empty set; membership testing is O(1)."
    },
    {
        "id": "day17-step4",
        "stepNumber": 4,
        "title": "Unique Visitor Analyzer",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Find Unique and Common Log Visitors",
        "subheading": "Analyze visitor overlap between two servers using set operations.",
        "task": {
            "title": "Server Overlap Analyzer",
            "instructions": [
                "Given `srv1_logs = ['alice', 'bob', 'charlie', 'alice', 'dave']` and `srv2_logs = ['bob', 'dave', 'eve', 'frank']`.",
                "Convert both logs to sets to eliminate duplicates.",
                "Find `common_users` present on both servers using intersection (`&`).",
                "Find `unique_all` present across either server using union (`|`).",
                "Print `'Common users count:', len(common_users)` and `'Total unique visitors:', len(unique_all)`."
            ],
            "starterCode": "# Day 17 Practice: Server Overlap Analyzer\nsrv1_logs = [\"alice\", \"bob\", \"charlie\", \"alice\", \"dave\"]\nsrv2_logs = [\"bob\", \"dave\", \"eve\", \"frank\"]\n\n# TODO 1: Convert to sets\ns1 = set()\ns2 = set()\n\n# TODO 2: Compute common_users (intersection) and unique_all (union)\ncommon_users = set()\nunique_all = set()\n\nprint(\"Common users count:\", len(common_users))\nprint(\"Total unique visitors:\", len(unique_all))\n",
            "solutionCode": "srv1_logs = [\"alice\", \"bob\", \"charlie\", \"alice\", \"dave\"]\nsrv2_logs = [\"bob\", \"dave\", \"eve\", \"frank\"]\n\ns1 = set(srv1_logs)\ns2 = set(srv2_logs)\n\ncommon_users = s1 & s2\nunique_all = s1 | s2\n\nprint(\"Common users count:\", len(common_users))\nprint(\"Total unique visitors:\", len(unique_all))\n",
            "expectedOutputPatterns": [
                "Common users count: 2",
                "Total unique visitors: 6"
            ],
            "hint": "Convert logs with set(srv1_logs), then use s1 & s2 and s1 | s2."
        },
        "keyTakeaway": "Set conversions automatically deduplicate sequences, and bitwise operators execute fast set algebra."
    },
    {
        "id": "day17-step5",
        "stepNumber": 5,
        "title": "Sets & Mathematical Operations Mastery",
        "shortLabel": "Recap",
        "type": "completion",
        "isGated": false,
        "dayNumber": 17,
        "heading": "Day 17 Complete: Sets: Set Theory & Operations",
        "subheading": "You have mastered set hashing, O(1) membership, mathematical operations, and frozenset.",
        "recapRows": [
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
        "solidifiedConcepts": [
            "O(1) Hash Membership Testing",
            "Set Theory Operators (&, |, -, ^)",
            "frozenset Hashable Collections",
            "Deduplication Invariants"
        ],
        "nextDayPreview": {
            "dayNumber": 18,
            "title": "The Collections Module: Deque & Counter",
            "description": "Master collections.deque for O(1) appends and pops on both ends, defaultdict, and Counter."
        }
    }
]
},
  18: {
  "dayNumber": 18,
  "title": "The Collections Module",
  "topicName": "collections Module",
  "sectionId": "python-core",
  "estimatedMinutes": 30,
  "difficulty": "FOUNDATIONAL",
  "prerequisites": [
    17
  ],
  "concepts": [
    "collections.Counter",
    "defaultdict",
    "deque O(1) Pops",
    "OrderedDict"
  ],
  "practiceSkills": [
    "Counter Tallying & most_common",
    "defaultdict Nesting",
    "deque O(1) Push/Pop"
  ]
,
  "steps": [
    {
        "id": "day18-step1",
        "stepNumber": 1,
        "title": "Counter & defaultdict",
        "shortLabel": "Counter & defaultdict",
        "type": "explanation",
        "isGated": false,
        "heading": "Specialized Containers: collections.Counter and defaultdict",
        "subheading": "Eliminate boilerplate counting and grouping code.",
        "markdownContent": [
            "`collections.Counter` is a dictionary subclass designed specifically for counting hashable objects. It initializes frequency tallies instantly: `c = Counter(iterable)`.",
            "Accessing missing keys in a Counter returns `0` instead of raising `KeyError`.",
            "`Counter.most_common(k)` returns the `k` most frequent elements in $O(N \\log k)$ time using an internal heap.",
            "`collections.defaultdict(factory)` automatically calls `factory()` to generate default values whenever a non-existent key is accessed: `defaultdict(list)`, `defaultdict(int)`, `defaultdict(set)`."
        ],
        "snippets": [
            {
                "title": "Counter and defaultdict Usage",
                "code": "from collections import Counter, defaultdict\n\n# Instant frequency tally\ncounts = Counter('banana')\nprint(counts) # Counter({'a': 3, 'n': 2, 'b': 1})\nprint(counts.most_common(1)) # [('a', 3)]\n\n# Auto-grouping without setdefault boilerplate\ngroups = defaultdict(list)\ngroups['fruits'].append('apple')",
                "language": "python",
                "caption": "Zero-boilerplate counting and auto-initializing groups."
            }
        ],
        "callouts": [
            {
                "type": "tip",
                "title": "most_common(K) Performance",
                "content": "`Counter.most_common(k)` uses `heapq.nlargest` under the hood, running in $O(N \\log k)$ time without sorting the entire dictionary."
            }
        ],
        "keyTakeaway": "Counter tallies frequencies instantly; defaultdict creates missing keys automatically using a factory callable."
    },
    {
        "id": "day18-step2",
        "stepNumber": 2,
        "title": "deque: Double-Ended Queue",
        "shortLabel": "deque & O(1) Pops",
        "type": "explanation",
        "isGated": false,
        "heading": "Why collections.deque is Essential for Breadth-First Search (BFS) and Queues",
        "subheading": "Achieve true O(1) appends and pops from both ends.",
        "markdownContent": [
            "Python's `list` is a contiguous dynamic array, making `list.pop(0)` an $O(N)$ operation that shifts all elements.",
            "`collections.deque` (double-ended queue) is implemented as a **doubly linked list of fixed-size blocks (chunks of 64 elements)**.",
            "This architecture guarantees **$O(1)$ worst-case time complexity** for: `append()`, `appendleft()`, `pop()`, and `popleft()`!",
            "Every queue, BFS algorithm, and sliding window buffer in Python MUST use `deque` rather than a standard `list`."
        ],
        "snippets": [
            {
                "title": "deque Operations",
                "code": "from collections import deque\n\nq = deque([1, 2, 3])\nq.append(4)       # O(1) - push to right\nq.appendleft(0)   # O(1) - push to left\nfirst = q.popleft() # O(1) - pop from left (vital for BFS!)\nlast = q.pop()       # O(1) - pop from right\nprint('Queue remaining:', q) # deque([1, 2, 3])",
                "language": "python",
                "caption": "O(1) double-ended queue operations."
            }
        ],
        "callouts": [
            {
                "type": "warning",
                "title": "deque Random Access is O(N)",
                "content": "While `deque` is $O(1)$ at both ends, indexing in the middle (`q[N//2]`) is $O(N)$! Use a list if you need fast random indexing."
            }
        ],
        "keyTakeaway": "deque provides true O(1) appends and pops at both ends, making it mandatory for queues and BFS."
    },
    {
        "id": "day18-step3",
        "stepNumber": 3,
        "title": "Collections Checkpoint",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Test Your Mastery of Specialized Collections",
        "subheading": "Evaluate queue performance and defaultdict behavior.",
        "checkpoints": [
            {
                "id": "chk-d18-q1",
                "question": "Why should you NEVER use `lst.pop(0)` for a queue of N items in algorithmic problems?",
                "options": [
                    {
                        "id": "A",
                        "label": "It mutates the list"
                    },
                    {
                        "id": "B",
                        "label": "It shifts all N-1 elements left in memory, making N pops cost O(N^2) total"
                    },
                    {
                        "id": "C",
                        "label": "It raises IndexError on lists with even length"
                    },
                    {
                        "id": "D",
                        "label": "It converts integers to floats"
                    }
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
                    {
                        "id": "A",
                        "label": "Raises KeyError"
                    },
                    {
                        "id": "B",
                        "label": "Returns None"
                    },
                    {
                        "id": "C",
                        "label": "Returns 0 without raising an error"
                    },
                    {
                        "id": "D",
                        "label": "Inserts 'missing': None"
                    }
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
        "keyTakeaway": "pop(0) on a list is O(N) while deque.popleft() is O(1); Counter returns 0 for missing keys."
    },
    {
        "id": "day18-step4",
        "stepNumber": 4,
        "title": "Top-K Frequent Elements Preview",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Find Most Frequent Words Using Counter",
        "subheading": "Extract the top 2 most common words from a corpus.",
        "task": {
            "title": "Top-K Word Frequency Extractor",
            "instructions": [
                "Given `text = 'apple banana apple orange banana apple grape banana'`.",
                "Split the text into a list of words.",
                "Use `collections.Counter` to tally word frequencies.",
                "Extract the 2 most common words using `.most_common(2)`.",
                "Print `'Top 2 words:', top_words`."
            ],
            "starterCode": "# Day 18 Practice: Top-K Word Frequency Extractor\nfrom collections import Counter\n\ntext = \"apple banana apple orange banana apple grape banana\"\n\n# TODO 1: Split text into words\nwords = text.split()\n\n# TODO 2: Tally with Counter and extract most_common(2)\ncounts = Counter()\ntop_words = []\n\nprint(\"Top 2 words:\", top_words)\n",
            "solutionCode": "from collections import Counter\n\ntext = \"apple banana apple orange banana apple grape banana\"\nwords = text.split()\n\ncounts = Counter(words)\ntop_words = counts.most_common(2)\n\nprint(\"Top 2 words:\", top_words)\n",
            "expectedOutputPatterns": [
                "Top 2 words: [('apple', 3), ('banana', 3)]"
            ],
            "hint": "Initialize `counts = Counter(words)` then call `counts.most_common(2)`."
        },
        "keyTakeaway": "Counter.most_common(k) solves frequency ranking problems efficiently."
    },
    {
        "id": "day18-step5",
        "stepNumber": 5,
        "title": "Collections Module Mastery",
        "shortLabel": "Recap",
        "type": "completion",
        "isGated": false,
        "dayNumber": 18,
        "heading": "Day 18 Complete: The Collections Module",
        "subheading": "You have mastered Counter, defaultdict, and O(1) double-ended queue mechanics.",
        "recapRows": [
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
        "solidifiedConcepts": [
            "collections.Counter & most_common()",
            "defaultdict(factory) Pattern",
            "deque O(1) popleft() Invariant",
            "Avoid list.pop(0) Anti-Pattern"
        ],
        "nextDayPreview": {
            "dayNumber": 19,
            "title": "Iterators & The Iteration Protocol",
            "description": "Understand iterable vs iterator, the __iter__ and __next__ protocols, and consumable stream behavior."
        }
    }
]
},
  19: {
  "dayNumber": 19,
  "title": "Iterators & Iteration Protocol",
  "topicName": "Iteration Protocol",
  "sectionId": "python-core",
  "estimatedMinutes": 30,
  "difficulty": "FOUNDATIONAL",
  "prerequisites": [
    18
  ],
  "concepts": [
    "__iter__ and __next__",
    "StopIteration",
    "Iterable vs Iterator",
    "Sentinel iter()"
  ],
  "practiceSkills": [
    "Custom Iterator Implementation",
    "Iteration State Tracking",
    "StopIteration Termination"
  ]
,
  "steps": [
    {
        "id": "day19-step1",
        "stepNumber": 1,
        "title": "The Iteration Protocol Invariants",
        "shortLabel": "Iteration Protocol",
        "type": "explanation",
        "isGated": false,
        "heading": "How Python Loops Work: The __iter__() and __next__() Protocol",
        "subheading": "Discover the universal contract driving Python's for loops, comprehensions, and unpacking.",
        "markdownContent": [
            "An **Iterable** is any object capable of returning an iterator. It implements `__iter__()`, which returns an iterator object.",
            "An **Iterator** is an object representing a stream of data. It implements:",
            "1. `__iter__()`: Returns `self`.",
            "2. `__next__()`: Returns the next item from the stream. When no elements remain, it MUST raise `StopIteration`.",
            "When you write `for item in collection:`, Python calls `it = iter(collection)`, then repeatedly calls `next(it)` inside a hidden loop until catching `StopIteration`."
        ],
        "snippets": [
            {
                "title": "Manual Simulation of for Loop",
                "code": "items = [10, 20, 30]\n# What Python does behind the scenes:\nit = iter(items) # Calls items.__iter__()\nwhile True:\n    try:\n        val = next(it) # Calls it.__next__()\n        print(val)\n    except StopIteration:\n        break # End of stream reached!",
                "language": "python",
                "caption": "Explicit simulation of Python's iteration protocol."
            }
        ],
        "callouts": [
            {
                "type": "tip",
                "title": "Iterators are Consumable",
                "content": "An iterator is a one-way stateful stream! Once exhausted, calling `next()` continues to raise `StopIteration`. You cannot reset an iterator; you must create a new one."
            }
        ],
        "keyTakeaway": "Iterables implement __iter__; iterators implement __iter__ and stateful __next__, terminating with StopIteration."
    },
    {
        "id": "day19-step2",
        "stepNumber": 2,
        "title": "Building a Custom Iterator Class",
        "shortLabel": "Custom Iterator",
        "type": "explanation",
        "isGated": false,
        "heading": "Implementing State-Preserving Iterators with Bounds",
        "subheading": "Write your own iterator class from scratch.",
        "markdownContent": [
            "To build a custom iterator class:",
            "- Initialize state in `__init__` (e.g. current index or pointer).",
            "- Return `self` in `__iter__()`.",
            "- In `__next__()`, check boundaries. If within range, advance internal state and return the value; if out of range, raise `StopIteration`.",
            "The two-argument form `iter(callable, sentinel)` repeatedly calls `callable()` until it returns `sentinel`, creating an instant iterator from functions."
        ],
        "snippets": [
            {
                "title": "Custom Countdown Iterator",
                "code": "class Countdown:\n    def __init__(self, start):\n        self.current = start\n    def __iter__(self):\n        return self\n    def __next__(self):\n        if self.current <= 0:\n            raise StopIteration\n        val = self.current\n        self.current -= 1\n        return val\n\nfor num in Countdown(3):\n    print(num) # 3, 2, 1",
                "language": "python",
                "caption": "Stateful custom iterator class."
            }
        ],
        "callouts": [
            {
                "type": "deep-dive",
                "title": "Sentinel iter() Pattern",
                "content": "`for block in iter(lambda: f.read(1024), b''):` reads chunks of a file until an empty bytes sentinel is returned."
            }
        ],
        "keyTakeaway": "Custom iterators preserve state between calls to __next__() and signal completion with StopIteration."
    },
    {
        "id": "day19-step3",
        "stepNumber": 3,
        "title": "Iteration Protocol Checkpoint",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Test Your Mastery of the Iteration Protocol",
        "subheading": "Evaluate iterator exhaustion and protocol methods.",
        "checkpoints": [
            {
                "id": "chk-d19-q1",
                "question": "What happens if you run a second `for` loop over an iterator that has already completed?",
                "options": [
                    {
                        "id": "A",
                        "label": "It restarts from the beginning automatically"
                    },
                    {
                        "id": "B",
                        "label": "The second loop does nothing because the iterator is exhausted"
                    },
                    {
                        "id": "C",
                        "label": "Raises RuntimeError: Iterator reused"
                    },
                    {
                        "id": "D",
                        "label": "Iterates in reverse"
                    }
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
                    {
                        "id": "A",
                        "label": "__next__()"
                    },
                    {
                        "id": "B",
                        "label": "__iter__()"
                    },
                    {
                        "id": "C",
                        "label": "__hash__()"
                    },
                    {
                        "id": "D",
                        "label": "__len__()"
                    }
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
        "keyTakeaway": "Iterators are one-way streams that exhaust once; iterables implement __iter__."
    },
    {
        "id": "day19-step4",
        "stepNumber": 4,
        "title": "Build an Even Number Stepper",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Implement an EvenNumberIterator Class",
        "subheading": "Write an iterator that yields even numbers up to a maximum limit.",
        "task": {
            "title": "Even Number Iterator",
            "instructions": [
                "Create class `EvenStepper` that takes `max_limit` in `__init__` and initializes `self.current = 0`.",
                "Implement `__iter__(self)` returning `self`.",
                "Implement `__next__(self)`: while `self.current <= self.max_limit`, record the even number, increment `self.current += 2`, and return the number.",
                "When `self.current > self.max_limit`, raise `StopIteration`.",
                "Iterate over `EvenStepper(6)` and collect items into a list."
            ],
            "starterCode": "# Day 19 Practice: Even Number Iterator\n\nclass EvenStepper:\n    def __init__(self, max_limit):\n        self.max_limit = max_limit\n        self.current = 0\n\n    def __iter__(self):\n        return self\n\n    def __next__(self):\n        # TODO: If self.current > self.max_limit, raise StopIteration\n        # Otherwise save val = self.current, increment self.current by 2, and return val\n        pass\n\nevens = list(EvenStepper(6))\nprint(\"Evens:\", evens)\n",
            "solutionCode": "class EvenStepper:\n    def __init__(self, max_limit):\n        self.max_limit = max_limit\n        self.current = 0\n\n    def __iter__(self):\n        return self\n\n    def __next__(self):\n        if self.current > self.max_limit:\n            raise StopIteration\n        val = self.current\n        self.current += 2\n        return val\n\nevens = list(EvenStepper(6))\nprint(\"Evens:\", evens)\n",
            "expectedOutputPatterns": [
                "Evens: [0, 2, 4, 6]"
            ],
            "hint": "Raise StopIteration when `self.current > self.max_limit`, otherwise advance and return."
        },
        "keyTakeaway": "Custom iterator classes maintain pointer states and terminate cleanly with StopIteration."
    },
    {
        "id": "day19-step5",
        "stepNumber": 5,
        "title": "Iteration Protocol Mastery",
        "shortLabel": "Recap",
        "type": "completion",
        "isGated": false,
        "dayNumber": 19,
        "heading": "Day 19 Complete: Iterators & Iteration Protocol",
        "subheading": "You have mastered __iter__, __next__, StopIteration mechanics, and custom stream classes.",
        "recapRows": [
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
        "solidifiedConcepts": [
            "__iter__() & __next__() Contract",
            "StopIteration Signaling",
            "Stateful Stream Consumption",
            "Sentinel iter() Syntax"
        ],
        "nextDayPreview": {
            "dayNumber": 20,
            "title": "Generators & Lazy Memory Streaming",
            "description": "Implement generator functions with yield, understand execution suspension, generator expressions, and pipeline composition."
        }
    }
]
},
  20: {
  "dayNumber": 20,
  "title": "Generators & Yield Semantics",
  "topicName": "Generators & yield",
  "sectionId": "python-core",
  "estimatedMinutes": 30,
  "difficulty": "FOUNDATIONAL",
  "prerequisites": [
    19
  ],
  "concepts": [
    "yield & yield from",
    "Generator Expressions",
    "Lazy Evaluation",
    "Memory Optimization"
  ],
  "practiceSkills": [
    "Generator Function Authoring",
    "Lazy Pipeline Processing",
    "yield from Delegation"
  ]
,
  "steps": [
    {
        "id": "day20-step1",
        "stepNumber": 1,
        "title": "The yield Keyword & Frame Suspension",
        "shortLabel": "yield & Suspension",
        "type": "explanation",
        "isGated": false,
        "heading": "How Generators Work: Suspending and Resuming Call Frames",
        "subheading": "Generate infinite or massive data streams with fixed O(1) memory.",
        "markdownContent": [
            "A function containing the `yield` keyword is a **generator function**. Calling a generator function does NOT execute its body immediately; it returns a **generator object**.",
            "When `next()` is called on the generator, Python executes bytecode until encountering `yield <value>`. It produces `<value>` and **suspends the execution frame**, freezing all local variables and instruction pointers in place.",
            "On the next `next()` call, execution resumes immediately after the `yield` statement with all local state intact!",
            "When the generator returns (or finishes), it automatically raises `StopIteration`."
        ],
        "snippets": [
            {
                "title": "Generator Execution Lifecycle",
                "code": "def fibonacci():\n    a, b = 0, 1\n    while True:\n        yield a\n        a, b = b, a + b\n\n# Consuming infinite stream lazily with O(1) memory\nfib = fibonacci()\nfor _ in range(5):\n    print(next(fib)) # 0, 1, 1, 2, 3",
                "language": "python",
                "caption": "Infinite stream generator with O(1) memory footprint."
            }
        ],
        "callouts": [
            {
                "type": "tip",
                "title": "Memory Optimization",
                "content": "Reading a 10 GB log file with a list crashes with `MemoryError`. Yielding line by line with a generator uses only a few kilobytes of RAM."
            }
        ],
        "keyTakeaway": "yield suspends the function frame, returning values lazily with O(1) auxiliary memory."
    },
    {
        "id": "day20-step2",
        "stepNumber": 2,
        "title": "Generator Expressions & yield from",
        "shortLabel": "yield from & GenExps",
        "type": "explanation",
        "isGated": false,
        "heading": "Sub-generator Delegation and Lightweight Generator Expressions",
        "subheading": "Chain generators cleanly and write inline lazy streams.",
        "markdownContent": [
            "A **generator expression** uses parentheses: `gen = (x * x for x in range(10))`. Unlike list comprehensions, it computes values on demand without allocating an array.",
            "`yield from sub_gen` delegates iteration directly to a sub-generator, flattening nested streams efficiently without manual loops.",
            "Passing a generator expression directly into functions like `sum()`, `min()`, or `max()` avoids double parentheses: `sum(x * x for x in nums)`."
        ],
        "snippets": [
            {
                "title": "yield from and GenExps in Action",
                "code": "def flatten(nested):\n    for sublist in nested:\n        yield from sublist # Flattens sub-iterables cleanly\n\nprint(list(flatten([[1, 2], [3, 4]]))) # [1, 2, 3, 4]\n\n# Generator expression in sum()\ntotal = sum(x for x in range(100) if x % 2 == 0)",
                "language": "python",
                "caption": "Delegating iteration with yield from."
            }
        ],
        "callouts": [
            {
                "type": "warning",
                "title": "GenExp Exhaustion",
                "content": "Just like iterators, generator expressions can only be consumed once! If you iterate over `g` twice, the second pass yields nothing."
            }
        ],
        "keyTakeaway": "yield from delegates to sub-generators; generator expressions provide lazy inline streams."
    },
    {
        "id": "day20-step3",
        "stepNumber": 3,
        "title": "Generators Checkpoint",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Test Your Mastery of Generators and yield",
        "subheading": "Evaluate frame suspension and generator memory consumption.",
        "checkpoints": [
            {
                "id": "chk-d20-q1",
                "question": "What happens when you call a function that contains a `yield` statement, e.g. `g = my_gen()`?",
                "options": [
                    {
                        "id": "A",
                        "label": "The function executes completely up to the return statement"
                    },
                    {
                        "id": "B",
                        "label": "It returns a generator iterator object without executing the function body yet"
                    },
                    {
                        "id": "C",
                        "label": "It yields the first value immediately"
                    },
                    {
                        "id": "D",
                        "label": "SyntaxError unless decorated with @generator"
                    }
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
                    {
                        "id": "A",
                        "label": "The generator expression compiles to C code"
                    },
                    {
                        "id": "B",
                        "label": "The generator consumes O(1) memory because elements are produced on-the-fly, while the list allocates gigabytes for all 100M pointers upfront"
                    },
                    {
                        "id": "C",
                        "label": "The generator runs multithreaded"
                    },
                    {
                        "id": "D",
                        "label": "There is no difference"
                    }
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
        "keyTakeaway": "Calling a generator function returns a lazy generator object; generator expressions consume O(1) memory."
    },
    {
        "id": "day20-step4",
        "stepNumber": 4,
        "title": "Build a Windowed Batch Generator",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Stream Elements in Fixed-Size Batches",
        "subheading": "Write a generator function that yields items in chunks of size K.",
        "task": {
            "title": "Batch Stream Chunking Generator",
            "instructions": [
                "Write a generator function `batch_stream(items, batch_size)`.",
                "Loop through `items` using index steps: `for i in range(0, len(items), batch_size):`.",
                "Yield the slice `items[i : i + batch_size]`.",
                "Test it on `data = [1, 2, 3, 4, 5, 6, 7]` with `batch_size = 3`.",
                "Collect the batches into a list and print `'Batches:', batches`."
            ],
            "starterCode": "# Day 20 Practice: Batch Stream Chunking Generator\n\ndef batch_stream(items, batch_size):\n    # TODO: Loop i from 0 to len(items) with step batch_size\n    # and yield slice items[i : i + batch_size]\n    pass\n\ndata = [1, 2, 3, 4, 5, 6, 7]\nbatches = list(batch_stream(data, 3))\nprint(\"Batches:\", batches)\n",
            "solutionCode": "def batch_stream(items, batch_size):\n    for i in range(0, len(items), batch_size):\n        yield items[i : i + batch_size]\n\ndata = [1, 2, 3, 4, 5, 6, 7]\nbatches = list(batch_stream(data, 3))\nprint(\"Batches:\", batches)\n",
            "expectedOutputPatterns": [
                "Batches: [[1, 2, 3], [4, 5, 6], [7]]"
            ],
            "hint": "Use `yield items[i : i + batch_size]` inside `for i in range(0, len(items), batch_size):`."
        },
        "keyTakeaway": "Generators decompose bulk collections into lazy chunks without allocating duplicate outer structures."
    },
    {
        "id": "day20-step5",
        "stepNumber": 5,
        "title": "Generators & Yield Mastery",
        "shortLabel": "Recap",
        "type": "completion",
        "isGated": false,
        "dayNumber": 20,
        "heading": "Day 20 Complete: Generators & Yield Semantics",
        "subheading": "You have mastered frame suspension, lazy stream evaluation, and yield from delegation.",
        "recapRows": [
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
        "solidifiedConcepts": [
            "yield Frame Suspension Mechanics",
            "O(1) Memory Streams",
            "yield from Sub-generator Delegation",
            "Generator Expressions vs Comprehensions"
        ],
        "nextDayPreview": {
            "dayNumber": 21,
            "title": "Decorators, Closures & Metadata Wrappers",
            "description": "Write function decorators, understand closures, cell objects, and preserving function metadata with functools.wraps."
        }
    }
]
},
};
