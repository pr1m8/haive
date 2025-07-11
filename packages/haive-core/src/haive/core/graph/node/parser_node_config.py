# src/haive/core/graph/node/parser_node_config.py

import json
import logging
from typing import Any, Dict, List, Optional, Type, Union

from langchain_core.messages import AIMessage, BaseMessage, ToolMessage
from langchain_core.output_parsers import PydanticOutputParser
from langgraph.types import Command
from pydantic import BaseModel, Field

from haive.core.graph.common.types import ConfigLike, NodeType, StateLike
from haive.core.graph.node.base_config import NodeConfig

# Configure logger with rich handler
logger = logging.getLogger(__name__)

# Add rich handler if not already present
if not any(isinstance(handler, logging.StreamHandler) for handler in logger.handlers):
    from rich.logging import RichHandler

    handler = RichHandler(
        rich_tracebacks=True,
        show_time=True,
        show_path=True,
        enable_link_path=True,
        markup=True,
        log_time_format="[%Y-%m-%d %H:%M:%S]",
    )
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)


class ParserNodeConfig(NodeConfig):
    """Configuration for a node that parses tool outputs into Pydantic models.

    This node extracts tool information from the AI messages and parses
    the tool responses into structured Pydantic models.
    """

    node_type: NodeType = Field(default=NodeType.PARSER)
    messages_key: str = Field(default="messages")
    agent_node: str = Field(
        default="agent", description="Node to return to after parsing"
    )

    # Engine reference for getting tools
    engine_name: Optional[str] = Field(
        default=None, description="Name of engine to get tools from"
    )

    def _get_engine_from_state(self, state: StateLike) -> Optional[Any]:
        """Get engine from state.engines or registry."""
        logger.debug(f"[bold blue]Getting engine:[/bold blue] {self.engine_name}")

        if not self.engine_name:
            logger.warning("[bold yellow]No engine name configured[/bold yellow]")
            return None

        # FIRST: Try to get from state.engines using engine name
        if hasattr(state, "engines") and isinstance(state.engines, dict):
            logger.debug(f"  State has engines dict with {len(state.engines)} engines")
            logger.debug(f"  Available engine keys: {list(state.engines.keys())}")

            # Try exact name match
            engine = state.engines.get(self.engine_name)
            if engine:
                logger.info(
                    f"[bold green]✓ Found engine in state.engines:[/bold green] {self.engine_name}"
                )
                logger.debug(f"    Engine type: {type(engine).__name__}")
                return engine

            # Try to find by engine.name attribute
            for key, eng in state.engines.items():
                if hasattr(eng, "name") and eng.name == self.engine_name:
                    logger.info(
                        f"[bold green]✓ Found engine by name attribute:[/bold green] {self.engine_name} (key: {key})"
                    )
                    return eng

        # SECOND: Try to get from state directly (if engines are stored as attributes)
        if hasattr(state, self.engine_name):
            engine = getattr(state, self.engine_name)
            logger.info(
                f"[bold green]✓ Found engine as state attribute:[/bold green] {self.engine_name}"
            )
            return engine

        # LAST: Fallback to registry
        logger.debug("  Engine not found in state, trying registry...")
        try:
            from haive.core.engine.base import EngineRegistry

            registry = EngineRegistry.get_instance()
            engine = registry.find(self.engine_name)
            if engine:
                logger.info(
                    f"[bold green]✓ Found engine in EngineRegistry:[/bold green] {self.engine_name}"
                )
                return engine
            else:
                logger.warning(
                    f"[bold yellow]Engine not found in registry:[/bold yellow] {self.engine_name}"
                )
                return None
        except ImportError as e:
            logger.error(f"[bold red]Failed to import EngineRegistry:[/bold red] {e}")
            return None
        except Exception as e:
            logger.exception(f"[bold red]Error getting engine:[/bold red] {e}")
            return None

    def _find_tool_in_engine(self, engine: Any, tool_name: str) -> Optional[Any]:
        """Find a tool/schema in the engine by name."""
        logger.debug(
            f"[bold blue]Searching for tool:[/bold blue] '{tool_name}' in engine"
        )

        # Collect all possible tools/schemas from engine
        candidates = []

        # Check tools
        if hasattr(engine, "tools") and engine.tools:
            candidates.extend(engine.tools)
            logger.debug(f"  Found {len(engine.tools)} tools in engine.tools")

        # Check schemas
        if hasattr(engine, "schemas") and engine.schemas:
            candidates.extend(engine.schemas)
            logger.debug(f"  Found {len(engine.schemas)} schemas in engine.schemas")

        # Check pydantic_tools
        if hasattr(engine, "pydantic_tools") and engine.pydantic_tools:
            candidates.extend(engine.pydantic_tools)
            logger.debug(f"  Found {len(engine.pydantic_tools)} pydantic_tools")

        # Check structured_output_model
        if (
            hasattr(engine, "structured_output_model")
            and engine.structured_output_model
        ):
            candidates.append(engine.structured_output_model)
            logger.debug("  Found structured_output_model")

        # Search through candidates
        logger.debug(
            f"[bold cyan]Searching through {len(candidates)} candidates[/bold cyan]"
        )
        for candidate in candidates:
            candidate_name = None

            # Get candidate name
            if hasattr(candidate, "__name__"):
                candidate_name = candidate.__name__
            elif hasattr(candidate, "name"):
                candidate_name = candidate.name

            logger.debug(
                f"  Checking candidate: {candidate_name} (type: {type(candidate).__name__})"
            )

            if candidate_name == tool_name:
                logger.info(
                    f"[bold green]✓ Found matching tool:[/bold green] {tool_name}"
                )
                return candidate

        logger.warning(
            f"[bold yellow]Tool '{tool_name}' not found in engine[/bold yellow]"
        )

        # Log available tools for debugging
        available_names = []
        for candidate in candidates:
            if hasattr(candidate, "__name__"):
                available_names.append(candidate.__name__)
            elif hasattr(candidate, "name"):
                available_names.append(candidate.name)

        if available_names:
            logger.debug(f"  Available tools: {available_names}")

        return None

    def _extract_tool_from_messages(
        self, messages: List[BaseMessage]
    ) -> tuple[Optional[str], Optional[Any], Optional[ToolMessage]]:
        """Extract tool information from messages."""
        logger.debug("[bold blue]Extracting tool information from messages[/bold blue]")

        # Find the last AIMessage with tool calls
        last_ai_message = None
        for i, msg in enumerate(reversed(messages)):
            if isinstance(msg, AIMessage):
                logger.debug(f"  Found AIMessage at position {len(messages)-1-i}")
                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    last_ai_message = msg
                    logger.debug(f"    Has {len(msg.tool_calls)} tool calls")
                    break
                elif (
                    hasattr(msg, "additional_kwargs")
                    and "tool_calls" in msg.additional_kwargs
                ):
                    last_ai_message = msg
                    logger.debug(f"    Has tool calls in additional_kwargs")
                    break

        if not last_ai_message:
            logger.warning(
                "[bold yellow]No AIMessage with tool calls found[/bold yellow]"
            )
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
            logger.warning(
                "[bold yellow]No tool calls found in AIMessage[/bold yellow]"
            )
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
            logger.error(
                "[bold red]Could not extract tool name from tool call[/bold red]"
            )
            return None, None, None

        logger.info(f"[bold cyan]Found tool call:[/bold cyan] {tool_name}")
        logger.debug(
            f"  Tool call ID: {getattr(tool_call, 'id', tool_call.get('id', 'N/A'))}"
        )
        logger.debug(
            f"  Tool call args: {getattr(tool_call, 'args', tool_call.get('args', {}))}"
        )

        # Find corresponding ToolMessage
        tool_message = None
        # Look for ToolMessage after the AIMessage
        ai_msg_index = messages.index(last_ai_message)
        for msg in messages[ai_msg_index:]:
            if isinstance(msg, ToolMessage):
                msg_name = getattr(msg, "name", None)
                if msg_name == tool_name:
                    tool_message = msg
                    logger.info(
                        f"[bold green]✓ Found matching ToolMessage[/bold green]"
                    )
                    logger.debug(f"  Content type: {type(msg.content)}")
                    logger.debug(f"  Content preview: {str(msg.content)[:100]}...")
                    break

        if not tool_message:
            logger.warning(
                f"[bold yellow]No ToolMessage found for tool '{tool_name}'[/bold yellow]"
            )

        return tool_name, tool_call, tool_message

    def _parse_tool_content(self, content: Any, tool_class: Type[BaseModel]) -> Any:
        """Parse tool content into a Pydantic model."""
        logger.debug(
            f"[bold blue]Parsing content for:[/bold blue] {tool_class.__name__}"
        )
        logger.debug(f"  Content type: {type(content)}")
        logger.debug(f"  Content preview: {str(content)[:200]}...")

        # If content is already the right type, return it
        if isinstance(content, tool_class):
            logger.info("[bold green]✓ Content already correct type[/bold green]")
            return content

        # Try JSON parsing first if content is string
        if isinstance(content, str):
            try:
                logger.debug("  Attempting JSON parsing...")
                json_data = json.loads(content)
                logger.debug(f"  JSON parsed successfully: {type(json_data)}")

                # Validate with Pydantic
                model_instance = tool_class.model_validate(json_data)
                logger.info(
                    f"[bold green]✓ Successfully created {tool_class.__name__} from JSON[/bold green]"
                )
                return model_instance

            except json.JSONDecodeError as e:
                logger.debug(f"  JSON parsing failed: {e}")
            except Exception as e:
                logger.debug(f"  Model validation failed: {e}")

        # Try direct model validation if content is dict
        if isinstance(content, dict):
            try:
                logger.debug("  Attempting direct model validation from dict...")
                model_instance = tool_class.model_validate(content)
                logger.info(
                    f"[bold green]✓ Successfully created {tool_class.__name__} from dict[/bold green]"
                )
                return model_instance
            except Exception as e:
                logger.debug(f"  Direct validation failed: {e}")

        # Try PydanticOutputParser as last resort
        try:
            logger.debug("  Attempting PydanticOutputParser...")
            parser = PydanticOutputParser(pydantic_object=tool_class)
            model_instance = parser.parse(str(content))
            logger.info(
                f"[bold green]✓ Successfully parsed with PydanticOutputParser[/bold green]"
            )
            return model_instance
        except Exception as e:
            logger.error(f"[bold red]PydanticOutputParser failed:[/bold red] {e}")

        # Final fallback
        logger.warning(
            "[bold yellow]All parsing attempts failed, returning content as dict[/bold yellow]"
        )
        return {"content": content, "parse_error": "Could not parse into model"}

    def __call__(
        self, state: StateLike, config: Optional[ConfigLike] = None
    ) -> Command:
        """Parse the tool message into a Pydantic model."""
        logger.info("[bold magenta]=== ParserNodeConfig Execution ===[/bold magenta]")
        logger.debug(f"State type: {type(state).__name__}")
        logger.debug(f"Config: {config}")

        # Log state contents for debugging
        if hasattr(state, "__dict__"):
            logger.debug(f"State attributes: {list(state.__dict__.keys())}")
        if hasattr(state, "engines"):
            logger.debug(
                f"State.engines keys: {list(state.engines.keys()) if isinstance(state.engines, dict) else 'Not a dict'}"
            )

        # Determine goto node
        goto_node = self.command_goto or self.agent_node
        logger.debug(f"[bold cyan]Goto node:[/bold cyan] {goto_node}")

        # Get messages from state
        messages = getattr(state, self.messages_key, [])
        if not messages:
            logger.error("[bold red]No messages found in state[/bold red]")
            return Command(update={"error": "No messages found"}, goto=goto_node)

        logger.info(f"[bold cyan]Processing {len(messages)} messages[/bold cyan]")

        # Extract tool information from messages
        tool_name, tool_call, tool_message = self._extract_tool_from_messages(messages)

        if not tool_name:
            logger.error(
                "[bold red]Could not extract tool information from messages[/bold red]"
            )
            return Command(
                update={"error": "No tool information found"}, goto=goto_node
            )

        # Get the tool class from engine
        logger.info(f"[bold blue]Looking up tool class for:[/bold blue] {tool_name}")

        tool_class = None
        engine = self._get_engine_from_state(state)

        if engine:
            tool_class = self._find_tool_in_engine(engine, tool_name)
        else:
            logger.warning(
                "[bold yellow]No engine available for tool lookup[/bold yellow]"
            )

        if not tool_class:
            logger.error(f"[bold red]Tool class not found for:[/bold red] {tool_name}")
            return Command(
                update={"error": f"Tool '{tool_name}' not found in engine"},
                goto=goto_node,
            )

        # Parse the tool response
        logger.info("[bold blue]Parsing tool response[/bold blue]")

        content = None
        parsed_result = None

        # Try to get content from ToolMessage first
        if tool_message and hasattr(tool_message, "content"):
            content = tool_message.content
            logger.debug("  Using content from ToolMessage")
        # Fallback to tool_call args
        elif tool_call:
            if hasattr(tool_call, "args"):
                content = tool_call.args
                logger.debug("  Using args from tool_call (object)")
            elif isinstance(tool_call, dict):
                content = tool_call.get("args", tool_call.get("arguments"))
                logger.debug("  Using args from tool_call (dict)")
        else:
            logger.error("[bold red]No content available for parsing[/bold red]")
            return Command(
                update={"error": f"No content for tool '{tool_name}'"}, goto=goto_node
            )

        # Parse the content
        try:
            if isinstance(tool_class, type) and issubclass(tool_class, BaseModel):
                parsed_result = self._parse_tool_content(content, tool_class)
            else:
                logger.warning(
                    f"[bold yellow]Tool is not a Pydantic model:[/bold yellow] {type(tool_class)}"
                )
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

            logger.info(f"[bold green]✓ Successfully parsed tool response[/bold green]")
            logger.debug(f"  Field name: {field_name}")
            logger.debug(f"  Result type: {type(parsed_result).__name__}")

            # Create update
            update_dict = {field_name: parsed_result}

            # Log the update for debugging
            if isinstance(parsed_result, BaseModel):
                logger.debug(
                    f"  Parsed model fields: {list(parsed_result.model_fields.keys())}"
                )

            logger.info(
                f"[bold green]=== Parser completed successfully ===[/bold green]"
            )
            return Command(update=update_dict, goto=goto_node)

        except Exception as e:
            logger.exception(f"[bold red]Failed to parse tool response:[/bold red] {e}")
            return Command(
                update={"error": f"Parse error for '{tool_name}': {str(e)}"},
                goto=goto_node,
            )
