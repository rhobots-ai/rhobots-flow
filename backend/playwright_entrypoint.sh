#!/usr/bin/env bash
set -euo pipefail

# Config
export DISPLAY=${DISPLAY:-:99}
SCREEN_RESOLUTION=${SCREEN_RESOLUTION:-1920x1080x24}
VNC_PASSWORD=${VNC_PASSWORD:-automation}
VNC_PORT=${VNC_PORT:-5900}
NOVNC_PORT=${NOVNC_PORT:-7900}
CHROME_BIN=${CHROME_BIN:-google-chrome}

echo "[entrypoint] Starting virtual display on $DISPLAY with resolution $SCREEN_RESOLUTION"
# Start Xvfb
Xvfb "$DISPLAY" -screen 0 "$SCREEN_RESOLUTION" &

# Optional lightweight window manager for better rendering
if command -v fluxbox >/dev/null 2>&1; then
  echo "[entrypoint] Starting fluxbox window manager"
  fluxbox &
fi

# Start Chrome in non-headless mode attached to the virtual display, with CDP enabled
echo "[entrypoint] Starting Chrome with CDP on :9222"
$CHROME_BIN \
  --remote-debugging-port=9222 \
  --remote-debugging-address=0.0.0.0 \
  --no-sandbox \
  --disable-dev-shm-usage \
  --disable-gpu \
  --no-first-run \
  --no-default-browser-check \
  --start-maximized \
  about:blank &

# Wait briefly to let X and Chrome initialize
sleep 2

# Start x11vnc to expose the virtual display over VNC
echo "[entrypoint] Starting x0vncserver on port $VNC_PORT"
# Configure VNC password and start x0vncserver to expose the existing X display
if command -v vncpasswd >/dev/null 2>&1; then
  if [ -n "$VNC_PASSWORD" ]; then
    echo "$VNC_PASSWORD" | vncpasswd -f > /tmp/vncpass
    x0vncserver -display "$DISPLAY" -rfbauth /tmp/vncpass -rfbport "$VNC_PORT" -forever -shared >/dev/null 2>&1 &
  else
    x0vncserver -display "$DISPLAY" -rfbport "$VNC_PORT" -forever -shared >/dev/null 2>&1 &
  fi
else
  echo "[entrypoint] ERROR: vncpasswd not found; is tigervnc installed?"
  exit 1
fi

# Start noVNC (websockify) to proxy VNC to a websocket on NOVNC_PORT
NOVNC_WEB_DIR="/opt/novnc"

echo "[entrypoint] Starting noVNC websockify on port $NOVNC_PORT (serving $NOVNC_WEB_DIR)"
websockify --web="$NOVNC_WEB_DIR" "$NOVNC_PORT" "localhost:$VNC_PORT" &

echo "[entrypoint] Services started:
- Xvfb on $DISPLAY
- Chrome (CDP) on 0.0.0.0:9222
- VNC on localhost:$VNC_PORT
- noVNC websocket on 0.0.0.0:$NOVNC_PORT

Health checks:
- CDP: curl http://localhost:9222/json/version
- noVNC: open ws://<host>:$NOVNC_PORT (served via web/proxy at /vnc)
"

# Keep container running and forward logs
tail -f /dev/null
