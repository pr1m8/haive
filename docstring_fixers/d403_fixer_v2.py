"""D403 Fixer V2: Capitalize first word of docstring first line (improved)."""

import re
from typing import Any, Dict, List, Tuple

from .base_fixer import BaseFixer


class D403FixerV2(BaseFixer):
    """Improved fixer for D403: First word of the first line should be capitalized.

    This version handles edge cases better and doesn't add extra spaces.
    """

    def __init__(self):
        """Initialize D403 fixer V2."""
        super().__init__(
            error_codes=["D403"],
            description="Capitalize first word of docstring first line",
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

        # Process all docstrings
        # Pattern: (quotes)(content)(quotes)
        patterns = [
            re.compile(r'(""")(.*?)(""")', re.DOTALL),
            re.compile(r"(''')(.*?)(''')", re.DOTALL),
        ]

        for pattern in patterns:

            def replace_func(match):
                nonlocal fixes_count, changes

                quotes_open = match.group(1)
                content = match.group(2)
                quotes_close = match.group(3)

                if not content:
                    return match.group(0)

                # Get first line of content
                lines = content.split("\n", 1)
                first_line = lines[0]
                rest = lines[1] if len(lines) > 1 else ""

                # Strip leading/trailing whitespace from first line
                stripped = first_line.strip()
                if not stripped:
                    return match.group(0)

                # Check if first character is lowercase
                if stripped[0].islower():
                    # Check if we should skip this one
                    if not self._should_skip_capitalization(stripped):
                        # Capitalize first character
                        capitalized = stripped[0].upper() + stripped[1:]

                        # Reconstruct with original spacing
                        if first_line.startswith(" "):
                            # Had leading space
                            new_first_line = " " + capitalized
                        else:
                            new_first_line = capitalized

                        # Reconstruct full content
                        if rest:
                            new_content = new_first_line + "\n" + rest
                        else:
                            new_content = new_first_line

                        fixes_count += 1
                        changes.append(f"Capitalized: '{stripped[:50]}...'")

                        return quotes_open + new_content + quotes_close

                return match.group(0)

            fixed_content = pattern.sub(replace_func, fixed_content)

        return fixed_content, fixes_count, changes

    def _should_skip_capitalization(self, text: str) -> bool:
        """Check if we should skip capitalizing this text.

        Args:
            text: The text to check (already stripped).

        Returns:
            True if we should skip capitalizing this text.
        """
        text_lower = text.lower()

        # Skip if it starts with known technical terms
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
        ]

        # Check exact word match (not just prefix)
        first_word = text_lower.split()[0] if text_lower else ""

        return first_word in skip_patterns
