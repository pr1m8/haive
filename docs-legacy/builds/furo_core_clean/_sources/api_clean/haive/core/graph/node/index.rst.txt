
:py:mod:`haive.core.graph.node`
========================

.. py:module:: haive.core.graph.node

.. autoapi-nested-parse::

   Graph Node System - Organized for Better Documentation.

   This module provides a comprehensive node system for building LangGraph workflows,
   organized into logical groups for better discoverability and documentation.

   Engine Nodes
   ============
   Nodes that execute engines with intelligent I/O handling and field mapping.
   These nodes are the primary interface between engines and graph workflows.

   .. autosummary::
      :toctree: generated/

      EngineNodeConfig - Main engine node with field mapping support

   Agent Nodes
   ===========
   Nodes for agent execution and multi-agent coordination patterns.
   These enable complex multi-agent workflows with state management.

   .. autosummary::
      :toctree: generated/

      AgentNodeV3 - Advanced agent node with state projection

   Validation & Routing
   ====================
   Nodes for input/output validation, conditional routing, and workflow control.
   These enable dynamic workflow behavior based on state conditions.

   .. autosummary::
      :toctree: generated/

      ValidationNodeConfig - Basic validation node
      RoutingValidationNode - Validation with routing logic
      UnifiedValidationNode - Advanced validation with multiple features

   Field Mapping & Composition
   ===========================
   Advanced field mapping utilities and schema composition tools.
   These enable complex data transformations between workflow stages.

   .. autosummary::
      :toctree: generated/

      FieldMapping - Field mapping configuration
      NodeSchemaComposer - Advanced schema composition

   Utilities & Factories
   =====================
   Factory functions, registries, and utilities for creating and managing nodes.
   These provide convenient ways to create nodes with common patterns.

   .. autosummary::
      :toctree: generated/

      NodeFactory - Factory for creating node functions
      create_node - Main node creation function
      create_engine_node - Engine node creation function
      NodeRegistry - Node type registry

   Quick Start Examples
   ===================

   Basic engine node with field mapping::

       from haive.core.graph.node import EngineNodeConfig

       node = EngineNodeConfig(
           name="processor",
           engine=my_engine,
           output_fields={"result": "processed_data"}
       )

   Agent node for multi-agent workflows::

       from haive.core.graph.node import AgentNodeV3

       node = AgentNodeV3(
           name="agent_processor",
           agent=my_agent,
           shared_fields=["messages", "context"]
       )

   Factory functions for quick node creation::

       from haive.core.graph.node import create_engine_node

       node = create_engine_node(
           engine=my_engine,
           name="quick_processor",
           output_mapping={"result": "output"}
       )




Subpackages
-----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

   haive.core.graph.node.composer
.. toctree::
   :maxdepth: 2
   :hidden:

   /api_clean/haive/core/graph/node/composer/index

Submodules
----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

   haive.core.graph.node.base_config   haive.core.graph.node.base_node_config   haive.core.graph.node.callable_node   haive.core.graph.node.config   haive.core.graph.node.decorators   haive.core.graph.node.engine_node   haive.core.graph.node.engine_node_generic   haive.core.graph.node.factory   haive.core.graph.node.handlers   haive.core.graph.node.message_transformation   haive.core.graph.node.message_transformation_v2   haive.core.graph.node.output_parsing   haive.core.graph.node.output_parsing_v2   haive.core.graph.node.parser_node_config   haive.core.graph.node.parser_node_config_v2   haive.core.graph.node.placeholder_node   haive.core.graph.node.processors   haive.core.graph.node.protocols   haive.core.graph.node.registry   haive.core.graph.node.routing_validation_node   haive.core.graph.node.state_updating_validation_node   haive.core.graph.node.stateful_node_config   haive.core.graph.node.stateful_validation_node   haive.core.graph.node.test   haive.core.graph.node.tool_node_config   haive.core.graph.node.tool_node_config_v2   haive.core.graph.node.types   haive.core.graph.node.unified_validation_node   haive.core.graph.node.utils   haive.core.graph.node.validation_node_config   haive.core.graph.node.validation_node_config_v2   haive.core.graph.node.validation_node_v2   haive.core.graph.node.validation_node_with_routing   haive.core.graph.node.validation_router_v2
