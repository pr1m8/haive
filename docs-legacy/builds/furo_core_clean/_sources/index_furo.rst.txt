🤖 Haive AI Agent Framework - Clean Build
==========================================

Welcome to Haive, a professional framework for building sophisticated AI agents.

.. note::
   This is a clean build with minimal features for testing purposes.

Overview
--------

The Haive framework provides:

- **Core Engine System** - LLM integration and configuration
- **Agent Implementations** - Pre-built conversational agents
- **Tool Integration** - Extensible tool ecosystem
- **Graph Workflows** - Complex multi-step processes
- **Game Environments** - AI game playing capabilities

Quick Start
-----------

.. code-block:: python

   from haive.core.engine.aug_llm import AugLLMConfig
   from haive.agents.simple.agent import SimpleAgent

   # Configure LLM
   config = AugLLMConfig(temperature=0.7)
   
   # Create agent
   agent = SimpleAgent(name="assistant", engine=config)
   
   # Run conversation
   response = agent.run("Hello!")
   print(response)

Navigation
----------

.. toctree::
   :maxdepth: 2
   :caption: Contents

   self
   quickstart
   installation

Packages
--------

The Haive framework is organized into focused packages. Below is the API documentation for each package with proper ``haive.*`` namespacing:

.. toctree::
   :maxdepth: 3
   :caption: Package APIs
   :titlesonly:

   api/haive/index

Installation
------------

.. code-block:: bash

   # Install full framework
   pip install haive

   # Or install specific packages
   pip install haive-core haive-agents

GitHub Repository
-----------------

Visit our GitHub repository: https://github.com/will-astley/haive

License
-------

MIT License - see the repository for details.