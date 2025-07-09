"""
Test dynamic tool updates with a working supervisor.

This creates a minimal working example that can actually run.
"""

import asyncio
from datetime import datetime
from typing import Any, Dict, List, Optional

from langchain_core.tools import tool
from pydantic import Field, model_validator


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
        self.agents: Dict[str, MockAgent] = {}
        self.tools: Dict[str, Any] = {}
        self._create_base_tools()
        self._sync_count = 0

    def _create_base_tools(self):
        """Create base tools that are always available."""

        @tool
        def list_agents() -> List[str]:
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
        def sync_status() -> Dict[str, Any]:
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
        else:
            return tool_func.invoke({})

    def get_tool_descriptions(self) -> Dict[str, str]:
        """Get all tool names and descriptions."""
        descriptions = {}
        for name, tool_func in self.tools.items():
            descriptions[name] = tool_func.description or "No description"
        return descriptions


# Test the dynamic tools
def test_dynamic_tools():
    """Test dynamic tool registration and execution."""

    print("=== Testing Dynamic Tool Updates ===\n")

    # Create supervisor
    supervisor = DynamicToolSupervisor()

    # Test 1: Initial state
    print("1. Initial state:")
    print(f"   Tools: {list(supervisor.tools.keys())}")
    result = supervisor.execute_tool("list_agents")
    print(f"   Agents: {result}\n")

    # Test 2: Register first agent
    print("2. Register math agent:")
    msg = supervisor.register_agent("math_agent", "mathematical calculations")
    print(f"   {msg}")
    print(f"   Tools: {list(supervisor.tools.keys())}")
    result = supervisor.execute_tool("list_agents")
    print(f"   Agents: {result}\n")

    # Test 3: Execute math agent
    print("3. Execute math agent:")
    result = supervisor.execute_tool("execute_math_agent", "calculate 5 + 3")
    print(f"   Result: {result}\n")

    # Test 4: Register more agents
    print("4. Register search and writer agents:")
    supervisor.register_agent("search_agent", "web searching")
    supervisor.register_agent("writer_agent", "content writing")
    print(f"   Tools: {list(supervisor.tools.keys())}")
    result = supervisor.execute_tool("agent_count")
    print(f"   Agent count: {result}\n")

    # Test 5: Get sync status
    print("5. Check sync status:")
    result = supervisor.execute_tool("sync_status")
    print(f"   Status: {result}\n")

    # Test 6: Execute multiple agents
    print("6. Execute multiple agents:")
    for agent_name in ["math_agent", "search_agent", "writer_agent"]:
        tool_name = f"execute_{agent_name}"
        result = supervisor.execute_tool(tool_name, "do something")
        print(f"   {tool_name}: {result}")
    print()

    # Test 7: Unregister an agent
    print("7. Unregister math agent:")
    msg = supervisor.unregister_agent("math_agent")
    print(f"   {msg}")
    print(f"   Remaining tools: {list(supervisor.tools.keys())}\n")

    # Test 8: Try to execute unregistered agent
    print("8. Try to execute unregistered agent:")
    result = supervisor.execute_tool("execute_math_agent", {"task": "calculate"})
    print(f"   Result: {result}\n")

    # Test 9: Get all tool descriptions
    print("9. All tool descriptions:")
    descriptions = supervisor.get_tool_descriptions()
    for name, desc in descriptions.items():
        print(f"   {name}: {desc}")

    print("\n✅ Dynamic tool test complete!")
    print(
        f"   Final state: {len(supervisor.agents)} agents, {len(supervisor.tools)} tools"
    )


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

    def get_validation_report(self) -> Dict[str, Any]:
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

    print("\n=== Testing Validated Dynamic Supervisor ===\n")

    supervisor = ValidatedDynamicSupervisor()

    # Add agents
    supervisor.register_agent("agent1", "capability1")
    supervisor.register_agent("agent2", "capability2")

    print("After registration:")
    report = supervisor.get_validation_report()
    print(f"  Validation: {report}\n")

    # Manually break sync (simulate error)
    print("Simulating sync error (removing agent without tool):")
    del supervisor.agents["agent1"]  # Remove agent but not tool
    supervisor.validate_state()
    report = supervisor.get_validation_report()
    print(f"  Validation: {report}\n")

    # Fix by removing orphaned tool
    print("Fixing by removing orphaned tool:")
    del supervisor.tools["execute_agent1"]
    supervisor.validate_state()
    report = supervisor.get_validation_report()
    print(f"  Validation: {report}\n")

    print("✅ Validation test complete!")


if __name__ == "__main__":
    # Run both tests
    test_dynamic_tools()
    test_validated_supervisor()
