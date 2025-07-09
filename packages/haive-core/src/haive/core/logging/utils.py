# src/haive/core/logging/utils.py

"""
Utility functions for the Haive logging system.
"""

import logging
from contextlib import contextmanager
from typing import Any, Dict, Optional, TypeVar

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.traceback import Traceback

from haive.core.logging.manager import get_logging_manager

T = TypeVar("T")


def get_logger(name: str, component: Optional[str] = None) -> logging.Logger:
    """
    Get a logger with Haive Rich formatting.

    Args:
        name: Logger name (usually __name__)
        component: Component type (agent, engine, graph, etc.)

    Returns:
        Configured logger with Rich formatting
    """
    manager = get_logging_manager()
    return manager.get_logger(name, component)


def setup_project_logging(**kwargs) -> None:
    """
    Setup project-wide logging with Rich formatting.

    Args:
        **kwargs: Arguments passed to LoggingManager.setup_project_logging()
    """
    manager = get_logging_manager()
    manager.setup_project_logging(**kwargs)


def log_exception(
    exception: Exception,
    context: Optional[Dict[str, Any]] = None,
    component: str = "System",
    console: Optional[Console] = None,
) -> None:
    """
    Log an exception with Rich formatting and context.

    Args:
        exception: Exception to log
        context: Additional context information
        component: Component where exception occurred
        console: Optional Rich console (uses error console if None)
    """
    manager = get_logging_manager()

    if console is None:
        console = manager.error_console

    # Create rich traceback
    tb = Traceback.from_exception(
        type(exception),
        exception,
        exception.__traceback__,
        show_locals=True,
        max_frames=20,
    )

    # Create context panel if provided
    if context:
        context_text = Text()
        context_text.append("📋 Context Information:\n", style="bold yellow")

        for key, value in context.items():
            context_text.append(f"  {key}: ", style="dim yellow")
            context_text.append(f"{value}\n", style="bright_white")

        context_panel = Panel(
            context_text,
            title="[bold yellow]Exception Context[/bold yellow]",
            border_style="yellow",
            padding=(1, 2),
        )

        console.print(context_panel)

    # Print the traceback
    console.print(tb)

    # Log to file as well
    logger = get_logger(f"{component}.exception")
    logger.error(
        f"Exception in {component}: {type(exception).__name__}: {exception}",
        exc_info=exception,
        extra={"context": context or {}},
    )


@contextmanager
def log_context(logger: logging.Logger, context: Dict[str, Any]):
    """
    Context manager that adds context to all log messages within the block.

    Args:
        logger: Logger to add context to
        context: Context dictionary to add
    """

    def context_filter(record):
        # Add context to record
        if not hasattr(record, "context"):
            record.context = {}
        record.context.update(context)
        return True  # Always allow the record through

    try:
        logger.addFilter(context_filter)
        yield
    finally:
        logger.removeFilter(context_filter)
