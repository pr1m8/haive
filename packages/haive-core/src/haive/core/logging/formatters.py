# src/haive/core/logging/formatters.py

"""
Rich formatters for beautiful console and file logging.
"""

import logging
from datetime import datetime
from typing import Any, Dict

from rich.console import Console
from rich.text import Text


class RichFormatter(logging.Formatter):
    """Custom Rich formatter for beautiful console output."""

    def __init__(self):
        super().__init__()
        self.console = Console()

    def format(self, record: logging.LogRecord) -> str:
        """Format log record with Rich styling."""
        # Don't format Rich handler records (they're already formatted)
        if hasattr(record, "markup") and record.markup:
            return record.getMessage()

        # Create text with styling
        text = Text()

        # Timestamp
        timestamp = datetime.fromtimestamp(record.created).strftime("%H:%M:%S")
        text.append(f"[{timestamp}] ", style="haive.timestamp")

        # Level with color
        level_style = {
            logging.DEBUG: "logging.level.debug",
            logging.INFO: "logging.level.info",
            logging.WARNING: "logging.level.warning",
            logging.ERROR: "logging.level.error",
            logging.CRITICAL: "logging.level.critical",
        }.get(record.levelno, "dim white")

        text.append(f"{record.levelname:8}", style=level_style)
        text.append(" ", style="dim")

        # Component/module info
        module_parts = record.name.split(".")
        if len(module_parts) > 2:
            component = module_parts[-2]  # Second to last part
            module = module_parts[-1]  # Last part
            text.append(f"[{component}.{module}] ", style="haive.component")
        else:
            text.append(f"[{record.name}] ", style="haive.component")

        # Message
        message = record.getMessage()
        text.append(message, style="bright_white")

        # Exception info
        if record.exc_info:
            text.append("\n")
            text.append(self.formatException(record.exc_info), style="red")

        return text.plain


class FileFormatter(logging.Formatter):
    """Formatter for file output with detailed information."""

    def __init__(self):
        super().__init__(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    def format(self, record: logging.LogRecord) -> str:
        """Format record for file output."""
        # Add extra context if available
        if hasattr(record, "context"):
            original_msg = record.getMessage()
            context_str = self._format_context(record.context)
            record.msg = f"{original_msg} | Context: {context_str}"

        formatted = super().format(record)

        # Add exception traceback if present
        if record.exc_info:
            formatted += "\n" + self.formatException(record.exc_info)

        return formatted

    def _format_context(self, context: Dict[str, Any]) -> str:
        """Format context dictionary for file output."""
        if not context:
            return ""

        items = []
        for key, value in context.items():
            items.append(f"{key}={value}")

        return "{" + ", ".join(items) + "}"
