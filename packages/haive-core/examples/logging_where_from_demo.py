#!/usr/bin/env python3
"""
Demo: How to see where logs and prints are coming from

This shows the easiest ways to configure logging to see sources.
"""

# Method 2: Just see your code (recommended for most cases)
# Method 1: Quick one-liner to see EVERYTHING
from haive.core.logging.quick_setup import (
    setup_development_logging,
)

# Uncomment this to see EVERYTHING with sources:
# i_want_to_see_everything()


# This is usually what you want:
setup_development_logging()


# Now let's test it!

from haive.core.logging import get_logger


class MyService:
    """Example service class."""

    def __init__(self):
        self.logger = get_logger("myapp.service")
        print("MyService initialized")  # This print will show source!

    def do_work(self):
        """Do some work with logging."""
        self.logger.info("Starting work")
        print("Doing work...")  # This print will show source!

        try:
            result = self._internal_process()
            self.logger.info(f"Work completed: {result}")
        except Exception as e:
            self.logger.error(f"Work failed: {e}")

    def _internal_process(self):
        """Internal processing."""
        self.logger.debug("Internal processing")
        return "Success"


def standalone_function():
    """Function outside of a class."""
    logger = get_logger("myapp.functions")
    logger.info("This is from a standalone function")
    print("Regular print from function")


def main():
    """Main function to demonstrate source tracking."""
    print("\n" + "=" * 60)
    print("DEMO: Seeing where logs and prints come from")
    print("=" * 60 + "\n")

    # Create a logger
    logger = get_logger("myapp.main")

    # Log from main
    logger.info("Starting application")
    print("This is a regular print statement")

    # Create service
    service = MyService()
    service.do_work()

    # Call standalone function
    standalone_function()

    # Show how to check status
    print("\n" + "-" * 40)
    print("Checking logging configuration:")
    print("-" * 40)

    from haive.core.logging.quick_setup import check_status

    check_status()

    print("\n" + "=" * 60)
    print("WHAT YOU'RE SEEING:")
    print("=" * 60)
    print(
        """
Each log shows:
[TIME] LEVEL module.name | function() in file:line
    The actual message

Each print shows:
[PRINT from module.function():line] The printed text

This makes it easy to find exactly where any output is coming from!
"""
    )

    print("\nOTHER QUICK SETUP OPTIONS:")
    print("-" * 40)
    print(
        """
# See EVERYTHING (all modules, all levels):
from haive.core.logging.quick_setup import i_want_to_see_everything
i_want_to_see_everything()

# Just your code (hide libraries):
from haive.core.logging.quick_setup import just_show_my_code
just_show_my_code()

# Track specific modules:
from haive.core.logging.quick_setup import track_specific_modules
track_specific_modules(['haive.core.engine', 'myapp'])

# Find where a specific message comes from:
from haive.core.logging.quick_setup import where_is_this_coming_from
where_is_this_coming_from('error text to find')

# Enable/disable debug quickly:
from haive.core.logging.quick_setup import debug_on, debug_off
debug_on()   # Enable debug with sources
debug_off()  # Back to normal
"""
    )


if __name__ == "__main__":
    main()
