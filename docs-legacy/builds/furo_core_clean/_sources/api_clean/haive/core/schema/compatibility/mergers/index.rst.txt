
haive.core.schema.compatibility.mergers
=======================================

.. py:module:: haive.core.schema.compatibility.mergers

.. autoapi-nested-parse::

   Schema merging strategies for combining multiple schemas.






Functions
---------

   merge_schemas   create_union_schema   create_intersection_schema
.. autofunction:: merge_schemas
.. autofunction:: create_union_schema
.. autofunction:: create_intersection_schema

Classes
-------

* :py:class:`ConflictResolution` - How to resolve field conflicts during merge.* :py:class:`MergeContext` - Context for merge operations.* :py:class:`MergeStrategy` - Abstract base for merge strategies.* :py:class:`UnionMergeStrategy` - Include all fields from all schemas.* :py:class:`IntersectionMergeStrategy` - Include only fields present in all schemas.* :py:class:`SchemaMerger` - Main schema merging engine.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/schema/compatibility/mergers/ConflictResolution   /api_clean/haive/core/schema/compatibility/mergers/MergeContext   /api_clean/haive/core/schema/compatibility/mergers/MergeStrategy   /api_clean/haive/core/schema/compatibility/mergers/UnionMergeStrategy   /api_clean/haive/core/schema/compatibility/mergers/IntersectionMergeStrategy   /api_clean/haive/core/schema/compatibility/mergers/SchemaMerger

Package Contents
----------------