.. toctree::
   :maxdepth: 1
   :hidden:

   /api_clean/haive/core/graph/node/base_config/index   /api_clean/haive/core/graph/node/base_node_config/index   /api_clean/haive/core/graph/node/callable_node/index   /api_clean/haive/core/graph/node/config/index   /api_clean/haive/core/graph/node/decorators/index   /api_clean/haive/core/graph/node/engine_node/index   /api_clean/haive/core/graph/node/engine_node_generic/index   /api_clean/haive/core/graph/node/factory/index   /api_clean/haive/core/graph/node/handlers/index   /api_clean/haive/core/graph/node/message_transformation/index   /api_clean/haive/core/graph/node/message_transformation_v2/index   /api_clean/haive/core/graph/node/output_parsing/index   /api_clean/haive/core/graph/node/output_parsing_v2/index   /api_clean/haive/core/graph/node/parser_node_config/index   /api_clean/haive/core/graph/node/parser_node_config_v2/index   /api_clean/haive/core/graph/node/placeholder_node/index   /api_clean/haive/core/graph/node/processors/index   /api_clean/haive/core/graph/node/protocols/index   /api_clean/haive/core/graph/node/registry/index   /api_clean/haive/core/graph/node/routing_validation_node/index   /api_clean/haive/core/graph/node/state_updating_validation_node/index   /api_clean/haive/core/graph/node/stateful_node_config/index   /api_clean/haive/core/graph/node/stateful_validation_node/index   /api_clean/haive/core/graph/node/test/index   /api_clean/haive/core/graph/node/tool_node_config/index   /api_clean/haive/core/graph/node/tool_node_config_v2/index   /api_clean/haive/core/graph/node/types/index   /api_clean/haive/core/graph/node/unified_validation_node/index   /api_clean/haive/core/graph/node/utils/index   /api_clean/haive/core/graph/node/validation_node_config/index   /api_clean/haive/core/graph/node/validation_node_config_v2/index   /api_clean/haive/core/graph/node/validation_node_v2/index   /api_clean/haive/core/graph/node/validation_node_with_routing/index   /api_clean/haive/core/graph/node/validation_router_v2/index



Package Functions
-----------------

.. autosummary::
   :nosignatures:
   :template: autosummary/function.rst

   haive.core.graph.node.create_node   haive.core.graph.node.create_engine_node   haive.core.graph.node.create_validation_node   haive.core.graph.node.create_tool_node   haive.core.graph.node.create_branch_node   haive.core.graph.node.get_registry   haive.core.graph.node.register_custom_node_type
.. autofunction:: haive.core.graph.node.create_node
.. autofunction:: haive.core.graph.node.create_engine_node
.. autofunction:: haive.core.graph.node.create_validation_node
.. autofunction:: haive.core.graph.node.create_tool_node
.. autofunction:: haive.core.graph.node.create_branch_node
.. autofunction:: haive.core.graph.node.get_registry
.. autofunction:: haive.core.graph.node.register_custom_node_type



Package Contents
----------------

.. rubric:: haive.core.graph.node.__all__

.. autosummary::
   :nosignatures:

   haive.core.graph.node.END   haive.core.graph.node.AgentNodeV3   haive.core.graph.node.AsyncNodeFunction   haive.core.graph.node.Command   haive.core.graph.node.CommandGoto   haive.core.graph.node.ConfigType   haive.core.graph.node.EngineNodeConfig   haive.core.graph.node.NodeConfig   haive.core.graph.node.NodeFactory   haive.core.graph.node.NodeFunction   haive.core.graph.node.NodeRegistry   haive.core.graph.node.NodeType   haive.core.graph.node.RetryPolicy   haive.core.graph.node.Send   haive.core.graph.node.StateInput   haive.core.graph.node.StateOutput   haive.core.graph.node.ToolNode   haive.core.graph.node.ValidationNode   haive.core.graph.node.branch_node   haive.core.graph.node.create_branch_node   haive.core.graph.node.create_engine_node   haive.core.graph.node.create_node   haive.core.graph.node.create_send_node   haive.core.graph.node.create_tool_node   haive.core.graph.node.create_validation_node   haive.core.graph.node.extract_io_mapping_from_schema   haive.core.graph.node.factory   haive.core.graph.node.get_registry   haive.core.graph.node.register_custom_node_type   haive.core.graph.node.register_node   haive.core.graph.node.send_node   haive.core.graph.node.tool_node   haive.core.graph.node.validation_node

.. automodule:: haive.core.graph.node
   :members:
   :undoc-members:
   :show-inheritance: