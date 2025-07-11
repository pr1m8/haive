#!/usr/bin/env python3
"""Auto-wrapper for running Python scripts with source tracking.

Usage:
    python -m haive.core.logging.auto_wrapper your_script.py [args]

Or make it your default Python interpreter:
    alias python='python -m haive.core.logging.auto_wrapper'
"""

import runpy
import sys
from pathlib import Path


def setup_logging():
    """Set up logging with source tracking."""
    try:
        from haive.core.logging.quick_setup import setup_development_logging

        setup_development_logging()
        return True
    except ImportError:
        return False


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        sys.exit(1)

    # Get the script to run
    script_path = sys.argv[1]

    # Update sys.argv to remove wrapper script
    sys.argv = sys.argv[1:]

    # Set up logging
    if setup_logging():
        passn")

    # Run the script
    if script_path.endswith(".py"):
        # Run as a script file
        runpy.run_path(script_path, run_name="__main__")
    elif "." in script_path:
        # Run as a module (e.g., package.module)
        runpy.run_module(script_path, run_name="__main__", alter_sys=True)
    else:
        # Try both
        try:
            runpy.run_module(script_path, run_name="__main__", alter_sys=True)
        except ImportError:
            if Path(script_path + ".py").exists():
                runpy.run_path(script_path + ".py", run_name="__main__")
            else:
                raise


if __name__ == "__main__":
    main()
