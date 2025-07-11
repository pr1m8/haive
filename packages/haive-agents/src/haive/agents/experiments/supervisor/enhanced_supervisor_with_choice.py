#!/usr/bin/env python3
"""Enhanced supervisor using DynamicChoiceModel for structured decision making."""

from typing import Any

from haive.core.common.models.dynamic_choice_model import DynamicChoiceModel
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from pydantic import Field, model_validator

from haive.agents.experiments.supervisor.test_registry_setup import AgentRegistry
from haive.agents.experiments.supervisor.test_route_tools import (
    create_list_agents_tool,
    create_route_tools,
)
from haive.agents.react.agent import ReactAgent


class EnhancedSupervisorWithChoice(ReactAgent):
    """Enhanced supervisor that uses DynamicChoiceModel for structured agent selection."""

    # Core components
    agent_registry: AgentRegistry = Field(
        default_factory=AgentRegistry,
        description="Registry containing available agents",
    )

    agent_choice_model: DynamicChoiceModel = Field(
        default_factory=lambda: DynamicChoiceModel(
            model_name="AgentChoice", include_end=True
        ),
        description="Dynamic choice model for agent selection",
    )

    @model_validator(mode="after")
    def setup_enhanced_supervisor(self) -> "EnhancedSupervisorWithChoice":
        """Setup supervisor with choice model + route tools."""
        # Update choice model with available agents
        self._sync_choice_model_with_registry()

        # Create tools
        route_tools = create_route_tools(self.agent_registry)
        list_tool = create_list_agents_tool(self.agent_registry)
        choice_tool = self._create_agent_choice_tool()

        all_tools = [*route_tools, list_tool, choice_tool]

        for _tool in all_tools:
            pass

        # Create enhanced supervisor engine
        supervisor_engine = AugLLMConfig(
            name="enhanced_supervisor_engine",
            tools=all_tools,
            system_message="""You are an enhanced supervisor that routes tasks to specialized agents using structured decision making.

Available tools:
- list_agents: See what agents are available
- choose_agent: Make a structured decision about which agent to use (validates choice)
- route_to_X: Execute the task with the chosen agent

WORKFLOW:
1. First, use list_agents to see what's available
2. Use choose_agent to make a validated decision about which agent to use
3. Use route_to_X to execute the task with the chosen agent

Always follow this structured workflow for clear decision making.""",
        )

        # Set engine for ReactAgent
        self.engine = supervisor_engine
        self.engines["main"] = supervisor_engine

        return self

    def _sync_choice_model_with_registry(self) -> None:
        """Sync choice model options with available agents in registry."""
        available_agents = self.agent_registry.list_available()

        # Add each agent as an option to the choice model
        for agent_name in available_agents:
            self.agent_choice_model.add_option(agent_name)

    def _create_agent_choice_tool(self):
        """Create tool that uses DynamicChoiceModel for structured agent selection."""

        @tool
        def choose_agent(task_description: str, reasoning: str = "") -> str:
            """Make a structured, validated choice about which agent to use for a task.

            Args:
                task_description: Description of the task to be performed
                reasoning: Optional reasoning for the choice

            Returns:
                The name of the chosen agent (validated against available options)
            """
            try:

                # Get current choice model
                ChoiceModel = self.agent_choice_model.current_model
                available_options = self.agent_choice_model.option_names

                # For now, use simple heuristics to choose
                # In a real implementation, this could use LLM reasoning
                task_lower = task_description.lower()

                chosen_agent = "END"  # Default fallback

                if any(
                    word in task_lower
                    for word in ["math", "calculate", "add", "multiply", "number"]
                ):
                    if "math_agent" in available_options:
                        chosen_agent = "math_agent"
                elif any(
                    word in task_lower
                    for word in ["plan", "schedule", "organize", "steps"]
                ):
                    if "planning_agent" in available_options:
                        chosen_agent = "planning_agent"
                elif available_options and available_options[0] != "END":
                    # Pick first non-END option as fallback
                    chosen_agent = available_options[0]

                # Validate choice using the dynamic model
                try:
                    validated_choice = ChoiceModel(choice=chosen_agent)

                    if reasoning:
                        return f"Chosen agent: {validated_choice.choice} (Reasoning: {reasoning})"
                    return f"Chosen agent: {validated_choice.choice}"

                except Exception:
                    # Fall back to END
                    fallback_choice = ChoiceModel(choice="END")
                    return (
                        f"Chosen agent: {fallback_choice.choice} (validation fallback)"
                    )

            except Exception as e:
                return f"Error choosing agent: {e!s}"

        return choose_agent

    def add_agent_to_registry(self, name: str, agent: Any, description: str) -> None:
        """Add agent to registry and sync choice model."""
        self.agent_registry.register(name, agent, description)
        self.agent_choice_model.add_option(name)

    def remove_agent_from_registry(self, name: str) -> bool:
        """Remove agent from registry and choice model."""
        # Remove from choice model first
        removed_from_choice = self.agent_choice_model.remove_option_by_name(name)

        # Remove from registry (would need to implement this)
        # For now, just report
        return removed_from_choice


def test_enhanced_supervisor():
    """Test the enhanced supervisor with choice model."""
    # Import here to avoid circular imports
    from haive.agents.experiments.supervisor.test_registry_setup import (
        create_test_agents,
    )

    # Create registry with agents
    registry = AgentRegistry()
    agents = create_test_agents()
    registry.register(
        "math_agent", agents["math_agent"], "Performs mathematical calculations"
    )
    registry.register(
        "planning_agent", agents["planning_agent"], "Creates structured plans"
    )

    # Create enhanced supervisor
    supervisor = EnhancedSupervisorWithChoice(
        name="enhanced_supervisor", agent_registry=registry
    )

    # Test choice model directly
    supervisor.agent_choice_model.test_model("math_agent")

    # Test supervisor workflow
    try:
        supervisor.invoke({"messages": [HumanMessage("I need to calculate 15 * 7")]})

    except Exception:
        pass

    return supervisor


if __name__ == "__main__":
    supervisor = test_enhanced_supervisor()
