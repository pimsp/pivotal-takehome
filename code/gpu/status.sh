#!/usr/bin/env bash
# Status of a run started with start.sh: STATE=done|failed|running|died, plus the summary lines of its log
# and its last line (or progress bar).
# Summary lines: start.sh's "===" markers, Python errors, and lines starting "Wrote", "Saved", "Result" or "#"
# (print those from the code for anything worth seeing mid-run). Another pattern: STATUS_GREP='<extended regex>'.
# Usage: POD_SSH=... code/gpu/status.sh <name>
NAME="$1"
PAT="${STATUS_GREP:-^===|^# |^(Wrote|Saved|Result)|Traceback|Error|Killed|CUDA out of memory}"
TMP=$(mktemp); trap 'rm -f "$TMP"' EXIT
cat > "$TMP" <<S
if grep -q "=== ALL DONE" /workspace/$NAME.log; then echo STATE=done; elif grep -q "=== FAILED" /workspace/$NAME.log; then echo STATE=failed; elif pgrep -f "/workspace/$NAME.run.sh" >/dev/null; then echo STATE=running; else echo STATE=died; fi
grep -E '$PAT' /workspace/$NAME.log | tail -40
tail -c 300 /workspace/$NAME.log | tr "\r" "\n" | grep -v "^\$" | tail -1
S
"$(dirname "$0")/pod.sh" "$TMP"
