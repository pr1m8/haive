#!/usr/bin/env python3
"""Docstring Templates for Haive Documentation Automation.

This module provides standardized templates for generating consistent
documentation across the Haive framework packages.

Usage:
    python docstring_templates.py --module haive.agents.simple --output simple_docstrings.py
"""

import ast
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set

# =============================================================================
# DOCSTRING TEMPLATES
# =============================================================================

MODULE_DOCSTRING_TEMPLATE = '''"""{module_name} - {brief_description}

{detailed_description}

This module provides {main_functionality} for the Haive AI Agent Framework.

Key Components:
{key_components}

Example:
    Basic usage::

        from {module_path} import {main_class}
        
        # Create instance
        instance = {main_class}({basic_params})
        
        # Use the {main_functionality}
        result = instance.{main_method}({example_input})
        
        print(f"Result: {{result}}")

Advanced Usage:
    {advanced_example}

See Also:
    {related_modules}

Notes:
    {implementation_notes}
"""'''

FUNCTION_DOCSTRING_TEMPLATE = '''"""
{brief_description}

{detailed_description}

Args:
{args_section}

Returns:
{returns_section}

Raises:
{raises_section}

Example:
{example_section}

Note:
    {notes_section}
"""'''

CLASS_DOCSTRING_TEMPLATE = '''"""
{brief_description}

{detailed_description}

This class {class_purpose} and provides {main_functionality}.

Attributes:
{attributes_section}

Example:
    Basic usage::

        {basic_example}

    Advanced usage::

        {advanced_example}

See Also:
    {related_classes}

Notes:
    {implementation_notes}
"""'''

INIT_PY_TEMPLATE = '''"""
{package_name} - {brief_description}

{detailed_description}

This package provides {main_functionality} for the Haive framework.

Available Components:
{available_components}

Quick Start:
    {quick_start_example}

See Also:
    {related_packages}
"""

{imports}

__all__ = {all_exports}
'''


# =============================================================================
# INTELLIGENT CONTENT GENERATORS
# =============================================================================


class DocumentationAnalyzer:
    """Analyze Python modules to generate intelligent documentation."""

    def __init__(self, module_path: Path):
        """Initialize analyzer with module path."""
        self.module_path = module_path
        self.classes: List[str] = []
        self.functions: List[str] = []
        self.imports: List[str] = []
        self.constants: List[str] = []

    def analyze_module(self) -> Dict[str, any]:
        """Analyze module and extract components."""
        try:
            with open(self.module_path, "r", encoding="utf-8") as f:
                content = f.read()

            tree = ast.parse(content)

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    self.classes.append(node.name)
                elif isinstance(node, ast.FunctionDef):
                    if not node.name.startswith("_"):  # Skip private functions
                        self.functions.append(node.name)
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        self.imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        for alias in node.names:
                            self.imports.append(f"{node.module}.{alias.name}")
                elif isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id.isupper():
                            self.constants.append(target.id)

            return {
                "classes": self.classes,
                "functions": self.functions,
                "imports": self.imports,
                "constants": self.constants,
                "has_main_class": len(self.classes) > 0,
                "main_class": self.classes[0] if self.classes else None,
                "main_function": self.functions[0] if self.functions else None,
            }

        except Exception as e:
            print(f"Error analyzing {self.module_path}: {e}")
            return {}


def generate_module_docstring(module_path: Path, analysis: Dict) -> str:
    """Generate intelligent module docstring based on analysis."""

    # Extract module information
    module_parts = module_path.parts
    module_name = module_parts[-1].replace(".py", "").replace("_", " ").title()

    # Generate descriptions based on analysis
    if analysis.get("classes"):
        brief_desc = (
            f"Implementation of {', '.join(analysis['classes'])} for Haive framework"
        )
        main_functionality = f"{analysis['classes'][0]} implementation"
        key_components = "\n".join(
            [
                f"    - {cls}: Main {cls.lower()} implementation"
                for cls in analysis["classes"]
            ]
        )
    elif analysis.get("functions"):
        brief_desc = f"Utility functions for {module_name.lower()}"
        main_functionality = "utility functions"
        key_components = "\n".join(
            [
                f"    - {func}(): {func.replace('_', ' ').title()} function"
                for func in analysis["functions"][:5]
            ]
        )
    else:
        brief_desc = f"{module_name} module"
        main_functionality = "core functionality"
        key_components = "    - Core module components (see source code)"

    # Smart path generation
    module_import_path = (
        ".".join(module_parts[:-1]) if len(module_parts) > 1 else module_name.lower()
    )

    return MODULE_DOCSTRING_TEMPLATE.format(
        module_name=module_name,
        brief_description=brief_desc,
        detailed_description=f"TODO: Add comprehensive description of {module_name.lower()} functionality.",
        main_functionality=main_functionality,
        key_components=key_components,
        module_path=module_import_path,
        main_class=analysis.get("main_class", "MainClass"),
        basic_params="name='example'",
        main_method=analysis.get("main_function", "process"),
        example_input="'input_data'",
        advanced_example=f"TODO: Add advanced {main_functionality} example",
        related_modules="TODO: List related modules",
        implementation_notes="TODO: Add implementation notes and caveats",
    )


