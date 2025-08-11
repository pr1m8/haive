
haive.core.schema.state_schema
==============================

.. py:module:: haive.core.schema.state_schema

.. autoapi-nested-parse::

   State schema base class for the Haive framework.

   from typing import Any
   This module provides the StateSchema base class that extends Pydantic's BaseModel
   with features specifically designed for AI agent state management and graph-based
   workflows. The StateSchema class adds powerful capabilities including field sharing
   between parent and child graphs, reducer functions for state updates, engine I/O
   tracking, and extensive serialization support.

   StateSchema serves as the foundation of the Haive Schema System, enabling fully
   dynamic and serializable state schemas that can be composed, modified, and extended
   at runtime. This flexibility makes it ideal for complex agent architectures and
   nested workflows.

   Key features include:
   - Field sharing: Share state between parent and child graphs with explicit control
   - Reducer functions: Define how field values should be combined during state updates
   - Engine I/O tracking: Map which fields are inputs and outputs for specific engines
   - Message handling: Built-in methods for working with message fields
   - Serialization: Comprehensive support for converting to/from dictionaries and JSON
   - State manipulation: Methods for updating, merging, and comparing states
   - Pretty printing: Rich visualization of state content
   - Engine integration: Prepare inputs and process outputs for specific engines

   .. admonition:: Example

      ```python
      from typing import List
      from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
      from pydantic import Field
      from haive.core.schema import StateSchema
      from langgraph.graph import add_messages
      
      class ConversationState(StateSchema):
          messages: List[BaseMessage] = Field(default_factory=list)
          query: str = Field(default="")
          response: str = Field(default="")
          context: List[str] = Field(default_factory=list)
      
          # Define which fields should be shared with parent graphs
          __shared_fields__ = ["messages"]
      
          # Define reducer functions for each field
          __reducer_fields__ = {
              "messages": add_messages,
              "context": lambda a, b: (a or []) + (b or [])
          }
      
          # Define which fields are inputs/outputs for which engines
          __engine_io_mappings__ = {
              "retriever": {
                  "inputs": ["query"],
                  "outputs": ["context"]
              },
              "llm": {
                  "inputs": ["query", "context", "messages"],
                  "outputs": ["response"]
              }
          }
      ```







Classes
-------

* :py:class:`EngineIOConfig` - Configuration for engine input/output mappings.* :py:class:`StateConfig` - Configuration for state schema metadata.* :py:class:`StateSchema` - Enhanced base class for state schemas in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/schema/state_schema/EngineIOConfig   /api_clean/haive/core/schema/state_schema/StateConfig   /api_clean/haive/core/schema/state_schema/StateSchema

Package Contents
----------------

