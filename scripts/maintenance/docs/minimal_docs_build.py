#!/usr/bin/env python3
"""Minimal documentation build script."""

import os
import subprocess
from pathlib import Path


def build_minimal_docs():
    """Build minimal documentation."""
    # Change to project directory
    os.chdir(Path(__file__).parent)

    # Clean previous build
    subprocess.run(["rm", "-rf", "docs/build"], check=False)

    # Build with minimal settings
    subprocess.run(
        [
            "poetry",
            "run",
            "sphinx-build",
            "-b",
            "html",
            "-E",  # Rebuild all files
            "-a",  # Rebuild all files
            "--keep-going",
            "docs/source",
            "docs/build",
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    # Check if HTML files were generated
    html_files = list(Path("docs/build").rglob("*.html"))

    return bool(html_files)


if __name__ == "__main__":
    build_minimal_docs()
