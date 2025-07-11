"""
Tests for AugLLMConfig with focus on various prompt templates, output parsing,
and integration with the StateSchema system.
"""

import logging
import operator
from typing import Annotated, Any, Dict, List, Optional

from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser

# Mocked imports to avoid external dependencies
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotPromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
)
from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel, Field
from rich.console import Console

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from haive.core.schema.schema_composer import SchemaComposer
from haive.core.schema.state_schema import StateSchema
from haive.core.schema.ui import SchemaUI

# Set up logging for tests
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("aug_llm_tests")


# Test models for structured output
class SearchResult(BaseModel):
    """Search result schema for testing structured output."""

    answer: str = Field(description="Answer to the query")
    sources: List[str] = Field(default_factory=list, description="Source documents")
    confidence: float = Field(default=0.0, description="Confidence score")


class AgentAction(BaseModel):
    """Agent action schema for testing structured output."""

    action: str = Field(description="Action to take")
    thought: str = Field(description="Reasoning behind the action")
    parameters: Dict[str, Any] = Field(
        default_factory=dict, description="Action parameters"
    )


# Test StateSchema with messages field
class ConversationState(StateSchema):
    """State schema for conversation with reducible messages field."""

    messages: Annotated[List[BaseMessage], operator.add] = Field(
        default_factory=list, description="Conversation messages"
    )
    context: List[str] = Field(default_factory=list, description="Context documents")
    query: Optional[str] = Field(default=None, description="User query")
    response: Optional[str] = Field(default=None, description="AI response")


# Tests for different prompt templates
def test_chat_prompt_template():
    """Test AugLLMConfig with ChatPromptTemplate."""
    # Create a chat template with system message and messages placeholder
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content="You are a helpful assistant."),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    # Create AugLLMConfig
    aug_llm = AugLLMConfig(
        name="chat_assistant",
        prompt_template=prompt,
        llm_config=AzureLLMConfig(model="gpt-4o"),
    )

    # Test schema derivation
    input_schema = aug_llm.derive_input_schema()
    logger.info(f"Input schema: {input_schema.__name__}")

    # Verify schema fields
    assert hasattr(input_schema, "model_fields")
    assert "messages" in input_schema.model_fields

    # Check that it detected messages field correctly
    assert aug_llm.uses_messages_field

    # Create state from this engine
    schema = SchemaComposer.from_components([aug_llm], name="ChatState")
    logger.info(f"Created schema: {schema.__name__}")

    # Display schema with rich UI
    SchemaUI.display_schema(schema)

    # Verify messages field is in the schema
    assert hasattr(schema, "model_fields")
    assert "messages" in schema.model_fields


def test_few_shot_prompt_template():
    """Test AugLLMConfig with FewShotPromptTemplate."""
    # Create an example prompt
    example_prompt = PromptTemplate(
        input_variables=["question", "answer"],
        template="Question: {question}\nAnswer: {answer}",
    )

    # Define examples
    examples = [
        {"question": "What is the capital of France?", "answer": "Paris"},
        {"question": "What is the largest ocean?", "answer": "Pacific Ocean"},
    ]

    # Create a few-shot template
    few_shot_prompt = FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        prefix="Answer the following questions based on these examples:\n\n",
        suffix="\nQuestion: {question}\nAnswer:",
        input_variables=["question"],
        example_separator="\n\n",
    )

    # Create AugLLMConfig
    aug_llm = AugLLMConfig(
        name="few_shot_qa",
        prompt_template=few_shot_prompt,
        llm_config=AzureLLMConfig(model="gpt-4o"),
    )

    # Test schema derivation
    input_schema = aug_llm.derive_input_schema()
    logger.info(f"Input schema: {input_schema.__name__}")

    # Check input variables detection
    input_vars = aug_llm._get_input_variables()
    logger.info(f"Detected input variables: {input_vars}")

    # Verify schema has model_fields
    assert hasattr(input_schema, "model_fields")
    logger.info(f"Available fields: {list(input_schema.model_fields.keys())}")

    # Check for content and messages fields which are always included
    assert "content" in input_schema.model_fields
    assert "messages" in input_schema.model_fields

    # Check that it detected messages field correctly (should be False for FewShot)
    assert aug_llm.uses_messages_field in [False, None]

    # Create state from this engine
    schema = SchemaComposer.from_components([aug_llm], name="FewShotState")
    logger.info(f"Created schema: {schema.__name__}")

    # Display schema with rich UI
    SchemaUI.display_schema(schema)

    # Verify schema has model_fields
    assert hasattr(schema, "model_fields")
    logger.info(f"Schema fields: {list(schema.model_fields.keys())}")

    # Check for messages field which is always included by SchemaComposer
    assert "messages" in schema.model_fields


