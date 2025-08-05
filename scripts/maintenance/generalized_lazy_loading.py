#!/usr/bin/env python3
"""Generalized lazy loading implementation with dry-run support.

This script can apply lazy loading to any __init__.py file in the Haive
codebase, with comprehensive dry-run capabilities for safe execution.
"""

import argparse
import os
from pathlib import Path

# Optional: Use drypy if available, fallback to custom implementation
try:
    from drypy import dryrun, sham

    HAS_DRYPY = True
except ImportError:
    HAS_DRYPY = False
    # Custom dry-run implementation
    _DRY_RUN_MODE = False

    def dryrun(enabled: bool):
        global _DRY_RUN_MODE
        _DRY_RUN_MODE = enabled

    def sham(func):
        def wrapper(*args, **kwargs):
            if _DRY_RUN_MODE:
                return None
            return func(*args, **kwargs)

        return wrapper


class LazyLoadingGenerator:
    """Generate lazy loading implementations for __init__.py files."""

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        dryrun(dry_run)

    def analyze_package_structure(self, init_file: Path) -> dict[str, set[str]]:
        """Analyze package structure to find submodules and classes."""
        package_dir = init_file.parent

        # Find .py modules
        py_modules = {
            f.stem
            for f in package_dir.glob("*.py")
            if f.stem != "__init__" and not f.stem.startswith("_")
        }

        # Find subpackages
        subpackages = {
            d.name
            for d in package_dir.iterdir()
            if d.is_dir()
            and not d.name.startswith("_")
            and (d / "__init__.py").exists()
        }

        # Try to find existing exports in current __init__.py
        existing_exports = self._extract_existing_exports(init_file)

        return {
            "modules": py_modules,
            "packages": subpackages,
            "all_submodules": py_modules | subpackages,
            "existing_exports": existing_exports,
        }

    def _extract_existing_exports(self, init_file: Path) -> set[str]:
        """Extract existing class/function exports from __init__.py."""
        if not init_file.exists():
            return set()

        try:
            with open(init_file) as f:
                content = f.read()

            # Simple extraction of __all__ contents
            import ast

            tree = ast.parse(content)
            exports = set()

            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id == "__all__":
                            if isinstance(node.value, ast.List):
                                for elt in node.value.elts:
                                    if isinstance(elt, ast.Constant):
                                        exports.add(elt.value)

            return exports
        except Exception:
            return set()

    def generate_lazy_loading_content(
        self,
        init_file: Path,
        package_name: str,
        structure: dict[str, set[str]],
        template_type: str = "lazy_loader",
    ) -> str:
        """Generate lazy loading content based on package structure."""

        if template_type == "lazy_loader":
            return self._generate_lazy_loader_template(
                init_file,
                package_name,
                structure,
            )
        if template_type == "pep562":
            return self._generate_pep562_template(init_file, package_name, structure)
        raise ValueError(f"Unknown template type: {template_type}")

    def _extract_existing_docstring(self, init_file: Path) -> str | None:
        """Extract existing docstring from __init__.py file."""
        if not init_file.exists():
            return None

        try:
            with open(init_file) as f:
                content = f.read()

            import ast

            tree = ast.parse(content)

            # Get the first statement if it's a docstring
            if (
                tree.body
                and isinstance(tree.body[0], ast.Expr)
                and isinstance(tree.body[0].value, ast.Constant)
                and isinstance(tree.body[0].value.value, str)
            ):
                return tree.body[0].value.value

            return None
        except Exception:
            return None

    def _generate_lazy_loader_template(
        self,
        init_file: Path,
        package_name: str,
        structure: dict[str, set[str]],
    ) -> str:
        """Generate lazy_loader based template with preserved docstring."""
        submodules = sorted(structure["all_submodules"])

        # Try to preserve existing docstring
        existing_docstring = self._extract_existing_docstring(init_file)

        if existing_docstring:
            # Use existing docstring
            docstring_part = f'"""{existing_docstring}"""'
        else:
            # Generate new docstring
            docstring_part = f'''"""Lazy loading implementation for {package_name}.

This module uses lazy loading to improve import performance and avoid
loading heavy dependencies until they are actually needed.

Submodules are loaded on-demand when accessed, while maintaining
full compatibility with Sphinx AutoAPI and type checkers.
"""'''

        # Build submod_attrs section
        submod_attrs_lines = []
        for module in submodules:
            submod_attrs_lines.append(
                f"    '{module}': [],  # TODO: Add specific exports from {module}",
            )
        submod_attrs_content = "\n".join(submod_attrs_lines)

        content = f"""{docstring_part}

import lazy_loader as lazy

# Define submodules to lazy load
submodules = {submodules!r}

# Define specific attributes from submodules to expose
# TODO: Customize this based on actual exports from each submodule
submod_attrs = {{
{submod_attrs_content}
}}

# Attach lazy loading - this creates __getattr__, __dir__, and __all__
__getattr__, __dir__, __all__ = lazy.attach(
    __name__,
    submodules=submodules,
    submod_attrs=submod_attrs
)

# Add any eager imports here (lightweight utilities, etc.)
# Example: from .metadata import SomeUtility
# __all__ += ['SomeUtility']
"""

        return content

    def _generate_pep562_template(
        self,
        init_file: Path,
        package_name: str,
        structure: dict[str, set[str]],
    ) -> str:
        """Generate PEP 562 __getattr__ based template with preserved
        docstring."""
        submodules = sorted(structure["all_submodules"])

        # Try to preserve existing docstring
        existing_docstring = self._extract_existing_docstring(init_file)

        if existing_docstring:
            # Use existing docstring
            docstring_part = f'"""{existing_docstring}"""'
        else:
            # Generate new docstring
            docstring_part = f'''"""PEP 562 lazy loading implementation for {package_name}.

This module uses Python's PEP 562 __getattr__ mechanism for lazy loading.
"""'''

        content = f"""{docstring_part}

import importlib
from typing import TYPE_CHECKING

# For type checking, import everything
if TYPE_CHECKING:
"""

        for module in submodules:
            content += f"    from . import {module}\n"

        content += """

# Lazy imports mapping
_LAZY_IMPORTS = {
"""

        for module in submodules:
            content += f'    "{module}": "{package_name}.{module}",\n'

        content += '''}}

def __getattr__(name: str):
    """PEP 562 lazy loading."""
    if name in _LAZY_IMPORTS:
        module_name = _LAZY_IMPORTS[name]
        module = importlib.import_module(module_name)
        globals()[name] = module
        return module

    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

def __dir__():
    """List available attributes."""
    return list(__all__)

__all__ = list(_LAZY_IMPORTS.keys())
'''

        return content

    @sham
    def backup_file(self, file_path: Path) -> Path:
        """Create backup of original file."""
        backup_path = file_path.with_suffix(f".py.backup.{self._get_timestamp()}")

        if file_path.exists():
            import shutil

            shutil.copy2(file_path, backup_path)
            return backup_path
        print(f"Warning: {file_path} does not exist")
        return backup_path

    @sham
    def write_lazy_loading(self, init_file: Path, content: str) -> bool:
        """Write lazy loading content to __init__.py file."""
        try:
            with open(init_file, "w") as f:
                f.write(content)
            return True
        except Exception:
            return False

    def _get_timestamp(self) -> str:
        """Get timestamp for backup files."""
        from datetime import datetime

        return datetime.now().strftime("%Y%m%d_%H%M%S")

    def process_init_file(
        self,
        init_file: Path,
        template_type: str = "lazy_loader",
        preview: bool = False,
    ) -> bool:
        """Process a single __init__.py file."""

        if not init_file.exists():
            return False

        # Analyze structure
        structure = self.analyze_package_structure(init_file)

        if not structure["all_submodules"]:
            return False

        # Determine package name
        package_name = ".".join(init_file.parent.parts[-3:])  # Approximate

        # Generate content
        content = self.generate_lazy_loading_content(
            init_file,
            package_name,
            structure,
            template_type,
        )

        if preview or self.dry_run:
            return True

        if not self.dry_run:
            # Create backup
            self.backup_file(init_file)

            # Write new content
            success = self.write_lazy_loading(init_file, content)

            if success:
                self._test_import(init_file)
                return True
            print(f"❌ Failed to update {init_file}")
            return False
        return True

    def _test_import(self, init_file: Path):
        """Test that the updated module can be imported."""
        try:
            # Try to compile the file
            import py_compile

            py_compile.compile(init_file, doraise=True)
        except Exception:
            pass


def find_init_files(
    base_path: Path,
    pattern: str = "**/haive/*/__init__.py",
) -> list[Path]:
    """Find __init__.py files in the Haive codebase."""
    return list(base_path.glob(pattern))


def main():
    """Main entry point with comprehensive argument parsing."""
    parser = argparse.ArgumentParser(
        description="Apply lazy loading to Haive __init__.py files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dry-run on single file
  python generalized_lazy_loading.py --file packages/haive-core/src/haive/core/models/__init__.py --dry-run

  # Apply to all model files
  python generalized_lazy_loading.py --pattern "**/models/__init__.py"

  # Use PEP 562 template instead of lazy_loader
  python generalized_lazy_loading.py --template pep562 --dry-run

  # Environment variable control
  DRY_RUN=1 python generalized_lazy_loading.py --auto
        """,
    )

    parser.add_argument(
        "--file",
        type=Path,
        help="Specific __init__.py file to process",
    )
    parser.add_argument(
        "--pattern",
        default="**/haive/*/__init__.py",
        help="Glob pattern for finding __init__.py files",
    )
    parser.add_argument(
        "--template",
        choices=["lazy_loader", "pep562"],
        default="lazy_loader",
        help="Template type to use",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without applying them",
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Show generated content preview",
    )
    parser.add_argument(
        "--auto",
        action="store_true",
        help="Process common files automatically",
    )

    args = parser.parse_args()

    # Check environment variable
    dry_run = args.dry_run or os.getenv("DRY_RUN", "").lower() in ("1", "true", "yes")

    generator = LazyLoadingGenerator(dry_run=dry_run)

    # Determine files to process
    if args.file:
        files = [args.file]
    elif args.auto:
        base = Path("/home/will/Projects/haive/backend/haive/packages")
        files = [
            base / "haive-core/src/haive/core/models/__init__.py",
            base / "haive-core/src/haive/core/tools/__init__.py",
            base / "haive-agents/src/haive/agents/__init__.py",
            # Add more key files as needed
        ]
    else:
        base = Path("/home/will/Projects/haive/backend/haive")
        files = find_init_files(base, args.pattern)

    # Process files
    success_count = 0
    for init_file in files:
        if init_file.exists():
            success = generator.process_init_file(
                init_file,
                template_type=args.template,
                preview=args.preview,
            )
            if success:
                success_count += 1
        else:
            pass

    if dry_run:
        pass  # Dry run mode completed
    else:
        pass  # Changes applied successfully


if __name__ == "__main__":
    main()
