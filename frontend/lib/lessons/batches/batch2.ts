import { DailyLessonPackage } from "../types";

export const BATCH_2_LESSONS: Record<number, DailyLessonPackage> = {
  21: {
  "dayNumber": 21,
  "title": "Decorators & Closures",
  "topicName": "Decorators & Closures",
  "sectionId": "python-core",
  "estimatedMinutes": 35,
  "difficulty": "FOUNDATIONAL",
  "prerequisites": [
    20
  ],
  "concepts": [
    "Closure Cells",
    "Function Wrappers",
    "functools.wraps",
    "Decorator Arguments"
  ],
  "practiceSkills": [
    "Closure Encapsulation",
    "Timer Decorator Authoring",
    "functools.wraps Invariant"
  ]
,
  "steps": [
    {
        "id": "day21-step1",
        "stepNumber": 1,
        "title": "Closures & Free Variables",
        "shortLabel": "Closures & Cells",
        "type": "explanation",
        "isGated": false,
        "heading": "How Closures Work: Functions Retaining Enclosing State",
        "subheading": "Understand lexical scoping and how Python binds free variables in closure cells.",
        "markdownContent": [
            "A **closure** is a nested function that remembers and retains access to variables in its enclosing scope, even after the outer function has finished executing and its stack frame has been destroyed.",
            "Python implements closures using **cell objects** (`__closure__`). Instead of putting the enclosed variable on the stack, Python allocates a cell on the heap so both inner and outer functions share the exact same reference.",
            "Closures form the foundation for decorators, stateful factories, and memoization."
        ],
        "snippets": [
            {
                "title": "Lexical Closure Cell",
                "code": "def make_multiplier(factor):\n    def multiply(x):\n        return x * factor # 'factor' is stored in a closure cell\n    return multiply\n\ndouble = make_multiplier(2)\nprint(double(10)) # 20",
                "language": "python",
                "caption": "Nested function retaining outer parameter."
            }
        ],
        "callouts": [
            {
                "type": "tip",
                "title": "nonlocal Keyword",
                "content": "To reassign an enclosing variable inside a closure, declare it with `nonlocal count`. Without `nonlocal`, assignment creates a new local variable."
            }
        ],
        "keyTakeaway": "Closures capture enclosing variables in heap-allocated cell objects."
    },
    {
        "id": "day21-step2",
        "stepNumber": 2,
        "title": "Decorators & functools.wraps",
        "shortLabel": "Decorators & wraps",
        "type": "explanation",
        "isGated": false,
        "heading": "Syntactic Sugar: @decorator and Preserving Metadata with functools.wraps",
        "subheading": "Wrap and extend function behavior cleanly.",
        "markdownContent": [
            "A **decorator** is a callable that takes a function as an argument and returns an augmented wrapper function.",
            "The syntax `@my_decorator` placed above `def func():` is exact syntactic sugar for: `func = my_decorator(func)`.",
            "Crucially, wrapping a function hides its original name and docstring (`func.__name__` becomes `'wrapper'`). Always use `@functools.wraps(func)` on the wrapper to copy docstrings, annotations, and metadata."
        ],
        "snippets": [
            {
                "title": "Idiomatic Decorator Template",
                "code": "import functools\n\ndef log_call(func):\n    @functools.wraps(func)\n    def wrapper(*args, **kwargs):\n        print(f'Calling {func.__name__}...')\n        result = func(*args, **kwargs)\n        print(f'{func.__name__} completed!')\n        return result\n    return wrapper\n\n@log_call\ndef add(a, b):\n    return a + b",
                "language": "python",
                "caption": "Standard wrapper pattern with metadata preservation."
            }
        ],
        "callouts": [
            {
                "type": "warning",
                "title": "Always Return Result",
                "content": "A common beginner bug is forgetting `return result` inside the wrapper function, causing decorated functions to return None!"
            }
        ],
        "keyTakeaway": "@decorator rebinds func = decorator(func); functools.wraps preserves function name and docstrings."
    },
    {
        "id": "day21-step3",
        "stepNumber": 3,
        "title": "Decorators Checkpoint",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Test Your Mastery of Closures and Decorators",
        "subheading": "Evaluate closure cells and decorator execution timing.",
        "checkpoints": [
            {
                "id": "chk-d21-q1",
                "question": "What is the primary purpose of `@functools.wraps(func)` inside a decorator?",
                "options": [
                    {
                        "id": "A",
                        "label": "It makes the function run 10x faster"
                    },
                    {
                        "id": "B",
                        "label": "It preserves the original function's __name__, __doc__, and signature metadata"
                    },
                    {
                        "id": "C",
                        "label": "It automatically catches all exceptions"
                    },
                    {
                        "id": "D",
                        "label": "It converts synchronous functions to asynchronous"
                    }
                ],
                "correctOptionId": "B",
                "explanations": {
                    "A": "Incorrect: wraps does not optimize execution speed.",
                    "B": "Correct! Without wraps, introspecting func.__name__ returns 'wrapper'. wraps copies the original metadata.",
                    "C": "Incorrect: wraps does not catch exceptions.",
                    "D": "Incorrect: Async conversions require asyncio."
                }
            },
            {
                "id": "chk-d21-q2",
                "question": "When does the outer decorator function execute?",
                "options": [
                    {
                        "id": "A",
                        "label": "Every time the decorated function is called"
                    },
                    {
                        "id": "B",
                        "label": "Once, at the time the function is defined (module import time)"
                    },
                    {
                        "id": "C",
                        "label": "Only when the program terminates"
                    },
                    {
                        "id": "D",
                        "label": "Never; it is purely compile-time annotation"
                    }
                ],
                "correctOptionId": "B",
                "explanations": {
                    "A": "Incorrect: The wrapper runs on each call, but the decorator itself runs at definition time.",
                    "B": "Correct! `@decorator` executes immediately when Python parses the `def` statement, replacing the name with the wrapper.",
                    "C": "Incorrect: It executes immediately during definition.",
                    "D": "Incorrect: Python decorators are real runtime code."
                }
            }
        ],
        "keyTakeaway": "Decorators execute at definition time; functools.wraps preserves function identity."
    },
    {
        "id": "day21-step4",
        "stepNumber": 4,
        "title": "Build an Execution Counter Decorator",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Track Invocation Counts with a Closure Decorator",
        "subheading": "Author a decorator that counts how many times a function is called.",
        "task": {
            "title": "Call Counter Decorator",
            "instructions": [
                "Write a decorator `count_calls(func)` that tracks invocation count in a local integer `call_count = 0`.",
                "Use `@functools.wraps(func)` on `wrapper(*args, **kwargs)`.",
                "Increment `nonlocal call_count` on each call, and print `f'Call {call_count}: {func.__name__}'` before returning `func(*args, **kwargs)`.",
                "Decorate `def greet(name): return f'Hello, {name}'`.",
                "Call `greet('Alice')` and `greet('Bob')`."
            ],
            "starterCode": "# Day 21 Practice: Call Counter Decorator\nimport functools\n\ndef count_calls(func):\n    call_count = 0\n    @functools.wraps(func)\n    def wrapper(*args, **kwargs):\n        nonlocal call_count\n        call_count += 1\n        print(f\"Call {call_count}: {func.__name__}\")\n        return func(*args, **kwargs)\n    return wrapper\n\n@count_calls\ndef greet(name):\n    return f\"Hello, {name}\"\n\ngreet(\"Alice\")\ngreet(\"Bob\")\n",
            "solutionCode": "import functools\n\ndef count_calls(func):\n    call_count = 0\n    @functools.wraps(func)\n    def wrapper(*args, **kwargs):\n        nonlocal call_count\n        call_count += 1\n        print(f\"Call {call_count}: {func.__name__}\")\n        return func(*args, **kwargs)\n    return wrapper\n\n@count_calls\ndef greet(name):\n    return f\"Hello, {name}\"\n\ngreet(\"Alice\")\ngreet(\"Bob\")\n",
            "expectedOutputPatterns": [
                "Call 1: greet",
                "Call 2: greet"
            ],
            "hint": "Use `nonlocal call_count` inside wrapper to mutate the enclosed counter."
        },
        "keyTakeaway": "Decorators leverage closures to maintain state across independent function calls."
    },
    {
        "id": "day21-step5",
        "stepNumber": 5,
        "title": "Decorators & Closures Mastery",
        "shortLabel": "Recap",
        "type": "completion",
        "isGated": false,
        "dayNumber": 21,
        "heading": "Day 21 Complete: Decorators & Closures",
        "subheading": "You have mastered closure cells, syntactic sugar (@), and metadata preservation.",
        "recapRows": [
            {
                "concept": "Enclosing Variable Mutation",
                "naiveIntuition": "Assigning to count inside inner() modifies the outer count automatically",
                "pythonReality": "Without `nonlocal count`, assignment creates a new local variable"
            },
            {
                "concept": "Decorator Invocation Timing",
                "naiveIntuition": "The decorator function executes on every call",
                "pythonReality": "The decorator runs once at definition time; only the returned wrapper runs on calls"
            }
        ],
        "solidifiedConcepts": [
            "Closure Heap Cells",
            "@functools.wraps Invariant",
            "nonlocal Scope Binding",
            "Reusable Decorator Pattern"
        ],
        "nextDayPreview": {
            "dayNumber": 22,
            "title": "OOP Classes, Dunder Protocols & __lt__",
            "description": "Build classes, manage instance state, and implement dunder protocols (__repr__, __eq__, __hash__, and __lt__ for comparators)."
        }
    }
]
},
  22: {
  "dayNumber": 22,
  "title": "OOP: Classes & Dunder Methods",
  "topicName": "OOP Foundations",
  "sectionId": "python-core",
  "estimatedMinutes": 35,
  "difficulty": "FOUNDATIONAL",
  "prerequisites": [
    21
  ],
  "concepts": [
    "__init__, __str__, __repr__",
    "__eq__ & __hash__",
    "self parameter",
    "Instance vs Class Attributes"
  ],
  "practiceSkills": [
    "Dunder Method Implementation",
    "Object Equality Contract",
    "Encapsulation Design"
  ]
,
  "steps": [
    {
        "id": "day22-step1",
        "stepNumber": 1,
        "title": "The Python Data Model & Dunder Methods",
        "shortLabel": "Dunder Methods",
        "type": "explanation",
        "isGated": false,
        "heading": "Special Methods: Hooking Into Python's Native Operator Overloading",
        "subheading": "How dunder methods allow user-defined classes to behave like native types.",
        "markdownContent": [
            "In Python, Object-Oriented Programming is powered by the **Python Data Model**. By defining 'dunder' (double underscore) methods, your classes hook directly into Python operators and built-ins.",
            "`__init__(self, ...)`: Initializes instance attributes after object creation.",
            "`__repr__(self)`: Returns an unambiguous developer representation (ideally valid Python code to recreate the object).",
            "`__str__(self)`: Returns a human-readable string used by `print()` and `str()`.",
            "`__len__(self)` hooks into `len()`, `__getitem__` hooks into `obj[key]`, and `__call__` allows an instance to be invoked like a function."
        ],
        "snippets": [
            {
                "title": "str vs repr in Action",
                "code": "class Point:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n    def __repr__(self):\n        return f'Point({self.x}, {self.y})'\n    def __str__(self):\n        return f'({self.x}, {self.y})'\n\np = Point(3, 4)\nprint(str(p))  # '(3, 4)'\nprint(repr(p)) # 'Point(3, 4)'",
                "language": "python",
                "caption": "Implementing __repr__ and __str__."
            }
        ],
        "callouts": [
            {
                "type": "tip",
                "title": "Always Define __repr__ First",
                "content": "If `__str__` is not defined, Python falls back to `__repr__`. If you only implement one string method, implement `__repr__`!"
            }
        ],
        "keyTakeaway": "Dunder methods hook user classes into native Python operators and built-ins."
    },
    {
        "id": "day22-step2",
        "stepNumber": 2,
        "title": "Object Identity, __eq__, and __hash__",
        "shortLabel": "Equality & Hashing",
        "type": "explanation",
        "isGated": false,
        "heading": "The Contract Between __eq__ and __hash__",
        "subheading": "Why overriding __eq__ requires careful handling of __hash__ for set/dict membership.",
        "markdownContent": [
            "By default, custom classes compare equality using identity (`is`): two instances are equal only if they are the exact same object in memory.",
            "Overriding `__eq__(self, other)` allows value-based equality.",
            "**Crucial Invariant**: If two objects are equal (`a == b`), they **MUST have the exact same hash value (`hash(a) == hash(b)`)**!",
            "In Python, if you override `__eq__` without defining `__hash__`, Python automatically sets `__hash__ = None`, making the class **unhashable** (cannot be added to sets or used as dict keys) to prevent broken hash table contracts."
        ],
        "snippets": [
            {
                "title": "Implementing Hashable Classes",
                "code": "class Coordinate:\n    def __init__(self, r, c):\n        self.r = r\n        self.c = c\n    def __eq__(self, other):\n        return isinstance(other, Coordinate) and (self.r, self.c) == (other.r, other.c)\n    def __hash__(self):\n        return hash((self.r, self.c))\n\ncoords = {Coordinate(1, 2), Coordinate(1, 2)}\nprint(len(coords)) # 1 (properly deduplicated!)",
                "language": "python",
                "caption": "Consistent __eq__ and __hash__ enabling set deduplication."
            }
        ],
        "callouts": [
            {
                "type": "warning",
                "title": "Mutable Hash Trap",
                "content": "Only hash immutable attributes! If `self.r` changes after being inserted into a set, the object will be trapped in the wrong hash bucket and impossible to retrieve."
            }
        ],
        "keyTakeaway": "If a == b is True, hash(a) MUST equal hash(b); overriding __eq__ requires an explicit __hash__."
    },
    {
        "id": "day22-step3",
        "stepNumber": 3,
        "title": "OOP Dunder Checkpoint",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Test Your Mastery of Classes and Dunder Methods",
        "subheading": "Evaluate string representations and hash contracts.",
        "checkpoints": [
            {
                "id": "chk-d22-q1",
                "question": "What happens if you override `__eq__` in a class but do not define `__hash__`?",
                "options": [
                    {
                        "id": "A",
                        "label": "Python inherits object.__hash__ automatically"
                    },
                    {
                        "id": "B",
                        "label": "Python sets __hash__ = None, making instances unhashable"
                    },
                    {
                        "id": "C",
                        "label": "SyntaxError is raised at definition time"
                    },
                    {
                        "id": "D",
                        "label": "hash() returns 0 for all instances"
                    }
                ],
                "correctOptionId": "B",
                "explanations": {
                    "A": "Incorrect: In Python 3, inheriting object.__hash__ is deliberately disabled to prevent violating the hash invariant.",
                    "B": "Correct! CPython sets `__hash__ = None` to ensure that mutable or value-equal objects don't corrupt hash tables.",
                    "C": "Incorrect: Defining __eq__ without __hash__ is valid syntax.",
                    "D": "Incorrect: Attempting hash(instance) raises TypeError: unhashable type."
                }
            },
            {
                "id": "chk-d22-q2",
                "question": "If an object only implements `__repr__` and does NOT implement `__str__`, what does `print(obj)` display?",
                "options": [
                    {
                        "id": "A",
                        "label": "An empty string"
                    },
                    {
                        "id": "B",
                        "label": "TypeError: __str__ required"
                    },
                    {
                        "id": "C",
                        "label": "The output of __repr__ as a fallback"
                    },
                    {
                        "id": "D",
                        "label": "The raw hex memory address"
                    }
                ],
                "correctOptionId": "C",
                "explanations": {
                    "A": "Incorrect: It does not return empty.",
                    "B": "Incorrect: Python never requires __str__ if __repr__ exists.",
                    "C": "Correct! Python automatically falls back to `__repr__` whenever `__str__` is absent.",
                    "D": "Incorrect: The hex address is object's default repr, which was overridden."
                }
            }
        ],
        "keyTakeaway": "Python falls back to __repr__ if __str__ is missing; overriding __eq__ disables default hashing."
    },
    {
        "id": "day22-step4",
        "stepNumber": 4,
        "title": "Build a Vector2D Class",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Implement Vector Addition and String Representations",
        "subheading": "Build a 2D Vector class supporting addition with `__add__`.",
        "task": {
            "title": "Vector2D Vector Class",
            "instructions": [
                "Create class `Vector2D` with `__init__(self, x, y)`.",
                "Implement `__repr__(self)` returning `f'Vector2D({self.x}, {self.y})'`.",
                "Implement `__add__(self, other)`: return a new `Vector2D(self.x + other.x, self.y + other.y)`.",
                "Create `v1 = Vector2D(2, 3)` and `v2 = Vector2D(4, 5)`.",
                "Add them `v3 = v1 + v2` and print `v3`."
            ],
            "starterCode": "# Day 22 Practice: Vector2D Class\n\nclass Vector2D:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n\n    def __repr__(self):\n        return f\"Vector2D({self.x}, {self.y})\"\n\n    # TODO: Implement __add__(self, other) returning new Vector2D\n    def __add__(self, other):\n        return Vector2D(self.x + other.x, self.y + other.y)\n\nv1 = Vector2D(2, 3)\nv2 = Vector2D(4, 5)\nv3 = v1 + v2\n\nprint(\"Result:\", v3)\n",
            "solutionCode": "class Vector2D:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n\n    def __repr__(self):\n        return f\"Vector2D({self.x}, {self.y})\"\n\n    def __add__(self, other):\n        return Vector2D(self.x + other.x, self.y + other.y)\n\nv1 = Vector2D(2, 3)\nv2 = Vector2D(4, 5)\nv3 = v1 + v2\n\nprint(\"Result:\", v3)\n",
            "expectedOutputPatterns": [
                "Result: Vector2D(6, 8)"
            ],
            "hint": "Implement `__add__(self, other)` returning `Vector2D(self.x + other.x, self.y + other.y)`."
        },
        "keyTakeaway": "Implementing __add__ enables intuitive operator overloading with the + operator."
    },
    {
        "id": "day22-step5",
        "stepNumber": 5,
        "title": "OOP & Dunder Methods Mastery",
        "shortLabel": "Recap",
        "type": "completion",
        "isGated": false,
        "dayNumber": 22,
        "heading": "Day 22 Complete: OOP: Classes & Dunder Methods",
        "subheading": "You have mastered Python's Data Model, dunder operators, string representations, and hash invariants.",
        "recapRows": [
            {
                "concept": "String Representation",
                "naiveIntuition": "__str__ is mandatory for all classes",
                "pythonReality": "__repr__ is the primary method; __str__ falls back to __repr__ if omitted"
            },
            {
                "concept": "Hash & Equality Contract",
                "naiveIntuition": "Any class can be added to a set even after overriding __eq__",
                "pythonReality": "Overriding __eq__ disables __hash__; you must provide a matching __hash__"
            }
        ],
        "solidifiedConcepts": [
            "Python Data Model Hooks",
            "__repr__ vs __str__ Roles",
            "__eq__ & __hash__ Invariant",
            "Operator Overloading (__add__)"
        ],
        "nextDayPreview": {
            "dayNumber": 23,
            "title": "Inheritance & Method Resolution Order (C3)",
            "description": "Master single and multiple inheritance, super(), and CPython's C3 Linearization Method Resolution Order (MRO)."
        }
    }
]
},
  23: {
  "dayNumber": 23,
  "title": "Inheritance & Method Resolution Order",
  "topicName": "Inheritance & MRO",
  "sectionId": "python-core",
  "estimatedMinutes": 35,
  "difficulty": "FOUNDATIONAL",
  "prerequisites": [
    22
  ],
  "concepts": [
    "single & multiple inheritance",
    "super() Mechanics",
    "MRO C3 Linearization",
    "isinstance vs type"
  ],
  "practiceSkills": [
    "super() Delegation",
    "MRO Tracing",
    "Polymorphic Hierarchy Design"
  ]
,
  "steps": [
    {
        "id": "day23-step1",
        "stepNumber": 1,
        "title": "Inheritance, super() & Polymorphism",
        "shortLabel": "Inheritance & super()",
        "type": "explanation",
        "isGated": false,
        "heading": "Class Hierarchies and Cooperative Multiple Inheritance with super()",
        "subheading": "Understand why super() does not simply mean 'call parent'.",
        "markdownContent": [
            "Inheritance allows a child class to inherit attributes and methods from one or more base classes: `class Child(Base):`.",
            "`super().__init__(...)` delegates attribute initialization to the next class in the inheritance chain.",
            "In Python, `super()` does not just look at the immediate parent: it follows the **Method Resolution Order (MRO)** dynamically, making cooperative multiple inheritance possible.",
            "Always test types using `isinstance(obj, ClassName)` rather than `type(obj) is ClassName`, because `isinstance` respects the inheritance hierarchy."
        ],
        "snippets": [
            {
                "title": "super() and Polymorphism",
                "code": "class Animal:\n    def speak(self):\n        return 'Some sound'\n\nclass Dog(Animal):\n    def speak(self):\n        return 'Woof!'\n\ndef make_speak(animal: Animal):\n    print(animal.speak()) # Polymorphic dispatch\n\nmake_speak(Dog()) # 'Woof!'",
                "language": "python",
                "caption": "Polymorphic method resolution."
            }
        ],
        "callouts": [
            {
                "type": "tip",
                "title": "Use isinstance, Not type()",
                "content": "`isinstance(Dog(), Animal)` is True! `type(Dog()) is Animal` is False. Never use `type()` equality when verifying interfaces."
            }
        ],
        "keyTakeaway": "super() delegates up the MRO chain; isinstance() respects subclass relationships."
    },
    {
        "id": "day23-step2",
        "stepNumber": 2,
        "title": "Method Resolution Order & C3 Linearization",
        "shortLabel": "MRO & C3",
        "type": "explanation",
        "isGated": false,
        "heading": "The Diamond Problem and How C3 Linearization Computes Class.__mro__",
        "subheading": "How Python resolves method ambiguity in multiple inheritance.",
        "markdownContent": [
            "When a class inherits from multiple parents (`class D(B, C):`), Python must decide which version of a method to execute (the **Diamond Problem**).",
            "Python resolves this using the **C3 Linearization Algorithm**, which guarantees three invariants:",
            "1. Subclasses appear before their parents.",
            "2. Order of base classes listed in definition is strictly preserved.",
            "3. Monotonicity: no class is visited twice or reordered.",
            "You can inspect any class's exact lookup order with `Class.__mro__` or `Class.mro()`."
        ],
        "snippets": [
            {
                "title": "Inspecting MRO in Diamond Inheritance",
                "code": "class A: pass\nclass B(A): pass\nclass C(A): pass\nclass D(B, C): pass\n\nprint([cls.__name__ for cls in D.__mro__])\n# ['D', 'B', 'C', 'A', 'object']",
                "language": "python",
                "caption": "C3 linearization order for diamond inheritance."
            }
        ],
        "callouts": [
            {
                "type": "warning",
                "title": "Inconsistent Hierarchy Rejection",
                "content": "If you construct an impossible inheritance order (e.g. `class A(B)` and `class B(A)`), Python raises `TypeError: Cannot create a consistent method resolution order (MRO)`."
            }
        ],
        "keyTakeaway": "Python resolves multiple inheritance via C3 linearization, accessible via Class.__mro__."
    },
    {
        "id": "day23-step3",
        "stepNumber": 3,
        "title": "Inheritance & MRO Checkpoint",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Test Your Mastery of Inheritance and MRO",
        "subheading": "Trace method resolution orders and type checks.",
        "checkpoints": [
            {
                "id": "chk-d23-q1",
                "question": "If `class Square(Rectangle): pass`, what is the result of `isinstance(Square(5), Rectangle)`?",
                "options": [
                    {
                        "id": "A",
                        "label": "True"
                    },
                    {
                        "id": "B",
                        "label": "False"
                    },
                    {
                        "id": "C",
                        "label": "TypeError"
                    },
                    {
                        "id": "D",
                        "label": "None"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! isinstance checks the entire inheritance chain. Because Square is a subclass of Rectangle, the check evaluates to True.",
                    "B": "Incorrect: Square inherits from Rectangle.",
                    "C": "Incorrect: isinstance is standard and valid.",
                    "D": "Incorrect: It returns a boolean."
                }
            },
            {
                "id": "chk-d23-q2",
                "question": "What is the ultimate root base class of all classes in Python 3?",
                "options": [
                    {
                        "id": "A",
                        "label": "type"
                    },
                    {
                        "id": "B",
                        "label": "object"
                    },
                    {
                        "id": "C",
                        "label": "BaseException"
                    },
                    {
                        "id": "D",
                        "label": "NoneClass"
                    }
                ],
                "correctOptionId": "B",
                "explanations": {
                    "A": "Incorrect: type is the metaclass for creating classes.",
                    "B": "Correct! `object` is the base class for all new-style classes in Python 3, appearing at the end of every __mro__.",
                    "C": "Incorrect: BaseException is the root of exceptions.",
                    "D": "Incorrect: Does not exist."
                }
            }
        ],
        "keyTakeaway": "isinstance() checks the subclass hierarchy; object is the root class of all Python types."
    },
    {
        "id": "day23-step4",
        "stepNumber": 4,
        "title": "Shape Hierarchy with Polymorphism",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Implement Polymorphic Shape Calculators",
        "subheading": "Create a Shape base class with polymorphic area calculation.",
        "task": {
            "title": "Shape Area Hierarchy",
            "instructions": [
                "Create base class `Shape` with method `area(self)` returning `0.0`.",
                "Create subclass `Rectangle(Shape)` with `__init__(self, w, h)` and `area(self)` returning `w * h`.",
                "Create subclass `Square(Rectangle)` with `__init__(self, side)` that calls `super().__init__(side, side)`.",
                "Instantiate `sq = Square(4)` and print `'Square area:', sq.area()`."
            ],
            "starterCode": "# Day 23 Practice: Shape Area Hierarchy\n\nclass Shape:\n    def area(self):\n        return 0.0\n\nclass Rectangle(Shape):\n    def __init__(self, w, h):\n        self.w = w\n        self.h = h\n\n    def area(self):\n        return float(self.w * self.h)\n\n# TODO: Implement Square inheriting from Rectangle using super().__init__(side, side)\nclass Square(Rectangle):\n    def __init__(self, side):\n        super().__init__(side, side)\n\nsq = Square(4)\nprint(\"Square area:\", sq.area())\n",
            "solutionCode": "class Shape:\n    def area(self):\n        return 0.0\n\nclass Rectangle(Shape):\n    def __init__(self, w, h):\n        self.w = w\n        self.h = h\n\n    def area(self):\n        return float(self.w * self.h)\n\nclass Square(Rectangle):\n    def __init__(self, side):\n        super().__init__(side, side)\n\nsq = Square(4)\nprint(\"Square area:\", sq.area())\n",
            "expectedOutputPatterns": [
                "Square area: 16.0"
            ],
            "hint": "Use `super().__init__(side, side)` inside Square's `__init__`."
        },
        "keyTakeaway": "super() allows subclasses to delegate initialization to base classes cleanly."
    },
    {
        "id": "day23-step5",
        "stepNumber": 5,
        "title": "Inheritance & MRO Mastery",
        "shortLabel": "Recap",
        "type": "completion",
        "isGated": false,
        "dayNumber": 23,
        "heading": "Day 23 Complete: Inheritance & Method Resolution Order",
        "subheading": "You have mastered super() delegation, polymorphic method dispatch, and C3 linearization.",
        "recapRows": [
            {
                "concept": "Type Checking",
                "naiveIntuition": "type(x) == Parent checks if x is an instance of Parent",
                "pythonReality": "type(x) only matches exact class; use isinstance(x, Parent) for subclasses"
            },
            {
                "concept": "super() Role",
                "naiveIntuition": "super() only calls the immediate parent",
                "pythonReality": "super() traverses the MRO chain dynamically, supporting cooperative multiple inheritance"
            }
        ],
        "solidifiedConcepts": [
            "super().__init__() Delegation",
            "MRO & C3 Linearization Invariants",
            "isinstance() Polymorphic Checking",
            "Diamond Inheritance Resolution"
        ],
        "nextDayPreview": {
            "dayNumber": 24,
            "title": "Exception Handling & Custom Hierarchies",
            "description": "Write robust error-handling code with try/except/else/finally and build custom domain exception classes."
        }
    }
]
},
  24: {
  "dayNumber": 24,
  "title": "Exceptions, Tracebacks & Custom Errors",
  "topicName": "Exception Handling",
  "sectionId": "python-core",
  "estimatedMinutes": 30,
  "difficulty": "FOUNDATIONAL",
  "prerequisites": [
    23
  ],
  "concepts": [
    "try/except/else/finally",
    "Custom Exception Subclasses",
    "Exception Chaining",
    "EAFP vs LBYL"
  ],
  "practiceSkills": [
    "Custom Exception Creation",
    "try/except/else/finally Flow",
    "EAFP Defensive Programming"
  ]
,
  "steps": [
    {
        "id": "day24-step1",
        "stepNumber": 1,
        "title": "Exception Flow: try, except, else, finally",
        "shortLabel": "Exception Lifecycle",
        "type": "explanation",
        "isGated": false,
        "heading": "The Complete Exception Handling Lifecycle in Python",
        "subheading": "Understand the distinct roles of except, else, and finally.",
        "markdownContent": [
            "Python uses structured exception handling with four complementary clauses:",
            "- `try`: Code that might raise an exception.",
            "- `except ExceptionType as err`: Executes only if a matching exception is raised.",
            "- `else`: Executes **only if NO exception occurred** in the try block.",
            "- `finally`: Executes **unconditionally**, whether an exception occurred, was handled, or even if `return` was called! Ideal for releasing locks and closing files.",
            "Python embraces the **EAFP** philosophy ('Easier to Ask for Forgiveness than Permission'): prefer attempting operations in a try block rather than running defensive pre-checks (LBYL)."
        ],
        "snippets": [
            {
                "title": "Complete try/except/else/finally",
                "code": "def divide(a, b):\n    try:\n        res = a / b\n    except ZeroDivisionError:\n        print('Cannot divide by zero!')\n        return None\n    else:\n        print('Division successful!')\n        return res\n    finally:\n        print('Cleanup complete.') # Always runs!",
                "language": "python",
                "caption": "All four exception blocks in action."
            }
        ],
        "callouts": [
            {
                "type": "tip",
                "title": "Keep Try Blocks Minimal",
                "content": "Only place the specific statement that could raise an error inside the `try:` block. Code that runs upon success belongs in the `else:` block."
            }
        ],
        "keyTakeaway": "try guards, except catches, else runs on success, and finally executes unconditionally."
    },
    {
        "id": "day24-step2",
        "stepNumber": 2,
        "title": "Custom Exceptions & Exception Chaining",
        "shortLabel": "Custom Exceptions",
        "type": "explanation",
        "isGated": false,
        "heading": "Authoring Domain Exceptions and Chaining with 'from'",
        "subheading": "Build meaningful exception hierarchies for enterprise architectures.",
        "markdownContent": [
            "To create custom exceptions, inherit from Python's built-in `Exception` (never `BaseException`, which includes `KeyboardInterrupt` and `SystemExit`).",
            "When catching a low-level error and raising a high-level domain error, preserve the original traceback using exception chaining: `raise CustomError('...') from original_err`.",
            "This sets `__cause__` and outputs explicit context: `'The above exception was the direct cause of the following exception'`. "
        ],
        "snippets": [
            {
                "title": "Custom Exception with Chaining",
                "code": "class ValidationError(Exception):\n    \"\"\"Raised when input data fails domain constraints.\"\"\"\n    pass\n\ndef parse_age(raw):\n    try:\n        return int(raw)\n    except ValueError as err:\n        raise ValidationError(f'Invalid age token: {raw}') from err",
                "language": "python",
                "caption": "Preserving root causes with 'from err'."
            }
        ],
        "callouts": [
            {
                "type": "warning",
                "title": "Never Bare 'except:'",
                "content": "Writing bare `except:` catches `KeyboardInterrupt` (Ctrl+C) and `SystemExit`, making programs impossible to terminate! Always write `except Exception:`."
            }
        ],
        "keyTakeaway": "Custom exceptions inherit from Exception; 'raise ... from err' preserves root cause tracebacks."
    },
    {
        "id": "day24-step3",
        "stepNumber": 3,
        "title": "Exceptions Checkpoint",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Test Your Mastery of Exception Flow and Chaining",
        "subheading": "Trace finally execution and exception inheritance.",
        "checkpoints": [
            {
                "id": "chk-d24-q1",
                "question": "What will this function return?\n\n```python\ndef test():\n    try:\n        return 1\n    finally:\n        return 2\n```",
                "options": [
                    {
                        "id": "A",
                        "label": "1"
                    },
                    {
                        "id": "B",
                        "label": "2"
                    },
                    {
                        "id": "C",
                        "label": "SyntaxError"
                    },
                    {
                        "id": "D",
                        "label": "None"
                    }
                ],
                "correctOptionId": "B",
                "explanations": {
                    "A": "Incorrect: The finally block overrides earlier return statements.",
                    "B": "Correct! Because `finally` is guaranteed to execute before the function frame exits, a return statement inside finally overrides any return statement in try or except.",
                    "C": "Incorrect: Valid Python syntax.",
                    "D": "Incorrect: It returns 2."
                }
            },
            {
                "id": "chk-d24-q2",
                "question": "Why should custom application exceptions inherit from `Exception` rather than `BaseException`?",
                "options": [
                    {
                        "id": "A",
                        "label": "BaseException is not a valid class in Python 3"
                    },
                    {
                        "id": "B",
                        "label": "BaseException includes system-exiting signals like KeyboardInterrupt and SystemExit, which application code should not catch"
                    },
                    {
                        "id": "C",
                        "label": "Exception is faster"
                    },
                    {
                        "id": "D",
                        "label": "There is no difference"
                    }
                ],
                "correctOptionId": "B",
                "explanations": {
                    "A": "Incorrect: BaseException is the root of all exceptions.",
                    "B": "Correct! Inheriting from Exception ensures that standard `except Exception:` handlers will catch your custom error while allowing Ctrl+C (KeyboardInterrupt) to pass through.",
                    "C": "Incorrect: Performance is identical.",
                    "D": "Incorrect: BaseException bypasses standard except Exception handlers."
                }
            }
        ],
        "keyTakeaway": "finally overrides prior returns; inherit from Exception to allow graceful system interruption."
    },
    {
        "id": "day24-step4",
        "stepNumber": 4,
        "title": "Build a Validated Bank Account",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Enforce Balance Limits with InsufficientFundsError",
        "subheading": "Create a custom domain exception and raise it when balance is insufficient.",
        "task": {
            "title": "Bank Account Balance Guard",
            "instructions": [
                "Create custom exception `InsufficientFundsError(Exception)`.",
                "Create class `BankAccount` with `__init__(self, balance)`.",
                "Implement `withdraw(self, amount)`: if `amount > self.balance`, raise `InsufficientFundsError(f'Deficit of {amount - self.balance}')`.",
                "Otherwise deduct `self.balance -= amount` and return `self.balance`.",
                "In test code, catch `InsufficientFundsError as err` and print `'Caught:', type(err).__name__`."
            ],
            "starterCode": "# Day 24 Practice: Bank Account Balance Guard\n\nclass InsufficientFundsError(Exception):\n    pass\n\nclass BankAccount:\n    def __init__(self, balance):\n        self.balance = balance\n\n    def withdraw(self, amount):\n        # TODO: If amount > balance, raise InsufficientFundsError\n        if amount > self.balance:\n            raise InsufficientFundsError(f\"Deficit of {amount - self.balance}\")\n        self.balance -= amount\n        return self.balance\n\naccount = BankAccount(100)\n\ntry:\n    account.withdraw(150)\nexcept InsufficientFundsError as err:\n    print(\"Caught:\", type(err).__name__)\n",
            "solutionCode": "class InsufficientFundsError(Exception):\n    pass\n\nclass BankAccount:\n    def __init__(self, balance):\n        self.balance = balance\n\n    def withdraw(self, amount):\n        if amount > self.balance:\n            raise InsufficientFundsError(f\"Deficit of {amount - self.balance}\")\n        self.balance -= amount\n        return self.balance\n\naccount = BankAccount(100)\n\ntry:\n    account.withdraw(150)\nexcept InsufficientFundsError as err:\n    print(\"Caught:\", type(err).__name__)\n",
            "expectedOutputPatterns": [
                "Caught: InsufficientFundsError"
            ],
            "hint": "Raise `InsufficientFundsError` inside `withdraw` when amount exceeds balance."
        },
        "keyTakeaway": "Custom domain exceptions communicate business invariant violations with precision."
    },
    {
        "id": "day24-step5",
        "stepNumber": 5,
        "title": "Exceptions & Tracebacks Mastery",
        "shortLabel": "Recap",
        "type": "completion",
        "isGated": false,
        "dayNumber": 24,
        "heading": "Day 24 Complete: Exceptions, Tracebacks & Custom Errors",
        "subheading": "You have mastered try/except/else/finally lifecycle, custom errors, and exception chaining.",
        "recapRows": [
            {
                "concept": "else in Exceptions",
                "naiveIntuition": "else runs if an exception was caught",
                "pythonReality": "else runs ONLY if NO exception was raised in the try block"
            },
            {
                "concept": "finally Role",
                "naiveIntuition": "finally only runs if an error occurred",
                "pythonReality": "finally runs unconditionally, even if return or break was executed"
            }
        ],
        "solidifiedConcepts": [
            "try/except/else/finally Architecture",
            "EAFP vs LBYL Paradigms",
            "Custom Exception Subclasses",
            "Exception Chaining with 'from'"
        ],
        "nextDayPreview": {
            "dayNumber": 25,
            "title": "Python DSA Algorithmic Toolkit & Milestone",
            "description": "Synthesize Python core data structures into a complete algorithmic toolkit bridging into Data Structures & Algorithms."
        }
    }
]
},
  25: {
  "dayNumber": 25,
  "title": "Section 2 Review & Pythonic Mastery",
  "topicName": "Section 2 Synthesis",
  "sectionId": "python-core",
  "estimatedMinutes": 35,
  "difficulty": "FOUNDATIONAL",
  "prerequisites": [
    24
  ],
  "concepts": [
    "Composite Data Structures Synthesis",
    "Generators & Iterators",
    "OOP & Dunder Methods",
    "Pythonic Idioms"
  ],
  "practiceSkills": [
    "Multi-Paradigm Synthesis",
    "Custom Data Structure Design",
    "Memory & Algorithm Efficiency"
  ]
,
  "steps": [
    {
        "id": "day25-step1",
        "stepNumber": 1,
        "title": "Python Core Architecture Synthesis",
        "shortLabel": "Section 2 Model",
        "type": "explanation",
        "isGated": false,
        "heading": "Synthesizing Python Core: Data Structures, Protocols & OOP",
        "subheading": "Review the major milestones achieved across Days 11 to 24.",
        "markdownContent": [
            "In Section 2, you transitioned from basic syntax to the core machinery of Python:",
            "1. **Contiguous Arrays & Hash Tables**: Lists are pointer arrays with amortized $O(1)$ append; dicts and sets are open-addressing hash tables with $O(1)$ lookup.",
            "2. **Iteration Protocols & Generators**: `__iter__` and `__next__` define the universal streaming protocol; generators (`yield`) suspend frames for $O(1)$ memory consumption.",
            "3. **Metaprogramming & OOP**: Decorators leverage closure cells to wrap behavior; dunder methods (`__eq__`, `__repr__`, `__add__`) hook into Python's native runtime.",
            "4. **Defensive Architecture**: Exceptions cleanly separate normal flow from error handling using EAFP and custom hierarchy trees."
        ],
        "snippets": [
            {
                "title": "Integrated Python Core Architecture",
                "code": "from collections import deque\n\nclass TaskQueue:\n    \"\"\"Combines OOP, deque O(1) pops, and iterator protocol.\"\"\"\n    def __init__(self):\n        self._tasks = deque()\n    def push(self, task):\n        self._tasks.append(task)\n    def pop(self):\n        return self._tasks.popleft() if self._tasks else None\n    def __iter__(self):\n        while self._tasks:\n            yield self._tasks.popleft()",
                "language": "python",
                "caption": "Combining OOP, collections.deque, and generator yield."
            }
        ],
        "callouts": [
            {
                "type": "tip",
                "title": "Bridge to DSA",
                "content": "With complete mastery of Python's memory model, pointer arrays, hash maps, deques, and protocols, you are ready to study Computational Thinking and Big-O in Section 3!"
            }
        ],
        "keyTakeaway": "Mastery of Python's data model and memory characteristics is the prerequisite for rigorous algorithm design."
    },
    {
        "id": "day25-step2",
        "stepNumber": 2,
        "title": "Pythonic Style Guide & Complexity Invariants",
        "shortLabel": "Pythonic Invariants",
        "type": "explanation",
        "isGated": false,
        "heading": "The Zen of Python in Algorithmic Code",
        "subheading": "Key algorithmic invariants to remember when moving into DSA.",
        "markdownContent": [
            "As you transition into Data Structures and Algorithms:",
            "- **Never use `list.pop(0)`**: It is $O(N)$. Always use `collections.deque.popleft()` ($O(1)$).",
            "- **Never do `item in list` inside a loop**: It turns an $O(N)$ algorithm into $O(N^2)$. Convert to a `set` ($O(1)$).",
            "- **Never concatenate strings in a loop (`s += ch`)**: It allocates a new string each time ($O(N^2)$). Use `''.join(list_of_chars)` ($O(N)$).",
            "- **Always use list comprehensions or generators**: They avoid attribute lookup overhead."
        ],
        "snippets": [
            {
                "title": "Anti-Pattern vs Pythonic Invariants",
                "code": "# Anti-pattern: O(N^2) string building\ns = ''\nfor ch in ['a', 'b', 'c']:\n    s += ch # Allocates new string every iteration!\n\n# Pythonic: O(N) string joining\ns_clean = ''.join(['a', 'b', 'c']) # Single contiguous allocation",
                "language": "python",
                "caption": "Avoid quadratic string concatenation."
            }
        ],
        "callouts": [
            {
                "type": "deep-dive",
                "title": "CPython join() Optimization",
                "content": "`''.join()` precalculates the total byte length of all strings, allocates the exact memory buffer once, and copies all bytes in C."
            }
        ],
        "keyTakeaway": "''.join(seq) is O(N); set membership is O(1); deque.popleft() is O(1)."
    },
    {
        "id": "day25-step3",
        "stepNumber": 3,
        "title": "Python Core Milestone Checkpoint",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Verify Section 2 Mastery Across Core Tenets",
        "subheading": "Test your synthesized mental model of Python composite types and OOP.",
        "checkpoints": [
            {
                "id": "chk-d25-q1",
                "question": "Which operation sequence runs in strictly $O(N)$ total time for an input of size N?",
                "options": [
                    {
                        "id": "A",
                        "label": "Checking if an item exists in a list for each of N items"
                    },
                    {
                        "id": "B",
                        "label": "Popping N elements from index 0 of a list using lst.pop(0)"
                    },
                    {
                        "id": "C",
                        "label": "Converting a list of N elements into a set, then checking membership N times in the set"
                    },
                    {
                        "id": "D",
                        "label": "Concatenating N single characters using s += ch in a loop"
                    }
                ],
                "correctOptionId": "C",
                "explanations": {
                    "A": "Incorrect: N searches of O(N) each results in O(N^2).",
                    "B": "Incorrect: N pops of O(N) each results in O(N^2).",
                    "C": "Correct! Converting to set takes O(N). Each of the N set lookups takes O(1) average time. Total time: O(N) + N * O(1) = O(N)!",
                    "D": "Incorrect: Repeated string concatenation is O(N^2)."
                }
            },
            {
                "id": "chk-d25-q2",
                "question": "What is the key difference between a function with `yield` vs `return`?",
                "options": [
                    {
                        "id": "A",
                        "label": "yield terminates the function immediately"
                    },
                    {
                        "id": "B",
                        "label": "yield suspends the execution frame and retains state; return destroys the frame"
                    },
                    {
                        "id": "C",
                        "label": "yield can only produce integers"
                    },
                    {
                        "id": "D",
                        "label": "return functions are always faster"
                    }
                ],
                "correctOptionId": "B",
                "explanations": {
                    "A": "Incorrect: return terminates; yield suspends.",
                    "B": "Correct! yield freezes the frame and preserves local variables, allowing execution to resume on the next call to next().",
                    "C": "Incorrect: yield produces any Python object.",
                    "D": "Incorrect: For large data, generators save massive memory and time."
                }
            }
        ],
        "keyTakeaway": "Set lookup drops nested searches from O(N^2) to O(N); generators freeze execution frames."
    },
    {
        "id": "day25-step4",
        "stepNumber": 4,
        "title": "Synthesize: LRU Memory Buffer Preview",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Build an Ordered Task Buffer with deque",
        "subheading": "Implement a bounded task buffer that retains the last K items in O(1) time.",
        "task": {
            "title": "Bounded Task Buffer",
            "instructions": [
                "Use `collections.deque(maxlen=3)` to implement a fixed-capacity buffer.",
                "Append tasks `'task1'`, `'task2'`, `'task3'`, `'task4'` to the buffer.",
                "Observe that when capacity exceeds 3, the oldest item `'task1'` is automatically discarded in $O(1)$ time.",
                "Print `'Buffer contents:', list(buffer)` and `'Buffer size:', len(buffer)`."
            ],
            "starterCode": "# Day 25 Practice: Bounded Task Buffer\nfrom collections import deque\n\n# TODO 1: Initialize deque with maxlen=3\nbuffer = deque(maxlen=3)\n\n# TODO 2: Append 'task1', 'task2', 'task3', 'task4'\nbuffer.append(\"task1\")\nbuffer.append(\"task2\")\nbuffer.append(\"task3\")\nbuffer.append(\"task4\")\n\nprint(\"Buffer contents:\", list(buffer))\nprint(\"Buffer size:\", len(buffer))\n",
            "solutionCode": "from collections import deque\n\nbuffer = deque(maxlen=3)\nbuffer.append(\"task1\")\nbuffer.append(\"task2\")\nbuffer.append(\"task3\")\nbuffer.append(\"task4\")\n\nprint(\"Buffer contents:\", list(buffer))\nprint(\"Buffer size:\", len(buffer))\n",
            "expectedOutputPatterns": [
                "Buffer contents: ['task2', 'task3', 'task4']",
                "Buffer size: 3"
            ],
            "hint": "Initialize `deque(maxlen=3)` and append all four tasks."
        },
        "keyTakeaway": "deque with maxlen automatically drops overflow elements in O(1) time, perfect for ring buffers."
    },
    {
        "id": "day25-step5",
        "stepNumber": 5,
        "title": "Section 2 Core Mastery",
        "shortLabel": "Recap",
        "type": "completion",
        "isGated": false,
        "dayNumber": 25,
        "heading": "Day 25 Complete: Section 2 Review & Pythonic Mastery",
        "subheading": "Congratulations! You have completed Section 2: Python Core & Data Structures with complete mastery of memory, data types, OOP, and protocols.",
        "recapRows": [
            {
                "concept": "Algorithm Scaling",
                "naiveIntuition": "List pop(0) and in searches are fine for small data",
                "pythonReality": "They degrade to O(N^2); always use deques and sets for algorithmic scale"
            },
            {
                "concept": "Memory Management",
                "naiveIntuition": "Allocating lists for everything is standard",
                "pythonReality": "Generators allow streaming gigabytes of data in fixed O(1) RAM"
            }
        ],
        "solidifiedConcepts": [
            "Dynamic Arrays & Hash Tables",
            "collections.deque O(1) Invariants",
            "Generators & Iteration Protocols",
            "OOP, super() & Dunder Methods",
            "Section 2 Completion"
        ],
        "nextDayPreview": {
            "dayNumber": 26,
            "title": "Asymptotic Analysis & Big-O Notation",
            "description": "Understand Big-O notation, asymptotic upper bounds, growth rate hierarchies, and worst-case vs average-case behavior."
        }
    }
]
},
  26: {
  "dayNumber": 26,
  "title": "Asymptotic Analysis & Big-O Notation",
  "topicName": "Big-O Analysis",
  "sectionId": "computational-thinking",
  "estimatedMinutes": 35,
  "difficulty": "DEVELOPING",
  "prerequisites": [
    25
  ],
  "concepts": [
    "Big-O, Omega, Theta",
    "Worst vs Average Case",
    "Input Scaling",
    "Dominant Terms"
  ],
  "practiceSkills": [
    "Complexity Derivation",
    "Dominant Term Extraction",
    "Asymptotic Comparison"
  ]
,
  "steps": [
    {
        "id": "day26-step1",
        "stepNumber": 1,
        "title": "The Language of Algorithmic Scaling",
        "shortLabel": "Big-O Foundations",
        "type": "explanation",
        "isGated": false,
        "heading": "Why We Care About Asymptotics: Upper Bounds, Lower Bounds, and Tight Bounds",
        "subheading": "Formalizing how algorithms scale as input size N tends toward infinity.",
        "markdownContent": [
            "In computer science, wall-clock execution time depends on CPU clock speeds, operating system schedulers, and memory buses. To measure algorithmic efficiency independently of hardware, we use **asymptotic analysis**.",
            "- **Big-O ($O$)**: Represents an asymptotic **upper bound** (worst-case scaling guarantee). $f(N) = O(g(N))$ means $f(N) \\le c \\cdot g(N)$ for all $N \\ge N_0$.",
            "- **Big-Omega ($\\Omega$)**: Represents an asymptotic **lower bound** (best-case floor).",
            "- **Big-Theta ($\\Theta$)**: Represents an asymptotically **tight bound** (both upper and lower).",
            "When analyzing code, we drop non-dominant terms and constant coefficients: $3N^2 + 50N + 1000$ scales as $O(N^2)$ because as $N \\to \\infty$, the $N^2$ term dwarfs all others."
        ],
        "snippets": [
            {
                "title": "Dropping Constants and Dominant Terms",
                "code": "def process_data(arr):\n    n = len(arr)\n    # Step 1: O(N) pass\n    total = sum(arr)\n    # Step 2: O(N^2) nested loop\n    pairs = []\n    for i in range(n):\n        for j in range(i + 1, n):\n            pairs.append((arr[i], arr[j]))\n    return total, pairs # Total: O(N) + O(N^2) -> Dominant is O(N^2)",
                "language": "python",
                "caption": "Extracting the dominant term from multi-phase algorithms."
            }
        ],
        "callouts": [
            {
                "type": "tip",
                "title": "Hierarchy of Growth Rates",
                "content": "$O(1) < O(\\log N) < O(\\sqrt{N}) < O(N) < O(N \\log N) < O(N^2) < O(2^N) < O(N!)$."
            }
        ],
        "keyTakeaway": "Big-O characterizes the upper bound scaling rate by keeping only the highest-order dominant term."
    },
    {
        "id": "day26-step2",
        "stepNumber": 2,
        "title": "Common Big-O Pitfalls & Invariants",
        "shortLabel": "Big-O Gotchas",
        "type": "explanation",
        "isGated": false,
        "heading": "Analyzing Independent Variables: O(N + M) vs O(N * M)",
        "subheading": "Avoid the common trap of assuming all inputs have the same size.",
        "markdownContent": [
            "When an algorithm processes two distinct input arrays of lengths $N$ and $M$:",
            "- If loops run sequentially, time complexity is $O(N + M)$.",
            "- If loops are nested, time complexity is $O(N \\times M)$. Never abbreviate this as $O(N^2)$ unless $N = M$!",
            "String slicing `s[i:j]` of length $K$ takes $O(K)$ time, not $O(1)$. Slicing inside a loop of size $N$ can sneakily turn an $O(N)$ loop into $O(N^2)$!"
        ],
        "snippets": [
            {
                "title": "Multiple Variables and Hidden Slice Costs",
                "code": "def search_matrix(grid, query):\n    # grid has R rows and C columns\n    for row in grid:       # Runs R times\n        if query in row:   # Scans C elements: O(C)\n            return True\n    return False # Total time: O(R * C), not O(N^2)!",
                "language": "python",
                "caption": "Accurate accounting for multi-variable inputs."
            }
        ],
        "callouts": [
            {
                "type": "warning",
                "title": "The Hidden O(N) in String Slices",
                "content": "`sub = s[:i]` allocates a brand new string of length `i`. Doing this inside `for i in range(len(s))` costs $1 + 2 + ... + N = O(N^2)$ time!"
            }
        ],
        "keyTakeaway": "Differentiate multiple input dimensions (O(N*M)) and account for hidden sequence slice costs."
    },
    {
        "id": "day26-step3",
        "stepNumber": 3,
        "title": "Big-O Analysis Checkpoint",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Test Your Mastery of Asymptotic Scaling",
        "subheading": "Determine dominant terms and identify hidden complexity costs.",
        "checkpoints": [
            {
                "id": "chk-d26-q1",
                "question": "What is the Big-O time complexity of an algorithm that performs $1000 N + 4 N \\log N + 0.001 N^2$ operations?",
                "options": [
                    {
                        "id": "A",
                        "label": "O(N log N)"
                    },
                    {
                        "id": "B",
                        "label": "O(N)"
                    },
                    {
                        "id": "C",
                        "label": "O(N^2)"
                    },
                    {
                        "id": "D",
                        "label": "O(1000 N)"
                    }
                ],
                "correctOptionId": "C",
                "explanations": {
                    "A": "Incorrect: N^2 grows faster than N log N for large N.",
                    "B": "Incorrect: N is sub-dominant.",
                    "C": "Correct! As N -> infinity, N^2 grows strictly faster than N or N log N regardless of constant coefficients (even 0.001 vs 1000). The dominant term is O(N^2).",
                    "D": "Incorrect: Constant multipliers are dropped in asymptotic analysis."
                }
            },
            {
                "id": "chk-d26-q2",
                "question": "What is the time complexity of running `s = s[1:]` repeatedly N times where s initially has length N?",
                "options": [
                    {
                        "id": "A",
                        "label": "O(N)"
                    },
                    {
                        "id": "B",
                        "label": "O(N^2)"
                    },
                    {
                        "id": "C",
                        "label": "O(1)"
                    },
                    {
                        "id": "D",
                        "label": "O(N log N)"
                    }
                ],
                "correctOptionId": "B",
                "explanations": {
                    "A": "Incorrect: Each slice allocates a copy of remaining characters.",
                    "B": "Correct! In step 1, s[1:] copies N-1 chars; in step 2, N-2 chars, down to 1. The sum is (N-1) + (N-2) + ... + 1 = N(N-1)/2, which is O(N^2)!",
                    "C": "Incorrect: Slicing strings is not O(1) pointer movement because strings are immutable copies.",
                    "D": "Incorrect: It forms an arithmetic series summing to quadratic time."
                }
            }
        ],
        "keyTakeaway": "Drop constants and sub-dominant terms; repeated slicing on immutable sequences costs O(N^2)."
    },
    {
        "id": "day26-step4",
        "stepNumber": 4,
        "title": "Analyze and Optimize Nested Check",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Refactor Quadratic O(N^2) Pair Search to Linear O(N)",
        "subheading": "Optimize a target-difference check from nested loops to set lookup.",
        "task": {
            "title": "Target Difference Optimizer",
            "instructions": [
                "Given `nums = [1, 5, 3, 4, 2]` and `k = 2`, find if any pair `(a, b)` satisfies `a - b == k`.",
                "The naive approach uses nested loops costing $O(N^2)$.",
                "Refactor to $O(N)$ by loading `nums` into a `set` called `num_set`.",
                "Iterate over `x in nums`: if `(x - k) in num_set`, a pair exists!",
                "Print `'Pair found:', True`."
            ],
            "starterCode": "# Day 26 Practice: Target Difference Optimizer\nnums = [1, 5, 3, 4, 2]\nk = 2\n\n# TODO: Refactor O(N^2) search into O(N) using set lookup\nnum_set = set(nums)\nfound = False\n\nfor x in nums:\n    if (x - k) in num_set:\n        found = True\n        break\n\nprint(\"Pair found:\", found)\n",
            "solutionCode": "nums = [1, 5, 3, 4, 2]\nk = 2\n\nnum_set = set(nums)\nfound = False\n\nfor x in nums:\n    if (x - k) in num_set:\n        found = True\n        break\n\nprint(\"Pair found:\", found)\n",
            "expectedOutputPatterns": [
                "Pair found: True"
            ],
            "hint": "Convert nums to `num_set = set(nums)` and check `if (x - k) in num_set:` in O(1) time."
        },
        "keyTakeaway": "Replacing inner linear scans with O(1) hash sets reduces algorithmic complexity from O(N^2) to O(N)."
    },
    {
        "id": "day26-step5",
        "stepNumber": 5,
        "title": "Asymptotic Analysis Mastery",
        "shortLabel": "Recap",
        "type": "completion",
        "isGated": false,
        "dayNumber": 26,
        "heading": "Day 26 Complete: Asymptotic Analysis & Big-O Notation",
        "subheading": "You have mastered Big-O upper bounds, dominant term extraction, and hidden slice complexities.",
        "recapRows": [
            {
                "concept": "Dominant Terms",
                "naiveIntuition": "1000N is larger than 0.01N^2 so it dominates",
                "pythonReality": "For sufficiently large N, N^2 always grows faster than N; constants are discarded"
            },
            {
                "concept": "String Slicing Cost",
                "naiveIntuition": "s[1:] just moves a start pointer in O(1) time",
                "pythonReality": "Strings allocate new copies of characters, taking O(K) time and space"
            }
        ],
        "solidifiedConcepts": [
            "Big-O, Omega, and Theta Definitions",
            "Dominant Term Isolation",
            "Multi-Variable Complexities (O(N*M))",
            "Avoiding Hidden O(N^2) Slice Anti-Patterns"
        ],
        "nextDayPreview": {
            "dayNumber": 27,
            "title": "Identifying Common Time Complexities",
            "description": "Analyze code snippets to determine O(1), O(log N), O(N), O(N log N), O(N^2), and O(2^N) time complexities."
        }
    }
]
},
  27: {
  "dayNumber": 27,
  "title": "Space Complexity & Auxiliary Memory",
  "topicName": "Space Complexity",
  "sectionId": "computational-thinking",
  "estimatedMinutes": 30,
  "difficulty": "DEVELOPING",
  "prerequisites": [
    26
  ],
  "concepts": [
    "Auxiliary vs Total Space",
    "Call Stack Overhead",
    "In-Place Modifications",
    "Memory Tradeoffs"
  ],
  "practiceSkills": [
    "Space Complexity Accounting",
    "In-Place Mutation Invariants",
    "Stack Depth Analysis"
  ]
,
  "steps": [
    {
        "id": "day27-step1",
        "stepNumber": 1,
        "title": "Total Space vs Auxiliary Space",
        "shortLabel": "Space Accounting",
        "type": "explanation",
        "isGated": false,
        "heading": "Differentiating Input Space from Auxiliary (Working) Space",
        "subheading": "Accurately calculate memory consumption without confusing inputs with overhead.",
        "markdownContent": [
            "When analyzing memory complexity, we distinguish between two metrics:",
            "- **Total Space Complexity**: The total memory consumed, including input storage, working variables, and output structures.",
            "- **Auxiliary Space Complexity**: The **extra memory** allocated by the algorithm exclusively to perform its computation, excluding the input data.",
            "An algorithm that modifies an input array of size $N$ in-place without allocating extra buffers uses **$O(1)$ auxiliary space**, even though the input itself takes $O(N)$ memory."
        ],
        "snippets": [
            {
                "title": "O(1) Auxiliary Space In-Place Transformation",
                "code": "def reverse_in_place(arr):\n    # Modifies arr in-place: O(1) Auxiliary Space\n    left, right = 0, len(arr) - 1\n    while left < right:\n        arr[left], arr[right] = arr[right], arr[left]\n        left += 1\n        right -= 1\n    return arr",
                "language": "python",
                "caption": "Two-pointer swap requiring O(1) auxiliary variables."
            }
        ],
        "callouts": [
            {
                "type": "tip",
                "title": "Interview Standard",
                "content": "When interviewers ask for 'space complexity', they almost always mean **auxiliary space complexity** unless explicitly specified."
            }
        ],
        "keyTakeaway": "Auxiliary space measures only extra working memory allocated beyond the input itself."
    },
    {
        "id": "day27-step2",
        "stepNumber": 2,
        "title": "Call Stack Space in Recursion",
        "shortLabel": "Stack Overhead",
        "type": "explanation",
        "isGated": false,
        "heading": "Why Recursion is Never O(1) Space: The Hidden Call Stack",
        "subheading": "Account for frame allocations on the execution stack.",
        "markdownContent": [
            "Every recursive call creates a new stack frame storing local variables, parameters, and return addresses (~8KB per frame in CPython).",
            "If a recursive function recurses to a depth of $N$ before reaching its base case, it consumes **$O(N)$ auxiliary space on the call stack**, even if it creates no lists or variables!",
            "In Python, the maximum recursion depth is guarded by `sys.getrecursionlimit()` (default: 1000). Exceeding this raises `RecursionError: maximum recursion depth exceeded`."
        ],
        "snippets": [
            {
                "title": "Recursive Call Stack Depth",
                "code": "def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1) # Pushes N frames onto call stack!\n# Time: O(N), Auxiliary Space: O(N) stack frames\n\ndef factorial_iterative(n):\n    res = 1\n    for i in range(2, n + 1):\n        res *= i\n    return res\n# Time: O(N), Auxiliary Space: O(1) - single integer variable!",
                "language": "python",
                "caption": "Recursive vs iterative auxiliary memory footprint."
            }
        ],
        "callouts": [
            {
                "type": "warning",
                "title": "Python Does NOT Have Tail-Call Optimization (TCO)",
                "content": "Unlike Scheme or some JavaScript engines, Python never optimizes tail recursion. Every recursive call always allocates a new frame."
            }
        ],
        "keyTakeaway": "Recursive algorithms consume O(depth) auxiliary stack space; Python does not support TCO."
    },
    {
        "id": "day27-step3",
        "stepNumber": 3,
        "title": "Space Complexity Checkpoint",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Test Your Mastery of Space Accounting",
        "subheading": "Differentiate auxiliary memory from call stack frames.",
        "checkpoints": [
            {
                "id": "chk-d27-q1",
                "question": "What is the auxiliary space complexity of a recursive binary search that divides an array of size N in half each step without copying arrays?",
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
                        "label": "O(N log N)"
                    }
                ],
                "correctOptionId": "B",
                "explanations": {
                    "A": "Incorrect: Iterative binary search is O(1), but recursive binary search pushes frames onto the stack.",
                    "B": "Correct! The maximum recursion depth is log2(N). At peak depth, log2(N) call frames exist on the stack simultaneously, consuming O(log N) auxiliary space.",
                    "C": "Incorrect: The search space halves at every step, so depth is logarithmic, not linear.",
                    "D": "Incorrect: Recursion depth is log N."
                }
            },
            {
                "id": "chk-d27-q2",
                "question": "If an algorithm creates a frequency hash map of all unique characters in a string of length N containing only lowercase English letters ('a'-'z'), what is its auxiliary space complexity?",
                "options": [
                    {
                        "id": "A",
                        "label": "O(N)"
                    },
                    {
                        "id": "B",
                        "label": "O(1)"
                    },
                    {
                        "id": "C",
                        "label": "O(N^2)"
                    },
                    {
                        "id": "D",
                        "label": "O(26^N)"
                    }
                ],
                "correctOptionId": "B",
                "explanations": {
                    "A": "Incorrect: The map cannot exceed 26 entries regardless of how large N is.",
                    "B": "Correct! Because the alphabet is bounded by a fixed constant (26 keys), the hash map size is bounded by O(26) = O(1) space!",
                    "C": "Incorrect: Space is strictly bounded.",
                    "D": "Incorrect: Character count is fixed."
                }
            }
        ],
        "keyTakeaway": "Recursion stack depth determines recursive space; bounded alphabet size yields O(1) auxiliary space."
    },
    {
        "id": "day27-step4",
        "stepNumber": 4,
        "title": "Convert Recursion to O(1) Space",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Refactor Recursive Sum to O(1) Space Accumulator",
        "subheading": "Convert an O(N) call-stack recursive sum to an O(1) auxiliary space loop.",
        "task": {
            "title": "O(1) Space Summation",
            "instructions": [
                "Given `nums = [10, 20, 30, 40, 50]`.",
                "Implement `sum_iterative(arr)` using a single accumulator `total = 0` in an iterative loop.",
                "Confirm the result equals 150.",
                "Print `'Iterative sum:', result`."
            ],
            "starterCode": "# Day 27 Practice: O(1) Space Summation\nnums = [10, 20, 30, 40, 50]\n\ndef sum_iterative(arr):\n    # TODO: Sum elements with O(1) auxiliary space\n    total = 0\n    for x in arr:\n        total += x\n    return total\n\nresult = sum_iterative(nums)\nprint(\"Iterative sum:\", result)\n",
            "solutionCode": "nums = [10, 20, 30, 40, 50]\n\ndef sum_iterative(arr):\n    total = 0\n    for x in arr:\n        total += x\n    return total\n\nresult = sum_iterative(nums)\nprint(\"Iterative sum:\", result)\n",
            "expectedOutputPatterns": [
                "Iterative sum: 150"
            ],
            "hint": "Use a single `total` variable and loop over `arr` to achieve O(1) auxiliary memory."
        },
        "keyTakeaway": "Iterative loops replace call-stack frames with constant auxiliary state."
    },
    {
        "id": "day27-step5",
        "stepNumber": 5,
        "title": "Space Complexity Mastery",
        "shortLabel": "Recap",
        "type": "completion",
        "isGated": false,
        "dayNumber": 27,
        "heading": "Day 27 Complete: Space Complexity & Auxiliary Memory",
        "subheading": "You have mastered auxiliary vs total space, call stack overhead, and bounded alphabet optimization.",
        "recapRows": [
            {
                "concept": "Recursive Space",
                "naiveIntuition": "Recursion that returns numbers without arrays is O(1) space",
                "pythonReality": "Every recursive call allocates a stack frame; depth determines auxiliary space"
            },
            {
                "concept": "Alphabet Hash Tables",
                "naiveIntuition": "A dictionary storing counts for a string of length N is always O(N) space",
                "pythonReality": "If the character set is bounded (e.g. ASCII or English lowercase), space is O(1)"
            }
        ],
        "solidifiedConcepts": [
            "Auxiliary vs Total Memory Definition",
            "Call Stack Depth & Frame Allocation",
            "Lack of Tail-Call Optimization in Python",
            "Bounded Alphabet O(1) Space Invariant"
        ],
        "nextDayPreview": {
            "dayNumber": 28,
            "title": "Space Complexity & Auxiliary Memory",
            "description": "Differentiate total space from auxiliary space, measure memory allocations, and analyze recursion stack overhead."
        }
    }
]
},
  28: {
  "dayNumber": 28,
  "title": "Recursion Fundamentals & Call Stack",
  "topicName": "Recursion Foundations",
  "sectionId": "computational-thinking",
  "estimatedMinutes": 35,
  "difficulty": "DEVELOPING",
  "prerequisites": [
    27
  ],
  "concepts": [
    "Base Case Invariant",
    "Recursive Step",
    "Call Stack Unwinding",
    "Recursion Depth Limits"
  ],
  "practiceSkills": [
    "Base Case Design",
    "Call Stack Tracing",
    "Recursive Decomposition"
  ]
,
  "steps": [
    {
        "id": "day28-step1",
        "stepNumber": 1,
        "title": "The Anatomy of Recursion",
        "shortLabel": "Base Case & Step",
        "type": "explanation",
        "isGated": false,
        "heading": "How Recursion Works: Base Case, Recursive Leap, and Stack Frames",
        "subheading": "Master the two essential components that prevent infinite recursion.",
        "markdownContent": [
            "Recursion is a programming paradigm where a function solves a problem by calling itself on smaller instances of the exact same problem.",
            "Every valid recursive function must contain two essential parts:",
            "1. **Base Case(s)**: A terminating condition that returns a result immediately without making further recursive calls.",
            "2. **Recursive Step**: Reduces the problem size toward the base case and combines the returned result.",
            "Without a base case, or if the recursive step does not shrink the input, the function pushes frames indefinitely until hitting Python's `sys.getrecursionlimit()`."
        ],
        "snippets": [
            {
                "title": "Anatomy of Factorial Recursion",
                "code": "def factorial(n):\n    # 1. Base Case: stop condition\n    if n <= 1:\n        return 1\n    # 2. Recursive Step: shrink problem size toward base case\n    return n * factorial(n - 1)",
                "language": "python",
                "caption": "Clear base case and shrinking recursive subproblem."
            }
        ],
        "callouts": [
            {
                "type": "warning",
                "title": "Recursion Limit in Python",
                "content": "Python's default recursion limit is 1,000 frames. Deep recursion ($N > 1000$) will crash with `RecursionError` unless rewritten iteratively."
            }
        ],
        "keyTakeaway": "Recursion requires a base case to terminate and a recursive step that shrinks toward the base case."
    },
    {
        "id": "day28-step2",
        "stepNumber": 2,
        "title": "Call Stack Unwinding & Return Phase",
        "shortLabel": "Unwinding Phase",
        "type": "explanation",
        "isGated": false,
        "heading": "Winding vs Unwinding: How Values Propagate Back Up the Stack",
        "subheading": "Understand the two phases of recursive execution.",
        "markdownContent": [
            "A recursive call involves two distinct phases:",
            "1. **Winding Phase (Downwards)**: Frames are pushed onto the stack as the problem is broken down into subproblems.",
            "2. **Unwinding Phase (Upwards)**: Once the base case is reached, each frame computes its result using the returned value from its child frame and pops off the stack.",
            "Work performed before the recursive call executes on the way down; work performed after the recursive call executes on the way up during unwinding."
        ],
        "snippets": [
            {
                "title": "Pre-order vs Post-order Actions in Recursion",
                "code": "def countdown_and_up(n):\n    if n == 0:\n        print('Liftoff!')\n        return\n    print('Down:', n)         # Pre-recursion (winding)\n    countdown_and_up(n - 1)\n    print('Up:', n)           # Post-recursion (unwinding)",
                "language": "python",
                "caption": "Actions executed before vs after the recursive call."
            }
        ],
        "callouts": [
            {
                "type": "tip",
                "title": "Think Subproblem, Not Stack",
                "content": "When writing recursion, trust that `solve(n - 1)` correctly computes the subproblem, then focus only on how to combine it with `n`."
            }
        ],
        "keyTakeaway": "Work before the call runs on the way down; work after the call runs on the way up as frames unwind."
    },
    {
        "id": "day28-step3",
        "stepNumber": 3,
        "title": "Recursion Checkpoint",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Test Your Understanding of Recursive Invariants",
        "subheading": "Identify base case flaws and trace stack unwinding.",
        "checkpoints": [
            {
                "id": "chk-d28-q1",
                "question": "What happens if a recursive function does NOT make progress toward its base case?",
                "options": [
                    {
                        "id": "A",
                        "label": "It returns None"
                    },
                    {
                        "id": "B",
                        "label": "It enters an infinite loop until Python raises RecursionError"
                    },
                    {
                        "id": "C",
                        "label": "It automatically converts to an iterative loop"
                    },
                    {
                        "id": "D",
                        "label": "The CPU halts"
                    }
                ],
                "correctOptionId": "B",
                "explanations": {
                    "A": "Incorrect: It never reaches a return statement.",
                    "B": "Correct! Without shrinking the input, recursive calls push frames until exceeding sys.getrecursionlimit(), raising RecursionError: maximum recursion depth exceeded.",
                    "C": "Incorrect: Python has no automatic iteration compiler.",
                    "D": "Incorrect: The Python runtime intercepts stack overflow gracefully."
                }
            },
            {
                "id": "chk-d28-q2",
                "question": "In `def f(n): if n == 0: return; print(n); f(n-1); print(n)`, what prints for `f(2)`?",
                "options": [
                    {
                        "id": "A",
                        "label": "2, 1, 1, 2"
                    },
                    {
                        "id": "B",
                        "label": "2, 1, 2, 1"
                    },
                    {
                        "id": "C",
                        "label": "1, 2, 2, 1"
                    },
                    {
                        "id": "D",
                        "label": "2, 1"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! On the way down: prints 2, then 1. On unwinding: prints 1, then 2. Result: 2, 1, 1, 2.",
                    "B": "Incorrect: Unwinding pops the innermost frame (n=1) first.",
                    "C": "Incorrect: The first print executes before recursive call.",
                    "D": "Incorrect: The second print executes during unwinding."
                }
            }
        ],
        "keyTakeaway": "Recursion unwinds in LIFO order; failing to shrink inputs triggers RecursionError."
    },
    {
        "id": "day28-step4",
        "stepNumber": 4,
        "title": "Recursive String Reversal",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Reverse a String Recursively Without Slices",
        "subheading": "Implement string reversal by decomposing into head character and tail substring.",
        "task": {
            "title": "Recursive Reverser",
            "instructions": [
                "Write a recursive function `reverse_str(s)`.",
                "Base case: if `len(s) <= 1`, return `s`.",
                "Recursive step: return `reverse_str(s[1:]) + s[0]`.",
                "Call `reverse_str('algorithm')` and print `'Reversed:', result`."
            ],
            "starterCode": "# Day 28 Practice: Recursive Reverser\n\ndef reverse_str(s):\n    # TODO: Implement base case and recursive step\n    if len(s) <= 1:\n        return s\n    return reverse_str(s[1:]) + s[0]\n\nresult = reverse_str(\"algorithm\")\nprint(\"Reversed:\", result)\n",
            "solutionCode": "def reverse_str(s):\n    if len(s) <= 1:\n        return s\n    return reverse_str(s[1:]) + s[0]\n\nresult = reverse_str(\"algorithm\")\nprint(\"Reversed:\", result)\n",
            "expectedOutputPatterns": [
                "Reversed: mhtirogla"
            ],
            "hint": "Return `s` when `len(s) <= 1`, otherwise return `reverse_str(s[1:]) + s[0]`."
        },
        "keyTakeaway": "Recursion unwinds strings by appending the head character after reversing the tail."
    },
    {
        "id": "day28-step5",
        "stepNumber": 5,
        "title": "Recursion Fundamentals Mastery",
        "shortLabel": "Recap",
        "type": "completion",
        "isGated": false,
        "dayNumber": 28,
        "heading": "Day 28 Complete: Recursion Fundamentals & Call Stack",
        "subheading": "You have mastered base case design, call stack unwinding, and recursion depth limits.",
        "recapRows": [
            {
                "concept": "Base Case Omission",
                "naiveIntuition": "The compiler will detect if a loop or recursion doesn't stop",
                "pythonReality": "Missing base cases cause runtime stack overflow (RecursionError)"
            },
            {
                "concept": "Execution Order",
                "naiveIntuition": "All statements execute before recursive calls",
                "pythonReality": "Statements after the recursive call execute on stack unwinding in reverse order"
            }
        ],
        "solidifiedConcepts": [
            "Base Case Invariant",
            "Recursive Problem Shrinking",
            "Stack Winding and Unwinding",
            "RecursionError Limit Guard"
        ],
        "nextDayPreview": {
            "dayNumber": 29,
            "title": "Brute Force to Optimized Reductions",
            "description": "Learn systematic techniques to recognize quadratic bottlenecks and optimize them using precomputation or hash tables."
        }
    }
]
},
  29: {
  "dayNumber": 29,
  "title": "Recurrence Relations & Master Theorem",
  "topicName": "Recurrences & Master Theorem",
  "sectionId": "computational-thinking",
  "estimatedMinutes": 35,
  "difficulty": "DEVELOPING",
  "prerequisites": [
    28
  ],
  "concepts": [
    "Recurrence Equations",
    "Master Theorem Cases",
    "Recursion Trees",
    "Divide & Conquer Scaling"
  ],
  "practiceSkills": [
    "Recurrence Formulation",
    "Master Theorem Application",
    "Tree Depth Derivation"
  ]
,
  "steps": [
    {
        "id": "day29-step1",
        "stepNumber": 1,
        "title": "Formulating Recurrence Relations",
        "shortLabel": "Recurrences",
        "type": "explanation",
        "isGated": false,
        "heading": "Expressing Algorithmic Runtimes as Mathematical Equations",
        "subheading": "How to express recursive time complexity as $T(N) = a T(N/b) + f(N)$.",
        "markdownContent": [
            "A **recurrence relation** expresses the time required to solve a problem of size $N$ in terms of the time required to solve smaller subproblems.",
            "The standard divide-and-conquer recurrence has the form: $$T(N) = a \\cdot T(N/b) + f(N)$$ where:",
            "- $a \\ge 1$: Number of recursive subproblems created.",
            "- $b > 1$: Factor by which input size is divided at each step.",
            "- $f(N)$: Non-recursive work required to divide the problem and merge solutions.",
            "For example, Merge Sort divides an array into $2$ halves ($a=2, b=2$) and takes $O(N)$ linear time to merge them: $T(N) = 2T(N/2) + O(N)$."
        ],
        "snippets": [
            {
                "title": "Merge Sort Recurrence",
                "code": "# T(N) = 2 * T(N / 2) + O(N)\n# At depth d: 2^d subproblems of size N / 2^d\n# Total levels: log2(N)\n# Work per level: N\n# Total Time: O(N log N)",
                "language": "python",
                "caption": "Merge sort recursion tree derivation."
            }
        ],
        "callouts": [
            {
                "type": "tip",
                "title": "Tree Depth",
                "content": "Dividing $N$ by $b$ at each step yields a tree of depth $\\log_b N$."
            }
        ],
        "keyTakeaway": "Recurrences model divide-and-conquer algorithms via subproblem count, division factor, and merge work."
    },
    {
        "id": "day29-step2",
        "stepNumber": 2,
        "title": "The Master Theorem",
        "shortLabel": "Master Theorem",
        "type": "explanation",
        "isGated": false,
        "heading": "Instant Complexity Analysis with the 3 Master Theorem Cases",
        "subheading": "Compare subproblem creation rate against leaf work.",
        "markdownContent": [
            "The **Master Theorem** solves recurrences $T(N) = a T(N/b) + \\Theta(N^c)$ by comparing the critical exponent $\\log_b a$ against $c$:",
            "1. **Case 1 (Leaf Dominated)**: If $\\log_b a > c$, leaf work dominates: $$T(N) = \\Theta(N^{\\log_b a})$$",
            "2. **Case 2 (Balanced Work)**: If $\\log_b a = c$, all levels do equal work: $$T(N) = \\Theta(N^c \\log N)$$ *(e.g. Merge Sort: $\\log_2 2 = 1 = c \\implies O(N \\log N)$)*",
            "3. **Case 3 (Root Dominated)**: If $\\log_b a < c$, root/split work dominates: $$T(N) = \\Theta(N^c)$$"
        ],
        "snippets": [
            {
                "title": "Master Theorem Quick Checks",
                "code": "# Binary Search: T(N) = 1*T(N/2) + O(1)\n# a=1, b=2, c=0 -> log2(1) = 0 == c -> Case 2 -> O(log N)\n\n# Karatsuba Multiplication: T(N) = 3*T(N/2) + O(N)\n# a=3, b=2, c=1 -> log2(3) = 1.585 > 1 -> Case 1 -> O(N^1.585)",
                "language": "python",
                "caption": "Applying the Master Theorem across classic algorithms."
            }
        ],
        "callouts": [
            {
                "type": "deep-dive",
                "title": "When Master Theorem Doesn't Apply",
                "content": "Master Theorem only applies when subproblems are equal in size ($N/b$). It cannot solve Fibonacci ($T(N) = T(N-1) + T(N-2)$); use characteristic equations or recurrence trees instead."
            }
        ],
        "keyTakeaway": "Compare log_b(a) with c to instantly identify whether leaves, root, or all levels dominate."
    },
    {
        "id": "day29-step3",
        "stepNumber": 3,
        "title": "Master Theorem Checkpoint",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Test Your Mastery of Recurrence Relations",
        "subheading": "Classify recurrences and apply the Master Theorem.",
        "checkpoints": [
            {
                "id": "chk-d29-q1",
                "question": "What is the time complexity of the recurrence $T(N) = 4 T(N/2) + O(N)$?",
                "options": [
                    {
                        "id": "A",
                        "label": "O(N log N)"
                    },
                    {
                        "id": "B",
                        "label": "O(N^2)"
                    },
                    {
                        "id": "C",
                        "label": "O(N)"
                    },
                    {
                        "id": "D",
                        "label": "O(4^N)"
                    }
                ],
                "correctOptionId": "B",
                "explanations": {
                    "A": "Incorrect: log2(4) = 2, which is strictly greater than c = 1.",
                    "B": "Correct! a = 4, b = 2, c = 1. Critical exponent log_b(a) = log2(4) = 2. Since 2 > 1, Case 1 applies: T(N) = Theta(N^2).",
                    "C": "Incorrect: Subproblem creation rate dwarfs the linear merge work.",
                    "D": "Incorrect: Polynomial, not exponential."
                }
            },
            {
                "id": "chk-d29-q2",
                "question": "What recurrence relation represents standard Binary Search?",
                "options": [
                    {
                        "id": "A",
                        "label": "T(N) = 2 T(N/2) + O(1)"
                    },
                    {
                        "id": "B",
                        "label": "T(N) = T(N/2) + O(1)"
                    },
                    {
                        "id": "C",
                        "label": "T(N) = T(N - 1) + O(1)"
                    },
                    {
                        "id": "D",
                        "label": "T(N) = 2 T(N/2) + O(N)"
                    }
                ],
                "correctOptionId": "B",
                "explanations": {
                    "A": "Incorrect: Binary search only searches one half, not both.",
                    "B": "Correct! It creates 1 subproblem of size N/2 and performs O(1) comparison work: T(N) = T(N/2) + O(1), giving O(log N).",
                    "C": "Incorrect: It divides the search space in half, rather than subtracting 1.",
                    "D": "Incorrect: That is Merge Sort."
                }
            }
        ],
        "keyTakeaway": "T(N) = 4T(N/2) + O(N) yields O(N^2); Binary Search is T(N) = T(N/2) + O(1) -> O(log N)."
    },
    {
        "id": "day29-step4",
        "stepNumber": 4,
        "title": "Simulate Recurrence Tree Operations",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Trace Work Per Level in a Recurrence Tree",
        "subheading": "Simulate level-by-level work calculation for $T(N) = 2T(N/2) + N$.",
        "task": {
            "title": "Recurrence Tree Work Calculator",
            "instructions": [
                "Given `n = 16`, calculate the total work across all levels of the recurrence tree for $T(N) = 2T(N/2) + N$.",
                "At level 0, there is 1 node of size 16 (work: 16).",
                "At each subsequent level, node count doubles and node size halves, so work per level remains $N = 16$.",
                "The number of levels is `math.log2(n) + 1`.",
                "Compute `total_work = n * int(math.log2(n) + 1)` and print `'Total operations:', total_work`."
            ],
            "starterCode": "# Day 29 Practice: Recurrence Tree Work Calculator\nimport math\n\nn = 16\n\n# TODO: Compute levels = int(math.log2(n)) + 1\nlevels = int(math.log2(n)) + 1\n# Total work is n * levels\ntotal_work = n * levels\n\nprint(\"Total operations:\", total_work)\n",
            "solutionCode": "import math\n\nn = 16\nlevels = int(math.log2(n)) + 1\ntotal_work = n * levels\n\nprint(\"Total operations:\", total_work)\n",
            "expectedOutputPatterns": [
                "Total operations: 80"
            ],
            "hint": "Levels is log2(16) + 1 = 5 levels; 16 * 5 = 80 operations."
        },
        "keyTakeaway": "When each tree level performs equal work, total complexity is work_per_level * depth."
    },
    {
        "id": "day29-step5",
        "stepNumber": 5,
        "title": "Recurrence Relations Mastery",
        "shortLabel": "Recap",
        "type": "completion",
        "isGated": false,
        "dayNumber": 29,
        "heading": "Day 29 Complete: Recurrence Relations & Master Theorem",
        "subheading": "You have mastered recurrence modeling, the 3 Master Theorem cases, and recursion trees.",
        "recapRows": [
            {
                "concept": "Balanced Work Case",
                "naiveIntuition": "Dividing in half always gives O(log N)",
                "pythonReality": "Only if merge work is O(1); if merge work is O(N), total time is O(N log N)"
            },
            {
                "concept": "Unequal Subproblems",
                "naiveIntuition": "Master theorem works on all recursive functions",
                "pythonReality": "It only applies to equal division (N/b); unequal splits require tree summation"
            }
        ],
        "solidifiedConcepts": [
            "T(N) = aT(N/b) + f(N) Formulation",
            "Critical Exponent log_b(a)",
            "3 Master Theorem Regimes",
            "Recursion Tree Level Summation"
        ],
        "nextDayPreview": {
            "dayNumber": 30,
            "title": "Linear Recursion Fundamentals & Call Stack",
            "description": "Master base cases, recursive steps, stack frame allocation, stack unwinding, and recursion depth limits."
        }
    }
]
},
  30: {
  "dayNumber": 30,
  "title": "Divide and Conquer Paradigm",
  "topicName": "Divide & Conquer",
  "sectionId": "computational-thinking",
  "estimatedMinutes": 35,
  "difficulty": "DEVELOPING",
  "prerequisites": [
    29
  ],
  "concepts": [
    "Divide, Conquer, Combine",
    "Subproblem Independence",
    "Binary Search on Arrays",
    "Merge Sort Preview"
  ],
  "practiceSkills": [
    "Problem Partitioning",
    "Subproblem Recombination",
    "Recursive Conquering"
  ]
,
  "steps": [
    {
        "id": "day30-step1",
        "stepNumber": 1,
        "title": "The Three Pillars of Divide & Conquer",
        "shortLabel": "Divide & Conquer",
        "type": "explanation",
        "isGated": false,
        "heading": "Divide, Conquer, Combine: The Blueprint for Efficient Algorithms",
        "subheading": "A structured approach to transforming intractable problems into logarithmic layers.",
        "markdownContent": [
            "The **Divide-and-Conquer** paradigm operates in three distinct phases:",
            "1. **Divide**: Partition the problem into smaller, independent subproblems of the same type.",
            "2. **Conquer**: Recursively solve each subproblem. When subproblems become small enough (base cases), solve them directly.",
            "3. **Combine**: Merge the subproblem solutions into a solution for the original problem.",
            "For Divide-and-Conquer to be optimal, subproblems must be **independent** (non-overlapping). If subproblems overlap, Dynamic Programming is preferred to avoid redundant recomputations."
        ],
        "snippets": [
            {
                "title": "Divide and Conquer Template",
                "code": "def divide_and_conquer(problem):\n    if is_base_case(problem):\n        return solve_directly(problem)\n    \n    subproblems = divide(problem)\n    sub_solutions = [divide_and_conquer(sub) for sub in subproblems]\n    return combine(sub_solutions)",
                "language": "python",
                "caption": "Canonical Divide-and-Conquer architecture."
            }
        ],
        "callouts": [
            {
                "type": "tip",
                "title": "Subproblem Independence",
                "content": "Merge Sort and Binary Search are classic Divide-and-Conquer because left and right halves are completely independent."
            }
        ],
        "keyTakeaway": "Divide into independent subproblems, conquer recursively, and combine solutions."
    },
    {
        "id": "day30-step2",
        "stepNumber": 2,
        "title": "Fast Exponentiation (Binary Exponentiation)",
        "shortLabel": "Binary Exponentiation",
        "type": "explanation",
        "isGated": false,
        "heading": "Computing x^N in O(log N) Time Instead of O(N)",
        "subheading": "How divide-and-conquer slashes exponential loops to logarithmic time.",
        "markdownContent": [
            "Calculating $x^N$ by multiplying $x$ by itself $N$ times takes $O(N)$ operations.",
            "By Divide-and-Conquer (Binary Exponentiation):",
            "- If $N$ is even: $x^N = (x^{N/2})^2$",
            "- If $N$ is odd: $x^N = x \\cdot (x^{(N-1)/2})^2$",
            "At each step, the exponent $N$ is halved. Total multiplications drop from $N$ to **$O(\\log N)$**!",
            "This pattern is fundamental in cryptography (RSA modular exponentiation) and matrix exponentiation."
        ],
        "snippets": [
            {
                "title": "Fast Exponentiation Implementation",
                "code": "def fast_pow(x, n):\n    if n == 0:\n        return 1\n    half = fast_pow(x, n // 2)\n    if n % 2 == 0:\n        return half * half\n    else:\n        return x * half * half\n\nprint(fast_pow(2, 10)) # 1024 in only 4 recursive steps!",
                "language": "python",
                "caption": "Logarithmic power computation via binary halving."
            }
        ],
        "callouts": [
            {
                "type": "warning",
                "title": "Avoid Double Calls",
                "content": "Writing `fast_pow(x, n//2) * fast_pow(x, n//2)` calls the subproblem TWICE, destroying the $O(\\log N)$ speed and reverting to $O(N)$! Always store `half = fast_pow(...)` in a variable."
            }
        ],
        "keyTakeaway": "Binary exponentiation computes x^N in O(log N) time by squaring subproblem halves."
    },
    {
        "id": "day30-step3",
        "stepNumber": 3,
        "title": "Divide and Conquer Checkpoint",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Test Your Mastery of Divide and Conquer",
        "subheading": "Evaluate subproblem independence and binary halving.",
        "checkpoints": [
            {
                "id": "chk-d30-q1",
                "question": "Why is naive recursive Fibonacci `fib(n) = fib(n-1) + fib(n-2)` NOT an efficient Divide-and-Conquer algorithm?",
                "options": [
                    {
                        "id": "A",
                        "label": "It does not have a base case"
                    },
                    {
                        "id": "B",
                        "label": "The subproblems overlap heavily, recomputing identical values exponentially (O(2^N))"
                    },
                    {
                        "id": "C",
                        "label": "It divides by 2 instead of 3"
                    },
                    {
                        "id": "D",
                        "label": "Fibonacci numbers cannot be computed recursively"
                    }
                ],
                "correctOptionId": "B",
                "explanations": {
                    "A": "Incorrect: fib(0) and fib(1) are base cases.",
                    "B": "Correct! Divide-and-conquer requires independent subproblems. fib(n-1) and fib(n-2) overlap extensively, making memoization (DP) necessary.",
                    "C": "Incorrect: It subtracts 1 and 2.",
                    "D": "Incorrect: It can be computed recursively with memoization."
                }
            },
            {
                "id": "chk-d30-q2",
                "question": "How many multiplications does `fast_pow(x, 1024)` perform?",
                "options": [
                    {
                        "id": "A",
                        "label": "1024"
                    },
                    {
                        "id": "B",
                        "label": "10"
                    },
                    {
                        "id": "C",
                        "label": "512"
                    },
                    {
                        "id": "D",
                        "label": "2"
                    }
                ],
                "correctOptionId": "B",
                "explanations": {
                    "A": "Incorrect: That is the naive linear loop.",
                    "B": "Correct! log2(1024) = 10. The exponent halves at each step: 1024 -> 512 -> 256 -> 128 -> 64 -> 32 -> 16 -> 8 -> 4 -> 2 -> 1, taking 10 steps.",
                    "C": "Incorrect: Halving occurs recursively at all levels.",
                    "D": "Incorrect: 2^10 = 1024."
                }
            }
        ],
        "keyTakeaway": "Divide and Conquer requires independent subproblems; binary exponentiation takes log2(N) steps."
    },
    {
        "id": "day30-step4",
        "stepNumber": 4,
        "title": "Build Modular Fast Exponentiation",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Implement Modular Fast Exponentiation (pow_mod)",
        "subheading": "Compute (base^exp) % mod in O(log exp) time.",
        "task": {
            "title": "Modular Exponentiation Engine",
            "instructions": [
                "Write `mod_pow(base, exp, mod)` using divide-and-conquer.",
                "If `exp == 0`, return `1 % mod`.",
                "Compute `half = mod_pow(base, exp // 2, mod)`.",
                "If `exp % 2 == 0`, return `(half * half) % mod`; else `(base * half * half) % mod`.",
                "Test with `base = 3, exp = 13, mod = 7` and print `'Result:', result`."
            ],
            "starterCode": "# Day 30 Practice: Modular Exponentiation Engine\n\ndef mod_pow(base, exp, mod):\n    # TODO: Implement fast modular exponentiation\n    if exp == 0:\n        return 1 % mod\n    half = mod_pow(base, exp // 2, mod)\n    if exp % 2 == 0:\n        return (half * half) % mod\n    else:\n        return (base * half * half) % mod\n\nresult = mod_pow(3, 13, 7)\nprint(\"Result:\", result)\n",
            "solutionCode": "def mod_pow(base, exp, mod):\n    if exp == 0:\n        return 1 % mod\n    half = mod_pow(base, exp // 2, mod)\n    if exp % 2 == 0:\n        return (half * half) % mod\n    else:\n        return (base * half * half) % mod\n\nresult = mod_pow(3, 13, 7)\nprint(\"Result:\", result)\n",
            "expectedOutputPatterns": [
                "Result: 3"
            ],
            "hint": "3^13 % 7: 3^1=3, 3^2=2, 3^3=6, 3^6=1, 3^12=1, 3^13=3."
        },
        "keyTakeaway": "Modular exponentiation applies modulo at each halving step, preventing massive integer bit growth."
    },
    {
        "id": "day30-step5",
        "stepNumber": 5,
        "title": "Divide and Conquer Mastery",
        "shortLabel": "Recap",
        "type": "completion",
        "isGated": false,
        "dayNumber": 30,
        "heading": "Day 30 Complete: Divide and Conquer Paradigm",
        "subheading": "You have mastered divide-and-conquer decomposition, binary exponentiation, and subproblem independence.",
        "recapRows": [
            {
                "concept": "Recursive Call Storage",
                "naiveIntuition": "Calling f(n//2) * f(n//2) is the same as half * half",
                "pythonReality": "Calling f(n//2) twice creates two recursive branches, degrading O(log N) back to O(N)"
            },
            {
                "concept": "Overlapping Subproblems",
                "naiveIntuition": "All recursive problems are Divide and Conquer",
                "pythonReality": "Only problems with independent subproblems qualify; overlapping ones require DP"
            }
        ],
        "solidifiedConcepts": [
            "Divide, Conquer, Combine Framework",
            "Subproblem Independence Invariant",
            "Binary Exponentiation O(log N)",
            "Modular Reduction in Recursion"
        ],
        "nextDayPreview": {
            "dayNumber": 31,
            "title": "Branching Recursion & Tree Diagramming",
            "description": "Analyze branching recursion, tree representations of recursive calls, redundant work in Fibonacci, and work per level."
        }
    }
]
},
  31: {
  "dayNumber": 31,
  "title": "Dynamic Arrays vs Static Arrays",
  "topicName": "Array Data Structures",
  "sectionId": "computational-thinking",
  "estimatedMinutes": 30,
  "difficulty": "DEVELOPING",
  "prerequisites": [
    30
  ],
  "concepts": [
    "Static vs Dynamic Allocations",
    "Amortized Geometric Resizing",
    "Memory Locality & Cache Lines",
    "O(1) Access vs O(N) Inserts"
  ],
  "practiceSkills": [
    "Dynamic Array Simulation",
    "Amortized Cost Calculation",
    "Cache Locality Optimization"
  ]
,
  "steps": [
    {
        "id": "day31-step1",
        "stepNumber": 1,
        "title": "Static Arrays & Hardware Memory",
        "shortLabel": "Static Arrays & Hardware",
        "type": "explanation",
        "isGated": false,
        "heading": "Fixed-Size Buffers, Memory Locality, and CPU Cache Lines",
        "subheading": "Why contiguous memory buffers are the fastest data structure on modern hardware.",
        "markdownContent": [
            "A **static array** is a contiguous block of fixed-size memory allocated upfront. Because elements are adjacent in physical RAM, computing the address of element `i` is an instantaneous hardware operation: `base_address + i * element_size`.",
            "Contiguous arrays have exceptional **spatial locality**: when the CPU reads element `arr[0]`, the hardware prefetcher loads the entire 64-byte **CPU cache line** containing `arr[1]...arr[7]` into ultra-fast L1 cache.",
            "However, static arrays cannot grow. If you need more capacity, you must allocate a new, larger buffer and copy all elements over."
        ],
        "snippets": [
            {
                "title": "Hardware Address Offset Calculation",
                "code": "# Static array access is pure arithmetic:\n# address(i) = base + i * 8 bytes (on 64-bit architectures)\n# No pointer chasing, O(1) direct hardware indexing",
                "language": "python",
                "caption": "Hardware indexing via base offset."
            }
        ],
        "callouts": [
            {
                "type": "tip",
                "title": "Cache Locality Advantage",
                "content": "Iterating over a contiguous array can be 10x-50x faster than traversing a linked list of the same size due to CPU cache hits vs cache misses."
            }
        ],
        "keyTakeaway": "Contiguous array indexing is a single address calculation benefiting from CPU cache line prefetching."
    },
    {
        "id": "day31-step2",
        "stepNumber": 2,
        "title": "Dynamic Resizing & Geometric Amortization",
        "shortLabel": "Amortized Resizing",
        "type": "explanation",
        "isGated": false,
        "heading": "Why Dynamic Arrays Double Capacity: Geometric Growth vs Arithmetic Growth",
        "subheading": "The mathematical proof of amortized O(1) append.",
        "markdownContent": [
            "A **dynamic array** wraps a static buffer. When full, it allocates a new buffer of size $2 \\times$ (or $1.5 \\times$) capacity and copies existing elements.",
            "If capacity grew arithmetically (+10 each time), copying $N$ elements would cost $O(N^2)$ total, making each append cost $O(N)$.",
            "Under **geometric growth** (doubling), resizing occurs at sizes $1, 2, 4, 8, ..., N$. The total elements copied across all resizings is: $$1 + 2 + 4 + ... + N = 2N - 1 < 2N$$",
            "Dividing $2N$ copies across $N$ total appends yields $\\le 2$ copies per append\u2014proving **amortized $O(1)$** cost!"
        ],
        "snippets": [
            {
                "title": "Geometric Amortization Proof",
                "code": "# N appends trigger resizes at 1, 2, 4, 8, 16... N\n# Total copy operations: sum_{i=0}^{k} 2^i = 2^(k+1) - 1 ~ 2N\n# Amortized work per append: 2N / N = O(1) constant!",
                "language": "python",
                "caption": "Geometric series proving amortized O(1) complexity."
            }
        ],
        "callouts": [
            {
                "type": "warning",
                "title": "Fixed Over-Allocation Penalty",
                "content": "Appending to an array with fixed additions (`capacity += 1`) degrades total append time from $O(N)$ to catastrophic $O(N^2)$."
            }
        ],
        "keyTakeaway": "Geometric capacity scaling (multiplying by a factor) guarantees amortized O(1) insertion."
    },
    {
        "id": "day31-step3",
        "stepNumber": 3,
        "title": "Arrays Checkpoint",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Test Your Mastery of Array Architecture",
        "subheading": "Evaluate cache locality and resizing mechanics.",
        "checkpoints": [
            {
                "id": "chk-d31-q1",
                "question": "Why does doubling array capacity give amortized O(1) append, whereas increasing capacity by +100 gives O(N) append?",
                "options": [
                    {
                        "id": "A",
                        "label": "Doubling is supported by CPU hardware instructions"
                    },
                    {
                        "id": "B",
                        "label": "Geometric doubling spreads infrequent O(N) copies over exponentially many O(1) inserts, bounding total copies to 2N"
                    },
                    {
                        "id": "C",
                        "label": "Doubling avoids memory allocation"
                    },
                    {
                        "id": "D",
                        "label": "There is no difference in asymptotic complexity"
                    }
                ],
                "correctOptionId": "B",
                "explanations": {
                    "A": "Incorrect: It is a mathematical property of geometric series, not a CPU instruction.",
                    "B": "Correct! Total copies for doubling is bounded by 2N, yielding 2N/N = O(1) per insert. Fixed additions copy N elements every 100 inserts, yielding O(N^2)/N = O(N) per insert.",
                    "C": "Incorrect: Resizing still allocates memory.",
                    "D": "Incorrect: One is O(1) amortized, the other is O(N)."
                }
            },
            {
                "id": "chk-d31-q2",
                "question": "What primary hardware mechanism makes iterating an array faster than traversing a linked list?",
                "options": [
                    {
                        "id": "A",
                        "label": "CPU branch prediction"
                    },
                    {
                        "id": "B",
                        "label": "Spatial locality and CPU cache line prefetching"
                    },
                    {
                        "id": "C",
                        "label": "Instruction pipelining only"
                    },
                    {
                        "id": "D",
                        "label": "Virtual memory paging"
                    }
                ],
                "correctOptionId": "B",
                "explanations": {
                    "A": "Incorrect: Branch prediction predicts conditionals.",
                    "B": "Correct! Contiguous memory allows hardware prefetchers to load entire 64-byte cache lines, reducing high-latency RAM round-trips.",
                    "C": "Incorrect: Pipelining benefits both, but memory latency dominates.",
                    "D": "Incorrect: Paging handles OS virtual memory."
                }
            }
        ],
        "keyTakeaway": "Geometric doubling yields amortized O(1) append; spatial locality optimizes CPU cache performance."
    },
    {
        "id": "day31-step4",
        "stepNumber": 4,
        "title": "Simulate Dynamic Resizing",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Track Resizing Events in a Dynamic Array Buffer",
        "subheading": "Simulate a dynamic array and count how many elements are copied during growth.",
        "task": {
            "title": "Dynamic Array Capacity Simulator",
            "instructions": [
                "Initialize `capacity = 1`, `size = 0`, and `total_copies = 0`.",
                "Simulate appending 8 elements (values 1 through 8).",
                "When `size == capacity`, double capacity: `capacity *= 2`, and add the old `size` to `total_copies`.",
                "Increment `size += 1` on each append.",
                "Print `'Final capacity:', capacity` and `'Total elements copied:', total_copies`."
            ],
            "starterCode": "# Day 31 Practice: Dynamic Array Capacity Simulator\ncapacity = 1\nsize = 0\ntotal_copies = 0\n\nfor val in range(1, 9):\n    if size == capacity:\n        total_copies += size\n        capacity *= 2\n    size += 1\n\nprint(\"Final capacity:\", capacity)\nprint(\"Total elements copied:\", total_copies)\n",
            "solutionCode": "capacity = 1\nsize = 0\ntotal_copies = 0\n\nfor val in range(1, 9):\n    if size == capacity:\n        total_copies += size\n        capacity *= 2\n    size += 1\n\nprint(\"Final capacity:\", capacity)\nprint(\"Total elements copied:\", total_copies)\n",
            "expectedOutputPatterns": [
                "Final capacity: 8",
                "Total elements copied: 7"
            ],
            "hint": "Resizes happen at size 1 (1 copy), 2 (2 copies), 4 (4 copies) -> Total = 7 copies for 8 items (< 2N)."
        },
        "keyTakeaway": "Total copies during geometric doubling remain strictly less than input size N."
    },
    {
        "id": "day31-step5",
        "stepNumber": 5,
        "title": "Dynamic Arrays Mastery",
        "shortLabel": "Recap",
        "type": "completion",
        "isGated": false,
        "dayNumber": 31,
        "heading": "Day 31 Complete: Dynamic Arrays vs Static Arrays",
        "subheading": "You have mastered contiguous memory layout, CPU cache locality, and geometric amortized analysis.",
        "recapRows": [
            {
                "concept": "Resizing Overhead",
                "naiveIntuition": "Every append has an unpredictable execution time",
                "pythonReality": "Resizes are rare; across N appends, amortized time is constant O(1)"
            },
            {
                "concept": "Cache Locality",
                "naiveIntuition": "Linked lists and arrays have identical sequential access speed",
                "pythonReality": "Arrays are dramatically faster because adjacent memory loads into CPU cache lines"
            }
        ],
        "solidifiedConcepts": [
            "Spatial Locality & Cache Lines",
            "Geometric Doubling Mathematics",
            "Amortized O(1) Proof",
            "Static vs Dynamic Buffer Tradeoffs"
        ],
        "nextDayPreview": {
            "dayNumber": 32,
            "title": "Tail Recursion & State Accumulators",
            "description": "Understand tail calls, accumulator parameters, transforming recursion to iteration, and Python recursion limitations."
        }
    }
]
},
  32: {
  "dayNumber": 32,
  "title": "Prefix Sums & Range Queries (1D)",
  "topicName": "Prefix Sums",
  "sectionId": "computational-thinking",
  "estimatedMinutes": 30,
  "difficulty": "DEVELOPING",
  "prerequisites": [
    31
  ],
  "concepts": [
    "Prefix Sum Array",
    "O(1) Range Queries",
    "1-based Indexing Invariant",
    "Subarray Sum Equals K Preview"
  ],
  "practiceSkills": [
    "Prefix Array Construction",
    "O(1) Range Sum Querying",
    "Boundary Off-by-One Avoidance"
  ]
,
  "steps": [
    {
        "id": "day32-step1",
        "stepNumber": 1,
        "title": "The Power of Prefix Sums",
        "shortLabel": "Prefix Sums",
        "type": "explanation",
        "isGated": false,
        "heading": "Transforming O(N) Range Sum Queries into O(1) Instant Lookups",
        "subheading": "Precompute cumulative sums once to answer any range query in constant time.",
        "markdownContent": [
            "If you are given an array of size $N$ and asked to answer $Q$ range sum queries (`sum(arr[L:R+1])`), the naive approach sums the elements in $O(N)$ per query, taking $O(Q \\times N)$ total time.",
            "By precomputing a **Prefix Sum Array** in $O(N)$ time, every subsequent range query is answered in **$O(1)$ constant time**, dropping total complexity to **$O(N + Q)$**!",
            "Let `prefix[i]` be the sum of the first `i` elements: `prefix[i] = prefix[i - 1] + arr[i - 1]`. The sum of any range from index `L` to `R` (inclusive) is simply: $$\\text{sum}(L, R) = \\text{prefix}[R + 1] - \\text{prefix}[L]$$"
        ],
        "snippets": [
            {
                "title": "1-Indexed Prefix Sum Array",
                "code": "arr = [3, 1, 4, 1, 5, 9]\nn = len(arr)\n# 1-indexed prefix sum array of size n + 1 (prefix[0] = 0)\npref = [0] * (n + 1)\nfor i in range(n):\n    pref[i + 1] = pref[i] + arr[i]\n# pref: [0, 3, 4, 8, 9, 14, 23]\n\n# Query sum from index 1 to 4 (values: 1, 4, 1, 5 -> sum = 11):\n# pref[4 + 1] - pref[1] = pref[5] - pref[1] = 14 - 3 = 11 (O(1)!)\nprint(pref[5] - pref[1]) # 11",
                "language": "python",
                "caption": "Constructing and querying 1-indexed prefix sums."
            }
        ],
        "callouts": [
            {
                "type": "tip",
                "title": "Why 1-Based Prefix Arrays?",
                "content": "Setting `prefix[0] = 0` eliminates messy edge cases when querying from index 0 (`L = 0`). `prefix[R + 1] - prefix[0]` works without an `if L == 0` check."
            }
        ],
        "keyTakeaway": "Prefix sums preprocess an array in O(N) time to answer any range sum query in O(1) time."
    },
    {
        "id": "day32-step2",
        "stepNumber": 2,
        "title": "Cumulative State & Prefix Invariants",
        "shortLabel": "Prefix Invariants",
        "type": "explanation",
        "isGated": false,
        "heading": "Extending Prefix Sums to Frequencies, Products, and Parity",
        "subheading": "Apply the prefix pattern beyond simple addition.",
        "markdownContent": [
            "The prefix concept applies to any associative, invertible operation:",
            "- **Prefix Products**: `prefix_prod[i]` for range products (guarding against zeroes).",
            "- **Prefix XOR**: Range XOR queries: `xor(L, R) = pref[R + 1] ^ pref[L]` (used in range query problems).",
            "- **Prefix Frequencies**: Counting character occurrences within ranges in $O(1)$ time.",
            "- **Subarray Sum Equals K**: If `pref[j] - pref[i] == k`, then `pref[i] == pref[j] - k`. Combining prefix sums with a hash map finds target sum subarrays in $O(N)$ time!"
        ],
        "snippets": [
            {
                "title": "Prefix XOR Invariant",
                "code": "# Because X ^ X == 0:\n# pref[R + 1] ^ pref[L] cancels out all elements before L,\n# leaving exact range XOR arr[L] ^ ... ^ arr[R] in O(1) time!",
                "language": "python",
                "caption": "Invertible operations with prefix arrays."
            }
        ],
        "callouts": [
            {
                "type": "warning",
                "title": "Static Arrays Only",
                "content": "Standard prefix sum arrays are designed for **static** arrays. If array elements update frequently, recomputing the prefix sum takes $O(N)$. For dynamic range updates and queries, use a Binary Indexed Tree (Fenwick) or Segment Tree."
            }
        ],
        "keyTakeaway": "Prefix precomputation applies to any invertible operation; combined with hash maps it finds target subarrays."
    },
    {
        "id": "day32-step3",
        "stepNumber": 3,
        "title": "Prefix Sums Checkpoint",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Test Your Mastery of Prefix Sums",
        "subheading": "Calculate range query formula and identify off-by-one errors.",
        "checkpoints": [
            {
                "id": "chk-d32-q1",
                "question": "Given `arr = [2, 3, 5, 7, 11]` and 1-indexed `pref = [0, 2, 5, 10, 17, 28]`, how do you compute `sum(arr[1:4])` (indices 1 to 3 inclusive: 3 + 5 + 7)?",
                "options": [
                    {
                        "id": "A",
                        "label": "pref[4] - pref[1]"
                    },
                    {
                        "id": "B",
                        "label": "pref[3] - pref[0]"
                    },
                    {
                        "id": "C",
                        "label": "pref[4] - pref[2]"
                    },
                    {
                        "id": "D",
                        "label": "pref[3] - pref[1]"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Formula is pref[R + 1] - pref[L]. For L = 1 and R = 3: pref[3 + 1] - pref[1] = pref[4] - pref[1] = 17 - 2 = 15 (3 + 5 + 7 = 15).",
                    "B": "Incorrect: That would calculate range from index 0 to 2.",
                    "C": "Incorrect: Subtracting pref[2] would exclude index 1.",
                    "D": "Incorrect: Missing boundary."
                }
            },
            {
                "id": "chk-d32-q2",
                "question": "What is the total time complexity to answer Q range queries on an array of size N using prefix sums?",
                "options": [
                    {
                        "id": "A",
                        "label": "O(N * Q)"
                    },
                    {
                        "id": "B",
                        "label": "O(N + Q)"
                    },
                    {
                        "id": "C",
                        "label": "O(Q log N)"
                    },
                    {
                        "id": "D",
                        "label": "O(N log N)"
                    }
                ],
                "correctOptionId": "B",
                "explanations": {
                    "A": "Incorrect: That is the naive un-preprocessed time.",
                    "B": "Correct! Building the prefix array takes O(N) preprocessing, and each of the Q queries takes O(1) time. Total time: O(N + Q).",
                    "C": "Incorrect: Binary search is not needed for range lookups.",
                    "D": "Incorrect: Sorting is not performed."
                }
            }
        ],
        "keyTakeaway": "Range sum from L to R is pref[R + 1] - pref[L]; total complexity for Q queries is O(N + Q)."
    },
    {
        "id": "day32-step4",
        "stepNumber": 4,
        "title": "Build Range Sum Query Engine",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Implement a RangeSumQuery Class",
        "subheading": "Create a class that precomputes prefix sums and answers range queries in O(1).",
        "task": {
            "title": "Range Sum Query Engine",
            "instructions": [
                "Build class `NumArray` with `__init__(self, nums)`.",
                "Build a 1-indexed prefix array `self.pref` of size `len(nums) + 1` with `self.pref[0] = 0`.",
                "Implement `sum_range(self, left, right)` returning `self.pref[right + 1] - self.pref[left]`.",
                "Test with `nums = [-2, 0, 3, -5, 2, -1]`.",
                "Query `sum_range(0, 2)` (should be 1) and `sum_range(2, 5)` (should be -1).",
                "Print `'Query 1:', q1` and `'Query 2:', q2`."
            ],
            "starterCode": "# Day 32 Practice: Range Sum Query Engine\n\nclass NumArray:\n    def __init__(self, nums):\n        n = len(nums)\n        self.pref = [0] * (n + 1)\n        for i in range(n):\n            self.pref[i + 1] = self.pref[i] + nums[i]\n\n    def sum_range(self, left, right):\n        # TODO: Return range sum in O(1) time\n        return self.pref[right + 1] - self.pref[left]\n\nobj = NumArray([-2, 0, 3, -5, 2, -1])\nq1 = obj.sum_range(0, 2)\nq2 = obj.sum_range(2, 5)\n\nprint(\"Query 1:\", q1)\nprint(\"Query 2:\", q2)\n",
            "solutionCode": "class NumArray:\n    def __init__(self, nums):\n        n = len(nums)\n        self.pref = [0] * (n + 1)\n        for i in range(n):\n            self.pref[i + 1] = self.pref[i] + nums[i]\n\n    def sum_range(self, left, right):\n        return self.pref[right + 1] - self.pref[left]\n\nobj = NumArray([-2, 0, 3, -5, 2, -1])\nq1 = obj.sum_range(0, 2)\nq2 = obj.sum_range(2, 5)\n\nprint(\"Query 1:\", q1)\nprint(\"Query 2:\", q2)\n",
            "expectedOutputPatterns": [
                "Query 1: 1",
                "Query 2: -1"
            ],
            "hint": "Use `self.pref[right + 1] - self.pref[left]` to answer range sum queries in O(1) time."
        },
        "keyTakeaway": "1-indexed prefix sums eliminate edge-case branches and provide instant range answers."
    },
    {
        "id": "day32-step5",
        "stepNumber": 5,
        "title": "Prefix Sums Mastery",
        "shortLabel": "Recap",
        "type": "completion",
        "isGated": false,
        "dayNumber": 32,
        "heading": "Day 32 Complete: Prefix Sums & Range Queries (1D)",
        "subheading": "You have mastered prefix sum construction, 1-indexed padding, and O(1) range query algebra.",
        "recapRows": [
            {
                "concept": "Query Bounds",
                "naiveIntuition": "Range sum is prefix[R] - prefix[L]",
                "pythonReality": "To include index R, you must subtract from prefix[R + 1] with 1-indexing"
            },
            {
                "concept": "Dynamic Updates",
                "naiveIntuition": "Prefix sums are great when array values change frequently",
                "pythonReality": "Updating a single value takes O(N) to recompute prefix sums; use Fenwick trees for dynamic arrays"
            }
        ],
        "solidifiedConcepts": [
            "1-Indexed Prefix Array Convention",
            "O(1) Range Formula: pref[R+1] - pref[L]",
            "O(N + Q) Query Amortization",
            "Associative/Invertible Operation Extensions"
        ],
        "nextDayPreview": {
            "dayNumber": 33,
            "title": "Divide & Conquer Master Theorem",
            "description": "Formulate recurrence relations and apply the Master Theorem to divide-and-conquer recurrences T(n) = aT(n/b) + f(n)."
        }
    }
]
},
  33: {
  "dayNumber": 33,
  "title": "2D Prefix Sums & Submatrix Queries",
  "topicName": "2D Prefix Sums",
  "sectionId": "computational-thinking",
  "estimatedMinutes": 35,
  "difficulty": "DEVELOPING",
  "prerequisites": [
    32
  ],
  "concepts": [
    "Inclusion-Exclusion Principle",
    "2D Prefix Table Construction",
    "O(1) Submatrix Sum Queries",
    "Boundary Invariants"
  ],
  "practiceSkills": [
    "2D Prefix Matrix Construction",
    "Inclusion-Exclusion Query Formulation",
    "Submatrix Area Calculation"
  ]
,
  "steps": [
    {
        "id": "day33-step1",
        "stepNumber": 1,
        "title": "The Inclusion-Exclusion Principle in 2D",
        "shortLabel": "2D Prefix Concept",
        "type": "explanation",
        "isGated": false,
        "heading": "Extending Prefix Sums to 2D Grids with Inclusion-Exclusion",
        "subheading": "Answer submatrix sum queries in O(1) time using area arithmetic.",
        "markdownContent": [
            "Given an $R \\times C$ matrix, we construct a 2D prefix table `P` of size $(R + 1) \\times (C + 1)$, where `P[r][c]` stores the sum of all cells in the submatrix from $(0, 0)$ down to $(r - 1, c - 1)$.",
            "To construct `P` in $O(R \\times C)$ time using the **Inclusion-Exclusion Principle**:",
            "$$P[r][c] = \\text{matrix}[r-1][c-1] + P[r-1][c] + P[r][c-1] - P[r-1][c-1]$$",
            "Notice that adding the rectangle above and the rectangle to the left double-counts the top-left diagonal rectangle, so we subtract $P[r-1][c-1]$ once."
        ],
        "snippets": [
            {
                "title": "2D Prefix Construction",
                "code": "R, C = len(grid), len(grid[0])\npref = [[0] * (C + 1) for _ in range(R + 1)]\nfor r in range(R):\n    for c in range(C):\n        pref[r+1][c+1] = grid[r][c] + pref[r][c+1] + pref[r+1][c] - pref[r][c]",
                "language": "python",
                "caption": "Constructing the 2D prefix matrix."
            }
        ],
        "callouts": [
            {
                "type": "tip",
                "title": "Zero Padding Row & Column",
                "content": "The extra row 0 and column 0 of zeroes handles edges cleanly, preventing index-out-of-bounds checks."
            }
        ],
        "keyTakeaway": "2D prefix tables precompute areas in O(R*C) time using the Inclusion-Exclusion Principle."
    },
    {
        "id": "day33-step2",
        "stepNumber": 2,
        "title": "O(1) Submatrix Range Queries",
        "shortLabel": "Submatrix Query",
        "type": "explanation",
        "isGated": false,
        "heading": "Querying any Submatrix (r1, c1) to (r2, c2) in Constant Time",
        "subheading": "Deriving the 4-corner formula for instant submatrix sums.",
        "markdownContent": [
            "To query the sum of the submatrix spanning from top-left $(r_1, c_1)$ to bottom-right $(r_2, c_2)$ (inclusive):",
            "1. Start with the entire rectangle from $(0, 0)$ to $(r_2, c_2)$: `P[r2 + 1][c2 + 1]`.",
            "2. Subtract the area above the target submatrix: `P[r1][c2 + 1]`.",
            "3. Subtract the area to the left of the target submatrix: `P[r2 + 1][c1]`.",
            "4. The top-left corner was subtracted twice! Add it back once: `P[r1][c1]`.",
            "$$\\text{Sum} = P[r_2+1][c_2+1] - P[r_1][c_2+1] - P[r_2+1][c_1] + P[r_1][c_1]$$"
        ],
        "snippets": [
            {
                "title": "O(1) Submatrix Query Formula",
                "code": "def query_submatrix(pref, r1, c1, r2, c2):\n    return pref[r2+1][c2+1] - pref[r1][c2+1] - pref[r2+1][c1] + pref[r1][c1]",
                "language": "python",
                "caption": "The 4-term Inclusion-Exclusion query formula."
            }
        ],
        "callouts": [
            {
                "type": "warning",
                "title": "Coordinates Ordering",
                "content": "Ensure $r_1 \\le r_2$ and $c_1 \\le c_2$. If coordinates are reversed, the formula yields corrupted values."
            }
        ],
        "keyTakeaway": "Submatrix sum = BottomRight - TopStrip - LeftStrip + TopLeftOverlap in O(1) time."
    },
    {
        "id": "day33-step3",
        "stepNumber": 3,
        "title": "2D Prefix Checkpoint",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Test Your Understanding of 2D Prefix Sums",
        "subheading": "Verify Inclusion-Exclusion terms and submatrix coordinates.",
        "checkpoints": [
            {
                "id": "chk-d33-q1",
                "question": "Why do we ADD `pref[r1][c1]` back in the submatrix query formula?",
                "options": [
                    {
                        "id": "A",
                        "label": "Because the cell at (r1, c1) was omitted"
                    },
                    {
                        "id": "B",
                        "label": "Because it was subtracted twice: once in the top strip and once in the left strip"
                    },
                    {
                        "id": "C",
                        "label": "To account for 1-based indexing offsets"
                    },
                    {
                        "id": "D",
                        "label": "To handle negative values in the matrix"
                    }
                ],
                "correctOptionId": "B",
                "explanations": {
                    "A": "Incorrect: Inclusion-Exclusion corrects overlapping regions.",
                    "B": "Correct! Subtracting the top region (P[r1][c2+1]) and left region (P[r2+1][c1]) both subtract the common overlapping region P[r1][c1]. Adding it back once restores mathematical balance.",
                    "C": "Incorrect: Indexing handles offsets, but the + term is algebraic.",
                    "D": "Incorrect: The formula holds for all integer values."
                }
            },
            {
                "id": "chk-d33-q2",
                "question": "What is the time complexity to answer Q submatrix queries on an R x C grid using 2D prefix sums?",
                "options": [
                    {
                        "id": "A",
                        "label": "O(R * C * Q)"
                    },
                    {
                        "id": "B",
                        "label": "O(R * C + Q)"
                    },
                    {
                        "id": "C",
                        "label": "O(Q log(R * C))"
                    },
                    {
                        "id": "D",
                        "label": "O(R + C + Q)"
                    }
                ],
                "correctOptionId": "B",
                "explanations": {
                    "A": "Incorrect: That is the un-precomputed naive approach.",
                    "B": "Correct! Preprocessing the table takes O(R * C), and each query executes in O(1) time via the 4-term arithmetic formula: O(R * C + Q).",
                    "C": "Incorrect: No binary search is involved.",
                    "D": "Incorrect: Filling the 2D grid requires visiting all R*C cells."
                }
            }
        ],
        "keyTakeaway": "Adding back pref[r1][c1] balances the double-subtraction; Q queries cost O(R*C + Q)."
    },
    {
        "id": "day33-step4",
        "stepNumber": 4,
        "title": "Build a 2D Submatrix Query Engine",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Implement NumMatrix for 2D Range Queries",
        "subheading": "Build a 2D matrix query class supporting O(1) area lookups.",
        "task": {
            "title": "Submatrix Query Engine",
            "instructions": [
                "Given `matrix = [[3, 0, 1], [5, 6, 3], [1, 2, 0]]`.",
                "Precompute 2D prefix table `self.p` of dimensions 4x4.",
                "Implement `sum_region(r1, c1, r2, c2)`.",
                "Query the region from $(1, 1)$ to $(2, 2)$ (cells: 6, 3, 2, 0 -> sum = 11).",
                "Print `'Submatrix sum:', result`."
            ],
            "starterCode": "# Day 33 Practice: Submatrix Query Engine\n\nclass NumMatrix:\n    def __init__(self, matrix):\n        R, C = len(matrix), len(matrix[0])\n        self.p = [[0] * (C + 1) for _ in range(R + 1)]\n        for r in range(R):\n            for c in range(C):\n                self.p[r+1][c+1] = matrix[r][c] + self.p[r][c+1] + self.p[r+1][c] - self.p[r][c]\n\n    def sum_region(self, r1, c1, r2, c2):\n        # TODO: Compute submatrix sum in O(1)\n        return self.p[r2+1][c2+1] - self.p[r1][c2+1] - self.p[r2+1][c1] + self.p[r1][c1]\n\ngrid = [\n    [3, 0, 1],\n    [5, 6, 3],\n    [1, 2, 0]\n]\nobj = NumMatrix(grid)\nresult = obj.sum_region(1, 1, 2, 2)\nprint(\"Submatrix sum:\", result)\n",
            "solutionCode": "class NumMatrix:\n    def __init__(self, matrix):\n        R, C = len(matrix), len(matrix[0])\n        self.p = [[0] * (C + 1) for _ in range(R + 1)]\n        for r in range(R):\n            for c in range(C):\n                self.p[r+1][c+1] = matrix[r][c] + self.p[r][c+1] + self.p[r+1][c] - self.p[r][c]\n\n    def sum_region(self, r1, c1, r2, c2):\n        return self.p[r2+1][c2+1] - self.p[r1][c2+1] - self.p[r2+1][c1] + self.p[r1][c1]\n\ngrid = [\n    [3, 0, 1],\n    [5, 6, 3],\n    [1, 2, 0]\n]\nobj = NumMatrix(grid)\nresult = obj.sum_region(1, 1, 2, 2)\nprint(\"Submatrix sum:\", result)\n",
            "expectedOutputPatterns": [
                "Submatrix sum: 11"
            ],
            "hint": "Cells (1,1)=6, (1,2)=3, (2,1)=2, (2,2)=0 -> 6 + 3 + 2 + 0 = 11."
        },
        "keyTakeaway": "2D prefix matrices allow constant-time computation of any rectangular subregion."
    },
    {
        "id": "day33-step5",
        "stepNumber": 5,
        "title": "2D Prefix Sums Mastery",
        "shortLabel": "Recap",
        "type": "completion",
        "isGated": false,
        "dayNumber": 33,
        "heading": "Day 33 Complete: 2D Prefix Sums & Submatrix Queries",
        "subheading": "You have mastered 2D Inclusion-Exclusion, table construction, and instant submatrix queries.",
        "recapRows": [
            {
                "concept": "Overlapping Areas",
                "naiveIntuition": "Summing submatrix requires adding elements cell-by-cell",
                "pythonReality": "Inclusion-Exclusion calculates the area using only 4 corner values in O(1)"
            },
            {
                "concept": "Boundary Zero Padding",
                "naiveIntuition": "Use R x C prefix matrix directly",
                "pythonReality": "(R+1) x (C+1) with zeroes on row/col 0 avoids complex edge conditions"
            }
        ],
        "solidifiedConcepts": [
            "2D Inclusion-Exclusion Formula",
            "(R+1) x (C+1) Table Padding",
            "O(1) Submatrix Sum Querying",
            "O(R*C + Q) Complexity Budget"
        ],
        "nextDayPreview": {
            "dayNumber": 34,
            "title": "Invariant Design & Loop Verification",
            "description": "Formalize algorithm correctness using loop invariants: initialization, maintenance, and termination proof techniques."
        }
    }
]
},
  34: {
  "dayNumber": 34,
  "title": "Difference Arrays & Range Updates",
  "topicName": "Difference Arrays",
  "sectionId": "computational-thinking",
  "estimatedMinutes": 35,
  "difficulty": "DEVELOPING",
  "prerequisites": [
    33
  ],
  "concepts": [
    "Range Update Operations",
    "O(1) Boundary Marking",
    "Prefix Sum Reconstruction",
    "Sweep-line Foundations"
  ],
  "practiceSkills": [
    "Difference Array Construction",
    "O(1) Range Modification",
    "Cumulative Prefix Reconstruction"
  ]
,
  "steps": [
    {
        "id": "day34-step1",
        "stepNumber": 1,
        "title": "The Difference Array Invariant",
        "shortLabel": "Difference Array",
        "type": "explanation",
        "isGated": false,
        "heading": "Transforming O(N) Range Updates into O(1) Boundary Marks",
        "subheading": "Apply hundreds of range modifications in constant time per update.",
        "markdownContent": [
            "Suppose you have an array of zeroes of length $N$ and need to execute $K$ range update operations: *'Add $V$ to all elements from index $L$ to $R$'*.",
            "Applying each update with a loop takes $O(N)$ per operation ($O(K \\times N)$ total).",
            "A **Difference Array** $D$ is defined such that $D[i] = A[i] - A[i-1]$ (with $D[0] = A[0]$). Taking the prefix sum of $D$ reconstructs the original array $A$!",
            "Crucially, adding $V$ to range $[L, R]$ changes only **TWO elements** in the difference array:",
            "1. `D[L] += V` (starts the boost of $+V$ at index $L$)",
            "2. `D[R + 1] -= V` (cancels the boost after index $R$)",
            "Each range update executes in **$O(1)$ constant time**!"
        ],
        "snippets": [
            {
                "title": "Difference Array Range Update",
                "code": "n = 5\ndiff = [0] * (n + 1)\n\n# Range update: Add 10 to range [1, 3] in O(1)\nL, R, V = 1, 3, 10\ndiff[L] += V       # diff[1] += 10\ndiff[R + 1] -= V   # diff[4] -= 10\n\n# Reconstruct final array via prefix sum in O(N)\narr = [0] * n\ncurr = 0\nfor i in range(n):\n    curr += diff[i]\n    arr[i] = curr\nprint(arr) # [0, 10, 10, 10, 0]",
                "language": "python",
                "caption": "O(1) marking and O(N) prefix sum reconstruction."
            }
        ],
        "callouts": [
            {
                "type": "tip",
                "title": "Inverse of Prefix Sums",
                "content": "Difference arrays are the exact mathematical inverse of prefix sums. Prefix sum converts point updates to range queries; difference arrays convert range updates to point updates."
            }
        ],
        "keyTakeaway": "Add V at L, subtract V at R+1; taking prefix sums reconstructs the updated array in O(N) time."
    },
    {
        "id": "day34-step2",
        "stepNumber": 2,
        "title": "Flight Bookings & Sweep-Line Preview",
        "shortLabel": "Sweep-Line Preview",
        "type": "explanation",
        "isGated": false,
        "heading": "Corporate Flight Bookings & Meeting Room Overlap",
        "subheading": "How difference arrays solve interval overlap problems.",
        "markdownContent": [
            "Consider the classic problem: Given flight booking reservations `[first, last, seats]`, determine the total seats reserved on each flight.",
            "Instead of filling seats seat-by-seat, mark `diff[first - 1] += seats` and `diff[last] -= seats`.",
            "When all $K$ updates are marked, a single $O(N)$ cumulative sweep yields the final answer.",
            "Total time is **$O(N + K)$** instead of $O(N \\times K)$, effortlessly handling $K = 10^5$ operations."
        ],
        "snippets": [
            {
                "title": "Flight Bookings Solution",
                "code": "def corp_flight_bookings(bookings, n):\n    diff = [0] * (n + 1)\n    for first, last, seats in bookings:\n        diff[first - 1] += seats\n        diff[last] -= seats\n    # Prefix sum sweep\n    res = [0] * n\n    curr = 0\n    for i in range(n):\n        curr += diff[i]\n        res[i] = curr\n    return res",
                "language": "python",
                "caption": "Linear flight booking resolution via difference array."
            }
        ],
        "callouts": [
            {
                "type": "warning",
                "title": "R + 1 Boundary Check",
                "content": "Always size the difference array to $N + 1$ so that when an update reaches the end ($R = N - 1$), the decrement at $R + 1 = N$ does not throw an IndexError."
            }
        ],
        "keyTakeaway": "Difference arrays solve batch interval modifications in O(N + K) total time."
    },
    {
        "id": "day34-step3",
        "stepNumber": 3,
        "title": "Difference Arrays Checkpoint",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Test Your Mastery of Difference Arrays",
        "subheading": "Evaluate boundary modifications and reconstruction mechanics.",
        "checkpoints": [
            {
                "id": "chk-d34-q1",
                "question": "To add value V to all elements from index 2 to 5 in an array of size 10, what modifications are made to difference array D?",
                "options": [
                    {
                        "id": "A",
                        "label": "D[2] += V and D[5] -= V"
                    },
                    {
                        "id": "B",
                        "label": "D[2] += V and D[6] -= V"
                    },
                    {
                        "id": "C",
                        "label": "D[1] += V and D[5] -= V"
                    },
                    {
                        "id": "D",
                        "label": "D[2] += V and D[6] += V"
                    }
                ],
                "correctOptionId": "B",
                "explanations": {
                    "A": "Incorrect: Subtracting at index 5 would cancel the value at index 5 itself, omitting it.",
                    "B": "Correct! Increment at L = 2 and decrement at R + 1 = 5 + 1 = 6 so that indices 2, 3, 4, 5 receive the added value.",
                    "C": "Incorrect: L = 2, not 1.",
                    "D": "Incorrect: The cancellation must be a subtraction (-= V)."
                }
            },
            {
                "id": "chk-d34-q2",
                "question": "What is the time complexity to perform K range updates and reconstruct an array of length N using a difference array?",
                "options": [
                    {
                        "id": "A",
                        "label": "O(N * K)"
                    },
                    {
                        "id": "B",
                        "label": "O(N + K)"
                    },
                    {
                        "id": "C",
                        "label": "O(K log N)"
                    },
                    {
                        "id": "D",
                        "label": "O(N log K)"
                    }
                ],
                "correctOptionId": "B",
                "explanations": {
                    "A": "Incorrect: That is the un-optimized loop approach.",
                    "B": "Correct! Each of the K updates takes O(1) time (2 point modifications), and the final prefix sum sweep takes O(N). Total: O(N + K).",
                    "C": "Incorrect: Difference arrays use direct indexing without trees.",
                    "D": "Incorrect: Reconstruction is a single linear pass."
                }
            }
        ],
        "keyTakeaway": "Range update modifies D[L] += V and D[R+1] -= V in O(1); total time for K updates is O(N + K)."
    },
    {
        "id": "day34-step4",
        "stepNumber": 4,
        "title": "Range Addition with Difference Array",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Apply Multiple Range Increments in O(1) Per Update",
        "subheading": "Execute batch updates on an array and reconstruct the final values.",
        "task": {
            "title": "Range Addition Engine",
            "instructions": [
                "Given `n = 5` and `updates = [[1, 3, 2], [2, 4, 3], [0, 2, -2]]` where each update is `[start, end, val]`.",
                "Initialize `diff = [0] * (n + 1)`.",
                "Apply all updates in $O(1)$ per update using the difference array technique.",
                "Reconstruct the array `res` using cumulative summation.",
                "Print `'Final array:', res`."
            ],
            "starterCode": "# Day 34 Practice: Range Addition Engine\nn = 5\nupdates = [[1, 3, 2], [2, 4, 3], [0, 2, -2]]\n\ndiff = [0] * (n + 1)\n\n# TODO 1: Apply updates to diff in O(1)\nfor start, end, val in updates:\n    diff[start] += val\n    diff[end + 1] -= val\n\n# TODO 2: Reconstruct final array\nres = [0] * n\ncurr = 0\nfor i in range(n):\n    curr += diff[i]\n    res[i] = curr\n\nprint(\"Final array:\", res)\n",
            "solutionCode": "n = 5\nupdates = [[1, 3, 2], [2, 4, 3], [0, 2, -2]]\n\ndiff = [0] * (n + 1)\nfor start, end, val in updates:\n    diff[start] += val\n    diff[end + 1] -= val\n\nres = [0] * n\ncurr = 0\nfor i in range(n):\n    curr += diff[i]\n    res[i] = curr\n\nprint(\"Final array:\", res)\n",
            "expectedOutputPatterns": [
                "Final array: [-2, 0, 3, 5, 3]"
            ],
            "hint": "Indices: 0 has -2; 1 has -2+2=0; 2 has -2+2+3=3; 3 has 2+3=5; 4 has 3."
        },
        "keyTakeaway": "Difference arrays allow batch updates to occur in constant time, resolved in a single linear pass."
    },
    {
        "id": "day34-step5",
        "stepNumber": 5,
        "title": "Difference Arrays Mastery",
        "shortLabel": "Recap",
        "type": "completion",
        "isGated": false,
        "dayNumber": 34,
        "heading": "Day 34 Complete: Difference Arrays & Range Updates",
        "subheading": "You have mastered difference array mechanics, O(1) boundary updates, and prefix reconstruction.",
        "recapRows": [
            {
                "concept": "Boundary Cancellation",
                "naiveIntuition": "Subtract at R because range ends at R",
                "pythonReality": "Subtract at R + 1 so that index R still receives the added value"
            },
            {
                "concept": "Batch vs Online",
                "naiveIntuition": "Use difference arrays when you need to query values between updates",
                "pythonReality": "Difference arrays are best for batch updates followed by queries; online queries need Segment Trees"
            }
        ],
        "solidifiedConcepts": [
            "D[L] += V & D[R+1] -= V Invariant",
            "Cumulative Prefix Reconstruction",
            "O(N + K) Batch Complexity",
            "Sweep-Line Algorithmic Foundation"
        ],
        "nextDayPreview": {
            "dayNumber": 35,
            "title": "Section 3 Milestone & Complexity Audit",
            "description": "Perform an end-to-end complexity audit and algorithmic proof evaluation across recursion, iterative state, and recurrences."
        }
    }
]
},
  35: {
  "dayNumber": 35,
  "title": "Section 3 Review & Algorithmic Foundations",
  "topicName": "Section 3 Synthesis",
  "sectionId": "computational-thinking",
  "estimatedMinutes": 35,
  "difficulty": "DEVELOPING",
  "prerequisites": [
    34
  ],
  "concepts": [
    "Asymptotic Synthesis",
    "Recursion & Master Theorem",
    "Prefix Sums & Difference Arrays",
    "Space-Time Tradeoffs"
  ],
  "practiceSkills": [
    "Algorithm Complexity Evaluation",
    "Cumulative Precomputation Selection",
    "Algorithmic Pattern Matching"
  ]
,
  "steps": [
    {
        "id": "day35-step1",
        "stepNumber": 1,
        "title": "Computational Thinking Synthesis",
        "shortLabel": "Section 3 Model",
        "type": "explanation",
        "isGated": false,
        "heading": "Synthesizing Complexity, Recursion, and Cumulative Precomputation",
        "subheading": "Consolidate the core mathematical and algorithmic foundations built in Days 26 to 34.",
        "markdownContent": [
            "Section 3 established the mathematical and conceptual toolkit of computer science:",
            "1. **Asymptotic Complexity**: Big-O upper bounds, dominant term extraction, dropping constants, and recognizing hidden $O(N)$ operations.",
            "2. **Space Accounting**: Differentiating input space from auxiliary space; understanding call stack frame consumption in recursion.",
            "3. **Divide and Conquer & Recurrences**: Formulating recurrence relations $T(N) = aT(N/b) + f(N)$, Master Theorem cases, and fast binary exponentiation ($O(\\log N)$).",
            "4. **Prefix Sums & Difference Arrays**: Dual techniques turning $O(N)$ range queries and $O(N)$ range updates into $O(1)$ operations."
        ],
        "snippets": [
            {
                "title": "The Duality of Prefix and Difference",
                "code": "# Prefix Sum:    Turns O(N) Range Query  -> O(1) Instant Query\n# Difference:    Turns O(N) Range Update -> O(1) Instant Update\n# They are exact mathematical inverses of each other!",
                "language": "python",
                "caption": "Dual relationship of prefix sums and difference arrays."
            }
        ],
        "callouts": [
            {
                "type": "tip",
                "title": "Ready for Core DSA",
                "content": "With this mathematical and computational foundation, you are fully equipped for Section 4: Arrays & Strings and two-pointer algorithms!"
            }
        ],
        "keyTakeaway": "Computational thinking translates problem constraints into optimal Big-O design patterns."
    },
    {
        "id": "day35-step2",
        "stepNumber": 2,
        "title": "Algorithmic Decision Matrix",
        "shortLabel": "Decision Matrix",
        "type": "explanation",
        "isGated": false,
        "heading": "Selecting the Optimal Algorithmic Pattern Based on Constraints",
        "subheading": "How to read problem constraints and deduce the required complexity.",
        "markdownContent": [
            "When reading problem constraints in technical interviews:",
            "- $N \\le 20$: Exponential / Backtracking ($O(2^N)$ or $O(N!)$).",
            "- $N \\le 500$: Cubic or quadratic ($O(N^3)$ or $O(N^2)$).",
            "- $N \\le 5,000$: Quadratic acceptable ($O(N^2)$).",
            "- $N \\le 10^5$ to $10^6$: Linear or Log-linear mandatory ($O(N)$ or $O(N \\log N)$).",
            "- $N \\ge 10^9$: Logarithmic or Constant ($O(\\log N)$ or $O(1)$ via math/binary search)."
        ],
        "snippets": [
            {
                "title": "Constraint to Complexity Mapping",
                "code": "# If N = 10^5: O(N^2) = 10^10 operations -> Time Limit Exceeded (TLE)!\n# Must use O(N) Two Pointers, Sliding Window, or Prefix Sums.",
                "language": "python",
                "caption": "Matching constraint magnitude to acceptable Big-O."
            }
        ],
        "callouts": [
            {
                "type": "deep-dive",
                "title": "The 10^8 Operations Rule of Thumb",
                "content": "Standard competitive programming and LeetCode judges execute roughly $10^8$ basic Python operations per second before triggering a Time Limit Exceeded (TLE)."
            }
        ],
        "keyTakeaway": "N = 10^5 requires O(N) or O(N log N); use the 10^8 operations per second benchmark."
    },
    {
        "id": "day35-step3",
        "stepNumber": 3,
        "title": "Section 3 Milestone Checkpoint",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Verify Section 3 Mastery Across Core Concepts",
        "subheading": "Test your synthesized algorithmic decision making.",
        "checkpoints": [
            {
                "id": "chk-d35-q1",
                "question": "If a problem specifies $N = 2 \\times 10^5$, which time complexity will PASS within a 1-second time limit?",
                "options": [
                    {
                        "id": "A",
                        "label": "O(N^2)"
                    },
                    {
                        "id": "B",
                        "label": "O(N log N)"
                    },
                    {
                        "id": "C",
                        "label": "O(2^N)"
                    },
                    {
                        "id": "D",
                        "label": "O(N^3)"
                    }
                ],
                "correctOptionId": "B",
                "explanations": {
                    "A": "Incorrect: (2*10^5)^2 = 4*10^10 operations, which takes ~400 seconds (TLE).",
                    "B": "Correct! N log N for 2*10^5 is approximately (2*10^5) * 18 = 3.6*10^6 operations, executing in under 0.1 seconds.",
                    "C": "Incorrect: Exponential time.",
                    "D": "Incorrect: Cubic time."
                }
            },
            {
                "id": "chk-d35-q2",
                "question": "When should you prefer a Difference Array over a standard loop for updates?",
                "options": [
                    {
                        "id": "A",
                        "label": "When you have a single point update"
                    },
                    {
                        "id": "B",
                        "label": "When you have many batch range updates on an array before querying the final state"
                    },
                    {
                        "id": "C",
                        "label": "When array elements are floating point numbers"
                    },
                    {
                        "id": "D",
                        "label": "Only on linked lists"
                    }
                ],
                "correctOptionId": "B",
                "explanations": {
                    "A": "Incorrect: Point updates are already O(1) in arrays.",
                    "B": "Correct! Difference arrays turn each range update into 2 point modifications (O(1)), resolving all updates in a single final prefix sweep.",
                    "C": "Incorrect: Data type is irrelevant.",
                    "D": "Incorrect: Difference arrays require direct index access."
                }
            }
        ],
        "keyTakeaway": "N = 10^5 demands O(N log N) or faster; difference arrays excel at batch range updates."
    },
    {
        "id": "day35-step4",
        "stepNumber": 4,
        "title": "Equilibrium Index Finder",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Find Equilibrium Index Using Total Sum and Running Prefix",
        "subheading": "Find an index where sum of elements to left equals sum of elements to right in O(N) time and O(1) space.",
        "task": {
            "title": "Equilibrium Index Solver",
            "instructions": [
                "Given `nums = [1, 7, 3, 6, 5, 6]`.",
                "Calculate `total_sum = sum(nums)` in $O(N)$ time.",
                "Maintain a running `left_sum = 0` as you iterate with index `i`.",
                "At index `i`, the right sum is `total_sum - left_sum - nums[i]`.",
                "If `left_sum == right_sum`, return `i`.",
                "Otherwise add `nums[i]` to `left_sum`.",
                "Print `'Equilibrium index:', eq_idx`."
            ],
            "starterCode": "# Day 35 Practice: Equilibrium Index Solver\nnums = [1, 7, 3, 6, 5, 6]\n\ntotal_sum = sum(nums)\nleft_sum = 0\neq_idx = -1\n\n# TODO: Iterate with enumerate(nums)\n# If left_sum == total_sum - left_sum - x: set eq_idx = i and break\n# Else add x to left_sum\n\nprint(\"Equilibrium index:\", eq_idx)\n",
            "solutionCode": "nums = [1, 7, 3, 6, 5, 6]\n\ntotal_sum = sum(nums)\nleft_sum = 0\neq_idx = -1\n\nfor i, x in enumerate(nums):\n    right_sum = total_sum - left_sum - x\n    if left_sum == right_sum:\n        eq_idx = i\n        break\n    left_sum += x\n\nprint(\"Equilibrium index:\", eq_idx)\n",
            "expectedOutputPatterns": [
                "Equilibrium index: 3"
            ],
            "hint": "At index 3 (value 6): left sum is 1+7+3=11; right sum is 5+6=11. Matches in O(N) time and O(1) auxiliary space!"
        },
        "keyTakeaway": "Combining total sum with running prefix achieves O(N) time with O(1) auxiliary memory."
    },
    {
        "id": "day35-step5",
        "stepNumber": 5,
        "title": "Section 3 Synthesis Mastery",
        "shortLabel": "Recap",
        "type": "completion",
        "isGated": false,
        "dayNumber": 35,
        "heading": "Day 35 Complete: Section 3 Review & Algorithmic Foundations",
        "subheading": "Congratulations! You have completed Section 3: Problem Solving & Computational Thinking.",
        "recapRows": [
            {
                "concept": "Big-O Scale Limits",
                "naiveIntuition": "O(N^2) is fine for all LeetCode problems",
                "pythonReality": "When N >= 10^4, O(N^2) exceeds 10^8 operations and triggers TLE"
            },
            {
                "concept": "Running Sum vs Array",
                "naiveIntuition": "Prefix sums always require allocating a full prefix array",
                "pythonReality": "If only past sums are needed, a single running accumulator achieves O(1) space"
            }
        ],
        "solidifiedConcepts": [
            "Asymptotic Scaling Invariants",
            "Recursion & Master Theorem",
            "Prefix Sums & Difference Arrays",
            "10^8 Operations Benchmark"
        ],
        "nextDayPreview": {
            "dayNumber": 36,
            "title": "Static vs Dynamic Arrays & Cache Locality",
            "description": "Understand physical contiguous arrays, memory layouts, CPU cache line caching, and access patterns."
        }
    }
]
},
  36: {
  "dayNumber": 36,
  "title": "String Invariants & Manipulation",
  "topicName": "String Manipulation",
  "sectionId": "arrays-and-strings",
  "estimatedMinutes": 30,
  "difficulty": "DEVELOPING",
  "prerequisites": [
    35
  ],
  "concepts": [
    "String Immutability Pitfalls",
    "O(N) join vs O(N^2) Concatenation",
    "Two Pointers on Strings",
    "Palindrome Verification"
  ],
  "practiceSkills": [
    "Two-Pointer Palindrome Check",
    "Efficient String Assembly",
    "Alphanumeric Filtering"
  ]
,
  "steps": [
    {
        "id": "day36-step1",
        "stepNumber": 1,
        "title": "String Invariants in DSA",
        "shortLabel": "String Invariants",
        "type": "explanation",
        "isGated": false,
        "heading": "Why String Concatenation in Loops is O(N^2) and How to Avoid It",
        "subheading": "Master Python's memory model for high-performance string manipulation.",
        "markdownContent": [
            "In Python, strings are immutable. Every time you write `s += char` inside a loop of length $N$, Python must allocate a new string of size $1, 2, ..., N$ and copy all previous characters.",
            "The total operations required are: $$1 + 2 + 3 + ... + N = \\frac{N(N + 1)}{2} = O(N^2)$$",
            "To build strings in linear **$O(N)$ time**, always append characters to a `list` and combine them once at the end with `''.join(chars)`."
        ],
        "snippets": [
            {
                "title": "O(N) List Buffer vs O(N^2) Concatenation",
                "code": "# DANGEROUS: O(N^2) time\ns = ''\nfor ch in stream:\n    s += ch\n\n# OPTIMAL: O(N) time\nbuffer = []\nfor ch in stream:\n    buffer.append(ch)\ns_clean = ''.join(buffer)",
                "language": "python",
                "caption": "Using list buffer and ''.join() for linear string construction."
            }
        ],
        "callouts": [
            {
                "type": "tip",
                "title": "Memory Pre-allocation in CPython",
                "content": "`''.join()` calculates the exact total byte length of all strings, allocates the buffer once, and copies data via high-speed C `memcpy`."
            }
        ],
        "keyTakeaway": "Always assemble strings using list buffers and ''.join() to avoid quadratic O(N^2) overhead."
    },
    {
        "id": "day36-step2",
        "stepNumber": 2,
        "title": "Valid Palindrome with Two Pointers",
        "shortLabel": "Palindrome Check",
        "type": "explanation",
        "isGated": false,
        "heading": "Two-Pointer Technique for In-Place String Verification",
        "subheading": "Verify palindromes with O(1) auxiliary space without reversing strings.",
        "markdownContent": [
            "A string is a palindrome if it reads the same forward and backward.",
            "While `s == s[::-1]` checks palindromes, creating the reversed slice allocates an extra $O(N)$ copy of the string in memory.",
            "The **Two-Pointer technique** places `left = 0` and `right = len(s) - 1`. While `left < right`, compare characters. If they mismatch, return `False`. Increment `left` and decrement `right`.",
            "This achieves **$O(N)$ time** and **$O(1)$ auxiliary space**, handling character normalization on-the-fly."
        ],
        "snippets": [
            {
                "title": "Two-Pointer Palindrome Verification",
                "code": "def is_palindrome(s):\n    left, right = 0, len(s) - 1\n    while left < right:\n        if s[left] != s[right]:\n            return False\n        left += 1\n        right -= 1\n    return True",
                "language": "python",
                "caption": "O(1) auxiliary space palindrome check."
            }
        ],
        "callouts": [
            {
                "type": "warning",
                "title": "Alphanumeric Filtering",
                "content": "In LeetCode 'Valid Palindrome', skip non-alphanumeric characters on-the-fly (`ch.isalnum()`) without creating a pre-filtered copy string."
            }
        ],
        "keyTakeaway": "Two pointers verify palindromes in O(N) time with zero extra string allocations (O(1) space)."
    },
    {
        "id": "day36-step3",
        "stepNumber": 3,
        "title": "Strings Checkpoint",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Test Your Mastery of String Performance",
        "subheading": "Evaluate concatenation complexities and two-pointer pointers.",
        "checkpoints": [
            {
                "id": "chk-d36-q1",
                "question": "What is the time complexity of building a string of length N by executing `result += ch` N times in a loop?",
                "options": [
                    {
                        "id": "A",
                        "label": "O(N)"
                    },
                    {
                        "id": "B",
                        "label": "O(N^2)"
                    },
                    {
                        "id": "C",
                        "label": "O(N log N)"
                    },
                    {
                        "id": "D",
                        "label": "O(1)"
                    }
                ],
                "correctOptionId": "B",
                "explanations": {
                    "A": "Incorrect: Each concatenation allocates a new string copy.",
                    "B": "Correct! Because strings are immutable, copying characters on each step sums to 1 + 2 + ... + N = N(N+1)/2 = O(N^2) quadratic time.",
                    "C": "Incorrect: It is polynomial.",
                    "D": "Incorrect: String concatenation is not constant time."
                }
            },
            {
                "id": "chk-d36-q2",
                "question": "What is the auxiliary space complexity of `s == s[::-1]` vs two-pointer palindrome check?",
                "options": [
                    {
                        "id": "A",
                        "label": "Both are O(1)"
                    },
                    {
                        "id": "B",
                        "label": "s[::-1] is O(N) space; two pointers is O(1) space"
                    },
                    {
                        "id": "C",
                        "label": "s[::-1] is O(1) space; two pointers is O(N) space"
                    },
                    {
                        "id": "D",
                        "label": "Both are O(N)"
                    }
                ],
                "correctOptionId": "B",
                "explanations": {
                    "A": "Incorrect: Slicing creates a new string object.",
                    "B": "Correct! s[::-1] allocates a complete reversed string copy of size N (O(N) space), whereas two pointers only tracks two integer index variables (O(1) space).",
                    "C": "Incorrect: Slicing allocates memory.",
                    "D": "Incorrect: Two pointers uses constant variables."
                }
            }
        ],
        "keyTakeaway": "Concatenation in loops is O(N^2); s[::-1] allocates O(N) space while two pointers is O(1) space."
    },
    {
        "id": "day36-step4",
        "stepNumber": 4,
        "title": "Valid Palindrome with Normalization",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Check Palindrome Ignoring Case & Punctuation",
        "subheading": "Verify if a string is a palindrome using two pointers while ignoring spaces and punctuation.",
        "task": {
            "title": "Robust Palindrome Checker",
            "instructions": [
                "Given `s = 'A man, a plan, a canal: Panama'`.",
                "Use two pointers `left = 0` and `right = len(s) - 1`.",
                "While `left < right`: skip `s[left]` if not `s[left].isalnum()`; skip `s[right]` if not `s[right].isalnum()`.",
                "Compare `s[left].lower() != s[right].lower()`. If mismatch, return `False`.",
                "Advance pointers appropriately.",
                "Print `'Is palindrome:', is_valid`."
            ],
            "starterCode": "# Day 36 Practice: Robust Palindrome Checker\ns = \"A man, a plan, a canal: Panama\"\n\ndef check_palindrome(text):\n    left, right = 0, len(text) - 1\n    while left < right:\n        while left < right and not text[left].isalnum():\n            left += 1\n        while left < right and not text[right].isalnum():\n            right -= 1\n        if text[left].lower() != text[right].lower():\n            return False\n        left += 1\n        right -= 1\n    return True\n\nis_valid = check_palindrome(s)\nprint(\"Is palindrome:\", is_valid)\n",
            "solutionCode": "s = \"A man, a plan, a canal: Panama\"\n\ndef check_palindrome(text):\n    left, right = 0, len(text) - 1\n    while left < right:\n        while left < right and not text[left].isalnum():\n            left += 1\n        while left < right and not text[right].isalnum():\n            right -= 1\n        if text[left].lower() != text[right].lower():\n            return False\n        left += 1\n        right -= 1\n    return True\n\nis_valid = check_palindrome(s)\nprint(\"Is palindrome:\", is_valid)\n",
            "expectedOutputPatterns": [
                "Is palindrome: True"
            ],
            "hint": "Skipping non-alphanumeric characters on the fly achieves O(N) time and O(1) auxiliary space."
        },
        "keyTakeaway": "In-place two-pointer traversal solves string validation problems with minimal memory."
    },
    {
        "id": "day36-step5",
        "stepNumber": 5,
        "title": "String Manipulation Mastery",
        "shortLabel": "Recap",
        "type": "completion",
        "isGated": false,
        "dayNumber": 36,
        "heading": "Day 36 Complete: String Invariants & Manipulation",
        "subheading": "You have mastered string immutability performance, ''.join() buffers, and O(1) space two-pointer checks.",
        "recapRows": [
            {
                "concept": "String Concatenation",
                "naiveIntuition": "s += ch is harmless inside small loops",
                "pythonReality": "It allocates a new string copy every step, degrading loops to O(N^2)"
            },
            {
                "concept": "Palindrome Checks",
                "naiveIntuition": "Always reverse the string with s[::-1]",
                "pythonReality": "Slicing allocates O(N) extra memory; two pointers is in-place O(1) space"
            }
        ],
        "solidifiedConcepts": [
            "O(N) List Buffer & ''.join() Invariant",
            "Two-Pointer Opposing Traversal",
            "In-Place Alphanumeric Skipping",
            "O(1) Auxiliary Space Palindrome Proof"
        ],
        "nextDayPreview": {
            "dayNumber": 37,
            "title": "1D Prefix Sums & O(1) Range Queries",
            "description": "Construct 1D prefix sum arrays to answer range sum queries in O(1) time after O(N) precomputation."
        }
    }
]
},
  37: {
  "dayNumber": 37,
  "title": "Subarrays vs Subsequences",
  "topicName": "Subarrays vs Subsequences",
  "sectionId": "arrays-and-strings",
  "estimatedMinutes": 30,
  "difficulty": "DEVELOPING",
  "prerequisites": [
    36
  ],
  "concepts": [
    "Contiguous vs Non-Contiguous",
    "Total Counts: N(N+1)/2 vs 2^N",
    "Subarray Algorithms",
    "Subsequence Algorithms"
  ],
  "practiceSkills": [
    "Taxonomy Identification",
    "Subsequence Verification (Two Pointers)",
    "Subarray Generation"
  ]
,
  "steps": [
    {
        "id": "day37-step1",
        "stepNumber": 1,
        "title": "The Three Core Sequence Substructures",
        "shortLabel": "Sequence Taxonomy",
        "type": "explanation",
        "isGated": false,
        "heading": "Subarrays vs Substrings vs Subsequences vs Subsets",
        "subheading": "Never confuse contiguous slices with non-contiguous orderings.",
        "markdownContent": [
            "Algorithmic problems frequently ask about sequence substructures. Differentiating them is critical for selecting the right algorithm:",
            "1. **Subarray / Substring**: A **contiguous** slice of the original sequence. For an array of size $N$, there are exactly $\\frac{N(N + 1)}{2} = O(N^2)$ non-empty subarrays. Solved with **Sliding Window**, **Prefix Sums**, or **Two Pointers**.",
            "2. **Subsequence**: A sequence derived by deleting zero or more elements **without changing the relative order** of remaining elements. For size $N$, there are $2^N$ subsequences. Solved with **Dynamic Programming** or **Greedy** algorithms.",
            "3. **Subset**: An unordered selection of elements (order does not matter)."
        ],
        "snippets": [
            {
                "title": "Subarray vs Subsequence Examples",
                "code": "# arr = [1, 2, 3]\n# Subarrays (contiguous, O(N^2)): \n# [1], [2], [3], [1, 2], [2, 3], [1, 2, 3]\n\n# Subsequences (ordered non-contiguous, 2^N):\n# [], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]\n# Notice [1, 3] is a subsequence but NOT a subarray!",
                "language": "python",
                "caption": "[1, 3] maintains relative order but is not contiguous."
            }
        ],
        "callouts": [
            {
                "type": "tip",
                "title": "Counting Formula",
                "content": "Subarrays: $O(N^2)$ polynomial. Subsequences: $O(2^N)$ exponential. If a problem asks for 'longest subsequence', brute-force enumeration will TLE!"
            }
        ],
        "keyTakeaway": "Subarrays are strictly contiguous (O(N^2)); subsequences preserve relative order but can skip elements (2^N)."
    },
    {
        "id": "day37-step2",
        "stepNumber": 2,
        "title": "Is Subsequence? Two-Pointer Greedy Check",
        "shortLabel": "Subsequence Check",
        "type": "explanation",
        "isGated": false,
        "heading": "Checking if String s is a Subsequence of String t in O(len(t)) Time",
        "subheading": "A linear greedy two-pointer scan.",
        "markdownContent": [
            "To determine if `s` is a subsequence of `t` (e.g. `s = 'ace'`, `t = 'abcde'`):",
            "- Place pointer `i = 0` on `s` and pointer `j = 0` on `t`.",
            "- While `i < len(s)` and `j < len(t)`: if `s[i] == t[j]`, advance `i` (match found!).",
            "- Always advance `j` to examine the next character in `t`.",
            "- At the end, `s` is a subsequence if and only if `i == len(s)`.",
            "Time complexity is strictly **$O(\\text{len}(t))$** with **$O(1)$ auxiliary space**."
        ],
        "snippets": [
            {
                "title": "is_subsequence Implementation",
                "code": "def is_subsequence(s, t):\n    i, j = 0, 0\n    while i < len(s) and j < len(t):\n        if s[i] == t[j]:\n            i += 1\n        j += 1\n    return i == len(s)\n\nprint(is_subsequence('ace', 'abcde')) # True\nprint(is_subsequence('aec', 'abcde')) # False (wrong order!)",
                "language": "python",
                "caption": "Greedy linear scan to verify subsequences."
            }
        ],
        "callouts": [
            {
                "type": "warning",
                "title": "Order Matters in Subsequences",
                "content": "`'aec'` is NOT a subsequence of `'abcde'` because `'e'` appears before `'c'` in the query, violating the original sequence order."
            }
        ],
        "keyTakeaway": "Subsequence verification checks relative ordering in linear O(len(t)) time using two pointers."
    },
    {
        "id": "day37-step3",
        "stepNumber": 3,
        "title": "Substructures Checkpoint",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Test Your Mastery of Sequence Taxonomy",
        "subheading": "Classify substructures and calculate combinatorial counts.",
        "checkpoints": [
            {
                "id": "chk-d37-q1",
                "question": "Which of the following is a SUBSEQUENCE of [1, 2, 3, 4, 5] but NOT a SUBARRAY?",
                "options": [
                    {
                        "id": "A",
                        "label": "[2, 3, 4]"
                    },
                    {
                        "id": "B",
                        "label": "[1, 3, 5]"
                    },
                    {
                        "id": "C",
                        "label": "[5, 4, 3]"
                    },
                    {
                        "id": "D",
                        "label": "[1, 2]"
                    }
                ],
                "correctOptionId": "B",
                "explanations": {
                    "A": "Incorrect: [2, 3, 4] is contiguous, so it is both a subarray and a subsequence.",
                    "B": "Correct! [1, 3, 5] skips elements 2 and 4 (non-contiguous, so not a subarray), but preserves relative left-to-right order, making it a valid subsequence.",
                    "C": "Incorrect: Elements are in reversed order, so it is neither a subarray nor a subsequence.",
                    "D": "Incorrect: Contiguous subarray."
                }
            },
            {
                "id": "chk-d37-q2",
                "question": "How many total non-empty contiguous subarrays exist for an array of length N = 4?",
                "options": [
                    {
                        "id": "A",
                        "label": "16 (2^4)"
                    },
                    {
                        "id": "B",
                        "label": "10 (4 * 5 / 2)"
                    },
                    {
                        "id": "C",
                        "label": "24 (4!)"
                    },
                    {
                        "id": "D",
                        "label": "8"
                    }
                ],
                "correctOptionId": "B",
                "explanations": {
                    "A": "Incorrect: 2^N is the count of subsequences.",
                    "B": "Correct! The number of non-empty contiguous subarrays is N*(N+1)/2 = 4*5/2 = 10 (4 of length 1, 3 of length 2, 2 of length 3, 1 of length 4).",
                    "C": "Incorrect: N! is permutations.",
                    "D": "Incorrect: Miscalculation."
                }
            }
        ],
        "keyTakeaway": "Subarrays are contiguous (N*(N+1)/2); subsequences skip elements while preserving relative order."
    },
    {
        "id": "day37-step4",
        "stepNumber": 4,
        "title": "Subsequence Matcher",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Verify Multiple Subsequence Queries",
        "subheading": "Write a function to test whether target words are valid subsequences.",
        "task": {
            "title": "Subsequence Batch Checker",
            "instructions": [
                "Given source string `source = 'ahbgdc'` and test words `words = ['abc', 'axc', 'bgd']`.",
                "Implement `check_subseq(s, t)` using the two-pointer greedy pattern.",
                "Count how many words in `words` are valid subsequences of `source`.",
                "Print `'Valid subsequence count:', valid_count`."
            ],
            "starterCode": "# Day 37 Practice: Subsequence Batch Checker\nsource = \"ahbgdc\"\nwords = [\"abc\", \"axc\", \"bgd\"]\n\ndef is_sub(s, t):\n    i, j = 0, 0\n    while i < len(s) and j < len(t):\n        if s[i] == t[j]:\n            i += 1\n        j += 1\n    return i == len(s)\n\nvalid_count = sum(1 for w in words if is_sub(w, source))\nprint(\"Valid subsequence count:\", valid_count)\n",
            "solutionCode": "source = \"ahbgdc\"\nwords = [\"abc\", \"axc\", \"bgd\"]\n\ndef is_sub(s, t):\n    i, j = 0, 0\n    while i < len(s) and j < len(t):\n        if s[i] == t[j]:\n            i += 1\n        j += 1\n    return i == len(s)\n\nvalid_count = sum(1 for w in words if is_sub(w, source))\nprint(\"Valid subsequence count:\", valid_count)\n",
            "expectedOutputPatterns": [
                "Valid subsequence count: 2"
            ],
            "hint": "'abc' and 'bgd' are valid; 'axc' fails because 'x' is not present in source."
        },
        "keyTakeaway": "Two pointers greedily advance through the source string to match subsequence characters."
    },
    {
        "id": "day37-step5",
        "stepNumber": 5,
        "title": "Substructures Mastery",
        "shortLabel": "Recap",
        "type": "completion",
        "isGated": false,
        "dayNumber": 37,
        "heading": "Day 37 Complete: Subarrays vs Subsequences",
        "subheading": "You have mastered sequence taxonomy, combinatorial bounds, and linear subsequence checks.",
        "recapRows": [
            {
                "concept": "Subarray vs Subsequence",
                "naiveIntuition": "Subarray and subsequence are interchangeable terms",
                "pythonReality": "Subarrays are strictly contiguous slices; subsequences preserve order but can skip items"
            },
            {
                "concept": "Count Growth",
                "naiveIntuition": "Both have roughly the same number of variations",
                "pythonReality": "Subarrays grow polynomially (O(N^2)); subsequences grow exponentially (O(2^N))"
            }
        ],
        "solidifiedConcepts": [
            "Contiguous Subarrays (N*(N+1)/2)",
            "Non-contiguous Subsequences (2^N)",
            "Linear Two-Pointer Subsequence Match",
            "Combinatorial Bounds Invariants"
        ],
        "nextDayPreview": {
            "dayNumber": 38,
            "title": "Difference Arrays & Range Updates",
            "description": "Master difference arrays for O(1) range updates followed by a single O(N) prefix sum reconstruction."
        }
    }
]
},
  38: {
  "dayNumber": 38,
  "title": "In-Place Array Transformations",
  "topicName": "In-Place Transformations",
  "sectionId": "arrays-and-strings",
  "estimatedMinutes": 30,
  "difficulty": "DEVELOPING",
  "prerequisites": [
    37
  ],
  "concepts": [
    "Write-Pointer Technique",
    "Remove Duplicates Pattern",
    "Move Zeroes Invariant",
    "O(1) Auxiliary Space"
  ],
  "practiceSkills": [
    "Write-Pointer Coordination",
    "In-Place Compaction",
    "Stable Zero Shifting"
  ]
,
  "steps": [
    {
        "id": "day38-step1",
        "stepNumber": 1,
        "title": "The Write-Pointer Invariant",
        "shortLabel": "Write-Pointer",
        "type": "explanation",
        "isGated": false,
        "heading": "Overwriting Elements In-Place with Read/Write Pointer Decoupling",
        "subheading": "Modify arrays with O(1) auxiliary space without element shifting penalties.",
        "markdownContent": [
            "Many algorithmic challenges require modifying an array **in-place** (e.g. *'Remove duplicates from sorted array'*, *'Move zeroes'*), returning the length of the valid prefix.",
            "Using `arr.pop(i)` or `arr.remove(x)` inside a loop costs $O(N)$ per deletion, resulting in $O(N^2)$ time.",
            "The optimal paradigm decouples traversal into two pointers:",
            "- **Read Pointer (`read`)**: Scans through every element of the array.",
            "- **Write Pointer (`write`)**: Marks the position where the next valid element should be placed.",
            "Because `write <= read` at all times, the write pointer never overwrites unprocessed data! Total time is strictly **$O(N)$** with **$O(1)$ auxiliary space**."
        ],
        "snippets": [
            {
                "title": "Remove Duplicates In-Place",
                "code": "def remove_duplicates(nums):\n    if not nums:\n        return 0\n    write = 1\n    for read in range(1, len(nums)):\n        if nums[read] != nums[read - 1]:\n            nums[write] = nums[read]\n            write += 1\n    return write # Length of unique prefix",
                "language": "python",
                "caption": "Write-pointer compaction pattern."
            }
        ],
        "callouts": [
            {
                "type": "tip",
                "title": "write <= read Invariant",
                "content": "Since the write pointer advances at or slower than the read pointer, reading is always safe from premature overwrites."
            }
        ],
        "keyTakeaway": "Decoupling read and write pointers enables in-place array compaction in O(N) time and O(1) space."
    },
    {
        "id": "day38-step2",
        "stepNumber": 2,
        "title": "The Move Zeroes Pattern",
        "shortLabel": "Move Zeroes",
        "type": "explanation",
        "isGated": false,
        "heading": "Maintaining Relative Order While Shifting Zeroes to the End",
        "subheading": "Compact non-zero elements forward and fill the remainder with zeroes.",
        "markdownContent": [
            "Consider *Move Zeroes*: move all zeroes to the end while preserving the relative order of non-zero numbers.",
            "1. Walk through the array with `read`. Whenever `arr[read] != 0`, write it to `arr[write]` and increment `write`.",
            "2. Once `read` reaches the end, all non-zero elements occupy indices `0` to `write - 1` in their original order.",
            "3. Fill the remaining positions from `write` to `len(arr) - 1` with `0`.",
            "Alternatively, swap `arr[write], arr[read] = arr[read], arr[write]` whenever `arr[read] != 0`."
        ],
        "snippets": [
            {
                "title": "Move Zeroes via Swapping",
                "code": "def move_zeroes(nums):\n    write = 0\n    for read in range(len(nums)):\n        if nums[read] != 0:\n            nums[write], nums[read] = nums[read], nums[write]\n            write += 1\n\narr = [0, 1, 0, 3, 12]\nmove_zeroes(arr)\nprint(arr) # [1, 3, 12, 0, 0]",
                "language": "python",
                "caption": "In-place zero swapping."
            }
        ],
        "callouts": [
            {
                "type": "warning",
                "title": "Do Not Use pop(i)",
                "content": "Popping elements while iterating causes skipped indices and degrades performance to $O(N^2)$."
            }
        ],
        "keyTakeaway": "Swapping or compacting with a write pointer moves target elements in O(N) time with O(1) space."
    },
    {
        "id": "day38-step3",
        "stepNumber": 3,
        "title": "In-Place Transformations Checkpoint",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Test Your Mastery of In-Place Array Compaction",
        "subheading": "Evaluate read/write pointer states and array prefixes.",
        "checkpoints": [
            {
                "id": "chk-d38-q1",
                "question": "Why is `write <= read` a crucial invariant in write-pointer algorithms?",
                "options": [
                    {
                        "id": "A",
                        "label": "It guarantees that the write pointer never overwrites an element before the read pointer has inspected it"
                    },
                    {
                        "id": "B",
                        "label": "It ensures the array remains sorted"
                    },
                    {
                        "id": "C",
                        "label": "It prevents list index out of range errors on write"
                    },
                    {
                        "id": "D",
                        "label": "It forces O(1) time complexity"
                    }
                ],
                "correctOptionId": "A",
                "explanations": {
                    "A": "Correct! Because write <= read, the write pointer only modifies positions that have already been processed by the read pointer, preventing data loss.",
                    "B": "Incorrect: Sorting depends on comparison logic.",
                    "C": "Incorrect: Boundaries are capped by array length.",
                    "D": "Incorrect: Complexity is O(N)."
                }
            },
            {
                "id": "chk-d38-q2",
                "question": "In `remove_duplicates([1, 1, 2, 2, 3])`, what is the value of `write` at termination?",
                "options": [
                    {
                        "id": "A",
                        "label": "5"
                    },
                    {
                        "id": "B",
                        "label": "3"
                    },
                    {
                        "id": "C",
                        "label": "2"
                    },
                    {
                        "id": "D",
                        "label": "4"
                    }
                ],
                "correctOptionId": "B",
                "explanations": {
                    "A": "Incorrect: 5 is the original length.",
                    "B": "Correct! There are 3 unique elements: 1, 2, 3. The write pointer stops at index 3, defining the prefix length.",
                    "C": "Incorrect: Miscounted unique items.",
                    "D": "Incorrect: Duplicates are eliminated."
                }
            }
        ],
        "keyTakeaway": "write <= read prevents data loss; write pointer index indicates length of unique compacted prefix."
    },
    {
        "id": "day38-step4",
        "stepNumber": 4,
        "title": "Remove Element In-Place",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Implement In-Place Value Removal",
        "subheading": "Remove all instances of `val = 3` from `nums` in-place and return the new length.",
        "task": {
            "title": "In-Place Element Remover",
            "instructions": [
                "Given `nums = [3, 2, 2, 3, 4, 3, 5]` and `val = 3`.",
                "Initialize `write = 0`.",
                "Iterate `read` from 0 to `len(nums) - 1`.",
                "If `nums[read] != val`, set `nums[write] = nums[read]` and increment `write += 1`.",
                "Print `'New length:', write` and `'Compacted prefix:', nums[:write]`."
            ],
            "starterCode": "# Day 38 Practice: In-Place Element Remover\nnums = [3, 2, 2, 3, 4, 3, 5]\nval = 3\n\nwrite = 0\nfor read in range(len(nums)):\n    if nums[read] != val:\n        nums[write] = nums[read]\n        write += 1\n\nprint(\"New length:\", write)\nprint(\"Compacted prefix:\", nums[:write])\n",
            "solutionCode": "nums = [3, 2, 2, 3, 4, 3, 5]\nval = 3\n\nwrite = 0\nfor read in range(len(nums)):\n    if nums[read] != val:\n        nums[write] = nums[read]\n        write += 1\n\nprint(\"New length:\", write)\nprint(\"Compacted prefix:\", nums[:write])\n",
            "expectedOutputPatterns": [
                "New length: 4",
                "Compacted prefix: [2, 2, 4, 5]"
            ],
            "hint": "Elements != 3 are 2, 2, 4, 5. Write pointer stops at index 4."
        },
        "keyTakeaway": "In-place element removal compacts valid data into the array prefix with O(1) auxiliary space."
    },
    {
        "id": "day38-step5",
        "stepNumber": 5,
        "title": "In-Place Transformations Mastery",
        "shortLabel": "Recap",
        "type": "completion",
        "isGated": false,
        "dayNumber": 38,
        "heading": "Day 38 Complete: In-Place Array Transformations",
        "subheading": "You have mastered read/write pointer decoupling, array compaction, and O(1) auxiliary space mutations.",
        "recapRows": [
            {
                "concept": "Deletion In-Place",
                "naiveIntuition": "Call pop(i) or remove(x) when duplicate is found",
                "pythonReality": "pop(i) shifts all following elements taking O(N); write pointer overwrites in O(1)"
            },
            {
                "concept": "Prefix Validity",
                "naiveIntuition": "Array elements beyond the new length must be deleted",
                "pythonReality": "LeetCode only checks elements up to the returned prefix length write"
            }
        ],
        "solidifiedConcepts": [
            "Read vs Write Pointer Decoupling",
            "write <= read Safety Invariant",
            "Zero Shifting and Swapping",
            "O(N) Time and O(1) Space Guarantees"
        ],
        "nextDayPreview": {
            "dayNumber": 39,
            "title": "Two Pointers: Opposing Direction",
            "description": "Use two pointers moving inward from boundaries to solve two-sum on sorted arrays and maximize area."
        }
    }
]
},
  39: {
  "dayNumber": 39,
  "title": "Two Pointers: Opposing Direction",
  "topicName": "Opposing Two Pointers",
  "sectionId": "arrays-and-strings",
  "estimatedMinutes": 35,
  "difficulty": "DEVELOPING",
  "prerequisites": [
    38
  ],
  "concepts": [
    "Two Sum in Sorted Array",
    "Container With Most Water",
    "Monotonicity Invariant",
    "Greedy Elimination"
  ],
  "practiceSkills": [
    "Opposing Pointers Coordination",
    "Container Area Maximization",
    "Monotonic State Elimination"
  ]
,
  "steps": [
    {
        "id": "day39-step1",
        "stepNumber": 1,
        "title": "The Opposing Two-Pointer Pattern",
        "shortLabel": "Opposing Pointers",
        "type": "explanation",
        "isGated": false,
        "heading": "Exploiting Monotonicity to Eliminate Search Space in O(N) Time",
        "subheading": "Solve Two Sum and optimization problems on sorted arrays without hash maps.",
        "markdownContent": [
            "When an array is sorted, elements exhibit **monotonicity**: elements increase from left to right.",
            "In **Two Sum II (Sorted Array)**, we want to find two numbers that sum to `target`:",
            "- Place `left = 0` (smallest element) and `right = len(arr) - 1` (largest element).",
            "- Compute `current_sum = arr[left] + arr[right]`.",
            "- If `current_sum == target`: Return the pair!",
            "- If `current_sum < target`: The sum is too small. Because `arr[right]` is already the largest remaining element, pairing `arr[left]` with ANY other element will also be too small! We can safely eliminate `left` by doing `left += 1`.",
            "- If `current_sum > target`: The sum is too large. We can safely eliminate `right` by doing `right -= 1`.",
            "At each step, we eliminate an entire row or column of potential pairs, achieving **$O(N)$ time** and **$O(1)$ space**!"
        ],
        "snippets": [
            {
                "title": "Two Sum II Opposing Pointers",
                "code": "def two_sum_sorted(nums, target):\n    left, right = 0, len(nums) - 1\n    while left < right:\n        s = nums[left] + nums[right]\n        if s == target:\n            return (left, right)\n        elif s < target:\n            left += 1   # Need a larger sum\n        else:\n            right -= 1  # Need a smaller sum\n    return None",
                "language": "python",
                "caption": "O(N) search on sorted arrays via monotonic elimination."
            }
        ],
        "callouts": [
            {
                "type": "tip",
                "title": "Sorted Array Prerequisite",
                "content": "Opposing two pointers for sum targets strictly requires a **sorted array**. If the array is unsorted, either sort it in $O(N \\log N)$ or use an $O(N)$ hash map."
            }
        ],
        "keyTakeaway": "Monotonicity guarantees that adjusting left or right safely eliminates an entire row of candidates."
    },
    {
        "id": "day39-step2",
        "stepNumber": 2,
        "title": "Container With Most Water",
        "shortLabel": "Container Problem",
        "type": "explanation",
        "isGated": false,
        "heading": "Greedy Elimination in Container With Most Water",
        "subheading": "Why moving the shorter line is the only choice that could increase area.",
        "markdownContent": [
            "In *Container With Most Water*, given heights `h`, find two lines that hold the most water: $$\\text{Area} = (\\text{right} - \\text{left}) \\times \\min(h[\\text{left}], h[\\text{right}])$$",
            "Start with maximum width: `left = 0, right = len(h) - 1`.",
            "To find a larger area, the width $(\\text{right} - \\text{left})$ MUST decrease by 1 at the next step. Therefore, the **only way the area can increase is if the limiting height increases**!",
            "Since the area is bounded by the shorter line, moving the taller line can NEVER increase area (width decreases, height cannot exceed shorter line).",
            "Thus, we must **greedily move the pointer pointing to the shorter line** inward!"
        ],
        "snippets": [
            {
                "title": "Container With Most Water Implementation",
                "code": "def max_area(height):\n    left, right = 0, len(height) - 1\n    best = 0\n    while left < right:\n        w = right - left\n        h = min(height[left], height[right])\n        best = max(best, w * h)\n        if height[left] < height[right]:\n            left += 1\n        else:\n            right -= 1\n    return best",
                "language": "python",
                "caption": "Greedy shorter-line elimination in O(N) time."
            }
        ],
        "callouts": [
            {
                "type": "warning",
                "title": "Equal Heights Case",
                "content": "If `height[left] == height[right]`, you can move either pointer (or both inward), because neither can be part of a larger area with the other line fixed."
            }
        ],
        "keyTakeaway": "Always move the pointer corresponding to the bottleneck (shorter line) to seek a taller boundary."
    },
    {
        "id": "day39-step3",
        "stepNumber": 3,
        "title": "Opposing Two Pointers Checkpoint",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Test Your Mastery of Opposing Pointers",
        "subheading": "Evaluate pointer movements and greedy elimination logic.",
        "checkpoints": [
            {
                "id": "chk-d39-q1",
                "question": "In 'Container With Most Water', why do we move the pointer at the SHORTER line rather than the taller line?",
                "options": [
                    {
                        "id": "A",
                        "label": "Because moving the taller line would make width negative"
                    },
                    {
                        "id": "B",
                        "label": "Because width decreases; if we move the taller line, the new height cannot exceed the current shorter line, so area can only decrease or stay same"
                    },
                    {
                        "id": "C",
                        "label": "It is an arbitrary convention; moving either gives identical results"
                    },
                    {
                        "id": "D",
                        "label": "To sort the array"
                    }
                ],
                "correctOptionId": "B",
                "explanations": {
                    "A": "Incorrect: Width is right - left > 0.",
                    "B": "Correct! The bottleneck is the shorter line. Moving the taller line decreases width while the height remains capped by the shorter line, guaranteeing a strictly smaller area. Moving the shorter line is the only possibility to find a taller bottleneck.",
                    "C": "Incorrect: Moving the taller line misses the optimal solution.",
                    "D": "Incorrect: The heights are not being sorted."
                }
            },
            {
                "id": "chk-d39-q2",
                "question": "Given sorted `nums = [1, 3, 5, 8, 12]` and `target = 11`, with `left = 0 (1)` and `right = 4 (12)`. What is the next pointer move?",
                "options": [
                    {
                        "id": "A",
                        "label": "left += 1"
                    },
                    {
                        "id": "B",
                        "label": "right -= 1"
                    },
                    {
                        "id": "C",
                        "label": "Both increment"
                    },
                    {
                        "id": "D",
                        "label": "Return 1"
                    }
                ],
                "correctOptionId": "B",
                "explanations": {
                    "A": "Incorrect: That would increase the sum further.",
                    "B": "Correct! Current sum is 1 + 12 = 13. Since 13 > 11, the sum is too large. We decrement right -= 1 to reduce the sum.",
                    "C": "Incorrect: Only one pointer moves per step.",
                    "D": "Incorrect: Target is not yet matched."
                }
            }
        ],
        "keyTakeaway": "Move left pointer when sum < target; move right pointer when sum > target; move shorter container line."
    },
    {
        "id": "day39-step4",
        "stepNumber": 4,
        "title": "Container With Most Water Solver",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Maximize Water Retention Between Vertical Lines",
        "subheading": "Implement the O(N) two-pointer solution for Container With Most Water.",
        "task": {
            "title": "Water Container Maximizer",
            "instructions": [
                "Given `heights = [1, 8, 6, 2, 5, 4, 8, 3, 7]`.",
                "Initialize `left = 0, right = len(heights) - 1, max_water = 0`.",
                "While `left < right`: compute area `(right - left) * min(heights[left], heights[right])`.",
                "Update `max_water = max(max_water, area)`.",
                "Advance the pointer pointing to the smaller height.",
                "Print `'Max water container:', max_water`."
            ],
            "starterCode": "# Day 39 Practice: Water Container Maximizer\nheights = [1, 8, 6, 2, 5, 4, 8, 3, 7]\n\nleft, right = 0, len(heights) - 1\nmax_water = 0\n\nwhile left < right:\n    w = right - left\n    h = min(heights[left], heights[right])\n    max_water = max(max_water, w * h)\n    if heights[left] < heights[right]:\n        left += 1\n    else:\n        right -= 1\n\nprint(\"Max water container:\", max_water)\n",
            "solutionCode": "heights = [1, 8, 6, 2, 5, 4, 8, 3, 7]\n\nleft, right = 0, len(heights) - 1\nmax_water = 0\n\nwhile left < right:\n    w = right - left\n    h = min(heights[left], heights[right])\n    max_water = max(max_water, w * h)\n    if heights[left] < heights[right]:\n        left += 1\n    else:\n        right -= 1\n\nprint(\"Max water container:\", max_water)\n",
            "expectedOutputPatterns": [
                "Max water container: 49"
            ],
            "hint": "Optimal lines are index 1 (height 8) and index 8 (height 7): width = 7, min_height = 7 -> 7 * 7 = 49."
        },
        "keyTakeaway": "Opposing two pointers evaluate maximum width configurations and eliminate suboptimal bottlenecks in O(N) time."
    },
    {
        "id": "day39-step5",
        "stepNumber": 5,
        "title": "Opposing Two Pointers Mastery",
        "shortLabel": "Recap",
        "type": "completion",
        "isGated": false,
        "dayNumber": 39,
        "heading": "Day 39 Complete: Two Pointers: Opposing Direction",
        "subheading": "You have mastered sorted monotonicity elimination, Two Sum II, and Container With Most Water.",
        "recapRows": [
            {
                "concept": "Sorting Prerequisite",
                "naiveIntuition": "Opposing two pointers works on any arbitrary list for target sum",
                "pythonReality": "It strictly requires a sorted sequence so pointer movements have predictable effects"
            },
            {
                "concept": "Container Bottleneck",
                "naiveIntuition": "Always move the taller line to try and find an even taller one",
                "pythonReality": "The shorter line caps container volume; moving it is the only way to increase area"
            }
        ],
        "solidifiedConcepts": [
            "Two Sum II Monotonic Elimination",
            "O(N) Time and O(1) Auxiliary Space",
            "Container With Most Water Invariant",
            "Greedy Bottleneck Advancement"
        ],
        "nextDayPreview": {
            "dayNumber": 40,
            "title": "Two Pointers: Fast & Slow In-Place Writers",
            "description": "Implement fast and slow pointers for in-place array mutation, deduplication, and zero-shifting in O(1) space."
        }
    }
]
},
  40: {
  "dayNumber": 40,
  "title": "Two Pointers: Fast & Slow",
  "topicName": "Fast & Slow Pointers",
  "sectionId": "arrays-and-strings",
  "estimatedMinutes": 35,
  "difficulty": "DEVELOPING",
  "prerequisites": [
    39
  ],
  "concepts": [
    "Floyd's Tortoise and Hare",
    "Cycle Detection in Arrays",
    "Duplicate Number Finding",
    "Linked List Preview"
  ],
  "practiceSkills": [
    "Cycle Traversal Simulation",
    "Tortoise & Hare Index Mapping",
    "Floyd's Phase 1 & Phase 2"
  ]
,
  "steps": [
    {
        "id": "day40-step1",
        "stepNumber": 1,
        "title": "Floyd's Cycle Detection Algorithm",
        "shortLabel": "Tortoise & Hare",
        "type": "explanation",
        "isGated": false,
        "heading": "The Tortoise and Hare: Detecting Cycles with Relative Speed",
        "subheading": "How two pointers moving at different speeds guarantee cycle detection in O(N) time and O(1) space.",
        "markdownContent": [
            "**Floyd's Cycle Detection Algorithm** (also called the Tortoise and Hare) uses two pointers traversing a sequence:",
            "- **Slow Pointer (`slow`)**: Advances by 1 step each iteration.",
            "- **Fast Pointer (`fast`)**: Advances by 2 steps each iteration.",
            "If the sequence is linear without a cycle, `fast` reaches the end and terminates.",
            "If a cycle exists, `fast` will enter the cycle first. Inside the cycle, the relative distance between `fast` and `slow` decreases by 1 step on every iteration! Therefore, `fast` is mathematically **guaranteed to catch and collide with `slow`** in at most $C$ iterations (where $C$ is cycle length)."
        ],
        "snippets": [
            {
                "title": "Floyd's Collision Principle",
                "code": "# On each iteration:\n# distance_gap = (distance_gap + 2 - 1) % cycle_length\n# distance_gap increases by 1 modulo C each step\n# Collision is guaranteed within C steps of slow entering cycle!",
                "language": "python",
                "caption": "Relative speed guarantee of cycle collision."
            }
        ],
        "callouts": [
            {
                "type": "tip",
                "title": "O(1) Auxiliary Space",
                "content": "A hash set of seen nodes detects cycles in $O(N)$ space. Floyd's algorithm detects cycles in **$O(1)$ auxiliary space** using only two pointers!"
            }
        ],
        "keyTakeaway": "Moving at 1x and 2x speeds guarantees collision within cycles in O(N) time and O(1) space."
    },
    {
        "id": "day40-step2",
        "stepNumber": 2,
        "title": "Finding the Duplicate Number (LeetCode 287)",
        "shortLabel": "Duplicate Detection",
        "type": "explanation",
        "isGated": false,
        "heading": "Mapping an Array to a Functional Graph: nums[i] as a Pointer",
        "subheading": "Solve 'Find the Duplicate Number' in O(N) time and O(1) space without modifying the array.",
        "markdownContent": [
            "Given an array `nums` of size $N + 1$ containing integers between $1$ and $N$, the Pigeonhole Principle guarantees at least one duplicate exists.",
            "If we treat the array as a directed graph where index `i` points to `nums[i]`:",
            "- Because a duplicate value exists, at least two distinct indices point to the same target index (in-degree $\\ge 2$).",
            "- This forms a **cycle**, where the duplicate number is the **entry point of the cycle**!",
            "**Phase 1 (Collision)**: Advance `slow = nums[slow]` and `fast = nums[nums[fast]]` until `slow == fast`.",
            "**Phase 2 (Entry Point)**: Reset `slow = 0`. Keep `fast` at the collision point. Advance both by 1 step (`slow = nums[slow]`, `fast = nums[fast]`). The point where they meet is the duplicate number!"
        ],
        "snippets": [
            {
                "title": "Find the Duplicate Number Implementation",
                "code": "def find_duplicate(nums):\n    # Phase 1: Find collision\n    slow = nums[0]\n    fast = nums[0]\n    while True:\n        slow = nums[slow]\n        fast = nums[nums[fast]]\n        if slow == fast:\n            break\n    # Phase 2: Find cycle entrance\n    slow = nums[0]\n    while slow != fast:\n        slow = nums[slow]\n        fast = nums[fast]\n    return slow",
                "language": "python",
                "caption": "Floyd's algorithm for finding duplicate numbers."
            }
        ],
        "callouts": [
            {
                "type": "warning",
                "title": "Read-Only Invariant",
                "content": "This algorithm runs in $O(N)$ time and $O(1)$ space without mutating `nums`, satisfying interview constraints that forbid sorting or negative marking."
            }
        ],
        "keyTakeaway": "Mapping index to value nums[i] creates a functional graph where cycle entrance is the duplicate."
    },
    {
        "id": "day40-step3",
        "stepNumber": 3,
        "title": "Fast & Slow Pointers Checkpoint",
        "shortLabel": "Checkpoint",
        "type": "checkpoint",
        "isGated": true,
        "heading": "Test Your Mastery of Floyd's Algorithm",
        "subheading": "Verify cycle collision mathematics and Phase 2 mechanics.",
        "checkpoints": [
            {
                "id": "chk-d40-q1",
                "question": "Once the fast and slow pointers collide in Phase 1 of Floyd's algorithm, how is the cycle entrance located in Phase 2?",
                "options": [
                    {
                        "id": "A",
                        "label": "Move fast backward by one step"
                    },
                    {
                        "id": "B",
                        "label": "Reset slow to the starting node, and advance BOTH pointers at 1 step per iteration until they meet"
                    },
                    {
                        "id": "C",
                        "label": "Continue moving fast at 2 steps until it collides again"
                    },
                    {
                        "id": "D",
                        "label": "Return the collision point directly"
                    }
                ],
                "correctOptionId": "B",
                "explanations": {
                    "A": "Incorrect: Linked structures cannot traverse backwards.",
                    "B": "Correct! Mathematical proof shows that the distance from start to cycle entry equals the distance from collision point to cycle entry. Advancing both at 1 step per cycle causes them to meet exactly at the cycle entrance.",
                    "C": "Incorrect: That would simply circle the loop again.",
                    "D": "Incorrect: The collision point is inside the cycle, not necessarily at the entry."
                }
            },
            {
                "id": "chk-d40-q2",
                "question": "Why is Floyd's algorithm preferred over a hash set for cycle detection in memory-constrained environments?",
                "options": [
                    {
                        "id": "A",
                        "label": "A hash set is O(N^2) time"
                    },
                    {
                        "id": "B",
                        "label": "Floyd's uses O(1) auxiliary space, whereas a hash set stores all N visited nodes (O(N) space)"
                    },
                    {
                        "id": "C",
                        "label": "Floyd's works on unhashable objects"
                    },
                    {
                        "id": "D",
                        "label": "Floyd's algorithm executes in O(log N) time"
                    }
                ],
                "correctOptionId": "B",
                "explanations": {
                    "A": "Incorrect: Hash set is O(N) time.",
                    "B": "Correct! A hash set allocates O(N) memory to record seen nodes. Floyd's tracks only two pointer variables, achieving O(1) auxiliary space.",
                    "C": "Incorrect: Floyd's still requires addressable nodes.",
                    "D": "Incorrect: Both algorithms are O(N) time."
                }
            }
        ],
        "keyTakeaway": "Phase 2 resets one pointer to start and advances both by 1 step; Floyd's achieves O(1) auxiliary space."
    },
    {
        "id": "day40-step4",
        "stepNumber": 4,
        "title": "Find Duplicate in Array",
        "shortLabel": "Practice",
        "type": "practice",
        "isGated": true,
        "heading": "Implement Floyd's Tortoise and Hare on Array Graph",
        "subheading": "Find the duplicate number in an array of N+1 integers without extra space.",
        "task": {
            "title": "Duplicate Number Finder",
            "instructions": [
                "Given `nums = [1, 3, 4, 2, 2]`.",
                "In Phase 1, advance `slow = nums[slow]` and `fast = nums[nums[fast]]` until collision.",
                "In Phase 2, reset `slow = 0` (or `nums[0]` if start is 0) and advance both by 1 step until they meet.",
                "Return the meeting value as the duplicate.",
                "Print `'Duplicate number:', duplicate`."
            ],
            "starterCode": "# Day 40 Practice: Duplicate Number Finder\nnums = [1, 3, 4, 2, 2]\n\ndef find_duplicate(arr):\n    # Phase 1: Collision\n    slow = arr[0]\n    fast = arr[0]\n    while True:\n        slow = arr[slow]\n        fast = arr[arr[fast]]\n        if slow == fast:\n            break\n            \n    # Phase 2: Entrance\n    slow = arr[0]\n    while slow != fast:\n        slow = arr[slow]\n        fast = arr[fast]\n        \n    return slow\n\nduplicate = find_duplicate(nums)\nprint(\"Duplicate number:\", duplicate)\n",
            "solutionCode": "nums = [1, 3, 4, 2, 2]\n\ndef find_duplicate(arr):\n    slow = arr[0]\n    fast = arr[0]\n    while True:\n        slow = arr[slow]\n        fast = arr[arr[fast]]\n        if slow == fast:\n            break\n            \n    slow = arr[0]\n    while slow != fast:\n        slow = arr[slow]\n        fast = arr[fast]\n        \n    return slow\n\nduplicate = find_duplicate(nums)\nprint(\"Duplicate number:\", duplicate)\n",
            "expectedOutputPatterns": [
                "Duplicate number: 2"
            ],
            "hint": "Indices: 0->1->3->2->4->2. The cycle is 2->4->2; entrance is 2."
        },
        "keyTakeaway": "Floyd's algorithm treats arrays as functional graphs to locate cycles in O(N) time and O(1) space."
    },
    {
        "id": "day40-step5",
        "stepNumber": 5,
        "title": "Fast & Slow Pointers Mastery",
        "shortLabel": "Recap",
        "type": "completion",
        "isGated": false,
        "dayNumber": 40,
        "heading": "Day 40 Complete: Two Pointers: Fast & Slow",
        "subheading": "Congratulations! You have completed Batch 2 (Days 21 to 40) with complete mastery of asymptotics, recursion, prefix systems, and two-pointer paradigms.",
        "recapRows": [
            {
                "concept": "Cycle Collision Proof",
                "naiveIntuition": "Fast might hop over slow and never meet inside a cycle",
                "pythonReality": "Fast closes the gap by exactly 1 step per cycle, guaranteeing collision"
            },
            {
                "concept": "Array as Graph",
                "naiveIntuition": "Linked list cycle algorithms cannot be applied to arrays",
                "pythonReality": "Treating index -> nums[i] maps arrays directly to functional graphs"
            }
        ],
        "solidifiedConcepts": [
            "Floyd's Tortoise & Hare Mechanics",
            "Relative Speed Collision Guarantee",
            "Phase 1 & Phase 2 Proof",
            "Batch 2 (Days 21-40) Completion"
        ],
        "nextDayPreview": {
            "dayNumber": 41,
            "title": "Sliding Window: Fixed Size",
            "description": "Apply fixed-size sliding windows to compute rolling sums, max averages, and contiguous subarray statistics in O(N) time."
        }
    }
]
},
};