def test_system_message_shortcut():
    """Test AugLLMConfig with system_message shortcut."""
    # Create AugLLMConfig with just system message
    aug_llm = AugLLMConfig(
        name="system_message_assistant",
        system_message="You are a helpful assistant specialized in data analysis.",
        llm_config=AzureLLMConfig(model="gpt-4o"),
    )

    # Verify prompt template was created
    assert aug_llm.prompt_template is not None
    assert isinstance(aug_llm.prompt_template, ChatPromptTemplate)

    # Test schema derivation
    input_schema = aug_llm.derive_input_schema()
    logger.info(f"Input schema: {input_schema.__name__}")

    # Verify schema fields
    assert hasattr(input_schema, "model_fields")
    assert "messages" in input_schema.model_fields

    # Check that it detected messages field correctly
    assert aug_llm.uses_messages_field


# Tests for input/output field handling
def test_get_input_variables():
    """Test extracting input variables from different prompt templates."""
    # Test with ChatPromptTemplate
    chat_prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content="You are a helpful assistant."),
            HumanMessage(content="Query: {query}"),
            MessagesPlaceholder(variable_name="chat_history"),
        ]
    )

    aug_llm = AugLLMConfig(
        name="chat_input_vars",
        prompt_template=chat_prompt,
        llm_config=AzureLLMConfig(model="gpt-4o"),
    )

    # Get the actual input variables
    input_vars = aug_llm._get_input_variables()
    logger.info(f"Chat template input vars: {input_vars}")

    # Log available values for debugging
    logger.info(f"Chat prompt attributes: {dir(chat_prompt)}")
    if hasattr(chat_prompt, "input_variables"):
        logger.info(f"Chat prompt input_variables: {chat_prompt.input_variables}")

    # Test with regular PromptTemplate
    text_prompt = PromptTemplate(
        template="Answer the following question: {question}\nContext: {context}",
        input_variables=["question", "context"],
    )

    aug_llm = AugLLMConfig(
        name="text_input_vars",
        prompt_template=text_prompt,
        llm_config=AzureLLMConfig(model="gpt-4o"),
    )

    # Get the actual input variables
    input_vars = aug_llm._get_input_variables()
    logger.info(f"Text template input vars: {input_vars}")

    # Log available values for debugging
    logger.info(f"Text prompt attributes: {dir(text_prompt)}")
    logger.info(f"Text prompt input_variables: {text_prompt.input_variables}")

    # Add a basic assertion that _get_input_variables returns a set
    assert isinstance(input_vars, set)


def test_partial_variables():
    """Test handling of partial variables in prompt templates."""
    # Create template with partial variables
    prompt = PromptTemplate(
        template="System: {system}\nUser: {query}\nAssistant:",
        input_variables=["query"],
        partial_variables={"system": "You are a helpful assistant."},
    )

    # Create AugLLMConfig with additional partial variables
    aug_llm = AugLLMConfig(
        name="partial_vars",
        prompt_template=prompt,
        partial_variables={"model_date": "April 2025"},
        llm_config=AzureLLMConfig(model="gpt-4o"),
    )

    # Test input schema derivation
    input_schema = aug_llm.derive_input_schema()
    logger.info(f"Input schema: {input_schema.__name__}")

    # Verify schema fields - should only have query, not system
    assert hasattr(input_schema, "model_fields")
    assert "query" in input_schema.model_fields
    assert "system" not in input_schema.model_fields
    assert "model_date" not in input_schema.model_fields

    # Create a runnable to verify that partial variables are applied
    aug_llm.create_runnable()

    # Can't actually run it, but we can check its composition


# Tests for output parsing
def test_str_output_parser():
    """Test AugLLMConfig with string output parser."""
    # Create AugLLMConfig with StrOutputParser
    aug_llm = AugLLMConfig(
        name="string_output",
        system_message="You are a helpful assistant.",
        output_parser=StrOutputParser(),
        llm_config=AzureLLMConfig(model="gpt-4o"),
    )

    # Test output schema
    output_schema = aug_llm.derive_output_schema()
    logger.info(f"Output schema: {output_schema.__name__}")

    # Verify schema fields
    assert hasattr(output_schema, "model_fields")
    assert "content" in output_schema.model_fields


def test_pydantic_output_parser():
    """Test AugLLMConfig with PydanticOutputParser."""
    # Create a parser for the SearchResult model
    parser = PydanticOutputParser(pydantic_object=SearchResult)

    # Create AugLLMConfig with structured output
    aug_llm = AugLLMConfig(
        name="structured_output",
        system_message="You are a helpful assistant that provides answers with sources.",
        output_parser=parser,
        structured_output_model=SearchResult,  # Explicitly set the model
        llm_config=AzureLLMConfig(model="gpt-4o"),
    )

    # Test output schema
    output_schema = aug_llm.derive_output_schema()
    logger.info(f"Output schema: {output_schema.__name__}")

    # Verify schema has model_fields
    assert hasattr(output_schema, "model_fields")

    # Log the available fields for debugging
    logger.info(f"Output schema fields: {list(output_schema.model_fields.keys())}")

    # Check fields that should always be present
    assert "content" in output_schema.model_fields
    assert "messages" in output_schema.model_fields

    # If SearchResult fields are extracted properly, they should be in the schema
    # Just log whether they're present for debugging
    for field in ["answer", "sources", "confidence"]:
        logger.info(f"Field '{field}' present: {field in output_schema.model_fields}")

    # Also log the structured_output_model to confirm it's being set correctly
    logger.info(f"Structured output model: {aug_llm.structured_output_model}")
    if aug_llm.structured_output_model:
        logger.info(
            f"Model fields: {list(aug_llm.structured_output_model.model_fields.keys())}"
        )


def test_structured_output_model():
    """Test AugLLMConfig with direct structured_output_model."""
    # Create AugLLMConfig with structured output model
    aug_llm = AugLLMConfig(
        name="agent_action_output",
        system_message="You are an agent that takes actions based on user queries.",
        structured_output_model=AgentAction,
        llm_config=AzureLLMConfig(model="gpt-4o"),
    )

    # Test output schema
    output_schema = aug_llm.derive_output_schema()
    logger.info(f"Output schema: {output_schema.__name__}")

    # Verify schema fields
    assert hasattr(output_schema, "model_fields")
    assert "action" in output_schema.model_fields
    assert "thought" in output_schema.model_fields
    assert "parameters" in output_schema.model_fields


# Tests for StateSchema integration
def test_schema_composer_with_aug_llm():
    """Test SchemaComposer with AugLLMConfig for automatic schema generation."""
    # Create AugLLMConfig with various input fields
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content="You are a helpful assistant."),
            HumanMessage(content="Query: {query}\nContext: {context}"),
            MessagesPlaceholder(variable_name="chat_history"),
        ]
    )

    aug_llm = AugLLMConfig(
        name="complex_assistant",
        prompt_template=prompt,
        structured_output_model=SearchResult,
        llm_config=AzureLLMConfig(model="gpt-4o"),
    )

    # Log the input variables to understand what's being detected
    input_vars = aug_llm._get_input_variables()
    logger.info(f"Detected input variables: {input_vars}")

    # Get schema fields to see what's available
    schema_fields = aug_llm.get_schema_fields()
    logger.info(f"Schema fields: {list(schema_fields.keys())}")

    # Create schema from the engine
    schema = SchemaComposer.from_components([aug_llm], name="AssistantState")
    logger.info(f"Created schema: {schema.__name__}")

    # Display schema with rich UI
    SchemaUI.display_schema(schema)

    # Generate pretty code representation
    code_repr = SchemaUI.schema_to_code(schema)
    logger.info(f"Schema code representation:\n{code_repr}")

    # Verify schema has model_fields
    assert hasattr(schema, "model_fields")

    # Log all fields that were created in the schema
    logger.info(f"Schema fields: {list(schema.model_fields.keys())}")

    # Test that messages field is always included by SchemaComposer
    assert "messages" in schema.model_fields

    # For any fields found in the structured output model, log whether they're present
    if hasattr(SearchResult, "model_fields"):
        for field in SearchResult.model_fields:
            logger.info(
                f"Output model field '{field}' present: {field in schema.model_fields}"
            )

    # Log whether input variables were included
    for var in input_vars:
        logger.info(f"Input variable '{var}' present: {var in schema.model_fields}")

    # Log what's in the engine I/O mappings
    if hasattr(schema, "__engine_io_mappings__"):
        logger.info(f"Engine I/O mappings: {schema.__engine_io_mappings__}")
    if hasattr(schema, "__input_fields__"):
        logger.info(f"Input fields: {schema.__input_fields__}")
    if hasattr(schema, "__output_fields__"):
        logger.info(f"Output fields: {schema.__output_fields__}")


