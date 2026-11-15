"""Aggregate stats over the tool-split file + SWE-smith tasks. Usage: python -I inspect_stats.py <rawdir>"""
import sys, json, glob, re, collections as C, pandas as pd
raw = sys.argv[1]
t = pd.read_parquet(f"{raw}/data/tool-00000-of-00008.parquet")
s = pd.concat([pd.read_parquet(f) for f in sorted(glob.glob(f"{raw}/data/train-*.parquet"))]).set_index("instance_id")
P = lambda *a: print(*a)

P("resolved:", t.resolved.value_counts().to_dict())
P("models:", t.model.value_counts().to_dict())
P("traj_id unique:", t.traj_id.nunique(), "/", len(t))
dup = t.instance_id.value_counts(); P("runs per instance:", dup.value_counts().sort_index().to_dict(), "max eg", dup.index[0], dup.iloc[0])
both = t.groupby("instance_id").resolved.agg(["min", "max"]); P("instances with both pass+fail runs:", ((both["min"] != both["max"])).sum(), both[both["min"] != both["max"]].index[:2].tolist())
P("traj patch empty:", (t.patch.str.strip() == "").sum(), "eg", t[t.patch.str.strip() == ""].instance_id.head(2).tolist())
P("traj patch empty by resolved:", t.assign(e=t.patch.str.strip() == "").groupby("resolved").e.sum().to_dict())
m = t.instance_id.isin(s.index)
P("traj patch == task patch (bug):", sum(t.patch[i] == s.patch.get(t.instance_id[i]) for i in t.index[m]))
P("task problem_statement empty:", (s.problem_statement.fillna("").str.strip() == "").sum(), "/", len(s))
ps_joined = s.problem_statement.reindex(t.instance_id[m]).fillna("")
P("  of joined traj rows, empty PS:", (ps_joined.str.strip() == "").sum())

stats = C.Counter(); nmsgs = []; nsubmit = C.Counter(); tools = C.Counter(); last_role = C.Counter(); roles = C.Counter()
ps_in_user = 0; ps_checked = 0; trunc = C.Counter(); test_runs = 0; ex = {}
end_kinds = C.Counter(); content_types = C.Counter(); lens = []
for i, r in t.iterrows():
    msgs = json.loads(r.messages); nmsgs.append(len(msgs)); lens.append(len(r.messages))
    k = 0
    for mm in msgs:
        roles[mm["role"]] += 1; content_types[type(mm.get("content")).__name__] += 1
        for tc in mm.get("tool_calls") or []:
            n = tc["function"]["name"]; tools[n] += 1
            if n == "submit": k += 1
            if n == "bash":
                cmd = json.loads(tc["function"]["arguments"]).get("command", "")
                if re.search(r"pytest|unittest|tox|nosetests|runtests", cmd): test_runs += 1; ex.setdefault("test", r.instance_id)
        c = mm.get("content"); c = c if isinstance(c, str) else json.dumps(c)
        if mm["role"] == "tool":
            for pat in ["Observations should not exceed", "truncated", "<response clipped>", "too long"]:
                if pat in c: trunc[pat] += 1; ex.setdefault(pat, r.instance_id)
    nsubmit[k] += 1; ex.setdefault(f"submit{k}", r.instance_id)
    last = msgs[-1]; last_role[last["role"]] += 1
    lc = [tc["function"]["name"] for tc in last.get("tool_calls") or []]
    end_kinds[("last_tool=" + ",".join(lc)) if lc else "last=" + last["role"] + ":" + str(last.get("content"))[:60]] += 1
    first_user = next(mm for mm in msgs if mm["role"] == "user"); fu = first_user["content"] if isinstance(first_user["content"], str) else json.dumps(first_user["content"])
    if r.instance_id in s.index:
        ps = s.problem_statement[r.instance_id].strip()
        if ps: ps_checked += 1; ps_in_user += ps[:200] in fu
P("message counts: min/median/max", min(nmsgs), sorted(nmsgs)[len(nmsgs)//2], max(nmsgs), "longest eg", t.instance_id[nmsgs.index(max(nmsgs))])
P("json chars: median/max", sorted(lens)[len(lens)//2], max(lens))
P("roles:", dict(roles)); P("content types:", dict(content_types))
P("tool names:", tools.most_common())
P("submit calls per run:", dict(sorted(nsubmit.items())))
P("last message role:", dict(last_role)); P("end kinds:", end_kinds.most_common(8))
P(f"problem_statement (first 200 chars) found in first user msg: {ps_in_user}/{ps_checked}")
P("bash test runs:", test_runs); P("truncation markers in tool outputs:", dict(trunc))
P("examples:", ex)
