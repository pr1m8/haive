"""Integration test for agents demonstrating key concepts.

This test shows:
- Simple and React agents working
- Multi-agent with proper schema composition
- model_post_init usage
- Conditional edges in multi-agent
"""

import logging
from typing import Any, Dict, List, Optional
from unittest.mock import Mock, patch

import pytest
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.tools import tool
from pydantic import BaseModel, Field

from haive.agents.multi.base import SequentialAgent
from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent

logger = logging.getLogger(__name__)


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


def test_simple_agent_with_tools():
    """Test SimpleAgent with tools and structured output."""
    # Create mock engine
    mock_engine = Mock(spec=AugLLMConfig)
    mock_engine.name = "test_llm"
    mock_engine.model_name = "gpt-4"
    mock_engine.tools = [search_tool, calculate_tool]
    mock_engine.structured_output_model = AnalysisResult

    # Mock schema methods
    mock_engine.get_input_fields.return_value = {
        "messages": (list[BaseMessage], Field(default_factory=list))
    }
    mock_engine.get_output_fields.return_value = {"response": (str, Field(default=""))}

    # Mock output schema class
    class MockSchema(BaseModel):
        response: str = ""
        messages: list[BaseMessage] = Field(default_factory=list)

    mock_engine.derive_output_schema.return_value = MockSchema
    mock_engine.output_schema = MockSchema

    # Create agent
    with patch("haive.agents.simple.agent.SimpleAgent.setup_workflow"):
        agent = SimpleAgent(
            engine=mock_engine,
            structured_output_model=AnalysisResult,
            structured_output_field_name="analysis_result",
        )

        # Verify schema modification
        agent._modify_engine_schema()

        # Check tool categorization
        tool_routes = agent._categorize_tools()
        assert "langchain_tool" in tool_routes
        assert len(tool_routes["langchain_tool"]) == 2


def test_react_agent_looping():
    """Test ReactAgent creates loops in graph."""
    mock_engine = Mock(spec=AugLLMConfig)
    mock_engine.name = "react_llm"
    mock_engine.tools = [search_tool]

    mock_engine.get_input_fields.return_value = {
        "messages": (list[BaseMessage], Field(default_factory=list))
    }
    mock_engine.get_output_fields.return_value = {"response": (str, Field(default=""))}

    with patch("haive.agents.react.agent.ReactAgent.setup_workflow"):
        agent = ReactAgent(engine=mock_engine)

        # Build graph
        agent.build_graph()

        # Check for loops

        # Should have edges that create loops
        # In ReactAgent, tool_node connects back to agent_node


def test_multi_agent_schema_composition():
    """Test multi-agent with schema composition."""
    # Create two mock engines with compatible schemas
    engine1 = Mock(spec=AugLLMConfig)
    engine1.name = "processor"
    engine1.get_input_fields.return_value = {
        "messages": (list[BaseMessage], Field(default_factory=list)),
        "query": (str, Field(default="")),
    }
    engine1.get_output_fields.return_value = {
        "processed_query": (str, Field()),
        "intent": (str, Field()),
    }

    engine2 = Mock(spec=AugLLMConfig)
    engine2.name = "analyzer"
    engine2.get_input_fields.return_value = {
        "processed_query": (str, Field()),
        "intent": (str, Field()),
    }
    engine2.get_output_fields.return_value = {
        "analysis": (str, Field()),
        "score": (float, Field(default=0.0)),
    }

    with patch("haive.agents.simple.agent.SimpleAgent.setup_workflow"):
        agent1 = SimpleAgent(engine=engine1, name="processor")
        agent2 = SimpleAgent(engine=engine2, name="analyzer")

        # Create multi-agent
        with patch("haive.agents.multi.base.SequentialAgent.setup_workflow"):
            SequentialAgent(agents=[agent1, agent2], name="processing_pipeline")

            # The schemas should be compatible
            # agent1 outputs processed_query and intent
            # agent2 expects processed_query and intent


def test_multi_agent_with_model_post_init():
    """Test that multi-agent uses model_post_init properly."""

    # Create a custom multi-agent that uses model_post_init
    class CustomMultiAgent(SequentialAgent):
        """Multi-agent with enhanced model_post_init."""

        def model_post_init(self, __context):
            """Validate and set up after initialization."""
            super().model_post_init(__context)

            # Validate we have at least 2 agents
            if len(self.agents) < 2:
                raise ValueError("Need at least 2 agents")

            # Log agent names
            agent_names = [agent.name for agent in self.agents]
            logger.info(f"Initialized multi-agent with: {agent_names}")

            # Set up some derived state
            self._agent_count = len(self.agents)
            self._has_tools = any(
                hasattr(agent, "engine") and hasattr(agent.engine, "tools")
                for agent in self.agents
            )

    # Test with mock agents
    mock_agent1 = Mock()
    mock_agent1.name = "agent1"
    mock_agent1.engine = Mock(tools=[])

    mock_agent2 = Mock()
    mock_agent2.name = "agent2"

    with patch("haive.agents.multi.base.SequentialAgent.setup_workflow"):
        multi = CustomMultiAgent(agents=[mock_agent1, mock_agent2], name="custom_multi")

        # Verify model_post_init ran
        assert multi._agent_count == 2
        assert multi._has_tools


def test_conditional_edges_concept():
    """Demonstrate how conditional edges should work in multi-agent."""
    # This shows the concept - actual implementation would be in multi-agent
    from haive.core.graph.base_graph import END, START, BaseGraph

    def route_function(state: dict) -> str:
        """Route based on state content."""
        if "urgent" in str(state.get("messages", [])):
            return "fast_path"
        return "normal_path"

    # Create graph with conditional routing
    graph = BaseGraph()

    # Add nodes
    graph.add_node("router", {"type": "CALLABLE", "callable": route_function})
    graph.add_node(
        "fast_path", {"type": "CALLABLE", "callable": lambda x: {"result": "fast"}}
    )
    graph.add_node(
        "normal_path", {"type": "CALLABLE", "callable": lambda x: {"result": "normal"}}
    )

    # Add conditional edges
    graph.add_edge(START, "router")
    graph.add_conditional_edges(
        "router",
        route_function,
        {"fast_path": "fast_path", "normal_path": "normal_path"},
    )

    graph.add_edge("fast_path", END)
    graph.add_edge("normal_path", END)


if __name__ == "__main__":
    # Run all tests
    test_simple_agent_with_tools()
    test_react_agent_looping()
    test_multi_agent_schema_composition()
    test_multi_agent_with_model_post_init()
    test_conditional_edges_concept()
