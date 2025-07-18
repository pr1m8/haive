#!/usr/bin/env python3
"""Minimal documentation build script"""

import os
from pathlib import Path
import subprocess


def build_minimal_docs():
    """Build minimal documentation"""
    print("🚀 Building minimal documentation...")

    # Change to project directory
    os.chdir(Path(__file__).parent)

    # Clean previous build
    subprocess.run(["rm", "-rf", "docs/build"], check=False)

    # Build with minimal settings
    result = subprocess.run(
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

    print("Build result:", result.returncode)
    print("STDOUT:", result.stdout[-1000:])  # Last 1000 chars
    print("STDERR:", result.stderr[-1000:])  # Last 1000 chars

    # Check if HTML files were generated
    html_files = list(Path("docs/build").rglob("*.html"))
    print(f"Generated {len(html_files)} HTML files")

    if html_files:
        print("✅ Documentation built successfully!")
        print(f"📁 View at: {Path('docs/build/index.html').absolute()}")
        return True
    print("❌ No HTML files generated")
    return False


if __name__ == "__main__":
    build_minimal_docs()
