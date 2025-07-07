"""Fix autosummary module detection for Haive packages.

This extension ensures that haive.core.*, haive.agents.*, etc. submodules
are correctly recognized as modules rather than data attributes.
"""

import os
from pathlib import Path
from sphinx.ext.autosummary import Autosummary
from sphinx.ext.autosummary.generate import AutosummaryRenderer, generate_autosummary_docs
import logging

logger = logging.getLogger(__name__)


def is_haive_module(name):
    """Check if a name represents a haive module that should be treated as a module."""
    module_patterns = [
        'haive.core.engine',
        'haive.core.graph', 
        'haive.core.schema',
        'haive.core.persistence',
        'haive.core.registry',
        'haive.core.tools',
        'haive.agents.base',
        'haive.agents.simple',
        'haive.agents.react',
        'haive.agents.rag',
        'haive.agents.multi',
        'haive.agents.planning',
        'haive.tools.api',
        'haive.tools.search',
        'haive.tools.math',
        'haive.tools.data',
        'haive.tools.code',
        'haive.tools.utility',
    ]
    return name in module_patterns or any(name.startswith(p + '.') for p in module_patterns)


def fix_generated_file(filepath):
    """Fix incorrectly generated autosummary files."""
    if not os.path.exists(filepath):
        return
        
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Extract module name from the file
    lines = content.strip().split('\n')
    if len(lines) < 3:
        return
        
    # First line should be the title
    title_line = lines[0]
    if not title_line.startswith('haive.'):
        return
        
    module_name = title_line.strip('﻿').strip()
    
    # Check if this should be a module
    if not is_haive_module(module_name):
        return
        
    # Check if it's using autodata instead of automodule
    if '.. autodata::' in content:
        logger.info(f"Fixing {filepath}: converting autodata to automodule for {module_name}")
        
        # Generate correct content
        underline = '=' * len(module_name)
        new_content = f"""{module_name}
{underline}

.. automodule:: {module_name}
   :members:
   :undoc-members:
   :show-inheritance:
"""
        
        with open(filepath, 'w') as f:
            f.write(new_content)


def process_autosummary_toc(app, what, name, obj, options, lines):
    """Process autosummary table of contents to fix module detection."""
    if what == 'module' and is_haive_module(name):
        # Ensure it's treated as a module
        if hasattr(app.env, 'autosummary_context'):
            app.env.autosummary_context[name] = {'objtype': 'module'}


def fix_autosummary_files(app, exception):
    """Fix generated autosummary files after build."""
    if exception:
        return
        
    # Find generated autosummary files
    source_dir = Path(app.srcdir)
    api_dir = source_dir / 'api' / 'generated'
    
    if api_dir.exists():
        for rst_file in api_dir.glob('*.rst'):
            fix_generated_file(str(rst_file))


def setup(app):
    """Setup the extension."""
    app.connect('autodoc-process-docstring', process_autosummary_toc)
    app.connect('build-finished', fix_autosummary_files)
    
    # Override autosummary behavior
    original_get_items = Autosummary.get_items
    
    def patched_get_items(self, names):
        """Patched get_items to ensure modules are recognized."""
        items = original_get_items(self, names)
        
        # Fix items that should be modules
        fixed_items = []
        for name, sig, summary, real_name in items:
            if is_haive_module(real_name or name):
                # Force it to be treated as a module
                fixed_items.append((name, '', summary, real_name))
            else:
                fixed_items.append((name, sig, summary, real_name))
        
        return fixed_items
    
    Autosummary.get_items = patched_get_items
    
    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }