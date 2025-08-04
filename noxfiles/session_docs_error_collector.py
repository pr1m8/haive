"""Enhanced documentation error collection and analysis system.

This module captures ALL errors, warnings, and issues during documentation builds
and creates detailed reports for review and systematic fixing.
"""

import json
import os
import re
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import nox

# Configuration
PYTHON_VERSIONS = ["3.12"]
DOCS_DIR = Path("docs")
SOURCE_DIR = DOCS_DIR / "source"
BUILD_DIR = DOCS_DIR / "build"
LOGS_DIR = DOCS_DIR / "logs"
ERROR_REPORTS_DIR = DOCS_DIR / "error_reports"

# Ensure directories exist
LOGS_DIR.mkdir(parents=True, exist_ok=True)
ERROR_REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Reuse virtualenvs for speed
nox.options.reuse_existing_virtualenvs = True


class ErrorCollector:
    """Comprehensive error collection and analysis system."""

    def __init__(self, session, report_file: Path):
        self.session = session
        self.report_file = report_file
        self.timestamp = datetime.now()

        # Error categorization
        self.errors = {
            "import_errors": [],
            "syntax_errors": [],
            "autodoc_errors": [],
            "autoapi_errors": [],
            "toctree_errors": [],
            "image_errors": [],
            "cross_reference_errors": [],
            "extension_errors": [],
            "theme_errors": [],
            "build_errors": [],
            "unknown_errors": [],
        }

        # Warnings categorization
        self.warnings = {
            "import_warnings": [],
            "deprecation_warnings": [],
            "toctree_warnings": [],
            "image_warnings": [],
            "cross_reference_warnings": [],
            "autoapi_warnings": [],
            "build_warnings": [],
            "unknown_warnings": [],
        }

        # Build statistics
        self.stats = {
            "start_time": None,
            "end_time": None,
            "duration": 0,
            "files_processed": 0,
            "html_generated": 0,
            "packages_built": [],
            "profile_used": "unknown",
            "total_errors": 0,
            "total_warnings": 0,
            "success": False,
        }

        # File tracking
        self.problematic_files = {}
        self.current_file = None
        self.package_context = None

    def start_collection(self, package: str, profile: str):
        """Start error collection for a build."""
        self.stats["start_time"] = time.time()
        self.stats["packages_built"] = [package] if package != "all" else ["all"]
        self.stats["profile_used"] = profile
        self.package_context = package

        self.session.log(
            f"🔍 Starting error collection for {package} ({profile} profile)"
        )

    def categorize_error(self, line: str) -> str:
        """Categorize an error based on its content."""
        line_lower = line.lower()

        # Import errors
        if any(
            keyword in line_lower
            for keyword in ["modulenotfounderror", "importerror", "no module named"]
        ):
            return "import_errors"

        # Syntax errors
        if any(
            keyword in line_lower
            for keyword in [
                "syntaxerror",
                "indentationerror",
                "parsing python code failed",
            ]
        ):
            return "syntax_errors"

        # AutoDoc errors
        if any(
            keyword in line_lower
            for keyword in ["autodoc:", "failed to import", "autosummary"]
        ):
            return "autodoc_errors"

        # AutoAPI errors
        if any(
            keyword in line_lower for keyword in ["autoapi", "keyerror:", "all_objects"]
        ):
            return "autoapi_errors"

        # Toctree errors
        if any(
            keyword in line_lower
            for keyword in ["toctree", "document isn't included", "toc.not_included"]
        ):
            return "toctree_errors"

        # Image errors
        if any(
            keyword in line_lower
            for keyword in ["image file not readable", "image.not_readable"]
        ):
            return "image_errors"

        # Cross-reference errors
        if any(
            keyword in line_lower
            for keyword in [
                "undefined label",
                "unknown document",
                "reference target not found",
            ]
        ):
            return "cross_reference_errors"

        # Extension errors
        if any(
            keyword in line_lower
            for keyword in [
                "extension error",
                "failed to initialize",
                "extension not found",
            ]
        ):
            return "extension_errors"

        # Theme errors
        if any(
            keyword in line_lower
            for keyword in ["theme error", "template not found", "theme not found"]
        ):
            return "theme_errors"

        # Build errors
        if any(
            keyword in line_lower
            for keyword in ["build failed", "sphinx error", "configuration error"]
        ):
            return "build_errors"

        return "unknown_errors"

    def categorize_warning(self, line: str) -> str:
        """Categorize a warning based on its content."""
        line_lower = line.lower()

        # Import warnings
        if any(keyword in line_lower for keyword in ["import", "deprecation"]):
            if "deprecation" in line_lower:
                return "deprecation_warnings"
            return "import_warnings"

        # Toctree warnings
        if any(
            keyword in line_lower for keyword in ["toctree", "document isn't included"]
        ):
            return "toctree_warnings"

        # Image warnings
        if any(keyword in line_lower for keyword in ["image", "not readable"]):
            return "image_warnings"

        # Cross-reference warnings
        if any(
            keyword in line_lower
            for keyword in ["reference", "undefined", "unknown document"]
        ):
            return "cross_reference_warnings"

        # AutoAPI warnings
        if any(keyword in line_lower for keyword in ["autoapi", "failed to import"]):
            return "autoapi_warnings"

        # Build warnings
        if any(keyword in line_lower for keyword in ["build", "sphinx"]):
            return "build_warnings"

        return "unknown_warnings"

    def process_line(self, line: str):
        """Process a single output line and categorize errors/warnings."""
        line = line.strip()
        if not line:
            return

        # Track current file being processed
        if "[AutoAPI] Analyzing" in line:
            match = re.search(r"\[AutoAPI\] Analyzing (.+)$", line)
            if match:
                self.current_file = match.group(1)
        elif "reading sources..." in line:
            # Extract file being read
            match = re.search(r"reading sources\.\.\. \[\s*\d+%\] (.+)", line)
            if match:
                self.current_file = match.group(1)

        # Track build progress
        if "files processed" in line or "HTML files" in line:
            self.stats["files_processed"] += 1
        elif "writing output..." in line:
            self.stats["html_generated"] += 1

        # Categorize errors
        if any(
            error_indicator in line
            for error_indicator in ["ERROR:", "Exception", "Traceback", "failed"]
        ):
            if "failed to reach" not in line.lower():  # Skip network failures
                category = self.categorize_error(line)
                error_entry = {
                    "line": line,
                    "file": self.current_file,
                    "package": self.package_context,
                    "timestamp": time.strftime("%H:%M:%S"),
                    "severity": "high" if "ERROR:" in line else "medium",
                }
                self.errors[category].append(error_entry)
                self.stats["total_errors"] += 1

                # Track problematic files
                if self.current_file:
                    if self.current_file not in self.problematic_files:
                        self.problematic_files[self.current_file] = {
                            "errors": 0,
                            "warnings": 0,
                        }
                    self.problematic_files[self.current_file]["errors"] += 1

        # Categorize warnings
        elif "WARNING:" in line:
            category = self.categorize_warning(line)
            warning_entry = {
                "line": line,
                "file": self.current_file,
                "package": self.package_context,
                "timestamp": time.strftime("%H:%M:%S"),
                "severity": "low",
            }
            self.warnings[category].append(warning_entry)
            self.stats["total_warnings"] += 1

            # Track problematic files
            if self.current_file:
                if self.current_file not in self.problematic_files:
                    self.problematic_files[self.current_file] = {
                        "errors": 0,
                        "warnings": 0,
                    }
                self.problematic_files[self.current_file]["warnings"] += 1

    def finish_collection(self, success: bool = True):
        """Finish error collection and generate report."""
        self.stats["end_time"] = time.time()
        self.stats["duration"] = self.stats["end_time"] - self.stats["start_time"]
        self.stats["success"] = success

        self.session.log(
            f"📊 Error collection complete: {self.stats['total_errors']} errors, {self.stats['total_warnings']} warnings"
        )

    def generate_report(self) -> Dict:
        """Generate comprehensive error report."""
        report = {
            "metadata": {
                "timestamp": self.timestamp.isoformat(),
                "report_version": "1.0",
                "packages": self.stats["packages_built"],
                "profile": self.stats["profile_used"],
                "duration": self.stats["duration"],
                "success": self.stats["success"],
            },
            "summary": {
                "total_errors": self.stats["total_errors"],
                "total_warnings": self.stats["total_warnings"],
                "files_processed": self.stats["files_processed"],
                "html_generated": self.stats["html_generated"],
                "problematic_files_count": len(self.problematic_files),
            },
            "errors_by_category": {},
            "warnings_by_category": {},
            "problematic_files": self.problematic_files,
            "recommendations": self._generate_recommendations(),
        }

        # Add error counts by category
        for category, error_list in self.errors.items():
            if error_list:
                report["errors_by_category"][category] = {
                    "count": len(error_list),
                    "errors": error_list[:10],  # First 10 for brevity
                }

        # Add warning counts by category
        for category, warning_list in self.warnings.items():
            if warning_list:
                report["warnings_by_category"][category] = {
                    "count": len(warning_list),
                    "warnings": warning_list[:10],  # First 10 for brevity
                }

        return report

    def _generate_recommendations(self) -> List[str]:
        """Generate actionable recommendations based on errors found."""
        recommendations = []

        # Import error recommendations
        if self.errors["import_errors"]:
            recommendations.append(
                "🔧 Fix import errors by updating dependencies in pyproject.toml"
            )
            recommendations.append("🔧 Add missing packages to poetry dependencies")

        # Syntax error recommendations
        if self.errors["syntax_errors"]:
            recommendations.append("🔧 Fix Python syntax errors in source files")
            recommendations.append(
                "🔧 Run 'trunk check --fix --all' to auto-fix syntax issues"
            )

        # AutoAPI error recommendations
        if self.errors["autoapi_errors"]:
            recommendations.append("🔧 Check AutoAPI configuration in conf.py")
            recommendations.append("🔧 Verify package structure and __init__.py files")

        # Toctree error recommendations
        if self.errors["toctree_errors"] or self.warnings["toctree_warnings"]:
            recommendations.append(
                "🔧 Update toctree directives to include missing documents"
            )
            recommendations.append(
                "🔧 Remove references to deleted files from index.rst"
            )

        # Image error recommendations
        if self.errors["image_errors"] or self.warnings["image_warnings"]:
            recommendations.append("🔧 Update image paths or add missing image files")
            recommendations.append("🔧 Check relative paths in documentation files")

        return recommendations

    def save_report(self):
        """Save the error report to file."""
        report = self.generate_report()

        # Save JSON report
        json_file = self.report_file.with_suffix(".json")
        with open(json_file, "w") as f:
            json.dump(report, f, indent=2, default=str)

        # Save human-readable report
        self._save_human_readable_report(report)

        self.session.log(f"📄 Error report saved to {json_file}")
        self.session.log(f"📄 Human-readable report saved to {self.report_file}")

    def _save_human_readable_report(self, report: Dict):
        """Save a human-readable version of the report."""
        with open(self.report_file, "w") as f:
            f.write(f"# Documentation Build Error Report\n\n")
            f.write(f"**Generated**: {report['metadata']['timestamp']}\n")
            f.write(f"**Package(s)**: {', '.join(report['metadata']['packages'])}\n")
            f.write(f"**Profile**: {report['metadata']['profile']}\n")
            f.write(f"**Duration**: {report['metadata']['duration']:.1f}s\n")
            f.write(
                f"**Success**: {'✅' if report['metadata']['success'] else '❌'}\n\n"
            )

            # Summary
            f.write("## Summary\n\n")
            f.write(f"- **Total Errors**: {report['summary']['total_errors']}\n")
            f.write(f"- **Total Warnings**: {report['summary']['total_warnings']}\n")
            f.write(f"- **Files Processed**: {report['summary']['files_processed']}\n")
            f.write(f"- **HTML Generated**: {report['summary']['html_generated']}\n")
            f.write(
                f"- **Problematic Files**: {report['summary']['problematic_files_count']}\n\n"
            )

            # Errors by category
            if report["errors_by_category"]:
                f.write("## Errors by Category\n\n")
                for category, data in report["errors_by_category"].items():
                    f.write(
                        f"### {category.replace('_', ' ').title()} ({data['count']} errors)\n\n"
                    )
                    for error in data["errors"][:5]:  # Show first 5
                        f.write(f"- **File**: {error.get('file', 'Unknown')}\n")
                        f.write(f"  **Error**: {error['line']}\n")
                        f.write(f"  **Time**: {error['timestamp']}\n\n")

            # Warnings by category
            if report["warnings_by_category"]:
                f.write("## Warnings by Category\n\n")
                for category, data in report["warnings_by_category"].items():
                    f.write(
                        f"### {category.replace('_', ' ').title()} ({data['count']} warnings)\n\n"
                    )
                    for warning in data["warnings"][:3]:  # Show first 3
                        f.write(f"- **File**: {warning.get('file', 'Unknown')}\n")
                        f.write(f"  **Warning**: {warning['line']}\n\n")

            # Problematic files
            if report["problematic_files"]:
                f.write("## Most Problematic Files\n\n")
                sorted_files = sorted(
                    report["problematic_files"].items(),
                    key=lambda x: x[1]["errors"] + x[1]["warnings"],
                    reverse=True,
                )
                for file_path, issues in sorted_files[:10]:
                    f.write(
                        f"- **{file_path}**: {issues['errors']} errors, {issues['warnings']} warnings\n"
                    )
                f.write("\n")

            # Recommendations
            if report["recommendations"]:
                f.write("## Recommendations\n\n")
                for rec in report["recommendations"]:
                    f.write(f"- {rec}\n")


def run_sphinx_with_error_collection(
    session, args: List[str], package: str = "all", profile: str = "full"
) -> ErrorCollector:
    """Run sphinx-build with comprehensive error collection."""

    # Create error collector
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = ERROR_REPORTS_DIR / f"build_errors_{package}_{profile}_{timestamp}.md"
    collector = ErrorCollector(session, report_file)

    # Start collection
    collector.start_collection(package, profile)

    # Run sphinx-build command
    cmd = ["poetry", "run", "sphinx-build"] + args
    session.log(f"🚀 Running: {' '.join(cmd)}")

    try:
        # Run command with real-time output parsing
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True,
            cwd=Path.cwd(),
        )

        # Process output line by line
        for line in process.stdout:
            line = line.strip()
            if line:
                # Show output in real-time
                print(line, flush=True)
                # Collect errors/warnings
                collector.process_line(line)

        # Wait for process to complete
        return_code = process.wait()
        success = return_code == 0

    except Exception as e:
        session.log(f"❌ Exception during build: {e}")
        success = False

    # Finish collection and generate report
    collector.finish_collection(success)
    collector.save_report()

    return collector


@nox.session(python=PYTHON_VERSIONS, name="docs-phased-with-errors")
@nox.parametrize(
    "package",
    ["all", "core", "agents", "tools", "mcp", "games", "dataflow", "prebuilt"],
)
@nox.parametrize("profile", ["minimal", "standard", "full"])
def docs_phased_with_error_collection(session, package, profile):
    """Run docs_phased with comprehensive error collection and analysis."""

    session.log(f"🔍 Building {package} ({profile}) with error collection")

    # Set environment variables for package/profile
    env = {
        "SPHINX_PACKAGES": package,
        "SPHINX_PROFILE": profile,
        "SPHINX_DISABLE_EXAMPLES": "1",  # Disable examples for faster error collection
    }

    session.log(f"📊 Error collection configuration:")
    session.log(f"   SPHINX_PACKAGES = {package}")
    session.log(f"   SPHINX_PROFILE = {profile}")
    session.log(f"   SPHINX_DISABLE_EXAMPLES = 1 (disabled for speed)")
    session.log("   🚫 Examples disabled for faster error collection")

    # Determine output directory
    output_dir = BUILD_DIR / f"{package}_{profile}_with_errors"

    # Build args
    args = [
        "-b",
        "html",
        str(SOURCE_DIR),
        str(output_dir),
        "-E",  # Don't use saved environment
        "-W",
        "--keep-going",  # Treat warnings as errors but continue
    ]

    # Run with error collection
    collector = run_sphinx_with_error_collection(session, args, package, profile)

    # Report results
    session.log(f"📊 Build completed:")
    session.log(f"   📦 Package: {package}")
    session.log(f"   🎚️  Profile: {profile}")
    session.log(f"   ❌ Errors: {collector.stats['total_errors']}")
    session.log(f"   ⚠️  Warnings: {collector.stats['total_warnings']}")
    session.log(f"   📄 Report: {collector.report_file}")
    session.log(f"   🌐 Output: file://{output_dir}/index.html")


@nox.session(python=PYTHON_VERSIONS, name="review-errors")
def review_errors(session):
    """Review and summarize all error reports."""

    session.log("📋 Reviewing all error reports...")

    error_files = list(ERROR_REPORTS_DIR.glob("*.json"))

    if not error_files:
        session.log("❌ No error reports found")
        return

    # Load all reports
    all_errors = {}
    all_warnings = {}
    total_reports = 0

    for error_file in error_files:
        try:
            with open(error_file) as f:
                report = json.load(f)

            total_reports += 1

            # Aggregate errors
            for category, data in report.get("errors_by_category", {}).items():
                if category not in all_errors:
                    all_errors[category] = 0
                all_errors[category] += data["count"]

            # Aggregate warnings
            for category, data in report.get("warnings_by_category", {}).items():
                if category not in all_warnings:
                    all_warnings[category] = 0
                all_warnings[category] += data["count"]

        except Exception as e:
            session.log(f"⚠️ Could not load {error_file}: {e}")

    # Generate summary
    session.log(f"📊 Error Summary from {total_reports} reports:")
    session.log("\n🔴 ERRORS:")
    for category, count in sorted(all_errors.items(), key=lambda x: x[1], reverse=True):
        session.log(f"   {category.replace('_', ' ').title()}: {count}")

    session.log("\n🟡 WARNINGS:")
    for category, count in sorted(
        all_warnings.items(), key=lambda x: x[1], reverse=True
    ):
        session.log(f"   {category.replace('_', ' ').title()}: {count}")

    session.log(f"\n📁 Reports available in: {ERROR_REPORTS_DIR}")
