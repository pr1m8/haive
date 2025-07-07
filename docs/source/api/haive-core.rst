Haive Core
==========

.. note::
   
   For the complete Haive Core API documentation with detailed module breakdowns, please visit:
   
   📚 **:doc:`haive-core/index`**
   
   The new documentation provides:
   
   - Organized module hierarchy
   - Detailed submodule documentation
   - Better navigation within the package
   - Code examples for each component

Quick Links
-----------

.. grid:: 1 2 2 3
   :gutter: 3

   .. grid-item-card:: 🤖 **Engine System**
      :link: haive-core/engine/index
      :link-type: doc
      
      LLM integration and augmentation

   .. grid-item-card:: 📊 **Schema System**
      :link: haive-core/schema/index
      :link-type: doc
      
      Dynamic state schema composition

   .. grid-item-card:: 🌐 **Graph System**
      :link: haive-core/graph/index
      :link-type: doc
      
      State machines and workflows

Legacy Module Links
~~~~~~~~~~~~~~~~~~~

For backwards compatibility, the following direct module links are still available:

.. toctree::
   :maxdepth: 1
   :caption: Direct Module Access
   
   generated/haive.core.engine
   generated/haive.core.graph
   generated/haive.core.schema
   generated/haive.core.persistence
   generated/haive.core.registry
   generated/haive.core.tools


Quick Reference
~~~~~~~~~~~~~~~

**Engine Configuration**

.. code-block:: python

   from haive.core.engine import AugLLMConfig, get_llm
   
   # Configure an LLM
   engine = AugLLMConfig(
       model="gpt-4",
       temperature=0.7,
       system_message="You are a helpful assistant"
   )
   
   # Or use the registry
   llm = get_llm("gpt-4")

**State Schema**

.. code-block:: python

   from haive.core.schema import BaseStateSchema
   from typing import List
   
   class MyAgentState(BaseStateSchema):
       messages: List[str] = []
       context: Dict[str, Any] = {}
       
       class Config:
           schema_id = "my_agent_state_v1"

**Graph Building**

.. code-block:: python

   from haive.core.graph import GraphBuilder
   
   builder = GraphBuilder()
   builder.add_node("start", start_node)
   builder.add_node("process", process_node)
   builder.add_edge("start", "process")
   
   graph = builder.compile()

