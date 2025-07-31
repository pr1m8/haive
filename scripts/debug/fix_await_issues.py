#!/usr/bin/env python3
"""Fix await outside function issues in RST files."""

from pathlib import Path
import re


def fix_await_in_code_block(content):
    """Fix await statements in code blocks."""
    # Pattern to find code blocks with await outside functions
    pattern = r"(\.\. code-block:: python\n\n(?:   [^\n]*\n)*?)(\s*)(await\s+[^\n]+)"

    def replace_func(match):
        before = match.group(1)
        indent = match.group(2)
        await_line = match.group(3)

        # Check if this await is already inside a function
        if "async def" in before or "async with" in before or "async for" in before:
            return match.group(0)  # Already inside async context

        # Find all the code that should be in the async function
        lines = before.split("\n")
        code_lines = []
        base_indent = "   "  # RST code block base indent

        # Collect lines until we find the await
        for line in reversed(lines):
            if line.strip() and not line.startswith(base_indent):
                break
            code_lines.insert(0, line)

        # Find the related code after the await
        remaining = content[match.end() :]
        after_lines = []
        for line in remaining.split("\n"):
            if line.startswith(base_indent) or line.strip() == "":
                after_lines.append(line)
                if line.strip() == "":
                    break
            else:
                break

        # Build the async function
        result = []
        for line in code_lines[:-1]:  # All but the last line
            result.append(line)

        # Add async function definition
        result.append(f"{base_indent}# Run with async")
        result.append(f"{base_indent}async def main():")

        # Add the await line with extra indent
        result.append(f"{base_indent}    {await_line.strip()}")

        # Add any following related lines
        for line in after_lines:
            if line.strip():
                result.append(f"    {line}")
            else:
                result.append(line)

        # Add asyncio.run
        result.append(f"{base_indent}")
        result.append(f"{base_indent}# Execute")
        result.append(f"{base_indent}import asyncio")
        result.append(f"{base_indent}asyncio.run(main())")

        return "\n".join(result)

    # Apply fixes
    fixed = re.sub(pattern, replace_func, content, flags=re.MULTILINE)
    return fixed


def fix_file(file_path):
    """Fix await issues in a single file."""
    content = file_path.read_text()

    # Check if file has await issues
    if "await " not in content:
        return False

    # Fix the content
    fixed = fix_await_in_code_block(content)

    if fixed != content:
        file_path.write_text(fixed)
        print(f"Fixed: {file_path}")
        return True
    return False


def main():
    """Fix all RST files with await issues."""
    docs_dir = Path("docs/source")
    rst_files = list(docs_dir.rglob("*.rst"))

    fixed_count = 0
    for file_path in rst_files:
        if fix_file(file_path):
            fixed_count += 1

    print(f"\nFixed {fixed_count} files with await issues")


if __name__ == "__main__":
    main()
