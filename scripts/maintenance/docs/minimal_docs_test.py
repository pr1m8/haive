#!/usr/bin/env python3
"""Minimal documentation build test to verify basic functionality."""

import shutil
import subprocess
from pathlib import Path

# Directories
SOURCE_DIR = Path("docs/source")
BUILD_DIR = Path("docs/build/test")

# Clean build directory
if BUILD_DIR.exists():
    shutil.rmtree(BUILD_DIR)
BUILD_DIR.mkdir(parents=True, exist_ok=True)

# Minimal sphinx command
cmd = [
    "poetry",
    "run",
    "sphinx-build",
    "-b",
    "html",
    "-q",  # Quiet mode
    "--keep-going",  # Continue on errors
    "-D",
    "extensions=sphinx.ext.autodoc,sphinx.ext.napoleon",  # Minimal extensions
    "-D",
    "master_doc=index",
    "-D",
    "project=Haive",
    "-D",
    "html_theme=pydata_sphinx_theme",
    str(SOURCE_DIR),
    str(BUILD_DIR),
]


try:
    result = subprocess.run(cmd, check=False, capture_output=True, text=True)


    if result.stdout:

    if result.stderr:

    # Check for output
    html_files = list(BUILD_DIR.glob("*.html"))

    if html_files:
    else:
        pass")

except Exception as e:
    pass")
