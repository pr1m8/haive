#!/usr/bin/env python3
"""Rich documentation builder with progress tracking and caching."""

import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)
from rich.table import Table
from rich.text import Text
from rich.tree import Tree

console = Console()


class DocsBuildStats:
    """Track documentation build statistics."""

    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.total_files = 0
        self.html_files = 0
        self.css_files = 0
        self.js_files = 0
        self.image_files = 0
        self.other_files = 0
        self.warnings = []
        self.errors = []
        self.cache_hits = 0
        self.cache_misses = 0
        self.build_phases = {}

    def duration(self) -> float:
        """Get build duration in seconds."""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return 0

    def add_file(self, filepath: str):
        """Track a generated file."""
        self.total_files += 1
        ext = Path(filepath).suffix.lower()
        if ext == ".html":
            self.html_files += 1
        elif ext == ".css":
            self.css_files += 1
        elif ext == ".js":
            self.js_files += 1
        elif ext in [".png", ".jpg", ".jpeg", ".gif", ".svg"]:
            self.image_files += 1
        else:
            self.other_files += 1


class DocsCache:
    """Simple cache for documentation builds."""

    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_file = self.cache_dir / "build_cache.json"
        self.cache_data = self._load_cache()

    def _load_cache(self) -> dict:
        """Load cache from disk."""
        if self.cache_file.exists():
            try:
                with open(self.cache_file) as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def _save_cache(self):
        """Save cache to disk."""
        with open(self.cache_file, "w") as f:
            json.dump(self.cache_data, f, indent=2)

    def get_file_hash(self, filepath: Path) -> str:
        """Get hash of file contents."""
        if not filepath.exists():
            return ""
        return hashlib.md5(filepath.read_bytes()).hexdigest()

    def is_changed(self, filepath: Path) -> bool:
        """Check if file has changed since last build."""
        str_path = str(filepath)
        current_hash = self.get_file_hash(filepath)

        if str_path not in self.cache_data:
            self.cache_data[str_path] = current_hash
            self._save_cache()
            return True

        if self.cache_data[str_path] != current_hash:
            self.cache_data[str_path] = current_hash
            self._save_cache()
            return True

        return False

    def get_changed_files(self, directory: Path, pattern: str = "*.py") -> list[Path]:
        """Get list of changed files."""
        changed = []
        for filepath in directory.rglob(pattern):
            if self.is_changed(filepath):
                changed.append(filepath)
        return changed


