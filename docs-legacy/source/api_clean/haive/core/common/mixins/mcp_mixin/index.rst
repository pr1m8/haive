
haive.core.common.mixins.mcp_mixin
==================================

.. py:module:: haive.core.common.mixins.mcp_mixin

.. autoapi-nested-parse::

   MCP (Model Context Protocol) mixin for adding MCP support to configurations.

   This module provides a mixin that enhances configuration classes with MCP integration
   capabilities. It enables automatic discovery and wrapping of MCP tools, resource
   management, and prompt template integration while maintaining compatibility with
   existing Haive patterns.

   Usage:
       ```python
       from pydantic import BaseModel
       from haive.core.common.mixins import MCPMixin
       from haive.mcp.config import MCPConfig, MCPServerConfig

       class MyConfig(MCPMixin, BaseModel):
           name: str

       # Create config with MCP support
       config = MyConfig(
           name="agent",
           mcp_config=MCPConfig(
               enabled=True,
               servers={
                   "filesystem": MCPServerConfig(
                       transport="stdio",
                       command="npx",
                       args=["-y", "@modelcontextprotocol/server-filesystem"]
                   )
               }
           )
       )

       # Initialize MCP (discovers tools, resources, prompts)
       await config.setup_mcp()

       # Access MCP tools (automatically wrapped)
       tools = config.get_mcp_tools()

       # Access MCP resources
       resources = config.get_mcp_resources()

       # Use MCP-enhanced system prompt
       enhanced_prompt = config.enhance_system_prompt_with_mcp("Base prompt")
       ```







Classes
-------

* :py:class:`MCPResource` - Model representing an MCP resource.* :py:class:`MCPPromptTemplate` - Model representing an MCP prompt template.* :py:class:`MCPToolWrapper` - Wrapper to convert MCP tools to Haive-compatible tools.* :py:class:`MCPMixin` - Mixin for adding MCP (Model Context Protocol) support to configurations.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/common/mixins/mcp_mixin/MCPResource   /api_clean/haive/core/common/mixins/mcp_mixin/MCPPromptTemplate   /api_clean/haive/core/common/mixins/mcp_mixin/MCPToolWrapper   /api_clean/haive/core/common/mixins/mcp_mixin/MCPMixin

Package Contents
----------------

