"""Enhanced formatter for haive logging that shows detailed source information.

This formatter makes it easy to see exactly where each log message comes from,
including the module, class, function, and line number.
"""

import logging
import os
from datetime import datetime

try:
    from rich import box
    from rich.console import Console
    from rich.table import Table
    from rich.text import Text

    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


class SourceAwareFormatter(logging.Formatter):
    """Enhanced formatter that shows detailed source information.

    Shows:
    - Full module path (e.g., haive.core.engine.executor)
    - Class name if available
    - Function/method name
    - Line number
    - File path (shortened)
    """

    def __init__(self, show_full_path: bool = False, show_thread: bool = True):
        """Initialize the formatter.

        Args:
            show_full_path: Show full file paths instead of shortened ones
            show_thread: Show thread information
        """
        self.show_full_path = show_full_path
        self.show_thread = show_thread

        fmt = (
            "%(asctime)s | %(levelname)-8s | %(name)-30s | %(source)-40s | %(message)s"
        )

        if show_thread:
            fmt = "%(asctime)s | %(levelname)-8s | %(name)-30s | [%(threadName)s] %(source)-40s | %(message)s"

        super().__init__(fmt=fmt, datefmt="%H:%M:%S.%f")[:-3]

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record with enhanced source information."""
        # Add source information
        source_parts = []

        # Add class name if available
        if hasattr(record, "className") and record.className:
            source_parts.append(record.className)

        # Add function name
        if record.funcName and record.funcName != "<module>":
            source_parts.append(f"{record.funcName}()")

        # Add file and line
        if record.pathname:
            if self.show_full_path:
                file_path = record.pathname
            else:
                # Shorten path - show only last 2 directories
                path_parts = record.pathname.split(os.sep)
                if len(path_parts) > 3:
                    file_path = os.path.join("...", *path_parts[-3:])
                else:
                    file_path = record.pathname

            source_parts.append(f"{file_path}:{record.lineno}")

        # Combine source information
        record.source = " -> ".join(source_parts) if source_parts else "unknown"

        # Format the message
        formatted = super().format(record)

        # Add exception info if present
        if record.exc_info:
            formatted += "\n" + self.formatException(record.exc_info)

        return formatted


class RichSourceFormatter(logging.Formatter):
    """Rich formatter that beautifully displays source information."""

    def __init__(self):
        super().__init__()
        self.console = Console() if RICH_AVAILABLE else None

    def format(self, record: logging.LogRecord) -> str:
        """Format with rich colors and source info."""
        if not RICH_AVAILABLE:
            # Fallback to basic formatting
            return f"{record.levelname}: [{record.name}] {record.getMessage()} (from {record.funcName} in {record.filename}:{record.lineno})"

        text = Text()

        # Time
        timestamp = datetime.fromtimestamp(record.created).strftime("%H:%M:%S")
        text.append(f"[{timestamp}] ", style="dim cyan")

        # Level with color
        level_colors = {
            "DEBUG": "dim blue",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold red on white",
        }
        color = level_colors.get(record.levelname, "white")
        text.append(f"{record.levelname:8} ", style=color)

        # Module name with hierarchy highlighting
        module_parts = record.name.split(".")
        for i, part in enumerate(module_parts):
            if i == 0:
                # Root module (e.g., "haive")
                text.append(part, style="bold blue")
            elif i == len(module_parts) - 1:
                # Last part
                text.append(f".{part}", style="bold cyan")
            else:
                # Middle parts
                text.append(f".{part}", style="cyan")

        text.append(" | ", style="dim")

        # Source location
        if record.funcName and record.funcName != "<module>":
            text.append(f"{record.funcName}()", style="magenta")
            text.append(" in ", style="dim")

        # File location
        text.append(f"{record.filename}:{record.lineno}", style="dim yellow")

        # Thread info if not main thread
        if hasattr(record, "threadName") and record.threadName != "MainThread":
            text.append(f" [{record.threadName}]", style="dim purple")

        text.append("\n    ", style="")

        # Message
        text.append(record.getMessage(), style="white")

        # Exception
        if record.exc_info:
            text.append("\n", style="")
            text.append(self.formatException(record.exc_info), style="red")

        return text.plain if hasattr(text, "plain") else str(text)


def create_source_table(records: list) -> Table | None:
    """Create a rich table showing log sources.

    Useful for analyzing where logs are coming from.
    """
    if not RICH_AVAILABLE:
        return None

    table = Table(title="Log Sources", box=box.ROUNDED)

    table.add_column("Time", style="cyan", width=10)
    table.add_column("Level", style="green", width=8)
    table.add_column("Module", style="blue", width=25)
    table.add_column("Function", style="magenta", width=20)
    table.add_column("File:Line", style="yellow", width=30)
    table.add_column("Message", style="white", overflow="fold")

    for record in records:
        time_str = datetime.fromtimestamp(record.created).strftime("%H:%M:%S")

        # Color based on level
        level_style = {
            "DEBUG": "dim blue",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold red",
        }.get(record.levelname, "white")

        table.add_row(
            time_str,
            f"[{level_style}]{record.levelname}[/{level_style}]",
            record.name,
            record.funcName or "-",
            f"{record.filename}:{record.lineno}",
            (
                record.getMessage()[:80] + "..."
                if len(record.getMessage()) > 80
                else record.getMessage()
            ),
        )

    return table


class AutoSourceHandler(logging.Handler):
    """Handler that automatically captures and enriches source information."""

    def __init__(self, formatter=None):
        super().__init__()
        self.formatter = formatter or RichSourceFormatter()

    def emit(self, record: logging.LogRecord):
        """Emit a record with enhanced source information."""
        # Try to get class name from stack
        if not hasattr(record, "className"):
            # Look for 'self' in the calling frame
            import inspect

            frame = None
            try:
                # Get the frame that called the logging function
                for frame_info in inspect.stack()[6:10]:  # Skip logging internals
                    frame = frame_info.frame
                    if "self" in frame.f_locals:
                        obj = frame.f_locals["self"]
                        record.className = obj.__class__.__name__
                        break
                else:
                    record.className = None
            except:
                record.className = None
            finally:
                del frame  # Avoid reference cycles

        # Format and output
        try:
            self.format(record)
        except Exception:
            self.handleError(record)


def setup_source_aware_logging():
    """Set up logging to automatically show source information.

    This function configures the logging system to use enhanced formatters
    that show detailed source information for every log message.
    """
    # Remove existing handlers
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Add source-aware handler
    handler = AutoSourceHandler()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)

    # Also update haive loggers
    haive_logger = logging.getLogger("haive")
    haive_logger.propagate = True


# Convenience function to test
def demo_source_logging():
    """Demo showing source information in logs."""
    setup_source_aware_logging()

    # Create some test logs
    logger = logging.getLogger("haive.demo.test")

    class DemoClass:
        def __init__(self):
            self.logger = logging.getLogger("haive.demo.test")

        def do_something(self):
            self.logger.info("This is from inside a method")
            self.logger.debug("Debug info with full source")
            self._helper()

        def _helper(self):
            self.logger.warning("Warning from helper method")

    # Test logs
    logger.info("Direct module-level log")

    demo = DemoClass()
    demo.do_something()

    # Show in table format if rich is available
    if RICH_AVAILABLE:
        from haive.core.logging.interactive_cli import InteractiveLoggingCLI

        cli = InteractiveLoggingCLI()
        if cli.logs:
            console = Console()
            console.print("\n")
            table = create_source_table(list(cli.logs)[-10:])
            if table:
                console.print(table)


if __name__ == "__main__":
    demo_source_logging()
