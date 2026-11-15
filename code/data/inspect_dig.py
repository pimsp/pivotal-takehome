"""Follow-ups on the oddities. Usage: python -I inspect_dig.py <rawdir>"""
import sys, json, glob, re, collections as C, pandas as pd
raw = sys.argv[1]
t = pd.read_parquet(f"{raw}/data/tool-00000-of-00008.parquet")
s = pd.concat([pd.read_parquet(f) for f in sorted(glob.glob(f"{raw}/data/train-*.parquet"))]).set_index("instance_id")
txt = lambda c: c if isinstance(c, str) else " ".join(x.get("text", "") for x in c)
norm = lambda x: re.sub(r"\s+", " ", x).strip()
fmt = C.Counter(); ps_hit = C.Counter(); ex = {}
submit_resp = C.Counter(); thought_eq = C.Counter(); exit_by_res = C.Counter(); has_summary = 0
for i, r in t.iterrows():
    msgs = json.loads(r.messages)
    ntc = sum(len(m.get("tool_calls") or []) for m in msgs)
    ninline = sum("<function=" in txt(m.get("content") or "") for m in msgs if m["role"] == "assistant")
    k = ("structured" if ntc else "") + ("+inline" if ninline else "")
    fmt[k or "none"] += 1; ex.setdefault(k, r.instance_id)
    fu = norm(txt(next(m for m in msgs if m["role"] == "user")["content"]))
    if r.instance_id in s.index:
        ps = norm(s.problem_statement[r.instance_id])
        key = "full" if ps in fu else "first100" if ps[:100] in fu else "no"
        ps_hit[key] += 1; ex.setdefault("ps_" + key, r.instance_id)
    for j, m in enumerate(msgs):
        if m["role"] == "tool" and j > 0 and any(tc["function"]["name"] == "submit" for tc in msgs[j-1].get("tool_calls") or []):
            submit_resp[txt(m["content"])[:70]] += 1
        if m["role"] == "assistant":
            thought_eq[(m.get("thought") or "") == txt(m.get("content") or "")] += 1
    last = txt(msgs[-1].get("content") or "")
    if "Exit due to" in last: exit_by_res[(last[:40], r.resolved)] += 1
    if re.search(r"(?i)##\s*summary|in summary|to summarize", " ".join(txt(m.get("content") or "") for m in msgs[-6:] if m["role"] == "assistant")): has_summary += 1
print("tool-call format per run:", dict(fmt)); print("format examples:", ex)
print("PS vs first user msg:", dict(ps_hit))
print("tool response to submit:", submit_resp.most_common(5))
print("assistant thought == content:", dict(thought_eq))
print("exit-without-submit by resolved:", dict(exit_by_res))
print("runs with a 'summary' heading/phrase in last 6 assistant msgs:", has_summary, "/", len(t))
# empty patch but resolved
e = t[(t.patch.str.strip() == "") & t.resolved]
print("empty patch & resolved eg:", e.instance_id.head(3).tolist())
r = e.iloc[0]; msgs = json.loads(r.messages)
for m in msgs[-4:]: print("  >>", m["role"], txt(m.get("content") or "")[:600].replace("\n", " | "))
# nonempty patch: what does it look like
p = t[t.patch.str.strip() != ""].iloc[0]; print("nonempty patch eg", p.instance_id, p.patch[:300])
# messages/ agent field values, message_type
mt = C.Counter(); ag = C.Counter()
for ms in t.messages.head(300):
    for m in json.loads(ms): mt[(m["role"], m.get("message_type"))] += 1; ag[m.get("agent")] += 1
print("message_type:", dict(mt)); print("agent:", dict(ag))
