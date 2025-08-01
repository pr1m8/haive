#!/usr/bin/env python3
"""Docstring generation with Google/Sphinx style formatting.

This module provides automatic docstring generation including:
- Google-style docstring templates
- Function signature analysis for Args/Returns sections
- Module and class docstring generation
- Smart insertion logic that preserves existing code
"""

import ast
import logging
import sys
from pathlib import Path
from typing import List

from .coverage import DocstringTarget

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


class DocstringGenerator:
    """Generates missing docstrings using Google/Sphinx style."""

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.generated_docstrings: List[DocstringTarget] = []

    def generate_missing_docstrings(self, targets: List[DocstringTarget]) -> int:
        """Generate docstrings for missing targets."""
        if self.dry_run:
            logger.info(f"🧪 Would generate {len(targets)} missing docstrings")
            return len(targets)

        logger.info(f"📝 Generating {len(targets)} missing docstrings")
        generated_count = 0

        # Group by file for efficient processing
        targets_by_file = {}
        for target in targets:
            if target.file_path not in targets_by_file:
                targets_by_file[target.file_path] = []
            targets_by_file[target.file_path].append(target)

        for file_path, file_targets in targets_by_file.items():
            try:
                if self._generate_docstrings_for_file(file_path, file_targets):
                    generated_count += len(file_targets)
            except Exception as e:
                logger.error(f"❌ Failed to generate docstrings for {file_path}: {e}")

        logger.info(f"🎉 Generated {generated_count} docstrings")
        return generated_count

    def _generate_docstrings_for_file(
        self, file_path: Path, targets: List[DocstringTarget]
    ) -> bool:
        """Generate docstrings for targets in a specific file."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            # Sort targets by line number (reverse order to maintain line numbers)
            targets.sort(key=lambda t: t.line_number, reverse=True)

            for target in targets:
                docstring = self._create_docstring_for_target(target, file_path)
                if docstring:
                    self._insert_docstring(lines, target, docstring)

            # Write updated file
            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(lines)

            return True

        except Exception as e:
            logger.error(f"Failed to process {file_path}: {e}")
            return False

    def _create_docstring_for_target(
        self, target: DocstringTarget, file_path: Path
    ) -> str:
        """Create a docstring for a specific target."""
        if target.target_type == "module":
            return self._create_module_docstring(file_path)
        elif target.target_type == "class":
            return self._create_class_docstring(target)
        elif target.target_type in ["function", "method"]:
            return self._create_function_docstring(target, file_path)

        return ""

    def _create_module_docstring(self, file_path: Path) -> str:
        """Create a module-level docstring."""
        module_name = file_path.stem
        if module_name == "__init__":
            package_name = file_path.parent.name
            return f'"""Package initialization for {package_name}."""\n\n'
        else:
            return f'"""Module: {module_name}."""\n\n'

    def _create_class_docstring(self, target: DocstringTarget) -> str:
        """Create a class docstring."""
        class_name = target.class_name
        return f'    """Class: {class_name}."""\n'

    def _create_function_docstring(
        self, target: DocstringTarget, file_path: Path
    ) -> str:
        """Create a function/method docstring."""
        # Try to analyze the function signature for better docstring
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            tree = ast.parse(content)

            # Find the function node
            for node in ast.walk(tree):
                if (
                    isinstance(node, ast.FunctionDef)
                    and node.name == target.function_name
                    and node.lineno == target.line_number
                ):

                    return self._generate_google_style_docstring(node, target)

        except Exception:
            pass

        # Fallback to simple docstring
        indent = "        " if target.target_type == "method" else "    "
        return f'{indent}"""{target.function_name.replace("_", " ").title()}."""\n'

    def _generate_google_style_docstring(
        self, node: ast.FunctionDef, target: DocstringTarget
    ) -> str:
        """Generate Google-style docstring from function AST node."""
        indent = "        " if target.target_type == "method" else "    "

        # Extract function info
        func_name = node.name
        args = []

        for arg in node.args.args:
            if arg.arg == "self":
                continue
            args.append(arg.arg)

        # Create docstring
        docstring_lines = [f'{indent}"""{func_name.replace("_", " ").title()}.']

        if args:
            docstring_lines.extend(
                [
                    "",
                    "    Args:",
                ]
            )
            for arg in args:
                docstring_lines.append(f"        {arg}: Description of {arg}.")

        # Check if function has return statement
        has_return = any(
            isinstance(node_child, ast.Return) and node_child.value
            for node_child in ast.walk(node)
        )

        if has_return and func_name != "__init__":
            docstring_lines.extend(
                [
                    "",
                    "    Returns:",
                    "        Return value description.",
                ]
            )

        docstring_lines.append('    """')

        # Join with proper indentation
        result = "\n".join(docstring_lines) + "\n"
        return result

    def _insert_docstring(
        self, lines: List[str], target: DocstringTarget, docstring: str
    ):
        """Insert docstring into file lines."""
        if target.target_type == "module":
            # Insert at the beginning after any imports/comments
            insert_pos = 0
            for i, line in enumerate(lines):
                if (
                    line.strip()
                    and not line.strip().startswith("#")
                    and not line.strip().startswith('"""')
                    and not line.strip().startswith("import")
                    and not line.strip().startswith("from")
                ):
                    insert_pos = i
                    break
            lines.insert(insert_pos, docstring)
        else:
            # Insert after function/class declaration
            insert_pos = target.line_number  # Line after the def/class line
            lines.insert(insert_pos, docstring)


def main():
    """CLI entry point for docstring generation."""
    import argparse

    parser = argparse.ArgumentParser(description="Generate missing docstrings")
    parser.add_argument("--target", required=True, help="Target package")
    parser.add_argument(
        "--dry-run", action="store_true", help="Show what would be generated"
    )

    args = parser.parse_args()

    # Import coverage analyzer to find missing docstrings
    from .coverage import CoverageAnalyzer

    analyzer = CoverageAnalyzer()
    coverage_report = analyzer.analyze_package_coverage(args.target)

    if coverage_report.missing_targets:
        generator = DocstringGenerator(dry_run=args.dry_run)
        generated = generator.generate_missing_docstrings(
            coverage_report.missing_targets
        )
        logger.info(f"🎉 Generated {generated} docstrings")
        return 0
    else:
        logger.info("✅ No missing docstrings found!")
        return 0


if __name__ == "__main__":
    sys.exit(main())
