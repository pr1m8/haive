"""Type definitions for the Branch system."""

from enum import Enum
from typing import Any, Dict, Generic, List, Optional, Protocol

from pydantic import BaseModel, Field

# Import common types
from haive.core.graph.common.types import ConfigLike, NodeOutput, StateLike


class ComparisonType(str, Enum):
    """Comparison operations supported by Branch."""

    EQUALS = "=="
    NOT_EQUALS = "!="
    GREATER_THAN = ">"
    LESS_THAN = "<"
    GREATER_EQUALS = ">="
    LESS_EQUALS = "<="
    IN = "in"
    CONTAINS = "contains"
    IS = "is"
    IS_NOT = "is not"
    EXISTS = "exists"
    NOT_EXISTS = "not exists"
    MATCHES = "matches"
    STARTS_WITH = "starts_with"
    ENDS_WITH = "ends_with"
    HAS_LENGTH = "has_length"
    MESSAGE_CONTAINS = "message_contains"


class BranchMode(str, Enum):
    """Branch evaluation modes."""

    DIRECT = "direct"  # Direct key/value comparison
    FUNCTION = "function"  # Uses a function to evaluate
    CHAIN = "chain"  # Chain of branches
    CONDITION = "condition"  # Conditional branch
    SEND_MAPPER = "send_mapper"  # Maps to Send objects
    DYNAMIC = "dynamic"  # Dynamic output based on state


class BranchProtocol(Protocol, Generic[StateLike, ConfigLike]):
    """Protocol for branch callables."""

    def __call__(
        self, state: StateLike, config: ConfigLike | None = None
    ) -> NodeOutput: ...


class BranchResult(BaseModel):
    """Structured result from a branch evaluation."""

    next_node: str | None = None
    send_objects: list[Any] = Field(default_factory=list)  # Use Any instead of Send
    command_object: Any | None = None  # Use Any instead of Command
    output_mapping: dict[str, str] | None = None

    model_config = {"arbitrary_types_allowed": True}

    @property
    def is_send(self) -> bool:
        """Whether the result contains Send objects."""
        from langgraph.types import Send

        return len(self.send_objects) > 0 and all(
            isinstance(obj, Send) for obj in self.send_objects
        )

    @property
    def is_command(self) -> bool:
        """Whether the result contains a Command object."""
        from langgraph.types import Command

        return self.command_object is not None and isinstance(
            self.command_object, Command
        )

    @property
    def has_mapping(self) -> bool:
        """Whether the result contains output mapping."""
        return self.output_mapping is not None
