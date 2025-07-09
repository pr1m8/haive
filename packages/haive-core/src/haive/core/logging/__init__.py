# src/haive/core/logging/__init__.py

"""
Haive Rich Logging System

A comprehensive logging system built around Rich UI with extensive formatting,
file logging, and beautiful console output.
"""

from haive.core.logging.control import (
    debug_mode,
    haive_only,
    logging_control,
    only_show_modules,
    quiet_mode,
    set_log_level,
    suppress_modules,
)
from haive.core.logging.decorators import log_calls, log_errors, log_performance
from haive.core.logging.formatters import FileFormatter, RichFormatter
from haive.core.logging.handlers import RichConsoleHandler, RotatingFileHandler
from haive.core.logging.manager import LoggingManager
from haive.core.logging.mixins import LoggingMixin, RichLoggerMixin
from haive.core.logging.utils import get_logger, log_exception, setup_project_logging

# Import auto-configuration functions
try:
    from haive.core.logging.auto_config import (
        auto_configure_logging,
        configure_for_agent_development,
        configure_for_game_development,
        show_clean_logs,
    )

    AUTO_CONFIG_AVAILABLE = True
except ImportError:
    AUTO_CONFIG_AVAILABLE = False

# Import UI components if available
try:
    from haive.core.logging.ui import (
        LoggingMonitor,
        LoggingUI,
        launch_ui,
        monitor_logs,
    )

    UI_AVAILABLE = True
except ImportError:
    UI_AVAILABLE = False

try:
    from haive.core.logging.dashboard import (
        LoggingDashboard,
        ModuleActivityVisualizer,
        launch_dashboard,
    )

    DASHBOARD_AVAILABLE = True
except ImportError:
    DASHBOARD_AVAILABLE = False

__all__ = [
    # Manager and mixins
    "LoggingManager",
    "LoggingMixin",
    "RichLoggerMixin",
    # Formatters and handlers
    "RichFormatter",
    "FileFormatter",
    "RichConsoleHandler",
    "RotatingFileHandler",
    # Utilities
    "get_logger",
    "setup_project_logging",
    "log_exception",
    # Decorators
    "log_calls",
    "log_performance",
    "log_errors",
    # Control interface
    "logging_control",
    "set_log_level",
    "suppress_modules",
    "only_show_modules",
    "debug_mode",
    "quiet_mode",
    "haive_only",
]

# Add auto-config exports if available
if AUTO_CONFIG_AVAILABLE:
    __all__.extend(
        [
            "auto_configure_logging",
            "configure_for_game_development",
            "configure_for_agent_development",
            "show_clean_logs",
        ]
    )

# Add UI exports if available
if UI_AVAILABLE:
    __all__.extend(
        [
            "LoggingUI",
            "LoggingMonitor",
            "launch_ui",
            "monitor_logs",
        ]
    )

if DASHBOARD_AVAILABLE:
    __all__.extend(
        [
            "LoggingDashboard",
            "ModuleActivityVisualizer",
            "launch_dashboard",
        ]
    )
