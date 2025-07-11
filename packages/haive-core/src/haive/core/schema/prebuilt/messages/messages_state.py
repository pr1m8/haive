# src/haive/core/graph/state/messages_state.py

from collections import defaultdict
from datetime import datetime
from functools import cached_property
from typing import (
    Annotated,
    Any,
    Callable,
    ClassVar,
    Dict,
    Iterator,
    List,
    Literal,
    Optional,
    Set,
    Tuple,
    Union,
)

import tiktoken
from langchain_core.messages import (
    AIMessage,
    AnyMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
    convert_to_messages,
    filter_messages,
    get_buffer_string,
)
from langchain_core.messages.base import message_to_dict
from langchain_core.messages.utils import convert_to_openai_messages, messages_from_dict
from langgraph.graph import END, add_messages
from langgraph.types import Send
from pydantic import (
    BaseModel,
    Field,
    RootModel,
    computed_field,
    field_validator,
    model_serializer,
    model_validator,
)

from haive.core.schema.state_schema import StateSchema


class ToolCallInfo(BaseModel):
    """Information about a completed tool call."""

    tool_call_id: str = Field(description="ID of the tool call")
    tool_call: Dict[str, Any] = Field(description="Original tool call object")
    tool_message: ToolMessage = Field(description="Corresponding tool message")
    ai_message: AIMessage = Field(description="AI message that made the tool call")
    is_successful: bool = Field(description="Whether the tool call was successful")
    timestamp: datetime = Field(default_factory=datetime.now)


class MessageRound(BaseModel):
    """Information about a conversation round."""

    round_number: int = Field(description="Round number (1-indexed)")
    human_message: HumanMessage = Field(
        description="The human message that started this round"
    )
    ai_responses: List[AIMessage] = Field(
        default_factory=list, description="AI responses in this round"
    )
    tool_calls: List[Dict[str, Any]] = Field(
        default_factory=list, description="Tool calls made in this round"
    )
    tool_responses: List[ToolMessage] = Field(
        default_factory=list, description="Tool responses in this round"
    )
    is_complete: bool = Field(
        default=False, description="Whether the round is complete"
    )
    has_errors: bool = Field(
        default=False, description="Whether the round has any tool errors"
    )


