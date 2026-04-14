# Challenge 08 — LRU Cache
# Axis: CODE QUALITY (weight: 15%)

## Problem

Implement an LRU (Least Recently Used) cache class with a fixed capacity.

When the cache is full and a new item is inserted, the least recently used item
is evicted. Both get and put count as "recently used."

## Class signature

```python
class solution:
    def __init__(self, capacity: int): ...
    def get(self, key: int) -> int: ...
    def put(self, key: int, value: int) -> None: ...
```

## Examples

```
cache = solution(2)
cache.put(1, 1)     # cache: {1:1}
cache.put(2, 2)     # cache: {1:1, 2:2}
cache.get(1)        # returns 1, cache: {2:2, 1:1} (1 is now most recent)
cache.put(3, 3)     # evicts 2, cache: {1:1, 3:3}
cache.get(2)        # returns -1 (not found)
cache.put(4, 4)     # evicts 1, cache: {3:3, 4:4}
cache.get(1)        # returns -1
cache.get(3)        # returns 3
cache.get(4)        # returns 4
```

## Requirements

- O(1) time for both get and put
- get returns -1 if key not in cache
- put with existing key updates the value and marks it as recently used
- Capacity >= 1

## Quality criteria scored on

- Type annotations on all methods
- Docstring explaining the class purpose
- Clear helper method if using doubly-linked list
- No magic numbers — use named constants or comments

## Output

Output ONLY the class code in a single code block. No explanation, no tests.
