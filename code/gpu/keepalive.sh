#!/usr/bin/env bash
# Keep the pod from stopping itself after the run (e.g. when you'll be offline when it finishes): disables the
# post-run stop and the old safety timer, and starts a new safety timer of MIN minutes (default 150).
# Usage: POD_SSH=... code/gpu/keepalive.sh [minutes]       Worst case cost: MIN minutes of idle GPU ($0.59/h on an A40).
MIN="${1:-150}"
TMP=$(mktemp); trap 'rm -f "$TMP"' EXIT
cat > "$TMP" <<S
R=\$(which runpodctl); mv "\$R" "\$R.real" && echo "post-run stop and old timer disabled"
pkill -f "sleep [0-9]*m"; sleep 1
nohup bash -c "sleep ${MIN}m; \$R.real stop pod \\\$RUNPOD_POD_ID" > /workspace/stop-timer2.log 2>&1 &
echo "new safety timer: pod stops at \$(date -u -d '+${MIN} minutes' +%H:%M) UTC"
S
"$(dirname "$0")/pod.sh" "$TMP"
