"""Output_Parsing graph module.

This module provides output parsing functionality for the Haive framework.

Classes:
    OutputParserNodeConfig: OutputParserNodeConfig implementation.
    to: to implementation.

Functions:
    create_json_output_parser_node: Create Json Output Parser Node functionality.
"""

# ============================================================================
# OUTPUT PARSER NODE CONFIG - EXTENSION OF PARSER NODE
# ============================================================================

import logging
from typing import Any

from langchain_core.messages import BaseMessage
from langchain_core.output_parsers.base import BaseOutputParser
from langgraph.types import Command
from pydantic import Field
from rich.console import Console

from haive.core.graph.common.types import ConfigLike, StateLike
from haive.core.graph.node.parser_node_config import ParserNodeConfig
from haive.core.graph.node.types import NodeType

logger = logging.getLogger(__name__)
console = Console()
logger.setLevel(logging.WARNING)


class OutputParserNodeConfig(ParserNodeConfig):
    """Configuration for a node that parses LLM output using LangChain output parsers.

    This extends ParserNodeConfig to handle regular output parsing (not tool calls). It
    parses the last message content using a LangChain BaseOutputParser.
    """

    node_type: NodeType = Field(default=NodeType.OUTPUT_PARSER)

    # Output parser configuration
    output_parser: BaseOutputParser = Field(
        ..., description="LangChain output parser to use for parsing"
    )

    output_key: str = Field(
        default="parsed_output", description="Key to store parsed output in state"
    )

    # Override default behavior - we don't need tool info for output parsing
    require_tool_info: bool = Field(
        default=False,
        description="Whether tool information is required (False for output parsing)",
    )

    def __call__(self, state: StateLike, config: ConfigLike | None = None) -> Command:
        """Parse the last message content using the output parser."""
        # Ensure we have a valid command_goto
        goto_node = self.command_goto or self.agent_node

        # Get messages from state
        messages = (
            getattr(state, self.messages_key, state.get(self.messages_key, []))
            if hasattr(state, "get")
            else getattr(state, self.messages_key, [])
        )

        logger.debug(f"OutputParserNode processing {len(messages)} messages")

        if not messages:
            logger.warning(
                f"No messages found in state key '{
                    self.messages_key}'"
            )
            return Command(
                update={self.output_key: None, "parse_error": "No messages found"},
                goto=goto_node,
            )

        try:
            # Get the last message
            last_message = messages[-1]

            # Extract content from the message
            content = self._extract_content_from_message(last_message)

            if content is None:
                logger.warning(
                    f"Unable to extract content from message: {
                        type(last_message)}"
                )
                return Command(
                    update={
                        self.output_key: None,
                        "parse_error": f"Invalid message type: {type(last_message)}",
                    },
                    goto=goto_node,
                )

            # Parse the content using the output parser
            try:
                parsed_result = self.output_parser.parse(content)

                update_dict = {self.output_key: parsed_result}

                logger.info(
                    f"Successfully parsed output using {
                        self.output_parser.__class__.__name__}"
                )
                return Command(update=update_dict, goto=goto_node)

            except Exception as parse_error:
                logger.exception(f"Output parser failed: {parse_error}")
                return Command(
                    update={
                        self.output_key: None,
                        "parse_error": f"Parser failed: {parse_error!s}",
                        "raw_content": content,
                    },
                    goto=goto_node,
                )

        except Exception as e:
            logger.exception(f"Error in output parser node: {e}")
            return Command(
                update={
                    self.output_key: None,
                    "parse_error": f"Node error: {
                        e!s}",
                },
                goto=goto_node,
            )

    def _extract_content_from_message(self, message: Any) -> str | None:
        """Extract content from a message, handling different message types.

        Args:
            message: Message to extract content from

        Returns:
            String content or None if extraction fails
        """
        # Handle BaseMessage objects
        if isinstance(message, BaseMessage):
            return message.content

        # Handle dictionary messages
        if isinstance(message, dict):
            if "content" in message:
                return message["content"]
            # Some messages might have the content in different keys
            if "text" in message:
                return message["text"]
            if "message" in message:
                return message["message"]

        # Handle string messages directly
        elif isinstance(message, str):
            return message

        # Handle objects with content attribute
        elif hasattr(message, "content"):
            return message.content

        # Unable to extract content
        return None


