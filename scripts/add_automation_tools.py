#!/usr/bin/env python3
"""Add powerful automation tools to Haive project.

This script adds additional development tools that can help automate
various aspects of the development workflow.
"""

import subprocess
import sys
from typing import List, Tuple


def run_command(cmd: List[str]) -> Tuple[bool, str]:
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

    print("🚀 Adding Powerful Automation Tools to Haive\n")

    added = []
    skipped = []
    failed = []

    for tool, version, description in tools:
        print(f"📦 Adding {tool} - {description}...")

        # Check if already installed
        check_cmd = ["poetry", "show", tool]
        installed, _ = run_command(check_cmd)

        if installed:
            print(f"   ✓ Already installed\n")
            skipped.append(tool)
            continue

        # Add as dev dependency
        if version == "latest":
            add_cmd = ["poetry", "add", "--group", "dev", tool]
        else:
            add_cmd = ["poetry", "add", "--group", "dev", f"{tool}@{version}"]

        success, output = run_command(add_cmd)

        if success:
            print(f"   ✅ Successfully added {tool}\n")
            added.append(tool)
        else:
            print(f"   ❌ Failed to add {tool}: {output}\n")
            failed.append(tool)

    # Summary
    print("\n" + "=" * 60)
    print("📊 Summary:\n")
    print(f"✅ Added: {len(added)} tools")
    if added:
        for tool in added:
            print(f"   - {tool}")

    print(f"\n⏭️  Skipped (already installed): {len(skipped)} tools")
    if skipped:
        for tool in skipped:
            print(f"   - {tool}")

    print(f"\n❌ Failed: {len(failed)} tools")
    if failed:
        for tool in failed:
            print(f"   - {tool}")

    # Usage examples
    if added:
        print("\n" + "=" * 60)
        print("💡 Quick Usage Examples:\n")

        if "docformatter" in added:
            print("# Format docstrings:")
            print("poetry run docformatter --in-place packages/haive-core/src/")
            print()

        if "vulture" in added:
            print("# Find dead code:")
            print("poetry run vulture packages/ --min-confidence 80")
            print()

        if "radon" in added:
            print("# Code complexity:")
            print("poetry run radon cc packages/ -a -nc")
            print()

        if "pyupgrade" in added:
            print("# Upgrade Python syntax:")
            print("poetry run pyupgrade --py39-plus packages/**/*.py")
            print()

        if "unimport" in added:
            print("# Remove unused imports:")
            print("poetry run unimport --remove-all packages/")
            print()


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

    print("\n📝 Configuration suggestions:")
    print("\nAdd to .vulture.py:")
    print(vulture_config)
    print("\nAdd to pyproject.toml:")
    print(pyproject_additions)


if __name__ == "__main__":
    add_automation_tools()
    create_automation_config()
