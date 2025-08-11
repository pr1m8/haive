Haive AI Agent Framework
========================

.. raw:: html

   <div style="text-align: center; margin: 2em 0;">
     <h1 style="font-size: 3em; font-weight: 700; letter-spacing: -0.02em; margin: 0.5em 0;">
       🤖 Haive AI Agent Framework
     </h1>
     <p style="font-size: 1.5em; color: #6b7280; margin: 1em 0;">
       Build sophisticated AI agents with advanced reasoning, tool use, and multi-agent coordination
     </p>
     <div style="margin: 2em 0;">
       <a href="quickstart.html" style="background: #2563eb; color: white; padding: 0.75em 2em; border-radius: 6px; text-decoration: none; margin: 0 0.5em; display: inline-block;">
         Get Started →
       </a>
       <a href="https://github.com/will-astley/haive" style="background: #374151; color: white; padding: 0.75em 2em; border-radius: 6px; text-decoration: none; margin: 0 0.5em; display: inline-block;">
         View on GitHub
       </a>
     </div>
   </div>

.. grid:: 1 1 2 3
   :gutter: 3

   .. grid-item-card:: 🚀 Quick Start
      :link: quickstart
      :link-type: doc

      Get up and running with Haive in minutes. Learn the basics of creating
      and running AI agents.

   .. grid-item-card:: 📚 User Guide
      :link: guide/index
      :link-type: doc

      Comprehensive guides for building agents, using tools, and implementing
      advanced patterns.

   .. grid-item-card:: 🔧 API Reference
      :link: api/index
      :link-type: doc

      Complete API documentation for all packages, classes, and functions
      in the Haive framework.

.. grid:: 1 1 2 3
   :gutter: 3

   .. grid-item-card:: 🎯 Examples
      :link: examples/index
      :link-type: doc

      Real-world examples and tutorials showing how to build various types
      of AI agents.

   .. grid-item-card:: 🧩 Integrations
      :link: integrations/index
      :link-type: doc

      Connect Haive agents with external services, APIs, and tools through
      our integration guides.

   .. grid-item-card:: 🔌 MCP Servers
      :link: mcp/index
      :link-type: doc

      Model Context Protocol servers for extending agent capabilities with
      external data sources.

Key Features
------------

.. grid:: 1 1 2 2
   :gutter: 2

   .. grid-item::

      **🧠 Advanced Reasoning**
      
      Build agents with sophisticated reasoning capabilities using ReAct,
      Chain-of-Thought, and other advanced patterns.

   .. grid-item::

      **🛠️ Rich Tool Ecosystem**
      
      Extensive library of pre-built tools and seamless integration with
      LangChain tools and custom implementations.

   .. grid-item::

      **🔄 Multi-Agent Coordination**
      
      Create complex workflows with multiple specialized agents working
      together in sequential, parallel, or hierarchical patterns.

   .. grid-item::

      **💾 State Management**
      
      Robust state persistence, checkpointing, and recovery for long-running
      agent workflows and conversations.

Installation
------------

Install Haive using pip or poetry:

.. tabs::

   .. tab:: pip

      .. code-block:: bash

         pip install haive

   .. tab:: poetry

      .. code-block:: bash

         poetry add haive

   .. tab:: Development

      .. code-block:: bash

         git clone https://github.com/will-astley/haive.git
         cd haive
         poetry install --all-extras

Quick Example
-------------

Create your first AI agent in just a few lines:

.. code-block:: python

   from haive.agents.simple import SimpleAgent
   from haive.core.engine.aug_llm import AugLLMConfig

   # Create an agent with OpenAI GPT-4
   agent = SimpleAgent(
       name="assistant",
       engine=AugLLMConfig(
           model="gpt-4",
           temperature=0.7,
           system_message="You are a helpful AI assistant."
       )
   )

   # Run the agent
   response = agent.run("What can you help me with?")
   print(response)

Documentation Structure
-----------------------

.. toctree::
   :maxdepth: 2
   :caption: Getting Started
   :hidden:

   quickstart
   installation
   concepts
   first_agent

.. toctree::
   :maxdepth: 2
   :caption: User Guide
   :hidden:

   guide/index
   guide/agents/index
   guide/tools/index
   guide/multi_agent/index
   guide/state_management/index
   guide/best_practices

.. toctree::
   :maxdepth: 2
   :caption: Examples
   :hidden:

   examples/index
   examples/simple_agents
   examples/react_agents
   examples/multi_agent_workflows
   examples/rag_systems
   examples/game_agents

.. toctree::
   :maxdepth: 2
   :caption: API Reference
   :hidden:

   api/index
   api/src/haive/core/index
   api/src/haive/agents/index
   api/src/haive/tools/index
   api/src/haive/games/index
   api/src/haive/dataflow/index
   api/src/haive/mcp/index
   api/src/haive/prebuilt/index

.. toctree::
   :maxdepth: 2
   :caption: Integrations
   :hidden:

   integrations/index
   integrations/langchain
   integrations/openai
   integrations/anthropic
   integrations/huggingface
   integrations/databases
   integrations/vector_stores

.. toctree::
   :maxdepth: 1
   :caption: MCP Documentation
   :hidden:

   mcp/index
   mcp/servers/index
   mcp/development
   mcp/deployment

.. toctree::
   :maxdepth: 1
   :caption: Developer Guide
   :hidden:

   development/contributing
   development/architecture
   development/testing
   development/plugins
   development/changelog

.. toctree::
   :maxdepth: 1
   :caption: Resources
   :hidden:

   resources/faq
   resources/troubleshooting
   resources/performance
   resources/security
   resources/glossary

Package Overview
----------------

The Haive framework consists of several specialized packages:

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - Package
     - Description
   * - **haive-core**
     - Core engine, state management, and base classes
   * - **haive-agents**
     - Pre-built agent implementations (Simple, ReAct, RAG, etc.)
   * - **haive-tools**
     - Tool library and integrations
   * - **haive-games**
     - Game environments and game-playing agents
   * - **haive-dataflow**
     - Streaming and data processing capabilities
   * - **haive-mcp**
     - Model Context Protocol server integrations
   * - **haive-prebuilt**
     - Ready-to-use agent configurations

Community & Support
-------------------

.. grid:: 1 1 3 3
   :gutter: 2

   .. grid-item::
      
      **📖 Documentation**
      
      - :doc:`guide/index`
      - :doc:`api/index`
      - :doc:`examples/index`

   .. grid-item::
      
      **💬 Community**
      
      - `GitHub Discussions <https://github.com/will-astley/haive/discussions>`_
      - `Discord Server <https://discord.gg/haive>`_
      - `Stack Overflow <https://stackoverflow.com/questions/tagged/haive>`_

   .. grid-item::
      
      **🐛 Issues & Features**
      
      - `Report Issues <https://github.com/will-astley/haive/issues>`_
      - `Request Features <https://github.com/will-astley/haive/issues/new?labels=enhancement>`_
      - `Contribute <https://github.com/will-astley/haive/blob/main/CONTRIBUTING.md>`_

License
-------

Haive is released under the MIT License. See the `LICENSE <https://github.com/will-astley/haive/blob/main/LICENSE>`_ file for details.

Indices and Tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. note::

   Haive is under active development. APIs may change between versions.
   Always refer to the :doc:`development/changelog` for migration guides.