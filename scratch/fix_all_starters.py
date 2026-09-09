"""
Fix pre-solved starter code across:
- sec2_core_part1.py (Day 11)
- sec2_core_part2.py (Days 19, 20)
- gen_batch2_part1.py (Days 21, 22, 25)
- sec3_and_sec4_part.py (Days 35, 36, 37, 38, 39, 40)
"""

# Fix sec2_core_part1.py Day 11
with open("scratch/curriculum_generator/sec2_core_part1.py", "r", encoding="utf-8") as f:
    text = f.read()

old_d11_starter = '''nums = [12, 5, 8, 19, 24, 7, 10]

# TODO 1: Retain only elements > 10 in nums
nums = [x for x in nums if x > 10]

# TODO 2: Reverse nums in-place
# Call .reverse() on nums

print("Processed list:", nums)'''

new_d11_starter = '''nums = [12, 5, 8, 19, 24, 7, 10]

# TODO 1: Retain only elements > 10 in nums
# (Filter nums by keeping only numbers > 10)
nums = [x for x in nums if x > 10]
# Reset nums to trigger active coding:
nums = [12, 5, 8, 19, 24, 7, 10]
# TODO 1: Filter nums so it retains only numbers greater than 10
filtered = []
for x in nums:
    if x > 10:
        filtered.append(x)
nums = filtered

# TODO 2: Reverse nums in-place by calling .reverse()

print("Processed list:", nums)'''

# Wait, let's make it cleaner without duplicate definitions:
clean_d11_starter = '''nums = [12, 5, 8, 19, 24, 7, 10]

# TODO 1: Filter nums to retain only numbers greater than 10
# (Build a list of numbers > 10 or filter in a loop)
nums = []

# TODO 2: Reverse nums in-place by calling nums.reverse()

print("Processed list:", nums)'''

if old_d11_starter in text:
    text = text.replace(old_d11_starter, clean_d11_starter)
    with open("scratch/curriculum_generator/sec2_core_part1.py", "w", encoding="utf-8") as f:
        f.write(text)
    print("Fixed Day 11 in sec2_core_part1.py")


# Fix sec2_core_part2.py Days 19, 20
with open("scratch/curriculum_generator/sec2_core_part2.py", "r", encoding="utf-8") as f:
    text = f.read()

old_d19 = '''    def __next__(self):
        # TODO: Return self.current and advance by 2; raise StopIteration when > max_limit
        if self.current > self.max_limit:
            raise StopIteration
        val = self.current
        self.current += 2
        return val'''

new_d19 = '''    def __next__(self):
        # TODO: If self.current > self.max_limit, raise StopIteration
        # Otherwise save val = self.current, increment self.current by 2, and return val
        pass'''

old_d20 = '''def batch_stream(items, batch_size):
    # TODO: Yield chunks of items from 0 to len(items) with step batch_size
    for i in range(0, len(items), batch_size):
        yield items[i : i + batch_size]'''

new_d20 = '''def batch_stream(items, batch_size):
    # TODO: Loop i from 0 to len(items) with step batch_size
    # and yield slice items[i : i + batch_size]
    pass'''

if old_d19 in text:
    text = text.replace(old_d19, new_d19)
if old_d20 in text:
    text = text.replace(old_d20, new_d20)

with open("scratch/curriculum_generator/sec2_core_part2.py", "w", encoding="utf-8") as f:
    f.write(text)
print("Fixed Days 19 & 20 in sec2_core_part2.py")


# Fix gen_batch2_part1.py Days 21, 22, 25
with open("scratch/curriculum_generator/gen_batch2_part1.py", "r", encoding="utf-8") as f:
    text = f.read()

old_d21 = '''def count_calls(func):
    call_count = 0
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        print(f"Call {call_count}: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper'''

new_d21 = '''def count_calls(func):
    call_count = 0
    # TODO: Implement wrapper that increments call_count, prints f"Call {call_count}: {func.__name__}",
    # and returns func(*args, **kwargs)
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal call_count
        # Increment call_count, print message, and return func(*args, **kwargs)
        pass
    return wrapper'''

old_d22 = '''    # TODO: Implement __add__(self, other) returning new Vector2D
    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)'''

new_d22 = '''    # TODO: Implement __add__(self, other) returning new Vector2D(self.x + other.x, self.y + other.y)
    def __add__(self, other):
        pass'''

old_d25 = '''# TODO 1: Initialize deque with maxlen=3
buffer = deque(maxlen=3)

# TODO 2: Append 'task1', 'task2', 'task3', 'task4'
buffer.append("task1")
buffer.append("task2")
buffer.append("task3")
buffer.append("task4")'''

new_d25 = '''# TODO 1: Initialize deque with maxlen=3
buffer = None

# TODO 2: Append 'task1', 'task2', 'task3', 'task4' to buffer
'''

if old_d21 in text:
    text = text.replace(old_d21, new_d21)
if old_d22 in text:
    text = text.replace(old_d22, new_d22)
if old_d25 in text:
    text = text.replace(old_d25, new_d25)

with open("scratch/curriculum_generator/gen_batch2_part1.py", "w", encoding="utf-8") as f:
    f.write(text)
print("Fixed Days 21, 22, 25 in gen_batch2_part1.py")


# Fix sec3_and_sec4_part.py Days 35, 36, 37, 38, 39, 40
with open("scratch/curriculum_generator/sec3_and_sec4_part.py", "r", encoding="utf-8") as f:
    text = f.read()

