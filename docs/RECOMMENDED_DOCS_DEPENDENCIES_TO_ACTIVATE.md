# Recommended Documentation Dependencies to Activate

Based on the `poetry show --only docs` output, here are the most valuable dependencies that are installed but not currently used in `conf.py`:

## 🌟 High Priority - Immediate Value

### 1. **sphinx-autodoc-typehints** (3.1.0) ✅ Installed
**Purpose**: Automatically document type hints in function signatures
```python
extensions.append("sphinx_autodoc_typehints")

# Configuration
autodoc_typehints = "description"  # or "signature" or "both"
typehints_defaults = "comma"
```

### 2. **autodoc-pydantic** (2.2.0) ✅ Installed
**Purpose**: Beautiful documentation for Pydantic models (critical for Haive!)
```python
extensions.append("sphinxcontrib.autodoc_pydantic")

# Configuration
autodoc_pydantic_model_show_json = True
autodoc_pydantic_settings_show_json = False
autodoc_pydantic_model_show_config_summary = True
```

### 3. **sphinx-tabs** (3.4.7) ✅ Installed
**Purpose**: Tabbed content for showing examples in multiple formats
```python
extensions.append("sphinx_tabs.tabs")
# No configuration needed
```

### 4. **sphinx-prompt** (1.10.0) ✅ Installed
**Purpose**: Beautiful command-line examples with prompts
```python
extensions.append("sphinx_prompt")
# No configuration needed
```

### 5. **readthedocs-sphinx-search** (0.3.2) ✅ Installed
**Purpose**: Enhanced search for ReadTheDocs
```python
extensions.append("readthedocs_sphinx_search")
# No configuration needed
```

### 6. **sphinx-sitemap** (2.6.0) ✅ Installed
**Purpose**: Generate sitemap.xml for SEO
```python
extensions.append("sphinx_sitemap")

# Configuration
html_baseurl = "https://haive.readthedocs.io"
sitemap_url_scheme = "{link}"
```

### 7. **sphinxext-opengraph** (0.10.0) ✅ Installed
**Purpose**: Rich social media previews
```python
extensions.append("sphinxext.opengraph")

# Configuration
ogp_site_url = "https://haive.readthedocs.io"
ogp_site_name = "Haive Documentation"
ogp_image = "https://haive.readthedocs.io/_static/logo.png"
ogp_enable_meta_description = True
```

### 8. **sphinx-codeautolink** (0.15.2) ✅ Installed
**Purpose**: Automatically link code references to API docs
```python
extensions.append("sphinx_codeautolink")

# Configuration
codeautolink_global_preface = """
from haive.core import *
from haive.agents import *
from haive.tools import *
"""
```

## 🎯 Medium Priority - Enhanced Features

### 9. **myst-nb** (1.3.0) ✅ Installed
**Purpose**: Execute Jupyter notebooks as documentation
```python
extensions.append("myst_nb")

# Configuration
nb_execution_mode = "cache"
nb_execution_timeout = 60
nb_execution_excludepatterns = ["**/test_*.ipynb"]
jupyter_execute_notebooks = "cache"
```

### 10. **sphinx-inline-tabs** (2023.4.21) ✅ Installed
**Purpose**: Inline tabs for compact comparisons
```python
extensions.append("sphinx_inline_tabs")
# Works with MyST
```

### 11. **sphinx-togglebutton** (0.3.2) ✅ Installed
**Purpose**: Collapsible sections
```python
extensions.append("sphinx_togglebutton")
# No configuration needed
```

### 12. **sphinxcontrib-youtube** (1.4.1) ✅ Installed
**Purpose**: Embed YouTube videos
```python
extensions.append("sphinxcontrib.youtube")
# No configuration needed
```

### 13. **sphinx-last-updated-by-git** (0.3.8) ✅ Installed
**Purpose**: Show last git update time
```python
extensions.append("sphinx_last_updated_by_git")
# No configuration needed
```

