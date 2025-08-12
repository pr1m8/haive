"""D100 Fixer: Add missing module docstrings with template insertion.

This fixer analyzes module content to generate appropriate docstrings for
Python modules that are missing them (D100 pydocstyle errors).
"""

import ast
import re
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

from .base_fixer import BaseFixer


class D100Fixer(BaseFixer):
    """Fixer for D100: Missing module docstring.

    This fixer analyzes the module content using AST parsing to understand
    what the module contains (classes, functions, imports) and generates
    appropriate module docstrings based on the content.

    Examples:
        Module with classes and functions gets comprehensive docstring:

        Before:
            import os
            class MyClass: pass
            def my_func(): pass

        After:
            \"\"\"Module containing MyClass and utility functions.

            This module provides MyClass for object management and
            utility functions for data processing.
            \"\"\"
            import os
            class MyClass: pass
            def my_func(): pass
    """

    def __init__(self):
        """Initialize D100 fixer."""
        super().__init__(
            error_codes=["D100"],
            description="Add missing module docstrings with template insertion",
        )

    def fix_content(self, content: str) -> Tuple[str, int, List[str]]:
        """Fix D100 issues in content.

        Args:
            content: Original file content.

        Returns:
            Tuple of (fixed_content, fixes_count, list_of_changes_made).
        """
        # Check if module already has docstring
        if self._has_module_docstring(content):
            return content, 0, []

        # Analyze module content to generate appropriate docstring
        module_info = self._analyze_module_content(content)

        if not module_info:
            # Skip empty or parse-error modules
            return content, 0, []

        # Generate docstring based on content
        docstring = self._generate_module_docstring(module_info)

        # Insert docstring at appropriate location
        fixed_content = self._insert_module_docstring(content, docstring)

        changes = [f"Added module docstring: {docstring.split('.')[0]}..."]

        return fixed_content, 1, changes

    def _has_module_docstring(self, content: str) -> bool:
        """Check if module already has a docstring.

        Args:
            content: Module content to check.

        Returns:
            True if module docstring exists.
        """
        try:
            tree = ast.parse(content)
            return ast.get_docstring(tree) is not None
        except SyntaxError:
            # If can't parse, assume no docstring to be safe
            return False

    def _analyze_module_content(self, content: str) -> Dict[str, Any]:
        """Analyze module content to understand what it contains.

        Args:
            content: Module content to analyze.

        Returns:
            Dictionary with module analysis results.
        """
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return {}

        analysis = {
            "classes": [],
            "functions": [],
            "imports": [],
            "constants": [],
            "has_main": False,
            "complexity": "simple",  # simple, moderate, complex
        }

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                analysis["classes"].append(
                    {
                        "name": node.name,
                        "is_private": node.name.startswith("_"),
                        "has_docstring": ast.get_docstring(node) is not None,
                        "methods": len(
                            [n for n in node.body if isinstance(n, ast.FunctionDef)]
                        ),
                    }
                )

            elif isinstance(node, ast.FunctionDef):
                # Only count top-level functions
                if (
                    isinstance(node, ast.FunctionDef)
                    and hasattr(tree, "body")
                    and node in tree.body
                ):
                    analysis["functions"].append(
                        {
                            "name": node.name,
                            "is_private": node.name.startswith("_"),
                            "is_main": node.name == "main",
                            "has_docstring": ast.get_docstring(node) is not None,
                        }
                    )
                    if node.name == "main":
                        analysis["has_main"] = True

            elif isinstance(node, ast.Import):
                for alias in node.names:
                    analysis["imports"].append(alias.name)

            elif isinstance(node, ast.ImportFrom) and node.module:
                analysis["imports"].append(node.module)

            elif isinstance(node, ast.Assign):
                # Look for module-level constants (ALL_CAPS)
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id.isupper():
                        analysis["constants"].append(target.id)

        # Determine complexity
        total_items = len(analysis["classes"]) + len(analysis["functions"])
        if total_items > 10:
            analysis["complexity"] = "complex"
        elif total_items > 3:
            analysis["complexity"] = "moderate"

        return analysis

    def _generate_module_docstring(self, module_info: Dict[str, Any]) -> str:
        """Generate appropriate module docstring based on content analysis.

        Args:
            module_info: Analysis results from _analyze_module_content.

        Returns:
            Generated module docstring.
        """
        classes = module_info["classes"]
        functions = module_info["functions"]
        has_main = module_info["has_main"]
        complexity = module_info["complexity"]

        # Determine primary purpose
        if has_main:
            primary_type = "script"
        elif classes and not functions:
            primary_type = "classes"
        elif functions and not classes:
            primary_type = "utilities"
        elif classes and functions:
            primary_type = "mixed"
        else:
            primary_type = "module"

        # Generate summary line
        if primary_type == "script":
            summary = "Command-line script for automated processing."
        elif primary_type == "classes":
            if len(classes) == 1:
                class_name = classes[0]["name"]
                summary = f"Module containing {class_name} class."
            else:
                summary = (
                    f"Module containing {len(classes)} classes for object management."
                )
        elif primary_type == "utilities":
            summary = "Utility functions and helper methods."
        elif primary_type == "mixed":
            summary = f"Module with {len(classes)} classes and {len(functions)} utility functions."
        else:
            summary = "Module for specialized functionality."

        # Build docstring
        lines = [f'"""{summary}']

        # Add detailed description for complex modules
        if complexity in ["moderate", "complex"]:
            lines.append("")

            if classes:
                class_names = [c["name"] for c in classes if not c["is_private"]]
                if class_names:
                    if len(class_names) == 1:
                        lines.append(
                            f"This module provides the {class_names[0]} class for"
                        )
                        lines.append("core functionality and data management.")
                    else:
                        lines.append("This module provides classes for:")
                        for name in class_names[:3]:  # Limit to first 3
                            lines.append(f"- {name}: Core functionality")
                        if len(class_names) > 3:
                            lines.append(
                                f"- And {len(class_names) - 3} additional classes"
                            )

            if functions:
                func_names = [
                    f["name"]
                    for f in functions
                    if not f["is_private"] and f["name"] != "main"
                ]
                if func_names and len(func_names) > 1:
                    lines.append("")
                    lines.append("Key functions:")
                    for name in func_names[:3]:  # Limit to first 3
                        lines.append(f"- {name}(): Data processing")
                    if len(func_names) > 3:
                        lines.append(
                            f"- And {len(func_names) - 3} additional utilities"
                        )

        # Add usage example for scripts
        if has_main and complexity != "simple":
            lines.append("")
            lines.append("Usage:")
            lines.append("    python -m module_name [arguments]")

        lines.append('"""')

        return "\n".join(lines)

    def _insert_module_docstring(self, content: str, docstring: str) -> str:
        """Insert module docstring at appropriate location.

        Args:
            content: Original module content.
            docstring: Generated docstring to insert.

        Returns:
            Content with docstring inserted.
        """
        lines = content.split("\n")
        insert_index = 0

        # Skip shebang line
        if lines and lines[0].startswith("#!"):
            insert_index = 1

        # Skip encoding declarations
        for i in range(insert_index, min(len(lines), insert_index + 2)):
            if lines[i].strip() and ("coding" in lines[i] or "encoding" in lines[i]):
                insert_index = i + 1

        # Insert docstring with proper spacing
        lines.insert(insert_index, docstring)

        # Ensure proper spacing after docstring
        if insert_index + 1 < len(lines) and lines[insert_index + 1].strip():
            lines.insert(insert_index + 1, "")

        return "\n".join(lines)

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
        if self._has_module_docstring(content):
            return []

        module_info = self._analyze_module_content(content)
        if not module_info:
            return []

        docstring = self._generate_module_docstring(module_info)
        lines = content.split("\n")

        # Find insertion point
        insert_index = 0
        if lines and lines[0].startswith("#!"):
            insert_index = 1

        for i in range(insert_index, min(len(lines), insert_index + 2)):
            if lines[i].strip() and ("coding" in lines[i] or "encoding" in lines[i]):
                insert_index = i + 1

        # Build context
        start_line = max(0, insert_index - context_lines)
        end_line = min(len(lines), insert_index + context_lines)

        context = []
        for i in range(start_line, end_line):
            if i < len(lines):
                prefix = "   " if i != insert_index else "+++"
                context.append(f"{prefix} {i+1:3}: {lines[i]}")

        # Insert the new docstring in preview
        docstring_lines = docstring.split("\n")
        for j, ds_line in enumerate(docstring_lines):
            context.append(f"+++ {insert_index + j + 1:3}: {ds_line}")

        return [
            {
                "line_number": insert_index + 1,
                "change_type": "insert_module_docstring",
                "classes_found": len(module_info["classes"]),
                "functions_found": len(module_info["functions"]),
                "docstring_preview": docstring.split("\n")[0],
                "context": "\n".join(context),
            }
        ]
