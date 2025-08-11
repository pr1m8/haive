#!/usr/bin/env python3
"""Documentation Audit Script.

Finds all Python files with suboptimal or missing documentation.
Checks for:
- Missing module docstrings
- Missing class docstrings
- Missing method/function docstrings
- Missing type hints
- Poor docstring quality
- Missing __all__ exports
- Incomplete docstrings (no Args, Returns, etc.)
"""

import ast
import json
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class DocIssue:
    """Documentation issue found in code."""

    file_path: str
    line_number: int
    issue_type: str
    severity: str  # "critical", "high", "medium", "low"
    message: str
    context: str = ""


@dataclass
class FileReport:
    """Report for a single file."""

    file_path: str
    total_issues: int = 0
    critical_issues: int = 0
    high_issues: int = 0
    medium_issues: int = 0
    low_issues: int = 0
    issues: list[DocIssue] = field(default_factory=list)

    def add_issue(self, issue: DocIssue):
        """Add an issue to the report."""
        self.issues.append(issue)
        self.total_issues += 1
        if issue.severity == "critical":
            self.critical_issues += 1
        elif issue.severity == "high":
            self.high_issues += 1
        elif issue.severity == "medium":
            self.medium_issues += 1
        elif issue.severity == "low":
            self.low_issues += 1


