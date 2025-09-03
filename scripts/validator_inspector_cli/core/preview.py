from __future__ import annotations

from rich.console import Console
from validator_inspector_cli.core.fixer import fix_validators
from validator_inspector_cli.core.post_validation import validate_fixed_code

console = Console()


def preview_fixes(filepath: str):
    fixed_tree = fix_validators(filepath)
    fixed_code = fixed_tree.code

    console.rule(f"Preview Fixes for [bold]{filepath}[/bold]")
    console.print(f"[cyan]{fixed_code}[/cyan]")

    validate_fixed_code(fixed_code, original_path=filepath)
