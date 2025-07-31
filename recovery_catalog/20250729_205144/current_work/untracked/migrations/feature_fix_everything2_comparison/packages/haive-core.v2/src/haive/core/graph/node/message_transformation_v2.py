"""Message_Transformation_V2 graph module.

This module provides message transformation v2 functionality for the Haive framework.

Classes:
    TransformationType: TransformationType implementation.
    MessageTransformationNodeConfig: MessageTransformationNodeConfig implementation.
    target_cls: target_cls implementation.

Functions:
    validate_transformation_config: Validate Transformation Config functionality.
    get_default_input_fields: Get Default Input Fields functionality.
    get_default_output_fields: Get Default Output Fields functionality.
"""

# ============================================================================
# MESSAGE TRANSFORMATION NODE CONFIG V2 - WITH SCHEMA SUPPORT
# ============================================================================

import logging
from collections.abc import Callable
from enum import Enum
from typing import Any, Optional, Self, TypeVar

from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langgraph.types import Command
from pydantic import BaseModel, Field, model_validator
from rich.console import Console

from haive.core.graph.common.types import ConfigLike, NodeType, StateLike
from haive.core.graph.node.base_node_config import BaseNodeConfig
from haive.core.schema.field_definition import FieldDefinition
from haive.core.schema.field_registry import StandardFields

logger = logging.getLogger(__name__)
console = Console()

# Type variables for input/output schemas
TInput = TypeVar("TInput", bound=BaseModel)
TOutput = TypeVar("TOutput", bound=BaseModel)


class TransformationType(str, Enum):
    """Types of message transformations available."""

    AI_TO_HUMAN = "ai_to_human"
    HUMAN_TO_AI = "human_to_ai"
    REFLECTION = "reflection"
    AGENT_TO_AGENT = "agent_to_agent"
    ADD_ENGINE_ID = "add_engine_id"
    EXTRACT_FIRST_HUMAN = "extract_first_human"
    FILTER_BY_TYPE = "filter_by_type"
    MERGE_CONSECUTIVE = "merge_consecutive"
    CUSTOM = "custom"


