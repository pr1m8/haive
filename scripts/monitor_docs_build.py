#!/usr/bin/env python3
"""Live monitoring dashboard for Sphinx documentation builds.

This script watches the build monitor JSON file and displays a live
updating dashboard of the build progress.
"""
from __future__ import annotations

import argparse
import curses
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any
from typing import Dict
from typing import Optional


class BuildDashboard:
    """Terminal dashboard for monitoring Sphinx builds."""

    def __init__(self, monitor_file: Path):
        self.monitor_file = monitor_file
        self.last_data: dict[str, Any] | None = None
        self.start_time = time.time()

    def load_monitor_data(self) -> dict[str, Any] | None:
        """Load the latest monitor data."""
        try:
            if self.monitor_file.exists():
                with open(self.monitor_file) as f:
                    return json.load(f)
        except:
            pass
        return None

    def format_duration(self, seconds: float) -> str:
        """Format duration in human-readable format."""
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            secs = seconds % 60
            return f"{minutes}m {secs:.0f}s"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours}h {minutes}m"

    def draw_progress_bar(
        self, stdscr, y: int, x: int, progress: float, width: int = 50,
    ):
        """Draw a progress bar."""
        filled = int(width * (progress / 100))
        empty = width - filled

        bar = '█' * filled + '░' * empty
        percentage = f"{progress:.1f}%"

        # Draw bar
        stdscr.addstr(y, x, '[')
        stdscr.addstr(y, x + 1, bar[:filled], curses.color_pair(2))  # Green
        stdscr.addstr(y, x + 1 + filled, bar[filled:])
        stdscr.addstr(y, x + width + 1, '] ' + percentage)

    def draw_dashboard(self, stdscr):
        """Draw the monitoring dashboard."""
        curses.curs_set(0)  # Hide cursor
        stdscr.nodelay(1)  # Non-blocking input

        # Set up colors
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)

        while True:
            stdscr.clear()
            height, width = stdscr.getmaxyx()

            # Load latest data
            data = self.load_monitor_data()
            if not data:
                stdscr.addstr(
                    height // 2, width // 2 - 15, 'Waiting for build to start...',
                )
                stdscr.refresh()
                time.sleep(0.5)

                # Check for quit
                key = stdscr.getch()
                if key == ord('q'):
                    break
                continue

            # Header
            title = '📊 SPHINX BUILD MONITOR'
            stdscr.addstr(
                0,
                width // 2 - len(title) // 2,
                title,
                curses.color_pair(1) | curses.A_BOLD,
            )
            stdscr.addstr(1, 0, '─' * width)

            # Overall progress
            y = 3
            duration = data.get('total_duration', 0)
            stages = data.get('stages', {})
            completed = stages.get('completed', 0)
            total = stages.get('total', 1)
            overall_progress = (completed / total) * 100 if total > 0 else 0

            stdscr.addstr(y, 2, 'Overall Progress:', curses.A_BOLD)
            self.draw_progress_bar(stdscr, y, 20, overall_progress)
            stdscr.addstr(y, 75, f"Time: {self.format_duration(duration)}")

            # Current stage
            y += 2
            current_stage = data.get('current_stage', 'Unknown')
            stage_details = data.get('stage_details', {})

            if current_stage and current_stage in stage_details:
                stage = stage_details[current_stage]
                stdscr.addstr(y, 2, 'Current Stage:', curses.A_BOLD)
                stdscr.addstr(y, 20, stage['description'], curses.color_pair(3))

                if stage['progress_percent'] > 0:
                    y += 1
                    self.draw_progress_bar(stdscr, y, 20, stage['progress_percent'])
                    stdscr.addstr(y, 75, f"{stage['progress']}/{stage['total']}")

                if stage.get('current_item'):
                    y += 1
                    item = stage['current_item']
                    if len(item) > width - 25:
                        item = '...' + item[-(width - 28):]
                    stdscr.addstr(y, 20, f"Processing: {item}", curses.A_DIM)

            # Stage list
            y += 3
            stdscr.addstr(y, 2, 'Stages:', curses.A_BOLD)
            y += 1

            for name, stage in stage_details.items():
                if y >= height - 5:
                    break

                # Status icon
                status_icons = {
                    'success': ('✅', curses.color_pair(2)),
                    'failed': ('❌', curses.color_pair(4)),
                    'running': ('🔄', curses.color_pair(3)),
                    'pending': ('⏳', curses.A_DIM),
                }
                icon, color = status_icons.get(stage['status'], ('❓', curses.A_NORMAL))

                stdscr.addstr(y, 4, icon)
                stdscr.addstr(y, 7, f"{stage['description']:<40}", color)

                if stage['status'] in ['success', 'failed']:
                    stdscr.addstr(y, 50, f"{stage['duration']:.1f}s")
                elif stage['status'] == 'running':
                    stdscr.addstr(
                        y, 50, f"{stage['progress_percent']:.1f}%", curses.color_pair(
                            3),
                    )

                # Errors/warnings
                if stage['errors'] > 0:
                    stdscr.addstr(y, 60, f"❌ {stage['errors']}", curses.color_pair(4))
                if stage['warnings'] > 0:
                    stdscr.addstr(
                        y, 70, f"⚠️  {stage['warnings']}", curses.color_pair(3),
                    )

                y += 1

            # File statistics
            y = height - 8
            stdscr.addstr(y, 0, '─' * width)
            y += 1

            files = data.get('files', {})
            if files.get('by_type'):
                stdscr.addstr(y, 2, 'Files Processed:', curses.A_BOLD)
                x_offset = 20
                for file_type, count in sorted(files['by_type'].items())[:4]:
                    if x_offset + 20 < width:
                        stdscr.addstr(y, x_offset, f"{file_type}: {count}")
                        x_offset += 20

            # Instructions
            y = height - 2
            stdscr.addstr(y, 0, '─' * width)
            stdscr.addstr(
                y + 1, 2, "Press 'q' to quit | Updates every 0.5s", curses.A_DIM,
            )

            # Refresh
            stdscr.refresh()

            # Check for quit
            key = stdscr.getch()
            if key == ord('q'):
                break

            time.sleep(0.5)

    def run_simple_monitor(self):
        """Run a simple text-based monitor (no curses)."""
        print('📊 SPHINX BUILD MONITOR')
        print('=' * 80)
        print(f"Monitoring: {self.monitor_file}")
        print('Press Ctrl+C to quit\n')

        last_stage = None

        try:
            while True:
                data = self.load_monitor_data()
                if not data:
                    print('Waiting for build to start...', end='\r')
                    time.sleep(1)
                    continue

                current_stage = data.get('current_stage')
                stage_details = data.get('stage_details', {})

                # Update when stage changes
                if current_stage != last_stage:
                    last_stage = current_stage
                    print()  # New line

                    if current_stage and current_stage in stage_details:
                        stage = stage_details[current_stage]
                        print(f"▶️  {stage['description']}")

                # Show progress
                if current_stage and current_stage in stage_details:
                    stage = stage_details[current_stage]
                    if stage['total'] > 0:
                        progress = f"{stage['progress']}/{stage['total']} ({stage['progress_percent']:.1f}%)"
                        print(
                            f"   {progress:<30} {stage.get('current_item', '')[:50]:<50}",
                            end='\r',
                        )

                time.sleep(0.5)

        except KeyboardInterrupt:
            print('\n\nMonitoring stopped.')

            # Print final summary
            data = self.load_monitor_data()
            if data:
                print('\n📊 Final Summary:')
                print(f"Total Duration: {data.get('total_duration', 0):.1f}s")

                files = data.get('files', {})
                print(f"Files Processed: {files.get('total', 0)}")

                # Stage summary
                print('\nStages:')
                for name, stage in data.get('stage_details', {}).items():
                    status = (
                        '✅'
                        if stage['status'] == 'success'
                        else '❌' if stage['status'] == 'failed' else '⏳'
                    )
                    print(
                        f"  {status} {stage['description']:<40} {stage.get('duration', 0):.1f}s",
                    )


