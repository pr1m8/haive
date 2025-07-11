"""
Validation Node Configuration V2 - Improved version that can update state.

This version addresses the key issues with the original validation node:
1. Can add ToolMessages to state (not just route)
2. Handles dynamic tool routes properly
3. Uses Command with Send objects for proper routing
4. Supports both Pydantic models and regular tools

Key improvements:
- Proper node implementation (not conditional edge)
- ToolMessage creation for Pydantic model validation
- Error handling with appropriate ToolMessages
- Dynamic routing based on actual tool calls
"""

import logging
from typing import Any, Dict, List, Optional, Sequence, Union

from langchain_core.messages import AIMessage, BaseMessage, ToolMessage
from langgraph.types import Command, Send
from pydantic import BaseModel, Field, ValidationError

from haive.core.graph.node.base_node_config import BaseNodeConfig
from haive.core.graph.node.types import CommandGoto, NodeType

logger = logging.getLogger(__name__)


class ValidationNodeConfigV2(BaseNodeConfig):
    """V2 Validation node that can update state and add ToolMessages.

    This node processes tool calls from AIMessages and:
    1. Validates Pydantic models and creates ToolMessages
    2. Routes regular tools to appropriate nodes
    3. Handles errors by creating error ToolMessages
    4. Updates state with new messages before routing

    Args:
        engine_name: Name of the engine to get tool routes from
        tool_node: Name of the tool execution node
        parser_node: Name of the parser node
        available_nodes: List of available nodes for routing
        pydantic_models: Dict of model name -> model class for validation
    """

    engine_name: str = Field(..., description="Engine name for tool routes")
    tool_node: str = Field(default="tool_node", description="Tool execution node name")
    parser_node: str = Field(default="parse_output", description="Parser node name")
    available_nodes: List[str] = Field(
        default_factory=list, description="Available nodes"
    )
    pydantic_models: Dict[str, type[BaseModel]] = Field(
        default_factory=dict, description="Pydantic models for validation"
    )
    node_type: NodeType = Field(default=NodeType.VALIDATION, description="Node type")

    def __call__(self, state: Dict[str, Any]) -> Command:
        """Process tool calls and update state with ToolMessages."""
        # Get messages from state
        messages = state.get("messages", [])
        if not messages:
            return Command(goto="END")

        last_message = messages[-1]

        # Check if last message is AIMessage with tool calls
        if not isinstance(last_message, AIMessage):
            return Command(goto="END")

        tool_calls = getattr(last_message, "tool_calls", [])
        if not tool_calls:
            return Command(goto="END")

        # Get tool routes from state or engine
        tool_routes = state.get("tool_routes", {})

        # Process each tool call
        new_messages = []
        destinations = set()

        for tool_call in tool_calls:
            tool_name = tool_call.get("name")
            tool_id = tool_call.get("id")
            args = tool_call.get("args", {})

            if not tool_name or not tool_id:
                continue

            # Get route for this tool
            route = tool_routes.get(tool_name, "unknown")

            if route == "pydantic_model":
                # Handle Pydantic model validation
                tool_msg = self._validate_pydantic_model(tool_name, tool_id, args)
                new_messages.append(tool_msg)

                # Route to parser if validation succeeded
                if "Successfully" in tool_msg.content:
                    destinations.add(self.parser_node)
                else:
                    destinations.add("END")

            elif route in ["langchain_tool", "function", "tool_node"]:
                # Route to tool node for execution
                destinations.add(self.tool_node)

            else:
                # Unknown tool - create error message
                tool_msg = ToolMessage(
                    content=f"Unknown tool: {tool_name}",
                    tool_call_id=tool_id,
                    name=tool_name,
                )
                new_messages.append(tool_msg)
                destinations.add("END")

        # Update state with new messages
        update_dict = {}
        if new_messages:
            update_dict["messages"] = new_messages

        # Determine where to go next
        goto = self._determine_destination(destinations)

        logger.info(
            f"ValidationV2: Created {len(new_messages)} ToolMessages, routing to {goto}"
        )

        return Command(update=update_dict, goto=goto)

    def _validate_pydantic_model(
        self, tool_name: str, tool_id: str, args: Dict[str, Any]
    ) -> ToolMessage:
        """Validate Pydantic model and create ToolMessage."""
        try:
            # Get model class
            model_class = self.pydantic_models.get(tool_name)

            if not model_class:
                # Try to dynamically find model class
                model_class = self._find_model_class(tool_name)

            if not model_class:
                return ToolMessage(
                    content=f"Unknown Pydantic model: {tool_name}",
                    tool_call_id=tool_id,
                    name=tool_name,
                )

            # Validate the model
            model_instance = model_class(**args)

            # Create success message with model data
            success_msg = (
                f"Successfully validated {tool_name}: {model_instance.model_dump()}"
            )

            return ToolMessage(
                content=success_msg, tool_call_id=tool_id, name=tool_name
            )

        except ValidationError as e:
            # Create error message
            error_msg = f"Validation error for {tool_name}: {str(e)}"
            return ToolMessage(content=error_msg, tool_call_id=tool_id, name=tool_name)
        except Exception as e:
            # Create generic error message
            error_msg = f"Error processing {tool_name}: {str(e)}"
            return ToolMessage(content=error_msg, tool_call_id=tool_id, name=tool_name)

    def _find_model_class(self, tool_name: str) -> Optional[type[BaseModel]]:
        """Try to find Pydantic model class by name."""
        # Common model names to try
        import sys

        # Look in current module globals
        if tool_name in globals():
            candidate = globals()[tool_name]
            if isinstance(candidate, type) and issubclass(candidate, BaseModel):
                return candidate

        # Try to import from common locations
        try:
            # Try importing from test modules
            from haive.agents.planning.p_and_e.models import (
                Act,
                Plan,
                PlanStep,
                Response,
            )

            models = {
                "Plan": Plan,
                "PlanStep": PlanStep,
                "Act": Act,
                "Response": Response,
            }
            if tool_name in models:
                return models[tool_name]
        except ImportError:
            pass

        return None

    def _determine_destination(self, destinations: set) -> str:
        """Determine where to route based on destinations."""
        if not destinations:
            return "END"

        destinations_list = list(destinations)

        if len(destinations_list) == 1:
            return destinations_list[0]

        # Multiple destinations - prioritize
        if self.tool_node in destinations_list:
            return self.tool_node
        elif self.parser_node in destinations_list:
            return self.parser_node
        else:
            return "END"
