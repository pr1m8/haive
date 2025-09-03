
:py:mod:`haive.core.common.mixins`
========================

.. py:module:: haive.core.common.mixins

.. autoapi-nested-parse::

   Mixins package providing reusable functionality for Haive components.

   This package contains a collection of mixins that provide common functionality
   that can be composed into classes through multiple inheritance. Mixins help
   avoid code duplication and promote consistent behavior across the codebase.

   The mixins are organized into several categories:
   - General purpose mixins (ID, state, versioning, etc.)
   - Engine integration mixins
   - Tool management mixins
   - Configuration mixins
   - State management mixins

   Usage:
       ```python
       from haive.core.common.mixins import IdentifierMixin, StateMixin

       class MyComponent(IdentifierMixin, StateMixin):
           def __init__(self, id: str = None):
               super().__init__(id=id)
               # Now the class has ID management and state management capabilities
       ```




Subpackages
-----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

   haive.core.common.mixins.general   haive.core.common.mixins.mixins
.. toctree::
   :maxdepth: 2
   :hidden:

   /api_clean/haive/core/common/mixins/general/index   /api_clean/haive/core/common/mixins/mixins/index

Submodules
----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

   haive.core.common.mixins.checkpointer_mixin   haive.core.common.mixins.dynamic_tool_route_mixin   haive.core.common.mixins.engine_mixin   haive.core.common.mixins.getter_mixin   haive.core.common.mixins.identifier   haive.core.common.mixins.mcp_mixin   haive.core.common.mixins.prompt_template_mixin   haive.core.common.mixins.recompile_mixin   haive.core.common.mixins.rich_logger_mixin   haive.core.common.mixins.secure_config   haive.core.common.mixins.state_interface_mixin   haive.core.common.mixins.structured_output_mixin   haive.core.common.mixins.timestamp_mixin   haive.core.common.mixins.tool_list_mixin   haive.core.common.mixins.tool_route_mixin
.. toctree::
   :maxdepth: 1
   :hidden:

   /api_clean/haive/core/common/mixins/checkpointer_mixin/index   /api_clean/haive/core/common/mixins/dynamic_tool_route_mixin/index   /api_clean/haive/core/common/mixins/engine_mixin/index   /api_clean/haive/core/common/mixins/getter_mixin/index   /api_clean/haive/core/common/mixins/identifier/index   /api_clean/haive/core/common/mixins/mcp_mixin/index   /api_clean/haive/core/common/mixins/prompt_template_mixin/index   /api_clean/haive/core/common/mixins/recompile_mixin/index   /api_clean/haive/core/common/mixins/rich_logger_mixin/index   /api_clean/haive/core/common/mixins/secure_config/index   /api_clean/haive/core/common/mixins/state_interface_mixin/index   /api_clean/haive/core/common/mixins/structured_output_mixin/index   /api_clean/haive/core/common/mixins/timestamp_mixin/index   /api_clean/haive/core/common/mixins/tool_list_mixin/index   /api_clean/haive/core/common/mixins/tool_route_mixin/index





Package Contents
----------------

.. rubric:: haive.core.common.mixins.__all__

.. autosummary::
   :nosignatures:

   haive.core.common.mixins.CheckpointerMixin   haive.core.common.mixins.EngineMixin   haive.core.common.mixins.GetterMixin   haive.core.common.mixins.IdMixin   haive.core.common.mixins.IdentifierMixin   haive.core.common.mixins.MCPMixin   haive.core.common.mixins.MetadataMixin   haive.core.common.mixins.RichLoggerMixin   haive.core.common.mixins.SecureConfigMixin   haive.core.common.mixins.SerializationMixin   haive.core.common.mixins.StateInterfaceMixin   haive.core.common.mixins.StateMixin   haive.core.common.mixins.StructuredOutputMixin   haive.core.common.mixins.TimestampMixin   haive.core.common.mixins.ToolListMixin   haive.core.common.mixins.ToolRouteMixin   haive.core.common.mixins.VersionMixin

.. automodule:: haive.core.common.mixins
   :members:
   :undoc-members:
   :show-inheritance: