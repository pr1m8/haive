
haive.core.graph.node.engine_node_generic
=========================================

.. py:module:: haive.core.graph.node.engine_node_generic

.. autoapi-nested-parse::

   Generic Engine Node Configuration with Type Safety and Field Registry Integration.

   This module provides generic engine node configurations that can distinguish between
   different engine types (LLM, RAG, etc.) while maintaining backwards compatibility.
   It integrates with the field registry for standardized field definitions.






Functions
---------

   create_engine_node
.. autofunction:: create_engine_node

Classes
-------

* :py:class:`GenericEngineNodeConfig` - Generic engine node with type-safe input/output schemas.* :py:class:`LLMNodeConfig` - Specialized node configuration for LLM engines.* :py:class:`RAGNodeConfig` - Specialized node configuration for RAG engines.* :py:class:`NodeFactory` - Factory for creating specialized node configurations.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/graph/node/engine_node_generic/GenericEngineNodeConfig   /api_clean/haive/core/graph/node/engine_node_generic/LLMNodeConfig   /api_clean/haive/core/graph/node/engine_node_generic/RAGNodeConfig   /api_clean/haive/core/graph/node/engine_node_generic/NodeFactory

Package Contents
----------------

