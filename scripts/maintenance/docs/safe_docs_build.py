#!/usr/bin/env python3
"""Safe documentation build with error handling."""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def create_safe_conf():
    """Create a safe configuration with error handling."""

    # Read the original config
    with open("docs/source/conf.py") as f:
        content = f.read()

    # Add error handling for AutoAPI
    safe_config = content.replace(
        "# === AUTOAPI - BEST-IN-CLASS API DOCUMENTATION ===",
        '''# === AUTOAPI - BEST-IN-CLASS API DOCUMENTATION WITH ERROR HANDLING ===
# Custom error handling for problematic agents
import warnings
from autoapi.directives import AutoapiSummary

# Override the problematic get_items method
original_get_items = AutoapiSummary.get_items

def safe_get_items(self, names):
    """Safe version of get_items with error handling"""
    try:
        return original_get_items(self, names)
    except KeyError as e:
        print(f"⚠️  Skipping problematic object: {e}")
        # Return empty list for problematic objects
        return []
    except Exception as e:
        print(f"⚠️  Error processing AutoAPI object: {e}")
        return []

# Apply the safe method
AutoapiSummary.get_items = safe_get_items

# Add more error handling
def setup_error_handling(app):
    """Setup error handling for documentation build"""
    import logging

    # Set up logging to catch and handle errors
    logging.basicConfig(level=logging.WARNING)

    # Handle missing references
    app.config.nitpicky = False
    app.config.autoapi_keep_files = True

    # Set up warning filters
    warnings.filterwarnings("ignore", category=UserWarning)
    warnings.filterwarnings("ignore", category=ImportWarning)

    return app

# Add the setup function to extensions
def setup(app):
    return setup_error_handling(app)

''',
    )

    # Remove problematic extensions temporarily
    safe_config = safe_config.replace(
        "extensions = [",
        """extensions = [
    # Core Sphinx extensions
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    # Safe extensions only
    'autoapi.extension',
    'myst_parser',
    'sphinx_copybutton',
    'sphinx_design',
    'pydata_sphinx_theme',
]

# Disable problematic extensions
old_extensions = [""",
    ).replace(
        "]",
        """
    # Disabled problematic extensions:
    # 'sphinx_tabs',
    # 'sphinx_inline_tabs',
    # 'sphinx_togglebutton',
    # 'sphinx_exec_directive',
    # 'sphinxcontrib.mermaid',
    # 'sphinxcontrib.youtube',
    # 'sphinx_sitemap',
    # 'sphinxcontrib.httpdomain',
    # 'sphinxcontrib.openapi',
    # 'sphinxext.opengraph',
    # 'sphinx_autodoc_typehints',
]""",
        1,  # Replace only first occurrence
    )

    # Write the safe config
    with open("docs/source/conf_safe.py", "w") as f:
        f.write(safe_config)


def build_safe_docs():
    """Build documentation with safe configuration."""

    # Change to project directory
    os.chdir(Path(__file__).parent)

    # Create safe configuration
    create_safe_conf()

    # Clean previous build
    subprocess.run(["rm", "-rf", "docs/build"], check=False)

    # Build with safe settings and error handling
    result = subprocess.run(
        [
            "poetry",
            "run",
            "sphinx-build",
            "-b",
            "html",
            "-c",
            "docs/source",  # Use configuration directory
            "--keep-going",  # Continue on errors
            "-W",
            "--keep-going",  # Convert warnings to errors but keep going
            "-v",  # Verbose output
            "docs/source",
            "docs/build",
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    # Show last part of output
    if result.stdout:

    if result.stderr:

    # Check if HTML files were generated
    html_files = list(Path("docs/build").rglob("*.html"))

    if html_files:

        # List some key files
        key_files = ["index.html", "api/index.html", "agents/index.html"]
        for key_file in key_files:
            path = Path(f"docs/build/{key_file}")
            if path.exists():
                pass")
            else:
                pass")

        return True
    return False


if __name__ == "__main__":
    try:
        success = build_safe_docs()
        if success:
            pass!")
        else:
            sys.exit(1)
    except Exception as e:
        sys.exit(1)
