#!/usr/bin/env python3
"""Haive File Normalizer and Import Fixer

A comprehensive utility for the Haive polyrepo framework:
1. Normalizing file names in directories
2. Removing common prefixes and suffixes
3. Deduplicating files (keeping newest)
4. Fixing imports using libcst for Haive namespace packages
5. Download management and normalization

Haive Structure:
- Files: packages/haive-games/src/haive/games/holdem/engines.py
- Imports: from haive.games.holdem.engines import ...

Usage:
    python file_normalizer.py normalize <directory>
    python file_normalizer.py fix-imports <directory> --target-package haive.games.holdem
    python file_normalizer.py download-normalize <download-pattern> <destination>
    python file_normalizer.py all <directory> --target-package haive.games.holdem
"""

import argparse
import re
import shutil
import sys
from pathlib import Path

# Rich imports for beautiful CLI
from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
)
from rich.table import Table

# Import fixing dependencies
try:
    import libcst as cst
    from libcst import matchers as m

    LIBCST_AVAILABLE = True
except ImportError:
    LIBCST_AVAILABLE = False

console = Console()


class HaivePathResolver:
    """Resolves Haive polyrepo paths and import statements."""

    @staticmethod
    def detect_haive_root(current_path: Path) -> Path | None:
        """Find the Haive polyrepo root by looking for packages/ directory."""
        path = Path(current_path).resolve()

        # Look up the directory tree for packages/ folder
        for parent in [path] + list(path.parents):
            packages_dir = parent / "packages"
            if packages_dir.exists() and packages_dir.is_dir():
                # Verify it looks like Haive structure
                haive_packages = list(packages_dir.glob("haive-*"))
                if haive_packages:
                    return parent

        return None

    @staticmethod
    def resolve_import_path(file_path: Path) -> str | None:
        """Convert file path to proper Haive import path."""
        path = Path(file_path).resolve()

        # Find src/haive/ in the path
        parts = path.parts
        try:
            # Look for the pattern: .../src/haive/...
            src_idx = None
            haive_idx = None

            for i, part in enumerate(parts):
                if part == "src" and i + 1 < len(parts) and parts[i + 1] == "haive":
                    src_idx = i
                    haive_idx = i + 1
                    break

            if src_idx is not None and haive_idx is not None:
                # Get the module path after haive/
                module_parts = parts[haive_idx:]

                # Remove .py extension from the last part if it's a file
                if module_parts[-1].endswith(".py"):
                    module_parts = module_parts[:-1] + (module_parts[-1][:-3],)

                return ".".join(module_parts)

        except (IndexError, ValueError):
            pass

        return None

    @staticmethod
    def get_package_name(file_path: Path) -> str | None:
        """Get the Haive package name (e.g., 'haive-games') from file path."""
        path = Path(file_path).resolve()
        parts = path.parts

        for i, part in enumerate(parts):
            if part == "packages" and i + 1 < len(parts):
                next_part = parts[i + 1]
                if next_part.startswith("haive-"):
                    return next_part

        return None


class ImportFixer:
    """Fixes Python imports using libcst."""

    def __init__(self, target_package: str):
        self.target_package = target_package
        self.console = console

    def fix_relative_imports(self, source_code: str, file_path: Path) -> str:
        """Fix relative imports to absolute imports in Haive namespace."""
        if not LIBCST_AVAILABLE:
            self.console.print(
                "[red]libcst not available. Install with: pip install libcst[/red]"
            )
            return source_code

        try:
            tree = cst.parse_module(source_code)
            transformer = RelativeImportTransformer(file_path, self.target_package)
            modified_tree = tree.visit(transformer)
            return modified_tree.code
        except Exception as e:
            self.console.print(f"[red]Error parsing {file_path}: {e}[/red]")
            return source_code