class MessageTransformationNodeConfig(BaseNodeConfig[TInput, TOutput]):
    """Configuration for a node that transforms messages in various ways.

    Supports multiple transformation types including role swapping,
    metadata manipulation, and agent-to-agent communication.

    Input Schema Requirements:
    - Must have a messages field (List[BaseMessage]) or custom messages field

    Output Schema:
    - Will contain the transformed messages field
    - Optional error field for transformation failures
    """

    node_type: NodeType = Field(default=NodeType.MESSAGE_TRANSFORMER)

    # Core transformation configuration
    transformation_type: TransformationType = Field(
        description="Type of transformation to apply"
    )

    # Field names
    messages_field: str = Field(
        default="messages", description="Name of the messages field in input schema"
    )

    output_field: str | None = Field(
        default=None,
        description="Name of the output field in output schema (defaults to messages_field)",
    )

    error_field: str = Field(
        default="transformation_error",
        description="Name of the error field in output schema",
    )

    # Engine ID configuration
    engine_id: str | None = Field(
        default=None,
        description="Engine ID to add to messages (for ADD_ENGINE_ID transformation)",
    )

    # Engine name configuration
    engine_name: str | None = Field(
        default=None,
        description="Engine name to add to messages (for engine attribution)",
    )

    # Filtering configuration
    preserve_first_message: bool = Field(
        default=True,
        description="Whether to preserve the first message unchanged (for REFLECTION)",
    )

    exclude_system_messages: bool = Field(
        default=False,
        description="Whether to exclude system messages from transformation",
    )

    exclude_tool_messages: bool = Field(
        default=False,
        description="Whether to exclude tool messages from transformation",
    )

    # Filter by type configuration
    include_types: list[str] | None = Field(
        default=None, description="Message types to include (for FILTER_BY_TYPE)"
    )

    exclude_types: list[str] | None = Field(
        default=None, description="Message types to exclude (for FILTER_BY_TYPE)"
    )

    # Agent-specific configuration
    agent_name: str | None = Field(
        default=None,
        description="Agent name for filtering (for AGENT_TO_AGENT transformation)",
    )

    # Custom transformation
    custom_transformer: Callable[[list[BaseMessage]], list[BaseMessage]] | None = Field(
        default=None, description="Custom transformation function", exclude=True
    )

    # Additional options
    preserve_metadata: bool = Field(
        default=True,
        description="Whether to preserve message metadata during transformation",
    )

    debug: bool = Field(default=False, description="Enable debug output")

    @model_validator(mode="after")
    def validate_transformation_config(self) -> Self:
        """Validate transformation-specific configuration."""
        if (
            self.transformation_type == TransformationType.ADD_ENGINE_ID
            and not self.engine_id
            and not self.engine_name
        ):
            raise ValueError(
                "engine_id or engine_name is required for ADD_ENGINE_ID transformation"
            )

        if (
            self.transformation_type == TransformationType.CUSTOM
            and not self.custom_transformer
        ):
            raise ValueError("custom_transformer is required for CUSTOM transformation")

        if self.transformation_type == TransformationType.FILTER_BY_TYPE:
            if not self.include_types and not self.exclude_types:
                raise ValueError(
                    "Either include_types or exclude_types must be set for FILTER_BY_TYPE"
                )

        return self

    def get_default_input_fields(self) -> list[FieldDefinition]:
        """Get default input field definitions."""
        return [StandardFields.messages(use_enhanced=True)]

    def get_default_output_fields(self) -> list[FieldDefinition]:
        """Get default output field definitions."""
        output_field_name = self.output_field or self.messages_field

        fields = [
            FieldDefinition(
                name=output_field_name,
                field_type=list[BaseMessage],
                default_factory=list,
                description="Transformed messages",
                shared=output_field_name == "messages",
                reducer_name=(
                    "add_messages" if output_field_name == "messages" else None
                ),
            ),
            FieldDefinition(
                name=self.error_field,
                field_type=Optional[str],
                default=None,
                description="Transformation error message if transformation failed",
            ),
        ]

        return fields

    def __call__(self, state: StateLike, config: ConfigLike | None = None) -> Command:
        """Execute the message transformation."""
        if self.debug:
            console.print(
                f"[cyan]MessageTransformation[/] Starting {
                    self.transformation_type} transformation"
            )

        try:
            # Get messages from state
            messages = self._get_messages_from_state(state)

            if not messages:
                logger.warning(
                    f"No messages found in field '{
                        self.messages_field}'"
                )
                return self._create_output_command({}, goto=self._get_goto_node())

            if self.debug:
                console.print(f"[dim]Processing {len(messages)} messages[/]")

            # Apply the transformation
            transformed_messages = self._apply_transformation(messages)

            if self.debug:
                console.print(
                    f"[green]Transformed to {
                        len(transformed_messages)} messages[/]"
                )

            # Create update dictionary
            output_field = self.output_field or self.messages_field
            update = {output_field: transformed_messages, self.error_field: None}

            return self._create_output_command(update, goto=self._get_goto_node())

        except Exception as e:
            logger.exception(f"Error in message transformation: {e}")
            output_field = self.output_field or self.messages_field
            return self._create_output_command(
                {output_field: [], self.error_field: str(e)}, goto=self._get_goto_node()
            )

    def _get_messages_from_state(self, state: StateLike) -> list[BaseMessage]:
        """Extract messages from state."""
        if hasattr(state, self.messages_field):
            messages = getattr(state, self.messages_field)
        elif hasattr(state, "get"):
            messages = state.get(self.messages_field, [])
        else:
            messages = []

        # Ensure it's a list
        if not isinstance(messages, list):
            messages = [messages]

        return messages

    def _get_goto_node(self) -> str:
        """Get the node to go to after transformation."""
        return self.command_goto or "agent"

    def _create_output_command(self, update: dict[str, Any], goto: str) -> Command:
        """Create output command with proper typing."""
        return Command(update=update, goto=goto)

    def _apply_transformation(self, messages: list[BaseMessage]) -> list[BaseMessage]:
        """Apply the specified transformation to messages."""
        transformation_map = {
            TransformationType.AI_TO_HUMAN: self._transform_ai_to_human,
            TransformationType.HUMAN_TO_AI: self._transform_human_to_ai,
            TransformationType.REFLECTION: self._transform_reflection,
            TransformationType.AGENT_TO_AGENT: self._transform_agent_to_agent,
            TransformationType.ADD_ENGINE_ID: self._add_engine_id,
            TransformationType.EXTRACT_FIRST_HUMAN: self._extract_first_human,
            TransformationType.FILTER_BY_TYPE: self._filter_by_type,
            TransformationType.MERGE_CONSECUTIVE: self._merge_consecutive,
            TransformationType.CUSTOM: self._apply_custom_transformation,
        }

        transformer = transformation_map.get(self.transformation_type)
        if not transformer:
            raise ValueError(
                f"Unsupported transformation type: {self.transformation_type}"
            )

        return transformer(messages)

    def _transform_ai_to_human(self, messages: list[BaseMessage]) -> list[BaseMessage]:
        """Transform AI messages to Human messages, preserving metadata."""
        transformed = []

        for msg in messages:
            if isinstance(msg, AIMessage):
                # Create HumanMessage with preserved metadata
                kwargs = {
                    "content": msg.content,
                }

                if self.preserve_metadata:
                    # Preserve additional_kwargs and other metadata
                    if hasattr(msg, "additional_kwargs") and msg.additional_kwargs:
                        kwargs["additional_kwargs"] = msg.additional_kwargs.copy()

                    # Add engine_id if specified
                    if self.engine_id:
                        if "additional_kwargs" not in kwargs:
                            kwargs["additional_kwargs"] = {}
                        kwargs["additional_kwargs"]["engine_id"] = self.engine_id
                    # Add engine_name if specified
                    if self.engine_name:
                        if "additional_kwargs" not in kwargs:
                            kwargs["additional_kwargs"] = {}
                        kwargs["additional_kwargs"]["engine_name"] = self.engine_name

                    # Preserve name if it exists
                    if hasattr(msg, "name") and msg.name:
                        kwargs["name"] = msg.name

                transformed.append(HumanMessage(**kwargs))

                if self.debug:
                    console.print(
                        f"[green]Transformed AI → Human:[/] {msg.content[:50]}..."
                    )
            else:
                # Keep other message types unchanged
                transformed.append(msg)

        return transformed

    def _transform_human_to_ai(self, messages: list[BaseMessage]) -> list[BaseMessage]:
        """Transform Human messages to AI messages, preserving metadata."""
        transformed = []

        for msg in messages:
            if isinstance(msg, HumanMessage):
                # Create AIMessage with preserved metadata
                kwargs = {
                    "content": msg.content,
                }

                if self.preserve_metadata:
                    # Preserve additional_kwargs and other metadata
                    if hasattr(msg, "additional_kwargs") and msg.additional_kwargs:
                        kwargs["additional_kwargs"] = msg.additional_kwargs.copy()

                    # Add engine_id if specified
                    if self.engine_id:
                        if "additional_kwargs" not in kwargs:
                            kwargs["additional_kwargs"] = {}
                        kwargs["additional_kwargs"]["engine_id"] = self.engine_id
                    # Add engine_name if specified
                    if self.engine_name:
                        if "additional_kwargs" not in kwargs:
                            kwargs["additional_kwargs"] = {}
                        kwargs["additional_kwargs"]["engine_name"] = self.engine_name

                    # Preserve name if it exists
                    if hasattr(msg, "name") and msg.name:
                        kwargs["name"] = msg.name

                transformed.append(AIMessage(**kwargs))

                if self.debug:
                    console.print(
                        f"[green]Transformed Human → AI:[/] {msg.content[:50]}..."
                    )
            else:
                # Keep other message types unchanged
                transformed.append(msg)

        return transformed

    def _transform_reflection(self, messages: list[BaseMessage]) -> list[BaseMessage]:
        """Apply reflection transformation: swap AI ↔ Human roles.

        Based on the reflection pattern where:
        - First message (original user request) is preserved
        - Subsequent messages have roles swapped
        """
        if not messages:
            return []

        transformed = []

        # Class mapping for role swapping
        cls_map = {"ai": HumanMessage, "human": AIMessage}

        # Preserve first message if requested
        if self.preserve_first_message and len(messages) > 0:
            transformed.append(messages[0])
            start_idx = 1

            if self.debug:
                console.print(
                    f"[dim]Preserving first message:[/] {messages[0].content[:50]}..."
                )
        else:
            start_idx = 0

        # Transform remaining messages with role swap
        for msg in messages[start_idx:]:
            if msg.type in cls_map:
                # Get the target class
                target_cls = cls_map[msg.type]

                # Create new message with swapped role
                kwargs = {"content": msg.content}

                if self.preserve_metadata:
                    if hasattr(msg, "additional_kwargs") and msg.additional_kwargs:
                        kwargs["additional_kwargs"] = msg.additional_kwargs.copy()

                    if hasattr(msg, "name") and msg.name:
                        kwargs["name"] = msg.name

                transformed.append(target_cls(**kwargs))

                if self.debug:
                    console.print(
                        f"[green]Reflection swap {msg.type} → {target_cls.__name__.lower()}:[/] {msg.content[:50]}..."
                    )
            # Keep non-human/ai messages unchanged (unless excluded)
            elif not (
                (self.exclude_system_messages and isinstance(msg, SystemMessage))
                or (self.exclude_tool_messages and isinstance(msg, ToolMessage))
            ):
                transformed.append(msg)

        return transformed

    def _transform_agent_to_agent(
        self, messages: list[BaseMessage]
    ) -> list[BaseMessage]:
        """Transform messages for agent-to-agent communication.

        Excludes system messages and converts AI messages to Human messages.
        """
        transformed = []

        for msg in messages:
            # Skip system messages (they're agent-specific)
            if isinstance(msg, SystemMessage):
                if self.debug:
                    console.print(
                        f"[dim]Excluding system message:[/] {msg.content[:50]}..."
                    )
                continue

            # Skip tool messages if requested
            if self.exclude_tool_messages and isinstance(msg, ToolMessage):
                if self.debug:
                    console.print(
                        f"[dim]Excluding tool message:[/] {msg.content[:50]}..."
                    )
                continue

            # Convert AI messages to Human messages for the receiving agent
            if isinstance(msg, AIMessage):
                kwargs = {"content": msg.content}

                if self.preserve_metadata:
                    if hasattr(msg, "additional_kwargs") and msg.additional_kwargs:
                        kwargs["additional_kwargs"] = msg.additional_kwargs.copy()

                    # Add source agent name if specified
                    if self.agent_name:
                        if "additional_kwargs" not in kwargs:
                            kwargs["additional_kwargs"] = {}
                        kwargs["additional_kwargs"]["source_agent"] = self.agent_name

                transformed.append(HumanMessage(**kwargs))

                if self.debug:
                    console.print(f"[green]Agent AI → Human:[/] {msg.content[:50]}...")
            else:
                # Keep human messages and other types
                transformed.append(msg)

        return transformed

    def _add_engine_id(self, messages: list[BaseMessage]) -> list[BaseMessage]:
        """Add engine_id and engine_name to all AI messages."""
        if not self.engine_id and not self.engine_name:
            return messages

        transformed = []

        for msg in messages:
            if isinstance(msg, AIMessage):
                # Clone the message and add engine_id
                kwargs = {"content": msg.content}

                # Copy existing metadata
                if hasattr(msg, "additional_kwargs") and msg.additional_kwargs:
                    kwargs["additional_kwargs"] = msg.additional_kwargs.copy()
                else:
                    kwargs["additional_kwargs"] = {}

                # Add engine_id
                kwargs["additional_kwargs"]["engine_id"] = self.engine_id
                # Add engine_name if specified
                if self.engine_name:
                    kwargs["additional_kwargs"]["engine_name"] = self.engine_name

                # Preserve other attributes
                if hasattr(msg, "name") and msg.name:
                    kwargs["name"] = msg.name
                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    kwargs["tool_calls"] = msg.tool_calls

                transformed.append(AIMessage(**kwargs))

                if self.debug:
                    console.print(
                        f"[green]Added engine_id to AI message:[/] {
                            self.engine_id}"
                    )
            else:
                # Keep other messages unchanged
                transformed.append(msg)

        return transformed

    def _extract_first_human(self, messages: list[BaseMessage]) -> list[BaseMessage]:
        """Extract the first real human input (content-only, no metadata).

        Returns only the first human message that has pure content without metadata like
        engine_id or name.
        """
        for msg in messages:
            if isinstance(msg, HumanMessage):
                # Check if this is a "real" human message (no metadata
                # indicating transformation)
                has_metadata = (hasattr(msg, "name") and msg.name) or (
                    hasattr(msg, "additional_kwargs")
                    and msg.additional_kwargs
                    and any(
                        key in msg.additional_kwargs
                        for key in ["engine_id", "engine_name", "source_agent"]
                    )
                )

                if not has_metadata:
                    if self.debug:
                        console.print(
                            f"[green]Found first real human input:[/] {msg.content[:50]}..."
                        )
                    return [msg]

        if self.debug:
            console.print("[yellow]No real human input found[/]")
        return []

    def _filter_by_type(self, messages: list[BaseMessage]) -> list[BaseMessage]:
        """Filter messages by type (include or exclude)."""
        transformed = []

        for msg in messages:
            msg_type = msg.type

            # Check inclusion
            if self.include_types:
                if msg_type in self.include_types:
                    transformed.append(msg)
                    if self.debug:
                        console.print(f"[green]Including {msg_type} message[/]")
                elif self.debug:
                    console.print(
                        f"[dim]Excluding {msg_type} message (not in include list)[/]"
                    )

            # Check exclusion
            elif self.exclude_types:
                if msg_type not in self.exclude_types:
                    transformed.append(msg)
                    if self.debug:
                        console.print(f"[green]Including {msg_type} message[/]")
                elif self.debug:
                    console.print(
                        f"[dim]Excluding {msg_type} message (in exclude list)[/]"
                    )

        return transformed

    def _merge_consecutive(self, messages: list[BaseMessage]) -> list[BaseMessage]:
        """Merge consecutive messages of the same type."""
        if not messages:
            return []

        transformed = []
        current_group = [messages[0]]

        for msg in messages[1:]:
            # Check if same type as current group
            if isinstance(msg, type(current_group[0])):
                current_group.append(msg)
            else:
                # Different type - merge current group and start new one
                merged = self._merge_message_group(current_group)
                if merged:
                    transformed.append(merged)
                current_group = [msg]

        # Don't forget the last group
        merged = self._merge_message_group(current_group)
        if merged:
            transformed.append(merged)

        if self.debug:
            console.print(
                f"[green]Merged {
                    len(messages)} messages into {
                    len(transformed)}[/]"
            )

        return transformed

    def _merge_message_group(self, messages: list[BaseMessage]) -> BaseMessage | None:
        """Merge a group of messages of the same type."""
        if not messages:
            return None

        if len(messages) == 1:
            return messages[0]

        # Merge content
        merged_content = "\n\n".join(msg.content for msg in messages)

        # Use first message as template
        template = messages[0]
        msg_class = type(template)

        kwargs = {"content": merged_content}

        if self.preserve_metadata:
            # Merge metadata from all messages
            if hasattr(template, "additional_kwargs"):
                merged_kwargs = {}
                for msg in messages:
                    if hasattr(msg, "additional_kwargs") and msg.additional_kwargs:
                        merged_kwargs.update(msg.additional_kwargs)
                if merged_kwargs:
                    kwargs["additional_kwargs"] = merged_kwargs

            # Use first message's name if any
            if hasattr(template, "name") and template.name:
                kwargs["name"] = template.name

        return msg_class(**kwargs)

    def _apply_custom_transformation(
        self, messages: list[BaseMessage]
    ) -> list[BaseMessage]:
        """Apply custom transformation function."""
        if not self.custom_transformer:
            return messages

        try:
            result = self.custom_transformer(messages)

            if self.debug:
                console.print(
                    f"[green]Applied custom transformation:[/] {
                        len(messages)} → {
                        len(result)} messages"
                )

            return result
        except Exception as e:
            logger.exception(f"Custom transformation failed: {e}")
            return messages


