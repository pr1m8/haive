#!/usr/bin/env python3
"""
Master documentation test runner.

Runs all documentation validation and testing scripts
and generates a comprehensive report.

Usage:
    poetry run python docs/run_all_doc_tests.py [--screenshots] [--visual]
"""

import argparse
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple


class DocumentationTestRunner:
    """Runs all documentation tests and validations."""

    def __init__(self, run_screenshots: bool = False, run_visual: bool = False):
        self.run_screenshots = run_screenshots
        self.run_visual = run_visual
        self.results: Dict[str, Tuple[bool, str]] = {}
        self.start_time = time.time()

    def run_command(self, name: str, command: List[str]) -> Tuple[bool, str]:
        """Run a command and capture results."""
        print(f"\n{'=' * 60}")
        print(f"Running: {name}")
        print(f"Command: {' '.join(command)}")
        print("=" * 60)

        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            print(result.stdout)
            if result.stderr:
                print("Warnings:", result.stderr)
            return True, "Success"
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed with exit code: {e.returncode}")
            print("STDOUT:", e.stdout)
            print("STDERR:", e.stderr)
            return False, f"Exit code {e.returncode}"
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False, str(e)

    def build_documentation(self):
        """Build the documentation."""
        print("🔨 Building documentation...")
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
        print("\n🎨 Validating CSS fixes...")
        success, msg = self.run_command(
            "CSS Validation", ["poetry", "run", "python", "docs/validate_css_fixes.py"]
        )
        self.results["CSS Validation"] = (success, msg)

    def run_game_demo_validation(self):
        """Run game demo validation."""
        print("\n🎮 Validating game demos...")
        success, msg = self.run_command(
            "Game Demo Validation",
            ["poetry", "run", "python", "docs/validate_game_demos.py"],
        )
        self.results["Game Demo Validation"] = (success, msg)

    def run_screenshot_tests(self):
        """Run comprehensive screenshot tests."""
        if not self.run_screenshots:
            print("\n📸 Skipping screenshot tests (use --screenshots to enable)")
            return

        print("\n📸 Running screenshot tests (this may take a few minutes)...")
        success, msg = self.run_command(
            "Screenshot Tests",
            ["poetry", "run", "python", "docs/test_documentation_screenshots.py"],
        )
        self.results["Screenshot Tests"] = (success, msg)

    def run_visual_check(self):
        """Run visual check."""
        if not self.run_visual:
            print("\n👁️  Skipping visual check (use --visual to enable)")
            return

        print("\n👁️  Running visual check (will open browser)...")
        success, msg = self.run_command(
            "Visual Check", ["poetry", "run", "python", "docs/quick_visual_check.py"]
        )
        self.results["Visual Check"] = (success, msg)

    def check_generated_files(self):
        """Check for generated test files."""
        print("\n📁 Checking generated files...")

        files_to_check = [
            ("Screenshot directory", Path("docs/test_screenshots")),
            ("Test report", Path("docs/documentation_test_report.md")),
            ("Built docs", Path("docs/build/html/index.html")),
            ("Custom CSS", Path("docs/build/html/_static/haive-minimal.css")),
        ]

        for name, path in files_to_check:
            exists = path.exists()
            status = "✅" if exists else "❌"
            print(f"  {status} {name}: {path}")

    def generate_summary_report(self):
        """Generate summary report."""
        elapsed = time.time() - self.start_time

        print("\n" + "=" * 60)
        print("DOCUMENTATION TEST SUMMARY")
        print("=" * 60)
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Duration: {elapsed:.1f} seconds")
        print()

        # Results summary
        passed = sum(1 for success, _ in self.results.values() if success)
        total = len(self.results)

        print(f"Tests run: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print()

        # Detailed results
        print("Detailed Results:")
        print("-" * 40)
        for test_name, (success, message) in self.results.items():
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"{status}: {test_name}")
            if not success:
                print(f"       {message}")

        # Recommendations
        if total - passed > 0:
            print("\n⚠️  Some tests failed. Recommendations:")

            if not self.results.get("Documentation Build", (True, ""))[0]:
                print("  1. Fix documentation build errors first")
                print(
                    "     Run: poetry run sphinx-build -b html docs/source docs/build/html"
                )

            if not self.results.get("CSS Validation", (True, ""))[0]:
                print("  2. Fix CSS alignment issues")
                print("     Edit: docs/source/_static/haive-minimal.css")

            if not self.results.get("Game Demo Validation", (True, ""))[0]:
                print("  3. Add streaming content to game demos")
                print("     Edit: docs/source/games/demos/*.rst files")
        else:
            print("\n✅ All tests passed! Documentation is ready.")

        # File locations
        print("\n📍 Important file locations:")
        print("  - Built docs: docs/build/html/")
        print("  - Screenshots: docs/test_screenshots/")
        print("  - Test report: docs/documentation_test_report.md")
        print("  - Custom CSS: docs/source/_static/haive-minimal.css")

        # Next steps
        print("\n🚀 Next steps:")
        if self.run_screenshots:
            print("  - Review screenshots in docs/test_screenshots/")
            print("  - Check docs/documentation_test_report.md for details")
        else:
            print("  - Run with --screenshots for comprehensive testing")

        if not self.run_visual:
            print("  - Run with --visual for manual inspection")

        print(
            "  - Serve docs locally: cd docs/build/html && python -m http.server 8000"
        )

    def run_all_tests(self):
        """Run all documentation tests."""
        print("🚀 Starting comprehensive documentation tests...")

        # Build documentation first
        if not self.build_documentation():
            print(
                "\n❌ Documentation build failed. Fix build errors before running other tests."
            )
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
    parser = argparse.ArgumentParser(
        description="Run comprehensive documentation tests"
    )
    parser.add_argument(
        "--screenshots",
        action="store_true",
        help="Run screenshot tests (requires Playwright)",
    )
    parser.add_argument(
        "--visual", action="store_true", help="Run visual check (opens browser)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all tests including screenshots and visual",
    )

    args = parser.parse_args()

    if args.all:
        args.screenshots = True
        args.visual = True

    runner = DocumentationTestRunner(
        run_screenshots=args.screenshots, run_visual=args.visual
    )

    success = runner.run_all_tests()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
