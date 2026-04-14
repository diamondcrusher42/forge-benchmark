# Challenge 12 — Deduplicate Preserving Order
# Axis: EFFICIENCY (weight: 5%)

## Problem

Remove duplicates from a list while preserving the original order of first occurrences.

## Function signature

```python
def solution(items: list) -> list:
```

## Examples

- `solution([1, 2, 1, 3, 2])` → `[1, 2, 3]`
- `solution([])` → `[]`
- `solution([1])` → `[1]`
- `solution([1, 1, 1])` → `[1]`
- `solution(["a", "b", "a", "c"])` → `["a", "b", "c"]`
- `solution([3, 1, 4, 1, 5, 9, 2, 6, 5])` → `[3, 1, 4, 5, 9, 2, 6]`

## Requirements

- O(n) time — use a set to track seen items, do not nest loops over the list
- Preserve order of first occurrence
- Works for list of ints or strings

## Output

Output ONLY the Python function in a single code block. No explanation, no tests.
