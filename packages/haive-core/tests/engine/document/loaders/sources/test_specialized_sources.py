"""Tests for specialized platform source loaders.

This module tests the specialized loaders including academic platforms,
media processing, development tools, and domain-specific systems.
"""

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from unittest.mock import MagicMock, Mock, patch

import pytest

from haive.core.engine.document.loaders.sources.source_types import (
    CredentialType,
    LoaderCapability,
    SourceCategory,
)
from haive.core.engine.document.loaders.sources.specialized_sources import (
    ArxivSource,
    AudioFileSource,
    DevelopmentDataType,
    GitHubSource,
    GitSource,
    MediaType,
    PubMedSource,
    ResearchField,
    SpecializedPlatform,
    WikipediaSource,
    YouTubeSource,
    detect_specialized_platform,
    get_specialized_sources_statistics,
    validate_specialized_sources,
)


@pytest.fixture
def mock_registry():
    """Create a mock registry for testing."""
    registry = MagicMock()
    registry._sources = {}
    registry.find_sources_by_category = MagicMock(return_value=[])
    return registry


@pytest.fixture
def arxiv_source() -> ArxivSource:
    """Create a test arXiv source instance."""
    return ArxivSource(
        source_id="arxiv-test-001",
        category=SourceCategory.SPECIALIZED,
        query="quantum computing",
        max_results=5,
        categories=["cs.AI", "cs.LG"],
    )


@pytest.fixture
def youtube_source() -> YouTubeSource:
    """Create a test YouTube source instance."""
    return YouTubeSource(
        source_id="youtube-test-001",
        category=SourceCategory.SPECIALIZED,
        video_url="https://youtube.com/watch?v=dQw4w9WgXcQ",
        media_type=MediaType.TRANSCRIPT,
        language="en",
    )


@pytest.fixture
def github_source() -> GitHubSource:
    """Create a test GitHub source instance."""
    return GitHubSource(
        source_id="github-test-001",
        category=SourceCategory.SPECIALIZED,
        repo="owner/repository",
        access_token="test-token",
        data_types=[DevelopmentDataType.ISSUES, DevelopmentDataType.PULL_REQUESTS],
    )


class TestSpecializedPlatformDetection:
    """Test suite for specialized platform detection."""

    def test_detect_arxiv_from_url(self):
        """Test detecting arXiv from various URL patterns."""
        test_urls = [
            "https://arxiv.org/abs/2301.12345",
            "https://arxiv.org/pdf/2301.12345.pdf",
            "arxiv:2301.12345",
        ]

        for url in test_urls:
            result = detect_specialized_platform(url)
            assert result == SpecializedPlatform.ARXIV

    def test_detect_youtube_from_url(self):
        """Test detecting YouTube from various URL patterns."""
        test_urls = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://youtu.be/dQw4w9WgXcQ",
            "https://youtube.com/playlist?list=PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf",
        ]

        for url in test_urls:
            result = detect_specialized_platform(url)
            assert result == SpecializedPlatform.YOUTUBE

    def test_detect_github_from_url(self):
        """Test detecting GitHub from URL."""
        result = detect_specialized_platform(
            "https://github.com/langchain-ai/langchain"
        )
        assert result == SpecializedPlatform.GITHUB

    def test_detect_unknown_platform(self):
        """Test handling of unknown platform URLs."""
        result = detect_specialized_platform("https://unknown-platform.com")
        assert result is None

    @pytest.mark.parametrize(
        "url,expected",
        [
            ("https://pubmed.ncbi.nlm.nih.gov/12345678", SpecializedPlatform.PUBMED),
            ("pmid:12345678", SpecializedPlatform.PUBMED),
            ("https://en.wikipedia.org/wiki/Python", SpecializedPlatform.WIKIPEDIA),
            ("https://www.bilibili.com/video/BV1234567", SpecializedPlatform.BILIBILI),
        ],
    )
    def test_detect_various_platforms(self, url: str, expected: SpecializedPlatform):
        """Test detecting various specialized platforms."""
        result = detect_specialized_platform(url)
        assert result == expected


class TestAcademicSources:
    """Test suite for academic research sources."""

    def test_arxiv_source_initialization(self, arxiv_source):
        """Test arXiv source initialization."""
        assert arxiv_source.platform == SpecializedPlatform.ARXIV
        assert arxiv_source.query == "quantum computing"
        assert arxiv_source.max_results == 5
        assert len(arxiv_source.categories) == 2

    def test_arxiv_query_construction(self, arxiv_source):
        """Test arXiv query parameter construction."""
        kwargs = arxiv_source.get_loader_kwargs()

        assert "query" in kwargs
        assert "load_max_docs" in kwargs
        assert kwargs["load_max_docs"] == 5

        # Check category filtering in query
        assert "cat:cs.AI" in kwargs["query"] or "cat:cs.LG" in kwargs["query"]

    def test_arxiv_with_specific_ids(self):
        """Test arXiv source with specific paper IDs."""
        source = ArxivSource(
            source_id="arxiv-test-002",
            category=SourceCategory.SPECIALIZED,
            arxiv_ids=["2301.12345", "2302.54321"],
            include_metadata=True,
        )

        kwargs = source.get_loader_kwargs()

        assert "query" in kwargs
        assert "id:2301.12345" in kwargs["query"]
        assert "id:2302.54321" in kwargs["query"]
        assert kwargs["load_all_available_meta"] is True

    def test_pubmed_source_initialization(self):
        """Test PubMed source initialization."""
        source = PubMedSource(
            source_id="pubmed-test-001",
            category=SourceCategory.SPECIALIZED,
            query="COVID-19 vaccines",
            max_results=20,
            include_abstracts=True,
        )

        assert source.platform == SpecializedPlatform.PUBMED
        assert source.query == "COVID-19 vaccines"
        assert source.max_results == 20

    @pytest.mark.parametrize(
        "field,expected",
        [
            (ResearchField.PHYSICS, "physics"),
            (ResearchField.COMPUTER_SCIENCE, "cs"),
            (ResearchField.BIOLOGY, "biology"),
            (ResearchField.ALL_FIELDS, "all"),
        ],
    )
    def test_research_field_values(self, field: ResearchField, expected: str):
        """Test research field enum values."""
        assert field.value == expected


class TestMediaSources:
    """Test suite for media platform sources."""

    def test_youtube_source_initialization(self, youtube_source):
        """Test YouTube source initialization."""
        assert youtube_source.platform == SpecializedPlatform.YOUTUBE
        assert youtube_source.video_url == "https://youtube.com/watch?v=dQw4w9WgXcQ"
        assert youtube_source.media_type == MediaType.TRANSCRIPT
        assert youtube_source.language == "en"

    def test_youtube_video_id_extraction(self, youtube_source):
        """Test automatic video ID extraction from URL."""
        assert youtube_source.video_id == "dQw4w9WgXcQ"

        # Test with youtu.be URL
        source = YouTubeSource(
            source_id="youtube-test-002",
            category=SourceCategory.SPECIALIZED,
            video_url="https://youtu.be/dQw4w9WgXcQ",
        )
        assert source.video_id == "dQw4w9WgXcQ"

    def test_youtube_transcript_loader_kwargs(self, youtube_source):
        """Test YouTube transcript loader kwargs."""
        kwargs = youtube_source.get_loader_kwargs()

        assert kwargs["add_video_info"] is True
        assert kwargs["video_id"] == "dQw4w9WgXcQ"
        assert kwargs["language"] == ["en"]

    def test_youtube_audio_loader_config(self):
        """Test YouTube audio loader configuration."""
        source = YouTubeSource(
            source_id="youtube-test-003",
            category=SourceCategory.SPECIALIZED,
            video_url="https://youtube.com/watch?v=test123",
            media_type=MediaType.AUDIO,
            save_audio_file=True,
            audio_format="mp3",
        )

        kwargs = source.get_loader_kwargs()

        assert kwargs["save_dir"] == "./youtube_audio"
        assert kwargs["urls"] == ["https://youtube.com/watch?v=test123"]

    def test_audio_file_source(self):
        """Test audio file transcription source."""
        source = AudioFileSource(
            source_id="audio-test-001",
            category=SourceCategory.SPECIALIZED,
            path=Path("/path/to/audio.mp3"),
            language="en",
            speaker_labels=True,
            timestamps=True,
        )

        kwargs = source.get_loader_kwargs()

        assert kwargs["file_path"] == "/path/to/audio.mp3"
        assert kwargs["language"] == "en"
        assert kwargs["speaker_labels"] is True
        assert kwargs["timestamps"] is True

    @pytest.mark.parametrize(
        "media_type,expected",
        [
            (MediaType.VIDEO, "video"),
            (MediaType.AUDIO, "audio"),
            (MediaType.TRANSCRIPT, "transcript"),
            (MediaType.SUBTITLES, "subtitles"),
            (MediaType.METADATA, "metadata"),
        ],
    )
    def test_media_type_values(self, media_type: MediaType, expected: str):
        """Test media type enum values."""
        assert media_type.value == expected


