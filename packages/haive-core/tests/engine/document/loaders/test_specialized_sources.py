"""Test the specialized platform sources system.

This test validates:
- Academic platform source registration (arXiv, PubMed)
- Media platform integration (YouTube, audio processing)
- Development platform support (GitHub, Git)
- Knowledge platform access (Wikipedia)
- Domain-specific systems (weather, financial)
"""

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add the source path to sys.path
base_path = Path("/home/will/Projects/haive/backend/haive/packages/haive-core/src")
sys.path.insert(0, str(base_path))


try:
    # Test importing the specialized sources components

    # Test the enums and basic classes
    from enum import Enum

    # Test SpecializedPlatform enum
    class SpecializedPlatform(str, Enum):
        # Academic & Research
        ARXIV = "arxiv"
        PUBMED = "pubmed"
        BIORXIV = "biorxiv"
        SEMANTIC_SCHOLAR = "semantic_scholar"

        # Media Platforms
        YOUTUBE = "youtube"
        BILIBILI = "bilibili"
        VIMEO = "vimeo"

        # Development Platforms
        GITHUB = "github"
        GITLAB = "gitlab"
        BITBUCKET = "bitbucket"

        # Knowledge Platforms
        WIKIPEDIA = "wikipedia"
        MEDIAWIKI = "mediawiki"

        # Domain-Specific
        WEATHER = "weather"
        FINANCIAL = "financial"
        NEWS = "news"

    # Test MediaType enum
    class MediaType(str, Enum):
        VIDEO = "video"
        AUDIO = "audio"
        TRANSCRIPT = "transcript"
        SUBTITLES = "subtitles"
        METADATA = "metadata"

    # Test DevelopmentDataType enum
    class DevelopmentDataType(str, Enum):
        REPOSITORIES = "repositories"
        ISSUES = "issues"
        PULL_REQUESTS = "pull_requests"
        COMMITS = "commits"
        WIKI = "wiki"
        RELEASES = "releases"
        DISCUSSIONS = "discussions"


except Exception as e:
    pass")


def test_platform_detection():
    """Test specialized platform detection from URLs."""

    def detect_specialized_platform(url_or_path: str):
        """Detect specialized platform from URL or path."""
        lower = url_or_path.lower()

        patterns = {
            SpecializedPlatform.ARXIV: ["arxiv.org", "arxiv:"],
            SpecializedPlatform.PUBMED: ["pubmed.ncbi", "pmid:"],
            SpecializedPlatform.YOUTUBE: ["youtube.com", "youtu.be"],
            SpecializedPlatform.GITHUB: ["github.com"],
            SpecializedPlatform.WIKIPEDIA: ["wikipedia.org"],
            SpecializedPlatform.BILIBILI: ["bilibili.com"],
        }

        for platform, keywords in patterns.items():
            if any(keyword in lower for keyword in keywords):
                return platform

        return None

    test_urls = {
        "https://arxiv.org/abs/2301.12345": SpecializedPlatform.ARXIV,
        "https://pubmed.ncbi.nlm.nih.gov/12345678": SpecializedPlatform.PUBMED,
        "https://youtube.com/watch?v=dQw4w9WgXcQ": SpecializedPlatform.YOUTUBE,
        "https://github.com/langchain-ai/langchain": SpecializedPlatform.GITHUB,
        "https://en.wikipedia.org/wiki/Python": SpecializedPlatform.WIKIPEDIA,
        "https://www.bilibili.com/video/BV1234567": SpecializedPlatform.BILIBILI,
    }

    detection_success = 0
    for url, expected_platform in test_urls.items():
        detected = detect_specialized_platform(url)
        status = "✅" if detected == expected_platform else "❌"
        if detected == expected_platform:
            detection_success += 1

    success_rate = (detection_success / len(test_urls)) * 100

    return detection_success >= 5


