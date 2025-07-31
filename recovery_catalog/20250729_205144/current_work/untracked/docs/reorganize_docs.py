#!/usr/bin/env python3
"""Documentation Directory Reorganization Script
Clean up the docs directory chaos and create proper organization.
"""

import shutil
from datetime import datetime
from pathlib import Path


class DocsReorganizer:
    def __init__(self, docs_dir: Path | None = None):
        self.docs_dir = docs_dir or Path("docs")
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.moved_files = []
        self.created_dirs = []

    def log_action(self, action: str):
        """Log what we're doing."""

    def create_directory_structure(self):
        """Create the proper directory structure."""
        dirs_to_create = [
            "guides/development",
            "guides/automation",
            "guides/architecture",
            "guides/troubleshooting",
            "scripts/build",
            "scripts/quality",
            "scripts/generation",
            "scripts/maintenance",
            "reports/build-quality",
            "reports/test-results",
            "reports/analysis",
            "reports/performance",
            "logs/builds",
            "logs/quality",
            "logs/scripts",
            "data/agent-showcase",
            "data/screenshots",
            "data/examples",
            "archive/old-scripts",
            "archive/legacy-docs",
            "archive/previous-builds",
            "notes/user_sessions",
            "notes/planning",
        ]

        for dir_path in dirs_to_create:
            full_path = self.docs_dir / dir_path
            if not full_path.exists():
                full_path.mkdir(parents=True, exist_ok=True)
                self.created_dirs.append(str(full_path))
                self.log_action(f"Created directory: {dir_path}")

    def move_file_safely(self, source: Path, dest: Path, reason: str = ""):
        """Move a file safely with logging."""
        if source.exists() and source.is_file():
            dest.parent.mkdir(parents=True, exist_ok=True)
            try:
                shutil.move(str(source), str(dest))
                self.moved_files.append(f"{source} → {dest}")
                self.log_action(f"Moved {source.name} → {dest.parent.name}/ ({reason})")
                return True
            except Exception:
                return False
        return False

    def organize_guides(self):
        """Move guide files to proper locations."""
        self.log_action("🔧 Organizing guides...")

        guide_mappings = {
            # Development guides
            "AUTOMATION_TOOLS_GUIDE.md": "guides/development/automation_tools.md",
            "GRAPH_VISUALIZATION_GUIDE.md": "guides/development/graph_visualization.md",
            "JINJA_TEMPLATE_GUIDE.md": "guides/development/jinja_templates.md",
            "FURO_THEME_GUIDE.md": "guides/development/furo_theme.md",
            "TEMPLATE_CONVERSION_WORKFLOW.md": "guides/development/template_conversion.md",
            "TESTING_README.md": "guides/development/testing.md",
            "README_GIT_LFS.md": "guides/development/git_lfs.md",
            # Architecture guides
            "AGENT_CAPTURE_SYSTEM.md": "guides/architecture/agent_capture_system.md",
            # Troubleshooting
            "RSTCHECK_ANALYSIS.md": "guides/troubleshooting/rstcheck_analysis.md",
            "RSTCHECK_FIX_PLAN.md": "guides/troubleshooting/rstcheck_fixes.md",
        }

        for old_name, new_path in guide_mappings.items():
            old_file = self.docs_dir / old_name
            new_file = self.docs_dir / new_path
            self.move_file_safely(old_file, new_file, "guide organization")

    def organize_scripts(self):
        """Move Python scripts to proper script directories."""
        self.log_action("🐍 Organizing scripts...")

        script_mappings = {
            # Generation scripts
            "add_function_docstrings.py": "scripts/generation/add_function_docstrings.py",
            "docstring_templates.py": "scripts/generation/docstring_templates.py",
            "generate_agent_demos.py": "scripts/generation/generate_agent_demos.py",
            "generate_game_demos.py": "scripts/generation/generate_game_demos.py",
            "run_examples_for_docs.py": "scripts/generation/run_examples_for_docs.py",
            # Quality scripts
            "validate_css_fixes.py": "scripts/quality/validate_css_fixes.py",
            "validate_game_demos.py": "scripts/quality/validate_game_demos.py",
            "run_all_doc_tests.py": "scripts/quality/run_all_doc_tests.py",
            "quick_visual_check.py": "scripts/quality/quick_visual_check.py",
            # Build scripts
            "cleanup_and_build.py": "scripts/build/cleanup_and_build.py",
            "test_documentation_screenshots.py": "scripts/build/test_documentation_screenshots.py",
            # Maintenance scripts
            "take_screenshot_both.py": "scripts/maintenance/take_screenshot_both.py",
            "take_screenshot_quick.py": "scripts/maintenance/take_screenshot_quick.py",
            "visualize_agent_example.py": "scripts/maintenance/visualize_agent_example.py",
        }

        for old_name, new_path in script_mappings.items():
            old_file = self.docs_dir / old_name
            new_file = self.docs_dir / new_path
            self.move_file_safely(old_file, new_file, "script organization")

        # Move shell scripts to build
        shell_scripts = [
            "auto_build.sh",
            "autobuild.sh",
            "check_navigation_status.sh",
            "monitor_build.sh",
            "quick_rebuild.sh",
            "serve.sh",
            "sphinx_autobuild.sh",
            "start_docs.sh",
            "start_docs_server.sh",
        ]

        for script in shell_scripts:
            old_file = self.docs_dir / script
            new_file = self.docs_dir / "scripts" / "build" / script
            self.move_file_safely(old_file, new_file, "shell script")

    def organize_logs(self):
        """Move log files to logs directory."""
        self.log_action("📋 Organizing logs...")

        # Move all .log files
        for log_file in self.docs_dir.glob("*.log"):
            if "sphinx" in log_file.name or "build" in log_file.name:
                dest = self.docs_dir / "logs" / "builds" / log_file.name
            else:
                dest = self.docs_dir / "logs" / "scripts" / log_file.name
            self.move_file_safely(log_file, dest, "log file")

    def organize_data_files(self):
        """Move data files to data directory."""
        self.log_action("💾 Organizing data files...")

        data_mappings = {
            "agent_showcase_data.json": "data/agent-showcase/agent_showcase_data.json",
            "import_analysis.txt": "data/analysis/import_analysis.txt",
            "test_gallery_conf.py": "data/examples/test_gallery_conf.py",
            "test_scripts_summary.md": "reports/analysis/test_scripts_summary.md",
        }

        for old_name, new_path in data_mappings.items():
            old_file = self.docs_dir / old_name
            new_file = self.docs_dir / new_path
            self.move_file_safely(old_file, new_file, "data file")

    def organize_reports(self):
        """Move existing reports to reports directory."""
        self.log_action("📊 Organizing reports...")

        report_mappings = {
            "CURRENT_STATUS_SUMMARY.md": "reports/analysis/current_status_summary.md",
            "DOCUMENTATION_FIX_SUMMARY.md": "reports/analysis/documentation_fix_summary.md",
            "FINAL_DOCUMENTATION_SUMMARY.md": "reports/analysis/final_documentation_summary.md",
            "SPHINX_CONF_FIXES_AND_IMPROVEMENTS.md": "reports/analysis/sphinx_conf_fixes.md",
            "EXAMPLE_EXECUTION_SETUP_ANALYSIS.md": "reports/analysis/example_execution_setup.md",
        }

        for old_name, new_path in report_mappings.items():
            old_file = self.docs_dir / old_name
            new_file = self.docs_dir / new_path
            self.move_file_safely(old_file, new_file, "report")

    def organize_archives(self):
        """Move old/deprecated content to archive."""
        self.log_action("📦 Organizing archives...")

        # Move old directories that are no longer active
        old_dirs = ["css_analysis_20250726_002246", "audit_results", "archive_old_docs"]

        for old_dir in old_dirs:
            old_path = self.docs_dir / old_dir
            if old_path.exists():
                new_path = self.docs_dir / "archive" / "legacy-docs" / old_dir
                try:
                    shutil.move(str(old_path), str(new_path))
                    self.log_action(f"Archived directory: {old_dir}")
                except Exception:
                    pass

    def clean_empty_files(self):
        """Remove empty log files and other clutter."""
        self.log_action("🧹 Cleaning empty files...")

        # Remove empty .log files
        for log_file in self.docs_dir.glob("**/*.log"):
            if log_file.stat().st_size == 0:
                try:
                    log_file.unlink()
                    self.log_action(f"Removed empty file: {log_file.name}")
                except Exception:
                    pass

        # Clean up specific empty files
        empty_files = ["Chinook.db", ".nox_cache.json"]

        for empty_file in empty_files:
            file_path = self.docs_dir / empty_file
            if file_path.exists() and file_path.stat().st_size == 0:
                try:
                    file_path.unlink()
                    self.log_action(f"Removed empty file: {empty_file}")
                except Exception:
                    pass

    def create_navigation_readmes(self):
        """Create README files for navigation."""
        self.log_action("📖 Creating navigation READMEs...")

        readmes = {
            "guides/README.md": """# Documentation Guides

User-facing documentation and guides for the Haive project.

## Directory Structure

- **development/**: Developer guides and workflows
- **automation/**: Automation and tooling guides
- **architecture/**: System architecture documentation
- **troubleshooting/**: Problem solving and debugging guides
""",
            "scripts/README.md": """# Documentation Scripts

Development scripts for building, testing, and maintaining documentation.

## Directory Structure

- **build/**: Build and deployment scripts
- **quality/**: Quality checking and validation scripts
- **generation/**: Content generation scripts
- **maintenance/**: Maintenance and utility scripts

## Usage

All scripts should be run from the project root:
```bash
poetry run python docs/scripts/category/script_name.py
```
""",
            "reports/README.md": """# Documentation Reports

Generated reports and analysis results.

## Directory Structure

- **build-quality/**: Build quality and error reports
- **test-results/**: Test execution reports
- **analysis/**: Code and documentation analysis
- **performance/**: Performance benchmarks and metrics
""",
            "logs/README.md": """# Documentation Logs

Build and process logs organized by category.

## Directory Structure

- **builds/**: Sphinx build logs
- **quality/**: Quality check execution logs
- **scripts/**: Script execution logs

## Log Retention

Logs are kept for debugging and analysis. Old logs can be archived periodically.
""",
            "data/README.md": """# Documentation Data

Generated data files and examples.

## Directory Structure

- **agent-showcase/**: Agent demonstration data
- **screenshots/**: Generated screenshots
- **examples/**: Example outputs and test files
""",
        }

        for readme_path, content in readmes.items():
            readme_file = self.docs_dir / readme_path
            if not readme_file.exists():
                readme_file.write_text(content)
                self.log_action(f"Created README: {readme_path}")

    def create_summary_report(self):
        """Create a summary of what was reorganized."""
        summary = f"""# Documentation Reorganization Summary
**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Script**: reorganize_docs.py

## Directories Created
{chr(10).join(f"- {d}" for d in self.created_dirs)}

## Files Moved
{chr(10).join(f"- {f}" for f in self.moved_files)}

## Structure Created
```
docs/
├── guides/          # User-facing documentation
├── scripts/         # Development scripts
├── reports/         # Generated reports
├── logs/           # Build and process logs
├── data/           # Generated data files
├── archive/        # Historical content
└── notes/          # Session notes
```

## Next Steps
1. Update any scripts that reference old file paths
2. Update documentation that links to moved files
3. Add this reorganization to your workflow documentation
"""

        summary_file = (
            self.docs_dir
            / "notes"
            / "claude_sessions"
            / "20250729_documentation_enhancement"
            / f"reorganization_summary_{self.timestamp}.md"
        )
        summary_file.write_text(summary)
        self.log_action(f"Created summary report: {summary_file.name}")

    def reorganize_all(self):
        """Execute the complete reorganization."""
        self.create_directory_structure()
        self.organize_guides()
        self.organize_scripts()
        self.organize_logs()
        self.organize_data_files()
        self.organize_reports()
        self.organize_archives()
        self.clean_empty_files()
        self.create_navigation_readmes()
        self.create_summary_report()


if __name__ == "__main__":
    reorganizer = DocsReorganizer()
    reorganizer.reorganize_all()
