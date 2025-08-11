
haive.core.schema.base_state_schemas
====================================

.. py:module:: haive.core.schema.base_state_schemas

.. autoapi-nested-parse::

   Base state schemas with clear inheritance hierarchy.

   This module provides a cleaner inheritance structure for state schemas,
   separating concerns between different types of agents and workflows.






Functions
---------

   create_agent_state   create_multi_agent_state
.. autofunction:: create_agent_state
.. autofunction:: create_multi_agent_state

Classes
-------

* :py:class:`MinimalState` - Absolute minimal state - just data, no engines or agents.* :py:class:`MessagingState` - State that includes message handling.* :py:class:`EngineState` - State that can hold engines (serializable components).* :py:class:`ToolState` - State that includes tool management.* :py:class:`AgentState` - State for a single agent with a primary engine (usually LLM).* :py:class:`WorkflowState` - State for workflow agents that can modify their own execution graph.* :py:class:`MetaAgentState` - State for meta-agents that can spawn and manage other agents.* :py:class:`MultiAgentState` - State for multi-agent systems with proper isolation.* :py:class:`HierarchicalAgentState` - State for hierarchical agent systems (parent-child relationships).* :py:class:`ToolExecutorState` - Specialized state for pure tool execution workflows.* :py:class:`DataProcessingState` - State for data processing workflows.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/schema/base_state_schemas/MinimalState   /api_clean/haive/core/schema/base_state_schemas/MessagingState   /api_clean/haive/core/schema/base_state_schemas/EngineState   /api_clean/haive/core/schema/base_state_schemas/ToolState   /api_clean/haive/core/schema/base_state_schemas/AgentState   /api_clean/haive/core/schema/base_state_schemas/WorkflowState   /api_clean/haive/core/schema/base_state_schemas/MetaAgentState   /api_clean/haive/core/schema/base_state_schemas/MultiAgentState   /api_clean/haive/core/schema/base_state_schemas/HierarchicalAgentState   /api_clean/haive/core/schema/base_state_schemas/ToolExecutorState   /api_clean/haive/core/schema/base_state_schemas/DataProcessingState

Package Contents
----------------

