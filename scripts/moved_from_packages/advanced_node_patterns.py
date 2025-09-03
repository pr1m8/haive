"""Advanced node patterns with extended logic and flexible callables.

This demonstrates:
1. Different callable signatures (typed/untyped)
2. Extended extraction/update logic
3. Command/Send handling
4. Decorator patterns
5. Custom pipelines
"""

from datetime import datetime
from typing import Any

from haive.core.graph.node.composer import FieldMapping
from haive.core.graph.node.composer.advanced_node_composer import (
    AdvancedNodeComposer,
    as_node,
    callable_to_node,
    node_with_custom_logic,
)
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.types import Command, Send
from pydantic import BaseModel, Field


# Example state schemas
class MessagesState(BaseModel):
    """Example state with messages."""

    messages: list[BaseMessage] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    config: dict[str, Any] = Field(default_factory=dict)


class ProcessingState(BaseModel):
    """State for processing workflows."""

    documents: list[dict[str, Any]] = Field(default_factory=list)
    processing_status: str = "pending"
    results: dict[str, Any] = Field(default_factory=dict)


def example_1_different_callable_signatures():
    """Example 1: Handle various callable signatures automatically."""
    composer = AdvancedNodeComposer()

    # 1. Simple function - just state
    def process_simple(state):
        """Simple processor - receives state only."""
        return {"message_count": len(state.messages)}

    # 2. Function with config
    def process_with_config(state, config):
        """Processor that uses config."""
        threshold = config.get("threshold", 5)
        return {"over_threshold": len(state.messages) > threshold}

    # 3. Typed function
    def process_typed(state: MessagesState, config: dict[str, Any]) -> dict[str, Any]:
        """Fully typed processor."""
        return {
            "last_message": state.messages[-1].content if state.messages else None,
            "metadata": state.metadata,
        }

    # 4. Function returning Command
    def process_command(state, config) -> Command:
        """Returns Command directly."""
        if len(state.messages) > 10:
            return Command(update={"should_summarize": True}, goto="summarize")
        return Command(update={"should_summarize": False})

    # 5. No-argument function (uses closure/globals)
    context = {"run_id": "abc123"}

    def process_no_args():
        """Uses external context."""
        return {"run_id": context["run_id"], "timestamp": datetime.now()}

    # Create nodes - all handled automatically!
    simple_node = composer.from_callable_advanced(process_simple)
    config_node = composer.from_callable_advanced(process_with_config)
    typed_node = composer.from_callable_advanced(process_typed)
    command_node = composer.from_callable_advanced(process_command)
    no_args_node = composer.from_callable_advanced(process_no_args)

    return {
        "simple": simple_node,
        "config": config_node,
        "typed": typed_node,
        "command": command_node,
        "no_args": no_args_node,
    }


def example_2_extended_extraction_logic():
    """Example 2: Custom extraction logic beyond simple field mapping."""
    composer = AdvancedNodeComposer()

    # Custom extraction function
    def extract_conversation_context(state, config):
        """Extract rich conversation context."""
        messages = state.messages

        # Extract last N messages based on config
        window_size = config.get("context_window", 5)
        recent_messages = messages[-window_size:] if messages else []

        # Extract speaker patterns
        speakers = {}
        for msg in recent_messages:
            role = "human" if isinstance(msg, HumanMessage) else "assistant"
            speakers[role] = speakers.get(role, 0) + 1

        # Extract topic indicators (simplified)
        all_content = " ".join(msg.content for msg in recent_messages)
        has_question = "?" in all_content

        return {
            "recent_messages": recent_messages,
            "message_count": len(recent_messages),
            "speaker_distribution": speakers,
            "has_question": has_question,
            "total_length": len(all_content),
        }

    # Processing function
    def analyze_conversation(context_data):
        """Analyze the extracted context."""
        if (
            context_data["has_question"]
            and context_data["speaker_distribution"].get("human", 0) > 0
        ):
            return {
                "needs_response": True,
                "priority": "high" if context_data["message_count"] < 3 else "normal",
            }
        return {"needs_response": False, "priority": "low"}

    # Custom update function
    def update_conversation_state(result, state, config):
        """Update state with analysis results."""
        updates = {
            "metadata": {
                **state.metadata,
                "last_analysis": {
                    "timestamp": datetime.now().isoformat(),
                    "needs_response": result["needs_response"],
                    "priority": result["priority"],
                },
            }
        }

        # Add suggested action
        if result["needs_response"]:
            updates["suggested_action"] = "generate_response"

        return updates

    # Create node with custom extract/update logic
    analysis_node = composer.from_callable_advanced(
        func=analyze_conversation,
        extract_logic=extract_conversation_context,
        update_logic=update_conversation_state,
        name="conversation_analyzer",
    )

    return analysis_node


