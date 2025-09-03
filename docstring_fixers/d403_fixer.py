"""D403 Fixer: Capitalize first word of docstring first line."""

import re
from typing import Any, Dict, List, Tuple

from .base_fixer import BaseFixer


class D403Fixer(BaseFixer):
    """Fixer for D403: First word of the first line should be capitalized.

    This fixer identifies docstring first lines that start with lowercase letters
    and capitalizes the first word to fix the issue.

    Examples:
        "lowercase start of sentence." → "Lowercase start of sentence."
        "get configuration data." → "Get configuration data."
        "abstract base class for models." → "Abstract base class for models."
    """

    def __init__(self):
        """Initialize D403 fixer."""
        super().__init__(
            error_codes=["D403"],
            description="Capitalize first word of docstring first line",
        )

        # Pattern to match docstring first lines starting with lowercase
        # Captures: (opening quotes + whitespace)(lowercase_first_word)(rest_of_line)(closing quotes)
        self.docstring_pattern = re.compile(
            r'^(\s*""")\s*([a-z])([^"]*?)(\s*""")$', re.MULTILINE
        )

        # Alternative pattern for triple single quotes
        single_quotes = "'" * 3
        self.docstring_single_pattern = re.compile(
            rf"^(\s*{re.escape(single_quotes)})\s*([a-z])([^']*?)(\s*{re.escape(single_quotes)})$",
            re.MULTILINE,
        )

    def fix_content(self, content: str) -> Tuple[str, int, List[str]]:
        """Fix D403 issues in content.

        Args:
            content: Original file content.

        Returns:
            Tuple of (fixed_content, fixes_count, list_of_changes_made).
        """
        fixed_content = content
        fixes_count = 0
        changes = []

        # Process triple double quotes
        matches = self.docstring_pattern.findall(content)
        if matches:
            fixes_count += len(matches)
            for opening, first_char, rest, closing in matches:
                original_text = first_char + rest
                changes.append(f'Capitalized: "{original_text.strip()[:50]}..."')

            # Apply fixes: capitalize the first character
            fixed_content = self.docstring_pattern.sub(
                lambda m: f"{m.group(1)} {m.group(2).upper()}{m.group(3)}{m.group(4)}",
                fixed_content,
            )

        # Process triple single quotes
        single_matches = self.docstring_single_pattern.findall(fixed_content)
        if single_matches:
            single_fixes = len(single_matches)
            fixes_count += single_fixes
            for opening, first_char, rest, closing in single_matches:
                original_text = first_char + rest
                changes.append(
                    f'Capitalized (single quotes): "{original_text.strip()[:50]}..."'
                )

            # Apply fixes for single quotes
            fixed_content = self.docstring_single_pattern.sub(
                lambda m: f"{m.group(1)} {m.group(2).upper()}{m.group(3)}{m.group(4)}",
                fixed_content,
            )

        return fixed_content, fixes_count, changes

    def _should_skip_capitalization(self, text: str) -> bool:
        """Check if we should skip capitalizing this text.

        Args:
            text: The text to check.

        Returns:
            True if we should skip capitalizing this text.
        """
        text = text.strip().lower()

        # Skip if it starts with known technical terms that should stay lowercase
        skip_patterns = [
            "api",
            "url",
            "http",
            "https",
            "json",
            "xml",
            "html",
            "css",
            "js",
            "sql",
            "db",
            "id",
            "uuid",
            "uri",
            "tcp",
            "udp",
            "ip",
            "dns",
            "__init__",
            "__call__",
            "__str__",
            "__repr__",
            "get_",
            "set_",
            "is_",
            "has_",
            "can_",
            "should_",
            "async ",
            "await ",
            "def ",
            "class ",
            "import ",
            "from ",
        ]

        return any(text.startswith(pattern) for pattern in skip_patterns)

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

        # Check both patterns
        patterns_and_quotes = [
            (self.docstring_pattern, '"""'),
            (self.docstring_single_pattern, "'''"),
        ]

        for pattern, quote_style in patterns_and_quotes:
            for match in pattern.finditer(content):
                opening, first_char, rest, closing = match.groups()
                full_text = first_char + rest

                # Skip if we shouldn't capitalize this
                if self._should_skip_capitalization(full_text):
                    continue

                # Find line number
                line_num = content[: match.start()].count("\n")

                # Get context
                start_line = max(0, line_num - context_lines)
                end_line = min(len(lines), line_num + context_lines + 1)

                context = []
                for i in range(start_line, end_line):
                    if i < len(lines):
                        prefix = ">>>" if i == line_num else "   "
                        context.append(f"{prefix} {i+1:3}: {lines[i]}")

                previews.append(
                    {
                        "line_number": line_num + 1,
                        "original": f"{opening}{full_text}{closing}",
                        "fixed": f"{opening} {first_char.upper()}{rest}{closing}",
                        "quote_style": quote_style,
                        "context": "\n".join(context),
                    }
                )

        return previews
