#!/usr/bin/env python3
"""
Logging module for CS:GO Legacy server setup scripts
Provides colored console output and file logging
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


class ColoredFormatter(logging.Formatter):
    """Custom formatter with color support for console output"""
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'        # Reset
    }
    
    def format(self, record):
        # Add color to levelname
        if sys.platform != 'win32' or 'ANSICON' in sys.environ:
            levelname = record.levelname
            if levelname in self.COLORS:
                record.levelname = f"{self.COLORS[levelname]}{levelname}{self.COLORS['RESET']}"
        return super().format(record)


class SetupLogger:
    """Logger for the CS:GO server setup process"""
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Create timestamped log file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = self.log_dir / f"setup_{timestamp}.log"
        
        # Setup logger
        self.logger = logging.getLogger("CSGOSetup")
        self.logger.setLevel(logging.DEBUG)
        
        # Remove existing handlers
        self.logger.handlers.clear()
        
        # Console handler with colors
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_format = ColoredFormatter(
            '%(levelname)-8s | %(message)s'
        )
        console_handler.setFormatter(console_format)
        
        # File handler without colors
        file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_format)
        
        # Add handlers
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
    
    def debug(self, msg: str):
        """Log debug message"""
        self.logger.debug(msg)
    
    def info(self, msg: str):
        """Log info message"""
        self.logger.info(msg)
    
    def success(self, msg: str):
        """Log success message (INFO level with ✓ prefix)"""
        self.logger.info(f"✓ {msg}")
    
    def warning(self, msg: str):
        """Log warning message"""
        self.logger.warning(msg)
    
    def error(self, msg: str):
        """Log error message"""
        self.logger.error(msg)
    
    def critical(self, msg: str):
        """Log critical message"""
        self.logger.critical(msg)
    
    def section(self, title: str):
        """Log a section header"""
        separator = "=" * 60
        self.logger.info(separator)
        self.logger.info(f"  {title}")
        self.logger.info(separator)


# Global logger instance
_logger_instance: Optional[SetupLogger] = None


def get_logger() -> SetupLogger:
    """Get or create the global logger instance"""
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = SetupLogger()
    return _logger_instance

