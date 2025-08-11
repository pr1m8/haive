
haive.core.common.mixins.tool_route_mixin
=========================================

.. py:module:: haive.core.common.mixins.tool_route_mixin

.. autoapi-nested-parse::

   Tool routing mixin for managing tool destinations and metadata.

   This module provides a mixin for managing tool routes and related metadata in
   configuration classes. It enables mapping tool names to their types or destinations,
   keeping track of metadata, and provides utilities for creating tools from configs.

   Usage:
       ```python
       from pydantic import BaseModel
       from haive.core.common.mixins import ToolRouteMixin

       class AgentConfig(ToolRouteMixin, BaseModel):
           name: str
           description: str

           def _create_tool_implementation(self, name, description, **kwargs):
               # Custom tool creation logic
               return SomeTool(name=name, description=description)

       # Create config with tool routes
       config = AgentConfig(
           name="MyAgent",
           description="Agent configuration"
       )

       # Set tool routes
       config.set_tool_route("search", "retriever", {"source": "web"})
       config.set_tool_route("math", "function", {"language": "python"})

       # Create a tool
       search_tool = config.to_tool(name="search", description="Web search tool")

       # Get routes by type
       retriever_tools = config.list_tools_by_route("retriever")
       ```







Classes
-------

* :py:class:`ToolRouteMixin` - Enhanced mixin for managing tools, routes, and converting configurations to tools.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/common/mixins/tool_route_mixin/ToolRouteMixin

Package Contents
----------------

