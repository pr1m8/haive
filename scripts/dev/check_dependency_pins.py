# scripts/dev/check_dependency_pins.py
#!/usr/bin/env python
"""Check that dependencies have appropriate version constraints."""

import re
import sys
from pathlib import Path
import tomli
import os
def find_poetry_files():
    """Find all pyproject.toml files in the repo."""
    # Get repository root (2 directories up from this script)
    repo_root = Path(__file__).parent.parent.parent.resolve()
    os.chdir(repo_root)
    
    poetry_files = []
    
    # Check root
    if Path("pyproject.toml").exists():
        poetry_files.append(Path("pyproject.toml"))
    
    # Check sub-packages
    packages_dir = Path("packages")
    if packages_dir.exists():
        for pyproject in packages_dir.glob("*/pyproject.toml"):
            poetry_files.append(pyproject)
    
    return poetry_files

def check_dependencies(poetry_file):
    """Check dependencies in a poetry file."""
    with open(poetry_file, "rb") as f:
        try:
            data = tomli.load(f)
        except Exception as e:
            print(f"Error parsing {poetry_file}: {e}")
            return False
    
    issues = []
    
    # Check main dependencies
    if "dependencies" in data.get("tool", {}).get("poetry", {}):
        deps = data["tool"]["poetry"]["dependencies"]
        for pkg, constraint in deps.items():
            if pkg == "python":
                continue
                
            if isinstance(constraint, str) and not any(c in constraint for c in ("^", "~", ">=", "==")):
                issues.append(f"- {pkg}: {constraint} (missing version constraint)")
            
            if isinstance(constraint, dict) and "version" in constraint:
                version = constraint["version"]
                if not any(c in version for c in ("^", "~", ">=", "==")):
                    issues.append(f"- {pkg}: {version} (missing version constraint)")
    
    # Check dev dependencies
    if "group" in data.get("tool", {}).get("poetry", {}):
        for group_name, group in data["tool"]["poetry"]["group"].items():
            if "dependencies" in group:
                for pkg, constraint in group["dependencies"].items():
                    if isinstance(constraint, str) and not any(c in constraint for c in ("^", "~", ">=", "==")):
                        issues.append(f"- {pkg} ({group_name}): {constraint} (missing version constraint)")
                    
                    if isinstance(constraint, dict) and "version" in constraint:
                        version = constraint["version"]
                        if not any(c in version for c in ("^", "~", ">=", "==")):
                            issues.append(f"- {pkg} ({group_name}): {version} (missing version constraint)")
    
    if issues:
        print(f"\n❌ Issues in {poetry_file}:")
        for issue in issues:
            print(issue)
        return False
    
    print(f"✅ {poetry_file} dependencies look good")
    return True

def main():
    """Main entry point."""
    poetry_files = find_poetry_files()
    all_good = True
    
    for file in poetry_files:
        if not check_dependencies(file):
            all_good = False
    
    if not all_good:
        print("\nSome dependencies are missing version constraints.")
        print("Add appropriate version constraints ('^', '~', '>=', '==') to dependencies.")
        sys.exit(1)
    
    print("\nAll dependencies have appropriate version constraints!")

if __name__ == "__main__":
    main()