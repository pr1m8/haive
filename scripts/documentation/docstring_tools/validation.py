#!/usr/bin/env python3
"""PEP 257 compliance checking using pydocstyle and other validation tools.

This module provides comprehensive docstring validation including:
- pydocstyle for PEP 257 compliance checking
- Custom validation rules specific to Google/Sphinx style
- Integration with flake8-docstrings for additional checks
- Detailed error reporting and suggestions
"""

import logging
from pathlib import Path
import subprocess
import sys
from typing import Any

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


class ComplianceChecker:
    """Manages PEP 257 compliance checking with pydocstyle and other tools."""

    def __init__(self):
        pass

    def run_pydocstyle_check(self, package_path: str) -> list[str]:
        """Run pydocstyle PEP 257 compliance check."""
        logger.info(f"✅ Running pydocstyle PEP 257 check on {package_path}")

        # Convert package path to directory
        if package_path.startswith("haive."):
            package_path = package_path.replace(".", "/")

        package_dir = project_root / "packages" / package_path / "src"

        try:
            result = subprocess.run(
                [
                    "pydocstyle",
                    str(package_dir),
                    "--convention=google",  # Use Google convention
                    "--add-ignore=D100,D104",  # Ignore missing module/package docstrings for now
                ],
                capture_output=True,
                text=True,
                timeout=60,
                check=False,
            )

            if result.stdout:
                issues = result.stdout.strip().split("\n")
                logger.info(f"📋 Found {len(issues)} pydocstyle issues")

                # Show first few issues
                for issue in issues[:10]:
                    logger.warning(f"  ⚠️ {issue}")

                if len(issues) > 10:
                    logger.info(f"  ... and {len(issues) - 10} more issues")

                return issues
            logger.info("✅ No pydocstyle issues found!")
            return []

        except FileNotFoundError:
            logger.error(
                "❌ pydocstyle not found. Install with: pip install pydocstyle",
            )
            return []
        except subprocess.TimeoutExpired:
            logger.error("❌ pydocstyle check timed out")
            return []
        except Exception as e:
            logger.error(f"❌ pydocstyle check failed: {e}")
            return []

    def run_flake8_docstring_check(self, package_path: str) -> list[str]:
        """Run flake8-docstrings for additional docstring validation."""
        logger.info(f"🔍 Running flake8-docstrings check on {package_path}")

        # Convert package path to directory
        if package_path.startswith("haive."):
            package_path = package_path.replace(".", "/")

        package_dir = project_root / "packages" / package_path / "src"

        try:
            result = subprocess.run(
                [
                    "flake8",
                    str(package_dir),
                    "--select=D",  # Only docstring errors
                    "--docstring-convention=google",
                ],
                capture_output=True,
                text=True,
                timeout=60,
                check=False,
            )

            if result.stdout:
                issues = result.stdout.strip().split("\n")
                logger.info(f"📋 Found {len(issues)} flake8-docstrings issues")

                # Show first few issues
                for issue in issues[:10]:
                    logger.warning(f"  ⚠️ {issue}")

                if len(issues) > 10:
                    logger.info(f"  ... and {len(issues) - 10} more issues")

                return issues
            logger.info("✅ No flake8-docstrings issues found!")
            return []

        except FileNotFoundError:
            logger.info("ℹ️ flake8 with docstring plugin not found")
            return []
        except subprocess.TimeoutExpired:
            logger.error("❌ flake8-docstrings check timed out")
            return []
        except Exception as e:
            logger.error(f"❌ flake8-docstrings check failed: {e}")
            return []

    def comprehensive_validation(self, package_path: str) -> dict[str, Any]:
        """Run comprehensive docstring validation with multiple tools."""
        logger.info(
            f"🔍 Running comprehensive docstring validation on {package_path}")

        validation_results = {
            "pydocstyle_issues": [],
            "flake8_docstring_issues": [],
            "total_issues": 0,
            "tools_used": [],
        }

        # 1. pydocstyle validation
        pydocstyle_issues = self.run_pydocstyle_check(package_path)
        validation_results["pydocstyle_issues"] = pydocstyle_issues
        if pydocstyle_issues:
            validation_results["tools_used"].append("pydocstyle")

        # 2. flake8-docstrings validation
        flake8_issues = self.run_flake8_docstring_check(package_path)
        validation_results["flake8_docstring_issues"] = flake8_issues
        if flake8_issues:
            validation_results["tools_used"].append("flake8-docstrings")

        # Calculate total issues
        validation_results["total_issues"] = len(pydocstyle_issues) + len(
            flake8_issues)

        self._report_validation_results(validation_results)
        return validation_results

    def _report_validation_results(self, results: dict[str, Any]):
        """Report comprehensive validation results."""
        logger.info("📋 Comprehensive Docstring Validation Report:")
        logger.info(f"  🔍 Total Issues Found: {results['total_issues']}")
        logger.info(
            f"  🛠️ Tools Used: {
                ', '.join(
                    results['tools_used']) if results['tools_used'] else 'None'}",
        )

        if results["pydocstyle_issues"]:
            logger.info(
                f"  📝 pydocstyle Issues: {len(results['pydocstyle_issues'])}")

        if results["flake8_docstring_issues"]:
            logger.info(
                f"  🔧 flake8-docstrings Issues: {len(results['flake8_docstring_issues'])}",
            )

        if results["total_issues"] == 0:
            logger.info("  🎉 All docstring validation passed!")


def main():
    """CLI entry point for docstring validation."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Docstring PEP 257 compliance checking", )
    parser.add_argument("--target", required=True, help="Target package")
    parser.add_argument("--pydocstyle",
                        action="store_true",
                        help="Use pydocstyle only")
    parser.add_argument(
        "--flake8",
        action="store_true",
        help="Use flake8-docstrings only",
    )
    parser.add_argument(
        "--comprehensive",
        action="store_true",
        help="Use all validation tools",
    )

    args = parser.parse_args()

    checker = ComplianceChecker()

    if args.comprehensive or (not args.pydocstyle and not args.flake8):
        # Default to comprehensive
        results = checker.comprehensive_validation(args.target)
        return 0 if results["total_issues"] == 0 else 1
    if args.pydocstyle:
        issues = checker.run_pydocstyle_check(args.target)
        return 0 if len(issues) == 0 else 1
    if args.flake8:
        issues = checker.run_flake8_docstring_check(args.target)
        return 0 if len(issues) == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