class RelativeImportTransformer(cst.CSTTransformer):
    """Transforms relative imports to absolute imports."""

    def __init__(self, file_path: Path, target_package: str):
        self.file_path = file_path
        self.target_package = target_package
        self.current_module = HaivePathResolver.resolve_import_path(file_path)

    def leave_ImportFrom(
        self, original_node: cst.ImportFrom, updated_node: cst.ImportFrom
    ) -> cst.ImportFrom:
        """Transform relative imports to absolute imports."""
        if updated_node.module is None:
            return updated_node

        # Check if it's a relative import
        if isinstance(updated_node.module, cst.Attribute) or (
            isinstance(updated_node.module, cst.Name)
            and str(updated_node.module.value).startswith(".")
        ):
            # Convert relative to absolute
            relative_path = (
                str(updated_node.module.value)
                if hasattr(updated_node.module, "value")
                else str(updated_node.module)
            )

            if relative_path.startswith("."):
                # Calculate absolute import
                if self.current_module:
                    module_parts = self.current_module.split(".")

                    # Handle different levels of relative imports
                    levels = len(relative_path) - len(relative_path.lstrip("."))
                    remaining_path = relative_path.lstrip(".")

                    if levels == 1:  # from .module
                        base_module = ".".join(module_parts[:-1])
                    else:  # from ..module, ...module, etc.
                        base_module = ".".join(
                            module_parts[: -(levels - 1)]
                            if levels > 1
                            else module_parts
                        )

                    if remaining_path:
                        absolute_import = f"{base_module}.{remaining_path}"
                    else:
                        absolute_import = base_module

                    # Create new module node
                    new_module = cst.parse_expression(f'"{absolute_import}"').value
                    return updated_node.with_changes(
                        module=(
                            cst.Attribute(
                                value=cst.Name(absolute_import.split(".")[0]),
                                attr=cst.Name(".".join(absolute_import.split(".")[1:])),
                            )
                            if "." in absolute_import
                            else cst.Name(absolute_import)
                        )
                    )

        return updated_node


