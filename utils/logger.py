"""
Utility module untuk logging configuration
Centralized logging setup untuk aplikasi
"""
import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logger(name: str, log_file: str = "koperasi.log", level=logging.INFO) -> logging.Logger:
    """
    Setup logger dengan configuration yang konsisten
    
    Args:
        name: Nama logger (biasanya __name__)
        log_file: Path ke file log
        level: Logging level (default: INFO)
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    # Format untuk log messages
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler dengan rotation (max 5MB, keep 3 backups)
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,  # 5MB
        backupCount=3,
        encoding='utf-8'
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Console handler untuk development
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)  # Only show warnings/errors in console
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger
