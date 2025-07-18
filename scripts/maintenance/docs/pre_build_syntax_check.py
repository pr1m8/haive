#!/usr/bin/env python3
"""Pre-build syntax checker for Haive documentation.

This script checks all Python files for syntax errors before running the documentation build,
saving time by catching issues early.
"""

import ast
import py_compile
import sys
from pathlib import Path


def check_syntax_with_ast(file_path: Path) -> tuple[bool, str]:
    """Check syntax using AST parsing."""
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()
        ast.parse(content)
        return True, ""
    except SyntaxError as e:
        return False, f"Line {e.lineno}: {e.msg}\n  Text: {e.text}"
    except Exception as e:
        return False, f"Unexpected error: {e}"


def check_syntax_with_py_compile(file_path: Path) -> tuple[bool, str]:
    """Check syntax using py_compile."""
    try:
        py_compile.compile(file_path, doraise=True)
        return True, ""
    except py_compile.PyCompileError as e:
        return False, f"Compilation error: {e}"
    except Exception as e:
        return False, f"Unexpected error: {e}"


def find_python_files() -> list[Path]:
    """Find all Python files in the packages directory."""
    packages_dir = Path("packages")
    python_files = []

    if packages_dir.exists():
        for package_dir in packages_dir.iterdir():
            if package_dir.is_dir() and package_dir.name.startswith("haive-"):
                src_dir = package_dir / "src"
                if src_dir.exists():
                    python_files.extend(src_dir.rglob("*.py"))

    return python_files


def main():
    """Main syntax checking function."""

    # Find all Python files
    python_files = find_python_files()

    # Check syntax
    errors = []
    warnings = []

    for i, file_path in enumerate(python_files, 1):
        # Progress indicator
        if i % 50 == 0 or i == len(python_files):
            pass

        # Check with AST first (faster)
        ast_ok, ast_error = check_syntax_with_ast(file_path)
        if not ast_ok:
            errors.append((file_path, f"AST: {ast_error}"))
            continue

        # Check with py_compile (more thorough)
        compile_ok, compile_error = check_syntax_with_py_compile(file_path)
        if not compile_ok:
            # Some compile errors might be warnings (like unused imports)
            if (
                "unused" in compile_error.lower()
                or "imported but never used" in compile_error.lower()
            ):
                warnings.append((file_path, f"Compile: {compile_error}"))
            else:
                errors.append((file_path, f"Compile: {compile_error}"))

    # Report results

    if errors:
        for file_path, error in errors:
    else:
        pass")

    if warnings:
        for file_path, warning in warnings:


    if errors:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