### 14. **autodocsumm** (0.2.14) ✅ Installed
**Purpose**: Auto-generate summary tables for modules
```python
extensions.append("autodocsumm")
autodoc_default_options = {"autosummary": True}
```

## 🔧 Special Purpose - Use if Needed

### 15. **sphinxcontrib-mermaid** (1.0.0) ✅ Already configured!

### 16. **sphinx-needs** (5.1.0) ✅ Installed
**Purpose**: Requirements tracking (complex but powerful)
```python
extensions.append("sphinx_needs")
# Requires significant configuration
```

### 17. **jupytext** (1.17.2) ✅ Installed
**Purpose**: Convert between .py and .ipynb formats
```python
# Use with myst-nb for Python script notebooks
```

### 18. **sphinx-data-viewer** (0.1.5) ✅ Installed
**Purpose**: Display data tables interactively
```python
extensions.append("sphinx_data_viewer")
```

## 🚀 Recommended Configuration to Add

Add this to your `conf.py`:

```python
# Add these high-value extensions
extensions.extend([
    # Type documentation
    "sphinx_autodoc_typehints",
    "sphinxcontrib.autodoc_pydantic",
    
    # Enhanced display
    "sphinx_tabs.tabs",
    "sphinx_prompt",
    "sphinx_togglebutton",
    "autodocsumm",
    
    # Search and SEO
    "readthedocs_sphinx_search",
    "sphinx_sitemap",
    "sphinxext.opengraph",
    
    # Code linking
    "sphinx_codeautolink",
    
    # Media
    "sphinxcontrib.youtube",
    
    # Metadata
    "sphinx_last_updated_by_git",
    
    # Notebooks (if using)
    "myst_nb",
])

# Configure autodoc with type hints
autodoc_typehints = "description"
autodoc_typehints_format = "short"
typehints_defaults = "comma"
autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "undoc-members": True,
    "autosummary": True,  # For autodocsumm
}

# Pydantic configuration
autodoc_pydantic_model_show_json = True
autodoc_pydantic_settings_show_json = False
autodoc_pydantic_model_show_config_summary = True
autodoc_pydantic_model_show_field_summary = True
autodoc_pydantic_model_show_validator_summary = True

# Sitemap
html_baseurl = "https://haive.readthedocs.io"
sitemap_url_scheme = "{link}"

# OpenGraph
ogp_site_url = "https://haive.readthedocs.io"
ogp_site_name = "Haive - AI Agent Framework"
ogp_enable_meta_description = True

# Code autolink
codeautolink_global_preface = """
from haive.core import *
from haive.agents import *
from haive.tools import *
from haive.games import *
"""

# Notebook execution (if using myst-nb)
nb_execution_mode = "cache"
nb_execution_timeout = 60
jupyter_execute_notebooks = "cache"
jupyter_cache = ".jupyter_cache"
```

## 📊 Impact Analysis

Adding these extensions will provide:

1. **Better API Documentation**: Type hints and Pydantic models properly documented
2. **Enhanced User Experience**: Tabs, toggles, prompts for better content presentation
3. **Improved SEO**: Sitemap and OpenGraph for better search visibility
4. **Code Integration**: Auto-linking between examples and API docs
5. **Modern Features**: Video embedding, git timestamps, enhanced search

## ⚠️ Dependencies to Avoid

These are installed but might cause issues:

- **sphinx-autodoc2** - Conflicts with autoapi
- **sphinx-multiversion** - Complex setup, use ReadTheDocs versioning
- **sphinxcontrib-plantuml** - Requires Java, use Mermaid instead
- **language-tool-python** / **language-check** - Heavy grammar checkers
- **vale** - External binary dependency

## 🎯 Quick Win

Just add this minimal set for immediate improvement:

```python
extensions.extend([
    "sphinx_autodoc_typehints",
    "sphinxcontrib.autodoc_pydantic",
    "sphinx_tabs.tabs",
    "sphinx_prompt",
    "readthedocs_sphinx_search",
])

autodoc_typehints = "description"
```

This will significantly improve your documentation with minimal effort!