🤖 Haive Documentation
======================

.. card:: 🤖 Professional AI Agent Framework
   :class-card: hero-section
   :text-align: center
   
   Build sophisticated AI agents with conversational AI, game intelligence, tool orchestration,
   and knowledge systems. Modern Python framework with auto-persistence and multi-agent coordination.
   
   Professional AI agent framework for Python developers.

🚀 Quick Start
================

⚡ **Get Started in Minutes**

.. code-block:: python

   # Install Haive
   pip install haive-agents

   # Create your first agent
   from haive.agents import SimpleAgent
   from haive.core.engine.aug_llm import AugLLMConfig

   # Configure agent
   config = AugLLMConfig(
       model="gpt-4",
       temperature=0.7,
       system_message="You are a helpful AI assistant."
   )

   # Create and run agent
   agent = SimpleAgent(name="assistant", engine=config)
   response = await agent.arun("Hello, world!")
   print(response)

🎯 Core Capabilities
===================

Explore the main features of the Haive framework

.. grid:: 1 2 3 3
   :gutter: 3
   :padding: 2

   .. grid-item-card:: 🧠 AI Agents
      :link: agents/index
      :class-header: bg-primary text-white
      :shadow: lg
      
      **Conversational Intelligence**
      
      Build intelligent agents with memory, personality, and advanced reasoning capabilities.
      
      +++
      
      .. badge:: SimpleAgent
         :color: primary
         
      .. badge:: ReactAgent  
         :color: secondary
         
      .. badge:: RAG Systems
         :color: info

   .. grid-item-card:: 🎮 Game Intelligence
      :link: games/index
      :class-header: bg-success text-white
      :shadow: lg
      
      **Strategic Gameplay**
      
      Create AI opponents for Chess, Go, Poker, and other strategic games with advanced algorithms.
      
      +++
      
      .. badge:: Chess Engine
         :color: success
         
      .. badge:: Board Games
         :color: success
         
      .. badge:: AI Strategies
         :color: success

   .. grid-item-card:: 🔧 Tool Orchestration
      :link: tools/index
      :class-header: bg-info text-white
      :shadow: lg
      
      **External Integrations**
      
      Connect agents to APIs, databases, search engines, and external services seamlessly.
      
      +++
      
      .. badge:: Web APIs
         :color: info
         
      .. badge:: Databases
         :color: info
         
      .. badge:: Search Tools
         :color: info

   .. grid-item-card:: 🔄 Dynamic MCP Integration
      :link: mcp/index
      :class-header: bg-warning text-white
      :shadow: lg
      
      **1,960+ Servers • Hot-Reload • AI Discovery**
      
      Intelligent MCP server discovery with hot-reload capabilities and HITL approval.
      
      +++
      
      .. badge:: Auto-Discovery
         :color: warning
         
      .. badge:: Hot-Reload
         :color: warning
         
      .. badge:: HITL Approval
         :color: warning

   .. grid-item-card:: 📖 API Reference
      :link: api/index
      :class-header: bg-secondary text-white
      :shadow: lg
      
      **Complete Documentation**
      
      Comprehensive API documentation with examples, guides, and implementation details.
      
      +++
      
      .. badge:: Core API
         :color: secondary
         
      .. badge:: Agent Classes
         :color: secondary
         
      .. badge:: Tools API
         :color: secondary

   .. grid-item-card:: 📚 Guides & Examples
      :link: guides/index
      :class-header: bg-dark text-white
      :shadow: lg
      
      **Learn by Doing**
      
      Step-by-step tutorials, implementation guides, and real-world examples to get started.
      
      +++
      
      .. badge:: Tutorials
         :color: dark
         
      .. badge:: Examples
         :color: dark
         
      .. badge:: Best Practices
         :color: dark

.. toctree::
   :maxdepth: 2
   :caption: 📚 Getting Started

   introduction/index

.. toctree::
   :maxdepth: 2
   :caption: 🤖 Agent Showcase

   agents/index
   agents/simple/index
   agents/react/index
   agents/rag/index
   agents/multi/index

.. toctree::
   :maxdepth: 2
   :caption: 🎮 Games

   games/index
   games/chess/index

.. toctree::
   :maxdepth: 2
   :caption: 🔧 Tools

   tools/index
   tools/search/index

.. toctree::
   :maxdepth: 2
   :caption: 📡 MCP Integration

   mcp/index
   mcp/dynamic-mcp
   mcp/servers
   mcp/setup

.. toctree::
   :maxdepth: 2
   :caption: 📖 API Reference

   api/index

.. toctree::
   :maxdepth: 2
   :caption: 🧑‍💻 Guides & Examples

   gallery
   guides/index
   examples/index
   reference/index

Quick Links
-----------

- :doc:`api/index` - Complete API Reference
- :doc:`api/src/haive/core/index` - Core infrastructure
- :doc:`api/src/haive/agents/index` - Agent implementations
- :ref:`genindex` - Complete index
- :ref:`modindex` - Module index
- :ref:`search` - Search documentation

Package Status
^^^^^^^^^^^^^^

.. raw:: html

   <div class="package-status">
       <div class="status-item">
           <span class="status-icon">🚀</span>
           <strong>haive-core</strong>
           <span class="status-badge stable">Stable</span>
       </div>
       <div class="status-item">
           <span class="status-icon">🤖</span>
           <strong>haive-agents</strong>
           <span class="status-badge stable">Stable</span>
       </div>
       <div class="status-item">
           <span class="status-icon">🛠️</span>
           <strong>haive-tools</strong>
           <span class="status-badge stable">Stable</span>
       </div>
       <div class="status-item">
           <span class="status-icon">🎮</span>
           <strong>haive-games</strong>
           <span class="status-badge beta">Beta</span>
       </div>
       <div class="status-item">
           <span class="status-icon">📡</span>
           <strong>haive-mcp</strong>
           <span class="status-badge beta">Beta</span>
       </div>
   </div>

   <style>
   .package-status {
       display: flex;
       flex-wrap: wrap;
       gap: 1rem;
       margin: 1rem 0;
       padding: 1rem;
       background: #f8fafc;
       border-radius: 8px;
       border: 1px solid #e2e8f0;
   }

   .status-item {
       display: flex;
       align-items: center;
       gap: 0.5rem;
       padding: 0.5rem 1rem;
       background: white;
       border-radius: 6px;
       border: 1px solid #e2e8f0;
       font-size: 0.9rem;
   }

   .status-icon {
       font-size: 1.2rem;
   }

   .status-badge {
       padding: 0.25rem 0.5rem;
       border-radius: 4px;
       font-size: 0.75rem;
       font-weight: 600;
       text-transform: uppercase;
   }

   .status-badge.stable {
       background: #dcfce7;
       color: #166534;
   }

   .status-badge.beta {
       background: #fef3c7;
       color: #92400e;
   }
   </style>

What's New
----------

.. note::

   **New Navigation Structure!**

   The API documentation now uses a hierarchical structure with Haive as the root.
   Navigate through packages → modules → submodules for better organization.

Latest Updates
^^^^^^^^^^^^^^

- Restructured API documentation for better navigation
- Added contextual navigation that changes based on your location
- Improved module discovery and documentation generation
