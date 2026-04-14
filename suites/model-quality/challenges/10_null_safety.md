# Challenge 10 — Robust Average Calculator
# Axis: STABILITY (weight: 10%)

## Problem

Write a function that calculates the average of a list of numbers.
It must handle all edge cases without raising exceptions.

## Function signature

```python
def solution(values) -> float:
```

## Behaviour spec

- Normal list of numbers → return average as float
- Empty list → return 0.0
- None input → return 0.0
- List containing None values → skip None values, average the rest
- List of all None values → return 0.0
- Single-element list → return that element as float
- List with mix of int and float → handle both

## Examples

- `solution([1, 2, 3])` → `2.0`
- `solution([])` → `0.0`
- `solution(None)` → `0.0`
- `solution([None, 2, None, 4])` → `3.0`
- `solution([None, None])` → `0.0`
- `solution([7])` → `7.0`
- `solution([1.5, 2.5])` → `2.0`

## Requirements

- Never raise an exception for any of the above inputs
- Return type is always float

## Output

Output ONLY the Python function in a single code block. No explanation, no tests.
