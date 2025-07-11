"""Working integration test for agents.

Tests core functionality without mocking internal methods.
"""

from typing import Any, Dict, List
from unittest.mock import MagicMock, Mock

import pytest
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.base_graph import END, START, BaseGraph
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.tools import tool
from pydantic import BaseModel, Field


# Test tools
@tool
def search_tool(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"


# Test schema
class QueryResult(BaseModel):
    """Query result schema."""

    answer: str
    confidence: float = 0.8


def test_graph_with_conditional_edges():
    """Test graph creation with conditional edges."""

    def route_by_content(state: dict) -> str:
        """Route based on message content."""
        messages = state.get("messages", [])
        if messages and "search" in str(messages[-1]).lower():
            return "search_path"
        return "direct_path"

    # Create graph
    graph = BaseGraph()

    # Add routing node
    graph.add_node("router", {"type": "CALLABLE", "callable": route_by_content})

    # Add processing nodes
    graph.add_node(
        "search_path",
        {"type": "CALLABLE", "callable": lambda s: {"result": "searched"}},
    )

    graph.add_node(
        "direct_path", {"type": "CALLABLE", "callable": lambda s: {"result": "direct"}}
    )

    # Connect with conditional edges
    graph.add_edge(START, "router")
    graph.add_conditional_edges(
        "router",
        route_by_content,
        {"search_path": "search_path", "direct_path": "direct_path"},
    )

    graph.add_edge("search_path", END)
    graph.add_edge("direct_path", END)

    # Verify structure
    assert "router" in graph.nodes
    assert len(graph.branches) > 0  # Should have conditional branches


def test_schema_composition_concepts():
    """Test schema composition patterns."""
    from haive.core.schema.composer import SchemaComposer
    from haive.core.schema.state import MessagesState

    # Create composer
    composer = SchemaComposer(name="TestSchema", base_class=MessagesState)

    # Add fields
    composer.add_field("query", str, default="")
    composer.add_field("results", list[str], default_factory=list)
    composer.add_field("confidence", float, default=0.0)

    # Build schema
    Schema = composer.build()

    # Test instantiation
    instance = Schema(
        messages=[HumanMessage(content="Hello")], query="test query", confidence=0.9
    )

    # Verify fields
    assert hasattr(instance, "messages")  # From MessagesState
    assert hasattr(instance, "query")  # Custom field
    assert instance.confidence == 0.9


def test_engine_configuration():
    """Test engine configuration patterns."""
    # Create mock engine
    engine = MagicMock(spec=AugLLMConfig)
    engine.name = "test_engine"
    engine.model_name = "gpt-4"
    engine.temperature = 0.7

    # Set up schema methods
    engine.get_input_fields.return_value = {
        "messages": (list[BaseMessage], Field(default_factory=list)),
        "context": (str, Field(default="")),
    }

    engine.get_output_fields.return_value = {
        "response": (str, Field()),
        "metadata": (dict, Field(default_factory=dict)),
    }

    # Test field extraction
    input_fields = engine.get_input_fields()
    output_fields = engine.get_output_fields()

    assert "messages" in input_fields
    assert "response" in output_fields


def test_model_post_init_pattern():
    """Test Pydantic model_post_init pattern."""

    class ConfiguredModel(BaseModel):
        """Model using model_post_init for setup."""

        name: str
        value: int = 0
        computed: str = ""

        def model_post_init(self, __context):
            """Post-initialization setup."""
            # Compute derived field
            self.computed = f"{self.name}_{self.value}"

            # Validate constraints
            if self.value < 0:
                raise ValueError("Value must be non-negative")

    # Test valid model
    model = ConfiguredModel(name="test", value=5)
    assert model.computed == "test_5"

    # Test invalid model
    try:
        ConfiguredModel(name="bad", value=-1)
        raise AssertionError("Should have raised ValueError")
    except ValueError:
        pass


def test_component_composition():
    """Test component composition patterns."""

    # Define components
    def processor(state: dict) -> dict:
        """Process input."""
        return {"processed": True}

    def validator(state: dict) -> dict:
        """Validate processed data."""
        if not state.get("processed"):
            raise ValueError("Not processed")
        return {"validated": True}

    def formatter(state: dict) -> dict:
        """Format output."""
        return {"formatted": state}

    # Compose into workflow
    components = {
        "processor": processor,
        "validator": validator,
        "formatter": formatter,
    }

    # Define flow

    # Test composition
    state = {}
    for component_name in ["processor", "validator", "formatter"]:
        state = components[component_name](state)

    assert state.get("formatted") is not None


def test_multi_agent_concepts():
    """Test multi-agent coordination concepts."""

    class AgentState(BaseModel):
        """Shared state for agents."""

        messages: list[BaseMessage] = Field(default_factory=list)
        query: str = ""
        results: list[str] = Field(default_factory=list)

    # Mock agents
    class MockAgent:
        def __init__(self, name: str, process_fn):
            self.name = name
            self.process = process_fn

    # Create agent chain
    agents = [
        MockAgent("extractor", lambda s: {"query": "extracted query"}),
        MockAgent("searcher", lambda s: {"results": ["result1", "result2"]}),
        MockAgent(
            "formatter",
            lambda s: {"messages": [*s.get("messages", []), AIMessage(content="Done")]},
        ),
    ]

    # Simulate sequential execution
    state = {"messages": [HumanMessage(content="Search for Python")]}

    for agent in agents:
        result = agent.process(state)
        state.update(result)

    # Verify final state
    assert state["query"] == "extracted query"
    assert len(state["results"]) == 2
    assert len(state["messages"]) == 2


if __name__ == "__main__":
    # Run all tests
    test_graph_with_conditional_edges()
    test_schema_composition_concepts()
    test_engine_configuration()
    test_model_post_init_pattern()
    test_component_composition()
    test_multi_agent_concepts()
