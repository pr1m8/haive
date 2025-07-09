"""Basic validation test to see current behavior without checkpointer issues."""

import uuid
from typing import List

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.tools import tool
from pydantic import BaseModel, Field

from haive.agents.simple import SimpleAgent


# Test schemas
class Plan(BaseModel):
    """A plan with steps."""

    steps: List[str] = Field(description="A list of steps to complete the task")


# Test tools
@tool
def add_numbers(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b


def test_simple_agent_creation():
    """Test that we can create simple agents with different configurations."""

    # Test 1: Agent with Pydantic model
    engine1 = AugLLMConfig(
        id=f"engine_{uuid.uuid4().hex[:8]}",
        name="test_pydantic_engine",
        system_message="You are a helpful assistant.",
        structured_output_model=Plan,
    )

    agent1 = SimpleAgent(name="pydantic_agent", engine=engine1)
    assert agent1.name == "pydantic_agent"
    assert "parse_output" in agent1.graph.nodes  # Should have parser node

    # Test 2: Agent with tools
    engine2 = AugLLMConfig(
        id=f"engine_{uuid.uuid4().hex[:8]}",
        name="test_tools_engine",
        system_message="You are a helpful assistant.",
        tools=[add_numbers],
    )

    agent2 = SimpleAgent(name="tools_agent", engine=engine2)
    assert agent2.name == "tools_agent"
    assert "tool_node" in agent2.graph.nodes  # Should have tool node

    # Test 3: Agent with both
    engine3 = AugLLMConfig(
        id=f"engine_{uuid.uuid4().hex[:8]}",
        name="test_mixed_engine",
        system_message="You are a helpful assistant.",
        tools=[add_numbers],
        structured_output_model=Plan,
    )

    agent3 = SimpleAgent(name="mixed_agent", engine=engine3)
    assert agent3.name == "mixed_agent"
    assert "tool_node" in agent3.graph.nodes  # Should have both
    assert "parse_output" in agent3.graph.nodes

    print("✅ All simple agent creation tests passed!")


def test_graph_structure():
    """Test the graph structure of simple agents."""

    # Create agent with tools and Pydantic model
    engine = AugLLMConfig(
        id=f"engine_{uuid.uuid4().hex[:8]}",
        name="test_engine",
        system_message="You are a helpful assistant.",
        tools=[add_numbers],
        structured_output_model=Plan,
    )

    agent = SimpleAgent(name="test_agent", engine=engine)
    graph = agent.graph

    # Check expected nodes exist
    expected_nodes = ["agent_node", "validation", "tool_node", "parse_output"]
    for node in expected_nodes:
        assert node in graph.nodes, f"Missing node: {node}"

    # Check that validation is connected properly
    # In current implementation, validation is used as conditional edge
    print(f"Graph nodes: {list(graph.nodes.keys())}")
    print(f"Graph edges: {graph.edges}")

    print("✅ Graph structure test passed!")


if __name__ == "__main__":
    test_simple_agent_creation()
    test_graph_structure()
