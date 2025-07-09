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
            if hasattr(tool, "__call__"):
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
    def __init__(self, content: str, tool_calls: List[Dict[str, Any]] = None):
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
        print(f"✅ Applied validation results to state")


def demonstrate_validation_integration():
    """Demonstrate how SimpleAgentWithValidation works."""

    print("🚀 SimpleAgentWithValidation Integration Demonstration")
    print("=" * 65)

    # Create tools
    search_tool = MockTool("web_search")
    calculator_tool = MockTool("calculator")

    # Create engine with tools
    engine = MockAugLLMConfig(
        model="gpt-4", temperature=0.7, tools=[search_tool, calculator_tool]
    )

    print(f"📚 Created engine with tools:")
    print(f"   Tools: {[t.name for t in engine.tools]}")
    print(f"   Tool routes: {engine.tool_routes}")

    # Define structured output model
    class TaskResult(BaseModel):
        completed: bool = Field(description="Whether the task was completed")
        result: str = Field(description="The result of the task")
        confidence: float = Field(description="Confidence score 0-1")
        tools_used: List[str] = Field(description="List of tools that were used")

    print(f"\n📋 Structured Output Model: {TaskResult.__name__}")

    # Create agent configuration (mock)
    agent_config = {
        "name": "Demo Agent",
        "engine": engine,
        "structured_output_model": TaskResult,
        "validation_mode": ValidationMode.PARTIAL,
        "update_validation_messages": True,
        "track_error_tools": True,
    }

    print(f"\n⚙️ Agent Configuration:")
    print(f"   Name: {agent_config['name']}")
    print(f"   Validation mode: {agent_config['validation_mode']}")
    print(f"   Update messages: {agent_config['update_validation_messages']}")
    print(f"   Track errors: {agent_config['track_error_tools']}")

    # Show how the validation node would be configured
    print(f"\n🔧 Validation Node Configuration:")
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

    print(f"   Engine name: {validation_config['engine_name']}")
    print(f"   Route mapping: {validation_config['route_to_node_mapping']}")

    # Show the graph structure
    print(f"\n🌊 Graph Flow Structure:")
    print(f"   START → agent_node")
    print(f"   agent_node → state_validator (if tool calls)")
    print(f"   agent_node → END (if no tool calls)")
    print(f"   state_validator → validation_router")
    print(f"   validation_router → tool_node|parse_output|agent_node (via Send)")
    print(f"   tool_node → END")
    print(f"   parse_output → END")

    # Simulate execution flow
    print(f"\n" + "=" * 65)
    print("EXECUTION SIMULATION")
    print("=" * 65)

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

    print(f"\n📨 AI Message with Tool Calls:")
    for tc in ai_message.tool_calls:
        print(f"   - {tc['name']} (id: {tc['id']})")

    # Simulate validation process
    print(f"\n🔍 Validation Process:")

    valid_tools = []
    error_tools = []

    for tool_call in ai_message.tool_calls:
        tool_name = tool_call["name"]
        if tool_name in state.tool_routes:
            route = state.tool_routes[tool_name]
            target = route_mapping.get(route, "tool_node")
            valid_tools.append((tool_name, target))
            print(f"   ✅ {tool_name}: valid → {target} (route: {route})")
        else:
            error_tools.append(tool_name)
            print(f"   ❌ {tool_name}: ERROR - tool not found")

    # Simulate state update
    print(f"\n📊 State Update Results:")
    print(f"   Valid tools: {len(valid_tools)}")
    print(f"   Error tools: {len(error_tools)}")
    print(f"   Validation state: Updated")
    print(f"   Tool message statuses: Updated")
    print(f"   Branch conditions: Updated")

    # Simulate routing decision
    print(f"\n🔀 Routing Decision:")

    if valid_tools:
        print(f"   Decision: Create {len(valid_tools)} Send branches")
        for tool_name, target in valid_tools:
            print(f"   📤 Send({target}, {tool_name}_call)")

        print(f"\n🎯 Execution Flow:")
        print(f"   1. state_validator updates state with validation results")
        print(f"   2. validation_router creates Send branches for valid tools")
        print(f"   3. Each Send creates parallel execution:")
        for tool_name, target in valid_tools:
            print(f"      - {tool_name} executes in {target}")
        print(f"   4. Results converge back to agent or END")
    else:
        print(f"   Decision: Route to agent (all validations failed)")

    # Show validation modes
    print(f"\n⚙️ Validation Mode Behaviors:")
    print(f"   STRICT: Any failure → route to agent")
    print(f"   PARTIAL: Continue with valid tools (current)")
    print(f"   PERMISSIVE: Only route to agent if ALL fail")

    print(f"\n🎉 Integration Benefits:")
    print(f"   ✅ Replaces placeholder with actual validation logic")
    print(f"   ✅ Provides both state updates and dynamic routing")
    print(f"   ✅ Integrates with state schema for persistence")
    print(f"   ✅ Supports different validation strategies")
    print(f"   ✅ Maintains backward compatibility")
    print(f"   ✅ Enables sophisticated tool management")


