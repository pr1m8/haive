#!/usr/bin/env python3
"""Audit all validators in the codebase and report issues."""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Any


class ValidatorAuditor(ast.NodeVisitor):

    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.issues = []
        self.current_class = None
        self.decorators_stack = []

    def visit_ClassDef(self, node):
        old_class = self.current_class
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = old_class

    def visit_FunctionDef(self, node):
        # Check if this is a validator
        validator_info = self.analyze_decorators(node.decorator_list)

        if validator_info:
            # Analyze the function signature
            has_cls = any(arg.arg == "cls" for arg in node.args.args)
            has_self = any(arg.arg == "self" for arg in node.args.args)

            # Check for issues
            if validator_info["type"] == "field_validator":
                if not validator_info["has_classmethod"]:
                    self.issues.append(
                        {
                            "file": str(self.file_path),
                            "line": node.lineno,
                            "class": self.current_class,
                            "function": node.name,
                            "issue": "field_validator missing @classmethod",
                            "severity": "error",
                        }, )
                elif has_self:
                    self.issues.append(
                        {
                            "file": str(self.file_path),
                            "line": node.lineno,
                            "class": self.current_class,
                            "function": node.name,
                            "issue": "field_validator has self instead of cls",
                            "severity": "error",
                        }, )

            elif validator_info["type"] == "model_validator":
                mode = validator_info.get("mode", "after")

                if mode == "before":
                    if not validator_info["has_classmethod"]:
                        self.issues.append(
                            {
                                "file": str(self.file_path),
                                "line": node.lineno,
                                "class": self.current_class,
                                "function": node.name,
                                "issue":
                                'model_validator(mode="before") missing @classmethod',
                                "severity": "error",
                            }, )
                    elif has_self:
                        self.issues.append(
                            {
                                "file": str(
                                    self.file_path),
                                "line": node.lineno,
                                "class": self.current_class,
                                "function": node.name,
                                "issue": 'model_validator(mode="before") has self instead of cls',
                                "severity": "error",
                            },
                        )

                elif mode == "after":
                    if validator_info["has_classmethod"]:
                        self.issues.append(
                            {
                                "file": str(
                                    self.file_path),
                                "line": node.lineno,
                                "class": self.current_class,
                                "function": node.name,
                                "issue": 'model_validator(mode="after") should not have @classmethod',
                                "severity": "error",
                            },
                        )
                    elif has_cls:
                        self.issues.append(
                            {
                                "file": str(self.file_path),
                                "line": node.lineno,
                                "class": self.current_class,
                                "function": node.name,
                                "issue":
                                'model_validator(mode="after") has cls instead of self',
                                "severity": "error",
                            }, )

                elif mode == "wrap":
                    if validator_info["has_classmethod"]:
                        self.issues.append(
                            {
                                "file": str(
                                    self.file_path),
                                "line": node.lineno,
                                "class": self.current_class,
                                "function": node.name,
                                "issue": 'model_validator(mode="wrap") should not have @classmethod',
                                "severity": "error",
                            },
                        )

        self.generic_visit(node)

    def analyze_decorators(self, decorators):
        validator_info = None
        has_classmethod = False

        for dec in decorators:
            dec_str = ast.unparse(dec)

            if "field_validator" in dec_str:
                validator_info = {"type": "field_validator"}
            elif "model_validator" in dec_str:
                validator_info = {"type": "model_validator"}
                # Extract mode
                if isinstance(dec, ast.Call):
                    for keyword in dec.keywords:
                        if keyword.arg == "mode":
                            if isinstance(keyword.value, ast.Constant):
                                validator_info["mode"] = keyword.value.value
            elif "classmethod" in dec_str:
                has_classmethod = True

        if validator_info:
            validator_info["has_classmethod"] = has_classmethod

        return validator_info


def audit_file(file_path: Path) -> list[dict[str, Any]]:
    """Audit a single Python file for validator issues."""
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        tree = ast.parse(content)
        auditor = ValidatorAuditor(file_path)
        auditor.visit(tree)
        return auditor.issues
    except BaseException:
        return []


def main():
    """Audit all Python files in packages."""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    packages_dir = project_root / "packages"

    all_issues = []

    print("Auditing validators in all packages...")

    for py_file in packages_dir.rglob("*.py"):
        if "__pycache__" in str(py_file) or "/tests/" in str(py_file):
            continue

        issues = audit_file(py_file)
        all_issues.extend(issues)

    # Group by issue type
    issue_types = {}
    for issue in all_issues:
        issue_type = issue["issue"]
        if issue_type not in issue_types:
            issue_types[issue_type] = []
        issue_types[issue_type].append(issue)

    # Report
    print(f"\nTotal issues found: {len(all_issues)}")
    print("\nIssues by type:")

    for issue_type, issues in sorted(issue_types.items()):
        print(f"\n{issue_type}: {len(issues)} occurrences")
        # Show first 3 examples
        for issue in issues[:3]:
            print(
                f"  - {
                    issue['file']}:{
                    issue['line']} in {
                    issue['class']}.{
                    issue['function']}",
            )
        if len(issues) > 3:
            print(f"  ... and {len(issues) - 3} more")

    # Save detailed report
    report_file = script_dir / "validator_audit_report.txt"
    with open(report_file, "w") as f:
        f.write("VALIDATOR AUDIT REPORT\n")
        f.write("=====================\n\n")

        for issue_type, issues in sorted(issue_types.items()):
            f.write(f"\n{issue_type}: {len(issues)} occurrences\n")
            f.write("-" * 80 + "\n")

            for issue in issues:
                f.write(f"{issue['file']}:{issue['line']}\n")
                f.write(f"  Class: {issue['class']}\n")
                f.write(f"  Function: {issue['function']}\n")
                f.write("\n")

    print(f"\nDetailed report saved to: {report_file}")


if __name__ == "__main__":
    main()
