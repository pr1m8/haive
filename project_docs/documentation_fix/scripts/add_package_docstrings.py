#!/usr/bin/env python3
"""Auto-generate package docstrings for __init__.py files."""

import os
from pathlib import Path

def generate_package_docstring(init_file: Path) -> str:
    """Generate package docstring based on directory structure.
    
    Args:
        init_file: Path to the __init__.py file
        
    Returns:
        Generated docstring with triple quotes and newlines
    """
    
    package_dir = init_file.parent
    package_name = package_dir.name
    
    # Count submodules and subpackages
    py_files = [f for f in package_dir.glob("*.py") if f.name != "__init__.py"]
    subpackages = [d for d in package_dir.iterdir() if d.is_dir() and (d / "__init__.py").exists()]
    
    # Generate contextual description
    if package_name in ['engine', 'engines']:
        description = "processing engines"
    elif package_name in ['schema', 'schemas']:
        description = "schema definitions and validation"
    elif package_name in ['graph', 'graphs']:
        description = "graph building and management"
    elif package_name in ['models', 'model']:
        description = "data models and types"
    elif package_name in ['utils', 'utilities']:
        description = "utility functions and helpers"
    elif package_name in ['config', 'configuration']:
        description = "configuration management"
    elif package_name in ['tools', 'tool']:
        description = "tool implementations"
    elif package_name in ['mixins', 'mixin']:
        description = "reusable mixin classes"
    elif package_name in ['types', 'typing']:
        description = "type definitions and protocols"
    elif package_name in ['providers', 'provider']:
        description = "service provider implementations"
    else:
        description = f"{package_name.replace('_', ' ')} functionality"
    
    docstring = f'"""{package_name.title()} package.\n\n'
    docstring += f"This package provides {description} for the Haive framework.\n"
    
    if py_files:
        docstring += f"\nModules:\n"
        for py_file in sorted(py_files)[:5]:  # Limit to top 5
            module_name = py_file.stem
            docstring += f"    {module_name}: {module_name.replace('_', ' ').title()} implementation.\n"
    
    if subpackages:
        docstring += f"\nSubpackages:\n"
        for subpkg in sorted(subpackages)[:5]:  # Limit to top 5
            docstring += f"    {subpkg.name}: {subpkg.name.replace('_', ' ').title()} functionality.\n"
    
    # Add usage example for important packages
    if package_name in ['engine', 'schema', 'graph']:
        docstring += f"\nExample:\n"
        docstring += f"    >>> from haive.core.{package_name} import *\n"
        docstring += f"    >>> # Use {package_name} components\n"
    
    docstring += '"""\n\n'
    return docstring

def add_package_docstrings(directory: Path):
    """Add package docstrings to __init__.py files.
    
    Args:
        directory: Directory to process recursively
    """
    files_processed = 0
    files_updated = 0
    
    for init_file in directory.rglob("__init__.py"):
        files_processed += 1
        
        try:
            content = init_file.read_text()
            
            # Skip if already has docstring
            if content.strip().startswith('"""') or content.strip().startswith("'''"):
                continue
            
            # Skip very minimal __init__.py files (just imports)
            meaningful_lines = [line for line in content.split('\n') if line.strip() and not line.strip().startswith('#')]
            if len(meaningful_lines) == 0:  # Empty file
                continue
                
            # Generate and prepend docstring
            docstring = generate_package_docstring(init_file)
            new_content = docstring + content
            
            init_file.write_text(new_content)
            print(f"✅ Added package docstring to {init_file.relative_to(directory)}")
            files_updated += 1
            
        except Exception as e:
            print(f"❌ Error processing {init_file}: {e}")
    
    print(f"\n📊 Summary:")
    print(f"   Files processed: {files_processed}")
    print(f"   Files updated: {files_updated}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        target_dir = Path(sys.argv[1])
    else:
        target_dir = Path("/home/will/Projects/haive/backend/haive/packages/haive-core/src")
    
    print(f"🚀 Adding package docstrings to: {target_dir}")
    add_package_docstrings(target_dir)
    print("✨ Package docstring generation complete!")