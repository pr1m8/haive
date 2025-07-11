"""API-based Web Loaders.

This module contains loaders for various web APIs and scraping services.
"""

import logging
from typing import List, Optional

from langchain_core.document_loaders.base import BaseLoader
from langchain_core.documents import Document

from haive.core.engine.document.loaders.sources.implementation import WebSource

logger = logging.getLogger(__name__)


class BraveSearchSource(WebSource):
    """Brave Search API loader."""

    def __init__(
        self,
        query: str,
        api_key: str,
        count: int = 10,
        search_lang: str = "en",
        country: str = "US",
        include_snippets: bool = True,
        **kwargs,
    ):
        super().__init__(
            source_path="https://api.search.brave.com", requires_auth=True, **kwargs
        )
        self.query = query
        self.api_key = api_key
        self.count = count
        self.search_lang = search_lang
        self.country = country
        self.include_snippets = include_snippets

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a Brave Search loader."""
        try:
            from langchain_community.document_loaders import BraveSearchLoader

            return BraveSearchLoader(
                query=self.query,
                api_key=self.api_key,
                search_kwargs={
                    "count": self.count,
                    "search_lang": self.search_lang,
                    "country": self.country,
                },
            )

        except ImportError:
            logger.warning(
                "BraveSearchLoader not available. Install with: pip install langchain-community"
            )
            return None
        except Exception as e:
            logger.error(f"Failed to create Brave Search loader: {e}")
            return None


class GoogleSearchSource(WebSource):
    """Google Search API loader using Custom Search JSON API."""

    def __init__(
        self, query: str, api_key: str, cse_id: str, num_results: int = 10, **kwargs
    ):
        super().__init__(
            source_path="https://www.googleapis.com/customsearch/v1",
            requires_auth=True,
            **kwargs,
        )
        self.query = query
        self.api_key = api_key
        self.cse_id = cse_id
        self.num_results = num_results

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a Google Search loader."""
        try:
            from langchain_community.document_loaders import GoogleSearchAPILoader

            return GoogleSearchAPILoader(
                query=self.query,
                google_api_key=self.api_key,
                google_cse_id=self.cse_id,
                num_results=self.num_results,
            )

        except ImportError:
            logger.warning("GoogleSearchAPILoader not available")
            return None
        except Exception as e:
            logger.error(f"Failed to create Google Search loader: {e}")
            return None


class ApifyDatasetSource(WebSource):
    """Apify dataset loader for web scraping results."""

    def __init__(
        self,
        dataset_id: str,
        api_token: Optional[str] = None,
        dataset_mapping_function: Optional[callable] = None,
        **kwargs,
    ):
        super().__init__(
            source_path=f"https://api.apify.com/v2/datasets/{dataset_id}",
            requires_auth=bool(api_token),
            **kwargs,
        )
        self.dataset_id = dataset_id
        self.api_token = api_token
        self.dataset_mapping_function = dataset_mapping_function

    def create_loader(self) -> Optional[BaseLoader]:
        """Create an Apify dataset loader."""
        try:
            from langchain_community.document_loaders import ApifyDatasetLoader

            return ApifyDatasetLoader(
                dataset_id=self.dataset_id,
                api_token=self.api_token,
                dataset_mapping_function=self.dataset_mapping_function,
            )

        except ImportError:
            logger.warning(
                "ApifyDatasetLoader not available. Install with: pip install apify-client"
            )
            return None
        except Exception as e:
            logger.error(f"Failed to create Apify dataset loader: {e}")
            return None


class DiffbotSource(WebSource):
    """Diffbot API loader for structured web data extraction."""

    def __init__(
        self,
        urls: List[str],
        api_token: str,
        api_type: str = "article",  # article, product, image, video, discussion
        **kwargs,
    ):
        super().__init__(
            source_path="https://api.diffbot.com", requires_auth=True, **kwargs
        )
        self.urls = urls
        self.api_token = api_token
        self.api_type = api_type

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a Diffbot loader."""
        try:
            from langchain_community.document_loaders import DiffbotLoader

            return DiffbotLoader(
                urls=self.urls,
                api_token=self.api_token,
                api_type=self.api_type,
            )

        except ImportError:
            logger.warning("DiffbotLoader not available")
            return None
        except Exception as e:
            logger.error(f"Failed to create Diffbot loader: {e}")
            return None


class ScrapingBeeSource(WebSource):
    """ScrapingBee API loader for JavaScript-rendered pages."""

    def __init__(
        self,
        urls: List[str],
        api_key: str,
        render_js: bool = True,
        premium_proxy: bool = False,
        country_code: Optional[str] = None,
        wait_for_selector: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(
            source_path="https://app.scrapingbee.com/api/v1",
            requires_auth=True,
            **kwargs,
        )
        self.urls = urls
        self.api_key = api_key
        self.render_js = render_js
        self.premium_proxy = premium_proxy
        self.country_code = country_code
        self.wait_for_selector = wait_for_selector

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a ScrapingBee loader."""
        try:
            # Custom implementation as LangChain doesn't have native support
            return ScrapingBeeLoader(
                urls=self.urls,
                api_key=self.api_key,
                render_js=self.render_js,
                premium_proxy=self.premium_proxy,
                country_code=self.country_code,
                wait_for_selector=self.wait_for_selector,
            )

        except Exception as e:
            logger.error(f"Failed to create ScrapingBee loader: {e}")
            return None


