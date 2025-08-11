
:py:mod:`haive.core.graph`
========================

.. py:module:: haive.core.graph

.. autoapi-nested-parse::

   Graph system for building AI workflows in the Haive framework.

   This module provides a powerful, flexible system for creating graph-based workflows
   that orchestrate AI agents, tools, and data processing pipelines. The graph system
   is built on top of LangGraph and extends it with Haive-specific features for
   agent coordination, dynamic state management, and advanced workflow patterns.

   The graph system enables complex AI workflows through composable nodes, conditional
   routing, parallel processing, and state persistence. It's designed to handle
   everything from simple linear workflows to complex multi-agent orchestration.

   Key Components:
       BaseGraph: Foundation class for all graph implementations
           - State schema management and validation
           - Node registration and execution
           - Edge definition and routing logic
           - Built-in persistence and checkpointing
           - Visual graph representation and debugging

       Graph Builder Components:
           - Dynamic graph construction from configuration
           - Pattern-based graph templates
           - Node factory system for component creation
           - Advanced routing and branching logic

       State Management:
           - Schema composition and validation
           - State sharing between parent and child graphs
           - Reducer functions for intelligent state merging
           - Field-level access control and visibility

   Features:
       - Dynamic graph construction and modification
       - Schema-aware state management
       - Parallel and conditional execution
       - Built-in persistence and checkpointing
       - Visual graph debugging and analysis
       - Pattern-based workflow templates
       - Tool and agent integration
       - Error handling and recovery
       - Performance monitoring and optimization

   .. admonition:: Examples

      Basic graph creation::
      
          from haive.core.graph import BaseGraph
          from haive.core.schema import StateSchema
      
          class MyWorkflowState(StateSchema):
              query: str = ""
              results: List[str] = []
      
          graph = BaseGraph(state_schema=MyWorkflowState)
      
          # Add nodes
          graph.add_node("process", processing_function)
          graph.add_node("validate", validation_function)
      
          # Define flow
          graph.set_entry_point("process")
          graph.add_edge("process", "validate")
          graph.set_finish_point("validate")
      
          # Compile and run
          compiled_graph = graph.compile()
          result = compiled_graph.invoke({"query": "What is AI?"})
      
      Agent integration::
      
          from haive.core.graph import BaseGraph
          from haive.agents.simple import SimpleAgent
      
          # Create agents
          research_agent = SimpleAgent(name="researcher")
          writer_agent = SimpleAgent(name="writer")
      
          # Build workflow
          graph = BaseGraph()
          graph.add_agent_node("research", research_agent)
          graph.add_agent_node("write", writer_agent)
      
          # Sequential workflow
          graph.set_entry_point("research")
          graph.add_edge("research", "write")
          graph.set_finish_point("write")
      
      Conditional routing::
      
          def route_logic(state):
              if state["requires_verification"]:
                  return "verify"
              return "finalize"
      
          graph.add_conditional_edges(
              source="process",
              path=route_logic,
              path_map={"verify": "verification", "finalize": "finalization"}
          )

   .. seealso::

      - Node system: haive.core.graph.node
      - State management: haive.core.schema
      - Agent integration: haive.agents
      - Workflow patterns: haive.core.graph.patterns




Subpackages
-----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

   haive.core.graph.branches   haive.core.graph.common   haive.core.graph.gb   haive.core.graph.node   haive.core.graph.patterns   haive.core.graph.retry   haive.core.graph.routers   haive.core.graph.state_graph   haive.core.graph.utils
.. toctree::
   :maxdepth: 2
   :hidden:

   /api_clean/haive/core/graph/branches/index   /api_clean/haive/core/graph/common/index   /api_clean/haive/core/graph/gb/index   /api_clean/haive/core/graph/node/index   /api_clean/haive/core/graph/patterns/index   /api_clean/haive/core/graph/retry/index   /api_clean/haive/core/graph/routers/index   /api_clean/haive/core/graph/state_graph/index   /api_clean/haive/core/graph/utils/index

Submodules
----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

   haive.core.graph.NodeFactory   haive.core.graph.StateGraphEditor   haive.core.graph.StateSchema   haive.core.graph.ToolManager   haive.core.graph.dynamic_graph_builder   haive.core.graph.graph_builder2   haive.core.graph.graph_pattern_registry   haive.core.graph.routing   haive.core.graph.state_graph_manager   haive.core.graph.tool_config   haive.core.graph.tool_injector   haive.core.graph.tool_manager
.. toctree::
   :maxdepth: 1
   :hidden:

   /api_clean/haive/core/graph/NodeFactory/index   /api_clean/haive/core/graph/StateGraphEditor/index   /api_clean/haive/core/graph/StateSchema/index   /api_clean/haive/core/graph/ToolManager/index   /api_clean/haive/core/graph/dynamic_graph_builder/index   /api_clean/haive/core/graph/graph_builder2/index   /api_clean/haive/core/graph/graph_pattern_registry/index   /api_clean/haive/core/graph/routing/index   /api_clean/haive/core/graph/state_graph_manager/index   /api_clean/haive/core/graph/tool_config/index   /api_clean/haive/core/graph/tool_injector/index   /api_clean/haive/core/graph/tool_manager/index





Package Contents
----------------

.. rubric:: haive.core.graph.__all__

.. autosummary::
   :nosignatures:

   haive.core.graph.BaseGraph

.. automodule:: haive.core.graph
   :members:
   :undoc-members:
   :show-inheritance: