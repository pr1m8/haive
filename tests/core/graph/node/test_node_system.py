"""
Tests for the new node system.

These tests validate the core functionality of the node system,
including decorators, factory methods, and execution behavior.
"""

import pytest
from pydantic import BaseModel, Field

from haive.core.graph.node import (
    # Core
    NodeConfig,
    NodeFactory,
    
    # Decorators
    node,
    async_node,
    engine_node,
    validation_node,
    retry_node,
    interruptible_node,
    tool_node,
    
    # Types
    Command,
    Send,
    State,
)
from haive.core.graph.node.utils.testing import NodeTester
from haive.core.schema.state_schema import StateSchema


# Example schema for testing
class ExampleState(StateSchema):
    """Example state schema for testing."""
    
    input: str = ""
    output: str = ""
    messages: list = Field(default_factory=list)
    counter: int = 0
    
    def increment(self) -> None:
        """Increment the counter."""
        self.counter += 1


# Test basic node decorator
def test_basic_node_decorator():
    """Test the basic node decorator."""
    
    @node()
    def simple_node(state: State) -> State:
        """Simple node that returns state."""
        return state
    
    # Test with dict state
    state = {"hello": "world"}
    result = simple_node(state)
    assert result == state
    
    # Test with schema state
    schema_state = ExampleState(input="hello")
    result = simple_node(schema_state)
    assert isinstance(result, ExampleState)
    assert result.input == "hello"


# Test async node decorator
@pytest.mark.asyncio
async def test_async_node_decorator():
    """Test the async node decorator."""
    
    @async_node()
    async def async_simple_node(state: State) -> State:
        """Simple async node that returns state."""
        return state
    
    # Test with dict state
    state = {"hello": "world"}
    result = await async_simple_node(state)
    assert result == state
    
    # Test with schema state
    schema_state = ExampleState(input="hello")
    result = await async_simple_node(schema_state)
    assert isinstance(result, ExampleState)
    assert result.input == "hello"


# Test command routing
def test_command_routing():
    """Test command routing with goto."""
    
    @node(command_goto="next_node")
    def routing_node(state: State) -> State:
        """Node that routes to next_node."""
        return state
    
    # Test with dict state
    state = {"hello": "world"}
    result = routing_node(state)
    
    # Check that result is a Command
    assert isinstance(result, Command)
    assert result.goto == "next_node"
    assert result.update == state


# Test input/output mapping
def test_input_output_mapping():
    """Test input and output mapping."""
    
    @node(
        input_mapping={"input": "query"},
        output_mapping={"result": "output"}
    )
    def mapping_node(query: str) -> dict:
        """Node that processes a query."""
        return {"result": query.upper()}
    
    # Test with dict state
    state = {"input": "hello"}
    result = mapping_node(state)
    
    # Check that output is mapped correctly
    assert isinstance(result, dict)
    assert result["output"] == "HELLO"


# Test validation node
def test_validation_node():
    """Test validation node."""
    
    class UserState(BaseModel):
        """User state with validation."""
        
        username: str
        email: str
        
    validator = validation_node(
        validation_schema=UserState,
        success_node="success",
        failure_node="failure"
    )
    
    # Test with valid state
    valid_state = {"username": "testuser", "email": "test@example.com"}
    valid_result = validator(valid_state)
    
    # Check that validation passed
    assert isinstance(valid_result, Command)
    assert valid_result.goto == "success"
    assert isinstance(valid_result.update, UserState)
    
    # Test with invalid state
    invalid_state = {"username": "testuser"}  # Missing email
    invalid_result = validator(invalid_state)
    
    # Check that validation failed
    assert isinstance(invalid_result, Command)
    assert invalid_result.goto == "failure"
    assert "validation_error" in invalid_result.update


# Test interruptible node
def test_interruptible_node():
    """Test interruptible node."""
    
    @interruptible_node(resume_node="resume_node")
    def interrupt_node(state: State) -> State:
        """Node that interrupts execution."""
        from haive.core.graph.node import interrupt
        
        # Check if we're resuming
        if hasattr(state, "resume_payload") or (
            isinstance(state, dict) and "resume_payload" in state
        ):
            # Return the resume payload
            if isinstance(state, dict):
                return {"result": state["resume_payload"]}
            return {"result": state.resume_payload}
        
        # Otherwise interrupt
        interrupt(payload="interrupted")
        return state  # Never reached
    
    # Test interrupt behavior
    state = {"input": "hello"}
    result = interrupt_node(state)
    
    # Check that we got an interrupt Command
    assert isinstance(result, Command)
    assert result.goto == "resume_node"
    assert result.update["interrupt_status"] == "interrupted"
    assert result.update["interrupt_payload"] == "interrupted"
    
    # Now test resumption
    resume_state = {"resume_payload": "resumed"}
    resume_result = interrupt_node(resume_state)
    
    # Check that we resumed correctly
    assert isinstance(resume_result, dict)
    assert resume_result["result"] == "resumed"


# Test tool node
def test_tool_node():
    """Test tool node."""
    
    # Define a mock tool
    class MockTool:
        """Mock tool for testing."""
        
        name = "mock_tool"
        
        def __call__(self, arg1=None, arg2=None):
            """Execute the tool."""
            return f"Executed with {arg1} and {arg2}"
    
    # Create tool node
    tools = [MockTool()]
    tool_executor = tool_node(
        tools=tools,
        command_goto="next_node",
        name="test_tool_node"
    )
    
    # Create state with tool calls
    state = {
        "messages": [
            {
                "tool_calls": [
                    {
                        "name": "mock_tool",
                        "args": {"arg1": "value1", "arg2": "value2"}
                    }
                ]
            }
        ]
    }
    
    # Execute the tool node
    result = tool_executor(state)
    
    # Check the result
    assert isinstance(result, Command)
    assert result.goto == "next_node"
    assert len(result.update["messages"]) == 2
    assert result.update["messages"][1]["tool_name"] == "mock_tool"
    assert "Executed with value1 and value2" in result.update["messages"][1]["content"]


# Test NodeTester utilities
def test_node_tester():
    """Test NodeTester utilities."""
    
    @node()
    def test_node(state: State) -> State:
        """Node for testing."""
        if isinstance(state, dict):
            return {"result": state.get("input", "") + "_processed"}
        return {"result": "processed"}
    
    # Run the node
    result = NodeTester.run_node(test_node, {"input": "test"})
    assert result["result"] == "test_processed"
    
    # Test assertion
    NodeTester.assert_node_output(
        test_node,
        {"input": "hello"},
        "hello_processed",
        path="result"
    )