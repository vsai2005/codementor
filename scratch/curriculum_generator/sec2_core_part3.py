from .common import (
    CURRICULUM_MAP,
    get_difficulty,
    get_next_preview,
    make_explanation_step,
    make_checkpoint_step,
    make_practice_step,
    make_completion_step,
)

def get_sec2_part3_days():
    days = {}

    # DAY 21: Decorators & Closures
    days[21] = {
        "dayNumber": 21,
        "title": "Decorators & Closures",
        "topicName": "Decorators & Closures",
        "sectionId": "python-core",
        "estimatedMinutes": 35,
        "difficulty": "FOUNDATIONAL",
        "prerequisites": [20],
        "concepts": ["Closure Cells", "Function Wrappers", "functools.wraps", "Decorator Arguments"],
        "practiceSkills": ["Closure Encapsulation", "Timer Decorator Authoring", "functools.wraps Invariant"],
        "steps": [
            make_explanation_step(
                "day21-step1", 1, "Closures & Free Variables", "Closures & Cells",
                "How Closures Work: Functions Retaining Enclosing State",
                "Understand lexical scoping and how Python binds free variables in closure cells.",
                [
                    "A **closure** is a nested function that remembers and retains access to variables in its enclosing scope, even after the outer function has finished executing and its stack frame has been destroyed.",
                    "Python implements closures using **cell objects** (`__closure__`). Instead of putting the enclosed variable on the stack, Python allocates a cell on the heap so both inner and outer functions share the exact same reference.",
                    "Closures form the foundation for decorators, stateful factories, and memoization."
                ],
                snippets=[{
                    "title": "Lexical Closure Cell",
                    "code": "def make_multiplier(factor):\n    def multiply(x):\n        return x * factor # 'factor' is stored in a closure cell\n    return multiply\n\ndouble = make_multiplier(2)\nprint(double(10)) # 20",
                    "language": "python",
                    "caption": "Nested function retaining outer parameter."
                }],
                callouts=[{
                    "type": "tip",
                    "title": "nonlocal Keyword",
                    "content": "To reassign an enclosing variable inside a closure, declare it with `nonlocal count`. Without `nonlocal`, assignment creates a new local variable."
                }],
                takeaway="Closures capture enclosing variables in heap-allocated cell objects."
            ),
            make_explanation_step(
                "day21-step2", 2, "Decorators & functools.wraps", "Decorators & wraps",
                "Syntactic Sugar: @decorator and Preserving Metadata with functools.wraps",
                "Wrap and extend function behavior cleanly.",
                [
                    "A **decorator** is a callable that takes a function as an argument and returns an augmented wrapper function.",
                    "The syntax `@my_decorator` placed above `def func():` is exact syntactic sugar for: `func = my_decorator(func)`.",
                    "Crucially, wrapping a function hides its original name and docstring (`func.__name__` becomes `'wrapper'`). Always use `@functools.wraps(func)` on the wrapper to copy docstrings, annotations, and metadata."
                ],
                snippets=[{
                    "title": "Idiomatic Decorator Template",
                    "code": "import functools\n\ndef log_call(func):\n    @functools.wraps(func)\n    def wrapper(*args, **kwargs):\n        print(f'Calling {func.__name__}...')\n        result = func(*args, **kwargs)\n        print(f'{func.__name__} completed!')\n        return result\n    return wrapper\n\n@log_call\ndef add(a, b):\n    return a + b",
                    "language": "python",
                    "caption": "Standard wrapper pattern with metadata preservation."
                }],
                callouts=[{
                    "type": "warning",
                    "title": "Always Return Result",
                    "content": "A common beginner bug is forgetting `return result` inside the wrapper function, causing decorated functions to return None!"
                }],
                takeaway="@decorator rebinds func = decorator(func); functools.wraps preserves function name and docstrings."
            ),
            make_checkpoint_step(
                "day21-step3", 3, "Decorators Checkpoint", "Checkpoint",
                "Test Your Mastery of Closures and Decorators",
                "Evaluate closure cells and decorator execution timing.",
                [
                    {
                        "id": "chk-d21-q1",
                        "question": "What is the primary purpose of `@functools.wraps(func)` inside a decorator?",
                        "options": [
                            {"id": "A", "label": "It makes the function run 10x faster"},
                            {"id": "B", "label": "It preserves the original function's __name__, __doc__, and signature metadata"},
                            {"id": "C", "label": "It automatically catches all exceptions"},
                            {"id": "D", "label": "It converts synchronous functions to asynchronous"}
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
                            {"id": "A", "label": "Every time the decorated function is called"},
                            {"id": "B", "label": "Once, at the time the function is defined (module import time)"},
                            {"id": "C", "label": "Only when the program terminates"},
                            {"id": "D", "label": "Never; it is purely compile-time annotation"}
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
                takeaway="Decorators execute at definition time; functools.wraps preserves function identity."
            ),
            make_practice_step(
                "day21-step4", 4, "Build an Execution Counter Decorator", "Practice",
                "Track Invocation Counts with a Closure Decorator",
                "Author a decorator that counts how many times a function is called.",
                "Call Counter Decorator",
                [
                    "Write a decorator `count_calls(func)` that tracks invocation count in a local integer `call_count = 0`.",
                    "Use `@functools.wraps(func)` on `wrapper(*args, **kwargs)`.",
                    "Increment `nonlocal call_count` on each call, and print `f'Call {call_count}: {func.__name__}'` before returning `func(*args, **kwargs)`.",
                    "Decorate `def greet(name): return f'Hello, {name}'`.",
                    "Call `greet('Alice')` and `greet('Bob')`."
                ],
                """# Day 21 Practice: Call Counter Decorator
import functools

def count_calls(func):
    call_count = 0
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        print(f"Call {call_count}: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@count_calls
def greet(name):
    return f"Hello, {name}"

greet("Alice")
greet("Bob")
""",
                """import functools

def count_calls(func):
    call_count = 0
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        print(f"Call {call_count}: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@count_calls
def greet(name):
    return f"Hello, {name}"

greet("Alice")
greet("Bob")
""",
                ["Call 1: greet", "Call 2: greet"],
                "Use `nonlocal call_count` inside wrapper to mutate the enclosed counter.",
                takeaway="Decorators leverage closures to maintain state across independent function calls."
            ),
            make_completion_step(
                "day21-step5", 5, "Decorators & Closures Mastery", "Recap",
                21, "Day 21 Complete: Decorators & Closures",
                "You have mastered closure cells, syntactic sugar (@), and metadata preservation.",
                [
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
                ["Closure Heap Cells", "@functools.wraps Invariant", "nonlocal Scope Binding", "Reusable Decorator Pattern"],
                get_next_preview(21)
            )
        ]
    }

    # DAY 22: OOP: Classes & Dunder Methods
    days[22] = {
        "dayNumber": 22,
        "title": "OOP: Classes & Dunder Methods",
        "topicName": "OOP Foundations",
        "sectionId": "python-core",
        "estimatedMinutes": 35,
        "difficulty": "FOUNDATIONAL",
        "prerequisites": [21],
        "concepts": ["__init__, __str__, __repr__", "__eq__ & __hash__", "self parameter", "Instance vs Class Attributes"],
        "practiceSkills": ["Dunder Method Implementation", "Object Equality Contract", "Encapsulation Design"],
        "steps": [
            make_explanation_step(
                "day22-step1", 1, "The Python Data Model & Dunder Methods", "Dunder Methods",
                "Special Methods: Hooking Into Python's Native Operator Overloading",
                "How dunder methods allow user-defined classes to behave like native types.",
                [
                    "In Python, Object-Oriented Programming is powered by the **Python Data Model**. By defining 'dunder' (double underscore) methods, your classes hook directly into Python operators and built-ins.",
                    "`__init__(self, ...)`: Initializes instance attributes after object creation.",
                    "`__repr__(self)`: Returns an unambiguous developer representation (ideally valid Python code to recreate the object).",
                    "`__str__(self)`: Returns a human-readable string used by `print()` and `str()`.",
                    "`__len__(self)` hooks into `len()`, `__getitem__` hooks into `obj[key]`, and `__call__` allows an instance to be invoked like a function."
                ],
                snippets=[{
                    "title": "str vs repr in Action",
                    "code": "class Point:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n    def __repr__(self):\n        return f'Point({self.x}, {self.y})'\n    def __str__(self):\n        return f'({self.x}, {self.y})'\n\np = Point(3, 4)\nprint(str(p))  # '(3, 4)'\nprint(repr(p)) # 'Point(3, 4)'",
                    "language": "python",
                    "caption": "Implementing __repr__ and __str__."
                }],
                callouts=[{
                    "type": "tip",
                    "title": "Always Define __repr__ First",
                    "content": "If `__str__` is not defined, Python falls back to `__repr__`. If you only implement one string method, implement `__repr__`!"
                }],
                takeaway="Dunder methods hook user classes into native Python operators and built-ins."
            ),
            make_explanation_step(
                "day22-step2", 2, "Object Identity, __eq__, and __hash__", "Equality & Hashing",
                "The Contract Between __eq__ and __hash__",
                "Why overriding __eq__ requires careful handling of __hash__ for set/dict membership.",
                [
                    "By default, custom classes compare equality using identity (`is`): two instances are equal only if they are the exact same object in memory.",
                    "Overriding `__eq__(self, other)` allows value-based equality.",
                    "**Crucial Invariant**: If two objects are equal (`a == b`), they **MUST have the exact same hash value (`hash(a) == hash(b)`)**!",
                    "In Python, if you override `__eq__` without defining `__hash__`, Python automatically sets `__hash__ = None`, making the class **unhashable** (cannot be added to sets or used as dict keys) to prevent broken hash table contracts."
                ],
                snippets=[{
                    "title": "Implementing Hashable Classes",
                    "code": "class Coordinate:\n    def __init__(self, r, c):\n        self.r = r\n        self.c = c\n    def __eq__(self, other):\n        return isinstance(other, Coordinate) and (self.r, self.c) == (other.r, other.c)\n    def __hash__(self):\n        return hash((self.r, self.c))\n\ncoords = {Coordinate(1, 2), Coordinate(1, 2)}\nprint(len(coords)) # 1 (properly deduplicated!)",
                    "language": "python",
                    "caption": "Consistent __eq__ and __hash__ enabling set deduplication."
                }],
                callouts=[{
                    "type": "warning",
                    "title": "Mutable Hash Trap",
                    "content": "Only hash immutable attributes! If `self.r` changes after being inserted into a set, the object will be trapped in the wrong hash bucket and impossible to retrieve."
                }],
                takeaway="If a == b is True, hash(a) MUST equal hash(b); overriding __eq__ requires an explicit __hash__."
            ),
            make_checkpoint_step(
                "day22-step3", 3, "OOP Dunder Checkpoint", "Checkpoint",
                "Test Your Mastery of Classes and Dunder Methods",
                "Evaluate string representations and hash contracts.",
                [
                    {
                        "id": "chk-d22-q1",
                        "question": "What happens if you override `__eq__` in a class but do not define `__hash__`?",
                        "options": [
                            {"id": "A", "label": "Python inherits object.__hash__ automatically"},
                            {"id": "B", "label": "Python sets __hash__ = None, making instances unhashable"},
                            {"id": "C", "label": "SyntaxError is raised at definition time"},
                            {"id": "D", "label": "hash() returns 0 for all instances"}
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
                            {"id": "A", "label": "An empty string"},
                            {"id": "B", "label": "TypeError: __str__ required"},
                            {"id": "C", "label": "The output of __repr__ as a fallback"},
                            {"id": "D", "label": "The raw hex memory address"}
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
                takeaway="Python falls back to __repr__ if __str__ is missing; overriding __eq__ disables default hashing."
            ),
            make_practice_step(
                "day22-step4", 4, "Build a Vector2D Class", "Practice",
                "Implement Vector Addition and String Representations",
                "Build a 2D Vector class supporting addition with `__add__`.",
                "Vector2D Vector Class",
                [
                    "Create class `Vector2D` with `__init__(self, x, y)`.",
                    "Implement `__repr__(self)` returning `f'Vector2D({self.x}, {self.y})'`.",
                    "Implement `__add__(self, other)`: return a new `Vector2D(self.x + other.x, self.y + other.y)`.",
                    "Create `v1 = Vector2D(2, 3)` and `v2 = Vector2D(4, 5)`.",
                    "Add them `v3 = v1 + v2` and print `v3`."
                ],
                """# Day 22 Practice: Vector2D Class

class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Vector2D({self.x}, {self.y})"

    # TODO: Implement __add__(self, other) returning new Vector2D
    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

v1 = Vector2D(2, 3)
v2 = Vector2D(4, 5)
v3 = v1 + v2

print("Result:", v3)
""",
                """class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Vector2D({self.x}, {self.y})"

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

v1 = Vector2D(2, 3)
v2 = Vector2D(4, 5)
v3 = v1 + v2

print("Result:", v3)
""",
                ["Result: Vector2D(6, 8)"],
                "Implement `__add__(self, other)` returning `Vector2D(self.x + other.x, self.y + other.y)`.",
                takeaway="Implementing __add__ enables intuitive operator overloading with the + operator."
            ),
            make_completion_step(
                "day22-step5", 5, "OOP & Dunder Methods Mastery", "Recap",
                22, "Day 22 Complete: OOP: Classes & Dunder Methods",
                "You have mastered Python's Data Model, dunder operators, string representations, and hash invariants.",
                [
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
                ["Python Data Model Hooks", "__repr__ vs __str__ Roles", "__eq__ & __hash__ Invariant", "Operator Overloading (__add__)"],
                get_next_preview(22)
            )
        ]
    }

    # DAY 23: Inheritance & Method Resolution Order
    days[23] = {
        "dayNumber": 23,
        "title": "Inheritance & Method Resolution Order",
        "topicName": "Inheritance & MRO",
        "sectionId": "python-core",
        "estimatedMinutes": 35,
        "difficulty": "FOUNDATIONAL",
        "prerequisites": [22],
        "concepts": ["single & multiple inheritance", "super() Mechanics", "MRO C3 Linearization", "isinstance vs type"],
        "practiceSkills": ["super() Delegation", "MRO Tracing", "Polymorphic Hierarchy Design"],
        "steps": [
            make_explanation_step(
                "day23-step1", 1, "Inheritance, super() & Polymorphism", "Inheritance & super()",
                "Class Hierarchies and Cooperative Multiple Inheritance with super()",
                "Understand why super() does not simply mean 'call parent'.",
                [
                    "Inheritance allows a child class to inherit attributes and methods from one or more base classes: `class Child(Base):`.",
                    "`super().__init__(...)` delegates attribute initialization to the next class in the inheritance chain.",
                    "In Python, `super()` does not just look at the immediate parent: it follows the **Method Resolution Order (MRO)** dynamically, making cooperative multiple inheritance possible.",
                    "Always test types using `isinstance(obj, ClassName)` rather than `type(obj) is ClassName`, because `isinstance` respects the inheritance hierarchy."
                ],
                snippets=[{
                    "title": "super() and Polymorphism",
                    "code": "class Animal:\n    def speak(self):\n        return 'Some sound'\n\nclass Dog(Animal):\n    def speak(self):\n        return 'Woof!'\n\ndef make_speak(animal: Animal):\n    print(animal.speak()) # Polymorphic dispatch\n\nmake_speak(Dog()) # 'Woof!'",
                    "language": "python",
                    "caption": "Polymorphic method resolution."
                }],
                callouts=[{
                    "type": "tip",
                    "title": "Use isinstance, Not type()",
                    "content": "`isinstance(Dog(), Animal)` is True! `type(Dog()) is Animal` is False. Never use `type()` equality when verifying interfaces."
                }],
                takeaway="super() delegates up the MRO chain; isinstance() respects subclass relationships."
            ),
            make_explanation_step(
                "day23-step2", 2, "Method Resolution Order & C3 Linearization", "MRO & C3",
                "The Diamond Problem and How C3 Linearization Computes Class.__mro__",
                "How Python resolves method ambiguity in multiple inheritance.",
                [
                    "When a class inherits from multiple parents (`class D(B, C):`), Python must decide which version of a method to execute (the **Diamond Problem**).",
                    "Python resolves this using the **C3 Linearization Algorithm**, which guarantees three invariants:",
                    "1. Subclasses appear before their parents.",
                    "2. Order of base classes listed in definition is strictly preserved.",
                    "3. Monotonicity: no class is visited twice or reordered.",
                    "You can inspect any class's exact lookup order with `Class.__mro__` or `Class.mro()`."
                ],
                snippets=[{
                    "title": "Inspecting MRO in Diamond Inheritance",
                    "code": "class A: pass\nclass B(A): pass\nclass C(A): pass\nclass D(B, C): pass\n\nprint([cls.__name__ for cls in D.__mro__])\n# ['D', 'B', 'C', 'A', 'object']",
                    "language": "python",
                    "caption": "C3 linearization order for diamond inheritance."
                }],
                callouts=[{
                    "type": "warning",
                    "title": "Inconsistent Hierarchy Rejection",
                    "content": "If you construct an impossible inheritance order (e.g. `class A(B)` and `class B(A)`), Python raises `TypeError: Cannot create a consistent method resolution order (MRO)`."
                }],
                takeaway="Python resolves multiple inheritance via C3 linearization, accessible via Class.__mro__."
            ),
            make_checkpoint_step(
                "day23-step3", 3, "Inheritance & MRO Checkpoint", "Checkpoint",
                "Test Your Mastery of Inheritance and MRO",
                "Trace method resolution orders and type checks.",
                [
                    {
                        "id": "chk-d23-q1",
                        "question": "If `class Square(Rectangle): pass`, what is the result of `isinstance(Square(5), Rectangle)`?",
                        "options": [
                            {"id": "A", "label": "True"},
                            {"id": "B", "label": "False"},
                            {"id": "C", "label": "TypeError"},
                            {"id": "D", "label": "None"}
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
                            {"id": "A", "label": "type"},
                            {"id": "B", "label": "object"},
                            {"id": "C", "label": "BaseException"},
                            {"id": "D", "label": "NoneClass"}
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
                takeaway="isinstance() checks the subclass hierarchy; object is the root class of all Python types."
            ),
            make_practice_step(
                "day23-step4", 4, "Shape Hierarchy with Polymorphism", "Practice",
                "Implement Polymorphic Shape Calculators",
                "Create a Shape base class with polymorphic area calculation.",
                "Shape Area Hierarchy",
                [
                    "Create base class `Shape` with method `area(self)` returning `0.0`.",
                    "Create subclass `Rectangle(Shape)` with `__init__(self, w, h)` and `area(self)` returning `w * h`.",
                    "Create subclass `Square(Rectangle)` with `__init__(self, side)` that calls `super().__init__(side, side)`.",
                    "Instantiate `sq = Square(4)` and print `'Square area:', sq.area()`."
                ],
                """# Day 23 Practice: Shape Area Hierarchy

class Shape:
    def area(self):
        return 0.0

class Rectangle(Shape):
    def __init__(self, w, h):
        self.w = w
        self.h = h

    def area(self):
        return float(self.w * self.h)

# TODO: Implement Square inheriting from Rectangle using super().__init__(side, side)
class Square(Rectangle):
    def __init__(self, side):
        super().__init__(side, side)

sq = Square(4)
print("Square area:", sq.area())
""",
                """class Shape:
    def area(self):
        return 0.0

class Rectangle(Shape):
    def __init__(self, w, h):
        self.w = w
        self.h = h

    def area(self):
        return float(self.w * self.h)

class Square(Rectangle):
    def __init__(self, side):
        super().__init__(side, side)

sq = Square(4)
print("Square area:", sq.area())
""",
                ["Square area: 16.0"],
                "Use `super().__init__(side, side)` inside Square's `__init__`.",
                takeaway="super() allows subclasses to delegate initialization to base classes cleanly."
            ),
            make_completion_step(
                "day23-step5", 5, "Inheritance & MRO Mastery", "Recap",
                23, "Day 23 Complete: Inheritance & Method Resolution Order",
                "You have mastered super() delegation, polymorphic method dispatch, and C3 linearization.",
                [
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
                ["super().__init__() Delegation", "MRO & C3 Linearization Invariants", "isinstance() Polymorphic Checking", "Diamond Inheritance Resolution"],
                get_next_preview(23)
            )
        ]
    }

    # DAY 24: Exceptions, Tracebacks & Custom Errors
    days[24] = {
        "dayNumber": 24,
        "title": "Exceptions, Tracebacks & Custom Errors",
        "topicName": "Exception Handling",
        "sectionId": "python-core",
        "estimatedMinutes": 30,
        "difficulty": "FOUNDATIONAL",
        "prerequisites": [23],
        "concepts": ["try/except/else/finally", "Custom Exception Subclasses", "Exception Chaining", "EAFP vs LBYL"],
        "practiceSkills": ["Custom Exception Creation", "try/except/else/finally Flow", "EAFP Defensive Programming"],
        "steps": [
            make_explanation_step(
                "day24-step1", 1, "Exception Flow: try, except, else, finally", "Exception Lifecycle",
                "The Complete Exception Handling Lifecycle in Python",
                "Understand the distinct roles of except, else, and finally.",
                [
                    "Python uses structured exception handling with four complementary clauses:",
                    "- `try`: Code that might raise an exception.",
                    "- `except ExceptionType as err`: Executes only if a matching exception is raised.",
                    "- `else`: Executes **only if NO exception occurred** in the try block.",
                    "- `finally`: Executes **unconditionally**, whether an exception occurred, was handled, or even if `return` was called! Ideal for releasing locks and closing files.",
                    "Python embraces the **EAFP** philosophy ('Easier to Ask for Forgiveness than Permission'): prefer attempting operations in a try block rather than running defensive pre-checks (LBYL)."
                ],
                snippets=[{
                    "title": "Complete try/except/else/finally",
                    "code": "def divide(a, b):\n    try:\n        res = a / b\n    except ZeroDivisionError:\n        print('Cannot divide by zero!')\n        return None\n    else:\n        print('Division successful!')\n        return res\n    finally:\n        print('Cleanup complete.') # Always runs!",
                    "language": "python",
                    "caption": "All four exception blocks in action."
                }],
                callouts=[{
                    "type": "tip",
                    "title": "Keep Try Blocks Minimal",
                    "content": "Only place the specific statement that could raise an error inside the `try:` block. Code that runs upon success belongs in the `else:` block."
                }],
                takeaway="try guards, except catches, else runs on success, and finally executes unconditionally."
            ),
            make_explanation_step(
                "day24-step2", 2, "Custom Exceptions & Exception Chaining", "Custom Exceptions",
                "Authoring Domain Exceptions and Chaining with 'from'",
                "Build meaningful exception hierarchies for enterprise architectures.",
                [
                    "To create custom exceptions, inherit from Python's built-in `Exception` (never `BaseException`, which includes `KeyboardInterrupt` and `SystemExit`).",
                    "When catching a low-level error and raising a high-level domain error, preserve the original traceback using exception chaining: `raise CustomError('...') from original_err`.",
                    "This sets `__cause__` and outputs explicit context: `'The above exception was the direct cause of the following exception'`. "
                ],
                snippets=[{
                    "title": "Custom Exception with Chaining",
                    "code": "class ValidationError(Exception):\n    \"\"\"Raised when input data fails domain constraints.\"\"\"\n    pass\n\ndef parse_age(raw):\n    try:\n        return int(raw)\n    except ValueError as err:\n        raise ValidationError(f'Invalid age token: {raw}') from err",
                    "language": "python",
                    "caption": "Preserving root causes with 'from err'."
                }],
                callouts=[{
                    "type": "warning",
                    "title": "Never Bare 'except:'",
                    "content": "Writing bare `except:` catches `KeyboardInterrupt` (Ctrl+C) and `SystemExit`, making programs impossible to terminate! Always write `except Exception:`."
                }],
                takeaway="Custom exceptions inherit from Exception; 'raise ... from err' preserves root cause tracebacks."
            ),
            make_checkpoint_step(
                "day24-step3", 3, "Exceptions Checkpoint", "Checkpoint",
                "Test Your Mastery of Exception Flow and Chaining",
                "Trace finally execution and exception inheritance.",
                [
                    {
                        "id": "chk-d24-q1",
                        "question": "What will this function return?\n\n```python\ndef test():\n    try:\n        return 1\n    finally:\n        return 2\n```",
                        "options": [
                            {"id": "A", "label": "1"},
                            {"id": "B", "label": "2"},
                            {"id": "C", "label": "SyntaxError"},
                            {"id": "D", "label": "None"}
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
                            {"id": "A", "label": "BaseException is not a valid class in Python 3"},
                            {"id": "B", "label": "BaseException includes system-exiting signals like KeyboardInterrupt and SystemExit, which application code should not catch"},
                            {"id": "C", "label": "Exception is faster"},
                            {"id": "D", "label": "There is no difference"}
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
                takeaway="finally overrides prior returns; inherit from Exception to allow graceful system interruption."
            ),
            make_practice_step(
                "day24-step4", 4, "Build a Validated Bank Account", "Practice",
                "Enforce Balance Limits with InsufficientFundsError",
                "Create a custom domain exception and raise it when balance is insufficient.",
                "Bank Account Balance Guard",
                [
                    "Create custom exception `InsufficientFundsError(Exception)`.",
                    "Create class `BankAccount` with `__init__(self, balance)`.",
                    "Implement `withdraw(self, amount)`: if `amount > self.balance`, raise `InsufficientFundsError(f'Deficit of {amount - self.balance}')`.",
                    "Otherwise deduct `self.balance -= amount` and return `self.balance`.",
                    "In test code, catch `InsufficientFundsError as err` and print `'Caught:', type(err).__name__`."
                ],
                """# Day 24 Practice: Bank Account Balance Guard

class InsufficientFundsError(Exception):
    pass

class BankAccount:
    def __init__(self, balance):
        self.balance = balance

    def withdraw(self, amount):
        # TODO: If amount > balance, raise InsufficientFundsError
        if amount > self.balance:
            raise InsufficientFundsError(f"Deficit of {amount - self.balance}")
        self.balance -= amount
        return self.balance

account = BankAccount(100)

try:
    account.withdraw(150)
except InsufficientFundsError as err:
    print("Caught:", type(err).__name__)
""",
                """class InsufficientFundsError(Exception):
    pass

class BankAccount:
    def __init__(self, balance):
        self.balance = balance

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFundsError(f"Deficit of {amount - self.balance}")
        self.balance -= amount
        return self.balance

account = BankAccount(100)

try:
    account.withdraw(150)
except InsufficientFundsError as err:
    print("Caught:", type(err).__name__)
""",
                ["Caught: InsufficientFundsError"],
                "Raise `InsufficientFundsError` inside `withdraw` when amount exceeds balance.",
                takeaway="Custom domain exceptions communicate business invariant violations with precision."
            ),
            make_completion_step(
                "day24-step5", 5, "Exceptions & Tracebacks Mastery", "Recap",
                24, "Day 24 Complete: Exceptions, Tracebacks & Custom Errors",
                "You have mastered try/except/else/finally lifecycle, custom errors, and exception chaining.",
                [
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
                ["try/except/else/finally Architecture", "EAFP vs LBYL Paradigms", "Custom Exception Subclasses", "Exception Chaining with 'from'"],
                get_next_preview(24)
            )
        ]
    }

    # DAY 25: Section 2 Review & Pythonic Mastery
    days[25] = {
        "dayNumber": 25,
        "title": "Section 2 Review & Pythonic Mastery",
        "topicName": "Section 2 Synthesis",
        "sectionId": "python-core",
        "estimatedMinutes": 35,
        "difficulty": "FOUNDATIONAL",
        "prerequisites": [24],
        "concepts": ["Composite Data Structures Synthesis", "Generators & Iterators", "OOP & Dunder Methods", "Pythonic Idioms"],
        "practiceSkills": ["Multi-Paradigm Synthesis", "Custom Data Structure Design", "Memory & Algorithm Efficiency"],
        "steps": [
            make_explanation_step(
                "day25-step1", 1, "Python Core Architecture Synthesis", "Section 2 Model",
                "Synthesizing Python Core: Data Structures, Protocols & OOP",
                "Review the major milestones achieved across Days 11 to 24.",
                [
                    "In Section 2, you transitioned from basic syntax to the core machinery of Python:",
                    "1. **Contiguous Arrays & Hash Tables**: Lists are pointer arrays with amortized $O(1)$ append; dicts and sets are open-addressing hash tables with $O(1)$ lookup.",
                    "2. **Iteration Protocols & Generators**: `__iter__` and `__next__` define the universal streaming protocol; generators (`yield`) suspend frames for $O(1)$ memory consumption.",
                    "3. **Metaprogramming & OOP**: Decorators leverage closure cells to wrap behavior; dunder methods (`__eq__`, `__repr__`, `__add__`) hook into Python's native runtime.",
                    "4. **Defensive Architecture**: Exceptions cleanly separate normal flow from error handling using EAFP and custom hierarchy trees."
                ],
                snippets=[{
                    "title": "Integrated Python Core Architecture",
                    "code": "from collections import deque\n\nclass TaskQueue:\n    \"\"\"Combines OOP, deque O(1) pops, and iterator protocol.\"\"\"\n    def __init__(self):\n        self._tasks = deque()\n    def push(self, task):\n        self._tasks.append(task)\n    def pop(self):\n        return self._tasks.popleft() if self._tasks else None\n    def __iter__(self):\n        while self._tasks:\n            yield self._tasks.popleft()",
                    "language": "python",
                    "caption": "Combining OOP, collections.deque, and generator yield."
                }],
                callouts=[{
                    "type": "tip",
                    "title": "Bridge to DSA",
                    "content": "With complete mastery of Python's memory model, pointer arrays, hash maps, deques, and protocols, you are ready to study Computational Thinking and Big-O in Section 3!"
                }],
                takeaway="Mastery of Python's data model and memory characteristics is the prerequisite for rigorous algorithm design."
            ),
            make_explanation_step(
                "day25-step2", 2, "Pythonic Style Guide & Complexity Invariants", "Pythonic Invariants",
                "The Zen of Python in Algorithmic Code",
                "Key algorithmic invariants to remember when moving into DSA.",
                [
                    "As you transition into Data Structures and Algorithms:",
                    "- **Never use `list.pop(0)`**: It is $O(N)$. Always use `collections.deque.popleft()` ($O(1)$).",
                    "- **Never do `item in list` inside a loop**: It turns an $O(N)$ algorithm into $O(N^2)$. Convert to a `set` ($O(1)$).",
                    "- **Never concatenate strings in a loop (`s += ch`)**: It allocates a new string each time ($O(N^2)$). Use `''.join(list_of_chars)` ($O(N)$).",
                    "- **Always use list comprehensions or generators**: They avoid attribute lookup overhead."
                ],
                snippets=[{
                    "title": "Anti-Pattern vs Pythonic Invariants",
                    "code": "# Anti-pattern: O(N^2) string building\ns = ''\nfor ch in ['a', 'b', 'c']:\n    s += ch # Allocates new string every iteration!\n\n# Pythonic: O(N) string joining\ns_clean = ''.join(['a', 'b', 'c']) # Single contiguous allocation",
                    "language": "python",
                    "caption": "Avoid quadratic string concatenation."
                }],
                callouts=[{
                    "type": "deep-dive",
                    "title": "CPython join() Optimization",
                    "content": "`''.join()` precalculates the total byte length of all strings, allocates the exact memory buffer once, and copies all bytes in C."
                }],
                takeaway="''.join(seq) is O(N); set membership is O(1); deque.popleft() is O(1)."
            ),
            make_checkpoint_step(
                "day25-step3", 3, "Python Core Milestone Checkpoint", "Checkpoint",
                "Verify Section 2 Mastery Across Core Tenets",
                "Test your synthesized mental model of Python composite types and OOP.",
                [
                    {
                        "id": "chk-d25-q1",
                        "question": "Which operation sequence runs in strictly $O(N)$ total time for an input of size N?",
                        "options": [
                            {"id": "A", "label": "Checking if an item exists in a list for each of N items"},
                            {"id": "B", "label": "Popping N elements from index 0 of a list using lst.pop(0)"},
                            {"id": "C", "label": "Converting a list of N elements into a set, then checking membership N times in the set"},
                            {"id": "D", "label": "Concatenating N single characters using s += ch in a loop"}
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
                            {"id": "A", "label": "yield terminates the function immediately"},
                            {"id": "B", "label": "yield suspends the execution frame and retains state; return destroys the frame"},
                            {"id": "C", "label": "yield can only produce integers"},
                            {"id": "D", "label": "return functions are always faster"}
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
                takeaway="Set lookup drops nested searches from O(N^2) to O(N); generators freeze execution frames."
            ),
            make_practice_step(
                "day25-step4", 4, "Synthesize: LRU Memory Buffer Preview", "Practice",
                "Build an Ordered Task Buffer with deque",
                "Implement a bounded task buffer that retains the last K items in O(1) time.",
                "Bounded Task Buffer",
                [
                    "Use `collections.deque(maxlen=3)` to implement a fixed-capacity buffer.",
                    "Append tasks `'task1'`, `'task2'`, `'task3'`, `'task4'` to the buffer.",
                    "Observe that when capacity exceeds 3, the oldest item `'task1'` is automatically discarded in $O(1)$ time.",
                    "Print `'Buffer contents:', list(buffer)` and `'Buffer size:', len(buffer)`."
                ],
                """# Day 25 Practice: Bounded Task Buffer
from collections import deque

# TODO 1: Initialize deque with maxlen=3
buffer = deque(maxlen=3)

# TODO 2: Append 'task1', 'task2', 'task3', 'task4'
buffer.append("task1")
buffer.append("task2")
buffer.append("task3")
buffer.append("task4")

print("Buffer contents:", list(buffer))
print("Buffer size:", len(buffer))
""",
                """from collections import deque

buffer = deque(maxlen=3)
buffer.append("task1")
buffer.append("task2")
buffer.append("task3")
buffer.append("task4")

print("Buffer contents:", list(buffer))
print("Buffer size:", len(buffer))
""",
                ["Buffer contents: ['task2', 'task3', 'task4']", "Buffer size: 3"],
                "Initialize `deque(maxlen=3)` and append all four tasks.",
                takeaway="deque with maxlen automatically drops overflow elements in O(1) time, perfect for ring buffers."
            ),
            make_completion_step(
                "day25-step5", 5, "Section 2 Core Mastery", "Recap",
                25, "Day 25 Complete: Section 2 Review & Pythonic Mastery",
                "Congratulations! You have completed Section 2: Python Core & Data Structures with complete mastery of memory, data types, OOP, and protocols.",
                [
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
                ["Dynamic Arrays & Hash Tables", "collections.deque O(1) Invariants", "Generators & Iteration Protocols", "OOP, super() & Dunder Methods", "Section 2 Completion"],
                get_next_preview(25)
            )
        ]
    }

    return days
