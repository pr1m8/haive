# src/haive/core/graph/node/tool_node_config.py

import logging
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Type, Union

from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.tools import BaseTool, BaseToolkit, StructuredTool, Tool
from langgraph.prebuilt import ToolNode
from langgraph.types import Command
from pydantic import BaseModel, Field

from haive.core.graph.node.base_config import NodeConfig
from haive.core.graph.node.types import NodeType

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ToolNodeConfig(NodeConfig):
    """
    Configuration for a tool node in a graph.

    Tool nodes execute LangChain tools and handle tool calls from LLM messages.
    Uses tools directly from the associated engine in state.
    """

    # Override node_type from base class
    node_type: NodeType = Field(default=NodeType.TOOL, description="The type of node")

    # Tool-specific fields
    tags: Optional[List[str]] = Field(
        default=None, description="Optional tags for the tool node"
    )
    handle_tool_errors: Union[
        bool, str, Callable[..., str], Tuple[Type[Exception], ...]
    ] = Field(default=True, description="How to handle tool errors")
    messages_key: str = Field(
        default="messages", description="The key to use for the messages field"
    )

    # Engine reference for getting tools from state
    engine_name: Optional[str] = Field(
        default=None, description="Name of engine in state.engines dict"
    )

    # Tool filtering - which routes should this node handle
    allowed_routes: List[str] = Field(
        default_factory=lambda: ["langchain_tool", "function", "tool_node"],
        description="Tool routes this node should handle",
    )

    def _get_engine_from_state(self, state: Dict[str, Any]) -> Optional[Any]:
        """Get engine from state.engines dict."""
        logger.debug(f"Looking for engine '{self.engine_name}' in state")

        if not self.engine_name:
            logger.warning("No engine name configured")
            return None

        # Try to get from engines dict in state
        engines_dict = state.get("engines", {})

        if not engines_dict:
            logger.error("No engines dict found in state")
            return None

        if not isinstance(engines_dict, dict):
            logger.error(f"state.engines is not a dict: {type(engines_dict)}")
            return None

        logger.debug(f"Available engines in state: {list(engines_dict.keys())}")

        if self.engine_name in engines_dict:
            engine = engines_dict[self.engine_name]
            if engine:
                logger.info(f"✅ Found engine '{self.engine_name}' in state.engines")
                return engine
            else:
                logger.error(f"Engine '{self.engine_name}' exists in state but is None")
        else:
            logger.error(f"Engine '{self.engine_name}' not found in state.engines")
            logger.error(f"Available engines: {list(engines_dict.keys())}")

        return None

    def __call__(
        self, state: Dict[str, Any], config: Optional[Dict[str, Any]] = None
    ) -> Command:
        """
        Execute the tool node with the given state and configuration.

        Gets tools from engine in state.engines dict.

        Args:
            state: The current state of the graph
            config: Optional runtime configuration

        Returns:
            A Command with state update including tool execution results
        """
        logger.info("=" * 60)
        logger.info(f"TOOL NODE EXECUTION: {self.name}")
        logger.info("=" * 60)

        # Get current messages
        messages = state.get(self.messages_key, [])
        logger.debug(f"Current message count: {len(messages)}")

        # Check if we have tool calls to process
        if not messages:
            logger.warning("No messages in state")
            return Command(update={}, goto=self.command_goto)

        last_message = messages[-1]
        if not isinstance(last_message, AIMessage):
            logger.warning("Last message is not an AIMessage")
            return Command(update={}, goto=self.command_goto)

        if not hasattr(last_message, "tool_calls") or not last_message.tool_calls:
            logger.warning("No tool calls in last message")
            return Command(update={}, goto=self.command_goto)

        logger.info(f"Found {len(last_message.tool_calls)} tool calls to process")

        # Get engine from state
        engine = self._get_engine_from_state(state)
        if not engine:
            logger.error(f"Could not get engine '{self.engine_name}' from state")
            return Command(update={}, goto=self.command_goto)

        # Get tools from engine
        logger.debug("Collecting tools from engine...")
        engine_tools = []

        if hasattr(engine, "tools") and engine.tools:
            engine_tools.extend(engine.tools)
            logger.debug(f"Found {len(engine.tools)} tools in engine.tools")

        if hasattr(engine, "schemas") and engine.schemas:
            engine_tools.extend(engine.schemas)
            logger.debug(f"Found {len(engine.schemas)} schemas in engine.schemas")

        if hasattr(engine, "pydantic_tools") and engine.pydantic_tools:
            engine_tools.extend(engine.pydantic_tools)
            logger.debug(f"Found {len(engine.pydantic_tools)} pydantic_tools")

        if not engine_tools:
            logger.warning("No tools found in engine")
            return Command(update={}, goto=self.command_goto)

        logger.debug(f"Total tools collected: {len(engine_tools)}")

        # Get tool routes from engine (not state)
        tool_routes = {}
        if hasattr(engine, "tool_routes") and engine.tool_routes:
            tool_routes = engine.tool_routes
            logger.debug(f"Found tool_routes in engine: {tool_routes}")
        else:
            logger.debug("No tool_routes found in engine")

        # Filter tools by allowed routes
        filtered_tools = []
        for tool in engine_tools:
            tool_name = getattr(tool, "name", getattr(tool, "__name__", str(tool)))
            route = tool_routes.get(
                tool_name, "langchain_tool"
            )  # Default to langchain_tool

            logger.debug(f"Tool '{tool_name}' has route '{route}'")

            if route in self.allowed_routes:
                filtered_tools.append(tool)
                logger.info(f"✅ Including tool '{tool_name}' (route: {route})")
            else:
                logger.debug(
                    f"❌ Excluding tool '{tool_name}' (route: {route} not in allowed routes: {self.allowed_routes})"
                )

        if not filtered_tools:
            logger.warning("No tools available for tool node after filtering")
            logger.warning(f"Allowed routes: {self.allowed_routes}")
            logger.warning(f"Tool routes found: {list(tool_routes.values())}")
            return Command(update={}, goto=self.command_goto)

        logger.info(
            f"Tool node using {len(filtered_tools)} tools from engine '{self.engine_name}'"
        )

        # Log tool names
        for tool in filtered_tools:
            tool_name = getattr(tool, "name", getattr(tool, "__name__", str(tool)))
            logger.debug(f"  - {tool_name}")

        # Create the tool node with filtered tools
        logger.debug("Creating ToolNode...")
        tool_node = ToolNode(
            tools=filtered_tools,
            name=self.name,
            tags=self.tags,
            handle_tool_errors=self.handle_tool_errors,
            messages_key=self.messages_key,
        )

        # Execute the tool node
        logger.info("Executing tool node...")
        try:
            # ToolNode.invoke returns a dict with messages that include ToolMessages
            result = tool_node.invoke(state, config)
            logger.info("✅ Tool node execution completed")

            # The result should have the messages key with tool messages added
            if isinstance(result, dict) and self.messages_key in result:
                updated_messages = result[self.messages_key]
                logger.info(
                    f"Tool node added {len(updated_messages) - len(messages)} ToolMessages"
                )

                # Count ToolMessages added
                tool_msg_count = 0
                for msg in updated_messages[len(messages) :]:
                    if isinstance(msg, ToolMessage):
                        tool_msg_count += 1
                        logger.debug(
                            f"ToolMessage: {msg.name} - {str(msg.content)[:100]}..."
                        )

                logger.info(f"✅ Added {tool_msg_count} ToolMessages to state")

                # Return the full result which includes the updated messages
                return Command(update=result, goto=self.command_goto)
            else:
                logger.error(f"Unexpected result format from ToolNode: {type(result)}")
                logger.error(f"Result: {result}")

                # Manually create ToolMessages if needed
                logger.warning("Creating ToolMessages manually...")
                new_messages = list(messages)

                for tool_call in last_message.tool_calls:
                    # Find the tool
                    tool_name = (
                        tool_call["name"]
                        if isinstance(tool_call, dict)
                        else tool_call.name
                    )
                    tool_id = (
                        tool_call.get("id", f"call_{tool_name}")
                        if isinstance(tool_call, dict)
                        else tool_call.id
                    )

                    # Create error message since ToolNode didn't work properly
                    tool_msg = ToolMessage(
                        content="Tool execution failed - unexpected result format",
                        name=tool_name,
                        tool_call_id=tool_id,
                    )
                    new_messages.append(tool_msg)
                    logger.debug(f"Added error ToolMessage for {tool_name}")

                return Command(
                    update={self.messages_key: new_messages}, goto=self.command_goto
                )

        except Exception as e:
            logger.error(f"Error executing tool node: {e}")
            logger.exception(e)

            # Create error ToolMessages for each tool call
            new_messages = list(messages)

            for tool_call in last_message.tool_calls:
                tool_name = (
                    tool_call["name"] if isinstance(tool_call, dict) else tool_call.name
                )
                tool_id = (
                    tool_call.get("id", f"call_{tool_name}")
                    if isinstance(tool_call, dict)
                    else tool_call.id
                )

                tool_msg = ToolMessage(
                    content=f"Tool execution error: {str(e)}",
                    name=tool_name,
                    tool_call_id=tool_id,
                )
                new_messages.append(tool_msg)
                logger.debug(f"Added error ToolMessage for {tool_name}")

            return Command(
                update={self.messages_key: new_messages}, goto=self.command_goto
            )

    @classmethod
    def from_route_filter(cls, allowed_routes: List[str], engine_name: str, **kwargs):
        """
        Create a tool node configuration for specific routes.

        Args:
            allowed_routes: List of tool routes this node should handle
            engine_name: Name of engine in state.engines dict
            **kwargs: Additional configuration parameters

        Returns:
            Configured ToolNodeConfig
        """
        return cls(allowed_routes=allowed_routes, engine_name=engine_name, **kwargs)
