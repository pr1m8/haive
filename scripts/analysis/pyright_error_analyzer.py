#!/usr/bin/env python3
"""
Pyright Error Analyzer - Comprehensive error analysis and severity classification

This script analyzes pyright errors across the Haive codebase and categorizes them by:
- Error type and frequency
- Severity (will break at runtime vs compile-time only)
- Package distribution
- Import vs type vs other errors
- Suggested fix priority
"""

import json
import re
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


# Color codes for terminal output
class Colors:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


@dataclass
class ErrorInfo:
    """Information about a specific error"""

    file_path: str
    line: int
    column: int
    error_type: str
    message: str
    severity: str = "unknown"
    will_break_runtime: bool = False
    suggested_fix: str = ""
    category: str = "other"


@dataclass
class ErrorStats:
    """Statistics about errors"""

    total_errors: int = 0
    total_warnings: int = 0
    runtime_breaking: int = 0
    import_errors: int = 0
    type_errors: int = 0
    attribute_errors: int = 0
    other_errors: int = 0
    by_package: Dict[str, int] = field(default_factory=dict)
    by_severity: Dict[str, int] = field(default_factory=dict)
    by_type: Dict[str, int] = field(default_factory=dict)
    most_common_errors: List[Tuple[str, int]] = field(default_factory=list)