def show_comparison():
    """Show comparison between old and new approach."""

    print(f"\n" + "=" * 65)
    print("BEFORE vs AFTER COMPARISON")
    print("=" * 65)

    print(f"\n📜 BEFORE (SimpleAgent with placeholder):")
    print(f"   graph.add_node('validation', placeholder_node)")
    print(f"   validation_config = ValidationNodeConfig(...)")
    print(
        f"   graph.add_conditional_edges('validation', validation_config, routing_map)"
    )
    print(f"   ")
    print(f"   Issues:")
    print(f"   - Placeholder does nothing")
    print(f"   - No state updates")
    print(f"   - Validation logic separated from routing")
    print(f"   - Limited flexibility")

    print(f"\n✨ AFTER (SimpleAgentWithValidation):")
    print(f"   validation_node = StateUpdatingValidationNode(...)")
    print(f"   state_updater = validation_node.create_node_function()")
    print(f"   router_func = validation_node.create_router_function()")
    print(f"   graph.add_node('state_validator', state_updater)")
    print(f"   graph.add_node('validation_router', router_func)")
    print(f"   ")
    print(f"   Benefits:")
    print(f"   ✅ Actual validation logic")
    print(f"   ✅ State persistence")
    print(f"   ✅ Unified validation + routing")
    print(f"   ✅ Dynamic behavior")
    print(f"   ✅ Multiple validation modes")
    print(f"   ✅ Rich error tracking")


def show_usage_examples():
    """Show different usage patterns."""

    print(f"\n" + "=" * 65)
    print("USAGE EXAMPLES")
    print("=" * 65)

    print(f"\n1️⃣ Basic Usage:")
    print(f"   agent = SimpleAgentWithValidation.from_engine(engine)")
    print(f"   result = agent.invoke({{'query': 'process this'}})")

    print(f"\n2️⃣ With Structured Output:")
    print(f"   agent = SimpleAgentWithValidation(")
    print(f"       engine=engine,")
    print(f"       structured_output_model=TaskResult")
    print(f"   )")

    print(f"\n3️⃣ Strict Validation Mode:")
    print(f"   agent = SimpleAgentWithValidation.create_strict_validation(engine)")
    print(f"   # Any validation failure routes to agent")

    print(f"\n4️⃣ Permissive Validation Mode:")
    print(f"   agent = SimpleAgentWithValidation.create_permissive_validation(engine)")
    print(f"   # Only route to agent if ALL tools fail")

    print(f"\n5️⃣ Custom Validation Config:")
    print(f"   agent = SimpleAgentWithValidation(")
    print(f"       engine=engine,")
    print(f"       validation_mode=ValidationMode.PARTIAL,")
    print(f"       update_validation_messages=True,")
    print(f"       track_error_tools=True")
    print(f"   )")

    print(f"\n6️⃣ Upgrading Existing SimpleAgent:")
    print(f"   old_agent = SimpleAgent(engine=engine)")
    print(f"   new_agent = upgrade_simple_agent_with_validation(old_agent)")


if __name__ == "__main__":
    demonstrate_validation_integration()
    show_comparison()
    show_usage_examples()

    print(f"\n🎯 Key Takeaway:")
    print("   SimpleAgentWithValidation shows how to properly integrate")
    print("   StateUpdatingValidationNode into existing agent architecture,")
    print("   replacing placeholders with actual validation and routing logic.")
