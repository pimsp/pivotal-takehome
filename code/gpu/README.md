# Running on a rented GPU (Runpod)

The runbook for running this project's code on a Runpod GPU pod. Adapted on 2026-11-15 from a working setup in
another project. Billing runs per second while a pod exists: **fetch the results, then delete the pod.**

## The standard workflow (what Claude does)

Use a fresh pod for each job and delete it afterwards. There is no network volume: each pod installs its venv and
downloads its model (if `MODEL` is set) during setup. The downloads use the data center's bandwidth, not yours.

**0. Check before creating** (prices and templates change; the numbers below are from 2026-11-15):
```bash
runpodctl gpu list                       # securePricePerHr and stockStatus per GPU
runpodctl template get runpod-torch-v280 # does the template still exist?
runpodctl user                           # balance
```
Pim confirms the GPU, the price and the expected duration before any pod is created.

**1. Create the pod:**
```bash
runpodctl pod create --name pivotal-<job> --gpu-id "NVIDIA A40" --template-id runpod-torch-v280 \
  --min-cuda-version 12.8 --container-disk-in-gb 60            # prints the pod, with its id
runpodctl pod get <id>                                          # repeat until it is running
```
Don't use `--wait`: it tests the pod's direct SSH port from this machine, which some networks block (see "Why the
proxy"). On a timeout it also keeps the pod running.
- GPU: **A40** (48 GB), Secure Cloud, **$0.59/h** (2026-11-15). Other 48 GB options: RTX A6000 ($0.69/h), L40S
  ($1.09/h). If 24 GB is enough: RTX 3090 ($0.50/h) or L4 ($0.69/h). Any data center will do.
- Template **Runpod PyTorch 2.8** (`runpod-torch-v280`: image `runpod/pytorch:1.0.2-cu1281-torch280-ubuntu2404`,
  50 GB volume on `/workspace`). Use `--min-cuda-version 12.8` to match the image's CUDA. Raise it if a dependency
  needs a newer driver (a vLLM built for CUDA 13 needs `13.0`).
- Container disk: 60 GB holds the venv. The model goes to `/workspace`, which is the template's 50 GB volume. For a
  bigger model, add `--volume-in-gb 100`.
- The SSH proxy user looks like `<podid>-<number>@ssh.runpod.io`. You find it in the web console's Connect tab.
  `runpodctl pod get <id>` shows only the direct SSH command, with the key in `~/.runpod/ssh/`.

**Why `runpodctl`:** the Runpod connector doesn't reach Kiteline tabs. `runpodctl` (v3.1.1, `~/.local/bin`) uses the
API key Pim saved with `runpodctl doctor`. Claude never handles the key. Fallback: Pim creates the pod in the web
console with the same settings and gives the session the SSH proxy user. Steps 2 and 3 only need SSH with Pim's key.

**2. Run it with the scripts in this folder.** Run them from the repo root, with the code in `code/`.
`POD_SSH` is the proxy user from step 1.
```bash
export POD_SSH=<podid-xxxx@ssh.runpod.io>
code/gpu/bootstrap.sh 90                  # safety timer (stops the pod after 90 min whatever happens) + upload code/ + setup
code/gpu/setup_state.sh                   # repeat until STATE=done (a few min; longer with a big MODEL)
code/gpu/start.sh job1 "python <script>.py --out /workspace/results/job1_..."
code/gpu/status.sh job1                   # STATE=running|done|failed|died + summary lines; repeat
code/gpu/fetch.sh 'job1_*'                # copy result files (and setup's pip-freeze) into results/
runpodctl pod delete <id>                 # once fetch.sh has listed the files
```
- **What the pod gets:** `bootstrap.sh` uploads `code/` without `.venv/` and `data/`. Everything travels as base64
  through the proxy, so large data files should be downloaded on the pod as part of the command. Setup makes a
  Python 3.13 venv with uv and installs `code/requirements.txt` there. List torch in that file if the code needs it,
  because the template's own torch is not in the venv.
- **Model:** put `MODEL=<hf id>` before `bootstrap.sh` and setup downloads that model to `/workspace/hf` (`HF_HOME`).
  Without `MODEL`, nothing is downloaded.
- **Results:** the code should write its outputs to `/workspace/results/`. `fetch.sh` brings matching files back to
  `results/`. It never overwrites a local file, and it names any file that differs from the pod's copy.

**The safety timer** *stops* the pod. It does not delete it. GPU billing ends and `/workspace` is kept (a little
storage billing continues). But a stopped pod often can't be restarted, so results you haven't fetched may be out of
reach. Set the timer to the job's expected length plus setup plus time for fetching, and **fetch before it runs out**.
After the run, `start.sh` leaves 30 minutes (`STOP_AFTER`) for fetching, then stops the pod. Then delete the pod
(`runpodctl pod delete <id>`, or in the web console) and commit `results/`.

| Script | Does |
| --- | --- |
| `pod.sh` | runs a local script on the pod through Runpod's SSH proxy and prints its output (the base of the others) |
| `bootstrap.sh [min]` | starts the safety timer, uploads `code/` as base64, prints the `.py` checksums (local and pod), starts `setup.sh` |
| `setup_state.sh` | is setup done? |
| `start.sh <name> "<cmd>"` | starts a run in the background (survives dropped connections); log `/workspace/<name>.log`, ending `=== ALL DONE` or `=== FAILED`; afterwards the pod waits `STOP_AFTER` minutes (default 30), then stops itself |
| `status.sh <name>` | state of that run, and its log lines starting `===`, `# `, `Wrote`, `Saved` or `Result`, its errors, and its last line; `STATUS_GREP='<regex>'` for other lines |
| `fetch.sh '<glob>'` | downloads matching files from `/workspace/results` into `results/` |
| `keepalive.sh [min]` | for when you'll be offline when a run ends: disables the post-run stop and starts a new safety timer (default 150 min) |
| `setup.sh` | runs *on* the pod: uv, a Python 3.13 venv in `/root/venv` with `code/requirements.txt`, the model download (`MODEL`), `pip freeze` |

**Why the proxy:** some networks (Pim's mobile data) block a pod's direct SSH port, and the proxy uses port 22. The
proxy needs a terminal and has no scp, so scripts are piped in and files travel as base64 (`pod.sh` handles both).

**Practicalities:**
- Two pods at once: give each command its own `POD_SSH=...` prefix rather than exporting one.
- Stopped pods often can't be restarted (their machine's GPU gets rented out), and a stopped pod's disk is only
  reachable after a restart, so fetch before the pod stops.
- The commands in `start.sh` run in `/workspace/code` with the venv active and `HF_HOME=/workspace/hf`.
- For progress you can read with `status.sh`, have the code print lines starting `# ` or `Wrote <file>`.
- Proxy user unknown: the scripts also work over direct SSH. Put a wrapper `exec /usr/bin/ssh -F <cfg> "$@"` first on
  PATH, where `<cfg>` has a Host alias with the IP, port and key from `runpodctl pod get`. Then set `POD_SSH=<alias>`.

## Stopping a pod yourself (e.g. if Claude's session limit is hit)
- **Web console** (also on a phone): https://www.runpod.io/console/pods → the pod → **Terminate** (deletes it and
  its disk; only after the results are fetched) or **Stop** (GPU billing stops and the disk is kept, but restarting
  may fail).
- Every pod has a safety timer (`bootstrap.sh`) and stops itself after a run (`start.sh`).
- Spending is capped by the prepaid credit.
