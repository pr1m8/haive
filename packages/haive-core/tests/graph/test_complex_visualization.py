"""
Complex tests integrating the visualization capabilities with validation and engine nodes.

These tests demonstrate the enhanced visualization features in scenarios with complex graph
structures, including subgraphs, validation branching, and engine nodes.
"""

import os
from typing import Any, Dict, List, Optional

import pytest
from langchain_core.tools import tool
from langgraph.types import Command
from pydantic import BaseModel, Field

from haive.core.engine.base import Engine
from haive.core.graph.node.engine_node import EngineNodeConfig
from haive.core.graph.node.validation_node_config import ValidationNodeConfig
from haive.core.graph.state_graph import END, START, StateGraph
from haive.core.graph.state_graph.visualization import MermaidGenerator
from haive.core.schema.prebuilt.tool_state import ToolState


# Define tools for testing
@tool
def get_weather(location: str, unit: str = "fahrenheit") -> str:
    """Get the current weather in a location."""
    return f"Weather in {location} is sunny and 75 degrees {unit}"


@tool
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression."""
    return f"Result: {eval(expression)}"


@tool
def translate(text: str, target_language: str) -> str:
    """Translate text to the target language."""
    return f"Translated to {target_language}: {text} (mock)"


# Mock engine for testing
class MockEngine(Engine):
    """Mock engine for testing visualization."""

    def __init__(self, name: str = "mock_engine", mode: str = "normal"):
        self.name = name
        self.id = f"mock_engine_{name}"
        self.mode = mode

    def invoke(self, inputs: Any, config: Optional[Dict[str, Any]] = None) -> Any:
        """Mock invoke method that returns input."""
        return inputs


# State schema for testing
class ComplexWorkflowState(ToolState):
    """Extended ToolState with additional workflow fields."""

    validation_complete: bool = Field(default=False)
    processing_complete: bool = Field(default=False)
    current_stage: str = Field(default="init")
    engine_results: Dict[str, Any] = Field(default_factory=dict)


# Test fixtures
@pytest.fixture
def mock_engines():
    """Create mock engines with different names."""
    return {
        "llm": MockEngine(name="llm_engine"),
        "embedding": MockEngine(name="embedding_engine"),
        "retrieval": MockEngine(name="retrieval_engine"),
        "processing": MockEngine(name="processing_engine"),
    }


@pytest.fixture
def validation_tools():
    """Create validation tools for testing."""
    return [get_weather, calculate, translate]


@pytest.fixture
def hierarchical_graph(mock_engines, validation_tools):
    """
    Create a complex hierarchical graph with nested subgraphs,
    validation nodes, and engine nodes.
    """
    # Create main graph
    main_graph = StateGraph(name="MainWorkflow", state_schema=ComplexWorkflowState)

    # Create preprocessing subgraph
    preprocessing = StateGraph(name="Preprocessing")

    # Add nodes to preprocessing
    preprocessing.add_node(
        "input_validation",
        ValidationNodeConfig(
            name="input_validator",
            schemas=validation_tools,
            messages_field="messages",
            validation_status_key="input_validated",
        ),
    )

    preprocessing.add_node(
        "input_processor",
        EngineNodeConfig(
            name="input_processor",
            engine=mock_engines["processing"],
            input_fields=["messages", "validated_tool_calls"],
            output_fields={"result": "processed_input"},
        ),
    )

    # Connect preprocessing nodes
    preprocessing.add_edge(START, "input_validation")
    preprocessing.add_conditional_edges(
        "input_validation",
        lambda state: state.get("input_validated", False),
        {True: "input_processor", False: END},
    )
    preprocessing.add_edge("input_processor", END)

    # Create retrieval subgraph
    retrieval = StateGraph(name="Retrieval")

    # Add nodes to retrieval
    retrieval.add_node(
        "embedder",
        EngineNodeConfig(
            name="embedding_engine",
            engine=mock_engines["embedding"],
            input_fields=["processed_input"],
            output_fields={"result": "embeddings"},
        ),
    )

    retrieval.add_node(
        "retriever",
        EngineNodeConfig(
            name="retrieval_engine",
            engine=mock_engines["retrieval"],
            input_fields=["embeddings", "context_data"],
            output_fields={"result": "retrieved_documents"},
        ),
    )

    # Connect retrieval nodes
    retrieval.add_edge(START, "embedder")
    retrieval.add_edge("embedder", "retriever")
    retrieval.add_edge("retriever", END)

    # Create generation subgraph with nested structure
    generation = StateGraph(name="Generation")

    # Create nested prompt construction subgraph
    prompt_construction = StateGraph(name="PromptConstruction")

    # Add nodes to prompt construction
    prompt_construction.add_node(
        "template_selection",
        lambda state: {
            "selected_template": (
                "default" if not state.get("context_data") else "context"
            )
        },
    )

    prompt_construction.add_node(
        "prompt_assembly",
        lambda state: {
            "prompt": f"Generated prompt with {len(state.get('retrieved_documents', []))} documents"
        },
    )

    # Connect prompt construction nodes
    prompt_construction.add_edge(START, "template_selection")
    prompt_construction.add_edge("template_selection", "prompt_assembly")
    prompt_construction.add_edge("prompt_assembly", END)

    # Add nodes to generation
    generation.add_node("prompt_builder", prompt_construction)  # Add subgraph as node

    generation.add_node(
        "generator",
        EngineNodeConfig(
            name="llm_generator",
            engine=mock_engines["llm"],
            input_fields=["prompt", "retrieved_documents"],
            output_fields={"result": "generated_text"},
        ),
    )

    generation.add_node(
        "response_validator",
        ValidationNodeConfig(
            name="response_validator",
            schemas=[
                # Simple schema for validating response
                type(
                    "ResponseSchema",
                    (BaseModel,),
                    {"text": (str, ...), "confidence": (float, Field(gt=0, lt=1))},
                )
            ],
            messages_field="generated_text",
            validation_status_key="response_validated",
        ),
    )

    # Connect generation nodes
    generation.add_edge(START, "prompt_builder")
    generation.add_edge("prompt_builder", "generator")
    generation.add_edge("generator", "response_validator")
    generation.add_edge("response_validator", END)

    # Add subgraphs to main graph
    main_graph.add_node("preprocessing", preprocessing)
    main_graph.add_node("retrieval", retrieval)
    main_graph.add_node("generation", generation)

    # Add final processing node to main graph
    main_graph.add_node(
        "output_processor",
        lambda state: Command(
            update={
                "processing_complete": True,
                "current_stage": "complete",
                "engine_results": {
                    "input": state.get("processed_input", {}),
                    "documents": state.get("retrieved_documents", []),
                    "output": state.get("generated_text", ""),
                },
            },
            goto=END,
        ),
    )

    # Connect main graph
    main_graph.add_edge(START, "preprocessing")
    main_graph.add_edge("preprocessing", "retrieval")
    main_graph.add_edge("retrieval", "generation")
    main_graph.add_edge("generation", "output_processor")

    return main_graph


@pytest.fixture
def complex_branching_graph(mock_engines, validation_tools):
    """
    Create a complex graph with multiple branching paths based on
    validation results and engine outputs.
    """
    # Create main graph
    graph = StateGraph(name="BranchingWorkflow", state_schema=ComplexWorkflowState)

    # Input validation node
    input_validator = ValidationNodeConfig(
        name="input_validator",
        schemas=validation_tools,
        messages_field="messages",
        validation_status_key="input_validated",
    )

    # Processing engines
    text_processor = EngineNodeConfig(
        name="text_processor",
        engine=mock_engines["processing"],
        input_fields=["messages"],
        output_fields={"result": "processed_text"},
    )

    retrieval_engine = EngineNodeConfig(
        name="retrieval",
        engine=mock_engines["retrieval"],
        input_fields=["processed_text"],
        output_fields={"result": "retrieved_documents"},
    )

    llm_engine = EngineNodeConfig(
        name="llm",
        engine=mock_engines["llm"],
        input_fields=["processed_text", "retrieved_documents"],
        output_fields={"result": "generated_response"},
    )

    # Validation for retrieval
    retrieval_validator = ValidationNodeConfig(
        name="retrieval_validator",
        schemas=[
            # Schema for validating retrieval
            type(
                "DocumentSchema",
                (BaseModel,),
                {
                    "documents": (List[Dict[str, Any]], ...),
                    "relevance_scores": (List[float], ...),
                },
            )
        ],
        messages_field="retrieved_documents",
        validation_status_key="retrieval_validated",
    )

    # Response validation
    response_validator = ValidationNodeConfig(
        name="response_validator",
        schemas=[
            # Schema for validating response
            type(
                "ResponseSchema",
                (BaseModel,),
                {"text": (str, ...), "sources": (List[str], ...)},
            )
        ],
        messages_field="generated_response",
        validation_status_key="response_validated",
    )

    # Add routing functions
    def route_on_retrieval(state):
        """Route based on document count in retrieved_documents."""
        docs = state.get("retrieved_documents", {}).get("documents", [])
        if len(docs) > 5:
            return "many_docs"
        elif len(docs) > 0:
            return "few_docs"
        else:
            return "no_docs"

    # Processing for different document counts
    def process_many_docs(state):
        return {
            "current_stage": "processing_many",
            "document_summary": f"Processed {len(state['retrieved_documents']['documents'])} documents",
        }

    def process_few_docs(state):
        return {
            "current_stage": "processing_few",
            "document_summary": f"Processed {len(state['retrieved_documents']['documents'])} documents",
        }

    def process_no_docs(state):
        return {
            "current_stage": "processing_none",
            "document_summary": "No documents to process",
        }

    # Final output assembly
    def assemble_output(state):
        return Command(
            update={
                "processing_complete": True,
                "current_stage": "complete",
                "engine_results": {
                    "summary": state.get("document_summary", "No summary"),
                    "response": state.get("generated_response", {}),
                },
            },
            goto=END,
        )

    # Error handling
    def handle_validation_error(state):
        return Command(
            update={
                "processing_complete": False,
                "current_stage": "validation_error",
                "error_message": "Validation failed",
            },
            goto=END,
        )

    # Add nodes to graph
    graph.add_node("input_validator", input_validator)
    graph.add_node("text_processor", text_processor)
    graph.add_node("retrieval_engine", retrieval_engine)
    graph.add_node("retrieval_validator", retrieval_validator)
    graph.add_node("llm_engine", llm_engine)
    graph.add_node("response_validator", response_validator)

    graph.add_node("process_many_docs", process_many_docs)
    graph.add_node("process_few_docs", process_few_docs)
    graph.add_node("process_no_docs", process_no_docs)

    graph.add_node("assemble_output", assemble_output)
    graph.add_node("handle_error", handle_validation_error)

    # Connect the graph with conditional branching
    graph.add_edge(START, "input_validator")

    # Branch based on input validation
    graph.add_conditional_edges(
        "input_validator",
        lambda state: state.get("input_validated", False),
        {True: "text_processor", False: "handle_error"},
    )

    graph.add_edge("text_processor", "retrieval_engine")
    graph.add_edge("retrieval_engine", "retrieval_validator")

    # Branch based on retrieval validation
    graph.add_conditional_edges(
        "retrieval_validator",
        lambda state: state.get("retrieval_validated", False),
        {True: "llm_engine", False: "handle_error"},
    )

    # Branch based on document count
    graph.add_conditional_edges(
        "retrieval_validator",
        route_on_retrieval,
        {
            "many_docs": "process_many_docs",
            "few_docs": "process_few_docs",
            "no_docs": "process_no_docs",
        },
    )

    graph.add_edge("process_many_docs", "llm_engine")
    graph.add_edge("process_few_docs", "llm_engine")
    graph.add_edge("process_no_docs", "llm_engine")

    graph.add_edge("llm_engine", "response_validator")

    # Branch based on response validation
    graph.add_conditional_edges(
        "response_validator",
        lambda state: state.get("response_validated", False),
        {True: "assemble_output", False: "handle_error"},
    )

    return graph


# Tests
def test_hierarchical_graph_visualization(hierarchical_graph, tmp_path):
    """Test visualization of hierarchical graphs with nested subgraphs."""
    # Create output directory
    output_dir = tmp_path / "hierarchy"
    output_dir.mkdir()

    # Generate visualizations at different depths
    for depth in range(1, 4):
        # Generate diagram
        diagram = MermaidGenerator.generate(
            graph=hierarchical_graph,
            include_subgraphs=True,
            max_depth=depth,
            highlight_nodes=["preprocessing", "retrieval", "generation"],
            theme="default",
            show_node_type=True,
        )

        # Save diagram for inspection
        with open(output_dir / f"depth_{depth}.mmd", "w") as f:
            f.write(diagram)

        # Basic validations
        assert "flowchart TD" in diagram
        assert "preprocessing" in diagram
        assert "retrieval" in diagram
        assert "generation" in diagram

        # Validate subgraph rendering based on depth
        if depth >= 2:
            assert "input_validation" in diagram
            assert "input_processor" in diagram
            assert "embedder" in diagram
            assert "retriever" in diagram

        if depth >= 3:
            assert "prompt_builder" in diagram
            assert "template_selection" in diagram
            assert "prompt_assembly" in diagram


def test_complex_branching_visualization(complex_branching_graph, tmp_path):
    """Test visualization of complex branching logic with validation nodes."""
    # Create output path
    output_path = tmp_path / "branching.mmd"

    # Generate diagram
    diagram = MermaidGenerator.generate(
        graph=complex_branching_graph,
        include_subgraphs=True,
        highlight_nodes=[
            "input_validator",
            "retrieval_validator",
            "response_validator",
        ],
        theme="forest",
        show_node_type=True,
    )

    # Save diagram for inspection
    with open(output_path, "w") as f:
        f.write(diagram)

    # Basic validations
    assert "flowchart TD" in diagram
    assert "input_validator" in diagram
    assert "retrieval_validator" in diagram
    assert "response_validator" in diagram
    assert "process_many_docs" in diagram
    assert "process_few_docs" in diagram
    assert "process_no_docs" in diagram

    # Validate branch visualizations
    assert "many_docs" in diagram
    assert "few_docs" in diagram
    assert "no_docs" in diagram

    # Check for validation branches
    assert "True" in diagram  # For validation conditionals
    assert "False" in diagram  # For validation conditionals


def test_cycle_detection_visualization(mock_engines):
    """Test visualization of a graph with cycles."""
    # Create graph with cycles
    graph = StateGraph(
        name="CycleGraph", state_schema=ComplexWorkflowState, allow_cycles=True
    )

    # Add nodes
    graph.add_node(
        "processor_a",
        EngineNodeConfig(
            name="processor_a",
            engine=mock_engines["processing"],
            input_fields=["messages"],
            output_fields={"result": "result_a"},
        ),
    )

    graph.add_node(
        "processor_b",
        EngineNodeConfig(
            name="processor_b",
            engine=mock_engines["llm"],
            input_fields=["result_a"],
            output_fields={"result": "result_b"},
        ),
    )

    # Create a cycle between nodes
    graph.add_edge(START, "processor_a")
    graph.add_edge("processor_a", "processor_b")
    graph.add_edge("processor_b", "processor_a")  # Creates cycle

    # Add conditional exit from cycle
    graph.add_conditional_edges(
        "processor_b",
        lambda state: len(state.get("messages", [])) > 5,
        {True: END, False: "processor_a"},  # Cycle until messages > 5
    )

    # Generate diagram
    diagram = MermaidGenerator.generate(
        graph=graph,
        include_subgraphs=True,
        highlight_nodes=["processor_a", "processor_b"],
    )

    # Validate cycle is visualized
    assert "processor_a" in diagram
    assert "processor_b" in diagram
    assert "processor_a -->" in diagram
    assert "processor_b -->" in diagram

    # Edge from B back to A should be present (the cycle)
    assert "processor_b --> processor_a" in diagram


def test_deep_nesting_visualization(hierarchical_graph, mock_engines):
    """Test visualization with deep nesting that exceeds max_depth."""
    # Create a graph with very deep nesting
    main_graph = StateGraph(name="DeepNestTest")

    # Create a chain of nested subgraphs
    current_graph = main_graph
    previous_name = "START"

    # Create 5 levels of nesting
    for i in range(5):
        # Create a subgraph for this level
        subgraph = StateGraph(name=f"Level_{i}")

        # Add a node at this level
        node_name = f"node_{i}"
        subgraph.add_node(
            node_name,
            EngineNodeConfig(
                name=node_name,
                engine=mock_engines["processing"],
                input_fields=["data"],
                output_fields={"result": f"result_{i}"},
            ),
        )

        # Connect START to this node and node to END
        subgraph.add_edge(START, node_name)
        subgraph.add_edge(node_name, END)

        # Add this subgraph to the current graph
        current_graph.add_node(f"subgraph_{i}", subgraph)

        # Connect the previous level to this one
        if i == 0:
            current_graph.add_edge(START, f"subgraph_{i}")
        else:
            current_graph.add_edge(previous_name, f"subgraph_{i}")

        previous_name = f"subgraph_{i}"

    # Connect the last subgraph to END
    current_graph.add_edge(previous_name, END)

    # Create visualizations with different max depths
    for depth in range(1, 6):
        diagram = MermaidGenerator.generate(
            graph=main_graph, include_subgraphs=True, max_depth=depth, theme="default"
        )

        # Basic validation
        assert "flowchart TD" in diagram

        # Check that we only see nodes up to max_depth
        for i in range(min(depth, 5)):
            assert f"Level_{i}" in diagram or f"subgraph_{i}" in diagram

        # Nodes beyond max_depth should not be rendered in detail
        if depth < 5:
            for i in range(depth, 5):
                # We might see the node name as an opaque node, but not its internal structure
                assert f"node_{i}" not in diagram


def test_visualize_method_integration(hierarchical_graph, tmp_path):
    """Test the integration of the visualize method on StateGraph."""
    # Create output path
    output_path = str(tmp_path / "direct_visualization.png")

    # Use the visualize method directly on the graph
    mermaid_code = hierarchical_graph.visualize(
        include_subgraphs=True,
        highlight_nodes=["preprocessing", "generation"],
        max_depth=2,
        show_node_type=True,
        theme="forest",
        output_path=output_path,
        save_png=True,
    )

    # Check that the file was created
    assert os.path.exists(output_path)

    # Basic validations of the mermaid code
    assert "flowchart TD" in mermaid_code
    assert "preprocessing" in mermaid_code
    assert "generation" in mermaid_code
