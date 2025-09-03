#!/usr/bin/env python3
"""Apply documentation improvements from haive-mcp to other packages.

This script automates the application of successful documentation
patterns from haive-mcp to other Haive packages.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import subprocess


class DocImprover:
    """Applies documentation improvements to Haive packages."""

    def __init__(self, package_name: str, dry_run: bool = False):
        self.package_name = package_name
        self.dry_run = dry_run
        self.package_path = Path(f"packages/{package_name}")
        self.docs_path = self.package_path / "docs" / "source"
        self.static_path = self.docs_path / "_static"

    def apply_all_improvements(self):
        """Apply all documentation improvements."""
        print(f"\n🚀 Applying improvements to {self.package_name}...")

        # 1. Update conf.py
        self.update_sphinx_config()

        # 2. Apply black/blue theme
        self.apply_theme()

        # 3. Fix RST docstrings
        self.fix_docstrings()

        # 4. Update index.rst structure
        self.update_index_structure()

        # 5. Create inheritance diagram
        self.create_inheritance_diagram()

        print(f"\n✅ Improvements applied to {self.package_name}!")

    def update_sphinx_config(self):
        """Update conf.py with improved settings."""
        print("\n📝 Updating Sphinx configuration...")

        conf_path = self.docs_path / "conf.py"
        if not conf_path.exists():
            print(f"  ❌ conf.py not found at {conf_path}")
            return

        # Read existing config
        with open(conf_path) as f:
            content = f.read()

        # Key improvements to add
        improvements = {
            "autoapi_own_page_level":
            'autoapi_own_page_level = "module"',
            "autoapi_member_order":
            'autoapi_member_order = "groupwise"',
            "autoapi_toctree_caption":
            'autoapi_toctree_caption = "🔍 Complete API Reference"',
            "autoapi_toctree_first":
            "autoapi_toctree_first = True",
            "autoapi_python_class_content":
            'autoapi_python_class_content = "both"',
        }

        # Enhanced extensions list
        extensions = """extensions = [
    "autoapi.extension",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.ifconfig",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_tabs.tabs",
    "sphinx_togglebutton",
    "sphinxcontrib.mermaid",
    "sphinx.ext.graphviz",
]"""

        modified = False

        # Update extensions if needed
        if "sphinx_design" not in content:
            content = re.sub(r"extensions = \[.*?\]",
                             extensions,
                             content,
                             flags=re.DOTALL)
            modified = True

        # Add AutoAPI improvements
        for key, line in improvements.items():
            if key not in content:
                # Find where to insert (after autoapi_dirs)
                if "autoapi_dirs" in content:
                    content = re.sub(r"(autoapi_dirs = .*?\n)", f"\\1{line}\n",
                                     content)
                    modified = True

        # Update theme options for black/blue
        if "dark_css_variables" in content:
            # Update existing dark theme
            content = re.sub(
                r'"color-background-primary":\s*"[^"]*"',
                '"color-background-primary": "#000612"',
                content,
            )
            content = re.sub(
                r'"color-sidebar-background":\s*"[^"]*"',
                '"color-sidebar-background": "#0a1428"',
                content,
            )
            modified = True

        if modified:
            if self.dry_run:
                print(f"  🔍 Would update {conf_path}")
                print("  Changes:")
                for key in improvements:
                    if key not in content:
                        print(f"    - Add {key}")
            else:
                with open(conf_path, "w") as f:
                    f.write(content)
                print(f"  ✅ Updated {conf_path}")
        else:
            print("  ℹ️  Config already up to date")

    def apply_theme(self):
        """Apply black/blue theme CSS."""
        print("\n🎨 Applying black/blue theme...")

        # Create _static directory if needed
        self.static_path.mkdir(parents=True, exist_ok=True)

        theme_css = """/* Haive Black/Blue Theme */
/* Dark Mode Enhancements */
body[data-theme="dark"] {
    background-color: #000612 !important; /* Very dark blue-black */
}

body[data-theme="dark"] .sidebar-container {
    background-color: #0a1428 !important; /* Dark navy blue */
    border-right: 1px solid #1e3a8a !important;
}

body[data-theme="dark"] .sidebar-content {
    background-color: #0a1428 !important;
}

body[data-theme="dark"] .content-wrapper {
    background-color: #000612 !important;
}

body[data-theme="dark"] .content {
    background-color: #000612 !important;
}

