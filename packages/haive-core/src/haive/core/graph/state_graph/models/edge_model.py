from enum import Enum
from typing import ClassVar, List, Optional

from pydantic import Field, model_validator

from haive.core.graph.state_graph.base import SerializableModel


class EdgeType(str, Enum):
    """Types of edges in a graph."""

    STANDARD = "standard"
    WAITING = "waiting"
    BRANCH = "branch"
    BRANCH_THEN = "branch_then"


class EdgeModel(SerializableModel):
    """Serializable representation of a graph edge."""

    source: str = Field(..., description="Source node name")
    target: str = Field(..., description="Target node name")
    edge_type: EdgeType = Field(default=EdgeType.STANDARD, description="Type of edge")
    sources: list[str] | None = Field(
        default=None, description="Source nodes for waiting edges"
    )
    branch_name: str | None = Field(
        default=None, description="Branch name for branch edges"
    )
    condition: str | None = Field(
        default=None, description="Condition value for branch edges"
    )

    __model_type__: ClassVar[str] = "edge"
    __abstract__ = False

    @model_validator(mode="after")
    def validate_edge_structure(self) -> "EdgeModel":
        """Validate edge structure based on type."""
        if self.edge_type == EdgeType.WAITING and not self.sources:
            raise ValueError("Waiting edges must specify sources")

        if (
            self.edge_type in [EdgeType.BRANCH, EdgeType.BRANCH_THEN]
            and not self.branch_name
        ):
            raise ValueError("Branch edges must specify branch_name")

        if self.edge_type == EdgeType.BRANCH and not self.condition:
            raise ValueError("Branch edges must specify condition")

        return self

    @classmethod
    def create_standard(cls, source: str, target: str) -> "EdgeModel":
        """Create a standard edge."""
        return cls(
            name=f"{source}_to_{target}",
            source=source,
            target=target,
            edge_type=EdgeType.STANDARD,
        )

    @classmethod
    def create_waiting(cls, sources: list[str], target: str) -> "EdgeModel":
        """Create a waiting edge."""
        return cls(
            name=f"wait_{'+'.join(sources)}_to_{target}",
            source=sources[0],  # Representative source
            target=target,
            edge_type=EdgeType.WAITING,
            sources=sources,
        )

    @classmethod
    def create_branch(
        cls, source: str, target: str, branch_name: str, condition: str
    ) -> "EdgeModel":
        """Create a branch edge."""
        return cls(
            name=f"{source}_branch_{branch_name}_{condition}_to_{target}",
            source=source,
            target=target,
            edge_type=EdgeType.BRANCH,
            branch_name=branch_name,
            condition=condition,
        )

    @classmethod
    def create_branch_then(
        cls, source: str, target: str, branch_name: str
    ) -> "EdgeModel":
        """Create a branch then edge."""
        return cls(
            name=f"{source}_branch_{branch_name}_then_to_{target}",
            source=source,
            target=target,
            edge_type=EdgeType.BRANCH_THEN,
            branch_name=branch_name,
        )