class DocstringAnalyzer(ast.NodeVisitor):
    """Analyzes Python AST for documentation issues."""

    def __init__(self, file_path: str, source_code: str):
        self.file_path = file_path
        self.source_lines = source_code.splitlines()
        self.issues: list[DocIssue] = []
        self.current_class = None
        self.has_module_docstring = False
        self.module_exports: set[str] = set()
        self.defined_names: set[str] = set()

    def visit_Module(self, node: ast.Module) -> None:
        """Check module-level documentation."""
        # Check for module docstring
        if ast.get_docstring(node):
            self.has_module_docstring = True
            docstring = ast.get_docstring(node)
            self._check_module_docstring_quality(docstring, node)
        else:
            self.issues.append(
                DocIssue(
                    file_path=self.file_path,
                    line_number=1,
                    issue_type="missing_module_docstring",
                    severity="high",
                    message="Module has no docstring",
                    context="Add module-level docstring with description and examples",
                )
            )

        # Check for __all__ definition
        self._check_module_exports(node)

        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Check class documentation."""
        self.defined_names.add(node.name)
        self.current_class = node.name

        # Skip test classes
        if node.name.startswith("Test") or node.name.endswith("Test"):
            self.current_class = None
            return

        docstring = ast.get_docstring(node)
        if not docstring:
            self.issues.append(
                DocIssue(
                    file_path=self.file_path,
                    line_number=node.lineno,
                    issue_type="missing_class_docstring",
                    severity="high",
                    message=f"Class '{node.name}' has no docstring",
                    context=f"class {node.name}",
                )
            )
        else:
            self._check_class_docstring_quality(docstring, node)

        # Check __init__ method specifically
        for item in node.body:
            if isinstance(item, ast.FunctionDef) and item.name == "__init__":
                self._check_init_method(item, node.name)

        self.generic_visit(node)
        self.current_class = None

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Check function/method documentation."""
        self.defined_names.add(node.name)

        # Skip private/test functions
        if node.name.startswith("_") and not node.name.startswith("__"):
            return
        if node.name.startswith("test_"):
            return

        # Check for docstring
        docstring = ast.get_docstring(node)
        if not docstring:
            severity = "high" if not node.name.startswith("_") else "medium"
            context = f"class {self.current_class}" if self.current_class else "module-level"
            self.issues.append(
                DocIssue(
                    file_path=self.file_path,
                    line_number=node.lineno,
                    issue_type="missing_function_docstring",
                    severity=severity,
                    message=f"Function '{node.name}' has no docstring",
                    context=context,
                )
            )
        else:
            self._check_function_docstring_quality(docstring, node)

        # Check for type hints
        self._check_type_hints(node)

        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        """Check async function documentation."""
        # Treat async functions the same as regular functions
        self.visit_FunctionDef(node)

    def _check_module_docstring_quality(self, docstring: str, node: ast.Module) -> None:
        """Check quality of module docstring."""
        lines = docstring.strip().splitlines()

        # Check for single-line summary
        if len(lines) < 1 or len(lines[0]) > 79:
            self.issues.append(
                DocIssue(
                    file_path=self.file_path,
                    line_number=1,
                    issue_type="poor_module_docstring",
                    severity="medium",
                    message="Module docstring should start with single-line summary (<79 chars)",
                    context="First line of docstring",
                )
            )

        # Check for key sections
        docstring_lower = docstring.lower()
        if "example" not in docstring_lower and "usage" not in docstring_lower:
            self.issues.append(
                DocIssue(
                    file_path=self.file_path,
                    line_number=1,
                    issue_type="missing_examples",
                    severity="medium",
                    message="Module docstring should include usage examples",
                    context="Add 'Example:' or 'Usage:' section",
                )
            )

    def _check_class_docstring_quality(self, docstring: str, node: ast.ClassDef) -> None:
        """Check quality of class docstring."""
        lines = docstring.strip().splitlines()

        # Check for single-line summary
        if len(lines) < 1 or len(lines[0]) > 79:
            self.issues.append(
                DocIssue(
                    file_path=self.file_path,
                    line_number=node.lineno,
                    issue_type="poor_class_docstring",
                    severity="medium",
                    message=f"Class '{node.name}' docstring should start with single-line summary",
                    context=f"class {node.name}",
                )
            )

        # Check for Args/Attributes sections
        docstring_lower = docstring.lower()
        has_init = any(isinstance(n, ast.FunctionDef) and n.name == "__init__" for n in node.body)

        if has_init and "args:" not in docstring_lower and "parameters:" not in docstring_lower:
            self.issues.append(
                DocIssue(
                    file_path=self.file_path,
                    line_number=node.lineno,
                    issue_type="missing_args_section",
                    severity="high",
                    message=f"Class '{node.name}' docstring missing Args section",
                    context="Add 'Args:' section for __init__ parameters",
                )
            )

        if "attributes:" not in docstring_lower and "attribute:" not in docstring_lower:
            # Check if class has any attributes
            has_attributes = any(isinstance(n, ast.AnnAssign) for n in node.body)
            if has_attributes:
                self.issues.append(
                    DocIssue(
                        file_path=self.file_path,
                        line_number=node.lineno,
                        issue_type="missing_attributes_section",
                        severity="medium",
                        message=f"Class '{node.name}' docstring missing Attributes section",
                        context="Add 'Attributes:' section",
                    )
                )

    def _check_function_docstring_quality(self, docstring: str, node: ast.FunctionDef) -> None:
        """Check quality of function docstring."""
        lines = docstring.strip().splitlines()

        # Check for single-line summary
        if len(lines) < 1:
            return

        if len(lines[0]) > 79:
            self.issues.append(
                DocIssue(
                    file_path=self.file_path,
                    line_number=node.lineno,
                    issue_type="poor_function_docstring",
                    severity="low",
                    message=f"Function '{node.name}' docstring summary too long (>79 chars)",
                    context=f"def {node.name}",
                )
            )

        docstring_lower = docstring.lower()

        # Check for Args section if function has parameters
        if node.args.args or node.args.kwonlyargs:
            if "args:" not in docstring_lower and "parameters:" not in docstring_lower:
                # Skip if only 'self' parameter
                param_names = [arg.arg for arg in node.args.args]
                if param_names != ["self"]:
                    self.issues.append(
                        DocIssue(
                            file_path=self.file_path,
                            line_number=node.lineno,
                            issue_type="missing_args_documentation",
                            severity="high",
                            message=f"Function '{node.name}' missing Args documentation",
                            context=f"Parameters: {', '.join(param_names)}",
                        )
                    )

        # Check for Returns section if function has return annotation or returns
        has_return = any(isinstance(n, ast.Return) and n.value for n in ast.walk(node))
        if has_return or node.returns:
            if "returns:" not in docstring_lower and "return:" not in docstring_lower:
                self.issues.append(
                    DocIssue(
                        file_path=self.file_path,
                        line_number=node.lineno,
                        issue_type="missing_returns_documentation",
                        severity="high",
                        message=f"Function '{node.name}' missing Returns documentation",
                        context="Add 'Returns:' section",
                    )
                )

        # Check for Raises section if function raises exceptions
        has_raise = any(isinstance(n, ast.Raise) for n in ast.walk(node))
        if has_raise:
            if "raises:" not in docstring_lower and "raise:" not in docstring_lower:
                self.issues.append(
                    DocIssue(
                        file_path=self.file_path,
                        line_number=node.lineno,
                        issue_type="missing_raises_documentation",
                        severity="medium",
                        message=f"Function '{node.name}' raises exceptions but missing Raises documentation",
                        context="Add 'Raises:' section",
                    )
                )

    def _check_init_method(self, node: ast.FunctionDef, class_name: str) -> None:
        """Check __init__ method specifically."""
        # If __init__ has parameters beyond self, they should be documented
        if len(node.args.args) > 1:  # More than just 'self'
            docstring = ast.get_docstring(node)

            # __init__ docstring is optional if class docstring has Args
            if not docstring:
                # This is okay if class has Args section, otherwise it's an issue
                pass  # We already check this in class docstring quality

    def _check_type_hints(self, node: ast.FunctionDef) -> None:
        """Check if function has proper type hints."""
        # Check parameters
        for arg in node.args.args:
            if arg.arg != "self" and not arg.annotation:
                self.issues.append(
                    DocIssue(
                        file_path=self.file_path,
                        line_number=node.lineno,
                        issue_type="missing_type_hint",
                        severity="high",
                        message=f"Parameter '{arg.arg}' in '{node.name}' missing type hint",
                        context=f"def {node.name}",
                    )
                )

        # Check return type
        if not node.returns and node.name != "__init__":
            # Check if function has return statements
            has_return = any(isinstance(n, ast.Return) and n.value for n in ast.walk(node))
            if has_return:
                self.issues.append(
                    DocIssue(
                        file_path=self.file_path,
                        line_number=node.lineno,
                        issue_type="missing_return_type",
                        severity="high",
                        message=f"Function '{node.name}' missing return type hint",
                        context="Add -> ReturnType",
                    )
                )

    def _check_module_exports(self, node: ast.Module) -> None:
        """Check for __all__ exports in module."""
        has_all = False

        for item in node.body:
            if isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name) and target.id == "__all__":
                        has_all = True
                        # Extract exported names
                        if isinstance(item.value, ast.List):
                            for elt in item.value.elts:
                                if isinstance(elt, ast.Constant):
                                    self.module_exports.add(elt.value)

        # Check if this is an __init__.py file
        if "__init__.py" in self.file_path and not has_all:
            self.issues.append(
                DocIssue(
                    file_path=self.file_path,
                    line_number=1,
                    issue_type="missing___all__",
                    severity="high",
                    message="Module __init__.py missing __all__ exports",
                    context="Add __all__ = ['exported', 'names']",
                )
            )


