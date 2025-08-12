"""D107 Fixer: Add missing __init__ method docstrings with parameter analysis.

This fixer uses AST parsing to analyze __init__ method signatures and generate
appropriate docstrings with Args sections for missing D107 pydocstyle errors.
"""

import ast
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from .base_fixer import BaseFixer


class D107Fixer(BaseFixer):
    """Fixer for D107: Missing __init__ method docstring.

    This fixer analyzes __init__ method signatures using AST parsing to understand
    the parameters and their types, then generates appropriate docstrings with
    proper Args sections.

    Examples:
        Simple __init__ method:

        Before:
            def __init__(self, name: str, value: int = 0):
                self.name = name
                self.value = value

        After:
            def __init__(self, name: str, value: int = 0):
                \"\"\"Initialize instance.

                Args:
                    name: The name value.
                    value: The value setting (default: 0).
                \"\"\"
                self.name = name
                self.value = value
    """

    def __init__(self):
        """Initialize D107 fixer."""
        super().__init__(
            error_codes=["D107"],
            description="Add missing __init__ method docstrings with parameter analysis",
        )

    def fix_content(self, content: str) -> Tuple[str, int, List[str]]:
        """Fix D107 issues in content.

        Args:
            content: Original file content.

        Returns:
            Tuple of (fixed_content, fixes_count, list_of_changes_made).
        """
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return content, 0, []

        # Find all __init__ methods without docstrings
        missing_init_docstrings = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                for item in node.body:
                    if (
                        isinstance(item, ast.FunctionDef)
                        and item.name == "__init__"
                        and ast.get_docstring(item) is None
                    ):
                        missing_init_docstrings.append(
                            {
                                "class_name": node.name,
                                "method_node": item,
                                "line_number": item.lineno,
                            }
                        )

        if not missing_init_docstrings:
            return content, 0, []

        # Sort by line number in reverse order so we can insert from bottom up
        missing_init_docstrings.sort(key=lambda x: x["line_number"], reverse=True)

        lines = content.split("\n")
        fixes_count = 0
        changes = []

        for init_info in missing_init_docstrings:
            method_node = init_info["method_node"]
            class_name = init_info["class_name"]

            # Generate docstring for this __init__
            docstring = self._generate_init_docstring(method_node, class_name)

            # Find insertion point (after method definition line)
            method_line_idx = method_node.lineno - 1  # AST is 1-indexed

            # Find the method definition line (handle multi-line definitions)
            insert_line_idx = method_line_idx
            while insert_line_idx < len(lines) and not lines[
                insert_line_idx
            ].rstrip().endswith(":"):
                insert_line_idx += 1

            # Insert docstring with proper indentation
            method_indent = self._get_method_indent(lines[method_line_idx])
            docstring_indent = method_indent + "    "  # One more level of indentation

            docstring_lines = docstring.split("\n")
            indented_docstring = []
            for ds_line in docstring_lines:
                if ds_line.strip():
                    indented_docstring.append(docstring_indent + ds_line)
                else:
                    indented_docstring.append("")

            # Insert after the method definition
            for i, ds_line in enumerate(reversed(indented_docstring)):
                lines.insert(insert_line_idx + 1, ds_line)

            fixes_count += 1
            changes.append(f"Added __init__ docstring for {class_name}.__init__")

        return "\n".join(lines), fixes_count, changes

    def _generate_init_docstring(
        self, method_node: ast.FunctionDef, class_name: str
    ) -> str:
        """Generate appropriate __init__ docstring based on method signature.

        Args:
            method_node: AST node for the __init__ method.
            class_name: Name of the containing class.

        Returns:
            Generated docstring for the __init__ method.
        """
        # Analyze method arguments
        args_info = self._analyze_init_arguments(method_node)

        if not args_info:
            # Simple case with just self
            return f'"""Initialize {class_name} instance."""'

        # Build docstring with Args section
        lines = [f'"""Initialize {class_name} instance.']
        lines.append("")
        lines.append("Args:")

        for arg_info in args_info:
            arg_line = f"    {arg_info['name']}: {arg_info['description']}"
            if arg_info["has_default"]:
                arg_line += f" (default: {arg_info['default_desc']})."
            else:
                arg_line += "."
            lines.append(arg_line)

        lines.append('"""')

        return "\n".join(lines)

    def _analyze_init_arguments(
        self, method_node: ast.FunctionDef
    ) -> List[Dict[str, Any]]:
        """Analyze __init__ method arguments to generate descriptions.

        Args:
            method_node: AST node for the __init__ method.

        Returns:
            List of argument information dictionaries.
        """
        args_info = []
        args = method_node.args

        # Skip 'self' parameter
        arg_names = [arg.arg for arg in args.args[1:]]  # Skip self
        arg_annotations = [getattr(arg, "annotation", None) for arg in args.args[1:]]

        # Handle defaults
        defaults = args.defaults or []
        num_defaults = len(defaults)
        num_args = len(arg_names)

        for i, (name, annotation) in enumerate(zip(arg_names, arg_annotations)):
            # Check if this argument has a default value
            default_index = i - (num_args - num_defaults)
            has_default = default_index >= 0

            arg_info = {
                "name": name,
                "has_default": has_default,
                "annotation": annotation,
                "description": self._generate_arg_description(name, annotation),
                "default_desc": (
                    self._get_default_description(defaults[default_index])
                    if has_default
                    else None
                ),
            }

            args_info.append(arg_info)

        return args_info

    def _generate_arg_description(
        self, name: str, annotation: Optional[ast.AST]
    ) -> str:
        """Generate description for an argument based on name and type annotation.

        Args:
            name: Argument name.
            annotation: Type annotation AST node.

        Returns:
            Generated description for the argument.
        """
        # Common argument name patterns
        name_patterns = {
            "name": "The name value",
            "id": "Identifier value",
            "value": "The value setting",
            "config": "Configuration settings",
            "path": "File or directory path",
            "file_path": "Path to file",
            "data": "Data to process",
            "text": "Text content",
            "content": "Content to process",
            "url": "URL address",
            "host": "Host address",
            "port": "Port number",
            "username": "Username for authentication",
            "password": "Password for authentication",
            "token": "Authentication token",
            "key": "Key value",
            "timeout": "Timeout duration",
            "max_retries": "Maximum retry attempts",
            "debug": "Enable debug mode",
            "verbose": "Enable verbose output",
            "force": "Force operation",
            "recursive": "Process recursively",
            "overwrite": "Overwrite existing files",
        }

        # Try exact match first
        if name in name_patterns:
            return name_patterns[name]

        # Try pattern matching
        if name.endswith("_path"):
            return f"Path to {name[:-5].replace('_', ' ')}"
        elif name.endswith("_file"):
            return f"File for {name[:-5].replace('_', ' ')}"
        elif name.endswith("_dir"):
            return f"Directory for {name[:-4].replace('_', ' ')}"
        elif name.startswith("is_"):
            return f"Whether to {name[3:].replace('_', ' ')}"
        elif name.startswith("enable_"):
            return f"Enable {name[7:].replace('_', ' ')}"
        elif name.startswith("disable_"):
            return f"Disable {name[8:].replace('_', ' ')}"
        elif name.startswith("max_"):
            return f"Maximum {name[4:].replace('_', ' ')}"
        elif name.startswith("min_"):
            return f"Minimum {name[4:].replace('_', ' ')}"

        # Use type annotation if available
        if annotation:
            type_desc = self._annotation_to_description(annotation)
            if type_desc:
                return f"The {name.replace('_', ' ')} {type_desc}"

        # Fallback
        return f"The {name.replace('_', ' ')} parameter"

    def _annotation_to_description(self, annotation: ast.AST) -> str:
        """Convert type annotation to descriptive text.

        Args:
            annotation: Type annotation AST node.

        Returns:
            Description based on type.
        """
        if isinstance(annotation, ast.Name):
            type_names = {
                "str": "string",
                "int": "integer",
                "float": "floating point number",
                "bool": "boolean flag",
                "list": "list",
                "dict": "dictionary",
                "set": "set",
                "tuple": "tuple",
            }
            return type_names.get(annotation.id, annotation.id.lower())
        elif isinstance(annotation, ast.Attribute):
            return "object"
        elif isinstance(annotation, ast.Subscript):
            return "collection"

        return ""

    def _get_default_description(self, default_node: ast.AST) -> str:
        """Get description of default value.

        Args:
            default_node: AST node for default value.

        Returns:
            String description of the default.
        """
        if isinstance(default_node, ast.Constant):
            if default_node.value is None:
                return "None"
            elif isinstance(default_node.value, str):
                return f'"{default_node.value}"'
            else:
                return str(default_node.value)
        elif isinstance(default_node, ast.Name):
            return default_node.id
        elif isinstance(default_node, ast.List):
            return "[]"
        elif isinstance(default_node, ast.Dict):
            return "{}"
        else:
            return "default"

    def _get_method_indent(self, line: str) -> str:
        """Get indentation of method definition line.

        Args:
            line: Line containing method definition.

        Returns:
            Indentation string.
        """
        return line[: len(line) - len(line.lstrip())]

    def preview_fixes(
        self, content: str, context_lines: int = 5
    ) -> List[Dict[str, Any]]:
        """Preview what fixes would be applied without making changes.

        Args:
            content: Content to analyze.
            context_lines: Number of context lines to show.

        Returns:
            List of preview dictionaries with line numbers and changes.
        """
        previews = []

        try:
            tree = ast.parse(content)
        except SyntaxError:
            return previews

        lines = content.split("\n")

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                for item in node.body:
                    if (
                        isinstance(item, ast.FunctionDef)
                        and item.name == "__init__"
                        and ast.get_docstring(item) is None
                    ):

                        # Generate preview
                        docstring = self._generate_init_docstring(item, node.name)
                        method_line_idx = item.lineno - 1

                        # Build context
                        start_line = max(0, method_line_idx - context_lines)
                        end_line = min(len(lines), method_line_idx + context_lines + 3)

                        context = []
                        for i in range(start_line, end_line):
                            if i < len(lines):
                                prefix = "   " if i != method_line_idx + 1 else "+++"
                                context.append(f"{prefix} {i+1:3}: {lines[i]}")

                        # Add preview of docstring
                        method_indent = self._get_method_indent(lines[method_line_idx])
                        docstring_indent = method_indent + "    "
                        docstring_lines = docstring.split("\n")

                        for j, ds_line in enumerate(docstring_lines):
                            if ds_line.strip():
                                preview_line = docstring_indent + ds_line
                            else:
                                preview_line = ""
                            context.append(
                                f"+++ {method_line_idx + j + 2:3}: {preview_line}"
                            )

                        args_info = self._analyze_init_arguments(item)

                        previews.append(
                            {
                                "line_number": item.lineno,
                                "class_name": node.name,
                                "method_name": "__init__",
                                "args_count": len(args_info),
                                "has_type_annotations": any(
                                    arg.get("annotation") for arg in args_info
                                ),
                                "docstring_preview": docstring.split("\n")[0],
                                "context": "\n".join(context),
                            }
                        )

        return previews
