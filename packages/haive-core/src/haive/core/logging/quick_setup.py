"""
Quick setup utilities for haive logging with source tracking.

This module provides easy functions to configure logging so you always
know where messages are coming from.
"""

import logging
from typing import List, Optional

from haive.core.logging.auto_config import enable_source_tracking
from haive.core.logging.control import logging_control


def show_all_sources():
    """
    Enable logging that shows the source of EVERY log message.

    This is the easiest way to see where everything is coming from!
    """
    # Enable source tracking
    enable_source_tracking(verbose=True)

    # Set to debug level to see everything
    logging_control.set_level("DEBUG")

    # Show all modules (remove any filters)
    logging_control.show_all()

    print("📍 Source tracking enabled for ALL modules!")
    print("   You'll now see: [TIME] LEVEL module.name | function() in file:line")
    print(
        "   Example: [14:32:15] INFO haive.core.engine | execute() in executor.py:123\n"
    )


def show_haive_sources():
    """
    Show source information only for haive modules.

    This filters out third-party noise but shows where haive logs come from.
    """
    # Enable source tracking
    enable_source_tracking(verbose=True)

    # Only show haive modules
    logging_control.haive_only()

    print("📍 Source tracking enabled for haive modules only!")
    print("   Third-party libraries are hidden.\n")


def track_specific_modules(modules: List[str]):
    """
    Track specific modules with source information.

    Args:
        modules: List of module names to track (e.g., ["haive.core.engine", "myapp"])
    """
    # Enable source tracking
    enable_source_tracking()

    # Filter to specific modules
    logging_control.only_show(modules)

    # Set them to debug level
    for module in modules:
        logging_control.set_module_level(module, "DEBUG")

    print(f"📍 Source tracking enabled for: {', '.join(modules)}")
    print("   All other modules are hidden.\n")


def debug_with_source(module: Optional[str] = None):
    """
    Enable debug mode with source tracking.

    Args:
        module: Specific module to debug, or None for all haive modules
    """
    # Enable source tracking
    enable_source_tracking()

    if module:
        # Debug specific module
        logging_control.set_module_level(module, "DEBUG")
        print(f"🐛 Debug mode with source tracking enabled for: {module}\n")
    else:
        # Debug all haive modules
        logging_control.debug_mode()
        print("🐛 Debug mode with source tracking enabled for all haive modules!\n")


def intercept_prints():
    """
    Intercept print() statements to show where they come from.

    This replaces the built-in print() with a version that shows source info.
    """
    import builtins
    import inspect

    # Check if already intercepted
    if hasattr(builtins.print, "_is_tracked"):
        return  # Already intercepted, don't do it again

    original_print = builtins.print

    def tracked_print(*args, **kwargs):
        """Print with source tracking."""
        # Get caller info
        frame = inspect.currentframe()
        caller_frame = frame.f_back

        filename = caller_frame.f_code.co_filename
        line_no = caller_frame.f_lineno
        func_name = caller_frame.f_code.co_name

        # Get module name from filename
        module_name = "unknown"
        if "site-packages" in filename:
            # Third-party module
            parts = filename.split("site-packages/")[1].split("/")
            module_name = parts[0]
        elif "haive" in filename:
            # Haive module
            parts = filename.split("haive/")[1].replace("/", ".").replace(".py", "")
            module_name = f"haive.{parts}"
        else:
            # Local file
            import os

            module_name = os.path.basename(filename).replace(".py", "")

        # Format the output
        source_info = f"[PRINT from {module_name}.{func_name}():{line_no}]"

        # Print with source info
        original_print(f"\033[36m{source_info}\033[0m", *args, **kwargs)

    # Mark as tracked
    tracked_print._is_tracked = True

    # Replace print
    builtins.print = tracked_print

    # Only print the message if this is the first time
    if not hasattr(intercept_prints, "_already_announced"):
        original_print(
            "🖨️  Print tracking enabled! All print() statements will show their source."
        )
        original_print("   Example: [PRINT from mymodule.function():123] Hello world\n")
        intercept_prints._already_announced = True


def intercept_prints_silent():
    """
    Silently intercept print() statements to show where they come from.

    This is the same as intercept_prints() but without any announcement.
    """
    import builtins
    import inspect

    # Check if already intercepted
    if hasattr(builtins.print, "_is_tracked"):
        return  # Already intercepted, don't do it again

    original_print = builtins.print

    def tracked_print(*args, **kwargs):
        """Print with source tracking."""
        # Get caller info
        frame = inspect.currentframe()
        caller_frame = frame.f_back

        filename = caller_frame.f_code.co_filename
        line_no = caller_frame.f_lineno
        func_name = caller_frame.f_code.co_name

        # Get module name from filename
        module_name = "unknown"
        if "site-packages" in filename:
            # Third-party module
            parts = filename.split("site-packages/")[1].split("/")
            module_name = parts[0]
        elif "haive" in filename:
            # Haive module
            parts = filename.split("haive/")[1].replace("/", ".").replace(".py", "")
            module_name = f"haive.{parts}"
        else:
            # Local file
            import os

            module_name = os.path.basename(filename).replace(".py", "")

        # Format the output
        source_info = f"[PRINT from {module_name}.{func_name}():{line_no}]"

        # Print with source info
        original_print(f"\033[36m{source_info}\033[0m", *args, **kwargs)

    # Mark as tracked
    tracked_print._is_tracked = True

    # Replace print
    builtins.print = tracked_print

    # Silent - no announcement


