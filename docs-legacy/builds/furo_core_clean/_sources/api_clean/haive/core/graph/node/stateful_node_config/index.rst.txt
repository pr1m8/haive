
haive.core.graph.node.stateful_node_config
==========================================

.. py:module:: haive.core.graph.node.stateful_node_config

.. autoapi-nested-parse::

   Stateful Node Configuration - Enhanced Dynamic Architecture.

   This module provides a truly dynamic node architecture where:
   - All routing destinations are discovered from state at runtime
   - Field configurations are dynamically resolved from state
   - Engine references, tool references, and node references are all stateful
   - Nodes adapt their behavior based on what's available in state

   Key Features:
   - Runtime discovery of engines, tools, and routing destinations
   - Dynamic field mapping configuration
   - Stateful routing with fallback mechanisms
   - Type-safe parameter extraction with automatic field detection







Classes
-------

* :py:class:`StatefulNodeConfig` - Base class for stateful nodes that discover resources from state at runtime.* :py:class:`StatefulValidationNodeConfig` - Stateful validation node that discovers everything from state.* :py:class:`StatefulParserNodeConfig` - Stateful parser node that discovers routing from state.* :py:class:`StatefulToolNodeConfig` - Stateful tool node that discovers tools from state.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/graph/node/stateful_node_config/StatefulNodeConfig   /api_clean/haive/core/graph/node/stateful_node_config/StatefulValidationNodeConfig   /api_clean/haive/core/graph/node/stateful_node_config/StatefulParserNodeConfig   /api_clean/haive/core/graph/node/stateful_node_config/StatefulToolNodeConfig

Package Contents
----------------

