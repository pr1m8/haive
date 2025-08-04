#!/usr/bin/env python3
"""Parse pyright JSON reports and generate actionable issue checklists.

This script processes the pyright JSON output files and creates readable
checklists for systematic issue resolution.
"""

from __future__ import annotations

from collections import defaultdict
import json
from pathlib import Path
from typing import Any


def load_pyright_report(json_file: Path) -> dict[str, Any]:
    """Load a pyright JSON report file."""
    try:
        with open(json_file) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading {json_file}: {e}")
        return {}


def group_issues_by_file(
        diagnostics: list[dict[str, Any]], ) -> dict[str, list[dict[str, Any]]]:
    """Group issues by file path."""
    grouped = defaultdict(list)
    for issue in diagnostics:
        file_path = issue.get("file", "unknown")
        # Get relative path from packages/
        if "packages/" in file_path:
            rel_path = file_path.split("packages/")[-1]
        else:
            rel_path = file_path
        grouped[rel_path].append(issue)
    return dict(grouped)


def group_issues_by_rule(
        diagnostics: list[dict[str, Any]], ) -> dict[str, list[dict[str, Any]]]:
    """Group issues by pyright rule."""
    grouped = defaultdict(list)
    for issue in diagnostics:
        rule = issue.get("rule", "unknown")
        grouped[rule].append(issue)
    return dict(grouped)


def format_issue_location(issue: dict[str, Any]) -> str:
    """Format the file location for an issue."""
    file_path = issue.get("file", "unknown")
    if "packages/" in file_path:
        rel_path = file_path.split("packages/")[-1]
    else:
        rel_path = file_path

    range_info = issue.get("range", {})
    start = range_info.get("start", {})
    line = start.get("line", 0) + 1  # Convert to 1-based
    char = start.get("character", 0)

    return f"{rel_path}:{line}:{char}"