/* Code blocks */
body[data-theme="dark"] pre {
    background-color: #0f172a !important; /* Dark slate blue */
    border: 1px solid #1e3a8a !important;
}

body[data-theme="dark"] code:not(pre code) {
    background-color: #1e293b !important;
    color: #e2e8f0 !important;
    padding: 0.2em 0.4em;
    border-radius: 3px;
}

/* Improve contrast for links */
body[data-theme="dark"] a {
    color: #60a5fa !important; /* Bright blue */
}

body[data-theme="dark"] a:hover {
    color: #93bbfc !important;
}

/* Navigation improvements */
body[data-theme="dark"] .sidebar-tree a:hover {
    background-color: #1e293b !important;
    color: #f1f5f9 !important;
}

body[data-theme="dark"] .current > a {
    background-color: #1e40af !important;
    color: #ffffff !important;
}"""

        theme_path = self.static_path / "black-blue-theme.css"

        if self.dry_run:
            print(f"  🔍 Would create {theme_path}")
        else:
            with open(theme_path, "w") as f:
                f.write(theme_css)
            print(f"  ✅ Created {theme_path}")

        # Update conf.py to include the CSS
        conf_path = self.docs_path / "conf.py"
        if conf_path.exists():
            with open(conf_path) as f:
                content = f.read()

            if "html_css_files" not in content:
                css_config = """
html_css_files = [
    "black-blue-theme.css",
]"""
                content += css_config

                if not self.dry_run:
                    with open(conf_path, "w") as f:
                        f.write(content)
                    print("  ✅ Added CSS to conf.py")

    def fix_docstrings(self):
        """Fix RST formatting in docstrings."""
        print("\n🔧 Fixing RST docstrings...")

        # Find all __init__.py files
        init_files = list(self.package_path.rglob("__init__.py"))

        fixes_applied = 0
        for init_file in init_files:
            if self._fix_file_docstrings(init_file):
                fixes_applied += 1

        print(f"  ✅ Fixed {fixes_applied} files")

    def _fix_file_docstrings(self, file_path: Path) -> bool:
        """Fix docstrings in a single file."""
        try:
            with open(file_path) as f:
                content = f.read()

            original = content

            # Fix common RST issues
            # 1. Fix section headers
            content = re.sub(
                r"^([A-Z][A-Za-z\s]+)$\n^(-+)$",
                r"\1\n" + "=" * 50,
                content,
                flags=re.MULTILINE,
            )
            content = re.sub(
                r"^(\s*)([A-Z][A-Za-z\s]+):$",
                r"\1**\2**:",
                content,
                flags=re.MULTILINE,
            )

            # 2. Fix code blocks
            content = re.sub(r"```python\n", r".. code-block:: python\n\n    ",
                             content)
            content = re.sub(r"```\n", r"\n", content)

            # 3. Fix lists
            content = re.sub(r"^(\s*)- ([A-Z])",
                             r"\1* \2",
                             content,
                             flags=re.MULTILINE)

            if content != original:
                if self.dry_run:
                    print(
                        f"  🔍 Would fix {file_path.relative_to(self.package_path)}"
                    )
                else:
                    with open(file_path, "w") as f:
                        f.write(content)
                return True

        except Exception as e:
            print(f"  ⚠️  Error processing {file_path}: {e}")

        return False

    def update_index_structure(self):
        """Update index.rst with better structure."""
        print("\n📚 Updating index.rst structure...")

        index_path = self.docs_path / "index.rst"
        if not index_path.exists():
            print("  ❌ index.rst not found")
            return

        # Package-specific templates
        templates = {
            "haive-agents": self._get_agents_index_template(),
            "haive-games": self._get_games_index_template(),
            "haive-dataflow": self._get_dataflow_index_template(),
            "haive-prebuilt": self._get_prebuilt_index_template(),
        }

        template = templates.get(self.package_name)
        if template:
            if self.dry_run:
                print(f"  🔍 Would update {index_path}")
            else:
                with open(index_path, "w") as f:
                    f.write(template)
                print(f"  ✅ Updated {index_path}")
        else:
            print(f"  ℹ️  No template for {self.package_name}")

    def _get_agents_index_template(self) -> str:
        """Get index.rst template for haive-agents."""
        return """Haive Agents Documentation
=========================

.. toctree::
   :maxdepth: 4
   :caption: 📖 Documentation
   :hidden:

   API Overview <api_reference>
   Agent Hierarchy <inheritance_diagram>

