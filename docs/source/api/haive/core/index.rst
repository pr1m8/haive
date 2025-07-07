Haive Core
==========

Core infrastructure and utilities

Modules
-------

.. grid:: 1 2 2 3
   :gutter: 3

   .. grid-item-card:: **Engine**
      :link: engine/index
      :link-type: doc
      
      8 submodules
   .. grid-item-card:: **Schema**
      :link: schema/index
      :link-type: doc
      
      4 submodules
   .. grid-item-card:: **Graph**
      :link: graph/index
      :link-type: doc
      
      6 submodules
   .. grid-item-card:: **Persistence**
      :link: persistence/index
      :link-type: doc
      
      3 submodules
   .. grid-item-card:: **Registry**
      :link: registry/index
      :link-type: doc
      
      3 submodules
   .. grid-item-card:: **Common**
      :link: common/index
      :link-type: doc
      
      3 submodules
   .. grid-item-card:: **Config**
      :link: config/index
      :link-type: doc
      
      Core module
   .. grid-item-card:: **Logging**
      :link: logging/index
      :link-type: doc
      
      Core module
   .. grid-item-card:: **Models**
      :link: models/index
      :link-type: doc
      
      4 submodules
   .. grid-item-card:: **Runtime**
      :link: runtime/index
      :link-type: doc
      
      2 submodules
   .. grid-item-card:: **Types**
      :link: types/index
      :link-type: doc
      
      Core module
   .. grid-item-card:: **Ui**
      :link: ui/index
      :link-type: doc
      
      Core module
   .. grid-item-card:: **Utils**
      :link: utils/index
      :link-type: doc
      
      Core module

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
