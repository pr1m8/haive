#!/usr/bin/env python3
"""Comprehensive documentation build system for Haive monorepo.

This script handles building documentation for individual packages and
the aggregated root-level documentation with proper cross-linking.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import contextmanager
from dataclasses import dataclass
import logging
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@contextmanager
def temporary_chdir(path: Path):
    """Context manager for safely changing working directory.

    Args:
        path: Directory to change to

    Yields:
        None

    Example:
        with temporary_chdir(Path("/tmp")):
            # Do work in /tmp
            pass
        # Automatically returns to original directory
    """
    original_cwd = Path.cwd()
    try:
        os.chdir(path)
        logger.debug(f"Changed to directory: {path}")
        yield
    finally:
        os.chdir(original_cwd)
        logger.debug(f"Restored directory: {original_cwd}")


@dataclass
class BuildResult:
    """Result of a documentation build operation."""

    package: str
    success: bool
    duration: float
    output_dir: Path
    errors: list[str] = None
    warnings: list[str] = None

    def __post_init__(self):
        if self.errors is None:
            self.errors = []
        if self.warnings is None:
            self.warnings = []


@dataclass
class PackageConfig:
    """Configuration for a package documentation build."""

    name: str
    path: Path
    docs_dir: Path
    output_dir: Path
    dependencies: list[str] = None

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


class MonorepoDocsBuilder:
    """Advanced documentation builder for monorepo architecture.

    This class handles the complex task of building documentation
    for multiple interdependent packages in a monorepo structure
    with proper cross-linking and aggregation.

    Features:
    - Parallel package builds with dependency resolution
    - Cross-package intersphinx linking
    - Comprehensive error reporting and recovery
    - Build caching and incremental updates
    - Root-level documentation aggregation
    """

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.packages_dir = project_root / "packages"
        self.root_docs_dir = project_root / "docs"
        self.shared_config_dir = project_root / "docs" / "config"
        self.build_dir = project_root / "_build"
        self.build_cache = self.build_dir / ".cache"

        # Package discovery and configuration
        self.packages = self._discover_packages()
        self._build_dependency_graph()

        # Build state
        self.build_results = {}
        self.failed_packages = set()

    def _discover_packages(self) -> dict[str, PackageConfig]:
        """Discover all packages in the monorepo."""
        packages = {}

        if not self.packages_dir.exists():
            return packages

        for package_dir in self.packages_dir.iterdir():
            if not package_dir.is_dir():
                continue

            pyproject_file = package_dir / "pyproject.toml"
            docs_dir = package_dir / "docs"

            if not pyproject_file.exists() or not docs_dir.exists():
                continue

            # Extract package name from pyproject.toml
            package_name = self._extract_package_name(pyproject_file)
            if not package_name:
                package_name = package_dir.name

            packages[package_name] = PackageConfig(
                name=package_name,
                path=package_dir,
                docs_dir=docs_dir,
                output_dir=self.build_dir / "packages" / package_name,
            )

        return packages

    def _extract_package_name(self, pyproject_file: Path) -> str | None:
        """Extract package name from pyproject.toml."""
        try:
            # Simple TOML parsing for package name
            content = pyproject_file.read_text()
            for line in content.split("\n"):
                if line.strip().startswith("name ="):
                    # Extract name from: name = "package-name"
                    return line.split("=")[1].strip().strip("\"'")
        except Exception:
            pass
        return None

    def _build_dependency_graph(self):
        """Build dependency graph between packages."""
        for package_name, config in self.packages.items():
            pyproject_file = config.path / "pyproject.toml"
            if pyproject_file.exists():
                deps = self._extract_local_dependencies(pyproject_file)
                config.dependencies = [
                    dep for dep in deps if dep in self.packages
                ]

    def _extract_local_dependencies(self, pyproject_file: Path) -> list[str]:
        """Extract local package dependencies."""
        try:
            content = pyproject_file.read_text()
            deps = []
            in_deps_section = False

            for line in content.split("\n"):
                line = line.strip()

                if line == "[tool.poetry.dependencies]":
                    in_deps_section = True
                    continue
                if line.startswith("[") and in_deps_section:
                    in_deps_section = False
                    continue

                if in_deps_section and "path =" in line and "haive-" in line:
                    # Extract dependency name
                    dep_name = line.split("=")[0].strip()
                    deps.append(dep_name)

            return deps
        except Exception:
            return []

    def build_all(
        self,
        parallel: bool = True,
        max_workers: int = 4,
        clean: bool = False,
        include_root: bool = True,
    ) -> dict[str, BuildResult]:
        """Build documentation for all packages and root.

        Args:
            parallel: Whether to build packages in parallel
            max_workers: Maximum number of parallel workers
            clean: Whether to clean build directory first
            include_root: Whether to build root documentation

        Returns:
            Dictionary of build results by package name
        """
        print("🚀 Starting monorepo documentation build")
        print(
            f"📦 Found {len(self.packages)} packages: {', '.join(self.packages.keys())}",
        )

        if clean:
            self._clean_build_directory()

        # Create build directories
        self._prepare_build_directories()

        # Build packages
        if parallel and len(self.packages) > 1:
            results = self._build_packages_parallel(max_workers)
        else:
            results = self._build_packages_sequential()

        # Build root documentation if requested
        if include_root:
            root_result = self._build_root_documentation()
            results["haive"] = root_result

        self.build_results = results
        self._print_build_summary()

        return results

    def build_package(self, package_name: str) -> BuildResult:
        """Build documentation for a specific package."""
        if package_name not in self.packages:
            return BuildResult(
                package=package_name,
                success=False,
                duration=0.0,
                output_dir=Path(),
                errors=[f"Package '{package_name}' not found"],
            )

        return self._build_single_package(self.packages[package_name])

    def _clean_build_directory(self):
        """Clean the build directory."""
        if self.build_dir.exists():
            print(f"🧹 Cleaning build directory: {self.build_dir}")
            shutil.rmtree(self.build_dir)

    def _prepare_build_directories(self):
        """Prepare necessary build directories."""
        self.build_dir.mkdir(exist_ok=True)
        self.build_cache.mkdir(exist_ok=True)
        (self.build_dir / "packages").mkdir(exist_ok=True)

        for config in self.packages.values():
            config.output_dir.mkdir(parents=True, exist_ok=True)

    def _build_packages_sequential(self) -> dict[str, BuildResult]:
        """Build packages sequentially."""
        results = {}
        build_order = self._get_build_order()

        for package_name in build_order:
            print(f"📝 Building {package_name} documentation...")
            config = self.packages[package_name]
            result = self._build_single_package(config)
            results[package_name] = result

            if not result.success:
                self.failed_packages.add(package_name)
                print(f"❌ Failed to build {package_name}: {result.errors}")

        return results

    def _build_packages_parallel(
        self,
        max_workers: int,
    ) -> dict[str, BuildResult]:
        """Build packages in parallel respecting dependencies."""
        results = {}
        remaining_packages = set(self.packages.keys())

        while remaining_packages:
            # Find packages that can be built now (dependencies satisfied)
            ready_packages = []
            for package_name in remaining_packages:
                config = self.packages[package_name]
                deps_satisfied = all(dep not in remaining_packages
                                     or dep in self.failed_packages
                                     for dep in config.dependencies)
                if deps_satisfied:
                    ready_packages.append(package_name)

            if not ready_packages:
                # Circular dependency or all remaining packages failed
                for package_name in remaining_packages:
                    results[package_name] = BuildResult(
                        package=package_name,
                        success=False,
                        duration=0.0,
                        output_dir=self.packages[package_name].output_dir,
                        errors=["Circular dependency or dependency failure"],
                    )
                break

            # Build ready packages in parallel
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                future_to_package = {
                    executor.submit(self._build_single_package, self.packages[pkg]):
                    pkg
                    for pkg in ready_packages
                }

                for future in as_completed(future_to_package):
                    package_name = future_to_package[future]
                    try:
                        result = future.result()
                        results[package_name] = result

                        if not result.success:
                            self.failed_packages.add(package_name)
                            print(f"❌ Failed to build {package_name}")
                        else:
                            print(f"✅ Successfully built {package_name}")

                    except Exception as e:
                        results[package_name] = BuildResult(
                            package=package_name,
                            success=False,
                            duration=0.0,
                            output_dir=self.packages[package_name].output_dir,
                            errors=[str(e)],
                        )
                        self.failed_packages.add(package_name)

            # Remove completed packages from remaining
            for package_name in ready_packages:
                remaining_packages.discard(package_name)

        return results

    def _build_single_package(self, config: PackageConfig) -> BuildResult:
        """Build documentation for a single package."""
        start_time = time.time()

        try:
            with temporary_chdir(config.docs_dir):
                # Build command
                cmd = [
                    sys.executable,
                    "-m",
                    "sphinx",
                    "-b",
                    "html",
                    "-d",
                    str(config.output_dir / ".doctrees"),
                    ".",
                    str(config.output_dir),
                ]

                # Run sphinx build
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=300,
                    check=False,  # 5 minute timeout
                )

            duration = time.time() - start_time

            # Parse output for errors and warnings
            errors, warnings = self._parse_sphinx_output(
                result.stderr + result.stdout, )

            build_result = BuildResult(
                package=config.name,
                success=result.returncode == 0,
                duration=duration,
                output_dir=config.output_dir,
                errors=errors,
                warnings=warnings,
            )

            return build_result

        except subprocess.TimeoutExpired:
            return BuildResult(
                package=config.name,
                success=False,
                duration=time.time() - start_time,
                output_dir=config.output_dir,
                errors=["Build timeout (>5 minutes)"],
            )
        except Exception as e:
            return BuildResult(
                package=config.name,
                success=False,
                duration=time.time() - start_time,
                output_dir=config.output_dir,
                errors=[str(e)],
            )

    def _build_root_documentation(self) -> BuildResult:
        """Build root-level aggregated documentation."""
        print("📚 Building root-level documentation...")
        start_time = time.time()

        try:
            root_output_dir = self.build_dir / "html"
            root_output_dir.mkdir(exist_ok=True)

            with temporary_chdir(self.root_docs_dir):
                # Build command
                cmd = [
                    sys.executable,
                    "-m",
                    "sphinx",
                    "-b",
                    "html",
                    "-d",
                    str(self.build_dir / ".doctrees"),
                    ".",
                    str(root_output_dir),
                ]

                # Run sphinx build
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=600,
                    check=False,  # 10 minute timeout for root docs
                )

            duration = time.time() - start_time
            errors, warnings = self._parse_sphinx_output(
                result.stderr + result.stdout, )

            return BuildResult(
                package="haive",
                success=result.returncode == 0,
                duration=duration,
                output_dir=root_output_dir,
                errors=errors,
                warnings=warnings,
            )

        except Exception as e:
            return BuildResult(
                package="haive",
                success=False,
                duration=time.time() - start_time,
                output_dir=self.build_dir / "html",
                errors=[str(e)],
            )

    def _get_build_order(self) -> list[str]:
        """Get build order respecting dependencies."""
        # Simple topological sort
        visited = set()
        temp_visited = set()
        result = []

        def visit(package_name: str):
            if package_name in temp_visited:
                # Circular dependency - ignore for now
                return
            if package_name in visited:
                return

            temp_visited.add(package_name)

            config = self.packages.get(package_name)
            if config:
                for dep in config.dependencies:
                    if dep in self.packages:
                        visit(dep)

            temp_visited.remove(package_name)
            visited.add(package_name)
            result.append(package_name)

        for package_name in self.packages:
            visit(package_name)

        return result

    def _parse_sphinx_output(self, output: str) -> tuple[list[str], list[str]]:
        """Parse Sphinx output for errors and warnings."""
        errors = []
        warnings = []

        for line in output.split("\n"):
            line = line.strip()
            if "ERROR:" in line or "CRITICAL:" in line:
                errors.append(line)
            elif "WARNING:" in line:
                warnings.append(line)

        return errors, warnings

    def _print_build_summary(self):
        """Print comprehensive build summary."""
        total_packages = len(self.build_results)
        successful = sum(1 for result in self.build_results.values()
                         if result.success)
        failed = total_packages - successful
        total_duration = sum(result.duration
                             for result in self.build_results.values())

        print("\n" + "=" * 80)
        print("📊 BUILD SUMMARY")
        print("=" * 80)
        print(f"Total packages: {total_packages}")
        print(f"✅ Successful: {successful}")
        print(f"❌ Failed: {failed}")
        print(f"⏱️  Total time: {total_duration:.2f}s")
        print()

        # Detailed results
        for package_name, result in self.build_results.items():
            status = "✅ SUCCESS" if result.success else "❌ FAILED"
            print(f"{status} {package_name} ({result.duration:.2f}s)")

            if result.warnings:
                print(f"   ⚠️  {len(result.warnings)} warnings")
            if result.errors:
                print(f"   🚨 {len(result.errors)} errors")
                for error in result.errors[:3]:  # Show first 3 errors
                    print(f"      {error}")
                if len(result.errors) > 3:
                    print(
                        f"      ... and {len(result.errors) - 3} more errors",
                    )

        if successful == total_packages:
            print("\n🎉 All documentation built successfully!")
            if "haive" in self.build_results:
                print(
                    f"📖 Root documentation: {self.build_results['haive'].output_dir}",
                )
        else:
            print(f"\n⚠️  {failed} package(s) failed to build")


def main():
    """Main entry point for the build script."""
    parser = argparse.ArgumentParser(
        description="Build documentation for Haive monorepo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python build-monorepo-docs.py                    # Build all packages
  python build-monorepo-docs.py --clean            # Clean build
  python build-monorepo-docs.py --package core     # Build specific package
  python build-monorepo-docs.py --no-parallel      # Sequential build
        """,
    )

    parser.add_argument(
        "--clean",
        "-c",
        action="store_true",
        help="Clean build directory before building",
    )

    parser.add_argument(
        "--package",
        "-p",
        type=str,
        help="Build specific package only",
    )

    parser.add_argument(
        "--no-parallel",
        action="store_true",
        help="Build packages sequentially instead of in parallel",
    )

    parser.add_argument(
        "--max-workers",
        "-j",
        type=int,
        default=4,
        help="Maximum number of parallel workers (default: 4)",
    )

    parser.add_argument(
        "--no-root",
        action="store_true",
        help="Skip building root documentation",
    )

    args = parser.parse_args()

    # Find project root
    project_root = Path(__file__).parent.parent.parent
    builder = MonorepoDocsBuilder(project_root)

    if not builder.packages:
        print("❌ No packages found in the monorepo")
        return 1

    # Build specific package or all packages
    if args.package:
        if args.package not in builder.packages:
            print(f"❌ Package '{args.package}' not found")
            print(f"Available packages: {', '.join(builder.packages.keys())}")
            return 1

        result = builder.build_package(args.package)
        if result.success:
            print(f"✅ Successfully built {args.package}")
            return 0
        print(f"❌ Failed to build {args.package}")
        return 1
    # Build all packages
    results = builder.build_all(
        parallel=not args.no_parallel,
        max_workers=args.max_workers,
        clean=args.clean,
        include_root=not args.no_root,
    )

    # Return error code if any builds failed
    failed_count = sum(1 for result in results.values() if not result.success)
    return min(failed_count, 1)


if __name__ == "__main__":
    sys.exit(main())
