"""Tool creation and management for supervisors.

This module provides functions to create and manage tools for supervisor agents,
including handoff tools, control tools, and utility tools.
"""

import logging
from typing import Any, Callable, Dict, List, Optional, Type

from langchain_core.tools import BaseTool, tool
from langgraph_supervisor import create_forward_message_tool, create_handoff_tool
from pydantic import BaseModel as LangchainBaseModel
from pydantic import Field as LangchainField

from haive.agents.experiments.supervisor.state_models import (
    AgentMetadata,
    DynamicSupervisorState,
    SupervisorState,
    ToolMapping,
)

logger = logging.getLogger(__name__)


# Tool argument schemas
class HandoffArgs(LangchainBaseModel):
    """Arguments for agent handoff."""

    task: str = LangchainField(..., description="The task to hand off to the agent")
    context: dict[str, Any] | None = LangchainField(
        default=None, description="Additional context for the agent"
    )
    return_raw: bool = LangchainField(
        default=False, description="Whether to return raw agent output"
    )


class CreateAgentArgs(LangchainBaseModel):
    """Arguments for creating a new agent."""

    name: str = LangchainField(..., description="Name for the new agent")
    description: str = LangchainField(
        ..., description="Description of agent capabilities"
    )
    agent_type: str = LangchainField(
        default="simple",
        description="Type of agent to create (simple, react, research, etc.)",
    )
    system_message: str = LangchainField(
        default="", description="System message for the agent"
    )
    capabilities: list[str] = LangchainField(
        default_factory=list, description="List of agent capabilities"
    )
    tools: list[str] = LangchainField(
        default_factory=list, description="List of tools to give the agent"
    )


class AgentStatusArgs(LangchainBaseModel):
    """Arguments for agent status queries."""

    agent_name: str | None = LangchainField(
        default=None, description="Specific agent to get status for"
    )
    include_performance: bool = LangchainField(
        default=False, description="Include performance metrics"
    )


def create_supervisor_handoff_tool(
    agent_name: str,
    description: str,
    get_state_fn: Callable[[], SupervisorState],
    update_state_fn: Callable[[SupervisorState], None],
) -> BaseTool:
    """Create a handoff tool that works with supervisor state.

    This creates a tool that can access and update the supervisor's state
    to properly execute agent handoffs.
    """

    @tool(args_schema=HandoffArgs)
    def handoff_tool(
        task: str, context: dict[str, Any] | None = None, return_raw: bool = False
    ) -> str:
        f"""Hand off a task to {agent_name}.

        {description}
        """
        state = get_state_fn()

        # Check if agent exists
        if agent_name not in state.agents:
            return f"Error: Agent '{agent_name}' not found in registry"

        # Get the agent
        try:
            agent = state.agents[agent_name].get_agent()
        except Exception as e:
            logger.exception(f"Failed to deserialize agent {agent_name}: {e}")
            return f"Error: Failed to load agent '{agent_name}': {e!s}"

        # Update execution context
        state.execution_context.current_agent = agent_name
        state.execution_context.current_task = task
        state.execution_context.total_steps += 1

        # Execute the agent
        try:
            # Prepare input
            agent_input = {"messages": [{"role": "user", "content": task}]}
            if context:
                agent_input["context"] = context

            # Execute
            result = agent.invoke(agent_input)

            # Extract response
            if isinstance(result, dict):
                if result.get("messages"):
                    response = result["messages"][-1].get("content", str(result))
                else:
                    response = result.get("output", str(result))
            else:
                response = str(result)

            # Update state
            state.update_agent_usage(agent_name)
            state.last_result = result if return_raw else response
            state.add_execution_record(
                {
                    "agent": agent_name,
                    "task": task,
                    "success": True,
                    "response_length": len(str(response)),
                }
            )

            # Save state
            update_state_fn(state)

            return response

        except Exception as e:
            logger.exception(f"Agent {agent_name} execution failed: {e}")

            # Update state with failure
            state.add_execution_record(
                {"agent": agent_name, "task": task, "success": False, "error": str(e)}
            )
            update_state_fn(state)

            return f"Error executing {agent_name}: {e!s}"

    # Set the name dynamically
    handoff_tool.__name__ = f"handoff_to_{agent_name}"
    handoff_tool.__doc__ = f"Hand off a task to {agent_name}. {description}"

    return handoff_tool


