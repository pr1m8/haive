#!/usr/bin/env python3
"""Clean and robust docstring converter from markdown to Google style.

This script safely converts markdown code blocks in docstrings to Google style format.
Features:
- Robust error handling
- Proper indentation preservation
- Safe dry-run by default
- Comprehensive validation
- Detailed progress reporting
"""

import re
import sys
import shutil
import argparse
import subprocess
import tempfile
import traceback
from pathlib import Path
from datetime import datetime
from typing import Tuple, List, Optional
import difflib


class DocstringConverter:
    """Handles conversion of markdown docstrings to Google style."""
    
    def __init__(self, verbose: bool = False):
        """Initialize converter.
        
        Args:
            verbose: Enable verbose output.
        """
        self.verbose = verbose
        self.errors = []
        
    def convert_content(self, content: str) -> Tuple[str, int, List[str]]:
        """Convert markdown code blocks in docstrings to Google style.
        
        Args:
            content: File content to process.
            
        Returns:
            Tuple of (converted_content, number_of_changes, list_of_errors).
        """
        changes_made = 0
        self.errors = []
        
        def process_docstring(match):
            """Process a single docstring."""
            nonlocal changes_made
            
            try:
                full_match = match.group(0)
                quotes = match.group(1)  # """ or '''
                docstring_content = match.group(2)
                
                # Check if it contains markdown code blocks
                if '```' not in docstring_content:
                    return full_match
                
                # Determine indentation level
                # Find the line this docstring starts on
                start_pos = match.start()
                lines_before = content[:start_pos].split('\n')
                if lines_before:
                    last_line = lines_before[-1]
                    base_indent = len(last_line) - len(last_line.lstrip())
                else:
                    base_indent = 0
                
                # Process line by line
                lines = docstring_content.split('\n')
                result_lines = []
                in_code_block = False
                code_block_lines = []
                examples_added = False
                
                i = 0
                while i < len(lines):
                    line = lines[i]
                    
                    # Check for code block markers
                    if '```python' in line or '```Python' in line or line.strip() == '```python':
                        in_code_block = True
                        code_block_lines = []
                        changes_made += 1
                    elif line.strip() == '```' and in_code_block:
                        # End of code block - convert to Google style
                        in_code_block = False
                        
                        if code_block_lines:
                            # Add Examples section if not already added
                            if not examples_added:
                                # Check if we need blank line before
                                if result_lines and result_lines[-1].strip():
                                    result_lines.append('')
                                    
                                # For function/class docstrings, indent Examples
                                if base_indent > 0:
                                    result_lines.append('    Examples:')
                                else:
                                    result_lines.append('Examples:')
                                examples_added = True
                            elif result_lines and result_lines[-1].strip():
                                # Add blank line between example blocks
                                result_lines.append('')
                            
                            # Add code with >>> prefix
                            for code_line in code_block_lines:
                                stripped = code_line.lstrip()
                                if stripped:
                                    if base_indent > 0:
                                        # Function/class docstring
                                        result_lines.append('        >>> ' + stripped)
                                    else:
                                        # Module docstring
                                        result_lines.append('    >>> ' + stripped)
                                else:
                                    if base_indent > 0:
                                        result_lines.append('        >>>')
                                    else:
                                        result_lines.append('    >>>')
                        
                        code_block_lines = []
                    elif in_code_block:
                        # Inside code block - collect lines
                        code_block_lines.append(line)
                    else:
                        # Regular docstring line
                        result_lines.append(line)
                    
                    i += 1
                
                # Handle unclosed code block (shouldn't happen but be safe)
                if in_code_block and code_block_lines:
                    if not examples_added:
                        if result_lines and result_lines[-1].strip():
                            result_lines.append('')
                        if base_indent > 0:
                            result_lines.append('    Examples:')
                        else:
                            result_lines.append('Examples:')
                    
                    for code_line in code_block_lines:
                        stripped = code_line.lstrip()
                        if stripped:
                            if base_indent > 0:
                                result_lines.append('        >>> ' + stripped)
                            else:
                                result_lines.append('    >>> ' + stripped)
                        else:
                            if base_indent > 0:
                                result_lines.append('        >>>')
                            else:
                                result_lines.append('    >>>')
                
                # Reconstruct docstring
                return quotes + '\n'.join(result_lines) + quotes
                
            except Exception as e:
                self.errors.append(f"Error processing docstring: {e}")
                if self.verbose:
                    traceback.print_exc()
                return match.group(0)  # Return original on error
        
        # Match all docstrings (module, class, function)
        # This pattern captures triple-quoted strings
        pattern = r'("""|\'\'\')((?:[^\\]|\\.|(?!\1).)*?)\1'
        
        try:
            result = re.sub(pattern, process_docstring, content, flags=re.DOTALL)
            return result, changes_made, self.errors
        except Exception as e:
            self.errors.append(f"Error during conversion: {e}")
            return content, 0, self.errors


