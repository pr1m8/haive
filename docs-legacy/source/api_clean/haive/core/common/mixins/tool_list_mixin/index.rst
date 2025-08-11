
haive.core.common.mixins.tool_list_mixin
========================================

.. py:module:: haive.core.common.mixins.tool_list_mixin

.. autoapi-nested-parse::

   Tool list mixin for managing LangChain tools.

   This module provides a mixin that adds LangChain tool management capabilities
   to Pydantic models. It defines a ToolList class that manages various tool types
   with automatic expansion of toolkits, type tracking, and convenient querying.

   Usage:
       ```python
       from pydantic import BaseModel
       from haive.core.common.mixins.tool_list_mixin import ToolListMixin
       from langchain_core.tools import BaseTool, Tool

       class MyAgent(ToolListMixin, BaseModel):
           name: str

           def run(self, query: str):
               # Access tools by name
               calculator = self.tools.get_tool("calculator")
               result = calculator.run(query)
               return result

       # Create tools
       search_tool = Tool(name="search", func=lambda x: f"Searched for {x}")
       calculator = Tool(name="calculator", func=lambda x: f"Calculated {x}")

       # Create agent with tools
       agent = MyAgent(name="MyAgent", tools=[search_tool, calculator])

       # Get all tools of a specific type
       base_tools = agent.tools.get_by_tool_type("base_tool_instance")
       ```







Classes
-------

* :py:class:`ToolList` - A specialized collection for managing LangChain tools.* :py:class:`ToolListMixin` - Mixin that adds a ToolList for managing LangChain tools.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/common/mixins/tool_list_mixin/ToolList   /api_clean/haive/core/common/mixins/tool_list_mixin/ToolListMixin

Package Contents
----------------

