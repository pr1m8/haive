from __future__ import annotations

from pathlib import Path

import libcst as cst
from rich.console import Console

console = Console()


def validate_fixed_code(code: str, original_path: str = "") -> bool:
    try:
        cst.parse_module(code)
        console.print(f"[green]✅ Parsed successfully: {original_path}[/green]")
        return True
    except Exception as e:
        console.print(
            f"[red]❌ Failed to parse fixed code in {original_path}: {e}[/red]",
        )
        return False


def validate_fixed_file(filepath: str) -> bool:
    try:
        code = Path(filepath).read_text(encoding="utf-8")
        return validate_fixed_code(code, original_path=filepath)
    except Exception as e:
        console.print(f"[red]❌ Failed to read {filepath} for validation: {e}[/red]")
        return False
