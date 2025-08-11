Haive Core Documentation
========================

Core infrastructure for the Haive AI Agent Framework.

Overview
--------

Haive Core provides the foundational components for building AI agents:

- **Engine** - LLM configuration and execution
- **Schema** - Type-safe state management with Pydantic
- **Graph** - Workflow orchestration with LangGraph
- **Memory** - Conversation and context persistence
- **Utils** - Common utilities and helpers

Core Components
---------------

Engine
^^^^^^

The engine module provides LLM configuration and execution:

- ``AugLLMConfig`` - Enhanced LLM configuration with Pydantic
- ``BaseEngine`` - Base class for all engines
- ``LLMEngine`` - Standard LLM execution engine

Schema
^^^^^^

Type-safe state management:

- ``StateSchema`` - Base state schema class
- ``MessagesState`` - Message-based conversation state
- ``MetaStateSchema`` - Meta-capability state container

Graph
^^^^^

Workflow orchestration:

- ``BaseGraph`` - Foundation for all graphs
- ``DynamicGraph`` - Dynamically modifiable graphs
- ``GraphBuilder`` - Utility for building graphs

API Reference
-------------

Complete API documentation for haive-core:

.. toctree::
   :maxdepth: 3
   :caption: Core API
   :titlesonly:

   api_clean/haive/index

Quick Examples
--------------

Basic Engine Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from haive.core.engine.aug_llm import AugLLMConfig
   
   # Create LLM configuration
   config = AugLLMConfig(
       temperature=0.7,
       max_tokens=1000,
       system_message="You are a helpful assistant"
   )

State Management
^^^^^^^^^^^^^^^^

.. code-block:: python

   from haive.core.schema.prebuilt.messages_state import MessagesState
   from langchain_core.messages import HumanMessage
   
   # Create state
   state = MessagesState()
   
   # Add messages
   state.messages.append(HumanMessage(content="Hello!"))

Graph Building
^^^^^^^^^^^^^^

.. code-block:: python

   from haive.core.graph.base import BaseGraph
   
   # Create a workflow graph
   graph = BaseGraph()
   graph.add_node("start", start_function)
   graph.add_node("process", process_function)
   graph.add_edge("start", "process")

Indices
-------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`