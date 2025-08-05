"""Content processing extensions.

This module configures extensions for processing different content types:
- MyST: Markdown support with MyST parser
- Jupyter: Notebook integration and execution
- Example galleries: Auto-generate example galleries
- Jinja2: Template processing for dynamic content
- External TOC: External table of contents management
"""

from __future__ import annotations

from typing import Any


def get_config(
    enable_myst: bool = True,
    enable_jupyter: bool = True,
    enable_gallery: bool = True,
    enable_jinja: bool = True,
    enable_external_toc: bool = True,
    enable_live_code: bool = False,
    packages: list[str] | None = None,
) -> dict[str, Any]:
    """Get content processing extension configuration.

    Args:
        enable_myst: Enable MyST markdown parser
        enable_jupyter: Enable Jupyter notebook integration
        enable_gallery: Enable example gallery generation
        enable_jinja: Enable Jinja2 template processing
        enable_external_toc: Enable external table of contents
        enable_live_code: Enable live code execution in browser
        packages: List of packages with examples

    Returns:
        Dictionary with content processing configuration
    """
    config = {}
    extensions = []

    # MyST parser for markdown
    if enable_myst:
        extensions.append("myst_nb")  # Includes MyST + Jupyter support
        config.update(_get_myst_config())

    # Jupyter notebook integration
    if enable_jupyter:
        if "myst_nb" not in extensions:
            extensions.append("myst_nb")
        config.update(_get_jupyter_config())

    # Example galleries
    if enable_gallery:
        extensions.append("sphinx_gallery.gen_gallery")
        config.update(_get_gallery_config(packages))

    # Template processing
    if enable_jinja:
        extensions.append("sphinx_jinja2")
        config.update(_get_jinja_config())

    # External TOC
    if enable_external_toc:
        extensions.append("sphinx_external_toc")
        config.update(_get_external_toc_config())

    # Live code execution
    if enable_live_code:
        extensions.append("sphinx_thebe")  # Live code execution in browser
        # config.update(_get_thebe_config())  # DISABLED: Conflicts with extension registration

    config["extensions"] = extensions
    return config


def _get_myst_config() -> dict[str, Any]:
    """Get MyST parser configuration."""
    return {
        "myst_enable_extensions": [
            "deflist",  # Definition lists
            "tasklist",  # Task lists with checkboxes
            "colon_fence",  # ::: code fences
            "smartquotes",  # Smart quotes
            "linkify",  # Auto-link URLs
            "strikethrough",  # ~~strikethrough~~
            "dollarmath",  # $math$ and $$math$$
            "substitution",  # |substitution|
            "attrs_inline",  # {attrs} for inline elements
            "attrs_block",  # {attrs} for block elements
        ],
        "myst_url_schemes": ["http", "https", "ftp", "mailto"],
        "myst_heading_anchors":
        3,  # Auto-generate anchors for headings
    }


def _get_jupyter_config() -> dict[str, Any]:
    """Get Jupyter notebook configuration."""
    return {
        "jupyter_cache": "../../.jupyter_cache",
        "jupyter_execute_notebooks": "cache",  # Cache execution results
        "execution_timeout": 600,  # 10 minutes for complex examples
        "execution_show_tb": "short",  # Show short tracebacks on errors
        "execution_in_temp": False,  # Execute in project directory
        "nb_execution_mode": "cache",
        "nb_execution_timeout": 300,
        "nb_execution_raise_on_error": False,
    }


