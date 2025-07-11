#!/usr/bin/env python3
"""Demo: How to see where logs and prints are coming from.

This shows the easiest ways to configure logging to see sources.
"""

# Method 2: Just see your code (recommended for most cases)
# Method 1: Quick one-liner to see EVERYTHING
from haive.core.logging.quick_setup import (
    setup_development_logging,
)

# Uncomment this to see EVERYTHING with sources:


# This is usually what you want:
setup_development_logging()


# Now let's test it!

from haive.core.logging import get_logger


class MyService:
    """Example service class."""

    def __init__(self):
        self.logger = get_logger("myapp.service")

    def do_work(self):
        """Do some work with logging."""
        self.logger.info("Starting work")

        try:
            result = self._internal_process()
            self.logger.info(f"Work completed: {result}")
        except Exception as e:
            self.logger.exception(f"Work failed: {e}")

    def _internal_process(self):
        """Internal processing."""
        self.logger.debug("Internal processing")
        return "Success"


def standalone_function():
    """Function outside of a class."""
    logger = get_logger("myapp.functions")
    logger.info("This is from a standalone function")


def main():
    """Main function to demonstrate source tracking."""
    # Create a logger
    logger = get_logger("myapp.main")

    # Log from main
    logger.info("Starting application")

    # Create service
    service = MyService()
    service.do_work()

    # Call standalone function
    standalone_function()

    # Show how to check status

    from haive.core.logging.quick_setup import check_status

    check_status()


if __name__ == "__main__":
    main()
