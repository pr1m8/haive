"""
Tests for the OutputParserEngine with a focus on LangChain chain integration.

These tests verify that our OutputParserEngine works correctly standalone
and when integrated into LangChain chains.
"""

from enum import Enum
from typing import Optional

import pytest

# Mock LLM for testing
from langchain_core.language_models.fake import FakeListLLM
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from pydantic import BaseModel, Field

# Import our parser engine
from haive.core.engine.output_parser.base import (
    OutputParserType,
    create_json_parser,
    create_list_parser,
    create_output_parser_engine,
    create_pydantic_parser,
    create_str_parser,
)


# Test data models
class Person(BaseModel):
    """Test model for Pydantic parser."""

    name: str = Field(description="The person's name")
    age: int = Field(description="The person's age")
    occupation: Optional[str] = Field(default=None, description="The person's job")


class MovieGenre(str, Enum):
    """Test enum for enum parser."""

    ACTION = "action"
    COMEDY = "comedy"
    DRAMA = "drama"
    SCIFI = "sci-fi"


# Fixtures
@pytest.fixture
def mock_llm():
    """Create a mock LLM that returns predefined responses."""
    return FakeListLLM(
        responses=[
            # JSON output
            """{"name": "John Doe", "age": 30, "occupation": "Engineer"}""",
            # List output
            """1. Apple
2. Banana
3. Cherry""",
            # Boolean output (for boolean parser)
            "true",
            # Datetime output (for datetime parser)
            "2023-05-15T14:30:00",
            # XML output
            """<person>
  <name>Alice Smith</name>
  <age>28</age>
  <occupation>Designer</occupation>
</person>""",
        ]
    )


@pytest.fixture
def json_string():
    """Sample JSON string for testing."""
    return """{"name": "Jane Smith", "age": 42, "occupation": "Doctor"}"""


@pytest.fixture
def list_string():
    """Sample list string for testing."""
    return """- First item
- Second item
- Third item with some extra text"""


# Basic parser tests
def test_create_json_parser():
    """Test creating a JSON parser engine."""
    parser = create_json_parser(name="test_json_parser")
    assert parser.name == "test_json_parser"
    assert parser.parser_type == OutputParserType.JSON

    # Test direct invocation
    result = parser.invoke("""{"name": "Test", "value": 123}""")
    assert result == {"name": "Test", "value": 123}


def test_create_list_parser():
    """Test creating list parser engines."""
    # Default list parser
    parser = create_list_parser(name="test_list_parser")
    assert parser.parser_type == OutputParserType.LIST

    # Numbered list parser
    numbered_parser = create_list_parser(list_type="numbered", name="numbered_parser")
    assert numbered_parser.parser_type == OutputParserType.NUMBERED_LIST

    # Test parsing
    result = numbered_parser.invoke(
        """1. First item
2. Second item
3. Third item"""
    )

    assert result == ["First item", "Second item", "Third item"]


def test_create_pydantic_parser():
    """Test creating and using a Pydantic parser."""
    parser = create_pydantic_parser(pydantic_model=Person, name="person_parser")
    assert parser.parser_type == OutputParserType.PYDANTIC
    assert parser.pydantic_model == Person

    # Test parsing
    result = parser.invoke("""{"name": "Alice", "age": 30}""")
    assert isinstance(result, Person)
    assert result.name == "Alice"
    assert result.age == 30
    assert result.occupation is None


def test_parser_with_message_input():
    """Test parser with LangChain message as input."""
    parser = create_json_parser()

    # Create a message with JSON content
    message = AIMessage(content="""{"name": "Bob", "age": 25}""")

    # Parse from message
    result = parser.invoke(message)
    assert result == {"name": "Bob", "age": 25}


def test_parser_with_list_of_messages():
    """Test parser with a list of messages as input."""
    parser = create_str_parser()

    # Create messages
    messages = [HumanMessage(content="Hello"), AIMessage(content="World")]

    # Parse messages
    result = parser.invoke(messages)
    assert result == "Hello\nWorld"


# Chain integration tests
def test_simple_llm_parser_chain(mock_llm):
    """Test a simple LLM -> Parser chain."""
    json_parser = create_output_parser_engine(parser_type=OutputParserType.JSON)

    # Create a simple chain
    chain = mock_llm | json_parser

    # Invoke the chain
    result = chain.invoke("Generate a person")

    # Verify the result - should be parsed JSON from the mock LLM's first response
    assert isinstance(result, dict)
    assert result["name"] == "John Doe"
    assert result["age"] == 30


