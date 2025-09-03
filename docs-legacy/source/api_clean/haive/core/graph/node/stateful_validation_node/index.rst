
haive.core.graph.node.stateful_validation_node
==============================================

.. py:module:: haive.core.graph.node.stateful_validation_node

.. autoapi-nested-parse::

   Stateful Validation Node - Tracks tool call validation results in state.

   This node processes tool calls and stores validation results in state using computed fields.
   It separates validation logic from routing logic, enabling intelligent routing decisions
   based on validation history and patterns.

   Key features:
   - Stores validation results in state with computed fields
   - Tracks valid vs invalid tool calls for routing decisions
   - Supports dynamic routing based on validation patterns
   - Maintains validation history for analysis
   - Integrates with ToolState for seamless tool tracking







Classes
-------

* :py:class:`ToolCallValidationResult` - Result of a tool call validation.* :py:class:`StatefulValidationNode` - Stateful validation node that tracks tool call validation results in state.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/graph/node/stateful_validation_node/ToolCallValidationResult   /api_clean/haive/core/graph/node/stateful_validation_node/StatefulValidationNode

Package Contents
----------------

