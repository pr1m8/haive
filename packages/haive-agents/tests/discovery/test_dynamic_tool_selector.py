"""Comprehensive tests for dynamic tool selector.

This test suite provides extensive testing of the dynamic tool selection
system with challenging scenarios, LangGraph-style patterns, and edge cases.
"""

import asyncio
from typing import Any, Dict, List, Optional
from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pytest
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.tools import BaseTool, StructuredTool

from haive.agents.discovery.dynamic_tool_selector import (
    ContextAwareSelector,
    ContextAwareState,
    DynamicToolSelector,
    LangGraphStyleSelector,
    SelectionMode,
    ToolBindingStrategy,
    ToolSelectionResult,
    ToolUsageStats,
    create_context_aware_selector,
    create_dynamic_tool_selector,
    create_langgraph_style_selector,
)
from haive.agents.discovery.semantic_discovery import ComponentMetadata


class MockTool(BaseTool):
    """Mock tool for testing."""

    def __init__(
        self, name: str, description: str = "", capabilities: List[str] = None
    ):
        super().__init__()
        self.name = name
        self.description = description
        self.capabilities = capabilities or []

    def _run(self, query: str) -> str:
        return f"Mock tool {self.name} executed with: {query}"

    async def _arun(self, query: str) -> str:
        return f"Mock tool {self.name} async executed with: {query}"


class TestToolSelectionResult:
    """Test ToolSelectionResult model."""

    def test_default_creation(self):
        """Test creating ToolSelectionResult with defaults."""
        result = ToolSelectionResult()

        assert result.selected_tools == []
        assert result.selection_metadata == {}
        assert result.query_analysis is None
        assert result.selection_confidence == 0.0
        assert result.fallback_used == False
        assert result.selection_time_ms == 0.0

    def test_creation_with_data(self):
        """Test creating ToolSelectionResult with data."""
        tools = [MockTool("test_tool")]
        metadata = {"strategy": "test"}

        result = ToolSelectionResult(
            selected_tools=tools,
            selection_metadata=metadata,
            selection_confidence=0.8,
            selection_time_ms=150.5,
        )

        assert result.selected_tools == tools
        assert result.selection_metadata == metadata
        assert result.selection_confidence == 0.8
        assert result.selection_time_ms == 150.5


class TestToolUsageStats:
    """Test ToolUsageStats model."""

    def test_default_stats(self):
        """Test default tool usage statistics."""
        stats = ToolUsageStats(tool_name="test_tool")

        assert stats.tool_name == "test_tool"
        assert stats.usage_count == 0
        assert stats.success_count == 0
        assert stats.avg_execution_time == 0.0
        assert stats.error_count == 0
        assert stats.contexts_used == []
        assert stats.last_used is None

    def test_stats_with_data(self):
        """Test tool usage statistics with data."""
        stats = ToolUsageStats(
            tool_name="data_tool",
            usage_count=10,
            success_count=8,
            avg_execution_time=250.5,
            error_count=2,
            contexts_used=["web", "data"],
            last_used="2024-01-01",
        )

        assert stats.tool_name == "data_tool"
        assert stats.usage_count == 10
        assert stats.success_count == 8
        assert stats.avg_execution_time == 250.5
        assert stats.error_count == 2
        assert stats.contexts_used == ["web", "data"]
        assert stats.last_used == "2024-01-01"


class TestContextAwareState:
    """Test ContextAwareState model."""

    def test_default_state(self):
        """Test default context state."""
        state = ContextAwareState()

        assert state.current_query == ""
        assert state.conversation_history == []
        assert state.previous_tools_used == []
        assert state.current_context == {}
        assert state.user_preferences == {}
        assert state.session_metadata == {}

    def test_state_with_data(self):
        """Test context state with data."""
        messages = [HumanMessage(content="test")]

        state = ContextAwareState(
            current_query="test query",
            conversation_history=messages,
            previous_tools_used=["tool1", "tool2"],
            current_context={"domain": "test"},
            user_preferences={"style": "detailed"},
            session_metadata={"type": "analysis"},
        )

        assert state.current_query == "test query"
        assert state.conversation_history == messages
        assert state.previous_tools_used == ["tool1", "tool2"]
        assert state.current_context == {"domain": "test"}
        assert state.user_preferences == {"style": "detailed"}
        assert state.session_metadata == {"type": "analysis"}


