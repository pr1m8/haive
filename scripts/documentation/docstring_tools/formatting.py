#!/usr/bin/env python3
"""Docstring formatting using docformatter and other formatting tools.

This module provides comprehensive docstring formatting including:
- Docformatter for PEP 257 compliant formatting
- Automatic line wrapping and spacing
- Consistent formatting across the codebase
- Dry-run validation before applying changes
"""

from __future__ import annotations

import logging
import subprocess
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


class DocstringFormatter:
    """Manages docstring formatting with docformatter and other tools."""

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run

    def format_with_docformatter(self, package_path: str) -> bool:
        """Format docstrings using docformatter."""
        logger.info(f"🔧 Running docformatter on {package_path}")

        # Convert package path to directory
        if package_path.startswith("haive."):
            package_path = package_path.replace(".", "/")

        package_dir = project_root / "packages" / package_path / "src"

        try:
            # Build docformatter command
            cmd = [
                "docformatter",
                "--recursive",
                "--wrap-summaries",
                "88",
                "--wrap-descriptions",
                "88",
                "--make-summary-multi-line",
                "--force-wrap",
                "--pre-summary-newline",
            ]

            if self.dry_run:
                cmd.append("--diff")  # Show changes without applying
            else:
                cmd.extend(["--in-place"])  # Apply changes

            cmd.append(str(package_dir))

            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=120, check=False
            )

            if result.stdout:
                if self.dry_run:
                    logger.info("🧪 Docformatter changes preview:")
                    print(result.stdout)
                else:
                    logger.info("✅ Docformatter applied successfully")

                return True
            logger.info("ℹ️ No formatting changes needed")
            return True

        except FileNotFoundError:
            logger.error(
                "❌ docformatter not found. Install with: pip install docformatter",
            )
            return False
        except subprocess.TimeoutExpired:
            logger.error("❌ docformatter timed out")
            return False
        except Exception as e:
            logger.error(f"❌ docformatter failed: {e}")
            return False


def main():
    """CLI entry point for docstring formatting."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Docstring formatting with docformatter",
    )
    parser.add_argument("--target", required=True, help="Target package")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show changes without applying",
    )

    args = parser.parse_args()

    formatter = DocstringFormatter(dry_run=args.dry_run)
    success = formatter.format_with_docformatter(args.target)

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
