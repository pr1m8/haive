#!/usr/bin/env python3
"""Create a comprehensive catalog of all syntax errors with examples and
proposed fixes."""
from __future__ import annotations

import ast
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


def analyze_file(file_path: Path) -> dict[str, Any]:
    """Analyze a Python file for syntax errors with context."""
    try:
        with open(file_path, encoding="utf-8") as f:
            lines = f.readlines()

        # Try to parse the file
        with open(file_path, encoding="utf-8") as f:
            ast.parse(f.read(), filename=str(file_path))
        return None

    except (SyntaxError, IndentationError) as e:
        # Get context lines
        context_before = []
        context_after = []

        if e.lineno and e.lineno > 0:
            # Get 2 lines before and after
            start = max(0, e.lineno - 3)
            end = min(len(lines), e.lineno + 2)

            for i in range(start, end):
                if i < len(lines):
                    line_info = {
                        "line_num": i + 1,
                        "content": lines[i].rstrip(),
                        "is_error_line": (i + 1) == e.lineno,
                    }
                    if i < e.lineno - 1:
                        context_before.append(line_info)
                    elif i > e.lineno - 1:
                        context_after.append(line_info)

        return {
            "file": str(file_path),
            "line": e.lineno,
            "error_type": type(e).__name__,
            "msg": e.msg,
            "text": e.text.strip() if e.text else None,
            "category": categorize_error(e.msg),
            "context_before": context_before,
            "context_after": context_after,
            "error_line": (
                lines[e.lineno - 1].rstrip()
                if e.lineno and e.lineno <= len(lines)
                else None
            ),
            "proposed_fix": propose_fix(
                e.msg,
                e.text,
                lines[e.lineno - 1] if e.lineno and e.lineno <= len(lines) else None,
            ),
        }
    except Exception as e:
        return {
            "file": str(file_path),
            "line": 0,
            "error_type": type(e).__name__,
            "msg": str(e),
            "category": "other",
            "proposed_fix": None,
        }


def categorize_error(msg: str) -> str:
    """Categorize syntax error by message."""
    msg_lower = msg.lower()

    if "unterminated string" in msg_lower:
        return "unterminated_string"
    if "unexpected character after line continuation" in msg_lower:
        return "line_continuation"
    if "expected an indented block" in msg_lower:
        return "missing_indented_block"
    if "unexpected indent" in msg_lower:
        return "unexpected_indent"
    if "unmatched" in msg_lower:
        return "unmatched_bracket"
    if "invalid syntax" in msg_lower:
        return "invalid_syntax"
    if "closing parenthesis" in msg_lower and "does not match" in msg_lower:
        return "mismatched_parenthesis"
    if "expected" in msg_lower and ("except" in msg_lower or "finally" in msg_lower):
        return "missing_except_finally"
    return "other"


def propose_fix(msg: str, error_text: str, full_line: str) -> dict[str, str]:
    """Propose a fix for the error."""
    msg_lower = msg.lower()

    if "unterminated string" in msg_lower:
        # Find the quote type and suggest closing it
        if error_text:
            if '"' in error_text and not error_text.count('"') % 2 == 0:
                return {
                    "type": "add_quote",
                    "description": "Add closing double quote",
                    "example": error_text + '"',
                }
            if "'" in error_text and not error_text.count("'") % 2 == 0:
                return {
                    "type": "add_quote",
                    "description": "Add closing single quote",
                    "example": error_text + "'",
                }

    elif "unexpected character after line continuation" in msg_lower:
        if full_line and "\\" in full_line:
            # Show what needs to be escaped
            return {
                "type": "escape_backslash",
                "description": "Escape backslash or remove line continuation",
                "example": full_line.replace("\\n", "\\\\n")
                .replace("\\d", "\\\\d")
                .replace("\\w", "\\\\w"),
            }

    elif "expected an indented block" in msg_lower:
        # Find indentation level
        if full_line:
            indent = len(full_line) - len(full_line.lstrip())
            return {
                "type": "add_pass",
                "description": "Add indented pass statement",
                "example": " " * (indent + 4) + "pass",
            }

    elif "unmatched" in msg_lower:
        if error_text and "}" in error_text:
            return {
                "type": "remove_bracket",
                "description": "Remove extra closing bracket",
                "example": error_text.replace("}", ""),
            }

    elif "closing parenthesis" in msg_lower and "does not match" in msg_lower:
        # Extract the mismatched brackets
        if "}" in msg and "[" in msg:
            return {
                "type": "fix_bracket",
                "description": "Change } to ]",
                "example": full_line.replace("}", "]") if full_line else None,
            }
        if "]" in msg and "(" in msg:
            return {
                "type": "fix_bracket",
                "description": "Change ] to )",
                "example": full_line.replace("]", ")") if full_line else None,
            }

    return {
        "type": "manual_review",
        "description": "Requires manual review",
        "example": None,
    }


