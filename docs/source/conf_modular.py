"""Modular Sphinx configuration.

This is an alternative configuration approach that loads settings
from separate modules for better organization and maintainability.
"""

import os
import sys

# Add conf_modules to path
sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("conf_modules"))

from conf_modules.autoapi import *

# Import all configuration modules
from conf_modules.base import *
from conf_modules.enums import *
from conf_modules.extensions import get_all_extensions
from conf_modules.pydantic import *

# Set up extensions
extensions = get_all_extensions(include_optional=True)

# Additional configuration that depends on loaded modules
if "myst_parser" in extensions:
    # Configure MyST if available
    myst_enable_extensions = [
        "deflist",
        "tasklist",
        "html_image",
        "colon_fence",
        "smartquotes",
        "replacements",
        "linkify",
        "strikethrough",
    ]

# Jinja2 configuration for templates
jinja_env_options = {"extensions": ["jinja2.ext.do"]}


# Event handlers
def setup(app):
    """Setup Sphinx application with event handlers."""
    # AutoAPI skip logic
    if "autoapi.extension" in extensions:
        from conf_modules.autoapi import autoapi_skip_member

        app.connect("autoapi-skip-member", autoapi_skip_member)

    # Enum setup
    from conf_modules.enums import setup_enum_documentation

    setup_enum_documentation(app)

    # Custom CSS
    app.add_css_file("css/custom.css")

    # Log configuration summary
    app.info("=" * 70)
    app.info("PyAutoDoc Documentation Build Configuration")
    app.info("=" * 70)
    app.info(f"Extensions loaded: {len(extensions)}")
    app.info(f"Theme: {html_theme}")
    app.info(f"AutoAPI enabled: {'autoapi.extension' in extensions}")
    app.info(f"Pydantic support: {'sphinxcontrib.autodoc_pydantic' in extensions}")
    app.info(f"Enum tools: {'enum_tools.autoenum' in extensions}")
    app.info("=" * 70)
