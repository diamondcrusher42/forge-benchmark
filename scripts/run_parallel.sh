#!/bin/bash
# Run all model × effort combinations in parallel git worktrees.
# Each clone gets its own isolated worktree, runs claude -p, scores automatically.
#
# Usage: bash run_parallel.sh <suite-dir> [--matrix "haiku:medium,sonnet:max"]
#
# Suite dir must contain:
#   prompts/task-*.md  (concatenated into one prompt, alphabetical order)
#   setup.sh           (idempotent worktree prep, receives WORKTREE env var)
#   score.py           (called per task after run; --session <jsonl> --task <id>)
#   teardown.sh        (optional cleanup)

set -euo pipefail

SUITE_DIR="${1:?Usage: run_parallel.sh <suite-dir> [--matrix 'model:effort,...']}"
SHIFT_COUNT=1

# Matrix: model-short:effort pairs
DEFAULT_MATRIX="haiku:medium haiku:max sonnet:medium sonnet:max opus:medium opus:max"
MATRIX="$DEFAULT_MATRIX"

for arg in "$@"; do
    if [[ "$arg" == "--matrix" ]]; then
        SHIFT_COUNT=$((SHIFT_COUNT + 1))
    elif [[ "$SHIFT_COUNT" -gt 1 ]]; then
        MATRIX="${arg//,/ }"
        SHIFT_COUNT=0
    fi
done

# Model ID map
model_id() {
    case "$1" in
        haiku)  echo "claude-haiku-4-5-20251001" ;;
        sonnet) echo "claude-sonnet-4-6" ;;
        opus)   echo "claude-opus-4-6" ;;
        *)      echo "$1" ;;  # pass-through for full model IDs
    esac
}

# Paths
SUITE_NAME=$(basename "$SUITE_DIR")
RESULTS_DIR="$HOME/.claude/benchmark/$SUITE_NAME"
RUN_DATE=$(date +%Y%m%d-%H%M)
BENCH_WORKDIR="/tmp/bench-$SUITE_NAME-$RUN_DATE"
BASE_REPO="${BENCHMARK_BASE_REPO:-}"  # must be set in suite or env
BRANCH="${BENCHMARK_BRANCH:-}"

mkdir -p "$RESULTS_DIR" "$BENCH_WORKDIR"

# Build combined prompt from prompts/*.md and *.txt (alphabetical)
PROMPT_FILES=$(ls -1 "$SUITE_DIR/prompts/"*.md "$SUITE_DIR/prompts/"*.txt 2>/dev/null | sort || true)
if [[ -z "$PROMPT_FILES" ]]; then
    echo "ERROR: No prompt files found in $SUITE_DIR/prompts/" >&2
    exit 1
fi

TASK_IDS=()
PROMPT=""
for f in $PROMPT_FILES; do
    name=$(basename "$f")
    task_id="${name%%.*}"  # task-A.md → task-A, then extract last char
    task_id="${task_id##*-}"  # task-A → A
    TASK_IDS+=("$task_id")
    PROMPT+="## Task ${task_id}

$(cat "$f")

"
done

echo "Tasks: ${TASK_IDS[*]}"
echo "Matrix: $MATRIX"
echo "Results: $RESULTS_DIR"
echo ""

# ── Spawn all runs in parallel ─────────────────────────────────────────────────
declare -A WORKTREES PIDS

for combo in $MATRIX; do
    model_short="${combo%%:*}"
    effort="${combo##*:}"
    model=$(model_id "$model_short")
    run_id="${SUITE_NAME}-${model_short}-${effort}-${RUN_DATE}"
    worktree="$BENCH_WORKDIR/$model_short-$effort"

    echo "→ Setting up worktree: $worktree"

    # Create isolated worktree
    if [[ -n "$BASE_REPO" ]]; then
        branch_arg=""
        [[ -n "$BRANCH" ]] && branch_arg="--branch $BRANCH"
        git -C "$BASE_REPO" worktree add "$worktree" ${branch_arg:-} 2>/dev/null || \
        git -C "$BASE_REPO" worktree add --detach "$worktree" 2>/dev/null || \
        cp -r "$BASE_REPO" "$worktree"
    else
        mkdir -p "$worktree"
    fi

    # Run suite setup.sh inside the worktree
    WORKTREE="$worktree" BENCHMARK_WORKTREE="$worktree" bash "$SUITE_DIR/setup.sh" 2>&1 | \
        sed "s/^/[$model_short:$effort] /"

    # Launch claude -p in background
    (
        cd "$worktree"
        echo "[$model_short:$effort] Starting..."
        claude -p "$PROMPT" \
            --model "$model" \
            --effort "$effort" \
            --permission-mode bypassPermissions \
            2>&1 | tail -5
        echo "[$model_short:$effort] Session complete."
    ) &

    WORKTREES["$combo"]="$worktree"
    PIDS["$combo"]=$!
done

echo ""
echo "All $( echo $MATRIX | wc -w ) runs launched. Waiting for completion..."
echo "(This may take several minutes — models are working in parallel)"
echo ""

# ── Wait and collect results ───────────────────────────────────────────────────
for combo in $MATRIX; do
    model_short="${combo%%:*}"
    effort="${combo##*:}"
    model=$(model_id "$model_short")
    run_id="${SUITE_NAME}-${model_short}-${effort}-${RUN_DATE}"
    worktree="${WORKTREES[$combo]}"
    pid="${PIDS[$combo]}"

    wait "$pid" 2>/dev/null || true
    echo "✓ $model_short $effort — done"

    # Find the JSONL for this worktree
    # Claude escapes paths by replacing all / with - (leading / becomes leading -)
    escaped=$(echo "$worktree" | sed 's|/|-|g')
    jsonl=$(ls -t "$HOME/.claude/projects/$escaped/"*.jsonl 2>/dev/null | head -1)

    if [[ -z "$jsonl" ]]; then
        echo "  ✗ JSONL not found for $worktree" >&2
        jsonl="NOT_FOUND"
    else
        echo "  JSONL: $jsonl"
    fi

    # Score each task
    scores="{}"
    source "$HOME/workspace/venv/bin/activate" 2>/dev/null || true
    for task_id in "${TASK_IDS[@]}"; do
        if [[ "$jsonl" != "NOT_FOUND" ]]; then
            task_score=$(WORKTREE="$worktree" python3 "$SUITE_DIR/score.py" --session "$jsonl" --task "$task_id" --worktree "$worktree" 2>/dev/null || echo '{"error":"score failed"}')
            scores=$(python3 -c "
import json, sys
s = json.loads('$scores')
t = json.loads('''$task_score''')
s['$task_id'] = t
print(json.dumps(s))
" 2>/dev/null || echo "$scores")
        fi
    done

    # Save run result
    cat > "$RESULTS_DIR/$run_id.json" << EOF
{
  "run_id": "$run_id",
  "model": "$model",
  "model_short": "$model_short",
  "effort": "$effort",
  "suite": "$SUITE_DIR",
  "worktree": "$worktree",
  "jsonl": "$jsonl",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "scores": $scores
}
EOF
    echo "  Saved: $RESULTS_DIR/$run_id.json"

    # Teardown
    [[ -f "$SUITE_DIR/teardown.sh" ]] && WORKTREE="$worktree" bash "$SUITE_DIR/teardown.sh" 2>/dev/null || true
done

echo ""
echo "All runs complete. Generating report..."
python3 "$(dirname "$0")/report.py" "$RESULTS_DIR"
