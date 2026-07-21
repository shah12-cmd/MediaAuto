#!/usr/bin/env bash
set -euo pipefail

# MediaAuto installer - installs into /opt/mediaauto by default and sets up systemd services

REPO_CWD="$(cd "$(dirname "$0")" && pwd)"
DEFAULT_INSTALL_DIR="/opt/mediaauto"

if [ "$EUID" -ne 0 ]; then
  echo "This installer must be run as root (or via sudo)." >&2
  exit 1
fi

read -p "Install directory [${DEFAULT_INSTALL_DIR}]: " INSTALL_DIR
INSTALL_DIR=${INSTALL_DIR:-$DEFAULT_INSTALL_DIR}

echo "Installing MediaAuto into: $INSTALL_DIR"

# Create mediaauto system user
if ! id -u mediaauto >/dev/null 2>&1; then
  useradd --system --create-home --home-dir $INSTALL_DIR --shell /usr/sbin/nologin mediaauto || true
  echo "Created system user 'mediaauto'"
fi

# Stop services if running
systemctl stop mediaauto-bot.service mediaauto-panel.service >/dev/null 2>&1 || true

# Rsync files to install dir
mkdir -p "$INSTALL_DIR"
rsync -a --delete --exclude ".git" --exclude "venv" "$REPO_CWD/" "$INSTALL_DIR/"
chown -R mediaauto:mediaauto "$INSTALL_DIR"

# Create Python venv
if [ ! -d "$INSTALL_DIR/venv" ]; then
  python3 -m venv "$INSTALL_DIR/venv"
fi

# Install system packages
apt update
apt install -y python3-venv python3-pip ffmpeg git nginx

# Ensure pip up-to-date and install requirements into venv
"$INSTALL_DIR/venv/bin/pip" install --upgrade pip
"$INSTALL_DIR/venv/bin/pip" install -r "$INSTALL_DIR/requirements.txt"

# Make sure scripts are executable
chmod +x "$INSTALL_DIR/scripts/create_session.py"
chmod +x "$INSTALL_DIR/install.sh"

# Interactive configuration - prompt and write to .env in install dir (owned by mediaauto)
ENV_FILE="$INSTALL_DIR/.env"

read -p "Telegram bot token (leave empty if using user account): " TELEGRAM_BOT_TOKEN
read -p "Telegram API ID: " TELEGRAM_API_ID
read -p "Telegram API HASH: " TELEGRAM_API_HASH
read -p "Telegram phone number (for Telethon user login, e.g. +98912...): " TELEGRAM_PHONE
read -p "OpenAI API Key (leave empty to skip AI features): " OPENAI_API_KEY
read -p "Panel admin username (default: admin): " PANEL_USER
PANEL_USER=${PANEL_USER:-admin}
read -sp "Panel admin password (will be stored hashed): " PANEL_PASS
echo
read -p "Media storage directory under install dir (default: data/media): " MEDIA_DIR_INPUT
MEDIA_DIR_INPUT=${MEDIA_DIR_INPUT:-data/media}
MEDIA_DIR="$INSTALL_DIR/$MEDIA_DIR_INPUT"

mkdir -p "$MEDIA_DIR"
chown -R mediaauto:mediaauto "$INSTALL_DIR"

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

chown mediaauto:mediaauto "$ENV_FILE"
chmod 600 "$ENV_FILE"

# Create systemd service files with correct paths
BOT_SERVICE="/etc/systemd/system/mediaauto-bot.service"
PANEL_SERVICE="/etc/systemd/system/mediaauto-panel.service"

cat > "$BOT_SERVICE" <<EOF
[Unit]
Description=MediaAuto Bot Service
After=network.target

[Service]
Type=simple
User=mediaauto
WorkingDirectory=$INSTALL_DIR
ExecStart=$INSTALL_DIR/venv/bin/python $INSTALL_DIR/src/worker_launcher.py
Restart=always
RestartSec=5
Environment=PYTHONPATH=$INSTALL_DIR

[Install]
WantedBy=multi-user.target
EOF

cat > "$PANEL_SERVICE" <<EOF
[Unit]
Description=MediaAuto Panel (FastAPI)
After=network.target

[Service]
Type=simple
User=mediaauto
WorkingDirectory=$INSTALL_DIR
ExecStart=$INSTALL_DIR/venv/bin/uvicorn src.panel:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=5
Environment=PYTHONPATH=$INSTALL_DIR

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable --now mediaauto-bot.service mediaauto-panel.service || true

echo "Installation complete."
echo "Install dir: $INSTALL_DIR"
echo "To follow logs: sudo journalctl -u mediaauto-bot -f"