#!/usr/bin/env python3
"""
Haive Schema System Examples

This file demonstrates comprehensive usage of the Haive Schema System,
including state creation, dynamic composition, reducers, and real-world patterns.
"""

import operator
from typing import Any, Dict, List, Optional, Tuple

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from pydantic import Field, validator

from haive.core.schema import (
    FieldDefinition,
    FieldExtractor,
    SchemaComposer,
    SchemaType,
    StateSchema,
    StateSchemaManager,
    create_agent_state,
    create_message_state,
    create_simple_state,
    get_schema_info,
    validate_schema,
)
from haive.core.schema.ui import SchemaUI


def example_basic_state_creation():
    """Example 1: Basic state creation patterns."""
    print("=== Example 1: Basic State Creation ===\n")

    # Method 1: Declarative definition
    class ConversationState(StateSchema):
        """Simple conversation state."""

        messages: List[BaseMessage] = Field(default_factory=list)
        topic: str = Field(default="general chat")
        turn_count: int = Field(default=0)

        __reducer_fields__ = {
            "messages": "add_messages",  # Use built-in reducer
            "turn_count": operator.add,  # Sum turn counts
        }

    # Create and use state
    state = ConversationState(topic="AI Ethics")
    state.add_message(HumanMessage(content="What are the main concerns?"))
    state.add_messages(
        [
            AIMessage(content="The main concerns include..."),
            HumanMessage(content="What about bias?"),
        ]
    )

    print(f"Topic: {state.topic}")
    print(f"Messages: {len(state.messages)}")
    print(f"First message: {state.messages[0].content}")

    # Method 2: Using factory function
    QuickState = create_message_state(
        {"user_id": (str, Field(default="")), "session_id": (str, Field(default=""))}
    )

    quick_state = QuickState(user_id="user123")
    print(f"\nQuick state user: {quick_state.user_id}")


def example_dynamic_composition():
    """Example 2: Dynamic schema composition."""
    print("\n\n=== Example 2: Dynamic Schema Composition ===\n")

    # Create composer
    composer = SchemaComposer(name="DynamicRAGState")

    # Add fields programmatically
    composer.add_field(
        name="query",
        field_type=str,
        default="",
        description="User query",
        input_for=["retriever", "reranker"],
    )

    composer.add_field(
        name="documents",
        field_type=List[Dict[str, Any]],
        default_factory=list,
        description="Retrieved documents",
        output_from=["retriever"],
        input_for=["reranker"],
        reducer=operator.add,  # Accumulate documents
    )

    composer.add_field(
        name="context",
        field_type=List[str],
        default_factory=list,
        description="Reranked context",
        output_from=["reranker"],
        input_for=["generator"],
        shared=True,  # Share with parent graph
    )

    composer.add_field(
        name="response",
        field_type=str,
        default="",
        description="Generated response",
        output_from=["generator"],
    )

    # Configure messages field
    composer.configure_messages_field(
        default_factory=list,
        description="Conversation history",
        shared=True,
        with_reducer=True,
    )

    # Build the schema
    DynamicRAGState = composer.build()

    # Use the dynamic schema
    rag_state = DynamicRAGState(query="What is quantum computing?")
    print(f"Schema name: {DynamicRAGState.__name__}")
    print(f"Fields: {list(DynamicRAGState.model_fields.keys())}")
    print(f"Shared fields: {DynamicRAGState.__shared_fields__}")
    print(f"Reducer fields: {list(DynamicRAGState.__reducer_fields__.keys())}")


def example_reducer_behavior():
    """Example 3: Understanding reducer behavior."""
    print("\n\n=== Example 3: Reducer Behavior ===\n")

    class MetricsState(StateSchema):
        """State with various reducer types."""

        # List concatenation
        events: List[str] = Field(default_factory=list)

        # Number addition
        total_count: int = Field(default=0)

        # Replace (last write wins)
        status: str = Field(default="idle")

        # Custom reducer
        tags: List[str] = Field(default_factory=list)

        # Max value reducer
        high_score: float = Field(default=0.0)

        __reducer_fields__ = {
            "events": operator.add,  # Concatenate lists
            "total_count": operator.add,  # Sum numbers
            "status": lambda old, new: new,  # Replace
            "tags": lambda old, new: list(set(old + new)),  # Unique merge
            "high_score": max,  # Keep maximum
        }

    # Initial state
    state = MetricsState()

    # First update
    update1 = {
        "events": ["started", "processing"],
        "total_count": 5,
        "status": "running",
        "tags": ["urgent", "ml"],
        "high_score": 0.85,
    }
    state.apply_reducers(update1)

    print("After first update:")
    print(f"  Events: {state.events}")
    print(f"  Count: {state.total_count}")
    print(f"  Status: {state.status}")
    print(f"  Tags: {state.tags}")
    print(f"  High score: {state.high_score}")

    # Second update
    update2 = {
        "events": ["completed"],
        "total_count": 3,
        "status": "done",
        "tags": ["ml", "production"],  # ml is duplicate
        "high_score": 0.92,
    }
    state.apply_reducers(update2)

    print("\nAfter second update:")
    print(f"  Events: {state.events}")  # All events
    print(f"  Count: {state.total_count}")  # 5 + 3 = 8
    print(f"  Status: {state.status}")  # Replaced with 'done'
    print(f"  Tags: {state.tags}")  # Unique: urgent, ml, production
    print(f"  High score: {state.high_score}")  # Max: 0.92


def example_parent_child_sharing():
    """Example 4: Parent-child graph state sharing."""
    print("\n\n=== Example 4: Parent-Child State Sharing ===\n")

    # Parent graph state
    class ParentState(StateSchema):
        """Main workflow state."""

        messages: List[BaseMessage] = Field(default_factory=list)
        user_query: str = Field(default="")
        final_answer: str = Field(default="")
        metadata: Dict[str, Any] = Field(default_factory=dict)

        # Only messages and query are shared
        __shared_fields__ = ["messages", "user_query"]

        __reducer_fields__ = {
            "messages": "add_messages",
            "metadata": lambda old, new: {**old, **new},  # Merge dicts
        }

    # Child graph state
    class ResearchState(StateSchema):
        """Research subgraph state."""

        # Shared from parent
        messages: List[BaseMessage] = Field(default_factory=list)
        user_query: str = Field(default="")

        # Local to child
        search_results: List[Dict[str, str]] = Field(default_factory=list)
        research_summary: str = Field(default="")

        __shared_fields__ = ["messages", "user_query"]  # Must match parent
        __reducer_fields__ = {
            "messages": "add_messages",
            "search_results": operator.add,
        }

    # Simulate parent state
    parent = ParentState(user_query="Explain quantum entanglement")
    parent.add_message(HumanMessage(content="Explain quantum entanglement"))

    # Child would receive shared fields
    child = ResearchState(
        messages=parent.messages, user_query=parent.user_query  # Shared fields
    )

    # Child does work
    child.search_results = [
        {"title": "Quantum Entanglement Basics", "url": "..."},
        {"title": "EPR Paradox Explained", "url": "..."},
    ]
    child.add_message(AIMessage(content="I found several resources..."))

    # Updates to shared fields would propagate back
    print("Parent query:", parent.user_query)
    print("Child query:", child.user_query)
    print("Shared messages:", len(child.messages))


