#!/usr/bin/env python3
"""
Demo of the Haive Logging Control System

This script demonstrates how to use the unified logging control interface
to manage logging across all haive packages.
"""

import time

from haive.core.logging import (
    LoggingMixin,
    debug_mode,
    get_logger,
    haive_only,
    logging_control,
    only_show_modules,
    quiet_mode,
)


# Example class using LoggingMixin
class ExampleAgent(LoggingMixin):
    def __init__(self, name: str):
        self.name = name
        super().__init__()

    def process(self):
        self.log_info("Starting processing...")
        self.log_debug("Debug details that might be hidden")
        self.log_warning("This is a warning")
        self.log_error("This is an error (not real)")


def main():
    print("=== Haive Logging Control Demo ===\n")

    # Create some loggers
    core_logger = get_logger("haive.core.example")
    engine_logger = get_logger("haive.core.engine.test")
    game_logger = get_logger("haive.games.demo")
    external_logger = get_logger("langchain.test")

    # Create an agent
    agent = ExampleAgent("DemoAgent")

    # Demo 1: Default logging
    print("1. Default logging (INFO level):")
    print("-" * 40)
    core_logger.info("Core info message")
    core_logger.debug("Core debug message (hidden)")
    engine_logger.info("Engine info message")
    game_logger.warning("Game warning message")
    external_logger.info("External library message")
    agent.process()
    print()

    # Demo 2: Debug mode
    print("\n2. Debug mode (shows all debug messages):")
    print("-" * 40)
    debug_mode()
    core_logger.debug("Core debug message (now visible)")
    engine_logger.debug("Engine debug message")
    agent.process()
    print()

    # Demo 3: Quiet mode
    print("\n3. Quiet mode (only warnings and above):")
    print("-" * 40)
    quiet_mode()
    core_logger.info("Core info (hidden)")
    core_logger.warning("Core warning (visible)")
    engine_logger.error("Engine error (visible)")
    agent.process()
    print()

    # Demo 4: Haive-only mode
    print("\n4. Haive-only mode (suppress external libraries):")
    print("-" * 40)
    haive_only()
    core_logger.info("Core info (visible)")
    external_logger.info("External info (hidden)")
    external_logger.error("External error (also hidden)")
    print()

    # Demo 5: Custom configuration
    print("\n5. Custom configuration:")
    print("-" * 40)
    # Reset to normal
    logging_control.quick_setup("normal")

    # Set specific module to debug
    logging_control.set_module_level("haive.core.engine", "DEBUG")

    # Suppress a specific module
    logging_control.suppress("haive.games")

    core_logger.info("Core info (visible)")
    engine_logger.debug("Engine debug (visible - set to DEBUG)")
    game_logger.error("Game error (hidden - suppressed)")
    print()

    # Demo 6: Show current status
    print("\n6. Current logging configuration:")
    print("-" * 40)
    logging_control.status()
    print()

    # Demo 7: Only show specific modules
    print("\n7. Filter mode - only show core modules:")
    print("-" * 40)
    only_show_modules(["haive.core"])
    core_logger.info("Core info (visible)")
    engine_logger.info("Engine info (visible - part of core)")
    game_logger.info("Game info (hidden - not in filter)")
    print()

    # Demo 8: Verbosity levels
    print("\n8. Verbosity levels (0-5):")
    print("-" * 40)
    for v in range(6):
        logging_control.set_verbosity(v)
        print(f"Verbosity {v}:")
        core_logger.debug("  Debug")
        core_logger.info("  Info")
        core_logger.warning("  Warning")
        core_logger.error("  Error")
        core_logger.critical("  Critical")
        print()

    # Demo 9: Save and restore configuration
    print("\n9. Save configuration:")
    print("-" * 40)
    logging_control.quick_setup("debug")
    logging_control.suppress("noisy_module")
    logging_control.save_config()
    print("Configuration saved!")

    # Reset and show it loads on next instantiation
    print("\nConfiguration will be automatically loaded on next run.")

    # Demo 10: Performance logging
    print("\n10. Performance tracking:")
    print("-" * 40)
    logging_control.set_level("INFO")

    perf_logger = get_logger("haive.performance.demo")

    # Simulate some operations
    start = time.time()
    time.sleep(0.1)
    duration = time.time() - start
    perf_logger.info(f"Operation completed in {duration:.3f}s")


if __name__ == "__main__":
    main()
