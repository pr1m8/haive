
haive.core.schema.compatibility.protocols
=========================================

.. py:module:: haive.core.schema.compatibility.protocols

.. autoapi-nested-parse::

   from typing import Any
   Protocol definitions for extending the schema compatibility system.






Functions
---------

   converter_plugin   validator_plugin   compatibility_plugin
.. autofunction:: converter_plugin
.. autofunction:: validator_plugin
.. autofunction:: compatibility_plugin

Classes
-------

* :py:class:`SchemaConvertible` - Protocol for objects that can be converted to/from schemas.* :py:class:`FieldTransformer` - Protocol for field transformation functions.* :py:class:`SchemaValidator` - Protocol for schema validators.* :py:class:`ConversionStrategy` - Protocol for conversion strategies.* :py:class:`FieldResolver` - Protocol for resolving field mappings.* :py:class:`TypeInspector` - Protocol for custom type inspection.* :py:class:`SchemaEvolution` - Protocol for schema evolution/migration.* :py:class:`CompatibilityPlugin` - Protocol for compatibility checker plugins.* :py:class:`AsyncConverter` - Protocol for async converters.* :py:class:`SchemaRegistry` - Protocol for schema registries.* :py:class:`PluginManager` - Manages plugins for the compatibility system.* :py:class:`ExampleFieldResolver` - Example field resolver using similarity matching.* :py:class:`ExampleTypeInspector` - Example type inspector for custom types.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/schema/compatibility/protocols/SchemaConvertible   /api_clean/haive/core/schema/compatibility/protocols/FieldTransformer   /api_clean/haive/core/schema/compatibility/protocols/SchemaValidator   /api_clean/haive/core/schema/compatibility/protocols/ConversionStrategy   /api_clean/haive/core/schema/compatibility/protocols/FieldResolver   /api_clean/haive/core/schema/compatibility/protocols/TypeInspector   /api_clean/haive/core/schema/compatibility/protocols/SchemaEvolution   /api_clean/haive/core/schema/compatibility/protocols/CompatibilityPlugin   /api_clean/haive/core/schema/compatibility/protocols/AsyncConverter   /api_clean/haive/core/schema/compatibility/protocols/SchemaRegistry   /api_clean/haive/core/schema/compatibility/protocols/PluginManager   /api_clean/haive/core/schema/compatibility/protocols/ExampleFieldResolver   /api_clean/haive/core/schema/compatibility/protocols/ExampleTypeInspector

Package Contents
----------------

