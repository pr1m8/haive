from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Any

import toml

logger = logging.getLogger(__name__)


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

    def extract_top_level_external_dependencies(
        self,
        root_pyproject: dict[str, Any],
    ) -> dict[str, Any]:
        """Extract top-level external dependencies (excluding Haive packages).

        Args:
            root_pyproject: Parsed root pyproject configuration

        Returns:
            Dictionary of external dependencies
        """
        dependencies = (
            root_pyproject.get("tool", {}).get("poetry", {}).get("dependencies", {})
        )

        # Filter out Haive-specific packages
        external_deps = {
            dep: version
            for dep, version in dependencies.items()
            if not dep.startswith("haive-") and dep != "python"
        }

        return external_deps

    def distribute_external_dependencies(self, root_pyproject: dict[str, Any]):
        """Distribute external dependencies to core package.

        Args:
            root_pyproject: Parsed root pyproject configuration
        """
        external_deps = self.extract_top_level_external_dependencies(root_pyproject)

        core_pyproject_path = self.packages_dir / "haive-core" / "pyproject.toml"

        try:
            # Load existing core pyproject
            core_pyproject = (
                toml.load(core_pyproject_path) if core_pyproject_path.exists() else {}
            )

            # Ensure nested structure exists
            core_pyproject.setdefault("tool", {})
            core_pyproject["tool"].setdefault("poetry", {})

            # Update dependencies
            core_pyproject["tool"]["poetry"]["dependencies"] = external_deps

            # Ensure Python version is specified
            core_pyproject["tool"]["poetry"]["dependencies"]["python"] = "^3.12"

            # Write updated configuration
            with open(core_pyproject_path, "w") as f:
                toml.dump(core_pyproject, f)

            logger.info("✅ Successfully exported external dependencies to haive-core")
            for dep, version in external_deps.items():
                logger.info(f"  - {dep}: {version}")

        except Exception as e:
            logger.exception(f"Failed to export external dependencies: {e}")

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

        # Distribute external dependencies to core
        self.distribute_external_dependencies(root_pyproject)

        logger.info("✨ Dependency Management Complete!")


def main():
    dependency_manager = HaiveDependencyManager()
    dependency_manager.run()


if __name__ == "__main__":
    main()
