"""
Advanced Logging Dashboard for Haive Framework

This module provides a sophisticated Rich-based dashboard for real-time
logging control and monitoring with advanced features.
"""

import asyncio
import logging
import time
from collections import Counter, deque
from datetime import datetime
from typing import Any, Deque, Dict, List

from rich import box
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from haive.core.logging.control import logging_control

try:
    from prompt_toolkit import prompt
    from prompt_toolkit.completion import WordCompleter

    PROMPT_TOOLKIT_AVAILABLE = True
except ImportError:
    PROMPT_TOOLKIT_AVAILABLE = False


class LoggingDashboard:
    """
    Advanced logging dashboard with real-time monitoring and control.

    Features:
    - Real-time log streaming with filtering
    - Module activity heatmap
    - Log level distribution
    - Performance metrics
    - Interactive configuration
    - Search and filter capabilities
    """

    def __init__(self):
        """Initialize the dashboard."""
        self.console = Console()
        self.running = False

        # Log data structures
        self.log_buffer: Deque[Dict[str, Any]] = deque(maxlen=1000)
        self.filtered_logs: List[Dict[str, Any]] = []
        self.module_activity: Counter = Counter()
        self.level_counts: Counter = Counter()
        self.error_buffer: Deque[Dict[str, Any]] = deque(maxlen=50)

        # UI state
        self.active_panel = "logs"  # logs, config, modules, search
        self.search_query = ""
        self.module_filter = ""
        self.level_filter = None
        self.auto_scroll = True
        self.show_timestamps = True
        self.show_module_path = True

        # Performance tracking
        self.log_rate = 0
        self.last_log_count = 0
        self.last_rate_check = time.time()

        # Set up log capture
        self._setup_log_capture()

    def _setup_log_capture(self):
        """Set up advanced log capture."""

        class DashboardHandler(logging.Handler):
            def __init__(self, dashboard):
                super().__init__()
                self.dashboard = dashboard

            def emit(self, record):
                try:
                    # Create log entry
                    entry = {
                        "timestamp": datetime.now(),
                        "level": record.levelname,
                        "module": record.name,
                        "message": self.format(record),
                        "thread": record.thread,
                        "func": record.funcName,
                        "line": record.lineno,
                        "exc_info": record.exc_info,
                    }

                    # Add to buffer
                    self.dashboard.log_buffer.append(entry)

                    # Update counters
                    self.dashboard.module_activity[record.name] += 1
                    self.dashboard.level_counts[record.levelname] += 1

                    # Track errors
                    if record.levelname in ["ERROR", "CRITICAL"]:
                        self.dashboard.error_buffer.append(entry)

                    # Apply filters
                    self.dashboard._apply_filters()

                except Exception:
                    self.handleError(record)

        self.handler = DashboardHandler(self)
        self.handler.setFormatter(logging.Formatter("%(message)s"))
        logging.getLogger().addHandler(self.handler)

    def _apply_filters(self):
        """Apply current filters to log buffer."""
        self.filtered_logs = []

        for entry in self.log_buffer:
            # Level filter
            if self.level_filter and entry["level"] != self.level_filter:
                continue

            # Module filter
            if self.module_filter and not entry["module"].startswith(
                self.module_filter
            ):
                continue

            # Search filter
            if self.search_query:
                search_lower = self.search_query.lower()
                if (
                    search_lower not in entry["message"].lower()
                    and search_lower not in entry["module"].lower()
                ):
                    continue

            self.filtered_logs.append(entry)

    def create_layout(self) -> Layout:
        """Create the dashboard layout."""
        layout = Layout()

        # Main structure
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body"),
            Layout(name="footer", size=4),
        )

        # Body layout
        layout["body"].split_row(
            Layout(name="main", ratio=3), Layout(name="sidebar", ratio=1)
        )

        # Sidebar sections
        layout["body"]["sidebar"].split_column(
            Layout(name="stats", size=10),
            Layout(name="controls", size=12),
            Layout(name="errors"),
        )

        return layout

    def render_header(self) -> Panel:
        """Render the header with title and stats."""
        # Calculate log rate
        current_time = time.time()
        if current_time - self.last_rate_check > 1:
            log_count = len(self.log_buffer)
            self.log_rate = (log_count - self.last_log_count) / (
                current_time - self.last_rate_check
            )
            self.last_log_count = log_count
            self.last_rate_check = current_time

        header = Table.grid(padding=1)
        header.add_column(style="cyan", justify="center")
        header.add_column(style="yellow", justify="center")
        header.add_column(style="green", justify="center")
        header.add_column(style="magenta", justify="center")

        header.add_row(
            "🚀 HAIVE LOGGING DASHBOARD",
            f"📊 Rate: {self.log_rate:.1f}/s",
            f"📝 Total: {len(self.log_buffer)}",
            f"🔍 Filtered: {len(self.filtered_logs)}",
        )

        return Panel(header, border_style="bright_blue", box=box.DOUBLE)

    def render_main_panel(self) -> Panel:
        """Render the main log display."""
        # Create log table
        log_table = Table(
            show_header=True,
            header_style="bold cyan",
            show_lines=False,
            box=None,
            padding=(0, 1),
        )

        # Columns
        if self.show_timestamps:
            log_table.add_column("Time", style="dim white", width=12)
        log_table.add_column("Level", style="white", width=8)
        if self.show_module_path:
            log_table.add_column("Module", style="green", width=30)
        log_table.add_column("Message", style="white", ratio=1)

        # Add logs (show latest if auto-scroll)
        logs_to_show = (
            self.filtered_logs[-30:] if self.auto_scroll else self.filtered_logs[:30]
        )

        for entry in logs_to_show:
            # Level styling
            level_styles = {
                "DEBUG": "dim cyan",
                "INFO": "bright_blue",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold red on white",
            }
            level_style = level_styles.get(entry["level"], "white")

            row = []
            if self.show_timestamps:
                row.append(entry["timestamp"].strftime("%H:%M:%S.%f")[:-3])
            row.append(Text(entry["level"], style=level_style))
            if self.show_module_path:
                row.append(Text(entry["module"], style="green", overflow="ellipsis"))
            row.append(entry["message"])

            log_table.add_row(*row)

        title = f"📜 Logs ({len(self.filtered_logs)} entries)"
        if self.search_query:
            title += f" | 🔍 '{self.search_query}'"
        if self.module_filter:
            title += f" | 📦 {self.module_filter}"
        if self.level_filter:
            title += f" | ⚡ {self.level_filter}"

        return Panel(log_table, title=title, border_style="yellow", padding=(0, 1))

    def render_stats(self) -> Panel:
        """Render statistics panel."""
        stats = Table(show_header=False, box=None, padding=0)
        stats.add_column("Label", style="cyan")
        stats.add_column("Value", style="yellow")

        # Level distribution
        total_logs = sum(self.level_counts.values())
        for level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            count = self.level_counts.get(level, 0)
            if total_logs > 0:
                percentage = (count / total_logs) * 100
                stats.add_row(f"{level}:", f"{count} ({percentage:.1f}%)")
            else:
                stats.add_row(f"{level}:", "0")

        return Panel(stats, title="📊 Statistics", border_style="green")

    def render_controls(self) -> Panel:
        """Render control panel."""
        controls = Table(show_header=False, box=None, padding=0)
        controls.add_column("Key", style="bright_cyan")
        controls.add_column("Action", style="white")

        controls.add_row("F1", "Filter Level")
        controls.add_row("F2", "Filter Module")
        controls.add_row("F3", "Search")
        controls.add_row("F4", "Clear Filters")
        controls.add_row("F5", "Presets")
        controls.add_row("F6", "Toggle Time")
        controls.add_row("F7", "Toggle Path")
        controls.add_row("F8", "Auto-scroll")
        controls.add_row("F9", "Export Logs")
        controls.add_row("ESC", "Exit")

        return Panel(controls, title="⌨️ Controls", border_style="cyan")

    def render_errors(self) -> Panel:
        """Render recent errors panel."""
        if not self.error_buffer:
            content = Text("No errors ✅", style="green", justify="center")
        else:
            error_list = []
            for error in list(self.error_buffer)[-5:]:
                error_text = Text()
                error_text.append(
                    f"{error['timestamp'].strftime('%H:%M:%S')} ", style="dim"
                )
                error_text.append(f"{error['module']}\n", style="red")
                error_text.append(f"  {error['message'][:50]}...\n", style="white")
                error_list.append(error_text)

            content = Text("\n").join(error_list)

        return Panel(
            content,
            title=f"❌ Recent Errors ({len(self.error_buffer)})",
            border_style="red",
        )

    def render_footer(self) -> Panel:
        """Render footer with current configuration."""
        config_items = []

        # Global level
        config_items.append(
            f"[cyan]Global:[/cyan] {logging.getLevelName(logging_control._global_level)}"
        )

        # Module count
        if logging_control._module_levels:
            config_items.append(
                f"[green]Modules:[/green] {len(logging_control._module_levels)}"
            )

        # Suppressed count
        if logging_control._suppressed_modules:
            config_items.append(
                f"[red]Suppressed:[/red] {len(logging_control._suppressed_modules)}"
            )

        # Active filters
        if logging_control._allowed_modules:
            config_items.append("[yellow]Filter:[/yellow] Active")

        config_text = " | ".join(config_items)

        return Panel(config_text, title="⚙️ Configuration", border_style="dim")

    def handle_key_press(self, key: str):
        """Handle keyboard input."""
        if key == "F1":
            self.show_level_filter_menu()
        elif key == "F2":
            self.show_module_filter_menu()
        elif key == "F3":
            self.show_search_dialog()
        elif key == "F4":
            self.clear_filters()
        elif key == "F5":
            self.show_preset_menu()
        elif key == "F6":
            self.show_timestamps = not self.show_timestamps
        elif key == "F7":
            self.show_module_path = not self.show_module_path
        elif key == "F8":
            self.auto_scroll = not self.auto_scroll
        elif key == "F9":
            self.export_logs()
        elif key in ["q", "ESC"]:
            self.running = False

    def show_level_filter_menu(self):
        """Show level filter menu."""
        if PROMPT_TOOLKIT_AVAILABLE:
            levels = ["ALL", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
            completer = WordCompleter(levels)

            try:
                level = prompt(
                    "Filter by level (ALL to clear): ", completer=completer
                ).upper()

                if level == "ALL":
                    self.level_filter = None
                elif level in levels[1:]:
                    self.level_filter = level

                self._apply_filters()
            except:
                pass

    def show_module_filter_menu(self):
        """Show module filter menu."""
        if PROMPT_TOOLKIT_AVAILABLE:
            # Get unique modules
            modules = list(set(entry["module"] for entry in self.log_buffer))
            completer = WordCompleter(modules)

            try:
                module = prompt(
                    "Filter by module prefix (empty to clear): ", completer=completer
                )

                self.module_filter = module
                self._apply_filters()
            except:
                pass

    def show_search_dialog(self):
        """Show search dialog."""
        if PROMPT_TOOLKIT_AVAILABLE:
            try:
                query = prompt("Search logs: ", default=self.search_query)
                self.search_query = query
                self._apply_filters()
            except:
                pass

    def clear_filters(self):
        """Clear all filters."""
        self.search_query = ""
        self.module_filter = ""
        self.level_filter = None
        self._apply_filters()

    def show_preset_menu(self):
        """Show preset menu."""
        if PROMPT_TOOLKIT_AVAILABLE:
            presets = ["debug", "normal", "quiet", "haive-only", "cancel"]
            completer = WordCompleter(presets)

            try:
                preset = prompt("Select preset: ", completer=completer)

                if preset in presets[:-1]:
                    logging_control.quick_setup(preset)
            except:
                pass

    def export_logs(self):
        """Export logs to file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"haive_logs_{timestamp}.txt"

        with open(filename, "w") as f:
            for entry in self.filtered_logs:
                f.write(
                    f"{entry['timestamp']} [{entry['level']}] "
                    f"{entry['module']} - {entry['message']}\n"
                )

        self.console.print(f"\n✅ Logs exported to {filename}")
        time.sleep(2)

    async def run_async(self):
        """Run the dashboard asynchronously."""
        self.running = True

        with Live(
            self.create_layout(),
            refresh_per_second=10,
            console=self.console,
            screen=True,
        ) as live:
            while self.running:
                layout = self.create_layout()

                # Update all panels
                layout["header"].update(self.render_header())
                layout["body"]["main"].update(self.render_main_panel())
                layout["body"]["sidebar"]["stats"].update(self.render_stats())
                layout["body"]["sidebar"]["controls"].update(self.render_controls())
                layout["body"]["sidebar"]["errors"].update(self.render_errors())
                layout["footer"].update(self.render_footer())

                live.update(layout)

                # Small delay to prevent CPU spinning
                await asyncio.sleep(0.1)

    def run(self):
        """Run the dashboard."""
        try:
            asyncio.run(self.run_async())
        finally:
            # Cleanup
            logging.getLogger().removeHandler(self.handler)
            self.console.clear()


def launch_dashboard():
    """Launch the logging dashboard."""
    dashboard = LoggingDashboard()
    dashboard.run()


# Module activity visualizer
class ModuleActivityVisualizer:
    """Visualize module logging activity as a heatmap."""

    def __init__(self):
        self.console = Console()
        self.activity_data: Dict[str, List[int]] = {}
        self.time_window = 60  # seconds
        self.update_interval = 1  # second

    def visualize(self, duration: int = 60):
        """
        Visualize module activity for a duration.

        Args:
            duration: How long to monitor (seconds)
        """
        import signal

        self.running = True

        def signal_handler(sig, frame):
            self.running = False

        signal.signal(signal.SIGINT, signal_handler)

        # Set up log capture
        class ActivityHandler(logging.Handler):
            def __init__(self, visualizer):
                super().__init__()
                self.visualizer = visualizer

            def emit(self, record):
                module = record.name
                if module not in self.visualizer.activity_data:
                    self.visualizer.activity_data[module] = []

                # Add timestamp
                self.visualizer.activity_data[module].append(time.time())

                # Clean old data
                cutoff = time.time() - self.visualizer.time_window
                self.visualizer.activity_data[module] = [
                    t for t in self.visualizer.activity_data[module] if t > cutoff
                ]

        handler = ActivityHandler(self)
        logging.getLogger().addHandler(handler)

        start_time = time.time()

        try:
            with Live(console=self.console, refresh_per_second=1) as live:
                while self.running and (time.time() - start_time) < duration:
                    # Create heatmap
                    table = Table(
                        title="📊 Module Activity Heatmap",
                        show_header=False,
                        box=box.SIMPLE,
                    )

                    # Sort modules by activity
                    sorted_modules = sorted(
                        self.activity_data.items(),
                        key=lambda x: len(x[1]),
                        reverse=True,
                    )[
                        :20
                    ]  # Top 20

                    for module, timestamps in sorted_modules:
                        # Calculate activity level
                        activity = len(timestamps)

                        # Create bar
                        max_width = 40
                        bar_width = min(int(activity / 10 * max_width), max_width)
                        bar = "█" * bar_width

                        # Color based on activity
                        if activity < 10:
                            color = "green"
                        elif activity < 50:
                            color = "yellow"
                        else:
                            color = "red"

                        table.add_row(
                            Text(module[:40], style="cyan"),
                            Text(bar, style=color),
                            Text(str(activity), style="white"),
                        )

                    live.update(table)
                    time.sleep(self.update_interval)

        finally:
            logging.getLogger().removeHandler(handler)


__all__ = ["LoggingDashboard", "ModuleActivityVisualizer", "launch_dashboard"]
