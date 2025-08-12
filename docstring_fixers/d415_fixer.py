"""D415 Fixer: Add missing punctuation to docstring first lines."""

import re
from typing import Any, Dict, List, Tuple

from .base_fixer import BaseFixer


class D415Fixer(BaseFixer):
    """Fixer for D415: First line should end with a period, question mark, or exclamation point.

    This fixer identifies docstring first lines that don't end with proper punctuation
    and adds a period to fix the issue.

    Examples:
        "Abstract base class for models" → "Abstract base class for models."
        "Haive - AI Agent Framework" → "Haive - AI Agent Framework."
        "Get loader configuration" → "Get loader configuration."
    """

    def __init__(self):
        """Initialize D415 fixer."""
        super().__init__(
            error_codes=["D415"],
            description="Add missing punctuation to docstring first lines",
        )

        # Pattern to match docstring first lines without proper punctuation
        # Captures: opening quotes + content + closing quotes
        self.docstring_pattern = re.compile(
            r'^(\s*""")(.*?)(?<![.!?])(\s*""")$', re.MULTILINE
        )

        # Alternative pattern for triple single quotes
        single_quotes = "'" * 3
        self.docstring_single_pattern = re.compile(
            rf"^(\s*{re.escape(single_quotes)})(.*?)(?<![.!?])(\s*{re.escape(single_quotes)})$",
            re.MULTILINE,
        )

    def fix_content(self, content: str) -> Tuple[str, int, List[str]]:
        """Fix D415 issues in content.

        Args:
            content: Original file content.

        Returns:
            Tuple of (fixed_content, fixes_count, list_of_changes_made).
        """
        fixed_content = content
        fixes_count = 0
        changes = []

        # Process triple double quotes
        fixes_count += self._fix_docstring_pattern(
            fixed_content, self.docstring_pattern, '"""', changes
        )
        if fixes_count > 0:
            fixed_content = self.docstring_pattern.sub(
                lambda m: f"{m.group(1)}{m.group(2).rstrip()}.{m.group(3)}",
                fixed_content,
            )

        # Process triple single quotes
        single_quote_style = "'" * 3
        single_fixes = self._fix_docstring_pattern(
            fixed_content, self.docstring_single_pattern, single_quote_style, changes
        )
        if single_fixes > 0:
            fixes_count += single_fixes
            fixed_content = self.docstring_single_pattern.sub(
                lambda m: f"{m.group(1)}{m.group(2).rstrip()}.{m.group(3)}",
                fixed_content,
            )

        return fixed_content, fixes_count, changes

    def _fix_docstring_pattern(
        self, content: str, pattern: re.Pattern, quote_style: str, changes: List[str]
    ) -> int:
        """Fix docstrings matching a specific pattern.

        Args:
            content: Content to search.
            pattern: Regex pattern to match.
            quote_style: Style of quotes (triple double or triple single).
            changes: List to append changes to.

        Returns:
            Number of fixes applied.
        """
        matches = pattern.findall(content)
        fixes = 0

        for indent, text, closing in matches:
            # Skip empty docstrings or ones that are just whitespace
            if not text.strip():
                continue

            # Skip if already ends with punctuation (shouldn't match, but safety check)
            if text.rstrip().endswith((".", "!", "?")):
                continue

            # Skip if it looks like it's not a first line (contains newlines)
            if "\n" in text:
                continue

            # Skip if it's a single word (probably a variable name or similar)
            words = text.strip().split()
            if len(words) < 2:
                continue

            fixes += 1
            changes.append(f"Added period to: {quote_style}{text.strip()}{quote_style}")

        return fixes

    def preview_fixes(
        self, content: str, context_lines: int = 2
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

        # Find all matches
        single_quote_style = "'" * 3
        patterns_and_quotes = [
            (self.docstring_pattern, '"""'),
            (self.docstring_single_pattern, single_quote_style),
        ]
        for pattern, quote_style in patterns_and_quotes:
            for match in pattern.finditer(content):
                indent, text, closing = match.groups()

                if not text.strip() or text.rstrip().endswith((".", "!", "?")):
                    continue
                if "\n" in text or len(text.strip().split()) < 2:
                    continue

                # Find line number
                line_num = content[: match.start()].count("\n")

                # Get context
                start_line = max(0, line_num - context_lines)
                end_line = min(len(lines), line_num + context_lines + 1)

                context = []
                for i in range(start_line, end_line):
                    prefix = ">>>" if i == line_num else "   "
                    context.append(f"{prefix} {i+1:3}: {lines[i]}")

                previews.append(
                    {
                        "line_number": line_num + 1,
                        "original": f"{indent}{text}{closing}",
                        "fixed": f"{indent}{text.rstrip()}.{closing}",
                        "context": "\n".join(context),
                    }
                )

        return previews
