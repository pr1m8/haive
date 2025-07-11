#!/usr/bin/env python3
"""Integrated supervisor using DynamicChoiceModel + proper handoff/forward tools."""

from typing import Any, List

from haive.core.common.models.dynamic_choice_model import DynamicChoiceModel
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph_supervisor import create_forward_message_tool, create_handoff_tool
from pydantic import Field, model_validator

from haive.agents.experiments.supervisor.test_registry_setup import AgentRegistry
from haive.agents.react.agent import ReactAgent


class IntegratedSupervisorWithHandoff(ReactAgent):
    """Integrated supervisor using DynamicChoiceModel + langgraph_supervisor handoff tools."""

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
    def setup_integrated_supervisor(self) -> "IntegratedSupervisorWithHandoff":
        """Setup supervisor with choice model + proper handoff/forward tools."""

        # Update choice model with available agents
        self._sync_choice_model_with_registry()

        # Create tools
        handoff_tools = self._create_handoff_tools()
        forward_tool = create_forward_message_tool("supervisor")
        choice_tool = self._create_agent_choice_tool()
        list_tool = self._create_list_agents_tool()

        all_tools = [*handoff_tools, forward_tool, choice_tool, list_tool]

        for tool in all_tools:
            pass

        # Create integrated supervisor engine
        supervisor_engine = AugLLMConfig(
            name="integrated_supervisor_engine",
            tools=all_tools,
            system_message="""You are an integrated supervisor that routes tasks to specialized agents using proper handoff mechanisms.

WORKFLOW:
1. Use list_agents to see available agents
2. Use choose_agent to make a structured decision about which agent to use
3. Use transfer_to_<agent_name> to handoff control to the chosen agent
4. Use forward_message to relay agent responses back to the user

Tools available:
- list_agents: Show available agents and their capabilities
- choose_agent: Make a validated choice about which agent to use
- transfer_to_X: Handoff control to agent X (proper LangGraph handoff)
- forward_message: Forward agent responses to user

Always follow this structured workflow for proper agent coordination.""",
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

    def _create_handoff_tools(self) -> list[Any]:
        """Create proper handoff tools for each agent using langgraph_supervisor."""
        handoff_tools = []

        available_agents = self.agent_registry.list_available()

        for agent_name, description in available_agents.items():
            # Create proper handoff tool
            handoff_tool = create_handoff_tool(
                agent_name=agent_name,
                description=f"Transfer control to {agent_name}: {description}",
            )
            handoff_tools.append(handoff_tool)

        return handoff_tools

    def _create_agent_choice_tool(self):
        """Create tool that uses DynamicChoiceModel for structured agent selection."""

        @tool
        def choose_agent(task_description: str, reasoning: str = "") -> str:
            """Make a structured, validated choice about which agent to use for a task.

            This tool uses the DynamicChoiceModel to ensure the chosen agent exists.
            After calling this, use transfer_to_<agent_name> to actually handoff control.

            Args:
                task_description: Description of the task to be performed
                reasoning: Optional reasoning for the choice

            Returns:
                The name of the chosen agent (validated) and next steps
            """
            try:

                # Get current choice model
                ChoiceModel = self.agent_choice_model.current_model
                available_options = self.agent_choice_model.option_names


                # Simple heuristics for agent selection
                task_lower = task_description.lower()

                chosen_agent = "END"  # Default fallback

                if any(
                    word in task_lower
                    for word in [
                        "math",
                        "calculate",
                        "add",
                        "multiply",
                        "number",
                        "*",
                        "+",
                        "-",
                        "/",
                    ]
                ):
                    if "math_agent" in available_options:
                        chosen_agent = "math_agent"
                elif any(
                    word in task_lower
                    for word in ["plan", "schedule", "organize", "steps", "strategy"]
                ):
                    if "planning_agent" in available_options:
                        chosen_agent = "planning_agent"
                elif available_options and available_options[0] != "END":
                    # Pick first non-END option as fallback
                    chosen_agent = available_options[0]

                # Validate choice using the dynamic model
                try:
                    validated_choice = ChoiceModel(choice=chosen_agent)

                    if validated_choice.choice == "END":
                        return f"Task complete or no suitable agent found. Chosen: {validated_choice.choice}"
                    return f"Chosen agent: {validated_choice.choice}. Next: Use transfer_to_{validated_choice.choice} to handoff control."

                except Exception as validation_error:
                    # Fall back to END
                    fallback_choice = ChoiceModel(choice="END")
                    return f"Validation failed, ending task. Chosen: {fallback_choice.choice}"

            except Exception as e:
                return f"Error choosing agent: {e!s}"

        return choose_agent

    def _create_list_agents_tool(self):
        """Create tool to list available agents."""

        @tool
        def list_agents() -> str:
            """List all available agents and their capabilities."""
            available = self.agent_registry.list_available()
            if not available:
                return "No agents currently available"

            result = "Available agents:\\n"
            for name, desc in available.items():
                result += f"- {name}: {desc}\\n"
            return result

        return list_agents

    def add_agent_to_registry(self, name: str, agent: Any, description: str) -> None:
        """Add agent to registry and sync choice model + create handoff tool."""
        self.agent_registry.register(name, agent, description)
        self.agent_choice_model.add_option(name)

        # Create new handoff tool for this agent
        new_handoff_tool = create_handoff_tool(
            agent_name=name, description=f"Transfer control to {name}: {description}"
        )

        # Add to engine tools (this is the dynamic part!)
        if self.engine and hasattr(self.engine, "tools"):
            self.engine.tools.append(new_handoff_tool)

    def remove_agent_from_registry(self, name: str) -> bool:
        """Remove agent from registry, choice model, and handoff tools."""
        # Remove from choice model
        removed_from_choice = self.agent_choice_model.remove_option_by_name(name)

        # Remove handoff tool from engine
        if self.engine and hasattr(self.engine, "tools"):
            tool_name = f"transfer_to_{name}"
            original_count = len(self.engine.tools)
            self.engine.tools = [
                t for t in self.engine.tools if getattr(t, "name", "") != tool_name
            ]
            removed_tool = len(self.engine.tools) < original_count

            return removed_from_choice and removed_tool

        return removed_from_choice


def test_integrated_supervisor():
    """Test the integrated supervisor with proper handoff tools."""

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

    # Create integrated supervisor
    supervisor = IntegratedSupervisorWithHandoff(
        name="integrated_supervisor", agent_registry=registry
    )

    test_choice = supervisor.agent_choice_model.test_model("math_agent")

    if hasattr(supervisor.engine, "tools"):
        tool_names = [getattr(t, "name", "unknown") for t in supervisor.engine.tools]

        # Check for expected tools
        expected_tools = [
            "transfer_to_math_agent",
            "transfer_to_planning_agent",
            "forward_message",
            "choose_agent",
            "list_agents",
        ]
        for expected in expected_tools:
            if expected in tool_names:
                pass")
            else:
                pass")

    try:
        result = supervisor.invoke(
            {"messages": [HumanMessage("I need to calculate 25 * 8")]}
        )

    except Exception as e:
        pass

    return supervisor


if __name__ == "__main__":
    supervisor = test_integrated_supervisor()
