#!/usr/bin/env python3
"""Function Docstring Automation Script.

This script automatically adds missing docstrings to Python functions
across the Haive codebase, using intelligent analysis to generate
appropriate documentation.

Usage:
    python add_function_docstrings.py <packages_dir> [--limit N]
"""

import ast
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class FunctionAnalyzer:
    """Analyze Python functions to generate intelligent docstrings."""

    def __init__(self, file_path: Path):
        """Initialize analyzer with file path."""
        self.file_path = file_path
        self.tree = None
        self.source_lines = []

    def analyze_file(self) -> list[dict]:
        """Analyze file and return functions needing docstrings."""
        try:
            with open(self.file_path, encoding="utf-8") as f:
                content = f.read()
                self.source_lines = content.splitlines()

            self.tree = ast.parse(content)
            functions_needing_docs = []

            for node in ast.walk(self.tree):
                if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                    if self._needs_docstring(node):
                        func_info = self._analyze_function(node)
                        functions_needing_docs.append(func_info)

            return functions_needing_docs

        except Exception as e:
            return []

    def _needs_docstring(self, node: ast.FunctionDef) -> bool:
        """Check if function needs a docstring."""
        # Skip private functions unless they're special methods
        if node.name.startswith("_") and not node.name.startswith("__"):
            return False

        # Check if docstring already exists
        return not (node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant) and isinstance(node.body[0].value.value, str))

    def _analyze_function(self, node: ast.FunctionDef) -> dict:
        """Analyze function and extract information for docstring generation."""
        # Extract parameters
        args = []
        for arg in node.args.args:
            arg_info = {"name": arg.arg, "type": None, "default": None}
            if arg.annotation:
                arg_info["type"] = ast.unparse(arg.annotation)
            args.append(arg_info)

        # Extract defaults
        defaults = node.args.defaults
        if defaults:
            num_defaults = len(defaults)
            for i, default in enumerate(defaults):
                arg_index = len(args) - num_defaults + i
                if arg_index >= 0:
                    args[arg_index]["default"] = ast.unparse(default)

        # Extract return type
        return_type = None
        if node.returns:
            return_type = ast.unparse(node.returns)

        # Analyze function body for patterns
        body_analysis = self._analyze_function_body(node)

        return {
            "name": node.name,
            "lineno": node.lineno,
            "is_async": isinstance(node, ast.AsyncFunctionDef),
            "args": args,
            "return_type": return_type,
            "body_analysis": body_analysis,
            "is_property": self._is_property(node),
            "is_classmethod": self._is_classmethod(node),
            "is_staticmethod": self._is_staticmethod(node),
        }

    def _analyze_function_body(self, node: ast.FunctionDef) -> dict:
        """Analyze function body to understand what it does."""
        analysis = {
            "has_return": False,
            "has_yield": False,
            "raises_exceptions": [],
            "calls_methods": [],
            "complexity": "simple",
        }

        for child in ast.walk(node):
            if isinstance(child, ast.Return) and child.value is not None:
                analysis["has_return"] = True
            elif isinstance(child, ast.Yield | ast.YieldFrom):
                analysis["has_yield"] = True
            elif isinstance(child, ast.Raise) and child.exc:
                if isinstance(child.exc, ast.Name):
                    analysis["raises_exceptions"].append(child.exc.id)
                elif isinstance(child.exc, ast.Call) and isinstance(
                    child.exc.func, ast.Name
                ):
                    analysis["raises_exceptions"].append(child.exc.func.id)
            elif isinstance(child, ast.Call) and isinstance(child.func, ast.Attribute):
                analysis["calls_methods"].append(child.func.attr)

        # Determine complexity
        if len(list(ast.walk(node))) > 20:
            analysis["complexity"] = "complex"
        elif len(list(ast.walk(node))) > 10:
            analysis["complexity"] = "moderate"

        return analysis

    def _is_property(self, node: ast.FunctionDef) -> bool:
        """Check if function is a property."""
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Name) and decorator.id == "property":
                return True
        return False

    def _is_classmethod(self, node: ast.FunctionDef) -> bool:
        """Check if function is a classmethod."""
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Name) and decorator.id == "classmethod":
                return True
        return False

    def _is_staticmethod(self, node: ast.FunctionDef) -> bool:
        """Check if function is a staticmethod."""
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Name) and decorator.id == "staticmethod":
                return True
        return False


