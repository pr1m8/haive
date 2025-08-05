#!/usr/bin/env python3
"""Docstring coverage analysis using AST parsing and interrogate integration.

This module provides comprehensive docstring coverage analysis including:
- AST-based parsing to find missing docstrings
- Integration with interrogate for professional coverage reports
- Docstr-coverage for alternative coverage analysis
- Detailed reporting by file, function, class, and module
"""

from __future__ import annotations

import ast
import logging
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


@dataclass
class DocstringTarget:
    """Represents a target for docstring analysis/generation."""

    file_path: Path
    function_name: str = ""
    class_name: str = ""
    line_number: int = 0
    current_docstring: str = ""
    missing_docstring: bool = False
    docstring_issues: list[str] = field(default_factory=list)
    target_type: str = "function"  # function, method, class, module


@dataclass
class CoverageReport:
    """Docstring coverage analysis report."""

    total_functions: int = 0
    documented_functions: int = 0
    total_classes: int = 0
    documented_classes: int = 0
    total_modules: int = 0
    documented_modules: int = 0
    missing_targets: list[DocstringTarget] = field(default_factory=list)
    coverage_percentage: float = 0.0
    interrogate_score: float = 0.0
    docstr_coverage_score: float = 0.0


class CoverageAnalyzer(ast.NodeVisitor):
    """AST visitor to analyze docstring coverage and quality."""

    def __init__(self):
        self.targets_needing_docs: list[DocstringTarget] = []
        self.current_class = None
        self.file_path = None
        self.stats = {
            "functions": 0,
            "documented_functions": 0,
            "classes": 0,
            "documented_classes": 0,
            "methods": 0,
            "documented_methods": 0,
        }

    def analyze_file(self, file_path: Path) -> list[DocstringTarget]:
        """Analyze a Python file for docstring coverage."""
        self.file_path = file_path
        self.targets_needing_docs.clear()
        self.current_class = None

        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            tree = ast.parse(content)
            self.visit(tree)

            # Check module-level docstring
            module_docstring = ast.get_docstring(tree)
            if not module_docstring:
                self.targets_needing_docs.append(
                    DocstringTarget(
                        file_path=file_path,
                        line_number=1,
                        missing_docstring=True,
                        target_type="module",
                    ),
                )

            return self.targets_needing_docs

        except Exception as e:
            logger.error(f"❌ Failed to analyze {file_path}: {e}")
            return []

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Visit function definitions."""
        is_method = self.current_class is not None
        docstring = ast.get_docstring(node)

        # Skip private functions unless they're special methods
        if node.name.startswith("_") and not node.name.startswith("__"):
            self.generic_visit(node)
            return

        if is_method:
            self.stats["methods"] += 1
            if docstring:
                self.stats["documented_methods"] += 1
        else:
            self.stats["functions"] += 1
            if docstring:
                self.stats["documented_functions"] += 1

        if not docstring:
            target = DocstringTarget(
                file_path=self.file_path,
                function_name=node.name,
                class_name=self.current_class or "",
                line_number=node.lineno,
                missing_docstring=True,
                target_type="method" if is_method else "function",
            )
            self.targets_needing_docs.append(target)

        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        """Visit class definitions."""
        old_class = self.current_class
        self.current_class = node.name

        self.stats["classes"] += 1
        docstring = ast.get_docstring(node)

        if docstring:
            self.stats["documented_classes"] += 1
        else:
            target = DocstringTarget(
                file_path=self.file_path,
                class_name=node.name,
                line_number=node.lineno,
                missing_docstring=True,
                target_type="class",
            )
            self.targets_needing_docs.append(target)

        self.generic_visit(node)
        self.current_class = old_class

    def analyze_package_coverage(self, package_path: str) -> CoverageReport:
        """Analyze docstring coverage for a package using multiple.

        approaches.
        """
        logger.info(f"📊 Analyzing docstring coverage in {package_path}")

        # Convert package path to directory
        if package_path.startswith("haive."):
            package_path = package_path.replace(".", "/")

        package_dir = project_root / "packages" / package_path / "src" / "haive"

        if not package_dir.exists():
            package_dir = project_root / "packages" / package_path / "src"

        if not package_dir.exists():
            logger.error(f"❌ Package directory not found: {package_dir}")
            return CoverageReport()

        # AST-based analysis
        all_targets = []
        python_files = list(package_dir.rglob("*.py"))

        logger.info(f"📁 Found {len(python_files)} Python files to analyze")

        total_stats = {
            "functions": 0,
            "documented_functions": 0,
            "classes": 0,
            "documented_classes": 0,
            "methods": 0,
            "documented_methods": 0,
            "modules": len(python_files),
        }

        for py_file in python_files:
            if py_file.name == "__init__.py":
                continue  # Handle separately if needed

            targets = self.analyze_file(py_file)
            all_targets.extend(targets)

            # Aggregate stats
            for key in total_stats:
                if key in self.stats:
                    total_stats[key] += self.stats[key]

        # Calculate coverage
        total_documented = (
            total_stats["documented_functions"]
            + total_stats["documented_classes"]
            + total_stats["documented_methods"]
        )
        total_items = (
            total_stats["functions"] + total_stats["classes"] + total_stats["methods"]
        )

        coverage_percentage = (
            (total_documented / total_items * 100) if total_items > 0 else 0
        )

        # Get interrogate score
        interrogate_score = self._run_interrogate_analysis(package_dir)

        # Get docstr-coverage score
        docstr_coverage_score = self._run_docstr_coverage_analysis(package_dir)

        report = CoverageReport(
            total_functions=total_stats["functions"],
            documented_functions=total_stats["documented_functions"],
            total_classes=total_stats["classes"],
            documented_classes=total_stats["documented_classes"],
            total_modules=total_stats["modules"],
            missing_targets=all_targets,
            coverage_percentage=coverage_percentage,
            interrogate_score=interrogate_score,
            docstr_coverage_score=docstr_coverage_score,
        )

        self._report_coverage_results(report)
        return report

    def _run_interrogate_analysis(self, package_dir: Path) -> float:
        """Run interrogate for professional docstring coverage analysis."""
        logger.info("🔍 Running interrogate analysis...")

        try:
            result = subprocess.run(
                [
                    "interrogate",
                    str(package_dir),
                    "--ignore-init-method",
                    "--ignore-init-module",
                    "--ignore-magic",
                    "--ignore-private",
                    "--ignore-semiprivate",
                    "--quiet-level",
                    "2",
                    "--output",
                    "json",
                ],
                capture_output=True,
                text=True,
                timeout=60,
                check=False,
            )

            if result.returncode == 0 and result.stdout:
                import json

                data = json.loads(result.stdout)
                score = data.get("overall_coverage", 0.0)
                logger.info(f"📊 Interrogate coverage: {score:.1f}%")
                return score
            logger.warning("⚠️ Interrogate analysis failed")
            return 0.0

        except FileNotFoundError:
            logger.info("ℹ️ interrogate not found (available in poetry dependencies)")
            return 0.0
        except Exception as e:
            logger.error(f"❌ Interrogate analysis error: {e}")
            return 0.0

    def _run_docstr_coverage_analysis(self, package_dir: Path) -> float:
        """Run docstr-coverage for alternative coverage analysis."""
        logger.info("🔍 Running docstr-coverage analysis...")

        try:
            result = subprocess.run(
                ["docstr-coverage", str(package_dir), "--percentage-only"],
                capture_output=True,
                text=True,
                timeout=60,
                check=False,
            )

            if result.returncode == 0 and result.stdout.strip():
                score = float(result.stdout.strip().replace("%", ""))
                logger.info(f"📊 Docstr-coverage: {score:.1f}%")
                return score
            logger.warning("⚠️ Docstr-coverage analysis failed")
            return 0.0

        except (FileNotFoundError, ValueError):
            logger.info(
                "ℹ️ docstr-coverage not found (available in poetry dependencies)",
            )
            return 0.0
        except Exception as e:
            logger.error(f"❌ Docstr-coverage analysis error: {e}")
            return 0.0

    def _report_coverage_results(self, report: CoverageReport):
        """Report comprehensive docstring coverage results."""
        logger.info("📊 Comprehensive Docstring Coverage Report:")
        logger.info(f"  📈 AST Analysis Coverage: {report.coverage_percentage:.1f}%")

        if report.interrogate_score > 0:
            logger.info(f"  🔍 Interrogate Score: {report.interrogate_score:.1f}%")

        if report.docstr_coverage_score > 0:
            logger.info(
                f"  📋 Docstr-Coverage Score: {report.docstr_coverage_score:.1f}%",
            )

        logger.info(
            f"  🔧 Functions: {report.documented_functions}/{report.total_functions} documented",
        )
        logger.info(
            f"  🏗️ Classes: {report.documented_classes}/{report.total_classes} documented",
        )
        logger.info(f"  📁 Modules: {report.total_modules} analyzed")

        if report.missing_targets:
            logger.info(f"  ❌ Missing Docstrings: {len(report.missing_targets)} items")

            # Group by type
            by_type = {}
            for target in report.missing_targets:
                if target.target_type not in by_type:
                    by_type[target.target_type] = []
                by_type[target.target_type].append(target)

            for target_type, targets in by_type.items():
                logger.info(f"    {target_type.title()}: {len(targets)} missing")


def main():
    """CLI entry point for coverage analysis."""
    import argparse

    parser = argparse.ArgumentParser(description="Docstring coverage analysis")
    parser.add_argument("--target", required=True, help="Target package")
    parser.add_argument(
        "--interrogate",
        action="store_true",
        help="Use interrogate analysis",
    )
    parser.add_argument(
        "--docstr-coverage",
        action="store_true",
        help="Use docstr-coverage analysis",
    )

    args = parser.parse_args()

    analyzer = CoverageAnalyzer()
    report = analyzer.analyze_package_coverage(args.target)

    return 0 if report.coverage_percentage > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
