"""
Base graph implementation for the Haive framework.

This module provides the core graph data structures without
additional functionality, which is added via mixins.
"""

import logging
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from pydantic import BaseModel, Field

from haive.core.graph.branches.branch import Branch
from haive.core.graph.common.types import NodeType

# Setup logging
logger = logging.getLogger(__name__)


class GraphBase(BaseModel):
    """
    Base class for graph management in the Haive framework.

    This class provides the core data structures for a graph without
    additional functionality, which is added via mixins.
    """

    # Unique identifier and metadata
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

    # Core graph components
    nodes: Dict[str, Optional[Any]] = Field(default_factory=dict)
    edges: List[Tuple[str, str]] = Field(default_factory=list)
    branches: Dict[str, Branch] = Field(default_factory=dict)

    # Entry and finish points
    entry_points: List[str] = Field(default_factory=list)
    finish_points: List[str] = Field(default_factory=list)

    # Keep backward compatibility fields for singular points
    entry_point: Optional[str] = Field(
        default=None, description="Deprecated: Use entry_points instead"
    )
    finish_point: Optional[str] = Field(
        default=None, description="Deprecated: Use finish_points instead"
    )

    # Configuration
    state_schema: Optional[Any] = None

    # Additional components for advanced functionality
    subgraphs: Dict[str, Any] = Field(default_factory=dict)
    node_types: Dict[str, NodeType] = Field(default_factory=dict)

    # Tracking fields
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    model_config = {"arbitrary_types_allowed": True}

    def get_node(self, node_name: str) -> Optional[Any]:
        """
        Get a node by name.

        Args:
            node_name: Name of the node to retrieve

        Returns:
            Node object if found, None otherwise
        """
        return self.nodes.get(node_name)

    def get_nodes(self) -> Dict[str, Any]:
        """
        Get all nodes.

        Returns:
            Dictionary of node names to node objects
        """
        return {k: v for k, v in self.nodes.items() if v is not None}

    def get_edges(self) -> List[Tuple[str, str]]:
        """
        Get all edges.

        Returns:
            List of (source, target) edge tuples
        """
        return self.edges

    def get_branches(self) -> Dict[str, Branch]:
        """
        Get all branches.

        Returns:
            Dictionary of branch IDs to branch objects
        """
        return self.branches

    def get_entry_points(self) -> List[str]:
        """
        Get all entry points.

        Returns:
            List of entry point node names
        """
        return self.entry_points

    def get_finish_points(self) -> List[str]:
        """
        Get all finish points.

        Returns:
            List of finish point node names
        """
        return self.finish_points
