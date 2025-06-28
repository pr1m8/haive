#!/usr/bin/env python3
"""Generate module README.md files and update __init__.py docstrings.

This script helps create consistent documentation for all modules in the Haive project.
"""

import ast
from pathlib import Path

# Root directory
ROOT_DIR = Path(__file__).parent.parent

# Template for module README
MODULE_README_TEMPLATE = """# {module_name}

{description}

## Overview

{overview}

## Key Components

{components}

## Installation

This module is part of the `{package_name}` package. Install it using:

```bash
pip install {package_name}
```

## Usage Examples

### Basic Usage

```python
{basic_example}
```

## API Reference

For detailed API documentation, see the [API Reference](../../../docs/source/api/{module_path}/index.rst).

## See Also

{see_also}
"""

# Template for __init__.py docstring
INIT_DOCSTRING_TEMPLATE = '''"""{module_name} - {brief_description}

{detailed_description}

{features}

Example:
    {example}

{see_also}
"""
'''


def get_module_info(module_path: Path) -> dict[str, any]:
    """Extract information about a module."""
    info = {
        "path": module_path,
        "name": module_path.name,
        "package": None,
        "classes": [],
        "functions": [],
        "submodules": [],
        "has_init": False,
        "init_docstring": None,
        "description": "",
    }

    # Determine package
    parts = module_path.parts
    if "packages" in parts:
        pkg_idx = parts.index("packages")
        if pkg_idx + 1 < len(parts):
            info["package"] = parts[pkg_idx + 1]

    # Check for __init__.py
    init_file = module_path / "__init__.py"
    if init_file.exists():
        info["has_init"] = True
        try:
            content = init_file.read_text()
            tree = ast.parse(content)

            # Get module docstring
            docstring = ast.get_docstring(tree)
            if docstring:
                info["init_docstring"] = docstring
                # Extract brief description (first line)
                info["description"] = docstring.split("\n")[0].strip()

            # Extract classes and functions
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    info["classes"].append(node.name)
                elif isinstance(node, ast.FunctionDef):
                    if not node.name.startswith("_"):
                        info["functions"].append(node.name)
        except:
            pass

    # Find submodules
    for item in module_path.iterdir():
        if (
            item.is_dir()
            and not item.name.startswith(("_", "."))
            and item.name != "__pycache__"
        ) and (item / "__init__.py").exists():
            info["submodules"].append(item.name)

    return info


def generate_module_readme(info: dict[str, any]) -> str:
    """Generate README content for a module."""
    module_name = info["name"].replace("_", " ").title()

    # Build components section
    components_parts = []
    if info["classes"]:
        components_parts.append("### Classes\n")
        for cls in info["classes"][:5]:  # Limit to first 5
            components_parts.append(f"- **{cls}**: TODO: Add description\n")

    if info["functions"]:
        components_parts.append("\n### Functions\n")
        for func in info["functions"][:5]:  # Limit to first 5
            components_parts.append(f"- **{func}()**: TODO: Add description\n")

    if info["submodules"]:
        components_parts.append("\n### Submodules\n")
        for submod in info["submodules"]:
            components_parts.append(f"- **{submod}**: TODO: Add description\n")

    components = (
        "".join(components_parts) if components_parts else "TODO: Document components"
    )

    # Generate basic example
    if info["classes"]:
        main_class = info["classes"][0]
        basic_example = f"""from haive.{info['name']} import {main_class}

# Initialize
instance = {main_class}()

# TODO: Add usage example"""
    else:
        basic_example = f"""from haive.{info['name']} import module_function

# TODO: Add usage example"""

    # Build see also section
    see_also_parts = []
    if info["submodules"]:
        for submod in info["submodules"][:3]:
            see_also_parts.append(
                f"- [`{info['name']}.{submod}`](./{submod}/): TODO: Add description"
            )

    see_also = (
        "\n".join(see_also_parts) if see_also_parts else "- TODO: Add related modules"
    )

    # Fill template
    return MODULE_README_TEMPLATE.format(
        module_name=module_name,
        description=info["description"] or "TODO: Add module description",
        overview="TODO: Add detailed overview of this module's functionality",
        components=components,
        package_name=info["package"] or "haive",
        basic_example=basic_example,
        module_path=info["name"],
        see_also=see_also,
    )


