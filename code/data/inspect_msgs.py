"""Message structure of one trajectory. Usage: python -I inspect_msgs.py <rawdir> [row]"""
import sys, json, pandas as pd
t = pd.read_parquet(f"{sys.argv[1]}/data/tool-00000-of-00008.parquet")
row = int(sys.argv[2]) if len(sys.argv) > 2 else 0
print(type(t.messages.iloc[row]))
msgs = json.loads(t.messages.iloc[row])
print(len(msgs), "messages; keys:", {k for m in msgs for k in m})
for i, m in enumerate(msgs):
    c = m.get("content")
    if isinstance(c, list): c = " | ".join(str(x.get("text", x))[:200] for x in c)
    print(f"--- {i} {m['role']} keys={list(m)}")
    print(str(c)[:500 if i < 2 else 250])
    if m.get("tool_calls"): print("  TOOL_CALLS:", json.dumps(m["tool_calls"])[:400])
