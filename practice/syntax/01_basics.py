"""
Syntax warmup 01 — variables, types, printing, basic operators.

HOW TO USE THIS FILE:
- Each task is a comment starting with `# TODO`.
- Write the code yourself, right below the TODO.
- Run it:  uv run python practice/syntax/01_basics.py
- The `check(...)` calls at the bottom will tell you if you got it right.

No solutions are in this file. That's the point. Struggle a little.
"""


# TODO 1: Create a variable `name` holding your first name as a string,
#         and a variable `age` holding your age as an integer.
name = "Dylan"
age = 27

# TODO 2: Print a single line that says:  "<name> is <age> years old"
#         Use an f-string.
print(f"{name} is {age} years old")

# TODO 3: Create `a = 17` and `b = 5`. Compute and store:
#         q  -> integer (floor) division of a by b
#         r  -> remainder of a divided by b
#         f  -> true (float) division of a by b
a = 17
b = 5
q = a // b
r = a % b
f = a / b


# TODO 4: You have the string `s = "leetcode"`. Without retyping the letters:
#         length -> its length
#         shout  -> the same string in ALL CAPS
#         rev    -> the string reversed   (hint: slicing with a step)
s = "leetcode"
length = len(s)
shout = s.upper()
rev = s[::-1]


# TODO 5: Booleans & truthiness. Set `empty = []`.
#         is_empty -> a boolean that is True when `empty` has no items,
#                     computed WITHOUT using len(). (hint: truthiness)
empty = []
is_empty = empty == []


# ----------------------------------------------------------------------
# Don't edit below this line. These checks grade your work.
# ----------------------------------------------------------------------
def check(label, got, want):
    ok = got == want
    print(f"[{'PASS' if ok else 'FAIL'}] {label}: got {got!r}", "" if ok else f"(want {want!r})")


if __name__ == "__main__":
    try:
        check("TODO3 q", q, 3)
        check("TODO3 r", r, 2)
        check("TODO3 f", f, 3.4)
        check("TODO4 length", length, 8)
        check("TODO4 shout", shout, "LEETCODE")
        check("TODO4 rev", rev, "edocteel")
        check("TODO5 is_empty", is_empty, True)
    except NameError as e:
        print("Not done yet —", e)
