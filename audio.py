"""Server-side TTS using espeak-ng for Big Bird installation.

Speaks text through the default audio output (USB speaker).
Falls back silently on Mac/dev where espeak-ng isn't installed.
"""

import logging
import os
import shutil
import subprocess
import tempfile
import threading

logger = logging.getLogger(__name__)

_HAS_ESPEAK = shutil.which("espeak-ng") is not None


def play_test_sound() -> None:
    """Play the ALSA test sound to verify audio output works."""
    test_file = "/usr/share/sounds/alsa/Front_Center.wav"
    if os.path.exists(test_file):
        try:
            subprocess.run(["aplay", test_file], timeout=10)
            logger.info("[AUDIO] test sound played")
        except Exception as exc:
            logger.warning("[AUDIO] test sound failed: %s", exc)
    else:
        logger.warning("[AUDIO] test file not found: %s", test_file)


def speak(text: str) -> None:
    """Speak text asynchronously via espeak-ng. No-op if unavailable."""
    if not _HAS_ESPEAK:
        logger.debug("[AUDIO] espeak-ng not available, skipping: %s", text[:60])
        return
    threading.Thread(target=_speak_sync, args=(text,), daemon=True).start()


def speak_sync(text: str) -> None:
    """Speak text synchronously (blocks until done)."""
    if not _HAS_ESPEAK:
        logger.debug("[AUDIO] espeak-ng not available, skipping: %s", text[:60])
        return
    _speak_sync(text)


def _speak_sync(text: str) -> None:
    """Internal: generate WAV via espeak-ng to a temp file, then play with aplay."""
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_path = tmp.name
        # Generate WAV to temp file
        result = subprocess.run(
            ["espeak-ng", "-v", "en", "-s", "140", "-p", "30", "-w", tmp_path, text],
            timeout=10,
            capture_output=True,
        )
        if result.returncode != 0:
            logger.warning("[AUDIO] espeak-ng failed: %s", result.stderr.decode(errors="ignore")[:200])
            return
        # Play it
        subprocess.run(["aplay", "-q", tmp_path], timeout=15)
        logger.debug("[AUDIO] spoke: %s", text[:60])
    except subprocess.TimeoutExpired:
        logger.warning("[AUDIO] audio subprocess timed out")
    except Exception as exc:
        logger.warning("[AUDIO] audio failed: %s", exc)
    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except Exception:
                pass
