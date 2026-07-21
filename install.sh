#!/bin/bash

# MediaAuto Installation Script
# Professional Telegram Media Automation Bot

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration file
CONFIG_FILE="config.json"
SYSTEMD_SERVICE="/etc/systemd/system/mediauto.service"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}   MediaAuto Installation Script${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Check if running as root for systemd setup
if [[ $EUID -ne 0 ]]; then
   echo -e "${YELLOW}⚠️  Not running as root. Systemd service won't be installed.${NC}"
   SKIP_SYSTEMD=true
fi

# Update system
echo -e "${BLUE}📦 Updating system packages...${NC}"
sudo apt-get update
sudo apt-get install -y python3.11 python3-pip python3-venv git ffmpeg

# Create virtual environment
echo -e "${BLUE}🐍 Creating Python virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo -e "${BLUE}📚 Installing Python dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
echo -e "${BLUE}📁 Creating directories...${NC}"
mkdir -p data/media logs backups mediauto_sessions

# Check if config exists
if [ -f "$CONFIG_FILE" ]; then
    echo -e "${YELLOW}⚠️  Configuration file already exists at $CONFIG_FILE${NC}"
    read -p "Do you want to reconfigure? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        SKIP_CONFIG=true
    fi
fi

# Configuration setup
if [ "$SKIP_CONFIG" != "true" ]; then
    echo -e "${BLUE}\n⚙️  Configuration Setup${NC}"
    echo -e "${BLUE}=====================================${NC}\n"
    
    # Telegram Token
    read -p "🤖 Enter Telegram Bot Token: " TELEGRAM_TOKEN
    while [ -z "$TELEGRAM_TOKEN" ]; do
        echo -e "${RED}❌ Token cannot be empty${NC}"
        read -p "🤖 Enter Telegram Bot Token: " TELEGRAM_TOKEN
    done
    
    # API ID and Hash
    read -p "🔑 Enter Telegram API ID: " API_ID
    while [ -z "$API_ID" ]; then
        echo -e "${RED}❌ API ID cannot be empty${NC}"
        read -p "🔑 Enter Telegram API ID: " API_ID
    done
    
    read -p "🔑 Enter Telegram API Hash: " API_HASH
    while [ -z "$API_HASH" ]; do
        echo -e "${RED}❌ API Hash cannot be empty${NC}"
        read -p "🔑 Enter Telegram API Hash: " API_HASH
    done
    
    # Phone number
    read -p "📱 Enter your Telegram phone number (with country code): " PHONE_NUMBER
    while [ -z "$PHONE_NUMBER" ]; do
        echo -e "${RED}❌ Phone number cannot be empty${NC}"
        read -p "📱 Enter your Telegram phone number: " PHONE_NUMBER
    done
    
    # Admin password
    read -sp "🔐 Enter admin password for bot: " ADMIN_PASSWORD
    echo
    while [ -z "$ADMIN_PASSWORD" ]; then
        echo -e "${RED}❌ Password cannot be empty${NC}"
        read -sp "🔐 Enter admin password for bot: " ADMIN_PASSWORD
        echo
    done
    
    # Source channels
    echo -e "\n📥 Source Channels Setup"
    CHANNELS="[]"
    read -p "Do you want to add source channels now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        CHANNELS='['
        first=true
        while true; do
            read -p "Enter channel ID/username (or press Enter to skip): " CHANNEL
            if [ -z "$CHANNEL" ]; then
                break
            fi
            if [ "$first" = false ]; then
                CHANNELS="${CHANNELS},"
            fi
            CHANNELS="${CHANNELS}\"${CHANNEL}\""
            first=false
        done
        CHANNELS="${CHANNELS}]"
    fi
    
    # Destination channel
    read -p "📤 Enter destination channel ID/username: " DESTINATION_CHANNEL
    while [ -z "$DESTINATION_CHANNEL" ]; do
        echo -e "${RED}❌ Destination channel cannot be empty${NC}"
        read -p "📤 Enter destination channel ID/username: " DESTINATION_CHANNEL
    done
    
    # Send delay
    echo -e "\n⏰ Send Delay Setup"
    echo "1) 5 minutes (300 seconds)"
    echo "2) 10 minutes (600 seconds)"
    echo "3) 30 minutes (1800 seconds)"
    echo "4) 1 hour (3600 seconds)"
    read -p "Select delay option (1-4): " DELAY_OPTION
    case $DELAY_OPTION in
        1) SEND_DELAY=300 ;;
        2) SEND_DELAY=600 ;;
        3) SEND_DELAY=1800 ;;
        4) SEND_DELAY=3600 ;;
        *) SEND_DELAY=600 ;;
    esac
    
    # Advertisement text
    read -p "📝 Enter advertisement text (optional, press Enter to skip): " AD_TEXT
    
    # AI Settings
    read -p "🤖 Do you want to enable AI features? (y/n) " -n 1 -r
    echo
    AI_ENABLED=false
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        AI_ENABLED=true
        read -p "Enter AI provider (openai/anthropic/google): " AI_PROVIDER
        read -sp "Enter AI API Key: " AI_API_KEY
        echo
    fi
    
    # Watermark Settings
    read -p "🖼 Do you want to enable watermark? (y/n) " -n 1 -r
    echo
    WATERMARK_ENABLED=false
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        WATERMARK_ENABLED=true
        read -p "Enter watermark text: " WATERMARK_TEXT
    fi
    
    # Database selection
    echo -e "\n💾 Database Setup"
    echo "1) SQLite (default, no setup needed)"
    echo "2) PostgreSQL"
    read -p "Select database type (1-2): " DB_OPTION
    case $DB_OPTION in
        2)
            DB_TYPE="postgresql"
            read -p "PostgreSQL connection URL: " DATABASE_URL
            ;;
        *)
            DB_TYPE="sqlite"
            DATABASE_URL="sqlite:///./data/mediauto.db"
            ;;
    esac
    
    # Create config JSON
    echo -e "\n${BLUE}📝 Creating configuration file...${NC}"
    
    cat > "$CONFIG_FILE" << EOF
{
    "telegram_token": "$TELEGRAM_TOKEN",
    "api_id": $API_ID,
    "api_hash": "$API_HASH",
    "phone_number": "$PHONE_NUMBER",
    "admin_password": "$ADMIN_PASSWORD",
    "source_channels": $CHANNELS,
    "destination_channel": "$DESTINATION_CHANNEL",
    "send_delay": $SEND_DELAY,
    "ad_text": "$AD_TEXT",
    "ai_enabled": $AI_ENABLED,
    "ai_provider": "${AI_PROVIDER:-openai}",
    "ai_api_key": "${AI_API_KEY:-}",
    "watermark_enabled": $WATERMARK_ENABLED,
    "watermark_text": "${WATERMARK_TEXT:-}",
    "database_type": "$DB_TYPE",
    "database_url": "$DATABASE_URL",
    "log_level": "INFO",
    "remove_channel_links": true,
    "remove_channel_ids": true,
    "remove_ads": true,
    "remove_extra_hashtags": true,
    "save_files": true,
    "files_directory": "./data/media",
    "backup_enabled": true,
    "backup_interval": 3600
}
EOF
    
    echo -e "${GREEN}✅ Configuration saved to $CONFIG_FILE${NC}"
