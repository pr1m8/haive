
haive.core.common.mixins.checkpointer_mixin
===========================================

.. py:module:: haive.core.common.mixins.checkpointer_mixin

.. autoapi-nested-parse::

   Checkpointer mixin for stateful graphs and execution persistence.

   This module provides a mixin that adds checkpointing capabilities to any class
   that uses LangGraph or LangChain for stateful execution. It handles both
   synchronous and asynchronous checkpointing patterns, state restoration, and
   runtime configuration management.

   Usage:
       ```python
       from pydantic import BaseModel, Field
       from langgraph.graph import StateGraph
       from haive.core.common.mixins import CheckpointerMixin
       from haive.core.persistence.config import CheckpointerConfig

       class MyAgent(CheckpointerMixin, BaseModel):
           # Define the required fields
           persistence: Optional[CheckpointerConfig] = Field(default=None)
           checkpoint_mode: str = Field(default="sync")

           def __init__(self, **data):
               super().__init__(**data)
               # Create graph
               builder = StateGraph(...)
               self.app = builder.compile()

           # Use run with automatic checkpointing
           def process(self, input_data, thread_id=None):
               return self.run(input_data, thread_id=thread_id)

           # Use streaming with automatic checkpointing
           def process_stream(self, input_data, thread_id=None):
               return self.stream(input_data, thread_id=thread_id)
       ```







Classes
-------

* :py:class:`CheckpointerMixin` - Mixin that provides checkpointing capabilities for stateful graph execution.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/common/mixins/checkpointer_mixin/CheckpointerMixin

Package Contents
----------------

