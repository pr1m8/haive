"""Simple D100 and D107 fixer using doq for template-based docstring generation.

This module uses the doq library to generate docstrings for missing module
and __init__ method docstrings, providing a simpler alternative to custom AST parsing.
"""

import ast
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Tuple

from .base_fixer import BaseFixer


class D100SimpleFixer(BaseFixer):
    """Simple fixer for D100: Missing module docstring using doq."""

    def __init__(self):
        """Initialize D100 simple fixer."""
        super().__init__(
            error_codes=["D100"],
            description="Add missing module docstrings using doq templates",
        )

    def fix_content(self, content: str) -> Tuple[str, int, List[str]]:
        """Fix D100 issues in content using doq.

        Args:
            content: Original file content.

        Returns:
            Tuple of (fixed_content, fixes_count, list_of_changes_made).
        """
        # Skip empty or whitespace-only content
        if not content or not content.strip():
            return content, 0, []

        # Check if module already has docstring
        if self._has_module_docstring(content):
            return content, 0, []

        # Use doq to generate docstring
        try:
            # Write content to temp file
            with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
                f.write(content)
                temp_path = f.name

            # Run doq with Google format (simpler than Sphinx)
            result = subprocess.run(
                ["poetry", "run", "doq", "--formatter=google", temp_path],
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                # Read the modified content
                with open(temp_path, "r") as f:
                    fixed_content = f.read()

                # Check if docstring was added
                if fixed_content != content and self._has_module_docstring(
                    fixed_content
                ):
                    return fixed_content, 1, ["Added module docstring using doq"]

            return content, 0, []

        except Exception as e:
            print(f"Error running doq: {e}")
            return content, 0, []

        finally:
            # Clean up temp file
            if "temp_path" in locals():
                Path(temp_path).unlink(missing_ok=True)

    def _has_module_docstring(self, content: str) -> bool:
        """Check if module already has a docstring."""
        try:
            tree = ast.parse(content)
            return ast.get_docstring(tree) is not None
        except:
            return False


class D107SimpleFixer(BaseFixer):
    """Simple fixer for D107: Missing __init__ method docstring using doq."""

    def __init__(self):
        """Initialize D107 simple fixer."""
        super().__init__(
            error_codes=["D107"],
            description="Add missing __init__ method docstrings using doq",
        )

    def fix_content(self, content: str) -> Tuple[str, int, List[str]]:
        """Fix D107 issues in content using doq.

        Args:
            content: Original file content.

        Returns:
            Tuple of (fixed_content, fixes_count, list_of_changes_made).
        """
        # Skip empty or whitespace-only content
        if not content or not content.strip():
            return content, 0, []

        # First check if there are any __init__ methods without docstrings
        if not self._has_missing_init_docstrings(content):
            return content, 0, []

        try:
            # Write content to temp file
            with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
                f.write(content)
                temp_path = f.name

            # Run doq with Google format
            result = subprocess.run(
                ["poetry", "run", "doq", "--formatter=google", temp_path],
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                # Read the modified content
                with open(temp_path, "r") as f:
                    fixed_content = f.read()

                # Count how many __init__ docstrings were added
                original_missing = self._count_missing_init_docstrings(content)
                fixed_missing = self._count_missing_init_docstrings(fixed_content)
                fixes_count = original_missing - fixed_missing

                if fixes_count > 0:
                    changes = [f"Added {fixes_count} __init__ docstring(s) using doq"]
                    return fixed_content, fixes_count, changes

            return content, 0, []

        except Exception as e:
            print(f"Error running doq: {e}")
            return content, 0, []

        finally:
            # Clean up temp file
            if "temp_path" in locals():
                Path(temp_path).unlink(missing_ok=True)

    def _has_missing_init_docstrings(self, content: str) -> bool:
        """Check if any __init__ methods are missing docstrings."""
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    for item in node.body:
                        if (
                            isinstance(item, ast.FunctionDef)
                            and item.name == "__init__"
                            and ast.get_docstring(item) is None
                        ):
                            return True
            return False
        except:
            return False

    def _count_missing_init_docstrings(self, content: str) -> int:
        """Count how many __init__ methods are missing docstrings."""
        count = 0
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    for item in node.body:
                        if (
                            isinstance(item, ast.FunctionDef)
                            and item.name == "__init__"
                            and ast.get_docstring(item) is None
                        ):
                            count += 1
        except:
            pass
        return count


class CombinedD100D107Fixer:
    """Combined fixer that handles both D100 and D107 in one pass using doq."""

    def __init__(self):
        """Initialize combined fixer."""
        self.description = (
            "Fix both D100 (module) and D107 (__init__) docstrings using doq"
        )

    def fix_file(self, file_path: Path, dry_run: bool = False) -> Dict[str, Any]:
        """Fix both D100 and D107 issues in a single file.

        Args:
            file_path: Path to Python file.
            dry_run: If True, show what would be fixed without changing.

        Returns:
            Dictionary with results.
        """
        if not file_path.exists():
            return {"success": False, "error": "File not found"}

        # Read original content
        original_content = file_path.read_text()

        # Check what needs fixing
        d100_needed = self._needs_module_docstring(original_content)
        d107_count = self._count_missing_init_docstrings(original_content)

        if not d100_needed and d107_count == 0:
            return {
                "success": True,
                "file": str(file_path),
                "d100_fixed": False,
                "d107_fixed": 0,
                "changes": [],
            }

        if dry_run:
            changes = []
            if d100_needed:
                changes.append("Would add module docstring")
            if d107_count > 0:
                changes.append(f"Would add {d107_count} __init__ docstring(s)")

            return {
                "success": True,
                "file": str(file_path),
                "d100_needed": d100_needed,
                "d107_needed": d107_count,
                "dry_run": True,
                "changes": changes,
            }

        # Run doq on the file
        try:
            result = subprocess.run(
                ["poetry", "run", "doq", "--formatter=google", str(file_path)],
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                # Read the modified content
                fixed_content = file_path.read_text()

                # Check what was actually fixed
                d100_fixed = d100_needed and not self._needs_module_docstring(
                    fixed_content
                )
                d107_fixed = d107_count - self._count_missing_init_docstrings(
                    fixed_content
                )

                changes = []
                if d100_fixed:
                    changes.append("Added module docstring")
                if d107_fixed > 0:
                    changes.append(f"Added {d107_fixed} __init__ docstring(s)")

                return {
                    "success": True,
                    "file": str(file_path),
                    "d100_fixed": d100_fixed,
                    "d107_fixed": d107_fixed,
                    "changes": changes,
                }
            else:
                return {
                    "success": False,
                    "file": str(file_path),
                    "error": f"doq failed: {result.stderr}",
                }

        except Exception as e:
            return {"success": False, "file": str(file_path), "error": str(e)}

    def _needs_module_docstring(self, content: str) -> bool:
        """Check if module needs docstring."""
        try:
            tree = ast.parse(content)
            return ast.get_docstring(tree) is None
        except:
            return False

    def _count_missing_init_docstrings(self, content: str) -> int:
        """Count missing __init__ docstrings."""
        count = 0
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    for item in node.body:
                        if (
                            isinstance(item, ast.FunctionDef)
                            and item.name == "__init__"
                            and ast.get_docstring(item) is None
                        ):
                            count += 1
        except:
            pass
        return count
