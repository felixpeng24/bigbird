#!/usr/bin/env bash
# install-pi.sh — One-time Pi setup script
#
# Run this once after cloning the repo onto the Pi:
#   chmod +x install-pi.sh && ./install-pi.sh
#
# What it does:
#   1. Installs system dependencies (unclutter, chromium)
#   2. Installs Python dependencies
#   3. Installs the systemd service for auto-boot
#   4. Enables the service
#
# After running, reboot the Pi and the installation starts automatically.

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
# Systemd service
# -----------------------------------------------------------------------
echo "[SETUP] Installing systemd service..."
sudo cp bigbird.service /etc/systemd/system/bigbird.service

# Update paths in the service file to match actual install location
ACTUAL_USER=$(whoami)
sudo sed -i "s|User=pi|User=${ACTUAL_USER}|g" /etc/systemd/system/bigbird.service
sudo sed -i "s|/home/pi/bigbird|${SCRIPT_DIR}|g" /etc/systemd/system/bigbird.service
sudo sed -i "s|/home/pi/.Xauthority|/home/${ACTUAL_USER}/.Xauthority|g" /etc/systemd/system/bigbird.service

sudo systemctl daemon-reload
sudo systemctl enable bigbird.service

echo ""
echo "[SETUP] ✓ Installation complete!"
echo ""
echo "  To start now:   sudo systemctl start bigbird"
echo "  To check logs:  journalctl -u bigbird -f"
echo "  To auto-start:  Already enabled (starts on boot)"
echo ""
echo "  Make sure .env contains OPENAI_API_KEY before starting."
echo "  Reboot to verify auto-start works."
