#!/usr/bin/env python3
"""
Rich Terminal UI for monitoring Haive package documentation builds
Features: Progress bars, time estimates, build status, live updates
"""

import asyncio
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    from rich.align import Align
    from rich.box import ROUNDED
    from rich.columns import Columns
    from rich.console import Console
    from rich.layout import Layout
    from rich.live import Live
    from rich.panel import Panel
    from rich.progress import (
        BarColumn,
        Progress,
        SpinnerColumn,
        TaskProgressColumn,
        TextColumn,
        TimeElapsedColumn,
        TimeRemainingColumn,
    )
    from rich.table import Table
    from rich.text import Text
except ImportError:
    print("❌ Missing dependencies. Install with:")
    print("pip install rich")
    sys.exit(1)


class PackageBuildMonitor:
    """Monitor documentation builds for Haive packages with rich UI"""

    def __init__(self):
        self.console = Console()
        self.packages = ["hap", "tools", "mcp", "dataflow", "games", "agents"]

        # Build time estimates in minutes (based on package complexity)
        self.time_estimates = {
            "hap": 3,  # Smallest
            "tools": 4,  # Small
            "mcp": 6,  # Medium (1900+ servers)
            "dataflow": 5,  # Medium
            "games": 8,  # Large (19+ games)
            "agents": 12,  # Largest (memory system)
        }

        # Package info
        self.package_info = {
            "hap": {"emoji": "🏗️", "desc": "Agent Orchestration", "priority": 1},
            "tools": {"emoji": "🛠️", "desc": "Tool Integrations", "priority": 2},
            "mcp": {"emoji": "📦", "desc": "1900+ MCP Servers", "priority": 3},
            "dataflow": {"emoji": "🌊", "desc": "Stream Processing", "priority": 4},
            "games": {"emoji": "🎮", "desc": "19+ Game Environments", "priority": 5},
            "agents": {"emoji": "🤖", "desc": "Dynamic Agents", "priority": 6},
        }

        # Build states
        self.build_states = {}
        self.start_times = {}
        self.processes = {}

        # Initialize states
        for pkg in self.packages:
            self.build_states[pkg] = "waiting"
            self.start_times[pkg] = None

    def get_build_status(self, package: str) -> Tuple[str, str, str]:
        """Get build status with color and icon"""
        state = self.build_states[package]

        if state == "waiting":
            return "⏳", "yellow", "Waiting"
        elif state == "building":
            return "🔨", "blue", "Building"
        elif state == "completed":
            return "✅", "green", "Completed"
        elif state == "failed":
            return "❌", "red", "Failed"
        elif state == "timeout":
            return "⏰", "orange3", "Timeout"
        else:
            return "❓", "white", "Unknown"

    def calculate_eta(self, package: str) -> str:
        """Calculate ETA for package build"""
        if self.build_states[package] not in ["building"]:
            return "N/A"

        if self.start_times[package] is None:
            return "N/A"

        elapsed = time.time() - self.start_times[package]
        estimated_total = self.time_estimates[package] * 60  # Convert to seconds

        if elapsed >= estimated_total:
            return "Soon..."

        remaining = estimated_total - elapsed
        return f"{remaining/60:.1f}m"

    def get_elapsed_time(self, package: str) -> str:
        """Get elapsed time for package"""
        if self.start_times[package] is None:
            return "0:00"

        elapsed = time.time() - self.start_times[package]
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        return f"{minutes}:{seconds:02d}"

    def check_build_completion(self, package: str) -> bool:
        """Check if build is completed by looking for index.html"""
        build_path = Path(f"packages/haive-{package}/docs/build/html/index.html")
        return build_path.exists()

    def get_build_size(self, package: str) -> str:
        """Get build directory size"""
        build_dir = Path(f"packages/haive-{package}/docs/build/html/")
        if not build_dir.exists():
            return "N/A"

        try:
            result = subprocess.run(
                ["du", "-sh", str(build_dir)], capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                return result.stdout.split()[0]
        except:
            pass
        return "N/A"

    def count_html_files(self, package: str) -> str:
        """Count HTML files in build"""
        build_dir = Path(f"packages/haive-{package}/docs/build/html/")
        if not build_dir.exists():
            return "0"

        try:
            html_files = list(build_dir.rglob("*.html"))
            return str(len(html_files))
        except:
            return "0"

    def create_header_panel(self) -> Panel:
        """Create the header panel with overall status"""
        current_time = datetime.now().strftime("%H:%M:%S")

        # Count states
        waiting = sum(1 for s in self.build_states.values() if s == "waiting")
        building = sum(1 for s in self.build_states.values() if s == "building")
        completed = sum(1 for s in self.build_states.values() if s == "completed")
        failed = sum(1 for s in self.build_states.values() if s == "failed")

        total_estimated = sum(self.time_estimates.values())

        header_text = Text.assemble(
            ("🚀 Haive Documentation Build Monitor", "bold blue"),
            ("\n"),
            (f"⏰ {current_time} | ", "dim"),
            (f"📦 {len(self.packages)} packages | ", "dim"),
            (f"⌛ ~{total_estimated}m estimated", "dim"),
            ("\n"),
            (f"⏳ {waiting} waiting | ", "yellow"),
            (f"🔨 {building} building | ", "blue"),
            (f"✅ {completed} completed | ", "green"),
            (f"❌ {failed} failed", "red"),
        )

        return Panel(
            Align.center(header_text),
            title="[bold]Haive Package Builds[/bold]",
            border_style="blue",
            box=ROUNDED,
        )

    def create_progress_table(self) -> Table:
        """Create the main progress table"""
        table = Table(show_header=True, header_style="bold blue", box=ROUNDED)

        table.add_column("📦 Package", style="bold", width=12)
        table.add_column("Status", justify="center", width=10)
        table.add_column("Progress", width=20)
        table.add_column("ETA", justify="center", width=8)
        table.add_column("Elapsed", justify="center", width=8)
        table.add_column("Size", justify="center", width=8)
        table.add_column("Files", justify="center", width=6)
        table.add_column("Description", width=20)

        for pkg in self.packages:
            icon, color, status_text = self.get_build_status(pkg)
            info = self.package_info[pkg]

            # Progress bar
            if self.build_states[pkg] == "building":
                if self.start_times[pkg]:
                    elapsed = time.time() - self.start_times[pkg]
                    estimated = self.time_estimates[pkg] * 60
                    progress = min(elapsed / estimated * 100, 99)
                    progress_bar = f"[blue]{'█' * int(progress/5)}{'░' * (20-int(progress/5))}[/blue] {progress:.0f}%"
                else:
                    progress_bar = "[blue]░░░░░░░░░░░░░░░░░░░░[/blue] 0%"
            elif self.build_states[pkg] == "completed":
                progress_bar = "[green]████████████████████[/green] 100%"
            elif self.build_states[pkg] == "failed":
                progress_bar = "[red]████████████████████[/red] ERROR"
            else:
                progress_bar = "[dim]░░░░░░░░░░░░░░░░░░░░[/dim] 0%"

            table.add_row(
                f"{info['emoji']} haive-{pkg}",
                f"[{color}]{icon} {status_text}[/{color}]",
                progress_bar,
                self.calculate_eta(pkg),
                self.get_elapsed_time(pkg),
                self.get_build_size(pkg),
                self.count_html_files(pkg),
                f"[dim]{info['desc']}[/dim]",
            )

        return table

    def create_stats_panel(self) -> Panel:
        """Create statistics panel"""
        total_elapsed = 0
        total_estimated = sum(self.time_estimates.values()) * 60

        for pkg in self.packages:
            if self.start_times[pkg]:
                if self.build_states[pkg] == "completed":
                    # Use estimated time for completed
                    total_elapsed += self.time_estimates[pkg] * 60
                elif self.build_states[pkg] == "building":
                    total_elapsed += time.time() - self.start_times[pkg]

        stats_text = Text.assemble(
            ("📊 Build Statistics", "bold cyan"),
            ("\n"),
            (f"⏱️  Total Estimated: {total_estimated/60:.1f} minutes", "dim"),
            ("\n"),
            (f"⏰ Total Elapsed: {total_elapsed/60:.1f} minutes", "dim"),
            ("\n"),
            (
                f"🎯 Efficiency: {(total_elapsed/total_estimated*100):.1f}% of estimated",
                "dim",
            ),
        )

        return Panel(stats_text, title="Stats", border_style="cyan")

    def create_controls_panel(self) -> Panel:
        """Create controls panel"""
        controls_text = Text.assemble(
            ("⌨️  Controls", "bold yellow"),
            ("\n"),
            ("Ctrl+C: Stop monitoring", "dim"),
            ("\n"),
            ("Builds run automatically in order", "dim"),
            ("\n"),
            ("View logs: tail -f /tmp/build_*.log", "dim"),
        )

        return Panel(controls_text, title="Controls", border_style="yellow")

    def create_layout(self) -> Layout:
        """Create the main layout"""
        layout = Layout()

        layout.split_column(
            Layout(self.create_header_panel(), size=6, name="header"),
            Layout(self.create_progress_table(), name="main"),
            Layout(name="bottom", size=8),
        )

        layout["bottom"].split_row(
            Layout(self.create_stats_panel(), name="stats"),
            Layout(self.create_controls_panel(), name="controls"),
        )

        return layout

    async def start_build(self, package: str):
        """Start building a package"""
        self.console.print(f"🚀 Starting build for haive-{package}...")

        self.build_states[package] = "building"
        self.start_times[package] = time.time()

        # Start build process
        cmd = f"./scripts/build_package_docs.sh {package}"
        log_file = f"/tmp/build_{package}.log"

        try:
            process = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
                cwd=".",
            )

            self.processes[package] = process

            # Monitor the process
            stdout, _ = await asyncio.wait_for(
                process.communicate(), timeout=600
            )  # 10 min timeout

            if process.returncode == 0:
                self.build_states[package] = "completed"
                self.console.print(f"✅ haive-{package} completed successfully!")
            else:
                self.build_states[package] = "failed"
                self.console.print(f"❌ haive-{package} build failed!")

        except asyncio.TimeoutError:
            self.build_states[package] = "timeout"
            if package in self.processes:
                self.processes[package].terminate()
            self.console.print(f"⏰ haive-{package} build timed out!")

        except Exception as e:
            self.build_states[package] = "failed"
            self.console.print(f"❌ haive-{package} error: {e}")

    async def run_sequential_builds(self):
        """Run builds sequentially"""
        for package in self.packages:
            if self.build_states[package] == "waiting":
                await self.start_build(package)
                # Small delay between builds
                await asyncio.sleep(2)

    async def monitor_builds(self):
        """Main monitoring loop with live UI"""

        # Start the builds in background
        build_task = asyncio.create_task(self.run_sequential_builds())

        # Create live display
        with Live(self.create_layout(), refresh_per_second=2, screen=True) as live:
            try:
                while not build_task.done():
                    live.update(self.create_layout())
                    await asyncio.sleep(0.5)

                    # Check if all builds are done
                    all_done = all(
                        state in ["completed", "failed", "timeout"]
                        for state in self.build_states.values()
                    )

                    if all_done:
                        break

                # Final update
                live.update(self.create_layout())
                await asyncio.sleep(2)

            except KeyboardInterrupt:
                self.console.print("\n🛑 Build monitoring stopped by user")
                # Cancel builds
                for process in self.processes.values():
                    if process and process.returncode is None:
                        process.terminate()
                build_task.cancel()

        # Final summary
        self.show_final_summary()

    def show_final_summary(self):
        """Show final build summary"""
        self.console.print("\n" + "=" * 80)
        self.console.print("🏁 [bold]Build Summary[/bold]")
        self.console.print("=" * 80)

        for pkg in self.packages:
            icon, color, status = self.get_build_status(pkg)
            elapsed = self.get_elapsed_time(pkg)
            size = self.get_build_size(pkg)
            files = self.count_html_files(pkg)

            self.console.print(
                f"{icon} [bold]haive-{pkg}[/bold]: "
                f"[{color}]{status}[/{color}] | "
                f"Time: {elapsed} | "
                f"Size: {size} | "
                f"Files: {files}"
            )

        completed = sum(1 for s in self.build_states.values() if s == "completed")
        self.console.print(
            f"\n✅ {completed}/{len(self.packages)} packages completed successfully"
        )

        if completed > 0:
            self.console.print("\n🌐 [bold]View Documentation:[/bold]")
            for pkg in self.packages:
                if self.build_states[pkg] == "completed":
                    path = f"packages/haive-{pkg}/docs/build/html/"
                    self.console.print(
                        f"   • haive-{pkg}: [blue]file://{os.path.abspath(path)}index.html[/blue]"
                    )


async def main():
    """Main entry point"""
    monitor = PackageBuildMonitor()

    # Check if we're in the right directory
    if not Path("packages").exists():
        print("❌ Run this script from the Haive project root directory")
        sys.exit(1)

    # Check if build script exists
    if not Path("scripts/build_package_docs.sh").exists():
        print("❌ Build script not found: scripts/build_package_docs.sh")
        sys.exit(1)

    await monitor.monitor_builds()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Build monitoring stopped")
    except Exception as e:
        print(f"❌ Error: {e}")
