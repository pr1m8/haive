#!/usr/bin/env python3
"""Find remaining import errors efficiently."""

import ast
import sys
import traceback
from collections import Counter, defaultdict
from pathlib import Path

# Add packages to path
packages_dir = Path(__file__).parent / "packages"
for package_dir in packages_dir.glob("haive-*/src"):
    sys.path.insert(0, str(package_dir))


def check_imports(file_path):
    """Check a single file for import errors."""
    errors = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Try to parse the AST
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return errors

        # Extract imports
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    try:
                        exec(f"import {alias.name}")
                    except ImportError as e:
                        errors.append(
                            {
                                "file": str(file_path),
                                "line": node.lineno,
                                "type": "import",
                                "module": alias.name,
                                "error": str(e),
                            }
                        )
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    try:
                        if module:
                            exec(f"from {module} import {alias.name}")
                        else:
                            exec(f"import {alias.name}")
                    except ImportError as e:
                        errors.append(
                            {
                                "file": str(file_path),
                                "line": node.lineno,
                                "type": "from_import",
                                "module": module,
                                "name": alias.name,
                                "error": str(e),
                            }
                        )
    except Exception:
        pass

    return errors


def main():
    """Find all remaining import errors."""
    print("🔍 Scanning for remaining import errors...\n")

    all_errors = []
    files_checked = 0

    # Check all Python files
    for package in [
        "haive-core",
        "haive-agents",
        "haive-tools",
        "haive-games",
        "haive-dataflow",
        "haive-mcp",
        "haive-prebuilt",
    ]:
        package_src = packages_dir / package / "src"
        if package_src.exists():
            for py_file in package_src.rglob("*.py"):
                files_checked += 1
                errors = check_imports(py_file)
                all_errors.extend(errors)

    print(f"✅ Checked {files_checked} files")
    print(f"❌ Found {len(all_errors)} import errors\n")

    # Analyze patterns
    missing_modules = Counter()
    failed_imports = Counter()
    error_by_package = defaultdict(int)

    for error in all_errors:
        package = error["file"].split("/haive-")[1].split("/")[0]
        error_by_package[package] += 1

        if error["type"] == "import":
            missing_modules[error["module"]] += 1
        else:
            failed_imports[f"{error['module']}.{error['name']}"] += 1

    print("📊 Errors by package:")
    for package, count in sorted(error_by_package.items()):
        print(f"  haive-{package}: {count}")

    print("\n🔝 Top 20 import issues:")
    all_issues = missing_modules + failed_imports
    for issue, count in all_issues.most_common(20):
        print(f"  {issue}: {count} occurrences")

    # Group similar errors for bulk fixes
    print("\n🔧 Suggested bulk fixes:")

    # Find relative import patterns
    relative_imports = defaultdict(list)
    for error in all_errors:
        if (
            error["type"] == "from_import"
            and error["module"]
            and not error["module"].startswith("haive")
        ):
            relative_imports[error["module"]].append(error["file"])

    if relative_imports:
        print("\n1. Fix relative imports:")
        for module, files in list(relative_imports.items())[:5]:
            print(f"   '{module}' -> 'haive.XXX.{module}' in {len(files)} files")

    # Find missing exports
    missing_exports = defaultdict(list)
    for error in all_errors:
        if "cannot import name" in error["error"]:
            missing_exports[error["module"]].append(error["name"])

    if missing_exports:
        print("\n2. Add missing exports to __init__.py files:")
        for module, names in list(missing_exports.items())[:5]:
            print(f"   {module}: {', '.join(set(names[:3]))}")

    # Find deprecated imports
    deprecated = defaultdict(int)
    for error in all_errors:
        if "langchain" in error.get("module", ""):
            deprecated[error["module"]] += 1

    if deprecated:
        print("\n3. Update deprecated imports:")
        for module, count in list(deprecated.items())[:5]:
            if "embeddings" in module:
                print(f"   {module} -> langchain_community.embeddings ({count} files)")
            elif "vectorstores" in module:
                print(
                    f"   {module} -> langchain_community.vectorstores ({count} files)"
                )


if __name__ == "__main__":
    main()
