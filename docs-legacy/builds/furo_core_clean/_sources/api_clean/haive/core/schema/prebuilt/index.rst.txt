
:py:mod:`haive.core.schema.prebuilt`
========================

.. py:module:: haive.core.schema.prebuilt

.. autoapi-nested-parse::

   Prebuilt state schemas for common agent patterns.

   This module provides ready-to-use state schemas for various agent architectures:

   - BasicAgentState: Simple agent state with messages and context
   - MessagesState: Conversation management with LangChain integration
   - ToolState: Extended MessagesState with tool management
   - MultiAgentStateSchema: State for multi-agent architectures
   - MessagesStateWithTokenUsage: MessagesState with token tracking

   The messages submodule provides additional functionality:
   - TokenUsage: Token tracking and cost calculation
   - TokenUsageMixin: Mixin for adding token tracking to any schema
   - Enhanced message utilities (if available)




Subpackages
-----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

   haive.core.schema.prebuilt.messages   haive.core.schema.prebuilt.tools
.. toctree::
   :maxdepth: 2
   :hidden:

   /api_clean/haive/core/schema/prebuilt/messages/index   /api_clean/haive/core/schema/prebuilt/tools/index

Submodules
----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

   haive.core.schema.prebuilt.document_state   haive.core.schema.prebuilt.dynamic_activation_state   haive.core.schema.prebuilt.llm_state   haive.core.schema.prebuilt.messages_state   haive.core.schema.prebuilt.meta_state   haive.core.schema.prebuilt.query_state   haive.core.schema.prebuilt.rag_state   haive.core.schema.prebuilt.structured_output_state   haive.core.schema.prebuilt.tool_state   haive.core.schema.prebuilt.tool_state_with_validation   haive.core.schema.prebuilt.validation_aware_tool_state
.. toctree::
   :maxdepth: 1
   :hidden:

   /api_clean/haive/core/schema/prebuilt/document_state/index   /api_clean/haive/core/schema/prebuilt/dynamic_activation_state/index   /api_clean/haive/core/schema/prebuilt/llm_state/index   /api_clean/haive/core/schema/prebuilt/messages_state/index   /api_clean/haive/core/schema/prebuilt/meta_state/index   /api_clean/haive/core/schema/prebuilt/query_state/index   /api_clean/haive/core/schema/prebuilt/rag_state/index   /api_clean/haive/core/schema/prebuilt/structured_output_state/index   /api_clean/haive/core/schema/prebuilt/tool_state/index   /api_clean/haive/core/schema/prebuilt/tool_state_with_validation/index   /api_clean/haive/core/schema/prebuilt/validation_aware_tool_state/index





Package Contents
----------------

.. rubric:: haive.core.schema.prebuilt.__all__

.. autosummary::
   :nosignatures:

   haive.core.schema.prebuilt.AgentState   haive.core.schema.prebuilt.DocumentEngineInputSchema   haive.core.schema.prebuilt.DocumentEngineOutputSchema   haive.core.schema.prebuilt.DocumentState   haive.core.schema.prebuilt.DynamicActivationState   haive.core.schema.prebuilt.EnhancedMultiAgentState   haive.core.schema.prebuilt.LLMState   haive.core.schema.prebuilt.MessagesState   haive.core.schema.prebuilt.MessagesStateWithTokenUsage   haive.core.schema.prebuilt.MetaStateSchema   haive.core.schema.prebuilt.MultiAgentState   haive.core.schema.prebuilt.MultiAgentStateSchema   haive.core.schema.prebuilt.QueryComplexity   haive.core.schema.prebuilt.QueryIntent   haive.core.schema.prebuilt.QueryMetrics   haive.core.schema.prebuilt.QueryProcessingConfig   haive.core.schema.prebuilt.QueryProcessingState   haive.core.schema.prebuilt.QueryResult   haive.core.schema.prebuilt.QueryState   haive.core.schema.prebuilt.QueryType   haive.core.schema.prebuilt.RAGState   haive.core.schema.prebuilt.RetrievalStrategy   haive.core.schema.prebuilt.TokenAwareState   haive.core.schema.prebuilt.TokenToolState   haive.core.schema.prebuilt.TokenUsage   haive.core.schema.prebuilt.TokenUsageMixin   haive.core.schema.prebuilt.ToolState   haive.core.schema.prebuilt.aggregate_token_usage   haive.core.schema.prebuilt.calculate_token_cost   haive.core.schema.prebuilt.extract_token_usage_from_message

.. automodule:: haive.core.schema.prebuilt
   :members:
   :undoc-members:
   :show-inheritance: