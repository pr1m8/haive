"""
Tool node decorators.

These decorators create nodes that handle tool execution, following the
patterns described in langgraph-toolnode.md.
"""

import asyncio
import concurrent.futures
from typing import Any, Callable, Dict, List, Optional, Type, Union

from langgraph.types import Command, Send
from pydantic import BaseModel

from haive.core.graph.node.config import NodeConfig
from haive.core.graph.node.factory import NodeFactory
from haive.core.graph.node.protocols import AsyncNodeProtocol, NodeProtocol, State


def tool_node(
    tools: List[Any],
    command_goto: Optional[Union[str, Command, Send, List[Send]]] = None,
    name: Optional[str] = None,
    handle_errors: bool = True,
    parallel: bool = True,
    max_workers: int = 4,
    messages_key: str = "messages",
    preserve_schema: bool = True,
    auto_register: bool = True,
):
    """
    Create a tool node that executes tools from messages.
    
    Based on langgraph-toolnode.md implementation patterns.
    
    Args:
        tools: List of tools to execute
        command_goto: Where to go after tool execution
        name: Name for the node
        handle_errors: Whether to catch and handle tool errors
        parallel: Whether to execute tools in parallel
        max_workers: Maximum number of workers for parallel execution
        messages_key: Key in state containing messages
        preserve_schema: Whether to preserve StateSchema instances
        auto_register: Whether to automatically register the node
        
    Returns:
        A tool node function
    """
    node_name = name or "tool_node"
    
    # Create tool map
    tool_map = {tool.name: tool for tool in tools}
    
    def tool_node_function(state: State) -> Any:
        """Execute tools based on the last message in state."""
        # Get messages from state
        messages = _get_messages_from_state(state, messages_key)
        if not messages:
            # No messages, just pass through
            return Command(goto=command_goto) if command_goto else state
        
        # Get tool calls from last message
        last_message = messages[-1]
        tool_calls = _get_tool_calls_from_message(last_message)
        if not tool_calls:
            # No tool calls, just pass through
            return Command(goto=command_goto) if command_goto else state
        
        # Execute tools
        results = _execute_tools(
            tool_calls, 
            tool_map, 
            parallel=parallel, 
            max_workers=max_workers,
            handle_errors=handle_errors
        )
        
        # Create tool messages
        tool_messages = _create_tool_messages(results)
        
        # Add tool messages to state
        updated_state = _update_state_with_messages(state, messages, tool_messages, messages_key)
        
        # Return state with tool messages
        if command_goto:
            return Command(update=updated_state, goto=command_goto)
        return updated_state
    
    # Create node config
    config = NodeConfig(
        name=node_name,
        engine=tool_node_function,
        command_goto=command_goto,
        preserve_schema=preserve_schema,
    )
    
    # Create node function
    node_func = NodeFactory.create_node(config)
    
    # Auto-register if requested
    if auto_register:
        registry = NodeFactory.get_registry()
        registry.register_node(node_name, node_func)
    
    # Add metadata for introspection
    node_func.__tools__ = tools
    node_func.__tool_map__ = tool_map
    node_func.__node_config__ = config
    
    return node_func


def tools_condition(state: State, messages_key: str = "messages") -> str:
    """
    Condition function for routing based on tool calls.
    
    Args:
        state: Current state
        messages_key: Key in state containing messages
        
    Returns:
        "tools" if the last message has tool calls, "continue" otherwise
    """
    # Get messages from state
    messages = _get_messages_from_state(state, messages_key)
    if not messages:
        return "continue"
    
    # Check last message for tool calls
    last_message = messages[-1]
    tool_calls = _get_tool_calls_from_message(last_message)
    
    if tool_calls:
        return "tools"
    return "continue"


def create_tools_router(
    routes: Dict[str, str] = None,
    messages_key: str = "messages",
):
    """
    Create a routing function for tool execution.
    
    Args:
        routes: Routes to use (defaults to {"tools": "tool_node", "continue": "next_node"})
        messages_key: Key in state containing messages
        
    Returns:
        Routing function compatible with add_conditional_edges
    """
    routes = routes or {"tools": "tool_node", "continue": "next_node"}
    
    def router(state: State) -> str:
        result = tools_condition(state, messages_key)
        return routes.get(result, routes.get("continue"))
    
    return router


