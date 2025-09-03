"""D212 Fixer: Multi-line docstring summary should start at the first line."""

import re
from typing import Any, Dict, List, Tuple

from .base_fixer import BaseFixer


class D212Fixer(BaseFixer):
    """Fixer for D212: Multi-line docstring summary should start at the first line.

    This fixer identifies multi-line docstrings where the summary is on a separate line
    after the opening quotes and moves the summary up to the same line as the quotes.

    Examples:
        def function():\n    '''\n    Function description.\n    '''
        → def function():\n    '''Function description.\n    '''

        class MyClass:\n    '''\n    Class description here.\n    \n    More details.\n    '''
        → class MyClass:\n    '''Class description here.\n    \n    More details.\n    '''
    """

    def __init__(self):
        """Initialize D212 fixer."""
        super().__init__(
            error_codes=["D212"],
            description="Move multi-line docstring summary to first line",
        )

        # Pattern to match docstrings with summary on separate line
        # Captures: (indent)(opening_quotes)(whitespace/newlines)(summary_line)(rest_including_closing)
        self.pattern = re.compile(
            r'^(\s*)(""")\s*\n\s*([^\n]+)(.*?""")$', re.MULTILINE | re.DOTALL
        )

        # Alternative pattern for single quotes
        single_quotes = "'" * 3
        self.single_pattern = re.compile(
            rf"^(\s*)({re.escape(single_quotes)})\s*\n\s*([^\n]+)(.*?{re.escape(single_quotes)})$",
            re.MULTILINE | re.DOTALL,
        )

    def fix_content(self, content: str) -> Tuple[str, int, List[str]]:
        """Fix D212 issues in content.

        Args:
            content: Original file content.

        Returns:
            Tuple of (fixed_content, fixes_count, list_of_changes_made).
        """
        fixed_content = content
        fixes_count = 0
        changes = []

        # Process triple double quotes
        matches = self.pattern.findall(content)
        if matches:
            fixes_count += len(matches)
            for indent, opening, summary, rest in matches:
                changes.append(
                    f'Moved summary to first line: "{summary.strip()[:50]}..."'
                )

            # Apply fixes: move summary to same line as opening quotes
            fixed_content = self.pattern.sub(
                lambda m: f"{m.group(1)}{m.group(2)}{m.group(3).strip()}{m.group(4)}",
                fixed_content,
            )

        # Process triple single quotes
        single_matches = self.single_pattern.findall(fixed_content)
        if single_matches:
            single_fixes = len(single_matches)
            fixes_count += single_fixes
            for indent, opening, summary, rest in single_matches:
                changes.append(
                    f'Moved summary to first line (single quotes): "{summary.strip()[:50]}..."'
                )

            # Apply fixes for single quotes
            fixed_content = self.single_pattern.sub(
                lambda m: f"{m.group(1)}{m.group(2)}{m.group(3).strip()}{m.group(4)}",
                fixed_content,
            )

        return fixed_content, fixes_count, changes

    def _is_valid_summary_line(self, line: str) -> bool:
        """Check if this line is a valid summary line.

        Args:
            line: The line to check.

        Returns:
            True if this is a valid summary line.
        """
        line = line.strip()

        # Skip empty lines
        if not line:
            return False

        # Skip lines that look like section headers
        section_headers = [
            "args:",
            "arguments:",
            "parameters:",
            "param:",
            "params:",
            "returns:",
            "return:",
            "yields:",
            "yield:",
            "raises:",
            "raise:",
            "note:",
            "notes:",
            "example:",
            "examples:",
            "see also:",
            "todo:",
            "warning:",
            "warnings:",
            "deprecated:",
            "attributes:",
            "attr:",
        ]

        if line.lower().rstrip(":") in section_headers:
            return False

        # Skip lines that start with special markers
        special_markers = ["..", ">>>", "...", ">>>"]
        if any(line.startswith(marker) for marker in special_markers):
            return False

        # Must have at least 2 words to be a proper summary
        words = line.split()
        return len(words) >= 2

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
        patterns_and_quotes = [(self.pattern, '"""'), (self.single_pattern, "'''")]

        for pattern, quote_style in patterns_and_quotes:
            for match in pattern.finditer(content):
                indent, opening, summary, rest = match.groups()

                # Skip if not a valid summary line
                if not self._is_valid_summary_line(summary):
                    continue

                # Find line number of opening quotes
                line_num = content[: match.start()].count("\n")

                # Get context
                start_line = max(0, line_num - context_lines)
                end_line = min(
                    len(lines), line_num + context_lines + 3
                )  # Show a bit more for docstrings

                context = []
                for i in range(start_line, end_line):
                    if i < len(lines):
                        prefix = ">>>" if i == line_num or i == line_num + 1 else "   "
                        context.append(f"{prefix} {i+1:3}: {lines[i]}")

                # Show before and after
                original_snippet = f"{opening}\n{summary.strip()}"
                fixed_snippet = f"{opening}{summary.strip()}"

                previews.append(
                    {
                        "line_number": line_num + 1,
                        "original_snippet": original_snippet,
                        "fixed_snippet": fixed_snippet,
                        "summary_text": summary.strip(),
                        "quote_style": quote_style,
                        "context": "\n".join(context),
                    }
                )

        return previews
