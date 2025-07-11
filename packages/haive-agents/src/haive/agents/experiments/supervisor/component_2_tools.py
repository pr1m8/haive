"""Component 2: Tool generation from state.agents with choice model integration."""

from typing import Dict, List, Optional, Set

from haive.core.common.models.dynamic_choice_model import DynamicChoiceModel
from langchain_core.tools import tool
from pydantic import Field, field_validator, model_validator

from haive.agents.experiments.supervisor.supervisor_state import SupervisorState


class SupervisorStateWithTools(SupervisorState):
    """SupervisorState with dynamic tool generation and choice model integration."""

    # Choice model for validation
    agent_choice_model: DynamicChoiceModel = Field(
        default_factory=lambda: DynamicChoiceModel(
            model_name="AgentChoice", include_end=True
        ),
        description="Dynamic choice model for agent selection validation",
    )

    # Generated tools (for tracking)
    generated_tools: list[str] = Field(
        default_factory=list, description="Names of tools generated from agents"
    )

    # Enable validation on assignment and allow arbitrary types
    model_config = {"validate_assignment": True, "arbitrary_types_allowed": True}

    @model_validator(mode="after")
    def sync_choice_model_and_tools(self):
        """Sync choice model with agents and generate tools."""
        # Update choice model with available agents
        self._update_choice_model()

        # Generate tools from agents
        self._generate_tools_from_agents()

        return self

    def _update_choice_model(self):
        """Update choice model with current agents."""
        # Remove existing agent options (keep END)
        current_options = self.agent_choice_model.option_names.copy()
        for option in current_options:
            if option != "END":
                self.agent_choice_model.remove_option_by_name(option)

        # Add current agents
        for agent_name in self.agents:
            self.agent_choice_model.add_option(agent_name)

    def _generate_tools_from_agents(self):
        """Generate tools from current agents."""
        self.generated_tools.clear()

        # Create handoff tools for each agent
        for agent_name, _agent_info in self.agents.items():
            tool_name = f"handoff_to_{agent_name}"
            self.generated_tools.append(tool_name)

        # Add choice validation tool
        choice_tool_name = "choose_agent"
        self.generated_tools.append(choice_tool_name)

    @model_validator(mode="after")
    def validate_agent_routing(self):
        """Validate agent routing after all fields are set."""
        # Validate next_agent exists in registry
        if self.next_agent is not None and self.next_agent != "END":
            if self.next_agent not in self.agents:
                available = [*list(self.agents.keys()), "END"]
                raise ValueError(
                    f"Agent '{self.next_agent}' not found in registry. Available: {available}"
                )

        return self

    def create_handoff_tool(self, agent_name: str):
        """Create a handoff tool for a specific agent."""
        agent_info = self.agents[agent_name]

        def handoff_tool(task_description: str) -> str:
            """Hand off a task to the specified agent."""
            try:
                # Set routing in state
                self.set_routing(agent_name, task_description)

                # Get agent and execute (for now, just return routing info)
                agent_info.get_agent()
                return f"Task routed to {agent_name}: {task_description}"

            except Exception as e:
                return f"Error routing to {agent_name}: {e!s}"

        # Create tool with proper name and description
        handoff_tool.__name__ = f"handoff_to_{agent_name}"
        decorated_tool = tool(
            description=f"Hand off a task to {agent_name}. {agent_info.description}"
        )(handoff_tool)
        decorated_tool.name = f"handoff_to_{agent_name}"
        return decorated_tool

    def create_choice_tool(self):
        """Create agent choice validation tool."""

        def choose_agent(task_description: str, reasoning: str = "") -> str:
            """Choose which agent should handle a task using validated selection."""
            try:

                # Simple heuristic-based selection
                task_lower = task_description.lower()
                chosen_agent = "END"

                # Basic keyword matching
                if any(
                    word in task_lower
                    for word in ["search", "find", "research", "look up"]
                ):
                    if "search_agent" in self.agents:
                        chosen_agent = "search_agent"
                elif any(
                    word in task_lower
                    for word in ["math", "calculate", "add", "multiply"]
                ):
                    if "math_agent" in self.agents:
                        chosen_agent = "math_agent"
                elif any(word in task_lower for word in ["plan", "organize", "steps"]):
                    if "planning_agent" in self.agents:
                        chosen_agent = "planning_agent"
                elif self.active_agents:
                    # Fallback to first active agent
                    chosen_agent = next(iter(self.active_agents))

                # Validate choice using choice model
                ChoiceModel = self.agent_choice_model.current_model
                validated_choice = ChoiceModel(choice=chosen_agent)

                result = f"Chosen agent: {validated_choice.choice}"
                if validated_choice.choice != "END":
                    result += f"\nNext: Use handoff_to_{validated_choice.choice} to execute the task"

                return result

            except Exception as e:
                return f"Error choosing agent: {e!s}"

        return tool(
            choose_agent,
            description="Choose which agent should handle a task using validated selection",
        )

    def get_all_tools(self):
        """Get all generated tools as actual tool objects."""
        tools = []

        # Create handoff tools for each agent
        for agent_name in self.agents:
            handoff_tool = self.create_handoff_tool(agent_name)
            tools.append(handoff_tool)

        # Add choice tool
        choice_tool = self.create_choice_tool()
        tools.append(choice_tool)

        return tools

    def add_agent(self, name: str, agent: any, description: str, active: bool = True):
        """Override to trigger tool regeneration."""
        # Call parent method
        super().add_agent(name, agent, description, active)

        # Regenerate tools and choice model
        self._update_choice_model()
        self._generate_tools_from_agents()

    def remove_agent(self, name: str) -> bool:
        """Override to trigger tool regeneration."""
        # Call parent method
        result = super().remove_agent(name)

        if result:
            # Regenerate tools and choice model
            self._update_choice_model()
            self._generate_tools_from_agents()

        return result

    def sync_agents(self):
        """Sync agents with choice model and regenerate tools."""
        self._update_choice_model()
        self._generate_tools_from_agents()