# ============================================================================
# CONVENIENCE FACTORY FUNCTIONS
# ============================================================================


def create_ai_to_human_transformer(
    name: str = "ai_to_human",
    messages_field: str = "messages",
    output_field: str | None = None,
    engine_id: str | None = None,
    engine_name: str | None = None,
    preserve_metadata: bool = True,
    **kwargs,
) -> MessageTransformationNodeConfig:
    """Create a transformer that converts AI messages to Human messages."""
    return MessageTransformationNodeConfig(
        name=name,
        transformation_type=TransformationType.AI_TO_HUMAN,
        messages_field=messages_field,
        output_field=output_field,
        engine_id=engine_id,
        engine_name=engine_name,
        preserve_metadata=preserve_metadata,
        **kwargs,
    )


def create_reflection_transformer(
    name: str = "reflection",
    messages_field: str = "messages",
    output_field: str | None = None,
    preserve_first_message: bool = True,
    **kwargs,
) -> MessageTransformationNodeConfig:
    """Create a reflection transformer that swaps AI ↔ Human roles."""
    return MessageTransformationNodeConfig(
        name=name,
        transformation_type=TransformationType.REFLECTION,
        messages_field=messages_field,
        output_field=output_field,
        preserve_first_message=preserve_first_message,
        **kwargs,
    )


