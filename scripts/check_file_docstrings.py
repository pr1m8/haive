#!/usr/bin/env python3
"""Check specific files for docstring completeness and provide recommendations.

This script analyzes individual files and provides targeted feedback
on what needs to be documented for AutoAPI compatibility.
"""

import ast
import os
import sys
from typing import Any, Dict, List

from analyze_missing_docstrings import DocstringAnalyzer


def analyze_file_detailed(file_path: str) -> Dict[str, Any]:
    """Analyze a single file in detail and provide recommendations.

    Args:
        file_path: Path to the Python file to analyze.

    Returns:
        Dictionary with detailed analysis and recommendations.
    """
    if not os.path.exists(file_path):
        return {"error": f"File not found: {file_path}"}

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source_code = f.read()
    except Exception as e:
        return {"error": f"Could not read file: {e}"}

    try:
        tree = ast.parse(source_code)
    except SyntaxError as e:
        return {"error": f"Syntax error in file: {e}"}

    analyzer = DocstringAnalyzer(file_path, source_code)
    issues = analyzer.analyze()

    # Categorize issues
    categorized = {
        "module_issues": [],
        "class_issues": [],
        "function_issues": [],
        "method_issues": [],
        "missing_count": 0,
        "incomplete_count": 0,
        "total_issues": len(issues),
    }

    for issue in issues:
        categorized[f"{issue.item_type}_issues"].append(issue)
        if issue.issue_type == "missing":
            categorized["missing_count"] += 1
        elif issue.issue_type == "incomplete":
            categorized["incomplete_count"] += 1

    # Get file stats
    stats = {
        "total_lines": len(source_code.split("\n")),
        "has_module_docstring": ast.get_docstring(tree) is not None,
        "classes_count": len(
            [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
        ),
        "functions_count": len(
            [
                n
                for n in ast.walk(tree)
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
            ]
        ),
    }

    return {
        "file_path": file_path,
        "stats": stats,
        "issues": categorized,
        "recommendations": generate_file_recommendations(file_path, categorized, stats),
    }


def generate_file_recommendations(
    file_path: str, issues: Dict, stats: Dict
) -> List[str]:
    """Generate specific recommendations for a file.

    Args:
        file_path: Path to the file.
        issues: Categorized issues.
        stats: File statistics.

    Returns:
        List of recommendation strings.
    """
    recommendations = []

    # Module docstring
    if issues["module_issues"]:
        recommendations.append("🔥 HIGH PRIORITY: Add module docstring")
        recommendations.append(
            "   - Module docstrings are critical for AutoAPI navigation"
        )
        recommendations.append(
            "   - Should describe the module's purpose and key classes/functions"
        )
        recommendations.append("   - Use Google-style format with Examples section")

    # Class docstrings
    if issues["class_issues"]:
        missing_classes = [
            i for i in issues["class_issues"] if i.issue_type == "missing"
        ]
        incomplete_classes = [
            i for i in issues["class_issues"] if i.issue_type == "incomplete"
        ]

        if missing_classes:
            recommendations.append(
                f"🔥 HIGH PRIORITY: Add docstrings to {len(missing_classes)} classes"
            )
            for issue in missing_classes[:3]:  # Show first 3
                recommendations.append(
                    f"   - Class `{issue.item_name}` (line {issue.line_number})"
                )

        if incomplete_classes:
            recommendations.append(
                f"⚠️  MEDIUM PRIORITY: Complete {len(incomplete_classes)} class docstrings"
            )
            for issue in incomplete_classes[:3]:
                recommendations.append(
                    f"   - Class `{issue.item_name}`: {', '.join(issue.details)}"
                )

    # Function/method docstrings
    missing_functions = [
        i for i in issues["function_issues"] if i.issue_type == "missing"
    ]
    missing_methods = [i for i in issues["method_issues"] if i.issue_type == "missing"]

    if missing_functions:
        recommendations.append(
            f"📝 MEDIUM PRIORITY: Add docstrings to {len(missing_functions)} functions"
        )
        public_functions = [i for i in missing_functions if i.is_public]
        if public_functions:
            recommendations.append(
                f"   - {len(public_functions)} are public functions (higher priority)"
            )

    if missing_methods:
        recommendations.append(
            f"📝 MEDIUM PRIORITY: Add docstrings to {len(missing_methods)} methods"
        )
        public_methods = [i for i in missing_methods if i.is_public]
        init_methods = [i for i in missing_methods if i.item_name == "__init__"]
        if public_methods:
            recommendations.append(f"   - {len(public_methods)} are public methods")
        if init_methods:
            recommendations.append(
                f"   - {len(init_methods)} are __init__ methods (important for AutoAPI)"
            )

    # File-specific guidance
    if "base" in file_path or "core" in file_path:
        recommendations.append("🎯 This is a core/base file - prioritize completeness")

    if any(
        name in os.path.basename(file_path)
        for name in ["agent", "config", "schema", "state"]
    ):
        recommendations.append(
            "🎯 This file contains key API classes - high AutoAPI impact"
        )

    if stats["classes_count"] == 0 and stats["functions_count"] > 0:
        recommendations.append(
            "💡 Utility module - focus on function docstrings and clear module overview"
        )

    if not recommendations:
        recommendations.append("✅ This file has good docstring coverage!")

    return recommendations


def print_file_analysis(analysis: Dict[str, Any]) -> None:
    """Print a detailed analysis of a file's docstring status.

    Args:
        analysis: Analysis results from analyze_file_detailed().
    """
    if "error" in analysis:
        print(f"❌ Error: {analysis['error']}")
        return

    file_path = analysis["file_path"]
    stats = analysis["stats"]
    issues = analysis["issues"]

    print(f"📁 File: {os.path.relpath(file_path)}")
    print(
        f"📊 Stats: {stats['total_lines']} lines, {stats['classes_count']} classes, {stats['functions_count']} functions"
    )
    print(
        f"📈 Issues: {issues['total_issues']} total ({issues['missing_count']} missing, {issues['incomplete_count']} incomplete)"
    )
    print()

    # Show issue breakdown
    if issues["module_issues"]:
        print(f"🏗️  Module: {len(issues['module_issues'])} issues")
    if issues["class_issues"]:
        print(f"🏛️  Classes: {len(issues['class_issues'])} issues")
    if issues["function_issues"]:
        print(f"⚙️  Functions: {len(issues['function_issues'])} issues")
    if issues["method_issues"]:
        print(f"🔧 Methods: {len(issues['method_issues'])} issues")

    print()
    print("📋 RECOMMENDATIONS:")
    for i, rec in enumerate(analysis["recommendations"], 1):
        print(f"{i:2d}. {rec}")

    print()


def main():
    """Main function to check specific files."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Check specific files for docstring issues"
    )
    parser.add_argument("files", nargs="+", help="Python files to analyze")
    parser.add_argument(
        "--summary", action="store_true", help="Show only summary statistics"
    )

    args = parser.parse_args()

    total_issues = 0
    total_files = len(args.files)

    for i, file_path in enumerate(args.files, 1):
        if total_files > 1:
            print(f"{'='*60}")
            print(f"FILE {i}/{total_files}")
            print(f"{'='*60}")

        analysis = analyze_file_detailed(file_path)

        if args.summary:
            if "error" in analysis:
                print(f"❌ {file_path}: {analysis['error']}")
            else:
                issues_count = analysis["issues"]["total_issues"]
                missing_count = analysis["issues"]["missing_count"]
                print(
                    f"📁 {os.path.relpath(file_path)}: {issues_count} issues ({missing_count} missing)"
                )
                total_issues += issues_count
        else:
            print_file_analysis(analysis)
            if "issues" in analysis:
                total_issues += analysis["issues"]["total_issues"]

        if i < total_files:
            print()

    if total_files > 1:
        print(f"{'='*60}")
        print(f"SUMMARY: {total_issues} total issues across {total_files} files")


if __name__ == "__main__":
    main()
