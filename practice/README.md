# Practice

My Python refresher + LeetCode workspace. Two phases:

1. `syntax/` — relearn the language from zero. Small exercise files. Fill in the `TODO`s, run, repeat.
2. `leetcode/` — problems grouped by pattern. Each problem = a solution file + its own test file.

## Running things

From the repo root:

```bash
# Run a single syntax file (just executes it, prints output)
uv run python practice/syntax/01_basics.py

# Run all tests
uv run pytest practice

# Run tests for one problem
uv run pytest practice/leetcode/arrays_hashing/test_two_sum.py

# Run tests and stop at the first failure, show prints
uv run pytest practice/leetcode/arrays_hashing/test_two_sum.py -x -s

# Lint / autoformat (optional, good habit)
uv run ruff check practice
uv run ruff format practice
```

## Workflow per LeetCode problem

1. Read the problem. Don't code yet — say the approach out loud (or to Claude).
2. Write the function signature + a docstring with the approach and Big-O.
3. Write your tests FIRST (a few normal cases + edge cases).
4. Implement. Run tests. Iterate.
5. Bring the solution here to discuss / get reviewed.

## Log

Track misses in `../LEARNING_LOG.md` and re-do every missed problem ~1 week later.
