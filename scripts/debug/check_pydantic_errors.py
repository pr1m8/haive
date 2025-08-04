#!/usr/bin/env python3
"""Check for common Pydantic validation errors in the codebase.

This script systematically checks for:
1. @model_validator(mode="after") with @classmethod (incorrect)
2. BaseTool classes with args_schema = Model (should use Field annotation)
3. @field_validator syntax errors

Run before documentation builds to catch errors early.
"""

from __future__ import annotations

import ast
from pathlib import Path
import sys


def check_file_for_pydantic_errors(filepath: Path) -> list[str]:
    """Check a single file for Pydantic validation errors."""
    errors = []

    try:
        with open(filepath) as f:
            content = f.read()

        # Parse AST for structural analysis
        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            return [f"{filepath}:{e.lineno}: Syntax error: {e.msg}"]

        # Check for text patterns first (faster for some errors)
        lines = content.split("\n")

        # 1. Check for @field_validatorvalidate_* syntax errors
        for line_num, line in enumerate(lines, 1):
            if "@field_validatorvalidate_" in line:
                errors.append(
                    f"{filepath}:{line_num}: Invalid @field_validator syntax - missing parentheses", )

        # 2. Check for args_schema direct assignment in BaseTool classes
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Check if this inherits from BaseTool
                inherits_basetool = any(
                    (isinstance(base, ast.Name) and base.id == "BaseTool")
                    or (isinstance(base, ast.Attribute) and base.attr == "BaseTool")
                    for base in node.bases
                )

                if inherits_basetool:
                    for item in node.body:
                        if (
                            isinstance(item, ast.Assign)
                            and len(item.targets) == 1
                            and isinstance(item.targets[0], ast.Name)
                            and item.targets[0].id == "args_schema"
                        ):
                            # Check if it's a simple assignment without Field
                            is_field_call = (
                                isinstance(item.value, ast.Call)
                                and isinstance(
                                    item.value.func,
                                    ast.Name,
                                )
                                and item.value.func.id == "Field"
                            )

                            if not is_field_call:
                                errors.append(
                                    f"{filepath}:{
                                        item.lineno
                                    }: args_schema in BaseTool should use Field(default=Model) annotation",
                                )

            # 3. Check for @model_validator(mode="after") with @classmethod
            if isinstance(node, ast.FunctionDef):
                has_model_validator_after = False
                has_classmethod = False

                for decorator in node.decorator_list:
                    if isinstance(decorator, ast.Call):
                        if (
                            isinstance(decorator.func, ast.Attribute)
                            and decorator.func.attr == "model_validator"
                        ):
                            for keyword in decorator.keywords:
                                if (
                                    keyword.arg == "mode"
                                    and isinstance(
                                        keyword.value,
                                        ast.Constant,
                                    )
                                    and keyword.value.value == "after"
                                ):
                                    has_model_validator_after = True
                    elif (
                        isinstance(
                            decorator,
                            ast.Name,
                        )
                        and decorator.id == "classmethod"
                    ):
                        has_classmethod = True

                if has_model_validator_after and has_classmethod:
                    errors.append(
                        f"{filepath}:{
                            node.lineno
                        }: @model_validator(mode='after') should not use @classmethod",
                    )

    except Exception as e:
        errors.append(f"{filepath}: Exception during analysis: {e}")

    return errors


def main():
    """Main function to check all Python files in packages/ and migrations/."""
    project_root = Path(__file__).parent.parent.parent
    packages_dir = project_root / "packages"
    migrations_dir = project_root / "migrations"

    dirs_to_check = []
    if packages_dir.exists():
        dirs_to_check.append(packages_dir)
    if migrations_dir.exists():
        dirs_to_check.append(migrations_dir)

    if not dirs_to_check:
        print("ERROR: No directories found to check")
        sys.exit(1)

    print(
        f"🔍 Checking for Pydantic validation errors in: {
            ', '.join(str(d) for d in dirs_to_check)
        }",
    )
    print("=" * 60)

    all_errors = []
    files_checked = 0

    # Find all Python files in packages/ and migrations/
    for check_dir in dirs_to_check:
        for py_file in check_dir.rglob("*.py"):
            files_checked += 1
            errors = check_file_for_pydantic_errors(py_file)
            all_errors.extend(errors)

    print(f"📊 Checked {files_checked} Python files")

    if all_errors:
        print(f"❌ Found {len(all_errors)} Pydantic validation errors:")
        print("-" * 60)
        for error in all_errors:
            print(f"  {error}")
        print("=" * 60)
        print("🔧 Fix these errors before running documentation builds")
        sys.exit(1)
    else:
        print("✅ No Pydantic validation errors found!")
        sys.exit(0)


if __name__ == "__main__":
    main()
