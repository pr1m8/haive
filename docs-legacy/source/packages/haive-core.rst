haive-core
==========

Foundation package for the Haive AI Agent Framework.

Overview
--------

The ``haive-core`` package provides the essential building blocks for creating AI agents:

- **Engine System** - LLM integration and configuration
- **State Management** - Structured state schemas and persistence  
- **Graph Framework** - Workflow orchestration with LangGraph
- **Schema System** - Type-safe data models with Pydantic
- **Persistence** - State saving and loading mechanisms

Installation
------------

.. code-block:: bash

   pip install haive-core

Or as part of the full framework:

.. code-block:: bash

   pip install haive

Quick Start
-----------

.. code-block:: python

   from haive.core.engine.aug_llm import AugLLMConfig
   from haive.core.schema.prebuilt.messages_state import MessagesState
   
   # Configure LLM engine
   config = AugLLMConfig(
       temperature=0.7,
       max_tokens=1000,
       system_message="You are a helpful assistant"
   )
   
   # Create state container
   state = MessagesState()

Core Components
---------------

Engine System
^^^^^^^^^^^^^

.. grid:: 2
   :gutter: 2

   .. grid-item-card:: AugLLMConfig
      :link: ../api/core/engine/aug_llm/index
      :link-type: doc

      Main LLM configuration class
      
      - Provider selection
      - Model parameters
      - Structured output
      - Tool integration

   .. grid-item-card:: LLM Providers
      :link: ../api/core/llm_providers/index
      :link-type: doc

      Supported LLM providers
      
      - OpenAI/Azure OpenAI
      - Anthropic Claude
      - Google Gemini
      - Local models

State Management
^^^^^^^^^^^^^^^^

.. grid:: 2
   :gutter: 2

   .. grid-item-card:: StateSchema
      :link: ../api/core/schema/state_schema/index
      :link-type: doc

      Base state management
      
      - Type-safe schemas
      - Validation
      - Serialization
      - State updates

   .. grid-item-card:: MessagesState
      :link: ../api/core/schema/prebuilt/messages_state/index
      :link-type: doc

      Conversation state
      
      - Message history
      - Context management
      - Token counting
      - Persistence

Graph System
^^^^^^^^^^^^

.. grid:: 2
   :gutter: 2

   .. grid-item-card:: BaseGraph
      :link: ../api/core/graph/base_graph/index
      :link-type: doc

      Graph foundation
      
      - Node management
      - Edge connections
      - State flow
      - Execution control

   .. grid-item-card:: StateGraph
      :link: ../api/core/graph/state_graph/index
      :link-type: doc

      Stateful workflows
      
      - LangGraph integration
      - Conditional edges
      - Parallel execution
      - Checkpointing

Key Classes
-----------

.. autosummary::
   :toctree: ../api
   :recursive:
   :nosignatures:
   :template: autosummary/class.rst

   haive.core.engine.aug_llm.AugLLMConfig
   haive.core.schema.prebuilt.messages_state.MessagesState
   haive.core.schema.state_schema.StateSchema
   haive.core.graph.base_graph.BaseGraph
   haive.core.schema.prebuilt.meta_state.MetaStateSchema
   haive.core.llm_providers.factory.create_llm
   haive.core.persistence.base.BasePersistence

Engine Components
-----------------

.. autosummary::
   :toctree: ../api
   :recursive:
   :nosignatures:
   :template: autosummary/class.rst

   haive.core.engine.aug_llm.AugLLMConfig
   haive.core.engine.base_engine_config.BaseEngineConfig
   haive.core.engine.invoke_engine.InvokableEngine
   haive.core.engine.document.universal_loader.UniversalLoader

LLM Providers
-------------

.. autosummary::
   :toctree: ../api
   :recursive:
   :nosignatures:
   :template: autosummary/class.rst

   haive.core.llm_providers.openai_provider.OpenAIProvider
   haive.core.llm_providers.anthropic_provider.AnthropicProvider
   haive.core.llm_providers.google_provider.GoogleProvider
   haive.core.llm_providers.azure_provider.AzureOpenAIProvider

State Management
----------------

.. autosummary::
   :toctree: ../api
   :recursive:
   :nosignatures:
   :template: autosummary/class.rst

   haive.core.schema.state_schema.StateSchema
   haive.core.schema.prebuilt.messages_state.MessagesState
   haive.core.schema.prebuilt.meta_state.MetaStateSchema
   haive.core.schema.prebuilt.validation_routing.ValidationNodeConfigV2

Graph Components
----------------

.. autosummary::
   :toctree: ../api
   :recursive:
   :nosignatures:
   :template: autosummary/class.rst

   haive.core.graph.base_graph.BaseGraph
   haive.core.graph.state_graph.StateGraph
   haive.core.graph.node.base_node.BaseNode
   haive.core.graph.node.engine_node.EngineNode

Complete API Reference
----------------------

For the complete API documentation with all classes, functions, and modules:

.. toctree::
   :maxdepth: 3

   ../api/core/index

Examples
--------

Basic Engine Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from haive.core.engine.aug_llm import AugLLMConfig
   
   # Default configuration
   config = AugLLMConfig()
   
   # Custom configuration
   config = AugLLMConfig(
       model="gpt-4",
       temperature=0.3,
       max_tokens=2000,
       system_message="You are an expert Python developer"
   )

State Management
^^^^^^^^^^^^^^^^

.. code-block:: python

   from haive.core.schema.prebuilt.messages_state import MessagesState
   from langchain_core.messages import HumanMessage, AIMessage
   
   # Create state
   state = MessagesState()
   
   # Add messages
   state.messages.append(HumanMessage(content="Hello!"))
   state.messages.append(AIMessage(content="Hi there!"))
   
   # Access messages
   for msg in state.messages:
       print(f"{msg.__class__.__name__}: {msg.content}")

Custom State Schema
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from haive.core.schema import StateSchema
   from pydantic import Field
   from typing import List, Dict
   
   class MyCustomState(StateSchema):
       """Custom state for my agent."""
       
       task: str = Field(description="Current task")
       context: Dict[str, Any] = Field(default_factory=dict)
       history: List[str] = Field(default_factory=list)
       
       def add_to_history(self, item: str):
           """Add item to history."""
           self.history.append(item)

Best Practices
--------------

1. **Always use AugLLMConfig** for LLM configuration
2. **Extend StateSchema** for custom state management
3. **Use type hints** for all state fields
4. **Leverage Pydantic validation** for data integrity
5. **Follow the import pattern**: ``from haive.core.module import Class``

Related Documentation
---------------------

- :doc:`../guide/state_management/index` - State management guide
- :doc:`../api/core/index` - Complete core API reference
- :doc:`haive-agents` - Agent implementations using core