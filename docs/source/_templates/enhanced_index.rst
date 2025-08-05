🤖 Haive AI Agent Framework Documentation
========================================

.. container:: hero-banner

   :name: hero-banner

   .. container:: hero-content

      .. image:: /_static/images/haive-logo-light.svg
         :class:``hero-logo``
         :alt: Haive Logo
         :width: 200px

      Build Intelligent AI Agents with Professional Tools
      ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

      Professional framework for creating sophisticated AI agents with conversational intelligence,
      tool orchestration, game strategies, and multi-agent coordination.

      .. button-ref:: introduction/quickstart
         :ref-type: doc
         :color: primary
         :class:``sd-rounded-pill``

         🚀 Get Started

      .. button-link:: https://github.com/haive/haive
         :color: secondary
         :class:``sd-rounded-pill``

         📚 View on GitHub

.. grid:: 1 1 4 4

   :gutter: 3
   :class-container: feature-grid

   .. grid-item-card:: 🧠 AI Agents

      :class-header: feature-card-header
      :class-body: feature-card-body
      :shadow: lg
      :link: agents/index
      :link-type: doc

      Build intelligent agents with memory, reasoning, and tool integration capabilities.

      .. list-table::
         :class:``feature-list``
         :widths: 1 2

         * - *Types**
           - Simple • React • RAG • Multi-Agent
         * - *Features**
           - Auto-persistence • Tool routing • State management

   .. grid-item-card:: 🎮 Game Intelligence

      :class-header: feature-card-header
      :class-body: feature-card-body
      :shadow: lg
      :link: games/index
      :link-type: doc

      Create AI opponents for strategic games with advanced algorithms and decision making.

      .. list-table::
         :class:``feature-list``
         :widths: 1 2

         * - *Games**
           - Chess • Go • Poker • Board Games
         * - *Features**
           - Strategy AI • Game state • Player modeling

   .. grid-item-card:: 🔧 Tool Orchestration

      :class-header: feature-card-header
      :class-body: feature-card-body
      :shadow: lg
      :link: tools/index
      :link-type: doc

      Connect agents to APIs, databases, search engines, and external services seamlessly.

      .. list-table::
         :class:``feature-list``
         :widths: 1 2

         * - *Types**
           - Web APIs • Databases • File Systems
         * - *Features**
           - Auto-discovery • Type safety • Error handling

   .. grid-item-card:: 📡 MCP Integration

      :class-header: feature-card-header
      :class-body: feature-card-body
      :shadow: lg
      :link: mcp/index
      :link-type: doc

      1,960+ Model Context Protocol servers with hot-reload and AI-powered discovery.

      .. list-table::
         :class:``feature-list``
         :widths: 1 2

         * - *Servers**
           - 1,960+ available • Auto-discovery
         * - *Features**
           - Hot-reload • Plugin system • Integration

.. tab-set::

   .. tab-item:: 🚀 Quick Start

      :sync: quickstart

.. code-block:: python

    # Code example here

         :caption: Create your first agent
         :linenos:
         :emphasize-lines: 8-10
         :class:``copy-button``

         from haive.agents import SimpleAgent
         from haive.core.engine import AugLLMConfig

         # Configure with enhanced settings
         config = AugLLMConfig(
             model="gpt-4",
             temperature=0.7,
             system_message="You are a helpful AI assistant with expertise in technical topics.",
             max_tokens=1000
         )

         # Create and run agent
         agent = SimpleAgent(name="assistant", engine=config)
         response = await agent.arun("Explain quantum computing in simple terms")
         print(response)

         .. tab-item:: 🔧 Tool Integration

         :sync: tools

.. code-block:: python

    # Code example here

         :caption: Agent with tools
         :linenos:
         :emphasize-lines: 13-16
         :class:``copy-button``

         from haive.agents import ReactAgent
         from haive.tools import WebSearchTool, CalculatorTool

         # Create tools
         search = WebSearchTool()
         calc = CalculatorTool()

         # Configure agent with tools
         agent = ReactAgent(
             name="research_agent",
             engine=config,
             tools=[search, calc]
         )

         # Agent can now search and calculate
         result = await agent.arun("What's the population of Tokyo and what's 20% of that?")

         .. tab-item:: 🤝 Multi-Agent

         :sync: multiagent

