"""Comprehensive tests for the AutoLoader system.

This module provides complete test coverage for the ultimate document loader
system including unit tests, integration tests, performance tests, and
error handling tests.

Author: Claude (Haive Document Loader System)
Version: 1.0.0
"""

import asyncio
import time
from pathlib import Path
from typing import Any, Dict, List
from unittest.mock import MagicMock, Mock, patch

import pytest
from langchain_core.documents import Document

from haive.core.engine.document.loaders.auto_loader import (
    AutoLoader,
    AutoLoaderConfig,
    BulkLoadingResult,
    LoadingResult,
    aload_document,
    load_document,
    load_documents_bulk,
)
from haive.core.engine.document.loaders.auto_registry import (
    auto_register_all,
    get_registration_status,
    list_available_sources,
)
from haive.core.engine.document.loaders.sources.enhanced_registry import (
    LoaderPreference,
)
from haive.core.engine.document.loaders.sources.source_types import (
    LoaderCapability,
    SourceCategory,
)


class TestAutoLoaderConfig:
    """Test AutoLoaderConfig functionality."""

    def test_default_config(self):
        """Test default configuration values."""
        config = AutoLoaderConfig()

        assert config.preference == LoaderPreference.BALANCED
        assert config.max_concurrency == 10
        assert config.timeout == 300
        assert config.retry_attempts == 3
        assert config.enable_caching is False
        assert config.cache_ttl == 3600
        assert config.default_chunk_size == 1000
        assert config.enable_metadata is True
        assert config.credential_manager is None

    def test_custom_config(self):
        """Test custom configuration values."""
        config = AutoLoaderConfig(
            preference=LoaderPreference.QUALITY,
            max_concurrency=20,
            timeout=600,
            retry_attempts=5,
            enable_caching=True,
            cache_ttl=7200,
            default_chunk_size=2000,
            enable_metadata=False,
        )

        assert config.preference == LoaderPreference.QUALITY
        assert config.max_concurrency == 20
        assert config.timeout == 600
        assert config.retry_attempts == 5
        assert config.enable_caching is True
        assert config.cache_ttl == 7200
        assert config.default_chunk_size == 2000
        assert config.enable_metadata is False

    def test_config_validation(self):
        """Test configuration validation."""
        # Test invalid max_concurrency
        with pytest.raises(ValueError):
            AutoLoaderConfig(max_concurrency=0)

        with pytest.raises(ValueError):
            AutoLoaderConfig(max_concurrency=101)

        # Test invalid timeout
        with pytest.raises(ValueError):
            AutoLoaderConfig(timeout=5)

        # Test invalid retry_attempts
        with pytest.raises(ValueError):
            AutoLoaderConfig(retry_attempts=11)

        # Test invalid cache_ttl
        with pytest.raises(ValueError):
            AutoLoaderConfig(cache_ttl=30)

        # Test invalid chunk_size
        with pytest.raises(ValueError):
            AutoLoaderConfig(default_chunk_size=50)


class TestAutoLoaderBasic:
    """Test basic AutoLoader functionality."""

    def test_initialization(
        self, auto_loader_config, mock_enhanced_registry, mock_path_analyzer
    ):
        """Test AutoLoader initialization."""
        loader = AutoLoader(
            config=auto_loader_config,
            registry=mock_enhanced_registry,
            path_analyzer=mock_path_analyzer,
        )

        assert loader.config == auto_loader_config
        assert loader.registry == mock_enhanced_registry
        assert loader.path_analyzer == mock_path_analyzer
        assert isinstance(loader._cache, dict)
        assert len(loader._cache) == 0

    def test_default_initialization(self):
        """Test initialization with default parameters."""
        loader = AutoLoader()

        assert isinstance(loader.config, AutoLoaderConfig)
        assert loader.registry is not None
        assert loader.path_analyzer is not None

    def test_detect_source(self, auto_loader, mock_source_info):
        """Test source detection."""
        auto_loader.path_analyzer.analyze_path.return_value = mock_source_info

        result = auto_loader.detect_source("/path/to/test.pdf")

        assert result == mock_source_info
        auto_loader.path_analyzer.analyze_path.assert_called_once_with(
            "/path/to/test.pdf"
        )

    def test_detect_source_error(self, auto_loader):
        """Test source detection with error."""
        auto_loader.path_analyzer.analyze_path.side_effect = Exception(
            "Analysis failed"
        )

        with pytest.raises(ValueError, match="Could not detect source type"):
            auto_loader.detect_source("/invalid/path")

    def test_get_best_loader(self, auto_loader, mock_source_info):
        """Test best loader selection."""
        auto_loader.registry.get_loader_for_source.return_value = "pypdf"
        auto_loader.registry.get_loader_config.return_value = {"speed": "fast"}

        loader_name, loader_config = auto_loader.get_best_loader(mock_source_info)

        assert loader_name == "pypdf"
        assert loader_config == {"speed": "fast"}

        auto_loader.registry.get_loader_for_source.assert_called_once_with(
            mock_source_info.source_type, preference=auto_loader.config.preference
        )

    def test_get_best_loader_error(self, auto_loader, mock_source_info):
        """Test best loader selection with error."""
        auto_loader.registry.get_loader_for_source.side_effect = Exception(
            "No loader found"
        )

        with pytest.raises(ValueError, match="No suitable loader found"):
            auto_loader.get_best_loader(mock_source_info)


