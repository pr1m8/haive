from typing import Any, ClassVar, Dict, Generic, List, Optional, TypeVar

from pydantic import Field, field_validator

from haive.core.graph.state_graph.base import SerializableModel
from haive.core.graph.state_graph.models.function_ref import FunctionReference
from haive.core.graph.state_graph.models.type_ref import TypeReference

TSpec = TypeVar("TSpec", bound=Any)


class NodeModel(SerializableModel, Generic[TSpec]):
    """Serializable representation of a graph node."""

    runnable: FunctionReference | None = Field(
        default=None, description="Function reference for this node"
    )
    input_type: TypeReference | None = Field(
        default=None, description="Input type for this node"
    )
    retry_policy: dict[str, Any] | None = Field(
        default=None, description="Retry configuration"
    )
    spec: TSpec | None = Field(
        default=None, description="Original specification object", exclude=True
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )
    tags: list[str] = Field(default_factory=list, description="Tags for categorization")

    # Class variables
    RESERVED_NAMES: ClassVar[list[str]] = ["__start__", "__end__"]
    __model_type__: ClassVar[str] = "node"
    __abstract__ = False

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate node name."""
        if not v:
            raise ValueError("Node name cannot be empty")

        if v in cls.RESERVED_NAMES:
            raise ValueError(f"'{v}' is a reserved node name")

        if ":" in v:
            raise ValueError("Node names cannot contain ':'")

        return v

    @classmethod
    def from_node_spec(cls, name: str, node_spec: Any) -> Optional["NodeModel"]:
        """Create a NodeModel from a node specification."""
        if node_spec is None:
            return None

        node = cls(name=name)

        # Handle runnable
        if hasattr(node_spec, "runnable"):
            node.runnable = FunctionReference.from_callable(
                node_spec.runnable, name=name
            )

        # Handle metadata
        if hasattr(node_spec, "metadata") and node_spec.metadata:
            node.metadata = dict(node_spec.metadata)

        # Handle input type
        if hasattr(node_spec, "input"):
            node.input_type = TypeReference.from_type(node_spec.input)

        # Handle retry policy
        if hasattr(node_spec, "retry_policy") and node_spec.retry_policy:
            # Simplified - would need more work for full serialization
            if isinstance(node_spec.retry_policy, dict):
                node.retry_policy = dict(node_spec.retry_policy)
            else:
                node.retry_policy = {"exists": True}

        # Store the original spec object
        node.spec = node_spec

        return node
