"""Unified Schema Integration Examples.

This demonstrates the integrated schema architecture with:
- StateSchema for state management
- SchemaComposer for dynamic schema creation
- NodeSchemaComposer for flexible I/O
- IntegratedNodeComposer for unified patterns
"""

from datetime import datetime
from typing import Any, Optional

from haive.core.graph.node.callable_node import CallableNodeConfig
from haive.core.graph.node.composer import FieldMapping, NodeSchemaComposer
from haive.core.graph.node.composer.integrated_node_composer import (
    IntegratedNodeComposer,
    create_schema_aware_node,
    integrate_node_with_schema,
    with_state_schema,
)
from haive.core.schema import StateSchema
from haive.core.schema.schema_composer import SchemaComposer
from langchain_core.messages import BaseMessage, HumanMessage
from pydantic import Field


# Example 1: Schema-First Development
class RAGWorkflowState(StateSchema):
    """Complete RAG workflow state with schema features."""

    # Core fields
    query: str
    documents: list[dict[str, Any]] = Field(default_factory=list)
    context: str | None = None
    response: str | None = None

    # Metadata
    retrieval_metadata: dict[str, Any] = Field(default_factory=dict)
    generation_metadata: dict[str, Any] = Field(default_factory=dict)

    # Schema features
    __shared_fields__ = ["query", "context"]  # Shared with subgraphs
    __reducer_fields__ = {
        # Accumulate docs
        "documents": lambda old, new: (old or []) + (new or []),
        "retrieval_metadata": lambda old, new: {
            **(old or {}),
            **(new or {}),
        },  # Merge metadata
    }

    __engine_io_mappings__ = {
        "retriever": {
            "inputs": ["query"],
            "outputs": ["documents", "retrieval_metadata"],
        },
        "generator": {
            "inputs": ["query", "context"],
            "outputs": ["response", "generation_metadata"],
        },
    }


def example_1_schema_first_development():
    """Example 1: Start with StateSchema, create nodes that work with it."""

    # 1. Define retrieval function
    def retrieve_documents(state: RAGWorkflowState) -> dict[str, Any]:
        """Retrieve documents based on query."""
        # Simulate retrieval
        docs = [
            {"content": f"Document 1 about {state.query}", "score": 0.95},
            {"content": f"Document 2 about {state.query}", "score": 0.87},
        ]
        return {
            "documents": docs,
            "retrieval_metadata": {
                "query_processed": state.query,
                "num_results": len(docs),
                "timestamp": datetime.now().isoformat(),
            },
        }

    # 2. Create schema-aware retriever node
    retriever = create_schema_aware_node(
        func=retrieve_documents, schema=RAGWorkflowState, name="retriever"
    )

    # 3. Define context builder
    @with_state_schema(RAGWorkflowState)
    def build_context(state: RAGWorkflowState) -> dict[str, Any]:
        """Build context from retrieved documents."""
        if not state.documents:
            return {"context": "No documents available"}

        context = "\n".join(
            [
                f"Document {i + 1}: {doc['content']}"
                for i, doc in enumerate(state.documents)
            ]
        )

        return {"context": context}

    # 4. Create generator with existing function
    def generate_response(query: str, context: str) -> dict[str, Any]:
        """Generate response from query and context."""
        return {
            "response": f"Based on the context about '{query}': [Generated response using provided context]",
            "generation_metadata": {
                "context_length": len(context),
                "generated_at": datetime.now().isoformat(),
            },
        }

    # 5. Adapt generator to work with schema
    generator = create_schema_aware_node(
        func=generate_response,
        schema=RAGWorkflowState,
        input_mappings=[
            FieldMapping("query", "query"),
            FieldMapping("context", "context"),
        ],
        name="generator",
    )

    # 6. Test the pipeline
    initial_state = RAGWorkflowState(query="machine learning applications")

    # Execute retrieval
    result1 = retriever(initial_state)
    state1 = initial_state.model_copy(update=result1.update)

    # Execute context building
    result2 = build_context(state1)
    state2 = state1.model_copy(update=result2.update)

    # Execute generation
    result3 = generator(state2)
    final_state = state2.model_copy(update=result3.update)

    return final_state


def example_2_dynamic_schema_composition():
    """Example 2: Build schemas dynamically then create nodes."""
    # 1. Start with SchemaComposer
    composer = SchemaComposer()

    # 2. Add fields from various sources
    composer.add_field("user_id", str, description="User identifier")
    composer.add_field("session_id", str, description="Session identifier")
    composer.add_field("messages", list[BaseMessage], default_factory=list)
    composer.add_field("current_tool", Optional[str], default=None)
    composer.add_field("tool_results", list[dict], default_factory=list)

    # 3. Add engine tracking
    composer.add_engine_input_mapping("chat_llm", "messages")
    composer.add_engine_output_mapping("chat_llm", "messages")
    composer.add_engine_input_mapping("tool_executor", "current_tool")
    composer.add_engine_output_mapping("tool_executor", "tool_results")

    # 4. Build dynamic schema
    ChatSessionState = composer.build_state_schema("ChatSessionState")

    # 5. Create nodes that work with dynamic schema
    integrated_composer = IntegratedNodeComposer()

    def process_user_message(messages: list[BaseMessage]) -> dict[str, Any]:
        """Process user message and determine if tool needed."""
        if not messages:
            return {"current_tool": None}

        last_message = messages[-1]
        content = (
            last_message.content
            if hasattr(last_message, "content")
            else str(last_message)
        )

        # Simple tool detection
        if "calculate" in content.lower() or "math" in content.lower():
            return {"current_tool": "calculator"}
        if "search" in content.lower() or "find" in content.lower():
            return {"current_tool": "search"}
        return {"current_tool": None}

    # 6. Create integrated node
    message_processor = integrated_composer.from_callable_with_schema(
        func=process_user_message,
        input_schema=ChatSessionState,
        input_mappings=[FieldMapping("messages", "messages")],
        output_mappings=[FieldMapping("current_tool", "current_tool")],
    )

    # 7. Test with dynamic schema
    initial_state = ChatSessionState(
        user_id="user123",
        session_id="session456",
        messages=[HumanMessage(content="Can you help me calculate 15 * 23?")],
    )

    result = message_processor(initial_state)
    final_state = initial_state.model_copy(update=result.update)

    return final_state


def example_3_existing_node_integration():
    """Example 3: Integrate existing nodes with schema system."""

    # 1. Define state schema
    class ProcessingState(StateSchema):
        raw_data: list[str] = Field(default_factory=list)
        processed_data: list[str] = Field(default_factory=list)
        processing_stats: dict[str, Any] = Field(default_factory=dict)

        __shared_fields__ = ["processing_stats"]
        __reducer_fields__ = {
            "processed_data": lambda old, new: (old or []) + (new or [])
        }

    # 2. Create existing node (legacy style)
    def legacy_processor(
        state: dict[str, Any], config: dict[str, Any]
    ) -> dict[str, Any]:
        """Legacy processor that expects different field names."""
        items = state.get("items", [])  # Expects 'items' not 'raw_data'

        processed = [item.upper() for item in items]

        return {
            "results": processed,  # Returns 'results' not 'processed_data'
            "count": len(processed),
            "timestamp": datetime.now().isoformat(),
        }

    legacy_node = CallableNodeConfig(
        name="legacy_processor", callable_func=legacy_processor
    )

    # 3. Integrate with schema system
    integrated_node = integrate_node_with_schema(
        node=legacy_node,
        schema=ProcessingState,
        input_mappings=[
            # Map schema field to expected field
            FieldMapping("raw_data", "items")
        ],
        output_mappings=[
            # Map output to schema field
            FieldMapping("results", "processed_data"),
            FieldMapping("count", "processing_stats.count"),
            FieldMapping("timestamp", "processing_stats.timestamp"),
        ],
    )

    # 4. Test integration
    initial_state = ProcessingState(raw_data=["hello", "world", "integration", "test"])

    result = integrated_node(initial_state)
    final_state = initial_state.model_copy(update=result.update)

    return final_state