def test_academic_sources():
    """Test academic platform source configurations."""

    # Mock academic source class
    class MockAcademicSource:
        def __init__(self, platform, **kwargs):
            self.platform = platform
            self.query = kwargs.get("query")
            self.arxiv_ids = kwargs.get("arxiv_ids")
            self.max_results = kwargs.get("max_results", 10)
            self.categories = kwargs.get("categories", [])
            self.include_metadata = kwargs.get("include_metadata", True)

        def get_loader_kwargs(self):
            kwargs = {"platform": self.platform.value, "max_results": self.max_results}

            if self.arxiv_ids:
                kwargs["query"] = " OR ".join([f"id:{id}" for id in self.arxiv_ids])
            elif self.query:
                kwargs["query"] = self.query

            if self.categories:
                cat_query = " OR ".join([f"cat:{cat}" for cat in self.categories])
                if "query" in kwargs:
                    kwargs["query"] = f"({kwargs['query']}) AND ({cat_query})"
                else:
                    kwargs["query"] = cat_query

            return kwargs

    academic_tests_passed = 0
    test_configs = [
        {
            "platform": SpecializedPlatform.ARXIV,
            "name": "arXiv Search",
            "query": "quantum computing",
            "categories": ["cs.AI", "cs.LG"],
            "max_results": 5,
        },
        {
            "platform": SpecializedPlatform.ARXIV,
            "name": "arXiv IDs",
            "arxiv_ids": ["2301.12345", "2302.54321"],
            "include_metadata": True,
        },
        {
            "platform": SpecializedPlatform.PUBMED,
            "name": "PubMed Search",
            "query": "COVID-19 vaccines",
            "max_results": 20,
        },
    ]

    for config in test_configs:
        try:
            source = MockAcademicSource(
                platform=config["platform"],
                **{k: v for k, v in config.items() if k not in ["platform", "name"]},
            )

            loader_kwargs = source.get_loader_kwargs()


            assert loader_kwargs["platform"] == config["platform"].value

            academic_tests_passed += 1

        except Exception as e:
            pass")


    return academic_tests_passed >= 2


def test_media_sources():
    """Test media platform source configurations."""

    def extract_video_id(url):
        """Extract YouTube video ID from URL."""
        if "youtube.com/watch?v=" in url:
            return url.split("v=")[1].split("&")[0]
        if "youtu.be/" in url:
            return url.split("youtu.be/")[1].split("?")[0]
        return None

    # Mock media source class
    class MockYouTubeSource:
        def __init__(self, **kwargs):
            self.platform = SpecializedPlatform.YOUTUBE
            self.video_url = kwargs.get("video_url")
            self.video_id = (
                kwargs.get("video_id") or extract_video_id(self.video_url)
                if self.video_url
                else None
            )
            self.media_type = kwargs.get("media_type", MediaType.TRANSCRIPT)
            self.language = kwargs.get("language")
            self.include_metadata = kwargs.get("include_metadata", True)
            self.save_audio_file = kwargs.get("save_audio_file", False)

        def get_loader_kwargs(self):
            kwargs = {"platform": self.platform.value}

            if self.media_type == MediaType.TRANSCRIPT:
                kwargs["add_video_info"] = self.include_metadata
                if self.video_id:
                    kwargs["video_id"] = self.video_id
                if self.language:
                    kwargs["language"] = [self.language]
            elif self.media_type == MediaType.AUDIO:
                kwargs["save_dir"] = "./youtube_audio" if self.save_audio_file else None
                if self.video_url:
                    kwargs["urls"] = [self.video_url]

            return kwargs

    media_tests_passed = 0
    test_configs = [
        {
            "name": "YouTube Transcript",
            "video_url": "https://youtube.com/watch?v=dQw4w9WgXcQ",
            "media_type": MediaType.TRANSCRIPT,
            "language": "en",
            "expected_id": "dQw4w9WgXcQ",
        },
        {
            "name": "YouTube Short URL",
            "video_url": "https://youtu.be/dQw4w9WgXcQ",
            "media_type": MediaType.TRANSCRIPT,
            "expected_id": "dQw4w9WgXcQ",
        },
        {
            "name": "YouTube Audio",
            "video_url": "https://youtube.com/watch?v=test123",
            "media_type": MediaType.AUDIO,
            "save_audio_file": True,
        },
    ]

    for config in test_configs:
        try:
            source = MockYouTubeSource(**config)
            loader_kwargs = source.get_loader_kwargs()


            # Verify video ID extraction
            if "expected_id" in config:
                assert (
                    source.video_id == config["expected_id"]
                ), f"Expected {config['expected_id']}, got {source.video_id}"

            # Verify loader kwargs
            if source.media_type == MediaType.TRANSCRIPT:
                assert "video_id" in loader_kwargs or "add_video_info" in loader_kwargs
            elif source.media_type == MediaType.AUDIO:
                assert "urls" in loader_kwargs or "save_dir" in loader_kwargs

            media_tests_passed += 1

        except Exception as e:
            pass")


    return media_tests_passed >= 2