class PyrightErrorAnalyzer:
    """Analyzes pyright errors and categorizes them by severity and type"""

    # Error patterns that will definitely break at runtime
    RUNTIME_BREAKING_PATTERNS = [
        r"Cannot import.*Module.*not installed",
        r"No module named",
        r"Import.*could not be resolved",
        r"Cannot access member.*for type.*None",
        r"Object of type.*is not callable",
        r"Argument of type.*cannot be assigned to parameter",
        r"No overloads for.*match the provided arguments",
        r"Cannot instantiate abstract class",
        r"is not defined",
        r"has no attribute",
        r"Cannot access attribute.*for type.*None",
        r"Expected.*arguments? to.*but.*provided",
        r"Missing positional argument",
        r"takes.*positional argument.*but.*were given",
        r"Incompatible return value type",
        r"Cannot assign to.*because it is not a variable",
        r"Unsupported operand types",
        r"not subscriptable",
        r"object is not iterable",
        r"Cannot unpack.*values",
        r"Key.*not found in.*TypedDict",
        r"Required key.*missing from TypedDict",
    ]

    # Error patterns that are type-checking only (won't break at runtime)
    TYPE_ONLY_PATTERNS = [
        r"Type of.*is unknown",
        r"Type of.*is partially unknown",
        r"Could not infer type of",
        r"Type annotation.*is not defined",
        r"Expected type.*but received.*Unknown",
        r"Variable not allowed in type expression",
        r"Type parameter.*cannot be generic",
        r"TypeVar.*appears only once in generic function signature",
        r"Method.*is marked as overload",
        r"Overloaded implementation is not consistent with signature",
        r"Expression of type.*cannot be assigned to declared type",
        r"cannot be assigned to type.*Literal",
        r"Type.*is not assignable to type",
        r"Unnecessary.*type: ignore.*comment",
        r"is partially unknown",
    ]

    # Import-related patterns
    IMPORT_PATTERNS = [
        r"Import.*could not be resolved",
        r"No module named",
        r"Cannot import.*from",
        r"Attempted relative import beyond top-level package",
        r"Module.*has no exported member",
        r"Unknown import symbol",
    ]

    # Attribute access patterns
    ATTRIBUTE_PATTERNS = [
        r"Cannot access member",
        r"has no attribute",
        r"Attribute.*not found",
        r"No attribute.*on.*type",
        r"Cannot access attribute",
    ]

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.errors: List[ErrorInfo] = []
        self.stats = ErrorStats()

    def run_pyright(self, target_path: Optional[Path] = None) -> str:
        """Run pyright and capture output"""
        cmd = ["poetry", "run", "pyright"]
        if target_path:
            cmd.append(str(target_path))
        else:
            # Analyze all packages
            packages_dir = self.project_root / "packages"
            if packages_dir.exists():
                for package in packages_dir.iterdir():
                    if package.is_dir() and package.name.startswith("haive-"):
                        cmd.append(str(package))

        print(f"{Colors.CYAN}Running pyright analysis...{Colors.RESET}")
        print(f"Command: {' '.join(cmd)}")

        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, cwd=self.project_root
            )
            return result.stdout + result.stderr
        except Exception as e:
            print(f"{Colors.RED}Error running pyright: {e}{Colors.RESET}")
            return ""

    def parse_pyright_output(self, output: str):
        """Parse pyright output and extract error information"""
        lines = output.split("\n")

        # Pattern to match pyright error lines
        error_pattern = re.compile(
            r"^\s*(.+?):(\d+):(\d+)\s*-\s*(error|warning|information):\s*(.+?)(?:\s*\(.*?\))?$"
        )

        for line in lines:
            match = error_pattern.match(line)
            if match:
                file_path, line_num, col_num, level, message = match.groups()

                # Skip if not in a package
                if "packages/haive-" not in file_path:
                    continue

                error = ErrorInfo(
                    file_path=file_path,
                    line=int(line_num),
                    column=int(col_num),
                    error_type=level,
                    message=message.strip(),
                )

                # Categorize the error
                self._categorize_error(error)
                self.errors.append(error)

    def _categorize_error(self, error: ErrorInfo):
        """Categorize an error by type and severity"""
        message = error.message

        # Check if it's a runtime-breaking error
        for pattern in self.RUNTIME_BREAKING_PATTERNS:
            if re.search(pattern, message, re.IGNORECASE):
                error.will_break_runtime = True
                error.severity = "critical"
                break

        # Check if it's type-only
        if not error.will_break_runtime:
            for pattern in self.TYPE_ONLY_PATTERNS:
                if re.search(pattern, message, re.IGNORECASE):
                    error.severity = "type-only"
                    break

        # If still unknown, set medium severity
        if error.severity == "unknown":
            error.severity = "medium"

        # Categorize by type
        for pattern in self.IMPORT_PATTERNS:
            if re.search(pattern, message, re.IGNORECASE):
                error.category = "import"
                error.suggested_fix = "Check if module is installed or fix import path"
                return

        for pattern in self.ATTRIBUTE_PATTERNS:
            if re.search(pattern, message, re.IGNORECASE):
                error.category = "attribute"
                error.suggested_fix = "Check object type and available attributes"
                return

        if "type" in message.lower():
            error.category = "type"
            error.suggested_fix = "Fix type annotation or cast"
        else:
            error.category = "other"

    def calculate_stats(self):
        """Calculate statistics from parsed errors"""
        self.stats.total_errors = len(
            [e for e in self.errors if e.error_type == "error"]
        )
        self.stats.total_warnings = len(
            [e for e in self.errors if e.error_type == "warning"]
        )

        error_type_counts = defaultdict(int)

        for error in self.errors:
            if error.error_type != "error":
                continue

            # Count by category
            if error.category == "import":
                self.stats.import_errors += 1
            elif error.category == "type":
                self.stats.type_errors += 1
            elif error.category == "attribute":
                self.stats.attribute_errors += 1
            else:
                self.stats.other_errors += 1

            # Count runtime breaking
            if error.will_break_runtime:
                self.stats.runtime_breaking += 1

            # Count by package
            for package in [
                "haive-core",
                "haive-agents",
                "haive-tools",
                "haive-games",
                "haive-mcp",
                "haive-dataflow",
                "haive-prebuilt",
            ]:
                if package in error.file_path:
                    self.stats.by_package[package] = (
                        self.stats.by_package.get(package, 0) + 1
                    )
                    break

            # Count by severity
            self.stats.by_severity[error.severity] = (
                self.stats.by_severity.get(error.severity, 0) + 1
            )

            # Count specific error messages
            # Normalize the message to group similar errors
            normalized_msg = re.sub(r'"[^"]*"', '""', error.message)
            normalized_msg = re.sub(r"'[^']*'", "''", normalized_msg)
            normalized_msg = re.sub(r"\b\d+\b", "N", normalized_msg)
            error_type_counts[normalized_msg] += 1

        # Get most common errors
        self.stats.most_common_errors = sorted(
            error_type_counts.items(), key=lambda x: x[1], reverse=True
        )[:20]

    def generate_report(self, output_dir: Path):
        """Generate comprehensive error report"""
        output_dir.mkdir(parents=True, exist_ok=True)

        # Generate summary report
        summary_path = output_dir / "error_analysis_summary.md"
        with open(summary_path, "w") as f:
            f.write(self._generate_summary_markdown())

        # Generate detailed report
        detailed_path = output_dir / "error_analysis_detailed.json"
        with open(detailed_path, "w") as f:
            json.dump(
                {
                    "metadata": {
                        "timestamp": datetime.now().isoformat(),
                        "total_files_analyzed": len(
                            set(e.file_path for e in self.errors)
                        ),
                        "project_root": str(self.project_root),
                    },
                    "stats": {
                        "total_errors": self.stats.total_errors,
                        "total_warnings": self.stats.total_warnings,
                        "runtime_breaking": self.stats.runtime_breaking,
                        "by_category": {
                            "import": self.stats.import_errors,
                            "type": self.stats.type_errors,
                            "attribute": self.stats.attribute_errors,
                            "other": self.stats.other_errors,
                        },
                        "by_package": self.stats.by_package,
                        "by_severity": self.stats.by_severity,
                    },
                    "errors": [
                        {
                            "file": e.file_path,
                            "line": e.line,
                            "column": e.column,
                            "type": e.error_type,
                            "message": e.message,
                            "severity": e.severity,
                            "will_break_runtime": e.will_break_runtime,
                            "category": e.category,
                            "suggested_fix": e.suggested_fix,
                        }
                        for e in self.errors
                        if e.error_type == "error"
                    ],
                },
                f,
                indent=2,
            )

        # Generate priority fix list
        priority_path = output_dir / "priority_fixes.md"
        with open(priority_path, "w") as f:
            f.write(self._generate_priority_fixes())

        print(f"\n{Colors.GREEN}Reports generated in {output_dir}{Colors.RESET}")
        print(f"  - Summary: {summary_path}")
        print(f"  - Detailed: {detailed_path}")
        print(f"  - Priority fixes: {priority_path}")

    def _generate_summary_markdown(self) -> str:
        """Generate markdown summary report"""
        total = self.stats.total_errors
        runtime_pct = (self.stats.runtime_breaking / total * 100) if total > 0 else 0

        report = f"""# Pyright Error Analysis Report

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Executive Summary

- **Total Errors**: {self.stats.total_errors:,}
- **Total Warnings**: {self.stats.total_warnings:,}
- **Runtime Breaking Errors**: {self.stats.runtime_breaking:,} ({runtime_pct:.1f}%)
- **Files with Errors**: {len(set(e.file_path for e in self.errors)):,}

## Severity Breakdown

| Severity | Count | Percentage | Description |
|----------|-------|------------|-------------|
| Critical | {self.stats.by_severity.get("critical", 0):,} | {self.stats.by_severity.get("critical", 0) / total * 100:.1f}% | Will break at runtime |
| Medium | {self.stats.by_severity.get("medium", 0):,} | {self.stats.by_severity.get("medium", 0) / total * 100:.1f}% | May cause runtime issues |
| Type-only | {self.stats.by_severity.get("type-only", 0):,} | {self.stats.by_severity.get("type-only", 0) / total * 100:.1f}% | Type checking only |

## Error Categories

| Category | Count | Percentage | Typical Fix |
|----------|-------|------------|-------------|
| Import | {self.stats.import_errors:,} | {self.stats.import_errors / total * 100:.1f}% | Fix import paths or install packages |
| Type | {self.stats.type_errors:,} | {self.stats.type_errors / total * 100:.1f}% | Fix type annotations |
| Attribute | {self.stats.attribute_errors:,} | {self.stats.attribute_errors / total * 100:.1f}% | Check object types |
| Other | {self.stats.other_errors:,} | {self.stats.other_errors / total * 100:.1f}% | Various fixes needed |

## Package Distribution

| Package | Errors | Percentage |
|---------|--------|------------|
"""
        for package, count in sorted(
            self.stats.by_package.items(), key=lambda x: x[1], reverse=True
        ):
            report += f"| {package} | {count:,} | {count / total * 100:.1f}% |\n"

        report += f"""
## Most Common Error Types

| Error Pattern | Occurrences |
|---------------|-------------|
"""
        for error_msg, count in self.stats.most_common_errors[:15]:
            # Truncate long messages
            if len(error_msg) > 80:
                error_msg = error_msg[:77] + "..."
            report += f"| {error_msg} | {count:,} |\n"

        return report

    def _generate_priority_fixes(self) -> str:
        """Generate priority fix recommendations"""
        # Group errors by file and severity
        file_errors = defaultdict(list)
        for error in self.errors:
            if error.error_type == "error" and error.severity == "critical":
                file_errors[error.file_path].append(error)

        # Sort files by number of critical errors
        sorted_files = sorted(
            file_errors.items(), key=lambda x: len(x[1]), reverse=True
        )

        report = """# Priority Fix Recommendations

Fix these files first - they contain runtime-breaking errors:

## Critical Files (Top 20)

"""
        for i, (file_path, errors) in enumerate(sorted_files[:20]):
            report += (
                f"\n### {i + 1}. `{file_path}` ({len(errors)} critical errors)\n\n"
            )

            # Group similar errors
            error_groups = defaultdict(list)
            for error in errors[:5]:  # Show first 5 errors
                error_groups[error.category].append(error)

            for category, group_errors in error_groups.items():
                report += f"**{category.title()} Errors:**\n"
                for error in group_errors[:3]:
                    report += f"- Line {error.line}: {error.message}\n"
                    if error.suggested_fix:
                        report += f"  - *Fix*: {error.suggested_fix}\n"
                report += "\n"

        # Add quick wins section
        report += """
## Quick Wins

These patterns appear frequently and can be fixed systematically:

"""
        # Find most common fixable patterns
        common_fixes = defaultdict(int)
        for error in self.errors:
            if error.error_type == "error" and error.category == "import":
                if "Optional" in error.message:
                    common_fixes["Add `from typing import Optional`"] += 1
                elif "Any" in error.message:
                    common_fixes["Add `from typing import Any`"] += 1
                elif "Dict" in error.message:
                    common_fixes["Add `from typing import Dict`"] += 1
                elif "List" in error.message:
                    common_fixes["Add `from typing import List`"] += 1
                elif "Field" in error.message and "pydantic" in error.message.lower():
                    common_fixes["Add `from pydantic import Field`"] += 1

        for fix, count in sorted(
            common_fixes.items(), key=lambda x: x[1], reverse=True
        )[:10]:
            report += f"- {fix} ({count} occurrences)\n"

        return report

    def print_summary(self):
        """Print colored summary to console"""
        print(
            f"\n{Colors.BOLD}{Colors.CYAN}=== Pyright Error Analysis Summary ==={Colors.RESET}\n"
        )

        print(f"{Colors.YELLOW}Total Errors:{Colors.RESET} {self.stats.total_errors:,}")
        print(
            f"{Colors.YELLOW}Total Warnings:{Colors.RESET} {self.stats.total_warnings:,}"
        )

        if self.stats.runtime_breaking > 0:
            print(
                f"\n{Colors.RED}⚠️  Runtime Breaking Errors: {self.stats.runtime_breaking:,}{Colors.RESET}"
            )
            print(f"   These errors WILL cause crashes when the code runs!")

        print(f"\n{Colors.CYAN}Error Categories:{Colors.RESET}")
        print(f"  Import errors: {self.stats.import_errors:,}")
        print(f"  Type errors: {self.stats.type_errors:,}")
        print(f"  Attribute errors: {self.stats.attribute_errors:,}")
        print(f"  Other errors: {self.stats.other_errors:,}")

        print(f"\n{Colors.CYAN}Top 5 Packages with Errors:{Colors.RESET}")
        for package, count in sorted(
            self.stats.by_package.items(), key=lambda x: x[1], reverse=True
        )[:5]:
            bar = "█" * int(count / max(self.stats.by_package.values()) * 30)
            print(f"  {package:<20} {bar} {count:,}")

        print(
            f"\n{Colors.CYAN}Most Common Error (appears {self.stats.most_common_errors[0][1]} times):{Colors.RESET}"
        )
        print(f"  {self.stats.most_common_errors[0][0][:80]}...")


def main():
    """Main entry point"""
    project_root = Path(__file__).parent.parent.parent
    analyzer = PyrightErrorAnalyzer(project_root)

    # Run pyright
    output = analyzer.run_pyright()

    if not output:
        print(
            f"{Colors.RED}No output from pyright. Make sure pyright is installed.{Colors.RESET}"
        )
        sys.exit(1)

    # Parse output
    analyzer.parse_pyright_output(output)

    # Calculate statistics
    analyzer.calculate_stats()

    # Print summary
    analyzer.print_summary()

    # Generate reports
    report_dir = (
        project_root / "error_reports" / datetime.now().strftime("%Y%m%d_%H%M%S")
    )
    analyzer.generate_report(report_dir)


if __name__ == "__main__":
    main()