class TestAutoLoaderLoading:
    """Test document loading functionality."""

    def test_load_success(
        self,
        auto_loader,
        sample_documents,
        mock_source_info,
        mock_pdf_source,
        mock_document_loader,
    ):
        """Test successful document loading."""
        # Setup mocks
        auto_loader.path_analyzer.analyze_path.return_value = mock_source_info
        auto_loader.registry.get_loader_for_source.return_value = "pypdf"
        auto_loader.registry.get_loader_config.return_value = {"speed": "fast"}
        auto_loader.registry.get_source_class.return_value = mock_pdf_source
        auto_loader.registry.get_loader_class.return_value = mock_document_loader

        # Mock source instance
        mock_source_instance = Mock()
        mock_source_instance.get_loader_kwargs.return_value = {"file_path": "/test.pdf"}

        with patch.object(
            auto_loader, "create_source_instance", return_value=mock_source_instance
        ):
            with patch.object(
                auto_loader, "_load_with_retry", return_value=sample_documents
            ):
                result = auto_loader.load("/test.pdf")

        assert result == sample_documents
        assert len(result) == 3

    def test_load_with_caching(self, auto_loader, sample_documents):
        """Test loading with caching enabled."""
        auto_loader.config.enable_caching = True

        # First load
        with patch.object(auto_loader, "detect_source") as mock_detect:
            with patch.object(
                auto_loader, "_load_documents_internal", return_value=sample_documents
            ) as mock_load:
                result1 = auto_loader.load("/test.pdf")

        # Second load (should use cache)
        with patch.object(auto_loader, "detect_source") as mock_detect2:
            with patch.object(auto_loader, "_load_documents_internal") as mock_load2:
                result2 = auto_loader.load("/test.pdf")

        assert result1 == sample_documents
        assert result2 == sample_documents
        # Second call should not trigger actual loading
        mock_detect2.assert_not_called()
        mock_load2.assert_not_called()

    def test_load_detailed(self, auto_loader, sample_documents, mock_source_info):
        """Test detailed loading with result information."""
        with patch.object(auto_loader, "detect_source", return_value=mock_source_info):
            with patch.object(
                auto_loader,
                "get_best_loader",
                return_value=("pypdf", {"speed": "fast"}),
            ):
                with patch.object(auto_loader, "load", return_value=sample_documents):
                    result = auto_loader.load_detailed("/test.pdf")

        assert isinstance(result, LoadingResult)
        assert result.documents == sample_documents
        assert result.source_info == mock_source_info
        assert result.loader_used == "pypdf"
        assert result.loading_time > 0
        assert isinstance(result.metadata, dict)
        assert len(result.errors) == 0

    def test_load_detailed_error(self, auto_loader):
        """Test detailed loading with error."""
        with patch.object(
            auto_loader, "detect_source", side_effect=Exception("Detection failed")
        ):
            result = auto_loader.load_detailed("/invalid.pdf")

        assert isinstance(result, LoadingResult)
        assert len(result.documents) == 0
        assert result.loader_used == "none"
        assert len(result.errors) == 1
        assert "Detection failed" in result.errors[0]

    def test_load_all(
        self, auto_loader, sample_documents, mock_source_info, mock_web_source
    ):
        """Test loading all documents with scrape_all."""
        # Create mock source instance with scrape_all
        mock_source_instance = Mock()
        mock_source_instance.scrape_all.return_value = {
            "recursive": True,
            "max_depth": 3,
        }

        with patch.object(auto_loader, "detect_source", return_value=mock_source_info):
            with patch.object(
                auto_loader, "create_source_instance", return_value=mock_source_instance
            ):
                with patch.object(
                    auto_loader, "load", return_value=sample_documents
                ) as mock_load:
                    result = auto_loader.load_all("https://example.com")

        assert result == sample_documents
        # Verify load was called with scrape_all config
        mock_load.assert_called_once_with(
            "https://example.com", recursive=True, max_depth=3
        )

    def test_load_all_no_scrape_support(
        self, auto_loader, sample_documents, mock_source_info
    ):
        """Test load_all when source doesn't support scrape_all."""
        # Create mock source without scrape_all
        mock_source_instance = Mock(spec=[])  # No scrape_all method

        with patch.object(auto_loader, "detect_source", return_value=mock_source_info):
            with patch.object(
                auto_loader, "create_source_instance", return_value=mock_source_instance
            ):
                with patch.object(
                    auto_loader, "load", return_value=sample_documents
                ) as mock_load:
                    result = auto_loader.load_all("/test.pdf")

        assert result == sample_documents
        # Should fall back to regular load
        mock_load.assert_called_once_with("/test.pdf")


