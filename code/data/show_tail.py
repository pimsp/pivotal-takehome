"""Print the last assistant texts of one run. Usage: python -I show_tail.py <rawdir> <instance_id>"""
import sys, json, pandas as pd
t = pd.read_parquet(f"{sys.argv[1]}/data/tool-00000-of-00008.parquet")
txt = lambda c: c if isinstance(c, str) else " ".join(x.get("text", "") for x in c)
r = t[t.instance_id == sys.argv[2]].iloc[0]; print("resolved", r.resolved)
for m in [m for m in json.loads(r.messages) if m["role"] == "assistant"][-3:]: print(">>", txt(m.get("content") or "")[:700].replace("\n", " | "))
