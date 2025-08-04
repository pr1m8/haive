#!/usr/bin/env python3
"""Validate Python syntax with py_compile and commit fixes by package."""
from __future__ import annotations

import logging
import py_compile
import subprocess
from pathlib import Path
from typing import Dict
from typing import List
from typing import Set

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


class PackageValidator:
    """Validate and commit fixes for each package individually."""

    def __init__(self, packages_dir: Path):
        self.packages_dir = packages_dir
        self.package_names = [
            "haive-core",
            "haive-agents",
            "haive-tools",
            "haive-games",
            "haive-dataflow",
            "haive-mcp",
            "haive-prebuilt",
        ]

    def check_package_syntax(self, package_name: str) -> dict[str, list[str]]:
        """Check syntax for all Python files in a package."""
        package_dir = self.packages_dir / package_name
        if not package_dir.exists():
            logger.warning(f"Package directory not found: {package_dir}")
            return {"errors": [], "files_checked": []}

        logger.info(f"Checking syntax in package: {package_name}")

        errors = []
        files_checked = []

        # Find all Python files
        python_files = list(package_dir.rglob("*.py"))
        logger.info(f"Found {len(python_files)} Python files in {package_name}")

        for py_file in python_files:
            # Skip certain directories
            if any(
                part in str(py_file)
                for part in [".venv", "__pycache__", ".git", ".pytest_cache"]
            ):
                continue

            try:
                py_compile.compile(py_file, doraise=True)
                files_checked.append(str(py_file))
            except py_compile.PyCompileError as e:
                error_msg = f"SYNTAX ERROR in {py_file}: {e}"
                errors.append(error_msg)
                logger.exception(error_msg)
            except Exception as e:
                error_msg = f"COMPILE ERROR in {py_file}: {e}"
                errors.append(error_msg)
                logger.exception(error_msg)

        logger.info(
            f"Package {package_name}: {
    len(files_checked)} files OK, {
        len(errors)} errors"
        )
        return {"errors": errors, "files_checked": files_checked}

    def commit_package_changes(self, package_name: str, message: str) -> bool:
        """Commit changes in a specific package."""
        package_dir = self.packages_dir / package_name

        try:
            # Check if there are changes to commit
            result = subprocess.run(
                ["git", "status", "--porcelain", str(package_dir)],
                check=False,
                capture_output=True,
                text=True,
                cwd=self.packages_dir.parent,
            )

            if not result.stdout.strip():
                logger.info(f"No changes to commit in {package_name}")
                return True

            # Add package changes
            subprocess.run(
                ["git", "add", str(package_dir)],
                check=True,
                cwd=self.packages_dir.parent,
            )

            # Commit changes
            commit_msg = f"fix({package_name}): {message}\n\n🤖 Generated with Claude Code\n\nCo-Authored-By: Claude <noreply@anthropic.com>"

            subprocess.run(
                ["git", "commit", "-m", commit_msg],
                check=True,
                cwd=self.packages_dir.parent,
            )

            logger.info(f"✅ Committed changes in {package_name}")
            return True

        except subprocess.CalledProcessError as e:
            logger.exception(f"Failed to commit {package_name}: {e}")
            return False

    def push_changes(self) -> bool:
        """Push all committed changes."""
        try:
            subprocess.run(["git", "push"], check=True, cwd=self.packages_dir.parent)
            logger.info("✅ Pushed all changes to remote")
            return True
        except subprocess.CalledProcessError as e:
            logger.exception(f"Failed to push changes: {e}")
            return False

    def validate_all_packages(self) -> dict[str, dict]:
        """Validate syntax in all packages."""
        results = {}

        for package_name in self.package_names:
            results[package_name] = self.check_package_syntax(package_name)

        return results

    def fix_basic_syntax_errors(self, package_name: str) -> list[str]:
        """Fix basic syntax errors we can detect automatically."""
        fixed_files = []
        package_dir = self.packages_dir / package_name

        if not package_dir.exists():
            return fixed_files

        # Get files with syntax errors
        errors_result = self.check_package_syntax(package_name)
        error_files = set()

        for error in errors_result["errors"]:
            # Extract file path from error message
            if "SYNTAX ERROR in " in error:
                file_path = error.split("SYNTAX ERROR in ")[1].split(":")[0]
                error_files.add(Path(file_path))

        logger.info(
            f"Found {len(error_files)} files with syntax errors in {package_name}"
        )

        # Apply fixes to error files
        for py_file in error_files:
            if self.fix_file_syntax_errors(py_file):
                fixed_files.append(str(py_file))

        return fixed_files

    def fix_file_syntax_errors(self, py_file: Path) -> bool:
        """Fix syntax errors in a specific file."""
        if not py_file.exists():
            return False

        try:
            with open(py_file, encoding="utf-8") as f:
                content = f.read()

            original_content = content

            # Fix common escape sequence issues
            fixes = [
                # Fix regex escape sequences
                (r'"""([^"]*?)\\s\+([^"]*?)"""', r'r"""\1\\s+\2"""'),
                (r'"""([^"]*?)\\w\+([^"]*?)"""', r'r"""\1\\w+\2"""'),
                (r'"""([^"]*?)\\d\+([^"]*?)"""', r'r"""\1\\d+\2"""'),
                # Fix malformed Unicode strings
                (r'"([^"]*?)"\s*\*\s*🏛️"?', r'"\1 🏛️"'),
                # Fix unexpected indentation at start of files
                (r"^    ([a-zA-Z])", r"\1"),  # Remove leading spaces from first line
            ]

            for pattern, replacement in fixes:
                import re

                content = re.sub(
                    pattern, replacement, content, flags=re.MULTILINE | re.DOTALL
                )

            # Check if we actually fixed anything
            if content != original_content:
                # Test compile the fixed content
                try:
                    compile(content, str(py_file), "exec")
                    # If compilation succeeds, write the fix
                    with open(py_file, "w", encoding="utf-8") as f:
                        f.write(content)
                    logger.info(f"Fixed syntax errors in: {py_file}")
                    return True
                except SyntaxError as e:
                    logger.warning(f"Fix didn't resolve syntax error in {py_file}: {e}")
                    return False

        except Exception as e:
            logger.exception(f"Error fixing {py_file}: {e}")

        return False

    def run_fix_and_commit_cycle(self) -> dict[str, bool]:
        """Run the complete fix and commit cycle for all packages."""
        results = {}

        logger.info("Starting fix and commit cycle for all packages...")

        for package_name in self.package_names:
            logger.info(f"\n🔧 Processing package: {package_name}")

            # 1. Check current syntax status
            syntax_check = self.check_package_syntax(package_name)

            if not syntax_check["errors"]:
                logger.info(f"✅ {package_name}: No syntax errors found")
                results[package_name] = True
                continue

            # 2. Attempt to fix syntax errors
            logger.info(
                f"🛠️  Attempting to fix {
    len(
        syntax_check['errors'])} errors in {package_name}"
            )
            fixed_files = self.fix_basic_syntax_errors(package_name)

            if fixed_files:
                logger.info(f"Fixed {len(fixed_files)} files in {package_name}")

                # 3. Verify fixes worked
                post_fix_check = self.check_package_syntax(package_name)

                if len(post_fix_check["errors"]) < len(syntax_check["errors"]):
                    # 4. Commit the fixes
                    success = self.commit_package_changes(
                        package_name,
                        f"resolve syntax errors in {len(fixed_files)} files",
                    )
                    results[package_name] = success
                else:
                    logger.warning(f"Fixes didn't resolve errors in {package_name}")
                    results[package_name] = False
            else:
                logger.warning(
                    f"No files could be automatically fixed in {package_name}"
                )
                results[package_name] = False

        # 5. Push all changes
        if any(results.values()):
            self.push_changes()

        return results


def main():
    """Main execution."""
    script_dir = Path(__file__).parent
    packages_dir = script_dir.parent / "packages"

    if not packages_dir.exists():
        logger.error(f"Packages directory not found: {packages_dir}")
        return

    validator = PackageValidator(packages_dir)

    # Run the complete cycle
    results = validator.run_fix_and_commit_cycle()

    # Summary

    sum(1 for success in results.values() if success)

    for _package_name, success in results.items():
        passLED"


if __name__ == "__main__":
    main()
