#!/usr/bin/env python3
"""Automated type hint fixer with smart pattern recognition.

This script applies automated type hint fixes to Python files based on
intelligent analysis of function signatures and naming patterns.
"""

import argparse
import ast
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class TypeHintFixer:
    """Apply automated type hint fixes to Python code."""

    def __init__(self):
        self.fixes_applied = 0
        self.files_modified = 0

        # Import suggestions based on common patterns
        self.common_imports = {
            "List": "from typing import List",
            "Dict": "from typing import Dict",
            "Optional": "from typing import Optional",
            "Union": "from typing import Union",
            "Any": "from typing import Any",
            "Tuple": "from typing import Tuple",
            "Callable": "from typing import Callable",
        }

    def fix_function_signature(self, file_path: Path, dry_run: bool = True) -> bool:
        """Fix type hints in a single file."""
        try:
            with open(file_path, encoding="utf-8") as f:
                original_content = f.read()

            # Parse the AST
            tree = ast.parse(original_content)

            # Find functions that need fixes
            fixes = self._identify_fixes(tree, original_content)

            if not fixes:
                return False

            # Apply fixes to content
            modified_content = self._apply_fixes(original_content, fixes)

            if dry_run:
                for _fix in fixes[:3]:  # Show first 3
                    pass
                return True
            # Write the modified content
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(modified_content)

            self.fixes_applied += len(fixes)
            self.files_modified += 1
            return True

        except Exception:
            return False

    def _identify_fixes(self, tree: ast.AST, content: str) -> list[dict]:
        """Identify functions that need type hint fixes."""
        fixes = []
        lines = content.split("\n")

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                fix = self._analyze_function_for_fixes(node, lines)
                if fix:
                    fixes.append(fix)

        return fixes

    def _analyze_function_for_fixes(
        self, node: ast.FunctionDef, lines: list[str]
    ) -> dict | None:
        """Analyze a function to determine what fixes are needed."""
        # Skip private methods (except __init__)
        if node.name.startswith("_") and node.name not in ["__init__", "__call__"]:
            return None

        # Get the original function signature line
        func_line_idx = node.lineno - 1
        original_line = lines[func_line_idx]

        # Check what's missing
        missing_params = []
        for arg in node.args.args:
            if arg.annotation is None and arg.arg not in ["self", "cls"]:
                suggested_type = self._suggest_param_type(arg.arg, node.name)
                if suggested_type:
                    missing_params.append({"name": arg.arg, "type": suggested_type})

        # Check return type
        missing_return = None
        if node.returns is None:
            suggested_return = self._suggest_return_type(node)
            if suggested_return:
                missing_return = suggested_return

        if missing_params or missing_return:
            return {
                "line": node.lineno,
                "function_name": node.name,
                "original_line": original_line.strip(),
                "missing_params": missing_params,
                "missing_return": missing_return,
                "description": self._generate_fix_description(
                    node.name, missing_params, missing_return
                ),
            }

        return None

    def _suggest_param_type(self, param_name: str, func_name: str) -> str | None:
        """Suggest parameter type based on naming patterns."""
        # Enhanced pattern matching
        patterns = {
            # Configuration and data
            "config": "Dict[str, Any]",
            "data": "Dict[str, Any]",
            "kwargs": "Any",
            "params": "Dict[str, Any]",
            "options": "Dict[str, Any]",
            "settings": "Dict[str, Any]",
            # Strings
            "name": "str",
            "text": "str",
            "content": "str",
            "message": "str",
            "query": "str",
            "prompt": "str",
            "input": "str",
            "output": "str",
            "response": "str",
            "path": "str",
            "url": "str",
            "key": "str",
            "value": "str",
            "token": "str",
            "model": "str",
            "provider": "str",
            # Numbers
            "count": "int",
            "size": "int",
            "limit": "int",
            "offset": "int",
            "max_tokens": "int",
            "temperature": "float",
            "threshold": "float",
            "timeout": "float",
            "score": "float",
            # Booleans
            "enabled": "bool",
            "active": "bool",
            "debug": "bool",
            "strict": "bool",
            "force": "bool",
            "async": "bool",
            "validate": "bool",
            # Collections
            "items": "List[Any]",
            "results": "List[Any]",
            "tools": "List[str]",
            "messages": "List[Dict[str, Any]]",
            "headers": "Dict[str, str]",
            "metadata": "Dict[str, Any]",
            "context": "Dict[str, Any]",
            "state": "Dict[str, Any]",
        }

        # Exact match
        if param_name in patterns:
            return patterns[param_name]

        # Suffix patterns
        if param_name.endswith("_id"):
            return "str"
        if param_name.endswith("_list"):
            return "List[Any]"
        if param_name.endswith("_dict"):
            return "Dict[str, Any]"
        if param_name.endswith("_count"):
            return "int"
        elif param_name.endswith(("_enabled", "_flag")):
            return "bool"
        elif param_name.endswith("_config"):
            return "Dict[str, Any]"

        # Agent-specific patterns
        if "agent" in param_name.lower():
            return "Any"  # Agent types vary

        # LLM-specific patterns
        if any(term in param_name.lower() for term in ["llm", "model", "engine"]):
            return "Any"

        return None

    def _suggest_return_type(self, node: ast.FunctionDef) -> str | None:
        """Suggest return type based on function analysis."""
        func_name = node.name

        # Analyze return statements
        return_types = set()
        has_explicit_return = False

        for child in ast.walk(node):
            if isinstance(child, ast.Return):
                has_explicit_return = True
                if child.value is None:
                    return_types.add("None")
                elif isinstance(child.value, ast.Constant):
                    if isinstance(child.value.value, bool):
                        return_types.add("bool")
                    elif isinstance(child.value.value, int | float):
                        return_types.add("Union[int, float]")
                    elif isinstance(child.value.value, str):
                        return_types.add("str")
                elif isinstance(child.value, ast.List):
                    return_types.add("List[Any]")
                elif isinstance(child.value, ast.Dict):
                    return_types.add("Dict[str, Any]")
                else:
                    return_types.add("Any")

        # Function name patterns
        if func_name.startswith(("is_", "has_", "can_", "should_")):
            return "bool"
        if func_name.startswith(("get_", "find_", "search_")):
            return "Optional[Any]"
        if func_name.startswith(("create_", "build_", "make_")):
            return "Any"
        if func_name.startswith(("list_", "all_")):
            return "List[Any]"
        elif func_name == "__init__":
            return "None"
        elif func_name.startswith("_") and not has_explicit_return:
            return "None"

        # Based on return analysis
        if return_types:
            if len(return_types) == 1:
                return next(iter(return_types))
            if "None" in return_types and len(return_types) == 2:
                other_type = next(t for t in return_types if t != "None")
                return f"Optional[{other_type}]"
            return "Any"

        # Default for functions without explicit returns
        return "None" if not has_explicit_return else "Any"

    def _generate_fix_description(
        self, func_name: str, missing_params: list[dict], missing_return: str | None
    ) -> str:
        """Generate human-readable description of fixes."""
        parts = []

        if missing_params:
            param_strs = [f"{p['name']}: {p['type']}" for p in missing_params]
            parts.append(f"params({', '.join(param_strs)})")

        if missing_return:
            parts.append(f"return(-> {missing_return})")

        return f"{func_name} - Add {', '.join(parts)}"

    def _apply_fixes(self, content: str, fixes: list[dict]) -> str:
        """Apply type hint fixes to file content."""
        lines = content.split("\n")

        # Sort fixes by line number (descending) to avoid line number shifts
        fixes.sort(key=lambda x: x["line"], reverse=True)

        needed_imports = set()

        for fix in fixes:
            line_idx = fix["line"] - 1
            original_line = lines[line_idx]

            # Apply the fix
            new_line = self._modify_function_signature(
                original_line, fix["missing_params"], fix["missing_return"]
            )

            lines[line_idx] = new_line

            # Track needed imports
            for param in fix["missing_params"]:
                self._track_needed_imports(param["type"], needed_imports)

            if fix["missing_return"]:
                self._track_needed_imports(fix["missing_return"], needed_imports)

        # Add imports at the top
        if needed_imports:
            lines = self._add_imports(lines, needed_imports)

        return "\n".join(lines)

    def _modify_function_signature(
        self, line: str, missing_params: list[dict], missing_return: str | None
    ) -> str:
        """Modify a function signature line to add type hints."""
        # Parse the function signature
        # This is a simplified approach - could be enhanced with AST manipulation

        # Add parameter type hints
        for param in missing_params:
            pattern = rf'\b{param["name"]}\b(?!\s*:)'
            replacement = f'{param["name"]}: {param["type"]}'
            line = re.sub(pattern, replacement, line)

        # Add return type hint
        if missing_return and ")" in line and "->" not in line:
            # Find the last ) before any :
            colon_pos = line.find(":")
            if colon_pos != -1:
                paren_pos = line.rfind(")", 0, colon_pos)
                if paren_pos != -1:
                    line = (
                        line[: paren_pos + 1]
                        + f" -> {missing_return}"
                        + line[paren_pos + 1 :]
                    )

        return line

    def _track_needed_imports(self, type_hint: str, needed_imports: set):
        """Track what imports are needed for type hints."""
        for typing_type in [
            "List",
            "Dict",
            "Optional",
            "Union",
            "Any",
            "Tuple",
            "Callable",
        ]:
            if typing_type in type_hint:
                needed_imports.add(typing_type)

    def _add_imports(self, lines: list[str], needed_imports: set) -> list[str]:
        """Add necessary typing imports to the file."""
        if not needed_imports:
            return lines

        # Find where to insert imports
        insert_pos = 0

        # Skip docstring and comments at top
        for i, line in enumerate(lines):
            if (
                line.strip()
                and not line.strip().startswith("#")
                and not line.strip().startswith('"""')
            ):
                if line.startswith(("from ", "import ")):
                    insert_pos = i + 1
                else:
                    insert_pos = i
                    break

        # Check if typing import already exists
        existing_typing_imports = set()
        for line in lines[: insert_pos + 5]:  # Check first few lines
            if "from typing import" in line:
                # Extract existing imports
                match = re.search(r"from typing import (.+)", line)
                if match:
                    imports = [imp.strip() for imp in match.group(1).split(",")]
                    existing_typing_imports.update(imports)

        # Add missing imports
        new_imports = needed_imports - existing_typing_imports
        if new_imports:
            import_line = f"from typing import {', '.join(sorted(new_imports))}"
            lines.insert(insert_pos, import_line)

        return lines


def main():
    """Main fixer function."""
    parser = argparse.ArgumentParser(description="Fix type hints in Python files")
    parser.add_argument("target", help="File or directory to fix")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be fixed without applying changes",
    )
    parser.add_argument("--package", help="Fix specific package")

    args = parser.parse_args()

    fixer = TypeHintFixer()

    if args.package:
        # Fix specific package
        package_path = Path(f"packages/{args.package}/src")
        if not package_path.exists():
            return

        python_files = list(package_path.rglob("*.py"))
        for py_file in python_files:
            if "__pycache__" not in str(py_file):
                fixer.fix_function_signature(py_file, dry_run=args.dry_run)

        if not args.dry_run:
            pass

    else:
        # Fix single file or directory
        target_path = Path(args.target)

        if target_path.is_file():
            fixer.fix_function_signature(target_path, dry_run=args.dry_run)
        elif target_path.is_dir():
            python_files = list(target_path.rglob("*.py"))
            for py_file in python_files:
                fixer.fix_function_signature(py_file, dry_run=args.dry_run)
        else:
            pass


if __name__ == "__main__":
    main()
