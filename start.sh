#!/usr/bin/env bash
# start.sh — Launch Big Bird installation on Raspberry Pi
#
# Starts the Flask server and opens Chromium in kiosk mode.
# Designed to be called by bigbird.service on boot.
#
# Usage:
#   ./start.sh          # normal launch
#   ./start.sh --no-browser  # server only (for development)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PORT=8080
URL="http://localhost:${PORT}"
LOG_DIR="${SCRIPT_DIR}/logs"
SERVER_LOG="${LOG_DIR}/server.log"

mkdir -p "$LOG_DIR"

# -----------------------------------------------------------------------
# Pi display configuration
# -----------------------------------------------------------------------
setup_display() {
    # Hide mouse cursor (requires unclutter)
    if command -v unclutter &>/dev/null; then
        unclutter -idle 0 -root &
        echo "[STARTUP] Cursor hidden via unclutter"
    else
        echo "[STARTUP] unclutter not installed — cursor will be visible"
    fi

    # Disable screen blanking / screensaver
    if command -v xset &>/dev/null; then
        xset s off
        xset -dpms
        xset s noblank
        echo "[STARTUP] Screen blanking disabled"
    fi
}

# -----------------------------------------------------------------------
# Start Flask server
# -----------------------------------------------------------------------
start_server() {
    echo "[STARTUP] Starting Flask server on port ${PORT}..."
    cd "$SCRIPT_DIR"

    # Load .env if present
    if [ -f .env ]; then
        set -a
        source .env
        set +a
        echo "[STARTUP] Loaded .env"
    fi

    python server.py >> "$SERVER_LOG" 2>&1 &
    SERVER_PID=$!
    echo "[STARTUP] Server PID: ${SERVER_PID}"

    # Wait for server to be ready
    echo "[STARTUP] Waiting for server on port ${PORT}..."
    for i in $(seq 1 30); do
        if curl -s -o /dev/null "http://localhost:${PORT}" 2>/dev/null; then
            echo "[STARTUP] Server is ready"
            return 0
        fi
        sleep 1
    done

    echo "[STARTUP] ERROR: Server did not start within 30 seconds"
    return 1
}

# -----------------------------------------------------------------------
# Start Chromium in kiosk mode
# -----------------------------------------------------------------------
start_browser() {
    if [ "${1:-}" = "--no-browser" ]; then
        echo "[STARTUP] Skipping browser (--no-browser flag)"
        return 0
    fi

    echo "[STARTUP] Launching Chromium in kiosk mode..."

    # Find chromium binary (varies by Pi OS version)
    CHROMIUM=""
    for candidate in chromium-browser chromium google-chrome; do
        if command -v "$candidate" &>/dev/null; then
            CHROMIUM="$candidate"
            break
        fi
    done

    if [ -z "$CHROMIUM" ]; then
        echo "[STARTUP] ERROR: No Chromium binary found"
        return 1
    fi

    "$CHROMIUM" \
        --kiosk \
        --noerrdialogs \
        --disable-infobars \
        --disable-session-crashed-bubble \
        --disable-restore-session-state \
        --disable-features=TranslateUI \
        --disable-pinch \
        --overscroll-history-navigation=0 \
        --check-for-update-interval=31536000 \
        --autoplay-policy=no-user-gesture-required \
        --no-first-run \
        --start-fullscreen \
        --window-size=1024,600 \
        --window-position=0,0 \
        "$URL" &

    BROWSER_PID=$!
    echo "[STARTUP] Chromium PID: ${BROWSER_PID}"
}

# -----------------------------------------------------------------------
# Cleanup on exit
# -----------------------------------------------------------------------
cleanup() {
    echo "[STARTUP] Shutting down..."
    kill "$SERVER_PID" 2>/dev/null || true
    kill "$BROWSER_PID" 2>/dev/null || true
    wait 2>/dev/null
    echo "[STARTUP] Done"
}

trap cleanup EXIT INT TERM

# -----------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------
echo "============================================"
echo " BIG BIRD IS WATCHING YOU"
echo " $(date)"
echo "============================================"

# Only configure display if we have a DISPLAY
if [ -n "${DISPLAY:-}" ]; then
    setup_display
fi

start_server
start_browser "$@"

# Keep script alive (server and browser are backgrounded)
echo "[STARTUP] Installation running. Press Ctrl+C to stop."
wait
