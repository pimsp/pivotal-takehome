"""Does the trajectory patch belong to the run? And the inline tool-call format. Usage: python -I inspect_patch.py <rawdir>"""
import sys, json, glob, re, collections as C, pandas as pd
raw = sys.argv[1]
t = pd.read_parquet(f"{raw}/data/tool-00000-of-00008.parquet")
s = pd.concat([pd.read_parquet(f) for f in sorted(glob.glob(f"{raw}/data/train-*.parquet"))])
bug_by_patch = dict(zip(s.patch, s.instance_id))
txt = lambda c: c if isinstance(c, str) else " ".join(x.get("text", "") for x in c)
res = C.Counter(); ex = {}
for i, r in t[t.patch.str.strip() != ""].iterrows():
    files = set(re.findall(r"^diff --git a/(\S+)", r.patch, re.M))
    msgs = json.loads(r.messages); blob = r.messages
    touched = all(f in blob for f in files)
    k = ("files_mentioned_in_run" if touched else "files_NOT_in_run") + ("|equals_some_bug_patch:" + ("own" if bug_by_patch[r.patch] == r.instance_id else "other") if r.patch in bug_by_patch else "")
    res[(k, r.resolved)] += 1; ex.setdefault(k, (r.instance_id, sorted(files)[:3]))
print(dict(res)); print(ex)
# duplicate patch values across rows
vc = t.patch[t.patch.str.strip() != ""].value_counts(); print("distinct nonempty patches", len(vc), "max repeat", vc.iloc[0])
# inline run
r = t[t.instance_id == "django__channels.a144b4b8.lm_rewrite__9vzepjtr"].iloc[0]; msgs = json.loads(r.messages)
for m in msgs[1:5] + msgs[-3:]:
    print("--", m["role"], "action=", repr(m.get("action"))[:150], "tool_calls=", m.get("tool_calls"))
    print("   ", txt(m.get("content") or "")[-300:].replace("\n", " | "))
print("system prompt (inline run):", txt(msgs[0]["content"])[:400].replace("\n", " | "))
