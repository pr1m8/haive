"""
Haive Logging Control - Simple interface to manage logging across all packages.

This module provides a unified control interface for managing logging levels,
filtering output, and controlling what gets printed across the entire haive framework.

Usage:
    from haive.core.logging.control import logging_control

    # Set global level
    logging_control.set_level("WARNING")

    # Set specific module levels
    logging_control.set_module_level("haive.core.engine", "DEBUG")

    # Suppress noisy modules
    logging_control.suppress("langchain")

    # Only show specific modules
    logging_control.only_show(["haive.core", "haive.games"])
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Set, Union

from haive.core.logging.manager import get_logging_manager
from haive.core.logging.utils import get_logger as get_haive_logger


class HaiveLoggingControl:
    """
    Unified control interface for all logging in the haive framework.

    This provides simple methods to:
    - Set logging levels globally or per module
    - Suppress noisy modules
    - Filter to only show specific modules
    - Save/load logging configurations
    """

    def __init__(self):
        """Initialize the logging control."""
        self.logging_manager = get_logging_manager()
        self._suppressed_modules: Set[str] = set()
        self._allowed_modules: Optional[Set[str]] = None  # None means allow all
        self._module_levels: Dict[str, int] = {}
        self._global_level = logging.INFO

        # Common third-party modules that can be noisy
        self.common_noisy_modules = [
            "urllib3",
            "httpx",
            "httpcore",
            "openai",
            "anthropic",
            "langchain",
            "langchain_core",
            "langchain_community",
            "asyncio",
            "PIL",
            "matplotlib",
            "rich",
            "websocket",
            "aiohttp",
            "requests",
            "boto3",
            "botocore",
            "google",
            "azure",
            "transformers",
            "torch",
            "tensorflow",
            "numpy",
            "pandas",
            "sklearn",
            "psycopg",
            "sqlalchemy",
            "alembic",
            "uvicorn",
            "fastapi",
            "pydantic",
        ]

        # Load any saved configuration
        self._load_config()

    def _load_config(self):
        """Load saved logging configuration if it exists."""
        config_path = Path.home() / ".haive" / "logging_config.json"
        if config_path.exists():
            try:
                with open(config_path) as f:
                    config = json.load(f)
                    self._global_level = config.get("global_level", logging.INFO)
                    self._module_levels = {
                        k: v for k, v in config.get("module_levels", {}).items()
                    }
                    self._suppressed_modules = set(config.get("suppressed_modules", []))
                    allowed = config.get("allowed_modules")
                    self._allowed_modules = set(allowed) if allowed else None
            except Exception:
                pass  # Ignore errors loading config

    def save_config(self):
        """Save current logging configuration."""
        config_path = Path.home() / ".haive" / "logging_config.json"
        config_path.parent.mkdir(parents=True, exist_ok=True)

        config = {
            "global_level": self._global_level,
            "module_levels": self._module_levels,
            "suppressed_modules": list(self._suppressed_modules),
            "allowed_modules": (
                list(self._allowed_modules) if self._allowed_modules else None
            ),
        }

        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)

    def set_level(self, level: Union[str, int]):
        """
        Set global logging level for all haive modules.

        Args:
            level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) or numeric value
        """
        if isinstance(level, str):
            level = getattr(logging, level.upper(), logging.INFO)

        self._global_level = level
        self.logging_manager.log_level = level

        # Update all existing loggers
        self._update_all_loggers()

        # Also set root logger
        logging.getLogger().setLevel(level)

    def set_module_level(self, module: str, level: Union[str, int]):
        """
        Set logging level for a specific module or package.

        Args:
            module: Module name (e.g., "haive.core.engine")
            level: Logging level
        """
        if isinstance(level, str):
            level = getattr(logging, level.upper(), logging.INFO)

        self._module_levels[module] = level

        # Update any existing loggers for this module
        self._update_module_loggers(module, level)

    def suppress(self, *modules: str):
        """
        Suppress all logging from specified modules.

        Args:
            *modules: Module names to suppress
        """
        for module in modules:
            self._suppressed_modules.add(module)
            # Set to CRITICAL + 1 to suppress all logs
            self.set_module_level(module, logging.CRITICAL + 1)

    def unsuppress(self, *modules: str):
        """
        Unsuppress logging from specified modules.

        Args:
            *modules: Module names to unsuppress
        """
        for module in modules:
            self._suppressed_modules.discard(module)
            # Reset to global level
            if module in self._module_levels:
                del self._module_levels[module]
            self._update_module_loggers(module, self._global_level)

    def suppress_third_party(self):
        """Suppress common noisy third-party modules."""
        self.suppress(*self.common_noisy_modules)

    def only_show(self, modules: List[str]):
        """
        Only show logs from specified modules (filter mode).

        Args:
            modules: List of module prefixes to show
        """
        self._allowed_modules = set(modules)
        self._update_all_loggers()

    def show_all(self):
        """Remove module filtering - show all logs."""
        self._allowed_modules = None
        self._update_all_loggers()

    def _update_all_loggers(self):
        """Update all existing loggers with current configuration."""
        # Update haive loggers
        for name, logger in self.logging_manager.loggers.items():
            self._configure_logger(name, logger)

        # Update all other loggers
        for name, logger in logging.Logger.manager.loggerDict.items():
            if isinstance(logger, logging.Logger):
                self._configure_logger(name, logger)

    def _update_module_loggers(self, module: str, level: int):
        """Update all loggers for a specific module."""
        # Update exact match
        if module in logging.Logger.manager.loggerDict:
            logger = logging.getLogger(module)
            logger.setLevel(level)

        # Update all child loggers
        for name in logging.Logger.manager.loggerDict:
            if name.startswith(module + ".") or name == module:
                logger = logging.getLogger(name)
                logger.setLevel(level)

    def _configure_logger(self, name: str, logger: logging.Logger):
        """Configure a single logger based on current settings."""
        # Check if module is suppressed
        for suppressed in self._suppressed_modules:
            if name.startswith(suppressed):
                logger.setLevel(logging.CRITICAL + 1)
                return

        # Check if we're in filter mode
        if self._allowed_modules is not None:
            allowed = any(name.startswith(prefix) for prefix in self._allowed_modules)
            if not allowed:
                logger.setLevel(logging.CRITICAL + 1)
                return

        # Check for specific module level
        level = self._global_level
        for module, module_level in self._module_levels.items():
            if name.startswith(module):
                level = module_level
                break

        logger.setLevel(level)

    def status(self):
        """Print current logging configuration status."""
        from rich.console import Console
        from rich.table import Table

        console = Console()

        # Create status table
        table = Table(title="Haive Logging Configuration")
        table.add_column("Setting", style="cyan")
        table.add_column("Value", style="yellow")

        # Global level
        table.add_row("Global Level", logging.getLevelName(self._global_level))

        # Module levels
        if self._module_levels:
            module_info = "\n".join(
                [
                    f"{m}: {logging.getLevelName(l)}"
                    for m, l in sorted(self._module_levels.items())
                ]
            )
            table.add_row("Module Levels", module_info)

        # Suppressed modules
        if self._suppressed_modules:
            table.add_row("Suppressed", ", ".join(sorted(self._suppressed_modules)))

        # Filter mode
        if self._allowed_modules:
            table.add_row("Filter Mode", "Active")
            table.add_row("Allowed Modules", ", ".join(sorted(self._allowed_modules)))
        else:
            table.add_row("Filter Mode", "Disabled (showing all)")

        console.print(table)

    def quick_setup(self, preset: str = "normal"):
        """
        Quick setup with common presets.

        Args:
            preset: One of "debug", "normal", "quiet", "silent", "haive-only"
        """
        presets = {
            "debug": {
                "level": "DEBUG",
                "suppress_third_party": True,
            },
            "normal": {
                "level": "INFO",
                "suppress_third_party": True,
            },
            "quiet": {
                "level": "WARNING",
                "suppress_third_party": True,
            },
            "silent": {
                "level": "CRITICAL",
            },
            "haive-only": {
                "level": "INFO",
                "only_show": ["haive"],
                "suppress_third_party": False,  # Not needed with only_show
            },
        }

        if preset not in presets:
            raise ValueError(
                f"Unknown preset: {preset}. Choose from: {list(presets.keys())}"
            )

        config = presets[preset]

        # Apply configuration
        self.set_level(config.get("level", "INFO"))

        if config.get("suppress_third_party", False):
            self.suppress_third_party()

        if "only_show" in config:
            self.only_show(config["only_show"])

        print(f"✅ Logging configured with '{preset}' preset")

    def set_verbosity(self, verbosity: int):
        """
        Set logging verbosity level (0-5).

        Args:
            verbosity: 0=silent, 1=critical, 2=error, 3=warning, 4=info, 5=debug
        """
        levels = {
            0: logging.CRITICAL + 1,  # Silent
            1: logging.CRITICAL,
            2: logging.ERROR,
            3: logging.WARNING,
            4: logging.INFO,
            5: logging.DEBUG,
        }

        level = levels.get(verbosity, logging.INFO)
        self.set_level(level)

    def enable_debug_for(self, *modules: str):
        """Enable debug logging for specific modules while keeping others at current level."""
        for module in modules:
            self.set_module_level(module, "DEBUG")

    def get_logger(self, name: str) -> logging.Logger:
        """Get a logger with current configuration applied."""
        logger = get_haive_logger(name)
        self._configure_logger(name, logger)
        return logger


# Global instance
logging_control = HaiveLoggingControl()


# Convenience functions for quick access
def set_log_level(level: Union[str, int]):
    """Set global logging level."""
    logging_control.set_level(level)


def suppress_modules(*modules: str):
    """Suppress logging from specified modules."""
    logging_control.suppress(*modules)


def only_show_modules(modules: List[str]):
    """Only show logs from specified modules."""
    logging_control.only_show(modules)


def debug_mode():
    """Enable debug mode with sensible defaults."""
    logging_control.quick_setup("debug")


def quiet_mode():
    """Enable quiet mode - only warnings and above."""
    logging_control.quick_setup("quiet")


def haive_only():
    """Show only haive framework logs."""
    logging_control.quick_setup("haive-only")


# Export main control
__all__ = [
    "logging_control",
    "set_log_level",
    "suppress_modules",
    "only_show_modules",
    "debug_mode",
    "quiet_mode",
    "haive_only",
]
