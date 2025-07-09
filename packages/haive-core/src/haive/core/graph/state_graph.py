"""State graph wrapper for LangGraph integration."""

from typing import Any, Type

from pydantic import BaseModel, Field

from haive.core.graph.state_graph.state_graph import StateGraphSerializable


class StateGraph(BaseModel):
    """Wrapper for LangGraph StateGraph with enhanced features.

    This class provides a simplified interface for working with LangGraph
    StateGraphs while maintaining compatibility with the existing infrastructure.
    """

    name: str = Field(default="state_graph", description="Name of the graph")
    state_schema: Type[Any] = Field(default=dict, description="State schema type")

    def __init__(
        self, state_schema: Type[Any] = dict, name: str = "state_graph", **kwargs
    ):
        """Initialize a new state graph."""
        super().__init__(name=name, state_schema=state_schema, **kwargs)
        self._serializable = StateGraphSerializable()

    def add_node(self, node_name: str, node_function: Any) -> "StateGraph":
        """Add a node to the state graph."""
        # This would integrate with the existing StateGraphSerializable
        return self

    def add_edge(self, source: str, target: str) -> "StateGraph":
        """Add an edge to the state graph."""
        # This would integrate with the existing StateGraphSerializable
        return self

    def compile(self) -> Any:
        """Compile the state graph."""
        # This would compile using LangGraph
        return self
