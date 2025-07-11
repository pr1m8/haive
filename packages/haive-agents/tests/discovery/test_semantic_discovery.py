"""Comprehensive tests for semantic discovery system.

This test suite provides extensive testing of the semantic discovery
system with challenging real-world scenarios and edge cases.
"""

import asyncio
from typing import Any, Dict, List, Optional
from unittest.mock import AsyncMock, Mock, patch

import pytest

from haive.agents.discovery.semantic_discovery import (
    CapabilityMatcher,
    ComponentMetadata,
    DiscoveryMode,
    QueryAnalysis,
    QueryAnalyzer,
    SemanticDiscoveryEngine,
    ToolSelectionStrategy,
    VectorBasedToolSelector,
    create_semantic_discovery,
)


class TestQueryAnalyzer:
    """Test suite for QueryAnalyzer."""

    def setup_method(self):
        """Setup test fixtures."""
        self.analyzer = QueryAnalyzer()

    def test_simple_query_analysis(self):
        """Test analysis of simple queries."""
        query = "search for documents about machine learning"
        analysis = self.analyzer.analyze_query(query)

        assert analysis.original_query == query
        assert "machine" in analysis.extracted_keywords
        assert "learning" in analysis.extracted_keywords
        assert "search" in analysis.extracted_keywords
        assert (
            "text_processing" in analysis.inferred_capabilities
            or "retrieval" in analysis.inferred_capabilities
        )
        assert analysis.complexity_score >= 0.0
        assert analysis.intent_classification in ["retrieval", "general"]

    def test_complex_technical_query(self):
        """Test analysis of complex technical queries."""
        query = """Create a comprehensive data analysis pipeline that can:
        1. Extract data from multiple REST APIs
        2. Transform and clean the data using pandas
        3. Generate statistical reports and visualizations
        4. Send automated email notifications with results
        5. Store processed data in a SQL database"""

        analysis = self.analyzer.analyze_query(query)

        assert analysis.complexity_score > 0.5  # Should be complex
        assert len(analysis.inferred_capabilities) >= 3  # Multiple capabilities needed
        assert "api_integration" in analysis.inferred_capabilities
        assert "data_analysis" in analysis.inferred_capabilities
        assert (
            "database" in analysis.inferred_capabilities
            or "email" in analysis.inferred_capabilities
        )
        assert analysis.intent_classification in ["generation", "complex_workflow"]

    def test_domain_identification(self):
        """Test domain identification from queries."""
        test_cases = [
            (
                "Analyze medical patient data for diagnosis patterns",
                ["healthcare", "scientific"],
            ),
            ("Create a business strategy report for Q4 revenue", ["business"]),
            (
                "Write academic research paper on neural networks",
                ["academic", "technical"],
            ),
            (
                "Design creative marketing materials for campaign",
                ["creative", "business"],
            ),
        ]

        for query, expected_domains in test_cases:
            analysis = self.analyzer.analyze_query(query)
            assert any(
                domain in analysis.domain_tags for domain in expected_domains
            ), f"Expected domains {expected_domains} not found in {analysis.domain_tags} for query: {query}"

    def test_edge_cases(self):
        """Test edge cases and unusual queries."""
        edge_cases = [
            "",  # Empty query
            "a",  # Single character
            "the quick brown fox jumps over the lazy dog",  # Common words only
            "🚀 🔬 💡",  # Emojis only
            "1234567890",  # Numbers only
            "UPPERCASE QUERY WITH LOTS OF SHOUTING",  # All caps
        ]

        for query in edge_cases:
            analysis = self.analyzer.analyze_query(query)
            assert isinstance(analysis, QueryAnalysis)
            assert analysis.original_query == query
            assert analysis.complexity_score >= 0.0
            assert analysis.complexity_score <= 1.0


class TestCapabilityMatcher:
    """Test suite for CapabilityMatcher."""

    def setup_method(self):
        """Setup test fixtures."""
        self.matcher = CapabilityMatcher()

    def test_perfect_capability_match(self):
        """Test perfect capability matching."""
        required = ["search", "analysis", "reporting"]
        available = ["search", "analysis", "reporting", "extra_capability"]

        score = self.matcher.calculate_capability_match(required, available)
        assert score == 1.0  # Perfect match

    def test_partial_capability_match(self):
        """Test partial capability matching."""
        required = ["search", "analysis", "reporting", "database"]
        available = ["search", "analysis"]

        score = self.matcher.calculate_capability_match(required, available)
        assert score == 0.5  # 2 out of 4 capabilities matched

    def test_no_capability_match(self):
        """Test no capability matching."""
        required = ["search", "analysis"]
        available = ["email", "calendar"]

        score = self.matcher.calculate_capability_match(required, available)
        assert (
            score < 0.3
        )  # Should be low, but keyword similarity might give some score

    def test_tag_based_matching(self):
        """Test capability matching with tags."""
        required = ["web_search"]
        available = ["internet_access"]
        tags = ["web_search", "online"]

        score = self.matcher.calculate_capability_match(required, available, tags)
        assert score >= 0.5  # Tag match should provide partial credit

    def test_keyword_similarity_matching(self):
        """Test keyword-level similarity matching."""
        required = ["data_analysis"]
        available = ["data_processing", "statistical_analysis"]

        score = self.matcher.calculate_capability_match(required, available)
        assert score > 0.0  # Should have some similarity due to overlapping words


class MockEmbeddingProvider:
    """Mock embedding provider for testing."""

    def embed_text(self, text: str) -> list[float]:
        """Mock text embedding."""
        # Simple hash-based embedding for testing
        import hashlib

        hash_obj = hashlib.md5(text.encode())
        # Convert hash to list of floats
        hash_bytes = hash_obj.digest()
        return [float(b) / 255.0 for b in hash_bytes[:10]]  # 10-dimensional embedding

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """Mock multiple text embeddings."""
        return [self.embed_text(text) for text in texts]


class MockVectorStore:
    """Mock vector store for testing."""

    def __init__(self):
        self.documents = []
        self.embeddings = []

    def add_documents(self, documents) -> None:
        """Mock add documents."""
        self.documents.extend(documents)

    def similarity_search(self, query: str, k: int = 5, filter=None) -> list:
        """Mock similarity search."""
        # Simple mock that returns documents based on keyword matching
        query_words = set(query.lower().split())

        scored_docs = []
        for doc in self.documents:
            doc_words = set(doc.page_content.lower().split())
            score = len(query_words.intersection(doc_words)) / max(len(query_words), 1)
            if score > 0:
                scored_docs.append((doc, score))

        # Sort by score and return top k
        scored_docs.sort(key=lambda x: x[1], reverse=True)
        return [doc for doc, _ in scored_docs[:k]]

    def similarity_search_with_score(self, query: str, k: int = 5, filter=None) -> list:
        """Mock similarity search with scores."""
        query_words = set(query.lower().split())

        scored_docs = []
        for doc in self.documents:
            doc_words = set(doc.page_content.lower().split())
            score = len(query_words.intersection(doc_words)) / max(len(query_words), 1)
            scored_docs.append((doc, score))

        # Sort by score and return top k
        scored_docs.sort(key=lambda x: x[1], reverse=True)
        return scored_docs[:k]


