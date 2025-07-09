from collections.abc import Callable
from typing import Any

from agents.react_agent2.models import Action, ActionType, Thought
from haive.core.engine.aug_llm import AugLLMConfig, compose_runnable
from langchain_core.messages import AIMessage
from langgraph.graph import END
from langgraph.types import Command
from pydantic import BaseModel


def get_tool_by_name(tools, name):
    """Get a tool by name from the tools dictionary or list.
    Handles different tool formats (function, BaseTool, or class with name attribute).
    """
    # If tools is a dictionary, direct lookup
    if isinstance(tools, dict):
        return tools.get(name)

    # If tools is a list, search by name attribute or __name__
    if isinstance(tools, list):
        for tool in tools:
            # BaseTool or StructuredTool with name attribute
            if (hasattr(tool, "name") and tool.name == name) or (
                hasattr(tool, "__name__") and tool.__name__ == name
            ):
                return tool
            # Class with name class variable
            if (
                hasattr(tool, "name")
                and isinstance(tool.name, str)
                and tool.name == name
            ):
                return tool

    return None


def get_tool_description(tool):
    """Get the description of a tool.
    Handles different tool formats (function, BaseTool, or class with description).
    """
    # Function with docstring
    if hasattr(tool, "__doc__") and tool.__doc__:
        return tool.__doc__

    # BaseTool or class with description attribute
    if hasattr(tool, "description") and tool.description:
        return tool.description

    # No description found
    return f"Tool: {get_tool_name(tool)}"


def get_tool_name(tool):
    """Get the name of a tool.
    Handles different tool formats (function, BaseTool, or class with name).
    """
    # BaseTool with name attribute
    if hasattr(tool, "name") and isinstance(tool.name, str):
        return tool.name

    # Function with __name__ attribute
    if hasattr(tool, "__name__"):
        return tool.__name__

    # Class with name class variable
    if hasattr(tool.__class__, "name") and isinstance(tool.__class__.name, str):
        return tool.__class__.name

    # No name found
    return "unknown_tool"


def execute_tool(tool, input_value):
    """Execute a tool with the given input.
    Handles different tool formats (function, BaseTool, or class with __call__).
    """
    # Direct function call
    if callable(tool) and not hasattr(tool, "run"):
        return tool(input_value)

    # BaseTool with run method
    if hasattr(tool, "run"):
        return tool.run(input_value)

    # Class with __call__ method
    if callable(tool):
        return tool(input_value)

    # Cannot execute
    return f"Error: Cannot execute tool {get_tool_name(tool)}"


import traceback


