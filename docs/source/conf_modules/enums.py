"""Enum documentation configuration module.

This module contains configuration for documenting Python enums
using enum-tools extension.
"""

# Check if enum-tools is available
try:
    import enum_tools

    enum_extension = "enum_tools.autoenum"
    enum_tools_available = True
except ImportError:
    enum_extension = None
    enum_tools_available = False
    print("Warning: enum-tools not installed")

# Enum documentation options
if enum_tools_available:
    # AutoEnum configuration
    autoenum_default_options = [
        "members",
        "undoc-members",
        "show-inheritance",
    ]

    # Custom enum member formatting
    autoenum_member_format = "{name} = {value!r}"

    # Show enum class docstring
    autoenum_include_class_doc = True

    # Include init method if customized
    autoenum_include_init = True

# Fallback configuration without enum-tools
enum_fallback_config = {
    "show_enum_values": True,
    "show_enum_class": True,
    "enum_class_signature_prefix": "enum",
}


def setup_enum_documentation(app):
    """Setup enum documentation based on available extensions."""
    if enum_tools_available:
        # Use enum-tools specific configuration
        app.config.autoenum_default_options = autoenum_default_options
        app.config.autoenum_member_format = autoenum_member_format
    else:
        # Use standard autodoc for enums
        print("Using standard autodoc for enum documentation")
