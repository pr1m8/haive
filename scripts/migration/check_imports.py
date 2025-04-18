#!/usr/bin/env python3
"""Check if packages can be imported and identify major issues."""

import importlib
import sys
from pathlib import Path


def check_package(package_path):
    """Check if a package can be imported."""
    pkg_name = Path(package_path).name.replace("-", "_")

    try:
        # Try importing the package
        importlib.import_module(pkg_name)
        return True
    except Exception:
        return False


def main():
    if len(sys.argv) < 2:
        sys.exit(1)

    packages_dir = Path(sys.argv[1])

    if not packages_dir.is_dir():
        sys.exit(1)

    successful = 0
    failed = 0

    # Add the parent directory to sys.path so we can import the packages
    sys.path.insert(0, str(packages_dir.parent))

    for pkg_dir in packages_dir.iterdir():
        if pkg_dir.is_dir() and not pkg_dir.name.startswith("."):
            if check_package(pkg_dir):
                successful += 1
            else:
                failed += 1

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
