"""Interactive CLI for Haive Logging System.

Provides a rich, interactive command-line interface with auto-completion,
debugging tools, and real-time log monitoring.
"""

import logging
import os
import time

# Core imports
from collections import defaultdict, deque
from datetime import datetime

from haive.core.logging.control import logging_control

# Rich imports
try:
    from rich import box
    from rich.console import Console
    from rich.layout import Layout
    from rich.live import Live
    from rich.panel import Panel
    from rich.syntax import Syntax
    from rich.table import Table
    from rich.text import Text
    from rich.tree import Tree

    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

# Prompt toolkit imports
try:
    from prompt_toolkit import PromptSession
    from prompt_toolkit.application import Application
    from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
    from prompt_toolkit.completion import FuzzyCompleter, WordCompleter
    from prompt_toolkit.formatted_text import HTML
    from prompt_toolkit.history import FileHistory
    from prompt_toolkit.key_binding import KeyBindings
    from prompt_toolkit.layout import Layout as PTLayout
    from prompt_toolkit.layout.containers import HSplit, VSplit, Window
    from prompt_toolkit.layout.controls import FormattedTextControl
    from prompt_toolkit.shortcuts import confirm, input_dialog
    from prompt_toolkit.validation import ValidationError, Validator
    from prompt_toolkit.widgets import SearchToolbar, TextArea

    PROMPT_TOOLKIT_AVAILABLE = True
except ImportError:
    PROMPT_TOOLKIT_AVAILABLE = False

# Readchar for simple key input
try:
    import readchar

    READCHAR_AVAILABLE = True
except ImportError:
    READCHAR_AVAILABLE = False


class LogLevelValidator(Validator):
    """Validate log level input."""

    def validate(self, document):
        text = document.text.upper()
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if text and text not in valid_levels:
            raise ValidationError(
                message=f"Invalid log level. Choose from: {', '.join(valid_levels)}",
                cursor_position=len(document.text),
            )


class InteractiveLoggingCLI:
    """Interactive CLI for managing logging with rich UI and debugging features."""

    def __init__(self):
        self.console = Console() if RICH_AVAILABLE else None
        self.running = False
        self.logs = deque(maxlen=1000)
        self.module_stats = defaultdict(
            lambda: {"count": 0, "levels": defaultdict(int)}
        )
        self.session = None
        self.history_file = os.path.expanduser("~/.haive/logging_cli_history")

        # Ensure history directory exists
        os.makedirs(os.path.dirname(self.history_file), exist_ok=True)

        # Setup prompt session if available
        if PROMPT_TOOLKIT_AVAILABLE:
            self._setup_prompt_session()

    def _setup_prompt_session(self):
        """Setup prompt toolkit session with completions."""
        # Command completions
        commands = [
            "help",
            "status",
            "level",
            "module",
            "suppress",
            "unsuppress",
            "filter",
            "clear-filter",
            "preset",
            "debug",
            "monitor",
            "ui",
            "dashboard",
            "export",
            "stats",
            "test",
            "quit",
            "exit",
            "show-all",
            "hide-all",
            "trace",
            "profile",
            "breakpoint",
        ]

        # Log level completions
        levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

        # Preset completions
        presets = [
            "debug",
            "normal",
            "quiet",
            "silent",
            "haive-only",
            "development",
            "production",
            "minimal",
            "verbose",
        ]

        # Combined completer
        word_completer = WordCompleter(
            commands + levels + presets + list(logging_control._module_levels.keys()),
            ignore_case=True,
        )

        self.session = PromptSession(
            history=FileHistory(self.history_file),
            auto_suggest=AutoSuggestFromHistory(),
            completer=FuzzyCompleter(word_completer),
            complete_while_typing=True,
            enable_history_search=True,
        )

    def _capture_logs(self):
        """Capture logs in real-time for display."""

        class CLILogHandler(logging.Handler):
            def __init__(self, cli):
                super().__init__()
                self.cli = cli

            def emit(self, record):
                # Add to deque
                self.cli.logs.append(record)

                # Update stats
                module = record.name
                level = record.levelname
                self.cli.module_stats[module]["count"] += 1
                self.cli.module_stats[module]["levels"][level] += 1

        # Add handler to root logger
        self.log_handler = CLILogHandler(self)
        logging.getLogger().addHandler(self.log_handler)

    def _remove_log_capture(self):
        """Remove log capture handler."""
        if hasattr(self, "log_handler"):
            logging.getLogger().removeHandler(self.log_handler)

    def _format_log_record(self, record: logging.LogRecord) -> Text:
        """Format a log record with rich colors."""
        if not RICH_AVAILABLE:
            return f"{record.levelname}: {record.name} - {record.getMessage()}"

        # Color based on level
        level_colors = {
            "DEBUG": "dim cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold red on white",
        }

        color = level_colors.get(record.levelname, "white")

        # Create rich text
        text = Text()
        text.append(f"[{record.levelname:8}]", style=color)
        text.append(f" {record.name:30}", style="blue")
        text.append(f" {record.getMessage()}", style="white")

        return text

    def _create_status_table(self) -> Table:
        """Create a status table with current settings."""
        table = Table(title="Logging Configuration Status", box=box.ROUNDED)

        table.add_column("Setting", style="cyan")
        table.add_column("Value", style="green")

        # Global level
        table.add_row("Global Level", logging_control.current_level)

        # Suppressed modules
        suppressed = ", ".join(logging_control._suppressed_modules) or "None"
        table.add_row(
            "Suppressed",
            suppressed[:50] + "..." if len(suppressed) > 50 else suppressed,
        )

        # Filtered modules
        filtered = ", ".join(logging_control._show_only_modules) or "All"
        table.add_row("Filtered", filtered)

        # Module count
        table.add_row("Configured Modules", str(len(logging_control._module_levels)))

        # Recent logs
        if self.logs:
            recent_count = len(
                [l for l in list(self.logs)[-100:] if time.time() - l.created < 60]
            )
            table.add_row("Logs/min", str(recent_count))

        return table

    def _create_module_stats_table(self) -> Table:
        """Create a table showing module statistics."""
        table = Table(title="Module Activity", box=box.ROUNDED)

        table.add_column("Module", style="cyan")
        table.add_column("Total", style="white")
        table.add_column("DEBUG", style="dim cyan")
        table.add_column("INFO", style="green")
        table.add_column("WARN", style="yellow")
        table.add_column("ERROR", style="red")

        # Sort by total count
        sorted_modules = sorted(
            self.module_stats.items(), key=lambda x: x[1]["count"], reverse=True
        )[
            :10
        ]  # Top 10

        for module, stats in sorted_modules:
            table.add_row(
                module[:30] + "..." if len(module) > 30 else module,
                str(stats["count"]),
                str(stats["levels"].get("DEBUG", 0)),
                str(stats["levels"].get("INFO", 0)),
                str(stats["levels"].get("WARNING", 0)),
                str(stats["levels"].get("ERROR", 0)),
            )

        return table

    def show_help(self):
        """Display help information."""
        if RICH_AVAILABLE:
            help_text = """
[bold cyan]Haive Logging CLI Commands[/bold cyan]

[yellow]Basic Commands:[/yellow]
  help              Show this help message
  status            Show current logging configuration
  quit/exit         Exit the CLI

[yellow]Level Control:[/yellow]
  level <LEVEL>     Set global log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
  module <name> <LEVEL>  Set level for specific module

[yellow]Filtering:[/yellow]
  suppress <module>      Suppress logs from module
  unsuppress <module>    Stop suppressing module
  filter <modules...>    Only show logs from specified modules
  clear-filter          Show logs from all modules

[yellow]Presets:[/yellow]
  preset <name>     Apply preset (debug, normal, quiet, silent, haive-only)
  debug             Enable debug mode

[yellow]Monitoring:[/yellow]
  monitor           Start real-time log monitoring
  ui                Launch interactive UI
  dashboard         Launch advanced dashboard
  stats             Show module statistics

[yellow]Advanced:[/yellow]
  trace <module>    Enable detailed tracing for module
  profile           Show performance profiling
  breakpoint <module> <message>  Set log breakpoint
  export <file>     Export logs to file
  test              Generate test logs

[yellow]Tips:[/yellow]
  - Use Tab for auto-completion
  - Use Up/Down arrows for command history
  - Ctrl+C to stop monitoring
  - Type partial commands and hit Tab
            """
            self.console.print(Panel(help_text, title="Help", border_style="blue"))
        else:

    def handle_command(self, command: str) -> bool:
        """Handle a single command.

        Returns:
            bool: True to continue, False to exit
        """
        if not command.strip():
            return True

        parts = command.strip().split()
        cmd = parts[0].lower()
        args = parts[1:]

        try:
            if cmd in ["quit", "exit"]:
                return False

            if cmd == "help":
                self.show_help()

            elif cmd == "status":
                if RICH_AVAILABLE:
                    self.console.print(self._create_status_table())
                else:

            elif cmd == "level" and args:
                level = args[0].upper()
                logging_control.set_level(level)
                self.console.print(f"[green]Set global level to {level}[/green]")

            elif cmd == "module" and len(args) >= 2:
                module_name = args[0]
                level = args[1].upper()
                logging_control.set_module_level(module_name, level)
                self.console.print(f"[green]Set {module_name} to {level}[/green]")

            elif cmd == "suppress" and args:
                for module in args:
                    logging_control.suppress(module)
                self.console.print(f"[yellow]Suppressed: {', '.join(args)}[/yellow]")

            elif cmd == "unsuppress" and args:
                for module in args:
                    if module in logging_control._suppressed_modules:
                        logging_control._suppressed_modules.remove(module)
                        logging_control._configure_logger(module)
                self.console.print(f"[green]Unsuppressed: {', '.join(args)}[/green]")

            elif cmd == "filter" and args:
                logging_control.only_show(args)
                self.console.print(f"[cyan]Filtering to: {', '.join(args)}[/cyan]")

            elif cmd == "clear-filter":
                logging_control.show_all()
                self.console.print(
                    "[green]Cleared filter - showing all modules[/green]"
                )

            elif cmd == "preset" and args:
                preset = args[0]
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
                self.console.print(f"[green]Applied preset: {preset}[/green]")

            elif cmd == "debug":
                if args:
                    # Debug specific modules
                    for module in args:
                        logging_control.set_module_level(module, "DEBUG")
                    self.console.print(
                        f"[cyan]Debug enabled for: {', '.join(args)}[/cyan]"
                    )
                else:
                    logging_control.debug_mode()
                    self.console.print("[cyan]Debug mode enabled[/cyan]")

            elif cmd == "monitor":
                self.monitor_logs()

            elif cmd == "stats":
                if RICH_AVAILABLE:
                    self.console.print(self._create_module_stats_table())

            elif cmd == "trace" and args:
                # Enable detailed tracing
                module = args[0]
                logging_control.set_module_level(module, "DEBUG")
                # Add trace handler
                logger = logging.getLogger(module)
                logger.addHandler(logging.StreamHandler())
                self.console.print(f"[cyan]Tracing enabled for {module}[/cyan]")

            elif cmd == "test":
                self.generate_test_logs()

            elif cmd == "ui":
                self.console.print("[yellow]Launching UI...[/yellow]")
                from haive.core.logging.ui import launch_ui

                launch_ui()

            elif cmd == "dashboard":
                self.console.print("[yellow]Launching dashboard...[/yellow]")
                from haive.core.logging.dashboard import launch_dashboard

                launch_dashboard()

            elif cmd == "export" and args:
                filename = args[0]
                self.export_logs(filename)

            elif cmd == "breakpoint" and len(args) >= 2:
                module = args[0]
                message = " ".join(args[1:])
                self.set_breakpoint(module, message)

            else:
                self.console.print(f"[red]Unknown command: {cmd}[/red]")
                self.console.print("Type 'help' for available commands")

        except Exception as e:
            self.console.print(f"[red]Error: {e}[/red]")

        return True

    def monitor_logs(self):
        """Real-time log monitoring with rich display."""
        if not RICH_AVAILABLE:
            return

        self.console.print("[cyan]Starting log monitor... Press Ctrl+C to stop[/cyan]")

        # Start capturing logs
        self._capture_logs()

        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="status", size=8),
            Layout(name="logs", ratio=1),
        )

        try:
            with Live(layout, refresh_per_second=4, screen=True):
                while True:
                    # Update header
                    layout["header"].update(
                        Panel(
                            f"[bold cyan]Haive Log Monitor[/bold cyan] - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                            box=box.ROUNDED,
                        )
                    )

                    # Update status
                    layout["status"].update(self._create_status_table())

                    # Update logs
                    log_panel = Panel(
                        "\n".join(
                            [
                                self._format_log_record(record).plain
                                for record in list(self.logs)[-20:]  # Last 20 logs
                            ]
                        ),
                        title="Recent Logs",
                        border_style="green",
                        box=box.ROUNDED,
                    )
                    layout["logs"].update(log_panel)

                    time.sleep(0.25)

        except KeyboardInterrupt:
            self.console.print("\n[yellow]Monitoring stopped[/yellow]")
        finally:
            self._remove_log_capture()

    def generate_test_logs(self):
        """Generate test logs for debugging."""
        import random

        modules = [
            "haive.core.engine",
            "haive.core.graph",
            "haive.agents.test",
            "haive.tools.sample",
            "haive.games.example",
        ]

        levels = [
            (logging.DEBUG, "Debug message"),
            (logging.INFO, "Info message"),
            (logging.WARNING, "Warning message"),
            (logging.ERROR, "Error message"),
        ]

        self.console.print("[cyan]Generating test logs...[/cyan]")

        for _ in range(20):
            module = random.choice(modules)
            level, msg = random.choice(levels)
            logger = logging.getLogger(module)
            logger.log(level, f"Test {msg} from {module}")
            time.sleep(0.1)

        self.console.print("[green]Test logs generated[/green]")

    def export_logs(self, filename: str):
        """Export captured logs to file."""
        try:
            with open(filename, "w") as f:
                for record in self.logs:
                    f.write(
                        f"{record.levelname:<8} {record.name:<30} {record.getMessage()}\n"
                    )
            self.console.print(f"[green]Logs exported to {filename}[/green]")
        except Exception as e:
            self.console.print(f"[red]Export failed: {e}[/red]")

    def set_breakpoint(self, module: str, message: str):
        """Set a breakpoint that triggers when specific log message appears."""

        class BreakpointHandler(logging.Handler):
            def emit(self, record):
                if message.lower() in record.getMessage().lower():
                    import pdb

                    pdb.set_trace()

        logger = logging.getLogger(module)
        logger.addHandler(BreakpointHandler())
        self.console.print(
            f"[yellow]Breakpoint set for '{message}' in {module}[/yellow]"
        )

    def run(self):
        """Main CLI loop."""
        if RICH_AVAILABLE:
            self.console.print(
                Panel(
                    "[bold cyan]Haive Interactive Logging CLI[/bold cyan]\n"
                    "Type 'help' for commands, 'quit' to exit",
                    box=box.DOUBLE,
                )
            )
        else:

        # Start log capture
        self._capture_logs()

        try:
            while True:
                try:
                    if PROMPT_TOOLKIT_AVAILABLE and self.session:
                        # Use prompt toolkit
                        command = self.session.prompt(
                            HTML("<ansicyan>haive-log></ansicyan> "),
                            vi_mode=False,
                            enable_open_in_editor=True,
                        )
                    else:
                        # Fallback to basic input
                        command = input("haive-log> ")

                    if not self.handle_command(command):
                        break

                except KeyboardInterrupt:
                    continue
                except EOFError:
                    break

        finally:
            self._remove_log_capture()
            if RICH_AVAILABLE:
                self.console.print("\n[yellow]Goodbye![/yellow]")


def main():
    """Main entry point."""
    cli = InteractiveLoggingCLI()
    cli.run()


if __name__ == "__main__":
    main()
