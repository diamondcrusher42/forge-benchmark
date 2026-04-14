# Challenge 05 — Coin Change (Minimum Coins)
# Axis: COMPLEXITY (weight: 20%)

## Problem

Given a list of coin denominations and a target amount, return the minimum number
of coins needed to make the amount. If the amount cannot be made, return -1.

This requires dynamic programming — a greedy approach will fail on some inputs.

## Function signature

```python
def solution(coins: list, amount: int) -> int:
```

## Examples

- `solution([1, 5, 11], 15)` → `3` (5+5+5, NOT 11+1+1+1+1 which greedy picks)
- `solution([1, 2, 5], 11)` → `3` (5+5+1)
- `solution([2], 3)` → `-1` (impossible)
- `solution([1], 0)` → `0` (zero coins for zero amount)
- `solution([186, 419, 83, 408], 6249)` → `20`
- `solution([1, 2, 5], 0)` → `0`

## Requirements

- Use dynamic programming (O(amount × len(coins)) time)
- Return -1 if impossible
- Amount 0 always requires 0 coins

## Output

Output ONLY the Python function in a single code block. No explanation, no tests.
