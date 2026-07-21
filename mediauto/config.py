"""Configuration management for MediaAuto"""

import os
import json
from pathlib import Path
from typing import Any, Dict, Optional
from dataclasses import dataclass, asdict
import logging

logger = logging.getLogger(__name__)


@dataclass
class BotConfig:
    """Bot configuration dataclass"""
    telegram_token: str = ""
    api_id: int = 0
    api_hash: str = ""
    phone_number: str = ""
    admin_password: str = ""
    
    source_channels: list = None
    destination_channel: int = 0
    
    send_delay: int = 600  # seconds
    ai_enabled: bool = False
    ai_provider: str = "openai"  # openai, anthropic, google
    ai_api_key: str = ""
    
    save_files: bool = True
    files_directory: str = "./data/media"
    
    watermark_enabled: bool = False
    watermark_text: str = ""
    watermark_image: str = ""
    
    ad_text: str = ""
    remove_channel_links: bool = True
    remove_channel_ids: bool = True
    remove_ads: bool = True
    remove_extra_hashtags: bool = True
    
    database_type: str = "sqlite"  # sqlite or postgresql
    database_url: str = ""
    
    backup_enabled: bool = True
    backup_interval: int = 3600  # seconds
    
    log_level: str = "INFO"
    
    def __post_init__(self):
        if self.source_channels is None:
            self.source_channels = []


class ConfigManager:
    """Manages bot configuration"""
    
    def __init__(self, config_path: str = "config.json"):
        self.config_path = Path(config_path)
        self.config = BotConfig()
        self.load_config()
    
    def load_config(self) -> None:
        """Load configuration from file"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for key, value in data.items():
                        if hasattr(self.config, key):
                            setattr(self.config, key, value)
                logger.info(f"Configuration loaded from {self.config_path}")
            except Exception as e:
                logger.error(f"Error loading configuration: {e}")
        else:
            logger.info("No configuration file found, using defaults")
    
    def save_config(self) -> None:
        """Save configuration to file"""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(asdict(self.config), f, indent=4, ensure_ascii=False)
            logger.info(f"Configuration saved to {self.config_path}")
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
    
    def update_config(self, **kwargs) -> None:
        """Update configuration values"""
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
        self.save_config()
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return getattr(self.config, key, default)
    
    def validate_config(self) -> tuple[bool, list[str]]:
        """Validate configuration"""
        errors = []
        
        if not self.config.telegram_token:
            errors.append("Telegram token not configured")
        if not self.config.api_id or not self.config.api_hash:
            errors.append("Telegram API credentials not configured")
        if not self.config.phone_number:
            errors.append("Phone number not configured")
        if not self.config.admin_password:
            errors.append("Admin password not configured")
        if not self.config.source_channels:
            errors.append("No source channels configured")
        if not self.config.destination_channel:
            errors.append("Destination channel not configured")
        
        return len(errors) == 0, errors


# Global configuration manager
config_manager = ConfigManager()