def test_prompt_llm_parser_chain(mock_llm):
    """Test a Prompt -> LLM -> Parser chain."""
    list_parser = create_output_parser_engine(
        parser_type=OutputParserType.NUMBERED_LIST
    )

    # Create a prompt
    prompt = PromptTemplate.from_template("List some {item}:")

    # Create a chain
    chain = prompt | mock_llm | list_parser

    # Invoke the chain
    result = chain.invoke({"item": "fruits"})

    # Verify the result
    assert isinstance(result, list)
    assert len(result) == 3
    assert "Apple" in result
    assert "Banana" in result
    assert "Cherry" in result


def test_pydantic_parser_with_format_instructions(mock_llm):
    """Test using a Pydantic parser with format instructions in the prompt."""
    # Create parser
    parser = create_output_parser_engine(
        parser_type=OutputParserType.PYDANTIC, pydantic_model=Person
    )

    # Create a prompt template that includes format instructions
    prompt = ChatPromptTemplate.from_template(
        """Generate information about a person in the following format:
        
        {format_instructions}
        
        Make the person a {occupation} named {name}.
        """
    )

    # Create chain with format instructions injected
    chain = (
        {
            "format_instructions": parser.get_format_instructions,
            "occupation": lambda x: x["occupation"],
            "name": lambda x: x["name"],
        }
        | prompt
        | mock_llm
        | parser
    )

    # Test the chain
    result = chain.invoke({"occupation": "Engineer", "name": "John"})

    # Verify result is a Person instance
    assert isinstance(result, Person)
    assert result.name == "John Doe"  # From mock response
    assert result.occupation == "Engineer"


def test_error_handling_in_parser():
    """Test error handling in parser."""

    # Create JSON parser with custom error handler
    def error_handler(text, error):
        return {"error": str(error), "text": text}

    parser = create_output_parser_engine(
        parser_type=OutputParserType.JSON,
        name="error_handling_parser",
        parser_config={"error_handler": error_handler},
    )

    # Test with invalid JSON
    result = parser.invoke("This is not valid JSON")

    # Verify error handling
    assert "error" in result
    assert "text" in result
    assert result["text"] == "This is not valid JSON"


def test_structured_output_parser():
    """Test creating and using a structured output parser."""
    # Define response schemas
    response_schemas = [
        {"name": "name", "description": "The person's name"},
        {"name": "age", "description": "The person's age"},
        {"name": "favorite_color", "description": "The person's favorite color"},
    ]

    # Create parser
    parser = create_output_parser_engine(
        parser_type=OutputParserType.STRUCTURED, response_schemas=response_schemas
    )

    # Test with structured format
    result = parser.invoke(
        """
    name: Jane Smith
    age: 32
    favorite_color: blue
    """
    )

    # Verify result
    assert result["name"] == "Jane Smith"
    assert result["age"] == "32"
    assert result["favorite_color"] == "blue"


# Async tests
@pytest.mark.asyncio
async def test_async_parser_chain(mock_llm):
    """Test asynchronous operation of parser in a chain."""
    # Create parser
    xml_parser = create_output_parser_engine(
        parser_type=OutputParserType.XML, name="async_xml_parser"
    )

    # Create chain
    chain = mock_llm | xml_parser

    # Invoke asynchronously (uses the 5th mock response, which is XML)
    # We need to skip to the 5th response since the mock LLM keeps a counter
    mock_llm.invoke("Skip 1")
    mock_llm.invoke("Skip 2")
    mock_llm.invoke("Skip 3")
    mock_llm.invoke("Skip 4")

    # Now get XML response
    result = await chain.ainvoke("Generate XML")

    # Verify result
    assert isinstance(result, dict)
    assert "person" in result


@pytest.mark.asyncio
async def test_parser_with_streaming_llm():
    """Test parser with a streaming LLM."""
    # Create a streaming mock LLM
    from langchain_core.language_models.fake import FakeStreamingLLM

    streaming_llm = FakeStreamingLLM(
        responses=["""{"name": "Streaming", "data": "Test"}"""]
    )

    # Create parser
    json_parser = create_output_parser_engine(parser_type=OutputParserType.JSON)

    # Create chain
    chain = streaming_llm | json_parser

    # Invoke
    result = await chain.ainvoke("Generate streaming data")

    # Verify result
    assert result["name"] == "Streaming"
    assert result["data"] == "Test"


# Integration with other LangChain components
def test_parser_with_runnable_map():
    """Test using a parser with RunnableMap for parallel processing."""
    from langchain_core.runnables import RunnableMap

    # Create two parsers
    json_parser = create_output_parser_engine(parser_type=OutputParserType.JSON)
    list_parser = create_output_parser_engine(
        parser_type=OutputParserType.MARKDOWN_LIST
    )

    # Create a map that applies different parsers to different inputs
    parallel_parser = RunnableMap(
        {
            "person": lambda inputs: json_parser.invoke(inputs["json_text"]),
            "items": lambda inputs: list_parser.invoke(inputs["list_text"]),
        }
    )

    # Test the parallel parser
    result = parallel_parser.invoke(
        {
            "json_text": """{"name": "Test Person", "age": 25}""",
            "list_text": """- Item A\n- Item B\n- Item C""",
        }
    )

    # Verify results
    assert result["person"]["name"] == "Test Person"
    assert result["person"]["age"] == 25
    assert result["items"] == ["Item A", "Item B", "Item C"]


def test_parser_chain_with_lcel_branching():
    """Test parser in a chain with branching logic using LCEL."""
    from langchain_core.runnables import RunnableBranch

    # Create parsers
    json_parser = create_output_parser_engine(parser_type=OutputParserType.JSON)
    list_parser = create_output_parser_engine(parser_type=OutputParserType.LIST)
    str_parser = create_output_parser_engine(parser_type=OutputParserType.STRING)

    # Create a branch that chooses parser based on input format
    branch = RunnableBranch(
        # If input starts with [, use list parser
        (lambda x: x.startswith("["), list_parser),
        # If input starts with {, use JSON parser
        (lambda x: x.startswith("{"), json_parser),
        # Default to string parser
        str_parser,
    )

    # Test with JSON input
    json_result = branch.invoke("""{"key": "value"}""")
    assert json_result == {"key": "value"}

    # Test with list input
    list_result = branch.invoke("""[1, 2, 3]""")
    # This would actually parse as JSON since the default ListOutputParser
    # expects a different format. That's fine for this test.
    assert list_result == [1, 2, 3]

    # Test with plain text
    text_result = branch.invoke("""Just plain text""")
    assert text_result == "Just plain text"


# Integration with Haive components
def test_output_parser_as_graph_component():
    """Test using an output parser as a component in Haive framework."""
    # Create parser
    json_parser = create_output_parser_engine(parser_type=OutputParserType.JSON)

    # Test basic functionality
    assert hasattr(json_parser, "get_input_fields")
    assert hasattr(json_parser, "get_output_fields")
    assert hasattr(json_parser, "create_runnable")
    assert hasattr(json_parser, "invoke")
    assert hasattr(json_parser, "ainvoke")

    # Test processing a JSON string
    json_str = """{"name": "Test User", "score": 42, "active": true}"""
    result = json_parser.invoke(json_str)

    assert isinstance(result, dict)
    assert result["name"] == "Test User"
    assert result["score"] == 42
    assert result["active"] is True

    # Verify correct output field definition
    output_fields = json_parser.get_output_fields()
    assert "result" in output_fields

    # Verify correct input field definition
    input_fields = json_parser.get_input_fields()
    assert "input" in input_fields


def test_parser_with_runnable_config():
    """Test parser with different runnable configurations."""
    # Create parser with no default config
    json_parser = create_output_parser_engine(parser_type=OutputParserType.JSON)

    # Create a runnable config
    runnable_config = {
        "configurable": {
            "schema": {"type": "object", "properties": {"name": {"type": "string"}}}
        }
    }

    # Test direct invocation with config
    json_str = """{"name": "Config Test", "value": 123}"""
    result = json_parser.invoke(json_str, runnable_config)

    assert isinstance(result, dict)
    assert result["name"] == "Config Test"

    # Test engine's ability to extract config params
    params = json_parser.apply_runnable_config(runnable_config)
    assert "schema" in params


def test_output_parser_error_recovery():
    """Test parser's ability to recover from parsing errors."""

    # Create parser with error handling
    def error_handler(text, error):
        return {"success": False, "original_text": text, "error": str(error)}

    parser = create_output_parser_engine(
        parser_type=OutputParserType.JSON,
        parser_config={"error_handler": error_handler},
    )

    # Test with invalid JSON
    invalid_json = "This is not valid JSON { missing closing bracket"
    result = parser.invoke(invalid_json)

    # Verify error handler was called
    assert result["success"] is False
    assert "original_text" in result
    assert "error" in result
