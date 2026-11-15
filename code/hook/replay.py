#!/usr/bin/env python3
"""Replay a recorded SWE-smith-trajectories run through the commit-first hook.

Each recorded tool call becomes a Claude Code PreToolUse event, sent to the hook
on stdin, with the transcript so far in transcript_path. Only the run's final
submit is reviewed (SWE-agent's first submit just shows the diff back to the agent).
Every submit goes to the hook; the hook reviews only the second one (the first is
SWE-agent's "review your diff and clean up" step). The test result shown is the
dataset's `resolved` column: the reviewer judges whether the patch is good, not
whether it passes. --verdicts a,d,... pre-generates the reviewer's answers for a demo.
--pretty samples only clean runs (see pretty()).

usage: python -I code/hook/replay.py TRAJ.parquet [--runs ID ...] [--n 2] [--seed 0] [--pretty] [--verdicts a,d]
"""
import argparse, ast, json, re, os, subprocess, sys, tempfile
import pandas as pd

HOOK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "commit_first.py")

def lit(v):
    """Nested fields are Python reprs inside the JSON (single quotes), not JSON."""
    if isinstance(v, str) and v[:1] in "[{":
        try: return ast.literal_eval(v)
        except (ValueError, SyntaxError): return v
    return v

def text_of(content):
    content = lit(content)
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(c.get("text", "") for c in content if isinstance(c, dict))
    return "" if content is None else str(content)

def calls_of(msg):
    out = []
    for tc in lit(msg.get("tool_calls")) or []:
        fn = tc.get("function", tc)
        args = fn.get("arguments", {})
        if isinstance(args, str):
            try: args = json.loads(args)
            except json.JSONDecodeError: args = {"raw": args}
        out.append((tc.get("id"), fn.get("name"), args))
    return out

# The patch column is misaligned with the runs in this file (1886 of 2364 non-empty patches
# touch files their own run never mentions), so the diff comes from the run itself.
def preview_diff(submit_ids, results):
    """SWE-agent's first submit echoes the diff; use the latest one before the final submit."""
    for cid in reversed(submit_ids[:-1]):
        out = results.get(cid, "")
        i = out.find("diff --git")
        if i >= 0:
            return out[i:].split("</diff>")[0].strip()
    return "(no diff recorded)"

def drop_removed(diff, msgs_text):
    """Drop file sections for scratch files the agent created and later rm'd (repro scripts)."""
    parts = re.split(r"(?=^diff --git )", diff, flags=re.M)
    keep = []
    for part in parts:
        mm = re.match(r"diff --git a/(\S+)", part)
        name = mm.group(1).split("/")[-1] if mm else None
        if name and "new file mode" in part[:300] and re.search(r"\brm\b[^\n]*" + re.escape(name), msgs_text):
            continue
        keep.append(part)
    return "".join(keep).strip() or diff

def replay(row, tmpdir):
    msgs = row["messages"]
    if isinstance(msgs, str):
        msgs = json.loads(msgs)
    msgs = list(msgs)
    run = row.get("traj_id") or row.get("instance_id")
    tpath = os.path.join(tmpdir, f"{run}.jsonl".replace("/", "_"))
    results = {}
    for m in msgs:
        if m.get("role") == "tool":
            for cid in lit(m.get("tool_call_ids")) or [m.get("tool_call_id")]:
                results[cid] = text_of(m.get("content"))
    submit_ids = [cid for m in msgs if m.get("role") == "assistant" for cid, name, _ in calls_of(m) if name == "submit"]
    last_submit = submit_ids[-1] if submit_ids else None
    transcript, n_events = [], 0
    for m in msgs:
        role = m.get("role")
        if role in ("system",):
            continue
        if role == "user":
            transcript.append({"role": "user", "text": text_of(m.get("content"))})
        elif role == "assistant":
            transcript.append({"role": "assistant", "text": text_of(m.get("content"))})
            for cid, name, args in calls_of(m):
                is_final = cid == last_submit
                with open(tpath, "w") as f:
                    f.write("\n".join(json.dumps(t) for t in transcript) + "\n")
                ev = {"session_id": run, "transcript_path": tpath, "hook_event_name": "PreToolUse",
                      "tool_name": name,
                      "tool_input": dict(args, diff=drop_removed(preview_diff(submit_ids, results), json.dumps(msgs)),
                                         test_result="PASSED" if row.get("resolved") else "FAILED")
                                    if is_final else args}
                r = subprocess.run([sys.executable, "-I", HOOK], input=json.dumps(ev), capture_output=True, text=True)
                n_events += 1
                if is_final:
                    if r.stderr: print(r.stderr)
                    print(f"[replay] {run}: {n_events} events, hook said: {r.stdout.strip() or r.stderr.strip()}")
                    return
                transcript.append({"role": "tool", "tool_name": name,
                                   "tool_input": args.get("command", args), "tool_output": results.get(cid, "")})
    print(f"[replay] {run}: no submit call found after {n_events} events (run never submitted)")

def pretty(row):
    """A clean demo run: native tool calls, two submits, a small own diff, a real closing thought.
    (Some runs call tools as text described in the system prompt; they have no tool_calls.)"""
    msgs = json.loads(row["messages"])
    subs = [cid for m in msgs if m.get("role") == "assistant" for cid, n, _ in calls_of(m) if n == "submit"]
    if len(subs) != 2:
        return False
    res = {}
    for m in msgs:
        if m.get("role") == "tool":
            for cid in lit(m.get("tool_call_ids")) or []:
                res[cid] = text_of(m.get("content"))
    d = drop_removed(preview_diff(subs, res), row["messages"])
    if not d.startswith("diff --git") or not 5 < d.count("\n") < 80:
        return False
    thoughts = [text_of(m.get("content")) for m in msgs if m.get("role") == "assistant"][-6:]
    return max((len(t) for t in thoughts), default=0) > 300

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("parquet"); ap.add_argument("--runs", nargs="*"); ap.add_argument("--n", type=int, default=2)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--pretty", action="store_true"); ap.add_argument("--verdicts")
    a = ap.parse_args()
    df = pd.read_parquet(a.parquet)
    if a.runs:
        key = "traj_id" if "traj_id" in df else "instance_id"
        df = df[df[key].isin(a.runs)]
    else:
        if a.pretty:
            df = df.sample(n=min(len(df), 300), random_state=a.seed)
            df = df[df.apply(pretty, axis=1)]
        df = df.sample(n=min(a.n, len(df)), random_state=a.seed)
    if a.verdicts:
        os.environ["COMMIT_FIRST_ANSWERS"] = a.verdicts
    os.makedirs("results", exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        for _, row in df.iterrows():
            row = row.to_dict()
            with open("results/labels.jsonl", "a") as f:
                f.write(json.dumps({"run": row.get("traj_id") or row.get("instance_id"),
                                    "resolved": bool(row.get("resolved"))}) + "\n")
            replay(row, tmp)

if __name__ == "__main__":
    main()
