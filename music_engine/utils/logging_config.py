"""
Logging configuration for Music Theory Engine.

Provides centralized logging setup with file and console handlers.
"""

import logging
import sys
import os
from pathlib import Path


def setup_logging(level=logging.INFO, log_file='music_engine.log'):
    """
    Setup application-wide logging configuration.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file (relative to project root)
    """
    # Create logs directory if it doesn't exist
    log_path = Path(log_file)
    log_path.parent.mkdir(exist_ok=True)

    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(level)

    # Remove any existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(levelname)s - %(name)s - %(message)s'
    )

    # File handler
    try:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    except (OSError, IOError) as e:
        # If file logging fails, continue with console only
        print(f"Warning: Could not setup file logging: {e}")

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # Set specific loggers for external libraries to WARNING to reduce noise
    logging.getLogger('customtkinter').setLevel(logging.WARNING)
    logging.getLogger('PIL').setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name.

    Args:
        name: Logger name (usually __name__)

    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)


def log_function_call(logger: logging.Logger, level=logging.DEBUG):
    """
    Decorator to log function calls.

    Usage:
        @log_function_call(logger)
        def my_function(arg1, arg2):
            pass
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger.log(level, f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
            try:
                result = func(*args, **kwargs)
                logger.log(level, f"{func.__name__} completed successfully")
                return result
            except Exception as e:
                logger.error(f"{func.__name__} failed: {e}", exc_info=True)
                raise
        return wrapper
    return decorator


# Convenience functions for common logging patterns
def log_error_with_context(logger: logging.Logger, error: Exception, context: str = "", exc_info=True):
    """
    Log an error with additional context information.

    Args:
        logger: Logger instance
        error: The exception that occurred
        context: Additional context information
        exc_info: Whether to include exception traceback
    """
    message = f"{context}: {error}" if context else str(error)
    logger.error(message, exc_info=exc_info)


def log_user_friendly_error(logger: logging.Logger, user_message: str, technical_details: str = ""):
    """
    Log both user-friendly and technical error information.

    Args:
        logger: Logger instance
        user_message: Message safe to show to users
        technical_details: Technical details for developers
    """
    logger.warning(f"User error: {user_message}")
    if technical_details:
        logger.debug(f"Technical details: {technical_details}")