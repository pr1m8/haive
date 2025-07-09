"""Node component implementation for the Haive graph system.

This module defines the Node class which represents a processing unit in a graph.
Nodes are responsible for transforming state and producing outputs that can be used
by subsequent nodes in the graph flow.

Classes:
    Node: Base node class for state processing in a graph

Typical usage:
    ```python
    from haive.core.graph.state_graph.components import Node
    from haive.core.graph.common.types import NodeType

    # Create a simple processing node
    node = Node(
        name="transform_data",
        node_type=NodeType.CALLABLE,
        metadata={"callable": lambda state: {"output": state["input"] * 2}}
    )

    # Process state through the node
    result = node.process({"input": 5})
    assert result["output"] == 10
    ```
"""

import uuid
from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union

from langgraph.types import RetryPolicy
from pydantic import BaseModel, Field

from haive.core.graph.common.types import ConfigLike, NodeOutput, NodeType, StateLike

# Type variables for generic parameters
T = TypeVar("T", bound=StateLike)
C = TypeVar("C", bound=ConfigLike)
O = TypeVar("O", bound=NodeOutput)


class Node(BaseModel, Generic[T, C, O]):
    """Base node in a graph system.

    A node represents a processing unit in a graph that can receive a state,
    optionally a configuration, and produce an output. Nodes are the fundamental
    building blocks for computational graphs in the Haive framework.

    Attributes:
        id: Unique identifier for the node
        name: Human-readable name for the node
        node_type: Type of node (CALLABLE, LLM, TOOL, etc.)
        input_mapping: Optional mapping of input keys
        output_mapping: Optional mapping of output keys
        command_goto: Optional command for routing control
        retry_policy: Optional policy for retrying node execution
        description: Optional human-readable description
        metadata: Additional metadata for the node
        created_at: Creation timestamp

    Example:
        ```python
        node = Node(
            name="process_data",
            node_type=NodeType.CALLABLE,
            description="Processes input data by doubling it",
            metadata={"callable": lambda state: {"output": state["input"] * 2}}
        )
        ```
    """

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    node_type: NodeType

    # Configuration
    input_mapping: Optional[Dict[str, str]] = None
    output_mapping: Optional[Dict[str, str]] = None
    command_goto: Optional[Union[str, List[str]]] = None
    retry_policy: Optional[RetryPolicy] = None

    # Metadata
    description: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)

    model_config = {"arbitrary_types_allowed": True}

    def process(self, state: T, config: Optional[C] = None) -> O:
        """Process state and return output.

        This method processes the input state according to the node's configuration
        and produces an output. Subclasses must implement this method to define
        the specific processing logic.

        Args:
            state: Input state to be processed
            config: Optional configuration parameters for processing

        Returns:
            Process output based on the node's implementation

        Raises:
            NotImplementedError: Subclasses must implement this method
        """
        raise NotImplementedError("Subclasses must implement process method")

    @property
    def display_name(self) -> str:
        """Get a human-readable display name.

        Returns:
            Node display name (defaults to node name)
        """
        return self.name

    def to_dict(self) -> Dict[str, Any]:
        """Convert to serializable dictionary.

        Creates a dictionary representation of the node suitable for serialization.

        Returns:
            Dictionary representation of the node
        """
        return {
            "id": self.id,
            "name": self.name,
            "node_type": self.node_type,
            "input_mapping": self.input_mapping,
            "output_mapping": self.output_mapping,
            "command_goto": self.command_goto,
            "description": self.description,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
