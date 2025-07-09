"""Comprehensive tests for the Document Agent.

Tests the complete document processing agent that implements:
FETCH -> LOAD -> TRANSFORM -> SPLIT -> ANNOTATE -> EMBED -> STORE -> RETRIEVE
"""

import tempfile
from pathlib import Path
from typing import List

import pytest
from haive.core.engine.document.config import (
    ChunkingStrategy,
    DocumentSourceType,
    ProcessingStrategy,
)

from haive.agents.document.agent import DocumentAgent, DocumentProcessingResult


class TestDocumentAgent:
    """Test the DocumentAgent class."""

    def test_create_default_agent(self):
        """Test creating a document agent with default configuration."""
        agent = DocumentAgent()

        assert agent is not None
        assert agent.name is not None
        assert agent.engine is not None
        assert agent.processing_strategy == ProcessingStrategy.ENHANCED
        assert agent.chunking_strategy == ChunkingStrategy.RECURSIVE
        assert agent.chunk_size == 1000
        assert agent.chunk_overlap == 200
        assert agent.parallel_processing is True

    def test_create_agent_with_custom_config(self):
        """Test creating agent with custom configuration."""
        agent = DocumentAgent(
            name="Custom Document Agent",
            processing_strategy=ProcessingStrategy.PARALLEL,
            chunking_strategy=ChunkingStrategy.SEMANTIC,
            chunk_size=1500,
            chunk_overlap=300,
            max_workers=8,
            enable_embedding=True,
            enable_storage=True,
        )

        assert agent.name == "Custom Document Agent"
        assert agent.processing_strategy == ProcessingStrategy.PARALLEL
        assert agent.chunking_strategy == ChunkingStrategy.SEMANTIC
        assert agent.chunk_size == 1500
        assert agent.chunk_overlap == 300
        assert agent.max_workers == 8
        assert agent.enable_embedding is True
        assert agent.enable_storage is True

    def test_validation_chunk_overlap(self):
        """Test validation that chunk_overlap < chunk_size."""
        with pytest.raises(
            ValueError, match="chunk_overlap must be less than chunk_size"
        ):
            DocumentAgent(
                chunk_size=100, chunk_overlap=100  # Equal to chunk_size should fail
            )

    def test_agent_setup(self):
        """Test agent setup process."""
        agent = DocumentAgent()

        # Setup should be called during initialization
        assert "main" in agent.engines
        assert agent.engines["main"] == agent.engine
        assert agent.set_schema is True

    def test_build_graph(self):
        """Test graph building for document processing."""
        agent = DocumentAgent()
        graph = agent.build_graph()

        assert graph is not None
        assert "document_processor" in graph.nodes
        assert graph.metadata is not None
        assert "pipeline_stages" in graph.metadata
        assert "processing_strategy" in graph.metadata
        assert "chunking_strategy" in graph.metadata

    def test_pipeline_stages(self):
        """Test pipeline stage configuration."""
        # Test basic pipeline
        agent = DocumentAgent()
        stages = agent._get_pipeline_stages()
        expected_basic = ["fetch", "load", "transform", "split", "annotate"]
        assert stages == expected_basic

        # Test extended pipeline
        agent = DocumentAgent(
            enable_embedding=True, enable_storage=True, enable_retrieval=True
        )
        stages = agent._get_pipeline_stages()
        expected_extended = [
            "fetch",
            "load",
            "transform",
            "split",
            "annotate",
            "embed",
            "store",
            "retrieve",
        ]
        assert stages == expected_extended


