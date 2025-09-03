
haive.core.engine.aug_llm.mcp_config
====================================

.. py:module:: haive.core.engine.aug_llm.mcp_config

.. autoapi-nested-parse::

   MCP-enhanced AugLLMConfig with full type checking.

   This module provides MCPAugLLMConfig, which extends AugLLMConfig with Model Context
   Protocol (MCP) support through proper mixin composition. It includes full type
   checking and seamless integration with the existing Haive configuration system.

   The configuration automatically discovers MCP tools, manages resources, and enhances
   prompts while maintaining compatibility with all existing AugLLMConfig features.






Functions
---------

   create_mcp_aug_llm_config
.. autofunction:: create_mcp_aug_llm_config

Classes
-------

* :py:class:`MCPAugLLMConfig` - AugLLMConfig enhanced with MCP (Model Context Protocol) support.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/aug_llm/mcp_config/MCPAugLLMConfig

Package Contents
----------------

