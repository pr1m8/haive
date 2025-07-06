#!/usr/bin/env python3
"""
Generate key module documentation - focused on main public APIs only.

This creates a targeted set of module pages for the most important APIs,
avoiding the performance issues of generating 900+ files.
"""

import logging
from pathlib import Path
from typing import List, Dict

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Project structure
PROJECT_ROOT = Path(__file__).parent.parent
DOCS_SOURCE_DIR = PROJECT_ROOT / "docs" / "source"
MODULES_DIR = DOCS_SOURCE_DIR / "api" / "modules"

# Key modules to generate (public APIs only)
KEY_MODULES = {
    "haive-core": [
        "haive.core",
        "haive.core.engine", 
        "haive.core.graph",
        "haive.core.schema", 
        "haive.core.persistence",
        "haive.core.registry",
        "haive.core.tools",
        "haive.core.config",
    ],
    "haive-agents": [
        "haive.agents",
        "haive.agents.simple",
        "haive.agents.react", 
        "haive.agents.rag",
        "haive.agents.multi",
        "haive.agents.planning",
        "haive.agents.conversation",
        "haive.agents.research",
        "haive.agents.base",
    ],
    "haive-tools": [
        "haive.tools",
        "haive.tools.search",
        "haive.tools.api",
        "haive.tools.data",
        "haive.tools.code", 
        "haive.tools.math",
        "haive.tools.utility",
    ],
    "haive-games": [
        "haive.games",
        "haive.games.chess",
        "haive.games.tic_tac_toe",
        "haive.games.checkers",
        "haive.games.go",
        "haive.games.connect4",
        "haive.games.cards",
        "haive.games.poker",
    ],
    "haive-mcp": [
        "haive.mcp",
        "haive.mcp.agents",
        "haive.mcp.config",
        "haive.mcp.manager",
        "haive.mcp.discovery",
        "haive.mcp.servers",
    ],
    "haive-prebuilt": [
        "haive.prebuilt",
        "haive.prebuilt.research",
        "haive.prebuilt.content",
        "haive.prebuilt.business",
        "haive.prebuilt.academic",
    ],
    "haive-dataflow": [
        "haive.dataflow",
        "haive.dataflow.api",
        "haive.dataflow.auth",
        "haive.dataflow.db",
        "haive.dataflow.persistence",
    ],
}

def create_module_rst(module_name: str) -> str:
    """Create RST content for a key module."""
    title = module_name
    underline = "=" * len(title)
    
    rst_content = f"""{title}
{underline}

.. py:module:: {module_name}

.. currentmodule:: {module_name}

.. raw:: html

   <div class="module-path" style="margin-bottom: 1rem; color: var(--color-foreground-secondary);">
      <code>{module_name}</code>
   </div>

.. automodule:: {module_name}
   :members:
   :undoc-members:
   :show-inheritance:
   :inherited-members:
   :special-members: __init__, __call__, __new__
   :imported-members:
   :exclude-members: logger
"""
    
    return rst_content

def main():
    """Generate key module documentation only."""
    logger.info("Generating key module documentation...")
    
    # Clean existing modules directory
    if MODULES_DIR.exists():
        import shutil
        shutil.rmtree(MODULES_DIR)
        logger.info("Cleaned existing modules directory")
    
    # Create fresh modules directory
    MODULES_DIR.mkdir(parents=True, exist_ok=True)
    
    generated_count = 0
    
    # Generate key modules for each package
    for package_name, modules in KEY_MODULES.items():
        logger.info(f"Generating key modules for {package_name}...")
        
        for module_name in modules:
            try:
                # Create RST content
                rst_content = create_module_rst(module_name)
                
                # Write to file
                rst_filename = f"{module_name}.rst"
                rst_path = MODULES_DIR / rst_filename
                
                rst_path.write_text(rst_content, encoding='utf-8')
                generated_count += 1
                
                logger.info(f"✅ Generated: {rst_filename}")
                
            except Exception as e:
                logger.error(f"Failed to generate {module_name}: {e}")
    
    # Create marker file
    marker_file = MODULES_DIR / ".generated"
    marker_file.touch()
    
    logger.info(f"✅ Generated {generated_count} key module files")
    logger.info(f"📁 Files saved to: {MODULES_DIR}")
    logger.info("🚀 Ready for fast documentation build!")
    
    return 0

if __name__ == "__main__":
    exit(main())