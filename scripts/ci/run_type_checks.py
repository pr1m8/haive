# scripts/ci/run_type_checks.py
#!/usr/bin/env python
"""Run type checking across all packages."""

import os
import subprocess
import sys
from pathlib import Path


def find_packages():
    """Find all directories with pyproject.toml files."""
    # Get repository root (2 directories up from this script)
    repo_root = Path(__file__).parent.parent.parent.resolve()
    os.chdir(repo_root)

    packages = []

    # Check packages directory
    packages_dir = Path("packages")
    if packages_dir.exists():
        for item in packages_dir.glob("*"):
            if item.is_dir() and (item / "pyproject.toml").exists():
                packages.append((item.name, str(item)))

    return packages


def run_mypy(package_name, package_dir):
    """Run mypy on a package."""
    # Run mypy
    src_dir = Path(package_dir) / "src"
    Path(package_dir) / "tests"

    if src_dir.exists():
        result = subprocess.run(
            ["mypy", str(src_dir)], capture_output=True, text=True, check=False
        )

        # Print output
        if result.stdout:
            pass
        if result.stderr:
            pass

        # Return error code
        return result.returncode == 0
    return True


def main():
    """Main entry point."""
    packages = find_packages()

    # Track success
    success = True

    for name, path in packages:
        if not run_mypy(name, path):
            success = False

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
