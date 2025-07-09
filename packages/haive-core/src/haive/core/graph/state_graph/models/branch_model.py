from typing import ClassVar, Dict, Literal, Optional

from pydantic import Field, field_validator, model_validator

from haive.core.graph.state_graph.base import SerializableModel
from haive.core.graph.state_graph.models.function_ref import FunctionReference


class BranchModel(SerializableModel):
    """Serializable representation of a graph branch."""

    source_node: str = Field(..., description="Source node name")
    path: Optional[FunctionReference] = Field(
        default=None, description="Function reference for condition"
    )
    ends: Dict[str, str] = Field(
        default_factory=dict, description="Mapping of condition values to target nodes"
    )
    then: Optional[str] = Field(
        default=None, description="Target node after condition evaluation"
    )
    branch_type: Literal["conditional", "parallel", "switch"] = Field(
        default="conditional", description="Type of branch"
    )

    __model_type__: ClassVar[str] = "branch"
    __abstract__ = False

    @field_validator("branch_type")
    @classmethod
    def validate_branch_type(cls, v: str) -> str:
        """Validate branch type."""
        valid_types = ["conditional", "parallel", "switch"]
        if v not in valid_types:
            raise ValueError(f"Invalid branch type: {v}. Must be one of {valid_types}")
        return v

    @model_validator(mode="after")
    def ensure_valid_branch(self) -> "BranchModel":
        """Ensure the branch specification is valid."""
        # For conditional branches, we need either ends or then
        if self.branch_type == "conditional" and not self.ends and not self.then:
            raise ValueError("Conditional branch must have either 'ends' or 'then'")
        return self

    @classmethod
    def from_branch(
        cls, name: str, source: str, branch: Any
    ) -> Optional["BranchModel"]:
        """Create a BranchModel from a branch object."""
        if branch is None:
            return None

        branch_model = cls(name=name, source_node=source)

        # Handle path (condition function)
        if hasattr(branch, "path"):
            branch_model.path = FunctionReference.from_callable(
                branch.path, name=f"{source}_{name}_condition"
            )

        # Handle ends (routing targets)
        if hasattr(branch, "ends"):
            if isinstance(branch.ends, dict):
                branch_model.ends = dict(branch.ends)  # Make a copy
            elif isinstance(branch.ends, (list, tuple)):
                # Convert list/tuple to dict with index keys
                branch_model.ends = {str(i): v for i, v in enumerate(branch.ends)}
            else:
                branch_model.ends = {"target": str(branch.ends)}

        # Handle then (next node)
        if hasattr(branch, "then"):
            branch_model.then = branch.then

        # Determine branch type
        if hasattr(branch, "type"):
            branch_model.branch_type = branch.type
        elif hasattr(branch, "branch_type"):
            branch_model.branch_type = branch.branch_type

        return branch_model
