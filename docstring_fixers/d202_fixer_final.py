"""D202 Fixer Final: Remove extra blank lines after function docstrings."""

import re
from typing import Any, Dict, List, Tuple

from .base_fixer import BaseFixer


class D202FixerFinal(BaseFixer):
    """Final fixer for D202: No blank lines allowed after function docstring.

    This version uses a simpler and more robust regex approach.
    """

    def __init__(self):
        """Initialize D202 fixer Final."""
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
        # Pattern to match docstring followed by 2+ newlines
        # This will match any docstring (single or multi-line) followed by blank lines
        pattern = re.compile(r'(""".*?"""|\'\'\'.*?\'\'\')(\n\n+)', re.DOTALL)

        fixes_count = 0
        changes = []

        def replacer(match):
            nonlocal fixes_count, changes
            docstring = match.group(1)
            newlines = match.group(2)

            # Count extra blank lines (total newlines - 1)
            blank_count = newlines.count("\n") - 1

            if blank_count > 0:
                fixes_count += 1
                # Find line number
                line_num = content[: match.start()].count("\n") + 1
                changes.append(
                    f"Removed {blank_count} blank line(s) after docstring at line {line_num}"
                )

            # Return with single newline
            return docstring + "\n"

        fixed_content = pattern.sub(replacer, content)

        return fixed_content, fixes_count, changes
