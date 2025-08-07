Haive Packages & API Reference
==============================

The Haive framework is organized into modular packages, each serving a specific purpose in building AI agent systems.

.. raw:: html

   <div class="packages-overview">
      <div class="package-stats">
         <div class="stat-card">
            <div class="stat-icon">📦</div>
            <div class="stat-number">7</div>
            <div class="stat-label">Core Packages</div>
         </div>
         <div class="stat-card">
            <div class="stat-icon">🔧</div>
            <div class="stat-number">100+</div>
            <div class="stat-label">Components</div>
         </div>
         <div class="stat-card">
            <div class="stat-icon">📚</div>
            <div class="stat-number">1000+</div>
            <div class="stat-label">API Methods</div>
         </div>
      </div>
   </div>

Package Overview
----------------

.. grid:: 1 2 2 3
   :gutter: 3

   .. grid-item-card:: 🎯 haive-core
      :link: haive-core
      :link-type: doc

      Foundation for the Haive AI Agent Framework
      
      - Engine system and LLM integration
      - State management and schemas
      - Graph-based workflows
      - Persistence layer

   .. grid-item-card:: 🤖 haive-agents
      :link: haive-agents
      :link-type: doc

      Pre-built agent implementations
      
      - Simple, React, RAG agents
      - Multi-agent coordination
      - Planning and reasoning
      - Memory systems

   .. grid-item-card:: 🔧 haive-tools
      :link: haive-tools
      :link-type: doc

      Tool library for agent capabilities
      
      - Web search and scraping
      - File operations
      - API integrations
      - Custom tool creation

   .. grid-item-card:: 🎮 haive-games
      :link: haive-games
      :link-type: doc

      Game environments and AI players
      
      - Chess, Go, Poker
      - Board game frameworks
      - Tournament systems
      - Strategy algorithms

   .. grid-item-card:: 📡 haive-mcp
      :link: haive-mcp
      :link-type: doc

      Model Context Protocol integration
      
      - MCP server implementations
      - Tool and resource providers
      - GitHub, database servers
      - Custom MCP servers

   .. grid-item-card:: 🌊 haive-dataflow
      :link: haive-dataflow
      :link-type: doc

      Streaming and data processing
      
      - Async data pipelines
      - Event streaming
      - Data transformations
      - Real-time processing

   .. grid-item-card:: 📦 haive-prebuilt
      :link: haive-prebuilt
      :link-type: doc

      Ready-to-use configurations
      
      - Pre-configured agents
      - Common workflows
      - Best practice templates
      - Quick-start setups

Quick Links
-----------

**Most Used Components**

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Component
     - Description
   * - :doc:`SimpleAgent <../api/agents/simple/agent/index>`
     - Basic conversational agent
   * - :doc:`ReactAgent <../api/agents/react/agent/index>`
     - Reasoning agent with tool use
   * - :doc:`AugLLMConfig <../api/core/engine/aug_llm/index>`
     - LLM configuration
   * - :doc:`MessagesState <../api/core/schema/prebuilt/messages_state/index>`
     - Conversation state management
   * - :doc:`Tool <../api/tools/index>`
     - Tool creation and integration

Import Examples
---------------

.. code-block:: python

   # Core imports
   from haive.core.engine.aug_llm import AugLLMConfig
   from haive.core.schema.prebuilt.messages_state import MessagesState
   
   # Agent imports
   from haive.agents.simple.agent import SimpleAgent
   from haive.agents.react.agent import ReactAgent
   from haive.agents.rag.base.agent import BaseRAGAgent
   
   # Tool imports
   from haive.tools import tool
   from haive.tools.web import WebSearchTool
   
   # Game imports
   from haive.games.chess import ChessGame
   from haive.games.framework import GameFramework

API Documentation Structure
---------------------------

The API documentation is organized hierarchically:

1. **Package Level** - Overview and main components
2. **Module Level** - Specific functionality areas  
3. **Class/Function Level** - Detailed API reference

Each package documentation includes:

- **Overview** - Purpose and main features
- **Quick Start** - Basic usage examples
- **API Reference** - Complete class and function documentation
- **Examples** - Real-world usage patterns
- **Best Practices** - Recommended patterns

Navigation Tips
---------------

.. tip::

   - Use the **search** feature to quickly find specific classes or functions
   - Check the **Module Index** for alphabetical listing
   - Browse the **Source Code** links to see implementations
   - Look for **Examples** sections in each module

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Package Documentation

   haive-core
   haive-agents
   haive-tools
   haive-games
   haive-mcp
   haive-dataflow
   haive-prebuilt

.. raw:: html

   <style>
   .packages-overview {
       margin: 2rem 0;
   }

   .package-stats {
       display: flex;
       justify-content: center;
       gap: 2rem;
       margin-bottom: 3rem;
   }

   .stat-card {
       text-align: center;
       padding: 1.5rem;
       background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
       border-radius: 1rem;
       min-width: 150px;
   }

   .stat-icon {
       font-size: 2.5rem;
       margin-bottom: 0.5rem;
   }

   .stat-number {
       font-size: 2rem;
       font-weight: bold;
       color: #2563eb;
   }

   .stat-label {
       font-size: 0.875rem;
       color: #6b7280;
       text-transform: uppercase;
       letter-spacing: 0.05em;
   }

   /* Dark mode support */
   @media (prefers-color-scheme: dark) {
       body[data-theme="dark"] .stat-card {
           background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
       }

       body[data-theme="dark"] .stat-number {
           color: #60a5fa;
       }

       body[data-theme="dark"] .stat-label {
           color: #9ca3af;
       }
   }
   </style>