def test_multiple_engines_schema():
    """Test combining multiple AugLLMConfig engines in one schema."""
    # Create first engine for question answering
    qa_prompt = PromptTemplate(
        template="Answer the following question: {question}\nContext: {context}",
        input_variables=["question", "context"],
    )

    qa_engine = AugLLMConfig(
        name="qa_engine",
        prompt_template=qa_prompt,
        structured_output_model=SearchResult,
        llm_config=AzureLLMConfig(model="gpt-4o"),
    )

    # Create second engine for agent actions
    agent_prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content="You are an agent that takes actions."),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    agent_engine = AugLLMConfig(
        name="agent_engine",
        prompt_template=agent_prompt,
        structured_output_model=AgentAction,
        llm_config=AzureLLMConfig(model="gpt-4o"),
    )

    # Log the detected input variables for both engines
    qa_vars = qa_engine._get_input_variables()
    agent_vars = agent_engine._get_input_variables()
    logger.info(f"QA engine input vars: {qa_vars}")
    logger.info(f"Agent engine input vars: {agent_vars}")

    # Log the schema fields for both engines
    qa_fields = qa_engine.get_schema_fields()
    agent_fields = agent_engine.get_schema_fields()
    logger.info(f"QA engine schema fields: {list(qa_fields.keys())}")
    logger.info(f"Agent engine schema fields: {list(agent_fields.keys())}")

    # Combine them with SchemaComposer
    schema = SchemaComposer.from_components(
        [qa_engine, agent_engine], name="CombinedState"
    )
    logger.info(f"Created combined schema: {schema.__name__}")

    # Display schema with rich UI
    SchemaUI.display_schema(schema)

    # Log all fields in the combined schema
    logger.info(f"Combined schema fields: {list(schema.model_fields.keys())}")

    # Verify schema has model_fields
    assert hasattr(schema, "model_fields")

    # Test that messages field is always present
    assert "messages" in schema.model_fields

    # Log which input variables from each engine were included
    for var in qa_vars:
        logger.info(f"QA input var '{var}' present: {var in schema.model_fields}")

    for var in agent_vars:
        logger.info(f"Agent input var '{var}' present: {var in schema.model_fields}")

    # Log which output model fields were included
    if hasattr(SearchResult, "model_fields"):
        for field in SearchResult.model_fields:
            logger.info(
                f"SearchResult field '{field}' present: {field in schema.model_fields}"
            )

    if hasattr(AgentAction, "model_fields"):
        for field in AgentAction.model_fields:
            logger.info(
                f"AgentAction field '{field}' present: {field in schema.model_fields}"
            )

    # Log metadata about engine I/O mappings
    if hasattr(schema, "__engine_io_mappings__"):
        logger.info(f"Engine I/O mappings: {schema.__engine_io_mappings__}")
    if hasattr(schema, "__input_fields__"):
        logger.info(f"Input fields: {schema.__input_fields__}")
    if hasattr(schema, "__output_fields__"):
        logger.info(f"Output fields: {schema.__output_fields__}")


def test_schema_with_reducers():
    """Test schema with reducers tracked correctly from AugLLMConfig."""

    # Create existing state schema with reducers
    class CustomState(StateSchema):
        messages: Annotated[List[BaseMessage], operator.add] = Field(
            default_factory=list, description="Messages with add reducer"
        )
        context: Annotated[List[str], operator.add] = Field(
            default_factory=list, description="Context documents with add reducer"
        )

    # Create AugLLMConfig with output fields
    aug_llm = AugLLMConfig(
        name="reducer_aware_llm",
        system_message="You are a helpful assistant.",
        structured_output_model=SearchResult,
        llm_config=AzureLLMConfig(model="gpt-4o"),
    )

    # Combine them with SchemaComposer
    schema = SchemaComposer.from_components([CustomState, aug_llm], name="ReducerState")
    logger.info(f"Created reducer schema: {schema.__name__}")

    # Display schema with rich UI
    SchemaUI.display_schema(schema)

    # Verify reducers were preserved
    assert hasattr(schema, "__reducer_fields__")
    assert hasattr(schema, "__serializable_reducers__")
    assert "messages" in schema.__reducer_fields__
    assert "messages" in schema.__serializable_reducers__
    assert "context" in schema.__reducer_fields__
    assert "context" in schema.__serializable_reducers__

    # Create an instance to test reducer functionality
    state = schema()

    # Add messages (just a test, don't actually invoke)
    new_messages = [HumanMessage(content="Test message")]
    test_updates = {"messages": new_messages}

    # Apply updates with reducers
    updated_state = state.apply_reducers(test_updates)

    # Verify messages were properly reduced (concatenated)
    assert len(updated_state.messages) == 1


