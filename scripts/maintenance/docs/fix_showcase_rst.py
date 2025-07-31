#!/usr/bin/env python3
"""Fix common issues in showcase RST files."""

from pathlib import Path
import re


def fix_showcase_file(file_path):
    """Fix common RST issues in a showcase file."""
    content = file_path.read_text()
    original = content

    # Fix malformed bold/italic markers
    content = re.sub(r"\*\*\*(\w+)\*\*\*:\*\*", r"**\1:**", content)
    content = re.sub(r"\*\*(\w+)\*\*\*:\*\*", r"**\1:**", content)
    content = re.sub(r"\*\*\*\n", "\n", content)
    content = re.sub(r"\*\*\*$", "", content, flags=re.MULTILINE)
    content = re.sub(r"^\*\*\*", "", content, flags=re.MULTILINE)
    content = re.sub(r"\*\*Succes\*\*\*s\*\*", "**Success**", content)
    content = re.sub(r"\*\*\s+", "** ", content)
    content = re.sub(r"\s+\*\*", " **", content)

    # Fix section underlines
    content = re.sub(r"\n-{3,}\n", lambda m: "\n" + "-" * len(m.group().strip()) + "\n", content)

    # Fix JSON indentation in code blocks
    lines = content.split("\n")
    in_json_block = False
    fixed_lines = []

    for i, line in enumerate(lines):
        if line.strip() == ".. code-block:: json":
            in_json_block = True
            fixed_lines.append(line)
        elif in_json_block and line and not line[0].isspace() and line.strip() != "":
            in_json_block = False
            fixed_lines.append(line)
        elif in_json_block and line.strip().startswith("{"):
            # Ensure proper indentation for JSON blocks
            fixed_lines.append("   {")
        elif in_json_block and line.strip() and not line.startswith("   "):
            # Fix indentation
            fixed_lines.append("   " + line.strip())
        else:
            fixed_lines.append(line)

    content = "\n".join(fixed_lines)

    # Fix missing JSON closing braces
    content = re.sub(r'(\n\s*"[^"]+"\s*:\s*"[^"]+"\s*\n)\s*\n}', r"\1   }\n}", content)

    # Fix backticks
    content = re.sub(r"``\s*``(\w+)``\s*``", r"``\1``", content)
    content = re.sub(r"``\s+", "``", content)
    content = re.sub(r"\s+``", "``", content)

    # Fix list items
    content = re.sub(r"^\*\s*$", "", content, flags=re.MULTILINE)

    # Fix title underlines
    lines = content.split("\n")
    fixed_lines = []
    for i in range(len(lines)):
        if i > 0 and i < len(lines) - 1:
            if lines[i].strip() and all(c in "=-" for c in lines[i].strip()):
                # This is an underline
                title_len = len(lines[i - 1].strip())
                if title_len > 0:
                    char = lines[i].strip()[0]
                    fixed_lines.append(char * title_len)
                else:
                    fixed_lines.append(lines[i])
            else:
                fixed_lines.append(lines[i])
        else:
            fixed_lines.append(lines[i])

    content = "\n".join(fixed_lines)

    if content != original:
        file_path.write_text(content)
        print(f"Fixed: {file_path}")
        return True
    return False


def main():
    """Fix all showcase RST files."""
    docs_dir = Path("docs/source/agents")
    showcase_files = list(docs_dir.glob("*_showcase.rst"))

    fixed_count = 0
    for file_path in showcase_files:
        if fix_showcase_file(file_path):
            fixed_count += 1

    print(f"\nFixed {fixed_count} out of {len(showcase_files)} showcase files")


if __name__ == "__main__":
    main()
