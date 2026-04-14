# Challenge 03 — Flatten Nested Dict
# Axis: CORRECTNESS (weight: 40%)

## Problem

Write a function that flattens a nested dictionary using dot notation for keys.
Values that are not dicts are kept as-is.

## Function signature

```python
def solution(d: dict, prefix: str = "") -> dict:
```

## Examples

- `solution({"a": 1})` → `{"a": 1}`
- `solution({"a": {"b": 2}})` → `{"a.b": 2}`
- `solution({"a": {"b": {"c": 3}}})` → `{"a.b.c": 3}`
- `solution({"x": 1, "y": {"z": 2, "w": 3}})` → `{"x": 1, "y.z": 2, "y.w": 3}`
- `solution({})` → `{}`
- `solution({"a": {"b": 1}, "c": 2})` → `{"a.b": 1, "c": 2}`

## Requirements

- Arbitrarily deep nesting
- Handle empty dicts
- Non-dict values (int, str, list, None) are leaf values — do not recurse into them

## Output

Output ONLY the Python function in a single code block. No explanation, no tests.
