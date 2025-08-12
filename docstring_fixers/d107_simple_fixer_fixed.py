"""D107 Simple Fixer: Add missing __init__ docstrings (fixed)."""

import ast
from typing import Any, Dict, List, Tuple

from .base_fixer import BaseFixer


class D107SimpleFixerFixed(BaseFixer):
    """Simple fixer for D107: Missing __init__ method docstring.

    This version manually adds simple docstrings to __init__ methods.
    """

    def __init__(self):
        """Initialize D107 simple fixer."""
        super().__init__(
            error_codes=["D107"], description="Add missing __init__ method docstrings"
        )

    def fix_content(self, content: str) -> Tuple[str, int, List[str]]:
        """Fix D107 issues by adding __init__ docstrings.

        Args:
            content: Original file content.

        Returns:
            Tuple of (fixed_content, fixes_count, list_of_changes_made).
        """
        lines = content.split("\n")
        fixed_lines = []
        fixes_count = 0
        changes = []
        i = 0

        while i < len(lines):
            line = lines[i]
            fixed_lines.append(line)

            # Check if this is an __init__ method definition
            stripped = line.strip()
            if stripped.startswith("def __init__(") and stripped.endswith(":"):
                # Get the indentation
                indent = line[: len(line) - len(line.lstrip())]

                # Check if next line has a docstring
                has_docstring = False
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    if next_line.startswith('"""') or next_line.startswith("'''"):
                        has_docstring = True

                if not has_docstring:
                    # Add a simple docstring
                    docstring_indent = indent + "    "  # One more level of indentation
                    fixed_lines.append(f'{docstring_indent}"""Initialize instance."""')
                    fixes_count += 1
                    changes.append(f"Added __init__ docstring at line {i + 1}")

            i += 1

        return "\n".join(fixed_lines), fixes_count, changes
