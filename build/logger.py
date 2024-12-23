import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Optional
from pathlib import Path

class BotLogger:
    _instance: Optional['BotLogger'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BotLogger, cls).__new__(cls)
            cls._instance._initialize_logger()
        return cls._instance
    
    def _initialize_logger(self):
        """Initialize the logger with both file and console handlers"""
        # Create logs directory if it doesn't exist
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        
        # Configure main logger
        self.logger = logging.getLogger('bot')
        self.logger.setLevel(logging.INFO)
        
        # Create formatters
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # File handler (with rotation)
        file_handler = RotatingFileHandler(
            log_dir / 'bot.log',
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(file_formatter)
        
        # Error file handler
        error_handler = RotatingFileHandler(
            log_dir / 'error.log',
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(file_formatter)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(console_formatter)
        
        # Add handlers to logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(error_handler)
        self.logger.addHandler(console_handler)
    
    @classmethod
    def get_logger(cls):
        """Get the logger instance"""
        if cls._instance is None:
            cls()
        return cls._instance.logger

# Create global logger instance
logger = BotLogger.get_logger()

def log_error(error: Exception, context: str = ""):
    """Log error with full traceback"""
    if context:
        logger.error(f"{context}: {str(error)}", exc_info=True)
    else:
        logger.error(str(error), exc_info=True)

def log_user_action(user_id: int, action: str, status: bool = True):
    """Log user actions"""
    status_str = "SUCCESS" if status else "FAILED"
    logger.info(f"User {user_id} - {action} - {status_str}")

def log_system_action(action: str, status: bool = True, details: str = ""):
    """Log system actions"""
    status_str = "SUCCESS" if status else "FAILED"
    if details:
        logger.info(f"System action: {action} - {status_str} - {details}")
    else:
        logger.info(f"System action: {action} - {status_str}") 