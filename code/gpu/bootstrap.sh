#!/usr/bin/env bash
# Prepare a fresh pod: start a safety timer, upload this repo's code/ (as base64 through the proxy), run setup.sh.
# Usage (from the repo root): POD_SSH=... [MODEL=<hf id>] code/gpu/bootstrap.sh [safety-timer-minutes, default 120]
# The timer stops the pod (not terminates): set it to the run plus fetching (README, "The safety timer").
# MODEL: a Hugging Face model for setup.sh to download to /workspace/hf (default none: no download).
# code/ travels through the proxy as base64, so keep it small: .venv/ and data/ are left out (download data on the pod).
# The checksums of code/'s .py files are printed here and on the pod, to see that the pod runs this code.
# Then wait for setup (a few min; longer with a large MODEL): POD_SSH=... code/gpu/setup_state.sh
set -euo pipefail
MIN="${1:-120}"
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
tar czf "$TMP/code.tgz" --exclude=__pycache__ --exclude=.venv --exclude=data code
SUMS="find code -name '*.py' -not -path '*/__pycache__/*' -not -path '*/.venv/*' | sort | xargs -r md5sum"
{
  echo "nohup bash -c 'sleep ${MIN}m; runpodctl stop pod \$RUNPOD_POD_ID' > /workspace/stop-timer.log 2>&1 &"
  echo "echo \"safety timer: pod stops at \$(date -u -d '+${MIN} minutes' +%H:%M) UTC\""
  echo 'base64 -d > /workspace/code.tgz <<"B64EOF"'; base64 "$TMP/code.tgz"; echo B64EOF
  echo "cd /workspace && rm -rf code && tar xzf code.tgz --no-same-owner && rm -f code.tgz && mkdir -p results && $SUMS"
  echo "cd /workspace/code && MODEL=${MODEL:-} nohup bash gpu/setup.sh > /workspace/setup.log 2>&1 & echo \"setup started\""
} > "$TMP/boot.sh"
eval "$SUMS"
"$(dirname "$0")/pod.sh" "$TMP/boot.sh"
