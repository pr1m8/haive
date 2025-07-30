"""Tool selection strategies for dynamic tool selection.

This module implements various strategies for selecting tools based on different
criteria and approaches, providing flexibility in how tools are chosen for different
contexts and use cases.
"""

import logging
from abc import ABC, abstractmethod
from typing import Any

from haive.agents.discovery.dynamic_tool_selector import (
    ContextAwareState,
    ToolSelectionResult,
)
from haive.agents.discovery.semantic_discovery import (
    ComponentMetadata,
)

logger = logging.getLogger(__name__)


class BaseSelectionStrategy(ABC):
    """Base class for tool selection strategies."""

    @abstractmethod
    async def select_tools(
        self,
        query: str,
        available_tools: list[ComponentMetadata],
        context: ContextAwareState,
        max_tools: int = 5,
    ) -> ToolSelectionResult:
        """Select tools based on strategy."""


class SemanticSelectionStrategy(BaseSelectionStrategy):
    """Semantic similarity-based tool selection."""

    def __init__(self, similarity_threshold: float = 0.7):
        self.similarity_threshold = similarity_threshold

    async def select_tools(
        self,
        query: str,
        available_tools: list[ComponentMetadata],
        context: ContextAwareState,
        max_tools: int = 5,
    ) -> ToolSelectionResult:
        """Select tools based on semantic similarity to query."""
        # Simple key-based similarity for now
        # In a real implementation, this would use vector embeddings
        query_words = set(query.lower().split())

        scored_tools = []
        for tool in available_tools:
            # Calculate similarity score
            tool_words = set(
                (tool.description + " " + " ".join(tool.capabilities)).lower().split()
            )
            common_words = query_words.intersection(tool_words)
            similarity = len(common_words) / max(len(query_words), len(tool_words), 1)

            if similarity >= self.similarity_threshold:
                tool.similarity_score = similarity
                scored_tools.append(tool)

        # Sort by similarity and take top K
        scored_tools.sort(key=lambda t: t.similarity_score, reverse=True)
        selected = scored_tools[:max_tools]

        return ToolSelectionResult(
            selected_tools=selected,
            selection_metadata={
                "strategy": "semantic",
                "similarity_threshold": self.similarity_threshold,
                "total_candidates": len(available_tools),
            },
            selection_confidence=0.8 if selected else 0.0,
        )


class CapabilityBasedStrategy(BaseSelectionStrategy):
    """Capability-based tool selection."""

    def __init__(self, capability_weights: dict[str, float] | None = None):
        self.capability_weights = capability_weights or {}

    async def select_tools(
        self,
        query: str,
        available_tools: list[ComponentMetadata],
        context: ContextAwareState,
        max_tools: int = 5,
    ) -> ToolSelectionResult:
        """Select tools based on capability matching."""
        # Extract capabilities from query (simple key matching)
        required_capabilities = self._extract_capabilities_from_query(query)

        scored_tools = []
        for tool in available_tools:
            capability_score = self._calculate_capability_match(
                required_capabilities, tool.capabilities
            )

            if capability_score > 0:
                tool.capability_match_score = capability_score
                scored_tools.append(tool)

        # Sort by capability match and take top K
        scored_tools.sort(key=lambda t: t.capability_match_score, reverse=True)
        selected = scored_tools[:max_tools]

        return ToolSelectionResult(
            selected_tools=selected,
            selection_metadata={
                "strategy": "capability",
                "required_capabilities": required_capabilities,
                "total_candidates": len(available_tools),
            },
            selection_confidence=0.7 if selected else 0.0,
        )

    def _extract_capabilities_from_query(self, query: str) -> list[str]:
        """Extract required capabilities from query."""
        capability_keywords = {
            "search": ["search", "find", "lookup", "retrieve"],
            "analysis": ["analyze", "examine", "evaluate", "assess"],
            "generation": ["create", "generate", "build", "make"],
            "processing": ["process", "transform", "convert", "parse"],
            "communication": ["send", "message", "email", "notify"],
        }

        query_lower = query.lower()
        detected_capabilities = []

        for capability, keywords in capability_keywords.items():
            if any(key in query_lower for key in keywords):
                detected_capabilities.append(capability)

        return detected_capabilities

    def _calculate_capability_match(
        self, required: list[str], available: list[str]
    ) -> float:
        """Calculate capability match score."""
        if not required:
            return 1.0

        if not available:
            return 0.0

        matches = len(set(required).intersection(set(available)))
        return matches / len(required)


