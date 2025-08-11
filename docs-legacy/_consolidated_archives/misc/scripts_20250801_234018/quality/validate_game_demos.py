#!/usr/bin/env python3
"""Game demo content validation script.

Validates that game demos have proper streaming content,
asciinema players, and interactive elements.

Usage:
    poetry run python docs/validate_game_demos.py
"""

import re
import subprocess
from pathlib import Path


class GameDemoValidator:
    """Validates game demo content in documentation."""

    def __init__(self):
        self.source_dir = Path("docs/source/games/demos")
        self.build_dir = Path("docs/build/html/games/demos")
        self.results: dict[str, list[tuple[str, bool, str]]] = {}

        # Game demos to validate
        self.game_demos = [
            "chess-demo.rst",
            "checkers-demo.rst",
            "tictactoe-demo.rst",
            "mancala-demo.rst",
            "monopoly-demo.rst",
            "among_us-demo.rst",
        ]

    def validate_source_files(self) -> bool:
        """Validate source RST files have proper content."""
        self.results["source_files"] = []
        all_passed = True

        for demo_file in self.game_demos:
            file_path = self.source_dir / demo_file

            if not file_path.exists():
                self.results["source_files"].append(
                    (f"{demo_file} exists", False, "File not found")
                )
                all_passed = False
                continue

            content = file_path.read_text()

            # Check for required elements
            checks = [
                (r"\.\..*class::\s*game-demo", "Game demo class directive"),
                (r"\.\..*class::\s*streaming-content", "Streaming content class"),
                (r"\.\..*raw::\s*html", "Raw HTML directive for embedding"),
                (r"asciinema|asciicast|iframe", "Streaming player element"),
                (r"Game Features|Features", "Features section"),
                (r"How to Play|Gameplay", "How to play section"),
            ]

            for pattern, description in checks:
                found = re.search(pattern, content, re.IGNORECASE | re.MULTILINE)
                passed = found is not None
                details = (
                    f"Line {content[: found.start()].count(chr(10)) + 1}" if found else "Not found"
                )
                self.results["source_files"].append(
                    (f"{demo_file}: {description}", passed, details)
                )
                if not passed:
                    all_passed = False

        return all_passed

    def validate_built_html(self) -> bool:
        """Validate built HTML files have proper content."""
        if not self.build_dir.exists():
            return False

        self.results["built_html"] = []
        all_passed = True

        for demo_file in self.game_demos:
            html_file = demo_file.replace(".rst", ".html")
            file_path = self.build_dir / html_file

            if not file_path.exists():
                self.results["built_html"].append((f"{html_file} exists", False, "File not found"))
                all_passed = False
                continue

            content = file_path.read_text()

            # Check for required HTML elements
            checks = [
                (r'class="[^"]*game-demo[^"]*"', "Game demo class in HTML"),
                (
                    r'class="[^"]*streaming-content[^"]*"',
                    "Streaming content class in HTML",
                ),
                (r"<iframe[^>]*asciinema", "Asciinema iframe"),
                (r'id="player-[^"]*"', "Player element ID"),
                (r"<script[^>]*asciinema-player", "Asciinema player script"),
            ]

            # Alternative streaming methods
            streaming_found = False
            streaming_patterns = [
                r"<iframe[^>]*asciinema",
                r'<div[^>]*id="player',
                r"<asciinema-player",
                r"<script[^>]*AsciinemaPlayer",
                r'<div[^>]*class="[^"]*asciicast',
            ]

            for pattern in streaming_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    streaming_found = True
                    break

            self.results["built_html"].append(
                (
                    f"{html_file}: Has streaming content",
                    streaming_found,
                    ("Streaming element found" if streaming_found else "No streaming elements"),
                )
            )

            if not streaming_found:
                all_passed = False

            # Check standard elements
            for pattern, description in checks:
                found = re.search(pattern, content, re.IGNORECASE)
                if found:  # Only report if found (since we check alternatives)
                    self.results["built_html"].append(
                        (f"{html_file}: {description}", True, "Found")
                    )

        return all_passed

    def validate_asciinema_casts(self) -> bool:
        """Validate asciinema cast files are referenced."""
        self.results["asciinema_casts"] = []

        # Common asciinema cast locations
        cast_patterns = [
            r"https://asciinema\.org/a/\d+",
            r'/casts/[^"]+\.cast',
            r'data-cast-[^=]+="[^"]+"',
        ]

        for demo_file in self.game_demos:
            file_path = self.source_dir / demo_file
            if not file_path.exists():
                continue

            content = file_path.read_text()

            cast_found = False
            for pattern in cast_patterns:
                match = re.search(pattern, content)
                if match:
                    cast_found = True
                    self.results["asciinema_casts"].append(
                        (
                            f"{demo_file}: Cast reference",
                            True,
                            f"Found: {match.group()}",
                        )
                    )
                    break

            if not cast_found:
                self.results["asciinema_casts"].append(
                    (f"{demo_file}: Cast reference", False, "No cast file referenced")
                )

        return len([r for _, r, _ in self.results["asciinema_casts"] if r]) > 0

    def check_example_structure(self):
        """Check if proper example structure is in place."""

    def print_report(self):
        """Print validation report."""
        for _section, checks in self.results.items():
            if not checks:
                continue

            passed = sum(1 for _, p, _ in checks if p)
            len(checks)

            # Group by file
            by_file = {}
            for description, passed, details in checks:
                file_part = description.split(":")[0]
                if file_part not in by_file:
                    by_file[file_part] = []
                by_file[file_part].append((description, passed, details))

            for _file_name, file_checks in by_file.items():
                all(p for _, p, _ in file_checks)

                for description, passed, details in file_checks:
                    if not passed:
                        (description.split(": ", 1)[1] if ": " in description else description)

        # Overall summary
        all_checks = []
        for checks in self.results.values():
            all_checks.extend(checks)

        total_passed = sum(1 for _, p, _ in all_checks if p)
        total_checks = len(all_checks)

        if total_passed == total_checks:
            pass
        else:
            pass

        self.check_example_structure()

    def run_validation(self):
        """Run all validation checks."""
        # Build docs first
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
            check=False,
        )

        if result.returncode != 0:
            return

        # Run validations
        self.validate_source_files()
        self.validate_built_html()
        self.validate_asciinema_casts()

        # Print report
        self.print_report()


def main():
    """Main entry point."""
    validator = GameDemoValidator()
    validator.run_validation()


if __name__ == "__main__":
    main()
