#!/usr/bin/env python3
"""Type hint analyzer and improvement automation.

This script analyzes Python files for missing type hints and provides
automated fixes where possible. Uses mypy output to identify issues
and suggests improvements.
"""

import argparse
import ast
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


class TypeHintAnalyzer:
    """Analyze and improve type hints in Python code."""

    def __init__(self, base_path: str = "packages/"):
        self.base_path = Path(base_path)
        self.stats = {
            "files_analyzed": 0,
            "functions_without_hints": 0,
            "functions_with_partial_hints": 0,
            "functions_improved": 0,
            "common_patterns": {},
        }

    def run_mypy_analysis(self, target_path: str) -> list[str]:
        """Run mypy and return list of type hint issues."""
        try:
            result = subprocess.run(
                [
                    "poetry",
                    "run",
                    "mypy",
                    target_path,
                    "--ignore-missing-imports",
                    "--show-error-codes",
                ],
                check=False, capture_output=True,
                text=True,
                timeout=60,
            )

            # Filter for type hint related errors
            lines = result.stdout.split("\n")
            type_hint_issues = []

            for line in lines:
                if any(
                    code in line
                    for code in [
                        "no-untyped-def",
                        "no-untyped-call",
                        "type-arg",
                        "return-value",
                        "arg-type",
                    ]
                ):
                    type_hint_issues.append(line.strip())

            return type_hint_issues

        except subprocess.TimeoutExpired:
            return []
        except Exception as e:
            return []

    def analyze_function_signatures(self, file_path: Path) -> list[dict[str, Any]]:
        """Analyze function signatures for missing type hints."""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            tree = ast.parse(content)
            functions = []

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_info = self._analyze_function_node(node, content)
                    if func_info:
                        functions.append(func_info)

            return functions

        except Exception as e:
            return []

    def _analyze_function_node(
        self, node: ast.FunctionDef, content: str
    ) -> Dict[str, Any] | None:
        """Analyze a single function node for type hints."""
        # Skip private methods and special methods (but not __init__)
        if node.name.startswith("_") and node.name not in ["__init__", "__call__"]:
            return None

        # Check parameter type hints
        missing_param_hints = []
        for arg in node.args.args:
            if arg.annotation is None and arg.arg != "self":
                missing_param_hints.append(arg.arg)

        # Check return type hint
        has_return_hint = node.returns is not None

        # Analyze function body for return patterns
        return_patterns = self._analyze_return_patterns(node)

        # Only report if missing hints
        if missing_param_hints or not has_return_hint:
            return {
                "name": node.name,
                "line": node.lineno,
                "missing_param_hints": missing_param_hints,
                "has_return_hint": has_return_hint,
                "return_patterns": return_patterns,
                "is_async": isinstance(node, ast.AsyncFunctionDef),
                "docstring": ast.get_docstring(node),
            }

        return None

    def _analyze_return_patterns(self, node: ast.FunctionDef) -> list[str]:
        """Analyze return statements to suggest return types."""
        patterns = []

        for child in ast.walk(node):
            if isinstance(child, ast.Return):
                if child.value is None:
                    patterns.append("None")
                elif isinstance(child.value, ast.Constant):
                    if isinstance(child.value.value, bool):
                        patterns.append("bool")
                    elif isinstance(child.value.value, int):
                        patterns.append("int")
                    elif isinstance(child.value.value, str):
                        patterns.append("str")
                    elif isinstance(child.value.value, float):
                        patterns.append("float")
                elif isinstance(child.value, ast.List):
                    patterns.append("List")
                elif isinstance(child.value, ast.Dict):
                    patterns.append("Dict")
                elif isinstance(child.value, ast.Call):
                    patterns.append("object")  # Generic for function calls

        return list(set(patterns))  # Remove duplicates

    def suggest_type_hints(self, func_info: dict[str, Any]) -> dict[str, str]:
        """Suggest type hints based on function analysis."""
        suggestions = {}

        # Parameter suggestions based on name patterns
        for param in func_info["missing_param_hints"]:
            param_type = self._suggest_param_type(param, func_info)
            if param_type:
                suggestions[param] = param_type

        # Return type suggestions
        if not func_info["has_return_hint"]:
            return_type = self._suggest_return_type(func_info)
            if return_type:
                suggestions["return"] = return_type

        return suggestions

    def _suggest_param_type(
        self, param_name: str, func_info: dict[str, Any]
    ) -> str | None:
        """Suggest parameter type based on naming patterns."""
        name_patterns = {
            # Common patterns
            "config": "Dict[str, Any]",
            "data": "Dict[str, Any]",
            "kwargs": "Any",
            "args": "Any",
            "params": "Dict[str, Any]",
            # String patterns
            "name": "str",
            "text": "str",
            "content": "str",
            "message": "str",
            "query": "str",
            "prompt": "str",
            "input": "str",
            "output": "str",
            "response": "str",
            # Number patterns
            "count": "int",
            "size": "int",
            "limit": "int",
            "offset": "int",
            "timeout": "float",
            "temperature": "float",
            "threshold": "float",
            # Boolean patterns
            "enabled": "bool",
            "active": "bool",
            "debug": "bool",
            "strict": "bool",
            "force": "bool",
            # Collection patterns
            "items": "List[Any]",
            "results": "List[Any]",
            "tools": "List[str]",
            "messages": "List[Dict[str, Any]]",
            "headers": "Dict[str, str]",
            "metadata": "Dict[str, Any]",
        }

        # Check exact matches first
        if param_name in name_patterns:
            return name_patterns[param_name]

        # Check suffix patterns
        if param_name.endswith("_id"):
            return "str"
        if param_name.endswith("_list"):
            return "List[Any]"
        elif param_name.endswith("_dict"):
            return "Dict[str, Any]"
        elif param_name.endswith("_count"):
            return "int"
        elif param_name.endswith("_enabled"):
            return "bool"

        return None

    def _suggest_return_type(self, func_info: dict[str, Any]) -> str | None:
        """Suggest return type based on analysis."""
        patterns = func_info["return_patterns"]

        if not patterns:
            # No explicit returns found, likely None
            return "None"

        if len(patterns) == 1:
            pattern = patterns[0]
            if pattern == "None":
                return "None"
            if pattern in ["bool", "int", "str", "float"]:
                return pattern
            elif pattern == "List":
                return "List[Any]"
            elif pattern == "Dict":
                return "Dict[str, Any]"

        # Multiple return types - use Union or Any
        if "None" in patterns and len(patterns) == 2:
            other_type = next(p for p in patterns if p != "None")
            return f"Optional[{other_type}]"

        # Function name patterns
        func_name = func_info["name"]
        if (
            func_name.startswith(("is_", "has_", "can_"))
        ):
            return "bool"
        if func_name.startswith(("get_", "find_")):
            return "Any"  # Could be anything
        elif func_name.startswith(("create_", "build_")):
            return "Any"  # Object creation

        return "Any"

    def generate_type_hint_fixes(self, file_path: Path) -> list[str]:
        """Generate concrete type hint fixes for a file."""
        functions = self.analyze_function_signatures(file_path)
        fixes = []

        for func in functions:
            suggestions = self.suggest_type_hints(func)
            if suggestions:
                fix_desc = f"{file_path}:{func['line']} - Function '{func['name']}'"

                param_fixes = []
                for param, hint in suggestions.items():
                    if param != "return":
                        param_fixes.append(f"{param}: {hint}")

                if param_fixes:
                    fix_desc += f" - Add param hints: {', '.join(param_fixes)}"

                if "return" in suggestions:
                    fix_desc += f" - Add return hint: -> {suggestions['return']}"

                fixes.append(fix_desc)

        return fixes

    def analyze_package(self, package_name: str) -> dict[str, Any]:
        """Analyze a specific package for type hint issues."""
        package_path = self.base_path / package_name / "src"

        if not package_path.exists():
            return {}


        python_files = list(package_path.rglob("*.py"))
        results = {
            "package": package_name,
            "files": [],
            "total_issues": 0,
            "mypy_issues": [],
        }

        for py_file in python_files:
            if py_file.name == "__pycache__":
                continue

            self.stats["files_analyzed"] += 1

            # Analyze function signatures
            functions = self.analyze_function_signatures(py_file)
            issues = len(functions)

            if issues > 0:
                results["files"].append(
                    {
                        "path": str(py_file.relative_to(self.base_path)),
                        "issues": issues,
                        "functions": functions,
                    }
                )
                results["total_issues"] += issues

        # Run mypy analysis on package
        try:
            mypy_issues = self.run_mypy_analysis(str(package_path))
            results["mypy_issues"] = mypy_issues
        except Exception as e:
            print("pass")

        return results

    def print_analysis_report(self, results: dict[str, Any]):
        """Print formatted analysis report."""
        pkg = results["package"]
        total = results["total_issues"]


        if results.get("mypy_issues"):
            pass

        # Top files by issue count
        if results["files"]:
            sorted_files = sorted(
                results["files"], key=lambda x: x["issues"], reverse=True
            )

            for i, file_info in enumerate(sorted_files[:5]):
                pass

        # Sample suggestions
        if results["files"]:
            sample_file = results["files"][0]
            fixes = self.generate_type_hint_fixes(Path(sample_file["path"]))

            for i, fix in enumerate(fixes[:3]):
                pass



def main():
    """Main analysis function."""
    parser = argparse.ArgumentParser(description="Analyze type hints in Haive packages")
    parser.add_argument("--package", help="Specific package to analyze")
    parser.add_argument("--all", action="store_true", help="Analyze all packages")
    parser.add_argument("--suggest", action="store_true", help="Generate suggestions")

    args = parser.parse_args()

    analyzer = TypeHintAnalyzer()

    # Available packages
    packages = [
        "haive-core",
        "haive-agents",
        "haive-tools",
        "haive-dataflow",
        "haive-games",
        "haive-mcp",
        "haive-prebuilt",
    ]

    if args.package:
        if args.package in packages:
            results = analyzer.analyze_package(args.package)
            analyzer.print_analysis_report(results)
        else:
            pass

    elif args.all:

        all_results = []
        for package in packages:
            results = analyzer.analyze_package(package)
            if results:
                all_results.append(results)
                analyzer.print_analysis_report(results)

        # Summary
        total_issues = sum(r["total_issues"] for r in all_results)

    else:
        # Quick analysis of core packages
        quick_packages = ["haive-core", "haive-agents"]

        for package in quick_packages:
            results = analyzer.analyze_package(package)
            if results:
                analyzer.print_analysis_report(results)


if __name__ == "__main__":
    main()