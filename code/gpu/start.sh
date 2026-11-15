#!/usr/bin/env bash
# Start a run on the pod in the background (survives a dropped connection), logging to /workspace/<name>.log.
# The log ends "=== ALL DONE" if every command succeeded, "=== FAILED (exit n)" if one failed (the rest are skipped).
# After the run, the pod waits STOP_AFTER minutes (default 30) and then stops itself, so results can be fetched first.
# Usage: POD_SSH=... code/gpu/start.sh <name> "<command, run in /workspace/code with the venv active>"
#   e.g. code/gpu/start.sh pilot "python run_study.py --n 40 --samples 2 --seed 396000 --plans-only"
# Several commands: separate them with ';' or newlines inside the quotes; any quotes in them are kept as written
# (the command travels as a file, base64). A second model (e.g. phi-4) can use HF_HOME=/root/hf (the pod's own
# disk) so /workspace keeps room.
set -euo pipefail
NAME="$1"; CMD="$2"; AFTER="${STOP_AFTER:-30}"
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
{
  echo 'cd /workspace/code && source /root/venv/bin/activate && export HF_HOME=/workspace/hf'
  echo '( set -eo pipefail'
  printf '%s\n' "$CMD"
  echo ')'
  echo 'rc=$?; if [ $rc = 0 ]; then echo "=== ALL DONE"; else echo "=== FAILED (exit $rc)"; fi'
  echo "sleep $((AFTER * 60)); runpodctl stop pod \$RUNPOD_POD_ID"
} > "$TMP/run.sh"
{
  echo "base64 -d > /workspace/$NAME.run.sh <<'B64EOF'"; base64 "$TMP/run.sh"; echo B64EOF
  echo "nohup bash /workspace/$NAME.run.sh > /workspace/$NAME.log 2>&1 &"
  echo "echo started $NAME"
} > "$TMP/start.sh"
"$(dirname "$0")/pod.sh" "$TMP/start.sh"
