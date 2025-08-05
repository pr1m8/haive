#!/usr/bin/env python3
"""Debug script to find Python syntax errors in the codebase."""
from __future__ import annotations

import ast
import sys
from pathlib import Path


def check_file_syntax(file_path: Path) -> tuple[bool, str]:
    """Check if a Python file has syntax errors.

    Returns:
        (success, error_message)
    """
    try:
        with open(file_path, encoding='utf-8') as f:
            content = f.read()

        # Try to parse the file
        ast.parse(content, filename=str(file_path))
        return True, ''

    except SyntaxError as e:
        return False, f"SyntaxError at line {e.lineno}: {e.msg}"
    except IndentationError as e:
        return False, f"IndentationError at line {e.lineno}: {e.msg}"
    except Exception as e:
        return False, f"Error: {type(e).__name__}: {e!s}"


def scan_directory(directory: Path) -> list[tuple[Path, str]]:
    """Scan directory for Python files with syntax errors."""
    errors = []

    for py_file in directory.rglob('*.py'):
        # Skip some directories
        if any(
            skip in str(py_file)
            for skip in [
                '__pycache__',
                '.git',
                '.tox',
                '.nox',
                'build',
                'dist',
                '.egg',
                '.venv',
            ]
        ):
            continue

        success, error_msg = check_file_syntax(py_file)
        if not success:
            errors.append((py_file, error_msg))

    return errors


def main():
    """Main function."""
    if len(sys.argv) > 1:
        search_path = Path(sys.argv[1])
    else:
        search_path = Path('packages/')

    print(f"🔍 Scanning {search_path} for Python syntax errors...\n")

    errors = scan_directory(search_path)

    if not errors:
        print('✅ No syntax errors found!')
        return 0

    print(f"❌ Found {len(errors)} files with syntax errors:\n")

    for file_path, error_msg in errors:
        # Make path relative for readability
        try:
            rel_path = file_path.relative_to(Path.cwd())
        except ValueError:
            rel_path = file_path

        print(f"📁 {rel_path}")
        print(f"   ❌ {error_msg}\n")

    # Group by error type
    error_types = {}
    for _, error_msg in errors:
        error_type = error_msg.split(':')[0]
        error_types[error_type] = error_types.get(error_type, 0) + 1

    print('\n📊 Error Summary:')
    for error_type, count in sorted(error_types.items()):
        print(f"   - {error_type}: {count}")

    return 1


if __name__ == '__main__':
    sys.exit(main())
