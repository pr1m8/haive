
haive.core.graph.node.validation_node_v2
========================================

.. py:module:: haive.core.graph.node.validation_node_v2

.. autoapi-nested-parse::

   Validation Node V2 - Regular node that updates state with ToolMessages.

   This is a proper node (not conditional edge) that can update state by adding
   ToolMessages for Pydantic model validation and errors. It works with a separate
   validation router function for routing decisions.

   Flow:
   1. V2 Validation Node: Processes tool calls, adds ToolMessages to state
   2. V2 Validation Router: Reads updated state, makes routing decisions







Classes
-------

* :py:class:`ValidationNodeV2` - V2 Validation node that updates state with ToolMessages using schema-aware I/O.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/graph/node/validation_node_v2/ValidationNodeV2

Package Contents
----------------

