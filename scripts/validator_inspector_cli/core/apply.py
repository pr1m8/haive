from __future__ import annotations

from pathlib import Path

from rich.console import Console
from validator_inspector_cli.core.fixer import fix_validators
from validator_inspector_cli.core.post_validation import validate_fixed_file

console = Console()


def apply_fixes(filepath: str):
    fixed_tree = fix_validators(filepath)
    Path(filepath).write_text(fixed_tree.code, encoding='utf-8')

    validate_fixed_file(filepath)
