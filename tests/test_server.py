"""Tests for the Flask server endpoints and phase management."""

import base64
import json

import pytest

from server import Phase, app, button, camera, current_phase, reset_to_idle, socketio
import server as server_module


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def _reset_state():
    """Reset server state between tests."""
    server_module.current_phase = Phase.IDLE
    button.unlock()
    yield
    server_module.current_phase = Phase.IDLE
    button.unlock()


@pytest.fixture
def client():
    """Flask test client."""
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


@pytest.fixture
def socketio_client():
    """Flask-SocketIO test client."""
    app.config["TESTING"] = True
    client = socketio.test_client(app)
    # Drain the initial phase_change emitted on connect
    client.get_received()
    yield client
    client.disconnect()


# ---------------------------------------------------------------------------
# App creation tests
# ---------------------------------------------------------------------------

class TestAppCreation:
    """Server module imports and creates app without errors."""

    def test_app_exists(self):
        assert app is not None

    def test_socketio_exists(self):
        assert socketio is not None

    def test_phase_enum_has_all_values(self):
        names = {p.name for p in Phase}
        assert names == {"IDLE", "CAPTURING", "ANALYZING", "CALCULATING", "REVEALING", "RESETTING"}


# ---------------------------------------------------------------------------
# Phase management tests
# ---------------------------------------------------------------------------

class TestPhaseManagement:
    """Phase state machine transitions."""

    def test_initial_phase_is_idle(self):
        assert server_module.current_phase == Phase.IDLE

    def test_reset_to_idle(self):
        server_module.current_phase = Phase.CAPTURING
        button.lock()
        reset_to_idle()
        assert server_module.current_phase == Phase.IDLE
        assert button.is_locked is False


# ---------------------------------------------------------------------------
# Capture endpoint tests
# ---------------------------------------------------------------------------

class TestCaptureEndpoint:
    """POST /api/capture returns base64-encoded JPEG."""

    def test_capture_returns_json(self, client):
        resp = client.post("/api/capture")
        assert resp.status_code == 200
        assert resp.content_type == "application/json"

    def test_capture_has_image_key(self, client):
        resp = client.post("/api/capture")
        data = resp.get_json()
        assert "image" in data

    def test_capture_has_phase_key(self, client):
        resp = client.post("/api/capture")
        data = resp.get_json()
        assert data["phase"] == "CAPTURING"

    def test_capture_base64_decodes_to_jpeg(self, client):
        resp = client.post("/api/capture")
        data = resp.get_json()
        raw = base64.b64decode(data["image"])
        assert raw[:2] == b"\xff\xd8", "Decoded image must start with JPEG magic bytes"


# ---------------------------------------------------------------------------
# Video feed endpoint tests
# ---------------------------------------------------------------------------

class TestVideoFeedEndpoint:
    """GET /api/video_feed returns MJPEG multipart content type."""

    def test_video_feed_content_type(self, client):
        resp = client.get("/api/video_feed")
        assert "multipart/x-mixed-replace" in resp.content_type


# ---------------------------------------------------------------------------
# SocketIO button_press tests
# ---------------------------------------------------------------------------

class TestSocketIOButtonPress:
    """SocketIO button_press handler manages phase and locking."""

    def test_button_press_sets_capturing(self, socketio_client):
        socketio_client.emit("button_press")
        received = socketio_client.get_received()
        phases = [m["args"][0]["phase"] for m in received if m["name"] == "phase_change"]
        assert "CAPTURING" in phases

    def test_button_press_locks_button(self, socketio_client):
        socketio_client.emit("button_press")
        assert button.is_locked is True

    def test_double_press_rejected(self, socketio_client):
        socketio_client.emit("button_press")
        first = socketio_client.get_received()
        # Second press while locked
        socketio_client.emit("button_press")
        second = socketio_client.get_received()
        # Second press should NOT produce another phase_change
        phase_events = [m for m in second if m["name"] == "phase_change"]
        assert phase_events == [], "Double-press must be rejected when button is locked"

    def test_phase_change_on_connect(self):
        """Client receives current phase on connect."""
        app.config["TESTING"] = True
        client = socketio.test_client(app)
        received = client.get_received()
        phases = [m["args"][0]["phase"] for m in received if m["name"] == "phase_change"]
        assert "IDLE" in phases
        client.disconnect()
