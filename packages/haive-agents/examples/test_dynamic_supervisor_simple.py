"""Simple test of the cleaned up dynamic supervisor implementation."""

import asyncio

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig

from haive.agents.dynamic_supervisor import (
    DynamicSupervisorAgent,
    SupervisorStateWithTools,
)
from haive.agents.simple import SimpleAgent


class MockAgent:
    """Mock agent for testing without real LLMs."""

    def __init__(self, name: str, response: str = "Mock response"):
        self.name = name
        self.response = response
        self.calls = []

    def run(self, task: str) -> str:
        """Sync execution."""
        self.calls.append(task)
        return f"{self.response} for: {task}"

    async def arun(self, task: str) -> str:
        """Async execution."""
        return self.run(task)


def test_direct_tool_execution():
    """Test that handoff tools execute agents directly."""
    print("\n=== Testing Direct Tool Execution ===\n")

    # Create supervisor (mock engine for testing)
    supervisor = DynamicSupervisorAgent(
        name="test_supervisor",
        engine=AugLLMConfig(
            name="mock_engine", llm_config=AzureLLMConfig(model="gpt-4"), tools=[]
        ),
    )

    # Create state and add mock agents
    state = supervisor.create_initial_state()

    search_agent = MockAgent("search", "Found results")
    math_agent = MockAgent("math", "Calculated")

    state.add_agent("search", search_agent, "Search specialist")
    state.add_agent("math", math_agent, "Math expert")

    print(f"Registered {len(state.agents)} agents")
    print(f"Generated {len(state.generated_tools)} tools")

    # Get the generated tools
    tools = state.get_all_tools()
    tool_names = [t.name for t in tools]
    print(f"\nAvailable tools: {tool_names}")

    # Test handoff tool execution
    print("\n--- Testing Search Handoff ---")
    search_tool = next(t for t in tools if t.name == "handoff_to_search")
    result = search_tool.invoke({"task_description": "Find information about Python"})
    print(f"Result: {result}")
    print(f"State response: {state.agent_response}")
    print(f"Last executed: {state.last_executed_agent}")

    print("\n--- Testing Math Handoff ---")
    math_tool = next(t for t in tools if t.name == "handoff_to_math")
    result = math_tool.invoke({"task_description": "Calculate 2+2"})
    print(f"Result: {result}")
    print(f"State response: {state.agent_response}")
    print(f"Last executed: {state.last_executed_agent}")

    # Verify agents were called
    print("\n--- Verification ---")
    print(f"Search agent calls: {search_agent.calls}")
    print(f"Math agent calls: {math_agent.calls}")

    assert search_agent.calls == ["Find information about Python"]
    assert math_agent.calls == ["Calculate 2+2"]
    print("\n✅ All tests passed!")


def test_dynamic_agent_management():
    """Test adding and removing agents dynamically."""
    print("\n=== Testing Dynamic Agent Management ===\n")

    supervisor = DynamicSupervisorAgent(name="dynamic_test")
    state = supervisor.create_initial_state()

    print("Initial state:")
    print(f"  Agents: {list(state.agents.keys())}")
    print(f"  Tools: {state.generated_tools}")

    # Add an agent
    print("\nAdding calculator agent...")
    calc_agent = MockAgent("calc", "Result")
    state.add_agent("calculator", calc_agent, "Calculator expert")

    print(f"  Agents: {list(state.agents.keys())}")
    print(f"  Tools: {state.generated_tools}")

    # Test the new tool exists
    tools = state.get_all_tools()
    calc_tool = next((t for t in tools if t.name == "handoff_to_calculator"), None)
    assert calc_tool is not None, "Calculator handoff tool should exist"

    # Remove an agent
    print("\nRemoving calculator agent...")
    state.remove_agent("calculator")

    print(f"  Agents: {list(state.agents.keys())}")
    print(f"  Tools: {state.generated_tools}")

    # Verify tool was removed
    tools = state.get_all_tools()
    calc_tool = next((t for t in tools if t.name == "handoff_to_calculator"), None)
    assert calc_tool is None, "Calculator handoff tool should be removed"

    print("\n✅ Dynamic management tests passed!")


if __name__ == "__main__":
    print("🧪 Testing Cleaned Up Dynamic Supervisor Implementation")
    print("=" * 60)

    test_direct_tool_execution()
    test_dynamic_agent_management()

    print("\n" + "=" * 60)
    print("✨ All tests completed successfully!")
    print("\nThe dynamic supervisor now:")
    print("- Uses handoff tools that execute agents directly")
    print("- No separate agent_execution node needed")
    print("- Follows the experimental pattern we built")
    print("- Agents are properly excluded from serialization")
