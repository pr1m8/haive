"""Base tools for supervisor agents.

This module provides common tools used across all supervisor implementations
for agent management, routing, and coordination.
"""

import logging
from collections.abc import Callable
from typing import Any

from langchain_core.tools import BaseTool, tool
from pydantic import BaseModel, Field

from .models import AgentInfo

logger = logging.getLogger(__name__)


class SupervisorToolBase(BaseModel):
    """Base class for supervisor tool configurations."""

    supervisor_name: str = Field(..., description="Name of supervisor using tools")
    agent_registry: dict[str, Any] = Field(
        default_factory=dict, description="Registry of available agents"
    )


def create_list_agents_tool(get_agents_func: Callable[[], dict[str, str]]) -> BaseTool:
    """Create a tool for listing available agents.

    Args:
        get_agents_func: Function that returns dict of agent_name -> description

    Returns:
        Tool for listing agents
    """

    @tool
    def list_agents() -> str:
        """List all available agents and their capabilities.

        Use this tool to see what agents are available for task routing.
        """
        try:
            agents = get_agents_func()

            if not agents:
                return "No agents are currently registered with this supervisor."

            lines = ["Available agents:"]
            for name, description in agents.items():
                lines.append(f"- **{name}**: {description}")

            return "\n".join(lines)

        except Exception as e:
            logger.error(f"Error listing agents: {e}")
            return f"Error listing agents: {e!s}"

    return list_agents


def create_forward_message_tool() -> BaseTool:
    """Create a tool for forwarding messages between agents.

    Returns:
        Tool for message forwarding
    """

    @tool
    def forward_message(message: str, context: str = "") -> str:
        """Forward a message with optional context.

        Args:
            message: The message to forward
            context: Optional context or instructions

        Returns:
            Confirmation of message forwarding
        """
        try:
            forwarded_msg = f"Message: {message}"
            if context:
                forwarded_msg += f"\nContext: {context}"

            logger.info(f"Forwarded message: {message}")
            return f"Message forwarded successfully: {forwarded_msg}"

        except Exception as e:
            logger.error(f"Error forwarding message: {e}")
            return f"Error forwarding message: {e!s}"

    return forward_message


def create_end_supervision_tool() -> BaseTool:
    """Create a tool for ending supervision.

    Returns:
        Tool for ending supervision
    """

    @tool
    def end_supervision(summary: str = "") -> str:
        """End the supervision session with optional summary.

        Args:
            summary: Optional summary of what was accomplished

        Returns:
            Confirmation of supervision ending
        """
        try:
            result = "Supervision ended successfully."
            if summary:
                result += f"\n\nSummary: {summary}"

            logger.info("Supervision session ended")
            return result

        except Exception as e:
            logger.error(f"Error ending supervision: {e}")
            return f"Error ending supervision: {e!s}"

    return end_supervision


def create_get_agent_info_tool(
    get_agent_info_func: Callable[[str], AgentInfo | None],
) -> BaseTool:
    """Create a tool for getting detailed agent information.

    Args:
        get_agent_info_func: Function to get agent info by name

    Returns:
        Tool for getting agent information
    """

    @tool
    def get_agent_info(agent_name: str) -> str:
        """Get detailed information about a specific agent.

        Args:
            agent_name: Name of the agent to get info for

        Returns:
            Detailed agent information
        """
        try:
            agent_info = get_agent_info_func(agent_name)

            if not agent_info:
                return f"Agent '{agent_name}' not found in registry."

            info_lines = [
                f"Agent: {agent_info.name}",
                f"Description: {agent_info.description}",
                f"Class: {agent_info.agent_class}",
                f"Active: {agent_info.is_active}",
                f"Usage Count: {agent_info.usage_count}",
            ]

            if agent_info.capabilities:
                info_lines.append(f"Capabilities: {', '.join(agent_info.capabilities)}")

            if agent_info.last_used:
                info_lines.append(f"Last Used: {agent_info.last_used.isoformat()}")

            return "\n".join(info_lines)

        except Exception as e:
            logger.error(f"Error getting agent info: {e}")
            return f"Error getting agent info: {e!s}"

    return get_agent_info


