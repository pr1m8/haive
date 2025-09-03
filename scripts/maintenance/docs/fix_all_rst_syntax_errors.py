#!/usr/bin/env python3
"""Find and fix RST syntax errors in documentation files."""
from __future__ import annotations

import re
from pathlib import Path


def find_malformed_directives(
    content: str, filepath: Path
) -> list[tuple[int, str, str]]:
    """Find malformed RST directives in content."""
    issues = []
    lines = content.split("\n")

    # Patterns to check
    patterns = [
        # Malformed autosummary
        (r"^\.\.\s+autosummary\s*::\s*$", "autosummary directive with no content"),
        # Malformed automodule/autoclass
        (
            r"^\.\.\s+auto(module|class|function)\s*::\s*$",
            "auto directive with no module specified",
        ),
        # Missing blank line after directive
        (r"^\.\.\s+\w+::\s*\S+.*\n[^\s]", "directive missing blank line after"),
        # Incorrect indentation in directives
        (r"^\.\.\s+\w+::\s*\n\s{0,2}\S", "directive content not properly indented"),
        # Orphaned directive options
        (r"^\s+:\w+:\s*\S+", "directive option without parent directive"),
    ]

    for i, line in enumerate(lines):
        for pattern, description in patterns:
            if re.match(pattern, line):
                issues.append((i + 1, line.strip(), description))

    # Check for autosummary with problematic module names
    autosummary_block = False
    autosummary_start = 0

    for i, line in enumerate(lines):
        if re.match(r"^\.\.\s+autosummary::", line):
            autosummary_block = True
        elif autosummary_block and line.strip() == "":
            # Empty line ends the block
            autosummary_block = False
        elif autosummary_block and line.strip() and not line.startswith(" "):
            # Non-indented content ends the block
            autosummary_block = False
        elif autosummary_block and line.strip():
            # Check module name
            module_name = line.strip()
            # Check for invalid Python module names
            if " " in module_name or "(" in module_name or ")" in module_name:
                issues.append(
                    (i + 1, line, f"Invalid module name in autosummary: {module_name}")
                )

    return issues


def find_broken_references(content: str, filepath: Path) -> list[tuple[int, str, str]]:
    """Find broken references in RST content."""
    issues = []
    lines = content.split("\n")

    # Check for various reference patterns
    for i, line in enumerate(lines):
        # Check for :ref: without backticks
        if ":ref:" in line and "`" not in line:
            issues.append((i + 1, line.strip(), "ref role missing backticks"))

        # Check for malformed doc references
        if ":doc:" in line and not re.search(r":doc:`[^`]+`", line):
            issues.append((i + 1, line.strip(), "malformed doc reference"))

        # Check for broken module references
        if ":mod:" in line or ":class:" in line or ":func:" in line:
            # Extract the reference
            matches = re.findall(r":(mod|class|func):`([^`]+)`", line)
            for role, ref in matches:
                # Check for spaces or invalid characters
                if " " in ref and "~" not in ref:
                    issues.append(
                        (i + 1, line.strip(), f"Space in {role} reference: {ref}")
                    )

    return issues


def check_rst_file(filepath: Path) -> list[tuple[str, int, str, str]]:
    """Check a single RST file for syntax errors."""
    all_issues = []

    try:
        content = filepath.read_text(encoding="utf-8")

        # Find malformed directives
        directive_issues = find_malformed_directives(content, filepath)
        for line_no, line, issue in directive_issues:
            all_issues.append((str(filepath), line_no, line, issue))

        # Find broken references
        ref_issues = find_broken_references(content, filepath)
        for line_no, line, issue in ref_issues:
            all_issues.append((str(filepath), line_no, line, issue))

    except Exception as e:
        all_issues.append((str(filepath), 0, "", f"Error reading file: {e}"))

    return all_issues


def main():
    """Main function to check all RST files."""
    project_root = Path(__file__).parent
    docs_dir = project_root / "docs" / "source"

    # Find all RST files
    rst_files = list(docs_dir.rglob("*.rst"))

    all_issues = []

    # Check each file
    for rst_file in rst_files:
        issues = check_rst_file(rst_file)
        all_issues.extend(issues)

    # Report findings
    if all_issues:

        # Group by file
        by_file = {}
        for filepath, line_no, line, issue in all_issues:
            if filepath not in by_file:
                by_file[filepath] = []
            by_file[filepath].append((line_no, line, issue))

        for filepath, issues in by_file.items():
            rel_path = Path(filepath).relative_to(project_root)
            for line_no, line, issue in sorted(issues):
                if line:
                    pass

        # Create a detailed report
        report_path = (
            project_root / "docs" / "error_reports" / "rst_syntax_errors_report.md"
        )
        report_path.parent.mkdir(exist_ok=True)

        with open(report_path, "w") as f:
            f.write("# RST Syntax Errors Report\n\n")
            f.write(
                f"Found {len(all_issues)} potential issues in {len(by_file)} files.\n\n"
            )

            for filepath, issues in by_file.items():
                rel_path = Path(filepath).relative_to(project_root)
                f.write(f"## {rel_path}\n\n")
                for line_no, line, issue in sorted(issues):
                    f.write(f"- **Line {line_no}**: {issue}\n")
                    if line:
                        f.write(f"  ```rst\n  {line}\n  ```\n")
                f.write("\n")

    else:
        pass")

    # Additional checks for problematic patterns

    # Check for files that might cause autosummary issues
    problematic_patterns = [
        ("**/*(*).py", "Python files with parentheses"),
        ("**/* *.py", "Python files with spaces"),
        ("**/*-*.py", "Python files with hyphens (should be underscores)"),
    ]

    for pattern, description in problematic_patterns:
        files = list(project_root.rglob(pattern))
        if files:
            for f in files[:10]:  # Show first 10
                pass
            if len(files) > 10:
                pass


if __name__ == "__main__":
    main()