def generate_init_docstring(info: dict[str, any]) -> str:
    """Generate or improve __init__.py docstring."""
    module_name = info["name"].replace("_", " ").title()

    # Build features section
    features = ""
    if info["classes"] or info["functions"]:
        features = "\nKey Components:\n"
        if info["classes"]:
            features += f"    * Classes: {', '.join(info['classes'][:3])}\n"
        if info["functions"]:
            features += f"    * Functions: {', '.join(info['functions'][:3])}\n"
        if info["submodules"]:
            features += f"    * Submodules: {', '.join(info['submodules'][:3])}\n"

    # Generate example
    if info["classes"]:
        example = f"""Basic usage::

        from haive.{info['name']} import {info['classes'][0]}

        instance = {info['classes'][0]}()
        # TODO: Complete example"""
    else:
        example = """Basic usage::

        from haive.{} import module_function

        # TODO: Add example""".format(
            info["name"]
        )

    # Build see also section
    see_also = ""
    if info["submodules"]:
        see_also = "\nSee Also:\n"
        for submod in info["submodules"][:3]:
            see_also += (
                f"    :mod:`haive.{info['name']}.{submod}`: TODO: Add description\n"
            )

    return INIT_DOCSTRING_TEMPLATE.format(
        module_name=module_name,
        brief_description=info["description"] or "TODO: Add brief description",
        detailed_description="TODO: Add detailed description of module functionality",
        features=features,
        example=example,
        see_also=see_also,
    )


def process_module(module_path: Path, dry_run: bool = True):
    """Process a single module."""
    info = get_module_info(module_path)

    # Generate README if it doesn't exist
    readme_path = module_path / "README.md"
    if not readme_path.exists():
        readme_content = generate_module_readme(info)
        if dry_run:
        else:
            readme_path.write_text(readme_content)

    # Update __init__.py if needed
    init_path = module_path / "__init__.py"
    if init_path.exists() and (not info["init_docstring"] or len(info["init_docstring"]) < 50):
        docstring = generate_init_docstring(info)

        if dry_run:
            print(f"Would update __init__.py: {init_path}")
            print(f"  New docstring first line: {docstring.split(chr(10))[0]}")
        else:
            # Read current content
            content = init_path.read_text()

            # If no docstring, add at beginning
            if not info["init_docstring"]:
                new_content = docstring + "\n" + content
            else:
                # Replace existing docstring
                tree = ast.parse(content)
                if (
                    tree.body
                    and isinstance(tree.body[0], ast.Expr)
                    and isinstance(tree.body[0].value, ast.Str)
                ):
                    # Find end of docstring
                    lines = content.split("\n")
                    in_docstring = False
                    end_line = 0
                    for i, line in enumerate(lines):
                        if line.strip().startswith('"""'):
                            if not in_docstring:
                                in_docstring = True
                            else:
                                end_line = i
                                break

                    # Replace docstring
                    new_lines = [docstring] + lines[end_line + 1 :]
                    new_content = "\n".join(new_lines)
                else:
                    new_content = docstring + "\n" + content

            init_path.write_text(new_content)
            print(f"Updated __init__.py: {init_path}")


def find_modules() -> list[Path]:
    """Find all modules that need documentation."""
    modules = []

    # Find all package modules
    packages_dir = ROOT_DIR / "packages"
    for package_dir in packages_dir.glob("haive-*"):
        src_dir = package_dir / "src" / "haive"
        if src_dir.exists():
            # Process each module in the package
            for module_dir in src_dir.iterdir():
                if module_dir.is_dir() and not module_dir.name.startswith(("_", ".")):
                    modules.append(module_dir)

                    # Also process submodules
                    for submodule in module_dir.rglob("*"):
                        if submodule.is_dir() and (submodule / "__init__.py").exists():
                            if not any(
                                skip in str(submodule)
                                for skip in ["__pycache__", "test", ".pyc"]
                            ):
                                modules.append(submodule)

    return sorted(set(modules))


def main(dry_run: bool = True):
    """Main function."""

    if dry_run:
        pass
    else:
        pass

    modules = find_modules()

    for module in modules:
        process_module(module, dry_run)


    if dry_run:


if __name__ == "__main__":
    import sys

    dry_run = "--no-dry-run" not in sys.argv
    main(dry_run)