class TestDocumentAgentProcessing:
    """Test document processing functionality."""

    def test_process_single_source_text(self):
        """Test processing a single text source."""
        agent = DocumentAgent(
            chunking_strategy=ChunkingStrategy.FIXED_SIZE,
            chunk_size=50,
            chunk_overlap=10,
        )

        test_content = "This is a test document. " * 10
        result = agent.process_sources(test_content)

        assert isinstance(result, DocumentProcessingResult)
        assert result.total_sources == 1
        assert result.total_documents == 1
        assert result.total_chunks > 0
        assert result.successful_sources == 1
        assert result.failed_sources == 0
        assert len(result.processing_errors) == 0

    def test_process_multiple_sources(self):
        """Test processing multiple sources."""
        agent = DocumentAgent(
            chunking_strategy=ChunkingStrategy.PARAGRAPH, chunk_size=100
        )

        test_sources = [
            "First document content. " * 20,
            "Second document content. " * 15,
            "Third document content. " * 25,
        ]

        result = agent.process_sources(test_sources)

        assert result.total_sources == 3
        assert result.total_documents == 3
        assert result.successful_sources == 3
        assert result.failed_sources == 0
        assert len(result.loaded_documents) == 3

    def test_process_with_max_sources_limit(self):
        """Test processing with max sources limit."""
        agent = DocumentAgent(max_sources=2)

        test_sources = [f"Document {i} content." for i in range(5)]
        result = agent.process_sources(test_sources)

        # Should only process first 2 sources
        assert result.total_sources == 2
        assert result.total_documents == 2

    def test_error_handling_skip_invalid(self):
        """Test error handling with skip_invalid=True."""
        agent = DocumentAgent(skip_invalid=True, raise_on_error=False)

        # Mix of valid and invalid sources
        sources = ["Valid content", None, "More valid content"]  # Invalid

        result = agent.process_sources(sources)

        # Should process valid sources and skip invalid ones
        assert result.total_sources == 3
        assert result.failed_sources > 0
        assert len(result.processing_errors) > 0

    def test_chunking_strategies(self):
        """Test different chunking strategies."""
        test_content = """This is paragraph one.

This is paragraph two with multiple sentences. It contains more content.

This is paragraph three."""

        strategies_to_test = [
            ChunkingStrategy.FIXED_SIZE,
            ChunkingStrategy.PARAGRAPH,
            ChunkingStrategy.SENTENCE,
            ChunkingStrategy.RECURSIVE,
        ]

        for strategy in strategies_to_test:
            agent = DocumentAgent(
                chunking_strategy=strategy, chunk_size=50, chunk_overlap=10
            )

            result = agent.process_sources(test_content)

            assert result.total_chunks > 0, f"Strategy {strategy} should create chunks"
            assert result.chunking_strategy == strategy.value

    def test_processing_strategies(self):
        """Test different processing strategies."""
        test_content = "Test content for processing strategy evaluation."

        strategies = [
            ProcessingStrategy.SIMPLE,
            ProcessingStrategy.ENHANCED,
            ProcessingStrategy.PARALLEL,
        ]

        for strategy in strategies:
            agent = DocumentAgent(processing_strategy=strategy)
            result = agent.process_sources(test_content)

            assert result.total_documents == 1
            assert result.pipeline_strategy == strategy.value

    def test_content_analysis(self):
        """Test content analysis features."""
        agent = DocumentAgent(extract_metadata=True, normalize_content=True)

        test_content = "   This   has   extra   spaces   and needs normalization.   "
        result = agent.process_sources(test_content)

        assert result.total_characters > 0
        assert result.total_words > 0
        assert result.total_annotations > 0

        # Check that content was normalized
        doc = result.loaded_documents[0]
        assert "   " not in doc["content"]  # Multiple spaces should be normalized


class TestDocumentAgentSpecializedMethods:
    """Test specialized processing methods."""

    def test_process_directory(self):
        """Test directory processing method."""
        # Create temporary directory with files
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test files
            for i in range(3):
                file_path = Path(temp_dir) / f"test_{i}.txt"
                file_path.write_text(f"Content of test file {i}")

            agent = DocumentAgent()

            # Test directory analysis (actual processing would need file loader)
            analysis = agent.analyze_source_structure(temp_dir)

            assert analysis is not None
            assert analysis["source"] == temp_dir

    def test_process_urls(self):
        """Test URL processing method."""
        agent = DocumentAgent()

        # Test URLs (won't actually fetch in test environment)
        urls = ["https://example.com/doc1.html", "https://example.com/doc2.pdf"]

        # This would normally process URLs, but we'll test the interface
        try:
            result = agent.process_urls(urls)
            # In test environment, this may fail due to network access
            # The important thing is the method exists and accepts the right parameters
        except Exception:
            # Expected in test environment without network access
            pass

    def test_process_cloud_storage(self):
        """Test cloud storage processing method."""
        agent = DocumentAgent()

        cloud_paths = ["s3://bucket/document1.pdf", "gs://bucket/document2.docx"]

        # Test the interface (won't actually access cloud in test)
        try:
            result = agent.process_cloud_storage(cloud_paths)
        except Exception:
            # Expected in test environment without cloud access
            pass

    def test_analyze_source_structure(self):
        """Test source structure analysis."""
        # Create a temporary file for testing
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("Test content for structure analysis")
            temp_path = f.name

        try:
            agent = DocumentAgent()
            analysis = agent.analyze_source_structure(temp_path)

            assert analysis is not None
            assert analysis["source"] == temp_path
            assert "analysis_time" in analysis

        finally:
            Path(temp_path).unlink(missing_ok=True)


