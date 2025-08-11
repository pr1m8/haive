
:py:mod:`haive.core.common`
========================

.. py:module:: haive.core.common

.. autoapi-nested-parse::

   Haive Core Common Module.

   This module provides common utilities, models, types, and mixins used throughout the Haive
   framework. It contains foundational components that enable consistent behavior across
   different parts of the system.

   Key Components:
       - Mixins: Reusable component behaviors through mixin classes
       - Models: Common data structures and models
       - Types: Type definitions and protocol interfaces
       - Structures: Collection structures with enhanced functionality
       - Logging: Centralized logging configuration

   Typical usage example:
       ```python
       from haive.core.common.mixins import IdentifierMixin, TimestampMixin
       from haive.core.common.types import JsonType, DictStrAny
       from haive.core.common.logging_config import configure_logging

       # Use mixins in your class
       class MyComponent(IdentifierMixin, TimestampMixin):
           def __init__(self, name: str):
               super().__init__()
               self.name = name

       # Configure logging
       configure_logging(level="INFO")
       ```




Subpackages
-----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

   haive.core.common.mixins   haive.core.common.models   haive.core.common.types
.. toctree::
   :maxdepth: 2
   :hidden:

   /api_clean/haive/core/common/mixins/index   /api_clean/haive/core/common/models/index   /api_clean/haive/core/common/types/index

Submodules
----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

   haive.core.common.logging_config
.. toctree::
   :maxdepth: 1
   :hidden:

   /api_clean/haive/core/common/logging_config/index





Package Contents
----------------

.. rubric:: haive.core.common.__all__

.. autosummary::
   :nosignatures:

   haive.core.common.DictStrAny   haive.core.common.DynamicChoiceModel   haive.core.common.IDMixin   haive.core.common.JsonType   haive.core.common.MetadataMixin   haive.core.common.NamedList   haive.core.common.RichLoggerMixin   haive.core.common.SerializationMixin   haive.core.common.StrOrPath   haive.core.common.TimestampMixin   haive.core.common.VersionMixin

.. automodule:: haive.core.common
   :members:
   :undoc-members:
   :show-inheritance: