#!/usr/bin/env python3
"""Restructure documentation navigation to use haive as root with consistent module-based pattern.

Navigation structure:
/api/haive/
    /core/
        /engine/
            /base.html
            /aug_llm.html
        /schema/
            /state_schema.html
    /agents/
        /base/
            /mixins.html
        /simple/
            /structured.html
"""

import os
from pathlib import Path
import shutil
import textwrap
from typing import Dict, List, Set


# Paths
DOCS_SOURCE = Path("/home/will/Projects/haive/backend/haive/docs/source/api")
PACKAGES_DIR = Path("/home/will/Projects/haive/backend/haive/packages")

# Package configurations with flattened structure
HAIVE_STRUCTURE = {
    "core": {
        "title": "Core",
        "description": "Core infrastructure and utilities",
        "icon": "🏗️",
        "modules": {
            "engine": [
                "base",
                "aug_llm",
                "document",
                "agent",
                "embedding",
                "retriever",
                "vectorstore",
                "tool",
            ],
            "schema": ["state_schema", "schema_composer", "compatibility", "prebuilt"],
            "graph": [
                "state_graph",
                "node",
                "patterns",
                "routers",
                "branches",
                "utils",
            ],
            "persistence": ["store", "handlers", "factory"],
            "registry": ["base", "decorators", "manager"],
            "common": ["mixins", "models", "types"],
            "config": [],
            "logging": [],
            "models": ["llm", "embeddings", "retriever", "vectorstore"],
            "runtime": ["base", "extension"],
            "types": [],
            "ui": [],
            "utils": [],
        },
    },
    "agents": {
        "title": "Agents",
        "description": "Pre-built agent implementations",
        "icon": "🤖",
        "modules": {
            "base": ["mixins"],
            "simple": ["structured", "v2"],
            "conversation": [
                "base",
                "collaborative",
                "debate",
                "directed",
                "round_robin",
                "social_media",
            ],
            "rag": [
                "base",
                "adaptive_rag",
                "self_rag",
                "multi_strategy",
                "hyde",
                "db_rag",
            ],
            "react": [],
            "reasoning_and_critique": [
                "lats",
                "reflection",
                "reflexion",
                "tot",
                "mcts",
                "self_discover",
            ],
            "multi": ["sequential"],
            "planning": ["plan_and_execute", "llm_compiler", "rewoo"],
            "research": ["person", "storm", "perplexity"],
        },
    },
    "tools": {
        "title": "Tools",
        "description": "Tools and utilities for agents",
        "icon": "🔧",
        "modules": {
            "api": [],
            "code": [],
            "data": [],
            "math": [],
            "search": [],
            "utility": [],
        },
    },
    "games": {
        "title": "Games",
        "description": "Game environments for agents",
        "icon": "🎮",
        "modules": {},
    },
    "dataflow": {
        "title": "Dataflow",
        "description": "Data processing pipelines",
        "icon": "🔄",
        "modules": {},
    },
    "prebuilt": {
        "title": "Prebuilt",
        "description": "Pre-configured solutions",
        "icon": "📦",
        "modules": {},
    },
    "mcp": {
        "title": "MCP",
        "description": "Model Context Protocol integration",
        "icon": "🔌",
        "modules": {},
    },
}


def create_haive_root_index() -> str:
    """Create the root haive index page."""
    # Create package grid
    grid_items = []
    for package_name, package_info in HAIVE_STRUCTURE.items():
        grid_items.append(
            f"""
   .. grid-item-card:: {package_info['icon']} **Haive {package_info['title']}**
      :link: {package_name}/index
      :link-type: doc

      {package_info['description']}"""
        )

    content = f"""Haive API Reference
===================

The complete API reference for the Haive framework.

Packages
--------

.. grid:: 1 2 2 3
   :gutter: 3
{"".join(grid_items)}

.. toctree::
   :maxdepth: 4
   :caption: API Reference
   :hidden:

   core/index
   agents/index
   tools/index
   games/index
   dataflow/index
   prebuilt/index
   mcp/index

Navigation
----------

The API documentation is organized hierarchically:

- **haive** (root)

  - **core** → engine → base, aug_llm, document...
  - **agents** → simple → structured, v2...
  - **tools** → search, math, api...

Each level provides both an overview and direct access to submodules.

Quick Links
-----------

* :ref:`genindex` - Complete index of all modules, classes, and functions
* :ref:`modindex` - Quick module finder
* :ref:`search` - Search the documentation
"""
    return content


