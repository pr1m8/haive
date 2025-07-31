import sys
from pathlib import Path

from rich.console import Console
from validator_inspector_cli.core.discovery import analyze_validators
from validator_inspector_cli.core.fixer import apply_fixes
from validator_inspector_cli.core.preview import preview_fixes

console = Console()


def process_file(file_path: Path, action: str):
    match action:
        case "discover":
            analyze_validators(str(file_path))
        case "preview":
            preview_fixes(str(file_path))
        case "apply":
            apply_fixes(str(file_path))
        case _:
            console.print(f"[red]Unknown action: {action}[/red]")


def process_path(input_path: Path, action: str):
    if input_path.is_file() and input_path.suffix == ".py":
        process_file(input_path, action)
    elif input_path.is_dir():
        py_files = list(input_path.rglob("*.py"))
        if not py_files:
            console.print(f"[yellow]No Python files found in {input_path}[/yellow]")
        for f in py_files:
            process_file(f, action)
    else:
        console.print(f"[red]Invalid path: {input_path}[/red]")


def run_cli():
    if len(sys.argv) < 2:
        console.print(
            "[red]Usage: python -m validator_inspector_cli <file_or_dir> [--preview|--apply][/red]"
        )
        sys.exit(1)

    target = Path(sys.argv[1])
    if not target.exists():
        console.print(f"[red]Path does not exist: {target}[/red]")
        sys.exit(1)

    action = "discover"
    if "--preview" in sys.argv:
        action = "preview"
    elif "--apply" in sys.argv:
        action = "apply"

    process_path(target, action)
