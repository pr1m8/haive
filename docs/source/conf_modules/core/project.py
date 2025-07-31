"""Project information configuration for Sphinx.

This module defines project metadata including:
- Project name and author
- Version information
- Copyright
- Language settings
"""

from datetime import datetime
from typing import Any


def get_config(
    project_name: str = "Haive",
    author: str = "William R. Astley",
    version: str = "1.0",
    release: str = "1.0.0",
    language: str = "en",
) -> dict[str, Any]:
    """Get project information configuration.

    Args:
        project_name: Name of the project
        author: Project author(s)
        version: Short version string
        release: Full release string
        language: Documentation language

    Returns:
        Dictionary with project configuration
    """
    config = {}

    # Basic project info
    config["project"] = project_name
    config["author"] = author

    # Copyright with current year
    current_year = datetime.now().year
    config["copyright"] = f"2025-{current_year}, {author}"

    # Version info
    config["version"] = version
    config["release"] = release

    # Language
    config["language"] = language

    # Master document
    config["master_doc"] = "index"

    # Source suffix
    config["source_suffix"] = {
        ".rst": "restructuredtext",
        ".md": "markdown",
    }

    # Nitpicky mode - warn about missing references
    config["nitpicky"] = True
    config["nitpick_ignore"] = [
        # Common ignore patterns
        ("py:class", "type"),
        ("py:class", "optional"),
        ("py:class", "Any"),
        ("py:class", "Dict"),
        ("py:class", "List"),
        ("py:class", "Tuple"),
        ("py:class", "Union"),
        ("py:class", "Optional"),
        ("py:class", "Callable"),
    ]

    # Highlighting
    config["pygments_style"] = "sphinx"
    config["pygments_dark_style"] = "monokai"

    # Figure numbering
    config["numfig"] = True
    config["numfig_secnum_depth"] = 2

    # Code block settings
    config["highlight_language"] = "python3"
    config["highlight_options"] = {
        "stripall": False,
        "stripnl": False,
    }

    return config


def get_minimal_config() -> dict[str, Any]:
    """Get minimal project configuration.

    Returns:
        Dictionary with minimal project settings
    """
    return get_config(
        project_name="Project", author="Author", version="0.1", release="0.1.0"
    )
