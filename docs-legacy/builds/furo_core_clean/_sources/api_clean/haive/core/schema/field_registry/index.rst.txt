
haive.core.schema.field_registry
================================

.. py:module:: haive.core.schema.field_registry

.. autoapi-nested-parse::

   Field Registry for standardized field definitions across Haive.

   This module provides a centralized registry of commonly used field definitions
   that can be referenced by nodes, engines, and schema composers. This ensures
   consistency and allows for selective state schema composition.

   Key benefits:
   - Standardized field definitions across the framework
   - Selective inclusion in state schemas (only what's needed)
   - Type safety with proper generics
   - Token counting integration for messages
   - Backwards compatibility






Functions
---------

   get_standard_field
.. autofunction:: get_standard_field

Classes
-------

* :py:class:`StandardFields` - Registry of standard field definitions used across Haive.* :py:class:`FieldRegistry` - Dynamic field registry for custom field definitions.* :py:class:`CommonFieldSets` - Pre-defined sets of fields for common use cases.* :py:class:`PrebuiltStates` - Registry of prebuilt state schemas for common use cases.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/schema/field_registry/StandardFields   /api_clean/haive/core/schema/field_registry/FieldRegistry   /api_clean/haive/core/schema/field_registry/CommonFieldSets   /api_clean/haive/core/schema/field_registry/PrebuiltStates

Package Contents
----------------

