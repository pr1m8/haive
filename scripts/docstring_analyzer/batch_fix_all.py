#!/usr/bin/env python3
"""Batch processor to fix all docstrings in the codebase.

This script finds and processes all Python files with markdown docstrings,
converting them to Google style format.
"""

import sys
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple
import json
from datetime import datetime


def find_files_with_markdown() -> List[Path]:
    """Find all Python files with markdown code blocks in docstrings.
    
    Returns:
        List of file paths that need conversion.
    """
    files_to_fix = []
    
    # Use the quick_scan script
    result = subprocess.run(
        ['python', 'scripts/docstring_analyzer/quick_scan.py'],
        capture_output=True,
        text=True
    )
    
    # Parse output to find files
    packages_dir = Path('packages')
    for package_dir in packages_dir.iterdir():
        if not package_dir.is_dir():
            continue
            
        for py_file in package_dir.rglob('*.py'):
            # Skip test files and build directories
            if any(skip in str(py_file) for skip in ['test', '__pycache__', 'build', '.tox', 'backup']):
                continue
                
            # Quick check for markdown
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if '"""' in content or "'''" in content:
                        if '```' in content:
                            files_to_fix.append(py_file)
            except:
                continue
    
    return files_to_fix


def process_file_safely(file_path: Path, apply: bool = False) -> Tuple[bool, List[str]]:
    """Safely process a single file.
    
    Args:
        file_path: Path to process.
        apply: Whether to apply changes.
        
    Returns:
        Tuple of (success, list_of_messages).
    """
    messages = []
    
    try:
        # Run the fixer script
        cmd = ['python', 'scripts/docstring_analyzer/fix_docstrings_clean.py', str(file_path)]
        if apply:
            cmd.append('--apply')
            
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Check for success indicators in output
        output = result.stdout + result.stderr
        
        if '✅ No markdown code blocks found' in output:
            messages.append("No changes needed")
            return True, messages
        elif '✅ File updated' in output and apply:
            messages.append("Successfully converted")
            return True, messages
        elif '📝 Found' in output and not apply:
            # Extract number of changes
            import re
            match = re.search(r'Found (\d+) markdown block', output)
            if match:
                messages.append(f"{match.group(1)} blocks to convert")
            return True, messages
        elif '❌' in output:
            # Error occurred
            messages.append("Error during processing")
            return False, messages
        else:
            return True, messages
            
    except subprocess.TimeoutExpired:
        messages.append("Timeout during processing")
        return False, messages
    except Exception as e:
        messages.append(f"Exception: {e}")
        return False, messages


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Batch process all files with markdown docstrings'
    )
    parser.add_argument('--dry-run', action='store_true', default=True,
                       help='Preview changes without applying (default)')
    parser.add_argument('--apply', action='store_true',
                       help='Apply changes to files')
    parser.add_argument('--package', help='Process only specific package')
    parser.add_argument('--json', action='store_true',
                       help='Output results as JSON')
    
    args = parser.parse_args()
    
    print("🔍 Finding files with markdown docstrings...")
    
    # Find files to process
    files_to_fix = find_files_with_markdown()
    
    # Filter by package if specified
    if args.package:
        files_to_fix = [f for f in files_to_fix if args.package in str(f)]
    
    if not files_to_fix:
        print("✅ No files with markdown docstrings found!")
        sys.exit(0)
    
    print(f"\n📊 Found {len(files_to_fix)} files to process")
    
    # Group by package
    packages = {}
    for file_path in files_to_fix:
        package = file_path.parts[1] if len(file_path.parts) > 1 else "unknown"
        if package not in packages:
            packages[package] = []
        packages[package].append(file_path)
    
    # Display summary
    print("\n📦 Files by package:")
    for package, files in packages.items():
        print(f"  {package}: {len(files)} files")
    
    if not args.apply:
        print("\n🔸 DRY RUN MODE - No files will be modified")
        print("  Use --apply to actually convert files")
    else:
        print("\n⚠️  APPLY MODE - Files will be modified!")
        response = input("Continue? [y/N]: ")
        if response.lower() != 'y':
            print("❌ Cancelled")
            sys.exit(1)
    
    # Process files
    print(f"\n{'='*80}")
    print("PROCESSING FILES")
    print("="*80)
    
    results = {
        'successful': [],
        'failed': [],
        'skipped': []
    }
    
    for i, file_path in enumerate(files_to_fix, 1):
        try:
            rel_path = file_path.relative_to(Path.cwd())
        except ValueError:
            rel_path = file_path
        print(f"\n[{i}/{len(files_to_fix)}] {rel_path}")
        
        success, messages = process_file_safely(file_path, apply=args.apply)
        
        if success:
            if "No changes needed" in str(messages):
                results['skipped'].append(str(rel_path))
                print("  ⏭️  Skipped (no changes needed)")
            else:
                results['successful'].append(str(rel_path))
                print(f"  ✅ {', '.join(messages)}")
        else:
            results['failed'].append(str(rel_path))
            print(f"  ❌ {', '.join(messages)}")
    
    # Summary
    print(f"\n{'='*80}")
    print("SUMMARY")
    print("="*80)
    print(f"✅ Successful: {len(results['successful'])}")
    print(f"⏭️  Skipped: {len(results['skipped'])}")
    print(f"❌ Failed: {len(results['failed'])}")
    
    if results['failed']:
        print("\n❌ Failed files:")
        for file_path in results['failed'][:10]:
            print(f"  - {file_path}")
        if len(results['failed']) > 10:
            print(f"  ... and {len(results['failed']) - 10} more")
    
    # JSON output if requested
    if args.json:
        output = {
            'timestamp': datetime.now().isoformat(),
            'mode': 'apply' if args.apply else 'dry-run',
            'total_files': len(files_to_fix),
            'results': results
        }
        print("\n📄 JSON Output:")
        print(json.dumps(output, indent=2))
    
    # Exit code
    sys.exit(0 if not results['failed'] else 1)


if __name__ == "__main__":
    main()