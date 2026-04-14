# Challenge 13 — Two Sum (Hash Map)
# Axis: EFFICIENCY (weight: 5%)

## Problem

Given a list of integers and a target sum, return the indices of the two numbers
that add up to the target. Each input has exactly one solution.

## Function signature

```python
def solution(nums: list, target: int) -> list:
```

## Examples

- `solution([2, 7, 11, 15], 9)` → `[0, 1]`  (2+7=9)
- `solution([3, 2, 4], 6)` → `[1, 2]`       (2+4=6)
- `solution([3, 3], 6)` → `[0, 1]`
- `solution([-1, -2, -3, -4, -5], -8)` → `[2, 4]` (-3+-5=-8)
- `solution([0, 4, 3, 0], 0)` → `[0, 3]`

## Requirements

- O(n) time — use a hash map, do NOT use nested loops (O(n²))
- Return indices as a list [i, j] where i < j
- Guaranteed exactly one solution exists
- Do not use the same element twice

## Output

Output ONLY the Python function in a single code block. No explanation, no tests.
