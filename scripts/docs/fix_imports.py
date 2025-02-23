#!/usr/bin/env python3
"""
Script to fix import issues in Sphinx documentation.
Place this in docs/scripts/fix_imports.py
"""

import os
from pathlib import Path
import sys

def create_module_stubs():
    """Create stub files for missing modules."""
    src_dir = Path('src/haive')
    if not src_dir.exists():
        print(f"❌ Source directory {src_dir} not found!")
        return

    # Create stubs for all modules
    modules = [
        'agents',
        'agents.base',
        'agents.react_agent',
        'agents.plan_and_execute',
        'agents.tot',
        'agents.self_discover',
        'agents.summarizer',
        'agents.web_nav',
        'core',
        'core.aug_llm',
        'core.models',
        'core.tools',
        'flstaesr',
        'flstaesr.annotate',
        'flstaesr.transform',
        'flstaesr.load',
    ]

    for module in modules:
        # Create directory structure
        module_path = src_dir / Path(*module.split('.'))
        module_path.mkdir(parents=True, exist_ok=True)

        # Create __init__.py if it doesn't exist
        init_file = module_path / '__init__.py'
        if not init_file.exists():
            init_file.write_text('"""Placeholder for auto-generated documentation."""\n')

def update_conf_py():
    """Update conf.py with correct settings."""
    conf_path = Path('docs/conf.py')
    if not conf_path.exists():
        print("❌ conf.py not found!")
        return

    content = conf_path.read_text()
    
    # Add necessary modifications
    updates = {
        "import sys": "import sys\nsys.path.insert(0, os.path.abspath('../src'))",
        "extensions = [": "extensions = [\n    'sphinx.ext.autodoc',\n    'sphinx.ext.viewcode',",
        "autodoc_mock_imports = [": """autodoc_mock_imports = [
    'langchain',
    'langchain_core',
    'langchain_community',
    'pydantic',
    'openai',
    'anthropic',
    'numpy',
    'pandas',
]"""
    }

    for old, new in updates.items():
        if old in content and new not in content:
            content = content.replace(old, new)

    conf_path.write_text(content)

def main():
    """Main entry point."""
    print("🔧 Fixing import issues...")
    
    # Create module stubs
    create_module_stubs()
    
    # Update conf.py
    update_conf_py()
    
    print("✅ Import fixes complete!")

if __name__ == "__main__":
    main()