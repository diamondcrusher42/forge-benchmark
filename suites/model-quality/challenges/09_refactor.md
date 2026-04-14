# Challenge 09 — Refactor Messy Code
# Axis: CODE QUALITY (weight: 15%)

## Problem

The following function works correctly but is poorly written.
Refactor it to be clean, readable, and maintainable — without changing its behaviour.

## Original code (DO NOT change the logic, only the style/structure)

```python
def f(l, x):
    a = 0
    b = len(l) - 1
    while a <= b:
        m = (a+b)//2
        if l[m]==x:
            return m
        elif l[m]<x:
            a=m+1
        else:
            b=m-1
    return -1
```

## Requirements for the refactored version

- Rename `f`, `l`, `x`, `a`, `b`, `m` to descriptive names
- Add a docstring explaining what the function does, its parameters, and return value
- Add type annotations
- Preserve exact behaviour (same algorithm, same return values)
- Keep it concise — do not add logging, error handling for non-list inputs, or extra features

## What the function does

Binary search: returns the index of `x` in sorted list `l`, or -1 if not found.

## Output

Output ONLY the refactored Python function in a single code block. No explanation.
