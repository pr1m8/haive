"""Test dynamic tool updates with a working supervisor.

This creates a minimal working example that can actually run.
"""

import asyncio
from datetime import datetime
from typing import Any

from langchain_core.tools import tool


class MockAgent:
    """Mock agent for testing without full Haive dependencies."""

    def __init__(self, name: str, capability: str):
        self.name = name
        self.capability = capability

    async def arun(self, task: str) -> str:
        """Simulate agent execution."""
        await asyncio.sleep(0.1)  # Simulate work
        return f"{self.name} processed '{task}' using {self.capability}"


class DynamicToolSupervisor:
    """Supervisor that can dynamically update its tools."""

    def __init__(self):
        self.agents: dict[str, MockAgent] = {}
        self.tools: dict[str, Any] = {}
        self._create_base_tools()
        self._sync_count = 0

    def _create_base_tools(self):
        """Create base tools that are always available."""

        @tool
        def list_agents() -> list[str]:
            """List all registered agents."""
            if not self.agents:
                return ["No agents registered"]
            return [
                f"{name} ({agent.capability})" for name, agent in self.agents.items()
            ]

        @tool
        def agent_count() -> int:
            """Get the number of registered agents."""
            return len(self.agents)

        @tool
        def sync_status() -> dict[str, Any]:
            """Get sync status information."""
            return {
                "total_agents": len(self.agents),
                "total_tools": len(self.tools),
                "sync_count": self._sync_count,
                "last_sync": datetime.now().isoformat(),
            }

        # Store base tools
        self.tools = {
            "list_agents": list_agents,
            "agent_count": agent_count,
            "sync_status": sync_status,
        }

    def register_agent(self, name: str, capability: str) -> str:
        """Register a new agent and create its tool."""
        # Create mock agent
        agent = MockAgent(name, capability)
        self.agents[name] = agent

        # Create execution tool for this agent
        @tool
        def execute_agent(task: str) -> str:
            f"""Execute {name} for: {capability}"""
            # Run async agent in sync context
            import nest_asyncio

            nest_asyncio.apply()
            result = asyncio.run(agent.arun(task))
            return result

        # Set dynamic name
        execute_agent.__name__ = f"execute_{name}"
        execute_agent.__doc__ = f"Execute {name} for: {capability}"

        # Add to tools
        self.tools[f"execute_{name}"] = execute_agent

        # Increment sync count
        self._sync_count += 1

        return f"Registered {name} with {len(self.tools)} total tools"

    def unregister_agent(self, name: str) -> str:
        """Remove an agent and its tool."""
        if name not in self.agents:
            return f"Agent {name} not found"

        # Remove agent
        del self.agents[name]

        # Remove tool
        tool_name = f"execute_{name}"
        if tool_name in self.tools:
            del self.tools[tool_name]

        self._sync_count += 1

        return f"Unregistered {name}, {len(self.tools)} tools remain"

    def execute_tool(self, tool_name: str, input_data: Any = None) -> Any:
        """Execute a tool by name."""
        if tool_name not in self.tools:
            return f"Tool {tool_name} not found. Available: {list(self.tools.keys())}"

        tool_func = self.tools[tool_name]
        # Handle tools that need input vs those that don't
        if input_data is not None:
            return tool_func.invoke(input_data)
        return tool_func.invoke({})

    def get_tool_descriptions(self) -> dict[str, str]:
        """Get all tool names and descriptions."""
        descriptions = {}
        for name, tool_func in self.tools.items():
            descriptions[name] = tool_func.description or "No description"
        return descriptions


# Test the dynamic tools
def test_dynamic_tools():
    """Test dynamic tool registration and execution."""
    # Create supervisor
    supervisor = DynamicToolSupervisor()

    # Test 1: Initial state
    supervisor.execute_tool("list_agents")

    # Test 2: Register first agent
    supervisor.register_agent("math_agent", "mathematical calculations")
    supervisor.execute_tool("list_agents")

    # Test 3: Execute math agent
    supervisor.execute_tool("execute_math_agent", "calculate 5 + 3")

    # Test 4: Register more agents
    supervisor.register_agent("search_agent", "web searching")
    supervisor.register_agent("writer_agent", "content writing")
    supervisor.execute_tool("agent_count")

    # Test 5: Get sync status
    supervisor.execute_tool("sync_status")

    # Test 6: Execute multiple agents
    for agent_name in ["math_agent", "search_agent", "writer_agent"]:
        tool_name = f"execute_{agent_name}"
        supervisor.execute_tool(tool_name, "do something")

    # Test 7: Unregister an agent
    supervisor.unregister_agent("math_agent")

    # Test 8: Try to execute unregistered agent
    supervisor.execute_tool("execute_math_agent", {"task": "calculate"})

    # Test 9: Get all tool descriptions
    descriptions = supervisor.get_tool_descriptions()
    for _name, _desc in descriptions.items():
        pass


# Test with state validation
class ValidatedDynamicSupervisor(DynamicToolSupervisor):
    """Enhanced supervisor with state validation."""

    def __init__(self):
        super().__init__()
        self.state_valid = True
        self.validation_errors = []

    def validate_state(self) -> bool:
        """Validate that tools and agents are in sync."""
        self.validation_errors = []

        # Check each agent has a tool
        for agent_name in self.agents:
            tool_name = f"execute_{agent_name}"
            if tool_name not in self.tools:
                self.validation_errors.append(f"Missing tool for agent: {agent_name}")

        # Check each execute tool has an agent
        for tool_name in self.tools:
            if tool_name.startswith("execute_"):
                agent_name = tool_name[8:]  # Remove "execute_" prefix
                if agent_name not in self.agents:
                    self.validation_errors.append(f"Tool without agent: {tool_name}")

        self.state_valid = len(self.validation_errors) == 0
        return self.state_valid

    def register_agent(self, name: str, capability: str) -> str:
        """Register with validation."""
        result = super().register_agent(name, capability)
        self.validate_state()
        return result

    def unregister_agent(self, name: str) -> str:
        """Unregister with validation."""
        result = super().unregister_agent(name)
        self.validate_state()
        return result

    def get_validation_report(self) -> dict[str, Any]:
        """Get validation status report."""
        return {
            "valid": self.state_valid,
            "errors": self.validation_errors,
            "agent_count": len(self.agents),
            "tool_count": len(self.tools),
            "execute_tool_count": sum(
                1 for t in self.tools if t.startswith("execute_")
            ),
        }


def test_validated_supervisor():
    """Test supervisor with state validation."""
    supervisor = ValidatedDynamicSupervisor()

    # Add agents
    supervisor.register_agent("agent1", "capability1")
    supervisor.register_agent("agent2", "capability2")

    supervisor.get_validation_report()

    # Manually break sync (simulate error)
    del supervisor.agents["agent1"]  # Remove agent but not tool
    supervisor.validate_state()
    supervisor.get_validation_report()

    # Fix by removing orphaned tool
    del supervisor.tools["execute_agent1"]
    supervisor.validate_state()
    supervisor.get_validation_report()


if __name__ == "__main__":
    # Run both tests
    test_dynamic_tools()
    test_validated_supervisor()