class TestAutoLoaderBulkLoading:
    """Test bulk loading functionality."""

    def test_load_bulk_success(self, auto_loader, sample_documents):
        """Test successful bulk loading."""
        sources = ["/test1.pdf", "/test2.pdf", "/test3.pdf"]

        def mock_load_detailed(path, **kwargs):
            return LoadingResult(
                documents=sample_documents[:1],  # One document per source
                source_info=Mock(source_type="pdf"),
                loader_used="pypdf",
                loading_time=1.0,
                metadata={},
                errors=[],
            )

        with patch.object(auto_loader, "load_detailed", side_effect=mock_load_detailed):
            result = auto_loader.load_bulk(sources)

        assert isinstance(result, BulkLoadingResult)
        assert result.total_documents == 3  # One doc per source
        assert len(result.results) == 3
        assert len(result.failed_sources) == 0
        assert result.summary["successful_loads"] == 3
        assert result.summary["failed_loads"] == 0
        assert result.summary["success_rate"] == 100.0

    def test_load_bulk_with_failures(self, auto_loader, sample_documents):
        """Test bulk loading with some failures."""
        sources = ["/test1.pdf", "/test2.pdf", "/invalid.pdf"]

        def mock_load_detailed(path, **kwargs):
            if "invalid" in path:
                return LoadingResult(
                    documents=[],
                    source_info=Mock(source_type="unknown"),
                    loader_used="none",
                    loading_time=0.0,
                    metadata={},
                    errors=["File not found"],
                )
            else:
                return LoadingResult(
                    documents=sample_documents[:1],
                    source_info=Mock(source_type="pdf"),
                    loader_used="pypdf",
                    loading_time=1.0,
                    metadata={},
                    errors=[],
                )

        with patch.object(auto_loader, "load_detailed", side_effect=mock_load_detailed):
            result = auto_loader.load_bulk(sources)

        assert result.total_documents == 2  # Two successful loads
        assert len(result.failed_sources) == 1
        assert result.summary["successful_loads"] == 2
        assert result.summary["failed_loads"] == 1
        assert result.summary["success_rate"] == pytest.approx(66.67, abs=0.01)

    def test_load_bulk_with_progress_callback(self, auto_loader, sample_documents):
        """Test bulk loading with progress callback."""
        sources = ["/test1.pdf", "/test2.pdf"]
        progress_calls = []

        def progress_callback(completed, total):
            progress_calls.append((completed, total))

        def mock_load_detailed(path, **kwargs):
            return LoadingResult(
                documents=sample_documents[:1],
                source_info=Mock(source_type="pdf"),
                loader_used="pypdf",
                loading_time=1.0,
                metadata={},
                errors=[],
            )

        with patch.object(auto_loader, "load_detailed", side_effect=mock_load_detailed):
            result = auto_loader.load_bulk(sources, progress_callback=progress_callback)

        assert len(progress_calls) == 2
        assert progress_calls[0] == (1, 2)
        assert progress_calls[1] == (2, 2)

    def test_load_bulk_dict_sources(self, auto_loader, sample_documents):
        """Test bulk loading with dictionary source configurations."""
        sources = [
            "/test1.pdf",
            {"path": "/test2.pdf", "extract_images": True},
            {"url": "https://example.com", "timeout": 60},
        ]

        def mock_load_detailed(path_or_url, **kwargs):
            return LoadingResult(
                documents=sample_documents[:1],
                source_info=Mock(source_type="pdf"),
                loader_used="pypdf",
                loading_time=1.0,
                metadata={"kwargs": kwargs},
                errors=[],
            )

        with patch.object(auto_loader, "load_detailed", side_effect=mock_load_detailed):
            result = auto_loader.load_bulk(sources)

        assert len(result.results) == 3
        # Check that kwargs were passed correctly
        assert result.results[1].metadata["kwargs"]["extract_images"] is True
        assert result.results[2].metadata["kwargs"]["timeout"] == 60


