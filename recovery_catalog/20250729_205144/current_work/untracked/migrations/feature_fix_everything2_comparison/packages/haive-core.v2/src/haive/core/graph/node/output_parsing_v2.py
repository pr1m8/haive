"""Output_Parsing_V2 graph module.

This module provides output parsing v2 functionality for the Haive framework.

Classes:
    OutputParserNodeConfig: OutputParserNodeConfig implementation.
    JsonParserNodeConfig: JsonParserNodeConfig implementation.
    PydanticParserNodeConfig: PydanticParserNodeConfig implementation.

Functions:
    get_default_input_fields: Get Default Input Fields functionality.
    get_default_output_fields: Get Default Output Fields functionality.
"""

# ============================================================================
# OUTPUT PARSER NODE CONFIG V2 - WITH SCHEMA SUPPORT
# ============================================================================

import logging
from typing import Any, Optional, TypeVar

from langchain_core.messages import BaseMessage
from langchain_core.output_parsers.base import BaseOutputParser
from langgraph.types import Command
from pydantic import BaseModel, Field
from rich.console import Console

from haive.core.graph.common.types import ConfigLike, StateLike
from haive.core.graph.node.base_node_config import BaseNodeConfig
from haive.core.graph.node.types import NodeType
from haive.core.schema.field_definition import FieldDefinition
from haive.core.schema.field_registry import StandardFields
from haive.core.schema.field_utils import create_field_name_from_model

logger = logging.getLogger(__name__)
console = Console()
logger.setLevel(logging.WARNING)

# Type variables for input/output schemas
TInput = TypeVar("TInput", bound=BaseModel)
TOutput = TypeVar("TOutput", bound=BaseModel)


class OutputParserNodeConfig(BaseNodeConfig[TInput, TOutput]):
    """Configuration for a node that parses LLM output using LangChain output parsers.

    This node extracts content from messages and parses it into structured data
    using LangChain output parsers. It supports multiple schema patterns through
    input/output schema definitions.

    Input Schema Requirements:
    - Must have a 'messages' field (List[BaseMessage]) or custom messages field

    Output Schema:
    - Will contain the parsed result field (type depends on parser)
    - Optional error fields for parse failures
    """

    node_type: NodeType = Field(default=NodeType.OUTPUT_PARSER)

    # Output parser configuration
    output_parser: BaseOutputParser = Field(
        ..., description="LangChain output parser to use for parsing"
    )

    # Field names
    messages_field: str = Field(
        default="messages", description="Name of the messages field in input schema"
    )

    output_field: str | None = Field(
        default=None, description="Name of the parsed output field in output schema"
    )

    error_field: str = Field(
        default="parse_error", description="Name of the error field in output schema"
    )

    raw_content_field: str = Field(
        default="raw_content",
        description="Name of the raw content field in output schema (on error)",
    )

    # Parsing options
    parse_all_messages: bool = Field(
        default=False, description="Whether to parse all messages or just the last one"
    )

    continue_on_error: bool = Field(
        default=True, description="Whether to continue to next node on parse error"
    )

    def get_default_input_fields(self) -> list[FieldDefinition]:
        """Get default input field definitions."""
        return [StandardFields.messages(use_enhanced=True)]

    def get_default_output_fields(self) -> list[FieldDefinition]:
        """Get default output field definitions based on parser type."""
        fields = []

        # Determine output field name and type
        output_field_name = self.output_field
        if not output_field_name:
            # Try to infer from parser
            if hasattr(self.output_parser, "pydantic_object"):
                # Pydantic parser
                model = self.output_parser.pydantic_object
                output_field_name = create_field_name_from_model(model)
                fields.append(
                    StandardFields.structured_output(
                        model_class=model, field_name=output_field_name
                    )
                )
            else:
                # Generic parsed output
                output_field_name = "parsed_output"
                fields.append(
                    FieldDefinition(
                        name=output_field_name,
                        field_type=Optional[Any],
                        default=None,
                        description="Parsed output from the parser",
                    )
                )

        # Add error fields
        fields.extend(
            [
                FieldDefinition(
                    name=self.error_field,
                    field_type=Optional[str],
                    default=None,
                    description="Parse error message if parsing failed",
                ),
                FieldDefinition(
                    name=self.raw_content_field,
                    field_type=Optional[str],
                    default=None,
                    description="Raw content that failed to parse",
                ),
            ]
        )

        return fields

    def __call__(self, state: StateLike, config: ConfigLike | None = None) -> Command:
        """Parse message content using the output parser."""
        # Get messages from state
        messages = self._get_messages_from_state(state)

        if not messages:
            logger.warning(
                f"No messages found in field '{
                    self.messages_field}'"
            )
            return self._create_error_response(
                "No messages found", goto_node=self._get_goto_node()
            )

        try:
            # Determine which messages to parse
            messages_to_parse = messages if self.parse_all_messages else [messages[-1]]

            # Extract and parse content
            parsed_results = []
            errors = []

            for message in messages_to_parse:
                content = self._extract_content_from_message(message)
                if content is None:
                    errors.append(f"No content in message: {type(message)}")
                    continue

                try:
                    parsed = self.output_parser.parse(content)
                    parsed_results.append(parsed)
                except Exception as e:
                    errors.append(f"Parse error: {e!s}")
                    if not self.continue_on_error:
                        return self._create_error_response(
                            str(e), raw_content=content, goto_node=self._get_goto_node()
                        )

            # Prepare output
            if parsed_results:
                # Use the last successful parse result
                result = (
                    parsed_results[-1]
                    if not self.parse_all_messages
                    else parsed_results
                )
                return self._create_success_response(result)
            # All parsing failed
            error_msg = "; ".join(errors) if errors else "No content to parse"
            return self._create_error_response(
                error_msg, goto_node=self._get_goto_node()
            )

        except Exception as e:
            logger.exception(f"Error in output parser node: {e}")
            return self._create_error_response(
                f"Node error: {e!s}", goto_node=self._get_goto_node()
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

    def _get_goto_node(self) -> str:
        """Get the node to go to after parsing."""
        return self.command_goto or "agent"

    def _create_success_response(self, parsed_result: Any) -> Command:
        """Create a successful parse response."""
        output_field = self.output_field or "parsed_output"

        update_dict = {
            output_field: parsed_result,
            self.error_field: None,
            self.raw_content_field: None,
        }

        logger.info(
            f"Successfully parsed output using {
                self.output_parser.__class__.__name__}"
        )

        return Command(update=update_dict, goto=self._get_goto_node())

    def _create_error_response(
        self,
        error_msg: str,
        raw_content: str | None = None,
        goto_node: str | None = None,
    ) -> Command:
        """Create an error response."""
        output_field = self.output_field or "parsed_output"

        update_dict = {
            output_field: None,
            self.error_field: error_msg,
            self.raw_content_field: raw_content,
        }

        goto = goto_node or self._get_goto_node()

        return Command(update=update_dict, goto=goto)


