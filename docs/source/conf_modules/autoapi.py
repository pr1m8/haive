"""AutoAPI configuration module.

This module contains configuration specific to sphinx-autoapi
for automatic API documentation generation.
"""

# AutoAPI Extension
autoapi_extension = "autoapi.extension"

# AutoAPI Configuration
autoapi_type = "python"
autoapi_dirs = ["../../../src"]
autoapi_template_dir = "_autoapi_templates"
autoapi_add_toctree_entry = True
autoapi_generate_api_docs = True
autoapi_keep_files = True
autoapi_root = "autoapi"

# AutoAPI Options
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
    "private-members",
    "special-members",
    "imported-members",
]

# Python class content
autoapi_python_class_content = "both"

# Class diagrams
autoapi_add_class_diagram = True
autoapi_class_diagram_depth = 2
autoapi_class_diagram_omit_members = False

# Member ordering
autoapi_member_order = "bysource"

# Ignore patterns
autoapi_ignore = [
    "*/migrations/*",
    "*/tests/*",
    "*/test_*.py",
    "*_test.py",
    "*/conftest.py",
]


# Custom skip logic
def autoapi_skip_member(app, what, name, obj, skip, options):
    """Custom logic to skip certain members."""
    # Skip private members starting with __pydantic
    if name.startswith("__pydantic"):
        return True

    # Skip test classes and functions
    if name.startswith("Test") or name.startswith("test_"):
        return True

    # Skip certain dunder methods
    skip_dunders = {"__weakref__", "__dict__", "__module__"}
    if name in skip_dunders:
        return True

    return None