class TestVectorBasedToolSelector:
    """Test suite for VectorBasedToolSelector."""

    def setup_method(self):
        """Setup test fixtures."""
        self.mock_embedding = MockEmbeddingProvider()
        self.mock_vector_store = MockVectorStore()

        self.selector = VectorBasedToolSelector(
            embedding_provider=self.mock_embedding,
            vector_store=self.mock_vector_store,
            similarity_threshold=0.3,
        )

        # Create test components
        self.test_components = [
            ComponentMetadata(
                name="web_search_tool",
                description="Search the web for information",
                capabilities=["search", "web_access", "information_retrieval"],
                tags=["web", "search", "online"],
            ),
            ComponentMetadata(
                name="data_analyzer",
                description="Analyze and process data files",
                capabilities=["data_analysis", "statistics", "visualization"],
                tags=["data", "analytics", "processing"],
            ),
            ComponentMetadata(
                name="email_sender",
                description="Send emails and notifications",
                capabilities=["email", "communication", "notification"],
                tags=["email", "messaging", "alerts"],
            ),
            ComponentMetadata(
                name="file_processor",
                description="Process and transform various file formats",
                capabilities=[
                    "file_processing",
                    "data_transformation",
                    "format_conversion",
                ],
                tags=["files", "processing", "conversion"],
            ),
        ]

    def test_component_indexing(self):
        """Test indexing of components in vector store."""
        self.selector.index_components(self.test_components)

        # Check that components were indexed
        assert len(self.selector._indexed_components) == len(self.test_components)
        assert len(self.mock_vector_store.documents) == len(self.test_components)

        # Check component metadata is stored
        for component in self.test_components:
            assert component.name in self.selector._indexed_components

    def test_tool_selection_top_k(self):
        """Test top-k tool selection."""
        self.selector.index_components(self.test_components)

        query = "search for information online"
        selected = self.selector.select_tools(
            query, strategy=ToolSelectionStrategy.TOP_K, k=2
        )

        assert len(selected) <= 2
        # Web search tool should be highly ranked for this query
        selected_names = [tool.name for tool in selected]
        assert "web_search_tool" in selected_names

    def test_tool_selection_threshold(self):
        """Test threshold-based tool selection."""
        self.selector.index_components(self.test_components)

        query = "analyze data statistics"
        selected = self.selector.select_tools(
            query, strategy=ToolSelectionStrategy.THRESHOLD, k=5
        )

        # All selected tools should meet similarity threshold
        for tool in selected:
            assert tool.similarity_score >= self.selector.similarity_threshold

    def test_diverse_tool_selection(self):
        """Test diverse tool selection to avoid redundancy."""
        # Add similar tools to test diversity
        similar_components = [
            *self.test_components,
            ComponentMetadata(
                name="alternative_search",
                description="Alternative web search engine",
                capabilities=["search", "web_access"],
                tags=["web", "search"],
            ),
            ComponentMetadata(
                name="another_analyzer",
                description="Another data analysis tool",
                capabilities=["data_analysis", "statistics"],
                tags=["data", "analytics"],
            ),
        ]

        self.selector.index_components(similar_components)

        query = "search and analyze web data"
        selected = self.selector.select_tools(
            query, strategy=ToolSelectionStrategy.DIVERSE, k=3
        )

        # Should select diverse tools, not just similar search tools
        capabilities = []
        for tool in selected:
            capabilities.extend(tool.capabilities)

        unique_capabilities = set(capabilities)
        assert len(unique_capabilities) >= 3  # Should have diverse capabilities

    def test_capability_filtering(self):
        """Test tool selection with capability filtering."""
        self.selector.index_components(self.test_components)

        query = "process files"
        selected = self.selector.select_tools(
            query, capability_filter=["file_processing", "data_transformation"]
        )

        # Should only return tools with specified capabilities
        for tool in selected:
            assert any(
                cap in tool.capabilities
                for cap in ["file_processing", "data_transformation"]
            )

    def test_empty_query_handling(self):
        """Test handling of empty or invalid queries."""
        self.selector.index_components(self.test_components)

        edge_cases = ["", "   ", "a", "the and or but"]

        for query in edge_cases:
            selected = self.selector.select_tools(query)
            assert isinstance(selected, list)  # Should not crash

    def test_no_components_scenario(self):
        """Test tool selection when no components are available."""
        query = "search for something"
        selected = self.selector.select_tools(query)

        assert selected == []  # Should return empty list


