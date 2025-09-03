#!/usr/bin/env python3
"""Clean all __init__.py files to only import what exists."""

import ast
import importlib.util
import sys
from pathlib import Path


def get_module_contents(module_path):
    """Get actual classes, functions, and constants from a module."""
    try:
        spec = importlib.util.spec_from_file_location("temp_module", module_path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            sys.modules["temp_module"] = module
            spec.loader.exec_module(module)

            # Get all public names
            if hasattr(module, "__all__"):
                return set(module.__all__)
            else:
                # Get all non-private names
                return {name for name in dir(module) if not name.startswith("_")}
    except Exception as e:
        print(f"Error loading {module_path}: {e}")
        return set()


def clean_init_file(init_path):
    """Clean an __init__.py file to only import what exists."""
    try:
        with open(init_path) as f:
            content = f.read()

        # Parse the AST
        tree = ast.parse(content)

        # Find all from imports
        new_imports = []
        valid_names = set()

        for node in tree.body:
            if isinstance(node, ast.ImportFrom) and node.module:
                if node.module.startswith("haive.games."):
                    # Convert module path to file path
                    module_parts = node.module.split(".")
                    relative_path = "/".join(module_parts[2:]) + ".py"
                    module_file = (
                        Path(init_path).parent.parent.parent
                        / "src/haive/games"
                        / relative_path
                    )

                    if module_file.exists():
                        # Get actual contents
                        actual_contents = get_module_contents(module_file)

                        # Filter imports
                        valid_imports = []
                        for alias in node.names:
                            if alias.name in actual_contents:
                                valid_imports.append(alias.name)
                                valid_names.add(alias.name)
                            else:
                                print(f"  Removing: {alias.name} from {node.module}")

                        if valid_imports:
                            # Create new import line
                            import_names = ", ".join(sorted(valid_imports))
                            new_imports.append(
                                f"from {node.module} import {import_names}"
                            )
                    else:
                        print(f"  Module not found: {module_file}")
                else:
                    # Keep non-haive.games imports as-is
                    import_line = (
                        ast.get_source_segment(content, node)
                        or f"from {node.module} import ..."
                    )
                    new_imports.append(import_line)

        # Create new content
        new_content = '"""Module exports."""\n\n'
        new_content += "\n".join(new_imports)
        new_content += "\n\n__all__ = [\n"
        for name in sorted(valid_names):
            new_content += f'    "{name}",\n'
        new_content += "]\n"

        # Write back
        with open(init_path, "w") as f:
            f.write(new_content)

        return True
    except Exception as e:
        print(f"Error cleaning {init_path}: {e}")
        return False


def main():
    """Clean all __init__.py files."""
    games_dir = Path("src/haive/games")

    # Focus on the most problematic ones first
    problem_files = [
        games_dir / "core/agent/__init__.py",
        games_dir / "base/__init__.py",
        games_dir / "framework/base/__init__.py",
    ]

    for init_file in problem_files:
        if init_file.exists():
            print(f"\nCleaning {init_file}...")
            clean_init_file(init_file)


if __name__ == "__main__":
    main()
