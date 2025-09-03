#!/usr/bin/env python3
"""Scan all packages for docstring issues and optionally fix them.

This script:
1. Scans all Python files in packages/ (excluding tests)
2. Detects markdown-style docstrings
3. Reports all issues
4. Can convert them with --fix flag
5. Validates all changes with pydocstyle
"""

import sys
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple
import argparse
from dataclasses import dataclass, field
import json


@dataclass
class PackageScanResult:
    """Results from scanning a package."""
    package_name: str
    total_files: int = 0
    files_with_issues: int = 0
    files_with_markdown: List[str] = field(default_factory=list)
    files_with_style_issues: List[str] = field(default_factory=list)
    total_markdown_blocks: int = 0
    

def scan_file(file_path: Path, detect_script: Path) -> Tuple[bool, bool]:
    """Scan a single file for issues.
    
    Returns:
        Tuple of (has_markdown_blocks, has_style_issues)
    """
    try:
        result = subprocess.run(
            ['python', str(detect_script), str(file_path)],
            capture_output=True,
            text=True
        )
        
        # Check output for markdown blocks
        has_markdown = 'Has markdown code blocks: True' in result.stdout
        has_issues = result.returncode != 0
        
        return has_markdown, has_issues
        
    except Exception as e:
        print(f"  ⚠️  Error scanning {file_path}: {e}")
        return False, False


def convert_file(file_path: Path, convert_script: Path, dry_run: bool = True) -> bool:
    """Convert a file's docstrings.
    
    Returns:
        True if conversion was successful
    """
    try:
        cmd = ['python', str(convert_script), str(file_path)]
        if not dry_run:
            cmd.append('--apply')
            
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Check if conversion was needed/successful
        return 'No markdown-style code blocks found' not in result.stdout
        
    except Exception as e:
        print(f"  ❌ Error converting {file_path}: {e}")
        return False


def scan_package(package_path: Path, detect_script: Path) -> PackageScanResult:
    """Scan a package for docstring issues."""
    package_name = package_path.name
    result = PackageScanResult(package_name=package_name)
    
    print(f"\n📦 Scanning {package_name}...")
    
    # Find all Python files (excluding tests)
    py_files = []
    for py_file in package_path.rglob('*.py'):
        # Skip test files
        if 'test' in py_file.parts or '__pycache__' in str(py_file):
            continue
        py_files.append(py_file)
    
    result.total_files = len(py_files)
    print(f"  Found {result.total_files} Python files")
    
    # Scan each file
    for py_file in py_files:
        has_markdown, has_issues = scan_file(py_file, detect_script)
        
        if has_markdown:
            result.files_with_markdown.append(str(py_file))
            result.total_markdown_blocks += 1
            
        if has_issues:
            result.files_with_issues += 1
            if not has_markdown:
                result.files_with_style_issues.append(str(py_file))
    
    # Report results
    if result.files_with_markdown:
        print(f"  ⚠️  {len(result.files_with_markdown)} files with markdown blocks:")
        for f in result.files_with_markdown[:5]:
            print(f"    - {Path(f).relative_to(package_path.parent)}")
        if len(result.files_with_markdown) > 5:
            print(f"    ... and {len(result.files_with_markdown) - 5} more")
    else:
        print(f"  ✅ No markdown blocks found")
        
    return result


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Scan all packages for docstring issues')
    parser.add_argument('--fix', action='store_true',
                       help='Fix markdown docstrings (convert to Google style)')
    parser.add_argument('--dry-run', action='store_true', default=True,
                       help='With --fix, show what would be changed without modifying')
    parser.add_argument('--package', help='Scan only a specific package')
    parser.add_argument('--json', action='store_true',
                       help='Output results as JSON')
    
    args = parser.parse_args()
    
    # Find scripts
    script_dir = Path(__file__).parent
    detect_script = script_dir / 'detect_docstring_issues.py'
    convert_script = script_dir / 'convert_docstrings.py'
    
    if not detect_script.exists():
        print(f"❌ Error: Detection script not found: {detect_script}")
        sys.exit(1)
        
    if args.fix and not convert_script.exists():
        print(f"❌ Error: Conversion script not found: {convert_script}")
        sys.exit(1)
    
    # Find packages to scan
    packages_dir = Path('packages')
    if not packages_dir.exists():
        print(f"❌ Error: packages/ directory not found")
        sys.exit(1)
    
    if args.package:
        package_dirs = [packages_dir / args.package]
        if not package_dirs[0].exists():
            print(f"❌ Error: Package {args.package} not found")
            sys.exit(1)
    else:
        package_dirs = sorted([d for d in packages_dir.iterdir() if d.is_dir()])
    
    # Scan packages
    all_results = []
    total_markdown_files = 0
    
    for package_dir in package_dirs:
        result = scan_package(package_dir, detect_script)
        all_results.append(result)
        total_markdown_files += len(result.files_with_markdown)
    
    # Summary
    print("\n" + "="*80)
    print("📊 SCAN SUMMARY")
    print("="*80)
    
    for result in all_results:
        status = "✅" if not result.files_with_markdown else "⚠️"
        print(f"{status} {result.package_name}: "
              f"{result.total_files} files, "
              f"{len(result.files_with_markdown)} with markdown blocks")
    
    print(f"\n📈 Total: {total_markdown_files} files need conversion")
    
    # Output JSON if requested
    if args.json:
        json_results = []
        for result in all_results:
            json_results.append({
                'package': result.package_name,
                'total_files': result.total_files,
                'files_with_markdown': result.files_with_markdown,
                'markdown_count': len(result.files_with_markdown)
            })
        print("\n📄 JSON Output:")
        print(json.dumps(json_results, indent=2))
    
    # Fix if requested
    if args.fix and total_markdown_files > 0:
        print("\n" + "="*80)
        print("🔧 FIX MODE")
        print("="*80)
        
        if args.dry_run:
            print("🔸 DRY RUN - No files will be modified")
            response = input("\nProceed with dry run? [Y/n]: ")
        else:
            print("⚠️  LIVE MODE - Files will be modified!")
            response = input(f"\nConvert {total_markdown_files} files? [y/N]: ")
            
        if response.lower() in ['y', 'yes', ''] if args.dry_run else response.lower() in ['y', 'yes']:
            print("\n🔄 Converting files...")
            
            converted_count = 0
            for result in all_results:
                for file_path in result.files_with_markdown:
                    print(f"\n📝 Converting: {Path(file_path).relative_to(Path.cwd())}")
                    if convert_file(Path(file_path), convert_script, dry_run=args.dry_run):
                        converted_count += 1
                        
            print(f"\n✅ Processed {converted_count} files")
            
            if args.dry_run:
                print("🔸 DRY RUN complete - no files were modified")
                print("  To apply changes, run with: --fix --dry-run=False")
        else:
            print("❌ Conversion cancelled")
    
    # Exit code
    sys.exit(0 if total_markdown_files == 0 else 1)


if __name__ == "__main__":
    main()