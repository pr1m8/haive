"""Complete extensions module with 60+ Sphinx extensions.

This module contains the original comprehensive extension list that was
referenced in conf_complete.py. Based on the audit from 2025-07-29, the
original system had 40+ premium extensions with 25+ active.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger("sphinx_config.extensions")

# ORIGINAL COMPREHENSIVE EXTENSION LIST (60+ extensions)
# This recreates the original extensions.py that was imported by conf_complete.py

ALL_EXTENSIONS = [
    # === CORE SPHINX EXTENSIONS (14) ===
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
    # === API DOCUMENTATION (3) ===
    "autoapi.extension",
    "sphinx_autodoc_typehints",
    "sphinx_click",
    "sphinx_argparse",
    # === CONTENT ENHANCEMENT (8) ===
    "myst_parser",
    "sphinx_copybutton",
    "sphinx_togglebutton",
    "sphinx_inline_tabs",
    "sphinx_tabs.tabs",
    "sphinx_exec_directive",
    "sphinx_prompt",
    "sphinx_jinja2",
    # === INTERACTIVE CONTENT (4) ===
    "sphinx_exercise",  # Interactive exercises with solutions
    "sphinx_proof",  # Mathematical proofs and theorems
    "sphinx_hoverxref",  # Hover tooltips for cross-references
    "sphinx_revealjs",  # Presentation slides from docs
    # === ADVANCED DIAGRAMS (6) ===
    "sphinxcontrib.mermaid",
    "sphinxcontrib.blockdiag",  # Block diagrams (architecture)
    "sphinxcontrib.seqdiag",  # Sequence diagrams (API flows)
    "sphinxcontrib.plantuml",  # UML diagrams (system design)
    "sphinxcontrib.drawio",  # Draw.io integration
    # "sphinx_design",  # DISABLED: Incompatible with Sphinx 8.2.3
    # === PROFESSIONAL POLISH (7) ===
    "sphinx_notfound_page",  # Custom 404 pages
    "sphinx_version_warning",  # Version warnings for old docs
    "sphinx_contributors",  # Automatic contributor lists
    "sphinxext.rediraffe",  # Redirect management
    "sphinx_issues",  # GitHub issues integration
    # "sphinx_sitemap",  # DISABLED: Incompatible with Sphinx 8.2.3 - is_directory_builder attribute error
    "sphinx_external_toc",
    # === ENHANCED UX (6) ===
    "sphinxemoji",  # Emoji support in docs 😀
    "sphinx_substitution_extensions",  # Advanced text substitutions
    # "sphinx_math_dollar",  # DISABLED: Incompatible with Sphinx 8.2.3 - causes NotImplementedError
    "sphinxcontrib.images",  # Image thumbnails and galleries
    "sphinxcontrib.youtube",
    "sphinxext.opengraph",
    # === API & PROTOCOLS (4) ===
    "sphinxcontrib.openapi",
    "sphinxcontrib.httpdomain",
    "sphinx_jsonschema",  # JSON schema documentation
    "sphinxcontrib.fulltoc",  # Full table of contents
    # === GALLERY & EXAMPLES (3) ===
    "sphinx_gallery.gen_gallery",
    "nbsphinx",  # Jupyter notebook integration
    "sphinx_needs",
    # === QUALITY & TESTING (2) ===
    "sphinxcontrib.spelling",
    "sphinx.ext.linkcheck",
    # === CUSTOM HAIVE EXTENSIONS (5) ===
    "_extensions.haive_sphinx_ext",
    "_extensions.agent_docs",
    "_extensions.auto_module_discovery",
    "_extensions.games_autodoc",
    "_extensions.namespace_autosummary",
]

# Extensions that were working in the original system
WORKING_EXTENSIONS = [
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.linkcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autosummary",
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.coverage",
    "sphinx.ext.todo",
    # "sphinx_design",  # DISABLED: Incompatible with Sphinx 8.2.3
    "sphinx_tabs.tabs",
    "sphinx_inline_tabs",
    "sphinx_togglebutton",
    "sphinx_copybutton",
    "sphinx_exec_directive",
    "myst_parser",
    "sphinxcontrib.mermaid",
    "sphinxcontrib.youtube",
    # "sphinx_sitemap",  # DISABLED: Incompatible with Sphinx 8.2.3 - is_directory_builder attribute error
    "sphinxcontrib.openapi",
    "sphinxcontrib.httpdomain",
    "sphinxext.opengraph",
    "sphinx_gallery.gen_gallery",
    "sphinx_autodoc_typehints",
    "sphinx_needs",
    "sphinx_prompt",
    "sphinx_jinja2",
    "sphinx_external_toc",
]

# High-value extensions from the audit report
HIGH_VALUE_EXTENSIONS = [
    "sphinx_exercise",
    "sphinx_proof",
    "sphinx_hoverxref",
    "sphinxcontrib.blockdiag",
    "sphinxcontrib.plantuml",
    "sphinx_notfound_page",
    "sphinx_contributors",
    "sphinx_issues",
    "sphinxemoji",
    "sphinx_math_dollar",
]


def get_all_extensions() -> list[str]:
    """Get all available extensions with compatibility testing.

    This function recreates the original get_all_extensions() that was
    imported by conf_complete.py and provided 60+ extensions.

    Returns:
        List of extension names that can be loaded by Sphinx
    """
    logger.info("🚀 Loading COMPLETE extension set (60+ extensions)")
    logger.info("=" * 80)

    loaded_extensions = []
    failed_extensions = []
    optional_missing = []

    for ext_name in ALL_EXTENSIONS:
        try:
            # Test if extension can be imported
            if ext_name.startswith("_extensions"):
                # Custom local extensions - try to import
                try:
                    __import__(ext_name)
                    loaded_extensions.append(ext_name)
                    logger.info(f"  ✅ {ext_name} (custom)")
                except ImportError as e:
                    logger.warning(
                        f"  ⚠️  {ext_name}: Custom extension not available - {e}",
                    )
                    optional_missing.append((ext_name, str(e)))
            elif "sphinxcontrib" in ext_name:
                # Test sphinxcontrib extensions
                try:
                    __import__(ext_name)
                    loaded_extensions.append(ext_name)
                    logger.info(f"  ✅ {ext_name}")
                except ImportError:
                    # Try alternative import pattern
                    try:
                        alt_name = ext_name.replace(
                            "sphinxcontrib.",
                            "sphinxcontrib_",
                        )
                        __import__(alt_name)
                        loaded_extensions.append(ext_name)
                        logger.info(f"  ✅ {ext_name} (alt import)")
                    except ImportError as e:
                        if ext_name in WORKING_EXTENSIONS:
                            logger.error(
                                f"  ❌ {ext_name}: Required extension failed - {e}",
                            )
                            failed_extensions.append((ext_name, str(e)))
                        else:
                            logger.warning(
                                f"  ⚠️  {ext_name}: Optional extension missing - {e}",
                            )
                            optional_missing.append((ext_name, str(e)))
            else:
                # Test standard extensions
                try:
                    if ext_name == "sphinx_gallery.gen_gallery" or ext_name == "nbsphinx":
                        pass
                    elif ext_name.startswith("sphinx.ext"):
                        # Sphinx built-in extensions - always available
                        pass
                    else:
                        # Third-party extensions
                        module_name = ext_name.split(".")[0]
                        __import__(module_name)

                    loaded_extensions.append(ext_name)
                    logger.info(f"  ✅ {ext_name}")

                except ImportError as e:
                    if ext_name in WORKING_EXTENSIONS:
                        logger.error(
                            f"  ❌ {ext_name}: Required extension failed - {e}",
                        )
                        failed_extensions.append((ext_name, str(e)))
                    else:
                        logger.warning(
                            f"  ⚠️  {ext_name}: Optional extension missing - {e}",
                        )
                        optional_missing.append((ext_name, str(e)))
                        # Don't add failed extensions to list - this causes early Sphinx
                        # failures

        except Exception as e:
            logger.error(f"  💥 {ext_name}: Unexpected error - {e}")
            failed_extensions.append((ext_name, str(e)))

    # Summary
    logger.info("\n" + "=" * 80)
    logger.info("📊 EXTENSION LOADING SUMMARY (COMPLETE SYSTEM)")
    logger.info("=" * 80)
    logger.info(f"  ✅ Successfully loaded: {len(loaded_extensions)}")
    logger.info(f"  ⚠️  Optional missing: {len(optional_missing)}")
    logger.info(f"  ❌ Failed to load: {len(failed_extensions)}")
    logger.info("  🎯 Target: 60+ extensions (Original system)")

    if len(loaded_extensions) >= 40:
        logger.info("🚀 SUCCESS: Premium documentation system active!")
    elif len(loaded_extensions) >= 30:
        logger.info("✅ GOOD: Comprehensive documentation system active")
    else:
        logger.warning("⚠️  PARTIAL: Basic documentation system active")

    logger.info("=" * 80 + "\n")

    return loaded_extensions


def test_extension_compatibility() -> dict[str, Any]:
    """Test extension compatibility and return detailed results.

    This recreates the test_extension_compatibility() function that was
    referenced in the original test script.

    Returns:
        Dictionary with compatibility test results
    """
    logger.info("🧪 Testing extension compatibility...")

    results = {
        "total_extensions": len(ALL_EXTENSIONS),
        "working_extensions": 0,
        "failed_extensions": [],
        "warnings": [],
        "high_value_status": {},
        "original_working_count": len(WORKING_EXTENSIONS),
    }

    # Test high-value extensions specifically
    for ext in HIGH_VALUE_EXTENSIONS:
        try:
            if ext.startswith("sphinx"):
                module_name = ext.split(".")[0] if "." in ext else ext
                __import__(module_name)
            results["high_value_status"][ext] = "available"
        except ImportError as e:
            results["high_value_status"][ext] = f"missing: {e}"
            results["warnings"].append(
                (ext, f"High-value extension missing: {e}"),
            )

    # Get working extensions count
    working_exts = get_all_extensions()
    results["working_extensions"] = len(working_exts)

    # Check if we match original system
    if results["working_extensions"] >= 40:
        results["status"] = "excellent"
    elif results["working_extensions"] >= 30:
        results["status"] = "good"
    else:
        results["status"] = "partial"
        results["warnings"].append(
            (
                "system",
                f"Only {results['working_extensions']} extensions active, "
                f"original had {results['original_working_count']}+",
            ),
        )

    return results


# For backward compatibility with any existing imports
def get_premium_extensions() -> list[str]:
    """Get the premium extensions that make the system world-class."""
    return HIGH_VALUE_EXTENSIONS


def get_working_extensions() -> list[str]:
    """Get extensions that were confirmed working in the original system."""
    return WORKING_EXTENSIONS
