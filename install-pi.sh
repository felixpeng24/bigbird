#!/usr/bin/env bash
# install-pi.sh — One-time Pi setup script
#
# Run this once after cloning the repo onto the Pi:
#   chmod +x install-pi.sh && ./install-pi.sh
#
# What it does:
#   1. Installs system dependencies (unclutter, chromium)
#   2. Installs Python dependencies
#   3. Registers an XDG autostart entry so start.sh launches inside the
#      user's desktop session (where PipeWire/ALSA audio works).
#
# After running, reboot the Pi and the installation starts automatically
# once the desktop logs in.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "============================================"
echo " Big Bird — Pi Installation Setup"
echo "============================================"

# -----------------------------------------------------------------------
# System packages
# -----------------------------------------------------------------------
echo "[SETUP] Installing system packages..."
sudo apt-get update -qq
sudo apt-get install -y -qq \
    python3-pip \
    python3-venv \
    chromium \
    unclutter \
    libcamera-apps \
    python3-picamera2 \
    espeak-ng

# -----------------------------------------------------------------------
# Python dependencies
# -----------------------------------------------------------------------
echo "[SETUP] Installing Python dependencies..."
cd "$SCRIPT_DIR"
pip3 install --break-system-packages -r requirements.txt

# -----------------------------------------------------------------------
# Remove any previously-installed systemd service (older installs)
# -----------------------------------------------------------------------
if [ -f /etc/systemd/system/bigbird.service ]; then
    echo "[SETUP] Removing old systemd service..."
    sudo systemctl disable --now bigbird.service 2>/dev/null || true
    sudo rm -f /etc/systemd/system/bigbird.service
    sudo systemctl daemon-reload
fi

# -----------------------------------------------------------------------
# XDG autostart entry (runs inside the desktop session for working audio)
# -----------------------------------------------------------------------
echo "[SETUP] Installing XDG autostart entry..."
AUTOSTART_DIR="${HOME}/.config/autostart"
mkdir -p "$AUTOSTART_DIR"

chmod +x "${SCRIPT_DIR}/start.sh"
sed "s|__INSTALL_DIR__|${SCRIPT_DIR}|g" \
    "${SCRIPT_DIR}/bigbird.desktop" > "${AUTOSTART_DIR}/bigbird.desktop"
chmod +x "${AUTOSTART_DIR}/bigbird.desktop"

echo ""
echo "[SETUP] ✓ Installation complete!"
echo ""
echo "  Autostart entry: ${AUTOSTART_DIR}/bigbird.desktop"
echo "  To start now:    ./start.sh"
echo "  To view logs:    tail -f logs/server.log"
echo "  To disable:      rm ${AUTOSTART_DIR}/bigbird.desktop"
echo ""
echo "  Make sure .env contains OPENAI_API_KEY before starting."
echo "  Reboot to verify auto-start works — it fires once the desktop logs in."
