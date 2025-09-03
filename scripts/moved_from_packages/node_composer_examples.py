"""Examples showing how to use NodeSchemaComposer for flexible node I/O.

This demonstrates solutions to the key problems:
1. Changing output keys (e.g., "documents" → "retrieved_documents")
2. Changing input keys for compatibility
3. Creating nodes from callables with custom field mapping
4. Adapting between different schema types
"""

from typing import Any

from haive.core.engine.retriever import RetrieverEngine
from haive.core.graph.node.composer import (
    FieldMapping,
    NodeSchemaComposer,
    change_output_key,
    remap_fields,
)
from haive.core.graph.node.engine_node import EngineNodeConfig
from langchain_core.messages import BaseMessage


def example_1_change_retriever_output():
    """Example 1: Change retriever output from 'documents' to 'retrieved_documents'."""
    # Create base retriever node (existing pattern)
    retriever_engine = RetrieverEngine(name="my_retriever")
    base_retriever = EngineNodeConfig(name="retriever_node", engine=retriever_engine)

    # SOLUTION: Use NodeSchemaComposer to change output key
    composer = NodeSchemaComposer()

    adapted_retriever = composer.compose_node(
        base_node=base_retriever,
        output_mappings=[FieldMapping("documents", "retrieved_documents")],
    )

    # OR use the quick factory function:
    change_output_key(base_retriever, "documents", "retrieved_documents")

    return adapted_retriever


def example_2_callable_with_field_mapping():
    """Example 2: Create callable node with custom input/output field mapping."""

    def check_message_length(messages: list[BaseMessage], threshold: int = 100) -> bool:
        """Function that checks if total message length exceeds threshold."""
        total_length = sum(len(msg.content) for msg in messages)
        return total_length > threshold

    # SOLUTION: Use composer to create node with field mappings
    composer = NodeSchemaComposer()

    length_checker = composer.from_callable(
        func=check_message_length,
        input_mappings=[
            # Map state.conversation to function parameter 'messages'
            FieldMapping("conversation", "messages"),
            # Map state.config.max_length to function parameter 'threshold'
            FieldMapping("config.max_length", "threshold", default=100),
        ],
        output_mappings=[
            # Map function result to state.should_continue
            FieldMapping("result", "should_continue"),
            # Also store the actual threshold used
            FieldMapping("threshold", "used_threshold"),
        ],
        goto_on_true="summarize",
        goto_on_false="continue",
    )

    return length_checker


def example_3_complex_field_transformations():
    """Example 3: Complex field transformations with custom logic."""

    def process_documents(docs: list[dict], mode: str = "simple") -> dict[str, Any]:
        """Process documents with different modes."""
        if mode == "simple":
            return {"processed": [doc.get("content", "") for doc in docs]}
        return {"processed": docs, "metadata": {"count": len(docs), "mode": mode}}

    # SOLUTION: Advanced field mapping with transforms
    composer = NodeSchemaComposer()

    # Register custom transform
    composer.register_transform_function(
        "filter_empty",
        lambda docs: [doc for doc in docs if doc.get("content", "").strip()],
    )

    processor = composer.from_callable(
        func=process_documents,
        input_mappings=[
            # Extract documents with filtering
            FieldMapping("retrieved_documents", "docs", transform=["filter_empty"]),
            # Extract processing mode from config
            FieldMapping("config.processing.mode", "mode", default="simple"),
        ],
        output_mappings=[
            # Map processed results
            FieldMapping("processed", "final_documents"),
            # Map metadata if available
            FieldMapping("metadata", "processing_info", default={}),
        ],
    )

    return processor


def example_4_adapt_between_node_types():
    """Example 4: Adapt between different node input/output expectations."""
    # Scenario: You have a node that expects "query" but your state has "user_question"
    # AND you want output as "answer" but node produces "response"

    existing_node = EngineNodeConfig(name="llm_node", engine=None)  # Placeholder

    # SOLUTION: Use remap_fields for quick adaptation
    adapted_node = remap_fields(
        node=existing_node,
        input_mapping={
            "user_question": "query",  # state.user_question → node input 'query'
            "context_data": "context",  # state.context_data → node input 'context'
        },
        output_mapping={
            "response": "answer",  # node output 'response' → state.answer
            "metadata": "llm_metadata",  # node output 'metadata' → state.llm_metadata
        },
    )

    return adapted_node


