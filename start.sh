#!/bin/bash
set -Eeuo pipefail

pids=()
cleanup() {
    trap - EXIT TERM INT
    if ((${#pids[@]})); then
        kill "${pids[@]}" 2>/dev/null || true
        wait "${pids[@]}" 2>/dev/null || true
    fi
}
trap cleanup EXIT
trap 'exit 0' TERM INT

# No host display socket or privileged container is needed.
Xvfb "$DISPLAY" -screen 0 800x700x24 -nolisten tcp &
pids+=("$!")
ready=false
for ((attempt=0; attempt<100; attempt++)); do
    if xdpyinfo -display "$DISPLAY" >/dev/null 2>&1; then
        ready=true
        break
    fi
    sleep 0.1
done
if [[ "$ready" != true ]]; then
    echo "Virtual display did not start" >&2
    exit 1
fi

# VNC is internal only. Browser access is through the SSH tunnel.
x11vnc -display "$DISPLAY" -localhost -rfbport 5900 -nopw \
    -forever -shared -xkb &
pids+=("$!")
websockify --web=/usr/share/novnc 6080 127.0.0.1:5900 &
pids+=("$!")
python3 /app/game.py &
pids+=("$!")

# If any service exits, stop the others instead of leaving a broken container.
set +e
wait -n "${pids[@]}"
status=$?
set -e
exit "$status"