# ============================================================================
# SPECIALIZED OUTPUT PARSER NODES
# ============================================================================


class JsonParserNodeConfig(OutputParserNodeConfig):
    """Specialized node for JSON parsing."""

    def __init__(self, **kwargs) -> None:
        from langchain_core.output_parsers import JsonOutputParser

        if "output_parser" not in kwargs:
            kwargs["output_parser"] = JsonOutputParser()
        if "output_field" not in kwargs:
            kwargs["output_field"] = "parsed_json"

        super().__init__(**kwargs)

    def get_default_output_fields(self) -> list[FieldDefinition]:
        """JSON parser outputs a dictionary."""
        return [
            FieldDefinition(
                name=self.output_field or "parsed_json",
                field_type=Optional[dict[str, Any]],
                default=None,
                description="Parsed JSON data",
            ),
            FieldDefinition(
                name=self.error_field,
                field_type=Optional[str],
                default=None,
                description="Parse error message if parsing failed",
            ),
            FieldDefinition(
                name=self.raw_content_field,
                field_type=Optional[str],
                default=None,
                description="Raw content that failed to parse",
            ),
        ]


class PydanticParserNodeConfig(OutputParserNodeConfig):
    """Specialized node for Pydantic model parsing."""

    pydantic_model: type[BaseModel] = Field(
        ..., description="Pydantic model to parse into"
    )

    def __init__(self, **kwargs) -> None:
        from langchain_core.output_parsers import PydanticOutputParser

        # Extract pydantic_model before super().__init__
        pydantic_model = kwargs.get("pydantic_model")
        if not pydantic_model:
            raise ValueError("pydantic_model is required for PydanticParserNodeConfig")

        if "output_parser" not in kwargs:
            kwargs["output_parser"] = PydanticOutputParser(
                pydantic_object=pydantic_model
            )
        if "output_field" not in kwargs:
            kwargs["output_field"] = create_field_name_from_model(pydantic_model)

        super().__init__(**kwargs)

    def get_default_output_fields(self) -> list[FieldDefinition]:
        """Pydantic parser outputs a specific model."""
        return [
            StandardFields.structured_output(
                model_class=self.pydantic_model, field_name=self.output_field
            ),
            FieldDefinition(
                name=self.error_field,
                field_type=Optional[str],
                default=None,
                description="Parse error message if parsing failed",
            ),
            FieldDefinition(
                name=self.raw_content_field,
                field_type=Optional[str],
                default=None,
                description="Raw content that failed to parse",
            ),
        ]


