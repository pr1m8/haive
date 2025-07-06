"""Content audit script to ensure complete preservation of functionality."""

import ast
from pathlib import Path


def extract_classes_and_methods(file_path):
    """Extract all classes, methods, and functions from a Python file."""
    with open(file_path) as f:
        content = f.read()

    tree = ast.parse(content)

    classes = {}
    functions = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            methods = []
            properties = []
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    methods.append(item.name)
                elif isinstance(item, ast.AsyncFunctionDef):
                    methods.append(f"async {item.name}")
            classes[node.name] = {
                "methods": methods,
                "properties": properties,
                "line": node.lineno,
            }
        elif isinstance(node, ast.FunctionDef):
            functions.append(node.name)

    return classes, functions


def audit_file(file_path, file_name):
    """Audit a single file."""
    try:
        classes, functions = extract_classes_and_methods(file_path)

        for _class_name, info in classes.items():
            for _method in info["methods"]:
                pass

        for _func in functions:
            pass

        return classes, functions

    except Exception:
        return {}, []


def main():
    """Main audit function."""
    base_path = Path(
        "/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema"
    )

    files_to_audit = [
        "schema_composer.py",
        "state_schema.py",
        "prebuilt/messages_state.py",
    ]

    total_audit = {}

    for file_name in files_to_audit:
        file_path = base_path / file_name
        if file_path.exists():
            classes, functions = audit_file(file_path, file_name)
            total_audit[file_name] = {
                "classes": classes,
                "functions": functions,
                "path": str(file_path),
            }

    # Summary

    total_classes = 0
    total_methods = 0
    total_functions = 0

    for file_name, data in total_audit.items():
        class_count = len(data["classes"])
        method_count = sum(len(info["methods"]) for info in data["classes"].values())
        func_count = len(data["functions"])

        total_classes += class_count
        total_methods += method_count
        total_functions += func_count


if __name__ == "__main__":
    main()