def example_3_typed_callable_with_validation():
    """Example 3: Type-safe nodes with validation."""
    composer = AdvancedNodeComposer()

    # Define result type
    class AnalysisResult(BaseModel):
        summary: str
        word_count: int
        sentiment: str = "neutral"

    # Typed processing function
    def analyze_messages(
        state: MessagesState, config: dict[str, Any]
    ) -> AnalysisResult:
        """Analyze messages with type safety."""
        all_text = " ".join(msg.content for msg in state.messages)

        # Simple analysis
        word_count = len(all_text.split())

        # Mock sentiment
        if "happy" in all_text.lower() or "great" in all_text.lower():
            sentiment = "positive"
        elif "sad" in all_text.lower() or "bad" in all_text.lower():
            sentiment = "negative"
        else:
            sentiment = "neutral"

        return AnalysisResult(
            summary=f"Analyzed {len(state.messages)} messages",
            word_count=word_count,
            sentiment=sentiment,
        )

    # Create typed node with validation
    typed_node = composer.create_typed_callable_node(
        func=analyze_messages,
        state_type=MessagesState,
        config_type=dict[str, Any],
        result_type=AnalysisResult,
        output_mappings=[
            FieldMapping("summary", "analysis_summary"),
            FieldMapping("sentiment", "detected_sentiment"),
            FieldMapping("word_count", "total_words"),
        ],
        validate_types=True,
    )

    return typed_node


def example_4_decorator_patterns():
    """Example 4: Using decorators for clean node definitions."""

    # Simple decorator usage
    @as_node(output_mappings=[FieldMapping("result", "should_continue")])
    def check_conversation_length(state) -> bool:
        """Check if conversation is too long."""
        return len(state.messages) > 20

    # With input mappings
    @as_node(
        input_mappings=[
            FieldMapping("messages", "conversation"),
            FieldMapping("config.max_length", "threshold", default=10),
        ],
        output_mappings=[
            FieldMapping("over_limit", "should_summarize"),
            FieldMapping("message_count", "current_count"),
        ],
    )
    def check_length_with_threshold(
        conversation: list[BaseMessage], threshold: int
    ) -> dict[str, Any]:
        """Check length against threshold."""
        count = len(conversation)
        return {"over_limit": count > threshold, "message_count": count}

    # Decorator with Command return
    @as_node(handle_command=True)
    def router_node(state) -> Command:
        """Route based on state."""
        if state.get("should_summarize"):
            return Command(goto="summarize")
        if state.get("needs_response"):
            return Command(goto="respond")
        return Command(goto="continue")

    # Quick callable conversion
    def process_documents(docs: list[dict]) -> dict[str, Any]:
        """Process documents."""
        return {
            "processed_count": len(docs),
            "total_size": sum(len(d.get("content", "")) for d in docs),
        }

    # Convert existing function
    doc_processor = callable_to_node(
        process_documents,
        input_mappings=[FieldMapping("documents", "docs")],
        output_mappings=[FieldMapping("processed_count", "num_processed")],
    )

    return {
        "length_checker": check_conversation_length,
        "threshold_checker": check_length_with_threshold,
        "router": router_node,
        "doc_processor": doc_processor,
    }


def example_5_custom_pipeline_nodes():
    """Example 5: Nodes with custom extract/process/update pipelines."""

    # Define pipeline components
    def extract_documents_for_summary(state, config):
        """Extract documents that need summarization."""
        min_length = config.get("min_doc_length", 100)

        # Filter documents by length
        long_docs = [
            doc
            for doc in state.get("documents", [])
            if len(doc.get("content", "")) >= min_length
        ]

        return {
            "docs_to_summarize": long_docs,
            "total_docs": len(state.get("documents", [])),
            "selected_docs": len(long_docs),
        }

    def summarize_documents(extracted_data):
        """Process documents to create summaries."""
        docs = extracted_data["docs_to_summarize"]

        summaries = []
        for doc in docs:
            # Mock summarization
            content = doc.get("content", "")
            summary = {
                "doc_id": doc.get("id", "unknown"),
                "summary": content[:100] + "..." if len(content) > 100 else content,
                "length": len(content),
            }
            summaries.append(summary)

        return {
            "summaries": summaries,
            "summarized_count": len(summaries),
            "skipped_count": extracted_data["total_docs"]
            - extracted_data["selected_docs"],
        }

    def update_with_summaries(result, state, config):
        """Update state with summarization results."""
        return {
            "processing_status": "summarized",
            "results": {
                "summaries": result["summaries"],
                "stats": {
                    "total_processed": result["summarized_count"],
                    "skipped": result["skipped_count"],
                    "timestamp": datetime.now().isoformat(),
                },
            },
        }

    # Create pipeline node
    summarizer_node = node_with_custom_logic(
        name="document_summarizer",
        extract=extract_documents_for_summary,
        process=summarize_documents,
        update=update_with_summaries,
    )

    return summarizer_node


