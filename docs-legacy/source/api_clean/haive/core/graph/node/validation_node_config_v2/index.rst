
haive.core.graph.node.validation_node_config_v2
===============================================

.. py:module:: haive.core.graph.node.validation_node_config_v2

.. autoapi-nested-parse::

   Validation Node Configuration V2 - Improved version that can update state.

   This version addresses the key issues with the original validation node:
   1. Can add ToolMessages to state (not just route)
   2. Handles dynamic tool routes properly
   3. Uses Command with Send objects for proper routing
   4. Supports both Pydantic models and regular tools

   Key improvements:
   - Proper node implementation (not conditional edge)
   - ToolMessage creation for Pydantic model validation
   - Error handling with appropriate ToolMessages
   - Dynamic routing based on actual tool calls







Classes
-------

* :py:class:`ValidationNodeConfigV2` - V2 Validation node that can update state and add ToolMessages.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/graph/node/validation_node_config_v2/ValidationNodeConfigV2

Package Contents
----------------

