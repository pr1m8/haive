
:py:mod:`haive.core.engine.tool`
========================

.. py:module:: haive.core.engine.tool

.. autoapi-nested-parse::

   Tool engine module for the Haive framework.

   This module provides engine implementations for LangChain tools and toolkits,
   enabling tool execution within the Haive framework's engine system.

   The tool engine supports individual tools, collections of tools, and toolkits,
   with features like automatic routing, parallel execution, and retry policies.
   It integrates with LangGraph for tool execution management and provides a
   consistent interface for tool usage across the framework.

   Key Components:
       ToolEngine: Engine for executing tools based on input state

   Features:
       - Support for multiple tool types (BaseTool, Tool, StructuredTool, BaseModel)
       - Toolkit integration for grouped tool functionality
       - Automatic tool routing based on input
       - Parallel tool execution when appropriate
       - Configurable retry policies
       - Message-based tool invocation
       - Source tracking for tool results

   .. admonition:: Examples

      Basic tool engine::
      
          from haive.core.engine.tool import ToolEngine
          from langchain_core.tools import Tool
      
          def calculator(expression: str) -> str:
              return str(eval(expression))
      
          calc_tool = Tool(
              name="calculator",
              description="Calculate mathematical expressions",
              func=calculator
          )
      
          engine = ToolEngine(
              name="calc_engine",
              tools=[calc_tool]
          )
      
          result = engine.invoke({
              "messages": [{"role": "user", "content": "Calculate 2 + 2"}]
          })
      
      Tool engine with toolkit::
      
          from haive.core.engine.tool import ToolEngine
          from langchain_community.agent_toolkits import SQLDatabaseToolkit
      
          toolkit = SQLDatabaseToolkit(db=database)
      
          engine = ToolEngine(
              name="sql_engine",
              toolkit=toolkit,
              parallel=True,
              auto_route=True
          )
      
      Tool engine with retry policy::
      
          from haive.core.engine.tool import ToolEngine
          from langgraph.types import RetryPolicy
      
          engine = ToolEngine(
              name="robust_engine",
              tools=my_tools,
              retry_policy=RetryPolicy(
                  max_attempts=3,
                  initial_interval=1.0,
                  backoff_factor=2.0
              )
          )

   .. seealso::

      - LangChain tools documentation
      - Tool implementation: base.py
      - LangGraph integration guide





Submodules
----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

   haive.core.engine.tool.base
.. toctree::
   :maxdepth: 1
   :hidden:

   /api_clean/haive/core/engine/tool/base/index





Package Contents
----------------

.. rubric:: haive.core.engine.tool.__all__

.. autosummary::
   :nosignatures:

   haive.core.engine.tool.ToolEngine

.. automodule:: haive.core.engine.tool
   :members:
   :undoc-members:
   :show-inheritance: