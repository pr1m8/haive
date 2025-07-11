"""Example showing SimpleAgentWithValidation in action."""

import os
import sys
from typing import Any, Dict, List

from pydantic import BaseModel, Field

# Add packages to path for example
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "..", "haive-core", "src")
)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


# Mock dependencies for example
class MockLLMConfig:
    def __init__(self, model="gpt-4", temperature=0.7):
        self.model = model
        self.temperature = temperature


class MockAugLLMConfig:
    def __init__(self, model="gpt-4", temperature=0.7, tools=None):
        self.name = f"engine_{id(self)}"
        self.model = model
        self.temperature = temperature
        self.tools = tools or []
        self.tool_routes = {}
        self.structured_output_model = None
        self.force_tool_use = False

        # Auto-generate tool routes
        for tool in self.tools:
            tool_name = getattr(tool, "name", str(tool))
            if callable(tool):
                self.tool_routes[tool_name] = "function"
            else:
                self.tool_routes[tool_name] = "langchain_tool"

    def derive_output_schema(self):
        """Mock schema derivation."""
        from pydantic import BaseModel

        class MockOutputSchema(BaseModel):
            content: str = "Mock output"

        return MockOutputSchema


class MockTool:
    def __init__(self, name: str):
        self.name = name

    def __call__(self, *args, **kwargs):
        return f"Executed {self.name}"


class MockAIMessage:
    def __init__(self, content: str, tool_calls: list[dict[str, Any]] = None):
        self.content = content
        self.tool_calls = tool_calls or []


# Mock the validation modes
class ValidationMode:
    STRICT = "strict"
    PARTIAL = "partial"
    PERMISSIVE = "permissive"


# Mock state for demonstration
class MockState:
    def __init__(self):
        self.messages = []
        self.tools = []
        self.tool_routes = {}
        self.engines = {}
        self.validation_state = None
        self.error_tool_calls = []

    def get_tool_calls(self):
        if not self.messages:
            return []
        last_msg = self.messages[-1]
        if hasattr(last_msg, "tool_calls"):
            return last_msg.tool_calls
        return []

    def apply_validation_results(self, validation_state):
        self.validation_state = validation_state


def demonstrate_validation_integration():
    """Demonstrate how SimpleAgentWithValidation works."""

    # Create tools
    search_tool = MockTool("web_search")
    calculator_tool = MockTool("calculator")

    # Create engine with tools
    engine = MockAugLLMConfig(
        model="gpt-4", temperature=0.7, tools=[search_tool, calculator_tool]
    )


    # Define structured output model
    class TaskResult(BaseModel):
        completed: bool = Field(description="Whether the task was completed")
        result: str = Field(description="The result of the task")
        confidence: float = Field(description="Confidence score 0-1")
        tools_used: list[str] = Field(description="List of tools that were used")


    # Create agent configuration (mock)
    agent_config = {
        "name": "Demo Agent",
        "engine": engine,
        "structured_output_model": TaskResult,
        "validation_mode": ValidationMode.PARTIAL,
        "update_validation_messages": True,
        "track_error_tools": True,
    }


    # Show how the validation node would be configured
    route_mapping = {
        "langchain_tool": "tool_node",
        "function": "tool_node",
        "pydantic_model": "parse_output",
        "retriever": "retriever_node",
        "unknown": "tool_node",
    }

    validation_config = {
        "name": "state_validator",
        "engine_name": engine.name,
        "validation_mode": agent_config["validation_mode"],
        "update_messages": agent_config["update_validation_messages"],
        "track_error_tools": agent_config["track_error_tools"],
        "route_to_node_mapping": route_mapping,
    }


    # Show the graph structure

    # Simulate execution flow

    # Create mock state
    state = MockState()
    state.tools = [search_tool, calculator_tool]
    state.tool_routes = engine.tool_routes
    state.engines = {"main": engine}

    # Add AI message with tool calls
    ai_message = MockAIMessage(
        content="I'll search for information and calculate the result.",
        tool_calls=[
            {"id": "call_1", "name": "web_search", "args": {"query": "AI trends"}},
            {"id": "call_2", "name": "calculator", "args": {"expr": "100 * 0.85"}},
            {"id": "call_3", "name": "unknown_tool", "args": {}},  # This will fail
        ],
    )
    state.messages.append(ai_message)

    for tc in ai_message.tool_calls:
        pass

    # Simulate validation process

    valid_tools = []
    error_tools = []

    for tool_call in ai_message.tool_calls:
        tool_name = tool_call["name"]
        if tool_name in state.tool_routes:
            route = state.tool_routes[tool_name]
            target = route_mapping.get(route, "tool_node")
            valid_tools.append((tool_name, target))
        else:
            error_tools.append(tool_name)

    # Simulate state update

    # Simulate routing decision

    if valid_tools:
        for tool_name, target in valid_tools:
            pass)")

        for tool_name, target in valid_tools:
            pass
    else:
        pass

    # Show validation modes



def show_comparison():
    """Show comparison between old and new approach."""




def show_usage_examples():
    """Show different usage patterns."""








if __name__ == "__main__":
    demonstrate_validation_integration()
    show_comparison()
    show_usage_examples()

