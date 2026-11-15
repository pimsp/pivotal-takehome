#!/usr/bin/env python3
"""Commit-first review: a Claude Code PreToolUse hook on the agent's submit tool.

Stage 1 shows only raw evidence (task, diff, test output) and asks approve/deny.
Stage 2 reveals the agent's own summary and asks again. Both verdicts are logged.
The decision goes back to Claude Code as permissionDecision allow/deny.

Input: the PreToolUse JSON on stdin. Evidence comes from the event itself:
tool_input.diff, and transcript_path (JSONL, one message per line:
{"role", "text", "tool_name", "tool_input", "tool_output"}), as written by replay.py.
The reviewer types on /dev/tty, because stdin carries the event.
"""
import json, os, re, sys, time

SUBMIT_TOOLS = {"submit", "mcp__swe__submit"}
LOG = os.environ.get("COMMIT_FIRST_LOG", "results/verdicts.jsonl")
TEST_RE = re.compile(r"pytest|unittest|python[3]? .*(test|repro)|tox|nose", re.I)
MAX_LINES = 60

def load_transcript(path):
    if not path or not os.path.exists(path):
        return []
    with open(path) as f:
        return [json.loads(l) for l in f if l.strip()]

def evidence(msgs):
    task = next((m["text"] for m in msgs if m["role"] == "user" and m.get("text")), "(no task text)")
    tests = [m for m in msgs if m["role"] == "tool" and TEST_RE.search(str(m.get("tool_input", "")))]
    # SWE-agent writes no formal summary; its closing thoughts right before submit are
    # often "let me clean up". Use the longest of its last 6 thoughts as the summary.
    last = [m["text"] for m in msgs if m["role"] == "assistant" and m.get("text", "").strip()][-6:]
    summary = max(last, key=len) if last else "(the agent wrote no summary)"
    return task, tests, summary

def clip(text, n=MAX_LINES):
    lines = str(text).splitlines()
    return "\n".join(lines[:n]) + (f"\n... [{len(lines) - n} more lines]" if len(lines) > n else "")

SCRIPTED = [a for a in os.environ.get("COMMIT_FIRST_ANSWERS", "").split(",") if a]  # for tests only

def ask(tty, prompt, tty_in=None):
    if SCRIPTED:
        tty.write(prompt + SCRIPTED[0] + " (scripted)\n"); return ask_map(SCRIPTED.pop(0))
    while True:
        tty.write(prompt); tty.flush()
        a = tty_in.readline().strip().lower()
        if a in ("a", "approve"): return "approve"
        if a in ("d", "deny"): return "deny"

def ask_map(a):
    return "approve" if a.startswith("a") else "deny"

def main():
    ev = json.load(sys.stdin)
    if ev.get("tool_name") not in SUBMIT_TOOLS:
        return  # not a submit: no output, Claude Code proceeds as normal
    msgs = load_transcript(ev.get("transcript_path"))
    if not any(m["role"] == "tool" and m.get("tool_name") == "submit" for m in msgs):
        # First submit: let it through; the submit tool itself answers with the diff and
        # asks the agent to rerun its repro, delete scratch files and submit again.
        return
    task, tests, summary = evidence(msgs)
    diff = ev.get("tool_input", {}).get("diff", "(no diff)")
    # /dev/tty can't be opened "r+" in text mode (not seekable): one handle each way.
    tty = sys.stderr if SCRIPTED else open("/dev/tty", "w")
    tty_in = None if SCRIPTED else open("/dev/tty")
    bar = "=" * 78
    tty.write(f"\n{bar}\nCOMMIT-FIRST REVIEW  run {ev.get('session_id')}\n{bar}\n")
    tty.write(f"\n--- TASK ---\n{clip(task, 40)}\n")
    tty.write(f"\n--- CODE CHANGE ---\n{clip(diff.replace(chr(13), ""), 80)}\n")
    result = ev.get("tool_input", {}).get("test_result")
    if result:
        tty.write(f"\n--- TEST SUITE (FAIL_TO_PASS + PASS_TO_PASS) ---\n{result}\n")
    tty.write(f"\n--- AGENT'S OWN TEST RUNS ({len(tests)}; last 1 shown) ---\n")
    for t in tests[-1:]:
        tty.write(f"$ {clip(t.get('tool_input'), 3)}\n{clip(t.get('tool_output'), 30)}\n\n")
    if not tests:
        tty.write("(the agent ran no tests)\n")
    t0 = time.time()
    v1 = ask(tty, "\nVerdict on the evidence alone [a]pprove / [d]eny: ", tty_in)
    t1 = time.time()
    tty.write(f"\n--- AGENT'S SUMMARY (hidden until now) ---\n{clip(summary, 30)}\n")
    v2 = ask(tty, f"\nYou said {v1}. Final verdict [a]pprove / [d]eny: ", tty_in)
    t2 = time.time()
    os.makedirs(os.path.dirname(LOG) or ".", exist_ok=True)
    with open(LOG, "a") as f:
        f.write(json.dumps({"run": ev.get("session_id"), "verdict_evidence": v1, "verdict_final": v2,
                            "changed": v1 != v2, "secs_evidence": round(t1 - t0, 1),
                            "secs_summary": round(t2 - t1, 1), "n_test_runs": len(tests), "test_result": result,
                            "ts": time.strftime("%Y-%m-%dT%H:%M:%S")}) + "\n")
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "allow" if v2 == "approve" else "deny",
        "permissionDecisionReason": f"Human review: evidence-only {v1}, after summary {v2}."}}))

if __name__ == "__main__":
    main()
