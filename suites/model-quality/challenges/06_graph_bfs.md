# Challenge 06 — BFS Shortest Path
# Axis: COMPLEXITY (weight: 20%)

## Problem

Given an unweighted undirected graph (as an adjacency list) and two nodes,
return the shortest path from start to end as a list of nodes.
If no path exists, return an empty list.

## Function signature

```python
def solution(graph: dict, start: str, end: str) -> list:
```

## Examples

- `solution({"A": ["B", "C"], "B": ["A", "D"], "C": ["A"], "D": ["B"]}, "A", "D")` → `["A", "B", "D"]`
- `solution({"A": ["B"], "B": ["A"], "C": []}, "A", "C")` → `[]`
- `solution({"A": ["B"]}, "A", "A")` → `["A"]`
- `solution({"A": ["B", "C"], "B": ["A", "D", "E"], "C": ["A", "F"], "D": ["B"], "E": ["B"], "F": ["C"]}, "A", "F")` → `["A", "C", "F"]`

## Requirements

- Use BFS (guarantees shortest path in unweighted graph)
- Start == End: return [start]
- No path: return []
- Graph may have nodes not connected to anything

## Output

Output ONLY the Python function in a single code block. No explanation, no tests.