def create_package_index(package_name: str, package_info: dict) -> str:
    """Create index page for a package (e.g., haive/core/index.rst)."""
    # Create module grid
    grid_items = []
    for module_name, submodules in package_info["modules"].items():
        module_title = module_name.replace("_", " ").title()
        submodule_count = len(submodules)
        desc = f"{submodule_count} submodules" if submodule_count > 0 else "Core module"

        grid_items.append(
            f"""
   .. grid-item-card:: **{module_title}**
      :link: {module_name}/index
      :link-type: doc

      {desc}"""
        )

    content = f"""Haive {package_info['title']}
{'=' * (6 + len(package_info['title']))}

{package_info['description']}

Modules
-------

.. grid:: 1 2 2 3
   :gutter: 3
{"".join(grid_items)}

.. toctree::
   :maxdepth: 3
   :caption: {package_info['title']} Modules
   :hidden:

{chr(10).join(f'   {module}/index' for module in package_info["modules"])}

Module Path
-----------

.. code-block:: python

   import haive.{package_name}
   # or
   from haive.{package_name} import *

Package Structure
-----------------

This package contains the following module hierarchy:

"""

    # Add module tree
    for module_name, submodules in package_info["modules"].items():
        content += f"\n**{module_name}**\n"
        if submodules:
            for submodule in submodules:
                content += f"  - {submodule}\n"
        else:
            content += "  - *(no submodules)*\n"

    return content


def create_module_index(
    package_name: str, module_name: str, submodules: list[str]
) -> str:
    """Create index page for a module (e.g., haive/core/engine/index.rst)."""
    module_title = module_name.replace("_", " ").title()

    # Create submodule grid if there are submodules
    grid_content = ""
    if submodules:
        grid_items = []
        for submodule in submodules:
            submodule_title = submodule.replace("_", " ").title()
            grid_items.append(
                f"""
   .. grid-item-card:: **{submodule_title}**
      :link: {submodule}
      :link-type: doc

      haive.{package_name}.{module_name}.{submodule}"""
            )

        grid_content = f"""
Submodules
----------

.. grid:: 1 2 2 3
   :gutter: 3
{"".join(grid_items)}
"""

    # Toctree
    toctree_entries = submodules if submodules else []

    content = f"""{module_title}
{'=' * len(module_title)}

Module path: ``haive.{package_name}.{module_name}``

{grid_content}

Module Documentation
--------------------

.. automodule:: haive.{package_name}.{module_name}
   :members:
   :undoc-members:
   :show-inheritance:

.. toctree::
   :maxdepth: 2
   :hidden:

{chr(10).join(f'   {sub}' for sub in toctree_entries)}

Import
------

.. code-block:: python

   from haive.{package_name}.{module_name} import *
   # or
   import haive.{package_name}.{module_name}
"""

    return content


def create_submodule_doc(
    package_name: str, module_name: str, submodule_name: str
) -> str:
    """Create documentation for a submodule (e.g., haive/core/engine/base.rst)."""
    title = f"haive.{package_name}.{module_name}.{submodule_name}"

    content = f"""{title}
{'=' * len(title)}

.. currentmodule:: haive.{package_name}.{module_name}.{submodule_name}

.. automodule:: haive.{package_name}.{module_name}.{submodule_name}
   :members:
   :undoc-members:
   :show-inheritance:
   :inherited-members:
   :private-members:
   :special-members: __init__, __call__

Classes
-------

.. autosummary::
   :nosignatures:
   :toctree: _autosummary

Functions
---------

.. autosummary::
   :nosignatures:
   :toctree: _autosummary

Examples
--------

.. code-block:: python

   from haive.{package_name}.{module_name}.{submodule_name} import *

   # Your code here

See Also
--------

- :doc:`/api/haive/{package_name}/index` - Package overview
- :doc:`/api/haive/{package_name}/{module_name}/index` - Module overview
"""

    return content


def restructure_docs():
    """Restructure the documentation with new navigation pattern."""
    # Create haive root directory
    haive_dir = DOCS_SOURCE / "haive"
    haive_dir.mkdir(parents=True, exist_ok=True)

    # Create root index
    root_index = create_haive_root_index()
    (haive_dir / "index.rst").write_text(root_index)

    # Create package directories and documentation
    for package_name, package_info in HAIVE_STRUCTURE.items():
        package_dir = haive_dir / package_name
        package_dir.mkdir(parents=True, exist_ok=True)

        # Create package index
        package_index = create_package_index(package_name, package_info)
        (package_dir / "index.rst").write_text(package_index)

        # Create module directories
        for module_name, submodules in package_info["modules"].items():
            module_dir = package_dir / module_name
            module_dir.mkdir(parents=True, exist_ok=True)

            # Create module index
            module_index = create_module_index(package_name, module_name, submodules)
            (module_dir / "index.rst").write_text(module_index)

            # Create submodule documentation
            for submodule_name in submodules:
                submodule_doc = create_submodule_doc(
                    package_name, module_name, submodule_name
                )
                (module_dir / f"{submodule_name}.rst").write_text(submodule_doc)

    # Update the main API index to point to the new structure
    api_index_content = """API Reference
=============

.. toctree::
   :maxdepth: 5
   :caption: Haive API

   haive/index

Legacy Documentation
--------------------

The previous package-based documentation is still available:

.. toctree::
   :maxdepth: 2
   :caption: Legacy Links
   :hidden:

   haive-core
   haive-agents
   haive-tools
   haive-games
   haive-dataflow
   haive-prebuilt
   haive-mcp
"""

    (DOCS_SOURCE / "index.rst").write_text(api_index_content)


if __name__ == "__main__":
    restructure_docs()