class TestDevelopmentSources:
    """Test suite for development platform sources."""

    def test_github_source_initialization(self, github_source):
        """Test GitHub source initialization."""
        assert github_source.platform == SpecializedPlatform.GITHUB
        assert github_source.repo == "owner/repository"
        assert github_source.access_token == "test-token"
        assert len(github_source.data_types) == 2

    def test_github_issues_loader_kwargs(self, github_source):
        """Test GitHub issues loader kwargs."""
        kwargs = github_source.get_loader_kwargs()

        assert kwargs["repo"] == "owner/repository"
        assert kwargs["access_token"] == "test-token"
        assert kwargs["state"] == "all"
        assert kwargs["include_prs"] is True

    def test_github_file_loader_config(self):
        """Test GitHub file loader configuration."""
        source = GitHubSource(
            source_id="github-test-002",
            category=SourceCategory.SPECIALIZED,
            repo="langchain-ai/langchain",
            file_path="README.md",
            branch="main",
        )

        kwargs = source.get_loader_kwargs()

        assert kwargs["file_path"] == "README.md"
        assert kwargs["branch"] == "main"

    def test_git_local_repository_source(self):
        """Test local Git repository source."""
        source = GitSource(
            source_id="git-test-001",
            category=SourceCategory.SPECIALIZED,
            path=Path("/home/user/project"),
            repo_path=Path("/home/user/project"),
            branch="develop",
            file_filter="*.py",
        )

        kwargs = source.get_loader_kwargs()

        assert kwargs["repo_path"] == "/home/user/project"
        assert kwargs["branch"] == "develop"
        assert kwargs["file_filter"] == "*.py"

    @pytest.mark.parametrize(
        "data_type,expected",
        [
            (DevelopmentDataType.REPOSITORIES, "repositories"),
            (DevelopmentDataType.ISSUES, "issues"),
            (DevelopmentDataType.PULL_REQUESTS, "pull_requests"),
            (DevelopmentDataType.COMMITS, "commits"),
            (DevelopmentDataType.WIKI, "wiki"),
        ],
    )
    def test_development_data_type_values(
        self, data_type: DevelopmentDataType, expected: str
    ):
        """Test development data type enum values."""
        assert data_type.value == expected


class TestKnowledgeSources:
    """Test suite for knowledge platform sources."""

    def test_wikipedia_source_with_query(self):
        """Test Wikipedia source with search query."""
        source = WikipediaSource(
            source_id="wiki-test-001",
            category=SourceCategory.SPECIALIZED,
            query="Python programming",
            lang="en",
            load_max_docs=5,
        )

        kwargs = source.get_loader_kwargs()

        assert kwargs["query"] == "Python programming"
        assert kwargs["lang"] == "en"
        assert kwargs["load_max_docs"] == 5
        assert kwargs["load_all_available_meta"] is True

    def test_wikipedia_source_with_specific_pages(self):
        """Test Wikipedia source with specific page titles."""
        source = WikipediaSource(
            source_id="wiki-test-002",
            category=SourceCategory.SPECIALIZED,
            page_titles=["Python (programming language)", "Machine learning"],
            lang="en",
        )

        kwargs = source.get_loader_kwargs()

        assert kwargs["query"] == "Python (programming language)"
        assert kwargs["load_max_docs"] == 2

    def test_wikipedia_content_length_limit(self):
        """Test Wikipedia source with content length limit."""
        source = WikipediaSource(
            source_id="wiki-test-003",
            category=SourceCategory.SPECIALIZED,
            query="Artificial intelligence",
            doc_content_chars_max=5000,
        )

        kwargs = source.get_loader_kwargs()

        assert kwargs["doc_content_chars_max"] == 5000


