#!/usr/bin/env python3
"""Run full automation workflow for Haive project.

This script runs all available automation tools in the correct order to
maximize code quality improvements.
"""

from __future__ import annotations

import subprocess
import time
from datetime import datetime
from pathlib import Path


class AutomationRunner:
    """Run automation tools in optimal order."""

    def __init__(self, target_path: str = "packages/"):
        self.target_path = Path(target_path)
        self.results: dict[str, dict] = {}
        self.start_time = time.time()

    def run_command(self, cmd: list[str], description: str) -> tuple[bool, str, float]:
        """Run a command and track results."""
        start = time.time()
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            elapsed = time.time() - start
            return True, result.stdout, elapsed
        except subprocess.CalledProcessError as e:
            elapsed = time.time() - start
            return False, e.stderr, elapsed

    def phase1_parse_fixes(self):
        """Phase 1: Fix parse errors and syntax issues."""
        # Fix common parse patterns
        if Path("scripts/fix_parse_patterns.py").exists():
            success, output, elapsed = self.run_command(
                [
                    "poetry",
                    "run",
                    "python",
                    "scripts/fix_parse_patterns.py",
                    str(self.target_path),
                ],
                "Fixing parse patterns",
            )
            self.results["parse_patterns"] = {
                "success": success,
                "time": elapsed,
                "output": output,
            }

        # Run trunk auto-fix
        success, output, elapsed = self.run_command(
            ["trunk", "check", "--fix", "--all"],
            "Running trunk auto-fixes",
        )
        self.results["trunk_fix"] = {
            "success": success,
            "time": elapsed,
            "output": output,
        }

    def phase2_imports_cleanup(self):
        """Phase 2: Clean up imports and unused code."""
        # Remove unused imports with autoflake
        success, output, elapsed = self.run_command(
            [
                "poetry",
                "run",
                "autoflake",
                "--remove-all-unused-imports",
                "--remove-unused-variables",
                "--in-place",
                "--recursive",
                str(self.target_path),
            ],
            "Removing unused imports and variables",
        )
        self.results["autoflake"] = {
            "success": success,
            "time": elapsed,
            "output": output,
        }

        # Sort imports with isort
        success, output, elapsed = self.run_command(
            ["poetry", "run", "isort", str(self.target_path)],
            "Sorting imports with isort",
        )
        self.results["isort"] = {"success": success, "time": elapsed, "output": output}

    def phase3_type_hints(self):
        """Phase 3: Add and fix type hints."""
        # Run our custom type hint fixer
        if Path("scripts/type_hint_fixer.py").exists():
            for package in ["haive-core", "haive-agents", "haive-tools"]:
                success, output, elapsed = self.run_command(
                    [
                        "poetry",
                        "run",
                        "python",
                        "scripts/type_hint_fixer.py",
                        "--package",
                        package,
                    ],
                    f"Adding type hints to {package}",
                )
                self.results[f"type_hints_{package}"] = {
                    "success": success,
                    "time": elapsed,
                    "output": output,
                }

        # Run autotyping for additional hints
        success, output, elapsed = self.run_command(
            ["poetry", "run", "autotyping", "--safe-imports", str(self.target_path)],
            "Running autotyping",
        )
        self.results["autotyping"] = {
            "success": success,
            "time": elapsed,
            "output": output,
        }

    def phase4_formatting(self):
        """Phase 4: Format code consistently."""
        # Format with black
        success, output, elapsed = self.run_command(
            ["poetry", "run", "black", str(self.target_path)],
            "Formatting with black",
        )
        self.results["black"] = {"success": success, "time": elapsed, "output": output}

        # Additional formatting with autopep8
        success, output, elapsed = self.run_command(
            [
                "poetry",
                "run",
                "autopep8",
                "--in-place",
                "--aggressive",
                "--recursive",
                str(self.target_path),
            ],
            "Additional formatting with autopep8",
        )
        self.results["autopep8"] = {
            "success": success,
            "time": elapsed,
            "output": output,
        }

    def phase5_documentation(self):
        """Phase 5: Check and improve documentation."""
        # Check docstring coverage
        success, output, elapsed = self.run_command(
            ["poetry", "run", "interrogate", str(self.target_path), "-vv"],
            "Checking docstring coverage",
        )
        self.results["interrogate"] = {
            "success": success,
            "time": elapsed,
            "output": output,
        }

        # Validate docstring style
        success, output, elapsed = self.run_command(
            [
                "poetry",
                "run",
                "pydocstyle",
                "--convention=google",
                str(self.target_path),
            ],
            "Validating docstring style",
        )
        self.results["pydocstyle"] = {
            "success": success,
            "time": elapsed,
            "output": output,
        }

        # Check docstring/implementation match
        success, output, elapsed = self.run_command(
            ["poetry", "run", "darglint", str(self.target_path)],
            "Checking docstring accuracy",
        )
        self.results["darglint"] = {
            "success": success,
            "time": elapsed,
            "output": output,
        }

    def phase6_quality_checks(self):
        """Phase 6: Run quality and type checks."""
        # Run ruff linter
        success, output, elapsed = self.run_command(
            ["poetry", "run", "ruff", "check", str(self.target_path)],
            "Running ruff linter",
        )
        self.results["ruff"] = {"success": success, "time": elapsed, "output": output}

        # Run mypy type checker
        success, output, elapsed = self.run_command(
            [
                "poetry",
                "run",
                "mypy",
                str(self.target_path),
                "--ignore-missing-imports",
            ],
            "Running mypy type checker",
        )
        self.results["mypy"] = {"success": success, "time": elapsed, "output": output}

        # Run pyright type checker
        success, output, elapsed = self.run_command(
            ["poetry", "run", "pyright", str(self.target_path)],
            "Running pyright type checker",
        )
        self.results["pyright"] = {
            "success": success,
            "time": elapsed,
            "output": output,
        }

    def phase7_testing(self):
        """Phase 7: Run tests to ensure nothing broke."""
        # Run tests with coverage
        success, output, elapsed = self.run_command(
            ["poetry", "run", "pytest", "--cov=haive", "-n", "auto"],
            "Running tests with coverage",
        )
        self.results["pytest"] = {"success": success, "time": elapsed, "output": output}

    def generate_report(self):
        """Generate summary report."""
        total_time = time.time() - self.start_time
        successful = sum(1 for r in self.results.values() if r["success"])
        failed = len(self.results) - successful

        for tool, result in self.results.items():
            "✅" if result["success"] else "❌"

        # Save detailed report
        report_path = Path(
            f"automation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        )
        with open(report_path, "w") as f:
            f.write("HAIVE AUTOMATION REPORT\n")
            f.write("=" * 60 + "\n")
            f.write(f"Date: {datetime.now()}\n")
            f.write(f"Total Time: {total_time:.1f}s\n")
            f.write(f"Successful: {successful}/{len(self.results)}\n")
            f.write(f"Failed: {failed}/{len(self.results)}\n\n")

            for tool, result in self.results.items():
                f.write(f"\n{'=' * 40}\n")
                f.write(f"Tool: {tool}\n")
                f.write(f"Status: {'Success' if result['success'] else 'Failed'}\n")
                f.write(f"Time: {result['time']:.1f}s\n")
                f.write(f"Output:\n{result['output'][:1000]}\n")

    def run_all_phases(self):
        """Run all automation phases."""
        # Run phases in order
        self.phase1_parse_fixes()
        self.phase2_imports_cleanup()
        self.phase3_type_hints()
        self.phase4_formatting()
        self.phase5_documentation()
        self.phase6_quality_checks()
        self.phase7_testing()

        # Generate report
        self.generate_report()


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Run full automation workflow")
    parser.add_argument(
        "--target",
        default="packages/",
        help="Target directory to process",
    )
    parser.add_argument("--skip-tests", action="store_true", help="Skip running tests")

    args = parser.parse_args()

    runner = AutomationRunner(args.target)

    if args.skip_tests:
        # Remove testing phase
        runner.phase7_testing = lambda: None

    runner.run_all_phases()


if __name__ == "__main__":
    main()
