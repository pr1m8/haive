#!/usr/bin/env python3
"""Advanced Haive Logging Demo.

Demonstrates all features of the haive logging system including:
- Interactive CLI with prompt-toolkit
- Debug toggling
- Rich UI integration
- Module-specific control
- Real-time monitoring
"""

# Import haive logging components
import logging
import time
from concurrent.futures import ThreadPoolExecutor

from haive.core.logging import (
    debug_mode,
    haive_only,
    logging_control,
    quiet_mode,
)

# Basic logging setup - replace the auto-config imports
# These functions don't exist in current haive.core structure


def demo_basic_control():
    """Demonstrate basic logging control."""
    # Get a logger
    logger = logging.getLogger("haive.demo.basic")

    # Show different log levels
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")

    debug_mode()

    logger.debug("Debug message - now visible!")
    logger.info("Info message - still visible")

    quiet_mode()

    logger.debug("Debug - hidden in quiet mode")
    logger.info("Info - hidden in quiet mode")
    logger.warning("Warning - visible in quiet mode")
    logger.error("Error - visible in quiet mode")

    # Reset
    logging_control.set_level("INFO")


def demo_module_control():
    """Demonstrate module-specific control."""
    # Create loggers for different modules
    engine_logger = logging.getLogger("haive.core.engine.demo")
    agent_logger = logging.getLogger("haive.agents.demo")
    tool_logger = logging.getLogger("haive.tools.demo")

    # Set different levels
    logging_control.set_module_level("haive.core.engine", "DEBUG")
    logging_control.set_module_level("haive.agents", "WARNING")
    logging_control.suppress("haive.tools")

    # Test each module
    engine_logger.debug("Engine debug - visible")
    engine_logger.info("Engine info - visible")

    agent_logger.debug("Agent debug - hidden")
    agent_logger.info("Agent info - hidden")
    agent_logger.warning("Agent warning - visible")

    tool_logger.error("Tool error - suppressed!")

    # Reset
    logging_control.show_all()
    logging_control.set_level("INFO")


def demo_filtering():
    """Demonstrate log filtering."""
    # Create various loggers
    loggers = {
        "haive.core.engine": logging.getLogger("haive.core.engine.test"),
        "haive.games.chess": logging.getLogger("haive.games.chess"),
        "haive.agents.planner": logging.getLogger("haive.agents.planner"),
        "external.library": logging.getLogger("external.library"),
    }

    logging_control.only_show(["haive.core", "haive.games"])

    for name, logger in loggers.items():
        logger.info(f"Message from {name}")

    haive_only()

    for name, logger in loggers.items():
        logger.info(f"Another message from {name}")

    # Reset
    logging_control.show_all()


def demo_auto_configuration():
    """Demonstrate auto-configuration presets."""
    # Game development preset - using basic config
    logging.basicConfig(
        level=logging.DEBUG, format="%(name)s - %(levelname)s - %(message)s"
    )

    game_logger = logging.getLogger("haive.games.demo")
    engine_logger = logging.getLogger("haive.games.engine")
    agent_logger = logging.getLogger("haive.games.chess.agent")

    game_logger.debug("Game debug message - visible")
    engine_logger.debug("Engine internals - suppressed")
    agent_logger.info("Agent decision - visible")

    # Agent development preset - using basic config
    logging.basicConfig(
        level=logging.DEBUG, format="%(name)s - %(levelname)s - %(message)s"
    )

    agent_logger = logging.getLogger("haive.agents.demo")
    graph_logger = logging.getLogger("haive.core.graph.dynamic")

    agent_logger.debug("Agent debug - visible")
    graph_logger.debug("Graph building - suppressed")

    # Reset to default
    logging.basicConfig(
        level=logging.INFO, format="%(name)s - %(levelname)s - %(message)s"
    )


def simulate_application_logs():
    """Simulate a real application generating logs."""
    # Apply default configuration
    logging.basicConfig(
        level=logging.INFO, format="%(name)s - %(levelname)s - %(message)s"
    )

    # Simulate different components
    components = [
        ("haive.core.engine.executor", "Executing task"),
        ("haive.core.graph.builder", "Building execution graph"),
        ("haive.agents.reasoning", "Processing reasoning step"),
        ("haive.tools.web_search", "Searching web"),
        ("langchain.chat_models", "Making LLM call"),
        ("urllib3.connectionpool", "HTTP connection"),
    ]

    for _ in range(3):
        for module, message in components:
            logger = logging.getLogger(module)
            logger.info(f"{message} - {time.time()}")
            time.sleep(0.1)


def demo_concurrent_logging():
    """Demonstrate thread-safe concurrent logging."""

    def worker(worker_id: int, count: int):
        """Worker function that generates logs."""
        logger = logging.getLogger(f"haive.worker.{worker_id}")
        for i in range(count):
            logger.info(f"Worker {worker_id} - Task {i}")
            time.sleep(0.05)

    # Use thread pool
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(worker, i, 5) for i in range(3)]

        # Wait for completion
        for future in futures:
            future.result()


def demo_debug_toggle():
    """Demonstrate the debug toggle functionality."""
    logger = logging.getLogger("haive.demo.toggle")

    logger.debug("Debug - not visible by default")
    logger.info("Info - visible")

    # Toggle debug - using standard logging
    logging.getLogger().setLevel(logging.DEBUG)

    logger.debug("Debug - now visible!")
    logger.info("Info - still visible")

    # Toggle debug off
    logging.getLogger().setLevel(logging.INFO)

    logger.debug("Debug - hidden again")
    logger.info("Info - still visible")


def show_cli_commands():
    """Show available CLI commands."""


def main():
    """Run all demos."""
    # Run demos
    demo_basic_control()
    input("\nPress Enter to continue...")

    demo_module_control()
    input("\nPress Enter to continue...")

    demo_filtering()
    input("\nPress Enter to continue...")

    demo_auto_configuration()
    input("\nPress Enter to continue...")

    simulate_application_logs()
    input("\nPress Enter to continue...")

    demo_concurrent_logging()
    input("\nPress Enter to continue...")

    demo_debug_toggle()

    # Show CLI commands
    show_cli_commands()


if __name__ == "__main__":
    main()