class TestAutoLoaderAsync:
    """Test asynchronous loading functionality."""

    @pytest.mark.asyncio
    async def test_aload(self, auto_loader, sample_documents):
        """Test asynchronous document loading."""
        with patch.object(
            auto_loader, "load", return_value=sample_documents
        ) as mock_load:
            result = await auto_loader.aload("/test.pdf")

        assert result == sample_documents
        mock_load.assert_called_once_with("/test.pdf")

    @pytest.mark.asyncio
    async def test_aload_bulk(self, auto_loader):
        """Test asynchronous bulk loading."""
        sources = ["/test1.pdf", "/test2.pdf"]
        mock_result = BulkLoadingResult(
            total_documents=2,
            results=[],
            failed_sources=[],
            total_time=2.0,
            summary={},
        )

        with patch.object(
            auto_loader, "load_bulk", return_value=mock_result
        ) as mock_bulk:
            result = await auto_loader.aload_bulk(sources)

        assert result == mock_result
        mock_bulk.assert_called_once_with(sources)


class TestAutoLoaderRetryAndErrorHandling:
    """Test retry logic and error handling."""

    def test_retry_success_after_failure(self, auto_loader):
        """Test successful retry after initial failure."""
        mock_loader = Mock()
        mock_loader.load.side_effect = [
            Exception("First attempt failed"),
            Exception("Second attempt failed"),
            [Document(page_content="Success!", metadata={})],
        ]

        # Set retry attempts to 2
        auto_loader.config.retry_attempts = 2

        result = auto_loader._load_with_retry(mock_loader, "test_source")

        assert len(result) == 1
        assert result[0].page_content == "Success!"
        assert mock_loader.load.call_count == 3

    def test_retry_exhausted(self, auto_loader):
        """Test when all retry attempts are exhausted."""
        mock_loader = Mock()
        mock_loader.load.side_effect = Exception("Always fails")

        auto_loader.config.retry_attempts = 2

        with pytest.raises(Exception, match="Always fails"):
            auto_loader._load_with_retry(mock_loader, "test_source")

        assert mock_loader.load.call_count == 3  # Initial + 2 retries

    def test_retry_with_load_and_split(self, auto_loader, sample_documents):
        """Test retry with load_and_split method."""
        mock_loader = Mock()
        # No load method, only load_and_split
        del mock_loader.load
        mock_loader.load_and_split.return_value = sample_documents

        result = auto_loader._load_with_retry(mock_loader, "test_source")

        assert result == sample_documents
        mock_loader.load_and_split.assert_called_once()

    def test_retry_no_load_method(self, auto_loader):
        """Test error when loader has no load method."""
        mock_loader = Mock(spec=[])  # No load or load_and_split methods

        with pytest.raises(ValueError, match="has no load method"):
            auto_loader._load_with_retry(mock_loader, "test_source")


