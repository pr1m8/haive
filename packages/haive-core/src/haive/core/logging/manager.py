# src/haive/core/logging/manager.py

"""Central logging manager for the Haive framework.

Manages Rich console output, file logging, and project-wide configuration.
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.text import Text
from rich.theme import Theme
from rich.traceback import install as install_rich_traceback

from haive.core.logging.formatters import FileFormatter, RichFormatter
from haive.core.logging.handlers import RichConsoleHandler, RotatingFileHandler


class LoggingManager:
    """Central manager for all logging in the Haive framework.

    Provides Rich-based console logging, file logging, and project-wide configuration.
    """

    _instance: Optional["LoggingManager"] = None

    def __init__(self):
        """Initialize the logging manager."""
        if LoggingManager._instance is not None:
            raise RuntimeError("LoggingManager is a singleton. Use get_instance().")

        # Rich console setup
        self.console = self._create_rich_console()
        self.error_console = self._create_error_console()

        # Logging configuration
        self.log_level = logging.INFO
        self.log_dir: Path | None = None
        self.file_logging_enabled = True
        self.console_logging_enabled = True
        self.rich_tracebacks_enabled = True

        # Component loggers
        self.loggers: dict[str, logging.Logger] = {}
        self.handlers: dict[str, logging.Handler] = {}

        # Initialize
        self._setup_rich_tracebacks()
        self._find_project_root()

    @classmethod
    def get_instance(cls) -> "LoggingManager":
        """Get the singleton instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _create_rich_console(self) -> Console:
        """Create the main Rich console with custom theme."""
        theme = Theme(
            {
                "logging.level.debug": "dim cyan",
                "logging.level.info": "bright_blue",
                "logging.level.warning": "yellow",
                "logging.level.error": "red",
                "logging.level.critical": "bold red on white",
                "haive.timestamp": "dim white",
                "haive.component": "bold cyan",
                "haive.engine": "bold green",
                "haive.agent": "bold magenta",
                "haive.graph": "bold yellow",
                "haive.tool": "bold blue",
                "haive.data": "dim green",
                "haive.performance": "bright_yellow",
                "haive.error": "bold red",
                "haive.success": "bold green",
                "haive.highlight": "bold white on blue",
            }
        )

        return Console(
            theme=theme, stderr=False, force_terminal=True, width=120, tab_size=2
        )

    def _create_error_console(self) -> Console:
        """Create console for error output."""
        return Console(stderr=True, force_terminal=True, width=120)

    def _setup_rich_tracebacks(self) -> None:
        """Setup Rich tracebacks."""
        if self.rich_tracebacks_enabled:
            install_rich_traceback(
                console=self.error_console,
                show_locals=True,
                max_frames=20,
                theme="monokai",
                word_wrap=True,
                extra_lines=2,
            )

    def _find_project_root(self) -> None:
        """Find the project root directory."""
        current_path = Path.cwd()

        # Look for project root indicators
        root_indicators = ["pyproject.toml", ".git", "haive", "packages"]

        # Walk up the directory tree
        for parent in [current_path, *list(current_path.parents)]:
            if any((parent / indicator).exists() for indicator in root_indicators):
                self.project_root = parent
                self.log_dir = parent / "logs"
                break
        else:
            # Fallback to current directory
            self.project_root = current_path
            self.log_dir = current_path / "logs"

        # Ensure logs directory exists
        self.log_dir.mkdir(exist_ok=True)

    def setup_project_logging(
        self,
        level: int | str = logging.INFO,
        log_dir: str | Path | None = None,
        console_output: bool = True,
        file_output: bool = True,
        rich_tracebacks: bool = True,
        component_subdirs: bool = True,
    ) -> None:
        """Setup project-wide logging configuration.

        Args:
            level: Logging level
            log_dir: Custom log directory (defaults to project_root/logs)
            console_output: Enable console logging
            file_output: Enable file logging
            rich_tracebacks: Enable Rich tracebacks
            component_subdirs: Create subdirectories for different components
        """
        # Set configuration
        self.log_level = (
            level if isinstance(level, int) else getattr(logging, level.upper())
        )
        self.console_logging_enabled = console_output
        self.file_logging_enabled = file_output
        self.rich_tracebacks_enabled = rich_tracebacks

        # Set custom log directory if provided
        if log_dir:
            self.log_dir = Path(log_dir)
            self.log_dir.mkdir(parents=True, exist_ok=True)

        # Setup Rich tracebacks
        if rich_tracebacks:
            self._setup_rich_tracebacks()

        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(self.log_level)

        # Clear existing handlers
        root_logger.handlers.clear()

        # Add console handler
        if console_output:
            console_handler = self._create_console_handler()
            root_logger.addHandler(console_handler)

        # Create component subdirectories if requested
        if component_subdirs and self.log_dir:
            self._create_component_subdirs()

        # Log setup completion
        self.print_startup_banner()

    def _create_component_subdirs(self) -> None:
        """Create subdirectories for different Haive components."""
        component_dirs = [
            "core",
            "agents",
            "engines",
            "graphs",
            "tools",
            "games",
            "general",
        ]

        for comp_dir in component_dirs:
            (self.log_dir / comp_dir).mkdir(exist_ok=True)

    def _create_console_handler(self) -> RichHandler:
        """Create Rich console handler."""
        handler = RichConsoleHandler(
            console=self.console,
            rich_tracebacks=True,
            tracebacks_show_locals=True,
            tracebacks_max_frames=20,
            tracebacks_theme="monokai",
        )
        handler.setLevel(self.log_level)
        handler.setFormatter(RichFormatter())
        return handler

    def _create_file_handler(
        self, component: str, filename: str | None = None
    ) -> RotatingFileHandler:
        """Create rotating file handler for a component."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d")
            filename = f"{component}_{timestamp}.log"

        # Determine subdirectory
        component_map = {
            "core": "core",
            "agent": "agents",
            "engine": "engines",
            "graph": "graphs",
            "tool": "tools",
            "game": "games",
        }

        subdir = "general"
        for key, dir_name in component_map.items():
            if key in component.lower():
                subdir = dir_name
                break

        log_file = self.log_dir / subdir / filename

        handler = RotatingFileHandler(
            filename=str(log_file),
            max_bytes=10 * 1024 * 1024,  # 10MB
            backup_count=5,
            encoding="utf-8",
        )
        handler.setLevel(self.log_level)
        handler.setFormatter(FileFormatter())

        return handler

    def get_logger(
        self, name: str, component: str | None = None, file_logging: bool = True
    ) -> logging.Logger:
        """Get or create a logger for a specific component.

        Args:
            name: Logger name (usually module name)
            component: Component type (core, agent, engine, etc.)
            file_logging: Whether to add file logging

        Returns:
            Configured logger
        """
        if name in self.loggers:
            return self.loggers[name]

        # Create logger
        logger = logging.getLogger(name)
        logger.setLevel(self.log_level)
        logger.propagate = False  # Don't propagate to root logger

        # Add console handler
        if self.console_logging_enabled:
            console_handler = self._create_console_handler()
            logger.addHandler(console_handler)

        # Add file handler
        if file_logging and self.file_logging_enabled:
            component = component or self._infer_component_from_name(name)
            file_handler = self._create_file_handler(component)
            logger.addHandler(file_handler)
            self.handlers[f"{name}_file"] = file_handler

        # Store logger
        self.loggers[name] = logger

        return logger

    def _infer_component_from_name(self, name: str) -> str:
        """Infer component type from logger name."""
        name_lower = name.lower()

        if "agent" in name_lower:
            return "agent"
        if "engine" in name_lower:
            return "engine"
        if "graph" in name_lower:
            return "graph"
        if "tool" in name_lower:
            return "tool"
        if "game" in name_lower:
            return "game"
        if "core" in name_lower:
            return "core"
        else:
            return "general"

    def print_startup_banner(self) -> None:
        """Print a beautiful startup banner."""
        banner_text = Text()
        banner_text.append("🚀 ", style="bright_yellow")
        banner_text.append("HAIVE FRAMEWORK", style="bold bright_blue")
        banner_text.append(" 🚀", style="bright_yellow")

        info_text = Text()
        info_text.append("Log Level: ", style="dim")
        info_text.append(
            f"{logging.getLevelName(self.log_level)}", style="bright_green"
        )
        info_text.append(" | Log Directory: ", style="dim")
        info_text.append(f"{self.log_dir}", style="bright_cyan")

        panel = Panel(
            Text.assemble(banner_text, "\n", info_text),
            title="[bold green]Logging Initialized[/bold green]",
            border_style="bright_blue",
            padding=(1, 2),
        )

        self.console.print(panel)

    def print_component_banner(
        self, component_name: str, component_type: str = "Component"
    ) -> None:
        """Print a banner for component initialization."""
        banner_text = Text()
        banner_text.append("⚡ ", style="bright_yellow")
        banner_text.append(f"{component_type.upper()}: ", style="bold bright_magenta")
        banner_text.append(component_name, style="bold bright_white")
        banner_text.append(" ⚡", style="bright_yellow")

        self.console.print(
            Panel(banner_text, border_style="bright_magenta", padding=(0, 1))
        )

    def log_performance(
        self,
        operation: str,
        duration: float,
        component: str = "System",
        details: dict[str, Any] | None = None,
    ) -> None:
        """Log performance information with Rich formatting."""
        perf_text = Text()
        perf_text.append("⚡ PERFORMANCE ", style="haive.performance")
        perf_text.append(f"[{component}] ", style="haive.component")
        perf_text.append(f"{operation}: ", style="bright_white")
        perf_text.append(f"{duration:.3f}s", style="bold bright_green")

        if details:
            detail_lines = []
            for key, value in details.items():
                detail_lines.append(f"  {key}: {value}")
            perf_text.append("\n" + "\n".join(detail_lines), style="dim")

        self.console.print(perf_text)

    def log_error_with_context(
        self, error: Exception, context: dict[str, Any], component: str = "System"
    ) -> None:
        """Log error with rich context information."""
        error_text = Text()
        error_text.append("💥 ERROR ", style="haive.error")
        error_text.append(f"[{component}] ", style="haive.component")
        error_text.append(f"{type(error).__name__}: ", style="bold red")
        error_text.append(str(error), style="red")

        # Add context
        if context:
            error_text.append("\n📋 Context:", style="bold yellow")
            for key, value in context.items():
                error_text.append(f"\n  {key}: {value}", style="dim yellow")

        self.error_console.print(
            Panel(
                error_text,
                title="[bold red]Exception Details[/bold red]",
                border_style="red",
                padding=(1, 2),
            )
        )

    def log_success(self, message: str, component: str = "System") -> None:
        """Log success message with Rich formatting."""
        success_text = Text()
        success_text.append("✅ SUCCESS ", style="haive.success")
        success_text.append(f"[{component}] ", style="haive.component")
        success_text.append(message, style="bright_white")

        self.console.print(success_text)

    def close(self) -> None:
        """Close all handlers and cleanup."""
        for handler in self.handlers.values():
            handler.close()

        for logger in self.loggers.values():
            for handler in logger.handlers:
                handler.close()
            logger.handlers.clear()


# Global instance
_logging_manager: LoggingManager | None = None


def get_logging_manager() -> LoggingManager:
    """Get the global logging manager instance."""
    global _logging_manager
    if _logging_manager is None:
        _logging_manager = LoggingManager.get_instance()
    return _logging_manager
