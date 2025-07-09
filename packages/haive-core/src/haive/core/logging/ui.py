"""
Interactive Rich UI for Haive Logging Control

This module provides a beautiful, interactive terminal UI for controlling
logging in real-time using Rich's Live display and keyboard input.
"""

import logging
import threading
import time
from datetime import datetime
from typing import List, Optional, Tuple

from rich import box
from rich.align import Align
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from haive.core.logging.control import logging_control

# Try to import keyboard handling
try:
    import readchar

    READCHAR_AVAILABLE = True
except ImportError:
    READCHAR_AVAILABLE = False
    print("Warning: readchar not available. Install with: pip install readchar")


class LoggingUI:
    """
    Interactive Rich UI for logging control.

    Provides a real-time dashboard for:
    - Viewing current logging configuration
    - Changing log levels interactively
    - Filtering modules
    - Monitoring log output
    """

    def __init__(self):
        """Initialize the UI."""
        self.console = Console()
        self.running = False
        self.selected_menu = 0
        self.selected_module = 0
        self.show_logs = True
        self.log_buffer: List[Tuple[str, str, str]] = []  # (time, level, message)
        self.max_log_lines = 20

        # Menu options
        self.menu_items = [
            ("1", "Set Global Level", self.set_global_level),
            ("2", "Module Levels", self.module_levels_menu),
            ("3", "Quick Presets", self.quick_presets_menu),
            ("4", "Suppress Modules", self.suppress_menu),
            ("5", "Filter Modules", self.filter_menu),
            ("6", "Toggle Log View", self.toggle_logs),
            ("7", "Save Config", self.save_config),
            ("8", "Clear Logs", self.clear_logs),
            ("q", "Quit", self.quit),
        ]

        # Capture logs
        self._setup_log_capture()

    def _setup_log_capture(self):
        """Set up a handler to capture log messages."""

        class UILogHandler(logging.Handler):
            def __init__(self, ui):
                super().__init__()
                self.ui = ui

            def emit(self, record):
                try:
                    # Format the message
                    msg = self.format(record)
                    level = record.levelname
                    timestamp = datetime.now().strftime("%H:%M:%S")

                    # Add to buffer
                    self.ui.log_buffer.append((timestamp, level, msg))

                    # Keep buffer size limited
                    if len(self.ui.log_buffer) > self.ui.max_log_lines:
                        self.ui.log_buffer.pop(0)

                except Exception:
                    self.handleError(record)

        # Add handler to root logger
        self.ui_handler = UILogHandler(self)
        self.ui_handler.setFormatter(logging.Formatter("%(name)s - %(message)s"))
        logging.getLogger().addHandler(self.ui_handler)

    def create_layout(self) -> Layout:
        """Create the UI layout."""
        layout = Layout()

        # Main layout structure
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body"),
            Layout(name="footer", size=3),
        )

        # Split body into config and logs
        layout["body"].split_row(
            Layout(name="config", ratio=2),
            (
                Layout(name="logs", ratio=3)
                if self.show_logs
                else Layout(name="empty", ratio=3)
            ),
        )

        # Split config into menu and status
        layout["body"]["config"].split_column(
            Layout(name="menu", ratio=1), Layout(name="status", ratio=2)
        )

        return layout

    def render_header(self) -> Panel:
        """Render the header."""
        title = Text()
        title.append("🎮 ", style="bright_yellow")
        title.append("HAIVE LOGGING CONTROL", style="bold bright_blue")
        title.append(" 🎮", style="bright_yellow")

        return Panel(Align.center(title), border_style="bright_blue", box=box.DOUBLE)

    def render_menu(self) -> Panel:
        """Render the menu."""
        menu_text = Text()

        for i, (key, label, _) in enumerate(self.menu_items):
            if i == self.selected_menu:
                menu_text.append(f"▶ [{key}] {label}\n", style="bold bright_cyan")
            else:
                menu_text.append(f"  [{key}] {label}\n", style="dim white")

        return Panel(menu_text, title="[bold]Menu[/bold]", border_style="cyan")

    def render_status(self) -> Panel:
        """Render the current status."""
        # Create status table
        table = Table(show_header=False, box=None, padding=0)
        table.add_column("Key", style="cyan")
        table.add_column("Value", style="yellow")

        # Global level
        table.add_row(
            "Global Level:", logging.getLevelName(logging_control._global_level)
        )

        # Module levels
        if logging_control._module_levels:
            modules_text = Text()
            for module, level in sorted(logging_control._module_levels.items()):
                modules_text.append(f"{module}: {logging.getLevelName(level)}\n")
            table.add_row("Module Levels:", modules_text)

        # Suppressed modules
        if logging_control._suppressed_modules:
            suppressed = ", ".join(sorted(logging_control._suppressed_modules)[:5])
            if len(logging_control._suppressed_modules) > 5:
                suppressed += f" (+{len(logging_control._suppressed_modules) - 5} more)"
            table.add_row("Suppressed:", suppressed)

        # Filter mode
        if logging_control._allowed_modules:
            allowed = ", ".join(sorted(logging_control._allowed_modules))
            table.add_row("Filter:", allowed)

        return Panel(
            table, title="[bold]Current Configuration[/bold]", border_style="green"
        )

    def render_logs(self) -> Panel:
        """Render the log output."""
        if not self.show_logs:
            return Panel(
                Align.center(Text("Logs hidden - press 6 to show", style="dim")),
                title="[bold]Logs[/bold]",
                border_style="yellow",
            )

        # Create log display
        log_lines = []

        for timestamp, level, message in self.log_buffer:
            # Color based on level
            level_colors = {
                "DEBUG": "dim cyan",
                "INFO": "bright_blue",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold red on white",
            }

            color = level_colors.get(level, "white")

            line = Text()
            line.append(f"{timestamp} ", style="dim white")
            line.append(f"[{level:>8}] ", style=color)
            line.append(message, style="white")

            log_lines.append(line)

        if not log_lines:
            log_lines.append(Text("No logs yet...", style="dim"))

        # Combine lines
        log_text = Text("\n").join(log_lines)

        return Panel(
            log_text,
            title=f"[bold]Live Logs ({len(self.log_buffer)}/{self.max_log_lines})[/bold]",
            border_style="yellow",
        )

    def render_footer(self) -> Panel:
        """Render the footer."""
        footer_text = Text()
        footer_text.append("Navigation: ", style="dim")
        footer_text.append("↑↓", style="bright_cyan")
        footer_text.append(" Select  ", style="dim")
        footer_text.append("Enter", style="bright_cyan")
        footer_text.append(" Execute  ", style="dim")
        footer_text.append("1-8", style="bright_cyan")
        footer_text.append(" Quick Select  ", style="dim")
        footer_text.append("q", style="bright_red")
        footer_text.append(" Quit", style="dim")

        return Panel(Align.center(footer_text), border_style="dim")

    def set_global_level(self):
        """Interactive global level setting."""
        self.console.clear()
        self.console.print("[bold cyan]Select Global Log Level:[/bold cyan]\n")

        levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL", "SILENT"]
        for i, level in enumerate(levels):
            self.console.print(f"  {i+1}. {level}")

        self.console.print("\nPress number to select or 'c' to cancel: ", end="")

        if READCHAR_AVAILABLE:
            key = readchar.readkey()
            if key in "123456":
                idx = int(key) - 1
                if idx < len(levels):
                    level = levels[idx]
                    if level == "SILENT":
                        logging_control.set_level(logging.CRITICAL + 1)
                    else:
                        logging_control.set_level(level)
                    self.console.print(f"\n✅ Set global level to {level}")
                    time.sleep(1)

    def module_levels_menu(self):
        """Interactive module level setting."""
        self.console.clear()
        self.console.print("[bold cyan]Module Level Configuration[/bold cyan]\n")
        self.console.print("Enter module name (e.g., haive.core.engine): ", end="")

        # Simple input (would need proper implementation)
        module = "haive.core.engine"  # Placeholder

        self.console.print(f"\nSelect level for {module}:")
        levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        for i, level in enumerate(levels):
            self.console.print(f"  {i+1}. {level}")

        if READCHAR_AVAILABLE:
            key = readchar.readkey()
            if key in "12345":
                idx = int(key) - 1
                if idx < len(levels):
                    level = levels[idx]
                    logging_control.set_module_level(module, level)
                    self.console.print(f"\n✅ Set {module} to {level}")
                    time.sleep(1)

    def quick_presets_menu(self):
        """Quick presets menu."""
        self.console.clear()
        self.console.print("[bold cyan]Quick Presets:[/bold cyan]\n")

        presets = [
            ("debug", "Debug mode - Show all debug messages"),
            ("normal", "Normal mode - INFO level + suppress third-party"),
            ("quiet", "Quiet mode - Only warnings and above"),
            ("silent", "Silent mode - Critical only"),
            ("haive-only", "Haive only - Show only haive logs"),
        ]

        for i, (preset, desc) in enumerate(presets):
            self.console.print(f"  {i+1}. {preset:<12} - {desc}")

        self.console.print("\nPress number to select or 'c' to cancel: ", end="")

        if READCHAR_AVAILABLE:
            key = readchar.readkey()
            if key in "12345":
                idx = int(key) - 1
                if idx < len(presets):
                    preset_name = presets[idx][0]
                    logging_control.quick_setup(preset_name)
                    self.console.print(f"\n✅ Applied preset: {preset_name}")
                    time.sleep(1)

    def suppress_menu(self):
        """Suppress modules menu."""
        self.console.clear()
        self.console.print("[bold cyan]Suppress Modules:[/bold cyan]\n")
        self.console.print("1. Suppress all third-party modules")
        self.console.print("2. Suppress specific module")
        self.console.print("3. Unsuppress module")
        self.console.print("4. Clear all suppressions")

        if READCHAR_AVAILABLE:
            key = readchar.readkey()
            if key == "1":
                logging_control.suppress_third_party()
                self.console.print("\n✅ Suppressed all third-party modules")
                time.sleep(1)

    def filter_menu(self):
        """Filter modules menu."""
        self.console.clear()
        self.console.print("[bold cyan]Filter Modules:[/bold cyan]\n")
        self.console.print("1. Show only haive modules")
        self.console.print("2. Show only specific modules")
        self.console.print("3. Show all modules (remove filter)")

        if READCHAR_AVAILABLE:
            key = readchar.readkey()
            if key == "1":
                logging_control.only_show(["haive"])
                self.console.print("\n✅ Showing only haive modules")
                time.sleep(1)
            elif key == "3":
                logging_control.show_all()
                self.console.print("\n✅ Showing all modules")
                time.sleep(1)

    def toggle_logs(self):
        """Toggle log display."""
        self.show_logs = not self.show_logs

    def save_config(self):
        """Save current configuration."""
        logging_control.save_config()
        self.console.print("\n✅ Configuration saved!")
        time.sleep(1)

    def clear_logs(self):
        """Clear log buffer."""
        self.log_buffer.clear()

    def quit(self):
        """Quit the UI."""
        self.running = False

    def handle_input(self, key: str):
        """Handle keyboard input."""
        # Direct menu selection
        for _i, (menu_key, _, action) in enumerate(self.menu_items):
            if key == menu_key:
                action()
                return

        # Navigation
        if key == "\x1b[A":  # Up arrow
            self.selected_menu = max(0, self.selected_menu - 1)
        elif key == "\x1b[B":  # Down arrow
            self.selected_menu = min(len(self.menu_items) - 1, self.selected_menu + 1)
        elif key == "\r":  # Enter
            _, _, action = self.menu_items[self.selected_menu]
            action()

    def run(self):
        """Run the interactive UI."""
        self.running = True

        # Input thread
        def input_thread():
            while self.running:
                if READCHAR_AVAILABLE:
                    try:
                        key = readchar.readkey()
                        self.handle_input(key)
                    except Exception:
                        pass
                else:
                    time.sleep(0.1)

        # Start input thread
        if READCHAR_AVAILABLE:
            input_thread = threading.Thread(target=input_thread, daemon=True)
            input_thread.start()

        # Main render loop
        with Live(
            self.create_layout(), refresh_per_second=4, console=self.console
        ) as live:
            while self.running:
                layout = self.create_layout()

                # Update sections
                layout["header"].update(self.render_header())
                layout["body"]["config"]["menu"].update(self.render_menu())
                layout["body"]["config"]["status"].update(self.render_status())

                if self.show_logs:
                    layout["body"]["logs"].update(self.render_logs())
                else:
                    layout["body"]["logs"] = Layout(self.render_logs())

                layout["footer"].update(self.render_footer())

                live.update(layout)
                time.sleep(0.1)

        # Cleanup
        logging.getLogger().removeHandler(self.ui_handler)
        self.console.clear()
        self.console.print("[bold green]Logging UI closed.[/bold green]")


