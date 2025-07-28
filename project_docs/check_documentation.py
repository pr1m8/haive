#!/usr/bin/env python3
"""Haive Documentation Checker Script.

Systematically checks all packages for documentation completeness including:
- Module docstrings
- Class docstrings
- Method/function docstrings
- Type hints
- __all__ exports
- Example files
- README files

Usage:
    python scripts/check_documentation.py
"""

import ast
import inspect
import json
import os
import re
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union, get_args, get_origin


@dataclass
class DocIssue:
    """Represents a documentation issue found in the codebase."""

    file_path: str
    line_number: int
    issue_type: str
    description: str
    severity: str  # 'critical', 'major', 'minor'


@dataclass
class FileReport:
    """Report for a single Python file."""

    file_path: str
    has_module_docstring: bool
    missing_class_docstrings: list[str]
    missing_method_docstrings: list[str]
    missing_function_docstrings: list[str]
    missing_type_hints: list[str]
    has_all_export: bool
    poor_type_signatures: list[str]
    pydantic_field_issues: list[str]
    async_typing_issues: list[str]
    generic_typing_issues: list[str]
    issues: list[DocIssue]


@dataclass
class PackageReport:
    """Report for an entire package."""

    package_name: str
    package_path: str
    file_reports: list[FileReport]
    has_main_init: bool
    has_readme: bool
    has_examples: bool
    missing_example_files: list[str]
    total_issues: int
    critical_issues: int
    major_issues: int
    minor_issues: int
    type_signature_issues: int
    pydantic_issues: int


