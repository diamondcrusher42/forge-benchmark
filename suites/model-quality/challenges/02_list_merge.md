# Challenge 02 — Merge Sorted Lists
# Axis: CORRECTNESS (weight: 40%)

## Problem

Write a function that merges two sorted lists into one sorted list.
Do NOT use `sorted()` on the concatenated result — implement the merge step directly.

## Function signature

```python
def solution(a: list, b: list) -> list:
```

## Examples

- `solution([1, 3, 5], [2, 4, 6])` → `[1, 2, 3, 4, 5, 6]`
- `solution([], [1, 2])` → `[1, 2]`
- `solution([1], [])` → `[1]`
- `solution([], [])` → `[]`
- `solution([1, 1, 2], [1, 3])` → `[1, 1, 1, 2, 3]`
- `solution([-3, 0, 7], [-1, 4, 8])` → `[-3, -1, 0, 4, 7, 8]`

## Requirements

- Both input lists are already sorted in ascending order
- Result must be sorted in ascending order
- Handle empty inputs
- Handle duplicate values

## Output

Output ONLY the Python function in a single code block. No explanation, no tests.
