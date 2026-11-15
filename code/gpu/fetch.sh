#!/usr/bin/env bash
# Download result files from the pod's /workspace/results into the repo's results/ (tar + base64 through the proxy).
# Usage (from the repo root): POD_SSH=... code/gpu/fetch.sh '<glob>'     e.g. 'study_*'  or  'pilot2_*.jsonl'
# Also fetches setup's pip-freeze_*.txt. A file already in results/ is never overwritten; if the pod's copy differs
# (e.g. an earlier fetch caught it mid-run) it is named instead.
# Check the list it prints; then terminate the pod (Runpod console, or the connector's delete-pod).
set -euo pipefail
GLOB="$1"
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
echo "cd /workspace/results && tar czf - $GLOB \$(ls pip-freeze_*.txt 2>/dev/null) | base64 -w 0; echo" > "$TMP/f.sh"
POD_TIMEOUT=900 "$(dirname "$0")/pod.sh" "$TMP/f.sh" > "$TMP/f.b64"
[ -n "$(tr -d '\n ' < "$TMP/f.b64")" ] || { echo "nothing fetched: no file on the pod matches '$GLOB'"; exit 1; }
mkdir "$TMP/x" && tr -d '\n ' < "$TMP/f.b64" | base64 -d | tar xzf - -C "$TMP/x"
ls "$TMP/x"
DIFF=0
for f in "$TMP"/x/*; do
    b=$(basename "$f")
    if [ ! -e "results/$b" ]; then cp "$f" results/
    elif ! cmp -s "$f" "results/$b"; then echo "DIFFERS, not copied: results/$b (if the pod's copy is the complete one: delete it locally, fetch again)"; DIFF=$((DIFF + 1)); fi
done
echo "copied to results/ (existing files not overwritten)"
[ "$DIFF" = 0 ] || { echo "WARNING: $DIFF file(s) differ from the pod's copy and were NOT updated (above)"; exit 1; }