def think_node(state: dict[str, Any], aug_llm: AugLLMConfig | None = None) -> Command:
    """Think about the current state and decide on an action.

    Args:
        state: Current state dict or ReactState
        aug_llm: Optional AugLLMConfig for thinking (if provided, overrides the default)

    Returns:
        Command object with next state updates
    """
    # Debugging: Print the state type
    print(f"DEBUG - think_node received state type: {type(state)}")

    # Convert state to dict if it's a model
    state_dict = state.model_dump() if hasattr(state, "model_dump") else state

    # Track iteration count to prevent infinite loops
    iteration_count = state_dict.get("iteration_count", 0) + 1
    max_iterations = state_dict.get("max_iterations", 10)

    print(f"DEBUG - Current iteration: {iteration_count}/{max_iterations}")

    if iteration_count > max_iterations:
        print("DEBUG - Maximum iterations reached")
        return Command(
            update={
                "final_answer": "Maximum iterations reached. I need to stop now.",
                "messages": state_dict.get("messages", [])
                + [
                    AIMessage(
                        content="I've reached my maximum number of thinking steps and need to stop now."
                    )
                ],
                "status": "done",
            },
            goto="observe",
        )

    # Prepare input for thinking
    messages = state_dict.get("messages", [])
    observations = state_dict.get("observations", [])
    intermediate_steps = state_dict.get("intermediate_steps", [])

    # Build context for thinking
    prompt_input = {}

    # Include messages
    if messages:
        prompt_input["messages"] = messages
        print(f"DEBUG - Using {len(messages)} messages in prompt")

    # Include original query from messages
    if "input" not in prompt_input:
        for msg in messages:
            if isinstance(msg, tuple) and msg[0] == "user":
                prompt_input["input"] = msg[1]
                print(f"DEBUG - Found user input: {msg[1][:50]}...")
                break
            if hasattr(msg, "type") and msg.type == "human":
                prompt_input["input"] = msg.content
                print(f"DEBUG - Found human message: {msg.content[:50]}...")
                break

    # If no input was found, add a default
    if "input" not in prompt_input:
        prompt_input["input"] = "Please provide assistance."
        print("DEBUG - Using default input message")

    # Include intermediate steps
    step_context = []
    for i, step in enumerate(intermediate_steps):
        if isinstance(step, tuple):
            action, observation = step
            step_context.append(f"Step {i+1}:")
            step_context.append(f"Action: {action}")
            step_context.append(f"Observation: {observation}")
        elif isinstance(step, dict):
            step_context.append(f"Step {i+1}:")
            step_context.append(f"Action: {step.get('action', 'unknown')}")
            step_context.append(f"Observation: {step.get('observation', 'unknown')}")

    if step_context:
        prompt_input["steps"] = "\n".join(step_context)
        print(f"DEBUG - Added {len(intermediate_steps)} intermediate steps to context")
    else:
        prompt_input["steps"] = ""

    # Make sure we have a valid LLM config
    if not aug_llm:
        print("DEBUG - No LLM config provided, creating a fallback response")
        return Command(
            update={
                "final_answer": "Error: Thinking LLM not configured properly.",
                "status": "done",
            },
            goto="observe",
        )

    # Call thinking LLM
    try:
        print("DEBUG - Composing thinking LLM runnable")
        runnable = compose_runnable(aug_llm)

        print(
            f"DEBUG - Invoking LLM with prompt input keys: {list(prompt_input.keys())}"
        )
        thought_result = runnable.invoke(prompt_input)

        print(f"DEBUG - LLM result type: {type(thought_result)}")
        if hasattr(thought_result, "content"):
            print(f"DEBUG - LLM result content: {thought_result.content[:100]}...")
        else:
            print(f"DEBUG - LLM raw result: {str(thought_result)[:100]}...")

        # Parse result
        if isinstance(thought_result, Thought):
            # Already parsed as Thought
            thought = thought_result
            print("DEBUG - Result already parsed as Thought")
        else:
            # Need to parse manually
            print("DEBUG - Need to manually parse result to Thought")

            # Extract content from various possible response formats
            content = ""
            if hasattr(thought_result, "content"):
                content = thought_result.content
            elif isinstance(thought_result, str):
                content = thought_result
            elif isinstance(thought_result, dict) and "thought" in thought_result:
                # Handle dict with direct mapping
                return Command(
                    update={
                        "thoughts": state_dict.get("thoughts", []) + [thought_result],
                        "current_thought": thought_result,
                        "current_action": thought_result.get(
                            "action",
                            {
                                "action_type": "final_answer",
                                "action_input": "I couldn't determine what to do.",
                            },
                        ),
                        "iteration_count": iteration_count,
                        "status": "acting",
                    },
                    goto="act",
                )
            else:
                content = str(thought_result)

            print(f"DEBUG - Extracted content: {content[:100]}...")

            # Try to extract action using regex
            import re

            action_type = ActionType.FINAL_ANSWER
            action_input = content

            # Look for "Action:" pattern
            action_match = re.search(r"Action:(.+?)(?:\n|$)", content)
            if action_match:
                action_name = action_match.group(1).strip()

                # Look for tool names in the action
                tools = state_dict.get("tools", {})
                tool_names = state_dict.get("tool_names", [])

                for name in tool_names:
                    if name.lower() in action_name.lower():
                        action_type = name
                        break

            # Look for "Action Input:" pattern
            action_input_match = re.search(
                r"Action Input:(.+?)(?:\n|$)", content, re.DOTALL
            )
            if action_input_match:
                action_input = action_input_match.group(1).strip()

            # Create a Thought object
            thought = Thought(
                thought=content,
                action=Action(action_type=action_type, action_input=action_input),
            )
            print(f"DEBUG - Manually created Thought: {thought}")

        # Update state with new thought
        thoughts = state_dict.get("thoughts", [])
        thoughts.append(thought)

        print("DEBUG - Successfully updated state with new thought")
        return Command(
            update={
                "thoughts": thoughts,
                "current_thought": thought.model_dump(),
                "current_action": thought.action.model_dump(),
                "iteration_count": iteration_count,
                "status": "acting",
            },
            goto="act",  # This is correct - going to "act"
        )

    except Exception as e:
        print(f"DEBUG - Error in think_node: {e!s}")
        print(traceback.format_exc())

        # Create a fallback response
        return Command(
            update={
                "final_answer": f"Error in thinking process: {e!s}",
                "status": "done",
            },
            goto="observe",
        )


def act_node(state: dict[str, Any]) -> Command:
    """Execute the action from the current thought."""
    # Convert state to dict if it's a model
    state_dict = state.model_dump() if hasattr(state, "model_dump") else state

    # Get current action
    current_action = state_dict.get("current_action")
    if not current_action:
        return Command(update={"status": "observing"}, goto="observe")

    # Check if it's a final answer
    if current_action.action_type == ActionType.FINAL_ANSWER:
        return Command(
            update={
                "final_answer": current_action.action_input,
                "messages": state_dict.get("messages", [])
                + [AIMessage(content=current_action.action_input)],
                "status": "done",
            },
            goto="observe",
        )

    # Get tools
    tools = state_dict.get("tools", {})

    # Find the tool
    tool = get_tool_by_name(tools, current_action.action_type)

    # Check for retry attempts
    retry_attempts = state_dict.get("retry_attempts", {})
    tool_key = str(current_action.action_type)
    current_attempts = retry_attempts.get(tool_key, 0)
    max_retry_attempts = state_dict.get("max_retry_attempts", 3)

    # Execute tool
    observation = None
    try:
        if tool:
            observation = execute_tool(tool, current_action.action_input)
        else:
            observation = f"Error: Tool '{current_action.action_type}' not found."
    except Exception as e:
        observation = f"Error executing tool '{current_action.action_type}': {e!s}"

        # Increment retry count
        current_attempts += 1
        retry_attempts[tool_key] = current_attempts

        # Check if we should retry
        if current_attempts <= max_retry_attempts:
            return Command(
                update={
                    "retry_attempts": retry_attempts,
                    "observations": state_dict.get("observations", [])
                    + [
                        f"Tool execution failed. Retrying ({current_attempts}/{max_retry_attempts})..."
                    ],
                },
                goto="think",  # Go back to thinking to try a different approach
            )

    # Reset retry count on success
    if tool_key in retry_attempts:
        retry_attempts[tool_key] = 0

    # Update observations
    observations = state_dict.get("observations", [])
    observations.append(observation)

    # Update intermediate steps
    intermediate_steps = state_dict.get("intermediate_steps", [])
    intermediate_steps.append(
        {
            "action": (
                current_action.model_dump()
                if hasattr(current_action, "model_dump")
                else current_action
            ),
            "observation": observation,
        }
    )

    # Update state
    return Command(
        update={
            "observations": observations,
            "intermediate_steps": intermediate_steps,
            "retry_attempts": retry_attempts,
            "status": "observing",
        },
        goto="observe",
    )


def observe_node(state: dict[str, Any]) -> Command:
    """Observe the results and decide next steps."""
    # Convert state to dict if it's a model
    state_dict = state.model_dump() if isinstance(state, BaseModel) else state

    # Check if we're done
    status = state_dict.get("status")
    if status == "done":
        return Command(goto=END)

    # Otherwise, continue thinking
    return Command(update={"status": "thinking"}, goto="think")


# Router functions for conditional edges


def route_by_status(state: dict[str, Any]) -> str:
    """Route based on the current status."""
    # Convert state to dict if it's a model
    state_dict = state.model_dump() if hasattr(state, "model_dump") else state

    # Get status
    status = state_dict.get("status", "thinking")

    # Route based on status
    if status == "thinking":
        return "think"
    if status == "acting":
        return "act"
    if status == "observing":
        return "observe"
    if status == "done":
        return "end"
    # Default to thinking
    return "think"


def create_tool_node(tool_name: str) -> Callable:
    """Create a node function for a specific tool.

    Args:
        tool_name: Name of the tool

    Returns:
        Node function for LangGraph
    """

    def tool_node(state: dict[str, Any]) -> Command:
        # Convert state to dict if it's a model
        state_dict = state.model_dump() if hasattr(state, "model_dump") else state

        # Get current action
        current_action = state_dict.get("current_action")
        if not current_action or current_action.action_type != tool_name:
            # Skip if not for this tool
            return Command(goto="observe")

        # Get tools
        tools = state_dict.get("tools", {})

        # Find the tool
        tool = get_tool_by_name(tools, tool_name)
        if not tool:
            observation = f"Error: Tool '{tool_name}' not found."
        else:
            try:
                observation = execute_tool(tool, current_action.action_input)
            except Exception as e:
                observation = f"Error executing tool '{tool_name}': {e!s}"

        # Update observations
        observations = state_dict.get("observations", [])
        observations.append(observation)

        # Update intermediate steps
        intermediate_steps = state_dict.get("intermediate_steps", [])
        intermediate_steps.append(
            {
                "action": (
                    current_action.model_dump()
                    if hasattr(current_action, "model_dump")
                    else current_action
                ),
                "observation": observation,
            }
        )

        # Update state
        return Command(
            update={
                "observations": observations,
                "intermediate_steps": intermediate_steps,
                "status": "observing",
            },
            goto="observe",
        )

    return tool_node
