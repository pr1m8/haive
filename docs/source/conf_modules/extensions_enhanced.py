"""Enhanced extensions configuration with structured error handling."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

# Try to import structured logging
try:
    pass

    logger = logging.getLogger("sphinx_config.extensions")
except ImportError:
    # Fallback to basic logging
    logger = logging.getLogger("sphinx_config.extensions")

# Extension categories for better organization
EXTENSION_CATEGORIES = {
    "core": {
        "extensions": [
            "sphinx.ext.autodoc",
            "sphinx.ext.autosummary",
            "sphinx.ext.napoleon",
            "sphinx.ext.viewcode",
            "sphinx.ext.intersphinx",
            "sphinx.ext.todo",
            "sphinx.ext.coverage",
            "sphinx.ext.mathjax",
            "sphinx.ext.ifconfig",
            "sphinx.ext.githubpages",
            "sphinx.ext.duration",
            "sphinx.ext.graphviz",
            "sphinx.ext.inheritance_diagram",
            "sphinx.ext.autosectionlabel",
        ],
        "description":
        "Core Sphinx extensions",
        "required":
        True,
    },
    "api": {
        "extensions": [
            "autoapi.extension",
            "sphinx_autodoc_typehints",
        ],
        "description": "API documentation generation",
        "required": True,
    },
    "content": {
        "extensions": [
            "myst_parser",
            "sphinx_copybutton",
            "sphinx_togglebutton",
            "sphinx_inline_tabs",
        ],
        "description":
        "Content enhancement extensions",
        "required":
        True,
    },
    "quality": {
        "extensions": [
            "sphinxcontrib.spelling",
            "sphinx.ext.doctest",
            "sphinx.ext.linkcheck",
        ],
        "description":
        "Documentation quality tools",
        "required":
        False,
    },
    "diagrams": {
        "extensions": [
            "sphinxcontrib.mermaid",
            "sphinx_design",
            "sphinxcontrib.plantuml",
        ],
        "description":
        "Diagram and design elements",
        "required":
        False,
    },
    "export": {
        "extensions": [
            "sphinx.ext.doctest",
            "nbsphinx",
            "sphinx_gallery.gen_gallery",
        ],
        "description":
        "Export and gallery features",
        "required":
        False,
    },
    "custom": {
        "extensions": [
            "_extensions.haive_sphinx_ext",
            "_extensions.agent_docs",
            "_extensions.auto_module_discovery",
            "_extensions.games_autodoc",
            "_extensions.namespace_autosummary",
        ],
        "description":
        "Custom Haive extensions",
        "required":
        True,
    },
}


def get_extension_with_structured_logging(
) -> tuple[list[str], dict[str, Any]]:
    """Load extensions with structured logging and status tracking."""

    extensions = []
    extension_status = {
        "loaded": [],
        "failed": [],
        "optional_missing": [],
        "categories": {},
    }

    logger.info("\n" + "=" * 80)
    logger.info("🔌 LOADING SPHINX EXTENSIONS")
    logger.info("=" * 80)

    for category, category_info in EXTENSION_CATEGORIES.items():
        logger.info(
            f"\n📦 Loading {category} extensions ({category_info['description']}):"
        )

        category_loaded = 0
        category_failed = 0
        category_optional_missing = 0

        for ext_name in category_info["extensions"]:
            try:
                # Try to import the extension
                if ext_name.startswith("_extensions"):
                    # Local extension
                    __import__(ext_name)
                elif ext_name == "sphinx_gallery.gen_gallery":
                    # Special handling for sphinx_gallery
                    pass
                elif ext_name == "nbsphinx":
                    # Special handling for nbsphinx
                    pass
                elif "sphinxcontrib" in ext_name:
                    # sphinxcontrib extensions
                    # Try both patterns: sphinxcontrib.foo and sphinxcontrib_foo
                    try:
                        __import__(ext_name)
                    except ImportError:
                        # Try with underscore
                        module_name = ext_name.replace("sphinxcontrib.",
                                                       "sphinxcontrib_")
                        __import__(module_name)

                extensions.append(ext_name)
                logger.info(f"  ✅ {ext_name}")
                extension_status["loaded"].append(
                    {
                        "name": ext_name,
                        "category": category,
                    }, )
                category_loaded += 1

            except ImportError as e:
                error_msg = str(e)

                if category_info["required"]:
                    # Required extension failed
                    logger.error(
                        f"  ❌ {ext_name}: Required extension failed - {error_msg}",
                        extra={
                            "category": "extension_error",
                            "extension": ext_name
                        },
                    )
                    extension_status["failed"].append(
                        {
                            "name": ext_name,
                            "category": category,
                            "error": error_msg,
                            "required": True,
                        }, )
                    category_failed += 1
                else:
                    # Optional extension missing
                    logger.warning(
                        f"  ⚠️  {ext_name}: Optional extension not available - {error_msg}",
                        extra={
                            "category": "missing_extension",
                            "extension": ext_name},
                    )
                    extension_status["optional_missing"].append(
                        {
                            "name": ext_name,
                            "category": category,
                            "error": error_msg,
                            "required": False,
                        }, )
                    category_optional_missing += 1
                    # Still add to extensions list for Sphinx
                    extensions.append(ext_name)

            except Exception as e:
                # Other errors
                logger.error(
                    f"  💥 {ext_name}: Unexpected error - {e}",
                    extra={
                        "category": "extension_error",
                        "extension": ext_name
                    },
                )
                extension_status["failed"].append(
                    {
                        "name": ext_name,
                        "category": category,
                        "error": str(e),
                        "type": type(e).__name__,
                    }, )
                category_failed += 1

        # Category summary
        extension_status["categories"][category] = {
            "total": len(category_info["extensions"]),
            "loaded": category_loaded,
            "failed": category_failed,
            "optional_missing": category_optional_missing,
            "required": category_info["required"],
        }

        logger.info(
            f"  📊 {category} summary: "
            f"{category_loaded} loaded, "
            f"{category_failed} failed, "
            f"{category_optional_missing} optional missing", )

    # Overall summary
    logger.info("\n" + "=" * 80)
    logger.info("📊 EXTENSION LOADING SUMMARY")
    logger.info("=" * 80)
    logger.info(f"  ✅ Successfully loaded: {len(extension_status['loaded'])}")
    logger.info(
        f"  ⚠️  Optional missing: {len(extension_status['optional_missing'])}")
    logger.info(f"  ❌ Failed to load: {len(extension_status['failed'])}")

    # List failed required extensions
    if extension_status["failed"]:
        logger.error("\n⚠️  Failed required extensions:")
        for ext in extension_status["failed"]:
            if ext.get("required", True):
                logger.error(
                    f"  - {ext['name']} ({ext['category']}): {ext['error']}")

    # Save extension status
    status_file = Path(
        __file__).parent.parent / "logs" / "build" / "extension_status.json"
    status_file.parent.mkdir(exist_ok=True, parents=True)
    with open(status_file, "w") as f:
        json.dump(extension_status, f, indent=2)

    logger.info(f"\n📄 Extension status saved to: {status_file}")
    logger.info("=" * 80 + "\n")

    return extensions, extension_status


# For backward compatibility


def get_all_extensions():
    """Get all available extensions (backward compatible)."""
    extensions, _ = get_extension_with_structured_logging()
    return extensions
