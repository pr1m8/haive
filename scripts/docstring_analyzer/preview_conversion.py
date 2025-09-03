#!/usr/bin/env python3
"""Preview docstring conversion from markdown to Google style."""

import sys
import re
from pathlib import Path
from typing import Tuple


def convert_markdown_to_google(content: str) -> Tuple[str, int]:
    """Convert markdown code blocks in docstrings to Google style.
    
    Returns:
        Tuple of (converted_content, number_of_changes)
    """
    changes = 0
    
    # Find all docstrings (triple quotes)
    def process_docstring(match):
        nonlocal changes
        docstring = match.group(0)
        quotes = docstring[:3]
        inner_content = docstring[3:-3]
        
        # Check if it contains markdown code blocks
        if '```' not in inner_content:
            return docstring
        
        # Convert markdown blocks to Google style
        lines = inner_content.split('\n')
        converted_lines = []
        in_code_block = False
        code_lines = []
        
        for line in lines:
            if line.strip().startswith('```python'):
                in_code_block = True
                code_lines = []
                changes += 1
            elif line.strip() == '```':
                in_code_block = False
                # Add the converted example
                if code_lines:
                    # Add Examples header if needed
                    if converted_lines and not any('Examples:' in l for l in converted_lines[-5:]):
                        converted_lines.append('')
                        converted_lines.append('Examples:')
                    # Add code with >>> prefix
                    for code_line in code_lines:
                        if code_line.strip():
                            converted_lines.append('    >>> ' + code_line)
                        else:
                            converted_lines.append('    >>>')
                code_lines = []
            elif in_code_block:
                code_lines.append(line)
            else:
                converted_lines.append(line)
        
        # Reconstruct docstring
        return quotes + '\n'.join(converted_lines) + quotes
    
    # Process all docstrings
    pattern = r'""".*?"""|\'\'\'.*?\'\'\''
    result = re.sub(pattern, process_docstring, content, flags=re.DOTALL)
    
    return result, changes


def show_google_style_rules():
    """Show Google style docstring rules."""
    print("\n" + "="*80)
    print("📚 GOOGLE STYLE DOCSTRING RULES")
    print("="*80)
    print("""
1. **Summary Line**: First line should be a brief summary ending with period.
   
2. **Blank Line**: After summary (if multi-line docstring).

3. **Sections** (in order):
   - Args: Function/method arguments
   - Returns: Return value description  
   - Yields: For generators
   - Raises: Exceptions that can be raised
   - Note/Notes: Additional information
   - Example/Examples: Usage examples with >>> prefix
   - Attributes: For classes
   - See Also: Related functions/classes

4. **Code Examples Format**:
   Instead of markdown blocks:
   ```python
   code here
   ```
   
   Use Google style:
   Examples:
       >>> code here
       >>> more code
       
5. **Indentation**: 
   - Section headers at same indent as quotes
   - Section content indented 4 spaces
   - Code examples indented 4 spaces with >>> prefix
""")


def preview_file(file_path: Path):
    """Preview conversion for a single file."""
    print(f"\n{'='*80}")
    print(f"📄 File: {file_path}")
    print(f"{'='*80}")
    
    with open(file_path, 'r') as f:
        original = f.read()
    
    # Check for markdown blocks
    if '```' not in original:
        print("✅ No markdown code blocks found")
        return
    
    # Convert
    converted, num_changes = convert_markdown_to_google(original)
    
    if num_changes == 0:
        print("✅ No markdown blocks in docstrings")
        return
    
    print(f"\n⚠️  Found {num_changes} markdown block(s) to convert\n")
    
    # Show a sample of the changes
    original_lines = original.splitlines()
    converted_lines = converted.splitlines()
    
    # Find first difference
    for i, (orig, conv) in enumerate(zip(original_lines, converted_lines)):
        if orig != conv:
            # Show context around the change
            start = max(0, i - 3)
            end = min(len(original_lines), i + 15)
            
            print("🔴 ORIGINAL (lines {}-{}):\n".format(start+1, end+1))
            for j in range(start, end):
                if j < len(original_lines):
                    line = original_lines[j]
                    if '```' in line:
                        print(f"    {j+1:4}: ⚠️  {line}")
                    else:
                        print(f"    {j+1:4}: {line}")
            
            print("\n🟢 CONVERTED (Google style):\n")
            for j in range(start, end):
                if j < len(converted_lines):
                    line = converted_lines[j]
                    if '>>>' in line or 'Examples:' in line:
                        print(f"    {j+1:4}: ✅ {line}")
                    else:
                        print(f"    {j+1:4}: {line}")
            
            break
    
    # Run pydocstyle check
    print("\n" + "="*80)
    print("🔍 GOOGLE STYLE VALIDATION")
    print("="*80)
    
    # Save converted to temp file and validate
    import tempfile
    import subprocess
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp:
        tmp.write(converted)
        tmp_path = tmp.name
    
    try:
        result = subprocess.run(
            ['pydocstyle', '--convention=google', tmp_path],
            capture_output=True,
            text=True
        )
        
        if result.stdout:
            print("\n⚠️  Remaining style issues to address:")
            for line in result.stdout.splitlines()[:10]:
                if line and not line.startswith('Checking'):
                    # Parse error code
                    if 'D' in line and ':' in line:
                        parts = line.split(':', 2)
                        if len(parts) > 2:
                            error_desc = parts[2].strip()
                            print(f"  - {error_desc}")
        else:
            print("✅ Passes Google style validation!")
            
    finally:
        Path(tmp_path).unlink()


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python preview_conversion.py <file.py>")
        print("\nThis will show:")
        print("  1. Google style rules")
        print("  2. Preview of conversions")
        print("  3. Validation results")
        sys.exit(1)
    
    file_path = Path(sys.argv[1])
    
    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        sys.exit(1)
    
    # Show rules
    show_google_style_rules()
    
    # Preview conversion
    preview_file(file_path)
    
    print("\n" + "="*80)
    print("💡 TO APPLY CHANGES:")
    print("="*80)
    print(f"python scripts/docstring_analyzer/convert_docstrings.py {file_path} --apply")
    print("\nThis will:")
    print("  1. Create a backup")
    print("  2. Apply the conversion")
    print("  3. Validate with pydocstyle")


if __name__ == "__main__":
    main()