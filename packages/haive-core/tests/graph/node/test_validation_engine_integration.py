"""Tests for integration between ValidationNodeConfig and EngineNodeConfig
in complex graph scenarios using the StateGraph system.
"""

from typing import Any, Dict, Optional

import pytest
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.types import Command
from pydantic import BaseModel, Field

from haive.core.engine.base import Engine
from haive.core.graph.node.engine_node import EngineNodeConfig
from haive.core.graph.node.validation_node_config import ValidationNodeConfig
from haive.core.graph.state_graph import END, START, StateGraph
from haive.core.schema.prebuilt.tool_state import ToolState


# Define simple tool functions for validation
@tool
def get_weather(location: str, unit: str = "fahrenheit") -> str:
    """Get the current weather in a location."""
    return f"Weather in {location} is sunny and 75 degrees {unit}"


@tool
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression."""
    return f"Result: {eval(expression)}"


# Mock engine for testing
class MockEngine(Engine):
    """Mock engine for testing with different execution modes."""

    def __init__(self, name: str = "mock_engine", mode: str = "normal"):
        self.name = name
        self.id = f"mock_engine_{name}"
        self.mode = mode
        self.call_count = 0

    def invoke(self, inputs: Any, config: dict[str, Any] | None = None) -> Any:
        """Mock invoke method with different behaviors based on mode."""
        self.call_count += 1

        if self.mode == "error":
            raise ValueError("Simulated engine error")

        if self.mode == "transform":
            # Transform input data in some way
            if isinstance(inputs, dict):
                return {k: f"processed_{v}" for k, v in inputs.items()}
            return f"processed_{inputs}"

        if self.mode == "structured":
            # Return structured data
            return {
                "result": "success",
                "data": inputs,
                "metadata": {"engine": self.name},
            }

        # normal mode
        # Simple pass-through
        return inputs


# Define a combined state schema for testing
class WorkflowState(ToolState):
    """Extended ToolState with additional workflow fields."""

    # Workflow state tracking
    validation_complete: bool = Field(default=False)
    processing_complete: bool = Field(default=False)
    current_stage: str = Field(default="init")

    # Engine results
    engine_results: dict[str, Any] = Field(default_factory=dict)

    # Workflow metrics
    processing_time: float = Field(default=0.0)
    error_count: int = Field(default=0)

    # Custom workflow data
    user_profile: dict[str, Any] | None = Field(default=None)
    context_data: dict[str, Any] | None = Field(default=None)


# Create fixtures for testing
@pytest.fixture
def validation_tools():
    """Create validation tools for testing."""
    return [get_weather, calculate]


@pytest.fixture
def mock_engines():
    """Create mock engines with different behaviors."""
    return {
        "normal": MockEngine(name="normal"),
        "transform": MockEngine(name="transform", mode="transform"),
        "structured": MockEngine(name="structured", mode="structured"),
        "error": MockEngine(name="error", mode="error"),
    }


@pytest.fixture
def validation_node_config(validation_tools):
    """Create a ValidationNodeConfig for testing."""
    return ValidationNodeConfig(
        name="validation_node",
        schemas=validation_tools,
        messages_field="messages",
        validation_status_key="validation_complete",
    )


@pytest.fixture
def engine_node_config(mock_engines):
    """Create an EngineNodeConfig for testing."""
    return EngineNodeConfig(
        name="engine_node",
        engine=mock_engines["normal"],
        input_fields=["messages", "context_data"],
        output_fields={"result": "engine_results"},
    )


@pytest.fixture
def complex_state():
    """Create a complex state with tool calls."""
    return WorkflowState(
        messages=[
            HumanMessage(content="What's the weather in Seattle and calculate 2+2"),
            AIMessage(
                content="",
                additional_kwargs={
                    "tool_calls": [
                        {
                            "id": "call_weather",
                            "type": "function",
                            "function": {
                                "name": "get_weather",
                                "arguments": '{"location": "Seattle, WA", "unit": "celsius"}',
                            },
                        },
                        {
                            "id": "call_calc",
                            "type": "function",
                            "function": {
                                "name": "calculate",
                                "arguments": '{"expression": "2+2"}',
                            },
                        },
                    ]
                },
            ),
        ],
        context_data={"user_id": "test123", "session": "abc456"},
    )


@pytest.fixture
def validation_branching_graph(validation_node_config, mock_engines):
    """Create a graph with validation node that branches based on validation result."""
    # Create graph
    graph = StateGraph(name="validation_branching_test", state_schema=WorkflowState)

    # Create nodes
    # Validation node with routing based on validation result
    validation_node = ValidationNodeConfig(
        name="validation_node",
        schemas=[get_weather, calculate],
        messages_field="messages",
        validation_status_key="validation_complete",
    )

    # Engine nodes for different paths
    success_engine = EngineNodeConfig(
        name="success_engine",
        engine=mock_engines["structured"],
        input_fields=["messages", "validated_tool_calls"],
        output_fields={"result": "engine_results"},
        command_goto="final_node",
    )

    failure_engine = EngineNodeConfig(
        name="failure_engine",
        engine=mock_engines["transform"],
        input_fields=["messages", "invalid_tool_calls"],
        output_fields={"result": "engine_results"},
        command_goto="final_node",
    )

    # Final processing node
    def final_node(state):
        return Command(
            update={"current_stage": "complete", "processing_complete": True}, goto=END
        )

    # Add nodes to graph
    graph.add_node("validator", validation_node)
    graph.add_node("success_processor", success_engine)
    graph.add_node("failure_processor", failure_engine)
    graph.add_node("final_node", final_node)

    # Add branching logic
    graph.add_conditional_edges(
        "validator",
        lambda state: state.get("validation_complete", False),
        {True: "success_processor", False: "failure_processor"},
    )

    # Connect START to validator
    graph.add_edge(START, "validator")

    return graph


@pytest.fixture
def complex_engine_chain_graph(mock_engines, validation_tools):
    """Create a graph with a chain of engine nodes and validation."""
    # Create graph
    graph = StateGraph(name="complex_engine_chain", state_schema=WorkflowState)

    # Create specialized engine nodes
    input_processor = EngineNodeConfig(
        name="input_processor",
        engine=mock_engines["transform"],
        input_fields=["messages", "context_data"],
        output_fields={"result": "processed_input"},
        command_goto="validator",
    )

    data_processor = EngineNodeConfig(
        name="data_processor",
        engine=mock_engines["structured"],
        input_fields=["processed_input", "validated_tool_calls"],
        output_fields={"result": "structured_data", "metadata": "metadata"},
        command_goto="output_processor",
    )

    output_processor = EngineNodeConfig(
        name="output_processor",
        engine=mock_engines["normal"],
        input_fields=["structured_data", "metadata"],
        output_fields={"result": "engine_results"},
        command_goto="decision_point",
    )

    # Validation node
    validator = ValidationNodeConfig(
        name="validator",
        schemas=validation_tools,
        messages_field="messages",
        validation_status_key="validation_complete",
    )

    # Decision point function for routing
    def decision_point(state):
        # Route based on presence of error_count
        if state.get("error_count", 0) > 0:
            return Command(goto="error_handler")
        return Command(
            update={"processing_complete": True, "current_stage": "complete"}, goto=END
        )

    # Error handler
    def error_handler(state):
        return Command(
            update={
                "messages": state["messages"]
                + [
                    ToolMessage(
                        content="Error occurred during processing", name="error_handler"
                    )
                ],
                "current_stage": "error",
            },
            goto=END,
        )

    # Add nodes to graph
    graph.add_node("input_processor", input_processor)
    graph.add_node("validator", validator)
    graph.add_node("data_processor", data_processor)
    graph.add_node("output_processor", output_processor)
    graph.add_node("decision_point", decision_point)
    graph.add_node("error_handler", error_handler)

    # Add conditional edges for validation results
    graph.add_conditional_edges(
        "validator",
        lambda state: state.get("validation_complete", False),
        {True: "data_processor", False: "error_handler"},
    )

    # Connect START to input processor
    graph.add_edge(START, "input_processor")

    return graph


@pytest.fixture
def parallel_validation_graph(mock_engines, validation_tools):
    """Create a graph with parallel validation and processing paths."""
    # Create graph
    graph = StateGraph(name="parallel_validation", state_schema=WorkflowState)

    # Tool validation node
    tool_validator = ValidationNodeConfig(
        name="tool_validator",
        schemas=validation_tools,
        messages_field="messages",
        validation_status_key="tools_validated",
    )

    # Input validation node for context data
    class ContextSchema(BaseModel):
        user_id: str
        session: str

    context_validator = ValidationNodeConfig(
        name="context_validator",
        schemas=[ContextSchema],
        messages_field="context_data",
        validation_status_key="context_validated",
    )

    # Processing nodes
    tool_processor = EngineNodeConfig(
        name="tool_processor",
        engine=mock_engines["structured"],
        input_fields=["validated_tool_calls"],
        output_fields={"result": "tool_results"},
    )

    context_processor = EngineNodeConfig(
        name="context_processor",
        engine=mock_engines["transform"],
        input_fields=["context_data"],
        output_fields={"result": "context_results"},
    )

    # Aggregator function
    def results_aggregator(state):
        # Combine results from both processing paths
        tool_results = state.get("tool_results", {})
        context_results = state.get("context_results", {})

        return Command(
            update={
                "engine_results": {"tools": tool_results, "context": context_results},
                "processing_complete": True,
                "current_stage": "complete",
            },
            goto=END,
        )

    # Add nodes
    graph.add_node("tool_validator", tool_validator)
    graph.add_node("context_validator", context_validator)
    graph.add_node("tool_processor", tool_processor)
    graph.add_node("context_processor", context_processor)
    graph.add_node("results_aggregator", results_aggregator)

    # Connect paths
    graph.add_edge(START, "tool_validator")
    graph.add_edge(START, "context_validator")

    # Add conditional branches
    graph.add_conditional_edges(
        "tool_validator",
        lambda state: state.get("tools_validated", False),
        {
            True: "tool_processor",
            False: "results_aggregator",  # Skip processing on failure
        },
    )

    graph.add_conditional_edges(
        "context_validator",
        lambda state: state.get("context_validated", False),
        {
            True: "context_processor",
            False: "results_aggregator",  # Skip processing on failure
        },
    )

    # Connect processors to aggregator
    graph.add_edge("tool_processor", "results_aggregator")
    graph.add_edge("context_processor", "results_aggregator")

    return graph


# Test cases
def test_validation_node_branching(validation_branching_graph, complex_state):
    """Test validation node that branches to different engine nodes based on result."""
    # Run the graph with valid input
    result = validation_branching_graph.invoke(complex_state)

    # Verify that we completed the workflow
    assert result["current_stage"] == "complete"
    assert result["processing_complete"] is True

    # Verify validation completed successfully
    assert result["validation_complete"] is True

    # Verify we took the success path
    assert "engine_results" in result
    assert "data" in result["engine_results"]


def test_validation_branching_with_invalid_input(validation_branching_graph):
    """Test branching with invalid input goes to the failure path."""
    # Create state with invalid tool calls
    invalid_state = WorkflowState(
        messages=[
            HumanMessage(content="What's the weather?"),
            AIMessage(
                content="",
                additional_kwargs={
                    "tool_calls": [
                        {
                            "id": "bad_call",
                            "type": "function",
                            "function": {
                                "name": "get_weather",
                                "arguments": '{"unit": "fahrenheit"}',  # Missing required location
                            },
                        }
                    ]
                },
            ),
        ]
    )

    # Run the graph
    result = validation_branching_graph.invoke(invalid_state)

    # Verify we completed the workflow
    assert result["current_stage"] == "complete"
    assert result["processing_complete"] is True

    # Verify validation failed
    assert result["validation_complete"] is False

    # Verify we took the failure path
    assert "engine_results" in result
    assert result["engine_results"] is not None


def test_complex_engine_chain(complex_engine_chain_graph, complex_state):
    """Test a complex chain of engine nodes with validation in the middle."""
    # Run the graph
    result = complex_engine_chain_graph.invoke(complex_state)

    # Verify workflow completed
    assert result["processing_complete"] is True
    assert result["current_stage"] == "complete"

    # Verify engines were called in sequence
    assert "processed_input" in result
    assert "structured_data" in result
    assert "metadata" in result
    assert "engine_results" in result

    # Verify validation was successful
    assert result["validation_complete"] is True


def test_parallel_validation_paths(parallel_validation_graph, complex_state):
    """Test parallel validation and processing paths."""
    # Run the graph
    result = parallel_validation_graph.invoke(complex_state)

    # Verify workflow completed
    assert result["processing_complete"] is True
    assert result["current_stage"] == "complete"

    # Verify both processors ran
    assert "engine_results" in result
    assert "tools" in result["engine_results"]
    assert "context" in result["engine_results"]


def test_error_handling_with_invalid_context(parallel_validation_graph):
    """Test error handling when context validation fails."""
    # Create state with invalid context
    invalid_context_state = WorkflowState(
        messages=[
            HumanMessage(content="What's the weather in Seattle?"),
            AIMessage(
                content="",
                additional_kwargs={
                    "tool_calls": [
                        {
                            "id": "call_1",
                            "type": "function",
                            "function": {
                                "name": "get_weather",
                                "arguments": '{"location": "Seattle", "unit": "celsius"}',
                            },
                        }
                    ]
                },
            ),
        ],
        context_data={"missing_required_fields": True},  # Invalid context
    )

    # Run the graph
    result = parallel_validation_graph.invoke(invalid_context_state)

    # Verify workflow completed
    assert result["processing_complete"] is True

    # Verify results include tool processing but not context processing
    assert "engine_results" in result
    assert "tools" in result["engine_results"]

    # Context validation should have failed
    assert "context_validated" not in result or not result["context_validated"]


def test_complex_visualization(
    validation_branching_graph, complex_engine_chain_graph, parallel_validation_graph
):
    """Test visualization capabilities with complex graphs."""
    from haive.core.graph.state_graph.visualization import MermaidGenerator

    # Generate diagrams for all test graphs
    branching_diagram = MermaidGenerator.generate(
        graph=validation_branching_graph,
        include_subgraphs=True,
        highlight_nodes=["validator", "success_processor"],
        max_depth=2,
    )

    chain_diagram = MermaidGenerator.generate(
        graph=complex_engine_chain_graph,
        include_subgraphs=True,
        highlight_nodes=["validator", "data_processor"],
        max_depth=2,
    )

    parallel_diagram = MermaidGenerator.generate(
        graph=parallel_validation_graph,
        include_subgraphs=True,
        highlight_nodes=["tool_validator", "context_validator"],
        max_depth=2,
    )

    # Basic assertions to verify diagram generation
    assert "flowchart TD" in branching_diagram
    assert "validator" in branching_diagram

    assert "flowchart TD" in chain_diagram
    assert "validator" in chain_diagram

    assert "flowchart TD" in parallel_diagram
    assert "tool_validator" in parallel_diagram
    assert "context_validator" in parallel_diagram
