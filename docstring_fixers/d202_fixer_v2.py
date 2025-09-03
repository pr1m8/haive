"""D202 Fixer V2: Remove extra blank lines after function docstrings."""

import re
from typing import Any, Dict, List, Tuple

from .base_fixer import BaseFixer


class D202FixerV2(BaseFixer):
    """Improved fixer for D202: No blank lines allowed after function docstring.

    This version uses a more robust approach to identify and fix D202 issues.
    """

    def __init__(self):
        """Initialize D202 fixer V2."""
        super().__init__(
            error_codes=["D202"],
            description="Remove extra blank lines after function docstrings",
        )

    def fix_content(self, content: str) -> Tuple[str, int, List[str]]:
        """Fix D202 issues in content.

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

            # Check if this line ends a docstring
            if line.strip().endswith('"""') or line.strip().endswith("'''"):
                # Check if it's part of a function/method/class docstring
                # Look backwards to find the definition
                def_line_idx = self._find_definition_line(lines, i)

                if def_line_idx is not None:
                    # Check if there are blank lines after the docstring
                    blank_count = 0
                    j = i + 1
                    while j < len(lines) and lines[j].strip() == "":
                        blank_count += 1
                        j += 1

                    if blank_count > 0 and j < len(lines):
                        # Skip the blank lines
                        i = j - 1  # Will be incremented at end of loop
                        fixes_count += 1
                        changes.append(
                            f"Removed {blank_count} blank line(s) after docstring at line {i + 1}"
                        )

            i += 1

        return "\n".join(fixed_lines), fixes_count, changes

    def _find_definition_line(self, lines: List[str], docstring_end_idx: int) -> int:
        """Find the function/class definition line before the docstring.

        Args:
            lines: All lines in the file.
            docstring_end_idx: Index of the line where docstring ends.

        Returns:
            Index of the definition line, or None if not found.
        """
        # Look backwards from the docstring
        for i in range(docstring_end_idx - 1, -1, -1):
            line = lines[i].strip()

            # Check if this is a definition line
            if (
                line.startswith("def ")
                or line.startswith("class ")
                or line.startswith("async def ")
            ) and line.endswith(":"):

                # Make sure there's a docstring between the def and our end line
                # (not some other string literal)
                has_docstring_start = False
                for j in range(i + 1, docstring_end_idx):
                    if lines[j].strip().startswith('"""') or lines[
                        j
                    ].strip().startswith("'''"):
                        has_docstring_start = True
                        break

                if has_docstring_start:
                    return i

        return None