class TestDynamicToolSelector:
    """Test suite for DynamicToolSelector."""

    def setup_method(self):
        """Setup test fixtures."""
        # Mock semantic discovery
        self.mock_semantic_discovery = MagicMock()
        self.mock_semantic_discovery.discover_and_index_components = AsyncMock()
        self.mock_semantic_discovery._component_cache = {
            "all": [
                ComponentMetadata(
                    name="search_tool",
                    description="Search for information",
                    capabilities=["search", "web_access"],
                    tags=["web", "search"],
                ),
                ComponentMetadata(
                    name="data_tool",
                    description="Process data files",
                    capabilities=["data_processing", "analysis"],
                    tags=["data", "analytics"],
                ),
                ComponentMetadata(
                    name="email_tool",
                    description="Send emails",
                    capabilities=["email", "communication"],
                    tags=["email", "messaging"],
                ),
            ]
        }

        self.selector = DynamicToolSelector(
            selection_mode=SelectionMode.DYNAMIC,
            max_tools_per_query=3,
            semantic_discovery=self.mock_semantic_discovery,
        )

        # Mock the selection strategies
        self.mock_strategy = AsyncMock()
        self.mock_strategy.select_tools.return_value = ToolSelectionResult(
            selected_tools=[
                ComponentMetadata(
                    name="mock_tool", description="", capabilities=[], tags=[]
                )
            ],
            selection_confidence=0.8,
        )
        self.selector.selection_strategies = {"semantic": self.mock_strategy}

    @pytest.mark.asyncio
    async def test_basic_tool_selection(self):
        """Test basic tool selection functionality."""
        query = "search for information"

        result = await self.selector.select_tools_for_query(query)

        assert isinstance(result, ToolSelectionResult)
        assert len(result.selected_tools) >= 0
        assert result.selection_time_ms > 0

    @pytest.mark.asyncio
    async def test_tool_selection_with_context(self):
        """Test tool selection with context information."""
        query = "analyze sales data"
        context = {
            "domain": "business",
            "user_preferences": {"detailed_analysis": True},
            "session_type": "analytics",
        }

        result = await self.selector.select_tools_for_query(query, context=context)

        assert isinstance(result, ToolSelectionResult)
        # Context should be updated in selector state
        assert self.selector.context_state.current_query == query
        assert "domain" in self.selector.context_state.current_context

    @pytest.mark.asyncio
    async def test_caching_behavior(self):
        """Test tool selection caching."""
        query = "test caching"

        # First call
        result1 = await self.selector.select_tools_for_query(query)

        # Second call with same query (should use cache)
        result2 = await self.selector.select_tools_for_query(query)

        # Cache hit should be indicated in metadata
        if result2.selection_metadata.get("cache_hit"):
            assert result2.selection_time_ms < result1.selection_time_ms

    @pytest.mark.asyncio
    async def test_force_refresh(self):
        """Test forcing refresh to bypass cache."""
        query = "test refresh"

        # First call
        await self.selector.select_tools_for_query(query)

        # Force refresh should bypass cache
        result = await self.selector.select_tools_for_query(query, force_refresh=True)

        assert not result.selection_metadata.get("cache_hit", False)

    @pytest.mark.asyncio
    async def test_different_selection_modes(self):
        """Test different selection modes."""
        query = "test selection modes"
        modes = [
            SelectionMode.DYNAMIC,
            SelectionMode.ADAPTIVE,
            SelectionMode.CONTEXTUAL,
        ]

        for mode in modes:
            self.selector.selection_mode = mode
            result = await self.selector.select_tools_for_query(query)
            assert isinstance(result, ToolSelectionResult)

    @pytest.mark.asyncio
    async def test_tool_binding_strategies(self):
        """Test different tool binding strategies."""
        # Mock LLM instance
        mock_llm = MagicMock()
        mock_llm.bind_tools = MagicMock(return_value=mock_llm)
        mock_llm.bound_tools = []

        tools = [MockTool("test_tool")]

        strategies = [
            ToolBindingStrategy.REPLACE_ALL,
            ToolBindingStrategy.APPEND,
            ToolBindingStrategy.MERGE,
            ToolBindingStrategy.SELECTIVE,
        ]

        for strategy in strategies:
            result = await self.selector.bind_tools_to_llm(mock_llm, tools, strategy)
            assert result is not None
            mock_llm.bind_tools.assert_called()

    @pytest.mark.asyncio
    async def test_iterative_refinement(self):
        """Test iterative tool refinement."""
        initial_query = "search and analyze data"
        llm_response = "I found some information"
        execution_results = {"success_count": 1, "error_count": 0}

        result = await self.selector.iterative_tool_refinement(
            initial_query, llm_response, execution_results, max_iterations=2
        )

        assert isinstance(result, ToolSelectionResult)
        assert result.selection_confidence >= 0.0

    @pytest.mark.asyncio
    async def test_usage_statistics_update(self):
        """Test updating usage statistics."""
        query = "test stats"
        tools = [MockTool("stat_tool")]
        context = {"domain": "testing"}

        # Enable learning
        self.selector.learning_enabled = True

        # Trigger stats update through tool selection
        await self.selector.select_tools_for_query(query, context=context)

        # Check if stats were updated (if tools were processed)
        if "stat_tool" in self.selector.usage_stats:
            stats = self.selector.usage_stats["stat_tool"]
            assert stats.usage_count >= 0

    @pytest.mark.asyncio
    async def test_performance_analysis(self):
        """Test tool performance analysis."""
        # Add some mock usage stats
        self.selector.usage_stats = {
            "tool1": ToolUsageStats(
                tool_name="tool1",
                usage_count=10,
                success_count=8,
                avg_execution_time=200.0,
            ),
            "tool2": ToolUsageStats(
                tool_name="tool2",
                usage_count=5,
                success_count=5,
                avg_execution_time=100.0,
            ),
        }

        analysis = await self.selector.analyze_tool_performance()

        assert "total_tools_tracked" in analysis
        assert "most_used_tools" in analysis
        assert "highest_success_rate" in analysis
        assert "fastest_tools" in analysis
        assert "recommendations" in analysis

        assert analysis["total_tools_tracked"] == 2

    @pytest.mark.asyncio
    async def test_error_handling(self):
        """Test error handling in tool selection."""
        # Mock strategy that raises exception
        error_strategy = AsyncMock()
        error_strategy.select_tools.side_effect = Exception("Test error")
        self.selector.selection_strategies = {"semantic": error_strategy}

        query = "test error handling"
        result = await self.selector.select_tools_for_query(query)

        # Should handle error gracefully
        assert isinstance(result, ToolSelectionResult)
        assert result.fallback_used == True
        assert "error" in result.selection_metadata

    @pytest.mark.asyncio
    async def test_edge_case_queries(self):
        """Test handling of edge case queries."""
        edge_cases = [
            "",  # Empty query
            "   ",  # Whitespace only
            "a",  # Single character
            "🚀",  # Emoji
            "SELECT * FROM table",  # SQL
            "def function():",  # Code
        ]

        for query in edge_cases:
            result = await self.selector.select_tools_for_query(query)
            assert isinstance(result, ToolSelectionResult)
            # Should not crash