def example_6_command_send_handling():
    """Example 6: Advanced Command and Send handling."""
    composer = AdvancedNodeComposer()

    # Function that returns Send for parallel execution
    def parallel_analyzer(state, config):
        """Analyze in parallel using Send."""
        messages = state.messages

        # Split messages for parallel processing
        mid = len(messages) // 2
        first_half = messages[:mid]
        second_half = messages[mid:]

        # Return Send commands for parallel execution
        return [
            Send("analyze_chunk", {"messages": first_half, "chunk_id": 1}),
            Send("analyze_chunk", {"messages": second_half, "chunk_id": 2}),
        ]

    # Function with conditional Command returns
    def smart_router(state):
        """Smart routing based on complex conditions."""
        metadata = state.get("metadata", {})

        # Complex routing logic
        if metadata.get("priority") == "high":
            return Command(update={"routed_to": "urgent_handler"}, goto="urgent")
        if state.get("message_count", 0) > 50:
            return Command(
                update={"routed_to": "batch_processor"},
                goto=["preprocess", "batch_process"],  # Multiple steps
            )
        # Regular command
        return Command(update={"routed_to": "normal_flow"})

    # Create nodes with automatic Command/Send handling
    parallel_node = composer.from_callable_advanced(
        parallel_analyzer,
        name="parallel_splitter",
        handle_command=False,  # Don't wrap Send
    )

    router_node = composer.from_callable_advanced(
        smart_router,
        name="smart_router",
        handle_command=False,  # Already returns Command
    )

    return {"parallel": parallel_node, "router": router_node}


def example_7_real_world_integration():
    """Example 7: Real-world pattern - RAG with custom logic."""
    composer = AdvancedNodeComposer()

    # Complex extraction for RAG
    def extract_for_retrieval(state, config):
        """Extract and prepare data for retrieval."""
        # Get recent messages for context
        recent = state.messages[-3:] if state.messages else []

        # Extract current query
        last_human = None
        for msg in reversed(state.messages):
            if isinstance(msg, HumanMessage):
                last_human = msg
                break

        if not last_human:
            return None

        # Prepare retrieval context
        context_messages = [m.content for m in recent[:-1]]  # Exclude current

        return {
            "query": last_human.content,
            "context": " ".join(context_messages),
            "metadata": {
                "timestamp": datetime.now(),
                "message_count": len(state.messages),
            },
        }

    # Processing with retrieval simulation
    def retrieve_and_process(extracted):
        """Simulate retrieval and processing."""
        if not extracted:
            return {"error": "No query found"}

        query = extracted["query"]
        context = extracted["context"]

        # Simulate retrieval
        mock_documents = [
            {"content": f"Document about {query[:20]}...", "score": 0.95},
            {"content": f"Related to {query[:15]}...", "score": 0.87},
        ]

        # Process results
        return {
            "retrieved_documents": mock_documents,
            "query_used": query,
            "has_context": bool(context),
            "retrieval_metadata": extracted["metadata"],
        }

    # Smart update based on results
    def update_rag_state(result, state, config):
        """Update state with RAG results."""
        if "error" in result:
            return {"processing_status": "failed", "error": result["error"]}

        updates = {
            "retrieved_documents": result["retrieved_documents"],
            "metadata": {
                **state.metadata,
                "last_retrieval": result["retrieval_metadata"],
                "documents_found": len(result["retrieved_documents"]),
            },
        }

        # Add routing based on results
        if result["retrieved_documents"]:
            updates["next_step"] = "generate_answer"
        else:
            updates["next_step"] = "fallback_response"

        return updates

    # Create RAG node with all custom logic
    rag_node = composer.from_callable_advanced(
        func=retrieve_and_process,
        extract_logic=extract_for_retrieval,
        update_logic=update_rag_state,
        name="rag_retriever",
        handle_command=True,
    )

    # Alternative: Use decorator pattern
    @as_node(extract_logic=extract_for_retrieval, update_logic=update_rag_state)
    def rag_with_decorator(extracted_data):
        """RAG using decorator pattern."""
        return retrieve_and_process(extracted_data)

    return {"rag_node": rag_node, "rag_decorated": rag_with_decorator}


if __name__ == "__main__":
    """Run all examples to demonstrate advanced patterns."""

    nodes = example_1_different_callable_signatures()

    analyzer = example_2_extended_extraction_logic()

    typed = example_3_typed_callable_with_validation()

    decorated = example_4_decorator_patterns()

    pipeline = example_5_custom_pipeline_nodes()

    command_nodes = example_6_command_send_handling()

    rag = example_7_real_world_integration()
