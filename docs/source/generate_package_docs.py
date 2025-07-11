#!/usr/bin/env python3
"""Generate comprehensive package documentation structure for Haive.

This script automatically creates index.rst files for all packages and their
modules/submodules with proper hierarchy and navigation.
"""

import os
import textwrap
from pathlib import Path
from typing import Dict, List, Set

# Package root paths
PACKAGES_DIR = Path("/home/will/Projects/haive/backend/haive/packages")
DOCS_SOURCE = Path("/home/will/Projects/haive/backend/haive/docs/source/api")

# Package configurations
PACKAGE_INFO = {
    "haive-core": {
        "title": "Haive Core",
        "description": "Core infrastructure and utilities for the Haive framework",
        "icon": "🏗️",
        "modules": {
            "engine": {
                "title": "Engine System",
                "description": "LLM integration and augmentation",
                "icon": "🤖",
                "submodules": [
                    "base",
                    "aug_llm",
                    "document",
                    "agent",
                    "embedding",
                    "retriever",
                    "vectorstore",
                    "tool",
                ],
            },
            "schema": {
                "title": "Schema System",
                "description": "Dynamic state schema composition",
                "icon": "📊",
                "submodules": [
                    "state_schema",
                    "schema_composer",
                    "compatibility",
                    "prebuilt",
                ],
            },
            "graph": {
                "title": "Graph System",
                "description": "State machines and workflow orchestration",
                "icon": "🌐",
                "submodules": [
                    "state_graph",
                    "node",
                    "patterns",
                    "routers",
                    "branches",
                    "utils",
                ],
            },
            "persistence": {
                "title": "Persistence",
                "description": "State persistence and recovery",
                "icon": "💾",
                "submodules": ["store", "handlers", "factory"],
            },
            "registry": {
                "title": "Registry",
                "description": "Component registration and discovery",
                "icon": "📖",
                "submodules": ["base", "decorators", "manager"],
            },
            "common": {
                "title": "Common",
                "description": "Shared utilities and mixins",
                "icon": "🏗️",
                "submodules": ["mixins", "models", "types"],
            },
            "config": {
                "title": "Configuration",
                "description": "Configuration management",
                "icon": "⚙️",
                "submodules": [],
            },
            "logging": {
                "title": "Logging",
                "description": "Enhanced logging system",
                "icon": "📝",
                "submodules": [],
            },
            "models": {
                "title": "Models",
                "description": "Model implementations",
                "icon": "🧠",
                "submodules": ["llm", "embeddings", "retriever", "vectorstore"],
            },
            "runtime": {
                "title": "Runtime",
                "description": "Runtime system",
                "icon": "⚡",
                "submodules": ["base", "extension"],
            },
            "types": {
                "title": "Types",
                "description": "Type definitions and utilities",
                "icon": "📐",
                "submodules": [],
            },
            "ui": {
                "title": "UI",
                "description": "User interface components",
                "icon": "🖼️",
                "submodules": [],
            },
            "utils": {
                "title": "Utilities",
                "description": "General utilities",
                "icon": "🔧",
                "submodules": [],
            },
        },
    },
    "haive-agents": {
        "title": "Haive Agents",
        "description": "Pre-built agent implementations",
        "icon": "🤖",
        "modules": {
            "base": {
                "title": "Base Agent",
                "description": "Base agent classes and mixins",
                "icon": "🏗️",
                "submodules": ["mixins"],
            },
            "simple": {
                "title": "Simple Agents",
                "description": "Basic conversational agents",
                "icon": "💬",
                "submodules": ["structured", "v2"],
            },
            "conversation": {
                "title": "Conversation Agents",
                "description": "Multi-turn dialogue agents",
                "icon": "🗣️",
                "submodules": [
                    "base",
                    "collaborative",
                    "debate",
                    "directed",
                    "round_robin",
                    "social_media",
                ],
            },
            "rag": {
                "title": "RAG Agents",
                "description": "Retrieval-augmented generation",
                "icon": "📚",
                "submodules": [
                    "base",
                    "adaptive_rag",
                    "self_rag",
                    "multi_strategy",
                    "hyde",
                    "db_rag",
                ],
            },
            "react": {
                "title": "ReAct Agents",
                "description": "Reasoning and action agents",
                "icon": "🔄",
                "submodules": [],
            },
            "reasoning_and_critique": {
                "title": "Reasoning Agents",
                "description": "Advanced reasoning agents",
                "icon": "🧠",
                "submodules": [
                    "lats",
                    "reflection",
                    "reflexion",
                    "tot",
                    "mcts",
                    "self_discover",
                ],
            },
            "multi": {
                "title": "Multi-Agent",
                "description": "Multi-agent coordination",
                "icon": "🤝",
                "submodules": ["sequential"],
            },
            "planning": {
                "title": "Planning Agents",
                "description": "Task planning agents",
                "icon": "📋",
                "submodules": ["plan_and_execute", "llm_compiler", "rewoo"],
            },
            "research": {
                "title": "Research Agents",
                "description": "Research and analysis agents",
                "icon": "🔬",
                "submodules": ["person", "storm", "perplexity"],
            },
        },
    },
    "haive-tools": {
        "title": "Haive Tools",
        "description": "Tools and utilities for agents",
        "icon": "🔧",
        "modules": {
            "api": {
                "title": "API Tools",
                "description": "API interaction tools",
                "icon": "🌐",
                "submodules": [],
            },
            "code": {
                "title": "Code Tools",
                "description": "Code manipulation tools",
                "icon": "💻",
                "submodules": [],
            },
            "data": {
                "title": "Data Tools",
                "description": "Data processing tools",
                "icon": "📊",
                "submodules": [],
            },
            "math": {
                "title": "Math Tools",
                "description": "Mathematical tools",
                "icon": "🔢",
                "submodules": [],
            },
            "search": {
                "title": "Search Tools",
                "description": "Search and retrieval tools",
                "icon": "🔍",
                "submodules": [],
            },
            "utility": {
                "title": "Utility Tools",
                "description": "General utility tools",
                "icon": "🛠️",
                "submodules": [],
            },
        },
    },
}


