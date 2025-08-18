#!/usr/bin/env python3
"""Utility script to find and clean up .bak backup files.

This script helps manage backup files created by the docstring fixer.

Usage:
    # List all backup files
    python scripts/cleanup_backups.py --list

    # Remove backups older than 7 days
    python scripts/cleanup_backups.py --clean --days 7

    # Remove all backups (with confirmation)
    python scripts/cleanup_backups.py --clean --all
"""

import argparse
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Tuple


def find_backup_files(
    root_path: Path = None, pattern: str = "*.py.bak"
) -> List[Tuple[Path, float]]:
    """Find all backup files with modification times.

    Args:
        root_path: Root directory to search (default: current directory).
        pattern: File pattern to match (default: *.py.bak).

    Returns:
        List of (file_path, modification_time) tuples.
    """
    if root_path is None:
        root_path = Path.cwd()

    backup_files = []
    for file_path in root_path.rglob(pattern):
        # Skip hidden directories
        if any(part.startswith(".") for part in file_path.parts):
            continue

        try:
            mtime = file_path.stat().st_mtime
            backup_files.append((file_path, mtime))
        except OSError:
            continue

    return sorted(backup_files, key=lambda x: x[1], reverse=True)


def format_file_info(file_path: Path, mtime: float) -> str:
    """Format file information for display."""
    mod_date = datetime.fromtimestamp(mtime)
    age_days = (datetime.now() - mod_date).days
    size_kb = file_path.stat().st_size / 1024

    return f"{file_path} ({size_kb:.1f}KB, {age_days}d old)"


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Manage .bak backup files created by docstring fixer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument("--list", action="store_true", help="List all backup files")
    parser.add_argument("--clean", action="store_true", help="Remove backup files")
    parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="Remove backups older than N days (default: 7)",
    )
    parser.add_argument(
        "--all", action="store_true", help="Remove all backups regardless of age"
    )
    parser.add_argument(
        "--pattern",
        default="*.py.bak",
        help="File pattern to match (default: *.py.bak)",
    )
    parser.add_argument(
        "--dir", type=Path, default=None, help="Directory to search (default: current)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be removed without removing",
    )

    args = parser.parse_args()

    # Find backup files
    backup_files = find_backup_files(args.dir, args.pattern)

    if not backup_files:
        print("No backup files found.")
        return 0

    print(f"Found {len(backup_files)} backup files")

    if args.list or (not args.clean):
        # List files
        total_size = 0
        for file_path, mtime in backup_files:
            print(f"  {format_file_info(file_path, mtime)}")
            total_size += file_path.stat().st_size

        print(f"\nTotal size: {total_size / 1024 / 1024:.1f}MB")

        if not args.clean:
            print("\nUse --clean to remove files")

    elif args.clean:
        # Determine which files to remove
        cutoff_time = 0
        if not args.all:
            cutoff_date = datetime.now() - timedelta(days=args.days)
            cutoff_time = cutoff_date.timestamp()

        files_to_remove = [
            (f, t) for f, t in backup_files if args.all or t < cutoff_time
        ]

        if not files_to_remove:
            print(f"No backup files older than {args.days} days.")
            return 0

        print(f"\nFiles to remove: {len(files_to_remove)}")
        total_size = sum(f.stat().st_size for f, _ in files_to_remove)
        print(f"Total size to free: {total_size / 1024 / 1024:.1f}MB")

        if args.dry_run:
            print("\nDRY RUN - Files that would be removed:")
            for file_path, mtime in files_to_remove:
                print(f"  {format_file_info(file_path, mtime)}")
        else:
            # Confirm before removing
            response = input(f"\nRemove {len(files_to_remove)} backup files? [y/N] ")
            if response.lower() != "y":
                print("Cancelled.")
                return 0

            # Remove files
            removed = 0
            failed = 0
            for file_path, _ in files_to_remove:
                try:
                    file_path.unlink()
                    removed += 1
                except Exception as e:
                    print(f"  Failed to remove {file_path}: {e}")
                    failed += 1

            print(f"\nRemoved {removed} files")
            if failed:
                print(f"Failed to remove {failed} files")

    return 0


if __name__ == "__main__":
    exit(main())
