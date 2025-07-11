#!/usr/bin/env python3
"""Demo showing automatic source tracking in haive logging.

This demonstrates how the logging system automatically shows:
- Exactly where each log comes from
- Module, class, method, and line information
- Automatic configuration when importing haive.core
"""

import time

# When you import haive.core, logging is automatically configured!
from haive.core.logging import get_logger, logging_control
from haive.core.logging.auto_config import enable_source_tracking


class ExampleService:
    """Example service to demonstrate logging."""

    def __init__(self, name: str):
        self.name = name
        self.logger = get_logger(f"haive.demo.{name}")

    def process_request(self, request_id: int):
        """Process a request with logging."""
        self.logger.info(f"Processing request {request_id}")

        try:
            self._validate_request(request_id)
            result = self._execute_request(request_id)
            self.logger.info(f"Request {request_id} completed successfully")
            return result
        except Exception as e:
            self.logger.exception(f"Request {request_id} failed: {e}")
            raise

    def _validate_request(self, request_id: int):
        """Validate the request."""
        self.logger.debug(f"Validating request {request_id}")

        if request_id < 0:
            self.logger.warning("Invalid request ID: negative value")
            raise ValueError("Request ID must be positive")

    def _execute_request(self, request_id: int):
        """Execute the request."""
        self.logger.debug(f"Executing request {request_id}")
        time.sleep(0.1)  # Simulate work
        return f"Result for request {request_id}"


class GameEngine:
    """Example game engine with logging."""

    def __init__(self):
        self.logger = get_logger("haive.games.engine")
        self.state = "idle"

    def start(self):
        """Start the game engine."""
        self.logger.info("Starting game engine")
        self.state = "running"
        self._initialize_components()

    def _initialize_components(self):
        """Initialize game components."""
        self.logger.debug("Initializing physics engine")
        self.logger.debug("Loading game assets")
        self.logger.info("Game engine initialized")

    def update(self, delta_time: float):
        """Update game state."""
        self.logger.debug(f"Updating game state (dt={delta_time:.3f})")


def module_level_function():
    """Function at module level to show source tracking."""
    logger = get_logger("haive.demo.module")
    logger.info("This is from a module-level function")
    logger.warning("You can see exactly where this comes from!")


def demo_automatic_logging():
    """Demonstrate automatic logging configuration.

    When you import haive.core, the logging system is automatically set up!
    """
    # The logging is already configured from importing haive.core
    logger = get_logger("haive.demo.main")

    logger.info("Main demo starting")
    logger.debug("Debug messages are hidden by default")

    # Create services
    service1 = ExampleService("api")
    service2 = ExampleService("processor")

    # Process some requests
    service1.process_request(123)
    service2.process_request(456)

    # Module level logging
    module_level_function()

    # Game engine example
    engine = GameEngine()
    engine.start()
    engine.update(0.016)  # 60 FPS


def demo_source_tracking():
    """Demonstrate enhanced source tracking.

    This shows exactly where each log message originates.
    """
    # Enable source tracking
    enable_source_tracking()

    # Create logger
    logger = get_logger("haive.demo.tracking")

    # Show different contexts
    logger.info("Direct call from demo_source_tracking()")

    class InnerClass:
        def __init__(self):
            self.logger = get_logger("haive.demo.tracking.inner")

        def method(self):
            self.logger.info("Call from InnerClass.method()")
            self.nested_method()

        def nested_method(self):
            self.logger.warning("Deep call from nested_method()")

    inner = InnerClass()
    inner.method()

    # Lambda and comprehension
    def process(x):
        return logger.info(f"Processing item {x}")

    for i in range(2):
        process(i)


def demo_debug_mode():
    """Demonstrate debug mode toggle."""
    logger = get_logger("haive.demo.debug")

    logger.debug("This debug message is hidden")
    logger.info("This info message is visible")

    logging_control.debug_mode()

    logger.debug("Now debug messages are visible!")
    logger.info("Info messages still visible")

    # Reset
    logging_control.set_level("INFO")


def demo_filtering():
    """Demonstrate module filtering."""
    # Create loggers from different modules
    haive_logger = get_logger("haive.core.test")
    external_logger = get_logger("external.library")

    haive_logger.info("Message from haive.core.test")
    external_logger.info("Message from external.library")

    logging_control.haive_only()

    haive_logger.info("Haive message - still visible")
    external_logger.info("External message - now hidden!")

    # Reset
    logging_control.show_all()


def main():
    """Run all demos."""
    # Basic automatic logging
    demo_automatic_logging()

    # Enhanced source tracking
    input("\nPress Enter to see enhanced source tracking...")
    demo_source_tracking()

    # Debug mode
    input("\nPress Enter to see debug mode demo...")
    demo_debug_mode()

    # Filtering
    input("\nPress Enter to see filtering demo...")
    demo_filtering()


if __name__ == "__main__":
    main()
