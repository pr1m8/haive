#!/usr/bin/env python3
"""Check all imports in the Haive project before documentation build."""

from __future__ import annotations

import ast
import importlib
import os
import sys
import traceback
import warnings
from collections import defaultdict
from pathlib import Path

# Suppress warnings during import checking

warnings.filterwarnings("ignore")

# Add all package sources to Python path
project_root = Path(__file__).parent
packages_dir = project_root / "packages"

for package_dir in packages_dir.glob("haive-*/src"):
    sys.path.insert(0, str(package_dir))


def find_all_python_files(directory):
    """Find all Python files in a directory."""
    return list(Path(directory).rglob("*.py"))


def get_imports_from_file(filepath):
    """Extract all import statements from a Python file."""
    imports = []
    try:
        with open(filepath, encoding="utf-8") as f:
            tree = ast.parse(f.read())

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    if module:
                        imports.append(f"{module}.{alias.name}")
                    else:
                        imports.append(alias.name)
    except Exception as e:
        print(f"⚠️  Error parsing {filepath}: {e}")

    return imports


def check_module_import(module_name):
    """Try to import a module and return error info if it fails."""
    try:
        importlib.import_module(module_name)
        return None
    except ModuleNotFoundError as e:
        return {
            "type": "ModuleNotFoundError",
            "error": str(e),
            "missing": e.name if hasattr(e, "name") else module_name,
        }
    except ImportError as e:
        return {
            "type": "ImportError",
            "error": str(e),
            "details": traceback.format_exc(),
        }
    except Exception as e:
        return {
            "type": type(e).__name__,
            "error": str(e),
            "details": traceback.format_exc(),
        }


def main():
    print("🔍 Checking all imports in Haive packages...\n")

    # Output file
    output_file = Path("import_errors_list.txt")
    output_lines = []

    # Track all errors
    errors_by_type = defaultdict(list)
    missing_modules = defaultdict(int)
    total_modules = 0
    successful_imports = 0

    # Check each package
    packages = [
        "haive-core",
        "haive-agents",
        "haive-tools",
        "haive-games",
        "haive-dataflow",
        "haive-mcp",
        "haive-prebuilt",
    ]

    for package in packages:
        print(f"\n📦 Checking {package}...")
        package_src = packages_dir / package / "src"

        if not package_src.exists():
            print(f"  ⚠️  Source directory not found: {package_src}")
            continue

        # Find all Python files
        python_files = find_all_python_files(package_src)
        print(f"  Found {len(python_files)} Python files")

        # Get all haive modules from the package
        haive_modules = []
        for py_file in python_files:
            relative_path = py_file.relative_to(package_src)
            if relative_path.name == "__init__.py":
                module_path = relative_path.parent
            else:
                module_path = relative_path.with_suffix("")

            module_name = str(module_path).replace(os.sep, ".")
            if module_name and module_name != ".":
                haive_modules.append(module_name)

        # Check each module
        package_errors = 0
        for module in haive_modules:
            total_modules += 1
            error = check_module_import(module)

            if error:
                package_errors += 1
                errors_by_type[error["type"]].append(
                    {"module": module, "package": package, **error},
                )

                if error["type"] == "ModuleNotFoundError":
                    missing_modules[error["missing"]] += 1
            else:
                successful_imports += 1

        print(
            f"  ✅ {len(haive_modules) - package_errors}/{len(haive_modules)} modules import successfully",
        )
        if package_errors > 0:
            print(f"  ❌ {package_errors} import errors")

    # Print summary
    print("\n" + "=" * 80)
    print("📊 IMPORT CHECK SUMMARY")
    print("=" * 80)
    print(f"Total modules checked: {total_modules}")
    print(f"Successful imports: {successful_imports}")
    print(f"Failed imports: {total_modules - successful_imports}")

    if errors_by_type:
        print("\n🔴 ERROR BREAKDOWN:")
        for error_type, errors in errors_by_type.items():
            print(f"  {error_type}: {len(errors)}")

        print("\n❌ TOP MISSING MODULES:")
        sorted_missing = sorted(
            missing_modules.items(),
            key=lambda x: x[1],
            reverse=True,
        )
        for module, count in sorted_missing[:10]:
            print(f"  {module}: {count} times")

        print("\n⚠️  SAMPLE ERRORS BY TYPE:")
        for error_type, errors in errors_by_type.items():
            print(f"\n{error_type} ({len(errors)} total):")
            # Show up to 3 examples per type
            for error in errors[:3]:
                print(f"  Module: {error['module']}")
                print(f"  Package: {error['package']}")
                print(f"  Error: {error['error']}")
                if error_type == "ImportError" and "details" in error:
                    # Show the actual import error line
                    details_lines = error["details"].split("\n")
                    for line in details_lines:
                        if "cannot import name" in line or "from" in line:
                            print(f"  Details: {line.strip()}")
                            break
                print()

    # Generate mock imports for conf.py
    if missing_modules:
        print("\n📝 MOCK IMPORTS FOR SPHINX (add to conf.py):")
        print("autodoc_mock_imports.extend([")
        for module in sorted(missing_modules.keys()):
            print(f'    "{module}",')
        print("])")

    # Write detailed error list to file
    output_lines.append("# Haive Import Errors List")
    output_lines.append(f"# Generated: {Path.cwd()}")
    output_lines.append(f"# Total modules checked: {total_modules}")
    output_lines.append(f"# Failed imports: {total_modules - successful_imports}")
    output_lines.append("")

    # Group errors by type
    for error_type, errors in sorted(errors_by_type.items()):
        output_lines.append(f"\n## {error_type} ({len(errors)} errors)")
        output_lines.append("")

        # Sort errors by module name
        sorted_errors = sorted(errors, key=lambda x: x["module"])

        for error in sorted_errors:
            output_lines.append(f"### {error['module']}")
            output_lines.append(f"- Package: {error['package']}")
            output_lines.append(f"- Error: {error['error']}")
            if "details" in error and error_type == "ImportError":
                # Extract the specific import error
                for line in error["details"].split("\n"):
                    if "cannot import name" in line or "from" in line:
                        output_lines.append(f"- Details: {line.strip()}")
                        break
            output_lines.append("")

    # Add missing modules summary
    if missing_modules:
        output_lines.append("\n## Missing Modules Summary")
        output_lines.append("")
        sorted_missing = sorted(
            missing_modules.items(),
            key=lambda x: x[1],
            reverse=True,
        )
        for module, count in sorted_missing:
            output_lines.append(f"- {module}: {count} occurrences")

    # Write to file
    with open(output_file, "w") as f:
        f.write("\n".join(output_lines))

    print(f"\n📄 Detailed error list saved to: {output_file}")

    return total_modules - successful_imports


if __name__ == "__main__":
    exit_code = main()
    sys.exit(1 if exit_code > 0 else 0)
