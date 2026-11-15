#!/usr/bin/env bash
# Run on a fresh pod (Runpod "PyTorch" template), from /workspace/code. The model goes to /workspace (the pod's volume).
# The venv goes to VENV: default /root/venv on the fast local disk, because /workspace can be a network
# drive where thousands of small files make installs and imports slow. The local disk is wiped when the
# pod stops, so after a restart this script reinstalls the venv but reuses the model.
# Python 3.13 through uv, as on the laptop; the dependencies are code/requirements.txt (the same file used locally),
# so list torch there if the code needs it (the template's own torch is not in this venv).
set -euo pipefail
export HF_HOME=/workspace/hf
MODEL=${MODEL:-}
VENV=${VENV:-/root/venv}
export PATH=/root/.local/bin:$PATH
if [ ! -x $VENV/bin/python ]; then
    command -v uv >/dev/null || curl -LsSf https://astral.sh/uv/install.sh | sh
    uv venv -q --python 3.13 $VENV
    uv pip install -q --python $VENV/bin/python huggingface_hub
    if [ -f requirements.txt ]; then uv pip install -q --python $VENV/bin/python -r requirements.txt; fi
fi
if [ -n "$MODEL" ]; then $VENV/bin/python -c "from huggingface_hub import snapshot_download; snapshot_download('$MODEL')"; fi
mkdir -p /workspace/results   # exact versions; fetch.sh brings them back with the results
uv pip freeze --python $VENV/bin/python > /workspace/results/pip-freeze_$(date -u +%Y%m%d-%H%M%S).txt
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv
echo "Setup done. Model: ${MODEL:-none}. Activate with: source $VENV/bin/activate."
