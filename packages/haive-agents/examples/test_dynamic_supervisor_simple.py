"""Simple test of the cleaned up dynamic supervisor implementation."""

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig

from haive.agents.dynamic_supervisor import (
    DynamicSupervisorAgent,
)


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

    # Get the generated tools
    tools = state.get_all_tools()
    [t.name for t in tools]

    # Test handoff tool execution
    search_tool = next(t for t in tools if t.name == "handoff_to_search")
    search_tool.invoke({"task_description": "Find information about Python"})

    math_tool = next(t for t in tools if t.name == "handoff_to_math")
    math_tool.invoke({"task_description": "Calculate 2+2"})

    # Verify agents were called

    assert search_agent.calls == ["Find information about Python"]
    assert math_agent.calls == ["Calculate 2+2"]


def test_dynamic_agent_management():
    """Test adding and removing agents dynamically."""
    supervisor = DynamicSupervisorAgent(name="dynamic_test")
    state = supervisor.create_initial_state()

    # Add an agent
    calc_agent = MockAgent("calc", "Result")
    state.add_agent("calculator", calc_agent, "Calculator expert")

    # Test the new tool exists
    tools = state.get_all_tools()
    calc_tool = next((t for t in tools if t.name == "handoff_to_calculator"), None)
    assert calc_tool is not None, "Calculator handoff tool should exist"

    # Remove an agent
    state.remove_agent("calculator")

    # Verify tool was removed
    tools = state.get_all_tools()
    calc_tool = next((t for t in tools if t.name == "handoff_to_calculator"), None)
    assert calc_tool is None, "Calculator handoff tool should be removed"


if __name__ == "__main__":

    test_direct_tool_execution()
    test_dynamic_agent_management()
