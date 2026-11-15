#!/usr/bin/env bash
# Is setup.sh on the pod done? Prints STATE=done|running|failed|died and the tail of the log.
# Usage: POD_SSH=... code/gpu/setup_state.sh       (loop: until ... | grep -q STATE=done; do sleep 30; done)
TMP=$(mktemp); trap 'rm -f "$TMP"' EXIT
cat > "$TMP" <<'S'
if grep -q "Setup done" /workspace/setup.log; then echo STATE=done; elif grep -qiE "error|traceback|killed" /workspace/setup.log; then echo STATE=failed; elif pgrep -f gpu/setup.sh >/dev/null; then echo STATE=running; else echo STATE=died; fi; tail -c 400 /workspace/setup.log
S
"$(dirname "$0")/pod.sh" "$TMP"
