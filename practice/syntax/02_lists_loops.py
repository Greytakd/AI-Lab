"""
Syntax warmup 02 — lists, conditionals, loops, functions.

Same rules as before:
- Write code under each `# TODO`.
- Run it:  uv run python practice/syntax/02_lists_loops.py
- Aim for all PASS. No solutions in this file.
"""


# TODO 1: Start with nums = [5, 3, 8, 1].
#         Append 10 to the end (mutate the list, don't rebuild it).
#         first -> the first element
#         last  -> the last element (use negative indexing, not nums[4])
nums = [5, 3, 8, 1]
nums.append(10)
first = nums[0]
last = nums[-1]

# TODO 2: Given vals below, compute `total` = the sum of all elements
#         using a for-loop and a running accumulator.
#         (Yes, sum() exists — but write the loop, that's the drill.)
vals = [4, 9, 2, 7]
total = 0
for x in vals:
    total += x

# TODO 3: Given words below, build `labeled` = a list of strings of the form
#         "<index>:<word>", e.g. "0:two". Use enumerate.
#         Expected: ["0:two", "1:pointers", "2:rule"]
words = ["two", "pointers", "rule"]
labeled = []
for i, num in enumerate(words): 
    labeled.append(f"{i}:{num}")

# TODO 4: Write a function classify(n) that returns:
#         "neg"  if n < 0
#         "zero" if n == 0
#         "pos"  if n > 0
#         Use if / elif / else.
def classify(n):
    if n < 0:
        return "neg"
    elif n > 0:
        return "pos"
    else:
        return "zero"


# TODO 5: Membership. Given haystack below, set `found` to a boolean that is
#         True if 8 is present. Use the `in` operator (no loop).
haystack = [2, 4, 8, 16]
found = 8 in haystack

# TODO 6: While loop. Starting from n = 25, count how many times you can do
#         integer-divide-by-2 (n = n // 2) until n becomes 0.
#         Store the count in `steps`.  (25 -> 12 -> 6 -> 3 -> 1 -> 0 = 5 steps)
n = 25
steps = 0
while n > 0:
    n = n // 2
    steps += 1

# ----------------------------------------------------------------------
# Don't edit below this line.
# ----------------------------------------------------------------------
def check(label, got, want):
    ok = got == want
    print(f"[{'PASS' if ok else 'FAIL'}] {label}: got {got!r}", "" if ok else f"(want {want!r})")


if __name__ == "__main__":
    try:
        check("TODO1 nums", nums, [5, 3, 8, 1, 10])
        check("TODO1 first", first, 5)
        check("TODO1 last", last, 10)
        check("TODO2 total", total, 22)
        check("TODO3 labeled", labeled, ["0:two", "1:pointers", "2:rule"])
        check("TODO4 classify(-3)", classify(-3), "neg")
        check("TODO4 classify(0)", classify(0), "zero")
        check("TODO4 classify(9)", classify(9), "pos")
        check("TODO5 found", found, True)
        check("TODO6 steps", steps, 5)
    except NameError as e:
        print("Not done yet —", e)