def generate_all_exports(analysis: Dict) -> List[str]:
    """Generate __all__ exports based on analysis."""
    exports = []

    # Add public classes
    exports.extend(analysis.get("classes", []))

    # Add public functions
    exports.extend(analysis.get("functions", []))

    # Add public constants
    exports.extend(analysis.get("constants", []))

    return sorted(exports)


# =============================================================================
# AUTOMATION SCRIPTS
# =============================================================================


def add_missing_all_exports(init_file: Path) -> bool:
    """Add missing __all__ exports to __init__.py file."""
    try:
        # Read current content
        if init_file.exists():
            with open(init_file, "r", encoding="utf-8") as f:
                content = f.read()
        else:
            content = ""

        # Check if __all__ already exists
        if "__all__" in content:
            print(f"✅ {init_file} already has __all__")
            return False

        # Analyze the file
        if content.strip():
            analyzer = DocumentationAnalyzer(init_file)
            analysis = analyzer.analyze_module()
            exports = generate_all_exports(analysis)
        else:
            exports = []

        # Generate new content
        if exports:
            all_line = f"\n__all__ = {exports}\n"
        else:
            all_line = "\n__all__ = []\n"

        # Add to file
        new_content = content + all_line

        with open(init_file, "w", encoding="utf-8") as f:
            f.write(new_content)

        print(f"✅ Added __all__ to {init_file} ({len(exports)} exports)")
        return True

    except Exception as e:
        print(f"❌ Error processing {init_file}: {e}")
        return False


def add_missing_module_docstring(py_file: Path) -> bool:
    """Add missing module docstring to Python file."""
    try:
        # Read current content
        with open(py_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Check if docstring already exists
        if content.strip().startswith('"""') or content.strip().startswith("'''"):
            return False

        # Analyze the file
        analyzer = DocumentationAnalyzer(py_file)
        analysis = analyzer.analyze_module()

        # Generate docstring
        docstring = generate_module_docstring(py_file, analysis)

        # Add to beginning of file
        new_content = docstring + "\n\n" + content

        with open(py_file, "w", encoding="utf-8") as f:
            f.write(new_content)

        print(f"✅ Added module docstring to {py_file}")
        return True

    except Exception as e:
        print(f"❌ Error processing {py_file}: {e}")
        return False


# =============================================================================
# MAIN EXECUTION
# =============================================================================


def main():
    """Main execution function."""
    if len(sys.argv) < 2:
        print("Usage: python docstring_templates.py <packages_dir>")
        sys.exit(1)

    packages_dir = Path(sys.argv[1])

    if not packages_dir.exists():
        print(f"Error: {packages_dir} does not exist")
        sys.exit(1)

    print(f"🚀 Starting documentation improvements for {packages_dir}")

    # Find all Python files
    init_files = list(packages_dir.rglob("__init__.py"))
    py_files = list(packages_dir.rglob("*.py"))

    # Exclude test files
    init_files = [f for f in init_files if "/tests/" not in str(f)]
    py_files = [f for f in py_files if "/tests/" not in str(f)]

    print(f"Found {len(init_files)} __init__.py files")
    print(f"Found {len(py_files)} Python files")

    # Add missing __all__ exports
    print("\n📋 Adding missing __all__ exports...")
    all_added = 0
    for init_file in init_files:
        if add_missing_all_exports(init_file):
            all_added += 1

    print(f"✅ Added __all__ to {all_added} files")

    # Add missing module docstrings
    print("\n📝 Adding missing module docstrings...")
    docs_added = 0
    for py_file in py_files[:20]:  # Start with first 20 files
        if add_missing_module_docstring(py_file):
            docs_added += 1

    print(f"✅ Added module docstrings to {docs_added} files")

    print("\n🎉 Documentation improvements complete!")


if __name__ == "__main__":
    main()