def example_engine_io_tracking():
    """Example 5: Engine I/O tracking for complex workflows."""
    print("\n\n=== Example 5: Engine I/O Tracking ===\n")

    class MultiEngineState(StateSchema):
        """State for multi-engine workflow."""

        # Input fields
        raw_text: str = Field(default="")
        language: str = Field(default="en")

        # Intermediate fields
        entities: List[Dict[str, str]] = Field(default_factory=list)
        sentiment: Dict[str, float] = Field(default_factory=dict)
        keywords: List[str] = Field(default_factory=list)

        # Output fields
        summary: str = Field(default="")
        insights: Dict[str, Any] = Field(default_factory=dict)

        __engine_io_mappings__ = {
            "ner_engine": {"inputs": ["raw_text", "language"], "outputs": ["entities"]},
            "sentiment_engine": {
                "inputs": ["raw_text"],
                "outputs": ["sentiment"],
            },
            "keyword_engine": {
                "inputs": ["raw_text", "language"],
                "outputs": ["keywords"],
            },
            "summary_engine": {
                "inputs": ["raw_text", "entities", "keywords"],
                "outputs": ["summary"],
            },
            "insight_engine": {
                "inputs": ["entities", "sentiment", "keywords"],
                "outputs": ["insights"],
            },
        }

    # Create state
    state = MultiEngineState(
        raw_text="Apple announced record profits...", language="en"
    )

    # Prepare input for specific engine
    ner_input = state.prepare_for_engine("ner_engine")
    print("NER engine inputs:", list(ner_input.keys()))

    # Simulate engine outputs
    state.entities = [{"text": "Apple", "type": "ORG"}]
    state.keywords = ["profits", "record", "announcement"]

    # Get inputs for summary engine
    summary_input = state.prepare_for_engine("summary_engine")
    print("Summary engine inputs:", list(summary_input.keys()))

    # Display engine dependencies
    print("\nEngine dependencies:")
    for engine, io in state.__engine_io_mappings__.items():
        print(f"  {engine}:")
        print(f"    Inputs: {io['inputs']}")
        print(f"    Outputs: {io['outputs']}")


def example_validation_and_custom_methods():
    """Example 6: Validation and custom methods."""
    print("\n\n=== Example 6: Validation & Custom Methods ===\n")

    class ValidatedState(StateSchema):
        """State with validation and custom methods."""

        email: str = Field(default="")
        age: int = Field(default=0)
        score: float = Field(default=0.0)
        tags: List[str] = Field(default_factory=list)

        @validator("email")
        def validate_email(cls, v):
            if v and "@" not in v:
                raise ValueError("Invalid email format")
            return v.lower()  # Normalize

        @validator("age")
        def validate_age(cls, v):
            if v < 0:
                raise ValueError("Age cannot be negative")
            if v > 150:
                raise ValueError("Age seems unrealistic")
            return v

        @validator("score")
        def validate_score(cls, v):
            return max(0.0, min(1.0, v))  # Clamp to [0, 1]

        @validator("tags")
        def validate_tags(cls, v):
            # Remove duplicates and empty strings
            return list(set(tag.strip() for tag in v if tag.strip()))

        def get_risk_level(self) -> str:
            """Calculate risk level based on score."""
            if self.score < 0.3:
                return "low"
            elif self.score < 0.7:
                return "medium"
            else:
                return "high"

        def add_tag(self, tag: str) -> None:
            """Add a tag if not already present."""
            tag = tag.strip()
            if tag and tag not in self.tags:
                self.tags.append(tag)

        def to_summary(self) -> Dict[str, Any]:
            """Generate summary of state."""
            return {
                "email": self.email,
                "age_group": "adult" if self.age >= 18 else "minor",
                "risk_level": self.get_risk_level(),
                "tag_count": len(self.tags),
            }

    # Test validation
    try:
        state = ValidatedState(email="invalid-email", age=200)
    except ValueError as e:
        print(f"Validation error: {e}")

    # Create valid state
    state = ValidatedState(email="user@example.com", age=25, score=1.5)  # Score clamped

    # Use custom methods
    state.add_tag("important")
    state.add_tag("urgent")
    state.add_tag("important")  # Duplicate, won't be added

    print(f"Email: {state.email}")
    print(f"Score: {state.score}")  # Clamped to 1.0
    print(f"Risk level: {state.get_risk_level()}")
    print(f"Tags: {state.tags}")
    print(f"Summary: {state.to_summary()}")


