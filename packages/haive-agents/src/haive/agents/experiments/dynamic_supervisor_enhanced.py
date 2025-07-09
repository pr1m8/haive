"""Enhanced Dynamic Supervisor with self-modification capabilities."""

import logging
from typing import Any, Dict, Optional, Type

from langchain_core.tools import tool

from haive.agents.base import Agent
from haive.agents.experiments.dynamic_supervisor import DynamicSupervisorAgent
from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent

logger = logging.getLogger(__name__)


def create_agent_management_tools(supervisor_instance):
    """Create tools that allow the supervisor to manage its own agent registry."""

    @tool
    def create_agent(
        name: str,
        description: str,
        agent_type: str = "simple",
        system_message: str = "",
        capabilities: Optional[str] = None,
    ) -> str:
        """Create and register a new agent in the supervisor's registry.

        Args:
            name: Unique name for the agent (e.g., 'coding_agent')
            description: What the agent does (e.g., 'Code generation and debugging')
            agent_type: Type of agent - 'simple' or 'react' (default: 'simple')
            system_message: System prompt for the agent
            capabilities: Comma-separated list of agent capabilities

        Returns:
            Success or error message
        """
        try:
            # Map agent types to classes
            agent_classes = {
                "simple": SimpleAgent,
                "react": ReactAgent,
            }

            agent_class = agent_classes.get(agent_type.lower())
            if not agent_class:
                return f"Error: Unknown agent type '{agent_type}'. Use 'simple' or 'react'."

            # Check if agent already exists
            if name in supervisor_instance.agent_registry.list_agents():
                return f"Error: Agent '{name}' already exists."

            # Prepare config
            config = {
                "name": name.replace("_", " ").title(),
                "system_message": system_message or f"You are a {description.lower()}.",
            }

            # Add agent to registry
            supervisor_instance.add_agent_to_registry(
                name=name,
                description=description,
                agent_class=agent_class,
                config=config,
            )

            # Store capabilities if provided
            if capabilities and hasattr(supervisor_instance.agent_registry, "_agents"):
                supervisor_instance.agent_registry._agents[name]["capabilities"] = [
                    cap.strip() for cap in capabilities.split(",")
                ]

            return f"Successfully created and registered agent '{name}' with handoff tool 'handoff_to_{name}'"

        except Exception as e:
            logger.error(f"Error creating agent {name}: {e}")
            return f"Error creating agent: {str(e)}"

    @tool
    def remove_agent(name: str) -> str:
        """Remove an agent from the supervisor's registry.

        Args:
            name: Name of the agent to remove

        Returns:
            Success or error message
        """
        try:
            if name not in supervisor_instance.agent_registry.list_agents():
                return f"Error: Agent '{name}' not found."

            supervisor_instance.remove_agent_from_registry(name)
            return f"Successfully removed agent '{name}' and its handoff tool."

        except Exception as e:
            return f"Error removing agent: {str(e)}"

    @tool
    def modify_agent(
        name: str,
        description: Optional[str] = None,
        system_message: Optional[str] = None,
    ) -> str:
        """Modify an existing agent's configuration.

        Args:
            name: Name of the agent to modify
            description: New description (optional)
            system_message: New system message (optional)

        Returns:
            Success or error message
        """
        try:
            agents = supervisor_instance.agent_registry.list_agents()
            if name not in agents:
                return f"Error: Agent '{name}' not found."

            # Update agent info
            if hasattr(supervisor_instance.agent_registry, "_agents"):
                if description:
                    supervisor_instance.agent_registry._agents[name][
                        "description"
                    ] = description
                if (
                    system_message
                    and "config" in supervisor_instance.agent_registry._agents[name]
                ):
                    supervisor_instance.agent_registry._agents[name]["config"][
                        "system_message"
                    ] = system_message

            return f"Successfully modified agent '{name}'"

        except Exception as e:
            return f"Error modifying agent: {str(e)}"

    @tool
    def analyze_task_and_suggest_agent(task: str) -> str:
        """Analyze a task and suggest what type of agent might be needed.

        Args:
            task: Description of the task to analyze

        Returns:
            Suggestion for agent creation
        """
        task_lower = task.lower()

        suggestions = []

        # Analyze task keywords
        if any(
            word in task_lower
            for word in ["code", "program", "debug", "script", "function"]
        ):
            suggestions.append(
                {
                    "name": "coding_agent",
                    "type": "react",
                    "description": "Code generation, debugging, and analysis",
                    "message": "You are an expert programmer who helps with coding tasks.",
                }
            )

        if any(
            word in task_lower
            for word in ["write", "draft", "compose", "edit", "content"]
        ):
            suggestions.append(
                {
                    "name": "writing_agent",
                    "type": "simple",
                    "description": "Creative writing and content generation",
                    "message": "You are a skilled writer who creates engaging content.",
                }
            )

        if any(
            word in task_lower for word in ["data", "analyze", "statistics", "visualiz"]
        ):
            suggestions.append(
                {
                    "name": "data_agent",
                    "type": "react",
                    "description": "Data analysis and visualization",
                    "message": "You are a data scientist who analyzes data and creates insights.",
                }
            )

        if any(word in task_lower for word in ["translate", "language", "localize"]):
            suggestions.append(
                {
                    "name": "translator_agent",
                    "type": "simple",
                    "description": "Language translation and localization",
                    "message": "You are a professional translator fluent in multiple languages.",
                }
            )

        if not suggestions:
            return "No specific agent type identified. Consider creating a general-purpose agent."

        result = "Based on the task, I suggest creating:\n\n"
        for s in suggestions:
            result += f"- Agent: '{s['name']}'\n"
            result += f"  Type: {s['type']}\n"
            result += f"  Description: {s['description']}\n"
            result += f"  System message: {s['message']}\n\n"

        result += "Use the 'create_agent' tool to create any of these agents."

        return result

    return [create_agent, remove_agent, modify_agent, analyze_task_and_suggest_agent]