class FileNormalizer:
    """Main file normalization utility."""

    def __init__(self, directory: Path):
        self.directory = Path(directory)
        self.console = console

    def find_common_prefix(self, files: list[str]) -> str:
        """Find common prefix among files, considering the directory name."""
        if not files:
            return ""

        # Get directory name as potential prefix
        dir_name = (
            self.directory.name.lower()
            .replace(" ", "")
            .replace("-", "")
            .replace("_", "")
        )

        # Check if directory name is a common prefix
        dir_matches = 0
        for file in files:
            clean_file = file.lower().replace(" ", "").replace("-", "").replace("_", "")
            if clean_file.startswith(dir_name):
                dir_matches += 1

        # If most files start with directory name, use it as prefix
        if dir_matches >= len(files) * 0.7:  # 70% threshold
            return dir_name

        # Otherwise find longest common prefix
        if len(files) == 1:
            return ""

        prefix = files[0]
        for file in files[1:]:
            while prefix and not file.startswith(prefix):
                prefix = prefix[:-1]

        # Only return meaningful prefixes (at least 3 chars)
        return prefix if len(prefix) >= 3 else ""

    def extract_number_suffix(self, filename: str) -> tuple[str, int | None]:
        """Extract number suffix from filename (e.g., 'file (1).py' -> ('file.py', 1))."""
        # Pattern for files with numbers: "name (n)", "name_n", "name-n", etc.
        patterns = [
            r"^(.+?)\s*\((\d+)\)(\.[^.]+)?$",  # file (1).ext
            r"^(.+?)[-_\s]+(\d+)(\.[^.]+)?$",  # file_1.ext, file-1.ext, file 1.ext
        ]

        for pattern in patterns:
            match = re.match(pattern, filename)
            if match:
                base_name = match.group(1).strip()
                number = int(match.group(2))
                extension = match.group(3) or ""
                return base_name + extension, number

        return filename, None

    def group_duplicate_files(self, files: list[Path]) -> dict[str, list[Path]]:
        """Group files that are likely duplicates."""
        groups = {}

        for file_path in files:
            if file_path.is_file():
                base_name, number = self.extract_number_suffix(file_path.name)

                if base_name not in groups:
                    groups[base_name] = []
                groups[base_name].append(file_path)

        return groups

    def get_newest_file(self, files: list[Path]) -> Path:
        """Get the newest file from a list based on modification time."""
        return max(files, key=lambda f: f.stat().st_mtime)

    def normalize_filename(self, filename: str, common_prefix: str) -> str:
        """Normalize a filename by removing prefix and cleaning up."""
        # Don't touch __init__.py files
        if filename == "__init__.py":
            return filename

        # Remove extension temporarily
        name_part = filename
        extension = ""
        if "." in filename:
            name_part, extension = filename.rsplit(".", 1)
            extension = "." + extension

        # Remove common prefix (case insensitive)
        if common_prefix:
            clean_name = name_part.lower()
            clean_prefix = common_prefix.lower()
            if clean_name.startswith(clean_prefix):
                # Remove prefix and any following separators
                remaining = name_part[len(common_prefix) :]
                name_part = remaining.lstrip("_- ")

        # Clean up the name
        name_part = re.sub(r"[_\-\s]+", "_", name_part)  # Normalize separators
        name_part = re.sub(
            r"^_+|_+$", "", name_part
        )  # Remove leading/trailing underscores

        # Ensure we have a name
        if not name_part:
            name_part = "file"

        return name_part + extension

    def normalize_directory(self, dry_run: bool = True) -> dict[str, any]:
        """Normalize all files in the directory."""
        if not self.directory.exists():
            self.console.print(f"[red]Directory {self.directory} does not exist[/red]")
            return {"success": False, "error": "Directory not found"}

        # Get all files
        all_files = [f for f in self.directory.iterdir() if f.is_file()]

        if not all_files:
            self.console.print("[yellow]No files found in directory[/yellow]")
            return {"success": True, "changes": []}

        # Show directory info
        self.console.print(
            Panel(
                f"[bold blue]Analyzing Directory:[/bold blue] {self.directory}\n"
                f"[dim]Found {len(all_files)} files[/dim]",
                title="File Normalizer",
            )
        )

        # Find common prefix
        filenames = [f.name for f in all_files]
        common_prefix = self.find_common_prefix(filenames)

        if common_prefix:
            self.console.print(
                f"[green]Detected common prefix:[/green] '{common_prefix}'"
            )

        # Group duplicates FIRST (before normalization)
        file_groups = self.group_duplicate_files(all_files)

        changes = []
        duplicates_removed = []

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=self.console,
        ) as progress:
            task = progress.add_task("Processing files...", total=len(file_groups))

            for base_name, files in file_groups.items():
                if len(files) > 1:
                    # Handle duplicates - keep newest
                    newest_file = self.get_newest_file(files)
                    for file in files:
                        if file != newest_file:
                            duplicates_removed.append(
                                {
                                    "file": str(file),
                                    "reason": f"Duplicate of {newest_file.name}",
                                }
                            )
                            if not dry_run:
                                file.unlink()

                    # Only keep the newest file for normalization
                    files_to_process = [newest_file]
                else:
                    files_to_process = files

                # Normalize filename for remaining files
                for file in files_to_process:
                    # For duplicates, we need to work with the base name (without numbers)
                    if len(file_groups[base_name]) > 1:
                        # This was a duplicate group, normalize the base name
                        normalized_name = self.normalize_filename(
                            base_name, common_prefix
                        )
                    else:
                        # Single file, normalize as normal
                        normalized_name = self.normalize_filename(
                            file.name, common_prefix
                        )

                    if normalized_name != file.name:
                        new_path = file.parent / normalized_name

                        # Check for conflicts with existing files
                        counter = 1
                        original_normalized = normalized_name
                        while new_path.exists() and new_path != file:
                            name_part, ext = (
                                original_normalized.rsplit(".", 1)
                                if "." in original_normalized
                                else (original_normalized, "")
                            )
                            normalized_name = (
                                f"{name_part}_{counter}.{ext}"
                                if ext
                                else f"{name_part}_{counter}"
                            )
                            new_path = file.parent / normalized_name
                            counter += 1

                        changes.append(
                            {"old": str(file), "new": str(new_path), "type": "rename"}
                        )
                        if not dry_run:
                            file.rename(new_path)

                progress.advance(task)

        # Display results
        self._display_results(changes, duplicates_removed, dry_run)

        return {
            "success": True,
            "changes": changes,
            "duplicates_removed": duplicates_removed,
            "common_prefix": common_prefix,
        }

    def _display_results(
        self, changes: list[dict], duplicates: list[dict], dry_run: bool
    ):
        """Display the results of normalization."""
        if not changes and not duplicates:
            self.console.print(
                "[green]✓ No changes needed - all files are already normalized[/green]"
            )
            return

        # Create results table
        table = Table(
            title=f"File Normalization Results {'(DRY RUN)' if dry_run else ''}"
        )
        table.add_column("Action", style="cyan")
        table.add_column("From", style="red")
        table.add_column("To", style="green")

        for change in changes:
            old_name = Path(change["old"]).name
            new_name = Path(change["new"]).name
            table.add_row("RENAME", old_name, new_name)

        for dup in duplicates:
            table.add_row("DELETE", Path(dup["file"]).name, dup["reason"])

        self.console.print(table)

        if dry_run:
            self.console.print(
                "\n[yellow]This was a dry run. Use --execute to apply changes.[/yellow]"
            )