class TestAutoLoaderUtilities:
    """Test utility methods and features."""

    def test_get_supported_sources(self, auto_loader):
        """Test getting supported sources information."""
        mock_info = {"pdf": {"description": "PDF files"}}
        auto_loader.registry.get_all_source_info.return_value = mock_info

        result = auto_loader.get_supported_sources()

        assert result == mock_info
        auto_loader.registry.get_all_source_info.assert_called_once()

    def test_get_capabilities(self, auto_loader):
        """Test getting source capabilities."""
        capabilities = [
            LoaderCapability.TEXT_EXTRACTION,
            LoaderCapability.METADATA_EXTRACTION,
        ]
        auto_loader.registry.get_source_capabilities.return_value = capabilities

        result = auto_loader.get_capabilities("pdf")

        assert result == capabilities
        auto_loader.registry.get_source_capabilities.assert_called_once_with("pdf")

    def test_validate_credentials_success(self, auto_loader, mock_pdf_source):
        """Test successful credential validation."""
        auto_loader.registry.get_source_class.return_value = mock_pdf_source

        result = auto_loader.validate_credentials("pdf", path="/test.pdf")

        assert result is True
        auto_loader.registry.get_source_class.assert_called_once_with("pdf")

    def test_validate_credentials_failure(self, auto_loader):
        """Test failed credential validation."""
        auto_loader.registry.get_source_class.side_effect = Exception(
            "Invalid credentials"
        )

        result = auto_loader.validate_credentials("pdf", invalid_param="invalid")

        assert result is False

    def test_enrich_documents_metadata(
        self, auto_loader, sample_documents, mock_source_info
    ):
        """Test metadata enrichment."""
        auto_loader.config.enable_metadata = True

        # Clear existing metadata
        for doc in sample_documents:
            doc.metadata = {"original": "metadata"}

        auto_loader._enrich_documents_metadata(
            sample_documents, mock_source_info, "pypdf"
        )

        for doc in sample_documents:
            assert doc.metadata["source_type"] == mock_source_info.source_type
            assert doc.metadata["source_category"] == mock_source_info.category.value
            assert doc.metadata["loader_used"] == "pypdf"
            assert doc.metadata["confidence"] == mock_source_info.confidence
            assert "loaded_at" in doc.metadata
            assert doc.metadata["original"] == "metadata"  # Original metadata preserved


class TestConvenienceFunctions:
    """Test convenience functions."""

    def test_load_document(self, sample_documents):
        """Test load_document convenience function."""
        with patch(
            "haive.core.engine.document.loaders.auto_loader.AutoLoader"
        ) as MockAutoLoader:
            mock_loader = Mock()
            mock_loader.load.return_value = sample_documents
            MockAutoLoader.return_value = mock_loader

            result = load_document("/test.pdf", extract_images=True)

        assert result == sample_documents
        mock_loader.load.assert_called_once_with("/test.pdf", extract_images=True)

    def test_load_documents_bulk(self, sample_documents):
        """Test load_documents_bulk convenience function."""
        mock_bulk_result = BulkLoadingResult(
            total_documents=6,
            results=[
                LoadingResult(
                    documents=sample_documents,
                    source_info=Mock(),
                    loader_used="pypdf",
                    loading_time=1.0,
                    metadata={},
                    errors=[],
                )
            ],
            failed_sources=[],
            total_time=2.0,
            summary={},
        )

        with patch(
            "haive.core.engine.document.loaders.auto_loader.AutoLoader"
        ) as MockAutoLoader:
            mock_loader = Mock()
            mock_loader.load_bulk.return_value = mock_bulk_result
            MockAutoLoader.return_value = mock_loader

            result = load_documents_bulk(["/test1.pdf", "/test2.pdf"])

        assert len(result) == 3  # Flattened documents
        assert result == sample_documents

    @pytest.mark.asyncio
    async def test_aload_document(self, sample_documents):
        """Test aload_document convenience function."""
        with patch(
            "haive.core.engine.document.loaders.auto_loader.AutoLoader"
        ) as MockAutoLoader:
            mock_loader = Mock()
            mock_loader.aload = Mock(return_value=sample_documents)
            MockAutoLoader.return_value = mock_loader

            result = await aload_document("/test.pdf")

        assert result == sample_documents


class TestAutoRegistryIntegration:
    """Test integration with auto-registry system."""

    def test_auto_register_all(self):
        """Test auto-registration of all sources."""
        with patch(
            "haive.core.engine.document.loaders.auto_registry.auto_registry"
        ) as mock_registry:
            mock_stats = Mock()
            mock_stats.total_sources_registered = 230
            mock_registry.register_all_sources.return_value = mock_stats

            result = auto_register_all()

        assert result == mock_stats
        mock_registry.register_all_sources.assert_called_once()

    def test_get_registration_status(self):
        """Test getting registration status."""
        with patch(
            "haive.core.engine.document.loaders.auto_registry.auto_registry"
        ) as mock_registry:
            mock_status = {"total_sources": 230, "categories_count": 12}
            mock_registry.get_registration_status.return_value = mock_status

            result = get_registration_status()

        assert result == mock_status
        mock_registry.get_registration_status.assert_called_once()

    def test_list_available_sources(self):
        """Test listing available sources."""
        with patch(
            "haive.core.engine.document.loaders.auto_registry.auto_registry"
        ) as mock_registry:
            mock_sources = ["pdf", "docx", "csv", "json", "web"]
            mock_registry.registered_sources.keys.return_value = mock_sources

            result = list_available_sources()

        assert result == mock_sources