class LoggingMonitor:
    """
    Simple logging monitor that shows live logs with filtering.
    """

    def __init__(self, filter_modules: Optional[List[str]] = None):
        """Initialize the monitor."""
        self.console = Console()
        self.filter_modules = filter_modules or []
        self.running = False
        self.log_entries = []
        self.max_entries = 100

    def monitor(self, duration: Optional[int] = None):
        """
        Monitor logs for a duration or until interrupted.

        Args:
            duration: Seconds to monitor (None = until interrupted)
        """
        import signal

        def signal_handler(sig, frame):
            self.running = False

        signal.signal(signal.SIGINT, signal_handler)

        self.console.clear()
        self.console.print("[bold cyan]📊 Live Log Monitor[/bold cyan]")
        self.console.print(
            f"Filters: {self.filter_modules if self.filter_modules else 'None'}"
        )
        self.console.print("Press Ctrl+C to stop\n")

        self.running = True
        start_time = time.time()

        # Set up log capture
        class MonitorHandler(logging.Handler):
            def __init__(self, monitor):
                super().__init__()
                self.monitor = monitor

            def emit(self, record):
                # Check filters
                if self.monitor.filter_modules:
                    if not any(
                        record.name.startswith(f) for f in self.monitor.filter_modules
                    ):
                        return

                # Format and display
                level_colors = {
                    "DEBUG": "cyan",
                    "INFO": "blue",
                    "WARNING": "yellow",
                    "ERROR": "red",
                    "CRITICAL": "bold red",
                }

                color = level_colors.get(record.levelname, "white")

                timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]

                self.monitor.console.print(
                    f"[dim]{timestamp}[/dim] "
                    f"[{color}]{record.levelname:>8}[/{color}] "
                    f"[green]{record.name}[/green] - "
                    f"{record.getMessage()}"
                )

        handler = MonitorHandler(self)
        logging.getLogger().addHandler(handler)

        try:
            while self.running:
                if duration and (time.time() - start_time) > duration:
                    break
                time.sleep(0.1)
        finally:
            logging.getLogger().removeHandler(handler)
            self.console.print("\n[bold green]Monitor stopped.[/bold green]")


# Convenience functions
def launch_ui():
    """Launch the interactive logging UI."""
    ui = LoggingUI()
    ui.run()


def monitor_logs(modules: Optional[List[str]] = None, duration: Optional[int] = None):
    """
    Monitor logs with optional filtering.

    Args:
        modules: List of module prefixes to monitor
        duration: How long to monitor (seconds)
    """
    monitor = LoggingMonitor(modules)
    monitor.monitor(duration)


__all__ = ["LoggingUI", "LoggingMonitor", "launch_ui", "monitor_logs"]