class TestSemanticDiscoveryEngine:
    """Test suite for SemanticDiscoveryEngine."""

    def setup_method(self):
        """Setup test fixtures."""
        self.mock_embedding = MockEmbeddingProvider()
        self.mock_vector_store = MockVectorStore()

        # Mock the Haive discovery
        self.mock_discovery_results = {
            "tools": [
                {
                    "name": "search_engine",
                    "description": "Web search capabilities",
                    "metadata": {
                        "capabilities": ["search", "web_access"],
                        "tags": ["web", "search"],
                    },
                },
                {
                    "name": "data_processor",
                    "description": "Process and analyze data",
                    "metadata": {
                        "capabilities": ["data_analysis", "processing"],
                        "tags": ["data", "analytics"],
                    },
                },
            ]
        }

        self.engine = SemanticDiscoveryEngine(
            discovery_mode=DiscoveryMode.HYBRID,
            embedding_provider=self.mock_embedding,
            vector_store=self.mock_vector_store,
        )

    @pytest.mark.asyncio
    async def test_component_discovery_and_indexing(self):
        """Test component discovery and indexing process."""
        # Mock the discovery process
        with patch.object(self.engine, "haive_discovery") as mock_haive:
            mock_haive.discover_all.return_value = self.mock_discovery_results

            await self.engine.discover_and_index_components()

            # Check that components were discovered and cached
            assert "all" in self.engine._component_cache
            components = self.engine._component_cache["all"]
            assert len(components) >= 2

            # Check that vector store was populated
            assert len(self.mock_vector_store.documents) >= 2

    @pytest.mark.asyncio
    async def test_semantic_tool_selection_simple(self):
        """Test semantic tool selection for simple queries."""
        # Setup discovery results
        with patch.object(self.engine, "haive_discovery") as mock_haive:
            mock_haive.discover_all.return_value = self.mock_discovery_results

            query = "search for web information"
            tools, analysis = await self.engine.semantic_tool_selection(
                query, max_tools=3
            )

            assert isinstance(tools, list)
            assert isinstance(analysis, QueryAnalysis)
            assert analysis.original_query == query
            assert len(analysis.suggested_tools) == len(tools)

    @pytest.mark.asyncio
    async def test_semantic_tool_selection_complex(self):
        """Test semantic tool selection for complex multi-step queries."""
        with patch.object(self.engine, "haive_discovery") as mock_haive:
            mock_haive.discover_all.return_value = self.mock_discovery_results

            complex_query = """
            I need to:
            1. Search for recent research papers on AI
            2. Download and analyze the data
            3. Create visualizations and reports
            4. Send notifications when complete
            """

            tools, analysis = await self.engine.semantic_tool_selection(
                complex_query, max_tools=5, strategy=ToolSelectionStrategy.HYBRID
            )

            assert analysis.complexity_score > 0.5  # Should be complex
            assert len(analysis.inferred_capabilities) >= 2  # Multiple capabilities
            assert len(tools) >= 1  # Should find relevant tools

    @pytest.mark.asyncio
    async def test_different_discovery_modes(self):
        """Test different discovery modes."""
        modes_to_test = [
            DiscoveryMode.SIMILARITY,
            DiscoveryMode.CAPABILITY,
            DiscoveryMode.CONTEXTUAL,
            DiscoveryMode.HYBRID,
        ]

        with patch.object(self.engine, "haive_discovery") as mock_haive:
            mock_haive.discover_all.return_value = self.mock_discovery_results

            query = "analyze web data"

            for mode in modes_to_test:
                self.engine.discovery_mode = mode
                tools, analysis = await self.engine.semantic_tool_selection(query)

                assert isinstance(tools, list)
                assert isinstance(analysis, QueryAnalysis)

    @pytest.mark.asyncio
    async def test_capability_filtering(self):
        """Test tool selection with capability filtering."""
        with patch.object(self.engine, "haive_discovery") as mock_haive:
            mock_haive.discover_all.return_value = self.mock_discovery_results

            query = "process data"
            capability_filter = ["data_analysis", "processing"]

            tools, analysis = await self.engine.semantic_tool_selection(
                query, capability_filter=capability_filter
            )

            # All selected tools should have the filtered capabilities
            for tool in tools:
                assert any(cap in tool.capabilities for cap in capability_filter)

    @pytest.mark.asyncio
    async def test_error_handling(self):
        """Test error handling in discovery process."""
        # Test with failing discovery
        with patch.object(self.engine, "haive_discovery") as mock_haive:
            mock_haive.discover_all.side_effect = Exception("Discovery failed")

            # Should not crash but handle gracefully
            with pytest.raises(Exception):
                await self.engine.discover_and_index_components(force_refresh=True)

    @pytest.mark.asyncio
    async def test_caching_behavior(self):
        """Test caching behavior of discovery system."""
        with patch.object(self.engine, "haive_discovery") as mock_haive:
            mock_haive.discover_all.return_value = self.mock_discovery_results

            # First call should trigger discovery
            await self.engine.discover_and_index_components()
            first_call_count = mock_haive.discover_all.call_count

            # Second call should use cache
            await self.engine.discover_and_index_components()
            second_call_count = mock_haive.discover_all.call_count

            assert second_call_count == first_call_count  # Should use cache

            # Force refresh should trigger new discovery
            await self.engine.discover_and_index_components(force_refresh=True)
            third_call_count = mock_haive.discover_all.call_count

            assert third_call_count > second_call_count  # Should discover again


