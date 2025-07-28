# Useful Documentation Dependencies for Haive

This guide analyzes the documentation dependencies available in the Haive project and recommends which ones would work well with the current Sphinx configuration.

## 📋 Table of Contents

1. [Currently Active Dependencies](#currently-active-dependencies)
2. [High-Priority Recommendations](#high-priority-recommendations)
3. [Category-Based Analysis](#category-based-analysis)
4. [Configuration Examples](#configuration-examples)
5. [Dependencies to Avoid](#dependencies-to-avoid)
6. [Missing Dependencies Worth Adding](#missing-dependencies-worth-adding)

## Currently Active Dependencies

Your `conf.py` currently uses these extensions effectively:

### ✅ Core Documentation
- **autoapi.extension** - Automatic API documentation generation
- **sphinx.ext.napoleon** - Google/NumPy docstring support
- **sphinx.ext.viewcode** - Source code links
- **sphinx.ext.intersphinx** - Cross-project references

### ✅ Enhancement Extensions
- **sphinx_copybutton** - Copy buttons for code blocks
- **sphinx_design** - Cards, tabs, grids, and other layouts
- **myst_parser** - Markdown support with MyST
- **sphinxcontrib.mermaid** - Mermaid diagram support

### ✅ Example Management
- **sphinx_gallery.gen_gallery** - Example gallery generation
- **sphinx_exec_directive** - Executable code blocks

## High-Priority Recommendations

Based on your AI agent framework needs, these dependencies would provide the most value:

### 1. **sphinx-autodoc-typehints** (Critical)
```python
# Add to extensions
"sphinx_autodoc_typehints"

# Configuration
autodoc_typehints = "description"  # or "signature" or "both"
autodoc_typehints_format = "short"
typehints_fully_qualified = False
always_document_param_types = True
```
**Why**: Automatically documents type hints in your function signatures. Essential for an AI framework with complex types.

### 2. **autodoc-pydantic** (Essential)
```python
# Add to extensions
"sphinxcontrib.autodoc_pydantic"

# Configuration
autodoc_pydantic_model_show_json = True
autodoc_pydantic_settings_show_json = False
autodoc_pydantic_model_show_config_summary = True
autodoc_pydantic_model_show_field_summary = True
```
**Why**: Since you use Pydantic extensively (StateSchema, configs), this provides beautiful documentation for your models.

### 3. **myst-nb** (Highly Recommended)
```python
# Add to extensions
"myst_nb"

# Configuration
nb_execution_mode = "cache"
nb_execution_timeout = 60
nb_execution_raise_on_error = True
```
**Why**: Execute Jupyter notebooks as documentation. Perfect for interactive agent examples.

### 4. **sphinx-codeautolink** (Recommended)
```python
# Add to extensions
"sphinx_codeautolink"

# Configuration
codeautolink_global_preface = """
from haive.core import *
from haive.agents import *
from haive.tools import *
"""
```
**Why**: Automatically links code references to API documentation. Great for examples.

## Category-Based Analysis

### 📊 API Documentation Enhancements

#### **sphinx-autosummary-accessors**
- **Use Case**: Document property accessors and descriptors
- **Value**: Medium - useful if you have many properties
- **Config**: Minimal setup required

#### **sphinxcontrib-apidoc**
- **Use Case**: Automatically run sphinx-apidoc
- **Value**: Low - autoapi already handles this better
- **Skip**: Already covered by autoapi

### 🎨 Formatting and Display

#### **sphinx-tabs** (Recommended)
```python
# Add to extensions
"sphinx_tabs.tabs"

# Usage in docs
"""
.. tabs::

   .. tab:: Python

      .. code-block:: python

         agent = SimpleAgent(name="assistant")

   .. tab:: YAML

      .. code-block:: yaml

         agent:
           name: assistant
"""
```
**Why**: Show code examples in multiple languages/formats

#### **sphinx-inline-tabs**
- **Use Case**: Inline tab navigation
- **Value**: Medium - good for compact comparisons
- **Alternative**: sphinx-tabs is more versatile

#### **sphinx-prompt**
```python
# Add to extensions
"sphinx_prompt"

# Usage
"""
.. prompt:: bash $

   pip install haive
   haive --version
"""
```
**Why**: Beautiful command-line examples with prompts

### 🔍 Search and Discovery

#### **readthedocs-sphinx-search** (Highly Recommended)
```python
# Add to extensions
"readthedocs_sphinx_search"

# No configuration needed for basic use
```
**Why**: Enhanced search functionality for ReadTheDocs

#### **sphinx-docsearch**
- **Use Case**: Algolia DocSearch integration
- **Value**: High if using Algolia
- **Note**: Requires Algolia account

### 📈 Quality and Testing

#### **sphinx-lint**
```python
# Run separately
poetry run sphinx-lint docs/source/
```
**Why**: Catch documentation errors before building

#### **pytest-sphinx**
- **Use Case**: Test documentation examples
- **Value**: High for ensuring examples work
- **Integration**: Works with your existing pytest setup

### 🌐 SEO and Sharing

#### **sphinx-sitemap** (Recommended)
```python
# Add to extensions
"sphinx_sitemap"

# Configuration
html_baseurl = "https://haive.readthedocs.io"
sitemap_url_scheme = "{link}"
```
**Why**: Generates sitemap.xml for better SEO

#### **sphinxext-opengraph**
```python
# Add to extensions
"sphinxext.opengraph"

# Configuration
ogp_site_url = "https://haive.readthedocs.io"
ogp_site_name = "Haive Documentation"
ogp_image = "https://haive.readthedocs.io/_static/haive-logo.png"
```
**Why**: Rich previews when sharing documentation links

### 📚 Advanced Features

#### **sphinx-needs**
- **Use Case**: Requirements tracking
- **Value**: High for complex projects
- **Complexity**: Requires significant setup

#### **jupyter-cache**
```python
# Already installed, works with myst-nb
jupyter_cache = "docs/_jupyter_cache"
```
**Why**: Cache notebook execution results

## Configuration Examples

### Enhanced MyST Configuration
```python
# Extend your current myst settings
myst_enable_extensions = [
    "deflist",
    "tasklist",
    "dollarmath",
    "amsmath",
    "colon_fence",      # ::: fences
    "substitution",     # Variable substitution
    "linkify",          # Auto-link URLs
    "html_image",       # HTML images
]

myst_substitutions = {
    "version": version,
    "project": project,
}
```

### Complete Type Documentation Setup
```python
# For comprehensive type documentation
extensions.extend([
    "sphinx_autodoc_typehints",
    "sphinxcontrib.autodoc_pydantic",
])

# Type hints configuration
autodoc_typehints = "description"
autodoc_type_aliases = {
    "StateType": "haive.core.schema.StateSchema",
    "AgentType": "haive.agents.base.Agent",
}

# Pydantic configuration
autodoc_pydantic_model_show_json = True
autodoc_pydantic_model_show_config_summary = True
autodoc_pydantic_field_list_validators = True
```

### Interactive Examples Setup
```python
# For executable documentation
extensions.extend([
    "myst_nb",
    "sphinx_thebe",  # Optional: live code execution
])

# Notebook execution
nb_execution_mode = "cache"
nb_execution_excludepatterns = ["**/debug_*.ipynb"]
nb_jupyter_kernels = {
    "python3": {
        "display_name": "Python 3 (Haive)",
        "language": "python",
        "env": {"HAIVE_DOCS_MODE": "true"},
    }
}
```

## Dependencies to Avoid

### ❌ Conflicting Dependencies
1. **sphinx-autodoc2** - Conflicts with autoapi
2. **sphinxcontrib-autoprogram** - Overlaps with your custom CLI docs
3. **sphinx-multiversion** - Complex setup, use versioning on ReadTheDocs instead

### ⚠️ High-Complexity Dependencies
1. **sphinx-needs** - Powerful but requires significant investment
2. **sphinx-plotly-directive** - Only if you need Plotly charts
3. **sphinxcontrib-plantuml** - Requires Java, use Mermaid instead

## Missing Dependencies Worth Adding

### 1. **sphinx-remove-toctrees**
```bash
poetry add --group docs sphinx-remove-toctrees
```
**Why**: Hide autogenerated toctrees from navigation while keeping pages accessible

### 2. **sphinx-favicon**
```bash
poetry add --group docs sphinx-favicon
```
```python
favicons = [
    {"href": "favicon-32x32.png"},
    {"href": "favicon-16x16.png"},
]
```
**Why**: Professional favicon support

### 3. **enum-tools[sphinx]**
```bash
poetry add --group docs "enum-tools[sphinx]"
```
**Why**: Better documentation for your many Enum types

## 🎯 Recommended Minimal Addition

Add these to your `conf.py` for immediate value:

```python
extensions.extend([
    # Type documentation
    "sphinx_autodoc_typehints",
    "sphinxcontrib.autodoc_pydantic",
    
    # Enhanced display
    "sphinx_tabs.tabs",
    "sphinx_prompt",
    
    # Search and SEO
    "readthedocs_sphinx_search",
    "sphinx_sitemap",
    "sphinxext.opengraph",
    
    # Interactive examples (if needed)
    "myst_nb",
])

# Configure autodoc typehints
autodoc_typehints = "description"
autodoc_typehints_format = "short"

# Configure sitemap
html_baseurl = "https://haive.readthedocs.io"

# Configure opengraph
ogp_site_url = "https://haive.readthedocs.io"
ogp_site_name = "Haive - AI Agent Framework"

# Enhanced MyST
myst_enable_extensions.extend([
    "colon_fence",
    "linkify",
    "substitution",
])
```

## 📊 Summary

You have **95+ documentation dependencies** installed but only use about 10. Focus on:

1. **Type documentation** (critical for AI framework)
2. **Interactive examples** (showcase agent capabilities)
3. **Search and discovery** (help users find what they need)
4. **Professional appearance** (tabs, prompts, SEO)

The recommended additions above will significantly enhance your documentation without adding complexity or conflicts.