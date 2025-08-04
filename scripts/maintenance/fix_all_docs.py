#!/usr/bin/env python3
"""Comprehensive documentation fix script for Haive project."""

import logging
import os
from pathlib import Path
import re

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


class DocumentationFixer:
    """Fix various documentation issues in the Haive project."""

    def __init__(self, docs_dir="docs"):
        self.docs_dir = Path(docs_dir)
        self.source_dir = self.docs_dir / "source"
        self.fixed_count = 0

    def fix_all(self):
        """Run all fixes."""
        logger.info("🔧 Starting comprehensive documentation fixes...")

        # Fix RST files
        self.fix_rst_files()

        # Fix showcase index
        self.fix_showcase_index()

        # Fix toctree issues
        self.fix_toctree_issues()

        # Clean up empty or broken files
        self.cleanup_broken_files()

        # Fix common docstring patterns in Python files
        self.fix_python_docstrings()

        logger.info(f"\n✅ Fixed {self.fixed_count} issues!")

    def fix_rst_files(self):
        """Fix all RST files with title underline issues."""
        logger.info("\n📝 Fixing RST title underlines...")

        # Find all RST files
        rst_files = list(self.source_dir.rglob("*.rst"))

        for rst_file in rst_files:
            if self.fix_title_underlines(rst_file):
                logger.info(
                    f"  ✓ Fixed: {rst_file.relative_to(self.docs_dir)}")
                self.fixed_count += 1

    def fix_title_underlines(self, file_path):
        """Fix title underline lengths in an RST file."""
        try:
            with open(file_path, encoding="utf-8") as f:
                lines = f.readlines()
        except Exception as e:
            logger.exception(f"  ✗ Error reading {file_path}: {e}")
            return False

        fixed = False
        fixed_lines = []
        i = 0

        while i < len(lines):
            line = lines[i]

            # Check if next line is an underline
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                # RST underline characters
                if next_line.strip() and all(c in '=-~^"+*#'
                                             for c in next_line.strip()):
                    title_length = len(line.rstrip())
                    underline_char = next_line.strip()[0]
                    current_underline_length = len(next_line.strip())

                    if current_underline_length != title_length:
                        correct_underline = underline_char * title_length + "\n"
                        fixed_lines.append(line)
                        fixed_lines.append(correct_underline)
                        fixed = True
                        i += 2
                        continue

            fixed_lines.append(line)
            i += 1

        if fixed:
            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(fixed_lines)

        return fixed

    def fix_showcase_index(self):
        """Fix the showcase_index.rst grid structure."""
        logger.info("\n🎨 Fixing showcase index grid structure...")

        showcase_file = self.source_dir / "agents" / "showcase_index.rst"
        if not showcase_file.exists():
            logger.warning("  ⚠️  showcase_index.rst not found")
            return

        try:
            with open(showcase_file, encoding="utf-8") as f:
                content = f.read()

            # Fix grid structure - ensure proper nesting
            # Look for grid directives without proper content
            content = re.sub(
                r"(\.\. grid:: .*?\n)(\s*\n)(\s*\.\. grid-item::)",
                r"\1\n   .. grid-row::\n\n\3",
                content,
                flags=re.MULTILINE,
            )

            # Fix toctree with multiple items on one line
            content = re.sub(
                r"(\s+)(\w+_showcase)\s+(\w+_showcase)\s+(\w+_showcase)",
                r"\1\2\n\1\3\n\1\4",
                content,
            )

            # Add content to empty grid directives
            content = re.sub(
                r"(\.\. grid:: [^\n]+)\n(\s*\.\. grid-row::)",
                r"\1\n   :gutter: 3\n   :class-container: showcase-grid\n\n\2",
                content,
            )

            with open(showcase_file, "w", encoding="utf-8") as f:
                f.write(content)

            logger.info("  ✓ Fixed showcase index")
            self.fixed_count += 1

        except Exception as e:
            logger.exception(f"  ✗ Error fixing showcase index: {e}")

    def fix_toctree_issues(self):
        """Fix toctree reference issues."""
        logger.info("\n🌳 Fixing toctree references...")

        # Find all RST files with toctree directives
        rst_files = list(self.source_dir.rglob("*.rst"))

        for rst_file in rst_files:
            try:
                with open(rst_file, encoding="utf-8") as f:
                    content = f.read()

                if ".. toctree::" in content:
                    # Fix common toctree issues
                    original_content = content

                    # Ensure proper indentation for toctree entries
                    content = re.sub(
                        r"(\.\. toctree::.*?\n(?:\s+:[^:]+:.*\n)*)\n(\S)",
                        r"\1\n   \2",
                        content,
                        flags=re.MULTILINE | re.DOTALL,
                    )

                    if content != original_content:
                        with open(rst_file, "w", encoding="utf-8") as f:
                            f.write(content)
                        logger.info(
                            f"  ✓ Fixed toctree in: {
                                rst_file.relative_to(
                                    self.docs_dir)}", )
                        self.fixed_count += 1

            except Exception as e:
                logger.exception(f"  ✗ Error processing {rst_file}: {e}")

    def cleanup_broken_files(self):
        """Remove or fix empty/broken documentation files."""
        logger.info("\n🧹 Cleaning up broken files...")

        # Remove duplicate index files (prefer .rst over .md)
        for dir_path in self.source_dir.rglob("**/"):
            if dir_path.is_dir():
                rst_index = dir_path / "index.rst"
                md_index = dir_path / "index.md"

                if rst_index.exists() and md_index.exists():
                    md_index.unlink()
                    logger.info(
                        f"  ✓ Removed duplicate: {md_index.relative_to(self.docs_dir)}",
                    )
                    self.fixed_count += 1

    def fix_python_docstrings(self):
        """Fix common docstring issues in Python files."""
        logger.info("\n🐍 Fixing Python docstring issues...")

        # Find the packages directory
        packages_dir = Path.cwd() / "packages"
        if not packages_dir.exists():
            logger.warning("  ⚠️  packages directory not found")
            return

        # Common docstring fixes
        fixes_applied = 0

        # Fix specific known problematic files
        problematic_files = [
            "haive-core/src/haive/core/schema/field_definition.py",
        ]

        for file_path in problematic_files:
            full_path = packages_dir / file_path
            if full_path.exists() and self.fix_docstring_formatting(full_path):
                logger.info(f"  ✓ Fixed docstrings in: {file_path}")
                fixes_applied += 1

        self.fixed_count += fixes_applied

    def fix_docstring_formatting(self, file_path):
        """Fix docstring formatting issues in a Python file."""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            original_content = content

            # Fix incomplete inline literals (backticks)
            # Match single backticks that aren't properly closed
            content = re.sub(r"`([^`\n]+)(?=\s|$)", r"``\1``", content)

            # Fix docstring indentation issues
            # This is a simplified fix - comprehensive fixing would require AST parsing
            lines = content.split("\n")
            fixed_lines = []
            in_docstring = False
            docstring_indent = 0

            for _i, line in enumerate(lines):
                if '"""' in line or "'''" in line:
                    in_docstring = not in_docstring
                    if in_docstring:
                        # Starting a docstring, determine base indentation
                        docstring_indent = len(line) - len(line.lstrip())

                if in_docstring and line.strip(
                ) and '"""' not in line and "'''" not in line:
                    # Ensure consistent indentation within docstrings
                    current_indent = len(line) - len(line.lstrip())
                    if current_indent < docstring_indent + 4 and line.strip():
                        # Fix under-indented lines
                        line = " " * (docstring_indent + 4) + line.lstrip()

                fixed_lines.append(line)

            content = "\n".join(fixed_lines)

            if content != original_content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                return True

        except Exception as e:
            logger.exception(f"  ✗ Error fixing {file_path}: {e}")

        return False


def main():
    """Run the documentation fixer."""
    # Change to docs directory if we're not already there
    if Path.cwd().name != "docs" and (Path.cwd() / "docs").exists():
        os.chdir("docs")

    fixer = DocumentationFixer()
    fixer.fix_all()

    logger.info("\n🎉 Documentation fixes complete!")
    logger.info(
        "   Run 'poetry run sphinx-build -b html source build/html' to rebuild"
    )


if __name__ == "__main__":
    main()
