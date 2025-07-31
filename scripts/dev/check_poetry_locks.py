# scripts/dev/check_poetry_locks.py
#!/usr/bin/env python
"""Check that Poetry lock files are in sync with pyproject.toml files."""

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

    # Check root package
    if Path("pyproject.toml").exists():
        packages.append(".")

    # Check sub-packages
    packages_dir = Path("packages")
    if packages_dir.exists():
        for item in packages_dir.glob("*"):
            if item.is_dir() and (item / "pyproject.toml").exists():
                packages.append(str(item))

    return packages


def check_lock_file(package_dir):
    """Check if lock file is in sync with pyproject.toml."""
    result = subprocess.run(
        ["poetry", "lock", "--check"],
        cwd=package_dir,
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode == 0, result.stderr if result.returncode != 0 else ""


def main():
    """Main entry point."""
    packages = find_packages()

    all_good = True
    for package in packages:
        is_sync, error = check_lock_file(package)
        if not is_sync:
            all_good = False
        else:
            pass

    if not all_good:
        sys.exit(1)


if __name__ == "__main__":
    main()
