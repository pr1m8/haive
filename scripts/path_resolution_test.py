#!/usr/bin/env python3
"""
Path Resolution Test Suite
Tests for broken links, circular references, and path resolution issues.
"""

import os
import re
import sys
import time
from collections import defaultdict
from pathlib import Path
from urllib.parse import urljoin, urlparse

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class PathResolutionTester:
    """Test path resolution and link validity in documentation."""

    def __init__(self, docs_dir: Path):
        self.docs_dir = docs_dir
        self.source_dir = docs_dir / "source"
        self.build_dir = docs_dir / "build" / "html"

        self.broken_links = []
        self.circular_refs = []
        self.deep_paths = []
        self.api_path_issues = []

    def test_all(self):
        """Run all path resolution tests."""
        print("🔗 Path Resolution Test Suite\n")

        self.test_rst_references()
        self.test_toctree_links()
        self.test_autoapi_paths()
        self.test_static_file_links()
        self.test_cross_references()
        self.test_path_depth()

        if self.build_dir.exists():
            self.test_html_links()
        else:
            print("⚠️  Build directory not found, skipping HTML link tests")

        self.print_report()

    def test_rst_references(self):
        """Test 1: RST Reference Resolution"""
        print("1️⃣ Testing RST references...")

        rst_files = list(self.source_dir.rglob("*.rst"))
        reference_patterns = [
            (r":doc:`([^`]+)`", "doc"),
            (r":ref:`([^`]+)`", "ref"),
            (r"`([^`]+) <([^>]+)>`_", "external"),
            (r"\.\. _([^:]+):", "label"),
            (r"\.\. include:: ([^\n]+)", "include"),
        ]

        for rst_file in rst_files:
            try:
                with open(rst_file, "r", encoding="utf-8") as f:
                    content = f.read()

                for pattern, ref_type in reference_patterns:
                    matches = re.findall(pattern, content)

                    for match in matches:
                        if isinstance(match, tuple):
                            ref_target = (
                                match[1] if ref_type == "external" else match[0]
                            )
                        else:
                            ref_target = match

                        # Check if reference target exists
                        if ref_type == "doc":
                            target_path = self.resolve_doc_reference(
                                rst_file, ref_target
                            )
                            if not target_path or not target_path.exists():
                                self.broken_links.append(
                                    {
                                        "file": str(
                                            rst_file.relative_to(self.source_dir)
                                        ),
                                        "type": "doc_reference",
                                        "target": ref_target,
                                        "resolved_path": (
                                            str(target_path) if target_path else None
                                        ),
                                    }
                                )

                        elif ref_type == "include":
                            include_path = self.resolve_include_path(
                                rst_file, ref_target
                            )
                            if not include_path or not include_path.exists():
                                self.broken_links.append(
                                    {
                                        "file": str(
                                            rst_file.relative_to(self.source_dir)
                                        ),
                                        "type": "include",
                                        "target": ref_target,
                                        "resolved_path": (
                                            str(include_path) if include_path else None
                                        ),
                                    }
                                )

            except Exception as e:
                print(f"      ❌ Error processing {rst_file}: {e}")

    def resolve_doc_reference(self, source_file, ref_target):
        """Resolve a :doc: reference to actual file path."""
        # Remove .rst extension if present
        ref_target = ref_target.replace(".rst", "")

        # Handle relative paths
        if ref_target.startswith("/"):
            # Absolute from source root
            target_path = self.source_dir / ref_target.lstrip("/") + ".rst"
        else:
            # Relative to current file
            current_dir = source_file.parent
            target_path = current_dir / ref_target + ".rst"

        return target_path.resolve() if target_path else None

    def resolve_include_path(self, source_file, include_target):
        """Resolve an .. include:: path."""
        current_dir = source_file.parent
        include_path = current_dir / include_target
        return include_path.resolve() if include_path else None

    def test_toctree_links(self):
        """Test 2: TOC Tree Link Resolution"""
        print("\n2️⃣ Testing toctree links...")

        rst_files = list(self.source_dir.rglob("*.rst"))
        toctree_pattern = r"\.\. toctree::\s*\n\s*:.*?\n\n((?:\s+[^\n]+\n)*)"

        for rst_file in rst_files:
            try:
                with open(rst_file, "r", encoding="utf-8") as f:
                    content = f.read()

                toctree_matches = re.findall(toctree_pattern, content, re.MULTILINE)

                for toctree_content in toctree_matches:
                    # Extract individual entries
                    entries = [
                        line.strip()
                        for line in toctree_content.split("\n")
                        if line.strip()
                    ]

                    for entry in entries:
                        # Skip comments and options
                        if entry.startswith(":") or entry.startswith("#"):
                            continue

                        # Resolve the toctree entry
                        target_path = self.resolve_doc_reference(rst_file, entry)
                        if not target_path or not target_path.exists():
                            self.broken_links.append(
                                {
                                    "file": str(rst_file.relative_to(self.source_dir)),
                                    "type": "toctree",
                                    "target": entry,
                                    "resolved_path": (
                                        str(target_path) if target_path else None
                                    ),
                                }
                            )

            except Exception as e:
                print(f"      ❌ Error processing toctree in {rst_file}: {e}")

    def test_autoapi_paths(self):
        """Test 3: AutoAPI Path Resolution"""
        print("\n3️⃣ Testing AutoAPI paths...")

        # Check conf.py for autoapi configuration
        conf_files = list(self.source_dir.glob("conf*.py"))

        for conf_file in conf_files:
            try:
                with open(conf_file, "r") as f:
                    content = f.read()

                # Find autoapi_dirs configuration
                autoapi_match = re.search(
                    r"autoapi_dirs\s*=\s*\[(.*?)\]", content, re.DOTALL
                )
                if autoapi_match:
                    dirs_content = autoapi_match.group(1)

                    # Extract directory paths
                    dir_matches = re.findall(r'["\']([^"\']+)["\']', dirs_content)

                    for api_dir in dir_matches:
                        # Resolve relative to project root
                        if api_dir.startswith("../"):
                            resolved_dir = (self.source_dir / api_dir).resolve()
                        else:
                            resolved_dir = Path(api_dir).resolve()

                        if not resolved_dir.exists():
                            self.api_path_issues.append(
                                {
                                    "conf_file": conf_file.name,
                                    "api_dir": api_dir,
                                    "resolved_path": str(resolved_dir),
                                    "issue": "directory_not_found",
                                }
                            )
                        else:
                            # Check for common path issues
                            if "/src/haive/" in str(resolved_dir):
                                self.api_path_issues.append(
                                    {
                                        "conf_file": conf_file.name,
                                        "api_dir": api_dir,
                                        "resolved_path": str(resolved_dir),
                                        "issue": "src_path_pattern",
                                    }
                                )

                            # Check for nested package patterns
                            if resolved_dir.name == "haive" and "packages" in str(
                                resolved_dir
                            ):
                                parent_haive = resolved_dir.parent
                                if parent_haive.name.startswith("haive-"):
                                    self.api_path_issues.append(
                                        {
                                            "conf_file": conf_file.name,
                                            "api_dir": api_dir,
                                            "resolved_path": str(resolved_dir),
                                            "issue": "nested_package_pattern",
                                        }
                                    )

            except Exception as e:
                print(f"      ❌ Error analyzing AutoAPI in {conf_file}: {e}")

    def test_static_file_links(self):
        """Test 4: Static File Link Resolution"""
        print("\n4️⃣ Testing static file links...")

        static_dirs = [
            self.source_dir / "_static",
            self.source_dir / "_templates",
        ]

        rst_files = list(self.source_dir.rglob("*.rst"))
        static_patterns = [
            (r"\.\. image:: ([^\n]+)", "image"),
            (r"\.\. figure:: ([^\n]+)", "figure"),
            (r":download:`[^`]+<([^>]+)>`", "download"),
        ]

        for rst_file in rst_files:
            try:
                with open(rst_file, "r", encoding="utf-8") as f:
                    content = f.read()

                for pattern, link_type in static_patterns:
                    matches = re.findall(pattern, content)

                    for static_ref in matches:
                        static_ref = static_ref.strip()

                        # Resolve static file path
                        if static_ref.startswith("_static/"):
                            target_path = self.source_dir / static_ref
                        elif static_ref.startswith("/"):
                            target_path = self.source_dir / static_ref.lstrip("/")
                        else:
                            target_path = rst_file.parent / static_ref

                        if not target_path.exists():
                            self.broken_links.append(
                                {
                                    "file": str(rst_file.relative_to(self.source_dir)),
                                    "type": f"static_{link_type}",
                                    "target": static_ref,
                                    "resolved_path": str(target_path),
                                }
                            )

            except Exception as e:
                print(f"      ❌ Error processing static links in {rst_file}: {e}")

    def test_cross_references(self):
        """Test 5: Cross-reference Resolution"""
        print("\n5️⃣ Testing cross-references...")

        # Collect all labels
        all_labels = set()
        rst_files = list(self.source_dir.rglob("*.rst"))

        for rst_file in rst_files:
            try:
                with open(rst_file, "r", encoding="utf-8") as f:
                    content = f.read()

                # Find labels
                label_matches = re.findall(r"\.\. _([^:]+):", content)
                all_labels.update(label_matches)

            except Exception as e:
                continue

        # Check references to labels
        for rst_file in rst_files:
            try:
                with open(rst_file, "r", encoding="utf-8") as f:
                    content = f.read()

                # Find references
                ref_matches = re.findall(r":ref:`([^`]+)`", content)

                for ref in ref_matches:
                    if ref not in all_labels:
                        self.broken_links.append(
                            {
                                "file": str(rst_file.relative_to(self.source_dir)),
                                "type": "cross_reference",
                                "target": ref,
                                "issue": "label_not_found",
                            }
                        )

            except Exception as e:
                continue

    def test_path_depth(self):
        """Test 6: Path Depth Analysis"""
        print("\n6️⃣ Testing path depth...")

        for path in self.source_dir.rglob("*"):
            if path.is_file():
                rel_path = path.relative_to(self.source_dir)
                depth = len(rel_path.parts)

                if depth > 6:
                    self.deep_paths.append(
                        {"path": str(rel_path), "depth": depth, "type": path.suffix}
                    )

    def test_html_links(self):
        """Test 7: HTML Link Validation (if build exists)"""
        print("\n7️⃣ Testing HTML links...")

        html_files = list(self.build_dir.rglob("*.html"))
        link_pattern = r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>'

        for html_file in html_files[:10]:  # Limit to first 10 for performance
            try:
                with open(html_file, "r", encoding="utf-8") as f:
                    content = f.read()

                links = re.findall(link_pattern, content)

                for link in links:
                    # Skip external links
                    if link.startswith(("http://", "https://", "mailto:", "#")):
                        continue

                    # Resolve relative link
                    if link.startswith("/"):
                        target_path = self.build_dir / link.lstrip("/")
                    else:
                        target_path = html_file.parent / link

                    # Remove fragments
                    if "#" in str(target_path):
                        target_path = Path(str(target_path).split("#")[0])

                    if not target_path.exists():
                        self.broken_links.append(
                            {
                                "file": str(html_file.relative_to(self.build_dir)),
                                "type": "html_link",
                                "target": link,
                                "resolved_path": str(target_path),
                            }
                        )

            except Exception as e:
                continue

    def print_report(self):
        """Print comprehensive path resolution report."""
        print("\n" + "=" * 60)
        print("📊 PATH RESOLUTION TEST REPORT")
        print("=" * 60)

        # Summary statistics
        total_issues = (
            len(self.broken_links)
            + len(self.circular_refs)
            + len(self.deep_paths)
            + len(self.api_path_issues)
        )

        print(f"\n📈 SUMMARY:")
        print(f"   Total path issues found: {total_issues}")
        print(f"   Broken links: {len(self.broken_links)}")
        print(f"   API path issues: {len(self.api_path_issues)}")
        print(f"   Deep paths (>6 levels): {len(self.deep_paths)}")

        # Broken links analysis
        if self.broken_links:
            print(f"\n🔗 BROKEN LINKS ({len(self.broken_links)}):")

            # Group by type
            by_type = defaultdict(list)
            for link in self.broken_links:
                by_type[link["type"]].append(link)

            for link_type, links in by_type.items():
                print(f"\n   {link_type} ({len(links)}):")
                for link in links[:5]:  # Show first 5
                    print(f"      📄 {link['file']}")
                    print(f"         Target: {link['target']}")
                    if "resolved_path" in link:
                        print(f"         Resolved: {link['resolved_path']}")
                if len(links) > 5:
                    print(f"      ... and {len(links) - 5} more")

        # API path issues
        if self.api_path_issues:
            print(f"\n🔧 API PATH ISSUES ({len(self.api_path_issues)}):")

            by_issue = defaultdict(list)
            for issue in self.api_path_issues:
                by_issue[issue["issue"]].append(issue)

            for issue_type, issues in by_issue.items():
                print(f"\n   {issue_type} ({len(issues)}):")
                for issue in issues:
                    print(f"      📄 {issue['conf_file']}: {issue['api_dir']}")

        # Deep path analysis
        if self.deep_paths:
            print(f"\n📏 DEEP PATHS ({len(self.deep_paths)}):")

            # Sort by depth
            sorted_paths = sorted(
                self.deep_paths, key=lambda x: x["depth"], reverse=True
            )

            for path_info in sorted_paths[:10]:  # Show top 10
                print(f"      {path_info['path']} (depth: {path_info['depth']})")

        # Recommendations
        print(f"\n💡 RECOMMENDATIONS:")

        if any(issue["issue"] == "src_path_pattern" for issue in self.api_path_issues):
            print("   1. 🔧 Fix AutoAPI paths to avoid '/src/haive/' pattern")

        if len(self.deep_paths) > 10:
            print("   2. 📁 Flatten directory structure to reduce path depth")

        if any(link["type"] == "doc_reference" for link in self.broken_links):
            print("   3. 📝 Fix broken document references in RST files")

        if any(link["type"] == "toctree" for link in self.broken_links):
            print("   4. 🌲 Update toctree entries to point to existing files")

        if len(self.broken_links) > 20:
            print("   5. 🔍 Run comprehensive link validation before builds")

        # Test execution summary
        print(f"\n⏱️  TEST EXECUTION:")
        print(f"   RST files analyzed: {len(list(self.source_dir.rglob('*.rst')))}")
        print(
            f"   Configuration files checked: {len(list(self.source_dir.glob('conf*.py')))}"
        )
        if self.build_dir.exists():
            print(
                f"   HTML files tested: {min(10, len(list(self.build_dir.rglob('*.html'))))}"
            )


def main():
    """Run path resolution tests."""
    docs_dir = project_root / "docs"

    if not docs_dir.exists():
        print(f"❌ Documentation directory not found: {docs_dir}")
        return 1

    tester = PathResolutionTester(docs_dir)
    tester.test_all()

    return 0


if __name__ == "__main__":
    sys.exit(main())
