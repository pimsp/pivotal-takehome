"""Confident final claims vs resolved; and whether patch rows are misaligned. Usage: python -I inspect_confidence.py <rawdir>"""
import sys, json, re, collections as C, pandas as pd, math
raw = sys.argv[1]
t = pd.read_parquet(f"{raw}/data/tool-00000-of-00008.parquet")
txt = lambda c: c if isinstance(c, str) else " ".join(x.get("text", "") for x in c)
CONF = re.compile(r"(?i)successfully (fixed|resolved|implemented|addressed)|(fix|changes?|solution) (works|is working|resolves|addresses|correctly)|all (the )?tests (now )?pass|issue (has been|is) (fixed|resolved)|we('ve| have) (fixed|resolved)|(fixed|resolved) the issue|works (correctly|as expected)")
HEDGE = re.compile(r"(?i)\b(might|may not|unable|couldn't|could not|not sure|still fail|still failing|unclear|partially|workaround|however, )")
def final_text(msgs):
    """Last non-trivial assistant text, dropping the bare submit call."""
    for m in reversed(msgs):
        if m["role"] != "assistant": continue
        c = re.sub(r"<function=submit>\s*</function>", "", txt(m.get("content") or "")).strip()
        if len(c) > 80 and "Exit due to" not in c: return c
    return ""
rows = []
for _, r in t.iterrows():
    msgs = json.loads(r.messages)
    ft = final_text(msgs)
    # summary-ish = last ~3 assistant texts (agents often summarise one step before the submit)
    tail = " ".join(txt(m.get("content") or "") for m in [m for m in msgs if m["role"] == "assistant"][-3:])
    exited = "Exit due to" in txt(msgs[-1].get("content") or "")
    rows.append(dict(id=r.instance_id, resolved=r.resolved, conf=bool(CONF.search(tail)), hedge=bool(HEDGE.search(ft)), exited=exited))
d = pd.DataFrame(rows)
def phi(a, b):
    tab = pd.crosstab(a, b); (n00, n01), (n10, n11) = tab.values
    return (n11*n00 - n10*n01) / math.sqrt((n10+n11)*(n00+n01)*(n01+n11)*(n00+n10))
for name, sub in [("all runs", d), ("runs that ended by submit", d[~d.exited])]:
    print(f"== {name} (n={len(sub)})"); print(pd.crosstab(sub.conf, sub.resolved, margins=True))
    print("P(resolved|confident)=%.2f  P(resolved|not confident)=%.2f  phi=%.3f" % (sub[sub.conf].resolved.mean(), sub[~sub.conf].resolved.mean(), phi(sub.conf, sub.resolved)))
    print("confident & hedge-free: P(resolved)=%.2f n=%d" % (sub[sub.conf & ~sub.hedge].resolved.mean(), (sub.conf & ~sub.hedge).sum()))
print("eg confident but unresolved:", d[d.conf & ~d.resolved].id.head(3).tolist())
print("eg not confident but resolved:", d[~d.conf & d.resolved].id.head(3).tolist())
# patch alignment: does the patch's file paths appear in some OTHER row's messages?
blobs = t.messages.tolist()
hits = C.Counter()
for i, r in t[t.patch.str.strip() != ""].head(150).iterrows():
    files = re.findall(r"^diff --git a/(\S+)", r.patch, re.M)
    own = all(f in blobs[i] for f in files)
    other = [j for j in range(len(t)) if j != i and all(f in blobs[j] for f in files)]
    hits[("own" if own else "not-own", "found-in-other-row" if other else "nowhere")] += 1
print("patch files (150 sampled patches):", dict(hits))