class AdaptiveSelectionStrategy(BaseSelectionStrategy):
    """Adaptive selection that learns from usage patterns."""

    def __init__(self, learning_rate: float = 0.1):
        self.learning_rate = learning_rate
        self.tool_performance: dict[str, float] = {}

    async def select_tools(
        self,
        query: str,
        available_tools: list[ComponentMetadata],
        context: ContextAwareState,
        max_tools: int = 5,
    ) -> ToolSelectionResult:
        """Select tools using adaptive learning."""
        # Combine semantic similarity with learned performance
        scored_tools = []
        for tool in available_tools:
            # Basic semantic score
            semantic_score = self._calculate_semantic_score(query, tool)

            # Learned performance score
            performance_score = self.tool_performance.get(tool.name, 0.5)

            # Combine scores
            combined_score = 0.6 * semantic_score + 0.4 * performance_score
            tool.composite_score = combined_score

            if combined_score > 0.3:  # Threshold for consideration
                scored_tools.append(tool)

        # Sort by combined score
        scored_tools.sort(key=lambda t: t.composite_score, reverse=True)
        selected = scored_tools[:max_tools]

        return ToolSelectionResult(
            selected_tools=selected,
            selection_metadata={
                "strategy": "adaptive",
                "learning_rate": self.learning_rate,
                "performance_data": len(self.tool_performance),
            },
            selection_confidence=0.9 if selected else 0.0,
        )

    def _calculate_semantic_score(self, query: str, tool: ComponentMetadata) -> float:
        """Calculate basic semantic similarity score."""
        query_words = set(query.lower().split())
        tool_text = (tool.description + " " + " ".join(tool.capabilities)).lower()
        tool_words = set(tool_text.split())

        common_words = query_words.intersection(tool_words)
        return len(common_words) / max(len(query_words), len(tool_words), 1)

    def update_performance(self, tool_name: str, success: bool) -> None:
        """Update tool performance based on execution results."""
        current_score = self.tool_performance.get(tool_name, 0.5)

        if success:
            new_score = current_score + self.learning_rate * (1.0 - current_score)
        else:
            new_score = current_score - self.learning_rate * current_score

        self.tool_performance[tool_name] = max(0.0, min(1.0, new_score))


class ContextualSelectionStrategy(BaseSelectionStrategy):
    """Context-aware tool selection considering conversation history."""

    def __init__(self, context_weight: float = 0.3):
        self.context_weight = context_weight

    async def select_tools(
        self,
        query: str,
        available_tools: list[ComponentMetadata],
        context: ContextAwareState,
        max_tools: int = 5,
    ) -> ToolSelectionResult:
        """Select tools considering full context."""
        scored_tools = []
        for tool in available_tools:
            # Base semantic score
            semantic_score = self._calculate_semantic_score(query, tool)

            # Context relevance score
            context_score = self._calculate_context_relevance(tool, context)

            # History-based score
            history_score = self._calculate_history_relevance(tool, context)

            # Combine scores
            combined_score = (
                0.5 * semantic_score + 0.3 * context_score + 0.2 * history_score
            )

            tool.composite_score = combined_score
            if combined_score > 0.2:
                scored_tools.append(tool)

        # Sort and select top tools
        scored_tools.sort(key=lambda t: t.composite_score, reverse=True)
        selected = scored_tools[:max_tools]

        return ToolSelectionResult(
            selected_tools=selected,
            selection_metadata={
                "strategy": "contextual",
                "context_keys": list(context.current_context.keys()),
                "history_length": len(context.conversation_history),
            },
            selection_confidence=0.85 if selected else 0.0,
        )

    def _calculate_semantic_score(self, query: str, tool: ComponentMetadata) -> float:
        """Calculate semantic similarity."""
        query_words = set(query.lower().split())
        tool_text = (tool.description + " " + " ".join(tool.capabilities)).lower()
        tool_words = set(tool_text.split())

        if not query_words or not tool_words:
            return 0.0

        common_words = query_words.intersection(tool_words)
        return len(common_words) / max(len(query_words), len(tool_words))

    def _calculate_context_relevance(
        self, tool: ComponentMetadata, context: ContextAwareState
    ) -> float:
        """Calculate how relevant tool is to current context."""
        relevance_score = 0.0

        # Check if tool capabilities match context requirements
        context_domain = context.current_context.get("domain", "")
        if context_domain and context_domain.lower() in [
            tag.lower() for tag in tool.tags
        ]:
            relevance_score += 0.5

        # Check user preferences
        preferred_tools = context.user_preferences.get("preferred_tools", [])
        if tool.name in preferred_tools:
            relevance_score += 0.3

        # Check session metadata
        session_type = context.session_metadata.get("type", "")
        if session_type and session_type in tool.capabilities:
            relevance_score += 0.2

        return min(1.0, relevance_score)

    def _calculate_history_relevance(
        self, tool: ComponentMetadata, context: ContextAwareState
    ) -> float:
        """Calculate tool relevance based on conversation history."""
        if not context.conversation_history:
            return 0.5  # Neutral score for no history

        # Check if tool was used recently and successfully
        recent_tools = context.previous_tools_used[-5:]  # Last 5 tools
        if tool.name in recent_tools:
            # Tool was used recently - slight preference
            return 0.7

        # Analyze conversation topics
        history_text = " ".join(
            [
                msg.content
                for msg in context.conversation_history
                if hasattr(msg, "content") and msg.content
            ]
        )

        # Simple topic relevance
        tool_keywords = tool.capabilities + tool.tags
        history_words = set(history_text.lower().split())
        tool_words = set(" ".join(tool_keywords).lower().split())

        common_words = history_words.intersection(tool_words)
        if tool_words:
            return len(common_words) / len(tool_words)

        return 0.5


class EnsembleSelectionStrategy(BaseSelectionStrategy):
    """Ensemble strategy combining multiple selection approaches."""

    def __init__(self, strategies: list[BaseSelectionStrategy] | None = None):
        self.strategies = strategies or [
            SemanticSelectionStrategy(),
            CapabilityBasedStrategy(),
            ContextualSelectionStrategy(),
        ]

        # Default weights for strategies
        self.strategy_weights = [0.4, 0.3, 0.3]

    async def select_tools(
        self,
        query: str,
        available_tools: list[ComponentMetadata],
        context: ContextAwareState,
        max_tools: int = 5,
    ) -> ToolSelectionResult:
        """Select tools using ensemble of strategies."""
        # Get results from all strategies
        strategy_results = []
        for strategy in self.strategies:
            try:
                result = await strategy.select_tools(
                    query, available_tools, context, max_tools * 2
                )
                strategy_results.append(result)
            except Exception as e:
                logger.warning(f"Strategy {type(strategy).__name__} failed: {e}")
                strategy_results.append(ToolSelectionResult())

        # Combine results using weighted voting
        tool_scores = {}
        total_confidence = 0.0

        for i, result in enumerate(strategy_results):
            weight = self.strategy_weights[i] if i < len(self.strategy_weights) else 0.1
            total_confidence += result.selection_confidence * weight

            for tool in result.selected_tools:
                if tool.name not in tool_scores:
                    tool_scores[tool.name] = {"tool": tool, "score": 0.0}

                # Add weighted score
                tool_score = (
                    getattr(tool, "similarity_score", 0.0)
                    or getattr(tool, "capability_match_score", 0.0)
                    or getattr(tool, "composite_score", 0.0)
                )

                tool_scores[tool.name]["score"] += weight * tool_score

        # Sort by ensemble score and select top tools
        ranked_tools = sorted(
            tool_scores.values(), key=lambda x: x["score"], reverse=True
        )

        selected_tools = [item["tool"] for item in ranked_tools[:max_tools]]

        return ToolSelectionResult(
            selected_tools=selected_tools,
            selection_metadata={
                "strategy": "ensemble",
                "num_strategies": len(self.strategies),
                "strategy_weights": self.strategy_weights,
            },
            selection_confidence=(
                total_confidence / len(self.strategies) if self.strategies else 0.0
            ),
        )


class LearningSelectionStrategy(BaseSelectionStrategy):
    """Selection strategy that learns from user feedback and tool performance."""

    def __init__(self) -> None:
        self.tool_ratings: dict[str, list[float]] = {}
        self.user_feedback: dict[str, list[dict[str, Any]]] = {}
        self.context_patterns: dict[str, list[str]] = {}

    async def select_tools(
        self,
        query: str,
        available_tools: list[ComponentMetadata],
        context: ContextAwareState,
        max_tools: int = 5,
    ) -> ToolSelectionResult:
        """Select tools using learned patterns and feedback."""
        scored_tools = []
        for tool in available_tools:
            # Calculate base compatibility score
            base_score = self._calculate_base_compatibility(query, tool)

            # Add learned performance score
            performance_score = self._get_learned_performance(tool.name)

            # Add context-based learning score
            context_score = self._get_context_learning_score(tool.name, context)

            # Combine scores
            final_score = (
                0.4 * base_score + 0.4 * performance_score + 0.2 * context_score
            )
            tool.composite_score = final_score

            if final_score > 0.3:
                scored_tools.append(tool)

        # Sort and select
        scored_tools.sort(key=lambda t: t.composite_score, reverse=True)
        selected = scored_tools[:max_tools]

        return ToolSelectionResult(
            selected_tools=selected,
            selection_metadata={
                "strategy": "learning",
                "learned_tools": len(self.tool_ratings),
                "feedback_entries": sum(
                    len(feedback) for feedback in self.user_feedback.values()
                ),
            },
            selection_confidence=0.9 if selected else 0.0,
        )

    def add_feedback(
        self, tool_name: str, rating: float, context: str, feedback_data: dict[str, Any]
    ) -> None:
        """Add user feedback for learning."""
        if tool_name not in self.tool_ratings:
            self.tool_ratings[tool_name] = []
            self.user_feedback[tool_name] = []

        self.tool_ratings[tool_name].append(rating)
        self.user_feedback[tool_name].append(feedback_data)

        # Store context patterns
        if context not in self.context_patterns:
            self.context_patterns[context] = []
        if tool_name not in self.context_patterns[context]:
            self.context_patterns[context].append(tool_name)

    def _calculate_base_compatibility(
        self, query: str, tool: ComponentMetadata
    ) -> float:
        """Calculate basic query-tool compatibility."""
        query_words = set(query.lower().split())
        tool_text = (tool.description + " " + " ".join(tool.capabilities)).lower()
        tool_words = set(tool_text.split())

        if not query_words or not tool_words:
            return 0.0

        return len(query_words.intersection(tool_words)) / len(
            query_words.union(tool_words)
        )

    def _get_learned_performance(self, tool_name: str) -> float:
        """Get learned performance score for tool."""
        if tool_name not in self.tool_ratings or not self.tool_ratings[tool_name]:
            return 0.5  # Neutral score for unknown tools

        ratings = self.tool_ratings[tool_name]
        return sum(ratings) / len(ratings)

    def _get_context_learning_score(
        self, tool_name: str, context: ContextAwareState
    ) -> float:
        """Get context-based learning score."""
        # Extract context key
        context_key = context.current_context.get("domain", "general")

        if context_key in self.context_patterns:
            successful_tools = self.context_patterns[context_key]
            if tool_name in successful_tools:
                return 0.8  # High score for tools successful in this context

        return 0.5  # Neutral score


# Factory function to create strategy instances
def create_selection_strategy(strategy_name: str, **kwargs) -> BaseSelectionStrategy:
    """Create a selection strategy by name."""
    strategies = {
        "semantic": SemanticSelectionStrategy,
        "capability": CapabilityBasedStrategy,
        "adaptive": AdaptiveSelectionStrategy,
        "contextual": ContextualSelectionStrategy,
        "ensemble": EnsembleSelectionStrategy,
        "learning": LearningSelectionStrategy,
    }

    if strategy_name not in strategies:
        raise ValueError(f"Unknown strategy: {strategy_name}")

    return strategies[strategy_name](**kwargs)
