#!/usr/bin/env python3
"""Comprehensive documentation fix script for Haive project."""

import logging
import os
import re
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def fix_rst_title_underlines():
    """Fix RST title underline issues in all files."""
    logger.info("📝 Fixing RST title underlines...")

    docs_dir = Path("docs/source")
    if not docs_dir.exists():
        logger.warning(f"  ⚠️  {docs_dir} not found")
        return 0

    fixed_count = 0

    # Find all RST files
    for rst_file in docs_dir.rglob("*.rst"):
        try:
            with open(rst_file, encoding="utf-8") as f:
                lines = f.readlines()

            fixed = False
            fixed_lines = []
            i = 0

            while i < len(lines):
                line = lines[i]

                # Check if next line is an underline
                if i + 1 < len(lines):
                    next_line = lines[i + 1]
                    # RST underline characters
                    if next_line.strip() and all(
                        c in '=-~^"+*#' for c in next_line.strip()
                    ):
                        title_length = len(line.rstrip())
                        underline_char = next_line.strip()[0]
                        current_underline_length = len(next_line.strip())

                        if (
                            current_underline_length != title_length
                            and title_length > 0
                        ):
                            correct_underline = underline_char * title_length + "\n"
                            fixed_lines.append(line)
                            fixed_lines.append(correct_underline)
                            fixed = True
                            i += 2
                            continue

                fixed_lines.append(line)
                i += 1

            if fixed:
                with open(rst_file, "w", encoding="utf-8") as f:
                    f.writelines(fixed_lines)
                logger.info(f"  ✓ Fixed: {rst_file}")
                fixed_count += 1

        except Exception as e:
            logger.exception(f"  ✗ Error fixing {rst_file}: {e}")

    return fixed_count


def fix_showcase_grid():
    """Fix showcase index grid structure."""
    logger.info("🎨 Fixing showcase grid structure...")

    showcase_file = Path("docs/source/agents/showcase_index.rst")
    if not showcase_file.exists():
        logger.warning(f"  ⚠️  {showcase_file} not found")
        return 0

    try:
        with open(showcase_file, encoding="utf-8") as f:
            content = f.read()

        original_content = content

        # Fix empty grid directive
        if ".. grid::" in content and "Content block expected" in str(content):
            content = re.sub(
                r"(\.\. grid::)\s*\n(\s*\n)*(\s*\.\. grid-item::)",
                r"\1\n   :gutter: 3\n   :class-container: showcase-grid\n\n   .. grid-row::\n\n\3",
                content,
                flags=re.MULTILINE,
            )

        # Fix toctree with multiple items on one line
        content = re.sub(
            r"(\s+)(\w+_showcase)\s+(\w+_showcase)\s+(\w+_showcase)",
            r"\1\2\n\1\3\n\1\4",
            content,
        )

        if content != original_content:
            with open(showcase_file, "w", encoding="utf-8") as f:
                f.write(content)
            logger.info("  ✓ Fixed showcase grid"d")
            return 1

    except Exception as e:
        logger.exception(f"  ✗ Error fixing showcase: {e}")

    return 0


def fix_specific_docstring_file():
    """Fix the specific field_definition.py file that's causing many warnings."""
    logger.info("🐍 Fixing specific docstring issues...")

    file_path = Path("packages/haive-core/src/haive/core/schema/field_definition.py")
    if not file_path.exists():
        logger.warning(f"  ⚠️  {file_path} not found")
        return 0

    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        original_content = content

        # Fix common docstring issues
        # Fix incomplete backticks (single backtick without closing)
        content = re.sub(r"([^`])`([^`\s][^`]*?)([^`])\s", r"\1``\2\3`` ", content)

        # Fix indentation issues in docstrings
        # This is a simple fix - more complex issues need manual review
        lines = content.split("\n")
        fixed_lines = []

        for line in lines:
            # Fix some specific patterns that cause warnings
            if "FieldInfo`" in line and "`FieldInfo" not in line:
                line = line.replace("FieldInfo`", "``FieldInfo``")
            if "pydantic.Field`" in line and "`pydantic.Field" not in line:
                line = line.replace("pydantic.Field`", "``pydantic.Field``")

            fixed_lines.append(line)

        content = "\n".join(fixed_lines)

        if content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            logger.info("  ✓ Fixed docstrings in field_definition.py"y")
            return 1

    except Exception as e:
        logger.exception(f"  ✗ Error fixing docstrings: {e}")

    return 0


def remove_duplicate_files():
    """Remove duplicate index files and other duplicates."""
    logger.info("🧹 Removing duplicate files...")

    docs_source = Path("docs/source")
    if not docs_source.exists():
        return 0

    removed_count = 0

    # Remove duplicate index files (prefer .rst over .md)
    for dir_path in docs_source.rglob("**/"):
        if dir_path.is_dir():
            rst_index = dir_path / "index.rst"
            md_index = dir_path / "index.md"

            if rst_index.exists() and md_index.exists():
                md_index.unlink()
                logger.info(f"  ✓ Removed duplicate: {md_index}")
                removed_count += 1

    return removed_count


def main():
    """Run all documentation fixes."""
    logger.info("🔧 Starting comprehensive documentation fixes...\n")

    total_fixes = 0

    # Run all fixes
    total_fixes += fix_rst_title_underlines()
    total_fixes += fix_showcase_grid()
    total_fixes += fix_specific_docstring_file()
    total_fixes += remove_duplicate_files()

    logger.info(f"\n✅ Applied {total_fixes} fixes!")

    if total_fixes > 0:
        logger.info("\n🔄 Rebuilding documentation...")
        # Rebuild docs to see improvement
        os.system(
            "cd docs && poetry run sphinx-build -b html source build/html > /dev/null 2>&1"
        )

        # Count remaining warnings
        result = os.popen(
            "cd docs && poetry run sphinx-build -b html source build/html 2>&1 | grep -E 'WARNING|ERROR' | wc -l"
        ).read()
        warnings_count = int(result.strip())
        logger.info(f"📊 Remaining warnings: {warnings_count}")

    logger.info("\n🎉 Documentation fixes complete!")


if __name__ == "__main__":
    main()