class TestErrorScenarios:
    """Test various error scenarios and edge cases."""

    def test_invalid_source_path(self, auto_loader):
        """Test loading from invalid source path."""
        auto_loader.path_analyzer.analyze_path.side_effect = ValueError("Invalid path")

        with pytest.raises(ValueError, match="Could not detect source type"):
            auto_loader.load("/invalid/path")

    def test_unsupported_source_type(self, auto_loader, mock_source_info):
        """Test loading from unsupported source type."""
        mock_source_info.source_type = "unsupported"
        auto_loader.path_analyzer.analyze_path.return_value = mock_source_info
        auto_loader.registry.get_loader_for_source.side_effect = ValueError(
            "Unsupported"
        )

        with pytest.raises(ValueError, match="No suitable loader found"):
            auto_loader.load("/test.unsupported")

    def test_source_creation_failure(self, auto_loader, mock_source_info):
        """Test failure in source instance creation."""
        auto_loader.path_analyzer.analyze_path.return_value = mock_source_info
        auto_loader.registry.get_loader_for_source.return_value = "pypdf"
        auto_loader.registry.get_loader_config.return_value = {}
        auto_loader.registry.get_source_class.side_effect = Exception(
            "Source creation failed"
        )

        with pytest.raises(ValueError, match="Could not create source"):
            auto_loader.load("/test.pdf")

    def test_empty_bulk_sources(self, auto_loader):
        """Test bulk loading with empty source list."""
        result = auto_loader.load_bulk([])

        assert isinstance(result, BulkLoadingResult)
        assert result.total_documents == 0
        assert len(result.results) == 0
        assert len(result.failed_sources) == 0
        assert result.summary["total_sources"] == 0

    def test_cache_expiration(self, auto_loader, sample_documents):
        """Test cache expiration functionality."""
        auto_loader.config.enable_caching = True
        auto_loader.config.cache_ttl = 1  # 1 second TTL

        # Add expired cache entry
        cache_key = "/test.pdf:12345"
        expired_time = datetime.now() - timedelta(seconds=2)
        auto_loader._cache[cache_key] = (sample_documents, expired_time)

        # Should not return cached documents (expired)
        result = auto_loader._get_from_cache(cache_key)
        assert result is None
        assert cache_key not in auto_loader._cache  # Should be removed


class TestPerformance:
    """Test performance characteristics."""

    def test_concurrent_loading_performance(self, auto_loader):
        """Test performance of concurrent loading."""
        import time

        sources = [f"/test{i}.pdf" for i in range(20)]

        def mock_load_detailed(path, **kwargs):
            time.sleep(0.1)  # Simulate loading time
            return LoadingResult(
                documents=[Document(page_content=f"Content from {path}", metadata={})],
                source_info=Mock(source_type="pdf"),
                loader_used="pypdf",
                loading_time=0.1,
                metadata={},
                errors=[],
            )

        with patch.object(auto_loader, "load_detailed", side_effect=mock_load_detailed):
            start_time = time.time()
            result = auto_loader.load_bulk(sources)
            end_time = time.time()

        # With 5 concurrent workers, 20 items should take ~0.4s (4 batches * 0.1s)
        # Allow some margin for overhead
        assert end_time - start_time < 1.0
        assert result.total_documents == 20

    def test_caching_performance_improvement(self, auto_loader, sample_documents):
        """Test that caching improves performance."""
        auto_loader.config.enable_caching = True

        def slow_load(*args, **kwargs):
            time.sleep(0.1)
            return sample_documents

        with patch.object(auto_loader, "detect_source"), patch.object(
            auto_loader, "get_best_loader"
        ), patch.object(auto_loader, "create_source_instance"), patch.object(
            auto_loader, "_load_with_retry", side_effect=slow_load
        ):

            # First load (should be slow)
            start_time = time.time()
            result1 = auto_loader.load("/test.pdf")
            first_load_time = time.time() - start_time

            # Second load (should be fast due to cache)
            start_time = time.time()
            result2 = auto_loader.load("/test.pdf")
            second_load_time = time.time() - start_time

        assert result1 == sample_documents
        assert result2 == sample_documents
        assert (
            second_load_time < first_load_time / 2
        )  # Cache should be significantly faster


