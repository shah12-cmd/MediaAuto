"""Proper logger setup for MediaAuto"""

import logging
import logging.handlers
from pathlib import Path
from datetime import datetime

LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


def get_logger(name: str = "mediauto", level: str = "INFO", log_dir: str = "logs"):
    """Get or create logger with file and console handlers"""
    
    # Create log directory
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True, parents=True)
    
    # Get logger
    logger = logging.getLogger(name)
    
    # Only add handlers if this logger doesn't already have them
    if not logger.handlers:
        logger.setLevel(LOG_LEVELS.get(level, logging.INFO))
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(LOG_LEVELS.get(level, logging.INFO))
        
        # File handler with rotation
        log_file = log_path / f"mediauto_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10485760,  # 10MB
            backupCount=10
        )
        file_handler.setLevel(LOG_LEVELS.get(level, logging.INFO))
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        
        # Add handlers
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
    
    return logger
