"""
Base module for the state graph system.

This module provides the core graph data structures and types.
"""

from haive.core.graph.state_graph.base.graph_base import GraphBase
from haive.core.graph.state_graph.base.graph_state import CompilationState
from haive.core.graph.state_graph.base.types import (
    GRAPH_CONSTANTS,
    BranchResultType,
    BranchType,
    Edge,
    EdgeType,
    SimpleEdge,
)

# Constants
START = GRAPH_CONSTANTS["START"]
END = GRAPH_CONSTANTS["END"]

__all__ = [
    "GraphBase",
    "CompilationState",
    "BranchResultType",
    "BranchType",
    "Edge",
    "EdgeType",
    "SimpleEdge",
    "START",
    "END",
]