def generate_package_checklist(
    package_name: str,
    error_data: dict[str, Any],
    warning_data: dict[str, Any] = None,
) -> str:
    """Generate a markdown checklist for a package."""

    error_diagnostics = error_data.get("generalDiagnostics", [])
    warning_diagnostics = warning_data.get("generalDiagnostics",
                                           []) if warning_data else []

    total_errors = len(error_diagnostics)
    total_warnings = len(warning_diagnostics)

    md = f"""# {package_name.upper()} - Pyright Issues Checklist

**Total Errors**: {total_errors}
**Total Warnings**: {total_warnings}
**Priority**: {"🔥 CRITICAL" if package_name in ["haive-core", "haive-agents"] else "📋 Standard"}

## Summary by Issue Type

"""

    # Group errors by rule
    if error_diagnostics:
        error_by_rule = group_issues_by_rule(error_diagnostics)
        md += "### Error Categories\n\n"
        for rule, issues in sorted(
                error_by_rule.items(),
                key=lambda x: len(x[1]),
                reverse=True,
        ):
            md += f"- **{rule}**: {len(issues)} issues\n"
        md += "\n"

    # Group warnings by rule
    if warning_diagnostics:
        warning_by_rule = group_issues_by_rule(warning_diagnostics)
        md += "### Warning Categories\n\n"
        for rule, issues in sorted(
                warning_by_rule.items(),
                key=lambda x: len(x[1]),
                reverse=True,
        ):
            md += f"- **{rule}**: {len(issues)} issues\n"
        md += "\n"

    # Detailed error checklist
    if error_diagnostics:
        md += "## 🚨 ERRORS (Must Fix)\n\n"

        # Group by file for better organization
        errors_by_file = group_issues_by_file(error_diagnostics)

        for file_path, file_issues in sorted(errors_by_file.items()):
            md += f"### 📄 {file_path}\n\n"

            for i, issue in enumerate(file_issues, 1):
                location = format_issue_location(issue)
                message = issue.get("message", "No message")
                rule = issue.get("rule", "unknown")

                md += f"- [ ] **Line {issue.get('range',
                                                {}).get('start',
                                                        {}).get('line',
                                                                0) + 1}** (`{rule}`)\n"
                md += f"  - **Issue**: {message}\n"
                md += f"  - **Location**: `{location}`\n\n"

    # Detailed warning checklist
    if warning_diagnostics:
        md += "## ⚠️ WARNINGS (Should Fix)\n\n"

        warnings_by_file = group_issues_by_file(warning_diagnostics)

        for file_path, file_issues in sorted(warnings_by_file.items()):
            md += f"### 📄 {file_path}\n\n"

            for i, issue in enumerate(file_issues, 1):
                location = format_issue_location(issue)
                message = issue.get("message", "No message")
                rule = issue.get("rule", "unknown")

                md += f"- [ ] **Line {issue.get('range',
                                                {}).get('start',
                                                        {}).get('line',
                                                                0) + 1}** (`{rule}`)\n"
                md += f"  - **Issue**: {message}\n"
                md += f"  - **Location**: `{location}`\n\n"

    if not error_diagnostics and not warning_diagnostics:
        md += "## ✅ No Issues Found!\n\nThis package has no pyright errors or warnings.\n\n"

    md += f"""
## Fix Priority Guidelines

### High Priority (Fix First)
1. `reportAttributeAccessIssue` - Missing/unknown attributes
2. `reportArgumentType` - Type mismatches in function calls
3. `reportOptionalMemberAccess` - Accessing potentially None objects

### Medium Priority
4. `reportTypedDictNotRequiredAccess` - Unsafe TypedDict access
5. `reportCallIssue` - Function call problems
6. `reportOptionalSubscript` - Subscripting None objects

### Low Priority (Polish)
7. `reportUnusedImport` - Cleanup unused imports
8. `reportUnnecessaryTypeIgnore` - Remove unnecessary ignores

## Testing After Fixes

```bash
# Test imports still work
poetry run python -c "from {package_name.replace("-", ".")} import *; print('✅ Imports OK')"

# Re-run pyright to verify fixes
poetry run pyright packages/{package_name}/src/ --level error

# Run any existing tests
poetry run pytest packages/{package_name}/tests/ -v
```

---

**Generated**: 2025-08-02
**Source**: `project_docs/build-reports/pyright-issues/{package_name}-*.json`
"""

    return md


def main():
    """Generate checklists for all packages."""

    # Base directories
    project_root = Path(__file__).parent.parent.parent
    reports_dir = project_root / "project_docs" / "build-reports" / "pyright-issues"
    output_dir = project_root / "project_docs" / "build-reports" / "pyright-checklists"

    # Create output directory
    output_dir.mkdir(exist_ok=True)

    # Package list
    packages = [
        "haive-core",
        "haive-agents",
        "haive-tools",
        "haive-games",
        "haive-mcp",
        "haive-dataflow",
        "haive-prebuilt",
    ]

    print("Generating pyright issue checklists...")

    for package in packages:
        print(f"Processing {package}...")

        # Load error report
        error_file = reports_dir / f"{package}-errors.json"
        error_data = load_pyright_report(error_file)

        # Load warning report (for critical packages)
        warning_file = reports_dir / f"{package}-warnings.json"
        warning_data = load_pyright_report(
            warning_file) if warning_file.exists() else None

        # Generate checklist
        checklist = generate_package_checklist(package, error_data,
                                               warning_data)

        # Write checklist file
        output_file = output_dir / f"{package}_issues_checklist.md"
        with open(output_file, "w") as f:
            f.write(checklist)

        print(f"  ✅ Generated: {output_file}")

    print(f"\n🎉 All checklists generated in: {output_dir}")
    print("\nNext steps:")
    print("1. Review package priority in PYRIGHT_ISSUES_SUMMARY.md")
    print("2. Start with haive-core checklist for critical fixes")
    print("3. Use checklists to systematically resolve all issues")


if __name__ == "__main__":
    main()
