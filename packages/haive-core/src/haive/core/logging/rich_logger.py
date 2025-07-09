"""
Rich logging infrastructure for Haive framework.

This module provides a unified logging solution that combines Python's logging
with Rich's formatting capabilities for beautiful console output.
"""

import logging
import os
import sys
from contextlib import contextmanager
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Optional, Union

from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.traceback import install as install_rich_traceback


class LogLevel(str, Enum):
    """Log levels with rich styling."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


# Silence all third-party loggers by default
THIRD_PARTY_LOGGERS = [
    "httpcore",
    "httpcore._trace",
    "httpcore._sync",
    "httpcore._async",
    "httpx",
    "httpx._client",
    "openai",
    "openai._base_client",
    "openai._client",
    "anthropic",
    "langchain",
    "langchain_core",
    "langchain_community",
    "langchain_openai",
    "urllib3",
    "urllib3.connectionpool",
    "requests",
    "requests.packages.urllib3",
    "asyncio",
    "azure",
    "azure.core",
    "azure.core.pipeline",
]


def silence_third_party_loggers(level: int = logging.WARNING):
    """Silence third-party library loggers."""
    for logger_name in THIRD_PARTY_LOGGERS:
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)
        logger.propagate = False

        # Remove all existing handlers to prevent output
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

        # Add a null handler to prevent any output
        if not any(isinstance(h, logging.NullHandler) for h in logger.handlers):
            logger.addHandler(logging.NullHandler())


# Apply silencing immediately on module import
silence_third_party_loggers()


class RichLogger:
    """
    Enhanced logger that combines Python logging with Rich formatting.

    This provides:
    - Standard logging interface
    - Rich console output
    - Structured logging for complex objects
    - Debug mode toggling
    - Performance tracking
    """

    _instances: Dict[str, "RichLogger"] = {}
    _console = Console(stderr=True)  # Use stderr for logging
    _debug_mode = False
    _initialized = False

    def __init__(self, name: str, level: int = logging.WARNING):
        """Initialize a RichLogger instance."""
        self.name = name
        self.logger = logging.getLogger(name)

        # Only add handler if not already present
        if not self.logger.handlers:
            handler = RichHandler(
                console=self._console,
                show_time=True,
                show_path=False,
                markup=True,
                rich_tracebacks=True,
                tracebacks_show_locals=True,
            )
            handler.setFormatter(logging.Formatter("%(message)s"))
            self.logger.addHandler(handler)
            self.logger.setLevel(level)

        # Install rich traceback handler only once
        if not RichLogger._initialized:
            install_rich_traceback(console=self._console, show_locals=True)
            RichLogger._initialized = True

            # Ensure third-party loggers are silenced
            silence_third_party_loggers()

    @classmethod
    def get_logger(cls, name: str, level: int = logging.INFO) -> "RichLogger":
        """Get or create a RichLogger instance."""
        if name not in cls._instances:
            cls._instances[name] = cls(name, level)
        return cls._instances[name]

    @classmethod
    def set_debug_mode(cls, enabled: bool = True):
        """Enable or disable debug mode globally."""
        cls._debug_mode = enabled

        # Update all logger levels
        for logger in cls._instances.values():
            logger.logger.setLevel(logging.DEBUG if enabled else logging.INFO)

        # Update third-party loggers
        if enabled:
            # Even in debug mode, keep third-party loggers at INFO unless explicitly debugging them
            silence_third_party_loggers(logging.INFO)
        else:
            silence_third_party_loggers(logging.WARNING)

    @classmethod
    def is_debug_mode(cls) -> bool:
        """Check if debug mode is enabled."""
        return cls._debug_mode

    # Standard logging methods
    def debug(self, msg: str, *args, **kwargs):
        """Log debug message."""
        if self._debug_mode:
            self.logger.debug(msg, *args, **kwargs)

    def info(self, msg: str, *args, **kwargs):
        """Log info message."""
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg: str, *args, **kwargs):
        """Log warning message."""
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg: str, *args, **kwargs):
        """Log error message."""
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg: str, *args, **kwargs):
        """Log critical message."""
        self.logger.critical(msg, *args, **kwargs)

    # Rich formatting methods
    def table(self, title: str, data: Dict[str, Any], level: int = logging.INFO):
        """Log data as a rich table."""
        if not self.logger.isEnabledFor(level):
            return

        table = Table(title=title, show_header=False)
        table.add_column("Key", style="cyan", no_wrap=True)
        table.add_column("Value", style="yellow")

        for key, value in data.items():
            formatted_value = self._format_value(value)
            table.add_row(str(key), formatted_value)

        # Create a panel for better visibility
        panel = Panel(table, expand=False, border_style="blue")

        # Log using console print but respect log level
        self._console.print(panel)

    def panel(
        self,
        msg: str,
        title: Optional[str] = None,
        level: int = logging.INFO,
        style: str = "blue",
    ):
        """Log message in a rich panel."""
        if self.logger.isEnabledFor(level):
            panel = Panel(msg, title=title, expand=False, border_style=style)
            self._console.print(panel)

    def success(self, msg: str):
        """Log success message with green styling."""
        self.logger.info(f"[green]✓[/green] {msg}")

    def failure(self, msg: str):
        """Log failure message with red styling."""
        self.logger.error(f"[red]✗[/red] {msg}")

    def progress(self, msg: str):
        """Log progress message with blue styling."""
        self.logger.info(f"[blue]→[/blue] {msg}")

    def debug_table(self, title: str, data: Dict[str, Any]):
        """Log debug table (only shown in debug mode)."""
        if self._debug_mode:
            self.table(title, data, level=logging.DEBUG)

    def debug_panel(self, msg: str, title: Optional[str] = None):
        """Log debug panel (only shown in debug mode)."""
        if self._debug_mode:
            self.panel(msg, title, level=logging.DEBUG, style="dim")

    @contextmanager
    def track_time(self, operation: str):
        """Context manager to track operation time."""
        start = datetime.now()
        self.debug(f"Starting: {operation}")
        try:
            yield
        finally:
            duration = (datetime.now() - start).total_seconds()
            self.debug(f"Completed: {operation} ({duration:.2f}s)")

    def log_exception(self, exc: Exception, msg: Optional[str] = None):
        """Log exception with rich traceback."""
        if msg:
            self.error(msg)
        self.logger.exception("Exception occurred:", exc_info=exc)

    # Helper methods
    def _format_value(self, value: Any, max_length: int = 100) -> str:
        """Format value for display."""
        if value is None:
            return "[dim]None[/dim]"

        str_value = str(value)
        if len(str_value) > max_length:
            return str_value[: max_length - 3] + "..."
        return str_value

    def set_level(self, level: Union[int, str]):
        """Set logger level."""
        if isinstance(level, str):
            level = getattr(logging, level.upper())
        self.logger.setLevel(level)


# Convenience functions
def get_logger(name: str, level: int = logging.INFO) -> RichLogger:
    """Get a RichLogger instance."""
    return RichLogger.get_logger(name, level)


def enable_debug_mode():
    """Enable debug mode globally."""
    RichLogger.set_debug_mode(True)


def disable_debug_mode():
    """Disable debug mode globally."""
    RichLogger.set_debug_mode(False)


def configure_logging(
    level: Union[int, str] = logging.INFO,
    debug_env_var: str = "HAIVE_DEBUG",
    log_file: Optional[Path] = None,
):
    """
    Configure logging for the entire application.

    Args:
        level: Default log level
        debug_env_var: Environment variable to check for debug mode
        log_file: Optional log file path
    """
    # Ensure third-party loggers are silenced first
    silence_third_party_loggers()

    # Set debug mode from environment
    if os.getenv(debug_env_var, "").lower() in ("true", "1", "yes"):
        RichLogger.set_debug_mode(True)
        level = logging.DEBUG

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Remove any existing handlers to avoid duplicates
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Add rich handler to root logger
    console = Console(stderr=True)
    rich_handler = RichHandler(
        console=console,
        show_time=True,
        show_path=False,
        markup=True,
        rich_tracebacks=True,
    )
    rich_handler.setLevel(level)
    root_logger.addHandler(rich_handler)

    # Add file handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        root_logger.addHandler(file_handler)

    # Final pass to ensure third-party loggers are silenced
    silence_third_party_loggers()


# Apply configuration on import if not already configured
if not logging.getLogger().handlers:
    configure_logging()
