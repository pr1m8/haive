"""Modular Sphinx configuration for Haive - Example using the new system.

This demonstrates how to use the modular configuration system to create
different types of documentation builds.
"""

import sys
import warnings
from datetime import datetime
from pathlib import Path

# Add the current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Suppress warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", message=".*Matplotlib.*")
warnings.filterwarnings("ignore", category=UserWarning, module="sphinx")

# ==============================================================================
# MODULAR CONFIGURATION - Choose your configuration style
# ==============================================================================

# Option 1: Full configuration (like current conf.py)
from conf_modules import create_full_config

config = create_full_config()

# Option 2: Standard configuration (recommended for most projects)
# from conf_modules import create_standard_config
# config = create_standard_config()

# Option 3: Minimal configuration (for simple projects)
# from conf_modules import create_minimal_config
# config = create_minimal_config()

# Option 4: Custom configuration (mix and match features)
# from conf_modules import create_custom_config
# config = create_custom_config(
#     project_name="Haive",
#     author="William R. Astley",
#     enable_api_docs=True,
#     enable_notebooks=True,
#     enable_diagrams=True,
#     enable_pdf=False,
#     enable_presentations=False,
#     github_repo="pr1m8/haive",
#     base_url="https://haive.readthedocs.io/",
# )

# Apply the configuration to current scope
locals().update(config)

# ==============================================================================
# CUSTOM OVERRIDES (if needed)
# ==============================================================================

# You can still override specific settings if needed
# For example:
# html_title = "🤖 Custom Title"
# extensions.append("my_custom_extension")

# ==============================================================================
# ADVANCED CUSTOMIZATION EXAMPLES
# ==============================================================================

# Example: Add custom CSS/JS based on environment
import os

if os.getenv("DOCS_THEME") == "dark":
    html_css_files.append("dark-theme.css")

# Example: Conditional extensions based on available packages
try:
    import plotly

    extensions.append("sphinx_plotly_directive")
except ImportError:
    pass

# Example: Environment-specific settings
if os.getenv("SPHINX_BUILD_TYPE") == "production":
    # Production settings
    nitpicky = True
    html_show_sourcelink = False
elif os.getenv("SPHINX_BUILD_TYPE") == "development":
    # Development settings
    nitpicky = False
    html_show_sourcelink = True
    # Add more verbose logging
    import logging

    logging.getLogger("sphinx").setLevel(logging.DEBUG)

# ==============================================================================
# CUSTOM FUNCTIONS AND HOOKS (from original conf.py if needed)
# ==============================================================================


# You can still add custom functions like linkcode_resolve, setup functions, etc.
def linkcode_resolve(domain, info):
    """Resolve function to link to GitHub source code."""
    if domain != "py":
        return None
    if not info["module"]:
        return None

    module_parts = info["module"].split(".")
    if len(module_parts) < 2 or module_parts[0] != "haive":
        return None

    package_name = module_parts[1]
    package_dir = f"haive-{package_name}"

    submodule_path = "/".join(module_parts[2:]) if len(module_parts) > 2 else ""
    if submodule_path:
        filename = (
            f"packages/{package_dir}/src/haive/{package_name}/{submodule_path}.py"
        )
    else:
        filename = f"packages/{package_dir}/src/haive/{package_name}/__init__.py"

    return f"https://github.com/will-astley/haive/blob/main/{filename}"


def setup(app):
    """Setup function for custom modifications."""
    # Get logger from the config
    logger = config.get("_logger")
    if logger:
        logger.info("Running modular Sphinx setup function")

    # Ensure directories exist
    static_dir = Path(__file__).parent / "_static"
    static_dir.mkdir(exist_ok=True)

    images_dir = static_dir / "images"
    images_dir.mkdir(exist_ok=True)

    # Add custom CSS for enhanced styling
    app.add_css_file("haive-enhanced.css")

    return {
        "version": "1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }


# ==============================================================================
# CONFIGURATION SUMMARY
# ==============================================================================

# Print configuration summary if logger is available
logger = config.get("_logger")
if logger:
    logger.info(f"Project: {project}")
    logger.info(f"Extensions loaded: {len(extensions)}")
    logger.info(f"Theme: {html_theme}")
    logger.info("Modular configuration loaded successfully")

    # Show which categories of extensions are enabled
    from conf_modules import get_all_available_extensions

    all_exts = get_all_available_extensions()
    for category, exts in all_exts.items():
        enabled = [ext for ext in exts if ext in extensions]
        if enabled:
            logger.info(f"{category}: {len(enabled)}/{len(exts)} extensions enabled")
