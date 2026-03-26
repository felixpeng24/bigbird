"""Flask + Flask-SocketIO server for Big Bird installation.

Wires the hardware abstraction layer to HTTP endpoints and WebSocket events:
- MJPEG stream at /api/video_feed
- Capture endpoint at POST /api/capture
- SocketIO phase state machine driven by button presses
"""

import base64
import enum
import json
import logging
import os
import time

from flask import Flask, Response, jsonify, send_from_directory
from flask_socketio import SocketIO, emit

from hardware import create_hardware

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.DEBUG,
    format="[%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Phase state machine
# ---------------------------------------------------------------------------
class Phase(enum.Enum):
    IDLE = "IDLE"
    CAPTURING = "CAPTURING"
    ANALYZING = "ANALYZING"
    CALCULATING = "CALCULATING"
    REVEALING = "REVEALING"
    RESETTING = "RESETTING"


# ---------------------------------------------------------------------------
# App + SocketIO
# ---------------------------------------------------------------------------
app = Flask(__name__, static_folder="static", static_url_path="/static")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "bigbird-dev")

socketio = SocketIO(app, async_mode="threading", cors_allowed_origins="*")

# ---------------------------------------------------------------------------
# Hardware + state
# ---------------------------------------------------------------------------
camera, button = create_hardware()
current_phase: Phase = Phase.IDLE


def _set_phase(new_phase: Phase) -> None:
    """Transition to *new_phase*, log it, and emit a SocketIO event."""
    global current_phase
    old = current_phase
    current_phase = new_phase
    logger.info("[PHASE] %s -> %s", old.value, new_phase.value)
    socketio.emit("phase_change", {"phase": new_phase.value})


def reset_to_idle() -> None:
    """Reset the state machine to IDLE and unlock the button."""
    _set_phase(Phase.IDLE)
    button.unlock()
    logger.info("[PHASE] reset to IDLE — button unlocked")


# ---------------------------------------------------------------------------
# Button callback (wired for both mock trigger and Pi GPIO)
# ---------------------------------------------------------------------------
def handle_button_press() -> None:
    """Handle a physical (or mock) button press."""
    if button.is_locked:
        logger.info("[BUTTON] locked — ignoring press")
        return
    logger.info("[BUTTON] press received")
    button.lock()
    _set_phase(Phase.CAPTURING)


button.on_press(handle_button_press)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    """Serve the frontend SPA."""
    return send_from_directory("static", "index.html")


def _generate_frames():
    """Yield MJPEG frame boundaries from the camera stream."""
    camera.start_stream()
    try:
        while True:
            frame = camera.get_frame()
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
            )
            time.sleep(0.05)  # small safety throttle
    finally:
        camera.stop_stream()


@app.route("/api/video_feed")
def video_feed():
    """MJPEG streaming endpoint — holds connection open."""
    return Response(
        _generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


@app.route("/api/capture", methods=["POST"])
def capture():
    """Capture a single frame and return as base64 JSON."""
    frame = camera.capture_frame()
    b64 = base64.b64encode(frame).decode("utf-8")
    logger.info("[CAPTURE] frame captured — %d bytes, base64 length %d", len(frame), len(b64))
    return jsonify({"image": b64, "phase": Phase.CAPTURING.value})


# ---------------------------------------------------------------------------
# SocketIO events
# ---------------------------------------------------------------------------
@socketio.on("button_press")
def on_button_press():
    """Client-side button press (spacebar in the browser)."""
    handle_button_press()


@socketio.on("connect")
def on_connect():
    logger.info("[SOCKET] client connected")
    emit("phase_change", {"phase": current_phase.value})


@socketio.on("disconnect")
def on_disconnect():
    logger.info("[SOCKET] client disconnected")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    logger.info("[SERVER] Starting Big Bird server on port 8080")
    socketio.run(app, host="0.0.0.0", port=8080, debug=True, allow_unsafe_werkzeug=True)
