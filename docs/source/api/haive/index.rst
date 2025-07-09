Haive API Reference
===================

The complete API reference for the Haive framework - your gateway to building intelligent agents.

.. note::
   **New to Haive?** Start with :doc:`../../introduction/index` or explore the :doc:`../../games/index` for interactive examples.

Core Packages
-------------

Essential foundation packages for building agents:

.. grid:: 1 2 2 2
   :gutter: 4

   .. grid-item-card:: 🏗️ **Haive Core**
      :link: core/index
      :link-type: doc
      :class-header: text-center
      :class-body: text-center
      
      Core infrastructure, engines, schemas, and graph workflows
      
      :bdg-primary:`Foundation` :bdg-secondary:`Essential`

   .. grid-item-card:: 🤖 **Haive Agents**
      :link: agents/index
      :link-type: doc
      :class-header: text-center
      :class-body: text-center
      
      Pre-built agent implementations for various use cases
      
      :bdg-success:`Ready-to-use` :bdg-info:`Intelligent`

Specialized Packages
--------------------

Domain-specific packages for targeted use cases:

.. grid:: 1 2 3 3
   :gutter: 3

   .. grid-item-card:: 🎮 **Haive Games**
      :link: games/index
      :link-type: doc
      :class-header: text-center
      :class-body: text-center
      
      Game environments and AI opponents
      
      :bdg-warning:`Interactive` :bdg-danger:`AI Opponents`

   .. grid-item-card:: 🔧 **Haive Tools**
      :link: tools/index
      :link-type: doc
      :class-header: text-center
      :class-body: text-center
      
      Tools and utilities for agent workflows
      
      :bdg-info:`Utilities` :bdg-primary:`Extensible`

   .. grid-item-card:: 🔄 **Haive Dataflow**
      :link: dataflow/index
      :link-type: doc
      :class-header: text-center
      :class-body: text-center
      
      Data processing and streaming pipelines
      
      :bdg-success:`Streaming` :bdg-secondary:`Processing`

Integration Packages
--------------------

Connectivity and deployment packages:

.. grid:: 1 2 2 2
   :gutter: 4

   .. grid-item-card:: 🔌 **Haive MCP**
      :link: mcp/index
      :link-type: doc
      :class-header: text-center
      :class-body: text-center
      
      Model Context Protocol integration for seamless LLM connectivity
      
      :bdg-light:`Protocol` :bdg-dark:`Integration`

   .. grid-item-card:: 📦 **Haive Prebuilt**
      :link: prebuilt/index
      :link-type: doc
      :class-header: text-center
      :class-body: text-center
      
      Pre-configured solutions and templates
      
      :bdg-light:`Templates` :bdg-dark:`Solutions`

.. toctree::
   :maxdepth: 4
   :caption: API Reference
   :hidden:
   
   core/index
   agents/index
   tools/index
   games/index
   dataflow/index
   prebuilt/index
   mcp/index

Navigation
----------

The API documentation is organized hierarchically:

- **haive** (root)
  
  - **core** → engine → base, aug_llm, document...
  - **agents** → simple → structured, v2...
  - **tools** → search, math, api...
  
Each level provides both an overview and direct access to submodules.

Quick Links
-----------

* :ref:`genindex` - Complete index of all modules, classes, and functions
* :ref:`modindex` - Quick module finder
* :ref:`search` - Search the documentation
