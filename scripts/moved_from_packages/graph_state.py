"""Graph state tracking for compilation optimization.

This module provides classes for tracking the state of a graph,
particularly whether it needs recompilation after changes.
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class CompilationState(BaseModel):
    """Track the compilation state of a graph.

    This class maintains a record of changes that would require recompilation
    and provides methods to check if recompilation is needed.
    """

    # Core tracking properties
    is_compiled: bool = False
    compile_timestamp: datetime | None = None
    schema_version: int = 0
    topology_version: int = 0

    # Detailed change tracking
    schema_changes: dict[str, int] = Field(default_factory=dict)
    node_changes: dict[str, int] = Field(default_factory=dict)
    edge_changes: list[tuple[str, str, int]] = Field(default_factory=list)
    branch_changes: dict[str, int] = Field(default_factory=dict)

    # Tracking flags
    track_detailed_changes: bool = True
    max_change_history: int = 100

    def mark_as_compiled(self) -> None:
        """Mark the graph as compiled."""
        self.is_compiled = True
        self.compile_timestamp = datetime.now()

        # Clear detailed change tracking
        if not self.track_detailed_changes:
            self.schema_changes.clear()
            self.node_changes.clear()
            self.edge_changes.clear()
            self.branch_changes.clear()

    def mark_as_dirty(self) -> None:
        """Mark the graph as needing recompilation."""
        self.is_compiled = False

    def track_schema_change(self, field_name: str) -> None:
        """Track a change to the schema."""
        self.schema_version += 1
        self.is_compiled = False

        if self.track_detailed_changes:
            self.schema_changes[field_name] = self.schema_version

    def track_node_change(self, node_name: str, change_type: str) -> None:
        """Track a node addition, update, or removal."""
        self.topology_version += 1
        self.is_compiled = False

        if self.track_detailed_changes:
            self.node_changes[f"{change_type}:{node_name}"] = self.topology_version

    def track_edge_change(self, source: str, target: str, change_type: str) -> None:
        """Track an edge addition or removal."""
        self.topology_version += 1
        self.is_compiled = False

        if self.track_detailed_changes:
            self.edge_changes.append((source, target, self.topology_version))

            # Maintain limited history
            if len(self.edge_changes) > self.max_change_history:
                self.edge_changes = self.edge_changes[-self.max_change_history :]

    def track_branch_change(self, branch_id: str, change_type: str) -> None:
        """Track a branch addition, update, or removal."""
        self.topology_version += 1
        self.is_compiled = False

        if self.track_detailed_changes:
            self.branch_changes[f"{change_type}:{branch_id}"] = self.topology_version

    def needs_recompilation(self) -> bool:
        """Check if the graph needs recompilation."""
        return not self.is_compiled

    def get_change_summary(self) -> dict[str, Any]:
        """Get a summary of changes since last compilation."""
        return {
            "schema_version": self.schema_version,
            "topology_version": self.topology_version,
            "schema_change_count": len(self.schema_changes),
            "node_change_count": len(self.node_changes),
            "edge_change_count": len(self.edge_changes),
            "branch_change_count": len(self.branch_changes),
            "is_compiled": self.is_compiled,
            "last_compiled": self.compile_timestamp,
        }
