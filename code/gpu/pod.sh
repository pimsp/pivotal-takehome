#!/usr/bin/env bash
# Run a local bash script on a Runpod pod through Runpod's SSH proxy and print its output.
# Usage: POD_SSH=<podid-xxxx@ssh.runpod.io> code/gpu/pod.sh script.sh
# Why the proxy: some networks (e.g. Pim's mobile data) block the pods' direct SSH ports; the proxy uses port 22.
# The proxy needs a terminal (-tt) and has no scp, so the script is piped in, and the output is cut out between
# markers (written split, '__B''EGIN__', so the echoed input never matches them).
set -euo pipefail
: "${POD_SSH:?set POD_SSH, e.g. POD_SSH=abc123-64411xyz@ssh.runpod.io (from the pod Connect menu or the create-pod result)}"
{ echo "stty -echo; echo __B''EGIN__"; cat "$1"; echo; echo "echo __E''ND__; exit"; } \
| timeout "${POD_TIMEOUT:-600}" ssh -tt -o StrictHostKeyChecking=accept-new -o ConnectTimeout=20 "$POD_SSH" 2>/dev/null \
| tr -d '\r' \
| sed 's/\x1b\][^\x07]*\x07//g; s/\x1b\[[?0-9;]*[a-zA-Z]//g' \
| awk '/^__BEGIN__$/{on=1; next} /^__END__$/{on=0} on && !/^(\(venv\) )?root@.*# *$/' | grep -v '^> *$' || true
