"""
Logging configuration for Text Helper IA
"""
import logging
import logging.handlers
import os
from typing import Dict, Any
from .config import Config


class Logger:
    """Logger configuration manager"""
    
    def __init__(self, config: Config):
        self.config = config
        self.logger = None
        self._setup_logging()
    
    def _setup_logging(self) -> None:
        """Setup logging configuration"""
        logging_config = self.config.get_logging_config()
        
        # Create logger
        self.logger = logging.getLogger('text_helper_ia')
        self.logger.setLevel(getattr(logging, logging_config['level']))
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # File handler with rotation
        log_file = logging_config['file']
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=logging_config['max_size'],
            backupCount=logging_config['backup_count']
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
    
    def get_logger(self) -> logging.Logger:
        """Get the configured logger"""
        return self.logger
    
    def info(self, message: str) -> None:
        """Log info message"""
        self.logger.info(message)
    
    def warning(self, message: str) -> None:
        """Log warning message"""
        self.logger.warning(message)
    
    def error(self, message: str) -> None:
        """Log error message"""
        self.logger.error(message)
    
    def debug(self, message: str) -> None:
        """Log debug message"""
        self.logger.debug(message)