.. toctree::
   :maxdepth: 3
   :caption: 🚀 Quick Start
   :hidden:

   getting_started
   installation
   quickstart

.. toctree::
   :maxdepth: 2
   :caption: 🤖 Agent Types
   :hidden:

   agents/simple
   agents/react
   agents/multi
   agents/rag
   agents/reasoning

Welcome to Haive Agents
----------------------

The Haive Agents package provides a comprehensive collection of AI agent implementations, from simple conversational agents to complex multi-agent systems with reasoning capabilities.

.. grid:: 2
   :gutter: 3

   .. grid-item-card:: 🤖 **Simple Agents**
      :text-align: center

      Basic agents for straightforward conversational tasks

      - SimpleAgent - Basic chat agent
      - ToolAgent - Agent with tool usage
      - MemoryAgent - Agent with conversation memory

   .. grid-item-card:: 🧠 **Reasoning Agents**
      :text-align: center

      Advanced agents with reasoning and planning capabilities

      - ReactAgent - Reasoning and acting
      - PlannerAgent - Multi-step planning
      - CritiqueAgent - Self-reflection

   .. grid-item-card:: 🔄 **Multi-Agent Systems**
      :text-align: center

      Coordinate multiple agents for complex tasks

      - MultiAgent - Agent orchestration
      - SequentialAgent - Step-by-step execution
      - ParallelAgent - Concurrent processing

   .. grid-item-card:: 📚 **RAG Agents**
      :text-align: center

      Retrieval-augmented generation for knowledge tasks

      - BaseRAGAgent - Core RAG functionality
      - SimpleRAGAgent - Easy RAG setup
      - AdvancedRAGAgent - Complex retrieval

Key Features
~~~~~~~~~~~

* 🎯 **Multiple Agent Types** - From simple to complex
* 🛠️ **Tool Integration** - Easy tool usage
* 💾 **Memory Management** - Conversation persistence
* 🔄 **Agent Composition** - Combine agents
* 📊 **State Management** - Advanced state handling
* 🧪 **Well Tested** - Comprehensive test coverage

Next Steps
~~~~~~~~~~

