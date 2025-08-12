"""Configurable D100 and D107 fixer with customizable templates and settings.

This module provides a more sophisticated version of the D100/D107 fixer that
allows custom configuration for docstring generation.
"""

import ast
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import jinja2
import toml

from .base_fixer import BaseFixer


class ConfigurableDocstringFixer:
    """Configurable docstring fixer with custom templates and settings."""

    def __init__(self, config_path: Optional[Path] = None):
        """Initialize configurable fixer.

        Args:
            config_path: Path to configuration file (pyproject.toml or custom).
        """
        self.config = self._load_config(config_path)
        self.formatter = self.config.get("formatter", "google")
        self.indent = self.config.get("indent", 4)
        self.template_path = self.config.get("template_path")
        self.omit_patterns = self.config.get("omit", [])

        # Load custom templates if provided
        if self.template_path:
            self.template_env = jinja2.Environment(
                loader=jinja2.FileSystemLoader(self.template_path)
            )
        else:
            self.template_env = None

    def _load_config(self, config_path: Optional[Path] = None) -> dict:
        """Load configuration from file or defaults.

        Args:
            config_path: Path to config file.

        Returns:
            Configuration dictionary.
        """
        # Default configuration
        default_config = {
            "formatter": "google",
            "indent": 4,
            "omit": ["test_*.py", "*_test.py", "tests/*"],
        }

        # Try to load from pyproject.toml
        if config_path is None:
            # Look for pyproject.toml in current directory or parent directories
            current = Path.cwd()
            while current != current.parent:
                pyproject_path = current / "pyproject.toml"
                if pyproject_path.exists():
                    config_path = pyproject_path
                    break
                current = current.parent

        if config_path and config_path.exists():
            try:
                with open(config_path, "r") as f:
                    data = toml.load(f)
                    if "tool" in data and "doq" in data["tool"]:
                        # Merge with defaults
                        config = default_config.copy()
                        config.update(data["tool"]["doq"])
                        return config
            except Exception as e:
                print(f"Warning: Could not load config from {config_path}: {e}")

        return default_config

    def should_skip_file(self, file_path: Path) -> bool:
        """Check if file should be skipped based on omit patterns.

        Args:
            file_path: Path to check.

        Returns:
            True if file should be skipped.
        """
        file_str = str(file_path)
        for pattern in self.omit_patterns:
            if "*" in pattern:
                # Simple glob matching
                import fnmatch

                if fnmatch.fnmatch(file_str, pattern):
                    return True
            elif pattern in file_str:
                return True
        return False

    def fix_file(
        self,
        file_path: Path,
        dry_run: bool = False,
        custom_config: Optional[dict] = None,
    ) -> Dict[str, Any]:
        """Fix D100 and D107 issues in a file with configuration.

        Args:
            file_path: Path to Python file.
            dry_run: If True, show what would be done.
            custom_config: Override configuration for this file.

        Returns:
            Result dictionary.
        """
        if not file_path.exists():
            return {"success": False, "error": "File not found"}

        # Check if file should be skipped
        if self.should_skip_file(file_path):
            return {
                "success": True,
                "file": str(file_path),
                "skipped": True,
                "reason": "File matches omit pattern",
            }

        # Use custom config if provided
        config = custom_config or self.config
        formatter = config.get("formatter", self.formatter)

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
                changes.append(f"Would add module docstring ({formatter} style)")
            if d107_count > 0:
                changes.append(
                    f"Would add {d107_count} __init__ docstring(s) ({formatter} style)"
                )

            return {
                "success": True,
                "file": str(file_path),
                "d100_needed": d100_needed,
                "d107_needed": d107_count,
                "formatter": formatter,
                "dry_run": True,
                "changes": changes,
            }

        # Run doq with specified formatter
        try:
            # Build doq command
            cmd = ["poetry", "run", "doq", f"--formatter={formatter}"]

            # Add template path if configured
            if self.template_path:
                cmd.extend(["--template_path", str(self.template_path)])

            cmd.append(str(file_path))

            result = subprocess.run(cmd, capture_output=True, text=True)

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
                    changes.append(f"Added module docstring ({formatter} style)")
                if d107_fixed > 0:
                    changes.append(
                        f"Added {d107_fixed} __init__ docstring(s) ({formatter} style)"
                    )

                return {
                    "success": True,
                    "file": str(file_path),
                    "formatter": formatter,
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

    def get_config_info(self) -> dict:
        """Get current configuration information.

        Returns:
            Configuration details.
        """
        return {
            "formatter": self.formatter,
            "indent": self.indent,
            "template_path": str(self.template_path) if self.template_path else None,
            "omit_patterns": self.omit_patterns,
            "config": self.config,
        }


# Example custom template strings for different styles
CUSTOM_TEMPLATES = {
    "haive_module": '''"""{{ module_name|replace('_', ' ')|title }} module.

This module provides functionality for {{ purpose|default('specialized operations') }}.

Key Components:
{% for component in components %}
    - {{ component.name }}: {{ component.description }}
{% endfor %}

Usage:
    from {{ import_path }} import {{ main_export }}
    
    # Example usage
    {{ example_code|indent(4) }}
"""''',
    "haive_init": '''"""Initialize {{ class_name }} instance.

Creates a new instance of {{ class_name }} with the specified configuration.

Args:
{% for arg in args %}
    {{ arg.name }}{% if arg.type %} ({{ arg.type }}){% endif %}: {{ arg.description }}
        {% if arg.constraints %}Constraints: {{ arg.constraints }}.{% endif %}
        {% if arg.default %}Default: {{ arg.default }}.{% endif %}
{% endfor %}

{% if raises %}
Raises:
{% for exc in raises %}
    {{ exc.type }}: {{ exc.description }}.
{% endfor %}
{% endif %}

{% if notes %}
Notes:
    {{ notes|indent(4) }}
{% endif %}
"""''',
}