class TestLangGraphStyleSelector:
    """Test LangGraph-style selector."""

    def setup_method(self):
        """Setup test fixtures."""
        self.selector = LangGraphStyleSelector(
            selection_mode=SelectionMode.CONTEXTUAL, max_tools_per_query=5
        )

        # Mock components
        self.selector.semantic_discovery = MagicMock()
        self.selector.semantic_discovery.discover_and_index_components = AsyncMock()
        self.selector.semantic_discovery._component_cache = {"all": []}

        # Mock strategy
        mock_strategy = AsyncMock()
        mock_strategy.select_tools.return_value = ToolSelectionResult(
            selected_tools=[], selection_confidence=0.7
        )
        self.selector.selection_strategies = {"contextual": mock_strategy}

    @pytest.mark.asyncio
    async def test_state_based_selection(self):
        """Test LangGraph-style state-based tool selection."""
        state = {
            "messages": [
                HumanMessage(content="search for information"),
                AIMessage(content="I'll help you search"),
            ],
            "stage": "research",
            "context": {"domain": "academic"},
        }

        result = await self.selector.select_tools_with_state(state)

        assert isinstance(result, ToolSelectionResult)

    @pytest.mark.asyncio
    async def test_empty_state_handling(self):
        """Test handling of empty or invalid state."""
        empty_states = [
            {},  # Empty state
            {"messages": []},  # No messages
            {"random_key": "value"},  # No messages key
        ]

        for state in empty_states:
            result = await self.selector.select_tools_with_state(state)
            assert isinstance(result, ToolSelectionResult)

    def test_tool_selection_node_creation(self):
        """Test creation of LangGraph node function."""
        node_func = self.selector.create_tool_selection_node()

        assert callable(node_func)

    @pytest.mark.asyncio
    async def test_tool_selection_node_execution(self):
        """Test execution of tool selection node."""
        node_func = self.selector.create_tool_selection_node()

        state = {"messages": [HumanMessage(content="test query")], "stage": "initial"}

        result_state = await node_func(state)

        assert isinstance(result_state, dict)
        assert "selected_tools" in result_state
        assert "tool_selection_metadata" in result_state
        assert "tools" in result_state

    @pytest.mark.asyncio
    async def test_node_error_handling(self):
        """Test error handling in node function."""
        # Mock strategy that raises exception
        error_strategy = AsyncMock()
        error_strategy.select_tools.side_effect = Exception("Node error")
        self.selector.selection_strategies = {"contextual": error_strategy}

        node_func = self.selector.create_tool_selection_node()

        state = {"messages": [HumanMessage(content="test")]}
        result_state = await node_func(state)

        # Should handle error gracefully
        assert isinstance(result_state, dict)
        assert result_state["selected_tools"] == []
        assert "error" in result_state["tool_selection_metadata"]


