#!/usr/bin/env python3
"""Organize test files from root directory to proper locations.
Uses git mv to preserve history.
"""

import os
import re
import subprocess
from pathlib import Path

# Base directories
ROOT_DIR = Path("/home/will/Projects/haive/backend/haive")
AGENTS_TESTS = ROOT_DIR / "packages/haive-agents/tests"
CORE_TESTS = ROOT_DIR / "packages/haive-core/tests"

# Create core tests directory if it doesn't exist
CORE_TESTS.mkdir(parents=True, exist_ok=True)

# File categorization rules
CATEGORIZATION_RULES = {
    # Multi-agent related tests
    "multi_agent": {
        "patterns": ["multi_agent", "meta_state", "recompile"],
        "destination": AGENTS_TESTS / "multi",
    },
    # Plan and Execute tests
    "plan_execute": {
        "patterns": ["plan_execute", "plan_and_execute"],
        "destination": AGENTS_TESTS / "test_planning",
    },
    # Schema related tests
    "schema": {
        "patterns": ["schema", "field_naming", "token_usage"],
        "destination": CORE_TESTS / "schema",
    },
    # MCP related tests
    "mcp": {"patterns": ["mcp"], "destination": AGENTS_TESTS / "mcp"},
    # Debug and utility tests
    "debug": {
        "patterns": ["debug", "verbose", "simple_debug"],
        "destination": AGENTS_TESTS / "utilities",
    },
    # Sphinx and documentation tests
    "docs": {"patterns": ["sphinx", "import"], "destination": CORE_TESTS / "docs"},
    # Sequential and state tests
    "state": {
        "patterns": ["sequential", "state_issue", "complete_flow"],
        "destination": CORE_TESTS / "state",
    },
}


def categorize_file(filename):
    """Categorize a test file based on its name."""
    filename_lower = filename.lower()

    for category, rules in CATEGORIZATION_RULES.items():
        for pattern in rules["patterns"]:
            if pattern in filename_lower:
                return category, rules["destination"]

    # Default to agents/tests if uncategorized
    return "uncategorized", AGENTS_TESTS / "utilities"


def move_file_with_git(source, destination_dir, filename):
    """Move file using git mv to preserve history."""
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = destination_dir / filename

    try:
        # Use git mv to preserve history
        cmd = ["git", "mv", str(source), str(destination)]
        result = subprocess.run(cmd, check=False, capture_output=True, text=True, cwd=ROOT_DIR)

        if result.returncode == 0:
            return True
        print(f"❌ Git mv failed for {filename}: {result.stderr}")

        # Try regular mv as fallback
        cmd = ["mv", str(source), str(destination)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ Moved {filename} to {destination_dir} (fallback)")
            return True
        else:
            print(f"❌ Regular mv also failed for {filename}: {result.stderr}")
            return False

    except Exception as e:
        return False


def main():
    """Main function to organize test files."""

    # Find all test files in root
    test_files = list(ROOT_DIR.glob("test_*.py"))

    if not test_files:
        return


    # Categorize and move files
    moved_count = 0
    failed_count = 0

    for test_file in test_files:
        filename = test_file.name
        category, destination_dir = categorize_file(filename)


        if move_file_with_git(test_file, destination_dir, filename):
            moved_count += 1
        else:
            failed_count += 1



    if moved_count > 0:


if __name__ == "__main__":
    main()