def generate_function_docstring(func_info: dict) -> str:
    """Generate a comprehensive docstring for a function."""
    name = func_info["name"]
    args = func_info["args"]
    return_type = func_info["return_type"]
    body_analysis = func_info["body_analysis"]
    is_async = func_info["is_async"]
    is_property = func_info["is_property"]

    # Generate brief description
    if is_property:
        brief = f"Get the {name.replace('_', ' ').strip()}."
    elif name.startswith("set_"):
        brief = f"Set the {name[4:].replace('_', ' ').strip()}."
    elif name.startswith("get_"):
        brief = f"Get the {name[4:].replace('_', ' ').strip()}."
    elif name.startswith(("is_", "has_")):
        brief = f"Check if {name[3:].replace('_', ' ').strip() if name.startswith('is_') else name[4:].replace('_', ' ').strip()}."
    elif name.startswith("create_"):
        brief = f"Create a new {name[7:].replace('_', ' ').strip()}."
    elif name.startswith("delete_"):
        brief = f"Delete the {name[7:].replace('_', ' ').strip()}."
    elif name.startswith("update_"):
        brief = f"Update the {name[7:].replace('_', ' ').strip()}."
    elif name.startswith("validate_"):
        brief = f"Validate the {name[9:].replace('_', ' ').strip()}."
    elif name.startswith("process_"):
        brief = f"Process the {name[8:].replace('_', ' ').strip()}."
    elif name == "__init__":
        brief = "Initialize the instance."
    elif name == "__str__":
        brief = "Return string representation."
    elif name == "__repr__":
        brief = "Return detailed string representation."
    else:
        # Generic description based on function name
        words = name.replace("_", " ").strip()
        brief = f"Execute {words} operation."

    # Build docstring
    docstring_parts = [f'"""{brief}']

    # Add more detailed description if complex
    if body_analysis["complexity"] != "simple":
        docstring_parts.append(
            f"\n    TODO: Add detailed description of {name} functionality."
        )

    # Add async note
    if is_async:
        docstring_parts.append(
            "\n    This is an async function that should be awaited."
        )

    # Args section
    if (args and args[0]["name"] != "self") or len(args) > 1:
        docstring_parts.append("\n    Args:")
        for arg in args:
            if arg["name"] == "self":
                continue
            arg_desc = f"        {arg['name']}"
            if arg["type"]:
                arg_desc += f" ({arg['type']})"
            arg_desc += f": TODO: Add description for {arg['name']}"
            if arg["default"]:
                arg_desc += f" (default: {arg['default']})"
            arg_desc += "."
            docstring_parts.append(arg_desc)

    # Returns section
    if body_analysis["has_return"] or return_type:
        docstring_parts.append("\n    Returns:")
        if return_type:
            docstring_parts.append(
                f"        {return_type}: TODO: Add description of return value."
            )
        else:
            docstring_parts.append("        TODO: Add description of return value.")

    # Yields section
    if body_analysis["has_yield"]:
        docstring_parts.append("\n    Yields:")
        docstring_parts.append("        TODO: Add description of yielded values.")

    # Raises section
    if body_analysis["raises_exceptions"]:
        docstring_parts.append("\n    Raises:")
        for exc in set(body_analysis["raises_exceptions"]):
            docstring_parts.append(
                f"        {exc}: TODO: Add description of when this exception is raised."
            )

    # Example section
    if not is_property and not name.startswith("__"):
        docstring_parts.append("\n    Example:")
        if is_async:
            docstring_parts.append(
                f"        >>> result = await {name}({', '.join(['param' for arg in args if arg['name'] != 'self'])})"
            )
        else:
            docstring_parts.append(
                f"        >>> result = {name}({', '.join(['param' for arg in args if arg['name'] != 'self'])})"
            )

    docstring_parts.append('    """')

    return "\n".join(docstring_parts)


def add_docstring_to_function(file_path: Path, func_info: dict) -> bool:
    """Add docstring to a specific function in a file."""
    try:
        with open(file_path, encoding="utf-8") as f:
            lines = f.readlines()

        # Find the function line
        func_line = func_info["lineno"] - 1  # Convert to 0-based index

        # Generate docstring
        docstring = generate_function_docstring(func_info)

        # Determine indentation
        func_def_line = lines[func_line]
        indent = len(func_def_line) - len(func_def_line.lstrip())

        # Indent the docstring
        docstring_lines = docstring.split("\n")
        indented_docstring = []
        for i, line in enumerate(docstring_lines):
            if i == 0:
                indented_docstring.append(" " * (indent + 4) + line)
            else:
                indented_docstring.append(" " * (indent + 4) + line)

        # Insert docstring after function definition
        insert_line = func_line + 1
        # Skip any decorators or multiline function definitions
        while insert_line < len(lines) and (
            lines[insert_line].strip().endswith(":") or not lines[insert_line].strip()
        ):
            if lines[insert_line].strip().endswith(":"):
                insert_line += 1
                break
            insert_line += 1

        # Insert the docstring
        for i, line in enumerate(indented_docstring):
            lines.insert(insert_line + i, line + "\n")

        # Write back to file
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(lines)

        return True

    except Exception as e:
        return False


def main():
    """Main execution function."""
    if len(sys.argv) < 2:
        sys.exit(1)

    packages_dir = Path(sys.argv[1])
    limit = None

    if "--limit" in sys.argv:
        limit_index = sys.argv.index("--limit") + 1
        if limit_index < len(sys.argv):
            limit = int(sys.argv[limit_index])

    if not packages_dir.exists():
        sys.exit(1)


    # Find Python files (exclude tests and examples)
    py_files = []
    for pattern in ["**/*.py"]:
        py_files.extend(packages_dir.rglob(pattern))

    # Filter files
    py_files = [
        f
        for f in py_files
        if "/tests/" not in str(f)
        and "/examples/" not in str(f)
        and "/.venv/" not in str(f)
        and "/site-packages/" not in str(f)
        and "test_" not in f.name
        and f.name != "__pycache__"
    ]

    if limit:
        py_files = py_files[:limit]


    total_functions_processed = 0
    files_modified = 0

    for file_path in py_files:
        analyzer = FunctionAnalyzer(file_path)
        functions_needing_docs = analyzer.analyze_file()

        if functions_needing_docs:
            file_modified = False

            # Sort functions by line number (process from bottom to top)
            functions_needing_docs.sort(key=lambda x: x["lineno"], reverse=True)

            for func_info in functions_needing_docs:
                if add_docstring_to_function(file_path, func_info):
                    total_functions_processed += 1
                    file_modified = True
                else:
                    print("pass")

            if file_modified:
                files_modified += 1



if __name__ == "__main__":
    main()