def find_latest_monitor_file(log_dir: Path) -> Path | None:
    """Find the most recent monitor file."""
    monitor_files = list(log_dir.glob('build_monitor_*.json'))
    if monitor_files:
        return max(monitor_files, key=lambda f: f.stat().st_mtime)
    return None


def main():
    parser = argparse.ArgumentParser(
        description='Monitor Sphinx documentation build progress',
    )
    parser.add_argument('monitor_file', nargs='?', help='Path to monitor JSON file')
    parser.add_argument(
        '--simple', action='store_true', help='Use simple text output (no curses)',
    )
    parser.add_argument(
        '--log-dir',
        default='docs/logs/build',
        help='Log directory to search for monitor files',
    )

    args = parser.parse_args()

    # Find monitor file
    if args.monitor_file:
        monitor_file = Path(args.monitor_file)
    else:
        log_dir = Path(args.log_dir)
        monitor_file = find_latest_monitor_file(log_dir)
        if not monitor_file:
            print(f"No monitor files found in {log_dir}")
            print('Start a documentation build first with monitoring enabled.')
            sys.exit(1)

    # Create dashboard
    dashboard = BuildDashboard(monitor_file)

    # Run monitor
    if args.simple or not sys.stdout.isatty():
        dashboard.run_simple_monitor()
    else:
        try:
            curses.wrapper(dashboard.draw_dashboard)
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(f"Error running curses dashboard: {e}")
            print('Falling back to simple monitor...')
            dashboard.run_simple_monitor()


if __name__ == '__main__':
    main()