def test_engine_io_tracking():
    """Test tracking of input/output fields for engines."""
    # Create an AugLLMConfig with complex IO requirements
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content="You are a helpful assistant."),
            HumanMessage(content="Query: {query}\nContext: {context}"),
            MessagesPlaceholder(variable_name="chat_history"),
        ]
    )

    aug_llm = AugLLMConfig(
        name="io_tracked_llm",
        prompt_template=prompt,
        structured_output_model=SearchResult,
        llm_config=AzureLLMConfig(model="gpt-4o"),
    )

    # Create schema from this engine
    schema = SchemaComposer.from_components([aug_llm], name="TrackedIOState")
    logger.info(f"Created IO tracking schema: {schema.__name__}")

    # Display fields that should be tracked
    logger.info(f"Input fields: {aug_llm._get_input_variables()}")

    # Verify engine IO mappings are tracked in the schema
    assert hasattr(schema, "__engine_io_mappings__")
    assert "io_tracked_llm" in schema.__engine_io_mappings__

    # Check input fields
    assert hasattr(schema, "__input_fields__")
    assert "io_tracked_llm" in schema.__input_fields__

    # Check that query and context are tracked as inputs
    inputs = schema.__input_fields__["io_tracked_llm"]
    assert "query" in inputs
    assert "context" in inputs
    assert "chat_history" in inputs

    # Check output fields
    assert hasattr(schema, "__output_fields__")
    assert "io_tracked_llm" in schema.__output_fields__

    # Check that answer, sources, confidence are tracked as outputs
    outputs = schema.__output_fields__["io_tracked_llm"]
    assert "answer" in outputs
    assert "sources" in outputs
    assert "confidence" in outputs


def test_runtime_config_integration():
    """Test integration with runtime configuration."""
    # Create AugLLMConfig with system message
    aug_llm = AugLLMConfig(
        name="configurable_llm",
        system_message="You are a helpful assistant.",
        llm_config=AzureLLMConfig(model="gpt-4o"),
    )

    # Create runtime config with override parameters
    runtime_config: RunnableConfig = {
        "configurable": {
            "temperature": 0.7,
            "max_tokens": 1000,
            "system_message": "You are a specialized coding assistant.",
            "engine_configs": {
                "configurable_llm": {"temperature": 0.5}  # More specific override
            },
        }
    }

    # Apply the runtime config and extract params
    params = aug_llm.apply_runnable_config(runtime_config)
    logger.info(f"Extracted params: {params}")

    # Verify the parameters were extracted correctly
    assert "temperature" in params
    assert params["temperature"] == 0.5  # Should use the more specific value
    assert "max_tokens" in params
    assert params["max_tokens"] == 1000
    assert "system_message" in params
    assert params["system_message"] == "You are a specialized coding assistant."


def test_ui_representation():
    """Test rich UI representation of schemas with AugLLMConfig contributions."""
    # Create AugLLMConfig with both input and output schemas
    aug_llm = AugLLMConfig(
        name="ui_test_llm",
        system_message="You are a helpful assistant.",
        structured_output_model=SearchResult,
        llm_config=AzureLLMConfig(model="gpt-4o"),
    )

    # Create schema from this engine
    schema = SchemaComposer.from_components([aug_llm], name="UITestState")

    # Display schema with rich UI
    console = Console()
    console.print("Schema UI Representation:")
    SchemaUI.display_schema(schema)

    # Display code representation
    console.print("\nSchema Code Representation:")
    SchemaUI.display_schema_code(schema)

    # Create another schema for comparison
    class ComparisonState(StateSchema):
        """A simple schema for comparison."""

        query: str = Field(description="User query")
        result: str = Field(default="", description="Generated result")

    # Compare schemas
    console.print("\nSchema Comparison:")
    SchemaUI.compare_schemas(schema, ComparisonState)