def example_5_schema_composition_for_compatibility():
    """Example 5: Create composed nodes for type compatibility in graphs."""
    composer = NodeSchemaComposer()

    # Create a pipeline of adapted nodes
    def create_rag_pipeline():
        """Create a RAG pipeline with consistent field naming."""
        # 1. Query preparation node
        query_preparer = composer.from_callable(
            func=lambda user_input: f"Search query: {user_input.strip()}",
            input_mappings=[FieldMapping("user_input", "user_input")],
            output_mappings=[FieldMapping("result", "prepared_query")],
        )

        # 2. Retriever node (adapted output)
        retriever = change_output_key(
            EngineNodeConfig(name="retriever", engine=None),  # Placeholder
            "documents",
            "retrieved_docs",
        )

        # 3. Context builder
        context_builder = composer.from_callable(
            func=lambda docs: "\n".join([doc.get("content", "") for doc in docs]),
            input_mappings=[FieldMapping("retrieved_docs", "docs")],
            output_mappings=[FieldMapping("result", "context")],
        )

        # 4. Final answer generator (adapted input/output)
        answer_generator = remap_fields(
            EngineNodeConfig(name="llm", engine=None),  # Placeholder
            input_mapping={"prepared_query": "query", "context": "context"},
            output_mapping={"response": "final_answer"},
        )

        return {
            "prepare": query_preparer,
            "retrieve": retriever,
            "build_context": context_builder,
            "generate": answer_generator,
        }

    pipeline = create_rag_pipeline()
    return pipeline


def example_6_real_world_scenario():
    """Example 6: Real-world scenario - integrating mismatched components."""
    # Scenario: You have:
    # - A retriever that outputs "documents"
    # - An LLM that expects "context" and outputs "response"
    # - Your state schema uses "retrieved_documents" and "ai_answer"

    composer = NodeSchemaComposer()

    # Original components (with mismatched interfaces)
    retriever_node = EngineNodeConfig(
        name="retriever", engine=None
    )  # outputs "documents"
    llm_node = EngineNodeConfig(
        name="llm", engine=None
    )  # expects "context", outputs "response"

    # SOLUTION: Adapt both nodes to work with your state schema

    # 1. Adapt retriever: "documents" → "retrieved_documents"
    adapted_retriever = change_output_key(
        retriever_node, "documents", "retrieved_documents"
    )

    # 2. Adapt LLM: state field → "context", "response" → state field
    adapted_llm = remap_fields(
        llm_node,
        input_mapping={
            "retrieved_documents": "context"  # Use retrieved docs as context
        },
        output_mapping={"response": "ai_answer"},
        # Store response as ai_answer
    )

    # 3. Optional: Add processing between retrieval and generation
    doc_processor = composer.from_callable(
        func=lambda docs: {
            "processed": [doc for doc in docs if len(doc.get("content", "")) > 50]
        },
        input_mappings=[FieldMapping("retrieved_documents", "docs")],
        output_mappings=[
            FieldMapping(
                "processed", "retrieved_documents"
            )  # Replace with filtered docs
        ],
    )

    workflow = {
        "retrieve": adapted_retriever,  # query → retrieved_documents
        "process": doc_processor,  # retrieved_documents → filtered retrieved_documents
        "generate": adapted_llm,  # retrieved_documents → ai_answer
    }

    return workflow


if __name__ == "__main__":
    """Run all examples to demonstrate NodeSchemaComposer capabilities."""

    example_1_change_retriever_output()

    example_2_callable_with_field_mapping()

    example_3_complex_field_transformations()

    example_4_adapt_between_node_types()

    example_5_schema_composition_for_compatibility()

    example_6_real_world_scenario()
