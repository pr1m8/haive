from rich.console import Console
from rich.panel import Panel

console = Console()


def report_and_log(filepath: str, issues: list):
    """Report issues for a file."""
    if not issues:
        console.print(f"No issues found in {filepath}")
        return

    console.print(Panel(f"Issues found in {filepath}", title="Validator Issues"))

    for func_name, issue in issues:
        console.print(f"  {func_name}: {issue}")


def log_debug(message: str):
    """Debug logging."""
    # Could add file logging here if needed
