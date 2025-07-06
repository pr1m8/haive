Haive Core
==========

.. include:: ../../../packages/haive-core/README.md
   :parser: myst_parser.sphinx_

Core Components Gallery
-----------------------

The Haive Core package provides the fundamental building blocks for the entire framework.

.. grid:: 1 2 2 3
   :gutter: 3

   .. grid-item-card:: 🌐 **Graph System**
      :link: generated/haive.core.graph
      :link-type: doc
      
      State machines and workflow orchestration
      
      **Features:** Nodes, edges, state management, execution

   .. grid-item-card:: 🤖 **Engine System**
      :link: modules/haive.core.engine
      :link-type: doc
      
      LLM integration and augmentation
      
      **Provides:** Multi-provider support, streaming, tools

   .. grid-item-card:: 📊 **Schema System**
      :link: modules/haive.core.schema
      :link-type: doc
      
      Dynamic state schema composition
      
      **Includes:** Validation, mixins, type safety

   .. grid-item-card:: 💾 **Persistence**
      :link: modules/haive.core.persistence
      :link-type: doc
      
      State persistence and recovery
      
      **Supports:** Multiple backends, auto-save, history

   .. grid-item-card:: 📖 **Registry**
      :link: modules/haive.core.registry
      :link-type: doc
      
      Component registration and discovery
      
      **Manages:** Engines, tools, agents, schemas

   .. grid-item-card:: 🔧 **Tools & Utils**
      :link: modules/haive.core.tools
      :link-type: doc
      
      Core utilities and tool system
      
      **Contains:** Helpers, validators, tool protocols

Core Modules
~~~~~~~~~~~~

.. toctree::
   :maxdepth: 2
   :caption: Core Components
   
   generated/haive.core
   generated/haive.core.engine
   generated/haive.core.graph
   generated/haive.core.schema
   generated/haive.core.persistence
   generated/haive.core.registry
   generated/haive.core.tools
   generated/haive.core.utils

Engine System
~~~~~~~~~~~~~

.. toctree::
   :maxdepth: 2
   :caption: Engine & LLM
   
   generated/haive.core.engine.base
   generated/haive.core.engine.engine
   generated/haive.core.engine.aug_llm
   generated/haive.core.engine.protocol

Graph System
~~~~~~~~~~~~

.. toctree::
   :maxdepth: 2
   :caption: Graph Architecture
   
   generated/haive.core.graph.state
   generated/haive.core.graph.nodes
   generated/haive.core.graph.edges
   generated/haive.core.graph.builder

Schema System
~~~~~~~~~~~~~

.. toctree::
   :maxdepth: 2
   :caption: State Management
   
   generated/haive.core.schema.state_schema
   generated/haive.core.schema.schema_composer
   generated/haive.core.schema.validation
   generated/haive.core.schema.mixins

Quick Reference
~~~~~~~~~~~~~~~

**Engine Configuration**

.. code-block:: python

   from haive.core.engine import AugLLMConfig, get_llm
   
   # Configure an LLM
   engine = AugLLMConfig(
       model="gpt-4",
       temperature=0.7,
       system_message="You are a helpful assistant"
   )
   
   # Or use the registry
   llm = get_llm("gpt-4")

**State Schema**

.. code-block:: python

   from haive.core.schema import BaseStateSchema
   from typing import List
   
   class MyAgentState(BaseStateSchema):
       messages: List[str] = []
       context: Dict[str, Any] = {}
       
       class Config:
           schema_id = "my_agent_state_v1"

**Graph Building**

.. code-block:: python

   from haive.core.graph import GraphBuilder
   
   builder = GraphBuilder()
   builder.add_node("start", start_node)
   builder.add_node("process", process_node)
   builder.add_edge("start", "process")
   
   graph = builder.compile()

Module Index
~~~~~~~~~~~~

Core modules with detailed API documentation:

.. toctree::
   :maxdepth: 2

   modules/haive.core.engine
   modules/haive.core.schema
   modules/haive.core.persistence
   modules/haive.core.registry
   modules/haive.core.tools

Detailed Module Structure
~~~~~~~~~~~~~~~~~~~~~~~~~

.. toctree::
   :maxdepth: 4
   :caption: Core Package Structure
   
   generated/haive.core

**Note**: The recursive documentation structure will be displayed after building the documentation with autosummary enabled.