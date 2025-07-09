"""
Path constants for the Haive framework.

This module handles path resolution for the polyrepo structure where
packages like haive-core are in the packages/ directory.
"""

import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

# Path resolution for packages/haive-core/src/haive/core/config/constants.py
CONFIG_DIR = Path(__file__).resolve().parent
CORE_DIR = CONFIG_DIR.parent  # haive/core
HAIVE_NAMESPACE_DIR = CORE_DIR.parent  # haive
SRC_DIR = HAIVE_NAMESPACE_DIR.parent  # src
HAIVE_CORE_PACKAGE_DIR = SRC_DIR.parent  # haive-core
PACKAGES_DIR = HAIVE_CORE_PACKAGE_DIR.parent  # packages
ROOT_DIR = PACKAGES_DIR.parent  # haive root (polyrepo root)

# Check if paths look correct and log warnings if not
if CORE_DIR.name != "core":
    logger.warning(f"Unexpected CORE_DIR name: {CORE_DIR.name}, expected 'core'")
if HAIVE_NAMESPACE_DIR.name != "haive":
    logger.warning(
        f"Unexpected HAIVE_NAMESPACE_DIR name: {HAIVE_NAMESPACE_DIR.name}, expected 'haive'"
    )
if SRC_DIR.name != "src":
    logger.warning(f"Unexpected SRC_DIR name: {SRC_DIR.name}, expected 'src'")
if "haive-core" not in str(HAIVE_CORE_PACKAGE_DIR):
    logger.warning(
        f"HAIVE_CORE_PACKAGE_DIR does not contain 'haive-core': {HAIVE_CORE_PACKAGE_DIR}"
    )
if PACKAGES_DIR.name != "packages":
    logger.warning(
        f"Unexpected PACKAGES_DIR name: {PACKAGES_DIR.name}, expected 'packages'"
    )

# Get other package directories
HAIVE_AGENTS_PACKAGE_DIR = PACKAGES_DIR / "haive-agents"
HAIVE_GAMES_PACKAGE_DIR = PACKAGES_DIR / "haive-games"
HAIVE_TOOLS_PACKAGE_DIR = PACKAGES_DIR / "haive-tools"

# Package source directories
HAIVE_CORE_DIR = HAIVE_CORE_PACKAGE_DIR / "src" / "haive" / "core"
HAIVE_AGENTS_DIR = HAIVE_AGENTS_PACKAGE_DIR / "src" / "haive" / "agents"
HAIVE_GAMES_DIR = HAIVE_GAMES_PACKAGE_DIR / "src" / "haive" / "games"
HAIVE_TOOLS_DIR = HAIVE_TOOLS_PACKAGE_DIR / "src" / "haive" / "tools"

# Important shared folders
RESOURCES_DIR = ROOT_DIR / "resources"
CACHE_DIR = ROOT_DIR / "lc_cache"
GRAPH_IMAGES_DIR = RESOURCES_DIR / "graph_images"
EMBEDDINGS_CACHE_DIR = RESOURCES_DIR / "embeddings_cache"

# Optional project-specific folders
PROJECTS_DIR = ROOT_DIR / "projects"
DOCUMENTS_DIR = ROOT_DIR / "documents"
VECTORSTORE_DIR = ROOT_DIR / "vectorstore"
AGENTS_DIR = HAIVE_AGENTS_DIR

# Create necessary dirs if not already present
DIRS_TO_CREATE = [
    RESOURCES_DIR,
    CACHE_DIR,
    GRAPH_IMAGES_DIR,
    EMBEDDINGS_CACHE_DIR,
    PROJECTS_DIR,
    DOCUMENTS_DIR,
    VECTORSTORE_DIR,
]


def create_directories():
    """Create the necessary directories if they don't exist."""
    for path in DIRS_TO_CREATE:
        try:
            path.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Ensured directory exists: {path}")
        except Exception as e:
            logger.warning(f"Could not create directory {path}: {e}")


# Create directories on module import
create_directories()

# Expose constants
__all__ = [
    "ROOT_DIR",
    "PACKAGES_DIR",
    "HAIVE_CORE_PACKAGE_DIR",
    "HAIVE_AGENTS_PACKAGE_DIR",
    "HAIVE_GAMES_PACKAGE_DIR",
    "HAIVE_TOOLS_PACKAGE_DIR",
    "HAIVE_CORE_DIR",
    "HAIVE_AGENTS_DIR",
    "HAIVE_GAMES_DIR",
    "HAIVE_TOOLS_DIR",
    "RESOURCES_DIR",
    "CACHE_DIR",
    "GRAPH_IMAGES_DIR",
    "EMBEDDINGS_CACHE_DIR",
    "PROJECTS_DIR",
    "DOCUMENTS_DIR",
    "VECTORSTORE_DIR",
    "AGENTS_DIR",
]

# Debug output
if os.environ.get("HAIVE_DEBUG_PATHS"):
    for name, path in {k: globals()[k] for k in __all__}.items():
        logger.info(f"{name}: {path}")
        print(f"{name}: {path}")
