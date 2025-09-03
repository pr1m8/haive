"""Base class for docstring fixers."""

import re
import subprocess
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Tuple


class BaseFixer(ABC):
    """Abstract base class for docstring fixers.

    Provides common functionality for all docstring fixer implementations.
    Each fixer targets specific pydocstyle error codes.
    """

    def __init__(self, error_codes: List[str], description: str):
        """Initialize the fixer.

        Args:
            error_codes: List of pydocstyle error codes this fixer handles.
            description: Human-readable description of what this fixer does.
        """
        self.error_codes = error_codes
        self.description = description
        self.fixes_applied = 0
        self.files_processed = 0

    @abstractmethod
    def fix_content(self, content: str) -> Tuple[str, int, List[str]]:
        """Fix docstring issues in the given content.

        Args:
            content: Original file content.

        Returns:
            Tuple of (fixed_content, fixes_count, list_of_changes_made).
        """
        pass

    def validate_with_pydocstyle(self, file_path: Path) -> Tuple[bool, List[str]]:
        """Validate file with pydocstyle and return relevant errors.

        Args:
            file_path: Path to file to validate.

        Returns:
            Tuple of (has_relevant_errors, list_of_relevant_error_messages).
        """
        try:
            result = subprocess.run(
                ["poetry", "run", "pydocstyle", "--convention=google", str(file_path)],
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode == 0:
                return False, []

            # Filter for errors this fixer handles
            relevant_errors = []
            for line in result.stdout.split("\n"):
                line = line.strip()
                if any(code in line for code in self.error_codes):
                    relevant_errors.append(line)

            return len(relevant_errors) > 0, relevant_errors

        except Exception as e:
            return True, [f"Error running pydocstyle: {e}"]

    def process_file(self, file_path: Path, dry_run: bool = False) -> Dict[str, Any]:
        """Process a single file with this fixer.

        Args:
            file_path: Path to file to process.
            dry_run: If True, don't write changes to disk.

        Returns:
            Dictionary with processing results.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                original_content = f.read()

            # Check for relevant errors before fixing
            has_errors_before, errors_before = self.validate_with_pydocstyle(file_path)

            # Apply fixes
            fixed_content, fixes_count, changes = self.fix_content(original_content)

            result = {
                "file": str(file_path),
                "success": True,
                "fixes_applied": fixes_count,
                "changes": changes,
                "had_relevant_errors_before": has_errors_before,
                "errors_before": errors_before,
                "validation_after": None,
                "remaining_errors": [],
                "error": None,
            }

            if fixes_count > 0 and not dry_run:
                # Write changes
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(fixed_content)

                # Validate after fixing
                has_errors_after, errors_after = self.validate_with_pydocstyle(
                    file_path
                )
                result["validation_after"] = has_errors_after
                result["remaining_errors"] = errors_after

                # Track statistics
                self.fixes_applied += fixes_count
                self.files_processed += 1

            return result

        except Exception as e:
            return {
                "file": str(file_path),
                "success": False,
                "fixes_applied": 0,
                "changes": [],
                "had_relevant_errors_before": False,
                "errors_before": [],
                "validation_after": None,
                "remaining_errors": [],
                "error": str(e),
            }

    def process_directory(
        self, directory: Path, dry_run: bool = False, recursive: bool = True
    ) -> Dict[str, Any]:
        """Process all Python files in a directory.

        Args:
            directory: Directory to process.
            dry_run: If True, don't write changes to disk.
            recursive: If True, process subdirectories.

        Returns:
            Dictionary with overall processing results.
        """
        if recursive:
            python_files = list(directory.rglob("*.py"))
        else:
            python_files = list(directory.glob("*.py"))

        results = []
        total_fixes = 0
        successful_files = 0
        files_with_fixes = 0

        for file_path in python_files:
            result = self.process_file(file_path, dry_run)
            results.append(result)

            if result["success"]:
                successful_files += 1
                if result["fixes_applied"] > 0:
                    files_with_fixes += 1
                    total_fixes += result["fixes_applied"]

        return {
            "fixer": self.__class__.__name__,
            "description": self.description,
            "error_codes": self.error_codes,
            "total_files": len(python_files),
            "successful_files": successful_files,
            "files_with_fixes": files_with_fixes,
            "total_fixes_applied": total_fixes,
            "dry_run": dry_run,
            "results": results,
        }

    def get_statistics(self) -> Dict[str, Any]:
        """Get fixer statistics.

        Returns:
            Dictionary with fixer statistics.
        """
        return {
            "fixer_name": self.__class__.__name__,
            "description": self.description,
            "error_codes": self.error_codes,
            "fixes_applied": self.fixes_applied,
            "files_processed": self.files_processed,
        }
