#!/usr/bin/env python3
"""
Ensures all necessary RST files exist for documentation.
"""

import os
from pathlib import Path
import importlib
import inspect

def get_module_contents(module_name):
    """Get all classes and functions from a module."""
    try:
        module = importlib.import_module(module_name)
        return {
            'classes': [name for name, obj in inspect.getmembers(module, inspect.isclass)
                       if obj.__module__ == module.__name__],
            'functions': [name for name, obj in inspect.getmembers(module, inspect.isfunction)
                        if obj.__module__ == module.__name__]
        }
    except ImportError:
        return {'classes': [], 'functions': []}

def create_rst_file(path, module_name, contents):
    """Create an RST file for a module."""
    with open(path, 'w') as f:
        # Write header
        title = module_name.split('.')[-1].replace('_', ' ').title()
        f.write(f'{title}\n{"=" * len(title)}\n\n')
        
        # Write module directive
        f.write(f'.. module:: {module_name}\n\n')
        
        # Write classes section if any
        if contents['classes']:
            f.write('Classes\n-------\n\n')
            f.write('.. autosummary::\n   :toctree: _autosummary\n   :template: custom-class-template.rst\n\n')
            for class_name in contents['classes']:
                f.write(f'   {class_name}\n')
            f.write('\n')
        
        # Write functions section if any
        if contents['functions']:
            f.write('Functions\n---------\n\n')
            f.write('.. autosummary::\n   :toctree: _autosummary\n\n')
            for func_name in contents['functions']:
                f.write(f'   {func_name}\n')
            f.write('\n')

def ensure_rst_files(base_path='src/haive', docs_path='docs/api'):
    """Ensure RST files exist for all modules."""
    base = Path(base_path)
    docs = Path(docs_path)
    
    for path in base.rglob('*.py'):
        if path.name == '__init__.py':
            continue
            
        # Get relative path and convert to module name
        rel_path = path.relative_to(base.parent)
        module_name = str(rel_path).replace('/', '.')[:-3]
        
        # Create corresponding RST file path
        rst_path = docs / f'{module_name}.rst'
        rst_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create# Create API index structure
mkdir -p docs/api/{agents,core,flstaesr}

# Create main API index
cat > docs/api/index.rst << 'EOL'
API Reference
============

.. toctree::
   :maxdepth: 2
   :caption: API Documentation:

   agents/index
   core/index
   flstaesr/index
