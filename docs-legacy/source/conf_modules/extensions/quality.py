"""Quality and testing extensions.

This module configures extensions for documentation quality and testing:
- Doctest: Test code examples in documentation
- Coverage: Documentation coverage reports
- TODO tracking: TODO list generation
- Spell checking: Spell check documentation
- Link checking: Validate external links
"""

from __future__ import annotations

from typing import Any


def get_config(
    enable_doctest: bool = True,
    enable_coverage: bool = True,
    enable_todo: bool = True,
    enable_linkcheck: bool = False,
    enable_spelling: bool = False,
) -> dict[str, Any]:
    """Get quality and testing extension configuration.

    Args:
        enable_doctest: Enable doctest for testing code examples
        enable_coverage: Enable documentation coverage reports
        enable_todo: Enable TODO list generation and tracking
        enable_linkcheck: Enable link checking (can be slow)
        enable_spelling: Enable spell checking (requires additional setup)

    Returns:
        Dictionary with quality configuration
    """
    config = {}
    extensions = []

    # Core testing extensions
    if enable_doctest:
        extensions.append("sphinx.ext.doctest")
        config.update(_get_doctest_config())

    if enable_coverage:
        extensions.append("sphinx.ext.coverage")
        config.update(_get_coverage_config())

    if enable_todo:
        extensions.append("sphinx.ext.todo")
        config.update(_get_todo_config())

    # Optional quality extensions
    if enable_linkcheck:
        # Note: linkcheck is a builder, not an extension
        # Use: sphinx-build -b linkcheck
        pass

    if enable_spelling:
        extensions.append("sphinxcontrib.spelling")
        config.update(_get_spelling_config())

    config["extensions"] = extensions
    return config


def _get_doctest_config() -> dict[str, Any]:
    """Get doctest configuration."""
    return {
        "doctest_global_setup": """
# Common imports for all doctests
import sys
import os
from pathlib import Path

# Add package paths for imports
workspace_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(workspace_dir))

# Add all package source paths
packages = ["haive-core", "haive-agents", "haive-tools", "haive-games", "haive-mcp", "haive-dataflow"]
for pkg in packages:
    src_path = workspace_dir / "packages" / pkg / "src"
    if src_path.exists():
        sys.path.insert(0, str(src_path))

# Essential Haive imports
try:
    from haive.core.engine.aug_llm import AugLLMConfig
    from haive.agents.simple.agent import SimpleAgent
except ImportError:
    pass  # Skip if packages not available during doctest
""",
        "doctest_test_doctest_blocks": "default",  # Test .. doctest:: blocks
        "doctest_global_cleanup": "",  # Cleanup after doctests
    }


def _get_coverage_config() -> dict[str, Any]:
    """Get documentation coverage configuration."""
    return {
        "coverage_write_headline": False,  # Don't write "Undocumented" headline
        "coverage_show_missing_items": True,  # Show what's missing
        "coverage_ignore_modules": [
            "haive.*.tests.*",  # Ignore test modules
            "haive.*.__main__",  # Ignore main modules
            "haive.*.migrations.*",  # Ignore migration modules
        ],
        "coverage_ignore_functions": [
            "__repr__",
            "__str__",
            "__init__",  # Ignore common dunder methods
        ],
    }


def _get_todo_config() -> dict[str, Any]:
    """Get TODO extension configuration."""
    return {
        "todo_include_todos": True,  # Include TODO items in output
        "todo_emit_warnings": False,  # Don't emit warnings for TODOs
        "todo_link_only": False,  # Show full TODO text, not just links
    }


def _get_spelling_config() -> dict[str, Any]:
    """Get spell checking configuration."""
    return {
        "spelling_lang": "en_US",
        "spelling_word_list_filename": "spelling_wordlist.txt",
        "spelling_show_suggestions": True,
        "spelling_ignore_pypi_package_names": True,
        "spelling_ignore_wiki_words": True,
        "spelling_ignore_acronyms": True,
        "spelling_ignore_python_builtins": True,
        "spelling_ignore_importable_modules": True,
    }


def get_linkcheck_config() -> dict[str, Any]:
    """Get link checking configuration.

    Note: This is used with sphinx-build -b linkcheck, not as an extension.
    """
    return {
        "linkcheck_ignore": [
            r"http://localhost:\d+/",  # Ignore localhost links
            r"https://github\.com/.*/edit/.*",  # Ignore edit links
            r"mailto:.*",  # Ignore email links
        ],
        "linkcheck_timeout": 10,
        "linkcheck_retries": 2,
        "linkcheck_workers": 5,
    }


def get_minimal_config() -> dict[str, Any]:
    """Get minimal quality configuration."""
    return get_config(
        enable_doctest=False,
        enable_coverage=False,
        enable_todo=True,
        enable_linkcheck=False,
        enable_spelling=False,
    )


def get_standard_config() -> dict[str, Any]:
    """Get standard quality configuration."""
    return get_config(
        enable_doctest=True,
        enable_coverage=True,
        enable_todo=True,
        enable_linkcheck=False,
        enable_spelling=False,
    )


def get_full_config() -> dict[str, Any]:
    """Get full quality configuration."""
    return get_config(
        enable_doctest=True,
        enable_coverage=True,
        enable_todo=True,
        enable_linkcheck=True,
        enable_spelling=True,
    )
