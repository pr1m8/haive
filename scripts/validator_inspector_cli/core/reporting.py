from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.panel import Panel

console = Console()

# === Constants ===
ROOT_DIR = Path.cwd()
DATA_DIR = ROOT_DIR / 'data'
REPORTS_DIR = DATA_DIR / 'reports'
LOG_FILE = DATA_DIR / 'debug.log'


def setup_report_dirs() -> None:
    """Ensure the data directories exist for logging and report output."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    LOG_FILE.touch(exist_ok=True)


def log_debug(message: str) -> None:
    """Append a debug message to the log file with a timestamp."""
    timestamp = datetime.now().isoformat()
    with LOG_FILE.open('a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] {message}\n")


def write_report(filepath: str, issues: list[tuple[str, str]]) -> None:
    """Save a JSON report of issues discovered in a file to the reports
    directory.

    The path is flattened to be filesystem-safe.
    """
    try:
        rel_path = os.path.relpath(filepath, start=ROOT_DIR)
    except ValueError:
        # In case relpath fails (e.g., different drive), fallback to absolute
        rel_path = Path(filepath).resolve().as_posix()

    safe_filename = rel_path.replace('/', '__').replace('\\', '__') + '.json'
    report_path = REPORTS_DIR / safe_filename

    report_data = {
        'file': rel_path,
        'issues': [{'function': name, 'message': msg} for name, msg in issues],
        'timestamp': datetime.now().isoformat(),
    }

    report_path.parent.mkdir(parents=True, exist_ok=True)
    with report_path.open('w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=2)


def report_and_log(filepath: str, issues: list[tuple[str, str]]) -> None:
    """Display issues in the Rich console, write a structured report, and log
    the result."""
    setup_report_dirs()

    if issues:
        console.print(
            Panel(f"Issues found in [bold]{filepath}[/bold]", title='Validator Issues'),
        )
        for name, issue in issues:
            console.print(f"  [red]{name}[/red]: {issue}")
        write_report(filepath, issues)
        log_debug(f"Issues found in {filepath}: {len(issues)}")
    else:
        console.print(f"[green]No issues found in {filepath}[/green]")
        log_debug(f"No issues found in {filepath}")
