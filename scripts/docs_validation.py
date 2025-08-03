#!/usr/bin/env python3
"""
Documentation Structure Validation Tests
Tests for identifying and validating documentation structure issues.
"""

import importlib.util
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class DocumentationValidator:
    """Validate documentation structure and configuration."""

    def __init__(self, docs_dir: Path):
        self.docs_dir = docs_dir
        self.source_dir = docs_dir / "source"
        self.issues = defaultdict(list)

    def validate_all(self):
        """Run all validation tests."""
        print("🔍 Documentation Structure Validation\n")

        self.validate_conf_files()
        self.validate_css_structure()
        self.validate_path_structure()
        self.validate_generated_content()
        self.validate_backup_files()

        self.print_report()

    def validate_conf_files(self):
        """Test 1: Configuration File Validation"""
        print("1️⃣ Validating Configuration Files...")

        conf_files = list(self.source_dir.glob("conf*.py"))
        print(f"   Found {len(conf_files)} conf files")

        # Check for duplicate settings across conf files
        all_settings = {}

        for conf_file in conf_files:
            if conf_file.name == "conftest.py":
                continue

            try:
                # Parse conf file for key settings
                with open(conf_file, "r") as f:
                    content = f.read()

                # Extract key settings using regex
                settings = {
                    "project": re.search(r'project\s*=\s*["\']([^"\']+)', content),
                    "extensions": re.findall(
                        r"extensions\s*=\s*\[(.*?)\]", content, re.DOTALL
                    ),
                    "html_theme": re.search(
                        r'html_theme\s*=\s*["\']([^"\']+)', content
                    ),
                    "autoapi_dirs": re.search(
                        r"autoapi_dirs\s*=\s*\[(.*?)\]", content, re.DOTALL
                    ),
                }

                # Check for conflicts
                for key, match in settings.items():
                    if match:
                        value = (
                            match.group(1) if hasattr(match, "group") else str(match)
                        )
                        if key in all_settings and all_settings[key] != value:
                            self.issues["conf_conflicts"].append(
                                {
                                    "file": conf_file.name,
                                    "setting": key,
                                    "value": value,
                                    "conflicts_with": all_settings[key],
                                }
                            )
                        all_settings[key] = value

            except Exception as e:
                self.issues["conf_errors"].append(
                    {"file": conf_file.name, "error": str(e)}
                )

        # Check which conf file is actually used
        main_conf = self.source_dir / "conf.py"
        if main_conf.exists():
            print(f"   ✓ Main conf.py exists")
        else:
            self.issues["conf_missing"].append("No main conf.py file found")

    def validate_css_structure(self):
        """Test 2: CSS Structure Validation"""
        print("\n2️⃣ Validating CSS Structure...")

        # Find all CSS files
        css_files = list(self.source_dir.rglob("*.css"))
        print(f"   Found {len(css_files)} CSS files")

        # Group by directory
        css_by_dir = defaultdict(list)
        for css_file in css_files:
            rel_path = css_file.relative_to(self.source_dir)
            css_by_dir[str(rel_path.parent)].append(css_file.name)

        # Check for duplicates and backups
        for dir_path, files in css_by_dir.items():
            if len(files) > 5:  # Arbitrary threshold
                self.issues["css_fragmentation"].append(
                    {
                        "directory": dir_path,
                        "file_count": len(files),
                        "files": files[:10],  # Show first 10
                    }
                )

            # Check for backup patterns
            backup_patterns = [".backup", ".old", ".bak", "_backup", "_old"]
            backups = [f for f in files if any(pat in f for pat in backup_patterns)]
            if backups:
                self.issues["css_backups"].append(
                    {"directory": dir_path, "backup_files": backups}
                )

    def validate_path_structure(self):
        """Test 3: Path Structure Validation"""
        print("\n3️⃣ Validating Path Structure...")

        # Check for excessive nesting
        for path in self.source_dir.rglob("*"):
            if path.is_file():
                rel_path = path.relative_to(self.source_dir)
                depth = len(rel_path.parts)

                if depth > 6:  # Flag paths deeper than 6 levels
                    self.issues["deep_nesting"].append(
                        {"path": str(rel_path), "depth": depth}
                    )

        # Check for path patterns that indicate problems
        problem_patterns = [
            ("multiple_api_dirs", "api/api/"),
            ("src_in_docs", "/src/haive/"),
            ("package_duplication", "packages/haive-"),
        ]

        for issue_type, pattern in problem_patterns:
            matching_paths = [
                str(p.relative_to(self.source_dir))
                for p in self.source_dir.rglob("*")
                if pattern in str(p)
            ]
            if matching_paths:
                self.issues[issue_type].append(
                    {
                        "pattern": pattern,
                        "count": len(matching_paths),
                        "examples": matching_paths[:5],
                    }
                )

    def validate_generated_content(self):
        """Test 4: Generated Content Validation"""
        print("\n4️⃣ Validating Generated Content...")

        # Check for generated files in source
        generated_patterns = [
            ("zip_files", "*.zip"),
            ("autoapi_files", "autoapi/**/*.rst"),
            ("autosummary_files", "_autosummary/**/*.rst"),
            ("build_artifacts", "_build/**/*"),
        ]

        for issue_type, pattern in generated_patterns:
            matching_files = list(self.source_dir.rglob(pattern))
            if matching_files:
                self.issues[f"generated_{issue_type}"].append(
                    {
                        "pattern": pattern,
                        "count": len(matching_files),
                        "size_mb": sum(
                            f.stat().st_size for f in matching_files if f.is_file()
                        )
                        / (1024 * 1024),
                        "examples": [
                            str(f.relative_to(self.source_dir))
                            for f in matching_files[:5]
                        ],
                    }
                )

    def validate_backup_files(self):
        """Test 5: Backup File Validation"""
        print("\n5️⃣ Validating Backup Files...")

        backup_patterns = ["*.backup", "*.bak", "*_backup.*", "*_old.*", "*.old"]
        backup_files = []

        for pattern in backup_patterns:
            backup_files.extend(self.source_dir.rglob(pattern))

        if backup_files:
            # Group by type
            backup_by_type = defaultdict(list)
            for backup in backup_files:
                ext = backup.suffix
                backup_by_type[ext].append(str(backup.relative_to(self.source_dir)))

            self.issues["backup_files"].append(
                {
                    "total_count": len(backup_files),
                    "by_type": dict(backup_by_type),
                    "size_mb": sum(
                        f.stat().st_size for f in backup_files if f.is_file()
                    )
                    / (1024 * 1024),
                }
            )

    def print_report(self):
        """Print validation report."""
        print("\n" + "=" * 60)
        print("📊 VALIDATION REPORT")
        print("=" * 60)

        if not self.issues:
            print("✅ No issues found!")
            return

        # Group issues by severity
        critical_issues = ["conf_conflicts", "conf_missing", "multiple_api_dirs"]
        warning_issues = ["deep_nesting", "css_fragmentation", "generated_zip_files"]
        info_issues = ["backup_files", "css_backups"]

        # Print critical issues
        critical_found = [k for k in critical_issues if k in self.issues]
        if critical_found:
            print("\n🚨 CRITICAL ISSUES:")
            for issue_type in critical_found:
                print(f"\n   {issue_type}:")
                for issue in self.issues[issue_type]:
                    print(f"      {json.dumps(issue, indent=6)}")

        # Print warnings
        warning_found = [k for k in warning_issues if k in self.issues]
        if warning_found:
            print("\n⚠️  WARNINGS:")
            for issue_type in warning_found:
                print(f"\n   {issue_type}:")
                issues = self.issues[issue_type]
                if isinstance(issues, list) and issues:
                    if isinstance(issues[0], dict):
                        for issue in issues[:3]:  # Show first 3
                            print(f"      {json.dumps(issue, indent=6)}")
                        if len(issues) > 3:
                            print(f"      ... and {len(issues) - 3} more")

        # Print info
        info_found = [k for k in info_issues if k in self.issues]
        if info_found:
            print("\n📝 INFO:")
            for issue_type in info_found:
                print(f"\n   {issue_type}:")
                issues = self.issues[issue_type]
                if isinstance(issues, list) and len(issues) > 0:
                    print(f"      {json.dumps(issues[0], indent=6)}")

        # Summary
        print("\n📈 SUMMARY:")
        print(f"   Total issue types: {len(self.issues)}")
        print(f"   Critical issues: {len(critical_found)}")
        print(f"   Warnings: {len(warning_found)}")
        print(f"   Info items: {len(info_found)}")

        # Recommendations
        print("\n💡 RECOMMENDATIONS:")
        if "conf_conflicts" in self.issues:
            print("   1. Consolidate configuration files into a single conf.py")
        if "css_fragmentation" in self.issues:
            print("   2. Merge CSS files and remove duplicates")
        if "deep_nesting" in self.issues:
            print("   3. Flatten directory structure for better navigation")
        if "generated_zip_files" in self.issues:
            print("   4. Clean up generated content from source directory")
        if "backup_files" in self.issues:
            print("   5. Remove or archive old backup files")


def main():
    """Run documentation validation."""
    docs_dir = project_root / "docs"

    if not docs_dir.exists():
        print(f"❌ Documentation directory not found: {docs_dir}")
        return 1

    validator = DocumentationValidator(docs_dir)
    validator.validate_all()

    return 0


if __name__ == "__main__":
    sys.exit(main())
