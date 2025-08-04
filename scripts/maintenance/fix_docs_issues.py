#!/usr/bin/env python3
"""Fix common documentation build issues."""

from __future__ import annotations

from pathlib import Path
import re


def fix_title_underlines(file_path):
    """Fix RST title underline length issues."""
    with open(file_path) as f:
        lines = f.readlines()

    fixed_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]

        # Check if next line exists and is an underline
        if i + 1 < len(lines):
            next_line = lines[i + 1]
            # Check for RST underline characters
            if next_line.strip() and all(c in '=-~^"'
                                         for c in next_line.strip()):
                title_length = len(line.rstrip())
                underline_char = next_line.strip()[0]
                correct_underline = underline_char * title_length + "\n"

                fixed_lines.append(line)
                fixed_lines.append(correct_underline)
                i += 2
                continue

        fixed_lines.append(line)
        i += 1

    with open(file_path, "w") as f:
        f.writelines(fixed_lines)


def fix_grid_items(file_path):
    """Fix grid-item parent issues in RST files."""
    with open(file_path) as f:
        content = f.read()

    # Fix grid structure by adding grid-row directives
    fixed_content = re.sub(
        r"(\.\. grid::.*?\n)((?:\s*\.\. grid-item::.*?\n(?:(?!\.\. grid).*\n)*)+)",
        lambda m: m.group(1) + "\n   .. grid-row::\n\n" + "\n".join(
            "      " + line for line in m.group(2).split("\n") if line),
        content,
        flags=re.MULTILINE | re.DOTALL,
    )

    with open(file_path, "w") as f:
        f.write(fixed_content)


def fix_duplicate_index_files():
    """Remove duplicate index files (keep RST over MD)."""
    docs_dir = Path("source")

    # Find all index.rst and index.md pairs
    for rst_file in docs_dir.rglob("index.rst"):
        md_file = rst_file.with_suffix(".md")
        if md_file.exists():
            md_file.unlink()


def fix_toctree_references(file_path):
    """Fix malformed toctree references."""
    with open(file_path) as f:
        content = f.read()

    # Fix multiple documents on one line in toctree
    fixed_content = re.sub(
        r"(\s+)(\w+_showcase)\s+(\w+_showcase)\s+(\w+_showcase)",
        r"\1\2\n\1\3\n\1\4",
        content,
    )

    with open(file_path, "w") as f:
        f.write(fixed_content)


def main():
    """Fix common documentation issues."""
    # Fix duplicate index files
    fix_duplicate_index_files()

    # Fix RST files with title underline issues
    rst_files = [
        "source/api/agents/base.rst",
        "source/api/agents/conversation.rst",
        "source/api/agents/document_modifiers.rst",
        "source/api/agents/rag.rst",
        "source/api/agents/react.rst",
        "source/api/agents/reasoning_and_critique.rst",
        "source/api/agents/simple.rst",
        "source/api/agents/task_analysis.rst",
    ]

    for rst_file in rst_files:
        file_path = Path(rst_file)
        if file_path.exists():
            fix_title_underlines(file_path)

    # Fix grid items in showcase_index.rst
    showcase_file = Path("source/agents/showcase_index.rst")
    if showcase_file.exists():
        fix_grid_items(showcase_file)
        fix_toctree_references(showcase_file)


if __name__ == "__main__":
    main()