def validate_python_syntax(content: str, file_path: Path) -> Tuple[bool, Optional[str]]:
    """Validate Python syntax of content.
    
    Args:
        content: Python code to validate.
        file_path: Path for error reporting.
        
    Returns:
        Tuple of (is_valid, error_message).
    """
    try:
        compile(content, str(file_path), 'exec')
        return True, None
    except SyntaxError as e:
        return False, f"Syntax error at line {e.lineno}: {e.msg}"


def validate_with_pydocstyle(file_path: Path) -> List[str]:
    """Validate file with pydocstyle Google convention.
    
    Args:
        file_path: Path to Python file.
        
    Returns:
        List of validation warnings.
    """
    try:
        result = subprocess.run(
            ['pydocstyle', '--convention=google', str(file_path)],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        warnings = []
        if result.stdout:
            for line in result.stdout.split('\n'):
                line = line.strip()
                if line and not line.startswith('Checking'):
                    # Parse and format nicely
                    if ':' in line and ' in ' in line:
                        parts = line.split(':', 2)
                        if len(parts) >= 3:
                            warnings.append(parts[2].strip())
                    elif line.startswith('D'):
                        warnings.append(line)
        
        return warnings
        
    except subprocess.TimeoutExpired:
        return ["Validation timeout"]
    except FileNotFoundError:
        return ["pydocstyle not installed"]
    except Exception as e:
        return [f"Validation error: {e}"]


def show_diff(original: str, converted: str, max_lines: int = 50) -> None:
    """Show colored diff between original and converted content.
    
    Args:
        original: Original content.
        converted: Converted content.
        max_lines: Maximum lines to show.
    """
    diff = difflib.unified_diff(
        original.splitlines(keepends=True),
        converted.splitlines(keepends=True),
        fromfile="original",
        tofile="converted",
        n=3
    )
    
    lines_shown = 0
    for line in diff:
        if lines_shown >= max_lines:
            print(f"... ({lines_shown} lines shown, diff truncated)")
            break
            
        if line.startswith('+') and not line.startswith('+++'):
            print(f"\033[92m{line}\033[0m", end='')  # Green
        elif line.startswith('-') and not line.startswith('---'):
            print(f"\033[91m{line}\033[0m", end='')  # Red
        else:
            print(line, end='')
        lines_shown += 1


def process_file(file_path: Path, apply: bool = False, verbose: bool = False) -> Tuple[bool, List[str]]:
    """Process a single Python file.
    
    Args:
        file_path: Path to the Python file.
        apply: If True, apply changes to file.
        verbose: Enable verbose output.
        
    Returns:
        Tuple of (had_changes, list_of_issues).
    """
    print(f"\n{'='*80}")
    print(f"📄 Processing: {file_path}")
    print(f"Mode: {'APPLY CHANGES' if apply else 'DRY RUN'}")
    print(f"{'='*80}")
    
    issues = []
    
    # Read file
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
    except Exception as e:
        error_msg = f"❌ Cannot read file: {e}"
        print(error_msg)
        return False, [error_msg]
    
    # Validate original syntax
    is_valid, syntax_error = validate_python_syntax(original_content, file_path)
    if not is_valid:
        error_msg = f"❌ Original file has syntax error: {syntax_error}"
        print(error_msg)
        return False, [error_msg]
    
    # Convert
    converter = DocstringConverter(verbose=verbose)
    converted_content, num_changes, conversion_errors = converter.convert_content(original_content)
    
    if conversion_errors:
        print(f"\n⚠️  Conversion warnings:")
        for error in conversion_errors:
            print(f"  - {error}")
            issues.append(error)
    
    if num_changes == 0:
        print("\n✅ No markdown code blocks found in docstrings")
        return False, issues
    
    print(f"\n📝 Found {num_changes} markdown block(s) to convert")
    
    # Validate converted syntax
    is_valid, syntax_error = validate_python_syntax(converted_content, file_path)
    if not is_valid:
        error_msg = f"❌ Converted file would have syntax error: {syntax_error}"
        print(error_msg)
        issues.append(error_msg)
        return False, issues
    
    # Show diff preview
    if not apply or verbose:
        print("\n📊 Preview of changes:")
        print("-" * 40)
        show_diff(original_content, converted_content)
    
    # Validate with pydocstyle
    print("\n🔍 Google style validation:")
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp:
        tmp.write(converted_content)
        tmp_path = Path(tmp.name)
    
    try:
        warnings = validate_with_pydocstyle(tmp_path)
        if warnings:
            # Filter out minor warnings
            major_warnings = [w for w in warnings if not any(
                ignore in w for ignore in [
                    'First line should end with a period',
                    'No blank lines allowed',
                    'Missing docstring in',
                    '1 blank line required'
                ]
            )]
            
            if major_warnings:
                print(f"  ⚠️  {len(major_warnings)} style warnings:")
                for warning in major_warnings[:5]:
                    print(f"    - {warning}")
                if len(major_warnings) > 5:
                    print(f"    ... and {len(major_warnings) - 5} more")
            else:
                print("  ✅ Only minor style warnings (punctuation, blank lines)")
        else:
            print("  ✅ Passes Google style validation!")
    finally:
        tmp_path.unlink(missing_ok=True)
    
    # Apply changes if requested
    if apply:
        try:
            # Create backup
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = file_path.with_suffix(f'.backup.{timestamp}')
            shutil.copy2(file_path, backup_path)
            print(f"\n💾 Backup created: {backup_path}")
            
            # Write converted content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(converted_content)
            print(f"✅ File updated: {file_path}")
            
        except Exception as e:
            error_msg = f"❌ Failed to write file: {e}"
            print(error_msg)
            issues.append(error_msg)
            return False, issues
    else:
        print(f"\n🔸 DRY RUN - No files modified")
        print(f"  To apply: {sys.argv[0]} {file_path} --apply")
    
    return True, issues


def process_directory(directory: Path, apply: bool = False, verbose: bool = False) -> None:
    """Process all Python files in a directory.
    
    Args:
        directory: Directory to process.
        apply: If True, apply changes.
        verbose: Enable verbose output.
    """
    py_files = []
    for py_file in directory.rglob('*.py'):
        # Skip test files and build directories
        if any(skip in str(py_file) for skip in ['test', '__pycache__', 'build', '.tox']):
            continue
        py_files.append(py_file)
    
    print(f"\n🔍 Found {len(py_files)} Python files to check")
    
    files_with_changes = 0
    total_issues = []
    
    for py_file in py_files:
        had_changes, issues = process_file(py_file, apply=apply, verbose=verbose)
        if had_changes:
            files_with_changes += 1
        if issues:
            total_issues.extend(issues)
    
    # Summary
    print("\n" + "="*80)
    print("📊 SUMMARY")
    print("="*80)
    print(f"Files processed: {len(py_files)}")
    print(f"Files with changes: {files_with_changes}")
    if total_issues:
        print(f"Total issues: {len(total_issues)}")
    else:
        print("No issues encountered ✅")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Convert markdown code blocks in docstrings to Google style',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dry run on a single file
  %(prog)s path/to/file.py
  
  # Apply changes to a file
  %(prog)s path/to/file.py --apply
  
  # Process entire directory
  %(prog)s --dir packages/haive-core
  
  # Apply to all packages with verbose output
  %(prog)s --dir packages --apply --verbose
        """
    )
    
    parser.add_argument('file', nargs='?', help='Python file to process')
    parser.add_argument('--apply', action='store_true',
                       help='Apply changes (default is dry-run)')
    parser.add_argument('--dir', help='Process all Python files in directory')
    parser.add_argument('--verbose', action='store_true',
                       help='Enable verbose output')
    
    args = parser.parse_args()
    
    if args.dir:
        # Process directory
        dir_path = Path(args.dir)
        if not dir_path.exists():
            print(f"❌ Directory not found: {dir_path}")
            sys.exit(1)
        process_directory(dir_path, apply=args.apply, verbose=args.verbose)
        
    elif args.file:
        # Process single file
        file_path = Path(args.file)
        
        if not file_path.exists():
            print(f"❌ File not found: {file_path}")
            sys.exit(1)
        
        if file_path.suffix != '.py':
            print(f"❌ Not a Python file: {file_path}")
            sys.exit(1)
        
        had_changes, issues = process_file(file_path, apply=args.apply, verbose=args.verbose)
        
        if issues and not args.apply:
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()