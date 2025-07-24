#!/usr/bin/env python3
"""
Game demo content validation script.

Validates that game demos have proper streaming content,
asciinema players, and interactive elements.

Usage:
    poetry run python docs/validate_game_demos.py
"""

import json
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple


class GameDemoValidator:
    """Validates game demo content in documentation."""
    
    def __init__(self):
        self.source_dir = Path("docs/source/games/demos")
        self.build_dir = Path("docs/build/html/games/demos")
        self.results: Dict[str, List[Tuple[str, bool, str]]] = {}
        
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
                details = f"Line {content[:found.start()].count(chr(10)) + 1}" if found else "Not found"
                self.results["source_files"].append(
                    (f"{demo_file}: {description}", passed, details)
                )
                if not passed:
                    all_passed = False
                    
        return all_passed
        
    def validate_built_html(self) -> bool:
        """Validate built HTML files have proper content."""
        if not self.build_dir.exists():
            print("❌ Build directory not found. Run 'poetry run nox -s docs' first.")
            return False
            
        self.results["built_html"] = []
        all_passed = True
        
        for demo_file in self.game_demos:
            html_file = demo_file.replace(".rst", ".html")
            file_path = self.build_dir / html_file
            
            if not file_path.exists():
                self.results["built_html"].append(
                    (f"{html_file} exists", False, "File not found")
                )
                all_passed = False
                continue
                
            content = file_path.read_text()
            
            # Check for required HTML elements
            checks = [
                (r'class="[^"]*game-demo[^"]*"', "Game demo class in HTML"),
                (r'class="[^"]*streaming-content[^"]*"', "Streaming content class in HTML"),
                (r'<iframe[^>]*asciinema', "Asciinema iframe"),
                (r'id="player-[^"]*"', "Player element ID"),
                (r'<script[^>]*asciinema-player', "Asciinema player script"),
            ]
            
            # Alternative streaming methods
            streaming_found = False
            streaming_patterns = [
                r'<iframe[^>]*asciinema',
                r'<div[^>]*id="player',
                r'<asciinema-player',
                r'<script[^>]*AsciinemaPlayer',
                r'<div[^>]*class="[^"]*asciicast',
            ]
            
            for pattern in streaming_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    streaming_found = True
                    break
                    
            self.results["built_html"].append(
                (f"{html_file}: Has streaming content", streaming_found, 
                 "Streaming element found" if streaming_found else "No streaming elements")
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
            r'https://asciinema\.org/a/\d+',
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
                        (f"{demo_file}: Cast reference", True, f"Found: {match.group()}")
                    )
                    break
                    
            if not cast_found:
                self.results["asciinema_casts"].append(
                    (f"{demo_file}: Cast reference", False, "No cast file referenced")
                )
                
        return len([r for _, r, _ in self.results["asciinema_casts"] if r]) > 0
        
    def check_example_structure(self):
        """Check if proper example structure is in place."""
        example_template = """
.. class:: game-demo streaming-content

   .. raw:: html

      <div id="player-{game_name}"></div>
      <script src="https://asciinema.org/a/{cast_id}.js" 
              id="asciicast-{cast_id}" 
              async 
              data-autoplay="true"
              data-theme="monokai"
              data-size="medium">
      </script>
"""
        
        print("\n📝 Example Game Demo Structure:")
        print("-" * 60)
        print(example_template)
        print("-" * 60)
        print("\nEnsure your game demo RST files follow this structure!")
        
    def print_report(self):
        """Print validation report."""
        print("=" * 60)
        print("GAME DEMO VALIDATION REPORT")
        print("=" * 60)
        
        for section, checks in self.results.items():
            if not checks:
                continue
                
            print(f"\n## {section.replace('_', ' ').title()}")
            print("-" * 40)
            
            passed = sum(1 for _, p, _ in checks if p)
            total = len(checks)
            
            print(f"Passed: {passed}/{total}")
            print()
            
            # Group by file
            by_file = {}
            for description, passed, details in checks:
                file_part = description.split(":")[0]
                if file_part not in by_file:
                    by_file[file_part] = []
                by_file[file_part].append((description, passed, details))
                
            for file_name, file_checks in by_file.items():
                file_passed = all(p for _, p, _ in file_checks)
                file_status = "✅" if file_passed else "❌"
                print(f"\n{file_status} {file_name}")
                
                for description, passed, details in file_checks:
                    if not passed:
                        check_name = description.split(": ", 1)[1] if ": " in description else description
                        print(f"   ❌ {check_name} - {details}")
                        
        # Overall summary
        all_checks = []
        for checks in self.results.values():
            all_checks.extend(checks)
            
        total_passed = sum(1 for _, p, _ in all_checks if p)
        total_checks = len(all_checks)
        
        print("\n" + "=" * 60)
        print(f"OVERALL: {total_passed}/{total_checks} checks passed")
        
        if total_passed == total_checks:
            print("✅ All game demo validation checks passed!")
        else:
            print("❌ Some game demo validation checks failed.")
            print("\nTo fix:")
            print("1. Add streaming content to game demo RST files")
            print("2. Use asciinema or similar for game recordings")
            print("3. Include proper CSS classes (game-demo, streaming-content)")
            print("4. Rebuild documentation: poetry run nox -s docs")
            
        self.check_example_structure()
        
    def run_validation(self):
        """Run all validation checks."""
        print("Starting game demo validation...\n")
        
        # Build docs first
        print("Building documentation...")
        result = subprocess.run(
            ["poetry", "run", "sphinx-build", "-b", "html", "docs/source", "docs/build/html"],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print("❌ Documentation build failed!")
            print(result.stderr)
            return
            
        print("✅ Documentation built successfully\n")
        
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