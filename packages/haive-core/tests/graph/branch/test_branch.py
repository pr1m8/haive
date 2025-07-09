"""
Test cases for the Haive Branch system.

This module provides comprehensive tests for branch functionality
including Send objects, dynamic mapping, and serialization.
"""

import logging
from typing import Any, List, Optional, Union

import pytest
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.types import Command, Send
from pydantic import Field
from rich.console import Console
from rich.panel import Panel
from rich.pretty import Pretty

# Import branch system
from haive.core.graph.branches import (
    Branch,
    BranchMode,
    ComparisonType,
    chain,
    conditional,
    from_function,
    key_equals,
    key_exists,
    message_contains,
    send_mapper,
)
from haive.core.graph.branches.dynamic import DynamicMapping
from haive.core.graph.branches.send_mapping import SendGenerator, SendMapping
from haive.core.schema.state_schema import StateSchema

# Setup logging
logger = logging.getLogger("branch_tests")
console = Console()


# Define test schemas
class _TestState(StateSchema):
    """Test state schema for branch tests."""

    query: str = Field(default="")
    messages: List[Union[HumanMessage, AIMessage]] = Field(default_factory=list)
    count: int = Field(default=0)
    flag: bool = Field(default=False)
    contents: List[str] = Field(default_factory=list)

    def has_greeting(self) -> bool:
        """Check if any message contains a greeting."""
        if not self.messages:
            return False

        for message in self.messages:
            content = message.content.lower()
            if any(word in content for word in ["hello", "hi", "hey", "greetings"]):
                return True

        return False


# Debugging helper to display test information
def log_test(
    title: str, state: Any = None, branch: Optional[Branch] = None, result: Any = None
):
    """Log test information with rich formatting."""
    console.rule(f"[bold magenta]{title}")

    if state:
        console.print(
            Panel(
                Pretty(state, expand_all=True), title="Test State", border_style="blue"
            )
        )

    if branch:
        branch_info = {
            "type": branch.mode,
            "key": branch.key,
            "value": branch.value,
            "comparison": branch.comparison,
            "default": branch.default,
        }
        console.print(
            Panel(
                Pretty(branch_info, expand_all=True),
                title="Branch Configuration",
                border_style="green",
            )
        )

    if result:
        console.print(
            Panel(
                Pretty(result, expand_all=True),
                title="Evaluation Result",
                border_style="yellow",
            )
        )

    console.print()


# Test fixtures
@pytest.fixture
def basic_state():
    """Create a basic dictionary state."""
    return {
        "query": "help me",
        "count": 5,
        "flag": True,
        "contents": ["Document 1", "Document 2", "Document 3"],
    }


@pytest.fixture
def schema_state():
    """Create a StateSchema instance."""
    return _TestState(
        query="help me",
        messages=[
            HumanMessage(content="Hello, can you help me?"),
            AIMessage(content="I'd be happy to help!"),
        ],
        count=5,
        flag=True,
        contents=["Document 1", "Document 2", "Document 3"],
    )


@pytest.fixture
def mapper_function():
    """Create a function that maps contents to Send objects."""

    def map_contents(state: Any) -> List[Send]:
        if hasattr(state, "contents"):
            contents = state.contents
        else:
            contents = state.get("contents", [])

        return [Send("process_content", {"content": content}) for content in contents]

    return map_contents


# Basic branch tests
def test_basic_key_equals(basic_state):
    """Test basic key equals branch."""
    # Create branch
    branch = key_equals("query", "help me", "help_route", "other_route")

    # Evaluate branch
    result = branch(basic_state)

    # Log test information
    log_test("Basic Key Equals Test", basic_state, branch, result)

    # Assert correct result
    assert result == "help_route"


def test_key_exists(basic_state):
    """Test key exists branch."""
    # Create branch checking for non-existent key
    branch = key_exists("missing_key", "exists_route", "missing_route")

    # Evaluate branch
    result = branch(basic_state)

    # Log test information
    log_test("Key Exists Test (Missing Key)", basic_state, branch, result)

    # Assert correct result
    assert result == "missing_route"


def test_from_function(schema_state):
    """Test branch from function."""
    # Create branch from state schema method
    branch = from_function(
        lambda state: state.has_greeting(),
        {True: "greeting_route", False: "normal_route"},
    )

    # Evaluate branch
    result = branch(schema_state)

    # Log test information
    log_test("Branch From Function Test", schema_state, branch, result)

    # Assert correct result
    assert result == "greeting_route"


def test_message_contains(schema_state):
    """Test message contains branch."""
    # Create branch to check if message contains "help"
    branch = message_contains("help", "help_route", "other_route")

    # Evaluate branch
    result = branch(schema_state)

    # Log test information
    log_test("Message Contains Test", schema_state, branch, result)

    # Assert correct result
    assert result == "help_route"


def test_chain_branches(schema_state):
    """Test chain of branches."""
    # Create chain of branches
    branch = chain(
        key_equals("query", "not_matching", "first_route"),
        message_contains("help", "help_route"),
        key_equals("count", 5, "count_route"),
        default="fallback_route",
    )

    # Evaluate branch
    result = branch(schema_state)

    # Log test information
    log_test("Chain Branches Test", schema_state, branch, result)

    # Assert correct result - should match the first successful branch
    assert result == "help_route"


def test_conditional_branch(schema_state):
    """Test conditional branch."""
    # Create conditional branch
    branch = conditional(
        lambda state: state.count > 3, "high_count_route", "low_count_route"
    )

    # Evaluate branch
    result = branch(schema_state)

    # Log test information
    log_test("Conditional Branch Test", schema_state, branch, result)

    # Assert correct result
    assert result == "high_count_route"


