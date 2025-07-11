#!/usr/bin/env python3
"""Fix common documentation warnings in the Haive project."""

import re
import sys
from pathlib import Path


def fix_rst_files():
    """Fix common RST formatting issues."""
    source_dir = Path(__file__).parent / "source"
    fixed_files = []

    # Fix showcase files
    showcase_files = list(source_dir.glob("agents/*_showcase.rst"))

    for rst_file in showcase_files:
        content = rst_file.read_text()
        original = content

        # Fix triple backticks in :doc: references
        content = re.sub(r":doc:```", ":doc:`", content)

        # Fix unterminated inline literals and strong text
        lines = content.split("\n")
        fixed_lines = []

        for line in lines:
            # Count backticks and asterisks
            backtick_count = line.count("`")
            double_backtick_count = line.count("``")
            asterisk_count = line.count("*")
            double_asterisk_count = line.count("**")

            # Fix odd number of backticks (excluding :doc:, :ref: etc)
            if backtick_count % 2 == 1:
                # Check if it's a role reference
                if not re.search(r":[a-z]+:`[^`]*$", line):
                    line = line.rstrip() + "`"

            # Fix odd number of double backticks
            if double_backtick_count % 2 == 1:
                line = line.rstrip() + "``"

            # Fix odd number of double asterisks
            if (
                asterisk_count - double_asterisk_count * 2
            ) == 0 and double_asterisk_count % 2 == 1:
                line = line.rstrip() + "**"

            fixed_lines.append(line)

        content = "\n".join(fixed_lines)

        if content != original:
            rst_file.write_text(content)
            fixed_files.append(rst_file.name)

    # Fix missing files by creating stubs
    missing_files = {
        "guides/agent_games.rst": """.. _agent_games:

Agent Games
===========

Documentation for agent-based games is coming soon.

See :doc:`/games/index` for available games.
""",
    }

    for file_path, content in missing_files.items():
        full_path = source_dir / file_path
        if not full_path.exists():
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content)

    return fixed_files


def fix_python_docstrings():
    """Fix common docstring issues in Python files."""
    packages_dir = Path(__file__).parent.parent / "packages"

    # Fix the specific RetrieverType docstring issue
    retriever_types_file = (
        packages_dir / "haive-core/src/haive/core/engine/retriever/types.py"
    )

    if retriever_types_file.exists():
        content = retriever_types_file.read_text()
        original = content

        # Fix the specific indentation issue in RetrieverType docstring
        # The issue is that the category descriptions have inconsistent indentation
        content = re.sub(
            r"(\s+Categories:\n)(\s+Base Vector Store Retrievers:\n)(\s+Simple retrievers.*\n\n)(\s+Advanced Retrieval Strategies:\n)(\s+Sophisticated.*)",
            lambda m: m.group(1)
            + m.group(2)
            + m.group(3)
            + m.group(4)
            + "        "
            + m.group(5),
            content,
            flags=re.DOTALL,
        )

        if content != original:
            retriever_types_file.write_text(content)

    # Fix BaseRetrieverConfig docstring issues
    retriever_file = (
        packages_dir / "haive-core/src/haive/core/engine/retriever/retriever.py"
    )

    if retriever_file.exists():
        content = retriever_file.read_text()
        original = content

        # Fix inline literals in docstrings
        # Look for lines that have an odd number of backticks
        lines = content.split("\n")
        fixed_lines = []
        in_docstring = False

        for line in lines:
            if '"""' in line:
                in_docstring = not in_docstring

            if in_docstring:
                # Count backticks
                backtick_count = line.count("`")
                if backtick_count % 2 == 1 and not re.search(r"```", line):
                    # Add closing backtick if missing
                    line = line.rstrip() + "`"

            fixed_lines.append(line)

        content = "\n".join(fixed_lines)

        if content != original:
            retriever_file.write_text(content)


if __name__ == "__main__":

    # Fix RST files
    fixed_rst = fix_rst_files()

    # Fix Python docstrings
    fix_python_docstrings()
