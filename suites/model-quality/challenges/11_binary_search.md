# Challenge 11 — Binary Search with Correct Bounds
# Axis: STABILITY (weight: 10%)

## Problem

Write a binary search function that finds the index of a target in a sorted list.
Common off-by-one bugs: returning wrong index for first/last element, infinite loop
when lo and hi are adjacent.

## Function signature

```python
def solution(nums: list, target: int) -> int:
```

## Examples

- `solution([1, 3, 5, 7, 9], 5)` → `2`
- `solution([1, 3, 5, 7, 9], 1)` → `0`  (first element)
- `solution([1, 3, 5, 7, 9], 9)` → `4`  (last element)
- `solution([1, 3, 5, 7, 9], 4)` → `-1` (not found)
- `solution([], 1)` → `-1`              (empty list)
- `solution([5], 5)` → `0`              (single element, found)
- `solution([5], 3)` → `-1`             (single element, not found)
- `solution([1, 2], 2)` → `1`           (two elements, second)

## Requirements

- O(log n) — must use binary search, not linear scan
- Return -1 if not found
- No exceptions for empty list
- Handle duplicates: return any valid index if duplicates exist

## Output

Output ONLY the Python function in a single code block. No explanation, no tests.
