#!/usr/bin/env python3
"""Quick debug toggle script for haive logging.

Usage:
    # Toggle debug mode
    python -m haive.core.logging.debug_toggle

    # Enable debug
    python -m haive.core.logging.debug_toggle on

    # Disable debug
    python -m haive.core.logging.debug_toggle off

    # Debug specific modules
    python -m haive.core.logging.debug_toggle on haive.core.engine haive.agents
"""

import sys

from haive.core.logging.control import logging_control


def toggle_debug(action: str | None = None, modules: list[str] | None = None):
    """Toggle debug logging.

    Args:
        action: 'on', 'off', or None (toggle)
        modules: Specific modules to debug (None = global)
    """
    if modules:
        # Module-specific debug
        if action in ["on", None]:
            for module in modules:
                logging_control.set_module_level(module, "DEBUG")
        else:  # off
            for module in modules:
                logging_control.set_module_level(module, "INFO")
    elif action == "on":
        logging_control.debug_mode()
    elif action == "off":
        logging_control.set_level("INFO")
    else:
        logging_control.debug_mode()

        # Show quick tips


def main():
    """Main entry point."""
    args = sys.argv[1:]

    if not args:
        # Just toggle
        toggle_debug()
    elif args[0] in ["on", "off"]:
        # Action specified
        action = args[0]
        modules = args[1:] if len(args) > 1 else None
        toggle_debug(action, modules)
    elif args[0] in ["--help", "-h", "help"]:
        pass
    else:
        # Assume modules for debug on
        toggle_debug("on", args)


if __name__ == "__main__":
    main()
