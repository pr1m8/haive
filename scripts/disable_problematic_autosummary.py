#!/usr/bin/env python3
"""Disable problematic autosummary sections that cause build hangs."""

import os
import re
from pathlib import Path

def disable_autosummary_in_file(file_path):
    """Comment out autosummary directives in a file."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Pattern to match autosummary blocks
    pattern = r'(\.\. autosummary::\s*\n(?:\s+:\S+\s*\n)*(?:\s*\n)*(?:\s+\S+\s*\n)*)'
    
    def comment_out_match(match):
        lines = match.group(1).split('\n')
        commented_lines = []
        for line in lines:
            if line.strip():
                commented_lines.append('.. ' + line)
            else:
                commented_lines.append(line)
        return '\n'.join(commented_lines)
    
    # Replace autosummary blocks with commented versions
    new_content = re.sub(pattern, comment_out_match, content, flags=re.MULTILINE)
    
    if new_content != content:
        with open(file_path, 'w') as f:
            f.write(new_content)
        return True
    return False

def main():
    """Disable autosummary in problematic files."""
    docs_dir = Path("/home/will/Projects/haive/backend/haive/docs/source")
    
    # Files known to cause issues
    problematic_files = [
        "api/haive/core/models/llm.rst",
        "api/haive/core/engine/vectorstore.rst",
        "api/haive/core/engine/retriever.rst", 
        "api/haive/core/engine/embedding.rst",
    ]
    
    fixed_count = 0
    for file_path in problematic_files:
        full_path = docs_dir / file_path
        if full_path.exists():
            if disable_autosummary_in_file(full_path):
                print(f"Disabled autosummary in: {file_path}")
                fixed_count += 1
            else:
                print(f"No changes needed in: {file_path}")
        else:
            print(f"File not found: {file_path}")
    
    print(f"\nDisabled autosummary in {fixed_count} files.")

if __name__ == "__main__":
    main()