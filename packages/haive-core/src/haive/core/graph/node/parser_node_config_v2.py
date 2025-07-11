"""
Parser Node Configuration V2 - With ToolMessage safety net.

This version extends the original parser node with an optional safety net feature
that can create ToolMessages if they don't already exist in state.

This addresses cases where:
1. Pydantic model validation succeeded but no ToolMessage was created
2. Tool calls exist but corresponding ToolMessages are missing
3. Need to ensure conversation continuity with proper ToolMessages

Config options:
- add_tool_message_safety_net: Whether to create missing ToolMessages
- safety_net_mode: How to handle missing ToolMessages ("create", "warn", "ignore")
"""

import json
import logging
from typing import Any, Dict, List, Optional, Type, Union

from langchain_core.messages import AIMessage, BaseMessage, ToolMessage
from langchain_core.output_parsers import PydanticOutputParser
from langgraph.types import Command
from pydantic import BaseModel, Field

from haive.core.graph.common.types import ConfigLike, NodeType, StateLike
from haive.core.graph.node.base_config import NodeConfig

logger = logging.getLogger(__name__)


class ParserNodeConfigV2(NodeConfig):
    """V2 Parser node with ToolMessage safety net and schema-aware I/O.

    This parser extends the original functionality with:
    1. Optional ToolMessage creation for missing tool responses
    2. Configurable safety net behavior
    3. Better error handling and state management
    4. Schema-aware input/output field handling

    Schema Features:
    - Uses enhanced MessageList for message handling
    - Supports structured output field detection and parsing
    - Engine attribution in generated ToolMessages
    - Selective state field extraction

    Safety net modes:
    - "create": Automatically create missing ToolMessages (default)
    - "warn": Log warnings but don't create ToolMessages
    - "ignore": Skip safety net entirely (V1 behavior)
    """

    node_type: NodeType = Field(default=NodeType.PARSER)
    messages_key: str = Field(default="messages")
    agent_node: str = Field(
        default="agent", description="Node to return to after parsing"
    )

    def model_post_init(self, __context):
        """Setup default field definitions for parser node."""
        if not self.input_field_defs:
            from haive.core.schema.field_registry import StandardFields

            # Parser nodes need messages, tool_routes, and engine info
            self.input_field_defs = [
                StandardFields.messages(use_enhanced=True),
                StandardFields.tool_routes(),
                StandardFields.engine_name(),
            ]

        if not self.output_field_defs:
            from haive.core.schema.field_registry import StandardFields

            # Parser nodes output updated messages and parsed structured output
            self.output_field_defs = [
                StandardFields.messages(use_enhanced=True),
                # Structured output fields will be added dynamically based on tools
            ]

        # Call parent post_init to handle schema setup
        super().model_post_init(__context)

    # Engine reference for getting tools
    engine_name: Optional[str] = Field(
        default=None, description="Name of engine to get tools from"
    )

    # V2 Safety net configuration
    add_tool_message_safety_net: bool = Field(
        default=True, description="Whether to add missing ToolMessages as safety net"
    )
    safety_net_mode: str = Field(
        default="create", description="Safety net mode: 'create', 'warn', or 'ignore'"
    )
    safety_net_success_content: str = Field(
        default="Parsing completed successfully",
        description="Content for success ToolMessages created by safety net",
    )
    safety_net_error_content: str = Field(
        default="Parsing failed",
        description="Content for error ToolMessages created by safety net",
    )

    def _get_engine_from_state(self, state: StateLike) -> Optional[Any]:
        """Get engine from state - same logic as V1."""
        logger.debug(f"Getting engine: {self.engine_name}")

        if not self.engine_name:
            return None

        # Try state.engines first
        if hasattr(state, "engines") and isinstance(state.engines, dict):
            engine = state.engines.get(self.engine_name)
            if engine:
                logger.info(f"Found engine in state.engines: {self.engine_name}")
                return engine

            # Try by engine.name attribute
            for key, eng in state.engines.items():
                if hasattr(eng, "name") and eng.name == self.engine_name:
                    logger.info(f"Found engine by name attribute: {self.engine_name}")
                    return eng

        # Try state attribute
        if hasattr(state, self.engine_name):
            engine = getattr(state, self.engine_name)
            logger.info(f"Found engine as state attribute: {self.engine_name}")
            return engine

        # Try registry
        try:
            from haive.core.engine.base import EngineRegistry

            registry = EngineRegistry.get_instance()
            engine = registry.find(self.engine_name)
            if engine:
                logger.info(f"Found engine in registry: {self.engine_name}")
                return engine
        except Exception as e:
            logger.warning(f"Registry lookup failed: {e}")

        logger.warning(f"Engine not found: {self.engine_name}")
        return None

    def _find_tool_in_engine(self, engine: Any, tool_name: str) -> Optional[Any]:
        """Find a tool/schema in the engine by name - same as V1."""
        logger.debug(f"Searching for tool: '{tool_name}' in engine")

        # Collect all possible tools/schemas from engine
        candidates = []

        # Check tools
        if hasattr(engine, "tools") and engine.tools:
            candidates.extend(engine.tools)

        # Check schemas
        if hasattr(engine, "schemas") and engine.schemas:
            candidates.extend(engine.schemas)

        # Check pydantic_tools
        if hasattr(engine, "pydantic_tools") and engine.pydantic_tools:
            candidates.extend(engine.pydantic_tools)

        # Check structured_output_model
        if (
            hasattr(engine, "structured_output_model")
            and engine.structured_output_model
        ):
            candidates.append(engine.structured_output_model)

        # Search through candidates
        for candidate in candidates:
            candidate_name = None

            # Get candidate name
            if hasattr(candidate, "__name__"):
                candidate_name = candidate.__name__
            elif hasattr(candidate, "name"):
                candidate_name = candidate.name

            if candidate_name == tool_name:
                logger.info(f"Found matching tool: {tool_name}")
                return candidate

        logger.warning(f"Tool '{tool_name}' not found in engine")
        return None

    def _extract_tool_from_messages(
        self, messages: List[BaseMessage]
    ) -> tuple[Optional[str], Optional[Any], Optional[ToolMessage]]:
        """Extract tool information from messages - same as V1."""
        logger.debug("Extracting tool information from messages")

        # Find the last AIMessage with tool calls
        last_ai_message = None
        for i, msg in enumerate(reversed(messages)):
            if isinstance(msg, AIMessage):
                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    last_ai_message = msg
                    break
                elif (
                    hasattr(msg, "additional_kwargs")
                    and "tool_calls" in msg.additional_kwargs
                ):
                    last_ai_message = msg
                    break

        if not last_ai_message:
            logger.warning("No AIMessage with tool calls found")
            return None, None, None

        # Get tool calls
        tool_calls = []
        if hasattr(last_ai_message, "tool_calls") and last_ai_message.tool_calls:
            tool_calls = last_ai_message.tool_calls
        elif (
            hasattr(last_ai_message, "additional_kwargs")
            and "tool_calls" in last_ai_message.additional_kwargs
        ):
            tool_calls = last_ai_message.additional_kwargs["tool_calls"]

        if not tool_calls:
            logger.warning("No tool calls found in AIMessage")
            return None, None, None

        # Get the last tool call
        tool_call = tool_calls[-1]

        # Extract tool name
        if hasattr(tool_call, "name"):
            tool_name = tool_call.name
        elif isinstance(tool_call, dict) and "name" in tool_call:
            tool_name = tool_call["name"]
        elif (
            isinstance(tool_call, dict)
            and "function" in tool_call
            and "name" in tool_call["function"]
        ):
            tool_name = tool_call["function"]["name"]
        else:
            logger.error("Could not extract tool name from tool call")
            return None, None, None

        tool_id = getattr(tool_call, "id", tool_call.get("id", "unknown"))

        logger.info(f"Found tool call: {tool_name}")

        # Find corresponding ToolMessage
        tool_message = None
        ai_msg_index = messages.index(last_ai_message)
        for msg in messages[ai_msg_index:]:
            if isinstance(msg, ToolMessage):
                if (
                    getattr(msg, "name", None) == tool_name
                    or getattr(msg, "tool_call_id", None) == tool_id
                ):
                    tool_message = msg
                    logger.info("Found matching ToolMessage")
                    break

        if not tool_message:
            logger.warning(f"No ToolMessage found for tool '{tool_name}'")

        return tool_name, tool_call, tool_message

    def _parse_tool_content(self, content: Any, tool_class: Type[BaseModel]) -> Any:
        """Parse tool content into a Pydantic model - same as V1."""
        logger.debug(f"Parsing content for: {tool_class.__name__}")

        # If content is already the right type, return it
        if isinstance(content, tool_class):
            logger.info("Content already correct type")
            return content

        # Try JSON parsing first if content is string
        if isinstance(content, str):
            try:
                json_data = json.loads(content)

                # V2 CHECK: If this looks like a V2 validation wrapper, extract the data
                if (
                    isinstance(json_data, dict)
                    and "data" in json_data
                    and "validated" in json_data
                ):
                    logger.debug(
                        "Detected V2 validation wrapper, extracting data field"
                    )
                    json_data = json_data["data"]

                model_instance = tool_class.model_validate(json_data)
                logger.info(f"Successfully created {tool_class.__name__} from JSON")
                return model_instance
            except (json.JSONDecodeError, Exception) as e:
                logger.debug(f"JSON parsing failed: {e}")

        # Try direct model validation if content is dict
        if isinstance(content, dict):
            try:
                # V2 CHECK: If this looks like a V2 validation wrapper, extract the data
                if "data" in content and "validated" in content:
                    logger.debug(
                        "Detected V2 validation wrapper, extracting data field"
                    )
                    content = content["data"]

                model_instance = tool_class.model_validate(content)
                logger.info(f"Successfully created {tool_class.__name__} from dict")
                return model_instance
            except Exception as e:
                logger.debug(f"Direct validation failed: {e}")

        # Try PydanticOutputParser as last resort
        try:
            parser = PydanticOutputParser(pydantic_object=tool_class)
            model_instance = parser.parse(str(content))
            logger.info("Successfully parsed with PydanticOutputParser")
            return model_instance
        except Exception as e:
            logger.error(f"PydanticOutputParser failed: {e}")

        # Final fallback
        logger.warning("All parsing attempts failed, returning content as dict")
        return {"content": content, "parse_error": "Could not parse into model"}

    def _create_safety_net_tool_message(
        self,
        tool_name: str,
        tool_call: Any,
        success: bool = True,
        parsed_result: Any = None,
        error: str = None,
    ) -> ToolMessage:
        """Create a ToolMessage as safety net when one is missing."""
        tool_id = getattr(tool_call, "id", tool_call.get("id", "unknown"))

        if success and parsed_result is not None:
            # Success ToolMessage
            if isinstance(parsed_result, BaseModel):
                content = json.dumps(parsed_result.model_dump(), indent=2)
            else:
                content = str(parsed_result)

            return ToolMessage(
                content=content,
                tool_call_id=tool_id,
                name=tool_name,
                additional_kwargs={
                    "is_error": False,
                    "created_by": "parser_safety_net",
                    "success": True,
                },
            )
        else:
            # Error ToolMessage
            error_content = {
                "success": False,
                "error": error or "Unknown parsing error",
                "tool": tool_name,
            }

            return ToolMessage(
                content=json.dumps(error_content),
                tool_call_id=tool_id,
                name=tool_name,
                additional_kwargs={
                    "is_error": True,
                    "created_by": "parser_safety_net",
                    "success": False,
                },
            )

    def _apply_safety_net(
        self,
        messages: List[BaseMessage],
        tool_name: str,
        tool_call: Any,
        tool_message: Optional[ToolMessage],
        parsed_result: Any = None,
        parsing_success: bool = True,
        error: str = None,
    ) -> List[BaseMessage]:
        """Apply safety net by adding missing ToolMessage if needed."""

        if not self.add_tool_message_safety_net:
            return messages

        if self.safety_net_mode == "ignore":
            return messages

        # Check if ToolMessage already exists
        if tool_message is not None:
            logger.debug("ToolMessage already exists, safety net not needed")
            return messages

        # ToolMessage is missing - apply safety net
        if self.safety_net_mode == "warn":
            logger.warning(
                f"Safety net: Missing ToolMessage for {tool_name} (warn mode)"
            )
            return messages

        elif self.safety_net_mode == "create":
            logger.info(f"Safety net: Creating missing ToolMessage for {tool_name}")

            # Create the missing ToolMessage
            safety_tool_message = self._create_safety_net_tool_message(
                tool_name, tool_call, parsing_success, parsed_result, error
            )

            # Add it to messages
            updated_messages = list(messages) + [safety_tool_message]
            logger.info("Safety net: Added ToolMessage to state")
            return updated_messages

        return messages

    def __call__(
        self, state: StateLike, config: Optional[ConfigLike] = None
    ) -> Command:
        """Parse the tool message into a Pydantic model with V2 safety net."""
        logger.info("=== ParserNodeConfigV2 Execution ===")
        logger.debug(f"Safety net enabled: {self.add_tool_message_safety_net}")
        logger.debug(f"Safety net mode: {self.safety_net_mode}")

        # Determine goto node
        goto_node = self.command_goto or self.agent_node

        # Get messages from state
        messages = getattr(state, self.messages_key, [])
        if not messages:
            logger.error("No messages found in state")
            return Command(update={"error": "No messages found"}, goto=goto_node)

        logger.info(f"Processing {len(messages)} messages")

        # Extract tool information from messages
        tool_name, tool_call, tool_message = self._extract_tool_from_messages(messages)

        if not tool_name:
            logger.error("Could not extract tool information from messages")
            return Command(
                update={"error": "No tool information found"}, goto=goto_node
            )

        # Get the tool class from engine
        logger.info(f"Looking up tool class for: {tool_name}")

        tool_class = None
        engine = self._get_engine_from_state(state)

        if engine:
            tool_class = self._find_tool_in_engine(engine, tool_name)
        else:
            logger.warning("No engine available for tool lookup")

        if not tool_class:
            logger.error(f"Tool class not found for: {tool_name}")

            # Apply safety net for unknown tool
            updated_messages = self._apply_safety_net(
                messages,
                tool_name,
                tool_call,
                tool_message,
                parsing_success=False,
                error=f"Tool '{tool_name}' not found in engine",
            )

            update_dict = {"error": f"Tool '{tool_name}' not found in engine"}
            if updated_messages != messages:
                update_dict[self.messages_key] = updated_messages

            return Command(update=update_dict, goto=goto_node)

        # Parse the tool response
        logger.info("Parsing tool response")

        content = None
        parsed_result = None
        parsing_success = True
        parse_error = None

        # Try to get content from ToolMessage first
        if tool_message and hasattr(tool_message, "content"):
            content = tool_message.content
            logger.debug("Using content from ToolMessage")
        # Fallback to tool_call args
        elif tool_call:
            if hasattr(tool_call, "args"):
                content = tool_call.args
                logger.debug("Using args from tool_call (object)")
            elif isinstance(tool_call, dict):
                content = tool_call.get("args", tool_call.get("arguments"))
                logger.debug("Using args from tool_call (dict)")
        else:
            logger.error("No content available for parsing")

            # Apply safety net for missing content
            updated_messages = self._apply_safety_net(
                messages,
                tool_name,
                tool_call,
                tool_message,
                parsing_success=False,
                error=f"No content for tool '{tool_name}'",
            )

            update_dict = {"error": f"No content for tool '{tool_name}'"}
            if updated_messages != messages:
                update_dict[self.messages_key] = updated_messages

            return Command(update=update_dict, goto=goto_node)

        # Parse the content
        try:
            if isinstance(tool_class, type) and issubclass(tool_class, BaseModel):
                parsed_result = self._parse_tool_content(content, tool_class)
            else:
                logger.warning(f"Tool is not a Pydantic model: {type(tool_class)}")
                parsed_result = content

            # Determine field name for the result using proper naming utilities
            if isinstance(tool_class, type) and issubclass(tool_class, BaseModel):
                from haive.core.schema.field_utils import get_field_info_from_model

                field_info = get_field_info_from_model(tool_class)
                field_name = field_info["field_name"]
            else:
                # Fallback for non-Pydantic models
                field_name = (
                    tool_name.lower()
                    .replace("response", "")
                    .replace("result", "")
                    .strip()
                )
                if not field_name:
                    field_name = "parsed_result"

            logger.info("Successfully parsed tool response")

            # Apply safety net - create ToolMessage if missing
            updated_messages = self._apply_safety_net(
                messages,
                tool_name,
                tool_call,
                tool_message,
                parsed_result,
                parsing_success=True,
            )

            # Create update
            update_dict = {field_name: parsed_result}

            # Add updated messages if safety net was applied
            if updated_messages != messages:
                update_dict[self.messages_key] = updated_messages
                logger.info("Updated messages with safety net ToolMessage")

            logger.info("Parser V2 completed successfully")
            return Command(update=update_dict, goto=goto_node)

        except Exception as e:
            logger.exception(f"Failed to parse tool response: {e}")
            parsing_success = False
            parse_error = str(e)

            # Apply safety net for parsing error
            updated_messages = self._apply_safety_net(
                messages,
                tool_name,
                tool_call,
                tool_message,
                parsing_success=False,
                error=f"Parse error for '{tool_name}': {parse_error}",
            )

            update_dict = {"error": f"Parse error for '{tool_name}': {parse_error}"}
            if updated_messages != messages:
                update_dict[self.messages_key] = updated_messages

            return Command(update=update_dict, goto=goto_node)
