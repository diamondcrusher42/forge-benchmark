#!/usr/bin/env python3
"""
Model Quality Grader — 5-axis weighted scoring system.

Axes and weights (mirrors aistupidlevel.info methodology):
  Correctness  40% — does output pass test cases?
  Complexity   20% — handles non-trivial inputs and correct algorithm?
  Quality      15% — clean, typed, documented code?
  Stability    10% — handles edge cases without exceptions?
  Efficiency    5% — avoids obvious O(n²) patterns where O(n) required?
"""
import re
import ast
import subprocess
import sys
import textwrap
import json


# ── Axis weights ──────────────────────────────────────────────────────────────
WEIGHTS = {
    "correctness": 0.40,
    "complexity":  0.20,
    "quality":     0.15,
    "stability":   0.10,
    "efficiency":  0.05,
}


def extract_code_block(text: str) -> str:
    """Pull first ```python ... ``` block from model output."""
    pattern = r"```(?:python)?\n(.*?)```"
    m = re.search(pattern, text, re.DOTALL)
    if m:
        return m.group(1).strip()
    # Fallback: try to find def or class at top level
    lines = text.split("\n")
    code_lines = []
    in_code = False
    for line in lines:
        if line.startswith("def ") or line.startswith("class "):
            in_code = True
        if in_code:
            code_lines.append(line)
    return "\n".join(code_lines).strip()


def run_tests(code: str, test_cases: list[dict]) -> tuple[int, int]:
    """
    Execute code + test cases in a subprocess.
    Returns (passed, total).
    test_cases: list of {"call": "solution(...)", "expected": value}
    """
    passed = 0
    total = len(test_cases)

    for tc in test_cases:
        call = tc["call"]
        expected = tc["expected"]
        test_script = textwrap.dedent(f"""
import sys
{code}

try:
    result = {call}
    expected = {repr(expected)}
    if result == expected:
        print("PASS")
    else:
        print(f"FAIL: got {{repr(result)}}, expected {{repr(expected)}}")
except Exception as e:
    print(f"ERROR: {{e}}")
""").strip()

        try:
            out = subprocess.run(
                [sys.executable, "-c", test_script],
                capture_output=True, text=True, timeout=5
            )
            if out.stdout.strip().startswith("PASS"):
                passed += 1
        except subprocess.TimeoutExpired:
            pass  # timeout = fail

    return passed, total


def score_quality(code: str) -> float:
    """
    Static analysis for code quality.
    Returns 0.0 – 1.0.
    """
    score = 0.0
    checks = 0.0

    # Has docstring
    checks += 1
    if '"""' in code or "'''" in code:
        score += 1

    # Has type annotations (-> or : type)
    checks += 1
    if "->" in code or (": int" in code or ": str" in code or ": list" in code
                         or ": dict" in code or ": bool" in code or ": float" in code):
        score += 1

    # Descriptive names (no single-char vars except loop iterators i/j/k)
    checks += 1
    try:
        tree = ast.parse(code)
        names = [
            node.id for node in ast.walk(tree)
            if isinstance(node, ast.Name) and len(node.id) == 1
               and node.id not in ("i", "j", "k", "n", "v", "s", "p", "q", "x", "y", "_")
        ]
        if len(names) == 0:
            score += 1
    except SyntaxError:
        pass

    # No magic numbers (beyond 0, 1, -1, 2)
    checks += 1
    try:
        tree = ast.parse(code)
        magic = [
            node.n for node in ast.walk(tree)
            if isinstance(node, ast.Constant)
               and isinstance(node.n, (int, float))
               and node.n not in (0, 1, -1, 2, 0.0, 1.0, -1.0)
        ]
        if len(magic) <= 2:
            score += 1
    except (SyntaxError, AttributeError):
        pass

    return score / checks if checks > 0 else 0.0


