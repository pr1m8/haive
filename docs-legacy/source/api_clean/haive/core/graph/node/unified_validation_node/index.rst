
haive.core.graph.node.unified_validation_node
=============================================

.. py:module:: haive.core.graph.node.unified_validation_node

.. autoapi-nested-parse::

   Unified Validation Node V2 - Proper Pydantic implementation.

   This replaces the artificial separation between ValidationNodeV2 and validation_router_v2
   with a single node that validates and routes in one unified operation.

   Fixed to follow proper Pydantic patterns without custom __init__ methods.






Functions
---------

   create_unified_validation_node
.. autofunction:: create_unified_validation_node

Classes
-------

* :py:class:`UnifiedValidationNodeConfig` - Unified validation node that combines tool validation and routing.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/graph/node/unified_validation_node/UnifiedValidationNodeConfig

Package Contents
----------------

