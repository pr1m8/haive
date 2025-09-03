#!/usr/bin/env python3
"""Automated docstring generator using AST analysis and templates.

This script automatically generates comprehensive docstrings for Python
files by analyzing the code structure and applying intelligent templates.
"""

import ast
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


class DocstringGenerator:
    """Generate docstrings automatically based on code analysis."""

    def __init__(self):
        self.generated_count = 0
        self.skipped_count = 0

    def analyze_function(self, node: ast.FunctionDef) -> dict[str, Any]:
        """Analyze a function node to extract information for docstring."""
        info = {
            "name": node.name,
            "args": [],
            "returns": None,
            "raises": set(),
            "is_async": isinstance(node, ast.AsyncFunctionDef),
            "is_property": False,
            "is_classmethod": False,
            "is_staticmethod": False,
            "has_yield": False,
            "complexity": 0,
        }

        # Check decorators
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Name):
                if decorator.id == "property":
                    info["is_property"] = True
                elif decorator.id == "classmethod":
                    info["is_classmethod"] = True
                elif decorator.id == "staticmethod":
                    info["is_staticmethod"] = True

        # Extract arguments
        for arg in node.args.args:
            if arg.arg not in ["self", "cls"]:
                arg_info = {"name": arg.arg, "type": None, "default": None}

                # Get type annotation
                if arg.annotation:
                    arg_info["type"] = ast.unparse(arg.annotation)

                info["args"].append(arg_info)

        # Extract return type
        if node.returns:
            info["returns"] = ast.unparse(node.returns)

        # Analyze function body
        for child in ast.walk(node):
            # Check for raise statements
            if isinstance(child, ast.Raise):
                if isinstance(child.exc, ast.Call) and isinstance(
                    child.exc.func, ast.Name
                ):
                    info["raises"].add(child.exc.func.id)
                elif isinstance(child.exc, ast.Name):
                    info["raises"].add(child.exc.id)

            # Check for yield
            if isinstance(child, ast.Yield | ast.YieldFrom):
                info["has_yield"] = True

            # Simple complexity metric
            if isinstance(child, ast.If | ast.For | ast.While | ast.Try):
                info["complexity"] += 1

        return info

    def generate_function_docstring(self, func_info: dict[str, Any]) -> str:
        """Generate a docstring for a function based on analysis."""
        lines = []

        # Summary line
        summary = self._generate_summary(func_info)
        lines.append(f'"""{summary}')

        # Extended description for complex functions
        if func_info["complexity"] > 3 or len(func_info["args"]) > 3:
            lines.append("")
            lines.append(self._generate_extended_description(func_info))

        # Args section
        if func_info["args"]:
            lines.append("")
            lines.append("Args:")
            for arg in func_info["args"]:
                arg_desc = self._generate_arg_description(arg)
                if arg["type"]:
                    lines.append(f"    {arg['name']}: {arg_desc}")
                else:
                    lines.append(f"    {arg['name']}: {arg_desc}")

        # Returns section
        if func_info["returns"] or not func_info["is_property"]:
            lines.append("")
            lines.append("Returns:")
            returns_desc = self._generate_returns_description(func_info)
            lines.append(f"    {returns_desc}")

        # Raises section
        if func_info["raises"]:
            lines.append("")
            lines.append("Raises:")
            for exc in sorted(func_info["raises"]):
                exc_desc = self._generate_exception_description(exc)
                lines.append(f"    {exc}: {exc_desc}")

        # Yields section
        if func_info["has_yield"]:
            lines.append("")
            lines.append("Yields:")
            lines.append("    Generated values from the iteration.")

        # Examples section for public methods
        if not func_info["name"].startswith("_") and func_info["complexity"] > 2:
            lines.append("")
            lines.append("Examples:")
            lines.append(self._generate_example(func_info))

        lines.append('"""')
        return "\n".join(lines)

    def _generate_summary(self, func_info: dict[str, Any]) -> str:
        """Generate a one-line summary for a function."""
        name = func_info["name"]

        # Common patterns
        if name.startswith("get_"):
            return f"Get {name[4:].replace('_', ' ')}."
        if name.startswith("set_"):
            return f"Set {name[4:].replace('_', ' ')}."
        elif name.startswith("is_"):
            return f"Check if {name[3:].replace('_', ' ')}."
        elif name.startswith("has_"):
            return f"Check if has {name[4:].replace('_', ' ')}."
        elif name.startswith("create_"):
            return f"Create {name[7:].replace('_', ' ')}."
        elif name.startswith("update_"):
            return f"Update {name[7:].replace('_', ' ')}."
        elif name.startswith("delete_"):
            return f"Delete {name[7:].replace('_', ' ')}."
        elif name.startswith("validate_"):
            return f"Validate {name[9:].replace('_', ' ')}."
        elif name.startswith("process_"):
            return f"Process {name[8:].replace('_', ' ')}."
        elif name.startswith("handle_"):
            return f"Handle {name[7:].replace('_', ' ')}."
        elif name == "__init__":
            return "Initialize the instance."
        elif name == "__str__":
            return "Return string representation."
        elif name == "__repr__":
            return "Return detailed representation."
        elif func_info["is_property"]:
            return f"Get the {name.replace('_', ' ')} property."
        elif func_info["is_async"]:
            return f"Asynchronously {name.replace('_', ' ')}."
        else:
            return f"{name.replace('_', ' ').capitalize()}."

    def _generate_extended_description(self, func_info: dict[str, Any]) -> str:
        """Generate extended description for complex functions."""
        if func_info["is_async"]:
            return "This is an asynchronous function that should be awaited."
        if func_info["has_yield"]:
            return "This is a generator function that yields values lazily."
        elif func_info["complexity"] > 5:
            return "This function implements complex logic with multiple conditional branches."
        else:
            return f"This function processes {
    len(
        func_info['args'])} parameters to produce a result."

    def _generate_arg_description(self, arg: dict[str, Any]) -> str:
        """Generate description for an argument."""
        name = arg["name"]
        arg_type = arg["type"]

        # Type-based descriptions
        if arg_type:
            if "str" in arg_type:
                return f"The {name.replace('_', ' ')} string."
            if "int" in arg_type:
                return f"The {name.replace('_', ' ')} integer value."
            elif "float" in arg_type:
                return f"The {name.replace('_', ' ')} floating point value."
            elif "bool" in arg_type:
                return f"Whether to {name.replace('_', ' ')}."
            elif "List" in arg_type:
                return f"List of {name.replace('_', ' ')}."
            elif "Dict" in arg_type:
                return f"Dictionary containing {name.replace('_', ' ')}."
            elif "Optional" in arg_type:
                return f"Optional {name.replace('_', ' ')}."

        # Name-based descriptions
        if name == "config":
            return "Configuration dictionary."
        if name == "data":
            return "Input data to process."
        elif name == "context":
            return "Execution context."
        elif name == "callback":
            return "Callback function to invoke."
        elif name.endswith("_id"):
            return f"Unique identifier for {name[:-3].replace('_', ' ')}."
        elif name.endswith("_path"):
            return f"Path to {name[:-5].replace('_', ' ')}."
        elif name.endswith("_url"):
            return f"URL for {name[:-4].replace('_', ' ')}."
        else:
            return f"The {name.replace('_', ' ')}."

    def _generate_returns_description(self, func_info: dict[str, Any]) -> str:
        """Generate description for return value."""
        returns_type = func_info["returns"]
        name = func_info["name"]

        if returns_type:
            if returns_type == "None":
                return "None"
            if returns_type == "bool":
                return "True if successful, False otherwise."
            elif returns_type == "str":
                return "The resulting string."
            elif returns_type == "int":
                return "The calculated integer value."
            elif returns_type == "float":
                return "The calculated floating point value."
            elif "List" in returns_type:
                return "List of results."
            elif "Dict" in returns_type:
                return "Dictionary containing the results."
            elif "Optional" in returns_type:
                return "The result if found, None otherwise."
            else:
                return f"The {returns_type} result."

        # Name-based inference
        if name.startswith(("is_", "has_")):
            return "True if condition is met, False otherwise."
        if name.startswith(("get_", "find_")):
            return "The requested value or None if not found."
        elif name.startswith(("create_", "build_")):
            return "The newly created instance."
        elif func_info["is_property"]:
            return f"The {name.replace('_', ' ')} value."
        else:
            return "The processed result."

    def _generate_exception_description(self, exc_name: str) -> str:
        """Generate description for an exception."""
        common_exceptions = {
            "ValueError": "If the input value is invalid.",
            "TypeError": "If the input type is incorrect.",
            "KeyError": "If the required key is not found.",
            "AttributeError": "If the required attribute is missing.",
            "RuntimeError": "If a runtime error occurs.",
            "NotImplementedError": "If the feature is not implemented.",
            "FileNotFoundError": "If the specified file is not found.",
            "PermissionError": "If permission is denied.",
            "ConnectionError": "If connection fails.",
            "TimeoutError": "If operation times out.",
        }

        return common_exceptions.get(exc_name, f"If {exc_name} occurs.")

    def _generate_example(self, func_info: dict[str, Any]) -> str:
        """Generate a simple example for a function."""
        name = func_info["name"]
        args = func_info["args"]

        # Build example call
        if args:
            arg_examples = []
            for arg in args[:3]:  # Limit to first 3 args
                if arg["type"] and "str" in arg["type"]:
                    arg_examples.append(f'"{arg["name"]}_value"')
                elif arg["type"] and "int" in arg["type"]:
                    arg_examples.append("123")
                elif arg["type"] and "bool" in arg["type"]:
                    arg_examples.append("True")
                else:
                    arg_examples.append(f"{arg['name']}_value")

            args_str = ", ".join(arg_examples)
            example = f"    >>> result = {name}({args_str})"
        else:
            example = f"    >>> result = {name}()"

        if func_info["is_async"]:
            example = f"    >>> result = await {name}()"

        return example

    def analyze_class(self, node: ast.ClassDef) -> dict[str, Any]:
        """Analyze a class node to extract information."""
        info = {
            "name": node.name,
            "bases": [],
            "methods": [],
            "attributes": [],
            "is_dataclass": False,
            "is_pydantic": False,
        }

        # Extract base classes
        for base in node.bases:
            if isinstance(base, ast.Name):
                info["bases"].append(base.id)
                if base.id in ["BaseModel", "BaseSettings"]:
                    info["is_pydantic"] = True

        # Check decorators
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Name) and decorator.id == "dataclass":
                info["is_dataclass"] = True

        # Extract methods
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                info["methods"].append(item.name)

        return info

    def generate_class_docstring(self, class_info: dict[str, Any]) -> str:
        """Generate a docstring for a class."""
        lines = []
        name = class_info["name"]

        # Summary
        if class_info["is_pydantic"]:
            lines.append(f'"""{name} Pydantic model.')
        elif class_info["is_dataclass"]:
            lines.append(f'"""{name} dataclass.')
        elif class_info["bases"]:
            lines.append(f'"""{name} extending {", ".join(class_info["bases"])}.')
        else:
            lines.append(f'"""{name} implementation.')

        # Extended description
        lines.append("")
        if class_info["is_pydantic"]:
            lines.append("This model validates and serializes data using Pydantic.")
        elif class_info["is_dataclass"]:
            lines.append("This dataclass provides a convenient data container.")
        else:
            lines.append(
                f"This class implements {name.replace('_', ' ').lower()} functionality."
            )

        # Attributes section
        if class_info["attributes"]:
            lines.append("")
            lines.append("Attributes:")
            for attr in class_info["attributes"]:
                lines.append(f"    {attr}: Description of {attr}.")

        # Methods section
        if class_info["methods"]:
            public_methods = [m for m in class_info["methods"] if not m.startswith("_")]
            if public_methods:
                lines.append("")
                lines.append("Methods:")
                for method in public_methods[:5]:  # Limit to first 5
                    lines.append(
                        f"    {method}: {method.replace('_', ' ').capitalize()}."
                    )

        lines.append('"""')
        return "\n".join(lines)

    def generate_module_docstring(self, file_path: Path) -> str:
        """Generate a module-level docstring."""
        module_name = file_path.stem

        # Special cases
        if module_name == "__init__":
            parent = file_path.parent.name
            return f'"""Package initialization for {parent}."""'
        if module_name == "config":
            return '"""Configuration management module."""'
        elif module_name == "utils":
            return '"""Utility functions and helpers."""'
        elif module_name == "models":
            return '"""Data models and schemas."""'
        elif module_name == "exceptions":
            return '"""Custom exception definitions."""'
        elif module_name.startswith("test_"):
            return f'"""Tests for {module_name[5:].replace("_", " ")}."""'
        else:
            return f'"""{module_name.replace("_", " ").capitalize()} module."""'

    def process_file(self, file_path: Path, dry_run: bool = False) -> bool:
        """Process a single file to add docstrings."""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            # Parse AST
            tree = ast.parse(content)

            # Check if module docstring exists
            has_module_docstring = (
                isinstance(tree.body[0], ast.Expr)
                and isinstance(tree.body[0].value, ast.Constant)
                and isinstance(tree.body[0].value.value, str)
            )

            modifications = []

            # Add module docstring if missing
            if not has_module_docstring:
                module_doc = self.generate_module_docstring(file_path)
                modifications.append((0, 0, module_doc + "\n\n"))

            # Process functions and classes
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if not ast.get_docstring(node):
                        func_info = self.analyze_function(node)
                        docstring = self.generate_function_docstring(func_info)
                        # Calculate indentation
                        indent = "    " * (node.col_offset // 4)
                        modifications.append(
                            (node.lineno, node.col_offset, f"{indent}{docstring}")
                        )
                        self.generated_count += 1

                elif isinstance(node, ast.ClassDef) and not ast.get_docstring(node):
                    class_info = self.analyze_class(node)
                    docstring = self.generate_class_docstring(class_info)
                    indent = "    " * (node.col_offset // 4)
                    modifications.append(
                        (node.lineno, node.col_offset, f"{indent}{docstring}")
                    )
                    self.generated_count += 1

            if modifications and not dry_run:
                # Apply modifications
                lines = content.split("\n")

                # Sort by line number (descending) to avoid offset issues
                modifications.sort(key=lambda x: x[0], reverse=True)

                for line_no, _col_offset, docstring in modifications:
                    if line_no == 0:
                        # Module docstring
                        lines.insert(0, docstring)
                    else:
                        # Function/class docstring
                        # Insert after the definition line
                        lines.insert(line_no, docstring)

                # Write back
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write("\n".join(lines))

                return True

            return bool(modifications)

        except Exception as e:
            return False


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Generate docstrings automatically")
    parser.add_argument("target", help="File or directory to process")
    parser.add_argument(
        "--dry-run", action="store_true", help="Show what would be done"
    )

    args = parser.parse_args()

    generator = DocstringGenerator()
    target = Path(args.target)

    if target.is_file():
        if generator.process_file(target, args.dry_run):
            pass")
    elif target.is_dir():
        files = list(target.rglob("*.py"))
        for file in files:
            if "__pycache__" not in str(file):
                if generator.process_file(file, args.dry_run):
                    pass")



if __name__ == "__main__":
    main()
