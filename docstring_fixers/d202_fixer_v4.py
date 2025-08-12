"""D202 Fixer V4: Remove extra blank lines after function docstrings (fully corrected)."""

import re
from typing import Any, Dict, List, Tuple

from .base_fixer import BaseFixer


class D202FixerV4(BaseFixer):
    """Final corrected fixer for D202: No blank lines allowed after function docstring.

    This version handles both single-line and multi-line docstrings correctly.
    """

    def __init__(self):
        """Initialize D202 fixer V4."""
        super().__init__(
            error_codes=["D202"],
            description="Remove extra blank lines after function docstrings",
        )

    def fix_content(self, content: str) -> Tuple[str, int, List[str]]:
        """Fix D202 issues in content using regex pattern matching.

        Args:
            content: Original file content.

        Returns:
            Tuple of (fixed_content, fixes_count, list_of_changes_made).
        """
        # Pattern to match docstring followed by blank lines
        # Groups: (indent)(quotes)(content)(quotes)(blank_lines)(next_content)
        patterns = [
            # Triple double quotes
            re.compile(
                r'^(\s*)(""")((?:[^"]|"(?!""))*)(""")\n(\n+)(\s*\S)', re.MULTILINE
            ),
            # Triple single quotes
            re.compile(
                r"^(\s*)(''')((?:[^']|'(?!''))*)(''')\n(\n+)(\s*\S)", re.MULTILINE
            ),
        ]

        fixed_content = content
        fixes_count = 0
        changes = []

        for pattern in patterns:

            def replacer(match):
                nonlocal fixes_count, changes
                indent = match.group(1)
                open_quotes = match.group(2)
                docstring_content = match.group(3)
                close_quotes = match.group(4)
                blank_lines = match.group(5)
                next_content = match.group(6)

                # Count blank lines
                blank_count = (
                    len(blank_lines) - 1
                )  # -1 because we want to keep one newline

                if blank_count > 0:
                    fixes_count += 1
                    line_num = content[: match.start()].count("\n") + 1
                    changes.append(
                        f"Removed {blank_count} blank line(s) after docstring at line {line_num}"
                    )

                # Return with only one newline after docstring
                return f"{indent}{open_quotes}{docstring_content}{close_quotes}\n{next_content}"

            fixed_content = pattern.sub(replacer, fixed_content)

        return fixed_content, fixes_count, changes
