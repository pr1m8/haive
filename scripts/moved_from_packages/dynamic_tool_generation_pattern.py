"""Dynamic supervisor with tool creation from agents and choice model.

This implementation focuses on:
1. Dynamic tool creation from registered agents
2. Dynamic choice model integration
3. Clean supervisor state management
4. Basic handoff/forward tools

No fancy features - just the core dynamic tooling pattern.
"""

from typing import Any

from haive.agents.react.agent import ReactAgent
from haive.core.common.models.dynamic_choice_model import DynamicChoiceModel
from haive.core.schema import StateSchema
from langchain_core.tools import tool
from pydantic import Field, model_validator


class SupervisorState(StateSchema):
    """State for dynamic supervisor with agent registry."""

    current_task: str = Field(default="")
    agent_to_execute: str | None = Field(default=None)
    agent_task: str = Field(default="")
    agent_response: str | None = Field(default=None)
    available_agents: dict[str, str] = Field(default_factory=dict)
    execution_history: list[dict[str, Any]] = Field(default_factory=list)


class AgentRegistry:
    """Simple registry for holding agents."""

    def __init__(self):
        self.agents: dict[str, Any] = {}
        self.descriptions: dict[str, str] = {}

    def register(self, name: str, agent: Any, description: str):
        """Register an agent with description."""
        self.agents[name] = agent
        self.descriptions[name] = description

    def get(self, name: str) -> Any | None:
        """Get agent by name."""
        return self.agents.get(name)

    def list_available(self) -> dict[str, str]:
        """List all available agents with descriptions."""
        return self.descriptions.copy()

    def remove(self, name: str) -> bool:
        """Remove agent from registry."""
        if name in self.agents:
            del self.agents[name]
            del self.descriptions[name]
            return True
        return False


class DynamicSupervisorV2(ReactAgent):
    """Dynamic supervisor with tool creation from agents and choice model."""

    agent_registry: AgentRegistry = Field(default_factory=AgentRegistry)
    agent_choice_model: DynamicChoiceModel | None = Field(default=None)

    @model_validator(mode="after")
    def setup_dynamic_supervisor(self):
        """Set up supervisor with dynamic tool creation."""
        self.agent_choice_model = DynamicChoiceModel(
            model_name="AgentChoice", include_end=True
        )
        self._rebuild_tools()
        return self

    def _rebuild_tools(self):
        """Rebuild all tools based on current registry state."""
        available_agents = self.agent_registry.list_available()
        for existing_name in self.agent_choice_model.option_names:
            if existing_name != "END":
                self.agent_choice_model.remove_option_by_name(existing_name)
        for agent_name in available_agents:
            self.agent_choice_model.add_option(agent_name)
        tools = []
        tools.append(self._create_list_agents_tool())
        tools.append(self._create_choose_agent_tool())
        for agent_name, description in available_agents.items():
            tools.append(self._create_handoff_tool(agent_name, description))
            tools.append(self._create_forward_tool(agent_name, description))
        tools.append(self._create_execution_status_tool())
        for _tool in tools:
            pass
        if hasattr(self, "engine") and self.engine:
            self.engine.tools = [
                t for t in self.engine.tools if not self._is_dynamic_tool(t)
            ]
            self.engine.tools.extend(tools)

    def _is_dynamic_tool(self, tool) -> bool:
        """Check if a tool is dynamically created by supervisor."""
        dynamic_prefixes = [
            "list_agents",
            "choose_agent",
            "handoff_to_",
            "forward_to_",
            "execution_status",
        ]
        return any((tool.name.startswith(prefix) for prefix in dynamic_prefixes))

    def _create_list_agents_tool(self):
        """Create tool to list available agents."""

        @tool
        def list_agents() -> str:
            """List all available agents and their capabilities."""
            available = self.agent_registry.list_available()
            if not available:
                return "No agents currently available"
            result = "Available agents:\n"
            for name, description in available.items():
                result += f"- {name}: {description}\n"
            return result.strip()

        return list_agents

    def _create_choose_agent_tool(self):
        """Create tool that uses dynamic choice model for agent selection."""

        @tool
        def choose_agent(task_description: str, reasoning: str = "") -> str:
            """Make a validated choice about which agent to use for a task.

            Args:
                task_description: Description of the task to be performed
                reasoning: Optional reasoning for the choice

            Returns:
                The chosen agent name and next steps
            """
            try:
                if not self.agent_choice_model:
                    return "Error: No choice model available"
                ChoiceModel = self.agent_choice_model.current_model
                available_options = self.agent_choice_model.option_names
                task_lower = task_description.lower()
                chosen_agent = "END"
                if any(
                    (
                        word in task_lower
                        for word in ["math", "calculate", "add", "multiply", "number"]
                    )
                ):
                    if "math_agent" in available_options:
                        chosen_agent = "math_agent"
                elif any(
                    (
                        word in task_lower
                        for word in ["plan", "schedule", "organize", "steps"]
                    )
                ):
                    if "planning_agent" in available_options:
                        chosen_agent = "planning_agent"
                elif available_options and available_options[0] != "END":
                    chosen_agent = available_options[0]
                validated_choice = ChoiceModel(choice=chosen_agent)
                if validated_choice.choice == "END":
                    return f"Task complete or no suitable agent found. Chosen: {validated_choice.choice}"
                return f"Chosen agent: {validated_choice.choice}. Use handoff_to_{validated_choice.choice} to execute."
            except Exception as e:
                return f"Error choosing agent: {e!s}"

        return choose_agent

    def _create_handoff_tool(self, agent_name: str, description: str):
        """Create handoff tool for specific agent."""

        def handoff_tool(task_description: str) -> str:
            """Hand off a task to agent.

            Args:
                task_description: The task to hand off to the agent

            Returns:
                Result from the agent execution
            """
            try:
                agent = self.agent_registry.get(agent_name)
                if not agent:
                    return f"Error: Agent '{agent_name}' not found in registry"
                result = agent.invoke(
                    {"messages": [{"role": "user", "content": task_description}]}
                )
                if isinstance(result, dict) and "messages" in result:
                    response = result["messages"][-1].get("content", str(result))
                else:
                    response = str(result)
                self.state.execution_history.append(
                    {
                        "agent": agent_name,
                        "task": task_description,
                        "success": True,
                        "response_length": len(response),
                    }
                )
                return f"{agent_name} response: {response}"
            except Exception as e:
                self.state.execution_history.append(
                    {
                        "agent": agent_name,
                        "task": task_description,
                        "success": False,
                        "error": str(e),
                    }
                )
                return f"Error executing {agent_name}: {e!s}"

        handoff_tool.__name__ = f"handoff_to_{agent_name}"
        decorated_tool = tool(handoff_tool)
        decorated_tool.name = f"handoff_to_{agent_name}"
        decorated_tool.description = f"Hand off a task to {agent_name}. {description}"
        return decorated_tool

    def _create_forward_tool(self, agent_name: str, description: str):
        """Create forward tool for specific agent."""

        def forward_tool(message: str, context: str = "") -> str:
            """Forward a message to agent for processing.

            Args:
                message: The message to forward
                context: Optional context for the message

            Returns:
                Formatted response from the agent
            """
            try:
                agent = self.agent_registry.get(agent_name)
                if not agent:
                    return f"Error: Agent '{agent_name}' not found in registry"
                full_message = f"{message}"
                if context:
                    full_message = f"Context: {context}\n\nMessage: {message}"
                result = agent.invoke(
                    {"messages": [{"role": "user", "content": full_message}]}
                )
                if isinstance(result, dict) and "messages" in result:
                    response = result["messages"][-1].get("content", str(result))
                else:
                    response = str(result)
                return f"Forwarded to {agent_name}: {response}"
            except Exception as e:
                return f"Error forwarding to {agent_name}: {e!s}"

        forward_tool.__name__ = f"forward_to_{agent_name}"
        return tool(
            name=f"forward_to_{agent_name}",
            description=f"Forward a message to {agent_name} for processing. {description}",
        )(forward_tool)

    def _create_execution_status_tool(self):
        """Create tool for checking execution status."""

        @tool
        def execution_status() -> str:
            """Get current execution status and history."""
            if not self.state.execution_history:
                return "No execution history available"
            status_lines = ["Execution History:"]
            for i, record in enumerate(self.state.execution_history[-5:], 1):
                agent = record.get("agent", "unknown")
                success = "✅" if record.get("success", False) else "❌"
                status_lines.append(f"{i}. {success} {agent}")
            return "\n".join(status_lines)

        return execution_status

    def add_agent(self, name: str, agent: Any, description: str):
        """Add agent to registry and rebuild tools."""
        self.agent_registry.register(name, agent, description)
        self._rebuild_tools()
        self.state.available_agents = self.agent_registry.list_available()

    def remove_agent(self, name: str) -> bool:
        """Remove agent from registry and rebuild tools."""
        if self.agent_registry.remove(name):
            self._rebuild_tools()
            self.state.available_agents = self.agent_registry.list_available()
            return True
        return False
