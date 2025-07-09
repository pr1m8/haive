"""Components module for the Haive state graph system.

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

Example:
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
"""

# New modular components
from haive.core.graph.state_graph.components.base_component import (
    BaseGraphComponent,
    ComponentRegistry,
)

# Modular components
from haive.core.graph.state_graph.components.branch_manager import BranchManager
from haive.core.graph.state_graph.components.edge_manager import EdgeManager
from haive.core.graph.state_graph.components.modular_base_graph import ModularBaseGraph
from haive.core.graph.state_graph.components.node_manager import NodeManager

# Legacy components (if they exist)
try:
    from haive.core.graph.state_graph.components.branch import Branch
except ImportError:
    from haive.core.graph.branches.branch import Branch

try:
    from haive.core.graph.state_graph.components.node import Node
except ImportError:
    from haive.core.graph.state_graph.base_graph2 import Node

__all__ = [
    # Legacy components
    "Node",
    "Branch",
    # New modular components
    "BaseGraphComponent",
    "ComponentRegistry",
    "NodeManager",
    "EdgeManager",
    "BranchManager",
    "ModularBaseGraph",
]
