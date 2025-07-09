from collections.abc import Callable, Sequence
from typing import Any
from uuid import uuid4

from langchain_core.messages import (
    AIMessage,
    AnyMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langchain_core.tools import BaseTool, StructuredTool, Tool


def has_tool_calls(state) -> bool:
    """Check if the last AI message has tool calls."""
    # Get last AI message, return False if none exists
    print(state)

    # Check if state has messages attribute
    if not hasattr(state, "messages") or not state.messages:
        return False

    last_msg = state.messages[-1]

    # Check if it's an AIMessage
    if not isinstance(last_msg, AIMessage):
        return False

    # Check for tool_calls attribute and if it's non-empty
    tool_calls = getattr(last_msg, "tool_calls", None)

    # Return True only if tool_calls exists and is non-empty
    return bool(tool_calls)


def has_tool_call(message: AIMessage):
    """
    Check if an AI message contains any tool calls.

    Args:
        message (AIMessage): The AI message object to check

    Returns:
        bool: True if the message has tool calls, False otherwise
    """
    return hasattr(message, "tool_calls")


def has_tool_error(tool_message: ToolMessage):
    """
    Check if a tool message contains an error.

    Args:
        tool_message (ToolMessage): The tool message object to check

    Returns:
        bool: True if the message indicates a tool error, False otherwise
    """
    # Check if additional_kwargs exists and contains 'is_error' key
    if hasattr(tool_message, "additional_kwargs") and isinstance(
        tool_message.additional_kwargs, dict
    ):
        return tool_message.additional_kwargs.get("is_error", False)
    return False


def add_messages(left, right):
    """Add two lists of messages together."""
    if not isinstance(left, list):
        left = [left]
    if not isinstance(right, list):
        right = [right]
    return left + right


def tag_with_name(ai_message: AIMessage, name: str):
    """Tag an AIMessage with a name."""
    ai_message.name = name
    return ai_message


def tag_ai_messages_transform(message, kwargs):
    """Adds a tag to AI messages."""
    tag = kwargs.get("tag", "[AI]")  # Default tag if not provided

    if isinstance(message, AIMessage):
        return AIMessage(
            content=f"{tag} {message.content}", **message.dict(exclude={"content"})
        )

    return message


def transform_messages(
    state: dict[str, Any], transform_fn: Callable[[Any, dict[str, Any]], Any], **kwargs
) -> dict[str, Any]:
    """Generalized function to apply a transformation to all messages in state.

    :param state: The state dictionary containing "messages".
    :param transform_fn: A function that transforms each message.
    :param kwargs: Additional keyword arguments for the transform function.
    :return: A new state dictionary with transformed messages.
    """
    return {
        "messages": [
            transform_fn(message, kwargs) for message in state.get("messages", [])
        ]
    }


def swap_roles_transform(message, kwargs):
    """Specific transformation function for swapping AI/Human roles."""
    name = kwargs.get("name")  # Get the "name" argument

    if isinstance(message, AIMessage) and message.name != name:
        return HumanMessage(**message.dict(exclude={"type"}))

    return message  # Return unchanged if conditions don't match


def route_messages(
    state: dict,
    speaker_name: str = "Subject_Matter_Expert",
    max_turns: int = 5,
    last_question_trigger: str = "Thank you so much for your help!",
    end_route: str = "END",
    continue_route: str = "ask_question",
) -> str:
    messages: list[AIMessage | HumanMessage | SystemMessage] = state["messages"]

    # Count how many AI messages from this speaker
    num_responses = len(
        [m for m in messages if isinstance(m, AIMessage) and m.name == speaker_name]
    )
    if num_responses >= max_turns:
        return end_route

    # Check if second-to-last message ends with a certain string
    if len(messages) >= 2:
        last_question = messages[-2]
        if last_question.content.endswith(last_question_trigger):
            return end_route

    return continue_route


def reduce_messages(
    left: list[AnyMessage], right: list[AnyMessage]
) -> list[AnyMessage]:
    # assign ids to messages that don't have them
    for message in right:
        if not message.id:
            message.id = str(uuid4())
    # merge the new messages with the existing messages
    merged = left.copy()
    for message in right:
        for i, existing in enumerate(merged):
            # replace any existing messages with the same id
            if existing.id == message.id:
                merged[i] = message
                break
        else:
            # append any new messages to the end
            merged.append(message)
    return merged


# =============================================
# Message Utilities
# =============================================


def normalize_message(message: dict[str, Any] | BaseMessage) -> BaseMessage:
    """Normalize a message to a BaseMessage instance.

    Args:
        message: Either a BaseMessage or a dict representation of a message

    Returns:
        A BaseMessage instance
    """
    # If it's already a BaseMessage, return it
    if isinstance(message, BaseMessage):
        return message

    # Otherwise, convert from dict
    msg_type = message.get("type", "")
    content = message.get("content", "")

    if msg_type == "ai":
        additional_kwargs = message.get("additional_kwargs", {})
        additional_kwargs.get("tool_calls", [])
        return AIMessage(
            content=content,
            additional_kwargs=additional_kwargs,
        )
    if msg_type == "human":
        return HumanMessage(content=content)
    if msg_type == "system":
        return SystemMessage(content=content)
    if msg_type == "tool":
        tool_call_id = message.get("tool_call_id")
        name = message.get("name", "")
        return ToolMessage(content=content, tool_call_id=tool_call_id, name=name)

    # Default to HumanMessage if type is unknown
    return HumanMessage(content=str(message))


def normalize_messages(
    messages: Sequence[dict[str, Any] | BaseMessage],
) -> list[BaseMessage]:
    """Normalize a list of messages to BaseMessage instances.

    Args:
        messages: List of messages in various formats

    Returns:
        List of BaseMessage instances
    """
    return [normalize_message(msg) for msg in messages]


def has_tool_calls(state: dict[str, Any] | Any) -> bool:
    """Check if the last message in state has tool calls.

    Args:
        state: Agent state

    Returns:
        True if the last message has tool calls, False otherwise
    """
    # Get messages from the state
    if isinstance(state, dict):
        messages = state.get("messages", [])
    elif hasattr(state, "messages"):
        messages = state.messages
    else:
        return False

    # No messages, no tool calls
    if not messages:
        return False

    # Get the last message
    last_message = messages[-1]

    # Normalize if it's a dict
    if isinstance(last_message, dict):
        last_message = normalize_message(last_message)

    # Check for tool calls in AIMessage
    if isinstance(last_message, AIMessage):
        # Check direct tool_calls attribute
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return True

        # Check in additional_kwargs
        if (
            hasattr(last_message, "additional_kwargs")
            and "tool_calls" in last_message.additional_kwargs
            and last_message.additional_kwargs["tool_calls"]
        ):
            return True

    return False


def get_last_message(state: dict[str, Any] | Any) -> BaseMessage | None:
    """Get the last message from state.

    Args:
        state: Agent state

    Returns:
        Last message or None if there are no messages
    """
    # Get messages from the state
    if isinstance(state, dict):
        messages = state.get("messages", [])
    elif hasattr(state, "messages"):
        messages = state.messages
    else:
        return None

    # No messages
    if not messages:
        return None

    # Get the last message
    last_message = messages[-1]

    # Normalize if it's a dict
    if isinstance(last_message, dict):
        return normalize_message(last_message)

    return last_message


class MessageNormalizingToolNode:
    """A wrapper around LangGraph's ToolNode that ensures proper message normalization.

    This fixes serialization warnings by ensuring all messages are properly
    converted to and from the correct types.
    """

    def __init__(self, tools: list[BaseTool | Tool | StructuredTool | Callable]):
        """Initialize with tools.

        Args:
            tools: List of tools to use
        """
        # Create the underlying ToolNode
        from langgraph.prebuilt import ToolNode as LangGraphToolNode

        self.tool_node = LangGraphToolNode(tools)
        self.tools = tools

        # Store tool names for stats
        self.tool_names = {
            tool.name if hasattr(tool, "name") else getattr(tool, "__name__", "unknown")
            for tool in tools
        }

    def __call__(self, state: dict[str, Any] | Any):
        """Process state with tools, ensuring proper message normalization.

        Args:
            state: Agent state

        Returns:
            Updated state
        """
        # Convert state to dict if it's a BaseModel
        if hasattr(state, "model_dump"):
            state_dict = state.model_dump()
        else:
            state_dict = dict(state)

        # Normalize messages
        if "messages" in state_dict:
            state_dict["messages"] = normalize_messages(state_dict["messages"])

        # Get the last message to check for tool calls
        last_message = get_last_message(state_dict)

        # Only process if we have an AI message with tool calls
        if isinstance(last_message, AIMessage) and (
            (hasattr(last_message, "tool_calls") and last_message.tool_calls)
            or "tool_calls" in last_message.additional_kwargs
        ):
            # Process with the underlying tool node
            result = self.tool_node.invoke(state_dict)

            # Update tool usage stats if available
            if "tool_usage_stats" in state_dict and result.get("messages"):
                for msg in result["messages"]:
                    if isinstance(msg, ToolMessage):
                        tool_name = msg.name
                        if tool_name in state_dict["tool_usage_stats"]:
                            state_dict["tool_usage_stats"][tool_name] += 1
                        else:
                            state_dict["tool_usage_stats"][tool_name] = 1

            # Update current step if tracking
            if "current_step" in state_dict:
                state_dict["current_step"] = state_dict.get("current_step", 0) + 1

            # Update remaining steps if tracking
            if "remaining_steps" in state_dict and "max_iterations" in state_dict:
                max_steps = state_dict.get("max_iterations", 10)
                current_step = state_dict.get("current_step", 0)
                state_dict["remaining_steps"] = max(0, max_steps - current_step)
                state_dict["is_last_step"] = state_dict["remaining_steps"] <= 0

            return result
        # No tool calls to process, return state unchanged
        return state_dict

    def get_tool_by_name(self, name: str) -> BaseTool | None:
        """Get a tool by name.

        Args:
            name: Tool name

        Returns:
            Tool instance or None if not found
        """
        return self.tool_node.get_tool(name)

    def run_tool(self, tool_name: str, **kwargs) -> Any:
        """Run a specific tool directly.

        Args:
            tool_name: Name of the tool to run
            **kwargs: Arguments for the tool

        Returns:
            Tool execution result
        """
        tool = self.get_tool_by_name(tool_name)
        if not tool:
            raise ValueError(f"Tool '{tool_name}' not found")

        return tool.invoke(kwargs)
