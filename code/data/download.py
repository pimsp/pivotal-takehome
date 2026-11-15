"""Download one tool-split trajectory file and the SWE-smith task files that cover its instance_ids.

Usage: python -I code/data/download.py <outdir>
Files are saved exactly as published (no filtering).
"""
import sys
import pyarrow.parquet as pq
from huggingface_hub import hf_hub_download, HfFileSystem

out = sys.argv[1]
traj = hf_hub_download("SWE-bench/SWE-smith-trajectories", "data/tool-00000-of-00008.parquet",
                       repo_type="dataset", local_dir=out)
ids = set(pq.read_table(traj, columns=["instance_id"]).column("instance_id").to_pylist())
print("trajectory ids:", len(ids))

fs = HfFileSystem()
remaining = set(ids)
for f in sorted(fs.glob("datasets/SWE-bench/SWE-smith/data/*.parquet")):
    with fs.open(f) as fh:  # reads only the instance_id column chunks remotely
        task_ids = set(pq.read_table(fh, columns=["instance_id"]).column("instance_id").to_pylist())
    hit = ids & task_ids
    print(f.split("/")[-1], "rows", len(task_ids), "covers", len(hit))
    if hit:
        hf_hub_download("SWE-bench/SWE-smith", f.split("SWE-smith/")[1], repo_type="dataset", local_dir=out)
        remaining -= hit
print("trajectory ids not found in any task file:", len(remaining))