class RichDocsBuilder:
    """Rich documentation builder with UI."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.docs_dir = project_root / "docs"
        self.source_dir = self.docs_dir / "source"
        self.build_dir = self.docs_dir / "build"
        self.cache_dir = self.docs_dir / ".cache"
        self.cache = DocsCache(self.cache_dir)
        self.stats = DocsBuildStats()
        self.progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            TimeRemainingColumn(),
            console=console,
        )

    def create_layout(self) -> Layout:
        """Create the UI layout."""
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body"),
            Layout(name="footer", size=10),
        )

        # Header
        header_text = Text("📚 Haive Documentation Builder", style="bold blue")
        layout["header"].update(Panel(header_text, title="Rich Docs UI"))

        # Body split
        layout["body"].split_row(
            Layout(name="stats", ratio=1),
            Layout(name="progress", ratio=2),
        )

        return layout

    def update_stats_panel(self) -> Panel:
        """Create statistics panel."""
        table = Table(title="Build Statistics", show_header=False)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")

        elapsed = time.time() - self.stats.start_time if self.stats.start_time else 0

        table.add_row("⏱️  Elapsed Time", f"{elapsed:.1f}s")
        table.add_row("📄 HTML Files", str(self.stats.html_files))
        table.add_row("🎨 CSS Files", str(self.stats.css_files))
        table.add_row("📜 JS Files", str(self.stats.js_files))
        table.add_row("🖼️  Image Files", str(self.stats.image_files))
        table.add_row("📁 Total Files", str(self.stats.total_files))
        table.add_row("✅ Cache Hits", str(self.stats.cache_hits))
        table.add_row("❌ Cache Misses", str(self.stats.cache_misses))
        table.add_row("⚠️  Warnings", str(len(self.stats.warnings)))
        table.add_row("❌ Errors", str(len(self.stats.errors)))

        return Panel(table, title="📊 Statistics", border_style="blue")

    def update_progress_panel(self) -> Panel:
        """Create progress panel."""
        return Panel(self.progress, title="🚀 Build Progress", border_style="green")

    def update_footer_panel(self) -> Panel:
        """Create footer panel with recent activity."""
        tree = Tree("📋 Recent Activity")

        # Add build phases
        if self.stats.build_phases:
            phases_branch = tree.add("⚙️  Build Phases")
            for phase, duration in self.stats.build_phases.items():
                phases_branch.add(f"{phase}: {duration:.1f}s")

        # Add recent warnings
        if self.stats.warnings:
            warnings_branch = tree.add(
                f"⚠️  Recent Warnings ({len(self.stats.warnings)})"
            )
            for warning in self.stats.warnings[-5:]:  # Last 5 warnings
                warnings_branch.add(Text(warning[:80] + "...", style="yellow"))

        # Add recent errors
        if self.stats.errors:
            errors_branch = tree.add(f"❌ Recent Errors ({len(self.stats.errors)})")
            for error in self.stats.errors[-5:]:  # Last 5 errors
                errors_branch.add(Text(error[:80] + "...", style="red"))

        return Panel(tree, title="📝 Activity Log", border_style="cyan")

    def count_source_files(self) -> dict[str, int]:
        """Count source files by type."""
        counts = {"python": 0, "rst": 0, "md": 0, "total": 0}

        for pattern, key in [("*.py", "python"), ("*.rst", "rst"), ("*.md", "md")]:
            for _ in self.source_dir.rglob(pattern):
                counts[key] += 1
                counts["total"] += 1

        # Also count package Python files
        packages_dir = self.project_root / "packages"
        if packages_dir.exists():
            for _ in packages_dir.rglob("*.py"):
                counts["python"] += 1
                counts["total"] += 1

        return counts

    def analyze_build_output(self, output_dir: Path):
        """Analyze generated documentation files."""
        if not output_dir.exists():
            return

        for filepath in output_dir.rglob("*"):
            if filepath.is_file():
                self.stats.add_file(str(filepath))

    def run_sphinx_build(self, task_id) -> tuple[bool, str]:
        """Run the actual Sphinx build."""
        cmd = [
            "poetry",
            "run",
            "sphinx-build",
            "-b",
            "html",
            "-j",
            "auto",  # Parallel build
            "-W",
            "--keep-going",  # Warnings as errors but continue
            str(self.source_dir),
            str(self.build_dir / "html"),
        ]

        try:
            # Start the build
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=self.project_root,
            )

            # Process output line by line
            while True:
                line = process.stdout.readline()
                if not line and process.poll() is not None:
                    break

                if line:
                    line = line.strip()

                    # Parse progress
                    if "reading sources..." in line:
                        self.progress.update(
                            task_id, description="📖 Reading sources..."
                        )
                    elif "building [html]:" in line:
                        self.progress.update(task_id, description="🔨 Building HTML...")
                    elif "writing output..." in line:
                        self.progress.update(
                            task_id, description="✍️  Writing output..."
                        )
                    elif "copying" in line:
                        self.progress.update(task_id, description="📋 Copying files...")
                    elif "dumping" in line:
                        self.progress.update(task_id, description="💾 Dumping data...")

                    # Track warnings/errors
                    if "WARNING" in line:
                        self.stats.warnings.append(line)
                    elif "ERROR" in line:
                        self.stats.errors.append(line)

                    # Update progress
                    self.progress.advance(task_id, 0.1)

            # Get any remaining output
            stdout, stderr = process.communicate()

            return process.returncode == 0, stdout + stderr

        except Exception as e:
            return False, str(e)

    def build(self):
        """Run the documentation build with rich UI."""
        self.stats.start_time = time.time()

        # Count source files
        source_counts = self.count_source_files()

        # Create layout
        layout = self.create_layout()

        with Live(layout, refresh_per_second=4, console=console):
            # Update initial UI
            layout["stats"].update(self.update_stats_panel())
            layout["progress"].update(self.update_progress_panel())
            layout["footer"].update(self.update_footer_panel())

            # Check for changed files
            with self.progress:
                # Phase 1: Analyze changes
                task1 = self.progress.add_task(
                    "🔍 Analyzing changes...", total=source_counts["total"]
                )

                self.stats.build_phases["analyze"] = time.time() - self.stats.start_time

                changed_files = []
                for ext in ["*.py", "*.rst", "*.md"]:
                    for filepath in self.source_dir.rglob(ext):
                        if self.cache.is_changed(filepath):
                            changed_files.append(filepath)
                            self.stats.cache_misses += 1
                        else:
                            self.stats.cache_hits += 1
                        self.progress.advance(task1, 1)

                # Phase 2: Build documentation
                task2 = self.progress.add_task(
                    "🏗️  Building documentation...", total=100
                )

                build_start = time.time()
                success, output = self.run_sphinx_build(task2)
                self.stats.build_phases["sphinx"] = time.time() - build_start

                # Phase 3: Analyze output
                task3 = self.progress.add_task("📊 Analyzing output...", total=100)

                analyze_start = time.time()
                self.analyze_build_output(self.build_dir / "html")
                self.stats.build_phases["analyze_output"] = time.time() - analyze_start
                self.progress.update(task3, completed=100)

                # Update final stats
                self.stats.end_time = time.time()

                # Final UI update
                layout["stats"].update(self.update_stats_panel())
                layout["footer"].update(self.update_footer_panel())

        # Print summary
        console.print("\n" + "=" * 80)
        if success:
            console.print(
                "✅ [bold green]Documentation build completed successfully![/bold green]"
            )
        else:
            console.print("❌ [bold red]Documentation build failed![/bold red]")

        console.print("\n📊 Build Summary:")
        console.print(f"   • Duration: {self.stats.duration():.1f} seconds")
        console.print(f"   • HTML pages: {self.stats.html_files}")
        console.print(f"   • Total files: {self.stats.total_files}")
        console.print(
            f"   • Cache efficiency: {self.stats.cache_hits}/{self.stats.cache_hits + self.stats.cache_misses} hits"
        )
        console.print(f"   • Warnings: {len(self.stats.warnings)}")
        console.print(f"   • Errors: {len(self.stats.errors)}")

        if success:
            console.print(
                f"\n🌐 View docs at: file://{self.build_dir / 'html' / 'index.html'}"
            )
            console.print(
                f"   Or run: python -m http.server 8003 --directory {self.build_dir / 'html'}"
            )

        return success


def main():
    """Main entry point."""
    project_root = Path(__file__).parent.parent
    builder = RichDocsBuilder(project_root)
    success = builder.build()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
