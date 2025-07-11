"""Dynamic tool generation for supervisor agent.

This module handles the creation of dynamic tools based on registered agents.
It generates handoff tools for each agent and a choice validation tool.

Functions:
    create_agent_tools: Generate all tools from supervisor state
    create_handoff_tool: Create a handoff tool for a specific agent
    create_choice_tool: Create the agent choice validation tool

Example:
    Generating tools from state::

        state = SupervisorStateWithTools()
        state.add_agent("search", agent, "Search expert")

        tools = create_agent_tools(state)
        # Returns: [handoff_to_search, choose_agent]
"""

from typing import TYPE_CHECKING, Any, List

from langchain_core.tools import tool

if TYPE_CHECKING:
    from haive.agents.dynamic_supervisor.state import SupervisorStateWithTools


def create_agent_tools(state: "SupervisorStateWithTools") -> list[Any]:
    """Generate all tools from current agents in state.

    Creates handoff tools for each registered agent and a choice validation tool.
    Tools are generated dynamically based on the current agent registry.

    Args:
        state: Supervisor state with agent registry

    Returns:
        List of tool instances ready for use

    Example:
        Getting tools for supervisor::

            tools = create_agent_tools(state)
            # Use tools in an engine or pass to LLM
    """
    tools = []

    # Create handoff tools for each agent
    for agent_name, _agent_info in state.agents.items():
        handoff_tool = create_handoff_tool(state, agent_name)
        tools.append(handoff_tool)

    # Add choice validation tool
    choice_tool = create_choice_tool(state)
    tools.append(choice_tool)

    return tools


def create_handoff_tool(state: "SupervisorStateWithTools", agent_name: str) -> Any:
    """Create a handoff tool for a specific agent.

    The handoff tool executes the agent directly and returns results,
    following the pattern from our experimental implementation.

    Args:
        state: Supervisor state instance
        agent_name: Name of the agent to create tool for

    Returns:
        Tool instance for handing off to the agent

    Example:
        Creating a handoff tool::

            tool = create_handoff_tool(state, "search_agent")
            # Creates: handoff_to_search_agent tool
    """
    agent_info = state.agents[agent_name]

    def handoff_tool(task_description: str) -> str:
        """Hand off a task to the specified agent.

        Args:
            task_description: Detailed description of the task

        Returns:
            Result from agent execution
        """
        try:
            # Check if agent is active
            if not agent_info.is_active():
                return f"Agent '{agent_name}' is currently inactive"

            # Get agent instance
            agent = agent_info.get_agent()
            if not agent:
                return f"Could not retrieve agent instance for '{agent_name}'"

            # Execute agent directly (following experimental pattern)
            try:
                # Prepare input with current messages + task
                from langchain_core.messages import HumanMessage

                agent_input = {
                    "messages": [
                        *state.messages,
                        HumanMessage(content=task_description),
                    ]
                }

                # Execute the agent (prefer sync methods in tools)
                if hasattr(agent, "run"):
                    # Sync agent
                    result = agent.run(task_description)
                elif hasattr(agent, "invoke"):
                    # LangChain-style agent
                    result = agent.invoke(agent_input)
                elif hasattr(agent, "arun"):
                    # Async agent - use sync wrapper if available
                    import asyncio

                    result = asyncio.run(agent.arun(task_description))
                else:
                    return f"Agent {agent_name} has no execution method"

                # Extract response - focus on last message only
                response = None
                if hasattr(result, "messages") and result.messages:
                    # Get the last message from agent
                    last_message = result.messages[-1]
                    response = (
                        last_message.content
                        if hasattr(last_message, "content")
                        else str(last_message)
                    )
                elif isinstance(result, dict) and "messages" in result:
                    # Handle dict response with messages
                    messages = result["messages"]
                    if messages:
                        last_message = messages[-1]
                        if hasattr(last_message, "content"):
                            response = last_message.content
                        elif (
                            isinstance(last_message, dict) and "content" in last_message
                        ):
                            response = last_message["content"]
                        else:
                            response = str(last_message)
                elif isinstance(result, str):
                    response = result
                else:
                    response = str(result)

                # Update execution state
                state.last_executed_agent = agent_name
                state.agent_response = response
                state.execution_success = True

                # Get engine info properly
                engine_name = "unknown"
                if hasattr(agent, "engine"):
                    engine = agent.engine
                    if hasattr(engine, "name"):
                        engine_name = engine.name
                    elif hasattr(engine, "llm_config") and hasattr(
                        engine.llm_config, "model"
                    ):
                        engine_name = f"{engine.llm_config.model}"

                # Add response as HumanMessage with agent/engine info
                # This matches how engine nodes add engine information
                human_msg = HumanMessage(
                    content=response,
                    additional_kwargs={
                        "agent_name": agent_name,
                        "engine_name": engine_name,
                        "source": "agent_execution",
                    },
                )
                state.messages.append(human_msg)

                return f"Agent {agent_name} completed: {response}"

            except Exception as e:
                return f"Error executing {agent_name}: {e!s}"

        except Exception as e:
            return f"Error with {agent_name}: {e!s}"

    # Create tool with proper name and description
    handoff_tool.__name__ = f"handoff_to_{agent_name}"
    handoff_tool.__doc__ = f"""Hand off a task to {agent_name}.

    {agent_info.description}

    Capabilities: {', '.join(agent_info.capabilities) if agent_info.capabilities else 'General'}

    Args:
        task_description: The task to delegate to this agent
    """

    # Decorate as tool
    decorated_tool = tool(
        description=f"Hand off task to {agent_name}. {agent_info.description}"
    )(handoff_tool)

    # Ensure name is set correctly
    decorated_tool.name = f"handoff_to_{agent_name}"

    return decorated_tool


def create_choice_tool(state: "SupervisorStateWithTools") -> Any:
    """Create agent choice validation tool.

    This tool provides validated agent selection with dynamic options
    based on the current agent registry. It includes "END" as an option
    for when no suitable agent exists.

    Args:
        state: Supervisor state instance

    Returns:
        Choice validation tool

    Example:
        Using the choice tool::

            tool = create_choice_tool(state)
            result = tool.invoke({"agent": "search_agent"})
    """

    @tool
    def choose_agent(agent: str) -> str:
        """Choose which agent should handle the task.

        Use this when you need to explicitly select an agent or indicate
        that no suitable agent exists (choose "END").

        Args:
            agent: Name of the agent to choose, or "END" if none suitable

        Returns:
            Validation result and routing confirmation
        """
        try:
            # Get valid options from state
            valid_options = [*list(state.agents.keys()), "END"]

            # Validate choice
            if agent not in valid_options:
                return f"Invalid choice '{agent}'. Valid options: {valid_options}"

            # Use the dynamic choice model for validation
            ChoiceModel = state.agent_choice_model.current_model
            validated_choice = ChoiceModel(choice=agent)

            result = f"Selected: {validated_choice.choice}"

            if validated_choice.choice == "END":
                result += "\nNo suitable agent available for this task."
            else:
                # Provide agent info
                agent_info = state.agents.get(validated_choice.choice)
                if agent_info:
                    result += f"\nAgent: {agent_info.description}"
                    if not agent_info.is_active():
                        result += " (currently inactive)"

            return result

        except Exception as e:
            return f"Error validating choice: {e!s}"

    # Update tool description with current options
    agent_list = "\n".join(
        [f"- {name}: {info.description}" for name, info in state.agents.items()]
    )

    choose_agent.__doc__ = f"""Choose which agent should handle the task.

    Available agents:
    {agent_list}
    - END: No suitable agent available

    Args:
        agent: Name of the agent to choose
    """

    return choose_agent


def create_add_agent_tool() -> Any:
    """Create tool for requesting a new agent be added.

    This tool allows the supervisor to formally request a new agent
    when it identifies a missing capability. In a full implementation,
    this would interface with an agent builder or registry service.

    Returns:
        Add agent request tool

    Example:
        Requesting a new agent::

            tool = create_add_agent_tool()
            tool.invoke({
                "capability": "translation",
                "reason": "Need to translate results to French"
            })
    """

    @tool
    def request_agent(
        capability: str, reason: str, requirements: list[str] | None = None
    ) -> str:
        """Request a new agent with specific capability.

        Use this when you identify a missing capability needed for the task.

        Args:
            capability: The capability needed (e.g., "translation", "code_analysis")
            reason: Why this capability is needed for the current task
            requirements: Optional specific requirements for the agent

        Returns:
            Confirmation of the request
        """
        req_str = "\n- ".join(requirements) if requirements else "None"

        return f"""Agent request submitted:
Capability: {capability}
Reason: {reason}
Requirements: {req_str}

The request has been logged. In a production system, this would trigger
the agent builder service to create or fetch an appropriate agent."""

    return request_agent