def analyze_file(file_path: Path) -> FileReport:
    """Analyze a single Python file for documentation issues."""
    report = FileReport(file_path=str(file_path))

    try:
        source_code = file_path.read_text(encoding="utf-8")
        tree = ast.parse(source_code)

        analyzer = DocstringAnalyzer(str(file_path), source_code)
        analyzer.visit(tree)

        for issue in analyzer.issues:
            report.add_issue(issue)

    except Exception as e:
        report.add_issue(
            DocIssue(
                file_path=str(file_path),
                line_number=0,
                issue_type="parse_error",
                severity="critical",
                message=f"Failed to parse file: {e!s}",
                context="",
            )
        )

    return report


def find_python_files(root_dir: Path, exclude_dirs: set[str] | None = None) -> list[Path]:
    """Find all Python files in directory tree."""
    if exclude_dirs is None:
        exclude_dirs = {".venv", "__pycache__", ".git", ".nox", "build", "dist", ".tox"}

    python_files = []

    for path in root_dir.rglob("*.py"):
        # Skip excluded directories
        if any(excluded in path.parts for excluded in exclude_dirs):
            continue

        # Skip test files (optional)
        if "test" in path.parts or path.name.startswith("test_"):
            continue

        python_files.append(path)

    return sorted(python_files)