- :doc:`getting_started` - Understand agent concepts
- :doc:`installation` - Install haive-agents
- :doc:`quickstart` - Create your first agent
- :doc:`agents/simple` - Start with simple agents

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""

    def _get_games_index_template(self) -> str:
        """Get index.rst template for haive-games."""
        return """Haive Games Documentation
========================

Game environments and agents for reinforcement learning and game AI.

[Template content here...]
"""

    def _get_dataflow_index_template(self) -> str:
        """Get index.rst template for haive-dataflow."""
        return """Haive Dataflow Documentation
===========================

Streaming data processing and flow control for Haive agents.

[Template content here...]
"""

    def _get_prebuilt_index_template(self) -> str:
        """Get index.rst template for haive-prebuilt."""
        return """Haive Prebuilt Documentation
===========================

Ready-to-use agent configurations for common use cases.

[Template content here...]
"""

    def create_inheritance_diagram(self):
        """Create Mermaid inheritance diagram."""
        print("\n🎨 Creating inheritance diagram...")

        # Package-specific diagrams
        diagrams = {
            "haive-agents": self._get_agents_diagram(),
            "haive-games": self._get_games_diagram(),
            "haive-dataflow": self._get_dataflow_diagram(),
            "haive-prebuilt": self._get_prebuilt_diagram(),
        }

        diagram_content = diagrams.get(self.package_name)
        if not diagram_content:
            print(f"  ℹ️  No diagram template for {self.package_name}")
            return

        diagram_path = self.docs_path / "inheritance_diagram.rst"

        if self.dry_run:
            print(f"  🔍 Would create {diagram_path}")
        else:
            with open(diagram_path, "w") as f:
                f.write(diagram_content)
            print(f"  ✅ Created {diagram_path}")

    def _get_agents_diagram(self) -> str:
        """Get inheritance diagram for haive-agents."""
        return """Agent Class Hierarchy
====================

Interactive diagram showing the inheritance relationships between agent classes.

.. raw:: html

   <details>
   <summary><strong>🔍 Click to view interactive agent hierarchy diagram</strong></summary>

.. mermaid::
   :align: center

   graph TD
       Agent[🤖 Agent<br/>Base agent class]:::base
       SimpleAgent[🤖 SimpleAgent<br/>Basic conversational agent]:::simple
       ReactAgent[🧠 ReactAgent<br/>Reasoning and acting]:::react
       MultiAgent[🔄 MultiAgent<br/>Agent orchestration]:::multi
       BaseRAGAgent[📚 BaseRAGAgent<br/>RAG foundation]:::rag

       Agent --> SimpleAgent
       Agent --> ReactAgent
       Agent --> MultiAgent
       Agent --> BaseRAGAgent

       SimpleAgent --> ToolAgent[🛠️ ToolAgent<br/>With tool usage]:::simple
       SimpleAgent --> MemoryAgent[💾 MemoryAgent<br/>With memory]:::simple

       ReactAgent --> PlannerAgent[📋 PlannerAgent<br/>Multi-step planning]:::react
       ReactAgent --> CritiqueAgent[🔍 CritiqueAgent<br/>Self-reflection]:::react

       MultiAgent --> SequentialAgent[📊 SequentialAgent<br/>Step-by-step]:::multi
       MultiAgent --> ParallelAgent[⚡ ParallelAgent<br/>Concurrent]:::multi

       BaseRAGAgent --> SimpleRAGAgent[📖 SimpleRAGAgent<br/>Easy RAG]:::rag
       BaseRAGAgent --> AdvancedRAGAgent[🎓 AdvancedRAGAgent<br/>Complex RAG]:::rag

       click Agent "https://haive-central.readthedocs.io/en/latest/agents/base.html"
       click SimpleAgent "autoapi/haive/agents/simple/index.html"
       click ReactAgent "autoapi/haive/agents/react/index.html"
       click MultiAgent "autoapi/haive/agents/multi/index.html"
       click BaseRAGAgent "autoapi/haive/agents/rag/index.html"

       classDef base fill:#1e3a8a,stroke:#60a5fa,color:#fff
       classDef simple fill:#059669,stroke:#34d399,color:#fff
       classDef react fill:#7c3aed,stroke:#a78bfa,color:#fff
       classDef multi fill:#dc2626,stroke:#f87171,color:#fff
       classDef rag fill:#ea580c,stroke:#fb923c,color:#fff

.. raw:: html

   </details>

Agent Categories
---------------

.. grid:: 2
   :gutter: 2

   .. grid-item-card:: 🟦 **Base Classes**
      :text-align: center

      Core agent infrastructure from haive-core

      Links to: `haive-central documentation <https://haive-central.readthedocs.io>`_

   .. grid-item-card:: 🟩 **Simple Agents**
      :text-align: center

      Basic conversational agents for straightforward tasks

      Links to: :doc:`autoapi/haive/agents/simple/index`

   .. grid-item-card:: 🟣 **Reasoning Agents**
      :text-align: center

      Advanced agents with reasoning and planning capabilities

      Links to: :doc:`autoapi/haive/agents/react/index`

   .. grid-item-card:: 🟥 **Multi-Agent Systems**
      :text-align: center

      Orchestration and coordination of multiple agents

      Links to: :doc:`autoapi/haive/agents/multi/index`
"""

    def _get_games_diagram(self) -> str:
        """Get inheritance diagram for haive-games."""
        return """Game Environment Hierarchy
=========================

[Game-specific diagram content...]
"""

    def _get_dataflow_diagram(self) -> str:
        """Get inheritance diagram for haive-dataflow."""
        return """Dataflow Component Hierarchy
===========================

[Dataflow-specific diagram content...]
"""

    def _get_prebuilt_diagram(self) -> str:
        """Get inheritance diagram for haive-prebuilt."""
        return """Prebuilt Agent Hierarchy
=======================

[Prebuilt-specific diagram content...]
"""


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Apply documentation improvements to Haive packages", )
    parser.add_argument(
        "package",
        choices=[
            "haive-agents", "haive-games", "haive-dataflow", "haive-prebuilt"
        ],
        help="Package to update",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without making changes",
    )

    args = parser.parse_args()

    # Change to project root
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)

    # Apply improvements
    improver = DocImprover(args.package, args.dry_run)
    improver.apply_all_improvements()

    if not args.dry_run:
        print(f"\n🏗️  Building documentation for {args.package}...")
        build_cmd = [
            "sphinx-build",
            "-b",
            "html",
            f"packages/{args.package}/docs/source",
            f"packages/{args.package}/docs/build/html",
        ]
        subprocess.run(build_cmd, check=False)
        print("\n✅ Documentation built successfully!")
        print(f"📂 View at: packages/{args.package}/docs/build/html/index.html")


if __name__ == "__main__":
    main()
