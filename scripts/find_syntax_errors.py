#!/usr/bin/env python3
"""Find Python files with syntax errors in the source code."""

import ast
import sys
from pathlib import Path
from typing import List, Tuple


def check_syntax(file_path: Path) -> Tuple[bool, str]:
    """Check if Python file has valid syntax."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        ast.parse(content)
        return True, ""
    except SyntaxError as e:
        return False, f"Line {e.lineno}: {e.msg}"
    except Exception as e:
        return False, f"Error: {str(e)}"


def find_syntax_errors(base_path: Path, limit: int = 10) -> List[Tuple[Path, str]]:
    """Find Python files with syntax errors."""
    errors = []

    # Focus on source directories, skip .venv
    for pattern in ["*/src/**/*.py", "*/examples/**/*.py", "*/tests/**/*.py"]:
        for file_path in base_path.glob(pattern):
            if ".venv" in str(file_path) or "site-packages" in str(file_path):
                continue

            valid, error = check_syntax(file_path)
            if not valid:
                errors.append((file_path, error))
                if len(errors) >= limit:
                    return errors

    return errors


def main():
    base_path = Path("/home/will/Projects/haive/backend/haive/packages")

    print("Finding Python files with syntax errors...\n")

    errors = find_syntax_errors(base_path, limit=20)

    if not errors:
        print("No syntax errors found in source files!")
        return

    print(f"Found {len(errors)} files with syntax errors:\n")

    for file_path, error in errors:
        relative_path = file_path.relative_to(base_path.parent)
        print(f"📄 {relative_path}")
        print(f"   ❌ {error}")
        print()

        # Show the problematic lines
        try:
            with open(file_path, "r") as f:
                lines = f.readlines()
                if "Line" in error:
                    line_no = int(error.split("Line ")[1].split(":")[0])
                    start = max(0, line_no - 3)
                    end = min(len(lines), line_no + 2)

                    print("   Code context:")
                    for i in range(start, end):
                        prefix = ">>>" if i == line_no - 1 else "   "
                        print(f"   {prefix} {i+1}: {lines[i].rstrip()}")
                    print()
        except:
            pass


if __name__ == "__main__":
    main()
