#!/usr/bin/env python3
"""Comprehensive documentation audit combining all docstring tools.

This module provides comprehensive documentation auditing including:
- Coverage analysis with multiple tools (AST, interrogate, docstr-coverage)
- PEP 257 compliance checking with pydocstyle and flake8-docstrings
- Documentation quality analysis with Vale
- Markdown quality and link validation
- Comprehensive recommendations and reporting
"""

import logging
import sys
from pathlib import Path
from typing import Any, Dict, List

from .coverage import CoverageAnalyzer
from .formatting import DocstringFormatter
from .generation import DocstringGenerator
from .quality import QualityChecker
from .validation import ComplianceChecker

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


class DocumentationAuditor:
    """Comprehensive documentation auditor using all available tools."""

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.coverage_analyzer = CoverageAnalyzer()
        self.formatter = DocstringFormatter(dry_run=dry_run)
        self.generator = DocstringGenerator(dry_run=dry_run)
        self.compliance_checker = ComplianceChecker()
        self.quality_checker = QualityChecker()

    def comprehensive_audit(self, package_path: str) -> Dict[str, Any]:
        """Run comprehensive documentation audit with all tools."""
        logger.info(f"🔍 Running comprehensive documentation audit on {package_path}")

        audit_results = {
            "coverage_report": None,
            "validation_results": None,
            "quality_results": None,
            "formatting_needed": False,
            "generation_needed": False,
            "recommendations": [],
            "tools_used": [],
            "overall_score": 0.0,
        }

        # 1. Coverage analysis with multiple tools
        logger.info("📊 Step 1: Analyzing docstring coverage...")
        coverage_report = self.coverage_analyzer.analyze_package_coverage(package_path)
        audit_results["coverage_report"] = coverage_report
        audit_results["tools_used"].extend(["ast-analysis"])

        if coverage_report.interrogate_score > 0:
            audit_results["tools_used"].append("interrogate")
        if coverage_report.docstr_coverage_score > 0:
            audit_results["tools_used"].append("docstr-coverage")

        # 2. PEP 257 compliance validation
        logger.info("📋 Step 2: Validating PEP 257 compliance...")
        validation_results = self.compliance_checker.comprehensive_validation(
            package_path
        )
        audit_results["validation_results"] = validation_results
        audit_results["tools_used"].extend(validation_results["tools_used"])

        # 3. Documentation quality analysis
        logger.info("📖 Step 3: Analyzing documentation quality...")
        quality_results = self.quality_checker.comprehensive_quality_check(package_path)
        audit_results["quality_results"] = quality_results
        audit_results["tools_used"].extend(quality_results["tools_used"])

        # 4. Check if formatting would make improvements
        if not self.dry_run:
            logger.info("🔧 Step 4: Checking docstring formatting...")
            # Temporarily set dry_run to check formatting
            original_dry_run = self.formatter.dry_run
            self.formatter.dry_run = True
            formatting_result = self.formatter.format_with_docformatter(package_path)
            self.formatter.dry_run = original_dry_run
            audit_results["formatting_needed"] = formatting_result

        # 5. Check if generation is needed
        if coverage_report.missing_targets:
            audit_results["generation_needed"] = True

        # 6. Generate comprehensive recommendations
        recommendations = self._generate_recommendations(audit_results)
        audit_results["recommendations"] = recommendations

        # 7. Calculate overall score
        overall_score = self._calculate_overall_score(audit_results)
        audit_results["overall_score"] = overall_score

        # 8. Report comprehensive results
        self._report_comprehensive_audit_results(audit_results)

        return audit_results

    def _generate_recommendations(self, audit_results: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations based on audit results."""
        recommendations = []

        coverage_report = audit_results["coverage_report"]
        validation_results = audit_results["validation_results"]
        quality_results = audit_results["quality_results"]

        # Coverage recommendations
        if coverage_report and coverage_report.coverage_percentage < 70:
            recommendations.append(
                f"📝 Low docstring coverage ({coverage_report.coverage_percentage:.1f}%) - "
                f"Consider generating {len(coverage_report.missing_targets)} missing docstrings"
            )
        elif coverage_report and coverage_report.coverage_percentage >= 90:
            recommendations.append(
                "🎉 Excellent docstring coverage! Focus on quality improvements"
            )

        # Validation recommendations
        if validation_results and validation_results["total_issues"] > 50:
            recommendations.append(
                f"📋 Many PEP 257 issues ({validation_results['total_issues']}) - "
                "Run docformatter to fix formatting issues"
            )
        elif validation_results and validation_results["total_issues"] > 0:
            recommendations.append(
                f"📋 {validation_results['total_issues']} PEP 257 issues found - "
                "Review and fix compliance issues"
            )

        # Quality recommendations
        if quality_results and quality_results["total_issues"] > 20:
            recommendations.append(
                f"📖 Many documentation quality issues ({quality_results['total_issues']}) - "
                "Review markdown formatting and broken links"
            )

        # Tool-specific recommendations
        if coverage_report and coverage_report.interrogate_score == 0.0:
            recommendations.append(
                "🔍 Consider installing interrogate for professional coverage analysis"
            )

        if not quality_results or not quality_results["vale_passed"]:
            recommendations.append(
                "📖 Consider installing Vale for prose quality analysis"
            )

        # Generation recommendations
        if audit_results["generation_needed"]:
            missing_count = (
                len(coverage_report.missing_targets) if coverage_report else 0
            )
            recommendations.append(
                f"🚀 Generate {missing_count} missing docstrings to improve coverage"
            )

        # Formatting recommendations
        if audit_results["formatting_needed"]:
            recommendations.append(
                "🔧 Apply docformatter to improve docstring formatting"
            )

        # Overall recommendations
        if not recommendations:
            recommendations.append("✅ Documentation is in excellent condition!")

        return recommendations

    def _calculate_overall_score(self, audit_results: Dict[str, Any]) -> float:
        """Calculate overall documentation quality score (0-100)."""
        score_components = []

        # Coverage score (40% weight)
        coverage_report = audit_results["coverage_report"]
        if coverage_report:
            coverage_score = coverage_report.coverage_percentage
            # Use interrogate score if available (more accurate)
            if coverage_report.interrogate_score > 0:
                coverage_score = coverage_report.interrogate_score
            score_components.append(("coverage", coverage_score, 0.4))

        # Validation score (30% weight)
        validation_results = audit_results["validation_results"]
        if validation_results:
            # Convert issues to score (fewer issues = higher score)
            total_issues = validation_results["total_issues"]
            # Assume 100 issues = 0 score, 0 issues = 100 score
            validation_score = max(0, 100 - (total_issues * 2))
            score_components.append(("validation", validation_score, 0.3))

        # Quality score (20% weight)
        quality_results = audit_results["quality_results"]
        if quality_results:
            # Convert issues to score
            total_issues = quality_results["total_issues"]
            quality_score = max(0, 100 - (total_issues * 5))
            # Bonus for Vale passing
            if quality_results["vale_passed"]:
                quality_score = min(100, quality_score + 10)
            score_components.append(("quality", quality_score, 0.2))

        # Tools availability bonus (10% weight)
        tools_used = audit_results["tools_used"]
        tools_bonus = len(set(tools_used)) * 5  # 5 points per unique tool
        tools_score = min(100, tools_bonus)
        score_components.append(("tools", tools_score, 0.1))

        # Calculate weighted average
        if score_components:
            weighted_sum = sum(score * weight for _, score, weight in score_components)
            total_weight = sum(weight for _, _, weight in score_components)
            overall_score = weighted_sum / total_weight if total_weight > 0 else 0
        else:
            overall_score = 0

        return round(overall_score, 1)

    def _report_comprehensive_audit_results(self, audit_results: Dict[str, Any]):
        """Report comprehensive audit results with summary."""
        logger.info("=" * 60)
        logger.info("📊 COMPREHENSIVE DOCUMENTATION AUDIT REPORT")
        logger.info("=" * 60)

        # Overall score
        overall_score = audit_results["overall_score"]
        score_emoji = (
            "🎉"
            if overall_score >= 90
            else "👍" if overall_score >= 70 else "⚠️" if overall_score >= 50 else "❌"
        )
        logger.info(f"{score_emoji} Overall Documentation Score: {overall_score}/100")

        # Tools used
        tools_used = list(set(audit_results["tools_used"]))
        logger.info(f"🛠️ Tools Used: {', '.join(tools_used) if tools_used else 'None'}")

        # Coverage summary
        coverage_report = audit_results["coverage_report"]
        if coverage_report:
            logger.info(
                f"📈 Coverage: {coverage_report.coverage_percentage:.1f}% (AST analysis)"
            )
            if coverage_report.interrogate_score > 0:
                logger.info(f"🔍 Interrogate: {coverage_report.interrogate_score:.1f}%")
            if coverage_report.docstr_coverage_score > 0:
                logger.info(
                    f"📋 Docstr-Coverage: {coverage_report.docstr_coverage_score:.1f}%"
                )

        # Validation summary
        validation_results = audit_results["validation_results"]
        if validation_results:
            logger.info(f"📋 PEP 257 Issues: {validation_results['total_issues']}")

        # Quality summary
        quality_results = audit_results["quality_results"]
        if quality_results:
            logger.info(f"📖 Quality Issues: {quality_results['total_issues']}")
            if quality_results["vale_passed"]:
                logger.info("📖 Vale: Passed")

        # Recommendations
        recommendations = audit_results["recommendations"]
        if recommendations:
            logger.info("💡 Top Recommendations:")
            for i, rec in enumerate(recommendations[:5], 1):
                logger.info(f"  {i}. {rec}")
            if len(recommendations) > 5:
                logger.info(
                    f"  ... and {len(recommendations) - 5} more recommendations"
                )

        logger.info("=" * 60)


def main():
    """CLI entry point for comprehensive documentation audit."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Comprehensive documentation audit with all tools",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Full audit
  python audit.py --target haive-core
  
  # Audit with generation
  python audit.py --target haive-tools --generate
  
  # Audit with formatting
  python audit.py --target haive-agents --format --dry-run
        """,
    )

    parser.add_argument("--target", required=True, help="Target package")
    parser.add_argument(
        "--dry-run", action="store_true", help="Show what would be done"
    )
    parser.add_argument(
        "--generate", action="store_true", help="Generate missing docstrings"
    )
    parser.add_argument(
        "--format", action="store_true", help="Apply docstring formatting"
    )

    args = parser.parse_args()

    auditor = DocumentationAuditor(dry_run=args.dry_run)

    # Run comprehensive audit
    results = auditor.comprehensive_audit(args.target)

    # Apply fixes if requested
    if args.generate and results["generation_needed"]:
        coverage_report = results["coverage_report"]
        if coverage_report and coverage_report.missing_targets:
            logger.info("🚀 Generating missing docstrings...")
            generated = auditor.generator.generate_missing_docstrings(
                coverage_report.missing_targets
            )
            logger.info(f"✅ Generated {generated} docstrings")

    if args.format and results["formatting_needed"]:
        logger.info("🔧 Applying docstring formatting...")
        success = auditor.formatter.format_with_docformatter(args.target)
        if success:
            logger.info("✅ Docstring formatting applied")

    # Return exit code based on overall score
    return 0 if results["overall_score"] >= 70 else 1


if __name__ == "__main__":
    sys.exit(main())
