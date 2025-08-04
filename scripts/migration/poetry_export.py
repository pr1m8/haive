#!/usr/bin/env python3
"""Advanced Dependency Management and Distribution Script for Haive Monorepo.

This script provides intelligent dependency management across multiple
packages, with a focus on monorepo dependency distribution and
standardization.
"""

from __future__ import annotations

from collections import defaultdict
import logging
from pathlib import Path
import sys
from typing import Any

import toml

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("haive-dependency-manager")


class HaiveDependencyManager:

    def __init__(self, project_root: Path | None = None):
        """Initialize the Dependency Manager.

        Args:
            project_root: Root directory of the project. Defaults to script location.
        """
        self.project_root = project_root or Path(__file__).resolve().parents[2]
        self.packages_dir = self.project_root / "packages"

        # Standard package configurations
        self.PACKAGES = [
            "haive-core",
            "haive-agents",
            "haive-tools",
            "haive-games",
            "haive-dataflow",
            "haive-prebuilt",
        ]

        # Toolkit mappings
        self.TOOLKIT_MAPPING = {
            "gmail_toolkit": "haive-tools",
            "github_toolkit": "haive-tools",
            # ... other toolkit mappings ...
        }

    def load_root_pyproject(self) -> dict[str, Any]:
        """Load and parse the root pyproject.toml."""
        try:
            with open(self.project_root / "pyproject.toml") as f:
                return toml.load(f)
        except Exception as e:
            logger.exception(f"Failed to load root pyproject.toml: {e}")
            return {}

    def export_dev_dependencies_to_core(self, root_pyproject: dict[str, Any]):
        """Export development dependencies to haive-core package.

        Args:
            root_pyproject: Parsed root pyproject configuration
        """
        core_pyproject_path = self.packages_dir / "haive-core" / "pyproject.toml"

        try:
            # Load existing core pyproject
            core_pyproject = toml.load(
                core_pyproject_path) if core_pyproject_path.exists() else {}

            # Extract dev dependencies from root
            root_dev_deps = (root_pyproject.get("tool", {}).get(
                "poetry", {}).get("group", {}).get("dev",
                                                   {}).get("dependencies", {}))

            # Ensure nested structure exists
            core_pyproject.setdefault("tool", {})
            core_pyproject["tool"].setdefault("poetry", {})
            core_pyproject["tool"]["poetry"].setdefault("group", {})

            # Update dev dependencies
            core_pyproject["tool"]["poetry"]["group"]["dev"] = {
                "dependencies": root_dev_deps,
            }

            # Write updated configuration
            with open(core_pyproject_path, "w") as f:
                toml.dump(core_pyproject, f)

            logger.info(
                "✅ Successfully exported dev dependencies to haive-core")
            for dep, version in root_dev_deps.items():
                logger.info(f"  - {dep}: {version}")

        except Exception as e:
            logger.exception(f"Failed to export dev dependencies: {e}")

    def distribute_toolkits(self, root_pyproject: dict[str, Any]):
        """Distribute toolkits across packages based on predefined mapping.

        Args:
            root_pyproject: Parsed root pyproject configuration
        """
        group_packages = self._extract_toolkit_dependencies(root_pyproject)

        for package_name, toolkits in group_packages.items():
            try:
                package_path = self.packages_dir / package_name
                pyproject_path = package_path / "pyproject.toml"

                if not pyproject_path.exists():
                    logger.warning(
                        f"No pyproject.toml found for {package_name}")
                    continue

                package_pyproject = toml.load(pyproject_path)

                # Update package pyproject with toolkit dependencies
                package_pyproject.setdefault("tool", {})
                package_pyproject["tool"].setdefault("poetry", {})
                package_pyproject["tool"]["poetry"].setdefault("group", {})

                for toolkit_name, toolkit_deps in toolkits.items():
                    package_pyproject["tool"]["poetry"]["group"][
                        toolkit_name] = {
                            "dependencies": toolkit_deps,
                    }

                # Write updated configuration
                with open(pyproject_path, "w") as f:
                    toml.dump(package_pyproject, f)

                logger.info(f"✅ Updated toolkits for {package_name}")

            except Exception as e:
                logger.exception(f"Error processing {package_name}: {e}")

    def _extract_toolkit_dependencies(
        self,
        root_pyproject: dict[str, Any],
    ) -> dict[str, dict[str, Any]]:
        """Extract toolkit dependencies and map them to packages.

        Args:
            root_pyproject: Parsed root pyproject configuration

        Returns:
            Dictionary mapping package names to their toolkit dependencies
        """
        toolkit_distribution = defaultdict(dict)

        groups = root_pyproject.get("tool", {}).get("poetry",
                                                    {}).get("group", {})

        for group_name, group_data in groups.items():
            target_package = self.TOOLKIT_MAPPING.get(group_name)

            if target_package and "dependencies" in group_data:
                toolkit_distribution[target_package][group_name] = group_data[
                    "dependencies"]

        return dict(toolkit_distribution)

    def run(self):
        """Main execution method to manage dependencies."""
        logger.info("🚀 Starting Haive Dependency Management")

        # Load root pyproject
        root_pyproject = self.load_root_pyproject()

        if not root_pyproject:
            logger.error("❌ Cannot proceed without root pyproject.toml")
            sys.exit(1)

        # Export dev dependencies to core
        self.export_dev_dependencies_to_core(root_pyproject)

        # Distribute toolkits
        self.distribute_toolkits(root_pyproject)

        logger.info("✨ Dependency Management Complete!")


def main():
    dependency_manager = HaiveDependencyManager()
    dependency_manager.run()


if __name__ == "__main__":
    main()
