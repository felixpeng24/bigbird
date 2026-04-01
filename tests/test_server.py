"""Tests for the Flask server endpoints and phase management."""

import base64
import json
from unittest.mock import patch, MagicMock

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
    # Reset the OpenAI client to None so tests don't leak state
    server_module._openai_client = None
    yield
    server_module.current_phase = Phase.IDLE
    button.unlock()
    server_module._openai_client = None


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
# Analyze endpoint tests
# ---------------------------------------------------------------------------

class TestAnalyzeEndpoint:
    """POST /api/analyze handles vision API calls and fallbacks."""

    def test_analyze_missing_image_returns_400(self, client):
        resp = client.post("/api/analyze", json={})
        assert resp.status_code == 400
        data = resp.get_json()
        assert "error" in data

    def test_analyze_no_body_returns_400(self, client):
        resp = client.post("/api/analyze")
        assert resp.status_code == 400

    def test_analyze_returns_fallback_without_api_key(self, client):
        """Without OPENAI_API_KEY, should return refusal fallback."""
        with patch.dict("os.environ", {}, clear=False):
            # Ensure no API key
            import os
            old = os.environ.pop("OPENAI_API_KEY", None)
            server_module._openai_client = None
            try:
                resp = client.post("/api/analyze", json={"image": "fakebase64data"})
                assert resp.status_code == 200
                data = resp.get_json()
                assert data.get("refused") is True
                assert "DEFIES" in data.get("message", "")
            finally:
                if old:
                    os.environ["OPENAI_API_KEY"] = old

    def test_analyze_returns_demographics_on_success(self, client):
        """With a mocked OpenAI client, should parse demographics."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = json.dumps({
            "race": "White",
            "gender": "Male",
            "age": "Mid-20s",
            "religion": "Unknown",
            "socioeconomic_status": "Middle class",
            "education": "College-educated",
        })
        mock_client.chat.completions.create.return_value = mock_response
        server_module._openai_client = mock_client

        resp = client.post("/api/analyze", json={"image": "fakebase64data"})
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["race"] == "White"
        assert data["gender"] == "Male"
        assert not data.get("refused")

    def test_analyze_returns_fallback_on_api_error(self, client):
        """If the API call throws, should return fallback."""
        mock_client = MagicMock()
        mock_client.chat.completions.create.side_effect = Exception("Network timeout")
        server_module._openai_client = mock_client

        resp = client.post("/api/analyze", json={"image": "fakebase64data"})
        assert resp.status_code == 200
        data = resp.get_json()
        assert data.get("refused") is True

    def test_analyze_returns_fallback_on_refusal(self, client):
        """If the API refuses, should return fallback."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "I'm sorry, I cannot classify people by demographics."
        mock_client.chat.completions.create.return_value = mock_response
        server_module._openai_client = mock_client

        resp = client.post("/api/analyze", json={"image": "fakebase64data"})
        assert resp.status_code == 200
        data = resp.get_json()
        assert data.get("refused") is True
        assert "DEFIES" in data.get("message", "")


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


# ---------------------------------------------------------------------------
# Phase loop tests
# ---------------------------------------------------------------------------

class TestPhaseLoop:
    """Evaluation loop transitions through all phases and resets."""

    def test_set_phase_with_data(self):
        """_set_phase can carry a data payload."""
        server_module._set_phase(Phase.REVEALING, data={"score": "42"})
        assert server_module.current_phase == Phase.REVEALING

    def test_evaluation_loop_resets_to_idle(self):
        """After the evaluation loop, phase should be IDLE and button unlocked.

        We mock the OpenAI client and use short sleeps in a patched loop.
        """
        # Mock the API to return quickly
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = json.dumps({
            "race": "Test", "gender": "Test", "age": "Test",
            "religion": "Test", "socioeconomic_status": "Test", "education": "Test",
        })
        mock_client.chat.completions.create.return_value = mock_response
        server_module._openai_client = mock_client

        # Patch time.sleep to make the loop fast
        with patch("server.time.sleep", return_value=None):
            server_module._run_evaluation_loop()

        assert server_module.current_phase == Phase.IDLE
        assert button.is_locked is False

    def test_evaluation_loop_handles_api_failure(self):
        """Loop should still complete and reset even if API fails."""
        mock_client = MagicMock()
        mock_client.chat.completions.create.side_effect = Exception("API down")
        server_module._openai_client = mock_client

        with patch("server.time.sleep", return_value=None):
            server_module._run_evaluation_loop()

        assert server_module.current_phase == Phase.IDLE
        assert button.is_locked is False
