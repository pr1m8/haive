#!/usr/bin/env python3
"""Convert markdown-style docstrings to Google style with validation.

This script:
1. Detects docstrings with markdown code blocks (```)
2. Converts them to Google-style Examples sections
3. Validates with pydocstyle
4. Supports dry-run mode to preview changes
5. Creates backups before modifying files
"""

import ast
import sys
import re
import shutil
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field
import difflib
import tempfile
from datetime import datetime


@dataclass
class DocstringConversion:
    """Represents a docstring conversion."""
    file_path: str
    line_number: int
    node_name: str
    node_type: str
    original: str
    converted: str
    validation_errors: List[str] = field(default_factory=list)


class DocstringConverter(ast.NodeTransformer):
    """AST transformer to convert docstrings from markdown to Google style."""
    
    def __init__(self, source_lines: List[str]):
        self.source_lines = source_lines
        self.conversions: List[DocstringConversion] = []
        
    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Visit function definitions."""
        self._process_docstring(node, "function")
        return self.generic_visit(node)
        
    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        """Visit async function definitions."""
        self._process_docstring(node, "async_function")
        return self.generic_visit(node)
        
    def visit_ClassDef(self, node: ast.ClassDef):
        """Visit class definitions."""
        self._process_docstring(node, "class")
        return self.generic_visit(node)
        
    def visit_Module(self, node: ast.Module):
        """Visit module (file-level docstring)."""
        self._process_docstring(node, "module")
        return self.generic_visit(node)
        
    def _process_docstring(self, node, node_type: str):
        """Process and convert a node's docstring if needed."""
        docstring = ast.get_docstring(node, clean=False)
        if not docstring:
            return
            
        # Check if conversion is needed
        if '```' not in docstring:
            return
            
        # Convert the docstring
        converted = self._convert_docstring(docstring, node_type)
        
        if converted != docstring:
            # Store conversion info
            node_name = getattr(node, 'name', 'module')
            conversion = DocstringConversion(
                file_path="",  # Will be set by caller
                line_number=node.lineno if hasattr(node, 'lineno') else 1,
                node_name=node_name,
                node_type=node_type,
                original=docstring,
                converted=converted
            )
            self.conversions.append(conversion)
            
            # Update the node's docstring
            if isinstance(node.body, list) and node.body:
                first = node.body[0]
                if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant):
                    # Update the docstring node
                    first.value = ast.Constant(value=converted)
                    
    def _convert_docstring(self, docstring: str, node_type: str) -> str:
        """Convert markdown-style code blocks to Google style Examples section."""
        lines = docstring.split('\n')
        converted_lines = []
        in_code_block = False
        code_block_lines = []
        code_block_lang = None
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # Check for code block start
            if line.strip().startswith('```'):
                if not in_code_block:
                    # Starting a code block
                    in_code_block = True
                    code_block_lang = line.strip()[3:].strip() or 'python'
                    code_block_lines = []
                else:
                    # Ending a code block - convert it
                    in_code_block = False
                    
                    # Add the converted code block
                    if code_block_lines:
                        # Add Examples section header if not already present
                        if not any('Example' in l for l in converted_lines[-5:] if l):
                            converted_lines.append('')
                            converted_lines.append('Examples:')
                        
                        # Add code with proper indentation
                        converted_lines.append('    >>> # Example code')
                        for code_line in code_block_lines:
                            if code_line.strip():
                                converted_lines.append('    >>> ' + code_line)
                            else:
                                converted_lines.append('    >>>')
                    
                    code_block_lines = []
                    code_block_lang = None
            elif in_code_block:
                # Inside a code block
                code_block_lines.append(line)
            else:
                # Regular docstring line
                converted_lines.append(line)
            
            i += 1
        
        # Handle unclosed code block
        if in_code_block and code_block_lines:
            if not any('Example' in l for l in converted_lines[-5:] if l):
                converted_lines.append('')
                converted_lines.append('Examples:')
            
            converted_lines.append('    >>> # Example code')
            for code_line in code_block_lines:
                if code_line.strip():
                    converted_lines.append('    >>> ' + code_line)
                else:
                    converted_lines.append('    >>>')
        
        return '\n'.join(converted_lines)


def validate_with_pydocstyle(file_path: Path, specific_line: Optional[int] = None) -> List[str]:
    """Validate a file with pydocstyle and return any errors."""
    try:
        # Run pydocstyle with Google convention
        result = subprocess.run(
            ['pydocstyle', '--convention=google', str(file_path)],
            capture_output=True,
            text=True
        )
        
        errors = []
        if result.stdout:
            # Parse errors
            for line in result.stdout.split('\n'):
                if line.strip() and not line.startswith('Checking'):
                    # If specific_line is provided, only include errors for that line
                    if specific_line:
                        if f':{specific_line}' in line:
                            errors.append(line.strip())
                    else:
                        errors.append(line.strip())
        
        return errors
        
    except subprocess.CalledProcessError as e:
        return [f"Error running pydocstyle: {e}"]
    except FileNotFoundError:
        return ["pydocstyle not found. Install with: pip install pydocstyle"]


