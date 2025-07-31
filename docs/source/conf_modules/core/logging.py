"""Logging configuration for Sphinx builds.

This module sets up logging for debugging Sphinx builds including:
- File and console logging
- Log formatting
- Debug helpers
"""

import logging
from pathlib import Path
from typing import Any


def get_config(
    log_level: str = "INFO",
    log_file: str | None = "sphinx_debug.log",
    console_output: bool = True,
) -> dict[str, Any]:
    """Configure logging for Sphinx.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Log file name (relative to source dir). None to disable.
        console_output: Whether to also log to console

    Returns:
        Dictionary with logging configuration
    """
    config = {}

    # Get source directory (where conf.py is)
    conf_dir = Path(__file__).parent.parent.parent

    # Set up handlers
    handlers = []

    # File handler
    if log_file:
        log_path = conf_dir / log_file
        file_handler = logging.FileHandler(str(log_path))
        file_handler.setLevel(getattr(logging, log_level))
        handlers.append(file_handler)

    # Console handler
    if console_output:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, log_level))
        handlers.append(console_handler)

    # Configure logging
    logging.basicConfig(
        level=getattr(logging, log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=handlers,
        force=True,  # Override any existing configuration
    )

    # Get logger for use in conf.py
    logger = logging.getLogger("sphinx.conf")
    config["_logger"] = logger

    # Log startup
    logger.info(f"Sphinx configuration starting - log level: {log_level}")
    logger.info(f"Configuration directory: {conf_dir}")

    # Suppress verbose loggers
    logging.getLogger("sphinx.util.docutils").setLevel(logging.WARNING)
    logging.getLogger("sphinx.util.i18n").setLevel(logging.WARNING)
    logging.getLogger("sphinx.util.matching").setLevel(logging.WARNING)

    return config


def get_debug_config() -> dict[str, Any]:
    """Get debug logging configuration.

    Returns:
        Dictionary with debug-level logging
    """
    return get_config(
        log_level="DEBUG", log_file="sphinx_debug_full.log", console_output=True
    )


def get_minimal_config() -> dict[str, Any]:
    """Get minimal logging configuration."""
    return get_config(log_level="WARNING", log_file=None, console_output=True)


def get_standard_config() -> dict[str, Any]:
    """Get standard logging configuration."""
    return get_config(log_level="INFO", log_file="sphinx.log", console_output=True)


def get_full_config() -> dict[str, Any]:
    """Get full logging configuration with debug."""
    return get_config(
        log_level="DEBUG", log_file="sphinx_debug.log", console_output=True
    )


def get_quiet_config() -> dict[str, Any]:
    """Get quiet logging configuration.

    Returns:
        Dictionary with minimal logging
    """
    return get_config(log_level="WARNING", log_file=None, console_output=True)
