"""
Quiet imports - suppress all rich print output.

Usage:
    import haive.core.logging.quiet_imports  # This silences rich print
    import your_module  # Now imports are quiet
"""

# Monkey-patch rich print to be silent
try:
    import rich

    # Save original
    _original_print = rich.print

    # Replace with no-op
    def silent_print(*args, **kwargs):
        pass

    rich.print = silent_print

    # Also patch rprint if it's imported anywhere
    import sys

    for _module_name, module in sys.modules.items():
        if hasattr(module, "rprint"):
            module.rprint = silent_print

except ImportError:
    pass  # Rich not installed

# Set environment for quiet logging
import os

os.environ["HAIVE_LOG_QUIET"] = "1"


def restore_rich_print():
    """Restore original rich print functionality."""
    try:
        import rich

        rich.print = _original_print
    except:
        pass
