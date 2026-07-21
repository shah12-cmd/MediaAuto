#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$REPO_DIR/venv"
ENV_FILE="$REPO_DIR/.env"

echo "=== MediaAuto Installer ==="

# Update and install system packages
sudo apt update
sudo apt install -y python3 python3-venv python3-pip ffmpeg git nginx supervisor

# yt-dlp
python3 -m pip install --upgrade pip
python3 -m pip install yt-dlp

# Create virtualenv
if [ ! -d "$VENV_DIR" ]; then
  python3 -m venv "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"

pip install --upgrade pip
pip install -r requirements.txt

# Interactive configuration
read -p "Telegram bot token (leave empty if you will use user account instead): " TELEGRAM_BOT_TOKEN
read -p "Telegram API ID: " TELEGRAM_API_ID
read -p "Telegram API HASH: " TELEGRAM_API_HASH
read -p "Telegram phone number (for Telethon user login, e.g. +98912...): " TELEGRAM_PHONE

read -p "Do you want to login now and create Telethon session? (y/n): " LOGIN_NOW

# AI settings
read -p "OpenAI API Key (leave empty to skip AI features): " OPENAI_API_KEY

# Panel settings
read -p "Panel admin username: " PANEL_USER
read -sp "Panel admin password: " PANEL_PASS
echo

# Storage and download settings
read -p "Media storage directory (default: data/media): " MEDIA_DIR
MEDIA_DIR=${MEDIA_DIR:-data/media}

mkdir -p "$MEDIA_DIR"

# Write to .env
cat > "$ENV_FILE" <<EOF
TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN
TELEGRAM_API_ID=$TELEGRAM_API_ID
TELEGRAM_API_HASH=$TELEGRAM_API_HASH
TELEGRAM_PHONE=$TELEGRAM_PHONE
OPENAI_API_KEY=$OPENAI_API_KEY
MEDIA_DIR=$MEDIA_DIR
PANEL_ADMIN_USER=$PANEL_USER
PANEL_ADMIN_PASS=$PANEL_PASS
EOF

echo "Written configuration to $ENV_FILE"

# Optionally create telethon session via helper
if [[ "$LOGIN_NOW" =~ ^[Yy]$ ]]; then
  echo "Starting interactive Telethon login. Follow prompts."
  python3 "$REPO_DIR/scripts/create_session.py"
fi

# Setup systemd services
sudo cp "$REPO_DIR/system/mediaauto-bot.service" /etc/systemd/system/mediaauto-bot.service
sudo cp "$REPO_DIR/system/mediaauto-panel.service" /etc/systemd/system/mediaauto-panel.service
sudo systemctl daemon-reload
sudo systemctl enable --now mediaauto-bot.service
sudo systemctl enable --now mediaauto-panel.service

echo "Installation complete."
echo "Use: sudo journalctl -u mediaauto-bot -f  (or mediaauto-panel) to follow logs."