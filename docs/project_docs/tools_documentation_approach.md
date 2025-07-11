# Tools Package Documentation Approach

## Problem

The tools package has a non-standard structure:

- Expected: `haive.tools.api`, `haive.tools.code`, `haive.tools.utility`
- Actual: `haive.tools.toolkits.dev`, `haive.tools.tools.{individual_tools}`

## Solution

### 1. **Create Virtual Module Pages**

Since users expect `haive.tools.api`, create documentation that redirects:

```rst
API Tools
=========

API-related tools in Haive are organized within toolkits for specific services.

.. note::

   Looking for ``haive.tools.api``? API tools are organized by service
   in the toolkits directory.

Available API Toolkits
----------------------

.. autosummary::
   :toctree: _autosummary
   :recursive:

   haive.tools.toolkits.airbyte
   haive.tools.toolkits.azure_ai_services
   haive.tools.toolkits.clickup
   haive.tools.toolkits.gitlab
   haive.tools.toolkits.jira
   haive.tools.toolkits.office365
   haive.tools.toolkits.slack
   haive.tools.toolkits.zapier

Code Example
------------

.. code-block:: python

   # Instead of: from haive.tools.api import SomeAPITool
   # Use: from haive.tools.toolkits.{service} import SpecificTool

   from haive.tools.toolkits.gitlab import GitLabTool
   from haive.tools.toolkits.slack import SlackTool
```

### 2. **Document Actual Structure**

```rst
Haive Tools
===========

.. module:: haive.tools

The Haive tools package provides integrations with external services and utilities.

Package Structure
-----------------

The tools package is organized into two main categories:

**Individual Tools** (``haive.tools.tools.*``)
   Standalone tool implementations for specific tasks

**Toolkits** (``haive.tools.toolkits.*``)
   Collections of related tools organized by service or domain

Quick Start
-----------

The main module exports commonly used tools:

.. autodata:: haive.tools.arxiv_query_tool
.. autodata:: haive.tools.duckduckgo_search_tool
.. autodata:: haive.tools.google_search_tool

For other tools, import from their specific locations:

.. code-block:: python

   # Search tools
   from haive.tools.tools.duckduckgo_search import DuckDuckGoSearchTool

   # Development tools
   from haive.tools.toolkits.dev.tools import CodeEditorTool

   # API integrations
   from haive.tools.toolkits.github import GitHubTool

Navigation Guide
----------------

.. list-table:: Where to Find Tools
   :header-rows: 1
   :widths: 30 70

   * - Tool Category
     - Import Path
   * - Web Search
     - ``haive.tools.tools.{google, duckduckgo, brave}_search``
   * - Code/Development
     - ``haive.tools.toolkits.dev.*``
   * - API Integrations
     - ``haive.tools.toolkits.{service_name}``
   * - Academic/Research
     - ``haive.tools.tools.arxiv``, ``haive.tools.tools.pubmed``
   * - AI/ML Services
     - ``haive.tools.toolkits.{openai, azure_ai_services}``
```

### 3. **Auto-generate Toolkit Documentation**

```python
# _scripts/generate_toolkit_docs.py

from pathlib import Path
import ast

def generate_toolkit_index():
    """Generate index of all toolkits with proper imports."""
    toolkit_path = Path("../packages/haive-tools/src/haive/tools/toolkits")

    toolkits = {}
    for toolkit_dir in toolkit_path.iterdir():
        if toolkit_dir.is_dir() and not toolkit_dir.name.startswith('_'):
            # Find main tool classes
            tools = []
            for py_file in toolkit_dir.glob("*.py"):
                with open(py_file) as f:
                    try:
                        tree = ast.parse(f.read())
                        for node in ast.walk(tree):
                            if isinstance(node, ast.ClassDef):
                                if node.name.endswith('Tool') or node.name.endswith('Toolkit'):
                                    tools.append(node.name)
                    except:
                        pass

            toolkits[toolkit_dir.name] = tools

    # Generate RST
    rst = """
Toolkit Reference
=================

.. list-table:: Available Toolkits
   :header-rows: 1
   :widths: 20 30 50

   * - Toolkit
     - Main Classes
     - Description
"""

    for name, tools in sorted(toolkits.items()):
        rst += f"""
   * - :doc:`toolkits/{name}`
     - {', '.join(tools[:3])}
     - {get_toolkit_description(name)}
"""

    return rst
```

### 4. **Handle Import Errors Gracefully**

```python
# In conf.py

def missing_module_handler(app, what, name, obj, options, lines):
    """Add documentation for missing modules."""
    if name in ['haive.tools.api', 'haive.tools.code', 'haive.tools.utility']:
        lines.clear()
        lines.extend([
            f".. warning::",
            f"",
            f"   This module path is deprecated. Please use:",
            f"",
        ])

        if 'api' in name:
            lines.extend([
                "   - :mod:`haive.tools.toolkits.{service}` for API integrations",
                "   - See :doc:`/api/haive-tools/toolkits` for available services",
            ])
        elif 'code' in name:
            lines.extend([
                "   - :mod:`haive.tools.toolkits.dev` for code tools",
                "   - :class:`haive.tools.toolkits.dev.tools.CodeEditorTool`",
            ])
        elif 'utility' in name:
            lines.extend([
                "   - Individual tools in :mod:`haive.tools.tools`",
                "   - Specific toolkits in :mod:`haive.tools.toolkits`",
            ])

def setup(app):
    app.connect('autodoc-process-docstring', missing_module_handler)
```

### 5. **Create Migration Guide**

```rst
Tool Import Migration Guide
===========================

If you're seeing import errors, use this guide to find the correct imports:

Old Import → New Import
-----------------------

.. code-block:: python

   # ❌ Old (doesn't exist)
   from haive.tools.api import APITool

   # ✅ New (correct path)
   from haive.tools.toolkits.{service} import SpecificTool

   # ❌ Old (doesn't exist)
   from haive.tools.code import CodeTool

   # ✅ New (correct path)
   from haive.tools.toolkits.dev.tools import CodeEditorTool

   # ❌ Old (doesn't exist)
   from haive.tools.utility import UtilityTool

   # ✅ New (correct path)
   from haive.tools.tools.{specific_tool} import Tool

Common Tools Quick Reference
----------------------------

.. list-table::
   :header-rows: 1

   * - Task
     - Import
     - Example
   * - Web Search
     - ``from haive.tools import google_search_tool``
     - Built-in export
   * - Code Editing
     - ``from haive.tools.toolkits.dev.tools import CodeEditorTool``
     - AST-based editing
   * - API Calls
     - ``from haive.tools.toolkits.requests import RequestsTool``
     - HTTP requests
   * - File Operations
     - ``from haive.tools.toolkits.dev.shell import FileSystemTool``
     - File manipulation
```

## Benefits

1. **Acknowledges Reality**: Documents what actually exists
2. **Helps Users**: Clear migration path from expected to actual imports
3. **Discoverable**: Makes the non-obvious structure navigable
4. **Future-Proof**: If structure changes, only update mapping tables
