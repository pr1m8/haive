"""D100 Simple Fixer: Add missing module docstrings (fixed)."""

import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Tuple

from .base_fixer import BaseFixer


class D100SimpleFixerFixed(BaseFixer):
    """Simple fixer for D100: Missing module docstring.

    This version correctly uses doq with the -f flag.
    """

    def __init__(self):
        """Initialize D100 simple fixer."""
        super().__init__(
            error_codes=["D100"], description="Add missing module docstring using doq"
        )

    def fix_content(self, content: str) -> Tuple[str, int, List[str]]:
        """Fix D100 issues by adding module docstring.

        Args:
            content: Original file content.

        Returns:
            Tuple of (fixed_content, fixes_count, list_of_changes_made).
        """
        # Check if module already has docstring
        if self._has_module_docstring(content):
            return content, 0, []

        # For simple modules without docstring, add a basic one
        lines = content.strip().split("\n")

        # Skip shebang and encoding lines
        insert_pos = 0
        for i, line in enumerate(lines):
            if (
                line.startswith("#!")
                or line.startswith("# -*- coding")
                or line.startswith("# coding:")
            ):
                insert_pos = i + 1
            else:
                break

        # Add simple module docstring
        module_docstring = '"""Module docstring."""\n\n'

        # Insert the docstring
        if insert_pos == 0:
            fixed_content = module_docstring + content
        else:
            lines_before = lines[:insert_pos]
            lines_after = lines[insert_pos:]
            fixed_lines = (
                lines_before + ["", '"""Module docstring."""', ""] + lines_after
            )
            fixed_content = "\n".join(fixed_lines)

        return fixed_content, 1, ["Added module docstring"]

    def _has_module_docstring(self, content: str) -> bool:
        """Check if module already has a docstring."""
        lines = content.strip().split("\n")

        # Skip shebang, encoding, and blank lines
        for line in lines:
            stripped = line.strip()

            # Skip special lines
            if not stripped or stripped.startswith("#"):
                continue

            # Check if it's a docstring
            if stripped.startswith('"""') or stripped.startswith("'''"):
                return True

            # If we hit any other code, there's no module docstring
            return False

        return False
