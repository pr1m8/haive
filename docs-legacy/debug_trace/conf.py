#!/usr/bin/env python3
"""
DEBUG CONF.PY - Add breakpoints and tracing everywhere
Find exactly where the conflicting extensions are coming from
"""

print("🐛 DEBUG: Starting conf.py execution")

import logging
import os
import sys
from pathlib import Path

print("🐛 DEBUG: Basic imports complete")

# Add tracing to extension loading
original_extension_list = []


def trace_extension_changes():
    global original_extension_list
    if "extensions" in globals():
        current = globals()["extensions"][:]
        if current != original_extension_list:
            print(f"🚨 EXTENSION LIST CHANGED!")
            print(f"   Before: {original_extension_list}")
            print(f"   After:  {current}")
            print(f"   Added:  {set(current) - set(original_extension_list)}")
            print(f"   Removed: {set(original_extension_list) - set(current)}")
            import traceback

            print("   Call stack:")
            traceback.print_stack()
            original_extension_list = current[:]


# Path setup
project_root = Path(__file__).parent.parent.parent
packages_dir = project_root / "packages"
sys.path.insert(0, str(packages_dir / "haive-core/src"))
print(f"🐛 DEBUG: Added path: {packages_dir / 'haive-core/src'}")

# Basic project info
project = "Debug Haive"
copyright = "2024, Debug"
author = "Debug"

print("🐛 DEBUG: Project info set")

# MINIMAL extensions
extensions = ["autoapi.extension"]
original_extension_list = extensions[:]
print(f"🐛 DEBUG: Initial extensions = {extensions}")

# Trace any changes
trace_extension_changes()

# AutoAPI minimal config
autoapi_dirs = [str(packages_dir / "haive-core/src")]
autoapi_type = "python"
autoapi_root = "api"
autoapi_generate_api_docs = True
autoapi_add_toctree_entry = True
autoapi_python_use_implicit_namespaces = True
autoapi_options = ["members", "undoc-members"]

print(
    f"🐛 DEBUG: AutoAPI configured with {len(list(Path(autoapi_dirs[0]).rglob('*.py')))} Python files"
)

# NO MOCKS, NO IGNORES
autodoc_mock_imports = []
autoapi_ignore = []

print("🐛 DEBUG: No mocks, no ignores")

# Simple theme
html_theme = "alabaster"

print("🐛 DEBUG: Theme set")

# Check extensions again
trace_extension_changes()

# Minimal templates
templates_path = ["_templates"]

# Check extensions again
trace_extension_changes()

print("🐛 DEBUG: Basic configuration complete")

# Skip import tracing for now - focus on direct extension loading
print("🐛 DEBUG: Skipping import tracing to avoid builtins issues")

# Check extensions one more time
trace_extension_changes()

print("🐛 DEBUG: conf.py execution complete")
print(f"🐛 DEBUG: Final extensions = {extensions}")


# Setup function with tracing
def setup(app):
    print(f"🐛 DEBUG SETUP: Called with app = {type(app)}")
    print(
        f"🐛 DEBUG SETUP: app.extensions = {list(app.extensions.keys()) if hasattr(app, 'extensions') else 'No extensions attr'}"
    )

    # Trace when extensions get added
    if hasattr(app, "extensions"):
        original_setup_extension = app.setup_extension

        def traced_setup_extension(name):
            print(f"🚨 SETUP_EXTENSION CALLED: {name}")
            import traceback

            traceback.print_stack(limit=5)
            return original_setup_extension(name)

        app.setup_extension = traced_setup_extension
        print("🐛 DEBUG SETUP: Applied setup_extension tracing")

    print("🐛 DEBUG SETUP: Complete")


print("🐛 DEBUG: Setup function defined")