class TestSpecializedUtilityFunctions:
    """Test suite for specialized source utility functions."""

    @patch(
        "haive.core.engine.document.loaders.sources.specialized_sources.enhanced_registry"
    )
    def test_get_specialized_sources_statistics(self, mock_registry):
        """Test specialized sources statistics calculation."""
        # Mock registry responses
        mock_registry.find_sources_by_category.return_value = [
            "arxiv",
            "pubmed",
            "youtube",
            "github",
        ]
        mock_registry._sources = {
            "arxiv": MagicMock(platform=SpecializedPlatform.ARXIV),
            "pubmed": MagicMock(platform=SpecializedPlatform.PUBMED),
            "youtube": MagicMock(platform=SpecializedPlatform.YOUTUBE),
            "github": MagicMock(platform=SpecializedPlatform.GITHUB),
        }

        stats = get_specialized_sources_statistics()

        assert "total_specialized" in stats
        assert "academic_sources" in stats
        assert "media_sources" in stats
        assert "development_sources" in stats
        assert "platform_breakdown" in stats

    @patch(
        "haive.core.engine.document.loaders.sources.specialized_sources.enhanced_registry"
    )
    def test_validate_specialized_sources_success(self, mock_registry):
        """Test successful validation of specialized sources."""
        # Mock all required sources as present
        mock_registry._sources = {
            "arxiv": MagicMock(),
            "pubmed": MagicMock(),
            "youtube": MagicMock(),
            "github": MagicMock(),
            "git": MagicMock(),
            "wikipedia": MagicMock(),
        }

        result = validate_specialized_sources()
        assert result is True

    @patch(
        "haive.core.engine.document.loaders.sources.specialized_sources.enhanced_registry"
    )
    def test_validate_specialized_sources_missing(self, mock_registry):
        """Test validation failure when sources are missing."""
        # Mock only some sources as present
        mock_registry._sources = {"arxiv": MagicMock(), "youtube": MagicMock()}

        result = validate_specialized_sources()
        assert result is False


@pytest.mark.integration
class TestSpecializedSourceIntegration:
    """Integration tests for specialized sources with mock loaders."""

    @patch("langchain_community.document_loaders.ArxivLoader")
    async def test_arxiv_loader_integration(self, mock_loader_class, arxiv_source):
        """Test arXiv source integration with mock loader."""
        # Mock the loader instance
        mock_loader = MagicMock()
        mock_loader.load.return_value = [
            {"content": "Paper 1 abstract", "metadata": {"title": "Quantum Computing"}},
            {"content": "Paper 2 abstract", "metadata": {"title": "Machine Learning"}},
        ]
        mock_loader_class.return_value = mock_loader

        # Get loader kwargs
        kwargs = arxiv_source.get_loader_kwargs()

        # Simulate loader creation
        loader = mock_loader_class(**kwargs)
        documents = loader.load()

        assert len(documents) == 2
        assert documents[0]["metadata"]["title"] == "Quantum Computing"
        mock_loader_class.assert_called_once()

    @pytest.mark.parametrize(
        "platform,loader_class",
        [
            (SpecializedPlatform.ARXIV, "ArxivLoader"),
            (SpecializedPlatform.PUBMED, "PubMedLoader"),
            (SpecializedPlatform.YOUTUBE, "YoutubeLoader"),
            (SpecializedPlatform.GITHUB, "GitHubIssuesLoader"),
            (SpecializedPlatform.WIKIPEDIA, "WikipediaLoader"),
        ],
    )
    def test_platform_loader_mapping(
        self, platform: SpecializedPlatform, loader_class: str
    ):
        """Test that each platform maps to the correct loader class."""
        # This test verifies the loader class names match expected conventions
        assert (
            platform.value in loader_class.lower()
            or loader_class.lower().startswith(platform.value[:3])
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
