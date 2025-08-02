#!/usr/bin/env python3
"""
Clean up the messy docs directory structure.

This script organizes the docs folder by:
1. Moving old logs to archive
2. Organizing build outputs
3. Cleaning up duplicate files
4. Creating proper directory structure
"""

import os
import shutil
from datetime import datetime
from pathlib import Path


def cleanup_docs_directory():
    """Clean up the docs directory structure."""
    docs_root = Path("/home/will/Projects/haive/backend/haive/docs")

    print("🧹 Starting docs directory cleanup...")

    # Create organized directory structure
    create_organized_structure(docs_root)

    # Move old build logs to archive
    archive_old_logs(docs_root)

    # Clean up duplicate and temporary files
    clean_duplicate_files(docs_root)

    # Organize build outputs
    organize_build_outputs(docs_root)

    # Clean up source directory
    clean_source_directory(docs_root)

    print("✅ Docs directory cleanup complete!")


def create_organized_structure(docs_root):
    """Create proper directory structure."""
    print("📁 Creating organized directory structure...")

    # Create main directories
    directories = [
        "archive/old_builds",
        "archive/old_logs",
        "archive/old_scripts",
        "current/build",
        "current/logs",
        "current/reports",
        "source/_static",
        "source/_templates",
        "source/api",
        "tools/scripts",
        "tools/maintenance",
    ]

    for dir_path in directories:
        (docs_root / dir_path).mkdir(parents=True, exist_ok=True)

    print(f"✅ Created {len(directories)} organized directories")


def archive_old_logs(docs_root):
    """Move old build logs to archive."""
    print("📦 Archiving old build logs...")

    logs_dir = docs_root / "logs"
    archive_logs = docs_root / "archive/old_logs"

    if logs_dir.exists():
        # Move all date-stamped log files
        log_files = list(logs_dir.glob("*_20[0-9][0-9][0-9][0-9][0-9][0-9]_*"))
        for log_file in log_files:
            shutil.move(str(log_file), str(archive_logs / log_file.name))

        # Move vault_cli logs
        vault_logs = list(logs_dir.glob("vault_cli_*"))
        for vault_log in vault_logs:
            shutil.move(str(vault_log), str(archive_logs / vault_log.name))

        print(f"✅ Archived {len(log_files) + len(vault_logs)} old log files")


def clean_duplicate_files(docs_root):
    """Remove duplicate and temporary files."""
    print("🗑️ Cleaning duplicate and temporary files...")

    # Files to remove
    files_to_remove = [
        "build_output.log",
        "reorganize_docs.py",
        "SPHINX_BUILD_FIXES_SUMMARY.md",
    ]

    removed_count = 0
    for file_name in files_to_remove:
        file_path = docs_root / file_name
        if file_path.exists():
            file_path.unlink()
            removed_count += 1

    # Clean up old backup conf files in source
    source_dir = docs_root / "source"
    if source_dir.exists():
        backup_files = list(source_dir.glob("conf_backup*.py")) + list(
            source_dir.glob("conf_*.py")
        )
        for backup_file in backup_files:
            if backup_file.name != "conf.py" and backup_file.exists():
                try:
                    backup_file.unlink()
                    removed_count += 1
                except FileNotFoundError:
                    pass

    print(f"✅ Removed {removed_count} duplicate/temporary files")


def organize_build_outputs(docs_root):
    """Organize build outputs."""
    print("📋 Organizing build outputs...")

    # Move old build directories to archive
    old_build_dirs = ["auto-generated", "docs", "site"]
    archive_builds = docs_root / "archive/old_builds"

    for build_dir in old_build_dirs:
        build_path = docs_root / build_dir
        if build_path.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            shutil.move(
                str(build_path), str(archive_builds / f"{build_dir}_{timestamp}")
            )

    # Keep main build directory clean
    current_build = docs_root / "current/build"
    main_build = docs_root / "build"

    if main_build.exists() and current_build.exists():
        # Sync main build to current build if needed
        pass

    print(f"✅ Organized build outputs")


def clean_source_directory(docs_root):
    """Clean up source directory."""
    print("📝 Cleaning source directory...")

    source_dir = docs_root / "source"
    if not source_dir.exists():
        return

    # Remove temporary files in source
    temp_files = [
        "agent_cache_loader.py",
        "agent_cache_react.json",
        "agent_cache_simple.json",
        "agent_demo_data.py",
        "dynamic_graph.log",
        "poker_game.log",
        "sphinx_debug.log",
    ]

    removed = 0
    for temp_file in temp_files:
        file_path = source_dir / temp_file
        if file_path.exists():
            file_path.unlink()
            removed += 1

    # Move vault logs to archive
    vault_logs = list(source_dir.glob("vault_cli_*"))
    archive_logs = docs_root / "archive/old_logs"

    for vault_log in vault_logs:
        shutil.move(str(vault_log), str(archive_logs / vault_log.name))
        removed += 1

    print(f"✅ Cleaned {removed} files from source directory")


def show_final_structure(docs_root):
    """Show the cleaned directory structure."""
    print("\n📁 New docs directory structure:")

    for root, dirs, files in os.walk(docs_root):
        level = root.replace(str(docs_root), "").count(os.sep)
        indent = " " * 2 * level
        print(f"{indent}{os.path.basename(root)}/")

        # Only show first few levels to avoid clutter
        if level < 3:
            sub_indent = " " * 2 * (level + 1)
            for file in files[:3]:  # Show first 3 files only
                print(f"{sub_indent}{file}")
            if len(files) > 3:
                print(f"{sub_indent}... and {len(files) - 3} more files")


if __name__ == "__main__":
    cleanup_docs_directory()
