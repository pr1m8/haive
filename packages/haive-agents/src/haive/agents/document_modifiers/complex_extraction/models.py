from collections.abc import Callable, Sequence
from typing import Any, Literal, TypedDict

from langchain_core.messages import AIMessage, AnyMessage, BaseMessage
from langchain_core.runnables import Runnable
from pydantic import BaseModel, Field


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
    aggregate_messages: Callable[[Sequence[AnyMessage]], AIMessage] | None


class JsonPatch(BaseModel):
    r"""A JSON Patch document represents an operation to be performed on a JSON document.

    Note that the op and path are ALWAYS required. Value is required for ALL operations except 'remove'.

    Examples:
    \`\`\`json
    {"op": "add", "path": "/a/b/c", "patch_value": 1}
    {"op": "replace", "path": "/a/b/c", "patch_value": 2}
    {"op": "remove", "path": "/a/b/c"}
    \`\`\`
    """

    op: Literal["add", "remove", "replace"] = Field(
        ...,
        description="The operation to be performed. Must be one of 'add', 'remove', 'replace'.",
    )
    path: str = Field(
        ...,
        description="A JSON Pointer path that references a location within the target document where the operation is performed.",
    )
    value: Any = Field(
        ...,
        description="The value to be used within the operation. REQUIRED for 'add', 'replace', and 'test' operations.",
    )


class PatchFunctionParameters(BaseModel):
    """Respond with all JSONPatch operation to correct validation errors caused by passing in incorrect or incomplete parameters in a previous tool call."""

    tool_call_id: str = Field(
        ...,
        description="The ID of the original tool call that generated the error. Must NOT be an ID of a PatchFunctionParameters tool call.",
    )
    reasoning: str = Field(
        ...,
        description="Think step-by-step, listing each validation error and the"
        " JSONPatch operation needed to correct it. "
        "Cite the fields in the JSONSchema you referenced in developing this plan.",
    )
    patches: list[JsonPatch] = Field(
        ...,
        description="A list of JSONPatch operations to be applied to the previous tool call's response.",
    )
