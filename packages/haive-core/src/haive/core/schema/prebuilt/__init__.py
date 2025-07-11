"""Prebuilt state schemas for common agent patterns.

This module provides ready-to-use state schemas for various agent architectures:

- BasicAgentState: Simple agent state with messages and context
- MessagesState: Conversation management with LangChain integration
- ToolState: Extended MessagesState with tool management
- MultiAgentStateSchema: State for multi-agent architectures
- MessagesStateWithTokenUsage: MessagesState with token tracking

The messages submodule provides additional functionality:
- TokenUsage: Token tracking and cost calculation
- TokenUsageMixin: Mixin for adding token tracking to any schema
- Enhanced message utilities (if available)
"""

from haive.core.schema.multi_agent_state_schema import MultiAgentStateSchema

# from haive.core.schema.prebuilt.basic_agent_state import BasicAgentState
from haive.core.schema.prebuilt.llm_state import LLMState

# Import messages module components
from haive.core.schema.prebuilt.messages import (
    MessagesStateWithTokenUsage,
    TokenUsage,
    TokenUsageMixin,
    aggregate_token_usage,
    calculate_token_cost,
    extract_token_usage_from_message,
)
from haive.core.schema.prebuilt.messages_state import MessagesState
from haive.core.schema.prebuilt.multi_agent_state import MultiAgentState
from haive.core.schema.prebuilt.tool_state import ToolState

# Convenient aliases
TokenAwareState = MessagesStateWithTokenUsage  # Shorter name
TokenToolState = ToolState  # Makes it clear it has token tracking
AgentState = LLMState  # Generic agent state with single engine

__all__ = [
    # Core prebuilt schemas
    # "BasicAgentState",
    "MessagesState",
    "ToolState",
    "MultiAgentStateSchema",
    "MultiAgentState",
    "LLMState",
    # Token usage components
    "TokenUsage",
    "TokenUsageMixin",
    "MessagesStateWithTokenUsage",
    # Token usage utilities
    "extract_token_usage_from_message",
    "aggregate_token_usage",
    "calculate_token_cost",
    # Aliases
    "TokenAwareState",
    "TokenToolState",
    "AgentState",
]