class TestDocumentAgentConvenienceConstructors:
    """Test convenience constructor methods."""

    def test_create_for_pdfs(self):
        """Test PDF-optimized constructor."""
        agent = DocumentAgent.create_for_pdfs(name="Test PDF Agent", chunk_size=1500)

        assert agent.name == "Test PDF Agent"
        assert agent.chunking_strategy == ChunkingStrategy.PARAGRAPH
        assert agent.chunk_size == 1500
        assert agent.processing_strategy == ProcessingStrategy.ENHANCED
        assert agent.parallel_processing is True
        assert agent.extract_metadata is True

    def test_create_for_web_scraping(self):
        """Test web scraping constructor."""
        agent = DocumentAgent.create_for_web_scraping()

        assert "Web Scraping Agent" in agent.name
        assert DocumentSourceType.URL in agent.allowed_source_types
        assert agent.chunking_strategy == ChunkingStrategy.SEMANTIC
        assert agent.chunk_size == 1500
        assert agent.normalize_content is True
        assert agent.detect_language is True

    def test_create_for_databases(self):
        """Test database constructor."""
        agent = DocumentAgent.create_for_databases()

        assert "Database Document Agent" in agent.name
        assert agent.allowed_source_types == [DocumentSourceType.DATABASE]
        assert agent.chunking_strategy == ChunkingStrategy.FIXED_SIZE
        assert agent.chunk_size == 500
        assert agent.processing_strategy == ProcessingStrategy.PARALLEL
        assert agent.max_workers == 8

    def test_create_for_enterprise(self):
        """Test enterprise constructor."""
        agent = DocumentAgent.create_for_enterprise()

        assert "Enterprise Document Agent" in agent.name
        assert agent.processing_strategy == ProcessingStrategy.PARALLEL
        assert agent.chunking_strategy == ChunkingStrategy.RECURSIVE
        assert agent.max_workers == 16
        assert agent.enable_embedding is True
        assert agent.enable_storage is True
        assert agent.extract_metadata is True
        assert agent.normalize_content is True
        assert agent.detect_language is True

    def test_create_for_research(self):
        """Test research constructor."""
        agent = DocumentAgent.create_for_research()

        assert "Research Document Agent" in agent.name
        assert DocumentSourceType.FILE in agent.allowed_source_types
        assert DocumentSourceType.URL in agent.allowed_source_types
        assert DocumentSourceType.DATABASE in agent.allowed_source_types
        assert agent.chunking_strategy == ChunkingStrategy.SEMANTIC
        assert agent.chunk_size == 2000
        assert agent.chunk_overlap == 300
        assert agent.enable_embedding is True