def generate_report(reports: list[FileReport], output_format: str = "text") -> str:
    """Generate summary report from file reports."""
    total_files = len(reports)
    total_issues = sum(r.total_issues for r in reports)
    total_critical = sum(r.critical_issues for r in reports)
    total_high = sum(r.high_issues for r in reports)
    total_medium = sum(r.medium_issues for r in reports)
    total_low = sum(r.low_issues for r in reports)

    # Group issues by type
    issues_by_type = defaultdict(int)
    for report in reports:
        for issue in report.issues:
            issues_by_type[issue.issue_type] += 1

    if output_format == "json":
        data = {
            "summary": {
                "total_files": total_files,
                "total_issues": total_issues,
                "critical": total_critical,
                "high": total_high,
                "medium": total_medium,
                "low": total_low,
            },
            "issues_by_type": dict(issues_by_type),
            "files": [],
        }

        for report in reports:
            if report.issues:
                file_data = {
                    "file": report.file_path,
                    "issue_count": report.total_issues,
                    "issues": [
                        {
                            "line": issue.line_number,
                            "type": issue.issue_type,
                            "severity": issue.severity,
                            "message": issue.message,
                            "context": issue.context,
                        }
                        for issue in report.issues
                    ],
                }
                data["files"].append(file_data)

        return json.dumps(data, indent=2)

    # text format
    output = []
    output.append("=" * 80)
    output.append("DOCUMENTATION AUDIT REPORT")
    output.append("=" * 80)
    output.append("")
    output.append(f"Total Files Analyzed: {total_files}")
    output.append(f"Total Issues Found: {total_issues}")
    output.append("")
    output.append("Issue Breakdown by Severity:")
    output.append(f"  🔴 Critical: {total_critical}")
    output.append(f"  🟠 High: {total_high}")
    output.append(f"  🟡 Medium: {total_medium}")
    output.append(f"  🟢 Low: {total_low}")
    output.append("")
    output.append("Issue Types:")
    for issue_type, count in sorted(issues_by_type.items(), key=lambda x: x[1], reverse=True):
        output.append(f"  - {issue_type}: {count}")
    output.append("")
    output.append("=" * 80)
    output.append("DETAILED ISSUES BY FILE")
    output.append("=" * 80)

    # Sort reports by number of issues (worst first)
    sorted_reports = sorted(reports, key=lambda r: r.total_issues, reverse=True)

    for report in sorted_reports:
        if report.issues:
            output.append("")
            output.append(f"\n📁 {report.file_path}")
            output.append(
                f"   Issues: {report.total_issues} (C:{report.critical_issues} H:{report.high_issues} M:{report.medium_issues} L:{report.low_issues})"
            )
            output.append("-" * 60)

            # Sort issues by line number
            sorted_issues = sorted(report.issues, key=lambda i: i.line_number)

            for issue in sorted_issues:
                severity_icon = {
                    "critical": "🔴",
                    "high": "🟠",
                    "medium": "🟡",
                    "low": "🟢",
                }.get(issue.severity, "❓")

                output.append(f"   {severity_icon} Line {issue.line_number}: {issue.message}")
                if issue.context:
                    output.append(f"      Context: {issue.context}")

    return "\n".join(output)


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Audit Python code documentation")
    parser.add_argument("path", help="Path to analyze (file or directory)")
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    parser.add_argument(
        "--include-tests", action="store_true", help="Include test files in analysis"
    )
    parser.add_argument(
        "--exclude", nargs="+", default=[], help="Additional directories to exclude"
    )

    args = parser.parse_args()

    path = Path(args.path)

    if not path.exists():
        sys.exit(1)

    # Collect files to analyze
    if path.is_file():
        files = [path]
    else:
        exclude_dirs = {".venv", "__pycache__", ".git", ".nox", "build", "dist", ".tox"}
        exclude_dirs.update(args.exclude)

        if not args.include_tests:
            exclude_dirs.add("tests")
            exclude_dirs.add("test")

        files = find_python_files(path, exclude_dirs)

    # Analyze files
    reports = []
    for file_path in files:
        report = analyze_file(file_path)
        reports.append(report)

    # Generate report
    output = generate_report(reports, args.format)

    # Output results
    if args.output:
        Path(args.output).write_text(output)
    else:
        pass

    # Exit with error if issues found
    total_issues = sum(r.total_issues for r in reports)
    if total_issues > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
