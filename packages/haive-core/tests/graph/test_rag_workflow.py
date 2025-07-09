"""
Test implementation of a complex RAG workflow using StateGraph with
validation nodes, engine nodes, and visualization capabilities.

This test demonstrates a real-world Retrieval Augmented Generation (RAG) workflow
with comprehensive validation, engine orchestration, and visualizations.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

import pytest
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.types import Command
from pydantic import BaseModel, Field, validator

from haive.core.engine.base import Engine
from haive.core.graph.node.engine_node import EngineNodeConfig
from haive.core.graph.node.validation_node_config import ValidationNodeConfig
from haive.core.graph.state_graph import END, START, StateGraph
from haive.core.graph.state_graph.visualization import MermaidGenerator
from haive.core.schema.prebuilt.tool_state import ToolState


# Define specialized domain objects and tools for RAG
class Document(BaseModel):
    """Document schema representing a retrieved document."""

    id: str = Field(..., description="Unique identifier for the document")
    content: str = Field(..., description="Document content")
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Document metadata"
    )
    embedding: Optional[List[float]] = Field(
        default=None, description="Vector embedding"
    )
    relevance_score: Optional[float] = Field(
        default=None, description="Relevance score"
    )


class RetrievalResult(BaseModel):
    """Result schema for document retrieval."""

    query: str = Field(..., description="Original or rewritten query")
    documents: List[Document] = Field(
        default_factory=list, description="Retrieved documents"
    )
    total_found: int = Field(..., description="Total number of documents found")
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Retrieval metadata"
    )

    @validator("documents")
    def validate_documents(cls, v):
        """Validate that documents have required fields."""
        if len(v) == 0:
            return v
        for doc in v:
            if not doc.id or not doc.content:
                raise ValueError("Documents must have id and content")
        return v


class GenerationParameters(BaseModel):
    """Parameters for text generation."""

    max_length: int = Field(
        default=1000, description="Maximum length of generated text"
    )
    temperature: float = Field(
        default=0.7, ge=0.0, le=1.0, description="Sampling temperature"
    )
    top_p: float = Field(
        default=0.9, ge=0.0, le=1.0, description="Top-p sampling parameter"
    )
    model: str = Field(default="default", description="Model identifier")


class RAGState(ToolState):
    """State schema for RAG workflow."""

    # RAG-specific fields
    query: Optional[str] = Field(default=None, description="User query")
    rewritten_query: Optional[str] = Field(default=None, description="Rewritten query")
    retrieval_result: Optional[RetrievalResult] = Field(
        default=None, description="Retrieved documents"
    )
    generation_params: Optional[GenerationParameters] = Field(
        default=None, description="Generation parameters"
    )

    # Validation tracking
    query_validated: bool = Field(
        default=False, description="Whether query validation passed"
    )
    retrieval_validated: bool = Field(
        default=False, description="Whether retrieval validation passed"
    )
    params_validated: bool = Field(
        default=False, description="Whether generation params validation passed"
    )
    response_validated: bool = Field(
        default=False, description="Whether response validation passed"
    )

    # Workflow state
    workflow_stage: str = Field(default="init", description="Current workflow stage")
    workflow_complete: bool = Field(
        default=False, description="Whether workflow is complete"
    )
    generated_at: Optional[datetime] = Field(
        default=None, description="Timestamp of generation"
    )

    # Metrics
    processing_time: Dict[str, float] = Field(
        default_factory=dict, description="Processing time by stage"
    )
    token_usage: Dict[str, int] = Field(
        default_factory=dict, description="Token usage by stage"
    )


# Mock engines for testing
class QueryAnalysisEngine(Engine):
    """Engine for analyzing and rewriting queries."""

    def __init__(self, name: str = "query_analysis"):
        self.name = name
        self.id = f"engine_{name}"

    def invoke(
        self, inputs: Any, config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Analyze query and return rewritten version."""
        # Extract query from different input types
        query = inputs
        if isinstance(inputs, dict):
            query = inputs.get("query") or inputs.get("messages", [{}])[-1].get(
                "content", ""
            )

        # Simple mock implementation - prepend "improved: "
        return {
            "rewritten_query": f"improved: {query}",
            "analysis": {
                "entities": ["mock_entity_1", "mock_entity_2"],
                "intent": "information_retrieval",
                "confidence": 0.95,
            },
        }


class DocumentRetrievalEngine(Engine):
    """Engine for retrieving documents."""

    def __init__(self, name: str = "document_retrieval"):
        self.name = name
        self.id = f"engine_{name}"

    def invoke(
        self, inputs: Any, config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Retrieve documents based on query."""
        # Extract query
        query = inputs
        if isinstance(inputs, dict):
            query = inputs.get("rewritten_query") or inputs.get(
                "query", "default query"
            )

        # Mock implementation - generate fake documents
        return {
            "retrieval_result": RetrievalResult(
                query=query,
                documents=[
                    Document(
                        id=f"doc{i}",
                        content=f"This is document {i} relevant to {query}",
                        metadata={"source": f"source{i}"},
                        relevance_score=0.9 - (i * 0.1),
                    )
                    for i in range(3)
                ],
                total_found=3,
                metadata={"retrieval_model": "mock_bm25"},
            )
        }


class ContentGenerationEngine(Engine):
    """Engine for generating content based on documents."""

    def __init__(self, name: str = "content_generation"):
        self.name = name
        self.id = f"engine_{name}"

    def invoke(
        self, inputs: Any, config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate content based on documents and query."""
        if isinstance(inputs, dict):
            query = inputs.get("query", "")
            rewritten_query = inputs.get("rewritten_query", query)
            retrieval_result = inputs.get("retrieval_result", None)
            inputs.get("generation_params", {})
        else:
            query = "default query"
            rewritten_query = query
            retrieval_result = None

        # Extract documents if available
        docs = []
        if retrieval_result and hasattr(retrieval_result, "documents"):
            docs = retrieval_result.documents

        # Mock implementation - generate response based on inputs
        doc_sources = [f"[{d.id}]" for d in docs] if docs else ["[no sources]"]

        # Generate a response message
        return {
            "generated_response": {
                "text": f"Response to '{rewritten_query}' based on {len(docs)} documents: {', '.join(doc_sources)}",
                "sources": [d.id for d in docs] if docs else [],
                "score": 0.85,
            },
            "generated_at": datetime.now(),
            "token_usage": {
                "prompt_tokens": 150,
                "completion_tokens": 50,
                "total_tokens": 200,
            },
        }


# Create test fixtures
@pytest.fixture
def rag_engines():
    """Create RAG workflow engines."""
    return {
        "query_analysis": QueryAnalysisEngine(),
        "retrieval": DocumentRetrievalEngine(),
        "generation": ContentGenerationEngine(),
    }


@pytest.fixture
def rag_workflow(rag_engines):
    """Create a complex RAG workflow with validation and visualization."""
    # Create main graph
    workflow = StateGraph(name="RAGWorkflow", state_schema=RAGState)

    # -- Create the preprocessing subgraph --
    preprocessing = StateGraph(name="QueryPreprocessing")

    # Add nodes to preprocessing
    # Validation for query
    query_validator = ValidationNodeConfig(
        name="query_validator",
        schemas=[
            # Schema for validating query
            type(
                "QuerySchema", (BaseModel,), {"query": (str, Field(..., min_length=3))}
            )
        ],
        messages_field="query",
        validation_status_key="query_validated",
    )

    # Query analysis engine
    query_analyzer = EngineNodeConfig(
        name="query_analyzer",
        engine=rag_engines["query_analysis"],
        input_fields=["query", "messages"],
        output_fields={
            "rewritten_query": "rewritten_query",
            "analysis": "query_analysis",
        },
    )

    # Connect preprocessing nodes
    preprocessing.add_node("validate_query", query_validator)
    preprocessing.add_node("analyze_query", query_analyzer)

    preprocessing.add_edge(START, "validate_query")
    preprocessing.add_conditional_edges(
        "validate_query",
        lambda state: state.get("query_validated", False),
        {True: "analyze_query", False: END},
    )
    preprocessing.add_edge("analyze_query", END)

    # -- Create the retrieval subgraph --
    retrieval = StateGraph(name="DocumentRetrieval")

    # Retrieval engine
    document_retriever = EngineNodeConfig(
        name="document_retriever",
        engine=rag_engines["retrieval"],
        input_fields=["rewritten_query", "query"],
        output_fields={"retrieval_result": "retrieval_result"},
    )

    # Validation for retrieval results
    retrieval_validator = ValidationNodeConfig(
        name="retrieval_validator",
        schemas=[RetrievalResult],
        messages_field="retrieval_result",
        validation_status_key="retrieval_validated",
    )

    # Connect retrieval nodes
    retrieval.add_node("retrieve_documents", document_retriever)
    retrieval.add_node("validate_retrieval", retrieval_validator)

    retrieval.add_edge(START, "retrieve_documents")
    retrieval.add_edge("retrieve_documents", "validate_retrieval")
    retrieval.add_edge("validate_retrieval", END)

    # -- Create the generation subgraph --
    generation = StateGraph(name="ResponseGeneration")

    # Validation for generation parameters
    params_validator = ValidationNodeConfig(
        name="params_validator",
        schemas=[GenerationParameters],
        messages_field="generation_params",
        validation_status_key="params_validated",
    )

    # Generation engine
    content_generator = EngineNodeConfig(
        name="content_generator",
        engine=rag_engines["generation"],
        input_fields=[
            "query",
            "rewritten_query",
            "retrieval_result",
            "generation_params",
        ],
        output_fields={
            "generated_response": "generated_response",
            "generated_at": "generated_at",
            "token_usage": "token_usage",
        },
    )

    # Connect generation nodes
    generation.add_node("validate_params", params_validator)
    generation.add_node("generate_content", content_generator)

    generation.add_edge(START, "validate_params")
    generation.add_conditional_edges(
        "validate_params",
        lambda state: state.get(
            "params_validated", True
        ),  # Default to True if no params
        {True: "generate_content", False: END},
    )
    generation.add_edge("generate_content", END)

    # -- Create response processing --
    def format_final_response(state):
        """Format the final response and update workflow state."""
        # Extract data for response
        query = state.get("query", "")
        response_data = state.get("generated_response", {})
        retrieval_result = state.get("retrieval_result", None)

        # Format as messages
        new_messages = [
            # Add system message
            SystemMessage(content="I am a RAG assistant powered by Haive."),
            # Add user query
            HumanMessage(content=query),
        ]

        # Add response with sources
        response_text = response_data.get("text", "No response generated")
        sources = response_data.get("sources", [])

        # If we have documents, add source information
        source_text = ""
        if retrieval_result and retrieval_result.documents:
            source_text = "\n\nSources:\n"
            for doc_id in sources:
                # Find the document
                for doc in retrieval_result.documents:
                    if doc.id == doc_id:
                        source_text += f"- {doc.id}: {doc.content[:50]}...\n"

        # Add assistant response
        new_messages.append(AIMessage(content=response_text + source_text))

        # Update state
        return Command(
            update={
                "messages": new_messages,
                "workflow_complete": True,
                "workflow_stage": "complete",
                "processing_time": {"total": 1.23},  # Mock processing time
            },
            goto=END,
        )

    # -- Add all components to main workflow --
    workflow.add_node("preprocessing", preprocessing)
    workflow.add_node("retrieval", retrieval)
    workflow.add_node("generation", generation)
    workflow.add_node("format_response", format_final_response)

    # Add error handler
    def handle_error(state):
        """Handle errors in the workflow."""
        # Determine error stage based on validation flags
        error_stage = "unknown"
        error_message = "An error occurred during processing"

        if not state.get("query_validated", False):
            error_stage = "query_validation"
            error_message = "Invalid query format"
        elif not state.get("retrieval_validated", False):
            error_stage = "retrieval"
            error_message = "Document retrieval failed"
        elif not state.get("params_validated", False):
            error_stage = "generation_params"
            error_message = "Invalid generation parameters"

        # Add error message
        return Command(
            update={
                "messages": state.get("messages", [])
                + [SystemMessage(content=f"Error: {error_message}")],
                "workflow_complete": True,
                "workflow_stage": f"error_{error_stage}",
            },
            goto=END,
        )

    workflow.add_node("handle_error", handle_error)

    # Connect main workflow
    workflow.add_edge(START, "preprocessing")

    # Branch after preprocessing based on validation
    workflow.add_conditional_edges(
        "preprocessing",
        lambda state: state.get("query_validated", False),
        {True: "retrieval", False: "handle_error"},
    )

    # Branch after retrieval based on validation
    workflow.add_conditional_edges(
        "retrieval",
        lambda state: state.get("retrieval_validated", False),
        {True: "generation", False: "handle_error"},
    )

    # Connect generation to response formatting
    workflow.add_edge("generation", "format_response")

    return workflow


@pytest.fixture
def sample_query_input():
    """Create a sample query input."""
    return RAGState(
        query="What is the capital of France?",
        messages=[HumanMessage(content="What is the capital of France?")],
        generation_params=GenerationParameters(temperature=0.7, max_length=500),
    )


@pytest.fixture
def invalid_query_input():
    """Create an invalid query input."""
    return RAGState(
        query="",  # Empty query - will fail validation
        messages=[HumanMessage(content="")],
    )


# Tests
def test_rag_workflow_execution(rag_workflow, sample_query_input):
    """Test end-to-end execution of the RAG workflow."""
    # Run the workflow
    result = rag_workflow.invoke(sample_query_input)

    # Verify workflow completed successfully
    assert result["workflow_complete"] is True
    assert result["workflow_stage"] == "complete"

    # Verify all stages executed
    assert "rewritten_query" in result
    assert "retrieval_result" in result
    assert "generated_response" in result

    # Check that messages were updated
    assert len(result["messages"]) >= 3  # System, Human, and AI messages
    assert any(isinstance(msg, AIMessage) for msg in result["messages"])

    # Check that token usage was tracked
    assert "token_usage" in result
    assert "total_tokens" in result["token_usage"]


def test_rag_workflow_validation_error(rag_workflow, invalid_query_input):
    """Test workflow handling of validation errors."""
    # Run the workflow with invalid input
    result = rag_workflow.invoke(invalid_query_input)

    # Verify workflow completed with error
    assert result["workflow_complete"] is True
    assert "error" in result["workflow_stage"]

    # Check that error message was added
    assert any(
        isinstance(msg, SystemMessage) and "Error" in msg.content
        for msg in result["messages"]
    )

    # Validation should have failed
    assert not result.get("query_validated", False)


def test_rag_workflow_visualization(rag_workflow, tmp_path):
    """Test visualization of the RAG workflow."""
    # Create output directory
    output_dir = tmp_path / "rag_workflow"
    output_dir.mkdir()

    # Generate timestamp for filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Generate visualizations at different depths
    for depth in range(1, 4):
        output_path = output_dir / f"TestRAGWorkflow_{timestamp}_{depth}.png"

        # Generate diagram using the visualize method
        mermaid_code = rag_workflow.visualize(
            include_subgraphs=True,
            max_depth=depth,
            highlight_nodes=[
                "preprocessing",
                "retrieval",
                "generation",
                "format_response",
                "handle_error",
            ],
            theme="default",
            show_node_type=True,
            output_path=str(output_path),
            save_png=True,
            width="100%",
        )

        # Also save the Mermaid code for inspection
        with open(output_dir / f"TestRAGWorkflow_{timestamp}_{depth}.mmd", "w") as f:
            f.write(mermaid_code)

        # Basic validations
        assert "flowchart TD" in mermaid_code
        assert "preprocessing" in mermaid_code
        assert "retrieval" in mermaid_code
        assert "generation" in mermaid_code

        # Check for specific nodes based on depth
        if depth >= 2:
            assert "validate_query" in mermaid_code
            assert "analyze_query" in mermaid_code
            assert "retrieve_documents" in mermaid_code
            assert "validate_retrieval" in mermaid_code

        # Check that the PNG file was created
        assert output_path.exists()


def test_graph_validation_and_cycles():
    """Test graph validation features with the RAG workflow pattern."""
    # Create a graph with a cycle (for testing validation)
    graph = StateGraph(
        name="CyclicRAG",
        state_schema=RAGState,
        allow_cycles=True,  # Explicitly allow cycles
    )

    # Add simple nodes
    graph.add_node("query_analysis", lambda state: {"query_analyzed": True})
    graph.add_node("retrieval", lambda state: {"documents_retrieved": True})
    graph.add_node("generation", lambda state: {"response_generated": True})
    graph.add_node("feedback", lambda state: {"feedback_processed": True})

    # Connect in a workflow with a feedback loop
    graph.add_edge(START, "query_analysis")
    graph.add_edge("query_analysis", "retrieval")
    graph.add_edge("retrieval", "generation")
    graph.add_edge("generation", "feedback")
    graph.add_edge("feedback", "query_analysis")  # Cycle for refinement

    # Add conditional exit
    graph.add_conditional_edges(
        "feedback",
        lambda state: state.get("iteration_count", 0) >= 3,
        {True: END, False: "query_analysis"},
    )

    # Validate the graph
    validation_issues = graph.validate_graph()

    # Should have no issues because cycles are explicitly allowed
    assert len(validation_issues) == 0

    # Create the same graph but with cycles disallowed
    no_cycles_graph = StateGraph(
        name="NoCyclesRAG",
        state_schema=RAGState,
        allow_cycles=False,  # Explicitly disallow cycles
    )

    # Add the same nodes and edges
    no_cycles_graph.add_node("query_analysis", lambda state: {"query_analyzed": True})
    no_cycles_graph.add_node("retrieval", lambda state: {"documents_retrieved": True})
    no_cycles_graph.add_node("generation", lambda state: {"response_generated": True})
    no_cycles_graph.add_node("feedback", lambda state: {"feedback_processed": True})

    no_cycles_graph.add_edge(START, "query_analysis")
    no_cycles_graph.add_edge("query_analysis", "retrieval")
    no_cycles_graph.add_edge("retrieval", "generation")
    no_cycles_graph.add_edge("generation", "feedback")
    no_cycles_graph.add_edge("feedback", "query_analysis")  # Cycle for refinement

    # Validate the graph - should have issues due to cycle
    validation_issues = no_cycles_graph.validate_graph()
    assert len(validation_issues) > 0
    assert any("cycle" in issue.lower() for issue in validation_issues)

    # Visualize both graphs to compare
    cyclic_diagram = MermaidGenerator.generate(
        graph=graph,
        include_subgraphs=True,
        highlight_nodes=["feedback", "query_analysis"],
        max_depth=2,
    )

    no_cycles_diagram = MermaidGenerator.generate(
        graph=no_cycles_graph,
        include_subgraphs=True,
        highlight_nodes=["feedback", "query_analysis"],
        max_depth=2,
    )

    # Both diagrams should show the cycle regardless of validation status
    assert "feedback" in cyclic_diagram
    assert "query_analysis" in cyclic_diagram
    assert "feedback --> query_analysis" in cyclic_diagram

    assert "feedback" in no_cycles_diagram
    assert "query_analysis" in no_cycles_diagram
    assert "feedback --> query_analysis" in no_cycles_diagram