def example_4_multi_component_pipeline():
    """Example 4: Complex pipeline with multiple composers."""

    # 1. Start with base schema
    class PipelineState(StateSchema):
        input_text: str
        tokens: list[str] = Field(default_factory=list)
        embeddings: list[float] = Field(default_factory=list)
        similarity_scores: list[float] = Field(default_factory=list)
        final_result: str | None = None

        pipeline_metadata: dict[str, Any] = Field(default_factory=dict)

        __shared_fields__ = ["pipeline_metadata"]
        __reducer_fields__ = {
            "pipeline_metadata": lambda old, new: {**(old or {}), **(new or {})}
        }

    # 2. Create components with different I/O requirements

    # Tokenizer - simple function
    def tokenize_text(text: str) -> list[str]:
        return text.lower().split()

    # Embedder - expects different field names
    def create_embeddings(word_list: list[str]) -> dict[str, Any]:
        # Mock embedding creation
        embeddings = [len(word) * 0.1 for word in word_list]  # Simple mock
        return {"vectors": embeddings, "metadata": {"vocab_size": len(word_list)}}

    # Similarity calculator - complex logic
    def calculate_similarity(state: PipelineState) -> dict[str, Any]:
        if not state.embeddings:
            return {"similarity_scores": [], "final_result": "No embeddings available"}

        # Mock similarity calculation
        target_embedding = [0.3, 0.5, 0.7]  # Mock target
        scores = []

        for i in range(0, len(state.embeddings), 3):
            chunk = state.embeddings[i : i + 3]
            if len(chunk) == 3:
                score = sum(
                    a * b for a, b in zip(chunk, target_embedding, strict=False)
                )
                scores.append(score)

        best_score = max(scores) if scores else 0
        result = "High similarity" if best_score > 0.5 else "Low similarity"

        return {
            "similarity_scores": scores,
            "final_result": result,
            "pipeline_metadata": {
                "best_score": best_score,
                "num_comparisons": len(scores),
            },
        }

    # 3. Create integrated pipeline
    integrated_composer = IntegratedNodeComposer()

    # Tokenizer node
    tokenizer = integrated_composer.from_callable_with_schema(
        func=tokenize_text,
        input_schema=PipelineState,
        input_mappings=[FieldMapping("input_text", "text")],
        output_mappings=[FieldMapping("result", "tokens")],
    )

    # Embedder node (adapt field names)
    embedder = integrated_composer.from_callable_with_schema(
        func=create_embeddings,
        input_schema=PipelineState,
        input_mappings=[FieldMapping("tokens", "word_list")],
        output_mappings=[
            FieldMapping("vectors", "embeddings"),
            FieldMapping("metadata", "pipeline_metadata.embedding_metadata"),
        ],
    )

    # Similarity calculator (schema-aware)
    similarity_calc = create_schema_aware_node(
        func=calculate_similarity, schema=PipelineState, name="similarity_calculator"
    )

    # 4. Execute pipeline
    initial_state = PipelineState(
        input_text="Machine learning is fascinating and complex technology"
    )

    # Step 1: Tokenize
    result1 = tokenizer(initial_state)
    state1 = initial_state.model_copy(update=result1.update)

    # Step 2: Create embeddings
    result2 = embedder(state1)
    state2 = state1.model_copy(update=result2.update)

    # Step 3: Calculate similarity
    result3 = similarity_calc(state2)
    final_state = state2.model_copy(update=result3.update)

    return final_state


def example_5_backwards_compatibility():
    """Example 5: Show backwards compatibility with existing patterns."""

    # 1. Old-style node (still works)
    def old_style_processor(
        state: dict[str, Any], config: dict[str, Any]
    ) -> dict[str, Any]:
        data = state.get("data", [])
        return {"processed": [x.upper() for x in data]}

    old_node = CallableNodeConfig(
        name="old_processor", callable_func=old_style_processor
    )

    # 2. Use old node with new composers
    basic_composer = NodeSchemaComposer()

    # Still works with basic composer
    adapted_old = basic_composer.compose_node(
        base_node=old_node,
        input_mappings=[FieldMapping("items", "data")],
        output_mappings=[FieldMapping("processed", "results")],
    )

    # 3. Can also upgrade to schema-aware
    class CompatState(StateSchema):
        items: list[str] = Field(default_factory=list)
        results: list[str] = Field(default_factory=list)

    schema_aware_old = integrate_node_with_schema(node=adapted_old, schema=CompatState)

    # 4. Test both approaches
    test_state = {"items": ["hello", "world"]}

    # Old way still works
    adapted_old(test_state, {})

    # New way also works
    schema_state = CompatState(items=["hello", "world"])
    result2 = schema_aware_old(schema_state)
    final_state = schema_state.model_copy(update=result2.update)

    return final_state


def example_6_performance_comparison():
    """Example 6: Show performance characteristics."""
    import time

    # 1. Simple function
    def simple_process(data: list[str]) -> list[str]:
        return [x.upper() for x in data]

    # 2. Different node types
    data = ["test"] * 1000

    # Direct function call
    start = time.time()
    for _ in range(100):
        simple_process(data)
    direct_time = time.time() - start

    # Basic composed node
    basic_composer = NodeSchemaComposer()
    basic_node = basic_composer.from_callable(
        func=simple_process,
        input_mappings=[FieldMapping("items", "data")],
        output_mappings=[FieldMapping("result", "processed")],
    )

    start = time.time()
    for _ in range(100):
        basic_node({"items": data}, {})
    basic_time = time.time() - start

    # Schema-aware node
    class PerfState(StateSchema):
        items: list[str] = Field(default_factory=list)
        processed: list[str] = Field(default_factory=list)

    schema_node = create_schema_aware_node(
        func=simple_process,
        schema=PerfState,
        input_mappings=[FieldMapping("items", "data")],
        output_mappings=[FieldMapping("result", "processed")],
    )

    start = time.time()
    for _ in range(100):
        state = PerfState(items=data)
        schema_node(state)
    schema_time = time.time() - start

    return {"direct": direct_time, "basic": basic_time, "schema": schema_time}


if __name__ == "__main__":
    """Run all integration examples."""

    # Run all examples
    result1 = example_1_schema_first_development()
    result2 = example_2_dynamic_schema_composition()
    result3 = example_3_existing_node_integration()
    result4 = example_4_multi_component_pipeline()
    result5 = example_5_backwards_compatibility()
    result6 = example_6_performance_comparison()
