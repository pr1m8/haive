#!/usr/bin/env python3
"""Demo of the Haive Logging Control System.

This script demonstrates how to use the unified logging control interface
to manage logging across all haive packages.
"""

import logging
import time

# Note: The haive.core.logging module functions don't exist in current structure
# This demo will use standard Python logging instead


# Example class using standard logging
class ExampleAgent:
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(f"agent.{name}")

    def process(self):
        self.logger.info("Starting processing...")
        self.logger.debug("Debug details that might be hidden")
        self.logger.warning("This is a warning")
        self.logger.error("This is an error (not real)")


def main():
    # Setup basic logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Create some loggers
    core_logger = logging.getLogger("haive.core.example")
    engine_logger = logging.getLogger("haive.core.engine.test")
    game_logger = logging.getLogger("haive.games.demo")
    external_logger = logging.getLogger("langchain.test")

    # Create an agent
    agent = ExampleAgent("DemoAgent")

    # Demo 1: Default logging
    core_logger.info("Core info message")
    core_logger.debug("Core debug message (hidden)")
    engine_logger.info("Engine info message")
    game_logger.warning("Game warning message")
    external_logger.info("External library message")
    agent.process()

    # Demo 2: Debug mode
    logging.getLogger().setLevel(logging.DEBUG)
    core_logger.debug("Core debug message (now visible)")
    engine_logger.debug("Engine debug message")
    agent.process()

    # Demo 3: Quiet mode (warning and above)
    logging.getLogger().setLevel(logging.WARNING)
    core_logger.info("Core info (hidden)")
    core_logger.warning("Core warning (visible)")
    engine_logger.error("Engine error (visible)")
    agent.process()

    # Demo 4: Filter mode (normally would filter non-haive)
    logging.getLogger().setLevel(logging.INFO)
    core_logger.info("Core info (visible)")
    external_logger.info("External info (would be hidden with proper filter)")
    external_logger.error("External error (would be hidden with proper filter)")

    # Demo 5: Custom configuration
    # Reset to normal
    logging.getLogger().setLevel(logging.INFO)

    # Set specific module to debug
    logging.getLogger("haive.core.engine.test").setLevel(logging.DEBUG)

    # Suppress a specific module
    logging.getLogger("haive.games.demo").setLevel(logging.CRITICAL)

    core_logger.info("Core info (visible)")
    engine_logger.debug("Engine debug (visible - set to DEBUG)")
    game_logger.error("Game error (hidden - suppressed)")

    # Demo 6: Show current status

    # Demo 7: Only show specific modules (would need custom filter)
    # Reset levels for demo
    logging.getLogger("haive.games.demo").setLevel(logging.INFO)
    core_logger.info("Core info (visible)")
    engine_logger.info("Engine info (visible - part of core)")
    game_logger.info("Game info (would be filtered in real implementation)")

    # Demo 8: Verbosity levels
    levels = [
        logging.CRITICAL,
        logging.ERROR,
        logging.WARNING,
        logging.INFO,
        logging.DEBUG,
        logging.NOTSET,
    ]
    for _i, level in enumerate(levels):
        logging.getLogger().setLevel(level)
        core_logger.debug("  Debug")
        core_logger.info("  Info")
        core_logger.warning("  Warning")
        core_logger.error("  Error")
        core_logger.critical("  Critical")

    # Demo 9: Configuration management (basic example)
    # Set debug level
    logging.getLogger().setLevel(logging.DEBUG)

    # Reset for performance demo
    logging.getLogger().setLevel(logging.INFO)

    # Demo 10: Performance logging
    logging.getLogger().setLevel(logging.INFO)

    perf_logger = logging.getLogger("haive.performance.demo")

    # Simulate some operations
    start = time.time()
    time.sleep(0.1)
    duration = time.time() - start
    perf_logger.info(f"Operation completed in {duration:.3f}s")


if __name__ == "__main__":
    main()
