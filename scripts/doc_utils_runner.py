#!/usr/bin/env python3
"""Haive Documentation Utilities Runner.

Convenient entry point for the documentation utilities system.
This script provides easy access to all documentation tools.

Examples:
    # Analyze all agents
    python doc_utils_runner.py analyze --report

    # Run all examples
    python doc_utils_runner.py run --run-all --visualize

    # Create visualizations
    python doc_utils_runner.py visualize --compare --format html

    # Generate documentation
    python doc_utils_runner.py docs --api-docs --output ./agent_docs
"""

from __future__ import annotations

import asyncio
from pathlib import Path
import sys

from scripts.doc_utils.cli import main

# Add the project root to the path to ensure imports work
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

if __name__ == "__main__":
    asyncio.run(main())
