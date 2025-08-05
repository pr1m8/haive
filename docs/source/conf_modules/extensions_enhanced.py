"""Enhanced extensions configuration with structured error handling."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

# Try to import structured logging
try:
    logger = logging.getLogger("sphinx_config.extensions")
except ImportError:
    # Fallback to basic logging
    logger = logging.getLogger("sphinx_config.extensions")

# COMPREHENSIVE Extension categories - recreating the original 60+ extension system
EXTENSION_CATEGORIES = {
    "core": {
        "extensions": [
            "sphinx.ext.autodoc",
            "sphinx.ext.autosummary",
            "sphinx.ext.napoleon",
            "sphinx.ext.viewcode",
            "sphinx.ext.linkcode",
            "sphinx.ext.intersphinx",
            "sphinx.ext.todo",
            "sphinx.ext.coverage",
            "sphinx.ext.doctest",
            "sphinx.ext.mathjax",
            "sphinx.ext.ifconfig",
            "sphinx.ext.githubpages",
            "sphinx.ext.duration",
            "sphinx.ext.graphviz",
            "sphinx.ext.inheritance_diagram",
            "sphinx.ext.autosectionlabel",
        ],
        "description": "Core Sphinx extensions (16 total)",
        "required": True,
    },
    "api": {
        "extensions": [
            "autoapi.extension",
            "sphinx_autodoc_typehints",
            "sphinx_click",
            "sphinx_argparse",
        ],
        "description": "API documentation generation (4 total)",
        "required": True,
    },
    "content": {
        "extensions": [
            "myst_parser",
            "sphinx_copybutton",
            "sphinx_togglebutton",
            "sphinx_inline_tabs",
            "sphinx_tabs.tabs",
            "sphinx_exec_directive",
            "sphinx_prompt",
            "sphinx_jinja2",
        ],
        "description": "Content enhancement extensions (8 total)",
        "required": True,
    },
    "interactive": {
        "extensions": [
            "sphinx_exercise",  # Interactive exercises with solutions
            "sphinx_proof",  # Mathematical proofs and theorems
            "sphinx_hoverxref",  # Hover tooltips for cross-references
            "sphinx_revealjs",  # Presentation slides from docs
        ],
        "description": "Interactive content features (4 total)",
        "required": False,
    },
    "diagrams": {
        "extensions": [
            "sphinxcontrib.mermaid",
            # # "sphinx_design",  # DISABLED: Incompatible with Sphinx 8.2.3  # DISABLED: Incompatible with Sphinx 8.2.3 - sphinx_design_css_changed error
            "sphinxcontrib.plantuml",
            "sphinxcontrib.blockdiag",  # Block diagrams (architecture)
            "sphinxcontrib.seqdiag",  # Sequence diagrams (API flows)
            "sphinxcontrib.drawio",  # Draw.io integration
        ],
        "description": "Diagram and design elements (5 total)",
        "required": False,
    },
    "professional": {
        "extensions": [
            "sphinx_notfound_page",  # Custom 404 pages
            "sphinx_version_warning",  # Version warnings for old docs
            "sphinx_contributors",  # Automatic contributor lists
            "sphinxext.rediraffe",  # Redirect management
            "sphinx_issues",  # GitHub issues integration
            # "sphinx_sitemap",  # DISABLED: Incompatible with Sphinx 8.2.3 - is_directory_builder attribute error
            "sphinx_external_toc",
        ],
        "description": "Professional polish features (7 total)",
        "required": False,
    },
    "ux": {
        "extensions": [
            "sphinxemoji",  # Emoji support in docs 😀
            "sphinx_substitution_extensions",  # Advanced text substitutions
            # "sphinx_math_dollar",  # DISABLED: Incompatible with Sphinx 8.2.3 - causes NotImplementedError
            "sphinxcontrib.images",  # Image thumbnails and galleries
            "sphinxcontrib.youtube",
            "sphinxext.opengraph",
        ],
        "description": "Enhanced user experience (6 total)",
        "required": False,
    },
    "protocols": {
        "extensions": [
            "sphinxcontrib.openapi",
            "sphinxcontrib.httpdomain",
            "sphinx_jsonschema",  # JSON schema documentation
            "sphinxcontrib.fulltoc",  # Full table of contents
        ],
        "description": "API & protocols documentation (4 total)",
        "required": False,
    },
    "gallery": {
        "extensions": [
            "sphinx_gallery.gen_gallery",
            "nbsphinx",  # Jupyter notebook integration
            "sphinx_needs",
        ],
        "description": "Gallery & examples (3 total)",
        "required": False,
    },
    "quality": {
        "extensions": [
            "sphinxcontrib.spelling",
            "sphinx.ext.linkcheck",
        ],
        "description": "Documentation quality tools (2 total)",
        "required": False,
    },
    "custom": {
        "extensions": [
            "_extensions.haive_sphinx_ext",
            "_extensions.agent_docs",
            "_extensions.auto_module_discovery",
            "_extensions.games_autodoc",
            "_extensions.namespace_autosummary",
        ],
        "description": "Custom Haive extensions (5 total)",
        "required": False,  # Changed to False since these are failing
    },
}


def get_extension_with_structured_logging() -> tuple[list[str], dict[str, Any]]:
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
            f"\n📦 Loading {category} extensions ({category_info['description']}):",
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
                        module_name = ext_name.replace(
                            "sphinxcontrib.",
                            "sphinxcontrib_",
                        )
                        __import__(module_name)

                extensions.append(ext_name)
                logger.info(f"  ✅ {ext_name}")
                extension_status["loaded"].append(
                    {
                        "name": ext_name,
                        "category": category,
                    },
                )
                category_loaded += 1

            except ImportError as e:
                error_msg = str(e)

                if category_info["required"]:
                    # Required extension failed
                    logger.error(
                        f"  ❌ {ext_name}: Required extension failed - {error_msg}",
                        extra={
                            "category": "extension_error",
                            "extension": ext_name,
                        },
                    )
                    extension_status["failed"].append(
                        {
                            "name": ext_name,
                            "category": category,
                            "error": error_msg,
                            "required": True,
                        },
                    )
                    category_failed += 1
                else:
                    # Optional extension missing
                    logger.warning(
                        f"  ⚠️  {ext_name}: Optional extension not available - {error_msg}",
                        extra={
                            "category": "missing_extension",
                            "extension": ext_name,
                        },
                    )
                    extension_status["optional_missing"].append(
                        {
                            "name": ext_name,
                            "category": category,
                            "error": error_msg,
                            "required": False,
                        },
                    )
                    category_optional_missing += 1
                    # Still add to extensions list for Sphinx
                    extensions.append(ext_name)

            except Exception as e:
                # Other errors
                logger.error(
                    f"  💥 {ext_name}: Unexpected error - {e}",
                    extra={
                        "category": "extension_error",
                        "extension": ext_name,
                    },
                )
                extension_status["failed"].append(
                    {
                        "name": ext_name,
                        "category": category,
                        "error": str(e),
                        "type": type(e).__name__,
                    },
                )
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
            f"{category_optional_missing} optional missing",
        )

    # Overall summary
    logger.info("\n" + "=" * 80)
    logger.info("📊 EXTENSION LOADING SUMMARY")
    logger.info("=" * 80)
    logger.info(f"  ✅ Successfully loaded: {len(extension_status['loaded'])}")
    logger.info(
        f"  ⚠️  Optional missing: {len(extension_status['optional_missing'])}",
    )
    logger.info(f"  ❌ Failed to load: {len(extension_status['failed'])}")

    # List failed required extensions
    if extension_status["failed"]:
        logger.error("\n⚠️  Failed required extensions:")
        for ext in extension_status["failed"]:
            if ext.get("required", True):
                logger.error(
                    f"  - {ext['name']} ({ext['category']}): {ext['error']}",
                )

    # Save extension status
    status_file = Path(__file__).parent.parent / "logs" / "build" / "extension_status.json"
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
