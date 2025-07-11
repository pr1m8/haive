#!/usr/bin/env python3
"""Automatically fix all toctree and cross-reference paths in RST files."""

import os
import re
from pathlib import Path


def fix_rst_file(file_path):
    """Fix all path references in an RST file."""
    with open(file_path) as f:
        content = f.read()

    original_content = content

    # Get the directory name from the file path
    dir_name = Path(file_path).stem

    # Fix patterns based on the file location
    if "/api/haive/core/engine/" in str(file_path):
        # Fix toctree entries: "document/sources/index" -> "sources/index"
        content = re.sub(rf"(\s+){dir_name}/(\S+)", r"\1\2", content)

        # Fix cross-references in See Also sections: ":doc:`document/sources/index`" -> ":doc:`sources/index`"
        content = re.sub(rf":doc:`{dir_name}/([^`]+)`", r":doc:`\1`", content)

    elif "/api/haive/core/models/" in str(file_path):
        # Similar fixes for models directory
        content = re.sub(rf"(\s+){dir_name}/(\S+)", r"\1\2", content)
        content = re.sub(rf":doc:`{dir_name}/([^`]+)`", r":doc:`\1`", content)

    # Add :hidden: directive after :caption: if missing
    if ".. toctree::" in content and ":caption:" in content:
        lines = content.split("\n")
        new_lines = []
        in_toctree = False

        for i, line in enumerate(lines):
            new_lines.append(line)
            if ".. toctree::" in line:
                in_toctree = True
            elif in_toctree and ":caption:" in line:
                # Check if :hidden: is already in the next few lines
                has_hidden = False
                for j in range(i + 1, min(i + 5, len(lines))):
                    if ":hidden:" in lines[j]:
                        has_hidden = True
                        break
                if not has_hidden:
                    # Find the indentation level
                    indent = len(line) - len(line.lstrip())
                    new_lines.append(" " * indent + ":hidden:")
            elif (
                in_toctree
                and line.strip()
                and not line.strip().startswith(":")
                and not line.startswith(" ")
            ):
                in_toctree = False

        content = "\n".join(new_lines)

    # Write back if changed
    if content != original_content:
        with open(file_path, "w") as f:
            f.write(content)
        return True

    return False


def fix_directory(directory):
    """Fix all RST files in a directory and its subdirectories."""
    directory = Path(directory)
    fixed_files = []

    # Find all RST files
    for rst_file in directory.rglob("*.rst"):
        if fix_rst_file(rst_file):
            fixed_files.append(rst_file)

    return fixed_files


def main():
    """Fix all documentation files."""
    base_dir = Path("/home/will/Projects/haive/backend/haive/docs/source")

    # Directories to process
    directories = [
        base_dir / "api/haive/core/engine",
        base_dir / "api/haive/core/models",
        base_dir / "api/haive/agents",
    ]

    all_fixed = []

    for directory in directories:
        if directory.exists():
            fixed = fix_directory(directory)
            all_fixed.extend(fixed)
            for _f in fixed:
                pass

    # Show summary of changes
    if all_fixed:
        for _f in sorted(all_fixed):
            pass


if __name__ == "__main__":
    main()
