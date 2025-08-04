#!/usr/bin/env python3
"""Fix common issues in showcase RST files - improved version."""

from __future__ import annotations

from pathlib import Path
import re


def fix_showcase_file(file_path):
    """Fix common RST issues in a showcase file."""
    with open(file_path) as f:
        lines = f.readlines()

    fixed_lines = []
    in_json_block = False

    for i, line in enumerate(lines):
        # Remove trailing spaces
        line = line.rstrip() + "\n" if line.endswith("\n") else line.rstrip()

        # Fix malformed asterisks
        line = re.sub(r"\*{3,}", "", line)
        line = re.sub(r"\*\*([^*]+)\*{3,}:\*\*", r"**\1:**", line)
        line = re.sub(r"\*\*(\w+)\s+", r"**\1** ", line)
        line = re.sub(r"(\w+)\s+\*\*", r"\1 **", line)

        # Fix specific patterns
        line = line.replace("**Success***s**", "**Success**")
        line = line.replace("``custom.SimpleAgen``t````",
                            "``custom.SimpleAgent``")
        line = line.replace("``haive.mock.simpleagen``t``",
                            "``haive.mock.simpleagent``")
        line = line.replace("`` ``SimpleAgen``t``", "``SimpleAgent``")

        # Handle JSON blocks
        if line.strip() == ".. code-block:: json":
            in_json_block = True
            fixed_lines.append(line)
            continue
        if (in_json_block and line.strip() == "" and i + 1 < len(lines)
                and lines[i + 1].strip().startswith("{")):
            fixed_lines.append(line)
            continue
        if in_json_block and not line.startswith(" ") and line.strip() != "":
            in_json_block = False

        if in_json_block and line.strip():
            # Ensure proper indentation for JSON content
            content = line.lstrip()
            if (content.startswith("{") or content.startswith("}")
                    or content.startswith("[") or content.startswith("]")):
                line = "   " + content.rstrip() + "\n"
            elif content.startswith('"'):
                line = "     " + content.rstrip() + "\n"
            elif re.match(r"\s*\{", line):
                line = "   {\n"
            elif re.match(r"\s*\}", line):
                line = "   }\n"

        # Fix section underlines
        if i > 0 and line.strip() and all(c in "=-~" for c in line.strip()):
            prev_line = lines[i - 1].rstrip()
            if prev_line:
                char = line.strip()[0]
                fixed_lines.append(char * len(prev_line) + "\n")
                continue

        # Clean up lists
        if line.strip() == "*":
            continue

        fixed_lines.append(line)

    # Join and clean up multiple blank lines
    content = "".join(fixed_lines)
    content = re.sub(r"\n{3,}", "\n\n", content)

    # Write back
    with open(file_path, "w") as f:
        f.write(content)

    print(f"Fixed: {file_path}")
    return True


def main():
    """Fix all showcase RST files."""
    docs_dir = Path("docs/source/agents")
    showcase_files = list(docs_dir.glob("*_showcase.rst"))

    for file_path in showcase_files:
        fix_showcase_file(file_path)

    print(f"\nProcessed {len(showcase_files)} showcase files")


if __name__ == "__main__":
    main()
