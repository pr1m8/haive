#!/usr/bin/env python3
"""Archive and clean up docs/source directory following backup methodology."""

from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path

# Paths
SOURCE_DIR = Path("docs/source")
ARCHIVE_DIR = Path("docs/_archives")


def create_archive_structure():
    """Create the archive directory structure."""
    dirs = [
        ARCHIVE_DIR / "conf_backups",
        ARCHIVE_DIR / "logs" / datetime.now().strftime("%Y/%m"),
        ARCHIVE_DIR / "scripts",
        ARCHIVE_DIR / "analysis",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
    print(f"✅ Created archive structure at {ARCHIVE_DIR}")


def archive_config_files():
    """Archive all backup conf files."""
    conf_files = [
        "conf.backup.py",
        "conf_complete.py",
        "conf_fixed.py",
        "conf_minimal.py",
        "conf_organized.py",
        "conf_quick.py",
        "conf_simple.py",
        "conf_stable.py",
        "conf_working.py",
        "conf_fast.py",
        "conf_quick_test.py",
        "conf_complete_backup_20250803_173227.py",
        "conf_fixed_backup_20250803_173220.py",
        "conf.py.bak",
    ]

    count = 0
    for conf_file in conf_files:
        src = SOURCE_DIR / conf_file
        if src.exists():
            dst = ARCHIVE_DIR / "conf_backups" / conf_file
            shutil.move(str(src), str(dst))
            count += 1

    print(f"📦 Archived {count} config backup files")
    return count


def archive_log_files():
    """Archive all log files."""
    log_dir = ARCHIVE_DIR / "logs" / datetime.now().strftime("%Y/%m")

    # Archive vault_cli logs
    count = 0
    for log_file in SOURCE_DIR.glob("vault_cli_*.log"):
        dst = log_dir / log_file.name
        shutil.move(str(log_file), str(dst))
        count += 1

    # Archive other logs
    other_logs = ["dynamic_graph.log", "poker_game.log"]
    for log_name in other_logs:
        src = SOURCE_DIR / log_name
        if src.exists():
            dst = log_dir / log_name
            shutil.move(str(src), str(dst))
            count += 1

    print(f"📦 Archived {count} log files")
    return count


def archive_scripts():
    """Archive orphaned Python scripts."""
    scripts = [
        "generate_package_docs.py",
        "restructure_navigation.py",
        "test_conf_extensions.py",
        "test_memory_management.py",
        "update_sidebar_structure.py",
        "toc_control_example.py",
    ]

    count = 0
    for script in scripts:
        src = SOURCE_DIR / script
        if src.exists():
            dst = ARCHIVE_DIR / "scripts" / script
            shutil.move(str(src), str(dst))
            count += 1

    print(f"📦 Archived {count} orphaned scripts")
    return count


def archive_analysis_docs():
    """Archive analysis documentation."""
    analysis_docs = [
        "CONF_MODULARIZATION_PLAN.md",
        "DOCUMENTATION_ANALYSIS.md",
        "NAVIGATION_STRUCTURE.md",
        "RST_TEMPLATE_UPDATE_GUIDE.md",
        "documentation_enhancement_plan.md",
    ]

    count = 0
    for doc in analysis_docs:
        src = SOURCE_DIR / doc
        if src.exists():
            dst = ARCHIVE_DIR / "analysis" / doc
            shutil.move(str(src), str(dst))
            count += 1

    print(f"📦 Archived {count} analysis documents")
    return count


def create_gitignore():
    """Create or update .gitignore for docs directory."""
    gitignore_content = """# Documentation backups and archives
docs/_archives/
docs/source/*.log
docs/source/conf_*.py
!docs/source/conf.py
docs/source/*_backup*
docs/source/test_*.py
docs/source/vault_cli_*.log

# Temporary files
*.bak
*.tmp
*~

# Generated content
docs/build/
docs/source/logs/
"""

    gitignore_path = Path("docs/.gitignore")
    with open(gitignore_path, "w") as f:
        f.write(gitignore_content)

    print(f"✅ Created {gitignore_path}")


def generate_report():
    """Generate a report of what was archived."""
    report = f"""
# Documentation Cleanup Report
**Date**: {datetime.now().strftime("%Y-%m-%d %H:%M")}
**Archive Location**: {ARCHIVE_DIR}

## Summary
- Config files archived: Check {ARCHIVE_DIR}/conf_backups/
- Log files archived: Check {ARCHIVE_DIR}/logs/
- Scripts archived: Check {ARCHIVE_DIR}/scripts/
- Analysis docs archived: Check {ARCHIVE_DIR}/analysis/

## Next Steps
1. Verify documentation build still works
2. Check that no critical files were moved
3. Commit the cleaned structure
"""

    report_path = ARCHIVE_DIR / "cleanup_report.md"
    with open(report_path, "w") as f:
        f.write(report)

    print(f"\n📄 Report saved to {report_path}")


def main():
    """Main cleanup function."""
    print("🧹 Starting documentation cleanup...")
    print(f"📁 Source: {SOURCE_DIR}")
    print(f"📁 Archive: {ARCHIVE_DIR}")
    print()

    # Create archive structure
    create_archive_structure()

    # Archive files by category
    total = 0
    total += archive_config_files()
    total += archive_log_files()
    total += archive_scripts()
    total += archive_analysis_docs()

    # Create .gitignore
    create_gitignore()

    # Generate report
    generate_report()

    print(f"\n✅ Cleanup complete! Archived {total} files total.")
    print("📌 Remember to test the documentation build!")


if __name__ == "__main__":
    main()