def create_list_agents_tool(get_state_fn: Callable[[], SupervisorState]) -> BaseTool:
    """Create tool for listing available agents."""

    @tool(args_schema=AgentStatusArgs)
    def list_agents(
        agent_name: str | None = None, include_performance: bool = False
    ) -> str:
        """List available agents and their capabilities.

        Can list all agents or get detailed info about a specific agent.
        """
        state = get_state_fn()

        if agent_name:
            # Get specific agent info
            if agent_name not in state.agents:
                return f"Agent '{agent_name}' not found"

            agent_info = state.agents[agent_name]
            metadata = agent_info.metadata

            info = [
                f"Agent: {metadata.name}",
                f"Description: {metadata.description}",
                f"Class: {agent_info.agent_class}",
                f"Created: {metadata.created_at.strftime('%Y-%m-%d %H:%M')}",
                f"Usage Count: {metadata.usage_count}",
            ]

            if metadata.last_used:
                info.append(
                    f"Last Used: {metadata.last_used.strftime('%Y-%m-%d %H:%M')}"
                )

            if metadata.capabilities:
                info.append(f"Capabilities: {', '.join(metadata.capabilities)}")

            if include_performance:
                info.append(f"Performance Score: {metadata.performance_score:.2f}")

            return "\n".join(info)

        # List all agents
        if not state.agents:
            return "No agents currently registered."

        agent_list = ["Available agents:"]

        for name, agent_info in state.agents.items():
            metadata = agent_info.metadata
            status = f"- {name}: {metadata.description}"

            if include_performance:
                status += f" (score: {metadata.performance_score:.2f}, used: {metadata.usage_count}x)"

            agent_list.append(status)

        return "\n".join(agent_list)

    return list_agents


def create_agent_creation_tool(
    get_state_fn: Callable[[], DynamicSupervisorState],
    update_state_fn: Callable[[DynamicSupervisorState], None],
    agent_factory: Callable[[str, dict[str, Any]], Any] | None = None,
) -> BaseTool:
    """Create tool for dynamic agent creation.

    Args:
        get_state_fn: Function to get current state
        update_state_fn: Function to update state
        agent_factory: Optional factory function to create agents
    """

    @tool(args_schema=CreateAgentArgs)
    def create_agent(
        name: str,
        description: str,
        agent_type: str = "simple",
        system_message: str = "",
        capabilities: list[str] | None = None,
        tools: list[str] | None = None,
    ) -> str:
        """Create a new agent with specified capabilities.

        This tool allows dynamic creation of new agents during execution.
        """
        state = get_state_fn()

        # Check if we can create agents
        if not state.can_create_agents:
            return "Error: Agent creation is disabled"

        # Check agent limit
        if len(state.agents) >= state.max_agents:
            return f"Error: Maximum agent limit ({state.max_agents}) reached"

        # Check if name already exists
        if name in state.agents:
            return f"Error: Agent '{name}' already exists"

        # Create the agent
        try:
            if agent_factory:
                # Use provided factory
                agent_config = {
                    "name": name,
                    "agent_type": agent_type,
                    "system_message": system_message,
                    "tools": tools or [],
                }
                agent = agent_factory(agent_type, agent_config)
            else:
                # Default creation logic
                from haive.agents.react.agent import ReactAgent
                from haive.agents.simple.agent import SimpleAgent

                # Simple factory based on type
                agent = (
                    ReactAgent(name=name)
                    if agent_type == "react"
                    else SimpleAgent(name=name)
                )

            # Create metadata
            metadata = AgentMetadata(
                name=name,
                description=description,
                capabilities=capabilities or [],
                tags=[agent_type],
            )

            # Register the agent
            state.register_agent(agent, metadata)

            # Record creation
            state.record_agent_creation(name, agent_type)

            # Update state
            update_state_fn(state)

            return f"Successfully created agent '{name}' of type '{agent_type}'"

        except Exception as e:
            logger.exception(f"Failed to create agent {name}: {e}")
            return f"Error creating agent: {e!s}"

    return create_agent


