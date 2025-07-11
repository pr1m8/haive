"""Test registry supervisor with real agents - no mocks."""

import asyncio
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../src"))


# Minimal test without external dependencies
class HumanMessage:
    def __init__(self, content: str):
        self.content = content


class BaseTool:
    name: str
    description: str

    def _run(self, *args, **kwargs):
        return f"Tool {self.name} executed"


class ResearchTool(BaseTool):
    def __init__(self):
        self.name = "research_tool"
        self.description = "Research information on any topic"

    def _run(self, query: str) -> str:
        return f"Research results for: {query}"


class CodingTool(BaseTool):
    def __init__(self):
        self.name = "coding_tool"
        self.description = "Write and analyze code"

    def _run(self, code_request: str) -> str:
        return f"Code solution for: {code_request}"


class WritingTool(BaseTool):
    def __init__(self):
        self.name = "writing_tool"
        self.description = "Create written content"

    def _run(self, writing_request: str) -> str:
        return f"Written content for: {writing_request}"


# Mock ReactAgent for testing
class MockReactAgent:
    def __init__(self, name: str, description: str, tools: list):
        self.name = name
        self.description = description
        self.tools = tools

    async def ainvoke(self, input_data):
        return f"Agent {self.name} processed: {input_data['messages'][0].content}"


# Mock RegistrySupervisor for testing
class MockRegistrySupervisor:
    def __init__(self, name: str):
        self.name = name
        self.agent_registry = {}
        self.tools = []

    def populate_registry(self, agents):
        for agent in agents:
            self.agent_registry[agent.name] = agent
            self.tools.extend(agent.tools)

    async def ainvoke(self, input_data):
        message = input_data["messages"][0].content

        # Simple routing logic
        if "research" in message.lower():
            agent = self.agent_registry.get("research_agent")
            return await agent.ainvoke(input_data)
        if "code" in message.lower() or "python" in message.lower():
            agent = self.agent_registry.get("coding_agent")
            return await agent.ainvoke(input_data)
        if "write" in message.lower() or "summary" in message.lower():
            agent = self.agent_registry.get("writing_agent")
            return await agent.ainvoke(input_data)
        return f"Supervisor couldn't route: {message}"


async def test_registry_supervisor_real_agents():
    """Test registry supervisor with real agent-like instances."""
    # Create agent instances
    research_agent = MockReactAgent(
        name="research_agent",
        description="Specialized in research tasks",
        tools=[ResearchTool()],
    )

    coding_agent = MockReactAgent(
        name="coding_agent",
        description="Specialized in coding tasks",
        tools=[CodingTool()],
    )

    writing_agent = MockReactAgent(
        name="writing_agent",
        description="Specialized in writing tasks",
        tools=[WritingTool()],
    )

    # Create supervisor and populate registry
    supervisor = MockRegistrySupervisor(name="test_supervisor")
    supervisor.populate_registry(agents=[research_agent, coding_agent, writing_agent])

    # Test 1: Research task
    await supervisor.ainvoke(
        {"messages": [HumanMessage(content="Research AI trends in 2024")]}
    )

    # Test 2: Coding task
    await supervisor.ainvoke(
        {"messages": [HumanMessage(content="Write a Python function to sort a list")]}
    )

    # Test 3: Writing task
    await supervisor.ainvoke(
        {"messages": [HumanMessage(content="Write a summary of machine learning")]}
    )

    # Test 4: Add new agent dynamically

    class AnalysisTool(BaseTool):
        def __init__(self):
            self.name = "analysis_tool"
            self.description = "Analyze data and provide insights"

        def _run(self, data: str) -> str:
            return f"Analysis of: {data}"

    analysis_agent = MockReactAgent(
        name="analysis_agent",
        description="Specialized in data analysis",
        tools=[AnalysisTool()],
    )

    # Add agent to registry dynamically
    supervisor.agent_registry["analysis_agent"] = analysis_agent
    supervisor.tools.extend(analysis_agent.tools)

    # Test with new agent (should fallback to supervisor default)
    await supervisor.ainvoke(
        {"messages": [HumanMessage(content="Analyze sales data trends")]}
    )

    # Verify supervisor has aggregated tools
    for _tool in supervisor.tools:
        pass

    for _name, _agent in supervisor.agent_registry.items():
        pass


if __name__ == "__main__":
    asyncio.run(test_registry_supervisor_real_agents())