def score_efficiency(code: str, forbidden_patterns: list[str]) -> float:
    """
    Check for O(n²) anti-patterns where O(n) is required.
    forbidden_patterns: regex strings for bad patterns
    Returns 1.0 if clean, 0.0 if pattern found.
    """
    for pat in forbidden_patterns:
        if re.search(pat, code):
            return 0.0
    return 1.0


# ── Per-challenge test definitions ────────────────────────────────────────────

CHALLENGES = {
    "01_string_balanced": {
        "axis": "correctness",
        "correctness_tests": [
            {"call": 'solution("()")', "expected": True},
            {"call": 'solution("({[]})")', "expected": True},
            {"call": 'solution("(]")', "expected": False},
            {"call": 'solution("")', "expected": True},
            {"call": 'solution("(((")', "expected": False},
            {"call": 'solution("{[]}")', "expected": True},
            {"call": 'solution("([)]")', "expected": False},
        ],
        "stability_tests": [
            {"call": 'solution("   ")', "expected": True},  # spaces only
        ],
        "efficiency_forbidden": [],
    },
    "02_list_merge": {
        "axis": "correctness",
        "correctness_tests": [
            {"call": "solution([1,3,5],[2,4,6])", "expected": [1,2,3,4,5,6]},
            {"call": "solution([],[1,2])", "expected": [1,2]},
            {"call": "solution([1],[])", "expected": [1]},
            {"call": "solution([],[])", "expected": []},
            {"call": "solution([1,1,2],[1,3])", "expected": [1,1,1,2,3]},
            {"call": "solution([-3,0,7],[-1,4,8])", "expected": [-3,-1,0,4,7,8]},
        ],
        "stability_tests": [],
        "efficiency_forbidden": [r"sorted\("],  # must not use sorted()
    },
    "03_dict_flatten": {
        "axis": "correctness",
        "correctness_tests": [
            {"call": 'solution({"a":1})', "expected": {"a":1}},
            {"call": 'solution({"a":{"b":2}})', "expected": {"a.b":2}},
            {"call": 'solution({"a":{"b":{"c":3}}})', "expected": {"a.b.c":3}},
            {"call": 'solution({"x":1,"y":{"z":2,"w":3}})', "expected": {"x":1,"y.z":2,"y.w":3}},
            {"call": 'solution({})', "expected": {}},
            {"call": 'solution({"a":{"b":1},"c":2})', "expected": {"a.b":1,"c":2}},
        ],
        "stability_tests": [
            {"call": 'solution({"a":None})', "expected": {"a":None}},
        ],
        "efficiency_forbidden": [],
    },
    "04_word_frequency": {
        "axis": "correctness",
        "correctness_tests": [
            {"call": 'solution("the cat sat on the mat the cat",2)', "expected": [("the",3),("cat",2)]},
            {"call": 'solution("a b a b c",3)', "expected": [("a",2),("b",2),("c",1)]},
            {"call": 'solution("",5)', "expected": []},
            {"call": 'solution("hello",1)', "expected": [("hello",1)]},
            {"call": 'solution("x y z",2)', "expected": [("x",1),("y",1)]},
        ],
        "stability_tests": [
            {"call": 'solution("The the THE",1)', "expected": [("the",3)]},
        ],
        "efficiency_forbidden": [],
    },
    "05_dp_coins": {
        "axis": "complexity",
        "correctness_tests": [
            {"call": "solution([1,5,11],15)", "expected": 3},
            {"call": "solution([1,2,5],11)", "expected": 3},
            {"call": "solution([2],3)", "expected": -1},
            {"call": "solution([1],0)", "expected": 0},
            {"call": "solution([1,2,5],0)", "expected": 0},
        ],
        "stability_tests": [
            {"call": "solution([186,419,83,408],6249)", "expected": 20},
        ],
        "efficiency_forbidden": [],
    },
    "06_graph_bfs": {
        "axis": "complexity",
        "correctness_tests": [
            {"call": 'solution({"A":["B","C"],"B":["A","D"],"C":["A"],"D":["B"]},"A","D")', "expected": ["A","B","D"]},
            {"call": 'solution({"A":["B"],"B":["A"],"C":[]},"A","C")', "expected": []},
            {"call": 'solution({"A":["B"]},"A","A")', "expected": ["A"]},
        ],
        "stability_tests": [
            {"call": 'solution({},"A","A")', "expected": []},
        ],
        "efficiency_forbidden": [],
    },
    "07_sliding_window": {
        "axis": "complexity",
        "correctness_tests": [
            {"call": "solution([2,1,5,1,3,2],3)", "expected": 9},
            {"call": "solution([2,3,4,1,5],2)", "expected": 7},
            {"call": "solution([1,4,2,10,2,3,1,0,20],4)", "expected": 24},
            {"call": "solution([5],1)", "expected": 5},
            {"call": "solution([-1,-2,-3,-4],2)", "expected": -3},
        ],
        "stability_tests": [],
        "efficiency_forbidden": [
            r"for .+ in .+:\s*\n\s+for .+ in",  # nested loop anti-pattern
        ],
    },
    "08_lru_cache": {
        "axis": "quality",
        "correctness_tests": [
            {"call": textwrap.dedent("""
(lambda c: [
    c.put(1,1), c.put(2,2),
    c.get(1),   # 1
    c.put(3,3),
    c.get(2),   # -1
    c.put(4,4),
    c.get(1),   # -1
    c.get(3),   # 3
    c.get(4),   # 4
])(solution(2))[-4:]
""").strip(), "expected": [-1, -1, 3, 4]},
        ],
        "stability_tests": [
            {"call": "(lambda c: c.get(99))(solution(1))", "expected": -1},
        ],
        "efficiency_forbidden": [],
    },
    "09_refactor": {
        "axis": "quality",
        # Test that the refactored function still behaves correctly
        "correctness_tests": [
            {"call": "solution([1,3,5,7,9],5)", "expected": 2},
            {"call": "solution([1,3,5,7,9],1)", "expected": 0},
            {"call": "solution([1,3,5,7,9],9)", "expected": 4},
            {"call": "solution([1,3,5,7,9],4)", "expected": -1},
            {"call": "solution([],1)", "expected": -1},
        ],
        "stability_tests": [],
        "efficiency_forbidden": [],
    },
    "10_null_safety": {
        "axis": "stability",
        "correctness_tests": [
            {"call": "solution([1,2,3])", "expected": 2.0},
            {"call": "solution([])", "expected": 0.0},
            {"call": "solution(None)", "expected": 0.0},
            {"call": "solution([7])", "expected": 7.0},
            {"call": "solution([1.5,2.5])", "expected": 2.0},
        ],
        "stability_tests": [
            {"call": "solution([None,2,None,4])", "expected": 3.0},
            {"call": "solution([None,None])", "expected": 0.0},
        ],
        "efficiency_forbidden": [],
    },
    "11_binary_search": {
        "axis": "stability",
        "correctness_tests": [
            {"call": "solution([1,3,5,7,9],5)", "expected": 2},
            {"call": "solution([1,3,5,7,9],4)", "expected": -1},
            {"call": "solution([],1)", "expected": -1},
            {"call": "solution([5],5)", "expected": 0},
            {"call": "solution([5],3)", "expected": -1},
        ],
        "stability_tests": [
            {"call": "solution([1,3,5,7,9],1)", "expected": 0},   # first
            {"call": "solution([1,3,5,7,9],9)", "expected": 4},   # last
            {"call": "solution([1,2],2)", "expected": 1},         # two elements
        ],
        "efficiency_forbidden": [],
    },
    "12_dedup_order": {
        "axis": "efficiency",
        "correctness_tests": [
            {"call": "solution([1,2,1,3,2])", "expected": [1,2,3]},
            {"call": "solution([])", "expected": []},
            {"call": "solution([1])", "expected": [1]},
            {"call": "solution([1,1,1])", "expected": [1]},
            {"call": 'solution(["a","b","a","c"])', "expected": ["a","b","c"]},
            {"call": "solution([3,1,4,1,5,9,2,6,5])", "expected": [3,1,4,5,9,2,6]},
        ],
        "stability_tests": [],
        "efficiency_forbidden": [
            r"\.index\(",          # list.index() = O(n) inside loop = O(n²)
            r"not in \[",          # membership test on list = O(n) inside loop
        ],
    },
    "13_two_sum": {
        "axis": "efficiency",
        "correctness_tests": [
            {"call": "solution([2,7,11,15],9)", "expected": [0,1]},
            {"call": "solution([3,2,4],6)", "expected": [1,2]},
            {"call": "solution([3,3],6)", "expected": [0,1]},
            {"call": "solution([-1,-2,-3,-4,-5],-8)", "expected": [2,4]},
            {"call": "solution([0,4,3,0],0)", "expected": [0,3]},
        ],
        "stability_tests": [],
        "efficiency_forbidden": [
            r"for .+ in range.*:\s*\n\s+for .+ in range",  # nested loop O(n²)
        ],
    },
}