fi

# Create systemd service
if [ "$SKIP_SYSTEMD" != "true" ]; then
    echo -e "\n${BLUE}🔧 Setting up systemd service...${NC}"
    
    INSTALL_DIR=$(pwd)
    
    sudo tee "$SYSTEMD_SERVICE" > /dev/null << EOF
[Unit]
Description=MediaAuto Telegram Bot
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$INSTALL_DIR
Environment="PATH=$INSTALL_DIR/venv/bin"
ExecStart=$INSTALL_DIR/venv/bin/python -m mediauto.main
Restart=always
RestartSec=10
StartLimitInterval=200
StartLimitBurst=5

[Install]
WantedBy=multi-user.target
EOF
    
    sudo systemctl daemon-reload
    sudo systemctl enable mediauto
    
    echo -e "${GREEN}✅ Systemd service installed${NC}"
    echo -e "${BLUE}To start the bot, run: sudo systemctl start mediauto${NC}"
    echo -e "${BLUE}To view logs, run: sudo systemctl status mediauto${NC}"
else
    echo -e "${YELLOW}⚠️  Systemd service not installed (requires root)${NC}"
fi

# Create run script
echo -e "\n${BLUE}📝 Creating run script...${NC}"
cat > "run.sh" << 'EOF'
#!/bin/bash
source venv/bin/activate
python -m mediauto.main
EOF
chmod +x run.sh

echo -e "${GREEN}\n========================================${NC}"
echo -e "${GREEN}✅ Installation Complete!${NC}"
echo -e "${GREEN}========================================\n${NC}"

echo -e "${BLUE}Next Steps:${NC}"
echo -e "${BLUE}1. Start the bot:${NC}"
if [ "$SKIP_SYSTEMD" != "true" ]; then
    echo -e "   ${YELLOW}sudo systemctl start mediauto${NC}"
else
    echo -e "   ${YELLOW}./run.sh${NC}"
fi
echo
echo -e "${BLUE}2. Check configuration:${NC}"
echo -e "   ${YELLOW}cat config.json${NC}"
echo
echo -e "${BLUE}3. View logs:${NC}"
if [ "$SKIP_SYSTEMD" != "true" ]; then
    echo -e "   ${YELLOW}sudo systemctl status mediauto${NC}"
    echo -e "   ${YELLOW}sudo journalctl -u mediauto -f${NC}"
else
    echo -e "   ${YELLOW}tail -f logs/mediauto_*.log${NC}"
fi
echo
echo -e "${GREEN}🎉 Ready to use!${NC}\n"