# Helper functions

def _get_messages_from_state(state: State, messages_key: str) -> List[Any]:
    """Extract messages from state."""
    if isinstance(state, dict) and messages_key in state:
        return state[messages_key]
    elif hasattr(state, messages_key):
        return getattr(state, messages_key)
    return []


def _get_tool_calls_from_message(message: Any) -> List[Dict[str, Any]]:
    """Extract tool calls from a message."""
    # Handle various message formats
    if hasattr(message, "tool_calls") and message.tool_calls:
        return message.tool_calls
    elif hasattr(message, "additional_kwargs") and message.additional_kwargs.get("tool_calls"):
        return message.additional_kwargs["tool_calls"]
    elif isinstance(message, dict) and message.get("tool_calls"):
        return message["tool_calls"]
    return []


def _execute_tools(
    tool_calls: List[Dict[str, Any]],
    tool_map: Dict[str, Any],
    parallel: bool = True,
    max_workers: int = 4,
    handle_errors: bool = True
) -> List[Dict[str, Any]]:
    """Execute tools in parallel or sequentially."""
    results = []
    
    if parallel and len(tool_calls) > 1:
        # Execute tools in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            for tool_call in tool_calls:
                if tool_call["name"] in tool_map:
                    tool = tool_map[tool_call["name"]]
                    futures.append(
                        executor.submit(
                            _execute_single_tool,
                            tool,
                            tool_call,
                            handle_errors
                        )
                    )
            
            # Gather results
            for future in concurrent.futures.as_completed(futures):
                results.append(future.result())
    else:
        # Execute tools sequentially
        for tool_call in tool_calls:
            if tool_call["name"] in tool_map:
                tool = tool_map[tool_call["name"]]
                result = _execute_single_tool(tool, tool_call, handle_errors)
                results.append(result)
    
    return results


def _execute_single_tool(tool: Any, tool_call: Dict[str, Any], handle_errors: bool) -> Dict[str, Any]:
    """Execute a single tool."""
    tool_name = tool_call["name"]
    tool_args = tool_call.get("args", {})
    
    try:
        # Try to execute the tool
        result = tool(**tool_args)
        
        # Return successful result
        return {
            "name": tool_name,
            "args": tool_args,
            "result": result,
            "status": "success"
        }
    except Exception as e:
        if handle_errors:
            # Return error result
            return {
                "name": tool_name,
                "args": tool_args,
                "error": str(e),
                "status": "error"
            }
        # Re-raise if not handling errors
        raise


def _create_tool_messages(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Create tool messages from execution results."""
    messages = []
    
    for result in results:
        if result["status"] == "success":
            # Create success message
            message = {
                "type": "tool",
                "tool_name": result["name"],
                "tool_args": result["args"],
                "content": str(result["result"]),
            }
        else:
            # Create error message
            message = {
                "type": "tool",
                "tool_name": result["name"],
                "tool_args": result["args"],
                "content": f"Error: {result['error']}",
                "error": True,
            }
        
        messages.append(message)
    
    return messages


def _update_state_with_messages(
    state: State,
    current_messages: List[Any],
    new_messages: List[Any],
    messages_key: str
) -> Any:
    """Update state with new messages."""
    # Handle different state types
    if isinstance(state, dict):
        # Dict state
        updated_state = state.copy()
        updated_state[messages_key] = current_messages + new_messages
        return updated_state
    elif hasattr(state, messages_key) and hasattr(state, "model_copy"):
        # Pydantic v2 BaseModel or StateSchema
        updated_state = state.model_copy()
        setattr(updated_state, messages_key, current_messages + new_messages)
        return updated_state
    elif hasattr(state, messages_key) and hasattr(state, "copy"):
        # Pydantic v1 BaseModel
        updated_state = state.copy()
        setattr(updated_state, messages_key, current_messages + new_messages)
        return updated_state
    
    # Fallback: return state with message dict
    return {messages_key: current_messages + new_messages}