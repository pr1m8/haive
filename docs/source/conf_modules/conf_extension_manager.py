# Configuration file using the Extension Manager
#
# This is an alternative configuration approach that uses the modular
# extension management system for cleaner, more maintainable configuration.

import os
import sys

from sphinx.application import Sphinx

from .extension_definitions import ALL_EXTENSION_GROUPS, EXTENSION_SETS

# Import our extension management system
from .extension_manager import ExtensionManager

# -- Path setup ----------------------------------------------------------------
sys.path.insert(0, os.path.abspath("../../../src"))

# -- Project metadata ----------------------------------------------------------
project = "pyautodoc"
author = "William R. Astley"
copyright = "2025, William R. Astley"
release = "0.1.0"

# -- Extension Management ------------------------------------------------------

# Initialize the extension manager
manager = ExtensionManager()

# Register all extension groups
for group_name, extensions in ALL_EXTENSION_GROUPS.items():
    manager.bulk_register(extensions)

# Load extensions based on current needs
# Options: "minimal", "standard", "full", "development", "execution", "versioning", "everything"
EXTENSION_SET = os.environ.get("SPHINX_EXTENSION_SET", "standard")

if EXTENSION_SET in EXTENSION_SETS:
    # Load by predefined set
    categories = EXTENSION_SETS[EXTENSION_SET]
    extensions, config_vars = manager.load_extensions(categories=categories)
else:
    # Load by specific categories or extensions
    extensions, config_vars = manager.load_extensions(
        categories=["core", "api", "content"]
    )

# Get status report for debugging
status_report = manager.get_status_report()
print(
    f"Extension Manager Status: {status_report['loaded']}/{status_report['total_registered']} loaded"
)
print(f"Failed extensions: {list(status_report['failed_extensions'].keys())}")

# -- Apply collected configuration variables ----------------------------------
globals().update(config_vars)

# -- General configuration -----------------------------------------------------
templates_path = ["_templates", "_autoapi_templates"]
html_static_path = ["_static"]
exclude_patterns = []

add_module_names = False
toc_object_entries_show_parents = "hide"

# -- Jinja2 options ------------------------------------------------------------
jinja_env_options = {"extensions": ["jinja2.ext.do"]}

# -- AutoAPI configuration (if loaded) ----------------------------------------
if "autoapi.extension" in extensions:
    autoapi_type = "python"
    autoapi_dirs = ["../../../src"]
    autoapi_template_dir = "_autoapi_templates"
    autoapi_add_toctree_entry = True
    autoapi_generate_api_docs = True
    autoapi_keep_files = True
    autoapi_options = [
        "members",
        "undoc-members",
        "show-inheritance",
        "show-module-summary",
        "private-members",
        "special-members",
        "imported-members",
    ]
    autoapi_python_class_content = "both"
    autoapi_add_class_diagram = True
    autoapi_class_diagram_depth = 2
    autoapi_class_diagram_omit_members = False

# -- HTML theme ----------------------------------------------------------------
html_theme = "furo"
html_baseurl = "https://pyautodoc.readthedocs.io/"

html_theme_options = {
    "sidebar_hide_name": False,
    "source_repository": "https://github.com/yourusername/pyautodoc/",
    "source_branch": "main",
    "source_directory": "docs/",
    "announcement": "🚀 PyAutoDoc 0.1.0 with modular extension system!",
}


# -- Event Hooks ---------------------------------------------------------------
def autoapi_skip_member(app, what, name, obj, skip, options):
    if name.startswith("__pydantic"):
        return True
    return None


def setup(app: Sphinx):
    app.connect("autoapi-skip-member", autoapi_skip_member)

    # Log extension loading status
    print("\n" + "=" * 60)
    print("EXTENSION MANAGER REPORT")
    print("=" * 60)
    for category, count in status_report["categories"].items():
        loaded_in_category = [
            ext
            for ext in status_report["loaded_extensions"]
            if ext in [spec.name for spec in ALL_EXTENSION_GROUPS.get(category, [])]
        ]
        print(f"{category.upper()}: {len(loaded_in_category)}/{count} loaded")

    if status_report["failed_extensions"]:
        print("\nFAILED EXTENSIONS:")
        for name, reason in status_report["failed_extensions"].items():
            print(f"  - {name}: {reason}")
    print("=" * 60)