def create_agent_to_agent_transformer(
    agent_name: str | None = None,
    name: str = "agent_to_agent",
    messages_field: str = "messages",
    output_field: str = "transformed_messages",
    exclude_system_messages: bool = True,
    **kwargs,
) -> MessageTransformationNodeConfig:
    """Create a transformer for agent-to-agent communication."""
    return MessageTransformationNodeConfig(
        name=name,
        transformation_type=TransformationType.AGENT_TO_AGENT,
        agent_name=agent_name,
        messages_field=messages_field,
        output_field=output_field,
        exclude_system_messages=exclude_system_messages,
        **kwargs,
    )


def create_message_filter(
    name: str = "message_filter",
    include_types: list[str] | None = None,
    exclude_types: list[str] | None = None,
    messages_field: str = "messages",
    output_field: str | None = None,
    **kwargs,
) -> MessageTransformationNodeConfig:
    """Create a message filter by type."""
    return MessageTransformationNodeConfig(
        name=name,
        transformation_type=TransformationType.FILTER_BY_TYPE,
        include_types=include_types,
        exclude_types=exclude_types,
        messages_field=messages_field,
        output_field=output_field,
        **kwargs,
    )


def create_message_merger(
    name: str = "message_merger",
    messages_field: str = "messages",
    output_field: str | None = None,
    **kwargs,
) -> MessageTransformationNodeConfig:
    """Create a transformer that merges consecutive messages of the same type."""
    return MessageTransformationNodeConfig(
        name=name,
        transformation_type=TransformationType.MERGE_CONSECUTIVE,
        messages_field=messages_field,
        output_field=output_field,
        **kwargs,
    )
