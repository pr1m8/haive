# Clean Modular Sphinx Configuration Proposal

## 🎯 Goal: Modular but Clear

### Proposed Structure

```
docs/source/
├── conf.py                  # Main entry point - SIMPLE
├── _conf/                   # Clear configuration modules
│   ├── __init__.py         # Empty
│   ├── project.py          # Project metadata
│   ├── extensions.py       # Extension configuration
│   ├── paths.py            # Path configuration
│   ├── theme.py            # Theme settings
│   ├── api.py              # AutoAPI settings
│   └── mocks.py            # Mock imports
```

## 📄 Example Implementation

### conf.py (Main Entry - Clean & Simple)

```python
"""Sphinx configuration for Haive documentation."""

# Import modular configs
from _conf.project import *
from _conf.extensions import *
from _conf.paths import *
from _conf.theme import *
from _conf.api import *
from _conf.mocks import *

# Any overrides or special config here
# This file stays small and just orchestrates
```

### \_conf/project.py

```python
"""Project metadata configuration."""

# Project information
project = "Haive AI Agent Framework"
copyright = "2024, Haive Team"
author = "Haive Team"
version = "1.0"
release = "1.0.0"

# Language settings
language = "en"
```

### \_conf/extensions.py

```python
"""Sphinx extensions configuration."""

# Core extensions
extensions = [
    # === Sphinx Built-in ===
    "sphinx.ext.autodoc",         # Extract docstrings
    "sphinx.ext.napoleon",        # Google/NumPy docstring support
    "sphinx.ext.viewcode",        # Add source code links
    "sphinx.ext.intersphinx",     # Link to other docs

    # === API Documentation ===
    "autoapi.extension",          # Auto-generate API docs

    # === Content Enhancement ===
    "myst_parser",                # Markdown support
    "sphinx_copybutton",          # Copy button for code blocks

    # === Custom Extensions ===
    "_extensions.haive_sphinx_ext",  # Our custom extensions
]

# Extension-specific configs
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
```

### \_conf/paths.py

```python
"""Path configuration for documentation."""

from pathlib import Path

# Base paths
DOCS_DIR = Path(__file__).parent.parent
SOURCE_DIR = DOCS_DIR
BUILD_DIR = DOCS_DIR.parent / "build"
PROJECT_ROOT = DOCS_DIR.parent.parent

# Templates and static files
templates_path = ["_templates"]
html_static_path = ["_static"]

# Exclude patterns
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "**/__pycache__",
    "**/test_*.py",
]

# Source suffix
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}
```

### \_conf/theme.py

```python
"""Theme configuration."""

# Theme selection
html_theme = "furo"  # or "sphinx_rtd_theme"

# Theme options
html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "#007acc",
        "color-brand-content": "#007acc",
    },
    "dark_css_variables": {
        "color-brand-primary": "#00d9ff",
        "color-brand-content": "#00d9ff",
    },
}

# Logo and favicon
html_logo = "_static/images/haive-logo-light.svg"
html_favicon = "_static/images/favicon.ico"

# Sidebar
html_sidebars = {
    "**": [
        "sidebar/brand.html",
        "sidebar/search.html",
        "sidebar/navigation.html",
    ]
}
```

### \_conf/api.py

```python
"""AutoAPI configuration for automatic documentation generation."""

from pathlib import Path

# AutoAPI settings
autoapi_type = "python"
autoapi_dirs = [
    "../../packages/haive-core/src",
    "../../packages/haive-agents/src",
    "../../packages/haive-tools/src",
]

autoapi_root = "api"
autoapi_keep_files = True
autoapi_add_toctree_entry = True

# Control what gets documented
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
    "imported-members",
]

# Ignore patterns for AutoAPI
autoapi_ignore = [
    "**/test_*.py",
    "**/conftest.py",
    "**/*_test.py",
    "**/tests/**",
]
```

### \_conf/mocks.py

```python
"""Mock imports for missing dependencies during doc build."""

# External dependencies to mock
autodoc_mock_imports = [
    # Data science
    "numpy",
    "pandas",
    "scipy",

    # ML frameworks
    "tensorflow",
    "torch",
    "transformers",

    # Other tools
    "langchain",
    "openai",
    "anthropic",

    # Add your mock imports here...
]

# Also add any discovered mocks
try:
    from _conf.discovered_mocks import discovered_mocks
    autodoc_mock_imports.extend(discovered_mocks)
except ImportError:
    pass
```

## 🎯 Benefits of This Approach

1. **Clear Separation**: Each file has ONE responsibility
2. **Easy to Find**: Need to change theme? Look in theme.py
3. **Easy to Test**: Can import and test each module separately
4. **No Deep Nesting**: Just one level: conf.py → \_conf/module.py
5. **Self-Documenting**: File names tell you what's inside

## 🚀 Migration Path

1. Create `_conf/` directory
2. Move configs to appropriate modules
3. Update conf.py to import from modules
4. Test build still works
5. Delete old conf_modules/ mess

## 📝 Documentation for Each Module

Each module should have:

- Clear docstring explaining purpose
- Comments for non-obvious settings
- Examples where helpful

This gives you modularity without the confusion!