def create_module_index(
    package_name: str, module_name: str, module_info: dict, package_prefix: str
) -> str:
    """Create index.rst content for a module."""
    submodules = module_info.get("submodules", [])

    # Create grid cards for submodules if they exist
    grid_content = ""
    if submodules:
        grid_items = []
        for submodule in submodules:
            # Try to get submodule info if it exists
            submodule_title = submodule.replace("_", " ").title()
            grid_items.append(
                f"""
   .. grid-item-card:: **{submodule_title}**
      :link: {submodule}/index
      :link-type: doc

      {package_prefix}.{module_name}.{submodule}"""
            )

        if grid_items:
            grid_content = f"""
.. grid:: 1 2 2 3
   :gutter: 3
{"".join(grid_items)}
"""

    # Create toctree
    toctree_entries = []
    if submodules:
        for submodule in submodules:
            toctree_entries.append(f"   {submodule}/index")

    # Always add the module documentation itself
    toctree_entries.append("   module")

    toctree = f"""
.. toctree::
   :maxdepth: 2
   :caption: Contents
   :hidden:

{chr(10).join(toctree_entries)}"""

    content = f"""{module_info['title']}
{'=' * len(module_info['title'])}

{module_info['description']}

Module Path: ``{package_prefix}.{module_name}``
{grid_content}

Module Documentation
--------------------

.. automodule:: {package_prefix}.{module_name}
   :members:
   :undoc-members:
   :show-inheritance:
{toctree}

Quick Reference
---------------

Import this module:

.. code-block:: python

   from {package_prefix}.{module_name} import *
   # or
   import {package_prefix}.{module_name}
"""

    return content


