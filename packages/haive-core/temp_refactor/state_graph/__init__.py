"""
State graph system for the Haive framework.

This module provides a comprehensive system for building, manipulating,
and executing graphs with consistent interfaces, serialization support,
and dynamic composition.
"""

from langgraph.graph import END, START

from haive.core.graph.state_graph.base import (
    BranchResultType,
    BranchType,
    Edge,
    EdgeType,
    GraphBase,
    SimpleEdge,
)
from haive.core.graph.state_graph.graph import StateGraph
from haive.core.graph.state_graph.mixins import (
    CompilationMixin,
    SchemaMixin,
    ValidationMixin,
)
from haive.core.graph.state_graph.schema_graph import SchemaGraph
from haive.core.graph.state_graph.visualization import MermaidGenerator

__all__ = [
    # Main graph classes
    "StateGraph",
    "SchemaGraph",
    # Base classes
    "GraphBase",
    # Mixins
    "CompilationMixin",
    "SchemaMixin",
    "ValidationMixin",
    # Types
    "BranchResultType",
    "BranchType",
    "Edge",
    "EdgeType",
    "SimpleEdge",
    # Constants
    "START",
    "END",
    # Visualization
    "MermaidGenerator",
]
