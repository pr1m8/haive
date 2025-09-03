#!/usr/bin/env python3
"""Master documentation test runner.

Runs all documentation validation and testing scripts
and generates a comprehensive report.

Usage:
    poetry run python docs/run_all_doc_tests.py [--screenshots] [--visual]
"""

import argparse
import subprocess
import sys
import time
from pathlib import Path


class DocumentationTestRunner:
    """Runs all documentation tests and validations."""

    def __init__(self, run_screenshots: bool = False, run_visual: bool = False):
        self.run_screenshots = run_screenshots
        self.run_visual = run_visual
        self.results: dict[str, tuple[bool, str]] = {}
        self.start_time = time.time()

    def run_command(self, name: str, command: list[str]) -> tuple[bool, str]:
        """Run a command and capture results."""
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            if result.stderr:
                pass
            return True, "Success"
        except subprocess.CalledProcessError as e:
            return False, f"Exit code {e.returncode}"
        except Exception as e:
            return False, str(e)

    def build_documentation(self):
        """Build the documentation."""
        success, msg = self.run_command(
            "Documentation Build",
            [
                "poetry",
                "run",
                "sphinx-build",
                "-b",
                "html",
                "docs/source",
                "docs/build/html",
            ],
        )
        self.results["Documentation Build"] = (success, msg)
        return success

    def run_css_validation(self):
        """Run CSS validation."""
        success, msg = self.run_command(
            "CSS Validation", ["poetry", "run", "python", "docs/validate_css_fixes.py"]
        )
        self.results["CSS Validation"] = (success, msg)

    def run_game_demo_validation(self):
        """Run game demo validation."""
        success, msg = self.run_command(
            "Game Demo Validation",
            ["poetry", "run", "python", "docs/validate_game_demos.py"],
        )
        self.results["Game Demo Validation"] = (success, msg)

    def run_screenshot_tests(self):
        """Run comprehensive screenshot tests."""
        if not self.run_screenshots:
            return

        success, msg = self.run_command(
            "Screenshot Tests",
            ["poetry", "run", "python", "docs/test_documentation_screenshots.py"],
        )
        self.results["Screenshot Tests"] = (success, msg)

    def run_visual_check(self):
        """Run visual check."""
        if not self.run_visual:
            return

        success, msg = self.run_command(
            "Visual Check", ["poetry", "run", "python", "docs/quick_visual_check.py"]
        )
        self.results["Visual Check"] = (success, msg)

    def check_generated_files(self):
        """Check for generated test files."""
        files_to_check = [
            ("Screenshot directory", Path("docs/test_screenshots")),
            ("Test report", Path("docs/documentation_test_report.md")),
            ("Built docs", Path("docs/build/html/index.html")),
            ("Custom CSS", Path("docs/build/html/_static/haive-minimal.css")),
        ]

        for _name, path in files_to_check:
            path.exists()

    def generate_summary_report(self):
        """Generate summary report."""
        time.time() - self.start_time

        # Results summary
        passed = sum(1 for success, _ in self.results.values() if success)
        total = len(self.results)

        # Detailed results
        for _test_name, (success, _message) in self.results.items():
            if not success:
                pass

        # Recommendations
        if total - passed > 0:
            if not self.results.get("Documentation Build", (True, ""))[0]:
                pass

            if not self.results.get("CSS Validation", (True, ""))[0]:
                pass

            if not self.results.get("Game Demo Validation", (True, ""))[0]:
                pass
        else:
            pass

        # File locations

        # Next steps
        if self.run_screenshots:
            pass
        else:
            pass

        if not self.run_visual:
            pass

    def run_all_tests(self):
        """Run all documentation tests."""
        # Build documentation first
        if not self.build_documentation():
            self.generate_summary_report()
            return False

        # Run validations
        self.run_css_validation()
        self.run_game_demo_validation()

        # Run optional tests
        self.run_screenshot_tests()
        self.run_visual_check()

        # Check generated files
        self.check_generated_files()

        # Generate summary
        self.generate_summary_report()

        # Return success if all required tests passed
        required_tests = [
            "Documentation Build",
            "CSS Validation",
            "Game Demo Validation",
        ]
        return all(self.results.get(test, (False, ""))[0] for test in required_tests)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Run comprehensive documentation tests")
    parser.add_argument(
        "--screenshots",
        action="store_true",
        help="Run screenshot tests (requires Playwright)",
    )
    parser.add_argument("--visual", action="store_true", help="Run visual check (opens browser)")
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all tests including screenshots and visual",
    )

    args = parser.parse_args()

    if args.all:
        args.screenshots = True
        args.visual = True

    runner = DocumentationTestRunner(run_screenshots=args.screenshots, run_visual=args.visual)

    success = runner.run_all_tests()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