def _get_gallery_config(packages: list[str] | None = None) -> dict[str, Any]:
    """Get example gallery configuration."""
    packages = packages or [
        "haive-agents",
        "haive-games",
        "haive-mcp",
    ]

    examples_dirs = []
    gallery_dirs = []

    for pkg in packages:
        examples_dir = f"../../packages/{pkg}/examples"
        gallery_dir = f"auto_examples/{pkg.split('-')[1]}"
        examples_dirs.append(examples_dir)
        gallery_dirs.append(gallery_dir)

    return {
        "sphinx_gallery_conf": {
            "examples_dirs": examples_dirs,
            "gallery_dirs": gallery_dirs,
            "filename_pattern": "/.*tutorial|.*guide|.*example",
            "ignore_pattern": "__init__.py|debug_*|test_*",
            "download_all_examples": True,
            "show_memory": True,
            "remove_config_comments": True,
            "expected_failing_examples": [],
            "thumbnail_size": (300, 200),
            "subsection_order": "ExplicitOrder",
            "within_subsection_order": "FileNameSortKey",
            "show_signature": True,
            "plot_gallery": False,  # We don't need matplotlib plots
            "execute_examples":
            False,  # Disable execution to avoid computational cost
            "run_code_after_examples": False,  # Don't run code after examples
            "first_notebook_cell": "%matplotlib inline",
            "last_notebook_cell": "# End of example",
            "promote_jupyter_magic": True,
            "binder": {
                "org": "haive",
                "repo": "haive",
                "branch": "main",
                "binderhub_url": "https://mybinder.org",
                "dependencies": ["../../pyproject.toml"],
            },
        },
    }


def _get_jinja_config() -> dict[str, Any]:
    """Get Jinja2 template processing configuration."""
    return {
        "jinja2_contexts": {
            "agent_demo": {
                # These will be imported from agent demo modules
            },
        },
        "jinja2_debug": False,
    }


def _get_external_toc_config() -> dict[str, Any]:
    """Get external table of contents configuration."""
    return {
        "external_toc_path": "_toc.yml",  # Use external TOC file (optional)
        "external_toc_exclude_missing":
        True,  # Don't break build for missing entries
    }


def _get_thebe_config() -> dict[str, Any]:
    """Get Thebe (live code) configuration."""
    return {
        "thebe_config": {
            "repository_url": "https://github.com/pr1m8/haive",
            "repository_branch": "main",
            "selector": ".thebe",
            "binderUrl": "https://mybinder.org",
        },
    }


def get_exec_config() -> dict[str, Any]:
    """Get code execution configuration."""
    return {
        "exec_code_working_dir": "../..",  # Project root
        "exec_code_example_dir": "examples/executed",
        "exec_code_source_folders": ["packages"],  # Where to look for imports
        "exec_code_add_conf_path": True,  # Add conf.py path to sys.path
    }


def get_exercise_config() -> dict[str, Any]:
    """Get interactive exercises configuration."""
    return {
        "exercise_include_exercises": True,  # Include exercises in output
        "exercise_include_solutions": True,  # Include solutions in output
    }


def get_proof_config() -> dict[str, Any]:
    """Get mathematical proofs configuration."""
    return {
        "proof_theorem_types": {
            "algorithm": "Algorithm",
            "axiom": "Axiom",
            "definition": "Definition",
            "example": "Example",
            "lemma": "Lemma",
            "theorem": "Theorem",
            "property": "Property",
        },
    }


def get_minimal_config() -> dict[str, Any]:
    """Get minimal content processing configuration."""
    return get_config(
        enable_myst=True,
        enable_jupyter=False,
        enable_gallery=False,
        enable_jinja=False,
        enable_external_toc=False,
        enable_live_code=False,
    )


def get_standard_config() -> dict[str, Any]:
    """Get standard content processing configuration."""
    return get_config(
        enable_myst=True,
        enable_jupyter=True,
        enable_gallery=True,
        enable_jinja=False,
        enable_external_toc=True,
        enable_live_code=False,
    )


def get_full_config() -> dict[str, Any]:
    """Get full content processing configuration."""
    config = get_config(
        enable_myst=True,
        enable_jupyter=True,
        enable_gallery=True,
        enable_jinja=True,
        enable_external_toc=True,
        enable_live_code=True,
    )

    # Add additional full-featured extensions
    config["extensions"].extend(
        [
            "sphinx_exercise",  # Interactive exercises
            "sphinx_proof",  # Mathematical proofs
        ], )

    config.update(get_exec_config())
    config.update(get_exercise_config())
    config.update(get_proof_config())

    return config
