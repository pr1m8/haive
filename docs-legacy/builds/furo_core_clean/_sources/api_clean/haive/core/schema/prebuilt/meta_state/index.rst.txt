
haive.core.schema.prebuilt.meta_state
=====================================

.. py:module:: haive.core.schema.prebuilt.meta_state

.. autoapi-nested-parse::

   Meta state schema with embedded agent and graph composition support.

   This module provides MetaStateSchema, a specialized state schema for graph-level
   agent composition and recompilation management. It focuses on agent lifecycle,
   graph coordination, and dynamic recompilation rather than tool routing.

   The meta state pattern enables:
   - Agent embedding within graph states
   - Graph composition and coordination
   - Recompilation tracking and management
   - Agent lifecycle management
   - Dynamic agent modification

   .. admonition:: Example

      ```python
      from haive.core.schema.prebuilt.meta_state import MetaStateSchema
      from haive.agents.simple.agent import SimpleAgent
      
      # Create a contained agent
      inner_agent = SimpleAgent()
      
      # Create meta state with embedded agent
      meta_state = MetaStateSchema(
          agent=inner_agent,
          agent_state={"initialized": True},
          graph_context={"composition": "nested"}
      )
      
      # Agent can be executed and recompiled within graph nodes
      result = meta_state.execute_agent()
      ```







Classes
-------

* :py:class:`MetaStateSchema` - State schema with embedded agent and graph composition support.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/schema/prebuilt/meta_state/MetaStateSchema

Package Contents
----------------

