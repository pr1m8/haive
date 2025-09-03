
haive.core.tools.interrupt_tool_wrapper
=======================================

.. py:module:: haive.core.tools.interrupt_tool_wrapper

.. autoapi-nested-parse::

   from typing import Any
   Human-in-the-Loop Tool Wrapper for LangGraph Agents.

   This module defines a utility function `add_human_in_the_loop` that allows
   LangChain tools to be wrapped with interrupt-based human review via LangGraph.
   This enables human approval, editing, or feedback substitution before a tool is executed.

   Typical usage:
       from this_module import add_human_in_the_loop

       @tool
       def search_docs(query: str) -> str:
           return f"Results for: {query}"

       safe_tool = add_human_in_the_loop(search_docs)
       result = safe_tool.invoke({"query": "pydantic base models"})






Functions
---------

   add_human_in_the_loop
.. autofunction:: add_human_in_the_loop



Package Contents
----------------

