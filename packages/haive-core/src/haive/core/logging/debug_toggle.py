#!/usr/bin/env python3
"""
Quick debug toggle script for haive logging.

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
from typing import List, Optional

from haive.core.logging.control import logging_control


def toggle_debug(action: Optional[str] = None, modules: Optional[List[str]] = None):
    """
    Toggle debug logging.

    Args:
        action: 'on', 'off', or None (toggle)
        modules: Specific modules to debug (None = global)
    """
    if modules:
        # Module-specific debug
        if action in ["on", None]:
            for module in modules:
                logging_control.set_module_level(module, "DEBUG")
            print(f"✅ Debug enabled for: {', '.join(modules)}")
        else:  # off
            for module in modules:
                logging_control.set_module_level(module, "INFO")
            print(f"❌ Debug disabled for: {', '.join(modules)}")
    else:
        # Global debug toggle
        current_level = logging_control.current_level

        if action == "on":
            logging_control.debug_mode()
            print("🐛 Debug mode ENABLED")
            print("   Showing: All haive modules at DEBUG level")
            print("   Suppressed: Third-party libraries")
        elif action == "off":
            logging_control.set_level("INFO")
            print("🔕 Debug mode DISABLED")
            print("   Showing: INFO level and above")
        else:  # toggle
            if current_level == "DEBUG":
                logging_control.set_level("INFO")
                print("🔕 Debug mode DISABLED")
                print("   Showing: INFO level and above")
            else:
                logging_control.debug_mode()
                print("🐛 Debug mode ENABLED")
                print("   Showing: All haive modules at DEBUG level")
                print("   Suppressed: Third-party libraries")

        # Show quick tips
        print("\nTips:")
        print("  - Use 'python -m haive.core.logging interactive' for full control")
        print("  - Set HAIVE_LOG_VERBOSE=1 for verbose output")
        print("  - Set HAIVE_LOG_QUIET=1 for quiet output")


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
        print(__doc__)
    else:
        # Assume modules for debug on
        toggle_debug("on", args)


if __name__ == "__main__":
    main()
