"""List the files of the SWE-smith datasets on the HF hub (no download)."""
from huggingface_hub import HfApi
api = HfApi()
for repo in ["SWE-bench/SWE-smith-trajectories", "SWE-bench/SWE-smith"]:
    info = api.dataset_info(repo, files_metadata=True)
    print(repo)
    for s in info.siblings:
        print(f"  {s.rfilename}  {(s.size or 0)/1e6:.1f} MB")
