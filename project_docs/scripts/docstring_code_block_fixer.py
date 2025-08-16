#!/usr/bin/env python3
"""Fix Google-style docstring code blocks that cause AutoAPI import errors.

This script converts problematic '::' literal blocks to explicit '.. code-block:: python'
directives to prevent AutoAPI from trying to execute example code.

Usage:
    python fix_docstring_code_blocks.py --dry-run  # Preview changes
    python fix_docstring_code_blocks.py --check    # Validate files
    python fix_docstring_code_blocks.py --apply    # Apply fixes
"""

from __future__ import annotations

import argparse
import ast
from dataclasses import dataclass
import difflib
import logging
from pathlib import Path
import re
import subprocess
import sys
import tempfile

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


@dataclass
class FileIssue:
    """Track issues found in a file."""

    file_path: Path
    line_numbers: list[int]
    pattern_type: str
    original_content: str
    fixed_content: str | None = None
    validation_errors: list[str] = None


class DocstringFixer:
    """Fix Google-style docstring code blocks."""

    # Pattern to find problematic :: blocks in Examples sections
    EXAMPLE_PATTERN = re.compile(
        r"(Examples?:\s*\n)"  # Examples: header
        r"(\s*)([\w\s]+)::\s*\n"  # Description with ::
        r"((?:\s*\n)?)"  # Optional blank line
        r"((?:\s+.*\n)+)",  # Indented code block
        re.MULTILINE,
    )

    # Pattern to validate import statements in examples
    IMPORT_PATTERN = re.compile(r"^\s*(?:from|import)\s+[\w\.]+")

    def __init__(self, root_dir: Path = None):
        """Initialize the fixer with root directory."""
        self.root_dir = root_dir or Path.cwd()
        self.issues: list[FileIssue] = []

    def find_files_with_issues(self) -> list[Path]:
        """Find all Python files with problematic docstring patterns."""
        files_with_issues = []

        # Common patterns for files with provider/config examples
        patterns = [
            "providers/**/*.py",
            "config/**/*.py",
            "factory/**/*.py",
            "**/*provider*.py",
            "**/*config*.py",
        ]

        for pattern in patterns:
            for file_path in self.root_dir.rglob(pattern):
                if file_path.is_file() and file_path.suffix == ".py":
                    if self._has_problematic_pattern(file_path):
                        files_with_issues.append(file_path)

        return sorted(set(files_with_issues))

    def _has_problematic_pattern(self, file_path: Path) -> bool:
        """Check if file has problematic :: patterns in docstrings."""
        try:
            content = file_path.read_text()
            # Look for Examples: followed by :: blocks
            if "Examples:" in content and "::" in content:
                # More specific check for the pattern
                matches = self.EXAMPLE_PATTERN.findall(content)
                if matches:
                    logger.debug(
                        f"Found {len(matches)} problematic patterns in {file_path}",
                    )
                return len(matches) > 0
            return False
        except Exception as e:
            logger.warning(f"Error reading {file_path}: {e}")
            return False

    def fix_file(self,
                 file_path: Path,
                 dry_run: bool = True) -> FileIssue | None:
        """Fix problematic patterns in a single file."""
        try:
            content = file_path.read_text()
            original_content = content

            logger.debug(f"Processing {file_path}")

            # Track line numbers for reporting
            line_numbers = []

            def replacement(match):
                """Replace :: blocks with .. code-block:: python."""
                # Extract parts
                header = match.group(1)  # Examples:\n
                indent = match.group(2)  # Leading whitespace
                description = match.group(3)  # Description text
                blank = match.group(4)  # Optional blank line
                code_block = match.group(5)  # The code

                # Track line number
                line_num = content[:match.start()].count("\n") + 1
                line_numbers.append(line_num)

                # Build replacement
                result = f"{header}"
                result += f"{indent}{description}:\n"  # Remove double colon
                result += "\n"  # Always add blank line
                result += f"{indent}.. code-block:: python\n"
                result += "\n"  # Blank line after directive
                result += code_block

                return result

            # Apply fixes
            matches = list(self.EXAMPLE_PATTERN.finditer(content))
            logger.debug(f"Found {len(matches)} matches to fix")

            fixed_content = self.EXAMPLE_PATTERN.sub(replacement, content)

            if fixed_content != original_content:
                issue = FileIssue(
                    file_path=file_path,
                    line_numbers=line_numbers,
                    pattern_type="example_code_block",
                    original_content=original_content,
                    fixed_content=fixed_content,
                )

                if not dry_run:
                    file_path.write_text(fixed_content)
                    logger.info(f"Fixed {file_path}")

                return issue

        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
            return None

    def validate_file(self, file_path: Path) -> list[str]:
        """Validate a Python file for docstring issues."""
        errors = []

        try:
            content = file_path.read_text()

            # Check 1: Parse as valid Python
            try:
                ast.parse(content)
            except SyntaxError as e:
                errors.append(f"Syntax error: {e}")
                return errors

            # Check 2: Look for remaining :: patterns in Examples
            if "Examples:" in content:
                lines = content.split("\n")
                for i, line in enumerate(lines, 1):
                    if "::" in line and "Examples" in lines[max(0, i - 10):i]:
                        # Check if it's not already a code-block
                        if ".. code-block::" not in line:
                            errors.append(
                                f"Line {i}: Possible unfixed :: pattern")

            # Check 3: Validate RST syntax (if rstcheck is available)
            try:
                with tempfile.NamedTemporaryFile(
                        mode="w",
                        suffix=".rst",
                        delete=False,
                ) as tmp:
                    # Extract docstrings for RST validation
                    tree = ast.parse(content)
                    for node in ast.walk(tree):
                        if isinstance(
                                node,
                            (ast.FunctionDef, ast.ClassDef, ast.Module),
                        ):
                            docstring = ast.get_docstring(node)
                            if docstring:
                                tmp.write(docstring + "\n\n")
                    tmp.flush()

                    # Run rstcheck if available
                    result = subprocess.run(
                        ["rstcheck", tmp.name],
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    if result.returncode != 0:
                        errors.append(
                            f"RST validation errors: {result.stderr}")

            except (subprocess.CalledProcessError, FileNotFoundError):
                # rstcheck not available, skip RST validation
                pass
            except Exception as e:
                logger.debug(f"RST validation skipped: {e}")

        except Exception as e:
            errors.append(f"Validation error: {e}")

        return errors

    def show_diff(self, issue: FileIssue):
        """Show unified diff for a file change."""
        if not issue.fixed_content:
            return

        original_lines = issue.original_content.splitlines(keepends=True)
        fixed_lines = issue.fixed_content.splitlines(keepends=True)

        diff = difflib.unified_diff(
            original_lines,
            fixed_lines,
            fromfile=str(issue.file_path),
            tofile=str(issue.file_path) + " (fixed)",
            lineterm="",
        )

        print("\n".join(diff))

    def generate_report(self, issues: list[FileIssue]) -> str:
        """Generate a summary report of all issues."""
        report = []
        report.append("=" * 80)
        report.append("DOCSTRING CODE BLOCK FIX REPORT")
        report.append("=" * 80)
        report.append(f"\nTotal files with issues: {len(issues)}")
        report.append(
            f"Total patterns found: {sum(len(i.line_numbers) for i in issues)}",
        )

        if issues:
            report.append("\nFiles requiring fixes:")
            for issue in issues:
                report.append(f"\n  {issue.file_path}")
                report.append(
                    f"    Lines: {', '.join(map(str, issue.line_numbers))}")
                if issue.validation_errors:
                    report.append(
                        f"    Validation errors: {len(issue.validation_errors)}",
                    )

        report.append("\n" + "=" * 80)
        return "\n".join(report)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Fix Google-style docstring code blocks for AutoAPI compatibility", )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without modifying files",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate files for remaining issues",
    )
    parser.add_argument("--apply",
                        action="store_true",
                        help="Apply fixes to all files")
    parser.add_argument(
        "--path",
        type=Path,
        default=Path.cwd(),
        help="Root path to search for files (default: current directory)",
    )
    parser.add_argument(
        "--file",
        type=Path,
        help="Process a single file instead of searching",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show detailed output",
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Validate arguments
    if sum([args.dry_run, args.check, args.apply]) != 1:
        parser.error(
            "Exactly one of --dry-run, --check, or --apply must be specified")

    fixer = DocstringFixer(args.path)

    # Process single file or find all files
    if args.file:
        files_to_process = [args.file] if args.file.exists() else []
    else:
        logger.info(
            "Searching for files with problematic docstring patterns...")
        files_to_process = fixer.find_files_with_issues()

    if not files_to_process:
        logger.info("No files found with problematic patterns!")
        return 0

    logger.info(f"Found {len(files_to_process)} files to process")

    issues = []
    validation_failed = False

    # Process each file
    for file_path in files_to_process:
        if args.check:
            # Validation mode
            errors = fixer.validate_file(file_path)
            if errors:
                logger.error(f"\n{file_path} has validation errors:")
                for error in errors:
                    logger.error(f"  - {error}")
                validation_failed = True
            else:
                logger.info(f"{file_path}: OK")

        else:
            # Fix mode (dry-run or apply)
            issue = fixer.fix_file(file_path, dry_run=args.dry_run)
            if issue:
                issues.append(issue)

                if args.dry_run:
                    print(f"\n{'=' * 80}")
                    print(f"Changes for: {file_path}")
                    print("=" * 80)
                    fixer.show_diff(issue)

                # Validate the fixed content
                if issue.fixed_content:
                    # Create temp file for validation
                    with tempfile.NamedTemporaryFile(
                            mode="w",
                            suffix=".py",
                            delete=False,
                    ) as tmp:
                        tmp.write(issue.fixed_content)
                        tmp.flush()
                        errors = fixer.validate_file(Path(tmp.name))
                        if errors:
                            issue.validation_errors = errors
                            validation_failed = True

    # Generate report
    if issues:
        print("\n" + fixer.generate_report(issues))

    # Final summary
    if args.dry_run:
        print("\nThis was a DRY RUN. No files were modified.")
        print("To apply these changes, run with --apply")

    if validation_failed:
        logger.error(
            "\nValidation failed! Fix validation errors before applying changes.",
        )
        return 1

    if args.apply and issues:
        logger.info(f"\nSuccessfully fixed {len(issues)} files!")

    return 0


if __name__ == "__main__":
    sys.exit(main())
