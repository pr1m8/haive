#!/usr/bin/env python3
"""
Advanced Haive Logging Demo

Demonstrates all features of the haive logging system including:
- Interactive CLI with prompt-toolkit
- Debug toggling
- Rich UI integration
- Module-specific control
- Real-time monitoring
"""

import time
from concurrent.futures import ThreadPoolExecutor

# Import haive logging components
from haive.core.logging import (
    debug_mode,
    get_logger,
    haive_only,
    logging_control,
    quiet_mode,
)

# Import auto-config
from haive.core.logging.auto_config import (
    auto_configure_logging,
    configure_for_agent_development,
    configure_for_game_development,
)


def demo_basic_control():
    """Demonstrate basic logging control."""
    print("\n=== Basic Logging Control Demo ===")

    # Get a logger
    logger = get_logger("haive.demo.basic")

    # Show different log levels
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")

    print("\nToggling debug mode...")
    debug_mode()

    logger.debug("Debug message - now visible!")
    logger.info("Info message - still visible")

    print("\nSwitching to quiet mode...")
    quiet_mode()

    logger.debug("Debug - hidden in quiet mode")
    logger.info("Info - hidden in quiet mode")
    logger.warning("Warning - visible in quiet mode")
    logger.error("Error - visible in quiet mode")

    # Reset
    logging_control.set_level("INFO")


def demo_module_control():
    """Demonstrate module-specific control."""
    print("\n=== Module-Specific Control Demo ===")

    # Create loggers for different modules
    engine_logger = get_logger("haive.core.engine.demo")
    agent_logger = get_logger("haive.agents.demo")
    tool_logger = get_logger("haive.tools.demo")

    # Set different levels
    logging_control.set_module_level("haive.core.engine", "DEBUG")
    logging_control.set_module_level("haive.agents", "WARNING")
    logging_control.suppress("haive.tools")

    print("\nEngine at DEBUG, Agents at WARNING, Tools suppressed:")

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
    print("\n=== Log Filtering Demo ===")

    # Create various loggers
    loggers = {
        "haive.core.engine": get_logger("haive.core.engine.test"),
        "haive.games.chess": get_logger("haive.games.chess"),
        "haive.agents.planner": get_logger("haive.agents.planner"),
        "external.library": get_logger("external.library"),
    }

    print("\nShowing only haive.core and haive.games:")
    logging_control.only_show(["haive.core", "haive.games"])

    for name, logger in loggers.items():
        logger.info(f"Message from {name}")

    print("\nShowing only haive logs:")
    haive_only()

    for name, logger in loggers.items():
        logger.info(f"Another message from {name}")

    # Reset
    logging_control.show_all()


def demo_auto_configuration():
    """Demonstrate auto-configuration presets."""
    print("\n=== Auto-Configuration Demo ===")

    # Game development preset
    print("\nApplying game development preset...")
    configure_for_game_development()

    game_logger = get_logger("haive.games.demo")
    engine_logger = get_logger("haive.games.engine")
    agent_logger = get_logger("haive.games.chess.agent")

    game_logger.debug("Game debug message - visible")
    engine_logger.debug("Engine internals - suppressed")
    agent_logger.info("Agent decision - visible")

    # Agent development preset
    print("\nApplying agent development preset...")
    configure_for_agent_development()

    agent_logger = get_logger("haive.agents.demo")
    graph_logger = get_logger("haive.core.graph.dynamic")

    agent_logger.debug("Agent debug - visible")
    graph_logger.debug("Graph building - suppressed")

    # Reset to default
    auto_configure_logging(preset="default")


def simulate_application_logs():
    """Simulate a real application generating logs."""
    print("\n=== Simulating Application Logs ===")

    # Apply default configuration
    auto_configure_logging(preset="default")

    # Simulate different components
    components = [
        ("haive.core.engine.executor", "Executing task"),
        ("haive.core.graph.builder", "Building execution graph"),
        ("haive.agents.reasoning", "Processing reasoning step"),
        ("haive.tools.web_search", "Searching web"),
        ("langchain.chat_models", "Making LLM call"),
        ("urllib3.connectionpool", "HTTP connection"),
    ]

    print("\nGenerating logs from various components...")
    print("(Notice how third-party libraries are suppressed)")

    for _ in range(3):
        for module, message in components:
            logger = get_logger(module)
            logger.info(f"{message} - {time.time()}")
            time.sleep(0.1)


def demo_concurrent_logging():
    """Demonstrate thread-safe concurrent logging."""
    print("\n=== Concurrent Logging Demo ===")

    def worker(worker_id: int, count: int):
        """Worker function that generates logs."""
        logger = get_logger(f"haive.worker.{worker_id}")
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
    print("\n=== Debug Toggle Demo ===")

    logger = get_logger("haive.demo.toggle")

    print("\nCurrent state:")
    logger.debug("Debug - not visible by default")
    logger.info("Info - visible")

    print("\nToggling debug ON...")
    from haive.core.logging.debug_toggle import toggle_debug

    toggle_debug("on")

    logger.debug("Debug - now visible!")
    logger.info("Info - still visible")

    print("\nToggling debug OFF...")
    toggle_debug("off")

    logger.debug("Debug - hidden again")
    logger.info("Info - still visible")


def show_cli_commands():
    """Show available CLI commands."""
    print("\n=== Available CLI Commands ===")
    print(
        """
# Launch interactive CLI with auto-completion
python -m haive.core.logging interactive

# Quick debug toggle
python -m haive.core.logging debug on
python -m haive.core.logging debug off

# Launch rich UI
python -m haive.core.logging ui

# Launch advanced dashboard
python -m haive.core.logging dashboard

# Monitor logs in real-time
python -m haive.core.logging monitor

# Set log levels
python -m haive.core.logging level DEBUG
python -m haive.core.logging module haive.core.engine DEBUG

# Apply presets
python -m haive.core.logging preset development

# Show status
python -m haive.core.logging status

# Generate test logs
python -m haive.core.logging test
"""
    )


def main():
    """Run all demos."""
    print("🚀 Haive Advanced Logging Demo")
    print("=" * 50)

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

    print("\n✅ Demo complete!")
    print("\nTry the interactive CLI:")
    print("  python -m haive.core.logging interactive")
    print("\nOr quick debug toggle:")
    print("  python -m haive.core.logging.debug_toggle")


if __name__ == "__main__":
    main()