class SelfModifyingSupervisor(DynamicSupervisorAgent):
    """A supervisor that can modify its own agent registry based on task requirements."""

    def __init__(self, *args, enable_self_modification: bool = True, **kwargs):
        """Initialize with self-modification capabilities."""
        # Set attribute before calling parent init
        self._enable_self_modification = enable_self_modification

        # Update system message if enabled
        if enable_self_modification and "system_message" not in kwargs:
            kwargs[
                "system_message"
            ] = """You are an intelligent dynamic supervisor that coordinates multiple specialized agents.

Your key capabilities:
1. Analyze incoming tasks and determine which agents are best suited
2. Create new specialized agents when needed using the 'create_agent' tool
3. Remove agents that are no longer needed
4. Delegate tasks to appropriate agents using 'handoff_to_X' tools
5. Coordinate multi-agent workflows

When you receive a task:
- First check available agents with 'list_agents'
- If no suitable agent exists, use 'analyze_task_and_suggest_agent' to get suggestions
- Create new agents as needed with 'create_agent'
- Then delegate the task using the appropriate 'handoff_to_X' tool

Always think step-by-step about the best approach before acting."""

        super().__init__(*args, **kwargs)

    def _create_dynamic_tools(self) -> list:
        """Create tools including self-modification capabilities."""
        # Get base tools
        tools = super()._create_dynamic_tools()

        # Add self-modification tools if enabled
        if self._enable_self_modification:
            management_tools = create_agent_management_tools(self)
            tools.extend(management_tools)

        return tools


# Example usage
if __name__ == "__main__":
    import asyncio

    from haive.core.engine import AugLLMEngine

    async def demo_self_modifying_supervisor():
        # Create self-modifying supervisor
        supervisor = SelfModifyingSupervisor(
            name="Autonomous Supervisor", enable_self_modification=True, debug=True
        )

        # Initial state - maybe just one general agent
        supervisor.agent_registry.register(
            "general_agent",
            "General purpose assistant",
            SimpleAgent,
            {
                "name": "General Assistant",
                "system_message": "You are a helpful assistant.",
            },
        )

        print("🤖 Self-Modifying Supervisor Demo")
        print("=" * 50)
        print(f"Initial agents: {list(supervisor.agent_registry.list_agents().keys())}")
        print(f"Initial tools: {len(supervisor.tools)}")

        # Simulate a task that requires a specialized agent
        task = "I need help writing a Python script to analyze sales data and create visualizations"

        print(f"\n📋 Task: {task}")
        print("\nSupervisor will:")
        print("1. Analyze the task")
        print("2. Realize it needs specialized agents")
        print("3. Create appropriate agents")
        print("4. Delegate the work")

        # In actual use, the supervisor would handle this autonomously
        # through its tool calls during execution

        return supervisor

    # Run demo
    supervisor = asyncio.run(demo_self_modifying_supervisor())
    print(f"\n✅ Supervisor ready with {len(supervisor.tools)} tools")
