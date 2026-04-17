"""Server-side TTS using espeak-ng for Big Bird installation.

Speaks text through the default audio output (USB speaker).
Falls back silently on Mac/dev where espeak-ng isn't installed.
"""

import logging
import shutil
import subprocess
import threading

logger = logging.getLogger(__name__)

_HAS_ESPEAK = shutil.which("espeak-ng") is not None


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
    """Internal: run espeak-ng subprocess."""
    try:
        subprocess.run(
            ["espeak-ng", "-v", "en", "-s", "140", "-p", "30", text],
            capture_output=True,
            timeout=15,
        )
        logger.debug("[AUDIO] spoke: %s", text[:60])
    except subprocess.TimeoutExpired:
        logger.warning("[AUDIO] espeak-ng timed out")
    except Exception as exc:
        logger.warning("[AUDIO] espeak-ng failed: %s", exc)