class DocumentationChecker:
    """Main documentation checker class."""

    def __init__(self, root_path: str):
        self.root_path = Path(root_path)
        self.packages_path = self.root_path / "packages"
        self.output_dir = self.root_path / "doc_progress"
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Ensure output directory exists
        self.output_dir.mkdir(exist_ok=True)

    def check_all_packages(self) -> dict[str, PackageReport]:
        """Check documentation for all packages."""
        reports = {}

        if not self.packages_path.exists():
            return reports

        for package_dir in self.packages_path.iterdir():
            if package_dir.is_dir() and not package_dir.name.startswith("."):
                report = self.check_package(package_dir)
                reports[package_dir.name] = report

        return reports

    def check_package(self, package_path: Path) -> PackageReport:
        """Check documentation for a single package."""
        src_path = package_path / "src"

        # Find the main package directory
        main_package_path = None
        if src_path.exists():
            # Look for haive subdirectory structure
            for item in src_path.rglob("haive"):
                if item.is_dir():
                    main_package_path = item
                    break

        if not main_package_path:
            # Fallback to package_path itself
            main_package_path = package_path

        file_reports = []
        python_files = list(main_package_path.rglob("*.py"))

        for py_file in python_files:
            if not any(part.startswith(".") for part in py_file.parts):
                file_report = self.check_file(py_file)
                file_reports.append(file_report)

        # Check for main __init__.py
        main_init = main_package_path / "__init__.py"
        has_main_init = main_init.exists()

        # Check for README
        readme_files = list(package_path.glob("README*"))
        has_readme = len(readme_files) > 0

        # Check for examples
        example_files = list(package_path.rglob("example*.py"))
        examples_dir = package_path / "examples"
        has_examples = len(example_files) > 0 or examples_dir.exists()

        # Identify missing example files for major components
        missing_example_files = self._identify_missing_examples(main_package_path)

        # Count issues by severity
        total_issues = sum(len(fr.issues) for fr in file_reports)
        critical_issues = sum(
            len([i for i in fr.issues if i.severity == "critical"])
            for fr in file_reports
        )
        major_issues = sum(
            len([i for i in fr.issues if i.severity == "major"]) for fr in file_reports
        )
        minor_issues = sum(
            len([i for i in fr.issues if i.severity == "minor"]) for fr in file_reports
        )

        # Count type-related issues
        type_signature_issues = sum(len(fr.poor_type_signatures) for fr in file_reports)
        pydantic_issues = sum(len(fr.pydantic_field_issues) for fr in file_reports)

        return PackageReport(
            package_name=package_path.name,
            package_path=str(package_path),
            file_reports=file_reports,
            has_main_init=has_main_init,
            has_readme=has_readme,
            has_examples=has_examples,
            missing_example_files=missing_example_files,
            total_issues=total_issues,
            critical_issues=critical_issues,
            major_issues=major_issues,
            minor_issues=minor_issues,
            type_signature_issues=type_signature_issues,
            pydantic_issues=pydantic_issues,
        )

    def check_file(self, file_path: Path) -> FileReport:
        """Check documentation for a single Python file."""
        issues = []

        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            tree = ast.parse(content)

        except Exception as e:
            issues.append(
                DocIssue(
                    file_path=str(file_path),
                    line_number=1,
                    issue_type="parse_error",
                    description=f"Could not parse file: {e}",
                    severity="critical",
                )
            )

            return FileReport(
                file_path=str(file_path),
                has_module_docstring=False,
                missing_class_docstrings=[],
                missing_method_docstrings=[],
                missing_function_docstrings=[],
                missing_type_hints=[],
                has_all_export=False,
                poor_type_signatures=[],
                pydantic_field_issues=[],
                async_typing_issues=[],
                generic_typing_issues=[],
                issues=issues,
            )

        # Check module docstring
        has_module_docstring = ast.get_docstring(tree) is not None
        if not has_module_docstring and file_path.name != "__init__.py":
            issues.append(
                DocIssue(
                    file_path=str(file_path),
                    line_number=1,
                    issue_type="missing_module_docstring",
                    description="Module missing docstring",
                    severity="major",
                )
            )

        # Check for __all__ export
        has_all_export = any(
            isinstance(node, ast.Assign)
            and any(
                isinstance(target, ast.Name) and target.id == "__all__"
                for target in node.targets
            )
            for node in tree.body
        )

        if file_path.name == "__init__.py" and not has_all_export:
            issues.append(
                DocIssue(
                    file_path=str(file_path),
                    line_number=1,
                    issue_type="missing_all_export",
                    description="__init__.py missing __all__ definition",
                    severity="major",
                )
            )

        # Analyze classes, methods, and functions
        missing_class_docstrings = []
        missing_method_docstrings = []
        missing_function_docstrings = []
        missing_type_hints = []
        poor_type_signatures = []
        pydantic_field_issues = []
        async_typing_issues = []
        generic_typing_issues = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                if not ast.get_docstring(node):
                    missing_class_docstrings.append(node.name)
                    issues.append(
                        DocIssue(
                            file_path=str(file_path),
                            line_number=node.lineno,
                            issue_type="missing_class_docstring",
                            description=f"Class '{node.name}' missing docstring",
                            severity="major",
                        )
                    )

                # Check methods
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        if not ast.get_docstring(item) and not item.name.startswith(
                            "_"
                        ):
                            missing_method_docstrings.append(f"{node.name}.{item.name}")
                            issues.append(
                                DocIssue(
                                    file_path=str(file_path),
                                    line_number=item.lineno,
                                    issue_type="missing_method_docstring",
                                    description=f"Method '{node.name}.{item.name}' missing docstring",
                                    severity="minor",
                                )
                            )

                        # Check type hints
                        if not self._has_adequate_type_hints(item):
                            missing_type_hints.append(f"{node.name}.{item.name}")
                            issues.append(
                                DocIssue(
                                    file_path=str(file_path),
                                    line_number=item.lineno,
                                    issue_type="missing_type_hints",
                                    description=f"Method '{node.name}.{item.name}' missing type hints",
                                    severity="minor",
                                )
                            )

                        # Check for poor type signatures
                        signature_issues = self._check_type_signature_quality(
                            item, f"{node.name}.{item.name}"
                        )
                        poor_type_signatures.extend(signature_issues)

                        # Check for async typing issues
                        async_issues = self._check_async_typing(
                            item, f"{node.name}.{item.name}"
                        )
                        async_typing_issues.extend(async_issues)

            elif isinstance(node, ast.FunctionDef) and not self._is_inside_class(
                node, tree
            ):
                if not ast.get_docstring(node) and not node.name.startswith("_"):
                    missing_function_docstrings.append(node.name)
                    issues.append(
                        DocIssue(
                            file_path=str(file_path),
                            line_number=node.lineno,
                            issue_type="missing_function_docstring",
                            description=f"Function '{node.name}' missing docstring",
                            severity="major",
                        )
                    )

                # Check type hints
                if not self._has_adequate_type_hints(node):
                    missing_type_hints.append(node.name)
                    issues.append(
                        DocIssue(
                            file_path=str(file_path),
                            line_number=node.lineno,
                            issue_type="missing_type_hints",
                            description=f"Function '{node.name}' missing type hints",
                            severity="minor",
                        )
                    )

                # Check for poor type signatures
                signature_issues = self._check_type_signature_quality(node, node.name)
                poor_type_signatures.extend(signature_issues)

                # Check for async typing issues
                async_issues = self._check_async_typing(node, node.name)
                async_typing_issues.extend(async_issues)

        # Check for Pydantic model issues
        pydantic_field_issues = self._check_pydantic_fields(tree, str(file_path))

        # Check for generic typing issues
        generic_typing_issues = self._check_generic_typing(tree, str(file_path))

        # Add type signature issues to main issues list
        for sig_issue in poor_type_signatures:
            issues.append(
                DocIssue(
                    file_path=str(file_path),
                    line_number=1,  # Will be updated by specific checks
                    issue_type="poor_type_signature",
                    description=sig_issue,
                    severity="minor",
                )
            )

        return FileReport(
            file_path=str(file_path),
            has_module_docstring=has_module_docstring,
            missing_class_docstrings=missing_class_docstrings,
            missing_method_docstrings=missing_method_docstrings,
            missing_function_docstrings=missing_function_docstrings,
            missing_type_hints=missing_type_hints,
            has_all_export=has_all_export,
            poor_type_signatures=poor_type_signatures,
            pydantic_field_issues=pydantic_field_issues,
            async_typing_issues=async_typing_issues,
            generic_typing_issues=generic_typing_issues,
            issues=issues,
        )

    def _has_adequate_type_hints(self, func_node: ast.FunctionDef) -> bool:
        """Check if function has adequate type hints."""
        # Skip private methods and __init__
        if func_node.name.startswith("_"):
            return True

        # Check return annotation
        has_return_annotation = func_node.returns is not None

        # Check argument annotations (skip 'self' and 'cls')
        args_with_annotations = 0
        total_args = 0

        for arg in func_node.args.args:
            if arg.arg not in ["self", "cls"]:
                total_args += 1
                if arg.annotation is not None:
                    args_with_annotations += 1

        # Consider adequate if most args have annotations and return is annotated
        args_ratio = args_with_annotations / max(total_args, 1)
        return args_ratio >= 0.8 and (has_return_annotation or total_args == 0)

    def _is_inside_class(self, func_node: ast.FunctionDef, tree: ast.AST) -> bool:
        """Check if function is defined inside a class."""
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and func_node in ast.walk(node):
                return True
        return False

    def _identify_missing_examples(self, package_path: Path) -> list[str]:
        """Identify major components that should have example files."""
        missing_examples = []

        # Look for agent directories
        agent_dirs = []
        for item in package_path.rglob("*"):
            if item.is_dir() and (
                "agent" in item.name.lower() or "engine" in item.name.lower()
            ):
                agent_dirs.append(item)

        for agent_dir in agent_dirs:
            example_file = agent_dir / "example.py"
            if not example_file.exists():
                missing_examples.append(str(agent_dir.relative_to(package_path)))

        return missing_examples

    def _check_type_signature_quality(
        self, func_node: ast.FunctionDef, func_name: str
    ) -> list[str]:
        """Check for poor quality type signatures."""
        issues = []

        # Check for overly generic types like 'Any'
        for arg in func_node.args.args:
            if arg.annotation and self._is_generic_type(arg.annotation):
                issues.append(
                    f"Function '{func_name}' uses overly generic type 'Any' for parameter '{arg.arg}'"
                )

        if func_node.returns and self._is_generic_type(func_node.returns):
            issues.append(f"Function '{func_name}' returns overly generic type 'Any'")

        # Check for missing Union types where None is possible
        if func_node.returns and self._might_return_none(func_node):
            if not self._has_optional_return_type(func_node.returns):
                issues.append(
                    f"Function '{func_name}' might return None but type signature doesn't indicate Optional"
                )

        # Check for inconsistent parameter naming with types
        for arg in func_node.args.args:
            if arg.annotation and self._has_type_name_mismatch(arg.arg, arg.annotation):
                issues.append(
                    f"Function '{func_name}' parameter '{arg.arg}' name doesn't match type hint"
                )

        return issues

    def _check_async_typing(
        self, func_node: ast.FunctionDef, func_name: str
    ) -> list[str]:
        """Check for async function typing issues."""
        issues = []

        # Check if async function returns proper Awaitable/Coroutine type
        if hasattr(func_node, "returns") and func_node.returns:
            if self._is_async_function(func_node):
                if not self._has_proper_async_return_type(func_node.returns):
                    issues.append(
                        f"Async function '{func_name}' should return Awaitable or Coroutine type"
                    )

        return issues

    def _check_pydantic_fields(self, tree: ast.AST, file_path: str) -> list[str]:
        """Check for Pydantic model field documentation issues."""
        issues = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Check if this might be a Pydantic model
                if self._is_pydantic_model(node):
                    for item in node.body:
                        if isinstance(item, ast.AnnAssign) and isinstance(
                            item.target, ast.Name
                        ):
                            field_name = item.target.id

                            # Check if Field() is used with description
                            if item.value and not self._has_field_description(
                                item.value
                            ):
                                issues.append(
                                    f"Pydantic field '{field_name}' in class '{node.name}' missing Field description"
                                )

                            # Check for proper type annotations on fields
                            if not item.annotation:
                                issues.append(
                                    f"Pydantic field '{field_name}' in class '{node.name}' missing type annotation"
                                )

        return issues

    def _check_generic_typing(self, tree: ast.AST, file_path: str) -> list[str]:
        """Check for proper use of generic types."""
        issues = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Check for generic classes without proper TypeVar usage
                if self._uses_generics_without_typevar(node):
                    issues.append(
                        f"Class '{node.name}' uses generic types but doesn't define TypeVar"
                    )

            elif isinstance(node, ast.FunctionDef):
                # Check for functions with generic parameters but no type bounds
                if self._has_unbounded_generics(node):
                    issues.append(
                        f"Function '{node.name}' uses unbounded generic types"
                    )

        return issues

    def _is_generic_type(self, annotation: ast.AST) -> bool:
        """Check if annotation is overly generic (Any, object, etc.)."""
        if isinstance(annotation, ast.Name):
            return annotation.id in ["Any", "object"]
        if isinstance(annotation, ast.Attribute):
            return annotation.attr in ["Any", "object"]
        return False

    def _might_return_none(self, func_node: ast.FunctionDef) -> bool:
        """Check if function might return None by examining its body."""
        for node in ast.walk(func_node):
            if isinstance(node, ast.Return) and (node.value is None or (
                isinstance(node.value, ast.Constant) and node.value.value is None
            )):
                return True
        return False

    def _has_optional_return_type(self, returns: ast.AST) -> bool:
        """Check if return type indicates Optional/Union with None."""
        if isinstance(returns, ast.Subscript):
            if isinstance(returns.value, ast.Name):
                return returns.value.id in ["Optional", "Union"]
            if isinstance(returns.value, ast.Attribute):
                return returns.value.attr in ["Optional", "Union"]
        return False

    def _has_type_name_mismatch(self, param_name: str, annotation: ast.AST) -> bool:
        """Check for obvious mismatches between parameter name and type."""
        # Simple heuristic checks
        if "id" in param_name.lower() and isinstance(annotation, ast.Name):
            if annotation.id not in ["int", "str", "UUID"]:
                return True
        if "count" in param_name.lower() and isinstance(annotation, ast.Name):
            if annotation.id not in ["int", "float"]:
                return True
        return False

    def _is_async_function(self, func_node: ast.FunctionDef) -> bool:
        """Check if function is async."""
        return isinstance(func_node, ast.AsyncFunctionDef)

    def _has_proper_async_return_type(self, returns: ast.AST) -> bool:
        """Check if async function has proper return type."""
        if isinstance(returns, ast.Name):
            return returns.id in ["Awaitable", "Coroutine"]
        if isinstance(returns, ast.Subscript):
            if isinstance(returns.value, ast.Name):
                return returns.value.id in ["Awaitable", "Coroutine"]
        return False

    def _is_pydantic_model(self, class_node: ast.ClassDef) -> bool:
        """Check if class is likely a Pydantic model."""
        for base in class_node.bases:
            if isinstance(base, ast.Name) and "BaseModel" in base.id:
                return True
            if isinstance(base, ast.Attribute) and base.attr == "BaseModel":
                return True
        return False

    def _has_field_description(self, value: ast.AST) -> bool:
        """Check if Pydantic Field has description."""
        if isinstance(value, ast.Call):
            if isinstance(value.func, ast.Name) and value.func.id == "Field":
                # Check for description keyword argument
                for keyword in value.keywords:
                    if keyword.arg == "description":
                        return True
        return False

    def _uses_generics_without_typevar(self, class_node: ast.ClassDef) -> bool:
        """Check if class uses generics without proper TypeVar."""
        # Simplified check - look for Generic in bases but no TypeVar in class
        has_generic = False
        for base in class_node.bases:
            if isinstance(base, ast.Subscript):
                if isinstance(base.value, ast.Name) and base.value.id == "Generic":
                    has_generic = True
                    break

        if has_generic:
            # Check if class defines or imports TypeVar
            # This is a simplified check
            return True  # Could be enhanced with more sophisticated analysis

        return False

    def _has_unbounded_generics(self, func_node: ast.FunctionDef) -> bool:
        """Check if function uses unbounded generic types."""
        # Simplified check for TypeVar usage without bounds
        return False  # Could be enhanced with more sophisticated analysis

    def generate_reports(self, reports: dict[str, PackageReport]) -> None:
        """Generate comprehensive reports."""
        timestamp_dir = self.output_dir / f"report_{self.timestamp}"
        timestamp_dir.mkdir(exist_ok=True)

        # Generate JSON report
        json_data = {pkg: asdict(report) for pkg, report in reports.items()}
        with open(timestamp_dir / "full_report.json", "w") as f:
            json.dump(json_data, f, indent=2)

        # Generate summary report
        self._generate_summary_report(reports, timestamp_dir)

        # Generate detailed reports per package
        for _pkg_name, report in reports.items():
            self._generate_package_report(report, timestamp_dir)

        # Generate priority action list
        self._generate_action_list(reports, timestamp_dir)


    def _generate_summary_report(
        self, reports: dict[str, PackageReport], output_dir: Path
    ) -> None:
        """Generate summary report."""
        with open(output_dir / "summary.md", "w") as f:
            f.write("# Haive Documentation Status Summary\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            # Overall stats
            total_packages = len(reports)
            total_issues = sum(r.total_issues for r in reports.values())
            critical_issues = sum(r.critical_issues for r in reports.values())
            major_issues = sum(r.major_issues for r in reports.values())
            minor_issues = sum(r.minor_issues for r in reports.values())
            type_signature_issues = sum(
                r.type_signature_issues for r in reports.values()
            )
            pydantic_issues = sum(r.pydantic_issues for r in reports.values())

            f.write("## Overview\n\n")
            f.write(f"- **Total Packages Checked**: {total_packages}\n")
            f.write(f"- **Total Issues**: {total_issues}\n")
            f.write(f"- **Critical Issues**: {critical_issues}\n")
            f.write(f"- **Major Issues**: {major_issues}\n")
            f.write(f"- **Minor Issues**: {minor_issues}\n")
            f.write(f"- **Type Signature Issues**: {type_signature_issues}\n")
            f.write(f"- **Pydantic Field Issues**: {pydantic_issues}\n\n")

            # Package breakdown
            f.write("## Package Status\n\n")
            f.write(
                "| Package | Total Issues | Critical | Major | Minor | Type Sig | Pydantic | README | Examples |\n"
            )
            f.write(
                "|---------|--------------|----------|-------|-------|----------|----------|--------|----------|\n"
            )

            for pkg_name, report in sorted(reports.items()):
                readme_status = "✅" if report.has_readme else "❌"
                examples_status = "✅" if report.has_examples else "❌"
                f.write(
                    f"| {pkg_name} | {report.total_issues} | {report.critical_issues} | {report.major_issues} | {report.minor_issues} | {report.type_signature_issues} | {report.pydantic_issues} | {readme_status} | {examples_status} |\n"
                )

    def _generate_package_report(self, report: PackageReport, output_dir: Path) -> None:
        """Generate detailed report for a single package."""
        filename = f"{report.package_name}_detail.md"

        with open(output_dir / filename, "w") as f:
            f.write(f"# {report.package_name} Documentation Report\n\n")

            f.write("## Package Overview\n\n")
            f.write(f"- **Package Path**: {report.package_path}\n")
            f.write(f"- **Type Signature Issues**: {report.type_signature_issues}\n")
            f.write(f"- **Pydantic Field Issues**: {report.pydantic_issues}\n")
            f.write(
                f"- **Has Main __init__.py**: {'✅' if report.has_main_init else '❌'}\n"
            )
            f.write(f"- **Has README**: {'✅' if report.has_readme else '❌'}\n")
            f.write(f"- **Has Examples**: {'✅' if report.has_examples else '❌'}\n")
            f.write(f"- **Total Issues**: {report.total_issues}\n\n")

            if report.missing_example_files:
                f.write("## Missing Example Files\n\n")
                for missing in report.missing_example_files:
                    f.write(f"- {missing}\n")
                f.write("\n")

            # Group issues by file
            issues_by_file = {}
            for file_report in report.file_reports:
                if file_report.issues:
                    issues_by_file[file_report.file_path] = file_report.issues

            if issues_by_file:
                f.write("## Issues by File\n\n")
                for file_path, issues in issues_by_file.items():
                    rel_path = Path(file_path).relative_to(Path(report.package_path))
                    f.write(f"### {rel_path}\n\n")

                    for issue in issues:
                        severity_emoji = {
                            "critical": "🔴",
                            "major": "🟡",
                            "minor": "🔵",
                        }
                        emoji = severity_emoji.get(issue.severity, "⚪")
                        f.write(
                            f"- {emoji} **Line {issue.line_number}**: {issue.description}\n"
                        )
                    f.write("\n")

    def _generate_action_list(
        self, reports: dict[str, PackageReport], output_dir: Path
    ) -> None:
        """Generate prioritized action list."""
        with open(output_dir / "action_plan.md", "w") as f:
            f.write("# Documentation Action Plan\n\n")
            f.write("Prioritized list of documentation improvements needed.\n\n")

            # Collect all critical issues
            critical_issues = []
            major_issues = []

            for pkg_name, report in reports.items():
                for file_report in report.file_reports:
                    for issue in file_report.issues:
                        if issue.severity == "critical":
                            critical_issues.append((pkg_name, issue))
                        elif issue.severity == "major":
                            major_issues.append((pkg_name, issue))

            if critical_issues:
                f.write("## 🔴 Critical Issues (Fix First)\n\n")
                for pkg_name, issue in critical_issues:
                    rel_path = Path(issue.file_path).name
                    f.write(
                        f"- **{pkg_name}**/{rel_path}:{issue.line_number} - {issue.description}\n"
                    )
                f.write("\n")

            if major_issues:
                f.write("## 🟡 Major Issues\n\n")
                for pkg_name, issue in major_issues:
                    rel_path = Path(issue.file_path).name
                    f.write(
                        f"- **{pkg_name}**/{rel_path}:{issue.line_number} - {issue.description}\n"
                    )
                f.write("\n")

            # Package-level recommendations
            f.write("## 📦 Package-Level Actions\n\n")
            for pkg_name, report in reports.items():
                actions = []
                if not report.has_readme:
                    actions.append("Create README.md")
                if not report.has_examples:
                    actions.append("Add example files")
                if report.missing_example_files:
                    actions.append(
                        f"Add examples for: {', '.join(report.missing_example_files)}"
                    )

                if actions:
                    f.write(f"### {pkg_name}\n")
                    for action in actions:
                        f.write(f"- {action}\n")
                    f.write("\n")


def main():
    """Main entry point."""
    script_dir = Path(__file__).parent
    root_dir = script_dir.parent

    checker = DocumentationChecker(str(root_dir))


    reports = checker.check_all_packages()

    if not reports:
        return

    checker.generate_reports(reports)

    # Print quick summary
    total_issues = sum(r.total_issues for r in reports.values())
    critical_issues = sum(r.critical_issues for r in reports.values())


    if critical_issues > 0:
        pass
    elif total_issues > 0:
        print("pass.")
    else:
        print("pass")


if __name__ == "__main__":
    main()