"""D202 Fixer: Remove extra blank lines after function docstrings."""

import re
from typing import Any, Dict, List, Tuple

from .base_fixer import BaseFixer


class D202Fixer(BaseFixer):
    """Fixer for D202: No blank lines allowed after function docstring.

    This fixer identifies docstrings that are followed by extra blank lines
    and removes those blank lines to fix the issue.

    Examples:
        def function():\n    '''Docstring.'''\n\n    return "test"
        → def function():\n    '''Docstring.'''\n    return "test"

        def method(self):\n    '''Method docstring.'''\n\n\n    self.value = 1
        → def method(self):\n    '''Method docstring.'''\n    self.value = 1
    """

    def __init__(self):
        """Initialize D202 fixer."""
        super().__init__(
            error_codes=["D202"],
            description="Remove extra blank lines after function docstrings",
        )

        # Pattern to match docstring followed by one or more blank lines
        # This needs to specifically match function/class docstrings
        # Pattern: (def/class line + docstring)(blank lines)(next line)
        self.pattern = re.compile(
            r'((?:^|\n)(?:\s*(?:def|class)\s+[^\n]+:\n)?(\s*)""".*?"""\n)(\n+)(\2\S)',
            re.MULTILINE | re.DOTALL,
        )

        # Alternative pattern for single quotes
        self.single_pattern = re.compile(
            r"((?:^|\n)(?:\s*(?:def|class)\s+[^\n]+:\n)?(\s*)'''.*?'''\n)(\n+)(\2\S)",
            re.MULTILINE | re.DOTALL,
        )

    def fix_content(self, content: str) -> Tuple[str, int, List[str]]:
        """Fix D202 issues in content.

        Args:
            content: Original file content.

        Returns:
            Tuple of (fixed_content, fixes_count, list_of_changes_made).
        """
        fixed_content = content
        fixes_count = 0
        changes = []

        # Process triple double quotes
        matches = self.pattern.findall(fixed_content)
        if matches:
            for docstring_part, blank_lines, next_content in matches:
                if len(blank_lines) > 1:  # More than one newline (blank line)
                    fixes_count += 1
                    changes.append(
                        f"Removed {len(blank_lines) - 1} extra blank line(s) after docstring"
                    )

            # Apply the fix: keep docstring + one newline + next content
            fixed_content = self.pattern.sub(r"\1\3", fixed_content)

        # Process triple single quotes
        single_matches = self.single_pattern.findall(fixed_content)
        if single_matches:
            for docstring_part, blank_lines, next_content in single_matches:
                if len(blank_lines) > 1:  # More than one newline (blank line)
                    fixes_count += 1
                    changes.append(
                        f"Removed {len(blank_lines) - 1} extra blank line(s) after single-quoted docstring"
                    )

            # Apply the fix for single quotes
            fixed_content = self.single_pattern.sub(r"\1\3", fixed_content)

        return fixed_content, fixes_count, changes

    def preview_fixes(
        self, content: str, context_lines: int = 3
    ) -> List[Dict[str, Any]]:
        """Preview what fixes would be applied without making changes.

        Args:
            content: Content to analyze.
            context_lines: Number of context lines to show around each fix.

        Returns:
            List of preview dictionaries with line numbers and changes.
        """
        previews = []
        lines = content.split("\n")

        # Check both patterns
        for pattern, quote_style in [
            (self.pattern, '"""'),
            (self.single_pattern, "'''"),
        ]:
            for match in pattern.finditer(content):
                docstring_part, blank_lines, next_content = match.groups()

                if len(blank_lines) <= 1:  # No extra blank lines to remove
                    continue

                # Find line number where the blank lines start
                line_num = content[: match.start(2)].count("\n")

                # Get context
                start_line = max(0, line_num - context_lines)
                end_line = min(len(lines), line_num + len(blank_lines) + context_lines)

                context = []
                for i in range(start_line, end_line):
                    if i < len(lines):
                        prefix = (
                            ">>>"
                            if line_num <= i < line_num + len(blank_lines)
                            else "   "
                        )
                        context.append(f"{prefix} {i+1:3}: {lines[i]}")

                previews.append(
                    {
                        "line_number": line_num + 1,
                        "blank_lines_to_remove": len(blank_lines) - 1,
                        "quote_style": quote_style,
                        "context": "\n".join(context),
                    }
                )

        return previews
