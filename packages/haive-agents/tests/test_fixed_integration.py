"""Fixed integration test with correct imports.

Tests core functionality with proper imports.
"""

from typing import Any, Dict, List
from unittest.mock import MagicMock, Mock, patch

import pytest
from haive.core.engine.aug_llm import AugLLMConfig

# Use base_graph2 as indicated
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.schema.schema_composer import SchemaComposer
from haive.core.schema.state import MessagesState
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.graph import END, START
from pydantic import BaseModel, Field

from haive.agents.multi.base import SequentialAgent
from haive.agents.react.agent import ReactAgent

# Import SimpleAgent from correct location
from haive.agents.simple.agent import SimpleAgent


# Test tools
@tool
def search_tool(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"


@tool
def calculate_tool(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


# Test schema
class AnalysisResult(BaseModel):
    """Analysis output schema."""

    summary: str
    confidence: float = Field(ge=0, le=1, default=0.8)


def test_graph_with_conditional_edges():
    """Test graph creation with conditional edges."""

    def route_by_content(state: Dict) -> str:
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

    print("✅ Conditional edges test passed")
    return True


def test_schema_composition():
    """Test schema composition patterns."""

    # Create composer
    composer = SchemaComposer(name="TestSchema", base_class=MessagesState)

    # Add fields
    composer.add_field("query", str, default="")
    composer.add_field("results", List[str], default_factory=list)
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

    print("✅ Schema composition test passed")
    return True


def test_simple_agent_mock():
    """Test SimpleAgent with mocked engine."""

    # Create mock engine
    mock_engine = Mock(spec=AugLLMConfig)
    mock_engine.name = "test_llm"
    mock_engine.model_name = "gpt-4"
    mock_engine.tools = [search_tool, calculate_tool]
    mock_engine.structured_output_model = AnalysisResult

    # Mock schema methods
    mock_engine.get_input_fields.return_value = {
        "messages": (List[BaseMessage], Field(default_factory=list))
    }
    mock_engine.get_output_fields.return_value = {"response": (str, Field(default=""))}

    # Mock output schema class
    class MockSchema(BaseModel):
        response: str = ""
        messages: List[BaseMessage] = Field(default_factory=list)

    mock_engine.derive_output_schema.return_value = MockSchema
    mock_engine.output_schema = MockSchema

    # Patch the setup method to avoid full initialization
    with patch.object(SimpleAgent, "_setup_persistence", return_value=None):
        with patch.object(SimpleAgent, "_compile_graph", return_value=None):
            with patch.object(SimpleAgent, "_validate_state_schema", return_value=None):
                # Create agent
                agent = SimpleAgent(
                    engine=mock_engine,
                    structured_output_model=AnalysisResult,
                    structured_output_field_name="analysis_result",
                )

                # Test tool categorization
                tool_routes = agent._categorize_tools()
                assert "langchain_tool" in tool_routes
                assert len(tool_routes["langchain_tool"]) == 2

                print("✅ SimpleAgent mock test passed")
                return True


def test_multi_agent_concept():
    """Test multi-agent coordination concept with model_post_init."""

    # Create a custom base model that uses model_post_init
    class ValidatedConfig(BaseModel):
        """Config that validates on initialization."""

        name: str
        min_agents: int = Field(default=2, ge=1)
        agents: List[str] = Field(default_factory=list)

        def model_post_init(self, __context):
            """Validate after initialization."""
            if len(self.agents) < self.min_agents:
                raise ValueError(
                    f"Need at least {self.min_agents} agents, got {len(self.agents)}"
                )

            # Set derived fields
            self.agent_count = len(self.agents)
            self.is_valid = True
            print(f"✓ Validated config with {self.agent_count} agents")

    # Test valid config
    config = ValidatedConfig(name="test_multi", agents=["agent1", "agent2", "agent3"])
    assert config.agent_count == 3
    assert config.is_valid

    # Test invalid config
    try:
        ValidatedConfig(name="bad_multi", min_agents=5, agents=["only_one"])
        assert False, "Should have raised ValueError"
    except ValueError as e:
        print(f"✓ Correctly caught validation error: {e}")

    print("✅ Multi-agent concept test passed")
    return True


def test_conditional_routing_in_graph():
    """Test conditional routing with actual BaseGraph."""

    # Create routing function
    def intent_router(state: Dict) -> str:
        """Route based on detected intent."""
        query = state.get("query", "").lower()

        if "analyze" in query:
            return "analyzer"
        elif "search" in query:
            return "searcher"
        else:
            return "default"

    # Create graph with conditional routing
    graph = BaseGraph()

    # Add router node
    graph.add_node(
        "intent_detector",
        {
            "type": "CALLABLE",
            "callable": intent_router,
            "description": "Detect user intent",
        },
    )

    # Add processing nodes
    graph.add_node(
        "analyzer",
        {
            "type": "CALLABLE",
            "callable": lambda s: {"result": "analysis complete", "path": "analyzer"},
        },
    )

    graph.add_node(
        "searcher",
        {
            "type": "CALLABLE",
            "callable": lambda s: {"result": "search complete", "path": "searcher"},
        },
    )

    graph.add_node(
        "default",
        {
            "type": "CALLABLE",
            "callable": lambda s: {"result": "default processing", "path": "default"},
        },
    )

    # Set up routing
    graph.add_edge(START, "intent_detector")

    # Add conditional edges from router to processors
    graph.add_conditional_edges(
        "intent_detector",
        intent_router,
        {"analyzer": "analyzer", "searcher": "searcher", "default": "default"},
    )

    # All paths lead to END
    graph.add_edge("analyzer", END)
    graph.add_edge("searcher", END)
    graph.add_edge("default", END)

    # Verify graph structure
    assert "intent_detector" in graph.nodes
    assert "analyzer" in graph.nodes
    assert len(graph.branches) > 0

    # Test routing logic
    assert intent_router({"query": "analyze this data"}) == "analyzer"
    assert intent_router({"query": "search for info"}) == "searcher"
    assert intent_router({"query": "hello"}) == "default"

    print("✅ Conditional routing test passed")
    return True


if __name__ == "__main__":
    # Run all tests
    results = []

    print("\n🧪 Running Fixed Integration Tests\n")

    results.append(
        ("Graph with conditional edges", test_graph_with_conditional_edges())
    )
    results.append(("Schema composition", test_schema_composition()))
    results.append(("SimpleAgent mock", test_simple_agent_mock()))
    results.append(("Multi-agent concept", test_multi_agent_concept()))
    results.append(("Conditional routing", test_conditional_routing_in_graph()))

    # Summary
    print("\n📊 Test Results:")
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"  {test_name}: {status}")

    all_passed = all(result[1] for result in results)
    if all_passed:
        print("\n🎉 All tests passed!")
    else:
        print("\n❌ Some tests failed!")
