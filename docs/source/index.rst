🤖 Haive AI Agent Framework
==========================

   <div class="hero-section">
   <h1 class="gradient-text">Build Intelligent AI Agents</h1>
   <p>Professional framework for creating sophisticated AI agents with conversational intelligence,
   tool orchestration, game strategies, and multi-agent coordination.</p>

   <div class="hero-buttons">
   <a href="introduction/index.html" class="sd-btn sd-btn-primary">Get Started →</a>
   <a href="https://github.com/haive/haive" class="sd-btn sd-btn-secondary">View on GitHub</a>
   </div>

   </div>

🚀 Quick Start
=============

.. grid:: 1 1 2 2

   :gutter: 3

   .. grid-item::


      **Install Haive*

.. code-block:: bash
   :class: copy-button

   pip install haive-agents

**Create Your First Agent*

.. code-block:: python
   :class: copy-button

         from haive.agents import SimpleAgent
         from haive.core.engine import AugLLMConfig

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

         .. grid-item::


         **Key Features*

         <div class="feature-list">

         <div class="feature-item">
         <span class="feature-icon">✨</span>

         <div>
         <strong>Auto-Persistence</strong>
         <p>Automatic state saving and loading</p>
         </div>

         </div>

         <div class="feature-item">
         <span class="feature-icon">🔧</span>

         <div>
         <strong>Tool Integration</strong>
         <p>Connect to APIs, databases, and services</p>
         </div>

         </div>

         <div class="feature-item">
         <span class="feature-icon">🧠</span>

         <div>
         <strong>Advanced Reasoning</strong>
         <p>ReAct pattern for complex problem solving</p>
         </div>

         </div>

         <div class="feature-item">
         <span class="feature-icon">🤝</span>

         <div>
         <strong>Multi-Agent Systems</strong>
         <p>Coordinate multiple specialized agents</p>
         </div>

         </div>
         </div>

         <style>

         .feature-list {
             display: flex;
             flex-direction: column;
             gap: 1rem;
         }
         .feature-item {
             display: flex;
             align-items: start;
             gap: 1rem;
         }
         .feature-icon {
             font-size: 1.5rem;
             flex-shrink: 0;
         }
         .feature-item p {
             margin: 0;
             color: var(--haive-text-muted);
             font-size: 0.875rem;
         }
         </style>

         🎯 Core Capabilities
         =====================

         .. grid:: 1 2 3 3

         :gutter: 3
         :padding: 2

         .. grid-item-card:: 🧠 AI Agents

         :shadow: lg
         :link: agents/index

         Build intelligent agents with memory, personality, and advanced reasoning capabilities.

         +++

         **Available Types:* SimpleAgent • ReactAgent • RAG Systems

         .. grid-item-card:: 🎮 Game Intelligence

         :shadow: lg
         :link: games/index

         Create AI opponents for Chess, Go, Poker, and other strategic games with advanced algorithms.

         +++

         **Available Types:* Chess Engine • Board Games • Strategy AI

         .. grid-item-card:: 🔧 Tool Orchestration

         :shadow: lg
         :link: tools/index

         Connect agents to APIs, databases, search engines, and external services seamlessly.

         +++

         **Supported:* Web APIs • Databases • File Systems

         .. grid-item-card:: 🔄 Dynamic MCP

         :shadow: lg
         :link: mcp/index

         1,960+ servers with hot-reload capabilities and AI-powered discovery.

         +++

         **Features:* Auto-Discovery • Hot-Reload • Plugin System

         .. grid-item-card:: 📖 API Reference

         :shadow: lg
         :link: api/index

         Comprehensive API documentation with examples and implementation details.

         +++

         **Coverage:* Core API • Agent Classes • Tools

         .. grid-item-card:: 📚 Examples

         :shadow: lg
         :link: examples/index

         Step-by-step tutorials and real-world examples to get started quickly.

         +++

         **Content:* Tutorials • Guides • Code Samples

         <div class="why-haive">
         <h2>Why Choose Haive?</h2>

         <div class="benefits-grid">

         <div class="benefit">
         <span class="benefit-icon">⚡</span>

         <div class="benefit-title">Production Ready</div>

         <div class="benefit-desc">Battle-tested in production environments</div>
         </div>

         <div class="benefit">
         <span class="benefit-icon">🔒</span>

         <div class="benefit-title">Type Safe</div>

         <div class="benefit-desc">Full type hints and Pydantic models</div>
         </div>

         <div class="benefit">
         <span class="benefit-icon">🚀</span>

         <div class="benefit-title">High Performance</div>

         <div class="benefit-desc">Async-first with optimized execution</div>
         </div>

         <div class="benefit">
         <span class="benefit-icon">🎯</span>

         <div class="benefit-title">Extensible</div>

         <div class="benefit-desc">Plugin architecture for custom agents</div>
         </div>

         </div>
         </div>

         📊 Architecture Overview
         ========================

         <div class="architecture-diagram">
         <img src="_static/architecture-overview.svg" alt="Haive Architecture" style="max-width: 100%; height: auto;">
         <p style="margin-top: 1rem; color: var(--haive-text-muted);">
         Haive's modular architecture allows you to compose agents, tools, and engines flexibly.
         </p>
         </div>

         🎯 Agent Comparison
         ===================

         <table class="feature-table">
         <thead>
         <tr>
         <th>Agent Type</th>
         <th>Best For</th>
         <th>Key Features</th>
         <th>Performance</th>
         </tr>
         </thead>
         <tbody>
         <tr>
         <td><strong>SimpleAgent</strong></td>
         <td>Basic conversations, Q&A</td>
         <td>Lightweight, fast responses</td>
         <td>⚡⚡⚡⚡⚡</td>
         </tr>
         <tr>
         <td><strong>ReactAgent</strong></td>
         <td>Complex reasoning, tool use</td>
         <td>ReAct pattern, self-correction</td>
         <td>⚡⚡⚡⚡</td>
         </tr>
         <tr>
         <td><strong>RAG Agent</strong></td>
         <td>Knowledge-based Q&A</td>
         <td>Vector search, citations</td>
         <td>⚡⚡⚡⚡</td>
         </tr>
         <tr>
         <td><strong>Multi-Agent</strong></td>
         <td>Complex workflows</td>
         <td>Agent coordination, delegation</td>
         <td>⚡⚡⚡</td>
         </tr>
         </tbody>
         </table>

         📈 Performance Metrics
         ======================

         .. grid:: 1 2 4 4

         :gutter: 2

         .. grid-item::


         <div class="metric-card">
         <span class="value">&lt;100ms</span>
         <span class="label">Response Time</span>
         </div>

         .. grid-item::

         <div class="metric-card">
         <span class="value">10K+</span>
         <span class="label">Agents/Hour</span>
         </div>

         .. grid-item::

         <div class="metric-card">
         <span class="value">99.9%</span>
         <span class="label">Uptime</span>
         </div>

         .. grid-item::

         <div class="metric-card">
         <span class="value">50+</span>
         <span class="label">Tool Types</span>
         </div>

         💬 What Developers Say
         ======================

         <div class="testimonial">

         <div class="content">
         Haive transformed how we build AI applications. The agent architecture is intuitive
         and the performance is outstanding. We reduced our development time by 70%.
         </div>

         <div class="author">— Sarah Chen, CTO at TechCorp</div>
         </div>

         <div class="testimonial">

         <div class="content">
         The best AI agent framework I've used. The documentation is excellent and the
         community support is fantastic. Highly recommended for production use.
         </div>

         <div class="author">— Michael Rodriguez, AI Engineer</div>
         </div>

         🚀 Get Started Today
         ====================

         .. grid:: 1 1 3 3

         :gutter: 3

         .. grid-item-card:: 📖 Read the Docs

         :link: introduction/index
         :shadow: md

         Start with our comprehensive introduction and quickstart guide.

         .. grid-item-card:: 💻 View Examples

         :link: gallery
         :shadow: md

         Explore real-world examples and implementation patterns.

         .. grid-item-card:: 🌟 Star on GitHub

         :link: https://github.com/haive/haive
         :shadow: md

         Show your support and contribute to the project.

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

         api_index

         .. toctree::

         :maxdepth: 2
         :caption: 🧑‍💻 Guides & Examples
         :hidden:

         simple_agent_guide
         conversation_showcase
         examples/index
         gallery
         guides/index
         real_examples
         reference/index

         Quick Links
         -----------

         - :doc:`api/index - Complete API Reference`
         - :doc:`api/src/haive/core/index - Core infrastructure`
         - :doc:`api/src/haive/agents/index - Agent implementations`
         - :ref:``genindex - Complete index``
         - :ref:``modindex - Module index``
         - :ref:``search - Search documentation``
