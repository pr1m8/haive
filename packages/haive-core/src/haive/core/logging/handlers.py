# src/haive/core/logging/handlers.py

"""
Custom handlers for Rich console and rotating file output.
"""

import logging
from logging.handlers import RotatingFileHandler as BaseRotatingFileHandler
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.text import Text


class RichConsoleHandler(RichHandler):
    """Enhanced Rich console handler with additional formatting."""

    def __init__(self, console: Optional[Console] = None, **kwargs):
        # Set up console
        if console is None:
            console = Console()

        super().__init__(
            console=console,
            show_time=False,  # We handle time in our formatter
            show_level=False,  # We handle level in our formatter
            show_path=False,  # We handle path in our formatter
            **kwargs,
        )

    def emit(self, record: logging.LogRecord) -> None:
        """Emit a log record with Rich formatting."""
        try:
            # Check if this is a special Haive log type
            if hasattr(record, "haive_type"):
                self._emit_special_record(record)
            else:
                super().emit(record)
        except Exception:
            self.handleError(record)

    def _emit_special_record(self, record: logging.LogRecord) -> None:
        """Handle special Haive log record types."""
        haive_type = getattr(record, "haive_type", None)

        if haive_type == "banner":
            self._emit_banner(record)
        elif haive_type == "performance":
            self._emit_performance(record)
        elif haive_type == "error_context":
            self._emit_error_with_context(record)
        else:
            super().emit(record)

    def _emit_banner(self, record: logging.LogRecord) -> None:
        """Emit a banner-style log record."""
        title = getattr(record, "banner_title", "Information")
        style = getattr(record, "banner_style", "bright_blue")

        panel = Panel(
            record.getMessage(),
            title=f"[bold]{title}[/bold]",
            border_style=style,
            padding=(1, 2),
        )

        self.console.print(panel)

    def _emit_performance(self, record: logging.LogRecord) -> None:
        """Emit a performance log record."""
        operation = getattr(record, "operation", "Operation")
        duration = getattr(record, "duration", 0.0)
        component = getattr(record, "component", "System")

        perf_text = Text()
        perf_text.append("⚡ PERFORMANCE ", style="bright_yellow")
        perf_text.append(f"[{component}] ", style="bright_cyan")
        perf_text.append(f"{operation}: ", style="bright_white")
        perf_text.append(f"{duration:.3f}s", style="bold bright_green")

        self.console.print(perf_text)

    def _emit_error_with_context(self, record: logging.LogRecord) -> None:
        """Emit an error record with context."""
        context = getattr(record, "error_context", {})

        error_text = Text()
        error_text.append("💥 ERROR ", style="bold red")
        error_text.append(record.getMessage(), style="red")

        if context:
            error_text.append("\n📋 Context:", style="bold yellow")
            for key, value in context.items():
                error_text.append(f"\n  {key}: {value}", style="dim yellow")

        panel = Panel(
            error_text,
            title="[bold red]Exception Details[/bold red]",
            border_style="red",
            padding=(1, 2),
        )

        self.console.print(panel)


class RotatingFileHandler(BaseRotatingFileHandler):
    """Enhanced rotating file handler with better path handling."""

    def __init__(
        self,
        filename: str,
        max_bytes: int = 10 * 1024 * 1024,  # 10MB
        backup_count: int = 5,
        encoding: str = "utf-8",
        **kwargs,
    ):
        # Ensure directory exists
        file_path = Path(filename)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        super().__init__(
            filename=filename,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding=encoding,
            **kwargs,
        )

    def emit(self, record: logging.LogRecord) -> None:
        """Emit a record with additional context handling."""
        # Add extra context to file logs
        if hasattr(record, "context") and record.context:
            original_msg = record.msg
            context_items = []
            for key, value in record.context.items():
                context_items.append(f"{key}={value}")

            record.msg = f"{original_msg} [Context: {', '.join(context_items)}]"

        super().emit(record)
