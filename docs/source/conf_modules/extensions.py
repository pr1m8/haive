"""Additional Sphinx extensions configuration.

This module manages optional Sphinx extensions and their configurations.
"""

# Optional extensions with fallback handling
optional_extensions = []

# Markdown support
try:
    import myst_parser

    optional_extensions.append("myst_parser")
    myst_extensions = [
        "deflist",
        "tasklist",
        "html_image",
        "colon_fence",
        "smartquotes",
        "replacements",
        "linkify",
        "strikethrough",
    ]
    myst_enable_extensions = myst_extensions
    myst_heading_anchors = 3
except ImportError:
    print("Warning: myst_parser not installed")

# Toggle buttons
try:
    import sphinx_togglebutton

    optional_extensions.append("sphinx_togglebutton")
    togglebutton_hint = "Click to show"
    togglebutton_hint_hide = "Click to hide"
except ImportError:
    print("Warning: sphinx_togglebutton not installed")

# Copy button for code blocks
try:
    import sphinx_copybutton

    optional_extensions.append("sphinx_copybutton")
    copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
    copybutton_prompt_is_regexp = True
except ImportError:
    print("Warning: sphinx_copybutton not installed")

# Sitemap generation
try:
    import sphinx_sitemap

    optional_extensions.append("sphinx_sitemap")
    sitemap_url_scheme = "{link}"
except ImportError:
    print("Warning: sphinx_sitemap not installed")

# Type hints
try:
    import sphinx_autodoc_typehints

    optional_extensions.append("sphinx_autodoc_typehints")
    always_document_param_types = True
    typehints_defaults = "comma"
except ImportError:
    print("Warning: sphinx_autodoc_typehints not installed")

# PlantUML diagrams
try:
    import sphinxcontrib.plantuml

    optional_extensions.append("sphinxcontrib.plantuml")
    plantuml = "plantuml"
    plantuml_output_format = "svg"
except ImportError:
    print("Warning: sphinxcontrib-plantuml not installed")

# Mermaid diagrams
try:
    import sphinxcontrib.mermaid

    optional_extensions.append("sphinxcontrib.mermaid")
    mermaid_params = ["--theme", "neutral"]
except ImportError:
    print("Warning: sphinxcontrib-mermaid not installed")

# Design elements
try:
    import sphinx_design

    optional_extensions.append("sphinx_design")
except ImportError:
    print("Warning: sphinx_design not installed")

# Tabs
try:
    import sphinx_tabs

    optional_extensions.append("sphinx_tabs.tabs")
    sphinx_tabs_disable_tab_closing = True
except ImportError:
    print("Warning: sphinx_tabs not installed")

# Inline tabs
try:
    import sphinx_inline_tabs

    optional_extensions.append("sphinx_inline_tabs")
except ImportError:
    print("Warning: sphinx_inline_tabs not installed")


def get_all_extensions(include_optional=True):
    """Get list of all extensions to load."""
    from .autoapi import autoapi_extension
    from .base import base_extensions
    from .enums import enum_extension
    from .pydantic import pydantic_extension

    extensions = base_extensions.copy()

    # Add required extensions
    extensions.append(autoapi_extension)
    extensions.append(pydantic_extension)

    # Add enum extension if available
    if enum_extension:
        extensions.append(enum_extension)

    # Add optional extensions
    if include_optional:
        extensions.extend(optional_extensions)

    # Remove duplicates while preserving order
    seen = set()
    unique_extensions = []
    for ext in extensions:
        if ext not in seen:
            seen.add(ext)
            unique_extensions.append(ext)

    return unique_extensions