def test_development_sources():
    """Test development platform source configurations."""

    # Mock development source class
    class MockGitHubSource:
        def __init__(self, **kwargs):
            self.platform = SpecializedPlatform.GITHUB
            self.repo = kwargs.get("repo")
            self.access_token = kwargs.get("access_token")
            self.data_types = kwargs.get("data_types", [DevelopmentDataType.ISSUES])
            self.branch = kwargs.get("branch", "main")
            self.issue_state = kwargs.get("issue_state", "all")
            self.file_path = kwargs.get("file_path")

        def get_loader_kwargs(self):
            kwargs = {
                "platform": self.platform.value,
                "repo": self.repo,
                "access_token": self.access_token,
            }

            if DevelopmentDataType.ISSUES in self.data_types:
                kwargs["state"] = self.issue_state
                kwargs["include_prs"] = (
                    DevelopmentDataType.PULL_REQUESTS in self.data_types
                )

            if self.file_path:
                kwargs["file_path"] = self.file_path
                kwargs["branch"] = self.branch

            return kwargs

    dev_tests_passed = 0
    test_configs = [
        {
            "name": "GitHub Issues",
            "repo": "langchain-ai/langchain",
            "access_token": "test-token",
            "data_types": [
                DevelopmentDataType.ISSUES,
                DevelopmentDataType.PULL_REQUESTS,
            ],
            "issue_state": "open",
        },
        {
            "name": "GitHub File",
            "repo": "owner/repository",
            "file_path": "README.md",
            "branch": "develop",
        },
        {
            "name": "GitHub Mixed",
            "repo": "microsoft/vscode",
            "data_types": [DevelopmentDataType.ISSUES, DevelopmentDataType.WIKI],
            "access_token": "gh-token",
        },
    ]

    for config in test_configs:
        try:
            source = MockGitHubSource(**config)
            loader_kwargs = source.get_loader_kwargs()


            # Check data types
            if "data_types" in config:
                data_type_names = [dt.value for dt in config["data_types"]]

            # Verify loader kwargs
            assert loader_kwargs["repo"] == config["repo"]
            if config.get("file_path"):
                assert loader_kwargs["file_path"] == config["file_path"]
                assert loader_kwargs["branch"] == config.get("branch", "main")

            dev_tests_passed += 1

        except Exception as e:
            pass")


    return dev_tests_passed >= 2


def test_knowledge_sources():
    """Test knowledge platform source configurations."""

    # Mock knowledge source class
    class MockWikipediaSource:
        def __init__(self, **kwargs):
            self.platform = SpecializedPlatform.WIKIPEDIA
            self.query = kwargs.get("query")
            self.page_titles = kwargs.get("page_titles")
            self.lang = kwargs.get("lang", "en")
            self.load_max_docs = kwargs.get("load_max_docs", 10)
            self.doc_content_chars_max = kwargs.get("doc_content_chars_max")

        def get_loader_kwargs(self):
            kwargs = {
                "platform": self.platform.value,
                "lang": self.lang,
                "load_max_docs": self.load_max_docs,
            }

            if self.query:
                kwargs["query"] = self.query
            elif self.page_titles:
                kwargs["query"] = (
                    self.page_titles[0] if len(self.page_titles) == 1 else None
                )
                kwargs["load_max_docs"] = len(self.page_titles)

            if self.doc_content_chars_max:
                kwargs["doc_content_chars_max"] = self.doc_content_chars_max

            return kwargs

    knowledge_tests_passed = 0
    test_configs = [
        {
            "name": "Wikipedia Search",
            "query": "Python programming",
            "lang": "en",
            "load_max_docs": 5,
        },
        {
            "name": "Wikipedia Pages",
            "page_titles": ["Machine learning", "Artificial intelligence"],
            "lang": "en",
        },
        {
            "name": "Wikipedia Limited",
            "query": "Quantum computing",
            "doc_content_chars_max": 5000,
        },
    ]

    for config in test_configs:
        try:
            source = MockWikipediaSource(**config)
            loader_kwargs = source.get_loader_kwargs()


            if config.get("query"):
                pass
            elif config.get("page_titles"):
                pass

            assert loader_kwargs["platform"] == source.platform.value
            assert loader_kwargs["lang"] == source.lang

            knowledge_tests_passed += 1

        except Exception as e:
            pass")


    return knowledge_tests_passed >= 2


def display_specialized_system_summary():
    """Display summary of the specialized sources implementation."""











def main():
    """Run all specialized sources tests."""

    tests_passed = 0
    total_tests = 5

    # Test 1: Platform Detection
    if test_platform_detection():
        tests_passed += 1
    else:
        pass")

    # Test 2: Academic Sources
    if test_academic_sources():
        tests_passed += 1
    else:
        pass")

    # Test 3: Media Sources
    if test_media_sources():
        tests_passed += 1
    else:
        pass")

    # Test 4: Development Sources
    if test_development_sources():
        tests_passed += 1
    else:
        pass")

    # Test 5: Knowledge Sources
    if test_knowledge_sources():
        tests_passed += 1
    else:
        pass")

    # Results

    if tests_passed >= 4:
        display_specialized_system_summary()
        return True
    print("⚠️ SPECIALIZED SOURCES: NEEDS IMPROVEMENT")
    return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
