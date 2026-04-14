# Challenge 04 — Word Frequency Counter
# Axis: CORRECTNESS (weight: 40%)

## Problem

Write a function that counts the frequency of each word in a string and returns
the top N most frequent words as a list of (word, count) tuples, sorted by
frequency descending, then alphabetically ascending for ties.

## Function signature

```python
def solution(text: str, n: int) -> list:
```

## Examples

- `solution("the cat sat on the mat the cat", 2)` → `[("the", 3), ("cat", 2)]`
- `solution("a b a b c", 3)` → `[("a", 2), ("b", 2), ("c", 1)]`  (ties: a before b alphabetically)
- `solution("", 5)` → `[]`
- `solution("hello", 1)` → `[("hello", 1)]`
- `solution("x y z", 2)` → `[("x", 1), ("y", 1)]`  (top 2 of 3 tied: alphabetical)

## Requirements

- Case-insensitive: "The" and "the" are the same word
- Punctuation: strip leading/trailing punctuation from each word
- If fewer than N unique words exist, return all of them
- Ties broken alphabetically ascending

## Output

Output ONLY the Python function in a single code block. No explanation, no tests.
