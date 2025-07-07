#!/usr/bin/env python3
"""Auto-generate manual module documentation pages.

This script creates manual automodule pages for all Haive packages to replace
the broken autosummary approach. It scans package directories and creates
properly formatted RST files with full automodule directives.
"""

import ast
import importlib.util
import logging
import os
import sys
from pathlib import Path
from typing import Dict, List, Set

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# Project structure
PROJECT_ROOT = Path(__file__).parent.parent
PACKAGES_DIR = PROJECT_ROOT / "packages"
DOCS_SOURCE_DIR = PROJECT_ROOT / "docs" / "source"
MODULES_DIR = DOCS_SOURCE_DIR / "api" / "modules"

# Package mappings
PACKAGE_MAPPINGS = {
    "haive-core": "haive.core",
    "haive-agents": "haive.agents",
    "haive-tools": "haive.tools",
    "haive-games": "haive.games",
    "haive-dataflow": "haive.dataflow",
    "haive-prebuilt": "haive.prebuilt",
    "haive-mcp": "haive.mcp",
}

# Skip certain modules/files
SKIP_PATTERNS = {
    "__pycache__",
    ".pyc",
    ".pyo",
    ".pytest_cache",
    "test_",
    "_test",
    "conftest.py",
    "setup.py",
    ".git",
    ".nox",
    "build",
    "dist",
}


def should_skip(path: Path) -> bool:
    """Check if a path should be skipped."""
    return any(pattern in str(path) for pattern in SKIP_PATTERNS)


def find_python_modules(package_dir: Path, namespace_prefix: str) -> list[str]:
    """Find all Python modules in a package directory."""
    modules = []
    src_dir = package_dir / "src"

    if not src_dir.exists():
        logger.warning(f"No src directory found in {package_dir}")
        return modules

    # Find the actual package directory (e.g., src/haive/core)
    haive_dir = src_dir / "haive"
    if not haive_dir.exists():
        logger.warning(f"No haive directory found in {src_dir}")
        return modules

    # Get the specific package subdirectory
    package_name = namespace_prefix.split(".")[-1]  # e.g., 'core' from 'haive.core'
    package_path = haive_dir / package_name

    if not package_path.exists():
        logger.warning(f"Package path {package_path} does not exist")
        return modules

    def scan_directory(dir_path: Path, current_module: str):
        """Recursively scan directory for Python modules."""
        if should_skip(dir_path):
            return

        # Check if this directory is a Python package
        init_file = dir_path / "__init__.py"
        if init_file.exists():
            modules.append(current_module)
            logger.debug(f"Found module: {current_module}")

        # Scan Python files in this directory
        for py_file in dir_path.glob("*.py"):
            if should_skip(py_file) or py_file.name == "__init__.py":
                continue

            module_name = py_file.stem
            full_module = f"{current_module}.{module_name}"
            modules.append(full_module)
            logger.debug(f"Found module: {full_module}")

        # Recursively scan subdirectories
        for subdir in dir_path.iterdir():
            if subdir.is_dir() and not should_skip(subdir):
                submodule = f"{current_module}.{subdir.name}"
                scan_directory(subdir, submodule)

    # Start scanning from the package root
    scan_directory(package_path, namespace_prefix)

    # Sort modules for consistent ordering
    modules.sort()
    return modules


def can_import_module(module_name: str) -> bool:
    """Check if a module can be imported."""
    try:
        spec = importlib.util.find_spec(module_name)
        return spec is not None
    except (ImportError, ModuleNotFoundError, ValueError):
        return False


def get_module_info(module_name: str) -> dict[str, any]:
    """Get information about a module for documentation."""
    info = {
        "name": module_name,
        "short_name": module_name.split(".")[-1],
        "can_import": can_import_module(module_name),
        "description": "",
    }

    # Try to get module docstring
    try:
        if info["can_import"]:
            module = importlib.import_module(module_name)
            if hasattr(module, "__doc__") and module.__doc__:
                info["description"] = module.__doc__.split("\n")[0].strip()
    except Exception as e:
        logger.debug(f"Could not import {module_name}: {e}")

    return info


def create_module_rst(module_info: dict[str, any]) -> str:
    """Create RST content for a module."""
    module_name = module_info["name"]
    module_info["short_name"]
    description = module_info.get("description", "")

    # Create header
    title = module_name
    underline = "=" * len(title)

    rst_content = f"""{title}
{underline}

.. py:module:: {module_name}

.. currentmodule:: {module_name}

"""

    # Add description if available
    if description:
        rst_content += f"""{description}

"""

    # Add module path info
    rst_content += f""".. raw:: html

   <div class="module-path" style="margin-bottom: 1rem; color: var(--color-foreground-secondary);">
      <code>{module_name}</code>
   </div>

"""

    # Add automodule directive with comprehensive options
    rst_content += f""".. automodule:: {module_name}
   :members:
   :undoc-members:
   :show-inheritance:
   :inherited-members:
   :special-members: __init__, __call__, __new__
   :imported-members:
   :exclude-members: logger
"""

    return rst_content


def create_modules_directory():
    """Create the modules directory if it doesn't exist."""
    MODULES_DIR.mkdir(parents=True, exist_ok=True)
    logger.info(f"Created modules directory: {MODULES_DIR}")


def generate_package_modules(package_name: str, namespace: str) -> list[str]:
    """Generate module documentation for a specific package."""
    package_dir = PACKAGES_DIR / package_name
    if not package_dir.exists():
        logger.warning(f"Package directory {package_dir} does not exist")
        return []

    logger.info(f"Generating modules for {package_name} -> {namespace}")

    # Find all modules in the package
    modules = find_python_modules(package_dir, namespace)

    if not modules:
        logger.warning(f"No modules found for {package_name}")
        return []

    logger.info(f"Found {len(modules)} modules in {package_name}")

    generated_files = []

    for module_name in modules:
        # Get module information
        module_info = get_module_info(module_name)

        # Create RST content
        rst_content = create_module_rst(module_info)

        # Write to file
        rst_filename = f"{module_name}.rst"
        rst_path = MODULES_DIR / rst_filename

        try:
            rst_path.write_text(rst_content, encoding="utf-8")
            generated_files.append(rst_filename)

            status = "✅" if module_info["can_import"] else "⚠️"
            logger.info(f"{status} Generated: {rst_filename}")

        except Exception as e:
            logger.exception(f"Failed to write {rst_filename}: {e}")

    return generated_files


def main():
    """Main function to generate all module documentation."""
    logger.info("Starting module documentation generation...")

    # Create modules directory
    create_modules_directory()

    # Track all generated files
    all_generated = []

    # Generate for each package
    for package_name, namespace in PACKAGE_MAPPINGS.items():
        try:
            generated = generate_package_modules(package_name, namespace)
            all_generated.extend(generated)
        except Exception as e:
            logger.exception(f"Failed to generate modules for {package_name}: {e}")

    # Summary
    logger.info("✅ Generation complete!"!")
    logger.info(f"📄 Generated {len(all_generated)} module files")
    logger.info(f"📁 Files saved to: {MODULES_DIR}")

    if not all_generated:
        logger.warning("⚠️ No module files were generated - check package structure")
        return 1

    # Show some examples
    logger.info("📋 Sample generated files:")
    for file in sorted(all_generated)[:5]:
        logger.info(f"   - {file}")

    if len(all_generated) > 5:
        logger.info(f"   ... and {len(all_generated) - 5} more")

    return 0


if __name__ == "__main__":
    sys.exit(main())
