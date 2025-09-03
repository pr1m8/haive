
:py:mod:`haive.core.utils`
========================

.. py:module:: haive.core.utils

.. autoapi-nested-parse::

   Core utility functions and helpers.

   This module provides common utility functions and helpers used throughout
   the Haive framework. It includes utilities for Pydantic models, tools,
   discovery mechanisms, and other shared functionality.

   The utilities are organized into submodules:
       - pydantic_utils: Helpers for working with Pydantic models
       - tools: Tool-related utilities and helpers
       - haive_discovery: Discovery and introspection utilities

   .. admonition:: Example

      Basic usage::
      
          from haive.core.utils import pydantic_utils
          from haive.core.utils.tools import create_tool
      
          # Use utilities for model operations
          serialized = pydantic_utils.model_to_dict(my_model)

   .. seealso::

      :mod:`haive.core.utils.pydantic_utils`: Pydantic model utilities
      :mod:`haive.core.utils.tools`: Tool creation and management utilities
      :mod:`haive.core.utils.haive_discovery`: Component discovery utilities




Subpackages
-----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

   haive.core.utils.debugkit   haive.core.utils.haive_discovery   haive.core.utils.pydantic_utils   haive.core.utils.tools
.. toctree::
   :maxdepth: 2
   :hidden:

   /api_clean/haive/core/utils/debugkit/index   /api_clean/haive/core/utils/haive_discovery/index   /api_clean/haive/core/utils/pydantic_utils/index   /api_clean/haive/core/utils/tools/index

Submodules
----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

   haive.core.utils.chat_utils   haive.core.utils.config   haive.core.utils.config_utils   haive.core.utils.doc_utils   haive.core.utils.env_utils   haive.core.utils.file_utils   haive.core.utils.getter_mixin   haive.core.utils.haive_collections   haive.core.utils.inspection   haive.core.utils.interrupt_utils   haive.core.utils.logging_utils   haive.core.utils.mermaid_utils   haive.core.utils.message_utils   haive.core.utils.model_utils   haive.core.utils.parser_utils   haive.core.utils.runnable_config_utils   haive.core.utils.serialization   haive.core.utils.state_utils   haive.core.utils.tool_list   haive.core.utils.tool_utils   haive.core.utils.visualize_graph_utils
.. toctree::
   :maxdepth: 1
   :hidden:

   /api_clean/haive/core/utils/chat_utils/index   /api_clean/haive/core/utils/config/index   /api_clean/haive/core/utils/config_utils/index   /api_clean/haive/core/utils/doc_utils/index   /api_clean/haive/core/utils/env_utils/index   /api_clean/haive/core/utils/file_utils/index   /api_clean/haive/core/utils/getter_mixin/index   /api_clean/haive/core/utils/haive_collections/index   /api_clean/haive/core/utils/inspection/index   /api_clean/haive/core/utils/interrupt_utils/index   /api_clean/haive/core/utils/logging_utils/index   /api_clean/haive/core/utils/mermaid_utils/index   /api_clean/haive/core/utils/message_utils/index   /api_clean/haive/core/utils/model_utils/index   /api_clean/haive/core/utils/parser_utils/index   /api_clean/haive/core/utils/runnable_config_utils/index   /api_clean/haive/core/utils/serialization/index   /api_clean/haive/core/utils/state_utils/index   /api_clean/haive/core/utils/tool_list/index   /api_clean/haive/core/utils/tool_utils/index   /api_clean/haive/core/utils/visualize_graph_utils/index





Package Contents
----------------


.. automodule:: haive.core.utils
   :members:
   :undoc-members:
   :show-inheritance: