
Haive AI Agent Framework
========================

Build intelligent AI agents with state-of-the-art tools, seamless integrations, and powerful orchestration patterns.

.. toctree::
   :maxdepth: 2
   :caption: Documentation:

   packages_index
   autoapi/index

Quick Links
-----------

* **Documentation Hub**: `Browse All Package Docs <../../docs_export/index.html>`_
* **GitHub**: `haive-ai/haive <https://github.com/haive-ai/haive>`_
* **PyPI**: Coming soon

Framework Overview
------------------

The Haive Framework provides:

* **🧠 Core Engine** - Powerful agent execution engine with state management
* **🤖 Pre-built Agents** - React, Simple, Multi-agent, RAG, and more
* **📦 MCP Integration** - Model Context Protocol for external tools
* **🛠️ Rich Tooling** - Extensive tool library and integrations
* **🎮 Game Environments** - Train and test agents in game scenarios
* **🌊 Data Pipelines** - Stream processing and real-time workflows
* **🏗️ Ready Solutions** - Pre-configured agents for common use cases

Getting Started
---------------

.. code-block:: bash

   # Install Haive
   pip install haive
   
   # Create your first agent
   from haive.agents.simple import SimpleAgent
   from haive.core.engine import AugLLMConfig
   
   agent = SimpleAgent(
       name="my_agent",
       engine=AugLLMConfig(temperature=0.7)
   )
   
   result = agent.run("Hello, Haive!")

Package Documentation
---------------------

Explore comprehensive documentation for each package:

.. list-table::
   :header-rows: 1
   :widths: 20 50 30

   * - Package
     - Description
     - Documentation
   * - haive-core
     - Core framework and infrastructure
     - `1,251 pages <../../docs_export/haive-core/index.html>`_
   * - haive-agents  
     - Agent implementations and patterns
     - `1,043 pages <../../docs_export/haive-agents/index.html>`_
   * - haive-mcp
     - Model Context Protocol integration
     - `139 pages <../../docs_export/haive-mcp/index.html>`_
   * - haive-hap
     - Hierarchical Agent Protocol
     - `59 pages <../../docs_export/haive-hap/index.html>`_
   * - haive-tools
     - Tool integrations and utilities
     - `132 pages <../../docs_export/haive-tools/index.html>`_
   * - haive-games
     - Game environments and agents
     - `482 pages <../../docs_export/haive-games/index.html>`_
   * - haive-dataflow
     - Stream processing pipelines
     - `166 pages <../../docs_export/haive-dataflow/index.html>`_
   * - haive-prebuilt
     - Pre-configured solutions
     - `209 pages <../../docs_export/haive-prebuilt/index.html>`_

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