# ============================================================================
# CONVENIENCE FACTORY FUNCTIONS
# ============================================================================


def create_json_output_parser_node(
    messages_key: str = "messages",
    output_key: str = "parsed_json",
    agent_node: str = "agent",
    **kwargs,
) -> OutputParserNodeConfig:
    """Create an OutputParserNodeConfig for JSON parsing.

    Args:
        messages_key: State key to get messages from
        output_key: Key to store parsed JSON in
        agent_node: Node to return to after parsing
        **kwargs: Additional config parameters

    Returns:
        Configured OutputParserNodeConfig for JSON parsing
    """
    from langchain_core.output_parsers import JsonOutputParser

    return OutputParserNodeConfig(
        output_parser=JsonOutputParser(),
        messages_key=messages_key,
        output_key=output_key,
        agent_node=agent_node,
        **kwargs,
    )


def create_string_output_parser_node(
    messages_key: str = "messages",
    output_key: str = "parsed_string",
    agent_node: str = "agent",
    **kwargs,
) -> OutputParserNodeConfig:
    """Create an OutputParserNodeConfig for string extraction.

    Args:
        messages_key: State key to get messages from
        output_key: Key to store string content in
        agent_node: Node to return to after parsing
        **kwargs: Additional config parameters

    Returns:
        Configured OutputParserNodeConfig for string extraction
    """
    from langchain_core.output_parsers import StrOutputParser

    return OutputParserNodeConfig(
        output_parser=StrOutputParser(),
        messages_key=messages_key,
        output_key=output_key,
        agent_node=agent_node,
        **kwargs,
    )


def create_pydantic_output_parser_node(
    pydantic_model: type,
    messages_key: str = "messages",
    output_key: str | None = None,
    agent_node: str = "agent",
    **kwargs,
) -> OutputParserNodeConfig:
    """Create an OutputParserNodeConfig for Pydantic model parsing.

    Args:
        pydantic_model: Pydantic model class to parse into
        messages_key: State key to get messages from
        output_key: Key to store parsed model in (defaults to model name)
        agent_node: Node to return to after parsing
        **kwargs: Additional config parameters

    Returns:
        Configured OutputParserNodeConfig for Pydantic parsing
    """
    from langchain_core.output_parsers import PydanticOutputParser

    if output_key is None:
        output_key = f"parsed_{pydantic_model.__name__.lower()}"

    return OutputParserNodeConfig(
        output_parser=PydanticOutputParser(pydantic_object=pydantic_model),
        messages_key=messages_key,
        output_key=output_key,
        agent_node=agent_node,
        **kwargs,
    )


# ============================================================================
# INTEGRATION WITH SIMPLE AGENT
# ============================================================================


def detect_output_parser_need(agent: Any) -> bool:
    """Detect if an agent needs an output parser node.

    Args:
        agent: Agent instance to check

    Returns:
        True if output parser node is needed
    """
    # Check if agent has output_parser field (not synced to engine)
    return hasattr(agent, "output_parser") and agent.output_parser is not None


def create_output_parser_node_for_agent(agent: Any) -> OutputParserNodeConfig | None:
    """Create an output parser node config for an agent if needed.

    Args:
        agent: Agent instance

    Returns:
        OutputParserNodeConfig if needed, None otherwise
    """
    if not detect_output_parser_need(agent):
        return None

    output_key = getattr(agent, "output_parser_field", "parsed_output")

    return OutputParserNodeConfig(
        name="output_parser",
        output_parser=agent.output_parser,
        output_key=output_key,
        agent_node="agent_node",  # Route back to main agent node
    )
