
haive.core.graph.gb.types
=========================

.. py:module:: haive.core.graph.gb.types

.. autoapi-nested-parse::

   Core types for the Haive graph system.

   This module defines fundamental types, protocols, and enums used throughout
   the graph system, providing a strong typing foundation for graph components.

   The system is built on several key concepts:
   1. Protocols: Define structural interfaces (like NamedEntity)
   2. Type aliases: Simplify complex type combinations
   3. Enums: Define constants for node/edge types and states
   4. Policies: Define configuration objects like RetryPolicy

   These types ensure consistency and type safety across the system while
   enabling IDE auto-completion and static type checking.







Classes
-------

* :py:class:`NamedEntity` - Protocol that requires a name property.* :py:class:`EdgeType` - Types of edges in the graph.* :py:class:`EdgeState` - States for edges with waiting conditions.* :py:class:`NodeType` - Types of nodes in the graph.* :py:class:`RetryPolicy` - Policy for retrying node execution on failure.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/graph/gb/types/NamedEntity   /api_clean/haive/core/graph/gb/types/EdgeType   /api_clean/haive/core/graph/gb/types/EdgeState   /api_clean/haive/core/graph/gb/types/NodeType   /api_clean/haive/core/graph/gb/types/RetryPolicy

Package Contents
----------------

