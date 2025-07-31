#!/usr/bin/env python3
"""
CSS validation script for documentation.

Validates that CSS fixes for alignment and game streaming content
are properly applied in the built documentation.

Usage:
    poetry run python docs/validate_css_fixes.py
"""

import re
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple


class CSSValidator:
    """Validates CSS fixes in documentation."""

    def __init__(self):
        self.source_css = Path("docs/source/_static/haive-minimal.css")
        self.build_dir = Path("docs/build/html")
        self.results: Dict[str, List[Tuple[str, bool, str]]] = {}

    def validate_source_css(self) -> bool:
        """Validate the source CSS file has required fixes."""
        if not self.source_css.exists():
            print("❌ Source CSS file not found: docs/source/_static/haive-minimal.css")
            return False

        content = self.source_css.read_text()

        # Required CSS patterns
        required_patterns = [
            # Container alignment fixes
            (r"\.container\s*{[^}]*max-width:\s*1200px", "Container max-width set"),
            (
                r"\.container\s*{[^}]*margin:\s*0\s+auto",
                "Container centered with margin",
            ),
            (r"\.container\s*{[^}]*padding:\s*0\s+20px", "Container padding set"),
            # Main content alignment
            (r"\.body\s*{[^}]*text-align:\s*left", "Body text aligned left"),
            (
                r"\[role=\"main\"\]\s*{[^}]*text-align:\s*left",
                "Main content aligned left",
            ),
            # Navigation fixes
            (r"\.navbar\s*{[^}]*background-color:", "Navbar background set"),
            (r"\.navbar\s*{[^}]*border-bottom:", "Navbar border set"),
            # Game demo styles
            (r"\.game-demo\s*{", "Game demo class defined"),
            (r"\.streaming-content\s*{", "Streaming content class defined"),
            (r"\.game-board\s*{", "Game board class defined"),
            # Responsive styles
            (r"@media.*max-width:\s*768px", "Mobile responsive styles"),
            # Code block alignment
            (r"\.highlight\s*{[^}]*text-align:\s*left", "Code blocks aligned left"),
            (r"pre\s*{[^}]*text-align:\s*left", "Pre blocks aligned left"),
        ]

        self.results["source_css"] = []
        all_passed = True

        for pattern, description in required_patterns:
            found = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            passed = found is not None
            details = f"Found at position {found.start()}" if found else "Not found"
            self.results["source_css"].append((description, passed, details))
            if not passed:
                all_passed = False

        return all_passed

    def validate_built_css(self) -> bool:
        """Validate CSS in built documentation."""
        if not self.build_dir.exists():
            print("❌ Build directory not found. Run 'poetry run nox -s docs' first.")
            return False

        # Find all CSS files in build
        css_files = list(self.build_dir.rglob("*.css"))

        if not css_files:
            print("❌ No CSS files found in build directory")
            return False

        # Check if haive-minimal.css is copied
        haive_css = self.build_dir / "_static" / "haive-minimal.css"
        if not haive_css.exists():
            print("❌ haive-minimal.css not found in build directory")
            return False

        # Validate it matches source
        source_content = self.source_css.read_text()
        built_content = haive_css.read_text()

        self.results["built_css"] = []

        if source_content == built_content:
            self.results["built_css"].append(
                ("CSS file copied correctly", True, "Files match")
            )
        else:
            self.results["built_css"].append(
                ("CSS file copied correctly", False, "Files differ")
            )
            return False

        return True

    def validate_html_structure(self) -> bool:
        """Validate HTML structure includes necessary classes."""
        html_files_to_check = [
            ("index.html", "Homepage"),
            ("agents/index.html", "Agents index"),
            ("games/demos/chess-demo.html", "Chess demo"),
            ("games/demos/checkers-demo.html", "Checkers demo"),
        ]

        self.results["html_structure"] = []
        all_passed = True

        for file_path, description in html_files_to_check:
            full_path = self.build_dir / file_path
            if not full_path.exists():
                self.results["html_structure"].append(
                    (f"{description} exists", False, "File not found")
                )
                all_passed = False
                continue

            content = full_path.read_text()

            # Check for required elements
            checks = [
                (r"<link[^>]+haive-minimal\.css", f"{description}: Custom CSS linked"),
                (
                    r'class="[^"]*container[^"]*"',
                    f"{description}: Container class present",
                ),
                (r'role="main"', f"{description}: Main role present"),
            ]

            # Additional checks for game demos
            if "demo" in file_path:
                checks.extend(
                    [
                        (
                            r'class="[^"]*game-demo[^"]*"',
                            f"{description}: Game demo class",
                        ),
                        (
                            r'class="[^"]*streaming-content[^"]*"',
                            f"{description}: Streaming content class",
                        ),
                    ]
                )

            for pattern, check_desc in checks:
                found = re.search(pattern, content, re.IGNORECASE)
                passed = found is not None
                details = "Found" if found else "Not found"
                self.results["html_structure"].append((check_desc, passed, details))
                if not passed:
                    all_passed = False

        return all_passed

    def print_report(self):
        """Print validation report."""
        print("=" * 60)
        print("CSS VALIDATION REPORT")
        print("=" * 60)

        for section, checks in self.results.items():
            print(f"\n## {section.replace('_', ' ').title()}")
            print("-" * 40)

            passed = sum(1 for _, p, _ in checks if p)
            total = len(checks)

            print(f"Passed: {passed}/{total}")
            print()

            for description, passed, details in checks:
                status = "✅" if passed else "❌"
                print(f"{status} {description}")
                if not passed:
                    print(f"   → {details}")

        # Overall summary
        all_checks = []
        for checks in self.results.values():
            all_checks.extend(checks)

        total_passed = sum(1 for _, p, _ in all_checks if p)
        total_checks = len(all_checks)

        print("\n" + "=" * 60)
        print(f"OVERALL: {total_passed}/{total_checks} checks passed")

        if total_passed == total_checks:
            print("✅ All CSS validation checks passed!")
        else:
            print("❌ Some CSS validation checks failed.")
            print("\nTo fix:")
            print(
                "1. Update docs/source/_static/haive-minimal.css with required styles"
            )
            print("2. Rebuild documentation: poetry run nox -s docs")
            print("3. Run this validator again")

    def run_validation(self):
        """Run all validation checks."""
        print("Starting CSS validation...\n")

        # Build docs first
        print("Building documentation...")
        result = subprocess.run(
            [
                "poetry",
                "run",
                "sphinx-build",
                "-b",
                "html",
                "docs/source",
                "docs/build/html",
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            print("❌ Documentation build failed!")
            print(result.stderr)
            return

        print("✅ Documentation built successfully\n")

        # Run validations
        self.validate_source_css()
        self.validate_built_css()
        self.validate_html_structure()

        # Print report
        self.print_report()


def main():
    """Main entry point."""
    validator = CSSValidator()
    validator.run_validation()


if __name__ == "__main__":
    main()
