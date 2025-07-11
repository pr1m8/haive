"""Prompt templates for dynamic supervisor agent.

This module contains prompt templates and system messages used by the
dynamic supervisor for task routing and agent management.

Constants:
    SUPERVISOR_SYSTEM_PROMPT: Main system prompt for supervisor
    CAPABILITY_ANALYSIS_PROMPT: Prompt for analyzing required capabilities
    ROUTING_DECISION_PROMPT: Prompt for making routing decisions

Functions:
    format_supervisor_prompt: Format the main supervisor prompt with agents
    format_agent_list: Format agent list for inclusion in prompts
"""

from typing import TYPE_CHECKING, Dict, List

if TYPE_CHECKING:
    from haive.agents.dynamic_supervisor.models import AgentInfo


# Main supervisor system prompt
SUPERVISOR_SYSTEM_PROMPT = """You are an intelligent task supervisor that routes tasks to specialized agents.

Your role is to:
1. Analyze incoming tasks to understand what capabilities are needed
2. Route tasks to the most appropriate available agent
3. Identify when required capabilities are missing
4. Coordinate multi-step tasks that require multiple agents

Available agents:
{agent_list}

When routing tasks:
- Use handoff tools (handoff_to_[agent_name]) to delegate work to specific agents
- Provide clear, detailed task descriptions when handing off
- Consider agent capabilities and current availability (active/inactive)
- If no suitable agent exists, use choose_agent("END") and explain what's missing

For multi-step tasks:
- Break down the task into logical steps
- Identify which agent should handle each step
- Route to agents sequentially as needed

Always:
- Explain your routing decisions
- Provide context when handing off tasks
- Be specific about what you need from each agent"""


# Prompt for capability analysis
CAPABILITY_ANALYSIS_PROMPT = """Analyze the following task and identify required capabilities:

Task: {task}

Consider:
1. What type of expertise is needed?
2. What tools or resources are required?
3. Are there multiple steps requiring different capabilities?
4. What would be the ideal agent profile for this task?

Required capabilities:"""


# Prompt for routing decision
ROUTING_DECISION_PROMPT = """Based on the task analysis and available agents, make a routing decision:

Task: {task}
Required capabilities: {capabilities}

Available agents:
{agent_list}

Decision criteria:
- Match required capabilities to agent descriptions
- Consider agent availability (active/inactive)
- Identify if multiple agents are needed
- Determine if any capabilities are missing

Your routing decision:"""


# Missing capability prompt
MISSING_CAPABILITY_PROMPT = """I've identified that this task requires capabilities we don't currently have.

Task: {task}
Missing capability: {capability}

The task requires {capability} because {reason}. We would need an agent that can:
{requirements}

For now, I'm unable to complete this task without the {capability} capability."""


def format_supervisor_prompt(agents: dict[str, "AgentInfo"]) -> str:
    """Format the supervisor system prompt with current agents.

    Args:
        agents: Dictionary of agent name to AgentInfo

    Returns:
        Formatted system prompt

    Example:
        Formatting prompt with agents::

            prompt = format_supervisor_prompt(state.agents)
            # Use in supervisor engine configuration
    """
    agent_list = format_agent_list(agents)
    return SUPERVISOR_SYSTEM_PROMPT.format(agent_list=agent_list)


def format_agent_list(agents: dict[str, "AgentInfo"]) -> str:
    """Format agent list for inclusion in prompts.

    Creates a formatted list showing agent names, descriptions,
    capabilities, and status.

    Args:
        agents: Dictionary of agent name to AgentInfo

    Returns:
        Formatted agent list string

    Example:
        Agent list format::

            - search_agent: Web search specialist
              Capabilities: search, research, web
              Status: Active

            - math_agent: Mathematics expert
              Capabilities: math, calculation, statistics
              Status: Inactive
    """
    if not agents:
        return "No agents currently available"

    lines = []
    for name, info in agents.items():
        status = "Active" if info.is_active() else "Inactive"
        capabilities = ", ".join(info.capabilities) if info.capabilities else "General"

        lines.append(f"- {name}: {info.description}")
        lines.append(f"  Capabilities: {capabilities}")
        lines.append(f"  Status: {status}")
        lines.append("")  # Empty line between agents

    return "\n".join(lines).strip()


def format_missing_capability(
    task: str, capability: str, reason: str, requirements: list[str]
) -> str:
    """Format a missing capability message.

    Args:
        task: The task that needs the capability
        capability: The missing capability
        reason: Why this capability is needed
        requirements: What the ideal agent would need to do

    Returns:
        Formatted message about missing capability
    """
    req_list = "\n".join(f"- {req}" for req in requirements)

    return MISSING_CAPABILITY_PROMPT.format(
        task=task, capability=capability, reason=reason, requirements=req_list
    )


# Template for multi-agent coordination
MULTI_AGENT_COORDINATION_TEMPLATE = """This task requires coordination between multiple agents:

Task: {task}

Step-by-step plan:
{plan}

I'll coordinate the execution:
1. First, I'll route to {first_agent} for {first_step}
2. Then use the results with {second_agent} for {second_step}
3. Finally, {final_step}

Starting with step 1..."""


# Template for explaining routing decisions
ROUTING_EXPLANATION_TEMPLATE = """I'm routing this task to {agent_name} because:

- The task requires: {required_capabilities}
- {agent_name} provides: {agent_capabilities}
- Match confidence: {confidence}%

Task for {agent_name}: {task_description}"""
