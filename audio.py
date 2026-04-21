"""Server-side TTS using espeak-ng for Big Bird installation.

Speaks text through the default audio output (USB speaker).
Falls back silently on Mac/dev where espeak-ng isn't installed.
"""

import logging
import os
import shutil
import struct
import subprocess
import tempfile
import threading
import wave

logger = logging.getLogger(__name__)

_HAS_ESPEAK = shutil.which("espeak-ng") is not None
_keep_alive_started = False


def _make_keep_alive_wav(path: str, duration_sec: float = 2.0, sample_rate: int = 44100) -> None:
    """Generate a WAV file with a near-silent low-amplitude sine wave."""
    import math
    n_frames = int(sample_rate * duration_sec)
    with wave.open(path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(sample_rate)
        # Very low amplitude sine at 50 Hz — inaudible but keeps speaker awake
        frames = bytearray()
        for i in range(n_frames):
            # Amplitude ~5 (out of 32767), effectively silent to human ear
            sample = int(5 * math.sin(2 * math.pi * 50 * i / sample_rate))
            frames += struct.pack("<h", sample)
        wf.writeframes(bytes(frames))


def start_speaker_keep_alive() -> None:
    """Play a near-silent tone in the background to prevent USB speaker auto-sleep."""
    global _keep_alive_started
    if _keep_alive_started:
        return
    _keep_alive_started = True

    # Generate the keep-alive WAV once
    keep_alive_path = os.path.join(tempfile.gettempdir(), "bigbird_keepalive.wav")
    try:
        _make_keep_alive_wav(keep_alive_path)
    except Exception as exc:
        logger.warning("[AUDIO] failed to generate keep-alive WAV: %s", exc)
        return

    def _loop():
        while True:
            try:
                subprocess.run(["aplay", "-q", keep_alive_path], timeout=5)
            except Exception as exc:
                logger.debug("[AUDIO] keep-alive tick failed: %s", exc)

    threading.Thread(target=_loop, daemon=True).start()
    logger.info("[AUDIO] speaker keep-alive started")


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