def example_schema_merging():
    """Example 7: Merging schemas from multiple sources."""
    print("\n\n=== Example 7: Schema Merging ===\n")

    # Create first schema
    composer1 = SchemaComposer(name="SearchSchema")
    composer1.add_field("query", str, default="")
    composer1.add_field("results", List[Dict[str, Any]], default_factory=list)

    # Create second schema
    composer2 = SchemaComposer(name="AnalysisSchema")
    composer2.add_field("text", str, default="")
    composer2.add_field("analysis", Dict[str, Any], default_factory=dict)

    # Merge schemas
    merged = SchemaComposer.merge(
        composer1, composer2, name="SearchAndAnalyzeState", messages_field=True
    )

    # Build merged schema
    MergedState = merged.build()

    # Check fields
    print("Merged schema fields:")
    for field_name, field_info in MergedState.model_fields.items():
        print(f"  {field_name}: {field_info.annotation}")

    # Use merged state
    state = MergedState(query="AI safety", text="Recent research shows...")
    print(f"\nState query: {state.query}")
    print(f"State text: {state.text}")
    print(f"Has messages: {'messages' in state.model_fields}")


def example_real_world_agent_state():
    """Example 8: Real-world agent state pattern."""
    print("\n\n=== Example 8: Real-World Agent State ===\n")

    # Use factory for common agent pattern
    AgentState = create_agent_state(
        name="SmartAgentState",
        additional_fields={
            "plan": (List[str], Field(default_factory=list)),
            "current_step": (int, Field(default=0)),
            "tools_used": (List[str], Field(default_factory=list)),
            "reasoning": (str, Field(default="")),
        },
        shared_fields=["messages", "context"],
        reducers={
            "plan": operator.add,
            "tools_used": operator.add,
            "current_step": max,  # Keep highest step
        },
    )

    # Create agent state
    state = AgentState()

    # Simulate agent execution
    state.add_message(HumanMessage(content="Research climate change solutions"))
    state.plan = ["Search for recent papers", "Analyze findings", "Generate summary"]
    state.reasoning = "User wants comprehensive climate solutions research"

    # Execute first step
    state.current_step = 1
    state.tools_used.append("search_tool")
    state.context.append("Found 15 relevant papers on renewable energy")

    # Execute second step
    state.apply_reducers(
        {
            "current_step": 2,
            "tools_used": ["analysis_tool"],
            "context": ["Key finding: Solar efficiency increased 40%"],
        }
    )

    print("Agent State Summary:")
    print(f"  Current step: {state.current_step}/{len(state.plan)}")
    print(f"  Tools used: {state.tools_used}")
    print(f"  Context items: {len(state.context)}")
    print(f"  Plan: {state.plan}")


def example_serialization_patterns():
    """Example 9: Serialization and persistence patterns."""
    print("\n\n=== Example 9: Serialization Patterns ===\n")

    class PersistentState(StateSchema):
        """State designed for persistence."""

        session_id: str = Field(default="")
        messages: List[BaseMessage] = Field(default_factory=list)
        metadata: Dict[str, Any] = Field(default_factory=dict)
        created_at: str = Field(default="")

        __reducer_fields__ = {
            "messages": "add_messages",
            "metadata": lambda old, new: {**old, **new},
        }

        class Config:
            # Custom JSON encoders for special types
            json_encoders = {
                BaseMessage: lambda v: {
                    "type": v.__class__.__name__,
                    "content": v.content,
                    "additional_kwargs": v.additional_kwargs,
                }
            }

    # Create state
    import datetime

    state = PersistentState(
        session_id="sess_123",
        created_at=datetime.datetime.now().isoformat(),
        metadata={"user": "alice", "topic": "chatbot"},
    )

    state.add_messages(
        [
            HumanMessage(content="Hello!"),
            AIMessage(content="Hi there! How can I help?"),
        ]
    )

    # Serialize to JSON
    json_data = state.to_json()
    print("Serialized JSON:")
    print(json_data[:200] + "...")  # First 200 chars

    # Serialize to dict
    dict_data = state.to_dict()
    print(f"\nDict keys: {list(dict_data.keys())}")

    # Restore from JSON
    restored = PersistentState.from_json(json_data)
    print(f"\nRestored session: {restored.session_id}")
    print(f"Message count: {len(restored.messages)}")

    # Pretty print for debugging
    print("\nPretty printed state:")
    restored.pretty_print()


