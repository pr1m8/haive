#!/usr/bin/env python3
"""Generate a summary of docstring analysis results.

Quick overview of the documentation status across packages.
"""

from collections import defaultdict
import os
import re


def analyze_summary(report_path: str) -> None:
    """Analyze the report and show key statistics."""
    with open(report_path) as f:
        content = f.read()

    # Extract total counts
    total_match = re.search(r"Total issues found: (\d+)", content)
    missing_match = re.search(r"Missing docstrings: (\d+)", content)
    incomplete_match = re.search(r"Incomplete docstrings: (\d+)", content)
    public_match = re.search(r"Public API issues: (\d+)", content)

    print("=== DOCSTRING ANALYSIS SUMMARY ===")
    print()

    if total_match:
        print(f"📊 Total Issues: {total_match.group(1)}")
    if missing_match:
        print(f"❌ Missing Docstrings: {missing_match.group(1)}")
    if incomplete_match:
        print(f"⚠️  Incomplete Docstrings: {incomplete_match.group(1)}")
    if public_match:
        print(f"🔥 Public API Issues: {public_match.group(1)}")

    print()

    # Find the "Files with Most Issues" section
    files_section = re.search(
        r"## Files with Most Issues.*?Top 10 files.*?\n(.*?)(?=\n##|\n$)",
        content,
        re.DOTALL,
    )

    if files_section:
        print("=== TOP 10 WORST FILES ===")
        lines = files_section.group(1).strip().split("\n")
        for i, line in enumerate(lines[:10], 1):
            if line.strip().startswith("-"):
                # Extract file and issue count
                match = re.search(r"- ([^:]+): (\d+) issues \((\d+) public\)", line)
                if match:
                    file_path = os.path.relpath(match.group(1))
                    total_issues = match.group(2)
                    public_issues = match.group(3)
                    print(f"{i:2d}. {file_path}")
                    print(
                        f"    📈 {total_issues} total issues ({public_issues} public)"
                    )

    print()

    # Extract package statistics
    package_stats = defaultdict(lambda: {"total": 0, "public": 0, "files": set()})

    # Look for issue lines in HIGH and MEDIUM PRIORITY sections
    priority_sections = re.findall(
        r"## (HIGH|MEDIUM) PRIORITY.*?\n(.*?)(?=\n##|\n$)", content, re.DOTALL
    )

    for section_name, section_content in priority_sections:
        lines = section_content.split("\n")
        for line in lines:
            if line.strip().startswith("- packages/"):
                match = re.search(r"packages/([^/]+)/", line)
                if match:
                    package = match.group(1)
                    file_match = re.search(r"- ([^:]+):", line)
                    if file_match:
                        package_stats[package]["files"].add(file_match.group(1))
                        package_stats[package]["total"] += 1
                        # Assume it's public if in HIGH/MEDIUM priority
                        package_stats[package]["public"] += 1

    if package_stats:
        print("=== PACKAGE OVERVIEW ===")
        sorted_packages = sorted(
            package_stats.items(), key=lambda x: x[1]["total"], reverse=True
        )

        for package, stats in sorted_packages:
            print(f"📦 {package}")
            print(f"   Issues: {stats['total']} ({stats['public']} public)")
            print(f"   Files affected: {len(stats['files'])}")
            print()

    print("=== RECOMMENDATIONS ===")
    print()
    print("1. 🎯 START WITH: haive-core module docstrings")
    print("   - These are foundation for all AutoAPI navigation")
    print("   - Focus on engine/, schema/, graph/ directories")
    print()
    print("2. 🔥 NEXT: haive-agents main classes")
    print("   - SimpleAgent, ReactAgent, base classes")
    print("   - These are primary user entry points")
    print()
    print("3. 📝 THEN: Complete public methods")
    print("   - __init__, run, arun, execute methods")
    print("   - Tool and utility functions")
    print()
    print("4. ✅ FINALLY: Internal/private items")
    print("   - Lower priority but helps completeness")
    print()
    print("🚀 Use the action plan for specific file priorities!")


def main():
    """Main function."""
    import argparse

    parser = argparse.ArgumentParser(description="Summarize docstring analysis")
    parser.add_argument(
        "--report",
        default="project_docs/documentation_fix/MISSING_DOCSTRINGS_REPORT.md",
        help="Path to the docstring analysis report",
    )

    args = parser.parse_args()

    if not os.path.exists(args.report):
        print(f"Error: Report file not found: {args.report}")
        print("Run analyze_missing_docstrings.py first to generate the report.")
        return 1

    analyze_summary(args.report)


if __name__ == "__main__":
    main()
