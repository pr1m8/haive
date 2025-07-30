"""Base prompt templates for supervisor agents.

This module provides common prompt templates used across all supervisor
implementations for routing, coordination, and agent management.
"""


class BaseSupervisorPrompts:
    """Base prompt templates for supervisor functionality."""

    SUPERVISOR_SYSTEM_PROMPT = """You are an intelligent supervisor agent that coordinates multiple specialized agents to accomplish complex tasks.

Your responsibilities:
1. Analyze incoming tasks and determine the best agent to handle them
2. Route tasks to appropriate specialized agents
3. Coordinate multi-step workflows across different agents
4. Monitor execution and handle any errors
5. Provide comprehensive responses based on agent outputs

Available agents and their capabilities:
{agent_list}

Guidelines:
- Always analyze the task carefully before routing
- Choose the most appropriate agent based on task requirements
- Use the available tools to communicate with agents
- Provide clear, comprehensive responses
- Handle errors gracefully and try alternative approaches if needed

When you need to hand off a task to an agent, use the handoff tools provided.
When you need information about available agents, use the list_agents tool.
"""

    ROUTING_DECISION_PROMPT = """Analyze this task and determine the best agent to handle it:

Task: {task}

Available agents:
{agent_list}

Consider:
1. Which agent's capabilities best match the task requirements?
2. What is the complexity of the task?
3. Are there any special requirements or constraints?
4. Would this task benefit from a specific agent's expertise?

Provide your reasoning and select the most appropriate agent."""

    MULTI_AGENT_COORDINATION_PROMPT = """You are coordinating a multi-step task that may require multiple agents:

Original task: {task}

Available agents:
{agent_list}

Break down the task and determine:
1. What steps are needed to complete this task?
2. Which agents should handle each step?
3. How should the results be combined?
4. What is the optimal execution order?

Coordinate the agents to complete this task efficiently."""

    ERROR_RECOVERY_PROMPT = """An error occurred during task execution:

Original task: {task}
Agent used: {agent_name}
Error: {error_message}

Available alternative agents:
{available_agents}

Determine how to recover:
1. Can the same agent retry with different approach?
2. Should we try a different agent?
3. Should we break down the task differently?
4. What additional context might help?

Provide a recovery strategy."""

    TASK_COMPLETION_PROMPT = """Summarize the completion of this task:

Original task: {task}
Agent(s) used: {agents_used}
Results: {results}

Provide a comprehensive summary that:
1. Confirms the task was completed successfully
2. Highlights key results and insights
3. Notes any important details from the execution
4. Suggests any follow-up actions if relevant"""


class RoutingPrompts:
    """Specialized prompts for agent routing decisions."""

    CAPABILITY_ANALYSIS_PROMPT = """Analyze the capabilities needed for this task:

Task: {task}

Consider what capabilities are required:
- Domain expertise needed
- Technical skills required  
- Tool access needed
- Processing complexity
- Output format requirements

Available agent capabilities:
{agent_capabilities}

Match the task requirements to agent capabilities."""

    LOAD_BALANCING_PROMPT = """Consider load balancing when selecting an agent:

Task: {task}

Agent options with current load:
{agent_load_info}

Select the best agent considering:
1. Capability match for the task
2. Current workload/availability
3. Recent performance history
4. Response time requirements

Balance effectiveness with efficiency."""

    FALLBACK_ROUTING_PROMPT = """Primary routing failed. Determine fallback strategy:

Task: {task}
Primary agent: {primary_agent}
Failure reason: {failure_reason}

Fallback options:
{fallback_agents}

Select the best fallback approach and modify the task if needed."""


class CoordinationPrompts:
    """Prompts for multi-agent coordination."""

    WORKFLOW_PLANNING_PROMPT = """Plan a multi-agent workflow for this complex task:

Task: {task}

Available agents:
{agent_list}

Create a workflow plan:
1. Break task into logical steps
2. Assign agents to steps based on expertise
3. Define input/output between steps
4. Identify dependencies and sequencing
5. Plan error handling and fallbacks

Output a structured workflow plan."""

    STEP_COORDINATION_PROMPT = """Coordinate the next step in a multi-agent workflow:

Current workflow step: {current_step}
Previous results: {previous_results}
Remaining steps: {remaining_steps}

Available agents for next step:
{available_agents}

Execute the next step and prepare for subsequent coordination."""

    RESULT_AGGREGATION_PROMPT = """Aggregate results from multiple agents:

Original task: {original_task}

Agent contributions:
{agent_results}

Synthesize these results into a comprehensive response that:
1. Addresses the original task completely
2. Integrates insights from all agents
3. Resolves any conflicts or inconsistencies
4. Provides actionable conclusions"""


def format_agent_list(agents: dict[str, str]) -> str:
    """Format agent list for prompts.

    Args:
        agents: Dict mapping agent names to descriptions

    Returns:
        Formatted string listing agents and capabilities
    """
    if not agents:
        return "No agents currently available."

    lines = []
    for name, description in agents.items():
        lines.append(f"- {name}: {description}")

    return "\n".join(lines)


def format_agent_capabilities(agents: dict[str, list[str]]) -> str:
    """Format agent capabilities for prompts.

    Args:
        agents: Dict mapping agent names to capability lists

    Returns:
        Formatted string with detailed capabilities
    """
    if not agents:
        return "No agent capabilities available."

    lines = []
    for name, capabilities in agents.items():
        cap_str = (
            ", ".join(capabilities)
            if capabilities
            else "No specific capabilities listed"
        )
        lines.append(f"- {name}: {cap_str}")

    return "\n".join(lines)


def create_system_prompt(
    agent_list: str,
    supervisor_name: str | None = None,
    additional_instructions: str | None = None,
) -> str:
    """Create a customized system prompt for supervisor.

    Args:
        agent_list: Formatted string of available agents
        supervisor_name: Optional supervisor name
        additional_instructions: Optional additional instructions

    Returns:
        Complete system prompt
    """
    prompt = BaseSupervisorPrompts.SUPERVISOR_SYSTEM_PROMPT.format(
        agent_list=agent_list
    )

    if supervisor_name:
        prompt = (
            f"You are {supervisor_name}, an intelligent supervisor agent...\n\n"
            + prompt[len("You are an intelligent supervisor agent") :]
        )

    if additional_instructions:
        prompt += f"\n\nAdditional Instructions:\n{additional_instructions}"

    return prompt