def example_schema_visualization():
    """Example 10: Schema visualization and introspection."""
    print("\n\n=== Example 10: Schema Visualization ===\n")

    class ComplexState(StateSchema):
        """Complex state for visualization demo."""

        # Message handling
        messages: List[BaseMessage] = Field(
            default_factory=list, description="Conversation messages"
        )

        # Query processing
        query: str = Field(default="", description="User query")
        query_embedding: Optional[List[float]] = Field(
            default=None, description="Query vector"
        )

        # Results
        results: List[Dict[str, Any]] = Field(
            default_factory=list, description="Search results"
        )
        score: float = Field(default=0.0, description="Relevance score")

        # Metadata
        metadata: Dict[str, Any] = Field(
            default_factory=dict, description="Additional metadata"
        )

        __shared_fields__ = ["messages", "query"]
        __reducer_fields__ = {
            "messages": "add_messages",
            "results": operator.add,
            "score": max,
            "metadata": lambda old, new: {**old, **new},
        }
        __engine_io_mappings__ = {
            "embedder": {"inputs": ["query"], "outputs": ["query_embedding"]},
            "searcher": {
                "inputs": ["query", "query_embedding"],
                "outputs": ["results", "score"],
            },
        }

    # Display schema information
    print("Schema Visualization:")
    SchemaUI.display_schema(ComplexState)

    # Get schema info programmatically
    info = get_schema_info(ComplexState)
    print("\nSchema Info Summary:")
    print(f"  Total fields: {info['total_fields']}")
    print(f"  Required fields: {info['required_fields']}")
    print(f"  Optional fields: {info['optional_fields']}")
    print(f"  Has messages: {info['has_messages']}")
    print(f"  Has reducers: {info['has_reducers']}")

    # Generate code representation
    print("\nGenerated Code:")
    code = ComplexState.to_python_code()
    print(code[:500] + "...")  # First 500 chars

    # Validate schema structure
    is_valid = validate_schema(ComplexState)
    print(f"\nSchema validation: {'✓ Passed' if is_valid else '✗ Failed'}")


def main():
    """Run all examples."""
    examples = [
        example_basic_state_creation,
        example_dynamic_composition,
        example_reducer_behavior,
        example_parent_child_sharing,
        example_engine_io_tracking,
        example_validation_and_custom_methods,
        example_schema_merging,
        example_real_world_agent_state,
        example_serialization_patterns,
        example_schema_visualization,
    ]

    for example in examples:
        example()
        input("\nPress Enter to continue to next example...")


if __name__ == "__main__":
    # Run specific example or all
    import sys

    if len(sys.argv) > 1:
        example_num = int(sys.argv[1]) - 1
        examples = [
            example_basic_state_creation,
            example_dynamic_composition,
            example_reducer_behavior,
            example_parent_child_sharing,
            example_engine_io_tracking,
            example_validation_and_custom_methods,
            example_schema_merging,
            example_real_world_agent_state,
            example_serialization_patterns,
            example_schema_visualization,
        ]
        if 0 <= example_num < len(examples):
            examples[example_num]()
        else:
            print(f"Invalid example number. Choose 1-{len(examples)}")
    else:
        main()