class DownloadNormalizer:
    """Handles download directory normalization."""

    def __init__(self, downloads_dir: Path = None):
        self.downloads_dir = downloads_dir or Path.home() / "Downloads"
        self.console = console

    def find_matching_downloads(self, pattern: str, limit: int = 10) -> list[Path]:
        """Find recent downloads matching pattern."""
        if not self.downloads_dir.exists():
            return []

        # Find Python files matching pattern
        files = []
        for file in self.downloads_dir.glob("*.py"):
            if pattern.lower() in file.name.lower():
                files.append(file)

        # Sort by modification time (newest first)
        files.sort(key=lambda f: f.stat().st_mtime, reverse=True)

        return files[:limit]

    def normalize_downloads(
        self, pattern: str, destination: Path, limit: int = 10, dry_run: bool = True
    ) -> dict[str, any]:
        """Find, normalize, and move matching downloads."""
        matching_files = self.find_matching_downloads(pattern, limit)

        if not matching_files:
            self.console.print(
                f"[yellow]No Python files found matching pattern '{pattern}'[/yellow]"
            )
            return {"success": True, "files": []}

        destination = Path(destination)
        if not dry_run:
            destination.mkdir(parents=True, exist_ok=True)

        # Show found files
        self.console.print(
            Panel(
                f"Found {len(matching_files)} files matching '{pattern}'",
                title="Download Normalizer",
            )
        )

        # Create temporary directory for normalization
        temp_dir = destination / "temp_normalize" if not dry_run else None
        if temp_dir and not dry_run:
            temp_dir.mkdir(exist_ok=True)

        processed_files = []

        try:
            # Copy files to temp directory first
            if not dry_run and temp_dir:
                for file in matching_files:
                    shutil.copy2(file, temp_dir)

            # Normalize in temp directory
            if temp_dir:
                normalizer = FileNormalizer(
                    temp_dir if not dry_run else self.downloads_dir
                )
                result = normalizer.normalize_directory(dry_run=dry_run)

                if not dry_run:
                    # Move normalized files to final destination
                    for file in temp_dir.iterdir():
                        if file.is_file():
                            final_path = destination / file.name
                            shutil.move(str(file), str(final_path))
                            processed_files.append(str(final_path))

                    # Clean up temp directory
                    shutil.rmtree(temp_dir)

            return {
                "success": True,
                "files": processed_files,
                "normalization_result": result if temp_dir else None,
            }

        except Exception as e:
            if temp_dir and temp_dir.exists():
                shutil.rmtree(temp_dir)
            self.console.print(f"[red]Error during download normalization: {e}[/red]")
            return {"success": False, "error": str(e)}


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Haive File Normalizer and Import Fixer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Normalize files in a directory (dry run)
  python file_normalizer.py normalize ./my_files/
  
  # Normalize and execute changes
  python file_normalizer.py normalize ./my_files/ --execute
  
  # Fix imports for Haive package
  python file_normalizer.py fix-imports ./packages/haive-games/src/haive/games/holdem/
  
  # Normalize recent downloads
  python file_normalizer.py download-normalize "holdem" ./normalized_holdem/
  
  # Do everything
  python file_normalizer.py all ./my_files/ --target-package haive.games.holdem --execute
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Normalize command
    normalize_parser = subparsers.add_parser("normalize", help="Normalize file names")
    normalize_parser.add_argument("directory", type=Path, help="Directory to normalize")
    normalize_parser.add_argument(
        "--execute", action="store_true", help="Execute changes (default is dry run)"
    )

    # Fix imports command
    fix_parser = subparsers.add_parser("fix-imports", help="Fix Python imports")
    fix_parser.add_argument("directory", type=Path, help="Directory to fix imports in")
    fix_parser.add_argument(
        "--target-package",
        required=True,
        help="Target package (e.g., haive.games.holdem)",
    )
    fix_parser.add_argument(
        "--execute", action="store_true", help="Execute changes (default is dry run)"
    )

    # Download normalize command
    download_parser = subparsers.add_parser(
        "download-normalize", help="Normalize downloads"
    )
    download_parser.add_argument(
        "pattern", help="Pattern to match in download filenames"
    )
    download_parser.add_argument("destination", type=Path, help="Destination directory")
    download_parser.add_argument(
        "--limit", type=int, default=10, help="Max files to process"
    )
    download_parser.add_argument(
        "--execute", action="store_true", help="Execute changes (default is dry run)"
    )

    # All command
    all_parser = subparsers.add_parser(
        "all", help="Run normalization and import fixing"
    )
    all_parser.add_argument("directory", type=Path, help="Directory to process")
    all_parser.add_argument("--target-package", help="Target package for import fixing")
    all_parser.add_argument(
        "--execute", action="store_true", help="Execute changes (default is dry run)"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return None

    # Show Haive banner
    console.print(
        Panel(
            "[bold blue]Haive File Normalizer & Import Fixer[/bold blue]\n"
            "[dim]Polyrepo-aware file management for the Haive framework[/dim]",
            title="🤖 Haive Tools",
            border_style="blue",
        )
    )

    try:
        if args.command == "normalize":
            normalizer = FileNormalizer(args.directory)
            result = normalizer.normalize_directory(dry_run=not args.execute)

        elif args.command == "fix-imports":
            if not LIBCST_AVAILABLE:
                console.print(
                    "[red]libcst is required for import fixing. Install with: pip install libcst[/red]"
                )
                return 1

            # Fix imports in Python files
            import_fixer = ImportFixer(args.target_package)
            directory = Path(args.directory)

            python_files = list(directory.glob("**/*.py"))
            if not python_files:
                console.print("[yellow]No Python files found[/yellow]")
                return None

            with Progress(console=console) as progress:
                task = progress.add_task("Fixing imports...", total=len(python_files))

                for py_file in python_files:
                    try:
                        with open(py_file, encoding="utf-8") as f:
                            original_content = f.read()

                        fixed_content = import_fixer.fix_relative_imports(
                            original_content, py_file
                        )

                        if fixed_content != original_content:
                            console.print(f"[green]Fixed imports in:[/green] {py_file}")
                            if args.execute:
                                with open(py_file, "w", encoding="utf-8") as f:
                                    f.write(fixed_content)

                    except Exception as e:
                        console.print(f"[red]Error processing {py_file}: {e}[/red]")

                    progress.advance(task)

            if not args.execute:
                console.print(
                    "\n[yellow]This was a dry run. Use --execute to apply changes.[/yellow]"
                )

        elif args.command == "download-normalize":
            normalizer = DownloadNormalizer()
            result = normalizer.normalize_downloads(
                args.pattern, args.destination, args.limit, dry_run=not args.execute
            )

        elif args.command == "all":
            # Run normalization first
            console.print("[bold]Step 1: File Normalization[/bold]")
            normalizer = FileNormalizer(args.directory)
            norm_result = normalizer.normalize_directory(dry_run=not args.execute)

            # Then fix imports if package specified
            if args.target_package and LIBCST_AVAILABLE:
                console.print("\n[bold]Step 2: Import Fixing[/bold]")
                import_fixer = ImportFixer(args.target_package)
                # Implementation similar to fix-imports command
            elif args.target_package and not LIBCST_AVAILABLE:
                console.print(
                    "[yellow]Skipping import fixing - libcst not available[/yellow]"
                )

    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user[/yellow]")
        return 1
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
        return 1


if __name__ == "__main__":
    sys.exit(main() or 0)
