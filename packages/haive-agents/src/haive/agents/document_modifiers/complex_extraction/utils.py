import uuid
from collections.abc import Callable, Sequence
from typing import TypedDict

import jsonpatch
from langchain_core.messages import AIMessage, AnyMessage, BaseMessage, ToolCall
from langchain_core.prompt_values import PromptValue
from langchain_core.runnables import Runnable
from langgraph.graph import add_messages
from langgraph.types import Command
from pydantic import BaseModel

from haive.agents.document_modifiers.complex_extraction.models import (
    PatchFunctionParameters,
)


def encode(state: BaseModel) -> dict:
    """Ensure the input is the correct format."""
    if isinstance(state.messages, PromptValue):
        return Command(
            update={"messages": state.messages.to_messages(), "input_format": "list"}
        )
    if isinstance(state.messages, list):
        return Command(update={"messages": state.messages, "input_format": "list"})
    raise ValueError(f"Unexpected input type: {type(state.messages)}")


def decode(state: BaseModel) -> dict:
    """Ensure the output is in the expected format.

    This function handles extracting data from the AI message's tool calls and optionally
    parsing it into a Pydantic object based on the configuration.

    Args:
        state: The state containing messages and configuration

    Returns:
        A dictionary with the extracted data
    """
    # Find the AI message with tool calls in the state
    ai_message = None
    extracted_data = None

    if hasattr(state, "messages") and state.messages:
        for message in reversed(state.messages):
            if (
                message.type == "ai"
                and hasattr(message, "tool_calls")
                and message.tool_calls
            ):
                ai_message = message
                # Extract data from tool calls
                for tool_call in message.tool_calls:
                    # If we have a tool call with args, use that as extracted data
                    if "args" in tool_call:
                        extracted_data = tool_call.get("args", {})
                        break
                break

    # If we found extracted data and we should parse into a Pydantic object
    if (
        extracted_data
        and hasattr(state, "config")
        and getattr(state.config, "parse_pydantic", False)
    ):
        # Get the extraction model from config
        extraction_model = getattr(state.config, "extraction_model", None)
        if extraction_model:
            try:
                # Parse the data into the Pydantic model
                parsed_data = extraction_model(**extracted_data)
                return {"extracted_data": parsed_data}
            except Exception as e:
                import logging

                logging.exception(f"Error parsing data into Pydantic model: {e}")
                # Fall back to returning the raw data

    # Return the extracted data or empty dict
    return {"extracted_data": extracted_data or {}}


def default_aggregator(messages: Sequence[AnyMessage]) -> AIMessage:
    """Aggregates a sequence of messages into a single AI message."""
    for m in messages[::-1]:
        if m.type == "ai":
            return m
    raise ValueError("No AI message found in the sequence.")


def aggregate_messages(
    messages: Sequence[AnyMessage],
) -> AIMessage:
    # Get all the AI messages and apply json patches
    resolved_tool_calls: dict[str | None, ToolCall] = {}
    content: str | list[str | dict] = ""
    for m in messages:
        if m.type != "ai":
            continue
        if not content:
            content = m.content
        for tc in m.tool_calls:
            if tc["name"] == PatchFunctionParameters.__name__:
                tcid = tc["args"]["tool_call_id"]
                # Add logging in later.
                if tcid not in resolved_tool_calls:
                    # logger.debug(
                    #    f"JsonPatch tool call ID {tc['args']['tool_call_id']} not found."
                    #    f"Valid tool call IDs: {list(resolved_tool_calls.keys())}"
                    # )
                    tcid = next(iter(resolved_tool_calls.keys()), None)
                orig_tool_call = resolved_tool_calls[tcid]
                current_args = orig_tool_call["args"]
                patches = tc["args"].get("patches") or []
                orig_tool_call["args"] = jsonpatch.apply_patch(
                    current_args,
                    patches,
                )
                orig_tool_call["id"] = tc["id"]
            else:
                resolved_tool_calls[tc["id"]] = tc.copy()
    return AIMessage(
        content=content,
        tool_calls=list(resolved_tool_calls.values()),
    )


def add_or_overwrite_messages(left: list, right: list | dict) -> list:
    """Append or replace messages depending on format."""
    if isinstance(right, dict) and "finalize" in right:
        finalized = right["finalize"]
        if not isinstance(finalized, list):
            finalized = [finalized]
        for m in finalized:
            if m.id is None:
                m.id = str(uuid.uuid4())
        return finalized
    res = add_messages(left, right)
    if not isinstance(res, list):
        return [res]
    return res


def dedict(x: BaseModel) -> list:
    """Get the messages from the state."""
    return x.messages


class RetryStrategy(TypedDict, total=False):
    """The retry strategy for a tool call."""

    max_attempts: int
    """The maximum number of attempts to make."""
    fallback: (
        Runnable[Sequence[AnyMessage], AIMessage]
        | Runnable[Sequence[AnyMessage], BaseMessage]
        | Callable[[Sequence[AnyMessage]], AIMessage]
        | None
    )
    """The function to use once validation fails."""
    aggregate_messages: Callable[[Sequence[AnyMessage]], AIMessage] | None = (
        default_aggregator
    )