def grade_challenge(challenge_id: str, model_output: str) -> dict:
    """
    Grade a model's response to one challenge.
    Returns dict with axis scores and weighted total.
    """
    cfg = CHALLENGES.get(challenge_id)
    if not cfg:
        return {"error": f"unknown challenge: {challenge_id}"}

    code = extract_code_block(model_output)
    if not code:
        return {
            "challenge": challenge_id,
            "code_extracted": False,
            "correctness": 0.0,
            "complexity": 0.0,
            "quality": 0.0,
            "stability": 0.0,
            "efficiency": 0.0,
            "weighted_total": 0.0,
        }

    # For challenge 08 (LRU cache), rename class to 'solution' for test harness
    if challenge_id == "08_lru_cache" and "class " in code and "class solution" not in code:
        code = re.sub(r"class \w+", "class solution", code, count=1)

    # Correctness
    c_pass, c_total = run_tests(code, cfg.get("correctness_tests", []))
    correctness = c_pass / c_total if c_total > 0 else 0.0

    # Stability (edge cases — separate from correctness)
    s_pass, s_total = run_tests(code, cfg.get("stability_tests", []))
    stability = s_pass / s_total if s_total > 0 else 1.0  # no stability tests = full score

    # Complexity: if axis is "complexity", correctness includes hard cases; give complexity bonus
    axis = cfg.get("axis", "correctness")
    if axis == "complexity":
        complexity = correctness  # hard test cases already embedded
        correctness = min(correctness + 0.2, 1.0)  # slight correctness credit
    else:
        complexity = 1.0 if correctness > 0.5 else 0.0  # partial credit

    # Code quality
    quality = score_quality(code)

    # Efficiency
    forbidden = cfg.get("efficiency_forbidden", [])
    efficiency = score_efficiency(code, forbidden)

    # Weighted total
    total = (
        correctness * WEIGHTS["correctness"] +
        complexity  * WEIGHTS["complexity"] +
        quality     * WEIGHTS["quality"] +
        stability   * WEIGHTS["stability"] +
        efficiency  * WEIGHTS["efficiency"]
    )

    return {
        "challenge": challenge_id,
        "axis": axis,
        "code_extracted": True,
        "code_length": len(code.splitlines()),
        "correctness": round(correctness, 3),
        "complexity":  round(complexity, 3),
        "quality":     round(quality, 3),
        "stability":   round(stability, 3),
        "efficiency":  round(efficiency, 3),
        "weighted_total": round(total, 3),
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Grade a model output file")
    parser.add_argument("--output", required=True, help="Path to model output text file")
    parser.add_argument("--challenge", required=True, help="Challenge ID (e.g. 01_string_balanced)")
    args = parser.parse_args()

    with open(args.output) as f:
        model_output = f.read()

    result = grade_challenge(args.challenge, model_output)
    print(json.dumps(result, indent=2))
