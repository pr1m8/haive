#!/usr/bin/env python3
"""Disable sphinx_design extension across all configuration files."""

import os
import re
from pathlib import Path


def disable_sphinx_design(file_path):
    """Comment out sphinx_design in a file."""
    with open(file_path, "r") as f:
        content = f.read()

    # Pattern to match sphinx_design entries
    patterns = [
        # In lists
        (
            r'(\s*)"sphinx_design"(,?)(\s*#.*)?$',
            r'\1# "sphinx_design"\2  # DISABLED: Incompatible with Sphinx 8.2.3\3',
        ),
        # In dicts
        (
            r"(\s*)\'sphinx_design\':\s*\'sphinx_design\'(,?)(\s*#.*)?$",
            r"\1# \'sphinx_design\': \'sphinx_design\'\2  # DISABLED: Incompatible with Sphinx 8.2.3\3",
        ),
        # In append statements
        (
            r'(\s*)extensions\.append\("sphinx_design"\)',
            r'\1# extensions.append("sphinx_design")  # DISABLED: Incompatible with Sphinx 8.2.3',
        ),
    ]

    modified = False
    for pattern, replacement in patterns:
        new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
        if new_content != content:
            content = new_content
            modified = True

    if modified:
        with open(file_path, "w") as f:
            f.write(content)
        print(f"Modified: {file_path}")

    return modified


# Find all Python files in conf_modules
conf_modules_dir = Path("source/conf_modules")
files_modified = 0

for py_file in conf_modules_dir.rglob("*.py"):
    if disable_sphinx_design(py_file):
        files_modified += 1

print(f"\nTotal files modified: {files_modified}")

# Also clean up any cached files
for cache_dir in conf_modules_dir.rglob("__pycache__"):
    for pyc_file in cache_dir.glob("*.pyc"):
        pyc_file.unlink()
    print(f"Cleaned cache: {cache_dir}")
