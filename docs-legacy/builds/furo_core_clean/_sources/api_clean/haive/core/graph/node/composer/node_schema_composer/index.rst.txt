
haive.core.graph.node.composer.node_schema_composer
===================================================

.. py:module:: haive.core.graph.node.composer.node_schema_composer

.. autoapi-nested-parse::

   NodeSchemaComposer - Main composer for flexible node I/O configuration.

   This module provides the main NodeSchemaComposer class that enables arbitrary
   field mappings like "result → retrieved_documents" or "documents → potato"
   with pluggable extract/update functions.

   This solves the critical gap where you cannot easily modify node input/output
   schemas or create composed nodes with custom field mappings.






Functions
---------

   change_output_key   change_input_key   remap_fields
.. autofunction:: change_output_key
.. autofunction:: change_input_key
.. autofunction:: remap_fields

Classes
-------

* :py:class:`NodeSchemaComposer` - Main composer for flexible node I/O configuration.* :py:class:`ComposedNode` - A node composed with custom I/O mappings.* :py:class:`ComposedCallableNode` - A callable function composed as a node with custom I/O mappings.* :py:class:`SchemaAdapter` - Adapter between two Pydantic schemas with field mappings.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/graph/node/composer/node_schema_composer/NodeSchemaComposer   /api_clean/haive/core/graph/node/composer/node_schema_composer/ComposedNode   /api_clean/haive/core/graph/node/composer/node_schema_composer/ComposedCallableNode   /api_clean/haive/core/graph/node/composer/node_schema_composer/SchemaAdapter

Package Contents
----------------

