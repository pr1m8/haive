#!/usr/bin/env python3
"""Comprehensive documentation quality pipeline for Haive.

This script runs all documentation quality checks and generates reports.
"""

from __future__ import annotations

import argparse
import contextlib
import json
from pathlib import Path
import subprocess
import sys

# ANSI color codes
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"


class DocQualityChecker:
    """Documentation quality checker for Haive."""

    def __init__(self, verbose: bool = False):
        """Initialize the checker."""
        self.verbose = verbose
        self.results = {}
        self.project_root = Path(__file__).parent.parent

    def run_command(self, cmd: list[str], check: bool = False) -> tuple[int, str, str]:
        """Run a command and return exit code, stdout, stderr."""
        if self.verbose:
            pass

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=self.project_root,
            check=False,
        )

        if check and result.returncode != 0 and result.stderr:
            pass

        return result.returncode, result.stdout, result.stderr

    def check_docstring_coverage(self) -> dict[str, any]:
        """Check docstring coverage with interrogate."""
        cmd = [
            "poetry",
            "run",
            "interrogate",
            "-vv",
            "packages/",
            "--generate-badge",
            "docs/badges/",
        ]
        returncode, stdout, stderr = self.run_command(cmd)

        # Parse output
        coverage = 0.0
        if "TOTAL" in stdout:
            for line in stdout.split("\n"):
                if "TOTAL" in line:
                    parts = line.split()
                    if len(parts) >= 2:
                        with contextlib.suppress(ValueError):
                            coverage = float(parts[-1].rstrip("%"))

        return {
            "coverage": coverage,
            "passed": coverage >= 80,
            "details": stdout if self.verbose else None,
        }

    def check_docstring_style(self) -> dict[str, any]:
        """Check Google-style docstrings with pydocstyle."""
        cmd = [
            "poetry",
            "run",
            "pydocstyle",
            "packages/",
            "--convention=google",
            "--count",
        ]
        returncode, stdout, stderr = self.run_command(cmd)

        error_count = 0
        if stdout:
            lines = stdout.strip().split("\n")
            if lines and lines[-1].isdigit():
                error_count = int(lines[-1])

        return {
            "error_count": error_count,
            "passed": error_count == 0,
            "details": stdout if self.verbose else None,
        }

    def check_docstring_match(self) -> dict[str, any]:
        """Check docstring-function match with darglint."""
        cmd = ["poetry", "run", "darglint", "packages/", "-v", "2"]
        returncode, stdout, stderr = self.run_command(cmd)

        error_count = len([line for line in stdout.split("\n") if line.strip()])

        return {
            "error_count": error_count,
            "passed": error_count == 0,
            "details": stdout if self.verbose else None,
        }

    def check_rst_syntax(self) -> dict[str, any]:
        """Check RST syntax with rstcheck."""
        cmd = ["poetry", "run", "rstcheck-core", "README.rst", "docs/"]
        returncode, stdout, stderr = self.run_command(cmd)

        error_count = len(
            [line for line in (stdout + stderr).split("\n") if "Error" in line],
        )

        return {
            "error_count": error_count,
            "passed": error_count == 0,
            "details": (stdout + stderr) if self.verbose else None,
        }

    def check_spelling(self) -> dict[str, any]:
        """Check spelling with codespell."""
        cmd = [
            "poetry",
            "run",
            "codespell",
            ".",
            "--skip=.git,*.pyc,*.png,*.jpg,.venv,poetry.lock,*.min.js,*.min.css",
        ]
        returncode, stdout, stderr = self.run_command(cmd)

        error_count = len(stdout.strip().split("\n")) if stdout.strip() else 0

        return {
            "error_count": error_count,
            "passed": error_count == 0,
            "details": stdout if self.verbose else None,
        }

    def check_prose_quality(self) -> dict[str, any]:
        """Check prose quality with proselint."""
        cmd = ["poetry", "run", "proselint", "README.md", "docs/"]
        returncode, stdout, stderr = self.run_command(cmd)

        error_count = len(
            [line for line in stdout.split("\n") if line.strip() and ":" in line],
        )

        return {
            "error_count": error_count,
            "passed": error_count == 0,
            "details": stdout if self.verbose else None,
        }

    def check_sphinx_build(self) -> dict[str, any]:
        """Check Sphinx documentation build."""
        cmd = [
            "poetry",
            "run",
            "sphinx-build",
            "-W",
            "-b",
            "html",
            "docs/source",
            "docs/build/html",
        ]
        returncode, stdout, stderr = self.run_command(cmd)

        return {
            "build_success": returncode == 0,
            "passed": returncode == 0,
            "details": (stdout + stderr) if self.verbose else None,
        }

    def run_all_checks(self) -> dict[str, any]:
        """Run all documentation quality checks."""
        self.results["docstring_coverage"] = self.check_docstring_coverage()
        self.results["docstring_style"] = self.check_docstring_style()
        self.results["docstring_match"] = self.check_docstring_match()
        self.results["rst_syntax"] = self.check_rst_syntax()
        self.results["spelling"] = self.check_spelling()
        self.results["prose_quality"] = self.check_prose_quality()
        self.results["sphinx_build"] = self.check_sphinx_build()

        # Calculate overall status
        all_passed = all(check.get("passed", False) for check in self.results.values())

        for _check_name, result in self.results.items():
            "✅" if result.get("passed", False) else "❌"

        if all_passed:
            pass
        else:
            pass

        return self.results

    def save_report(self, output_path: Path):
        """Save results to a JSON report."""
        with open(output_path, "w") as f:
            json.dump(self.results, f, indent=2)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Run documentation quality checks for Haive",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show detailed output",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("docs/quality-report.json"),
        help="Output path for JSON report",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Attempt to auto-fix issues where possible",
    )

    args = parser.parse_args()

    # Run checks
    checker = DocQualityChecker(verbose=args.verbose)
    results = checker.run_all_checks()

    # Save report
    checker.save_report(args.output)

    # Auto-fix if requested
    if args.fix:
        # Fix formatting
        subprocess.run(
            ["poetry", "run", "docformatter", "-i", "-r", "packages/"],
            check=False,
        )

        # Fix spelling interactively

    # Exit with error if checks failed
    all_passed = all(check.get("passed", False) for check in results.values())
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
