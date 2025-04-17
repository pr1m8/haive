
#!/usr/bin/env python3
"""
Check if packages can be imported and identify major issues.
"""

import sys
import importlib
from pathlib import Path
import traceback

def check_package(package_path):
    """Check if a package can be imported."""
    pkg_name = Path(package_path).name.replace('-', '_')
    print(f"Checking {pkg_name}...")
    
    try:
        # Try importing the package
        module = importlib.import_module(pkg_name)
        print(f"✅ Successfully imported {pkg_name}")
        return True
    except Exception as e:
        print(f"❌ Error importing {pkg_name}: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python check_imports.py <packages_dir>")
        sys.exit(1)
    
    packages_dir = Path(sys.argv[1])
    
    if not packages_dir.is_dir():
        print(f"Error: {packages_dir} is not a directory")
        sys.exit(1)
    
    successful = 0
    failed = 0
    
    # Add the parent directory to sys.path so we can import the packages
    sys.path.insert(0, str(packages_dir.parent))
    
    for pkg_dir in packages_dir.iterdir():
        if pkg_dir.is_dir() and not pkg_dir.name.startswith('.'):
            if check_package(pkg_dir):
                successful += 1
            else:
                failed += 1
    
    print(f"\nSummary: {successful} packages importable, {failed} packages with issues")
    
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())