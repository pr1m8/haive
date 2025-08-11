#!/usr/bin/env python3
"""Check syntax errors in haive-mcp package."""

import ast
import sys
from pathlib import Path
from typing import Dict, List, Tuple


def check_file_syntax(file_path: Path) -> Tuple[bool, str]:
    """Check syntax of a single Python file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Try to parse the file
        ast.parse(content)
        return True, ""
    except SyntaxError as e:
        return False, f"SyntaxError at line {e.lineno}: {e.msg}"
    except UnicodeDecodeError as e:
        return False, f"UnicodeDecodeError: {e}"
    except Exception as e:
        return False, f"Error: {e}"


def scan_directory() -> Dict[str, List[Tuple[Path, str]]]:
    """Scan for Python files with syntax errors."""
    current_dir = Path(".")
    python_files = list(current_dir.rglob("*.py"))

    results = {"valid": [], "invalid": []}

    print(f"🔍 Scanning {len(python_files)} Python files in haive-mcp...")

    for file_path in python_files:
        # Skip __pycache__ and other generated directories
        if any(
            part.startswith(".") or part == "__pycache__" for part in file_path.parts
        ):
            continue

        is_valid, error_msg = check_file_syntax(file_path)

        if is_valid:
            results["valid"].append((file_path, ""))
        else:
            results["invalid"].append((file_path, error_msg))

    return results


def main():
    """Main function."""
    results = scan_directory()

    if not results["invalid"]:
        print("\n✅ No syntax errors found!")
        return 0

    print(f"\n❌ Found {len(results['invalid'])} files with syntax errors:")
    print()

    for file_path, error_msg in results["invalid"]:
        print(f"📁 {file_path}")
        print(f"   ❌ {error_msg}")
        print()

    print("📊 Error Summary:")
    error_counts = {}
    for _, error_msg in results["invalid"]:
        error_type = error_msg.split(":")[0] if ":" in error_msg else error_msg
        error_counts[error_type] = error_counts.get(error_type, 0) + 1

    for error_type, count in sorted(error_counts.items()):
        print(f"   - {error_type}: {count}")

    return 1


if __name__ == "__main__":
    sys.exit(main())
