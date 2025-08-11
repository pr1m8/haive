
haive.core.graph.node.validation_router_v2
==========================================

.. py:module:: haive.core.graph.node.validation_router_v2

.. autoapi-nested-parse::

   Validation Router V2 - Conditional edge function for routing after V2 validation.

   This router function works with ValidationNodeV2 to make routing decisions
   based on the ToolMessages that were added to state by the validation node.

   Flow:
   1. ValidationNodeV2 processes tool calls and adds ToolMessages to state
   2. This router reads the updated state and makes routing decisions
   3. Routes to appropriate nodes (tool_node, parse_output, agent_node, END)






Functions
---------

   has_tool_error_v2   validation_router_v2
.. autofunction:: has_tool_error_v2
.. autofunction:: validation_router_v2



Package Contents
----------------

