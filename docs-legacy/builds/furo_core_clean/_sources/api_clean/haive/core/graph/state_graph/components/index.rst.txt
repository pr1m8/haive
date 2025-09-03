
:py:mod:`haive.core.graph.state_graph.components`
========================

.. py:module:: haive.core.graph.state_graph.components

.. autoapi-nested-parse::

   Components module for the Haive state graph system.

   This module provides both legacy components and new modular components for building
   computational graphs with rich state management and control flow capabilities.

   Legacy Components:
       - Node: Base processing unit in a graph that handles state transformation
       - Branch: Conditional routing component for decision points in the graph

   New Modular Components (Composition-based architecture):
       - BaseGraphComponent: Abstract base for all graph components
       - ComponentRegistry: Manages component lifecycle
       - NodeManager: Handles all node operations
       - EdgeManager: Handles direct edge operations
       - BranchManager: Handles conditional routing and branches
       - ModularBaseGraph: Main graph class using composition

   .. admonition:: Example

      Using the new modular architecture:
      ```python
      from haive.core.graph.state_graph.components import ModularBaseGraph
      
      # Create a modular graph
      graph = ModularBaseGraph(name="my_workflow")
      
      # Add nodes
      graph.add_node("start", start_function)
      graph.add_node("process", process_function)
      
      # Add edges and routing
      graph.add_edge("start", "process")
      graph.add_conditional_edges("process", router_function, {
          "success": "finish",
          "error": "retry"
      })
      ```





Submodules
----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

   haive.core.graph.state_graph.components.architecture_summary   haive.core.graph.state_graph.components.base_component   haive.core.graph.state_graph.components.branch   haive.core.graph.state_graph.components.branch_manager   haive.core.graph.state_graph.components.demo_modular_benefits   haive.core.graph.state_graph.components.edge_manager   haive.core.graph.state_graph.components.modular_base_graph   haive.core.graph.state_graph.components.node   haive.core.graph.state_graph.components.node_manager
.. toctree::
   :maxdepth: 1
   :hidden:

   /api_clean/haive/core/graph/state_graph/components/architecture_summary/index   /api_clean/haive/core/graph/state_graph/components/base_component/index   /api_clean/haive/core/graph/state_graph/components/branch/index   /api_clean/haive/core/graph/state_graph/components/branch_manager/index   /api_clean/haive/core/graph/state_graph/components/demo_modular_benefits/index   /api_clean/haive/core/graph/state_graph/components/edge_manager/index   /api_clean/haive/core/graph/state_graph/components/modular_base_graph/index   /api_clean/haive/core/graph/state_graph/components/node/index   /api_clean/haive/core/graph/state_graph/components/node_manager/index





Package Contents
----------------

.. rubric:: haive.core.graph.state_graph.components.__all__

.. autosummary::
   :nosignatures:

   haive.core.graph.state_graph.components.BaseGraphComponent   haive.core.graph.state_graph.components.Branch   haive.core.graph.state_graph.components.BranchManager   haive.core.graph.state_graph.components.ComponentRegistry   haive.core.graph.state_graph.components.EdgeManager   haive.core.graph.state_graph.components.ModularBaseGraph   haive.core.graph.state_graph.components.Node   haive.core.graph.state_graph.components.NodeManager

.. automodule:: haive.core.graph.state_graph.components
   :members:
   :undoc-members:
   :show-inheritance: