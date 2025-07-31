"""Sphinx Configuration Builder - Generate modular conf.py files.

This module helps create different types of Sphinx configurations:
- Minimal: Just the essentials
- Standard: Common features for most projects
- Full: All features including advanced extensions
- Custom: Pick and choose features
"""

from pathlib import Path


class SphinxConfigBuilder:
    """Build Sphinx configurations from modular components."""

    def __init__(self, project_name: str = "Haive", author: str = "William R. Astley"):
        self.project_name = project_name
        self.author = author
        self.components = []

    def add_core(
        self, version: str = "1.0", release: str = "1.0.0"
    ) -> "SphinxConfigBuilder":
        """Add core project configuration."""
        self.components.append(
            f"""
# ==============================================================================
# Project Information
# ==============================================================================

project = "{self.project_name}"
author = "{self.author}"
copyright = f"{{datetime.now().year}}, {self.author}"
version = "{version}"
release = "{release}"

# Master document
master_doc = 'index'
language = 'en'
"""
        )
        return self

    def add_paths(self, packages: list[str] | None = None) -> "SphinxConfigBuilder":
        """Add path configuration."""
        packages = packages or [
            "haive-core",
            "haive-agents",
            "haive-tools",
            "haive-games",
            "haive-dataflow",
            "haive-mcp",
        ]

        packages_str = ",\n    ".join(f'"{p}"' for p in packages)

        self.components.append(
            f"""
# ==============================================================================
# Path Setup
# ==============================================================================

import sys
from pathlib import Path

# Get paths
docs_dir = Path(__file__).parent.parent
workspace_dir = docs_dir.parent
packages_dir = workspace_dir / "packages"

# Add package paths
package_names = [
    {packages_str}
]

for package in package_names:
    src_path = packages_dir / package / "src"
    if src_path.exists():
        sys.path.insert(0, str(src_path))

# Exclude patterns
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "**/__pycache__"]
"""
        )
        return self

    def add_basic_extensions(self) -> "SphinxConfigBuilder":
        """Add basic Sphinx extensions."""
        self.components.append(
            """
# ==============================================================================
# Basic Extensions
# ==============================================================================

extensions = [
    # Core Sphinx
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",

    # Enhanced features
    "sphinx_copybutton",
    "myst_parser",
]

# Napoleon - Google docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True

# Autodoc
autodoc_member_order = "bysource"
autodoc_typehints = "description"
autodoc_default_options = {
    "members": True,
    "show-inheritance": True,
}

# MyST
myst_enable_extensions = ["deflist", "tasklist", "colon_fence"]

# Intersphinx
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "langchain": ("https://python.langchain.com/", None),
    "pydantic": ("https://docs.pydantic.dev/", None),
}

# Source suffix
source_suffix = {".rst": "restructuredtext", ".md": "markdown"}
"""
        )
        return self

    def add_autoapi(self) -> "SphinxConfigBuilder":
        """Add AutoAPI extension configuration."""
        self.components.append(
            """
# ==============================================================================
# AutoAPI Configuration
# ==============================================================================

extensions.append("autoapi.extension")

autoapi_dirs = []
for package in package_names:
    src_path = packages_dir / package / "src"
    if src_path.exists():
        autoapi_dirs.append(str(src_path))

autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
    "imported-members",
]

autoapi_ignore = ["**/test_*.py", "**/tests/**", "**/*_test.py"]
autoapi_python_class_content = "both"
autoapi_member_order = "bysource"
autoapi_keep_files = True
"""
        )
        return self

    def add_theme(self, theme: str = "furo") -> "SphinxConfigBuilder":
        """Add theme configuration."""
        if theme == "furo":
            self.components.append(
                """
# ==============================================================================
# Theme Configuration
# ==============================================================================

html_theme = "furo"
html_title = f"{project} Documentation"
html_static_path = ["_static"]

html_theme_options = {
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
    "light_css_variables": {
        "color-brand-primary": "#0066cc",
        "color-brand-content": "#0066cc",
    },
}
"""
            )
        elif theme == "sphinx_rtd_theme":
            self.components.append(
                """
# ==============================================================================
# Theme Configuration
# ==============================================================================

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

html_theme_options = {
    "navigation_depth": 4,
    "collapse_navigation": False,
    "sticky_navigation": True,
}
"""
            )
        return self

    def add_advanced_extensions(self) -> "SphinxConfigBuilder":
        """Add advanced extensions."""
        self.components.append(
            '''
# ==============================================================================
# Advanced Extensions
# ==============================================================================

extensions.extend([
    # Documentation quality
    "sphinx.ext.coverage",
    "sphinx.ext.doctest",
    "sphinx_autodoc_typehints",

    # Enhanced features
    "sphinx_design",
    "sphinx_tabs.tabs",
    "sphinx_togglebutton",
    "sphinx_favicon",

    # External integrations
    "sphinxcontrib.mermaid",
    "sphinx_sitemap",
    "sphinx_github_changelog",
])

# Autodoc typehints
typehints_document_rtype = True
always_document_param_types = True

# Doctest
doctest_global_setup = """
import numpy as np
import pandas as pd
from haive.core import *
"""

# Sitemap
html_baseurl = "https://haive.readthedocs.io/"
sitemap_url_scheme = "{lang}latest/{link}"
'''
        )
        return self

    def add_jupyter_support(self) -> "SphinxConfigBuilder":
        """Add Jupyter notebook support."""
        self.components.append(
            """
# ==============================================================================
# Jupyter Support
# ==============================================================================

extensions.extend([
    "jupyter_sphinx",
    "nbsphinx",
    "sphinx_jupyter",
])

# nbsphinx
nbsphinx_execute = "never"  # Don't execute notebooks during build
nbsphinx_allow_errors = True
nbsphinx_timeout = 300

# Exclude notebook checkpoints
exclude_patterns.extend([
    "**/.ipynb_checkpoints",
    "**/~*.ipynb",
])
"""
        )
        return self

    def build(self) -> str:
        """Build the complete configuration."""
        header = f'''"""Sphinx configuration for {self.project_name}.

Generated by SphinxConfigBuilder.
"""

from datetime import datetime
'''

        # Add imports if needed
        if any("logging" in comp for comp in self.components):
            header += "import logging\n"
        if any("warnings" in comp for comp in self.components):
            header += "import warnings\n"

        return header + "\n".join(self.components)

    def save(self, path: Path) -> None:
        """Save configuration to file."""
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.build())

    @classmethod
    def minimal(cls, project_name: str = "Project", author: str = "Author") -> str:
        """Create minimal configuration."""
        builder = cls(project_name, author)
        return builder.add_core().add_paths().add_basic_extensions().add_theme().build()

    @classmethod
    def standard(cls, project_name: str = "Project", author: str = "Author") -> str:
        """Create standard configuration with common features."""
        builder = cls(project_name, author)
        return (
            builder.add_core()
            .add_paths()
            .add_basic_extensions()
            .add_autoapi()
            .add_theme()
            .add_advanced_extensions()
            .build()
        )

    @classmethod
    def full(cls, project_name: str = "Project", author: str = "Author") -> str:
        """Create full configuration with all features."""
        builder = cls(project_name, author)
        return (
            builder.add_core()
            .add_paths()
            .add_basic_extensions()
            .add_autoapi()
            .add_theme()
            .add_advanced_extensions()
            .add_jupyter_support()
            .build()
        )


# Convenience functions
def create_minimal_conf() -> str:
    """Create a minimal conf.py."""
    return SphinxConfigBuilder.minimal("Haive", "William R. Astley")


def create_standard_conf() -> str:
    """Create a standard conf.py."""
    return SphinxConfigBuilder.standard("Haive", "William R. Astley")


def create_full_conf() -> str:
    """Create a full-featured conf.py."""
    return SphinxConfigBuilder.full("Haive", "William R. Astley")


if __name__ == "__main__":
    # Example: Generate different configurations

    # Minimal
    minimal = create_minimal_conf()
    Path("conf_minimal.py").write_text(minimal)

    # Standard
    standard = create_standard_conf()
    Path("conf_standard.py").write_text(standard)

    # Full
    full = create_full_conf()
    Path("conf_full.py").write_text(full)

    # Custom
    custom = (
        SphinxConfigBuilder("MyProject", "My Name")
        .add_core("2.0", "2.0.1")
        .add_paths(["mypackage"])
        .add_basic_extensions()
        .add_theme("sphinx_rtd_theme")
        .build()
    )
    Path("conf_custom.py").write_text(custom)