class ScrapflySource(WebSource):
    """Scrapfly API loader for advanced web scraping."""

    def __init__(
        self,
        urls: List[str],
        api_key: str,
        format: str = "markdown",
        asp: bool = True,  # Anti-Scraping Protection
        render_js: bool = True,
        country: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(
            source_path="https://api.scrapfly.io/scrape", requires_auth=True, **kwargs
        )
        self.urls = urls
        self.api_key = api_key
        self.format = format
        self.asp = asp
        self.render_js = render_js
        self.country = country

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a Scrapfly loader."""
        try:
            from langchain_community.document_loaders import ScrapflyLoader

            return ScrapflyLoader(
                urls=self.urls,
                api_key=self.api_key,
                scrape_config={
                    "format": self.format,
                    "asp": self.asp,
                    "render_js": self.render_js,
                    "country": self.country,
                },
            )

        except ImportError:
            logger.warning(
                "ScrapflyLoader not available. Install with: pip install scrapfly-sdk"
            )
            return None
        except Exception as e:
            logger.error(f"Failed to create Scrapfly loader: {e}")
            return None


class NewsAPISource(WebSource):
    """NewsAPI loader for news articles."""

    def __init__(
        self,
        api_key: str,
        query: Optional[str] = None,
        sources: Optional[List[str]] = None,
        domains: Optional[List[str]] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        language: str = "en",
        sort_by: str = "popularity",  # relevancy, popularity, publishedAt
        page_size: int = 100,
        **kwargs,
    ):
        super().__init__(
            source_path="https://newsapi.org/v2", requires_auth=True, **kwargs
        )
        self.api_key = api_key
        self.query = query
        self.sources = sources
        self.domains = domains
        self.from_date = from_date
        self.to_date = to_date
        self.language = language
        self.sort_by = sort_by
        self.page_size = page_size

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a NewsAPI loader."""
        try:
            from langchain_community.document_loaders import NewsAPILoader

            return NewsAPILoader(
                api_key=self.api_key,
                query=self.query,
                sources=self.sources,
                domains=self.domains,
                from_date=self.from_date,
                to_date=self.to_date,
                language=self.language,
                sort_by=self.sort_by,
                page_size=self.page_size,
            )

        except ImportError:
            logger.warning("NewsAPILoader not available")
            return None
        except Exception as e:
            logger.error(f"Failed to create NewsAPI loader: {e}")
            return None


class AssemblyAITranscriptSource(WebSource):
    """AssemblyAI API loader for audio transcription."""

    def __init__(
        self,
        file_path: Optional[str] = None,
        transcript_id: Optional[str] = None,
        api_key: str = None,
        speaker_labels: bool = True,
        auto_chapters: bool = False,
        entity_detection: bool = False,
        **kwargs,
    ):
        super().__init__(
            source_path="https://api.assemblyai.com/v2", requires_auth=True, **kwargs
        )
        self.file_path = file_path
        self.transcript_id = transcript_id
        self.api_key = api_key
        self.speaker_labels = speaker_labels
        self.auto_chapters = auto_chapters
        self.entity_detection = entity_detection

    def create_loader(self) -> Optional[BaseLoader]:
        """Create an AssemblyAI loader."""
        try:
            if self.transcript_id:
                from langchain_community.document_loaders import (
                    AssemblyAIAudioLoaderById,
                )

                return AssemblyAIAudioLoaderById(
                    transcript_id=self.transcript_id,
                    api_key=self.api_key,
                )
            elif self.file_path:
                from langchain_community.document_loaders import (
                    AssemblyAIAudioTranscriptLoader,
                )

                return AssemblyAIAudioTranscriptLoader(
                    file_path=self.file_path,
                    api_key=self.api_key,
                    speaker_labels=self.speaker_labels,
                    auto_chapters=self.auto_chapters,
                    entity_detection=self.entity_detection,
                )
            else:
                raise ValueError("Either file_path or transcript_id must be provided")

        except ImportError:
            logger.warning(
                "AssemblyAI loaders not available. Install with: pip install assemblyai"
            )
            return None
        except Exception as e:
            logger.error(f"Failed to create AssemblyAI loader: {e}")
            return None


class EtherscanSource(WebSource):
    """Etherscan blockchain data loader."""

    def __init__(
        self,
        account: Optional[str] = None,
        contract_address: Optional[str] = None,
        api_key: str = None,
        start_block: int = 0,
        end_block: int = 99999999,
        sort: str = "asc",
        **kwargs,
    ):
        super().__init__(
            source_path="https://api.etherscan.io/api", requires_auth=True, **kwargs
        )
        self.account = account
        self.contract_address = contract_address
        self.api_key = api_key
        self.start_block = start_block
        self.end_block = end_block
        self.sort = sort

    def create_loader(self) -> Optional[BaseLoader]:
        """Create an Etherscan loader."""
        try:
            from langchain_community.document_loaders import EtherscanLoader

            if self.account:
                filter_type = "normal_transaction"
                filter_value = self.account
            elif self.contract_address:
                filter_type = "contract_interaction"
                filter_value = self.contract_address
            else:
                raise ValueError("Either account or contract_address must be provided")

            return EtherscanLoader(
                api_key=self.api_key,
                filter=filter_type,
                account_address=filter_value,
                start_block=self.start_block,
                end_block=self.end_block,
                sort=self.sort,
            )

        except ImportError:
            logger.warning("EtherscanLoader not available")
            return None
        except Exception as e:
            logger.error(f"Failed to create Etherscan loader: {e}")
            return None


# Custom loader implementations


class ScrapingBeeLoader(BaseLoader):
    """Custom loader for ScrapingBee API."""

    def __init__(
        self,
        urls: List[str],
        api_key: str,
        render_js: bool = True,
        premium_proxy: bool = False,
        country_code: Optional[str] = None,
        wait_for_selector: Optional[str] = None,
    ):
        self.urls = urls
        self.api_key = api_key
        self.render_js = render_js
        self.premium_proxy = premium_proxy
        self.country_code = country_code
        self.wait_for_selector = wait_for_selector

    def load(self) -> List[Document]:
        """Load pages using ScrapingBee API."""
        try:
            import requests

            documents = []

            for url in self.urls:
                params = {
                    "api_key": self.api_key,
                    "url": url,
                    "render_js": str(self.render_js).lower(),
                    "premium_proxy": str(self.premium_proxy).lower(),
                }

                if self.country_code:
                    params["country_code"] = self.country_code
                if self.wait_for_selector:
                    params["wait_for_selector"] = self.wait_for_selector

                response = requests.get(
                    "https://app.scrapingbee.com/api/v1",
                    params=params,
                )

                if response.status_code == 200:
                    content = response.text

                    metadata = {
                        "source": url,
                        "type": "scrapingbee_web_page",
                        "render_js": self.render_js,
                    }

                    documents.append(Document(page_content=content, metadata=metadata))
                else:
                    logger.error(f"Failed to scrape {url}: {response.status_code}")

            return documents

        except Exception as e:
            logger.error(f"Failed to load with ScrapingBee: {e}")
            return []


# Export API sources
__all__ = [
    "BraveSearchSource",
    "GoogleSearchSource",
    "ApifyDatasetSource",
    "DiffbotSource",
    "ScrapingBeeSource",
    "ScrapflySource",
    "NewsAPISource",
    "AssemblyAITranscriptSource",
    "EtherscanSource",
    "ScrapingBeeLoader",
]