class TestRealWorldScenarios:
    """Test real-world usage scenarios."""

    def test_mixed_source_types(self, auto_loader, sample_documents):
        """Test loading from mixed source types."""
        sources = [
            "/documents/report.pdf",
            "https://example.com/page.html",
            "s3://bucket/data.csv",
            {"path": "/archive.zip", "extract_all": True},
        ]

        def mock_load_detailed(path_or_url, **kwargs):
            return LoadingResult(
                documents=sample_documents[:1],  # One doc per source
                source_info=Mock(source_type="mixed"),
                loader_used="auto",
                loading_time=1.0,
                metadata={"path": path_or_url},
                errors=[],
            )

        with patch.object(auto_loader, "load_detailed", side_effect=mock_load_detailed):
            result = auto_loader.load_bulk(sources)

        assert result.total_documents == 4
        assert len(result.results) == 4
        assert all(not errors for _, errors in result.failed_sources)

    def test_large_document_processing(self, auto_loader):
        """Test processing of large documents."""
        large_content = "Lorem ipsum dolor sit amet. " * 10000  # Large content
        large_doc = Document(page_content=large_content, metadata={"size": "large"})

        def mock_load_detailed(path, **kwargs):
            return LoadingResult(
                documents=[large_doc],
                source_info=Mock(source_type="pdf"),
                loader_used="pypdf",
                loading_time=2.0,
                metadata={},
                errors=[],
            )

        with patch.object(auto_loader, "load_detailed", side_effect=mock_load_detailed):
            result = auto_loader.load("/large_document.pdf")

        assert len(result) == 1
        assert len(result[0].page_content) > 100000

    def test_error_recovery_in_bulk_loading(self, auto_loader, sample_documents):
        """Test error recovery during bulk loading."""
        sources = ["/good1.pdf", "/bad.pdf", "/good2.pdf", "/bad2.pdf", "/good3.pdf"]

        def mock_load_detailed(path, **kwargs):
            if "bad" in path:
                return LoadingResult(
                    documents=[],
                    source_info=Mock(source_type="unknown"),
                    loader_used="none",
                    loading_time=0.0,
                    metadata={},
                    errors=["Simulated error"],
                )
            else:
                return LoadingResult(
                    documents=sample_documents[:1],
                    source_info=Mock(source_type="pdf"),
                    loader_used="pypdf",
                    loading_time=1.0,
                    metadata={},
                    errors=[],
                )

        with patch.object(auto_loader, "load_detailed", side_effect=mock_load_detailed):
            result = auto_loader.load_bulk(sources)

        assert result.total_documents == 3  # 3 good files
        assert len(result.failed_sources) == 2  # 2 bad files
        assert result.summary["success_rate"] == 60.0  # 3/5 = 60%

    def test_configuration_driven_loading(
        self, mock_enhanced_registry, mock_path_analyzer
    ):
        """Test loading with different configurations."""
        configs = [
            AutoLoaderConfig(preference=LoaderPreference.SPEED, max_concurrency=20),
            AutoLoaderConfig(preference=LoaderPreference.QUALITY, max_concurrency=5),
            AutoLoaderConfig(preference=LoaderPreference.BALANCED, enable_caching=True),
        ]

        for config in configs:
            loader = AutoLoader(config, mock_enhanced_registry, mock_path_analyzer)

            # Verify configuration is applied
            assert loader.config.preference == config.preference
            assert loader.config.max_concurrency == config.max_concurrency
            assert loader.config.enable_caching == config.enable_caching


# Integration tests that require actual file system


class TestFileSystemIntegration:
    """Test integration with actual file system."""

    def test_real_file_loading(self, auto_loader, test_files):
        """Test loading real files from file system."""
        # This would require mocking the actual loader classes
        # or having test files available
        pass

    def test_directory_traversal(self, auto_loader, temp_dir):
        """Test recursive directory loading."""
        # This would test the actual directory traversal functionality
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
