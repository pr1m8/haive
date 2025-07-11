# src/haive/core/graph/node/message_transformation_node_config.py

import logging
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Union

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

from haive.core.graph.common.types import ConfigLike, StateLike
from haive.core.graph.node.base_config import NodeConfig
from haive.core.graph.node.types import NodeType

logger = logging.getLogger(__name__)
console = Console()


class TransformationType(str, Enum):
    """Types of message transformations available."""

    AI_TO_HUMAN = "ai_to_human"
    HUMAN_TO_AI = "human_to_ai"
    REFLECTION = "reflection"
    AGENT_TO_AGENT = "agent_to_agent"
    ADD_ENGINE_ID = "add_engine_id"
    EXTRACT_FIRST_HUMAN = "extract_first_human"
    CUSTOM = "custom"


class MessageTransformationNodeConfig(NodeConfig):
    """
    Configuration for a node that transforms messages in various ways.

    Supports multiple transformation types including role swapping,
    metadata manipulation, and agent-to-agent communication.
    """

    node_type: NodeType = Field(default=NodeType.MESSAGE_TRANSFORMER)

    # Core transformation configuration
    transformation_type: TransformationType = Field(
        description="Type of transformation to apply"
    )

    messages_key: str = Field(
        default="messages", description="State key containing the messages to transform"
    )

    output_key: str = Field(
        default="messages", description="State key to store transformed messages"
    )

    # Engine ID configuration
    engine_id: Optional[str] = Field(
        default=None,
        description="Engine ID to add to messages (for ADD_ENGINE_ID transformation)",
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

    # Agent-specific configuration
    agent_name: Optional[str] = Field(
        default=None,
        description="Agent name for filtering (for AGENT_TO_AGENT transformation)",
    )

    # Custom transformation
    custom_transformer: Optional[Callable[[List[BaseMessage]], List[BaseMessage]]] = (
        Field(default=None, description="Custom transformation function")
    )

    # Additional options
    preserve_metadata: bool = Field(
        default=True,
        description="Whether to preserve message metadata during transformation",
    )

    debug: bool = Field(default=False, description="Enable debug output")

    @model_validator(mode="after")
    def validate_transformation_config(self) -> "MessageTransformationNodeConfig":
        """Validate transformation-specific configuration."""
        if (
            self.transformation_type == TransformationType.ADD_ENGINE_ID
            and not self.engine_id
        ):
            raise ValueError("engine_id is required for ADD_ENGINE_ID transformation")

        if (
            self.transformation_type == TransformationType.CUSTOM
            and not self.custom_transformer
        ):
            raise ValueError("custom_transformer is required for CUSTOM transformation")

        return self

    def __call__(
        self, state: StateLike, config: Optional[ConfigLike] = None
    ) -> Command:
        """Execute the message transformation."""

        if self.debug:
            console.print(
                f"[cyan]MessageTransformation[/] Starting {self.transformation_type} transformation"
            )

        try:
            # Get messages from state
            messages = self._get_messages_from_state(state)

            if not messages:
                logger.warning(f"No messages found in state key '{self.messages_key}'")
                return Command(update={}, goto=self.command_goto)

            if self.debug:
                console.print(f"[dim]Processing {len(messages)} messages[/]")

            # Apply the transformation
            transformed_messages = self._apply_transformation(messages)

            if self.debug:
                console.print(
                    f"[green]Transformed to {len(transformed_messages)} messages[/]"
                )

            # Create update dictionary
            update = {self.output_key: transformed_messages}

            return Command(update=update, goto=self.command_goto)

        except Exception as e:
            logger.error(f"Error in message transformation: {e}")
            return Command(
                update={"transformation_error": str(e)}, goto=self.command_goto
            )

    def _get_messages_from_state(self, state: StateLike) -> List[BaseMessage]:
        """Extract messages from state."""
        if hasattr(state, self.messages_key):
            return getattr(state, self.messages_key, [])
        elif isinstance(state, dict):
            return state.get(self.messages_key, [])
        else:
            return []

    def _apply_transformation(self, messages: List[BaseMessage]) -> List[BaseMessage]:
        """Apply the specified transformation to messages."""

        transformation_map = {
            TransformationType.AI_TO_HUMAN: self._transform_ai_to_human,
            TransformationType.HUMAN_TO_AI: self._transform_human_to_ai,
            TransformationType.REFLECTION: self._transform_reflection,
            TransformationType.AGENT_TO_AGENT: self._transform_agent_to_agent,
            TransformationType.ADD_ENGINE_ID: self._add_engine_id,
            TransformationType.EXTRACT_FIRST_HUMAN: self._extract_first_human,
            TransformationType.CUSTOM: self._apply_custom_transformation,
        }

        transformer = transformation_map.get(self.transformation_type)
        if not transformer:
            raise ValueError(
                f"Unsupported transformation type: {self.transformation_type}"
            )

        return transformer(messages)

    def _transform_ai_to_human(self, messages: List[BaseMessage]) -> List[BaseMessage]:
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

    def _transform_human_to_ai(self, messages: List[BaseMessage]) -> List[BaseMessage]:
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

    def _transform_reflection(self, messages: List[BaseMessage]) -> List[BaseMessage]:
        """
        Apply reflection transformation: swap AI ↔ Human roles.

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
            else:
                # Keep non-human/ai messages unchanged (unless excluded)
                if not (
                    (self.exclude_system_messages and isinstance(msg, SystemMessage))
                    or (self.exclude_tool_messages and isinstance(msg, ToolMessage))
                ):
                    transformed.append(msg)

        return transformed

    def _transform_agent_to_agent(
        self, messages: List[BaseMessage]
    ) -> List[BaseMessage]:
        """
        Transform messages for agent-to-agent communication.

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

    def _add_engine_id(self, messages: List[BaseMessage]) -> List[BaseMessage]:
        """Add engine_id to all AI messages."""
        if not self.engine_id:
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

                # Preserve other attributes
                if hasattr(msg, "name") and msg.name:
                    kwargs["name"] = msg.name
                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    kwargs["tool_calls"] = msg.tool_calls

                transformed.append(AIMessage(**kwargs))

                if self.debug:
                    console.print(
                        f"[green]Added engine_id to AI message:[/] {self.engine_id}"
                    )
            else:
                # Keep other messages unchanged
                transformed.append(msg)

        return transformed

    def _extract_first_human(self, messages: List[BaseMessage]) -> List[BaseMessage]:
        """
        Extract the first real human input (content-only, no metadata).

        Returns only the first human message that has pure content without
        metadata like engine_id or name.
        """
        for msg in messages:
            if isinstance(msg, HumanMessage):
                # Check if this is a "real" human message (no metadata indicating transformation)
                has_metadata = (hasattr(msg, "name") and msg.name) or (
                    hasattr(msg, "additional_kwargs")
                    and msg.additional_kwargs
                    and any(
                        key in msg.additional_kwargs
                        for key in ["engine_id", "source_agent"]
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

    def _apply_custom_transformation(
        self, messages: List[BaseMessage]
    ) -> List[BaseMessage]:
        """Apply custom transformation function."""
        if not self.custom_transformer:
            return messages

        try:
            result = self.custom_transformer(messages)

            if self.debug:
                console.print(
                    f"[green]Applied custom transformation:[/] {len(messages)} → {len(result)} messages"
                )

            return result
        except Exception as e:
            logger.error(f"Custom transformation failed: {e}")
            return messages


# ============================================================================
# CONVENIENCE FACTORY FUNCTIONS
# ============================================================================


def create_ai_to_human_transformer(
    messages_key: str = "messages",
    output_key: str = "messages",
    engine_id: Optional[str] = None,
    preserve_metadata: bool = True,
    **kwargs,
) -> MessageTransformationNodeConfig:
    """Create a transformer that converts AI messages to Human messages."""
    return MessageTransformationNodeConfig(
        name="ai_to_human_transformer",
        transformation_type=TransformationType.AI_TO_HUMAN,
        messages_key=messages_key,
        output_key=output_key,
        engine_id=engine_id,
        preserve_metadata=preserve_metadata,
        **kwargs,
    )


def create_reflection_transformer(
    messages_key: str = "messages",
    output_key: str = "messages",
    preserve_first_message: bool = True,
    **kwargs,
) -> MessageTransformationNodeConfig:
    """Create a reflection transformer that swaps AI ↔ Human roles."""
    return MessageTransformationNodeConfig(
        name="reflection_transformer",
        transformation_type=TransformationType.REFLECTION,
        messages_key=messages_key,
        output_key=output_key,
        preserve_first_message=preserve_first_message,
        **kwargs,
    )


def create_agent_to_agent_transformer(
    agent_name: Optional[str] = None,
    messages_key: str = "messages",
    output_key: str = "transformed_messages",
    exclude_system_messages: bool = True,
    **kwargs,
) -> MessageTransformationNodeConfig:
    """Create a transformer for agent-to-agent communication."""
    return MessageTransformationNodeConfig(
        name="agent_to_agent_transformer",
        transformation_type=TransformationType.AGENT_TO_AGENT,
        agent_name=agent_name,
        messages_key=messages_key,
        output_key=output_key,
        exclude_system_messages=exclude_system_messages,
        **kwargs,
    )


def create_engine_id_transformer(
    engine_id: str,
    messages_key: str = "messages",
    output_key: str = "messages",
    **kwargs,
) -> MessageTransformationNodeConfig:
    """Create a transformer that adds engine_id to AI messages."""
    return MessageTransformationNodeConfig(
        name="engine_id_transformer",
        transformation_type=TransformationType.ADD_ENGINE_ID,
        engine_id=engine_id,
        messages_key=messages_key,
        output_key=output_key,
        **kwargs,
    )


def create_first_human_extractor(
    messages_key: str = "messages", output_key: str = "first_human_message", **kwargs
) -> MessageTransformationNodeConfig:
    """Create a transformer that extracts the first real human input."""
    return MessageTransformationNodeConfig(
        name="first_human_extractor",
        transformation_type=TransformationType.EXTRACT_FIRST_HUMAN,
        messages_key=messages_key,
        output_key=output_key,
        **kwargs,
    )


def create_custom_transformer(
    transformer_func: Callable[[List[BaseMessage]], List[BaseMessage]],
    messages_key: str = "messages",
    output_key: str = "messages",
    **kwargs,
) -> MessageTransformationNodeConfig:
    """Create a transformer with custom transformation logic."""
    return MessageTransformationNodeConfig(
        name="custom_transformer",
        transformation_type=TransformationType.CUSTOM,
        custom_transformer=transformer_func,
        messages_key=messages_key,
        output_key=output_key,
        **kwargs,
    )
