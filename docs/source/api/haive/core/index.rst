Haive Core
==========

The foundation of the Haive framework - core infrastructure, engines, and utilities for building intelligent agents.

.. tip::
   **Quick Start**: Most users start with :doc:`engine/index` for LLM integration and :doc:`schema/index` for state management.

Core Components
---------------

Essential components for agent development:

.. grid:: 1 2 3 3
   :gutter: 3

   .. grid-item-card:: ⚙️ **Engine**
      :link: engine/index
      :link-type: doc
      :class-header: text-center
      :class-body: text-center
      
      LLM engines, embeddings, and retrieval systems
      
      :bdg-primary:`8 modules` :bdg-secondary:`Essential`

   .. grid-item-card:: 📋 **Schema**
      :link: schema/index
      :link-type: doc
      :class-header: text-center
      :class-body: text-center
      
      State management and schema composition
      
      :bdg-success:`4 modules` :bdg-info:`Type-safe`

   .. grid-item-card:: 🔄 **Graph**
      :link: graph/index
      :link-type: doc
      :class-header: text-center
      :class-body: text-center
      
      Workflow graphs, nodes, and routing patterns
      
      :bdg-warning:`6 modules` :bdg-danger:`Workflows`

Infrastructure
--------------

Supporting infrastructure and utilities:

.. grid:: 1 2 3 3
   :gutter: 3

   .. grid-item-card:: 💾 **Persistence**
      :link: persistence/index
      :link-type: doc
      :class-header: text-center
      :class-body: text-center
      
      Data storage and state persistence
      
      :bdg-light:`3 modules` :bdg-dark:`Storage`

   .. grid-item-card:: 📚 **Registry**
      :link: registry/index
      :link-type: doc
      :class-header: text-center
      :class-body: text-center
      
      Component registration and discovery
      
      :bdg-light:`3 modules` :bdg-dark:`Registry`

   .. grid-item-card:: 🔧 **Common**
      :link: common/index
      :link-type: doc
      :class-header: text-center
      :class-body: text-center
      
      Shared utilities and base classes
      
      :bdg-light:`3 modules` :bdg-dark:`Utilities`

   .. grid-item-card:: 🎭 **Models**
      :link: models/index
      :link-type: doc
      :class-header: text-center
      :class-body: text-center
      
      LLM models and embedding interfaces
      
      :bdg-primary:`4 modules` :bdg-secondary:`Models`

   .. grid-item-card:: 🚀 **Runtime**
      :link: runtime/index
      :link-type: doc
      :class-header: text-center
      :class-body: text-center
      
      Runtime environment and extensions
      
      :bdg-success:`2 modules` :bdg-info:`Runtime`

   .. grid-item-card:: 🖥️ **UI**
      :link: ui/index
      :link-type: doc
      :class-header: text-center
      :class-body: text-center
      
      User interface components
      
      :bdg-warning:`Core` :bdg-danger:`Interface`

System Utilities
----------------

Configuration and system utilities:

.. grid:: 1 2 3 3
   :gutter: 3

   .. grid-item-card:: ⚙️ **Config**
      :link: config/index
      :link-type: doc
      :class-header: text-center
      :class-body: text-center
      
      Configuration management and settings
      
      :bdg-light:`Core` :bdg-dark:`Config`

   .. grid-item-card:: 📝 **Logging**
      :link: logging/index
      :link-type: doc
      :class-header: text-center
      :class-body: text-center
      
      Structured logging and monitoring
      
      :bdg-light:`Core` :bdg-dark:`Logging`

   .. grid-item-card:: 🏷️ **Types**
      :link: types/index
      :link-type: doc
      :class-header: text-center
      :class-body: text-center
      
      Type definitions and annotations
      
      :bdg-light:`Core` :bdg-dark:`Types`

   .. grid-item-card:: 🛠️ **Utils**
      :link: utils/index
      :link-type: doc
      :class-header: text-center
      :class-body: text-center
      
      General utilities and helper functions
      
      :bdg-light:`Core` :bdg-dark:`Utils`

.. toctree::
   :maxdepth: 3
   :caption: Core Modules
   :hidden:
   
   engine/index
   schema/index
   graph/index
   persistence/index
   registry/index
   common/index
   config/index
   logging/index
   models/index
   runtime/index
   types/index
   ui/index
   utils/index

Module Path
-----------

.. code-block:: python

   import haive.core
   # or
   from haive.core import *

Package Structure
-----------------

This package contains the following module hierarchy:


**engine**
  - base
  - aug_llm
  - document
  - agent
  - embedding
  - retriever
  - vectorstore
  - tool

**schema**
  - state_schema
  - schema_composer
  - compatibility
  - prebuilt

**graph**
  - state_graph
  - node
  - patterns
  - routers
  - branches
  - utils

**persistence**
  - store
  - handlers
  - factory

**registry**
  - base
  - decorators
  - manager

**common**
  - mixins
  - models
  - types

**config**
  - *(no submodules)*

**logging**
  - *(no submodules)*

**models**
  - llm
  - embeddings
  - retriever
  - vectorstore

**runtime**
  - base
  - extension

**types**
  - *(no submodules)*

**ui**
  - *(no submodules)*

**utils**
  - *(no submodules)*
