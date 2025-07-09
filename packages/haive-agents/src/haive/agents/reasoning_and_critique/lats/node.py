from typing import Any, Optional

from langchain_core.messages import BaseMessage
from pydantic import BaseModel, Field, field_serializer, model_serializer


class Node(BaseModel):
    """Node class for reflection/reflexion trees with proper serialization."""

    messages: list[BaseMessage]
    reflection: dict[str, Any] | None = None
    parent: Optional["Node"] = None
    children: list["Node"] = Field(default_factory=list)
    value: float = 0.0
    visits: int = 0
    depth: int = Field(default=1)

    def __init__(self, **data):
        super().__init__(**data)
        # Set depth based on parent
        if self.parent:
            self.depth = self.parent.depth + 1
        else:
            self.depth = 1

    @field_serializer("parent")
    def serialize_parent(self, parent: Optional["Node"]) -> dict[str, Any] | None:
        """Serialize parent node as ID only to avoid recursion."""
        if parent is None:
            return None
        # Return minimal representation - just enough to identify the node
        return {"id": id(parent), "depth": parent.depth}

    @field_serializer("children")
    def serialize_children(self, children: list["Node"]) -> list[dict[str, Any]]:
        """Serialize children as IDs only to avoid recursion."""
        return [{"id": id(child), "depth": child.depth} for child in children]

    @model_serializer
    def serialize_model(self) -> dict[str, Any]:
        """Custom model serializer to handle recursion."""
        return {
            "messages": self.messages,
            "reflection": self.reflection,
            "parent_id": id(self.parent) if self.parent else None,
            "children_ids": [id(child) for child in self.children],
            "value": self.value,
            "visits": self.visits,
            "depth": self.depth,
        }

    def add_child(self, child: "Node") -> None:
        """Add a child node."""
        self.children.append(child)
        child.parent = self
        child.depth = self.depth + 1

    def get_path(self) -> list["Node"]:
        """Get path from root to this node."""
        path = []
        current = self
        while current:
            path.append(current)
            current = current.parent
        return list(reversed(path))

    def get_trajectory(self, include_reflections: bool = True) -> list[BaseMessage]:
        """Get all messages in the path from root to this node."""
        messages = []
        current = self
        while current:
            if include_reflections and current.reflection:
                # You would need to convert reflection dict to a message here
                reflection_msg = BaseMessage(content=str(current.reflection))
                messages.extend([*current.messages, reflection_msg])
            else:
                messages.extend(current.messages)
            current = current.parent
        return list(reversed(messages))


# NodeManager for keeping track of nodes and rebuilding the tree
class NodeManager:
    """Manages Node objects to rebuild references after serialization/deserialization."""

    def __init__(self):
        self.nodes: dict[int, Node] = {}

    def register(self, node: Node) -> None:
        """Register a node."""
        self.nodes[id(node)] = node

    def get(self, node_id: int) -> Node | None:
        """Get a node by ID."""
        return self.nodes.get(node_id)

    def rebuild_references(self) -> None:
        """Rebuild parent-child references after deserialization."""
        for node in self.nodes.values():
            parent_id = getattr(node, "parent_id", None)
            children_ids = getattr(node, "children_ids", [])

            if parent_id and parent_id in self.nodes:
                node.parent = self.nodes[parent_id]

            node.children = [
                self.nodes[child_id]
                for child_id in children_ids
                if child_id in self.nodes
            ]
