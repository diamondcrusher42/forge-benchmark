#!/usr/bin/env python3
"""Timing test scorer — just measures tokens, duration, and whether output was produced."""
import argparse, json
from pathlib import Path
from datetime import datetime

def parse_events(path):
    events = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                try: events.append(json.loads(line))
                except: pass
    return events

def score(session_path, task):
    events = parse_events(session_path)
    output_tokens = sum(
        e.get("message", {}).get("usage", {}).get("output_tokens", 0)
        for e in events if e.get("type") == "assistant"
    )
    timestamps = [e.get("timestamp") for e in events if e.get("timestamp") and e.get("type") in ("user","assistant")]
    duration_min = None
    if len(timestamps) >= 2:
        try:
            t0 = datetime.fromisoformat(timestamps[0].replace("Z","+00:00"))
            t1 = datetime.fromisoformat(timestamps[-1].replace("Z","+00:00"))
            duration_min = round((t1-t0).total_seconds()/60, 2)
        except: pass
    produced_output = output_tokens > 0
    return {
        "task": task,
        "tokens_output": output_tokens,
        "duration_min": duration_min,
        "produced_output": produced_output,
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--session", required=True)
    parser.add_argument("--task", required=True)
    args = parser.parse_args()
    print(json.dumps(score(args.session, args.task), indent=2))