class ListParserNodeConfig(OutputParserNodeConfig):
    """Specialized node for list parsing."""

    list_type: str = Field(
        default="comma_separated",
        description="Type of list parsing: comma_separated, numbered, markdown",
    )

    def __init__(self, **kwargs) -> None:
        list_type = kwargs.get("list_type", "comma_separated")

        if "output_parser" not in kwargs:
            if list_type == "comma_separated":
                from langchain_core.output_parsers import CommaSeparatedListOutputParser

                kwargs["output_parser"] = CommaSeparatedListOutputParser()
            elif list_type == "numbered":
                from langchain.output_parsers import NumberedListOutputParser

                kwargs["output_parser"] = NumberedListOutputParser()
            elif list_type == "markdown":
                from langchain.output_parsers import MarkdownListOutputParser

                kwargs["output_parser"] = MarkdownListOutputParser()
            else:
                raise ValueError(f"Unknown list_type: {list_type}")

        if "output_field" not in kwargs:
            kwargs["output_field"] = "parsed_list"

        super().__init__(**kwargs)

    def get_default_output_fields(self) -> list[FieldDefinition]:
        """List parser outputs a list of strings."""
        return [
            FieldDefinition(
                name=self.output_field or "parsed_list",
                field_type=Optional[list[str]],
                default=None,
                description="Parsed list of items",
            ),
            FieldDefinition(
                name=self.error_field,
                field_type=Optional[str],
                default=None,
                description="Parse error message if parsing failed",
            ),
            FieldDefinition(
                name=self.raw_content_field,
                field_type=Optional[str],
                default=None,
                description="Raw content that failed to parse",
            ),
        ]


# ============================================================================
# CONVENIENCE FACTORY FUNCTIONS
# ============================================================================


def create_json_parser_node(
    name: str = "json_parser",
    messages_field: str = "messages",
    output_field: str = "parsed_json",
    **kwargs,
) -> JsonParserNodeConfig:
    """Create a JSON parser node."""
    return JsonParserNodeConfig(
        name=name, messages_field=messages_field, output_field=output_field, **kwargs
    )


def create_pydantic_parser_node(
    pydantic_model: type[BaseModel],
    name: str | None = None,
    messages_field: str = "messages",
    output_field: str | None = None,
    **kwargs,
) -> PydanticParserNodeConfig:
    """Create a Pydantic model parser node."""
    if not name:
        name = f"parse_{pydantic_model.__name__.lower()}"

    return PydanticParserNodeConfig(
        name=name,
        pydantic_model=pydantic_model,
        messages_field=messages_field,
        output_field=output_field,
        **kwargs,
    )


def create_list_parser_node(
    name: str = "list_parser",
    list_type: str = "comma_separated",
    messages_field: str = "messages",
    output_field: str = "parsed_list",
    **kwargs,
) -> ListParserNodeConfig:
    """Create a list parser node."""
    return ListParserNodeConfig(
        name=name,
        list_type=list_type,
        messages_field=messages_field,
        output_field=output_field,
        **kwargs,
    )


# ============================================================================
# INTEGRATION WITH AGENTS
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

    output_field = getattr(agent, "output_parser_field", "parsed_output")

    # Check if it's a Pydantic parser
    if hasattr(agent.output_parser, "pydantic_object"):
        return PydanticParserNodeConfig(
            name="output_parser",
            pydantic_model=agent.output_parser.pydantic_object,
            output_field=output_field,
            command_goto="agent_node",
        )

    # Generic output parser
    return OutputParserNodeConfig(
        name="output_parser",
        output_parser=agent.output_parser,
        output_field=output_field,
        command_goto="agent_node",
    )
