#!/usr/bin/env python3
"""Find the most recent indentation error that's blocking the docs build."""

import ast
import sys
from pathlib import Path


def check_indentation_error(file_path: Path):
    """Check for specific indentation errors."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Try to compile to catch indentation errors
        compile(content, str(file_path), "exec")
        return None

    except IndentationError as e:
        # Check if it's the "unexpected indent" error
        if "unexpected indent" in str(e):
            return {
                "file": file_path,
                "line": e.lineno,
                "text": e.text.strip() if e.text else "N/A",
                "msg": e.msg,
            }
    except SyntaxError:
        # Ignore other syntax errors for now
        pass
    except Exception:
        # Ignore other errors
        pass

    return None


def main():
    """Find indentation errors in haive packages."""
    print("🔍 Searching for 'unexpected indent' errors...\n")

    errors = []

    # Check all Python files in packages
    for py_file in Path("packages/").rglob("*.py"):
        # Skip cache directories
        if "__pycache__" in str(py_file):
            continue

        error = check_indentation_error(py_file)
        if error:
            errors.append(error)

    if not errors:
        print("✅ No 'unexpected indent' errors found!")
        return 0

    print(f"❌ Found {len(errors)} files with 'unexpected indent' errors:\n")

    # Sort by file path
    errors.sort(key=lambda x: str(x["file"]))

    for error in errors:
        try:
            rel_path = error["file"].relative_to(Path.cwd())
        except ValueError:
            rel_path = error["file"]

        print(f"📁 {rel_path}")
        print(f"   Line {error['line']}: {error['msg']}")
        print(f"   Text: {error['text']}")
        print()

    return 1


if __name__ == "__main__":
    sys.exit(main())
