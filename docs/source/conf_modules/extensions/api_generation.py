"""API documentation generation extensions.

This module configures extensions for automatically generating API documentation:
- AutoAPI: Auto-generate API docs from source
- Autodoc: Include docstrings in documentation
- Napoleon: Google/NumPy docstring support
- Type hints: Enhanced type hint documentation
"""

from typing import Any


def get_config(
    enable_autoapi: bool = True,
    enable_autodoc: bool = True,
    enable_napoleon: bool = True,
    enable_typehints: bool = True,
    packages: list[str] | None = None,
) -> dict[str, Any]:
    """Get API generation extension configuration.

    Args:
        enable_autoapi: Enable AutoAPI extension
        enable_autodoc: Enable autodoc extension
        enable_napoleon: Enable Napoleon (Google docstrings)
        enable_typehints: Enable enhanced type hints
        packages: List of packages to document

    Returns:
        Dictionary with API generation configuration
    """
    config = {}
    extensions = []

    # Core API documentation extensions
    if enable_autodoc:
        extensions.append("sphinx.ext.autodoc")
        config.update(_get_autodoc_config())

    if enable_napoleon:
        extensions.append("sphinx.ext.napoleon")
        config.update(_get_napoleon_config())

    if enable_typehints:
        extensions.append("sphinx_autodoc_typehints")
        config.update(_get_typehints_config())

    if enable_autoapi:
        extensions.append("autoapi.extension")
        config.update(_get_autoapi_config(packages))

    # Additional API extensions
    extensions.extend(
        [
            "sphinx.ext.viewcode",  # [source] links
            "sphinx.ext.linkcode",  # GitHub source links
            "sphinx.ext.autosummary",  # Summary tables
        ]
    )

    config["extensions"] = extensions
    return config


def _get_autodoc_config() -> dict[str, Any]:
    """Get autodoc configuration."""
    return {
        "autodoc_member_order": "groupwise",
        "autodoc_typehints": "both",  # Show in signature AND description
        "autodoc_preserve_defaults": True,  # Show default values
        "autodoc_default_options": {
            "members": True,
            "undoc-members": True,
            "show-inheritance": True,
            "special-members": "__init__,__call__",
        },
        "autodoc_mock_imports": [
            "torch",
            "tensorflow",
            # Add other optional dependencies
        ],
        "autodoc_warningiserror": False,  # Don't treat warnings as errors
        "autodoc_type_aliases": {
            "Agent": "haive.agents.base.Agent",
            "StateSchema": "haive.core.schema.StateSchema",
            "Engine": "haive.core.engine.Engine",
            "Tool": "haive.core.tools.Tool",
            "Graph": "haive.core.graph.BaseGraph",
        },
    }


def _get_napoleon_config() -> dict[str, Any]:
    """Get Napoleon (Google docstrings) configuration."""
    return {
        "napoleon_google_docstring": True,
        "napoleon_numpy_docstring": False,
        "napoleon_include_init_with_doc": True,
        "napoleon_include_private_with_doc": False,
        "napoleon_include_special_with_doc": True,
        "napoleon_use_admonition_for_examples": True,
        "napoleon_use_admonition_for_notes": True,
        "napoleon_use_admonition_for_references": True,
        "napoleon_use_ivar": True,
        "napoleon_use_param": True,
        "napoleon_use_rtype": True,
        "napoleon_use_keyword": True,
        "napoleon_preprocess_types": True,
        "napoleon_attr_annotations": True,
    }


def _get_typehints_config() -> dict[str, Any]:
    """Get type hints configuration."""
    return {
        "typehints_document_rtype": True,
        "typehints_use_signature": True,
        "typehints_use_signature_return": True,
        "typehints_format": "short",  # Use short format for readability
        "always_document_param_types": True,
    }


def _get_autoapi_config(packages: list[str] | None = None) -> dict[str, Any]:
    """Get AutoAPI configuration."""
    packages = packages or [
        "haive-core",
        "haive-agents",
        "haive-tools",
        "haive-games",
        "haive-dataflow",
        "haive-mcp",
    ]

    return {
        "autoapi_type": "python",
        "autoapi_dirs": [f"../../packages/{pkg}/src" for pkg in packages],
        "autoapi_root": "api",
        "autoapi_options": [
            "members",
            "show-inheritance",
            "show-module-summary",
            "special-members",  # Show __init__, __call__, etc.
            "private-members",  # Show documented private methods
        ],
        "autoapi_keep_files": True,
        "autoapi_add_toctree_entry": True,
        "autoapi_member_order": "groupwise",
        "autoapi_python_class_content": "both",
        "autoapi_python_use_implicit_namespaces": True,
        "autoapi_generate_api_docs": True,
        "autoapi_template_dir": "_templates/autoapi",
        "autoapi_ignore": [
            "**/__pycache__/**",
            "**/*.pyc",
            "**/*.pyo",
            "**/test_*.py",
            "**/tests/**",
            "**/*_test.py",
            "**/demo*.py",
            "**/debug*.py",
            "**/examples/**",
            "**/scripts/**",
            "**/.venv/**",
            "**/app.py",
            "**/main.py",
            "**/cli.py",
        ],
    }


def get_minimal_config() -> dict[str, Any]:
    """Get minimal API generation configuration."""
    return get_config(
        enable_autoapi=False,
        enable_typehints=False,
    )


def get_standard_config() -> dict[str, Any]:
    """Get standard API generation configuration."""
    return get_config()


def get_full_config() -> dict[str, Any]:
    """Get full API generation configuration with all features."""
    return get_config(
        enable_autoapi=True,
        enable_autodoc=True,
        enable_napoleon=True,
        enable_typehints=True,
    )
