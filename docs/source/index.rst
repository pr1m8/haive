🤖 Haive Documentation
======================

.. raw:: html

   <div class="agent-hero-section">
      <div class="hero-content">
         <h2>🤖 Professional AI Agent Framework</h2>
         <p class="hero-description">
            Build sophisticated AI agents with conversational AI, game intelligence, tool orchestration,
            and knowledge systems. Modern Python framework with auto-persistence and multi-agent coordination.
         </p>
      </div>
   </div>

Professional AI agent framework for Python developers.

.. raw:: html

   <div class="showcase-section">
      <div class="showcase-header">
         <h2>🚀 Quick Start</h2>
      </div>

      <div class="code-example-section">
         <h4>⚡ Get Started in Minutes</h4>
      </div>
   </div>

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

.. raw:: html

   <div class="showcase-section">
      <div class="showcase-header">
         <h2>🎯 Core Capabilities</h2>
         <p>Explore the main features of the Haive framework</p>
      </div>

      <div class="agent-showcase">
         <div class="agent-card">
            <div class="agent-header">
               <div class="agent-emoji">🧠</div>
               <div>
                  <h3 class="agent-title">AI Agents</h3>
                  <p class="agent-subtitle">Conversational intelligence</p>
               </div>
            </div>
            <p class="agent-description">
               Build intelligent agents with memory, personality, and advanced reasoning capabilities.
            </p>
            <div class="agent-features">
               <span class="feature-tag">SimpleAgent</span>
               <span class="feature-tag">ReactAgent</span>
               <span class="feature-tag">RAG Systems</span>
            </div>
            <a href="agents/index.html" class="agent-link">Browse Agents</a>
         </div>

         <div class="agent-card">
            <div class="agent-header">
               <div class="agent-emoji">🎮</div>
               <div>
                  <h3 class="agent-title">Game Intelligence</h3>
                  <p class="agent-subtitle">Strategic gameplay</p>
               </div>
            </div>
            <p class="agent-description">
               Create AI opponents for Chess, Go, Poker, and other strategic games with advanced algorithms.
            </p>
            <div class="agent-features">
               <span class="feature-tag">Chess Engine</span>
               <span class="feature-tag">Board Games</span>
               <span class="feature-tag">AI Strategies</span>
            </div>
            <a href="games/index.html" class="agent-link">View Games</a>
         </div>

         <div class="agent-card">
            <div class="agent-header">
               <div class="agent-emoji">🔧</div>
               <div>
                  <h3 class="agent-title">Tool Orchestration</h3>
                  <p class="agent-subtitle">External integrations</p>
               </div>
            </div>
            <p class="agent-description">
               Connect agents to APIs, databases, search engines, and external services seamlessly.
            </p>
            <div class="agent-features">
               <span class="feature-tag">Web APIs</span>
               <span class="feature-tag">Databases</span>
               <span class="feature-tag">Search Tools</span>
            </div>
            <a href="tools/index.html" class="agent-link">Browse Tools</a>
         </div>

         <div class="agent-card">
            <div class="agent-header">
               <div class="agent-emoji">🔄</div>
               <div>
                  <h3 class="agent-title">Dynamic MCP Integration</h3>
                  <p class="agent-subtitle">1,960+ Servers • Hot-Reload • AI Discovery</p>
               </div>
            </div>
            <p class="agent-description">
               Intelligent MCP server discovery with hot-reload capabilities and HITL approval.
               Access 1,960+ pre-indexed servers with AI-powered discovery.
            </p>
            <div class="agent-features">
               <span class="feature-tag">Auto-Discovery</span>
               <span class="feature-tag">Hot-Reload</span>
               <span class="feature-tag">HITL Approval</span>
            </div>
            <a href="mcp/index.html" class="agent-link">MCP Integration</a>
         </div>

         <div class="agent-card">
            <div class="agent-header">
               <div class="agent-emoji">📖</div>
               <div>
                  <h3 class="agent-title">API Reference</h3>
                  <p class="agent-subtitle">Complete documentation</p>
               </div>
            </div>
            <p class="agent-description">
               Comprehensive API documentation with examples, guides, and implementation details.
            </p>
            <div class="agent-features">
               <span class="feature-tag">Core API</span>
               <span class="feature-tag">Agent Classes</span>
               <span class="feature-tag">Tools API</span>
            </div>
            <a href="api/index.html" class="agent-link">View API Reference</a>
         </div>

         <div class="agent-card">
            <div class="agent-header">
               <div class="agent-emoji">📚</div>
               <div>
                  <h3 class="agent-title">Guides & Examples</h3>
                  <p class="agent-subtitle">Learn by doing</p>
               </div>
            </div>
            <p class="agent-description">
               Step-by-step tutorials, implementation guides, and real-world examples to get you started.
            </p>
            <div class="agent-features">
               <span class="feature-tag">Tutorials</span>
               <span class="feature-tag">Examples</span>
               <span class="feature-tag">Best Practices</span>
            </div>
            <a href="guides/index.html" class="agent-link">Learn More</a>
         </div>
      </div>
   </div>

.. toctree::
   :maxdepth: 2
   :caption: 📚 Getting Started
   :hidden:

   introduction/index

.. toctree::
   :maxdepth: 2
   :caption: 🤖 Agent Showcase
   :hidden:

   agents/index
   agents/simple/index
   agents/react/index
   agents/rag/index
   agents/multi/index

.. toctree::
   :maxdepth: 2
   :caption: 🎮 Games
   :hidden:

   games/index
   games/chess/index

.. toctree::
   :maxdepth: 2
   :caption: 🔧 Tools
   :hidden:

   tools/index
   tools/search/index

.. toctree::
   :maxdepth: 2
   :caption: 📡 MCP Integration
   :hidden:

   mcp/index
   mcp/dynamic-mcp
   mcp/servers
   mcp/setup

.. toctree::
   :maxdepth: 2
   :caption: 📖 API Reference
   :hidden:

   api/index

.. toctree::
   :maxdepth: 2
   :caption: 🧑‍💻 Guides & Examples
   :hidden:

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