.. code-block:: python

    # Code example here

         :caption: Multi-agent coordination
         :linenos:
         :emphasize-lines: 8-12
         :class:``copy-button``

         from haive.agents import MultiAgent, SimpleAgent, ReactAgent

         # Create specialized agents
         researcher = ReactAgent(name="researcher", tools=[search])
         writer = SimpleAgent(name="writer", engine=creative_config)

         # Coordinate agents
         team = MultiAgent(
             name="content_team",
             agents=[researcher, writer],
             execution_mode="sequential"
         )

         result = await team.arun("Research AI trends and write a summary")

         .. dropdown:: 💡 Why Choose Haive?

         :color: info
         :icon: light-bulb

         .. grid:: 1 2 4 4

         :gutter: 2

         .. grid-item::
         :class:``benefit-item``

         .. container:: benefit-icon

            ⚡


     **Production Ready*

         Battle-tested in production environments with comprehensive error handling.

         .. grid-item::
         :class:``benefit-item``

         .. container:: benefit-icon

            🔒

         **Type Safe*

         Full type hints and Pydantic models for reliable development.

         .. grid-item::
         :class:``benefit-item``

         .. container:: benefit-icon

            🚀

         **High Performance*

         Async-first architecture with optimized execution and caching.

         .. grid-item::
         :class:``benefit-item``

         .. container:: benefit-icon

            🎯

         **Extensible*

         Plugin architecture allows custom agents, tools, and integrations.

         .. admonition:: 📊 Performance Metrics

         :class:``note``

         .. grid:: 1 2 4 4

         :gutter: 2
         :class-container: metrics-grid

         .. grid-item::
         :class:``metric-item``

         **<100ms*

         *Average Response Time*

         .. grid-item::
         :class:``metric-item``

         **10K+*

         *Agents per Hour*

         .. grid-item::
         :class:``metric-item``

         **99.9%*

         *System Uptime*

         .. grid-item::
         :class:``metric-item``

         **86+*

         *Documentation Extensions*

         📖 Documentation Sections
         ==========================

         .. grid:: 1 2 3 3

         :gutter: 3
         :class-container: docs-grid

         .. grid-item-card:: 📚 Getting Started

         :shadow: md
         :link: introduction/index
         :link-type: doc
         :class-header: docs-card-header

         Installation, quickstart, and core concepts to get you up and running.

         * Installation guide*
         * Quick start tutorial  *
         * Core concepts overview*
         * Best practices*

         .. grid-item-card:: 🤖 Agent Development

         :shadow: md
         :link: agents/index
         :link-type: doc
         :class-header: docs-card-header

         Comprehensive guide to building and deploying AI agents.

         * Agent types and patterns*
         * Configuration and setup*
         * Advanced features*
         * Real-world examples*

         .. grid-item-card:: 📖 API Reference

         :shadow: md
         :link: api/index
         :link-type: doc
         :class-header: docs-card-header

         Complete API documentation with enhanced Pydantic model docs.

         * Full API coverage*
         * Pydantic models*
         * Type information*
         * Usage examples*

         .. grid-item-card:: 💻 Examples & Demos

         :shadow: md
         :link: examples/index
         :link-type: doc
         :class-header: docs-card-header

         Interactive examples and step-by-step tutorials.

         * Live code examples*
         * Jupyter notebooks*
         * Demo applications*
         * Video tutorials*

         .. grid-item-card:: 🔧 Tools & Integrations

         :shadow: md
         :link: tools/index
         :link-type: doc
         :class-header: docs-card-header

         Tool creation, integration patterns, and MCP servers.

         * Custom tool creation*
         * MCP integration*
         * API connections*
         * Database integration*

         .. grid-item-card:: 🎮 Game Intelligence

         :shadow: md
         :link: games/index
         :link-type: doc
         :class-header: docs-card-header

         Game AI development and strategy implementation.

         * Game engine integration*
         * Strategy algorithms*
         * Multi-player systems*
         * Tournament modes*

         .. toctree::

         :maxdepth: 2
         :caption: 📚 Getting Started
         :hidden:

         introduction/index
         introduction/installation
         introduction/quickstart
         introduction/concepts

         .. toctree::

         :maxdepth: 2
         :caption: 🤖 Agents
         :hidden:

         agents/index
         agents/simple/index
         agents/react/index
         agents/rag/index
         agents/multi/index
         agents/demos/index

         .. toctree::

         :maxdepth: 2
         :caption: 🔧 Tools & Integration
         :hidden:

         tools/index
         mcp/index
         mcp/servers
         mcp/setup

         .. toctree::

         :maxdepth: 2
         :caption: 🎮 Games & Examples
         :hidden:

         games/index
         examples/index
         gallery

         .. toctree::

         :maxdepth: 2
         :caption: 📖 Reference
         :hidden:

         api/index
         guides/index
         reference/index

         .. toctree::

         :maxdepth: 1
         :caption: 🛠️ Development
         :hidden:

         development/index
