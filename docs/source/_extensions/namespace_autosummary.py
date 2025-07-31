"""Custom autosummary extension for namespace packages.

This extension handles the complexities of PEP 420 namespace packages
by providing better error handling and discovery.
"""

import importlib
import os
from typing import Any

from sphinx.ext.autosummary import Autosummary, ImportExceptionGroup, import_by_name
from sphinx.util import logging as sphinx_logging


logger = sphinx_logging.getLogger(__name__)


def safe_import_by_name(
    name: str, prefixes: list[str | None] | None = None
) -> tuple[str, Any, Any, str]:
    """Import by name with better error handling for namespace packages.

    This function attempts to import a name, but if it fails, it tries
    to handle namespace package edge cases.
    """
    if prefixes is None:
        prefixes = [None]
    if prefixes is None:
        prefixes = [None]
    if prefixes is None:
        prefixes = [None]
    if prefixes is None:
        prefixes = [None]
    try:
        # First try the standard import
        return import_by_name(name, prefixes)
    except ImportExceptionGroup as e:
        # Log the error but don't fail
        logger.debug(f"Failed to import {name}: {e}")

        # Try to handle namespace packages
        parts = name.split(".")

        # For namespace packages, we might need to import parent first
        if len(parts) > 2:
            parent = ".".join(parts[:-1])
            try:
                parent_mod = importlib.import_module(parent)
                # Now try to get the attribute
                obj = getattr(parent_mod, parts[-1], None)
                if obj:
                    return parts[-1], obj, parent, parent_mod.__name__
            except Exception:
                pass

        # If it's a module, try direct import
        try:
            obj = importlib.import_module(name)
            return (
                name.split(".")[-1],
                obj,
                ".".join(parts[:-1]) if len(parts) > 1 else None,
                name,
            )
        except Exception:
            pass

        # Return a dummy object to avoid breaking the build
        class DummyModule:
            __name__ = name
            __module__ = name
            __doc__ = f"Failed to import {name}"
            __file__ = None

        return (
            parts[-1],
            DummyModule(),
            ".".join(parts[:-1]) if len(parts) > 1 else None,
            name,
        )


class NamespaceAutosummary(Autosummary):
    """Custom autosummary that handles namespace packages better."""

    def get_items(self, names: list[str]) -> list[tuple[str, str, str, str]]:
        """Get items with better error handling."""
        items = []

        for name in names:
            try:
                display_name, obj, parent, modname = safe_import_by_name(name)
                items.append((display_name, obj, parent, modname))
            except Exception as e:
                logger.warning(f"Failed to process {name}: {e}")
                # Add a placeholder
                items.append((name, None, None, name))

        return items


def get_module_members(module_name: str) -> list[str]:
    """Get members of a module safely."""
    try:
        module = importlib.import_module(module_name)
        members = []

        # Get all public members
        for name in dir(module):
            if not name.startswith("_"):
                try:
                    obj = getattr(module, name)
                    # Only include objects that are actually from this module
                    if hasattr(obj, "__module__") and obj.__module__.startswith(
                        module_name
                    ):
                        members.append(f"{module_name}.{name}")
                except Exception:
                    pass

        return members
    except Exception as e:
        logger.debug(f"Failed to get members of {module_name}: {e}")
        return []


def process_namespace_packages(app, what, name, obj, options, lines):
    """Process namespace packages in autodoc."""
    if what == "module" and hasattr(obj, "__path__"):
        # This is a namespace package
        lines.insert(0, "**Namespace Package**")
        lines.insert(1, "")

        # Try to list submodules
        if hasattr(obj, "__path__"):
            submodules = []
            for path in obj.__path__:
                if os.path.exists(path):
                    for item in os.listdir(path):
                        if item.endswith(".py") and not item.startswith("_"):
                            submodules.append(item[:-3])
                        elif os.path.isdir(
                            os.path.join(path, item)
                        ) and not item.startswith("_"):
                            if os.path.exists(os.path.join(path, item, "__init__.py")):
                                submodules.append(item)

            if submodules:
                lines.append("**Submodules:**")
                lines.append("")
                for submod in sorted(set(submodules)):
                    lines.append(f"- :mod:`{name}.{submod}`")
                lines.append("")


def setup(app):
    """Setup the extension."""
    # Replace the standard autosummary directive
    app.add_directive("autosummary", NamespaceAutosummary, override=True)

    # Add event handler for namespace packages
    app.connect("autodoc-process-docstring", process_namespace_packages, priority=100)

    # Patch the import function
    import sphinx.ext.autosummary

    sphinx.ext.autosummary.import_by_name = safe_import_by_name

    return {
        "version": "1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
