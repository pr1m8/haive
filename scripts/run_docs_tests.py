#!/usr/bin/env python3
"""
Documentation Test Suite Runner
Orchestrates all documentation testing methodologies and generates comprehensive report.
"""

import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from build_performance_test import BuildPerformanceTester
from css_audit import CSSAuditor

# Import our test modules
from docs_validation import DocumentationValidator
from path_resolution_test import PathResolutionTester


class DocumentationTestSuite:
    """Comprehensive documentation testing suite."""

    def __init__(self, docs_dir: Path):
        self.docs_dir = docs_dir
        self.source_dir = docs_dir / "source"
        self.results_dir = Path(__file__).parent / "test_results"
        self.results_dir.mkdir(exist_ok=True)

        self.test_results = {
            "timestamp": datetime.now().isoformat(),
            "test_suite_version": "1.0",
            "tests_run": [],
            "summary": {},
            "recommendations": [],
        }

    def run_all_tests(self):
        """Run all documentation tests in sequence."""
        print("🧪 Documentation Test Suite")
        print("=" * 60)
        print(f"📁 Testing directory: {self.docs_dir}")
        print(f"📊 Results will be saved to: {self.results_dir}")
        print("=" * 60)

        # Run test suites in order
        test_suites = [
            ("structure_validation", self.run_structure_validation),
            ("css_audit", self.run_css_audit),
            ("path_resolution", self.run_path_resolution),
            ("build_performance", self.run_build_performance),
        ]

        start_time = time.time()

        for test_name, test_func in test_suites:
            print(f"\n🔬 Running {test_name.replace('_', ' ').title()}...")
            print("-" * 40)

            test_start = time.time()
            try:
                test_result = test_func()
                test_duration = time.time() - test_start

                self.test_results["tests_run"].append(
                    {
                        "name": test_name,
                        "status": "success",
                        "duration": round(test_duration, 2),
                        "result": test_result,
                    }
                )

                print(f"✅ {test_name} completed in {test_duration:.1f}s")

            except Exception as e:
                test_duration = time.time() - test_start
                print(f"❌ {test_name} failed: {e}")

                self.test_results["tests_run"].append(
                    {
                        "name": test_name,
                        "status": "failed",
                        "duration": round(test_duration, 2),
                        "error": str(e),
                    }
                )

        total_duration = time.time() - start_time

        # Generate summary and recommendations
        self.generate_summary()
        self.generate_recommendations()

        # Save results
        self.save_results()

        # Print final report
        self.print_final_report(total_duration)

    def run_structure_validation(self):
        """Run documentation structure validation."""
        validator = DocumentationValidator(self.docs_dir)
        validator.validate_all()

        return {
            "issues_found": len(validator.issues),
            "issue_types": list(validator.issues.keys()),
            "critical_issues": [
                k
                for k in validator.issues.keys()
                if k in ["conf_conflicts", "conf_missing", "multiple_api_dirs"]
            ],
            "file_counts": validator.results.get("file_counts", {}),
            "detailed_issues": dict(validator.issues),
        }

    def run_css_audit(self):
        """Run CSS audit."""
        auditor = CSSAuditor(self.docs_dir)
        auditor.audit_all()

        return {
            "css_files_found": len(auditor.css_files),
            "duplicate_rules": len(auditor.duplicate_rules),
            "total_css_size_kb": sum(
                data["size"] for data in auditor.css_rules.values()
            )
            / 1024,
            "optimization_opportunities": getattr(auditor, "optimizations", {}),
            "css_by_directory": self.group_css_by_directory(auditor.css_files),
        }

    def run_path_resolution(self):
        """Run path resolution tests."""
        tester = PathResolutionTester(self.docs_dir)
        tester.test_all()

        return {
            "broken_links": len(tester.broken_links),
            "api_path_issues": len(tester.api_path_issues),
            "deep_paths": len(tester.deep_paths),
            "broken_link_types": self.categorize_broken_links(tester.broken_links),
            "path_issues_by_type": self.categorize_api_issues(tester.api_path_issues),
        }

    def run_build_performance(self):
        """Run build performance tests."""
        tester = BuildPerformanceTester(self.docs_dir)
        tester.test_all()

        # Extract key metrics
        build_times = tester.results.get("build_times", {})
        fastest_build = (
            min(build_times.values(), key=lambda x: x["time_seconds"])
            if build_times
            else None
        )
        slowest_build = (
            max(build_times.values(), key=lambda x: x["time_seconds"])
            if build_times
            else None
        )

        return {
            "builds_tested": len(build_times),
            "fastest_build_time": (
                fastest_build["time_seconds"] if fastest_build else None
            ),
            "slowest_build_time": (
                slowest_build["time_seconds"] if slowest_build else None
            ),
            "bottlenecks_found": len(tester.results.get("bottlenecks", [])),
            "api_generation_overhead": tester.results.get("api_generation", {}),
            "source_file_counts": tester.results.get("file_counts", {}),
            "total_source_size_mb": tester.results.get("total_size_mb", 0),
        }

    def group_css_by_directory(self, css_files):
        """Group CSS files by directory."""
        from collections import defaultdict

        css_by_dir = defaultdict(int)

        for css_file in css_files:
            rel_path = css_file.relative_to(self.source_dir)
            css_by_dir[str(rel_path.parent)] += 1

        return dict(css_by_dir)

    def categorize_broken_links(self, broken_links):
        """Categorize broken links by type."""
        from collections import Counter

        return dict(Counter(link["type"] for link in broken_links))

    def categorize_api_issues(self, api_issues):
        """Categorize API path issues by type."""
        from collections import Counter

        return dict(Counter(issue["issue"] for issue in api_issues))

    def generate_summary(self):
        """Generate test suite summary."""
        successful_tests = [
            t for t in self.test_results["tests_run"] if t["status"] == "success"
        ]
        failed_tests = [
            t for t in self.test_results["tests_run"] if t["status"] == "failed"
        ]

        # Collect key metrics
        total_issues = 0
        critical_issues = 0

        for test in successful_tests:
            result = test.get("result", {})

            if test["name"] == "structure_validation":
                total_issues += result.get("issues_found", 0)
                critical_issues += len(result.get("critical_issues", []))

            elif test["name"] == "path_resolution":
                total_issues += result.get("broken_links", 0)
                total_issues += result.get("api_path_issues", 0)

            elif test["name"] == "build_performance":
                total_issues += result.get("bottlenecks_found", 0)

        self.test_results["summary"] = {
            "tests_total": len(self.test_results["tests_run"]),
            "tests_successful": len(successful_tests),
            "tests_failed": len(failed_tests),
            "total_issues_found": total_issues,
            "critical_issues_found": critical_issues,
            "test_success_rate": len(successful_tests)
            / len(self.test_results["tests_run"])
            * 100,
        }

    def generate_recommendations(self):
        """Generate comprehensive recommendations based on all test results."""
        recommendations = []

        for test in self.test_results["tests_run"]:
            if test["status"] != "success":
                continue

            result = test.get("result", {})

            # Structure validation recommendations
            if test["name"] == "structure_validation":
                if result.get("critical_issues"):
                    recommendations.append(
                        {
                            "priority": "critical",
                            "category": "configuration",
                            "title": "Fix Configuration Conflicts",
                            "description": f"Found {len(result['critical_issues'])} critical configuration issues",
                            "action": "Consolidate conf*.py files into single configuration",
                        }
                    )

                if result.get("issues_found", 0) > 10:
                    recommendations.append(
                        {
                            "priority": "high",
                            "category": "cleanup",
                            "title": "Clean Up Documentation Structure",
                            "description": f"Found {result['issues_found']} structural issues",
                            "action": "Remove backup files, organize directories, clean generated content",
                        }
                    )

            # CSS audit recommendations
            elif test["name"] == "css_audit":
                if result.get("css_files_found", 0) > 20:
                    recommendations.append(
                        {
                            "priority": "medium",
                            "category": "css",
                            "title": "Consolidate CSS Files",
                            "description": f"Found {result['css_files_found']} CSS files",
                            "action": "Merge related CSS files and remove duplicates",
                        }
                    )

                if result.get("duplicate_rules", 0) > 5:
                    recommendations.append(
                        {
                            "priority": "medium",
                            "category": "css",
                            "title": "Remove Duplicate CSS Rules",
                            "description": f"Found {result['duplicate_rules']} duplicate rule patterns",
                            "action": "Consolidate duplicate CSS rules across files",
                        }
                    )

            # Path resolution recommendations
            elif test["name"] == "path_resolution":
                if result.get("broken_links", 0) > 5:
                    recommendations.append(
                        {
                            "priority": "high",
                            "category": "links",
                            "title": "Fix Broken Links",
                            "description": f"Found {result['broken_links']} broken links",
                            "action": "Update references to point to correct paths",
                        }
                    )

                if result.get("api_path_issues", 0) > 0:
                    recommendations.append(
                        {
                            "priority": "high",
                            "category": "api",
                            "title": "Fix API Path Configuration",
                            "description": f"Found {result['api_path_issues']} API path issues",
                            "action": "Update autoapi_dirs configuration to correct paths",
                        }
                    )

            # Build performance recommendations
            elif test["name"] == "build_performance":
                slowest_time = result.get("slowest_build_time", 0)
                if slowest_time > 60:
                    recommendations.append(
                        {
                            "priority": "medium",
                            "category": "performance",
                            "title": "Optimize Build Performance",
                            "description": f"Slowest build takes {slowest_time:.1f} seconds",
                            "action": "Consider parallel builds, selective API generation, or caching",
                        }
                    )

                if result.get("bottlenecks_found", 0) > 0:
                    recommendations.append(
                        {
                            "priority": "medium",
                            "category": "performance",
                            "title": "Address Performance Bottlenecks",
                            "description": f"Found {result['bottlenecks_found']} performance bottlenecks",
                            "action": "Review build configuration and source structure",
                        }
                    )

        # Sort recommendations by priority
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        recommendations.sort(key=lambda x: priority_order.get(x["priority"], 4))

        self.test_results["recommendations"] = recommendations

    def save_results(self):
        """Save test results to JSON file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = self.results_dir / f"docs_test_results_{timestamp}.json"

        with open(results_file, "w") as f:
            json.dump(self.test_results, f, indent=2, default=str)

        print(f"\n💾 Results saved to: {results_file}")

        # Also save a "latest" version
        latest_file = self.results_dir / "docs_test_results_latest.json"
        with open(latest_file, "w") as f:
            json.dump(self.test_results, f, indent=2, default=str)

    def print_final_report(self, total_duration):
        """Print comprehensive final report."""
        print("\n" + "=" * 80)
        print("📋 DOCUMENTATION TEST SUITE - FINAL REPORT")
        print("=" * 80)

        summary = self.test_results["summary"]

        # Test execution summary
        print(f"\n⏱️  EXECUTION SUMMARY:")
        print(f"   Total duration: {total_duration:.1f} seconds")
        print(f"   Tests run: {summary['tests_total']}")
        print(f"   Successful: {summary['tests_successful']} ✅")
        print(f"   Failed: {summary['tests_failed']} ❌")
        print(f"   Success rate: {summary['test_success_rate']:.1f}%")

        # Issue summary
        print(f"\n🔍 ISSUES SUMMARY:")
        print(f"   Total issues found: {summary['total_issues_found']}")
        print(f"   Critical issues: {summary['critical_issues_found']}")

        # Test results breakdown
        print(f"\n📊 TEST RESULTS BREAKDOWN:")
        for test in self.test_results["tests_run"]:
            status_emoji = "✅" if test["status"] == "success" else "❌"
            print(
                f"   {status_emoji} {test['name'].replace('_', ' ').title()}: {test['duration']}s"
            )

            if test["status"] == "success" and "result" in test:
                result = test["result"]

                # Show key metrics for each test
                if test["name"] == "structure_validation":
                    print(f"      Issues found: {result.get('issues_found', 0)}")

                elif test["name"] == "css_audit":
                    print(f"      CSS files: {result.get('css_files_found', 0)}")
                    print(f"      Duplicate rules: {result.get('duplicate_rules', 0)}")

                elif test["name"] == "path_resolution":
                    print(f"      Broken links: {result.get('broken_links', 0)}")
                    print(f"      API issues: {result.get('api_path_issues', 0)}")

                elif test["name"] == "build_performance":
                    fastest = result.get("fastest_build_time")
                    slowest = result.get("slowest_build_time")
                    if fastest and slowest:
                        print(
                            f"      Build time range: {fastest:.1f}s - {slowest:.1f}s"
                        )

        # Recommendations
        if self.test_results["recommendations"]:
            print(f"\n💡 PRIORITY RECOMMENDATIONS:")

            for i, rec in enumerate(
                self.test_results["recommendations"][:10], 1
            ):  # Top 10
                priority_emoji = {
                    "critical": "🔴",
                    "high": "🟠",
                    "medium": "🟡",
                    "low": "🟢",
                }.get(rec["priority"], "⚪")

                print(f"\n   {i}. {priority_emoji} {rec['title']} ({rec['category']})")
                print(f"      {rec['description']}")
                print(f"      Action: {rec['action']}")

        # Next steps
        print(f"\n🚀 NEXT STEPS:")

        critical_count = len(
            [
                r
                for r in self.test_results["recommendations"]
                if r["priority"] == "critical"
            ]
        )
        high_count = len(
            [r for r in self.test_results["recommendations"] if r["priority"] == "high"]
        )

        if critical_count > 0:
            print(f"   1. 🔴 Address {critical_count} critical issues immediately")
        if high_count > 0:
            print(f"   2. 🟠 Plan fixes for {high_count} high-priority issues")

        print(f"   3. 📊 Review detailed results in {self.results_dir}")
        print(f"   4. 🔄 Re-run tests after making fixes")
        print(f"   5. 📈 Set up regular testing schedule")

        # Health score
        total_possible_score = 100
        issues_penalty = min(summary["total_issues_found"] * 2, 50)
        critical_penalty = summary["critical_issues_found"] * 10
        failed_tests_penalty = summary["tests_failed"] * 15

        health_score = max(
            0,
            total_possible_score
            - issues_penalty
            - critical_penalty
            - failed_tests_penalty,
        )

        print(f"\n🏥 DOCUMENTATION HEALTH SCORE: {health_score}/100")

        if health_score >= 80:
            print("   🟢 Excellent - Documentation is in good shape")
        elif health_score >= 60:
            print("   🟡 Good - Some improvements needed")
        elif health_score >= 40:
            print("   🟠 Fair - Significant issues to address")
        else:
            print("   🔴 Poor - Major cleanup required")

        print("\n" + "=" * 80)


def main():
    """Run the complete documentation test suite."""
    docs_dir = project_root / "docs"

    if not docs_dir.exists():
        print(f"❌ Documentation directory not found: {docs_dir}")
        return 1

    # Check if we have the required dependencies
    try:
        import psutil
    except ImportError:
        print("❌ Missing dependency: psutil")
        print("Install with: poetry add psutil")
        return 1

    suite = DocumentationTestSuite(docs_dir)
    suite.run_all_tests()

    return 0


if __name__ == "__main__":
    sys.exit(main())
