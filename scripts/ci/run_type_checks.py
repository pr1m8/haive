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
    print(f"\n{'='*80}\nRunning mypy on {package_name}\n{'='*80}")
    
    # Run mypy
    src_dir = Path(package_dir) / "src"
    tests_dir = Path(package_dir) / "tests"
    
    if src_dir.exists():
        result = subprocess.run(
            ["mypy", str(src_dir)],
            capture_output=True,
            text=True
        )
        
        # Print output
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
            
        # Return error code
        return result.returncode == 0
    else:
        print(f"No src directory found in {package_dir}")
        return True

def main():
    """Main entry point."""
    packages = find_packages()
    print(f"Found {len(packages)} packages to check")
    
    # Track success
    success = True
    
    for name, path in packages:
        if not run_mypy(name, path):
            success = False
    
    if not success:
        print("\n❌ Type checking failed!")
        sys.exit(1)
    
    print("\n✅ All type checks passed!")

if __name__ == "__main__":
    main()