# Day 35
old_d35 = '''# Day 35 Practice: Equilibrium Index Solver
nums = [1, 7, 3, 6, 5, 6]

total_sum = sum(nums)
left_sum = 0
eq_idx = -1

for i, x in enumerate(nums):
    right_sum = total_sum - left_sum - x
    if left_sum == right_sum:
        eq_idx = i
        break
    left_sum += x

print("Equilibrium index:", eq_idx)'''

new_d35 = '''# Day 35 Practice: Equilibrium Index Solver
nums = [1, 7, 3, 6, 5, 6]

total_sum = sum(nums)
left_sum = 0
eq_idx = -1

# TODO: Iterate with enumerate(nums)
# If left_sum == total_sum - left_sum - x: set eq_idx = i and break
# Else add x to left_sum

print("Equilibrium index:", eq_idx)'''

if old_d35 in text:
    text = text.replace(old_d35, new_d35)

# Day 36
old_d36 = '''# Day 36 Practice: Robust Palindrome Checker
s = "A man, a plan, a canal: Panama"

def check_palindrome(text):
    left, right = 0, len(text) - 1
    while left < right:
        while left < right and not text[left].isalnum():
            left += 1
        while left < right and not text[right].isalnum():
            right -= 1
        if text[left].lower() != text[right].lower():
            return False
        left += 1
        right -= 1
    return True

print("Is palindrome:", check_palindrome(s))'''

new_d36 = '''# Day 36 Practice: Robust Palindrome Checker
s = "A man, a plan, a canal: Panama"

def check_palindrome(text):
    left, right = 0, len(text) - 1
    # TODO: While left < right, skip non-alphanumeric with isalnum()
    # and compare text[left].lower() != text[right].lower()
    return False

print("Is palindrome:", check_palindrome(s))'''

if old_d36 in text:
    text = text.replace(old_d36, new_d36)

# Day 37
old_d37 = '''# Day 37 Practice: Subsequence Batch Checker
source = "ahbgdc"
words = ["abc", "axc", "bgd"]

def is_sub(s, t):
    i, j = 0, 0
    while i < len(s) and j < len(t):
        if s[i] == t[j]:
            i += 1
        j += 1
    return i == len(s)

matches = [w for w in words if is_sub(w, source)]
print("Matched words:", matches)'''

new_d37 = '''# Day 37 Practice: Subsequence Batch Checker
source = "ahbgdc"
words = ["abc", "axc", "bgd"]

def is_sub(s, t):
    # TODO: Check if s is a subsequence of t using two pointers i and j
    return False

matches = [w for w in words if is_sub(w, source)]
print("Matched words:", matches)'''

if old_d37 in text:
    text = text.replace(old_d37, new_d37)

# Day 38
old_d38 = '''# Day 38 Practice: In-Place Element Remover
nums = [3, 2, 2, 3, 4, 3, 5]
val = 3

write = 0
for read in range(len(nums)):
    if nums[read] != val:
        nums[write] = nums[read]
        write += 1

print("Remaining elements:", nums[:write])
print("New length:", write)'''

new_d38 = '''# Day 38 Practice: In-Place Element Remover
nums = [3, 2, 2, 3, 4, 3, 5]
val = 3

write = 0
# TODO: Loop read in range(len(nums)): if nums[read] != val: copy to nums[write] and write += 1

print("Remaining elements:", nums[:write])
print("New length:", write)'''

if old_d38 in text:
    text = text.replace(old_d38, new_d38)

# Day 39
old_d39 = '''# Day 39 Practice: Water Container Maximizer
heights = [1, 8, 6, 2, 5, 4, 8, 3, 7]

left, right = 0, len(heights) - 1
max_water = 0

while left < right:
    w = right - left
    h = min(heights[left], heights[right])
    max_water = max(max_water, w * h)
    if heights[left] < heights[right]:
        left += 1
    else:
        right -= 1

print("Max water trapped:", max_water)'''

new_d39 = '''# Day 39 Practice: Water Container Maximizer
heights = [1, 8, 6, 2, 5, 4, 8, 3, 7]

left, right = 0, len(heights) - 1
max_water = 0

# TODO: While left < right, calculate area (right - left) * min(h[left], h[right])
# Update max_water and move pointer with smaller height inward

print("Max water trapped:", max_water)'''

if old_d39 in text:
    text = text.replace(old_d39, new_d39)

# Day 40
old_d40 = '''# Day 40 Practice: Duplicate Number Finder
nums = [1, 3, 4, 2, 2]

def find_duplicate(arr):
    # Phase 1: Collision
    slow = arr[0]
    fast = arr[0]
    while True:
        slow = arr[slow]
        fast = arr[arr[fast]]
        if slow == fast:
            break
            
    # Phase 2: Entrance
    slow = arr[0]
    while slow != fast:
        slow = arr[slow]
        fast = arr[fast]
    return slow

print("Duplicate number:", find_duplicate(nums))'''

new_d40 = '''# Day 40 Practice: Duplicate Number Finder
nums = [1, 3, 4, 2, 2]

def find_duplicate(arr):
    # TODO 1: Phase 1 - Find collision using slow = arr[slow] and fast = arr[arr[fast]]
    slow, fast = arr[0], arr[0]
    
    # TODO 2: Phase 2 - Find cycle entrance by resetting slow = arr[0] and advancing both 1 step
    return -1

print("Duplicate number:", find_duplicate(nums))'''

if old_d40 in text:
    text = text.replace(old_d40, new_d40)

with open("scratch/curriculum_generator/sec3_and_sec4_part.py", "w", encoding="utf-8") as f:
    f.write(text)
print("Fixed Days 35..40 in sec3_and_sec4_part.py")
