#!/usr/bin/env python3
"""Prioritize docstring fixes based on AutoAPI importance and usage patterns.

This script analyzes the docstring report and creates a prioritized action plan
for fixing the most important documentation issues first.
"""

import json
import os
import re
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

# Core packages in order of importance for AutoAPI
CORE_PACKAGES = [
    "haive-core",  # Foundation - highest priority
    "haive-agents",  # Main user-facing agents
    "haive-tools",  # Tools and utilities
    "haive-mcp",  # MCP integration
    "haive-games",  # Games package
    "haive-dataflow",  # Data flow
    "haive-prebuilt",  # Prebuilt components
]

# Key modules that are most important for AutoAPI documentation
PRIORITY_MODULES = {
    "haive-core": [
        "engine",  # AugLLMConfig and core engines
        "schema",  # State schemas and models
        "graph",  # Graph system
        "models",  # Core models
    ],
    "haive-agents": [
        "simple",  # SimpleAgent
        "react",  # ReactAgent
        "base",  # Base agent classes
        "rag",  # RAG agents
        "multi",  # Multi-agent systems
    ],
    "haive-tools": [
        "core",  # Core tools
        "web",  # Web tools
        "file",  # File tools
    ],
}

# AutoAPI-critical classes and functions
AUTOAPI_CRITICAL = [
    # Classes
    r"class\s+(\w*Agent)\b",
    r"class\s+(\w*Config)\b",
    r"class\s+(\w*Schema)\b",
    r"class\s+(\w*State)\b",
    r"class\s+(\w*Engine)\b",
    r"class\s+(\w*Graph)\b",
    r"class\s+(\w*Tool)\b",
    # Functions
    r"def\s+(run|arun|execute|process)\b",
    r"def\s+(create|build|compile)\b",
    r"def\s+(__init__|__call__)\b",
]


def parse_report_line(line: str) -> Tuple[str, int, str, str, str]:
    """Parse a report line to extract file info.

    Args:
        line: Report line like "- packages/.../file.py:123 - class `ClassName`"

    Returns:
        Tuple of (file_path, line_number, item_type, item_name, issue_type)
    """
    # Pattern: - file_path:line_number - item_type `item_name`
    pattern = r"- ([^:]+):(\d+) - (\w+) `([^`]+)`(?:: (.+))?"
    match = re.match(pattern, line.strip())

    if match:
        file_path = match.group(1)
        line_number = int(match.group(2))
        item_type = match.group(3)
        item_name = match.group(4)
        issue_type = match.group(5) or "missing"
        return file_path, line_number, item_type, item_name, issue_type

    return "", 0, "", "", ""


def calculate_priority_score(file_path: str, item_type: str, item_name: str) -> int:
    """Calculate priority score for a docstring issue.

    Args:
        file_path: Path to the Python file
        item_type: Type of item (class, function, method, module)
        item_name: Name of the item

    Returns:
        Priority score (higher = more important)
    """
    score = 0

    # Package priority (core packages are most important)
    for i, package in enumerate(CORE_PACKAGES):
        if package in file_path:
            score += (len(CORE_PACKAGES) - i) * 10
            break

    # Module priority within packages
    for package, modules in PRIORITY_MODULES.items():
        if package in file_path:
            for j, module in enumerate(modules):
                if f"/{module}/" in file_path or f"/{module}.py" in file_path:
                    score += (len(modules) - j) * 5
                    break

    # Item type priority
    type_scores = {
        "module": 20,  # Module docstrings are critical for AutoAPI
        "class": 15,  # Classes are main API entry points
        "function": 10,  # Public functions
        "method": 5,  # Methods (lower unless special)
    }
    score += type_scores.get(item_type, 0)

    # Special item name patterns (AutoAPI critical)
    for pattern in AUTOAPI_CRITICAL:
        if re.search(pattern, item_name):
            score += 15
            break

    # Special methods that are important
    if item_name in ("__init__", "__call__", "__repr__", "__str__"):
        score += 10

    # Public vs private (items starting with _ are lower priority)
    if item_name.startswith("_") and item_name not in (
        "__init__",
        "__call__",
        "__repr__",
        "__str__",
    ):
        score -= 5

    # File location importance
    if "/src/" in file_path and "/core/" in file_path:
        score += 8
    elif "/src/" in file_path and "/base/" in file_path:
        score += 6
    elif "/src/" in file_path:
        score += 4

    return max(score, 0)


