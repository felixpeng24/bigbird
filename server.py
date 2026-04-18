"""Flask + Flask-SocketIO server for Big Bird installation.

Wires the hardware abstraction layer to HTTP endpoints and WebSocket events:
- MJPEG stream at /api/video_feed
- Capture endpoint at POST /api/capture
- Analyze endpoint at POST /api/analyze (OpenAI vision)
- SocketIO phase state machine driven by button presses
- Full phase loop: IDLE → CAPTURING → ANALYZING → CALCULATING → REVEALING → RESETTING → IDLE
"""

import base64
import enum
import json
import logging
import os
import time
import threading

from dotenv import load_dotenv
from flask import Flask, Response, jsonify, request, send_from_directory
from flask_socketio import SocketIO, emit

from audio import speak, speak_sync
from hardware import create_hardware
from prompts import build_messages, parse_response, REFUSAL_FALLBACK, DEMOGRAPHIC_LABELS, DEMOGRAPHIC_KEYS
from scores import generate_score

# ---------------------------------------------------------------------------
# Env
# ---------------------------------------------------------------------------
load_dotenv()

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


def _set_phase(new_phase: Phase, data: dict | None = None) -> None:
    """Transition to *new_phase*, log it, and emit a SocketIO event."""
    global current_phase
    old = current_phase
    current_phase = new_phase
    logger.info("[PHASE] %s -> %s", old.value, new_phase.value)
    payload = {"phase": new_phase.value}
    if data:
        payload["data"] = data
    socketio.emit("phase_change", payload)


def reset_to_idle() -> None:
    """Reset the state machine to IDLE and unlock the button."""
    _set_phase(Phase.IDLE)
    button.unlock()
    logger.info("[PHASE] reset to IDLE — button unlocked")


# ---------------------------------------------------------------------------
# OpenAI client (lazy init)
# ---------------------------------------------------------------------------
_openai_client = None


def _get_openai_client():
    """Lazily initialize the OpenAI client."""
    global _openai_client
    if _openai_client is None:
        try:
            import openai
            api_key = os.environ.get("OPENAI_API_KEY")
            if not api_key:
                logger.warning("[ANALYZE] OPENAI_API_KEY not set — analyze will always return fallback")
                return None
            _openai_client = openai.OpenAI(api_key=api_key)
            logger.info("[ANALYZE] OpenAI client initialized")
        except ImportError:
            logger.warning("[ANALYZE] openai package not installed")
            return None
    return _openai_client


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

    # Kick off the evaluation loop in a background thread
    threading.Thread(target=_run_evaluation_loop, daemon=True).start()


def _run_evaluation_loop() -> None:
    """Run the full evaluation cycle in a background thread.

    CAPTURING → ANALYZING → CALCULATING → REVEALING → RESETTING → IDLE
    """
    try:
        # Brief pause in CAPTURING phase
        speak_sync("Target acquired.")
        time.sleep(0.5)

        # --- CAPTURE ---
        frame = camera.capture_frame()
        image_b64 = base64.b64encode(frame).decode("utf-8")
        logger.info("[CAPTURE] frame captured — %d bytes", len(frame))

        # --- ANALYZE ---
        _set_phase(Phase.ANALYZING)
        demographics = _call_vision_api(image_b64)

        # Photo is used and discarded — R018
        del frame, image_b64

        # Send demographics to frontend
        _set_phase(Phase.ANALYZING, data={"demographics": demographics})

        # Speak demographics, timed to match frontend reveal (1.8s per attribute)
        if demographics.get("refused"):
            speak_sync("Subject defies classification.")
            time.sleep(3.0)
        else:
            speak_sync("Subject analysis complete. Displaying results.")
            for i, key in enumerate(DEMOGRAPHIC_KEYS):
                # Wait for frontend to reveal this attribute (1.8s delay per)
                time.sleep(1.8)
                value = demographics.get(key, "UNKNOWN")
                label = DEMOGRAPHIC_LABELS.get(key, key).lower().replace("_", " ")
                speak_sync(f"{label}: {value}")
            # Hold demographics on screen for 3 seconds after all are shown
            time.sleep(3.0)

        # --- BRIEF TRANSITION: explain what's happening ---
        _set_phase(Phase.ANALYZING, data={"demographics": demographics, "transition": True})
        speak_sync("Using detected attributes to calculate Leadership Index.")
        time.sleep(2.0)

        # --- CALCULATE ---
        _set_phase(Phase.CALCULATING)
        speak_sync("Computing your Leadership Index. Please stand by.")
        time.sleep(6.0)  # calculation theater runs on frontend

        # --- REVEAL ---
        score = generate_score()
        _set_phase(Phase.REVEALING, data={"score": score})
        speak_sync(f"Your Leadership Index has been calculated.")
        time.sleep(5.0)

        # --- RESET ---
        _set_phase(Phase.RESETTING)
        speak_sync("Evaluation complete. Returning to surveillance mode.")
        time.sleep(2.0)

        # --- IDLE ---
        reset_to_idle()

    except Exception as exc:
        logger.error("[LOOP] Evaluation loop failed: %s", exc, exc_info=True)
        # Ensure we always return to idle
        try:
            reset_to_idle()
        except Exception:
            pass


def _call_vision_api(image_b64: str) -> dict:
    """Call OpenAI vision API. Returns demographics dict or fallback."""
    client = _get_openai_client()
    if client is None:
        logger.info("[ANALYZE] No OpenAI client — returning fallback")
        return dict(REFUSAL_FALLBACK)

    try:
        messages = build_messages(image_b64)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=300,
            temperature=0.7,
        )
        text = response.choices[0].message.content
        logger.info("[ANALYZE] Raw response: %s", text[:300])
        return parse_response(text)

    except Exception as exc:
        logger.error("[ANALYZE] API call failed: %s", exc)
        # R016: network failure → skip demographics, still deliver a score
        return dict(REFUSAL_FALLBACK)


button.on_press(handle_button_press)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    """Serve the frontend SPA."""
    return send_from_directory("static", "index.html")


@app.route("/build-guide")
def build_guide():
    """Serve the build guide."""
    return send_from_directory("static", "build-guide.html")


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


@app.route("/api/analyze", methods=["POST"])
def analyze():
    """Analyze a captured image via OpenAI vision API.

    Expects JSON body: {"image": "<base64-encoded JPEG>"}
    Returns demographics JSON or fallback.
    """
    body = request.get_json(silent=True)
    if not body or "image" not in body:
        return jsonify({"error": "Missing 'image' field"}), 400

    image_b64 = body["image"]
    demographics = _call_vision_api(image_b64)
    return jsonify(demographics)


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
    socketio.run(app, host="0.0.0.0", port=8080, debug=False, allow_unsafe_werkzeug=True)
