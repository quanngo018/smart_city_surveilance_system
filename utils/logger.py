"""
Logger Module for Smart City Monitoring System
Provides centralized logging functionality for debugging and error tracking.
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

# ============================================================================
# LOGGER CONFIGURATION
# ============================================================================

def setup_logger(
    name: str = "smart_city",
    log_level: int = logging.INFO,
    log_file: Optional[Path] = None
) -> logging.Logger:
    """
    Set up and configure logger for the application.
    
    Args:
        name: Logger name
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional path to log file
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    # Create formatter
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (if log_file specified)
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


# ============================================================================
# DEFAULT LOGGER INSTANCE
# ============================================================================

# Create default logger
logger = setup_logger()


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def log_info(message: str) -> None:
    """Log info message."""
    logger.info(message)


def log_warning(message: str) -> None:
    """Log warning message."""
    logger.warning(message)


def log_error(message: str, exc_info: bool = False) -> None:
    """
    Log error message.
    
    Args:
        message: Error message
        exc_info: Include exception information
    """
    logger.error(message, exc_info=exc_info)


def log_debug(message: str) -> None:
    """Log debug message."""
    logger.debug(message)


def log_critical(message: str, exc_info: bool = True) -> None:
    """
    Log critical message.
    
    Args:
        message: Critical message
        exc_info: Include exception information
    """
    logger.critical(message, exc_info=exc_info)


# ============================================================================
# CONTEXT MANAGERS
# ============================================================================

class LogOperation:
    """Context manager for logging operation start and end."""
    
    def __init__(self, operation_name: str):
        self.operation_name = operation_name
        self.start_time = None
    
    def __enter__(self):
        self.start_time = datetime.now()
        log_info(f"Starting operation: {self.operation_name}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = (datetime.now() - self.start_time).total_seconds()
        
        if exc_type is not None:
            log_error(
                f"Operation failed: {self.operation_name} "
                f"(duration: {duration:.2f}s) - {exc_val}",
                exc_info=True
            )
            return False
        
        log_info(
            f"Completed operation: {self.operation_name} "
            f"(duration: {duration:.2f}s)"
        )
        return True