def main():
    """Create comprehensive error catalog."""
    if len(sys.argv) > 1:
        search_path = Path(sys.argv[1])
    else:
        search_path = Path("packages/")

    print(f"🔍 Cataloging syntax errors in {search_path}...\n")

    errors = []
    error_by_category = defaultdict(list)

    # Scan all Python files
    for py_file in search_path.rglob("*.py"):
        # Skip cache directories
        if any(
            skip in str(py_file)
            for skip in [
                "__pycache__",
                ".git",
                ".tox",
                ".nox",
                "build",
                "dist",
                ".egg",
                ".venv",
            ]
        ):
            continue

        error = analyze_file(py_file)
        if error:
            errors.append(error)
            error_by_category[error["category"]].append(error)

    # Create detailed catalog
    catalog = {
        "total_errors": len(errors),
        "categories": {cat: len(errs) for cat, errs in error_by_category.items()},
        "errors_by_category": {},
    }

    # Organize by category with examples
    for category, cat_errors in error_by_category.items():
        catalog["errors_by_category"][category] = {
            "count": len(cat_errors),
            "examples": cat_errors[:3],  # First 3 examples
            "all_files": [e["file"] for e in cat_errors],
        }

    # Save JSON catalog
    with open("syntax_errors_catalog.json", "w") as f:
        json.dump(catalog, f, indent=2)

    # Create human-readable report
    with open("syntax_errors_report_detailed.txt", "w") as f:
        f.write("COMPREHENSIVE SYNTAX ERROR CATALOG\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Total Errors: {len(errors)}\n\n")

        # Summary
        f.write("ERROR CATEGORIES:\n")
        for cat, count in sorted(error_by_category.items(), key=lambda x: -len(x[1])):
            f.write(f"  - {cat}: {count} errors\n")
        f.write("\n")

        # Detailed examples by category
        for category, cat_errors in sorted(error_by_category.items()):
            f.write(f"\n{'=' * 80}\n")
            f.write(f"{category.upper()} ({len(cat_errors)} errors)\n")
            f.write(f"{'=' * 80}\n\n")

            # Show first 5 examples with full context
            for i, error in enumerate(cat_errors[:5]):
                f.write(f"Example {i + 1}:\n")
                f.write(f"File: {error['file']}\n")
                f.write(f"Line {error['line']}: {error['msg']}\n")

                if error.get("context_before"):
                    f.write("\nContext:\n")
                    for ctx in error["context_before"]:
                        f.write(f"  {ctx['line_num']:4d}: {ctx['content']}\n")

                if error.get("error_line"):
                    f.write(
                        f"→ {error['line']:4d}: {error['error_line']}  ← ERROR HERE\n",
                    )

                if error.get("context_after"):
                    for ctx in error["context_after"]:
                        f.write(f"  {ctx['line_num']:4d}: {ctx['content']}\n")

                if error.get("proposed_fix"):
                    fix = error["proposed_fix"]
                    f.write(f"\nProposed Fix: {fix['description']}\n")
                    if fix.get("example"):
                        f.write(f"Example: {fix['example']}\n")

                f.write("\n" + "-" * 60 + "\n\n")

    # Print summary
    print(f"📊 Found {len(errors)} syntax errors\n")
    print("📈 Error Categories:")
    for cat, count in sorted(error_by_category.items(), key=lambda x: -len(x[1])):
        print(f"   {cat}: {count} errors")

    print("\n📄 Detailed catalog saved to:")
    print("   - syntax_errors_catalog.json (machine-readable)")
    print("   - syntax_errors_report_detailed.txt (human-readable with examples)")

    # Show a few examples
    print("\n📌 Sample Fixes:")
    shown = 0
    for cat, cat_errors in error_by_category.items():
        if shown >= 3:
            break
        for error in cat_errors[:1]:
            fix = error.get("proposed_fix")
            if fix and fix["type"] != "manual_review":
                print(f"\n{cat}: {error['file']}:{error['line']}")
                print(f"  Current: {error['error_line']}")
                if fix.get("example"):
                    print(f"  Fix: {fix['example']}")
                shown += 1


if __name__ == "__main__":
    main()
