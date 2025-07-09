"""
LangChain-specific type converters for documents, messages, and prompts.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, List, Optional, Union

from langchain_core.documents import Document
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    FunctionMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langchain_core.prompts import (
    BasePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
)

from haive.core.schema.compatibility.converters import TypeConverter
from haive.core.schema.compatibility.types import ConversionContext, ConversionQuality


class MessageConverter(TypeConverter):
    """Converter for LangChain message types."""

    # Message type priority for lossy conversions
    MESSAGE_HIERARCHY = {
        BaseMessage: 0,
        SystemMessage: 1,
        HumanMessage: 1,
        AIMessage: 1,
        ToolMessage: 2,
        FunctionMessage: 2,
    }

    @property
    def name(self) -> str:
        return "langchain_message_converter"

    @property
    def priority(self) -> int:
        return 10  # High priority for message conversions

    def can_convert(self, source_type: type, target_type: type) -> bool:
        """Check if we can convert between message types."""
        try:
            return issubclass(source_type, BaseMessage) and issubclass(
                target_type, BaseMessage
            )
        except TypeError:
            return False

    def get_quality(self, source_type: type, target_type: type) -> ConversionQuality:
        """Determine conversion quality."""
        if source_type == target_type:
            return ConversionQuality.LOSSLESS

        # Converting to base type is lossy
        if target_type == BaseMessage:
            return ConversionQuality.LOSSY

        # Check hierarchy levels
        source_level = self.MESSAGE_HIERARCHY.get(source_type, 99)
        target_level = self.MESSAGE_HIERARCHY.get(target_type, 99)

        if source_level == target_level:
            return ConversionQuality.SAFE
        elif source_level < target_level:
            # Converting from general to specific
            return ConversionQuality.UNSAFE
        else:
            # Converting from specific to general
            return ConversionQuality.LOSSY

    def convert(self, value: BaseMessage, context: ConversionContext) -> BaseMessage:
        """Convert between message types."""
        target_type_name = context.target_type.split(".")[-1]
        target_type = self._get_message_type(target_type_name)

        # Same type - no conversion
        if type(value) == target_type:
            return value

        # Extract core data
        content = value.content
        additional_kwargs = value.additional_kwargs.copy()

        # Special conversions
        if isinstance(value, AIMessage) and target_type == ToolMessage:
            return self._ai_to_tool(value, context)
        elif isinstance(value, ToolMessage) and target_type == AIMessage:
            return self._tool_to_ai(value, context)
        elif (
            isinstance(value, (HumanMessage, AIMessage))
            and target_type == SystemMessage
        ):
            context.add_warning("Converting user/assistant message to system message")
            return SystemMessage(content=content, additional_kwargs=additional_kwargs)

        # Generic conversion
        try:
            if target_type == HumanMessage:
                return HumanMessage(
                    content=content, additional_kwargs=additional_kwargs
                )
            elif target_type == AIMessage:
                return AIMessage(content=content, additional_kwargs=additional_kwargs)
            elif target_type == SystemMessage:
                return SystemMessage(
                    content=content, additional_kwargs=additional_kwargs
                )
            elif target_type == BaseMessage:
                # Keep original type but track as "converted"
                context.add_warning(f"Keeping as {type(value).__name__}")
                return value
            else:
                # Try direct instantiation
                return target_type(content=content, **additional_kwargs)
        except Exception as e:
            context.add_error(f"Conversion failed: {str(e)}")
            return value

    def _ai_to_tool(self, ai_msg: AIMessage, context: ConversionContext) -> ToolMessage:
        """Convert AIMessage to ToolMessage."""
        # Check for tool calls
        if hasattr(ai_msg, "tool_calls") and ai_msg.tool_calls:
            tool_call = ai_msg.tool_calls[0]
            context.track_lost_field("additional_tool_calls", ai_msg.tool_calls[1:])

            return ToolMessage(
                content=ai_msg.content or json.dumps(tool_call.get("args", {})),
                tool_call_id=tool_call.get("id", self._generate_id(ai_msg.content)),
                additional_kwargs=ai_msg.additional_kwargs,
            )
        else:
            # No tool calls - generate synthetic tool message
            context.add_warning(
                "No tool calls in AIMessage, creating synthetic ToolMessage"
            )
            return ToolMessage(
                content=ai_msg.content,
                tool_call_id=self._generate_id(ai_msg.content),
                additional_kwargs={
                    **ai_msg.additional_kwargs,
                    "synthetic": True,
                    "original_type": "AIMessage",
                },
            )

    def _tool_to_ai(
        self, tool_msg: ToolMessage, context: ConversionContext
    ) -> AIMessage:
        """Convert ToolMessage to AIMessage."""
        return AIMessage(
            content=f"Tool Response [{tool_msg.tool_call_id}]: {tool_msg.content}",
            additional_kwargs={
                **tool_msg.additional_kwargs,
                "was_tool_message": True,
                "tool_call_id": tool_msg.tool_call_id,
            },
        )

    def _get_message_type(self, type_name: str) -> type:
        """Get message type from string name."""
        type_map = {
            "BaseMessage": BaseMessage,
            "HumanMessage": HumanMessage,
            "AIMessage": AIMessage,
            "SystemMessage": SystemMessage,
            "ToolMessage": ToolMessage,
            "FunctionMessage": FunctionMessage,
        }
        return type_map.get(type_name, BaseMessage)

    def _generate_id(self, content: str) -> str:
        """Generate ID from content."""
        return hashlib.md5(content.encode()).hexdigest()[:8]


class DocumentConverter(TypeConverter):
    """Converter for Document-related conversions."""

    @property
    def name(self) -> str:
        return "langchain_document_converter"

    @property
    def priority(self) -> int:
        return 10

    def can_convert(self, source_type: type, target_type: type) -> bool:
        """Check if conversion is possible."""
        # Document to Message conversions
        if source_type == Document and issubclass(target_type, BaseMessage):
            return True

        # Message to Document conversions
        if issubclass(source_type, BaseMessage) and target_type == Document:
            return True

        # Document to dict/str
        if source_type == Document and target_type in [dict, str]:
            return True

        # dict/str to Document
        if source_type in [dict, str] and target_type == Document:
            return True

        return False

    def get_quality(self, source_type: type, target_type: type) -> ConversionQuality:
        """Determine conversion quality."""
        # Document <-> Message is lossy (metadata handling)
        if (
            source_type == Document
            and issubclass(target_type, BaseMessage)
            or issubclass(source_type, BaseMessage)
            and target_type == Document
        ):
            return ConversionQuality.LOSSY

        # Document <-> dict is safe
        if source_type == Document and target_type == dict:
            return ConversionQuality.SAFE

        # Document <-> str is lossy
        if source_type == Document and target_type == str:
            return ConversionQuality.LOSSY

        return ConversionQuality.SAFE

    def convert(self, value: Any, context: ConversionContext) -> Any:
        """Perform conversion."""
        source_type_name = context.source_type.split(".")[-1]
        target_type_name = context.target_type.split(".")[-1]

        # Document to Message
        if isinstance(value, Document):
            if target_type_name in ["HumanMessage", "BaseMessage"]:
                return self._doc_to_human_message(value, context)
            elif target_type_name == "AIMessage":
                return self._doc_to_ai_message(value, context)
            elif target_type_name == "dict":
                return self._doc_to_dict(value, context)
            elif target_type_name == "str":
                return self._doc_to_str(value, context)

        # Message to Document
        elif isinstance(value, BaseMessage):
            return self._message_to_doc(value, context)

        # Dict to Document
        elif isinstance(value, dict):
            return self._dict_to_doc(value, context)

        # String to Document
        elif isinstance(value, str):
            return self._str_to_doc(value, context)

        return value

    def _doc_to_human_message(
        self, doc: Document, context: ConversionContext
    ) -> HumanMessage:
        """Convert Document to HumanMessage."""
        # Include metadata in message
        metadata_str = ""
        if doc.metadata:
            metadata_str = f"\n[Source: {doc.metadata.get('source', 'unknown')}]"
            context.track_lost_field("full_metadata", doc.metadata)

        return HumanMessage(
            content=doc.page_content + metadata_str,
            additional_kwargs={
                "source": "document",
                "doc_metadata": doc.metadata,
            },
        )

    def _doc_to_ai_message(
        self, doc: Document, context: ConversionContext
    ) -> AIMessage:
        """Convert Document to AIMessage."""
        return AIMessage(
            content=f"Document content: {doc.page_content}",
            additional_kwargs={
                "source": "document",
                "doc_metadata": doc.metadata,
            },
        )

    def _doc_to_dict(self, doc: Document, context: ConversionContext) -> dict:
        """Convert Document to dict."""
        return {
            "page_content": doc.page_content,
            "metadata": doc.metadata,
            "type": "Document",
        }

    def _doc_to_str(self, doc: Document, context: ConversionContext) -> str:
        """Convert Document to string."""
        if doc.metadata:
            context.track_lost_field("metadata", doc.metadata)
        return doc.page_content

    def _message_to_doc(self, msg: BaseMessage, context: ConversionContext) -> Document:
        """Convert Message to Document."""
        metadata = {
            "source": "message",
            "message_type": type(msg).__name__,
            **msg.additional_kwargs,
        }

        return Document(
            page_content=msg.content,
            metadata=metadata,
        )

    def _dict_to_doc(self, data: dict, context: ConversionContext) -> Document:
        """Convert dict to Document."""
        # Handle different dict formats
        if "page_content" in data:
            return Document(
                page_content=data["page_content"],
                metadata=data.get("metadata", {}),
            )
        elif "content" in data:
            return Document(
                page_content=data["content"],
                metadata={k: v for k, v in data.items() if k != "content"},
            )
        else:
            # Treat entire dict as metadata
            return Document(
                page_content=str(data),
                metadata=data,
            )

    def _str_to_doc(self, text: str, context: ConversionContext) -> Document:
        """Convert string to Document."""
        return Document(
            page_content=text,
            metadata={"source": "string"},
        )


class PromptConverter(TypeConverter):
    """Converter for Prompt-related conversions."""

    @property
    def name(self) -> str:
        return "langchain_prompt_converter"

    @property
    def priority(self) -> int:
        return 10

    def can_convert(self, source_type: type, target_type: type) -> bool:
        """Check if conversion is possible."""
        # String to Prompt
        if source_type == str and issubclass(target_type, BasePromptTemplate):
            return True

        # Prompt to String
        if issubclass(source_type, BasePromptTemplate) and target_type == str:
            return True

        # Between prompt types
        if issubclass(source_type, BasePromptTemplate) and issubclass(
            target_type, BasePromptTemplate
        ):
            return True

        # Messages to ChatPrompt
        if source_type == list and target_type == ChatPromptTemplate:
            return True

        return False

    def get_quality(self, source_type: type, target_type: type) -> ConversionQuality:
        """Determine conversion quality."""
        # Same type
        if source_type == target_type:
            return ConversionQuality.LOSSLESS

        # String conversions are lossy (lose template info)
        if source_type == str or target_type == str:
            return ConversionQuality.LOSSY

        # PromptTemplate <-> ChatPromptTemplate
        if (
            source_type == PromptTemplate
            and target_type == ChatPromptTemplate
            or source_type == ChatPromptTemplate
            and target_type == PromptTemplate
        ):
            return ConversionQuality.SAFE

        return ConversionQuality.SAFE

    def convert(self, value: Any, context: ConversionContext) -> Any:
        """Perform conversion."""
        target_type_name = context.target_type.split(".")[-1]

        # String to Prompt
        if isinstance(value, str):
            if target_type_name == "PromptTemplate":
                return PromptTemplate.from_template(value)
            elif target_type_name == "ChatPromptTemplate":
                return ChatPromptTemplate.from_template(value)

        # Prompt to String
        elif isinstance(value, BasePromptTemplate):
            if target_type_name == "str":
                # Try to get template string
                if hasattr(value, "template"):
                    return value.template
                else:
                    context.add_warning(
                        "Complex prompt converted to string representation"
                    )
                    return str(value)

        # PromptTemplate to ChatPromptTemplate
        elif isinstance(value, PromptTemplate):
            if target_type_name == "ChatPromptTemplate":
                return ChatPromptTemplate.from_template(value.template)

        # ChatPromptTemplate to PromptTemplate
        elif isinstance(value, ChatPromptTemplate):
            if target_type_name == "PromptTemplate":
                # Flatten to single template
                context.add_warning("Flattening ChatPromptTemplate to PromptTemplate")
                messages = value.messages
                template_parts = []

                for msg in messages:
                    if hasattr(msg, "prompt") and hasattr(msg.prompt, "template"):
                        template_parts.append(msg.prompt.template)
                    elif isinstance(msg, MessagesPlaceholder):
                        template_parts.append(f"{{{msg.variable_name}}}")

                return PromptTemplate.from_template("\n".join(template_parts))

        # List of messages to ChatPromptTemplate
        elif isinstance(value, list):
            if target_type_name == "ChatPromptTemplate":
                return ChatPromptTemplate.from_messages(value)

        return value


def register_langchain_converters(registry: Optional[Any] = None) -> None:
    """Register all LangChain converters with the global registry."""
    # Import here to avoid circular imports
    from haive.core.schema.compatibility.converters import register_converter

    # Register converters
    register_converter(MessageConverter())
    register_converter(DocumentConverter())
    register_converter(PromptConverter())
