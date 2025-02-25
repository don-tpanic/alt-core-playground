"""Logging configuration for alt-core."""

import logging
import os
import sys


def get_logger(name: str, level: str | None = None) -> logging.Logger:
    """Get a logger with the given name.

    Args:
        name: The name of the logger.
        level: Optional logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
              Defaults to INFO if not specified.

    Returns:
        The logger.
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        # Create console handler
        handler = logging.StreamHandler(sys.stdout)

        # Create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(name)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Set up handler
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # Set level from environment variable or parameter, default to INFO
        log_level = str(level or os.getenv("LOG_LEVEL", "INFO")).upper()
        logger.setLevel(getattr(logging, log_level))

        # Prevent propagation to root logger
        logger.propagate = False

    return logger