def create_get_performance_stats_tool(
    get_stats_func: Callable[[], dict[str, Any]],
) -> BaseTool:
    """Create a tool for getting supervisor performance statistics.

    Args:
        get_stats_func: Function that returns performance statistics

    Returns:
        Tool for getting performance stats
    """

    @tool
    def get_performance_stats() -> str:
        """Get performance statistics for the supervisor and its agents.

        Returns:
            Performance statistics summary
        """
        try:
            stats = get_stats_func()

            lines = ["Supervisor Performance Statistics:", ""]

            # Overall stats
            if "total_executions" in stats:
                lines.append(f"Total Executions: {stats['total_executions']}")
            if "success_rate" in stats:
                lines.append(f"Overall Success Rate: {stats['success_rate']:.2%}")
            if "average_execution_time" in stats:
                lines.append(
                    f"Average Execution Time: {stats['average_execution_time']:.2f}s"
                )

            # Per-agent stats
            if "agent_stats" in stats:
                lines.append("\nPer-Agent Statistics:")
                for agent_name, agent_stats in stats["agent_stats"].items():
                    lines.append(f"\n{agent_name}:")
                    lines.append(f"  Executions: {agent_stats.get('executions', 0)}")
                    lines.append(
                        f"  Success Rate: {agent_stats.get('success_rate', 0):.2%}"
                    )
                    lines.append(f"  Avg Time: {agent_stats.get('avg_time', 0):.2f}s")

            return "\n".join(lines)

        except Exception as e:
            logger.error(f"Error getting performance stats: {e}")
            return f"Error getting performance stats: {e!s}"

    return get_performance_stats


def create_handoff_tool(
    agent_name: str,
    agent_description: str,
    execute_agent_func: Callable[[str, str], str],
) -> BaseTool:
    """Create a handoff tool for a specific agent.

    Args:
        agent_name: Name of the agent
        agent_description: Description of agent capabilities
        execute_agent_func: Function to execute the agent with task

    Returns:
        Tool for handing off tasks to this agent
    """

    @tool
    def handoff_tool(task: str, context: str = "") -> str:
        f"""Hand off a task to {agent_name}.
        
        {agent_description}
        
        Args:
            task: The task to hand off to {agent_name}
            context: Optional additional context for the task
            
        Returns:
            Result from {agent_name}
        """
        try:
            logger.info(f"Handing off task to {agent_name}: {task}")

            # Combine task and context
            full_task = task
            if context:
                full_task += f"\n\nContext: {context}"

            result = execute_agent_func(agent_name, full_task)

            logger.info(f"Received result from {agent_name}")
            return f"Result from {agent_name}: {result}"

        except Exception as e:
            logger.error(f"Error executing {agent_name}: {e}")
            return f"Error executing {agent_name}: {e!s}"

    # Set the tool name dynamically
    handoff_tool.name = f"handoff_to_{agent_name}"
    handoff_tool.__name__ = f"handoff_to_{agent_name}"

    return handoff_tool


class SupervisorToolFactory:
    """Factory for creating supervisor tools with shared state."""

    def __init__(
        self,
        supervisor_name: str,
        get_agents_func: Callable[[], dict[str, str]],
        get_agent_info_func: Callable[[str], AgentInfo | None],
        get_stats_func: Callable[[], dict[str, Any]],
        execute_agent_func: Callable[[str, str], str],
    ):
        """Initialize tool factory.

        Args:
            supervisor_name: Name of the supervisor
            get_agents_func: Function to get agent registry
            get_agent_info_func: Function to get agent info
            get_stats_func: Function to get performance stats
            execute_agent_func: Function to execute agents
        """
        self.supervisor_name = supervisor_name
        self.get_agents_func = get_agents_func
        self.get_agent_info_func = get_agent_info_func
        self.get_stats_func = get_stats_func
        self.execute_agent_func = execute_agent_func

    def create_base_tools(self) -> list[BaseTool]:
        """Create the base set of supervisor tools.

        Returns:
            List of base supervisor tools
        """
        return [
            create_list_agents_tool(self.get_agents_func),
            create_forward_message_tool(),
            create_end_supervision_tool(),
            create_get_agent_info_tool(self.get_agent_info_func),
            create_get_performance_stats_tool(self.get_stats_func),
        ]

    def create_handoff_tools(self, agent_registry: dict[str, str]) -> list[BaseTool]:
        """Create handoff tools for all registered agents.

        Args:
            agent_registry: Dict of agent_name -> description

        Returns:
            List of handoff tools
        """
        tools = []
        for agent_name, description in agent_registry.items():
            tool = create_handoff_tool(agent_name, description, self.execute_agent_func)
            tools.append(tool)
        return tools

    def create_all_tools(self, agent_registry: dict[str, str]) -> list[BaseTool]:
        """Create all supervisor tools (base + handoff).

        Args:
            agent_registry: Dict of agent_name -> description

        Returns:
            Complete list of supervisor tools
        """
        base_tools = self.create_base_tools()
        handoff_tools = self.create_handoff_tools(agent_registry)
        return base_tools + handoff_tools
