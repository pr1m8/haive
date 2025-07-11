#!/usr/bin/env python3
"""Test Sphinx import handling."""

import sys
from pathlib import Path

# Simulate sphinx import
sys.path.insert(0, str(Path(__file__).parent / "docs/source"))
