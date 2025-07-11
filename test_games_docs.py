#!/usr/bin/env python3
"""Test building documentation for haive.games specifically."""

import os
from pathlib import Path
import subprocess
import sys


# Set up environment
project_root = Path(__file__).parent
os.chdir(project_root)

# Run sphinx-build with minimal configuration
cmd = [
    "poetry",
    "run",
    "sphinx-build",
    "-b",
    "html",
    "-E",  # Force rebuild
    "-v",  # Verbose
    "--keep-going",  # Continue on errors
    "-D",
    "autosummary_generate=True",
    "docs/source",
    "docs/_test_build",
    "api/haive/games/index.rst",  # Build only games docs
]


result = subprocess.run(cmd, check=False, capture_output=True, text=True)


# Check the debug log
debug_log = project_root / "docs/source/sphinx_debug.log"
if debug_log.exists():
    with open(debug_log) as f:
        pass
