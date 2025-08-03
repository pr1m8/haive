#!/usr/bin/env python3
"""
CSS Audit Script
Identifies unused CSS rules, duplicate styles, and optimization opportunities.
"""

import hashlib
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class CSSAuditor:
    """Audit CSS files for optimization opportunities."""

    def __init__(self, docs_dir: Path):
        self.docs_dir = docs_dir
        self.source_dir = docs_dir / "source"
        self.css_files = list(self.source_dir.rglob("*.css"))
        self.html_files = list(self.source_dir.rglob("*.html"))
        self.rst_files = list(self.source_dir.rglob("*.rst"))

        self.css_rules = {}
        self.selector_usage = defaultdict(int)
        self.duplicate_rules = defaultdict(list)

    def audit_all(self):
        """Run complete CSS audit."""
        print("🎨 CSS Audit Report\n")

        self.parse_css_files()
        self.find_duplicate_rules()
        self.analyze_selector_usage()
        self.check_file_sizes()
        self.identify_optimization_opportunities()

        self.print_report()

    def parse_css_files(self):
        """Parse all CSS files and extract rules."""
        print("1️⃣ Parsing CSS files...")

        for css_file in self.css_files:
            rel_path = str(css_file.relative_to(self.source_dir))
            print(f"   📄 {rel_path}")

            try:
                with open(css_file, "r", encoding="utf-8") as f:
                    content = f.read()

                # Extract CSS rules (simplified parser)
                rules = self.extract_css_rules(content)
                self.css_rules[rel_path] = {
                    "content": content,
                    "rules": rules,
                    "size": len(content),
                    "line_count": content.count("\n") + 1,
                }

            except Exception as e:
                print(f"      ❌ Error parsing {css_file}: {e}")

    def extract_css_rules(self, css_content):
        """Extract CSS rules from content."""
        rules = []

        # Remove comments
        css_content = re.sub(r"/\*.*?\*/", "", css_content, flags=re.DOTALL)

        # Find rule blocks
        rule_pattern = r"([^{}]+)\s*{\s*([^{}]*)\s*}"
        matches = re.findall(rule_pattern, css_content)

        for selector, declarations in matches:
            selector = selector.strip()
            declarations = declarations.strip()

            if selector and declarations:
                # Hash the rule for duplicate detection
                rule_hash = hashlib.md5(
                    f"{selector}:{declarations}".encode()
                ).hexdigest()

                rules.append(
                    {
                        "selector": selector,
                        "declarations": declarations,
                        "hash": rule_hash,
                    }
                )

        return rules

    def find_duplicate_rules(self):
        """Find duplicate CSS rules across files."""
        print("\n2️⃣ Finding duplicate rules...")

        rule_hashes = defaultdict(list)

        for file_path, file_data in self.css_rules.items():
            for rule in file_data["rules"]:
                rule_hashes[rule["hash"]].append(
                    {
                        "file": file_path,
                        "selector": rule["selector"],
                        "declarations": rule["declarations"],
                    }
                )

        # Find duplicates
        for rule_hash, occurrences in rule_hashes.items():
            if len(occurrences) > 1:
                self.duplicate_rules[rule_hash] = occurrences

        print(f"   Found {len(self.duplicate_rules)} duplicate rule patterns")

    def analyze_selector_usage(self):
        """Analyze selector usage patterns."""
        print("\n3️⃣ Analyzing selector usage...")

        # Count selector types
        selector_types = Counter()

        for file_data in self.css_rules.values():
            for rule in file_data["rules"]:
                selector = rule["selector"]

                # Classify selector type
                if selector.startswith("#"):
                    selector_types["id"] += 1
                elif selector.startswith("."):
                    selector_types["class"] += 1
                elif "::" in selector:
                    selector_types["pseudo-element"] += 1
                elif ":" in selector:
                    selector_types["pseudo-class"] += 1
                elif "[" in selector:
                    selector_types["attribute"] += 1
                else:
                    selector_types["element"] += 1

        print(f"   Selector distribution: {dict(selector_types)}")

    def check_file_sizes(self):
        """Analyze CSS file sizes."""
        print("\n4️⃣ Checking file sizes...")

        total_size = 0
        largest_files = []

        for file_path, file_data in self.css_rules.items():
            size_kb = file_data["size"] / 1024
            total_size += file_data["size"]

            largest_files.append(
                {
                    "file": file_path,
                    "size_kb": round(size_kb, 2),
                    "lines": file_data["line_count"],
                    "rules": len(file_data["rules"]),
                }
            )

        # Sort by size
        largest_files.sort(key=lambda x: x["size_kb"], reverse=True)

        print(f"   Total CSS size: {round(total_size / 1024, 2)} KB")
        print(
            f"   Average file size: {round(total_size / len(self.css_files) / 1024, 2)} KB"
        )

        if largest_files:
            print(
                f"   Largest file: {largest_files[0]['file']} ({largest_files[0]['size_kb']} KB)"
            )

    def identify_optimization_opportunities(self):
        """Identify optimization opportunities."""
        print("\n5️⃣ Identifying optimization opportunities...")

        self.optimizations = {
            "merge_candidates": [],
            "unused_selectors": [],
            "redundant_rules": [],
            "size_issues": [],
        }

        # Find files that could be merged
        small_files = [
            file_path
            for file_path, file_data in self.css_rules.items()
            if file_data["size"] < 1024  # Less than 1KB
        ]

        if len(small_files) > 3:
            self.optimizations["merge_candidates"] = small_files

        # Find very large files that might need splitting
        large_files = [
            file_path
            for file_path, file_data in self.css_rules.items()
            if file_data["size"] > 50 * 1024  # More than 50KB
        ]

        if large_files:
            self.optimizations["size_issues"] = large_files

        # Find potentially redundant rules
        if self.duplicate_rules:
            self.optimizations["redundant_rules"] = list(self.duplicate_rules.keys())[
                :10
            ]

    def print_report(self):
        """Print comprehensive CSS audit report."""
        print("\n" + "=" * 60)
        print("📊 CSS AUDIT REPORT")
        print("=" * 60)

        # File overview
        total_size = sum(data["size"] for data in self.css_rules.values())
        total_rules = sum(len(data["rules"]) for data in self.css_rules.values())

        print(f"\n📈 OVERVIEW:")
        print(f"   CSS files found: {len(self.css_files)}")
        print(f"   Total size: {round(total_size / 1024, 2)} KB")
        print(f"   Total rules: {total_rules}")
        print(
            f"   Average rules per file: {round(total_rules / len(self.css_files), 1)}"
        )

        # Duplicate analysis
        if self.duplicate_rules:
            print(f"\n🔄 DUPLICATE RULES:")
            print(f"   Duplicate rule patterns: {len(self.duplicate_rules)}")

            # Show top duplicates
            for i, (rule_hash, occurrences) in enumerate(
                list(self.duplicate_rules.items())[:5]
            ):
                print(f"\n   Duplicate #{i+1}:")
                print(f"      Selector: {occurrences[0]['selector']}")
                print(f"      Found in {len(occurrences)} files:")
                for occ in occurrences:
                    print(f"         - {occ['file']}")

        # File size analysis
        print(f"\n📏 FILE SIZE ANALYSIS:")
        file_sizes = [(path, data["size"]) for path, data in self.css_rules.items()]
        file_sizes.sort(key=lambda x: x[1], reverse=True)

        print("   Largest files:")
        for path, size in file_sizes[:5]:
            print(f"      {path}: {round(size / 1024, 2)} KB")

        # Optimization opportunities
        if hasattr(self, "optimizations"):
            print(f"\n💡 OPTIMIZATION OPPORTUNITIES:")

            if self.optimizations["merge_candidates"]:
                print(
                    f"   Small files to merge ({len(self.optimizations['merge_candidates'])}):"
                )
                for file_path in self.optimizations["merge_candidates"][:5]:
                    size_kb = round(self.css_rules[file_path]["size"] / 1024, 2)
                    print(f"      {file_path}: {size_kb} KB")

            if self.optimizations["size_issues"]:
                print(f"   Large files to consider splitting:")
                for file_path in self.optimizations["size_issues"]:
                    size_kb = round(self.css_rules[file_path]["size"] / 1024, 2)
                    print(f"      {file_path}: {size_kb} KB")

            if self.optimizations["redundant_rules"]:
                print(
                    f"   Redundant rules to review: {len(self.optimizations['redundant_rules'])}"
                )

        # Directory analysis
        print(f"\n📁 DIRECTORY ANALYSIS:")
        css_by_dir = defaultdict(list)
        for css_file in self.css_files:
            rel_path = css_file.relative_to(self.source_dir)
            css_by_dir[str(rel_path.parent)].append(css_file.name)

        for dir_path, files in sorted(css_by_dir.items()):
            if len(files) > 1:
                total_size = sum(
                    self.css_rules.get(f"{dir_path}/{f}", {}).get("size", 0)
                    for f in files
                )
                print(
                    f"   {dir_path}: {len(files)} files, {round(total_size / 1024, 2)} KB"
                )

        # Recommendations
        print(f"\n🎯 RECOMMENDATIONS:")

        if len(self.duplicate_rules) > 10:
            print("   1. 🔄 Consolidate duplicate rules across files")

        if len([f for f in file_sizes if f[1] < 1024]) > 5:
            print("   2. 📦 Merge small CSS files for better performance")

        if any(size > 50 * 1024 for _, size in file_sizes):
            print("   3. 📏 Split large CSS files into logical modules")

        if len(self.css_files) > 20:
            print("   4. 🗂️  Organize CSS files into logical directory structure")

        if total_size > 200 * 1024:
            print("   5. 🗜️  Consider CSS minification and compression")


def main():
    """Run CSS audit."""
    docs_dir = project_root / "docs"

    if not docs_dir.exists():
        print(f"❌ Documentation directory not found: {docs_dir}")
        return 1

    auditor = CSSAuditor(docs_dir)
    auditor.audit_all()

    return 0


if __name__ == "__main__":
    sys.exit(main())
