"""Hardware abstraction layer for Big Bird installation.

Provides abstract interfaces for camera and button hardware, with concrete
implementations for both Raspberry Pi (real hardware) and Mac (mock).
The factory function `create_hardware()` auto-detects the platform.
"""

import abc
import base64
import io
import logging
import os
import threading
import time

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Pi-only imports — expected to fail on Mac
# ---------------------------------------------------------------------------
try:
    from picamera2 import Picamera2
    from picamera2.encoders import MJPEGEncoder
    from picamera2.outputs import FileOutput
    _HAS_PICAMERA = True
except ImportError:
    _HAS_PICAMERA = False

try:
    from gpiozero import Button as GPIOButton
    _HAS_GPIO = True
except ImportError:
    _HAS_GPIO = False


# ===========================================================================
# Abstract interfaces
# ===========================================================================

class AbstractCamera(abc.ABC):
    """Camera interface for capturing JPEG frames."""

    @abc.abstractmethod
    def capture_frame(self) -> bytes:
        """Capture and return a single JPEG-encoded frame."""

    @abc.abstractmethod
    def start_stream(self) -> None:
        """Start continuous frame capture for MJPEG streaming."""

    @abc.abstractmethod
    def stop_stream(self) -> None:
        """Stop continuous frame capture."""

    @abc.abstractmethod
    def get_frame(self) -> bytes:
        """Return the latest JPEG frame (blocks briefly if stream is running)."""


class AbstractButton(abc.ABC):
    """Button interface with press callback and lockout support."""

    @abc.abstractmethod
    def on_press(self, callback) -> None:
        """Register *callback* to be invoked on button press."""

    @abc.abstractmethod
    def lock(self) -> None:
        """Lock the button — presses are ignored until unlock()."""

    @abc.abstractmethod
    def unlock(self) -> None:
        """Unlock the button — presses fire the callback again."""

    @property
    @abc.abstractmethod
    def is_locked(self) -> bool:
        """Return True if the button is currently locked."""


# ===========================================================================
# Mock implementations (Mac / dev)
# ===========================================================================

class MockCamera(AbstractCamera):
    """Camera mock that serves a static JPEG test image."""

    def __init__(self) -> None:
        image_path = os.path.join(os.path.dirname(__file__), "test_image.jpg")
        with open(image_path, "rb") as f:
            self._image_bytes: bytes = f.read()
        if len(self._image_bytes) < 2 or self._image_bytes[:2] != b"\xff\xd8":
            raise RuntimeError(f"test_image.jpg is not a valid JPEG: {image_path}")
        self._streaming = False
        logger.info("[CAMERA] MockCamera initialised — %d byte test image", len(self._image_bytes))

    def capture_frame(self) -> bytes:
        logger.debug("[CAMERA] MockCamera capture_frame")
        return self._image_bytes

    def start_stream(self) -> None:
        self._streaming = True
        logger.info("[CAMERA] MockCamera stream started")

    def stop_stream(self) -> None:
        self._streaming = False
        logger.info("[CAMERA] MockCamera stream stopped")

    def get_frame(self) -> bytes:
        return self._image_bytes


class MockButton(AbstractButton):
    """Button mock with programmatic trigger() for testing."""

    def __init__(self) -> None:
        self._locked: bool = False
        self._callback = None
        logger.info("[BUTTON] MockButton initialised")

    def on_press(self, callback) -> None:
        self._callback = callback
        logger.debug("[BUTTON] MockButton callback registered")

    def lock(self) -> None:
        self._locked = True
        logger.info("[BUTTON] MockButton locked")

    def unlock(self) -> None:
        self._locked = False
        logger.info("[BUTTON] MockButton unlocked")

    @property
    def is_locked(self) -> bool:
        return self._locked

    def trigger(self) -> None:
        """Simulate a button press. Respects lock state."""
        if self._locked:
            logger.info("[BUTTON] locked — ignoring press")
            return
        logger.info("[BUTTON] press received")
        if self._callback is not None:
            self._callback()


# ===========================================================================
# Pi implementations
# ===========================================================================

class PiCamera(AbstractCamera):
    """Camera backed by picamera2 on Raspberry Pi."""

    class _StreamingOutput(io.BufferedIOBase):
        """Thread-safe frame buffer for MJPEG streaming."""

        def __init__(self) -> None:
            self.frame: bytes = b""
            self.condition = threading.Condition()

        def write(self, buf: bytes) -> int:
            with self.condition:
                self.frame = buf
                self.condition.notify_all()
            return len(buf)

    def __init__(self) -> None:
        if not _HAS_PICAMERA:
            raise ImportError("picamera2 is not available")
        self._picam = Picamera2()
        self._picam.configure(self._picam.create_video_configuration(
            main={"size": (640, 480)}
        ))
        self._output = self._StreamingOutput()
        self._streaming = False
        logger.info("[CAMERA] PiCamera initialised")

    def capture_frame(self) -> bytes:
        stream = io.BytesIO()
        self._picam.capture_file(stream, format="jpeg")
        data = stream.getvalue()
        logger.debug("[CAMERA] PiCamera captured frame: %d bytes", len(data))
        return data

    def start_stream(self) -> None:
        self._picam.start_recording(MJPEGEncoder(), FileOutput(self._output))
        self._streaming = True
        logger.info("[CAMERA] PiCamera stream started")

    def stop_stream(self) -> None:
        if self._streaming:
            self._picam.stop_recording()
            self._streaming = False
            logger.info("[CAMERA] PiCamera stream stopped")

    def get_frame(self) -> bytes:
        with self._output.condition:
            self._output.condition.wait()
            return self._output.frame


class PiButton(AbstractButton):
    """Button backed by gpiozero on Raspberry Pi (GPIO 17)."""

    def __init__(self) -> None:
        if not _HAS_GPIO:
            raise ImportError("gpiozero is not available")
        self._button = GPIOButton(17, bounce_time=0.3)
        self._locked: bool = False
        self._callback = None
        logger.info("[BUTTON] PiButton initialised on GPIO 17")

    def on_press(self, callback) -> None:
        self._callback = callback

        def _guarded_callback() -> None:
            if self._locked:
                logger.info("[BUTTON] locked — ignoring press")
                return
            logger.info("[BUTTON] press received")
            if self._callback is not None:
                self._callback()

        self._button.when_pressed = _guarded_callback
        logger.debug("[BUTTON] PiButton callback registered")

    def lock(self) -> None:
        self._locked = True
        logger.info("[BUTTON] PiButton locked")

    def unlock(self) -> None:
        self._locked = False
        logger.info("[BUTTON] PiButton unlocked")

    @property
    def is_locked(self) -> bool:
        return self._locked

    def trigger(self) -> None:
        """Software trigger for interface consistency. On Pi, hardware fires directly."""
        if self._locked:
            logger.info("[BUTTON] locked — ignoring press")
            return
        logger.info("[BUTTON] press received (software trigger)")
        if self._callback is not None:
            self._callback()


# ===========================================================================
# Factory
# ===========================================================================

def create_hardware() -> tuple[AbstractCamera, AbstractButton]:
    """Create camera and button instances, auto-detecting platform.

    Returns (MockCamera, MockButton) on Mac/dev, (PiCamera, PiButton) on Pi.
    """
    try:
        camera = PiCamera()
        button = PiButton()
        logger.info("[HARDWARE] Using Pi hardware (picamera2 + gpiozero)")
        return camera, button
    except (ImportError, RuntimeError) as exc:
        logger.info("[HARDWARE] Pi hardware unavailable (%s), using mock implementations", exc)
        camera = MockCamera()
        button = MockButton()
        return camera, button