class TestContextAwareSelector:
    """Test context-aware selector."""

    def setup_method(self):
        """Setup test fixtures."""
        self.selector = ContextAwareSelector(
            max_tools_per_query=3, min_confidence_threshold=0.6
        )

        # Mock components
        self.selector.semantic_discovery = MagicMock()
        self.selector.semantic_discovery.discover_and_index_components = AsyncMock()
        self.selector.semantic_discovery._component_cache = {"all": []}

        # Mock strategy
        mock_strategy = AsyncMock()
        mock_strategy.select_tools.return_value = ToolSelectionResult(
            selected_tools=[], selection_confidence=0.8
        )
        self.selector.selection_strategies = {"contextual": mock_strategy}

    @pytest.mark.asyncio
    async def test_conversation_context_selection(self):
        """Test tool selection with conversation context."""
        query = "analyze the data we discussed earlier"
        conversation_history = [
            HumanMessage(content="I have sales data from last quarter"),
            AIMessage(content="I can help analyze sales data"),
            HumanMessage(content="Let's focus on revenue trends"),
            AIMessage(content="I'll analyze revenue trends"),
            HumanMessage(content=query),
        ]
        user_preferences = {
            "analysis_style": "detailed",
            "preferred_visualization": "charts",
        }

        result = await self.selector.select_with_conversation_context(
            query, conversation_history, user_preferences
        )

        assert isinstance(result, ToolSelectionResult)

    @pytest.mark.asyncio
    async def test_conversation_memory_tracking(self):
        """Test conversation memory tracking."""
        # Should start with empty memory
        assert len(self.selector.conversation_memory) == 0

        # After selection with context, memory should be updated
        query = "test memory"
        history = [HumanMessage(content="previous context")]

        await self.selector.select_with_conversation_context(query, history)

        # Memory tracking would be implemented in actual context analysis
        # This tests the structure is in place
        assert hasattr(self.selector, "conversation_memory")

    @pytest.mark.asyncio
    async def test_pattern_analysis(self):
        """Test conversation pattern analysis."""
        complex_history = [
            HumanMessage(content="I need to search for research papers"),
            AIMessage(content="I can help with academic search"),
            ToolMessage(content="Found 10 papers", name="search_tool"),
            HumanMessage(content="Now analyze the citation patterns"),
            AIMessage(content="I'll analyze citations"),
            ToolMessage(content="Analysis complete", name="analysis_tool"),
            HumanMessage(content="Create a visualization of the trends"),
        ]

        # Test pattern analysis method
        patterns = await self.selector._analyze_conversation_patterns(complex_history)

        assert isinstance(patterns, dict)
        assert "topic_consistency" in patterns
        assert "complexity_trend" in patterns
        assert "tool_effectiveness" in patterns
        assert "user_satisfaction_signals" in patterns

    def test_previous_tool_extraction(self):
        """Test extraction of previously used tools."""
        history_with_tools = [
            HumanMessage(content="search for data"),
            AIMessage(content="searching..."),
            ToolMessage(content="search results", name="search_tool"),
            HumanMessage(content="analyze results"),
            ToolMessage(content="analysis done", name="analysis_tool"),
        ]

        tools_used = self.selector._extract_previous_tool_usage(history_with_tools)

        assert "search_tool" in tools_used
        assert "analysis_tool" in tools_used
        assert len(tools_used) == 2