def analyze_report(report_path: str) -> Dict[str, List]:
    """Analyze the docstring report and prioritize issues.

    Args:
        report_path: Path to the docstring analysis report

    Returns:
        Dictionary with prioritized issues and recommendations
    """
    issues = []

    with open(report_path, "r") as f:
        content = f.read()

    # Extract issues from HIGH PRIORITY and MEDIUM PRIORITY sections
    sections = ["HIGH PRIORITY", "MEDIUM PRIORITY"]

    for section in sections:
        section_start = content.find(f"## {section}")
        if section_start == -1:
            continue

        section_end = content.find("## ", section_start + 1)
        if section_end == -1:
            section_content = content[section_start:]
        else:
            section_content = content[section_start:section_end]

        # Extract issue lines
        lines = section_content.split("\n")
        for line in lines:
            if line.strip().startswith("- packages/"):
                file_path, line_num, item_type, item_name, issue_type = (
                    parse_report_line(line)
                )
                if file_path:
                    priority_score = calculate_priority_score(
                        file_path, item_type, item_name
                    )
                    issues.append(
                        {
                            "file_path": file_path,
                            "line_number": line_num,
                            "item_type": item_type,
                            "item_name": item_name,
                            "issue_type": issue_type,
                            "priority_score": priority_score,
                            "section": section,
                        }
                    )

    # Sort by priority score (highest first)
    issues.sort(key=lambda x: x["priority_score"], reverse=True)

    # Group by file and package
    by_file = defaultdict(list)
    by_package = defaultdict(list)

    for issue in issues:
        by_file[issue["file_path"]].append(issue)

        # Extract package name
        package_match = re.search(r"packages/([^/]+)/", issue["file_path"])
        if package_match:
            package = package_match.group(1)
            by_package[package].append(issue)

    return {
        "all_issues": issues,
        "by_file": dict(by_file),
        "by_package": dict(by_package),
        "top_files": sorted(
            by_file.items(),
            key=lambda x: sum(i["priority_score"] for i in x[1]),
            reverse=True,
        )[:20],
        "top_packages": sorted(
            by_package.items(),
            key=lambda x: sum(i["priority_score"] for i in x[1]),
            reverse=True,
        ),
    }