def setup_development_logging():
    """
    Set up ideal logging configuration for development.

    This gives you:
    - Source tracking for all logs
    - Debug level for haive modules
    - Suppressed third-party noise
    - Print statement tracking
    """
    # Enable source tracking
    enable_source_tracking()

    # Configure for development
    from haive.core.logging.auto_config import auto_configure_logging

    auto_configure_logging(preset="development", use_source_formatter=True)

    # Also track prints (silently)
    intercept_prints_silent()


# Convenience functions for common cases
def i_want_to_see_everything():
    """Use this when you're really confused and need to see EVERYTHING."""
    show_all_sources()
    intercept_prints()
    print("🔍 MAXIMUM VISIBILITY MODE ACTIVATED!")
    print("   You'll see EVERY log and print with full source info.\n")


def just_show_my_code():
    """Use this to see only your application code, not libraries."""
    enable_source_tracking()

    # Suppress all common third-party modules
    from haive.core.logging.auto_config import NOISY_MODULES

    for module in NOISY_MODULES:
        logging_control.suppress(module)

    print("👁️  Showing only your code (third-party libraries hidden)\n")


def where_is_this_coming_from(search_text: str):
    """
    Helper to find where specific log messages are coming from.

    Args:
        search_text: Text to search for in log messages
    """
    print(f"🔎 Setting up tracking for messages containing: '{search_text}'")
    print("   Run your code and look for messages with this text.\n")

    # Enable source tracking
    enable_source_tracking()

    # Set everything to debug to catch all messages
    logging_control.set_level("DEBUG")

    # Add a filter that highlights matching messages
    import logging

    class HighlightFilter(logging.Filter):
        def filter(self, record):
            if search_text.lower() in record.getMessage().lower():
                # Add marker to make it stand out
                record.msg = f"🎯 FOUND: {record.msg}"
            return True

    # Add filter to root logger
    root_logger = logging.getLogger()
    root_logger.addFilter(HighlightFilter())


# Quick aliases for common commands
def debug_on():
    """Quick command to enable debug with source tracking."""
    debug_with_source()


def debug_off():
    """Quick command to disable debug mode."""
    logging_control.set_level("INFO")
    print("🔕 Debug mode disabled\n")


def check_status():
    """Show current logging configuration."""
    from rich.console import Console
    from rich.table import Table

    console = Console()

    table = Table(title="Current Logging Configuration")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Global Level", logging_control.current_level)
    table.add_row(
        "Source Tracking",
        (
            "Enabled"
            if any(
                isinstance(h.formatter, type) and "Source" in type(h.formatter).__name__
                for h in logging.getLogger().handlers
            )
            else "Disabled"
        ),
    )
    table.add_row("Suppressed Modules", str(len(logging_control._suppressed_modules)))
    table.add_row(
        "Filtered Modules",
        (
            ", ".join(logging_control._show_only_modules)
            if logging_control._show_only_modules
            else "None (showing all)"
        ),
    )

    console.print(table)

    # Show module-specific levels if any
    if logging_control._module_levels:
        console.print("\n[yellow]Module-specific levels:[/yellow]")
        for module, level in sorted(logging_control._module_levels.items()):
            console.print(f"  {module}: {level}")


def redirect_rich_print_to_logging():
    """
    Redirect rich print statements to logging.

    This converts rprint() calls to logger.debug() calls.
    """
    try:
        import logging

        import rich

        # Get or create a logger for rich output
        rich_logger = logging.getLogger("rich.print")

        # Store original print
        if not hasattr(rich, "_original_print"):
            rich._original_print = rich.print

        def logged_print(*args, **kwargs):
            # Convert args to string
            message = " ".join(str(arg) for arg in args)
            # Log at debug level
            rich_logger.debug(message)

        # Replace rich.print
        rich.print = logged_print

    except ImportError:
        pass  # Rich not available


if __name__ == "__main__":
    # Demo the functionality
    print("Haive Logging Quick Setup Demo\n")

    # Show different options
    print("1. See everything with sources:")
    print("   from haive.core.logging.quick_setup import i_want_to_see_everything")
    print("   i_want_to_see_everything()\n")

    print("2. Just your code:")
    print("   from haive.core.logging.quick_setup import just_show_my_code")
    print("   just_show_my_code()\n")

    print("3. Track specific modules:")
    print("   from haive.core.logging.quick_setup import track_specific_modules")
    print("   track_specific_modules(['haive.core.engine', 'myapp'])\n")

    print("4. Find where something is coming from:")
    print("   from haive.core.logging.quick_setup import where_is_this_coming_from")
    print("   where_is_this_coming_from('error message text')\n")

    print("5. Development setup (recommended):")
    print("   from haive.core.logging.quick_setup import setup_development_logging")
    print("   setup_development_logging()\n")
