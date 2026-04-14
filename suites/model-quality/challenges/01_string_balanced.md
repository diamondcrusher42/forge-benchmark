# Challenge 01 — Balanced Brackets
# Axis: CORRECTNESS (weight: 40%)

## Problem

Write a function that determines whether a string of brackets is balanced.
A string is balanced if every opening bracket has a matching closing bracket
in the correct order.

Valid brackets: `()`, `[]`, `{}`

## Function signature

```python
def solution(s: str) -> bool:
```

## Examples

- `solution("()")` → `True`
- `solution("({[]})")` → `True`
- `solution("(]")` → `False`
- `solution("")` → `True`
- `solution("(((")` → `False`
- `solution("{[]}")` → `True`
- `solution("([)]")` → `False`

## Requirements

- Handle empty string (return True)
- Handle all three bracket types
- Order matters: `([)]` is NOT balanced

## Output

Output ONLY the Python function in a single code block. No explanation, no tests, no imports beyond what the function needs.
