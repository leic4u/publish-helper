"""Logging utilities for the application."""

import logging
import sys
from pathlib import Path
from typing import Optional

from config.settings import config


class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for different log levels."""

    # Color codes
    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[35m",  # Magenta
        "RESET": "\033[0m",  # Reset
    }

    def format(self, record):
        """Format log record with colors."""
        log_color = self.COLORS.get(record.levelname, self.COLORS["RESET"])
        reset_color = self.COLORS["RESET"]

        # Format the message
        formatted = super().format(record)

        # Add colors to console output only
        if hasattr(record, "console_output"):
            return f"{log_color}{formatted}{reset_color}"
        return formatted


def setup_logger(
    name: str,
    level: Optional[str] = None,
    log_file: Optional[Path] = None,
    console_output: bool = True,
) -> logging.Logger:
    """
    Set up a logger with both file and console handlers.

    Args:
        name: Logger name
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file
        console_output: Whether to output to console

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    # Set log level
    log_level = getattr(logging, (level or config.LOG_LEVEL).upper(), logging.INFO)
    logger.setLevel(log_level)

    # Clear existing handlers
    logger.handlers.clear()

    # Create formatters
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
    )
    console_formatter = ColoredFormatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # File handler
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(log_level)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    # Console handler
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_handler.setFormatter(console_formatter)

        # Add custom attribute for colored output
        class ColoredStreamHandler(logging.StreamHandler):
            def emit(self, record):
                record.console_output = True
                super().emit(record)

        console_handler = ColoredStreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with default configuration."""
    return setup_logger(
        name=name, level=config.LOG_LEVEL, log_file=config.LOG_FILE, console_output=True
    )
