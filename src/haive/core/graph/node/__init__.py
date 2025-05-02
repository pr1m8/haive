"""
Node system with simplified schema integration.

This module provides a streamlined node system for creating graph workflows
with strong typing, proper Command/Send usage, and StateSchema integration.
"""

from haive.core.graph.node.config import NodeConfig
from haive.core.graph.node.factory import NodeFactory
from haive.core.graph.node.protocols import NodeProtocol, AsyncNodeProtocol, NodeReturn, State
from haive.core.graph.node.registry import NodeRegistry

# Re-export all decorators
from haive.core.graph.node.decorators import (
    # Base decorators
    node,
    async_node,
    
    # Engine decorators
    engine_node,
    llm_node,
    retriever_node,
    
    # Specialized decorators
    validation_node,
    retry_node,
    interruptible_node,
    interrupt,
    NodeInterrupt,
    
    # Tool decorators
    tool_node,
    tools_condition,
    create_tools_router,
)

# Re-export types for convenience
from langgraph.types import Command, Send

__all__ = [
    # Core classes
    "NodeConfig",
    "NodeFactory",
    "NodeRegistry",
    
    # Protocols
    "NodeProtocol",
    "AsyncNodeProtocol",
    "NodeReturn",
    "State",
    
    # LangGraph types
    "Command",
    "Send",
    
    # Base decorators
    "node",
    "async_node",
    
    # Engine decorators
    "engine_node",
    "llm_node",
    "retriever_node",
    
    # Specialized decorators
    "validation_node",
    "retry_node",
    "interruptible_node",
    "interrupt",
    "NodeInterrupt",
    
    # Tool decorators
    "tool_node",
    "tools_condition",
    "create_tools_router",
]