#!/usr/bin/env python3
"""Extract and categorize all import errors from documentation build logs."""

import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Set


def extract_import_errors_from_log(log_file: str) -> Dict[str, List[str]]:
    """Extract all import errors from the build log."""

    # Read the log file
    try:
        with open(log_file, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ Log file not found: {log_file}")
        return {}

    # Patterns to match import errors
    patterns = {
        "ModuleNotFoundError": r'ModuleNotFoundError - No module named [\'"]([^\'"]+)[\'"]',
        "ImportError": r'ImportError - cannot import name [\'"]([^\'"]+)[\'"] from [\'"]([^\'"]+)[\'"]',
        "TypeError_Generic": r"TypeError.*Generic.*you should inherit from typing\.Generic",
        "TypeError_MRO": r"TypeError - Cannot create a consistent method resolution order",
        "TypeError_Abstract": r"TypeError - Can\'t instantiate abstract class (\w+)",
        "NameError": r'NameError - name [\'"]([^\'"]+)[\'"] is not defined',
        "AttributeError": r'AttributeError.*has no attribute [\'"]([^\'"]+)[\'"]',
    }

    errors_by_type = defaultdict(set)
    errors_by_module = defaultdict(list)

    # Split content into lines and process
    lines = content.split("\n")
    current_module = None

    for line in lines:
        # Extract module name from WARNING lines
        module_match = re.search(r"WARNING\s+❌\s+([^:]+):", line)
        if module_match:
            current_module = module_match.group(1).strip()
            continue

        # Match error patterns
        for error_type, pattern in patterns.items():
            matches = re.findall(pattern, line)
            if matches:
                if error_type == "ModuleNotFoundError":
                    for missing_module in matches:
                        errors_by_type[error_type].add(missing_module)
                        if current_module:
                            errors_by_module[current_module].append(
                                f"{error_type}: {missing_module}"
                            )

                elif error_type == "ImportError":
                    for missing_name, from_module in matches:
                        error_desc = (
                            f"cannot import '{missing_name}' from '{from_module}'"
                        )
                        errors_by_type[error_type].add(error_desc)
                        if current_module:
                            errors_by_module[current_module].append(
                                f"{error_type}: {error_desc}"
                            )

                elif error_type == "TypeError_Abstract":
                    for class_name in matches:
                        errors_by_type[error_type].add(class_name)
                        if current_module:
                            errors_by_module[current_module].append(
                                f"{error_type}: {class_name}"
                            )

                elif error_type == "NameError":
                    for undefined_name in matches:
                        errors_by_type[error_type].add(undefined_name)
                        if current_module:
                            errors_by_module[current_module].append(
                                f"{error_type}: {undefined_name}"
                            )

                else:  # Generic error types
                    errors_by_type[error_type].add(line.strip())
                    if current_module:
                        errors_by_module[current_module].append(
                            f"{error_type}: {line.strip()}"
                        )

    return {
        "errors_by_type": dict(errors_by_type),
        "errors_by_module": dict(errors_by_module),
    }


def categorize_errors(errors_by_type: Dict[str, Set[str]]) -> Dict[str, List[str]]:
    """Categorize errors by their likely fix approach."""

    categories = {
        "missing_modules_core": [],
        "missing_modules_dataflow": [],
        "missing_modules_games": [],
        "missing_imports_from_existing": [],
        "abstract_class_instantiation": [],
        "generic_type_issues": [],
        "undefined_names": [],
        "circular_imports": [],
        "other": [],
    }

    # Categorize ModuleNotFoundError
    if "ModuleNotFoundError" in errors_by_type:
        for module in errors_by_type["ModuleNotFoundError"]:
            if module.startswith("haive.core"):
                categories["missing_modules_core"].append(module)
            elif module.startswith("haive.dataflow"):
                categories["missing_modules_dataflow"].append(module)
            elif module.startswith("haive.games"):
                categories["missing_modules_games"].append(module)
            elif any(x in module for x in ["game", "api", "auth", "db"]):
                categories["missing_modules_dataflow"].append(module)
            else:
                categories["missing_modules_core"].append(module)

    # Categorize ImportError
    if "ImportError" in errors_by_type:
        for error in errors_by_type["ImportError"]:
            if "partially initialized module" in error:
                categories["circular_imports"].append(error)
            else:
                categories["missing_imports_from_existing"].append(error)

    # Other categories
    if "TypeError_Abstract" in errors_by_type:
        categories["abstract_class_instantiation"].extend(
            errors_by_type["TypeError_Abstract"]
        )

    if "TypeError_Generic" in errors_by_type:
        categories["generic_type_issues"].extend(errors_by_type["TypeError_Generic"])

    if "NameError" in errors_by_type:
        categories["undefined_names"].extend(errors_by_type["NameError"])

    # Clean up empty categories
    return {k: v for k, v in categories.items() if v}


def generate_report(log_file: str, output_file: str = None):
    """Generate comprehensive import error report."""

    print(f"🔍 Extracting import errors from: {log_file}")

    # Extract errors
    error_data = extract_import_errors_from_log(log_file)
    if not error_data:
        return

    errors_by_type = error_data["errors_by_type"]
    errors_by_module = error_data["errors_by_module"]

    # Categorize errors
    categories = categorize_errors(errors_by_type)

    # Generate report
    report_lines = [
        "# Comprehensive Import Error Analysis",
        "",
        f"**Source**: {log_file}",
        f"**Generated**: {Path(__file__).name}",
        "",
        "## Summary",
        "",
    ]

    # Summary statistics
    total_modules_with_errors = len(errors_by_module)
    total_unique_errors = sum(len(errors) for errors in errors_by_type.values())

    report_lines.extend(
        [
            f"- **Total modules with errors**: {total_modules_with_errors}",
            f"- **Total unique error types**: {len(errors_by_type)}",
            f"- **Total unique errors**: {total_unique_errors}",
            "",
        ]
    )

    # Error breakdown by type
    report_lines.extend(
        [
            "## Error Breakdown by Type",
            "",
        ]
    )

    for error_type, errors in errors_by_type.items():
        report_lines.extend(
            [
                f"### {error_type} ({len(errors)} unique)",
                "",
            ]
        )
        for error in sorted(errors):
            report_lines.append(f"- `{error}`")
        report_lines.append("")

    # Categorized fixes
    report_lines.extend(
        [
            "## Categorized Fix Strategies",
            "",
        ]
    )

    fix_strategies = {
        "missing_modules_core": "Add to autodoc_mock_imports or fix module structure",
        "missing_modules_dataflow": "Add to autoapi_ignore (dataflow is experimental)",
        "missing_modules_games": "Add to autodoc_mock_imports or fix imports",
        "missing_imports_from_existing": "Fix __init__.py exports or create missing functions",
        "abstract_class_instantiation": "Add to autoapi_ignore (can't be instantiated)",
        "generic_type_issues": "Fix Generic[T] usage or add to mock imports",
        "undefined_names": "Add missing imports or mock the names",
        "circular_imports": "Restructure imports or add to autoapi_ignore",
    }

    for category, errors in categories.items():
        if errors:
            strategy = fix_strategies.get(category, "Manual investigation needed")
            report_lines.extend(
                [
                    f"### {category.replace('_', ' ').title()} ({len(errors)} items)",
                    f"**Strategy**: {strategy}",
                    "",
                ]
            )
            for error in sorted(errors)[:20]:  # Limit to first 20
                report_lines.append(f"- `{error}`")
            if len(errors) > 20:
                report_lines.append(f"- ... and {len(errors) - 20} more")
            report_lines.append("")

    # Top problematic modules
    if errors_by_module:
        sorted_modules = sorted(
            errors_by_module.items(), key=lambda x: len(x[1]), reverse=True
        )
        report_lines.extend(
            [
                "## Top Problematic Modules",
                "",
            ]
        )

        for module, errors in sorted_modules[:15]:  # Top 15
            report_lines.extend(
                [
                    f"### {module} ({len(errors)} errors)",
                    "",
                ]
            )
            for error in errors[:5]:  # First 5 errors per module
                report_lines.append(f"- {error}")
            if len(errors) > 5:
                report_lines.append(f"- ... and {len(errors) - 5} more")
            report_lines.append("")

    # Generate actionable fixes
    report_lines.extend(
        [
            "## Immediate Action Items",
            "",
            "### 1. Add to autoapi_ignore (experimental/broken modules)",
            "```python",
        ]
    )

    # Suggest modules to ignore
    ignore_candidates = []
    if "missing_modules_dataflow" in categories:
        ignore_candidates.extend([f'"**/dataflow/**/*.py"'])
    if "abstract_class_instantiation" in categories:
        ignore_candidates.extend(
            [f'"**/configurable_config.py"', f'"**/generic_engines.py"']
        )

    for candidate in ignore_candidates[:10]:
        report_lines.append(f"    {candidate},")

    report_lines.extend(
        [
            "```",
            "",
            "### 2. Add to autodoc_mock_imports",
            "```python",
        ]
    )

    # Suggest mock imports
    mock_candidates = set()
    if "missing_modules_core" in categories:
        mock_candidates.update(categories["missing_modules_core"][:15])
    if "undefined_names" in categories:
        mock_candidates.update(categories["undefined_names"][:10])

    for candidate in sorted(mock_candidates):
        report_lines.append(f'    "{candidate}",')

    report_lines.extend(
        [
            "```",
            "",
            "### 3. Fix Missing Exports",
            "",
        ]
    )

    if "missing_imports_from_existing" in categories:
        for error in categories["missing_imports_from_existing"][:10]:
            if "cannot import" in error:
                parts = error.split("'")
                if len(parts) >= 4:
                    missing_name = parts[1]
                    from_module = parts[3]
                    report_lines.append(
                        f"- Add `{missing_name}` to `{from_module}/__init__.py`"
                    )

    # Write report
    report_content = "\n".join(report_lines)

    if output_file:
        with open(output_file, "w") as f:
            f.write(report_content)
        print(f"📝 Report written to: {output_file}")
    else:
        print(report_content)

    return categories, errors_by_module


if __name__ == "__main__":
    # Use the most recent log file or accept from command line
    log_file = "/tmp/docs_build_verification.log"
    if len(sys.argv) > 1:
        log_file = sys.argv[1]

    output_file = (
        "/home/will/Projects/haive/backend/haive/comprehensive_import_error_analysis.md"
    )

    generate_report(log_file, output_file)
