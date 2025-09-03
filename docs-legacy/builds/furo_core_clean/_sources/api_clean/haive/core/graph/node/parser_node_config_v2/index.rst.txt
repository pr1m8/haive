
haive.core.graph.node.parser_node_config_v2
===========================================

.. py:module:: haive.core.graph.node.parser_node_config_v2

.. autoapi-nested-parse::

   Parser Node Configuration V2 - With ToolMessage safety net.

   This version extends the original parser node with an optional safety net feature
   that can create ToolMessages if they don't already exist in state.

   This addresses cases where:
   1. Pydantic model validation succeeded but no ToolMessage was created
   2. Tool calls exist but corresponding ToolMessages are missing
   3. Need to ensure conversation continuity with proper ToolMessages

   Config options:
   - add_tool_message_safety_net: Whether to create missing ToolMessages
   - safety_net_mode: How to handle missing ToolMessages ("create", "warn", "ignore")







Classes
-------

* :py:class:`ParserNodeConfigV2` - V2 Parser node with ToolMessage safety net and schema-aware I/O.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/graph/node/parser_node_config_v2/ParserNodeConfigV2

Package Contents
----------------

