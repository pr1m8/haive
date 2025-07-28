#!/usr/bin/env python3
"""Documentation Issue Tracker - Track and categorize documentation improvements.

This script provides a comprehensive tracking system for documentation issues,
progress monitoring, and automated solution integration.
"""

from dataclasses import dataclass
from datetime import datetime
import sqlite3

import click


@dataclass
class DocumentationIssue:
    """Represents a documentation issue."""

    id: str
    file_path: str
    line_number: int
    issue_type: str  # docstring_missing, type_hint_missing, format_issue, etc.
    severity: str  # critical, high, medium, low
    description: str
    auto_fixable: bool
    suggested_tool: str | None
    estimated_effort: int  # minutes
    status: str  # open, in_progress, fixed, ignored
    created_at: str
    updated_at: str
    fixed_by: str | None  # human, tool_name, or None


class DocumentationTracker:
    """Track documentation issues and improvements."""

    def __init__(self, db_path: str = "doc_issues.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Initialize SQLite database for tracking."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS issues (
                id TEXT PRIMARY KEY,
                file_path TEXT NOT NULL,
                line_number INTEGER,
                issue_type TEXT NOT NULL,
                severity TEXT NOT NULL,
                description TEXT,
                auto_fixable BOOLEAN,
                suggested_tool TEXT,
                estimated_effort INTEGER,
                status TEXT DEFAULT 'open',
                created_at TEXT,
                updated_at TEXT,
                fixed_by TEXT
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS automation_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tool_name TEXT NOT NULL,
                files_processed INTEGER,
                issues_fixed INTEGER,
                run_time REAL,
                success BOOLEAN,
                error_message TEXT,
                timestamp TEXT
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS progress_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                total_issues INTEGER,
                fixed_issues INTEGER,
                coverage_percentage REAL,
                docstring_coverage REAL,
                type_hint_coverage REAL,
                timestamp TEXT
            )
        """
        )

        conn.commit()
        conn.close()

    def add_issue(self, issue: DocumentationIssue) -> bool:
        """Add a new documentation issue."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO issues VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    issue.id,
                    issue.file_path,
                    issue.line_number,
                    issue.issue_type,
                    issue.severity,
                    issue.description,
                    issue.auto_fixable,
                    issue.suggested_tool,
                    issue.estimated_effort,
                    issue.status,
                    issue.created_at,
                    issue.updated_at,
                    issue.fixed_by,
                ),
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # Issue already exists
        finally:
            conn.close()

    def update_issue_status(
        self, issue_id: str, status: str, fixed_by: str | None = None
    ):
        """Update the status of an issue."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE issues 
            SET status = ?, fixed_by = ?, updated_at = ?
            WHERE id = ?
        """,
            (status, fixed_by, datetime.now().isoformat(), issue_id),
        )

        conn.commit()
        conn.close()

    def get_issues_by_category(self) -> dict[str, list[DocumentationIssue]]:
        """Get issues grouped by category."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM issues")
        rows = cursor.fetchall()
        conn.close()

        # Group by issue type
        categories = {}
        for row in rows:
            issue = DocumentationIssue(*row)
            if issue.issue_type not in categories:
                categories[issue.issue_type] = []
            categories[issue.issue_type].append(issue)

        return categories

    def get_auto_fixable_issues(self) -> list[DocumentationIssue]:
        """Get all auto-fixable issues."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM issues 
            WHERE auto_fixable = 1 AND status = 'open'
            ORDER BY severity DESC, estimated_effort ASC
        """
        )

        rows = cursor.fetchall()
        conn.close()

        return [DocumentationIssue(*row) for row in rows]

    def record_automation_run(
        self,
        tool_name: str,
        files_processed: int,
        issues_fixed: int,
        run_time: float,
        success: bool,
        error_message: str | None = None,
    ):
        """Record the results of an automation run."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO automation_runs 
            (tool_name, files_processed, issues_fixed, run_time, success, error_message, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (
                tool_name,
                files_processed,
                issues_fixed,
                run_time,
                success,
                error_message,
                datetime.now().isoformat(),
            ),
        )

        conn.commit()
        conn.close()

    def take_progress_snapshot(self):
        """Take a snapshot of current progress."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get current statistics
        cursor.execute("SELECT COUNT(*) FROM issues")
        total_issues = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM issues WHERE status = 'fixed'")
        fixed_issues = cursor.fetchone()[0]

        coverage_percentage = (
            (fixed_issues / total_issues * 100) if total_issues > 0 else 0
        )

        # For now, use placeholder values for docstring and type coverage
        # These could be calculated by running interrogate and mypy
        docstring_coverage = 0.0  # TODO: Integrate with interrogate
        type_hint_coverage = 0.0  # TODO: Integrate with mypy

        cursor.execute(
            """
            INSERT INTO progress_snapshots 
            (total_issues, fixed_issues, coverage_percentage, docstring_coverage, type_hint_coverage, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (
                total_issues,
                fixed_issues,
                coverage_percentage,
                docstring_coverage,
                type_hint_coverage,
                datetime.now().isoformat(),
            ),
        )

        conn.commit()
        conn.close()

        return {
            "total_issues": total_issues,
            "fixed_issues": fixed_issues,
            "coverage_percentage": coverage_percentage,
        }

    def generate_progress_report(self) -> str:
        """Generate a comprehensive progress report."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Overall statistics
        cursor.execute("SELECT COUNT(*) FROM issues")
        total_issues = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM issues WHERE status = 'fixed'")
        fixed_issues = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM issues WHERE auto_fixable = 1 AND status = 'open'"
        )
        auto_fixable_remaining = cursor.fetchone()[0]

        # Issues by category
        cursor.execute(
            """
            SELECT issue_type, COUNT(*) as count, 
                   SUM(CASE WHEN status = 'fixed' THEN 1 ELSE 0 END) as fixed
            FROM issues 
            GROUP BY issue_type
            ORDER BY count DESC
        """
        )
        categories = cursor.fetchall()

        # Recent automation runs
        cursor.execute(
            """
            SELECT tool_name, issues_fixed, timestamp 
            FROM automation_runs 
            WHERE success = 1 
            ORDER BY timestamp DESC 
            LIMIT 5
        """
        )
        recent_runs = cursor.fetchall()

        conn.close()

        # Generate report
        report = []
        report.append("# 📊 Documentation Progress Report")
        report.append("")
        report.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")

        # Overall progress
        progress_pct = (fixed_issues / total_issues * 100) if total_issues > 0 else 0
        report.append("## 🎯 Overall Progress")
        report.append("")
        report.append(f"- **Total Issues**: {total_issues}")
        report.append(f"- **Fixed Issues**: {fixed_issues}")
        report.append(f"- **Progress**: {progress_pct:.1f}%")
        report.append(f"- **Auto-fixable Remaining**: {auto_fixable_remaining}")
        report.append("")

        # Progress bar
        filled = int(progress_pct / 5)  # 20 chars for 100%
        bar = "█" * filled + "░" * (20 - filled)
        report.append(f"**Progress Bar**: `{bar}` {progress_pct:.1f}%")
        report.append("")

        # Issues by category
        report.append("## 📋 Issues by Category")
        report.append("")
        report.append("| Category | Total | Fixed | Remaining | Progress |")
        report.append("|----------|-------|-------|-----------|----------|")

        for issue_type, count, fixed in categories:
            remaining = count - fixed
            cat_progress = (fixed / count * 100) if count > 0 else 0
            report.append(
                f"| {issue_type} | {count} | {fixed} | {remaining} | {cat_progress:.1f}% |"
            )

        report.append("")

        # Recent automation successes
        if recent_runs:
            report.append("## 🤖 Recent Automation Successes")
            report.append("")
            for tool_name, issues_fixed, timestamp in recent_runs:
                dt = datetime.fromisoformat(timestamp)
                report.append(
                    f"- **{tool_name}**: {issues_fixed} fixes on {dt.strftime('%m/%d %H:%M')}"
                )
            report.append("")

        # Next recommended actions
        report.append("## 🚀 Recommended Next Actions")
        report.append("")

        if auto_fixable_remaining > 0:
            report.append(
                f"1. **Run automated tools**: {auto_fixable_remaining} issues can be auto-fixed"
            )

        # Find highest impact categories
        remaining_categories = [
            (issue_type, count - fixed)
            for issue_type, count, fixed in categories
            if count - fixed > 0
        ]
        remaining_categories.sort(key=lambda x: x[1], reverse=True)

        if remaining_categories:
            top_category = remaining_categories[0]
            report.append(
                f"2. **Focus on {top_category[0]}**: {top_category[1]} remaining issues"
            )

        report.append("3. **Take progress snapshot**: Track improvements over time")
        report.append("")

        return "\n".join(report)

    def export_issues_csv(self, filename: str = "documentation_issues.csv"):
        """Export issues to CSV for external analysis."""
        import csv

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM issues")
        rows = cursor.fetchall()
        conn.close()

        with open(filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                [
                    "id",
                    "file_path",
                    "line_number",
                    "issue_type",
                    "severity",
                    "description",
                    "auto_fixable",
                    "suggested_tool",
                    "estimated_effort",
                    "status",
                    "created_at",
                    "updated_at",
                    "fixed_by",
                ]
            )
            writer.writerows(rows)

        return filename


@click.group()
def cli():
    """Documentation Issue Tracker CLI."""


@cli.command()
@click.option("--root", default="packages/", help="Root directory to scan")
def scan(root: str):
    """Scan codebase and populate issue database."""
    tracker = DocumentationTracker()

    print("🔍 Scanning codebase for documentation issues...")

    # This would integrate with existing analysis scripts
    # For now, showing the structure

    # Example: Add some sample issues
    sample_issues = [
        DocumentationIssue(
            id="missing_docstring_1",
            file_path="packages/haive-core/src/haive/core/example.py",
            line_number=10,
            issue_type="docstring_missing",
            severity="high",
            description="Function missing docstring",
            auto_fixable=True,
            suggested_tool="pydocstring",
            estimated_effort=5,
            status="open",
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            fixed_by=None,
        )
    ]

    for issue in sample_issues:
        tracker.add_issue(issue)

    print("✅ Scan complete! Use 'report' command to see results.")


@cli.command()
def report():
    """Generate progress report."""
    tracker = DocumentationTracker()
    report = tracker.generate_progress_report()
    print(report)


@cli.command()
def snapshot():
    """Take a progress snapshot."""
    tracker = DocumentationTracker()
    progress = tracker.take_progress_snapshot()
    print(
        f"📸 Snapshot taken: {progress['fixed_issues']}/{progress['total_issues']} issues fixed ({progress['coverage_percentage']:.1f}%)"
    )


@cli.command()
@click.option("--tool", required=True, help="Tool name")
@click.option("--files", default=0, help="Files processed")
@click.option("--fixes", default=0, help="Issues fixed")
@click.option("--time", default=0.0, help="Run time in seconds")
@click.option("--success/--failure", default=True, help="Success status")
def record_run(tool: str, files: int, fixes: int, time: float, success: bool):
    """Record automation tool run results."""
    tracker = DocumentationTracker()
    tracker.record_automation_run(tool, files, fixes, time, success)
    print(f"✅ Recorded {tool} run: {fixes} fixes in {files} files")


@cli.command()
def auto_fixable():
    """List auto-fixable issues."""
    tracker = DocumentationTracker()
    issues = tracker.get_auto_fixable_issues()

    print(f"🤖 Found {len(issues)} auto-fixable issues:")
    print("")

    for issue in issues[:10]:  # Show top 10
        print(f"- **{issue.file_path}:{issue.line_number}**")
        print(f"  Type: {issue.issue_type} | Tool: {issue.suggested_tool}")
        print(f"  Effort: {issue.estimated_effort}min | {issue.description}")
        print("")


@cli.command()
@click.option("--output", default="issues.csv", help="Output CSV file")
def export(output: str):
    """Export issues to CSV."""
    tracker = DocumentationTracker()
    filename = tracker.export_issues_csv(output)
    print(f"📊 Issues exported to: {filename}")


if __name__ == "__main__":
    cli()
