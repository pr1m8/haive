
:py:mod:`haive.core.common.mixins.general`
========================

.. py:module:: haive.core.common.mixins.general

.. autoapi-nested-parse::

   General-purpose mixins providing basic functionality for Haive components.

   This package contains fundamental mixins that provide core functionality
   like ID management, serialization, state tracking, and versioning. These
   mixins are designed to be lightweight and composable, making them suitable
   for inclusion in a wide variety of components.

   Available mixins:
   - IdMixin: Basic ID generation and management
   - MetadataMixin: Key-value metadata storage
   - SerializationMixin: Enhanced serialization capabilities
   - StateMixin: State tracking and validation
   - TimestampMixin: Creation and modification timestamp tracking
   - VersionMixin: Version tracking and compatibility checking

   Usage:
       ```python
       from pydantic import BaseModel
       from haive.core.common.mixins.general import (
           IdMixin, TimestampMixin, VersionMixin
       )

       class MyComponent(IdMixin, TimestampMixin, VersionMixin, BaseModel):
           name: str

           def __init__(self, **data):
               super().__init__(**data)
               # Now the component has ID, timestamp, and version capabilities
       ```





Submodules
----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

   haive.core.common.mixins.general.id   haive.core.common.mixins.general.metadata   haive.core.common.mixins.general.serialization   haive.core.common.mixins.general.state   haive.core.common.mixins.general.timestamp   haive.core.common.mixins.general.version
.. toctree::
   :maxdepth: 1
   :hidden:

   /api_clean/haive/core/common/mixins/general/id/index   /api_clean/haive/core/common/mixins/general/metadata/index   /api_clean/haive/core/common/mixins/general/serialization/index   /api_clean/haive/core/common/mixins/general/state/index   /api_clean/haive/core/common/mixins/general/timestamp/index   /api_clean/haive/core/common/mixins/general/version/index





Package Contents
----------------

.. rubric:: haive.core.common.mixins.general.__all__

.. autosummary::
   :nosignatures:

   haive.core.common.mixins.general.IdMixin   haive.core.common.mixins.general.MetadataMixin   haive.core.common.mixins.general.SerializationMixin   haive.core.common.mixins.general.StateMixin   haive.core.common.mixins.general.TimestampMixin   haive.core.common.mixins.general.VersionMixin

.. automodule:: haive.core.common.mixins.general
   :members:
   :undoc-members:
   :show-inheritance: