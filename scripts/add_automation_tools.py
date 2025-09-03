#!/usr/bin/env python3
"""Add powerful automation tools to Haive project.

This script adds additional development tools that can help automate
various aspects of the development workflow.
"""

import subprocess
from typing import List, Tuple


def run_command(cmd: list[str]) -> tuple[bool, str]:
    """Run a command and return success status and output."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr


def add_automation_tools():
    """Add automation tools as development dependencies."""
    tools = [
        # Documentation automation
        ("docformatter", "latest", "Format docstrings to PEP 257"),
        ("pydocstringformatter", "latest", "Another docstring formatter"),
        ("pyupgrade", "latest", "Automatically upgrade Python syntax"),
        # Code quality automation
        ("vulture", "latest", "Find dead code"),
        ("radon", "latest", "Code complexity metrics"),
        ("xenon", "latest", "Monitor code complexity"),
        ("prospector", "latest", "Python code analysis"),
        # Import management
        ("removestar", "latest", "Remove * imports"),
        ("unimport", "latest", "Remove unused imports"),
        # Type checking enhancements
        ("pytype", "latest", "Google's type checker"),
        ("pyre-check", "latest", "Facebook's type checker"),
        # Testing automation
        ("pytest-timeout", "latest", "Timeout for tests"),
        ("pytest-benchmark", "latest", "Benchmark tests"),
        ("pytest-mock", "latest", "Mock helpers (for external only)"),
        ("mutmut", "latest", "Mutation testing"),
        # Documentation generation
        ("pdoc", "latest", "Alternative doc generator"),
        ("mkdocs", "latest", "Project documentation"),
        ("mkdocstrings", "latest", "Auto doc from docstrings"),
        # Dependency management
        ("pipdeptree", "latest", "Dependency tree visualization"),
        ("poetry-plugin-export", "latest", "Export requirements"),
        ("deptry", "latest", "Find unused dependencies"),
        # Performance profiling
        ("py-spy", "latest", "Sampling profiler"),
        ("scalene", "latest", "High-performance profiler"),
        ("memray", "latest", "Memory profiler"),
    ]

    added = []
    skipped = []
    failed = []

    for tool, version, description in tools:

        # Check if already installed
        check_cmd = ["poetry", "show", tool]
        installed, _ = run_command(check_cmd)

        if installed:
            skipped.append(tool)
            continue

        # Add as dev dependency
        if version == "latest":
            add_cmd = ["poetry", "add", "--group", "dev", tool]
        else:
            add_cmd = ["poetry", "add", "--group", "dev", f"{tool}@{version}"]

        success, output = run_command(add_cmd)

        if success:
            added.append(tool)
        else:
            failed.append(tool)

    # Summary
    if added:
        for tool in added:
            pass

    if skipped:
        for tool in skipped:
            pass

    if failed:
        for tool in failed:
            pass

    # Usage examples
    if added:

        if "docformatter" in added:

        if "vulture" in added:

        if "radon" in added:

        if "pyupgrade" in added:

        if "unimport" in added:


def create_automation_config():
    """Create configuration files for automation tools."""
    # .vulture.py - whitelist for vulture
    vulture_config = """# Vulture whitelist
# Add items here that vulture incorrectly marks as unused

# Common false positives
_.model_config  # Pydantic v2
_.model_fields  # Pydantic v2
_.model_validate  # Pydantic v2

# FastAPI dependencies
_.Depends
_.Body
_.Query
_.Path

# Testing
_.pytest_plugins
_.pytestmark
"""

    # pyproject.toml additions
    pyproject_additions = """
[tool.vulture]
min_confidence = 80
paths = ["packages/"]
exclude = ["tests/", "examples/"]

[tool.radon]
cc_min = "B"
mi_min = "B"
exclude = "tests/*,examples/*"

[tool.unimport]
sources = ["packages/"]
exclude = "__pycache__|.git"
remove_all = true

[tool.docformatter]
recursive = true
wrap-summaries = 88
wrap-descriptions = 88
blank = true

[tool.pyupgrade]
py39_plus = true
keep_percent_format = false

[tool.mutmut]
paths_to_mutate = "packages/"
tests_dir = "tests/"
runner = "python -m pytest -x"
"""


if __name__ == "__main__":
    add_automation_tools()
    create_automation_config()
