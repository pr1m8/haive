"""
Automatic logging configuration for haive framework.

This module provides default configurations to reduce log clutter
while preserving important information.
"""

import logging
import os
from typing import List, Optional

from haive.core.logging.control import logging_control

# Try to import enhanced formatter
try:
    from haive.core.logging.enhanced_formatter import (
        AutoSourceHandler,
        RichSourceFormatter,
        setup_source_aware_logging,
    )

    ENHANCED_FORMATTER_AVAILABLE = True
except ImportError:
    ENHANCED_FORMATTER_AVAILABLE = False


# Default noisy modules to suppress
NOISY_MODULES = [
    # LangChain ecosystem - very chatty
    "langchain",
    "langchain_core",
    "langchain_community",
    "langsmith",
    "langgraph",
    "langchain.schema",
    "langchain.callbacks",
    "langchain.chat_models",
    # HTTP/Network libraries
    "urllib3",
    "httpx",
    "httpcore",
    "aiohttp",
    "requests",
    "websocket",
    # AI Provider libraries
    "openai",
    "anthropic",
    "google.generativeai",
    "cohere",
    "mistralai",
    # Async/concurrent
    "asyncio",
    "concurrent.futures",
    # Database/ORM
    "sqlalchemy",
    "alembic",
    "psycopg",
    "psycopg2",
    # Other frameworks
    "transformers",
    "torch",
    "tensorflow",
    "numpy",
    "pandas",
    "matplotlib",
    "PIL",
    # Haive internals that are too verbose
    "haive.core.graph.dynamic",
    "haive.core.graph.dynamic_graph_builder",
    "DynamicGraph",
]

# Modules to set to WARNING level
WARNING_MODULES = [
    # These can be noisy but sometimes have useful warnings
    "haive.core.engine.aug_llm",
    "haive.core.engine.aug_llm.config",
    "haive.core.engine.aug_llm.factory",
    "haive.core.engine.agent.workflow",
    "rich.print",  # Suppress rich print output
]

# Modules that should stay at INFO level
INFO_MODULES = [
    # Important for understanding flow
    "haive.core.engine.agent",
    "haive.games",
    "haive.agents",
    "haive.tools",
]


def auto_configure_logging(
    preset: str = "default",
    additional_suppressions: Optional[List[str]] = None,
    debug_modules: Optional[List[str]] = None,
    use_source_formatter: bool = True,
):
    """
    Automatically configure logging with sensible defaults.

    Args:
        preset: Configuration preset ('default', 'minimal', 'verbose', 'development')
        additional_suppressions: Extra modules to suppress
        debug_modules: Modules to set to DEBUG level
        use_source_formatter: Use enhanced formatter that shows source info
    """

    # Set up enhanced formatter if available and requested
    if use_source_formatter and ENHANCED_FORMATTER_AVAILABLE:
        # Remove existing handlers
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

        # Add enhanced handler
        handler = AutoSourceHandler()
        root_logger.addHandler(handler)

        # Also add a simple handler for libraries that don't use root logger
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(RichSourceFormatter())
        logging.getLogger("haive").addHandler(console_handler)

    # Load preset
    if preset == "minimal":
        # Very quiet - only errors and critical
        logging_control.set_level("ERROR")
        suppress_list = NOISY_MODULES + WARNING_MODULES

    elif preset == "verbose":
        # Show more detail
        logging_control.set_level("DEBUG")
        suppress_list = NOISY_MODULES[:10]  # Only suppress the worst offenders

    elif preset == "development":
        # Good for development - see your code but not libraries
        logging_control.set_level("INFO")
        suppress_list = NOISY_MODULES
        # Set haive modules to DEBUG
        if debug_modules is None:
            debug_modules = ["haive"]

    else:  # default
        # Balanced configuration
        logging_control.set_level("INFO")
        suppress_list = NOISY_MODULES

    # Apply suppressions
    for module in suppress_list:
        logging_control.suppress(module)

    # Add additional suppressions
    if additional_suppressions:
        for module in additional_suppressions:
            logging_control.suppress(module)

    # Set WARNING level modules
    for module in WARNING_MODULES:
        logging_control.set_module_level(module, "WARNING")

    # Set DEBUG modules if specified
    if debug_modules:
        for module in debug_modules:
            logging_control.set_module_level(module, "DEBUG")

    # Environment variable overrides
    if os.getenv("HAIVE_LOG_VERBOSE"):
        logging_control.set_level("DEBUG")
    elif os.getenv("HAIVE_LOG_QUIET"):
        logging_control.set_level("WARNING")

    # Show only haive logs if requested
    if os.getenv("HAIVE_ONLY"):
        logging_control.only_show(["haive"])

    # Disable source formatter if requested
    if os.getenv("HAIVE_LOG_SIMPLE"):
        use_source_formatter = False


def configure_for_game_development():
    """Special configuration for game development."""
    auto_configure_logging(preset="development")

    # Show game-specific logs
    logging_control.set_module_level("haive.games", "DEBUG")

    # Suppress game engine internals
    logging_control.suppress("haive.games.base")
    logging_control.suppress("haive.games.engine")

    # But show game agent decisions
    logging_control.set_module_level("haive.games.*.agent", "INFO")


def configure_for_agent_development():
    """Special configuration for agent development."""
    auto_configure_logging(preset="development")

    # Show agent logs
    logging_control.set_module_level("haive.agents", "DEBUG")
    logging_control.set_module_level("haive.core.engine.agent", "DEBUG")

    # Suppress graph building noise
    logging_control.suppress("haive.core.graph.dynamic")


def show_clean_logs():
    """
    Ultra-clean configuration showing only essential logs.
    Perfect for demos or when you just want to see your app work.
    """
    # Start with minimal
    auto_configure_logging(preset="minimal")

    # Only show specific haive modules
    logging_control.only_show(["haive.agents", "haive.games", "haive.tools"])

    # And only INFO and above
    logging_control.set_level("INFO")


def enable_source_tracking(verbose: bool = False):
    """
    Enable detailed source tracking for all logs.

    This shows exactly where each log message comes from:
    - Module path (e.g., haive.core.engine)
    - Function/method name
    - File and line number
    - Thread information

    Args:
        verbose: Whether to print status messages
    """
    if ENHANCED_FORMATTER_AVAILABLE:
        setup_source_aware_logging()
        if verbose and not hasattr(enable_source_tracking, "_already_announced"):
            print(
                "📍 Source tracking enabled - you'll see exactly where each log comes from!"
            )
            enable_source_tracking._already_announced = True
    else:
        if verbose:
            print("⚠️  Enhanced formatter not available - using standard logging")


# Export convenience functions
__all__ = [
    "auto_configure_logging",
    "configure_for_game_development",
    "configure_for_agent_development",
    "show_clean_logs",
    "enable_source_tracking",
    "NOISY_MODULES",
    "WARNING_MODULES",
    "INFO_MODULES",
]
