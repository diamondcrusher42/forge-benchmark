# Challenge 07 — Max Sum Subarray of Size K
# Axis: COMPLEXITY (weight: 20%)

## Problem

Given an array of integers and a window size k, return the maximum sum of any
contiguous subarray of exactly size k.

Use the sliding window technique — O(n), not O(n*k).

## Function signature

```python
def solution(nums: list, k: int) -> int:
```

## Examples

- `solution([2, 1, 5, 1, 3, 2], 3)` → `9` (5+1+3)
- `solution([2, 3, 4, 1, 5], 2)` → `7` (3+4)
- `solution([1, 4, 2, 10, 2, 3, 1, 0, 20], 4)` → `24` (10+2+3+1 = no, 2+10+2+3=17... 1+0+20+? actually [10,2,3,1]=16, [2,3,1,0]=6, [3,1,0,20]=24)
- `solution([5], 1)` → `5`
- `solution([-1, -2, -3, -4], 2)` → `-3` (-1 + -2)

## Requirements

- k is always valid (1 <= k <= len(nums))
- Handle negative numbers
- Implement sliding window, not brute-force O(n*k)

## Output

Output ONLY the Python function in a single code block. No explanation, no tests.
