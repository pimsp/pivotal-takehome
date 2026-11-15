"""First look: schemas, row counts, join. Usage: python -I inspect_basic.py <rawdir>"""
import sys, glob, pandas as pd, pyarrow.parquet as pq
raw = sys.argv[1]
t = pd.read_parquet(f"{raw}/data/tool-00000-of-00008.parquet")
s = pd.concat([pd.read_parquet(f) for f in sorted(glob.glob(f"{raw}/data/train-*.parquet"))])
print("traj", t.shape); print(t.dtypes)
print("tasks", s.shape); print(s.dtypes)
print("traj unique ids", t.instance_id.nunique(), "task unique ids", s.instance_id.nunique())
m = t.instance_id.isin(s.instance_id)
print("traj rows matched", m.sum(), "/", len(t))
print(t[~m].instance_id.head().tolist())
for c in t.columns:
    if c != "messages": print(c, repr(t[c].iloc[0])[:300])
for c in s.columns: print("S", c, repr(s[c].iloc[0])[:300])
