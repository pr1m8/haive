"""Core Sphinx extensions configuration.

This module configures essential Sphinx extensions including:
- autodoc
- napoleon
- viewcode
- intersphinx
- todo
- duration
- coverage
"""

from typing import Any


def get_config() -> dict[str, Any]:
    """Get standard core Sphinx extensions configuration."""
    return _get_config_impl(minimal=False)


def get_minimal_config() -> dict[str, Any]:
    """Get minimal core Sphinx extensions configuration."""
    return _get_config_impl(minimal=True)


def get_standard_config() -> dict[str, Any]:
    """Get standard core Sphinx extensions configuration."""
    return _get_config_impl(minimal=False)


def get_full_config() -> dict[str, Any]:
    """Get full core Sphinx extensions configuration."""
    return _get_config_impl(minimal=False)


def _get_config_impl(minimal: bool = False) -> dict[str, Any]:
    """Get core Sphinx extensions configuration.

    Args:
        minimal: If True, only includes essential extensions

    Returns:
        Dictionary with extensions configuration
    """
    config = {}

    # Essential extensions
    extensions = [
        "sphinx.ext.autodoc",  # Auto-generate API docs
        "sphinx.ext.napoleon",  # Google/NumPy docstring support
        "sphinx.ext.viewcode",  # Add source code links
        "sphinx.ext.intersphinx",  # Link to other projects
    ]

    if not minimal:
        extensions.extend(
            [
                "sphinx.ext.todo",  # TODO directives
                "sphinx.ext.duration",  # Build duration tracking
                "sphinx.ext.coverage",  # Documentation coverage
                "sphinx.ext.doctest",  # Doctest support
                "sphinx.ext.ifconfig",  # Conditional content
                "sphinx.ext.imgmath",  # Math support
                "sphinx.ext.mathjax",  # Better math rendering
                "sphinx.ext.githubpages",  # GitHub pages support
                "sphinx.ext.inheritance_diagram",  # Class diagrams
                "sphinx.ext.autosummary",  # Auto summary tables
                "sphinx.ext.extlinks",  # External link shortcuts
            ], )

    config["extensions"] = extensions

    # Napoleon configuration - Google docstrings
    config["napoleon_google_docstring"] = True
    config["napoleon_numpy_docstring"] = False
    config["napoleon_include_init_with_doc"] = True
    config["napoleon_include_private_with_doc"] = False
    config["napoleon_include_special_with_doc"] = True
    config["napoleon_use_admonition_for_examples"] = True
    config["napoleon_use_admonition_for_notes"] = True
    config["napoleon_use_admonition_for_references"] = True
    config["napoleon_use_ivar"] = True
    config["napoleon_use_param"] = True
    config["napoleon_use_rtype"] = True
    config["napoleon_type_aliases"] = {
        "array-like": ":term:`array-like <numpy.ndarray>`",
        "array_like": ":term:`array_like <numpy.ndarray>`",
    }

    # Autodoc configuration
    config["autodoc_default_options"] = {
        "members": True,
        "member-order": "bysource",
        "special-members": "__init__",
        "undoc-members": True,
        "exclude-members": "__weakref__",
        "show-inheritance": True,
        "inherited-members": False,
    }

    config["autodoc_typehints"] = "description"
    config["autodoc_typehints_format"] = "short"
    config["autodoc_type_aliases"] = {
        "DataFrame": "pandas.DataFrame",
        "Series": "pandas.Series",
        "ndarray": "numpy.ndarray",
    }

    # Intersphinx configuration
    config["intersphinx_mapping"] = {
        "python": ("https://docs.python.org/3/", None),
        "numpy": ("https://numpy.org/doc/stable/", None),
        "pandas": ("https://pandas.pydata.org/docs/", None),
        "sklearn": ("https://scikit-learn.org/stable/", None),
        "torch": ("https://pytorch.org/docs/stable/", None),
        "langchain": ("https://python.langchain.com/", None),
        "pydantic": ("https://docs.pydantic.dev/", None),
    }

    if not minimal:
        # TODO extension
        config["todo_include_todos"] = True
        config["todo_emit_warnings"] = True
        config["todo_link_only"] = False

        # Coverage extension
        config["coverage_ignore_modules"] = []
        config["coverage_ignore_classes"] = []
        config["coverage_ignore_functions"] = []
        config["coverage_ignore_pyobjects"] = []
        config["coverage_write_headline"] = True
        config["coverage_skip_undoc_in_source"] = True

        # Extlinks for common external links
        config["extlinks"] = {
            "issue":
            ("https://github.com/username/haive/issues/%s", "issue %s"),
            "pr": ("https://github.com/username/haive/pull/%s", "PR %s"),
            "commit":
            ("https://github.com/username/haive/commit/%s", "commit %s"),
        }

    return config


def get_minimal_extensions() -> list[str]:
    """Get minimal list of extensions for simple projects.

    Returns:
        List of essential extension names
    """
    return [
        "sphinx.ext.autodoc",
        "sphinx.ext.napoleon",
        "sphinx.ext.viewcode",
        "sphinx.ext.intersphinx",
    ]
