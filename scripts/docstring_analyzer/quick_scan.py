#!/usr/bin/env python3
"""Quick scanner to find Python files with markdown code blocks in docstrings."""

import sys
import re
from pathlib import Path
from typing import List


def has_markdown_in_docstrings(file_path: Path) -> bool:
    """Check if a file has markdown code blocks in docstrings."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check for ``` inside triple-quoted strings (docstrings)
        # First find all triple-quoted sections
        triple_quote_pattern = r'(""".*?"""|\'\'\'.*?\'\'\')'
        
        for match in re.finditer(triple_quote_pattern, content, re.DOTALL):
            docstring_content = match.group(0)
            if '```' in docstring_content:
                return True
            
        return False
        
    except Exception:
        return False


def scan_directory(root_path: Path) -> List[Path]:
    """Scan directory for Python files with markdown in docstrings."""
    files_with_issues = []
    
    # Find all Python files
    for py_file in root_path.rglob('*.py'):
        # Skip test files
        if 'test' in str(py_file) or '__pycache__' in str(py_file):
            continue
            
        if has_markdown_in_docstrings(py_file):
            files_with_issues.append(py_file)
            
    return files_with_issues


def main():
    """Main entry point."""
    packages_dir = Path('packages')
    
    if not packages_dir.exists():
        print("❌ packages/ directory not found")
        sys.exit(1)
    
    print("🔍 Quick scan for markdown code blocks in docstrings...\n")
    
    total_issues = 0
    
    # Scan each package
    for package_dir in sorted(packages_dir.iterdir()):
        if not package_dir.is_dir():
            continue
            
        print(f"📦 {package_dir.name}:")
        
        issues = scan_directory(package_dir)
        
        if issues:
            print(f"  ⚠️  Found {len(issues)} file(s) with markdown blocks:")
            for file_path in issues[:5]:
                rel_path = file_path.relative_to(packages_dir)
                print(f"    - {rel_path}")
            if len(issues) > 5:
                print(f"    ... and {len(issues) - 5} more")
        else:
            print(f"  ✅ No markdown blocks found")
            
        total_issues += len(issues)
    
    print(f"\n📊 Total files with markdown blocks: {total_issues}")
    
    if total_issues > 0:
        print("\n💡 To convert these files, use:")
        print("  python scripts/docstring_analyzer/convert_docstrings.py <file> --dry-run")
        print("  python scripts/docstring_analyzer/convert_docstrings.py <file> --apply")


if __name__ == "__main__":
    main()