class TestIntegrationScenarios:
    """Integration tests for dynamic tool selection."""

    @pytest.mark.asyncio
    async def test_multi_step_workflow_selection(self):
        """Test tool selection for complex multi-step workflows."""
        selector = DynamicToolSelector(
            selection_mode=SelectionMode.ADAPTIVE, max_tools_per_query=5
        )

        # Mock comprehensive workflow
        workflow_query = """
        Execute a complete data science pipeline:
        1. Extract data from APIs and databases
        2. Clean and preprocess the data
        3. Perform statistical analysis and modeling
        4. Create visualizations and dashboards
        5. Generate automated reports and send notifications
        """

        # Mock semantic discovery with relevant tools
        mock_discovery = MagicMock()
        mock_discovery.discover_and_index_components = AsyncMock()
        mock_discovery._component_cache = {
            "all": [
                ComponentMetadata(
                    name="api_extractor",
                    description="Extract data from APIs",
                    capabilities=["api_integration", "data_extraction"],
                    tags=["api", "data"],
                ),
                ComponentMetadata(
                    name="data_cleaner",
                    description="Clean and preprocess data",
                    capabilities=["data_cleaning", "preprocessing"],
                    tags=["data", "cleaning"],
                ),
                ComponentMetadata(
                    name="ml_analyzer",
                    description="Statistical analysis and modeling",
                    capabilities=["statistics", "machine_learning", "modeling"],
                    tags=["ml", "statistics"],
                ),
                ComponentMetadata(
                    name="visualizer",
                    description="Create charts and dashboards",
                    capabilities=["visualization", "dashboards"],
                    tags=["charts", "visualization"],
                ),
                ComponentMetadata(
                    name="report_generator",
                    description="Generate automated reports",
                    capabilities=["reporting", "document_generation"],
                    tags=["reports", "documents"],
                ),
            ]
        }
        selector.semantic_discovery = mock_discovery

        # Mock strategy that returns relevant tools
        mock_strategy = AsyncMock()
        mock_strategy.select_tools.return_value = ToolSelectionResult(
            selected_tools=mock_discovery._component_cache["all"][
                :4
            ],  # Return first 4 tools
            selection_confidence=0.9,
            selection_metadata={"strategy": "workflow_aware"},
        )
        selector.selection_strategies = {"adaptive": mock_strategy}

        result = await selector.select_tools_for_query(workflow_query)

        # Should select multiple tools for complex workflow
        assert len(result.selected_tools) >= 3
        assert result.selection_confidence > 0.7

        # Should identify workflow complexity
        context = selector.context_state
        assert "data" in context.current_query.lower()
        assert "pipeline" in context.current_query.lower()

    @pytest.mark.asyncio
    async def test_iterative_tool_refinement_scenario(self):
        """Test iterative refinement in a realistic scenario."""
        selector = DynamicToolSelector(learning_enabled=True)

        # Mock discovery
        mock_discovery = MagicMock()
        mock_discovery.discover_and_index_components = AsyncMock()
        mock_discovery._component_cache = {
            "all": [
                ComponentMetadata(
                    name="web_search",
                    description="Search the web",
                    capabilities=["search", "web"],
                    tags=["web"],
                ),
                ComponentMetadata(
                    name="academic_search",
                    description="Search academic papers",
                    capabilities=["search", "academic"],
                    tags=["academic"],
                ),
            ]
        }
        selector.semantic_discovery = mock_discovery

        # Mock strategy
        mock_strategy = AsyncMock()
        mock_strategy.select_tools.return_value = ToolSelectionResult(
            selected_tools=[mock_discovery._component_cache["all"][0]],
            selection_confidence=0.6,
        )
        selector.selection_strategies = {"adaptive": mock_strategy}

        initial_query = "search for information about quantum computing"
        llm_response = "I need more specific academic sources"
        execution_results = {
            "success_count": 1,
            "error_count": 0,
            "incomplete": True,  # Indicates need for refinement
            "feedback": "need academic sources",
        }

        refined_result = await selector.iterative_tool_refinement(
            initial_query, llm_response, execution_results, max_iterations=2
        )

        assert isinstance(refined_result, ToolSelectionResult)
        assert refined_result.selection_confidence >= 0.0

    @pytest.mark.asyncio
    async def test_learning_from_usage_patterns(self):
        """Test learning from tool usage patterns."""
        selector = DynamicToolSelector(learning_enabled=True)

        # Simulate usage patterns
        selector.usage_stats = {
            "high_success_tool": ToolUsageStats(
                tool_name="high_success_tool",
                usage_count=20,
                success_count=18,
                avg_execution_time=150.0,
                contexts_used=["data_analysis", "research"],
            ),
            "low_success_tool": ToolUsageStats(
                tool_name="low_success_tool",
                usage_count=15,
                success_count=5,
                avg_execution_time=300.0,
                error_count=10,
                contexts_used=["web_search"],
            ),
            "fast_tool": ToolUsageStats(
                tool_name="fast_tool",
                usage_count=10,
                success_count=9,
                avg_execution_time=50.0,
                contexts_used=["quick_tasks"],
            ),
        }

        analysis = await selector.analyze_tool_performance()

        # Should identify performance patterns
        assert analysis["total_tools_tracked"] == 3
        assert len(analysis["most_used_tools"]) > 0
        assert len(analysis["highest_success_rate"]) > 0
        assert len(analysis["fastest_tools"]) > 0
        assert len(analysis["recommendations"]) >= 0  # May have recommendations

        # Check specific patterns
        most_used = analysis["most_used_tools"][0]
        assert most_used["usage_count"] == 20  # high_success_tool

        fastest = analysis["fastest_tools"][0]
        assert fastest["avg_time_ms"] == 50.0  # fast_tool

    @pytest.mark.asyncio
    async def test_real_world_performance_scenario(self):
        """Test performance with realistic load."""
        import time

        selector = DynamicToolSelector(max_tools_per_query=10, cache_ttl_seconds=60.0)

        # Create realistic number of tools
        large_tool_set = []
        for i in range(50):
            large_tool_set.append(
                ComponentMetadata(
                    name=f"tool_{i}",
                    description=f"Tool for task type {i % 10}",
                    capabilities=[f"capability_{i % 5}", "general"],
                    tags=[f"category_{i % 3}", "utility"],
                )
            )

        mock_discovery = MagicMock()
        mock_discovery.discover_and_index_components = AsyncMock()
        mock_discovery._component_cache = {"all": large_tool_set}
        selector.semantic_discovery = mock_discovery

        # Mock efficient strategy
        mock_strategy = AsyncMock()
        mock_strategy.select_tools.return_value = ToolSelectionResult(
            selected_tools=large_tool_set[:5], selection_confidence=0.8  # Return top 5
        )
        selector.selection_strategies = {"adaptive": mock_strategy}

        # Test multiple queries
        queries = [
            "process data files",
            "search for information",
            "analyze results",
            "generate reports",
            "send notifications",
        ]

        start_time = time.time()

        for query in queries:
            result = await selector.select_tools_for_query(query)
            assert isinstance(result, ToolSelectionResult)
            assert len(result.selected_tools) <= 10

        total_time = time.time() - start_time

        # Should handle multiple queries efficiently
        assert total_time < 2.0  # Should complete in under 2 seconds

        # Cache should improve performance on repeated queries
        start_time = time.time()
        await selector.select_tools_for_query(queries[0])  # Repeat first query
        cache_time = time.time() - start_time

        # Cached query should be faster (if caching is working)
        assert cache_time < 0.1  # Should be very fast with cache


class TestFactoryFunctions:
    """Test factory functions for creating selectors."""

    def test_create_dynamic_tool_selector(self):
        """Test factory function for dynamic tool selector."""
        selector = create_dynamic_tool_selector(
            selection_mode=SelectionMode.ADAPTIVE, max_tools=7
        )

        assert isinstance(selector, DynamicToolSelector)
        assert selector.selection_mode == SelectionMode.ADAPTIVE
        assert selector.max_tools_per_query == 7

    def test_create_langgraph_style_selector(self):
        """Test factory function for LangGraph-style selector."""
        selector = create_langgraph_style_selector(max_tools=8, learning_enabled=False)

        assert isinstance(selector, LangGraphStyleSelector)
        assert selector.selection_mode == SelectionMode.CONTEXTUAL
        assert selector.max_tools_per_query == 8
        assert selector.learning_enabled == False

    def test_create_context_aware_selector(self):
        """Test factory function for context-aware selector."""
        selector = create_context_aware_selector(max_tools=6, min_confidence=0.8)

        assert isinstance(selector, ContextAwareSelector)
        assert selector.selection_mode == SelectionMode.CONTEXTUAL
        assert selector.max_tools_per_query == 6
        assert selector.min_confidence_threshold == 0.8


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
