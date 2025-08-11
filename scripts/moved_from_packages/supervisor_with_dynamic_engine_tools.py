"""Supervisor with dynamically updating tools via engine.

Key insight: The tool node gets tools from the engine by name at runtime,
so we just need to update the engine's tools and they'll be used automatically!
"""

import asyncio
from datetime import datetime
from typing import Any

from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent
from haive.core.common.models.dynamic_choice_model import DynamicChoiceModel
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.tools import BaseTool, tool
from pydantic import Field, model_validator


class AgentRegistry:
    """Registry for managing agents."""

    def __init__(self):
        self.agents: dict[str, Any] = {}
        self.metadata: dict[str, dict[str, Any]] = {}

    def register(self, name: str, agent: Any, description: str):
        """Register an agent."""
        self.agents[name] = agent
        self.metadata[name] = {
            "description": description,
            "registered_at": datetime.now(),
        }

    def get_agent(self, name: str) -> Any | None:
        """Get an agent by name."""
        return self.agents.get(name)

    def list_agents(self) -> list[str]:
        """List all registered agents."""
        return list(self.agents.keys())


class DynamicToolSupervisor(ReactAgent):
    """Supervisor that dynamically updates its tools by modifying the engine.

    Since the tool node gets tools from the engine by name, we can update
    the engine's tools list and the tool node will automatically use them!
    """

    agent_registry: AgentRegistry = Field(default_factory=AgentRegistry)
    agent_choice_model: DynamicChoiceModel | None = Field(default=None)

    @model_validator(mode="after")
    def setup_supervisor(self):
        """Setup supervisor and sync initial tools."""
        self._create_base_tools()
        self._sync_tools_to_engine()
        return self

    def _create_base_tools(self) -> list[BaseTool]:
        """Create tools that are always available."""
        base_tools = []

        @tool
        def list_available_agents() -> list[str]:
            """List all available agents and their descriptions."""
            if not self.agent_registry.agents:
                return ["No agents registered"]
            agents = []
            for name, _agent in self.agent_registry.agents.items():
                desc = self.agent_registry.metadata[name].get(
                    "description", "No description"
                )
                agents.append(f"{name}: {desc}")
            return agents

        @tool
        def check_agent_capability(agent_name: str) -> dict[str, Any]:
            """Check what an agent can do."""
            if agent_name not in self.agent_registry.agents:
                return {"error": f"Agent {agent_name} not found"}
            metadata = self.agent_registry.metadata.get(agent_name, {})
            return {
                "name": agent_name,
                "description": metadata.get("description", "No description"),
                "available": True,
            }

        base_tools.extend([list_available_agents, check_agent_capability])
        return base_tools

    def _create_agent_execution_tool(self, agent_name: str) -> BaseTool:
        """Create a tool to execute a specific agent."""
        agent = self.agent_registry.agents[agent_name]
        description = self.agent_registry.metadata[agent_name].get("description", "")

        @tool
        def execute_agent(task: str) -> str:
            f"Execute {agent_name} to handle: {description}"
            try:
                import nest_asyncio

                nest_asyncio.apply()
                result = asyncio.run(agent.arun(task))
                return f"{agent_name} completed: {result}"
            except Exception as e:
                return f"{agent_name} error: {e!s}"

        execute_agent.__name__ = f"execute_{agent_name}"
        execute_agent.__doc__ = f"Execute {agent_name} to handle: {description}"
        return execute_agent

    def _sync_tools_to_engine(self):
        """Sync all tools to the engine - this is the key!"""
        if not self.engine:
            return
        all_tools = self._create_base_tools()
        for agent_name in self.agent_registry.list_agents():
            agent_tool = self._create_agent_execution_tool(agent_name)
            all_tools.append(agent_tool)
        self.engine.tools = all_tools
        self._update_choice_model()
        for _tool in all_tools:
            pass

    def _update_choice_model(self):
        """Update the choice model with current agents."""
        agent_names = self.agent_registry.list_agents()
        if agent_names:
            self.agent_choice_model = DynamicChoiceModel.from_choices(
                agent_names,
                name="AgentSelection",
                description="Available agents to execute",
            )

    def register_agent(self, name: str, agent: Any, description: str):
        """Register a new agent and update tools."""
        self.agent_registry.register(name, agent, description)
        self._sync_tools_to_engine()

    def unregister_agent(self, name: str):
        """Unregister an agent and update tools."""
        if name in self.agent_registry.agents:
            del self.agent_registry.agents[name]
            del self.agent_registry.metadata[name]
            self._sync_tools_to_engine()


async def test_dynamic_engine_tools():
    """Test supervisor with dynamic tool updates via engine."""
    supervisor_engine = AugLLMConfig(
        name="supervisor_engine",
        model="gpt-4",
        tools=[],
        system_message="You are a task supervisor that manages other agents.\n\nAvailable tools:\n- list_available_agents: See what agents are registered\n- check_agent_capability: Check what a specific agent can do\n- execute_[agent_name]: Execute a specific agent (tools added dynamically)\n\nAlways check available agents before trying to execute tasks.",
    ).create()
    supervisor = DynamicToolSupervisor(
        name="dynamic_supervisor", engine=supervisor_engine
    )
    await supervisor.arun("What agents are available?")

    @tool
    def calculate(expression: str) -> str:
        """Calculate a mathematical expression."""
        try:
            return str(eval(expression))
        except:
            return "Invalid expression"

    math_engine = AugLLMConfig(
        name="math_engine",
        model="gpt-4",
        tools=[calculate],
        system_message="You are a math assistant. Use the calculate tool for computations.",
    ).create()
    math_agent = SimpleAgent(name="math_agent", engine=math_engine)
    supervisor.register_agent(
        "math_agent", math_agent, "Mathematical calculations and computations"
    )
    await supervisor.arun("Calculate 15 * 4 + 10")
    search_engine = AugLLMConfig(
        name="search_engine",
        model="gpt-4",
        system_message="You are a search assistant. Simulate searching for information and return relevant results.",
    ).create()
    search_agent = SimpleAgent(name="search_agent", engine=search_engine)
    supervisor.register_agent(
        "search_agent", search_agent, "Information search and research"
    )
    await supervisor.arun(
        "Search for the height of Mount Everest in meters, then calculate how many feet that is (1 meter = 3.28084 feet)"
    )
    supervisor.unregister_agent("math_agent")
    await supervisor.arun("Calculate 5 + 5")


if __name__ == "__main__":
    engine = AugLLMConfig(name="test_engine", model="gpt-4", tools=[]).create()
    supervisor = DynamicToolSupervisor(name="test_supervisor", engine=engine)
    mock_agent = SimpleAgent(name="mock_agent")
    supervisor.register_agent("mock_agent", mock_agent, "Mock agent for testing")
