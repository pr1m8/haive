
:py:mod:`haive.core.schema`
========================

.. py:module:: haive.core.schema

.. autoapi-nested-parse::

   Haive Schema System - Dynamic State Management for AI Agents.

   This package provides a powerful foundation for dynamic state management in AI agents
   and workflows. It extends Pydantic's model system with features specifically designed
   for graph-based AI workflows, including field sharing between graphs, reducer functions
   for state updates, and engine I/O tracking.

   The schema system enables fully dynamic and serializable state schemas that can be
   composed, modified, and extended at runtime, making it ideal for complex agent
   architectures and nested workflows.

   Architecture:
       The schema system is built around a core StateSchema that extends Pydantic BaseModel
       with additional capabilities for AI agent workflows:

       - Field sharing between parent and child graphs
       - Reducer functions for intelligent state merging
       - Engine I/O tracking for workflow coordination
       - Structured output model integration
       - Rich visualization and debugging tools

   Core Components:
       StateSchema: Base class that extends Pydantic models with sharing, reducers,
           and I/O tracking. Serves as the foundation for all agent state management.
       SchemaComposer: Utility for building schemas from components dynamically.
           Supports field extraction from engines, models, and dictionaries.
       StateSchemaManager: Tool for manipulating schemas at runtime.
           Provides methods for schema modification and transformation.
       MultiAgentStateSchema: Enhanced schema for multi-agent architectures.
           Handles complex state coordination across multiple agents.
       AgentSchemaComposer: Schema composer specialized for agent architectures.
           Includes build modes and agent-specific optimizations.
       FieldDefinition: Representation of field type, default, and metadata.
           Provides comprehensive field information for schema building.
       FieldExtractor: Utility for extracting fields from various sources.
           Supports engines, models, tools, and custom components.
       Field Utilities: Common functions for field manipulation.
           Includes type inference, reducer resolution, and field creation.

   Prebuilt Schemas:
       # BasicAgentState: Simple state with common agent fields (Module doesn't exist)
       MessagesState: State optimized for conversation handling
       ToolState: State with built-in tool management
       TokenUsage: Token tracking and cost calculation utilities

   Usage Patterns:
       Basic Usage::

           from haive.core.schema import StateSchema, Field
           from typing import List, Dict, Any

           class MyAgentState(StateSchema):
               messages: List[str] = Field(default_factory=list)
               context: Dict[str, Any] = Field(default_factory=dict)

               __shared_fields__ = ["messages"]
               __reducer_fields__ = {
                   "messages": lambda a, b: a + b
               }

       Dynamic Schema Building::

           from haive.core.schema import SchemaComposer

           composer = SchemaComposer(name="DynamicState")
           composer.add_field("query", str, default="")
           composer.add_field("results", List[str], default_factory=list)

           DynamicState = composer.build()
           state = DynamicState()

       Multi-Agent Coordination::

           from haive.core.schema import MultiAgentStateSchema

           class CoordinatedState(MultiAgentStateSchema):
               shared_memory: Dict[str, Any] = Field(default_factory=dict)
               agent_states: Dict[str, Dict] = Field(default_factory=dict)

               __shared_fields__ = ["shared_memory"]

   .. admonition:: Examples

      For detailed usage examples, see the documentation and examples directory.
      Key example files:
      - examples/basic_schema_usage.py
      - examples/dynamic_schema_building.py
      - examples/multi_agent_coordination.py
      - examples/engine_integration.py

   Version: 2.0.0
   Author: Haive Team
   License: MIT




Subpackages
-----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

   haive.core.schema.compatibility   haive.core.schema.composer   haive.core.schema.mixins   haive.core.schema.prebuilt   haive.core.schema.state
.. toctree::
   :maxdepth: 2
   :hidden:

   /api_clean/haive/core/schema/compatibility/index   /api_clean/haive/core/schema/composer/index   /api_clean/haive/core/schema/mixins/index   /api_clean/haive/core/schema/prebuilt/index   /api_clean/haive/core/schema/state/index

Submodules
----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

   haive.core.schema.base_state_schemas   haive.core.schema.engine_io_mixin   haive.core.schema.example   haive.core.schema.field_definition   haive.core.schema.field_extractor   haive.core.schema.field_registry   haive.core.schema.field_utils   haive.core.schema.preserve_messages_reducer   haive.core.schema.schema_composer   haive.core.schema.schema_manager   haive.core.schema.state_schema   haive.core.schema.typed_state_schema   haive.core.schema.ui   haive.core.schema.utils
.. toctree::
   :maxdepth: 1
   :hidden:

   /api_clean/haive/core/schema/base_state_schemas/index   /api_clean/haive/core/schema/engine_io_mixin/index   /api_clean/haive/core/schema/example/index   /api_clean/haive/core/schema/field_definition/index   /api_clean/haive/core/schema/field_extractor/index   /api_clean/haive/core/schema/field_registry/index   /api_clean/haive/core/schema/field_utils/index   /api_clean/haive/core/schema/preserve_messages_reducer/index   /api_clean/haive/core/schema/schema_composer/index   /api_clean/haive/core/schema/schema_manager/index   /api_clean/haive/core/schema/state_schema/index   /api_clean/haive/core/schema/typed_state_schema/index   /api_clean/haive/core/schema/ui/index   /api_clean/haive/core/schema/utils/index



Package Functions
-----------------

.. autosummary::
   :nosignatures:
   :template: autosummary/function.rst

   haive.core.schema.create_simple_state   haive.core.schema.create_agent_state   haive.core.schema.validate_schema   haive.core.schema.get_schema_info
.. autofunction:: haive.core.schema.create_simple_state
.. autofunction:: haive.core.schema.create_agent_state
.. autofunction:: haive.core.schema.validate_schema
.. autofunction:: haive.core.schema.get_schema_info



Package Contents
----------------

.. rubric:: haive.core.schema.__all__

.. autosummary::
   :nosignatures:

   haive.core.schema.AgentSchemaComposer   haive.core.schema.BuildMode   haive.core.schema.FieldDefinition   haive.core.schema.FieldExtractor   haive.core.schema.FieldType   haive.core.schema.MessagesState   haive.core.schema.MessagesStateWithTokenUsage   haive.core.schema.MultiAgentSchemaComposer   haive.core.schema.MultiAgentStateSchema   haive.core.schema.PrebuiltMultiAgentStateSchema   haive.core.schema.ReducerType   haive.core.schema.SchemaComposer   haive.core.schema.SchemaType   haive.core.schema.SchemaUI   haive.core.schema.StateSchema   haive.core.schema.StateSchemaManager   haive.core.schema.TokenUsage   haive.core.schema.TokenUsageMixin   haive.core.schema.ToolState   haive.core.schema.ValidatorType   haive.core.schema.__author__   haive.core.schema.__license__   haive.core.schema.__version__   haive.core.schema.aggregate_token_usage   haive.core.schema.calculate_token_cost   haive.core.schema.create_agent_state   haive.core.schema.create_annotated_field   haive.core.schema.create_field   haive.core.schema.create_simple_state   haive.core.schema.extract_token_usage_from_message   haive.core.schema.extract_type_metadata   haive.core.schema.get_common_reducers   haive.core.schema.get_schema_info   haive.core.schema.infer_field_type   haive.core.schema.preserve_messages_reducer   haive.core.schema.resolve_reducer   haive.core.schema.validate_schema

.. automodule:: haive.core.schema
   :members:
   :undoc-members:
   :show-inheritance: