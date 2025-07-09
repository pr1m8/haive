# src/haive/agents/react/tool_handler.py

from typing import Any


def normalize_tool_message(message: dict[str, Any]) -> dict[str, Any]:
    """Normalize a tool message to ensure it has the required attributes.

    Args:
        message: The tool message dictionary

    Returns:
        Normalized tool message dictionary
    """
    # Skip non-tool messages
    if message.get("type") != "tool":
        return message

    # Ensure tool_call_id is present
    if "tool_call_id" not in message and "id" in message:
        message["tool_call_id"] = message["id"]
    elif "tool_call_id" not in message and "name" in message:
        # If no ID but has name, create a placeholder ID
        import uuid

        message["tool_call_id"] = f"call_{uuid.uuid4().hex[:12]}"

    return message


def process_messages(messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Process a list of messages to ensure all tool messages are properly formatted.

    Args:
        messages: List of message dictionaries

    Returns:
        Processed message list
    """
    processed = []

    # First pass - find AIMessages with tool calls and ensure they have IDs
    for i, msg in enumerate(messages):
        if msg.get("type") == "ai" and "tool_calls" in msg.get("additional_kwargs", {}):
            tool_calls = msg["additional_kwargs"]["tool_calls"]
            for tool_call in tool_calls:
                if "id" not in tool_call:
                    import uuid

                    tool_call["id"] = f"call_{uuid.uuid4().hex[:12]}"
        processed.append(msg)

    # Second pass - ensure tool messages have matching tool_call_id
    for i, msg in enumerate(processed):
        if msg.get("type") == "tool":
            # Find the previous AI message with a matching tool call
            for j in range(i - 1, -1, -1):
                prev = processed[j]
                if prev.get("type") == "ai" and "tool_calls" in prev.get(
                    "additional_kwargs", {}
                ):
                    tool_calls = prev["additional_kwargs"]["tool_calls"]
                    for tool_call in tool_calls:
                        if tool_call.get("name") == msg.get("name"):
                            # Link this tool message to the tool call
                            msg["tool_call_id"] = tool_call.get("id")
                            break
                    if "tool_call_id" in msg:
                        break

            # If still no tool_call_id, create one
            if "tool_call_id" not in msg:
                import uuid

                msg["tool_call_id"] = f"call_{uuid.uuid4().hex[:12]}"

    return processed
