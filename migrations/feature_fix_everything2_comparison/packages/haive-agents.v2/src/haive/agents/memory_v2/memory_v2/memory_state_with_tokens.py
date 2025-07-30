"""Memory state with integrated token tracking and summarization hooks.

This module extends MessagesStateWithTokenUsage to add memory-specific
functionality with pre-hooks for summarization and token management.
"""

import logging
from datetime import datetime
from typing import Any

from haive.core.schema.prebuilt.messages.messages_with_token_usage import (
    MessagesStateWithTokenUsage,
)
from langchain_core.messages import AnyMessage
from pydantic import ConfigDict, Field, computed_field

from .memory_state_original import (
    MemoryStats,
    UnifiedMemoryEntry,
)

logger = logging.getLogger(__name__)

# Graph transformer imports
try:
    from haive.agents.document_modifiers.kg.kg_map_merge.models import (
        EntityNode,
        EntityRelationship,
        KnowledgeGraph,
    )

    GRAPH_AVAILABLE = True
except ImportError:
    logger.warning("Graph transformer components not available")
    GRAPH_AVAILABLE = False

    # Create stub classes
    class EntityNode:
        pass

    class EntityRelationship:
        pass

    class KnowledgeGraph:
        pass


logger = logging.getLogger(__name__)


class MemoryStateWithTokens(MessagesStateWithTokenUsage):
    """MessagesState with memory and token-aware summarization hooks.

    This state combines:
    - MessagesStateWithTokenUsage (automatic token tracking)
    - Memory management (current memories, retrieved memories)
    - Pre-hook system for summarization triggers
    - Token threshold monitoring with branching logic

    Features:
    - Automatic token tracking from parent class
    - Memory storage and retrieval tracking
    - Pre-execution hooks that check token thresholds
    - Summarization triggers when thresholds are exceeded
    - Running summary maintenance
    - Branch decision logic for token management

    Example:
        >>> state = MemoryStateWithTokens()
        >>> state.add_message(user_message)
        >>>
        >>> # Pre-hook automatically checks tokens
        >>> if state.should_trigger_summarization():
        >>>     state.prepare_for_summarization()
        >>>
        >>> # Branch logic for routing
        >>> route = state.get_memory_route()  # "process", "summarize", "rewrite"
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    # Memory tracking using original models
    current_memories: list[UnifiedMemoryEntry] = Field(
        default_factory=list, description="Current memories in working set"
    )

    retrieved_memories: list[UnifiedMemoryEntry] = Field(
        default_factory=list, description="Recently retrieved memories"
    )

    memory_metadata: dict[str, Any] = Field(
        default_factory=dict, description="Memory operation metadata"
    )

    memory_stats: MemoryStats = Field(
        default_factory=MemoryStats, description="Memory usage statistics"
    )

    # Token management for memory
    memory_token_usage: dict[str, int] = Field(
        default_factory=dict, description="Token usage breakdown for memory operations"
    )

    # Summarization state
    running_summary: str | None = Field(
        default=None, description="Current running summary of conversation"
    )

    summarized_message_ids: list[str] = Field(
        default_factory=list, description="IDs of messages that have been summarized"
    )

    last_summarization: dict[str, Any] | None = Field(
        default=None, description="Details of last summarization operation"
    )

    # Thresholds for decision making
    warning_threshold: float = Field(
        default=0.7, description="Token warning threshold (0.0-1.0)"
    )

    critical_threshold: float = Field(
        default=0.85, description="Token critical threshold (0.0-1.0)"
    )

    max_context_tokens: int = Field(
        default=8000, description="Maximum context window tokens"
    )

    # Graph transformation state
    knowledge_graph: KnowledgeGraph | None = Field(
        default=None,
        description="Current knowledge graph extracted from memories and conversations",
    )

    graph_nodes: list[EntityNode] = Field(
        default_factory=list, description="Extracted entity nodes from content"
    )

    graph_relationships: list[EntityRelationship] = Field(
        default_factory=list, description="Extracted relationships between entities"
    )

    graph_generation_enabled: bool = Field(
        default=True, description="Whether to automatically generate knowledge graphs"
    )

    last_graph_update: dict[str, Any] | None = Field(
        default=None, description="Details of last graph transformation operation"
    )

    # ========================================================================
    # COMPUTED PROPERTIES
    # ========================================================================

    @computed_field
    @property
    def total_memory_tokens(self) -> int:
        """Calculate total tokens used by memories."""
        total = 0

        # Count tokens in current memories
        for memory in self.current_memories:
            # Estimate ~4 characters per token
            total += len(memory.content) // 4

        # Count tokens in running summary
        if self.running_summary:
            total += len(self.running_summary) // 4

        return total

    @computed_field
    @property
    def estimated_total_tokens(self) -> int:
        """Estimate total tokens for messages + memories."""
        message_tokens = self.get_token_usage_summary().get("total_tokens", 0)
        return message_tokens + self.total_memory_tokens

    @computed_field
    @property
    def token_usage_ratio(self) -> float:
        """Calculate current token usage as ratio of max."""
        if self.max_context_tokens <= 0:
            return 0.0
        return self.estimated_total_tokens / self.max_context_tokens

    @computed_field
    @property
    def token_status(self) -> str:
        """Get current token status."""
        ratio = self.token_usage_ratio

        if ratio >= self.critical_threshold:
            return "CRITICAL"
        if ratio >= self.warning_threshold:
            return "WARNING"
        return "OK"

    # ========================================================================
    # PRE-HOOK SYSTEM
    # ========================================================================

    def pre_message_hook(self, message: AnyMessage) -> dict[str, Any]:
        """Pre-hook executed before adding any message.

        This hook:
        1. Checks current token usage
        2. Determines if summarization is needed
        3. Prepares summarization data if required
        4. Returns decision for routing

        Args:
            message: Message about to be added

        Returns:
            Dict with hook results and routing decisions
        """
        logger.debug(f"Pre-message hook: current tokens={self.estimated_total_tokens}")

        # Estimate tokens for incoming message
        incoming_tokens = len(str(message)) // 4  # Rough estimate
        projected_total = self.estimated_total_tokens + incoming_tokens
        projected_ratio = projected_total / self.max_context_tokens

        hook_result = {
            "current_tokens": self.estimated_total_tokens,
            "incoming_tokens": incoming_tokens,
            "projected_total": projected_total,
            "projected_ratio": projected_ratio,
            "current_status": self.token_status,
            "action_needed": False,
            "recommended_route": "process",  # Default route
        }

        # Check if action is needed
        if projected_ratio >= self.critical_threshold:
            hook_result.update(
                {
                    "action_needed": True,
                    "recommended_route": "summarize_critical",
                    "reason": f"Projected ratio {projected_ratio:.2%} >= critical threshold {self.critical_threshold:.2%}",
                }
            )
            logger.info(
                "Pre-hook: Critical threshold reached, recommending summarization"
            )

        elif projected_ratio >= self.warning_threshold:
            hook_result.update(
                {
                    "action_needed": True,
                    "recommended_route": "summarize_warning",
                    "reason": f"Projected ratio {projected_ratio:.2%} >= warning threshold {self.warning_threshold:.2%}",
                }
            )
            logger.info(
                "Pre-hook: Warning threshold reached, recommending memory consolidation"
            )

        return hook_result

    def should_trigger_summarization(self) -> bool:
        """Check if summarization should be triggered."""
        return self.token_usage_ratio >= self.warning_threshold

    def prepare_for_summarization(self) -> dict[str, Any]:
        """Prepare state for summarization operation.

        This method:
        1. Identifies messages/memories to summarize
        2. Preserves recent important content
        3. Calculates target compression ratios
        4. Prepares summarization context

        Returns:
            Dict with summarization preparation data
        """
        # Find messages not yet summarized
        unsummarized_messages = [
            msg
            for msg in self.messages
            if hasattr(msg, "id") and msg.id not in self.summarized_message_ids
        ]

        # Split into summarizable and preserve
        preserve_count = min(5, len(unsummarized_messages))  # Keep last 5
        to_summarize = (
            unsummarized_messages[:-preserve_count]
            if preserve_count > 0
            else unsummarized_messages
        )
        to_preserve = (
            unsummarized_messages[-preserve_count:] if preserve_count > 0 else []
        )

        # Prepare memories for summarization
        old_memories = (
            self.current_memories[:-10] if len(self.current_memories) > 10 else []
        )
        recent_memories = (
            self.current_memories[-10:]
            if len(self.current_memories) > 10
            else self.current_memories
        )

        # Calculate current token usage
        messages_tokens = sum(len(str(msg)) // 4 for msg in to_summarize)
        memories_tokens = sum(len(mem.content) // 4 for mem in old_memories)
        total_to_summarize = messages_tokens + memories_tokens

        # Target: compress to 30% of original
        target_tokens = int(total_to_summarize * 0.3)

        prep_data = {
            "messages_to_summarize": to_summarize,
            "messages_to_preserve": to_preserve,
            "memories_to_summarize": old_memories,
            "memories_to_preserve": recent_memories,
            "current_tokens": total_to_summarize,
            "target_tokens": target_tokens,
            "compression_ratio": 0.3,
            "has_existing_summary": self.running_summary is not None,
            "existing_summary": self.running_summary,
            "preparation_timestamp": datetime.now().isoformat(),
        }

        logger.info(
            f"Summarization prep: {len(to_summarize)} messages, {len(old_memories)} memories, "
            f"{total_to_summarize} → {target_tokens} tokens"
        )

        return prep_data

    def get_memory_route(self) -> str:
        """Determine routing decision based on current state.

        Returns:
            Route name for graph branching logic
        """
        status = self.token_status
        ratio = self.token_usage_ratio

        # Emergency: immediate aggressive action needed
        if ratio >= 0.95:
            return "emergency_compress"

        # Critical: summarization required
        if status == "CRITICAL":
            return "summarize"

        # Warning: consider consolidation or graph transformation
        if status == "WARNING":
            if len(self.current_memories) > 20:
                return "consolidate_memories"
            if self.running_summary is None:
                return "create_summary"
            if self.graph_generation_enabled and not self.knowledge_graph:
                return "transform_to_graph"
            return "update_summary"

        # Normal processing with optional graph updates
        if (
            self.graph_generation_enabled
            and len(self.current_memories) > 5
            and len(self.messages) > 3
            and (
                not self.last_graph_update
                or len(self.current_memories)
                - self.last_graph_update.get("memory_count", 0)
                > 5
            )
        ):
            return "update_graph"
        return "process"

    # ========================================================================
    # SUMMARIZATION INTEGRATION
    # ========================================================================

    def add_message_with_hooks(self, message: AnyMessage) -> dict[str, Any]:
        """Add message with pre-hook processing.

        This method:
        1. Runs pre-message hook
        2. Adds the message normally
        3. Updates token tracking
        4. Returns hook results for routing decisions

        Args:
            message: Message to add

        Returns:
            Hook results for routing decisions
        """
        # Run pre-hook
        hook_result = self.pre_message_hook(message)

        # Add message normally (triggers token tracking)
        self.add_message(message)

        # Update memory token tracking
        self.memory_token_usage[f"message_{len(self.messages)}"] = hook_result[
            "incoming_tokens"
        ]

        # Update stats
        self.memory_stats.total_operations += 1

        return hook_result

    def apply_summarization_result(
        self,
        summary: str,
        summarized_message_ids: list[str],
        summarized_memory_ids: list[str],
    ) -> None:
        """Apply results of summarization operation.

        Args:
            summary: Generated summary text
            summarized_message_ids: IDs of messages that were summarized
            summarized_memory_ids: IDs of memories that were summarized
        """
        # Update running summary
        if self.running_summary:
            # Combine with existing summary
            self.running_summary = (
                f"{self.running_summary}\n\n--- Recent Summary ---\n{summary}"
            )
        else:
            self.running_summary = summary

        # Track summarized messages
        self.summarized_message_ids.extend(summarized_message_ids)

        # Remove summarized memories from current set
        self.current_memories = [
            mem for mem in self.current_memories if mem.id not in summarized_memory_ids
        ]

        # Create summary memory entry
        if summary:
            summary_memory = MemoryEntry(
                id=f"summary_{datetime.now().timestamp()}",
                content=summary,
                metadata=MemoryMetadata(
                    memory_type="meta",
                    importance="high",
                    source="summarization",
                    tags=["summary", "compressed"],
                    confidence=0.9,
                ),
            )
            self.current_memories.insert(0, summary_memory)

        # Record summarization details
        self.last_summarization = {
            "timestamp": datetime.now().isoformat(),
            "messages_summarized": len(summarized_message_ids),
            "memories_summarized": len(summarized_memory_ids),
            "summary_length": len(summary),
            "new_running_summary_length": (
                len(self.running_summary) if self.running_summary else 0
            ),
        }

        logger.info(
            f"Applied summarization: {len(summarized_message_ids)} messages, "
            f"{len(summarized_memory_ids)} memories → {len(summary)} char summary"
        )

    # ========================================================================
    # UTILITY METHODS
    # ========================================================================

    def get_comprehensive_status(self) -> dict[str, Any]:
        """Get comprehensive state status for debugging/monitoring."""
        token_summary = self.get_token_usage_summary()

        return {
            # Basic info
            "total_messages": len(self.messages),
            "total_memories": len(self.current_memories),
            "retrieved_memories": len(self.retrieved_memories),
            # Token info
            "message_tokens": token_summary.get("total_tokens", 0),
            "memory_tokens": self.total_memory_tokens,
            "estimated_total_tokens": self.estimated_total_tokens,
            "max_context_tokens": self.max_context_tokens,
            "token_usage_ratio": self.token_usage_ratio,
            "token_status": self.token_status,
            # Summarization info
            "has_running_summary": self.running_summary is not None,
            "running_summary_length": (
                len(self.running_summary) if self.running_summary else 0
            ),
            "summarized_messages": len(self.summarized_message_ids),
            "last_summarization": self.last_summarization,
            # Routing
            "recommended_route": self.get_memory_route(),
            "needs_action": self.should_trigger_summarization(),
            # Timestamps
            "status_timestamp": datetime.now().isoformat(),
        }

    def reset_for_new_session(self) -> None:
        """Reset state for new conversation session."""
        # Keep running summary and core memories
        core_memories = [
            mem
            for mem in self.current_memories
            if mem.metadata.memory_type in ["semantic", "meta"]
            and mem.metadata.importance == "high"
        ]

        # Clear transient state
        self.current_memories = core_memories
        self.retrieved_memories.clear()
        self.memory_metadata.clear()
        self.memory_token_usage.clear()

        # Reset token tracking (from parent)
        self.reset_token_usage()

        # Keep summarization state
        # (running_summary and summarized_message_ids remain)

        logger.info(
            f"Reset for new session: kept {len(core_memories)} core memories and running summary"
        )
