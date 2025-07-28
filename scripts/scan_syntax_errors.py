#!/usr/bin/env python3
"""Scan for syntax errors in Python files and categorize them."""

import ast
from collections import defaultdict
import json
from pathlib import Path
import re
import sys


def find_python_files(root_dir: Path, exclude_patterns: list[str]) -> list[Path]:
    """Find all Python files, excluding certain patterns."""
    python_files = []

    for pattern in ["**/*.py"]:
        for file_path in root_dir.glob(pattern):
            # Skip if matches exclude pattern
            if any(exc in str(file_path) for exc in exclude_patterns):
                continue
            python_files.append(file_path)

    return python_files


def check_syntax(file_path: Path) -> tuple[bool, str, int]:
    """Check if a Python file has syntax errors.

    Returns:
        Tuple of (has_error, error_message, line_number)
    """
    try:
        with open(file_path, encoding="utf-8") as f:
            source = f.read()

        # Try to parse with ast
        ast.parse(source)
        return False, "", 0

    except SyntaxError as e:
        return True, str(e.msg), e.lineno or 0
    except Exception as e:
        # Other parsing errors
        return True, str(e), 0


def categorize_error(error_msg: str) -> str:
    """Categorize syntax error by type."""
    error_lower = error_msg.lower()

    if "unterminated string" in error_lower:
        return "unterminated string literal"
    if "unexpected character after line continuation" in error_lower:
        return "line continuation error"
    if "unmatched" in error_lower:
        return "unmatched bracket/parenthesis"
    if "invalid syntax" in error_lower:
        return "invalid syntax"
    if "indent" in error_lower:
        return "indentation error"
    if "f-string" in error_lower:
        return "f-string error"
    if "expected" in error_lower:
        return "expected token error"
    if "was never closed" in error_lower:
        return "unclosed bracket/parenthesis"
    return "other syntax error"


def get_line_context(file_path: Path, line_number: int, context_lines: int = 2) -> dict:
    """Get the problematic line with context."""
    try:
        with open(file_path, encoding="utf-8") as f:
            lines = f.readlines()

        if line_number > 0 and line_number <= len(lines):
            start = max(0, line_number - context_lines - 1)
            end = min(len(lines), line_number + context_lines)

            context = {
                "line": lines[line_number - 1].rstrip() if line_number > 0 else "",
                "line_number": line_number,
                "context": [],
            }

            for i in range(start, end):
                prefix = ">>> " if i == line_number - 1 else "    "
                context["context"].append(f"{prefix}{i+1}: {lines[i].rstrip()}")

            return context
    except:
        return {"line": "", "line_number": line_number, "context": []}


def analyze_error_for_fix(file_path: Path, line_number: int, error_msg: str) -> str:
    """Analyze error and suggest a fix."""
    try:
        context = get_line_context(file_path, line_number)
        line = context.get("line", "")

        if "unterminated string" in error_msg.lower():
            # Check for common patterns
            if re.search(r'"\s*[^"\s]+"\s*\)', line):
                # Pattern like print("text"extra")
                extra_match = re.search(r'"([^"]*)"([^")\s]+)("\s*\))', line)
                if extra_match:
                    return f"Remove extra '{extra_match.group(2)}'"

            # Check for missing quote
            if line.count('"') % 2 == 1:
                return "Add missing closing double quote"
            if line.count("'") % 2 == 1:
                return "Add missing closing single quote"

        elif "continuation" in error_msg.lower():
            if "\\" in line:
                # Check what's after the backslash
                idx = line.rfind("\\")
                after = line[idx + 1 :].strip()
                if after:
                    return f"Remove '{after}' after line continuation"

        elif "invalid syntax" in error_msg.lower():
            # Check for common issues
            if re.search(r"\[\s*\]", line):
                return "Empty index [] - add index value"
            if re.search(r"=\s*,", line):
                return "Missing value after ="
            if re.search(r",\s*\)", line):
                return "Trailing comma before closing parenthesis"

        return ""
    except:
        return ""


def main():
    """Main scanning function."""
    print("Scanning for Python syntax errors...")

    # Define paths
    root_dir = Path(".")
    exclude_patterns = [
        "__pycache__",
        ".git",
        "build",
        "dist",
        ".egg-info",
        ".venv",
        "venv",
        ".tox",
        ".pytest_cache",
        "node_modules",
        "migrations",
    ]

    # Find Python files
    python_files = find_python_files(root_dir, exclude_patterns)
    print(f"Found {len(python_files)} Python files to scan")

    # Scan for errors
    errors_by_type = defaultdict(list)
    total_errors = 0
    files_with_errors = set()

    for file_path in python_files:
        has_error, error_msg, line_number = check_syntax(file_path)

        if has_error:
            total_errors += 1
            files_with_errors.add(str(file_path))

            # Get error category
            category = categorize_error(error_msg)

            # Get line context
            context = get_line_context(file_path, line_number)

            # Get fix suggestion
            suggestion = analyze_error_for_fix(file_path, line_number, error_msg)

            error_info = {
                "file": str(file_path),
                "line": line_number,
                "error": error_msg,
                "category": category,
                "code": context.get("line", ""),
                "context": context.get("context", []),
                "suggestion": suggestion,
            }

            errors_by_type[category].append(error_info)

    # Summary
    print(f"\nFound {total_errors} syntax errors in {len(files_with_errors)} files")
    print("\nErrors by category:")

    for category, errors in sorted(
        errors_by_type.items(), key=lambda x: len(x[1]), reverse=True
    ):
        print(f"  {category}: {len(errors)} errors")

    # Save detailed report
    report = {
        "summary": {
            "total_errors": total_errors,
            "files_with_errors": len(files_with_errors),
            "errors_by_category": {k: len(v) for k, v in errors_by_type.items()},
        },
        "errors_by_type": dict(errors_by_type),
        "all_errors": [error for errors in errors_by_type.values() for error in errors],
    }

    with open("syntax_errors_report.json", "w") as f:
        json.dump(report, f, indent=2)

    print("\nDetailed report saved to: syntax_errors_report.json")

    # Also save a human-readable report
    with open("syntax_errors_readable.txt", "w") as f:
        f.write("Python Syntax Errors Report\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Total errors: {total_errors}\n")
        f.write(f"Files with errors: {len(files_with_errors)}\n\n")

        for category, errors in sorted(
            errors_by_type.items(), key=lambda x: len(x[1]), reverse=True
        ):
            f.write(f"\n{category.upper()} ({len(errors)} errors)\n")
            f.write("-" * 60 + "\n")

            for error in errors[:5]:  # Show first 5 of each type
                f.write(f"\nFile: {error['file']}\n")
                f.write(f"Line {error['line']}: {error['error']}\n")
                if error["suggestion"]:
                    f.write(f"Suggestion: {error['suggestion']}\n")
                f.write("Context:\n")
                for line in error["context"]:
                    f.write(f"  {line}\n")

            if len(errors) > 5:
                f.write(f"\n... and {len(errors) - 5} more {category} errors\n")

    print("Human-readable report saved to: syntax_errors_readable.txt")

    return 0


if __name__ == "__main__":
    sys.exit(main())