class MessageList(RootModel[List[AnyMessage]]):
    """
    Enhanced root model for managing conversation messages with advanced filtering,
    analysis, and transformation capabilities.

    Key Features:
    - Direct list access via .root
    - Computed properties for common queries (last_message, has_tool_calls, etc.)
    - Advanced filtering and message analysis
    - Tool call management with deduplication and error tracking
    - Message round counting and completion tracking
    - Sophisticated transformations with history tracking
    - Automatic string-to-message conversion
    - Comprehensive testing support
    """

    root: Annotated[List[AnyMessage], add_messages] = Field(
        default_factory=list,
        description="List of conversation messages with add_messages reducer",
    )

    # Class-level configuration for StateSchema compatibility
    __shared_fields__: ClassVar[List[str]] = ["root"]
    __serializable_reducers__: ClassVar[Dict[str, str]] = {"root": "add_messages"}
    __reducer_fields__: ClassVar[Dict[str, Callable]] = {"root": add_messages}

    # Tokenizer for message processing
    tokenizer: ClassVar = tiktoken.get_encoding("cl100k_base")

    @field_validator("root", mode="before")
    @classmethod
    def convert_strings_to_messages(cls, v: Any) -> List[AnyMessage]:
        """Automatically convert strings and dicts to proper Message objects."""
        if isinstance(v, str):
            # Single string -> HumanMessage
            return [HumanMessage(content=v)]
        elif isinstance(v, dict):
            if "messages" in v:
                # Handle legacy format with "messages" key
                messages_data = v["messages"]
                return cls._convert_message_data(messages_data)
            elif "root" in v:
                # Handle direct root format
                return cls._convert_message_data(v["root"])
            else:
                # Treat as single message dict
                return [messages_from_dict([v])[0]]
        elif isinstance(v, list):
            return cls._convert_message_data(v)
        elif hasattr(v, "__class__") and issubclass(
            v.__class__, (AIMessage, HumanMessage, SystemMessage, ToolMessage)
        ):
            return [v]

        return v or []

    @classmethod
    def _convert_message_data(cls, data: Any) -> List[AnyMessage]:
        """Convert various message data formats to AnyMessage list."""
        if isinstance(data, list):
            converted = []
            for item in data:
                if isinstance(item, str):
                    converted.append(HumanMessage(content=item))
                elif isinstance(item, dict):
                    # Convert dict to proper message type based on 'type' field
                    msg_type = item.get("type", "human")
                    if msg_type == "human":
                        converted.append(
                            HumanMessage(
                                **{k: v for k, v in item.items() if k != "type"}
                            )
                        )
                    elif msg_type == "ai":
                        converted.append(
                            AIMessage(**{k: v for k, v in item.items() if k != "type"})
                        )
                    elif msg_type == "system":
                        converted.append(
                            SystemMessage(
                                **{k: v for k, v in item.items() if k != "type"}
                            )
                        )
                    elif msg_type == "tool":
                        converted.append(
                            ToolMessage(
                                **{k: v for k, v in item.items() if k != "type"}
                            )
                        )
                    else:
                        # Fallback to convert_to_messages for other types
                        converted.append(convert_to_messages([item])[0])
                elif hasattr(item, "__class__") and issubclass(
                    item.__class__,
                    (AIMessage, HumanMessage, SystemMessage, ToolMessage),
                ):
                    # It's already a Message object
                    converted.append(item)
                else:
                    raise ValueError(f"Unsupported message type: {type(item)}")
            return converted
        elif isinstance(data, str):
            return [HumanMessage(content=data)]
        elif hasattr(data, "__class__") and issubclass(
            data.__class__, (AIMessage, HumanMessage, SystemMessage, ToolMessage)
        ):
            return [data]
        else:
            return convert_to_messages(data)

    @model_validator(mode="after")
    def ensure_proper_messages_and_ordering(self) -> "MessageList":
        """Ensure all messages are proper Message objects and system messages come before human."""
        # First ensure all items are proper Message objects
        # This handles cases where persistence returns dicts instead of Message objects
        for i, item in enumerate(self.root):
            if isinstance(item, dict):
                # Convert dict to proper message type
                msg_type = item.get("type", "human")
                if msg_type == "human":
                    self.root[i] = HumanMessage(
                        **{k: v for k, v in item.items() if k != "type"}
                    )
                elif msg_type == "ai":
                    self.root[i] = AIMessage(
                        **{k: v for k, v in item.items() if k != "type"}
                    )
                elif msg_type == "system":
                    self.root[i] = SystemMessage(
                        **{k: v for k, v in item.items() if k != "type"}
                    )
                elif msg_type == "tool":
                    self.root[i] = ToolMessage(
                        **{k: v for k, v in item.items() if k != "type"}
                    )
                else:
                    self.root[i] = convert_to_messages([item])[0]

        # Then handle ordering - ensure system messages come before human messages
        if len(self.root) < 2:
            return self

        messages = self.root
        i = 0
        while i < len(messages) - 1:
            current_msg = messages[i]
            next_msg = messages[i + 1]

            # If we find human followed by system, swap them
            if isinstance(current_msg, HumanMessage) and isinstance(
                next_msg, SystemMessage
            ):
                messages[i], messages[i + 1] = messages[i + 1], messages[i]
                i += 2  # Skip the next position since we just swapped
            else:
                i += 1

        return self

    # ============================================================================
    # COMPUTED PROPERTIES FOR EFFICIENT ACCESS
    # ============================================================================

    @computed_field
    # @cached_property
    def last_message(self) -> Optional[AnyMessage]:
        """Get the last message in the conversation."""
        return self.root[-1] if self.root else None

    @computed_field
    # @cached_property
    def last_human_message(self) -> Optional[HumanMessage]:
        """Get the last human message (including transformed ones)."""
        for msg in reversed(self.root):
            if isinstance(msg, HumanMessage):
                return msg
        return None

    @computed_field
    # @cached_property
    def last_ai_message(self) -> Optional[AIMessage]:
        """Get the last AI message."""
        for msg in reversed(self.root):
            if isinstance(msg, AIMessage):
                return msg
        return None

    @computed_field
    # @cached_property
    def first_real_human_message(self) -> Optional[HumanMessage]:
        """Get the first real human message (not transformed)."""
        for msg in self.root:
            if isinstance(msg, HumanMessage) and self._is_real_human_message(msg):
                return msg
        return None

    @computed_field
    # @cached_property
    def system_message(self) -> Optional[SystemMessage]:
        """Get the first system message if one exists."""
        for msg in self.root:
            if isinstance(msg, SystemMessage):
                return msg
        return None

    @computed_field
    # @cached_property
    def has_tool_calls(self) -> bool:
        """Check if the last AI message has tool calls."""
        last_ai = self.last_ai_message
        if not last_ai:
            return False

        # Check for tool_calls attribute
        if hasattr(last_ai, "tool_calls") and last_ai.tool_calls:
            return True

        # Also check in additional_kwargs
        if hasattr(last_ai, "additional_kwargs") and last_ai.additional_kwargs.get(
            "tool_calls"
        ):
            return True

        return False

    @computed_field
    # @cached_property
    def has_tool_errors(self) -> bool:
        """Check if there are any tool messages with errors."""
        for msg in self.root:
            if isinstance(msg, ToolMessage) and self._is_tool_error(msg):
                return True
        return False

    @computed_field
    @cached_property
    def message_count(self) -> int:
        """Total number of messages."""
        return len(self.root)

    @computed_field
    @cached_property
    def round_count(self) -> int:
        """Number of complete conversation rounds."""
        return self._count_message_rounds()

    @computed_field
    @cached_property
    def tool_call_errors(self) -> List[ToolMessage]:
        """Get all tool messages with errors."""
        return [
            msg
            for msg in self.root
            if isinstance(msg, ToolMessage) and self._is_tool_error(msg)
        ]

    @computed_field
    @cached_property
    def completed_tool_calls(self) -> List[ToolCallInfo]:
        """Get all completed tool calls with their responses."""
        return self._get_completed_tool_calls()

    @computed_field
    @cached_property
    def conversation_rounds(self) -> List[MessageRound]:
        """Get detailed information about each conversation round."""
        return self._get_conversation_rounds()

    @computed_field
    @cached_property
    def real_human_messages(self) -> List[HumanMessage]:
        """Get only real human messages (not transformed)."""
        return [
            msg
            for msg in self.root
            if isinstance(msg, HumanMessage) and self._is_real_human_message(msg)
        ]

    @computed_field
    @cached_property
    def transformed_human_messages(self) -> List[HumanMessage]:
        """Get human messages that were transformed from AI messages."""
        return [
            msg
            for msg in self.root
            if isinstance(msg, HumanMessage) and not self._is_real_human_message(msg)
        ]

    # ============================================================================
    # LIST-LIKE INTERFACE WITH CACHE INVALIDATION
    # ============================================================================

    def __iter__(self) -> Iterator[AnyMessage]:
        """Make the root model iterable."""
        return iter(self.root)

    def __len__(self) -> int:
        """Get the length of the messages list."""
        return len(self.root)

    def __getitem__(
        self, index: Union[int, slice]
    ) -> Union[AnyMessage, List[AnyMessage]]:
        """Support indexing and slicing."""
        return self.root[index]

    def __setitem__(self, index: int, value: Union[AnyMessage, str]) -> None:
        """Support item assignment with auto-conversion."""
        if isinstance(value, str):
            value = HumanMessage(content=value)
        self.root[index] = value
        self._invalidate_cache()

    def append(self, message: Union[AnyMessage, str]) -> None:
        """Append a message to the list with auto-conversion."""
        if isinstance(message, str):
            message = HumanMessage(content=message)
        self.root.append(message)
        self._invalidate_cache()

    def extend(self, messages: List[Union[AnyMessage, str]]) -> None:
        """Extend the list with multiple messages with auto-conversion."""
        converted = [
            HumanMessage(content=msg) if isinstance(msg, str) else msg
            for msg in messages
        ]
        self.root.extend(converted)
        self._invalidate_cache()

    def insert(self, index: int, message: Union[AnyMessage, str]) -> None:
        """Insert a message at a specific index with auto-conversion."""
        if isinstance(message, str):
            message = HumanMessage(content=message)
        self.root.insert(index, message)
        self._invalidate_cache()

    def remove(self, message: AnyMessage) -> None:
        """Remove a message from the list."""
        self.root.remove(message)
        self._invalidate_cache()

    def clear(self) -> None:
        """Clear all messages."""
        self.root.clear()
        self._invalidate_cache()

    def copy(self) -> List[AnyMessage]:
        """Create a copy of the messages list."""
        return self.root.copy()

    def _invalidate_cache(self) -> None:
        """Invalidate cached properties when messages change."""
        # Clear cached properties
        for attr in [
            "last_message",
            "last_human_message",
            "last_ai_message",
            "first_real_human_message",
            "system_message",
            "has_tool_calls",
            "has_tool_errors",
            "message_count",
            "round_count",
            "tool_call_errors",
            "completed_tool_calls",
            "conversation_rounds",
            "real_human_messages",
            "transformed_human_messages",
        ]:
            if hasattr(self, f"_{attr}"):
                delattr(self, f"_{attr}")

    # ============================================================================
    # ADVANCED FILTERING
    # ============================================================================

    def filter_by_type(self, message_type: Union[type, List[type]]) -> List[AnyMessage]:
        """Filter messages by type(s)."""
        if not isinstance(message_type, list):
            message_type = [message_type]

        return [msg for msg in self.root if isinstance(msg, tuple(message_type))]

    def filter_by_content_pattern(
        self, pattern: str, case_sensitive: bool = False
    ) -> List[AnyMessage]:
        """Filter messages by content pattern."""
        import re

        flags = 0 if case_sensitive else re.IGNORECASE

        return [
            msg
            for msg in self.root
            if hasattr(msg, "content") and re.search(pattern, msg.content, flags)
        ]

    def filter_by_metadata(self, key: str, value: Any = None) -> List[AnyMessage]:
        """Filter messages by metadata key/value."""
        filtered = []
        for msg in self.root:
            if hasattr(msg, "additional_kwargs") and msg.additional_kwargs:
                if value is None:
                    # Just check for key existence
                    if key in msg.additional_kwargs:
                        filtered.append(msg)
                else:
                    # Check for key and value
                    if msg.additional_kwargs.get(key) == value:
                        filtered.append(msg)
        return filtered

    def filter_by_engine(
        self, engine_id: Optional[str] = None, engine_name: Optional[str] = None
    ) -> List[AnyMessage]:
        """Filter messages by engine ID or name."""
        filtered = []
        for msg in self.root:
            if hasattr(msg, "additional_kwargs") and msg.additional_kwargs:
                if engine_id and msg.additional_kwargs.get("engine_id") == engine_id:
                    filtered.append(msg)
                elif (
                    engine_name
                    and msg.additional_kwargs.get("engine_name") == engine_name
                ):
                    filtered.append(msg)
        return filtered

    def filter_by_time_range(
        self, start_index: int = 0, end_index: Optional[int] = None
    ) -> List[AnyMessage]:
        """Filter messages by index range (time-based ordering)."""
        if end_index is None:
            end_index = len(self.root)

        return self.root[start_index:end_index]

    def get_messages_since_last_human(
        self, include_human: bool = True
    ) -> List[AnyMessage]:
        """Get all messages since the last real human message."""
        if not self.last_human_message:
            return []

        # Find the index of the last human message
        last_human_idx = None
        for i in reversed(range(len(self.root))):
            if self.root[i] is self.last_human_message:
                last_human_idx = i
                break

        if last_human_idx is None:
            return []

        start_idx = last_human_idx if include_human else last_human_idx + 1
        return self.root[start_idx:]

    def get_messages_in_current_round(self) -> List[AnyMessage]:
        """Get all messages in the current (potentially incomplete) round."""
        if not self.conversation_rounds:
            return []

        current_round = self.conversation_rounds[-1]
        messages = [current_round.human_message]
        messages.extend(current_round.ai_responses)
        messages.extend(current_round.tool_responses)

        return messages

    # ============================================================================
    # TOOL CALL MANAGEMENT
    # ============================================================================

    def deduplicate_tool_calls(self) -> int:
        """
        Remove duplicate tool calls based on tool call ID.

        Returns:
            Number of duplicates removed
        """
        seen_tool_call_ids = set()
        duplicates_removed = 0

        for msg in self.root:
            if (
                isinstance(msg, AIMessage)
                and hasattr(msg, "tool_calls")
                and msg.tool_calls
            ):
                unique_tool_calls = []
                for tool_call in msg.tool_calls:
                    # Handle different tool call formats
                    if isinstance(tool_call, dict):
                        tool_call_id = tool_call.get("id")
                    else:
                        tool_call_id = getattr(tool_call, "id", None)

                    if tool_call_id and tool_call_id not in seen_tool_call_ids:
                        unique_tool_calls.append(tool_call)
                        seen_tool_call_ids.add(tool_call_id)
                    elif tool_call_id and tool_call_id in seen_tool_call_ids:
                        duplicates_removed += 1
                    elif not tool_call_id:
                        # If no ID, keep it (can't deduplicate)
                        unique_tool_calls.append(tool_call)

                msg.tool_calls = unique_tool_calls

        if duplicates_removed > 0:
            self._invalidate_cache()

        return duplicates_removed

    def get_tool_calls_from_message(
        self, message: Optional[AIMessage] = None
    ) -> List[Dict]:
        """Get tool calls from an AI message."""
        msg = message or self.last_ai_message
        if not msg:
            return []

        # Check direct tool_calls attribute
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            return msg.tool_calls

        # Check in additional_kwargs
        if hasattr(msg, "additional_kwargs") and msg.additional_kwargs.get(
            "tool_calls"
        ):
            return msg.additional_kwargs["tool_calls"]

        return []

    def get_pending_tool_calls(self) -> List[Dict[str, Any]]:
        """Get tool calls that don't have corresponding responses yet."""
        all_tool_calls = {}
        tool_responses = set()

        # Collect all tool calls
        for msg in self.root:
            if (
                isinstance(msg, AIMessage)
                and hasattr(msg, "tool_calls")
                and msg.tool_calls
            ):
                for tool_call in msg.tool_calls:
                    tool_call_id = getattr(tool_call, "id", None)
                    if tool_call_id:
                        all_tool_calls[tool_call_id] = {
                            "tool_call": tool_call,
                            "ai_message": msg,
                        }

        # Collect all tool responses
        for msg in self.root:
            if isinstance(msg, ToolMessage):
                tool_call_id = getattr(msg, "tool_call_id", None)
                if tool_call_id:
                    tool_responses.add(tool_call_id)

        # Return tool calls without responses
        pending = []
        for tool_call_id, info in all_tool_calls.items():
            if tool_call_id not in tool_responses:
                pending.append(info)

        return pending

    def inject_state_into_tool_calls(
        self, tool_calls: List[Dict], state_data: Optional[Dict[str, Any]] = None
    ) -> List[Dict]:
        """Inject state data into tool call arguments."""
        if not tool_calls:
            return []

        # Default state data
        if state_data is None:
            state_data = {"messages": self.root}

        # Inject state into each tool call
        injected_calls = []
        for call in tool_calls:
            call_copy = call.copy()

            if "args" not in call_copy or not isinstance(call_copy["args"], dict):
                call_copy["args"] = {}

            if "_state" not in call_copy["args"]:
                call_copy["args"]["_state"] = state_data

            injected_calls.append(call_copy)

        return injected_calls

    def send_tool_calls(self, node_name: str = "tools") -> Union[str, List[Send]]:
        """Convert tool calls from the last AI message into Send objects."""
        tool_calls = self.get_tool_calls_from_message()
        if not tool_calls:
            return END

        # Inject state into tool calls
        injected_calls = self.inject_state_into_tool_calls(tool_calls)

        # Create a Send object for each tool call
        return [Send(node_name, tool_call) for tool_call in injected_calls]

    # ============================================================================
    # HELPER METHODS
    # ============================================================================

    def _is_real_human_message(self, msg: HumanMessage) -> bool:
        """Check if a human message is real (not transformed)."""
        has_name = hasattr(msg, "name") and msg.name is not None
        has_engine_metadata = self._has_engine_metadata(msg)
        has_agent_metadata = self._has_agent_metadata(msg)

        return not (has_name or has_engine_metadata or has_agent_metadata)

    def _has_engine_metadata(self, msg: AnyMessage) -> bool:
        """Check if message has engine-related metadata."""
        if not hasattr(msg, "additional_kwargs") or not msg.additional_kwargs:
            return False
        return (
            "engine_id" in msg.additional_kwargs
            or "engine_name" in msg.additional_kwargs
        )

    def _has_agent_metadata(self, msg: AnyMessage) -> bool:
        """Check if message has agent-related metadata."""
        if not hasattr(msg, "additional_kwargs") or not msg.additional_kwargs:
            return False
        return "source_agent" in msg.additional_kwargs

    def _is_tool_error(self, msg: ToolMessage) -> bool:
        """Check if a tool message represents an error."""
        if hasattr(msg, "additional_kwargs") and msg.additional_kwargs:
            return msg.additional_kwargs.get("is_error", False)
        return False

    def _count_message_rounds(self) -> int:
        """Count the number of human->AI message rounds."""
        rounds = 0
        expecting_ai = False

        for msg in self.root:
            if isinstance(msg, HumanMessage) and self._is_real_human_message(msg):
                expecting_ai = True
            elif isinstance(msg, AIMessage) and expecting_ai:
                rounds += 1
                expecting_ai = False

        return rounds

    def _get_completed_tool_calls(self) -> List[ToolCallInfo]:
        """Get all completed tool calls with their responses."""
        completed = []

        # Build a mapping of tool call IDs to their messages
        tool_messages = {}
        for msg in self.root:
            if isinstance(msg, ToolMessage):
                tool_call_id = getattr(msg, "tool_call_id", None)
                if tool_call_id:
                    is_error = self._is_tool_error(msg)
                    tool_messages[tool_call_id] = {"message": msg, "is_error": is_error}

        # Find AI messages with tool calls and match them to tool messages
        for msg in self.root:
            if (
                isinstance(msg, AIMessage)
                and hasattr(msg, "tool_calls")
                and msg.tool_calls
            ):
                for tool_call in msg.tool_calls:
                    # Handle different tool call formats
                    if isinstance(tool_call, dict):
                        tool_call_id = tool_call.get("id")
                    else:
                        tool_call_id = getattr(tool_call, "id", None)

                    if tool_call_id and tool_call_id in tool_messages:
                        tool_msg_info = tool_messages[tool_call_id]
                        completed.append(
                            ToolCallInfo(
                                tool_call_id=tool_call_id,
                                tool_call=tool_call,
                                tool_message=tool_msg_info["message"],
                                ai_message=msg,
                                is_successful=not tool_msg_info["is_error"],
                            )
                        )

        return completed

    def _get_conversation_rounds(self) -> List[MessageRound]:
        """Get detailed information about each conversation round."""
        rounds = []
        current_round = None
        round_number = 0

        for msg in self.root:
            if isinstance(msg, HumanMessage) and self._is_real_human_message(msg):
                # Start a new round
                if current_round:
                    current_round.is_complete = self._is_round_complete(current_round)
                    rounds.append(current_round)

                round_number += 1
                current_round = MessageRound(
                    round_number=round_number, human_message=msg
                )

            elif current_round:
                if isinstance(msg, AIMessage):
                    current_round.ai_responses.append(msg)

                    # Track tool calls
                    if hasattr(msg, "tool_calls") and msg.tool_calls:
                        current_round.tool_calls.extend(msg.tool_calls)

                elif isinstance(msg, ToolMessage):
                    current_round.tool_responses.append(msg)

                    # Check for errors
                    if self._is_tool_error(msg):
                        current_round.has_errors = True

        # Add the last round if it exists
        if current_round:
            current_round.is_complete = self._is_round_complete(current_round)
            rounds.append(current_round)

        return rounds

    def _is_round_complete(self, round_info: MessageRound) -> bool:
        """Check if a conversation round is complete."""
        # A round is complete if:
        # 1. There's at least one AI response
        # 2. All tool calls have corresponding responses (if any)

        if not round_info.ai_responses:
            return False

        tool_call_ids = set()
        for tool_call in round_info.tool_calls:
            if hasattr(tool_call, "id"):
                tool_call_ids.add(tool_call.id)

        tool_response_ids = set()
        for tool_response in round_info.tool_responses:
            if hasattr(tool_response, "tool_call_id"):
                tool_response_ids.add(tool_response.tool_call_id)

        # Round is complete if all tool calls have responses
        return tool_call_ids.issubset(tool_response_ids)

    # ============================================================================
    # MESSAGE TRANSFORMATIONS
    # ============================================================================

    def transform_ai_to_human(
        self,
        preserve_metadata: bool = True,
        engine_id: Optional[str] = None,
        engine_name: Optional[str] = None,
    ) -> None:
        """Transform AI messages to Human messages in place."""
        transformed_messages = []

        for msg in self.root:
            if isinstance(msg, AIMessage):
                kwargs = {"content": msg.content}

                if preserve_metadata:
                    if hasattr(msg, "additional_kwargs") and msg.additional_kwargs:
                        kwargs["additional_kwargs"] = msg.additional_kwargs.copy()

                    if engine_id or engine_name:
                        if "additional_kwargs" not in kwargs:
                            kwargs["additional_kwargs"] = {}
                        if engine_id:
                            kwargs["additional_kwargs"]["engine_id"] = engine_id
                        if engine_name:
                            kwargs["additional_kwargs"]["engine_name"] = engine_name

                    if hasattr(msg, "name") and msg.name:
                        kwargs["name"] = msg.name

                transformed_messages.append(HumanMessage(**kwargs))
            else:
                transformed_messages.append(msg)

        self.root = transformed_messages
        self._invalidate_cache()

    def transform_for_reflection(self, preserve_first: bool = True) -> None:
        """Apply reflection transformation: swap AI ↔ Human roles."""
        if not self.root:
            return

        transformed = []

        # Class mapping for role swapping
        cls_map = {"ai": HumanMessage, "human": AIMessage}

        # Preserve first message if requested
        if preserve_first and len(self.root) > 0:
            transformed.append(self.root[0])
            start_idx = 1
        else:
            start_idx = 0

        # Transform remaining messages with role swap
        for msg in self.root[start_idx:]:
            if msg.type in cls_map:
                target_cls = cls_map[msg.type]
                kwargs = {"content": msg.content}

                if hasattr(msg, "additional_kwargs") and msg.additional_kwargs:
                    kwargs["additional_kwargs"] = msg.additional_kwargs.copy()

                if hasattr(msg, "name") and msg.name:
                    kwargs["name"] = msg.name

                transformed.append(target_cls(**kwargs))
            else:
                # Keep non-human/ai messages unchanged
                transformed.append(msg)

        self.root = transformed
        self._invalidate_cache()

    def transform_for_agent_handoff(
        self,
        source_agent: Optional[str] = None,
        exclude_system: bool = True,
        exclude_tools: bool = False,
    ) -> None:
        """Transform messages for agent-to-agent communication."""
        transformed = []

        for msg in self.root:
            # Skip system messages (they're agent-specific)
            if exclude_system and isinstance(msg, SystemMessage):
                continue

            # Skip tool messages if requested
            if exclude_tools and isinstance(msg, ToolMessage):
                continue

            # Convert AI messages to Human messages for the receiving agent
            if isinstance(msg, AIMessage):
                kwargs = {"content": msg.content}

                if hasattr(msg, "additional_kwargs") and msg.additional_kwargs:
                    kwargs["additional_kwargs"] = msg.additional_kwargs.copy()
                else:
                    kwargs["additional_kwargs"] = {}

                # Add source agent name
                if source_agent:
                    kwargs["additional_kwargs"]["source_agent"] = source_agent

                transformed.append(HumanMessage(**kwargs))
            else:
                # Keep human messages and other types
                transformed.append(msg)

        self.root = transformed
        self._invalidate_cache()

    # ============================================================================
    # UTILITY METHODS
    # ============================================================================

    def add_message(self, message: Union[AnyMessage, str, Dict]) -> None:
        """Add a message to the conversation with auto-conversion."""
        if isinstance(message, str):
            message = HumanMessage(content=message)
        elif isinstance(message, dict):
            message = messages_from_dict([message])[0]

        self.append(message)

    def add_system_message(
        self, content: str, metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Add a system message at the beginning of the conversation."""
        kwargs = {"content": content}
        if metadata:
            kwargs["additional_kwargs"] = metadata

        system_msg = SystemMessage(**kwargs)

        # Remove existing system messages
        self.root = [msg for msg in self.root if not isinstance(msg, SystemMessage)]

        # Add at the beginning
        self.insert(0, system_msg)

    def add_engine_metadata(
        self, engine_id: Optional[str] = None, engine_name: Optional[str] = None
    ) -> None:
        """Add engine metadata to all AI messages."""
        for msg in self.root:
            if isinstance(msg, AIMessage):
                if not hasattr(msg, "additional_kwargs"):
                    msg.additional_kwargs = {}
                elif msg.additional_kwargs is None:
                    msg.additional_kwargs = {}

                if engine_id:
                    msg.additional_kwargs["engine_id"] = engine_id
                if engine_name:
                    msg.additional_kwargs["engine_name"] = engine_name

    # ============================================================================
    # FORMAT CONVERSION
    # ============================================================================

    def to_openai_format(self) -> List[Dict]:
        """Convert messages to OpenAI API format."""
        return convert_to_openai_messages(self.root)

    def to_langchain_prompt(self) -> str:
        """Convert message history to LangChain compatible prompt string."""
        return get_buffer_string(self.root, human_prefix="User", ai_prefix="Assistant")

    def get_filtered_messages(self, **filter_kwargs) -> List[AnyMessage]:
        """Filter messages using LangChain's built-in filter_messages utility."""
        limit = filter_kwargs.pop("limit", None)
        filtered_messages = filter_messages(self.root, **filter_kwargs)

        if limit is not None and limit > 0:
            return filtered_messages[-limit:]

        return filtered_messages

    # ============================================================================
    # STATIC CONSTRUCTORS
    # ============================================================================

    @classmethod
    def from_messages(cls, messages: List[Union[AnyMessage, str]]) -> "MessageList":
        """Create instance from a list of messages."""
        return cls(root=messages)

    @classmethod
    def from_dict(cls, data: Union[List[Dict], Dict[str, Any]]) -> "MessageList":
        """Create instance from dictionary format."""
        if isinstance(data, dict) and "messages" in data:
            return cls(root=data["messages"])
        elif isinstance(data, list):
            return cls(root=data)
        else:
            return cls()

    @classmethod
    def with_system_message(cls, system_content: str) -> "MessageList":
        """Create a new state with a system message."""
        state = cls()
        state.add_system_message(system_content)
        return state

    @classmethod
    def from_string(cls, content: str) -> "MessageList":
        """Create instance from a single string."""
        return cls(root=[HumanMessage(content=content)])

    # ============================================================================
    # COMPATIBILITY WITH LANGGRAPH REDUCERS
    # ============================================================================

    @model_serializer
    def serialize_model(self):
        """Custom serializer to properly handle MessageList for LangGraph compatibility."""
        # Get the root list - handle both MessageList objects and plain lists
        messages = self.root if hasattr(self, "root") else self

        # Use LangChain's built-in serialization with proper BaseMessage checking
        serialized_messages = []
        for msg in messages:
            if isinstance(msg, BaseMessage):
                # Use serialize_as_any to ensure all fields are preserved
                msg_dict = msg.model_dump(serialize_as_any=True)

                # For ToolMessage, ensure tool_call_id is preserved explicitly
                if isinstance(msg, ToolMessage) and hasattr(msg, "tool_call_id"):
                    msg_dict["tool_call_id"] = msg.tool_call_id

                # Preserve engine metadata from additional_kwargs at top level
                if hasattr(msg, "additional_kwargs") and msg.additional_kwargs:
                    # Check for engine_name, engine_id and other metadata
                    engine_fields = ["engine_name", "engine_id"]
                    for field in engine_fields:
                        if field in msg.additional_kwargs:
                            msg_dict[field] = msg.additional_kwargs[field]

                serialized_messages.append(msg_dict)
            elif isinstance(msg, dict):
                # Already serialized
                serialized_messages.append(msg)
            else:
                # For non-BaseMessage objects, serialize as-is
                serialized_messages.append(msg)
        return serialized_messages

    def __add__(self, other):
        """Support addition for LangGraph reducers."""
        if isinstance(other, MessageList):
            return MessageList(root=add_messages(self.root, other.root))
        elif isinstance(other, list):
            return MessageList(root=add_messages(self.root, other))
        return NotImplemented


class MessagesState(StateSchema):
    """
    Enhanced state schema that uses MessageList as a field.

    Use this when you need additional state fields beyond just messages.
    """

    messages: MessageList = Field(
        default_factory=MessageList,
        description="Conversation messages using enhanced MessageList",
    )

    # Additional state fields
    transformation_history: List[Dict[str, Any]] = Field(
        default_factory=list, description="History of transformations applied"
    )

    # Configuration for LangGraph compatibility
    __shared_fields__ = ["messages"]
    __serializable_reducers__ = {"messages": "add_messages"}
    __reducer_fields__ = {"messages": add_messages}

    def __init__(self, messages=None, **data):
        """Initialize with optional messages parameter for compatibility."""
        if messages is not None and "messages" not in data:
            # Handle direct list/string initialization
            data["messages"] = messages
        super().__init__(**data)

    # ============================================================================
    # DELEGATED PROPERTIES - Use @property instead of @computed_field
    # ============================================================================

    @property
    def last_message(self) -> Optional[AnyMessage]:
        """Delegate to messages state."""
        return self.messages.last_message

    @property
    def last_human_message(self) -> Optional[HumanMessage]:
        """Delegate to messages state."""
        return self.messages.last_human_message

    @property
    def last_ai_message(self) -> Optional[AIMessage]:
        """Delegate to messages state."""
        return self.messages.last_ai_message

    @property
    def first_real_human_message(self) -> Optional[HumanMessage]:
        """Delegate to messages state."""
        return self.messages.first_real_human_message

    @property
    def system_message(self) -> Optional[SystemMessage]:
        """Delegate to messages state."""
        return self.messages.system_message

    @property
    def has_tool_calls(self) -> bool:
        """Delegate to messages state."""
        return self.messages.has_tool_calls

    @property
    def has_tool_errors(self) -> bool:
        """Delegate to messages state."""
        return self.messages.has_tool_errors

    @property
    def message_count(self) -> int:
        """Delegate to messages state."""
        return self.messages.message_count

    @property
    def round_count(self) -> int:
        """Delegate to messages state."""
        return self.messages.round_count

    @property
    def tool_call_errors(self) -> List[ToolMessage]:
        """Delegate to messages state."""
        return self.messages.tool_call_errors

    @property
    def completed_tool_calls(self) -> List[ToolCallInfo]:
        """Delegate to messages state."""
        return self.messages.completed_tool_calls

    @property
    def conversation_rounds(self) -> List[MessageRound]:
        """Delegate to messages state."""
        return self.messages.conversation_rounds

    @property
    def real_human_messages(self) -> List[HumanMessage]:
        """Delegate to messages state."""
        return self.messages.real_human_messages

    @property
    def transformed_human_messages(self) -> List[HumanMessage]:
        """Delegate to messages state."""
        return self.messages.transformed_human_messages

    # ============================================================================
    # DELEGATED LIST-LIKE METHODS
    # ============================================================================

    def __iter__(self) -> Iterator[AnyMessage]:
        """Make MessagesState iterable."""
        return iter(self.messages)

    def __len__(self) -> int:
        """Get the length of messages."""
        return len(self.messages)

    def __getitem__(
        self, index: Union[int, slice]
    ) -> Union[AnyMessage, List[AnyMessage]]:
        """Support indexing and slicing."""
        return self.messages[index]

    def __setitem__(self, index: int, value: Union[AnyMessage, str]) -> None:
        """Support item assignment."""
        self.messages[index] = value

    def append(self, message: Union[AnyMessage, str]) -> None:
        """Append a message."""
        self.messages.append(message)

    def extend(self, messages: List[Union[AnyMessage, str]]) -> None:
        """Extend with multiple messages."""
        self.messages.extend(messages)

    def insert(self, index: int, message: Union[AnyMessage, str]) -> None:
        """Insert a message at index."""
        self.messages.insert(index, message)

    def remove(self, message: AnyMessage) -> None:
        """Remove a message."""
        self.messages.remove(message)

    def clear(self) -> None:
        """Clear all messages."""
        self.messages.clear()

    # ============================================================================
    # DELEGATED METHODS
    # ============================================================================

    def add_message(self, message: Union[AnyMessage, str, Dict]) -> None:
        """Delegate to messages state."""
        self.messages.add_message(message)

    def deduplicate_tool_calls(self) -> int:
        """Delegate to messages state."""
        return self.messages.deduplicate_tool_calls()

    def get_pending_tool_calls(self) -> List[Dict[str, Any]]:
        """Delegate to messages state."""
        return self.messages.get_pending_tool_calls()

    def filter_by_type(self, message_type: Union[type, List[type]]) -> List[AnyMessage]:
        """Delegate to messages state."""
        return self.messages.filter_by_type(message_type)

    def filter_by_content_pattern(
        self, pattern: str, case_sensitive: bool = False
    ) -> List[AnyMessage]:
        """Delegate to messages state."""
        return self.messages.filter_by_content_pattern(pattern, case_sensitive)

    def filter_by_metadata(self, key: str, value: Any = None) -> List[AnyMessage]:
        """Delegate to messages state."""
        return self.messages.filter_by_metadata(key, value)

    def filter_by_engine(
        self, engine_id: Optional[str] = None, engine_name: Optional[str] = None
    ) -> List[AnyMessage]:
        """Delegate to messages state."""
        return self.messages.filter_by_engine(engine_id, engine_name)

    def get_messages_since_last_human(
        self, include_human: bool = True
    ) -> List[AnyMessage]:
        """Delegate to messages state."""
        return self.messages.get_messages_since_last_human(include_human)

    def transform_ai_to_human(
        self,
        preserve_metadata: bool = True,
        engine_id: Optional[str] = None,
        engine_name: Optional[str] = None,
    ) -> None:
        """Delegate to messages state."""
        self.messages.transform_ai_to_human(preserve_metadata, engine_id, engine_name)

    def transform_for_reflection(self, preserve_first: bool = True) -> None:
        """Delegate to messages state."""
        self.messages.transform_for_reflection(preserve_first)

    def transform_for_agent_handoff(
        self,
        source_agent: Optional[str] = None,
        exclude_system: bool = True,
        exclude_tools: bool = False,
    ) -> None:
        """Delegate to messages state."""
        self.messages.transform_for_agent_handoff(
            source_agent, exclude_system, exclude_tools
        )

    def add_system_message(
        self, content: str, metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Delegate to messages state."""
        self.messages.add_system_message(content, metadata)

    def add_engine_metadata(
        self, engine_id: Optional[str] = None, engine_name: Optional[str] = None
    ) -> None:
        """Delegate to messages state."""
        self.messages.add_engine_metadata(engine_id, engine_name)

    # ============================================================================
    # STATIC CONSTRUCTORS
    # ============================================================================

    @classmethod
    def from_messages(cls, messages: List[Union[AnyMessage, str]]) -> "MessagesState":
        """Create instance from a list of messages."""
        return cls(messages=messages)

    @classmethod
    def from_dict(cls, data: Union[List[Dict], Dict[str, Any]]) -> "MessagesState":
        """Create instance from dictionary format."""
        if isinstance(data, dict) and "messages" in data:
            return cls(**data)
        elif isinstance(data, list):
            return cls(messages=data)
        else:
            return cls()

    @classmethod
    def with_system_message(cls, system_content: str) -> "MessagesState":
        """Create a new state with a system message."""
        state = cls()
        state.add_system_message(system_content)
        return state

    @classmethod
    def from_string(cls, content: str) -> "MessagesState":
        """Create instance from a single string."""
        return cls(messages=[content])