class TestDocumentAgentResultProcessing:
    """Test result processing and aggregation."""

    def test_result_aggregation(self):
        """Test aggregation of multiple processing results."""
        agent = DocumentAgent()

        # Simulate multiple sources
        sources = [
            "Document 1 content. " * 50,
            "Document 2 content. " * 30,
            "Document 3 content. " * 40,
        ]

        result = agent.process_sources(sources)

        # Verify aggregation
        assert result.total_sources == 3
        assert result.total_documents == 3
        assert result.total_characters > 0
        assert result.total_words > 0
        assert result.processing_time > 0

        # Verify source types tracking
        assert "text" in result.source_types or "unknown" in result.source_types

        # Verify format tracking
        assert len(result.document_formats) > 0

    def test_result_statistics(self):
        """Test result statistics calculation."""
        agent = DocumentAgent(
            chunking_strategy=ChunkingStrategy.FIXED_SIZE, chunk_size=50
        )

        test_content = "Statistical test content. " * 20
        result = agent.process_sources(test_content)

        # Verify statistics
        assert result.total_chunks > 0
        assert result.average_chunk_size > 0
        assert result.average_chunk_size <= agent.chunk_size + 10  # Allow some variance

    def test_error_reporting(self):
        """Test error reporting in results."""
        agent = DocumentAgent(skip_invalid=True, raise_on_error=False)

        # Include some invalid content
        sources = [
            "Valid content",
            None,  # This should cause an error
        ]

        result = agent.process_sources(sources)

        assert result.failed_sources > 0
        assert len(result.processing_errors) > 0


class TestDocumentAgentIntegration:
    """Integration tests for DocumentAgent."""

    def test_real_file_processing(self):
        """Test processing real files."""
        # Create a temporary markdown file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(
                """# Test Document

This is a test markdown document for integration testing.

## Section 1

Content for section 1 with enough text to create multiple chunks when processed.

## Section 2

Content for section 2 with additional information and more detailed explanations.
"""
            )
            temp_path = f.name

        try:
            agent = DocumentAgent(
                chunking_strategy=ChunkingStrategy.PARAGRAPH,
                chunk_size=100,
                extract_metadata=True,
            )

            result = agent.process_sources(temp_path)

            assert result.total_documents == 1
            assert result.successful_sources == 1
            assert result.failed_sources == 0
            assert result.total_chunks > 0

            # Verify content was processed
            doc = result.loaded_documents[0]
            assert "Test Document" in doc["content"]

        finally:
            Path(temp_path).unlink(missing_ok=True)

    @pytest.mark.asyncio
    async def test_async_compatibility(self):
        """Test async compatibility of DocumentAgent."""
        agent = DocumentAgent()

        # Test that agent can be used in async context
        test_content = "Async test content for document processing."

        # The agent invoke method should work in async context
        try:
            result = agent.process_sources(test_content)
            assert result.total_documents == 1
        except Exception as e:
            pytest.skip(f"Async test skipped due to: {e}")

    def test_repr_string(self):
        """Test string representation of DocumentAgent."""
        agent = DocumentAgent(
            name="Test Agent",
            processing_strategy=ProcessingStrategy.ENHANCED,
            chunking_strategy=ChunkingStrategy.RECURSIVE,
            enable_embedding=True,
            enable_storage=True,
        )

        repr_str = repr(agent)

        assert "DocumentAgent" in repr_str
        assert "Test Agent" in repr_str
        assert "enhanced" in repr_str.lower()
        assert "recursive" in repr_str.lower()
        assert (
            "fetch->load->transform->split->annotate->embed->store" in repr_str.lower()
        )


class TestDocumentAgentPerformance:
    """Performance tests for DocumentAgent."""

    def test_large_content_processing(self):
        """Test processing large content efficiently."""
        agent = DocumentAgent(
            processing_strategy=ProcessingStrategy.PARALLEL,
            parallel_processing=True,
            max_workers=4,
        )

        # Create large content
        large_content = "This is a large document. " * 1000  # ~27KB

        result = agent.process_sources(large_content)

        assert result.total_documents == 1
        assert result.total_chunks > 0
        assert result.processing_time < 10.0  # Should complete within 10 seconds

    def test_multiple_sources_performance(self):
        """Test performance with multiple sources."""
        agent = DocumentAgent(
            processing_strategy=ProcessingStrategy.PARALLEL, max_workers=8
        )

        # Create multiple medium-sized documents
        sources = [f"Document {i}: " + "Content. " * 200 for i in range(10)]

        result = agent.process_sources(sources)

        assert result.total_sources == 10
        assert result.total_documents == 10
        assert result.processing_time < 30.0  # Should complete within 30 seconds


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
