#!/usr/bin/env python3
"""Find files with problematic characters in filenames that can cause build issues."""

import os
import re
from pathlib import Path
from typing import List, Tuple

# Define problematic patterns
PROBLEMATIC_PATTERNS = {
    "spaces": re.compile(r"\s"),
    "parentheses": re.compile(r"[()]"),
    "brackets": re.compile(r"[\[\]]"),
    "special_chars": re.compile(r'[!@#$%^&*+={}|\\:;"\'<>?,]'),
    "unicode": re.compile(r"[^\x00-\x7F]"),  # Non-ASCII characters
    "double_extension": re.compile(r"\.[^.]+\.[^.]+$"),  # e.g., .test.py
}


def find_problematic_files(root_dir: str = ".") -> dict[str, List[Tuple[str, str]]]:
    """Find all files with problematic characters in their names.

    Returns:
        Dictionary mapping problem type to list of (filepath, matched_pattern) tuples
    """
    problems = {key: [] for key in PROBLEMATIC_PATTERNS}

    # Walk through all files
    for root, dirs, files in os.walk(root_dir):
        # Skip hidden directories and common build/cache directories
        dirs[:] = [
            d
            for d in dirs
            if not d.startswith(".")
            and d not in ["__pycache__", "node_modules", "build", "dist"]
        ]

        for filename in files:
            # Skip hidden files
            if filename.startswith("."):
                continue

            filepath = os.path.join(root, filename)

            # Check each pattern
            for pattern_name, pattern in PROBLEMATIC_PATTERNS.items():
                if pattern.search(filename):
                    match = pattern.search(filename)
                    problems[pattern_name].append((filepath, match.group(0)))

    return problems


def main():
    """Main function to find and report problematic files."""
    print("🔍 Searching for files with problematic characters...\n")

    # Find problems in packages directory
    packages_dir = "packages"
    if os.path.exists(packages_dir):
        print(f"Scanning {packages_dir}/...\n")
        problems = find_problematic_files(packages_dir)
    else:
        print("Scanning current directory...\n")
        problems = find_problematic_files(".")

    # Report findings
    total_issues = sum(len(files) for files in problems.values())

    if total_issues == 0:
        print("✅ No problematic filenames found!")
        return

    print(f"❌ Found {total_issues} files with problematic characters:\n")

    # Group by problem type
    for problem_type, files in problems.items():
        if files:
            print(f"\n{'=' * 60}")
            print(f"🚨 {problem_type.upper().replace('_', ' ')} ({len(files)} files):")
            print(f"{'=' * 60}")

            # Show first 10 examples
            for filepath, matched in files[:10]:
                print(f"  - {filepath}")
                print(f"    → Matched: '{matched}'")

            if len(files) > 10:
                print(f"  ... and {len(files) - 10} more files")

    # Summary and recommendations
    print(f"\n{'=' * 60}")
    print("📊 SUMMARY:")
    print(f"{'=' * 60}")

    for problem_type, files in problems.items():
        if files:
            print(f"  - {problem_type}: {len(files)} files")

    print("\n💡 RECOMMENDATIONS:")
    print("  1. Rename files to use underscores instead of spaces")
    print("  2. Remove parentheses and special characters")
    print("  3. Use simple alphanumeric filenames with underscores")
    print("  4. Consider using a batch rename script")

    # Generate rename suggestions
    print("\n📝 Example rename commands:")
    count = 0
    for problem_type, files in problems.items():
        for filepath, _ in files[:5]:  # Show first 5 examples
            dirname = os.path.dirname(filepath)
            filename = os.path.basename(filepath)

            # Create safe filename
            safe_name = filename
            safe_name = re.sub(r"\s+", "_", safe_name)  # Replace spaces
            safe_name = re.sub(r"[()]", "", safe_name)  # Remove parentheses
            safe_name = re.sub(r"[^\w.-]", "_", safe_name)  # Replace special chars
            safe_name = re.sub(r"_+", "_", safe_name)  # Collapse multiple underscores
            safe_name = safe_name.strip("_")  # Remove leading/trailing underscores

            if safe_name != filename:
                print(f"\n  mv '{filepath}' '{os.path.join(dirname, safe_name)}'")
                count += 1
                if count >= 5:
                    print("\n  ... (showing first 5 examples only)")
                    break
        if count >= 5:
            break


if __name__ == "__main__":
    main()