def convert_file(file_path: Path, dry_run: bool = True, validate: bool = True) -> List[DocstringConversion]:
    """Convert docstrings in a file from markdown to Google style.
    
    Args:
        file_path: Path to the Python file
        dry_run: If True, don't modify the file, just show what would change
        validate: If True, validate with pydocstyle after conversion
        
    Returns:
        List of conversions made
    """
    print(f"\n{'='*80}")
    print(f"Processing: {file_path}")
    print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    print(f"{'='*80}")
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        original_content = f.read()
        original_lines = original_content.splitlines(keepends=True)
    
    # Parse AST
    try:
        tree = ast.parse(original_content, filename=str(file_path))
    except SyntaxError as e:
        print(f"❌ Syntax error in {file_path}: {e}")
        return []
    
    # Convert docstrings
    converter = DocstringConverter(original_lines)
    new_tree = converter.visit(tree)
    
    # If no conversions needed, return
    if not converter.conversions:
        print("✅ No markdown-style code blocks found.")
        return []
    
    # Set file paths in conversions
    for conv in converter.conversions:
        conv.file_path = str(file_path)
    
    print(f"\n📝 Found {len(converter.conversions)} docstring(s) to convert:")
    for conv in converter.conversions:
        print(f"  - Line {conv.line_number}: {conv.node_type} '{conv.node_name}'")
    
    # Apply conversions to source
    modified_lines = original_lines.copy()
    modified_content = apply_conversions(original_content, converter.conversions)
    
    # Show diff
    print("\n📊 Changes preview:")
    diff = difflib.unified_diff(
        original_content.splitlines(keepends=True),
        modified_content.splitlines(keepends=True),
        fromfile=f"{file_path} (original)",
        tofile=f"{file_path} (converted)",
        lineterm=''
    )
    
    diff_lines = list(diff)
    if diff_lines:
        # Show first 50 lines of diff
        for line in diff_lines[:50]:
            if line.startswith('+'):
                print(f"\033[92m{line}\033[0m", end='')  # Green
            elif line.startswith('-'):
                print(f"\033[91m{line}\033[0m", end='')  # Red
            else:
                print(line, end='')
        
        if len(diff_lines) > 50:
            print(f"\n... ({len(diff_lines) - 50} more lines)")
    
    # Validate if requested
    if validate:
        print("\n🔍 Validation:")
        
        # Write to temp file for validation
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp:
            tmp.write(modified_content)
            tmp_path = Path(tmp.name)
        
        try:
            # Validate converted file
            errors = validate_with_pydocstyle(tmp_path)
            
            if errors:
                print("  ⚠️  Validation warnings (review these):")
                for error in errors[:10]:  # Show first 10
                    print(f"    - {error}")
                if len(errors) > 10:
                    print(f"    ... and {len(errors) - 10} more")
            else:
                print("  ✅ No validation errors!")
                
            # Store validation errors in conversions
            for conv in converter.conversions:
                conv.validation_errors = [e for e in errors if f':{conv.line_number}' in e]
                
        finally:
            tmp_path.unlink()
    
    # Apply changes if not dry run
    if not dry_run:
        # Create backup
        backup_path = file_path.with_suffix(f'.backup.{datetime.now().strftime("%Y%m%d_%H%M%S")}')
        shutil.copy2(file_path, backup_path)
        print(f"\n💾 Backup created: {backup_path}")
        
        # Write modified content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(modified_content)
        print(f"✅ File updated: {file_path}")
    else:
        print(f"\n🔸 DRY RUN - No files modified")
        print(f"  To apply changes, run without --dry-run flag")
    
    return converter.conversions


def apply_conversions(content: str, conversions: List[DocstringConversion]) -> str:
    """Apply docstring conversions to file content."""
    # Simple approach: replace original docstrings with converted ones
    result = content
    
    # Sort conversions by position (reverse to maintain positions)
    sorted_convs = sorted(conversions, key=lambda c: c.line_number, reverse=True)
    
    for conv in sorted_convs:
        # Find and replace the original docstring
        # We need to be careful about quotes (""" or ''')
        
        # Try triple double quotes first
        pattern1 = f'"""{re.escape(conv.original)}"""'
        if pattern1 in result:
            result = result.replace(pattern1, f'"""{conv.converted}"""', 1)
            continue
            
        # Try triple single quotes
        pattern2 = f"'''{re.escape(conv.original)}'''"
        if pattern2 in result:
            result = result.replace(pattern2, f"'''{conv.converted}'''", 1)
            continue
            
        # Try with raw strings
        pattern3 = f'r"""{re.escape(conv.original)}"""'
        if pattern3 in result:
            result = result.replace(pattern3, f'r"""{conv.converted}"""', 1)
            continue
    
    return result


def main():
    """Main entry point for the docstring converter."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Convert markdown docstrings to Google style')
    parser.add_argument('file', help='Python file to convert')
    parser.add_argument('--dry-run', action='store_true', default=True,
                       help='Show what would be changed without modifying files (default: True)')
    parser.add_argument('--apply', action='store_true',
                       help='Actually modify the files (overrides --dry-run)')
    parser.add_argument('--no-validate', action='store_true',
                       help='Skip pydocstyle validation')
    
    args = parser.parse_args()
    
    file_path = Path(args.file)
    
    if not file_path.exists():
        print(f"❌ Error: File {file_path} does not exist")
        sys.exit(1)
        
    if not file_path.suffix == '.py':
        print(f"❌ Error: File {file_path} is not a Python file")
        sys.exit(1)
    
    # Determine if dry run
    dry_run = not args.apply
    
    # Convert the file
    conversions = convert_file(
        file_path, 
        dry_run=dry_run,
        validate=not args.no_validate
    )
    
    # Exit code based on whether conversions were needed
    if conversions:
        sys.exit(1 if dry_run else 0)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()