class TestIntegrationScenarios:
    """Integration tests with challenging real-world scenarios."""

    @pytest.mark.asyncio
    async def test_scientific_research_workflow(self):
        """Test tool selection for scientific research workflow."""
        # Mock comprehensive scientific tools
        scientific_tools = {
            "tools": [
                {
                    "name": "paper_searcher",
                    "description": "Search academic papers and publications",
                    "metadata": {
                        "capabilities": [
                            "search",
                            "academic_search",
                            "paper_retrieval",
                        ],
                        "tags": ["academic", "research", "papers"],
                        "domain": "scientific",
                    },
                },
                {
                    "name": "data_analyzer",
                    "description": "Statistical analysis and data processing",
                    "metadata": {
                        "capabilities": ["statistics", "data_analysis", "modeling"],
                        "tags": ["data", "statistics", "analysis"],
                        "domain": "scientific",
                    },
                },
                {
                    "name": "visualization_tool",
                    "description": "Create charts, graphs and scientific visualizations",
                    "metadata": {
                        "capabilities": ["visualization", "charting", "graphing"],
                        "tags": ["visualization", "charts", "graphics"],
                        "domain": "scientific",
                    },
                },
                {
                    "name": "citation_manager",
                    "description": "Manage citations and references",
                    "metadata": {
                        "capabilities": [
                            "citation",
                            "reference_management",
                            "bibliography",
                        ],
                        "tags": ["citations", "references", "academic"],
                        "domain": "scientific",
                    },
                },
            ]
        }

        engine = SemanticDiscoveryEngine(
            discovery_mode=DiscoveryMode.HYBRID,
            embedding_provider=MockEmbeddingProvider(),
            vector_store=MockVectorStore(),
        )

        with patch.object(engine, "haive_discovery") as mock_haive:
            mock_haive.discover_all.return_value = scientific_tools

            research_query = """
            Conduct a comprehensive literature review on quantum computing algorithms:
            1. Search for recent papers from top conferences
            2. Analyze citation patterns and research trends
            3. Create visualizations showing the evolution of the field
            4. Generate a bibliography with proper citations
            """

            tools, analysis = await engine.semantic_tool_selection(
                research_query, max_tools=4
            )

            # Should identify this as complex academic workflow
            assert analysis.complexity_score > 0.7
            assert "academic" in analysis.domain_tags
            assert analysis.intent_classification in ["complex_workflow", "analysis"]

            # Should select relevant tools for each step
            selected_names = [tool.name for tool in tools]
            assert "paper_searcher" in selected_names
            assert any("analyz" in name for name in selected_names)
            assert len(tools) >= 2  # Should select multiple tools for complex workflow

    @pytest.mark.asyncio
    async def test_business_intelligence_scenario(self):
        """Test tool selection for business intelligence tasks."""
        business_tools = {
            "tools": [
                {
                    "name": "crm_connector",
                    "description": "Connect to CRM systems and extract customer data",
                    "metadata": {
                        "capabilities": [
                            "crm_integration",
                            "data_extraction",
                            "customer_data",
                        ],
                        "tags": ["crm", "business", "customers"],
                        "domain": "business",
                    },
                },
                {
                    "name": "sales_analyzer",
                    "description": "Analyze sales performance and trends",
                    "metadata": {
                        "capabilities": [
                            "sales_analysis",
                            "performance_metrics",
                            "trending",
                        ],
                        "tags": ["sales", "business", "analytics"],
                        "domain": "business",
                    },
                },
                {
                    "name": "dashboard_creator",
                    "description": "Create business dashboards and KPI reports",
                    "metadata": {
                        "capabilities": ["dashboards", "reporting", "kpi_tracking"],
                        "tags": ["dashboard", "business", "reporting"],
                        "domain": "business",
                    },
                },
                {
                    "name": "forecast_model",
                    "description": "Create predictive models for business forecasting",
                    "metadata": {
                        "capabilities": [
                            "forecasting",
                            "predictive_modeling",
                            "predictions",
                        ],
                        "tags": ["forecasting", "business", "predictions"],
                        "domain": "business",
                    },
                },
            ]
        }

        engine = SemanticDiscoveryEngine(
            discovery_mode=DiscoveryMode.CONTEXTUAL,
            embedding_provider=MockEmbeddingProvider(),
            vector_store=MockVectorStore(),
        )

        with patch.object(engine, "haive_discovery") as mock_haive:
            mock_haive.discover_all.return_value = business_tools

            business_query = """
            Create a quarterly business performance report:
            - Pull customer data from our CRM
            - Analyze sales trends and growth patterns
            - Build interactive dashboards for stakeholders
            - Generate forecasts for next quarter
            """

            tools, analysis = await engine.semantic_tool_selection(
                business_query, max_tools=5
            )

            # Should identify business domain
            assert "business" in analysis.domain_tags
            assert analysis.intent_classification in ["generation", "complex_workflow"]

            # Should select business-relevant tools
            selected_capabilities = []
            for tool in tools:
                selected_capabilities.extend(tool.capabilities)

            assert any("crm" in cap for cap in selected_capabilities)
            assert any("sales" in cap for cap in selected_capabilities)
            assert any("dashboard" in cap for cap in selected_capabilities)

    @pytest.mark.asyncio
    async def test_edge_case_queries(self):
        """Test handling of edge case queries."""
        engine = SemanticDiscoveryEngine(
            embedding_provider=MockEmbeddingProvider(), vector_store=MockVectorStore()
        )

        # Mock minimal tools
        minimal_tools = {
            "tools": [
                {
                    "name": "generic_tool",
                    "description": "A generic tool",
                    "metadata": {"capabilities": ["general"], "tags": ["generic"]},
                }
            ]
        }

        with patch.object(engine, "haive_discovery") as mock_haive:
            mock_haive.discover_all.return_value = minimal_tools

            edge_cases = [
                "",  # Empty query
                "help",  # Single word
                "What can you do?",  # Meta question
                "Lorem ipsum dolor sit amet",  # Latin text
                "🚀 🔬 💡 🎯 ⚡",  # Emojis only
                "1 + 1 = 2",  # Mathematical expression
                "SELECT * FROM users WHERE active = 1",  # SQL query
            ]

            for query in edge_cases:
                tools, analysis = await engine.semantic_tool_selection(query)

                # Should handle gracefully without crashing
                assert isinstance(tools, list)
                assert isinstance(analysis, QueryAnalysis)
                assert analysis.original_query == query
                assert 0.0 <= analysis.complexity_score <= 1.0

    @pytest.mark.asyncio
    async def test_performance_with_many_tools(self):
        """Test performance with large number of tools."""
        import time

        # Create many tools
        many_tools = {"tools": []}
        for i in range(100):
            many_tools["tools"].append(
                {
                    "name": f"tool_{i}",
                    "description": f"Tool number {i} for various tasks",
                    "metadata": {
                        "capabilities": [f"capability_{i % 10}", "general"],
                        "tags": [f"tag_{i % 5}", "category"],
                        "domain": "general",
                    },
                }
            )

        engine = SemanticDiscoveryEngine(
            embedding_provider=MockEmbeddingProvider(), vector_store=MockVectorStore()
        )

        with patch.object(engine, "haive_discovery") as mock_haive:
            mock_haive.discover_all.return_value = many_tools

            query = "find tools for data processing"

            # Measure performance
            start_time = time.time()
            tools, analysis = await engine.semantic_tool_selection(query, max_tools=10)
            end_time = time.time()

            execution_time = end_time - start_time

            # Should complete reasonably quickly even with many tools
            assert execution_time < 5.0  # Should complete in under 5 seconds
            assert len(tools) <= 10  # Should respect max_tools limit
            assert isinstance(analysis, QueryAnalysis)


class TestFactoryFunctions:
    """Test factory functions and convenience methods."""

    def test_create_semantic_discovery(self):
        """Test factory function for creating semantic discovery."""
        engine = create_semantic_discovery()

        assert isinstance(engine, SemanticDiscoveryEngine)
        assert engine.discovery_mode == DiscoveryMode.HYBRID
        assert engine.query_analyzer is not None
        assert engine.capability_matcher is not None
        assert engine.vector_selector is not None

    def test_create_semantic_discovery_with_params(self):
        """Test factory function with custom parameters."""
        mock_embedding = MockEmbeddingProvider()
        mock_vector_store = MockVectorStore()

        engine = create_semantic_discovery(
            embedding_provider=mock_embedding,
            vector_store=mock_vector_store,
            haive_root="/custom/path",
        )

        assert engine.vector_selector.embedding_provider == mock_embedding
        assert engine.vector_selector.vector_store == mock_vector_store
        assert engine.haive_root == "/custom/path"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