# Send tests
def test_send_mapper_with_function(schema_state, mapper_function):
    """Test send mapper using a function."""
    # Create send mapper
    branch = Branch(
        mode=BranchMode.SEND_MAPPER,
        function=mapper_function,  # Set function directly instead of function_ref
    )

    # Evaluate branch
    result = branch(schema_state)

    # Log test information
    log_test("Send Mapper with Function Test", schema_state, branch, result)

    # Get the Send objects - they're wrapped in BranchResult
    if hasattr(result, "send_objects"):
        send_objects = result.send_objects
    else:
        # For backward compatibility, might be direct list
        send_objects = result

    # Assert correct result is list of Send objects
    assert isinstance(send_objects, list)
    assert len(send_objects) == 3
    assert all(isinstance(item, Send) for item in send_objects)
    assert all(item.node == "process_content" for item in send_objects)


def test_send_mapper_with_mappings(schema_state):
    """Test send mapper using SendMapping objects."""
    # Create send mapper with explicit mappings
    branch = send_mapper(
        mappings=[
            SendMapping(
                target="process_content",
                fields={"content": "contents.0", "index": "count"},
                condition="contents.0",
                condition_value=None,  # Not None means it exists
            ),
            SendMapping(
                target="process_content",
                fields={"content": "contents.1"},
                condition="contents.1",
                condition_value=None,
            ),
        ]
    )

    # Evaluate branch
    result = branch(schema_state)

    # Log test information
    log_test("Send Mapper with Mappings Test", schema_state, branch, result)

    # Get the Send objects
    if hasattr(result, "send_objects"):
        send_objects = result.send_objects
    else:
        # For backward compatibility
        send_objects = result

    # Assert correct result is list of Send objects
    assert isinstance(send_objects, list)
    assert len(send_objects) == 2
    assert all(isinstance(item, Send) for item in send_objects)
    assert all(item.node == "process_content" for item in send_objects)
    assert send_objects[0].arg["content"] == "Document 1"
    assert send_objects[0].arg["index"] == 5
    assert send_objects[1].arg["content"] == "Document 2"


def test_send_mapper_with_generator(schema_state):
    """Test send mapper using SendGenerator."""
    # Create send mapper with generator
    branch = send_mapper(
        generators=[
            SendGenerator(
                target="process_content",
                collection_field="contents",
                item_mapping={
                    "content": lambda item: item.upper(),
                    "original": lambda item: item,
                },
            )
        ]
    )

    # Evaluate branch
    result = branch(schema_state)

    # Log test information
    log_test("Send Mapper with Generator Test", schema_state, branch, result)

    # Get the Send objects
    if hasattr(result, "send_objects"):
        send_objects = result.send_objects
    else:
        # For backward compatibility
        send_objects = result

    # Assert correct result is list of Send objects
    assert isinstance(send_objects, list)
    assert len(send_objects) == 3
    assert all(isinstance(item, Send) for item in send_objects)
    assert all(item.node == "process_content" for item in send_objects)
    assert send_objects[0].arg["content"] == "DOCUMENT 1"
    assert send_objects[0].arg["original"] == "Document 1"


# Command and dynamic mapping tests
def test_dynamic_output_mapping():
    """Test dynamic output mapping with Command object return."""
    # Create state with score
    state = {"score": 85, "query": "complex question"}

    # Create a branch with dynamic mode
    branch = Branch(mode=BranchMode.DYNAMIC, default="normal_route")

    # Set dynamic mapping
    branch.dynamic_mapping = DynamicMapping(
        mappings={
            "high_score_route": {
                "response": "detailed_answer",
                "sources": "all_sources",
            },
            "normal_route": {"response": "simple_answer", "sources": "top_sources"},
        },
        key="score",
        value=80,
        comparison=ComparisonType.GREATER_THAN,
        default_node="normal_route",
    )

    # For debugging - print the dynamic_mapping config
    console.print(
        f"\nDynamic Mapping: key={branch.dynamic_mapping.key}, value={branch.dynamic_mapping.value}, "
        f"comparison={branch.dynamic_mapping.comparison}"
    )

    # Evaluate branch
    result = branch(state)

    # Log test information
    log_test("Dynamic Output Mapping Test", state, branch, result)

    # Check the result is a Command object
    assert isinstance(result, Command), f"Expected Command, got {type(result)}"
    assert result.goto == "high_score_route"
    assert "output_mapping" in result.update
    assert result.update["output_mapping"] == {
        "response": "detailed_answer",
        "sources": "all_sources",
    }


# Serialization tests
def test_serialization_deserialization(schema_state):
    """Test serialization and deserialization of branches."""
    # Create a complex branch
    original_branch = chain(
        message_contains("help"),
        key_equals("count", 5),
        conditional(
            lambda state: state.has_greeting(),
            "greeting_route",
            key_equals("flag", True, "flag_route", "no_flag_route"),
        ),
    )

    # Serialize to dict
    branch_dict = original_branch.model_dump()

    # Log serialized data
    console.rule("[bold magenta]Serialization Test")
    console.print(
        Panel(
            Pretty(
                branch_dict, expand_all=False
            ),  # Not expanding to avoid too much output
            title="Serialized Branch Dictionary",
            border_style="cyan",
        )
    )

    # Deserialize
    restored_branch = Branch.model_validate(branch_dict)

    # Test with same state
    original_result = original_branch(schema_state)
    restored_result = restored_branch(schema_state)

    # Log test information
    console.print(
        Panel(
            f"Original result: [bold green]{original_result}[/bold green]\n"
            f"Restored result: [bold green]{restored_result}[/bold green]",
            title="Serialization Results",
            border_style="green",
        )
    )

    # Assert results match
    assert original_result == restored_result
