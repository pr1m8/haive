#!/usr/bin/env python3
"""
Ensures all necessary RST files exist for documentation.
This script scans your Python package and automatically creates
RST documentation files for all modules, maintaining proper structure.
"""

import os
from pathlib import Path
import importlib
import inspect
import sys
import logging
from typing import Dict, List, Set

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

class DocFileManager:
    """Manages documentation file creation and structure."""
    
    def __init__(self, src_path: str = 'src/haive', docs_path: str = 'docs/api'):
        self.base_path = Path(src_path)
        self.docs_path = Path(docs_path)
        self.modules_seen: Set[str] = set()
        
        # Add source directory to Python path
        sys.path.insert(0, str(self.base_path.parent))

    def get_module_contents(self, module_name: str) -> Dict[str, List[str]]:
        """Extract classes and functions from a module."""
        try:
            module = importlib.import_module(module_name)
            return {
                'classes': [
                    name for name, obj in inspect.getmembers(module, inspect.isclass)
                    if obj.__module__ == module.__name__
                ],
                'functions': [
                    name for name, obj in inspect.getmembers(module, inspect.isfunction)
                    if obj.__module__ == module.__name__
                ],
                'submodules': [
                    name for name, obj in inspect.getmembers(module)
                    if inspect.ismodule(obj) and obj.__name__.startswith(module_name)
                ]
            }
        except ImportError as e:
            logger.warning(f"Could not import {module_name}: {e}")
            return {'classes': [], 'functions': [], 'submodules': []}
        except Exception as e:
            logger.error(f"Error processing {module_name}: {e}")
            return {'classes': [], 'functions': [], 'submodules': []}

    def create_rst_content(self, module_name: str, contents: Dict[str, List[str]]) -> str:
        """Generate RST content for a module."""
        title = module_name.split('.')[-1].replace('_', ' ').title()
        lines = [
            title,
            '=' * len(title),
            '',
            f'.. module:: {module_name}',
            '',
            '.. currentmodule:: ' + module_name,
            '',
        ]

        # Add module description if available
        try:
            module = importlib.import_module(module_name)
            if module.__doc__:
                lines.extend([module.__doc__.strip(), '', ''])
        except ImportError:
            pass

        # Add classes section
        if contents['classes']:
            lines.extend([
                'Classes',
                '-------',
                '',
                '.. autosummary::',
                '   :toctree: _autosummary',
                '   :template: custom-class-template.rst',
                '',
            ])
            lines.extend(f'   {cls}' for cls in sorted(contents['classes']))
            lines.append('')

        # Add functions section
        if contents['functions']:
            lines.extend([
                'Functions',
                '---------',
                '',
                '.. autosummary::',
                '   :toctree: _autosummary',
                '',
            ])
            lines.extend(f'   {func}' for func in sorted(contents['functions']))
            lines.append('')

        # Add submodules section
        if contents['submodules']:
            lines.extend([
                'Submodules',
                '----------',
                '',
                '.. toctree::',
                '   :maxdepth: 1',
                '',
            ])
            lines.extend(f'   {sub}' for sub in sorted(contents['submodules']))
            lines.append('')

        return '\n'.join(lines)

    def create_index_rst(self, module_name: str, submodules: List[str]) -> str:
        """Create index.rst content for a package."""
        title = module_name.split('.')[-1].replace('_', ' ').title()
        lines = [
            title,
            '=' * len(title),
            '',
            f'.. module:: {module_name}',
            '',
        ]

        if submodules:
            lines.extend([
                'Submodules',
                '----------',
                '',
                '.. toctree::',
                '   :maxdepth: 2',
                '',
            ])
            lines.extend(f'   {sub}' for sub in sorted(submodules))
            lines.append('')

        return '\n'.join(lines)

    def ensure_rst_file(self, module_path: Path) -> None:
        """Ensure RST documentation exists for a module."""
        # Convert path to module name
        rel_path = module_path.relative_to(self.base_path.parent)
        module_name = str(rel_path).replace('/', '.')[:-3]  # Remove .py extension
        
        if module_name in self.modules_seen:
            return
        self.modules_seen.add(module_name)

        # Get module contents
        contents = self.get_module_contents(module_name)
        
        # Determine RST file path
        if module_path.name == '__init__.py':
            rst_path = self.docs_path / module_path.parent.relative_to(self.base_path) / 'index.rst'
        else:
            rst_path = self.docs_path / module_path.relative_to(self.base_path).with_suffix('.rst')

        # Create directory if needed
        rst_path.parent.mkdir(parents=True, exist_ok=True)

        # Create appropriate RST content
        if module_path.name == '__init__.py':
            content = self.create_index_rst(module_name, contents['submodules'])
        else:
            content = self.create_rst_content(module_name, contents)

        # Write the file
        rst_path.write_text(content)
        logger.info(f"Created/updated {rst_path}")

    def process_directory(self) -> None:
        """Process all Python files in the directory."""
        # Process all Python files
        for path in self.base_path.rglob('*.py'):
            if any(part.startswith('.') for part in path.parts):
                continue
            self.ensure_rst_file(path)

def main():
    """Main entry point."""
    try:
        manager = DocFileManager()
        manager.process_directory()
        logger.info("✅ Documentation files generated successfully!")
    except Exception as e:
        logger.error(f"❌ Error generating documentation files: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()