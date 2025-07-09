"""Messages state module with token usage tracking and utilities.

This module provides enhanced message state functionality including:
- Token usage tracking and cost calculation
- Message round analysis and conversation tracking
- Tool call management and deduplication
- Message transformation utilities
"""

from haive.core.schema.prebuilt.messages.messages_with_token_usage import (
    MessagesStateWithTokenUsage,
)
from haive.core.schema.prebuilt.messages.token_usage import (
    TokenUsage,
    aggregate_token_usage,
    calculate_token_cost,
    extract_token_usage_from_message,
)
from haive.core.schema.prebuilt.messages.token_usage_mixin import TokenUsageMixin

# Import compatibility and utils if they exist
try:
    from haive.core.schema.prebuilt.messages.compatibility import MessagesStateAdapter
    from haive.core.schema.prebuilt.messages.utils import (
        MessageRound,
        ToolCallInfo,
        is_real_human_message,
        is_tool_error,
    )

    ENHANCED_FEATURES_AVAILABLE = True
except ImportError:
    ENHANCED_FEATURES_AVAILABLE = False

__all__ = [
    "TokenUsage",
    "extract_token_usage_from_message",
    "aggregate_token_usage",
    "calculate_token_cost",
    "TokenUsageMixin",
    "MessagesStateWithTokenUsage",
]

# Add enhanced features to exports if available
if ENHANCED_FEATURES_AVAILABLE:
    __all__.extend(
        [
            "MessagesStateAdapter",
            "MessageRound",
            "ToolCallInfo",
            "is_real_human_message",
            "is_tool_error",
        ]
    )
