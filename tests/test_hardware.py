"""Tests for the hardware abstraction layer."""

import pytest

from hardware import (
    AbstractButton,
    AbstractCamera,
    MockButton,
    MockCamera,
    create_hardware,
)


# ---------------------------------------------------------------------------
# MockCamera tests
# ---------------------------------------------------------------------------

class TestMockCamera:
    """MockCamera serves a valid JPEG test image."""

    def test_capture_frame_returns_jpeg(self):
        cam = MockCamera()
        data = cam.capture_frame()
        assert isinstance(data, bytes)
        assert data[:2] == b"\xff\xd8", "capture_frame must return JPEG bytes"

    def test_capture_frame_nonzero_size(self):
        cam = MockCamera()
        data = cam.capture_frame()
        assert len(data) > 100, f"JPEG too small ({len(data)} bytes)"

    def test_get_frame_returns_jpeg(self):
        cam = MockCamera()
        data = cam.get_frame()
        assert isinstance(data, bytes)
        assert data[:2] == b"\xff\xd8"

    def test_capture_and_get_frame_consistent(self):
        cam = MockCamera()
        assert cam.capture_frame() == cam.get_frame()

    def test_start_stop_stream_no_raise(self):
        cam = MockCamera()
        cam.start_stream()
        cam.stop_stream()

    def test_get_frame_works_during_stream(self):
        cam = MockCamera()
        cam.start_stream()
        data = cam.get_frame()
        assert data[:2] == b"\xff\xd8"
        cam.stop_stream()


# ---------------------------------------------------------------------------
# MockButton tests
# ---------------------------------------------------------------------------

class TestMockButton:
    """MockButton lock/unlock and trigger behaviour."""

    def test_initial_state_unlocked(self):
        btn = MockButton()
        assert btn.is_locked is False

    def test_lock(self):
        btn = MockButton()
        btn.lock()
        assert btn.is_locked is True

    def test_unlock(self):
        btn = MockButton()
        btn.lock()
        btn.unlock()
        assert btn.is_locked is False

    def test_on_press_and_trigger(self):
        btn = MockButton()
        called = []
        btn.on_press(lambda: called.append(True))
        btn.trigger()
        assert called == [True], "Callback should fire on trigger"

    def test_trigger_while_locked_ignores(self):
        btn = MockButton()
        called = []
        btn.on_press(lambda: called.append(True))
        btn.lock()
        btn.trigger()
        assert called == [], "Callback must NOT fire when locked"

    def test_trigger_without_callback_no_error(self):
        btn = MockButton()
        btn.trigger()  # should not raise

    def test_lock_unlock_cycle(self):
        btn = MockButton()
        called = []
        btn.on_press(lambda: called.append(True))
        btn.lock()
        btn.trigger()
        assert called == []
        btn.unlock()
        btn.trigger()
        assert called == [True]


# ---------------------------------------------------------------------------
# Factory tests
# ---------------------------------------------------------------------------

class TestCreateHardware:
    """create_hardware() returns the right types on Mac."""

    def test_returns_tuple(self):
        result = create_hardware()
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_returns_abstract_types(self):
        cam, btn = create_hardware()
        assert isinstance(cam, AbstractCamera)
        assert isinstance(btn, AbstractButton)

    def test_returns_mock_on_mac(self):
        cam, btn = create_hardware()
        assert type(cam).__name__ == "MockCamera"
        assert type(btn).__name__ == "MockButton"

    def test_camera_works_after_factory(self):
        cam, _ = create_hardware()
        data = cam.capture_frame()
        assert data[:2] == b"\xff\xd8"
        assert len(data) > 100