def create_execution_status_tool(
    get_state_fn: Callable[[], SupervisorState],
) -> BaseTool:
    """Create tool for checking execution status."""

    @tool
    def execution_status() -> str:
        """Get current execution status and history.

        Shows what's currently running and recent execution history.
        """
        state = get_state_fn()
        context = state.execution_context

        status_lines = ["Execution Status:"]

        # Current execution
        if context.current_agent:
            status_lines.append(f"Currently executing: {context.current_agent}")
            if context.current_task:
                status_lines.append(f"Current task: {context.current_task[:100]}...")

        status_lines.append(f"Total steps: {context.total_steps}")

        # Execution stack
        if context.execution_stack:
            status_lines.append(f"Call stack: {' -> '.join(context.execution_stack)}")

        # Recent history
        if state.execution_history:
            status_lines.append("\nRecent executions:")
            for record in state.execution_history[-5:]:  # Last 5
                agent = record.get("agent", "unknown")
                success = "✓" if record.get("success", False) else "✗"
                timestamp = record.get("timestamp", "")
                status_lines.append(f"  {success} {agent} - {timestamp}")

        return "\n".join(status_lines)

    return execution_status


def build_supervisor_tools(
    get_state_fn: Callable[[], SupervisorState],
    update_state_fn: Callable[[SupervisorState], None],
    include_dynamic_creation: bool = False,
    agent_factory: Callable | None = None,
) -> list[BaseTool]:
    """Build the complete set of supervisor tools.

    Args:
        get_state_fn: Function to get current state
        update_state_fn: Function to update state
        include_dynamic_creation: Whether to include agent creation tool
        agent_factory: Optional factory for creating agents

    Returns:
        List of tools for the supervisor
    """
    tools = []

    # Core supervisor tools
    tools.append(create_list_agents_tool(get_state_fn))
    tools.append(create_execution_status_tool(get_state_fn))
    tools.append(create_forward_message_tool())  # From langgraph_supervisor

    # Add handoff tools for existing agents
    state = get_state_fn()
    for agent_name, agent_info in state.agents.items():
        handoff_tool = create_supervisor_handoff_tool(
            agent_name=agent_name,
            description=agent_info.metadata.description,
            get_state_fn=get_state_fn,
            update_state_fn=update_state_fn,
        )
        tools.append(handoff_tool)

    # Add dynamic creation if enabled
    if include_dynamic_creation:
        tools.append(
            create_agent_creation_tool(
                get_state_fn=get_state_fn,
                update_state_fn=update_state_fn,
                agent_factory=agent_factory,
            )
        )

    return tools


def sync_tools_with_state(
    state: SupervisorState,
    update_state_fn: Callable[[SupervisorState], None],
    get_state_fn: Callable[[], SupervisorState],
) -> dict[str, BaseTool]:
    """Synchronize tools based on current state.

    Returns a dictionary of tool_name -> tool for all tools that should exist.
    """
    tools_dict = {}

    # Always include base tools
    base_tools = [
        create_list_agents_tool(get_state_fn),
        create_execution_status_tool(get_state_fn),
        create_forward_message_tool(),
    ]

    for tool in base_tools:
        tools_dict[tool.name] = tool

    # Add handoff tools for each agent
    for agent_name, agent_info in state.agents.items():
        tool_name = f"handoff_to_{agent_name}"

        handoff_tool = create_supervisor_handoff_tool(
            agent_name=agent_name,
            description=agent_info.metadata.description,
            get_state_fn=get_state_fn,
            update_state_fn=update_state_fn,
        )

        tools_dict[tool_name] = handoff_tool

    # Add dynamic creation tool if state supports it
    if isinstance(state, DynamicSupervisorState) and state.can_create_agents:
        create_tool = create_agent_creation_tool(
            get_state_fn=get_state_fn, update_state_fn=update_state_fn
        )
        tools_dict[create_tool.name] = create_tool

    return tools_dict