def generate_action_plan(analysis: Dict) -> str:
    """Generate a concrete action plan for fixing docstrings.

    Args:
        analysis: Analysis results from analyze_report()

    Returns:
        Action plan as a markdown string
    """
    lines = [
        "# AutoAPI Docstring Fix Action Plan",
        "",
        "Prioritized plan for fixing the most critical documentation issues for AutoAPI generation.",
        "",
        "## Strategy",
        "",
        "1. **Phase 1**: Fix highest-impact core modules (haive-core foundation)",
        "2. **Phase 2**: Fix main user-facing APIs (haive-agents)",
        "3. **Phase 3**: Complete remaining public APIs",
        "",
        "## Phase 1: Critical Core Infrastructure (haive-core)",
        "",
        "Focus on the foundation that all other packages depend on:",
        "",
    ]

    # Phase 1: Top haive-core issues
    core_issues = [
        issue
        for issue in analysis["all_issues"]
        if "haive-core" in issue["file_path"] and issue["priority_score"] >= 50
    ]

    if core_issues:
        lines.extend(["### Top Priority haive-core Issues", ""])

        # Group by file for better organization
        core_by_file = defaultdict(list)
        for issue in core_issues[:30]:  # Top 30 core issues
            core_by_file[issue["file_path"]].append(issue)

        for file_path, file_issues in sorted(
            core_by_file.items(),
            key=lambda x: sum(i["priority_score"] for i in x[1]),
            reverse=True,
        )[:10]:
            rel_path = os.path.relpath(file_path)
            total_score = sum(i["priority_score"] for i in file_issues)
            lines.append(f"#### {rel_path} (Priority: {total_score})")
            lines.append("")

            for issue in sorted(
                file_issues, key=lambda x: x["priority_score"], reverse=True
            )[:5]:
                lines.append(
                    f"- Line {issue['line_number']}: {issue['item_type']} `{issue['item_name']}` (score: {issue['priority_score']})"
                )

            if len(file_issues) > 5:
                lines.append(f"- ... and {len(file_issues) - 5} more issues")
            lines.append("")

    # Phase 2: Top haive-agents issues
    lines.extend(
        [
            "## Phase 2: Main User APIs (haive-agents)",
            "",
            "Focus on the main user-facing agent classes:",
            "",
        ]
    )

    agents_issues = [
        issue
        for issue in analysis["all_issues"]
        if "haive-agents" in issue["file_path"] and issue["priority_score"] >= 40
    ]

    if agents_issues:
        agents_by_file = defaultdict(list)
        for issue in agents_issues[:25]:  # Top 25 agent issues
            agents_by_file[issue["file_path"]].append(issue)

        for file_path, file_issues in sorted(
            agents_by_file.items(),
            key=lambda x: sum(i["priority_score"] for i in x[1]),
            reverse=True,
        )[:8]:
            rel_path = os.path.relpath(file_path)
            total_score = sum(i["priority_score"] for i in file_issues)
            lines.append(f"#### {rel_path} (Priority: {total_score})")
            lines.append("")

            for issue in sorted(
                file_issues, key=lambda x: x["priority_score"], reverse=True
            )[:5]:
                lines.append(
                    f"- Line {issue['line_number']}: {issue['item_type']} `{issue['item_name']}` (score: {issue['priority_score']})"
                )

            if len(file_issues) > 5:
                lines.append(f"- ... and {len(file_issues) - 5} more issues")
            lines.append("")

    # Package-level summary
    lines.extend(
        [
            "## Package Priority Summary",
            "",
            "Total issues by package (sorted by cumulative priority):",
            "",
        ]
    )

    for package, issues in analysis["top_packages"][:6]:
        total_score = sum(i["priority_score"] for i in issues)
        high_priority = len([i for i in issues if i["priority_score"] >= 50])
        lines.append(
            f"- **{package}**: {len(issues)} issues (total priority: {total_score}, high-priority: {high_priority})"
        )

    lines.extend(
        [
            "",
            "## Implementation Guidelines",
            "",
            "### Google-Style Docstring Template",
            "",
            "Use this template for all new docstrings:",
            "",
            "```python",
            "def example_function(param1: str, param2: int = 10) -> bool:",
            '    """One-line summary of what the function does.',
            "    ",
            "    Longer description explaining the purpose, algorithm,",
            "    or implementation details if needed.",
            "    ",
            "    Args:",
            "        param1: Description of param1 and its purpose.",
            "        param2: Description of param2 (default: 10).",
            "        ",
            "    Returns:",
            "        Description of what the function returns.",
            "        ",
            "    Raises:",
            "        ValueError: If param1 is empty.",
            "        TypeError: If param2 is not an integer.",
            "        ",
            "    Examples:",
            "        Basic usage::",
            "        ",
            '            result = example_function("hello", 20)',
            "            assert result is True",
            '    """',
            "```",
            "",
            "### Module Docstring Template",
            "",
            "```python",
            '"""Module for handling specific functionality.',
            "",
            "This module provides classes and functions for [specific purpose].",
            "It is designed to work with [related systems] and supports",
            "[key features].",
            "",
            "Key Classes:",
            "    MainClass: Primary interface for [functionality]",
            "    HelperClass: Utility class for [specific tasks]",
            "    ",
            "Key Functions:",
            "    main_function: Primary function for [purpose]",
            "    utility_function: Helper function for [specific task]",
            "    ",
            "Examples:",
            "    Basic usage::",
            "    ",
            "        from module import MainClass",
            "        instance = MainClass()",
            "        result = instance.main_method()",
            '"""',
            "```",
            "",
            "### Class Docstring Template",
            "",
            "```python",
            "class ExampleClass:",
            '    """One-line summary of the class purpose.',
            "    ",
            "    Detailed description of what the class does,",
            "    its role in the system, and key concepts.",
            "    ",
            "    Attributes:",
            "        attr1: Description of public attribute.",
            "        attr2: Description of another attribute.",
            "        ",
            "    Examples:",
            "        Basic usage::",
            "        ",
            '            instance = ExampleClass(param="value")',
            "            result = instance.method()",
            "            ",
            "    Note:",
            "        Any important notes about usage, thread-safety,",
            "        or integration with other components.",
            '    """',
            "```",
            "",
            "## Next Steps",
            "",
            "1. **Start with Phase 1** - Fix the top 10 haive-core files",
            "2. **Focus on modules first** - Module docstrings have highest AutoAPI impact",
            "3. **Then classes** - Class docstrings define the main API structure",
            "4. **Finally methods** - Complete the public method documentation",
            "5. **Test AutoAPI generation** - Verify docs build correctly after each phase",
            "",
            "Remember: AutoAPI depends heavily on module and class docstrings for navigation and structure!",
        ]
    )

    return "\n".join(lines)


def main():
    """Main function to analyze and prioritize docstring fixes."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Prioritize docstring fixes for AutoAPI"
    )
    parser.add_argument(
        "--report",
        default="project_docs/documentation_fix/MISSING_DOCSTRINGS_REPORT.md",
        help="Path to the docstring analysis report",
    )
    parser.add_argument(
        "--output",
        default="project_docs/documentation_fix/DOCSTRING_ACTION_PLAN.md",
        help="Output file for the action plan",
    )

    args = parser.parse_args()

    if not os.path.exists(args.report):
        print(f"Error: Report file not found: {args.report}")
        print("Run analyze_missing_docstrings.py first to generate the report.")
        return 1

    print(f"Analyzing report: {args.report}")
    analysis = analyze_report(args.report)

    print(f"Found {len(analysis['all_issues'])} prioritized issues")
    print(
        f"Top package: {analysis['top_packages'][0][0]} with {len(analysis['top_packages'][0][1])} issues"
    )

    action_plan = generate_action_plan(analysis)

    with open(args.output, "w") as f:
        f.write(action_plan)

    print(f"Action plan saved to: {args.output}")

    # Show top 5 immediate priorities
    print("\n=== TOP 5 IMMEDIATE PRIORITIES ===")
    for i, issue in enumerate(analysis["all_issues"][:5], 1):
        rel_path = os.path.relpath(issue["file_path"])
        print(
            f"{i}. {rel_path}:{issue['line_number']} - {issue['item_type']} `{issue['item_name']}` (priority: {issue['priority_score']})"
        )


if __name__ == "__main__":
    main()
