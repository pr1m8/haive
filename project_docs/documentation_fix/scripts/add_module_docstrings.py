#!/usr/bin/env python3
"""Auto-generate module docstrings for Python files."""

import os
import re
from pathlib import Path

def generate_module_docstring(file_path: Path) -> str:
    """Generate appropriate module docstring based on file content.
    
    Args:
        file_path: Path to the Python file
        
    Returns:
        Generated docstring with triple quotes and newlines
    """
    
    # Read file content
    content = file_path.read_text()
    
    # Extract classes and functions for description
    classes = re.findall(r'class\s+(\w+)', content)
    functions = re.findall(r'def\s+(\w+)', content)
    
    # Generate description based on path and content
    module_name = file_path.stem
    relative_path = str(file_path).replace('/home/will/Projects/haive/backend/haive/packages/haive-core/src/', '')
    
    # Create contextual description
    if 'engine' in str(file_path):
        category = "engine"
    elif 'schema' in str(file_path):
        category = "schema"
    elif 'graph' in str(file_path):
        category = "graph"
    elif 'utils' in str(file_path):
        category = "utility"
    elif 'models' in str(file_path):
        category = "model"
    elif 'config' in str(file_path):
        category = "configuration"
    else:
        category = "core"
    
    docstring = f'"""{module_name.title()} {category} module.\n\n'
    docstring += f'This module provides {module_name.replace("_", " ")} functionality for the Haive framework.\n'
    
    if classes:
        docstring += f"\nClasses:\n"
        for cls in classes[:3]:  # Limit to top 3
            docstring += f"    {cls}: {cls} implementation.\n"
    
    if functions:
        docstring += f"\nFunctions:\n"
        for func in functions[:3]:  # Limit to top 3
            if not func.startswith('_'):  # Skip private functions
                docstring += f"    {func}: {func.replace('_', ' ').title()} functionality.\n"
    
    docstring += '"""\n\n'
    return docstring

def add_module_docstrings(directory: Path):
    """Add module docstrings to files missing them.
    
    Args:
        directory: Directory to process recursively
    """
    files_processed = 0
    files_updated = 0
    
    for py_file in directory.rglob("*.py"):
        files_processed += 1
        
        try:
            content = py_file.read_text()
            
            # Skip if already has module docstring
            if content.strip().startswith('"""') or content.strip().startswith("'''"):
                continue
                
            # Skip __init__.py files (handled separately)
            if py_file.name == "__init__.py":
                continue
                
            # Skip files that are mostly imports
            lines = content.strip().split('\n')
            non_import_lines = [line for line in lines if not line.startswith(('import ', 'from ')) and line.strip()]
            if len(non_import_lines) < 5:  # Skip very small files
                continue
                
            # Generate and prepend docstring
            docstring = generate_module_docstring(py_file)
            new_content = docstring + content
            
            py_file.write_text(new_content)
            print(f"✅ Added module docstring to {py_file.relative_to(directory)}")
            files_updated += 1
            
        except Exception as e:
            print(f"❌ Error processing {py_file}: {e}")
    
    print(f"\n📊 Summary:")
    print(f"   Files processed: {files_processed}")
    print(f"   Files updated: {files_updated}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        target_dir = Path(sys.argv[1])
    else:
        target_dir = Path("/home/will/Projects/haive/backend/haive/packages/haive-core/src")
    
    print(f"🚀 Adding module docstrings to: {target_dir}")
    add_module_docstrings(target_dir)
    print("✨ Module docstring generation complete!")