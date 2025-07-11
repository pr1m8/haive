"""Static supervisor with dynamically updating tools.

Start simple: Fixed graph structure, but tools can be added/removed/updated
using model validators to sync after changes.
"""

import asyncio
from datetime import datetime
from typing import Any, Dict, List, Optional, Set

from haive.core.common.models.dynamic_choice_model import DynamicChoiceModel
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.schema import StateSchema
from langchain_core.messages import HumanMessage
from langchain_core.tools import BaseTool, tool
from pydantic import Field, field_validator, model_validator

from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent


class AgentRegistry:
    """Simple registry for agents."""

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

    def unregister(self, name: str):
        """Remove an agent."""
        self.agents.pop(name, None)
        self.metadata.pop(name, None)

    def get_agent(self, name: str) -> Any | None:
        """Get an agent by name."""
        return self.agents.get(name)

    def list_agents(self) -> list[str]:
        """List all registered agents."""
        return list(self.agents.keys())


class SupervisorState(StateSchema):
    """State that validates and syncs tools."""

    messages: list[dict[str, Any]] = Field(default_factory=list)
    available_agents: set[str] = Field(default_factory=set)
    last_sync: datetime | None = Field(default=None)

    @model_validator(mode="after")
    def sync_available_agents(self):
        """Sync available agents after state changes."""
        # This will be called to ensure state stays in sync
        return self


class StaticSupervisorWithDynamicTools(ReactAgent):
    """Static supervisor that can update its tools dynamically."""

    agent_registry: AgentRegistry = Field(default_factory=AgentRegistry)
    agent_choice_model: DynamicChoiceModel | None = Field(default=None)
    _tool_cache: dict[str, BaseTool] = {}

    @model_validator(mode="after")
    def setup_supervisor(self):
        """Initial setup."""
        # Create base tools that are always available
        self._create_base_tools()
        # Sync agent tools
        self._sync_agent_tools()
        return self

    def _create_base_tools(self):
        """Create tools that are always available."""

        @tool
        def list_available_agents() -> list[str]:
            """List all available agents."""
            agents = self.agent_registry.list_agents()
            return agents if agents else ["No agents registered"]

        @tool
        def check_agent_status(agent_name: str) -> dict[str, Any]:
            """Check the status of a specific agent."""
            if agent_name in self.agent_registry.agents:
                metadata = self.agent_registry.metadata.get(agent_name, {})
                return {
                    "name": agent_name,
                    "available": True,
                    "description": metadata.get("description", "No description"),
                    "registered_at": str(metadata.get("registered_at", "Unknown")),
                }
            return {"name": agent_name, "available": False, "error": "Agent not found"}

        # Add base tools to engine
        if hasattr(self, "engine") and self.engine:
            self.engine.tools = [list_available_agents, check_agent_status]

    def _sync_agent_tools(self):
        """Sync tools based on registered agents."""
        if not hasattr(self, "engine") or not self.engine:
            return

        # Remove old agent tools
        base_tool_names = {"list_available_agents", "check_agent_status"}
        self.engine.tools = [
            t
            for t in self.engine.tools
            if t.name in base_tool_names or not t.name.startswith("execute_")
        ]

        # Create new agent execution tools
        new_tools = []
        for agent_name in self.agent_registry.list_agents():
            tool_func = self._create_agent_tool(agent_name)
            new_tools.append(tool_func)

        # Add new tools
        self.engine.tools.extend(new_tools)

        # Update choice model
        self._update_choice_model()

        # Log sync
        for _t in self.engine.tools:
            pass

    def _create_agent_tool(self, agent_name: str) -> BaseTool:
        """Create an execution tool for a specific agent."""
        agent = self.agent_registry.agents[agent_name]
        description = self.agent_registry.metadata[agent_name].get("description", "")

        @tool
        def agent_tool(task: str) -> str:
            f"""Execute {agent_name}: {description}"""
            try:
                # Use asyncio.run since tool is sync but agent is async
                import asyncio

                import nest_asyncio

                nest_asyncio.apply()

                result = asyncio.run(agent.arun(task))
                return f"{agent_name} result: {result}"
            except Exception as e:
                return f"{agent_name} error: {e!s}"

        # Set dynamic name and description
        agent_tool.__name__ = f"execute_{agent_name}"
        agent_tool.__doc__ = f"Execute {agent_name}: {description}"

        return agent_tool

    def _update_choice_model(self):
        """Update the choice model with current agents."""
        agent_names = self.agent_registry.list_agents()
        if agent_names:
            self.agent_choice_model = DynamicChoiceModel.from_choices(
                agent_names,
                name="AvailableAgents",
                description="Currently available agents",
            )

    def register_agent(self, name: str, agent: Any, description: str):
        """Register a new agent and sync tools."""
        self.agent_registry.register(name, agent, description)
        self._sync_agent_tools()

    def unregister_agent(self, name: str):
        """Unregister an agent and sync tools."""
        self.agent_registry.unregister(name)
        self._sync_agent_tools()

    async def arun(self, input_text: str) -> str:
        """Override arun to ensure tools are synced."""
        # Could add periodic sync here if needed
        return await super().arun(input_text)


# Demo the pattern
async def demo_static_dynamic_tools():
    """Demonstrate static supervisor with dynamic tool updates."""
    # Create supervisor first
    supervisor_engine = AugLLMConfig(
        name="supervisor_engine",
        model="gpt-4",
        tools=[],  # Tools will be added dynamically
        system_message="""You are a task supervisor.
Use list_available_agents to see what agents are available.
Use execute_[agent_name] tools to delegate tasks to specific agents.
Always check available agents before trying to execute.""",
    ).create()

    supervisor = StaticSupervisorWithDynamicTools(
        name="supervisor", engine=supervisor_engine
    )

    # Test 1: Try to list agents when none registered
    await supervisor.arun("What agents are available?")

    # Create and register math agent
    @tool
    def add(a: int, b: int) -> int:
        """Add two numbers."""
        return a + b

    math_engine = AugLLMConfig(
        name="math_engine",
        model="gpt-4",
        tools=[add],
        system_message="You are a math helper. Use the add tool for calculations.",
    ).create()

    math_agent = SimpleAgent(name="math_agent", engine=math_engine)

    supervisor.register_agent(
        "math_agent", math_agent, "Handles mathematical calculations"
    )

    # Test 2: List agents after registration
    await supervisor.arun("What agents are available now?")

    # Test 3: Use the math agent
    await supervisor.arun("Calculate 15 + 27")

    # Create and register search agent
    search_engine = AugLLMConfig(
        name="search_engine",
        model="gpt-4",
        system_message="You are a search helper. Simulate searching for information.",
    ).create()

    search_agent = SimpleAgent(name="search_agent", engine=search_engine)

    supervisor.register_agent("search_agent", search_agent, "Searches for information")

    # Test 4: Use multiple agents
    await supervisor.arun("Search for the population of Tokyo and add 1000 to it")

    # Test 5: Unregister an agent
    supervisor.unregister_agent("math_agent")

    await supervisor.arun("What agents are available after removing math agent?")


if __name__ == "__main__":
    # For testing

    # Run the demo
    asyncio.run(demo_static_dynamic_tools())
