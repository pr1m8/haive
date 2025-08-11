
:py:mod:`haive.core.graph.state_graph`
========================

.. py:module:: haive.core.graph.state_graph

.. autoapi-nested-parse::

   Haive State Graph System.

   This package provides a comprehensive graph implementation for the Haive framework,
   with flexible node and branch management, visualization, and LangGraph integration.

   The state graph system is the foundational computational graph infrastructure in Haive,
   enabling the creation, manipulation, and execution of complex workflows with robust
   state management and schema validation.

   Key Features:
       - Schema Validation: Enforce type safety through Pydantic models
       - Dynamic Routing: Create complex workflows with conditional branching
       - Serialization: Full serialization and deserialization support
       - LangGraph Integration: Seamless integration with LangChain's LangGraph
       - Visualization: Built-in visualization capabilities
       - Pattern Support: Reusable graph patterns and templates

   Modules:
       base_graph2: Core graph implementation (transitional version)
       schema_graph: Schema-aware graph with validation
       state_graph: State graph serialization model
       components: Node and branch implementations
       models: Data models for graph components
       conversion: Format conversion utilities
       pattern: Graph pattern implementations
       utils: Utility functions

   .. admonition:: Example

      Basic graph creation:
      ```python
      from haive.core.graph.state_graph import BaseGraph
      from langgraph.graph import START, END
      
      # Create a new graph
      graph = BaseGraph(name="my_graph")
      
      # Add nodes
      graph.add_node("node1", lambda state: state)
      graph.add_node("node2", lambda state: state)
      
      # Add edges
      graph.add_edge(START, "node1")
      graph.add_edge("node1", "node2")
      graph.add_edge("node2", END)
      
      # Compile and run the graph
      compiled_graph = graph.compile()
      result = compiled_graph.invoke({"input": "some input"})
      ```




Subpackages
-----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

   haive.core.graph.state_graph.components   haive.core.graph.state_graph.conversion   haive.core.graph.state_graph.pattern   haive.core.graph.state_graph.utils
.. toctree::
   :maxdepth: 2
   :hidden:

   /api_clean/haive/core/graph/state_graph/components/index   /api_clean/haive/core/graph/state_graph/conversion/index   /api_clean/haive/core/graph/state_graph/pattern/index   /api_clean/haive/core/graph/state_graph/utils/index

Submodules
----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

   haive.core.graph.state_graph.base   haive.core.graph.state_graph.base_graph2   haive.core.graph.state_graph.compiled_state_graph   haive.core.graph.state_graph.graph_path   haive.core.graph.state_graph.graph_visualizer   haive.core.graph.state_graph.mixin   haive.core.graph.state_graph.pattern_decorator   haive.core.graph.state_graph.pattern_definition   haive.core.graph.state_graph.pattern_registry   haive.core.graph.state_graph.registry   haive.core.graph.state_graph.schema_graph   haive.core.graph.state_graph.schema_mixin   haive.core.graph.state_graph.serializable   haive.core.graph.state_graph.state_graph   haive.core.graph.state_graph.state_graph_builder   haive.core.graph.state_graph.types   haive.core.graph.state_graph.validation_mixin
.. toctree::
   :maxdepth: 1
   :hidden:

   /api_clean/haive/core/graph/state_graph/base/index   /api_clean/haive/core/graph/state_graph/base_graph2/index   /api_clean/haive/core/graph/state_graph/compiled_state_graph/index   /api_clean/haive/core/graph/state_graph/graph_path/index   /api_clean/haive/core/graph/state_graph/graph_visualizer/index   /api_clean/haive/core/graph/state_graph/mixin/index   /api_clean/haive/core/graph/state_graph/pattern_decorator/index   /api_clean/haive/core/graph/state_graph/pattern_definition/index   /api_clean/haive/core/graph/state_graph/pattern_registry/index   /api_clean/haive/core/graph/state_graph/registry/index   /api_clean/haive/core/graph/state_graph/schema_graph/index   /api_clean/haive/core/graph/state_graph/schema_mixin/index   /api_clean/haive/core/graph/state_graph/serializable/index   /api_clean/haive/core/graph/state_graph/state_graph/index   /api_clean/haive/core/graph/state_graph/state_graph_builder/index   /api_clean/haive/core/graph/state_graph/types/index   /api_clean/haive/core/graph/state_graph/validation_mixin/index





Package Contents
----------------

.. rubric:: haive.core.graph.state_graph.__all__

.. autosummary::
   :nosignatures:

   haive.core.graph.state_graph.BaseGraph   haive.core.graph.state_graph.Branch   haive.core.graph.state_graph.GraphVisualizer   haive.core.graph.state_graph.Node   haive.core.graph.state_graph.SchemaGraph   haive.core.graph.state_graph.convert_to_langgraph

.. automodule:: haive.core.graph.state_graph
   :members:
   :undoc-members:
   :show-inheritance: