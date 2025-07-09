"""Dynamic Tool Selector implementing LangGraph-style tool management patterns.

This module implements sophisticated tool selection and management patterns
inspired by LangGraph's many-tools approach, providing dynamic tool binding,
context-aware selection, and intelligent tool routing.

Key Features:
- Dynamic tool selection and binding like LangGraph
- Context-aware tool recommendation
- Intelligent tool routing and management
- State-aware tool selection
- Tool usage learning and optimization
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Protocol, Tuple, Union

from haive.core.common.mixins.tool_route_mixin import ToolRouteMixin
from haive.core.registry import (
    ComponentMetadata,
    ComponentType,
    EnhancedComponentRegistry,
    create_component_registry,
)
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, ToolMessage
from langchain_core.tools import BaseTool, StructuredTool
from pydantic import BaseModel, Field, model_validator

from haive.agents.discovery.semantic_discovery import (
    QueryAnalysis,
    SemanticDiscoveryEngine,
    ToolSelectionStrategy,
)

logger = logging.getLogger(__name__)


class SelectionMode(str, Enum):
    """Tool selection modes."""

    STATIC = "static"  # Pre-selected fixed tools
    DYNAMIC = "dynamic"  # Select tools per query
    ADAPTIVE = "adaptive"  # Learn optimal tools over time
    CONTEXTUAL = "contextual"  # Context-aware selection
    ITERATIVE = "iterative"  # Iterative refinement


class ToolBindingStrategy(str, Enum):
    """Strategies for binding tools to LLM."""

    REPLACE_ALL = "replace_all"  # Replace all existing tools
    APPEND = "append"  # Add to existing tools
    MERGE = "merge"  # Intelligently merge with existing
    SELECTIVE = "selective"  # Selectively replace specific tools


class ToolSelectionResult(BaseModel):
    """Result of tool selection process."""

    selected_tools: List[BaseTool] = Field(default_factory=list)
    selection_metadata: Dict[str, Any] = Field(default_factory=dict)
    query_analysis: Optional[QueryAnalysis] = None
    selection_confidence: float = Field(default=0.0)
    fallback_used: bool = Field(default=False)
    selection_time_ms: float = Field(default=0.0)


class ToolUsageStats(BaseModel):
    """Statistics for tool usage and performance."""

    tool_name: str
    usage_count: int = 0
    success_count: int = 0
    avg_execution_time: float = 0.0
    error_count: int = 0
    contexts_used: List[str] = Field(default_factory=list)
    last_used: Optional[str] = None


class ContextAwareState(BaseModel):
    """State information for context-aware tool selection."""

    current_query: str = ""
    conversation_history: List[BaseMessage] = Field(default_factory=list)
    previous_tools_used: List[str] = Field(default_factory=list)
    current_context: Dict[str, Any] = Field(default_factory=dict)
    user_preferences: Dict[str, Any] = Field(default_factory=dict)
    session_metadata: Dict[str, Any] = Field(default_factory=dict)


class ToolSelectionStrategy(Protocol):
    """Protocol for tool selection strategies."""

    async def select_tools(
        self,
        query: str,
        available_tools: List[ComponentMetadata],
        context: ContextAwareState,
        max_tools: int = 5,
    ) -> ToolSelectionResult:
        """Select tools based on strategy."""
        ...


class DynamicToolSelector(BaseModel, ToolRouteMixin):
    """Dynamic tool selector implementing LangGraph-style patterns.

    This class provides sophisticated tool selection capabilities that adapt
    to query content, context, and usage patterns, similar to LangGraph's
    approach to handling many tools.
    """

    # Core configuration
    selection_mode: SelectionMode = Field(default=SelectionMode.DYNAMIC)
    binding_strategy: ToolBindingStrategy = Field(default=ToolBindingStrategy.MERGE)
    max_tools_per_query: int = Field(
        default=5, description="Maximum tools to select per query"
    )
    min_confidence_threshold: float = Field(
        default=0.6, description="Minimum confidence for tool selection"
    )

    # Discovery and selection components
    semantic_discovery: Optional[SemanticDiscoveryEngine] = Field(
        default=None, exclude=True
    )
    selection_strategies: Dict[str, ToolSelectionStrategy] = Field(
        default_factory=dict, exclude=True
    )

    # State and learning
    usage_stats: Dict[str, ToolUsageStats] = Field(default_factory=dict)
    context_state: ContextAwareState = Field(default_factory=ContextAwareState)
    learning_enabled: bool = Field(default=True)

    # Caching and performance
    tool_cache: Dict[str, List[BaseTool]] = Field(default_factory=dict, exclude=True)
    cache_ttl_seconds: float = Field(default=300.0)  # 5 minutes

    @model_validator(mode="after")
    def setup_selector(self) -> "DynamicToolSelector":
        """Setup the tool selector with default components."""
        # Initialize semantic discovery if not provided
        if not self.semantic_discovery:
            from haive.agents.discovery.semantic_discovery import (
                create_semantic_discovery,
            )

            self.semantic_discovery = create_semantic_discovery()

        # Setup default selection strategies
        if not self.selection_strategies:
            self._setup_default_strategies()

        return self

    def _setup_default_strategies(self) -> None:
        """Setup default tool selection strategies."""
        from .selection_strategies import (
            AdaptiveSelectionStrategy,
            CapabilityBasedStrategy,
            ContextualSelectionStrategy,
            SemanticSelectionStrategy,
        )

        self.selection_strategies = {
            "semantic": SemanticSelectionStrategy(),
            "capability": CapabilityBasedStrategy(),
            "adaptive": AdaptiveSelectionStrategy(),
            "contextual": ContextualSelectionStrategy(),
        }

    async def select_tools_for_query(
        self,
        query: str,
        available_tools: Optional[List[BaseTool]] = None,
        context: Optional[Dict[str, Any]] = None,
        force_refresh: bool = False,
    ) -> ToolSelectionResult:
        """Select optimal tools for a given query using LangGraph-style selection.

        This is the main entry point for tool selection, implementing the
        LangGraph pattern of dynamically selecting relevant tools based on
        query content and context.
        """
        start_time = asyncio.get_event_loop().time()

        try:
            # Update context state
            await self._update_context_state(query, context or {})

            # Check cache first (unless force refresh)
            cache_key = self._generate_cache_key(query, context)
            if not force_refresh and cache_key in self.tool_cache:
                cached_tools = self.tool_cache[cache_key]
                return ToolSelectionResult(
                    selected_tools=cached_tools,
                    selection_metadata={"cache_hit": True},
                    selection_confidence=0.9,  # High confidence for cached results
                    selection_time_ms=(asyncio.get_event_loop().time() - start_time)
                    * 1000,
                )

            # Discover available components if needed
            if not available_tools:
                await self.semantic_discovery.discover_and_index_components()

            # Select strategy based on mode
            strategy = self._select_strategy()

            # Get component metadata for selection
            components = await self._get_available_components()

            # Perform tool selection
            selection_result = await strategy.select_tools(
                query=query,
                available_tools=components,
                context=self.context_state,
                max_tools=self.max_tools_per_query,
            )

            # Convert ComponentMetadata to actual tools
            tools = await self._convert_to_tools(selection_result.selected_tools)

            # Update result
            selection_result.selected_tools = tools
            selection_result.selection_time_ms = (
                asyncio.get_event_loop().time() - start_time
            ) * 1000

            # Cache result
            if selection_result.selection_confidence >= self.min_confidence_threshold:
                self.tool_cache[cache_key] = tools

            # Update usage statistics if learning enabled
            if self.learning_enabled:
                await self._update_usage_stats(query, tools, context)

            logger.info(
                f"Selected {len(tools)} tools for query in {selection_result.selection_time_ms:.2f}ms"
            )
            return selection_result

        except Exception as e:
            logger.error(f"Error selecting tools for query: {e}")
            return ToolSelectionResult(
                selected_tools=[],
                selection_metadata={"error": str(e)},
                fallback_used=True,
                selection_time_ms=(asyncio.get_event_loop().time() - start_time) * 1000,
            )

    async def bind_tools_to_llm(
        self,
        llm_instance: Any,
        selected_tools: List[BaseTool],
        strategy: ToolBindingStrategy = None,
    ) -> Any:
        """Bind selected tools to LLM instance using specified strategy.

        This implements the LangGraph pattern of dynamically binding tools
        to the language model based on the current query context.
        """
        binding_strategy = strategy or self.binding_strategy

        try:
            if binding_strategy == ToolBindingStrategy.REPLACE_ALL:
                # Replace all existing tools
                return llm_instance.bind_tools(selected_tools)

            elif binding_strategy == ToolBindingStrategy.APPEND:
                # Add to existing tools
                existing_tools = getattr(llm_instance, "bound_tools", [])
                all_tools = existing_tools + selected_tools
                return llm_instance.bind_tools(all_tools)

            elif binding_strategy == ToolBindingStrategy.MERGE:
                # Intelligently merge tools
                merged_tools = await self._merge_tools_intelligently(
                    getattr(llm_instance, "bound_tools", []), selected_tools
                )
                return llm_instance.bind_tools(merged_tools)

            elif binding_strategy == ToolBindingStrategy.SELECTIVE:
                # Selectively replace specific tools
                updated_tools = await self._selective_tool_replacement(
                    getattr(llm_instance, "bound_tools", []), selected_tools
                )
                return llm_instance.bind_tools(updated_tools)

            else:
                # Default to replace all
                return llm_instance.bind_tools(selected_tools)

        except Exception as e:
            logger.error(f"Error binding tools to LLM: {e}")
            # Fallback to simple binding
            return llm_instance.bind_tools(selected_tools)

    async def iterative_tool_refinement(
        self,
        initial_query: str,
        llm_response: str,
        execution_results: Dict[str, Any],
        max_iterations: int = 3,
    ) -> ToolSelectionResult:
        """Iteratively refine tool selection based on execution feedback.

        This implements an advanced pattern where tool selection is refined
        based on the results of previous tool executions, similar to
        LangGraph's iterative approaches.
        """
        current_query = initial_query
        iteration = 0
        best_result = None

        while iteration < max_iterations:
            logger.info(f"Tool refinement iteration {iteration + 1}")

            # Analyze previous results to refine query
            if iteration > 0:
                current_query = await self._refine_query_from_feedback(
                    initial_query, execution_results
                )

            # Select tools with updated context
            result = await self.select_tools_for_query(
                current_query,
                context={
                    "iteration": iteration,
                    "previous_results": execution_results,
                    "refinement_mode": True,
                },
            )

            # Evaluate selection quality
            quality_score = await self._evaluate_selection_quality(
                result, execution_results
            )

            if not best_result or quality_score > best_result.selection_confidence:
                best_result = result
                best_result.selection_confidence = quality_score

            # Check if we've reached good enough quality
            if quality_score >= 0.9:
                logger.info(
                    f"High quality selection achieved in iteration {iteration + 1}"
                )
                break

            iteration += 1

        return best_result or ToolSelectionResult()

    async def analyze_tool_performance(self) -> Dict[str, Any]:
        """Analyze tool performance and provide insights."""
        if not self.usage_stats:
            return {"message": "No usage statistics available"}

        analysis = {
            "total_tools_tracked": len(self.usage_stats),
            "most_used_tools": [],
            "highest_success_rate": [],
            "fastest_tools": [],
            "recommendations": [],
        }

        # Sort tools by different metrics
        tools_by_usage = sorted(
            self.usage_stats.items(), key=lambda x: x[1].usage_count, reverse=True
        )

        tools_by_success = sorted(
            self.usage_stats.items(),
            key=lambda x: x[1].success_count / max(x[1].usage_count, 1),
            reverse=True,
        )

        tools_by_speed = sorted(
            self.usage_stats.items(), key=lambda x: x[1].avg_execution_time
        )

        # Populate analysis
        analysis["most_used_tools"] = [
            {"name": name, "usage_count": stats.usage_count}
            for name, stats in tools_by_usage[:5]
        ]

        analysis["highest_success_rate"] = [
            {
                "name": name,
                "success_rate": stats.success_count / max(stats.usage_count, 1),
                "usage_count": stats.usage_count,
            }
            for name, stats in tools_by_success[:5]
            if stats.usage_count > 0
        ]

        analysis["fastest_tools"] = [
            {"name": name, "avg_time_ms": stats.avg_execution_time}
            for name, stats in tools_by_speed[:5]
            if stats.avg_execution_time > 0
        ]

        # Generate recommendations
        analysis["recommendations"] = await self._generate_tool_recommendations()

        return analysis

    # Private helper methods

    async def _update_context_state(self, query: str, context: Dict[str, Any]) -> None:
        """Update the context state with new information."""
        self.context_state.current_query = query

        # Update context
        self.context_state.current_context.update(context)

        # Add to conversation history if this is a new query
        if (
            not self.context_state.conversation_history
            or self.context_state.conversation_history[-1].content != query
        ):
            self.context_state.conversation_history.append(HumanMessage(content=query))

    def _generate_cache_key(self, query: str, context: Dict[str, Any]) -> str:
        """Generate cache key for tool selection."""
        import hashlib

        key_components = [
            query,
            str(sorted(context.items())),
            self.selection_mode.value,
            str(self.max_tools_per_query),
        ]

        key_string = "|".join(key_components)
        return hashlib.md5(key_string.encode()).hexdigest()

    def _select_strategy(self) -> ToolSelectionStrategy:
        """Select appropriate tool selection strategy."""
        if self.selection_mode == SelectionMode.STATIC:
            return self.selection_strategies.get(
                "semantic", self.selection_strategies["semantic"]
            )
        elif self.selection_mode == SelectionMode.DYNAMIC:
            return self.selection_strategies.get(
                "semantic", self.selection_strategies["semantic"]
            )
        elif self.selection_mode == SelectionMode.ADAPTIVE:
            return self.selection_strategies.get(
                "adaptive", self.selection_strategies["semantic"]
            )
        elif self.selection_mode == SelectionMode.CONTEXTUAL:
            return self.selection_strategies.get(
                "contextual", self.selection_strategies["semantic"]
            )
        else:
            return self.selection_strategies.get(
                "semantic", self.selection_strategies["semantic"]
            )

    async def _get_available_components(self) -> List[ComponentMetadata]:
        """Get available components from semantic discovery."""
        if not self.semantic_discovery:
            return []

        # Force discovery if cache is empty
        await self.semantic_discovery.discover_and_index_components()

        # Return all cached components
        return self.semantic_discovery._component_cache.get("all", [])

    async def _convert_to_tools(
        self, components: List[ComponentMetadata]
    ) -> List[BaseTool]:
        """Convert ComponentMetadata to actual BaseTool instances."""
        tools = []

        for component in components:
            try:
                # Try to create tool from component
                tool = await self._create_tool_from_component(component)
                if tool:
                    tools.append(tool)
            except Exception as e:
                logger.warning(
                    f"Could not create tool from component {component.name}: {e}"
                )

        return tools

    async def _create_tool_from_component(
        self, component: ComponentMetadata
    ) -> Optional[BaseTool]:
        """Create a BaseTool from ComponentMetadata."""
        try:
            # This would need to be implemented based on component type
            # For now, create a simple placeholder tool

            def placeholder_function(query: str) -> str:
                return f"Tool {component.name} executed with query: {query}"

            tool = StructuredTool.from_function(
                func=placeholder_function,
                name=component.name.replace(" ", "_").lower(),
                description=component.description or f"Tool for {component.name}",
            )

            return tool

        except Exception as e:
            logger.error(f"Error creating tool from component {component.name}: {e}")
            return None

    async def _merge_tools_intelligently(
        self, existing_tools: List[BaseTool], new_tools: List[BaseTool]
    ) -> List[BaseTool]:
        """Intelligently merge existing and new tools."""
        merged = {}

        # Add existing tools
        for tool in existing_tools:
            merged[tool.name] = tool

        # Add new tools (replacing duplicates)
        for tool in new_tools:
            merged[tool.name] = tool

        return list(merged.values())

    async def _selective_tool_replacement(
        self, existing_tools: List[BaseTool], new_tools: List[BaseTool]
    ) -> List[BaseTool]:
        """Selectively replace tools based on performance metrics."""
        tools_by_name = {tool.name: tool for tool in existing_tools}

        for new_tool in new_tools:
            # Replace if new tool is better or doesn't exist
            if new_tool.name not in tools_by_name:
                tools_by_name[new_tool.name] = new_tool
            else:
                # Check if new tool is better based on usage stats
                if await self._is_tool_better(new_tool, tools_by_name[new_tool.name]):
                    tools_by_name[new_tool.name] = new_tool

        return list(tools_by_name.values())

    async def _is_tool_better(
        self, new_tool: BaseTool, existing_tool: BaseTool
    ) -> bool:
        """Determine if new tool is better than existing tool."""
        new_stats = self.usage_stats.get(new_tool.name)
        existing_stats = self.usage_stats.get(existing_tool.name)

        if not new_stats or not existing_stats:
            return True  # Prefer new tool if no stats available

        new_success_rate = new_stats.success_count / max(new_stats.usage_count, 1)
        existing_success_rate = existing_stats.success_count / max(
            existing_stats.usage_count, 1
        )

        return new_success_rate > existing_success_rate

    async def _update_usage_stats(
        self, query: str, tools: List[BaseTool], context: Optional[Dict[str, Any]]
    ) -> None:
        """Update usage statistics for selected tools."""
        for tool in tools:
            if tool.name not in self.usage_stats:
                self.usage_stats[tool.name] = ToolUsageStats(tool_name=tool.name)

            stats = self.usage_stats[tool.name]
            stats.usage_count += 1

            # Extract context information
            if context:
                context_str = str(context.get("domain", "general"))
                if context_str not in stats.contexts_used:
                    stats.contexts_used.append(context_str)

    async def _refine_query_from_feedback(
        self, original_query: str, execution_results: Dict[str, Any]
    ) -> str:
        """Refine query based on execution feedback."""
        # Simple refinement - could be enhanced with ML
        if execution_results.get("errors"):
            return f"{original_query} (refined to avoid previous errors)"
        elif execution_results.get("incomplete"):
            return f"{original_query} (seeking more comprehensive results)"
        else:
            return original_query

    async def _evaluate_selection_quality(
        self, result: ToolSelectionResult, execution_results: Dict[str, Any]
    ) -> float:
        """Evaluate the quality of tool selection."""
        # Simple quality scoring - could be enhanced
        base_score = result.selection_confidence

        # Bonus for successful execution
        if execution_results.get("success_count", 0) > 0:
            base_score += 0.2

        # Penalty for errors
        if execution_results.get("error_count", 0) > 0:
            base_score -= 0.1

        return max(0.0, min(1.0, base_score))

    async def _generate_tool_recommendations(self) -> List[str]:
        """Generate recommendations for tool usage optimization."""
        recommendations = []

        # Find underused but successful tools
        for name, stats in self.usage_stats.items():
            if (
                stats.usage_count < 5
                and stats.success_count / max(stats.usage_count, 1) > 0.8
            ):
                recommendations.append(
                    f"Consider using '{name}' more often - high success rate but low usage"
                )

        # Find slow tools
        slow_tools = [
            name
            for name, stats in self.usage_stats.items()
            if stats.avg_execution_time > 5000  # 5 seconds
        ]
        if slow_tools:
            recommendations.append(f"These tools are slow: {', '.join(slow_tools[:3])}")

        # Find error-prone tools
        error_prone = [
            name
            for name, stats in self.usage_stats.items()
            if stats.error_count / max(stats.usage_count, 1) > 0.3
        ]
        if error_prone:
            recommendations.append(
                f"These tools have high error rates: {', '.join(error_prone[:3])}"
            )

        return recommendations


class LangGraphStyleSelector(DynamicToolSelector):
    """LangGraph-style tool selector with state-based selection.

    This class specifically implements the LangGraph pattern of using
    state to determine tool selection and binding.
    """

    async def select_tools_with_state(
        self, state: Dict[str, Any], available_tools: Optional[List[BaseTool]] = None
    ) -> ToolSelectionResult:
        """Select tools based on LangGraph-style state.

        This method implements the LangGraph pattern where tool selection
        is based on the current state of the conversation/workflow.
        """
        # Extract query from state
        messages = state.get("messages", [])
        if not messages:
            return ToolSelectionResult()

        last_message = messages[-1]
        query = getattr(last_message, "content", "")

        # Extract additional context from state
        context = {
            "state_keys": list(state.keys()),
            "message_count": len(messages),
            "workflow_stage": state.get("stage", "unknown"),
        }

        # Use standard selection with state context
        return await self.select_tools_for_query(query, available_tools, context)

    def create_tool_selection_node(self) -> Callable:
        """Create a node function for LangGraph that selects tools.

        This returns a function that can be used as a node in a LangGraph
        workflow for dynamic tool selection.
        """

        async def select_tools_node(state: Dict[str, Any]) -> Dict[str, Any]:
            """Node function that selects and binds tools based on state."""
            try:
                # Perform tool selection
                result = await self.select_tools_with_state(state)

                # Update state with selected tools
                return {
                    "selected_tools": [tool.name for tool in result.selected_tools],
                    "tool_selection_metadata": result.selection_metadata,
                    "tools": result.selected_tools,  # Actual tools for binding
                }

            except Exception as e:
                logger.error(f"Error in tool selection node: {e}")
                return {
                    "selected_tools": [],
                    "tool_selection_metadata": {"error": str(e)},
                    "tools": [],
                }

        return select_tools_node


class ContextAwareSelector(DynamicToolSelector):
    """Context-aware tool selector that considers conversation history."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.conversation_memory: List[Dict[str, Any]] = []

    async def select_with_conversation_context(
        self,
        query: str,
        conversation_history: List[BaseMessage],
        user_preferences: Optional[Dict[str, Any]] = None,
    ) -> ToolSelectionResult:
        """Select tools considering full conversation context."""

        # Analyze conversation patterns
        context = await self._analyze_conversation_patterns(conversation_history)

        # Add user preferences
        if user_preferences:
            context.update(user_preferences)

        # Extract tool usage patterns from history
        previous_tools = self._extract_previous_tool_usage(conversation_history)
        context["previous_tools"] = previous_tools

        # Perform context-aware selection
        return await self.select_tools_for_query(query, context=context)

    async def _analyze_conversation_patterns(
        self, history: List[BaseMessage]
    ) -> Dict[str, Any]:
        """Analyze conversation to extract useful patterns."""
        patterns = {
            "topic_consistency": 0.0,
            "complexity_trend": "stable",
            "tool_effectiveness": {},
            "user_satisfaction_signals": [],
        }

        # Simple pattern analysis - could be enhanced with NLP
        if len(history) > 1:
            # Analyze topic consistency
            topics = []
            for msg in history:
                if hasattr(msg, "content") and msg.content:
                    # Simple keyword extraction for topic analysis
                    words = msg.content.lower().split()
                    topics.extend([w for w in words if len(w) > 3])

            # Calculate topic consistency (simplified)
            if topics:
                unique_topics = set(topics)
                patterns["topic_consistency"] = 1.0 - (len(unique_topics) / len(topics))

        return patterns

    def _extract_previous_tool_usage(self, history: List[BaseMessage]) -> List[str]:
        """Extract tools that were used in conversation."""
        tools_used = []

        for msg in history:
            if isinstance(msg, ToolMessage):
                tool_name = getattr(msg, "name", None)
                if tool_name:
                    tools_used.append(tool_name)

        return tools_used


# Factory functions for easy creation


def create_dynamic_tool_selector(
    selection_mode: SelectionMode = SelectionMode.DYNAMIC,
    max_tools: int = 5,
    semantic_discovery: Optional[SemanticDiscoveryEngine] = None,
) -> DynamicToolSelector:
    """Create a dynamic tool selector with sensible defaults."""
    return DynamicToolSelector(
        selection_mode=selection_mode,
        max_tools_per_query=max_tools,
        semantic_discovery=semantic_discovery,
    )


def create_langgraph_style_selector(
    max_tools: int = 5, learning_enabled: bool = True
) -> LangGraphStyleSelector:
    """Create a LangGraph-style tool selector."""
    return LangGraphStyleSelector(
        selection_mode=SelectionMode.CONTEXTUAL,
        max_tools_per_query=max_tools,
        learning_enabled=learning_enabled,
    )


def create_context_aware_selector(
    max_tools: int = 5, min_confidence: float = 0.7
) -> ContextAwareSelector:
    """Create a context-aware tool selector."""
    return ContextAwareSelector(
        selection_mode=SelectionMode.CONTEXTUAL,
        max_tools_per_query=max_tools,
        min_confidence_threshold=min_confidence,
    )
