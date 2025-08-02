#!/usr/bin/env python3
"""
Properly reorganize the docs directory.

This script completely restructures the docs folder to be clean and logical:
- Keeps only essential files in root
- Archives all the messy accumulated files
- Creates a proper structure for ongoing work
"""

import os
import shutil
from datetime import datetime
from pathlib import Path


def reorganize_docs_directory():
    """Completely reorganize the docs directory."""
    docs_root = Path("/home/will/Projects/haive/backend/haive/docs")

    print("🧹 MAJOR DOCS REORGANIZATION")
    print("=" * 50)

    # First, let's see what we're dealing with
    show_current_mess(docs_root)

    # Create a proper clean structure
    create_clean_structure(docs_root)

    # Move the mess to archive
    archive_the_mess(docs_root)

    # Keep only essential files in root
    keep_essentials_only(docs_root)

    # Show final clean result
    show_clean_result(docs_root)


def show_current_mess(docs_root):
    """Show current messy state."""
    print(f"📊 CURRENT MESS in {docs_root}:")

    items = list(docs_root.iterdir())
    dirs = [item for item in items if item.is_dir()]
    files = [item for item in items if item.is_file()]

    print(f"   📁 Directories: {len(dirs)}")
    print(f"   📄 Files: {len(files)}")

    # Show the worst offenders
    if len(dirs) > 10:
        print(f"   🚨 TOO MANY DIRECTORIES: {[d.name for d in dirs[:10]]}...")
    if len(files) > 5:
        print(f"   🚨 TOO MANY ROOT FILES: {[f.name for f in files[:5]]}...")


def create_clean_structure(docs_root):
    """Create the clean target structure."""
    print("📁 Creating clean target structure...")

    # Target structure
    clean_structure = [
        "build",  # Sphinx build output
        "source",  # Sphinx source files
        "archive",  # All the mess goes here
        "tools",  # Scripts and utilities
    ]

    for dir_name in clean_structure:
        dir_path = docs_root / dir_name
        dir_path.mkdir(exist_ok=True)

    # Create archive subdirectories for the mess
    archive_structure = [
        "archive/logs",
        "archive/screenshots",
        "archive/scripts",
        "archive/data",
        "archive/guides",
        "archive/reports",
        "archive/captures",
        "archive/images",
        "archive/notes",
        "archive/misc",
    ]

    for subdir in archive_structure:
        (docs_root / subdir).mkdir(parents=True, exist_ok=True)

    print(f"✅ Created clean structure with {len(clean_structure)} main dirs")


def archive_the_mess(docs_root):
    """Move all the messy directories to archive."""
    print("📦 Archiving the mess...")

    # Directories to archive (move to archive/)
    dirs_to_archive = [
        "logs",
        "screenshots",
        "data",
        "guides",
        "reports",
        "captures",
        "images",
        "notes",
        "quality-reports",
        "scripts",
        "resources",
        "test_nitpick",
        "test_type_hints",
        "architecture",
        "examples",
        "current",  # Even our current attempt was messy
    ]

    archived_count = 0
    for dir_name in dirs_to_archive:
        source_dir = docs_root / dir_name
        if source_dir.exists() and source_dir.is_dir():
            target_dir = docs_root / "archive" / dir_name
            if target_dir.exists():
                # Merge if target exists
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                target_dir = docs_root / "archive" / f"{dir_name}_{timestamp}"

            shutil.move(str(source_dir), str(target_dir))
            archived_count += 1
            print(f"   📦 Archived: {dir_name}")

    print(f"✅ Archived {archived_count} directories")


def keep_essentials_only(docs_root):
    """Keep only essential files in root."""
    print("📄 Cleaning up root files...")

    # Files that should stay in root
    essential_files = [
        "Makefile",
        "make.bat",
        "README.md",
        "requirements.txt",
        "requirements-dev.txt",
    ]

    # Files to archive
    files_to_archive = []
    for item in docs_root.iterdir():
        if item.is_file() and item.name not in essential_files:
            files_to_archive.append(item)

    # Move non-essential files to archive
    for file_path in files_to_archive:
        target_path = docs_root / "archive" / "misc" / file_path.name
        shutil.move(str(file_path), str(target_path))
        print(f"   📦 Archived file: {file_path.name}")

    print(
        f"✅ Kept {len(essential_files)} essential files, archived {len(files_to_archive)} others"
    )


def show_clean_result(docs_root):
    """Show the final clean structure."""
    print("\n🎉 CLEAN DOCS DIRECTORY STRUCTURE:")
    print("=" * 50)

    for item in sorted(docs_root.iterdir()):
        if item.is_dir():
            file_count = len([f for f in item.rglob("*") if f.is_file()])
            print(f"📁 {item.name}/ ({file_count} files)")
        else:
            print(f"📄 {item.name}")

    print("\n✅ REORGANIZATION COMPLETE!")
    print("Now you have:")
    print("  📁 build/     - Sphinx HTML output")
    print("  📁 source/    - Sphinx source files")
    print("  📁 archive/   - All the old mess (safely stored)")
    print("  📁 tools/     - Scripts and utilities")
    print("  📄 Essential files only in root")


def handle_git_lfs():
    """Handle Git LFS if present."""
    docs_root = Path("/home/will/Projects/haive/backend/haive/docs")
    git_dir = docs_root / ".git"

    if git_dir.exists():
        print("\n⚠️  Found .git directory (probably Git LFS)")
        print("   This might be tracking large files like screenshots")
        print("   Keeping .git directory but archiving LFS content")

        # Move large files to archive but keep .git
        large_file_patterns = ["*.png", "*.jpg", "*.jpeg", "*.gif", "*.mp4"]
        for pattern in large_file_patterns:
            for file_path in docs_root.glob(pattern):
                target_path = docs_root / "archive" / "misc" / file_path.name
                if not target_path.exists():
                    shutil.move(str(file_path), str(target_path))
                    print(f"   📦 Moved large file: {file_path.name}")


if __name__ == "__main__":
    reorganize_docs_directory()
    handle_git_lfs()
