#!/usr/bin/env python3
"""Documentation quality analysis using Vale and other prose linting tools.

This module provides comprehensive documentation quality checking including:
- Vale prose linting for documentation files
- Markdown quality checking
- Documentation link validation
- Writing style consistency analysis
"""

from __future__ import annotations

import logging
import subprocess
import sys
from pathlib import Path
from typing import Any

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


class QualityChecker:
    """Manages documentation quality checking with Vale and other tools."""

    def __init__(self):
        pass

    def run_vale_check(self, package_path: str) -> bool:
        """Run Vale prose linting on documentation."""
        logger.info(f"📖 Running Vale prose linting on {package_path}")

        # Look for documentation files
        doc_patterns = ["*.md", "*.rst", "*.txt"]
        package_dir = project_root / "packages" / package_path.replace("-", "_")

        doc_files = []
        for pattern in doc_patterns:
            doc_files.extend(package_dir.rglob(pattern))

        if not doc_files:
            logger.info("ℹ️ No documentation files found for Vale analysis")
            return True

        try:
            result = subprocess.run(
                [
                    "vale",
                    "--config",
                    str(project_root / ".vale.ini"),
                    *[str(f) for f in doc_files[:10]],  # Limit to first 10 files
                ],
                capture_output=True,
                text=True,
                timeout=60,
                check=False,
            )

            if result.stdout:
                logger.info("📖 Vale prose analysis:")
                print(result.stdout)
            else:
                logger.info("✅ No Vale issues found!")

            return True

        except FileNotFoundError:
            logger.info("ℹ️ Vale not found. Install from: https://vale.sh/")
            return False
        except Exception as e:
            logger.error(f"❌ Vale check failed: {e}")
            return False

    def run_markdown_quality_check(self, package_path: str) -> list[str]:
        """Check markdown files for quality issues."""
        logger.info(f"📝 Running markdown quality check on {package_path}")

        package_dir = project_root / "packages" / package_path.replace("-", "_")
        md_files = list(package_dir.rglob("*.md"))

        if not md_files:
            logger.info("ℹ️ No markdown files found")
            return []

        issues = []

        # Basic markdown quality checks
        for md_file in md_files:
            try:
                with open(md_file, encoding="utf-8") as f:
                    content = f.read()

                # Check for common issues
                lines = content.split("\n")
                for i, line in enumerate(lines, 1):
                    # Check for missing spaces after hash headers
                    if line.startswith("#") and not line.startswith("# "):
                        issues.append(f"{md_file}:{i}: Missing space after # in header")

                    # Check for trailing whitespace
                    if line.endswith(" "):
                        issues.append(f"{md_file}:{i}: Trailing whitespace")

                    # Check for very long lines (> 120 chars)
                    if len(line) > 120:
                        issues.append(
                            f"{md_file}:{i}: Line too long ({len(line)} chars)",
                        )

            except Exception as e:
                logger.error(f"❌ Failed to check {md_file}: {e}")

        if issues:
            logger.info(f"📋 Found {len(issues)} markdown quality issues")
            for issue in issues[:10]:
                logger.warning(f"  ⚠️ {issue}")
            if len(issues) > 10:
                logger.info(f"  ... and {len(issues) - 10} more issues")
        else:
            logger.info("✅ No markdown quality issues found!")

        return issues

    def run_link_validation(self, package_path: str) -> list[str]:
        """Validate links in documentation files."""
        logger.info(f"🔗 Running link validation on {package_path}")

        package_dir = project_root / "packages" / package_path.replace("-", "_")
        doc_files = []

        # Find documentation files
        for pattern in ["*.md", "*.rst"]:
            doc_files.extend(package_dir.rglob(pattern))

        if not doc_files:
            logger.info("ℹ️ No documentation files found for link validation")
            return []

        broken_links = []

        # Simple link validation (could be enhanced with actual HTTP checking)
        import re

        link_pattern = re.compile(r"\[([^\]]*)\]\(([^)]*)\)")

        for doc_file in doc_files:
            try:
                with open(doc_file, encoding="utf-8") as f:
                    content = f.read()

                lines = content.split("\n")
                for i, line in enumerate(lines, 1):
                    matches = link_pattern.findall(line)
                    for text, url in matches:
                        # Check for obviously broken links
                        if not url or url.startswith("TODO") or url == "#":
                            broken_links.append(
                                f"{doc_file}:{i}: Broken link '{text}' -> '{url}'",
                            )

                        # Check for relative links to missing files
                        if not url.startswith(("http", "https", "mailto", "#")):
                            link_file = doc_file.parent / url
                            if not link_file.exists():
                                broken_links.append(
                                    f"{doc_file}:{i}: Missing file '{url}' linked as '{text}'",
                                )

            except Exception as e:
                logger.error(f"❌ Failed to validate links in {doc_file}: {e}")

        if broken_links:
            logger.info(f"📋 Found {len(broken_links)} broken links")
            for link in broken_links[:10]:
                logger.warning(f"  ⚠️ {link}")
            if len(broken_links) > 10:
                logger.info(f"  ... and {len(broken_links) - 10} more broken links")
        else:
            logger.info("✅ No broken links found!")

        return broken_links

    def comprehensive_quality_check(self, package_path: str) -> dict[str, Any]:
        """Run comprehensive documentation quality check."""
        logger.info(
            f"🔍 Running comprehensive documentation quality check on {package_path}",
        )

        quality_results = {
            "vale_passed": False,
            "markdown_issues": [],
            "broken_links": [],
            "total_issues": 0,
            "tools_used": [],
        }

        # 1. Vale prose linting
        vale_result = self.run_vale_check(package_path)
        quality_results["vale_passed"] = vale_result
        if vale_result:
            quality_results["tools_used"].append("vale")

        # 2. Markdown quality check
        markdown_issues = self.run_markdown_quality_check(package_path)
        quality_results["markdown_issues"] = markdown_issues
        if markdown_issues:
            quality_results["tools_used"].append("markdown-quality")

        # 3. Link validation
        broken_links = self.run_link_validation(package_path)
        quality_results["broken_links"] = broken_links
        if broken_links:
            quality_results["tools_used"].append("link-validation")

        # Calculate total issues
        quality_results["total_issues"] = len(markdown_issues) + len(broken_links)

        self._report_quality_results(quality_results)
        return quality_results

    def _report_quality_results(self, results: dict[str, Any]):
        """Report comprehensive quality check results."""
        logger.info("📖 Comprehensive Documentation Quality Report:")
        logger.info(f"  🔍 Total Issues Found: {results['total_issues']}")
        logger.info(
            f"  🛠️ Tools Used: {
                ', '.join(results['tools_used']) if results['tools_used'] else 'None'
            }",
        )

        if results["vale_passed"]:
            logger.info("  📖 Vale: Passed")
        else:
            logger.info("  📖 Vale: Not available or failed")

        if results["markdown_issues"]:
            logger.info(
                f"  📝 Markdown Quality Issues: {len(results['markdown_issues'])}",
            )

        if results["broken_links"]:
            logger.info(f"  🔗 Broken Links: {len(results['broken_links'])}")

        if results["total_issues"] == 0 and results["vale_passed"]:
            logger.info("  🎉 All documentation quality checks passed!")


def main():
    """CLI entry point for documentation quality checking."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Documentation quality checking with Vale and other tools",
    )
    parser.add_argument("--target", required=True, help="Target package")
    parser.add_argument("--vale", action="store_true", help="Use Vale only")
    parser.add_argument(
        "--markdown",
        action="store_true",
        help="Check markdown quality only",
    )
    parser.add_argument("--links", action="store_true", help="Validate links only")
    parser.add_argument(
        "--comprehensive",
        action="store_true",
        help="Use all quality checks",
    )

    args = parser.parse_args()

    checker = QualityChecker()

    if args.comprehensive or (not args.vale and not args.markdown and not args.links):
        # Default to comprehensive
        results = checker.comprehensive_quality_check(args.target)
        return 0 if results["total_issues"] == 0 and results["vale_passed"] else 1
    if args.vale:
        passed = checker.run_vale_check(args.target)
        return 0 if passed else 1
    if args.markdown:
        issues = checker.run_markdown_quality_check(args.target)
        return 0 if len(issues) == 0 else 1
    if args.links:
        broken_links = checker.run_link_validation(args.target)
        return 0 if len(broken_links) == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