def create_package_index(package_name: str, package_info: dict) -> str:
    """Create main index.rst content for a package."""
    package_prefix = package_name.replace("-", ".")

    # Create module grid
    grid_items = []
    for module_name, module_info in package_info["modules"].items():
        grid_items.append(
            f"""
   .. grid-item-card:: {module_info['icon']} **{module_info['title']}**
      :link: {module_name}/index
      :link-type: doc

      {module_info['description']}"""
        )

    grid_content = f"""
.. grid:: 1 2 2 3
   :gutter: 3
{"".join(grid_items)}"""

    # Create toctree
    toctree_entries = [f"   {module}/index" for module in package_info["modules"]]

    content = f"""{package_info['title']} API Reference
{'=' * (len(package_info['title']) + 14)}

{package_info['description']}

Package Overview
----------------
{grid_content}

Module Reference
----------------

.. toctree::
   :maxdepth: 3
   :caption: Modules

{chr(10).join(toctree_entries)}

Installation
------------

.. code-block:: bash

   pip install {package_name}
   # or with poetry
   poetry add {package_name}

Quick Start
-----------

.. code-block:: python

   import {package_prefix}
   # or
   from {package_prefix} import *
"""

    return content


def create_submodule_index(
    package_name: str, module_name: str, submodule_name: str, package_prefix: str
) -> str:
    """Create index.rst content for a submodule."""
    title = submodule_name.replace("_", " ").title()

    content = f"""{title}
{'=' * len(title)}

.. automodule:: {package_prefix}.{module_name}.{submodule_name}
   :members:
   :undoc-members:
   :show-inheritance:
   :private-members:
   :special-members: __init__

Classes
-------

.. autosummary::
   :toctree: generated
   :template: class.rst
   :recursive:

   {package_prefix}.{module_name}.{submodule_name}

Functions
---------

.. autosummary::
   :toctree: generated
   :template: function.rst
   :recursive:

   {package_prefix}.{module_name}.{submodule_name}

Usage Example
-------------

.. code-block:: python

   from {package_prefix}.{module_name}.{submodule_name} import *
   # or
   import {package_prefix}.{module_name}.{submodule_name}
"""

    return content


def create_module_direct_doc(
    package_name: str, module_name: str, package_prefix: str
) -> str:
    """Create module.rst for direct module documentation."""
    content = f"""{module_name} module
{'=' * (len(module_name) + 7)}

.. automodule:: {package_prefix}.{module_name}
   :members:
   :undoc-members:
   :show-inheritance:
   :private-members:
   :special-members: __init__
"""
    return content


def generate_docs():
    """Generate all documentation files."""
    for package_name, package_info in PACKAGE_INFO.items():
        package_prefix = package_name.replace("-", ".")
        package_dir = DOCS_SOURCE / package_name

        # Create package directory
        package_dir.mkdir(parents=True, exist_ok=True)

        # Create package index
        index_content = create_package_index(package_name, package_info)
        (package_dir / "index.rst").write_text(index_content)

        # Create module directories and files
        for module_name, module_info in package_info["modules"].items():
            module_dir = package_dir / module_name
            module_dir.mkdir(parents=True, exist_ok=True)

            # Create module index
            module_index = create_module_index(
                package_name, module_name, module_info, package_prefix
            )
            (module_dir / "index.rst").write_text(module_index)

            # Create module.rst for direct documentation
            module_doc = create_module_direct_doc(
                package_name, module_name, package_prefix
            )
            (module_dir / "module.rst").write_text(module_doc)

            # Create submodule directories and files
            for submodule_name in module_info.get("submodules", []):
                submodule_dir = module_dir / submodule_name
                submodule_dir.mkdir(parents=True, exist_ok=True)

                submodule_index = create_submodule_index(
                    package_name, module_name, submodule_name, package_prefix
                )
                (submodule_dir / "index.rst").write_text(submodule_index)


if __name__ == "__main__":
    generate_docs()
