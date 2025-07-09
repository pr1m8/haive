#!/usr/bin/env python3
"""
Command-line interface for haive logging system.

Usage:
    python -m haive.core.logging [command] [options]
"""

import argparse
import sys
from typing import List, Optional

from haive.core.logging.control import logging_control


def create_parser():
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        description="Haive Logging Control CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Launch interactive CLI
  python -m haive.core.logging interactive
  
  # Enable source tracking (see where logs come from)
  python -m haive.core.logging source
  
  # Launch UI
  python -m haive.core.logging ui
  
  # Launch dashboard
  python -m haive.core.logging dashboard
  
  # Set global level
  python -m haive.core.logging level DEBUG
  
  # Suppress modules
  python -m haive.core.logging suppress langchain urllib3
  
  # Apply preset
  python -m haive.core.logging preset debug
  
  # Monitor logs
  python -m haive.core.logging monitor
  
  # Quick debug toggle
  python -m haive.core.logging debug on
  python -m haive.core.logging debug off
""",
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Interactive CLI command
    subparsers.add_parser(
        "interactive",
        aliases=["i", "cli"],
        help="Launch interactive CLI with prompt-toolkit",
    )

    # Source tracking command
    source_parser = subparsers.add_parser(
        "source",
        aliases=["src", "track"],
        help="Enable source tracking - see exactly where logs come from",
    )
    source_parser.add_argument(
        "--simple", action="store_true", help="Use simple format without rich colors"
    )

    # UI command
    subparsers.add_parser("ui", help="Launch interactive UI")

    # Dashboard command
    subparsers.add_parser("dashboard", help="Launch advanced dashboard")

    # Monitor command
    monitor_parser = subparsers.add_parser("monitor", help="Monitor logs in real-time")
    monitor_parser.add_argument(
        "-f", "--filter", nargs="+", help="Filter to specific modules"
    )

    # Level command
    level_parser = subparsers.add_parser("level", help="Set global log level")
    level_parser.add_argument(
        "level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Log level",
    )

    # Module command
    module_parser = subparsers.add_parser(
        "module", help="Set module-specific log level"
    )
    module_parser.add_argument("name", help="Module name")
    module_parser.add_argument(
        "level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Log level",
    )

    # Preset command
    preset_parser = subparsers.add_parser("preset", help="Apply logging preset")
    preset_parser.add_argument(
        "preset",
        choices=[
            "debug",
            "normal",
            "quiet",
            "silent",
            "haive-only",
            "development",
            "production",
            "minimal",
            "verbose",
        ],
        help="Preset name",
    )

    # Suppress command
    suppress_parser = subparsers.add_parser("suppress", help="Suppress modules")
    suppress_parser.add_argument("modules", nargs="+", help="Modules to suppress")

    # Filter command
    filter_parser = subparsers.add_parser("filter", help="Filter to specific modules")
    filter_parser.add_argument("modules", nargs="+", help="Modules to show")

    # Status command
    subparsers.add_parser("status", help="Show current status")

    # Test command
    subparsers.add_parser("test", help="Generate test logs")

    # Debug command - quick toggle
    debug_parser = subparsers.add_parser(
        "debug", help="Quick debug toggle or module-specific debug"
    )
    debug_parser.add_argument(
        "action",
        choices=["on", "off", "toggle"],
        nargs="?",
        default="toggle",
        help="Debug action",
    )
    debug_parser.add_argument(
        "-m", "--modules", nargs="+", help="Specific modules to debug"
    )

    return parser


def main(args: Optional[List[str]] = None):
    """Main entry point."""
    parser = create_parser()
    parsed_args = parser.parse_args(args)

    if not parsed_args.command:
        parser.print_help()
        return

    command = parsed_args.command

    try:
        if command in ["interactive", "i", "cli"]:
            # Launch interactive CLI
            from haive.core.logging.interactive_cli import InteractiveLoggingCLI

            cli = InteractiveLoggingCLI()
            cli.run()

        elif command in ["source", "src", "track"]:
            # Enable source tracking
            from haive.core.logging.auto_config import enable_source_tracking

            enable_source_tracking()

            # Show example
            print("\nExample output:")
            print(
                "[14:32:15] INFO     haive.core.engine | execute() in executor.py:123"
            )
            print("           └─ Shows: module path | function in file:line\n")

            if not parsed_args.simple:
                print("Tip: Use --simple flag for simpler output without colors")

        elif command == "ui":
            print("Launching logging UI...")
            from haive.core.logging.ui import launch_ui

            launch_ui()

        elif command == "dashboard":
            print("Launching logging dashboard...")
            from haive.core.logging.dashboard import launch_dashboard

            launch_dashboard()

        elif command == "monitor":
            from haive.core.logging.ui import monitor_logs

            if parsed_args.filter:
                logging_control.only_show(parsed_args.filter)
            monitor_logs()

        elif command == "level":
            logging_control.set_level(parsed_args.level)
            print(f"Set global log level to {parsed_args.level}")

        elif command == "module":
            logging_control.set_module_level(parsed_args.name, parsed_args.level)
            print(f"Set {parsed_args.name} to {parsed_args.level}")

        elif command == "preset":
            preset = parsed_args.preset
            if preset == "debug":
                logging_control.debug_mode()
            elif preset == "normal":
                logging_control.set_level("INFO")
            elif preset == "quiet":
                logging_control.quiet_mode()
            elif preset == "silent":
                logging_control.silent_mode()
            elif preset == "haive-only":
                logging_control.haive_only()
            elif preset == "development":
                from haive.core.logging.auto_config import auto_configure_logging

                auto_configure_logging(preset="development")
            elif preset == "production":
                from haive.core.logging.auto_config import auto_configure_logging

                auto_configure_logging(preset="minimal")
            elif preset == "minimal":
                from haive.core.logging.auto_config import auto_configure_logging

                auto_configure_logging(preset="minimal")
            elif preset == "verbose":
                from haive.core.logging.auto_config import auto_configure_logging

                auto_configure_logging(preset="verbose")
            print(f"Applied preset: {preset}")

        elif command == "suppress":
            for module in parsed_args.modules:
                logging_control.suppress(module)
            print(f"Suppressed: {', '.join(parsed_args.modules)}")

        elif command == "filter":
            logging_control.only_show(parsed_args.modules)
            print(f"Filtering to: {', '.join(parsed_args.modules)}")

        elif command == "status":
            print(f"Global level: {logging_control.current_level}")
            if logging_control._suppressed_modules:
                print(
                    f"Suppressed: {', '.join(sorted(logging_control._suppressed_modules))}"
                )
            if logging_control._show_only_modules:
                print(f"Filtered to: {', '.join(logging_control._show_only_modules)}")
            if logging_control._module_levels:
                print("Module levels:")
                for module, level in sorted(logging_control._module_levels.items()):
                    print(f"  {module}: {level}")

        elif command == "test":
            print("Generating test logs...")
            import logging
            import time

            # Test different levels
            test_logger = logging.getLogger("haive.test")
            test_logger.debug("This is a debug message")
            test_logger.info("This is an info message")
            test_logger.warning("This is a warning message")
            test_logger.error("This is an error message")

            # Test from different modules
            for module in [
                "haive.core.engine",
                "haive.agents.test",
                "haive.tools.sample",
            ]:
                logger = logging.getLogger(module)
                logger.info(f"Test message from {module}")
                time.sleep(0.1)

            print("Test logs generated!")

        elif command == "debug":
            action = parsed_args.action
            modules = parsed_args.modules

            if modules:
                # Module-specific debug
                if action in ["on", "toggle"]:
                    for module in modules:
                        logging_control.set_module_level(module, "DEBUG")
                    print(f"Debug enabled for: {', '.join(modules)}")
                else:  # off
                    for module in modules:
                        logging_control.set_module_level(module, "INFO")
                    print(f"Debug disabled for: {', '.join(modules)}")
            else:
                # Global debug toggle
                if action == "on":
                    logging_control.debug_mode()
                    print("Debug mode enabled")
                elif action == "off":
                    logging_control.set_level("INFO")
                    print("Debug mode disabled")
                else:  # toggle
                    if logging_control.current_level == "DEBUG":
                        logging_control.set_level("INFO")
                        print("Debug mode disabled")
                    else:
                        logging_control.debug_mode()
                        print("Debug mode enabled")

    except ImportError as e:
        print(f"Error: Required module not available - {e}")
        print("Install with: pip install haive[logging]")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
